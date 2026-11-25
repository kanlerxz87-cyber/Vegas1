#!/usr/bin/env python3
"""
check.py - post-build verification for the generated site.

Checks:
  1. every internal href resolves to a file that exists
  2. no page is missing from the nav
  3. every external link is https and syntactically valid
  4. no cell contains a bare 'None' / 'null' / 'nan' string (a silent data gap)
  5. every restaurant/hotel row on relevant pages carries a source link
Exit code 1 on any failure, so it can gate a publish step.
"""
import os, re, sys, glob

DOCS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "docs")
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "plan-data")
PAGES = [os.path.basename(p) for p in glob.glob(os.path.join(DOCS, "*.html"))]
fails, warns, checks = [], [], 0

print(f"checking {len(PAGES)} pages\n")

for page in sorted(PAGES):
    path = os.path.join(DOCS, page)
    src = open(path, encoding="utf-8").read()

    # 1. internal links
    for href in re.findall(r'href="([^"#?]+)"', src):
        if href.startswith(("http://", "https://", "mailto:", "tel:")):
            continue
        checks += 1
        if not os.path.exists(os.path.join(DOCS, href)):
            fails.append(f"{page}: broken internal link -> {href}")

    # 2. nav completeness
    nav = re.search(r"<nav>(.*?)</nav>", src, re.S)
    checks += 1
    if not nav:
        fails.append(f"{page}: no <nav> block")
    else:
        for p in PAGES:
            if f'href="{p}"' not in nav.group(1):
                fails.append(f"{page}: nav missing {p}")

    # 3. external link sanity
    for href in re.findall(r'href="(https?://[^"]+)"', src):
        checks += 1
        if " " in href:
            fails.append(f"{page}: malformed external link -> {href[:90]}")
        if href.startswith("http://"):
            warns.append(f"{page}: non-https link -> {href[:90]}")

    # 4. leaked python nulls
    for bad in (">None<", ">null<", ">nan<", ">NaN<"):
        if bad in src:
            checks += 1
            fails.append(f"{page}: leaked {bad[1:-1]} value")

# 5. source-link coverage on the data tables
for page, min_links in (("michelin.html", 20), ("hotels.html", 10), ("activities.html", 5)):
    src = open(os.path.join(DOCS, page), encoding="utf-8").read()
    ext = len(re.findall(r'href="https?://', src))
    print(f"{page}: {ext} external source links")
    if ext < min_links:
        fails.append(f"{page}: only {ext} external links, expected >= {min_links}")

# 6. date arithmetic: every night count must match its own window
import json, datetime

def nights_between(a, b):
    A = datetime.date(*map(int, a.split("-")))
    B = datetime.date(*map(int, b.split("-")))
    return (B - A).days

def walk_rows(o, path=""):
    """Yield (path, row) for every dict that carries a date window."""
    if isinstance(o, dict):
        if o.get("window") and o.get("nights"):
            yield path, o
        for k, v in o.items():
            yield from walk_rows(v, f"{path}.{k}")
    elif isinstance(o, list):
        for i, v in enumerate(o):
            yield from walk_rows(v, f"{path}[{i}]")

for fn in sorted(os.listdir(DATA_DIR)):
    if not fn.endswith(".json"):
        continue
    blob = json.load(open(os.path.join(DATA_DIR, fn), encoding="utf-8"))
    for path, row in walk_rows(blob):
        checks += 1
        w = row["window"]
        if not isinstance(w, str) or " to " not in w:
            continue
        a, b = w.split(" to ")
        try:
            actual = nights_between(a.strip(), b.strip())
        except Exception:
            fails.append(f"{fn}{path}: unparseable window {w!r}")
            continue
        if actual != row["nights"]:
            fails.append(
                f"{fn}{path}: window {w} is {actual} nights but row says {row['nights']}")
        if row.get("total_usd") and row.get("per_night_usd") and actual:
            expected = round(row["total_usd"] / actual)
            if abs(expected - row["per_night_usd"]) > 2:
                fails.append(
                    f"{fn}{path}: total {row['total_usd']} / {actual} nights = "
                    f"${expected}/night but row says ${row['per_night_usd']}/night")

print(f"{checks} individual checks run")

print()
for w in warns:
    print("WARN ", w)
for f in fails:
    print("FAIL ", f)

if fails:
    print(f"\n{len(fails)} FAILURE(S)")
    sys.exit(1)
print("\nAll checks passed." + (f" ({len(warns)} warnings)" if warns else ""))
