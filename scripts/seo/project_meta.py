# -*- coding: utf-8 -*-
"""The flagship project pages' search titles and descriptions (28.9.2026). Search Console, 29.8-26.9.2026: the project pages
drew 16,004 impressions and 96 clicks; Ashira 425 impressions at position 7.0 with 1 click, its title a keyword string
("ASHIRA - פרויקט אשירה שדה דב תל אביב מחיר") and its description the generic "כל המידע על..."; DUO's and Dimri's
descriptions generic too; H Infinity's said 52 floors and 242 apartments while its own lead (the company's 2025 report)
says 53 and about 278. Each text below is built only from the facts the page prints with their sources
(inc/project-stage.php configs, the pages' leads, docs/research/2026-09-28-duo). Written to Yoast's fields (title, meta
description, and the social descriptions where they are set), each guarded by the value read just before, through the
token-gated temporary bridge of rainbow_meta.py; the app password is decrypted in-process (DPAPI), never printed.
  python scripts/seo/project_meta.py            # read and show the plan
  python scripts/seo/project_meta.py --apply    # write"""
import io, json, os, secrets, sys, time
REPO = r"C:\Users\777\nad-lan\nad-lan-co-il"
src = io.open(os.path.join(REPO, "scripts", "project-stage", "rainbow_content4.py"), encoding="utf-8").read()
exec(compile(src[src.index("import base64, ctypes"):src.index("def read():")]
             .replace('QA = os.path.join(REPO, "docs", "qa", "rainbow-content-2026-09-24")', 'QA = os.path.join(REPO, "docs", "qa", "seo-meta-2026-09-28")'), "head", "exec"))

META = {
    "ashira-sde-dov": {
        "title": "פרויקט אשירה שדה דב (ASHIRA) של אביסרור | מחירים ודירות | נדלן",
        "desc": "פרויקט אשירה (ASHIRA) של אביסרור משה ובניו ברובע שדה דב: 406 דירות, מגדל של 35 קומות ושלושה בניינים, בריכה וחדרי כושר. בחירת קומה, הנוף מהקומה והמפה.",
    },
    "duo-tel-aviv": {
        "desc": "מגדלי DUO תל אביב של אפריקה ישראל מגורים, אבן גבירול פינת ארלוזורוב: 2 מגדלים של 54 קומות, 668 דירות, 372 מתוך 510 נמכרו עד 6.2026. בחירת קומה והנוף.",
    },
    "dimri-yama-sde-dov": {
        "title": "דמרי ימה שדה דב (DIMRI YAMA) | י.ח דמרי | מחירים ודירות | נדלן",
        "desc": "דמרי ימה (DIMRI YAMA) של י.ח דמרי ברובע שדה דב: מגדל של 40 קומות, 458 דירות וכ-70 חדרי מלון, כ-700 מ׳ מהים. מחיר הפתיחה שפורסם: מ-3.75 מיליון ₪.",
    },
    # Kikar Hamedina (P7, 30.9.2026): the same texts as scripts/project-stage/hamedina_page_data.py (deploy369.py writes them when
    # it creates the two posts; kept here so a later run of this script keeps them)
    "hamedina": {
        "title": "מגדלי כיכר המדינה תל אביב: מחירים, עסקאות, מפה ותלת ממד",
        "desc": "מגדלי כיכר המדינה בתל אביב: 3 מגדלים מסתובבים ו-453 דירות, עסקאות ב-9.58 עד 10.63 מיליון ₪, מועדי האכלוס, הפארק והאגם, והנוף מכל קומה.",
    },
    "hamedina-en": {
        "title": "Kikar Hamedina Towers Tel Aviv: Prices, Deals, Map & 3D",
        "desc": "Kikar Hamedina Towers, Tel Aviv: 3 twisting towers, 453 apartments, deals at ₪9.58M to ₪10.63M, occupancy dates, the park and the view from every floor.",
    },
    # P8 (1.72.370): the French, Russian and Arabic siblings (deploy370.py writes them when it creates the posts; the Arabic title
    # is English by the owner's ruling of 28.9.2026)
    "hamedina-fr": {
        "title": "Tours Kikar Hamedina à Tel Aviv\xa0: appartements, prix et 3D",
        "desc": "Tours Kikar Hamedina à Tel Aviv\xa0: 3 tours torsadées, 453 appartements, ventes de 9,58 à 10,63\xa0M₪, livraison, le parc et la vue de chaque étage.",
    },
    "hamedina-ru": {
        "title": "Башни Кикар ха-Медина, Тель-Авив: цены, сделки, карта и 3D",
        "desc": "Башни Кикар ха-Медина в Тель-Авиве: 3 закрученные башни, 453 квартиры, сделки от 9,58 до 10,63\xa0млн\xa0₪, сроки заселения, парк и вид с каждого этажа.",
    },
    "hamedina-ar": {
        "title": "Kikar Hamedina Towers, Tel Aviv: Prices, Deals & 3D Map",
        "desc": "أبراج كيكار همدينا في تل أبيب: 3 أبراج ملتفّة و453 شقة، صفقات بين 9.58 و10.63 مليون ₪، مواعيد السكن، الحديقة والإطلالة من كل طابق.",
    },
    "h-infinity-somail-tel-aviv": {
        "desc": "אייץ' אינפיניטי (H Infinity) של קבוצת חג'ג', אבן גבירול 128 במתחם סומייל: מגדל של 53 קומות ובניין בוטיק, כ-278 דירות של 2 עד 6 חדרים. נתונים, מפה וסביבה.",
    },
}
for k, v in META.items():
    assert len(v["desc"]) <= 160, (k, len(v["desc"]))
    assert "title" not in v or len(v["title"]) <= 66, (k, len(v["title"]))

