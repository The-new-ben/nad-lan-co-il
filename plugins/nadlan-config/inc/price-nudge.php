<?php
/**
 * nadlan-config - PRICE ALERT (HAD-684, Ben 8.11.2026; replaces the HAD-642 slip of 31.10 / 1.11): a two-step price-alert window
 * on every Hebrew project page and listing. Claude Design v106, component PriceAlert.
 *
 * Ben, 8.11.2026: "I don't see it pop up at all. Make it very smart, an attention mark, 'prices in this area are changing',
 * a blinking down arrow, without writing that prices are falling; sign up for price updates; phone AND email required.
 * On every project and real-estate page, except Meital Katzir and the professionals."
 *
 * Why the slip was never seen (8.11): 25 s AND 35% of the page, 20% of browsers held out for good, 7 days of quiet across the
 * whole site after any close (the 14 s self-fade counted as a close), once a session. v106 resets all of it (new keys).
 *
 * - Where: every published Hebrew nadlan_project (Ashira never, Ben 31.10; a project box that says off stays off: Rainbow,
 *   Ben 1.11), every Hebrew nadlan_property that is NOT a broker's (no nl_broker_id: Meital's listings are out, Ben 8.11),
 *   every Hebrew nadlan_intl project. Professionals, brokers' pages and articles never (the hook only runs on those types).
 * - The arrow is honest by data: it stands beside "המחירים באזור זה במגמת שינוי" only where the CBS dwelling price index of the
 *   page's district (or the national one, when the city is not mapped) is down over 12 months (data/prices-hub.json, the file
 *   the prices hub uses). Elsewhere (a rent listing, a project abroad, a district going up) the line is "משתנים" and the arrow
 *   points down at the form. The window never states a figure and never says "יורדים".
 * - When (v106.2, Ben 8.11.2026 "too fast, let them browse and look first"; all settings): behaviour, not a clock. Never before a
 *   15 s floor; then 25 s of ACTIVE time on the first project/listing page of a visit (15 s from the second), counted only while
 *   the reader scrolls, touches or moves; AND 2 signals of looking (read 1.5 screens, a ₪ figure on screen 2 s, a tap on the page's
 *   own tools, a 6 s reading pause, a 2nd page in the visit); THEN only at a natural break (scrolling stopped 1.5 s, no finger
 *   down, nothing selected, no video playing). Leaving signals (pointer out at the top, a fast run back to the top, a return to
 *   the tab) need the floor and one signal. Never while typing, in full screen, inside another dialog, after a WhatsApp tap.
 *   ?nudge=fresh = a real-timing test as a new visitor.
 * - Format: a phone bottom sheet (no backdrop, the page keeps scrolling, swipe down to close) and a desktop modal with a scrim.
 *   Step 1 asks one tap ("על מה לעדכן אתכם?": קנייה / יש לי נכס / השקעה); step 2 asks the phone and the email (both required),
 *   one consent box and the collection notice; step 3 says what happens next and offers WhatsApp.
 * - After: once a session and at most twice in 30 days (the second showing converts almost like the first, the third falls
 *   off: Popupsmart 2026); 3 days of quiet after a close, 1 day if it was ignored, a year after a sign-up. A 10% holdout,
 *   re-drawn every 30 days, so nobody is excluded for good. ?nudge=show shows it after 2 s for checking.
 * - The sign-up: POST /nadlan/v1/price-alert -> a private nadlan_lead (goal "עדכוני מחירים", utm_source price_alert), the
 *   owner's rich alert mail (inc/alerts.php) 2 minutes later. Never routed to a developer, a broker or a card owner (no
 *   lead_card_id, no nadlan_lead_route call), no drip, no AI call. The consent text, its version and time are kept with it.
 * - The frame says "נדל״ן · nad-lan.co.il", never a project's or a listing's name (Ben 1.11, the Brokers Law exemption).
 * - Measurement: pa_shown {trigger}, pa_step2 {interest}, pa_submit, pa_done (+ generate_lead), pa_error, pa_close {how},
 *   pa_holdout, through window.nadlanGA (dataLayer + gtag).
 */
if ( ! defined( 'ABSPATH' ) ) { exit; }

if ( ! defined( 'NADLAN_PA_NOTICE' ) ) {
	define( 'NADLAN_PA_NOTICE', 'pa1-2026-11-08' ); // the version of the collection notice and consent line the visitor saw
}

if ( ! function_exists( 'nadlan_pa_opts' ) ) {
	/** v106 settings, a new option (the 105.x option kept 25 s / 35% / 7 days / 20% and would override new defaults). */
	function nadlan_pa_opts() {
		/* v106.2 (Ben 8.11.2026 "too fast"): floor 15 s visible; 25 s of ACTIVE time on the first page of a visit, 15 s from the second;
		   2 behaviour signals; then a natural break (see assets/nudge/price-alert.js) */
		$d = array( 'on' => 1, 'listings' => 1, 'global' => 1, 'floor' => 15, 'act1' => 25, 'act2' => 15, 'need' => 2, 'depth' => 30, 'quiet' => 3, 'quiet_ign' => 1, 'holdout' => 10 );
		$o = get_option( 'nadlan_pa_opts', array() );
		return is_array( $o ) ? array_merge( $d, array_intersect_key( $o, $d ) ) : $d;
	}
}

if ( ! function_exists( 'nadlan_nudge_blocked' ) ) {
	/** never on these projects, whatever the box says (Ben 31.10.2026: not on Ashira) */
	function nadlan_nudge_blocked( $id ) {
		$slug = (string) get_post_field( 'post_name', $id );
		return 0 === strpos( $slug, 'ashira' ) || 0 === strpos( rawurldecode( $slug ), 'אשירה' );
	}
}

if ( ! function_exists( 'nadlan_nudge_on' ) ) {
	function nadlan_nudge_on( $id = 0 ) {
		$id = (int) ( $id ?: get_queried_object_id() );
		if ( ! $id || 'publish' !== get_post_status( $id ) || post_password_required( $id ) ) { return false; }
		$o  = nadlan_pa_opts();
		$t  = get_post_type( $id );
		$he = (bool) preg_match( '/\p{Hebrew}/u', (string) get_the_title( $id ) );
		if ( 'nadlan_property' === $t ) {
			/* Ben 8.11.2026: not on Meital Katzir's listings, nor any broker's (they carry their own contact bar) */
			if ( empty( $o['listings'] ) || '' !== trim( (string) get_post_meta( $id, 'nl_broker_id', true ) ) ) { return false; }
			return $he && 'off' !== (string) get_post_meta( $id, 'nadlan_nudge', true );
		}
		if ( 'nadlan_intl' === $t ) {
			return ! empty( $o['global'] ) && $he && 'off' !== (string) get_post_meta( $id, 'nadlan_nudge', true );
		}
		if ( 'nadlan_project' !== $t || nadlan_nudge_blocked( $id ) || ! $he ) { return false; }
		$m = (string) get_post_meta( $id, 'nadlan_nudge', true );
		if ( 'on' === $m ) { return true; }
		if ( 'off' === $m ) { return false; } // Rainbow (Ben 1.11.2026) and any project switched off in its box
		return ! empty( $o['on'] );
	}
}

