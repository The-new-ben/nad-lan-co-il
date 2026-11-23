<?php
/**
 * nadlan-config - the opening of /my-rentals/ for a visitor: the example landlord's portfolio on a 3D map
 * (HAD-795, owner's word 20.11.2026, design board 5: https://claude.ai/artifact/UnXWjYcZPJnARhMLhafL1C#page-b5).
 *
 * The example landlord: two apartments in a tower by Kikar HaMedina, two more in Tel Aviv, one each in Eilat, Limassol,
 * Athens and New York. Press a property: the map flies to its building in 3D; press the building: it comes forward
 * (the tower render turns under the finger), and the apartment's card opens: rent, tenant, state, the parts of the home.
 *
 * Honesty: EVERYTHING here is an example and says so on the frame and on each item. No developer name or logo, no real
 * unit numbers, no phone and no e-mail for the example people (1.72.728). The tower render of Kikar HaMedina is the
 * existing one of HAD-712, loaded read-only. The pictures of the other buildings and of the parts are illustrations.
 * Look: the site's showroom language (ink #14212b, sea #2f6f86, deep #0d2129, cyan #7fd3e6, Assistant, IBM Plex Mono for
 * numbers) with signal lights for state; not the page's older cream and terracotta.
 * No wheel or touch capture: the map uses cooperative gestures, the page scrolls under one finger.
 * The section carries the id nlpf and NOT the class of that name: the bare class .nlpf belongs to the professionals' card
 * (inc/directory.php), whose forced width and margins reached this stage on phones (found live, fixed in 1.72.731).
 */

if ( ! defined( 'ABSPATH' ) ) { exit; }

/* The product's name lives HERE and nowhere else (owner, 20.11.2026: a named product inside NadLan; working name, he may change it). */
if ( ! function_exists( 'nadlan_rm_brand' ) ) {
	function nadlan_rm_brand( $lang = 'he' ) {
		return 'he' === $lang ? array( 'השכרות', 'נדל״ן' ) : array( 'NadLan', 'Rentals' );
	}
}
if ( ! function_exists( 'nadlan_rm_brand_name' ) ) {
	function nadlan_rm_brand_name( $lang = 'he' ) { return implode( ' ', nadlan_rm_brand( $lang ) ); }
}
if ( ! function_exists( 'nadlan_rm_lockup' ) ) {
	/* the mark is the product's own lit floor: five floors, one lit */
	function nadlan_rm_lockup( $lang = 'he', $class = '' ) {
		$b = nadlan_rm_brand( $lang );
		return '<span class="nlrm-lk' . ( $class ? ' ' . esc_attr( $class ) : '' ) . '" dir="' . ( 'he' === $lang ? 'rtl' : 'ltr' ) . '">'
			. '<svg viewBox="0 0 40 40" width="34" height="34" aria-hidden="true" focusable="false"><rect x="9" y="4" width="22" height="5" rx="2.5"/><rect x="9" y="11" width="22" height="5" rx="2.5"/><rect class="nlrm-lk-lit" x="5" y="18" width="30" height="5" rx="2.5"/><rect x="9" y="25" width="22" height="5" rx="2.5"/><rect x="9" y="32" width="22" height="5" rx="2.5"/></svg>'
			. '<b>' . esc_html( $b[0] ) . '</b><i>' . esc_html( $b[1] ) . '</i></span>';
	}
}
if ( ! function_exists( 'nadlan_rm_one_line' ) ) {
	/* what it is, in plain words, before anything is touched */
	function nadlan_rm_one_line( $lang = 'he' ) {
		return 'he' === $lang ? 'ניהול דירות מושכרות במקום אחד: שוכרים, שכר דירה, חוזים ותיקונים.' : 'Managing the apartments you rent out in one place: tenants, rent, leases and repairs.';
	}
}

