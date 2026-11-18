<?php
/**
 * nad-lan professionals' forum: a member opens his OWN professional card, free (18.11.2026, Claude Design board 18
 * "MyCard": A the invitation, B the form sheet, C the opened card with the large video button, D the video pill by an answer).
 *
 * Why: a real interior designer joined, answered twice and wrote that there was nowhere to add her details. Cards existed only
 * for people imported from public registers (who claim them) or paid tiers; designers are in no register.
 * Plan: docs/research/2026-11-18-pro-membership/PLAN-HE.md, steps 1 and 2 only.
 *
 * Loaded by ONE line at the end of inc/pro-forum.php:
 *   if ( file_exists( __DIR__ . '/pro-forum-card.php' ) ) { require_once __DIR__ . '/pro-forum-card.php'; }
 * It fills hook points of inc/pro-forum-render.php (nlf_home_notices, nlf_member_bar_extra, nlf_before_replyform,
 * nlf_owner_box_extra, nlf_card_content, nlf_card_top). It never edits inc/professional-profile.php or inc/directory.php: the
 * card page is reached through the forum's own the_content filter (priority 40), a body class and CSS.
 *
 * Data: no new table and no new column. A card is a `nadlan_professional` post with the meta the card page already reads
 * (profession, city, bio, nl_name_he, nl_gender, phone only when the member chose to show it) plus source = forum_member,
 * nl_forum_member (the member id), nl_forum_trade (the trade key), _nl_email (the member's own verified address, so the
 * forum's entry route keeps the link on the next sign-in), _nlfm_phone (the number as typed, kept for editing) and
 * nl_forum_contact (phone | forum). The member row gets pro_id, role_label 'pro', trade and show_phone; the call switch
 * (nadlan_forum_callpref.video_on) follows the checkbox.
 *
 * Rules: only the member who fills the form gets a card; a card imported from a register is never touched, linked or shown
 * here. Every write goes through nlf_guard ('post'); errors are HTTP 400 in Hebrew. No redirects, no robots changes, nothing
 * asks a search engine to index. A card goes live at once only for a member with an approved post and clean text; otherwise
 * it waits for the site owner, who gets one mail with signed approve / reject links that act only on a POST press.
 * No long dashes in this file.
 */

if ( ! defined( 'ABSPATH' ) && ! defined( 'NLFM_PURE_ONLY' ) ) { exit; }
if ( defined( 'NLFM_LOADED' ) ) { return; }
define( 'NLFM_LOADED', true );
define( 'NLFM_SOURCE', 'forum_member' );

/* =========================================================================================================
 * 1. Pure functions (no WordPress). tests-local/pro-forum-card-test.php loads only this part (NLFM_PURE_ONLY), after the
 *    forum's own pure part (nlf_len, nlf_text_norm, nlf_has_link, nlf_has_phone, nlf_first_post_flag).
 * ======================================================================================================= */

function nlfm_months() {
	return array( 1 => 'ינואר', 'פברואר', 'מרץ', 'אפריל', 'מאי', 'יוני', 'יולי', 'אוגוסט', 'ספטמבר', 'אוקטובר', 'נובמבר', 'דצמבר' );
}

/** "חבר בפורום מאז נובמבר 2026 · הפרטים נמסרו על ידו" (female form when chosen); '' without a valid time */
function nlfm_since_line( $ts, $female ) {
	$ts = (int) $ts;
	if ( $ts <= 0 ) { return ''; }
	$mo = nlfm_months()[ (int) gmdate( 'n', $ts ) ];
	return ( $female ? 'חברה בפורום מאז ' : 'חבר בפורום מאז ' ) . $mo . ' ' . gmdate( 'Y', $ts ) . ' · הפרטים נמסרו על ' . ( $female ? 'ידה' : 'ידו' );
}

/** the first word of a name ("אלונה מור" -> "אלונה") */
function nlfm_first_name( $name ) {
	$w = preg_split( '/\s+/u', trim( (string) $name ) );
	return isset( $w[0] ) && '' !== $w[0] ? (string) $w[0] : (string) $name;
}

/** digits of a phone; '' when it is not 9 to 13 digits */
function nlfm_phone_norm( $s ) {
	$s = (string) $s;
	if ( preg_match( '/[^\d\s\-+().]/u', $s ) ) { return ''; }
	$d = preg_replace( '/\D+/', '', $s );
	$n = strlen( $d );
	return ( $n >= 9 && $n <= 13 ) ? $d : '';
}

/** the label of a trade in the chosen form ('f' female, anything else male) */
function nlfm_trade_label( array $trade, $form ) { return 'f' === $form ? (string) $trade['female'] : (string) $trade['label']; }

/** true when the male and female forms differ (then the form shows the two chips) */
function nlfm_has_forms( array $trade ) { return (string) $trade['label'] !== (string) $trade['female']; }

/**
 * Checks the form. $in keys: name, trade, form, city, bio, phone, how, video. $trades = nadlan_forum_trades().
 * Returns array( 'err' => Hebrew message ) or array( 'data' => clean values ).
 */
