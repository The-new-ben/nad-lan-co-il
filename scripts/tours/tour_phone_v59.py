# -*- coding: utf-8 -*-
"""The quarter tours' phone top bar and the guide button (1.72.313, design system TourPhone v59).

Adds scripts/tours/tour-phone-v59.css as <style id="tour-phone-v59"> before </head> in experience/{sde-dov,somail}/index.html
and copies each result to plugins/nadlan-config/assets/tours/{slug}-tour.html (served first by inc/tour-routes.php).

    python scripts/tours/tour_phone_v59.py
"""
import io, os
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
CSS = io.open(os.path.join(ROOT, "scripts", "tours", "tour-phone-v59.css"), encoding="utf-8").read().strip()
for slug in ("sde-dov", "somail"):
    src = os.path.join(ROOT, "experience", slug, "index.html")
    s = io.open(src, encoding="utf-8", newline="").read()
    if 'id="tour-phone-v59"' in s:
        print(slug, "already has v59"); continue
    assert s.count("</head>") == 1, slug
    s = s.replace("</head>", '<style id="tour-phone-v59">\n' + CSS + "\n</style>\n</head>")
    io.open(src, "w", encoding="utf-8", newline="").write(s)
    io.open(os.path.join(ROOT, "plugins", "nadlan-config", "assets", "tours", slug + "-tour.html"), "w", encoding="utf-8", newline="").write(s)
    print(slug, "ok", len(s.encode("utf-8")))
