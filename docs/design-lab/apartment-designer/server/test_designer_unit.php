<?php
// Offline unit test of plugins/nadlan-config/inc/designer.php (HAD-701). No network, no WordPress: minimal stubs below.
//   C:/Users/777/tools/php-8.3/php.exe docs/design-lab/apartment-designer/server/test_designer_unit.php
// Prints TAP lines; exits 1 on any failure.

define( 'ABSPATH', __DIR__ . '/' );
define( 'MINUTE_IN_SECONDS', 60 ); define( 'HOUR_IN_SECONDS', 3600 ); define( 'DAY_IN_SECONDS', 86400 );
define( 'NADLAN_CONFIG_VERSION', '9.9.9' );

$GLOBALS['OPT'] = array(); $GLOBALS['TR'] = array(); $GLOBALS['FILTERS'] = array(); $GLOBALS['STAGE'] = false;
class WP_Error { public $code; public $message; public $data; function __construct( $c = '', $m = '', $d = null ) { $this->code = $c; $this->message = $m; $this->data = $d; } function get_error_code() { return $this->code; } }
function is_wp_error( $x ) { return $x instanceof WP_Error; }
function get_option( $k, $d = false ) { return array_key_exists( $k, $GLOBALS['OPT'] ) ? $GLOBALS['OPT'][ $k ] : $d; }
function get_transient( $k ) { return $GLOBALS['TR'][ $k ] ?? false; }
function set_transient( $k, $v, $t = 0 ) { $GLOBALS['TR'][ $k ] = $v; return true; }
function wp_salt( $s = '' ) { return 'test-salt-' . $s; }
function wp_unslash( $v ) { return $v; }
function wp_json_encode( $d, $o = 0 ) { return json_encode( $d, $o ); }
function wp_parse_url( $u, $c = -1 ) { return parse_url( $u, $c ); }
function home_url( $p = '' ) { return 'https://nad-lan.co.il' . $p; }
function rest_url( $p = '' ) { return 'https://nad-lan.co.il/wp-json/' . $p; }
function plugins_url( $p, $f ) { return 'https://nad-lan.co.il/wp-content/plugins/nadlan-config/' . $p; }
function wp_strip_all_tags( $t, $r = false ) { $t = preg_replace( '@<(script|style)[^>]*?>.*?</\1>@si', '', (string) $t ); $t = strip_tags( $t ); return $r ? preg_replace( '/[\r\n\t ]+/', ' ', $t ) : trim( $t ); }
function esc_attr( $s ) { return htmlspecialchars( (string) $s, ENT_QUOTES, 'UTF-8' ); }
function shortcode_atts( $pairs, $atts, $sc = '' ) { $atts = (array) $atts; $o = array(); foreach ( $pairs as $k => $v ) { $o[ $k ] = array_key_exists( $k, $atts ) ? $atts[ $k ] : $v; } return $o; }
function add_filter( $t, $cb, $p = 10, $n = 1 ) { $GLOBALS['FILTERS'][ $t ][] = $cb; }
function apply_filters( $t, $v, ...$a ) { foreach ( $GLOBALS['FILTERS'][ $t ] ?? array() as $cb ) { $v = $cb( $v, ...$a ); } return $v; }
function add_action() {} function add_shortcode() {}
function nadlan_ps_current() { return $GLOBALS['STAGE']; }

$PLUG = dirname( __DIR__, 4 ) . '/plugins/nadlan-config';
require $PLUG . '/inc/designer.php';

$n = 0; $failed = 0;
function t( $name, $ok, $diag = '' ) {
	global $n, $failed; $n++;
	if ( $ok ) { echo "ok $n - $name\n"; } else { $failed++; echo "not ok $n - $name\n" . ( '' !== $diag ? '  # ' . str_replace( "\n", "\n  # ", $diag ) . "\n" : '' ); }
}
/** same meaning: same keys (any order), numbers equal within 1e-6, everything else identical */
function same( $a, $b ) {
	if ( is_numeric( $a ) && is_numeric( $b ) && ! is_string( $a ) && ! is_string( $b ) ) { return abs( $a - $b ) < 1e-6; }
	if ( is_array( $a ) && is_array( $b ) ) {
		if ( count( $a ) !== count( $b ) ) { return false; }
		foreach ( $a as $k => $v ) { if ( ! array_key_exists( $k, $b ) || ! same( $v, $b[ $k ] ) ) { return false; } }
		return true;
	}
	return $a === $b;
}

