<?php
/**
 * The TogetherRoom server checks, on the WordPress stand-in (wp-stub.php):
 *   php scripts/together/php_selftest.php
 * Rooms, tokens (fallback and LiveKit, the JWT verified), roles, the leader, the state, notes, the file, rate limits,
 * the page output (only with ?room=, no robots meta) and the retention cron.
 */
putenv( 'NLTR_STORE=' . sys_get_temp_dir() . '/nltg-selftest-' . getmypid() . '.json' );
require __DIR__ . '/wp-stub.php';
__nltr_reset();

$fails = 0; $n = 0;
function ok( $cond, $what ) { global $fails, $n; $n++; if ( $cond ) { echo "  ok   $what\n"; } else { $fails++; echo "  FAIL $what\n"; } }
function call( $m, $route, $q = array(), $b = array(), $ip = '10.0.0.1' ) { $_SERVER['REMOTE_ADDR'] = $ip; return __nltr_call( $m, 'nadlan/v1' . $route, $q, $b ); }
function b64d( $s ) { return base64_decode( strtr( $s, '-_', '+/' ) . str_repeat( '=', ( 4 - strlen( $s ) % 4 ) % 4 ) ); }

echo "rooms\n";
$GLOBALS['__nltr_user'] = 0;
list( $st, $d ) = call( 'POST', '/room', array(), array( 'post' => 101 ) );
ok( 403 === $st && 'no_rep' === $d['error'], 'a visitor cannot open a room while no representative is available' );
update_option( 'nadlan_tr_rep_now', '1', false );
list( $st, $d ) = call( 'POST', '/room', array(), array( 'post' => 999 ) );
ok( 400 === $st, 'a room needs a project page with the stage' );
list( $st, $d ) = call( 'POST', '/room', array(), array( 'post' => 101 ) );
ok( 201 === $st && preg_match( '/^[a-z2-7]{12}$/', $d['room'] ), 'a visitor opens a room while a representative is available (12 base32 chars)' );
ok( false !== strpos( $d['join_url'], '/projects/rainbow-tel-aviv/?room=' . $d['room'] ), 'the join link is the project page with ?room= (no new URL)' );
$room = $d['room'];
for ( $i = 0; $i < 5; $i++ ) { list( $st2 ) = call( 'POST', '/room', array(), array( 'post' => 101 ), '10.0.0.9' ); }
ok( 429 === $st2, 'a visitor may open 4 rooms an hour per address' );
$GLOBALS['__nltr_user'] = 7;
list( $st, $d ) = call( 'POST', '/room', array(), array( 'post' => 101 ), '10.0.0.9' );
ok( 201 === $st, 'a representative opens rooms beyond the visitor limit' );
$GLOBALS['__nltr_user'] = 0;

echo "joining\n";
list( $st, $d ) = call( 'POST', '/room/token', array(), array( 'room' => 'bad!', 'name' => 'x', 'role' => 'buyer' ) );
ok( 400 === $st, 'a malformed room id is refused' );
list( $st, $d ) = call( 'POST', '/room/token', array(), array( 'room' => $room, 'name' => 'x', 'role' => 'rep' ) );
ok( 403 === $st && 'role' === $d['error'], 'the role rep needs a logged-in user with edit_posts' );
list( $st, $d ) = call( 'POST', '/room/token', array(), array( 'room' => $room, 'name' => 'x', 'role' => 'wizard' ) );
ok( 400 === $st, 'an unknown role is refused' );
list( $st, $d ) = call( 'POST', '/room/token', array(), array( 'room' => $room, 'name' => '  <b>יואב</b> ' . str_repeat( 'א', 60 ), 'role' => 'buyer' ) );
ok( 200 === $st && 'fallback' === $d['mode'], 'without LiveKit the answer is {mode: fallback}' );
ok( mb_strlen( $d['name'] ) === 40 && false === strpos( $d['name'], '<' ), 'the name is cleaned and cut to 40 characters' );
$buyer = $d;
ok( 8 === strlen( $buyer['pid'] ) && 22 === strlen( $buyer['key'] ), 'a participant id and key come back' );
list( $st, $d ) = call( 'POST', '/room/token', array(), array( 'room' => $room, 'name' => 'יואב', 'role' => 'buyer', 'pid' => $buyer['pid'], 'key' => $buyer['key'] ) );
ok( 200 === $st && $d['pid'] === $buyer['pid'], 'the same browser comes back with the same id' );
$GLOBALS['__nltr_user'] = 7;
list( $st, $rep ) = call( 'POST', '/room/token', array(), array( 'room' => $room, 'name' => 'דנה', 'role' => 'rep' ) );
ok( 200 === $st && 'rep' === $rep['role'], 'a representative enters as rep' );
$GLOBALS['__nltr_user'] = 0;
ok( 2 === count( $rep['participants'] ), 'the participants list has both' );
ok( ! isset( $rep['participants'][0]['k'] ) && false === strpos( json_encode( $rep['participants'] ), 'harness' ), 'no key or hash leaves the server' );

