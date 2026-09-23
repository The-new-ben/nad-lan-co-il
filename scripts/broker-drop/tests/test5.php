<?php
require __DIR__ . '/harness2.php';
function get_privacy_policy_url() { return ''; }
function is_admin() { return false; }
require __DIR__ . '/../../../plugins/nadlan-config/inc/broker-join.php';
$cases = array(
	array( 'מיטל קציר', 'קציר מיטל', true ),
	array( 'מיטל קציר-לוי', 'קציר מיטל', true ),
	array( 'מיטל כהן', 'קציר מיטל', false ),
	array( 'קציר', 'קציר מיטל', false ),
	array( 'שרה לוי', 'לוי כהן שרה', true ),
	array( 'שרה', 'לוי כהן שרה', false ),
	array( 'אברהם  יוסף', 'יוסף אברהם', true ),
	array( 'Meital Katzir', 'קציר מיטל', false ),
	array( 'דוד בן חיים', 'בן חיים דוד', true ),
);
foreach ( $cases as $c ) {
	$r = nl_join_name_match( $c[0], $c[1] );
	printf( "%-5s %s | %s -> %s\n", $r === $c[2] ? 'OK' : 'FAIL', $c[0], $c[1], $r ? 'match' : 'no' );
}
foreach ( array( 'he', 'en', 'ru', 'fr' ) as $l ) {
	$h = nl_join_form( $l );
	file_put_contents( __DIR__ . "/join-$l.html", $h );
	printf( "form %s: bytes=%d inputs=%d required=%d h2=%d privacy_link=%d\n", $l, strlen( $h ), substr_count( $h, '<input' ), substr_count( $h, 'required' ), substr_count( $h, '<h2' ), substr_count( $h, 'mailto:' ) );
}
echo "mount: ", strlen( preg_replace_callback( '#<div class="nljoin-mount"(?: data-lang="([a-z]{2})")?[^>]*>\s*</div>#', function ( $m ) { return nl_join_form( $m[1] ?? 'he' ); }, '<p>x</p><div class="nljoin-mount" data-lang="he"></div>' ) ), "\n";
