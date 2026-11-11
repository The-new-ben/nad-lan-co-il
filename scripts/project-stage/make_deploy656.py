# -*- coding: utf-8 -*-
"""make deploy656.py from deploy655.py (the designer's 1.72.655): 1.72.656 = HAD-712, the Hebrew Kikar page title.
Ben, 11.11.2026 evening (through the Kikar session): "מגדלי כיכר המדינה, פרויקט כיכר המדינה, מחירים, דירות, איכלוס, תוכניות, תנסה לדחוף את
תוכניות איכשהו, ותעשה את זה." One Yoast meta, _yoast_wpseo_title of post 8113, guarded by the md5 of the current text (the runner stops
before writing if the live value is anything else, for example Yoast variables); UNDO restores the old text. The share titles
(_yoast_wpseo_opengraph-title, _yoast_wpseo_twitter-title) are only read and reported. No file, no hunk; the H1, the address, the
meta description and the four language titles stay. Logic in kl_release.py (build_meta_only)."""
import json, os, sys
H = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, H)
import kl_release  # noqa: E402

PREV, NEWV = 655, 656
rp = json.load(open(os.path.join(kl_release.QA, "deploy-result-%d.json" % PREV), encoding="utf-8"))
assert str(rp.get("state", "")).startswith("released"), "1.72.%d must be released first (state: %s)" % (PREV, rp.get("state"))
OLD = "מגדלי כיכר המדינה תל אביב: מחירים, עסקאות, מפה ותלת ממד"
NEW = "מגדלי כיכר המדינה: פרויקט כיכר המדינה, מחירים, תוכניות דירות, אכלוס"
kl_release.build_meta_only(PREV, NEWV, None, rp["files"].get(kl_release.REL) or "unchanged since its last release",
                           yoast={"id": 8113, "key": "_yoast_wpseo_title", "before": OLD, "after": NEW, "path": "/projects/hamedina/",
                                  "peek": ["_yoast_wpseo_opengraph-title", "_yoast_wpseo_twitter-title"]},
                           msg="the Hebrew Kikar page title (Ben, 11.11.2026)")