/* ---------- the trend behind the arrow (CBS dwelling price index, 12 months) ---------- */
if ( ! function_exists( 'nadlan_pa_norm' ) ) {
	function nadlan_pa_norm( $s ) {
		$s = str_replace( array( 'קריית', '-', "\u{2013}", '״', '"', "'", '׳', '(', ')' ), array( 'קרית', ' ', ' ', '', '', '', '', ' ', ' ' ), (string) $s );
		return trim( preg_replace( '/\s+/u', ' ', $s ) );
	}
}
if ( ! function_exists( 'nadlan_pa_index' ) ) {
	/** {nat: pct, asof, dist: {district: pct}, city: {normalised city: district}} from data/prices-hub.json, cached a day */
	function nadlan_pa_index() {
		static $x = null;
		if ( null !== $x ) { return $x; }
		$x = get_transient( 'nadlan_pa_index_v1' );
		if ( is_array( $x ) ) { return $x; }
		$x = array( 'nat' => null, 'asof' => '', 'dist' => array(), 'city' => array() );
		$f = dirname( __DIR__ ) . '/assets/instruments/data/prices-hub.json';
		$d = is_readable( $f ) ? json_decode( (string) file_get_contents( $f ), true ) : null; // phpcs:ignore
		$pct = function ( $v ) {
			$v = array_values( array_filter( (array) $v, 'is_numeric' ) );
			$n = count( $v );
			return $n >= 13 && (float) $v[ $n - 13 ] > 0 ? round( ( (float) $v[ $n - 1 ] / (float) $v[ $n - 13 ] - 1 ) * 100, 1 ) : null;
		};
		if ( is_array( $d ) ) {
			if ( isset( $d['hpi']['v'] ) ) {
				$x['nat'] = $pct( $d['hpi']['v'] );
				$from = explode( '-', (string) ( $d['hpi']['from'] ?? '' ) );
				if ( 2 === count( $from ) ) {
					$m = (int) $from[1] - 1 + count( (array) $d['hpi']['v'] ) - 1;
					$x['asof'] = sprintf( '%04d-%02d', (int) $from[0] + intdiv( $m, 12 ), $m % 12 + 1 );
				}
			}
			foreach ( (array) ( $d['dist'] ?? array() ) as $r ) {
				if ( ! empty( $r['n'] ) ) { $x['dist'][ (string) $r['n'] ] = $pct( $r['v'] ?? array() ); }
			}
			foreach ( (array) ( $d['city'] ?? array() ) as $r ) {
				if ( ! empty( $r['n'] ) && ! empty( $r['dist'] ) ) { $x['city'][ nadlan_pa_norm( $r['n'] ) ] = (string) $r['dist']; }
			}
		}
		/* towns outside the hub's 24 cities, by CBS district (only used to pick the district series; unknown = national) */
		$more = array(
			'הצפון' => array( 'נצרת', 'נוף הגליל', 'עפולה', 'כרמיאל', 'טבריה', 'נהריה', 'צפת', 'בית שאן', 'מגדל העמק', 'קרית שמונה', 'מעלות תרשיחא', 'יבנאל', 'שלומי', 'עכו' ),
			'חיפה'   => array( 'קרית אתא', 'קרית ביאליק', 'קרית מוצקין', 'קרית ים', 'טירת כרמל', 'נשר', 'חדרה', 'זכרון יעקב', 'פרדס חנה כרכור', 'אור עקיבא', 'יקנעם עילית', 'בנימינה גבעת עדה' ),
			'המרכז'  => array( 'לוד', 'רמלה', 'ראש העין', 'יהוד מונוסון', 'שוהם', 'גדרה', 'נס ציונה', 'באר יעקב', 'גבעת שמואל', 'אלעד', 'כפר יונה', 'טירה', 'קדימה צורן', 'אבן יהודה', 'גני תקווה', 'מזכרת בתיה', 'קרית עקרון', 'תל מונד', 'כוכב יאיר צור יגאל' ),
			'תל אביב' => array( 'אור יהודה', 'אזור' ),
			'ירושלים' => array( 'בית שמש', 'מבשרת ציון', 'אבו גוש' ),
			'הדרום'  => array( 'קרית גת', 'קרית מלאכי', 'דימונה', 'שדרות', 'נתיבות', 'אופקים', 'ירוחם', 'ערד', 'מצפה רמון', 'רהט' ),
		);
		foreach ( $more as $dist => $towns ) {
			foreach ( $towns as $tw ) { $k = nadlan_pa_norm( $tw ); if ( ! isset( $x['city'][ $k ] ) ) { $x['city'][ $k ] = $dist; } }
		}
		set_transient( 'nadlan_pa_index_v1', $x, DAY_IN_SECONDS );
		return $x;
	}
}
if ( ! function_exists( 'nadlan_pa_trend' ) ) {
	/** {city (display), pct, src: dist|nat|none, down: bool} for a page */
	function nadlan_pa_trend( $id ) {
		$city = trim( wp_strip_all_tags( (string) get_post_meta( $id, 'city', true ) ) );
		if ( mb_strlen( $city ) > 30 ) { $city = ''; }
		$out = array( 'city' => $city, 'pct' => null, 'src' => 'none', 'down' => false );
		if ( 'nadlan_intl' === get_post_type( $id ) ) { $out['city'] = ''; return $out; } // abroad: no Israeli series applies
		$ix = nadlan_pa_index();
		$k  = nadlan_pa_norm( $city );
		$dist = '';
		if ( '' !== $k ) {
			foreach ( $ix['city'] as $c => $dn ) {
				if ( $c === $k || 0 === strpos( $k, $c . ' ' ) || 0 === strpos( $c, $k . ' ' ) ) { $dist = $dn; break; }
			}
		}
		if ( '' !== $dist && isset( $ix['dist'][ $dist ] ) && null !== $ix['dist'][ $dist ] ) {
			$out['pct'] = $ix['dist'][ $dist ]; $out['src'] = 'dist';
		} elseif ( null !== $ix['nat'] ) {
			$out['pct'] = $ix['nat']; $out['src'] = 'nat';
		}
		$out['down'] = null !== $out['pct'] && $out['pct'] < 0;
		return $out;
	}
}

add_action( 'init', function () {
	foreach ( array( 'nadlan_nudge', 'nadlan_nudge_text' ) as $k ) {
		register_post_meta( 'nadlan_project', $k, array(
			'show_in_rest'  => true,
			'single'        => true,
			'type'          => 'string',
			'auth_callback' => function ( $allowed, $meta_key, $post_id ) { return current_user_can( 'edit_post', (int) $post_id ); },
		) );
	}
}, 20 );

/* ---------- admin: the box on every project ---------- */
add_action( 'add_meta_boxes_nadlan_project', function () {
	add_meta_box( 'nadlan_nudge_box', 'חלון עדכוני מחירים', function ( $post ) {
		$m   = (string) get_post_meta( $post->ID, 'nadlan_nudge', true );
		$t   = (string) get_post_meta( $post->ID, 'nadlan_nudge_text', true );
		$def = nadlan_pa_opts()['on'];
		wp_nonce_field( 'nadlan_nudge_save', 'nadlan_nudge_nonce' );
		if ( nadlan_nudge_blocked( $post->ID ) ) {
			echo '<p style="color:#b32d2e;font-weight:600">כבוי בפרויקט הזה לפי בן (31.10.2026).</p>';
		}
		foreach ( array( '' => 'לפי ברירת המחדל של האתר (כרגע: ' . ( $def ? 'מוצג' : 'לא מוצג' ) . ')', 'on' => 'להציג בעמוד הזה', 'off' => 'לא להציג בעמוד הזה' ) as $v => $label ) {
			echo '<label style="display:block;margin:4px 0"><input type="radio" name="nadlan_nudge" value="' . esc_attr( $v ) . '"' . checked( $m, $v, false ) . '> ' . esc_html( $label ) . '</label>';
		}
		echo '<p style="margin:10px 0 4px">שורה ראשית משלכם (לא חובה):</p><textarea name="nadlan_nudge_text" rows="2" style="width:100%" placeholder="המחירים באזור זה במגמת שינוי">' . esc_textarea( $t ) . '</textarea>';
		echo '<p style="color:#646970;font-size:12px;margin:4px 0 0">ריק = הנוסח הקבוע. החץ למטה מופיע ליד השורה רק כשמדד מחירי הדירות של המחוז ירד ב־12 החודשים האחרונים.</p>';
	}, 'nadlan_project', 'side', 'default' );
} );

add_action( 'save_post_nadlan_project', function ( $post_id ) {
	if ( ! isset( $_POST['nadlan_nudge_nonce'] ) || ! wp_verify_nonce( sanitize_text_field( wp_unslash( $_POST['nadlan_nudge_nonce'] ) ), 'nadlan_nudge_save' ) ) { return; }
	if ( defined( 'DOING_AUTOSAVE' ) && DOING_AUTOSAVE ) { return; }
	if ( ! current_user_can( 'edit_post', $post_id ) ) { return; }
	$v = isset( $_POST['nadlan_nudge'] ) ? sanitize_key( wp_unslash( $_POST['nadlan_nudge'] ) ) : '';
	if ( in_array( $v, array( 'on', 'off' ), true ) ) { update_post_meta( $post_id, 'nadlan_nudge', $v ); } else { delete_post_meta( $post_id, 'nadlan_nudge' ); }
	$t = isset( $_POST['nadlan_nudge_text'] ) ? sanitize_text_field( wp_unslash( $_POST['nadlan_nudge_text'] ) ) : '';
	if ( '' !== $t ) { update_post_meta( $post_id, 'nadlan_nudge_text', $t ); } else { delete_post_meta( $post_id, 'nadlan_nudge_text' ); }
} );

