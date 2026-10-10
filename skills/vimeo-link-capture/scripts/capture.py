"""GET-only Vimeo capture using the existing integration's credential conventions."""
import argparse
import csv
import json
import os
import re
import sys
import time
from urllib.error import HTTPError, URLError
from urllib.request import Request, HTTPRedirectHandler, build_opener
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import parse_qs, urljoin, urlparse

BASE = 'https://api.vimeo.com'


class CaptureError(RuntimeError):
    pass


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def load_credentials(path):
    # Read only the existing integration's credential keys; never execute a file.
    for line in path.read_text(encoding='utf-8-sig').splitlines():
        line = line.strip()
        if line.startswith('export '):
            line = line[7:].strip()
        key, separator, value = line.partition('=')
        key = key.strip()
        if not separator or key not in ('VIMEO_ACCESS_TOKEN', 'VIMEO_TEAM_OWNER_USER_IDS'):
            continue
        value = value.strip()
        if value[:1] in ('"', "'"):
            quote = value[0]
            end = value.find(quote, 1)
            if end < 0:
                raise CaptureError('Invalid quoted Vimeo configuration value.')
            value = value[1:end]
        else:
            value = value.split(' #', 1)[0].strip()
        os.environ.setdefault(key, value)


def normalize(value):
    return ' '.join(str(value).split()).casefold()


def resource_id(uri):
    return str(uri or '').rstrip('/').split('/')[-1]


class Client:
    def __init__(self, token):
        if not token.strip():
            raise CaptureError('VIMEO_ACCESS_TOKEN is missing; configure it locally or use --env-file.')
        self.opener = build_opener(NoRedirect())
        self.headers = {'Authorization': 'Bearer ' + token.strip(),
                        'Accept': 'application/vnd.vimeo.*+json;version=3.4'}

    @staticmethod
    def safe_url(path):
        url = urljoin(BASE + '/', path)
        if urlparse(url).scheme != 'https' or urlparse(url).netloc != 'api.vimeo.com':
            raise CaptureError('Unexpected external Vimeo API URL.')
        return url

    def get(self, path, params=None):
        url = self.safe_url(path)
        for attempt in range(3):
            try:
                from urllib.parse import urlencode
                request_url = url + ('&' if '?' in url else '?') + urlencode(params) if params else url
                with self.opener.open(Request(request_url, headers=self.headers), timeout=30) as response:
                    status = response.status
                    headers = response.headers
                    body = response.read()
            except HTTPError as exc:
                status, headers, body = exc.code, exc.headers, b''
            except (URLError, TimeoutError, OSError):
                if attempt < 2:
                    time.sleep(0.5 * 2**attempt)
                    continue
                raise CaptureError('Vimeo network request failed after retries.') from None
            if status == 429 or status >= 500:
                if attempt < 2:
                    try:
                        delay = float(headers.get('Retry-After', 0.5 * 2**attempt))
                    except ValueError:
                        delay = 0.5 * 2**attempt
                    if delay > 60:
                        raise CaptureError('Vimeo rate limited the request; retry later.')
                    time.sleep(max(0, delay))
                    continue
            if not 200 <= status < 300:
                raise CaptureError(f'Vimeo API HTTP {status} at {urlparse(url).path}; check token scopes and library access.')
            try:
                data = json.loads(body)
            except ValueError:
                raise CaptureError('Vimeo returned invalid JSON.') from None
            if not isinstance(data, dict):
                raise CaptureError('Unexpected Vimeo API response.')
            return data

    def pages(self, path):
        seen = set()
        params = {'per_page': 100, 'page': 1}
        while path:
            url = self.safe_url(path)
            if url in seen:
                raise CaptureError('Vimeo pagination repeated a page.')
            seen.add(url)
            payload = self.get(path, params)
            params = None
            if not isinstance(payload.get('data'), list):
                raise CaptureError('Vimeo list response has no data array.')
            yield from (item for item in payload['data'] if isinstance(item, dict))
            path = (payload.get('paging') or {}).get('next')


def connections(raw):
    return (raw.get('metadata') or {}).get('connections') or {}


def team_owner(raw):
    owner = raw.get('owner_user_id') or raw.get('owner_id')
    if not owner:
        owner = resource_id((raw.get('user') or {}).get('uri') or
                            (connections(raw).get('owner') or {}).get('uri'))
    return str(owner) if str(owner).isdigit() else ''


def discover(client, owner_id, configured, diagnostics):
    account = client.get('/me')
    own = resource_id(account.get('uri'))
    if not own.isdigit():
        raise CaptureError('Authenticated account has no numeric user ID.')
    owners = set(configured)
    folder_sources = []
    if owner_id:
        owners = {owner_id}
    else:
        folder_sources.append((own, (connections(account).get('folders') or {}).get('uri') or '/me/projects'))
        teams_uri = (connections(account).get('teams') or {}).get('uri')
        if teams_uri:
            try:
                owners.update(filter(None, (team_owner(t) for t in client.pages(teams_uri))))
            except CaptureError as exc:
                diagnostics.append(str(exc))
        try:
            owner = team_owner(client.get('/me/team'))
            if owner:
                owners.add(owner)
        except CaptureError as exc:
            diagnostics.append(str(exc))
        owners.discard(own)
    folder_sources.extend((owner, f'/users/{owner}/folders') for owner in sorted(owners))
    folders = {}
    for owner, uri in folder_sources:
        try:
            for folder in client.pages(uri):
                if folder.get('uri'):
                    folders[(owner, folder['uri'])] = dict(folder, owner_id=owner)
        except CaptureError as exc:
            diagnostics.append(str(exc))
    return {'name': account.get('name'), 'uri': account.get('uri')}, list(folders.values())