function nlfm_validate( array $in, array $trades ) {
	$name  = nlf_text_norm( (string) ( $in['name'] ?? '' ), true );
	$trade = preg_replace( '/[^a-z0-9_]/', '', strtolower( (string) ( $in['trade'] ?? '' ) ) );
	$form  = 'f' === (string) ( $in['form'] ?? '' ) ? 'f' : 'm';
	$city  = nlf_text_norm( (string) ( $in['city'] ?? '' ), true );
	$bio   = nlf_text_norm( (string) ( $in['bio'] ?? '' ) );
	$raw   = trim( (string) ( $in['phone'] ?? '' ) );
	$how   = 'phone' === (string) ( $in['how'] ?? '' ) ? 'phone' : 'forum';
	$video = in_array( (string) ( $in['video'] ?? '' ), array( '1', 'true', 'on' ), true );
	if ( nlf_len( $name ) < 2 || nlf_len( $name ) > 60 ) { return array( 'err' => 'כתבו שם, 2 עד 60 תווים.' ); }
	if ( nlf_has_link( $name ) || nlf_has_phone( $name ) ) { return array( 'err' => 'בשם אי אפשר לכתוב קישור או מספר טלפון.' ); }
	if ( '' === $trade || ! isset( $trades[ $trade ] ) ) { return array( 'err' => 'בחרו מקצוע מהרשימה.' ); }
	if ( ! nlfm_has_forms( $trades[ $trade ] ) ) { $form = 'm'; }
	if ( nlf_len( $city ) < 2 || nlf_len( $city ) > 40 ) { return array( 'err' => 'כתבו עיר או אזור, 2 עד 40 תווים.' ); }
	if ( nlf_has_link( $city ) || nlf_has_phone( $city ) ) { return array( 'err' => 'בעיר אי אפשר לכתוב קישור או מספר טלפון.' ); }
	if ( nlf_len( $bio ) > 300 ) { return array( 'err' => 'התיאור ארוך מדי. עד 300 תווים.' ); }
	if ( nlf_has_link( $bio ) ) { return array( 'err' => 'בתיאור אי אפשר לכתוב קישור או כתובת מייל.' ); }
	if ( nlf_has_phone( $bio ) ) { return array( 'err' => 'בתיאור אי אפשר לכתוב מספר טלפון. יש לו שדה משלו.' ); }
	$phone = '';
	if ( '' !== $raw ) {
		$phone = nlfm_phone_norm( $raw );
		if ( '' === $phone ) { return array( 'err' => 'מספר הטלפון לא נראה תקין. 9 עד 13 ספרות.' ); }
	}
	if ( 'phone' === $how && '' === $phone ) { return array( 'err' => 'כדי להציג טלפון ווואטסאפ, כתבו מספר טלפון. אפשר גם לבחור פנייה רק דרך הפורום.' ); }
	return array( 'data' => array( 'name' => $name, 'trade' => $trade, 'form' => $form, 'city' => $city, 'bio' => $bio, 'phone' => $phone,
		'phone_raw' => '' !== $phone ? mb_substr( preg_replace( '/[^\d\s\-+()]/', '', $raw ), 0, 20 ) : '', 'how' => $how, 'video' => $video ) );
}

/**
 * The status of a new or edited card. Live at once only for a member with at least 1 approved post whose texts pass the
 * forum's first-post flags; a trade the owner reviews ('review', real-estate lawyers) always waits. Else 'pending'.
 */
function nlfm_status( $approved_posts, $text, $reg = '' ) {
	if ( 'review' === (string) $reg ) { return 'pending'; }
	return ( (int) $approved_posts >= 1 && '' === nlf_first_post_flag( (string) $text ) ) ? 'publish' : 'pending';
}

/**
 * The value stored in the card's `profession` meta. A trade whose key the directory knows ($known) keeps that key, and the
 * directory's label function prints it in the stored gender (nl_gender). A trade the directory does not know stores its own
 * Hebrew label in the chosen form: nadlan_dir_prof_meta() passes a Hebrew (non machine) value through as the label.
 */
function nlfm_profession( $key, $form, array $trades, array $known ) {
	if ( in_array( (string) $key, $known, true ) ) { return (string) $key; }
	return isset( $trades[ $key ] ) ? nlfm_trade_label( $trades[ $key ], $form ) : '';
}

/** the avatar tint of a trade group (the forum's group tints, nlf_emb_author) */
function nlfm_group_tint( $group ) {
	$g = array( 'build' => array( '#DCE6F2', '#1D3B66' ), 'design' => array( '#E7E1FA', '#43308F' ), 'plan' => array( '#DCEFE3', '#1B4D33' ),
		'systems' => array( '#DDE3FB', '#1E2F8F' ), 'deal' => array( '#D9EEF0', '#0E4A57' ), 'living' => array( '#E3E6E8', '#22303A' ) );
	return isset( $g[ $group ] ) ? $g[ $group ] : array( '#E3E6E8', '#22303A' );
}

/** who sees the invitation: a member who chose "בעל מקצוע" and has no card */
function nlfm_wants_invite( $m ) { return is_array( $m ) && 'pro' === (string) ( $m['role_label'] ?? '' ) && (int) ( $m['pro_id'] ?? 0 ) <= 0 && 'ok' === (string) ( $m['status'] ?? 'ok' ); }

