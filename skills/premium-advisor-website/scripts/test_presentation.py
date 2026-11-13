"""Protect card inventory, destinations, script behavior and approved icon placement."""
import re
import unittest

import render
from numbering import without_numbering
from presentation import apply_presentation


class PresentationTests(unittest.TestCase):
    def test_all_sections_preserve_behavior_and_are_idempotent(self):
        design = render.contract()
        icons = arrows = 0
        for relative in design['sha256']:
            source = without_numbering((render.TEMPLATES / relative).read_text(encoding='utf-8'))
            result = apply_presentation(source)
            with self.subTest(section=relative):
                self.assertEqual(apply_presentation(result), result)
                self.assertEqual(re.findall(r'\b(?:href|src|poster|id|aria-controls)="[^"]*"', source), re.findall(r'\b(?:href|src|poster|id|aria-controls)="[^"]*"', result))
                self.assertEqual(re.findall(r'<script\b.*?</script>', source, re.S), re.findall(r'<script\b.*?</script>', result, re.S))
                markup = re.sub(r'<(?:style|script)\b[^>]*>.*?</(?:style|script)>', '', result, flags=re.S)
                self.assertNotRegex(markup, r'[↗→↓↑➜➡]')
                if relative.endswith(('06-services.html', '03-service-accordions.html')):
                    self.assertEqual(result.count('class="premium-service-heading"'), 8)
                icons += result.count('class="premium-service-heading"')
                arrows += result.count('class="premium-cta-arrow"')
        self.assertEqual(icons, 16)
        self.assertEqual(arrows, 16)
        render.contract()

    def test_scripts_are_not_transformed(self):
        script = '<script>const example="<div class=\"premium-service-heading\">↗</div>";</script>'
        self.assertEqual(apply_presentation(script), script)

    def test_substitution_applies_and_reports_policies(self):
        self.assertIn('restrained-arrows-responsive-v1', render.OUTPUT_POLICIES)
        self.assertIn('service-icons-v3', render.OUTPUT_POLICIES)
        values, paragraphs = render.prepare({'values': {'advisor_name': 'Test Advisor'}}, render.contract())
        source = (render.TEMPLATES / 'ghl-services-sections-inline/03-service-accordions.html').read_text(encoding='utf-8')
        result, _ = render.substitute(source, values, paragraphs)
        self.assertEqual(result.count('class="premium-service-heading"'), 8)
        self.assertIn('align-items:center;gap:14px', result)


if __name__ == '__main__':
    unittest.main()