PIDS = {}
for slug in list(META):
    s, d = req("GET", "/wp-json/wp/v2/nadlan_project?slug=%s&_fields=id" % slug)
    if not d:  # not created yet (the Kikar Hamedina pages come with deploy369.py / deploy370.py)
        print("[skip] %s: no published post yet" % slug)
        META.pop(slug)
        continue
    PIDS[slug] = int(d[0]["id"])
TOKEN = secrets.token_hex(24)
NS = "nadlan-pmeta-" + TOKEN[:8]
BRIDGE = r"""
add_action( 'rest_api_init', function () {
	register_rest_route( '__NS__/v1', '/run', array(
		'methods' => 'POST',
		'permission_callback' => function () { return current_user_can( 'manage_options' ); },
		'callback' => function ( $req ) {
			$b = $req->get_json_params();
			if ( ! is_array( $b ) || ! hash_equals( '__TOKEN__', (string) ( $b['token'] ?? '' ) ) ) { return new WP_Error( 'forbidden', 'token', array( 'status' => 400 ) ); }
			$allowed = array( __PIDS__ );
			$out = array();
			foreach ( $allowed as $pid ) {
				$y = array();
				foreach ( get_post_meta( $pid ) as $k => $v ) { if ( 0 === strpos( $k, '_yoast_wpseo_' ) ) { $y[ $k ] = is_array( $v ) ? $v[0] : $v; } }
				$out[ $pid ] = array( 'before' => $y );
			}
			if ( ! empty( $b['do'] ) ) {
				foreach ( (array) ( $b['write'] ?? array() ) as $pid => $w ) {
					$pid = (int) $pid;
					if ( ! in_array( $pid, $allowed, true ) ) { continue; }
					$done = array();
					foreach ( (array) $w as $k => $pair ) {
						if ( 0 !== strpos( $k, '_yoast_wpseo_' ) ) { $done[ $k ] = 'SKIP: not a Yoast field'; continue; }
						$cur = (string) get_post_meta( $pid, $k, true );
						if ( $cur !== (string) $pair[0] ) { $done[ $k ] = 'SKIP: changed since read'; continue; }
						update_post_meta( $pid, $k, wp_slash( (string) $pair[1] ) );
						$done[ $k ] = 'ok';
					}
					if ( function_exists( 'YoastSEO' ) ) {
						try {
							$repo = YoastSEO()->classes->get( \Yoast\WP\SEO\Repositories\Indexable_Repository::class );
							$bld  = YoastSEO()->classes->get( \Yoast\WP\SEO\Builders\Indexable_Builder::class );
							$ix   = $repo->find_by_id_and_type( $pid, 'post', false );
							if ( $ix ) { $bld->build_for_id_and_type( $pid, 'post', $ix ); $done['indexable'] = 'rebuilt'; }
						} catch ( \Throwable $e ) { $done['indexable'] = 'error: ' . $e->getMessage(); }
					}
					clean_post_cache( $pid );
					do_action( 'litespeed_purge_post', $pid );
					$out[ $pid ]['done'] = $done;
					$y = array();
					foreach ( get_post_meta( $pid ) as $k => $v ) { if ( 0 === strpos( $k, '_yoast_wpseo_' ) ) { $y[ $k ] = is_array( $v ) ? $v[0] : $v; } }
					$out[ $pid ]['after'] = $y;
				}
				do_action( 'litespeed_purge_all' );
			}
			return $out;
		},
	) );
} );
""".replace("__TOKEN__", TOKEN).replace("__NS__", NS).replace("__PIDS__", ", ".join(str(p) for p in PIDS.values()))

