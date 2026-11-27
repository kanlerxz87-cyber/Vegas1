#!/usr/bin/env python3
"""Validate the official field-evidence manifest, without rewriting research.

Historical zone matrices, OTA captures and peer audit overlays remain available,
but are never recomputed into a verified hotel ranking. Missing evidence is an
explicit null, not a build failure; contradictory evidence states do fail.
"""
import json
from pathlib import Path
from verified_views import load_manifest, validate_manifest, value

ROOT = Path(__file__).resolve().parent.parent


def validate():
    data = load_manifest()
    errors = validate_manifest(data)
    assert not errors, '\n'.join(errors)
    awards = {}
    for r in data['restaurants'].values():
        a = value(r, 'award')
        awards[a] = awards.get(a, 0) + 1
    assert awards == {'2 stars': 1, '1 star': 3, 'Bib Gourmand': 3, 'Recommended': 17}, awards
    for group in ('hotels', 'restaurants', 'activities'):
        raw = json.loads((ROOT / 'data' / (group + '.json')).read_text())[group]
        ids = [r['id'] for r in raw]
        assert len(ids) == len(set(ids)), f'{group}: duplicate canonical IDs'
    print('Evidence schema valid: ' + ', '.join(f'{len(data[k])} {k}' for k in ('hotels', 'restaurants', 'activities')))
    print('Historical source files left unchanged. No assumed transit scores recomputed.')


if __name__ == '__main__':
    validate()
