<?php
require __DIR__ . '/harness2.php';
$j    = json_decode( file_get_contents( __DIR__ . '/tr.json' ), true );
$f    = $j['f'];
$text = $j['text'];
$tr   = $j['tr'];
foreach ( $tr['names'] as $l => $nm ) { foreach ( $nm as $k => $v ) { if ( $v !== '' ) { $f[ $k . '_' . $l ] = $v; } } }
$he_en = nl_drop_finish_copy( array(), $f, $text );   // the plain Hebrew and English pages
$copy  = array_merge( $he_en, $tr['copy'] );
// a broker who joined alone: Hebrew site 8001, English 8002, Russian 8003, French 8004
$GLOBALS['POSTS'] = array(
	7900 => array( 'post_type' => 'nadlan_professional', 'status' => 'publish', 'post_title' => 'ישראל ישראלי · ישראלי נכסים' ),
	8001 => array( 'post_type' => 'page', 'status' => 'publish', 'link' => 'https://nad-lan.co.il/brokers/israel-israeli/', 'post_name' => 'israel-israeli' ),
	8002 => array( 'post_type' => 'page', 'status' => 'publish', 'link' => 'https://nad-lan.co.il/en/brokers/israel-israeli/' ),
	8003 => array( 'post_type' => 'page', 'status' => 'publish', 'link' => 'https://nad-lan.co.il/ru/brokers/israel-israeli/' ),
	8004 => array( 'post_type' => 'page', 'status' => 'publish', 'link' => 'https://nad-lan.co.il/fr/brokers/israel-israeli/' ),
	9001 => array( 'post_type' => 'nadlan_property', 'status' => 'publish', 'post_title' => nl_drop_fill( $copy['he']['title'], $f, 'he' ), 'link' => 'https://nad-lan.co.il/properties/nofei-yam-3-rooms-for-rent/' ),
	9002 => array( 'post_type' => 'page', 'status' => 'publish', 'post_title' => nl_drop_fill( $copy['en']['title'], $f, 'en' ), 'link' => 'https://nad-lan.co.il/en/brokers/israel-israeli/nofei-yam-3-rooms-for-rent/' ),
	9003 => array( 'post_type' => 'page', 'status' => 'publish', 'post_title' => nl_drop_fill( $copy['ru']['title'], $f, 'ru' ), 'link' => 'https://nad-lan.co.il/ru/brokers/israel-israeli/nofei-yam-3-rooms-for-rent/' ),
	9004 => array( 'post_type' => 'page', 'status' => 'publish', 'post_title' => nl_drop_fill( $copy['fr']['title'], $f, 'fr' ), 'link' => 'https://nad-lan.co.il/fr/brokers/israel-israeli/nofei-yam-3-rooms-for-rent/' ),
);
$GLOBALS['META'][7900] = array( 'nl_name_he' => 'ישראל ישראלי', 'nl_name_en' => 'Israel Israeli', 'company_name' => 'ישראלי נכסים', 'nl_brand_en' => 'Israeli Properties', 'license_number' => '1234567', 'phone' => '050-1234567',
	'nl_gender' => 'm', 'nl_site_he' => '8001', 'nl_site_en' => '8002', 'nl_site_ru' => '8003', 'nl_site_fr' => '8004', 'nl_langs' => 'he,en,ru,fr', 'areas_served' => 'נופי ים,צוקי אביב,רמת אביב', 'nl_areas_en' => 'Nofei Yam,Tzukei Aviv,Ramat Aviv',
	'nl_areas_ru' => 'Нофей Ям,Цукей Авив,Рамат-Авив', 'nl_areas_fr' => 'Nofei Yam,Tsoukei Aviv,Ramat Aviv', 'bio' => 'עשרים שנה בצפון תל אביב, בעיקר דירות משפחתיות ומגורים ליד הים.', 'nl_slug' => 'israel-israeli', 'nl_drop_on' => '1' );
$GLOBALS['META'][9001] = array( 'nl_broker_id' => '7900', 'nl_facts' => json_encode( $f, JSON_UNESCAPED_UNICODE ), 'nl_copy' => json_encode( $copy, JSON_UNESCAPED_UNICODE ),
	'nl_photos_json' => json_encode( array( array( 'id' => 1, 'url' => 'https://nad-lan.co.il/wp-content/uploads/2026/09/meital-katzir-sea-terrace.jpg', 'w' => 1600, 'h' => 1067 ), array( 'id' => 2, 'url' => 'https://nad-lan.co.il/wp-content/uploads/2026/09/meital-katzir-portrait.jpg', 'w' => 1080, 'h' => 1350 ) ) ),
	'nl_twins' => json_encode( array( 'en' => 9002, 'ru' => 9003, 'fr' => 9004 ) ), 'listing_type' => 'rent', 'nl_status' => 'active', 'source' => 'broker_drop', 'price' => 9500 );
