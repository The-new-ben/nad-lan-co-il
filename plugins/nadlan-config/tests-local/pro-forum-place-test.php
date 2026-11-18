<?php
/**
 * Plain PHP CLI test of the forum inside a place page (no WordPress): php tests-local/pro-forum-place-test.php
 * Loads the forum's pure part (NLF_PURE_ONLY) and then part 1 of inc/pro-forum-place.php (NLFP2_PURE_ONLY), plus static checks
 * on the module's files and on the one-line hooks it needs in the forum's own files. Exit code 0 = all passed.
 */
define( 'ABSPATH', __DIR__ . '/' );
define( 'NLF_PURE_ONLY', true );
define( 'NLFP2_PURE_ONLY', true );
require __DIR__ . '/../inc/pro-forum.php';
require __DIR__ . '/../inc/pro-forum-place.php';

$pass = 0; $fail = 0;
function t( $name, $cond ) {
	global $pass, $fail;
	if ( $cond ) { $pass++; echo "ok   $name\n"; } else { $fail++; echo "FAIL $name\n"; }
}

/* the registry: exactly the two places of board 24 */
$reg = nlfp2_registry();
t( 'registry: exactly sde-dov and hamedina', array( 'sde-dov', 'hamedina' ) === array_keys( $reg ) );
t( 'registry: labels', 'שדה דב' === $reg['sde-dov']['label'] && 'כיכר המדינה' === $reg['hamedina']['label'] );
t( 'registry: paths', '/sde-dov/' === $reg['sde-dov']['path'] && '/projects/hamedina/' === $reg['hamedina']['path'] );
t( 'registry: default heading and ask placeholder', 'שאלות של קונים על שדה דב' === $reg['sde-dov']['heading'] && 'מה תרצו לשאול על שדה דב?' === $reg['sde-dov']['ask']
	&& 'שאלות של קונים על כיכר המדינה' === $reg['hamedina']['heading'] && 'מה תרצו לשאול על כיכר המדינה?' === $reg['hamedina']['ask'] );
t( 'registry: keys fit place VARCHAR(20)', 2 === count( array_filter( array_keys( $reg ), function ( $k ) { return strlen( $k ) <= 20 && preg_match( '/^[a-z0-9-]+$/', $k ); } ) ) );
t( 'registry: no heading says פורום (board rule ג)', ! array_filter( $reg, function ( $p ) { return false !== strpos( $p['heading'], 'פורום' ); } ) );
t( 'default headings: key => heading', array( 'sde-dov' => 'שאלות של קונים על שדה דב', 'hamedina' => 'שאלות של קונים על כיכר המדינה' ) === nlfp2_default_headings() );

/* path match */
t( 'path: the two pages', 'sde-dov' === nlfp2_key_for_path( '/sde-dov/' ) && 'hamedina' === nlfp2_key_for_path( '/projects/hamedina/' ) );
t( 'path: slashes, case, query, fragment', 'sde-dov' === nlfp2_key_for_path( '/sde-dov' ) && 'sde-dov' === nlfp2_key_for_path( 'sde-dov' ) && 'sde-dov' === nlfp2_key_for_path( '/SDE-DOV/' )
	&& 'sde-dov' === nlfp2_key_for_path( '/sde-dov/?forum=on' ) && 'hamedina' === nlfp2_key_for_path( '/projects//hamedina/#x' ) );
t( 'path: every other page is nothing', '' === nlfp2_key_for_path( '/' ) && '' === nlfp2_key_for_path( '' ) && '' === nlfp2_key_for_path( '/projects/' ) && '' === nlfp2_key_for_path( '/hamedina/' )
	&& '' === nlfp2_key_for_path( '/projects/hamedina-en/' ) && '' === nlfp2_key_for_path( '/sde-dov/apartments/' ) && '' === nlfp2_key_for_path( '/tour/sde-dov/' ) && '' === nlfp2_key_for_path( '/forum/' ) );
t( 'path norm', '/projects/hamedina/' === nlfp2_path_norm( 'projects/hamedina' ) && '/' === nlfp2_path_norm( '' ) && '/a/b/' === nlfp2_path_norm( '//a//b//?q=1' ) );

/* place validation */
t( 'valid: registered keys', 'sde-dov' === nlfp2_valid( 'sde-dov' ) && 'hamedina' === nlfp2_valid( ' Hamedina ' ) );
t( 'valid: anything else is empty', '' === nlfp2_valid( '' ) && '' === nlfp2_valid( 'tel-aviv' ) && '' === nlfp2_valid( null ) && '' === nlfp2_valid( array( 'sde-dov' ) )
	&& '' === nlfp2_valid( "sde-dov'" ) && '' === nlfp2_valid( 'sde_dov' ) && '' === nlfp2_valid( 0 ) && '' === nlfp2_valid( 'label' ) );
