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
		$props = array(
			array( 'id' => 'k1', 'b' => 'kikar', 'pic' => 'k1', 'region' => 'il', 'll' => array( 34.78985, 32.08672 ), 'floors' => 40, 'floor' => 30, 'rooms' => 5, 'sqm' => 148,
				'name' => $en ? 'Kikar HaMedina · example apartment B' : 'כיכר המדינה · דירה לדוגמה ב', 'short' => $en ? 'Example apartment B' : 'דירה לדוגמה ב', 'tag' => $en ? 'Example B' : 'דוגמה ב', 'bname' => $en ? 'Kikar HaMedina' : 'כיכר המדינה',
				'city' => $en ? 'Tel Aviv' : 'תל אביב', 'rent' => '21,500 ₪', 'st' => 'ok', 'line' => $en ? 'This month\'s rent is in' : 'שכר הדירה של החודש התקבל',
				'tenant' => ( $en ? 'The Alon family' : 'משפחת אלון' ) . $x, 'lease' => $till( 'יוני', 'June' ), 'parts' => $ok_parts() ),
			array( 'id' => 'k2', 'b' => 'kikar', 'pic' => 'k1', 'region' => 'il', 'll' => array( 34.79035, 32.08655 ), 'floors' => 40, 'floor' => 20, 'rooms' => 4, 'sqm' => 121,
				'name' => $en ? 'Kikar HaMedina · example apartment A' : 'כיכר המדינה · דירה לדוגמה א', 'short' => $en ? 'Example apartment A' : 'דירה לדוגמה א', 'tag' => $en ? 'Example A' : 'דוגמה א', 'bname' => $en ? 'Kikar HaMedina' : 'כיכר המדינה',
				'city' => $en ? 'Tel Aviv' : 'תל אביב', 'rent' => '17,800 ₪', 'st' => 'due', 'line' => $en ? 'Rent is due in 3 days' : 'שכר דירה בעוד 3 ימים',
				'tenant' => ( $en ? 'Noa Barak' : 'נועה ברק' ) . $x, 'lease' => $till( 'מרץ', 'March' ), 'parts' => $ok_parts() ),
			array( 'id' => 't1', 'b' => 't1', 'pic' => 't1', 'region' => 'il', 'll' => array( 34.78370, 32.08760 ), 'floors' => 4, 'floor' => 3, 'rooms' => 3, 'sqm' => 72,
				'name' => $en ? '78 Arlozorov · apartment 7' : 'ארלוזורוב 78 · דירה 7', 'short' => $en ? 'Apartment 7' : 'דירה 7', 'bname' => $en ? '78 Arlozorov' : 'ארלוזורוב 78',
				'city' => $en ? 'Tel Aviv' : 'תל אביב', 'rent' => '7,800 ₪', 'st' => 'ok', 'line' => $en ? 'All in order' : 'הכול בסדר',
				'tenant' => ( $en ? 'The Levi family' : 'משפחת לוי' ) . $x, 'lease' => $till( 'אוגוסט', 'August' ), 'parts' => $ok_parts() ),
			array( 'id' => 't2', 'b' => 't2', 'pic' => 't2', 'region' => 'il', 'll' => array( 34.77020, 32.05630 ), 'floors' => 3, 'floor' => 2, 'rooms' => 2.5, 'sqm' => 58,
				'name' => $en ? '12 Florentin · apartment 3' : 'פלורנטין 12 · דירה 3', 'short' => $en ? 'Apartment 3' : 'דירה 3', 'bname' => $en ? '12 Florentin' : 'פלורנטין 12',
				'city' => $en ? 'Tel Aviv' : 'תל אביב', 'rent' => '6,400 ₪', 'st' => 'ok', 'line' => $en ? 'All in order' : 'הכול בסדר',
				'tenant' => ( $en ? 'Dana Cohen' : 'דנה כהן' ) . $x, 'lease' => $till( 'ינואר', 'January' ), 'parts' => $ok_parts() ),
			array( 'id' => 'e1', 'b' => 'e1', 'pic' => 'e1', 'region' => 'il', 'll' => array( 34.93700, 29.55000 ), 'floors' => 3, 'floor' => 2, 'rooms' => 3, 'sqm' => 80,
				'name' => $en ? '5 Shahamon · apartment 5' : 'שחמון 5 · דירה 5', 'short' => $en ? 'Apartment 5' : 'דירה 5', 'bname' => $en ? '5 Shahamon' : 'שחמון 5',
				'city' => $en ? 'Eilat' : 'אילת', 'rent' => '4,900 ₪', 'st' => 'care', 'line' => $en ? 'The air conditioner is not cooling · opened yesterday' : 'המזגן לא מקרר · נפתחה אתמול',
				'tenant' => ( $en ? 'Ron Mizrahi' : 'רון מזרחי' ) . $x, 'lease' => $till( 'אוקטובר', 'October' ), 'parts' => $care_parts ),
			array( 'id' => 'c1', 'b' => 'c1', 'pic' => 'c1', 'region' => 'med', 'll' => array( 33.04500, 34.68500 ), 'floors' => 6, 'floor' => 4, 'rooms' => 3, 'sqm' => 95,
				'name' => $en ? 'Limassol, by the sea' : 'לימסול, מול הים', 'short' => $en ? 'Seafront apartment' : 'דירה מול הים', 'bname' => $en ? 'Limassol, by the sea' : 'לימסול, מול הים',
				'city' => $en ? 'Cyprus' : 'קפריסין', 'rent' => '1,450 €', 'st' => 'ok', 'line' => $en ? 'All in order' : 'הכול בסדר',
				'tenant' => 'Andreas P.' . $x, 'lease' => $till( 'מאי', 'May' ), 'parts' => $ok_parts() ),
			array( 'id' => 'g1', 'b' => 'g1', 'pic' => 'g1', 'region' => 'med', 'll' => array( 23.74300, 37.97900 ), 'floors' => 6, 'floor' => 5, 'rooms' => 2, 'sqm' => 64,
				'name' => $en ? 'Athens, Kolonaki' : 'אתונה, קולונאקי', 'short' => $en ? 'Kolonaki apartment' : 'דירה בקולונאקי', 'bname' => $en ? 'Athens, Kolonaki' : 'אתונה, קולונאקי',
				'city' => $en ? 'Greece' : 'יוון', 'rent' => '1,200 €', 'st' => 'ok', 'line' => $en ? 'All in order' : 'הכול בסדר',
				'tenant' => 'Eleni K.' . $x, 'lease' => $till( 'ספטמבר', 'September' ), 'parts' => $ok_parts() ),
			array( 'id' => 'n1', 'b' => 'n1', 'pic' => 'n1', 'region' => 'ny', 'll' => array( -73.98400, 40.75100 ), 'floors' => 12, 'floor' => 8, 'rooms' => 2, 'sqm' => 70,
				'name' => $en ? 'Manhattan, 38th Street' : 'מנהטן, רחוב 38', 'short' => $en ? '38th Street apartment' : 'דירה ברחוב 38', 'bname' => $en ? 'Manhattan, 38th Street' : 'מנהטן, רחוב 38',
				'city' => $en ? 'New York' : 'ניו יורק', 'rent' => '4,300 $', 'st' => 'ok', 'line' => $en ? 'All in order' : 'הכול בסדר',
				'tenant' => 'Daniel Brooks' . $x, 'lease' => $till( 'דצמבר', 'December' ), 'parts' => $ok_parts() ),
		);
		$w = $en ? array(
			'title' => 'My properties', 'ex' => 'Example portfolio', 'ex1' => 'Example', 'all' => 'All', 'care' => 'Needs care', 'due' => 'Due this week', 'ok' => 'In order',
			'c_care' => 'Care', 'c_due' => 'Due', 'c_ok' => 'In order', 'filter' => 'Filter my properties', 'map' => 'The map of the properties', 'props' => 'The properties',
			'one_care' => 'One property needs care', 'see' => 'See it', 'n_props' => '{n} properties', 'hint' => 'Press a property to fly to it.', 'enter' => 'Enter the building', 'fix' => 'Handle it now',
			'world' => 'The whole world', 'back_map' => 'Back to the map', 'floor' => 'Floor', 'of' => 'of', 'rooms' => 'rooms', 'sqm' => 'sq m', 'rent' => 'Rent a month', 'tenant' => 'Tenant', 'lease' => 'Lease until',
			'home' => 'The parts of the home', 'p_ok' => 'in order', 'p_care' => 'needs care', 'turn' => 'Drag to turn the tower', 'note' => 'Illustration · example homes and figures',
			'apts' => '{n} example apartments in the tower', 'apt1' => 'One example apartment in the building', 'cta' => 'Start managing, free', 'demo' => 'Full demo',
			'places' => array( 'il' => 'Israel', 'med' => 'Cyprus and Greece', 'ny' => 'New York', 'near' => 'Israel and around' ),
			'gesture' => 'Use two fingers to move the map', 'ctrl' => 'Use ctrl + scroll to zoom the map', 'cmd' => 'Use ⌘ + scroll to zoom the map',
		) : array(
			'title' => 'הנכסים שלי', 'ex' => 'תיק לדוגמה', 'ex1' => 'דוגמה', 'all' => 'הכול', 'care' => 'צריך טיפול', 'due' => 'לתשלום השבוע', 'ok' => 'תקין',
			'c_care' => 'טיפול', 'c_due' => 'לתשלום', 'c_ok' => 'תקין', 'filter' => 'סינון הנכסים שלי', 'map' => 'המפה של הנכסים', 'props' => 'הנכסים',
			'one_care' => 'נכס אחד צריך טיפול', 'see' => 'לראות', 'n_props' => '{n} נכסים', 'hint' => 'לחצו על נכס כדי לטוס אליו.', 'enter' => 'להיכנס לבניין', 'fix' => 'לטפל עכשיו',
			'world' => 'כל העולם', 'back_map' => 'חזרה למפה', 'floor' => 'קומה', 'of' => 'מתוך', 'rooms' => 'חדרים', 'sqm' => 'מ״ר', 'rent' => 'שכר דירה לחודש', 'tenant' => 'שוכר', 'lease' => 'החוזה עד',
			'home' => 'המערכות של הדירה', 'p_ok' => 'תקין', 'p_care' => 'צריך טיפול', 'turn' => 'גררו כדי לסובב את המגדל', 'note' => 'הדמיה · דירות ונתונים לדוגמה',
			'apts' => '{n} דירות לדוגמה במגדל', 'apt1' => 'דירה אחת לדוגמה בבניין', 'cta' => 'להתחיל לנהל, חינם', 'demo' => 'ההדגמה המלאה',
			'places' => array( 'il' => 'ישראל', 'med' => 'קפריסין ויוון', 'ny' => 'ניו יורק', 'near' => 'ישראל והסביבה' ),
			'gesture' => 'השתמשו בשתי אצבעות כדי להזיז את המפה', 'ctrl' => 'החזיקו ctrl וגללו כדי להתקרב במפה', 'cmd' => 'החזיקו ⌘ וגללו כדי להתקרב במפה',
		);
		return array( 'props' => $props, 'w' => $w );
	}
}

if ( ! function_exists( 'nadlan_rm_portfolio_stage' ) ) {
	function nadlan_rm_portfolio_stage( $lang = 'he', $go = '' ) {
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
	data-go="<?php echo esc_url( $go ); ?>" data-pf="<?php echo esc_attr( wp_json_encode( $d, JSON_UNESCAPED_UNICODE ) ); ?>">
	<div class="nlpf-globe" aria-hidden="true"><i></i></div>
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