foreach ( array( 9002 => 'en', 9003 => 'ru', 9004 => 'fr' ) as $id => $l ) { $GLOBALS['META'][ $id ] = array( 'nl_twin' => '9001', 'nl_lang' => $l, 'nl_broker_id' => '7900' ); }
$b = nl_drop_broker( 7900 );
echo "broker langs: ", json_encode( $b['langs'] ), " name_ru: ", $b['name_ru'], "\n";
$alts = array( 'he' => get_permalink( 9001 ), 'en' => get_permalink( 9002 ), 'ru' => get_permalink( 9003 ), 'fr' => get_permalink( 9004 ) );
$data = nl_drop_data_for( 9001, $b );
foreach ( array( 'he' => 0, 'en' => 9002, 'ru' => 9003, 'fr' => 9004 ) as $l => $pid ) {
	$a = $alts; unset( $a[ $l ] );
	$h = nl_drop_listing_html( array_merge( $data, array( 'id' => 9001, 'url' => $alts[ $l ], 'alts' => $a, 'page_id' => $pid, 'date' => '2026-09-23' ) ), $l );
	file_put_contents( __DIR__ . "/listing-$l.html", $h );
	$body = preg_replace( '#<style>.*?</style>#s', '', $h );
	$txt  = html_entity_decode( strip_tags( preg_replace( '#<script.*?</script>#s', '', $body ) ), ENT_QUOTES, 'UTF-8' );
	printf( "%s: bytes=%d h1=%d langlinks=%d licence=%d token_left=%d bang=%d dash=%d ldjson=%d\n", $l, strlen( $h ), substr_count( $body, '<h1' ), substr_count( $body, 'class="nlx-lang' ), substr_count( $txt, '1234567' ), substr_count( $h, '{{PRICE}}' ), substr_count( $txt, '!' ), substr_count( $txt, '—' ), substr_count( $h, 'ld+json' ) );
	if ( $l === 'ru' || $l === 'fr' ) {
		preg_match( '#<dl class="nlx-facts">(.*?)</dl>#s', $body, $m );
		echo "   facts: ", trim( preg_replace( '/\s+/u', ' ', html_entity_decode( strip_tags( str_replace( '</div>', ' | ', $m[1] ) ), ENT_QUOTES, 'UTF-8' ) ) ), "\n";
		preg_match( '#<aside class="nlx-rail".*?</aside>#s', $body, $m );
		echo "   rail: ", trim( preg_replace( '/\s+/u', ' ', html_entity_decode( strip_tags( $m[0] ), ENT_QUOTES, 'UTF-8' ) ) ), "\n";
		preg_match( '#<nav class="nlx-toc".*?</nav>#s', $body, $m );
		echo "   toc: ", trim( preg_replace( '/\s+/u', ' ', strip_tags( str_replace( '</a>', ' · ', $m[0] ) ) ) ), "\n";
	}
}
foreach ( array( 'he', 'ru', 'fr' ) as $l ) {
	$L    = nl_drop_broker_listings( 7900, $l );
	$card = nl_drop_card_html( $L[0], $l, $b );
	file_put_contents( __DIR__ . "/card-$l.html", $card );
	echo "card $l: ", trim( preg_replace( '/\s+/u', ' ', html_entity_decode( strip_tags( str_replace( array( '</p>', '</li>', '</span>' ), ' | ', $card ) ), ENT_QUOTES, 'UTF-8' ) ) ), "\n";
}
foreach ( array( 'he' => 8001, 'en' => 8002, 'ru' => 8003, 'fr' => 8004 ) as $l => $pid ) {
	$a = array( 'he' => get_permalink( 8001 ), 'en' => get_permalink( 8002 ), 'ru' => get_permalink( 8003 ), 'fr' => get_permalink( 8004 ) ); unset( $a[ $l ] );
	$h = nl_drop_site_html( $b, $l, $pid, $a );
	file_put_contents( __DIR__ . "/site-$l.html", $h );
	$body = preg_replace( '#<style>.*?</style>#s', '', $h );
	$txt  = html_entity_decode( strip_tags( preg_replace( '#<script.*?</script>#s', '', $body ) ), ENT_QUOTES, 'UTF-8' );
	$seo  = nl_drop_site_seo( $b, $l );
	printf( "site %s: bytes=%d h1=%d cards=%d langs=%d licence=%d\n   seo: %s || %s\n", $l, strlen( $h ), substr_count( $body, '<h1' ), substr_count( $body, 'class="nlb-lcard"' ), substr_count( $body, 'class="is-lang"' ), substr_count( $txt, '1234567' ), $seo[0], $seo[1] );
	preg_match( '#<header class="nlb-hero">.*?</header>#s', $body, $m );
	echo "   hero: ", trim( preg_replace( '/\s+/u', ' ', html_entity_decode( strip_tags( str_replace( array( '</p>', '</h1>', '</dt>', '</a>' ), ' | ', $m[0] ) ), ENT_QUOTES, 'UTF-8' ) ) ), "\n";
}
// an empty site (a broker who has just joined)
$GLOBALS['POSTS'][9001]['status'] = 'draft';
$h = nl_drop_site_html( $b, 'he', 8001, array() );
$body = preg_replace( '#<style>.*?</style>#s', '', $h );
echo "empty he site: cards=", substr_count( $body, 'nlb-lcard' ), " filters=", substr_count( $body, 'nlb-filters' ), " lead: ", ( preg_match( '#<p class="nlb-lead">(.*?)</p>#', $body, $m ) ? $m[1] : '' ), " hero_img=", substr_count( $body, '<div class="nlb-hero-media" aria-hidden="true"></div>' ) ? 'none' : 'yes', "\n";
