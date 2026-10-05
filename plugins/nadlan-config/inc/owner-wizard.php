<?php
/**
 * nadlan-config · Owners publish on the same engine (x-owner-wizard) · v2.0.0 · 4.10.2026 (HAD-256)
 *
 * Owner order 23.9.2026: "the old wizard moves to the same engine": /post-listing/ keeps its address and its
 * account, and everything after it is the broker engine (x-broker-drop): a Latin address
 * (/properties/florentin-4-rooms-for-sale/), published at once, WhatsApp and call to the owner when the owner agrees.
 * The one hold left: a message that trips the fair-housing check (nadlan_compliance_scan) waits for a person.
 * "My listings" on the same page: sold or let in one tap, a new price in two (reg. 19(c) spirit for owners too).
 * Brokers who reach this page are sent to their own free site (/brokers/#join) instead.
 *
 * 2.0.0 (HAD-256, owner-approved design v5 "NadLan Listing Journey", Maya's contract L01-L17):
 *   - The listing journey: account (open, sign in, a recovery reply that never says whether an account exists) ->
 *     a saved draft to continue -> property details -> photos -> preview -> publish -> My listings
 *     (edit, price, sold or let, remove = trash, deleted drafts restored) -> promotion, switched off (no price,
 *     no checkout, no charge endpoint). Hebrew right to left first, English left to right (?lang=en).
 *   - The draft is a server entity owned by one user: a nadlan_drop with nl_draft_v=2 and ONE meta row nl_draft
 *     (rev, fields, photos, step, saved_at). Saving sends the revision it was based on; the server swaps the row
 *     only if it still holds that text (compare-and-swap in one UPDATE), else 409 with the server's version: no
 *     silent last-write-wins. Explicit fields; the street and house number are never asked and never published.
 *   - Photos are private until publish: each upload is cleaned of location and camera data
 *     (nl_drop_clean_image), kept outside the media library under uploads/nl-private/<keyed dir>/<128-bit ref>
 *     (deny-all .htaccess for Apache and LiteSpeed, or NL_OWNER_PRIVATE_DIR outside the web root), shown to its
 *     owner only through admin-ajax (nl_owner_img), and turned into media-library attachments at publish time.
 *     Per-file answers: 413 too big, 415 not an image / HEIC this server cannot clean, 422 corrupt, 429, 5xx.
 *   - Publish is idempotent: draft_id + a client request key; a retry returns the same result, the same key with
 *     another revision is refused. The build runs under x-broker-drop 1.1.4's lock with fencing tokens; a run that
 *     died after the listing row is finished by the next run (marker in the guid column), never written twice.
 *   - Quotas: abuse counters for attempts (saves, publish tries, photos), apart from unique publishes (8 a day,
 *     counted once per listing and only after the listing exists); a validation failure never costs a publish.
 *   - The phone is published only with the explicit consent box (unchecked by default). Without it the listing has
 *     no number, no WhatsApp and no call button (a wa.me link reveals the number too).
 *   - The 1.x doors: /owner/submit answers brokers as before and tells an old open page to refresh (410);
 *     /owner/build still builds a 1.x drop, under the lock; the plugin's first doors stay 410.
 * Needs x-broker-drop 1.1.4 (nl_drop_lock_acquire, nl_drop_clean_image). Installed as the persistent Code Snippet
 * "x-owner-wizard". Rollback: restore snippet 707's 1.0.0 text; 2.0 drafts stay as private nadlan_drop posts.
 */

if ( ! defined( 'ABSPATH' ) ) { return; }
if ( defined( 'NL_OWNER_VERSION' ) ) { return; }
define( 'NL_OWNER_VERSION', '2.0.0' );
define( 'NL_OWNER_MAX_ACTIVE', 5 );
define( 'NL_OWNER_MAX_DRAFTS', 10 );
define( 'NL_OWNER_PUB_DAY', 8 );
define( 'NL_OWNER_MAX_PHOTOS', 30 );

/* The shortcode and the REST doors are taken over after the plugin registered its own (plugins load before init). */
add_action( 'init', function () {
	if ( ! function_exists( 'nl_drop_build' ) ) { return; }
	remove_shortcode( 'nadlan_listing_wizard' );
	add_shortcode( 'nadlan_listing_wizard', 'nl_owner_shortcode' );
	remove_action( 'wp_enqueue_scripts', 'nadlan_pwiz_assets' );
}, 30 );

/** The engine this journey needs (x-broker-drop 1.1.4): the build lock and the photo cleaner. */
function nl_owner_engine_ok() {
	return function_exists( 'nl_drop_build' ) && function_exists( 'nl_drop_lock_acquire' ) && function_exists( 'nl_drop_clean_image' );
}

/** The owner as the engine's publisher: a name and a phone, no licence, no site, Hebrew only. */
function nl_owner_pseudo( $uid, $name, $phone ) {
	$digits = preg_replace( '/\D+/', '', (string) $phone );
	if ( $digits !== '' && $digits[0] === '0' ) { $digits = '972' . substr( $digits, 1 ); }
	$nat  = strpos( $digits, '972' ) === 0 ? substr( $digits, 3 ) : '';
	$intl = strlen( $nat ) >= 8 ? '+972 ' . substr( $nat, 0, 2 ) . '-' . substr( $nat, 2, 3 ) . '-' . substr( $nat, 5 ) : (string) $phone;
	$name = trim( (string) $name );
	return array(
		'id' => 0, 'kind' => 'owner', 'user_id' => (int) $uid,
		'name_he' => $name, 'name_en' => $name, 'name_ru' => $name, 'brand_he' => '', 'brand_en' => '', 'license' => '',
		'phone' => (string) $phone, 'phone_intl' => $intl, 'wa' => $digits, 'female' => false,
		'site_he' => 0, 'site_en' => 0, 'site_ru' => 0, 'site_fr' => 0, 'auto' => true, 'on' => true, 'token' => '',
		'areas' => array(), 'areas_l' => array(), 'bio' => array(), 'portrait' => '', 'hero' => 0, 'tier' => 'owner', 'slug' => '',
		'langs' => array( 'he' ),
	);
}

function nl_owner_from_listing( $pid ) {
	$c = json_decode( (string) get_post_meta( $pid, 'nl_owner_contact', true ), true );
	return nl_owner_pseudo( (int) get_post_meta( $pid, 'owner_user_id', true ), $c['name'] ?? '', $c['phone'] ?? '' );
}

/** An abuse counter: true when over the limit (counts the attempt). */
function nl_owner_rate( $uid, $bucket, $limit, $window ) {
	$k = 'nlowner_' . $bucket . '_' . (int) $uid;
	$n = (int) get_transient( $k );
	if ( $n >= $limit ) { return true; }
	set_transient( $k, $n + 1, $window );
	return false;
}

/** The same by a string identity (an address hash, an email hash): its own key, never cast to a number. */
function nl_owner_rate_key( $bucket, $ident, $limit, $window ) {
	$k = 'nlowner_' . $bucket . '_' . substr( md5( (string) $ident ), 0, 20 );
	$n = (int) get_transient( $k );
	if ( $n >= $limit ) { return true; }
	set_transient( $k, $n + 1, $window );
	return false;
}

/** By the caller's address, for the doors that work before an account exists. */
function nl_owner_rate_ip( $bucket, $limit, $window ) {
	$ip = preg_replace( '/[^0-9a-f\.\:]/i', '', (string) ( $_SERVER['REMOTE_ADDR'] ?? '' ) );
	return nl_owner_rate_key( 'ip_' . $bucket, 'ip|' . $ip, $limit, $window );
}

function nl_owner_phone( $raw ) {
	$d = preg_replace( '/\D+/', '', (string) $raw );
	if ( strpos( $d, '972' ) === 0 ) { $d = '0' . substr( $d, 3 ); }
	return preg_match( '/^05\d{8}$/', $d ) ? substr( $d, 0, 3 ) . '-' . substr( $d, 3 ) : '';
}

function nl_owner_listings( $uid, $only_ids = false, $with_trash = false ) {
	$st = array( 'publish', 'draft', 'pending' );
	if ( $with_trash ) { $st[] = 'trash'; }
	return get_posts( array(
		'post_type'        => 'nadlan_property',
		'post_status'      => $st,
		'numberposts'      => 50,
		'orderby'          => 'date',
		'order'            => 'DESC',
		'suppress_filters' => true,
		'fields'           => $only_ids ? 'ids' : 'all',
		'meta_query'       => array(
			array( 'key' => 'owner_user_id', 'value' => (int) $uid, 'type' => 'NUMERIC' ),
			array( 'key' => 'nl_owner', 'value' => '1' ),
		),
	) );
}

function nl_owner_active_count( $uid ) {
	$n = 0;
	foreach ( nl_owner_listings( $uid ) as $p ) {
		if ( $p->post_status === 'publish' && (string) get_post_meta( $p->ID, 'nl_status', true ) === 'active' ) { $n++; }
	}
	return $n;
}

/* =====================================================================================================
 * Words the server says, in the visitor's language
 * ===================================================================================================== */
function nl_owner_lang( $l ) {
	return 'en' === (string) $l ? 'en' : 'he';
}

function nl_owner_t( $k, $lang = 'he' ) {
	static $T = array(
		'he' => array(
			'nf'          => 'לא נמצא.',
			'rate'        => 'יותר מדי פעולות בזמן קצר. מה שכתבתם שמור; נסו שוב בעוד כמה דקות.',
			'conflict'    => 'הטיוטה השתנתה בלשונית אחרת.',
			'publishing'  => 'המודעה בפרסום כרגע. בודקים שוב בעוד רגע.',
			'drafts_max'  => 'יש לכם כבר 10 טיוטות פתוחות. ממשיכים אחת מהן מהמודעות שלי, או מוחקים טיוטה.',
			'key'         => 'מזהה הבקשה חסר. מרעננים את העמוד.',
			'key_reused'  => 'הבקשה הזו כבר נשלחה עם תוכן אחר. פותחים שוב את התצוגה המקדימה ושולחים משם.',
			'changed'     => 'הטיוטה השתנתה מאז התצוגה המקדימה. בודקים אותה שוב לפני הפרסום.',
			'invalid'     => 'יש פרטים לתיקון לפני הפרסום.',
			'cap'         => 'יש לכם כבר 5 מודעות פעילות. מודעה שנמכרה או הושכרה מסמנים במודעות שלי, והמקום מתפנה.',
			'quota'       => 'הגעתם למכסת הפרסומים היומית. הטיוטה שמורה, ואפשר לפרסם מחר.',
			'engine'      => 'הפרסום לא זמין כרגע. הטיוטה שמורה.',
			'build'       => 'בניית העמוד לא הושלמה. הטיוטה שמורה, ואפשר לנסות שוב.',
			'building'    => 'המודעה בבנייה. בודקים שוב בעוד כמה שניות.',
			'moved'       => 'הטופס עודכן. מרעננים את העמוד ושולחים שוב.',
			'not_draft'   => 'את המודעה הזו מסירים מהאתר דרך המודעות שלי.',
			'gone'        => 'הטיוטה לא נמצאת. ייתכן שנמחקה בלשונית אחרת.',
			'del_failed'  => 'המחיקה לא הושלמה. הטיוטה נשארה כמו שהיא.',
			'nofile'      => 'לא התקבל קובץ.',
			'need_draft'  => 'קודם שומרים את פרטי הנכס, ואז מוסיפים תמונות.',
			'big'         => 'התמונה גדולה מ-15 מ״ב.',
			'type'        => 'הקובץ אינו תמונה שאפשר להעלות: JPG, PNG, WebP או HEIC.',
			'heic'        => 'את קובץ ה-HEIC הזה אי אפשר לנקות כאן מנתוני המיקום. שומרים אותו כ-JPG ומעלים שוב.',
			'corrupt'     => 'הקובץ פגום ולא נפתח כתמונה.',
			'orient'      => 'התמונה שמורה מסובבת, והשרת לא יכול להחזיר אותה ליושר. שומרים אותה מחדש בטלפון או במחשב ומעלים שוב.',
			'upload'      => 'ההעלאה נכשלה בשרת. אפשר לנסות שוב.',
			'photos_max'  => 'אפשר עד 30 תמונות למודעה.',
			'acc_name'    => 'כותבים שם פרטי.',
			'acc_email'   => 'כותבים כתובת מייל תקינה.',
			'acc_pw'      => 'סיסמה של 8 תווים לפחות, שאינה נפוצה.',
			'acc_exists'  => 'המייל הזה כבר רשום אצלנו. השם והמייל שכתבתם נשמרו בטופס.',
			'acc_closed'  => 'פתיחת חשבונות סגורה כרגע.',
			'acc_rate'    => 'יותר מדי ניסיונות מהכתובת הזו. נסו שוב בעוד שעה.',
			'acc_wrong'   => 'המייל או הסיסמה אינם נכונים. מה שכתבתם נשמר בטופס.',
			'acc_locked'  => 'הכניסה נעולה זמנית אחרי כמה ניסיונות. נסו שוב בעוד 15 דקות.',
			'rec_sent'    => 'אם המייל רשום אצלנו, הקישור בדרך.',
			'rec_back'    => 'אחרי בחירת הסיסמה חוזרים לטיוטה כאן:',
			'f_deal'      => 'בוחרים מכירה או השכרה.',
			'f_ptype'     => 'בוחרים את סוג הנכס.',
			'f_city'      => 'כותבים את העיר.',
			'f_hood'      => 'כותבים את השכונה.',
			'f_place_num' => 'עיר ושכונה בלבד, בלי מספר בית.',
			'f_rooms'     => 'מספר חדרים בין 1 ל-20, אפשר חצי (3.5).',
			'f_size'      => 'שטח במ״ר, בספרות, בין 10 ל-2,000.',
			'f_floor'     => 'קומה בספרות, למשל 3 או 3 מתוך 8. אפשר להשאיר ריק.',
			'f_price_s'   => 'מחיר בספרות בלבד, בין 100,000 ל-500,000,000 ₪.',
			'f_price_r'   => 'שכר דירה לחודש בספרות, בין 500 ל-200,000 ₪.',
			'f_desc'      => 'כותבים כמה מילים על הנכס, לפחות 20 תווים.',
			'f_desc_st'   => 'נראה שבתיאור יש שם רחוב ומספר. הרחוב ומספר הבית לא מתפרסמים, אז מוחקים אותם מהתיאור.',
			'f_desc_ct'   => 'טלפון, מייל או קישור לא נכתבים בתיאור. פרטי הקשר מופיעים רק לפי הבחירה למטה.',
			'f_cname'     => 'כותבים שם להצגה, בלי ספרות וקישורים.',
			'f_phone'     => 'המספר לא נראה כמו נייד ישראלי. בדקו את הספרות. כל השאר שכתבתם נשמר.',
			'f_phone_req' => 'כדי לפרסם את המספר צריך נייד ישראלי, לדוגמה 050-0000000.',
			'f_owner'     => 'מסמנים את הצהרת הבעלות לפני הפרסום.',
			'f_photos'    => 'מוסיפים לפחות תמונה אחת.',
			'draft_title' => 'טיוטה',
			'mail_hold'   => '[nad-lan] מודעת בעלים ממתינה לבדיקה',
			'mail_hold_b' => 'הטקסט נעצר בבדיקת הפליה בדיור: ',
			'month'       => 'לחודש',
			'rooms_n'     => '%s חדרים',
			'size_n'      => '%s מ״ר',
			'floor_of'    => 'קומה %1$s מתוך %2$s',
			'floor_n'     => 'קומה %s',
			'ground'      => 'קומת קרקע',
			'sale'        => 'למכירה',
			'rent'        => 'להשכרה',
		),
		'en' => array(
			'nf'          => 'Not found.',
			'rate'        => 'Too many actions in a short time. What you wrote is kept; try again in a few minutes.',
			'conflict'    => 'The draft changed in another tab.',
			'publishing'  => 'The listing is being published right now. Checking again in a moment.',
			'drafts_max'  => 'You already have 10 open drafts. Continue one of them from My listings, or delete a draft.',
			'key'         => 'The request key is missing. Refresh the page.',
			'key_reused'  => 'This request was already sent with other content. Open the preview again and publish from there.',
			'changed'     => 'The draft changed since the preview. Check it again before publishing.',
			'invalid'     => 'Some details need fixing before publishing.',
			'cap'         => 'You already have 5 active listings. Mark a sold or rented one in My listings to free a place.',
			'quota'       => 'You reached today\'s publishing limit. The draft is saved; you can publish tomorrow.',
			'engine'      => 'Publishing is not available right now. The draft is saved.',
			'build'       => 'The page was not finished. The draft is saved; you can try again.',
			'building'    => 'The listing is being built. Checking again in a few seconds.',
			'moved'       => 'The form was updated. Refresh the page and send again.',
			'not_draft'   => 'Remove this listing from the site through My listings.',
			'gone'        => 'The draft is not there. It may have been deleted in another tab.',
			'del_failed'  => 'The deletion did not finish. The draft stays as it was.',
			'nofile'      => 'No file arrived.',
			'need_draft'  => 'Save the property details first, then add photos.',
			'big'         => 'The photo is larger than 15 MB.',
			'type'        => 'This file is not a photo we can take: JPG, PNG, WebP or HEIC.',
			'heic'        => 'This HEIC file cannot be cleaned of its location data here. Save it as JPG and upload again.',
			'corrupt'     => 'The file is damaged and does not open as a photo.',
			'orient'      => 'The photo is stored turned, and the server cannot set it upright. Save it again on your phone or computer and upload it again.',
			'upload'      => 'The upload failed on the server. You can try again.',
			'photos_max'  => 'Up to 30 photos per listing.',
			'acc_name'    => 'Type your first name.',
			'acc_email'   => 'Type a valid email address.',
			'acc_pw'      => 'A password of at least 8 characters that is not a common one.',
			'acc_exists'  => 'This email already has an account. The name and email you typed are kept in the form.',
			'acc_closed'  => 'Opening accounts is closed right now.',
			'acc_rate'    => 'Too many attempts from this address. Try again in an hour.',
			'acc_wrong'   => 'The email or the password is not right. What you typed is kept in the form.',
			'acc_locked'  => 'Signing in is locked for a while after several attempts. Try again in 15 minutes.',
			'rec_sent'    => 'If the email is registered, the link is on its way.',
			'rec_back'    => 'After you choose the password, return to your draft here:',
			'f_deal'      => 'Choose for sale or for rent.',
			'f_ptype'     => 'Choose the property type.',
			'f_city'      => 'Type the city.',
			'f_hood'      => 'Type the neighbourhood.',
			'f_place_num' => 'City and neighbourhood only, without a house number.',
			'f_rooms'     => 'Rooms between 1 and 20; halves are fine (3.5).',
			'f_size'      => 'Size in m², in digits, between 10 and 2,000.',
			'f_floor'     => 'Floor in digits, for example 3 or 3 of 8. You can leave it empty.',
			'f_price_s'   => 'Price in digits only, between 100,000 and 500,000,000 ₪.',
			'f_price_r'   => 'Monthly rent in digits, between 500 and 200,000 ₪.',
			'f_desc'      => 'Write a few words about the property, at least 20 characters.',
			'f_desc_st'   => 'The description seems to hold a street and number. The street and house number are never published, so take them out.',
			'f_desc_ct'   => 'No phone, email or link in the description. Contact details show only as you choose below.',
			'f_cname'     => 'Type a display name, without digits or links.',
			'f_phone'     => 'This does not look like an Israeli mobile number. Check the digits. Everything else you typed is kept.',
			'f_phone_req' => 'To publish the number we need an Israeli mobile, for example 050-0000000.',
			'f_owner'     => 'Tick the ownership statement before publishing.',
			'f_photos'    => 'Add at least one photo.',
			'draft_title' => 'Draft',
			'mail_hold'   => '[nad-lan] An owner listing waits for review',
			'mail_hold_b' => 'The text stopped at the fair-housing check: ',
			'month'       => 'a month',
			'rooms_n'     => '%s rooms',
			'size_n'      => '%s m²',
			'floor_of'    => 'Floor %1$s of %2$s',
			'floor_n'     => 'Floor %s',
			'ground'      => 'Ground floor',
			'sale'        => 'For sale',
			'rent'        => 'For rent',
		),
	);
	$lang = nl_owner_lang( $lang );
	return $T[ $lang ][ $k ] ?? ( $T['he'][ $k ] ?? $k );
}

function nl_owner_err( $code, $status, $lang, $extra = array() ) {
	return new WP_Error( $code, nl_owner_t( $code, $lang ), array_merge( array( 'status' => $status ), $extra ) );
}

/* =====================================================================================================
 * The draft: explicit fields, one row with its revision
 * ===================================================================================================== */
function nl_owner_fields_empty() {
	return array( 'deal' => '', 'ptype' => '', 'city' => '', 'hood' => '', 'rooms' => '', 'size' => '', 'floor' => '', 'price' => '', 'desc' => '', 'cname' => '', 'phone' => '', 'phone_ok' => false, 'owner_ok' => false );
}

function nl_owner_cut( $s, $max ) {
	return function_exists( 'mb_substr' ) ? mb_substr( (string) $s, 0, $max ) : substr( (string) $s, 0, $max );
}

function nl_owner_len( $s ) {
	return function_exists( 'mb_strlen' ) ? mb_strlen( (string) $s ) : strlen( (string) $s );
}

function nl_owner_fields_clean( $in ) {
	$in  = is_array( $in ) ? $in : array();
	$out = nl_owner_fields_empty();
	$s   = function ( $v, $max ) { return nl_owner_cut( trim( sanitize_text_field( is_scalar( $v ) ? (string) $v : '' ) ), $max ); };
	$out['deal']     = in_array( $in['deal'] ?? '', array( 'sale', 'rent' ), true ) ? $in['deal'] : '';
	$out['ptype']    = in_array( $in['ptype'] ?? '', array( 'apartment', 'garden', 'penthouse', 'duplex', 'house' ), true ) ? $in['ptype'] : '';
	$out['city']     = $s( $in['city'] ?? '', 40 );
	$out['hood']     = $s( $in['hood'] ?? '', 40 );
	$out['rooms']    = $s( $in['rooms'] ?? '', 6 );
	$out['size']     = $s( $in['size'] ?? '', 8 );
	$out['floor']    = $s( $in['floor'] ?? '', 20 );
	$out['price']    = $s( $in['price'] ?? '', 16 );
	$out['desc']     = nl_owner_cut( trim( sanitize_textarea_field( is_scalar( $in['desc'] ?? '' ) ? (string) $in['desc'] : '' ) ), 1500 );
	$out['cname']    = $s( $in['cname'] ?? '', 30 );
	$out['phone']    = $s( $in['phone'] ?? '', 20 );
	$out['phone_ok'] = ! empty( $in['phone_ok'] ) && $in['phone_ok'] !== 'false';
	$out['owner_ok'] = ! empty( $in['owner_ok'] ) && $in['owner_ok'] !== 'false';
	return $out;
}

/** The meta row as stored, read past every cache. */
function nl_owner_draft_raw( $id ) {
	global $wpdb;
	return $wpdb->get_var( $wpdb->prepare( "SELECT meta_value FROM {$wpdb->postmeta} WHERE post_id = %d AND meta_key = 'nl_draft' ORDER BY meta_id ASC LIMIT 1", (int) $id ) );
}

/** The draft of this user, or null (null also for another user's draft: the answer never says it exists). */
function nl_owner_draft_get( $id, $uid, $with_trash = false ) {
	$id  = (int) $id;
	$uid = (int) $uid;
	if ( $id <= 0 || $uid <= 0 ) { return null; }
	clean_post_cache( $id );
	$p = get_post( $id );
	if ( ! $p || $p->post_type !== 'nadlan_drop' ) { return null; }
	if ( (string) get_post_meta( $id, 'nl_owner_user', true ) !== (string) $uid ) { return null; }
	if ( (string) get_post_meta( $id, 'nl_draft_v', true ) !== '2' ) { return null; }
	if ( $p->post_status === 'trash' && ! $with_trash ) { return null; }
	$raw = nl_owner_draft_raw( $id );
	$d   = json_decode( (string) $raw, true );
	if ( ! is_array( $d ) ) { return null; }
	$d['id']     = $id;
	$d['_raw']   = (string) $raw;
	$d['_post']  = $p;
	$d['fields'] = array_merge( nl_owner_fields_empty(), is_array( $d['fields'] ?? null ) ? $d['fields'] : array() );
	$d['photos'] = is_array( $d['photos'] ?? null ) ? $d['photos'] : array();
	return $d;
}

/** Swap the row only if it still holds the text the caller read: one UPDATE, one winner. */
function nl_owner_draft_cas( $id, $old_raw, $new ) {
	global $wpdb;
	$json = wp_json_encode( $new, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES );
	$n    = $wpdb->query( $wpdb->prepare( "UPDATE {$wpdb->postmeta} SET meta_value = %s WHERE post_id = %d AND meta_key = 'nl_draft' AND meta_value = %s", $json, (int) $id, (string) $old_raw ) );
	wp_cache_delete( (int) $id, 'post_meta' );
	return 1 === (int) $n;
}

function nl_owner_draft_state( $id ) {
	$st = (string) get_post_meta( (int) $id, 'nl_state', true );
	return $st === '' ? 'editing' : $st;
}

/** True while a publish run holds the drop's lock (a run that died does not count after the TTL). */
function nl_owner_publishing( $id ) {
	if ( ! function_exists( 'nl_drop_lock_read' ) ) { return false; }
	$l = nl_drop_lock_read( $id );
	return $l && time() - $l['t'] < nl_drop_lock_ttl();
}

/* ---------------- photos: private until publish, sealed at rest ----------------
 * A draft photo is kept only as ciphertext (libsodium secretbox, or AES-256-GCM when sodium is missing), with a key
 * derived from this site's own secret (wp_salt 'auth'). Whatever the web server does with the folder (LiteSpeed,
 * Apache, nginx, PHP's built-in server), a direct request for the stored file gets bytes that are not an image and
 * cannot be opened without the site's secret. The owner sees the photo only through nl_owner_img, which checks the
 * account. No cipher available = no upload (fail closed). NL_OWNER_PRIVATE_DIR moves the folder out of the web root
 * where the host allows it. Rotating the auth salt makes unpublished draft photos unreadable (published ones are
 * ordinary media files by then). */
function nl_owner_crypto_ok() {
	return function_exists( 'sodium_crypto_secretbox' ) || ( function_exists( 'openssl_encrypt' ) && in_array( 'aes-256-gcm', (array) openssl_get_cipher_methods(), true ) );
}

function nl_owner_key() {
	return hash( 'sha256', 'nl-owner-photos|' . wp_salt( 'auth' ), true );
}

function nl_owner_seal( $bin ) {
	$key = nl_owner_key();
	if ( function_exists( 'sodium_crypto_secretbox' ) ) {
		$n = random_bytes( 24 );
		return 'NLS1' . $n . sodium_crypto_secretbox( $bin, $n, $key );
	}
	$iv  = random_bytes( 12 );
	$tag = '';
	$c   = openssl_encrypt( $bin, 'aes-256-gcm', $key, OPENSSL_RAW_DATA, $iv, $tag );
	return $c === false ? false : 'NLG1' . $iv . $tag . $c;
}

function nl_owner_unseal( $box ) {
	$box = (string) $box;
	$key = nl_owner_key();
	if ( substr( $box, 0, 4 ) === 'NLS1' && function_exists( 'sodium_crypto_secretbox_open' ) ) {
		$r = sodium_crypto_secretbox_open( substr( $box, 28 ), substr( $box, 4, 24 ), $key );
		return $r === false ? false : $r;
	}
	if ( substr( $box, 0, 4 ) === 'NLG1' && function_exists( 'openssl_decrypt' ) ) {
		return openssl_decrypt( substr( $box, 32 ), 'aes-256-gcm', $key, OPENSSL_RAW_DATA, substr( $box, 4, 12 ), substr( $box, 16, 16 ) );
	}
	return false;
}

/* ---------------- photos: private until publish ---------------- */
function nl_owner_private_base() {
	if ( defined( 'NL_OWNER_PRIVATE_DIR' ) && NL_OWNER_PRIVATE_DIR ) { return untrailingslashit( NL_OWNER_PRIVATE_DIR ); }
	$u = wp_upload_dir( null, false );
	return untrailingslashit( $u['basedir'] ) . '/nl-private';
}

function nl_owner_private_dir( $uid ) {
	$base = nl_owner_private_base();
	$dir  = $base . '/' . substr( hash_hmac( 'sha256', 'owner-' . (int) $uid, wp_salt( 'auth' ) ), 0, 32 );
	if ( ! is_dir( $dir ) ) { wp_mkdir_p( $dir ); }
	if ( ! file_exists( $base . '/.htaccess' ) ) {
		@file_put_contents( $base . '/.htaccess', "# HAD-256: owners' draft photos are private until publish\n<IfModule mod_authz_core.c>\nRequire all denied\n</IfModule>\n<IfModule !mod_authz_core.c>\nOrder allow,deny\nDeny from all\n</IfModule>\n" );
	}
	foreach ( array( $base, $dir ) as $d ) {
		if ( ! file_exists( $d . '/index.php' ) ) { @file_put_contents( $d . '/index.php', "<?php\n// Silence is golden.\n" ); }
	}
	return $dir;
}

/** The uploads recorded on a draft: ref => array( ref, ext, type, w, h, t ). */
function nl_owner_uploads( $id ) {
	global $wpdb;
	$rows = $wpdb->get_col( $wpdb->prepare( "SELECT meta_value FROM {$wpdb->postmeta} WHERE post_id = %d AND meta_key = 'nl_upload' ORDER BY meta_id ASC", (int) $id ) );
	$out  = array();
	foreach ( (array) $rows as $r ) {
		$j = json_decode( (string) $r, true );
		if ( is_array( $j ) && ! empty( $j['ref'] ) && preg_match( '/^[a-f0-9]{32}$/', (string) $j['ref'] ) ) { $out[ $j['ref'] ] = $j; }
	}
	return $out;
}

function nl_owner_upload_forget( $id, $uid, $ref ) {
	$ups = nl_owner_uploads( $id );
	if ( empty( $ups[ $ref ] ) ) { return; }
	$dir = nl_owner_private_dir( $uid );
	@unlink( $dir . '/' . $ref . '.bin' );
	@unlink( $dir . '/' . $ref . '-t.bin' );
	global $wpdb;
	$wpdb->query( $wpdb->prepare( "DELETE FROM {$wpdb->postmeta} WHERE post_id = %d AND meta_key = 'nl_upload' AND meta_value LIKE %s", (int) $id, '%' . $wpdb->esc_like( '"ref":"' . $ref . '"' ) . '%' ) );
	wp_cache_delete( (int) $id, 'post_meta' );
}

function nl_owner_img_url( $id, $ref, $size ) {
	return add_query_arg( array( 'action' => 'nl_owner_img', 'd' => (int) $id, 'r' => $ref, 's' => $size === 'f' ? 'f' : 't' ), admin_url( 'admin-ajax.php' ) );
}

/** A photo entry of a draft as the screen gets it: the owner-only proxy before publish, the public file after. */
function nl_owner_photo_out( $id, $p, $ups ) {
	$ref = (string) ( $p['ref'] ?? '' );
	$att = (int) ( $p['att'] ?? 0 );
	if ( $att && get_post_type( $att ) === 'attachment' ) {
		$m = wp_get_attachment_metadata( $att );
		$t = wp_get_attachment_image_url( $att, 'medium_large' );
		return array( 'ref' => $ref, 'att' => $att, 'thumb' => (string) ( $t ?: wp_get_attachment_url( $att ) ), 'full' => (string) wp_get_attachment_url( $att ), 'w' => (int) ( $m['width'] ?? 0 ), 'h' => (int) ( $m['height'] ?? 0 ) );
	}
	if ( $ref === '' || empty( $ups[ $ref ] ) ) { return null; }
	return array( 'ref' => $ref, 'att' => 0, 'thumb' => nl_owner_img_url( $id, $ref, 't' ), 'full' => nl_owner_img_url( $id, $ref, 'f' ), 'w' => (int) $ups[ $ref ]['w'], 'h' => (int) $ups[ $ref ]['h'] );
}

/* ---------------- facts, copy and the preview: one function for the preview and the page ---------------- */
function nl_owner_city_en( $city ) {
	$c = trim( (string) $city );
	if ( $c === '' ) { return ''; }
	if ( ! preg_match( '/\p{Hebrew}/u', $c ) ) { return $c; }
	static $map = array(
		'תל אביב' => 'Tel Aviv-Yafo', 'תל אביב יפו' => 'Tel Aviv-Yafo', 'תל אביב-יפו' => 'Tel Aviv-Yafo', 'יפו' => 'Tel Aviv-Yafo',
		'ירושלים' => 'Jerusalem', 'חיפה' => 'Haifa', 'רמת גן' => 'Ramat Gan', 'גבעתיים' => 'Givatayim', 'הרצליה' => 'Herzliya',
		'רעננה' => 'Raanana', 'כפר סבא' => 'Kfar Saba', 'הוד השרון' => 'Hod Hasharon', 'רמת השרון' => 'Ramat Hasharon',
		'פתח תקווה' => 'Petah Tikva', 'פתח תקוה' => 'Petah Tikva', 'ראשון לציון' => 'Rishon LeZion', 'חולון' => 'Holon', 'בת ים' => 'Bat Yam',
		'נתניה' => 'Netanya', 'רחובות' => 'Rehovot', 'נס ציונה' => 'Ness Ziona', 'אשדוד' => 'Ashdod', 'אשקלון' => 'Ashkelon',
		'באר שבע' => 'Beer Sheva', 'מודיעין' => 'Modiin', 'מודיעין מכבים רעות' => 'Modiin', 'בני ברק' => 'Bnei Brak', 'גבעת שמואל' => 'Givat Shmuel',
		'קריית אונו' => 'Kiryat Ono', 'קרית אונו' => 'Kiryat Ono', 'יהוד' => 'Yehud', 'אור יהודה' => 'Or Yehuda', 'לוד' => 'Lod', 'רמלה' => 'Ramla',
		'חדרה' => 'Hadera', 'כפר יונה' => 'Kfar Yona', 'אילת' => 'Eilat', 'טבריה' => 'Tiberias', 'נהריה' => 'Nahariya', 'עכו' => 'Akko',
		'כרמיאל' => 'Karmiel', 'עפולה' => 'Afula', 'נצרת' => 'Nazareth', 'קיסריה' => 'Caesarea', 'זכרון יעקב' => 'Zichron Yaakov',
		'אופקים' => 'Ofakim', 'שדרות' => 'Sderot', 'בית שמש' => 'Beit Shemesh', 'מעלה אדומים' => 'Maale Adumim', 'אריאל' => 'Ariel',
		'ראש העין' => 'Rosh HaAyin', 'יבנה' => 'Yavne', 'גדרה' => 'Gedera', 'קריית גת' => 'Kiryat Gat', 'דימונה' => 'Dimona',
	);
	$k = trim( preg_replace( '/\s+/u', ' ', str_replace( array( '־', '–' ), array( ' ', '-' ), $c ) ) );
	return $map[ $k ] ?? ( $map[ str_replace( '-', ' ', $k ) ] ?? '' );
}

function nl_owner_num( $s ) {
	$s = str_replace( array( ',', ' ', '₪', "\u{00A0}" ), '', trim( (string) $s ) );
	$s = str_replace( '٫', '.', $s );
	return preg_match( '/^\d+(?:\.\d+)?$/', $s ) ? (float) $s : null;
}