echo "the leader and the state\n";
list( $st, $d ) = call( 'POST', '/room/state', array(), array( 'room' => $room, 'pid' => $buyer['pid'], 'key' => 'wrong', 'state' => array( 'm' => 'building' ) ) );
ok( 403 === $st, 'a wrong key cannot write' );
list( $st, $d ) = call( 'POST', '/room/state', array(), array( 'room' => $room, 'pid' => $buyer['pid'], 'key' => $buyer['key'], 'lead' => true ) );
ok( 403 === $st, 'a buyer cannot lead ("עקבו אחריי" is the representative\'s)' );
list( $st, $d ) = call( 'POST', '/room/state', array(), array( 'room' => $room, 'pid' => $buyer['pid'], 'key' => $buyer['key'], 'state' => array( 'm' => 'building' ) ) );
ok( 409 === $st && 'not_leader' === $d['error'], 'only the leader posts the state' );
list( $st, $d ) = call( 'POST', '/room/state', array(), array( 'room' => $room, 'pid' => $rep['pid'], 'key' => $rep['key'], 'lead' => true ) );
ok( 200 === $st && $d['leader'] === $rep['pid'], 'the representative leads' );
$state = array( 'm' => 'inside', 'u' => '25-w', 'f' => 25, 'v' => array( 's' => 'w-balcony', 'y' => 0.42, 'p' => -0.1, 'f' => 70, 'evil' => '<script>' ), 'pt' => array( 'mode' => 'inside', 'yaw' => 0.3, 'pitch' => 0.1, 'scene' => 'w' ), 'x' => 'drop me' );
list( $st, $d ) = call( 'POST', '/room/state', array(), array( 'room' => $room, 'pid' => $rep['pid'], 'key' => $rep['key'], 'state' => $state ) );
ok( 200 === $st && $d['t'] > 0, 'the leader posts the state' );
list( $st, $d ) = call( 'GET', '/room/state', array( 'room' => $room, 'pid' => $buyer['pid'], 'key' => $buyer['key'], 'since' => 0 ) );
ok( 200 === $st && 'inside' === $d['state']['m'] && '25-w' === $d['state']['u'] && 'w-balcony' === $d['state']['v']['s'], 'a follower reads the state' );
ok( ! isset( $d['state']['x'] ) && ! isset( $d['state']['v']['evil'] ), 'unknown keys are dropped from the state' );
ok( 'דנה' === $d['state']['n'], 'the state carries the leader\'s name from the server, not from the client' );
list( $st, $d2 ) = call( 'GET', '/room/state', array( 'room' => $room, 'pid' => $buyer['pid'], 'key' => $buyer['key'], 'since' => $d['t'] ) );
ok( ! isset( $d2['state'] ), 'a poll with ?since= gets no state that it already has' );
list( $st, $d ) = call( 'GET', '/room/state', array( 'room' => $room, 'pid' => 'aaaaaaaa', 'key' => 'x' ) );
ok( ! empty( $d['rejoin'] ), 'an unknown participant is asked to join again' );

