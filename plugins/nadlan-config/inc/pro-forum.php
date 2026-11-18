<?php
/**
 * nadlan-config: the professionals' forum (version one, hidden by default). Built 12.11.2026, research in
 * docs/research/2026-11-12-pro-forum/ (existing-state.md, BUILD-NOTES.md). Design boards: Main, Thread, Compose, Card, Profile.
 *
 *  - Gate: option nadlan_forum_public ('0' default). While '0' every surface exists only for a visitor who opened any page with
 *    ?forum=on (cookie nlf_gate=1 for 30 days, ?forum=off clears it) or for a logged-in administrator. Without the gate /forum/
 *    answers a normal 404, the card window is not printed and the REST routes answer 400.
 *  - Addresses: /forum/ (home, filters ?c= ?v= and pages ?pg=) and /forum/<number>/ (one discussion).
 *  - Entry in one step: name + email, a 6-digit code by mail (filter nadlan_forum_send_code for a later SMS sender), a 90-day
 *    session cookie whose SHA-256 alone is stored. No password, no registration form.
 *  - Every write goes through nlf_guard(): gate, trap field, 3-second signed form time, a self-hosted proof-of-work human test,
 *    session, header nonce, member state, per-IP ceiling. Content writes add the Discourse-style limits and the text rules.
 *  - The site is a publisher: nothing here matches anyone with anyone; a question to a professional goes to that professional.
 *  - Owner correction 12.11.2026: the cards came from public registers. Only a professional who joined himself (a member linked
 *    by his verified email, nlf_pro_member) is shown as a participant, can be addressed, shows a phone or gets any mail.
 *  - No redirects anywhere in this module, no robots or noindex changes, no sitemap work, no indexing requests.
 * Files: inc/pro-forum.php (this: pure functions, data, guard, REST, routing, search-engine tags, mail),
 *        inc/pro-forum-render.php (HTML), inc/pro-forum-admin.php (wp-admin screen), assets/proforum/forum.css + forum.js.
 * Load: ONE line appended at the END of inc/pro-network.php (not the module list in nadlan-config.php):
 *   if ( file_exists( __DIR__ . '/pro-forum.php' ) ) { require_once __DIR__ . '/pro-forum.php'; }
 * This file loads its two siblings itself, creates its tables once per DB version and flushes the rewrite rules once per
 * rules version by itself (no manual step). No long dashes in this file.
 */
if ( ! defined( 'ABSPATH' ) ) { exit; }
if ( defined( 'NADLAN_FORUM_VERSION' ) ) { return; }
define( 'NADLAN_FORUM_VERSION', '0.1.0' );
define( 'NADLAN_FORUM_DB', '2' ); // 2: members.trade + members.trade_other (review 12.11.2026)
define( 'NADLAN_FORUM_RULES', '1' );

/* =========================================================================================================
 * 1. Pure functions (no WordPress). tests-local/pro-forum-test.php loads only this part (NLF_PURE_ONLY).
 * ======================================================================================================= */

/** key => array( Hebrew label, tint background, tint text ) */
function nlf_categories() {
	return array(
		'law'     => array( 'דיני מקרקעין', '#EBDDF0', '#4A1D5E' ),
		'build'   => array( 'שיפוץ ובנייה', '#DCE6F2', '#1D3B66' ),
		'loans'   => array( 'משכנתאות', '#DDE3FB', '#1E2F8F' ),
		'value'   => array( 'שמאות', '#DCEFE3', '#1B4D33' ),
		'design'  => array( 'עיצוב פנים', '#E7E1FA', '#43308F' ),
		'agents'  => array( 'תיווך', '#D9EEF0', '#0E4A57' ),
		'renewal' => array( 'יזמות והתחדשות עירונית', '#E3E6E8', '#22303A' ),
		'abroad'  => array( 'השקעות נדל"ן בחו"ל', '#E3E6E8', '#22303A' ),
		'general' => array( 'כללי', '#F2F4F5', '#3A4650' ),
	);
}

function nlf_cat_ok( $key ) { return is_string( $key ) && isset( nlf_categories()[ $key ] ); }

/** kind => label (Compose board) */
function nlf_kinds() {
	return array( 'question' => 'שאלה', 'seek' => 'מחפש בעל מקצוע', 'collab' => 'שיתוף פעולה', 'intro' => 'היי, אני בעל מקצוע', 'work' => 'עבודה שסיימתי' );
}

/** the labels an ordinary member may choose; a chosen "בעל מקצוע" never carries a verified mark */
function nlf_roles() {
	return array( 'buyer' => 'רוכש דירה', 'owner' => 'בעל דירה', 'investor' => 'משקיע', 'pro' => 'בעל מקצוע' );
}

function nlf_report_reasons() {
	return array( 'spam' => 'פרסום או ספאם', 'abuse' => 'פגיעה או העלבה', 'private' => 'פרטים אישיים של מישהו', 'wrong' => 'מידע מטעה', 'other' => 'סיבה אחרת' );
}

/** profession key => tint pair (the seven profession tints of the design) */
function nlf_prof_tint( $prof ) {
	$t = array(
		'contractor' => array( '#DCE6F2', '#1D3B66' ), 'lawyer' => array( '#EBDDF0', '#4A1D5E' ), 'appraiser' => array( '#DCEFE3', '#1B4D33' ),
		'mortgage' => array( '#DDE3FB', '#1E2F8F' ), 'designer' => array( '#E7E1FA', '#43308F' ), 'broker' => array( '#D9EEF0', '#0E4A57' ),
		'developer' => array( '#E3E6E8', '#22303A' ),
	);
	$map = array(
		'kablan' => 'contractor', 'renovation' => 'contractor', 'mefakeach' => 'contractor', 'bedek_bait' => 'contractor', 'engineer' => 'contractor',
		'electrician' => 'contractor', 'plumber' => 'contractor', 'hvac' => 'contractor', 'waterproofing' => 'contractor', 'solar' => 'contractor',
		'pools' => 'contractor', 'security' => 'contractor', 'flooring' => 'contractor', 'windows' => 'contractor',
		'lawyer' => 'lawyer', 'accountant' => 'lawyer',
		'shamai' => 'appraiser', 'surveyor' => 'appraiser', 'actuary' => 'appraiser',
		'mashkanta' => 'mortgage', 'insurance' => 'mortgage',
		'interior_designer' => 'designer', 'architect' => 'designer', 'kitchens' => 'designer', 'furniture' => 'designer', 'lighting' => 'designer', 'gardens' => 'designer',
		'metavech' => 'broker', 'property_manager' => 'broker',
	);
	$g = isset( $map[ (string) $prof ] ) ? $map[ (string) $prof ] : 'developer';
	return $t[ $g ];
}

/** Plain text in: control characters and bidi overrides out, line breaks kept (at most one empty line), trimmed. */
function nlf_text_norm( $s, $single_line = false ) {
	$s = (string) $s;
	if ( '' === $s || ! preg_match( '//u', $s ) ) { return ''; } // invalid UTF-8 = nothing
	$s = str_replace( array( "\r\n", "\r" ), "\n", $s );
	$s = preg_replace( '/[\x{202A}-\x{202E}\x{2066}-\x{2069}\x{FEFF}]/u', '', $s );
	$s = preg_replace( '/[\x00-\x09\x0B-\x1F\x7F]/u', ' ', $s );
	if ( $single_line ) { $s = str_replace( "\n", ' ', $s ); }
	$s = preg_replace( '/[ \x{00A0}]+\n/u', "\n", $s );
	$s = preg_replace( "/\n{3,}/", "\n\n", $s );
	$s = preg_replace( '/[ \x{00A0}]{2,}/u', ' ', $s );
	return trim( (string) $s );
}

/** looks like a link or an email address */
function nlf_has_link( $s ) {
	return (bool) preg_match( '~(https?://|www\.|wa\.me|t\.me/|bit\.ly|[\p{L}\p{N}._%+\-]+@[\p{L}\p{N}\-]+\.[\p{L}]{2,}|\b[a-z0-9\-]{2,}\.(com|co\.il|org\.il|net|org|il|io|me|ly|info|biz|app|site|xyz|online|shop)\b)~iu', (string) $s );
}

/** looks like a phone number: 9 or more digits with only spaces, dashes, dots, brackets or a plus between them */
function nlf_has_phone( $s ) {
	return (bool) preg_match( '/(?:\+?\d[\s\-.()\x{00A0}]{0,2}){9,}/u', (string) $s );
}

function nlf_len( $s ) { return function_exists( 'mb_strlen' ) ? mb_strlen( (string) $s, 'UTF-8' ) : strlen( utf8_decode( (string) $s ) ); }

/** '' when the title is fine, else the Hebrew message */
function nlf_title_error( $t ) {
	$n = nlf_len( $t );
	if ( $n < 8 ) { return 'הכותרת קצרה מדי. כתבו לפחות 8 תווים.'; }
	if ( $n > 140 ) { return 'הכותרת ארוכה מדי. עד 140 תווים.'; }
	return '';
}

function nlf_body_error( $b, $required ) {
	$n = nlf_len( $b );
	if ( $required && $n < 2 ) { return 'כתבו כמה מילים לפני השליחה.'; }
	if ( $n > 4000 ) { return 'ההודעה ארוכה מדי. עד 4,000 תווים.'; }
	return '';
}

/** links and phones are refused (never silently stripped) for a member with fewer than 2 approved posts */
function nlf_text_rule_error( $text, $approved ) {
	if ( (int) $approved >= 2 ) { return ''; }
	if ( nlf_has_link( $text ) ) { return 'בהודעות הראשונות אי אפשר לכתוב קישור או כתובת מייל. כתבו בלי, ואחרי שתי הודעות שאושרו זה ייפתח.'; }
	if ( nlf_has_phone( $text ) ) { return 'בהודעות הראשונות אי אפשר לכתוב מספר טלפון. כתבו בלי, ואחרי שתי הודעות שאושרו זה ייפתח.'; }
	return '';
}

/** the duplicate key of a text: case, spaces and punctuation do not make a text new */
function nlf_dup_key( $s ) {
	$s = function_exists( 'mb_strtolower' ) ? mb_strtolower( (string) $s, 'UTF-8' ) : strtolower( (string) $s );
	$s = preg_replace( '/[^\p{L}\p{N}]+/u', '', $s );
	return hash( 'sha256', (string) $s );
}

/** identical text inside the window: $recent = list of array( key, unix time ) of this member's own posts */
function nlf_dup_hit( array $recent, $key, $now, $window = 300 ) {
	foreach ( $recent as $r ) {
		if ( isset( $r[0], $r[1] ) && hash_equals( (string) $r[0], (string) $key ) && (int) $now - (int) $r[1] < $window ) { return true; }
	}
	return false;
}

/**
 * The posting limits (numbers from Discourse's published defaults). $s keys: is_topic, approved, age (seconds since the member
 * was created), topics_first_day, replies_first_day, since_last (seconds since the member's last post, null for none), ip_hour.
 * '' = allowed, else the Hebrew message.
 */
function nlf_limits_error( array $s ) {
	$is_topic = ! empty( $s['is_topic'] );
	if ( (int) ( $s['ip_hour'] ?? 0 ) >= 20 ) { return 'הגעתם למספר ההודעות המרבי לשעה. נסו שוב מאוחר יותר.'; }
	if ( (int) ( $s['age'] ?? 0 ) < 86400 ) {
		if ( $is_topic && (int) ( $s['topics_first_day'] ?? 0 ) >= 3 ) { return 'ביום הראשון אפשר לפתוח עד 3 דיונים. נסו שוב מחר.'; }
		if ( ! $is_topic && (int) ( $s['replies_first_day'] ?? 0 ) >= 10 ) { return 'ביום הראשון אפשר לכתוב עד 10 תשובות. נסו שוב מחר.'; }
	}
	$gap = (int) ( $s['approved'] ?? 0 ) < 2 ? 30 : 15;
	if ( isset( $s['since_last'] ) && null !== $s['since_last'] && (int) $s['since_last'] < $gap ) {
		return 'רגע, אפשר לכתוב שוב בעוד ' . max( 1, $gap - (int) $s['since_last'] ) . ' שניות.';
	}
	return '';
}

/**
 * 1.72.671 (owner 12.11.2026: "as little management from me as possible"): a member's FIRST message goes live by itself when
 * it is clean; only a suspicious one waits for the owner. Links, e-mails and phone numbers are already refused before this.
 * '' = clean, else the reason (kept for the admin screen). Pure.
 */
function nlf_first_post_flag( $text ) {
	$t = (string) $text;
	$low = strtolower( $t );
	foreach ( array( 'casino', 'viagra', 'crypto', 'bitcoin', 'forex', 'loan', 'telegram', 'קזינו', 'הימורים', 'הלוואה חוץ בנקאית', 'טלגרם', 'בינארי', 'קריפטו', 'סקס', 'ויאגרה' ) as $w ) {
		if ( false !== strpos( $low, $w ) ) { return 'word'; }
	}
	if ( preg_match( '/(.)\1{5,}/u', $t ) ) { return 'repeat'; }
	$latin = preg_match_all( '/[A-Za-z]/', $t );
	$heb   = preg_match_all( '/[\x{0590}-\x{05FF}]/u', $t );
	if ( $latin > 20 && $latin > 2 * max( 1, $heb ) ) { return 'latin'; }
	return '';
}

/** live or pending for a new message: a trusted member always live; a first message live when clean and the switch is on */
function nlf_first_status( $approved_posts, $text, $auto_on ) {
	if ( (int) $approved_posts >= 1 ) { return 'live'; }
	return ( $auto_on && '' === nlf_first_post_flag( $text ) ) ? 'live' : 'pending';
}

/** leading zero bits of a binary string */
function nlf_zero_bits( $bin ) {
	$n = 0;
	$len = strlen( (string) $bin );
	for ( $i = 0; $i < $len; $i++ ) {
		$b = ord( $bin[ $i ] );
		if ( 0 === $b ) { $n += 8; continue; }
		for ( $k = 7; $k >= 0; $k-- ) { if ( $b & ( 1 << $k ) ) { return $n; } $n++; }
	}
	return $n;
}

/** proof of work: SHA-256(salt + nonce) starts with $bits zero bits; the nonce is a decimal string */
function nlf_pow_ok( $salt, $nonce, $bits ) {
	if ( ! preg_match( '/^[a-f0-9]{8,64}$/', (string) $salt ) || ! preg_match( '/^[0-9]{1,12}$/', (string) $nonce ) ) { return false; }
	return nlf_zero_bits( hash( 'sha256', $salt . $nonce, true ) ) >= (int) $bits;
}