/* ---------- the sample: written by the spike's own store (dump-design.mjs), else built by hand to the schema ---------- */
$spike  = dirname( __DIR__ ) . '/spike';
$sample = null;
$cmd    = 'node ' . escapeshellarg( $spike . '/dump-design.mjs' ) . ' 2>' . ( '\\' === DIRECTORY_SEPARATOR ? 'NUL' : '/dev/null' );
$raw    = @shell_exec( $cmd );
if ( is_string( $raw ) && '' !== $raw ) { $sample = json_decode( $raw, true ); }
$from = is_array( $sample ) ? 'dump-design.mjs' : 'hand-built';
if ( ! is_array( $sample ) ) {
	$sample = array(
		'schema' => 'nadlan-unit-design', 'v' => 2, 'project' => null, 'unit_id' => null, 'geometry_revision' => 'example-4r:2026-11-10:a',
		'frame' => array( 'units' => 'cm', 'origin' => 'plan-top-left', 'rot' => 'deg-cw' ),
		'geometry' => array( 'walls' => array( 'p6' => 20 ) ), 'finishes' => array( 'floor:living' => 'oak-plank' ),
		'items' => array( array( 'id' => 'i1', 'sku' => 'gen.rug', 'x' => 455, 'y' => 210, 'rot' => 90, 'status' => 'decor', 'room' => 'living' ), array( 'id' => 'i2', 'sku' => 'gen.sofa3', 'x' => 340, 'y' => 220, 'rot' => 270, 'status' => 'decor', 'room' => 'living' ) ),
		'notes' => array(),
		'log' => array(
			array( 'n' => 1, 't' => '2026-11-11T10:03:49.783Z', 'by' => 'buyer', 'op' => array( 'op' => 'wall.shift', 'id' => 'p6', 'd' => 20 ), 'gesture' => null ),
			array( 'n' => 2, 't' => '2026-11-11T10:03:49.798Z', 'by' => 'designer', 'op' => array( 'op' => 'finish.set', 'key' => 'floor:living', 'value' => 'oak-plank' ), 'gesture' => null ),
			array( 'n' => 3, 't' => '2026-11-11T10:03:49.798Z', 'by' => 'rep', 'op' => array( 'op' => 'item.move', 'id' => 'i2', 'x' => 340, 'y' => 220 ), 'gesture' => 'g1' ),
		),
		'rev' => 3,
	);
}
echo "# sample: $from, " . count( $sample['items'] ) . ' items, ' . count( $sample['log'] ) . " log lines\n";

$c = nadlan_dsg_clean_design( $sample );
t( 'sample is accepted', is_array( $c ), is_wp_error( $c ) ? $c->code : '' );
t( 'sample comes back unchanged in meaning', is_array( $c ) && same( $sample, json_decode( json_encode( $c ), true ) ), json_encode( $c ) );
t( 'clean is idempotent', is_array( $c ) && same( $c, nadlan_dsg_clean_design( $c ) ) );
t( 'clean output under 200 KB as JSON', is_array( $c ) && strlen( json_encode( $c ) ) < 200 * 1024 );

