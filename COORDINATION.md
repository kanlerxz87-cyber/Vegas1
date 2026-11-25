# COORDINATION.md — Shared Task Board

Session ID format: short hex id. Current sessions may work in parallel on separate branches
(`session-<id>/<task>`). Shared outputs (site index/nav, combined table data) change only in
the final integration session.

## Sessions

| Session ID | Branch | Status |
|---|---|---|
| 48dbf0ae | arena/48dbf0ae-vegas1 | active (claimed initial tasks + integration) |

## Tasks

| Task ID | Task | Status | Owner | Files touched |
|---|---|---|---|---|
| T01 | Repo init, COORDINATION.md task board | done | 48dbf0ae | COORDINATION.md |
| T02 | Research: Las Vegas hotels (price, location, amenities, 7-night totals, booking window) | in progress | 48dbf0ae | data/hotels.json, hotels.html |
| T03 | Research: Michelin Guide Las Vegas restaurants (star vs listed, costs for 2, hours, links, social links) | in progress | 48dbf0ae | data/michelin.json, michelin.html |
| T04 | Research: Activities within ~1 hour transit of hotel cluster (hours, links, social links) | in progress | 48dbf0ae | data/activities.json, activities.html |
| T05 | Site: landing page + nav + CSS (mobile-friendly dashboard) | in progress | 48dbf0ae | index.html, css/style.css |
| T06 | Executive summary page | in progress | 48dbf0ae | summary.html |
| T07 | Suggestions + open questions (decision-support) page | in progress | 48dbf0ae | suggestions.html |
| T08 | Flagged-for-review page + verification log | in progress | 48dbf0ae | flagged.html, VERIFICATION.md |
| T09 | Final integration, line-by-line re-verification, link check, GitHub Pages publish | in progress | 48dbf0ae | all |

Claim rule: write your session ID into the Owner column and commit+push the claim before
starting. Never start a task whose Owner is another session. If a claim is >60 min old with
no commits, another session may take over and note the handoff here.

## Log

- 2026-11-25 — 48dbf0ae — Repo was empty (README only). Created task board. Claimed T01–T05
  (research + site scaffolding) because no other sessions were present at start. T06–T09 left
  unclaimed for any parallel session; if none appears, 48dbf0ae will claim them later and note it.
- 2026-11-25 — 48dbf0ae — No parallel session appeared after extended research phase
  (Michelin lists verified, hotel 7-night rates verified for 9 properties, transit verified).
  Claimed T06–T09 per the takeover rule in the log entry above; no competing owner exists.
