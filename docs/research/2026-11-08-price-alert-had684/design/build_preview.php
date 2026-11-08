<?php
// Builds the Claude Design v106 PriceAlert preview from the REAL inc/price-nudge.php markup and assets/nudge/price-alert.css.
define( 'ABSPATH', __DIR__ ); define( 'DAY_IN_SECONDS', 86400 ); define( 'HOUR_IN_SECONDS', 3600 );
$GLOBALS['H'] = array(); $GLOBALS['T'] = array(); $GLOBALS['META'] = array(); $GLOBALS['TYPE'] = array(); $GLOBALS['TITLE'] = array(); $GLOBALS['QID'] = 0;
function add_action( $h, $cb, $p = 10 ) { $GLOBALS['H'][ $h ][] = $cb; }
function add_filter() {} function register_rest_route() {}
function get_transient( $k ) { return $GLOBALS['T'][ $k ] ?? false; } function set_transient( $k, $v, $t = 0 ) { $GLOBALS['T'][ $k ] = $v; }
function get_post_meta( $id, $k, $s = false ) { return $GLOBALS['META'][ $id ][ $k ] ?? ''; }
function get_post_type( $id ) { return $GLOBALS['TYPE'][ $id ] ?? ''; }
function get_the_title( $id ) { return $GLOBALS['TITLE'][ $id ] ?? ''; }
function get_post_field( $f, $id ) { return 'demo-' . $id; }
function get_post_status() { return 'publish'; } function post_password_required() { return false; }
function get_option( $k, $d = false ) { return $d; }
function is_admin() { return false; } function is_singular() { return true; } function get_queried_object_id() { return $GLOBALS['QID']; }
function wp_strip_all_tags( $s ) { return strip_tags( $s ); }
function esc_attr( $s ) { return htmlspecialchars( (string) $s, ENT_QUOTES, 'UTF-8' ); }
function esc_html( $s ) { return htmlspecialchars( (string) $s, ENT_QUOTES, 'UTF-8' ); }
function esc_url( $s ) { return htmlspecialchars( (string) $s, ENT_QUOTES, 'UTF-8' ); }
function esc_url_raw( $s ) { return (string) $s; }
function wp_json_encode( $v ) { return json_encode( $v, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES ); }
function rest_url( $p ) { return 'https://nad-lan.co.il/wp-json/' . $p; }
function get_permalink( $id ) { return 'https://nad-lan.co.il/projects/demo-' . $id . '/'; }
function get_privacy_policy_url() { return 'https://nad-lan.co.il/privacy/'; }
function home_url( $p = '' ) { return 'https://nad-lan.co.il' . $p; }
function nadlan_cta_whatsapp_number() { return '972500000000'; }
require 'C:/Users/777/nad-lan/nad-lan-co-il/plugins/nadlan-config/inc/price-nudge.php';
$css = file_get_contents( 'C:/Users/777/nad-lan/nad-lan-co-il/plugins/nadlan-config/assets/nudge/price-alert.css' );

function markup( $id, $type, $title, $meta ) {
	$GLOBALS['QID'] = $id; $GLOBALS['TYPE'][ $id ] = $type; $GLOBALS['TITLE'][ $id ] = $title; $GLOBALS['META'][ $id ] = $meta;
	ob_start(); foreach ( $GLOBALS['H']['wp_footer'] as $cb ) { $cb(); } return ob_get_clean();
}
function frame( $m, $step, $desk, $w, $h, $fill = array() ) {
	global $css;
	$m = str_replace( array( '<template id="nlpa-tpl">', '</template>' ), '', $m );
	$m = str_replace( ' hidden data-c=', ' data-c=', $m );
	$m = str_replace( 'class="nlpa-root"', 'class="nlpa-root is-in' . ( $desk ? ' is-desk' : '' ) . '"', $m );
	$m = str_replace( 'data-step="1"', 'data-step="' . $step . '"', $m );
	foreach ( $fill as $a => $b ) { $m = str_replace( $a, $b, $m ); }
	$page = '<header style="height:56px;background:#fff;border-bottom:1px solid #e3e1da;display:flex;align-items:center;padding:0 18px;font:800 18px Assistant;color:#1f4b5c">נדל״ן</header>'
		. '<main style="padding:18px;max-width:900px;margin:0 auto;color:#3b4753;font:16px/1.6 Assistant"><h1 style="font:800 26px/1.25 Assistant;color:#14212b;margin:6px 0 10px">פרויקט מגורים חדש בצפון תל אביב</h1>'
		. '<p style="margin:0 0 14px">דירות 3 עד 6 חדרים, מרחק הליכה מהפארק ומהים. כאן מופיעים פרטי הפרויקט, המיקום, המחירים שפורסמו ושלבי הבנייה.</p>'
		. '<div style="height:' . ( $desk ? 260 : 210 ) . 'px;border-radius:16px;background:#dfe7ea"></div>'
		. '<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin-top:14px"><div style="height:64px;border-radius:12px;background:#fff;border:1px solid #e3e1da"></div><div style="height:64px;border-radius:12px;background:#fff;border:1px solid #e3e1da"></div><div style="height:64px;border-radius:12px;background:#fff;border:1px solid #e3e1da"></div></div>'
		. '<p style="margin:14px 0">הסבר על הפרויקט, ההיתרים והלוח. ' . str_repeat( 'טקסט לדוגמה בגוף העמוד. ', 18 ) . '</p></main>';
	$doc = '<!doctype html><html lang="he" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
		. '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Assistant:wght@400;600;700;800&amp;display=swap">'
		. '<style>html,body{margin:0;background:#f7f6f2}' . $css . ' #nlnu .nlpa-tick svg,#nlnu .nlpa-point svg,#nlnu .nlpa-warn{animation-iteration-count:infinite!important}</style></head><body class="nlnu-on">' . $page . $m . '</body></html>';
	static $n = 0; $n++;
	@mkdir( __DIR__ . '/ds/frames' ); file_put_contents( __DIR__ . '/ds/frames/f' . $n . '.html', $doc );
	return '<iframe title="תצוגה" style="width:' . $w . 'px;height:' . $h . 'px;border:0;border-radius:' . ( $desk ? 14 : 30 ) . 'px;box-shadow:0 10px 30px rgba(16,38,47,.18);background:#fff;flex:none" srcdoc="' . htmlspecialchars( $doc, ENT_QUOTES, 'UTF-8' ) . '"></iframe>';
}
$tlv  = markup( 4730, 'nadlan_project', 'פרויקט לדוגמה - תל אביב', array( 'city' => 'תל אביב' ) );
$rent = markup( 9001, 'nadlan_property', 'דירת 3 חדרים להשכרה בקריית אתא', array( 'city' => 'קריית אתא', 'listing_type' => 'rent' ) );
$abr  = markup( 9002, 'nadlan_intl', 'מגדל מרינה ווסט - דובאי', array( 'city' => 'דובאי' ) );
$fill = array( 'placeholder="050-1234567"' => 'placeholder="050-1234567" value="052-7654321"', 'placeholder="name@gmail.com"' => 'placeholder="name@gmail.com" value="dana@gmial.com" aria-invalid="false"',
	'<p class="nlpa-e" id="nlpa-mail-e" aria-live="polite"></p>' => '<p class="nlpa-e" id="nlpa-mail-e" aria-live="polite"><button type="button" class="nlpa-fix">התכוונתם ל־<bdi>dana@gmail.com</bdi>?</button></p>' );
