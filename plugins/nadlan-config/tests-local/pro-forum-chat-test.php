<?php
/**
 * Plain PHP CLI test of the chat inside a video room (no WordPress): php tests-local/pro-forum-chat-test.php
 * Loads the forum's pure part (NLF_PURE_ONLY) and then part 1 of inc/pro-forum-chat.php (NLFCH_PURE_ONLY), plus static checks on
 * the module's files and on the lines it needs elsewhere. Exit code 0 = all passed.
 */
define( 'ABSPATH', __DIR__ . '/' );
define( 'NLF_PURE_ONLY', true );
define( 'NLFCH_PURE_ONLY', true );
require __DIR__ . '/../inc/pro-forum.php';
require __DIR__ . '/../inc/pro-forum-chat.php';

$pass = 0; $fail = 0;
function t( $name, $cond ) {
	global $pass, $fail;
	if ( $cond ) { $pass++; echo "ok   $name\n"; } else { $fail++; echo "FAIL $name\n"; }
}

/* the numbers of the brief */
$L = nlfch_limits();
t( 'limits: 1000 characters, 30 a minute, 400 a day, 7 days', 1000 === $L['body'] && 30 === $L['minute'] && 400 === $L['day'] && 7 === $L['keep'] );
t( 'limits: 10 files on the answer (the media module\'s answer limit), under 4000 characters', 10 === $L['files'] && $L['sum'] < 4000 );
t( 'two word reactions, as on the board', array( 'useful' => 'מועיל', 'thanks' => 'תודה' ) === nlfch_reacts() );

/* body cleaning and limits */
t( 'clean: trims and drops control and bidi characters', 'שלום עולם' === nlfch_body_clean( "  שלום\x07 \u{202E}עולם  " ) || 'שלום  עולם' === nlfch_body_clean( "  שלום\x07 \u{202E}עולם  " ) );
t( 'clean: at most one empty line', "א\n\nב" === nlfch_body_clean( "א\n\n\n\n\nב" ) );
t( 'clean: CRLF to LF', "א\nב" === nlfch_body_clean( "א\r\nב" ) );
t( 'clean: invalid UTF-8 is nothing', '' === nlfch_body_clean( "\xC3\x28" ) );
t( 'empty without a file is refused', '' !== nlfch_body_error( '', false ) );
t( 'empty with a file goes', '' === nlfch_body_error( '', true ) );
t( '1000 characters go', '' === nlfch_body_error( str_repeat( 'א', 1000 ), false ) );
t( '1001 characters are refused, never cut', 'ההודעה ארוכה מדי. עד 1,000 תווים.' === nlfch_body_error( str_repeat( 'א', 1001 ), false ) );
t( 'length counts letters, not bytes', 3 === nlfch_len( 'אבג' ) );

/* the forum's own link and phone rule */
t( 'new member: a link is refused with the forum\'s words', nlf_text_rule_error( 'ראו www.example.com', 0 ) === nlfch_rule_error( 'ראו www.example.com', 0 ) && '' !== nlfch_rule_error( 'ראו www.example.com', 0 ) );
t( 'new member: a phone is refused', '' !== nlfch_rule_error( 'תתקשרו 050-1234567', 1 ) );
t( 'new member: an email is refused', '' !== nlfch_rule_error( 'כתבו ל a.b@example.co.il', 0 ) );
t( 'new member: plain words go', '' === nlfch_rule_error( 'הכתם מתחיל ליד החלון ויורד עד הרצפה.', 0 ) );
t( 'two approved posts: a link goes', '' === nlfch_rule_error( 'https://example.com', 2 ) );

