# -*- coding: utf-8 -*-
"""make deploy744.py from deploy743.py: 1.72.744 = HAD-801, the entries to the new Sde Dov 2036 tour (Codex's build, owner-approved).
The tour itself is a folder at <site root>/tour/sde-dov/ (scripts/had801/tour_ship.py), outside the plugin; this release only adds the
ways in, on the LIVE texts read 22.11.2026 (docs/qa/live-read/20261122T163736Z):
  - NEW assets/quarter-walk/: Codex's packaged WordPress entry ([nadlan_walk]: a still from the tour, the sign, three stops, the
    "places and sources" list; the engine loads only after a press, inside a dialog on the same page). Copied byte-for-byte from
    sde-dov-2036/.local-tools/wordpress/site/wp-content/plugins/nadlan-quarter-walk.
  - inc/sdedov-teaser.php: (a) /sde-dov/ gets the entry right after the opening paragraph and its buttons (before the picture and
    the area map, which stay); (b) a slow drift on the entry's picture so it moves by itself, a still for reduced motion;
    (c) the old band's words say what the new tour has; (d) project deep links go to the project's own plot in the new tour
    (#p=lot-...), for all ten projects the tour links to our pages.
  - inc/home-v3.php: the home tour card shows the new tour's picture (lazy, low priority) and its words."""
import os, sys, json, hashlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kl_release  # noqa: E402

PREV, NEW = 743, 744
rp = json.load(open(os.path.join(kl_release.QA, "deploy-result-%d.json" % PREV), encoding="utf-8"))
assert str(rp.get("state", "")).startswith("released"), rp.get("state")
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
LR = os.path.join(REPO, "docs", "qa", "live-read", "20261122T163736Z", "inc")
LIVE = {r: open(os.path.join(LR, r.split("/")[1]), encoding="utf-8").read() for r in ("inc/sdedov-teaser.php", "inc/home-v3.php")}
MD5 = {r: hashlib.md5(t.encode("utf-8")).hexdigest() for r, t in LIVE.items()}
assert MD5["inc/sdedov-teaser.php"].startswith("99aebd0284") and MD5["inc/home-v3.php"].startswith("297293bb28"), MD5

T = []
T.append(("\t$map = array( 'rainbow-tel-aviv' => 'rainbow', 'ashira-sde-dov' => 'ashira', 'dimri-yama-sde-dov' => 'dimri' );",
          "\t/* 1.72.744: the new tour (Sde Dov 2036) opens on a place by its id: each project's own plot */\n"
          "\t$map = array( 'ashira-sde-dov' => 'lot-eshkol-101', 'utopia-sde-dov' => 'lot-eshkol-103', 'dimri-yama-sde-dov' => 'lot-eshkol-107',\n"
          "\t\t'shikun-binui-sde-dov' => 'lot-eshkol-109', 'zohi-sde-dov' => 'lot-eshkol-110', 'rainbow-tel-aviv' => 'lot-eshkol-111',\n"
          "\t\t'gindi-vogue-sde-dov' => 'lot-merkaz-2206', 'first-sde-dov' => 'lot-merkaz-2270', 'migdalei-hayam-sde-dov' => 'lot-tzafon-150' );"))
T.append(("$url   = nadlan_sdedov_tour_url() . ( $focus ? '?focus=' . rawurlencode( $focus ) . '&mode=explore' : '' );",
          "$url   = nadlan_sdedov_tour_url() . ( $focus ? '#p=' . rawurlencode( $focus ) : '' );"))
T.append(("$link = $focus ? $url . '?focus=' . rawurlencode( $focus ) . '&mode=explore' : $url;",
          "$link = $focus ? $url . '#p=' . rawurlencode( $focus ) : $url;"))
T.append(("<p class=\"nlsdt-kick\">חדש · סיור תלת ממדי חי</p>", "<p class=\"nlsdt-kick\">חדש · שדה דב 2036, הליכה ברובע</p>"))
T.append(("'הפרויקט הזה הוא חלק מרובע שלם שקם על קו החוף. מסתובבים ברחובות של 2035, עוברים בין המגדלים, ורואים איך הכול מתחבר.'",
          "'הפרויקט הזה הוא חלק מרובע שלם שקם על קו החוף. הולכים ברחובות הרובע לפי התכנית, מגיעים אל המגרש של הפרויקט ורואים מי בונה מסביב.'"))