/** "3", "3 מתוך 8", "3/8", "3 of 8", "קרקע", "ground" -> array( floor, total ) ; array( null, null ) when empty; false when unreadable. */
function nl_owner_floor( $s ) {
	$s = trim( (string) $s );
	if ( $s === '' ) { return array( null, null ); }
	if ( preg_match( '/^(?:קרקע|קומת קרקע|ground(?: floor)?)$/iu', $s ) ) { return array( 0, null ); }
	if ( preg_match( '/^(-?\d{1,3})\s*(?:(?:מתוך|of|\/|מ-|מ)\s*(\d{1,3}))?$/iu', $s, $m ) ) {
		$fl = (int) $m[1];
		$to = isset( $m[2] ) && $m[2] !== '' ? (int) $m[2] : null;
		if ( $fl < -3 || $fl > 120 || ( $to !== null && ( $to < 1 || $to > 120 || $to < $fl ) ) ) { return false; }
		return array( $fl, $to );
	}
	return false;
}

function nl_owner_facts( $fl ) {
	$floor  = nl_owner_floor( $fl['floor'] );
	if ( $floor === false ) { $floor = array( null, null ); }
	$ptmap  = array( 'apartment' => 'apartment', 'garden' => 'garden', 'penthouse' => 'penthouse', 'duplex' => 'duplex', 'house' => 'cottage' );
	$rooms  = nl_owner_num( str_replace( ',', '.', $fl['rooms'] ) );
	$size   = nl_owner_num( $fl['size'] );
	$price  = nl_owner_num( preg_replace( '/[^\d]/', '', (string) $fl['price'] ) );
	$city   = trim( (string) $fl['city'] );
	$hood   = trim( (string) $fl['hood'] );
	return array(
		'listing_type'  => $fl['deal'] !== '' ? $fl['deal'] : null,
		'property_type' => $ptmap[ $fl['ptype'] ] ?? 'apartment',
		'exclusive'     => false,
		'city_he'       => $city !== '' ? $city : null,
		'city_en'       => nl_owner_city_en( $city ) !== '' ? nl_owner_city_en( $city ) : null,
		'area_he'       => $hood !== '' ? $hood : null,
		'area_en'       => null,
		'street_he'     => null, 'street_en' => null,
		'rooms'         => $rooms ? $rooms : null,
		'size_sqm'      => $size ? (int) round( $size ) : null,
		'balcony_sqm'   => null, 'garden_sqm' => null,
		'floor'         => $floor[0], 'total_floors' => $floor[1],
		'price'         => $price ? (int) $price : null,
		'parking_count' => null, 'parking' => null, 'storage' => null, 'elevator' => null, 'protected_room' => null, 'ac' => null, 'furnished' => null,
		'condition'     => null, 'entry_he' => null, 'entry_en' => null, 'view_he' => null, 'view_en' => null,
		'features_he'   => array(), 'features_en' => array(), 'notes_he' => null, 'notes_en' => null,
	);
}

function nl_owner_title_he( $f ) {
	$rooms = ! empty( $f['rooms'] ) ? nl_drop_fmt_num( $f['rooms'] ) : '';
	$type  = (string) ( $f['property_type'] ?? '' );
	$plain = in_array( $type, array( '', 'apartment', 'other' ), true );
	if ( $rooms !== '' ) { $head = $plain ? 'דירת ' . $rooms . ' חדרים' : nl_drop_type_label( $type, 'he' ) . ' ' . $rooms . ' חדרים'; }
	else { $head = nl_drop_type_label( $type !== '' ? $type : 'apartment', 'he' ); }
	$area = (string) ( $f['area_he'] ?: ( $f['city_he'] ?: '' ) );
	return $area !== '' ? $head . ' ' . nl_drop_he_in( $area ) : $head;
}

/** The description in the owner's own words, in paragraphs. */
function nl_owner_paras( $desc ) {
	$desc  = str_replace( "\r", '', (string) $desc );
	$parts = preg_split( '/\n\s*\n/u', $desc );
	if ( count( $parts ) < 2 ) { $parts = explode( "\n", $desc ); }
	return array_slice( array_values( array_filter( array_map( 'trim', $parts ), 'strlen' ) ), 0, 8 );
}

/** The page copy: the engine's plain template, the owner's title, and the owner's own description as the story. */
function nl_owner_copy( $f, $desc ) {
	$c               = nl_drop_tpl( $f, 'he' );
	$c['title']      = nl_owner_title_he( $f );
	$c['card_title'] = $c['title'];
	$paras           = nl_owner_paras( $desc );
	if ( $paras ) { $c['story'] = $paras; }
	return array( 'he' => $c );
}

function nl_owner_b( $uid, $fl ) {
	$phone = ! empty( $fl['phone_ok'] ) ? nl_owner_phone( $fl['phone'] ) : '';
	return nl_owner_pseudo( $uid, $fl['cname'], $phone );
}

/* ---------------- readiness: the same rules on the details step, the preview and the publish ---------------- */
function nl_owner_desc_street( $s ) {
	return (bool) preg_match( '/(?:^|[\s,.(])(?:ב?רחוב|ברח[\'׳’]?|רח[\'׳’]|שד[\'׳’]|ב?שדרות|ב?סמטת|ב?דרך|street|st\.|avenue|ave\.|road|rd\.|blvd\.?)\s+[\p{L}"״\'׳\- ]{2,30}?\s+\d{1,4}(?!\s*(?:חד|מ״ר|מ"ר|מטר|קומ|שנ|דק|rooms?|sqm|m²|floor|years?|min))/iu', (string) $s );
}

function nl_owner_desc_contact( $s ) {
	$s = (string) $s;
	if ( preg_match( '/(?:\+?972|\b0)[\s\-]?(?:5\d|[2-489])(?:[\s\-]?\d){7}\b/u', $s ) ) { return true; }
	if ( preg_match( '/[^\s@]+@[^\s@]+\.[^\s@]+/u', $s ) ) { return true; }
	return (bool) preg_match( '#https?://|www\.|wa\.me#i', $s );
}

/** Field => message for everything that stops a publish. $only limits the check to some fields (the details step). */
function nl_owner_check( $d, $lang, $only = null ) {
	$fl = $d['fields'];
	$e  = array();
	if ( $fl['deal'] === '' ) { $e['deal'] = nl_owner_t( 'f_deal', $lang ); }
	if ( $fl['ptype'] === '' ) { $e['ptype'] = nl_owner_t( 'f_ptype', $lang ); }
	if ( trim( $fl['city'] ) === '' ) { $e['city'] = nl_owner_t( 'f_city', $lang ); }
	elseif ( preg_match( '/\d/', $fl['city'] ) ) { $e['city'] = nl_owner_t( 'f_place_num', $lang ); }
	if ( trim( $fl['hood'] ) === '' ) { $e['hood'] = nl_owner_t( 'f_hood', $lang ); }
	elseif ( preg_match( '/\d/', $fl['hood'] ) ) { $e['hood'] = nl_owner_t( 'f_place_num', $lang ); }
	$rooms = nl_owner_num( str_replace( ',', '.', $fl['rooms'] ) );
	if ( $rooms === null || $rooms < 1 || $rooms > 20 || fmod( $rooms * 2, 1 ) != 0 ) { $e['rooms'] = nl_owner_t( 'f_rooms', $lang ); }
	$size = nl_owner_num( $fl['size'] );
	if ( $size === null || $size < 10 || $size > 2000 ) { $e['size'] = nl_owner_t( 'f_size', $lang ); }
	if ( nl_owner_floor( $fl['floor'] ) === false ) { $e['floor'] = nl_owner_t( 'f_floor', $lang ); }
	$pdig  = preg_replace( '/[\s,₪\x{00A0}]/u', '', (string) $fl['price'] );
	$price = preg_match( '/^\d+$/', $pdig ) ? (int) $pdig : 0;
	if ( $fl['deal'] === 'rent' ) {
		if ( $price < 500 || $price > 200000 ) { $e['price'] = nl_owner_t( 'f_price_r', $lang ); }
	} elseif ( $price < 100000 || $price > 500000000 ) {
		$e['price'] = nl_owner_t( 'f_price_s', $lang );
	}
	if ( nl_owner_len( trim( $fl['desc'] ) ) < 20 ) { $e['desc'] = nl_owner_t( 'f_desc', $lang ); }
	elseif ( nl_owner_desc_street( $fl['desc'] ) ) { $e['desc'] = nl_owner_t( 'f_desc_st', $lang ); }
	elseif ( nl_owner_desc_contact( $fl['desc'] ) ) { $e['desc'] = nl_owner_t( 'f_desc_ct', $lang ); }
	$name = trim( $fl['cname'] );
	if ( $name === '' || preg_match( '/https?:|www\.|@|\d/u', $name ) ) { $e['cname'] = nl_owner_t( 'f_cname', $lang ); }
	if ( $fl['phone_ok'] && nl_owner_phone( $fl['phone'] ) === '' ) { $e['phone'] = nl_owner_t( 'f_phone_req', $lang ); }
	elseif ( trim( $fl['phone'] ) !== '' && nl_owner_phone( $fl['phone'] ) === '' ) { $e['phone'] = nl_owner_t( 'f_phone', $lang ); }
	if ( ! $fl['owner_ok'] ) { $e['owner_ok'] = nl_owner_t( 'f_owner', $lang ); }
	if ( $only === null && ! $d['photos'] ) { $e['photos'] = nl_owner_t( 'f_photos', $lang ); }
	if ( is_array( $only ) ) { $e = array_intersect_key( $e, array_flip( $only ) ); }
	return $e;
}

function nl_owner_price_text( $f, $lang ) {
	if ( empty( $f['price'] ) ) { return ''; }
	return nl_drop_price_text( $f['price'], 'he' ) . ( ( $f['listing_type'] ?? '' ) === 'rent' ? ' ' . nl_owner_t( 'month', $lang ) : '' );
}

function nl_owner_fact_chips( $f, $lang ) {
	$out = array();
	if ( ! empty( $f['rooms'] ) ) { $out[] = sprintf( nl_owner_t( 'rooms_n', $lang ), nl_drop_fmt_num( $f['rooms'] ) ); }
	if ( ! empty( $f['size_sqm'] ) ) { $out[] = sprintf( nl_owner_t( 'size_n', $lang ), nl_drop_fmt_int( $f['size_sqm'] ) ); }
	if ( isset( $f['floor'] ) && $f['floor'] !== null ) {
		if ( (int) $f['floor'] === 0 ) { $out[] = nl_owner_t( 'ground', $lang ); }
		elseif ( ! empty( $f['total_floors'] ) ) { $out[] = sprintf( nl_owner_t( 'floor_of', $lang ), (int) $f['floor'], (int) $f['total_floors'] ); }
		else { $out[] = sprintf( nl_owner_t( 'floor_n', $lang ), (int) $f['floor'] ); }
	}
	return $out;
}

/** The listing behind a draft, if one was published from it. */
function nl_owner_draft_listing( $id ) {
	$res = get_post_meta( (int) $id, 'nl_result', true );
	$he  = is_array( $res ) ? (int) ( $res['he_id'] ?? 0 ) : 0;
	if ( ! $he || ! get_post( $he ) ) { return null; }
	return array( 'id' => $he, 'url' => (string) get_permalink( $he ), 'status' => (string) get_post_status( $he ), 'market' => (string) get_post_meta( $he, 'nl_status', true ) );
}

function nl_owner_summary( $d, $lang ) {
	$f     = nl_owner_facts( $d['fields'] );
	$ready = ! empty( $f['rooms'] ) || ! empty( $f['area_he'] ) || ! empty( $f['city_he'] );
	$place = trim( implode( ', ', array_filter( array( $f['area_he'] ?? '', $f['city_he'] ?? '' ) ) ) );
	return array( 'title' => $ready ? nl_owner_title_he( $f ) : nl_owner_t( 'draft_title', $lang ), 'place' => $place, 'deal' => (string) $d['fields']['deal'], 'price' => nl_owner_price_text( $f, $lang ) );
}

function nl_owner_draft_out( $d, $lang, $full = true ) {
	$id  = (int) $d['id'];
	$ups = nl_owner_uploads( $id );
	$ph  = array();
	$in  = array();
	foreach ( $d['photos'] as $p ) {
		$o = nl_owner_photo_out( $id, (array) $p, $ups );
		if ( $o ) { $ph[] = $o; if ( $o['ref'] !== '' ) { $in[ $o['ref'] ] = true; } }
	}
	// a photo the server took but no save listed yet (a refresh during an upload) comes back to its owner, never silently to the page
	$recovered = array();
	foreach ( $ups as $ref => $u ) {
		if ( ! isset( $in[ $ref ] ) && empty( $u['gone'] ) ) {
			$o = nl_owner_photo_out( $id, array( 'ref' => $ref ), $ups );
			if ( $o ) { $recovered[] = $o; }
		}
	}
	$out = array(
		'id'        => $id,
		'rev'       => (int) $d['rev'],
		'step'      => (string) ( $d['step'] ?? 'details' ),
		'saved_at'  => (int) ( $d['saved_at'] ?? 0 ),
		'state'     => nl_owner_draft_state( $id ),
		'trashed'   => $d['_post']->post_status === 'trash',
		'listing'   => nl_owner_draft_listing( $id ),
		'pub_rev'   => (int) get_post_meta( $id, 'nl_pub_rev', true ),
		'summary'   => nl_owner_summary( $d, $lang ),
		'photos'    => $ph,
		'recovered' => $recovered,
	);
	if ( $full ) { $out['fields'] = $d['fields']; }
	return $out;
}

/* =====================================================================================================
 * REST: the owner's doors (logged in, the REST nonce), the account doors, and the old doors answered honestly
 * ===================================================================================================== */
add_action( 'rest_api_init', function () {
	$in  = function () { return is_user_logged_in(); };
	$any = '__return_true';
	$ns  = 'nadlan/v1';
	register_rest_route( $ns, '/owner/account/signup', array( 'methods' => 'POST', 'permission_callback' => $any, 'callback' => 'nl_owner_rest_signup' ) );
	register_rest_route( $ns, '/owner/account/login', array( 'methods' => 'POST', 'permission_callback' => $any, 'callback' => 'nl_owner_rest_login' ) );
	register_rest_route( $ns, '/owner/account/recover', array( 'methods' => 'POST', 'permission_callback' => $any, 'callback' => 'nl_owner_rest_recover' ) );
	register_rest_route( $ns, '/owner/draft', array(
		array( 'methods' => 'GET', 'permission_callback' => $in, 'callback' => 'nl_owner_rest_drafts' ),
		array( 'methods' => 'POST', 'permission_callback' => $in, 'callback' => 'nl_owner_rest_draft_create' ),
	) );
	register_rest_route( $ns, '/owner/draft/(?P<id>\d+)', array(
		array( 'methods' => 'GET', 'permission_callback' => $in, 'callback' => 'nl_owner_rest_draft_get' ),
		array( 'methods' => 'POST', 'permission_callback' => $in, 'callback' => 'nl_owner_rest_draft_save' ),
	) );
	register_rest_route( $ns, '/owner/draft/(?P<id>\d+)/check', array( 'methods' => 'POST', 'permission_callback' => $in, 'callback' => 'nl_owner_rest_check' ) );
	register_rest_route( $ns, '/owner/draft/(?P<id>\d+)/preview', array( 'methods' => 'GET', 'permission_callback' => $in, 'callback' => 'nl_owner_rest_preview' ) );
	register_rest_route( $ns, '/owner/draft/(?P<id>\d+)/publish', array( 'methods' => 'POST', 'permission_callback' => $in, 'callback' => 'nl_owner_rest_publish' ) );
	register_rest_route( $ns, '/owner/draft/(?P<id>\d+)/delete', array( 'methods' => 'POST', 'permission_callback' => $in, 'callback' => 'nl_owner_rest_draft_delete' ) );
	register_rest_route( $ns, '/owner/draft/(?P<id>\d+)/restore', array( 'methods' => 'POST', 'permission_callback' => $in, 'callback' => 'nl_owner_rest_draft_restore' ) );
	register_rest_route( $ns, '/owner/photo', array( 'methods' => 'POST', 'permission_callback' => $in, 'callback' => 'nl_owner_rest_photo' ) );
	register_rest_route( $ns, '/owner/submit', array( 'methods' => 'POST', 'permission_callback' => $in, 'callback' => 'nl_owner_rest_submit' ) );
	register_rest_route( $ns, '/owner/build/(?P<drop>\d+)', array( 'methods' => 'POST', 'permission_callback' => $in, 'callback' => 'nl_owner_rest_build' ) );
	register_rest_route( $ns, '/owner/listings', array( 'methods' => 'GET', 'permission_callback' => $in, 'callback' => 'nl_owner_rest_listings' ) );
	register_rest_route( $ns, '/owner/update', array( 'methods' => 'POST', 'permission_callback' => $in, 'callback' => 'nl_owner_rest_update' ) );
	// the first wizard's doors: a page opened before this change gets a clear answer instead of a pending listing
	$gone = function () { return new WP_Error( 'nl_owner_moved', 'הטופס עודכן. מרעננים את העמוד ושולחים שוב.', array( 'status' => 410 ) ); };
	foreach ( array( '/listing-ai-draft', '/listing-submit', '/listing-photo' ) as $r ) {
		register_rest_route( $ns, $r, array( 'methods' => 'POST', 'permission_callback' => '__return_true', 'callback' => $gone ), true );
	}
}, 20 );

function nl_owner_req_lang( WP_REST_Request $req ) {
	return nl_owner_lang( (string) $req->get_param( 'lang' ) );
}

function nl_owner_nocache( $res ) {
	$r = rest_ensure_response( $res );
	if ( $r instanceof WP_REST_Response ) {
		$r->header( 'Cache-Control', 'no-store, private, max-age=0' );
		$r->header( 'X-Robots-Tag', 'noindex, nofollow' );
	}
	return $r;
}

/* ---------------- the account: open, sign in, recover ---------------- */
function nl_owner_rest_signup( WP_REST_Request $req ) {
	$lang = nl_owner_req_lang( $req );
	if ( is_user_logged_in() ) { return array( 'ok' => true, 'already' => true ); }
	if ( '' !== trim( (string) $req->get_param( 'website' ) ) ) { return array( 'ok' => true ); }   // the honeypot: bots fill every field
	if ( ! get_option( 'users_can_register' ) ) { return nl_owner_err( 'acc_closed', 403, $lang ); }
	$name  = nl_owner_cut( trim( sanitize_text_field( (string) $req->get_param( 'name' ) ) ), 40 );
	$email = sanitize_email( (string) $req->get_param( 'email' ) );
	$pass  = (string) $req->get_param( 'password' );
	if ( $name === '' || preg_match( '/https?:|www\.|@|\d/u', $name ) ) { return nl_owner_err( 'acc_name', 400, $lang, array( 'field' => 'name' ) ); }
	if ( ! is_email( $email ) ) { return nl_owner_err( 'acc_email', 400, $lang, array( 'field' => 'email' ) ); }
	if ( strlen( $pass ) < 8 || preg_match( '/^(?:12345678|password|qwerty|11111111|00000000|abcdefgh)/i', $pass ) ) { return nl_owner_err( 'acc_pw', 400, $lang, array( 'field' => 'password' ) ); }
	if ( nl_owner_rate_ip( 'signup', 5, HOUR_IN_SECONDS ) ) { return nl_owner_err( 'acc_rate', 429, $lang ); }
	// the existing signup doors (quick-register, auth-signup) already answer "exists"; this one keeps the input and offers sign-in
	if ( email_exists( $email ) ) { return nl_owner_err( 'acc_exists', 409, $lang, array( 'field' => 'email' ) ); }
	$uid = wp_insert_user( array(
		'user_login'   => sanitize_user( strstr( $email, '@', true ) . '_' . wp_generate_password( 4, false, false ), true ),
		'user_email'   => $email,
		'user_pass'    => $pass,
		'display_name' => $name,
		'first_name'   => $name,
		'role'         => 'subscriber',
	) );
	if ( is_wp_error( $uid ) ) { return new WP_Error( 'create_failed', nl_owner_t( 'upload', $lang ), array( 'status' => 500 ) ); }
	update_user_meta( $uid, 'nl_owner_name', $name );
	update_user_meta( $uid, 'nl_owner_signup', time() );
	wp_set_current_user( $uid );
	wp_set_auth_cookie( $uid, true );
	return array( 'ok' => true );
}

function nl_owner_rest_login( WP_REST_Request $req ) {
	$lang  = nl_owner_req_lang( $req );
	if ( '' !== trim( (string) $req->get_param( 'website' ) ) ) { return nl_owner_err( 'acc_wrong', 401, $lang ); }
	$email = sanitize_email( (string) $req->get_param( 'email' ) );
	$pass  = (string) $req->get_param( 'password' );
	// the same two counters as auth.php's /auth-login: address+email (5) and email alone (10), 15 minutes
	$lock  = 'nlauth_lock_' . md5( strtolower( $email ) . ( $_SERVER['REMOTE_ADDR'] ?? '' ) );
	$elock = 'nlauth_elock_' . md5( strtolower( $email ) );
	if ( (int) get_transient( $lock ) >= 5 || (int) get_transient( $elock ) >= 10 ) { return nl_owner_err( 'acc_locked', 429, $lang ); }
	$user = is_email( $email ) ? get_user_by( 'email', $email ) : false;
	$ok   = $user ? wp_check_password( $pass, $user->user_pass, $user->ID ) : false;
	if ( ! $ok ) {
		set_transient( $lock, (int) get_transient( $lock ) + 1, 15 * MINUTE_IN_SECONDS );
		set_transient( $elock, (int) get_transient( $elock ) + 1, 15 * MINUTE_IN_SECONDS );
		return nl_owner_err( 'acc_wrong', 401, $lang );   // the same answer for an unknown email and a wrong password
	}
	delete_transient( $lock );
	delete_transient( $elock );
	wp_set_current_user( $user->ID );
	wp_set_auth_cookie( $user->ID, true );
	do_action( 'wp_login', $user->user_login, $user );
	return array( 'ok' => true );
}

/** One neutral answer, whether or not the email has an account (OWASP forgot-password). WordPress' own reset link and pages do the rest. */
function nl_owner_rest_recover( WP_REST_Request $req ) {
	$lang  = nl_owner_req_lang( $req );
	$email = sanitize_email( (string) $req->get_param( 'email' ) );
	if ( ! is_email( $email ) ) { return nl_owner_err( 'acc_email', 400, $lang, array( 'field' => 'email' ) ); }
	if ( nl_owner_rate_ip( 'recover', 5, HOUR_IN_SECONDS ) ) { return nl_owner_err( 'acc_rate', 429, $lang ); }
	$t0   = microtime( true );
	$user = get_user_by( 'email', $email );
	if ( $user && ! nl_owner_rate_key( 'recover_mail', 'mail|' . strtolower( $email ), 3, HOUR_IN_SECONDS ) ) {
		$back = esc_url_raw( (string) $req->get_param( 'back' ) );
		if ( $back === '' || strpos( $back, home_url() ) !== 0 ) { $back = home_url( '/post-listing/' ); }
		$GLOBALS['nl_owner_recover_back'] = array( $back, $lang );
		retrieve_password( $user->user_login );
		unset( $GLOBALS['nl_owner_recover_back'] );
	}
	usleep( (int) max( 0, 350000 - ( microtime( true ) - $t0 ) * 1000000 ) + wp_rand( 0, 150000 ) );
	return array( 'ok' => true, 'message' => nl_owner_t( 'rec_sent', $lang ) );
}

add_filter( 'retrieve_password_message', function ( $message ) {
	if ( empty( $GLOBALS['nl_owner_recover_back'] ) ) { return $message; }
	list( $back, $lang ) = $GLOBALS['nl_owner_recover_back'];
	return $message . "\r\n" . nl_owner_t( 'rec_back', $lang ) . "\r\n" . $back . "\r\n";
} );

/* A fresh REST nonce for a signed-in page whose nonce expired (the REST API cannot hand one out: without a nonce it sees no user). */
add_action( 'wp_ajax_nl_owner_nonce', function () {
	nocache_headers();
	wp_send_json( array( 'nonce' => wp_create_nonce( 'wp_rest' ), 'uid' => get_current_user_id() ) );
} );
add_action( 'wp_ajax_nopriv_nl_owner_nonce', function () {
	nocache_headers();
	wp_send_json( array( 'nonce' => '', 'uid' => 0 ), 401 );
} );

/* The signed-in journey page is never stored by a browser or a page cache (another account's data must never come back
   from a cache or the back-forward cache). */
add_action( 'template_redirect', function () {
	if ( ! is_user_logged_in() || ! is_singular() ) { return; }
	$post = get_post( get_queried_object_id() );
	if ( ! $post || ! has_shortcode( (string) $post->post_content, 'nadlan_listing_wizard' ) ) { return; }
	do_action( 'litespeed_control_set_nocache', 'nadlan owner journey (signed in)' );
	nocache_headers();
	header( 'Cache-Control: no-store, no-cache, must-revalidate, max-age=0, private' );
}, 1 );

/* The owner's own draft photos, to the owner only, never cached. */
function nl_owner_img_serve() {
	nocache_headers();
	header( 'X-Robots-Tag: noindex, nofollow' );
	$uid = get_current_user_id();
	$d   = nl_owner_draft_get( (int) ( $_GET['d'] ?? 0 ), $uid, true );   // phpcs:ignore
	$ref = preg_replace( '/[^a-f0-9]/', '', (string) ( $_GET['r'] ?? '' ) );   // phpcs:ignore
	$ups = $d ? nl_owner_uploads( $d['id'] ) : array();
	if ( ! $d || strlen( $ref ) !== 32 || empty( $ups[ $ref ] ) ) { status_header( 404 ); exit; }
	$u     = $ups[ $ref ];
	$dir   = nl_owner_private_dir( (int) get_post_meta( $d['id'], 'nl_owner_user', true ) );
	$thumb = ( $_GET['s'] ?? 't' ) !== 'f' && file_exists( $dir . '/' . $ref . '-t.bin' );   // phpcs:ignore
	$bin   = nl_owner_unseal( (string) @file_get_contents( $dir . '/' . $ref . ( $thumb ? '-t' : '' ) . '.bin' ) );
	if ( $bin === false || $bin === '' ) { status_header( 404 ); exit; }
	header( 'Content-Type: ' . ( $thumb ? 'image/jpeg' : (string) $u['type'] ) );
	header( 'Content-Length: ' . strlen( $bin ) );
	header( 'Cache-Control: private, no-store, max-age=0' );
	header( 'X-Content-Type-Options: nosniff' );
	echo $bin;   // phpcs:ignore -- image bytes
	exit;
}
add_action( 'wp_ajax_nl_owner_img', 'nl_owner_img_serve' );
add_action( 'wp_ajax_nopriv_nl_owner_img', function () { status_header( 401 ); exit; } );

/* ---------------- drafts ---------------- */
function nl_owner_user_drafts( $uid, $status = 'private' ) {
	return get_posts( array(
		'post_type'        => 'nadlan_drop',
		'post_status'      => $status,
		'numberposts'      => 50,
		'orderby'          => 'modified',
		'order'            => 'DESC',
		'fields'           => 'ids',
		'suppress_filters' => true,
		'meta_query'       => array(
			array( 'key' => 'nl_owner_user', 'value' => (string) (int) $uid ),
			array( 'key' => 'nl_draft_v', 'value' => '2' ),
		),
	) );
}

/** Open drafts: never published (a published one lives in My listings). */
function nl_owner_open_drafts( $uid ) {
	$out = array();
	foreach ( nl_owner_user_drafts( $uid ) as $id ) {
		if ( ! nl_owner_draft_listing( $id ) ) { $out[] = (int) $id; }
	}
	return $out;
}

function nl_owner_rest_drafts( WP_REST_Request $req ) {
	$uid  = get_current_user_id();
	$lang = nl_owner_req_lang( $req );
	$list = array();
	foreach ( nl_owner_open_drafts( $uid ) as $id ) {
		$d = nl_owner_draft_get( $id, $uid );
		if ( $d ) { $list[] = nl_owner_draft_out( $d, $lang, false ); }
	}
	usort( $list, function ( $a, $b ) { return $b['saved_at'] - $a['saved_at']; } );
	return nl_owner_nocache( array( 'drafts' => $list ) );
}

function nl_owner_rest_draft_get( WP_REST_Request $req ) {
	$lang = nl_owner_req_lang( $req );
	$d    = nl_owner_draft_get( (int) $req['id'], get_current_user_id() );
	if ( ! $d ) { return nl_owner_err( 'nf', 404, $lang ); }
	return nl_owner_nocache( nl_owner_draft_out( $d, $lang ) );
}

function nl_owner_key_ok( $k ) {
	return is_string( $k ) && preg_match( '/^[A-Za-z0-9\-]{8,64}$/', $k );
}

function nl_owner_rest_draft_create( WP_REST_Request $req ) {
	global $wpdb;
	$uid  = get_current_user_id();
	$lang = nl_owner_req_lang( $req );
	$key  = (string) $req->get_param( 'create_key' );
	if ( ! nl_owner_key_ok( $key ) ) { return nl_owner_err( 'key', 400, $lang ); }
	// the same create key twice (a retry after a lost answer, a double tap) is the same draft
	$name = 'nl_owner_ck_' . md5( $uid . '|' . $key );
	if ( ! nl_drop_lock_insert( $name, 'pending|' . time() ) ) {
		for ( $i = 0; $i < 30; $i++ ) {
			$v = (string) $wpdb->get_var( $wpdb->prepare( "SELECT option_value FROM {$wpdb->options} WHERE option_name = %s", $name ) );
			if ( preg_match( '/^(\d+)\|/', $v, $m ) ) {
				$d = nl_owner_draft_get( (int) $m[1], $uid, true );
				if ( $d ) { $out = nl_owner_draft_out( $d, $lang ); $out['replayed'] = true; return nl_owner_nocache( $out ); }
				return nl_owner_err( 'nf', 404, $lang );
			}
			usleep( 200000 );
		}
		return nl_owner_err( 'publishing', 409, $lang );
	}
	if ( count( nl_owner_open_drafts( $uid ) ) >= NL_OWNER_MAX_DRAFTS || nl_owner_rate( $uid, 'create', 30, DAY_IN_SECONDS ) ) {
		$wpdb->query( $wpdb->prepare( "DELETE FROM {$wpdb->options} WHERE option_name = %s", $name ) );
		return nl_owner_err( 'drafts_max', 429, $lang );
	}
	$id = wp_insert_post( array(
		'post_type'    => 'nadlan_drop',
		'post_status'  => 'private',
		'post_title'   => 'בעלי נכס · טיוטה · #' . $uid . ' · ' . wp_date( 'j.n.Y H:i' ),
		'post_content' => '',
		'post_author'  => nl_drop_author(),
	), true );
	if ( is_wp_error( $id ) || ! $id ) {
		$wpdb->query( $wpdb->prepare( "DELETE FROM {$wpdb->options} WHERE option_name = %s", $name ) );
		return new WP_Error( 'save', nl_owner_t( 'upload', $lang ), array( 'status' => 500 ) );
	}
	$step   = in_array( (string) $req->get_param( 'step' ), array( 'details', 'photos', 'preview' ), true ) ? (string) $req->get_param( 'step' ) : 'details';
	$fields = nl_owner_fields_clean( $req->get_param( 'fields' ) );
	$draft  = array( 'v' => 2, 'rev' => 1, 'fields' => $fields, 'photos' => array(), 'step' => $step, 'saved_at' => time() );
	update_post_meta( $id, 'nl_owner_user', (string) $uid );
	update_post_meta( $id, 'nl_draft_v', '2' );
	update_post_meta( $id, 'nl_door', 'journey' );
	update_post_meta( $id, 'nl_state', 'editing' );
	update_post_meta( $id, 'nl_create_key', $key );
	add_post_meta( $id, 'nl_draft', wp_slash( wp_json_encode( $draft, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES ) ), true );
	$wpdb->update( $wpdb->options, array( 'option_value' => $id . '|' . time() ), array( 'option_name' => $name ) );
	if ( $fields['cname'] !== '' ) { update_user_meta( $uid, 'nl_owner_name', $fields['cname'] ); }
	$d = nl_owner_draft_get( $id, $uid );
	return nl_owner_nocache( new WP_REST_Response( nl_owner_draft_out( $d, $lang ), 201 ) );
}

/** The photos list a save sends: refs this draft holds and attachments its listing already shows, in order, at most 30. */
function nl_owner_photos_clean( $id, $uid, $list ) {
	$ups  = nl_owner_uploads( $id );
	$out  = array();
	$seen = array();
	foreach ( (array) $list as $p ) {
		$p   = is_array( $p ) ? $p : array( 'ref' => (string) $p );
		$ref = preg_replace( '/[^a-f0-9]/', '', (string) ( $p['ref'] ?? '' ) );
		$att = (int) ( $p['att'] ?? 0 );
		if ( $att && ( get_post_type( $att ) !== 'attachment' || (string) get_post_meta( $att, 'nl_owner_user', true ) !== (string) $uid ) ) { $att = 0; }
		if ( $ref !== '' && empty( $ups[ $ref ] ) && ! $att ) { continue; }
		if ( $ref === '' && ! $att ) { continue; }
		$k = $ref !== '' ? $ref : 'a' . $att;
		if ( isset( $seen[ $k ] ) ) { continue; }
		$seen[ $k ] = true;
		$out[]      = array_filter( array( 'ref' => $ref, 'att' => $att ) );
		if ( count( $out ) >= NL_OWNER_MAX_PHOTOS ) { break; }
	}
	return $out;
}

function nl_owner_conflict( $id, $uid, $lang ) {
	$d = nl_owner_draft_get( $id, $uid );
	return new WP_Error( 'conflict', nl_owner_t( 'conflict', $lang ), array( 'status' => 409, 'server' => $d ? nl_owner_draft_out( $d, $lang ) : null ) );
}

function nl_owner_rest_draft_save( WP_REST_Request $req ) {
	$uid  = get_current_user_id();
	$lang = nl_owner_req_lang( $req );
	$id   = (int) $req['id'];
	if ( nl_owner_rate( $uid, 'save', 600, HOUR_IN_SECONDS ) ) { return nl_owner_err( 'rate', 429, $lang ); }
	$d = nl_owner_draft_get( $id, $uid );
	if ( ! $d ) { return nl_owner_err( 'gone', 404, $lang ); }
	if ( in_array( nl_owner_draft_state( $id ), array( 'ready', 'writing' ), true ) && nl_owner_publishing( $id ) ) { return nl_owner_err( 'publishing', 409, $lang ); }
	if ( (int) $req->get_param( 'rev' ) !== (int) $d['rev'] ) { return nl_owner_conflict( $id, $uid, $lang ); }
	$fields = nl_owner_fields_clean( $req->get_param( 'fields' ) );
	$photos = nl_owner_photos_clean( $id, $uid, $req->get_param( 'photos' ) );
	$step   = in_array( (string) $req->get_param( 'step' ), array( 'details', 'photos', 'preview' ), true ) ? (string) $req->get_param( 'step' ) : (string) ( $d['step'] ?? 'details' );
	$new    = array( 'v' => 2, 'rev' => (int) $d['rev'] + 1, 'fields' => $fields, 'photos' => $photos, 'step' => $step, 'saved_at' => time() );
	if ( ! nl_owner_draft_cas( $id, $d['_raw'], $new ) ) { return nl_owner_conflict( $id, $uid, $lang ); }
	// photos the owner removed, or that finished uploading after their tile was removed, are deleted from the private folder
	$keep = array();
	foreach ( $photos as $p ) { if ( ! empty( $p['ref'] ) ) { $keep[ $p['ref'] ] = true; } }
	$drop = array();
	foreach ( (array) $d['photos'] as $p ) { if ( ! empty( $p['ref'] ) && empty( $p['att'] ) && ! isset( $keep[ $p['ref'] ] ) ) { $drop[] = $p['ref']; } }
	foreach ( (array) $req->get_param( 'discard' ) as $r ) { $r = preg_replace( '/[^a-f0-9]/', '', (string) $r ); if ( strlen( $r ) === 32 && ! isset( $keep[ $r ] ) ) { $drop[] = $r; } }
	foreach ( array_unique( $drop ) as $r ) { nl_owner_upload_forget( $id, $uid, $r ); }
	wp_update_post( array( 'ID' => $id, 'post_modified' => current_time( 'mysql' ), 'post_modified_gmt' => current_time( 'mysql', true ) ) );
	if ( $fields['cname'] !== '' ) { update_user_meta( $uid, 'nl_owner_name', $fields['cname'] ); }
	if ( $fields['phone_ok'] && nl_owner_phone( $fields['phone'] ) !== '' ) { update_user_meta( $uid, 'nl_owner_phone', nl_owner_phone( $fields['phone'] ) ); }
	$d = nl_owner_draft_get( $id, $uid );
	return nl_owner_nocache( nl_owner_draft_out( $d, $lang ) );
}