/* rate math */
t( 'window: minute index', 2 === nlfch_window( 179, 60 ) && 3 === nlfch_window( 180, 60 ) );
t( 'window: UTC day index', 1 === nlfch_window( 86400, 86400 ) && 0 === nlfch_window( 86399, 86400 ) );
t( 'rate: 29 this minute goes', '' === nlfch_rate_error( 29, 10 ) );
t( 'rate: the 31st in a minute is refused', '' !== nlfch_rate_error( 30, 10 ) );
t( 'rate: 399 today goes', '' === nlfch_rate_error( 0, 399 ) );
t( 'rate: the 401st today is refused, and the day wins over the minute', false !== strpos( nlfch_rate_error( 30, 400 ), '400' ) );
t( 'rate: Hebrew messages', 1 === preg_match( '/\p{Hebrew}/u', nlfch_rate_error( 30, 0 ) ) && 1 === preg_match( '/\p{Hebrew}/u', nlfch_rate_error( 0, 400 ) ) );

/* retention cutoff */
$now = 1763481600; // 2025-11-18 16:00:00 UTC
t( 'cutoff: 7 days back, UTC, SQL format', '2025-11-11 16:00:00' === nlfch_cutoff( $now ) );
t( 'cutoff: days given', '2025-11-17 16:00:00' === nlfch_cutoff( $now, 1 ) );
t( 'cutoff: never less than a day', nlfch_cutoff( $now, 0 ) === nlfch_cutoff( $now, 1 ) );

/* reactions: one per person per message */
t( 'react key', 'useful' === nlfch_react_norm( 'useful' ) && '' === nlfch_react_norm( 'love' ) );
$m = nlfch_reacts_toggle( '', 5, 'useful' );
t( 'first press adds', array( 'useful' => array( 5 ), 'thanks' => array() ) === $m );
$m = nlfch_reacts_toggle( wp_json_encode_or( $m ), 5, 'thanks' );
t( 'the other word moves the person (one per person)', array( 'useful' => array(), 'thanks' => array( 5 ) ) === $m );
$m = nlfch_reacts_toggle( $m, 5, 'thanks' );
t( 'the same word again takes it back', array( 'useful' => array(), 'thanks' => array() ) === $m );
$m = nlfch_reacts_toggle( nlfch_reacts_toggle( nlfch_reacts_toggle( '', 1, 'useful' ), 2, 'useful' ), 3, 'thanks' );
t( 'counts are everyone\'s', array( 'useful' => 2, 'thanks' => 1 ) === nlfch_reacts_counts( $m ) );
t( 'mine', 'useful' === nlfch_reacts_mine( $m, 2 ) && 'thanks' === nlfch_reacts_mine( $m, 3 ) && '' === nlfch_reacts_mine( $m, 9 ) );
t( 'garbage JSON counts as none', array( 'useful' => 0, 'thanks' => 0 ) === nlfch_reacts_counts( '{bad' ) );
t( 'stored ids are positive integers, once', array( 'useful' => array( 4 ), 'thanks' => array() ) === nlfch_reacts_read( '{"useful":[4,"4",-1,0],"evil":[1]}' ) );
t( 'unknown word changes nothing', nlfch_reacts_read( $m ) === nlfch_reacts_toggle( $m, 7, 'love' ) );

