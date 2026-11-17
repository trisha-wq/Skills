"""Check readability changes only typography and remains safe to repeat."""
import re
import unittest
import render
from readability import with_readable_type


class ReadabilityTests(unittest.TestCase):
    def test_full_template_keeps_content_scripts_links_and_large_headings(self):
        design=render.contract()
        for relative in design['sha256']:
            original=(render.TEMPLATES/relative).read_text(encoding='utf-8')
            changed=with_readable_type(original)
            self.assertEqual(with_readable_type(changed),changed)
            self.assertEqual(re.sub(r'<style>.*?</style>','',original,flags=re.S),re.sub(r'<style>.*?</style>','',changed,flags=re.S))
            self.assertEqual([n for n in re.findall(r'font-size:\s*(\d+)px',original) if int(n)>20],
                             [n for n in re.findall(r'font-size:\s*(\d+)px',changed) if int(n)>20])
        render.contract()

    def test_reading_sizes_and_layout_dimensions(self):
        source='<style>.copy{font-size:14px;line-height:1.7;padding:14px}.title{font-size:48px}.mobile{font-size:16px}.popup{font:600 18px/1.4 Manrope}.icon{width:18px;height:18px}</style><p>2026: 14 videos, $97, 847-604-5434</p>'
        result=with_readable_type(source)
        self.assertIn('font-size:16px;line-height:1.7;padding:14px',result)
        self.assertIn('.title{font-size:48px}',result)
        self.assertIn('.mobile{font-size:18px}',result)
        self.assertIn('font:600 20px/1.4 Manrope',result)
        self.assertIn('width:18px;height:18px',result)
        self.assertIn('<p>2026: 14 videos, $97, 847-604-5434</p>',result)
        self.assertIn('font:600 16px/18px Manrope',with_readable_type('<style>.copy{font:600 14px/18px Manrope}</style>'))


if __name__=='__main__':unittest.main()
