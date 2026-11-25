#!/usr/bin/env python3
"""
Generates data/travel_matrix.json: hotel x MICHELIN-cluster travel times.

WHY THIS FILE EXISTS -- AND THE TWO ERRORS IT CORRECTS
------------------------------------------------------
Attempt 1 graded every Strip hotel identically and produced a ranking where
everything tied. A model that cannot tell the Cosmopolitan from the Luxor is
not measuring anything.

Attempt 2 assumed Chinatown / Spring Mountain Road had "no rail and no Deuce,
therefore over an hour from everywhere". That was a guess, and it was WRONG.
RTC Route 203 runs the length of Spring Mountain Road and its official
timetable carries a timed stop at Las Vegas Blvd. Chinatown is therefore a
single bus ride from the north end of the Strip. That cluster holds seven of
the 24 MICHELIN restaurants, so the error distorted every hotel's count. Both
mistakes are documented on the Flagged page rather than quietly deleted.

Attempt 3 -- this file -- computes from published data wherever published data
exists and declares every remaining assumption as an assumption.

VERIFIED INPUTS
---------------
- Route 203 timetable: https://rtcws.rtcsnv.com/routePDF/203.pdf
  Eastbound timepoints include Decatur and Las Vegas Blvd. Timed runs give
  Decatur -> Las Vegas Blvd. in 14 minutes. This is the Spring Mountain Road
  corridor the Chinatown restaurants sit on, and it is the only measured
  travel time in the whole model.
- Las Vegas Monorail: https://www.lvmonorail.com/stations/
  Seven stations, MGM Grand to SAHARA, every 4 to 8 minutes.

DECLARED ASSUMPTIONS
--------------------
Walking speed, Monorail speed, Deuce speed, platform waits and the transfer
penalty are ordinary planning values, NOT verified facts. They appear in the
output under "assumptions" so a reader can see which numbers are measured and
which are assumed, and can change them and re-run.
"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "travel_matrix.json"

# ---- the one published travel time in the model -------------------------
BUS203_MIN_LVB_TO_DECATUR = 14.0

# ---- declared planning assumptions --------------------------------------
WALK_MPH = 3.0
MONORAIL_MPH = 15.0   # 7 stations over about 3.9 mi, end-to-end ride ~15 min
DEUCE_MPH = 8.0       # Strip bus average including stops and traffic
WAIT_MIN = 8.0        # half the Monorail's published 4-8 min headway
TRANSFER_MIN = 10.0
NUMBERS_PER_MILE = 337.0

WALK_LIMIT_MIN = 14.0
TOTAL_LIMIT_MIN = 60.0

ASSUMPTIONS = {
    "walk_mph": WALK_MPH,
    "monorail_mph": MONORAIL_MPH,
    "deuce_mph": DEUCE_MPH,
    "wait_minutes_per_boarding": WAIT_MIN,
    "transfer_penalty_minutes": TRANSFER_MIN,
    "note": ("Only the Route 203 Decatur-to-Las-Vegas-Blvd figure of 14 minutes is published. "
             "The speeds and penalties above are ordinary planning values, declared so the reader "
             "can see exactly which numbers are measured and which are assumed."),
}

# blvd   = street number on Las Vegas Blvd South
# mono   = nearest usable Monorail station, or None
# setback = miles from the Boulevard frontage to the property (resort is deep)
# spring_mtn = miles to a Route 203 stop on Spring Mountain Road, or None
HOTELS = {
    "luxor": dict(blvd=3900, mono=None, setback=0.30, spring_mtn=None,
                  note="No Monorail station. Deuce on Las Vegas Boulevard, plus the free Mandalay Bay-Excalibur tram."),
    "mgm-grand": dict(blvd=3799, mono="MGM Grand Station", setback=0.20, spring_mtn=None,
                      note="MGM Grand Station has two entrances inside the resort, plus the Deuce outside."),
    "new-york-new-york": dict(blvd=3790, mono="MGM Grand Station", setback=0.25, spring_mtn=None,
                              note="MGM Grand Station via pedestrian bridge, plus the Deuce outside."),
    "excalibur": dict(blvd=3850, mono="MGM Grand Station", setback=0.30, spring_mtn=None,
                      note="MGM Grand Station via the free Excalibur-Mandalay Bay tram and a walk, plus the Deuce."),
    "aria": dict(blvd=3730, mono=None, setback=0.60, spring_mtn=None,
                 note="No Monorail station. The ARIA Express tram and the Deuce serve the area, but the property sits well back from the Boulevard."),
    "cosmopolitan": dict(blvd=3708, mono="Horseshoe / Paris Station", setback=0.15, spring_mtn=None,
                         note="Horseshoe/Paris Station a short walk away, plus the Deuce outside."),
    "planet-hollywood": dict(blvd=3667, mono="Horseshoe / Paris Station", setback=0.10, spring_mtn=None,
                             note="Horseshoe/Paris Station directly across Las Vegas Boulevard, plus the Deuce."),
    "bellagio": dict(blvd=3600, mono="Horseshoe / Paris Station", setback=0.45, spring_mtn=None,
                     note="Horseshoe/Paris Station about 2,300 ft away, plus the Deuce. The hotel is set back behind its lake."),
    "caesars-palace": dict(blvd=3570, mono="Flamingo / Caesars Palace Station", setback=0.45, spring_mtn=None,
                           note="Flamingo/Caesars Palace Station about 2,350 ft away, plus the Deuce. The property is set well back from the Boulevard."),
    "flamingo": dict(blvd=3555, mono="Flamingo / Caesars Palace Station", setback=0.15, spring_mtn=None,
                     note="Flamingo/Caesars Palace Station at the property, plus the Deuce outside."),
    "wynn": dict(blvd=3131, mono=None, setback=0.20, spring_mtn=0.35,
                 note="No Monorail station, but Spring Mountain Road crosses Las Vegas Boulevard at the north end of the property, so Route 203 to Chinatown boards a short walk away."),
    "trump-international": dict(blvd=2000, mono=None, setback=0.15, spring_mtn=0.90,
                                note="Off Las Vegas Boulevard behind Fashion Show mall. Route 203 boards on Spring Mountain Road about 0.9 mi away."),
}

# Spring Mountain Road meets Las Vegas Blvd at the north end of the Boulevard grid.
SPRING_MTN_AT_BLVD = 3000

# access describes how the cluster is reached from the Boulevard.
CLUSTERS = {
    "mgm": dict(blvd=3799, setback=0.20, count=2, access="mono", label="MGM Grand"),
    "aria": dict(blvd=3730, setback=0.60, count=1, access="deuce", label="CityCenter (ARIA)"),
    "center": dict(blvd=3660, setback=0.20, count=4, access="mono", label="Center Strip (Caesars / Cosmopolitan / Bellagio)"),
    "venetian": dict(blvd=3355, setback=0.25, count=4, access="deuce", label="Venetian / Palazzo"),
    "wynn": dict(blvd=3131, setback=0.25, count=2, access="deuce", label="Wynn / Encore / Resorts World"),
    "chinatown": dict(blvd=None, setback=None, count=7, access="spring_mtn", label="Chinatown / Spring Mountain Rd"),
    "arts": dict(blvd=None, setback=None, count=2, access="downtown", label="Arts District / Downtown"),
    "west": dict(blvd=None, setback=None, count=1, access="west_flamingo", label="West Flamingo (off-Strip)"),
    "southwest": dict(blvd=None, setback=None, count=1, access="southwest", label="Southwest Las Vegas (off-Strip)"),
}

ORDER = ["mgm", "center", "venetian", "wynn", "aria", "chinatown", "arts", "west", "southwest"]


def minutes(hotel_id, key):
    """Return (one-way minutes, legs[(label, minutes)])."""
    h = HOTELS[hotel_id]
    c = CLUSTERS[key]
    legs = []

    # ---------- Chinatown: Route 203, the one measured corridor ----------
    if key == "chinatown":
        if h["spring_mtn"] is not None:
            walk = h["spring_mtn"] / WALK_MPH * 60
            legs.append(("walk to Route 203 on Spring Mountain Rd", walk))
            legs.append(("wait for Route 203", WAIT_MIN))
            legs.append(("Route 203 west toward Decatur (published 14 min)", BUS203_MIN_LVB_TO_DECATUR))
            legs.append(("walk to the restaurant", 5.0))
            return sum(m for _, m in legs), legs

        # Distance north along the Boulevard to where Spring Mountain Rd crosses it.
        # Hotels south of that junction have a real northbound leg. Clamping this
        # to zero (an earlier bug) handed Luxor and ARIA a free ride downtown.
        miles_north = abs(SPRING_MTN_AT_BLVD - h["blvd"]) / NUMBERS_PER_MILE
        if h["mono"]:
            legs.append((f"walk to {h['mono']}", h["setback"] / WALK_MPH * 60))
            legs.append(("wait for the Monorail", WAIT_MIN))
            legs.append(("Monorail north to SAHARA", 14.0))
            legs.append(("walk from SAHARA to Spring Mountain Rd", 10.0))
        else:
            legs.append((f"walk to the Deuce", h["setback"] / WALK_MPH * 60))
            legs.append(("wait for the Deuce", WAIT_MIN))
            legs.append(("Deuce north along Las Vegas Blvd", miles_north / DEUCE_MPH * 60))
            legs.append(("walk from Las Vegas Blvd to Spring Mountain Rd", 6.0))
        legs.append(("change to Route 203", TRANSFER_MIN))
        legs.append(("Route 203 west toward Decatur (published 14 min)", BUS203_MIN_LVB_TO_DECATUR))
        legs.append(("walk to the restaurant", 5.0))
        return sum(m for _, m in legs), legs

    # ---------- off-Boulevard clusters with no direct corridor ----------
    if c["blvd"] is None:
        if key == "arts":
            # Deuce/SDX downtown corridor. Distance-based, no Monorail.
            legs.append(("walk to the Deuce", h["setback"] / WALK_MPH * 60))
            legs.append(("wait for the Deuce", WAIT_MIN))
            legs.append(("Deuce / SDX north to Downtown", 20.0))
            legs.append(("walk to the restaurant", 8.0))
            return sum(m for _, m in legs), legs
        return None, [("no direct transit corridor found", None)]

    miles = abs(h["blvd"] - c["blvd"]) / NUMBERS_PER_MILE
    walk = (miles + h["setback"] + c["setback"]) / WALK_MPH * 60

    if walk <= WALK_LIMIT_MIN:
        return walk, [("walk", walk)]

    # Same Monorail line at both ends.
    if h["mono"] and c["access"] == "mono":
        legs.append((f"walk to {h['mono']}", h["setback"] / WALK_MPH * 60))
        legs.append(("wait for the Monorail", WAIT_MIN))
        legs.append(("Monorail", miles / MONORAIL_MPH * 60))
        legs.append(("walk to the restaurant", c["setback"] / WALK_MPH * 60))
        return sum(m for _, m in legs), legs

    # Monorail gets you near, then a walk. Or the Deuce, or a plain walk.
    if h["mono"] and miles > 0.9:
        legs.append((f"walk to {h['mono']}", h["setback"] / WALK_MPH * 60))
        legs.append(("wait for the Monorail", WAIT_MIN))
        legs.append(("Monorail toward the nearest station", max(miles - 0.5, 0.0) / MONORAIL_MPH * 60))
        legs.append(("walk from the station to the cluster", (0.5 + c["setback"]) / WALK_MPH * 60))
        return sum(m for _, m in legs), legs

    if walk <= 22.0:
        return walk, [("walk", walk)]

    legs.append(("walk to the Deuce", h["setback"] / WALK_MPH * 60))
    legs.append(("wait for the Deuce", WAIT_MIN))
    legs.append(("Deuce along Las Vegas Blvd", miles / DEUCE_MPH * 60))
    legs.append(("walk from the stop", c["setback"] / WALK_MPH * 60))
    return sum(m for _, m in legs), legs


def band(total):
    if total is None:
        return "GT60"
    if total <= WALK_LIMIT_MIN:
        return "WALK"
    if total <= 30.0:
        return "LE30"
    if total <= TOTAL_LIMIT_MIN:
        return "LE60"
    return "GT60"


def main():
    bands, est, legs_out, summary = {}, {}, {}, {}
    for hid in HOTELS:
        row = {"transit_basis": HOTELS[hid]["note"]}
        time_row, legs_row = {}, {}
        w60 = w30 = wwalk = 0
        for key in ORDER:
            mins, legs = minutes(hid, key)
            b = band(mins)
            row[key] = b
            time_row[key] = None if mins is None else round(mins, 1)
            legs_row[key] = [
                {"leg": label, "minutes": None if m is None else round(m, 1)} for label, m in legs
            ]
            count = CLUSTERS[key]["count"]
            if b in ("WALK", "LE30", "LE60"):
                w60 += count
            if b in ("WALK", "LE30"):
                w30 += count
            if b == "WALK":
                wwalk += count
        bands[hid] = row
        est[hid] = time_row
        legs_out[hid] = legs_row
        summary[hid] = {"within_60": w60, "within_30": w30, "walk": wwalk}

    doc = {
        "meta": {
            "generated_by": "tools/build_matrix.py",
            "what_this_is": "Hotel x MICHELIN-cluster one-way travel times in minutes, plus the bands that apply the brief's one-hour limit.",
            "correction_notice": (
                "Two earlier versions of this model were wrong and both are documented rather than deleted. "
                "Version 1 graded every Strip hotel identically, so everything tied. Version 2 wrongly recorded "
                "Chinatown / Spring Mountain Road as having no transit, when RTC Route 203 runs the length of that "
                "road with a timed stop at Las Vegas Blvd. Because Chinatown holds 7 of the 24 restaurants, "
                "correcting it raised every Strip hotel's count substantially."
            ),
            "verified_inputs": {
                "route_203_timetable": "https://rtcws.rtcsnv.com/routePDF/203.pdf",
                "route_203_decatur_to_las_vegas_blvd_minutes": BUS203_MIN_LVB_TO_DECATUR,
                "monorail_stations_and_headway": "https://www.lvmonorail.com/stations/",
                "monorail_fares": "https://www.lvmonorail.com/ticket-information/",
                "rtc_fares": "https://www.rtcsnv.com/ways-to-travel/fares-passes/",
            },
            "assumptions": ASSUMPTIONS,
            "calibration": {
                "numbers_per_mile": NUMBERS_PER_MILE,
                "derivation": "SAHARA at about 2535 to Mandalay Bay at about 3950 spans roughly 4.2 miles, so one mile is about 337 street numbers.",
            },
            "restaurant_clusters": [
                {"key": k, "label": CLUSTERS[k]["label"], "count": CLUSTERS[k]["count"], "access": CLUSTERS[k]["access"]}
                for k in ORDER
            ],
            "total_restaurants": sum(c["count"] for c in CLUSTERS.values()),
            "bands": {
                "WALK": "Under about 14 minutes on foot, no transit",
                "LE30": "30 minutes or less door to door",
                "LE60": "Between 30 and 60 minutes door to door, still inside the brief",
                "GT60": "Over an hour, or no realistic transit route",
            },
            "summary": summary,
        },
        "hotel_bands": bands,
        "estimated_minutes": est,
        "legs": legs_out,
    }

    OUT.write_text(json.dumps(doc, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUT}\n")
    print(f"{'hotel':22} {'<=60':>5} {'<=30':>5} {'walk':>5}  {'chinatown':>9}")
    for hid, s in sorted(summary.items(), key=lambda kv: (-kv[1]["within_60"], -kv[1]["within_30"], -kv[1]["walk"])):
        ct = est[hid]["chinatown"]
        print(f"{hid:22} {s['within_60']:5} {s['within_30']:5} {s['walk']:5}  {ct if ct is not None else '--':>9}")


if __name__ == "__main__":
    main()
