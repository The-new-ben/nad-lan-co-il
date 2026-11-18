<?php
/**
 * Plain PHP CLI test of "a member opens his own card" (no WordPress): php tests-local/pro-forum-card-test.php
 * Loads the forum's pure part (NLF_PURE_ONLY), the trades list, part 1 of inc/pro-forum-card.php (NLFM_PURE_ONLY) and part 1
 * of inc/pro-forum-call.php (NLFC_PURE_ONLY), plus static checks on the module's files. Exit code 0 = all passed.
 */
define( 'ABSPATH', __DIR__ . '/' );
define( 'NLF_PURE_ONLY', true );
define( 'NLFM_PURE_ONLY', true );
define( 'NLFC_PURE_ONLY', true );
require __DIR__ . '/../inc/pro-forum.php';
require __DIR__ . '/../inc/pro-forum-trades.php';
require __DIR__ . '/../inc/pro-forum-card.php';
require __DIR__ . '/../inc/pro-forum-call.php';

$pass = 0; $fail = 0;
function t( $name, $cond ) {
	global $pass, $fail;
	if ( $cond ) { $pass++; echo "ok   $name\n"; } else { $fail++; echo "FAIL $name\n"; }
}
$tr = nadlan_forum_trades();

/* the line under the name */
$nov = gmmktime( 12, 0, 0, 11, 18, 2026 );
t( 'since line, female (board 18 wording)', 'חברה בפורום מאז נובמבר 2026 · הפרטים נמסרו על ידה' === nlfm_since_line( $nov, true ) );
t( 'since line, male', 'חבר בפורום מאז נובמבר 2026 · הפרטים נמסרו על ידו' === nlfm_since_line( $nov, false ) );
t( 'since line: no time prints nothing', '' === nlfm_since_line( 0, true ) );
t( 'since line never says checked', false === strpos( nlfm_since_line( $nov, true ), 'מאומת' ) && false === strpos( nlfm_since_line( $nov, true ), 'נבדק' ) );
t( 'twelve Hebrew months', 12 === count( nlfm_months() ) && 'ינואר' === nlfm_months()[1] && 'דצמבר' === nlfm_months()[12] );
t( 'first name', 'אלונה' === nlfm_first_name( 'אלונה מור' ) && 'דני' === nlfm_first_name( '  דני ' ) );

/* phone */
t( 'phone: 050-0000000', '0500000000' === nlfm_phone_norm( '050-0000000' ) );
t( 'phone: +972 with spaces', '972501234567' === nlfm_phone_norm( '+972 50 123 4567' ) );
t( 'phone: 8 digits refused', '' === nlfm_phone_norm( '03-123456' ) );
t( 'phone: 14 digits refused', '' === nlfm_phone_norm( '12345678901234' ) );
t( 'phone: letters refused', '' === nlfm_phone_norm( '050-CALL-ME1' ) );

/* the form */
$ok = array( 'name' => 'אלונה מור', 'trade' => 'interior_designer', 'form' => 'f', 'city' => 'המרכז',
	'bio' => 'מתכננת ומעצבת פנים, הנדסאית עם 15 שנות ניסיון. עובדת עם מגוון קבלנים ועושה מכרז לביצוע.', 'phone' => '050-1234567', 'how' => 'phone', 'video' => '1' );
