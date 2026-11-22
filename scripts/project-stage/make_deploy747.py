# -*- coding: utf-8 -*-
"""make deploy747.py from deploy746.py: 1.72.747 = film loop cycle 3: from the project to renting the apartment out after
handover (board https://claude.ai/artifact/VdA956RZtEthDSgziFSJTW, artboard Cycle3). World reference: the rent estimate and
"rent it out" path on a Zillow home page, which ties buying to the owner's later rental. SWAP inc/project-shell.php: the
project row gets "השכרה אחרי המסירה" -> /my-rentals/ on Hebrew pages and "Rent it out after handover" -> /my-rentals/?lang=en on
English pages (the rentals product speaks Hebrew and English; fr/ru/ar keep their row). The site never rents out and is never a
broker; the link leads to the owner's own rentals tool."""
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kl_release  # noqa: E402
PREV, NEW = 746, 747
rp = json.load(open(os.path.join(kl_release.QA, "deploy-result-%d.json" % PREV), encoding="utf-8"))
assert str(rp.get("state", "")).startswith("released"), rp.get("state")
BAD = "['Fatal error', 'Warning</b>', 'Notice</b>']"
ROWS = ("    ('/projects/rainbow-tel-aviv/?t747r=1', ['data-nlsh=\"rent\"', 'השכרה אחרי המסירה', 'data-nlsh=\"ask\"', 'id=\"nlps\"'], %s, []),\n"
        "    ('/projects/rainbow-tel-aviv-en/?t747r=1', ['data-nlsh=\"rent\"', 'Rent it out after handover', 'my-rentals/?lang=en'], %s, []),\n"
        "    ('/projects/duo-tel-aviv-fr/?t747r=1', ['class=\"nlsh\"'], ['data-nlsh=\"rent\"', 'Fatal error'], []),\n"
        "    ('/projects/hamedina/?t747r=1', ['class=\"nlsh\"', 'data-nlsh=\"rent\"'], %s, []),\n"
        "    ('/projects/einstein-tower/?t747r=1', ['data-nlsh=\"rent\"', 'nadlan-einstein-he-dossier-v1'], %s, []),\n") % (BAD, BAD, BAD, BAD)
kl_release.build_release(PREV, NEW, ["inc/project-shell.php"], [], {}, {}, ROWS,
                         "rent it out after handover, from every project row (Hebrew and English)",
                         "film loop cycle 3: project to rentals")
