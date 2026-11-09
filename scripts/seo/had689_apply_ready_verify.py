# -*- coding: utf-8 -*-
"""HAD-689 (Ben 9.11.2026): the 85 immediate / near-occupancy rows of data/projects-market.json (read 25.10) were checked by hand
on 9.11 against developer pages and portals (docs/research/2026-11-09-new-projects-hub/ready-verify/*.json). 11 rows that the
site showed as "אכלוס מיידי" are only near occupancy today; 2 could not be found; 2 are still in marketing; 7 prices moved.
This applies the verified facts to the data file, row by row, with a public delivery wording chosen BY HAND per row (CURATED below,
one line per verified row, in the order of the merged verified list). Nothing is carried over that was not seen on 9.11.
python had689_apply_ready_verify.py [--go]   (dry run prints every change)"""
import io, json, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(HERE))
DATA = os.path.join(REPO, "plugins", "nadlan-config", "data", "projects-market.json")
V = os.path.join(REPO, "docs", "research", "2026-11-09-new-projects-hub", "ready-verify")
GO = "--go" in sys.argv
X = None  # drop the row from the published list (not found on 9.11)
# index in the merged verified list -> (status, public delivery wording). status None = drop.
CURATED = {
    0: ("immediate", "אכלוס מיידי"), 1: (X, ""), 2: ("near_occupancy", "12/2026"), 3: ("immediate", "מאוכלס"),
    4: ("immediate", "מאוכלס"), 5: ("immediate", "אכלוס מיידי"), 6: ("immediate", "אכלוס מיידי"), 7: ("immediate", "אכלוס מיידי"),
    8: ("immediate", "אכלוס מיידי"), 9: ("immediate", "אכלוס מיידי"), 10: ("immediate", "אכלוס מיידי"), 11: ("immediate", "אכלוס מיידי"),
    12: ("near_occupancy", "12/2026"), 13: ("immediate", "אכלוס מיידי"), 14: ("immediate", "אכלוס מיידי"), 15: (X, ""),
    16: ("immediate", "אכלוס מיידי"), 17: ("marketing", "02/2029"), 18: ("immediate", "מתאכלס בימים אלה"), 19: ("immediate", "מאוכלס"),
    20: ("near_occupancy", "רבעון 1, 2027"), 21: ("immediate", "מאוכלס"), 22: ("immediate", "מאוכלס"), 23: ("immediate", "מאוכלס"),
    24: ("immediate", "אכלוס מיידי"), 25: ("immediate", "אכלוס מיידי"), 26: ("near_occupancy", "03/2027"), 27: ("immediate", "מאוכלס"),
    28: ("near_occupancy", ""), 29: ("immediate", "אכלוס מיידי"), 30: ("near_occupancy", "01/2027"), 31: ("immediate", "מאוכלס"),
    32: ("near_occupancy", "שלב א׳ מאוכלס, הבנייה נמשכת"), 33: ("immediate", "מאוכלס"), 34: ("near_occupancy", "12/2026"),
    35: ("immediate", "שלב א׳ עם תעודת גמר"), 36: ("near_occupancy", "07/2026"), 37: ("immediate", "אכלוס מיידי"),
    38: ("near_occupancy", "10/2026"), 39: ("immediate", "מאוכלס"), 40: ("immediate", "אכלוס מיידי"), 41: ("immediate", "אכלוס מיידי"),
    42: ("immediate", "אכלוס מיידי"), 43: ("immediate", "אכלוס מיידי או 08/2029"), 44: ("immediate", "מאוכלס"),
    45: ("immediate", "אכלוס מיידי"), 46: ("near_occupancy", ""), 47: ("immediate", "אכלוס מיידי"), 48: ("near_occupancy", "02/2027"),
    49: ("near_occupancy", "02/2027"), 50: ("near_occupancy", "תוך כשנה"), 51: ("near_occupancy", "מועדים שונים"),
    52: ("immediate", "אכלוס מיידי"), 53: ("near_occupancy", "06/2026"), 54: ("immediate", "אכלוס מיידי"), 55: ("near_occupancy", "04/2027"),
    56: ("immediate", "אכלוס מיידי"), 57: ("immediate", "אכלוס מיידי"), 58: ("immediate", "בניין ראשון 2026, בניין שני 2027"),
    59: ("immediate", "מאוכלס"), 60: ("immediate", "אכלוס מיידי"), 61: ("near_occupancy", "01/2027"), 62: ("immediate", "אכלוס מיידי"),
    63: ("near_occupancy", "02/2027"), 64: ("immediate", "מאוכלס"), 65: ("marketing", ""), 66: ("immediate", "אכלוס מיידי"),
    67: ("immediate", "אכלוס מיידי"), 68: ("immediate", "אכלוס מיידי"), 69: ("near_occupancy", "תוך כחצי שנה"), 70: ("immediate", "אכלוס מיידי"),
    71: ("near_occupancy", ""), 72: ("immediate", "אכלוס מיידי"), 73: ("immediate", "אכלוס מיידי"), 74: ("immediate", "אכלוס מיידי"),
    75: ("near_occupancy", ""), 76: ("immediate", "מאוכלס"), 77: ("immediate", "אכלוס מיידי"), 78: ("immediate", "אכלוס מיידי"),
    79: ("immediate", "מאוכלס"), 80: ("immediate", "אכלוס מיידי"), 81: ("near_occupancy", "רבעון 3, 2026"), 82: ("immediate", "אכלוס מיידי"),
    83: ("near_occupancy", "08/2027"), 84: ("immediate", "אכלוס מיידי"),
}
NO_PRICE = {84}  # Tel Mond: the headline (5.29M) and the text (4.29M for 6 rooms) disagree, so no price is shown
assert len(CURATED) == 85

