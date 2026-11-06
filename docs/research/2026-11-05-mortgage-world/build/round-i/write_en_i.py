# -*- coding: utf-8 -*-
"""MortgageWorld I (C1), English page 8780: the one chapter that opened with no figure ("Olim and returning residents") gets an
answer-first paragraph, the same pattern as the ten Hebrew ones (AnswerFirst board). Figures from ptax.json (the Tax Authority's
brackets in force since 16.1.2025, the data of the live purchase-tax calculator: oleh track 0% to 1,978,745, 0.5% to 6,055,070) and
directive 329 (75% for a single home). Nothing removed. python write_en_i.py --dry | python write_en_i.py"""
import io, os, re, sys, time, urllib.request
H = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(H, "..", "..", "..", "..", ".."))
DRY = "--dry" in sys.argv
if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")
PID = 8780
H2 = "Olim and returning residents: what to check before you borrow"
P = ("An oleh who buys a home within the eligibility period pays no purchase tax on the first ₪1,978,745 of the price and 0.5% on the part "
     "up to ₪6,055,070 (Israel Tax Authority brackets in force since 16 January 2025), and borrows under the same Directive 329 limits as "
     "every Israeli citizen: up to 75% of the value for a single home.")
src = open(os.path.join(REPO, "scripts", "skin-a", "deployskin.py"), encoding="utf-8").read(); ns = {"__name__": "mw_ien"}
exec(compile(src[:src.index('s, h, _ = req("GET", "/wp-json/nadlan/v1/health")')], "h", "exec"), ns)
req = ns["req"]
s, r, _ = req("GET", "/wp-json/wp/v2/pages/%d?context=edit&_fields=content,link" % PID)
assert s == 200, s
raw = r["content"]["raw"]
assert 'class="nlx-ans"' not in raw, "already written"
pat = re.compile(r'(<h2[^>]*>\s*' + re.escape(H2) + r'\s*</h2>)')
assert len(pat.findall(raw)) == 1, len(pat.findall(raw))
new = pat.sub(lambda m: m.group(1) + '\n<p class="nlx-ans">' + P + '</p>', raw, count=1)
for line in raw.split("\n"):
    if line.strip():
        assert line in new, ("an original line is missing", line[:90])
assert not re.search(r"[–—]", P)
print("[page %d] 1 answer-first paragraph, %d words; content %d -> %d bytes" % (PID, len(P.split()), len(raw), len(new)))
if DRY:
    print("[dry] ok"); sys.exit(0)
bk = os.path.join(H, "page-backup"); os.makedirs(bk, exist_ok=True)
io.open(os.path.join(bk, "page-%d-%s.html" % (PID, time.strftime("%Y%m%d-%H%M%S"))), "w", encoding="utf-8", newline="").write(raw)
s2, _, _ = req("POST", "/wp-json/wp/v2/pages/%d" % PID, {"content": new}); assert s2 in (200, 201), s2
time.sleep(4)
page = urllib.request.urlopen(urllib.request.Request(r["link"] + "?x=%d" % time.time(), headers={"User-Agent": "Mozilla/5.0"}), timeout=90).read().decode("utf-8", "replace")
ok = {"answer": page.count('class="nlx-ans"') == 1 and "1,978,745" in page, "15 questions": page.count('"@type":"Question"') == 15,
      "one h1": page[page.find("<body"):].count("<h1") == 1, "fold": 'id="nlmx-fold-js"' in page}
for k, v_ in ok.items(): print("   ", "OK " if v_ else "BAD", k)