/* ---------- admin: the switch column in the projects list ---------- */
add_filter( 'manage_nadlan_project_posts_columns', function ( $cols ) {
	$cols['nadlan_nudge'] = 'חלון עדכון';
	return $cols;
} );
add_action( 'manage_nadlan_project_posts_custom_column', function ( $col, $post_id ) {
	if ( 'nadlan_nudge' !== $col ) { return; }
	if ( nadlan_nudge_blocked( $post_id ) ) { echo '<span style="color:#b32d2e">כבוי (בן)</span>'; return; }
	$on  = nadlan_nudge_on( $post_id ) || ( 'on' === get_post_meta( $post_id, 'nadlan_nudge', true ) );
	$url = wp_nonce_url( admin_url( 'admin-post.php?action=nadlan_nudge_toggle&post=' . (int) $post_id . '&to=' . ( $on ? 'off' : 'on' ) ), 'nadlan_nudge_toggle_' . (int) $post_id );
	echo '<a href="' . esc_url( $url ) . '" style="display:inline-block;padding:2px 10px;border-radius:999px;text-decoration:none;font-weight:600;'
		. ( $on ? 'background:#0f7a63;color:#fff">מוצג' : 'background:#dcdcde;color:#1d2327">כבוי' ) . '</a>';
}, 10, 2 );
add_action( 'admin_post_nadlan_nudge_toggle', function () {
	$id = isset( $_GET['post'] ) ? (int) $_GET['post'] : 0;
	check_admin_referer( 'nadlan_nudge_toggle_' . $id );
	if ( ! $id || ! current_user_can( 'edit_post', $id ) ) { wp_die( 'forbidden' ); }
	$to = isset( $_GET['to'] ) && 'on' === $_GET['to'] ? 'on' : 'off';
	update_post_meta( $id, 'nadlan_nudge', $to );
	wp_safe_redirect( wp_get_referer() ?: admin_url( 'edit.php?post_type=nadlan_project' ) );
	exit;
} );

/* ---------- admin: site settings ---------- */
add_action( 'admin_menu', function () {
	add_options_page( 'חלון עדכוני מחירים', 'חלון עדכוני מחירים', 'manage_options', 'nadlan-nudge', function () {
		if ( ! current_user_can( 'manage_options' ) ) { return; }
		if ( isset( $_POST['nadlan_pa_opts_nonce'] ) && wp_verify_nonce( sanitize_text_field( wp_unslash( $_POST['nadlan_pa_opts_nonce'] ) ), 'nadlan_pa_opts' ) ) {
			$in = wp_unslash( $_POST );
			update_option( 'nadlan_pa_opts', array(
				'on'        => ! empty( $in['on'] ) ? 1 : 0,
				'listings'  => ! empty( $in['listings'] ) ? 1 : 0,
				'global'    => ! empty( $in['global'] ) ? 1 : 0,
				'floor'     => max( 10, min( 120, (int) ( $in['floor'] ?? 15 ) ) ),
				'act1'      => max( 10, min( 180, (int) ( $in['act1'] ?? 25 ) ) ),
				'act2'      => max( 5, min( 120, (int) ( $in['act2'] ?? 15 ) ) ),
				'need'      => max( 1, min( 4, (int) ( $in['need'] ?? 2 ) ) ),
				'depth'     => max( 5, min( 90, (int) ( $in['depth'] ?? 30 ) ) ),
				'quiet'     => max( 1, min( 60, (int) ( $in['quiet'] ?? 3 ) ) ),
				'quiet_ign' => max( 1, min( 30, (int) ( $in['quiet_ign'] ?? 1 ) ) ),
				'holdout'   => max( 0, min( 50, (int) ( $in['holdout'] ?? 10 ) ) ),
			), false );
			echo '<div class="notice notice-success"><p>נשמר.</p></div>';
		}
		$o = nadlan_pa_opts();
		$f = function ( $k, $label, $hint ) use ( $o ) {
			echo '<tr><th><label for="nn-' . esc_attr( $k ) . '">' . esc_html( $label ) . '</label></th><td><input type="number" id="nn-' . esc_attr( $k ) . '" name="' . esc_attr( $k ) . '" value="' . (int) $o[ $k ] . '" class="small-text"> <span class="description">' . esc_html( $hint ) . '</span></td></tr>';
		};
		$c = function ( $k, $label ) use ( $o ) {
			echo '<label style="display:block;margin:3px 0"><input type="checkbox" name="' . esc_attr( $k ) . '" value="1"' . checked( ! empty( $o[ $k ] ), true, false ) . '> ' . esc_html( $label ) . '</label>';
		};
		$n = (int) ( new WP_Query( array( 'post_type' => 'nadlan_lead', 'post_status' => 'any', 'posts_per_page' => 1, 'fields' => 'ids', 'meta_key' => 'utm_source', 'meta_value' => 'price_alert' ) ) )->found_posts; // phpcs:ignore
		$ix = nadlan_pa_index();
		echo '<div class="wrap" dir="rtl"><h1>חלון עדכוני מחירים</h1><p>החלון עולה מאוחר בביקור בעמודי הפרויקטים והנכסים: סימן "שימו לב", "המחירים באזור זה במגמת שינוי" וחץ למטה, ואז טלפון ואימייל (שניהם חובה). כל הרשמה נכנסת לפניות (מקור: price_alert) ומגיעה אליכם במייל.</p>';
		$na_on = function_exists( 'nadlan_na_enabled' ) && nadlan_na_enabled();
		echo '<p><b>נרשמו עד היום: ' . (int) $n . '</b> · <a class="button" href="' . esc_url( wp_nonce_url( admin_url( 'admin-post.php?action=nadlan_pa_csv' ), 'nadlan_pa_csv' ) ) . '">הורדת כל הנרשמים (Excel)</a> · <a href="' . esc_url( admin_url( 'edit.php?post_type=nadlan_lead' ) ) . '">לפניות</a></p>';
		echo '<p>עדכונים אוטומטיים לנרשמים: <b>' . ( $na_on ? 'פעילים' : 'כבויים' ) . '</b>. כל נרשם מקבל מייל אישור, ואחרי לחיצה אחת מקבל מייל כשמשתנה מחיר למ״ר, שלב או מספר הדירות בפרויקט, כשיורד מחיר הנכס, או כשעולה נכס חדש עד 1.5 ק״מ. ' . ( $na_on ? '' : 'מדליקים במסך <a href="' . esc_url( admin_url( 'options-general.php?page=nadlan-mail' ) ) . '">מייל יוצא (Brevo)</a>, אחרי שמפתח השליחה נשמר.' ) . '</p><p>';
		echo 'מדד מחירי הדירות הארצי, 12 חודשים עד ' . esc_html( $ix['asof'] ) . ': ' . esc_html( null === $ix['nat'] ? 'אין נתון' : $ix['nat'] . '%' ) . ' (הלמ״ס)</p><form method="post">';
		wp_nonce_field( 'nadlan_pa_opts', 'nadlan_pa_opts_nonce' );
		echo '<table class="form-table"><tr><th>איפה</th><td>';
		$c( 'on', 'כל עמודי הפרויקטים (חוץ ממה שכובה בתיבה שלו, ואשירה)' );
		$c( 'listings', 'מודעות הנכסים (לא של מתווכים: לא מיטל קציר ולא אחרים)' );
		$c( 'global', 'פרויקטים בחו״ל (בלי חץ: אין להם מדד ישראלי)' );
		echo '</td></tr>';
		$f( 'floor', 'רצפה (שניות)', 'לעולם לא לפני: כמה שניות העמוד גלוי' );
		$f( 'act1', 'זמן פעיל, עמוד ראשון (שניות)', 'שניות שבהן הגולש באמת גלל, נגע או הזיז את העכבר, בעמוד הפרויקט או הנכס הראשון בביקור' );
		$f( 'act2', 'זמן פעיל, מהעמוד השני (שניות)', 'מי שכבר עבר לפרויקט או נכס נוסף מתעניין יותר' );
		$f( 'need', 'סימני עניין נדרשים', 'מתוך: קרא 1.5 מסכים, ראה מחיר בשקלים, לחץ על כלי בעמוד, עצר לקרוא, עמוד שני בביקור' );
		$f( 'depth', 'עומק קריאה (%)', 'או מסך וחצי, הקטן מביניהם, נחשב סימן עניין' );
		$f( 'quiet', 'שקט אחרי סגירה (ימים)', 'בכל האתר' );
		$f( 'quiet_ign', 'שקט כשהתעלמו (ימים)', 'כשהחלון נסגר בגלילה או בלי מגע' );
		$f( 'holdout', 'קבוצת ביקורת (%)', 'אחוז מבקרים שלא רואים אותו 30 יום, כדי למדוד מה הוא מוסיף' );
		echo '</table><p class="description">לבדיקה: ?nudge=show בסוף כתובת של פרויקט מראה את החלון אחרי 2 שניות (רק להסתכל עליו). ?nudge=fresh מתחיל אתכם כגולש חדש עם התזמון האמיתי: גללו, הסתכלו, והחלון יעלה רק כשתראו עניין.</p>';
		submit_button( 'שמירה' );
		echo '</form></div>';
	} );
} );