/* ---------- what must be stripped ---------- */
$bad = $sample;
$bad['evil']                       = 'x';
$bad['frame']['units']             = 'm';
$bad['geometry']['extra']          = 1;
$bad['geometry']['walls']['../x']  = 5;
$bad['geometry']['walls']['p7']    = 99999;
$bad['finishes']['floor:kitchen']  = '<script>alert(1)</script>';
$bad['finishes']['roof:x']         = 'oak-plank';
$bad['items'][0]['onclick']        = 'alert(1)';
$bad['items'][0]['note']           = '<script>alert(1)</script>ליד החלון <b>כאן</b>';
$bad['items'][]                    = array( 'id' => 'BAD ID', 'sku' => 'gen.sofa3', 'x' => 1, 'y' => 1, 'rot' => 0 );
$bad['items'][]                    = array( 'id' => 'okid', 'sku' => '<img>', 'x' => 1, 'y' => 1, 'rot' => 0 );
$bad['items'][]                    = array( 'id' => 'i1', 'sku' => 'gen.plant', 'x' => 1, 'y' => 1, 'rot' => 0 ); // duplicate id
$bad['items'][]                    = array( 'id' => 'big', 'sku' => 'gen.plant', 'x' => 1e12, 'y' => 'NaN', 'rot' => 0 );
$bad['items'][]                    = array( 'id' => 'spin', 'sku' => 'gen.plant', 'x' => 10.123456, 'y' => -5, 'rot' => 1170, 'status' => 'free' );
$bad['notes'][]                    = array( 'target' => array( 'kind' => 'room', 'id' => 'living', 'x' => 1 ), 'text' => '<script>steal()</script>להזיז את השקע', 'by' => 'Dana Levi', 'email' => 'a@b.c' );
$bad['notes'][]                    = array( 'target' => array( 'kind' => 'hack' ), 'text' => '   ' );
$bad['log'][0]['by']               = 'Moshe Cohen 050-1234567';
$bad['log'][0]['ip']               = '1.2.3.4';
$bad['log'][]                      = array( 'n' => 4, 't' => '2026-11-11T10:04:00Z', 'by' => 'buyer', 'op' => array( 'op' => 'system.exec', 'cmd' => 'rm' ) );
$bad['log'][]                      = array( 'n' => 5, 't' => 'yesterday', 'by' => 'buyer', 'op' => array( 'op' => 'item.remove', 'id' => 'i1' ) );
$bad['log'][]                      = array( 'n' => 6, 't' => '2026-11-11T10:05:00Z', 'by' => 'partner', 'op' => array( 'op' => 'wall.shift', 'id' => 'p6', 'd' => -5000, 'evil' => 1 ) );
$x = nadlan_dsg_clean_design( $bad );
$xj = json_encode( $x, JSON_UNESCAPED_UNICODE );
t( 'dirty design still cleans (no error)', is_array( $x ) );
t( 'unknown top-level key dropped', is_array( $x ) && ! isset( $x['evil'] ) );
t( 'frame forced to the v2 frame', $x['frame'] === array( 'units' => 'cm', 'origin' => 'plan-top-left', 'rot' => 'deg-cw' ) );
t( 'unknown key inside geometry dropped', array_keys( $x['geometry'] ) === array( 'walls' ) );
t( 'wall id with path characters dropped', ! isset( $x['geometry']['walls']['../x'] ) );
t( 'wall shift clamped to 1000', 1000 === $x['geometry']['walls']['p7'] );
t( 'finish value with a tag dropped', ! isset( $x['finishes']['floor:kitchen'] ) );
t( 'finish key outside the pattern dropped', ! isset( $x['finishes']['roof:x'] ) );
t( 'unknown item key dropped', ! isset( $x['items'][0]['onclick'] ) );
t( 'script tag stripped from an item note', isset( $x['items'][0]['note'] ) && false === strpos( $x['items'][0]['note'], 'script' ) && false === strpos( $x['items'][0]['note'], 'alert' ) && false !== strpos( $x['items'][0]['note'], 'כאן' ) && false === strpos( $x['items'][0]['note'], '<' ) );
$ids = array_column( $x['items'], 'id' );
t( 'item with a bad id dropped', ! in_array( 'BAD ID', $ids, true ) );
t( 'item with a bad sku dropped', ! in_array( 'okid', $ids, true ) );
t( 'second item with the same id dropped', 1 === count( array_keys( $ids, 'i1', true ) ) );
t( 'item with a non-number dropped', ! in_array( 'big', $ids, true ) );
$spin = null; foreach ( $x['items'] as $it ) { if ( 'spin' === $it['id'] ) { $spin = $it; } }
t( 'rotation brought into one turn, coordinates rounded, bad status dropped', $spin && 90 === $spin['rot'] && 10.1 === $spin['x'] && ! isset( $spin['status'] ), json_encode( $spin ) );
t( 'note: tags stripped, extra keys dropped, name in by reduced to a role', 1 === count( $x['notes'] ) && 'להזיז את השקע' === $x['notes'][0]['text'] && 'buyer' === $x['notes'][0]['by'] && ! isset( $x['notes'][0]['email'] ) && array( 'kind' => 'room', 'id' => 'living' ) === $x['notes'][0]['target'], json_encode( $x['notes'], JSON_UNESCAPED_UNICODE ) );
t( 'no personal name, phone or email anywhere', false === strpos( $xj, 'Dana' ) && false === strpos( $xj, 'Moshe' ) && false === strpos( $xj, '050' ) && false === strpos( $xj, 'a@b.c' ) && false === strpos( $xj, '1.2.3.4' ) );
t( 'log: name in by reduced to a role', 'buyer' === $x['log'][0]['by'] && ! isset( $x['log'][0]['ip'] ) );
$ops = array_map( function ( $e ) { return $e['op']['op']; }, $x['log'] );
t( 'log: unknown operation dropped', ! in_array( 'system.exec', $ops, true ) );
t( 'log: entry with a bad time dropped', ! in_array( 5, array_column( $x['log'], 'n' ), true ) );
$last = end( $x['log'] );
t( 'log: alias partner -> family, shift clamped, extra op key dropped', 6 === $last['n'] && 'family' === $last['by'] && -1000 === $last['op']['d'] && ! isset( $last['op']['evil'] ), json_encode( $last ) );
t( 'no "<script" anywhere in the clean JSON', false === stripos( $xj, '<script' ) );

