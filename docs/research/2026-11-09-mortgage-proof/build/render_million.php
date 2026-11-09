<?php
// Local render of the 1.72.615 million block from the real data file (no WordPress): php render_million.php > out.html
// Stubs only the WP functions the block calls. Also prints the CSV and checks the numbers against the Python cross-check.
define( 'ABSPATH', __DIR__ );
function esc_html( $s ) { return htmlspecialchars( (string) $s, ENT_QUOTES, 'UTF-8' ); }
function esc_attr( $s ) { return htmlspecialchars( (string) $s, ENT_QUOTES, 'UTF-8' ); }
function esc_url( $s ) { return htmlspecialchars( (string) $s, ENT_QUOTES, 'UTF-8' ); }
function get_permalink( $p = null ) { return 'https://nad-lan.co.il/mortgage-calculator/'; }
function rest_url( $p ) { return 'https://nad-lan.co.il/wp-json/' . $p; }
function home_url( $p = '/' ) { return 'https://nad-lan.co.il' . $p; }
function plugins_url( $p, $f ) { return 'https://nad-lan.co.il/wp-content/plugins/nadlan-config/' . $p; }
function add_shortcode() {} function add_action() {} function add_filter() {} function is_singular() { return false; }
require __DIR__ . '/../../../../plugins/nadlan-config/inc/mortgage-market.php';
$d = nadlan_mm_data();
$names = array(); foreach ( (array) $d['by_bank']['banks'] as $b ) { $names[ $b['k'] ] = $b['he']; } $names['system'] = 'כל הבנקים';
$rows = nadlan_mm_million_rows( $d );
$last = end( $rows );
$want = array( 'system' => 5428, 'hapoalim' => 5443, 'leumi' => 5404, 'discount' => 5354, 'mizrahi' => 5463, 'fibi' => 5281 );
foreach ( $want as $k => $v ) { if ( (int) $last[ $k ] !== $v ) { fwrite( STDERR, "MISMATCH $k {$last[$k]} != $v\n" ); exit( 1 ); } }
if ( 25 !== count( $rows ) || 5582 !== (int) $rows[0]['system'] ) { fwrite( STDERR, "MISMATCH rows\n" ); exit( 1 ); }
$mode = $argv[1] ?? 'html';
if ( 'csv' === $mode ) { echo nadlan_mm_million_csv(); exit; }
if ( 'sentence' === $mode ) { echo nadlan_mm_million_sentence( $d, $names ), "\n"; exit; }
echo '<section class="nlmm" dir="rtl" lang="he">' . nadlan_mm_million_html( $d, $names ) . nadlan_mm_css() . nadlan_mm_million_css() . '</section>';
