"""Protect the final template defaults and earlier output-policy behavior."""
import re
import unittest
import render
from approved_template import apply_approved_template
from video_popups import popup_palette


class ApprovedTemplateTests(unittest.TestCase):
    def test_all_sections_keep_destinations_inventory_and_scripts(self):
        design = render.contract()
        values, paragraphs = render.prepare({'values': {'advisor_name':'Sample Advisor'}}, design)
        for relative in design['sha256']:
            original=(render.TEMPLATES/relative).read_text(encoding='utf8')
            result,_=render.substitute(original,values,paragraphs)
            self.assertEqual(apply_approved_template(result,popup_palette(values)),result)
            for attr in ['src','poster','id','aria-controls','data-index','data-category']:
                pattern=rf'\b{attr}="[^"]*"'
                self.assertEqual(re.findall(pattern,original),re.findall(pattern,result)[:len(re.findall(pattern,original))],(relative,attr))
            self.assertNotIn('content:attr(data-index)',result)
        render.contract()

    def test_scoped_layout_and_legibility(self):
        values,paras=render.prepare({'values':{'advisor_name':'Sample Advisor','theme_deep':'#283828'}},render.contract())
        def section(path, **kwargs):
            return render.substitute((render.TEMPLATES/path).read_text(encoding='utf8'),values,paras,**kwargs)[0]
        header=section('ghl-home-sections-inline/01-header.html')
        self.assertIn('.pfg-nav>a{font-size:17px;font-weight:600}',header)
        self.assertIn('@media(max-width:1190px)',header)
        compact=section('ghl-home-sections-inline/02-hero.html')
        self.assertIn('padding-block:48px 104px!important',compact)
        self.assertNotIn('padding-block:48px 104px!important',section('ghl-home-sections-inline/02-hero.html',hero_layout='preserve'))
        caption=section('ghl-home-sections-inline/03-advisor-introduction.html')
        self.assertIn('.pfg-media-caption{background:#283828;color:#fff',caption)
        self.assertIn('flex-wrap:wrap;gap:8px 24px',caption)
        banner=section('ghl-home-sections-inline/10-legacy-banner.html')
        self.assertIn('.pfg-legacy-banner .pfg-eyebrow{color:#fff;background:#283828',banner)
        light=apply_approved_template('<style></style><div class="premium-template premium-home-03"></div>',{'background':'#eeeeee'})
        self.assertIn('color:#111',light)

    def test_substantive_numbers_and_image_host_validation(self):
        source='<style></style><div class="premium-template premium-videos-03"><p>14 videos; 21st Century; $59; 2026</p></div>'
        self.assertIn('<p>14 videos; 21st Century; $59; 2026</p>',apply_approved_template(source,popup_palette()))
        render.prepare({'values':{'advisor_name':'Sample Advisor','logo_url':'https://files.leadconnectorhq.com/file/verified/image.png'}},render.contract())
        for url in ['https://files.leadconnectorhq.com.evil.example/file/a','https://files.leadconnectorhq.com/not-original/a']:
            with self.assertRaises(ValueError):
                render.prepare({'values':{'advisor_name':'Sample Advisor','logo_url':url}},render.contract())

    def test_branding_changes_css_only_and_keeps_exact_palette(self):
        source='<style>.accent{color:#153a63;background:#e8edf4}.exact{color:#304030}</style><div class="premium-template premium-home-03"><img src="https://example.com/153a63.png"></div><script>const brand="#153a63";</script>'
        result=apply_approved_template(source,popup_palette({'theme_deep':'#283828'}),primary='#304030')
        self.assertNotIn('color:#153a63;',result)
        self.assertIn('.exact{color:#304030}',result)
        self.assertIn('src="https://example.com/153a63.png"',result)
        self.assertIn('const brand="#153a63"',result)


if __name__=='__main__': unittest.main()
