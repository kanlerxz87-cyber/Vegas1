#!/usr/bin/env python3
"""
build.py — computes the Michelin proximity scores and validates the dataset.

Run from the repo root:  python3 scripts/build.py

It rewrites exactly two fields in data/hotels.json:
  michelin_within_60  — count of Michelin restaurants reachable in <= 60 min one-way
  michelin_within_20  — count reachable in <= 20 min one-way (the ranking tiebreaker)

Everything else in the JSON is authored by hand and never touched.

Why this exists: the "within 1 hour" metric on its own returns 24/24 for every
hotel in Las Vegas, so it cannot rank anything. The 20-minute column is the one
that actually separates the field. Both are computed here from the single zone
matrix in data/transit.json so the site cannot drift from the source of truth.
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
        z = h["zone"]
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
        if not r["youtube"]:
            problems.append(f"{r['id']}: no YouTube link")

    for h in hotels["hotels"]:
        if not h["prices"]:
            problems.append(f"{h['id']}: no price rows")

    print(f"restaurants: {n_res}  award split: {award_counts}")
    print(f"hotels: {len(hotels['hotels'])}, rescored: {changed}")
    flat = {h['michelin_within_60'] for h in hotels['hotels']}
    print(f"distinct '<=60 min' counts: {sorted(flat)}")
    spread = sorted({h['michelin_within_20'] for h in hotels['hotels']}, reverse=True)
    print(f"distinct '<=20 min' counts: {spread}")

    if problems:
        print("\nPROBLEMS:")
        for p in problems:
            print(" -", p)
        return 1
    print("\nall integrity checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
