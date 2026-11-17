"""Check the footer policy stays scoped and all rendered pages remain verifiable."""
import re
import unittest
import render
from footer_policy import CREDIT, MISSION_PARAGRAPHS, apply_footer_policy


class FooterPolicyTests(unittest.TestCase):
    def test_all_footers_preserve_firm_copyright_and_destinations(self):
        design = render.contract()
        count = 0
        values, paragraphs = render.prepare({'values':{'advisor_name':'Test Advisor','firm_name':'Test Firm',
            'advisor_credentials':'CLU','license_number':'12345','copyright_year':'2026',
            'mission_text':'Old advisor-specific mission'}}, design)
        for relative in design['sha256']:
            source = (render.TEMPLATES/relative).read_text(encoding='utf-8')
            if 'class="pfg-footer-mission"' not in source:
                self.assertEqual(source,apply_footer_policy(source))
                continue
            count += 1
            changed = apply_footer_policy(source)
            self.assertEqual(changed,apply_footer_policy(changed))
            self.assertEqual(re.findall(r'(?:href|src|id)="[^"]*"',source),
                             re.findall(r'(?:href|src|id)="[^"]*"',changed))
            self.assertEqual(re.findall(r'<style>.*?</style>',source,re.S),re.findall(r'<style>.*?</style>',changed,re.S))
            output,missing = render.substitute(source,values,paragraphs)
            self.assertIn('© 2026 Test Firm. All rights reserved.',output)
            self.assertIn('Built, powered &amp; developed by ePIC Services Company.',output)
            for p in MISSION_PARAGRAPHS:self.assertIn('<p>'+p+'</p>',output)
            self.assertNotIn('Old advisor-specific mission',output)
            self.assertNotIn('mission_text',missing)
            self.assertNotIn('license_number',missing)
            self.assertIn('Test Advisor',render.substitute('<p>{{advisor_name}}</p>',values,paragraphs)[0])
        self.assertEqual(count,8)
        render.contract()


if __name__=='__main__':unittest.main()
