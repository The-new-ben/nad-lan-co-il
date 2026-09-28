# -*- coding: utf-8 -*-
"""AreaLife v100: the eye height above the street on three floor bands of a project, from the live stage's own
floorHeight() (the stage's floor table, the same numbers the floor card and the view use). Writes
scripts/project-stage/data/eye-<project>.json.   python scripts/project-stage/measure_eyes.py dimri|ashira|duo"""
import io, json, os, sys, time
from playwright.sync_api import sync_playwright
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
P = {"dimri": ("dimri-yama-sde-dov", [10, 25, 36]), "ashira": ("ashira-sde-dov", [10, 22, 32]), "duo": ("duo-tel-aviv", [10, 25, 45])}
pk = sys.argv[1]
slug, bands = P[pk]
with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome")
    pg = b.new_page(viewport={"width": 1280, "height": 900})
    pg.goto("https://nad-lan.co.il/projects/%s/?eyes=1" % slug, wait_until="networkidle", timeout=120000)
    pg.evaluate("document.querySelector('#nlps') && document.querySelector('#nlps').scrollIntoView()")
    for _ in range(40):
        if pg.evaluate("!!(window.__nlpsStage && window.__nlpsStage.floorHeight)"):
            break
        pg.wait_for_timeout(500)
    eye = pg.evaluate("(bs)=>{const s=window.__nlpsStage;const o={};for(const f of bs){o[f]=s&&s.floorHeight?s.floorHeight(f):null}return o}", bands)
    b.close()
if not all(v for v in eye.values()):
    sys.exit("no floorHeight for %s: %s" % (pk, eye))
out = {"project": pk, "page": "/projects/%s/" % slug, "measured": time.strftime("%Y-%m-%d"), "source": "the live stage's floorHeight()", "eye": eye}
os.makedirs(os.path.join(REPO, "scripts", "project-stage", "data"), exist_ok=True)
io.open(os.path.join(REPO, "scripts", "project-stage", "data", "eye-%s.json" % pk), "w", encoding="utf-8").write(json.dumps(out, indent=1))
print(pk, eye)