/** who sees the small "אני בעל מקצוע" link: a member with another role and no card */
function nlfm_wants_link( $m ) { return is_array( $m ) && 'pro' !== (string) ( $m['role_label'] ?? '' ) && (int) ( $m['pro_id'] ?? 0 ) <= 0 && 'ok' === (string) ( $m['status'] ?? 'ok' ); }

if ( defined( 'NLFM_PURE_ONLY' ) ) { return; }

/* =========================================================================================================
 * 2. Reading
 * ======================================================================================================= */

/** a card this module made for a member (never a register card) */
function nlfm_is_member_card( $pro ) {
	$pro = (int) $pro;
	return $pro > 0 && 'nadlan_professional' === get_post_type( $pro ) && NLFM_SOURCE === (string) get_post_meta( $pro, 'source', true )
		&& (int) get_post_meta( $pro, 'nl_forum_member', true ) > 0;
}

/** the member's own member-made card id, or 0 */
function nlfm_own_card( $m ) {
	if ( ! $m ) { return 0; }
	$pro = (int) $m['pro_id'];
	if ( ! nlfm_is_member_card( $pro ) || (int) get_post_meta( $pro, 'nl_forum_member', true ) !== (int) $m['id'] || 'trash' === get_post_status( $pro ) ) { return 0; }
	return $pro;
}

/** the directory keys the label function knows (the directory's own list plus the professions registry) */
function nlfm_known_keys() {
	$k = function_exists( 'nadlan_dir_professions_all' ) ? array_keys( (array) nadlan_dir_professions_all() ) : array();
	if ( function_exists( 'nadlan_pro_registry' ) ) { $k = array_merge( $k, array_keys( (array) nadlan_pro_registry() ) ); }
	return array_values( array_unique( array_map( 'strval', $k ) ) );
}

/** the video switch of a member (the call module's table); false when the module is absent */
function nlfm_video_on( $mid ) {
	if ( ! function_exists( 'nlfc_prefs' ) ) { return false; }
	$p = nlfc_prefs( array( (int) $mid ) );
	return ! empty( $p[ (int) $mid ]['video'] );
}

/** the state the page script needs: who is in, does he have a card, the values to edit */
function nlfm_state( $m ) {
	if ( ! $m ) { return array( 'member' => 0 ); }
	$own  = nlfm_own_card( $m );
	$card = null;
	if ( $own ) {
		$card = array(
			'id'     => $own,
			'name'   => (string) get_post_meta( $own, 'nl_name_he', true ),
			'trade'  => (string) get_post_meta( $own, 'nl_forum_trade', true ),
			'form'   => 'f' === (string) get_post_meta( $own, 'nl_gender', true ) ? 'f' : 'm',
			'city'   => (string) get_post_meta( $own, 'city', true ),
			'bio'    => (string) get_post_meta( $own, 'bio', true ),
			'phone'  => (string) get_post_meta( $own, '_nlfm_phone', true ),
			'how'    => 'phone' === (string) get_post_meta( $own, 'nl_forum_contact', true ) ? 'phone' : 'forum',
			'video'  => nlfm_video_on( (int) $m['id'] ) ? 1 : 0,
			'status' => (string) get_post_status( $own ),
			'url'    => 'publish' === get_post_status( $own ) ? (string) get_permalink( $own ) : '',
		);
	}
	return array( 'member' => 1, 'name' => (string) $m['display_name'], 'role' => (string) $m['role_label'], 'trade' => (string) $m['trade'],
		'linked' => (int) $m['pro_id'] > 0 ? 1 : 0, 'card' => $card, 'invite' => nlfm_wants_invite( $m ) ? 1 : 0 );
}

/* =========================================================================================================
 * 3. Markup: A the invitation, C the card, the small link and the owner's edit button
 * ======================================================================================================= */

function nlfm_invite_html( $where = '' ) {
	return '<section class="nlfm-inv" dir="rtl" aria-labelledby="nlfm-inv-h' . esc_attr( $where ) . '" data-nlfm-inv>'
		. '<span class="nlfm-free">חינם כרגע</span>'
		. '<h2 class="nlfm-inv-h" id="nlfm-inv-h' . esc_attr( $where ) . '">רוצים שהפרטים שלכם יופיעו ושיפנו אליכם?</h2>'
		. '<p class="nlfm-inv-p">פתחו כרטיס בעל מקצוע: שם, מקצוע, עיר וטלפון. הכרטיס מופיע ליד כל תשובה שלכם בפורום.</p>'
		. '<div class="nlfm-inv-row"><button type="button" class="nlfm-inv-btn" data-nlfm-open>פתיחת כרטיס</button><span class="nlfm-inv-fine">דקה אחת, בלי תשלום ובלי סיסמה</span></div>'
		. '</section>';
}

function nlfm_svg_video( $size = 22 ) {
	return '<svg aria-hidden="true" focusable="false" width="' . (int) $size . '" height="' . (int) $size . '" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="6" width="13" height="12" rx="2"></rect><path d="M16 10l5-3v10l-5-3z"></path></svg>';
}

