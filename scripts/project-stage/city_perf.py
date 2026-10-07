# -*- coding: utf-8 -*-
"""HAD-460: load times of the city price pages, before and after the price list (the CEO's terms: measure, compare, then decide
the other cities). The same method as docs/qa/had-460/city-perf/before.json: server first byte (median of 3 curl runs) and a
phone load in headless Chrome (390x844, best of 2, navigation timing loadEventEnd / domContentLoadedEventEnd).
python city_perf.py <out-name> <path> [<path> ...]      writes docs/qa/had-460/city-perf/<out-name>.json and prints the diff vs before"""
import json
import os
import statistics
import subprocess
import sys
import time

from playwright.sync_api import sync_playwright

HERE = os.path.dirname(os.path.abspath(__file__))
OUTDIR = os.path.join(os.path.dirname(os.path.dirname(HERE)), "docs", "qa", "had-460", "city-perf")
# --vs <name>: compare with <name>.json instead of before.json (each wave keeps its own baseline)
VS = sys.argv[sys.argv.index("--vs") + 1] if "--vs" in sys.argv else "before"
args = [a for i, a in enumerate(sys.argv[1:], 1) if a != "--vs" and (i < 2 or sys.argv[i - 1] != "--vs")]
name, pages = args[0], args[1:]
out = {}
for p in pages:
    ttfb, size = [], 0
    for i in range(3):
        r = subprocess.run(["curl", "-s", "-o", "NUL" if os.name == "nt" else "/dev/null", "-w", "%{time_starttransfer} %{size_download}",
                            "https://nad-lan.co.il" + p + "?nlperf=%d" % (time.time() * 1000 + i)], capture_output=True, text=True)
        a = r.stdout.split()
        ttfb.append(float(a[0])); size = int(float(a[1]))
    out[p] = {"ttfb_s": round(statistics.median(ttfb), 3), "html_bytes": size}
with sync_playwright() as pw:
    b = pw.chromium.launch(channel="chrome", headless=True)
    for p in pages:
        loads = []
        for i in range(2):
            c = b.new_context(viewport={"width": 390, "height": 844}, is_mobile=True)
            pg = c.new_page()
            pg.goto("https://nad-lan.co.il" + p + "?nlperf=%d" % (time.time() * 1000 + i), wait_until="load", timeout=120000)
            loads.append(pg.evaluate("()=>{const n=performance.getEntriesByType('navigation')[0];"
                                     "return {load:Math.round(n.loadEventEnd),dcl:Math.round(n.domContentLoadedEventEnd)}}"))
            c.close()
        out[p]["phone_load_ms"] = min(x["load"] for x in loads)
        out[p]["phone_dcl_ms"] = min(x["dcl"] for x in loads)
    b.close()
json.dump(out, open(os.path.join(OUTDIR, name + ".json"), "w"), indent=1)
before = json.load(open(os.path.join(OUTDIR, VS + ".json"))) if os.path.exists(os.path.join(OUTDIR, VS + ".json")) else {}
# the CEO's stop rule for the waves: first byte +0.15 s or phone load +0.3 s on any page
stop = [p for p, v in out.items() if before.get(p) and (v["ttfb_s"] - before[p]["ttfb_s"] > 0.15 or v["phone_load_ms"] - before[p]["phone_load_ms"] > 300)]
for p, v in out.items():
    w = before.get(p, {})
    print(f"{p}: first byte {w.get('ttfb_s', '-')} -> {v['ttfb_s']} s | phone load {w.get('phone_load_ms', '-')} -> {v['phone_load_ms']} ms"
          f" | DOM ready {w.get('phone_dcl_ms', '-')} -> {v['phone_dcl_ms']} ms | html {v['html_bytes']:,} bytes")
if before:
    print("STOP RULE HIT:" if stop else "stop rule: clear", stop)
