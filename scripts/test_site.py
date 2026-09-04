#!/usr/bin/env python3
"""Fast regression tests for content features; standard library only."""
from __future__ import annotations
import copy
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
import build_site as site

class ContentTests(unittest.TestCase):
    def setUp(self):
        self.data=list(copy.deepcopy(site.load_data()))
        # Rendering fixtures must not constrain the user's future real content.
        self.data[0].update(home_publication_limit=6, home_news_limit=4, home_project_limit=2)
        self.data[3]=[{
            "id":"example-project", "title":"Example research project",
            "summary":"A project used only by regression tests.", "featured":True,
        }]
        self.data[-1]=[{
            "id":f"test-paper-{i}", "title":f"Example paper {i}",
            "authors":["Amir Salarpour"], "year":2026, "venue_short":"TEST",
            "venue":"Example conference", "type":"Conference paper",
            "featured":True, "links":{"paper":f"https://example.org/paper/{i}"},
        } for i in range(8)]
        self.data[4]=[{
            "id":"test-news", "date":"2026-08-07", "label":"Aug 2026",
            "kind":"Publication", "publication":"test-paper-0",
            "text":"GATE was accepted.", "link_text":"GATE",
        }]
    def home(self, projects=None, profile=None):
        cfg,p,r,projects_original,n,t,s,pubs=self.data
        return site.home_page(cfg,profile or p,r,projects_original if projects is None else projects,n,pubs)
    def test_empty_projects(self):
        html=self.home(projects=[])
        self.assertNotIn('id="projects"',html)
    def test_featured_projects(self):
        p=copy.deepcopy(self.data[3][0]); p.update(id='second-project',title='Second featured project',featured=True)
        self.assertIn(p['title'],self.home(projects=[self.data[3][0],p]))
        p['featured']=False
        self.assertNotIn(p['title'],self.home(projects=[self.data[3][0],p]))
    def test_project_links(self):
        p=copy.deepcopy(self.data[3][0]); p['links']=[{'label':'Code','url':'https://github.com/example/project'}]
        self.assertIn('https://github.com/example/project',site.project_html(p))
    def test_six_selected_papers(self):
        self.assertEqual(self.home().count('class="publication publication-compact"'),6)
    def test_abbreviated_news_link(self):
        pubs={p['id']:p for p in self.data[-1]}
        news=self.data[4][0]
        self.assertIn('>GATE</a>',site.render_news_item(news,pubs))
    def test_changed_cv_affiliation(self):
        p=self.data[1];p['affiliation']='Future University'
        next(x for x in p['links'] if x['id']=='cv')['url']='/assets/files/new-cv.pdf'
        self.assertIn('/assets/files/new-cv.pdf',site.nav_html('home',p))
        self.assertIn('Future University',site.json_ld(self.data[0],p))
        self.assertNotIn('"name":"Clemson University"',site.json_ld(self.data[0],p))
    def test_preprint_type(self):
        self.assertEqual(site.type_key('Preprint'),'preprint')
        self.assertEqual(site.type_key('arXiv preprint'),'preprint')
    def test_optional_order(self):
        self.data[-1][0].pop('order',None)
        self.home()
    def test_refuse_unmarked_output_deletion(self):
        with tempfile.TemporaryDirectory() as td:
            out=Path(td)/'important';out.mkdir();keep=out/'keep.txt';keep.write_text('preserve')
            with self.assertRaises(SystemExit):
                site.build(out)
            self.assertEqual(keep.read_text(),'preserve')
    def test_repeat_build(self):
        with tempfile.TemporaryDirectory() as td:
            out=Path(td)/'dist'
            site.build(out);site.build(out)
            self.assertTrue((out/'index.html').exists())
            self.assertTrue((out/'.academic-site-build-output').exists())
if __name__=='__main__':
    unittest.main()
