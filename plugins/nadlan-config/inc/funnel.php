<?php
/**
 * nadlan-config - B2B funnel de-friction (owner god-mission 2026-07-06).
 *
 * 1) QUICK REGISTER: one small form on the listing-wizard gate creates the
 *    account and signs the visitor in on the spot - no email round-trip, no
 *    WP admin screens. Email verification can follow; the listing cannot be
 *    lost to a password email. Rate-limited + honeypot.
 * 2) /pricing/ belongs to the commercial offer: 301 to /join-pro/ (WordPress
 *    was slug-guessing it onto an article about apartment pricing).
 * 3) ADVERTISER APPLICATION: a native lead form appended to the /advertise/
 *    page so a developer who will not open WhatsApp still converts.
 */

if ( ! defined( 'ABSPATH' ) ) { exit; }

/* ---------------- 1) quick register ---------------- */
add_action( 'rest_api_init', function () {
	register_rest_route( 'nadlan/v1', '/quick-register', array(
		'methods' => 'POST', 'permission_callback' => '__return_true',
		'callback' => function ( WP_REST_Request $req ) {
			if ( is_user_logged_in() ) { return new WP_REST_Response( array( 'ok' => true, 'already' => true ), 200 ); }
			if ( ! get_option( 'users_can_register' ) ) { return new WP_REST_Response( array( 'ok' => false, 'error' => 'registration_closed' ), 403 ); }
			$p = $req->get_json_params();
			// honeypot: bots fill every field
			if ( '' !== trim( (string) ( $p['website'] ?? '' ) ) ) { return new WP_REST_Response( array( 'ok' => true ), 200 ); }
			$ip  = preg_replace( '/[^0-9a-f\.\:]/i', '', (string) ( $_SERVER['REMOTE_ADDR'] ?? '' ) );
			$rk  = 'nlqr_' . md5( $ip );
			$hits = (int) get_transient( $rk );
			if ( $hits >= 5 ) { return new WP_REST_Response( array( 'ok' => false, 'error' => 'rate_limited' ), 429 ); }
			set_transient( $rk, $hits + 1, HOUR_IN_SECONDS );
			$name  = sanitize_text_field( (string) ( $p['name'] ?? '' ) );
			$email = sanitize_email( (string) ( $p['email'] ?? '' ) );
			$phone = preg_replace( '/[^0-9+]/', '', (string) ( $p['phone'] ?? '' ) );
			if ( ! is_email( $email ) ) { return new WP_REST_Response( array( 'ok' => false, 'error' => 'bad_email' ), 400 ); }
			if ( email_exists( $email ) ) { return new WP_REST_Response( array( 'ok' => false, 'error' => 'exists', 'login_url' => wp_login_url( (string) ( $p['back'] ?? home_url( '/post-listing/' ) ) ) ), 409 ); }
			$uid = wp_create_user( $email, wp_generate_password( 24 ), $email );
			if ( is_wp_error( $uid ) ) { return new WP_REST_Response( array( 'ok' => false, 'error' => 'create_failed' ), 500 ); }
			if ( $name !== '' ) { wp_update_user( array( 'ID' => $uid, 'display_name' => $name, 'first_name' => $name ) ); }
			if ( $phone !== '' ) { update_user_meta( $uid, 'phone', $phone ); }
			update_user_meta( $uid, 'nadlan_quick_registered', time() );
			wp_set_current_user( $uid );
			wp_set_auth_cookie( $uid, true );
			// password-reset email doubles as the "set your password" path
			if ( function_exists( 'wp_send_new_user_notifications' ) ) { wp_send_new_user_notifications( $uid, 'user' ); }
			return new WP_REST_Response( array( 'ok' => true ), 200 );
		},
	) );
} );

/* ---------------- 2) /pricing/ -> /join-pro/ ---------------- */
add_action( 'template_redirect', function () {
	$path = trim( (string) parse_url( (string) ( $_SERVER['REQUEST_URI'] ?? '' ), PHP_URL_PATH ), '/' );
	if ( 'pricing' === $path ) { wp_redirect( home_url( '/join-pro/' ), 301 ); exit; }
}, 1 );

