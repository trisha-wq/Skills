import unittest
from pathlib import Path
from legacy_pricing import apply_legacy_pricing


class LegacyPricingTests(unittest.TestCase):
    def test_targeted_price_preserves_other_content(self):
        source = '<a href="https://example.com/order">Leverage Your Guidebook For $97</a><p>Other product $97; 1997; 97 stories.</p>'
        expected = source.replace('Leverage Your Guidebook For $97', 'Leverage Your Guidebook For $59')
        result = apply_legacy_pricing(source)
        self.assertEqual(result, expected)
        self.assertEqual(apply_legacy_pricing(result), result)

    def test_renderer_uses_new_price_with_pinned_template(self):
        import render
        render.contract()
        template = render.TEMPLATES / 'ghl-legacy-stories-sections-inline/03-guidebook.html'
        source = template.read_text(encoding='utf-8')
        self.assertIn('Leverage Your Guidebook For $97', source)
        result, _ = render.substitute(source, {'advisor_name': 'Test Advisor'}, [])
        self.assertIn('Leverage Your Guidebook For $59', result)
        self.assertNotIn('Leverage Your Guidebook For $97', result)


if __name__ == '__main__':
    unittest.main()
