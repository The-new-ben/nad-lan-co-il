# -*- coding: utf-8 -*-
"""MortgageWorld B, page 121 /mortgage-calculator/ (HAD-675). Runs AFTER release 1.72.588 is live (the six tools, mquick v2 with
the switcher wiring). ADDITIVE: nothing old changes; two insertions:
  1. after the lead paragraph, a phone-only style that sets the lead at 16px (the first field comes higher on a phone);
  2. after the full tool (its <details> and script) and before the folded classic calculator, the section "ומה עוד בודקים" with
     six chips and six panels, each a [nadlan_tool]: mbudget, moffers, mdecision, mreplay, mexit, mready. Without scripts every
     panel shows (readers, search engines, AI answers); with scripts one at a time (mquick.js wireSwitch). #tool-xxx opens one.
  python write_page_b.py --dry | python write_page_b.py"""
import io, json, os, re, sys, time, urllib.request
H = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(H, "..", "..", "..", "..", ".."))
DRY = "--dry" in sys.argv
if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")
PID = 121
LEAD_END = "כל הנתונים ממקורות רשמיים, עם תאריך.</p>\n"
LEAD_CSS = '<style id="nlmx-lead">@media (max-width:600px){.nlu1-lead{font-size:16px!important;line-height:1.65!important}}</style>\n'
CLASSIC_ANCHOR = '<details class="nlmx-fold"><summary><span>המחשבון הקלאסי לפי שלושה מסלולים'
TOOLS = [
    ("tool-budget", "כמה דירה זה קונה", "mbudget", "ההכנסה, ההון העצמי וסוג הרכישה: המחיר הגבוה שעובר את שתי המגבלות של בנק ישראל, הערים שבהן דירת 4 חדרים במחיר החציוני נכנסת בו, והדירות באתר עד המחיר הזה."),
    ("tool-offers", "שלוש הצעות, טבלה אחת", "moffers", "השוואת הצעות משכנתא: שלושת המספרים של כל סל אחיד משניים או שלושה אישורים עקרוניים, ההצעה הזולה בכל סל, הפער בשקלים, כל בנק מול הממוצע שלו ונוסח מוכן למיקוח."),
    ("tool-decision", "החלטת הריבית", "mdecision", "כמה כל רבע אחוז בריבית בנק ישראל מזיז את ההחזר שלכם בשקלים, מתי ההחלטה הבאה ומה התחזיות."),
    ("tool-replay", "אם 2022 חוזרת", "mreplay", "מבחן לחץ אמיתי: עשר העלאות הריבית של אפריל 2022 עד מאי 2023 והמדד של אותם חודשים, חודש אחרי חודש, על התמהיל שלכם."),
    ("tool-exit", "כמה תעלה היציאה", "mexit", "מתכננים למכור, לשדרג או למחזר בעוד כמה שנים? הריבית, ההצמדה ועמלת הפירעון המוקדם הצפויה עד אז, בתמהיל שלכם ובשלושת הסלים."),
    ("tool-ready", "מוכנים לאישור עקרוני?", "mready", "חמש שאלות, כרטיס מוכנות מול מגבלות בנק ישראל ורשימת מסמכים אישית לאישור העקרוני ולמשכנתא."),
]
SW = ('<section class="nlmx-sw" id="tools" aria-labelledby="nlmx-sw-h">\n<h2 id="nlmx-sw-h">ומה עוד בודקים: שישה כלים למשכנתא</h2>\n'
      '<p>כל כלי עונה על שאלה אחת שעולה לפני משכנתא או אחריה, על הנתונים הרשמיים של בנק ישראל ורשות המסים. בחרו כלי:</p>\n'
      '<div class="nlmx-sw__chips" role="group" aria-label="בחירת כלי">'
      + "".join('<button type="button" data-sw="%s" aria-controls="%s">%s</button>' % (i, i, lab) for i, lab, _, _ in TOOLS) + '</div>\n'
      + "".join('<div class="nlmx-pane" id="%s"><p>%s</p>\n[nadlan_tool id="%s"]\n</div>\n' % (i, intro, tid) for i, _, tid, intro in TOOLS)
      + '</section>\n')

