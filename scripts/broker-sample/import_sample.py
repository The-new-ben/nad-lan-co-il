# -*- coding: utf-8 -*-
"""Owner order 24.9.2026: "I won't bring in all the brokers now, but a sample from Tel Aviv, from areas with a lot
of money and real transactions; Jerusalem is very active; maybe Eilat."

A reproducible random sample (seed 2409) from the Ministry of Justice brokers register on data.gov.il
(resource a0f56034-88db-4132-8803-854bcdb01ca1, 24,724 active licences: licence number, name, city of residence):
Tel Aviv 50, Jerusalem 30, Herzliya 15, Eilat 10, Kfar Shmaryahu 5, Savyon 5, Caesarea 5 = 120 cards.
Each card: the register name as written, "תיווך נדל״ן", the licence number and the city, source `metavhim` (a register
source, so the licence badge is true), no phone or email (the register has none), claim path = the free-site join.
IndexNow is detached for the import; the cards reach search engines through the sitemap like every other card.

  python scripts/broker-sample/import_sample.py REGISTER.json [--dry]
"""
import io, json, os, random, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "ops"))
from nlbridge import Bridge, backup

REG = sys.argv[1]
DRY = "--dry" in sys.argv
rows = json.load(open(REG, encoding="utf-8"))
PLAN = [  # (label on the site, register spellings, how many)
    ("תל אביב יפו", ("תל אביב - יפו", "תל אביב", "תל אביב יפו", "תל אביב-יפו"), 50),
    ("ירושלים", ("ירושלים",), 30),
    ("הרצליה", ("הרצליה", "הרצליה פיתוח"), 15),
    ("אילת", ("אילת",), 10),
    ("כפר שמריהו", ("כפר שמריהו",), 5),
    ("סביון", ("סביון",), 5),
    ("קיסריה", ("קיסריה",), 5),
]
SKIP = {"3131540"}  # already on the site (Meital Katzir)
rnd = random.Random(2409)
cards = []
for label, spellings, n in PLAN:
    pool = sorted((r for r in rows if str(r["עיר מגורים"]).strip() in spellings and str(r["מס רשיון"]) not in SKIP), key=lambda r: int(r["מס רשיון"]))
    pick = rnd.sample(pool, min(n, len(pool)))
    for r in pick:
        lic = str(r["מס רשיון"]).strip()
        name = " ".join(str(r["שם המתווך"]).split())
        cards.append({"source": "metavhim", "source_id": lic, "title": name, "meta": {
            "profession": "metavech", "license_number": lic, "city": label,
            "claim_status": "unclaimed", "source_url": "https://data.gov.il/dataset/metavhim", "data_quality": "stub"}})
    print(f"{label}: {len(pick)} of {len(pool)} in the register")
print("total cards:", len(cards))
backup("broker-sample-plan", cards)
if DRY:
    for c in cards[:5]:
        print("  ", c["title"], c["meta"]["license_number"], c["meta"]["city"])
    raise SystemExit(0)
with Bridge("brkimport") as b:
    res = []
    for i in range(0, len(cards), 40):
        res += b.ops({"upsert_cards": cards[i:i + 40], "no_indexnow": 1}, timeout=300)["upsert_cards"]
    bad = [r for r in res if r.get("err")]
    print("imported:", len([r for r in res if r.get("id")]), "errors:", bad[:5])
    # Meital first on the professionals hub (admin pin), as the owner asked for the brokers list
    cur = b.ops({"get": {"ids": [7833], "meta": ["is_pinned"]}})["get"]["7833"]["meta"]["is_pinned"]
    if cur["value"] not in ("1",):
        print("pin Meital:", b.ops({"set_meta": [{"id": 7833, "key": "is_pinned", "value": "1", "expect": cur["md5"]}]})["set_meta"])
    print("purge:", b.ops({"purge": 1}).get("purged"))
backup("broker-sample-result", res)