$v  = nlfm_validate( $ok, $tr );
t( 'the board 18 example passes', isset( $v['data'] ) );
t( 'clean values', isset( $v['data'] ) && 'interior_designer' === $v['data']['trade'] && 'f' === $v['data']['form'] && '0501234567' === $v['data']['phone'] && true === $v['data']['video'] && 'phone' === $v['data']['how'] );
t( 'the typed phone is kept for editing', isset( $v['data'] ) && '050-1234567' === $v['data']['phone_raw'] );
$e = function ( $over ) use ( $ok, $tr ) { $r = nlfm_validate( array_merge( $ok, $over ), $tr ); return $r['err'] ?? ''; };
t( 'name too short', '' !== $e( array( 'name' => 'א' ) ) );
t( 'name of 60 passes, 61 refused', '' === $e( array( 'name' => str_repeat( 'א', 60 ) ) ) && '' !== $e( array( 'name' => str_repeat( 'א', 61 ) ) ) );
t( 'name with a link refused', '' !== $e( array( 'name' => 'אלונה www.alona.co.il' ) ) );
t( 'name with a phone refused', '' !== $e( array( 'name' => 'אלונה 0501234567' ) ) );
t( 'trade required', 'בחרו מקצוע מהרשימה.' === $e( array( 'trade' => '' ) ) );
t( 'trade must be a key of the list', '' !== $e( array( 'trade' => 'astronaut' ) ) && '' !== $e( array( 'trade' => 'other' ) ) );
t( 'city 2 to 40', '' !== $e( array( 'city' => 'א' ) ) && '' !== $e( array( 'city' => str_repeat( 'א', 41 ) ) ) && '' === $e( array( 'city' => str_repeat( 'א', 40 ) ) ) );
t( 'bio may be empty', '' === $e( array( 'bio' => '' ) ) );
t( 'bio of 300 passes, 301 refused', '' === $e( array( 'bio' => str_repeat( 'א', 300 ) ) ) && '' !== $e( array( 'bio' => str_repeat( 'א', 301 ) ) ) );
t( 'bio with a link refused (forum detector)', false !== strpos( $e( array( 'bio' => 'ראו באתר שלי alona.co.il' ) ), 'קישור' ) );
t( 'bio with an email refused', false !== strpos( $e( array( 'bio' => 'כתבו לי alona@gmail.com' ) ), 'קישור' ) );
t( 'bio with a phone refused (forum detector)', false !== strpos( $e( array( 'bio' => 'התקשרו 050 123 4567' ) ), 'טלפון' ) );
t( 'phone optional with "message only"', '' === $e( array( 'phone' => '', 'how' => 'forum' ) ) );
t( 'phone needed to show phone and WhatsApp', '' !== $e( array( 'phone' => '', 'how' => 'phone' ) ) );
t( 'a bad phone refused', '' !== $e( array( 'phone' => '1234' ) ) );
t( 'video unchecked stays off', false === nlfm_validate( array_merge( $ok, array( 'video' => '0' ) ), $tr )['data']['video'] );
t( 'video missing = off (never switched on for someone who did not choose)', false === nlfm_validate( array_merge( $ok, array( 'video' => '' ) ), $tr )['data']['video'] );
t( 'a trade with one form keeps m', 'm' === nlfm_validate( array_merge( $ok, array( 'trade' => 'home_staging', 'form' => 'f' ) ), $tr )['data']['form'] );
t( 'how is phone or forum only', 'forum' === nlfm_validate( array_merge( $ok, array( 'how' => 'fax' ) ), $tr )['data']['how'] );
t( 'all messages Hebrew', 1 === preg_match( '/\p{Hebrew}/u', $e( array( 'name' => '' ) ) . $e( array( 'phone' => 'x' ) ) ) );

/* forms of a trade */
t( 'interior designer has two forms', nlfm_has_forms( $tr['interior_designer'] ) && 'מעצבת פנים' === nlfm_trade_label( $tr['interior_designer'], 'f' ) && 'מעצב פנים' === nlfm_trade_label( $tr['interior_designer'], 'm' ) );
t( 'home staging has one', ! nlfm_has_forms( $tr['home_staging'] ) );

/* status */
t( 'no approved post: waits', 'pending' === nlfm_status( 0, 'אלונה מור המרכז' ) );
t( 'an approved post and clean text: live', 'publish' === nlfm_status( 1, 'אלונה מור המרכז' ) );
t( 'flagged word waits', 'pending' === nlfm_status( 5, 'קזינו בתל אביב' ) );
t( 'latin flood waits', 'pending' === nlfm_status( 5, str_repeat( 'buy now cheap ', 4 ) ) );
t( 'a reviewed trade always waits', 'pending' === nlfm_status( 9, 'עורכת דין', 'review' ) );
t( 'the lawyer trade is marked review', 'review' === $tr['lawyer']['reg'] );

/* the profession label */
$known = array( 'kablan', 'interior_designer', 'architect', 'metavech' );
t( 'a key the directory knows is stored as the key', 'interior_designer' === nlfm_profession( 'interior_designer', 'f', $tr, $known ) );
t( 'an unknown trade stores its Hebrew label in the chosen form', 'הנדימנית' === nlfm_profession( 'handyman', 'f', $tr, $known ) && 'הנדימן' === nlfm_profession( 'handyman', 'm', $tr, $known ) );
t( 'the stored value of an unknown trade is not a machine token', 1 !== preg_match( '/^[a-z0-9_\-]+$/', nlfm_profession( 'painter', 'm', $tr, $known ) ) );
t( 'unknown key gives nothing', '' === nlfm_profession( 'zzz', 'm', $tr, $known ) );
t( 'design group tint (board 18 avatar)', array( '#E7E1FA', '#43308F' ) === nlfm_group_tint( 'design' ) && array( '#E3E6E8', '#22303A' ) === nlfm_group_tint( 'zzz' ) );