def select_folder(folders, advisor, uri=None):
    matches = [f for f in folders if (f.get('uri') == uri if uri else
                                    normalize(f.get('name', '')) == normalize(advisor))]
    if len(matches) != 1:
        candidates = [{'name': f.get('name'), 'uri': f.get('uri'), 'owner_id': f['owner_id']} for f in matches]
        raise CaptureError('Advisor folder missing or ambiguous; select --owner-id / --folder-uri. Matches: ' + json.dumps(candidates))
    return matches[0]


def select_link(video):
    candidates = []
    groups = [('files', video.get('files') or []),
              ('play.progressive', (video.get('play') or {}).get('progressive') or [])]
    for source, files in groups:
        for file in files:
            if not isinstance(file, dict):
                continue
            url = str(file.get('link') or '')
            parsed = urlparse(url)
            path720 = '/rendition/720p/' in parsed.path
            if str(file.get('height')) != '720' and not path720:
                continue
            if parsed.scheme != 'https':
                continue
            candidates.append({'source': source, 'url': url, 'expires': file.get('expires'),
                               'height': file.get('height'), 'type': file.get('type')})
    video_id = resource_id(video.get('uri'))
    eligible = [c['url'] for c in candidates if c['source'] == 'files'
                and urlparse(c['url']).netloc == 'player.vimeo.com'
                and urlparse(c['url']).path.startswith(f'/progressive_redirect/playback/{video_id}/rendition/720p/')
                and parse_qs(urlparse(c['url']).query).get('signature')]
    eligible = list(dict.fromkeys(eligible))
    if len(eligible) == 1:
        return eligible[0], 'captured', candidates
    return '', 'ambiguous_720p_links' if eligible else 'missing_signed_720p_files_link', candidates


def capture(client, folder, diagnostics):
    stack = [(resource_id(folder['uri']), folder['name'], 0)]
    visited = set()
    videos = {}
    while stack:
        folder_id, path, depth = stack.pop()
        if folder_id in visited:
            continue
        visited.add(folder_id)
        if not folder_id.isdigit() or depth > 10:
            diagnostics.append(f'Cannot traverse folder {path}: invalid ID or depth limit.')
            continue
        try:
            items = list(client.pages(f'/users/{folder["owner_id"]}/projects/{folder_id}/items'))
        except CaptureError as exc:
            diagnostics.append(str(exc))
            continue
        for item in items:
            if item.get('type') == 'folder' and isinstance(item.get('folder'), dict):
                child = item['folder']
                stack.append((resource_id(child.get('uri')), path + ' / ' + str(child.get('name', '')), depth + 1))
            elif item.get('type') == 'video' and isinstance(item.get('video'), dict):
                video = item['video']
                vid = resource_id(video.get('uri'))
                if not vid.isdigit():
                    diagnostics.append(f'Invalid video ID in {path}.')
                    continue
                if vid in videos:
                    videos[vid]['folder_paths'].append(path)
                    continue
                record = {'video_id': vid, 'video_name': video.get('name'), 'folder_paths': [path],
                          'video_uri': video.get('uri'), 'url_720p': '', 'status': 'api_error'}
                try:
                    details = client.get(f'/videos/{vid}')
                    url, status, candidates = select_link(details)
                    record.update(url_720p=url, status=status, candidates=candidates,
                                  video_name=details.get('name') or video.get('name'))
                except CaptureError as exc:
                    record['error'] = str(exc)
                videos[vid] = record
    return sorted(videos.values(), key=lambda v: (normalize(v['video_name']), v['video_id']))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--advisor', required=True)
    parser.add_argument('--env-file', type=Path)
    parser.add_argument('--owner-id')
    parser.add_argument('--folder-uri')
    parser.add_argument('--output-dir', type=Path, required=True)
    args = parser.parse_args()
    try:
        if args.env_file:
            if not args.env_file.is_file():
                raise CaptureError('Specified env file does not exist.')
            load_credentials(args.env_file)
        configured = [v.strip() for v in os.getenv('VIMEO_TEAM_OWNER_USER_IDS', '').split(',') if v.strip()]
        if any(not v.isdigit() for v in configured + ([args.owner_id] if args.owner_id else [])):
            raise CaptureError('Team owner IDs must be numeric.')
        client = Client(os.getenv('VIMEO_ACCESS_TOKEN', ''))
        diagnostics = []
        account, folders = discover(client, args.owner_id, configured, diagnostics)
        folder = select_folder(folders, args.advisor, args.folder_uri)
        records = capture(client, folder, diagnostics)
        captured = sum(v['status'] == 'captured' for v in records)
        result = {'advisor': args.advisor, 'captured_at': datetime.now(timezone.utc).isoformat(),
                  'account': account, 'folder': {k: folder.get(k) for k in ('name', 'uri', 'owner_id')},
                  'captured_count': captured, 'unresolved_count': len(records) - captured,
                  'diagnostics': diagnostics, 'videos': records}
        args.output_dir.mkdir(parents=True, exist_ok=True)
        (args.output_dir / 'capture.json').write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding='utf-8')
        with (args.output_dir / 'capture.csv').open('w', newline='', encoding='utf-8') as handle:
            writer = csv.DictWriter(handle, fieldnames=['video_id', 'video_name', 'folder_paths', 'status', 'url_720p'])
            writer.writeheader()
            for record in records:
                writer.writerow({k: ' | '.join(record[k]) if k == 'folder_paths' else record[k] for k in writer.fieldnames})
        print(f'Captured {captured}; unresolved {len(records) - captured}; API diagnostics {len(diagnostics)}. Output: {args.output_dir.resolve()}')
        return 2 if len(records) != captured or not records or diagnostics else 0
    except CaptureError as exc:
        print(str(exc), file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
