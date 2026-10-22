# -*- coding: utf-8 -*-
"""Build the data of the registered-contractor check (HAD-592, /pinkas-hakablanim/, 22.10.2026).

Input (kept out of the public repo, it carries individuals' phones and emails):
  _private-research/2026-10-22-contractor-register/raw/register.json      the full register from the data.gov.il datastore API
  _private-research/2026-10-22-contractor-register/raw/nadlan-professionals.json   our profiles (public REST), for the profile link
Output:
  plugins/nadlan-config/data/pinkas-register.php      every contractor for the server search: number, name, company number,
      city, first year, recognised level, our profile slug, and per branch: code, group, level, restriction text. NO phone,
      email, street or staff names. The file starts with "<?php exit; ?>" so a direct request returns nothing.
  plugins/nadlan-config/assets/instruments/data/pinkas-meta.json   the small public part the page loads: the classification
      table in force, the thresholds, the branches, the cities, the counts.
The money table is NOT the dataset's HEKEF column (one period old); it is the official table in force from 1.10.2026
(gov.il/he/pages/sivug_kablanim, updated 6.10.2026), next change 1.4.2027.

  python tools/instruments/build_pinkas.py [--raw <folder>]"""
import ast, collections, io, json, os, re, sys

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
RAW = next((a.split("=", 1)[1] for a in sys.argv if a.startswith("--raw=")),
           os.path.join(os.path.dirname(REPO), "_private-research", "2026-10-22-contractor-register", "raw"))
PLUG = os.path.join(REPO, "plugins", "nadlan-config")

TABLE = {"from": "2026-10-01", "to": "2027-04-01", "src": "https://www.gov.il/he/pages/sivug_kablanim", "updated": "2026-10-06",
         "א": {"ק": 846, "1": 1994, "2": 3988, "3": 7977, "4": 15954, "5": 0},
         "ב": {"1": 3267, "2": 6533, "3": 13066, "4": 26131, "5": 0},
         "ג": {"1": 5458, "2": 9627, "3": 19255, "4": 38508, "5": 0},
         "sqm": {"1": 2000, "2": 3000, "3": 5000, "4": 10000, "5": 0}}  # thousand NIS per one site before VAT; 0 = unlimited
THR = {"main": 103250, "sub": 54000, "src": "https://www.gov.il/he/pages/general_information_for_registration_of_contractors", "updated": "2026-02-24"}
FINAL = str.maketrans("ךםןףץ", "כמנפצ")


def norm(s):
    s = (s or "").replace('בע"מ', " ").replace("בע״מ", " ").replace("בעמ", " ")
    s = re.sub(r"[\"'״׳`.,()\-–_/\\]", " ", s).translate(FINAL).lower()
    return re.sub(r"\s+", " ", s).strip()


def city_name(s):
    return re.sub(r"\s+", " ", re.sub(r"\s*-\s*", "-", (s or "").strip()))


def main():
    reg = json.load(io.open(os.path.join(RAW, "register.json"), encoding="utf-8"))
    rec, asof = reg["records"], "2026-08-17"
    pro = json.load(io.open(os.path.join(RAW, "nadlan-professionals.json"), encoding="utf-8"))["items"]
    slug = {}
    for p in pro:
        m = p["meta"] if isinstance(p["meta"], dict) else ast.literal_eval(p["meta"])
        if m.get("profession") == "kablan" and m.get("registry_number") and m.get("source") != "demo_seed":
            slug[str(m["registry_number"]).strip()] = p["slug"]
    by = collections.OrderedDict()
    for r in rec:
        by.setdefault(r["MISPAR_KABLAN"].strip(), []).append(r)
    cities = collections.Counter(city_name(rs[0]["SHEM_YISHUV"]) for rs in by.values())
    city_list = [c for c, _ in cities.most_common()]
    cidx = {c: i for i, c in enumerate(city_list)}
    bname, bgroup, bcount = {}, {}, collections.Counter()
    rows = []
    for n, rs in by.items():
        r0 = rs[0]
        br, muk = [], 0
        for r in rs:
            t = r["TEUR_ANAF"]
            name, _, restr = t.partition(" - ")
            code = int(r["KOD_ANAF"])
            bname.setdefault(code, re.sub(r"\s+", " ", name).strip()); bgroup.setdefault(code, r["KVUTZA"]); bcount[code] += 1
            br.append([code, r["KVUTZA"], r["SIVUG"], restr.strip()])
            m = re.search(r"מוכר בסיווג (\d)", r["KABLAN_MUKAR"] or "")
            if m: muk = max(muk, int(m.group(1)))
        yr = int((r0["TAARICH_KABLAN"] or "0")[:4] or 0)
        rows.append([int(n), r0["SHEM_YESHUT"].strip(), (r0["MISPAR_YESHUT"] or "").strip(), cidx[city_name(r0["SHEM_YISHUV"])], yr, muk,
                     slug.get(n, ""), br, norm(r0["SHEM_YESHUT"])])
    rows.sort(key=lambda x: x[0])
    data = {"asof": asof, "n": len(rows), "cities": city_list, "rows": rows}
    out = os.path.join(PLUG, "data", "pinkas-register.php")
    with io.open(out, "w", encoding="utf-8", newline="\n") as f:
        f.write("<?php exit; ?>\n")
        f.write(json.dumps(data, ensure_ascii=False, separators=(",", ":")))
    years = collections.Counter(x[4] for x in rows)
    meta = {"key": "pk", "asof": asof, "table": TABLE, "thr": THR,
            "branches": [[c, bname[c], bgroup[c], bcount[c]] for c in sorted(bname)],
            "cities": [[c, cities[c]] for c in city_list],
            "stats": {"contractors": len(rows), "companies": sum(1 for x in rows if x[2]), "cities": len(city_list), "branches": len(bname),
                      "rows": len(rec), "recognised": sum(1 for x in rows if x[5]), "restricted": sum(1 for x in rows if any(b[3] for b in x[7])),
                      "with_page": sum(1 for x in rows if x[6])},
            "years": {str(y): years[y] for y in range(2015, 2027)}}
    io.open(os.path.join(PLUG, "assets", "instruments", "data", "pinkas-meta.json"), "w", encoding="utf-8", newline="\n").write(
        json.dumps(meta, ensure_ascii=False, separators=(",", ":")))
    print("contractors", len(rows), "| with our page", meta["stats"]["with_page"], "| restricted", meta["stats"]["restricted"],
          "| register file", os.path.getsize(out), "bytes | meta", len(json.dumps(meta, ensure_ascii=False)), "bytes")


if __name__ == "__main__":
    main()