/* the end-of-call sheet */
t( 'media label: the board\'s pattern', 'תמונה אחת ותוכנית אחת' === nlfch_media_label( 1, 1 ) );
t( 'media label: plurals and the maqaf before a number', '3 תמונות ו-2 תוכניות' === nlfch_media_label( 3, 2 ) && 'תמונה אחת ו-4 תוכניות' === nlfch_media_label( 1, 4 ) );
t( 'media label: one kind only', '2 תמונות' === nlfch_media_label( 2, 0 ) && 'תוכנית אחת' === nlfch_media_label( 0, 1 ) && '' === nlfch_media_label( 0, 0 ) );
t( 'minutes: at least one, rounded', 1 === nlfch_minutes( 100, 110 ) && 24 === nlfch_minutes( 0, 24 * 60 + 20 ) );
$rows = array(
	array( 'id' => 1, 'name' => 'רונית ב.', 'body' => 'הכתם מתחיל ליד החלון.', 'media_id' => 0, 'media_kind' => '', 'pinned' => 0 ),
	array( 'id' => 2, 'name' => 'דני ש.', 'body' => 'שלחתי תמונה של הלחות מבחוץ', 'media_id' => 40, 'media_kind' => 'image', 'pinned' => 0 ),
	array( 'id' => 3, 'name' => 'דני ש.', 'body' => "בודקים קודם את המרזב מבחוץ,\nורק אחר כך פותחים את הקיר", 'media_id' => 0, 'media_kind' => '', 'pinned' => 1 ),
	array( 'id' => 4, 'name' => 'רונית ב.', 'body' => '', 'media_id' => 41, 'media_kind' => 'pdf', 'pinned' => 0 ),
	array( 'id' => 5, 'name' => 'רונית ב.', 'body' => 'תודה', 'media_id' => 42, 'media_kind' => 'avatar', 'pinned' => 0 ),
);
$p = nlfch_summary_parts( $rows );
t( 'parts: the pinned message', 3 === $p['pin']['id'] );
t( 'parts: pictures and plans only', array( 2, 4 ) === array_column( $p['media'], 'id' ) );
t( 'parts: the rest has words, without the pinned one', array( 1, 2, 5 ) === array_column( $p['rest'], 'id' ) );
$c = nlfch_summary_choose( $p, true, true, false );
t( 'board default (pinned + media): one line, two files', 1 === count( $c['items'] ) && array( 2, 4 ) === array_column( $c['media'], 'id' ) && array( 3, 2, 4 ) === $c['ids'] );
$c = nlfch_summary_choose( $p, true, false, true );
t( 'pinned first, then the others in order', array( 'דני ש.', 'רונית ב.', 'דני ש.', 'רונית ב.' ) === array_column( $c['items'], 'name' ) && ! $c['media'] );
t( 'nothing chosen = nothing', array() === nlfch_summary_choose( $p, false, false, false )['ids'] );
t( 'files capped', 1 === count( nlfch_summary_choose( $p, false, true, false, 1 )['media'] ) );
$txt = nlfch_summary_text( nlfch_summary_choose( $p, true, false, true )['items'] );
$lines = explode( "\n", $txt );
t( 'text: starts with the line "מה סוכם בשיחה"', 'מה סוכם בשיחה' === $lines[0] );
t( 'text: "שם: טקסט", one line each', 'דני ש.: בודקים קודם את המרזב מבחוץ, ורק אחר כך פותחים את הקיר' === $lines[2] && 'רונית ב.: הכתם מתחיל ליד החלון.' === $lines[3] );
t( 'text: only the heading when no words were chosen', 'מה סוכם בשיחה' === nlfch_summary_text( array() ) );
$many = array();
for ( $i = 0; $i < 40; $i++ ) { $many[] = array( 'name' => 'שם', 'text' => str_repeat( 'מילה ', 30 ) ); }
$long = nlfch_summary_text( $many, 1000 );
t( 'text: never longer than the limit, says how many stayed out', nlfch_len( $long ) <= 1000 && 1 === preg_match( '/ועוד \d+ הודעות מהשיחה\.$/u', $long ) );
t( 'text: fits the forum (4000) at the default limit', nlfch_len( nlfch_summary_text( $many ) ) <= 4000 && '' === nlf_body_error( nlfch_summary_text( $many ), true ) );
foreach ( array( 'off', 'room', 'notin', 'gone', 'host', 'own', 'self', 'media', 'home', 'already', 'nothing', 'rate', 'zzz' ) as $code ) {
	t( "message for $code is Hebrew", 1 === preg_match( '/\p{Hebrew}/u', nlfch_msg( $code ) ) );
}

