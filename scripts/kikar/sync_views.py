# -*- coding: utf-8 -*-
"""Copies the rendered window views (docs/research/2026-11-10-kikar-showcase/views/, scripts/interior/render_kikar_views.py) into
the plugin as WebP for the journey and the cockpit: hamedina/views/<T><floor>-<side>.webp (1280) and -640.webp, plus views.json
(the index with Blender's APARTMENT line, from which the true facing is read). Run it again as more views finish; then
scripts/kikar/sun_hours.mjs (optional) and scripts/kikar/build_cockpit_data.py.
  python scripts/kikar/sync_views.py"""
import json
import os
import shutil

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
SRC = os.path.join(REPO, "docs", "research", "2026-11-10-kikar-showcase", "views")
DST = os.path.join(REPO, "plugins", "nadlan-config", "assets", "project-stage", "hamedina", "views")
os.makedirs(DST, exist_ok=True)
idx = json.load(open(os.path.join(SRC, "views.json"), encoding="utf-8"))
n = 0
for k in idx:
    jpg = os.path.join(SRC, k + ".jpg")
    if not os.path.exists(jpg):
        continue
    big, small = os.path.join(DST, k + ".webp"), os.path.join(DST, k + "-640.webp")
    if not os.path.exists(big) or os.path.getmtime(big) < os.path.getmtime(jpg):
        im = Image.open(jpg).convert("RGB")
        im.save(big, "WEBP", quality=74, method=6)
        im.resize((640, 360), Image.LANCZOS).save(small, "WEBP", quality=72, method=6)
        n += 1
shutil.copyfile(os.path.join(SRC, "views.json"), os.path.join(DST, "views.json"))
tot = sum(os.path.getsize(os.path.join(DST, f)) for f in os.listdir(DST))
print(f"views: {len(idx)} in the index, {n} converted now, {len([f for f in os.listdir(DST) if f.endswith('-640.webp')])} in the plugin, {tot/1e6:.1f} MB")
