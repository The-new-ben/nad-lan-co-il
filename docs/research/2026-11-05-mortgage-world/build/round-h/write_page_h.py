# -*- coding: utf-8 -*-
"""MortgageWorld H, page 121 (HAD-675, T4), after release 1.72.593 registered the tool: the 7th chip "מהחוזה למפתח" and its pane in the
tools switcher (#tools), and the switcher heading says seven tools. Nothing removed; every original line kept (the three edited
lines in their edited form). python write_page_h.py --dry | python write_page_h.py"""
import io, os, re, sys, time, urllib.request
H = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(H, "..", "..", "..", "..", ".."))
DRY = "--dry" in sys.argv
if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")
PID = 121
H2_A = '<h2 id="nlmx-sw-h">ומה עוד בודקים: שישה כלים למשכנתא</h2>'
H2_B = '<h2 id="nlmx-sw-h">ומה עוד בודקים: שבעה כלים למשכנתא</h2>'
CHIP_A = 'aria-controls="tool-ready">מוכנים לאישור עקרוני?</button></div>'
CHIP_B = 'aria-controls="tool-ready">מוכנים לאישור עקרוני?</button><button type="button" data-sw="tool-keys" aria-controls="tool-keys">מהחוזה למפתח</button></div>'
PANE_A = '[nadlan_tool id="mready"]\n</div>\n</section>'
PANE_B = ('[nadlan_tool id="mready"]\n</div>\n'
          '<div class="nlmx-pane" id="tool-keys"><p>קונים דירה מקבלן? כל תשלום לקבלן לפי התאריך שלו: כמה מוסיפה ההצמדה למדד תשומות הבנייה, '
          'מה יוצא מההון העצמי ומה נמשך מהמשכנתא, כמה ריבית משלמים עד המסירה, ומה ההחזר המלא אחרי המפתח.</p>\n'
          '[nadlan_tool id="mkeys"]\n</div>\n</section>')
EDITS = [(H2_A, H2_B), (CHIP_A, CHIP_B), (PANE_A, PANE_B)]
src = open(os.path.join(REPO, "scripts", "skin-a", "deployskin.py"), encoding="utf-8").read(); ns = {"__name__": "mw_h"}
exec(compile(src[:src.index('s, h, _ = req("GET", "/wp-json/nadlan/v1/health")')], "h", "exec"), ns)
req = ns["req"]
s, r, _ = req("GET", "/wp-json/wp/v2/pages/%d?context=edit&_fields=content,link" % PID)
assert s == 200, s
raw = r["content"]["raw"]
assert '[nadlan_tool id="mkeys"]' not in raw, "already written"
new = raw
for o, n_ in EDITS:
    assert new.count(o) == 1, ("anchor", o[:50], new.count(o)); new = new.replace(o, n_)
for line in raw.split("\n"):
    if not line.strip():
        continue
    ln = line
    for o, n_ in EDITS:
        ln = ln.replace(o, n_)
    assert ln in new, ("an original line is missing", line[:90])
assert not re.search(r"[–—]", re.sub(r"<[^>]+>", " ", PANE_B + CHIP_B + H2_B))
print("[page %d] %d edits; content %d -> %d bytes; other mentions of six tools: %d" % (PID, len(EDITS), len(raw), len(new), new.count("ששת הכלים") + new.count("שישה כלים")))
if DRY:
    print("[dry] ok"); sys.exit(0)
bk = os.path.join(H, "page-backup"); os.makedirs(bk, exist_ok=True)
io.open(os.path.join(bk, "page-%d-%s.html" % (PID, time.strftime("%Y%m%d-%H%M%S"))), "w", encoding="utf-8", newline="").write(raw)
s2, _, _ = req("POST", "/wp-json/wp/v2/pages/%d" % PID, {"content": new}); assert s2 in (200, 201), s2
time.sleep(4)
page = urllib.request.urlopen(urllib.request.Request(r["link"] + "?x=%d" % time.time(), headers={"User-Agent": "Mozilla/5.0"}), timeout=90).read().decode("utf-8", "replace")
ok = {"mkeys host": 'data-nli="mkeys"' in page, "summary": "המדד האחרון שפרסמה הלשכה המרכזית לסטטיסטיקה" in page and "מהחוזה למפתח" in page,
      "7th chip": 'data-sw="tool-keys"' in page, "seven": "שבעה כלים למשכנתא" in page, "mkeys.js": "tools/mkeys.js" in page and "tools/indexation.js" in page,
      "no php warning": "Warning:" not in page and "Fatal error" not in page, "one h1": page[page.find("<body"):].count("<h1") == 1, "38 questions": page.count('"@type":"Question"') == 38}
for k, v_ in ok.items(): print("   ", "OK " if v_ else "BAD", k)