/* ---------- oversize arrays ---------- */
$big = $sample; $big['items'] = array(); $big['notes'] = array(); $big['log'] = array();
for ( $i = 0; $i < 260; $i++ ) { $big['items'][] = array( 'id' => 'k' . $i, 'sku' => 'gen.chair', 'x' => $i, 'y' => 1, 'rot' => 0 ); }
for ( $i = 0; $i < 120; $i++ ) { $big['notes'][] = array( 'target' => array( 'kind' => 'general' ), 'text' => str_repeat( 'א', 450 ) ); }
for ( $i = 0; $i < 600; $i++ ) { $big['log'][] = array( 'n' => $i, 't' => '2026-11-11T10:00:00Z', 'by' => 'buyer', 'op' => array( 'op' => 'item.rot', 'id' => 'k1', 'rot' => 90 ), 'gesture' => null ); }
$b = nadlan_dsg_clean_design( $big );
t( 'oversize design under 200 KB is cleaned', is_array( $b ), is_wp_error( $b ) ? $b->code . ' ' . strlen( json_encode( $big ) ) : '' );
t( 'items capped at 200', is_array( $b ) && 200 === count( $b['items'] ) );
t( 'notes capped at 80, text at 400 characters', is_array( $b ) && 80 === count( $b['notes'] ) && 400 === mb_strlen( $b['notes'][0]['text'] ) );
t( 'log capped at the newest 400', is_array( $b ) && 400 === count( $b['log'] ) && 200 === $b['log'][0]['n'] && 599 === $b['log'][399]['n'] );

/* ---------- refusals ---------- */
$huge = $sample; $huge['notes'] = array( array( 'target' => array( 'kind' => 'general' ), 'text' => str_repeat( 'x', 210 * 1024 ) ) );
$h = nadlan_dsg_clean_design( $huge );
t( 'over 200 KB is refused', is_wp_error( $h ) && 'design_size' === $h->code );
t( 'not an object is refused', is_wp_error( nadlan_dsg_clean_design( 'x' ) ) && is_wp_error( nadlan_dsg_clean_design( null ) ) );
$v1 = $sample; $v1['v'] = 1;
t( 'version 1 is refused here', is_wp_error( nadlan_dsg_clean_design( $v1 ) ) );
$gr = $sample; $gr['geometry_revision'] = '../../etc';
t( 'bad geometry_revision is refused', is_wp_error( nadlan_dsg_clean_design( $gr ) ) );
$pj = $sample; $pj['project'] = '<b>x</b>'; $pj['unit_id'] = 'A 1';
$pc = nadlan_dsg_clean_design( $pj );
t( 'bad project and unit become null', is_array( $pc ) && null === $pc['project'] && null === $pc['unit_id'] );
$pj['project'] = 'ashira'; $pj['unit_id'] = 'E-4A-10';
$pc = nadlan_dsg_clean_design( $pj );
t( 'good project and unit kept as written', 'ashira' === $pc['project'] && 'E-4A-10' === $pc['unit_id'] );

