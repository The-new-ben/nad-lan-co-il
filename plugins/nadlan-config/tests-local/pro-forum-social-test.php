<?php
/**
 * Plain PHP CLI test of the forum's social layer (no WordPress): php tests-local/pro-forum-social-test.php
 * Loads the forum's pure part (NLF_PURE_ONLY) and then part 1 of inc/pro-forum-social.php (NLFS_PURE_ONLY), plus static
 * checks on the module's files. Exit code 0 = all passed.
 */
define( 'ABSPATH', __DIR__ . '/' );
define( 'NLF_PURE_ONLY', true );
define( 'NLFS_PURE_ONLY', true );
require __DIR__ . '/../inc/pro-forum.php';
require __DIR__ . '/../inc/pro-forum-social.php';

$pass = 0; $fail = 0;
function t( $name, $cond ) {
	global $pass, $fail;
	if ( $cond ) { $pass++; echo "ok   $name\n"; } else { $fail++; echo "FAIL $name\n"; }
}

/* the five reactions (board 11) */
$k = nlfs_kinds();
t( 'five kinds in board order', array( 'pargen', 'useful', 'pro', 'nice', 'thanks' ) === array_keys( $k ) );
t( 'labels', array( 'מפרגן', 'מועיל', 'מקצועי', 'יפה', 'תודה' ) === array_column( array_values( $k ), 0 ) );
t( 'board pill tints', '#FBE9F0' === $k['pargen'][1] && '#8C0F3E' === $k['pargen'][2] && '#DCEFE3' === $k['useful'][1] && '#E7E1FA' === $k['nice'][1] && '#F2F4F5' === $k['thanks'][1] );
t( 'board dots raspberry, sea, green', '#B0144F' === $k['pargen'][3] && '#2F6F86' === $k['pro'][3] && '#1B4D33' === $k['useful'][3] );
t( 'no negative kind', ! preg_match( '/לא|רע|גרוע|down|dislike/u', implode( ' ', array_merge( array_keys( $k ), array_column( array_values( $k ), 0 ) ) ) ) );
t( 'kind_ok', nlfs_kind_ok( 'nice' ) && ! nlfs_kind_ok( 'angry' ) && ! nlfs_kind_ok( array() ) && ! nlfs_kind_ok( '' ) );
t( 'react: new', 'pro' === nlfs_react_next( '', 'pro' ) );
t( 'react: change', 'nice' === nlfs_react_next( 'pro', 'nice' ) );
t( 'react: same again removes', '' === nlfs_react_next( 'pro', 'pro' ) );
t( 'react: thanks again removes', '' === nlfs_react_next( 'thanks', 'thanks' ) );
t( 'react: unknown kind does nothing', '' === nlfs_react_next( 'pro', 'bad' ) );

/* old thanks rows count as "תודה"; a member counts once */
$th = array( array( 'member_id' => 1, 'target_type' => 'reply', 'target_id' => 7 ), array( 'member_id' => 2, 'target_type' => 'reply', 'target_id' => 7 ), array( 'member_id' => 3, 'target_type' => 'topic', 'target_id' => 7 ) );
$rx = array( array( 'member_id' => 4, 'target_type' => 'reply', 'target_id' => 7, 'kind' => 'pargen' ), array( 'member_id' => 2, 'target_type' => 'reply', 'target_id' => 7, 'kind' => 'pro' ),
	array( 'member_id' => 5, 'target_type' => 'reply', 'target_id' => 7, 'kind' => 'evil' ) );
$mg = nlfs_merge( $th, $rx );
t( 'merge: thanks rows are "thanks"', 'thanks' === $mg['reply|7'][1] );
t( 'merge: topic and reply apart', array( 3 => 'thanks' ) === $mg['topic|7'] );
t( 'merge: a member with both counts once, his reaction wins', 'pro' === $mg['reply|7'][2] && 3 === count( $mg['reply|7'] ) );
t( 'merge: an unknown kind is dropped', ! isset( $mg['reply|7'][5] ) );
$s = nlfs_summary( $mg['reply|7'] );
t( 'summary total', 3 === $s['total'] );
t( 'summary by kind', array( 'pargen' => 1, 'pro' => 1, 'thanks' => 1 ) === $s['by'] );
t( 'summary tie keeps board order', array( 'pargen', 'pro', 'thanks' ) === $s['top'] );
$s2 = nlfs_summary( array( 1 => 'nice', 2 => 'nice', 3 => 'useful', 4 => 'pargen', 5 => 'pro', 6 => 'thanks', 7 => 'useful', 8 => 'nice' ) );
t( 'summary most first', array( 'nice', 'useful', 'pargen' ) === $s2['top'] && 8 === $s2['total'] );
t( 'summary of nothing = zero, no top', 0 === nlfs_summary( array() )['total'] && array() === nlfs_summary( array() )['top'] );
t( 'zero prints no words', '' === nlfs_summary_words( nlfs_summary( array() ) ) );
t( 'words for a screen reader', 'פרגונים: יפה 3, מועיל 2, מפרגן 1, מקצועי 1, תודה 1' === substr( nlfs_summary_words( $s2 ), strlen( '8 ' ) ) );

