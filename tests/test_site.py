"""Offline publication/evidence regression tests — not remote fact verification.

Extends the peer integration's intent against the single live field renderer:
unknowns stay null/blank, prior research survives with attribution, exact operator
itemizations reconcile but do not become qualified offers, and every local page
is generated, linked, responsive-labelled and mirrored to root/docs.
"""
import copy
from datetime import date, timedelta
from decimal import Decimal
from html.parser import HTMLParser
import json
from pathlib import Path
import sys
import unittest
from unittest.mock import patch
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import verified_views as site
import gen_site
import build


class Document(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ids, self.links, self.rows, self.tables = [], [], [], []
        self.labels, self.evidence, self.fields = [], [], []
        self.row = self.cell = None
        self.in_body = False

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if "id" in a:
            self.ids.append(a["id"])
        if "data-evidence" in a:
            self.evidence.append(a["data-evidence"])
            self.fields.append(a.get("data-field"))
        if tag == "table":
            self.tables.append(a)
        if tag == "tbody":
            self.in_body = True
        if tag == "tr" and self.in_body:
            self.row = {"cells": [], "links": [], "id": a.get("id"), "key": a.get("data-row")}
        if tag in ("td", "th") and self.row is not None:
            self.cell = ""
            self.labels.append(a.get("data-label"))
        if tag == "a":
            self.links.append(a.get("href", ""))
            if self.row is not None:
                self.row["links"].append(a.get("href", ""))

    def handle_data(self, text):
        if self.cell is not None:
            self.cell += text

    def handle_endtag(self, tag):
        if tag in ("td", "th") and self.cell is not None:
            self.row["cells"].append(self.cell.strip())
            self.cell = None
        if tag == "tr" and self.row is not None:
            self.rows.append(self.row)
            self.row = None
        if tag == "tbody":
            self.in_body = False


def render():
    return site.build_verified_pages(gen_site.page, gen_site.build_flagged)


class SiteTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.E = site.load_manifest()
        cls.pages = render()
        cls.docs = {n: Document() for n in cls.pages}
        for name, doc in cls.docs.items():
            doc.feed(cls.pages[name])

    def test_evidence_schema_and_non_mutating_build(self):
        before = {p: p.read_bytes() for p in (ROOT / "data").glob("*.json")}
        build.validate()
        self.assertEqual(before, {p: p.read_bytes() for p in before})

    def test_all_source_rows_present(self):
        for group in ("restaurants", "activities", "hotels"):
            raw = json.loads((ROOT / f"data/{group}.json").read_text())[group]
            self.assertEqual(set(self.E[group]), {r["id"] for r in raw})
            rows = [r for r in self.docs[group + ".html"].rows if r["key"]]
            self.assertEqual({r["key"] for r in rows}, {f"{group}/{r['id']}" for r in raw})
        self.assertEqual(len(self.E["hotels"]), 34)
        self.assertEqual(len(self.E["restaurants"]), 24)
        self.assertEqual(len(self.E["activities"]), 6)
        self.assertIn("mgm-grand", self.E["hotels"])
        self.assertIn("hilton-resorts-world", self.E["hotels"])

    def test_every_table_body_row_has_external_reference(self):
        for name, doc in self.docs.items():
            for row in doc.rows:
                with self.subTest(page=name, row=row["id"] or row["cells"][:1]):
                    self.assertTrue(any(u.startswith("https://") for u in row["links"]))

    def test_all_pages_and_internal_anchors(self):
        self.assertEqual(set(self.pages), {"index.html", "summary.html", "pricing.html", "hotels.html", "restaurants.html", "activities.html", "transit.html", "dining.html", "costs.html", "itinerary.html", "questions.html", "suggestions.html", "flagged.html", "verification.html", "sources.html", "repo-review.html"})
        for name, doc in self.docs.items():
            self.assertEqual(len(doc.ids), len(set(doc.ids)), name + " duplicate IDs")
            for url in doc.links:
                parsed = urlsplit(url)
                if parsed.scheme or parsed.netloc:
                    continue
                target = unquote(parsed.path) or name
                self.assertIn(target, self.pages, (name, url))
                if parsed.fragment:
                    self.assertIn(unquote(parsed.fragment), self.docs[target].ids, (name, url))

    def test_hotel_final_offer_and_bus_cells_stay_blank(self):
        rows = [r for r in self.docs["hotels.html"].rows if (r["key"] or "").startswith("hotels/")]
        self.assertEqual(len(rows), 34)
        for row in rows:
            self.assertEqual(row["cells"][6:8], ["—", "—"], row["key"])
        self.assertEqual([r["key"].split("/")[1] for r in rows], sorted(self.E["hotels"], key=lambda i: self.E["hotels"][i]["name"].casefold()))
        for record in self.E["hotels"].values():
            self.assertIsNone(site.value(record, "total_7n"))
            self.assertIsNone(site.value(record, "within_60_bus"))
        self.assertTrue(any(t.get("id") == "official-hotel-decisions" for t in self.docs["hotels.html"].tables))

    def test_named_room_evidence_is_field_specific(self):
        self.assertIsNotNone(site.value(self.E["hotels"]["venetian"], "bed"))
        self.assertIsNotNone(site.value(self.E["hotels"]["hilton-resorts-world"], "bathroom"))
        self.assertIsNone(site.value(self.E["hotels"]["nobu-caesars"], "bed"))
        self.assertIsNone(site.value(self.E["hotels"]["mgm-grand"], "room"))
        self.assertIsNone(site.value(self.E["hotels"]["crockfords"], "total_7n"))

    def test_no_assumed_meal_or_trip_total(self):
        for rid in ("guy-savoy", "kame-omakase", "esthers-kitchen"):
            self.assertIsNone(site.value(self.E["restaurants"][rid], "price_2adults"))
            row = next(r for r in self.docs["restaurants.html"].rows if r["key"] == "restaurants/" + rid)
            self.assertEqual(row["cells"][4], "—")
        for name in ("restaurants.html", "dining.html", "costs.html", "hotels.html", "index.html"):
            for forbidden in ("$3,000", "$520", "$1,855.06", "$564", "$4,739", "$5,831"):
                self.assertNotIn(forbidden, self.pages[name], (name, forbidden))
        for text in ("$120", "$80", "$370", "$397.76", "$320"):
            self.assertIn(text, self.pages["dining.html"])
        self.assertIn("currently closed", self.pages["dining.html"])
        self.assertIn("not a complete", self.pages["dining.html"])

    def test_itemized_observation_is_not_a_qualified_offer(self):
        h = self.E["hotels"]["hilton-resorts-world"]
        f = h["fields"]["observed_total_7n"]
        p = f["itemized"]
        amount = sum(Decimal(x) for x in p["room_nights"])
        amount += sum(Decimal(p[k]) for k in ("room_tax", "resort_fees", "resort_fee_tax"))
        self.assertEqual(amount, Decimal("2200.15"))
        self.assertIsNone(site.value(h, "total_7n"))
        self.assertIn("$2,200.15", self.pages["pricing.html"])
        self.assertIn("not a qualified offer", self.pages["pricing.html"])
        self.assertIn("not Crockfords", self.pages["pricing.html"])

    def test_corrupt_itemization_and_incomplete_qualification_are_rejected(self):
        d = copy.deepcopy(self.E)
        d["hotels"]["hilton-resorts-world"]["fields"]["observed_total_7n"]["amount"] = "2200.16"
        self.assertTrue(any("non-reconciling" in e for e in site.validate_manifest(d)))
        d = copy.deepcopy(self.E)
        h = d["hotels"]["hilton-resorts-world"]
        h["fields"]["total_7n"] = copy.deepcopy(h["fields"]["observed_total_7n"])
        self.assertTrue(any("qualification" in e for e in site.validate_manifest(d)))

    def test_model_count_cannot_be_promoted_without_journeys(self):
        d = copy.deepcopy(self.E)
        h = d["hotels"]["caesars-palace"]
        h["fields"]["within_60_bus"].update(value=24, status="verified", source="rtc-trip")
        self.assertTrue(any("itinerary-level" in e for e in site.validate_manifest(d)))

    def test_missing_coverage_sources_and_states_fail_closed(self):
        for mutate, expected in (
            (lambda d: d["restaurants"].pop("guy-savoy"), "coverage"),
            (lambda d: d["sources"].pop("michelin"), "source"),
            (lambda d: d["restaurants"]["china-poblano"]["fields"].pop("days"), "explicit verification"),
            (lambda d: d["restaurants"]["guy-savoy"]["fields"]["price_2adults"].update(value="$3,000"), "null/unverified"),
        ):
            d = copy.deepcopy(self.E)
            mutate(d)
            self.assertTrue(any(expected in e for e in site.validate_manifest(d)))

    def test_unchecked_or_unofficial_source_never_authorizes_a_value(self):
        for changes in ({"authority": "third_party"}, {"result": "not_rechecked", "checked": None}):
            d = copy.deepcopy(self.E)
            d["sources"]["r-china-poblano"].update(changes)
            self.assertTrue(any("no checked official evidence" in e for e in site.validate_manifest(d)))
            with patch.object(site, "load_manifest", return_value=d):
                with self.assertRaisesRegex(ValueError, "Evidence validation failed"):
                    render()

    def test_blank_never_falls_back_and_zero_is_not_missing(self):
        r = {"room": "unsupported legacy King", "fields": {"room": {"value": None, "status": "unverified", "source": "x"}}}
        self.assertIsNone(site.value(r, "room"))
        self.assertIn("—", site.cell(r, "room"))
        self.assertNotIn("legacy", site.cell(r, "room"))
        r["fields"]["room"].update(value=0, status="verified")
        self.assertEqual(site.value(r, "room"), 0)
        self.assertNotIn("—", site.cell(r, "room"))

    def test_schedule_and_source_conflicts_stay_explicit(self):
        self.assertIn("9 AM–9 PM", site.value(self.E["activities"]["mob-museum"], "hours"))
        self.assertIsNone(site.value(self.E["activities"]["high-roller"], "hours"))
        self.assertIsNone(site.value(self.E["restaurants"]["esthers-kitchen"], "hours"))
        self.assertIsNone(site.value(self.E["restaurants"]["e-by-jose-andres"], "days"))
        self.assertIn("Tue–Sun vs Tue–Sat", self.pages["restaurants.html"])
        self.assertIn("temporarily closed", self.pages["restaurants.html"].lower())
        self.assertIn("6 PM–2 AM", self.pages["activities.html"])
        self.assertIn("2027 Admission", self.pages["activities.html"])

    def test_prior_research_and_all_backlog_entries_survive(self):
        # Media research is retained on Flagged, not silently promoted to official facts.
        for group in ("restaurants", "activities"):
            for row in json.loads((ROOT / f"data/{group}.json").read_text())[group]:
                for url in row.get("youtube", []):
                    self.assertIn(url, self.docs["flagged.html"].links)
        for x in json.loads((ROOT / "data/site-suggestions.json").read_text())["suggestions"]:
            self.assertIn(x["id"], self.docs["suggestions.html"].ids)
        for x in json.loads((ROOT / "data/verification-2026-11-27.json").read_text())["checks"]:
            self.assertIn(x["id"], self.docs["flagged.html"].ids)
        self.assertIn("Original provenance / caveat", self.pages["flagged.html"])
        self.assertIn("oEmbed", self.pages["flagged.html"])
        self.assertIn("F-54-history-2", self.docs["flagged.html"].ids)
        for n in range(58, 75):
            self.assertIn(f"F-{n}", self.docs["flagged.html"].ids)

    def test_social_scope_is_not_award_or_current_opening_evidence(self):
        self.assertIn("Shared", self.E["sources"]["ig-cote"]["note"])
        self.assertIn("three stars", self.E["sources"]["ig-joel-robuchon"]["note"])
        self.assertEqual(site.value(self.E["restaurants"]["joel-robuchon"], "award"), "2 stars")
        self.assertIsNone(site.value(self.E["restaurants"]["latelier-robuchon"], "instagram"))
        self.assertIn("parent venue", self.pages["activities.html"])
        self.assertIn("not a successfully opened target", self.pages["questions.html"])

    def test_rendered_evidence_keys_exist_and_are_official(self):
        for doc in self.docs.values():
            self.assertTrue(all(doc.fields))
            for key in doc.evidence:
                self.assertIn(key, self.E["sources"])
                source = self.E["sources"][key]
                self.assertEqual(source["authority"], "official")
                self.assertEqual(source["result"], "fetched")

    def test_mobile_accessibility_and_escaping(self):
        for name, content in self.pages.items():
            self.assertIn('name="viewport"', content)
            self.assertIn("Skip to content", content)
            self.assertEqual(content.count("<nav>"), 1)
            self.assertEqual(content.count("<h1>"), 1)
            self.assertTrue(all(self.docs[name].labels), name)
        self.assertIn("data-label", gen_site.CSS)
        self.assertIn("max-width:700px", gen_site.CSS)
        self.assertNotIn("<script>", site.cell({"fields": {"x": {"value": "<script>alert(1)</script>", "status": "verified", "source": "safe"}}}, "x"))
        self.assertNotIn("<script>", site.link("https://example.com/?x=\"", "<script>"))
        with self.assertRaises(ValueError):
            site.link("javascript:alert(1)", "bad")
        self.assertIn("&lt;script&gt;", gen_site.page("x", "<script>", "<script>", ""))

    def test_date_arithmetic_and_no_rounded_average_expansion(self):
        starts = []
        d = date(2027, 2, 15)
        while d + timedelta(days=7) <= date(2027, 3, 23):
            starts.append(d)
            d += timedelta(days=1)
        self.assertEqual(len(starts), 30)
        self.assertEqual(starts[-1], date(2027, 3, 16))
        self.assertEqual(date(2027, 2, 15) + timedelta(days=14), date(2027, 3, 1))
        self.assertNotIn("$4,739", self.pages["pricing.html"])
        self.assertNotIn("$5,831", self.pages["pricing.html"])
        self.assertIn("4 December 2026", self.pages["pricing.html"])

    def test_generated_output_matches_renderer_and_root_docs(self):
        for name, content in self.pages.items():
            self.assertEqual((ROOT / name).read_text(), content, name + " stale root output")
            self.assertEqual((ROOT / "docs" / name).read_text(), content, name + " stale docs output")
        self.assertEqual((ROOT / "style.css").read_text(), gen_site.CSS)
        self.assertEqual((ROOT / "docs/style.css").read_text(), gen_site.CSS)
        self.assertTrue((ROOT / ".nojekyll").is_file())
        self.assertTrue((ROOT / "docs/.nojekyll").is_file())


if __name__ == "__main__":
    unittest.main()
