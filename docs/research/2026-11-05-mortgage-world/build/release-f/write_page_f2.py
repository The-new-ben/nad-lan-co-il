# -*- coding: utf-8 -*-
"""MortgageWorld F2 (HAD-675): two fixes found by the benchmark after round F, content only, nothing removed.
  1. Layout shift (CLS 0.047 on a 390 px phone): the quick calculator mounts 500 to 640 px taller than its server summary and pushes
     the paragraph under it out of the first screen. A min-height reserved per width on the mquick host, measured on the live pages
     (Hebrew mounted: 933 at 360-375, 881 at 390-412, 863 at 430-600, 755 at 768, 771 at 1024+; English: 1021 at 360-390,
     1003 at 412, 951 at 430, 881 at 600, 825 at 768, 789 at 1024+). Each value is at most the mounted height, so no gap is left.
     The style goes right before the tool, so it applies before the first paint.
  2. The loan distribution by income share and by financing share sits in a chapter that folds on phones. One sentence with the two
     August 2026 figures already on the page (52.6% of the amount at 30% to 40% of income; 48.8% at 60% to 75% financing) is added
     to the chapter's first paragraph, which stays visible.
  python write_page_f2.py --dry | python write_page_f2.py"""
import io, os, re, sys, time, urllib.request
H = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(H, "..", "..", "..", "..", ".."))
DRY = "--dry" in sys.argv
if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")
TOOL = '[nadlan_tool id="mquick"]'
RES_HE = ('<style id="nlmq-reserve">.nli-host[data-nli="mquick"]{min-height:755px}@media (max-width:599px){.nli-host[data-nli="mquick"]{min-height:863px}}'
          '@media (max-width:429px){.nli-host[data-nli="mquick"]{min-height:881px}}@media (max-width:389px){.nli-host[data-nli="mquick"]{min-height:933px}}</style>\n')
RES_EN = ('<style id="nlmq-reserve">.nli-host[data-nli="mquick"]{min-height:789px}@media (max-width:599px){.nli-host[data-nli="mquick"]{min-height:951px}}'
          '@media (max-width:429px){.nli-host[data-nli="mquick"]{min-height:1003px}}@media (max-width:411px){.nli-host[data-nli="mquick"]{min-height:1021px}}</style>\n')
P_END = "בספטמבר, לפי פרסום ראשון של בנק ישראל, ניתנו משכנתאות בסך 8.67 מיליארד ₪.</p>"
P_ADD = ("בספטמבר, לפי פרסום ראשון של בנק ישראל, ניתנו משכנתאות בסך 8.67 מיליארד ₪. בהתפלגות של אוגוסט, 52.6% מסכום המשכנתאות החדשות ניתן ביחס החזר של 30% עד 40% "
         "מההכנסה, ו־48.8% בשיעור מימון של 60% עד 75% משווי הדירה.</p>")

src = open(os.path.join(REPO, "scripts", "skin-a", "deployskin.py"), encoding="utf-8").read(); ns = {"__name__": "mw_f2"}
exec(compile(src[:src.index('s, h, _ = req("GET", "/wp-json/nadlan/v1/health")')], "h", "exec"), ns)
req = ns["req"]


def build(pid, edits):
    s, r, _ = req("GET", "/wp-json/wp/v2/pages/%d?context=edit&_fields=content,link" % pid)
    assert s == 200, s
    raw = r["content"]["raw"]
    assert 'id="nlmq-reserve"' not in raw, (pid, "already written")
    new = raw
    for o, n_ in edits:
        assert new.count(o) == 1, (pid, "anchor", o[:40], new.count(o)); new = new.replace(o, n_)
    for line in raw.split("\n"):
        if not line.strip():
            continue
        ln = line
        for o, n_ in edits:
            ln = ln.replace(o, n_)
        assert ln in new, (pid, "an original line is missing", line[:90])
    assert not re.search(r"[–—]", re.sub(r"<[^>]+>", " ", "".join(n_ for _, n_ in edits)))
    print("[page %d] %d edits; content %d -> %d bytes" % (pid, len(edits), len(raw), len(new)))
    return r, raw, new


jobs = [(121, [(TOOL, RES_HE + TOOL), (P_END, P_ADD)]), (8780, [(TOOL, RES_EN + TOOL)])]
built = [(pid,) + build(pid, e) for pid, e in jobs]
if DRY:
    print("[dry] ok"); sys.exit(0)
bk = os.path.join(H, "page-backup"); os.makedirs(bk, exist_ok=True)
for pid, r, raw, new in built:
    io.open(os.path.join(bk, "page-%d-%s-f2.html" % (pid, time.strftime("%Y%m%d-%H%M%S"))), "w", encoding="utf-8", newline="").write(raw)
    s2, _, _ = req("POST", "/wp-json/wp/v2/pages/%d" % pid, {"content": new}); assert s2 in (200, 201), s2
    time.sleep(4)
    page = urllib.request.urlopen(urllib.request.Request(r["link"] + "?x=%d" % time.time(), headers={"User-Agent": "Mozilla/5.0"}), timeout=90).read().decode("utf-8", "replace")
    ok = {"reserve": 'id="nlmq-reserve"' in page, "one h1": page[page.find("<body"):].count("<h1") == 1, "fold": 'id="nlmx-fold-js"' in page}
    if pid == 121:
        ok["distribution sentence"] = "בהתפלגות של אוגוסט, 52.6%" in page
        ok["38 questions"] = page.count('"@type":"Question"') == 38
    for k, v_ in ok.items(): print("   ", pid, "OK " if v_ else "BAD", k)
