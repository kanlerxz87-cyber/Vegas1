#!/usr/bin/env python3
"""validate.py — link + structure checks for the built site in docs/."""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
PAGES = sorted(DOCS.glob("*.html"))
fails, warns = [], []

for p in PAGES:
    src = p.read_text(encoding="utf-8")
    # 1. every internal .html link must exist
    for href in re.findall(r'href="([^"#:]+\.html)', src):
        if not (DOCS / href).exists():
            fails.append(f"{p.name}: broken internal link -> {href}")
    # 2. every page must have the nav and a charset
    if 'charset="utf-8"' not in src:
        fails.append(f"{p.name}: missing charset")
    if 'name="viewport"' not in src:
        fails.append(f"{p.name}: missing viewport")
    if src.count("<nav>") != 1:
        fails.append(f"{p.name}: nav count {src.count('<nav>')}")
    # 3. table rows must not contain unescaped stray braces from f-strings.
    #    The bare words are matched on token boundaries: a substring test fired on
    #    ordinary prose ("provenance" contains "nan") and produced false warnings.
    for bad in ("{{", "}}"):
        if bad in src:
            warns.append(f"{p.name}: contains literal {bad!r}")
    for tok in ("None", "nan"):
        if re.search(rf"(?<![A-Za-z0-9_]){tok}(?![A-Za-z0-9_])", src):
            warns.append(f"{p.name}: contains standalone token {tok!r}")
    # 4. count links
    ext = len(re.findall(r'href="https?://', src))
    print(f"{p.name:20} {len(src):>7} bytes  {ext:>4} external links")

# 4b. every cross-page anchor must exist in its target page
texts = {p.name: p.read_text(encoding="utf-8") for p in PAGES}
for p in PAGES:
    for tgt, anchor in re.findall(r'href="([^":#]+\.html)#([^"]+)"', texts[p.name]):
        if tgt not in texts:
            fails.append(f"{p.name}: anchor link to missing page {tgt}#{anchor}")
        elif f'id="{anchor}"' not in texts[tgt]:
            fails.append(f"{p.name}: {tgt} has no id={anchor!r}")

# 5. total external links, and every restaurant/hotel must carry one
total_ext = sum(len(re.findall(r'href="https?://', p.read_text(encoding='utf-8'))) for p in PAGES)
print(f"\ntotal external links: {total_ext}")

# 6. style.css referenced by every page and present
for p in PAGES:
    if 'href="style.css"' not in p.read_text(encoding="utf-8"):
        fails.append(f"{p.name}: does not load style.css")
if not (DOCS / "style.css").exists():
    fails.append("style.css missing")
if not (DOCS / ".nojekyll").exists():
    warns.append(".nojekyll missing — Pages may run Jekyll")

print()
for w in warns:
    print("WARN:", w)
for f in fails:
    print("FAIL:", f)
print(f"\n{len(PAGES)} pages · {len(fails)} failures · {len(warns)} warnings")
sys.exit(1 if fails else 0)
