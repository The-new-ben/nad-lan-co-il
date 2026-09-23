<?php
// 1.1.1: the street never reaches a page
require __DIR__ . '/harness2.php';
$f = array( 'street_he' => 'רחוב דיזנגוף 120', 'street_en' => 'Dizengoff St 120' );
$cases = array(
	array( '4 חדרים בדיזנגוף, קומה 5', true ),
	array( 'Four rooms on Dizengoff, floor 5', true ),
	array( '4 חדרים בלב העיר, קומה 5', false ),
	array( 'Four rooms, floor 5', false ),
);
foreach ( $cases as $c ) {
	$r = nl_drop_has_street( $c[0], $f );
	printf( "%-5s %s -> %s\n", $r === $c[1] ? 'OK' : 'FAIL', $c[0], $r ? 'names the street' : 'clean' );
}
// finish_copy throws away a field that names the street and keeps the rest
$text = 'למכירה: 4 חדרים ברחוב דיזנגוף 120, תל אביב. 110 מ"ר, קומה 5 מתוך 8. 4.2 מיליון.';
$facts = array( 'listing_type' => 'sale', 'property_type' => 'apartment', 'city_he' => 'תל אביב-יפו', 'city_en' => 'Tel Aviv-Yafo', 'area_he' => null, 'area_en' => null,
	'street_he' => 'רחוב דיזנגוף 120', 'street_en' => 'Dizengoff St 120', 'rooms' => 4, 'size_sqm' => 110, 'floor' => 5, 'total_floors' => 8, 'price' => 4200000,
	'features_he' => array(), 'features_en' => array(), 'entry_he' => null, 'entry_en' => null );
$model = array( 'he' => array( 'title' => '4 חדרים בדיזנגוף, תל אביב', 'dek' => 'בקומה 5 מתוך 8: 4 חדרים על 110 מ״ר. {{PRICE}}.' ),
	'en' => array( 'title' => 'Four Rooms on Dizengoff, Tel Aviv', 'dek' => 'On floor 5 of 8: four rooms on 110 sqm. {{PRICE}}.' ) );
$c = nl_drop_finish_copy( $model, $facts, $text );
echo 'he title: ', $c['he']['title'], "\nhe dek: ", $c['he']['dek'], "\nen title: ", $c['en']['title'], "\n";
echo ( strpos( $c['he']['title'], 'דיזנגוף' ) === false && stripos( $c['en']['title'], 'dizengoff' ) === false ) ? "OK    street kept off the titles\n" : "FAIL  street in a title\n";
