"""Rotate hero backgrounds per new site; persist each site's chosen source."""
import html
import json
import os
import re
import time
from pathlib import Path
from urllib.parse import urlparse

POLICY = 'background-video-rotation-v1'
CATALOG = Path(__file__).resolve().parents[1] / 'assets/background-videos.json'


def validate_background(url):
    parsed = urlparse(url)
    if parsed.scheme != 'https' or not parsed.hostname or not parsed.path.lower().endswith('.mp4'):
        raise ValueError('background_video_url must be a public HTTPS MP4 URL')
    return url


def default_state_file(values_path):
    for parent in Path(values_path).resolve().parents:
        if (parent / '.git').exists():
            return parent / '.premium-background-video-rotation.json'
    return Path.cwd() / '.premium-background-video-rotation.json'


def write_json(path, data):
    path = Path(path)
    temporary = path.with_name(path.name + '.tmp')
    temporary.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    temporary.replace(path)


def assign_background(data, values_path, state_file=None):
    """Called once per render, never by verification or page loads."""
    if data.get('background_video_url'):
        return validate_background(data['background_video_url'])
    catalog = json.loads(CATALOG.read_text(encoding='utf-8'))
    pool = [validate_background(url) for url in catalog['videos']]
    if len(pool) < 2 or len(set(pool)) != len(pool):
        raise ValueError('Background rotation needs at least two distinct videos')
    state_file = Path(state_file) if state_file else default_state_file(values_path)
    state_file.parent.mkdir(parents=True, exist_ok=True)
    lock = state_file.with_name(state_file.name + '.lock')
    for attempt in range(50):
        try:
            descriptor = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
            break
        except FileExistsError:
            if attempt == 49:
                raise RuntimeError('Background rotation is busy; retry after the other build finishes')
            time.sleep(0.1)
    os.close(descriptor)
    try:
        state = json.loads(state_file.read_text(encoding='utf-8')) if state_file.exists() else {
            'next_index': catalog['next_index_for_new_state'], 'assignments': {}}
        project = str(Path(values_path).resolve())
        assignments = state.setdefault('assignments', {})
        if project in assignments:
            selected = validate_background(assignments[project])
        else:
            index = state['next_index'] % len(pool)
            selected = pool[index]
            assignments[project] = selected
            state['next_index'] = (index + 1) % len(pool)
        data['background_video_url'] = selected
        data.setdefault('sources', {})['backgroundVideo'] = {'url': selected, 'policy': POLICY}
        # Saving state first permits a retry to recover the same assignment.
        write_json(state_file, state)
        write_json(values_path, data)
        return selected
    finally:
        lock.unlink()


def apply_background_video(code, url=None):
    if not url:
        return code
    validate_background(url)
    def replace_video(match):
        video = match[0]
        previous = re.search(r'<source\b[^>]*\bsrc="([^"]*)"', video)
        if not previous:
            raise ValueError('Background video source element is missing')
        if html.unescape(previous[1]) != url:
            # A poster belonging to the previous clip must not describe a different one.
            video = re.sub(r'\s+poster="[^"]*"', '', video, count=1)
        return re.sub(r'(<source\b[^>]*\bsrc=")[^"]*(")',
                      lambda m: m[1] + html.escape(url, quote=True) + m[2], video, count=1)
    return re.sub(r'<video\b(?=[^>]*\bclass="[^"]*\bpfg-background-video\b)[^>]*>.*?</video>',
                  replace_video, code, flags=re.S)