/* ---------- services layer (not used yet) ---------- */
$pts = nadlan_dsg_clean_points( array(
	array( 'id' => 's1', 'kind' => 'socket', 'host' => 'wall', 'wall' => 'p6', 'at' => 120.44, 'h' => 30, 'status' => 'moved' ),
	array( 'id' => 'l1', 'kind' => 'light', 'host' => 'ceiling', 'x' => 300, 'y' => 200 ),
	array( 'id' => 's2', 'kind' => 'reactor', 'host' => 'wall', 'wall' => 'p6', 'at' => 1 ),
	array( 'id' => 's3', 'kind' => 'socket', 'host' => 'wall', 'wall' => '../p', 'at' => 1 ),
	array( 'id' => 's1', 'kind' => 'data', 'host' => 'floor', 'x' => 1, 'y' => 1 ),
	array( 'id' => 'w1', 'kind' => 'drain', 'host' => 'floor', 'x' => 1 ),
	'junk',
) );
t( 'points: valid kept, bad kind / wall / duplicate / missing coordinate dropped', 2 === count( $pts ) && 's1' === $pts[0]['id'] && 120.4 === $pts[0]['at'] && 'moved' === $pts[0]['status'] && 'added' === $pts[1]['status'], json_encode( $pts ) );
t( 'points: non-array gives an empty list', array() === nadlan_dsg_clean_points( 'x' ) );

/* ---------- ids and edit keys ---------- */
$id = nadlan_dsg_new_id(); $id2 = nadlan_dsg_new_id();
t( 'new id: 26 base32 characters, URL-safe, random', nadlan_dsg_valid_id( $id ) && strlen( $id ) >= 22 && $id !== $id2 && rawurlencode( $id ) === $id );
$key = nadlan_dsg_edit_key( $id );
t( 'edit key: 32 hex characters', 1 === preg_match( '/^[a-f0-9]{32}$/', $key ) );
t( 'edit key: the right key is accepted', nadlan_dsg_key_ok( $id, $key ) );
t( 'edit key: a wrong key is refused', ! nadlan_dsg_key_ok( $id, str_repeat( '0', 32 ) ) && ! nadlan_dsg_key_ok( $id, '' ) && ! nadlan_dsg_key_ok( $id, strtoupper( $key ) ) );
t( 'edit key: the key of another id is refused', ! nadlan_dsg_key_ok( $id2, $key ) );
t( 'edit key: a malformed id is refused', ! nadlan_dsg_key_ok( 'short', $key ) && ! nadlan_dsg_key_ok( $id . 'x', $key ) );
t( 'edit key: not stored in the clean design', false === strpos( json_encode( $c ), $key ) );

