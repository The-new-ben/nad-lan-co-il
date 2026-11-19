# -*- coding: utf-8 -*-
"""make deploy<N>.py: HAD-792 package 2 follow-up (assets only): on a phone the line "the view in the window is an illustration"
moves above the walk row instead of hiding behind it (designer.css), and the designer page is rebuilt for the version so the
browser fetches the new stylesheet.   python make_deploy713.py [PREV NEW]   (default 712 713)"""
import os, sys, json, subprocess
H = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, H)
import kl_release  # noqa: E402
PREV, NEWV = (int(sys.argv[1]), int(sys.argv[2])) if len(sys.argv) > 2 else (712, 713)
rp = json.load(open(os.path.join(kl_release.QA, "deploy-result-%d.json" % PREV), encoding="utf-8"))
assert str(rp.get("state", "")).startswith("released"), rp.get("state")
REPO = os.path.dirname(os.path.dirname(H))
o = subprocess.run([sys.executable, os.path.join(REPO, "docs", "tools", "design-studio", "build_tour.py"), "1.72.%d" % NEWV, "roomscan.js", "roomgeom.js"], capture_output=True, text=True, encoding="utf-8", errors="replace")
assert o.returncode == 0, o.stdout + o.stderr
print("[tour]", o.stdout.strip())
A = "/wp-content/plugins/nadlan-config/assets/designer/"
T = "t%dd" % NEWV
ROWS = ("    ('/tour/designer/?project=ashira&" + T + "=1', ['walknav.js?v=', 'NL_TRAIL_CFG'], ['Fatal error'], []),\n"
        "    ('" + A + "designer.css?" + T + "=1', ['.space:has(.walkbar:not([hidden])) .note'], [], []),\n"
        "    ('/projects/hamedina/?" + T + "=1', ['class=\"nlsh\"'], ['Fatal error'], []),\n")
# Carried for package 3 (its request 19.11; live text was 8e1e19d9 from 711, repo fix 7384d405): inc/project-shell.php places the
# project row (call, designer, basket) inside the buttons block on pages with no hero-pick anchor (the five Kikar world pages).
SHELL = "inc/project-shell.php"
import hashlib  # noqa: E402
assert hashlib.md5(open(os.path.join(REPO, "plugins", "nadlan-config", SHELL), "rb").read()).hexdigest() == "7384d40519896d9b254a8526418af8bb"
kl_release.build_release(PREV, NEWV, ["assets/tours/designer-tour.html", "assets/designer/designer.css", SHELL], [], {}, {}, ROWS,
                         "the window-view illustration line stays visible above the walk row on phones",
                         "HAD-792 package 2 follow-up: illustration line on phones (+ package 3 project row inside the buttons block)")
