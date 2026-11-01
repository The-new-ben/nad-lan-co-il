<?php
/**
 * nadlan-config - PRICE NUDGE (HAD-642, Ben 31.10.2026): a quiet price-list slip that rises from the bottom of a project
 * page late in the visit and offers a price update, plans and the project's status on WhatsApp in one tap.
 * Claude Design v105.2, component PriceNudge. Ben's words: "מחירי הנדל״ן משתנים. לחצו לקבלת עדכון מחיר, תוכניות וסטטוס
 * הפרויקט"; he owns the wording (a project's own line in its box wins).
 *
 * - Never on arrival: 25 s of the page being visible AND 35% scrolled (or 2.5 screens on a long page); or a leaving signal (desktop: the pointer leaves
 *   through the top after 15 s; phone: a fast scroll back up after half the page, or a return to the tab after 20 s away).
 *   No back-button trap. Never while a field has focus, after a WhatsApp tap or an open chat, or in full screen.
 * - A banner, not a modal: under 30% of a phone screen, no backdrop, the page keeps scrolling; swipe down, the x, "לא עכשיו",
 *   Esc, or it fades by itself after 14 s of being ignored (touch pauses it). Then quiet 7 days on every project, 30 after
 *   a WhatsApp tap. The floating "ייעוץ חינם" bar steps aside while it is up (one contact element per screen).
 * - Control: a box on every project (follow the site / show / do not show + an own line), a switch column in the projects
 *   list, and Settings > חלון עדכון מחירים. Ashira never (Ben, 31.10.2026). Site default: off; Rainbow first.
 * - Measurement: gtag events nudge_shown / nudge_close / nudge_wa / nudge_holdout; a holdout share never sees it.
 * - 105.7 (Ben 1.11.2026, after a broker asked him for Rainbow's prices and plans): the site's own window. The frame says
 *   "נדל״ן · nad-lan.co.il", never a project's or a listing's name; no plans are offered; the WhatsApp text carries the page
 *   address, not a project name; every trigger waits the full delay; no Tawk.to calls (the site hides that chat on load). Also on
 *   the Hebrew listings of the brokers in the option nadlan_nudge_brokers (first: Meital Katsir, 7833).
 */
if ( ! defined( 'ABSPATH' ) ) { exit; }

if ( ! function_exists( 'nadlan_nudge_opts' ) ) {
	function nadlan_nudge_opts() {
		$d = array( 'default' => 'off', 'delay' => 25, 'depth' => 35, 'quiet' => 7, 'quiet_wa' => 30, 'holdout' => 20, 'fade' => 14 );
		$o = get_option( 'nadlan_nudge_opts', array() );
		return is_array( $o ) ? array_merge( $d, array_intersect_key( $o, $d ) ) : $d;
	}
}

if ( ! function_exists( 'nadlan_nudge_blocked' ) ) {
	/** never on these projects, whatever the box says (Ben 31.10.2026: not on Ashira) */
	function nadlan_nudge_blocked( $id ) {
		$slug = (string) get_post_field( 'post_name', $id );
		return 0 === strpos( $slug, 'ashira' ) || 0 === strpos( rawurldecode( $slug ), 'אשירה' );
	}
}

if ( ! function_exists( 'nadlan_nudge_on' ) ) {
	function nadlan_nudge_on( $id = 0 ) {
		$id = (int) ( $id ?: get_queried_object_id() );
		if ( ! $id || 'publish' !== get_post_status( $id ) || post_password_required( $id ) ) { return false; }
		/* 105.9 (Ben 1.11.2026: "on everyone except Rainbow"): every Hebrew listing */
		if ( 'nadlan_property' === get_post_type( $id ) ) {
			return (bool) preg_match( '/\p{Hebrew}/u', (string) get_the_title( $id ) );
		}
		if ( 'nadlan_project' !== get_post_type( $id ) || nadlan_nudge_blocked( $id ) ) { return false; }
		$m = (string) get_post_meta( $id, 'nadlan_nudge', true );
		if ( 'on' === $m ) { return true; }
		if ( 'off' === $m ) { return false; }
		return true; // 105.9 (Ben 1.11.2026): on by default; a box that says off (Rainbow) and Ashira stay without it
	}
}