$cap = function ( $t, $s ) { return '<figcaption style="font:700 13px/1.4 Assistant;color:#14212b;margin-top:8px;max-width:390px">' . $t . '<br><span style="font-weight:400;color:#3b4753">' . $s . '</span></figcaption>'; };
$row = function ( $items ) { return '<div style="display:flex;gap:22px;flex-wrap:wrap;align-items:flex-start;justify-content:center;margin:0 0 30px">' . implode( '', $items ) . '</div>'; };
$fig = function ( $f, $c ) { return '<figure style="margin:0">' . $f . $c . '</figure>'; };
$out = '<!-- @dsCard group="Cards" height=2200 width=1320 subtitle="חלון עדכוני מחירים: שימו לב, חץ למטה, טלפון ומייל (גרסה 106)" -->' . "\n"
	. '<!doctype html><html lang="he" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>PriceAlert 106</title>'
	. '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Assistant:wght@400;700;800&amp;display=swap"><style>body{margin:0;padding:22px;background:#eef2f4;font-family:Assistant,sans-serif;color:#14212b}h1{font:800 24px Assistant;margin:0 0 4px}p.lead{margin:0 0 22px;color:#3b4753;font-size:15px}h2{font:800 17px Assistant;margin:0 0 12px}</style></head><body>'
	. '<h1>PriceAlert 106: חלון עדכוני מחירים</h1><p class="lead">לוח מחירים כהה עם חץ ירידה אדום שמהבהב 3 פעמים (פחות מ־5 שניות), ואז הרשמה בשני צעדים. בטלפון: גיליון תחתון בלי רקע חוסם, אפשר להחליק למטה. במחשב: חלון במרכז עם רקע מעומעם. התצוגה בנויה מהקוד האמיתי של האתר; כאן החץ מהבהב בלי הפסקה רק כדי שיהיה אפשר לראות אותו.</p>'
	. '<h2>טלפון, 390 על 844</h2>'
	. $row( array(
		$fig( frame( $tlv, 1, false, 390, 844 ), $cap( 'צעד 1: שימו לב, החץ, ושאלה אחת', 'תל אביב: מדד מחוז תל אביב ירד ב־12 חודשים, ולכן החץ עומד ליד השורה.' ) ),
		$fig( frame( $tlv, 2, false, 390, 844, $fill ), $cap( 'צעד 2: טלפון ומייל, שניהם חובה', 'סיבה ליד הטלפון, תיקון טעות במייל, אישור נפרד לא מסומן, הודעת פרטיות.' ) ),
		$fig( frame( $tlv, 3, false, 390, 844 ), $cap( 'צעד 3: מה קורה עכשיו', 'אישור, מה יקרה הלאה, וואטסאפ למי שרוצה תשובה מיד.' ) ),
	) )
	. $row( array(
		$fig( frame( $rent, 1, false, 390, 844 ), $cap( 'מודעת השכרה', '"מחירי השכירות באזור זה משתנים", בלי חץ ליד השורה; החץ מצביע אל השאלה.' ) ),
		$fig( frame( $abr, 1, false, 390, 844 ), $cap( 'פרויקט בחו״ל', 'אין מדד ישראלי, ולכן "משתנים" בלי חץ ליד השורה.' ) ),
	) )
	. '<h2>מחשב, 1280 על 760</h2>'
	. $row( array( $fig( frame( $tlv, 1, true, 1280, 760 ), $cap( 'חלון במרכז, רקע מעומעם', 'עולה בעזיבת העכבר דרך החלק העליון או אחרי 12 שניות וקריאה של מסך; Esc, הרקע או × סוגרים.' ) ) ) )
	. '</body></html>';
file_put_contents( $argv[1], $out );
echo strlen( $out ) . " bytes\n";
