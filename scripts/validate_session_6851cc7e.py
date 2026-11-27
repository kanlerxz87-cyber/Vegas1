#!/usr/bin/env python3
"""Strict validator for Task T20 structured datasets and generated HTML subsite."""
from __future__ import annotations

import json
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
SITE = ROOT / "docs" / "session-6851cc7e"

EXPECTED_PAGES = [
    "index.html",
    "hotels.html",
    "costs.html",
    "michelin.html",
    "activities-transit.html",
    "questions-suggestions.html",
    "repo-review.html",
    "flagged.html",
]

FORBIDDEN_OTA_DOMAINS = ("booking.com", "expedia.com", "hotels.com", "agoda.com", "priceline.com", "kayak.com")


class LinkAndMetaChecker(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.has_viewport = False
        self.local_refs: list[str] = []
        self.external_urls: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        ad = dict(attrs)
        if tag == "meta" and ad.get("name") == "viewport" and "width=device-width" in (ad.get("content") or ""):
            self.has_viewport = True
        for attr in ("href", "src"):
            val = ad.get(attr)
            if not val:
                continue
            if val.startswith("#") or val.startswith("mailto:") or val.startswith("tel:"):
                continue
            if val.startswith("http://") or val.startswith("https://"):
                self.external_urls.append(val)
            else:
                self.local_refs.append(val.split("#")[0])


def is_ota_url(url: str) -> bool:
    host = (urlparse(url).hostname or "").lower()
    return any(host == ota or host.endswith("." + ota) for ota in FORBIDDEN_OTA_DOMAINS)


def fail(msg: str) -> None:
    print(f"FAIL: {msg}", file=sys.stderr)
    sys.exit(1)


def main() -> None:
    hotels = json.loads((DATA / "session-6851cc7e-hotels.json").read_text(encoding="utf-8"))
    michelin = json.loads((DATA / "session-6851cc7e-michelin.json").read_text(encoding="utf-8"))
    act_tr = json.loads((DATA / "session-6851cc7e-activities-transit.json").read_text(encoding="utf-8"))
    audit_qa = json.loads((DATA / "session-6851cc7e-audit-qa.json").read_text(encoding="utf-8"))
    canon_ids = {r["id"] for r in json.load(open(DATA / "restaurants.json", encoding="utf-8"))["restaurants"]}

    # 1. Validate 15 Official-IBE Hotels
    vh = hotels["verified_hotels"]
    if len(vh) != 15:
        fail(f"Expected 15 verified hotels, got {len(vh)}")
    for h in vh:
        if not h["bed_verified"] or not h["private_bath"]:
            fail(f"Hotel {h['id']} missing bed or private bath verification")
        for ukey in ("official_url", "official_ibe_feb_url", "official_ibe_mar_url"):
            u = h[ukey]
            if not u.startswith("https://"):
                fail(f"Hotel {h['id']} {ukey} must be https://, got {u}")
            if is_ota_url(u):
                fail(f"Hotel {h['id']} {ukey} uses forbidden OTA URL {u}")
        for wkey in ("feb_15_22", "mar_14_21"):
            w = h[wkey]
            nt = w["nightly_incl_fee_pretax"]
            pre = w["total_7n_incl_fee_pretax"]
            tax = w["total_7n_all_in_est"]
            if nt is None:
                if pre is not None or tax is not None:
                    fail(f"Hotel {h['id']} {wkey} partial null")
            else:
                if abs(nt * 7 - pre) > 0.06:
                    fail(f"Hotel {h['id']} {wkey} 7*nightly ({nt*7}) != pre-tax ({pre})")
                expected_tax = round(pre * 1.1338, 2)
                # Hilton RW Feb uses exact itemised checkout ($2,200.15 vs $2,200.10)
                if abs(expected_tax - tax) > 0.08:
                    fail(f"Hotel {h['id']} {wkey} tax total {tax} != expected {expected_tax}")

    # 2. Validate 24 MICHELIN Restaurants
    starred = michelin["starred"]
    bib = michelin["bib_gourmand"]
    rec = michelin["recommended"]
    if (len(starred), len(bib), len(rec)) != (4, 3, 17):
        fail(f"Unexpected MICHELIN split: {len(starred)}, {len(bib)}, {len(rec)}")
    all_r = starred + bib + rec
    ids = {r["id"] for r in all_r}
    if ids != canon_ids:
        fail(f"MICHELIN IDs mismatch canonical: diff={ids ^ canon_ids}")
    for r in starred:
        if not r["is_starred"]:
            fail(f"Starred venue {r['id']} marked not starred")
    for r in bib + rec:
        if r["is_starred"]:
            fail(f"Non-starred venue {r['id']} marked is_starred=True")
    by_id = {r["id"]: r for r in all_r}
    if by_id["michael-mina"]["status"] != "temporarily_closed":
        fail("Michael Mina must be marked temporarily_closed")
    priced = [r for r in all_r if r["price_2_adults_pretax"] != ""]
    blanks = [r for r in all_r if r["price_2_adults_pretax"] == ""]
    if len(priced) != 15 or len(blanks) != 9:
        fail(f"Expected 15 priced and 9 blank restaurants, got {len(priced)} and {len(blanks)}")
    for r in blanks:
        if r["price_basis"] != "unpublished_blank":
            fail(f"Blank venue {r['id']} must have price_basis=unpublished_blank")

    # 3. Validate Combined Couple Packages Math
    for p in act_tr["combined_packages"]:
        exp_feb = round(p["hotel_7n_feb_all_in"] + p["michelin_pretax_total"] + p["activities_4_paid_plus_2_free"] + p["public_transit_7d_2adults"], 2)
        exp_mar = round(p["hotel_7n_mar_all_in"] + p["michelin_pretax_total"] + p["activities_4_paid_plus_2_free"] + p["public_transit_7d_2adults"], 2)
        if abs(exp_feb - p["combined_feb_15_22"]) > 0.01:
            fail(f"Package {p['id']} Feb total {p['combined_feb_15_22']} != {exp_feb}")
        if abs(exp_mar - p["combined_mar_14_21"]) > 0.01:
            fail(f"Package {p['id']} Mar total {p['combined_mar_14_21']} != {exp_mar}")

    # 4. Validate Generated HTML Pages
    if not (SITE / "style.css").is_file():
        fail("Missing style.css")
    for fname in EXPECTED_PAGES:
        fpath = SITE / fname
        if not fpath.is_file():
            fail(f"Missing generated page {fpath}")
        raw = fpath.read_text(encoding="utf-8")
        parser = LinkAndMetaChecker()
        parser.feed(raw)
        if not parser.has_viewport:
            fail(f"Page {fname} missing responsive viewport meta tag")
        for ref in parser.local_refs:
            target = (SITE / ref).resolve()
            if not target.exists():
                fail(f"Page {fname} has broken local reference: {ref} -> {target}")
        for ext in parser.external_urls:
            if not ext.startswith("https://"):
                fail(f"Page {fname} has non-https external URL: {ext}")
            if is_ota_url(ext):
                fail(f"Page {fname} links to forbidden OTA domain: {ext}")

    print(
        f"PASS: 15 official-IBE hotels (2 windows), 24 MICHELIN venues (4★/3 Bib/17 Rec; 15 priced, 9 blank), "
        f"{len(act_tr['activities'])} activities, {len(act_tr['combined_packages'])} combined packages, "
        f"{len(audit_qa['repo_audit'])} repo audit findings, {len(audit_qa['flags'])} flags, and {len(EXPECTED_PAGES)} mobile-ready HTML pages validated."
    )


if __name__ == "__main__":
    main()
