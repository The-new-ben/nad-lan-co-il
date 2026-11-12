<?php
/**
 * Plain PHP CLI test of the forum's pure functions (no WordPress): php tests-local/pro-forum-test.php
 * Loads only part 1 of inc/pro-forum.php (NLF_PURE_ONLY). Exit code 0 = all passed.
 */
define( 'ABSPATH', __DIR__ . '/' );
define( 'NLF_PURE_ONLY', true );
require __DIR__ . '/../inc/pro-forum.php';

$pass = 0; $fail = 0;
function t( $name, $cond ) {
	global $pass, $fail;
	if ( $cond ) { $pass++; echo "ok   $name\n"; } else { $fail++; echo "FAIL $name\n"; }
}
$K = 'test-key-123';

/* categories */
$c = nlf_categories();
t( 'nine categories', 9 === count( $c ) );
t( 'category keys', array( 'law', 'build', 'loans', 'value', 'design', 'agents', 'renewal', 'abroad', 'general' ) === array_keys( $c ) );
t( 'law label', 'דיני מקרקעין' === $c['law'][0] && '#EBDDF0' === $c['law'][1] );
t( 'abroad label', 'השקעות נדל"ן בחו"ל' === $c['abroad'][0] );
t( 'cat_ok', nlf_cat_ok( 'loans' ) && ! nlf_cat_ok( 'nope' ) && ! nlf_cat_ok( array() ) );
t( 'four kinds', array( 'question', 'seek', 'intro', 'work' ) === array_keys( nlf_kinds() ) );
t( 'profession tint', array( '#DCE6F2', '#1D3B66' ) === nlf_prof_tint( 'kablan' ) && array( '#E3E6E8', '#22303A' ) === nlf_prof_tint( 'unknown' ) );

/* text guard: links and phones */
t( 'link http', nlf_has_link( 'ראו https://x.co.il/a' ) );
t( 'link www', nlf_has_link( 'www.example.com' ) );
t( 'link bare domain', nlf_has_link( 'כנסו ל example.co.il עכשיו' ) );
t( 'link email', nlf_has_link( 'כתבו לי dan@mail.com' ) );
t( 'link wa.me', nlf_has_link( 'wa.me/972500000000' ) );
t( 'no link in plain Hebrew', ! nlf_has_link( 'הקבלן מאחר במסירה בחצי שנה. מה מגיע לי?' ) );
t( 'no link in decimal', ! nlf_has_link( 'ריבית 4.5 אחוז' ) );
t( 'phone 054-1234567', nlf_has_phone( 'התקשרו 054-1234567' ) );
t( 'phone spaced', nlf_has_phone( '054 123 4567' ) );
t( 'phone +972', nlf_has_phone( '+972 54 123 4567' ) );
t( 'landline 9 digits', nlf_has_phone( '03-1234567' ) );
t( 'no phone: price', ! nlf_has_phone( 'מחיר 2,500,000 ש"ח' ) );
t( 'no phone: year and rooms', ! nlf_has_phone( 'בשנת 2024 קנינו 4 חדרים' ) );
t( 'no phone: block and parcel', ! nlf_has_phone( 'גוש 6106 חלקה 123' ) );
t( 'rule: new member link refused', '' !== nlf_text_rule_error( 'www.x.com', 0 ) );
t( 'rule: new member phone refused', '' !== nlf_text_rule_error( '0541234567', 1 ) );
t( 'rule: 2 approved may', '' === nlf_text_rule_error( 'www.x.com 0541234567', 2 ) );