/* ---------- admin: every sign-up in one Excel-ready file (Ben 8.11.2026: "שנשמור את הפרטים שלהם") ---------- */
add_action( 'admin_post_nadlan_pa_csv', function () {
	if ( ! current_user_can( 'manage_options' ) ) { wp_die( 'forbidden' ); }
	check_admin_referer( 'nadlan_pa_csv' );
	$ids = get_posts( array( 'post_type' => 'nadlan_lead', 'post_status' => 'any', 'posts_per_page' => 5000, 'fields' => 'ids', 'no_found_rows' => true, 'suppress_filters' => true,
		'orderby' => 'date', 'order' => 'DESC', 'meta_query' => array( array( 'key' => 'utm_source', 'value' => 'price_alert' ) ) ) );
	nocache_headers();
	header( 'Content-Type: text/csv; charset=utf-8' );
	header( 'Content-Disposition: attachment; filename="price-alert-signups-' . gmdate( 'Y-m-d' ) . '.csv"' );
	$out = fopen( 'php://output', 'w' );
	fwrite( $out, "\xEF\xBB\xBF" ); // Excel reads the Hebrew as UTF-8
	fputcsv( $out, array( 'תאריך', 'טלפון', 'אימייל', 'עיר', 'עמוד', 'מה מעניין', 'התנהגות לפני ההרשמה', 'עדכונים אוטומטיים', 'הסכמה (UTC)', 'סטטוס' ) );
	$ints = array( 'buy' => 'קנייה', 'own' => 'יש נכס באזור', 'invest' => 'השקעה' );
	$al   = array( 'confirm-sent' => 'נשלח מייל אישור', 'off' => 'המנוע היה כבוי', 'no-point' => 'אין נקודה על המפה' );
	foreach ( $ids as $lid ) {
		$m = function ( $k ) use ( $lid ) { return (string) get_post_meta( $lid, $k, true ); };
		$i = $m( 'pa_interest' );
		$a = $m( 'pa_alerts' );
		fputcsv( $out, array( get_the_date( 'Y-m-d H:i', $lid ), $m( 'phone' ), $m( 'email' ), $m( 'city' ), $m( 'source_url' ), $ints[ $i ] ?? $i, $m( 'pa_signals' ), $al[ $a ] ?? $a, $m( 'consent_recorded' ), $m( 'lead_status' ) ) );
	}
	fclose( $out );
	exit;
} );

/* ---------- the owner's lead mail (v106.4, Ben 8.11.2026: "תשלח לי את הפרטים בצורה מסודרת... כמו ליד, כדי ליצור איתו קשר...
   שיהיה אפשר לבצע פעולות דרך המייל"): one HTML mail per sign-up, the phone first, one tap to call / WhatsApp / mail, the facts,
   and two signed actions that work from the mail with no login ("חזרתי אליו", "לא רלוונטי"). It replaces the plain-text alert
   of inc/alerts.php for these leads (that one is unscheduled at insert). ---------- */
