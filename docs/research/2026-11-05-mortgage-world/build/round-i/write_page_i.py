# -*- coding: utf-8 -*-
"""MortgageWorld I, page 121 (HAD-675, C1 + G1b): answer first. Ten chapters of the old guide opened with no number, date or source.
Each gets one short paragraph right after its heading (answers.json): a direct answer with a dated figure and its official source,
and a link to the page that owns the topic or to the tool on this page. The existing first paragraph follows unchanged; nothing is
removed. On phones the folded chapter keeps this new paragraph visible. Figures: the Bank of Israel all-banks average of 9.2026
(boi-mortgage.json, recomputed 6.11.2026), new loans 8.2026, directive 329, the Tax Authority's purchase-tax brackets (ptax.json) and
4-room medians (4-6.2026), the 2022 replay of the page's own tool. python write_page_i.py --dry | python write_page_i.py"""
import html, io, json, os, re, sys, time, urllib.request
H = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(H, "..", "..", "..", "..", ".."))
DRY = "--dry" in sys.argv
if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")
PID = 121
A = json.load(io.open(os.path.join(H, "answers.json"), encoding="utf-8"))
src = open(os.path.join(REPO, "scripts", "skin-a", "deployskin.py"), encoding="utf-8").read(); ns = {"__name__": "mw_i"}
exec(compile(src[:src.index('s, h, _ = req("GET", "/wp-json/nadlan/v1/health")')], "h", "exec"), ns)
req = ns["req"]
s, r, _ = req("GET", "/wp-json/wp/v2/pages/%d?context=edit&_fields=content,link" % PID)
assert s == 200, s
raw = r["content"]["raw"]
assert 'class="nlx-ans"' not in raw, "already written"
new = raw
for a in A:
    pat = re.compile(r'(<h2[^>]*>\s*' + re.escape(a["h2"]) + r'\s*</h2>)')
    m = pat.findall(new)
    assert len(m) == 1, ("heading", a["h2"], len(m))
    new = pat.sub(lambda mm: mm.group(1) + '\n<p class="nlx-ans">' + a["p"] + '</p>', new, count=1)
    assert not re.search(r"[–—]", re.sub(r"<[^>]+>", " ", a["p"]))
for line in raw.split("\n"):
    if line.strip():
        assert line in new, ("an original line is missing", line[:90])
print("[page %d] %d answer-first paragraphs; content %d -> %d bytes" % (PID, len(A), len(raw), len(new)))
if DRY:
    io.open(os.path.join(H, "preview-content-i.html"), "w", encoding="utf-8", newline="").write(new); print("[dry] ok"); sys.exit(0)
bk = os.path.join(H, "page-backup"); os.makedirs(bk, exist_ok=True)
io.open(os.path.join(bk, "page-%d-%s.html" % (PID, time.strftime("%Y%m%d-%H%M%S"))), "w", encoding="utf-8", newline="").write(raw)
s2, _, _ = req("POST", "/wp-json/wp/v2/pages/%d" % PID, {"content": new}); assert s2 in (200, 201), s2
time.sleep(4)
page = urllib.request.urlopen(urllib.request.Request(r["link"] + "?x=%d" % time.time(), headers={"User-Agent": "Mozilla/5.0"}), timeout=90).read().decode("utf-8", "replace")
ok = {"10 answers": page.count('class="nlx-ans"') == len(A), "38 questions": page.count('"@type":"Question"') == 38, "one h1": page[page.find("<body"):].count("<h1") == 1,
      "HowTo": 'id="nlmx-howto"' in page, "fold": 'id="nlmx-fold-js"' in page, "7 tools": 'data-sw="tool-keys"' in page}
for k, v_ in ok.items(): print("   ", "OK " if v_ else "BAD", k)
