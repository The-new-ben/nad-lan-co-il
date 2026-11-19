# -*- coding: utf-8 -*-
"""make deploy719.py from deploy718.py: 1.72.719 = HAD-790 follow-up, Ben's order (20.11.2026, through the coordinator): put rentals
management in the home menu, in a fitting place (the only entry was a link in the third column of the rentals panel; he did not find it).
  SWAP inc/home-v3.php: a top-level item "ניהול השכרה" right after the "דירות להשכרה" panel, leading to /my-rentals/, on every width
       (desktop bar and phone sheet; the existing plain item markup, kept visible below 1360 px where the other plain item hides); inside
       the rentals panel the landlords' column moves first. English home: "Rental management" after its rentals panel, to
       /my-rentals/?lang=en (the only language whose rentals page opens in its own language; fr and ar fall back to Hebrew, ru to
       English, so they get nothing). No new URL, no redirect.
  Fit (measured, scripts/had790/header_fit_check.py --sim, 0 overlaps at 1080-1920 + phone): the "פרסום מודעה" bar button hides only
  at 1061-1279 px (it stays in the panels and the phone sheet), "נדל״ן בחו״ל" shows from 1441 px; type size unchanged. This also
  fixes the live overlap at 1080 ("אנשי מקצוע" ran into the language button)."""
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kl_release  # noqa: E402

PREV = 718
rp = json.load(open(os.path.join(kl_release.QA, "deploy-result-%d.json" % PREV), encoding="utf-8"))
assert str(rp.get("state", "")).startswith("released"), rp.get("state")
E = ['Fatal error', 'Warning</b>', 'Notice</b>']
K = 'class="nlhp-nav__item nlhp-nav__plain nlhp-nav__keep" href="https://nad-lan.co.il/my-rentals/">ניהול השכרה</a>'
O = ('<summary class="nlhp-nav__item">דירות להשכרה <span class="nlhp-caret" aria-hidden="true"></span></summary><div class="nlhp-mega">'
     '<div class="nlhp-mega__in"><div class="nlhp-mega__col"><p class="nlhp-mega__h">לבעלי דירות</p>')
C = '@media (max-width:1440px){.nlhp-nav__plain{display:none}.nlhp-nav__plain.nlhp-nav__keep{display:flex}}@media (min-width:1061px) and (max-width:1279px){#nlhp-top:not(.nlhp-top--lang) .nlhp-post{display:none}}'
KE = 'class="nlhp-nav__item nlhp-nav__plain nlhp-nav__keep" href="https://nad-lan.co.il/my-rentals/?lang=en">Rental management</a>'
NO = 'nlhp-nav__keep"'
ROWS = ("    ('/?t719a=1', [%r, %r, %r, '</details><a ' + %r], %r, []),\n"
        "    ('/projects/hamedina/?t719a=1', [%r, %r, %r], %r, []),\n"
        "    ('/mortgage-calculator/?t719a=1', [%r, %r, %r], %r, []),\n"
        "    ('/en/?t719a=1', [%r, %r], %r, []),\n"
        "    ('/fr/?t719a=1', ['nlhp-top--lang'], %r + [%r], []),\n"
        "    ('/ru/?t719a=1', ['nlhp-top--lang'], %r + [%r], []),\n"
        "    ('/ar/?t719a=1', ['nlhp-top--lang'], %r + [%r], []),\n") % (
    K, O, C, K, E, K, O, C, E, K, O, C, E, KE, C, E, E, NO, E, NO, E, NO)
kl_release.build_release(PREV, 719, ["inc/home-v3.php"], [], {}, {}, ROWS,
                         "rentals management in the site menu: a top-level item after the rentals panel, the landlords' column first",
                         "HAD-790 follow-up: rentals management in the menu")