if ( ! function_exists( 'nadlan_pa_sig' ) ) {
	function nadlan_pa_sig( $lid, $a ) { return substr( hash_hmac( 'sha256', 'pa|' . (int) $lid . '|' . $a, wp_salt( 'nonce' ) ), 0, 24 ); }
	function nadlan_pa_act_url( $lid, $a ) { return add_query_arg( array( 'l' => (int) $lid, 'a' => $a, 's' => nadlan_pa_sig( $lid, $a ) ), rest_url( 'nadlan/v1/pa-act' ) ); }
}
if ( ! function_exists( 'nadlan_pa_owner_mail' ) ) {
	function nadlan_pa_owner_mail( $lid ) {
		$to = (string) get_option( 'admin_email' );
		if ( ! is_email( $to ) ) { return false; }
		$m      = function ( $k ) use ( $lid ) { return (string) get_post_meta( $lid, $k, true ); };
		$phone  = $m( 'phone' );
		$email  = $m( 'email' );
		$city   = $m( 'city' );
		$pid    = (int) $m( 'project_wp_id' );
		$ptitle = $pid ? wp_strip_all_tags( get_the_title( $pid ) ) : '';
		$call   = '1' === $m( 'pa_callback' );
		$ints   = array( 'buy' => 'קנייה באזור', 'own' => 'יש לו/ה נכס באזור', 'invest' => 'השקעה', 'call' => 'ביקש/ה שיחה' );
		$int    = $ints[ $m( 'pa_interest' ) ] ?? '';
		$note   = $m( 'pa_note' );
		$intl   = '972' . ltrim( $phone, '0' );
		$pretty = strlen( $phone ) === 10 ? substr( $phone, 0, 3 ) . '-' . substr( $phone, 3 ) : $phone;
		$beh    = '';
		if ( preg_match( '/^([a-z+]*):a(\d+):s(\d+):p(\d+)$/', $m( 'pa_signals' ), $sm ) ) {
			$names = array( 'read' => 'קרא את העמוד', 'price' => 'ראה מחירים', 'explore' => 'השתמש בכלים בעמוד', 'pause' => 'עצר לקרוא', 'ret' => 'עבר לעמוד נוסף' );
			$said  = array();
			foreach ( array_filter( explode( '+', $sm[1] ) ) as $s ) { if ( isset( $names[ $s ] ) ) { $said[] = $names[ $s ]; } }
			$beh = (int) $sm[2] . ' שניות פעילות, עמוד ' . (int) $sm[4] . ' בביקור' . ( $said ? ': ' . implode( ', ', $said ) : '' );
		}
		$al     = array( 'confirm-sent' => 'נשלח אליו מייל אישור; אחרי לחיצה יקבל עדכונים אוטומטיים', 'off' => 'מנוע העדכונים כבוי', 'no-point' => 'לעמוד אין נקודה על המפה' );
		$sans   = "'IBM Plex Sans Hebrew',Arial,Helvetica,sans-serif";
		$btn    = function ( $url, $txt, $bg, $fg = '#FFFFFF' ) use ( $sans ) {
			return '<a href="' . esc_url( $url ) . '" style="display:inline-block;margin:0 0 8px 8px;background:' . $bg . ';color:' . $fg . ';border:1px solid ' . ( '#FFFFFF' === $bg ? '#B8C2C9' : $bg ) . ';font-family:' . $sans . ';font-weight:700;font-size:16px;line-height:20px;padding:13px 18px;border-radius:8px;text-decoration:none">' . esc_html( $txt ) . '</a>';
		};
		$row    = function ( $k, $v ) { return '' === $v ? '' : '<tr><td style="padding:7px 0;width:120px;color:#5E6A75;font-size:14px;vertical-align:top">' . esc_html( $k ) . '</td><td style="padding:7px 0;font-size:15px;color:#12202A">' . $v . '</td></tr>'; };
		$facts  = $row( 'מה מעניין', esc_html( $int ) )
			. ( $call ? $row( 'בקשה', '<b style="color:#B3261E">רוצה שיחה חוזרת</b>' ) : '' )
			. ( '' !== $note ? $row( 'שאל/ה', esc_html( $note ) ) : '' )
			. $row( 'אזור', esc_html( $city ) )
			. ( $pid ? $row( 'עמוד', '<a href="' . esc_url( get_permalink( $pid ) ) . '" style="color:#2F6F86">' . esc_html( $ptitle ) . '</a>' ) : '' )
			. $row( 'לפני ההרשמה', esc_html( $beh ) )
			. $row( 'עדכונים', esc_html( $al[ $m( 'pa_alerts' ) ] ?? $m( 'pa_alerts' ) ) )
			. $row( 'זמן', esc_html( get_the_date( 'j.n.Y H:i', $lid ) ) );
		$h1     = $call ? 'ליד חם: ביקש/ה שיחה' : 'ליד חדש: נרשם/ה לעדכוני מחירים';
		$html   = '<!doctype html><html lang="he" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="color-scheme" content="light"></head>'
			. '<body style="margin:0;padding:0;background:#F6F8F9"><div style="display:none;max-height:0;overflow:hidden">' . esc_html( $pretty . ' · ' . $city . ' · ' . $int ) . '</div>'
			. '<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:#F6F8F9"><tr><td align="center" style="padding:18px 10px">'
			. '<table role="presentation" width="100%" cellpadding="0" cellspacing="0" dir="rtl" style="max-width:560px;font-family:' . $sans . ';color:#12202A;text-align:right;background:#FFFFFF;border:1px solid #D3DCE2;border-radius:12px">'
			. '<tr><td style="background:#10262F;border-radius:12px 12px 0 0;padding:14px 18px;color:#CFE3EA;font-size:13px;font-weight:700">נדל״ן · חלון עדכוני מחירים · ' . esc_html( $city ) . '</td></tr>'
			. '<tr><td style="padding:18px 18px 6px"><div style="font-size:15px;color:#5E6A75;font-weight:700">' . esc_html( $h1 ) . '</div>'
			. '<div style="font-size:34px;line-height:40px;font-weight:800;letter-spacing:.5px;margin:6px 0 2px" dir="ltr"><a href="tel:' . esc_attr( $phone ) . '" style="color:#12202A;text-decoration:none">' . esc_html( $pretty ) . '</a></div>'
			. '<div style="font-size:15px;margin:0 0 14px" dir="ltr"><a href="mailto:' . esc_attr( $email ) . '" style="color:#2F6F86">' . esc_html( $email ) . '</a></div>'
			. $btn( 'tel:' . $phone, 'התקשר', '#2F6F86' ) . $btn( 'https://wa.me/' . $intl, 'וואטסאפ', '#0F7A63' ) . $btn( 'mailto:' . $email, 'מייל', '#FFFFFF', '#12202A' ) . '</td></tr>'
			. '<tr><td style="padding:4px 18px 8px"><table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="border-top:1px solid #E3E1DA">' . $facts . '</table></td></tr>'
			. '<tr><td style="padding:10px 18px 18px;border-top:1px solid #E3E1DA"><div style="font-size:13px;color:#5E6A75;margin:0 0 8px">אחרי שטיפלת, לחיצה אחת מעדכנת את הליד באתר:</div>'
			. $btn( nadlan_pa_act_url( $lid, 'contacted' ), 'חזרתי אליו', '#12202A' ) . $btn( nadlan_pa_act_url( $lid, 'lost' ), 'לא רלוונטי', '#FFFFFF', '#5E6A75' )
			. '<div style="font-size:12px;color:#5E6A75;margin-top:6px"><a href="' . esc_url( admin_url( 'post.php?post=' . (int) $lid . '&action=edit' ) ) . '" style="color:#5E6A75">פתיחה בניהול</a> · <a href="' . esc_url( admin_url( 'options-general.php?page=nadlan-nudge' ) ) . '" style="color:#5E6A75">כל הנרשמים (Excel)</a></div></td></tr>'
			. '</table></td></tr></table></body></html>';
		$subj = ( $call ? 'ליד חם · ביקש/ה שיחה · ' : 'ליד חדש · עדכוני מחירים · ' ) . $city . ( '' !== $int && ! $call ? ' · ' . $int : '' ) . ' · ' . $pretty;
		$ok = wp_mail( $to, $subj, $html, array( 'Content-Type: text/html; charset=UTF-8', 'Reply-To: ' . $email ) );
		update_post_meta( $lid, 'pa_owner_mail', $ok ? 'sent ' . gmdate( 'Y-m-d H:i' ) : 'failed ' . gmdate( 'Y-m-d H:i' ) );
		return $ok;
	}
}
add_action( 'rest_api_init', function () {
	/* admin only: send the owner mail of one price-alert lead again (the check after a release, or a lost mail) */
	register_rest_route( 'nadlan/v1', '/pa-resend', array( 'methods' => 'POST', 'permission_callback' => function () { return current_user_can( 'manage_options' ); }, 'callback' => function ( $req ) {
		$lid = (int) $req->get_param( 'l' );
		if ( 'nadlan_lead' !== get_post_type( $lid ) || 'price_alert' !== (string) get_post_meta( $lid, 'utm_source', true ) ) { return new WP_REST_Response( array( 'ok' => false ), 200 ); }
		return new WP_REST_Response( array( 'ok' => (bool) nadlan_pa_owner_mail( $lid ), 'to' => (string) get_option( 'admin_email' ) ), 200 );
	} ) );
	/* the two actions from the mail: GET shows one button (a mail scanner opening the link changes nothing), POST acts */
	register_rest_route( 'nadlan/v1', '/pa-act', array( 'methods' => array( 'GET', 'POST' ), 'permission_callback' => '__return_true', 'callback' => function ( $req ) {
		$lid = (int) $req->get_param( 'l' );
		$a   = (string) $req->get_param( 'a' );
		$s   = (string) $req->get_param( 's' );
		$lbl = array( 'contacted' => 'חזרתי אליו', 'lost' => 'לא רלוונטי' );
		$page = function ( $t, $body, $code = 200 ) {
			status_header( $code ); nocache_headers(); header( 'Content-Type: text/html; charset=utf-8' );
			echo '<!doctype html><html lang="he" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex"><title>' . esc_html( $t ) . '</title></head>'
				. '<body style="margin:0;font-family:Assistant,Arial,sans-serif;background:#F6F8F9;color:#12202A"><div style="max-width:460px;margin:40px auto;padding:22px;background:#fff;border:1px solid #D3DCE2;border-radius:12px">'
				. '<p style="margin:0 0 6px;font-size:13px;color:#5E6A75;font-weight:700">נדל״ן · ניהול לידים</p><h1 style="margin:0 0 12px;font-size:24px">' . esc_html( $t ) . '</h1>' . $body . '</div></body></html>'; // phpcs:ignore
			exit;
		};
		if ( ! $lid || ! isset( $lbl[ $a ] ) || ! hash_equals( nadlan_pa_sig( $lid, $a ), $s ) || 'nadlan_lead' !== get_post_type( $lid ) ) {
			$page( 'הקישור אינו בתוקף', '<p>אפשר לטפל בליד מתוך הניהול באתר.</p>' ); // 200: the uPress edge swaps a PHP 403 for its own page
		}
		$who = esc_html( (string) get_post_meta( $lid, 'phone', true ) );
		if ( 'POST' !== $req->get_method() ) {
			$page( $lbl[ $a ] . '?', '<p>הליד ' . $who . '</p><form method="post"><input type="hidden" name="l" value="' . $lid . '"><input type="hidden" name="a" value="' . esc_attr( $a ) . '"><input type="hidden" name="s" value="' . esc_attr( $s ) . '">'
				. '<button type="submit" style="font:700 17px Assistant,Arial,sans-serif;background:#2F6F86;color:#fff;border:0;border-radius:10px;padding:14px 22px;cursor:pointer">כן, ' . esc_html( $lbl[ $a ] ) . '</button></form>' );
		}
		$old = (string) get_post_meta( $lid, 'lead_status', true );
		update_post_meta( $lid, 'lead_status', $a );
		update_post_meta( $lid, 'pa_action_at', gmdate( 'Y-m-d H:i' ) . ' ' . $a );
		if ( function_exists( 'nadlan_lead_e2e_audit' ) ) { nadlan_lead_e2e_audit( array( 'lead_id' => $lid, 'card_id' => 0, 'user_id' => 0, 'old' => $old, 'new' => $a ) ); }
		$page( 'עודכן: ' . $lbl[ $a ], '<p>הליד ' . $who . ' סומן "' . esc_html( $lbl[ $a ] ) . '". אפשר לסגור את העמוד.</p>' );
	} ) );
} );