function nl_owner_rest_check( WP_REST_Request $req ) {
	$uid  = get_current_user_id();
	$lang = nl_owner_req_lang( $req );
	$d    = nl_owner_draft_get( (int) $req['id'], $uid );
	if ( ! $d ) { return nl_owner_err( 'gone', 404, $lang ); }
	$only = $req->get_param( 'only' );
	$only = is_array( $only ) ? array_values( array_filter( array_map( 'sanitize_key', $only ) ) ) : null;
	$e    = nl_owner_check( $d, $lang, $only );
	return nl_owner_nocache( array( 'rev' => (int) $d['rev'], 'ready' => ! $e, 'errors' => (object) $e ) );
}

function nl_owner_rest_preview( WP_REST_Request $req ) {
	$uid  = get_current_user_id();
	$lang = nl_owner_req_lang( $req );
	$d    = nl_owner_draft_get( (int) $req['id'], $uid );
	if ( ! $d ) { return nl_owner_err( 'gone', 404, $lang ); }
	$fl   = $d['fields'];
	$f    = nl_owner_facts( $fl );
	$copy = nl_owner_copy( $f, $fl['desc'] );
	$b    = nl_owner_b( $uid, $fl );
	$out  = nl_owner_draft_out( $d, $lang );
	$list = nl_owner_draft_listing( $d['id'] );
	$url  = $list ? $list['url'] : home_url( '/properties/' . nl_drop_slug( $f, $b ) . '/' );
	$pics = array();
	foreach ( $out['photos'] as $p ) { $pics[] = array( 'id' => 0, 'url' => $p['full'], 'w' => $p['w'], 'h' => $p['h'] ); }
	$html = nl_drop_listing_html( array( 'id' => (int) $d['id'], 'facts' => $f, 'copy' => $copy, 'photos' => $pics, 'broker' => $b, 'url' => $url, 'alts' => array(), 'page_id' => 0, 'date' => wp_date( 'Y-m-d' ) ), 'he' );
	$html = preg_replace( '/^<!-- wp:html -->\s*|\s*<!-- \/wp:html -->$/', '', $html );
	return nl_owner_nocache( array(
		'rev'     => (int) $d['rev'],
		'errors'  => (object) nl_owner_check( $d, $lang ),
		'title'   => nl_drop_fill( $copy['he']['title'], $f, 'he' ),
		'place'   => trim( implode( ', ', array_filter( array( $f['area_he'] ?? '', $f['city_he'] ?? '' ) ) ) ),
		'deal'    => (string) $fl['deal'],
		'price'   => nl_owner_price_text( $f, $lang ),
		'facts'   => nl_owner_fact_chips( $f, $lang ),
		'desc'    => nl_owner_paras( $fl['desc'] ),
		'photos'  => $out['photos'],
		'contact' => array( 'name' => $fl['cname'], 'phone' => $b['phone'], 'buttons' => $b['wa'] !== '' ),
		'hold'    => function_exists( 'nadlan_compliance_scan' ) && (bool) nadlan_compliance_scan( $fl['desc'] ),
		'url'     => $url,
		'listing' => $list,
		'html'    => $html,
	) );
}

function nl_owner_rest_draft_delete( WP_REST_Request $req ) {
	$uid  = get_current_user_id();
	$lang = nl_owner_req_lang( $req );
	$d    = nl_owner_draft_get( (int) $req['id'], $uid );
	if ( ! $d ) { return nl_owner_err( 'gone', 404, $lang ); }
	if ( nl_owner_draft_listing( $d['id'] ) ) { return nl_owner_err( 'not_draft', 409, $lang ); }
	if ( nl_owner_publishing( $d['id'] ) ) { return nl_owner_err( 'publishing', 409, $lang ); }
	$r = wp_trash_post( $d['id'] );   // recoverable: WordPress keeps it in the trash (EMPTY_TRASH_DAYS, 30 by default)
	if ( ! $r ) { return nl_owner_err( 'del_failed', 500, $lang ); }
	return nl_owner_nocache( array( 'ok' => true, 'trashed' => true, 'id' => (int) $d['id'] ) );
}

function nl_owner_rest_draft_restore( WP_REST_Request $req ) {
	$uid  = get_current_user_id();
	$lang = nl_owner_req_lang( $req );
	$d    = nl_owner_draft_get( (int) $req['id'], $uid, true );
	if ( ! $d || $d['_post']->post_status !== 'trash' ) { return nl_owner_err( 'gone', 404, $lang ); }
	if ( count( nl_owner_open_drafts( $uid ) ) >= NL_OWNER_MAX_DRAFTS ) { return nl_owner_err( 'drafts_max', 429, $lang ); }
	add_filter( 'wp_untrash_post_status', 'wp_untrash_post_set_previous_status', 10, 3 );
	$r = wp_untrash_post( $d['id'] );
	remove_filter( 'wp_untrash_post_status', 'wp_untrash_post_set_previous_status', 10 );
	if ( ! $r ) { return nl_owner_err( 'del_failed', 500, $lang ); }
	if ( get_post_status( $d['id'] ) !== 'private' ) { wp_update_post( array( 'ID' => $d['id'], 'post_status' => 'private' ) ); }
	$d = nl_owner_draft_get( $d['id'], $uid );
	return nl_owner_nocache( nl_owner_draft_out( $d, $lang ) );
}

/* Deleting a draft for good (the trash emptied after 30 days, or an admin) deletes its private photos too. */
add_action( 'before_delete_post', function ( $id ) {
	if ( get_post_type( $id ) !== 'nadlan_drop' || (string) get_post_meta( $id, 'nl_draft_v', true ) !== '2' ) { return; }
	$uid = (int) get_post_meta( $id, 'nl_owner_user', true );
	foreach ( array_keys( nl_owner_uploads( $id ) ) as $ref ) { nl_owner_upload_forget( $id, $uid, $ref ); }
} );

/* ---------------- photos ---------------- */
function nl_owner_rest_photo( WP_REST_Request $req ) {
	$uid  = get_current_user_id();
	$lang = nl_owner_req_lang( $req );
	if ( ! nl_owner_engine_ok() || ! nl_owner_crypto_ok() ) { return nl_owner_err( 'engine', 503, $lang ); }
	if ( nl_owner_rate( $uid, 'photo', 90, HOUR_IN_SECONDS ) ) { return nl_owner_err( 'rate', 429, $lang ); }
	$d = nl_owner_draft_get( (int) $req->get_param( 'draft' ), $uid );
	if ( ! $d ) { return nl_owner_err( 'need_draft', 400, $lang ); }
	if ( count( nl_owner_uploads( $d['id'] ) ) >= NL_OWNER_MAX_PHOTOS * 2 ) { return nl_owner_err( 'photos_max', 400, $lang ); }
	$files = $req->get_file_params();
	$f     = $files['photo'] ?? null;
	if ( ! is_array( $f ) || empty( $f['tmp_name'] ) ) {
		$code = is_array( $f ) && in_array( (int) ( $f['error'] ?? 0 ), array( UPLOAD_ERR_INI_SIZE, UPLOAD_ERR_FORM_SIZE ), true ) ? 'big' : 'nofile';
		return nl_owner_err( $code, $code === 'big' ? 413 : 400, $lang );
	}
	if ( (int) $f['size'] > NL_DROP_MAX_BYTES ) { return nl_owner_err( 'big', 413, $lang ); }
	$mimes = array( 'jpg|jpeg|jpe' => 'image/jpeg', 'png' => 'image/png', 'webp' => 'image/webp', 'heic' => 'image/heic', 'heif' => 'image/heif' );
	// the bytes decide the type (the browser's shrink sends "photo.jpg"; a renamed file is caught here)
	$head = (string) @file_get_contents( $f['tmp_name'], false, null, 0, 16 );
	$type = '';
	if ( substr( $head, 0, 3 ) === "\xFF\xD8\xFF" ) { $type = 'image/jpeg'; }
	elseif ( substr( $head, 0, 8 ) === "\x89PNG\r\n\x1a\n" ) { $type = 'image/png'; }
	elseif ( substr( $head, 0, 4 ) === 'RIFF' && substr( $head, 8, 4 ) === 'WEBP' ) { $type = 'image/webp'; }
	elseif ( substr( $head, 4, 4 ) === 'ftyp' && preg_match( '/^(heic|heix|hevc|mif1|msf1|heif)$/', substr( $head, 8, 4 ) ) ) { $type = 'image/heic'; }
	if ( ! in_array( $type, $mimes, true ) ) { return nl_owner_err( 'type', 415, $lang ); }
	$ext  = array( 'image/jpeg' => 'jpg', 'image/png' => 'png', 'image/webp' => 'webp', 'image/heic' => 'heic' );
	require_once ABSPATH . 'wp-admin/includes/file.php';
	$tmp  = wp_tempnam( 'nlow.' . $ext[ $type ] );
	$tmp  = preg_replace( '/\.tmp$/', '', $tmp ) . '.' . $ext[ $type ];
	if ( ! @copy( $f['tmp_name'], $tmp ) ) { return nl_owner_err( 'upload', 500, $lang ); }
	$clean = nl_drop_clean_image( $tmp, $type );
	if ( is_wp_error( $clean ) ) {
		@unlink( $tmp );
		$code = in_array( $clean->get_error_code(), array( 'heic', 'orient' ), true ) ? $clean->get_error_code() : 'corrupt';
		return nl_owner_err( $code, $code === 'heic' ? 415 : 422, $lang );
	}
	$size  = @getimagesize( $clean['file'] );
	$w     = (int) ( $size[0] ?? 0 );
	$h     = (int) ( $size[1] ?? 0 );
	$thumb = '';
	$ed    = wp_get_image_editor( $clean['file'] );
	if ( ! is_wp_error( $ed ) ) {
		$ed->resize( 720, 720, false );
		$ed->set_quality( 82 );
		$saved = $ed->save( $clean['file'] . '-t.jpg', 'image/jpeg' );
		if ( ! is_wp_error( $saved ) && ! empty( $saved['path'] ) ) { $thumb = (string) @file_get_contents( $saved['path'] ); @unlink( $saved['path'] ); }
	}
	$dir = nl_owner_private_dir( $uid );
	$ref = bin2hex( random_bytes( 16 ) );
	$box = nl_owner_seal( (string) file_get_contents( $clean['file'] ) );
	@unlink( $clean['file'] );
	if ( $box === false || false === @file_put_contents( $dir . '/' . $ref . '.bin', $box ) ) { return nl_owner_err( 'upload', 500, $lang ); }
	if ( $thumb !== '' ) { $tb = nl_owner_seal( $thumb ); if ( $tb !== false ) { @file_put_contents( $dir . '/' . $ref . '-t.bin', $tb ); } }
	add_post_meta( $d['id'], 'nl_upload', wp_slash( wp_json_encode( array( 'ref' => $ref, 'ext' => $clean['ext'], 'type' => $clean['type'], 'w' => $w, 'h' => $h, 't' => time() ) ) ) );
	wp_cache_delete( $d['id'], 'post_meta' );
	$ups = nl_owner_uploads( $d['id'] );
	return nl_owner_nocache( nl_owner_photo_out( $d['id'], array( 'ref' => $ref ), $ups ) );
}

/* ---------------- public photos follow the listing's status (HAD-256 P0, Maya's R1 on d2b8f349) ----------------
 * A draft photo exists only sealed in private storage. A public copy (uploads/nl-listings/<ref>.<ext> + its media
 * attachment and sizes) is written ONLY while the listing's post_status is 'publish', and only after that status is
 * committed: the owner build writes the page as a non-public draft, commits 'publish', then copies (publish-then-copy).
 * A failed, held (pending), test (draft), fenced-out or crashed publish leaves no public copy. When a listing leaves
 * 'publish' (removed to the trash, sent back to pending or draft) its public copies are deleted (the sealed originals
 * stay, so publishing again re-creates them). The same holds when an editor approves a held listing in wp-admin
 * (transition_post_status). A crash between the 'publish' commit and the copy leaves a published listing with missing
 * pictures (fail-closed), repaired by the retry of the same publish or by the next transition.
 * Attachments are allocated like the listing: an auto-draft attachment WITHOUT a file, claimed by INSERT IGNORE on
 * nl_att_<ref>; only the claimed one ever gets the file. A loser keeps an empty row for WordPress' daily clean-up. */

/** The owner draft behind a listing (2.0 journey), or null. */
function nl_owner_listing_draft( $he_id ) {
	if ( get_post_type( $he_id ) !== 'nadlan_property' || (string) get_post_meta( $he_id, 'nl_owner', true ) !== '1' ) { return null; }
	$drop = (int) get_post_meta( $he_id, 'nl_drop_id', true );
	if ( ! $drop || (string) get_post_meta( $drop, 'nl_draft_v', true ) !== '2' ) { return null; }
	$uid = (int) get_post_meta( $drop, 'nl_owner_user', true );
	$d   = nl_owner_draft_get( $drop, $uid, true );
	return $d ? array( 'drop' => $drop, 'uid' => $uid, 'd' => $d ) : null;
}

function nl_owner_att_claim( $ref ) {
	global $wpdb;
	$j = json_decode( (string) $wpdb->get_var( $wpdb->prepare( "SELECT option_value FROM {$wpdb->options} WHERE option_name = %s LIMIT 1", 'nl_att_' . $ref ) ), true );
	return is_array( $j ) ? (int) ( $j['att'] ?? 0 ) : 0;
}

/** The planned public address of a photo (the page is rendered with it before any file exists). */
function nl_owner_public_url( $ref, $ext ) {
	$ud = wp_upload_dir( null, false );
	return untrailingslashit( $ud['baseurl'] ) . '/nl-listings/' . $ref . '.' . $ext;
}

/** The listing's photos as the page shows them: the attachment when it exists, else the planned address. */
function nl_owner_page_photos( $drop_id, $d ) {
	$ups = nl_owner_uploads( $drop_id );
	$out = array();
	foreach ( (array) $d['photos'] as $p ) {
		$ref = (string) ( $p['ref'] ?? '' );
		if ( $ref === '' || empty( $ups[ $ref ] ) ) { continue; }
		$att = nl_owner_att_claim( $ref );
		$m   = $att ? wp_get_attachment_metadata( $att ) : array();
		$out[] = array( 'id' => $att && get_attached_file( $att ) ? $att : 0, 'url' => nl_owner_public_url( $ref, $ups[ $ref ]['ext'] ), 'w' => (int) ( $m['width'] ?? $ups[ $ref ]['w'] ), 'h' => (int) ( $m['height'] ?? $ups[ $ref ]['h'] ), 'ref' => $ref );
	}
	return $out;
}

/** One public copy and its attachment, for a listing that is published right now. Returns the attachment id or 0. */
function nl_owner_attach( $drop_id, $uid, $ref, $he_id ) {
	global $wpdb;
	if ( get_post_status( $he_id ) !== 'publish' ) { return 0; }
	$ups = nl_owner_uploads( $drop_id );
	if ( empty( $ups[ $ref ] ) ) { return 0; }
	$u   = $ups[ $ref ];
	$att = nl_owner_att_claim( $ref );
	if ( ! $att || get_post_type( $att ) !== 'attachment' ) {
		$ph = wp_insert_attachment( array( 'post_mime_type' => $u['type'], 'post_title' => 'nadlan-owner-listing', 'post_status' => 'auto-draft', 'post_author' => (int) $uid, 'post_parent' => (int) $he_id ) );
		if ( is_wp_error( $ph ) || ! $ph ) { return 0; }
		do_action( 'nl_drop_checkpoint', 'attach_pending', (int) $drop_id );
		$wpdb->query( $wpdb->prepare( "DELETE FROM {$wpdb->options} WHERE option_name = %s AND option_value NOT LIKE %s", 'nl_att_' . $ref, '%"att":%' ) );
		nl_drop_lock_insert( 'nl_att_' . $ref, wp_json_encode( array( 'att' => (int) $ph, 't' => time() ) ) );
		$att = nl_owner_att_claim( $ref );
		if ( ! $att ) { return 0; }
	}
	$file = get_attached_file( $att );
	if ( ! $file || ! file_exists( $file ) ) {
		nl_drop_fence( $drop_id, 'attach' );
		if ( get_post_status( $he_id ) !== 'publish' ) { return 0; }   // the status decides, at the moment of the copy
		$ud  = wp_upload_dir();
		$dir = untrailingslashit( $ud['basedir'] ) . '/nl-listings';
		wp_mkdir_p( $dir );
		$dst = $dir . '/' . $ref . '.' . $u['ext'];
		if ( ! file_exists( $dst ) ) {
			$bin = nl_owner_unseal( (string) @file_get_contents( nl_owner_private_dir( $uid ) . '/' . $ref . '.bin' ) );
			if ( $bin === false || $bin === '' || false === @file_put_contents( $dst, $bin ) ) { return 0; }
		}
		update_attached_file( $att, $dst );
		$wpdb->update( $wpdb->posts, array( 'guid' => esc_url_raw( nl_owner_public_url( $ref, $u['ext'] ) ) ), array( 'ID' => $att ) );
		clean_post_cache( $att );
		do_action( 'litespeed_purge_url', nl_owner_public_url( $ref, $u['ext'] ) );   // a page cache may hold a 404 from an earlier withdraw
	}
	if ( get_post_status( $att ) !== 'inherit' || (int) get_post_field( 'post_parent', $att ) !== (int) $he_id ) {
		wp_update_post( array( 'ID' => $att, 'post_status' => 'inherit', 'post_parent' => (int) $he_id ) );
	}
	if ( ! wp_get_attachment_metadata( $att ) ) {
		require_once ABSPATH . 'wp-admin/includes/image.php';
		wp_update_attachment_metadata( $att, wp_generate_attachment_metadata( $att, get_attached_file( $att ) ) );
	}
	update_post_meta( $att, 'nl_owner_user', (string) $uid );
	update_post_meta( $att, 'nl_owner_ref', $ref );
	return (int) $att;
}

/** The public copies of a published listing: made for its current photos, removed for photos it no longer shows. */
function nl_owner_media_publish( $he_id ) {
	$x = nl_owner_listing_draft( $he_id );
	if ( ! $x || get_post_status( $he_id ) !== 'publish' ) { return false; }
	if ( ! nl_drop_lock_acquire( $x['drop'], 'media:' . $he_id ) ) { return false; }   // a build holds it; it copies itself
	try {
		$ids   = array();
		$keep  = array();
		$title = (string) get_the_title( $he_id );
		foreach ( (array) $x['d']['photos'] as $p ) {
			$ref = (string) ( $p['ref'] ?? '' );
			if ( $ref === '' ) { continue; }
			$keep[ $ref ] = true;
			$att = nl_owner_attach( $x['drop'], $x['uid'], $ref, $he_id );
			if ( $att ) { $ids[] = $att; }
		}
		foreach ( get_children( array( 'post_parent' => $he_id, 'post_type' => 'attachment', 'fields' => 'ids' ) ) as $old ) {
			$r = (string) get_post_meta( $old, 'nl_owner_ref', true );
			if ( $r !== '' && ! isset( $keep[ $r ] ) ) { nl_owner_media_drop( $old, $r ); }
		}
		nl_drop_fence( $x['drop'], 'media_meta' );
		if ( $ids ) { set_post_thumbnail( $he_id, $ids[0] ); }
		foreach ( $ids as $i => $att ) { update_post_meta( $att, '_wp_attachment_image_alt', wp_slash( $title . ( $i ? ' · ' . ( $i + 1 ) : '' ) ) ); }
		$photos = nl_owner_page_photos( $x['drop'], $x['d'] );
		update_post_meta( $he_id, 'nl_photos_json', wp_slash( wp_json_encode( $photos, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES ) ) );
		update_post_meta( $he_id, 'photos_csv', implode( ',', wp_list_pluck( $photos, 'url' ) ) );
		nl_drop_purge( array( $he_id ) );
		return true;
	} catch ( NL_Drop_Fenced $e ) {
		return false;
	} finally {
		nl_drop_lock_release( $x['drop'] );
	}
}

/** Every public file of one photo ref: its attachment (with its sizes) and the copy itself, even one a dead run left
 *  without an attachment record. The sealed original stays private, so publishing again re-creates them. */
function nl_owner_media_drop( $att, $ref, $ext = '' ) {
	global $wpdb;
	$urls = array();
	if ( $att && get_post_type( $att ) === 'attachment' ) {
		$urls[] = (string) wp_get_attachment_url( $att );
		wp_delete_attachment( (int) $att, true );
	}
	$ud = wp_upload_dir( null, false );
	foreach ( (array) glob( untrailingslashit( $ud['basedir'] ) . '/nl-listings/' . $ref . '*' ) as $f ) {
		if ( is_file( $f ) ) { $urls[] = untrailingslashit( $ud['baseurl'] ) . '/nl-listings/' . basename( $f ); @unlink( $f ); }
	}
	$wpdb->delete( $wpdb->options, array( 'option_name' => 'nl_att_' . $ref ) );
	foreach ( array_filter( $urls ) as $u ) { do_action( 'litespeed_purge_url', $u ); }
}

/** A listing that leaves 'publish' takes every public copy of every photo its draft ever had with it. */
function nl_owner_media_withdraw( $he_id ) {
	$x    = nl_owner_listing_draft( $he_id );
	$refs = $x ? array_keys( nl_owner_uploads( $x['drop'] ) ) : array();
	foreach ( get_children( array( 'post_parent' => $he_id, 'post_type' => 'attachment', 'post_status' => 'any', 'fields' => 'ids' ) ) as $att ) {
		$ref = (string) get_post_meta( $att, 'nl_owner_ref', true );
		if ( $ref !== '' ) { nl_owner_media_drop( $att, $ref ); $refs = array_diff( $refs, array( $ref ) ); }
	}
	foreach ( $refs as $ref ) { nl_owner_media_drop( nl_owner_att_claim( $ref ), $ref ); }
	delete_post_thumbnail( $he_id );
	nl_drop_purge( array( $he_id ) );
}

/* Leaving 'publish' (trash, pending, draft, private), from any door, wp-admin included: the public copies go FIRST,
   before the status row changes (fail-closed: a crash in between leaves a published listing without pictures, which
   the next view repairs, never an unpublished listing with public pictures). */
add_filter( 'wp_insert_post_data', function ( $data, $postarr ) {
	$id = (int) ( $postarr['ID'] ?? 0 );
	// WordPress empties the address of a pending post saved by a user who cannot publish (the owner): an owner listing
	// keeps its Latin address, so an approval in wp-admin never falls back to an address made of the Hebrew title
	if ( $id && ( $data['post_type'] ?? '' ) === 'nadlan_property' && ( $data['post_name'] ?? '' ) === '' && (string) get_post_meta( $id, 'nl_owner', true ) === '1' ) {
		$keep = (string) get_post_field( 'post_name', $id );
		if ( $keep !== '' ) { $data['post_name'] = $keep; }
	}
	if ( $id && ( $data['post_type'] ?? '' ) === 'nadlan_property' && ( $data['post_status'] ?? '' ) !== 'publish' && get_post_status( $id ) === 'publish' && nl_owner_listing_draft( $id ) ) {
		nl_owner_media_withdraw( $id );
	}
	return $data;
}, 99, 2 );

add_action( 'transition_post_status', function ( $new, $old, $post ) {
	if ( ! $post || $post->post_type !== 'nadlan_property' || $new === $old ) { return; }
	if ( ! nl_owner_listing_draft( $post->ID ) ) { return; }
	if ( $new === 'publish' ) { nl_owner_media_publish( $post->ID ); }
	elseif ( $old === 'publish' ) { nl_owner_media_withdraw( $post->ID ); }   // a second pass (idempotent)
}, 20, 3 );

/* A published owner listing whose pictures a dead run did not finish is repaired on its next view. */
add_action( 'template_redirect', function () {
	if ( ! is_singular( 'nadlan_property' ) ) { return; }
	$id = (int) get_queried_object_id();
	if ( get_post_status( $id ) !== 'publish' || ! nl_owner_listing_draft( $id ) ) { return; }
	$photos = json_decode( (string) get_post_meta( $id, 'nl_photos_json', true ), true );
	$ud     = wp_upload_dir( null, false );
	foreach ( (array) $photos as $p ) {
		$rel = str_replace( untrailingslashit( $ud['baseurl'] ), '', (string) ( $p['url'] ?? '' ) );
		if ( $rel !== '' && ! file_exists( untrailingslashit( $ud['basedir'] ) . $rel ) ) { nl_owner_media_publish( $id ); break; }
	}
}, 5 );

/* The daily sweep (WordPress' wp_scheduled_delete): a public copy whose listing is not published goes. */
add_action( 'wp_scheduled_delete', 'nl_owner_media_sweep' );
function nl_owner_media_sweep() {
	$ud = wp_upload_dir( null, false );
	foreach ( (array) glob( untrailingslashit( $ud['basedir'] ) . '/nl-listings/*' ) as $f ) {
		if ( ! is_file( $f ) || ! preg_match( '/^([a-f0-9]{32})/', basename( $f ), $m ) ) { continue; }
		$att    = nl_owner_att_claim( $m[1] );
		$parent = $att ? (int) get_post_field( 'post_parent', $att ) : 0;
		if ( ! $parent || get_post_status( $parent ) !== 'publish' ) { nl_owner_media_drop( $att, $m[1] ); }
	}
}

/**
 * The listing's status, written by ONE UPDATE that succeeds only while this run's own lock row exists (the same fence
 * as nl_drop_fenced_meta): a run that lost the lock can never publish, hold or unpublish the listing. Leaving
 * 'publish' takes the public copies first (fail-closed). A first publish gets its date and a unique address in the
 * same UPDATE. WordPress' transition hooks then run as for wp_update_post (the public copies for 'publish').
 */
function nl_owner_set_status( $drop_id, $he, $status, $slug = '' ) {
	global $wpdb;
	$drop_id = (int) $drop_id;
	$he      = (int) $he;
	$old     = (string) get_post_status( $he );
	if ( $old === $status ) { return; }
	$mine = (string) ( $GLOBALS['nl_drop_locks'][ $drop_id ]['val'] ?? '' );
	if ( $mine === '' ) { throw new NL_Drop_Fenced( 'status' ); }
	if ( $old === 'publish' ) { nl_owner_media_withdraw( $he ); }
	$post = get_post( $he );
	$name = (string) $post->post_name !== '' ? (string) $post->post_name : (string) $slug;
	$slug = $status === 'publish' ? wp_unique_post_slug( $name, $he, 'publish', $post->post_type, (int) $post->post_parent ) : $name;
	$now  = current_time( 'mysql' );
	$gmt  = current_time( 'mysql', true );
	$first = $status === 'publish' && ( (string) $post->post_date_gmt === '' || (string) $post->post_date_gmt === '0000-00-00 00:00:00' );
	do_action( 'nl_drop_checkpoint', 'owner_status_sql', $drop_id );
	$n = $wpdb->query( $wpdb->prepare(
		"UPDATE {$wpdb->posts} SET post_status = %s, post_name = %s, post_modified = %s, post_modified_gmt = %s" . ( $first ? ', post_date = %s, post_date_gmt = %s' : '' ) .
		" WHERE ID = %d AND EXISTS ( SELECT 1 FROM {$wpdb->options} WHERE option_name = %s AND option_value = %s )",
		array_merge( array( $status, $slug, $now, $gmt ), $first ? array( $now, $gmt ) : array(), array( $he, 'nl_drop_lock_' . $drop_id, $mine ) )
	) );
	clean_post_cache( $he );
	if ( 1 !== (int) $n ) { throw new NL_Drop_Fenced( 'status' ); }
	wp_transition_post_status( $status, $old, get_post( $he ) );
}

/**
 * The owner listing's own build (one drop, one Hebrew page), under the drop lock the caller holds:
 * claim the one post -> write it as a non-public draft (content, meta, page) -> commit the status (publish, or pending
 * on a fair-housing hold, or draft for an admin test) -> the public copies, only after 'publish' -> commit nl_result.
 * Every write that matters is fenced (x-broker-drop 1.1.4); the commit is the atomic fenced meta.
 */
function nl_owner_build( $drop_id, $uid, $d, $b, $target ) {
	$fl   = $d['fields'];
	$f    = nl_owner_facts( $fl );
	$copy = nl_owner_copy( $f, $fl['desc'] );
	$pub  = $f;
	unset( $pub['street_he'], $pub['street_en'] );
	nl_drop_fence( $drop_id, 'owner_claim' );
	update_post_meta( $drop_id, 'nl_state', 'writing' );
	$slug  = nl_drop_slug( $f, $b );
	$claim = nl_drop_claim_post( $drop_id, 'he', 'nadlan_property', 0, 0 );
	if ( is_wp_error( $claim ) ) { return $claim; }
	$he   = (int) $claim[0];
	$now  = (string) get_post_status( $he );
	$edit = ! in_array( $now, array( 'auto-draft', 'draft' ), true );
	if ( $now !== 'auto-draft' && (string) get_post_field( 'post_name', $he ) !== '' ) { $slug = (string) get_post_field( 'post_name', $he ); }   // a permanent address
	$title = nl_drop_fill( $copy['he']['title'], $f, 'he' );
	if ( $edit && $now === 'publish' && $target !== 'publish' ) {
		// an edit that must wait for review (or an admin test) leaves the site BEFORE its new words are written
		nl_drop_fence( $drop_id, 'owner_unpublish' );
		nl_owner_set_status( $drop_id, $he, $target, $slug );
		$now = $target;
	}
	nl_drop_fence( $drop_id, 'owner_content' );
	$had = nl_drop_kses_off();
	$r   = wp_update_post( array(
		'ID'           => $he,
		'post_status'  => $edit ? $now : 'draft',   // never public before the page is complete
		'post_title'   => $title,
		'post_name'    => $slug,
		'post_excerpt' => nl_drop_fill( $copy['he']['dek'], $f, 'he' ),
		'post_author'  => (int) $uid,
	), true );
	nl_drop_kses_on( $had );
	if ( is_wp_error( $r ) || ! $r ) { return is_wp_error( $r ) ? $r : new WP_Error( 'nl_owner_update', 'update failed' ); }
	// WordPress empties the address of a pending post saved by a user who cannot publish (the owner); the listing
	// keeps its Latin address, so an approval in wp-admin or the next publish never falls back to the Hebrew title
	if ( (string) get_post_field( 'post_name', $he ) !== $slug ) {
		global $wpdb;
		$wpdb->update( $wpdb->posts, array( 'post_name' => $slug ), array( 'ID' => $he ) );
		clean_post_cache( $he );
	}
	$ptype = array( 'garden' => 'garden', 'penthouse' => 'penthouse', 'duplex' => 'duplex', 'cottage' => 'cottage' );
	$meta  = array(
		'listing_type' => $f['listing_type'], 'property_type' => $ptype[ $f['property_type'] ] ?? 'apartment', 'price' => $f['price'], 'rooms' => $f['rooms'],
		'floor' => $f['floor'], 'total_floors' => $f['total_floors'], 'size_sqm' => $f['size_sqm'], 'sqm' => $f['size_sqm'], 'city' => $f['city_he'], 'neighborhood' => $f['area_he'],
	);
	nl_drop_fence( $drop_id, 'owner_meta' );
	foreach ( $meta as $k => $v ) {
		if ( $v !== null && $v !== '' ) { update_post_meta( $he, $k, $v ); } else { delete_post_meta( $he, $k ); }
	}
	if ( ! $edit ) {
		update_post_meta( $he, 'status', 'active' );
		update_post_meta( $he, 'nl_status', 'active' );
	}
	update_post_meta( $he, 'claim_status', 'verified' );
	update_post_meta( $he, 'nl_drop_id', (string) $drop_id );
	update_post_meta( $he, 'source', 'owner_wizard' );
	update_post_meta( $he, 'nl_owner', '1' );
	update_post_meta( $he, 'owner_user_id', (int) $uid );
	update_post_meta( $he, 'nl_owner_contact', wp_slash( wp_json_encode( array( 'name' => $b['name_he'], 'phone' => $b['phone'] ), JSON_UNESCAPED_UNICODE ) ) );
	update_post_meta( $he, 'nl_facts', wp_slash( wp_json_encode( $pub, JSON_UNESCAPED_UNICODE ) ) );
	update_post_meta( $he, 'nl_copy', wp_slash( wp_json_encode( $copy, JSON_UNESCAPED_UNICODE ) ) );
	$photos = nl_owner_page_photos( $drop_id, $d );
	update_post_meta( $he, 'nl_photos_json', wp_slash( wp_json_encode( $photos, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES ) ) );
	update_post_meta( $he, 'photos_csv', implode( ',', wp_list_pluck( $photos, 'url' ) ) );
	update_post_meta( $he, '_yoast_wpseo_title', wp_slash( nl_drop_fill( $copy['he']['seo_title'], $f, 'he' ) ) );
	update_post_meta( $he, '_yoast_wpseo_metadesc', wp_slash( nl_drop_fill( $copy['he']['seo_desc'], $f, 'he' ) ) );
	nl_drop_fence( $drop_id, 'owner_render' );
	nl_drop_render_all( $he, $b );
	// the status commit; the transition hook makes the public copies only for 'publish'
	nl_drop_fence( $drop_id, 'owner_status' );
	nl_owner_set_status( $drop_id, $he, $target, $slug );
	if ( $target === 'publish' ) {
		do_action( 'nl_drop_checkpoint', 'owner_before_media', (int) $drop_id );
		nl_owner_media_publish( $he );   // idempotent: repairs a run that died between the status and the copies
	} else {
		nl_owner_media_withdraw( $he );
	}
	nl_drop_purge( array( $he ) );
	$st  = (string) get_post_status( $he );
	$res = array( 'state' => $st === 'publish' ? 'published' : ( $st === 'pending' ? 'pending' : 'draft' ), 'he_id' => $he, 'en_id' => 0, 'url_he' => (string) get_permalink( $he ), 'url_en' => '', 'urls' => array( 'he' => (string) get_permalink( $he ) ), 'title' => $title, 'ai' => 'off', 'updated' => $edit );
	nl_drop_fenced_meta( $drop_id, 'nl_result', $res );
	nl_drop_fenced_meta( $drop_id, 'nl_state', $res['state'] );
	return $res;
}

/* ---------------- publish ---------------- */
function nl_owner_pubs( $uid ) {
	$v = get_transient( 'nlowner_pubs_' . (int) $uid );
	$v = is_array( $v ) ? $v : array();
	$now = time();
	return array_filter( $v, function ( $t ) use ( $now ) { return $now - (int) $t < DAY_IN_SECONDS; } );
}

function nl_owner_pub_count( $uid, $drop_id ) {
	$v = nl_owner_pubs( $uid );
	$v[ (int) $drop_id ] = $v[ (int) $drop_id ] ?? time();
	set_transient( 'nlowner_pubs_' . (int) $uid, $v, DAY_IN_SECONDS );
}

