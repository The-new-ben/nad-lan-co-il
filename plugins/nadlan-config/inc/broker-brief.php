<?php
/**
 * nadlan-config · Material request for one property (x-broker-brief) · v1.2.0 · 20.10.2026
 *
 * Ben, 20.10.2026: "make Meital a special link where she uploads, in an orderly way, everything we need for the
 * Kochav HaTzafon property: photos, the apartment's plan, the view, a description, the answers to our questions."
 *
 * /drop/<token>/brief/<key>/ is a private page (the broker's own drop token + a brief key bound to that broker and to one
 * listing). Sections: photos of the property, the plan, the view from the balcony, a short video or a link, documents;
 * then short questions, saved field by field as they are typed (she can stop and come back). Files are kept OUTSIDE the
 * web root (beside the WordPress folder, like the owner wizard's drafts): nothing is public until we choose it for the
 * page. Images lose their location data on arrival. Admins read and download through /wp-json/nadlan/v1/brief/<key>.
 * v1.1.0 (Ben, 20.10): the property is an existing, rented home (not a new project): no build or entry questions; the
 * questions cover upgrades, registration and nearby prices.
 * v1.2.0 (Ben, 20.10): the home is FOR SALE (18,000,000); the tenancy is not asked and never mentioned (buyers hear it
 * only when they call).
 * Needs x-broker-drop (the token). Installed as the Code Snippet "x-broker-brief" by scripts/broker-edit/deployedit.py.
 */

if ( ! defined( 'ABSPATH' ) ) { return; }
if ( defined( 'NL_BRIEF_VERSION' ) ) { return; }
define( 'NL_BRIEF_VERSION', '1.2.0' );
define( 'NL_BRIEF_MAX', 62914560 ); // 60 MB a file

/** The briefs: key => broker, listing, title. */
function nl_brief_defs() {
	return array(
		'kochav-ph' => array( 'broker' => 7833, 'listing' => 7634, 'title' => 'המיני פנטהאוז בכוכב הצפון' ),
	);
}

function nl_brief_dir( $key ) {
	$base = defined( 'NL_OWNER_PRIVATE_DIR' ) ? NL_OWNER_PRIVATE_DIR : rtrim( dirname( ABSPATH ), '/' ) . '/nl-private';
	$dir  = rtrim( $base, '/' ) . '/brief/' . $key;
	if ( ! is_dir( $dir ) ) { wp_mkdir_p( $dir ); }
	return $dir;
}

function nl_brief_get( $key ) {
	$v = json_decode( (string) get_option( 'nl_brief_' . $key, '' ), true );
	return is_array( $v ) ? $v + array( 'answers' => array(), 'files' => array() ) : array( 'answers' => array(), 'files' => array() );
}

function nl_brief_put( $key, $v ) {
	$v['updated'] = gmdate( 'c' );
	update_option( 'nl_brief_' . $key, wp_json_encode( $v, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES ), false );
}

/** Who may use the brief: the broker whose drop token it is, and only for a brief bound to that broker. */
function nl_brief_auth( $token, $key ) {
	if ( ! function_exists( 'nl_drop_broker_by_token' ) ) { return new WP_Error( 'nl_brief_off', 'הדף לא זמין כרגע.', array( 'status' => 503 ) ); }
	$defs = nl_brief_defs();
	if ( ! isset( $defs[ $key ] ) ) { return new WP_Error( 'nl_brief_none', 'הדף לא נמצא.', array( 'status' => 404 ) ); }
	$b = nl_drop_broker_by_token( (string) $token );
	if ( ! $b || (int) $b['id'] !== (int) $defs[ $key ]['broker'] ) { return new WP_Error( 'nl_brief_none', 'הדף לא נמצא.', array( 'status' => 404 ) ); }
	return array( 'b' => $b, 'def' => $defs[ $key ] );
}