echo "notes\n";
list( $st, $d ) = call( 'POST', '/room/notes', array(), array( 'room' => $room, 'pid' => $buyer['pid'], 'key' => $buyer['key'], 'text' => "  נקודת חשמל ליד החלון,\n40 ס״מ מהרצפה <img src=x onerror=alert(1)>", 'where' => 'סלון · קיר מערבי' . str_repeat( 'x', 80 ), 'anchor' => array( 'mode' => 'inside', 'floor' => 25, 'side' => 'w', 'scene' => 'w', 'yaw' => 0.2, 'pitch' => -0.3, 'bad' => 1 ), 'change' => false ) );
ok( 201 === $st && 1 === $d['note']['n'], 'a participant adds note 1' );
ok( false === strpos( $d['note']['text'], '<img' ) && false !== strpos( $d['note']['text'], "\n" ), 'the text is cleaned (sanitize_textarea_field keeps the line break)' );
ok( mb_strlen( $d['note']['where'] ) === 60, 'where is cut to 60 characters' );
ok( 'יואב' === $d['note']['author'] && 'buyer' === $d['note']['role'], 'the author and role come from the server' );
ok( ! isset( $d['note']['anchor']['bad'] ) && 'inside' === $d['note']['anchor']['mode'], 'the anchor is cleaned' );
$n1 = $d['note'];
list( $st, $d ) = call( 'POST', '/room/notes', array(), array( 'room' => $room, 'pid' => $rep['pid'], 'key' => $rep['key'], 'text' => str_repeat( 'ב', 500 ), 'anchor' => array( 'mode' => 'building', 'x' => 1.5, 'y' => 80, 'z' => -3, 'floor' => 25 ), 'change' => true ) );
ok( 201 === $st && 2 === $d['note']['n'] && 400 === mb_strlen( $d['note']['text'] ) && true === $d['note']['change'], 'note 2: cut to 400, marked as a change (subject to the developer)' );
list( $st, $d ) = call( 'POST', '/room/notes', array(), array( 'room' => $room, 'pid' => $buyer['pid'], 'key' => $buyer['key'], 'text' => '   ' ) );
ok( 400 === $st, 'an empty note is refused' );
list( $st, $d ) = call( 'GET', '/room/notes', array( 'room' => $room ) );
ok( 200 === $st && 2 === count( $d['notes'] ) && $d['rev'] >= 2, 'the notes list, with the revision' );
list( $st, $d ) = call( 'POST', '/room/notes', array(), array( 'room' => $room, 'pid' => $buyer['pid'], 'key' => $buyer['key'], 'delete' => $d['notes'][1]['id'] ) );
ok( 404 === $st, 'a buyer cannot delete the representative\'s note' );
list( $st, $d ) = call( 'POST', '/room/notes', array(), array( 'room' => $room, 'pid' => $rep['pid'], 'key' => $rep['key'], 'delete' => $n1['id'] ) );
ok( 200 === $st, 'the representative deletes any note' );
list( $st, $d ) = call( 'GET', '/room/notes', array( 'room' => $room ) );
ok( 1 === count( $d['notes'] ) && 2 === $d['notes'][0]['n'], 'one note left, its number kept' );

echo "the file\n";
list( $st, $f ) = call( 'GET', '/room/file', array( 'room' => $room ) );
ok( 200 === $st && 25 === $f['floor'] && '' !== $f['project']['name'] && 1 === count( $f['notes'] ), 'the file: project, floor, notes' );
ok( 'לכיוון הים' === $f['facing'] && 'w' === $f['side'] && true === $f['sample'], 'the side in the project\'s own words, always an example apartment' );
list( $st ) = call( 'GET', '/room/file', array( 'room' => 'aaaaaaaaaaaa' ) );
ok( 404 === $st, 'no file for an unknown room' );

