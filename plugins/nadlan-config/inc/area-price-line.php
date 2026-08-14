<?php
/**
 * Area price line under the project lead.
 *
 * Owner call 2026-08-05: the opening of a project page should carry an AREA
 * price signal because that is what the searcher came for - but never the
 * project's own prices, which are the developer's to publish. City-level
 * transaction medians are neutral public data; no developer can object to
 * "typical price per sqm recorded in the city".
 *
 * Data: the wp_nadlan_deals cache (avm-deals.php). Median price_per_sqm for
 * the project's city over the last 12 months, widened to 24 when thin, never
 * shown under 5 deals - an honest line or no line at all. Cached a day per
 * city. Renders only when the intent-first lead block leads the page, right
 * after the non-affiliation notice, so the reading order stays: lead,
 * notice, market context, everything else.
 *
 * @package nadlan-config
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

if ( ! function_exists( 'nadlan_apl_city_median' ) ) {
	/** @return array{psqm:int,n:int,months:int}|null */
	function nadlan_apl_city_median( $city ) {
		$city = trim( (string) $city );
		if ( '' === $city ) {
			return null;
		}
		$tkey = 'nlapl_' . md5( $city );
		$hit  = get_transient( $tkey );
		if ( is_array( $hit ) ) {
			return empty( $hit['psqm'] ) ? null : $hit;
		}
		global $wpdb;
		$table = $wpdb->prefix . 'nadlan_deals';
		$out   = null;
		foreach ( array( 12, 24 ) as $months ) {
			$vals = $wpdb->get_col( $wpdb->prepare(
				"SELECT price_per_sqm FROM $table WHERE city=%s AND price_per_sqm>0 AND deal_date >= DATE_SUB(CURDATE(), INTERVAL %d MONTH) ORDER BY deal_date DESC LIMIT 300",
				$city, $months
			) );
			$vals = array_map( 'floatval', array_filter( (array) $vals ) );
			$n    = count( $vals );
			if ( $n < 5 ) {
				continue;
			}
			sort( $vals );
			/* same 10% tail trim the AVM uses, one market voice */
			$trim = (int) floor( $n * 0.1 );
			$core = array_slice( $vals, $trim, max( 1, $n - 2 * $trim ) );
			$med  = $core[ (int) floor( count( $core ) / 2 ) ];
			$out  = array(
				'psqm'   => (int) ( round( $med / 100 ) * 100 ),
				'n'      => $n,
				'months' => $months,
			);
			break;
		}
		set_transient( $tkey, $out ? $out : array( 'psqm' => 0 ), DAY_IN_SECONDS );
		return $out;
	}
}

if ( ! function_exists( 'nadlan_apl_strings' ) ) {
	function nadlan_apl_strings( $lang ) {
		$all = array(
			'he' => 'מחיר אופייני למ"ר בעסקאות שנרשמו ב%1$s ב-%3$d החודשים האחרונים: כ-%2$s ש"ח (מתוך %4$d עסקאות במאגר). מחירי הפרויקט עצמו נמסרים אצל היזם.',
			'en' => 'Typical price per sqm recorded in %1$s over the last %3$d months: about NIS %2$s (from %4$d recorded deals). The project\'s own prices are provided by the developer.',
			'fr' => 'Prix typique au m2 enregistre a %1$s sur les %3$d derniers mois : environ %2$s NIS (sur %4$d transactions). Les prix du projet sont communiques par le promoteur.',
			'ru' => 'Типичная цена за кв. м по сделкам в %1$s за последние %3$d месяцев: около %2$s шекелей (по %4$d сделкам из базы). Цены самого проекта предоставляет застройщик.',
			'ar' => 'السعر النموذجي للمتر المربع في الصفقات المسجلة في %1$s خلال آخر %3$d شهرا: نحو %2$s شيكل (من %4$d صفقة). أسعار المشروع نفسه لدى المطور.',
		);
		return isset( $all[ $lang ] ) ? $all[ $lang ] : $all['he'];
	}
}

add_filter( 'the_content', function ( $content ) {
	if ( ! is_singular( 'nadlan_project' ) || ! in_the_loop() || ! is_main_query() ) {
		return $content;
	}
	/* only when the intent-first order actually leads the page */
	if ( 0 !== strpos( $content, '<div class="nl-lead">' ) ) {
		return $content;
	}
	static $done = false;
	if ( $done ) {
		return $content;
	}
	$done = true;
	$city = trim( (string) get_post_meta( get_the_ID(), 'city', true ) );
	$data = nadlan_apl_city_median( $city );
	if ( ! $data ) {
		return $content;
	}
	$lang = function_exists( 'nadlan_current_lang' ) ? nadlan_current_lang() : 'he';
	$rtl  = in_array( $lang, array( 'he', 'ar' ), true );
	$line = sprintf(
		nadlan_apl_strings( $lang ),
		esc_html( $city ),
		esc_html( number_format( $data['psqm'] ) ),
		(int) $data['months'],
		(int) $data['n']
	);
	$html = '<p class="nl-areaprice" dir="' . ( $rtl ? 'rtl' : 'ltr' ) . '">' . $line . '</p>';

	/* insertion point: after the notice when present, else after the lead */
	$pos = strpos( $content, '</div>' );
	if ( false === $pos ) {
		return $content;
	}
	$pos += 6;
	if ( substr( $content, $pos, 28 ) === '<aside class="nl-projnotice"' ) {
		$end = strpos( $content, '</aside>', $pos );
		if ( false !== $end ) {
			$pos = $end + 8;
		}
	}
	return substr( $content, 0, $pos ) . $html . substr( $content, $pos );
}, 22 );

add_action( 'wp_enqueue_scripts', function () {
	if ( ! is_singular( 'nadlan_project' ) ) {
		return;
	}
	wp_register_style( 'nadlan-apl', false, array(), NADLAN_CONFIG_VERSION );
	wp_enqueue_style( 'nadlan-apl' );
	wp_add_inline_style(
		'nadlan-apl',
		'.nl-areaprice{background:#F6F1E6;border:1px solid #E2DCD0;border-radius:10px;padding:10px 14px;' .
		'font-size:13.5px;line-height:1.6;color:#4B4639;margin:0 0 18px}'
	);
}, 22 );
