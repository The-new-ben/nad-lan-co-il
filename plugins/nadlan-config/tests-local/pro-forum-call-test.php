<?php
/**
 * Plain PHP CLI test of the forum call's pure functions (no WordPress): php tests-local/pro-forum-call-test.php
 * Loads only part 1 of inc/pro-forum-call.php (NLFC_PURE_ONLY). Exit code 0 = all passed.
 */
define( 'NLFC_PURE_ONLY', true );
require __DIR__ . '/../inc/pro-forum-call.php';

$pass = 0; $fail = 0;
function t( $name, $cond ) {
	global $pass, $fail;
	if ( $cond ) { $pass++; echo "ok   $name\n"; } else { $fail++; echo "FAIL $name\n"; }
}

/* room names */
$r = nlfc_rand( 12 );
t( 'room id is 12 of a-z2-7', 1 === preg_match( '/^[a-z2-7]{12}$/', $r ) && nlfc_room_valid( $r ) );
t( 'two rooms differ', nlfc_rand( 12 ) !== nlfc_rand( 12 ) );
t( 'rand is deterministic on given bytes', 'abcd' === nlfc_rand( 4, "\x00\x01\x02\x03" ) && '7a' === nlfc_rand( 2, "\x1f\x20" ) );
t( 'identity of 10', 1 === preg_match( '/^[a-z2-7]{10}$/', nlfc_rand( 10 ) ) );
t( 'LiveKit room prefix', 'nadlan-frm-' . $r === nlfc_lk_room( $r ) && nlfc_lk_room_valid( nlfc_lk_room( $r ) ) );
t( 'LiveKit room serves the edge function rule nadlan-*', 0 === strpos( nlfc_lk_room( $r ), 'nadlan-' ) );
t( 'not a designer room', ! nlfc_lk_room_valid( 'nadlan-dsg-' . $r ) && ! nlfc_lk_room_valid( 'nadlan-frm-' . $r . 'x' ) );
t( 'room refuses upper case, 1, 8, short, array', ! nlfc_room_valid( 'ABCDEFGHIJKL' ) && ! nlfc_room_valid( 'abcdefghijk1' ) && ! nlfc_room_valid( 'abcdefghijk8' ) && ! nlfc_room_valid( 'abc' ) && ! nlfc_room_valid( array() ) );

/* the limits window */
$day = 86400;
t( 'same UTC day = same window', nlfc_window( 1762905600, $day ) === nlfc_window( 1762905600 + 86399, $day ) );
t( 'next day = next window', nlfc_window( 1762905600, $day ) + 1 === nlfc_window( 1762905600 + 86400, $day ) );
t( 'key stable inside a day', nlfc_rl_key( 'room', 'm5', 1762905600, $day ) === nlfc_rl_key( 'room', 'm5', 1762905600 + 3600, $day ) );
t( 'key changes next day', nlfc_rl_key( 'room', 'm5', 1762905600, $day ) !== nlfc_rl_key( 'room', 'm5', 1762905600 + $day, $day ) );
t( 'key per member', nlfc_rl_key( 'room', 'm5', 1, $day ) !== nlfc_rl_key( 'room', 'm6', 1, $day ) );
t( 'key prefix is our own bucket (not nltr_ / nldsg_ / nlf_rl_)', 0 === strpos( nlfc_rl_key( 'room', 'all', 1, $day ), 'nlfc_rl_' ) );
t( 'key under the 172-character transient name limit', strlen( nlfc_rl_key( 'room', str_repeat( 'a', 64 ), 1, $day ) ) < 60 );
t( 'caps 8 / 8 / 40', array( 'member' => 8, 'ip' => 8, 'forum' => 40 ) === nlfc_caps() );
t( 'limits: fresh day passes', '' === nlfc_limits_verdict( array( 'member' => 0, 'ip' => 0, 'forum' => 0 ) ) );
t( 'limits: 7 passes', '' === nlfc_limits_verdict( array( 'member' => 7, 'ip' => 7, 'forum' => 39 ) ) );
t( 'limits: member 8 stops', 'rate_member' === nlfc_limits_verdict( array( 'member' => 8, 'ip' => 0, 'forum' => 0 ) ) );
t( 'limits: ip 8 stops', 'rate_ip' === nlfc_limits_verdict( array( 'member' => 0, 'ip' => 8, 'forum' => 0 ) ) );
t( 'limits: forum 40 stops', 'rate_forum' === nlfc_limits_verdict( array( 'member' => 0, 'ip' => 0, 'forum' => 40 ) ) );
t( 'limits: owner cap option', 'rate_forum' === nlfc_limits_verdict( array( 'forum' => 10 ), array( 'forum' => 10 ) ) && '' === nlfc_limits_verdict( array( 'forum' => 10 ), array( 'forum' => 50 ) ) );

