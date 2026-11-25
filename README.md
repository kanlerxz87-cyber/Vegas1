# Vegas1 — Las Vegas Trip Planner (Feb 2027)

Mobile-friendly trip-planning site for a 2-adult Las Vegas trip:
preferred **Feb 15–18, 2027**, window **Feb 15 – Mar 23, 2027**.

## Pages

| File | Contents |
|---|---|
| `index.html` | Landing page / dashboard |
| `summary.html` | Executive summary |
| `hotels.html` | 9 verified 7-night hotel quotes + 3-night preferred window + ranking by MICHELIN proximity + cheapest-time analysis |
| `michelin.html` | All 24 MICHELIN-listed LV restaurants: Star vs Bib Gourmand vs listed, cost for 2 adults, hours, official + social links |
| `activities.html` | 9 activities within ~1 h transit, hours, costs, sources, social links, RTC transit baseline |
| `suggestions.html` | Suggestions + open questions (Q1–Q10) that must be answered before booking |
| `flagged.html` | Flagged-for-review: blanks, source conflicts, rejected sources, staleness warnings |
| `css/style.css` | Mobile-first stylesheet |
| `data/*.json` | Machine-readable datasets (hotels, michelin, activities) |
| `VERIFICATION.md` | Line-by-line verification log (source URL → value read) |
| `COORDINATION.md` | Multi-session task board |

## Verification policy

- Every price/hour/address is read from a linked source and dated **2026-11-25**.
- Unconfirmable values are **left blank** and listed in `flagged.html` — never inferred.
- Source conflicts are displayed as conflicts, not silently resolved.

## Local preview

Open `index.html` in a browser, or serve the folder:

```bash
python3 -m http.server 8080
```

## GitHub Pages

Published from branch `arena/48dbf0ae-vegas1` (see COORDINATION.md T09).