/* ---------- the sign-up ---------- */
if ( ! function_exists( 'nadlan_pa_phone' ) ) {
	/** an Israeli number as 05XXXXXXXX / 0XXXXXXXX, or '' */
	function nadlan_pa_phone( $s ) {
		$d = preg_replace( '/\D+/', '', (string) $s );
		if ( 0 === strpos( $d, '00972' ) ) { $d = substr( $d, 5 ); } elseif ( 0 === strpos( $d, '972' ) ) { $d = substr( $d, 3 ); }
		if ( '' !== $d && '0' !== $d[0] ) { $d = '0' . $d; }
		return preg_match( '/^05\d{8}$/', $d ) || preg_match( '/^0(?:[23489]|7\d)\d{7}$/', $d ) ? $d : '';
	}
}
if ( ! function_exists( 'nadlan_pa_consent_text' ) ) {
	function nadlan_pa_consent_text() {
		return 'אני רוצה לקבל מנדל״ן עדכוני מחירים ופרסומים בנושא נדל״ן, במייל, בטלפון ובוואטסאפ. אפשר להסיר בכל רגע.';
	}
}
if ( ! function_exists( 'nadlan_pa_signup' ) ) {
	function nadlan_pa_signup( $req ) {
		$r = function ( $data, $status = 200 ) { $o = new WP_REST_Response( $data, $status ); $o->header( 'Cache-Control', 'no-store' ); return $o; };
		$p = $req->get_json_params();
		if ( ! is_array( $p ) ) { $p = (array) $req->get_body_params(); }
		if ( ! empty( $p['company'] ) ) { return $r( array( 'ok' => true ) ); } // the honeypot: looks done, nothing is kept
		$id = absint( $p['id'] ?? 0 );
		if ( ! $id || ! nadlan_nudge_on( $id ) ) { return $r( array( 'ok' => false, 'error' => 'page' ), 400 ); }
		$phone = nadlan_pa_phone( $p['phone'] ?? '' );
		if ( '' === $phone ) { return $r( array( 'ok' => false, 'error' => 'phone' ), 400 ); }
		$email = sanitize_email( (string) ( $p['email'] ?? '' ) );
		if ( ! is_email( $email ) || strlen( $email ) > 100 ) { return $r( array( 'ok' => false, 'error' => 'email' ), 400 ); }
		if ( empty( $p['consent'] ) ) { return $r( array( 'ok' => false, 'error' => 'consent' ), 400 ); }
		$cl = function_exists( 'nadlan_hardening_client_key' ) ? nadlan_hardening_client_key() : 'ip' . md5( substr( (string) ( $_SERVER['REMOTE_ADDR'] ?? '' ), 0, 80 ) ); // phpcs:ignore -- hashed, never stored
		$lim = function ( $k, $max, $win ) { $k = 'nadlan_pa_rl_' . md5( $k ); $n = (int) get_transient( $k ); if ( $n >= $max ) { return false; } set_transient( $k, $n + 1, $win ); return true; };
		if ( ! $lim( 'c|' . $cl, 6, HOUR_IN_SECONDS ) || ! $lim( 'e|' . strtolower( $email ), 4, DAY_IN_SECONDS ) ) { return $r( array( 'ok' => false, 'error' => 'rate' ), 429 ); }
		$interest = in_array( (string) ( $p['interest'] ?? '' ), array( 'buy', 'own', 'invest', 'call' ), true ) ? (string) $p['interest'] : '';
		$labels   = array( 'buy' => 'קנייה באזור', 'own' => 'יש לי נכס באזור', 'invest' => 'השקעה', 'call' => 'ביקש/ה שיחה', '' => '' );
		$callback = ! empty( $p['callback'] ) || 'call' === $interest; // v106.4 (Ben 8.11.2026): "לאפשר לפנות אלינו סתם כי הוא רוצה לפנות"
		$note     = mb_substr( sanitize_textarea_field( (string) ( $p['note'] ?? '' ) ), 0, 400 );
		$trigger  = substr( sanitize_key( (string) ( $p['trigger'] ?? '' ) ), 0, 20 );
		$signals  = substr( preg_replace( '/[^a-z0-9+:]/', '', strtolower( (string) ( $p['sig'] ?? '' ) ) ), 0, 80 ); // e.g. read+price:a31:s44:p2
		$tr       = nadlan_pa_trend( $id );
		/* one sign-up per email and page a day: a repeat answers ok and keeps the first */
		$dup = get_posts( array( 'post_type' => 'nadlan_lead', 'post_status' => 'any', 'posts_per_page' => 1, 'fields' => 'ids', 'no_found_rows' => true, 'suppress_filters' => true,
			'date_query' => array( array( 'after' => '1 day ago' ) ),
			'meta_query' => array( array( 'key' => 'utm_source', 'value' => 'price_alert' ), array( 'key' => 'email', 'value' => $email ), array( 'key' => 'project_wp_id', 'value' => (string) $id ) ) ) );
		if ( $dup ) {
			if ( $callback && '1' !== (string) get_post_meta( (int) $dup[0], 'pa_callback', true ) ) { // the same person now asks for a call: never lose it
				update_post_meta( (int) $dup[0], 'pa_callback', '1' );
				update_post_meta( (int) $dup[0], 'goal', 'בקשת שיחה + עדכוני מחירים' );
				if ( '' !== $note ) { update_post_meta( (int) $dup[0], 'pa_note', $note ); }
				nadlan_pa_owner_mail( (int) $dup[0] );
			}
			return $r( array( 'ok' => true, 'again' => true, 'call' => $callback ) );
		}
		$where = '' !== $tr['city'] ? $tr['city'] : 'האזור';
		/* the behaviour before the sign-up, in words for the owner's mail (first 200 characters of the content are mailed) */
		$beh = '';
		if ( preg_match( '/^([a-z+]*):a(\d+):s(\d+):p(\d+)$/', $signals, $sm ) ) {
			$names = array( 'read' => 'קרא את העמוד', 'price' => 'ראה מחירים', 'explore' => 'השתמש בכלים בעמוד', 'pause' => 'עצר לקרוא', 'ret' => 'עמוד נוסף בביקור' );
			$said  = array();
			foreach ( array_filter( explode( '+', $sm[1] ) ) as $s ) { if ( isset( $names[ $s ] ) ) { $said[] = $names[ $s ]; } }
			$beh = 'לפני ההרשמה: ' . (int) $sm[2] . ' שניות פעילות מתוך ' . (int) $sm[3] . ', עמוד ' . (int) $sm[4] . ' בביקור' . ( $said ? '; ' . implode( ', ', $said ) : '' ) . ".\n";
		}
		$lid = wp_insert_post( array(
			'post_type'    => 'nadlan_lead',
			'post_status'  => 'private',
			'post_title'   => ( $callback ? 'בקשת שיחה + עדכוני מחירים · ' : 'עדכוני מחירים · ' ) . $where . ' · ' . current_time( 'Y-m-d H:i' ),
			'post_content' => ( $callback ? "ביקש/ה שיחה חוזרת.\n" : '' ) . ( '' !== $note ? 'שאל/ה: ' . $note . "\n" : '' ) . ( '' !== $labels[ $interest ] && 'call' !== $interest ? 'מעניין אותו/ה: ' . $labels[ $interest ] . ".\n" : '' ) . $beh . 'נרשם/ה לעדכוני מחירים מהעמוד ' . get_permalink( $id ),
		), true );
		if ( is_wp_error( $lid ) || ! $lid ) { return $r( array( 'ok' => false, 'error' => 'store' ), 500 ); }
		wp_clear_scheduled_hook( 'nadlan_lead_rich_alert', array( (int) $lid ) ); // the owner gets nadlan_pa_owner_mail() instead of the plain-text alert
		$meta = array(
			'phone'            => $phone,
			'email'            => $email,
			'goal'             => $callback ? 'בקשת שיחה + עדכוני מחירים' : 'עדכוני מחירים',
			'pa_callback'      => $callback ? '1' : '',
			'pa_note'          => $note,
			'topic'            => 'price_alert',
			'utm_source'       => 'price_alert',
			'source_url'       => get_permalink( $id ),
			'project_wp_id'    => (string) $id, // for the owner's alert mail only; never lead_card_id, so nothing routes it to an owner
			'project_title'    => wp_strip_all_tags( get_the_title( $id ) ),
			'city'             => $tr['city'],
			'pa_interest'      => $interest,
			'pa_trigger'       => $trigger,
			'pa_signals'       => $signals,
			'pa_trend'         => null === $tr['pct'] ? '' : $tr['src'] . ':' . $tr['pct'],
			'consent'          => 1,
			'consent_text'     => nadlan_pa_consent_text(),
			'consent_notice'   => NADLAN_PA_NOTICE,
			'consent_recorded' => current_time( 'mysql', true ),
			'lead_status'      => 'new',
			'lead_e2e_context' => 'price_alert',
			'lead_e2e_created_at' => time(),
			'lead_no_route'    => 1,
		);
		foreach ( $meta as $k => $v ) { if ( '' !== $v ) { update_post_meta( $lid, $k, $v ); } }
		if ( function_exists( 'nadlan_lead_e2e_audit' ) ) {
			nadlan_lead_e2e_audit( array( 'lead_id' => $lid, 'card_id' => 0, 'user_id' => 0, 'old' => 'created', 'new' => 'new' ) );
		}
		/* v106.3 (Ben 8.11.2026, "תדליק מנוע עדכונים אוטומטי"): the sign-up also asks the existing alert engine (inc/near-alerts.php)
		   for real, automatic updates: on a project, a change in its price per m², stage or units and new listings within 1.5 km; on a
		   listing, a drop in its price and new listings around it. The engine's own double opt-in applies: one confirmation mail, and
		   nothing else is sent until the visitor clicks it. Abroad (no Israeli point) and with the engine off, the lead alone stands. */
		$alerts = 'off';
		if ( function_exists( 'nadlan_na_enabled' ) && nadlan_na_enabled() && function_exists( 'nadlan_na_signup' ) ) {
			$lat = (float) get_post_meta( $id, 'lat', true );
			$lng = (float) get_post_meta( $id, 'lng', true );
			$alerts = 'no-point';
			if ( $lat && $lng && 'nadlan_intl' !== get_post_type( $id ) ) {
				$isp  = 'nadlan_property' === get_post_type( $id );
				$deal = $isp && 'rent' === (string) get_post_meta( $id, 'listing_type', true ) ? 'rent' : 'sale';
				$body = array( 'email' => $email, 'lat' => $lat, 'lng' => $lng, 'r' => 1.5, 'deal' => $deal, 'freq' => 'day', 'place' => $tr['city'], 'v' => NADLAN_PA_NOTICE,
					'what' => $isp ? array( 'drop', 'new' ) : array( 'proj', 'new' ) );
				if ( $isp ) { $body['items'] = array( $id ); } else { $body['follow'] = array( $id ); }
				$rq = new WP_REST_Request( 'POST', '/nadlan/v1/near-alerts' );
				$rq->set_header( 'content-type', 'application/json' );
				$rq->set_body( wp_json_encode( $body ) );
				try {
					$res  = nadlan_na_signup( $rq );
					$data = $res instanceof WP_REST_Response ? (array) $res->get_data() : array();
					$alerts = ! empty( $data['ok'] ) ? 'confirm-sent' : 'na-' . sanitize_key( (string) ( $data['error'] ?? 'fail' ) );
				} catch ( \Throwable $e ) {
					$alerts = 'na-error';
				}
			}
		}
		update_post_meta( $lid, 'pa_alerts', $alerts );
		nadlan_pa_owner_mail( (int) $lid );
		return $r( array( 'ok' => true, 'confirm' => 'confirm-sent' === $alerts, 'call' => $callback ) );
	}
}
add_action( 'rest_api_init', function () {
	register_rest_route( 'nadlan/v1', '/price-alert', array( 'methods' => 'POST', 'permission_callback' => '__return_true', 'callback' => 'nadlan_pa_signup' ) );
} );
add_filter( 'nadlan_hardening_public_post_routes', function ( $r ) { // the site's generic public-POST limit (inc/final-hardening.php)
	$r[] = '#^/nadlan/v1/price-alert$#';
	$r[] = '#^/nadlan/v1/pa-act$#';
	return $r;
} );

