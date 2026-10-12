"""Render the portable Ardie-based Premium sections using content-only substitutions."""
import argparse
import csv
import hashlib
import html
import json
import re
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse

SKILL = Path(__file__).resolve().parents[1]
TEMPLATES = SKILL / 'assets/template'
TOKEN = re.compile(r'\{\{([a-z0-9_]+)\}\}')


def contract():
    data = json.loads((SKILL / 'assets/design-contract.json').read_text(encoding='utf-8'))
    for relative, expected in data['sha256'].items():
        path = TEMPLATES / relative
        if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != expected:
            raise ValueError('Baseline template changed: ' + relative + '. Review the design before explicitly updating its contract.')
    return data


def prepare(data, design):
    values = dict(data.get('values', {}))
    if not isinstance(values.get('advisor_name'), str) or not values['advisor_name'].strip():
        raise ValueError('values.advisor_name is required')
    if set(values) - set(design['tokens']):
        raise ValueError('Unknown values: ' + ', '.join(sorted(set(values) - set(design['tokens']))))
    for key, value in values.items():
        if not isinstance(value, str):
            raise ValueError(key + ' must be a string')
        if not value:
            continue
        if key.startswith('theme_'):
            if not re.fullmatch(r'#[a-fA-F0-9]{6}', value):
                raise ValueError(key + ' must be a six-digit hex color')
        elif key in {'roster_width', 'roster_height', 'copyright_year'}:
            if not value.isdigit() or int(value) <= 0:
                raise ValueError(key + ' must be a positive integer string')
        elif key.endswith(('_url', '_thumbnail')):
            parsed = urlparse(value)
            if parsed.scheme != 'https' or not parsed.hostname:
                raise ValueError(key + ' must be a public HTTPS URL')
            if key.endswith('_thumbnail') or key in {'logo_url', 'headshot_url', 'roster_url'}:
                if parsed.hostname != 'assets.cdn.filesafe.space':
                    raise ValueError(key + ' must use the verified GHL-hosted original image URL')
            elif key.startswith(('library_risk_', 'library_tax_')):
                if parsed.hostname != 'smartmoney.talk' or '/n-n-' not in parsed.path:
                    raise ValueError(key + ' requires the advisor-specific WebPrez WITHOUT Viewing Notice link')
            elif key.startswith(('video_', 'home_video_', 'library_kai_zen_')):
                if parsed.hostname != 'player.vimeo.com' or '/rendition/720p/' not in parsed.path or 'signature=' not in parsed.query:
                    raise ValueError(key + ' requires the complete signed Vimeo 720p file URL')
    if 'bio_paragraphs' in values:
        raise ValueError('Supply bios.about paragraph arrays, not raw HTML in values')
    paragraphs = data.get('bios', {}).get('about', [])
    if not isinstance(paragraphs, list) or any(not isinstance(p, str) for p in paragraphs):
        raise ValueError('bios.about must be a paragraph array')
    for key in ['advisor_name', 'advisor_title', 'advisor_credentials', 'firm_name']:
        if values.get(key):
            values.setdefault(key + '_upper', values[key].upper())
    values.setdefault('theme_primary', '#123238')
    values.setdefault('theme_deep', '#0d292f')
    return values, paragraphs


def substitute(original, values, paragraphs):
    missing = set()
    def replace(match):
        key = match[1]
        if key == 'bio_paragraphs' and paragraphs:
            return ''.join('<p>' + html.escape(p) + '</p>' for p in paragraphs)
        if values.get(key):
            return html.escape(values[key], quote=True)
        missing.add(key)
        return match[0]
    result = TOKEN.sub(replace, original)
    # Keep unavailable actions in place, but never navigate to placeholder URLs.
    result = re.sub(r'href="\{\{([a-z0-9_]+)\}\}"', lambda m: 'aria-disabled="true" data-unresolved="' + m[1] + '"', result)
    return result, missing