/* static checks on the files */
$php  = (string) file_get_contents( __DIR__ . '/../inc/pro-forum-chat.php' );
$js   = (string) file_get_contents( __DIR__ . '/../assets/proforum/chat.js' );
$cjs  = (string) file_get_contents( __DIR__ . '/../assets/proforum/call.js' );
$css  = (string) file_get_contents( __DIR__ . '/../assets/proforum/call.css' );
$core = (string) file_get_contents( __DIR__ . '/../inc/pro-forum.php' );
$kit  = (string) @file_get_contents( __DIR__ . '/../../../scripts/project-stage/forum_testkit.py' );
t( 'no 403 anywhere, errors are 400', false === strpos( $php, "'status' => 403" ) && false !== strpos( $php, "array( 'status' => 400 )" ) );
t( 'routes hidden from the index', false !== strpos( $php, "'show_in_index' => false" ) );
t( 'all eight routes', false !== strpos( $php, "\$reg( '', 'GET'" ) && false !== strpos( $php, "\$reg( '/send', 'POST'" ) && false !== strpos( $php, "\$reg( '/react', 'POST'" )
	&& false !== strpos( $php, "\$reg( '/pin', 'POST'" ) && false !== strpos( $php, "\$reg( '/delete', 'POST'" ) && false !== strpos( $php, "\$reg( '/report', 'POST'" )
	&& false !== strpos( $php, "\$reg( '/summary', 'GET'" ) && false !== strpos( $php, "\$reg( '/attach', 'POST'" ) );
t( 'every route goes through the room check', 8 === substr_count( $php, '$c = nlfch_ctx( $q, ' ) );
t( 'the room check uses nlfc_can_join and the member list', false !== strpos( $php, "'' !== nlfc_can_join( \$r, \$mid, nlfc_room_max( \$r ) ) || ! isset( \$r['ok'][ \$mid ] )" ) );
t( 'writes are member writes (nonce + same-site headers)', 6 === substr_count( $php, 'nlfch_ctx( $q, true )' ) );
t( 'table {prefix}nlf_chat with the brief\'s columns', false !== strpos( $php, "\$wpdb->prefix . 'nlf_chat'" ) && 1 === preg_match( '/room CHAR\(12\).*member_id BIGINT.*body TEXT.*media_id BIGINT UNSIGNED NULL.*pinned TINYINT.*reactions TEXT.*attached TINYINT.*created_at DATETIME/s', $php ) );
t( 'reports go into the forum flags table as chat', false !== strpos( $php, "VALUES ('chat', %d, %d, %s, %s, %s)" ) );
t( 'the answer runs the forum\'s own steps', false !== strpos( $php, 'nlf_post_limits( $m, false, $body )' ) && false !== strpos( $php, "apply_filters( 'nlf_post_check', '', 'reply', \$m, \$fake, \$t )" )
	&& false !== strpos( $php, 'nlf_first_status( $m[\'approved_posts\']' ) && false !== strpos( $php, "do_action( 'nlf_post_created', 'reply', \$id, \$m, \$fake, \$status, (int) \$t['id'] )" )
	&& false !== strpos( $php, 'nlf_on_reply_live( $id )' ) && false !== strpos( $php, "nlf_mail_admin_pending( 'reply', \$id )" ) && false !== strpos( $php, 'nlf_write_counted( $m )' ) );
