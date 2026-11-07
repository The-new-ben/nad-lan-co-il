# -*- coding: utf-8 -*-
"""HAD-681 (Ben 7.11.2026: "קניית דירה ... זה עושה לנו כמה התנגשויות"): on the owner of "קניית דירה" (/buying-apartment/, page 9),
9 link blocks carried H2s that lead with "מחירי דירות" / "מחירי בתים" / "בדיקת מחירי דירות", the head terms of other pages.
They become bold lines (not headings). Text and links stay; every link already points to that city's owner page. Backup + read-back.
python demote_price_headings_p9.py [--go]"""
import io, json, os, re, sys, time
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(HERE))
src = open(os.path.join(REPO, "scripts", "skin-a", "deployskin.py"), encoding="utf-8").read(); ns = {"__name__": "dm"}
exec(compile(src[:src.index('s, h, _ = req("GET", "/wp-json/nadlan/v1/health")')], "h", "exec"), ns); req = ns["req"]
TITLES = ["בדיקת מחירי דירות בתל אביב", "בדיקת מחירי דירות בנווה צדק", "בדיקת מחירי דירות בהרצליה פיתוח", "מחירי דירות בהרצליה",
          "מחירי דירות ברמת השרון", "מחירי דירות ברעננה", "מחירי בתים בכפר שמריהו", "מחירי בתים בסביון", "מחירי בתים ברשפון"]
s, b, _ = req("GET", "/wp-json/wp/v2/pages/9?context=edit&_fields=content"); assert s == 200, s
raw = b["content"]["raw"]; new = raw
for t in TITLES:
    rx = re.compile(r"<h2([^>]*)>\s*" + re.escape(t) + r"\s*</h2>")
    hits = rx.findall(new); assert len(hits) == 1, (t, len(hits))
    new = rx.sub('<p class="nl-linkhead" style="font-weight:700;font-size:1.15em;line-height:1.4;margin:0 0 .45em">' + t + "</p>", new)
print("[plan] H2 before %d, after %d" % (len(re.findall(r"<h2[\s>]", raw)), len(re.findall(r"<h2[\s>]", new))))
if "--go" not in sys.argv: sys.exit(0)
bk = os.path.join(REPO, "docs", "qa", "retitle-2026-11-07"); os.makedirs(bk, exist_ok=True)
io.open(os.path.join(bk, "backup-p9-headings-%s.html" % time.strftime("%Y%m%dT%H%M%S")), "w", encoding="utf-8").write(raw)
s2, _, _ = req("POST", "/wp-json/wp/v2/pages/9", {"content": new}); assert s2 in (200, 201), s2
s, r, _ = req("GET", "/wp-json/wp/v2/pages/9?context=edit&_fields=content"); assert r["content"]["raw"] == new, "read-back"
print("[done] page 9 written and read back")