/* who sees what */
t( 'invitation: a pro without a card', nlfm_wants_invite( array( 'role_label' => 'pro', 'pro_id' => null, 'status' => 'ok' ) ) );
t( 'invitation: not with a card', ! nlfm_wants_invite( array( 'role_label' => 'pro', 'pro_id' => 12, 'status' => 'ok' ) ) );
t( 'invitation: not for a buyer', ! nlfm_wants_invite( array( 'role_label' => 'buyer', 'pro_id' => 0, 'status' => 'ok' ) ) );
t( 'invitation: not for a blocked member', ! nlfm_wants_invite( array( 'role_label' => 'pro', 'pro_id' => 0, 'status' => 'blocked' ) ) );
t( 'invitation: guests see nothing', ! nlfm_wants_invite( null ) && ! nlfm_wants_link( null ) );
t( 'the small link: another role, no card', nlfm_wants_link( array( 'role_label' => 'owner', 'pro_id' => 0, 'status' => 'ok' ) ) && nlfm_wants_link( array( 'role_label' => '', 'pro_id' => 0, 'status' => 'ok' ) ) );
t( 'the small link: not for a pro', ! nlfm_wants_link( array( 'role_label' => 'pro', 'pro_id' => 0, 'status' => 'ok' ) ) );

/* the call rule of 18.11.2026 */
t( 'reach: anyone with video on', '' === nlfc_can_reach( 7, 2, true, true, 0 ) );
t( 'reach: never oneself', 'self' === nlfc_can_reach( 2, 2, true, true ) );
t( 'reach: video off', 'video_off' === nlfc_can_reach( 7, 2, true, false ) );
t( 'reach: blocked', 'member' === nlfc_can_reach( 7, 2, false, true ) );
t( 'reach: 3 a day to the same person', '' === nlfc_can_reach( 7, 2, true, true, 2 ) && 'rate_pair' === nlfc_can_reach( 7, 2, true, true, 3 ) );
t( 'reach: no ids', 'with' === nlfc_can_reach( 0, 2, true, true ) && 'with' === nlfc_can_reach( 7, 0, true, true ) );
t( 'pair cap is 3', 3 === nlfc_pair_cap() );
$topic   = array( 'id' => 10, 'member_id' => 1, 'status' => 'live' );
$replies = array( array( 'id' => 101, 'member_id' => 2, 'status' => 'live' ), array( 'id' => 102, 'member_id' => 3, 'status' => 'pending' ),
	array( 'id' => 103, 'member_id' => 4, 'status' => 'live' ), array( 'id' => 104, 'member_id' => 5, 'status' => 'live' ), array( 'id' => 105, 'member_id' => 2, 'status' => 'live' ) );
