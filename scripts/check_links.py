#!/usr/bin/env python3
"""check_links.py — resolve every external URL the built site publishes.

WHY THIS EXISTS
    validate.py checks internal structure only. Every external claim on this site
    ("official page", "Instagram", "tickets here") has, until now, been checked by a
    human reading a page. That does not scale past 400 links and it silently rots:
    a venue renames a domain and the citation keeps looking authoritative.

    This script does the mechanical half: for every href="http(s)://..." in the
    built pages it records the HTTP status, redirect chain and final URL. Anything
    that does not answer 2xx is printed as a finding.

WHAT IT DOES NOT DO
    A 200 does not mean the page supports the claim. A 404 on a bot-protected site
    does not mean the link is dead. Both cases are reported as "needs a human look"
    rather than as pass/fail, and the exit code stays 0 unless --strict is passed.
    This is deliberate: a red build over a bot-blocked hotel page would train the
    reader to ignore the check, which is the failure mode this repo has already had
    once (see the 'nan' false positive recorded in COORDINATION.md).

USAGE
    python3 scripts/check_links.py                # all pages, summary + findings
    python3 scripts/check_links.py --strict       # exit 1 if any hard failure
    python3 scripts/check_links.py --only docs/restaurants.html
    python3 scripts/check_links.py --limit 40     # spot-check the first 40

No third-party dependencies: urllib only, so it runs anywhere the repo clones.
"""
import argparse
import concurrent.futures
import re
import ssl
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
UA = "Mozilla/5.0 (compatible; Vegas1-link-checker/1.0; +https://kanlerxz87-cyber.github.io/Vegas1/)"
TIMEOUT = 20

# Hosts that answer automated traffic with a wall rather than a page. A non-2xx
# here is a limitation of the check, not a dead link, so it is reported apart.
WALLED = (
    "booking.com", "tripadvisor.", "yelp.", "opentable.", "sevenrooms.",
    "facebook.com", "instagram.com", "tiktok.com", "x.com", "twitter.com",
    "linkedin.com", "youtube.com", "resy.com", "toasttab.com",
    "caesars.com", "mgmresorts.com", "venetianlasvegas.com", "wynnlasvegas.com",
    "rwlasvegas.com", "venetian.com", "fontainebleaulasvegas.com",
)


def is_walled(host: str) -> bool:
    host = host.lower()
    return any(w in host for w in WALLED)


def resolve(url: str, ctx) -> dict:
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "*/*"})
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT, context=ctx) as r:
            return {"url": url, "status": r.status, "final": r.geturl(), "error": ""}
    except urllib.error.HTTPError as ex:
        return {"url": url, "status": ex.code, "final": ex.geturl() or url, "error": ex.reason or ""}
    except urllib.error.URLError as ex:
        return {"url": url, "status": 0, "final": url, "error": str(ex.reason)}
    except (ssl.SSLError, TimeoutError, OSError) as ex:
        return {"url": url, "status": 0, "final": url, "error": type(ex).__name__ + ": " + str(ex)[:80]}


def links_in(path: Path):
    src = path.read_text(encoding="utf-8")
    return sorted(set(re.findall(r'href="(https?://[^"]+)"', src)))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--strict", action="store_true", help="exit 1 on any hard failure")
    ap.add_argument("--only", help="check one page, e.g. docs/restaurants.html")
    ap.add_argument("--limit", type=int, default=0, help="cap the number of URLs checked")
    ap.add_argument("--workers", type=int, default=12)
    args = ap.parse_args()

    pages = [Path(args.only)] if args.only else sorted(DOCS.glob("*.html"))
    per_page = {p.name: links_in(p) for p in pages}
    all_urls = sorted({u for us in per_page.values() for u in us})
    if args.limit:
        all_urls = all_urls[: args.limit]

    print(f"{len(pages)} pages · {sum(len(v) for v in per_page.values())} link occurrences · "
          f"{len(all_urls)} unique external URLs\n")

    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    results = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as pool:
        for res in pool.map(lambda u: resolve(u, ctx), all_urls):
            results[res["url"]] = res

    # Detect a sandbox with no outbound HTTP at all. Without this, a fully
    # firewalled runner reports every link as dead, which is worse than no check.
    if results and all(r["status"] == 0 for r in results.values()):
        print("\nNO OUTBOUND HTTP FROM THIS MACHINE.")
        print("Every URL failed at connect/TLS before any server answered, so this run "
              "says nothing about the links. Run it on a host with internet access "
              "(or verify with a page fetcher) before drawing any conclusion.")
        return 0

    ok = [r for r in results.values() if 200 <= r["status"] < 300]
    redirected = [r for r in ok if r["final"].rstrip("/") != r["url"].rstrip("/")]
    hard = [r for r in results.values() if not (200 <= r["status"] < 300)]
    walled_fail = [r for r in hard if is_walled(r["url"])]
    real_fail = [r for r in hard if not is_walled(r["url"])]

    print(f"2xx                 {len(ok)}")
    print(f"  of which redirect {len(redirected)}")
    print(f"non-2xx total       {len(hard)}")
    print(f"  bot-walled hosts  {len(walled_fail)}  (inconclusive, not a dead link)")
    print(f"  needs a look      {len(real_fail)}")

    if redirected:
        print("\n-- redirects (a redirect can hide a rebrand; re-open the target, cf. F-47) --")
        for r in sorted(redirected, key=lambda x: x["url"]):
            print(f"  {r['url']}\n     -> {r['final']}")

    if real_fail:
        print("\n-- non-2xx on a host that is not bot-walled: open these by hand --")
        for r in sorted(real_fail, key=lambda x: (x["status"], x["url"])):
            print(f"  [{r['status'] or 'ERR'}] {r['url']}  {r['error'][:70]}")

    if walled_fail:
        print("\n-- bot-walled, status is not evidence either way --")
        for r in sorted(walled_fail, key=lambda x: x["url"])[:40]:
            print(f"  [{r['status'] or 'ERR'}] {r['url']}")
        if len(walled_fail) > 40:
            print(f"  ... and {len(walled_fail) - 40} more")

    print("\nThis checker proves a URL answers. It cannot prove the page says what "
          "the table claims — that still needs a human read (see README 'Verification').")
    return 1 if (args.strict and real_fail) else 0


if __name__ == "__main__":
    sys.exit(main())
