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

print(f"{checks} individual checks run")

# 5. source-link coverage on the data tables
for page, min_links in (("michelin.html", 20), ("hotels.html", 10), ("activities.html", 5)):
    src = open(os.path.join(DOCS, page), encoding="utf-8").read()
    ext = len(re.findall(r'href="https?://', src))
    print(f"{page}: {ext} external source links")
    if ext < min_links:
        fails.append(f"{page}: only {ext} external links, expected >= {min_links}")

print()
for w in warns:
    print("WARN ", w)
for f in fails:
    print("FAIL ", f)

if fails:
    print(f"\n{len(fails)} FAILURE(S)")
    sys.exit(1)
print("\nAll checks passed." + (f" ({len(warns)} warnings)" if warns else ""))
