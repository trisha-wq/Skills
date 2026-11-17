"""Verify arrow reduction without changing destinations or functional controls."""
import re
import unittest
from pathlib import Path
from arrows import with_restrained_arrows
from numbering import without_numbering


class ArrowTests(unittest.TestCase):
    def test_all_pinned_sections(self):
        root = Path(__file__).resolve().parents[1] / 'assets/template'
        if not root.exists():
            root = Path(r'C:\Users\Administrator\.codex\skills\premium-advisor-website\assets\template')
        files = list(root.glob('*/*.html'))
        self.assertEqual(len(files), 56)
        for file in files:
            original = without_numbering(file.read_text(encoding='utf-8'))
            result = with_restrained_arrows(original)
            self.assertEqual(result, with_restrained_arrows(result), str(file))
            for attr in ('href', 'src', 'id', 'aria-controls', 'aria-selected'):
                pattern = rf'\b{attr}="[^"]*"'
                self.assertEqual(re.findall(pattern, original), re.findall(pattern, result), (str(file), attr))
            self.assertNotIn('<span aria-hidden="true">\u2197</span>', result)
            self.assertNotIn("content:'\u2197'", result)
            if file.name == '02-hero.html' and 'home' in file.parent.name:
                self.assertEqual(result.count('class="premium-cta-arrow"'), 2)
            if 'consultation' in file.name:
                self.assertEqual(result.count('class="premium-cta-arrow"'), 1)
            if file.name == '06-services.html':
                self.assertNotIn('<div class="pfg-service-number">', result)

    def test_encoded_arrows_and_functional_controls(self):
        source = ('<div class="premium-template"><div class="pfg-actions">'
                  '<a href="/events"><span aria-hidden="true">&#8599;</span>Events</a></div>'
                  '<button aria-expanded="false">Menu +</button><span>\u25b6</span>'
                  '<script>const arrow="\u2197";</script></div>')
        result = with_restrained_arrows(source)
        self.assertIn('class="premium-cta-arrow"', result)
        self.assertIn('Menu +', result)
        self.assertIn('<span>\u25b6</span>', result)
        self.assertIn('const arrow="\u2197"', result)


if __name__ == '__main__':
    unittest.main()
