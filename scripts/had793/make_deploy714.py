# -*- coding: utf-8 -*-
"""HAD-793 follow-up, generates scripts/project-stage/deploy<new>.py: SWAP inc/page-lang.php only. The en/fr/ru article title and
headings get IBM Plex Sans with !important (the theme's heading rule outranked the 1.72.709 version, the H1 stayed in the Hebrew serif).
  python scripts/had793/make_deploy714.py [PREV NEW]   (default 713 714)"""
import hashlib, json, os, sys
H = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(H))
PS = os.path.join(REPO, "scripts", "project-stage"); sys.path.insert(0, PS)
import kl_release  # noqa: E402
PREV, NEW = (int(sys.argv[1]), int(sys.argv[2])) if len(sys.argv) > 2 else (713, 714)
rp = json.load(open(os.path.join(kl_release.QA, "deploy-result-%d.json" % PREV), encoding="utf-8"))
assert str(rp.get("state", "")).startswith("released"), rp.get("state")
F = "inc/page-lang.php"
assert hashlib.md5(open(os.path.join(REPO, "plugins", "nadlan-config", F), "rb").read()).hexdigest() == "b741af134e7a0a58f50a759754c6c742"
T = "t%dp" % NEW
RULE = 'font-family:"IBM Plex Sans",system-ui,-apple-system,"Segoe UI",sans-serif!important;font-weight:600!important'
ROWS = ("    ('/israel-mortgage-non-residents/?" + T + "=1', [" + repr(RULE) + ", '<meta name=\"author\" content=\"Ben Betesh\"', 'nlpg-toc'], ['Fatal error', 'Warning</b>', 'Notice</b>'], []),\n"
        "    ('/fr/mortgage-calculator/?" + T + "=1', ['<html lang=\"fr', 'Simulateur'], ['Fatal error', 'Warning</b>'], []),\n"
        "    ('/mortgage-calculator/?" + T + "=1', ['data-nli=\"mquick\"'], ['Fatal error', 'Warning</b>', 'id=\"nlpglang-latin\"'], []),\n")
kl_release.build_release(PREV, NEW, [F], [], {}, {}, ROWS,
                         "the English, French and Russian article title and headings in IBM Plex Sans (the theme rule no longer wins)",
                         "HAD-793 follow-up: article title font on en/fr/ru posts")
print("deploy%d.py written" % NEW)
