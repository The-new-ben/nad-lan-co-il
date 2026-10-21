# -*- coding: utf-8 -*-
"""HAD-534 Mission B: insert section.html into page 8406 (/sde-dov/contamination/) right before the "שאלות נפוצות" heading.
Backup before, read-back after, refuses to run twice. No names (checked again here).  python apply_env.py [--dry]"""
import io, os, re, sys, time
REPO = r"C:\Users\777\nad-lan\nad-lan-co-il"
src = open(os.path.join(REPO, "scripts", "skin-a", "deployskin.py"), encoding="utf-8").read(); ns = {"__name__": "env"}
exec(compile(src[:src.index('s, h, _ = req("GET", "/wp-json/nadlan/v1/health")')], "h", "exec"), ns)
req = ns["req"]
H = os.path.dirname(os.path.abspath(__file__))
sec = io.open(os.path.join(H, "section.html"), encoding="utf-8").read().strip()
for bad in ("זיהום", "מזוהמ", "דמרי", "גינדי", "שיכון ובינוי", "אוטופיה", "אשירה", "ריינבו", "חג'ג'", "פרשקובסקי"):
    assert bad not in sec, bad
s, b, _ = req("GET", "/wp-json/wp/v2/pages/8406?context=edit&_fields=content,modified")
raw = b["content"]["raw"]
if 'id="sde-dov-environment"' in raw:
    raise SystemExit("already there")
m = re.search(r"<h2[^>]*>\s*שאלות נפוצות\s*</h2>", raw)
assert m and raw.count("שאלות נפוצות</h2>") == 1, "the FAQ heading"
out = raw[:m.start()] + sec + "\n\n" + raw[m.start():]
print("[plan] 8406: %d -> %d chars, inserted at %d" % (len(raw), len(out), m.start()))
if "--dry" in sys.argv:
    raise SystemExit(0)
bk = os.path.join(REPO, "docs", "qa", "had-534", "page-backup"); os.makedirs(bk, exist_ok=True)
io.open(os.path.join(bk, "8406-%s.html" % time.strftime("%Y%m%d-%H%M%S")), "w", encoding="utf-8").write(raw)
req("POST", "/wp-json/wp/v2/pages/8406", {"content": out})
s, b2, _ = req("GET", "/wp-json/wp/v2/pages/8406?context=edit&_fields=content")
print("written:", b2["content"]["raw"] == out)