function nlf_sig( $payload, $key ) { return substr( hash_hmac( 'sha256', (string) $payload, (string) $key ), 0, 32 ); }

/** a signed one-click link token: action.id.expiry.sig (expiry 0 = never) */
function nlf_link_token( $action, $id, $exp, $key ) {
	$p = preg_replace( '/[^a-z]/', '', (string) $action ) . '.' . preg_replace( '/[^a-z0-9_]/', '', (string) $id ) . '.' . (int) $exp;
	return $p . '.' . nlf_sig( 'lnk|' . $p, $key );
}

/** array( action, id ) when the token is genuine and in time, else null */
function nlf_link_read( $token, $now, $key ) {
	$parts = explode( '.', (string) $token );
	if ( 4 !== count( $parts ) ) { return null; }
	list( $a, $id, $exp, $sig ) = $parts;
	if ( ! preg_match( '/^[a-z]{1,12}$/', $a ) || ! preg_match( '/^[a-z0-9_]{1,40}$/', $id ) || ! preg_match( '/^[0-9]{1,12}$/', $exp ) ) { return null; }
	if ( ! hash_equals( nlf_sig( 'lnk|' . $a . '.' . $id . '.' . $exp, $key ), (string) $sig ) ) { return null; }
	if ( (int) $exp > 0 && (int) $now > (int) $exp ) { return null; }
	return array( $a, $id );
}

/** a proof-of-work challenge: salt.bits.time.sig */
function nlf_challenge_make( $key, $now, $bits, $salt ) {
	$p = preg_replace( '/[^a-f0-9]/', '', (string) $salt ) . '.' . (int) $bits . '.' . (int) $now;
	return $p . '.' . nlf_sig( 'pow|' . $p, $key );
}

/** the salt when the challenge is genuine, fresh and solved by $nonce; '' otherwise (single use is checked by the caller) */
function nlf_challenge_check( $token, $nonce, $key, $now, $ttl = 600 ) {
	$parts = explode( '.', (string) $token );
	if ( 4 !== count( $parts ) ) { return ''; }
	list( $salt, $bits, $t, $sig ) = $parts;
	if ( ! preg_match( '/^[a-f0-9]{8,64}$/', $salt ) || ! preg_match( '/^[0-9]{1,2}$/', $bits ) || ! preg_match( '/^[0-9]{1,12}$/', $t ) ) { return ''; }
	if ( ! hash_equals( nlf_sig( 'pow|' . $salt . '.' . $bits . '.' . $t, $key ), (string) $sig ) ) { return ''; }
	if ( (int) $now - (int) $t > $ttl || (int) $t > (int) $now + 60 ) { return ''; }
	return nlf_pow_ok( $salt, $nonce, (int) $bits ) ? $salt : '';
}

/** the signed time a form was shown */
function nlf_form_ts_make( $key, $now ) { return (int) $now . '.' . nlf_sig( 'ts|' . (int) $now, $key ); }

/** '' when the form was shown at least $min seconds ago and less than 12 hours ago */
function nlf_form_ts_error( $token, $key, $now, $min = 3 ) {
	$parts = explode( '.', (string) $token );
	if ( 2 !== count( $parts ) || ! preg_match( '/^[0-9]{1,12}$/', $parts[0] ) || ! hash_equals( nlf_sig( 'ts|' . $parts[0], $key ), (string) $parts[1] ) ) {
		return 'הטופס פג תוקף. רעננו את הדף ונסו שוב.';
	}
	$age = (int) $now - (int) $parts[0];
	if ( $age < $min ) { return 'רגע, עוד שנייה ושלחו שוב.'; }
	if ( $age > 12 * 3600 ) { return 'הטופס פג תוקף. רעננו את הדף ונסו שוב.'; }
	return '';
}

function nlf_contact_norm( $email ) { return strtolower( trim( (string) $email ) ); }

function nlf_contact_hash( $email, $key ) { return hash_hmac( 'sha256', 'c|' . nlf_contact_norm( $email ), (string) $key ); }

function nlf_code_hash( $code, $contact_hash, $key ) { return hash_hmac( 'sha256', 'code|' . $contact_hash . '|' . (string) $code, (string) $key ); }

/** $row: array( code_hash, tries, expires (unix) ) or null. Returns ok | none | expired | tries | wrong. */
function nlf_code_verdict( $row, $code, $contact_hash, $now, $key, $max_tries = 5 ) {
	if ( ! is_array( $row ) || empty( $row['code_hash'] ) ) { return 'none'; }
	if ( (int) $now > (int) $row['expires'] ) { return 'expired'; }
	if ( (int) $row['tries'] >= $max_tries ) { return 'tries'; }
	if ( ! preg_match( '/^[0-9]{6}$/', (string) $code ) ) { return 'wrong'; }
	return hash_equals( (string) $row['code_hash'], nlf_code_hash( $code, $contact_hash, $key ) ) ? 'ok' : 'wrong';
}

/** plain text to safe HTML: everything escaped, line breaks kept, nothing auto-linked */
function nlf_body_html( $s ) { return nl2br( htmlspecialchars( (string) $s, ENT_QUOTES | ENT_SUBSTITUTE, 'UTF-8' ), false ); }

function nlf_excerpt( $s, $n ) {
	$s = trim( preg_replace( '/\s+/u', ' ', (string) $s ) );
	return nlf_len( $s ) > $n ? rtrim( mb_substr( $s, 0, $n, 'UTF-8' ) ) . '…' : $s;
}

/** two letters for an avatar */
function nlf_initials( $name ) {
	$w = preg_split( '/\s+/u', trim( preg_replace( '/[^\p{L}\s]/u', ' ', (string) $name ) ) );
	$w = array_values( array_filter( (array) $w ) );
	if ( ! $w ) { return '?'; }
	$a = mb_substr( $w[0], 0, 1, 'UTF-8' );
	return isset( $w[1] ) ? $a . mb_substr( $w[1], 0, 1, 'UTF-8' ) : $a;
}

/** Hebrew relative time for up to a week; '' beyond (the caller prints the date) */
function nlf_ago( $ts, $now ) {
	$d = (int) $now - (int) $ts;
	if ( $d < 60 ) { return 'עכשיו'; }
	if ( $d < 3600 ) { $m = (int) floor( $d / 60 ); return 1 === $m ? 'לפני דקה' : 'לפני ' . $m . ' דקות'; }
	if ( $d < 86400 ) { $h = (int) floor( $d / 3600 ); return 1 === $h ? 'לפני שעה' : ( 2 === $h ? 'לפני שעתיים' : 'לפני ' . $h . ' שעות' ); }
	if ( $d < 172800 ) { return 'אתמול'; }
	if ( $d < 604800 ) { $x = (int) floor( $d / 86400 ); return 2 === $x ? 'לפני יומיים' : 'לפני ' . $x . ' ימים'; }
	return '';
}

/** "N תשובות" with the Hebrew singular; '' for zero (an unknown or empty count is omitted, never "0") */
function nlf_count_words( $n, $one, $many ) {
	$n = (int) $n;
	if ( $n < 1 ) { return ''; }
	return 1 === $n ? $one : number_format( $n ) . ' ' . $many;
}

/** JSON for an inline <script>: < and > as < / >, so the output never holds "</" (review 12.11.2026) */
function nlf_json_script( $data ) {
	$f = JSON_HEX_TAG | JSON_HEX_AMP | JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES;
	$j = function_exists( 'wp_json_encode' ) ? wp_json_encode( $data, $f ) : json_encode( $data, $f );
	return false === $j ? 'null' : (string) $j;
}

/**
 * The status to give back when the owner shows his card again; '' = leave it as it is (review 12.11.2026).
 * Only a card the owner himself hid ($owner_hid) and that is private now goes back, and only to the status it had before.
 * A card the site's staff made private (no stored previous status) is never published from the forum.
 */
function nlf_restore_status( $current, $prev, $owner_hid ) {
	if ( 'private' !== (string) $current || ! $owner_hid ) { return ''; }
	return in_array( (string) $prev, array( 'publish', 'pending', 'draft' ), true ) ? (string) $prev : '';
}

/** the rewrite step for this request: none (rules of this version done), skip (the /forum/ address belongs to a page), flush */
function nlf_rules_step( $stored, $want, $slug_taken ) {
	if ( (string) $stored === (string) $want ) { return 'none'; }
	return $slug_taken ? 'skip' : 'flush';
}

/** a forum view takes over the request only for a genuine one-click link, or for a broken one while the gate is open */
function nlf_act_takeover( $link_ok, $gate_open ) { return (bool) $link_ok || (bool) $gate_open; }

if ( defined( 'NLF_PURE_ONLY' ) ) { return; }

/* =========================================================================================================
 * 2. Gate, keys, cookies
 * ======================================================================================================= */

function nlf_public() { return '1' === (string) get_option( 'nadlan_forum_public', '0' ); }

/** this request may see the forum */
function nlf_gate_open() {
	if ( nlf_public() ) { return true; }
	if ( function_exists( 'current_user_can' ) && current_user_can( 'manage_options' ) ) { return true; }
	$q = isset( $_GET['forum'] ) ? sanitize_key( wp_unslash( $_GET['forum'] ) ) : ''; // phpcs:ignore -- a view switch
	if ( 'off' === $q ) { return false; }
	if ( 'on' === $q ) { return true; }
	return isset( $_COOKIE['nlf_gate'] ) && '1' === (string) $_COOKIE['nlf_gate'];
}

function nlf_key() {
	static $k = null;
	if ( null === $k ) { $k = hash( 'sha256', 'nlf|' . wp_salt( 'auth' ) . '|' . wp_salt( 'nonce' ) ); }
	return $k;
}

function nlf_ip_hash() {
	$ip = isset( $_SERVER['REMOTE_ADDR'] ) ? (string) $_SERVER['REMOTE_ADDR'] : '0'; // phpcs:ignore -- hashed, never stored raw
	return hash( 'sha256', nlf_key() . '|ip|' . $ip );
}

function nlf_cookie( $name, $value, $expires, $httponly = true ) {
	if ( headers_sent() ) { return; }
	// Secure also when TLS ends at the host's proxy (is_ssl() false there) but the site itself is https
	$secure = is_ssl() || 'https' === wp_parse_url( home_url( '/' ), PHP_URL_SCHEME );
	setcookie( $name, $value, array( 'expires' => (int) $expires, 'path' => '/', 'domain' => defined( 'COOKIE_DOMAIN' ) && COOKIE_DOMAIN ? COOKIE_DOMAIN : '',
		'secure' => $secure, 'httponly' => $httponly, 'samesite' => 'Lax' ) );
	if ( 0 === (int) $expires || $expires > time() ) { $_COOKIE[ $name ] = $value; } else { unset( $_COOKIE[ $name ] ); } // 0 = a browser-session cookie
}

/**
 * A page or answer that depends on the gate or the session is never stored by a cache: no-cache headers (any proxy or CDN),
 * DONOTCACHEPAGE and the LiteSpeed no-cache action. The action is fired again on 'wp' (below) in case LiteSpeed Cache had not
 * hooked it yet when the decision was made at init priority 1. A raw X-LiteSpeed-Cache-Control header alone is not enough:
 * LiteSpeed Cache writes its own header at the end of the request.
 */
function nlf_nocache() {
	$GLOBALS['nlf_nocache'] = true;
	if ( ! headers_sent() ) {
		nocache_headers();
		header( 'X-LiteSpeed-Cache-Control: no-cache' );
	}
	do_action( 'litespeed_control_set_nocache', 'nadlan forum' );
	if ( ! defined( 'DONOTCACHEPAGE' ) ) { define( 'DONOTCACHEPAGE', true ); }
}
add_action( 'wp', function () {
	if ( ! empty( $GLOBALS['nlf_nocache'] ) ) { do_action( 'litespeed_control_set_nocache', 'nadlan forum' ); }
}, 0 );

/* ?forum=on opens the gate for 30 days on this browser, ?forum=off closes it. This is the ONLY place the gate cookie is set.
   Any request that carries ?forum=, the gate cookie or a forum session is never cached, whatever page it is (review 12.11.2026). */
add_action( 'init', function () {
	if ( is_admin() ) { return; }
	$q = isset( $_GET['forum'] ) ? sanitize_key( wp_unslash( $_GET['forum'] ) ) : null; // phpcs:ignore -- a view switch
	if ( 'on' === $q ) { nlf_cookie( 'nlf_gate', '1', time() + 30 * DAY_IN_SECONDS, true ); }
	if ( 'off' === $q ) { nlf_cookie( 'nlf_gate', '', time() - 3600, true ); }
	if ( null !== $q || isset( $_COOKIE['nlf_gate'] ) || isset( $_COOKIE['nlf_s'] ) ) { nlf_nocache(); }
}, 1 );

/* a professional's page with the gate open (decided before any output, so the headers go out) */
add_action( 'template_redirect', function () {
	if ( is_singular( 'nadlan_professional' ) && nlf_gate_open() ) { nlf_nocache(); }
}, 0 );

/* LiteSpeed: the gate cookie and the session are vary cookies. litespeed_vary_cookies feeds the .htaccess vary rule (written
   when LiteSpeed Cache saves its settings); litespeed_vary_curr_cookies adds X-LiteSpeed-Vary to the two kinds of page where
   the forum prints, so a public cached copy is never served to a gated browser and a gated copy is never stored (no-op when
   LiteSpeed Cache is absent). */
add_filter( 'litespeed_vary_cookies', function ( $list ) {
	$list = (array) $list;
	$list[] = 'nlf_gate';
	$list[] = 'nlf_s';
	return array_values( array_unique( $list ) );
} );
add_filter( 'litespeed_vary_curr_cookies', function ( $list ) {
	$list = (array) $list;
	if ( did_action( 'wp' ) && ( '' !== (string) get_query_var( 'nlf_view' ) || is_singular( 'nadlan_professional' ) ) ) {
		$list[] = 'nlf_gate';
		$list[] = 'nlf_s';
	}
	return array_values( array_unique( $list ) );
} );

