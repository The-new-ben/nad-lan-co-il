# -*- coding: utf-8 -*-
"""HAD-395 (Ben 28.9.2026: Pro = ₪349; the consolidation audit 5.10 found /en/ /fr/ /ru/brokers/ still at ₪149 a month and ₪1,490
a year, against Hebrew ₪349 / ₪3,490). Replaces ONLY the Pro card's two figures in pages 7803 (en), 7888 (fr), 7887 (ru);
the "we build it" price ₪1,490 stays. Backs up each raw content first, checks every anchor appears exactly once, reads back.
App password in-process, never printed.   python fix_broker_price_395.py [--dry | --rollback]"""
import glob, io, json, os, re, sys, time
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(HERE))
QA = os.path.join(REPO, "docs", "qa", "had-395")
src = open(os.path.join(REPO, "scripts", "skin-a", "deployskin.py"), encoding="utf-8").read()
ns = {"__name__": "h395"}; exec(compile(src[:src.index('s, h, _ = req("GET", "/wp-json/nadlan/v1/health")')], "deployskin-helpers", "exec"), ns)
req = ns["req"]
PAGES = {7803: "en", 7888: "fr", 7887: "ru"}
ARGS = sys.argv[1:]
if "--show" in ARGS:
    for pid in PAGES:
        s, p, _ = req("GET", f"/wp-json/wp/v2/pages/{pid}?context=edit&_fields=content")
        raw = p["content"]["raw"]
        for m in re.finditer(r"149|1,490|1&nbsp;490|1 490|1&#160;490", raw):
            print(pid, repr(raw[max(0, m.start() - 160): m.end() + 60]))
    sys.exit(0)
REPL = {
    7803: ('<span class="nlof-num">NIS 149</span> a month</p><p class="nlof-sub">or <span class="nlof-num">NIS 1,490</span> a year',
           '<span class="nlof-num">NIS 349</span> a month</p><p class="nlof-sub">or <span class="nlof-num">NIS 3,490</span> a year'),
    7888: ('<span class="nlof-num">149&nbsp;₪</span> par mois</p><p class="nlof-sub">ou <span class="nlof-num">1&nbsp;490&nbsp;₪</span> par an',
           '<span class="nlof-num">349&nbsp;₪</span> par mois</p><p class="nlof-sub">ou <span class="nlof-num">3&nbsp;490&nbsp;₪</span> par an'),
    7887: ('<span class="nlof-num">149&nbsp;₪</span> в месяц</p><p class="nlof-sub">или <span class="nlof-num">1&nbsp;490&nbsp;₪</span> в год',
           '<span class="nlof-num">349&nbsp;₪</span> в месяц</p><p class="nlof-sub">или <span class="nlof-num">3&nbsp;490&nbsp;₪</span> в год'),
}
os.makedirs(QA, exist_ok=True)
if "--rollback" in ARGS:
    b = sorted(glob.glob(os.path.join(QA, "backup-*.json")))[-1]
    old = json.load(io.open(b, encoding="utf-8"))
    for pid, raw in old.items():
        s, r, _ = req("POST", f"/wp-json/wp/v2/pages/{pid}", {"content": raw}); print("[rollback]", pid, s)
    sys.exit(0)
backup, new = {}, {}
for pid, (a, b) in REPL.items():
    s, p, _ = req("GET", f"/wp-json/wp/v2/pages/{pid}?context=edit&_fields=content")
    raw = p["content"]["raw"]
    if raw.count(a) != 1:
        raise SystemExit(f"FATAL {pid}: anchor found {raw.count(a)} times")
    backup[str(pid)] = raw
    new[pid] = raw.replace(a, b)
bp = os.path.join(QA, "backup-%s.json" % time.strftime("%Y%m%dT%H%M%SZ", time.gmtime()))
io.open(bp, "w", encoding="utf-8").write(json.dumps(backup, ensure_ascii=False))
print("[backup]", os.path.basename(bp))
if "--dry" in ARGS:
    print("[dry] anchors found once in all 3 pages; no writes"); sys.exit(0)
for pid, raw in new.items():
    s, r, _ = req("POST", f"/wp-json/wp/v2/pages/{pid}", {"content": raw})
    s2, p2, _ = req("GET", f"/wp-json/wp/v2/pages/{pid}?context=edit&_fields=content")
    print("[write]", pid, PAGES[pid], "http", s, "| read-back identical:", p2["content"]["raw"] == raw)