/** The questions: id, label, hint, type (text, area, yesno), group. Plain Hebrew, the broker's words. */
function nl_brief_questions() {
	return array(
		array( 'g' => 'הבניין', 'id' => 'address', 'l' => 'כתובת הבניין', 'h' => 'לא תפורסם. צריך אותה כדי לבנות את המפה, הנוף והשמש בדיוק.', 't' => 'text' ),
		array( 'g' => 'הבניין', 'id' => 'project', 'l' => 'שם הבניין או הפרויקט, ומי בנה אותו', 'h' => 'אם יש. יזם מוכר מוסיף לערך', 't' => 'text' ),
		array( 'g' => 'הבניין', 'id' => 'floors', 'l' => 'כמה קומות ודירות בבניין, כמה דירות בקומה 11, ומה יש בקומה 12 מעל הדירה', 'h' => 'למשל: פנטהאוז אחד מעל, האם רואים ממנו את המרפסת', 't' => 'area' ),
		array( 'g' => 'הבניין', 'id' => 'amenities', 'l' => 'מה יש בבניין', 'h' => 'לובי, שומר או לובי מאויש, חדר כושר, חדר דיירים, מספר מעליות, חניון, גנרטור', 't' => 'area' ),
		array( 'g' => 'הדירה', 'id' => 'sizes', 'l' => 'שטח הדירה ושטח כל מרפסת לפי הנסח או החוזה', 'h' => 'במדלן כתוב 190 מ״ר, מרפסות 74 ו-4 מ״ר. לתקן אם צריך. האם המרפסת פתוחה לשמיים או מקורה בחלקה', 't' => 'text' ),
		array( 'g' => 'הדירה', 'id' => 'rooms', 'l' => 'רשימת החדרים, כולל שירותים ומקלחות', 'h' => 'למשל: סלון ופינת אוכל, מטבח, סוויטת הורים עם חדר רחצה וחדר ארונות, 2 חדרי ילדים, ממ״ד, חדר רחצה, שירותי אורחים, מרפסת שירות', 't' => 'area' ),
		array( 'g' => 'הדירה', 'id' => 'facing', 'l' => 'לאן פונים הסלון, החדרים והמרפסת, ומה רואים מכל כיוון', 'h' => 'למשל: מערב ודרום, ים, פארק הירקון, מגדלי העיר. האם יש משהו שעתיד להיבנות מול הנוף', 't' => 'area' ),
		array( 'g' => 'הדירה', 'id' => 'upgrades', 'l' => 'מה שודרג בדירה מעבר למפרט הקבלן', 'h' => 'מטבח ומכשירים, נגרות, בית חכם, תאורה, מיזוג, ריצוף, הצללה במרפסת. ומה נשאר בדירה בעסקה', 't' => 'area' ),
		array( 'g' => 'הדירה', 'id' => 'ceiling', 'l' => 'גובה התקרה', 'h' => 'אם ידוע', 't' => 'text' ),
		array( 'g' => 'הדירה', 'id' => 'parking', 'l' => 'חניות ומחסן', 'h' => 'כמה, צמודות, מקורות, זו אחר זו או זו ליד זו, גודל המחסן', 't' => 'text' ),
		array( 'g' => 'מכירה', 'id' => 'price', 'l' => 'המחיר המבוקש לפרסום', 'h' => 'כרגע באתר: 18,000,000 ש״ח. לעדכן אם צריך', 't' => 'text' ),
		array( 'g' => 'מכירה', 'id' => 'costs', 'l' => 'ועד בית וארנונה בחודש', 'h' => 'אם ידוע', 't' => 'text' ),
		array( 'g' => 'מכירה', 'id' => 'register', 'l' => 'רישום הדירה: טאבו או חברה משכנת, והאם כל השטחים והמרפסות כלולים בהיתר', 'h' => 'בשביל הקונה ועורך הדין שלו. לא יפורסם', 't' => 'text' ),
		array( 'g' => 'מכירה', 'id' => 'comps', 'l' => 'עסקאות או מחירים שאת מכירה בבניין או בסביבה', 'h' => 'כל מספר עוזר להראות לקונה את הערך', 't' => 'area' ),
		array( 'g' => 'מכירה', 'id' => 'strengths', 'l' => 'מה הכי תופס את מי שבא לראות את הדירה', 'h' => 'במילים שלך', 't' => 'area' ),
		array( 'g' => 'מכירה', 'id' => 'buyers', 'l' => 'מי לדעתך הקונה המתאים, ומי כבר התעניין', 'h' => 'למשל: משפחה משדרגת, תושבי חוץ, מי שעוזב וילה. בלי שמות', 't' => 'area' ),
		array( 'g' => 'מכירה', 'id' => 'elsewhere', 'l' => 'איפה הנכס מפורסם היום', 'h' => 'קישורים: יד2, מדלן, אינסטגרם, אתרים בחו״ל', 't' => 'area' ),
		array( 'g' => 'מכירה', 'id' => 'desc', 'l' => 'תיאור חופשי', 'h' => 'כל מה שלא נשאל כאן ושכדאי שנדע', 't' => 'area' ),
		array( 'g' => 'אישור', 'id' => 'ok_publish', 'l' => 'אני מאשרת לפרסם את התמונות והפרטים שהעליתי בעמוד הנכס באתר (הכתובת המדויקת לא תפורסם)', 'h' => '', 't' => 'yesno' ),
	);
}