echo "LiveKit\n";
update_option( 'nadlan_tr_lk_url', 'wss://x.livekit.cloud', false );
update_option( 'nadlan_tr_lk_key', 'APIkey123', false );
update_option( 'nadlan_tr_lk_secret', 'secret-abc', false );
list( $st, $d ) = call( 'POST', '/room/token', array(), array( 'room' => $room, 'name' => 'מיכל', 'role' => 'partner' ), '10.0.0.2' );
ok( 200 === $st && 'livekit' === $d['mode'] && 'wss://x.livekit.cloud' === $d['url'], 'with the three settings the answer is a LiveKit token' );
$parts = explode( '.', $d['token'] );
$hdr   = json_decode( b64d( $parts[0] ), true );
$cl    = json_decode( b64d( $parts[1] ), true );
ok( array( 'alg' => 'HS256', 'typ' => 'JWT' ) === $hdr, 'the header is {alg:HS256, typ:JWT}' );
ok( hash_equals( rtrim( strtr( base64_encode( hash_hmac( 'sha256', $parts[0] . '.' . $parts[1], 'secret-abc', true ) ), '+/', '-_' ), '=' ), $parts[2] ), 'the signature is HMAC-SHA256 with the secret' );
ok( 'APIkey123' === $cl['iss'] && $cl['sub'] === $d['pid'] && 'מיכל' === $cl['name'], 'iss = the API key, sub = the identity, name' );
ok( $cl['exp'] - $cl['nbf'] >= 7200 && $cl['exp'] - time() <= 7200, 'nbf and exp (+2 hours)' );
ok( array( 'room' => 'nadlan-' . $room, 'roomJoin' => true, 'canPublish' => true, 'canSubscribe' => true, 'canPublishData' => true ) === $cl['video'], 'the video grant' );
ok( array( 'role' => 'partner' ) === json_decode( $cl['metadata'], true ), 'the metadata carries the role' );
file_put_contents( sys_get_temp_dir() . '/nltg-jwt.txt', $d['token'] );
delete_option( 'nadlan_tr_lk_secret' );
list( $st, $d ) = call( 'POST', '/room/token', array(), array( 'room' => $room, 'name' => 'מיכל', 'role' => 'partner' ), '10.0.0.2' );
ok( 'fallback' === $d['mode'], 'without the secret, back to the fallback' );

echo "rate limits\n";
for ( $i = 0; $i < 31; $i++ ) { list( $st ) = call( 'POST', '/room/token', array(), array( 'room' => $room, 'name' => 'x', 'role' => 'friend' ), '10.0.0.77' ); }
ok( 429 === $st, 'tokens: 30 per 10 minutes per address' );

echo "closing and reopening\n";
$GLOBALS['__nltr_now'] = time() + 7 * HOUR_IN_SECONDS;
list( $st, $d ) = call( 'POST', '/room/token', array(), array( 'room' => $room, 'name' => 'יואב', 'role' => 'buyer' ), '10.0.0.3' );
ok( 410 === $st && 'closed' === $d['error'], 'after 6 hours idle the room is closed to visitors' );
list( $st ) = call( 'GET', '/room/state', array( 'room' => $room ) );
ok( 410 === $st, 'the poll says closed' );
list( $st, $f ) = call( 'GET', '/room/file', array( 'room' => $room ) );
ok( 200 === $st && false === $f['open'], 'the file stays readable' );
$GLOBALS['__nltr_user'] = 7;
list( $st, $d ) = call( 'POST', '/room/token', array(), array( 'room' => $room, 'name' => 'דנה', 'role' => 'rep' ), '10.0.0.3' );
ok( 200 === $st, 'a representative reopens it' );
$GLOBALS['__nltr_user'] = 0;
list( $st, $d ) = call( 'POST', '/room/token', array(), array( 'room' => $room, 'name' => 'יואב', 'role' => 'buyer' ), '10.0.0.4' );
ok( 200 === $st, 'and visitors can join again' );