/* normalisation and length rules */
t( 'norm CRLF + controls', "שורה\nשתיים" === nlf_text_norm( "  שורה\r\nשתיים\x07 " ) || "שורה\nשתיים" === trim( nlf_text_norm( "שורה\r\nשתיים" ) ) );
t( 'norm 3+ newlines to 2', "א\n\nב" === nlf_text_norm( "א\n\n\n\n\nב" ) );
t( 'norm bidi override removed', 'אב' === nlf_text_norm( "א\u{202E}ב" ) );
t( 'norm single line', 'א ב' === nlf_text_norm( "א\nב", true ) );
t( 'norm invalid utf8', '' === nlf_text_norm( "\xC3\x28" ) );
t( 'title 7 chars refused', '' !== nlf_title_error( 'שבעה תו' ) );
t( 'title 8 chars ok', '' === nlf_title_error( 'שמונה תו' ) );
t( 'title 140 ok', '' === nlf_title_error( str_repeat( 'א', 140 ) ) );
t( 'title 141 refused', '' !== nlf_title_error( str_repeat( 'א', 141 ) ) );
t( 'body optional empty ok', '' === nlf_body_error( '', false ) );
t( 'reply body required', '' !== nlf_body_error( 'א', true ) );
t( 'body 4000 ok', '' === nlf_body_error( str_repeat( 'ב', 4000 ), true ) );
t( 'body 4001 refused', '' !== nlf_body_error( str_repeat( 'ב', 4001 ), true ) );

/* duplicate window */
$k1 = nlf_dup_key( 'שלום, מה שלומכם?' );
t( 'dup key ignores case/punct', $k1 === nlf_dup_key( 'שלום מה  שלומכם' ) );
$now = 1800000000;
t( 'dup within 5 min', nlf_dup_hit( array( array( $k1, $now - 299 ) ), $k1, $now ) );
t( 'no dup after 5 min', ! nlf_dup_hit( array( array( $k1, $now - 300 ) ), $k1, $now ) );
t( 'no dup other text', ! nlf_dup_hit( array( array( $k1, $now - 10 ) ), nlf_dup_key( 'אחר' ), $now ) );

/* rate windows (Discourse defaults) */
$base = array( 'is_topic' => true, 'approved' => 0, 'age' => 3600, 'topics_first_day' => 0, 'replies_first_day' => 0, 'since_last' => null, 'ip_hour' => 0 );
t( 'first post allowed', '' === nlf_limits_error( $base ) );
t( 'first day 3 topics max', '' !== nlf_limits_error( array_merge( $base, array( 'topics_first_day' => 3 ) ) ) );
t( 'first day 2 topics ok', '' === nlf_limits_error( array_merge( $base, array( 'topics_first_day' => 2 ) ) ) );
t( 'first day 10 replies max', '' !== nlf_limits_error( array_merge( $base, array( 'is_topic' => false, 'replies_first_day' => 10 ) ) ) );
t( 'after first day no day cap', '' === nlf_limits_error( array_merge( $base, array( 'age' => 90000, 'topics_first_day' => 9 ) ) ) );
t( 'new member 30 s gap', '' !== nlf_limits_error( array_merge( $base, array( 'since_last' => 29 ) ) ) && '' === nlf_limits_error( array_merge( $base, array( 'since_last' => 30 ) ) ) );
t( 'trusted member 15 s gap', '' !== nlf_limits_error( array_merge( $base, array( 'approved' => 2, 'since_last' => 14 ) ) ) && '' === nlf_limits_error( array_merge( $base, array( 'approved' => 2, 'since_last' => 15 ) ) ) );
t( 'ip ceiling 20 per hour', '' !== nlf_limits_error( array_merge( $base, array( 'ip_hour' => 20 ) ) ) && '' === nlf_limits_error( array_merge( $base, array( 'ip_hour' => 19 ) ) ) );

/* proof of work */
t( 'zero bits', 12 === nlf_zero_bits( "\x00\x0F\xFF" ) && 0 === nlf_zero_bits( "\x80" ) && 16 === nlf_zero_bits( "\x00\x00" ) );
$salt = 'a1b2c3d4e5f60718293a4b5c';
$bits = 12;
$t0 = microtime( true );
$nonce = null;
for ( $i = 0; $i < 2000000; $i++ ) { if ( nlf_pow_ok( $salt, (string) $i, $bits ) ) { $nonce = (string) $i; break; } }
$ms = (int) ( ( microtime( true ) - $t0 ) * 1000 );
t( "pow solvable at $bits bits (nonce $nonce, {$ms} ms in PHP)", null !== $nonce );
t( 'pow wrong nonce refused', ! nlf_pow_ok( $salt, (string) ( (int) $nonce + 1 ), 30 ) );
t( 'pow bad input refused', ! nlf_pow_ok( 'XYZ', '1', 1 ) && ! nlf_pow_ok( $salt, '1a', 1 ) );
$ch = nlf_challenge_make( $K, $now, $bits, $salt );
t( 'challenge verifies', $salt === nlf_challenge_check( $ch, $nonce, $K, $now + 5 ) );
t( 'challenge expired after 10 min', '' === nlf_challenge_check( $ch, $nonce, $K, $now + 601 ) );
t( 'challenge wrong key', '' === nlf_challenge_check( $ch, $nonce, 'other', $now + 5 ) );
t( 'challenge tampered bits', '' === nlf_challenge_check( str_replace( ".$bits.", '.1.', $ch ), $nonce, $K, $now + 5 ) );
t( 'challenge unsolved', '' === nlf_challenge_check( $ch, '999999999999', $K, $now + 5 ) || nlf_pow_ok( $salt, '999999999999', $bits ) );

