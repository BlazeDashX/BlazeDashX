import json
import sys
import tempfile
import unittest
from datetime import datetime,timezone
from pathlib import Path
import xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
import build_live

FIXTURE=json.loads((ROOT/'tests/data/sample_api.json').read_text())
NOW=datetime(2026,11,5,tzinfo=timezone.utc)

class ProfileBuildTests(unittest.TestCase):
    def test_public_repo_filter_and_stats(self):
        user,repos,events=build_live.fetch_data(build_live.Client(fixture=FIXTURE))
        self.assertEqual(len(repos),4)
        self.assertEqual(sum(r['stargazers_count'] for r in repos),8)
        self.assertNotIn('BlazeDashX',[r['name'] for r in repos])
        self.assertNotIn('test-fork',[r['name'] for r in repos])

    def test_filter_events_and_do_not_invent_commit_counts(self):
        rows=build_live.get_event_rows(FIXTURE['/users/BlazeDashX/events/public?per_page=100&page=1'],NOW)
        self.assertEqual(len(rows),5) # one profile-repo event and one old event are excluded
        self.assertEqual(rows[0]['verb'],'Pushed code')
        self.assertNotIn('3 commits',repr(rows))

    def test_generate_all_six_live_panels(self):
        with tempfile.TemporaryDirectory() as td:
            build_live.build(build_live.Client(fixture=FIXTURE),td,NOW)
            expected=['dashboard.svg','activity.svg','pulse.svg','languages.svg','radar.svg','constellation.svg','updated.json']
            for filename in expected:
                self.assertTrue((Path(td)/filename).is_file(),filename)
            for filename in expected[:-1]:
                ET.parse(Path(td)/filename)
            activity=(Path(td)/'activity.svg').read_text()
            self.assertIn('Personal-Expense-Tracker',activity)
            self.assertNotIn('3 commits',activity)
            self.assertNotIn('BlazeDashX/BlazeDashX',activity)
            board=(Path(td)/'dashboard.svg').read_text()
            self.assertIn('123',board)
            self.assertIn('PUBLIC REPOS',board)
            langs=(Path(td)/'languages.svg').read_text()
            self.assertIn('TypeScript',langs)
            self.assertNotIn('Python',langs) # fork/archive excluded

    def test_xml_escape_repo_names(self):
        poisoned=json.loads(json.dumps(FIXTURE))
        poisoned['/users/BlazeDashX/repos?type=owner&per_page=100&page=1'][1]['name']='a&b<demo>'
        with tempfile.TemporaryDirectory() as td:
            build_live.build(build_live.Client(fixture=poisoned),td,NOW)
            for file in Path(td).glob('*.svg'):
                ET.parse(file)
            self.assertIn('a&amp;b&lt;demo&gt;', (Path(td)/'radar.svg').read_text())

if __name__=='__main__':
    unittest.main()
