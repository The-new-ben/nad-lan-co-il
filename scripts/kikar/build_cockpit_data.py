# -*- coding: utf-8 -*-
"""Builds plugins/nadlan-config/assets/project-stage/hamedina/cockpit.json, the data of the apartment cockpit (HAD-699,
10.11.2026). Every number comes from a file in the repo with its source, and the file is read here, not typed:
  - the deals: the three published deals of inc/project-stage.php ('hamedina' => 'deals'), Globes;
  - purchase tax: the 2026 brackets, frozen to 15.1.2028 (docs/research/2026-10-26-upgrades/g4-purchase-tax/coverage-facts-g4.json);
  - arnona: Tel Aviv-Yafo's 2026 order, zone 1, building type אא (docs/research/2026-10-21-kikar-tools/arnona/arnona.md);
  - the mortgage rate: the Bank of Israel average, fixed non-indexed (plugins/nadlan-config/assets/instruments/data/boi-mortgage.json);
  - the views: the rendered window views that exist (assets/project-stage/hamedina/tour/ and, when rendered, views/).
  python scripts/kikar/build_cockpit_data.py
"""
import datetime
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
PLUG = os.path.join(REPO, "plugins", "nadlan-config")
HAM = os.path.join(PLUG, "assets", "project-stage", "hamedina")
OUT = os.path.join(HAM, "cockpit.json")

php = open(os.path.join(PLUG, "inc", "project-stage.php"), encoding="utf-8").read()
blk = php[php.index("'hamedina' => array("):]
blk = blk[blk.index("'deals'          => array("):blk.index("'deals_sum'")]
deals = []
for m in re.finditer(r"array\( 'floor' => '(\d+)'.*?'apt' => '([^']+)', 'price' => '([\d.]+) מיליון ₪', 'psqm' => '([^']+)', 'date' => '([^']+)', 'src' => '([^']+)', 'url' => '([^']+)'", blk):
    deals.append({"floor": int(m.group(1)), "apt": m.group(2), "price": round(float(m.group(3)) * 1e6), "psqm": m.group(4),
                  "date": m.group(5), "src": m.group(6), "url": m.group(7)})
assert len(deals) == 3, deals

g4 = json.dumps(json.load(open(os.path.join(REPO, "docs", "research", "2026-10-26-upgrades", "g4-purchase-tax", "coverage-facts-g4.json"), encoding="utf-8")), ensure_ascii=False)
for need in ("1,?978,?745", "6,?055,?070", "15\\\\.1\\\\.2028"):
    assert re.search(need, g4) or need in g4, "purchase-tax facts file lacks " + need

arn = open(os.path.join(REPO, "docs", "research", "2026-10-21-kikar-tools", "arnona", "arnona.md"), encoding="utf-8").read()
row = re.search(r"^\| אא \| ([\d.]+) \| ([\d.]+) \|", arn, re.M)
assert row and "## Kikar HaMedina: zone 1" in arn
boi = json.load(open(os.path.join(PLUG, "assets", "instruments", "data", "boi-mortgage.json"), encoding="utf-8"))
fx = boi["rates"]["fixed_nl"]

tour = os.path.join(HAM, "tour")
views = []
for fl, b in ((20, 278.11), (30, 265.61), (38, 255.61)):
    f = "twist-c%dw-day-card.webp" % fl
    if os.path.exists(os.path.join(tour, f)):
        views.append({"tower": "C", "floor": fl, "bearing": b, "tod": "day", "img": "tour/" + f, "src": "Blender Cycles"})
extra = [{"tower": "C", "floor": 30, "bearing": 265.61, "tod": "sunset", "img": "tour/balcony-c30w-sunset-card.webp", "what": "balcony"},
         {"tower": "C", "floor": 30, "bearing": 265.61, "tod": "evening", "img": "tour/living-c30w-evening-card.webp", "what": "living"}]
views += [x for x in extra if os.path.exists(os.path.join(HAM, x["img"]))]
vj = os.path.join(HAM, "views", "views.json")
sj = os.path.join(HAM, "views", "sun.json")
SUN = json.load(open(sj, encoding="utf-8")) if os.path.exists(sj) else {}
if os.path.exists(vj):
    for k, v in json.load(open(vj, encoding="utf-8")).items():
        if os.path.exists(os.path.join(HAM, "views", k + "-640.webp")):
            m = re.search(r"faces ([\d.]+)", " ".join(v.get("info") or []))  # the APARTMENT line Blender printed: the true facing
            views.append({"tower": v["tower"], "floor": v["floor"], "side": v["side"], "bearing": float(m.group(1)) if m else None, "tod": "day",
                          "img": "views/" + k + "-640.webp", "big": "views/" + k + ".webp"})

data = {
    "v": 1,
    "built": datetime.date.today().isoformat(),
    "deals": deals,
    "sums": {"towers_psqm": "כ-65,000 ₪", "area_psqm": "63,000 עד 66,000 ₪"},
    "tax": {"only": [[1978745, 0], [2347040, 0.035], [6055070, 0.05], [20183565, 0.08], [None, 0.10]],
            "additional": [[6055070, 0.08], [None, 0.10]], "asof": "מדרגות 2026, בתוקף עד 15.1.2028"},
    "arnona": {"zone": 1, "type": "אא", "le140": float(row.group(2)), "gt140": float(row.group(1)), "asof": "צו הארנונה של תל אביב-יפו לשנת 2026"},
    "mortgage": {"rate": fx["rate"], "label": fx["label"], "month": fx["hist"][-1][0], "src": "בנק ישראל"},
    # the towers' maintenance fees: Maariv, "5,000 שקל בחודש רק לוועד בית: תג המחיר החדש של פרויקט סמל הסטטוס התל אביבי" (read 10.11.2026)
    "fee": {"lo": 4000, "hi": 5000, "src": "מעריב", "url": "https://www.maariv.co.il/news/politics/article-1375393",
            "note": "דמי התחזוקה בפרויקט, כ-4,000 עד 5,000 ₪ לדירה לפי השטח"},
    "defaults": {"price": min(d["price"] for d in deals), "size": 140, "share": 50, "years": 25, "fee": 4500},
    "views": views,
    "plan": "plan-floor30-towerC.webp" if os.path.exists(os.path.join(HAM, "plan-floor30-towerC.webp")) else None,
}
json.dump(data, open(OUT, "w", encoding="utf-8", newline="\n"), ensure_ascii=False, separators=(",", ":"))
print("wrote", OUT, os.path.getsize(OUT), "bytes;", len(deals), "deals,", len(views), "views; arnona", data["arnona"]["le140"], data["arnona"]["gt140"], "; rate", fx["rate"])
