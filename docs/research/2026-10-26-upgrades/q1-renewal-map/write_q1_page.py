# -*- coding: utf-8 -*-
"""Q1 /urban-renewal/map/ (page 5471) page content after release 1.72.520 (the data block): the H1 with the searched phrase "מפת התחדשות
עירונית" (it was nowhere on the page), an answer paragraph with the official counts and their dates, two CTAs, the Yoast title.
Numbers: data.gov.il file 970 complexes / 76 cities (15.8.2026); the authority map 999 / 79 (20.10.2026). Keeps the shortcode and the
building-check line.   python docs/research/2026-10-26-upgrades/q1-renewal-map/write_q1_page.py [--dry]"""
import io, os, re, sys, time, urllib.request
H = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(H))))
src = open(os.path.join(REPO, "scripts", "skin-a", "deployskin.py"), encoding="utf-8").read(); ns = {"__name__": "q1p"}
exec(compile(src[:src.index('s, h, _ = req("GET", "/wp-json/nadlan/v1/health")')], "h", "exec"), ns)
req = ns["req"]; DRY = "--dry" in sys.argv
if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")
PID = 5471
TITLE = "מפת התחדשות עירונית: מתחמי פינוי בינוי לפי עיר ושלב | נדלן"
DESC = "מפת התחדשות עירונית: 970 מתחמי פינוי בינוי ב-76 ערים בקובץ הרשמי ו-999 במפת הרשות, לפי שלב, מחוז ועיר, עם דירות היום ואחרי הבנייה."
NEW = ("<h1 class=\"nlur-h1\">מפת התחדשות עירונית: מתחמים ופרויקטים של פינוי בינוי בכל עיר</h1>\n"
       "<p>מפת התחדשות עירונית של נדלן מציגה את מתחמי הפינוי בינוי שהרשות הממשלתית להתחדשות עירונית מפרסמת: 970 מתחמים ב-76 ערים בקובץ "
       "הרשמי (15.8.2026), ו-999 מתחמים ב-79 ערים במפת הרשות (20.10.2026). לכל שלב, לכל מחוז ולכל עיר יש כאן טבלה: כמה מתחמים מאושרים "
       "ובביצוע, כמה דירות יש היום וכמה יהיו אחרי הבנייה.</p>\n"
       "<p class=\"nlur-cta\"><a class=\"btn\" href=\"#nlurm-map\">חפשו את העיר שלכם במפה</a> <a class=\"btn secondary\" href=\"/urban-renewal/check/\">בדיקת בניין חינמית</a></p>\n"
       "[nadlan_ur_map]\n"
       "<p>לא בטוחים אם הבניין שלכם במתחם? <a href=\"/urban-renewal/check/\">בדיקת התחדשות לבניין שלי</a>.</p>")
print("[page %d] title %d chars, desc %d chars" % (PID, len(TITLE), len(DESC)))
if DRY:
    sys.exit(0)
s, r, _ = req("GET", "/wp-json/wp/v2/pages/%d?context=edit&_fields=content,link,meta" % PID)
assert "[nadlan_ur_map]" in r["content"]["raw"]
bk = os.path.join(H, "page-backup"); os.makedirs(bk, exist_ok=True)
io.open(os.path.join(bk, "page-%d-%s.html" % (PID, time.strftime("%Y%m%d-%H%M%S"))), "w", encoding="utf-8", newline="").write(r["content"]["raw"] + "\n<!-- meta " + repr(r["meta"].get("_yoast_wpseo_title")) + " -->")
req("POST", "/wp-json/wp/v2/pages/%d" % PID, {"content": NEW, "meta": {"_yoast_wpseo_title": TITLE, "_yoast_wpseo_metadesc": DESC}})
back = req("GET", "/wp-json/wp/v2/pages/%d?context=edit&_fields=content" % PID)[1]["content"]["raw"]
time.sleep(3)
page = urllib.request.urlopen(urllib.request.Request(r["link"] + "?x=%d" % time.time(), headers={"User-Agent": "Mozilla/5.0"}), timeout=90).read().decode("utf-8", "replace")
bd = page[page.find("<body"):]
title = re.search(r"<title>(.*?)</title>", page, re.S).group(1).strip()
ok = {"read-back": back == NEW, "one h1": bd.count("<h1") == 1, "phrase in H1": "מפת התחדשות עירונית: מתחמים" in bd, "title": title == TITLE,
      "data block": 'id="nlur2"' in bd, "map": 'id="nlurm-map"' in bd}
for k, v in ok.items(): print("   ", "OK " if v else "BAD", k)