/**
 * Part C: the opened card of a member. $h1 true when the theme's header was taken out (then this card carries the page's
 * only h1). Never a register tick and never a "verified" word: the line says the member gave the details himself.
 */
function nlfm_card_html( $pro, $me, $h1 ) {
	$pro    = (int) $pro;
	$member = nlf_pro_member( $pro );
	if ( ! $member ) { return ''; }
	$name   = (string) get_post_meta( $pro, 'nl_name_he', true );
	$name   = '' !== $name ? $name : (string) get_the_title( $pro );
	$first  = nlfm_first_name( $name );
	$female = 'f' === (string) get_post_meta( $pro, 'nl_gender', true );
	$trades = nlf_trades();
	$tk     = (string) get_post_meta( $pro, 'nl_forum_trade', true );
	$tr     = $trades[ $tk ] ?? null;
	$label  = nlf_pro_label( $pro );
	$tint   = nlfm_group_tint( $tr ? $tr['group'] : '' );
	$city   = (string) get_post_meta( $pro, 'city', true );
	$bio    = (string) get_post_meta( $pro, 'bio', true );
	$since  = nlfm_since_line( nlf_ts( $member['created_at'] ), $female );
	$own    = $me && (int) $me['id'] === (int) $member['id'];
	$video  = ! $own && 'publish' === get_post_status( $pro ) && nlfm_video_on( (int) $member['id'] ) && function_exists( 'nlfc_on' ) && nlfc_on();
	$phone  = nlf_pro_phone( $pro, $member );
	$tag    = $h1 ? 'h1' : 'p';
	$h  = '<section class="nlf nlfm-card" dir="rtl" aria-label="' . esc_attr( 'הכרטיס של ' . $name ) . '">';
	$h .= '<header class="nlfm-head"><span class="nlfm-av" style="' . nlf_tint_style( $tint ) . '" aria-hidden="true">' . esc_html( nlf_initials( $name ) ) . '</span>';
	$h .= '<div class="nlfm-id"><div class="nlfm-meta"><span class="nlfm-pill" style="' . nlf_tint_style( $tint ) . '">' . esc_html( $label ) . '</span>'
		. ( '' !== $city ? '<span>' . esc_html( $city ) . '</span>' : '' ) . '</div>';
	$h .= '<' . $tag . ' class="nlfm-name">' . esc_html( $name ) . '</' . $tag . '>';
	if ( '' !== $since ) { $h .= '<span class="nlfm-since">' . esc_html( $since ) . '</span>'; }
	$h .= '</div></header>';
	if ( '' !== trim( $bio ) ) { $h .= '<p class="nlfm-bio">' . nlf_body_html( $bio ) . '</p>'; }
	if ( $video ) {
		$h .= '<button type="button" class="nlfm-call" data-nlf-callcard="' . $pro . '" data-nlf-with="' . (int) $member['id'] . '" data-nlf-name="' . esc_attr( $first ) . '" data-nlf-label="' . esc_attr( $label ) . '">'
			. '<span class="nlfm-call-ic">' . nlfm_svg_video( 22 ) . '</span><span class="nlfm-call-t"><span class="nlfm-call-h">' . esc_html( 'שיחת וידאו עם ' . $first ) . '</span>'
			. '<span class="nlfm-call-s">בדפדפן, בלי התקנה. אפשר להראות תוכנית ולסמן עליה יחד.</span></span></button>';
	}
	if ( $phone ) {
		$h .= '<div class="nlfm-two">';
		if ( '' !== $phone['wa'] ) { $h .= '<a class="nlfm-wa" href="' . esc_url( 'https://wa.me/' . $phone['wa'] ) . '" target="_blank" rel="noopener">וואטסאפ</a>'; }
		if ( '' !== $phone['tel'] ) { $h .= '<a class="nlfm-tel" href="' . esc_url( 'tel:' . $phone['tel'] ) . '">חיוג</a>'; }
		$h .= '</div>';
	}
	if ( $video || $phone ) { $h .= '<span class="nlfm-direct">' . esc_html( 'הפנייה מגיעה ישר אל ' . $first . ', לא לאתר.' ) . '</span>'; }
	if ( $own ) { $h .= '<button type="button" class="nlfm-edit" data-nlfm-open>עריכת הכרטיס</button>'; }
	return $h . '</section>';
}

/* =========================================================================================================
 * 4. The hook points of inc/pro-forum-render.php
 * ======================================================================================================= */

/* A at the top of the forum home (the forum's own notices hook, right under the member bar) */
add_filter( 'nlf_home_notices', function ( $html, $me ) {
	return nlfm_wants_invite( $me ) ? $html . nlfm_invite_html( '-home' ) : $html;
}, 5, 2 );

/* A above the reply form of a discussion */
add_filter( 'nlf_before_replyform', function ( $html, $t, $me ) {
	return nlfm_wants_invite( $me ) ? $html . nlfm_invite_html( '-reply' ) : $html;
}, 10, 3 );

/* the small "אני בעל מקצוע" link in the member bar, for a member with another role */
add_filter( 'nlf_member_bar_extra', function ( $html, $me ) {
	return nlfm_wants_link( $me ) ? $html . '<button type="button" class="nlf-link nlfm-iam" data-nlfm-open>אני בעל מקצוע</button>' : $html;
}, 10, 2 );