T.append(("'מסתובבים ברחובות הרובע של 2035, עוברים בין המגדלים, יורדים לטיילת, ובוחרים דירה מתוך הבניין. הדמיה חיה בדפדפן, בלי להוריד כלום.'",
          "'הולכים ברחובות הרובע לפי התכנית, מצומת אבן גבירול ואיינשטיין ועד הים, ורואים מי בונה בכל מגרש. הדמיה חיה בדפדפן, בלי להוריד כלום.'"))
T.append(("<li>מכונת זמן 2026 ⇄ 2035</li><li>סיור חופשי עם חצים</li><li>כל בניין לחיץ</li>",
          "<li>מאבן גבירול עד הים</li><li>שמות הפרויקטים והיזמים</li><li>כל מקום עם מקור ותאריך</li>"))
CSS = ("\n\t\t// 1.72.744 (HAD-801): the walk entry moves by itself (a slow drift on its picture), a still for reduced motion; the skin's\n"
       "\t\t// forced heading and link colours must not reach the entry's own colours\n"
       "\t\t. '.nlq .nlq-cover{overflow:hidden}.nlqw-host{margin:18px 0 26px}'\n"
       "\t\t. '@media(prefers-reduced-motion:no-preference){@keyframes nlqwDrift{from{transform:scale(1.03) translate3d(0,0,0)}to{transform:scale(1.12) translate3d(-2.5%,-1.5%,0)}}'\n"
       "\t\t. '.nlq .nlq-cover img,.nlqw-drift{animation:nlqwDrift 18s ease-in-out infinite alternate;will-change:transform}}'\n"
       "\t\t. '.nlhp-svcard__media picture{display:block;width:100%;height:100%}.nlhp-svcard__media{overflow:hidden}'\n"
       "\t\t. 'body .nlq.nlq .nlq-sign h2,body .nlq.nlq .nlq-sign h2 *{color:#fff!important}body .nlq.nlq .nlq-sign p{color:#e3eff3!important}'\n"
       "\t\t. 'body .nlq.nlq a.nlq-enter{color:#123750!important;background:#fff!important}body .nlq.nlq .nlq-stops a{color:#17617c!important}';")
T.append((". 'body.nl-skin-a .nlsdt .nlsdt-note{color:#6D665C!important}';", ". 'body.nl-skin-a .nlsdt .nlsdt-note{color:#6D665C!important}'" + CSS))
ENTRY = r"""

/* 1.72.744 (HAD-801): Sde Dov 2036, the walk through the future quarter (Codex's build at <site root>/tour/sde-dov/).
 * Its WordPress entry ([nadlan_walk], assets/quarter-walk, copied as packaged) shows a still from the tour, the sign, three stops
 * and the list of places and sources; nothing of the 3D engine loads until a press, and then inside a dialog on this page.
 * On /sde-dov/ it stands right after the opening paragraph and its buttons; the picture, the area map and the rest stay. */
if ( ! function_exists( 'nadlan_walk_render' ) && file_exists( dirname( __DIR__ ) . '/assets/quarter-walk/nadlan-quarter-walk.php' ) ) {
	require_once dirname( __DIR__ ) . '/assets/quarter-walk/nadlan-quarter-walk.php';
}
function nadlan_sdedov_walk_entry( $content ) {
	if ( ! function_exists( 'nadlan_walk_render' ) || ! is_page( 'sde-dov' ) || ! in_the_loop() || ! is_main_query() || false !== strpos( $content, 'data-nlq' ) ) {
		return $content;
	}
	$i = strpos( $content, 'class="nls1-cta"' );
	$j = ( false === $i ) ? false : strpos( $content, '</div>', $i );
	if ( false === $j ) {
		return $content;
	}
	$j += 6;
	return substr( $content, 0, $j ) . '<div class="nlqw-host" id="walk">' . nadlan_walk_render( array() ) . '</div>' . substr( $content, $j );
}
add_filter( 'the_content', 'nadlan_sdedov_walk_entry', 22 );
"""
T.append(("add_filter( 'the_content', 'nadlan_sdedov_tour_page_append', 21 );", "add_filter( 'the_content', 'nadlan_sdedov_tour_page_append', 21 );" + ENTRY.rstrip("\n")))

