#!/usr/bin/env python3
"""T17 (arena/c7c75f9a-vegas1) — apply values verified on 2026-11-27.

Every value written here was read on the venue's own page (or its own hosted
menu PDF) on 2026-11-27 and the URL is stored next to the value in
price_source / hours_source / social_source. Nothing is inferred: a venue with
no official price stays blank.

Run once from the repo root:  python3 scripts/t17_apply_verified.py
"""
import json

P = "data/restaurants.json"
d = json.load(open(P, encoding="utf-8"))
R = {r["id"]: r for r in d["restaurants"]}
CHECKED = "2026-11-27"


def setp(rid, price, note, src, basis, calc):
    r = R[rid]
    r["price_2adults"] = price
    r["price_note"] = note
    r["price_source"] = src
    r["price_basis"] = basis
    r["price_calc"] = calc
    r["price_checked"] = CHECKED


def sethour(rid, days, hours, exceptions, src):
    r = R[rid]
    r["days"] = days
    r["hours"] = hours
    if exceptions is not None:
        r["exceptions"] = exceptions
    r["hours_source"] = src
    r["hours_checked"] = CHECKED


setp(
    "wing-lei",
    "$397.76++ (tasting menu)",
    "Official Wing Lei dinner menu PDF linked from wynnlasvegas.com: Chef Tam's Signature Tasting Menu "
    "$198.88 per person. Two adults = $397.76 before tax and gratuity. Wine journeys $128.88 / $208.88 per "
    "person extra. A la carte: Imperial Peking Duck $148.88, Kagoshima Wagyu $321.88.",
    "https://cdn.wynnresorts.com/image/upload/v1781902951/visitwynn_pdfs_files/wing-lei-main-menu-new.pdf",
    "2 x $198.88 tasting menu printed on the official menu",
    "198.88 x 2 = 397.76",
)

setp(
    "bouchon",
    "$116-$186 (dinner for two, a la carte)",
    "Official Bouchon dinner menu PDF (venetianlasvegas.com): entrees Steak Frites $56.00, Poulet Roti $42.00, "
    "Saumon Poele $45.00, Truite Amandine $39.00, Steak au Poivre $105.00; starters $22-$36. Two guests sharing "
    "a starter and two entrees lands about $116-$186 before tax and gratuity. Wine is extra. Bouchon prints no "
    "prix-fixe dinner on this menu.",
    "https://www.venetianlasvegas.com/content/dam/vlvweb/restaurants/bouchon/dinner-menu.pdf",
    "Arithmetic over printed a-la-carte dinner prices (official menu)",
    "low: 26 (soupe) + 45 (saumon) + 45 (moules) = 116; high: 36 (foie gras) + 45 + 105 (steak au poivre) = 186",
)

setp(
    "cote",
    "$190++ (Feast of USDA Prime set menu)",
    "Official COTE menu PDF (venetianlasvegas.com): 'Feast of USDA Prime - 95 per person' (four selected cuts "
    "with Korean accompaniments; the whole table must participate). Two adults = $190 before tax and gratuity. "
    "A la carte examples on the same menu: Grand Plateau $325, Kobe A5 ribeye $82/oz, caviar service from "
    "$145/oz.",
    "https://www.venetianlasvegas.com/content/dam/vlvweb/restaurants/cote/menu.pdf",
    "2 x $95 Feast of USDA Prime printed on the official menu",
    "95 x 2 = 190",
)

setp(
    "partage",
    "$260 / $320 / $420 (tasting menus, two guests)",
    "Official Partage menu page (partage.vegas/menu): 5 courses $130, 7 courses $160, Signature 9-course $210 "
    "per person. Two adults = $260 / $320 / $420 before tax and gratuity. Seared foie gras add-on +$33 per "
    "guest; wine pairings $60 to $125 per person.",
    "https://partage.vegas/menu",
    "2 x printed per-person tasting-menu price (official venue page)",
    "130x2=260; 160x2=320; 210x2=420",
)

setp(
    "kabuto",
    "$260-$370 (omakase, two guests)",
    "Official Kabuto menu PDF (kabutolv.com/menu): Yoroi Chef Omakase $130 per person; Kabuto Premium Chef "
    "Omakase $185 per person. Two adults = $260 / $370 before tax and gratuity. Sake pairings $62 / $68 per "
    "person extra.",
    "https://www.kabutolv.com/s/kabuto-menu2026.pdf",
    "2 x printed per-person omakase price (official menu PDF)",
    "130x2=260; 185x2=370",
)

setp(
    "sparrow-and-wolf",
    "$298++ (Chef's Tasting Menu)",
    "Official Sparrow + Wolf menu page: Chef's Tasting Menu $149 per person (pairing $78; all guests at the "
    "table participate; automatic gratuity is added to the tasting). Two adults = $298 before tax and gratuity. "
    "A la carte: 32 oz Porterhouse $175, Te Mana Lamb Wellington $48, Wagyu Beef Cheek $42.",
    "https://sparrowandwolflv.com/menu/",
    "2 x $149 Chef's Tasting Menu printed on the official menu",
    "149 x 2 = 298",
)