function nl_brief_sections() {
	return array(
		array( 'id' => 'photos', 'l' => 'תמונות של הדירה', 'h' => 'כל החדרים, גם השירותים, המטבח והמרפסת. כמה שיותר, באיכות המקורית. תמונות מהטלפון מצוינות.', 'accept' => 'image/*' ),
		array( 'id' => 'plan', 'l' => 'תוכנית הדירה', 'h' => 'תוכנית מהקבלן או צילום של התוכנית. קובץ PDF או תמונה. אם יש גם תוכנית קומה או חתך, גם אותם.', 'accept' => 'image/*,application/pdf' ),
		array( 'id' => 'view', 'l' => 'הנוף מהמרפסת ומהסלון', 'h' => 'צילום רחב לכל כיוון. אם אפשר: בבוקר, בשקיעה ובלילה.', 'accept' => 'image/*' ),
		array( 'id' => 'video', 'l' => 'סרטון קצר (לא חובה)', 'h' => 'סיבוב בדירה מהטלפון, עד 60MB. סרטון גדול יותר: אפשר לשים קישור בשאלה "איפה הנכס מפורסם היום".', 'accept' => 'video/*' ),
		array( 'id' => 'docs', 'l' => 'מסמכים (לא חובה)', 'h' => 'מפרט טכני, חוברת פרויקט, הדמיות מהיזם. לשימוש פנימי שלנו.', 'accept' => 'image/*,application/pdf' ),
	);
}

