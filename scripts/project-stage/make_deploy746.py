# -*- coding: utf-8 -*-
"""make deploy746.py from deploy745.py: 1.72.746 = film loop cycle 2: the project row wraps on phones (board
https://claude.ai/artifact/VdA956RZtEthDSgziFSJTW, artboard Cycle1), so "שאלות של קונים" and the basket are never cut at the
screen's edge. SWAP assets/project-shell/shell.css (live read 20261122T202849Z = repo before the change)."""
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kl_release  # noqa: E402
PREV, NEW = 745, 746
rp = json.load(open(os.path.join(kl_release.QA, "deploy-result-%d.json" % PREV), encoding="utf-8"))
assert str(rp.get("state", "")).startswith("released"), rp.get("state")
A = "/wp-content/plugins/nadlan-config/assets/project-shell/"
ROWS = ("    ('%sshell.css?t746w=1', [':root body .nlsh{display:flex!important;flex-wrap:wrap;'], ['flex-wrap:nowrap'], []),\n"
        "    ('/projects/rainbow-tel-aviv/?t746w=1', ['class=\"nlsh\"', 'data-nlsh=\"ask\"'], ['Fatal error'], []),\n") % (A,)
kl_release.build_release(PREV, NEW, ["assets/project-shell/shell.css"], [], {}, {}, ROWS,
                         "the project row wraps on phones, every button in view", "film loop cycle 2: row wraps on phones")