add_action( 'init', function () {
	foreach ( array( 'nadlan_nudge', 'nadlan_nudge_text' ) as $k ) {
		register_post_meta( 'nadlan_project', $k, array(
			'show_in_rest'  => true,
			'single'        => true,
			'type'          => 'string',
			'auth_callback' => function ( $allowed, $meta_key, $post_id ) { return current_user_can( 'edit_post', (int) $post_id ); },
		) );
	}
}, 20 );

/* ---------- admin: the box on every project ---------- */
add_action( 'add_meta_boxes_nadlan_project', function () {
	add_meta_box( 'nadlan_nudge_box', 'חלון עדכון מחירים', function ( $post ) {
		$m = (string) get_post_meta( $post->ID, 'nadlan_nudge', true );
		$t = (string) get_post_meta( $post->ID, 'nadlan_nudge_text', true );
		$def = nadlan_nudge_opts()['default'];
		wp_nonce_field( 'nadlan_nudge_save', 'nadlan_nudge_nonce' );
		if ( nadlan_nudge_blocked( $post->ID ) ) {
			echo '<p style="color:#b32d2e;font-weight:600">כבוי בפרויקט הזה לפי בן (31.10.2026).</p>';
		}
		foreach ( array( '' => 'לפי ברירת המחדל של האתר (כרגע: ' . ( 'on' === $def ? 'מוצג' : 'לא מוצג' ) . ')', 'on' => 'להציג בעמוד הזה', 'off' => 'לא להציג בעמוד הזה' ) as $v => $label ) {
			echo '<label style="display:block;margin:4px 0"><input type="radio" name="nadlan_nudge" value="' . esc_attr( $v ) . '"' . checked( $m, $v, false ) . '> ' . esc_html( $label ) . '</label>';
		}
		echo '<p style="margin:10px 0 4px">נוסח משלכם (לא חובה):</p><textarea name="nadlan_nudge_text" rows="2" style="width:100%" placeholder="מחירי הנדל״ן משתנים">' . esc_textarea( $t ) . '</textarea>';
		echo '<p style="color:#646970;font-size:12px;margin:4px 0 0">ריק = הנוסח הקבוע: "מחירי הנדל״ן משתנים. לחצו לקבלת עדכון מחיר, תוכניות וסטטוס הפרויקט".</p>';
	}, 'nadlan_project', 'side', 'default' );
} );

add_action( 'save_post_nadlan_project', function ( $post_id ) {
	if ( ! isset( $_POST['nadlan_nudge_nonce'] ) || ! wp_verify_nonce( sanitize_text_field( wp_unslash( $_POST['nadlan_nudge_nonce'] ) ), 'nadlan_nudge_save' ) ) { return; }
	if ( defined( 'DOING_AUTOSAVE' ) && DOING_AUTOSAVE ) { return; }
	if ( ! current_user_can( 'edit_post', $post_id ) ) { return; }
	$v = isset( $_POST['nadlan_nudge'] ) ? sanitize_key( wp_unslash( $_POST['nadlan_nudge'] ) ) : '';
	if ( in_array( $v, array( 'on', 'off' ), true ) ) { update_post_meta( $post_id, 'nadlan_nudge', $v ); } else { delete_post_meta( $post_id, 'nadlan_nudge' ); }
	$t = isset( $_POST['nadlan_nudge_text'] ) ? sanitize_text_field( wp_unslash( $_POST['nadlan_nudge_text'] ) ) : '';
	if ( '' !== $t ) { update_post_meta( $post_id, 'nadlan_nudge_text', $t ); } else { delete_post_meta( $post_id, 'nadlan_nudge_text' ); }
} );