d = json.load(io.open(DATA, encoding="utf-8"))
a = json.load(io.open(os.path.join(V, "tel-aviv.json"), encoding="utf-8")); b = json.load(io.open(os.path.join(V, "rest-of-country.json"), encoding="utf-8"))
for x in a: x.setdefault("city", "תל אביב-יפו")
ver = a + b
assert len(ver) == 85
n = lambda s: re.sub(r"[^\w]", "", str(s)).lower()
used = {}; rows = d["projects"]
for i, r in enumerate(rows):
    if r["status"] not in ("immediate", "near_occupancy"): continue
    cand = [j for j, v in enumerate(ver) if j not in used.values() and (n(v["name"]) == n(r["name"]) or n(r["name"]) in n(v["name"]) or n(v["name"]) in n(r["name"])) and n(v.get("city", ""))[:4] == n(r["city"])[:4]]
    assert len(cand) == 1, (r["name"], cand)
    used[i] = cand[0]
assert len(used) == 85
out, drop, changes = [], 0, {"status": 0, "price": 0, "delivery": 0}
for i, r in enumerate(rows):
    if i not in used:
        out.append(r); continue
    j = used[i]; v = ver[j]; st, dl = CURATED[j]
    if st is None:
        drop += 1; print("[drop] %s (%s): not found on 9.11" % (r["name"], r["city"])); continue
    new = dict(r)
    if new.get("status") != st: changes["status"] += 1; print("[status] %s: %s -> %s" % (r["name"], r.get("status"), st))
    new["status"] = st
    if dl:
        if new.get("delivery") != dl: changes["delivery"] += 1
        new["delivery"] = dl
    else:
        new.pop("delivery", None)
    p = None if j in NO_PRICE else v.get("price_from")
    p = int(p) if p not in (None, "") else None
    if p != (int(r["price_from"]) if r.get("price_from") else None):
        changes["price"] += 1; print("[price] %s: %s -> %s" % (r["name"], r.get("price_from"), p))
    if p: new["price_from"] = p
    else: new.pop("price_from", None)
    if p and v.get("price_rooms"):
        m = re.match(r"\s*(\d+(?:\.\d)?)", str(v["price_rooms"]))
        if m: new["price_note"] = "ל־%s חדרים" % m.group(1)
    elif "price_note" in new and not p:
        new.pop("price_note")
    new["checked"] = "2026-11-09"
    if v.get("source_url"): new["src_url"] = v["source_url"]
    out.append(new)
st = {}
for r in out: st[r["status"]] = st.get(r["status"], 0) + 1
print("\nrows %d -> %d | dropped %d | status changes %d | price changes %d | delivery wording %d" % (len(rows), len(out), drop, changes["status"], changes["price"], changes["delivery"]))
print("status counts:", st)
if GO:
    d["projects"] = out
    d["ready_checked"] = "2026-11-09"
    d["note"] = str(d.get("note", "")) + " | 9.11.2026: every immediate / near-occupancy row checked by hand against the developer page or the portal listing (HAD-689); unconfirmed rows removed."
    io.open(DATA, "w", encoding="utf-8", newline="\n").write(json.dumps(d, ensure_ascii=False, separators=(",", ":")))
    print("[done] written", DATA)