setp(
    "soulbelly-bbq",
    "$80 (Chef's Choice for 2)",
    "Official SoulBelly menu (soulbellybbq.com/menu): 'Chef's Choice for 2 - 6 items from the pit & 6 sides - "
    "$80, no substitutions (+$2.50 for brisket)'. Two adults = $80 before tax and gratuity. Cheapest route: two "
    "One Meat Combos at $18 = $36.",
    "https://soulbellybbq.com/menu",
    "Printed 'Chef's Choice for 2' price on the official menu",
    "80 as printed",
)

setp(
    "stubborn-seed",
    "$320-$390++ (tasting menu, two guests)",
    "Official Stubborn Seed tasting-menu PDF hosted by rwlasvegas.com: Tasting Menu $160 per person; Elevated "
    "Tasting +$35 per person. Two adults = $320 / $390 before tax and gratuity. Wine pairing $60 / $70 per "
    "person. An a-la-carte menu is published on the same page.",
    "https://www.rwlasvegas.com/pdf/stubborn-seed-tasting-menu-11-25-2026/",
    "2 x printed per-person tasting-menu price (official menu PDF)",
    "160x2=320; (160+35)x2=390",
)

setp(
    "esthers-kitchen",
    "$112-$196 (dinner for two, a la carte)",
    "Official Esther's Kitchen menus page (estherslv.com/menus): dinner a la carte printed - starters $15-$32, "
    "pasta $25-$41, entrees $34-$98, desserts $13-$18, sourdough bread service $12 (one) / $19 (three) / $25 "
    "(five). Two guests sharing a starter, two pastas and a dessert lands about $112-$196 before tax and "
    "gratuity. The official menu has no prix-fixe or tasting option.",
    "https://www.estherslv.com/menus/",
    "Arithmetic over printed a-la-carte dinner prices (official menu)",
    "low: 15 + 25 + 27 + 13 + 32 = 112; high: 32 + 41 + 38 + 17 + 68 = 196 (indicative, dish choice varies)",
)

# ---- hours / days / exceptions verified 2026-11-27 ----
sethour(
    "wing-lei",
    "Thu, Sun, Mon; Fri-Sat; closed Tue-Wed",
    "5:30 PM - 9:30 PM (Fri-Sat until 10:00 PM)",
    "Closed Tuesday and Wednesday. Dress code business casual; children under 5 not permitted.",
    "https://www.wynnlasvegas.com/dining/fine-dining/wing-lei",
)
sethour(
    "stubborn-seed",
    "Daily",
    "Dining room 5:00 PM - 10:00 PM; bar & lounge 4:00 PM - 10:00 PM",
    "Located in The District at Resorts World. No published closure days.",
    "https://www.rwlasvegas.com/dining/stubborn-seed/",
)
sethour(
    "mott-32",
    "Daily",
    "Lunch 11:00 AM - 2:30 PM (Sat-Sun brunch from 10:30 AM); dinner 5:00 PM - 10:00 PM",
    "Brunch Sat-Sun from 10:30 AM. On The Palazzo casino floor.",
    "https://www.venetianlasvegas.com/dining/restaurants/mott-32.html",
)
sethour(
    "bouchon",
    "Daily",
    "Dinner 5:00 PM - 10:00 PM; brunch Thu 8:00 AM - 1:00 PM, Fri-Sun 8:00 AM - 2:00 PM",
    "Thanksgiving 2026: 1:00 PM - 8:00 PM, no brunch service. Confirm 2027 holiday service before booking.",
    "https://www.venetianlasvegas.com/dining/restaurants/bouchon.html",
)
sethour(
    "gymkhana",
    "Daily",
    "Mon-Thu 5:00 PM - 10:00 PM; Fri-Sat 5:00 PM - 10:30 PM; Sun 5:00 PM - 10:00 PM",
    "Business casual dress code enforced (no tank tops, swimwear or open-toe shoes). Children 6+ only; under "
    "21 not admitted to the lounge after 10 PM.",
    "https://aria.mgmresorts.com/en/restaurants/gymkhana.html",
)
sethour(
    "e-by-jose-andres",
    "Tue-Sat",
    "5:30 PM - 8:30 PM",
    "Closed Sunday and Monday. Only two seatings nightly; reservations open up to three months in advance. "
    "Dress code upscale.",
    "https://cosmopolitanlasvegas.mgmresorts.com/en/restaurants/e-by-jose-andres.html",
)
sethour(
    "lamaii",
    "Daily",
    "Mon-Wed 11:00 AM - 12:00 AM; Thu-Sun 11:00 AM - 2:00 AM",
    "Chinatown room at 4480 Spring Mountain Rd #700. The MICHELIN Guide 2026 selection applies to this location.",
    "https://www.lamaiilv.com/chinatown/",
)
sethour(
    "soulbelly-bbq",
    "Tue-Sun",
    "Tue-Thu 11:00 AM - 9:00 PM; Fri-Sat 11:00 AM - 10:00 PM; Sun 11:00 AM - 9:00 PM",
    "Closed Monday. Happy hour Tue-Fri 2-5 PM; reverse happy hour Fri-Sat 9-10 PM. MICHELIN recognition "
    "applies to the Main Street location only.",
    "https://soulbellybbq.com/",
)
sethour(
    "pho-ga-bac-bac",
    "Daily",
    "Open 24 hours",
    "Open 24 hours with a full bar. Reservation requests are reviewed but not guaranteed.",
    "https://bestchickenpho.com/",
)