/* פרגון */
$ok = array( 'from' => 1, 'to' => 2, 'approved' => 2, 'to_ok' => true, 'already' => false );
$good = 'עבדנו יחד על שיפוץ מטבח. מדויק וזמין.';
t( 'rels: three, stated', array( 'together' => 'עבדנו יחד', 'client' => 'הייתי לקוח', 'known' => 'מכיר מקצועית' ) === nlfs_rels() );
t( 'kudos ok', '' === nlfs_kudos_error( $good, 'together', $ok ) );
t( 'kudos to self refused', '' !== nlfs_kudos_error( $good, 'together', array_merge( $ok, array( 'to' => 1 ) ) ) );
t( 'kudos needs 2 approved posts', false !== strpos( nlfs_kudos_error( $good, 'together', array_merge( $ok, array( 'approved' => 1 ) ) ), 'שתי הודעות' ) );
t( 'kudos one per pair', false !== strpos( nlfs_kudos_error( $good, 'together', array_merge( $ok, array( 'already' => true ) ) ), 'אחד' ) );
t( 'kudos to a non-member refused', '' !== nlfs_kudos_error( $good, 'together', array_merge( $ok, array( 'to_ok' => false ) ) ) );
t( 'kudos needs a relationship', '' !== nlfs_kudos_error( $good, 'friend', $ok ) && '' !== nlfs_kudos_error( $good, '', $ok ) );
t( 'kudos 9 characters refused', '' !== nlfs_kudos_error( 'קצר מדיי', 'known', $ok ) );
t( 'kudos 10 characters ok', '' === nlfs_kudos_error( 'אחלה בנאדם', 'known', $ok ) && 10 === nlf_len( 'אחלה בנאדם' ) );
t( 'kudos 240 ok, 241 refused', '' === nlfs_kudos_error( str_repeat( 'א', 240 ), 'known', $ok ) && '' !== nlfs_kudos_error( str_repeat( 'א', 241 ), 'known', $ok ) );
t( 'kudos link refused', false !== strpos( nlfs_kudos_error( 'מומלץ מאוד, ראו www.site.co.il', 'known', $ok ), 'קישור' ) );
t( 'kudos email refused', '' !== nlfs_kudos_error( 'כתבו לו dan@mail.com ממליץ', 'known', $ok ) );
t( 'kudos phone refused', false !== strpos( nlfs_kudos_error( 'מומלץ מאוד 054-1234567', 'known', $ok ), 'טלפון' ) );
t( 'kudos clean = no flag', '' === nlfs_kudos_flag( $good ) );
t( 'kudos with a negative word waits', 'negative' === nlfs_kudos_flag( 'לא ממליץ על העבודה שלו בכלל' ) );
t( 'kudos with a spam word waits', '' !== nlfs_kudos_flag( 'הכי טוב בקזינו של העיר' ) );