HV = []
HV.append(("$pic = '<img src=\"' . esc_url( nadlan_hp_img( 'tour-sdedov-dusk-960.jpg' ) ) . '\" srcset=\"' . esc_url( nadlan_hp_img( 'tour-sdedov-dusk-640.jpg' ) ) . ' 640w, ' . esc_url( nadlan_hp_img( 'tour-sdedov-dusk-960.jpg' ) ) . ' 960w\" sizes=\"(max-width:760px) 100vw, 55vw\" width=\"960\" height=\"600\" alt=\"\" loading=\"lazy\" decoding=\"async\" fetchpriority=\"low\">';",
           "/* 1.72.744 (HAD-801): the picture is a frame of the new tour (Sde Dov 2036) at the Ibn Gabirol and Einstein junction, lazy */\n"
           "\t\t$cv  = trailingslashit( $tour ) . 'media/wordpress/covers/junction-signs';\n"
           "\t\t$pic = '<picture><source type=\"image/avif\" srcset=\"' . esc_url( $cv . '-375.avif' ) . ' 375w, ' . esc_url( $cv . '-750.avif' ) . ' 750w, ' . esc_url( $cv . '-960.avif' ) . ' 960w, ' . esc_url( $cv . '-1440.avif' ) . ' 1440w\" sizes=\"(max-width:760px) 100vw, 55vw\">'\n"
           "\t\t\t. '<img class=\"nlqw-drift\" src=\"' . esc_url( $cv . '-wide.webp' ) . '\" width=\"1440\" height=\"800\" alt=\"הרכבת הקלה והמדרכה בצומת אבן גבירול ואיינשטיין, בסיור ברובע שדה דב\" loading=\"lazy\" decoding=\"async\" fetchpriority=\"low\"></picture>';"))
HV.append(("<small>סיור וירטואלי</small><h3>רובע שדה דב, לפי התכנית</h3>'", "<small>סיור וירטואלי</small><h3>שדה דב 2036: הולכים ברובע, לפי התכנית</h3>'"))
HV.append(("'<p>טיסת דמדומים מעל הרובע וסיור חופשי ברחובותיו, מהים ועד המגדלים של דמרי ימה, ריינבו ואשירה. מכל מגדל עוברים לעמוד הפרויקט.</p>'",
           "'<p>מצומת אבן גבירול ואיינשטיין ועד הים: הרחובות, הפארקים והמגרשים של הרובע, עם שמות הפרויקטים והיזמים שזכו במכרזים. יותר מ־3,000 מקומות, לכל אחד מקור ותאריך.</p>'"))
HV.append(("'<span class=\"nlhp-svcard__ctas\"><a class=\"nlhp-btn nlhp-btn--line\" href=\"' . esc_url( $tour ) . '\">כניסה לסיור</a></span>'",
           "'<span class=\"nlhp-svcard__ctas\"><a class=\"nlhp-btn nlhp-btn--line\" href=\"' . esc_url( $tour ) . '\">כניסה לסיור</a><a class=\"nlhp-btn nlhp-btn--line\" href=\"' . esc_url( home_url( '/sde-dov/#walk' ) ) . '\">רובע שדה דב</a></span>'"))
for rel, hs in (("inc/sdedov-teaser.php", T), ("inc/home-v3.php", HV)):
    for old, new in hs:
        assert LIVE[rel].count(old) == 1, (rel, "anchor x%d" % LIVE[rel].count(old), old[:90])
print("hunks:", len(T), "+", len(HV))

NEWF = ["assets/quarter-walk/nadlan-quarter-walk.php", "assets/quarter-walk/walk.css", "assets/quarter-walk/walk.js", "assets/quarter-walk/entries.json",
        "assets/quarter-walk/fonts/heebo.woff2", "assets/quarter-walk/fonts/barlow.woff2", "assets/quarter-walk/fonts/walk-year-digits.woff2",
        "assets/quarter-walk/fonts/heebo-OFL.txt", "assets/quarter-walk/fonts/barlow-OFL.txt", "assets/quarter-walk/fonts/barlowcondensed-OFL.txt"]