/* the permission predicate. Discussion 10 opened by member 1; member 2 replied (live), member 3 replied (pending),
   member 4 replied (live) but switched video off, member 5 replied (live) and is blocked, member 6 never wrote. */
$topic   = array( 'id' => 10, 'member_id' => 1, 'status' => 'live' );
$replies = array(
	array( 'member_id' => 2, 'status' => 'live' ),
	array( 'member_id' => 3, 'status' => 'pending' ),
	array( 'member_id' => 4, 'status' => 'live' ),
	array( 'member_id' => 5, 'status' => 'live' ),
	array( 'member_id' => 2, 'status' => 'live' ),
);
$video = array( 1 => true, 2 => true, 3 => true, 4 => false, 5 => true, 6 => true );
$ok    = array( 1 => true, 2 => true, 3 => true, 4 => true, 5 => false, 6 => true );
t( 'repliers: live only, unique', array( 2, 4, 5 ) === nlfc_repliers( $replies ) );
t( 'author calls a replier', '' === nlfc_can_call( $topic, $replies, 1, 2, $video, $ok ) );
t( 'replier calls the author', '' === nlfc_can_call( $topic, $replies, 2, 1, $video, $ok ) );
t( 'not with yourself', 'self' === nlfc_can_call( $topic, $replies, 1, 1, $video, $ok ) );
t( 'pending reply does not count', 'wrote' === nlfc_can_call( $topic, $replies, 1, 3, $video, $ok ) );
t( 'pending replier cannot call', 'wrote' === nlfc_can_call( $topic, $replies, 3, 1, $video, $ok ) );
t( 'someone who never wrote cannot call', 'wrote' === nlfc_can_call( $topic, $replies, 6, 1, $video, $ok ) );
t( 'nobody can call someone who never wrote', 'wrote' === nlfc_can_call( $topic, $replies, 1, 6, $video, $ok ) );
t( 'two repliers cannot call each other', 'pair' === nlfc_can_call( $topic, $replies, 2, 4, $video, $ok ) );
t( 'video switched off', 'video_off' === nlfc_can_call( $topic, $replies, 1, 4, $video, $ok ) );
t( 'blocked member', 'member' === nlfc_can_call( $topic, $replies, 1, 5, $video, $ok ) );
t( 'unknown switch = off', 'video_off' === nlfc_can_call( $topic, $replies, 1, 2, array(), $ok ) );
t( 'hidden discussion', 'topic' === nlfc_can_call( array( 'id' => 10, 'member_id' => 1, 'status' => 'hidden' ), $replies, 1, 2, $video, $ok ) );
t( 'pending discussion', 'topic' === nlfc_can_call( array( 'id' => 10, 'member_id' => 1, 'status' => 'pending' ), $replies, 1, 2, $video, $ok ) );
t( 'no discussion', 'topic' === nlfc_can_call( array(), $replies, 1, 2, $video, $ok ) );
t( 'missing member id', 'with' === nlfc_can_call( $topic, $replies, 1, 0, $video, $ok ) && 'with' === nlfc_can_call( $topic, $replies, 0, 2, $video, $ok ) );
t( 'author with no replies yet', 'wrote' === nlfc_can_call( $topic, array(), 1, 2, $video, $ok ) );
t( 'string ids work', '' === nlfc_can_call( array( 'id' => '10', 'member_id' => '1', 'status' => 'live' ), array( array( 'member_id' => '2', 'status' => 'live' ) ), '1', '2', $video, $ok ) );
t( 'targets of the author: 2 only', array( 2 ) === nlfc_targets( $topic, $replies, 1, $video, $ok ) );
t( 'targets of a replier: the author', array( 1 ) === nlfc_targets( $topic, $replies, 2, $video, $ok ) );
t( 'targets when the author switched video off: none', array() === nlfc_targets( $topic, $replies, 2, array( 1 => false ) + $video, $ok ) );
t( 'targets of someone who never wrote: none', array() === nlfc_targets( $topic, $replies, 6, $video, $ok ) );

/* the browser's same-site headers */
t( 'fetch: no headers pass', '' === nlfc_fetch_refusal( array(), 'nad-lan.co.il' ) );
t( 'fetch: same-origin passes', '' === nlfc_fetch_refusal( array( 'sec_fetch_site' => 'same-origin', 'origin' => 'https://nad-lan.co.il' ), 'nad-lan.co.il' ) );
t( 'fetch: cross-site refused', 'site' === nlfc_fetch_refusal( array( 'sec_fetch_site' => 'cross-site' ), 'nad-lan.co.il' ) );
t( 'fetch: other origin refused', 'origin' === nlfc_fetch_refusal( array( 'origin' => 'https://evil.example' ), 'nad-lan.co.il' ) );
t( 'fetch: lookalike origin refused', 'origin' === nlfc_fetch_refusal( array( 'origin' => 'https://nad-lan.co.il.evil.example' ), 'nad-lan.co.il' ) );