/* skills */
t( 'skill ok', '' === nlfs_skill_error( 'שמאות פינוי בינוי', array( 'היטל השבחה' ) ) );
t( 'skill 1 char refused', '' !== nlfs_skill_error( 'א', array() ) );
t( 'skill 2 chars ok', '' === nlfs_skill_error( 'אב', array() ) );
t( 'skill 41 refused', '' !== nlfs_skill_error( str_repeat( 'ב', 41 ), array() ) && '' === nlfs_skill_error( str_repeat( 'ב', 40 ), array() ) );
t( 'skill sixth refused', false !== strpos( nlfs_skill_error( 'חדשה', array( 'א1', 'א2', 'א3', 'א4', 'א5' ) ), '5' ) );
t( 'skill duplicate (spaces, case, marks) refused', '' !== nlfs_skill_error( 'היטל  השבחה!', array( 'היטל השבחה' ) ) && '' !== nlfs_skill_error( 'Bank Loans', array( 'bank loans' ) ) );
t( 'skill link or phone refused', '' !== nlfs_skill_error( 'www.x.com', array() ) && '' !== nlfs_skill_error( '0541234567', array() ) );
t( 'trade: linked card', nlfs_has_trade( array( 'pro_id' => 5, 'role_label' => '', 'trade' => '' ) ) );
t( 'trade: chosen from the list', nlfs_has_trade( array( 'pro_id' => null, 'role_label' => 'pro', 'trade' => 'kablan' ) ) );
t( 'trade: a buyer has none', ! nlfs_has_trade( array( 'pro_id' => 0, 'role_label' => 'buyer', 'trade' => '' ) ) && ! nlfs_has_trade( null ) );
t( 'trade: "pro" without a trade has none', ! nlfs_has_trade( array( 'pro_id' => 0, 'role_label' => 'pro', 'trade' => '' ) ) );

/* the response badge: 5+ answers, 80% within a day */
$h = 3600; $d = 86400;
t( 'badge counts', array( 3, 2 ) === nlfs_badge_counts( array( array( 0, $h ), array( 0, $d ), array( 0, $d + 1 ) ) ) );
t( 'badge: exactly 24 hours counts as within a day', array( 1, 1 ) === nlfs_badge_counts( array( array( 100, 100 + $d ) ) ) );
t( 'badge: 4 fast answers are not enough', ! nlfs_badge_earned( 4, 4 ) );
t( 'badge: 5 of 5', nlfs_badge_earned( 5, 5 ) );
t( 'badge: 4 of 5 = 80% earns', nlfs_badge_earned( 5, 4 ) );
t( 'badge: 3 of 5 does not', ! nlfs_badge_earned( 5, 3 ) );
t( 'badge: 7 of 9 (77%) does not, 8 of 10 does', ! nlfs_badge_earned( 9, 7 ) && nlfs_badge_earned( 10, 8 ) );
t( 'badge: nothing earns nothing', ! nlfs_badge_earned( 0, 0 ) );

/* tags on a finished work */
$tg = array( 'kind' => 'work', 'author' => 1, 'me' => 1, 'tagged' => 2, 'tagged_ok' => true, 'count' => 0, 'state' => '' );
t( 'tag ok', '' === nlfs_tag_error( $tg ) );
t( 'tag only on "work"', '' !== nlfs_tag_error( array_merge( $tg, array( 'kind' => 'question' ) ) ) );
t( 'tag only by the author', '' !== nlfs_tag_error( array_merge( $tg, array( 'me' => 3 ) ) ) );
t( 'tag not yourself', '' !== nlfs_tag_error( array_merge( $tg, array( 'tagged' => 1 ) ) ) );
t( 'tag a member only', '' !== nlfs_tag_error( array_merge( $tg, array( 'tagged_ok' => false ) ) ) );
t( 'tag up to 4', '' === nlfs_tag_error( array_merge( $tg, array( 'count' => 3 ) ) ) && '' !== nlfs_tag_error( array_merge( $tg, array( 'count' => 4 ) ) ) );
t( 'tag twice refused', '' !== nlfs_tag_error( array_merge( $tg, array( 'state' => 'on' ) ) ) );
t( 'tag after he removed himself refused', false !== strpos( nlfs_tag_error( array_merge( $tg, array( 'state' => 'off_member' ) ) ), 'בעצמו' ) );
t( 'tag again after the author removed it ok', '' === nlfs_tag_error( array_merge( $tg, array( 'state' => 'off_author' ) ) ) );

/* WhatsApp: no number, the person picks the recipient */
$wt = nlfs_wa_text( ' מדויק וזמין ', 'רונית ל.', 'אבי ב.', 'https://nad-lan.co.il/forum/#nlfs-m4' );
t( 'wa text holds the sentence, both names and the link', 0 === strpos( $wt, '"מדויק וזמין"' ) && false !== strpos( $wt, 'רונית ל. על אבי ב.' ) && false !== strpos( $wt, 'https://nad-lan.co.il/forum/#nlfs-m4' ) );
$wu = nlfs_wa_url( $wt );
t( 'wa url has no phone number', 0 === strpos( $wu, 'https://wa.me/?text=' ) );
t( 'wa url is encoded', false === strpos( $wu, ' ' ) && false === strpos( $wu, '"' ) && rawurldecode( substr( $wu, strlen( 'https://wa.me/?text=' ) ) ) === $wt );
t( 'first name', 'אבי' === nlfs_first( 'אבי ב.' ) && 'דנה' === nlfs_first( 'דנה' ) );