/* D: under the name of a member who opened his own card, "חברה בפורום · המרכז" (never a register mark) */
add_filter( 'nlf_name_extra', function ( $html, $m ) {
	if ( ! is_array( $m ) || ! nlfm_own_card( $m ) || 'publish' !== get_post_status( (int) $m['pro_id'] ) ) { return $html; }
	$pro  = (int) $m['pro_id'];
	$city = (string) get_post_meta( $pro, 'city', true );
	$line = ( 'f' === (string) get_post_meta( $pro, 'nl_gender', true ) ? 'חברה בפורום' : 'חבר בפורום' ) . ( '' !== $city ? ' · ' . $city : '' );
	return $html . '<span class="nlfm-sub">' . esc_html( $line ) . '</span>';
}, 20, 2 );

/* "עריכת הכרטיס" in the owner box of a member-made card */
add_filter( 'nlf_owner_box_extra', function ( $html, $pro, $me ) {
	return $me && nlfm_own_card( $me ) === (int) $pro ? $html . '<button type="button" class="nlf-btn nlf-btn-line nlfm-editbtn" data-nlfm-open>עריכת הכרטיס</button>' : $html;
}, 10, 3 );

/* C on the card page: the theme's header of a member-made card is replaced by the card of board 18 (its h1 moves with it),
   so the site's "פרסמו בקשה" hero button is not the main action. When the header is not found nothing is taken out and the
   card prints without a heading (CSS hides the hero button then). */
add_filter( 'nlf_card_content', function ( $content, $pro, $me ) {
	if ( ! nlfm_is_member_card( $pro ) || ! nlf_pro_member( $pro ) ) { return $content; }
	$h1 = false;
	$p  = strpos( $content, 'class="nlpp-hero"' );
	if ( false !== $p ) {
		$s = strrpos( substr( $content, 0, $p ), '<header' );
		$e = strpos( $content, '</header>', $p );
		if ( false !== $s && false !== $e && false === strpos( substr( $content, $s, $e - $s ), '<header', 7 ) ) {
			$content = substr( $content, 0, $s ) . substr( $content, $e + 9 );
			$h1 = true;
		}
	}
	$GLOBALS['nlfm_card_top'] = nlfm_card_html( $pro, $me, $h1 );
	return $content;
}, 10, 3 );

add_filter( 'nlf_card_top', function ( $top, $pro, $me ) {
	if ( empty( $GLOBALS['nlfm_card_top'] ) ) { return $top; }
	$c = (string) $GLOBALS['nlfm_card_top'];
	$GLOBALS['nlfm_card_top'] = '';
	return $c . $top;
}, 10, 3 );

/* a body class on member-made cards (CSS scope), and the scheduler band off there (the 1.72.672 pattern): the member is
   reached by the call, WhatsApp or a message, never through the site's calendar */
add_filter( 'body_class', function ( $c ) {
	$id = is_singular( 'nadlan_professional' ) ? (int) get_queried_object_id() : 0;
	// only where part C really prints (the forum's card filter runs only with the gate open and a joined member behind the card)
	if ( $id && nlfm_is_member_card( $id ) && nlf_gate_open() && nlf_pro_member( $id ) && ! nlf_pro_removed( $id ) ) { $c[] = 'nlfm-member-card'; }
	return $c;
} );
add_action( 'wp', function () {
	if ( is_admin() || ! is_singular( 'nadlan_professional' ) ) { return; }
	if ( nlfm_is_member_card( (int) get_queried_object_id() ) ) {
		add_filter( 'pre_option_nadlan_feature_scheduler', function () { return '0'; } );
	}
} );

/* =========================================================================================================
 * 5. Writing the card
 * ======================================================================================================= */

/** a post write from a forum request (no WordPress user): kses would strip nothing useful here but is kept off as the forum does */
function nlfm_post_write( array $post ) {
	$kses = false !== has_filter( 'content_save_pre', 'wp_filter_post_kses' );
	if ( $kses ) { kses_remove_filters(); }
	$id = isset( $post['ID'] ) ? wp_update_post( $post, true ) : wp_insert_post( $post, true );
	if ( $kses ) { kses_init_filters(); }
	return is_wp_error( $id ) ? 0 : (int) $id;
}

/** one mail to the site owner for a card that waits, with signed approve / reject links (a press on the page does it) */
function nlfm_mail_pending( $pro, $m, array $d, $label ) {
	$link = function ( $a ) use ( $pro ) { return add_query_arg( 'nlfm_act', nlf_link_token( $a, 'c' . (int) $pro, time() + 14 * DAY_IN_SECONDS, nlf_key() ), home_url( '/' ) ); };
	$body = "חבר בפורום פתח כרטיס בעל מקצוע, והוא מחכה לבדיקה.\n\n"
		. 'מאת: ' . $m['display_name'] . ' (' . $m['contact'] . ")\n"
		. 'שם בכרטיס: ' . $d['name'] . "\n" . 'מקצוע: ' . $label . "\n" . 'עיר או אזור: ' . $d['city'] . "\n"
		. ( '' !== $d['phone_raw'] ? 'טלפון: ' . $d['phone_raw'] . ( 'phone' === $d['how'] ? " (יוצג)\n" : " (לא יוצג)\n" ) : '' )
		. ( '' !== $d['bio'] ? "\nמה הוא עושה:\n" . nlf_excerpt( $d['bio'], 400 ) . "\n" : '' )
		. "\nאישור: " . $link( 'ok' ) . "\nדחייה: " . $link( 'no' ) . "\n\nהכרטיס בניהול האתר: " . admin_url( 'post.php?post=' . (int) $pro . '&action=edit' ) . "\n";
	nlf_mail( nlf_admin_to(), '[פורום] כרטיס בעל מקצוע מחכה לבדיקה: ' . nlf_excerpt( $d['name'], 60 ), $body );
}

