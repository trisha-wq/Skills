import copy
import json
import tempfile
import unittest
from pathlib import Path
from background_videos import CATALOG, apply_background_video, assign_background


class BackgroundRotationTests(unittest.TestCase):
    def test_rotation_wraps_and_rebuild_retains_assignment(self):
        pool = json.loads(CATALOG.read_text(encoding='utf-8'))['videos']
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            state = root / 'rotation.json'
            assigned = []
            for index in range(5):
                data = {'values': {'advisor_name': 'Advisor ' + str(index)}}
                path = root / ('site-' + str(index) + '.json')
                assigned.append(assign_background(data, path, state))
                before = state.read_bytes()
                self.assertEqual(assign_background(data, path, state), assigned[-1])
                self.assertEqual(state.read_bytes(), before)
                # Recreating inputs also recovers the recorded project assignment.
                self.assertEqual(assign_background({'values': {}}, path, state), assigned[-1])
            self.assertEqual(assigned, [pool[1], pool[2], pool[3], pool[0], pool[1]])

    def test_explicit_existing_site_video_does_not_consume_rotation(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            url = 'https://example.com/chosen.mp4'
            data = {'background_video_url': url}
            self.assertEqual(assign_background(data, root/'values.json', root/'rotation.json'), url)
            self.assertFalse((root/'rotation.json').exists())

    def test_only_background_source_changes(self):
        old = '<video class="pfg-background-video" autoplay muted loop playsinline poster="old.jpg"><source src="https://example.com/old.mp4" type="video/mp4"></video>'
        unrelated = '<a href="https://example.com/advisor.mp4">Advisor</a><video controls src="lesson.mp4"></video>'
        new = apply_background_video(old + unrelated, 'https://example.com/new.mp4')
        self.assertIn('src="https://example.com/new.mp4"', new)
        self.assertNotIn('poster="old.jpg"', new)
        self.assertTrue(new.endswith(unrelated))
        self.assertIn('autoplay muted loop playsinline', new)
        self.assertEqual(apply_background_video(new, 'https://example.com/new.mp4'), new)
        self.assertEqual(apply_background_video(old, 'https://example.com/old.mp4'), old)

    def test_renderer_keeps_selection_and_baseline_hashes(self):
        import render
        original = (render.TEMPLATES/'ghl-home-sections-inline/02-hero.html').read_text(encoding='utf-8')
        selected = json.loads(CATALOG.read_text(encoding='utf-8'))['videos'][2]
        code, _ = render.substitute(original, {'advisor_name': 'Test'}, [], background_video_url=selected)
        self.assertIn('<source src="'+selected+'"', code)
        render.contract()


if __name__ == '__main__':
    unittest.main()