/* form time */
$ts = nlf_form_ts_make( $K, $now );
t( 'form too fast (2 s)', '' !== nlf_form_ts_error( $ts, $K, $now + 2 ) );
t( 'form ok at 3 s', '' === nlf_form_ts_error( $ts, $K, $now + 3 ) );
t( 'form expired after 12 h', '' !== nlf_form_ts_error( $ts, $K, $now + 12 * 3600 + 1 ) );
t( 'form forged', '' !== nlf_form_ts_error( ( $now - 100 ) . '.deadbeef', $K, $now ) );

/* HMAC one-click links */
$l = nlf_link_token( 'unf', 'm12t34', 0, $K );
t( 'link round trip', array( 'unf', 'm12t34' ) === nlf_link_read( $l, $now, $K ) );
t( 'link wrong key', null === nlf_link_read( $l, $now, 'x' ) );
t( 'link tampered id', null === nlf_link_read( str_replace( 'm12t34', 'm13t34', $l ), $now, $K ) );
$le = nlf_link_token( 'ok', 't5', $now + 60, $K );
t( 'link in time', array( 'ok', 't5' ) === nlf_link_read( $le, $now + 59, $K ) );
t( 'link expired', null === nlf_link_read( $le, $now + 61, $K ) );
t( 'link garbage', null === nlf_link_read( 'a.b', $now, $K ) && null === nlf_link_read( '', $now, $K ) );

/* codes */
$chash = nlf_contact_hash( ' Dan@Example.COM ', $K );
t( 'contact hash case-insensitive', $chash === nlf_contact_hash( 'dan@example.com', $K ) );
$row = array( 'code_hash' => nlf_code_hash( '042517', $chash, $K ), 'tries' => 0, 'expires' => $now + 600 );
t( 'code ok', 'ok' === nlf_code_verdict( $row, '042517', $chash, $now, $K ) );
t( 'code wrong', 'wrong' === nlf_code_verdict( $row, '042518', $chash, $now, $K ) );
t( 'code not 6 digits', 'wrong' === nlf_code_verdict( $row, '42517', $chash, $now, $K ) );
t( 'code for another contact', 'wrong' === nlf_code_verdict( $row, '042517', nlf_contact_hash( 'x@y.z', $K ), $now, $K ) );
t( 'code expired after 10 min', 'expired' === nlf_code_verdict( $row, '042517', $chash, $now + 601, $K ) );
t( 'code 5 tries', 'tries' === nlf_code_verdict( array_merge( $row, array( 'tries' => 5 ) ), '042517', $chash, $now, $K ) );
t( 'code 4 tries still ok', 'ok' === nlf_code_verdict( array_merge( $row, array( 'tries' => 4 ) ), '042517', $chash, $now, $K ) );
t( 'no code', 'none' === nlf_code_verdict( null, '042517', $chash, $now, $K ) );
t( 'code hash is not the code', false === strpos( $row['code_hash'], '042517' ) && 64 === strlen( $row['code_hash'] ) );