/* ---------------- the page ---------------- */
add_action( 'parse_request', function () {
	$path = trim( (string) wp_parse_url( isset( $_SERVER['REQUEST_URI'] ) ? wp_unslash( $_SERVER['REQUEST_URI'] ) : '', PHP_URL_PATH ), '/' );
	if ( ! preg_match( '#^drop/([a-z0-9]{24})/brief/([a-z0-9-]{3,40})$#', $path, $m ) ) { return; }
	do_action( 'litespeed_control_set_nocache', 'nadlan brief page' );
	nocache_headers();
	header( 'Cache-Control: no-store, private, max-age=0' );
	header( 'X-Robots-Tag: noindex, nofollow' );
	header( 'Referrer-Policy: no-referrer' );
	header( 'Content-Type: text/html; charset=utf-8' );
	$a = nl_brief_auth( $m[1], $m[2] );
	if ( is_wp_error( $a ) ) { status_header( 404 ); echo '<!doctype html><meta charset="utf-8"><title>nad-lan</title><p style="font-family:Arial;padding:40px;direction:rtl">הקישור לא פעיל.</p>'; exit; }
	status_header( 200 );
	$cfg = array( 'api' => esc_url_raw( rest_url( 'nadlan/v1/drop/' . $m[1] . '/brief/' . $m[2] ) ), 'q' => nl_brief_questions(), 's' => nl_brief_sections() );
	$t   = $a['def']['title'];
	echo '<!doctype html><html lang="he" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><meta name="robots" content="noindex,nofollow"><meta name="referrer" content="no-referrer">';
	echo '<title>' . esc_html( 'חומרים לנכס · ' . $t ) . '</title><link rel="preconnect" href="https://fonts.googleapis.com"><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Assistant:wght@400;600;700&display=swap">';
	echo '<style>' . nl_brief_css() . '</style></head><body><header class="top"><div class="wrap"><b>' . esc_html( $a['b']['name_he'] ) . '</b><span>חומרים לנכס</span></div></header><main class="wrap">';
	echo '<section class="card intro"><h1>' . esc_html( $t ) . '</h1><p>כאן מעלים את כל מה שצריך לעמוד של הנכס. כל קובץ וכל תשובה נשמרים מיד, אפשר להפסיק ולחזור לאותו קישור מתי שנוח.</p>';
	echo '<ol class="steps"><li>מעלים תמונות, תוכנית ותמונות של הנוף.</li><li>עונים על השאלות הקצרות למטה.</li><li>מסמנים אישור פרסום. זהו.</li></ol><p class="small">הקבצים נשמרים אצלנו באופן פרטי ולא מתפרסמים עד שבוחרים אותם לעמוד.</p></section>';
	echo '<div id="app"></div><p class="foot">הקישור אישי. שאלה? כותבים לבן בוואטסאפ.</p></main>';
	echo '<script>window.NLBRIEF=' . wp_json_encode( $cfg, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES ) . ';</script><script>' . nl_brief_js() . '</script></body></html>';
	exit;
}, -2 );

/* ---------------- REST ---------------- */
add_action( 'rest_api_init', function () {
	$t = '/drop/(?P<token>[a-z0-9]{24})/brief/(?P<key>[a-z0-9-]{3,40})';
	$o = array( 'permission_callback' => '__return_true' );
	register_rest_route( 'nadlan/v1', $t . '/state', $o + array( 'methods' => 'GET', 'callback' => 'nl_brief_rest_state' ) );
	register_rest_route( 'nadlan/v1', $t . '/answer', $o + array( 'methods' => 'POST', 'callback' => 'nl_brief_rest_answer' ) );
	register_rest_route( 'nadlan/v1', $t . '/file', $o + array( 'methods' => 'POST', 'callback' => 'nl_brief_rest_file' ) );
	register_rest_route( 'nadlan/v1', $t . '/file/(?P<fid>[a-z0-9]{12})', $o + array( 'methods' => 'DELETE', 'callback' => 'nl_brief_rest_delete' ) );
	// admins: everything, and each file
	$adm = array( 'permission_callback' => function () { return current_user_can( 'manage_options' ); } );
	register_rest_route( 'nadlan/v1', '/brief/(?P<key>[a-z0-9-]{3,40})', $adm + array( 'methods' => 'GET', 'callback' => function ( $req ) { return nl_brief_get( (string) $req['key'] ); } ) );
	register_rest_route( 'nadlan/v1', '/brief/(?P<key>[a-z0-9-]{3,40})/file/(?P<fid>[a-z0-9]{12})', $adm + array( 'methods' => 'GET', 'callback' => 'nl_brief_rest_download' ) );
} );

function nl_brief_public_files( $files ) {
	$out = array();
	foreach ( (array) $files as $f ) {
		$out[] = array( 'id' => $f['id'], 'section' => $f['section'], 'name' => $f['name'], 'size' => (int) $f['size'], 'type' => $f['type'], 'thumb' => (string) ( $f['thumb'] ?? '' ) );
	}
	return $out;
}

function nl_brief_rest_state( WP_REST_Request $req ) {
	$a = nl_brief_auth( $req['token'], $req['key'] );
	if ( is_wp_error( $a ) ) { return $a; }
	$v = nl_brief_get( (string) $req['key'] );
	return array( 'answers' => (object) $v['answers'], 'files' => nl_brief_public_files( $v['files'] ) );
}