/* ---------- write guard (why no nonce) ---------- */
$okh = array( 'x_nl_designer' => '1', 'content_type' => 'application/json; charset=utf-8', 'sec_fetch_site' => 'same-origin', 'origin' => 'https://nad-lan.co.il' );
t( 'guard: a same-site JSON fetch with the header passes', '' === nadlan_dsg_write_refusal( $okh, 1000, 'nad-lan.co.il' ) );
t( 'guard: no header refused', 'header' === nadlan_dsg_write_refusal( array( 'x_nl_designer' => '' ) + $okh, 1000, 'nad-lan.co.il' ) );
t( 'guard: a form post (urlencoded) refused', 'json' === nadlan_dsg_write_refusal( array( 'content_type' => 'application/x-www-form-urlencoded' ) + $okh, 1000, 'nad-lan.co.il' ) );
t( 'guard: text/plain refused', 'json' === nadlan_dsg_write_refusal( array( 'content_type' => 'text/plain' ) + $okh, 1000, 'nad-lan.co.il' ) );
t( 'guard: cross-site refused', 'site' === nadlan_dsg_write_refusal( array( 'sec_fetch_site' => 'cross-site' ) + $okh, 1000, 'nad-lan.co.il' ) );
t( 'guard: foreign origin refused', 'origin' === nadlan_dsg_write_refusal( array( 'sec_fetch_site' => '', 'origin' => 'https://evil.example' ) + $okh, 1000, 'nad-lan.co.il' ) );
t( 'guard: origin null refused', 'origin' === nadlan_dsg_write_refusal( array( 'origin' => 'null' ) + $okh, 1000, 'nad-lan.co.il' ) );
t( 'guard: body over 256 KB refused', 'size' === nadlan_dsg_write_refusal( $okh, 300 * 1024, 'nad-lan.co.il' ) );

/* ---------- rate limit: no IP in any stored key ---------- */
$_SERVER['REMOTE_ADDR'] = '203.0.113.77'; $GLOBALS['TR'] = array();
$pass = 0; for ( $i = 0; $i < 25; $i++ ) { if ( nadlan_dsg_rl( 'save', 20, 3600 ) ) { $pass++; } }
t( 'rate limit: 20 saves pass, the 21st is refused', 20 === $pass );
$tk = implode( '|', array_keys( $GLOBALS['TR'] ) );
t( 'rate limit: the IP (or its md5) is not in the transient name', false === strpos( $tk, '203.0.113.77' ) && false === strpos( $tk, md5( '203.0.113.77' ) ) );

/* ---------- plans ---------- */
$fx = sys_get_temp_dir() . '/nldsg-test-' . getmypid();
@mkdir( $fx . '/plans', 0777, true );
file_put_contents( $fx . '/secret.json', '{"secret":1}' );
file_put_contents( $fx . '/plans/ashira-a4.json', '{}' );
file_put_contents( $fx . '/plans/index.json', json_encode( array( 'plans' => array(
	'ashira' => array( 'A4' => 'ashira-a4.json', 'B5' => 'missing.json', 'T' => '../secret.json' ),
	'evil'   => array( 'x' => '/etc/passwd' ),
) ) ) );
add_filter( 'nadlan_dsg_plans_dir', function () use ( $fx ) { return $fx . '/plans'; } );
t( 'plan: a known project and type resolves to its file', 0 === strpos( nadlan_dsg_plan_url( 'ashira', 'A4' ), 'https://nad-lan.co.il/wp-content/plugins/nadlan-config/assets/designer/plans/ashira-a4.json?v=' ) );
t( 'plan: an unknown project gives empty', '' === nadlan_dsg_plan_url( 'rainbow', 'A4' ) );
t( 'plan: an unknown type of a known project gives empty (no neighbour)', '' === nadlan_dsg_plan_url( 'ashira', 'A5' ) && '' === nadlan_dsg_plan_url( 'ashira', 'a4' ) );
t( 'plan: an indexed file that does not exist gives empty', '' === nadlan_dsg_plan_url( 'ashira', 'B5' ) );
t( 'plan: "../" in the index gives empty', '' === nadlan_dsg_plan_url( 'ashira', 'T' ) && '' === nadlan_dsg_plan_url( 'evil', 'x' ) );
t( 'plan: "../" in the project or type gives empty', '' === nadlan_dsg_plan_url( '../ashira', 'A4' ) && '' === nadlan_dsg_plan_url( 'ashira', '../A4' ) && '' === nadlan_dsg_plan_url( 'ashira/..', 'A4' ) );
t( 'plan: a direct file name with path tricks gives empty', '' === nadlan_dsg_plan_file( '../secret.json' ) && '' === nadlan_dsg_plan_file( '..\\secret.json' ) && '' === nadlan_dsg_plan_file( 'index.json' ) && '' === nadlan_dsg_plan_file( 'ashira-a4.php' ) && 'ashira-a4.json' === nadlan_dsg_plan_file( 'ashira-a4.json' ) );
t( 'plan: the parsed index is cached in a transient', (bool) array_filter( array_keys( $GLOBALS['TR'] ), function ( $k ) { return 0 === strpos( $k, 'nldsg_plans_' ); } ) );
$GLOBALS['FILTERS']['nadlan_dsg_plans_dir'] = array( function () use ( $fx ) { return $fx . '/nowhere'; } );
t( 'plan: no index file gives empty', '' === nadlan_dsg_plan_url( 'ashira', 'A4' ) );
unset( $GLOBALS['FILTERS']['nadlan_dsg_plans_dir'] );