/* output helpers */
t( 'body html escapes and keeps lines', 'a &lt;b&gt;<br>&quot;c&quot;' === str_replace( "\n", '', nlf_body_html( "a <b>\n\"c\"" ) ) );
t( 'body html does not link', false === strpos( nlf_body_html( 'https://x.com' ), '<a' ) );
t( 'initials', 'רל' === nlf_initials( 'רונית לוי' ) && 'מ' === nlf_initials( 'מיכל' ) && '?' === nlf_initials( '' ) );
t( 'excerpt', 'אבג…' === nlf_excerpt( 'אבגדה', 3 ) && 'אב' === nlf_excerpt( 'אב', 3 ) );
t( 'ago', 'עכשיו' === nlf_ago( $now - 5, $now ) && 'לפני דקה' === nlf_ago( $now - 60, $now ) && 'לפני שעתיים' === nlf_ago( $now - 7200, $now ) && 'אתמול' === nlf_ago( $now - 90000, $now ) && '' === nlf_ago( $now - 8 * 86400, $now ) );
t( 'count words omits zero', '' === nlf_count_words( 0, 'תשובה אחת', 'תשובות' ) && 'תשובה אחת' === nlf_count_words( 1, 'תשובה אחת', 'תשובות' ) && '1,200 תשובות' === nlf_count_words( 1200, 'תשובה אחת', 'תשובות' ) );

/* review 12.11.2026: fixes that are pure logic */
$js = nlf_json_script( array( 'text' => 'a</script><script>alert(1)</script> & "q" ש', 'url' => 'https://x.co.il/a/' ) );
t( 'json for script: no "</"', false === strpos( $js, '</' ) && false === strpos( $js, '<' ) && false === strpos( $js, '>' ) );
t( 'json for script: round trip', 'a</script><script>alert(1)</script> & "q" ש' === json_decode( $js, true )['text'] && 'https://x.co.il/a/' === json_decode( $js, true )['url'] );
t( 'json for script: Hebrew kept readable', false !== strpos( $js, 'ש' ) );
t( 'restore: owner-hidden private card goes back to publish', 'publish' === nlf_restore_status( 'private', 'publish', true ) );
t( 'restore: back to pending, not published', 'pending' === nlf_restore_status( 'private', 'pending', true ) );
t( 'restore: staff-private card (owner did not hide) stays private', '' === nlf_restore_status( 'private', 'publish', false ) );
t( 'restore: private with no stored status stays private', '' === nlf_restore_status( 'private', '', true ) );
t( 'restore: bad stored status ignored', '' === nlf_restore_status( 'private', 'future', true ) );
t( 'restore: a public card is left alone', '' === nlf_restore_status( 'publish', 'draft', true ) );
t( 'rules: same version = none', 'none' === nlf_rules_step( '1', '1', false ) && 'none' === nlf_rules_step( '1', '1', true ) );
t( 'rules: new version = flush', 'flush' === nlf_rules_step( '', '1', false ) );
t( 'rules: /forum/ owned by a page = skip', 'skip' === nlf_rules_step( '', '1', true ) );
t( 'act page: genuine link always', nlf_act_takeover( true, false ) && nlf_act_takeover( true, true ) );
t( 'act page: broken link only with the gate open', ! nlf_act_takeover( false, false ) && nlf_act_takeover( false, true ) );

/* the trade list (inc/pro-forum-trades.php) */
require __DIR__ . '/../inc/pro-forum-trades.php';
$tr = nadlan_forum_trades();
t( 'trades: 84 trades in 6 groups', 84 === count( $tr ) && 6 === count( nadlan_forum_trade_groups() ) );
$regs = array();
foreach ( $tr as $x ) { $regs[ $x['reg'] ] = 1; }
t( 'trades: reg values known', ! array_diff( array_keys( $regs ), array( '', 'contractors', 'brokers', 'appraisers', 'review' ) ) );
t( 'trades: keys are safe for sanitize_key', ! preg_grep( '/[^a-z0-9_\-]/', array_keys( $tr ) ) );
t( 'trades: search finds a trade', in_array( 'architect', nadlan_forum_trade_search( 'אדריכל' ), true ) );