sys.stdout.flush()
src = open(os.path.join(REPO, "scripts", "skin-a", "deployskin.py"), encoding="utf-8").read(); ns = {"__name__": "mw_page_b"}
exec(compile(src[:src.index('s, h, _ = req("GET", "/wp-json/nadlan/v1/health")')], "h", "exec"), ns)
req = ns["req"]
s, r, _ = req("GET", "/wp-json/wp/v2/pages/%d?context=edit&_fields=content,link,modified" % PID)
assert s == 200, s
raw = r["content"]["raw"]
assert '[nadlan_tool id="mquick"]' in raw and "[nadlan_mortgage_market]" in raw, "release A content is not on the page"
assert 'class="nlmx-sw"' not in raw, "already written"
new = raw
assert new.count(LEAD_END) == 1, new.count(LEAD_END)
new = new.replace(LEAD_END, LEAD_END + LEAD_CSS)
assert new.count(CLASSIC_ANCHOR) == 1, new.count(CLASSIC_ANCHOR)
new = new.replace(CLASSIC_ANCHOR, SW + CLASSIC_ANCHOR)
for line in raw.split("\n"):
    if line.strip():
        assert line in new, ("an original line is missing", line[:80])
order = [new.index(x) for x in ('[nadlan_tool id="mquick"]', 'id="mortgage-full"', 'class="nlmx-sw"', '[nadlan_tool id="mbudget"]', '[nadlan_tool id="mready"]', CLASSIC_ANCHOR, "[nadlan_mortgage_market]", '<section id="faq">')]
assert order == sorted(order), ("order", order)
v = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", re.sub(r"\[[a-z_]+[^\]]*\]", " ", re.sub(r"<style\b.*?</style>", " ", SW, flags=re.S))))
assert not re.search(r"[–—]", v), "long dash"
m_ = re.search(r"ממשק|מערכת|פלטפורמ|סימולצי|אינטראקטיב|בקרוב|מנגנון|מודל|הדגמה|טכנולוגי|אלגוריתם|\bדמו\b", v); assert not m_, m_.group(0) if m_ else ""
assert '"' not in v, "ASCII quote"
print("[page %d] %s | modified %s | switcher %d tools | new visible words %d" % (PID, r["link"], r["modified"], len(TOOLS), len(v.split())))
if DRY:
    io.open(os.path.join(H, "preview-content-b.html"), "w", encoding="utf-8", newline="").write(new)
    print("[dry] nothing written"); sys.exit(0)
bk = os.path.join(H, "page-backup"); os.makedirs(bk, exist_ok=True)
io.open(os.path.join(bk, "page-%d-%s.html" % (PID, time.strftime("%Y%m%d-%H%M%S"))), "w", encoding="utf-8", newline="").write(raw)
s2, _, _ = req("POST", "/wp-json/wp/v2/pages/%d" % PID, {"content": new})
assert s2 in (200, 201), s2
back = req("GET", "/wp-json/wp/v2/pages/%d?context=edit&_fields=content" % PID)[1]["content"]["raw"]
time.sleep(4)
page = urllib.request.urlopen(urllib.request.Request(r["link"] + "?x=%d" % time.time(), headers={"User-Agent": "Mozilla/5.0"}), timeout=90).read().decode("utf-8", "replace")
bd = page[page.find("<body"):]
ok = {"read-back": back.strip() == new.strip(), "one h1": bd.count("<h1") == 1, "switcher": 'class="nlmx-sw"' in bd}
for _, _, tid, _ in TOOLS:
    ok["mount " + tid] = 'data-nli="%s"' % tid in bd
for f in ("mbudget", "moffers", "mready", "mrates-common", "mdecision", "mreplay", "mexit", "mortgage", "mquick"):
    ok["script " + f] = "tools/%s.js" % f in page
ok["one FAQPage"] = page.count('"@type":"FAQPage"') == 1
ok["38 questions"] = page.count('"@type":"Question"') == 38
for k, v_ in ok.items(): print("   ", "OK " if v_ else "BAD", k)
print("ALL OK" if all(ok.values()) else "SOME CHECKS FAILED: the backup is in page-backup/")
