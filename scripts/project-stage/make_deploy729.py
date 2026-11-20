# -*- coding: utf-8 -*-
"""make deploy729.py from deploy728.py: 1.72.729 = HAD-795 package 6, the 3D opening of the PUBLIC /my-rentals/ (owner's word 20.11.2026
evening through the coordinator; design board 5). For a visitor, straight under the h1 and the answer paragraph: the example landlord's
portfolio on a 3D map (two apartments in a tower by Kikar HaMedina, two more in Tel Aviv, Eilat, Limassol, Athens, New York).
  NEW  inc/rentals/portfolio.php            the example data (he, en) and the server-rendered stage; everything marked as an example.
  NEW  assets/rentals/portfolio/pf.js       the map (Mapbox GL 3.14.0 as on the compound pages, globe, our colours), marks with pictures and
                                            state, the filter, the flight to a building in 3D with its floors, the building panel (the Kikar
                                            tower is the HAD-712 render, loaded read-only, turning under the finger), the apartment's card.
  NEW  assets/rentals/portfolio/pf.css      the stage and the hero and steps around it, redrawn in the showroom language (no text removed).
  NEW  assets/rentals/portfolio/img/*.webp  21 small pictures (7 buildings in two sizes, 7 parts of a home); illustrations, labelled.
  SWAP assets/rentals/rental-manager.js     the old demo waits for the stage's load of the map library instead of loading it twice.
  HUNK inc/rentals-manager.php              the landing prints the stage after the paragraph; the hero buttons follow it.
Not touched: HAD-712 files, the beam, engine.js, version 2 (administrators only), plans and prices (off), robots and redirects.
No wheel or touch capture: cooperative gestures. Lab: scripts/rentals/lab_pf.py 88/88 (he, en; 1280x800 and 390x664; Chrome, not a real phone)."""
import os, sys, json, hashlib, glob
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kl_release  # noqa: E402

PREV = 728
rp = json.load(open(os.path.join(kl_release.QA, "deploy-result-%d.json" % PREV), encoding="utf-8"))
assert str(rp.get("state", "")).startswith("released"), rp.get("state")
E = ['Fatal error', 'Warning</b>', 'Notice</b>']
IMGS = sorted("assets/rentals/portfolio/img/" + os.path.basename(f) for f in glob.glob(os.path.join(kl_release.PLUG, "assets", "rentals", "portfolio", "img", "*.webp")))
assert len(IMGS) == 21, len(IMGS)
NEW = ["inc/rentals/portfolio.php", "assets/rentals/portfolio/pf.js", "assets/rentals/portfolio/pf.css"] + IMGS
FILES = NEW + ["assets/rentals/rental-manager.js"]
R = "inc/rentals-manager.php"
H = [
    ("\t\t<div class=\"nlrm-ctas\">\n",
     "\t</header>\n"
     "\t<?php\n"
     "\t/* the opening (HAD-795, 20.11.2026): the example landlord's portfolio on a 3D map, right under the answer paragraph.\n"
     "\t   The file is included here so that a rollback which removes it simply prints nothing. */\n"
     "\tif ( ! function_exists( 'nadlan_rm_portfolio_stage' ) && is_readable( __DIR__ . '/rentals/portfolio.php' ) ) { include_once __DIR__ . '/rentals/portfolio.php'; }\n"
     "\tif ( function_exists( 'nadlan_rm_portfolio_stage' ) ) { nadlan_rm_portfolio_stage( $en ? 'en' : 'he', is_user_logged_in() ? '#nlrm-new' : wp_login_url( $self ) ); }\n"
     "\t?>\n"
     "\t<header class=\"nlrm-hero nlrm-hero--after\">\n"
     "\t\t<div class=\"nlrm-ctas\">\n"),
]
LIVE_MD5 = {R: hashlib.md5(open(os.path.join(kl_release.PLUG, *R.split("/")), "rb").read()).hexdigest()}
A = "/wp-content/plugins/nadlan-config/assets/rentals/"
T = "?t729a=1"
ROWS = ("    (%r, ['function layoutTurn', 'nlpf-own', 'cooperativeGestures: true'], [], []),\n"
        "    (%r, ['#nlpf .nlpf-panel', '.nlrm .nlrm-hero--after'], [], []),\n"
        "    (%r, [], [], []),\n"
        "    (%r, ['__nlMbx', 'nlu-wademo'], [], []),\n"
        "    ('/my-rentals/?t729a=1', ['id=\"nlpf\"', 'data-pf=', 'תיק לדוגמה', 'nlrm-hero--after', 'portfolio/pf.js', 'הנכסים', 'לפי מדריך רשות המסים, התקרה לשנת 2025'], %r, []),\n"
        "    ('/my-rentals/?lang=en&t729a=1', ['id=\"nlpf\"', 'Example portfolio', 'check the current ceiling'], %r, []),\n"
        "    ('/wp-json/nadlan/v1/rental-demo?t729a=1', ['\"props\"', '\"tenant_phone\":\"\"'], ['97250000', 'Fatal error'], []),\n"
        "    ('/wp-json/nadlan/v1/health?t729a=1', ['\"status\":\"ok\"'], %r, []),\n"
        "    ('/projects/rainbow-tel-aviv/?t729a=1', ['nlsh'], %r, []),\n"
        "    ('/projects/h-infinity-somail-tel-aviv/?t729a=1', [], %r, []),\n") % (
    A + "portfolio/pf.js" + T, A + "portfolio/pf.css" + T, A + "portfolio/img/k1-192.webp" + T, A + "rental-manager.js" + T, E, E, E, E, E)
kl_release.build_release(PREV, 729, FILES, NEW, {R: H}, LIVE_MD5, ROWS,
                         "rentals: the 3D opening of the public page (the example portfolio on a 3D map, buildings and apartments pressable)",
                         "HAD-795 package 6: the 3D opening of /my-rentals/")
