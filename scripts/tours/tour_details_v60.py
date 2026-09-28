# -*- coding: utf-8 -*-
"""The quarter tours' details (1.72.314, design system TourPhone v60).

- The time machine speaks English: its buttons ("היום 2026" / "הרובע 2035") had no strings in the tours' translation
  tables, so English mode kept them in Hebrew. New strings yearNow / yearQ in both languages, wired through I18N_HTML.
  Sde Dov: "Today / The quarter"; Somail (its English pages call it the compound): "Today / The compound".
- On phones the free walk's mini map moves up to 196px (under the free-tour button, which ends at 187px since release
  313) and the help box ("גררו כדי להביט…") sits below it from 406px instead of in the screen's centre, over the map.

Edits experience/{sde-dov,somail}/index.html and copies each to plugins/nadlan-config/assets/tours/{slug}-tour.html.

    python scripts/tours/tour_details_v60.py
"""
import io, os
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
Q_EN = {"sde-dov": "The quarter", "somail": "The compound"}
for slug in ("sde-dov", "somail"):
    src = os.path.join(ROOT, "experience", slug, "index.html")
    s = io.open(src, encoding="utf-8", newline="").read()
    if "yearNow:" in s:
        print(slug, "already has v60"); continue

    pairs = [
        ("helpMob: 'גררו", "yearNow: 'היום<small>2026</small>', yearQ: 'הרובע<small>2035</small>',\n    helpMob: 'גררו"),
        ("helpMob: 'Drag", "yearNow: 'Today<small>2026</small>', yearQ: '%s<small>2035</small>',\n    helpMob: 'Drag" % Q_EN[slug]),
        ("I18N_HTML = [", "I18N_HTML = [\n  ['#year2026', 'yearNow'], ['#year2035', 'yearQ'],"),
        ("#mmWrap{left:10px;bottom:auto;top:calc(232px + env(safe-area-inset-top));padding:7px 7px 6px}",
         "#mmWrap{left:10px;bottom:auto;top:calc(196px + env(safe-area-inset-top));padding:7px 7px 6px} /* v60: under the free-tour button (ends at 187px since v59) */\n"
         "    #exHelp{top:calc(406px + env(safe-area-inset-top));left:12px;right:12px;transform:none;margin-inline:auto;width:max-content;max-width:calc(100vw - 24px);text-wrap:balance} /* v60: the help box below the mini map (it was centred on the screen, over the map, and only half the screen wide: five lines), full width in balanced lines */"),
    ]
    for a, b in pairs:
        c = s.count(a)
        assert c == 1, (slug, c, a[:60])
        s = s.replace(a, b, 1)
        print(slug, "ok", a[:50])
    io.open(src, "w", encoding="utf-8", newline="").write(s)
    io.open(os.path.join(ROOT, "plugins", "nadlan-config", "assets", "tours", slug + "-tour.html"), "w", encoding="utf-8", newline="").write(s)
    print(slug, "written", len(s.encode("utf-8")))