/* messages and mail */
foreach ( array( 'closed', 'off', 'need_entry', 'nonce', 'topic', 'self', 'wrote', 'pair', 'member', 'video_off', 'rate_member', 'rate_ip', 'rate_forum', 'gone', 'notin', 'full', 'lk' ) as $c ) {
	t( "message for $c is Hebrew", 1 === preg_match( '/\p{Hebrew}/u', nlfc_msg( $c ) ) );
}
t( 'unknown code has a message', '' !== nlfc_msg( 'zzz' ) );
list( $s, $b ) = nlfc_mail_parts( "דני\nכהן", 'שיפוץ אמבטיה מלא · גבעתיים', 'https://nad-lan.co.il/forum/10/?forum=on#call=abcdefghijkl', 'https://nad-lan.co.il/?nlfc_stop=x' );
t( 'mail subject wording', 'דני כהן מזמין אתכם לשיחת וידאו על שיפוץ אמבטיה מלא · גבעתיים' === $s );
t( 'mail subject one line', false === strpos( $s, "\n" ) );
t( 'mail body has the room link', false !== strpos( $b, '#call=abcdefghijkl' ) );
t( 'mail body has the stop link', false !== strpos( $b, 'nlfc_stop=' ) );
t( 'mail says not recorded', false !== strpos( $b, 'השיחה לא מוקלטת' ) );
t( 'long title cut to 120', 120 === mb_strlen( nlfc_line( str_repeat( 'א', 300 ), 120 ), 'UTF-8' ) );

/* invites list */
$now = 1762905600;
$inv = nlfc_invites_prune( array(
	array( 'room' => 'aaaaaaaaaaaa', 't' => $now - 100 ),
	array( 'room' => 'bbbbbbbbbbbb', 't' => $now - 2000 ),  // too old
	array( 'room' => 'aaaaaaaaaaaa', 't' => $now - 50 ),   // the same room again
	array( 'room' => 'BAD', 't' => $now ),                  // not a room
	array( 'room' => 'cccccccccccc', 't' => $now - 10 ),
), $now );
t( 'invites: newest first, one per room, old and bad dropped', array( 'cccccccccccc', 'aaaaaaaaaaaa' ) === array_column( $inv, 'room' ) );
$many = array(); for ( $i = 0; $i < 9; $i++ ) { $many[] = array( 'room' => nlfc_rand( 12 ), 't' => $now - $i ); }
t( 'invites: at most 5', 5 === count( nlfc_invites_prune( $many, $now ) ) );

/* house rules on the new files */
$js  = (string) file_get_contents( __DIR__ . '/../assets/proforum/call.js' );
$php = (string) file_get_contents( __DIR__ . '/../inc/pro-forum-call.php' );
$css = (string) file_get_contents( __DIR__ . '/../assets/proforum/call.css' );
t( 'no 403 anywhere in the routes', false === strpos( $php, "'status' => 403" ) && false === strpos( $php, ', 403' ) );
t( 'errors are 400', false !== strpos( $php, "array( 'status' => 400 )" ) );
t( 'no owner mail in the module', false === strpos( $php, 'admin_email' ) && false === strpos( $php, 'nlf_admin_to' ) && false === strpos( $php, 'nadlan_alert_mail' ) );
t( 'no recording', 0 === preg_match( '/egress|startRecording|MediaRecorder/i', $js . $php ) );
t( 'js: innerHTML only for the constant icons', 1 === substr_count( $js, 'innerHTML' ) && false !== strpos( $js, 's.innerHTML = ICON[k]' ) );
t( 'js: reuses livekitTransport of the designer call', false !== strpos( $js, 'mod.livekitTransport(' ) );
t( 'js: no emoji', 0 === preg_match( '/[\x{1F300}-\x{1FAFF}\x{2600}-\x{27BF}]/u', $js . $css . $php ) );
t( 'js: no wheel or touch capture', 0 === preg_match( "/addEventListener\\(\\s*'(wheel|touchmove|touchstart)'/", $js ) );
t( 'css: 44px targets on the call controls', false !== strpos( $css, 'min-height: 56px' ) && false !== strpos( $css, 'min-height: 44px' ) );
t( 'no secret read outside the designer/together helpers', 0 === preg_match( "/get_option\\(\\s*'nadlan_tr_/", $php ) );

echo "\n$pass passed, $fail failed\n";
exit( $fail ? 1 : 0 );