s, c = req("POST", "/wp-json/code-snippets/v1/snippets", {"name": "x-tmp-pmeta-%d" % int(time.time()), "code": BRIDGE, "scope": "global", "active": False})
if s not in (200, 201):
    raise SystemExit("FATAL bridge create %s %s" % (s, str(c)[:200]))
BR = c["id"]
try:
    req("PUT", "/wp-json/code-snippets/v1/snippets/%s/activate" % BR, {})
    r = None
    for _ in range(10):
        s, r = req("POST", "/wp-json/" + NS + "/v1/run", {"token": TOKEN})
        if s == 200:
            break
        time.sleep(1.5)
    if s != 200:
        raise SystemExit("FATAL bridge call %s %s" % (s, str(r)[:300]))
    write = {}
    for slug, v in META.items():
        pid = PIDS[slug]
        y = r[str(pid)]["before"]
        y = y if isinstance(y, dict) else {}  # PHP sends an empty array as []
        w = {}
        if "title" in v:
            w["_yoast_wpseo_title"] = [y.get("_yoast_wpseo_title", ""), v["title"]]
        w["_yoast_wpseo_metadesc"] = [y.get("_yoast_wpseo_metadesc", ""), v["desc"]]
        for k in ("_yoast_wpseo_opengraph-description", "_yoast_wpseo_twitter-description"):
            if y.get(k):
                w[k] = [y[k], v["desc"]]
        write[str(pid)] = w
        print("[%s %d] before: title=%r desc=%r" % (slug, pid, y.get("_yoast_wpseo_title", ""), y.get("_yoast_wpseo_metadesc", "")[:80]))
        print("   plan:", json.dumps({k: x[1] for k, x in w.items()}, ensure_ascii=False))
    if "--apply" in sys.argv:
        os.makedirs(QA, exist_ok=True)
        stamp = time.strftime("%Y%m%dT%H%M%S")
        io.open(os.path.join(QA, "project-meta.%s.before.json" % stamp), "w", encoding="utf-8").write(json.dumps(r, ensure_ascii=False, indent=1))
        s, r2 = req("POST", "/wp-json/" + NS + "/v1/run", {"token": TOKEN, "do": 1, "write": write})
        print("[set]", s, json.dumps({k: v.get("done") for k, v in r2.items()} if isinstance(r2, dict) else r2, ensure_ascii=False))
        io.open(os.path.join(QA, "project-meta.%s.after.json" % stamp), "w", encoding="utf-8").write(json.dumps(r2, ensure_ascii=False, indent=1))
finally:
    req("PUT", "/wp-json/code-snippets/v1/snippets/%s/deactivate" % BR, {})
    s, _ = req("DELETE", "/wp-json/code-snippets/v1/snippets/%s" % BR)
    time.sleep(1.5)
    s2, _ = req("POST", "/wp-json/" + NS + "/v1/run", {"token": TOKEN})
    print("[bridge] delete http %s; route now http %s (want 404)" % (s, s2))
