# -*- coding: utf-8 -*-
import json, sys, os
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))

JS_STAGE_CONFIG = """() => {
    return {
        nlps: typeof window.nlps !== 'undefined' ? Object.keys(window.nlps) : null,
        nlpsConfig: window.NLPS_CONFIG || window.nlpsConfig || window.nadlanStage || null,
        stageData: window.__NLPS_DATA__ || null,
        scripts: Array.from(document.querySelectorAll('script')).map(s => s.src || s.innerText.slice(0, 100)).filter(s => s.includes('stage') || s.includes('nlps') || s.includes('project'))
    };
}"""

with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome", args=["--use-gl=angle", "--use-angle=swiftshader", "--enable-unsafe-swiftshader"])
    for key, url in [("A", "https://nad-lan.co.il/projects/ashira-sde-dov/"), ("B", "https://nad-lan.co.il/projects/rainbow-tel-aviv/")]:
        ctx = b.new_context(viewport={"width": 1440, "height": 900}, locale="he-IL")
        pg = ctx.new_page()
        pg.goto(url, wait_until="load", timeout=90000)
        pg.wait_for_timeout(5000)
        res = pg.evaluate(JS_STAGE_CONFIG)
        print(f"=== {key} ({url}) ===")
        print("nlps:", res['nlps'])
        print("nlpsConfig:", res['nlpsConfig'])
        print("stageData:", res['stageData'])
        print("scripts:", res['scripts'][:10])
        ctx.close()
    b.close()