function nl_brief_rest_answer( WP_REST_Request $req ) {
	$a = nl_brief_auth( $req['token'], $req['key'] );
	if ( is_wp_error( $a ) ) { return $a; }
	if ( function_exists( 'nl_drop_rate' ) && nl_drop_rate( $a['b']['id'], 'brief_answer', 600, HOUR_IN_SECONDS ) ) { return new WP_Error( 'rate', 'הרבה שינויים בשעה האחרונה.', array( 'status' => 429 ) ); }
	$d   = (array) $req->get_json_params();
	$ids = wp_list_pluck( nl_brief_questions(), 'id' );
	$id  = (string) ( $d['id'] ?? '' );
	if ( ! in_array( $id, $ids, true ) ) { return new WP_Error( 'nl_brief_q', 'שאלה לא מוכרת.', array( 'status' => 400 ) ); }
	$val = trim( wp_strip_all_tags( (string) ( $d['value'] ?? '' ) ) );
	$val = function_exists( 'mb_substr' ) ? mb_substr( $val, 0, 4000 ) : substr( $val, 0, 4000 );
	$v   = nl_brief_get( (string) $req['key'] );
	$v['answers'][ $id ] = array( 'v' => $val, 'at' => gmdate( 'c' ) );
	nl_brief_put( (string) $req['key'], $v );
	return array( 'ok' => true );
}

function nl_brief_rest_file( WP_REST_Request $req ) {
	$a = nl_brief_auth( $req['token'], $req['key'] );
	if ( is_wp_error( $a ) ) { return $a; }
	if ( function_exists( 'nl_drop_rate' ) && nl_drop_rate( $a['b']['id'], 'brief_file', 300, HOUR_IN_SECONDS ) ) { return new WP_Error( 'rate', 'הרבה קבצים בשעה האחרונה. אפשר להמשיך בעוד כמה דקות.', array( 'status' => 429 ) ); }
	$sec = (string) $req->get_param( 'section' );
	if ( ! in_array( $sec, wp_list_pluck( nl_brief_sections(), 'id' ), true ) ) { return new WP_Error( 'nl_brief_sec', 'חלק לא מוכר.', array( 'status' => 400 ) ); }
	$files = $req->get_file_params();
	$f     = $files['file'] ?? null;
	if ( ! is_array( $f ) || empty( $f['tmp_name'] ) || ! is_uploaded_file( $f['tmp_name'] ) ) { return new WP_Error( 'nofile', 'לא התקבל קובץ.', array( 'status' => 400 ) ); }
	if ( (int) $f['size'] > NL_BRIEF_MAX ) { return new WP_Error( 'big', 'הקובץ גדול מ-60MB. אפשר לשים קישור במקום.', array( 'status' => 400 ) ); }
	$mimes = array( 'jpg|jpeg|jpe' => 'image/jpeg', 'png' => 'image/png', 'webp' => 'image/webp', 'heic' => 'image/heic', 'heif' => 'image/heif', 'pdf' => 'application/pdf', 'mp4|m4v' => 'video/mp4', 'mov|qt' => 'video/quicktime' );
	$chk   = wp_check_filetype_and_ext( $f['tmp_name'], $f['name'], $mimes );
	if ( empty( $chk['type'] ) ) { return new WP_Error( 'type', 'אפשר להעלות תמונות, PDF או סרטון.', array( 'status' => 400 ) ); }
	$fid  = substr( bin2hex( random_bytes( 8 ) ), 0, 12 );
	$dir  = nl_brief_dir( (string) $req['key'] );
	$dest = $dir . '/' . $fid . '.' . ( $chk['ext'] ?: 'bin' );
	if ( ! @move_uploaded_file( $f['tmp_name'], $dest ) ) { return new WP_Error( 'move', 'ההעלאה נכשלה. אפשר לנסות שוב.', array( 'status' => 500 ) ); }
	@chmod( $dest, 0640 );
	if ( strpos( $chk['type'], 'image/' ) === 0 && function_exists( 'nl_drop_strip_gps' ) ) { nl_drop_strip_gps( $dest, $chk['type'] ); }
	// a small preview for the broker's own screen (data URI, never a public file)
	$thumb = '';
	if ( in_array( $chk['type'], array( 'image/jpeg', 'image/png', 'image/webp' ), true ) ) {
		$ed = wp_get_image_editor( $dest );
		if ( ! is_wp_error( $ed ) ) {
			$ed->resize( 240, 240, false );
			$tmp = wp_tempnam( 'nlb' ) . '.jpg';
			$sv  = $ed->save( $tmp, 'image/jpeg' );
			if ( ! is_wp_error( $sv ) && is_readable( $sv['path'] ) ) { $thumb = 'data:image/jpeg;base64,' . base64_encode( (string) file_get_contents( $sv['path'] ) ); @unlink( $sv['path'] ); }
			@unlink( $tmp );
		}
	}
	$name = sanitize_file_name( (string) $f['name'] );
	$v    = nl_brief_get( (string) $req['key'] );
	$v['files'][] = array( 'id' => $fid, 'section' => $sec, 'name' => $name, 'size' => (int) filesize( $dest ), 'type' => $chk['type'], 'path' => basename( $dest ), 'thumb' => $thumb, 'at' => gmdate( 'c' ) );
	nl_brief_put( (string) $req['key'], $v );
	return array( 'ok' => true, 'file' => nl_brief_public_files( array( end( $v['files'] ) ) )[0] );
}

