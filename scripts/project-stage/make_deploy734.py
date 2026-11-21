# -*- coding: utf-8 -*-
"""make deploy734.py from deploy733.py: 1.72.734 = HAD-795 package 6, "השכרות נדל״ן": one journey through the real screens.
Owner's orders of 20-21.11.2026 through the coordinator (decision A): a named product, understood at once, every function that exists
reachable from the opening press after press, on the sample portfolio; and two phone defects of 1.72.731 (1.72.732 and 1.72.733 are the forum session's releases, HAD-787).
THE OPENING (public /my-rentals/, he + en)
  SWAP inc/rentals/portfolio.php       the product's name and lockup in ONE place; one plain sentence; the example data is now the SAME
                                       nine apartments as the app's own sample (unit ids), so "enter the apartment" opens that apartment's
                                       real screens; a still globe with its marks as the first paint.
  SWAP assets/rentals/portfolio/pf.js  name labels on every mark; "enter the apartment" link; phones: the sentence under the filter.
  SWAP assets/rentals/portfolio/pf.css the still globe, the lockup, pictures on the three steps (the number is a tag on the picture), phones.
  NEW  assets/rentals/portfolio/img/poster-{he,en}-{desk,phone}.webp  the still globes (about 32 KB each).
  HUNK inc/rentals-manager.php         the landing prints the lockup and the sentence above the stage and its long paragraph, word for
                                       word, below it; the address ?sample=1 opens the example portfolio in the real screens; a new value
                                       'new' of the option nadlan_rentals_v2 (NOT set by this release).
THE TOUR (/my-rentals/?sample=1, anyone; nothing is saved, nothing is sent)
  SWAP inc/rentals/page.php            the sample mode: the bar, the app on the sample data with the new day screen; the brand in the
                                       app's title and above its h1; the lease-text maker open to administrators only.
  NEW  assets/rentals/rm-tour.js       the bar that walks the app's own screens: today, tenant, rent and payments, index update, lease and
                                       securities, repairs, documents, tax estimate, all properties, start with my own.
  SWAP assets/rentals/rm-demo.js       the sample portfolio: Kikar HaMedina (two example apartments), Arlozorov (two), Florentin, Eilat,
                                       Limassol, Athens, New York; the sample's index numbers add up; Hebrew repair text in the Hebrew sample.
  SWAP assets/rentals/rm-boot.js       the visitor's sample mounts the day screen; brand and maker flag passed on; two buyer events.
  SWAP assets/rentals/rm-views.js      the app's top bar shows the product's name.
  SWAP assets/rentals/rm-drawers.js    open-without-a-lawyer list: only what the statute names is compared with the cap (a security cheque
                                       and a note stay as their own lines); the signing card and the lease text are shown where the maker is open.
  SWAP assets/rentals/rm-today.css     a short day screen keeps its tabs at the bottom.
  SWAP assets/rentals/i18n/he.json, en.json  the screening tip keeps what a landlord may do and the two "do not" sentences.
NOT in this release: the switch of new sign-ups to version 2 (option nadlan_rentals_v2 stays 'admin'); plans and prices stay off.
Lab: lab_pf.py, lab_tour.py, lab_sample_people.py, lab_slice1*.py (headless, not a real phone)."""
import os, sys, json, hashlib, glob
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kl_release  # noqa: E402

PREV = 733
rp = json.load(open(os.path.join(kl_release.QA, "deploy-result-%d.json" % PREV), encoding="utf-8"))
assert str(rp.get("state", "")).startswith("released"), rp.get("state")
E = ['Fatal error', 'Warning</b>', 'Notice</b>']
POSTERS = ["assets/rentals/portfolio/img/poster-%s-%s.webp" % (l, d) for l in ("he", "en") for d in ("desk", "phone")]
NEW = ["assets/rentals/rm-tour.js"] + POSTERS
FILES = NEW + ["inc/rentals/portfolio.php", "inc/rentals/page.php", "assets/rentals/portfolio/pf.js", "assets/rentals/portfolio/pf.css",
               "assets/rentals/rm-demo.js", "assets/rentals/rm-boot.js", "assets/rentals/rm-views.js", "assets/rentals/rm-drawers.js",
               "assets/rentals/rm-today.css", "assets/rentals/i18n/he.json", "assets/rentals/i18n/en.json"]
