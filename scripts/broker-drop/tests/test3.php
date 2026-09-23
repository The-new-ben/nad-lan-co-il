<?php
require __DIR__ . '/harness2.php';
function show( $k, $v ) { echo str_pad( $k, 30 ), json_encode( $v, JSON_UNESCAPED_UNICODE ), "\n"; }
// formats
show( 'fmt ru', nl_drop_fmt_int( 4200000, 'ru' ) );
show( 'price ru/fr/en/he', array( nl_drop_price_text( 4200000, 'ru' ), nl_drop_price_text( 4200000, 'fr' ), nl_drop_price_text( 4200000, 'en' ), nl_drop_price_text( 4200000, 'he' ) ) );
show( 'num ru 4.5', nl_drop_fmt_num( 4.5, 'ru' ) );
show( 'nums ru', nl_drop_nums_in_copy( "4,5 комнаты, 110 м², этаж 5 из 8, 4\u{00A0}200\u{00A0}000 ₪", 'ru' ) );
show( 'nums fr', nl_drop_nums_in_copy( '4,5 pièces sur 1 200 m², 5e étage sur 8', 'fr' ) );
show( 'nums he unchanged', nl_drop_nums_in_copy( '4.5 חדרים, 4,200,000 ש״ח', 'he' ) );
// banned
show( 'ban ru', nl_drop_banned_hits( 'Уникальная квартира! Мечта.', 'ru' ) );
show( 'ban fr uniquement', nl_drop_banned_hits( 'Visites uniquement sur rendez-vous', 'fr' ) );
show( 'ban fr unique', nl_drop_banned_hits( 'Un bien unique, parfaitement situé', 'fr' ) );
show( 'ban he', nl_drop_banned_hits( 'הזדמנות נדירה!', 'he' ) );
// claims
show( 'claims ru', nl_drop_claims_in( 'Просторная квартира с видом на море, после ремонта' ) );
show( 'claims ru kindergarten', nl_drop_claims_in( 'рядом детский сад и школа' ) );
show( 'claims fr', nl_drop_claims_in( "Appartement lumineux et calme, proche d'un jardin d'enfants" ) );
show( 'claims ru seven', nl_drop_claims_in( 'семь комнат' ) );
// the gate on a Russian sentence with place names
$f = array( 'listing_type' => 'rent', 'property_type' => 'apartment', 'exclusive' => true, 'city_he' => 'תל אביב-יפו', 'city_en' => 'Tel Aviv', 'area_he' => 'נופי ים', 'area_en' => 'Nofei Yam',
	'rooms' => 3, 'size_sqm' => 90, 'balcony_sqm' => 20, 'garden_sqm' => null, 'floor' => 5, 'total_floors' => 7, 'price' => 9500, 'parking_count' => 2, 'parking' => true, 'storage' => true, 'elevator' => true, 'protected_room' => true,
	'ac' => null, 'furnished' => null, 'condition' => null, 'entry_he' => '1.10, גמיש', 'entry_en' => '1 October, flexible', 'view_he' => null, 'view_en' => null, 'features_he' => array( 'מרפסת לשטח פתוח' ), 'features_en' => array( 'Balcony facing an open area' ), 'notes_he' => null, 'notes_en' => null );
