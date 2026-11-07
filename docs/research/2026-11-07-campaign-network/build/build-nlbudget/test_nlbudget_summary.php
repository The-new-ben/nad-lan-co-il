<?php
/*
 * nlbudget build (7.11.2026) · PHP test of registry.php.txt: php -l, the registry entry, the two summary branches, and the summary
 * function nadlan_nlb_summary() on the real data file (plugins/nadlan-config/assets/instruments/data/nlbudget.json), with a tiny
 * esc_html stub. Writes summary.he.html and summary.en.html (pasted into preview.html as the shortcode prints them).
 * Run:  php docs/research/2026-11-07-campaign-network/build/build-nlbudget/test_nlbudget_summary.php
 *       ... --summary he|en   prints one summary (read by the node test)
 * Exit code 1 on any failure.
 */
$HERE = __DIR__;
$REPO = dirname( $HERE, 5 );
$DATA = $REPO . '/plugins/nadlan-config/assets/instruments/data/nlbudget.json';
$SNIP = $HERE . '/registry.php.txt';
if ( ! function_exists( 'esc_html' ) ) { function esc_html( $s ) { return htmlspecialchars( (string) $s, ENT_QUOTES, 'UTF-8' ); } }
require $SNIP;

if ( isset( $argv[1] ) && '--summary' === $argv[1] ) { echo nadlan_nlb_summary( isset( $argv[2] ) ? $argv[2] : 'he', $DATA ); exit( 0 ); }

$n = 0; $fails = 0;
function ok( $c, $name, $got = null ) { global $n, $fails; $n++; if ( ! $c ) { $fails++; } echo ( $c ? '  ok   ' : '  FAIL ' ) . $name . ( null !== $got ? '  [' . ( is_string( $got ) ? $got : json_encode( $got, JSON_UNESCAPED_UNICODE ) ) . ']' : '' ) . "\n"; }
$dash = '/[' . "\u{2013}\u{2014}" . ']/u';

echo "1. the snippet\n";
$lint = shell_exec( 'php -l ' . escapeshellarg( $SNIP ) . ' 2>&1' );
ok( false !== strpos( (string) $lint, 'No syntax errors' ), 'php -l registry.php.txt', trim( (string) $lint ) );
$e = nadlan_nlbudget_registry_snippet( 'other', 'he' );  // any other id: the branches return early for 'nlbudget'
$x = isset( $e['nlbudget'] ) ? $e['nlbudget'] : array();
ok( 'כמה עולה לשווק את הפרויקט' === ( $x['name'] ?? '' ) && 'תקציב שיווק ליזמים' === ( $x['kicker'] ?? '' ) && 'BusinessApplication' === ( $x['cat'] ?? '' ), 'entry: the Hebrew name, kicker and category' );
ok( array( 'nlbudget.json' ) === ( $x['data'] ?? null ), 'entry: one data file, nlbudget.json' );
ok( 'What it costs to market your project' === ( $x['en']['name'] ?? '' ) && array() === ( $x['en']['related'] ?? null ), 'entry: the English name, and no Hebrew related links on the English page' );
ok( ! preg_match( $dash, json_encode( $e, JSON_UNESCAPED_UNICODE ) ), 'entry: no long dash' );
$src = file_get_contents( $SNIP );
ok( 1 === substr_count( $src, "nadlan_nlb_summary( 'he' )" ) && 1 === substr_count( $src, "nadlan_nlb_summary( 'en' )" ), 'the two summary branches' );