$video = array( 1 => true, 2 => true, 3 => true, 4 => false, 5 => true, 6 => true );
$okm   = array( 1 => true, 2 => true, 3 => true, 4 => true, 5 => false, 6 => true );
t( 'old path still works: author calls a replier', '' === nlfc_can_call_open( $topic, $replies, 1, 2, $video, $okm ) );
t( 'new: two repliers may call each other', 'pair' === nlfc_can_call( $topic, $replies, 2, 4, array( 4 => true ) + $video, $okm ) && '' === nlfc_can_call_open( $topic, $replies, 2, 1, $video, $okm ) && '' === nlfc_can_call_open( $topic, $replies, 4, 2, $video, $okm ) );
t( 'new: someone who never wrote may call the author', '' === nlfc_can_call_open( $topic, $replies, 6, 1, $video, $okm ) );
t( 'new: someone who never wrote may call a replier', '' === nlfc_can_call_open( $topic, $replies, 6, 2, $video, $okm ) );
t( 'new: not someone who did not write in it', 'nowrote' === nlfc_can_call_open( $topic, $replies, 1, 6, $video, $okm ) );
t( 'new: a pending reply does not count', 'nowrote' === nlfc_can_call_open( $topic, $replies, 1, 3, $video, $okm ) );
t( 'new: video off refused', 'video_off' === nlfc_can_call_open( $topic, $replies, 6, 4, $video, $okm ) );
t( 'new: blocked refused', 'member' === nlfc_can_call_open( $topic, $replies, 6, 5, $video, $okm ) );
t( 'new: oneself refused', 'self' === nlfc_can_call_open( $topic, $replies, 2, 2, $video, $okm ) );
t( 'new: hidden discussion refused', 'topic' === nlfc_can_call_open( array( 'status' => 'hidden' ) + $topic, $replies, 6, 1, $video, $okm ) );
t( 'pair cap on both paths', 'rate_pair' === nlfc_can_call_open( $topic, $replies, 1, 2, $video, $okm, 3 ) && 'rate_pair' === nlfc_can_call_open( $topic, $replies, 6, 2, $video, $okm, 3 ) );
$p = nlfc_page_pills( $topic, $replies, 0, $video, $okm );
t( 'pills for a guest: the author and replier 2 (video on), not 4 (off) or 5 (blocked)', array( 1, 2 ) === array_column( $p, 'with' ) );
t( 'pills: every answer of the author of it', array( 101, 105 ) === $p[1]['replies'] && 105 === $p[1]['reply'] && 0 === $p[1]['op'] );
t( 'pills: the opening message', 1 === $p[0]['op'] && array() === $p[0]['replies'] );
t( 'pills: never on one\'s own answers', array( 1 ) === array_column( nlfc_page_pills( $topic, $replies, 2, $video, $okm ), 'with' ) );
t( 'pills: none on a hidden discussion', array() === nlfc_page_pills( array( 'status' => 'hidden' ) + $topic, $replies, 0, $video, $okm ) );
foreach ( array( 'nowrote', 'card', 'rate_pair' ) as $c ) { t( "call message for $c is Hebrew", 1 === preg_match( '/\p{Hebrew}/u', nlfc_msg( $c ) ) && 'משהו השתבש. נסו שוב.' !== nlfc_msg( $c ) ); }
list( $s, $b ) = nlfc_mail_parts( 'דני כהן', 'אלונה מור', 'https://nad-lan.co.il/professionals/x/#call=abcdefghijkl', 'https://nad-lan.co.il/?nlfc_stop=x', true );
t( 'card call mail: subject', 'דני כהן מזמין אתכם לשיחת וידאו מהכרטיס שלכם' === $s );
t( 'card call mail: no discussion wording, the link, not recorded', false === strpos( $b, 'הדיון' ) && false !== strpos( $b, '#call=abcdefghijkl' ) && false !== strpos( $b, 'השיחה לא מוקלטת' ) );
list( $s2 ) = nlfc_mail_parts( 'דני', 'שיפוץ', 'l', 's' );
t( 'discussion call mail unchanged', 'דני מזמין אתכם לשיחת וידאו על שיפוץ' === $s2 );