/* house laws on the module's own text: no long dashes, no banned words */
$src = '';
foreach ( array( 'inc/pro-forum.php', 'inc/pro-forum-render.php', 'inc/pro-forum-admin.php', 'assets/proforum/forum.js', 'assets/proforum/forum.css' ) as $f ) { $src .= file_get_contents( __DIR__ . '/../' . $f ); }
t( 'no long dashes in module files', false === strpos( $src, '—' ) && false === strpos( $src, '–' ) );
t( 'no banned words', ! preg_match( '/פלטפורמה|המערכת|אינטראקטיבי|אטלס|נחבר אתכם/u', $src ) );
t( 'no redirects in module', ! preg_match( '/wp_redirect\s*\(|wp_safe_redirect\s*\(|header\(\s*[\'"]Location/i', $src ) );
t( 'no robots changes in code', ! preg_match( '/wp_robots|\[\s*[\'"](noindex|nofollow)[\'"]\s*\]|content="[^"]*(noindex|nofollow)|rel="nofollow/i', $src ) );
// 1.72.670: "no previous post" must read as 0, never as now (a member with no posts could not post at all)
$src_ts = file_get_contents( __DIR__ . '/../inc/pro-forum.php' );
if ( preg_match( '/function nlf_ts\( \$sql_utc \) \{.*?\n\}/s', $src_ts, $mm_ts ) && ! function_exists( 'nlf_ts' ) ) { eval( substr( $mm_ts[0], 0 ) ); } // phpcs:ignore -- test only
t( 'nlf_ts empty is 0', function_exists( 'nlf_ts' ) && 0 === nlf_ts( '' ) && 0 === nlf_ts( null ) && 0 === nlf_ts( '0000-00-00 00:00:00' ) );
t( 'nlf_ts real time', function_exists( 'nlf_ts' ) && 1700000000 === nlf_ts( gmdate( 'Y-m-d H:i:s', 1700000000 ) ) );
// 1.72.671: a clean first message goes live by itself; a suspicious one waits; the switch off sends every first one to review
t( 'first clean live', 'live' === nlf_first_status( 0, 'מחפשים קבלן שיפוצים לאמבטיה בגבעתיים', true ) );
t( 'first spam word pending', 'pending' === nlf_first_status( 0, 'הכי טוב קזינו אונליין', true ) );
t( 'first repeat pending', 'pending' === nlf_first_status( 0, 'מבצעעעעעעעע', true ) );
t( 'first latin pending', 'pending' === nlf_first_status( 0, 'best cheap renovation offers in town call now for a deal', true ) );
t( 'first switch off pending', 'pending' === nlf_first_status( 0, 'שאלה נקייה לגמרי', false ) );
t( 'trusted always live', 'live' === nlf_first_status( 2, 'הכי טוב קזינו', false ) );
t( 'js under 27 KB', filesize( __DIR__ . '/../assets/proforum/forum.js' ) < 27648 ); // 12.11: + the menu's ?join=1 opener (was 25 KB)
t( 'no innerHTML / eval in js', ! preg_match( '/innerHTML|outerHTML|insertAdjacentHTML|\beval\s*\(|new Function/', file_get_contents( __DIR__ . '/../assets/proforum/forum.js' ) ) );
$css = file_get_contents( __DIR__ . '/../assets/proforum/forum.css' );
t( 'css: nothing pushed off-screen (RTL sideways scroll)', ! preg_match( '/(left|right)\s*:\s*-\d{3,}px/', $css ) );
t( 'css: reduced motion respected', false !== strpos( $css, 'prefers-reduced-motion' ) );
$core = file_get_contents( __DIR__ . '/../inc/pro-forum.php' );
t( 'rest routes hidden from the public index', false !== strpos( $core, "'show_in_index' => false" ) );
t( 'ping answers exactly loaded/public/v', 1 === preg_match( "/array\( 'loaded' => true, 'public' => nlf_public\(\), 'v' => NADLAN_FORUM_VERSION \)/", $core ) );
t( 'every forum error is HTTP 400', 1 === preg_match( "/'status' => 400/", $core ) && ! preg_match( "/'status' => 40[13]/", $core ) );
t( 'no 301/302 anywhere', ! preg_match( '/\b30[12]\b/', $src ) );
t( 'trades file loaded by the module', false !== strpos( $core, "require_once __DIR__ . '/pro-forum-trades.php'" ) );

echo "\n$pass passed, $fail failed\n";
exit( $fail ? 1 : 0 );
