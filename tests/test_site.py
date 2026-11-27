"""Offline regression tests, not external fact verification."""
import importlib.util
import json
import sys
import unittest
from datetime import date, timedelta
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
import strict_site as site
import build


class Document(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ids=[];self.links=[];self.rows=[];self.row=None;self.in_body=False;self.cell=None
        self.tables=[];self.table_depth=0;self.labels=[]
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if 'id' in a:self.ids.append(a['id'])
        if tag=='a':
            self.links.append(a.get('href',''))
            if self.row is not None:self.row['links'].append(a.get('href',''))
        if tag=='table':self.tables.append(a);self.table_depth+=1
        if tag=='tbody':self.in_body=True
        if tag=='tr' and self.in_body:self.row={'cells':[],'links':[],'id':a.get('id')}
        if tag=='td':
            self.cell='';self.labels.append(a.get('data-label'))
    def handle_data(self,value):
        if self.cell is not None:self.cell+=value
    def handle_endtag(self,tag):
        if tag=='td' and self.cell is not None:
            self.row['cells'].append(self.cell.strip());self.cell=None
        if tag=='tr' and self.row is not None:self.rows.append(self.row);self.row=None
        if tag=='tbody':self.in_body=False
        if tag=='table':self.table_depth-=1


class SiteTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pages=site.render()
        cls.docs={n:Document() for n in cls.pages}
        for n,d in cls.docs.items():d.feed(cls.pages[n])

    def test_evidence_schema(self):
        build.validate()

    def test_all_source_rows_present(self):
        self.assertEqual(set(site.E['restaurants']),{r['id'] for r in site.RES})
        self.assertEqual(len(site.E['hotels']),33)
        self.assertEqual(len(site.E['activities']),6)
        for key in ['restaurants','activities','hotels']:
            name={'restaurants':'restaurants.html','activities':'activities.html','hotels':'hotels.html'}[key]
            self.assertTrue(set(site.E[key]).issubset(set(self.docs[name].ids)))

    def test_every_row_has_source(self):
        # Each generated table body row must contain an external reference,
        # regardless of whether its decision fields are blank.
        for name,doc in self.docs.items():
            for row in doc.rows:
                with self.subTest(page=name,id=row['id']):
                    self.assertTrue(any(u.startswith('https://') for u in row['links']))

    def test_local_links_and_anchors(self):
        for name,doc in self.docs.items():
            self.assertEqual(len(doc.ids),len(set(doc.ids)),name+' duplicate IDs')
            for url in doc.links:
                p=urlsplit(url)
                if p.scheme or p.netloc:continue
                target=unquote(p.path) or name
                if target in self.pages:
                    if p.fragment:self.assertIn(unquote(p.fragment),self.docs[target].ids,(name,url))
                else:self.assertTrue((ROOT/target).is_file(),(name,url))

    def test_hotel_decision_values_stay_blank(self):
        doc=self.docs['hotels.html'];rows=[r for r in doc.rows if r['id'] in site.E['hotels']]
        self.assertEqual(len(rows),33)
        self.assertEqual([r['cells'][0] for r in rows],sorted(h['name'] for h in site.E['hotels'].values()))
        for row in rows:self.assertEqual(row['cells'][4:6],['—','—'])
        self.assertTrue(any(t.get('id')=='official-hotel-decisions' for t in doc.tables))
        for h in site.E['hotels'].values():
            self.assertIsNone(h['total_7n']);self.assertIsNone(h['within_60'])

    def test_no_assumed_meal_total(self):
        self.assertEqual(site.E['restaurants']['guy-savoy']['price_options'],[])
        self.assertNotIn('$3,000',self.pages['restaurants.html'])
        self.assertNotIn('$520',self.pages['restaurants.html'])
        self.assertNotIn('$1,855.06',self.pages['dining.html'])
        self.assertIn('$120.00',self.pages['dining.html'])
        self.assertIn('$80.00',self.pages['dining.html'])
        self.assertIn('$370.00',self.pages['dining.html'])
        self.assertIn('Sunday disputed',self.pages['restaurants.html'])
        self.assertIn('$397.76',self.pages['restaurants.html'])
        self.assertIn('$320.00',self.pages['restaurants.html'])
        self.assertIn('$42.00',self.pages['activities.html'])
        self.assertIn('$75.90',self.pages['activities.html'])

    def test_itemised_observation_and_retained_upstream_work(self):
        from decimal import Decimal
        o=site.E['hotel_engine_observations'][0]
        amount=sum(Decimal(str(x)) for x in o['room_nights'])
        amount+=sum(Decimal(str(o[k])) for k in ['room_tax','resort_fees','resort_fee_tax'])
        self.assertEqual(amount,Decimal(str(o['displayed_total'])))
        self.assertIn('$2,200.15',self.pages['pricing.html'])
        self.assertIn('bellagio-fountains',self.docs['activities.html'].ids)
        for a in site.load('activities.json')['activities']:
            for u in a.get('youtube',[]):self.assertIn(u,self.docs['activities.html'].links)
        for x in site.load('site-suggestions.json')['suggestions']:
            self.assertIn(x['id'],self.docs['suggestions.html'].ids)

    def test_schedule_corrections_and_flags(self):
        self.assertIn('9 AM–9 PM',site.E['activities']['mob-museum']['hours'])
        self.assertIsNone(site.E['activities']['high-roller']['hours'])
        self.assertIsNone(site.E['restaurants']['michael-mina']['hours'])
        self.assertIsNone(site.E['restaurants']['esthers-kitchen']['hours'])
        for f in site.E['checks']:self.assertIn(f['id'],self.docs['flagged.html'].ids)
        for n in range(52,70):self.assertIn(f'F-{n}',self.docs['flagged.html'].ids)

    def test_date_arithmetic(self):
        starts=[];d=date(2027,2,15)
        while d+timedelta(days=7)<=date(2027,3,23):starts.append(d);d+=timedelta(days=1)
        self.assertEqual(len(starts),30)
        self.assertEqual(starts[-1],date(2027,3,16))
        self.assertEqual(date(2027,2,15)+timedelta(days=14),date(2027,3,1))

    def test_mobile_accessibility_and_escaping(self):
        for name,content in self.pages.items():
            self.assertIn('name="viewport"',content)
            self.assertIn('Skip to content',content)
            self.assertEqual(content.count('<nav>'),1)
            self.assertTrue(all(self.docs[name].labels))
            for t in self.docs[name].tables:self.assertIn('responsive',t.get('class',''))
        self.assertEqual(site.text('<script>"&'), '&lt;script&gt;&quot;&amp;')
        self.assertIn('&amp;b=2',site.link('https://example.com/?a=1&b=2','test'))
        with self.assertRaises(ValueError):site.link('javascript:alert(1)')
        with self.assertRaises(ValueError):site.table(['a'],[['x','y']],'bad')

    def test_generated_root_docs_parity(self):
        self.assertEqual(len(self.pages),16)
        for name,content in self.pages.items():
            self.assertEqual((ROOT/name).read_text(),content)
            self.assertEqual((ROOT/'docs'/name).read_text(),content)
        self.assertEqual((ROOT/'style.css').read_bytes(),(ROOT/'docs/style.css').read_bytes())

    def test_prior_session_accounts_preserved_with_provenance(self):
        prior=site.load('socials.json')
        for category,name in [('restaurants','restaurants.html'),('activities','activities.html')]:
            for r in prior[category]:
                if r.get('instagram'):self.assertIn(r['instagram'],self.docs[name].links,r['id'])
        for r in prior['activities']:
            if r.get('also_recorded'):
                self.assertIn(site.text(r['also_recorded']),self.pages['activities.html'])
        self.assertIn('Earlier session evidence',self.pages['restaurants.html'])


if __name__=='__main__':unittest.main()
