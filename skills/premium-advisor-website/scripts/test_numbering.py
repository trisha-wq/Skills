"""Regression checks for the approved unnumbered Premium output policy."""
import json
import re
import tempfile
import unittest
from pathlib import Path

import render
from numbering import NumberingParser, without_numbering


class NumberingTests(unittest.TestCase):
    def wrap(self, body):
        return '<style>.test{display:block}</style><div class="premium-template test">' + body + '</div>'

    def test_numbering_contexts(self):
        body = '<div class="pfg-path-tabs"><button role="tab"><span>01</span>Family<span aria-hidden="true">&rarr;</span></button></div><div class="pfg-service-number"><span>02</span><span aria-hidden="true">&rarr;</span></div><div class="pfg-event-topics"><div><span>03</span><strong>Learn</strong></div></div><div class="pfg-step"><span>01 / LISTEN</span></div><span class="srs-partner-index">4</span><article class="pfg-resource-panel"><span class="pfg-resource-number">5</span><div>Assessment</div><div class="pfg-resource-action">Start</div></article>'
        result = without_numbering(self.wrap(body))
        self.assertFalse(NumberingParser(result).edits)
        self.assertNotRegex(result, r'<span[^>]*>\d+')
        self.assertIn('<span>LISTEN</span>', result)
        self.assertEqual(result.count('&rarr;'), 2)
        self.assertIn('grid-template-columns:minmax(0,1fr) auto', result)
        self.assertIn('.pfg-resource-action{grid-column:auto}', result)
        self.assertIn('@media(max-width:1000px)', result)

    def test_substantive_numbers(self):
        source = self.wrap('<p>469-853-5696, 1997, $97, 70%, 21st Century, 60 Seconds, 14 videos</p><span>2026</span><h3>21st Century Trust Funding Method</h3>')
        self.assertEqual(without_numbering(source), source)

    def test_script_literals_are_not_html(self):
        source = self.wrap('<script>const label="<span class=\'srs-partner-index\'>1</span>";</script>')
        self.assertEqual(without_numbering(source), source)

    def test_services_uses_advisor_elder_care_link_and_removes_quote(self):
        elder_care = 'https://smartmoney.talk/n-n-2vw3dv-AdvisorIdentity-n.VerifiedLink'
        data = {'values': {'advisor_name': 'Test Advisor', 'library_risk_02_url': elder_care, 'bridge_url': 'https://example.com/wrong-bridge', 'instant_quote_url': 'https://example.com/quote'}}
        values, paragraphs = render.prepare(data, render.contract())
        self.assertEqual(values['bridge_url'], elder_care)
        original = (render.TEMPLATES / 'ghl-services-sections-inline/05-planning-resources.html').read_text(encoding='utf-8')
        result, missing = render.substitute(original, values, paragraphs)
        self.assertIn('href="' + elder_care + '"', result)
        self.assertNotIn('Instant Quote', result)
        self.assertNotIn('instant life insurance quote', result)
        self.assertNotIn('instant_quote_url', missing)
        self.assertNotIn('example.com', result)

    def test_services_missing_or_wrong_video_is_not_substituted(self):
        values, paragraphs = render.prepare({'values': {'advisor_name': 'Test Advisor', 'bridge_url': 'https://example.com/unverified'}}, render.contract())
        original = (render.TEMPLATES / 'ghl-services-sections-inline/05-planning-resources.html').read_text(encoding='utf-8')
        result, missing = render.substitute(original, values, paragraphs)
        self.assertIn('data-unresolved="bridge_url"', result)
        self.assertNotIn('example.com', result)
        with self.assertRaises(ValueError):
            render.prepare({'values': {'advisor_name': 'Test Advisor', 'library_risk_02_url': 'https://smartmoney.talk/n-n-WrongVideo-Advisor-n.Link'}}, render.contract())

    def test_line_endings_and_entities(self):
        source = self.wrap('<span class="srs-partner-index">&#49;</span>\r\n<p>Phone 469-853-5696</p>')
        result = without_numbering(source)
        self.assertIn('\r\n<p>Phone 469-853-5696</p>', result)
        self.assertNotIn('&#49;', result)

    def test_pinned_sections_preserve_destinations_and_scripts(self):
        design = render.contract()
        removed = 0
        for relative in design['sha256']:
            source = (render.TEMPLATES / relative).read_text(encoding='utf-8')
            removed += len(NumberingParser(source).edits)
            result = without_numbering(source)
            with self.subTest(section=relative):
                self.assertFalse(NumberingParser(result).edits)
                self.assertEqual(without_numbering(result), result)
                self.assertEqual(re.findall(r'(?:href|src|poster|id|aria-controls)="[^"]*"', result), re.findall(r'(?:href|src|poster|id|aria-controls)="[^"]*"', source))
                self.assertEqual(re.findall(r'<script\b.*?</script>', result, re.S), re.findall(r'<script\b.*?</script>', source, re.S))
        self.assertEqual(removed, 37)
        render.contract()

    def test_full_render_and_verification(self):
        with tempfile.TemporaryDirectory() as temporary:
            values = Path(temporary) / 'values.json'
            values.write_text(json.dumps({'values': {'advisor_name': 'Test Advisor'}}), encoding='utf-8')
            output = Path(temporary) / 'output'
            report = render.render(values, output)
            self.assertTrue(report['templateIntegrityVerified'])
            self.assertTrue(report['outputPolicyVerified'])
            self.assertFalse(report['contentOnlyVerified'])
            self.assertEqual(len(list(output.glob('ghl-*/*.html'))), 56)
            target = output / 'ghl-home-sections-inline/05-planning-priorities.html'
            target.write_text(target.read_text(encoding='utf-8').replace('Family', 'CHANGED', 1), encoding='utf-8')
            with self.assertRaises(ValueError):
                render.verify(json.loads(values.read_text()), output)


if __name__ == '__main__':
    unittest.main()