/* ---------- the switch ---------- */
$GLOBALS['OPT'] = array(); $_GET = array();
t( 'switch: the embed is open by default (11.11.2026)', true === nadlan_dsg_on() );
t( 'switch: the server save is closed by default', false === nadlan_dsg_save_on() );
$_GET['designer'] = 'yes';
t( 'switch: another ?designer value keeps the save closed', false === nadlan_dsg_save_on() );
$_GET['designer'] = array( 'next' );
t( 'switch: an array value keeps the save closed', false === @nadlan_dsg_save_on() );
$_GET['designer'] = 'next';
t( 'switch: ?designer=next opens the save for a test', true === nadlan_dsg_save_on() );
$_GET = array(); $GLOBALS['OPT']['nadlan_designer_save'] = '1';
t( 'switch: option nadlan_designer_save = "1" opens the save', true === nadlan_dsg_save_on() );
$GLOBALS['OPT'] = array( 'nadlan_designer_enabled' => '0', 'nadlan_designer_save' => '1' );
t( 'switch: option nadlan_designer_enabled = "0" closes the embed and the save', false === nadlan_dsg_on() && false === nadlan_dsg_save_on() );

/* ---------- the shortcode ---------- */
$GLOBALS['OPT'] = array( 'nadlan_designer_enabled' => '0' ); $_GET = array(); unset( $GLOBALS['nadlan_dsg_map_done'], $GLOBALS['nadlan_dsg_n'] );
t( 'shortcode: prints nothing when closed', '' === nadlan_dsg_shortcode( array() ) );
$GLOBALS['OPT'] = array();
$GLOBALS['STAGE'] = false;
$o1 = nadlan_dsg_shortcode( array() );
$o2 = nadlan_dsg_shortcode( array() );
t( 'shortcode: one designer per page (the second prints nothing)', '' !== $o1 && '' === $o2 );
t( 'shortcode: no send hook while the save is closed', false !== strpos( $o1, '"save":false' ) );
unset( $GLOBALS['nadlan_dsg_n'], $GLOBALS['nadlan_dsg_map_done'] );
$oc = nadlan_dsg_shortcode( array( 'plans' => 'example-3r,../x,example-4r,example-5r' ) );
t( 'shortcode: plans="" gives a chooser of real plan files only, opening on the second', 3 === substr_count( $oc, '"label":"' ) && false !== strpos( $oc, '"label":"3 חדרים"' ) && false !== strpos( $oc, '"label":"5 חדרים"' ) && false === strpos( $oc, '../x' ) && false !== strpos( $oc, '"planUrl":"https://nad-lan.co.il/wp-content/plugins/nadlan-config/assets/designer/plans/example-4r.json' ), $oc );
unset( $GLOBALS['nadlan_dsg_n'], $GLOBALS['nadlan_dsg_map_done'] );
$o1 = nadlan_dsg_shortcode( array() );
t( 'shortcode: host element + one module script', 1 === substr_count( $o1, 'class="nadlan-designer"' ) && 1 === substr_count( $o1, '<script type="module">' ) );
t( 'shortcode: the import map once per page, with the stage id', 1 === substr_count( $o1 . $o2, 'type="importmap"' ) && false !== strpos( $o1, 'id="nadlan-ps-importmap"' ) && false !== strpos( $o1, 'three@0.170.0' ) );
t( 'shortcode: designer.js with the plugin version, example plan when no project', false !== strpos( $o1, 'assets/designer/designer.js?v=9.9.9' ) && false !== strpos( $o1, 'plans/example-4r.json' ) );
t( 'shortcode: REST calls carry ?designer=next while the save is closed for the public', false !== strpos( $o1, '"test":true' ) );
unset( $GLOBALS['nadlan_dsg_map_done'], $GLOBALS['nadlan_dsg_n'] ); $GLOBALS['STAGE'] = array( 'dir' => 'x' );
$o3 = nadlan_dsg_shortcode( array() );
unset( $GLOBALS['nadlan_dsg_n'] );
t( 'shortcode: no import map on a stage page', false === strpos( $o3, 'importmap' ) );
$o4 = nadlan_dsg_shortcode( array( 'project' => 'rainbow', 'type' => 'A4' ) );
t( 'shortcode: a project with no known plan prints no designer', false === strpos( $o4, '<script' ) );
unset( $GLOBALS['nadlan_dsg_n'] );
$o5 = nadlan_dsg_shortcode( array( 'height' => '"><script>alert(1)</script>' ) );
unset( $GLOBALS['nadlan_dsg_n'] );
t( 'shortcode: a bad height falls back, nothing injected', false !== strpos( $o5, 'height:86vh' ) && false === strpos( $o5, 'alert(1)' ) );
add_filter( 'nadlan_dsg_embed_config', function ( $c ) { $c['unitLabel'] = '</script><script>x()</script>דירה 10'; $c['lang'] = 'xx'; return $c; } );
add_filter( 'nadlan_dsg_send_handler', function () { return 'alert(1);//'; } );
$o6 = nadlan_dsg_shortcode( array() );
t( 'shortcode: filtered config is cleaned again (no closing script tag, lang fallback, bad send handler ignored)', 1 === substr_count( $o6, '</script>' ) && false !== strpos( $o6, '"lang":"he"' ) && false !== strpos( $o6, '"send":"share"' ) && false === strpos( $o6, 'x()' ), $o6 );
// the inline module must be valid JavaScript (node --check), when node is here
$js = preg_replace( '~^.*<script type="module">(.*)</script>.*$~s', '$1', $o1 );
$tmp = $fx . '/inline.mjs'; file_put_contents( $tmp, $js );
$chk = @shell_exec( 'node --version' ) ? (string) @shell_exec( 'node --check ' . escapeshellarg( $tmp ) . ' 2>&1 && echo NODE_OK' ) : null;
if ( null === $chk ) { echo "ok " . ( ++$n ) . " - inline module parses # SKIP node not found\n"; }
else { t( 'inline module parses (node --check)', 'NODE_OK' === trim( $chk ), $chk ); }
$GLOBALS['STAGE'] = false; $_GET = array();