add_action( 'rest_api_init', function () {
	$reg = function ( $path, $method, $cb ) {
		register_rest_route( 'nadlan/v1', '/forum/card/' . $path, array( 'methods' => $method, 'permission_callback' => '__return_true', 'callback' => $cb, 'show_in_index' => false ) );
	};

	// the member's card state (the page script after an entry without a reload)
	$reg( 'me', 'GET', function ( WP_REST_Request $q ) {
		$g = nlf_guard( $q, 'view' );
		if ( is_wp_error( $g ) ) { return $g; }
		return nlf_ok( array( 'card' => nlfm_state( nlf_me() ) ) );
	} );

	// open or update the member's own card
	$reg( 'save', 'POST', function ( WP_REST_Request $q ) {
		$m = nlf_guard( $q, 'post' );
		if ( is_wp_error( $m ) ) { return $m; }
		$own = nlfm_own_card( $m );
		if ( ! $own && (int) $m['pro_id'] > 0 && 'nadlan_professional' === get_post_type( (int) $m['pro_id'] ) && 'trash' !== get_post_status( (int) $m['pro_id'] ) ) {
			return nlf_err( 'יש לכם כבר כרטיס מחובר. אפשר לנהל אותו מהפרופיל שלכם.' );
		}
		$trades = nlf_trades();
		$v = nlfm_validate( array( 'name' => $q->get_param( 'name' ), 'trade' => $q->get_param( 'trade' ), 'form' => $q->get_param( 'form' ), 'city' => $q->get_param( 'city' ),
			'bio' => $q->get_param( 'bio' ), 'phone' => $q->get_param( 'phone' ), 'how' => $q->get_param( 'how' ), 'video' => (string) $q->get_param( 'video' ) ), $trades );
		if ( isset( $v['err'] ) ) { return nlf_err( $v['err'] ); }
		$d = $v['data'];
		if ( ! $own && ( ! nlf_rl( 'card_new', 2, DAY_IN_SECONDS, 'm' . (int) $m['id'] ) || ! nlf_rl( 'card_new_ip', 2, DAY_IN_SECONDS ) ) ) {
			return nlf_err( 'אפשר לפתוח עד 2 כרטיסים ביום. נסו שוב מחר.' );
		}
		$tr     = $trades[ $d['trade'] ];
		$label  = nlfm_trade_label( $tr, $d['form'] );
		$want   = nlfm_status( (int) $m['approved_posts'], $d['name'] . "\n" . $d['city'] . "\n" . $d['bio'], (string) $tr['reg'] );
		$cur    = $own ? (string) get_post_status( $own ) : '';
		// an edit never publishes a card that waits for the owner, and a card its owner hid stays hidden
		$status = 'private' === $cur ? 'private' : ( 'pending' === $cur ? 'pending' : $want );
		$post   = array( 'post_type' => 'nadlan_professional', 'post_title' => $d['name'], 'post_status' => $status );
		if ( $own ) { $post['ID'] = $own; } else { $post['post_content'] = ''; $post['post_author'] = 0; $post['comment_status'] = 'closed'; $post['ping_status'] = 'closed'; }
		$pro = nlfm_post_write( $post );
		if ( $pro <= 0 ) { return nlf_err( 'משהו השתבש. נסו שוב.' ); }
		$show = 'phone' === $d['how'] && '' !== $d['phone'];
		$meta = array(
			'source' => NLFM_SOURCE, 'nl_forum_member' => (int) $m['id'], 'nl_forum_trade' => $d['trade'], 'nl_gender' => $d['form'],
			'profession' => nlfm_profession( $d['trade'], $d['form'], $trades, nlfm_known_keys() ), 'nl_name_he' => $d['name'], 'city' => $d['city'],
			'bio' => $d['bio'], '_nl_email' => nlf_contact_norm( (string) $m['contact'] ), '_nlfm_phone' => $d['phone_raw'], 'nl_forum_contact' => $show ? 'phone' : 'forum',
		);
		foreach ( $meta as $k => $val ) { update_post_meta( $pro, $k, $val ); }
		if ( $show ) { update_post_meta( $pro, 'phone', $d['phone_raw'] ); } else { delete_post_meta( $pro, 'phone' ); } // the card page reads `phone` only when he chose to show it
		if ( ! $own ) { update_post_meta( $pro, 'nl_forum_since', gmdate( 'Y-m', nlf_ts( $m['created_at'] ) ) ); }
		global $wpdb;
		$wpdb->update( nlf_t( 'members' ), array( 'pro_id' => $pro, 'role_label' => 'pro', 'trade' => $d['trade'], 'trade_other' => '', 'show_phone' => $show ? 1 : 0 ), array( 'id' => (int) $m['id'] ) );
		if ( function_exists( 'nlfc_pref_set' ) && function_exists( 'nlfc_prefs' ) ) { // the call switch follows his own checkbox; the mail switch stays his
			$p = nlfc_prefs( array( (int) $m['id'] ) );
			nlfc_pref_set( (int) $m['id'], $d['video'], ! empty( $p[ (int) $m['id'] ]['mail'] ) );
		}
		nlf_write_counted( $m );
		clean_post_cache( $pro );
		do_action( 'litespeed_purge_post', $pro );
		if ( 'pending' === $status && 'pending' !== $cur ) { nlfm_mail_pending( $pro, $m, $d, $label ); }
		nlf_me( true );
		$me  = nlf_me();
		$msg = 'pending' === $status ? 'הכרטיס יעלה אחרי בדיקה קצרה.' : ( $own ? 'הכרטיס עודכן.' : 'הכרטיס נפתח.' );
		return nlf_ok( array( 'status' => $status, 'url' => 'publish' === $status ? (string) get_permalink( $pro ) : '', 'message' => $msg, 'card' => nlfm_state( $me ) ) );
	} );
} );

