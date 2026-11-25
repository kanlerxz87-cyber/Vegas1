# Vegas1 — Las Vegas Trip Planner

A verified, source-linked trip planner for a couple's 1–2 week vacation to **Las Vegas**
between **February 15 and March 23, 2027** (preferred window **Feb 15–18, 2027**).

## What's inside
- **Michelin restaurants** — all 24 Las Vegas distinctions in the inaugural **2026 MICHELIN
  Guide American Southwest** (1 Two-Star, 3 One-Star, 3 Bib Gourmand, 17 Selected), with hours,
  cost estimates, official links and social links. Star vs. listed is clearly separated.
- **Hotels** — 12 candidate hotels (private bathroom, queen+ bed, 2 adults) with 7-night total
  price estimates and resort-fee/tax breakdown.
- **Ranking** — hotels ranked by Michelin restaurant density within 1 hour (RTC Deuce bus +
  Las Vegas Monorail; Las Vegas has no subway).
- **Activities** — 12 activities within ~1 hour of a central-Strip base (Grand Canyon flagged
  as exceeding the rule).
- **Pricing & booking** — 7-night totals and the cheapest upcoming booking window.
- **Executive summary, suggestions, open questions, verification, flagged-for-review** pages.

## Site
A static, mobile-friendly multi-page site (no build step). A GitHub Actions workflow
(`.github/workflows/pages.yml`) is ready to deploy it to **GitHub Pages** on every push to this branch.

> **To go live (one toggle, no code change):** open **Settings → Pages → Source** and choose either
> **branch `arena/6263258d-vegas1`, folder `/ (root)`** or **GitHub Actions**. The sandbox's GitHub
> App token cannot change this setting automatically (HTTP 403), so this single repo-settings toggle
> is the only manual step required; the site deploys immediately after. See
> [Flagged for Review](flagged.html) item 10.

## Verification
Every table row links to an official source. Values that could not be confirmed from an official
source are **left blank and flagged** on the [Flagged for Review](flagged.html) page — never
inferred. See [Verification](verified.html).

## Coordination
`COORDINATION.md` is the shared task board (status, owning session, file scope, sources,
verification, irregularities).
