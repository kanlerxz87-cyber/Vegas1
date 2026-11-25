# Vegas1 — Las Vegas trip planner

Static site for planning a Las Vegas trip (2 adults, 15–22 Feb 2027; preferred 15–18 Feb).
Live site (GitHub Pages): https://kanlerxz87-cyber.github.io/Vegas1/

## Layout

- `docs/` — the published site (plain HTML/CSS; no build tools needed to view)
- `docs/data/*.json` — the data behind every table; each row carries its own source link
- `scripts/build_site.py` — regenerates `docs/*.html` from the JSON (Python 3 standard library only)
- `COORDINATION.md` — shared task board for parallel sessions

## Rebuild

```
python3 scripts/build_site.py
```

## Rules used

- Only values confirmed on an official or primary source are filled in. Anything else is blank and flagged "Unverified".
- Prices, booking windows, restaurant hours (except one), and social links are not yet verified and are left blank.
- Flags and conflicts between sources are listed on the "Flagged for review" page.
