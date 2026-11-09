# -*- coding: utf-8 -*-
"""HAD-689 follow-up to 1.72.625 (Ben 9.11, "כן, תתחיל"): the <title> and H1 changed in code, but the front page (page 4988) still
stores the old Yoast title, which feeds og:title and Yoast's WebPage schema name ("נדלן - דירות למכירה, פרויקטים חדשים ומחירי
דירות בישראל"). Set the stored Yoast title to the new one and the page's own title to the new H1, so every surface says the same.
Backup before, read-back after. python had689_home_yoast_title.py [--go]"""
import io, json, os, sys, time
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(HERE))
src = open(os.path.join(REPO, "scripts", "skin-a", "deployskin.py"), encoding="utf-8").read(); ns = {"__name__": "rt"}
exec(compile(src[:src.index('s, h, _ = req("GET", "/wp-json/nadlan/v1/health")')], "h", "exec"), ns); req = ns["req"]
GO = "--go" in sys.argv
PID = 4988
NEW_SEO = "נדלן - מידע נדל״ן בישראל: עסקאות, מחירים ופרויקטים"
NEW_TITLE = "מידע נדל״ן בישראל"
OLD_SEO = "נדלן - דירות למכירה, פרויקטים חדשים ומחירי דירות בישראל"
s, g, _ = req("GET", "/wp-json/wp/v2/pages/%d?context=edit&_fields=id,link,title,meta" % PID); assert s == 200, s
assert g["link"].rstrip("/") == "https://nad-lan.co.il", g["link"]
cur = (g.get("meta") or {}).get("_yoast_wpseo_title")
print("[now] title=%s | yoast title=%s" % (g["title"]["raw"], cur))
assert cur == OLD_SEO, "the stored Yoast title is not the one expected: read it by hand"
if not GO:
    print("[plan] yoast title -> %s | page title -> %s" % (NEW_SEO, NEW_TITLE)); sys.exit(0)
stamp = time.strftime("%Y%m%dT%H%M%S")
bk = os.path.join(REPO, "docs", "qa", "had689-2026-11-09", "home-4988-before-%s.json" % stamp)
io.open(bk, "w", encoding="utf-8").write(json.dumps({"id": PID, "title": g["title"]["raw"], "meta": g.get("meta")}, ensure_ascii=False))
s1, _, _ = req("POST", "/wp-json/wp/v2/pages/%d" % PID, {"title": NEW_TITLE, "meta": {"_yoast_wpseo_title": NEW_SEO}}); assert s1 in (200, 201), s1
s, r, _ = req("GET", "/wp-json/wp/v2/pages/%d?context=edit&_fields=title,meta" % PID)
assert r["title"]["raw"] == NEW_TITLE and r["meta"]["_yoast_wpseo_title"] == NEW_SEO, "read-back"
print("[done] page 4988 title and Yoast title written and read back; backup", os.path.basename(bk))