function nl_brief_rest_delete( WP_REST_Request $req ) {
	$a = nl_brief_auth( $req['token'], $req['key'] );
	if ( is_wp_error( $a ) ) { return $a; }
	$v = nl_brief_get( (string) $req['key'] );
	foreach ( $v['files'] as $i => $f ) {
		if ( $f['id'] === (string) $req['fid'] ) {
			// kept on disk in a "removed" folder (never destroyed by the broker's tap), out of the list
			$dir = nl_brief_dir( (string) $req['key'] );
			wp_mkdir_p( $dir . '/removed' );
			@rename( $dir . '/' . $f['path'], $dir . '/removed/' . $f['path'] );
			array_splice( $v['files'], $i, 1 );
			nl_brief_put( (string) $req['key'], $v );
			return array( 'ok' => true );
		}
	}
	return new WP_Error( 'nl_brief_nf', 'הקובץ לא נמצא.', array( 'status' => 404 ) );
}

function nl_brief_rest_download( WP_REST_Request $req ) {
	$v = nl_brief_get( (string) $req['key'] );
	foreach ( $v['files'] as $f ) {
		if ( $f['id'] === (string) $req['fid'] ) {
			$p = nl_brief_dir( (string) $req['key'] ) . '/' . $f['path'];
			if ( ! is_readable( $p ) ) { break; }
			return array( 'name' => $f['name'], 'type' => $f['type'], 'b64' => base64_encode( (string) file_get_contents( $p ) ) );
		}
	}
	return new WP_Error( 'nl_brief_nf', 'not found', array( 'status' => 404 ) );
}

