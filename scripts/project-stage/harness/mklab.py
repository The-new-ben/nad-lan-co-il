# -*- coding: utf-8 -*-
"""A local copy of the LIVE Rainbow page that runs the plugin's stage assets from a local folder, so a lab (Codex's
labs/unit-journey, or any agent) can try its own stage.js on the real page without touching WordPress.

  python scripts/project-stage/harness/mklab.py <outdir> [--stage path/to/stage.js] [--bridge path/to/bridge.js] [--url URL]
  python -m http.server 47930 --bind 127.0.0.1 --directory <outdir>      (Codex's ports: 47930 and up)

It downloads the page (read-only), copies plugins/nadlan-config/assets/project-stage/ into <outdir>/assets/project-stage/,
optionally replaces stage.js / bridge.js with the lab's copies, and points every project-stage URL in the page (plain and
JSON-escaped) at the local copy. The Mapbox public token stays inside the downloaded page and is never committed.
Design system component UnitCut (version 37) names this kit; the page's order law is docs/checklists/PROJECT-PAGE-CHECKLIST.md.
"""
import argparse, os, re, shutil, time, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
PLUG = os.path.join(REPO, "plugins", "nadlan-config")
LIVE = "https://nad-lan.co.il/wp-content/plugins/nadlan-config/assets/project-stage/"

ap = argparse.ArgumentParser()
ap.add_argument("outdir")
ap.add_argument("--stage")
ap.add_argument("--bridge")
ap.add_argument("--url", default="https://nad-lan.co.il/projects/rainbow-tel-aviv/")
a = ap.parse_args()
out = os.path.abspath(a.outdir)
dst = os.path.join(out, "assets", "project-stage")
if os.path.isdir(dst):
    shutil.rmtree(dst)
shutil.copytree(os.path.join(PLUG, "assets", "project-stage"), dst)
if a.stage:
    shutil.copy(a.stage, os.path.join(dst, "rainbow", "stage.js"))
if a.bridge:
    shutil.copy(a.bridge, os.path.join(dst, "bridge.js"))
req = urllib.request.Request(a.url + ("&" if "?" in a.url else "?") + "lab=%d" % time.time(), headers={"User-Agent": "NadLan-Lab/1.0"})
html = urllib.request.urlopen(req, timeout=60).read().decode("utf-8")
html = html.replace(LIVE, "/assets/project-stage/").replace(LIVE.replace("/", "\/"), "\/assets\/project-stage\/")
html = re.sub(r"/assets/project-stage/([^\"'?\s]+)\?ver=[0-9.]+", r"/assets/project-stage/\1?ver=lab", html)
os.makedirs(out, exist_ok=True)
open(os.path.join(out, "index.html"), "w", encoding="utf-8", newline="\n").write(html)
print("lab page:", os.path.join(out, "index.html"), len(html), "bytes; assets:", dst)
