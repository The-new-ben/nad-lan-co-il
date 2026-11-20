# -*- coding: utf-8 -*-
"""make deploy720.py from deploy719.py: 1.72.720 = HAD-795 package 6, rentals legal wording part 2 (coordinator order 20.11.2026), text only,
he + en. Source of every change: docs/rentals/bom/text-release-719/CHANGES.md + hunks.json (each hunk proven to apply once on the LIVE text
fetched 20.11; audit docs/rentals/bom/legal-claims-audit.md).
  SWAP assets/rentals/i18n/he.json, en.json, lease.json, assets/rentals/help/he.html, en.html (v2, administrators only): the seven
       not-confirmed legal sentences (security return "60 days or when the debts are paid, whichever is later" s.25י(ה); the four cases a
       security may be realised s.25י(ג); option notices s.25יב; the no-contracting-out clause cites s.25יד(2); the screening tip says only
       what the Credit Data Law and the Criminal Information Law say) and the v2 copies of the four sentences fixed in 1.72.718.
  SWAP assets/rentals/guide/he.html, en.html and assets/instruments/tools/rentfair.js (one line); HUNK inc/rentals-manager.php:
       the 10% tax-track date is no longer printed (the Tax Authority's two pages disagree: 30 days after the year end / 31 January);
       the exemption ceiling is labelled with the year the Tax Authority guide states (2025) and "check the current ceiling".
No layout, no feature, nothing removed: the December-January tax reminder stays, without a date."""
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kl_release  # noqa: E402

PREV = 719
rp = json.load(open(os.path.join(kl_release.QA, "deploy-result-%d.json" % PREV), encoding="utf-8"))
assert str(rp.get("state", "")).startswith("released"), rp.get("state")
E = ['Fatal error', 'Warning</b>', 'Notice</b>']
R = "inc/rentals-manager.php"
HK = json.load(open(os.path.join(kl_release.H, "..", "..", "docs", "rentals", "bom", "text-release-719", "hunks.json"), encoding="utf-8"))
HUNKS = {R: [tuple(x) for x in HK["plugins/nadlan-config/" + R]]}
LIVE_MD5 = {R: "d474b7278e25814b4de6f584de33bd84"}
FILES = ["assets/rentals/i18n/he.json", "assets/rentals/i18n/en.json", "assets/rentals/i18n/lease.json", "assets/rentals/help/he.html",
         "assets/rentals/help/en.html", "assets/rentals/guide/he.html", "assets/rentals/guide/en.html", "assets/instruments/tools/rentfair.js"]
A = "/wp-content/plugins/nadlan-config/assets/"
ROWS = ("    ('/my-rentals/?t720a=1', ['אחרי סוף השנה מדווחים ומשלמים', 'לפי מדריך רשות המסים, התקרה לשנת 2025', 'אחרי סוף שנת המס, לדווח ולשלם'], %r, []),\n"
        "    ('/my-rentals/?lang=en&t720a=1', ['after the year ends, report and pay', 'after the end of the tax year, to report and pay'], %r, []),\n"
        "    (%r, ['לפי המאוחר', 'סעיפים 26 ו-27 לחוק נתוני אשראי', 'אם התקרה חלה על החוזה'], ['אסור למשוך דוח אשראי על אדם אחר', 'דיווח ותשלום עד {date}'], []),\n"
        "    (%r, ['whichever is later', 'sections 26 and 27'], ['Pulling a credit report on someone else is not allowed', 'report and pay by {date}'], []),\n"
        "    (%r, ['25יד(2)', 'whichever is later'], ['as the law requires'], []),\n"
        "    (%r, ['מדווחים ומשלמים אחרי סוף שנת המס'], ['d.tax.tenDue'], []),\n"
        "    ('/projects/rainbow-tel-aviv/?t720a=1', ['nlsh'], %r, []),\n"
        "    ('/projects/h-infinity-somail-tel-aviv/?t720a=1', [], %r, []),\n") % (
    E + ['30 בינואר במסלול', 'דיווח ותשלום עד'], E + ['January 30 on the 10 percent route', 'report and pay by'],
    A + "rentals/i18n/he.json", A + "rentals/i18n/en.json", A + "rentals/i18n/lease.json", A + "instruments/tools/rentfair.js", E, E)
kl_release.build_release(PREV, 720, FILES, [], HUNKS, LIVE_MD5, ROWS,
                         "rentals legal wording part 2: security return and realisation, option notices, the screening tip, no 10% tax-track date",
                         "HAD-795 package 6: rentals legal wording 2")