/* ---------- admin: the switch column in the projects list ---------- */
add_filter( 'manage_nadlan_project_posts_columns', function ( $cols ) {
	$cols['nadlan_nudge'] = 'חלון עדכון';
	return $cols;
} );
add_action( 'manage_nadlan_project_posts_custom_column', function ( $col, $post_id ) {
	if ( 'nadlan_nudge' !== $col ) { return; }
	if ( nadlan_nudge_blocked( $post_id ) ) { echo '<span style="color:#b32d2e">כבוי (בן)</span>'; return; }
	$on  = nadlan_nudge_on( $post_id ) || ( 'on' === get_post_meta( $post_id, 'nadlan_nudge', true ) );
	$url = wp_nonce_url( admin_url( 'admin-post.php?action=nadlan_nudge_toggle&post=' . (int) $post_id . '&to=' . ( $on ? 'off' : 'on' ) ), 'nadlan_nudge_toggle_' . (int) $post_id );
	echo '<a href="' . esc_url( $url ) . '" style="display:inline-block;padding:2px 10px;border-radius:999px;text-decoration:none;font-weight:600;'
		. ( $on ? 'background:#0f7a63;color:#fff">מוצג' : 'background:#dcdcde;color:#1d2327">כבוי' ) . '</a>';
}, 10, 2 );
add_action( 'admin_post_nadlan_nudge_toggle', function () {
	$id = isset( $_GET['post'] ) ? (int) $_GET['post'] : 0;
	check_admin_referer( 'nadlan_nudge_toggle_' . $id );
	if ( ! $id || ! current_user_can( 'edit_post', $id ) ) { wp_die( 'forbidden' ); }
	$to = isset( $_GET['to'] ) && 'on' === $_GET['to'] ? 'on' : 'off';
	update_post_meta( $id, 'nadlan_nudge', $to );
	wp_safe_redirect( wp_get_referer() ?: admin_url( 'edit.php?post_type=nadlan_project' ) );
	exit;
} );

/* ---------- admin: site settings ---------- */
add_action( 'admin_menu', function () {
	add_options_page( 'חלון עדכון מחירים', 'חלון עדכון מחירים', 'manage_options', 'nadlan-nudge', function () {
		if ( ! current_user_can( 'manage_options' ) ) { return; }
		if ( isset( $_POST['nadlan_nudge_opts_nonce'] ) && wp_verify_nonce( sanitize_text_field( wp_unslash( $_POST['nadlan_nudge_opts_nonce'] ) ), 'nadlan_nudge_opts' ) ) {
			$in = wp_unslash( $_POST );
			update_option( 'nadlan_nudge_opts', array(
				'default'  => ( isset( $in['default'] ) && 'on' === $in['default'] ) ? 'on' : 'off',
				'delay'    => max( 10, min( 120, (int) ( $in['delay'] ?? 25 ) ) ),
				'depth'    => max( 10, min( 90, (int) ( $in['depth'] ?? 35 ) ) ),
				'quiet'    => max( 1, min( 60, (int) ( $in['quiet'] ?? 7 ) ) ),
				'quiet_wa' => max( 1, min( 120, (int) ( $in['quiet_wa'] ?? 30 ) ) ),
				'holdout'  => max( 0, min( 50, (int) ( $in['holdout'] ?? 20 ) ) ),
				'fade'     => max( 6, min( 60, (int) ( $in['fade'] ?? 14 ) ) ),
			), false );
			echo '<div class="notice notice-success"><p>נשמר.</p></div>';
		}
		$o = nadlan_nudge_opts();
		$f = function ( $k, $label, $hint ) use ( $o ) {
			echo '<tr><th><label for="nn-' . esc_attr( $k ) . '">' . esc_html( $label ) . '</label></th><td><input type="number" id="nn-' . esc_attr( $k ) . '" name="' . esc_attr( $k ) . '" value="' . (int) $o[ $k ] . '" class="small-text"> <span class="description">' . esc_html( $hint ) . '</span></td></tr>';
		};
		echo '<div class="wrap" dir="rtl"><h1>חלון עדכון מחירים</h1><p>התלוש עולה מתחתית עמוד הפרויקט מאוחר בביקור, עם וואטסאפ לעדכון מחיר, תוכניות וסטטוס. בכל פרויקט יש תיבה, וברשימת הפרויקטים יש עמודת מתג.</p><form method="post">';
		wp_nonce_field( 'nadlan_nudge_opts', 'nadlan_nudge_opts_nonce' );
		echo '<table class="form-table"><tr><th>ברירת המחדל לפרויקטים</th><td><label><input type="radio" name="default" value="off"' . checked( $o['default'], 'off', false ) . '> כבוי, רק בפרויקטים שסומנו</label><br><label><input type="radio" name="default" value="on"' . checked( $o['default'], 'on', false ) . '> מוצג בכל הפרויקטים (חוץ ממה שכובה, ואשירה)</label></td></tr>';
		$f( 'delay', 'המתנה (שניות)', 'כמה שניות העמוד גלוי לפני שהתלוש יכול לעלות' );
		$f( 'depth', 'עומק גלילה (%)', 'וגם כמה מהעמוד נגלל' );
		$f( 'fade', 'היעלמות (שניות)', 'אחרי כמה שניות בלי נגיעה הוא נעלם לבד' );
		$f( 'quiet', 'שקט אחרי סגירה (ימים)', 'בכל האתר' );
		$f( 'quiet_wa', 'שקט אחרי פנייה (ימים)', 'אחרי לחיצה על וואטסאפ' );
		$f( 'holdout', 'קבוצת ביקורת (%)', 'אחוז מבקרים שלא רואים אותו, כדי למדוד מה הוא מוסיף' );
		echo '</table>';
		submit_button( 'שמירה' );
		echo '</form></div>';
	} );
} );