function nl_owner_pub_out( $drop_id, $lang, $extra = array() ) {
	$res  = get_post_meta( (int) $drop_id, 'nl_result', true );
	$he   = is_array( $res ) ? (int) ( $res['he_id'] ?? 0 ) : 0;
	$st   = $he ? (string) get_post_status( $he ) : '';
	$time = $he ? (int) get_post_time( 'U', true, $he ) : 0;
	return array_merge( array(
		'state'        => $st === 'publish' ? 'published' : ( $st === 'pending' ? 'pending' : ( $st === 'trash' ? 'removed' : 'draft' ) ),
		'he_id'        => $he,
		'url'          => $he ? (string) get_permalink( $he ) : '',
		'title'        => $he ? html_entity_decode( get_the_title( $he ), ENT_QUOTES, 'UTF-8' ) : '',
		'published_at' => $time,
		'rev'          => (int) get_post_meta( (int) $drop_id, 'nl_pub_rev', true ),
	), $extra );
}

function nl_owner_rest_publish( WP_REST_Request $req ) {
	$uid  = get_current_user_id();
	$lang = nl_owner_req_lang( $req );
	$id   = (int) $req['id'];
	if ( ! nl_owner_engine_ok() ) { return nl_owner_err( 'engine', 503, $lang ); }
	if ( nl_owner_rate( $uid, 'pubtry', 30, HOUR_IN_SECONDS ) ) { return nl_owner_err( 'rate', 429, $lang ); }
	$key = (string) $req->get_param( 'request_key' );
	$rev = (int) $req->get_param( 'rev' );
	if ( ! nl_owner_key_ok( $key ) ) { return nl_owner_err( 'key', 400, $lang ); }
	$d = nl_owner_draft_get( $id, $uid );
	if ( ! $d ) { return nl_owner_err( 'gone', 404, $lang ); }
	$asked = get_post_meta( $id, 'nl_pub_req', true );
	$asked = is_array( $asked ) ? $asked : array();
	// the same key again: the same answer, or a refusal when it now carries another revision
	if ( ( $asked['key'] ?? '' ) === $key && (int) ( $asked['rev'] ?? 0 ) !== $rev ) { return nl_owner_err( 'key_reused', 409, $lang ); }
	$res = get_post_meta( $id, 'nl_result', true );
	if ( is_array( $res ) && ! empty( $res['he_id'] ) && (int) get_post_meta( $id, 'nl_pub_rev', true ) === $rev ) {
		return nl_owner_nocache( nl_owner_pub_out( $id, $lang, array( 'replayed' => true ) ) );
	}
	if ( (int) $d['rev'] !== $rev ) { return nl_owner_err( 'changed', 409, $lang, array( 'server' => nl_owner_draft_out( $d, $lang ) ) ); }
	$errors = nl_owner_check( $d, $lang );
	if ( $errors ) { return nl_owner_err( 'invalid', 422, $lang, array( 'errors' => $errors ) ); }
	if ( ! nl_drop_lock_acquire( $id, 'owner:' . $uid . ':' . substr( $key, 0, 12 ) ) ) {
		return nl_owner_nocache( new WP_REST_Response( array( 'state' => 'building', 'message' => nl_owner_t( 'building', $lang ) ), 202 ) );
	}
	try {
		wp_cache_delete( $id, 'post_meta' );
		nl_drop_fence( $id, 'owner_start' );
		$res = get_post_meta( $id, 'nl_result', true );
		if ( is_array( $res ) && ! empty( $res['he_id'] ) && (int) get_post_meta( $id, 'nl_pub_rev', true ) === $rev ) {
			return nl_owner_nocache( nl_owner_pub_out( $id, $lang, array( 'replayed' => true ) ) );
		}
		$he_id   = is_array( $res ) ? (int) ( $res['he_id'] ?? 0 ) : 0;
		$is_edit = $he_id && get_post( $he_id ) && get_post_status( $he_id ) !== 'trash';
		$counted = isset( nl_owner_pubs( $uid )[ $id ] ) || (string) get_post_meta( $id, 'nl_counted', true ) === '1';
		if ( ! $is_edit ) {
			if ( nl_owner_active_count( $uid ) >= NL_OWNER_MAX_ACTIVE ) { return nl_owner_err( 'cap', 409, $lang ); }
			if ( ! $counted && count( nl_owner_pubs( $uid ) ) >= NL_OWNER_PUB_DAY ) { return nl_owner_err( 'quota', 429, $lang ); }
		}
		update_post_meta( $id, 'nl_pub_req', array( 'key' => $key, 'rev' => $rev, 'hash' => hash( 'sha256', $d['_raw'] ), 't' => time() ) );
		$fl   = $d['fields'];
		$f    = nl_owner_facts( $fl );
		$b    = nl_owner_b( $uid, $fl );
		$hits = function_exists( 'nadlan_compliance_scan' ) ? nadlan_compliance_scan( $fl['desc'] ) : array();
		nl_drop_fence( $id, 'owner_drop_meta' );
		update_post_meta( $id, 'nl_facts', wp_slash( wp_json_encode( $f, JSON_UNESCAPED_UNICODE ) ) );
		update_post_meta( $id, 'nl_text', wp_slash( $fl['desc'] ) );
		update_post_meta( $id, 'nl_owner_contact', wp_slash( wp_json_encode( array( 'name' => $fl['cname'], 'phone' => $b['phone'] ), JSON_UNESCAPED_UNICODE ) ) );
		if ( $hits ) { update_post_meta( $id, 'nl_hold', wp_slash( wp_json_encode( $hits, JSON_UNESCAPED_UNICODE ) ) ); } else { delete_post_meta( $id, 'nl_hold' ); }
		$test   = (string) $req->get_param( 'test' ) === '1' && current_user_can( 'manage_options' );   // the owner's own test runs stay drafts
		$target = $hits ? 'pending' : ( $test ? 'draft' : 'publish' );
		@set_time_limit( 170 );
		$r = nl_owner_build( $id, $uid, $d, $b, $target );
		if ( is_wp_error( $r ) ) {
			if ( in_array( $r->get_error_code(), array( 'nl_drop_fenced', 'nl_drop_busy' ), true ) ) {
				return nl_owner_nocache( new WP_REST_Response( array( 'state' => 'building', 'message' => nl_owner_t( 'building', $lang ) ), 202 ) );
			}
			nl_drop_fenced_meta( $id, 'nl_state', 'failed' );
			return nl_owner_err( 'build', 500, $lang, array( 'detail' => $r->get_error_code() ) );
		}
		if ( $target === 'pending' ) {
			@wp_mail( get_option( 'admin_email' ), nl_owner_t( 'mail_hold', 'he' ), nl_owner_t( 'mail_hold_b', 'he' ) . admin_url( 'post.php?post=' . (int) $r['he_id'] . '&action=edit' ) );
		}
		if ( ! $is_edit && ! $counted ) { nl_owner_pub_count( $uid, $id ); update_post_meta( $id, 'nl_counted', '1' ); }
		nl_drop_fenced_meta( $id, 'nl_pub_rev', (string) $rev );
		return nl_owner_nocache( nl_owner_pub_out( $id, $lang, array( 'updated' => (bool) $is_edit ) ) );
	} catch ( NL_Drop_Fenced $e ) {
		return nl_owner_nocache( new WP_REST_Response( array( 'state' => 'building', 'message' => nl_owner_t( 'building', $lang ) ), 202 ) );
	} finally {
		nl_drop_lock_release( $id );
	}
}

/* ---------------- the 1.x doors ---------------- */
function nl_owner_rest_submit( WP_REST_Request $req ) {
	if ( (string) $req->get_param( 'who' ) === 'broker' ) {
		return array( 'state' => 'broker', 'url' => home_url( '/brokers/#join' ) );
	}
	// 1.x created a new submission on every send; an open 1.x page is told to refresh into the journey
	return nl_owner_err( 'moved', 410, 'he' );
}

function nl_owner_rest_build( WP_REST_Request $req ) {
	$uid  = get_current_user_id();
	$drop = (int) $req['drop'];
	if ( get_post_type( $drop ) !== 'nadlan_drop' || (string) get_post_meta( $drop, 'nl_owner_user', true ) !== (string) $uid ) {
		return new WP_Error( 'nf', 'לא נמצא.', array( 'status' => 404 ) );
	}
	if ( (string) get_post_meta( $drop, 'nl_draft_v', true ) === '2' ) { return new WP_Error( 'nf', 'לא נמצא.', array( 'status' => 404 ) ); }
	$state = (string) get_post_meta( $drop, 'nl_state', true );
	if ( ! in_array( $state, array( 'ready', 'writing', 'published', 'draft', 'pending' ), true ) ) { return new WP_Error( 'state', 'חסרים פרטים.', array( 'status' => 409 ) ); }
	$c    = json_decode( (string) get_post_meta( $drop, 'nl_owner_contact', true ), true );
	$b    = nl_owner_pseudo( $uid, $c['name'] ?? '', $c['phone'] ?? '' );
	$hold = (string) get_post_meta( $drop, 'nl_hold', true ) !== '';
	if ( $hold ) { $b['auto'] = false; }
	if ( (string) $req->get_param( 'test' ) === '1' && current_user_can( 'manage_options' ) ) { $b['auto'] = false; }
	@set_time_limit( 170 );
	$res = nl_drop_build( $drop, $b );
	if ( is_wp_error( $res ) && in_array( $res->get_error_code(), array( 'nl_drop_busy', 'nl_drop_fenced' ), true ) ) { return new WP_Error( 'busy', nl_owner_t( 'building', 'he' ), array( 'status' => 409 ) ); }
	if ( is_wp_error( $res ) ) { return new WP_Error( 'build', 'בניית העמוד נכשלה. אפשר לנסות שוב.', array( 'status' => 500 ) ); }
	if ( $hold && ! empty( $res['he_id'] ) && get_post_status( $res['he_id'] ) !== 'publish' ) {
		wp_update_post( array( 'ID' => (int) $res['he_id'], 'post_status' => 'pending' ) );
		$res['state'] = 'pending';
		update_post_meta( $drop, 'nl_state', 'pending' );
		@wp_mail( get_option( 'admin_email' ), '[nad-lan] מודעת בעלים ממתינה לבדיקה', 'הטקסט נעצר בבדיקת הפליה בדיור: ' . admin_url( 'post.php?post=' . (int) $res['he_id'] . '&action=edit' ) );
	}
	return $res;
}

/* ---------------- My listings ---------------- */
function nl_owner_rest_listings( WP_REST_Request $req ) {
	$uid  = get_current_user_id();
	$lang = nl_owner_req_lang( $req );
	$rows = array();
	foreach ( nl_owner_listings( $uid, false, true ) as $p ) {
		$st    = (string) get_post_meta( $p->ID, 'nl_status', true );
		$deal  = (string) get_post_meta( $p->ID, 'listing_type', true ) === 'rent' ? 'rent' : 'sale';
		$price = (int) get_post_meta( $p->ID, 'price', true );
		$drop  = (int) get_post_meta( $p->ID, 'nl_drop_id', true );
		$draft = $drop && (string) get_post_meta( $drop, 'nl_draft_v', true ) === '2' && (string) get_post_meta( $drop, 'nl_owner_user', true ) === (string) $uid ? $drop : 0;
		$state = $p->post_status === 'trash' ? 'removed' : ( $p->post_status === 'pending' ? 'pending' : ( $p->post_status === 'publish' ? ( in_array( $st, array( 'sold', 'rented' ), true ) ? $st : 'active' ) : 'draft' ) );
		$cover = (string) get_the_post_thumbnail_url( $p->ID, 'medium' );
		if ( $cover === '' && $draft ) {
			$dd = nl_owner_draft_get( $draft, $uid, true );
			if ( $dd && ! empty( $dd['photos'][0]['ref'] ) ) { $cover = nl_owner_img_url( $draft, (string) $dd['photos'][0]['ref'], 't' ); }
		}
		$rows[] = array(
			'id'       => (int) $p->ID,
			'title'    => html_entity_decode( get_the_title( $p ), ENT_QUOTES, 'UTF-8' ),
			'url'      => $p->post_status === 'publish' ? (string) get_permalink( $p ) : '',
			'cover'    => $cover,
			'deal'     => $deal,
			'state'    => $state,
			'status'   => in_array( $st, array( 'sold', 'rented' ), true ) ? $st : 'active',
			'price'    => $price ? nl_drop_price_text( $price, 'he' ) . ( $deal === 'rent' ? ' ' . nl_owner_t( 'month', $lang ) : '' ) : '',
			'price_raw'=> $price,
			'since'    => (int) get_post_time( 'U', true, $p->ID ),
			'changed'  => (int) get_post_modified_time( 'U', true, $p->ID ),
			'draft'    => $draft,
			'editable' => true,
			'live'     => $p->post_status === 'publish',
			'pending'  => $p->post_status === 'pending',
		);
	}
	$drafts  = array();
	foreach ( nl_owner_open_drafts( $uid ) as $id ) {
		$d = nl_owner_draft_get( $id, $uid );
		if ( $d ) { $drafts[] = nl_owner_draft_out( $d, $lang, false ); }
	}
	$deleted = array();
	foreach ( nl_owner_user_drafts( $uid, 'trash' ) as $id ) {
		$d = nl_owner_draft_get( $id, $uid, true );
		if ( $d && ! nl_owner_draft_listing( $id ) ) { $o = nl_owner_draft_out( $d, $lang, false ); $o['trashed_at'] = (int) get_post_meta( $id, '_wp_trash_meta_time', true ); $deleted[] = $o; }
	}
	$active = 0;
	foreach ( $rows as $r ) { if ( $r['state'] === 'active' ) { $active++; } }
	return nl_owner_nocache( array( 'listings' => $rows, 'drafts' => $drafts, 'deleted' => $deleted, 'active' => $active, 'max' => NL_OWNER_MAX_ACTIVE, 'listings_n' => count( $rows ) ) );
}

function nl_owner_rest_update( WP_REST_Request $req ) {
	$uid  = get_current_user_id();
	$lang = nl_owner_req_lang( $req );
	if ( nl_owner_rate( $uid, 'update', 60, HOUR_IN_SECONDS ) ) { return nl_owner_err( 'rate', 429, $lang ); }
	$id = (int) $req->get_param( 'id' );
	if ( get_post_type( $id ) !== 'nadlan_property' || (int) get_post_meta( $id, 'owner_user_id', true ) !== (int) $uid || (string) get_post_meta( $id, 'nl_owner', true ) !== '1' ) {
		return new WP_Error( 'nf', nl_owner_t( 'nf', $lang ), array( 'status' => 404 ) );
	}
	$act = (string) $req->get_param( 'action' );
	if ( $act === 'remove' ) {
		// off the site at once, kept in the owner's list (WordPress trash, restorable)
		if ( get_post_status( $id ) === 'trash' ) { return array( 'ok' => true, 'state' => 'removed' ); }
		if ( ! wp_trash_post( $id ) ) { return nl_owner_err( 'del_failed', 500, $lang ); }
		nl_drop_purge( array( $id ) );
		return array( 'ok' => true, 'state' => 'removed' );
	}
	if ( $act === 'republish' ) {
		if ( get_post_status( $id ) !== 'trash' ) { return array( 'ok' => true, 'state' => get_post_status( $id ) === 'publish' ? 'active' : 'pending' ); }
		if ( nl_owner_active_count( $uid ) >= NL_OWNER_MAX_ACTIVE ) { return nl_owner_err( 'cap', 409, $lang ); }
		add_filter( 'wp_untrash_post_status', 'wp_untrash_post_set_previous_status', 10, 3 );
		wp_untrash_post( $id );
		remove_filter( 'wp_untrash_post_status', 'wp_untrash_post_set_previous_status', 10 );
		$drop = (int) get_post_meta( $id, 'nl_drop_id', true );
		$hold = $drop && (string) get_post_meta( $drop, 'nl_hold', true ) !== '';
		wp_update_post( array( 'ID' => $id, 'post_status' => $hold ? 'pending' : 'publish' ) );
		update_post_meta( $id, 'nl_status', 'active' );
		update_post_meta( $id, 'status', 'active' );
		nl_drop_purge( array( $id ) );
		return array( 'ok' => true, 'state' => $hold ? 'pending' : 'active' );
	}
	if ( get_post_status( $id ) === 'trash' ) { return new WP_Error( 'nf', nl_owner_t( 'nf', $lang ), array( 'status' => 404 ) ); }
	if ( (string) $req->get_param( 'status' ) === 'active' && (string) get_post_meta( $id, 'nl_status', true ) !== 'active' && nl_owner_active_count( $uid ) >= NL_OWNER_MAX_ACTIVE ) {
		return nl_owner_err( 'cap', 409, $lang );
	}
	return nl_drop_apply_update( $id, nl_owner_from_listing( $id ), (string) $req->get_param( 'status' ), $req->get_param( 'price' ) );
}

/* Draft photos never leak through the media REST door: before publish they are not in the media library at all,
 * and an owner's listing photos are listed only for editors (they are shown on the listing page itself). */
add_filter( 'rest_attachment_query', function ( $args ) {
	if ( current_user_can( 'edit_others_posts' ) ) { return $args; }
	$mq   = isset( $args['meta_query'] ) && is_array( $args['meta_query'] ) ? $args['meta_query'] : array();
	$mq[] = array( 'key' => 'nl_owner_user', 'compare' => 'NOT EXISTS' );
	$args['meta_query'] = $mq;
	return $args;
} );

/* The create keys of drafts older than two days are not needed any more (WordPress' daily clean-up). */
add_action( 'wp_scheduled_delete', function () {
	global $wpdb;
	$rows = $wpdb->get_results( "SELECT option_name, option_value FROM {$wpdb->options} WHERE option_name LIKE 'nl\\_owner\\_ck\\_%' LIMIT 500" );
	foreach ( (array) $rows as $r ) {
		$parts = explode( '|', (string) $r->option_value );
		if ( time() - (int) ( $parts[1] ?? 0 ) > 2 * DAY_IN_SECONDS ) { delete_option( $r->option_name ); }
	}
} );

/* =====================================================================================================
 * The page: one app for the journey (account, draft, details, photos, preview, published, My listings, promotion)
 * ===================================================================================================== */
function nl_owner_page_lang( $atts ) {
	$a = is_array( $atts ) ? $atts : array();
	if ( isset( $a['lang'] ) ) { return nl_owner_lang( $a['lang'] ); }
	return nl_owner_lang( isset( $_GET['lang'] ) ? sanitize_key( wp_unslash( $_GET['lang'] ) ) : 'he' );   // phpcs:ignore
}

function nl_owner_shortcode( $atts = array() ) {
	if ( ! function_exists( 'nl_drop_build' ) ) { return ''; }
	$lang = nl_owner_page_lang( $atts );
	$he   = $lang === 'he';
	$uid  = get_current_user_id();
	$name = '';
	$phone = '';
	if ( $uid ) {
		$u     = wp_get_current_user();
		$name  = (string) get_user_meta( $uid, 'nl_owner_name', true );
		if ( $name === '' ) { $name = trim( (string) preg_split( '/\s+/u', (string) $u->display_name )[0] ); }
		if ( strpos( $name, '@' ) !== false ) { $name = ''; }
		$phone = (string) get_user_meta( $uid, 'nl_owner_phone', true );
		if ( $phone === '' ) { $phone = (string) get_user_meta( $uid, 'phone', true ); }
	}
	$page = (string) get_permalink();
	$cfg  = array(
		'api'       => esc_url_raw( rest_url( 'nadlan/v1/owner' ) ),
		'nonce'     => wp_create_nonce( 'wp_rest' ),
		'ajax'      => esc_url_raw( admin_url( 'admin-ajax.php' ) ),
		'uid'       => (int) $uid,
		'lang'      => $lang,
		'page'      => esc_url_raw( $page ),
		'name'      => $name,
		'prefill'   => array( 'cname' => $name, 'phone' => nl_owner_phone( $phone ) ),
		'maxActive' => NL_OWNER_MAX_ACTIVE,
		'maxPhotos' => NL_OWNER_MAX_PHOTOS,
		'maxBytes'  => NL_DROP_MAX_BYTES,
		'brokers'   => esc_url_raw( home_url( '/brokers/#join' ) ),
		'terms'     => esc_url_raw( home_url( '/terms/' ) ),
		'privacy'   => esc_url_raw( home_url( '/privacy/' ) ),
		// wp_logout_url() returns an HTML-escaped URL (&amp;); the app escapes once, into the href
		'logout'    => $uid ? html_entity_decode( wp_logout_url( add_query_arg( 'lang', $lang, $page ) ), ENT_QUOTES, 'UTF-8' ) : '',
		'engine'    => nl_owner_engine_ok(),
		'v'         => NL_OWNER_VERSION,
	);
	// what a visitor without the app (or a crawler) sees: the screen's words, no form
	$intro = $he
		? '<p class="nlj-kick">פרסום מודעה מבעלים</p><h2 class="nlj-h1">מפרסמים את הנכס שלכם</h2><p class="nlj-lead">פותחים חשבון בשם ובמייל, ממלאים את פרטי הנכס ומעלים תמונות. המודעה עולה בכתובת משלה. בלי עמלה.</p>'
		: '<p class="nlj-kick">List your property</p><h2 class="nlj-h1">List your property, owner to buyer</h2><p class="nlj-lead">Open an account with your name and email, fill in the property details and add photos. The listing goes live at its own address. No commission.</p>';
	$h  = '<style id="nlj-css">' . nl_owner_css() . '</style>';
	$h .= '<section class="nlj alignfull" id="nlj-app" dir="' . ( $he ? 'rtl' : 'ltr' ) . '" lang="' . $lang . '" data-v="' . esc_attr( NL_OWNER_VERSION ) . '">';
	$h .= '<div class="nlj-wrap"><div class="nlj-intro">' . $intro . '<noscript><p class="nlj-note">' . ( $he ? 'הפרסום עובד בדפדפן עם JavaScript פעיל.' : 'Publishing works in a browser with JavaScript on.' ) . '</p></noscript></div></div></section>';
	// the app's script goes to the footer, past the content filters (a theme's texturize can turn && into &#038;&#038;)
	$GLOBALS['nl_owner_cfg'] = $cfg;
	if ( ! has_action( 'wp_footer', 'nl_owner_footer' ) ) { add_action( 'wp_footer', 'nl_owner_footer', 20 ); }
	return $h;
}

function nl_owner_footer() {
	if ( empty( $GLOBALS['nl_owner_cfg'] ) ) { return; }
	echo '<script>window.NLOWNER=' . wp_json_encode( $GLOBALS['nl_owner_cfg'], JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES | JSON_HEX_TAG | JSON_HEX_AMP ) . ';</script>' . "\n";   // phpcs:ignore
	echo '<script id="nlj-js">' . nl_owner_js() . '</script>' . "\n";   // phpcs:ignore
	unset( $GLOBALS['nl_owner_cfg'] );
}

