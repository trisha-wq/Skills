"""Check complete Risk/Tax coverage, provider separation and theme fidelity."""
import json
import re
import tempfile
import unittest
from pathlib import Path
import render
from video_popups import popup_palette
from webprez_popups import with_webprez_popups
from readability import with_readable_type


class WebPrezPopupTests(unittest.TestCase):
    def test_mixed_provider_library_and_theme(self):
        design=render.contract()
        values={'advisor_name':'Independent Advisor','theme_deep':'#202727','theme_primary':'#8e9897'}
        destinations=[]
        for key in design['tokens']:
            if key.endswith('_url') and key.startswith(('library_risk_','library_tax_')):
                token='2vw3dv' if key=='library_risk_02_url' else 'OwnVideo'
                values[key]='https://smartmoney.talk/n-n-'+token+'-OwnAdvisor-n.'+key
                destinations.append(values[key])
            elif key.endswith('_url') and key.startswith(('video_','home_video_','library_kai_zen_')):
                values[key]='https://player.vimeo.com/progressive_redirect/playback/123456789/rendition/720p/file.mp4?loc=external&signature=ExactSignature'
        theme={'background':'#202727','accent':'#8e9897','link':'#d4dcdb','hover':'#3a4443'}
        data={'values':values,'popup_theme':theme}
        with tempfile.TemporaryDirectory() as temp:
            path=Path(temp)/'values.json'
            path.write_text(json.dumps(data),encoding='utf-8')
            output=Path(temp)/'site'
            render.render(path,output)
            data=json.loads(path.read_text(encoding='utf-8'))
            library=(output/'ghl-videos-sections-inline/03-video-library.html').read_text(encoding='utf-8')
            self.assertEqual(library.count('<dialog '),2)
            for url in destinations:self.assertIn('href="'+url+'"',library)
            self.assertEqual(len(re.findall(r'href="https://smartmoney.talk/',library)),28)
            self.assertEqual(library.count('data-ct-play-icon="true"'),14)
            self.assertEqual(library,with_readable_type(with_webprez_popups(library,popup_palette(values,theme))))
            self.assertIn('background:#202727',library.split('<!-- Premium WebPrez popup start -->')[1])
            self.assertIn('border:1px solid #8e9897',library.split('<!-- Premium WebPrez popup start -->')[1])
            self.assertIn("frame.src = 'about:blank'",library)
            self.assertIn('Close video',library)
            self.assertTrue(render.verify(data,output)['uniqueIdsVerified'])
            self.assertIn('webprez-popup-v1',render.verify(data,output)['approvedOutputPolicies'])

    def test_bridge_and_unavailable_cards_stay_unchanged(self):
        bridge='<div class="premium-template premium-services-05"><a href="https://smartmoney.talk/n-n-2vw3dv-own-n.URL">Bridge</a></div>'
        missing='<div class="premium-template premium-videos-03"><a data-category="risk" data-unresolved="library_risk_01_url"></a></div>'
        self.assertEqual(bridge,with_webprez_popups(bridge))
        self.assertEqual(missing,with_webprez_popups(missing))
        with self.assertRaises(ValueError):popup_palette(overrides={'accent':'red;display:none'})


if __name__=='__main__':unittest.main()