/* house rules on the files */
$php    = (string) file_get_contents( __DIR__ . '/../inc/pro-forum-card.php' );
$js     = (string) file_get_contents( __DIR__ . '/../assets/proforum/card.js' );
$css    = (string) file_get_contents( __DIR__ . '/../assets/proforum/card.css' );
$render = (string) file_get_contents( __DIR__ . '/../inc/pro-forum-render.php' );
$forum  = (string) file_get_contents( __DIR__ . '/../inc/pro-forum.php' );
$cjs    = (string) file_get_contents( __DIR__ . '/../assets/proforum/call.js' );
$cphp   = (string) file_get_contents( __DIR__ . '/../inc/pro-forum-call.php' );
t( 'one require line at the end of pro-forum.php', 1 === substr_count( $forum, "require_once __DIR__ . '/pro-forum-card.php'" ) );
foreach ( array( 'nlf_member_bar_extra', 'nlf_before_replyform', 'nlf_owner_box_extra', 'nlf_card_content', 'nlf_card_top' ) as $hk ) {
	t( "hook $hk offered by render and used by the module", false !== strpos( $render, "apply_filters( '$hk'" ) && false !== strpos( $php, "add_filter( '$hk'" ) );
}
t( 'the home invitation uses the forum\'s notices hook', false !== strpos( $php, "add_filter( 'nlf_home_notices'" ) );
t( 'no 403', false === strpos( $php, '403' ) );
t( 'every write through nlf_guard post', false !== strpos( $php, "nlf_guard( \$q, 'post' )" ) );
t( 'no redirects, no robots, no indexing', 0 === preg_match( '/wp_redirect|wp_safe_redirect|noindex|wp_robots|robots_txt|indexing|Indexing/', $php ) );
t( 'no register mark wording', false === strpos( $php, 'מאומת' ) && false === strpos( $php, 'nadlan_dir_registry_verified' ) );
t( 'source forum_member', false !== strpos( $php, "define( 'NLFM_SOURCE', 'forum_member' )" ) );
t( 'SQL only prepared', 1 === substr_count( $php, '$wpdb->query(' ) && false !== strpos( $php, '$wpdb->query( $wpdb->prepare(' ) );
t( 'the mail links act on a POST press', false !== strpos( $php, "isset( \$_POST['nlfm_confirm'] )" ) && false !== strpos( $php, '<form method="post"' ) );
t( 'two creations a day per member and per IP', false !== strpos( $php, "nlf_rl( 'card_new', 2, DAY_IN_SECONDS" ) && false !== strpos( $php, "nlf_rl( 'card_new_ip', 2, DAY_IN_SECONDS )" ) );
t( 'unique handles', false !== strpos( $php, "'nlf-mycard'" ) && 0 === preg_match( "/wp_enqueue_(style|script)\\( '(nlf|nlfc|nlf-call|nlf-social)'/", $php ) );
t( 'sheet printed before the footer scripts', false !== strpos( $php, "}, 6 );" ) );
t( 'js: people\'s text only through textContent', false === strpos( $js, 'innerHTML' ) && false === strpos( $js, 'insertAdjacentHTML' ) );
t( 'call.js: innerHTML still only for the constant icons', 1 === substr_count( $cjs, 'innerHTML' ) );
t( 'no emoji', 0 === preg_match( '/[\x{1F300}-\x{1FAFF}\x{2600}-\x{27BF}]/u', $js . $css . $php ) );
t( 'no long dashes', 0 === preg_match( '/[\x{2013}\x{2014}]/u', $js . $css . $php ) );
t( 'no wheel or touch capture', 0 === preg_match( "/addEventListener\\(\\s*'(wheel|touchmove|touchstart)'/", $js ) );
t( 'board 18 colours and faces', false !== strpos( $css, '#B0144F' ) && false !== strpos( $css, '#2F6F86' ) && false !== strpos( $css, '#101820' ) && false !== strpos( $css, 'Rubik' ) && false !== strpos( $css, 'Assistant' ) );
t( 'board 18 sizes: form 48 inputs, 54 button, 64 call button, 50 contact buttons, 44 pill', false !== strpos( $css, 'height:48px' ) && false !== strpos( $css, 'height:54px' ) && false !== strpos( $css, 'min-height:64px' ) && false !== strpos( $css, 'height:50px' ) && false !== strpos( $css, 'height:44px' ) );
t( 'pulse ring off under reduced motion', false !== strpos( $css, '@keyframes nlfm-ring' ) && false !== strpos( $css, 'prefers-reduced-motion:reduce' ) );
t( 'white on raspberry forced', false !== strpos( $css, 'background:#B0144F !important;color:#FFFFFF !important' ) );
foreach ( array( 'רוצים שהפרטים שלכם יופיעו ושיפנו אליכם?', 'חינם כרגע', 'פתיחת כרטיס', 'דקה אחת, בלי תשלום ובלי סיסמה', 'הכרטיס שלי', 'אפשר לשנות בכל רגע', 'השם שיופיע',
	'עיר או אזור', 'מה אתם עושים, בשתי שורות', 'טלפון (לא חובה)', 'איך פונים אליכם', 'טלפון, וואטסאפ ושיחת וידאו', 'רק בהודעה ובשיחת וידאו דרך הפורום',
	'אפשר לפנות אליי בשיחת וידאו', 'פתיחת הכרטיס', 'בדפדפן, בלי התקנה. אפשר להראות תוכנית ולסמן עליה יחד.', 'הפנייה מגיעה ישר אל ', 'הכרטיס יעלה אחרי בדיקה קצרה', 'אני בעל מקצוע', 'עריכת הכרטיס' ) as $copy ) {
	t( "copy: $copy", false !== strpos( $php, $copy ) );
}
t( 'video checkbox checked by default', false !== strpos( $php, 'name="video" value="1" checked' ) );
t( 'call: room carries a card', false !== strpos( $cphp, "'card' => (int) \$ctx['card'], 'by' => \$mid" ) );
t( 'call: pair counter hit on a new room', false !== strpos( $cphp, "nlfc_rl_hit( 'pair', 'm' . \$mid . 'w' . \$with" ) );
t( 'call.js: a card button and the pending call after entry', false !== strpos( $cjs, '[data-nlf-callcard]' ) && false !== strpos( $cjs, 'takePending()' ) );

echo "\n$pass passed, $fail failed\n";
exit( $fail ? 1 : 0 );
