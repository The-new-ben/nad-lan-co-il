<?php
/* Local preview of the renewal map data block (1.72.520): inc/urban-map-data.php with WordPress stand-ins. php render.php */
define( 'ABSPATH', __DIR__ );
function esc_html( $s ) { return htmlspecialchars( (string) $s, ENT_QUOTES, 'UTF-8' ); }
function esc_attr( $s ) { return htmlspecialchars( (string) $s, ENT_QUOTES, 'UTF-8' ); }
function esc_url( $s ) { return htmlspecialchars( (string) $s, ENT_QUOTES, 'UTF-8' ); }
function wp_list_pluck( $a, $k ) { return array_map( function ( $x ) use ( $k ) { return $x[ $k ]; }, $a ); }
function home_url( $p = '/' ) { return 'https://nad-lan.co.il' . $p; }
require dirname( __DIR__, 5 ) . '/plugins/nadlan-config/inc/urban-map-data.php';
$h = nadlan_urd_html();
$shell = '<!doctype html><html lang="he" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>מפת התחדשות עירונית · תצוגה</title>'
	. '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Hebrew:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500&family=Karantina:wght@700&display=swap">'
	. '<style>body{margin:0;background:#F6F8F9}main{max-width:1100px;margin:0 auto;padding:16px}h1{font:600 30px/1.2 "IBM Plex Sans Hebrew",sans-serif;color:#12202A}</style></head><body><main>'
	. '<h1>מפת התחדשות עירונית: מתחמים ופרויקטים של פינוי בינוי בכל עיר</h1>' . $h . '</main></body></html>';
file_put_contents( __DIR__ . '/preview.html', $shell );
echo strlen( $shell ), " bytes\n";
