# -*- coding: utf-8 -*-
"""make deploy663.py from deploy662.py: 1.72.663 = HAD-712, the Kikar session's two gaps on 1.72.661 (12.11.2026):
  1. The showroom's own small map (step 2, "the view and the map") still had the blue wedge and only "Sea" / "North": it now draws
     the #C2563A cone of the other projects, names the places and landmarks of hamedina/details.json on the map (the beam's ones
     stand out), puts a chip at the map's edge for a landmark in the beam beyond it, and the line under it names them ("in the
     window's direction", never a promise of the view itself).
  2. View-with-details labels: measured as they render, a long name wraps at a space (never cut mid-word), the box stays inside the
     part of the panorama that is on screen (it follows the drag) and clear of the controls drawn over the picture; an old stem bug
     drew every label 40 px above the place it was checked at.
  Small: "tap a floor on the tower" comes back when the tower is dragged again after a pick.
  FILES  world/showroom.js, showroom.css, showroom-i18n.js, viewdetails.js, cockpit.js. No PHP, no new file.
Evidence: docs/research/2026-11-11-kikar-journey/evidence/map-663-test (the local files on the live pages, he/en/fr x 390/1440)."""
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kl_release  # noqa: E402

W = "assets/project-stage/world/"
FILES = [W + "showroom.js", W + "showroom.css", W + "showroom-i18n.js", W + "viewdetails.js", W + "cockpit.js"]
rp = json.load(open(os.path.join(kl_release.QA, "deploy-result-662.json"), encoding="utf-8"))
assert str(rp.get("state", "")).startswith("released"), rp.get("state")
assert not set(FILES) & set(rp.get("files") or {}), "1.72.662 wrote a file this release swaps"
ROWS = ("    ('/wp-content/plugins/nadlan-config/assets/project-stage/world/showroom.js?t663s=1', ['function mapLabels(from, b)', 'function windowNames(f, b)', 'S.rechoose = true'], [], []),\n"
        "    ('/wp-content/plugins/nadlan-config/assets/project-stage/world/showroom.css?t663s=1', ['.nlsr-beam{fill:rgba(194,86,58,.34);stroke:#C2563A', '.nlsr-pe{'], [], []),\n"
        "    ('/wp-content/plugins/nadlan-config/assets/project-stage/world/showroom-i18n.js?t663s=1', ['sr_map_window', 'In the window’s direction:'], [], []),\n"
        "    ('/wp-content/plugins/nadlan-config/assets/project-stage/world/viewdetails.js?t663s=1', ['q.y - box.b - 7', 'opt.avoid'], ['text-overflow:ellipsis'], []),\n"
        "    ('/wp-content/plugins/nadlan-config/assets/project-stage/world/cockpit.js?t663s=1', [\"avoid: '.nlck-subtop > *, .nlck-cap, .nlck-vdt'\"], [], []),\n"
        "    ('/projects/hamedina/?t663s=1', ['id=\"nlkm-cfg\"', 'journey.js?ver=1.72.663'], ['Fatal error', 'Warning</b>'], []),\n"
        "    ('/projects/hamedina-en/?t663s=1', ['id=\"nlkm-cfg\"', 'journey.js?ver=1.72.663'], ['Fatal error', 'Warning</b>'], []),\n")
kl_release.build_release(662, 663, FILES, [], {}, {}, ROWS,
                         "the Kikar small map with the #C2563A cone and named places, view-with-details labels kept inside the picture",
                         "the Kikar small map and the view labels")