/* ---------------- 3) advertiser application on /advertise/ ---------------- */
if ( ! function_exists( 'nadlan_funnel_advertiser_form' ) ) {
	function nadlan_funnel_advertiser_form() {
		$rest = esc_url( rest_url( 'nadlan/v1/lead' ) );
		ob_start(); ?>
<section class="nladv" id="nladv-form" data-rest="<?php echo esc_attr( $rest ); ?>" dir="rtl">
	<h2>נחזור אליכם עוד היום</h2>
	<p class="nladv-sub">השאירו פרטים ונציג יחזור עם הצעה מותאמת לפרויקט או לעסק שלכם. בלי התחייבות.</p>
	<div class="nladv-grid">
		<label>שם מלא<input type="text" id="nladv-name" autocomplete="name"></label>
		<label>טלפון<input type="tel" id="nladv-phone" autocomplete="tel" inputmode="tel"></label>
		<label class="nladv-full">מה מעניין אתכם?<select id="nladv-topic">
			<option value="project-flag">חוויית דגל תלת ממדית לפרויקט</option>
			<option value="project-claim">בעלות על עמוד פרויקט קיים</option>
			<option value="pro-tier">מסלול Pro / Premier לבעלי מקצוע</option>
			<option value="listing">פרסום נכסים</option>
			<option value="other">אחר</option>
		</select></label>
		<input type="text" id="nladv-web" tabindex="-1" autocomplete="off" style="position:absolute;left:-9999px" aria-hidden="true">
	</div>
	<button type="button" class="nladv-btn" id="nladv-send">שלחו ונחזור אליכם ←</button>
	<p class="nladv-msg" id="nladv-msg" hidden></p>
</section>
<style>
.nladv{max-width:640px;margin:34px auto 10px;background:#fff;border:1px solid #D6C189;border-radius:18px;padding:26px 28px;box-shadow:0 18px 44px -24px rgba(27,26,23,.35);font-family:Heebo,system-ui,sans-serif}
.nladv h2{font-family:"Frank Ruhl Libre",serif;color:#1B1A17;margin:0 0 4px;font-size:1.5rem}
.nladv-sub{color:#6D665C;font-size:14px;margin:0 0 16px}
.nladv-grid{display:grid;grid-template-columns:1fr 1fr;gap:12px}
.nladv-grid label{display:flex;flex-direction:column;gap:5px;font-size:13px;color:#51483A;font-weight:600}
.nladv-full{grid-column:1/-1}
.nladv-grid input,.nladv-grid select{border:1px solid #E2DCD0;border-radius:10px;padding:11px 12px;font:inherit;background:#FAF7F1}
.nladv-grid input:focus,.nladv-grid select:focus{outline:none;border-color:#9C7A3C}
.nladv-btn{margin-top:16px;width:100%;background:#9C7A3C;color:#FAF7F1;font:700 15px/1 Heebo,sans-serif;border:0;border-radius:12px;padding:15px;cursor:pointer;transition:background .2s}
.nladv-btn:hover{background:#8a6a30}
.nladv-msg{margin-top:12px;font-size:14px;color:#517048;font-weight:600}
@media(max-width:560px){.nladv-grid{grid-template-columns:1fr}}
</style>
<script>
(function(){
	var b=document.getElementById("nladv-send");if(!b)return;
	b.addEventListener("click",function(){
		var n=document.getElementById("nladv-name").value.trim(),
			p=document.getElementById("nladv-phone").value.trim(),
			t=document.getElementById("nladv-topic").value,
			w=document.getElementById("nladv-web").value,
			m=document.getElementById("nladv-msg");
		if(!n||p.replace(/\D/g,"").length<8){m.hidden=false;m.style.color="#C2563A";m.textContent="צריך שם וטלפון תקין כדי שנחזור אליכם.";return}
		if(w){m.hidden=false;m.style.color="#517048";m.textContent="קיבלנו, נחזור אליכם בהקדם.";return}
		b.disabled=true;b.textContent="שולחים...";
		fetch(document.getElementById("nladv-form").dataset.rest,{method:"POST",headers:{"Content-Type":"application/json"},
			body:JSON.stringify({name:n,phone:p,source:"advertise-page",context:"advertiser:"+t,url:location.href})})
		.then(function(r){return r.json()}).then(function(){
			m.hidden=false;m.style.color="#517048";m.textContent="קיבלנו! נציג יחזור אליכם עוד היום בשעות הפעילות.";
			b.textContent="נשלח ✓";
		}).catch(function(){
			b.disabled=false;b.textContent="שלחו ונחזור אליכם ←";
			m.hidden=false;m.style.color="#C2563A";m.textContent="משהו השתבש - אפשר גם בוואטסאפ למטה.";
		});
	});
})();
</script>
<?php
		return ob_get_clean();
	}
}
add_filter( 'the_content', function ( $content ) {
	if ( is_page( 'advertise' ) && ! is_admin() ) { return $content . nadlan_funnel_advertiser_form(); }
	return $content;
}, 20 );

/* ---------------- 4) the free first month is TRUE (owner 2026-07-06) ----------------
 * Pro (product 476) promises a free first month. Instead of charging 349 at
 * checkout, a one-per-customer 100% coupon auto-applies so the first order is
 * a genuine 0 - no card needed. Month 2 is billed by the renewal engine
 * (inc/renewals.php) at full price. Premier stays paid-now by design. */
add_action( 'woocommerce_before_calculate_totals', function ( $cart ) {
	if ( is_admin() || ! $cart || $cart->has_discount( 'firstmonth' ) ) { return; }
	foreach ( $cart->get_cart() as $item ) {
		if ( (int) ( $item['product_id'] ?? 0 ) === 476 ) { $cart->apply_coupon( 'firstmonth' ); return; }
	}
}, 20 );

/* ---------------- 5) /join-pro/ belongs to the CMS again ----------------
 * The theme's functions.php (premium-revenue era, June 2026) still swaps the
 * whole join-pro page for a hardcoded nlrx pricing template via a the_content
 * filter at priority 98 - so editor changes to the page never render. The page
 * is now authored in the CMS (DNA rebuild 2026-07-07). At priority 99, restore
 * the real post content - but only while it carries the authored-page marker,
 * so a blanked page still falls back to the theme template instead of showing
 * nothing. */
add_filter( 'the_content', function ( $content ) {
	if ( is_page( 'join-pro' ) && in_the_loop() && is_main_query() ) {
		$raw = get_post_field( 'post_content', get_queried_object_id() );
		if ( $raw && false !== strpos( $raw, 'nadlan-joinpro' ) ) {
			return do_blocks( $raw );
		}
	}
	return $content;
}, 99 );
