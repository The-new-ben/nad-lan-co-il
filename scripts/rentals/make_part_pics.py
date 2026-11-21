# -*- coding: utf-8 -*-
"""The home-part pictures of the rentals product (HAD-795): one studio picture per part kind, the same family as the opening card.
Source: D:\Media\nad-lan\rentals-pictures\raw\p-<kind>.png (made one at a time in ChatGPT image generation; the prompt is in
docs/rentals/build/parts/PROMPT.md). Output: plugins/nadlan-config/assets/rentals/portfolio/img/p-<kind>-192.webp.
Usage: python scripts/rentals/make_part_pics.py dishwasher heater shutter gas"""
import os, sys
from PIL import Image
RAW = r"D:\Media\nad-lan\rentals-pictures\raw"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "plugins", "nadlan-config", "assets", "rentals", "portfolio", "img")
for k in sys.argv[1:]:
    im = Image.open(os.path.join(RAW, "p-%s.png" % k)).convert("RGB")
    s = min(im.size); l = (im.width - s) // 2; t = (im.height - s) // 2
    im = im.crop((l, t, l + s, t + s)).resize((192, 192), Image.LANCZOS)
    p = os.path.join(OUT, "p-%s-192.webp" % k)
    im.save(p, "WEBP", quality=72, method=6)
    print(k, os.path.getsize(p))
