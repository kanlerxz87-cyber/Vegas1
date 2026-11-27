#!/usr/bin/env python3
"""
build.py — checks research datasets and computes the legacy zone-model scores.

These model scores are unvalidated assumptions, NOT official bus journeys and
NOT a public hotel ranking. The public views use field-level evidence instead.
Missing research values are allowed when explicitly unverified; contradictions
and invalid evidence records fail. Run: python3 scripts/build.py
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"

THRESHOLD_LONG = 60
THRESHOLD_SHORT = 20


def load(name):
    with open(DATA / name, encoding="utf-8") as fh:
        return json.load(fh)


def score(hotel_zone, restaurant_zones, matrix, limit):
    """Count restaurants whose one-way estimate from hotel_zone is <= limit."""
    row = matrix.get(hotel_zone)
    if row is None:
        raise KeyError(f"unknown zone: {hotel_zone}")
    total = 0
    for rz in restaurant_zones:
        if rz not in row:
            raise KeyError(f"zone {rz} missing from matrix row {hotel_zone}")
        if row[rz] <= limit:
            total += 1
    return total


def main():
    hotels = load("hotels.json")
    restaurants = load("restaurants.json")
    transit = load("transit.json")

    matrix = transit["minutes"]
    rzones = [r["zone"] for r in restaurants["restaurants"]]
    missing = [z for z in set(rzones) if z not in matrix]
    if missing:
        sys.exit(f"transit.json is missing zone rows for: {sorted(missing)}")

    changed = 0
    for h in hotels["hotels"]:
        z = h.get("zone")
        if z is None:
            # No model input for a new official-only candidate. Never invent it.
            continue
        long_count = score(z, rzones, matrix, THRESHOLD_LONG)
        short_count = score(z, rzones, matrix, THRESHOLD_SHORT)
        if h.get("michelin_within_60") != long_count or h.get("michelin_within_20") != short_count:
            h["michelin_within_60"] = long_count
            h["michelin_within_20"] = short_count
            changed += 1

    with open(DATA / "hotels.json", "w", encoding="utf-8") as fh:
        json.dump(hotels, fh, indent=2, ensure_ascii=False)
        fh.write("\n")

    # ---- integrity checks -------------------------------------------------
    problems = []
    n_res = len(restaurants["restaurants"])
    if n_res != 24:
        problems.append(f"expected 24 restaurants, found {n_res}")

    award_counts = {}
    for r in restaurants["restaurants"]:
        award_counts[r["award_class"]] = award_counts.get(r["award_class"], 0) + 1
    expected_awards = {"starred": 4, "bib": 3, "recommended": 17}
    if award_counts != expected_awards:
        problems.append(f"award split {award_counts} != {expected_awards}")

    for r in restaurants["restaurants"]:
        if not r["official_url"]:
            problems.append(f"{r['id']}: no official_url")


    print(f"restaurants: {n_res}  award split: {award_counts}")
    print(f"hotels: {len(hotels['hotels'])}, rescored: {changed}")
    flat = {h['michelin_within_60'] for h in hotels['hotels'] if h.get('michelin_within_60') is not None}
    print(f"legacy MODEL ONLY '<=60 min' counts: {sorted(flat)} (not public journey evidence)")
    spread = sorted({h['michelin_within_20'] for h in hotels['hotels'] if h.get('michelin_within_20') is not None}, reverse=True)
    print(f"distinct '<=20 min' counts: {spread}")

    from verified_views import load_manifest, validate_manifest
    problems.extend(validate_manifest(load_manifest()))

    if problems:
        print("\nPROBLEMS:")
        for p in problems:
            print(" -", p)
        return 1
    print("\nall integrity checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
