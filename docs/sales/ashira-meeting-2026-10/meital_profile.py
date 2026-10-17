# -*- coding: utf-8 -*-
"""HAD-543 (Ben, 17.10.2026): add Meital's engineering degrees to her pages. Targeted string inserts only, nothing else touched.
  page 7644 /brokers/meital-katzir/      (her site, Hebrew, the "about" first paragraph)
  page 7804 /en/brokers/meital-katzir/   (her site, English, the "about" first paragraph)
  post 7833 /professionals/meital-katzir/ (her card in the professionals directory, the description)
python meital_profile.py [--apply]   (without --apply: shows what would change). Raw HTML before/after saved next to it."""
import os
import sys
import time
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
src = open(os.path.join(REPO, "scripts", "skin-a", "deployskin.py"), encoding="utf-8").read()
ns = {"__name__": "mprof"}
exec(compile(src[:src.index('s, h, _ = req("GET", "/wp-json/nadlan/v1/health")')], "deployskin-helpers", "exec"), ns)
req = ns["req"]
HE = "אני מהנדסת אזרחית (B.Tech) ומהנדסת בטיחות (B.Sc), ולכן כשקונה שואל על בנייה, מפרט או בטיחות, הוא מקבל תשובה של מהנדסת."
EN = "I am a civil engineer (B.Tech) and a safety engineer (B.Sc), so when a buyer asks about construction, specifications or safety, the answer comes from an engineer."
CARD = "מהנדסת אזרחית (B.Tech) ומהנדסת בטיחות (B.Sc)."
JOBS = [
    ("pages", 7644, "/brokers/meital-katzir/", "ואת השוק שלהם אני קוראת כל יום.", " " + HE),
    ("pages", 7804, "/en/brokers/meital-katzir/", None, " " + EN),
    ("nadlan_professional", 7833, "/professionals/meital-katzir/", "ותמונה שלמה לקונה לפני הסיור.", " " + CARD),
]
apply = "--apply" in sys.argv


def raw(path):
    r = urllib.request.urlopen(urllib.request.Request("https://nad-lan.co.il" + path + "?nlv=%d" % time.time(), headers={"User-Agent": "Mozilla/5.0 Chrome/128"}), timeout=90)
    return r.read().decode("utf-8", "replace")


for typ, pid, path, anchor, add in JOBS:
    s, d, _ = req("GET", f"/wp-json/wp/v2/{typ}/{pid}?context=edit")
    c = d["content"]["raw"]
    if add.strip() in c:
        print("ALREADY", path); continue
    if anchor is None:  # English: the first sentence of the about block that ends with "every day."
        import re
        m = re.search(r"read (?:their|its) market every day\.|every day\.", c)
        anchor = m.group(0) if m else None
    if not anchor or c.count(anchor) != 1:
        print("ANCHOR NOT UNIQUE/NOT FOUND", path, anchor, c.count(anchor) if anchor else 0); continue
    new = c.replace(anchor, anchor + add, 1)
    print("WILL CHANGE", path, "| +", len(new) - len(c), "chars after:", anchor[-40:])
    if apply:
        open(os.path.join(HERE, f"before-{pid}.html"), "w", encoding="utf-8").write(raw(path))
        s2, r2, _ = req("POST", f"/wp-json/wp/v2/{typ}/{pid}", {"content": new})
        print("  saved", s2)
        time.sleep(2)
        after = raw(path)
        open(os.path.join(HERE, f"after-{pid}.html"), "w", encoding="utf-8").write(after)
        print("  live has the line:", add.strip()[:30] in after, "| h1 count:", after.count("<h1"))