echo "the page\n";
$_GET = array();
ob_start(); __nltr_run( 'wp_footer', 'together.php' ); $out = ob_get_clean();
ok( false === strpos( $out, 'nltg-root' ) && false !== strpos( $out, 'nadlan-together-chooser' ) && false !== strpos( $out, 'room\/available' ), 'without ?room=: no room assets; the chooser script, which asks /room/available' );
list( $st, $d ) = call( 'GET', '/room/available' );
ok( 200 === $st && true === $d['now'], '/room/available: yes while a representative is marked available' );
update_option( 'nadlan_tr_rep_now', '0', false );
ob_start(); __nltr_run( 'wp_footer', 'together.php' ); $out2 = ob_get_clean();
list( $st, $d ) = call( 'GET', '/room/available' );
ok( false === $d['now'] && $out2 === $out, 'no representative: /room/available says no; the page stays the same (a cached page never lies)' );
$_GET = array( 'room' => $room );
ob_start(); __nltr_run( 'wp_head', 'together.php' ); $head = ob_get_clean();
ob_start(); __nltr_run( 'wp_footer', 'together.php' ); $foot = ob_get_clean();
ok( false !== strpos( $head, 'together.css' ) && false !== strpos( $foot, 'id="nltg-root"' ) && false !== strpos( $foot, 'together.js' ), 'with ?room=: the sheet in the head, the container and the script in the footer' );
ok( false === stripos( $head . $foot, 'robots' ) && false === stripos( $head . $foot, 'noindex' ), 'no robots meta, no noindex' );
preg_match( '/data-cfg="([^"]+)"/', $foot, $m );
$cfg = json_decode( html_entity_decode( $m[1], ENT_QUOTES ), true );
ok( '972525101555' === $cfg['wa'] && 101 === $cfg['post'] && false === $cfg['canRep'] && '' === $cfg['nonce'], 'the config: the site\'s WhatsApp, the project; no nonce and no rep for a visitor' );
ok( false === strpos( $foot, 'secret' ) && false === strpos( $foot, 'APIkey' ), 'no LiveKit key or secret in the page' );
$_GET = array( 'room' => 'new' );
ob_start(); __nltr_run( 'wp_footer', 'together.php' ); $foot = ob_get_clean();
ok( false !== strpos( $foot, 'nltg-root' ), '?room=new prints the room too' );
$_GET = array( 'room' => '"><script>' );
ob_start(); __nltr_run( 'wp_footer', 'together.php' ); $foot = ob_get_clean();
ok( false === strpos( $foot, 'nltg-root' ), 'a malformed ?room= prints nothing' );

echo "retention\n";
$GLOBALS['__nltr_now'] = null;
$old = wp_insert_post( array( 'post_type' => 'nadlan_room', 'post_status' => 'publish', 'post_title' => 'room old', 'post_name' => 'oldoldoldold' ) );
$GLOBALS['__nltr']['posts'][ $old ]['post_date_gmt'] = gmdate( 'Y-m-d H:i:s', time() - 31 * DAY_IN_SECONDS );
__nltr_save();
do_action( 'nadlan_tr_cleanup' );
ok( ! get_post_type( $old ) && 'nadlan_room' === get_post_type( nadlan_tr_post( $room ) ), 'the daily cleanup deletes rooms older than 30 days and keeps the rest' );
__nltr_run( 'init', 'together.php' );
ok( false !== wp_next_scheduled( 'nadlan_tr_cleanup' ), 'the daily event is scheduled' );
update_option( 'nadlan_tr_retention', '7', false );
ok( 7 === nadlan_tr_retention_days(), 'the retention days follow the setting' );
ok( 'off' === $GLOBALS['__nltr']['options']['nadlan_tr_lk_url']['autoload'] && 'off' === $GLOBALS['__nltr']['options']['nadlan_tr_rep_now']['autoload'], 'the options are saved with autoload off' );

@unlink( $GLOBALS['__nltr_store_file'] );
echo "\n$n checks, $fails failed\n";
exit( $fails ? 1 : 0 );