$text = 'להשכרה בבלעדיות: 3 חדרים 90 מ"ר, מרפסת 20 מ"ר לשטח פתוח, קומה 5 מתוך 7, בניין על עמודים עם מעלית, ממ"ד, 2 חניות נפרדות ומחסן גדול ליד החניה. 9,500 לחודש, כניסה 1.10 גמיש. נופי ים.';
$allowed = nl_drop_allowed_numbers( $f, $text );
$stated  = nl_drop_stated( $f, $text );
show( 'stated', $stated );
show( 'gate ru ok', nl_drop_gate_str( 'Нофей Ям: 3 комнаты на 90 м², балкон 20 м², этаж 5 из 7.', 'ru', $allowed, $stated, array( 'Нофей Ям' ) ) );
show( 'gate ru invented', nl_drop_gate_str( 'Тихая квартира с видом на море, 4 комнаты.', 'ru', $allowed, $stated, array( 'Нофей Ям' ) ) );
show( 'gate fr park name', nl_drop_gate_str( 'Parc Tsameret : 3 pièces sur 90 m².', 'fr', $allowed, $stated, array( 'Parc Tsameret' ) ) );
// the plain pages
foreach ( array( 'ru', 'fr' ) as $l ) {
	$fl = $f;
	$fl[ 'area_' . $l ]  = $l === 'ru' ? 'Нофей Ям' : 'Nofei Yam';
	$fl[ 'city_' . $l ]  = $l === 'ru' ? 'Тель-Авив' : 'Tel Aviv';
	$fl[ 'entry_' . $l ] = $l === 'ru' ? '1 октября, гибко' : '1er octobre, flexible';
	$t = nl_drop_tpl_x( $fl, $l );
	echo "\n[$l template]\n";
	foreach ( array( 'title', 'card_title', 'dek', 'story_h2', 'seo_title' ) as $k ) { echo "  $k: ", nl_drop_fill( $t[ $k ], $fl, $l ), "\n"; }
	echo "  story: ", nl_drop_fill( implode( ' | ', $t['story'] ), $fl, $l ), "\n  features: ", json_encode( $t['features'], JSON_UNESCAPED_UNICODE ), "\n  chips: ", json_encode( $t['chips'], JSON_UNESCAPED_UNICODE ), " hi: ", json_encode( $t['card_hi'], JSON_UNESCAPED_UNICODE ), "\n";
	$bad = array();
	foreach ( array( 'title', 'card_title', 'dek', 'story_h2', 'seo_title', 'seo_desc' ) as $k ) {
		$i = nl_drop_gate_str( $t[ $k ], $l, $allowed, $stated, array( $fl[ 'area_' . $l ], $fl[ 'city_' . $l ] ) );
		if ( $i ) { $bad[ $k ] = $i; }
	}
	show( "  template self-gate $l", $bad );
}
// a model translation with problems: a hype word, a literal price, an invented view
$model = array(
	'ru' => array( 'title' => '3 комнаты с балконом 20 м² и 2 парковками, Нофей Ям', 'card_title' => '3 комнаты с балконом 20 м²', 'dek' => 'Этаж 5 из 7 в Нофей Ям: 3 комнаты на 90 м², балкон 20 м², мамад, 2 парковки и кладовая. 9 500 ₪ в месяц.',
		'story_h2' => 'Уникальная квартира в Нофей Ям', 'story' => array( '3 комнаты на 90 м² с балконом 20 м² на открытое пространство.', 'Великолепный вид на море.' ),
		'features' => array( array( '90 м² и балкон 20 м²', '3 комнаты' ), array( 'Мамад', 'в квартире' ), array( '2 отдельные парковки', 'и большая кладовая' ), array( 'Этаж 5 из 7', 'дом на колоннах с лифтом' ) ),
		'chips' => array( 'Мамад, 2 парковки', 'Въезд 1.10' ), 'card_hi' => array( 'Балкон на открытое пространство', 'Кладовая у парковки', 'Дом с лифтом' ),
		'seo_title' => 'Аренда: 3 комнаты, балкон 20 м², Нофей Ям', 'seo_desc' => '3 комнаты, 90 м², балкон 20 м², этаж 5 из 7. {{PRICE}} в месяц.', 'area' => 'Нофей Ям', 'city' => 'Тель-Авив', 'entry' => '1 октября, гибко' ),
	'fr' => array( 'title' => '3 pièces avec balcon de 20 m², Nofei Yam', 'card_title' => '3 pièces avec balcon de 20 m²', 'dek' => 'Au 5e étage sur 7 à Nofei Yam : 3 pièces sur 90 m², balcon de 20 m², mamad, 2 parkings et une grande cave. {{PRICE}} par mois.',
		'story_h2' => '3 pièces et un balcon de 20 m²', 'story' => array( '3 pièces sur 90 m², un balcon de 20 m² ouvert sur un espace dégagé, et un mamad.', 'Deux places de parking séparées et une grande cave près du parking.' ),
		'features' => array( array( '90 m² et balcon de 20 m²', '3 pièces' ), array( 'Mamad', 'pièce sécurisée' ), array( '2 places de parking', 'et une grande cave' ), array( '5e étage sur 7', 'immeuble sur pilotis avec ascenseur' ) ),
		'chips' => array( 'Mamad, 2 parkings', 'Entrée le 1er octobre' ), 'card_hi' => array( 'Balcon ouvert', 'Cave près du parking', 'Ascenseur' ),
		'seo_title' => '3 pièces à louer, balcon de 20 m², Nofei Yam', 'seo_desc' => '3 pièces, 90 m², balcon de 20 m², 5e étage sur 7. {{PRICE}} par mois.', 'area' => 'Nofei Yam', 'city' => 'Tel Aviv', 'entry' => '1er octobre, flexible' ),
);
$tr = nl_drop_finish_tr( $model, $f, $text, array( 'ru', 'fr' ) );
echo "\n";
show( 'ru dek (price->token)', $tr['copy']['ru']['dek'] );
show( 'ru story_h2 (hype->tpl)', $tr['copy']['ru']['story_h2'] );
show( 'ru story (sea claim cut)', $tr['copy']['ru']['story'] );
show( 'ru names', $tr['names']['ru'] );
show( 'fr dek', $tr['copy']['fr']['dek'] );
show( 'fr story_h2', $tr['copy']['fr']['story_h2'] );
show( 'fr features', $tr['copy']['fr']['features'] );
show( 'fr chips', $tr['copy']['fr']['chips'] );
show( 'plain', $tr['plain'] );
file_put_contents( __DIR__ . '/tr.json', json_encode( array( 'f' => $f, 'text' => $text, 'tr' => $tr ), JSON_UNESCAPED_UNICODE ) );
