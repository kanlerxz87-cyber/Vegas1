#!/usr/bin/env python3
"""Validate primary evidence, without rewriting historical model outputs.

T-ec1d72e2 withdraws the unsupported 20/60-minute hotel scoring from decision views.
The old source matrix/counts remain in Git as explicitly historical research.
"""
import json
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parent.parent


def validate():
    def load(name):
        return json.loads((ROOT/'data'/name).read_text())
    d=load('verification-2026-11-27.json')
    raw=load('restaurants.json')['restaurants']
    assert set(d['restaurants'])=={r['id'] for r in raw}, 'Missing restaurant evidence row'
    assert set(d['activities'])=={r['id'] for r in load('activities.json')['activities']}, 'Missing activity row'
    assert set(d['hotels'])=={r['id'] for r in load('hotels.json')['hotels']}|{'mgm-grand'}, 'Missing hotel candidate'
    counts={}
    for id,r in d['restaurants'].items():
        counts[r['award_class']]=counts.get(r['award_class'],0)+1
        assert r['award'] and r['address'], f'{id}: no official award/location evidence'
    assert counts=={'starred':4,'bib':3,'recommended':17}, counts
    assert d['michelin_source'].startswith('https://www.michelin.com/'), 'Non-official award source'
    for category in ['restaurants','activities','hotels']:
        for id,r in d[category].items():
            assert r['source'] and urlsplit(r['source']).scheme=='https', f'{id}: missing official source'
            assert r['check'], f'{id}: missing verification scope'
            for opt in r.get('price_options',[]):
                price=opt.get('for_two',opt.get('per_person'))
                assert isinstance(price,(int,float)) and price>=0, id
                assert opt['label'], id
            for s in r.get('social',[]):
                assert urlsplit(s['url']).hostname in {'www.instagram.com','www.youtube.com','www.tiktok.com'}, id
                assert s['label'], id
    for id,h in d['hotels'].items():
        assert h['total_7n'] is None and h['within_60'] is None, f'{id}: unsupported decision field'
    flags=[f['id'] for f in d['checks']]
    assert len(flags)==len(set(flags)), 'Duplicate flag IDs'
    print(f"Evidence schema valid: {len(d['hotels'])} hotel candidates, {len(raw)} restaurants, {len(d['activities'])} activities.")
    print('Historical source files left unchanged. No unverified transit scores recomputed.')


if __name__=='__main__':
    validate()
