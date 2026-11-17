"""Regression coverage for portable Vimeo popup generation."""
import json
import re
import tempfile
import unittest
from pathlib import Path
import render
from video_popups import with_video_popups, popup_palette
from readability import with_readable_type


class VideoPopupTests(unittest.TestCase):
    def test_complete_render_preserves_urls_and_uses_distinct_dialog_ids(self):
        design=render.contract()
        values={'advisor_name':'Popup Test Advisor'}
        url='https://player.vimeo.com/progressive_redirect/playback/123456789/rendition/720p/file.mp4?loc=external&signature=test-value'
        for key in design['tokens']:
            if key.endswith('_url') and key.startswith(('video_','home_video_','library_kai_zen_')):
                values[key]=url
        with tempfile.TemporaryDirectory() as temporary:
            data={'values':values}
            path=Path(temporary)/'values.json'
            path.write_text(json.dumps(data),encoding='utf-8')
            output=Path(temporary)/'site'
            render.render(path,output)
            # Rendering persists the selected rotation clip in the input file.
            data=json.loads(path.read_text(encoding='utf-8'))
            ids=[]
            icons=0
            for file in output.glob('ghl-*/*.html'):
                text=file.read_text(encoding='utf-8')
                self.assertEqual(text,with_readable_type(with_video_popups(text,popup_palette(render.prepare(data,design)[0]))))
                ids+=re.findall(r'<dialog id="([^"]+)"',text)
                icons+=text.count('data-ct-play-icon="true"')
                for link in re.findall(r'href="([^"]*progressive_redirect[^"]*)"',text):
                    self.assertEqual(link,url.replace('&','&amp;'))
            self.assertEqual(len(ids),4)
            self.assertEqual(len(ids),len(set(ids)))
            self.assertEqual(icons,20)
            self.assertTrue(render.verify(data,output)['outputPolicyVerified'])
            # Deleting an overlay must invalidate the complete rendered output.
            file=output/'ghl-home-sections-inline/07-legacy-collection.html'
            file.write_text(file.read_text(encoding='utf-8').replace('data-ct-play-icon','removed-play-icon',1),encoding='utf-8')
            with self.assertRaises(ValueError):render.verify(data,output)

    def test_external_and_unavailable_actions_do_not_get_popups(self):
        external='<div class="premium-template premium-home-07"><a href="https://smartmoney.talk/n-n-own-video"><img src="art.jpg"></a></div>'
        unavailable='<div class="premium-template premium-home-07"><a aria-disabled="true" data-unresolved="home_video_01_url"><span class="ab-play"></span></a></div>'
        self.assertEqual(with_video_popups(external),external)
        self.assertEqual(with_video_popups(unavailable),unavailable)


if __name__=='__main__':unittest.main()