if ( ! function_exists( 'nadlan_rm_film_row' ) ) {
	/* The tutorial film (HAD-795, Ben 23.11.2026: "תעלה לאתר"; board https://claude.ai/artifact/SFpzAnjrdTW4qsYm3MmDr3#artboard-Placement).
	   One quiet row under the answer line: a poster and a play mark. Nothing loads until it is pressed (no video request, no
	   autoplay); pressed, the player opens in place under the row with its own controls, and "close" puts the row back.
	   The files live in the Media Library (ids 9295 he, 9296 en, 9297 poster), not in the plugin; captions are burned in. */
	function nadlan_rm_film_row( $lang = 'he' ) {
		$en  = ( 'he' !== $lang );
		$up  = content_url( '/uploads/2026/11/' );
		$ver = defined( 'NADLAN_CONFIG_VERSION' ) ? NADLAN_CONFIG_VERSION : '1';
		$src = $up . ( $en ? 'rentals-tutorial-en-phone.mp4' : 'rentals-tutorial-he-phone.mp4' );
		$pos = $up . 'rentals-tutorial-poster.webp';
		$t   = $en
			? array( 'k' => 'Video guide', 'b' => 'How it works, in two minutes', 's' => 'Add an apartment, the tenant reports no hot water, you handle it', 'n' => 'Hebrew narration, English captions', 'a' => 'Play the video guide, 2 minutes 2 seconds', 'x' => 'Close the video' )
			: array( 'k' => 'סרטון הדרכה', 'b' => 'איך זה עובד, בשתי דקות', 's' => 'מוסיפים דירה, השוכר מדווח שאין מים חמים, מטפלים', 'n' => '', 'a' => 'לנגן את סרטון ההדרכה, 2 דקות ו-2 שניות', 'x' => 'לסגור את הסרטון' );
		?>
<style>
#nlrm-film{--ink:#14212b;--sea:#2f6f86;--cy:#7fd3e6;max-width:560px;margin:14px auto 6px;text-align:start;font-family:'Assistant',Heebo,system-ui,sans-serif}
#nlrm-film button.nlrm-film-go{display:flex !important;align-items:center;gap:12px;width:100% !important;min-height:76px !important;margin:0 !important;padding:8px 14px 8px 8px !important;border:1px solid #d7e2e7 !important;border-radius:18px !important;background:#fff !important;color:var(--ink) !important;box-shadow:0 1px 2px rgba(13,33,41,.06) !important;cursor:pointer;text-align:start !important;font:inherit !important;text-transform:none !important;letter-spacing:0 !important;-webkit-appearance:none;appearance:none}
#nlrm-film[dir=rtl] button.nlrm-film-go{padding:8px 8px 8px 14px !important}
#nlrm-film button.nlrm-film-go[hidden],#nlrm-film .nlrm-film-n[hidden]{display:none !important}
#nlrm-film button.nlrm-film-go:hover{border-color:var(--sea) !important}
#nlrm-film button.nlrm-film-go:focus-visible,#nlrm-film button.nlrm-film-x:focus-visible{outline:3px solid var(--cy) !important;outline-offset:2px}
#nlrm-film .nlrm-film-th{position:relative;flex:none;width:112px;height:63px;border-radius:12px;overflow:hidden;background:#0d2129}
#nlrm-film .nlrm-film-th img{display:block;width:112px;height:63px;object-fit:cover}
#nlrm-film .nlrm-film-th i{position:absolute;inset:0;margin:auto;width:34px;height:34px;border-radius:50%;background:#fff;box-shadow:0 2px 8px rgba(0,0,0,.35)}
#nlrm-film .nlrm-film-th i:after{content:"";position:absolute;top:10px;left:13px;border-style:solid;border-width:7px 0 7px 11px;border-color:transparent transparent transparent var(--ink)}
#nlrm-film .nlrm-film-t{display:flex;flex-direction:column;gap:1px;min-width:0;flex:1}
#nlrm-film .nlrm-film-t small{font-weight:700;font-size:12.5px;line-height:1.3;color:var(--sea);letter-spacing:.02em}
#nlrm-film .nlrm-film-t b{font-weight:800;font-size:16.5px;line-height:1.3;color:var(--ink)}
#nlrm-film .nlrm-film-t span{font-weight:400;font-size:14px;line-height:1.35;color:#44545e}
#nlrm-film .nlrm-film-d{flex:none;font:600 13px/1 'IBM Plex Mono',ui-monospace,monospace;color:var(--ink);background:#eef4f6;border-radius:999px;padding:6px 9px}
#nlrm-film .nlrm-film-p{position:relative;margin:0;border-radius:18px;overflow:hidden;background:#0d2129;aspect-ratio:16/9}
#nlrm-film .nlrm-film-p video{display:block;width:100%;height:100%;background:#0d2129}
#nlrm-film button.nlrm-film-x{position:absolute;top:8px;inset-inline-end:8px;z-index:2;width:44px !important;height:44px !important;min-width:0 !important;min-height:0 !important;margin:0 !important;padding:0 !important;border:0 !important;border-radius:50% !important;background:rgba(13,33,41,.72) !important;color:#fff !important;font-weight:700 !important;font-size:22px !important;line-height:44px !important;font-family:inherit !important;cursor:pointer}
#nlrm-film .nlrm-film-n{margin:6px 4px 0;font-weight:400;font-size:13px;line-height:1.4;color:#5b6a73}
@media (max-width:420px){#nlrm-film .nlrm-film-th,#nlrm-film .nlrm-film-th img{width:96px;height:54px}#nlrm-film .nlrm-film-t span{font-size:13.5px}}
</style>
<div id="nlrm-film" dir="<?php echo $en ? 'ltr' : 'rtl'; ?>" lang="<?php echo $en ? 'en' : 'he'; ?>" data-src="<?php echo esc_url( $src ); ?>" data-poster="<?php echo esc_url( $pos ); ?>" data-lang="<?php echo $en ? 'en' : 'he'; ?>" data-close="<?php echo esc_attr( $t['x'] ); ?>">
	<button type="button" class="nlrm-film-go" aria-label="<?php echo esc_attr( $t['a'] ); ?>"><span class="nlrm-film-th"><img src="<?php echo esc_url( $pos ); ?>" width="112" height="63" alt="" decoding="async"><i aria-hidden="true"></i></span><span class="nlrm-film-t"><small><?php echo esc_html( $t['k'] ); ?></small><b><?php echo esc_html( $t['b'] ); ?></b><span><?php echo esc_html( $t['s'] ); ?></span></span><em class="nlrm-film-d" dir="ltr">2:02</em></button>
	<?php if ( $t['n'] ) : ?><p class="nlrm-film-n"><?php echo esc_html( $t['n'] ); ?></p><?php endif; ?>
</div>
<script defer src="<?php echo esc_url( plugins_url( 'assets/rentals/rm-film.js', dirname( __DIR__ ) ) . '?v=' . rawurlencode( $ver ) ); ?>"></script>
		<?php
	}
}

if ( ! function_exists( 'nadlan_rm_pf_data' ) ) {
	function nadlan_rm_pf_data( $lang = 'he' ) {
		$en = ( 'he' !== $lang );
		$x  = $en ? ' (example)' : ' (דוגמה)';
		$y1 = (int) gmdate( 'Y' ) + 1;
		$till = function ( $m_he, $m_en ) use ( $en, $y1 ) { return $en ? ( $m_en . ' ' . $y1 ) : ( $m_he . ' ' . $y1 ); };
		$ok_parts = function () use ( $en ) {
			return array(
				array( 'boiler', $en ? 'Water heater' : 'דוד מים', 'ok' ), array( 'ac', $en ? 'Air conditioner' : 'מזגן', 'ok' ),
				array( 'panel', $en ? 'Electric panel' : 'לוח חשמל', 'ok' ), array( 'fridge', $en ? 'Refrigerator' : 'מקרר', 'ok' ),
				array( 'washer', $en ? 'Washing machine' : 'מכונת כביסה', 'ok' ),
			);
		};
		$care_parts = $ok_parts();
		$care_parts[1][2] = 'care';
		/* The SAME portfolio as the app's own sample (assets/rentals/rm-demo.js): nine apartments in seven buildings; 'unit' is the
		   sample's unit id, so "enter the apartment" opens that apartment's real screens. A lab check keeps the two in step. */
		$T = function ( $he, $en_s ) use ( $en ) { return $en ? $en_s : $he; };
		$A = function ( $unit, $b, $pic, $region, $ll, $floors, $floor, $rooms, $sqm, $bname, $short, $city, $rent, $st, $line, $tenant, $care = '' ) use ( $x, $ok_parts ) {
			$parts = $ok_parts();
			if ( $care ) { foreach ( $parts as $k => $pt ) { if ( $pt[0] === $care ) { $parts[ $k ][2] = 'care'; } } }
			return array( 'id' => 'u' . $unit, 'unit' => $unit, 'b' => $b, 'pic' => $pic, 'region' => $region, 'll' => $ll, 'floors' => $floors, 'floor' => $floor, 'rooms' => $rooms, 'sqm' => $sqm,
				'bname' => $bname, 'short' => $short, 'name' => $bname . ' · ' . $short, 'city' => $city, 'rent' => $rent, 'st' => $st, 'line' => $line, 'tenant' => $tenant ? $tenant . $x : '', 'parts' => $parts );
		};
		$tlv = $T( 'תל אביב', 'Tel Aviv' );
		$props = array(
			$A( 21, 'kikar', 'k1', 'il', array( 34.79035, 32.08655 ), 40, 20, 4, 121, $T( 'כיכר המדינה', 'Kikar HaMedina' ), $T( 'דירה לדוגמה א', 'Example apartment A' ), $tlv, '17,800 ₪', 'care',
				$T( 'חוב של חודשיים · הדוד לא מחמם מים', 'Two months unpaid · the water heater does not heat' ), $T( 'רון מזרחי', 'Ron Mizrahi' ), 'boiler' ),
			$A( 22, 'kikar', 'k1', 'il', array( 34.78985, 32.08672 ), 40, 30, 5, 148, $T( 'כיכר המדינה', 'Kikar HaMedina' ), $T( 'דירה לדוגמה ב', 'Example apartment B' ), $tlv, '21,500 ₪', 'due',
				$T( 'פנויה · שלושה מתעניינים', 'Vacant · three applicants' ), '' ),
			$A( 12, 't1', 't1', 'il', array( 34.78370, 32.08760 ), 5, 5, 4, 95, $T( 'ארלוזורוב 78', '78 Arlozorov' ), $T( 'דירה 14', 'Apartment 14' ), $tlv, '6,400 ₪', 'due',
				$T( 'שכר הדירה של החודש עוד לא התקבל', 'This month\'s rent has not come in yet' ), $T( 'דנה כהן', 'Dana Cohen' ) ),
			$A( 31, 'e1', 'e1', 'il', array( 34.93700, 29.55000 ), 3, 2, 3, 80, $T( 'שחמון 5', '5 Shahamon' ), $T( 'דירה 5', 'Apartment 5' ), $T( 'אילת', 'Eilat' ), '4,900 ₪', 'due',
				$T( 'השוכר דיווח ששילם, מחכה לאישור שלכם', 'The tenant reported a payment; it waits for your confirmation' ), 'Daniel Brooks' ),
			$A( 11, 't1', 't1', 'il', array( 34.78370, 32.08760 ), 5, 3, 3, 72, $T( 'ארלוזורוב 78', '78 Arlozorov' ), $T( 'דירה 7', 'Apartment 7' ), $tlv, '7,800 ₪', 'ok',
				$T( 'שכר הדירה של החודש התקבל', 'This month\'s rent is in' ), $T( 'משפחת לוי', 'The Levi family' ) ),
			$A( 41, 't2', 't2', 'il', array( 34.77020, 32.05630 ), 3, 2, 2.5, 58, $T( 'פלורנטין 12', '12 Florentin' ), $T( 'דירה 3', 'Apartment 3' ), $tlv, '5,900 ₪', 'ok',
				$T( 'הכול בסדר', 'All in order' ), $T( 'נועה ברק', 'Noa Barak' ) ),
			$A( 51, 'c1', 'c1', 'med', array( 33.04500, 34.68500 ), 6, 4, 3, 95, $T( 'לימסול, מול הים', 'Limassol, by the sea' ), $T( 'דירה מול הים', 'Seafront apartment' ), $T( 'קפריסין', 'Cyprus' ), '5,800 ₪', 'ok',
				$T( 'הכול בסדר', 'All in order' ), 'Andreas P.' ),
			$A( 61, 'g1', 'g1', 'med', array( 23.74300, 37.97900 ), 6, 5, 2, 64, $T( 'אתונה, קולונאקי', 'Athens, Kolonaki' ), $T( 'דירה בקולונאקי', 'Kolonaki apartment' ), $T( 'יוון', 'Greece' ), '4,700 ₪', 'ok',
				$T( 'הכול בסדר', 'All in order' ), 'Eleni K.' ),
			$A( 71, 'n1', 'n1', 'ny', array( -73.98400, 40.75100 ), 12, 8, 2, 70, $T( 'מנהטן, רחוב 38', 'Manhattan, 38th Street' ), $T( 'דירה ברחוב 38', '38th Street apartment' ), $T( 'ניו יורק', 'New York' ), '15,900 ₪', 'ok',
				$T( 'הכול בסדר', 'All in order' ), 'Sarah Klein' ),
		);
		/* the two tower apartments carry a short tag beside their lit floors */
		$props[0]['tag'] = $T( 'דוגמה א', 'Example A' );
		$props[1]['tag'] = $T( 'דוגמה ב', 'Example B' );
		$w = $en ? array(
			'title' => 'My properties', 'ex' => 'Example portfolio', 'ex1' => 'Example', 'all' => 'All', 'care' => 'Urgent', 'due' => 'This week', 'ok' => 'In order', 'vacant' => 'No tenant yet', 'ask' => 'Asking rent',
			'c_care' => 'Urgent', 'c_due' => 'This week', 'c_ok' => 'In order', 'filter' => 'Filter my properties', 'map' => 'The map of the properties', 'props' => 'The properties',
			'one_care' => 'One apartment needs care now', 'see' => 'See it', 'n_props' => '{n} apartments', 'hint' => 'Press an apartment to fly to it.', 'fix' => 'Handle it now',
			'world' => 'The whole world', 'back_map' => 'Back to the map', 'floor' => 'Floor', 'of' => 'of', 'rooms' => 'rooms', 'sqm' => 'sq m', 'rent' => 'Rent a month', 'tenant' => 'Tenant', 'lease' => 'Lease until',
			'home' => 'The parts of the home', 'p_ok' => 'in order', 'p_care' => 'needs care', 'turn' => 'Drag to turn the tower', 'note' => 'Illustration · example homes and figures',
			'apts' => '{n} example apartments in the building', 'apt1' => 'One example apartment in the building', 'cta' => 'Start my own', 'enter' => 'Open the apartment', 'enter_b' => 'Enter the building', 'demo' => 'Full demo',
			'places' => array( 'il' => 'Israel', 'med' => 'Cyprus and Greece', 'ny' => 'New York', 'near' => 'Israel and around' ),
			'gesture' => 'Use two fingers to move the map', 'ctrl' => 'Use ctrl + scroll to zoom the map', 'cmd' => 'Use ⌘ + scroll to zoom the map',
		) : array(
			'title' => 'הנכסים שלי', 'ex' => 'תיק לדוגמה', 'ex1' => 'דוגמה', 'all' => 'הכול', 'care' => 'דחוף', 'due' => 'לטיפול השבוע', 'ok' => 'תקין', 'vacant' => 'אין שוכר עדיין', 'ask' => 'שכר מבוקש',
			'c_care' => 'דחוף', 'c_due' => 'השבוע', 'c_ok' => 'תקין', 'filter' => 'סינון הנכסים שלי', 'map' => 'המפה של הנכסים', 'props' => 'הנכסים',
			'one_care' => 'דירה אחת צריכה טיפול עכשיו', 'see' => 'לראות', 'n_props' => '{n} דירות', 'hint' => 'לחצו על דירה כדי לטוס אליה.', 'fix' => 'לטפל עכשיו',
			'world' => 'כל העולם', 'back_map' => 'חזרה למפה', 'floor' => 'קומה', 'of' => 'מתוך', 'rooms' => 'חדרים', 'sqm' => 'מ״ר', 'rent' => 'שכר דירה לחודש', 'tenant' => 'שוכר', 'lease' => 'החוזה עד',
			'home' => 'המערכות של הדירה', 'p_ok' => 'תקין', 'p_care' => 'צריך טיפול', 'turn' => 'גררו כדי לסובב את המגדל', 'note' => 'הדמיה · דירות ונתונים לדוגמה',
			'apts' => '{n} דירות לדוגמה בבניין', 'apt1' => 'דירה אחת לדוגמה בבניין', 'cta' => 'להתחיל עם הדירה שלי', 'enter' => 'להיכנס לדירה', 'enter_b' => 'להיכנס לבניין', 'demo' => 'ההדגמה המלאה',
			'places' => array( 'il' => 'ישראל', 'med' => 'קפריסין ויוון', 'ny' => 'ניו יורק', 'near' => 'ישראל והסביבה' ),
			'gesture' => 'השתמשו בשתי אצבעות כדי להזיז את המפה', 'ctrl' => 'החזיקו ctrl וגללו כדי להתקרב במפה', 'cmd' => 'החזיקו ⌘ וגללו כדי להתקרב במפה',
		);
		return array( 'props' => $props, 'w' => $w );
	}
}

if ( ! function_exists( 'nadlan_rm_portfolio_stage' ) ) {
	function nadlan_rm_portfolio_stage( $lang = 'he', $go = '', $sample = '' ) {
		$en   = ( 'he' !== $lang );
		$d    = nadlan_rm_pf_data( $lang );
		$w    = $d['w'];
		$ver  = defined( 'NADLAN_CONFIG_VERSION' ) ? NADLAN_CONFIG_VERSION : '1';
		$base = plugins_url( 'assets/rentals/portfolio/', dirname( __DIR__ ) );
		$turn = plugins_url( 'assets/project-stage/hamedina/turn/', dirname( __DIR__ ) );
		$tok  = function_exists( 'nadlan_mapbox_token' ) ? nadlan_mapbox_token() : '';
		$sign = array( 'care' => '!', 'due' => '', 'ok' => '' );
		?>
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Assistant:wght@400;600;700;800&amp;family=IBM+Plex+Mono:wght@500;600&amp;display=swap">
<link rel="stylesheet" href="<?php echo esc_url( $base . 'pf.css?v=' . rawurlencode( $ver ) ); ?>">
<section id="nlpf" class="nlmyrent-stage" dir="<?php echo $en ? 'ltr' : 'rtl'; ?>" lang="<?php echo esc_attr( $en ? 'en' : 'he' ); ?>" aria-label="<?php echo esc_attr( $w['title'] . ' · ' . $w['ex'] ); ?>"
	data-lang="<?php echo esc_attr( $en ? 'en' : 'he' ); ?>" data-token="<?php echo esc_attr( $tok ); ?>" data-base="<?php echo esc_url( $base ); ?>" data-turn="<?php echo esc_url( $turn ); ?>"
	data-go="<?php echo esc_url( $go ); ?>" data-sample="<?php echo esc_url( $sample ); ?>" data-pf="<?php echo esc_attr( wp_json_encode( $d, JSON_UNESCAPED_UNICODE ) ); ?>">
	<picture class="nlpf-poster" aria-hidden="true"><source media="(max-width: 700px)" srcset="<?php echo esc_url( $base . 'img/poster-' . ( $en ? 'en' : 'he' ) . '-phone.webp?v=' . rawurlencode( $ver ) ); ?>"><img src="<?php echo esc_url( $base . 'img/poster-' . ( $en ? 'en' : 'he' ) . '-desk.webp?v=' . rawurlencode( $ver ) ); ?>" alt="" decoding="async" fetchpriority="high"></picture>
	<div class="nlpf-map" id="nlpf-map" aria-label="<?php echo esc_attr( $w['map'] ); ?>"></div>
	<div class="nlpf-marks"></div>
	<div class="nlpf-top">
		<div class="nlpf-h"><div class="nlpf-title" role="heading" aria-level="2"><?php echo esc_html( $w['title'] ); ?></div><span class="nlpf-ex"><?php echo esc_html( $w['ex'] ); ?></span></div>
		<div class="nlpf-chips" role="group" aria-label="<?php echo esc_attr( $w['filter'] ); ?>"></div>
	</div>
	<div class="nlpf-say" aria-live="polite"></div>
	<div class="nlpf-tray" aria-label="<?php echo esc_attr( $w['props'] ); ?>"><div class="nlpf-cards">
		<?php foreach ( $d['props'] as $p ) : ?>
		<button type="button" class="nlpf-card is-<?php echo esc_attr( $p['st'] ); ?>" data-id="<?php echo esc_attr( $p['id'] ); ?>"><span class="nlpf-th"><img src="<?php echo esc_url( $base . 'img/' . $p['pic'] . '-192.webp' ); ?>" alt="" width="96" height="96" decoding="async"></span><i class="nlpf-bd nlpf-bd--<?php echo esc_attr( $p['st'] ); ?>" aria-hidden="true"><?php echo esc_html( $sign[ $p['st'] ] ); ?></i><span class="nlpf-card-t"><b><?php echo esc_html( $p['name'] ); ?></b><small><?php echo esc_html( $p['city'] . ' · ' . $w[ $p['st'] ] ); ?></small><em class="nlpf-mono"><?php echo esc_html( $p['rent'] ); ?></em></span></button>
		<?php endforeach; ?>
	</div></div>
	<div class="nlpf-panel" hidden></div>
</section>
<script defer src="<?php echo esc_url( $base . 'pf.js?v=' . rawurlencode( $ver ) ); ?>"></script>
		<?php
	}
}
