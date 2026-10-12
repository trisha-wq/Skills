"""Check MVP section inventory, CSS geometry, and scripts against the locked pilot."""
import argparse
import json
import re
from pathlib import Path
from render import layout_shape, normalize_css, verify_template_integrity


def verify(output, include_legacy=False):
    design = verify_template_integrity()
    output = Path(output)
    expected = [f'section-{n:02d}.html' for n in range(1, 10 if include_legacy else 9)]
    if sorted(p.name for p in output.glob('section-*.html')) != expected:
        raise ValueError('MVP section inventory changed')
    folder = Path(__file__).resolve().parents[1] / 'assets/template'
    for number, name in enumerate(expected, 1):
        original = (folder / (name if number < 9 else 'legacy-optional.html')).read_text(encoding='utf-8-sig')
        rendered = (output / name).read_text(encoding='utf-8')
        if normalize_css(original) != normalize_css(rendered):
            raise ValueError('MVP CSS geometry changed: ' + name)
        if layout_shape(original) != layout_shape(rendered):
            raise ValueError('MVP DOM layout changed: ' + name)
        if re.findall(r'<script\b[^>]*>.*?</script>', original, re.S | re.I) != re.findall(r'<script\b[^>]*>.*?</script>', rendered, re.S | re.I):
            raise ValueError('MVP scripts changed: ' + name)
    return {'designId': design['design_id'], 'sections': len(expected), 'templateIntegrityVerified': True, 'cssGeometryPreserved': True, 'domLayoutPreserved': True, 'scriptsPreserved': True, 'renderedVerified': False}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', required=True)
    parser.add_argument('--include-legacy', action='store_true')
    args = parser.parse_args()
    print(json.dumps(verify(args.output, args.include_legacy), indent=2))