function nl_owner_css() {
	return <<<'NLJCSS'
/* the site's floating "ייעוץ חינם" bar (#nlcta, inc/conversion-cta.php) sits fixed in the bottom corner. On this page it stays
   at its resting place (--nlcta-band: the site's own switch that stops its lifts, ConsultBand v104.25; a lift would put it over
   the fields above a form button), the page keeps room for it below the last control, and a focused field, link or button is
   scrolled above it (WCAG 2.4.11), also when a phone keyboard shrinks the screen. --nlj-bar-room is measured by the app. */
body:has(#nlj-app){--nlcta-band:1}
html:has(#nlj-app){scroll-padding-bottom:var(--nlj-bar-room,112px);scroll-padding-top:24px}
.nlj{--paper:#f7f6f2;--surf:#fff;--ink:#14212b;--ink2:#3b4753;--mute:#6b7680;--line:#e3e1da;--sea:#2f6f86;--seah:#255c70;--deep:#1f4b5c;--sand:#eee9dd;--champ:#cfe3ea;--wa:#0f7a63;--field:#fbfaf7;--bad:#b3261e;--badg:#fbedec;--ok:#2e7d5b;--okg:#eaf4ef;
  font-family:Assistant,"Segoe UI",Arial,sans-serif;font-size:15px;line-height:1.5;color:var(--ink2);background:var(--paper);box-sizing:border-box;position:relative;max-width:none!important;margin-inline:0!important;width:100%}
.nlj *,.nlj *::before,.nlj *::after{box-sizing:border-box}
.nlj [hidden]{display:none!important}
.nlj h1,.nlj h2,.nlj h3,.nlj .nlj-h1,.nlj .nlj-serif{font-family:"Noto Serif Hebrew","David Libre",Georgia,serif!important;font-weight:600;color:var(--ink)!important;letter-spacing:-.005em;text-wrap:balance;margin:0}
.nlj .nlj-h1{font-size:30px;line-height:1.15}
.nlj h2{font-size:21px;line-height:1.2}
.nlj h3{font-size:18px;line-height:1.25}
.nlj p{margin:0}
.nlj a{color:var(--sea);text-underline-offset:3px}
.nlj a:hover{color:var(--seah)}
.nlj-num{unicode-bidi:isolate;direction:ltr;display:inline-block}
.nlj-wrap{max-width:1240px;margin-inline:auto;padding-inline:16px;padding-block:16px calc(var(--nlj-bar-room,112px) + 24px);display:flex;flex-direction:column;gap:18px}
.nlj-bar{display:flex;align-items:center;justify-content:flex-end;gap:8px;min-height:48px}
.nlj-avatar{width:36px;height:36px;border-radius:999px;background:var(--deep);color:#fff;display:grid;place-items:center;font-weight:700;font-size:15px;flex:none}
.nlj-cols{display:flex;flex-wrap:wrap;gap:24px;align-items:flex-start}
.nlj-main{flex:999 1 560px;min-width:0;display:flex;flex-direction:column;gap:18px}
.nlj-aside{flex:1 1 320px;min-width:0;display:none;flex-direction:column;gap:16px}
.nlj-card{background:var(--surf);border:1px solid var(--line);border-radius:16px;padding:20px;display:flex;flex-direction:column;gap:18px}
.nlj-card--sand{background:var(--sand);border-color:transparent}
.nlj-lead{font-size:17px;line-height:1.55;color:var(--ink2);max-width:60ch}
.nlj-kick{font-size:13px;font-weight:700;color:var(--deep);letter-spacing:.02em}
.nlj-small{font-size:14px;line-height:1.45;color:var(--ink2)}
.nlj-meta{font-size:13.5px;color:var(--ink2)}
.nlj-hr{height:1px;background:var(--line);border:0;margin:0;width:100%}
.nlj-head{display:flex;flex-direction:column;gap:8px}
.nlj-head:focus{outline:none}
.nlj-prog5{display:flex;flex-direction:column;gap:8px}
.nlj-prog5-top{display:flex;justify-content:space-between;align-items:baseline;gap:12px;font-size:14px}
.nlj-prog5-top b{color:var(--ink);font-size:15px}
.nlj-bars{display:flex;gap:6px}
.nlj-bars i{flex:1;height:6px;border-radius:999px;background:var(--line)}
.nlj-bars i.is-done{background:var(--sea)}
.nlj-bars i.is-now{background:var(--deep)}
.nlj-steps{list-style:none;margin:0;padding:0;display:flex;flex-direction:column;gap:2px}
.nlj-steps li{display:flex;align-items:center;gap:12px;min-height:40px;font-size:15px;color:var(--ink2);margin:0}
.nlj-steps li .nlj-dot{width:26px;height:26px;border-radius:999px;border:1px solid var(--line);background:var(--surf);display:grid;place-items:center;font-size:13px;font-weight:700;color:var(--ink2);flex:none}
.nlj-steps li.is-done .nlj-dot{background:var(--sea);border-color:var(--sea);color:#fff}
.nlj-steps li.is-now{color:var(--ink);font-weight:700}
.nlj-steps li.is-now .nlj-dot{border:2px solid var(--deep);color:var(--deep)}
.nlj-status{display:flex;gap:10px;align-items:flex-start;border-radius:14px;padding:12px 14px;font-size:14px;line-height:1.45;background:var(--surf);border:1px solid var(--line);color:var(--ink2)}
.nlj-status b{color:var(--ink);display:block;font-size:14.5px}
.nlj-st-ico{flex:none;width:22px;height:22px;color:var(--deep);margin-top:1px}
.nlj-status--ok{background:var(--okg);border-color:transparent}
.nlj-status--ok .nlj-st-ico{color:var(--ok)}
.nlj-status--warn{background:var(--sand);border-color:transparent}
.nlj-status--bad{background:var(--badg);border-color:transparent}
.nlj-status--bad .nlj-st-ico{color:var(--bad)}
.nlj-status-acts{display:flex;flex-wrap:wrap;gap:8px;margin-top:10px}
.nlj-diff{margin:8px 0 0;padding-inline-start:18px;font-size:13.5px}
.nlj-diff li{margin:2px 0}
.nlj-form{display:flex;flex-direction:column;gap:18px}
.nlj-field{display:flex;flex-direction:column;gap:6px;min-width:0}
.nlj-label{font-size:15px;font-weight:700;color:var(--ink)}
.nlj-opt{font-weight:400;color:var(--ink2)}
.nlj-hint{font-size:13.5px;line-height:1.5;color:var(--ink2)}
.nlj-input{width:100%;height:48px;border:1px solid #858c93;border-radius:10px;background:var(--field);padding-inline:14px;font:inherit;font-size:16px;color:var(--ink);margin:0}
.nlj-input::placeholder{color:#59636d;opacity:1}
.nlj-input:focus-visible,.nlj-input:focus{outline:3px solid var(--sea);outline-offset:1px;border-color:transparent}
.nlj-input.is-bad{border-color:var(--bad);background:var(--surf)}
.nlj-input.is-ltr{direction:ltr;text-align:end}
.nlj[dir="ltr"] .nlj-input.is-ltr{text-align:start}
textarea.nlj-input{height:auto;min-height:150px;padding-block:12px;line-height:1.55;resize:vertical}
select.nlj-input{appearance:auto}
.nlj-affix{position:relative}
.nlj-affix .nlj-input{padding-inline-end:56px}
.nlj-affix span{position:absolute;inset-inline-end:14px;top:50%;transform:translateY(-50%);color:var(--ink2);font-size:15px;pointer-events:none}
.nlj-pw{display:flex;gap:8px}
.nlj-pw .nlj-input{flex:1;min-width:0}
.nlj-err{display:flex;gap:8px;align-items:flex-start;background:var(--badg);color:var(--bad);border-radius:10px;padding:8px 12px;font-size:14px;font-weight:600;line-height:1.45}
.nlj-err svg{flex:none;margin-top:2px}
.nlj-errsum{border:2px solid var(--bad);border-radius:12px;padding:12px 14px;background:var(--surf);color:var(--ink)}
.nlj-errsum:focus{outline:3px solid var(--sea);outline-offset:2px}
.nlj-errsum ul{margin:6px 0 0;padding-inline-start:20px}
.nlj-errsum a{font-weight:600}
.nlj-note{display:flex;gap:10px;align-items:flex-start;background:var(--sand);color:var(--ink);border-radius:12px;padding:12px 14px;font-size:14px;line-height:1.5}
.nlj-note svg{flex:none;margin-top:2px;color:var(--deep)}
.nlj-g2{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px}
.nlj-g3{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px}
.nlj-counter{display:flex;justify-content:space-between;gap:8px;font-size:13px;color:var(--ink2)}
.nlj-seg{display:flex;flex-wrap:wrap;gap:8px}
.nlj-pill{min-height:44px;padding-inline:18px;border-radius:999px;border:1px solid #858c93;background:var(--surf);font:inherit;font-size:15px;font-weight:700;color:var(--deep);cursor:pointer}
.nlj-pill[aria-pressed="true"]{background:var(--sea);border-color:var(--sea);color:#fff}
.nlj-check{display:flex;gap:12px;align-items:flex-start;min-height:44px;padding-block:8px;cursor:pointer;font-size:15px;color:var(--ink);font-weight:400}
.nlj-check input{width:22px;height:22px;margin:1px 0 0;accent-color:var(--sea);flex:none}
.nlj-check small{display:block;font-size:13.5px;color:var(--ink2);margin-top:2px}
.nlj-tabs{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:6px;background:var(--sand);border-radius:999px;padding:4px}
.nlj-tab{min-height:44px;border-radius:999px;border:0;background:none;font:inherit;font-size:15px;font-weight:700;color:var(--ink2);cursor:pointer;padding-inline:8px}
.nlj-tab[aria-pressed="true"]{background:var(--surf);color:var(--ink);box-shadow:0 1px 2px rgba(20,33,43,.08)}
.nlj-btn{min-height:52px;padding-inline:24px;border-radius:999px;border:1px solid transparent;font:inherit;font-size:16px;font-weight:700;display:inline-flex;align-items:center;justify-content:center;gap:10px;cursor:pointer;text-decoration:none!important;line-height:1.2;text-align:center}
.nlj-btn--primary{background:var(--sea);color:#fff!important}
.nlj-btn--primary:hover{background:var(--seah);color:#fff}
.nlj-btn--secondary{background:var(--surf);border-color:#858c93;color:var(--deep)!important}
.nlj-btn--secondary:hover{background:var(--sand)}
.nlj-btn--quiet{background:none;color:var(--sea)!important;min-height:44px;padding-inline:8px;text-decoration:underline!important;text-underline-offset:3px}
.nlj-btn--danger{background:var(--surf);border-color:var(--bad);color:var(--bad)!important}
.nlj-btn--bad{color:var(--bad)!important}
.nlj-btn--sm{min-height:44px;font-size:15px;padding-inline:18px}
.nlj-btn[disabled],.nlj-btn[aria-disabled="true"]{background:#e3e1da;border-color:#e3e1da;color:#3b4753!important;cursor:not-allowed}
.nlj-btn:focus-visible,.nlj-pill:focus-visible,.nlj-tab:focus-visible,.nlj-ibtn:focus-visible,.nlj a:focus-visible,.nlj-check input:focus-visible,.nlj summary:focus-visible{outline:2px solid var(--sea);outline-offset:3px}
.nlj-ibtn{width:44px;height:44px;border-radius:999px;border:1px solid #858c93;background:var(--surf);color:var(--deep);display:grid;place-items:center;cursor:pointer;flex:none;padding:0}
.nlj-ibtn[disabled]{opacity:.45;cursor:not-allowed}
.nlj-actions{display:flex;flex-direction:column;gap:10px}
.nlj-actions .nlj-btn{width:100%}
.nlj[dir="rtl"] .nlj-fwd{transform:scaleX(-1)}
.nlj-drop{border:1.5px dashed var(--sea);border-radius:16px;background:var(--surf);padding:20px;display:flex;flex-direction:column;align-items:center;gap:10px;text-align:center}
.nlj-drop.is-over{background:var(--champ)}
.nlj-file{position:absolute;width:1px;height:1px;opacity:0;overflow:hidden;clip:rect(0 0 0 0)}
.nlj-ph{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px;list-style:none;margin:0;padding:0}
.nlj-ph>li{margin:0}
.nlj-tile{background:var(--surf);border:1px solid var(--line);border-radius:14px;overflow:hidden;display:flex;flex-direction:column;height:100%}
.nlj-tile.is-fail{border-color:var(--bad)}
.nlj-img{aspect-ratio:4/3;background:var(--sand);position:relative;display:grid;place-items:center;color:var(--deep);overflow:hidden}
.nlj-img img{width:100%;height:100%;object-fit:cover;display:block}
.nlj-img svg{width:56%;height:auto;opacity:.85}
.nlj-cap{position:absolute;inset-block-end:8px;inset-inline-start:8px;background:rgba(20,33,43,.78);color:#fff;border-radius:6px;padding:3px 8px;font-size:12px;line-height:1.4}
.nlj-cover{position:absolute;inset-block-start:8px;inset-inline-start:8px;background:var(--deep);color:#fff;border-radius:999px;padding:4px 10px;font-size:12px;font-weight:700}
.nlj-tilebar{display:flex;align-items:center;justify-content:space-between;gap:6px;padding:8px;flex-wrap:wrap}
.nlj-grp{display:flex;gap:6px}
.nlj-up{padding:10px 12px;display:flex;flex-direction:column;gap:8px;font-size:13.5px;color:var(--ink)}
.nlj-upbar{height:6px;border-radius:999px;background:var(--line);overflow:hidden}
.nlj-upbar i{display:block;height:100%;background:var(--sea);border-radius:999px;width:0;transition:width .2s}
.nlj-fail{padding:10px 12px;display:flex;flex-direction:column;gap:8px;font-size:13.5px;color:var(--bad);font-weight:600}
.nlj-fail .nlj-grp,.nlj-up .nlj-grp,.nlj-tilebar .nlj-grp{flex-wrap:wrap}
.nlj-fail .nlj-btn{padding-inline:12px}
.nlj-banner{display:flex;gap:10px;align-items:center;background:var(--champ);color:var(--ink);border-radius:12px;padding:12px 14px;font-size:14.5px;font-weight:600}
.nlj-lcard{background:var(--surf);border:1px solid var(--line);border-radius:16px;overflow:hidden}
.nlj-lbody{padding:18px;display:flex;flex-direction:column;gap:12px}
.nlj-price{font-size:30px;line-height:1.1;font-weight:800;color:var(--ink);font-variant-numeric:tabular-nums lining-nums}
.nlj-facts{display:flex;flex-wrap:wrap;gap:8px}
.nlj-fact{display:inline-flex;align-items:center;gap:6px;min-height:34px;padding-inline:12px;border-radius:999px;background:var(--sand);color:var(--ink);font-size:14px;font-weight:600}
.nlj-chip{display:inline-flex;align-items:center;gap:6px;min-height:28px;padding-inline:10px;border-radius:999px;background:var(--sand);color:var(--ink);font-size:13px;font-weight:700;white-space:nowrap}
.nlj-chip--live{background:var(--okg);color:#226347}
.nlj-chip--owner{background:var(--champ);color:var(--deep)}
.nlj-chip--off{background:var(--sand);color:var(--ink2)}
.nlj-chip--warn{background:#fbf3e4;color:#7a5410}
.nlj-urlbox{display:flex;gap:8px;align-items:center;border:1px solid var(--line);border-radius:12px;background:var(--field);padding-block:6px;padding-inline:12px 6px;min-height:52px}
.nlj-urlbox code{flex:1;min-width:0;overflow-wrap:anywhere;font-family:ui-monospace,Consolas,monospace;font-size:13.5px;color:var(--ink);direction:ltr;text-align:start;background:none;padding:0}
.nlj-full{border:1px solid var(--line);border-radius:16px;background:var(--surf)}
.nlj-full>summary{min-height:52px;display:flex;align-items:center;padding-inline:18px;font-weight:700;color:var(--deep);cursor:pointer}
.nlj-full .nlj-fullbody{padding:0 8px 8px;overflow:hidden}
.nlj-mine{display:flex;flex-direction:column;gap:14px;list-style:none;margin:0;padding:0}
.nlj-mine>li{margin:0}
.nlj-item{background:var(--surf);border:1px solid var(--line);border-radius:16px;padding:14px;display:flex;flex-direction:column;gap:12px}
.nlj-item--off{background:var(--paper)}
.nlj-item-top{display:flex;gap:12px;align-items:flex-start}
.nlj-thumb{width:88px;aspect-ratio:4/5;border-radius:12px;background:var(--sand);display:grid;place-items:center;color:var(--deep);flex:none;overflow:hidden}
.nlj-thumb img{width:100%;height:100%;object-fit:cover}
.nlj-thumb svg{width:60%}
.nlj-item-acts{display:flex;flex-wrap:wrap;gap:8px}
.nlj-confirm{border-radius:12px;background:var(--badg);padding:14px;display:flex;flex-direction:column;gap:10px;color:var(--ink)}
.nlj-confirm b{color:var(--bad)}
.nlj-inline{display:flex;flex-wrap:wrap;gap:8px;align-items:flex-end}
.nlj-inline .nlj-field{flex:1 1 180px}
.nlj-okmark{width:64px;height:64px;border-radius:999px;background:var(--okg);color:var(--ok);display:grid;place-items:center}
.nlj-okmark--warn{background:#fbf3e4;color:#7a5410}
.nlj-deleted>summary{min-height:44px;display:flex;align-items:center;font-weight:700;color:var(--deep);cursor:pointer}
.nlj-loading{min-height:120px;display:grid;place-items:center;color:var(--ink2)}
.nlj-sr{position:absolute!important;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}
@media (max-width:480px){.nlj-g3{grid-template-columns:repeat(2,minmax(0,1fr))}.nlj-g3>:last-child{grid-column:1/-1}}
@media (max-width:359px){.nlj .nlj-h1{font-size:27px}.nlj-g2{grid-template-columns:minmax(0,1fr)}.nlj-card{padding:16px}.nlj-wrap{padding-inline:12px}}
@media (min-width:1024px){
 .nlj-wrap{padding-inline:32px;padding-block:28px calc(var(--nlj-bar-room,112px) + 32px);gap:24px}
 .nlj .nlj-h1{font-size:40px;line-height:1.1}
 .nlj-card{padding:28px;gap:22px}
 .nlj-actions{flex-direction:row;flex-wrap:wrap;align-items:center}
 .nlj-actions .nlj-btn{width:auto}
 .nlj-ph{grid-template-columns:repeat(3,minmax(0,1fr))}
 .nlj-lbody{padding:26px}
 .nlj-aside{display:flex}
}
NLJCSS;
}

function nl_owner_js() {
	return <<<'NLJS'
(function(){
'use strict';
var C=window.NLOWNER||{};
var root=document.getElementById('nlj-app');
if(!root||!C.api){return;}
var LANG=C.lang==='en'?'en':'he',HE=LANG==='he';
var TAB=Math.random().toString(36).slice(2);
var MAXP=C.maxPhotos||30,MAXB=C.maxBytes||15728640;

/* ---------------- words (HE first; EN is a full translation) ---------------- */
var W={he:{
 myListings:'המודעות שלי',signInTop:'כניסה',navAria:'החשבון שלי',acct:function(n){return 'מחוברים בתור '+n;},
 authKick:'פרסום מודעה מבעלים',authH1:'מפרסמים את הנכס שלכם',authLead:'פותחים חשבון בשם ובמייל, ממלאים את פרטי הנכס ומעלים תמונות. המודעה עולה בכתובת משלה. בלי עמלה.',
 authTabsAria:'פתיחת חשבון או כניסה',tabSignup:'פתיחת חשבון',tabLogin:'כבר יש לי חשבון',firstName:'שם פרטי',email:'מייל',password:'סיסמה',showPw:'הצגה',hidePw:'הסתרה',showPwAria:'הצגת הסיסמה',
 pwHint:'8 תווים לפחות. אפשר להחליף אותה בכל זמן.',termsA:'בפתיחת החשבון אתם מסכימים ל',terms:'תנאי השימוש',termsB:'ול',privacy:'מדיניות הפרטיות',
 signupCta:'פתיחת חשבון והמשך',signupBusy:'פותחים חשבון…',mailExistsAct:'כניסה עם המייל הזה',loginCta:'כניסה',loginBusy:'נכנסים…',forgot:'שכחתי את הסיסמה',
 recH:'איפוס סיסמה',recLead:'כתבו את המייל של החשבון. אם הוא רשום אצלנו, נשלח אליו קישור לבחירת סיסמה חדשה.',recSend:'שליחת קישור לאיפוס',recWait:function(n){return 'אפשר לשלוח שוב בעוד '+n+' שניות';},
 recSentH:'אם המייל רשום אצלנו, הקישור בדרך.',recSent:' הקישור תקף לזמן מוגבל. לא הגיע? בדקו גם בתיקיית הספאם.',backLogin:'חזרה לכניסה',
 brokerLine:'מתווכים מפרסמים מהאתר שלהם.',brokerLink:'לאתר המתווכים שלכם',howAria:'מה קורה אחרי ההרשמה',howH:'מה קורה אחר כך',how1:'פרטי הנכס, כמה דקות',how2:'עד 30 תמונות מהטלפון',how3:'תצוגה מקדימה ופרסום',
 howNote:'אפשר לעצור בכל שלב. הטיוטה נשמרת בחשבון ומחכה לכם.',netErr:'אין חיבור. מה שכתבתם נשמר בטופס; נסו שוב.',genericErr:'משהו השתבש. מה שכתבתם נשמר; נסו שוב.',
 draftKick:function(n){return n?'ברוכים השבים, '+n:'ברוכים השבים';},draftH1:'יש לכם טיוטה שמורה',draftLead:'המשיכו מהמקום שעצרתם. מה שמילאתם נשמר בחשבון.',chipDraft:'טיוטה',
 draftSaved:function(d){return 'נשמרה בחשבון ב־'+d;},draftStep:function(n){return 'שלב '+n+' מתוך 5';},draftNext:function(s){return 'הבא: '+s;},draftContinue:'המשך מהמקום שעצרתם',draftNew:'מודעה חדשה',
 draftNewNote:'פתיחת מודעה חדשה לא מוחקת את הטיוטה הזו. היא נשארת ברשימה במודעות שלי.',draftDelete:'מחיקת הטיוטה',delAskH:'למחוק את הטיוטה?',delAskTxt:'הטיוטה תעבור לפריטים שנמחקו ותיעלם מהרשימה. אפשר יהיה לשחזר אותה משם.',
 delYes:'מחיקה',cancel:'ביטול',delRunH:'מוחקים את הטיוטה',delRunTxt:' היא נשארת כאן עד שהשרת מאשר את ההעברה. אם החיבור ייפול, שום דבר לא יימחק.',delFailH:'הטיוטה לא נמחקה',delFail:' השרת לא אישר את המחיקה, והטיוטה נשארה כמו שהיא.',
 otherDrafts:function(n){return n===1?'יש לכם עוד טיוטה אחת במודעות שלי.':'יש לכם עוד '+n+' טיוטות במודעות שלי.';},
 stDeviceH:'נשמר במכשיר הזה',stDevice:' עוד לא בחשבון. הפרטים יישמרו בחשבון בעוד רגע.',stDeviceNoStore:' (השמירה במכשיר חסומה בדפדפן הזה, אז עד אז הם רק בדף הפתוח.)',stSavingH:'שומרים בחשבון…',stSaving:' מה שכתבתם כבר שמור במכשיר הזה.',
 stAccountH:'נשמר בחשבון',stAccount:function(t){return ' השמירה האחרונה ב־'+t+'. אפשר לעצור ולהמשיך מכל מכשיר.';},stNewH:'טיוטה חדשה',stNew:' עוד לא נשמר כלום. מה שתכתבו יישמר בחשבון תוך כדי.',
 stOfflineH:'אין חיבור לאינטרנט',stOffline:' מה שתכתבו נשמר במכשיר הזה ויישלח לחשבון כשהחיבור יחזור. אל תסגרו את הדף עד אז.',stOfflineNoStore:' השמירה במכשיר חסומה בדפדפן הזה, אז מה שתכתבו נמצא רק בדף הפתוח. אל תסגרו אותו עד שהחיבור יחזור.',
 stRetryH:'השמירה בחשבון לא הצליחה',stRetry:function(n){return ' הפרטים שמורים במכשיר הזה. ננסה שוב בעוד '+n+' שניות.';},stRetryNoStore:function(n){return ' הפרטים נמצאים בדף הפתוח. ננסה שוב בעוד '+n+' שניות.';},retryNow:'לנסות עכשיו',
 conflictH:'הטיוטה פתוחה גם בלשונית אחרת',conflictTxt:function(t){return ' שם נשמר שינוי ב־'+t+'. כדי לא לדרוס אותו, בחרו עם איזו גרסה להמשיך.';},conflictLoad:'לטעון את הגרסה מהלשונית האחרת',conflictKeep:'להמשיך כאן ולשמור את הגרסה הזו',
 conflictDiff:'מה שונה:',here:'כאן',there:'שם',empty:'ריק',loadedH:'נטענה הגרסה מהלשונית האחרת',loadedTxt:' הגרסה שהייתה כאן לא נמחקה, ואפשר לחזור אליה.',backToMine:'חזרה לגרסה שהייתה כאן',
 perAccount:'טיוטות נשמרות לכל חשבון בנפרד. אם התחלתם מודעה בחשבון אחר במכשיר הזה, היכנסו אליו כדי להמשיך אותה.',otherAccount:'כניסה לחשבון אחר',
 expiredH:'צריך להיכנס שוב',expiredTxt:' החיבור לחשבון הסתיים. מה שכתבתם שמור במכשיר הזה, ויישמר בחשבון אחרי הכניסה.',expiredTxtNoStore:' החיבור לחשבון הסתיים. אל תסגרו את הדף: מה שכתבתם נמצא בו, וייכנס לחשבון אחרי הכניסה בלשונית אחרת.',expiredBtn:'כניסה',
 nostoreH:'השמירה במכשיר חסומה בדפדפן הזה',nostore:' השינויים נשמרים רק בחשבון, כשיש חיבור. אל תסגרו את הדף לפני שמופיע ״נשמר בחשבון״.',
 goneH:'הטיוטה לא נמצאת',goneTxt:' ייתכן שנמחקה בלשונית אחרת. מה שכתבתם עדיין כאן.',goneNew:'לשמור כטיוטה חדשה',publishingH:'המודעה בפרסום כרגע',publishingTxt:' בודקים שוב בעוד רגע. מה שכתבתם שמור.',
 progAria:'התקדמות הפרסום',stepNames:['חשבון','פרטי הנכס','תמונות','תצוגה מקדימה','פרסום'],stepOf:function(n){return 'שלב '+n+' מתוך 5';},
 detH1:'פרטי הנכס',detLead:'כמה פרטים בסיסיים. אפשר לעצור בכל שלב ולהמשיך אחר כך מאותו מקום.',dealType:'סוג העסקה',sale:'מכירה',rent:'השכרה',propType:'סוג הנכס',ptChoose:'בחירה',
 ptApt:'דירה',ptGarden:'דירת גן',ptPh:'פנטהאוז',ptDuplex:'דופלקס',ptHouse:'בית פרטי',city:'עיר',hood:'שכונה',addrHint:'רחוב ומספר בית לא מתפרסמים. במודעה ובכתובת שלה מופיעות העיר והשכונה בלבד.',
 rooms:'חדרים',size:'שטח',sqm:'מ״ר',floor:'קומה',optional:'(לא חובה)',floorHint:'לדוגמה 3, או 3 מתוך 8',priceSale:'מחיר מבוקש',priceRent:'שכר דירה לחודש',priceHint:'בספרות בלבד. אפשר לעדכן אותו אחר כך מהמודעות שלי.',
 desc:'כמה מילים על הנכס',descHint:'מה חשוב לדעת: מרפסת, חניה, מעלית, מצב הדירה.',fairNote:'ניסוח שמגביל לפי דת, מוצא, מוגבלות או מצב משפחתי עוצר את המודעה לבדיקה לפני פרסום.',
 contactH:'איך פונים אליכם',contactName:'שם להצגה',phone:'טלפון',phoneOpt:'(לא חובה אם לא מפרסמים אותו)',showPhone:'אני מסכים לפרסם את מספר הטלפון שלי במודעה',
 showPhoneSub:'המספר יוצג במודעה, וגם כפתורי הוואטסאפ והחיוג חושפים אותו למי שלוחץ. בלי סימון, המספר לא יופיע במודעה ולא יהיו בה כפתורי וואטסאפ וחיוג.',
 ownerDecl:'אני בעל הנכס או מורשה לפרסם אותו',ownerDeclSub:'חובה לפני פרסום.',toPhotos:'המשך לתמונות',saveExit:'שמירה ויציאה',checking:'בודקים…',
 errSumH:function(n){return n===1?'יש פרט אחד לתיקון':'יש '+n+' פרטים לתיקון';},brokerHint:'מתווכים? לכם יש אתר משלכם וקישור אישי להעלאת נכסים, בחינם:',
 phH1:'תמונות',phLead:'עד 30 תמונות. התמונה הראשונה היא תמונת השער של המודעה.',addPhotos:'הוספת תמונות',phDropHint:'מהטלפון או מהמחשב. JPG, PNG, WebP או HEIC, עד 15 מ״ב לתמונה. נתוני המיקום שבקובץ נמחקים לפני השמירה.',
 phCount:function(n,m){return n+' מתוך '+m;},phOrderHint:'משנים סדר בחיצים, וקובעים תמונת שער בכוכב. הכפתורים עובדים גם מהמקלדת.',phListAria:'התמונות של המודעה',coverBadge:'תמונת שער',
 photoN:function(n){return 'תמונה '+n;},uploading:'מעלים',upFail:'התמונה לא עלתה.',tryAgain:'לנסות שוב',earlier:'הזזה קדימה: ',later:'הזזה אחורה: ',makeCover:'קביעה כתמונת שער: ',remove:'הסרה: ',
 toPreview:'המשך לתצוגה מקדימה',backDetails:'חזרה לפרטי הנכס',waitUploads:'מחכים שהתמונות יסיימו לעלות.',failedLeft:function(n){return n===1?'תמונה אחת לא עלתה: אפשר לנסות שוב או להסיר אותה. היא לא תופיע במודעה.':n+' תמונות לא עלו: אפשר לנסות שוב או להסיר אותן. הן לא יופיעו במודעה.';},
 tooMany:'אפשר עד 30 תמונות למודעה. התמונות העודפות לא נוספו.',photosNeedDraft:'שומרים קודם את פרטי הנכס…',
 upErr:{big:'התמונה גדולה מ-15 מ״ב.',type:'הקובץ אינו תמונה שאפשר להעלות: JPG, PNG, WebP או HEIC.',heic:'את קובץ ה-HEIC הזה אי אפשר לנקות כאן מנתוני המיקום. שומרים אותו כ-JPG ומעלים שוב.',corrupt:'הקובץ פגום ולא נפתח כתמונה.',orient:'התמונה שמורה מסובבת, והשרת לא יכול להחזיר אותה ליושר. שומרים אותה מחדש ומעלים שוב.',auth:'החיבור לחשבון פג. נכנסים שוב, והתמונה תעלה בניסיון הבא.',rate:'הרבה תמונות בשעה האחרונה. נסו שוב בעוד כמה דקות.',server:'תקלה בשרת. אפשר לנסות שוב.',timeout:'ההעלאה לקחה יותר מדי זמן. בדקו את החיבור ונסו שוב.',net:'אין חיבור. נסו שוב כשהחיבור יחזור.'},
 pvH1:'תצוגה מקדימה',pvLead:'ככה המודעה תיראה באתר. בדקו את הפרטים לפני הפרסום.',pvBanner:'תצוגה מקדימה. המודעה עוד לא פורסמה.',pvBannerEdit:'תצוגה מקדימה של השינויים. המודעה באוויר נשארת כמו שהיא עד העדכון.',
 pvAria:'תצוגה מקדימה של המודעה',pvCap:'תמונת שער',fromOwner:'מבעלי הנכס',wa:'וואטסאפ',call:'חיוג',pvBtnsNote:'כפתורי הפנייה יעבדו אחרי הפרסום. הם חושפים את המספר שהסכמתם לפרסם.',
 pvNoContact:'לא סימנתם הסכמה לפרסם את הטלפון, ולכן במודעה אין מספר ואין כפתורי וואטסאפ וחיוג.',pvHold:'ניסוח בתיאור יעצור את המודעה לבדיקה של אדם לפני שהיא עולה לאתר.',pvLangNote:'',
 pvAddr:'הכתובת של המודעה',pvAddrHint:'כתובת קבועה באותיות לטיניות: העיר, החדרים וסוג העסקה. בלי רחוב ובלי מספר.',pvAddrLive:'הכתובת של המודעה לא משתנה בעדכון.',
 publish:'פרסום המודעה',update:'עדכון המודעה',backEdit:'חזרה לעריכה',publishNote:'אפשר לערוך, לעדכן מחיר או להסיר את המודעה בכל זמן מהמודעות שלי.',
 sendingH:'מפרסמים את המודעה',sendingTxt:' מחכים לאישור מהשרת. אם החיבור נופל, בדקו במודעות שלי לפני ששולחים שוב.',sendingLabel:'מפרסמים…',buildingH:'המודעה בבנייה',buildingTxt:' השרת עוד עובד עליה. בודקים שוב בעוד כמה שניות.',
 lostH:'החיבור נפל לפני שהגיעה תשובה',lostTxt:' ייתכן שהמודעה כבר פורסמה. בדקו במודעות שלי, או בדקו שוב כאן: אותה בקשה נשלחת שוב.',checkAgain:'לבדוק שוב',
 pvFull:'לראות את עמוד המודעה המלא',pvErrH:'לפני הפרסום צריך לתקן:',fix:'לתיקון',pvOffline:'אין חיבור, ולכן אין תצוגה מקדימה כרגע. מה שכתבתם שמור.',pvLoading:'מכינים את התצוגה המקדימה…',
 doneH1:'המודעה באוויר',doneUpdatedH1:'המודעה עודכנה',doneLead:function(d){return 'המודעה שלכם פורסמה ב־'+d+'.';},doneUpdatedLead:'השינויים כבר בעמוד המודעה.',
 donePendingH1:'המודעה נשמרה ותעלה אחרי בדיקה קצרה',donePendingLead:'חלק מהניסוח דורש בדיקה של אדם לפני פרסום. המודעה לא מוצגת באתר עד הבדיקה.',doneDraftH1:'המודעה נשמרה כטיוטה',doneDraftLead:'היא לא מוצגת באתר.',
 copyLink:'העתקה',copied:'הקישור הועתק',toListing:'לעמוד המודעה',shareWa:'שיתוף בוואטסאפ',doneManage:'נמכר או הושכר? מסמנים בלחיצה אחת מהמודעות שלי, ומשם גם מעדכנים מחיר.',
 mineH1:'המודעות שלי',mineCount:function(a,m,d){return a+' מתוך '+m+' מודעות פעילות · '+(d===1?'טיוטה אחת':d+' טיוטות');},newListing:'מודעה חדשה',
 chipLive:'באוויר',chipSold:'נמכרה',chipRented:'הושכרה',chipPending:'בבדיקה',chipRemoved:'הוסרה מהאתר',chipDraftTest:'טיוטה (בדיקה)',livedSince:function(d){return 'באוויר מ־'+d;},
 edit:'עריכה',editPrice:'עדכון מחיר',markSold:'סימון כנמכרה',markRented:'סימון כהושכרה',removeLive:'הסרה מהאתר',rmH:'להסיר את המודעה מהאתר?',rmTxt:'המודעה תרד מהאתר מיד. הפרטים והתמונות יישארו ברשימה הזו, ואפשר לפרסם אותה שוב.',rmYes:'הסרה',
 republish:'פרסום מחדש',backOnMarket:'החזרה לפרסום',continueDraft:'המשך עריכה',draftMeta:function(s,d){return 'טיוטה · שלב '+s+' מתוך 5 · נשמרה ב־'+d;},
 soldAskH:'לסמן את המודעה כנמכרה?',rentedAskH:'לסמן את המודעה כהושכרה?',markAskTxt:'העמוד יישאר עם הודעה מתאימה, וכפתורי הפנייה יורדים. אפשר להחזיר לפרסום מכאן.',yesMark:'סימון',
 newPrice:'מחיר חדש בש״ח',savePrice:'שמירת המחיר',deletedH:'פריטים שנמחקו',deletedNote:'טיוטה שנמחקה נשמרת כאן 30 יום, ואפשר לשחזר אותה.',restore:'שחזור',restored:'הטיוטה שוחזרה.',
 mineEmpty:'עוד אין מודעות. המודעה הראשונה תופיע כאן.',loadFail:'לא הצלחנו לטעון את הרשימה. מרעננים את העמוד.',pendingNote:'בבדיקה לפני פרסום',removedNote:'לא מוצגת באתר',soldNote:'לא מוצגת כפעילה באתר',
 actionFail:'הפעולה לא הושלמה.',promoH:'קידום מודעה',promoOff:'לא פעיל כרגע',promoTeaser:'מקום בולט יותר ברשימות הנכסים. האפשרות עוד לא פעילה, ולא נגבה עליה תשלום.',promoMore:'מה זה יהיה',
 promoLead:'כאן תוכלו לבחור מודעה שתוצג במקום בולט יותר ברשימות הנכסים.',promoOffH:'האפשרות הזו עוד לא פעילה',promoOffTxt:' אין כאן תשלום ואין שמירה של פרטי תשלום. כשהיא תיפתח, המחיר והתנאים יוצגו לפני כל אישור.',
 promoPick:'בחירת מודעה',promoNone:'אין מודעה באוויר לבחירה.',promoWhere:'איפה',promoList:'רשימת הנכסים',promoCity:'עמוד העיר',promoPrice:'מחיר',promoPriceTxt:'יוצג כאן לפני כל אישור.',promoBtn:'לא זמין כרגע',backMine:'חזרה למודעות שלי',
 asideAria:'השלבים והמודעה שלכם',asideH:'השלבים',sumKick:'המודעה שלכם עד עכשיו',sumPhotos:function(n){return n===1?'תמונה אחת':n+' תמונות';},
 fn:{deal:'סוג העסקה',ptype:'סוג הנכס',city:'עיר',hood:'שכונה',rooms:'חדרים',size:'שטח',floor:'קומה',price:'מחיר',desc:'תיאור',cname:'שם להצגה',phone:'טלפון',phone_ok:'הסכמה לפרסום הטלפון',owner_ok:'הצהרת בעלות',photos:'תמונות'},
 yes:'כן',no:'לא',engineOff:'הפרסום לא זמין כרגע. מה שתכתבו נשמר.',
 switchedH:'החשבון במכשיר הזה השתנה',switchedTxt:'כדי לשמור על הפרטים של כל חשבון, הדף הזה נוקה. טיוטה שמורה בחשבון מחכה לבעליה, ואפשר להמשיך אותה אחרי כניסה.',switchedBtn:'לכניסה ולהמשך'
},en:{
 myListings:'My listings',signInTop:'Sign in',navAria:'My account',acct:function(n){return 'Signed in as '+n;},
 authKick:'List your property',authH1:'List your property, owner to buyer',authLead:'Open an account with your name and email, fill in the property details and add photos. The listing goes live at its own address. No commission.',
 authTabsAria:'Open an account or sign in',tabSignup:'Open an account',tabLogin:'I have an account',firstName:'First name',email:'Email',password:'Password',showPw:'Show',hidePw:'Hide',showPwAria:'Show the password',
 pwHint:'At least 8 characters. You can change it at any time.',termsA:'By opening an account you agree to the',terms:'terms of use',termsB:'and the',privacy:'privacy policy',
 signupCta:'Open an account and continue',signupBusy:'Opening the account…',mailExistsAct:'Sign in with this email',loginCta:'Sign in',loginBusy:'Signing in…',forgot:'I forgot my password',
 recH:'Reset your password',recLead:'Type the account email. If it is registered, we will send it a link to choose a new password.',recSend:'Send a reset link',recWait:function(n){return 'You can send again in '+n+' seconds';},
 recSentH:'If the email is registered, the link is on its way.',recSent:' The link works for a limited time. Nothing arrived? Check the spam folder too.',backLogin:'Back to sign in',
 brokerLine:'Brokers list from their own site.',brokerLink:'To your broker site',howAria:'What happens after you sign up',howH:'What comes next',how1:'Property details, a few minutes',how2:'Up to 30 photos from your phone',how3:'Preview and publish',
 howNote:'You can stop at any step. The draft waits for you in your account.',netErr:'No connection. What you typed is kept in the form; try again.',genericErr:'Something went wrong. What you typed is kept; try again.',
 draftKick:function(n){return n?'Welcome back, '+n:'Welcome back';},draftH1:'You have a saved draft',draftLead:'Continue where you stopped. What you filled in is saved in your account.',chipDraft:'Draft',
 draftSaved:function(d){return 'Saved in your account on '+d;},draftStep:function(n){return 'Step '+n+' of 5';},draftNext:function(s){return 'Next: '+s;},draftContinue:'Continue where you stopped',draftNew:'New listing',
 draftNewNote:'Starting a new listing does not delete this draft. It stays under My listings.',draftDelete:'Delete the draft',delAskH:'Delete the draft?',delAskTxt:'The draft moves to deleted items and leaves this list. You can restore it from there.',
 delYes:'Delete',cancel:'Cancel',delRunH:'Deleting the draft',delRunTxt:' It stays here until the server confirms the move. If the connection drops, nothing is deleted.',delFailH:'The draft was not deleted',delFail:' The server did not confirm, and the draft stays as it was.',
 otherDrafts:function(n){return n===1?'You have one more draft under My listings.':'You have '+n+' more drafts under My listings.';},
 stDeviceH:'Saved on this device',stDevice:' Not in your account yet. The details are saved to your account in a moment.',stDeviceNoStore:' (Saving on this device is blocked in this browser, so until then they are only in the open page.)',stSavingH:'Saving to your account…',stSaving:' What you typed is already kept on this device.',
 stAccountH:'Saved in your account',stAccount:function(t){return ' Last saved at '+t+'. You can stop and continue from any device.';},stNewH:'New draft',stNew:' Nothing is saved yet. What you type is saved to your account as you go.',
 stOfflineH:'No internet connection',stOffline:' What you type is kept on this device and sent to your account when the connection returns. Keep this page open until then.',stOfflineNoStore:' Saving on this device is blocked in this browser, so what you type is only in the open page. Keep it open until the connection returns.',
 stRetryH:'Saving to your account failed',stRetry:function(n){return ' Your details are kept on this device. We will try again in '+n+' seconds.';},stRetryNoStore:function(n){return ' Your details are in the open page. We will try again in '+n+' seconds.';},retryNow:'Try now',
 conflictH:'This draft is also open in another tab',conflictTxt:function(t){return ' A change was saved there at '+t+'. Choose which version to continue with, so nothing is overwritten.';},conflictLoad:'Load the version from the other tab',conflictKeep:'Continue here and save this version',
 conflictDiff:'What differs:',here:'here',there:'there',empty:'empty',loadedH:'The other tab\'s version is loaded',loadedTxt:' The version that was here is not lost; you can go back to it.',backToMine:'Back to the version that was here',
 perAccount:'Drafts are kept per account. If you started a listing in another account on this device, sign in to it to continue.',otherAccount:'Sign in to another account',
 expiredH:'Please sign in again',expiredTxt:' Your session ended. What you typed is kept on this device and is saved to your account after you sign in.',expiredTxtNoStore:' Your session ended. Keep this page open: what you typed is in it, and is saved after you sign in in another tab.',expiredBtn:'Sign in',
 nostoreH:'Saving on this device is blocked in this browser',nostore:' Changes are saved only to your account, when there is a connection. Do not close the page before you see "Saved in your account".',
 goneH:'The draft is not there',goneTxt:' It may have been deleted in another tab. What you typed is still here.',goneNew:'Save as a new draft',publishingH:'The listing is being published',publishingTxt:' Checking again in a moment. What you typed is kept.',
 progAria:'Listing progress',stepNames:['Account','Property details','Photos','Preview','Publish'],stepOf:function(n){return 'Step '+n+' of 5';},
 detH1:'Property details',detLead:'A few basic details. You can stop at any step and continue later from the same place.',dealType:'Deal type',sale:'For sale',rent:'For rent',propType:'Property type',ptChoose:'Choose',
 ptApt:'Apartment',ptGarden:'Garden apartment',ptPh:'Penthouse',ptDuplex:'Duplex',ptHouse:'House',city:'City',hood:'Neighbourhood',addrHint:'The street and house number are never published. The listing and its address show the city and neighbourhood only.',
 rooms:'Rooms',size:'Size',sqm:'m²',floor:'Floor',optional:'(optional)',floorHint:'For example 3, or 3 of 8',priceSale:'Asking price',priceRent:'Monthly rent',priceHint:'Digits only. You can update it later from My listings.',
 desc:'A few words about the property',descHint:'What matters: balcony, parking, lift, condition.',fairNote:'Wording that limits by religion, origin, disability or family status holds the listing for review before it goes live.',
 contactH:'How people reach you',contactName:'Display name',phone:'Phone',phoneOpt:'(optional if you do not publish it)',showPhone:'I agree to publish my phone number on the listing',
 showPhoneSub:'The number shows on the listing, and the WhatsApp and call buttons reveal it to whoever taps them. Unchecked, the number is not on the listing and it has no WhatsApp or call buttons.',
 ownerDecl:'I own the property or I am allowed to list it',ownerDeclSub:'Required before publishing.',toPhotos:'Continue to photos',saveExit:'Save and exit',checking:'Checking…',
 errSumH:function(n){return n===1?'One detail needs fixing':n+' details need fixing';},brokerHint:'Brokers? You have your own site and a personal link for listings, free:',
 phH1:'Photos',phLead:'Up to 30 photos. The first photo is the listing\'s cover.',addPhotos:'Add photos',phDropHint:'From your phone or computer. JPG, PNG, WebP or HEIC, up to 15 MB each. Location data in the file is removed before it is kept.',
 phCount:function(n,m){return n+' of '+m;},phOrderHint:'Reorder with the arrows and set the cover with the star. The buttons work from the keyboard too.',phListAria:'The listing\'s photos',coverBadge:'Cover',
 photoN:function(n){return 'Photo '+n;},uploading:'Uploading',upFail:'This photo did not upload.',tryAgain:'Try again',earlier:'Move earlier: ',later:'Move later: ',makeCover:'Set as cover: ',remove:'Remove: ',
 toPreview:'Continue to preview',backDetails:'Back to property details',waitUploads:'Waiting for the photos to finish uploading.',failedLeft:function(n){return n===1?'One photo did not upload: try again or remove it. It will not be on the listing.':n+' photos did not upload: try again or remove them. They will not be on the listing.';},
 tooMany:'Up to 30 photos per listing. The extra photos were not added.',photosNeedDraft:'Saving the property details first…',
 upErr:{big:'The photo is larger than 15 MB.',type:'This file is not a photo we can take: JPG, PNG, WebP or HEIC.',heic:'This HEIC file cannot be cleaned of its location data here. Save it as JPG and upload again.',corrupt:'The file is damaged and does not open as a photo.',orient:'The photo is stored turned, and the server cannot set it upright. Save it again and upload it again.',auth:'Your session ended. Sign in again and the photo uploads on the next try.',rate:'Many photos in the last hour. Try again in a few minutes.',server:'A server error. You can try again.',timeout:'The upload took too long. Check the connection and try again.',net:'No connection. Try again when it returns.'},
 pvH1:'Preview',pvLead:'This is how the listing will look on the site. Check the details before you publish.',pvBanner:'Preview. The listing is not live yet.',pvBannerEdit:'A preview of the changes. The live listing stays as it is until you update it.',
 pvAria:'Listing preview',pvCap:'Cover',fromOwner:'From the owner',wa:'WhatsApp',call:'Call',pvBtnsNote:'The contact buttons work once the listing is live. They reveal the number you agreed to publish.',
 pvNoContact:'You did not agree to publish the phone, so the listing has no number and no WhatsApp or call buttons.',pvHold:'Wording in the description holds the listing for a person to review before it goes live.',pvLangNote:'The listing page is published in Hebrew, with the city and neighbourhood as you typed them.',
 pvAddr:'The listing\'s address',pvAddrHint:'A permanent address in Latin letters: the city, the rooms and the deal. No street, no number.',pvAddrLive:'The listing\'s address does not change with an update.',
 publish:'Publish the listing',update:'Update the listing',backEdit:'Back to editing',publishNote:'You can edit, update the price or remove the listing at any time from My listings.',
 sendingH:'Publishing your listing',sendingTxt:' Waiting for the server to confirm. If the connection drops, check My listings before you send again.',sendingLabel:'Publishing…',buildingH:'The listing is being built',buildingTxt:' The server is still on it. Checking again in a few seconds.',
 lostH:'The connection dropped before an answer arrived',lostTxt:' The listing may already be live. Check My listings, or check again here: the same request is sent again.',checkAgain:'Check again',
 pvFull:'See the full listing page',pvErrH:'Before publishing, fix:',fix:'Fix',pvOffline:'No connection, so no preview right now. What you typed is kept.',pvLoading:'Preparing the preview…',
 doneH1:'Your listing is live',doneUpdatedH1:'Your listing is updated',doneLead:function(d){return 'Published on '+d+'.';},doneUpdatedLead:'The changes are already on the listing page.',
 donePendingH1:'Your listing is saved and goes live after a short review',donePendingLead:'Some wording needs a person to check it before publishing. The listing is not shown on the site until then.',doneDraftH1:'The listing is saved as a draft',doneDraftLead:'It is not shown on the site.',
 copyLink:'Copy',copied:'Link copied',toListing:'To the listing',shareWa:'Share on WhatsApp',doneManage:'Sold or rented? Mark it in one tap from My listings, where you can also update the price.',
 mineH1:'My listings',mineCount:function(a,m,d){return a+' of '+m+' active listings · '+(d===1?'1 draft':d+' drafts');},newListing:'New listing',
 chipLive:'Live',chipSold:'Sold',chipRented:'Rented',chipPending:'In review',chipRemoved:'Removed from the site',chipDraftTest:'Draft (test)',livedSince:function(d){return 'Live since '+d;},
 edit:'Edit',editPrice:'Update price',markSold:'Mark as sold',markRented:'Mark as rented',removeLive:'Remove from the site',rmH:'Remove the listing from the site?',rmTxt:'It comes off the site at once. Its details and photos stay in this list, and you can publish it again.',rmYes:'Remove',
 republish:'Publish again',backOnMarket:'Back on the market',continueDraft:'Continue editing',draftMeta:function(s,d){return 'Draft · step '+s+' of 5 · saved '+d;},
 soldAskH:'Mark the listing as sold?',rentedAskH:'Mark the listing as rented?',markAskTxt:'The page stays with a fitting notice and the contact buttons come down. You can put it back on the market from here.',yesMark:'Mark',
 newPrice:'New price in ₪',savePrice:'Save the price',deletedH:'Deleted items',deletedNote:'A deleted draft stays here for 30 days and can be restored.',restore:'Restore',restored:'The draft is restored.',
 mineEmpty:'No listings yet. Your first listing will show here.',loadFail:'The list did not load. Refresh the page.',pendingNote:'In review before publishing',removedNote:'Not shown on the site',soldNote:'Not shown as active on the site',
 actionFail:'The action did not finish.',promoH:'Promote a listing',promoOff:'Not active',promoTeaser:'A more prominent place in the property lists. Not active yet, and nothing is charged for it.',promoMore:'What it will be',
 promoLead:'Here you will be able to choose a listing to show in a more prominent place in the property lists.',promoOffH:'This option is not active yet',promoOffTxt:' There is no payment here and no payment details are stored. When it opens, the price and terms show before any confirmation.',
 promoPick:'Choose a listing',promoNone:'No live listing to choose.',promoWhere:'Where',promoList:'Property list',promoCity:'City page',promoPrice:'Price',promoPriceTxt:'Shown here before any confirmation.',promoBtn:'Not available yet',backMine:'Back to My listings',
 asideAria:'The steps and your listing',asideH:'The steps',sumKick:'Your listing so far',sumPhotos:function(n){return n===1?'1 photo':n+' photos';},
 fn:{deal:'Deal type',ptype:'Property type',city:'City',hood:'Neighbourhood',rooms:'Rooms',size:'Size',floor:'Floor',price:'Price',desc:'Description',cname:'Display name',phone:'Phone',phone_ok:'Consent to publish the phone',owner_ok:'Ownership statement',photos:'Photos'},
 yes:'yes',no:'no',engineOff:'Publishing is not available right now. What you type is kept.',
 switchedH:'The account on this device changed',switchedTxt:'To keep each account private, this page was cleared. A draft saved in an account waits for its owner and continues after signing in.',switchedBtn:'Sign in and continue'
}};
var T=W[LANG];

/* ---------------- small tools ---------------- */
function $(id){return document.getElementById(id);}
function esc(s){return String(s==null?'':s).replace(/[&<>"']/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c];});}
function clone(o){return JSON.parse(JSON.stringify(o));}
function pad(n){return (n<10?'0':'')+n;}
var LRI='⁦',PDI='⁩';   /* dates and times keep their order inside Hebrew text */
function fdate(ts){if(!ts){return '';}var d=new Date(ts*1000);return LRI+d.getDate()+'.'+(d.getMonth()+1)+'.'+d.getFullYear()+', '+pad(d.getHours())+':'+pad(d.getMinutes())+PDI;}
function fday(ts){if(!ts){return '';}var d=new Date(ts*1000);return LRI+d.getDate()+'.'+(d.getMonth()+1)+'.'+d.getFullYear()+PDI;}
function ftime(ts){if(!ts){return '';}var d=new Date(ts*1000);return LRI+pad(d.getHours())+':'+pad(d.getMinutes())+PDI;}
function rid(){try{if(window.crypto&&crypto.randomUUID){return crypto.randomUUID();}}catch(e){}var s='';for(var i=0;i<32;i++){s+=Math.floor(Math.random()*16).toString(16);}return s.slice(0,8)+'-'+s.slice(8,12)+'-'+s.slice(12,16)+'-'+s.slice(16,20)+'-'+s.slice(20);}
function online(){return navigator.onLine!==false;}
var ICO={
 err:'<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><circle cx="12" cy="12" r="9"></circle><path d="M12 7v6M12 16.5v.5"></path></svg>',
 info:'<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><circle cx="12" cy="12" r="9"></circle><path d="M12 11v6M12 7.5v.5"></path></svg>',
 dev:'<svg class="nlj-st-ico" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="6" y="2.5" width="12" height="19" rx="2.5"></rect><path d="M11 18.5h2"></path></svg>',
 ok:'<svg class="nlj-st-ico" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m5 12.5 4.5 4.5L19 7.5"></path></svg>',
 off:'<svg class="nlj-st-ico" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M2 8.5a15 15 0 0 1 20 0M5 12a10 10 0 0 1 14 0M8.5 15.5a5 5 0 0 1 7 0M12 19h.01M3 3l18 18"></path></svg>',
 retry:'<svg class="nlj-st-ico" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 12a8 8 0 1 1-2.3-5.6M20 4v5h-5"></path></svg>',
 tabs:'<svg class="nlj-st-ico" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="5" width="12" height="10" rx="2"></rect><rect x="9" y="9" width="12" height="10" rx="2"></rect></svg>',
 spin:'<svg class="nlj-st-ico" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><circle cx="12" cy="12" r="9" stroke-dasharray="40 20"></circle></svg>',
 mail:'<svg class="nlj-st-ico" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 6h16v12H4z"></path><path d="m4 7 8 6 8-6"></path></svg>',
 note:'<svg class="nlj-st-ico" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="6" y="2.5" width="12" height="19" rx="2.5"></rect><path d="M9.5 9.5h5M9.5 13h5"></path></svg>',
 house:'<svg viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M8 40V18l16-10 16 10v22z"></path><path d="M19 40V28h10v12"></path></svg>',
 bld:'<svg viewBox="0 0 96 64" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M6 56h84M14 56V22h28v34M50 56V12h32v44"></path><path d="M20 30h16v10H20zM56 20h20v12H56zM56 40h20v8H56z"></path></svg>',
 fwd:'<svg class="nlj-fwd" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"></path></svg>',
 prev:'<svg class="nlj-fwd" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M15 6l-6 6 6 6"></path></svg>',
 next:'<svg class="nlj-fwd" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M9 6l6 6-6 6"></path></svg>',
 star:'<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m12 3 2.6 5.6 6 .6-4.5 4.1 1.3 6L12 16.4 6.6 19.3l1.3-6L3.4 9.2l6-.6z"></path></svg>',
 bin:'<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 7h16M10 11v6M14 11v6M6 7l1 13h10l1-13M9 7V4h6v3"></path></svg>',
 pic:'<svg width="34" height="34" viewBox="0 0 24 24" fill="none" stroke="#2f6f86" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="5" width="18" height="14" rx="2.5"></rect><circle cx="9" cy="10" r="1.8"></circle><path d="m21 16-5-5-8 8"></path></svg>',
 eye:'<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M2 12s3.6-7 10-7 10 7 10 7-3.6 7-10 7S2 12 2 12z"></path><circle cx="12" cy="12" r="3"></circle></svg>',
 check:'<svg width="30" height="30" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m5 12.5 4.5 4.5L19 7.5"></path></svg>'
};

/* ---------------- storage: per user, honest about failures, nothing secret ---------------- */
var store=(function(){
 var ok=true;
 try{var k='nlow:probe';localStorage.setItem(k,'1');localStorage.removeItem(k);}catch(e){ok=false;}
 return {
  ok:function(){return ok;},
  get:function(k){if(!ok){return null;}try{var v=localStorage.getItem(k);return v?JSON.parse(v):null;}catch(e){return null;}},
  set:function(k,v){if(!ok){return false;}try{localStorage.setItem(k,JSON.stringify(v));return true;}catch(e){ok=false;render.status();return false;}},
  del:function(k){if(!ok){return;}try{localStorage.removeItem(k);}catch(e){}}
 };
})();
var MEM={};   // the same values in memory when storage is blocked
function qkey(id){return 'nlow:v2:u'+C.uid+':d'+(id||'new');}

/* ---------------- the server ---------------- */
function api(method,path,body,opt){
 opt=opt||{};
 var ctl=('AbortController' in window)?new AbortController():null,timer=null;
 if(ctl){timer=setTimeout(function(){ctl.abort();},opt.timeout||30000);}
 var url=C.api+path,init={method:method,credentials:'same-origin',headers:{'X-WP-Nonce':C.nonce||''}};
 if(ctl){init.signal=ctl.signal;}
 if(opt.keepalive){init.keepalive=true;}
 if(method==='GET'){url+=(url.indexOf('?')>-1?'&':'?')+'lang='+LANG+'&_='+Date.now();}
 else{init.headers['Content-Type']='application/json';init.body=JSON.stringify(Object.assign({lang:LANG},body||{}));}
 return fetch(url,init).then(function(r){
  if(timer){clearTimeout(timer);}
  return r.text().then(function(t){var j=null;try{j=JSON.parse(t);}catch(e){}return {ok:r.ok,status:r.status,j:j||{}};});
 },function(e){if(timer){clearTimeout(timer);}return {ok:false,status:0,net:true,aborted:!!(e&&e.name==='AbortError'),j:{}};});
}
function isExpired(x){return x.status===401||(x.status===403&&(x.j.code==='rest_cookie_invalid_nonce'||x.j.code==='rest_forbidden'));}
function refreshNonce(){
 return fetch(C.ajax+'?action=nl_owner_nonce&_='+Date.now(),{credentials:'same-origin'}).then(function(r){return r.json().then(function(j){return {ok:r.ok,j:j};});})
  .then(function(x){if(x.ok&&x.j&&x.j.nonce&&+x.j.uid===+C.uid){C.nonce=x.j.nonce;return true;}return false;}).catch(function(){return false;});
}
function call(method,path,body,opt){
 return api(method,path,body,opt).then(function(x){
  if(!isExpired(x)||!C.uid){return x;}
  return refreshNonce().then(function(ok){
   if(!ok){x.expired=true;return x;}
   return api(method,path,body,opt).then(function(y){if(isExpired(y)){y.expired=true;}return y;});
  });
 });
}
function pub(path,body){   // the account doors (no account yet)
 return fetch(C.api+path,{method:'POST',credentials:'same-origin',headers:{'Content-Type':'application/json'},body:JSON.stringify(Object.assign({lang:LANG},body||{}))})
  .then(function(r){return r.text().then(function(t){var j=null;try{j=JSON.parse(t);}catch(e){}return {ok:r.ok,status:r.status,j:j||{}};});},function(){return {ok:false,status:0,net:true,j:{}};});
}

/* ---------------- state ---------------- */
var FIELDS=['deal','ptype','city','hood','rooms','size','floor','price','desc','cname','phone','phone_ok','owner_ok'];
function emptyFields(){return {deal:'',ptype:'',city:'',hood:'',rooms:'',size:'',floor:'',price:'',desc:'',cname:(C.prefill&&C.prefill.cname)||'',phone:(C.prefill&&C.prefill.phone)||'',phone_ok:false,owner_ok:false};}
var S={screen:'',auth:'signup',authMail:'',authName:'',drafts:[],mine:null,errors:{},showErr:false,save:'',saveMsg:'',retryAt:0,conflict:null,stash:null,pub:null,preview:null,del:'closed',published:null,recUntil:0};
var D=newDraft();
function newDraft(){return {id:0,rev:0,fields:emptyFields(),photos:[],step:'details',saved_at:0,state:'editing',listing:null,pub_rev:0,ck:'',seq:0,synced:0,discard:[]};}
function dirty(){return D.seq!==D.synced;}
var P=[];   // photo tiles: {k,ref,att,thumb,full,w,h,s:'ok'|'wait'|'up'|'err',pct,err,file,preview,xhr,removed}
var tileSeq=0;

/* ---------------- the local queue (this user, this draft) ---------------- */
function queueWrite(){
 var f=clone(D.fields);delete f.phone;   // the phone never sits in this device's storage
 var v={id:D.id,rev:D.rev,fields:f,photos:photoList(),step:D.step,t:Math.floor(Date.now()/1000),ck:D.ck,tab:TAB};
 if(!store.set(qkey(D.id),v)){MEM[qkey(D.id)]=v;}
}
/* Only this account's exact keys are ever read or written. Another account's queue, and the 1.x wizard's unowned
   'nlow-draft' text, are never listed, read, shown, imported or deleted from here (HAD-256 privacy rule). */
function queueClear(){store.del(qkey(D.id));store.del(qkey(''));delete MEM[qkey(D.id)];}

/* ---------------- saving ---------------- */
var saveTimer=null,saving=false,again=false,retryTimer=null,tick=null;
function touch(){D.seq++;queueWrite();if(!online()){setSave('offline');}else if(S.save!=='conflict'&&S.save!=='expired'&&S.save!=='gone'){setSave('device');}schedule(1200);}
function schedule(ms){clearTimeout(saveTimer);saveTimer=setTimeout(function(){flush();},ms==null?1200:ms);}
function photoList(){return P.filter(function(t){return t.s==='ok'&&!t.removed;}).map(function(t){var o={};if(t.ref){o.ref=t.ref;}if(t.att){o.att=t.att;}return o;});}
function setSave(k,msg){S.save=k;S.saveMsg=msg||'';render.status();}
function retryIn(sec){
 clearTimeout(retryTimer);clearInterval(tick);S.retryAt=Date.now()+sec*1000;
 retryTimer=setTimeout(function(){flush();},sec*1000);
 tick=setInterval(function(){if(S.save!=='retry'){clearInterval(tick);return;}render.status();},1000);
}
function applyMeta(j){
 if(!j||!j.id){return;}
 var was=D.id;D.id=j.id;D.rev=j.rev;D.saved_at=j.saved_at;D.state=j.state;D.listing=j.listing;D.pub_rev=j.pub_rev||0;
 if(!was){store.del(qkey(''));delete MEM[qkey('')];setUrl(true);}
 (j.photos||[]).forEach(function(p){P.forEach(function(t){if(t.ref&&t.ref===p.ref){t.att=p.att||t.att;if(p.thumb){t.thumb=p.thumb;t.full=p.full;}}});});
}
var flushP=null;
function flush(opt){
 opt=opt||{};
 if(saving){again=true;return flushP;}
 if(!dirty()&&D.id){return Promise.resolve(true);}
 if(!dirty()&&!D.id&&!opt.create){return Promise.resolve(true);}
 if(!online()){setSave('offline');return Promise.resolve(false);}
 clearTimeout(saveTimer);clearTimeout(retryTimer);
 saving=true;var seq=D.seq,sent=D.discard.slice();
 if(S.save!=='conflict'){setSave('saving');}
 var body={rev:D.rev,fields:D.fields,photos:photoList(),step:D.step,discard:sent};
 var p;
 if(D.id){p=call('POST','/draft/'+D.id,body,{keepalive:!!opt.keepalive});}
 else{if(!D.ck){D.ck=rid();queueWrite();}body.create_key=D.ck;p=call('POST','/draft',body);}
 flushP=p.then(function(x){
  saving=false;
  if(x.ok){
   applyMeta(x.j);
   D.discard=D.discard.filter(function(r){return sent.indexOf(r)<0;});
   if(D.seq===seq){D.synced=seq;queueClear();}
   if(S.save!=='loaded'||D.seq!==seq){setSave(dirty()?'device':'account');}
   bcSend({type:'saved',id:D.id,rev:D.rev,at:D.saved_at});
   render.aside();
   if(again||dirty()){again=false;schedule(300);}
   return true;
  }
  again=false;
  if(x.expired){setSave('expired');checkIdentity(true);return false;}
  if(x.status===409&&x.j.code==='conflict'){showConflict(x.j.data&&x.j.data.server);return false;}
  if(x.status===409&&x.j.code==='publishing'){setSave('publishing');retryIn(8);return false;}
  if(x.status===404){setSave('gone');return false;}
  if(x.net){if(!online()){setSave('offline');}else{setSave('retry');retryIn(10);}return false;}
  if(x.status===429){setSave('retry',x.j.message||'');retryIn(60);return false;}
  setSave('retry',x.j.message||'');retryIn(10);
  return false;
 });
 return flushP;
}
window.addEventListener('online',function(){if(dirty()||(!D.id&&D.seq)){flush();}else if(S.save==='offline'){setSave(D.id?'account':'');}});
window.addEventListener('offline',function(){if(C.uid&&S.screen&&['details','photos','preview'].indexOf(S.screen)>-1){setSave('offline');}});
document.addEventListener('visibilitychange',function(){if(document.visibilityState==='hidden'&&dirty()&&D.id){flush({keepalive:true});}});
window.addEventListener('pagehide',function(){if(dirty()&&D.id){flush({keepalive:true});}});
window.addEventListener('beforeunload',function(e){if(dirty()&&C.uid){queueWrite();e.preventDefault();e.returnValue='';}});

/* ---------------- one account per page ----------------
   Another tab signs in or out: this page asks the server who is signed in now (on focus, on becoming visible, on a
   restore from the back-forward cache, and on an "auth changed" ping that carries no data). If it is not the account
   the page was made for, everything the page shows or holds is dropped at once. No local queue is read, changed or
   deleted here, and no draft is touched: its owner signs in again and continues it. */
var authBc=null,scrubbed=false,checking=false,lastCheck=0;
try{if('BroadcastChannel' in window){authBc=new BroadcastChannel('nlow-auth');}}catch(e){authBc=null;}
function authPing(){try{if(authBc){authBc.postMessage(1);}}catch(e){}try{localStorage.setItem('nlow:auth-ping',String(Date.now()));}catch(e){}}
function whoAmI(){return fetch(C.ajax+'?action=nl_owner_nonce&_='+Date.now(),{credentials:'same-origin',cache:'no-store'}).then(function(r){return r.json();}).then(function(j){return +((j&&j.uid)||0);}).catch(function(){return null;});}
function checkIdentity(force){
 if(!C.uid||scrubbed||checking){return;}
 if(!force&&Date.now()-lastCheck<1500){return;}
 checking=true;lastCheck=Date.now();
 whoAmI().then(function(uid){checking=false;if(uid!==null&&uid!==+C.uid){scrub();}});
}
function scrub(){
 scrubbed=true;
 clearTimeout(saveTimer);clearTimeout(retryTimer);clearInterval(tick);
 P.forEach(function(t){if(t.xhr){try{t.xhr.abort();}catch(e){}}if(t.preview){try{URL.revokeObjectURL(t.preview);}catch(e){}}});
 C.nonce='';C.name='';C.prefill={};
 P=[];D=newDraft();S.preview=null;S.pub=null;S.mine=null;S.drafts=[];S.conflict=null;S.stash=null;S.published=null;S.errors={};S.authName='';S.authMail='';
 try{if(bc){bc.close();bc=null;}}catch(e){}
 root.innerHTML='<div class="nlj-wrap"><div class="nlj-card" style="max-width:640px" role="alert"><div class="nlj-head" data-focus tabindex="-1"><h2 class="nlj-h1">'+esc(T.switchedH)+'</h2><p class="nlj-lead">'+esc(T.switchedTxt)+'</p></div><div class="nlj-actions"><a class="nlj-btn nlj-btn--primary" href="'+esc(C.page)+'">'+esc(T.switchedBtn)+'</a></div></div></div>';
 var hd=root.querySelector('[data-focus]');if(hd){hd.focus();}
}
window.addEventListener('focus',function(){checkIdentity(false);});
document.addEventListener('visibilitychange',function(){if(document.visibilityState==='visible'){checkIdentity(false);}});
window.addEventListener('pageshow',function(e){if(e.persisted){checkIdentity(true);}});
window.addEventListener('storage',function(e){if(e.key==='nlow:auth-ping'){checkIdentity(true);}});
if(authBc){authBc.onmessage=function(){checkIdentity(true);};}

/* ---------------- two tabs ---------------- */
var bc=null;
try{if('BroadcastChannel' in window&&C.uid){bc=new BroadcastChannel('nlow-u'+C.uid);}}catch(e){bc=null;}
function bcSend(m){if(bc){try{m.tab=TAB;bc.postMessage(m);}catch(e){}}}
if(bc){bc.onmessage=function(ev){
 var m=ev.data||{};if(m.tab===TAB||!m.id||m.id!==D.id){return;}
 if(m.type==='saved'&&m.rev>D.rev){
  call('GET','/draft/'+D.id).then(function(x){
   if(!x.ok||!x.j||x.j.rev<=D.rev){return;}
   if(dirty()){showConflict(x.j);}
   else{loadServer(x.j);setSave('account');render.screen();}
  });
 }
};}
function loadServer(s){
 D.rev=s.rev;D.saved_at=s.saved_at;D.state=s.state;D.listing=s.listing;D.pub_rev=s.pub_rev||0;
 if(s.fields){D.fields=Object.assign(emptyFields(),s.fields);}
 D.step=s.step||D.step;
 P=(s.photos||[]).map(function(p){return {k:++tileSeq,ref:p.ref,att:p.att||0,thumb:p.thumb,full:p.full,w:p.w,h:p.h,s:'ok'};});
 D.synced=D.seq;queueClear();
}
function showConflict(server){
 if(!server){setSave('retry');retryIn(10);return;}
 S.conflict={server:server,mine:{fields:clone(D.fields),photos:P.slice()}};
 setSave('conflict');
}
function conflictDiff(){
 if(!S.conflict){return '';}
 var a=S.conflict.mine.fields,b=Object.assign(emptyFields(),S.conflict.server.fields||{}),out=[];
 FIELDS.forEach(function(k){
  var x=a[k],y=b[k];if(String(x)===String(y)){return;}
  var fx=typeof x==='boolean'?(x?T.yes:T.no):(String(x).trim()?String(x):T.empty),fy=typeof y==='boolean'?(y?T.yes:T.no):(String(y).trim()?String(y):T.empty);
  if(k==='desc'){fx=fx.slice(0,40)+(fx.length>40?'…':'');fy=fy.slice(0,40)+(fy.length>40?'…':'');}
  out.push('<li><b>'+esc(T.fn[k])+'</b>: '+esc(T.here)+' «'+esc(fx)+'» · '+esc(T.there)+' «'+esc(fy)+'»</li>');
 });
 var n1=S.conflict.mine.photos.filter(function(t){return t.s==='ok';}).length,n2=(S.conflict.server.photos||[]).length;
 if(n1!==n2){out.push('<li><b>'+esc(T.fn.photos)+'</b>: '+esc(T.here)+' '+n1+' · '+esc(T.there)+' '+n2+'</li>');}
 return out.length?'<p class="nlj-small" style="margin-top:8px">'+esc(T.conflictDiff)+'</p><ul class="nlj-diff">'+out.slice(0,8).join('')+'</ul>':'';
}

/* ---------------- routing: back and forward keep the draft ---------------- */
function readUrl(){var q=new URLSearchParams(location.search);return {draft:+(q.get('draft')||0),screen:q.get('nlj')||''};}
function setUrl(replace){
 try{
  var q=new URLSearchParams(location.search);
  if(D.id&&['details','photos','preview','home'].indexOf(S.screen)>-1){q.set('draft',D.id);}else{q.delete('draft');}
  if(S.screen&&S.screen!=='auth'){q.set('nlj',S.screen);}else{q.delete('nlj');}
  var u=location.pathname+(q.toString()?'?'+q.toString():'')+location.hash;
  if(u===location.pathname+location.search+location.hash){return;}
  if(replace){history.replaceState({nlj:S.screen},'',u);}else{history.pushState({nlj:S.screen},'',u);}
 }catch(e){}
}
function go(screen,opt){
 opt=opt||{};
 if(['details','photos','preview'].indexOf(screen)>-1&&D.step!==screen){D.step=screen;if(D.id||D.seq){touch();}}
 S.screen=screen;S.showErr=false;
 if(!opt.noUrl){setUrl(!!opt.replace);}
 render.screen();
 if(!opt.keepScroll){try{root.scrollIntoView({block:'start'});}catch(e){}}
 var h=root.querySelector('[data-focus]');if(h&&!opt.noFocus){h.setAttribute('tabindex','-1');h.focus({preventScroll:true});}
}
window.addEventListener('popstate',function(){
 var u=readUrl();
 if(!C.uid){S.screen='auth';render.screen();return;}
 var sc=u.screen||(u.draft?D.step:'');
 if(u.draft&&u.draft!==D.id){openDraft(u.draft,sc||null,true);return;}
 if(!sc){startFresh(true);return;}
 go(sc,{noUrl:true,noFocus:false});
});

/* ---------------- rendering ---------------- */
var render={};
function progress(n){
 var bars='';for(var i=1;i<=5;i++){bars+='<i class="'+(i<n?'is-done':(i===n?'is-now':''))+'"></i>';}
 return '<div class="nlj-prog5" role="group" aria-label="'+esc(T.progAria)+'"><div class="nlj-prog5-top"><b>'+esc(T.stepOf(n))+'</b><span>'+esc(T.stepNames[n-1])+'</span></div><div class="nlj-bars" aria-hidden="true">'+bars+'</div></div>';
}
function statusBox(kind,ico,h,txt,acts,role){
 return '<div class="nlj-status'+(kind?' nlj-status--'+kind:'')+'"'+(role?' role="'+role+'"':'')+'>'+ico+'<div><b>'+esc(h)+'</b>'+esc(txt||'')+(acts?'<div class="nlj-status-acts">'+acts+'</div>':'')+'</div></div>';
}
render.status=function(){
 var el=$('nlj-st');if(!el){return;}
 var k=S.save,h='',ns=!store.ok();
 if(k==='conflict'&&S.conflict){
  h=statusBox('warn',ICO.tabs,T.conflictH,T.conflictTxt(ftime(S.conflict.server.saved_at)),'<button class="nlj-btn nlj-btn--secondary nlj-btn--sm" type="button" data-act="cf-load">'+esc(T.conflictLoad)+'</button><button class="nlj-btn nlj-btn--quiet" type="button" data-act="cf-keep">'+esc(T.conflictKeep)+'</button>','alert');
  h=h.replace('</div></div>',conflictDiff()+'</div></div>');
 }
 else if(k==='loaded'){h=statusBox('ok',ICO.ok,T.loadedH,T.loadedTxt,'<button class="nlj-btn nlj-btn--quiet" type="button" data-act="cf-back">'+esc(T.backToMine)+'</button>','status');}
 else if(k==='expired'){h=statusBox('bad',ICO.retry,T.expiredH,ns?T.expiredTxtNoStore:T.expiredTxt,'<a class="nlj-btn nlj-btn--secondary nlj-btn--sm" href="'+esc(C.page)+'" target="_blank" rel="noopener">'+esc(T.expiredBtn)+'</a><button class="nlj-btn nlj-btn--quiet" type="button" data-act="retry">'+esc(T.retryNow)+'</button>','alert');}
 else if(k==='gone'){h=statusBox('bad',ICO.retry,T.goneH,T.goneTxt,'<button class="nlj-btn nlj-btn--secondary nlj-btn--sm" type="button" data-act="gone-new">'+esc(T.goneNew)+'</button>','alert');}
 else if(k==='publishing'){h=statusBox('warn',ICO.spin,T.publishingH,T.publishingTxt,'','status');}
 else if(k==='offline'){h=statusBox('warn',ICO.off,T.stOfflineH,ns?T.stOfflineNoStore:T.stOffline,'','status');}
 else if(k==='retry'){var sec=Math.max(0,Math.ceil((S.retryAt-Date.now())/1000));h=statusBox('bad',ICO.retry,T.stRetryH,(S.saveMsg?' '+S.saveMsg:'')+(ns?T.stRetryNoStore(sec):T.stRetry(sec)),'<button class="nlj-btn nlj-btn--secondary nlj-btn--sm" type="button" data-act="retry">'+esc(T.retryNow)+'</button>','alert');}
 else if(k==='saving'){h=statusBox('',ICO.spin,T.stSavingH,ns?'':T.stSaving,'','status');}
 else if(k==='device'){h=statusBox('',ICO.dev,ns?T.stSavingH:T.stDeviceH,ns?T.stDeviceNoStore:T.stDevice,'','status');}
 else if(k==='account'&&D.saved_at){h=statusBox('ok',ICO.ok,T.stAccountH,T.stAccount(ftime(D.saved_at)),'','status');}
 else{h=statusBox('',ICO.dev,T.stNewH,T.stNew,'','status');}
 if(ns&&k!=='offline'&&k!=='expired'){h+=statusBox('warn',ICO.info.replace('width="18" height="18"','class="nlj-st-ico"'),T.nostoreH,T.nostore,'','note');}
 el.innerHTML=h;
};
render.aside=function(){
 var el=$('nlj-aside');if(!el){return;}
 var n={details:2,photos:3,preview:4}[S.screen]||2,steps='';
 T.stepNames.forEach(function(l,i){var k=i+1;steps+='<li class="'+(k<n?'is-done':(k===n?'is-now':''))+'"><span class="nlj-dot">'+k+'</span>'+esc(l)+'</li>';});
 var f=D.fields,okp=P.filter(function(t){return t.s==='ok';}).length,title=summaryTitle(f);
 el.innerHTML='<div class="nlj-card"><h2>'+esc(T.asideH)+'</h2><ol class="nlj-steps">'+steps+'</ol></div><div class="nlj-card nlj-card--sand" style="gap:10px"><p class="nlj-kick">'+esc(T.sumKick)+'</p><h3>'+esc(title)+'</h3><p class="nlj-small">'+esc([f.hood,f.city].filter(Boolean).join(', '))+'</p>'+(f.price?'<p class="nlj-label"><span class="nlj-num">'+esc(fmtPrice(f.price,f.deal))+'</span></p>':'')+'<p class="nlj-meta">'+esc(T.sumPhotos(okp))+'</p></div>';
};
function fmtPrice(p,deal){var n=String(p).replace(/[^\d]/g,'');if(!n){return '';}var s=Number(n).toLocaleString('en-US');return HE?s+' ₪'+(deal==='rent'?' לחודש':''):'₪'+s+(deal==='rent'?' a month':'');}
function summaryTitle(f){
 var rooms=String(f.rooms||'').replace(',','.').trim(),pt={apartment:'',garden:T.ptGarden,penthouse:T.ptPh,duplex:T.ptDuplex,house:T.ptHouse}[f.ptype]||'';
 var place=f.hood||f.city||'';
 if(HE){var head=rooms?(pt?pt+' '+rooms+' חדרים':'דירת '+rooms+' חדרים'):(pt||'טיוטה');return place?head+' '+(/^[֐-׿]/.test(place)?'ב':'ב-')+place:head;}
 var h2=rooms?rooms+'-room '+(pt?pt.toLowerCase():'apartment'):(pt||'Draft');return place?h2+' in '+place:h2;
}

/* ---- the app frame ---- */
render.frame=function(inner){
 var bar='<div class="nlj-bar" role="navigation" aria-label="'+esc(T.navAria)+'">';
 if(C.uid){bar+='<button class="nlj-btn nlj-btn--quiet" type="button" data-act="go-mine">'+esc(T.myListings)+'</button><span class="nlj-avatar" role="img" aria-label="'+esc(T.acct(C.name||''))+'">'+esc((C.name||'·').slice(0,1))+'</span>';}
 else if(S.auth!=='login'){bar+='<button class="nlj-btn nlj-btn--quiet" type="button" data-act="tab-login">'+esc(T.signInTop)+'</button>';}
 bar+='</div>';
 root.innerHTML='<div class="nlj-wrap">'+bar+inner+'</div>';
};
render.screen=function(){
 var s=S.screen;
 if(s==='auth'){return renderAuth();}
 if(s==='home'){return renderHome();}
 if(s==='details'||s==='photos'||s==='preview'){return renderFlow();}
 if(s==='published'){return renderPublished();}
 if(s==='mine'){return renderMine();}
 if(s==='promote'){return renderPromote();}
 render.frame('<div class="nlj-loading" role="status">…</div>');
};

/* ---------------- 1. account ---------------- */
function fieldErr(id,msg){return msg?'<p class="nlj-err" id="'+id+'-err" role="alert">'+ICO.err+'<span>'+esc(msg)+'</span></p>':'';}
function renderAuth(){
 var a=S.auth,e=S.authErr||{},h='';
 h+='<div class="nlj-cols"><div class="nlj-main"><div class="nlj-head" data-focus><p class="nlj-kick">'+esc(T.authKick)+'</p><h2 class="nlj-h1">'+esc(T.authH1)+'</h2><p class="nlj-lead">'+esc(T.authLead)+'</p></div><div class="nlj-card">';
 h+='<div class="nlj-tabs" role="group" aria-label="'+esc(T.authTabsAria)+'"><button class="nlj-tab" type="button" aria-pressed="'+(a==='signup')+'" data-act="tab-signup">'+esc(T.tabSignup)+'</button><button class="nlj-tab" type="button" aria-pressed="'+(a!=='signup')+'" data-act="tab-login">'+esc(T.tabLogin)+'</button></div>';
 if(a==='signup'){
  h+='<form class="nlj-form" id="nlj-signup" novalidate>';
  h+='<div class="nlj-field"><label class="nlj-label" for="j-name">'+esc(T.firstName)+'</label><input class="nlj-input'+(e.name?' is-bad':'')+'" id="j-name" name="name" autocomplete="given-name" value="'+esc(S.authName)+'"'+(e.name?' aria-invalid="true" aria-describedby="j-name-err"':'')+'>'+fieldErr('j-name',e.name)+'</div>';
  h+='<div class="nlj-field"><label class="nlj-label" for="j-mail">'+esc(T.email)+'</label><input class="nlj-input is-ltr'+(e.email?' is-bad':'')+'" id="j-mail" name="email" type="email" autocomplete="email" inputmode="email" value="'+esc(S.authMail)+'"'+(e.email?' aria-invalid="true" aria-describedby="j-mail-err"':'')+'>';
  if(e.email){h+='<div class="nlj-err" id="j-mail-err" role="alert">'+ICO.err+'<div style="display:flex;flex-direction:column;gap:6px"><span>'+esc(e.email)+'</span>'+(e.exists?'<button class="nlj-btn nlj-btn--quiet" type="button" data-act="exists-login" style="align-self:flex-start;padding-inline:0">'+esc(T.mailExistsAct)+'</button>':'')+'</div></div>';}
  h+='</div>';
  h+='<div class="nlj-field"><label class="nlj-label" for="j-pw">'+esc(T.password)+'</label><div class="nlj-pw"><input class="nlj-input is-ltr'+(e.password?' is-bad':'')+'" id="j-pw" name="password" type="password" autocomplete="new-password" aria-describedby="j-pw-hint'+(e.password?' j-pw-err':'')+'"'+(e.password?' aria-invalid="true"':'')+'><button class="nlj-btn nlj-btn--secondary nlj-btn--sm" type="button" data-act="pw" data-for="j-pw" aria-pressed="false">'+esc(T.showPw)+'</button></div><p class="nlj-hint" id="j-pw-hint">'+esc(T.pwHint)+'</p>'+fieldErr('j-pw',e.password)+'</div>';
  h+='<input type="text" name="website" id="j-web" tabindex="-1" autocomplete="off" class="nlj-file" aria-hidden="true">';
  var sp=HE?'':' ';
  h+='<p class="nlj-small">'+esc(T.termsA)+sp+'<a href="'+esc(C.terms)+'" target="_blank" rel="noopener">'+esc(T.terms)+'</a> '+esc(T.termsB)+sp+'<a href="'+esc(C.privacy)+'" target="_blank" rel="noopener">'+esc(T.privacy)+'</a>.</p>';
  if(e.form){h+=fieldErr('j-form',e.form);}
  h+='<div class="nlj-actions"><button class="nlj-btn nlj-btn--primary" type="submit" id="j-signup-go">'+esc(T.signupCta)+'</button></div></form>';
 }else if(a==='login'){
  h+='<form class="nlj-form" id="nlj-login" novalidate>';
  h+='<div class="nlj-field"><label class="nlj-label" for="j-mail2">'+esc(T.email)+'</label><input class="nlj-input is-ltr" id="j-mail2" name="email" type="email" autocomplete="username" inputmode="email" value="'+esc(S.authMail)+'"></div>';
  h+='<div class="nlj-field"><label class="nlj-label" for="j-pw2">'+esc(T.password)+'</label><div class="nlj-pw"><input class="nlj-input is-ltr" id="j-pw2" name="password" type="password" autocomplete="current-password"><button class="nlj-btn nlj-btn--secondary nlj-btn--sm" type="button" data-act="pw" data-for="j-pw2" aria-pressed="false">'+esc(T.showPw)+'</button></div></div>';
  if(e.form){h+=fieldErr('j-form',e.form);}
  h+='<div class="nlj-actions"><button class="nlj-btn nlj-btn--primary" type="submit" id="j-login-go">'+esc(T.loginCta)+'</button><button class="nlj-btn nlj-btn--quiet" type="button" data-act="tab-recover">'+esc(T.forgot)+'</button></div></form>';
 }else{
  var wait=Math.max(0,Math.ceil((S.recUntil-Date.now())/1000));
  h+='<form class="nlj-form" id="nlj-recover" novalidate><div style="display:flex;flex-direction:column;gap:6px"><h3>'+esc(T.recH)+'</h3><p class="nlj-small">'+esc(T.recLead)+'</p></div>';
  h+='<div class="nlj-field"><label class="nlj-label" for="j-mail3">'+esc(T.email)+'</label><input class="nlj-input is-ltr'+(e.email?' is-bad':'')+'" id="j-mail3" name="email" type="email" autocomplete="email" inputmode="email" value="'+esc(S.authMail)+'">'+fieldErr('j-mail3',e.email)+'</div>';
  if(S.recSent){h+=statusBox('ok',ICO.mail,T.recSentH,T.recSent,'','status');}
  if(e.form){h+=fieldErr('j-form',e.form);}
  h+='<div class="nlj-actions"><button class="nlj-btn nlj-btn--primary" type="submit" id="j-rec-go"'+(wait?' disabled':'')+'>'+esc(wait?T.recWait(wait):T.recSend)+'</button><button class="nlj-btn nlj-btn--quiet" type="button" data-act="tab-login">'+esc(T.backLogin)+'</button></div></form>';
 }
 h+='</div><p class="nlj-small">'+esc(T.brokerLine)+' <a href="'+esc(C.brokers)+'">'+esc(T.brokerLink)+'</a></p></div>';
 h+='<aside class="nlj-aside" aria-label="'+esc(T.howAria)+'"><div class="nlj-card nlj-card--sand"><h2>'+esc(T.howH)+'</h2><ol class="nlj-steps"><li><span class="nlj-dot">1</span>'+esc(T.how1)+'</li><li><span class="nlj-dot">2</span>'+esc(T.how2)+'</li><li><span class="nlj-dot">3</span>'+esc(T.how3)+'</li></ol><p class="nlj-small">'+esc(T.howNote)+'</p></div></aside></div>';
 render.frame(h);
 if(S.auth==='recover'&&S.recUntil>Date.now()){setTimeout(function(){if(S.screen==='auth'&&S.auth==='recover'){var b=$('j-rec-go'),w=Math.max(0,Math.ceil((S.recUntil-Date.now())/1000));if(b){b.disabled=w>0;b.textContent=w?T.recWait(w):T.recSend;}if(w>0){renderAuthTick();}}},1000);}
}
function renderAuthTick(){setTimeout(function(){if(S.screen==='auth'&&S.auth==='recover'){var b=$('j-rec-go'),w=Math.max(0,Math.ceil((S.recUntil-Date.now())/1000));if(b){b.disabled=w>0;b.textContent=w?T.recWait(w):T.recSend;}if(w>0){renderAuthTick();}}},1000);}
function authKeep(){var n=$('j-name'),m=$('j-mail')||$('j-mail2')||$('j-mail3');if(n){S.authName=n.value;}if(m){S.authMail=m.value;}}
function authSubmit(kind){
 authKeep();
 var e={},btn=null;
 if(kind==='signup'){
  var pw=$('j-pw').value;
  if(!S.authName.trim()){e.name=HE?'כותבים שם פרטי.':'Type your first name.';}
  if(!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(S.authMail.trim())){e.email=HE?'כותבים כתובת מייל תקינה.':'Type a valid email address.';}
  if(pw.length<8){e.password=HE?'סיסמה של 8 תווים לפחות, שאינה נפוצה.':'A password of at least 8 characters that is not a common one.';}
  if(e.name||e.email||e.password){S.authErr=e;renderAuth();focusFirstErr();return;}
  btn=$('j-signup-go');btn.disabled=true;btn.textContent=T.signupBusy;
  pub('/account/signup',{name:S.authName.trim(),email:S.authMail.trim(),password:pw,website:($('j-web')||{}).value||''}).then(function(x){
   if(x.ok){authPing();location.reload();return;}
   var f=(x.j.data&&x.j.data.field)||'',m=x.j.message||(x.net?T.netErr:T.genericErr),ee={};
   if(x.j.code==='acc_exists'){ee.email=m;ee.exists=true;}else if(f){ee[f]=m;}else{ee.form=m;}
   S.authErr=ee;renderAuth();var p=$('j-pw');if(p){p.value=pw;}focusFirstErr();
  });
 }else if(kind==='login'){
  var pw2=$('j-pw2').value;
  btn=$('j-login-go');btn.disabled=true;btn.textContent=T.loginBusy;
  pub('/account/login',{email:S.authMail.trim(),password:pw2}).then(function(x){
   if(x.ok){authPing();location.reload();return;}
   S.authErr={form:x.j.message||(x.net?T.netErr:T.genericErr)};renderAuth();var p=$('j-pw2');if(p){p.value=pw2;}focusFirstErr();
  });
 }else{
  if(!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(S.authMail.trim())){S.authErr={email:HE?'כותבים כתובת מייל תקינה.':'Type a valid email address.'};renderAuth();focusFirstErr();return;}
  btn=$('j-rec-go');btn.disabled=true;
  pub('/account/recover',{email:S.authMail.trim(),back:C.page}).then(function(x){
   if(x.ok){S.recSent=true;S.recUntil=Date.now()+60000;S.authErr={};renderAuth();var st=root.querySelector('.nlj-status');if(st){st.setAttribute('tabindex','-1');st.focus();}return;}
   S.authErr={form:x.j.message||(x.net?T.netErr:T.genericErr)};renderAuth();focusFirstErr();
  });
 }
}
function focusFirstErr(){var el=root.querySelector('.is-bad,[aria-invalid="true"]')||root.querySelector('.nlj-err');if(el){if(!/INPUT|TEXTAREA|SELECT/.test(el.tagName)){el.setAttribute('tabindex','-1');}el.focus();}}

/* ---------------- 2. a saved draft ---------------- */
function renderHome(){
 var d=S.drafts[0];
 if(!d){return go('details',{replace:true});}
 var stepN={details:2,photos:3,preview:4}[d.step]||2,h='';
 h+='<div class="nlj-head" data-focus style="max-width:760px"><p class="nlj-kick">'+esc(T.draftKick(C.name||''))+'</p><h2 class="nlj-h1">'+esc(T.draftH1)+'</h2><p class="nlj-lead">'+esc(T.draftLead)+'</p></div>';
 h+='<div class="nlj-card" style="max-width:760px"><div class="nlj-item-top"><div class="nlj-thumb">'+(d.photos&&d.photos[0]?'<img alt="" src="'+esc(d.photos[0].thumb)+'">':ICO.house)+'</div><div style="display:flex;flex-direction:column;gap:6px;min-width:0"><span class="nlj-chip" style="align-self:flex-start">'+esc(T.chipDraft)+'</span><h3>'+esc(d.summary.title)+'</h3>'+(d.summary.place?'<p class="nlj-small">'+esc(d.summary.place)+'</p>':'')+'<p class="nlj-meta">'+esc(T.draftSaved(fdate(d.saved_at)))+'</p></div></div>';
 var bars='';for(var i=1;i<=5;i++){bars+='<i class="'+(i<stepN?'is-done':(i===stepN?'is-now':''))+'"></i>';}
 h+='<div class="nlj-prog5"><div class="nlj-prog5-top"><b>'+esc(T.draftStep(stepN))+'</b><span>'+esc(T.draftNext(T.stepNames[Math.min(4,stepN)]))+'</span></div><div class="nlj-bars" aria-hidden="true">'+bars+'</div></div>';
 h+='<div class="nlj-actions"><button class="nlj-btn nlj-btn--primary" type="button" data-act="home-continue">'+esc(T.draftContinue)+'</button><button class="nlj-btn nlj-btn--secondary" type="button" data-act="home-new">'+esc(T.draftNew)+'</button></div><p class="nlj-hint">'+esc(T.draftNewNote)+'</p>'+perAccount();
 if(S.drafts.length>1){h+='<p class="nlj-hint">'+esc(T.otherDrafts(S.drafts.length-1))+' <button class="nlj-btn nlj-btn--quiet" type="button" data-act="go-mine" style="padding-inline:0;min-height:44px">'+esc(T.myListings)+'</button></p>';}
 h+='<hr class="nlj-hr">';
 if(S.del==='closed'||S.del==='failed'){h+='<button class="nlj-btn nlj-btn--quiet nlj-btn--bad" type="button" data-act="del-ask" style="align-self:flex-start">'+esc(T.draftDelete)+'</button>';}
 if(S.del==='failed'){h+=statusBox('bad',ICO.retry,T.delFailH,T.delFail,'','alert');}
 if(S.del==='ask'){h+='<div class="nlj-confirm" role="group" aria-label="'+esc(T.draftDelete)+'" id="nlj-del"><b>'+esc(T.delAskH)+'</b><p class="nlj-small" style="color:#14212b">'+esc(T.delAskTxt)+'</p><div class="nlj-item-acts"><button class="nlj-btn nlj-btn--danger nlj-btn--sm" type="button" data-act="del-run">'+esc(T.delYes)+'</button><button class="nlj-btn nlj-btn--secondary nlj-btn--sm" type="button" data-act="del-no">'+esc(T.cancel)+'</button></div></div>';}
 if(S.del==='running'){h+=statusBox('',ICO.spin,T.delRunH,T.delRunTxt,'','status');}
 h+='</div>';
 render.frame(h);
}

/* ---------------- 3-5. details, photos, preview ---------------- */
function perAccount(){return '<p class="nlj-hint nlj-peracct">'+esc(T.perAccount)+(C.logout?' <a href="'+esc(C.logout)+'" data-signout="1">'+esc(T.otherAccount)+'</a>':'')+'</p>';}
root.addEventListener('click',function(e){var a=e.target.closest&&e.target.closest('a[data-signout]');if(a){flush({keepalive:true});authPing();}},true);
function renderFlow(){
 var s=S.screen,n={details:2,photos:3,preview:4}[s],h='<div class="nlj-cols"><div class="nlj-main">'+progress(n)+'<div id="nlj-st" aria-live="polite"></div>';
 if(s==='details'){h+=detailsHtml();}
 else if(s==='photos'){h+=photosHtml();}
 else{h+='<div id="nlj-pv">'+previewHtml()+'</div>';}
 h+='</div><aside class="nlj-aside" id="nlj-aside" aria-label="'+esc(T.asideAria)+'"></aside></div>';
 render.frame(h);
 render.status();render.aside();
 if(s==='photos'){renderTiles();}
 if(s==='preview'&&!S.preview){loadPreview();}
}
function v(k){return D.fields[k]==null?'':D.fields[k];}
function errOf(k){return S.showErr?S.errors[k]:'';}
function inp(id,k,label,o){
 o=o||{};var e=errOf(k);
 var a='<div class="nlj-field"><label class="nlj-label" for="'+id+'">'+esc(label)+(o.opt?' <span class="nlj-opt">'+esc(o.opt)+'</span>':'')+'</label>';
 var input='<input class="nlj-input'+(o.ltr?' is-ltr':'')+(e?' is-bad':'')+'" id="'+id+'" data-f="'+k+'" value="'+esc(v(k))+'"'+(o.attrs||'')+(e?' aria-invalid="true"':'')+' aria-describedby="'+(o.hint?id+'-hint ':'')+(e?id+'-err':'')+'">';
 a+=o.affix?'<div class="nlj-affix">'+input+'<span>'+esc(o.affix)+'</span></div>':input;
 if(o.hint){a+='<p class="nlj-hint" id="'+id+'-hint">'+esc(o.hint)+'</p>';}
 return a+fieldErr(id,e)+'</div>';
}
var FID={deal:'j-deal',ptype:'j-type',city:'j-city',hood:'j-hood',rooms:'j-rooms',size:'j-size',floor:'j-floor',price:'j-price',desc:'j-desc',cname:'j-cname',phone:'j-phone',phone_ok:'j-phone-ok',owner_ok:'j-owner-ok',photos:'j-add'};
function errSummary(keys){
 var list=keys.filter(function(k){return S.errors[k];});
 if(!S.showErr||!list.length){return '';}
 return '<div class="nlj-errsum" id="nlj-errsum" role="alert" tabindex="-1"><b>'+esc(T.errSumH(list.length))+'</b><ul>'+list.map(function(k){return '<li><a href="#'+FID[k]+'" data-act="jump" data-k="'+k+'">'+esc(T.fn[k])+'</a>: '+esc(S.errors[k])+'</li>';}).join('')+'</ul></div>';
}
var DETAIL_KEYS=['deal','ptype','city','hood','rooms','size','floor','price','desc','cname','phone','owner_ok'];
function detailsHtml(){
 var f=D.fields,h='';
 h+='<div class="nlj-head" data-focus><h2 class="nlj-h1">'+esc(T.detH1)+'</h2><p class="nlj-lead">'+esc(T.detLead)+'</p></div>';
 if(!C.engine){h+=statusBox('warn',ICO.info.replace('width="18" height="18"','class="nlj-st-ico"'),T.engineOff,'','','status');}
 h+=errSummary(DETAIL_KEYS);
 h+='<form class="nlj-card nlj-form" id="nlj-details" novalidate aria-label="'+esc(T.detH1)+'">';
 h+='<fieldset id="j-deal" style="border:0;margin:0;padding:0;display:flex;flex-direction:column;gap:8px" tabindex="-1"'+(errOf('deal')?' aria-describedby="j-deal-err"':'')+'><legend class="nlj-label" style="padding:0;margin-bottom:8px">'+esc(T.dealType)+'</legend><div class="nlj-seg"><button class="nlj-pill" type="button" data-deal="sale" aria-pressed="'+(f.deal==='sale')+'">'+esc(T.sale)+'</button><button class="nlj-pill" type="button" data-deal="rent" aria-pressed="'+(f.deal==='rent')+'">'+esc(T.rent)+'</button></div>'+fieldErr('j-deal',errOf('deal'))+'</fieldset>';
 var pts=[['apartment',T.ptApt],['garden',T.ptGarden],['penthouse',T.ptPh],['duplex',T.ptDuplex],['house',T.ptHouse]],e=errOf('ptype');
 h+='<div class="nlj-field"><label class="nlj-label" for="j-type">'+esc(T.propType)+'</label><select class="nlj-input'+(e?' is-bad':'')+'" id="j-type" data-f="ptype"'+(e?' aria-invalid="true" aria-describedby="j-type-err"':'')+'><option value="">'+esc(T.ptChoose)+'</option>'+pts.map(function(p){return '<option value="'+p[0]+'"'+(f.ptype===p[0]?' selected':'')+'>'+esc(p[1])+'</option>';}).join('')+'</select>'+fieldErr('j-type',e)+'</div>';
 h+='<div class="nlj-g2">'+inp('j-city','city',T.city,{attrs:' autocomplete="address-level2"'})+inp('j-hood','hood',T.hood,{})+'</div><p class="nlj-hint" style="margin-top:-10px">'+esc(T.addrHint)+'</p>';
 h+='<div class="nlj-g3">'+inp('j-rooms','rooms',T.rooms,{attrs:' inputmode="decimal"'})+inp('j-size','size',T.size,{attrs:' inputmode="numeric"',affix:T.sqm})+inp('j-floor','floor',T.floor,{opt:T.optional,attrs:' placeholder="'+esc(HE?'3 מתוך 8':'3 of 8')+'"'})+'</div>';
 h+=inp('j-price','price',f.deal==='rent'?T.priceRent:T.priceSale,{attrs:' inputmode="numeric"',affix:'₪',hint:T.priceHint});
 var de=errOf('desc');
 h+='<div class="nlj-field"><label class="nlj-label" for="j-desc">'+esc(T.desc)+'</label><textarea class="nlj-input'+(de?' is-bad':'')+'" id="j-desc" data-f="desc" rows="6" maxlength="1500" aria-describedby="j-desc-count j-desc-note'+(de?' j-desc-err':'')+'"'+(de?' aria-invalid="true"':'')+'>'+esc(v('desc'))+'</textarea><div class="nlj-counter" id="j-desc-count"><span>'+esc(T.descHint)+'</span><span class="nlj-num" id="j-desc-n">'+String(v('desc')).length.toLocaleString('en-US')+' / 1,500</span></div>'+fieldErr('j-desc',de)+'<div class="nlj-note" id="j-desc-note">'+ICO.info+'<span>'+esc(T.fairNote)+'</span></div></div>';
 h+='<hr class="nlj-hr"><h3>'+esc(T.contactH)+'</h3>';
 h+='<div class="nlj-g2">'+inp('j-cname','cname',T.contactName,{attrs:' autocomplete="given-name" maxlength="30"'})+inp('j-phone','phone',T.phone,{ltr:true,opt:f.phone_ok?'':T.phoneOpt,attrs:' type="tel" autocomplete="tel" inputmode="tel" maxlength="20"'})+'</div>';
 h+='<label class="nlj-check"><input type="checkbox" id="j-phone-ok" data-f="phone_ok"'+(f.phone_ok?' checked':'')+'><span>'+esc(T.showPhone)+'<small>'+esc(T.showPhoneSub)+'</small></span></label>';
 var oe=errOf('owner_ok');
 h+='<label class="nlj-check"><input type="checkbox" id="j-owner-ok" data-f="owner_ok"'+(f.owner_ok?' checked':'')+(oe?' aria-invalid="true" aria-describedby="j-owner-ok-err"':'')+'><span>'+esc(T.ownerDecl)+'<small>'+esc(T.ownerDeclSub)+'</small></span></label>'+fieldErr('j-owner-ok',oe);
 h+='<div class="nlj-actions"><button class="nlj-btn nlj-btn--primary" type="submit" id="j-to-photos">'+esc(T.toPhotos)+ICO.fwd+'</button><button class="nlj-btn nlj-btn--quiet" type="button" data-act="save-exit">'+esc(T.saveExit)+'</button></div>';
 h+='</form>'+perAccount()+'<p class="nlj-small">'+esc(T.brokerHint)+' <a href="'+esc(C.brokers)+'">'+esc(T.brokerLink)+'</a></p>';
 return h;
}
function clientCheck(keys){
 var f=D.fields,e={};
 if(!f.deal){e.deal=1;}if(!f.ptype){e.ptype=1;}if(!String(f.city).trim()){e.city=1;}if(!String(f.hood).trim()){e.hood=1;}
 if(!String(f.rooms).trim()){e.rooms=1;}if(!String(f.size).trim()){e.size=1;}if(!String(f.price).trim()){e.price=1;}
 if(String(f.desc).trim().length<20){e.desc=1;}if(!String(f.cname).trim()){e.cname=1;}if(!f.owner_ok){e.owner_ok=1;}
 var out={};keys.forEach(function(k){if(e[k]){out[k]=(W[LANG].fn[k])+': '+(HE?'חסר':'missing');}});return out;
}
function detailsNext(){
 var btn=$('j-to-photos');if(btn){btn.disabled=true;btn.firstChild.textContent=T.checking;}
 var done=function(errors){
  S.errors=errors||{};
  var keys=Object.keys(S.errors).filter(function(k){return DETAIL_KEYS.indexOf(k)>-1;});
  if(keys.length){S.showErr=true;render.screen();var sm=$('nlj-errsum');if(sm){sm.focus();}return;}
  S.errors={};S.showErr=false;go('photos');
 };
 flush({create:true}).then(function(ok){
  if(!D.id||!online()){
   if(btn){btn.disabled=false;btn.firstChild.textContent=T.toPhotos;}
   var ce=clientCheck(DETAIL_KEYS);if(Object.keys(ce).length){done(ce);}else{go('photos');}
   return;
  }
  call('POST','/draft/'+D.id+'/check',{only:DETAIL_KEYS}).then(function(x){
   if(btn){btn.disabled=false;btn.firstChild.textContent=T.toPhotos;}
   if(x.ok){done(x.j.errors||{});}else{var ce=clientCheck(DETAIL_KEYS);if(Object.keys(ce).length){done(ce);}else{go('photos');}}
  });
 });
}

/* ---- photos ---- */
function photosHtml(){
 var okn=P.filter(function(t){return t.s!=='err';}).length,h='';
 h+='<div class="nlj-head" data-focus><h2 class="nlj-h1">'+esc(T.phH1)+'</h2><p class="nlj-lead">'+esc(T.phLead)+'</p></div>';
 h+=errSummary(['photos']);
 h+='<div class="nlj-drop" id="j-drop"><input type="file" id="j-files" class="nlj-file" accept="image/*,.heic,.heif" multiple tabindex="-1" aria-hidden="true">'+ICO.pic+'<button class="nlj-btn nlj-btn--secondary" type="button" id="j-add" data-act="add-photos">'+esc(T.addPhotos)+'</button><p class="nlj-hint">'+esc(T.phDropHint)+'</p><p class="nlj-label" aria-live="polite"><span class="nlj-num" id="j-phn">'+esc(T.phCount(okn,MAXP))+'</span></p></div>';
 h+='<p class="nlj-hint">'+esc(T.phOrderHint)+'</p><div id="j-phmsg" role="status" aria-live="polite"></div>';
 h+='<ul class="nlj-ph" id="j-tiles" aria-label="'+esc(T.phListAria)+'"></ul>';
 h+='<div class="nlj-actions"><button class="nlj-btn nlj-btn--primary" type="button" data-act="to-preview" id="j-to-preview">'+esc(T.toPreview)+ICO.fwd+'</button><button class="nlj-btn nlj-btn--quiet" type="button" data-act="back-details">'+esc(T.backDetails)+'</button></div>';
 h+=perAccount();
 return h;
}
function tileLabel(i){return T.photoN(i+1);}
function renderTiles(){
 var ul=$('j-tiles');if(!ul){return;}
 var vis=P.filter(function(t){return !t.removed;}),n=$('j-phn');
 if(n){n.textContent=T.phCount(vis.filter(function(t){return t.s!=='err';}).length,MAXP);}
 ul.innerHTML=vis.map(function(t,i){
  var lab=tileLabel(i),img=(t.thumb||t.preview)?'<img alt="" src="'+esc(t.thumb||t.preview)+'" loading="lazy" decoding="async">':ICO.bld;
  var h='<li><div class="nlj-tile'+(t.s==='err'?' is-fail':'')+'" data-k="'+t.k+'"><div class="nlj-img">'+img+(i===0&&t.s!=='err'?'<span class="nlj-cover">'+esc(T.coverBadge)+'</span>':'')+'<span class="nlj-cap">'+esc(lab)+'</span></div>';
  if(t.s==='ok'){
   h+='<div class="nlj-tilebar"><div class="nlj-grp"><button class="nlj-ibtn" type="button" data-act="ph-up" data-k="'+t.k+'" aria-label="'+esc(T.earlier+lab)+'"'+(i===0?' disabled':'')+'>'+ICO.prev+'</button><button class="nlj-ibtn" type="button" data-act="ph-down" data-k="'+t.k+'" aria-label="'+esc(T.later+lab)+'"'+(i===vis.length-1?' disabled':'')+'>'+ICO.next+'</button></div><div class="nlj-grp">'+(i>0?'<button class="nlj-ibtn" type="button" data-act="ph-cover" data-k="'+t.k+'" aria-label="'+esc(T.makeCover+lab)+'">'+ICO.star+'</button>':'')+'<button class="nlj-ibtn" type="button" data-act="ph-rm" data-k="'+t.k+'" aria-label="'+esc(T.remove+lab)+'">'+ICO.bin+'</button></div></div>';
  }else if(t.s==='err'){
   h+='<div class="nlj-fail" role="alert"><span>'+esc(T.upFail)+' '+esc(t.err||'')+'</span><div class="nlj-grp">'+(t.file&&t.retry!==false?'<button class="nlj-btn nlj-btn--secondary nlj-btn--sm" type="button" data-act="ph-retry" data-k="'+t.k+'">'+esc(T.tryAgain)+'</button>':'')+'<button class="nlj-ibtn" type="button" data-act="ph-rm" data-k="'+t.k+'" aria-label="'+esc(T.remove+lab)+'">'+ICO.bin+'</button></div></div>';
  }else{
   h+='<div class="nlj-up" role="status"><span>'+esc(T.uploading)+' <span class="nlj-num">'+(t.pct||0)+'%</span></span><div class="nlj-upbar"><i style="width:'+(t.pct||0)+'%"></i></div><div class="nlj-grp"><button class="nlj-ibtn" type="button" data-act="ph-rm" data-k="'+t.k+'" aria-label="'+esc(T.remove+lab)+'">'+ICO.bin+'</button></div></div>';
  }
  return h+'</div></li>';
 }).join('');
 render.aside();
}
function phMsg(t){var m=$('j-phmsg');if(m){m.innerHTML=t?'<p class="nlj-note">'+ICO.info+'<span>'+esc(t)+'</span></p>':'';}}
var active=0;
function addFiles(list){
 var vis=P.filter(function(t){return !t.removed;}).length,over=false;
 Array.prototype.forEach.call(list||[],function(f){
  if(vis>=MAXP){over=true;return;}
  var okType=/^image\//.test(f.type)||/\.(heic|heif|jpe?g|png|webp)$/i.test(f.name),t={k:++tileSeq,s:'wait',file:f,pct:0};
  try{t.preview=URL.createObjectURL(f);}catch(e){}
  if(!okType){t.s='err';t.err=T.upErr.type;t.retry=false;}
  P.push(t);vis++;
 });
 phMsg(over?T.tooMany:'');
 renderTiles();pump();
}
function pump(){
 if(!D.id){if(!saving){phMsg(T.photosNeedDraft);flush({create:true}).then(function(){if(D.id){phMsg('');pump();}});}return;}
 while(active<2){var t=P.filter(function(x){return x.s==='wait'&&!x.removed;})[0];if(!t){break;}upload(t);}
}
function shrink(file){
 return new Promise(function(res){
  var url,img=new Image();
  try{url=URL.createObjectURL(file);}catch(e){res(file);return;}
  img.onload=function(){try{var max=2400,w=img.naturalWidth,h=img.naturalHeight,s=Math.min(1,max/Math.max(w,h)),c=document.createElement('canvas');c.width=Math.round(w*s);c.height=Math.round(h*s);c.getContext('2d').drawImage(img,0,0,c.width,c.height);c.toBlob(function(b){URL.revokeObjectURL(url);res(b||file);},'image/jpeg',0.86);}catch(e){URL.revokeObjectURL(url);res(file);}};
  img.onerror=function(){URL.revokeObjectURL(url);res(file);};
  img.src=url;
 });
}
function upErrText(status,code,timeout,net){
 if(timeout){return T.upErr.timeout;}
 if(net||status===0){return T.upErr.net;}
 if(status===413||code==='big'){return T.upErr.big;}
 if(code==='heic'){return T.upErr.heic;}
 if(code==='orient'){return T.upErr.orient;}
 if(status===415||code==='type'){return T.upErr.type;}
 if(status===422||code==='corrupt'){return T.upErr.corrupt;}
 if(status===401||status===403){return T.upErr.auth;}
 if(status===429){return T.upErr.rate;}
 return T.upErr.server;
}
function upload(t,again2){
 active++;t.s='up';t.pct=0;renderTiles();
 shrink(t.file).then(function(blob){
  if(t.removed){active--;pump();return;}
  if(blob===t.file&&t.file.size>MAXB){active--;t.s='err';t.err=T.upErr.big;renderTiles();pump();return;}
  var fd=new FormData();fd.append('photo',blob,blob===t.file?t.file.name:'photo.jpg');fd.append('draft',String(D.id));fd.append('lang',LANG);
  var x=new XMLHttpRequest();t.xhr=x;
  x.open('POST',C.api+'/photo');x.setRequestHeader('X-WP-Nonce',C.nonce||'');x.withCredentials=true;x.timeout=90000;
  x.upload.onprogress=function(e){if(e.lengthComputable){t.pct=Math.min(99,Math.round(e.loaded/e.total*100));var el=root.querySelector('[data-k="'+t.k+'"] .nlj-upbar i'),nm=root.querySelector('[data-k="'+t.k+'"] .nlj-up .nlj-num');if(el){el.style.width=t.pct+'%';}if(nm){nm.textContent=t.pct+'%';}}};
  var fin=function(status,j,timeout,net){
   active--;t.xhr=null;
   if(status===200&&j&&j.ref){
    t.s='ok';t.ref=j.ref;t.thumb=j.thumb;t.full=j.full;t.w=j.w;t.h=j.h;t.pct=100;
    if(t.removed){D.discard.push(j.ref);}
    touch();
   }else if((status===401||status===403)&&!again2&&C.uid){
    refreshNonce().then(function(ok){if(ok&&!t.removed){upload(t,true);}else{t.s='err';t.err=upErrText(status,j&&j.code);renderTiles();}});return;
   }else{t.s='err';t.err=upErrText(status,j&&j.code,timeout,net);}
   renderTiles();pump();
  };
  x.onload=function(){var j=null;try{j=JSON.parse(x.responseText);}catch(e){}fin(x.status,j);};
  x.ontimeout=function(){fin(0,null,true,false);};
  x.onerror=function(){fin(0,null,false,true);};
  x.onabort=function(){active--;t.xhr=null;pump();};
  x.send(fd);
 });
}
function tileBy(k){k=+k;for(var i=0;i<P.length;i++){if(P[i].k===k){return P[i];}}return null;}
function visIndex(t){return P.filter(function(x){return !x.removed;}).indexOf(t);}
function moveTile(t,d){
 var vis=P.filter(function(x){return !x.removed;}),i=vis.indexOf(t),j=i+d;if(j<0||j>=vis.length){return;}
 var a=P.indexOf(vis[i]),b=P.indexOf(vis[j]),tmp=P[a];P[a]=P[b];P[b]=tmp;
}

/* ---- preview and publish ---- */
function previewHtml(){
 var x=S.preview,h='<div class="nlj-head" data-focus><h2 class="nlj-h1">'+esc(T.pvH1)+'</h2><p class="nlj-lead">'+esc(T.pvLead)+'</p></div>';
 if(!x){return h+'<div class="nlj-loading" role="status">'+esc(online()?T.pvLoading:T.pvOffline)+'</div>';}
 if(x.offline){return h+'<p class="nlj-note">'+ICO.info+'<span>'+esc(T.pvOffline)+'</span></p>';}
 var edit=!!(D.listing&&D.listing.status!=='trash');
 h+='<div class="nlj-banner" role="note">'+ICO.eye+esc(edit?T.pvBannerEdit:T.pvBanner)+'</div>';
 var errs=Object.keys(x.errors||{});
 if(errs.length){h+='<div class="nlj-errsum" role="alert" id="nlj-errsum" tabindex="-1"><b>'+esc(T.pvErrH)+'</b><ul>'+errs.map(function(k){return '<li>'+esc(T.fn[k]||k)+': '+esc(x.errors[k])+' <button class="nlj-btn nlj-btn--quiet" type="button" data-act="fix" data-k="'+esc(k)+'" style="min-height:44px">'+esc(T.fix)+'</button></li>';}).join('')+'</ul></div>';}
 var cover=x.photos&&x.photos[0];
 h+='<article class="nlj-lcard" aria-label="'+esc(T.pvAria)+'"><div class="nlj-img">'+(cover?'<img alt="'+esc(x.title)+'" src="'+esc(cover.full)+'">':ICO.bld)+'<span class="nlj-cap">'+esc(T.pvCap)+'</span></div><div class="nlj-lbody">';
 h+='<div style="display:flex;flex-wrap:wrap;gap:8px"><span class="nlj-chip nlj-chip--owner">'+esc(T.fromOwner)+'</span>'+(x.deal?'<span class="nlj-chip">'+esc(x.deal==='rent'?T.rent:T.sale)+'</span>':'')+'</div>';
 h+='<h3 class="nlj-serif" style="font-size:24px">'+esc(x.title)+'</h3>'+(x.place?'<p class="nlj-small">'+esc(x.place)+'</p>':'')+(x.price?'<p class="nlj-price"><span class="nlj-num">'+esc(x.price)+'</span></p>':'');
 if(x.facts&&x.facts.length){h+='<div class="nlj-facts">'+x.facts.map(function(f){return '<span class="nlj-fact">'+esc(f)+'</span>';}).join('')+'</div>';}
 (x.desc||[]).forEach(function(p){h+='<p style="font-size:16px;line-height:1.65;color:#3b4753">'+esc(p)+'</p>';});
 if(x.contact&&x.contact.buttons){h+='<div class="nlj-actions" style="flex-direction:row;flex-wrap:wrap"><button class="nlj-btn nlj-btn--secondary nlj-btn--sm" type="button" disabled>'+esc(T.wa)+'</button><button class="nlj-btn nlj-btn--secondary nlj-btn--sm" type="button" disabled>'+esc(T.call)+' <span class="nlj-num">'+esc(x.contact.phone)+'</span></button></div><p class="nlj-hint">'+esc(T.pvBtnsNote)+'</p>';}
 else{h+='<p class="nlj-note">'+ICO.info+'<span>'+esc(T.pvNoContact)+'</span></p>';}
 if(x.hold){h+='<p class="nlj-note">'+ICO.info+'<span>'+esc(T.pvHold)+'</span></p>';}
 if(!HE){h+='<p class="nlj-hint">'+esc(T.pvLangNote)+'</p>';}
 h+='</div></article>';
 if(x.html){h+='<details class="nlj-full"><summary>'+esc(T.pvFull)+'</summary><div class="nlj-fullbody" dir="rtl" lang="he">'+x.html+'</div></details>';}
 var st=S.pub,sending=st&&(st.s==='sending'||st.s==='building');
 h+='<div class="nlj-card"><p class="nlj-label">'+esc(T.pvAddr)+'</p><div class="nlj-urlbox"><code>'+esc(String(x.url||'').replace(/^https?:\/\//,''))+'</code></div><p class="nlj-hint">'+esc(edit?T.pvAddrLive:T.pvAddrHint)+'</p>';
 h+='<div class="nlj-actions"><button class="nlj-btn nlj-btn--primary" type="button" data-act="publish" id="j-publish"'+(sending||errs.length?' disabled':'')+(sending?' aria-busy="true"':'')+'>'+esc(sending?T.sendingLabel:(edit?T.update:T.publish))+'</button><button class="nlj-btn nlj-btn--quiet" type="button" data-act="back-edit">'+esc(T.backEdit)+'</button></div>';
 if(st){
  if(st.s==='sending'){h+=statusBox('',ICO.spin,T.sendingH,T.sendingTxt,'','status');}
  else if(st.s==='building'){h+=statusBox('',ICO.spin,T.buildingH,T.buildingTxt,'','status');}
  else if(st.s==='lost'){h+=statusBox('bad',ICO.retry,T.lostH,T.lostTxt,'<button class="nlj-btn nlj-btn--secondary nlj-btn--sm" type="button" data-act="pub-again">'+esc(T.checkAgain)+'</button><button class="nlj-btn nlj-btn--quiet" type="button" data-act="go-mine">'+esc(T.myListings)+'</button>','alert');}
  else if(st.s==='error'){h+=statusBox('bad',ICO.retry,st.msg||T.genericErr,'','','alert');}
 }
 h+='<p class="nlj-hint">'+esc(T.publishNote)+'</p></div>';
 h+=perAccount();
 return h;
}
function loadPreview(){
 S.preview=null;var box=$('nlj-pv');if(box){box.innerHTML=previewHtml();}
 flush({create:true}).then(function(){
  if(!D.id||!online()){S.preview={offline:true};var b=$('nlj-pv');if(b){b.innerHTML=previewHtml();}return;}
  call('GET','/draft/'+D.id+'/preview').then(function(x){
   if(S.screen!=='preview'){return;}
   S.preview=x.ok?x.j:{offline:!online(),errors:{},title:'',photos:[]};
   if(x.ok&&x.j.rev!==D.rev&&!dirty()){D.rev=x.j.rev;}
   var b=$('nlj-pv');if(b){b.innerHTML=previewHtml();}
  });
 });
}
function pubKey(){
 var k='nlow:v2:u'+C.uid+':pub:'+D.id+':'+D.rev,v=store.get(k)||MEM[k];
 if(!v){v=rid();if(!store.set(k,v)){MEM[k]=v;}}
 return v;
}
function publish(){
 if(S.pub&&(S.pub.s==='sending'||S.pub.s==='building')){return;}
 flush().then(function(){
  if(dirty()){S.pub={s:'error',msg:T.stRetryH};redrawPv();return;}
  S.pub={s:'sending',key:pubKey(),rev:D.rev};redrawPv();sendPub();
 });
}
function redrawPv(){var b=$('nlj-pv');if(b){b.innerHTML=previewHtml();}}
function sendPub(){
 var st=S.pub;if(!st){return;}
 call('POST','/draft/'+D.id+'/publish',{request_key:st.key,rev:st.rev},{timeout:180000}).then(function(x){
  if(S.pub!==st){return;}
  if(x.ok&&x.status===202){st.s='building';redrawPv();setTimeout(function(){if(S.pub===st){sendPub();}},3000);return;}
  if(x.ok){S.published=x.j;S.pub=null;D.listing={id:x.j.he_id,url:x.j.url,status:x.j.state==='published'?'publish':x.j.state};D.pub_rev=x.j.rev;store.del('nlow:v2:u'+C.uid+':pub:'+D.id+':'+st.rev);go('published');return;}
  if(x.net){st.s='lost';redrawPv();return;}
  if(x.expired){st.s='error';st.msg=T.expiredH;setSave('expired');redrawPv();return;}
  if(x.status===422){S.pub=null;S.preview.errors=(x.j.data&&x.j.data.errors)||{};redrawPv();var sm=$('nlj-errsum');if(sm){sm.focus();}return;}
  if(x.status===409&&x.j.code==='changed'){S.pub=null;if(x.j.data&&x.j.data.server&&!dirty()){loadServer(x.j.data.server);}loadPreview();return;}
  st.s='error';st.msg=x.j.message||T.genericErr;redrawPv();
 });
}

/* ---------------- 6. published ---------------- */
function renderPublished(){
 var r=S.published||{},state=r.state,h='';
 var t1=state==='pending'?T.donePendingH1:(state==='draft'?T.doneDraftH1:(r.updated?T.doneUpdatedH1:T.doneH1));
 var t2=state==='pending'?T.donePendingLead:(state==='draft'?T.doneDraftLead:(r.updated?T.doneUpdatedLead:T.doneLead(fdate(r.published_at))));
 h+='<div class="nlj-card" style="max-width:760px;align-items:flex-start"><span class="nlj-okmark'+(state==='published'?'':' nlj-okmark--warn')+'">'+ICO.check+'</span><div class="nlj-head" data-focus><h2 class="nlj-h1">'+esc(t1)+'</h2><p class="nlj-lead">'+esc(t2)+'</p></div>';
 if(state==='published'&&r.url){
  h+='<div class="nlj-urlbox" style="width:100%"><code id="j-url">'+esc(r.url.replace(/^https?:\/\//,''))+'</code><button class="nlj-btn nlj-btn--secondary nlj-btn--sm" type="button" data-act="copy">'+esc(T.copyLink)+'</button></div><p id="j-copied" role="status" class="nlj-hint"></p>';
  h+='<div class="nlj-actions" style="width:100%"><a class="nlj-btn nlj-btn--primary" href="'+esc(r.url)+'">'+esc(T.toListing)+'</a><a class="nlj-btn nlj-btn--secondary" href="https://wa.me/?text='+encodeURIComponent(r.url)+'" target="_blank" rel="noopener">'+esc(T.shareWa)+'</a><button class="nlj-btn nlj-btn--quiet" type="button" data-act="go-mine">'+esc(T.myListings)+'</button></div>';
 }else{h+='<div class="nlj-actions" style="width:100%"><button class="nlj-btn nlj-btn--primary" type="button" data-act="go-mine">'+esc(T.myListings)+'</button></div>';}
 h+='<hr class="nlj-hr"><p class="nlj-small">'+esc(T.doneManage)+'</p></div>';
 render.frame(h);
}

/* ---------------- 7. My listings ---------------- */
function renderMine(){
 var m=S.mine,h='';
 h+='<div style="display:flex;flex-wrap:wrap;gap:12px;align-items:flex-end;justify-content:space-between"><div class="nlj-head" data-focus><h2 class="nlj-h1">'+esc(T.mineH1)+'</h2>'+(m&&!m.fail?'<p class="nlj-small">'+esc(T.mineCount(m.active,m.max,m.drafts.length))+'</p>':'')+'</div><button class="nlj-btn nlj-btn--primary" type="button" data-act="mine-new">'+esc(T.newListing)+'</button></div>';
 h+='<div id="nlj-mine-msg" role="status" aria-live="polite"></div>';
 if(!m){h+='<div class="nlj-loading" role="status">…</div>';render.frame(h);loadMine();return;}
 if(m.fail){h+='<p class="nlj-note">'+ICO.info+'<span>'+esc(T.loadFail)+'</span></p>';render.frame(h);return;}
 var items=[];
 m.listings.forEach(function(L){items.push(listingItem(L));});
 m.drafts.forEach(function(d){items.push(draftItem(d));});
 h+=items.length?'<ul class="nlj-mine">'+items.map(function(x){return '<li>'+x+'</li>';}).join('')+'</ul>':'<p class="nlj-note">'+ICO.info+'<span>'+esc(T.mineEmpty)+'</span></p>';
 if(m.deleted.length){h+='<details class="nlj-deleted nlj-card"><summary>'+esc(T.deletedH)+' ('+m.deleted.length+')</summary><p class="nlj-hint">'+esc(T.deletedNote)+'</p><ul class="nlj-mine">'+m.deleted.map(function(d){return '<li><article class="nlj-item nlj-item--off"><div class="nlj-item-top"><div class="nlj-thumb">'+ICO.house+'</div><div style="display:flex;flex-direction:column;gap:6px;min-width:0;flex:1"><h3 style="font-size:18px">'+esc(d.summary.title)+'</h3><p class="nlj-small">'+esc(d.summary.place||'')+'</p></div></div><div class="nlj-item-acts"><button class="nlj-btn nlj-btn--secondary nlj-btn--sm" type="button" data-act="d-restore" data-id="'+d.id+'">'+esc(T.restore)+'</button></div></article></li>';}).join('')+'</ul></details>';}
 var live=m.listings.filter(function(L){return L.state==='active';});
 h+='<div class="nlj-card" style="gap:10px"><div style="display:flex;flex-wrap:wrap;gap:8px;align-items:center;justify-content:space-between"><h3>'+esc(T.promoH)+'</h3><span class="nlj-chip nlj-chip--off">'+esc(T.promoOff)+'</span></div><p class="nlj-small">'+esc(T.promoTeaser)+'</p><button class="nlj-btn nlj-btn--quiet" type="button" data-act="go-promote" style="align-self:flex-start;padding-inline:0">'+esc(T.promoMore)+'</button></div>';
 h+=perAccount();
 render.frame(h);
}
function chip(state){
 var map={active:['nlj-chip--live',T.chipLive],sold:['nlj-chip--off',T.chipSold],rented:['nlj-chip--off',T.chipRented],pending:['nlj-chip--warn',T.chipPending],removed:['nlj-chip--off',T.chipRemoved],draft:['',T.chipDraftTest]};
 var c=map[state]||map.draft;return '<span class="nlj-chip '+c[0]+'">'+esc(c[1])+'</span>';
}
function listingItem(L){
 var off=L.state!=='active'&&L.state!=='pending',h='<article class="nlj-item'+(off?' nlj-item--off':'')+'" id="L'+L.id+'"><div class="nlj-item-top"><div class="nlj-thumb">'+(L.cover?'<img alt="" src="'+esc(L.cover)+'">':ICO.house)+'</div><div style="display:flex;flex-direction:column;gap:6px;min-width:0;flex:1">';
 h+='<div style="display:flex;flex-wrap:wrap;gap:6px">'+chip(L.state)+'<span class="nlj-chip">'+esc(L.deal==='rent'?T.rent:T.sale)+'</span></div>';
 h+='<h3 style="font-size:19px">'+(L.url?'<a href="'+esc(L.url)+'">'+esc(L.title)+'</a>':esc(L.title))+'</h3>';
 var meta=[];if(L.price){meta.push('<span class="nlj-num">'+esc(L.price)+'</span>');}
 if(L.state==='active'){meta.push(esc(T.livedSince(fday(L.since))));}else if(L.state==='pending'){meta.push(esc(T.pendingNote));}else if(L.state==='removed'){meta.push(esc(T.removedNote));}else if(L.state==='sold'||L.state==='rented'){meta.push(esc(T.soldNote));}
 h+='<p class="nlj-small">'+meta.join(' · ')+'</p></div></div><div class="nlj-item-acts">';
 var ui=S.mineUi||{};
 if(L.state==='active'||L.state==='pending'){
  if(L.draft){h+='<button class="nlj-btn nlj-btn--secondary nlj-btn--sm" type="button" data-act="L-edit" data-id="'+L.id+'" data-draft="'+L.draft+'">'+esc(T.edit)+'</button>';}
  h+='<button class="nlj-btn nlj-btn--secondary nlj-btn--sm" type="button" data-act="L-price" data-id="'+L.id+'" aria-expanded="'+(ui.price===L.id)+'">'+esc(T.editPrice)+'</button>';
  if(L.state==='active'){h+='<button class="nlj-btn nlj-btn--secondary nlj-btn--sm" type="button" data-act="L-mark" data-id="'+L.id+'" aria-expanded="'+(ui.mark===L.id)+'">'+esc(L.deal==='rent'?T.markRented:T.markSold)+'</button>';}
  h+='<button class="nlj-btn nlj-btn--quiet nlj-btn--bad" type="button" data-act="L-rm" data-id="'+L.id+'" aria-expanded="'+(ui.rm===L.id)+'">'+esc(T.removeLive)+'</button>';
 }else if(L.state==='sold'||L.state==='rented'){
  h+='<button class="nlj-btn nlj-btn--secondary nlj-btn--sm" type="button" data-act="L-active" data-id="'+L.id+'">'+esc(T.backOnMarket)+'</button><button class="nlj-btn nlj-btn--quiet nlj-btn--bad" type="button" data-act="L-rm" data-id="'+L.id+'" aria-expanded="'+(ui.rm===L.id)+'">'+esc(T.removeLive)+'</button>';
 }else if(L.state==='removed'){
  h+='<button class="nlj-btn nlj-btn--secondary nlj-btn--sm" type="button" data-act="L-republish" data-id="'+L.id+'">'+esc(T.republish)+'</button>';
 }
 h+='</div>';
 if(ui.price===L.id){h+='<form class="nlj-inline" data-price="'+L.id+'" novalidate><div class="nlj-field"><label class="nlj-label" for="j-np-'+L.id+'">'+esc(T.newPrice)+'</label><input class="nlj-input is-ltr" id="j-np-'+L.id+'" inputmode="numeric" value="'+(L.price_raw||'')+'"></div><button class="nlj-btn nlj-btn--primary nlj-btn--sm" type="submit">'+esc(T.savePrice)+'</button><button class="nlj-btn nlj-btn--quiet" type="button" data-act="ui-close">'+esc(T.cancel)+'</button></form>';}
 if(ui.mark===L.id){h+='<div class="nlj-confirm" role="group"><b>'+esc(L.deal==='rent'?T.rentedAskH:T.soldAskH)+'</b><p class="nlj-small" style="color:#14212b">'+esc(T.markAskTxt)+'</p><div class="nlj-item-acts"><button class="nlj-btn nlj-btn--danger nlj-btn--sm" type="button" data-act="L-mark-yes" data-id="'+L.id+'" data-st="'+(L.deal==='rent'?'rented':'sold')+'">'+esc(T.yesMark)+'</button><button class="nlj-btn nlj-btn--secondary nlj-btn--sm" type="button" data-act="ui-close">'+esc(T.cancel)+'</button></div></div>';}
 if(ui.rm===L.id){h+='<div class="nlj-confirm" role="group"><b>'+esc(T.rmH)+'</b><p class="nlj-small" style="color:#14212b">'+esc(T.rmTxt)+'</p><div class="nlj-item-acts"><button class="nlj-btn nlj-btn--danger nlj-btn--sm" type="button" data-act="L-rm-yes" data-id="'+L.id+'">'+esc(T.rmYes)+'</button><button class="nlj-btn nlj-btn--secondary nlj-btn--sm" type="button" data-act="ui-close">'+esc(T.cancel)+'</button></div></div>';}
 if(ui.err&&ui.err.id===L.id){h+=fieldErr('j-L'+L.id,ui.err.msg);}
 return h+'</article>';
}
function draftItem(d){
 var stepN={details:2,photos:3,preview:4}[d.step]||2,ui=S.mineUi||{};
 var h='<article class="nlj-item" id="D'+d.id+'"><div class="nlj-item-top"><div class="nlj-thumb">'+(d.photos&&d.photos[0]?'<img alt="" src="'+esc(d.photos[0].thumb)+'">':ICO.house)+'</div><div style="display:flex;flex-direction:column;gap:6px;min-width:0;flex:1"><div style="display:flex;flex-wrap:wrap;gap:6px"><span class="nlj-chip">'+esc(T.chipDraft)+'</span>'+(d.summary.deal?'<span class="nlj-chip">'+esc(d.summary.deal==='rent'?T.rent:T.sale)+'</span>':'')+'</div><h3 style="font-size:19px">'+esc(d.summary.title)+'</h3><p class="nlj-small">'+esc(T.draftMeta(stepN,fday(d.saved_at)))+'</p></div></div>';
 h+='<div class="nlj-item-acts"><button class="nlj-btn nlj-btn--primary nlj-btn--sm" type="button" data-act="d-open" data-id="'+d.id+'" data-step="'+esc(d.step)+'">'+esc(T.continueDraft)+'</button><button class="nlj-btn nlj-btn--quiet nlj-btn--bad" type="button" data-act="d-del" data-id="'+d.id+'" aria-expanded="'+(ui.del===d.id)+'">'+esc(T.draftDelete)+'</button></div>';
 if(ui.del===d.id){h+='<div class="nlj-confirm" role="group"><b>'+esc(T.delAskH)+'</b><p class="nlj-small" style="color:#14212b">'+esc(T.delAskTxt)+'</p><div class="nlj-item-acts"><button class="nlj-btn nlj-btn--danger nlj-btn--sm" type="button" data-act="d-del-yes" data-id="'+d.id+'">'+esc(T.delYes)+'</button><button class="nlj-btn nlj-btn--secondary nlj-btn--sm" type="button" data-act="ui-close">'+esc(T.cancel)+'</button></div></div>';}
 if(ui.delRun===d.id){h+=statusBox('',ICO.spin,T.delRunH,T.delRunTxt,'','status');}
 if(ui.err&&ui.err.id===d.id){h+=fieldErr('j-D'+d.id,ui.err.msg);}
 return h+'</article>';
}
function loadMine(){
 call('GET','/listings').then(function(x){
  S.mine=x.ok?x.j:{fail:true};
  if(x.ok){S.drafts=x.j.drafts||[];}
  if(S.screen==='mine'){renderMine();}
 });
}
function mineAct(path,body,id,after){
 var msg=$('nlj-mine-msg');
 call('POST',path,body).then(function(x){
  if(x.ok){S.mineUi={};if(after){after(x);}else{S.mine=null;renderMine();}}
  else{S.mineUi=Object.assign({},S.mineUi,{err:{id:id,msg:x.j.message||(x.net?T.netErr:T.actionFail)}});renderMine();}
 });
}

/* ---------------- 8. promotion: switched off ---------------- */
function renderPromote(){
 var live=S.mine&&S.mine.listings?S.mine.listings.filter(function(L){return L.state==='active';}):[],h='';
 h+='<div class="nlj-head" data-focus style="max-width:760px"><p class="nlj-kick">'+esc(T.myListings)+'</p><h2 class="nlj-h1">'+esc(T.promoH)+'</h2><p class="nlj-lead">'+esc(T.promoLead)+'</p></div>';
 h+='<div style="max-width:760px">'+statusBox('warn',ICO.info.replace('width="18" height="18"','class="nlj-st-ico"'),T.promoOffH,T.promoOffTxt,'','status')+'</div>';
 h+='<div class="nlj-card" style="max-width:760px;opacity:.78" aria-disabled="true"><fieldset disabled style="border:0;margin:0;padding:0;display:flex;flex-direction:column;gap:16px"><legend class="nlj-label" style="padding:0;margin-bottom:8px">'+esc(T.promoPick)+'</legend>';
 h+=live.length?live.map(function(L,i){return '<label class="nlj-check"><input type="radio" name="pl"'+(i===0?' checked':'')+'><span>'+esc(L.title)+'<small>'+esc(T.chipLive)+'</small></span></label>';}).join(''):'<p class="nlj-small">'+esc(T.promoNone)+'</p>';
 h+='<div class="nlj-field"><span class="nlj-label">'+esc(T.promoWhere)+'</span><div class="nlj-seg"><button class="nlj-pill" type="button" aria-pressed="true">'+esc(T.promoList)+'</button><button class="nlj-pill" type="button" aria-pressed="false">'+esc(T.promoCity)+'</button></div></div>';
 h+='<div class="nlj-field"><span class="nlj-label">'+esc(T.promoPrice)+'</span><p class="nlj-hint">'+esc(T.promoPriceTxt)+'</p></div><button class="nlj-btn nlj-btn--primary" type="button" disabled>'+esc(T.promoBtn)+'</button></fieldset></div>';
 h+='<button class="nlj-btn nlj-btn--quiet" type="button" data-act="go-mine" style="align-self:flex-start">'+esc(T.backMine)+'</button>';
 render.frame(h);
}

/* ---------------- opening a draft ---------------- */
function openDraft(id,screen,noUrl){
 render.frame('<div class="nlj-loading" role="status">…</div>');
 call('GET','/draft/'+id).then(function(x){
  if(!x.ok){S.screen='';startFresh(true);return;}
  D=newDraft();loadServer(x.j);D.id=x.j.id;
  (x.j.recovered||[]).forEach(function(p){P.push({k:++tileSeq,ref:p.ref,att:0,thumb:p.thumb,full:p.full,w:p.w,h:p.h,s:'ok'});});
  if((x.j.recovered||[]).length){touch();}
  applyQueue();if(dirty()&&S.save!=='conflict'){schedule(400);}
  S.preview=null;S.pub=null;
  if(S.save!=='conflict'){setSave(dirty()?'device':'account');}
  go(screen||x.j.step||'details',{noUrl:!!noUrl,replace:!noUrl});
 });
}
/* this user's unsent changes on this device: applied when they start from the server's revision, else shown as a conflict */
function applyQueue(){
 var q=store.get(qkey(D.id))||MEM[qkey(D.id)];
 if(!q||!q.fields){return;}
 var mine=Object.assign({},D.fields,q.fields);mine.phone=D.fields.phone;
 if(+q.rev===+D.rev){D.fields=mine;if(q.photos){var have={};P.forEach(function(t){have[t.ref||('a'+t.att)]=t;});var np=[];q.photos.forEach(function(p){var t=have[p.ref||('a'+p.att)];if(t){np.push(t);delete have[p.ref||('a'+p.att)];}});Object.keys(have).forEach(function(k){np.push(have[k]);});P=np;}D.step=q.step||D.step;D.seq++;}
 else if(+q.rev<+D.rev){S.conflict={server:{rev:D.rev,saved_at:D.saved_at,fields:clone(D.fields),photos:P.map(function(t){return {ref:t.ref,att:t.att,thumb:t.thumb,full:t.full};})},mine:{fields:mine,photos:P.slice()}};S.save='conflict';}
}
function startFresh(noUrl){
 D=newDraft();P=[];S.preview=null;S.pub=null;
 var q=store.get(qkey(''))||MEM[qkey('')];   // typed offline before the draft existed on the server
 if(q&&q.fields){D.fields=Object.assign(emptyFields(),q.fields,{phone:D.fields.phone});D.ck=q.ck||'';D.seq++;}
 S.save=dirty()?'device':'';
 go('details',{noUrl:!!noUrl,replace:true});
 if(dirty()){schedule(800);}
}

/* ---------------- events (one delegated handler) ---------------- */
root.addEventListener('input',function(e){
 var el=e.target,k=el&&el.getAttribute('data-f');if(!k){return;}
 D.fields[k]=el.type==='checkbox'?el.checked:el.value;
 if(k==='desc'){var n=$('j-desc-n');if(n){n.textContent=String(el.value.length).replace(/\B(?=(\d{3})+(?!\d))/g,',')+' / 1,500';}}
 if(S.showErr&&S.errors[k]){delete S.errors[k];el.classList.remove('is-bad');el.removeAttribute('aria-invalid');var er=$((FID[k]||'')+'-err');if(er){er.parentNode.removeChild(er);}}
 touch();
});
root.addEventListener('change',function(e){
 var el=e.target;
 if(el&&el.id==='j-files'){addFiles(el.files);el.value='';return;}
 var k=el&&el.getAttribute('data-f');if(!k){return;}
 D.fields[k]=el.type==='checkbox'?el.checked:el.value;
 if(k==='phone_ok'){var lab=root.querySelector('label[for="j-phone"]');if(lab){lab.innerHTML=esc(T.phone)+(D.fields.phone_ok?'':' <span class="nlj-opt">'+esc(T.phoneOpt)+'</span>');}}
 touch();
});
root.addEventListener('submit',function(e){
 var f=e.target;e.preventDefault();
 if(f.id==='nlj-signup'){authSubmit('signup');}
 else if(f.id==='nlj-login'){authSubmit('login');}
 else if(f.id==='nlj-recover'){authSubmit('recover');}
 else if(f.id==='nlj-details'){detailsNext();}
 else if(f.getAttribute('data-price')){var id=+f.getAttribute('data-price'),val=$('j-np-'+id).value;mineAct('/update',{id:id,price:val},id);}
});
root.addEventListener('dragover',function(e){var d=e.target.closest&&e.target.closest('#j-drop');if(d){e.preventDefault();d.classList.add('is-over');}});
root.addEventListener('dragleave',function(e){var d=e.target.closest&&e.target.closest('#j-drop');if(d){d.classList.remove('is-over');}});
root.addEventListener('drop',function(e){var d=e.target.closest&&e.target.closest('#j-drop');if(d){e.preventDefault();d.classList.remove('is-over');addFiles(e.dataTransfer&&e.dataTransfer.files);}});
root.addEventListener('click',function(e){
 var b=e.target.closest&&e.target.closest('[data-act],[data-deal]');if(!b||!root.contains(b)){return;}
 var a=b.getAttribute('data-act'),k=b.getAttribute('data-k'),id=+(b.getAttribute('data-id')||0);
 if(b.hasAttribute('data-deal')){D.fields.deal=b.getAttribute('data-deal');root.querySelectorAll('[data-deal]').forEach(function(x){x.setAttribute('aria-pressed',String(x===b));});var pl=root.querySelector('label[for="j-price"]');if(pl){pl.textContent=D.fields.deal==='rent'?T.priceRent:T.priceSale;}if(S.errors.deal){delete S.errors.deal;var er=$('j-deal-err');if(er){er.parentNode.removeChild(er);}}touch();return;}
 switch(a){
  case 'tab-signup':authKeep();S.auth='signup';S.authErr={};S.screen='auth';renderAuth();break;
  case 'tab-login':authKeep();S.auth='login';S.authErr={};S.screen='auth';renderAuth();var m2=$('j-mail2');if(m2&&S.authMail){$('j-pw2').focus();}break;
  case 'tab-recover':authKeep();S.auth='recover';S.authErr={};S.recSent=false;renderAuth();break;
  case 'exists-login':authKeep();S.auth='login';S.authErr={};renderAuth();var p2=$('j-pw2');if(p2){p2.focus();}break;
  case 'pw':var inpw=$(b.getAttribute('data-for'));if(inpw){var show=inpw.type==='password';inpw.type=show?'text':'password';b.textContent=show?T.hidePw:T.showPw;b.setAttribute('aria-pressed',String(show));}break;
  case 'go-mine':flush();S.mine=null;S.mineUi={};go('mine');break;
  case 'go-promote':go('promote');break;
  case 'mine-new':case 'home-new':flush();startFresh();break;
  case 'home-continue':var d0=S.drafts[0];if(d0){openDraft(d0.id,d0.step);}break;
  case 'del-ask':S.del='ask';renderHome();var dl=$('nlj-del');if(dl){dl.querySelector('button').focus();}break;
  case 'del-no':S.del='closed';renderHome();break;
  case 'del-run':var dd=S.drafts[0];if(!dd){break;}S.del='running';renderHome();call('POST','/draft/'+dd.id+'/delete',{}).then(function(x){if(x.ok&&x.j.trashed){S.del='closed';S.drafts.shift();if(S.drafts.length){renderHome();}else{startFresh();}}else{S.del='failed';renderHome();}});break;
  case 'save-exit':flush().then(function(){S.mine=null;go('mine');});break;
  case 'jump':e.preventDefault();var tg=$(FID[k]);if(tg){tg.focus();tg.scrollIntoView({block:'center'});}break;
  case 'add-photos':var fi=$('j-files');if(fi){fi.click();}break;
  case 'back-details':flush();go('details');break;
  case 'to-preview':
   var up=P.filter(function(t){return (t.s==='up'||t.s==='wait')&&!t.removed;}).length,fl=P.filter(function(t){return t.s==='err'&&!t.removed;}).length,okc=P.filter(function(t){return t.s==='ok'&&!t.removed;}).length;
   if(up){phMsg(T.waitUploads);break;}
   if(!okc){S.errors={photos:HE?'מוסיפים לפחות תמונה אחת.':'Add at least one photo.'};S.showErr=true;renderFlow();var sm=$('nlj-errsum');if(sm){sm.focus();}break;}
   if(fl&&!b.getAttribute('data-warned')){phMsg(T.failedLeft(fl));b.setAttribute('data-warned','1');break;}
   S.preview=null;flush().then(function(){go('preview');});break;
  case 'ph-up':case 'ph-down':var t1=tileBy(k);if(t1){moveTile(t1,a==='ph-up'?-1:1);touch();renderTiles();var nb=root.querySelector('[data-k="'+k+'"][data-act="'+a+'"]');if(nb&&!nb.disabled){nb.focus();}else{var ob=root.querySelector('[data-k="'+k+'"][data-act="'+(a==='ph-up'?'ph-down':'ph-up')+'"]');if(ob){ob.focus();}}}break;
  case 'ph-cover':var t2=tileBy(k);if(t2){P.splice(P.indexOf(t2),1);P.unshift(t2);touch();renderTiles();var cb=root.querySelector('[data-k="'+k+'"][data-act="ph-down"]');if(cb){cb.focus();}}break;
  case 'ph-rm':var t3=tileBy(k);if(t3){t3.removed=true;if(t3.xhr){try{t3.xhr.abort();}catch(x){}}if(t3.s==='ok'&&t3.ref&&!t3.att){D.discard.push(t3.ref);}if(t3.s==='ok'||t3.ref){touch();}renderTiles();var nx=root.querySelector('#j-add');if(nx){nx.focus();}}break;
  case 'ph-retry':var t4=tileBy(k);if(t4&&t4.file){t4.s='wait';t4.err='';renderTiles();pump();}break;
  case 'back-edit':S.pub=null;go('details');break;
  case 'fix':var fk=k;if(fk==='photos'){go('photos');}else{S.errors=S.preview&&S.preview.errors||{};S.showErr=true;go('details');var ft=$(FID[fk]);if(ft){ft.focus();}}break;
  case 'publish':publish();break;
  case 'pub-again':if(S.pub){S.pub.s='sending';redrawPv();sendPub();}break;
  case 'copy':var u=(S.published||{}).url||'';var cp=$('j-copied');try{navigator.clipboard.writeText(u).then(function(){if(cp){cp.textContent=T.copied;}});}catch(x){if(cp){cp.textContent=u;}}break;
  case 'retry':clearTimeout(retryTimer);if(S.save==='expired'){refreshNonce().then(function(ok){if(ok){S.save='';flush();}});}else{flush();}break;
  case 'cf-load':if(S.conflict){S.stash=S.conflict.mine;loadServer(S.conflict.server);S.conflict=null;S.save='loaded';render.screen();}break;
  case 'cf-keep':if(S.conflict){D.rev=S.conflict.server.rev;S.conflict=null;D.seq++;setSave('device');flush();}break;
  case 'cf-back':if(S.stash){D.fields=S.stash.fields;P=S.stash.photos;S.stash=null;S.save='device';D.seq++;render.screen();flush();}break;
  case 'gone-new':D.id=0;D.rev=0;D.ck='';D.seq++;S.save='device';flush({create:true});break;
  case 'L-edit':openDraft(+b.getAttribute('data-draft'),'details');break;
  case 'L-price':S.mineUi={price:id};renderMine();var npi=$('j-np-'+id);if(npi){npi.focus();}break;
  case 'L-mark':S.mineUi={mark:id};renderMine();break;
  case 'L-rm':S.mineUi={rm:id};renderMine();break;
  case 'ui-close':S.mineUi={};renderMine();break;
  case 'L-mark-yes':mineAct('/update',{id:id,status:b.getAttribute('data-st')},id);break;
  case 'L-active':mineAct('/update',{id:id,status:'active'},id);break;
  case 'L-rm-yes':mineAct('/update',{id:id,action:'remove'},id);break;
  case 'L-republish':mineAct('/update',{id:id,action:'republish'},id);break;
  case 'd-open':openDraft(id,b.getAttribute('data-step'));break;
  case 'd-del':S.mineUi={del:id};renderMine();break;
  case 'd-del-yes':S.mineUi={delRun:id};renderMine();call('POST','/draft/'+id+'/delete',{}).then(function(x){if(x.ok&&x.j.trashed){S.mine=null;S.mineUi={};renderMine();}else{S.mineUi={err:{id:id,msg:x.j.message||T.delFail}};renderMine();}});break;
  case 'd-restore':mineAct('/draft/'+id+'/restore',{},id,function(){S.mine=null;renderMine();var mm=$('nlj-mine-msg');if(mm){mm.textContent=T.restored;}});break;
 }
});

/* ---------------- the site's floating bar never covers a control ---------------- */
function barRect(){var b=document.getElementById('nlcta');if(!b){return null;}var cs=getComputedStyle(b);if(cs.display==='none'||cs.visibility==='hidden'){return null;}var a=b.querySelector('a')||b,r=a.getBoundingClientRect();return r.height?r:null;}
function fitBar(){var r=barRect(),room=r?Math.max(0,Math.round(window.innerHeight-r.top+16)):0;document.documentElement.style.setProperty('--nlj-bar-room',room+'px');}
function clearBar(el){
 if(!el||!root.contains(el)||!el.getBoundingClientRect){return;}
 var r=barRect();if(!r){return;}
 var e=el.getBoundingClientRect();
 if(e.bottom>r.top-8&&e.top<r.bottom+8&&e.right>r.left-8&&e.left<r.right+8){window.scrollBy(0,Math.round(e.bottom-r.top+24));}
}
document.addEventListener('focusin',function(e){fitBar();clearBar(e.target);});
window.addEventListener('resize',function(){fitBar();clearBar(document.activeElement);});
window.addEventListener('load',fitBar);
fitBar();setTimeout(fitBar,600);setTimeout(fitBar,2000);

/* ---------------- start ---------------- */
authPing();
if(!C.uid){
 S.screen='auth';var u0=readUrl();if(u0.screen==='login'){S.auth='login';}
 renderAuth();
 return;
}
var u=readUrl();
if(u.draft){openDraft(u.draft,u.screen&&['details','photos','preview'].indexOf(u.screen)>-1?u.screen:null,true);}
else if(u.screen==='mine'||u.screen==='promote'){go(u.screen,{replace:true,noFocus:true});}
else{
 render.frame('<div class="nlj-loading" role="status">…</div>');
 call('GET','/draft').then(function(x){
  S.drafts=(x.ok&&x.j.drafts)||[];
  var q=store.get(qkey(''))||MEM[qkey('')];
  if(S.drafts.length&&!(q&&q.fields)){S.screen='home';setUrl(true);renderHome();}
  else{startFresh(false);}
 });
}
})();
NLJS;
}

add_filter( 'nadlan_config_healthcheck', function ( $out ) {
	$out['owner_wizard'] = array(
		'version' => NL_OWNER_VERSION,
		'engine'  => nl_owner_engine_ok(),
		'sealed'  => nl_owner_crypto_ok(),
		'journey' => 2,
		'live'    => count( get_posts( array( 'post_type' => 'nadlan_property', 'post_status' => 'publish', 'fields' => 'ids', 'numberposts' => 500, 'meta_query' => array( array( 'key' => 'nl_owner', 'value' => '1' ) ), 'suppress_filters' => true ) ) ),
	);
	return $out;
} );
