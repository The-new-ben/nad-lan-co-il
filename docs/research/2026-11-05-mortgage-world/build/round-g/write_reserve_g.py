# -*- coding: utf-8 -*-
"""Round G (T8, HAD-675), after release 1.72.592: the quick calculator is taller (the two cost fields and the note), so the min-height
reserved for it in the page content (style nlmq-reserve, round F2) follows the new mounted heights, measured with mquick v5
(round-g/verify-g.json "mounted"). Each value is at most the mounted height at the narrowest width of its range: no gap is left.
Hebrew mounted: 360 1119 · 375 1101 · 390 1049 · 412 1049 · 430 1031 · 600 1013 · 768 905 · 1024+ 921.
English mounted: 360-390 1207 · 412 1171 · 430 1119 · 600 1049 · 768 993 · 1024+ 957.
  python write_reserve_g.py --dry | python write_reserve_g.py"""
import io, os, re, sys, time, urllib.request
H = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(H, "..", "..", "..", "..", ".."))
DRY = "--dry" in sys.argv
if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")
RE = re.compile(r'<style id="nlmq-reserve">.*?</style>', re.S)


def css(base, steps):
    s = '.nli-host[data-nli="mquick"]{min-height:%dpx}' % base
    for w, h in steps:
        s += '@media (max-width:%dpx){.nli-host[data-nli="mquick"]{min-height:%dpx}}' % (w, h)
    return '<style id="nlmq-reserve">' + s + '</style>'


NEW = {121: css(905, [(599, 1013), (449, 1031), (429, 1049), (389, 1101), (374, 1119)]),
       8780: css(957, [(599, 1049), (449, 1119), (429, 1171), (411, 1207)])}
src = open(os.path.join(REPO, "scripts", "skin-a", "deployskin.py"), encoding="utf-8").read(); ns = {"__name__": "mw_g"}
exec(compile(src[:src.index('s, h, _ = req("GET", "/wp-json/nadlan/v1/health")')], "h", "exec"), ns)
req = ns["req"]
jobs = []
for pid, block in NEW.items():
    s, r, _ = req("GET", "/wp-json/wp/v2/pages/%d?context=edit&_fields=content,link" % pid)
    assert s == 200, s
    raw = r["content"]["raw"]
    m = RE.findall(raw)
    assert len(m) == 1, (pid, len(m))
    assert m[0] != block, (pid, "already written")
    new = raw.replace(m[0], block)
    for line in raw.split("\n"):
        if line.strip() and m[0] not in line:
            assert line in new, (pid, "an original line is missing", line[:90])
    print("[page %d] reserve %d -> %d bytes" % (pid, len(m[0]), len(block)))
    jobs.append((pid, r, raw, new))
if DRY:
    print("[dry] ok"); sys.exit(0)
bk = os.path.join(H, "page-backup"); os.makedirs(bk, exist_ok=True)
for pid, r, raw, new in jobs:
    io.open(os.path.join(bk, "page-%d-%s-g.html" % (pid, time.strftime("%Y%m%d-%H%M%S"))), "w", encoding="utf-8", newline="").write(raw)
    s2, _, _ = req("POST", "/wp-json/wp/v2/pages/%d" % pid, {"content": new}); assert s2 in (200, 201), s2
    time.sleep(4)
    page = urllib.request.urlopen(urllib.request.Request(r["link"] + "?x=%d" % time.time(), headers={"User-Agent": "Mozilla/5.0"}), timeout=90).read().decode("utf-8", "replace")
    print("   ", pid, "OK " if NEW[pid] in page else "BAD", "reserve live;", "OK " if page[page.find("<body"):].count("<h1") == 1 else "BAD", "one h1")
