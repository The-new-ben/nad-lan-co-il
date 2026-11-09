<?php
// HAD-689: the 301 map of smart-404.php, tested without WordPress. php tools/seo/test_h689_redirects.php
define( 'ABSPATH', __DIR__ );
function home_url( $p = '/' ) { return 'https://nad-lan.co.il' . $p; }
function add_action() {} function add_filter() {} function is_admin() { return false; }
require dirname( __DIR__, 2 ) . '/plugins/nadlan-config/inc/smart-404.php';
$cases = array(
	'/new-projects/new-projects-tel-aviv/' => 'https://nad-lan.co.il/projects/',
	'/new-projects/new-projects-tel-aviv'  => 'https://nad-lan.co.il/projects/',
	'/city/תל אביב יפו/projects/'          => 'https://nad-lan.co.il/projects/?city=' . rawurlencode( 'תל אביב' ),
	'/city/תל-אביב-יפו/'                    => 'https://nad-lan.co.il/projects/?city=' . rawurlencode( 'תל אביב' ),
	'/city/רמת-גן/projects/'               => 'https://nad-lan.co.il/projects/?city=' . rawurlencode( 'רמת גן' ),
	'/city/רמת גן/projects/'               => 'https://nad-lan.co.il/projects/?city=' . rawurlencode( 'רמת גן' ),
	'/city/באר-שבע/contractors/'           => 'https://nad-lan.co.il/projects/?city=' . rawurlencode( 'באר שבע' ),
	'/city/אשדוד/'                          => 'https://nad-lan.co.il/projects/?city=' . rawurlencode( 'אשדוד' ),
	'/cities/'                              => 'https://nad-lan.co.il/projects/',
	'/city/'                                => 'https://nad-lan.co.il/projects/',
	'/city/חיפה/properties/'               => '',   // other kinds keep their 410
	'/city/חיפה/projects/extra/'           => '',
	'/projects/'                            => '',
	'/new-projects/'                        => '',
	'/new-projects/north-tel-aviv-new-projects/' => '',
);
$bad = 0;
foreach ( $cases as $in => $want ) {
	$got = nadlan_h689_target( $in );
	if ( $got !== $want ) { $bad++; echo "FAIL $in => $got (want $want)\n"; }
}
echo ( $bad ? "FAILED $bad" : 'all ' . count( $cases ) . ' passed' ), "\n";
exit( $bad ? 1 : 0 );