# ---- Instagram handles: each profile was fetched 2026-11-27 and matched to the venue ----
SOC = {
    "joel-robuchon": ("https://www.instagram.com/joelrobuchon.lasvegas/",
                       "https://www.instagram.com/joelrobuchon.lasvegas/"),
    "latelier-robuchon": ("https://www.instagram.com/joelrobuchon.lasvegas/",
                          "https://www.instagram.com/joelrobuchon.lasvegas/"),
    "guy-savoy": ("https://www.instagram.com/guysavoylasvegas/",
                  "https://www.instagram.com/guysavoylasvegas/"),
    "e-by-jose-andres": ("https://www.instagram.com/ebyjoseandres/",
                         "https://www.instagram.com/ebyjoseandres/"),
    "china-poblano": ("https://www.instagram.com/chinapoblano/",
                      "https://www.instagram.com/chinapoblano/"),
    "cote": ("https://www.instagram.com/cotekoreansteakhouse/",
             "https://www.instagram.com/cotekoreansteakhouse/"),
    "estiatorio-milos": ("https://www.instagram.com/estiatoriomilos/",
                         "https://www.instagram.com/estiatoriomilos/"),
    "gymkhana": ("https://www.instagram.com/gymkhanalasvegas/",
                 "https://aria.mgmresorts.com/en/restaurants/gymkhana.html"),
    "anima-by-edo": ("https://www.instagram.com/animabyedo",
                     "https://animabyedo.com/"),
    "kabuto": ("https://www.instagram.com/kabutolv/",
               "https://www.instagram.com/kabutolv/"),
    "kame-omakase": ("https://www.instagram.com/kameomakase/",
                     "https://www.instagram.com/kameomakase/"),
    "lamaii": ("https://www.instagram.com/lamaiilv/",
               "https://www.instagram.com/lamaiilv/"),
    "sparrow-and-wolf": ("https://www.instagram.com/sparrowandwolflv/",
                         "https://www.instagram.com/sparrowandwolflv/"),
    "esthers-kitchen": ("https://www.instagram.com/estherskitchenlv/",
                        "https://www.instagram.com/estherskitchenlv/"),
    "soulbelly-bbq": ("https://www.instagram.com/soulbellybbqlv",
                      "https://soulbellybbq.com/"),
    "mott-32": ("https://www.instagram.com/mott32vegas/",
                "https://www.instagram.com/mott32vegas/"),
}
for rid, (ig, src) in SOC.items():
    r = R[rid]
    r["instagram"] = ig
    r["social_source"] = src
    r["social_checked"] = CHECKED

d["meta"]["social_rule"] = (
    "A handle is published only after this session fetched the Instagram profile itself and it matched the "
    "venue (bio names the restaurant, or the venue's own website links to it). Decoys were rejected: "
    "@stubbornseedvegas (7 followers), @pingpangpong (a private personal account), @phogabacbac (1 follower). "
    "Blank means no official handle was verified — never guessed. See FLAGS.md F-19."
)
d["meta"]["price_rule"] = (
    "price_2adults is ONLY filled where the venue's own page or its own hosted menu PDF stated a per-person or "
    "for-two price on 2026-11-27, or where a defensible range can be computed from prices the venue prints "
    "(the arithmetic is stored in price_calc). Blank = not verified. '++' means plus tax and gratuity, as "
    "printed by the venue."
)
d["meta"]["verified_2026_11_27"] = {
    "session": "arena/c7c75f9a-vegas1 (T17)",
    "checked": CHECKED,
    "what": "Couple-price pass (9 venues filled from official menus), hours re-confirmation (9 venues), and "
            "Instagram verification (16 venue rows).",
    "price_sources": "Each row carries price_source. Values were read, not inferred.",
}

json.dump(d, open(P, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
open(P, "a", encoding="utf-8").write("\n")

print("prices filled:", sum(1 for r in d["restaurants"] if r.get("price_2adults")))
print("instagram filled:", sum(1 for r in d["restaurants"] if r.get("instagram")))
print("hours filled:", sum(1 for r in d["restaurants"] if r.get("hours")))