t( 'key ok: strict', nlfp2_key_ok( 'sde-dov' ) && ! nlfp2_key_ok( 'SDE-DOV' ) && ! nlfp2_key_ok( '' ) && ! nlfp2_key_ok( 1 ) );

/* the heading option and its fallback */
t( 'heading: no option = default', 'שאלות של קונים על שדה דב' === nlfp2_heading( 'sde-dov', false ) && 'שאלות של קונים על כיכר המדינה' === nlfp2_heading( 'hamedina', array() ) );
t( 'heading: the option wins, trimmed', 'מה קונים שואלים על שדה דב' === nlfp2_heading( 'sde-dov', array( 'sde-dov' => '  מה קונים   שואלים על שדה דב ' ) ) );
t( 'heading: empty, not a string, too long = default', 'שאלות של קונים על שדה דב' === nlfp2_heading( 'sde-dov', array( 'sde-dov' => '   ' ) )
	&& 'שאלות של קונים על שדה דב' === nlfp2_heading( 'sde-dov', array( 'sde-dov' => array( 'x' ) ) )
	&& 'שאלות של קונים על שדה דב' === nlfp2_heading( 'sde-dov', array( 'sde-dov' => str_repeat( 'א', 121 ) ) )
	&& 'שאלות של קונים על שדה דב' === nlfp2_heading( 'sde-dov', 'a string option' ) );
t( 'heading: another key in the option does not leak', 'שאלות של קונים על כיכר המדינה' === nlfp2_heading( 'hamedina', array( 'sde-dov' => 'כותרת אחרת' ) ) );
t( 'heading: unknown key = empty', '' === nlfp2_heading( 'tel-aviv', array( 'tel-aviv' => 'x' ) ) );

/* the texts */
t( 'week: zero is omitted', '' === nlfp2_week_text( 0 ) && '' === nlfp2_week_text( -2 ) );
t( 'week: one and many', 'דיון אחד פעיל השבוע' === nlfp2_week_text( 1 ) && '3 דיונים פעילים השבוע' === nlfp2_week_text( 3 ) && '1,200 דיונים פעילים השבוע' === nlfp2_week_text( 1200 ) );
$now = 1763500000;
t( 'row: no answer', 'מחכה לתשובה ראשונה' === nlfp2_row_meta( 0, $now - 60, $now ) );
t( 'row: answers and time', '4 תשובות · לפני שעה' === nlfp2_row_meta( 4, $now - 3700, $now ) && 'תשובה אחת · אתמול' === nlfp2_row_meta( 1, $now - 100000, $now )
	&& '2 תשובות · לפני 5 דקות' === nlfp2_row_meta( 2, $now - 300, $now ) );
t( 'row: past a week the date, or nothing', '2 תשובות · 3.11.2026' === nlfp2_row_meta( 2, $now - 30 * 86400, $now, '3.11.2026' ) && '2 תשובות' === nlfp2_row_meta( 2, $now - 30 * 86400, $now ) );
t( 'row tint: 3+ raspberry, 1-2 sea, 0 grey', array( '#FBE7EF', '#8A0F3D' ) === nlfp2_row_tint( 4 ) && array( '#E6F0F4', '#1F4B5C' ) === nlfp2_row_tint( 2 ) && array( '#EEF2F4', '#3A4650' ) === nlfp2_row_tint( 0 ) );
t( 'board words: all, back, none', 'לכל השאלות על שדה דב' === nlfp2_all_text( 'שדה דב' ) && 'כל המידע על שדה דב: מחירים, פרויקטים ומפה' === nlfp2_back_text( 'שדה דב' ) && 'עוד אין שאלות. שאלו ראשונים.' === nlfp2_none_text() );