class Inventory(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids, self.categories = [], {}
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'id' in attrs:
            self.ids.append(attrs['id'])
        if 'data-category' in attrs:
            category = attrs['data-category']
            self.categories[category] = self.categories.get(category, 0) + 1


def verify(data, output):
    design = contract()
    values, paragraphs = prepare(data, design)
    output = Path(output)
    expected_files = {f for sections in design['section_files'].values() for f in sections}
    actual_files = {p.relative_to(output).as_posix() for p in output.glob('ghl-*-sections-inline/*.html')}
    if actual_files != expected_files:
        raise ValueError('Missing, extra, or reordered section files')
    all_code, missing = [], set()
    for relative in sorted(expected_files):
        expected, unresolved = substitute((TEMPLATES / relative).read_text(encoding='utf-8'), values, paragraphs)
        actual = (output / relative).read_text(encoding='utf-8')
        if expected != actual:
            raise ValueError('Content-only template check failed: ' + relative)
        missing.update(unresolved)
        all_code.append(actual)
    inventory = Inventory()
    inventory.feed('\n'.join(all_code))
    if len(inventory.ids) != len(set(inventory.ids)):
        raise ValueError('Duplicate IDs across sections')
    if inventory.categories != design['library_categories']:
        raise ValueError('Video categories or card counts changed')
    return {'designId': design['design_id'], 'reference': design['reference_url'], 'sectionCounts': design['section_counts'], 'templateIntegrityVerified': True, 'contentOnlyVerified': True, 'cssAndScriptsPreserved': True, 'uniqueIdsVerified': True, 'missing': sorted(missing), 'allValuesPresent': not missing, 'readyForInstallation': False, 'destinationsIdentityVerified': False, 'renderedVerified': False, 'playbackVerified': False, 'published': False}


def render(values_path, output):
    data = json.loads(Path(values_path).read_text(encoding='utf-8-sig'))
    design = contract()
    values, paragraphs = prepare(data, design)
    output = Path(output).resolve()
    if output == SKILL or SKILL in output.parents:
        raise ValueError('Output must be outside the installed skill')
    if output.exists() and any(output.iterdir()):
        raise ValueError('Use a new/empty output directory to preserve existing work')
    output.mkdir(parents=True, exist_ok=True)
    pages = {}
    for page, files in design['section_files'].items():
        pages[page] = []
        for relative in files:
            rendered, _ = substitute((TEMPLATES / relative).read_text(encoding='utf-8'), values, paragraphs)
            target = output / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(rendered, encoding='utf-8')
            pages[page].append(rendered)
    review = output / 'review'
    review.mkdir()
    for page in [*pages, 'combined-preview']:
        combined = ''.join(''.join(pages[p]) for p in (pages if page == 'combined-preview' else [page]))
        for route in pages:
            combined = combined.replace('href="/' + route + '"', 'href="' + route + '-sections-inline.html"')
        preview = '<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>' + html.escape(values['advisor_name']) + '</title><style>body{margin:0}html{scroll-behavior:smooth}@media(prefers-reduced-motion:reduce){html{scroll-behavior:auto}}</style></head><body>' + combined + '</body></html>'
        filename = 'combined-preview.html' if page == 'combined-preview' else page + '-sections-inline.html'
        (review / filename).write_text(preview, encoding='utf-8')
    report = verify(data, output)
    (output / 'verification.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    with (output / 'missing-values.csv').open('w', newline='', encoding='utf-8') as handle:
        writer = csv.writer(handle)
        writer.writerow(['key', 'status'])
        writer.writerows((key, 'needs_verified_source') for key in report['missing'])
    (output / 'source-manifest.json').write_text(json.dumps({'designId': design['design_id'], 'reference': design['reference_url'], 'sectionFiles': design['section_files'], 'sources': data.get('sources', {})}, indent=2) + '\n', encoding='utf-8')
    print('Rendered 56 locked Premium sections across eight pages; ' + str(len(report['missing'])) + ' unresolved values. Not published.')
    return report


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--values', required=True)
    parser.add_argument('--output', required=True)
    parser.add_argument('--verify-only', action='store_true')
    args = parser.parse_args()
    if args.verify_only:
        print(json.dumps(verify(json.loads(Path(args.values).read_text(encoding='utf-8-sig')), args.output), indent=2))
    else:
        render(args.values, args.output)