/* =========================================================================================================
 * 6. One-click approve / reject from the owner's mail (?nlfm_act=, signed, 14 days, a POST press on the page does it,
 *    because mail scanners open links by themselves). The social module's pattern.
 * ======================================================================================================= */

add_action( 'template_redirect', function () {
	if ( ! isset( $_GET['nlfm_act'] ) || is_admin() || ! function_exists( 'nlf_link_read' ) ) { return; } // phpcs:ignore
	$tok  = sanitize_text_field( wp_unslash( $_GET['nlfm_act'] ) ); // phpcs:ignore -- signed token, checked below
	$link = nlf_link_read( $tok, time(), nlf_key() );
	if ( ! $link || ! in_array( $link[0], array( 'ok', 'no' ), true ) || ! preg_match( '/^c(\d+)$/', $link[1], $mm ) ) { return; } // a made-up token shows the normal page
	$GLOBALS['nlf_act_page'] = true;
	nlf_nocache();
	nlf_install();
	$pro  = (int) $mm[1];
	$ok   = 'ok' === $link[0];
	$body = '';
	if ( ! nlfm_is_member_card( $pro ) || 'trash' === get_post_status( $pro ) ) {
		$h = 'הכרטיס לא נמצא.';
	} elseif ( 'pending' !== get_post_status( $pro ) ) {
		$h = 'הכרטיס כבר טופל.';
	} elseif ( 'POST' === ( $_SERVER['REQUEST_METHOD'] ?? '' ) && isset( $_POST['nlfm_confirm'] ) ) { // phpcs:ignore -- the signed token is the authority
		if ( $ok ) {
			nlf_pro_set_status( $pro, 'publish' );
			$h = 'הכרטיס אושר ועלה לאתר.';
		} else {
			global $wpdb;
			$wpdb->query( $wpdb->prepare( 'UPDATE ' . nlf_t( 'members' ) . ' SET pro_id = NULL WHERE pro_id = %d', $pro ) );
			wp_trash_post( $pro ); // to the trash, not deleted: the site owner can still bring it back
			do_action( 'litespeed_purge_post', $pro );
			$h = 'הכרטיס נדחה והועבר לפח.';
		}
	} else {
		$h    = $ok ? 'אישור הכרטיס' : 'דחיית הכרטיס';
		$body = '<blockquote class="nlf-quote">' . nlf_body_html( get_the_title( $pro ) . ' · ' . get_post_meta( $pro, 'city', true ) . "\n" . get_post_meta( $pro, 'bio', true ) ) . '</blockquote>'
			. '<form method="post" action="' . esc_url( add_query_arg( 'nlfm_act', $tok, home_url( '/' ) ) ) . '"><input type="hidden" name="nlfm_confirm" value="1">'
			. '<button type="submit" class="nlf-btn ' . ( $ok ? 'nlf-btn-fill' : 'nlf-btn-danger' ) . ' nlf-btn-big">' . ( $ok ? 'אישור הכרטיס' : 'דחיית הכרטיס' ) . '</button></form>';
	}
	status_header( 200 );
	nlf_shell_open();
	echo '<div class="nlf nlf-page nlf-act" dir="rtl"><h1 class="nlf-h1">' . esc_html( $h ) . '</h1>' . $body . '</div>'; // phpcs:ignore -- escaped parts
	nlf_shell_close();
	exit;
}, -97 );

/* =========================================================================================================
 * 7. Assets and B, the form sheet (printed before the footer scripts, like the forum's own sheets)
 * ======================================================================================================= */

function nlfm_surface() {
	if ( ! function_exists( 'nlf_surface' ) ) { return false; }
	if ( '' === nlf_rendering() && ! empty( $GLOBALS['nlf_act_page'] ) ) { return false; }
	return nlf_surface();
}