/* ---------------- look and script ---------------- */
function nl_brief_css() {
	return <<<'NLBCSS'
:root{--paper:#F7F6F2;--surf:#FFFFFF;--ink:#14212B;--mute:#5E6A74;--line:#E3E1DA;--sea:#2F6F86;--deep:#1F4B5C;--sand:#EEE9DD;--ok:#2E7D5B;--bad:#B3261E;color-scheme:light}
*{box-sizing:border-box}body{margin:0;background:var(--paper);color:var(--ink);font:400 17px/1.55 Assistant,Arial,sans-serif}
.wrap{max-width:720px;margin:0 auto;padding:0 max(16px,env(safe-area-inset-right)) 0 max(16px,env(safe-area-inset-left))}
.top{background:var(--deep);color:#fff;padding:12px 0}.top .wrap{display:flex;justify-content:space-between;align-items:center}.top span{opacity:.85;font-size:15px}
main{padding:16px 0 80px;display:grid;gap:14px}
.card{background:var(--surf);border:1px solid var(--line);border-radius:14px;padding:16px}
h1{margin:0 0 6px;font-size:24px}h2{margin:0 0 4px;font-size:19px}
.steps{margin:8px 0;padding-inline-start:20px}.small,.hint{color:var(--mute);font-size:14px;margin:6px 0 0}
.sec .count{color:var(--ok);font-weight:700;font-size:14px}
.up{display:flex;align-items:center;justify-content:center;gap:8px;min-height:52px;margin-top:10px;border:2px dashed var(--sea);border-radius:12px;color:var(--deep);font-weight:700;cursor:pointer;text-align:center;padding:8px}
.up:focus-within{outline:3px solid var(--sea);outline-offset:2px}
.files{list-style:none;margin:10px 0 0;padding:0;display:grid;grid-template-columns:repeat(auto-fill,minmax(96px,1fr));gap:8px}
.files li{position:relative;border:1px solid var(--line);border-radius:10px;overflow:hidden;background:var(--sand);aspect-ratio:1;display:flex;align-items:center;justify-content:center;font-size:12px;text-align:center;padding:4px;word-break:break-all}
.files li img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.files li button{position:absolute;top:4px;left:4px;width:34px;height:34px;border-radius:50%;border:0;background:rgba(20,33,43,.75);color:#fff;font-size:18px;cursor:pointer}
.files li.busy{opacity:.6}.files li .bar{position:absolute;inset:auto 0 0 0;height:5px;background:var(--sea)}
.q{display:grid;gap:6px;margin-top:14px}.q label{font-weight:700}
.q input,.q textarea{width:100%;min-height:48px;border:1.5px solid var(--line);border-radius:10px;padding:10px 12px;font:400 17px Assistant,Arial;background:var(--surf);color:var(--ink)}
.q textarea{min-height:96px}.q input:focus,.q textarea:focus{border-color:var(--sea);outline:none;box-shadow:0 0 0 3px rgba(47,111,134,.22)}
.q .st{font-size:13px;color:var(--ok);min-height:18px}
.yes{display:flex;gap:10px;align-items:flex-start;font-weight:700;cursor:pointer}.yes input{width:26px;height:26px;margin-top:2px}
.done{background:#E9F4EE;border-color:#BFDCCB}
.foot{color:var(--mute);font-size:14px;text-align:center}
NLBCSS;
}

function nl_brief_js() {
	return <<<'NLBJS'
(function(){
var C=window.NLBRIEF||{},API=C.api,app=document.getElementById('app');if(!API||!app)return;
var esc=function(s){return String(s==null?'':s).replace(/[&<>"]/g,function(c){return{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]})};
var S={answers:{},files:[]};
function kb(n){return n>1048576?(n/1048576).toFixed(1)+'MB':Math.round(n/1024)+'KB'}
function render(){var h='';
 C.s.forEach(function(s){var fs=S.files.filter(function(f){return f.section===s.id});
  h+='<section class="card sec" data-s="'+s.id+'"><h2>'+esc(s.l)+' <span class="count">'+(fs.length?'· '+fs.length+' הועלו':'')+'</span></h2><p class="hint">'+esc(s.h)+'</p>'+
   '<label class="up"><input type="file" multiple accept="'+esc(s.accept)+'" hidden><span aria-hidden="true">+</span>הוספת קבצים</label><ul class="files">'+
   fs.map(function(f){return '<li title="'+esc(f.name)+'">'+(f.thumb?'<img alt="" src="'+f.thumb+'">':esc(f.name)+'<br>'+kb(f.size))+'<button type="button" data-del="'+f.id+'" aria-label="הסרת '+esc(f.name)+'">×</button></li>'}).join('')+'</ul></section>'});
 var g='';h+='<section class="card"><h2>שאלות קצרות</h2><p class="hint">כל תשובה נשמרת לבד. מה שלא ידוע, משאירים ריק.</p>';
 C.q.forEach(function(q){if(q.g!==g){g=q.g;h+='<h3 style="margin:18px 0 0;font-size:16px;color:var(--deep)">'+esc(g)+'</h3>'}
  var v=(S.answers[q.id]&&S.answers[q.id].v)||'';
  if(q.t==='yesno')h+='<div class="q"><label class="yes"><input type="checkbox" data-q="'+q.id+'"'+(v==='yes'?' checked':'')+'><span>'+esc(q.l)+'</span></label><span class="st" data-st="'+q.id+'"></span></div>';
  else h+='<div class="q"><label for="q-'+q.id+'">'+esc(q.l)+'</label>'+(q.t==='area'?'<textarea id="q-'+q.id+'" data-q="'+q.id+'" rows="4">'+esc(v)+'</textarea>':'<input id="q-'+q.id+'" data-q="'+q.id+'" value="'+esc(v)+'">')+(q.h?'<span class="hint">'+esc(q.h)+'</span>':'')+'<span class="st" data-st="'+q.id+'"></span></div>'});
 h+='</section>';var ok=S.answers.ok_publish&&S.answers.ok_publish.v==='yes';
 h+='<section class="card '+(ok?'done':'')+'"><h2>'+(ok?'תודה! קיבלנו.':'כמעט סיימנו')+'</h2><p class="hint">'+(ok?'אפשר להוסיף עוד קבצים או לעדכן תשובות בכל זמן, באותו קישור.':'אחרי שהכול עלה, מסמנים למעלה את אישור הפרסום.')+'</p></section>';
 app.innerHTML=h;bind()}
function bind(){
 app.querySelectorAll('.sec input[type=file]').forEach(function(inp){inp.onchange=function(){var sec=inp.closest('.sec').dataset.s;upload(sec,Array.prototype.slice.call(inp.files));inp.value=''}});
 app.querySelectorAll('[data-del]').forEach(function(b){b.onclick=function(){var id=b.dataset.del;fetch(API+'/file/'+id,{method:'DELETE'}).then(function(){S.files=S.files.filter(function(f){return f.id!==id});render()})}});
 app.querySelectorAll('[data-q]').forEach(function(el){var t=0,id=el.dataset.q,st=app.querySelector('[data-st="'+id+'"]');
  var send=function(){var v=el.type==='checkbox'?(el.checked?'yes':''):el.value;st.textContent='שומרים…';
   fetch(API+'/answer',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id:id,value:v})}).then(function(r){st.textContent=r.ok?'נשמר':'לא נשמר, נסו שוב';if(r.ok){S.answers[id]={v:v};if(id==='ok_publish')render()}}).catch(function(){st.textContent='אין חיבור, נסו שוב'})};
  if(el.type==='checkbox')el.onchange=send;else{el.oninput=function(){clearTimeout(t);st.textContent='';t=setTimeout(send,900)};el.onblur=function(){clearTimeout(t);send()}}})}
function upload(sec,files){var box=app.querySelector('.sec[data-s="'+sec+'"] .files');
 var next=function(){if(!files.length){return}var f=files.shift(),li=document.createElement('li');li.className='busy';li.innerHTML=esc(f.name)+'<span class="bar" style="width:0"></span>';box.appendChild(li);
  var fd=new FormData();fd.append('section',sec);fd.append('file',f,f.name);var x=new XMLHttpRequest();x.open('POST',API+'/file');
  x.upload.onprogress=function(e){if(e.lengthComputable)li.querySelector('.bar').style.width=Math.round(e.loaded/e.total*100)+'%'};
  x.onload=function(){var j={};try{j=JSON.parse(x.responseText)}catch(e){}if(x.status<300&&j.file){S.files.push(j.file)}else{alert((j&&j.message)||'הקובץ לא עלה.')}render();next()};
  x.onerror=function(){li.innerHTML='לא עלה. נסו שוב';li.className='';next()};x.send(fd)};next()}
fetch(API+'/state').then(function(r){return r.json()}).then(function(j){S.answers=j.answers||{};S.files=j.files||[];render()}).catch(function(){app.innerHTML='<p class="card">אין חיבור כרגע. מרעננים את הדף.</p>'});
})();
NLBJS;
}