/* ---------- the page ---------- */
if ( ! function_exists( 'nadlan_pa_url' ) ) {
	function nadlan_pa_url( $rel ) { return plugins_url( 'assets/nudge/' . $rel, dirname( __DIR__ ) . '/nadlan-config.php' ); }
}
add_action( 'wp_enqueue_scripts', function () {
	if ( is_admin() || ! is_singular( array( 'nadlan_project', 'nadlan_property', 'nadlan_intl' ) ) || ! nadlan_nudge_on( (int) get_queried_object_id() ) ) { return; }
	$v = defined( 'NADLAN_CONFIG_VERSION' ) ? NADLAN_CONFIG_VERSION : '1';
	wp_enqueue_style( 'nadlan-pa', nadlan_pa_url( 'price-alert.css' ), array(), $v );
	wp_enqueue_script( 'nadlan-pa', nadlan_pa_url( 'price-alert.js' ), array(), $v, array( 'in_footer' => true, 'strategy' => 'defer' ) );
}, 30 );

add_action( 'wp_footer', function () {
	if ( is_admin() || ! is_singular( array( 'nadlan_project', 'nadlan_property', 'nadlan_intl' ) ) ) { return; }
	$id = (int) get_queried_object_id();
	if ( ! nadlan_nudge_on( $id ) ) { return; }
	$o    = nadlan_pa_opts();
	$type = get_post_type( $id );
	$tr   = nadlan_pa_trend( $id );
	$rent = 'nadlan_property' === $type && 'rent' === (string) get_post_meta( $id, 'listing_type', true );
	$down = ! $rent && $tr['down'];
	$own  = 'nadlan_project' === $type ? trim( (string) get_post_meta( $id, 'nadlan_nudge_text', true ) ) : '';
	$line = '' !== $own ? $own : ( $rent ? 'מחירי השכירות באזור זה משתנים' : ( $down ? 'המחירים באזור זה במגמת שינוי' : 'המחירים באזור זה משתנים' ) );
	$city = $tr['city'];
	$in   = '' !== $city ? 'ב' . $city : 'באזור';
	$wa   = function_exists( 'nadlan_cta_whatsapp_number' ) ? (string) nadlan_cta_whatsapp_number() : '';
	$wa1  = '' !== $wa ? 'https://wa.me/' . rawurlencode( $wa ) . '?text=' . rawurlencode( 'שלום, אשמח לקבל עדכון על מחירי הנדל״ן באזור. הגעתי מהעמוד: ' . get_permalink( $id ) ) : ''; // Ben's 105.7 wording
	$wa   = '' !== $wa ? 'https://wa.me/' . rawurlencode( $wa ) . '?text=' . rawurlencode( 'שלום, נרשמתי לעדכוני המחירים באתר ואשמח לשאול שאלה. הגעתי מהעמוד: ' . get_permalink( $id ) ) : '';
	$cfg  = array(
		'id' => $id, 't' => $type, 'api' => esc_url_raw( rest_url( 'nadlan/v1/price-alert' ) ),
		'f' => (int) $o['floor'], 'a1' => (int) $o['act1'], 'a2' => (int) $o['act2'], 'n' => (int) $o['need'],
		'dp' => (int) $o['depth'] / 100, 'q' => (int) $o['quiet'], 'qi' => (int) $o['quiet_ign'], 'h' => (int) $o['holdout'],
		'down' => $down ? 1 : 0, 'v' => NADLAN_PA_NOTICE,
	);
	$priv = function_exists( 'get_privacy_policy_url' ) && get_privacy_policy_url() ? get_privacy_policy_url() : home_url( '/privacy/' );
	$x    = '<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M6 6l12 12M18 6L6 18" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"/></svg>';
	$chev = '<svg viewBox="0 0 28 16" aria-hidden="true" focusable="false"><path d="M3 3l11 10L25 3" fill="none" stroke="currentColor" stroke-width="3.6" stroke-linecap="round" stroke-linejoin="round"/></svg>';
	?>
<div id="nlnu" class="nlpa-root" dir="rtl" hidden data-c="<?php echo esc_attr( wp_json_encode( $cfg ) ); ?>"><template id="nlpa-tpl">
<div class="nlpa" role="dialog" aria-modal="false" aria-labelledby="nlpa-h" aria-describedby="nlpa-sub" tabindex="-1" data-step="1">
	<div class="nlpa-board">
		<span class="nlpa-grab" aria-hidden="true"></span>
		<div class="nlpa-top">
			<p class="nlpa-kick"><span class="nlpa-live" aria-hidden="true"></span>נדל״ן · nad-lan.co.il<?php if ( '' !== $city ) : ?><span class="nlpa-city"><?php echo esc_html( $city ); ?></span><?php endif; ?></p>
			<button type="button" class="nlpa-x" aria-label="סגירה"><?php echo $x; // phpcs:ignore ?></button>
		</div>
		<div class="nlpa-head<?php echo $down ? ' is-down' : ''; ?>">
			<svg class="nlpa-warn" viewBox="0 0 32 29" aria-hidden="true" focusable="false"><path d="M13.4 2.2a3 3 0 0 1 5.2 0l12 20.8a3 3 0 0 1-2.6 4.5H4a3 3 0 0 1-2.6-4.5z" fill="currentColor"/><path d="M16 9.5v8" stroke="#10262f" stroke-width="3.2" stroke-linecap="round"/><circle cx="16" cy="22.4" r="2" fill="#10262f"/></svg>
			<div class="nlpa-htxt">
				<p class="nlpa-att">שימו לב</p>
				<p class="nlpa-h" id="nlpa-h" role="heading" aria-level="2"><?php echo esc_html( $line ); ?></p>
			</div>
			<?php if ( $down ) : ?><span class="nlpa-tick" aria-hidden="true"><?php echo $chev . $chev; // phpcs:ignore ?></span><?php endif; ?>
		</div>
	</div>
	<div class="nlpa-body">
		<p class="nlpa-sub" id="nlpa-sub">בשוק שזז, מחיר של לפני כמה חודשים כבר לא המחיר. הירשמו לעדכוני מחירים <?php echo esc_html( $in ); ?>, ותדעו על כל שינוי לפני שאתם מחליטים.</p>
		<div class="nlpa-s1">
			<p class="nlpa-q" id="nlpa-q"><?php if ( ! $down ) : ?><span class="nlpa-point" aria-hidden="true"><?php echo $chev; // phpcs:ignore ?></span><?php endif; ?>על מה לעדכן אתכם?</p>
			<div class="nlpa-chips" role="group" aria-labelledby="nlpa-q">
				<button type="button" class="nlpa-chip" data-i="buy">קנייה באזור</button>
				<button type="button" class="nlpa-chip" data-i="own">יש לי נכס באזור</button>
				<button type="button" class="nlpa-chip" data-i="invest">השקעה</button>
			</div>
			<div class="nlpa-or"><span>או ישר:</span><button type="button" class="nlpa-callme">שיחזרו אליי</button><?php if ( '' !== $wa1 ) : ?><a class="nlpa-wa-s" href="<?php echo esc_url( $wa1 ); ?>" target="_blank" rel="noopener">וואטסאפ</a><?php endif; ?></div>
		</div>
		<form class="nlpa-s2" novalidate>
			<p class="nlpa-q2">לאן לשלוח את העדכונים?</p>
			<div class="nlpa-f"><label for="nlpa-tel">טלפון נייד</label><p class="nlpa-hint" id="nlpa-tel-h">לעדכון מהיר בוואטסאפ כשיש שינוי. המספר לא עובר לאף אחד.</p><input id="nlpa-tel" name="phone" type="tel" inputmode="tel" autocomplete="tel-national" dir="ltr" placeholder="050-1234567" maxlength="20" required aria-describedby="nlpa-tel-h nlpa-tel-e"><p class="nlpa-e" id="nlpa-tel-e" aria-live="polite"></p></div>
			<div class="nlpa-f"><label for="nlpa-mail">אימייל</label><input id="nlpa-mail" name="email" type="email" inputmode="email" autocomplete="email" dir="ltr" placeholder="name@gmail.com" maxlength="100" required aria-describedby="nlpa-mail-e"><p class="nlpa-e" id="nlpa-mail-e" aria-live="polite"></p></div>
			<label class="nlpa-ok nlpa-cb"><input type="checkbox" name="callback" value="1"><span>אשמח גם שיחזרו אליי לשיחה קצרה על האזור</span></label>
			<div class="nlpa-f nlpa-note" hidden><label for="nlpa-note">מה תרצו לשאול? (לא חובה)</label><textarea id="nlpa-note" name="note" rows="2" maxlength="400"></textarea></div>
			<label class="nlpa-ok"><input type="checkbox" name="consent" value="1" required aria-describedby="nlpa-ok-e"><span><?php echo esc_html( nadlan_pa_consent_text() ); ?></span></label>
			<p class="nlpa-e" id="nlpa-ok-e" aria-live="polite"></p>
			<input class="nlpa-hp" type="text" name="company" tabindex="-1" autocomplete="off" aria-hidden="true">
			<button type="submit" class="nlpa-go"><span>כן, עדכנו אותי</span><svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M15 5l-7 7 7 7" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/></svg></button>
			<p class="nlpa-e nlpa-e--form" aria-live="polite"></p>
			<p class="nlpa-fine">מסירת הפרטים רשות, ובלעדיהם לא נוכל לשלוח עדכונים. הם נשמרים אצל נדל״ן (<bdi class="nlpa-nw">nad-lan.co.il</bdi>) רק כדי לשלוח לכם עדכונים, ולא יועברו ליזם, למתווך או לכל גורם אחר בלי הסכמה נפרדת. לעיון, לתיקון או למחיקה: <bdi class="nlpa-nw">info@nad-lan.co.il</bdi>. <a href="<?php echo esc_url( $priv ); ?>" target="_blank" rel="noopener">מדיניות הפרטיות</a></p>
		</form>
		<div class="nlpa-s3">
			<svg class="nlpa-check" viewBox="0 0 40 40" aria-hidden="true" focusable="false"><circle cx="20" cy="20" r="18" fill="#eaf4ef" stroke="#2e7d5b" stroke-width="2"/><path d="M12.5 20.5l5 5 10-11" fill="none" stroke="#2e7d5b" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round"/></svg>
			<p class="nlpa-done" tabindex="-1">נרשמתם לעדכוני המחירים</p>
			<p class="nlpa-sub2">נעדכן אתכם כשהמחירים <?php echo esc_html( $in ); ?> זזים. רוצים תשובה כבר עכשיו?</p>
			<p class="nlpa-callok" hidden>קיבלנו גם את הבקשה לשיחה: נחזור אליכם בהקדם למספר שמסרתם.</p>
			<p class="nlpa-conf" hidden>שלחנו לכם מייל קצר. לחיצה אחת בו מפעילה את העדכונים האוטומטיים (אם הוא לא מגיע, הציצו בספאם).</p>
			<?php if ( '' !== $wa ) : ?><a class="nlpa-wa" href="<?php echo esc_url( $wa ); ?>" target="_blank" rel="noopener"><svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path fill="currentColor" d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm0 18.2a8.2 8.2 0 0 1-4.2-1.2l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8s-.4-.1-.6.1l-.8 1c-.1.2-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.2-.4.2-.4.7-1.3.1-.2 0-.3 0-.4l-.8-1.9c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 3 3 0 0 0-.9 2.2 5.2 5.2 0 0 0 1.1 2.8 11.9 11.9 0 0 0 4.6 4c1.7.7 2.4.8 3.2.7a2.8 2.8 0 0 0 1.8-1.3 2.2 2.2 0 0 0 .2-1.3c-.1-.1-.3-.2-.5-.3z"/></svg>דברו איתנו בוואטסאפ</a><?php endif; ?>
			<button type="button" class="nlpa-later">סגירה</button>
		</div>
		<div class="nlpa-foot"><p class="nlpa-ind">אתר מידע עצמאי, לא מטעם יזם או מתווך.</p><button type="button" class="nlpa-later">לא עכשיו</button></div>
	</div>
</div>
</template></div>
	<?php
}, 40 );