add_action( 'wp_enqueue_scripts', function () {
	if ( ! nlfm_surface() ) { return; }
	$base = plugins_url( 'assets/proforum/', dirname( __FILE__ ) );
	$ver  = function_exists( 'nlf_ver' ) ? nlf_ver() : '1';
	wp_enqueue_style( 'nlf-mycard', $base . 'card.css', array( 'nlf' ), $ver );
	wp_enqueue_script( 'nlf-mycard', $base . 'card.js', array( 'nlf' ), $ver, true );
	$forms = array();
	foreach ( nlf_trades() as $k => $t ) { if ( nlfm_has_forms( $t ) ) { $forms[ $k ] = array( (string) $t['label'], (string) $t['female'] ); } }
	wp_add_inline_script( 'nlf-mycard', 'window.NLFM=' . nlf_json_script( array( 'state' => nlfm_state( nlf_me() ), 'forms' => $forms ) ) . ';', 'before' );
}, 33 );

add_action( 'wp_footer', function () {
	if ( ! nlfm_surface() || ( '' === nlf_rendering() && empty( $GLOBALS['nlf_card_printed'] ) ) ) { return; }
	echo nlfm_form_html(); // phpcs:ignore -- escaped inside
	echo '<template id="nlfm-inv-tpl">' . nlfm_invite_html( '-after' ) . '</template>'; // phpcs:ignore -- constant markup
}, 6 );

/** B: the form sheet (one dialog; the same form opens and edits) */
function nlfm_form_html() {
	ob_start();
	?>
<dialog class="nlf nlf-sheet nlfm-sheet" id="nlfm-form" dir="rtl" aria-labelledby="nlfm-form-h">
	<form class="nlfm-form" data-nlfm-form novalidate>
		<div class="nlfm-fh"><h2 class="nlfm-fh-h" id="nlfm-form-h">הכרטיס שלי</h2><span class="nlfm-fh-s">אפשר לשנות בכל רגע</span><button type="button" class="nlfm-x" data-nlf-close aria-label="סגירה"><?php echo nlf_svg( 'close' ); // phpcs:ignore ?></button></div>
		<div class="nlfm-fb">
			<div class="nlfm-f"><label for="nlfm-name">השם שיופיע</label><input id="nlfm-name" name="name" type="text" maxlength="60" autocomplete="name" required></div>
			<div class="nlfm-g2">
				<div class="nlfm-f"><label for="nlfm-trade">מקצוע</label><select id="nlfm-trade" name="trade" required><option value="">בחרו</option>
					<?php foreach ( ( function_exists( 'nadlan_forum_trade_groups' ) ? (array) nadlan_forum_trade_groups() : array() ) as $grp ) : ?><optgroup label="<?php echo esc_attr( $grp['label'] ); ?>"><?php foreach ( (array) $grp['trades'] as $tk => $tr ) : ?><option value="<?php echo esc_attr( $tk ); ?>"><?php echo esc_html( $tr[0] ); ?></option><?php endforeach; ?></optgroup><?php endforeach; ?>
				</select></div>
				<div class="nlfm-f"><label for="nlfm-city">עיר או אזור</label><input id="nlfm-city" name="city" type="text" maxlength="40" autocomplete="address-level2" required></div>
			</div>
			<fieldset class="nlfm-forms" data-nlfm-forms hidden><legend>איך לכתוב את המקצוע</legend>
				<div class="nlfm-chips"><label><input type="radio" name="form" value="m" checked><span data-nlfm-fm></span></label><label><input type="radio" name="form" value="f"><span data-nlfm-ff></span></label></div>
			</fieldset>
			<div class="nlfm-f"><label for="nlfm-bio">מה אתם עושים, בשתי שורות</label><textarea id="nlfm-bio" name="bio" rows="3" maxlength="300"></textarea><span class="nlfm-count" data-nlfm-count aria-live="polite"></span></div>
			<div class="nlfm-f"><label for="nlfm-tel">טלפון (לא חובה)</label><input id="nlfm-tel" name="phone" type="tel" dir="ltr" inputmode="tel" autocomplete="tel" maxlength="20" placeholder="050-0000000"></div>
			<fieldset class="nlfm-how"><legend>איך פונים אליכם</legend>
				<label><input type="radio" name="how" value="phone" checked>טלפון, וואטסאפ ושיחת וידאו</label>
				<label><input type="radio" name="how" value="forum">רק בהודעה ובשיחת וידאו דרך הפורום</label>
			</fieldset>
			<label class="nlfm-vid"><input type="checkbox" name="video" value="1" checked><span>אפשר לפנות אליי בשיחת וידאו</span></label>
			<?php echo nlf_trap(); // phpcs:ignore ?>
			<button type="submit" class="nlfm-go" data-nlfm-go>פתיחת הכרטיס</button>
			<p class="nlfm-msg" role="status" aria-live="polite"></p>
			<span class="nlfm-fine">הכרטיס יסומן "חבר בפורום". סימן "נבדק" מגיע רק אחרי בדיקה, ואף פעם לא בתשלום. אפשר להסתיר או למחוק את הכרטיס בלחיצה.</span>
		</div>
	</form>
</dialog>
	<?php
	return (string) ob_get_clean();
}