/** a fixed-window limit per hashed IP (or per $who): true while under $max in $window seconds, and counts this one */
function nlf_rl( $bucket, $max, $window, $who = '' ) {
	$who = '' === $who ? nlf_ip_hash() : (string) $who;
	$k   = 'nlf_rl_' . md5( $bucket . '|' . $who . '|' . (int) floor( time() / $window ) );
	$n   = (int) get_transient( $k );
	if ( $n >= $max ) { return false; }
	set_transient( $k, $n + 1, $window );
	return true;
}

/** how many hits a bucket has in the current window, without counting */
function nlf_rl_peek( $bucket, $window, $who = '' ) {
	$who = '' === $who ? nlf_ip_hash() : (string) $who;
	return (int) get_transient( 'nlf_rl_' . md5( $bucket . '|' . $who . '|' . (int) floor( time() / $window ) ) );
}

/** content writes this hour: the larger of the hashed IP's count and the member's own count */
function nlf_writes_hour( $m ) {
	return max( nlf_rl_peek( 'w', HOUR_IN_SECONDS ), nlf_rl_peek( 'wm', HOUR_IN_SECONDS, 'm' . (int) $m['id'] ) );
}

/** count one content write for the hashed IP AND for the member */
function nlf_write_counted( $m ) {
	nlf_rl( 'w', 100000, HOUR_IN_SECONDS );
	nlf_rl( 'wm', 100000, HOUR_IN_SECONDS, 'm' . (int) $m['id'] );
}

function nlf_pow_bits() { return max( 8, min( 20, (int) get_option( 'nadlan_forum_pow_bits', 14 ) ) ); }

/** a fresh challenge and form time, sent with every answer so the next write needs no extra round trip */
function nlf_fresh() {
	return array( 'ch' => nlf_challenge_make( nlf_key(), time(), nlf_pow_bits(), bin2hex( random_bytes( 12 ) ) ), 'ts' => nlf_form_ts_make( nlf_key(), time() ) );
}

/** errors are HTTP 400, never 403: the host turns a 403 into its own 404 page and the message is lost */
function nlf_err( $msg, $code = 'nlf' ) {
	nlf_nocache();
	return new WP_Error( $code, $msg, array_merge( array( 'status' => 400 ), nlf_fresh() ) );
}

function nlf_ok( array $data = array() ) {
	nlf_nocache(); // LiteSpeed Cache may cache REST GET answers; a member's state or nonce must never be stored
	$r = new WP_REST_Response( array_merge( array( 'ok' => 1 ), $data, nlf_fresh() ), 200 );
	$r->header( 'Cache-Control', 'no-store' );
	return $r;
}

/* =========================================================================================================
 * 3. Tables
 * ======================================================================================================= */

function nlf_t( $name ) { global $wpdb; return $wpdb->prefix . 'nadlan_forum_' . $name; }

function nlf_db_ready() { return NADLAN_FORUM_DB === (string) get_option( 'nadlan_forum_db_version' ); }

/** the tables once per NADLAN_FORUM_DB version (never on every request); a failed attempt waits an hour before the next */
function nlf_install() {
	if ( nlf_db_ready() || get_transient( 'nlf_install_wait' ) ) { return; }
	global $wpdb;
	require_once ABSPATH . 'wp-admin/includes/upgrade.php';
	$c = $wpdb->get_charset_collate();
	dbDelta( 'CREATE TABLE ' . nlf_t( 'topics' ) . " (
		id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
		cat VARCHAR(20) NOT NULL DEFAULT 'general',
		kind VARCHAR(10) NOT NULL DEFAULT 'question',
		title VARCHAR(200) NOT NULL DEFAULT '',
		body TEXT NOT NULL,
		member_id BIGINT UNSIGNED NOT NULL,
		pro_id BIGINT UNSIGNED NULL,
		city VARCHAR(60) NOT NULL DEFAULT '',
		status VARCHAR(10) NOT NULL DEFAULT 'pending',
		reply_count INT UNSIGNED NOT NULL DEFAULT 0,
		view_count INT UNSIGNED NOT NULL DEFAULT 0,
		thanks_count INT UNSIGNED NOT NULL DEFAULT 0,
		solved_reply_id BIGINT UNSIGNED NULL,
		pro_notified TINYINT(1) NOT NULL DEFAULT 0,
		need_profession VARCHAR(20) NULL,
		need_city VARCHAR(60) NULL,
		status_seek VARCHAR(10) NULL,
		body_hash CHAR(64) NOT NULL DEFAULT '',
		ip_hash CHAR(64) NOT NULL DEFAULT '',
		created_at DATETIME NOT NULL,
		last_at DATETIME NOT NULL,
		PRIMARY KEY  (id),
		KEY status_last (status,last_at),
		KEY cat_status (cat,status),
		KEY member_id (member_id),
		KEY pro_id (pro_id),
		KEY seek (kind,status_seek)
	) $c;" );
	dbDelta( 'CREATE TABLE ' . nlf_t( 'replies' ) . " (
		id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
		topic_id BIGINT UNSIGNED NOT NULL,
		member_id BIGINT UNSIGNED NOT NULL,
		body TEXT NOT NULL,
		quote_id BIGINT UNSIGNED NULL,
		status VARCHAR(10) NOT NULL DEFAULT 'pending',
		thanks_count INT UNSIGNED NOT NULL DEFAULT 0,
		body_hash CHAR(64) NOT NULL DEFAULT '',
		ip_hash CHAR(64) NOT NULL DEFAULT '',
		created_at DATETIME NOT NULL,
		PRIMARY KEY  (id),
		KEY topic_status (topic_id,status),
		KEY member_id (member_id)
	) $c;" );
	dbDelta( 'CREATE TABLE ' . nlf_t( 'members' ) . " (
		id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
		display_name VARCHAR(60) NOT NULL DEFAULT '',
		contact VARCHAR(190) NOT NULL DEFAULT '',
		contact_hash CHAR(64) NOT NULL,
		pro_id BIGINT UNSIGNED NULL,
		role_label VARCHAR(20) NOT NULL DEFAULT '',
		trade VARCHAR(40) NOT NULL DEFAULT '',
		trade_other VARCHAR(60) NOT NULL DEFAULT '',
		approved_posts INT UNSIGNED NOT NULL DEFAULT 0,
		status VARCHAR(10) NOT NULL DEFAULT 'ok',
		session_hash CHAR(64) NOT NULL DEFAULT '',
		show_phone TINYINT(1) NOT NULL DEFAULT 0,
		digest TINYINT(1) NOT NULL DEFAULT 0,
		created_at DATETIME NOT NULL,
		last_seen DATETIME NOT NULL,
		PRIMARY KEY  (id),
		UNIQUE KEY contact_hash (contact_hash),
		KEY session_hash (session_hash),
		KEY pro_id (pro_id)
	) $c;" );
	dbDelta( 'CREATE TABLE ' . nlf_t( 'codes' ) . " (
		contact_hash CHAR(64) NOT NULL,
		code_hash CHAR(64) NOT NULL,
		tries TINYINT UNSIGNED NOT NULL DEFAULT 0,
		expires_at DATETIME NOT NULL,
		PRIMARY KEY  (contact_hash)
	) $c;" );
	dbDelta( 'CREATE TABLE ' . nlf_t( 'flags' ) . " (
		id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
		target_type VARCHAR(10) NOT NULL,
		target_id BIGINT UNSIGNED NOT NULL,
		member_id BIGINT UNSIGNED NOT NULL,
		ip_hash CHAR(64) NOT NULL DEFAULT '',
		reason VARCHAR(20) NOT NULL DEFAULT '',
		created_at DATETIME NOT NULL,
		PRIMARY KEY  (id),
		UNIQUE KEY one_flag (member_id,target_type,target_id),
		KEY target (target_type,target_id)
	) $c;" );
	dbDelta( 'CREATE TABLE ' . nlf_t( 'thanks' ) . " (
		id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
		member_id BIGINT UNSIGNED NOT NULL,
		target_type VARCHAR(10) NOT NULL,
		target_id BIGINT UNSIGNED NOT NULL,
		PRIMARY KEY  (id),
		UNIQUE KEY one_thanks (member_id,target_type,target_id),
		KEY target (target_type,target_id)
	) $c;" );
	dbDelta( 'CREATE TABLE ' . nlf_t( 'follows' ) . " (
		id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
		member_id BIGINT UNSIGNED NOT NULL,
		topic_id BIGINT UNSIGNED NOT NULL,
		created_at DATETIME NOT NULL,
		PRIMARY KEY  (id),
		UNIQUE KEY one_follow (member_id,topic_id),
		KEY topic_id (topic_id)
	) $c;" );
	dbDelta( 'CREATE TABLE ' . nlf_t( 'requests' ) . " (
		id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
		kind VARCHAR(12) NOT NULL DEFAULT 'ownership',
		pro_id BIGINT UNSIGNED NOT NULL,
		member_id BIGINT UNSIGNED NOT NULL,
		contact VARCHAR(190) NOT NULL DEFAULT '',
		phone VARCHAR(30) NOT NULL DEFAULT '',
		body TEXT NOT NULL,
		status VARCHAR(10) NOT NULL DEFAULT 'pending',
		created_at DATETIME NOT NULL,
		PRIMARY KEY  (id),
		KEY status (status)
	) $c;" );
	foreach ( array( 'topics', 'replies', 'members', 'codes', 'flags', 'thanks', 'follows', 'requests' ) as $name ) {
		if ( nlf_t( $name ) !== (string) $wpdb->get_var( $wpdb->prepare( 'SHOW TABLES LIKE %s', $wpdb->esc_like( nlf_t( $name ) ) ) ) ) {
			set_transient( 'nlf_install_wait', 1, HOUR_IN_SECONDS ); // the version is stored only when every table exists
			return;
		}
	}
	update_option( 'nadlan_forum_db_version', NADLAN_FORUM_DB, true );
}
add_action( 'admin_init', 'nlf_install' );

function nlf_now_sql() { return gmdate( 'Y-m-d H:i:s' ); }

/** a stored UTC datetime as a unix time; 0 for none. 1.72.670 (live check 12.11.2026): an empty value read as "now"
 *  (strtotime(' UTC') is the current time), so a member with no posts was told to wait before every first post */
function nlf_ts( $sql_utc ) {
	$s = trim( (string) $sql_utc );
	if ( '' === $s || 0 === strpos( $s, '0000-00-00' ) ) { return 0; }
	$t = strtotime( $s . ' UTC' );
	return $t ? $t : 0;
}

/* =========================================================================================================
 * 4. Members and the session
 * ======================================================================================================= */

/** the member of this request (the session cookie), or null. nlf_me( true ) forgets the cached answer. */
function nlf_me( $reset = false ) {
	static $me = false;
	if ( $reset ) { $me = false; return null; }
	if ( false !== $me ) { return $me; }
	$me  = null;
	$tok = isset( $_COOKIE['nlf_s'] ) ? (string) $_COOKIE['nlf_s'] : '';
	if ( ! preg_match( '/^[a-f0-9]{64}$/', $tok ) || ! nlf_db_ready() ) { return null; }
	global $wpdb;
	$row = $wpdb->get_row( $wpdb->prepare( 'SELECT * FROM ' . nlf_t( 'members' ) . ' WHERE session_hash = %s LIMIT 1', hash( 'sha256', $tok ) ), ARRAY_A );
	if ( ! $row ) { return null; }
	$seen = nlf_ts( $row['last_seen'] );
	if ( $seen < time() - 90 * DAY_IN_SECONDS ) { return null; }
	if ( $seen < time() - HOUR_IN_SECONDS ) {
		$wpdb->update( nlf_t( 'members' ), array( 'last_seen' => nlf_now_sql() ), array( 'id' => (int) $row['id'] ) );
	}
	$me = $row;
	return $me;
}

function nlf_session_start( $member_id ) {
	global $wpdb;
	$tok = bin2hex( random_bytes( 32 ) );
	$wpdb->update( nlf_t( 'members' ), array( 'session_hash' => hash( 'sha256', $tok ), 'last_seen' => nlf_now_sql() ), array( 'id' => (int) $member_id ) );
	nlf_cookie( 'nlf_s', $tok, time() + 90 * DAY_IN_SECONDS, true );
	nlf_me( true );
}

function nlf_session_end() {
	$m = nlf_me();
	if ( $m ) {
		global $wpdb;
		$wpdb->update( nlf_t( 'members' ), array( 'session_hash' => '' ), array( 'id' => (int) $m['id'] ) );
	}
	nlf_cookie( 'nlf_s', '', time() - 3600, true );
	nlf_me( true );
}

/** the per-session header nonce (a cross-site page can neither read it nor send the header) */
function nlf_nonce_for( $m ) { return $m ? substr( hash_hmac( 'sha256', 'nonce|' . (string) $m['session_hash'], nlf_key() ), 0, 32 ) : ''; }