/* ---------- source hygiene ---------- */
$src = file_get_contents( $PLUG . '/inc/designer.php' );
preg_match_all( '/^\s*function\s+(nadlan_[a-z0-9_]+)/m', $src, $fn );
preg_match_all( "/function_exists\\(\\s*'(nadlan_[a-z0-9_]+)'/", $src, $fe );
t( 'every function is guarded with function_exists', array() === array_diff( $fn[1], $fe[1] ), implode( ', ', array_diff( $fn[1], $fe[1] ) ) );
t( 'every function has the nadlan_dsg_ prefix', array() === array_filter( $fn[1], function ( $f ) { return 0 !== strpos( $f, 'nadlan_dsg_' ); } ) );
t( 'no long dash in the source', ! preg_match( '/[\x{2013}\x{2014}]/u', $src ) );
t( 'no X-Forwarded-For trust', false === stripos( $src, 'HTTP_X_FORWARDED' ) && false === stripos( $src, "get_header( 'x_forwarded" ) );

foreach ( glob( $fx . '/plans/*' ) as $f ) { unlink( $f ); } @rmdir( $fx . '/plans' ); @unlink( $fx . '/secret.json' ); @unlink( $tmp ); @rmdir( $fx );
echo "1..$n\n";
echo $failed ? "# FAILED $failed of $n\n" : "# all $n passed\n";
exit( $failed ? 1 : 0 );
