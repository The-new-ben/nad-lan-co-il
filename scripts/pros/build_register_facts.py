# -*- coding: utf-8 -*-
"""ProNetwork (design system v98, 28.9.2026): the register's business facts for every contractor card, from the public
contractors register (pinkas hakablanim, data.gov.il resource 4eb61bd6-18cf-4e7c-9f9c-e166dfa0a2d8, CKAN datastore).

The owner, 28.9: "professionals still look very basic with this circle and a letter ... a social network".
A card can say, without inventing anything, what the state register says about the business:
  since       the year the contractor was first registered (TAARICH_KABLAN)
  branches    each branch (TEUR_ANAF) with its group and classification (KVUTZA + SIVUG, e.g. ג-5) and scope (HEKEF)
  recognised  'מוכר' for government work when the register says so (KABLAN_MUKAR)
  company     the register's entity is a company (name ends in בע"מ) - a private person's address is never shown
Kept OUT on purpose (privacy): phones, e-mails, street addresses, the employees' names.
Output: scripts/pros/data/register-facts.json  { registry_number: {...} }; the site loads it through a release, never live.
  python scripts/pros/build_register_facts.py"""
import io, json, os, sys, time, urllib.parse, urllib.request
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "data", "register-facts.json")
os.makedirs(os.path.dirname(OUT), exist_ok=True)
RES = "4eb61bd6-18cf-4e7c-9f9c-e166dfa0a2d8"
API = "https://data.gov.il/api/3/action/datastore_search"


def page(offset):
    q = urllib.parse.urlencode({"resource_id": RES, "limit": 5000, "offset": offset,
                                "fields": "MISPAR_KABLAN,SHEM_YESHUT,TAARICH_KABLAN,TEUR_ANAF,KVUTZA,SIVUG,HEKEF,KABLAN_MUKAR,SHEM_YISHUV"})
    for i in range(4):
        try:
            return json.load(urllib.request.urlopen(urllib.request.Request(API + "?" + q, headers={"User-Agent": "NadLan-register/1.0"}), timeout=120))["result"]
        except Exception as e:
            print("retry", offset, str(e)[:80]); time.sleep(5 * (i + 1))
    raise SystemExit("the register did not answer")


def main():
    rows, off = [], 0
    while True:
        r = page(off)
        rows += r["records"]
        off += len(r["records"])
        print("rows", off, "/", r.get("total"))
        if not r["records"] or off >= r.get("total", 0):
            break
    facts = {}
    for x in rows:
        k = str(x.get("MISPAR_KABLAN") or "").strip()
        if not k:
            continue
        f = facts.setdefault(k, {"name": (x.get("SHEM_YESHUT") or "").strip(), "since": None, "branches": [], "recognised": False,
                                 "city": (x.get("SHEM_YISHUV") or "").strip()})
        d = str(x.get("TAARICH_KABLAN") or "")[:4]
        if d.isdigit():
            f["since"] = min(int(d), f["since"] or 9999)
        br = (x.get("TEUR_ANAF") or "").strip()
        cls = ((x.get("KVUTZA") or "").strip() + "-" + str(x.get("SIVUG") or "").strip()).strip("-")
        if br and not any(b["b"] == br for b in f["branches"]):
            f["branches"].append({"b": br, "c": cls, "s": (x.get("HEKEF") or "").strip()})
        if str(x.get("KABLAN_MUKAR") or "").strip().startswith("מוכר"):  # "לא מוכר" also holds the word
            f["recognised"] = True
    for f in facts.values():
        f["company"] = bool(__import__("re").search(r"בע[\"״]?מ|בעמ$", f["name"]))
    io.open(OUT, "w", encoding="utf-8").write(json.dumps({"source": "פנקס הקבלנים הרשומים, data.gov.il, " + time.strftime("%d.%m.%Y"),
                                                          "resource": RES, "facts": facts}, ensure_ascii=False))
    print("contractors", len(facts), "bytes", os.path.getsize(OUT))


if __name__ == "__main__":
    main()