/* static checks: the module, its assets, the one-line hooks in the forum's files */
$root = __DIR__ . '/..';
$php  = (string) file_get_contents( $root . '/inc/pro-forum-place.php' );
$core = (string) file_get_contents( $root . '/inc/pro-forum.php' );
$rnd  = (string) file_get_contents( $root . '/inc/pro-forum-render.php' );
$js   = (string) file_get_contents( $root . '/assets/proforum/place.js' );
$css  = (string) file_get_contents( $root . '/assets/proforum/place.css' );
$fjs  = (string) file_get_contents( $root . '/assets/proforum/forum.js' );
$kit  = (string) file_get_contents( $root . '/../../scripts/project-stage/forum_testkit.py' );
t( 'core: loaded once, after the home module', 1 === substr_count( $core, "require_once __DIR__ . '/pro-forum-place.php';" ) && strpos( $core, "/pro-forum-place.php'" ) > strpos( $core, "/pro-forum-home.php'" ) );
t( 'core: filter args, home url args (HOOK lines)', 1 === substr_count( $core, "apply_filters( 'nlf_filter_args'," ) && 1 === substr_count( $core, "apply_filters( 'nlf_home_url_args'," ) );
t( 'core: the canonical of a filtered list is /forum/', false !== strpos( $core, "&& empty( \$a['place'] ) && \$a['pg'] > 1" ) );
t( 'render: the where hook, in the list and in the open count', 1 === substr_count( $rnd, "apply_filters( 'nlf_home_where_sql', '', \$a )" ) && false !== strpos( $rnd, "if ( '' !== \$xw ) { \$open_w .= ' AND ' . \$xw; }" ) );
t( 'render: the place chip before the category tag', false !== strpos( $rnd, "apply_filters( 'nlf_topic_meta_tags', '', \$t ) . nlf_cat_tag( \$t['cat'] )" ) );
t( 'the ask box is forum.js\'s own [data-nlf-ask] inside .nlf-win', false !== strpos( $php, 'class="nlf nlf-win nlfpl"' ) && false !== strpos( $php, 'data-nlf-ask' ) && false !== strpos( $fjs, "f.closest('.nlf-win')" ) );
t( 'the footer sheets print on the place page', false !== strpos( $php, "\$GLOBALS['nlf_card_printed'] = true;" ) && false !== strpos( $rnd, "empty( \$GLOBALS['nlf_card_printed'] )" ) );
t( 'the place goes through nlf_post_check / nlf_post_created, no new route', false !== strpos( $php, "add_filter( 'nlf_post_check'" ) && false !== strpos( $php, "add_action( 'nlf_post_created'" ) && false === strpos( $php, 'register_rest_route' ) );
t( 'the content filter: late, once, gate open', false !== strpos( $php, '}, 90 );' ) && false !== strpos( $php, 'nlfp2_on_page()' ) && false !== strpos( $php, "function_exists( 'nlf_gate_open' ) && nlf_gate_open()" ) );
t( 'table: topic_id primary, place VARCHAR(20)', false !== strpos( $php, 'PRIMARY KEY  (topic_id)' ) && false !== strpos( $php, 'place VARCHAR(20)' ) && false !== strpos( $php, "'nadlan_forum_place'" ) );
t( 'headings live in one option with the defaults', false !== strpos( $php, "add_option( 'nadlan_forum_place_headings', nlfp2_default_headings()" ) && false !== strpos( $php, "get_option( 'nadlan_forum_place_headings', nlfp2_default_headings() )" ) );
t( 'no new address, no robots, no redirect, no JSON-LD', false === strpos( $php, 'add_rewrite_rule' ) && false === stripos( $php, 'noindex' ) && false === strpos( $php, 'wp_redirect' ) && false === strpos( $php, 'wp_safe_redirect' )
	&& false === strpos( $php, 'ld+json' ) && false === strpos( $php, "add_filter( 'nlf_jsonld'" ) && false === strpos( $php, 'robots' ) );
t( 'the video room row is not built (no place room kind)', false === strpos( $php, 'nlfc_room_row_html(' ) );
t( 'js: nlfExtra wrapped, not replaced; text only through textContent', false !== strpos( $js, 'prev.call(cf, path)' ) && false === strpos( $js, 'innerHTML' ) && false === strpos( $js, 'insertAdjacentHTML' ) );
t( 'css: every rule under .nlf with the nlfpl- prefix', ! preg_match( '/^(?!\.nlf[ .]|@media|\/\*| |\t|\})[^\n]*\{/m', $css ) && ! preg_match( '/\.nlf \.(?!nlfpl-)[a-z]/', $css ) );
t( 'css: buttons and links pressed are 44px or more', false !== strpos( $css, 'min-height:44px;height:44px' ) && false !== strpos( $css, '.nlf .nlfpl-fchip{display:inline-flex;align-items:center;gap:8px;min-height:44px' ) && false !== strpos( $css, 'min-height:46px' ) );
t( 'board palette in the css', false !== strpos( $css, '#B0144F' ) && false !== strpos( $css, '#2F6F86' ) && false !== strpos( $css, '#101820' ) && false !== strpos( $css, '#3A4650' ) );
t( 'test kit clean removes the place rows', false !== strpos( $kit, 'nlfp2_purge_topics( (array) $tids )' ) && false !== strpos( $php, 'function nlfp2_purge_topics(' ) );
t( 'no long dashes in the new files', ! preg_match( '/\x{2014}|\x{2013}/u', $php . $js . $css ) );

echo "\n$pass passed, $fail failed\n";
exit( $fail ? 1 : 0 );
