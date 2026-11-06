# -*- coding: utf-8 -*-
"""Release 1.72.595 pre-check: every inherited or new check of deploy595.py that touches the near finder, evaluated BEFORE the run
against (a) the new finder.js / finder.css in the repo for asset URLs and (b) a simulation of the new pages: the live HTML with its
old footer block (#nlnf-lidi) replaced by the new one from footer_new.json, and the version string 1.72.594 -> 1.72.595."""
import ast, io, json, os, re, sys, time, urllib.request
if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")
H = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(H, "..", "..", ".."))
SRC = io.open(os.path.join(REPO, "scripts", "project-stage", "deploy595.py"), encoding="utf-8").read()
F = json.load(io.open(os.path.join(H, "footer_new.json"), encoding="utf-8"))
ASSET = {"near-finder/finder.js": os.path.join(REPO, "plugins", "nadlan-config", "assets", "near-finder", "finder.js"),
         "near-finder/finder.css": os.path.join(REPO, "plugins", "nadlan-config", "assets", "near-finder", "finder.css")}
PAGE = {"/": "home", "/properties/": "properties", "/%D7%93%D7%99%D7%A8%D7%95%D7%AA-%D7%9C%D7%94%D7%A9%D7%9B%D7%A8%D7%94/": "rent",
        "/brokers/meital-katzir/": "broker", "/professionals/meital-katzir/": "card"}
checks = []
for l in SRC.split("\n"):
    if l.startswith("    ('") and l.rstrip().endswith("),"):
        try:
            t = ast.literal_eval(l.strip()[:-1])
        except Exception:  # noqa: BLE001
            continue
        url = t[0]; path = url.split("?")[0]
        if any(k in url for k in ASSET) or path in PAGE:
            checks.append(t)
cache = {}
def page(path):
    if path in cache: return cache[path]
    h = urllib.request.urlopen(urllib.request.Request("https://nad-lan.co.il" + path + "?pc=%d" % time.time(), headers={"User-Agent": "Mozilla/5.0"}), timeout=90).read().decode("utf-8", "replace")
    m = re.search(r'<div class="nlnf nlnf-lidi" id="nlnf-lidi".*?(?=</body>|<script)', h, re.S)
    new = F.get(PAGE[path], "")
    if m:
        # the old block ends where the launcher's markup ends: find the matching close by counting divs
        i = m.start(); depth = 0; j = i
        for mm in re.finditer(r'<div\b|</div>', h[i:]):
            depth += 1 if mm.group(0).startswith('<div') else -1
            if depth == 0: j = i + mm.end(); break
        h = h[:i] + new + h[j:]
    if PAGE[path] == "card":  # the new context is empty there: nothing of the finder is enqueued
        h = re.sub(r"<(script|link)[^>]*near-finder/finder\.(js|css)[^>]*>(</script>)?", "", h)
    h = h.replace("ver=1.72.594", "ver=1.72.595")
    cache[path] = h; return h
bad = 0
for t in checks:
    url, must, mustnot = t[0], t[1], t[2]
    key = next((k for k in ASSET if k in url), None)
    body = io.open(ASSET[key], encoding="utf-8").read() if key else page(url.split("?")[0])
    miss = [m for m in must if m not in body]; hit = [m for m in mustnot if m in body]
    ok = not miss and not hit
    bad += 0 if ok else 1
    print(("OK  " if ok else "BAD ") + url[:70], ("missing " + str(miss)) if miss else "", ("present " + str(hit)) if hit else "")
print("BAD:", bad, "of", len(checks))