/** the professional card whose `email` or `_nl_email` equals this address (case-insensitive), or 0 */
function nlf_pro_for_email( $email ) {
	$email = nlf_contact_norm( $email );
	if ( '' === $email ) { return 0; }
	global $wpdb;
	$id = (int) $wpdb->get_var( $wpdb->prepare(
		"SELECT p.ID FROM {$wpdb->posts} p JOIN {$wpdb->postmeta} m ON m.post_id = p.ID
		 WHERE p.post_type = 'nadlan_professional' AND p.post_status IN ('publish','private','pending')
		 AND m.meta_key IN ('email','_nl_email') AND LOWER(TRIM(m.meta_value)) = %s
		 ORDER BY (p.post_status = 'publish') DESC, p.ID ASC LIMIT 1", $email ) );
	return $id;
}

/**
 * Owner correction 12.11.2026: the cards came from public registers and their people did not ask to take part. A professional
 * is a participant only after joining himself: a member row linked to the card through the verified email. Returns that member
 * (status ok) or null. Nothing in this module shows, addresses or mails a card that has no such member.
 */
function nlf_pro_member( $pro ) {
	static $memo = array();
	$pro = (int) $pro;
	if ( $pro <= 0 || ! nlf_db_ready() ) { return null; }
	if ( array_key_exists( $pro, $memo ) ) { return $memo[ $pro ]; }
	global $wpdb;
	$m = $wpdb->get_row( $wpdb->prepare( 'SELECT * FROM ' . nlf_t( 'members' ) . " WHERE pro_id = %d AND status = 'ok' ORDER BY last_seen DESC LIMIT 1", $pro ), ARRAY_A );
	return $memo[ $pro ] = $m ? $m : null;
}

/** the forum category that matches a profession (for a "seek" request prefilled from a card) */
function nlf_cat_for_profession( $prof ) {
	$map = array( 'lawyer' => 'law', 'accountant' => 'law', 'shamai' => 'value', 'surveyor' => 'value', 'actuary' => 'value', 'mashkanta' => 'loans', 'insurance' => 'loans',
		'interior_designer' => 'design', 'kitchens' => 'design', 'furniture' => 'design', 'lighting' => 'design', 'metavech' => 'agents', 'property_manager' => 'agents',
		'developer' => 'renewal', 'urban_planner' => 'renewal', 'organizer' => 'renewal' );
	if ( isset( $map[ (string) $prof ] ) ) { return $map[ (string) $prof ]; }
	if ( function_exists( 'nadlan_pro_registry' ) ) {
		$r = nadlan_pro_registry();
		if ( isset( $r[ $prof ] ) && in_array( $r[ $prof ]['group'], array( 'build', 'systems' ), true ) ) { return 'build'; }
		if ( isset( $r[ $prof ] ) && 'design' === $r[ $prof ]['group'] ) { return 'design'; }
	}
	return 'general';
}

function nlf_pro_removed( $pro ) { return '' !== (string) get_post_meta( (int) $pro, 'nl_removed_by_owner', true ); }

function nlf_pro_profession( $pro ) { return (string) get_post_meta( (int) $pro, 'profession', true ); }

function nlf_pro_label( $pro ) {
	$p = nlf_pro_profession( $pro );
	if ( function_exists( 'nadlan_dir_prof_label' ) ) { return (string) nadlan_dir_prof_label( $p, (int) $pro ); }
	if ( function_exists( 'nadlan_pro_registry' ) ) { $r = nadlan_pro_registry(); if ( isset( $r[ $p ] ) ) { return $r[ $p ]['label']; } }
	return 'בעל מקצוע';
}

/** the plural for "את כל ה..." */
function nlf_pro_plural_phrase( $pro ) {
	$p  = nlf_pro_profession( $pro );
	$pl = '';
	if ( function_exists( 'nadlan_pro_registry' ) ) { $r = nadlan_pro_registry(); if ( isset( $r[ $p ] ) ) { $pl = $r[ $p ]['plural']; } }
	if ( '' === $pl && function_exists( 'nadlan_dir_prof_plural' ) ) { $pl = (string) nadlan_dir_prof_plural( $p, '' ); }
	if ( '' === $pl ) { return 'כל בעלי המקצוע'; }
	return false === mb_strpos( $pl, ' ' ) ? 'כל ה' . $pl : 'כל ' . $pl; // a construct phrase takes no ה before it
}

function nlf_pro_female( $pro ) { return 'f' === (string) get_post_meta( (int) $pro, 'nl_gender', true ); }

/** the site's existing verified mark (nadlan_dir_registry_verified), worded as the site's trust labels; '' when not verified */
function nlf_verified_text( $pro ) {
	if ( ! function_exists( 'nadlan_dir_registry_verified' ) || ! nadlan_dir_registry_verified( (int) $pro ) ) { return ''; }
	$p = nlf_pro_profession( $pro );
	if ( 'kablan' === $p ) { return 'רשום בפנקס הקבלנים'; }
	if ( 'metavech' === $p ) { return 'רישיון בפנקס המתווכים'; }
	return 'פרטים נבדקו מול מאגר רשמי';
}

/** the professional's own WhatsApp digits and dial number, only when he switched the phone on in this module */
function nlf_pro_phone( $pro, $member ) {
	if ( ! $member || empty( $member['show_phone'] ) || (int) $member['pro_id'] !== (int) $pro || 'publish' !== get_post_status( (int) $pro ) ) { return null; }
	$raw = trim( (string) get_post_meta( (int) $pro, 'phone', true ) );
	$d   = preg_replace( '/\D+/', '', $raw );
	if ( strlen( $d ) < 9 ) { return null; }
	$wa = function_exists( 'nadlan_prof_wa_digits' ) ? (string) nadlan_prof_wa_digits( $raw ) : ( '0' === $d[0] ? '972' . substr( $d, 1 ) : $d );
	return array( 'wa' => $wa, 'tel' => preg_replace( '/[^\d+]/', '', $raw ) );
}

/** members by id, one query */
function nlf_members( array $ids ) {
	$ids = array_values( array_unique( array_filter( array_map( 'intval', $ids ) ) ) );
	if ( ! $ids ) { return array(); }
	global $wpdb;
	$rows = $wpdb->get_results( $wpdb->prepare( 'SELECT * FROM ' . nlf_t( 'members' ) . ' WHERE id IN (' . implode( ',', array_fill( 0, count( $ids ), '%d' ) ) . ')', $ids ), ARRAY_A );
	$out  = array();
	foreach ( (array) $rows as $r ) { $out[ (int) $r['id'] ] = $r; }
	return $out;
}

/** how a member is shown: name, label, verified line, tint, profile link, phone (only when switched on) */
function nlf_author( $m ) {
	$a = array( 'name' => 'משתמש', 'label' => '', 'verified' => '', 'tint' => array( '#E3E6E8', '#22303A' ), 'url' => '', 'pro' => 0, 'phone' => null, 'female' => false );
	if ( ! $m ) { return $a; }
	$a['name'] = '' !== (string) $m['display_name'] ? (string) $m['display_name'] : 'משתמש';
	$pro = (int) $m['pro_id'];
	if ( $pro > 0 && 'nadlan_professional' === get_post_type( $pro ) ) {
		if ( nlf_pro_removed( $pro ) ) { return $a; } // the owner removed the profile: the name only
		$a['pro']      = $pro;
		$a['label']    = nlf_pro_label( $pro );
		$a['verified'] = nlf_verified_text( $pro );
		$a['tint']     = nlf_prof_tint( nlf_pro_profession( $pro ) );
		$a['female']   = nlf_pro_female( $pro );
		$a['url']      = 'publish' === get_post_status( $pro ) ? (string) get_permalink( $pro ) : '';
		$a['phone']    = nlf_pro_phone( $pro, $m );
		return $a;
	}
	$roles = nlf_roles();
	$a['label'] = isset( $roles[ $m['role_label'] ] ) ? $roles[ $m['role_label'] ] : '';
	// a member who chose a trade from the list shows it (never a verified mark: no licence was checked); free text stays for review only
	if ( 'pro' === (string) $m['role_label'] && '' !== (string) ( $m['trade'] ?? '' ) ) {
		$tr = nlf_trade( (string) $m['trade'] );
		if ( $tr ) { $a['label'] = $tr['label']; }
	}
	return $a;
}

/** the trade list a member picks from (inc/pro-forum-trades.php, 84 trades in 6 groups); array() when the file is missing */
function nlf_trades() { return function_exists( 'nadlan_forum_trades' ) ? (array) nadlan_forum_trades() : array(); }

function nlf_trade( $key ) { $t = nlf_trades(); return ( '' !== (string) $key && isset( $t[ $key ] ) ) ? $t[ $key ] : null; }

/** the public state of the member for the page script */
function nlf_member_state( $m ) {
	if ( ! $m ) { return null; }
	$au = nlf_author( $m );
	return array( 'id' => (int) $m['id'], 'name' => $au['name'], 'label' => $au['label'], 'pro' => (int) $m['pro_id'], 'status' => (string) $m['status'] );
}

/* =========================================================================================================
 * 5. The guard: every write passes here
 * ======================================================================================================= */

/**
 * $kind: 'view' (gate + limit only), 'entry' (no member yet), 'light' (thanks, follow, owner switches), 'post' (content).
 * Returns the member row (array, empty for entry/view) or a WP_Error 400 with a Hebrew message.
 */
function nlf_guard( WP_REST_Request $r, $kind ) {
	if ( ! nlf_gate_open() ) { return nlf_err( 'הדף לא נמצא.', 'nlf_closed' ); }
	nlf_install();
	if ( 'view' === $kind ) { return nlf_rl( 'view', 240, HOUR_IN_SECONDS ) ? array() : nlf_err( 'נסו שוב מאוחר יותר.' ); }
	if ( '' !== trim( (string) $r->get_param( 'website' ) ) ) { return nlf_err( 'לא הצלחנו לשלוח. נסו שוב.' ); }
	$e = nlf_form_ts_error( (string) $r->get_param( 'ts' ), nlf_key(), time() );
	if ( '' !== $e ) { return nlf_err( $e, 'nlf_ts' ); }
	$salt = nlf_challenge_check( (string) $r->get_param( 'ch' ), (string) $r->get_param( 'n' ), nlf_key(), time(), 600 );
	if ( '' === $salt || get_transient( 'nlf_pw_' . $salt ) ) { return nlf_err( 'בדיקת האבטחה לא הושלמה. נסו שוב.', 'nlf_pow' ); }
	set_transient( 'nlf_pw_' . $salt, 1, 15 * MINUTE_IN_SECONDS ); // single use
	if ( 'entry' === $kind ) {
		return nlf_rl( 'entry', 30, HOUR_IN_SECONDS ) ? array() : nlf_err( 'יותר מדי ניסיונות. נסו שוב בעוד שעה.' );
	}
	$m = nlf_me();
	if ( ! $m ) { return nlf_err( 'כדי לכתוב צריך להיכנס. זה צעד אחד.', 'nlf_need_entry' ); }
	if ( ! hash_equals( nlf_nonce_for( $m ), (string) $r->get_header( 'x_nlf_nonce' ) ) ) { return nlf_err( 'הדף ישן. רעננו אותו ונסו שוב.', 'nlf_nonce' ); }
	if ( 'ok' !== (string) $m['status'] ) { return nlf_err( 'החשבון הזה לא יכול לכתוב בפורום כרגע.', 'nlf_blocked' ); }
	if ( 'post' === $kind ) { // ceilings per hashed IP AND per member
		if ( nlf_writes_hour( $m ) >= 20 ) { return nlf_err( 'הגעתם למספר ההודעות המרבי לשעה. נסו שוב מאוחר יותר.' ); }
	} elseif ( ! nlf_rl( 'light', 90, HOUR_IN_SECONDS ) || ! nlf_rl( 'lightm', 90, HOUR_IN_SECONDS, 'm' . (int) $m['id'] ) ) {
		return nlf_err( 'נסו שוב מאוחר יותר.' );
	}
	return $m;
}

/** the content limits for a member about to post; '' or a message */
function nlf_post_limits( $m, $is_topic, $text ) {
	global $wpdb;
	$err = nlf_text_rule_error( $text, (int) $m['approved_posts'] );
	if ( '' !== $err ) { return $err; }
	$mid     = (int) $m['id'];
	$created = nlf_ts( $m['created_at'] );
	$tt = nlf_t( 'topics' ); $rt = nlf_t( 'replies' );
	$since_sql = gmdate( 'Y-m-d H:i:s', $created );
	$last = max( (int) nlf_ts( (string) $wpdb->get_var( $wpdb->prepare( "SELECT MAX(created_at) FROM $tt WHERE member_id = %d", $mid ) ) ),
		(int) nlf_ts( (string) $wpdb->get_var( $wpdb->prepare( "SELECT MAX(created_at) FROM $rt WHERE member_id = %d", $mid ) ) ) );
	$err = nlf_limits_error( array(
		'is_topic'          => $is_topic,
		'approved'          => (int) $m['approved_posts'],
		'age'               => time() - $created,
		'topics_first_day'  => (int) $wpdb->get_var( $wpdb->prepare( "SELECT COUNT(*) FROM $tt WHERE member_id = %d AND created_at >= %s", $mid, $since_sql ) ),
		'replies_first_day' => (int) $wpdb->get_var( $wpdb->prepare( "SELECT COUNT(*) FROM $rt WHERE member_id = %d AND created_at >= %s", $mid, $since_sql ) ),
		'since_last'        => $last > 0 ? time() - $last : null,
		'ip_hour'           => nlf_writes_hour( $m ),
	) );
	if ( '' !== $err ) { return $err; }
	$since  = gmdate( 'Y-m-d H:i:s', time() - 300 );
	$recent = array();
	foreach ( array( $tt, $rt ) as $tab ) {
		foreach ( (array) $wpdb->get_results( $wpdb->prepare( "SELECT body_hash, created_at FROM $tab WHERE member_id = %d AND created_at >= %s", $mid, $since ), ARRAY_A ) as $row ) {
			$recent[] = array( $row['body_hash'], nlf_ts( $row['created_at'] ) );
		}
	}
	if ( nlf_dup_hit( $recent, nlf_dup_key( $text ), time(), 300 ) ) { return 'כבר שלחתם את ההודעה הזאת. אין צורך לשלוח שוב.'; }
	return '';
}

/* =========================================================================================================
 * 6. Topics, replies, moderation, counters
 * ======================================================================================================= */

function nlf_topic( $id ) {
	if ( ! nlf_db_ready() ) { return null; }
	global $wpdb;
	$t = $wpdb->get_row( $wpdb->prepare( 'SELECT * FROM ' . nlf_t( 'topics' ) . ' WHERE id = %d', (int) $id ), ARRAY_A );
	return $t ? $t : null;
}

function nlf_reply( $id ) {
	global $wpdb;
	$r = $wpdb->get_row( $wpdb->prepare( 'SELECT * FROM ' . nlf_t( 'replies' ) . ' WHERE id = %d', (int) $id ), ARRAY_A );
	return $r ? $r : null;
}

function nlf_is_admin() { return current_user_can( 'manage_options' ); }

/** live = everyone; any other status = its author and administrators only */
function nlf_topic_visible( $t, $me ) {
	if ( ! $t ) { return false; }
	if ( 'live' === $t['status'] || nlf_is_admin() ) { return true; }
	return $me && (int) $me['id'] === (int) $t['member_id'] && 'removed' !== $t['status'];
}

function nlf_topic_url( $id, $hash = '' ) {
	$u = home_url( '/forum/' . (int) $id . '/' );
	if ( ! nlf_public() ) { $u = add_query_arg( 'forum', 'on', $u ); } // a link in a mail while the forum is hidden opens the gate
	return $u . ( '' !== $hash ? '#' . $hash : '' );
}

function nlf_home_url( $args = array() ) {
	$args = array_filter( (array) $args, function ( $v ) { return '' !== (string) $v && null !== $v; } );
	return $args ? add_query_arg( array_map( 'rawurlencode', $args ), home_url( '/forum/' ) ) : home_url( '/forum/' );
}

function nlf_recount_topic( $tid ) {
	global $wpdb;
	$n    = (int) $wpdb->get_var( $wpdb->prepare( 'SELECT COUNT(*) FROM ' . nlf_t( 'replies' ) . " WHERE topic_id = %d AND status = 'live'", (int) $tid ) );
	$last = (string) $wpdb->get_var( $wpdb->prepare( 'SELECT MAX(created_at) FROM ' . nlf_t( 'replies' ) . " WHERE topic_id = %d AND status = 'live'", (int) $tid ) );
	$t    = nlf_topic( $tid );
	if ( ! $t ) { return; }
	$wpdb->update( nlf_t( 'topics' ), array( 'reply_count' => $n, 'last_at' => '' !== $last && $last > $t['created_at'] ? $last : $t['created_at'] ), array( 'id' => (int) $tid ) );
}

function nlf_member_live_bump( $mid ) {
	global $wpdb;
	$wpdb->query( $wpdb->prepare( 'UPDATE ' . nlf_t( 'members' ) . ' SET approved_posts = approved_posts + 1 WHERE id = %d', (int) $mid ) );
}

function nlf_follow( $mid, $tid, $on ) {
	global $wpdb;
	if ( $on ) {
		$wpdb->query( $wpdb->prepare( 'INSERT IGNORE INTO ' . nlf_t( 'follows' ) . ' (member_id, topic_id, created_at) VALUES (%d, %d, %s)', (int) $mid, (int) $tid, nlf_now_sql() ) );
	} else {
		$wpdb->delete( nlf_t( 'follows' ), array( 'member_id' => (int) $mid, 'topic_id' => (int) $tid ) );
	}
}

function nlf_follows( $mid, $tid ) {
	global $wpdb;
	return (bool) $wpdb->get_var( $wpdb->prepare( 'SELECT id FROM ' . nlf_t( 'follows' ) . ' WHERE member_id = %d AND topic_id = %d', (int) $mid, (int) $tid ) );
}

/** a topic went live for the first time: the author's count, the professional's one notification */
function nlf_on_topic_live( $tid ) {
	$t = nlf_topic( $tid );
	if ( ! $t ) { return; }
	nlf_member_live_bump( (int) $t['member_id'] );
	nlf_notify_pro( $t );
}

function nlf_on_reply_live( $rid ) {
	$r = nlf_reply( $rid );
	if ( ! $r ) { return; }
	nlf_member_live_bump( (int) $r['member_id'] );
	nlf_recount_topic( (int) $r['topic_id'] );
	nlf_notify_followers( $r );
}

/**
 * Moderation in one place (admin screen and the one-click mail links). $type topic|reply, $to live|hidden|removed.
 * pending -> live runs the first-time effects; hidden -> live restores without them.
 */
function nlf_moderate( $type, $id, $to ) {
	if ( ! in_array( $to, array( 'live', 'hidden', 'removed' ), true ) ) { return false; }
	global $wpdb;
	$row = 'topic' === $type ? nlf_topic( $id ) : nlf_reply( $id );
	if ( ! $row ) { return false; }
	$from = (string) $row['status'];
	$wpdb->update( nlf_t( 'topic' === $type ? 'topics' : 'replies' ), array( 'status' => $to ), array( 'id' => (int) $id ) );
	if ( 'live' === $to && 'pending' === $from ) {
		if ( 'topic' === $type ) { nlf_on_topic_live( $id ); } else { nlf_on_reply_live( $id ); }
	} elseif ( 'reply' === $type ) {
		nlf_recount_topic( (int) $row['topic_id'] );
	}
	return true;
}

function nlf_member_set_status( $mid, $status ) {
	if ( ! in_array( $status, array( 'ok', 'silenced', 'blocked' ), true ) ) { return false; }
	global $wpdb;
	return false !== $wpdb->update( nlf_t( 'members' ), array( 'status' => $status ), array( 'id' => (int) $mid ) );
}

/* =========================================================================================================
 * 7. Mail
 * ======================================================================================================= */

function nlf_mail( $to, $subject, $body, $unsub_url = '' ) {
	$h = array( 'Content-Type: text/plain; charset=UTF-8' );
	if ( '' !== $unsub_url ) { $h[] = 'List-Unsubscribe: <' . esc_url_raw( $unsub_url ) . '>'; }
	return wp_mail( $to, $subject, $body, $h );
}

/** a one-click link (front page + ?nlf_act=), handled in pro-forum-render.php; works with the gate closed too */
function nlf_act_url( $action, $id, $ttl = 0 ) {
	return add_query_arg( 'nlf_act', nlf_link_token( $action, $id, $ttl > 0 ? time() + $ttl : 0, nlf_key() ), home_url( '/' ) );
}

function nlf_admin_to() { return (string) apply_filters( 'nadlan_forum_admin_email', (string) get_option( 'admin_email' ) ); }

function nlf_mail_admin_pending( $type, $id ) {
	$row  = 'topic' === $type ? nlf_topic( $id ) : nlf_reply( $id );
	if ( ! $row ) { return; }
	$m    = nlf_members( array( (int) $row['member_id'] ) );
	$m    = $m ? reset( $m ) : null;
	$tid  = 'topic' === $type ? (int) $id : (int) $row['topic_id'];
	$t    = nlf_topic( $tid );
	$tok  = ( 'topic' === $type ? 't' : 'r' ) . (int) $id;
	$body = "הודעה ראשונה של משתתף חדש מחכה לבדיקה.\n\n"
		. 'מאת: ' . ( $m ? $m['display_name'] . ' (' . $m['contact'] . ')' : '' ) . "\n"
		. 'דיון: ' . ( $t ? $t['title'] : '' ) . "\n\n"
		. ( 'topic' === $type ? '' : "התשובה:\n" ) . nlf_excerpt( $row['body'], 1200 ) . "\n\n"
		. 'אישור: ' . nlf_act_url( 'ok', $tok, 14 * DAY_IN_SECONDS ) . "\n"
		. 'דחייה: ' . nlf_act_url( 'no', $tok, 14 * DAY_IN_SECONDS ) . "\n\n"
		. 'כל ההודעות שמחכות: ' . admin_url( 'admin.php?page=nadlan-forum' ) . "\n";
	nlf_mail( nlf_admin_to(), '[פורום] הודעה חדשה מחכה לבדיקה', $body );
}

function nlf_notify_followers( $reply ) {
	$t = nlf_topic( (int) $reply['topic_id'] );
	if ( ! $t || 'live' !== $t['status'] ) { return; }
	global $wpdb;
	$rows = $wpdb->get_results( $wpdb->prepare( 'SELECT m.id, m.contact FROM ' . nlf_t( 'follows' ) . ' f JOIN ' . nlf_t( 'members' ) . " m ON m.id = f.member_id
		WHERE f.topic_id = %d AND m.id <> %d AND m.status = 'ok' AND m.contact <> '' LIMIT 200", (int) $t['id'], (int) $reply['member_id'] ), ARRAY_A );
	if ( ! $rows ) { return; }
	$au = nlf_members( array( (int) $reply['member_id'] ) );
	$au = nlf_author( $au ? reset( $au ) : null );
	foreach ( $rows as $f ) {
		$unf  = nlf_act_url( 'unf', 'm' . (int) $f['id'] . 't' . (int) $t['id'] );
		$body = $au['name'] . ' כתב/ה תשובה חדשה בדיון "' . $t['title'] . "\":\n\n" . nlf_excerpt( $reply['body'], 400 ) . "\n\n"
			. 'לקריאה ולתשובה: ' . nlf_topic_url( (int) $t['id'], 'r' . (int) $reply['id'] ) . "\n\n"
			. 'לא לקבל עוד הודעות על הדיון הזה: ' . $unf . "\n";
		nlf_mail( $f['contact'], 'תשובה חדשה בדיון: ' . nlf_excerpt( $t['title'], 80 ), $body, $unf );
	}
}

/**
 * ONE mail per discussion to a JOINED professional who was asked directly (owner correction 12.11.2026: never to an address
 * on a register card; only to the member's own verified email). One-click opt-out kept on the card forever (nl_forum_optout=1).
 */
function nlf_notify_pro( $t ) {
	$pro = (int) $t['pro_id'];
	if ( $pro <= 0 || (int) $t['pro_notified'] || 'live' !== $t['status'] ) { return; }
	if ( '1' === (string) get_post_meta( $pro, 'nl_forum_optout', true ) || nlf_pro_removed( $pro ) ) { return; }
	$m = nlf_pro_member( $pro );
	if ( ! $m || (int) $m['id'] === (int) $t['member_id'] || '' === (string) $m['contact'] ) { return; }
	global $wpdb;
	$wpdb->update( nlf_t( 'topics' ), array( 'pro_notified' => 1 ), array( 'id' => (int) $t['id'] ) );
	$opt  = nlf_act_url( 'opt', 'p' . $pro );
	$body = "שלום,\n\nבפורום נדל\"ן שאלו אתכם ישירות:\n\n\"" . $t['title'] . "\"\n"
		. ( '' !== trim( $t['body'] ) ? "\n" . nlf_excerpt( $t['body'], 800 ) . "\n" : '' )
		. "\nלקריאה ולתשובה: " . nlf_topic_url( (int) $t['id'] ) . "\n\n"
		. 'לא לקבל עוד הודעות מהפורום: ' . $opt . "\n";
	nlf_mail( (string) $m['contact'], 'שאלה חדשה אליכם בפורום נדל"ן', $body, $opt );
}

/* =========================================================================================================
 * 8. Owner controls (the linked professional only)
 * ======================================================================================================= */

function nlf_owner_state( $pro ) {
	$me = nlf_me();
	return array(
		'visible' => 'publish' === get_post_status( (int) $pro ),
		'phone'   => $me && (int) $me['pro_id'] === (int) $pro && ! empty( $me['show_phone'] ),
		'removed' => nlf_pro_removed( $pro ),
	);
}

/**
 * Status change of a card from a forum request (no WordPress user is logged in there). Without the guard below wp_update_post
 * would run the card's content through kses for an unprivileged user and strip its HTML (review 12.11.2026). LiteSpeed is asked
 * to purge the card so "hidden" is true at once.
 */
function nlf_pro_set_status( $pro, $status ) {
	$kses = false !== has_filter( 'content_save_pre', 'wp_filter_post_kses' );
	if ( $kses ) { kses_remove_filters(); }
	$r = wp_update_post( array( 'ID' => (int) $pro, 'post_status' => $status ), true );
	if ( $kses ) { kses_init_filters(); }
	clean_post_cache( (int) $pro );
	do_action( 'litespeed_purge_post', (int) $pro );
	return ! is_wp_error( $r ) && $r;
}

/** hide (private, previous status kept) / show (previous status back) */
function nlf_owner_hide( $pro, $meta_key, $meta_value ) {
	$st = (string) get_post_status( (int) $pro );
	if ( 'private' !== $st ) { update_post_meta( (int) $pro, 'nl_forum_prev_status', $st ); }
	update_post_meta( (int) $pro, $meta_key, $meta_value );
	return 'private' === $st || nlf_pro_set_status( $pro, 'private' );
}

/** show again: only a card the owner hid goes back, to its own previous status (a card the staff made private stays private) */
function nlf_owner_show( $pro ) {
	$hid  = '' !== (string) get_post_meta( (int) $pro, 'nl_forum_hidden_by_owner', true ) || nlf_pro_removed( $pro );
	$prev = (string) get_post_meta( (int) $pro, 'nl_forum_prev_status', true );
	delete_post_meta( (int) $pro, 'nl_forum_hidden_by_owner' );
	delete_post_meta( (int) $pro, 'nl_removed_by_owner' );
	delete_post_meta( (int) $pro, 'nl_forum_prev_status' );
	$to = nlf_restore_status( (string) get_post_status( (int) $pro ), $prev, $hid );
	return '' === $to || nlf_pro_set_status( $pro, $to );
}

function nlf_owner_shown_msg( $pro ) {
	return 'publish' === get_post_status( (int) $pro ) ? 'הפרופיל מוצג באתר.' : 'הפרופיל לא מוצג כרגע. שלחו בקשה על הכרטיס ונטפל בה.';
}

/* =========================================================================================================
 * 9. REST: nadlan/v1/forum/...
 * ======================================================================================================= */

add_action( 'rest_api_init', function () {
	$ns = 'nadlan/v1';
	$r  = function ( $path, $method, $cb ) use ( $ns ) {
		// show_in_index false: the public /wp-json/ index does not list the forum's routes while it is hidden
		register_rest_route( $ns, '/forum/' . $path, array( 'methods' => $method, 'permission_callback' => '__return_true', 'callback' => $cb, 'show_in_index' => false ) );
	};

	// the release runner's probe: ALWAYS 200, gate open or closed, exactly three keys, no data, never cached
	$r( 'ping', 'GET', function () {
		nlf_nocache();
		$p = new WP_REST_Response( array( 'loaded' => true, 'public' => nlf_public(), 'v' => NADLAN_FORUM_VERSION ), 200 );
		$p->header( 'Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0' );
		return $p;
	} );

	// the page script's state: who is in, the nonce, a fresh challenge and form time
	$r( 'state', 'GET', function () {
		if ( ! nlf_gate_open() ) { return nlf_err( 'הדף לא נמצא.', 'nlf_closed' ); }
		nlf_install();
		$m = nlf_me();
		return nlf_ok( array( 'member' => nlf_member_state( $m ), 'nonce' => nlf_nonce_for( $m ), 'bits' => nlf_pow_bits() ) );
	} );

	// step 1 of the entry: name + email, a 6-digit code by mail
	$r( 'code', 'POST', function ( WP_REST_Request $q ) {
		$g = nlf_guard( $q, 'entry' );
		if ( is_wp_error( $g ) ) { return $g; }
		$name  = nlf_text_norm( (string) $q->get_param( 'name' ), true );
		$email = sanitize_email( (string) $q->get_param( 'email' ) );
		if ( nlf_len( $name ) < 2 || nlf_len( $name ) > 40 ) { return nlf_err( 'כתבו שם, 2 עד 40 תווים.' ); }
		if ( nlf_has_link( $name ) || nlf_has_phone( $name ) ) { return nlf_err( 'בשם אי אפשר לכתוב קישור או מספר טלפון.' ); }
		if ( ! $email || ! is_email( $email ) ) { return nlf_err( 'כתובת המייל לא נראית תקינה.' ); }
		if ( '1' !== (string) $q->get_param( 'consent' ) ) { return nlf_err( 'כדי להמשיך צריך לאשר את כללי הפורום ואת מדיניות הפרטיות.' ); }
		$ch = nlf_contact_hash( $email, nlf_key() );
		// per hashed IP, and per address (3 an hour, 6 a day: the form cannot be used to flood someone's mailbox)
		if ( ! nlf_rl( 'code_ip', 10, HOUR_IN_SECONDS ) || ! nlf_rl( 'code_c', 3, HOUR_IN_SECONDS, $ch ) || ! nlf_rl( 'code_cd', 6, DAY_IN_SECONDS, $ch ) ) {
			return nlf_err( 'ביקשתם כבר כמה קודים. נסו שוב בעוד שעה.' );
		}
		$code = str_pad( (string) random_int( 0, 999999 ), 6, '0', STR_PAD_LEFT );
		global $wpdb;
		$wpdb->replace( nlf_t( 'codes' ), array( 'contact_hash' => $ch, 'code_hash' => nlf_code_hash( $code, $ch, nlf_key() ), 'tries' => 0,
			'expires_at' => gmdate( 'Y-m-d H:i:s', time() + 10 * MINUTE_IN_SECONDS ) ) );
		// an SMS sender can take over later: return true (sent) or false (failed); null = this module mails the code
		$sent = apply_filters( 'nadlan_forum_send_code', null, $email, $code, array( 'name' => $name ) );
		if ( null === $sent ) {
			$sent = nlf_mail( $email, 'הקוד שלכם לפורום נדל"ן: ' . $code,
				"הקוד שלכם לכניסה לפורום נדל\"ן: " . $code . "\n\nהקוד בתוקף 10 דקות.\nאם לא ביקשתם קוד, אפשר להתעלם מההודעה הזאת.\n" );
		}
		if ( ! $sent ) {
			$wpdb->delete( nlf_t( 'codes' ), array( 'contact_hash' => $ch ) );
			return nlf_err( 'לא הצלחנו לשלוח את הקוד. נסו שוב בעוד דקה.' );
		}
		return nlf_ok( array( 'message' => 'שלחנו קוד בן 6 ספרות אל ' . $email . '. הוא בתוקף 10 דקות.' ) );
	} );

	// step 2: the code; a session begins
	$r( 'enter', 'POST', function ( WP_REST_Request $q ) {
		$g = nlf_guard( $q, 'entry' );
		if ( is_wp_error( $g ) ) { return $g; }
		$email = sanitize_email( (string) $q->get_param( 'email' ) );
		$code  = preg_replace( '/\D/', '', (string) $q->get_param( 'code' ) );
		if ( ! $email || ! is_email( $email ) ) { return nlf_err( 'כתובת המייל לא נראית תקינה.' ); }
		$ch = nlf_contact_hash( $email, nlf_key() );
		global $wpdb;
		$row = $wpdb->get_row( $wpdb->prepare( 'SELECT * FROM ' . nlf_t( 'codes' ) . ' WHERE contact_hash = %s', $ch ), ARRAY_A );
		$v   = nlf_code_verdict( $row ? array( 'code_hash' => $row['code_hash'], 'tries' => (int) $row['tries'], 'expires' => nlf_ts( $row['expires_at'] ) ) : null, $code, $ch, time(), nlf_key() );
		if ( 'ok' !== $v ) {
			if ( 'wrong' === $v ) {
				$wpdb->query( $wpdb->prepare( 'UPDATE ' . nlf_t( 'codes' ) . ' SET tries = tries + 1 WHERE contact_hash = %s', $ch ) );
				$left = 5 - ( (int) $row['tries'] + 1 );
				return nlf_err( $left > 0 ? 'הקוד לא נכון. נסו שוב.' : 'יותר מדי ניסיונות. בקשו קוד חדש.' );
			}
			return nlf_err( 'tries' === $v ? 'יותר מדי ניסיונות. בקשו קוד חדש.' : 'הקוד פג תוקף. בקשו קוד חדש.' );
		}
		$wpdb->delete( nlf_t( 'codes' ), array( 'contact_hash' => $ch ) );
		$name = nlf_text_norm( (string) $q->get_param( 'name' ), true );
		$name = nlf_len( $name ) >= 2 && nlf_len( $name ) <= 40 && ! nlf_has_link( $name ) && ! nlf_has_phone( $name ) ? $name : '';
		$role = sanitize_key( (string) $q->get_param( 'role' ) );
		$role = isset( nlf_roles()[ $role ] ) ? $role : '';
		// a professional picks his trade from the list (the key is stored); "other" keeps his own words for the admin to review
		$trade = sanitize_key( (string) $q->get_param( 'trade' ) );
		$trade = 'pro' === $role && nlf_trade( $trade ) ? $trade : '';
		$other = 'pro' === $role && '' === $trade ? mb_substr( nlf_text_norm( (string) $q->get_param( 'trade_other' ), true ), 0, 60 ) : '';
		if ( '' !== $other && ( nlf_len( $other ) < 2 || nlf_has_link( $other ) || nlf_has_phone( $other ) ) ) { $other = ''; }
		$pro  = nlf_pro_for_email( $email );
		$mt   = nlf_t( 'members' );
		$m    = $wpdb->get_row( $wpdb->prepare( "SELECT * FROM $mt WHERE contact_hash = %s", $ch ), ARRAY_A );
		if ( $m ) {
			$upd = array( 'pro_id' => $pro > 0 ? $pro : null, 'contact' => nlf_contact_norm( $email ) );
			if ( '' !== $name ) { $upd['display_name'] = $name; }
			if ( '' !== $role ) { $upd['role_label'] = $role; $upd['trade'] = $trade; $upd['trade_other'] = $other; }
			$wpdb->update( $mt, $upd, array( 'id' => (int) $m['id'] ) );
			$mid = (int) $m['id'];
		} else {
			if ( '' === $name ) { return nlf_err( 'כתבו שם, 2 עד 40 תווים.' ); }
			$wpdb->insert( $mt, array( 'display_name' => $name, 'contact' => nlf_contact_norm( $email ), 'contact_hash' => $ch, 'pro_id' => $pro > 0 ? $pro : null,
				'role_label' => $role, 'trade' => $trade, 'trade_other' => $other, 'approved_posts' => 0, 'status' => 'ok', 'created_at' => nlf_now_sql(), 'last_seen' => nlf_now_sql() ) );
			$mid = (int) $wpdb->insert_id;
			if ( $mid <= 0 ) { return nlf_err( 'משהו השתבש. נסו שוב.' ); }
		}
		nlf_session_start( $mid );
		$me    = nlf_me();
		$claim = (int) $q->get_param( 'claim_pro' );
		return nlf_ok( array( 'member' => nlf_member_state( $me ), 'nonce' => nlf_nonce_for( $me ),
			'claim_mismatch' => $claim > 0 && (int) $me['pro_id'] !== $claim ? 1 : 0, 'message' => 'נכנסתם. אפשר לכתוב.' ) );
	} );

	$r( 'leave', 'POST', function ( WP_REST_Request $q ) {
		if ( ! nlf_gate_open() ) { return nlf_err( 'הדף לא נמצא.', 'nlf_closed' ); }
		$m = nlf_me();
		if ( $m && ! hash_equals( nlf_nonce_for( $m ), (string) $q->get_header( 'x_nlf_nonce' ) ) ) { return nlf_err( 'הדף ישן. רעננו אותו ונסו שוב.', 'nlf_nonce' ); }
		nlf_session_end();
		return nlf_ok( array( 'member' => null, 'message' => 'יצאתם מהפורום.' ) );
	} );

	// open a discussion
	$r( 'topic', 'POST', function ( WP_REST_Request $q ) {
		$m = nlf_guard( $q, 'post' );
		if ( is_wp_error( $m ) ) { return $m; }
		$kind  = sanitize_key( (string) $q->get_param( 'kind' ) );
		$cat   = sanitize_key( (string) $q->get_param( 'cat' ) );
		$title = nlf_text_norm( (string) $q->get_param( 'title' ), true );
		$body  = nlf_text_norm( (string) $q->get_param( 'body' ) );
		$city  = mb_substr( nlf_text_norm( (string) $q->get_param( 'city' ), true ), 0, 40 );
		$pro   = (int) $q->get_param( 'pro_id' );
		if ( ! isset( nlf_kinds()[ $kind ] ) ) { return nlf_err( 'בחרו מה תרצו לכתוב.' ); }
		if ( ! nlf_cat_ok( $cat ) ) { return nlf_err( 'בחרו נושא.' ); }
		$e = nlf_title_error( $title );
		if ( '' === $e ) { $e = nlf_body_error( $body, false ); }
		if ( '' !== $e ) { return nlf_err( $e ); }
		// owner correction 12.11.2026: a discussion is addressed only to a professional who joined (a linked member); refused otherwise
		if ( $pro > 0 ) {
			if ( 'nadlan_professional' !== get_post_type( $pro ) || 'publish' !== get_post_status( $pro ) || nlf_pro_removed( $pro ) || ! nlf_pro_member( $pro ) ) {
				return nlf_err( 'אפשר לפנות ישירות רק לבעל מקצוע שהצטרף לפורום. פרסמו את הבקשה לכל הפורום.' );
			}
			if ( $pro === (int) $m['pro_id'] ) { return nlf_err( 'אי אפשר לפנות אל עצמכם.' ); }
		}
		$e = nlf_post_limits( $m, true, $title . "\n" . $body . "\n" . $city );
		if ( '' !== $e ) { return nlf_err( $e ); }
		global $wpdb;
		$status = nlf_first_status( $m['approved_posts'], $title . "\n" . $body, '0' !== (string) get_option( 'nadlan_forum_autoapprove', '1' ) );
		$now    = nlf_now_sql();
		$row    = array( 'cat' => $cat, 'kind' => $kind, 'title' => $title, 'body' => $body, 'member_id' => (int) $m['id'],
			'pro_id' => $pro > 0 ? $pro : null, 'city' => $city, 'status' => $status, 'body_hash' => nlf_dup_key( $title . "\n" . $body . "\n" . $city ),
			'ip_hash' => nlf_ip_hash(), 'created_at' => $now, 'last_at' => $now );
		if ( 'seek' === $kind ) { // the data for the open-requests board that comes next
			$row['need_profession'] = $cat;
			$row['need_city']       = '' !== $city ? $city : null;
			$row['status_seek']     = 'open';
		}
		$wpdb->insert( nlf_t( 'topics' ), $row );
		$id = (int) $wpdb->insert_id;
		if ( $id <= 0 ) { return nlf_err( 'משהו השתבש. נסו שוב.' ); }
		nlf_write_counted( $m ); // counts this write in the hour of the IP and of the member
		nlf_follow( (int) $m['id'], $id, true ); // the author follows their own discussion (one click to stop, in every mail)
		if ( 'live' === $status ) { nlf_on_topic_live( $id ); } else { nlf_mail_admin_pending( 'topic', $id ); }
		return nlf_ok( array( 'id' => $id, 'url' => home_url( '/forum/' . $id . '/' ), 'status' => $status,
			'message' => 'live' === $status ? 'ההודעה פורסמה.' : 'ההודעה תעלה אחרי בדיקה קצרה.' ) );
	} );

	// reply
	$r( 'reply', 'POST', function ( WP_REST_Request $q ) {
		$m = nlf_guard( $q, 'post' );
		if ( is_wp_error( $m ) ) { return $m; }
		$t = nlf_topic( (int) $q->get_param( 'topic_id' ) );
		if ( ! $t || 'live' !== $t['status'] ) { return nlf_err( 'הדיון לא נמצא.' ); }
		$body = nlf_text_norm( (string) $q->get_param( 'body' ) );
		$e    = nlf_body_error( $body, true );
		if ( '' !== $e ) { return nlf_err( $e ); }
		$quote = (int) $q->get_param( 'quote_id' );
		if ( $quote > 0 ) {
			$qr = nlf_reply( $quote );
			if ( ! $qr || 'live' !== $qr['status'] || (int) $qr['topic_id'] !== (int) $t['id'] ) { $quote = 0; }
		}
		$e = nlf_post_limits( $m, false, $body );
		if ( '' !== $e ) { return nlf_err( $e ); }
		global $wpdb;
		$status = nlf_first_status( $m['approved_posts'], $body, '0' !== (string) get_option( 'nadlan_forum_autoapprove', '1' ) );
		$wpdb->insert( nlf_t( 'replies' ), array( 'topic_id' => (int) $t['id'], 'member_id' => (int) $m['id'], 'body' => $body, 'quote_id' => $quote > 0 ? $quote : null,
			'status' => $status, 'body_hash' => nlf_dup_key( $body ), 'ip_hash' => nlf_ip_hash(), 'created_at' => nlf_now_sql() ) );
		$id = (int) $wpdb->insert_id;
		if ( $id <= 0 ) { return nlf_err( 'משהו השתבש. נסו שוב.' ); }
		nlf_write_counted( $m );
		if ( 'live' === $status ) { nlf_on_reply_live( $id ); } else { nlf_mail_admin_pending( 'reply', $id ); }
		$au = nlf_author( $m );
		return nlf_ok( array( 'id' => $id, 'status' => $status, 'author' => $au['name'] . ( '' !== $au['label'] ? ' · ' . $au['label'] : '' ),
			'message' => 'live' === $status ? 'התשובה פורסמה.' : 'ההודעה תעלה אחרי בדיקה קצרה.' ) );
	} );

	// thanks: one positive reaction, a toggle; no negative reaction exists
	$r( 'thank', 'POST', function ( WP_REST_Request $q ) {
		$m = nlf_guard( $q, 'light' );
		if ( is_wp_error( $m ) ) { return $m; }
		$type = 'reply' === (string) $q->get_param( 'type' ) ? 'reply' : 'topic';
		$id   = (int) $q->get_param( 'id' );
		$row  = 'topic' === $type ? nlf_topic( $id ) : nlf_reply( $id );
		if ( ! $row || 'live' !== $row['status'] ) { return nlf_err( 'ההודעה לא נמצאה.' ); }
		if ( (int) $row['member_id'] === (int) $m['id'] ) { return nlf_err( 'אי אפשר להודות לעצמכם.' ); }
		global $wpdb;
		$tt  = nlf_t( 'thanks' );
		$has = (int) $wpdb->get_var( $wpdb->prepare( "SELECT id FROM $tt WHERE member_id = %d AND target_type = %s AND target_id = %d", (int) $m['id'], $type, $id ) );
		if ( $has ) { $wpdb->delete( $tt, array( 'id' => $has ) ); } else { $wpdb->insert( $tt, array( 'member_id' => (int) $m['id'], 'target_type' => $type, 'target_id' => $id ) ); }
		$n = (int) $wpdb->get_var( $wpdb->prepare( "SELECT COUNT(*) FROM $tt WHERE target_type = %s AND target_id = %d", $type, $id ) );
		$wpdb->update( nlf_t( 'topic' === $type ? 'topics' : 'replies' ), array( 'thanks_count' => $n ), array( 'id' => $id ) );
		return nlf_ok( array( 'on' => $has ? 0 : 1, 'count' => $n ) );
	} );

	// the reply that helped (the discussion's author only; a second press clears it)
	$r( 'solve', 'POST', function ( WP_REST_Request $q ) {
		$m = nlf_guard( $q, 'light' );
		if ( is_wp_error( $m ) ) { return $m; }
		$t  = nlf_topic( (int) $q->get_param( 'topic_id' ) );
		$rp = nlf_reply( (int) $q->get_param( 'reply_id' ) );
		if ( ! $t || (int) $t['member_id'] !== (int) $m['id'] ) { return nlf_err( 'רק מי שפתח את הדיון יכול לסמן את התשובה שעזרה.' ); }
		if ( ! $rp || 'live' !== $rp['status'] || (int) $rp['topic_id'] !== (int) $t['id'] ) { return nlf_err( 'התשובה לא נמצאה.' ); }
		$new = (int) $t['solved_reply_id'] === (int) $rp['id'] ? null : (int) $rp['id'];
		global $wpdb;
		$wpdb->update( nlf_t( 'topics' ), array( 'solved_reply_id' => $new ), array( 'id' => (int) $t['id'] ) );
		return nlf_ok( array( 'solved' => $new ? (int) $new : 0 ) );
	} );

	$r( 'follow', 'POST', function ( WP_REST_Request $q ) {
		$m = nlf_guard( $q, 'light' );
		if ( is_wp_error( $m ) ) { return $m; }
		$t = nlf_topic( (int) $q->get_param( 'topic_id' ) );
		if ( ! nlf_topic_visible( $t, $m ) ) { return nlf_err( 'הדיון לא נמצא.' ); }
		$on = '1' === (string) $q->get_param( 'on' );
		nlf_follow( (int) $m['id'], (int) $t['id'], $on );
		return nlf_ok( array( 'on' => $on ? 1 : 0, 'message' => $on ? 'תקבלו מייל על כל תשובה חדשה.' : 'המעקב הופסק.' ) );
	} );

	// report: 3 different members hide an item until review
	$r( 'report', 'POST', function ( WP_REST_Request $q ) {
		$m = nlf_guard( $q, 'post' );
		if ( is_wp_error( $m ) ) { return $m; }
		$type   = 'reply' === (string) $q->get_param( 'type' ) ? 'reply' : 'topic';
		$id     = (int) $q->get_param( 'id' );
		$reason = sanitize_key( (string) $q->get_param( 'reason' ) );
		if ( ! isset( nlf_report_reasons()[ $reason ] ) ) { return nlf_err( 'בחרו סיבה.' ); }
		$row = 'topic' === $type ? nlf_topic( $id ) : nlf_reply( $id );
		if ( ! $row || 'live' !== $row['status'] ) { return nlf_err( 'ההודעה לא נמצאה.' ); }
		global $wpdb;
		$ft = nlf_t( 'flags' );
		$wpdb->query( $wpdb->prepare( "INSERT IGNORE INTO $ft (target_type, target_id, member_id, ip_hash, reason, created_at) VALUES (%s, %d, %d, %s, %s, %s)",
			$type, $id, (int) $m['id'], nlf_ip_hash(), $reason, nlf_now_sql() ) );
		nlf_write_counted( $m );
		$n = (int) $wpdb->get_var( $wpdb->prepare( "SELECT COUNT(DISTINCT member_id) FROM $ft WHERE target_type = %s AND target_id = %d", $type, $id ) );
		if ( $n >= 3 ) {
			nlf_moderate( $type, $id, 'hidden' );
			nlf_mail( nlf_admin_to(), '[פורום] הודעה הוסתרה אחרי 3 דיווחים',
				"שלושה משתתפים דיווחו על הודעה והיא הוסתרה עד הבדיקה שלכם.\n\n" . nlf_excerpt( $row['body'] ? $row['body'] : ( $row['title'] ?? '' ), 800 )
				. "\n\nלבדיקה: " . admin_url( 'admin.php?page=nadlan-forum&tab=hidden' ) . "\n" );
		}
		return nlf_ok( array( 'message' => 'תודה. הדיווח התקבל ונבדוק אותו.' ) );
	} );

	// similar discussions while typing a title (live titles, at most 3)
	$r( 'similar', 'GET', function ( WP_REST_Request $q ) {
		if ( ! nlf_gate_open() ) { return nlf_err( 'הדף לא נמצא.', 'nlf_closed' ); }
		if ( ! nlf_db_ready() || ! nlf_rl( 'similar', 120, HOUR_IN_SECONDS ) ) { return nlf_ok( array( 'items' => array() ) ); }
		$words = array_slice( array_values( array_filter( preg_split( '/[^\p{L}\p{N}"\']+/u', nlf_text_norm( (string) $q->get_param( 'q' ), true ) ), function ( $w ) {
			return nlf_len( $w ) >= 3;
		} ) ), 0, 5 );
		if ( ! $words ) { return nlf_ok( array( 'items' => array() ) ); }
		global $wpdb;
		$parts = array(); $args = array();
		foreach ( $words as $w ) { $parts[] = '(title LIKE %s)'; $args[] = '%' . $wpdb->esc_like( $w ) . '%'; }
		$score = implode( ' + ', $parts );
		$sql   = 'SELECT id, title, reply_count, (' . $score . ') AS score FROM ' . nlf_t( 'topics' ) . " WHERE status = 'live' HAVING score > 0 ORDER BY score DESC, last_at DESC LIMIT 3";
		$rows  = $wpdb->get_results( $wpdb->prepare( $sql, $args ), ARRAY_A ); // phpcs:ignore -- placeholders built above
		$items = array();
		foreach ( (array) $rows as $row ) {
			$items[] = array( 'title' => $row['title'], 'url' => home_url( '/forum/' . (int) $row['id'] . '/' ), 'replies' => nlf_count_words( $row['reply_count'], 'תשובה אחת', 'תשובות' ) );
		}
		return nlf_ok( array( 'items' => $items ) );
	} );

	// the view counter: once per browser session per discussion (a session cookie holds the ids already counted)
	$r( 'view', 'POST', function ( WP_REST_Request $q ) {
		$g = nlf_guard( $q, 'view' );
		if ( is_wp_error( $g ) ) { return $g; }
		$id   = (int) $q->get_param( 'topic_id' );
		$seen = isset( $_COOKIE['nlf_seen'] ) ? array_filter( array_map( 'intval', explode( '-', (string) $_COOKIE['nlf_seen'] ) ) ) : array();
		$ua   = isset( $_SERVER['HTTP_USER_AGENT'] ) ? (string) $_SERVER['HTTP_USER_AGENT'] : ''; // phpcs:ignore
		if ( $id > 0 && ! in_array( $id, $seen, true ) && ! preg_match( '/bot|crawl|spider|slurp|preview|headless/i', $ua ) ) {
			global $wpdb;
			$wpdb->query( $wpdb->prepare( 'UPDATE ' . nlf_t( 'topics' ) . " SET view_count = view_count + 1 WHERE id = %d AND status = 'live'", $id ) );
			$seen[] = $id;
			nlf_cookie( 'nlf_seen', implode( '-', array_slice( $seen, -60 ) ), 0, true ); // 0 = ends with the browser session
		}
		$r = new WP_REST_Response( array( 'ok' => 1 ), 200 );
		$r->header( 'Cache-Control', 'no-store' );
		return $r;
	} );

	// the professional's own switches: profile shown, phone shown, removal and its undo
	$r( 'owner', 'POST', function ( WP_REST_Request $q ) {
		$m = nlf_guard( $q, 'light' );
		if ( is_wp_error( $m ) ) { return $m; }
		$pro = (int) $m['pro_id'];
		if ( $pro <= 0 || 'nadlan_professional' !== get_post_type( $pro ) ) { return nlf_err( 'הפעולה הזאת שמורה לבעל הכרטיס.' ); }
		$do  = sanitize_key( (string) $q->get_param( 'do' ) );
		$val = '1' === (string) $q->get_param( 'value' );
		global $wpdb;
		$msg = '';
		if ( 'visible' === $do ) {
			if ( $val ) { nlf_owner_show( $pro ); $msg = nlf_owner_shown_msg( $pro ); }
			else { nlf_owner_hide( $pro, 'nl_forum_hidden_by_owner', '1' ); $msg = 'הפרופיל הוסתר. אפשר להחזיר בכל רגע.'; }
		} elseif ( 'phone' === $do ) {
			$wpdb->update( nlf_t( 'members' ), array( 'show_phone' => $val ? 1 : 0 ), array( 'id' => (int) $m['id'] ) );
			nlf_me( true );
			$msg = $val ? 'הטלפון שלכם מוצג בפורום.' : 'הטלפון לא מוצג. פונים אליכם רק דרך הפורום.';
		} elseif ( 'remove' === $do ) {
			nlf_owner_hide( $pro, 'nl_removed_by_owner', current_time( 'Y-m-d' ) );
			$msg = 'הפרופיל הוסר.';
		} elseif ( 'restore' === $do ) {
			nlf_owner_show( $pro );
			$msg = nlf_owner_shown_msg( $pro );
		} else {
			return nlf_err( 'פעולה לא מוכרת.' );
		}
		return nlf_ok( array( 'state' => nlf_owner_state( $pro ), 'message' => $msg ) );
	} );

	// "זה הכרטיס שלכם?" when the email does not match the card: an ownership or removal request for the admin screen
	$r( 'request', 'POST', function ( WP_REST_Request $q ) {
		$m = nlf_guard( $q, 'post' );
		if ( is_wp_error( $m ) ) { return $m; }
		$pro  = (int) $q->get_param( 'pro_id' );
		$kind = 'removal' === (string) $q->get_param( 'kind' ) ? 'removal' : 'ownership';
		$body = mb_substr( nlf_text_norm( (string) $q->get_param( 'body' ) ), 0, 1000 );
		$ph   = preg_replace( '/[^\d+\-\s]/', '', (string) $q->get_param( 'phone' ) );
		$ph   = strlen( preg_replace( '/\D/', '', $ph ) ) >= 9 ? mb_substr( trim( $ph ), 0, 30 ) : '';
		if ( 'nadlan_professional' !== get_post_type( $pro ) ) { return nlf_err( 'הכרטיס לא נמצא.' ); }
		if ( nlf_len( $body ) < 5 ) { return nlf_err( 'כתבו במשפט מה תרצו שנעשה.' ); }
		if ( ! nlf_rl( 'req', 3, DAY_IN_SECONDS, 'm' . (int) $m['id'] ) || ! nlf_rl( 'req_ip', 10, DAY_IN_SECONDS ) ) { return nlf_err( 'כבר שלחתם בקשות היום. נחזור אליכם.' ); }
		global $wpdb;
		$wpdb->insert( nlf_t( 'requests' ), array( 'kind' => $kind, 'pro_id' => $pro, 'member_id' => (int) $m['id'], 'contact' => (string) $m['contact'],
			'phone' => $ph, 'body' => $body, 'status' => 'pending', 'created_at' => nlf_now_sql() ) );
		nlf_write_counted( $m );
		nlf_mail( nlf_admin_to(), '[פורום] בקשה על כרטיס: ' . get_the_title( $pro ),
			( 'removal' === $kind ? 'בקשת הסרה' : 'בקשת בעלות' ) . ' על הכרטיס "' . get_the_title( $pro ) . "\"\n"
			. 'מאת: ' . $m['display_name'] . ' (' . $m['contact'] . ')' . ( '' !== $ph ? ', טלפון ' . $ph : '' ) . "\n\n" . $body . "\n\n"
			. 'הכרטיס בניהול האתר: ' . admin_url( 'post.php?post=' . $pro . '&action=edit' ) . "\n"
			. 'כל הבקשות: ' . admin_url( 'admin.php?page=nadlan-forum&tab=requests' ) . "\n" );
		return nlf_ok( array( 'message' => 'הבקשה נשלחה. נטפל בה היום.' ) );
	} );
} );

/* =========================================================================================================
 * 10. Addresses: /forum/ and /forum/<number>/
 * ======================================================================================================= */

function nlf_rules_state() { $s = get_option( 'nadlan_forum_rules', array() ); return is_array( $s ) ? $s : array(); }

/** a published page or post already owns the address /forum/ (then the module adds no rule and never hides it) */
function nlf_slug_taken() {
	$p = get_page_by_path( 'forum', OBJECT, array( 'page', 'post' ) );
	return $p && 'publish' === get_post_status( $p );
}

add_action( 'init', function () {
	$st = nlf_rules_state();
	if ( ! empty( $st['clash'] ) ) { return; }
	add_rewrite_rule( '^forum/?$', 'index.php?nlf_view=home', 'top' );
	add_rewrite_rule( '^forum/([0-9]+)/?$', 'index.php?nlf_view=topic&nlf_id=$matches[1]', 'top' );
} );

/* The rules are written ONCE per NADLAN_FORUM_RULES version by the module itself (no manual step). On wp_loaded, i.e. after
   every init callback of every plugin registered its own rules, so a flush here drops nobody's rules. The option is stored
   before the flush, so a failed or repeated flush never loops. */
add_action( 'wp_loaded', function () {
	$st = nlf_rules_state();
	if ( 'none' === nlf_rules_step( $st['v'] ?? '', NADLAN_FORUM_RULES, false ) ) { return; }
	$taken = nlf_slug_taken();
	update_option( 'nadlan_forum_rules', array( 'v' => NADLAN_FORUM_RULES, 'clash' => $taken ? 1 : 0, 'at' => time() ), true );
	if ( 'flush' === nlf_rules_step( $st['v'] ?? '', NADLAN_FORUM_RULES, $taken ) ) { flush_rewrite_rules( false ); }
}, 20 );

add_filter( 'query_vars', function ( $v ) { $v[] = 'nlf_view'; $v[] = 'nlf_id'; return $v; } );

/** true when the stored rewrite rules do not have the forum (the module flushes once by itself, see above) */
function nadlan_forum_flush_needed() {
	$rules = get_option( 'rewrite_rules' );
	return ! is_array( $rules ) || ! isset( $rules['^forum/?$'] ) || ! isset( $rules['^forum/([0-9]+)/?$'] );
}

function nlf_view() { return (string) get_query_var( 'nlf_view' ); }

/* our addresses are not the blog home: no posts are fetched for them */
add_action( 'parse_query', function ( $q ) {
	if ( $q->is_main_query() && '' !== (string) $q->get( 'nlf_view' ) ) { $q->is_home = false; }
} );
add_filter( 'posts_pre_query', function ( $posts, $q ) {
	return ( $q->is_main_query() && '' !== (string) $q->get( 'nlf_view' ) ) ? array() : $posts;
}, 10, 2 );

/* no canonical redirect on our addresses (no redirects in this module, ever) */
add_filter( 'redirect_canonical', function ( $url ) { return '' !== nlf_view() ? false : $url; } );

/* the status of a forum address: closed gate or a hidden discussion = a normal 404; else 200 and the page renders */
add_filter( 'pre_handle_404', function ( $pre, $wp_query ) {
	$view = (string) $wp_query->get( 'nlf_view' );
	if ( '' === $view ) { return $pre; }
	nlf_nocache();
	$ok = nlf_gate_open();
	if ( $ok ) {
		nlf_install();
		if ( 'topic' === $view ) {
			$t  = nlf_topic( (int) $wp_query->get( 'nlf_id' ) );
			$ok = nlf_topic_visible( $t, nlf_me() );
			if ( $ok ) { $GLOBALS['nlf_topic'] = $t; }
		}
	}
	if ( ! $ok ) { // nlf_view stays set, so redirect_canonical stays off: WordPress never guesses a "closest" page and redirects
		$wp_query->set_404();
		status_header( 404 );
		return true;
	}
	$GLOBALS['nlf_render'] = $view;
	status_header( 200 );
	return true;
}, 10, 2 );

function nlf_rendering() { return isset( $GLOBALS['nlf_render'] ) ? (string) $GLOBALS['nlf_render'] : ''; }

/* =========================================================================================================
 * 11. Search engines: title, description, canonical, structured data (passive only)
 * ======================================================================================================= */

function nlf_home_title() { $t = trim( (string) get_option( 'nadlan_forum_home_title', '' ) ); return '' !== $t ? $t : 'פורום נדל"ן: שאלות ותשובות עם בעלי מקצוע'; }

function nlf_home_h1() { $t = trim( (string) get_option( 'nadlan_forum_home_h1', '' ) ); return '' !== $t ? $t : 'פורום נדל"ן'; }

function nlf_filter_args() {
	$c  = isset( $_GET['c'] ) ? sanitize_key( wp_unslash( $_GET['c'] ) ) : ''; // phpcs:ignore -- a list filter
	$v  = isset( $_GET['v'] ) ? sanitize_key( wp_unslash( $_GET['v'] ) ) : ''; // phpcs:ignore
	$pg = isset( $_GET['pg'] ) ? max( 1, (int) $_GET['pg'] ) : 1; // phpcs:ignore
	return array( 'c' => nlf_cat_ok( $c ) ? $c : '', 'v' => in_array( $v, array( 'new', 'requests', 'hot', 'open', 'mine' ), true ) ? $v : '', 'pg' => $pg );
}

function nlf_doc_title() {
	$v = nlf_rendering();
	if ( 'topic' === $v && ! empty( $GLOBALS['nlf_topic'] ) ) { return $GLOBALS['nlf_topic']['title'] . ' | פורום נדל"ן'; }
	if ( 'home' === $v ) {
		$a = nlf_filter_args();
		$t = nlf_home_title();
		if ( '' !== $a['c'] ) { $t = nlf_categories()[ $a['c'] ][0] . ' | ' . $t; }
		return $a['pg'] > 1 ? $t . ' | עמוד ' . $a['pg'] : $t;
	}
	return '';
}

function nlf_doc_desc() {
	if ( 'topic' === nlf_rendering() && ! empty( $GLOBALS['nlf_topic'] ) ) {
		$t = $GLOBALS['nlf_topic'];
		return nlf_excerpt( '' !== trim( $t['body'] ) ? $t['body'] : $t['title'], 150 );
	}
	if ( 'home' === nlf_rendering() ) { return 'שאלות ותשובות על קנייה, שיפוץ, משכנתא, שמאות ודיני מקרקעין, עם בעלי מקצוע שעונים בעצמם.'; }
	return '';
}

/** the canonical: a discussion is its own address; the home is /forum/ for filtered views and its own page address otherwise */
function nlf_canonical() {
	if ( 'topic' === nlf_rendering() && ! empty( $GLOBALS['nlf_topic'] ) ) { return home_url( '/forum/' . (int) $GLOBALS['nlf_topic']['id'] . '/' ); }
	if ( 'home' === nlf_rendering() ) {
		$a = nlf_filter_args();
		$last = isset( $GLOBALS['nlf_pages'] ) ? (int) $GLOBALS['nlf_pages'] : 0;
		if ( '' === $a['c'] && '' === $a['v'] && $a['pg'] > 1 && $a['pg'] <= $last ) { return add_query_arg( 'pg', $a['pg'], home_url( '/forum/' ) ); }
		return home_url( '/forum/' );
	}
	return '';
}

add_filter( 'pre_get_document_title', function ( $t ) { $x = nlf_doc_title(); return '' !== $x ? $x : $t; }, 99 );
add_filter( 'wpseo_title', function ( $t ) { $x = nlf_doc_title(); return '' !== $x ? $x : $t; }, 99 );
add_filter( 'wpseo_opengraph_title', function ( $t ) { $x = nlf_doc_title(); return '' !== $x ? $x : $t; }, 99 );
/* description and canonical: the forum prints its own in wp_head (Yoast may not know a virtual address); Yoast's own are
   switched off on forum pages only, so each appears exactly once */
add_filter( 'wpseo_metadesc', function ( $d ) { return '' !== nlf_rendering() ? false : $d; }, PHP_INT_MAX );
add_filter( 'wpseo_opengraph_desc', function ( $d ) { $x = nlf_doc_desc(); return '' !== $x ? $x : $d; }, 99 );
add_filter( 'wpseo_canonical', function ( $c ) { return '' !== nlf_rendering() ? false : $c; }, PHP_INT_MAX );
add_filter( 'wpseo_opengraph_url', function ( $c ) { $x = nlf_canonical(); return '' !== $x ? $x : $c; }, PHP_INT_MAX );
/* Yoast would describe our address as the site's home page in its graph; the forum prints its own structured data instead */
add_filter( 'wpseo_json_ld_output', function ( $d ) { return '' !== nlf_rendering() ? false : $d; }, PHP_INT_MAX );

add_action( 'wp_head', function () {
	if ( '' === nlf_rendering() ) { return; }
	// always the forum's own description and canonical (Yoast's are switched off on forum pages above)
	echo '<meta name="description" content="' . esc_attr( nlf_doc_desc() ) . '">' . "\n";
	echo '<link rel="canonical" href="' . esc_url( nlf_canonical() ) . '">' . "\n";
	if ( 'topic' === nlf_rendering() && ! empty( $GLOBALS['nlf_topic'] ) && 'live' === $GLOBALS['nlf_topic']['status'] ) {
		$ld = nlf_jsonld( $GLOBALS['nlf_topic'] );
		if ( $ld ) { echo '<script type="application/ld+json">' . nlf_json_script( $ld ) . "</script>\n"; } // phpcs:ignore -- < and > are < / >
	}
}, 2 );

/* the canonical of WordPress itself is for singular pages only; ours is printed above or by Yoast */

function nlf_iso( $sql ) { return gmdate( 'c', nlf_ts( $sql ) ); }

/** DiscussionForumPosting, or QAPage when a question has the reply that helped */
function nlf_jsonld( $t ) {
	global $wpdb;
	$replies = $wpdb->get_results( $wpdb->prepare( 'SELECT * FROM ' . nlf_t( 'replies' ) . " WHERE topic_id = %d AND status = 'live' ORDER BY id ASC LIMIT 100", (int) $t['id'] ), ARRAY_A );
	$ids     = array( (int) $t['member_id'] );
	foreach ( (array) $replies as $r ) { $ids[] = (int) $r['member_id']; }
	$mem    = nlf_members( $ids );
	$person = function ( $mid ) use ( $mem ) {
		$a = nlf_author( $mem[ $mid ] ?? null );
		$p = array( '@type' => 'Person', 'name' => $a['name'] );
		if ( '' !== $a['url'] ) { $p['url'] = $a['url']; }
		return $p;
	};
	$url  = home_url( '/forum/' . (int) $t['id'] . '/' );
	$text = '' !== trim( $t['body'] ) ? $t['body'] : $t['title'];
	$solved = null;
	foreach ( (array) $replies as $r ) { if ( (int) $r['id'] === (int) $t['solved_reply_id'] ) { $solved = $r; } }
	if ( 'question' === $t['kind'] && $solved ) {
		$ans = function ( $r ) use ( $person, $url ) {
			return array( '@type' => 'Answer', 'text' => $r['body'], 'datePublished' => nlf_iso( $r['created_at'] ), 'author' => $person( (int) $r['member_id'] ),
				'url' => $url . '#r' . (int) $r['id'], 'upvoteCount' => (int) $r['thanks_count'] );
		};
		$others = array();
		foreach ( (array) $replies as $r ) { if ( (int) $r['id'] !== (int) $solved['id'] ) { $others[] = $ans( $r ); } }
		$q = array( '@type' => 'Question', 'name' => $t['title'], 'text' => $text, 'datePublished' => nlf_iso( $t['created_at'] ), 'author' => $person( (int) $t['member_id'] ),
			'answerCount' => count( (array) $replies ), 'acceptedAnswer' => $ans( $solved ) );
		if ( $others ) { $q['suggestedAnswer'] = $others; }
		return array( '@context' => 'https://schema.org', '@type' => 'QAPage', 'mainEntity' => $q );
	}
	$ld = array( '@context' => 'https://schema.org', '@type' => 'DiscussionForumPosting', 'headline' => $t['title'], 'text' => $text, 'url' => $url,
		'datePublished' => nlf_iso( $t['created_at'] ), 'author' => $person( (int) $t['member_id'] ),
		'interactionStatistic' => array( '@type' => 'InteractionCounter', 'interactionType' => 'https://schema.org/CommentAction', 'userInteractionCount' => count( (array) $replies ) ) );
	$cm = array();
	foreach ( (array) $replies as $r ) {
		$cm[] = array( '@type' => 'Comment', 'text' => $r['body'], 'datePublished' => nlf_iso( $r['created_at'] ), 'author' => $person( (int) $r['member_id'] ), 'url' => $url . '#r' . (int) $r['id'] );
	}
	if ( $cm ) { $ld['comment'] = $cm; }
	return $ld;
}

/* =========================================================================================================
 * 12. Assets (forum surfaces only) and the two other files
 * ======================================================================================================= */

function nlf_ver() { return defined( 'NADLAN_CONFIG_VERSION' ) ? NADLAN_CONFIG_VERSION : NADLAN_FORUM_VERSION; }

/** this request shows a forum surface (a forum page, a one-click page, or a professional's page with the gate open) */
function nlf_surface() {
	if ( '' !== nlf_rendering() || ! empty( $GLOBALS['nlf_act_page'] ) ) { return true; }
	return is_singular( 'nadlan_professional' ) && nlf_gate_open() && ! nlf_pro_removed( (int) get_queried_object_id() );
}

add_action( 'wp_enqueue_scripts', function () {
	if ( ! nlf_surface() ) { return; }
	nlf_nocache();
	$base = plugins_url( 'assets/proforum/', dirname( __FILE__ ) );
	wp_enqueue_style( 'nlf-fonts', 'https://fonts.googleapis.com/css2?family=Assistant:wght@400;600;700&family=Rubik:wght@500;700;800&display=swap', array(), null );
	wp_enqueue_style( 'nlf', $base . 'forum.css', array(), nlf_ver() );
	if ( '' === nlf_rendering() && ! empty( $GLOBALS['nlf_act_page'] ) ) { return; } // a one-click page needs no script
	wp_enqueue_script( 'nlf', $base . 'forum.js', array(), nlf_ver(), true );
	wp_add_inline_script( 'nlf', 'window.NLF=' . nlf_json_script( array(
		'rest'    => esc_url_raw( rest_url( 'nadlan/v1/forum/' ) ),
		'wpnonce' => is_user_logged_in() ? wp_create_nonce( 'wp_rest' ) : '',
		'home'    => home_url( '/forum/' ),
	) ) . ';', 'before' );
}, 30 );

add_filter( 'wp_resource_hints', function ( $urls, $rel ) {
	if ( 'preconnect' === $rel && function_exists( 'nlf_surface' ) && did_action( 'wp' ) && nlf_surface() ) {
		$urls[] = 'https://fonts.googleapis.com';
		$urls[] = array( 'href' => 'https://fonts.gstatic.com', 'crossorigin' );
	}
	return $urls;
}, 10, 2 );

if ( file_exists( __DIR__ . '/pro-forum-trades.php' ) ) { require_once __DIR__ . '/pro-forum-trades.php'; }
// 1.72.668: one-tap video calls between two people already talking in a discussion or request (LiveKit, docs CALL-NOTES.md)
if ( file_exists( __DIR__ . '/pro-forum-call.php' ) ) { require_once __DIR__ . '/pro-forum-call.php'; }
require_once __DIR__ . '/pro-forum-render.php';
if ( is_admin() ) { require_once __DIR__ . '/pro-forum-admin.php'; }
if ( file_exists( __DIR__ . '/pro-forum-social.php' ) ) { require_once __DIR__ . '/pro-forum-social.php'; }
if ( file_exists( __DIR__ . '/pro-forum-card.php' ) ) { require_once __DIR__ . '/pro-forum-card.php'; }