/* ---------- the page ---------- */
if ( ! function_exists( 'nadlan_nudge_name' ) ) {
	/** the project's short Hebrew name for the kicker: the title's Hebrew half ("Rainbow Tel Aviv - ריינבו תל אביב") */
	function nadlan_nudge_name( $id ) {
		$t = trim( wp_strip_all_tags( html_entity_decode( get_the_title( $id ), ENT_QUOTES, 'UTF-8' ) ) );
		foreach ( preg_split( '/\s+[-–|]\s+/u', $t ) as $part ) {
			if ( preg_match( '/\p{Hebrew}/u', $part ) ) { return trim( $part ); }
		}
		return $t;
	}
}

add_action( 'wp_footer', function () {
	if ( is_admin() || ! is_singular( array( 'nadlan_project', 'nadlan_property' ) ) ) { return; }
	$id = (int) get_queried_object_id();
	if ( ! nadlan_nudge_on( $id ) ) { return; }
	$wa = function_exists( 'nadlan_cta_whatsapp_number' ) ? nadlan_cta_whatsapp_number() : '';
	if ( '' === $wa ) { return; }
	$o    = nadlan_nudge_opts();
	/* 105.7 (Ben 1.11.2026): the site's own window. Never a project's or a listing's name on the frame or in the message, never
	   an offer of plans the site does not hold: the site is an independent publisher, never the developer or a broker. */
	$own  = trim( (string) get_post_meta( $id, 'nadlan_nudge_text', true ) );
	$line = '' !== $own ? $own : 'מחירי הנדל״ן משתנים';
	$base = 'https://wa.me/' . rawurlencode( $wa ) . '?text=';
	$msgs = array( 'all' => 'שלום, אשמח לקבל עדכון על מחירי הנדל״ן באזור. הגעתי מהעמוד: ' . get_permalink( $id ) );
	$cfg = array(
		'p'  => (string) get_post_field( 'post_name', $id ),
		'd'  => (int) $o['delay'], 'dp' => (int) $o['depth'] / 100, 'f' => (int) $o['fade'],
		'q'  => (int) $o['quiet'], 'qw' => (int) $o['quiet_wa'], 'h' => (int) $o['holdout'],
	);
	?>
<div id="nlnu" class="nlnu" dir="rtl" role="dialog" aria-modal="false" aria-labelledby="nlnu-line" hidden>
	<span class="nlnu-grab" aria-hidden="true"></span>
	<div class="nlnu-head"><p class="nlnu-kick">נדל״ן · nad-lan.co.il</p><button type="button" class="nlnu-x" aria-label="סגירה">×</button></div>
	<span class="nlnu-perf" aria-hidden="true"></span>
	<p class="nlnu-line" id="nlnu-line"><?php echo esc_html( $line ); ?></p>
	<p class="nlnu-small">רוצים לקבל עדכון כשהמחירים באזור משתנים? שלחו הודעה ונעדכן אתכם.</p>
	<div class="nlnu-acts">
		<a class="nlnu-wa" data-k="all" href="<?php echo esc_url( $base . rawurlencode( $msgs['all'] ) ); ?>" target="_blank" rel="noopener"><svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path fill="currentColor" d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm0 18.2a8.2 8.2 0 0 1-4.2-1.2l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8s-.4-.1-.6.1l-.8 1c-.1.2-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.2-.4.2-.4.7-1.3.1-.2 0-.3 0-.4l-.8-1.9c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 3 3 0 0 0-.9 2.2 5.2 5.2 0 0 0 1.1 2.8 11.9 11.9 0 0 0 4.6 4c1.7.7 2.4.8 3.2.7a2.8 2.8 0 0 0 1.8-1.3 2.2 2.2 0 0 0 .2-1.3c-.1-.1-.3-.2-.5-.3z"/></svg>עדכנו אותי בוואטסאפ</a>
		<button type="button" class="nlnu-later">לא עכשיו</button>
	</div>
	<p class="nlnu-ind">אתר מידע עצמאי, לא מטעם יזם או מתווך.</p>
	<span class="nlnu-fuse" aria-hidden="true"><i></i></span>
</div>
<style id="nadlan-nudge-css">
#nlnu{position:fixed;z-index:99990;inset-inline:10px;bottom:calc(10px + env(safe-area-inset-bottom,0px));max-height:min(46vh,340px);box-sizing:border-box;background:#fff;border:1px solid #e3e1da;border-radius:22px;box-shadow:0 18px 40px rgba(16,38,47,.16),0 3px 10px rgba(16,38,47,.06);padding:7px 16px 14px;display:grid;gap:6px;touch-action:none;user-select:none;-webkit-user-select:none;font-family:Assistant,Heebo,"Segoe UI",Arial,sans-serif;color:#14212b;transform:translateY(calc(100% + 30px));opacity:0;transition:transform .42s cubic-bezier(.2,.8,.2,1),opacity .3s;overflow:hidden}
#nlnu[hidden]{display:none!important}
#nlnu.is-in{transform:translateY(0);opacity:1}
#nlnu.is-drag{transition:none}
#nlnu.is-fade{opacity:0;transition:opacity 1.2s ease}
@media(min-width:760px){#nlnu{inset-inline:auto;inset-inline-end:18px;bottom:18px;width:384px;max-height:none}}
#nlnu .nlnu-grab{justify-self:center;width:40px;height:4px;border-radius:999px;background:#e3e1da}
#nlnu .nlnu-head{display:flex;align-items:flex-start;justify-content:space-between;gap:10px}
#nlnu p{margin:0}
#nlnu .nlnu-kick{font:700 12.5px/1.3 Assistant,Heebo,sans-serif;letter-spacing:.02em;color:#2f6f86}
#nlnu .nlnu-x{flex:none;display:grid;place-items:center;width:38px;height:38px;margin:-8px 0 0 -10px;border:0;background:transparent;border-radius:999px;color:#3b4753;font:400 24px/1 Assistant,sans-serif;cursor:pointer;padding:0}
#nlnu .nlnu-perf{position:relative;display:block;height:0;border-top:1.5px dashed #e3e1da;margin:0 -16px 2px}
#nlnu .nlnu-perf::before,#nlnu .nlnu-perf::after{content:"";position:absolute;top:-8px;width:14px;height:14px;border-radius:50%;background:#f7f6f2;border:1px solid #e3e1da}
#nlnu .nlnu-perf::before{inset-inline-start:-8px}#nlnu .nlnu-perf::after{inset-inline-end:-8px}
#nlnu .nlnu-line{font:600 20px/1.22 "Noto Serif Hebrew","Frank Ruhl Libre",Georgia,serif;color:#14212b}
#nlnu .nlnu-small{font-size:13.5px;line-height:1.45;color:#3b4753}
#nlnu .nlnu-ind{font-size:12px;line-height:1.4;color:#5b6670}
#nlnu .nlnu-chips{display:flex;flex-wrap:wrap;gap:6px}
html body #nlnu a.nlnu-chip{display:inline-flex;align-items:center;min-height:36px;padding:0 12px;border-radius:999px;border:1px solid #e3e1da;background:#fff;font:700 13.5px/1 Assistant,Heebo,sans-serif;color:#14212b!important;text-decoration:none!important}
html body #nlnu a.nlnu-chip::before{content:"";width:7px;height:7px;border-radius:50%;background:#0f7a63;margin-inline-end:7px}
#nlnu .nlnu-acts{display:grid;grid-template-columns:1fr auto;gap:8px;align-items:center;margin-top:2px}
html body #nlnu a.nlnu-wa{display:flex;align-items:center;justify-content:center;gap:9px;min-height:48px;border-radius:999px;background:#0f7a63;color:#fff!important;font:700 15.5px/1.1 Assistant,Heebo,sans-serif;text-decoration:none!important;box-shadow:0 10px 24px rgba(15,122,99,.30);padding:0 14px}
#nlnu a.nlnu-wa svg{width:20px;height:20px;flex:none}
#nlnu .nlnu-later{min-height:48px;padding:0 12px;border:0;background:transparent;font:600 14.5px/1 Assistant,Heebo,sans-serif;color:#3b4753;cursor:pointer}
#nlnu .nlnu-fuse{position:absolute;bottom:0;inset-inline:22px;height:2px;border-radius:2px;background:#e3e1da;overflow:hidden}
#nlnu .nlnu-fuse i{display:block;height:100%;background:#2f6f86;transform-origin:left center}
#nlnu .nlnu-fuse i.run{animation:nlnuFuse var(--f,14s) linear forwards}
@keyframes nlnuFuse{from{transform:scaleX(1)}to{transform:scaleX(0)}}
#nlnu .nlnu-x:focus-visible,#nlnu .nlnu-later:focus-visible,#nlnu a:focus-visible{outline:2px solid #2f6f86;outline-offset:3px}
html body.nlnu-on #nlcta{opacity:0!important;pointer-events:none!important;transform:translateY(24px)!important;transition:opacity .2s,transform .3s}
/* the accessibility button stays reachable: on a phone it rises above the slip while the slip is up */
@media(max-width:759px){html body.nlnu-on #nla11y{bottom:calc(var(--nlnu-h,260px) + 22px + env(safe-area-inset-bottom,0px))!important;transition:bottom .3s}}
@media(prefers-reduced-motion:reduce){#nlnu,#nlnu.is-fade{transition:none}#nlnu .nlnu-fuse{display:none}}
</style>
<script id="nadlan-nudge-js">
(function(){
	var C=<?php echo wp_json_encode( $cfg ); ?>,el=document.getElementById('nlnu');if(!el||window.__nlnu)return;window.__nlnu=1;
	var LS={g:function(k){try{return localStorage.getItem(k)}catch(e){return null}},s:function(k,v){try{localStorage.setItem(k,v)}catch(e){}}};
	var SS={g:function(k){try{return sessionStorage.getItem(k)}catch(e){return null}},s:function(k,v){try{sessionStorage.setItem(k,v)}catch(e){}}};
	function ev(n,x){var p={project:C.p};for(var k in (x||{}))p[k]=x[k];try{if(typeof gtag==='function')gtag('event',n,p);else if(window.dataLayer)dataLayer.push({event:n,project:C.p});}catch(e){}}
	var now=Date.now(),quiet=+(LS.g('nlnu_q')||0),PV=/[?&]nudge=show(?:&|#|$)/.test(location.search);
	/* ?nudge=show: a viewing link for the owner, the slip after 2 s, whatever the holdout, the quiet days or the session say */
	if(!PV&&(quiet>now||SS.g('nlnu_s')))return;
	var b=LS.g('nlnu_b');if(b===null){b=String(Math.floor(Math.random()*100));LS.s('nlnu_b',b);}
	if(!PV&&+b<C.h){if(!SS.g('nlnu_h')){SS.s('nlnu_h','1');ev('nudge_holdout');}return;}
	var state='idle',vis=0,maxD=0,maxPx=0,lastY=window.scrollY,lastT=performance.now(),awayAt=0,waTapped=false,fadeT=null,fadeLeft=C.f*1000,fadeStart=0,drag=null;
	var fuse=el.querySelector('.nlnu-fuse i');
	document.addEventListener('click',function(e){var a=e.target&&e.target.closest&&e.target.closest('a[href*="wa.me/"]');if(a&&!el.contains(a)){waTapped=true;}},true);
	function depth(){var h=document.documentElement.scrollHeight-innerHeight;return h>0?scrollY/h:0}
	/* a long project page (Rainbow is ~28,000 px) counts screens too: 35% of the page OR 2.5 screens read */
	function deep(){return maxD>=C.dp||maxPx>=2.5*innerHeight}
	function busy(){var a=document.activeElement;if(a&&/^(INPUT|TEXTAREA|SELECT)$/.test(a.tagName))return true;if(document.fullscreenElement)return true;if(waTapped)return true;
		try{if(window.Tawk_API&&typeof Tawk_API.isChatMaximized==='function'&&Tawk_API.isChatMaximized())return true;}catch(e){}return false}
	function show(tr){
		if(state!=='idle'||(!PV&&busy()))return;state='in';if(!PV)SS.s('nlnu_s','1');
		el.hidden=false;void el.offsetWidth;document.body.style.setProperty('--nlnu-h',el.offsetHeight+'px');el.classList.add('is-in');document.body.classList.add('nlnu-on');
		ev('nudge_shown',{trigger:PV?'preview':tr});startFade();
	}
	function hide(how){
		if(state!=='in')return;state='out';clearTimeout(fadeT);
		if(!PV)LS.s('nlnu_q',String(Date.now()+(how==='wa'?C.qw:C.q)*864e5));
		if(how==='fade'){el.classList.add('is-fade');}else{el.classList.remove('is-in');}
		setTimeout(function(){el.hidden=true;el.classList.remove('is-in','is-fade');el.style.transform='';document.body.classList.remove('nlnu-on');},how==='fade'?1250:450);
		ev(how==='wa'?'nudge_wa':'nudge_close',how==='wa'?{}:{how:how});
	}
	function startFade(){fadeStart=Date.now();fuse.style.setProperty('--f',(fadeLeft/1000)+'s');fuse.classList.remove('run');void fuse.offsetWidth;fuse.classList.add('run');fuse.style.animationPlayState='running';fadeT=setTimeout(function(){hide('fade')},fadeLeft);}
	function pauseFade(){if(state!=='in'||!fadeT)return;clearTimeout(fadeT);fadeT=null;fadeLeft=Math.max(2000,fadeLeft-(Date.now()-fadeStart));fuse.style.animationPlayState='paused';}
	function resumeFade(){if(state!=='in'||fadeT||drag)return;fadeStart=Date.now();fuse.style.animationPlayState='running';fadeT=setTimeout(function(){hide('fade')},fadeLeft);}
	setInterval(function(){if(document.hidden||state!=='idle')return;vis++;if(vis>=C.d&&deep())show('time');},1000);
	addEventListener('scroll',function(){var t=performance.now(),y=scrollY,d=depth();if(d>maxD)maxD=d;if(y>maxPx)maxPx=y;var v=(lastY-y)/Math.max(1,t-lastT);if((maxD>=.5||maxPx>=4*innerHeight)&&vis>=C.d&&v>1.2)show('scroll_up');lastY=y;lastT=t;},{passive:true});
	document.addEventListener('visibilitychange',function(){if(document.hidden){awayAt=Date.now();}else if(awayAt&&Date.now()-awayAt>=20000&&vis>=C.d){show('tab_return');}});
	document.addEventListener('mouseout',function(e){if(!e.relatedTarget&&e.clientY<=0&&vis>=C.d&&deep()&&matchMedia('(pointer:fine)').matches)show('leave_desktop');});
	el.querySelector('.nlnu-x').addEventListener('click',function(){hide('button')});
	el.querySelector('.nlnu-later').addEventListener('click',function(){hide('button')});
	[].forEach.call(el.querySelectorAll('a[href*="wa.me/"]'),function(a){a.addEventListener('click',function(){ev('nudge_wa_'+a.getAttribute('data-k'));hide('wa');});});
	document.addEventListener('keydown',function(e){if(e.key==='Escape')hide('esc')});
	el.addEventListener('pointerenter',pauseFade);el.addEventListener('pointerleave',resumeFade);el.addEventListener('focusin',pauseFade);el.addEventListener('focusout',resumeFade);
	el.addEventListener('pointerdown',function(e){if(e.target.closest('a,button'))return;pauseFade();drag={y0:e.clientY,t0:performance.now(),dy:0};el.classList.add('is-drag');try{el.setPointerCapture(e.pointerId)}catch(x){}});
	el.addEventListener('pointermove',function(e){if(!drag)return;var d=e.clientY-drag.y0;drag.dy=Math.max(0,d);el.style.transform='translateY('+(d<0?d*.25:d)+'px)';});
	function end(){if(!drag)return;var h=el.offsetHeight,v=drag.dy/Math.max(1,performance.now()-drag.t0);el.classList.remove('is-drag');
		if(drag.dy>h*.35||v>.5){el.style.transform='translateY('+(h+40)+'px)';drag=null;hide('swipe');}else{el.style.transform='';drag=null;resumeFade();}}
	el.addEventListener('pointerup',end);el.addEventListener('pointercancel',end);
	if(PV)setTimeout(function(){show('preview')},2000);
})();
</script>
	<?php
}, 40 );