echo "\n2. the summary\n";
$he = nadlan_nlb_summary( 'he', $DATA ); $en = nadlan_nlb_summary( 'en', $DATA );
$d = json_decode( file_get_contents( $DATA ), true ); $f = $d['figures'];
ok( strlen( $he ) > 1500 && strlen( $en ) > 1500, 'both summaries are written', array( strlen( $he ), strlen( $en ) ) );
ok( false !== strpos( $he, '2,880,000 עד 5,760,000 ₪' ) && false !== strpos( $en, '₪2,880,000 to ₪5,760,000' ), 'the source\'s example worked through: 60 x 2.4 million, 2% to 4% = 2,880,000 to 5,760,000' );
ok( false !== strpos( $he, 'וכ־1,440,000 ₪ לשיווק בלבד' ) && false !== strpos( $en, 'about ₪1,440,000 for marketing alone' ), 'and about 1,440,000 for marketing alone (the source said about 1.4 million)' );
ok( false !== strpos( $he, '2% עד 4% לשיווק ומכירה, כולל צוות מכירות ופרסום (סטארט פוינט, טענת משרד פרסום)' ), 'Hebrew: the anchor with its source and flag' );
ok( false !== strpos( $he, '128 עד 173 ₪ לפני מע״מ במחירון של סטארט פוינט' ) && false !== strpos( $en, '₪128 to ₪173 before VAT' ), 'the lead price list, before VAT as published' );
ok( false !== strpos( $he, '300 עד 800 ₪ (סמרנקו, טענת משרד, בלי שם המקור)' ), 'the campaign cost per lead, flagged as an unnamed source' );
ok( false !== strpos( $he, '0.75% עד 2% לשיווק בלבד ו־3% עד 5% לשיווק ומכירה (Feasly, אוסטרליה, טענת משרד פרסום)' ), 'the anchors abroad, named and flagged' );
ok( false !== strpos( $he, '4,000 עד 6,000 ₪' ) && false !== strpos( $he, '1,000 עד 1,500 ₪' ) && false !== strpos( $he, '12,000 עד 30,000 ₪' ) && false !== strpos( $he, 'מבטים, מחירון הדמיות, מחירון שפורסם' ), 'the render price list rows' );
ok( false !== strpos( $he, 'כלול במנוי נדל״ן: 36,000 ₪, 72,000 ₪ או 144,000 ₪ לשנה' ) && false !== strpos( $en, 'Included in the NadLan plan: ₪36,000, ₪72,000 or ₪144,000 a year' ), 'the tour line: included in the plan, the three yearly prices' );
ok( false !== strpos( $he, 'לא פורסם מחיר ישראלי לשורות האלה' ) && false !== strpos( $en, 'No Israeli price is published for these lines' ), 'the lines without an Israeli price are said, not priced' );
ok( ! preg_match( $dash, $he . $en ), 'no long dash' );
ok( ! preg_match( '/<a\s/i', $he . $en ), 'no outbound links (sources named, not linked)' );
ok( 1 === substr_count( $he, '<table>' ) && false !== strpos( $he, '</tbody></table>' ), 'one well-closed table' );
foreach ( array( 'ממשק', 'מערכת', 'פלטפורמ', 'אלגוריתם', 'דמו', 'סימולציה', 'הדגמה', 'מנגנון', 'אינטראקטיבי', 'טכנולוגי', 'דיגיטלי' ) as $w ) { if ( false !== strpos( $he, $w ) ) { ok( false, 'tech word in Hebrew: ' . $w ); } }
foreach ( array( 'interface', 'system', 'platform', 'algorithm', 'demo', 'simulation', 'interactive', 'technology' ) as $w ) { if ( false !== stripos( $en, $w ) ) { ok( false, 'tech word in English: ' . $w ); } }
ok( true, 'no tech word in either summary' );
ok( '' === nadlan_nlb_summary( 'he', $HERE . '/no-such-file.json' ), 'no data file: an empty summary, no error' );
ok( false !== strpos( $he, $f['sp_unit']['src_he'] ) && false !== strpos( $en, $f['wedo_total']['src_en'] ), 'source names come from the data file' );

file_put_contents( $HERE . '/summary.he.html', $he . "\n" );
file_put_contents( $HERE . '/summary.en.html', $en . "\n" );
// the preview carries the summaries exactly as the shortcode prints them, between its markers
$pv = file_get_contents( $HERE . '/preview.html' );
$put = function ( $html, $tag, $body ) { return preg_replace_callback( '#<!--' . $tag . '-->.*?<!--/' . $tag . '-->#s', function () use ( $tag, $body ) { return '<!--' . $tag . '-->' . $body . '<!--/' . $tag . '-->'; }, $html ); };
$pv2 = $put( $put( $pv, 'SUM_HE', $he ), 'SUM_EN', $en );
ok( false !== strpos( $pv2, '<!--SUM_HE-->' . $he . '<!--/SUM_HE-->' ) && false !== strpos( $pv2, '<!--SUM_EN-->' . $en . '<!--/SUM_EN-->' ), 'preview.html carries both summaries' );
if ( $pv2 !== $pv ) { file_put_contents( $HERE . '/preview.html', $pv2 ); }
echo "\n" . ( $n - $fails ) . " of $n passed" . ( $fails ? ", $fails FAILED" : '' ) . "\n";
exit( $fails ? 1 : 0 );