R = "inc/rentals-manager.php"
H = [
    # the address ?sample=1: the example portfolio in the real screens
    ("\tif ( nadlan_rm_v2() ) {\n\t\tnlrm_maybe_install();",
     "\t/* the tour of the example portfolio (HAD-795, 1.72.734): the app's real screens on the sample data, for anyone; nothing is saved */\n"
     "\tif ( isset( $_GET['sample'] ) && function_exists( 'nlrm_render_page' ) && function_exists( 'nlrm_lang' ) ) { // phpcs:ignore\n"
     "\t\tnlrm_render_page( 'sample', nlrm_lang() );\n"
     "\t\texit;\n"
     "\t}\n"
     "\tif ( nadlan_rm_v2() ) {\n\t\tnlrm_maybe_install();"),
    # a new value of the option: everyone gets version 2 except a landlord who already keeps properties in version 1
    ("\t\tif ( '1' === $mode ) { return true; }\n",
     "\t\tif ( '1' === $mode ) { return true; }\n"
     "\t\tif ( 'new' === $mode ) {\n"
     "\t\t\t/* 1.72.734: new sign-ups get version 2; a landlord who already keeps properties in version 1 keeps what he has;\n"
     "\t\t\t   a visitor sees the public page with the 3D opening */\n"
     "\t\t\tif ( current_user_can( 'manage_options' ) ) { return true; }\n"
     "\t\t\tif ( isset( $_GET['l'] ) && ! is_user_logged_in() && did_action( 'template_redirect' ) ) { return true; } // phpcs:ignore\n"
     "\t\t\tif ( ! is_user_logged_in() ) { return false; }\n"
     "\t\t\tif ( in_array( get_current_user_id(), array_map( 'intval', (array) get_option( 'nadlan_rentals_v2_pilot', array() ) ), true ) ) { return true; }\n"
     "\t\t\treturn ! ( function_exists( 'nadlan_rm_my_props' ) && nadlan_rm_my_props() );\n"
     "\t\t}\n"),
    # the landing: lockup, one sentence, the long paragraph under the stage
    ("\t<header class=\"nlrm-hero\">\n\t\t<p class=\"nlrm-kicker\">",
     "\t<?php if ( ! function_exists( 'nadlan_rm_portfolio_stage' ) && is_readable( __DIR__ . '/rentals/portfolio.php' ) ) { include_once __DIR__ . '/rentals/portfolio.php'; } ?>\n"
     "\t<header class=\"nlrm-hero\">\n"
     "\t\t<?php if ( function_exists( 'nadlan_rm_lockup' ) ) { echo nadlan_rm_lockup( $en ? 'en' : 'he' ); } // phpcs:ignore ?>\n"
     "\t\t<p class=\"nlrm-kicker\">"),
    ("\t\t<p class=\"sub\">",
     "\t\t<?php if ( function_exists( 'nadlan_rm_one_line' ) ) { echo '<p class=\"nlrm-one\">' . esc_html( nadlan_rm_one_line( $en ? 'en' : 'he' ) ) . '</p>'; } ob_start(); ?>\n"
     "\t\t<p class=\"sub\">"),
    ("; ?></p>\n\t</header>\n\t<?php\n\t/* the opening (HAD-795, 20.11.2026)",
     "; ?></p>\n"
     "\t\t<?php $nlrm_sub = (string) ob_get_clean(); if ( ! function_exists( 'nadlan_rm_one_line' ) ) { echo $nlrm_sub; $nlrm_sub = ''; } // phpcs:ignore ?>\n"
     "\t</header>\n\t<?php\n\t/* the opening (HAD-795, 20.11.2026)"),
    ("nadlan_rm_portfolio_stage( $en ? 'en' : 'he', is_user_logged_in() ? '#nlrm-new' : wp_login_url( $self ) ); }",
     "nadlan_rm_portfolio_stage( $en ? 'en' : 'he', is_user_logged_in() ? '#nlrm-new' : wp_login_url( $self ), home_url( '/my-rentals/?sample=1' . ( $en ? '&lang=en' : '' ) ) ); }"),
    ("\t<header class=\"nlrm-hero nlrm-hero--after\">\n\t\t<div class=\"nlrm-ctas\">",
     "\t<header class=\"nlrm-hero nlrm-hero--after\">\n"
     "\t\t<?php echo $nlrm_sub; // the page's own paragraph, word for word, under the stage. phpcs:ignore ?>\n"
     "\t\t<div class=\"nlrm-ctas\">"),
]
LIVE_MD5 = {R: hashlib.md5(open(os.path.join(kl_release.PLUG, *R.split("/")), "rb").read()).hexdigest()}
A = "/wp-content/plugins/nadlan-config/assets/rentals/"
T = "?t734a=1"
ROWS = ("    (%r, ['function layoutTurn', 'function fitPhone', 'nlpf-nm', 'data-enter'], [], []),\n"
        "    (%r, ['#nlpf .nlpf-poster', '.nlrm .nlrm-lk', 'img/k1-720.webp'], [], []),\n"
        "    (%r, [], [], []),\n"
        "    (%r, ['NLRMTour', 'nlrm-touring'], [], []),\n"
        "    (%r, ['Kikar HaMedina', 'Limassol', 'id: 71'], ['9725', '@example'], []),\n"
        "    (%r, ['N.mountToday(root, { urls: cfg.urls, today2: true })', 'rent_property_add'], [], []),\n"
        "    (%r, ['leaseMaker', 'tot = (sec.deposit || 0)'], ['(sec.cheque || 0) + (sec.deposit || 0)'], []),\n"
        "    ('/my-rentals/?t734a=1', ['id=\"nlpf\" class=\"nlmyrent-stage\"', 'class=\"nlrm-lk\"', 'class=\"nlrm-one\"', 'nlpf-poster', 'poster-he-phone.webp', 'sample=1', 'data-pf=', 'תיק לדוגמה', 'הנכסים', 'לפי מדריך רשות המסים, התקרה לשנת 2025', 'מוסיפים נכס, מסמנים את הדירות שלכם על מודל תלת-ממדי'], %r, []),\n"
        "    ('/my-rentals/?lang=en&t734a=1', ['id=\"nlpf\" class=\"nlmyrent-stage\"', 'class=\"nlrm-one\"', 'poster-en-desk.webp', 'Example portfolio', 'check the current ceiling'], %r, []),\n"
        "    ('/my-rentals/?sample=1&u=21&t734a=1', ['id=\"nlrm-tour\"', 'data-unit=\"21\"', 'rm-tour.js', 'id=\"nlrm-root\" data-mode=\"demo\"', '\"mode\":\"sample\"', '\"today2\":true', 'rel=\"canonical\" href=\"https://nad-lan.co.il/my-rentals/\"'], %r, []),\n"
        "    ('/my-rentals/?sample=1&lang=en&t734a=1', ['id=\"nlrm-tour\"', 'Example portfolio', 'rm-tour.js'], %r, []),\n"
        "    ('/wp-json/nadlan/v1/health?t734a=1', ['\"status\":\"ok\"'], %r, []),\n"
        "    ('/projects/rainbow-tel-aviv/?t734a=1', ['nlsh'], %r, []),\n"
        "    ('/projects/h-infinity-somail-tel-aviv/?t734a=1', [], %r, []),\n") % (
    A + "portfolio/pf.js" + T, A + "portfolio/pf.css" + T, A + "portfolio/img/poster-he-phone.webp" + T, A + "rm-tour.js" + T, A + "rm-demo.js" + T,
    A + "rm-boot.js" + T, A + "rm-drawers.js" + T, E, E, E, E, E, E, E)
kl_release.build_release(PREV, 734, FILES, NEW, {R: H}, LIVE_MD5, ROWS,
                         "rentals: the product 'השכרות נדל״ן': one journey from the 3D opening through the real screens on the sample portfolio; a still globe at first paint",
                         "HAD-795 package 6: the journey")

# inherited rows that this release changes on purpose: 1.72.728 asked rm-demo.js for the old name pattern; the page rows of 729-731 stay true
_p = os.path.join(kl_release.H, "deploy734.py")
_s = open(_p, encoding="utf-8").read()
print("inherited rows naming rm-demo.js:", _s.count("rm-demo.js?t728a"), "| rm-boot row of 728:", _s.count("rm-boot.js?t728a"))