BAD = "['Fatal error', 'Warning</b>', 'Notice</b>']"
ROWS = ("    ('/sde-dov/?t744=1', ['data-nlq', 'id=\"walk\"', 'הדמיה להמחשה, על פי התכנית', 'nls1-lead', 'class=\"nlam', 'sdplan-tool', 'quarter-walk/walk.js', 'נכנסים לעתיד של רובע שדה דב', 'wa.me/'], ['Fatal error', 'Warning</b>', 'Notice</b>', 'מכונת זמן 2026'], []),\n"
        "    ('/?t744=1', ['nlhp-svcard--tour', 'media/wordpress/covers/junction-signs-wide.webp', 'שדה דב 2036: הולכים ברובע'], ['Fatal error', 'Warning</b>', 'Notice</b>', 'טיסת דמדומים מעל הרובע'], []),\n"
        "    ('/projects/rainbow-tel-aviv/?t744=1', ['id=\"nlps\"', 'mountRainbowStage'], %s, []),\n"
        "    ('/projects/h-infinity-somail-tel-aviv/?t744=1', [], %s, []),\n"
        "    ('/tour/sde-dov/?t744=1', ['<title>שדה דב 2036 | הליכה ברובע העתידי של תל אביב', 'הדמיה להמחשה, על פי התכנית', 'id=\"nlTourWa\"', 'nad-lan host: .bin/.json', 'entry-6c2a6e0d822e9a0010/assets/entry.js'], ['Fatal error', 'load.php?f=', 'file.php?f='], []),\n"
        "    ('/tour/sde-dov/places/?t744=1', ['מקומות ומקורות', 'itemtype=\"https://schema.org/Place\"', '<base href=\"../\">'], ['Fatal error', 'name=\"robots\"'], []),\n") % (BAD, BAD)
kl_release.build_release(PREV, NEW, NEWF, NEWF, {"inc/sdedov-teaser.php": T, "inc/home-v3.php": HV}, MD5, ROWS,
                         "the entries to the new Sde Dov 2036 tour: /sde-dov/ after the opening, the home tour card, project deep links",
                         "HAD-801 Sde Dov 2036 entries")

# the inherited home row (sv310) asserted the old tour card; this release changes that card on purpose: the row now asserts the new one
_d = os.path.join(os.path.dirname(os.path.abspath(__file__)), "deploy%d.py" % NEW)
_t = open(_d, encoding="utf-8").read()
for a, b in (("<h3>רובע שדה דב, לפי התכנית</h3>'", "<h3>שדה דב 2036: הולכים ברובע, לפי התכנית</h3>'"),
             ("'assets/home/tour-sdedov-dusk-960.jpg?ver=1.72.744', 'tour-sdedov-dusk-640.jpg?ver=1.72.744 640w', ",
              "'media/wordpress/covers/junction-signs-wide.webp', 'junction-signs-960.avif 960w', ")):
    assert _t.count(a) == 1, ("inherited row token x%d" % _t.count(a), a[:60])
    _t = _t.replace(a, b)
for _ln in _t.splitlines():
    if "'/tour/sde-dov/?" in _ln or "\"/tour/sde-dov/?" in _ln:
        for _old in ("function walkToSea(", "tour-wa-v71s", "tagDimri:", "NARR_FIX_BASE", "focus="):
            assert _old not in _ln, "an inherited row still expects the OLD tour: " + _ln[:120]
# a gentle runner (coordinator 22.11): a short pause before every page check and a slow retry on 429 (the host's per-visitor limit)
_a = '            s, html = page(path + sep + "nlv=" + tag)\n'
if _t.count(_a) == 1:
    _t = _t.replace(_a, '            time.sleep(0.7)\n' + _a
                    + '            for _k in range(3):\n'
                    + '                if s != 429:\n'
                    + '                    break\n'
                    + '                print(f"[page] 429 on {path[:70]}: waiting {30 * (_k + 1)} s")\n'
                    + '                time.sleep(30 * (_k + 1))\n'
                    + '                s, html = page(path + sep + "nlv=" + tag + "q%d" % _k)\n')
    print("runner: 0.7 s pause per check, 429 retried up to 3 times")
else:
    print("runner: verify_pages anchor not found, left as the base has it")
open(_d, "w", encoding="utf-8", newline=chr(10)).write(_t)
print("inherited home tour-card row moved to the new card")