/* static checks on the module's files */
$php = file_get_contents( __DIR__ . '/../inc/pro-forum-social.php' );
$js  = file_get_contents( __DIR__ . '/../assets/proforum/social.js' );
$css = file_get_contents( __DIR__ . '/../assets/proforum/social.css' );
$rnd = file_get_contents( __DIR__ . '/../inc/pro-forum-render.php' );
$core = file_get_contents( __DIR__ . '/../inc/pro-forum.php' );
$all = $php . $js . $css;
t( 'no long dashes', false === strpos( $all, '—' ) && false === strpos( $all, '–' ) );
t( 'no banned words', ! preg_match( '/פלטפורמה|המערכת|אינטראקטיבי|אטלס|נחבר אתכם/u', $all ) );
t( 'no emoji', ! preg_match( '/[\x{1F300}-\x{1FAFF}\x{2600}-\x{27BF}]/u', $all ) );
t( 'no innerHTML / eval in js', ! preg_match( '/innerHTML|outerHTML|insertAdjacentHTML|\beval\s*\(|new Function|document\.write/', $js ) );
t( 'js sends the forum nonce and solves the challenge', false !== strpos( $js, "'X-NLF-Nonce'" ) && false !== strpos( $js, 'crypto.subtle.digest' ) );
t( 'js never opens wa.me with a number', ! preg_match( '/wa\.me\/\d/', $js . $php ) );
t( 'no 403 / 401, errors are 400', ! preg_match( "/'status' => 40[13]/", $php ) && false !== strpos( $php, "'status' => 400" ) );
t( 'routes hidden from the public index', substr_count( $php, "'show_in_index' => false" ) >= 1 && false === strpos( $php, "'show_in_index' => true" ) );
t( 'every write route goes through nlfs_guard', 9 === substr_count( $php, "nlfs_guard( \$q, 'light' )" ) + substr_count( $php, "nlfs_guard( \$q, 'post' )" ) );
t( 'no redirects, no robots changes', ! preg_match( '/wp_redirect\s*\(|wp_safe_redirect\s*\(|header\(\s*[\'"]Location|noindex|nofollow|\b30[12]\b/i', $all ) );
t( 'no mail to members (only the owner gets pending items)', 1 === substr_count( $php, 'nlf_mail(' ) && false !== strpos( $php, 'nlf_mail( nlf_admin_to()' ) );
t( 'own DB version, the nlf_install pattern', false !== strpos( $php, "define( 'NLFS_DB', '1' )" ) && false !== strpos( $php, "'nlfs_install_wait'" ) );
t( 'thanks_count recounted from the thanks table as the core does', false !== strpos( $php, "SELECT COUNT(*) FROM \$tt WHERE target_type = %s AND target_id = %d" ) );
t( 'css: dark surfaces carry !important colours', false !== strpos( $css, '.nlfs-kudo-q{' ) && preg_match( '/\.nlfs-kudo-alt\{[^}]*color:#FFFFFF !important/', $css ) );
t( 'css: links styled as buttons have no underline', preg_match( '/text-decoration:none !important/', $css ) );
t( 'css: nothing pushed off-screen', ! preg_match( '/(left|right)\s*:\s*-\d{3,}px/', $css ) );
t( 'js under 24 KB', strlen( $js ) < 24576 );
t( 'render: six hook points', 6 === count( array_unique( array_filter( array( 'nlf_topic_actions', 'nlf_reply_actions', 'nlf_name_extra', 'nlf_topic_after_body', 'nlf_home_notices', 'nlf_card_member_block' ), function ( $h ) use ( $rnd ) { return false !== strpos( $rnd, "apply_filters( '$h'" ); } ) ) ) );
t( 'render: the old thanks button stays as the default', 2 === substr_count( $rnd, 'data-nlf-thank=' ) );
t( 'core: the module loads by one line at the end', 1 === substr_count( $core, "require_once __DIR__ . '/pro-forum-social.php'" ) );
t( 'social filters registered', 6 === preg_match_all( "/add_filter\( 'nlf_(topic_actions|reply_actions|name_extra|topic_after_body|home_notices|card_member_block)'/", $php ) );

echo "\n$pass passed, $fail failed\n";
exit( $fail ? 1 : 0 );
