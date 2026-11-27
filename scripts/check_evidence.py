#!/usr/bin/env python3
"""Offline evidence-display regression checks; NOT an external-source verification tool."""
import json
from datetime import date, timedelta
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent.parent

class Table(HTMLParser):
    def __init__(self):
        super().__init__()
        self.active = False
        self.row = None
        self.cell = None
        self.rows = []
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == 'table' and a.get('id') == 'official-hotel-decisions':
            self.active = True
        if self.active:
            if tag == 'tr': self.row = {'cells': [], 'links': []}
            if tag == 'td': self.cell = ''
            if tag == 'a' and self.row is not None: self.row['links'].append(a.get('href', ''))
    def handle_data(self, text):
        if self.cell is not None: self.cell += text
    def handle_endtag(self, tag):
        if self.active:
            if tag == 'td' and self.cell is not None:
                self.row['cells'].append(self.cell.strip())
                self.cell = None
            if tag == 'tr' and self.row is not None:
                if self.row['cells']: self.rows.append(self.row)
                self.row = None
            if tag == 'table': self.active = False

def main():
    hotels = json.loads((ROOT / 'data/hotels.json').read_text())['hotels']
    restaurants = json.loads((ROOT / 'data/restaurants.json').read_text())['restaurants']
    activities = json.loads((ROOT / 'data/activities.json').read_text())['activities']
    for label, entries in [('hotels', hotels), ('restaurants', restaurants), ('activities', activities)]:
        ids = [x['id'] for x in entries]
        assert len(ids) == len(set(ids)), f'{label}: duplicate IDs'
        for x in entries:
            u = urlparse(x['official_url'])
            assert u.scheme == 'https' and u.hostname, (label, x['id'], 'missing official URL')
            assert u.hostname not in {'www.booking.com', 'booking.com'}, (label, x['id'], 'OTA passed as official')
    parser = Table()
    parser.feed((ROOT / 'hotels.html').read_text())
    assert len(parser.rows) == len(hotels) == 32
    names = [h['name'] for h in sorted(hotels, key=lambda h: h['name'].casefold())]
    for row, name in zip(parser.rows, names):
        assert row['cells'][0] == name
        assert row['cells'][1:4] == ['—'] * 3, f'{name}: unsupported decision number/specification'
        assert 'Unverified' in row['cells'][4]
        assert any(u.startswith('https://') for u in row['links']), name
    # Restaurant prices: every non-blank cell must name its basis and its own menu source,
    # and the withdrawn $3,000 Guy Savoy figure must not reappear anywhere in the data.
    for r in restaurants:
        if r.get('price_2adults'):
            assert r.get('price_basis'), f"{r['id']}: priced without a basis"
            src = r.get('price_source', '')
            assert src.startswith('https://') and 'booking.com' not in src, (r['id'], 'no menu source')
    assert all('3,000' not in (r.get('price_2adults') or '') for r in restaurants), 'withdrawn Krug figure used as a price'
    guy = next(r for r in restaurants if r['id'] == 'guy-savoy')
    assert guy['price_2adults'].endswith('(est.)') and 'menus' not in guy['price_source']
    assert 'restaurant-guy-savoy/main-menu' in guy['price_source']
    partage = next(r for r in restaurants if r['id'] == 'partage')
    wing = next(r for r in restaurants if r['id'] == 'wing-lei')
    assert partage['price_2adults'].startswith('$260') and 'partage.vegas/menu' in partage['price_source']
    assert wing['price_2adults'].startswith('$397.76') and 'wynnresorts.com' in wing['price_source']
    # The budget page must not smuggle a hotel total back in.
    dining = (ROOT / 'dining.html').read_text()
    assert '$712.30' in dining and '$1,025.06' in dining and '$1,855.06' in dining
    assert 'No hotel figure is used' in dining
    mob = next(a for a in activities if a['id'] == 'mob-museum')
    assert 'daily 9:00 AM–9:00 PM' in mob['hours']
    assert next(a for a in activities if a['id'] == 'high-roller')['hours'] == ''
    starts = []
    d = date(2027, 2, 15)
    while d + timedelta(days=7) <= date(2027, 3, 23):
        starts.append(d)
        d += timedelta(days=1)
    assert len(starts) == 30 and starts[-1] == date(2027, 3, 16)
    assert date(2027, 2, 15) + timedelta(days=14) == date(2027, 3, 1)
    for p in (ROOT / 'docs').glob('*.html'):
        assert p.read_bytes() == (ROOT / p.name).read_bytes(), f'root/docs drift: {p.name}'
    flags = (ROOT / 'flagged.html').read_text()
    for n in range(58, 64): assert f'id="F-{n}"' in flags
    print('PASS: 32 hotel rows, official discovery URLs, blank evidence cells, date arithmetic, corrections, flags and root/docs parity.')
    print('LIMIT: these are offline regression checks, not proof that external URLs work or facts remain current.')

if __name__ == '__main__':
    main()