t( 'the home room has no attach', false !== strpos( $php, "(int) \$ctx['topic'] <= 0 ) { return nlfch_err( 'home' ); }" ) );
t( 'only the host attaches, pins and sees the summary', 3 === substr_count( $php, "if ( ! \$c['host'] ) { return nlfch_err( 'host' ); }" ) );
t( 'a chat file is the sender\'s own pending file, then status chat', false !== strpos( $php, "SET status = 'chat' WHERE id = %d AND member_id = %d AND topic_id IS NULL AND reply_id IS NULL AND status = 'pending'" ) );
t( 'daily clean-up through WP-Cron, attached rows stay', false !== strpos( $php, "wp_schedule_event( time() + HOUR_IN_SECONDS, 'daily', 'nlfch_gc' )" ) && false !== strpos( $php, 'WHERE attached = 0 AND created_at < %s' ) );
t( 'core: one require line at the end, after the media module', 1 === substr_count( $core, "require_once __DIR__ . '/pro-forum-chat.php'" ) && strpos( $core, "'/pro-forum-chat.php'" ) > strpos( $core, "'/pro-forum-media.php'" ) );
t( 'test kit clean removes chat rows', '' === $kit || false !== strpos( $kit, 'nlfch_purge_members( $ids )' ) );
t( 'call.js loads chat.js with its own version query', false !== strpos( $cjs, "new URL('chat.js' + u.search, u)" ) && false !== strpos( $cjs, 'm.createChat({' ) );
t( 'call.js: the chat control sits between the camera and the board', false !== strpos( $cjs, 'bMic, bCam, bChat, bBoard, bInv, bMore, bEnd' ) );
t( 'call.js: the flip moved onto my own picture (the bar keeps seven 44px controls)', false !== strpos( $cjs, 'self.appendChild(bFlip);' ) && false !== strpos( $css, '.nlfc-self .nlfc-c.nlfc-flip { position: absolute;' ) );
t( 'call.js: still one innerHTML (the constant icons)', 1 === substr_count( $cjs, 'innerHTML' ) );
t( 'chat.js: no innerHTML at all', false === strpos( $js, 'innerHTML' ) );
t( 'chat.js: topic chat, a row shown only from its own author', false !== strpos( $js, "publishData('chat'" ) && false !== strpos( $js, 'm.row.who.identity === from' ) );
t( 'chat.js: role=log + aria-live=polite, Enter sends, Shift+Enter a new line, Esc closes', false !== strpos( $js, "role: 'log', 'aria-live': 'polite'" ) && false !== strpos( $js, "ev.key === 'Enter' && !ev.shiftKey" ) && false !== strpos( $js, "ev.key !== 'Escape'" ) );
t( 'chat.js: toast for 4 seconds', false !== strpos( $js, '}, 4000);' ) );
t( 'chat.js: pictures open the media module\'s full-screen view', false !== strpos( $js, "cls: 'nlfmd-tile nlfch-thumb'" ) && false !== strpos( $js, "'data-nlfmd-gal': true" ) );
foreach ( array( "צ'אט החדר", 'נעוץ:', 'הודעות מלפני שנכנסת', 'כתבו לחדר...', 'שליחה', 'מועיל', 'תודה', 'השיחה הסתיימה · ', 'מה לצרף לדיון "', 'כל שאר ההודעות (',
	'לצרף לדיון כ"מה סוכם בשיחה"', "רק מי שפתח את החדר מצרף. בלי הצירוף, הצ'אט נשאר בחדר בלבד ונמחק אחרי 7 ימים." ) as $w ) {
	t( 'board words in chat.js: ' . $w, false !== strpos( $js, $w ) );
}
t( 'css: the board\'s colours', false !== strpos( $css, '#FBE7EF' ) && false !== strpos( $css, '#B0144F' ) && false !== strpos( $css, '#2F6F86' ) && false !== strpos( $css, '#D5DBDF' ) );
t( 'css: buttons 44px', false !== strpos( $css, '.nlfch-send { flex: none; height: 44px' ) && false !== strpos( $css, '.nlfch-rxb { min-height: 44px' ) && false !== strpos( $css, '.nlfch-more { width: 44px; height: 44px' ) );
t( 'css: side panel from 900px', 1 === preg_match( '/@media \(min-width: 900px\) \{\s*\/\* desktop: a side panel/', $css ) );
t( 'no emoji, no long dashes', 0 === preg_match( '/[\x{1F300}-\x{1FAFF}\x{2600}-\x{27BF}]/u', $js . $php ) && false === strpos( $js . $php . $css, '—' ) );
t( 'no redirects, no noindex', 0 === preg_match( '/wp_redirect|wp_safe_redirect|noindex/i', $php . $js ) );

echo "\n$pass passed, $fail failed\n";
exit( $fail ? 1 : 0 );

/** JSON for a stored value in the test (wp_json_encode is not here) */
function wp_json_encode_or( $v ) { return json_encode( $v ); }
