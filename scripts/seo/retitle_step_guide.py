# -*- coding: utf-8 -*-
"""Ben, 7.11.2026 night: the step-by-step guide (page 572, /buying-apartment/buying-apartment-step-by-step/) must not compete with
the owner of "קניית דירה" (/buying-apartment/, page 9). New head: "איך כדאי לקנות דירה". The head term leaves the guide's title, H1,
meta title, meta description, focus phrase, Article headline and the four body places that opened sentences with it. Links that
point TO the owner keep the anchor "קניית דירה" (that helps the owner). On the owner page, the anchor to the guide changes too.
The slug stays (no-redirect law). Backup before, read-back after.
python retitle_step_guide.py [--go]"""
import io, json, os, sys, time
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(HERE))
src = open(os.path.join(REPO, "scripts", "skin-a", "deployskin.py"), encoding="utf-8").read(); ns = {"__name__": "rt"}
exec(compile(src[:src.index('s, h, _ = req("GET", "/wp-json/nadlan/v1/health")')], "h", "exec"), ns); req = ns["req"]
GO = "--go" in sys.argv
NEW_H1 = "איך כדאי לקנות דירה: 7 שלבים מהתקציב ועד הטאבו"
META = {"_yoast_wpseo_title": "איך כדאי לקנות דירה: 7 שלבים מהתקציב ועד הטאבו | nad-lan",
        "_yoast_wpseo_metadesc": "איך כדאי לקנות דירה, שלב אחר שלב: תקציב, אישור עקרוני למשכנתא, בדיקות טאבו ותכנון, חוזה מכר, הערת אזהרה ורישום בטאבו.",
        "_yoast_wpseo_focuskw": "איך כדאי לקנות דירה"}
SWAP_572 = [  # (old, new, expected count)
    ('"headline":"קניית דירה שלב אחר שלב 2026:', '"headline":"איך כדאי לקנות דירה 2026:', 1),
    ('<p dir="rtl">קניית דירה מתחילה הרבה לפני החיפוש', '<p dir="rtl">רכישה נכונה מתחילה הרבה לפני החיפוש', 1),
    ("קבוע. קניית דירה היא החלטה ארוכת טווח", "קבוע. דירה היא החלטה ארוכת טווח", 1),
    ("מה השלב הראשון בקניית דירה?", "מה השלב הראשון כשקונים דירה?", None),  # visible FAQ (+ schema if present)
]
SWAP_9 = [('color:#0a6">קניית דירה שלב אחר שלב</a>', 'color:#0a6">איך כדאי לקנות דירה, שלב אחר שלב</a>', 1)]


def apply(raw, swaps):
    for old, new, n in swaps:
        c = raw.count(old)
        assert c >= 1 and (n is None or c == n), ("anchor count", old, c)
        raw = raw.replace(old, new)
    return raw


s, g, _ = req("GET", "/wp-json/wp/v2/pages/572?context=edit&_fields=title,meta,content,link"); assert s == 200, s
s9, g9, _ = req("GET", "/wp-json/wp/v2/pages/9?context=edit&_fields=content"); assert s9 == 200, s9
new572 = apply(g["content"]["raw"], SWAP_572); new9 = apply(g9["content"]["raw"], SWAP_9)
left = new572.count("קניית דירה")
print("[plan] 572 H1: %s -> %s" % (g["title"]["raw"], NEW_H1))
for k, v in META.items(): print("[plan] 572 %s: %s -> %s" % (k[13:], (g.get("meta") or {}).get(k), v))
print("[plan] 572 body: 'קניית דירה' left %d (links to the owner only); page 9 anchor to the guide swapped" % left)
if not GO: sys.exit(0)
bk = os.path.join(REPO, "docs", "qa", "retitle-2026-11-07"); os.makedirs(bk, exist_ok=True)
stamp = time.strftime("%Y%m%dT%H%M%S")
io.open(os.path.join(bk, "backup-%s.json" % stamp), "w", encoding="utf-8").write(json.dumps(
    {"572": {"title": g["title"]["raw"], "meta": {k: (g.get("meta") or {}).get(k) for k in META}, "content": g["content"]["raw"]},
     "9": {"content": g9["content"]["raw"]}}, ensure_ascii=False))
s1, _, _ = req("POST", "/wp-json/wp/v2/pages/572", {"title": NEW_H1, "meta": META, "content": new572}); assert s1 in (200, 201), s1
s2, _, _ = req("POST", "/wp-json/wp/v2/pages/9", {"content": new9}); assert s2 in (200, 201), s2
s, r, _ = req("GET", "/wp-json/wp/v2/pages/572?context=edit&_fields=title,meta,content")
assert r["title"]["raw"] == NEW_H1 and all((r.get("meta") or {}).get(k) == v for k, v in META.items()) and r["content"]["raw"] == new572, "read-back 572"
s, r9, _ = req("GET", "/wp-json/wp/v2/pages/9?context=edit&_fields=content"); assert r9["content"]["raw"] == new9, "read-back 9"
print("[done] 572 + 9 written and read back; backup", stamp)
