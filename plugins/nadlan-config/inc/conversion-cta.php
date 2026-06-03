<?php
/**
 * nadlan-config — Conversion CTA layer (v1.40.3)
 *
 * STRIPPED 2026-06-03 per owner: the sticky bottom bar AND the exit-intent modal
 * are KILLED everywhere (mobile + desktop). They were too intrusive on mobile
 * (mouseout-based exit detection fired on scroll, sticky bar jumped the layout).
 *
 * What remains:
 *   - Floating WhatsApp click-to-chat button (owner-controlled via Settings → NadLan CTA)
 *   - window.nadlanGA() dataLayer helper (other plugin scripts depend on it)
 *   - /nadlan/v1/lead REST endpoint (still used by claim-prompt, AI concierge handoff, etc.)
 *   - Settings page for the WhatsApp number
 *
 * If we ever want the popup/sticky back, restore from git history of this file
 * (last good version: v1.40.2). Don't re-introduce them without a UX plan.
 */
if ( ! defined( 'ABSPATH' ) ) { exit; }

if ( ! function_exists( 'nadlan_cta_enabled' ) ) {
	function nadlan_cta_enabled() {
		if ( defined( 'NADLAN_DISABLE_CONVERSION_CTA' ) && NADLAN_DISABLE_CONVERSION_CTA ) { return false; }
		if ( is_admin() || is_user_logged_in() ) { return false; }
		if ( defined( 'REST_REQUEST' ) && REST_REQUEST ) { return false; }
		return true;
	}
}

if ( ! function_exists( 'nadlan_cta_whatsapp_number' ) ) {
	function nadlan_cta_whatsapp_number() {
		$raw = (string) get_option( 'nadlan_owner_whatsapp', '' );
		return preg_replace( '/[^0-9+]/', '', $raw );
	}
}

add_action( 'wp_footer', function () {
	if ( ! nadlan_cta_enabled() ) { return; }
	$wa = nadlan_cta_whatsapp_number();
	if ( ! $wa ) {
		// No WhatsApp configured — still emit the GA helper so other modules can use it.
		echo "<script>window.dataLayer=window.dataLayer||[];window.nadlanGA=window.nadlanGA||function(n,p){try{window.dataLayer.push(Object.assign({event:n},p||{}));}catch(e){}};</script>\n";
		return;
	}
	?>
<div id="nlcta" dir="rtl">
	<a class="nlcta-wa" href="https://wa.me/<?php echo esc_attr( $wa ); ?>?text=<?php echo rawurlencode( 'שלום, ראיתי את האתר נדל"ן חכם ואשמח להתייעצות.' ); ?>" target="_blank" rel="noopener" aria-label="WhatsApp">
		<svg viewBox="0 0 24 24" width="22" height="22" fill="#fff"><path d="M12.04 2c-5.46 0-9.91 4.45-9.91 9.91 0 1.75.46 3.45 1.32 4.95L2 22l5.25-1.38a9.9 9.9 0 0 0 4.79 1.22h.01c5.46 0 9.91-4.45 9.91-9.91 0-2.65-1.03-5.14-2.9-7.01A9.85 9.85 0 0 0 12.04 2zm0 18.15h-.01a8.22 8.22 0 0 1-4.19-1.15l-.3-.18-3.11.82.83-3.04-.2-.31a8.22 8.22 0 0 1-1.26-4.38c0-4.54 3.7-8.24 8.25-8.24 2.2 0 4.27.86 5.83 2.42a8.18 8.18 0 0 1 2.41 5.83c0 4.54-3.7 8.24-8.25 8.24zm4.52-6.16c-.25-.12-1.47-.72-1.7-.81-.22-.08-.39-.12-.55.13-.16.25-.62.81-.76.97-.14.17-.28.19-.53.06-.25-.13-1.05-.39-2-1.23a7.5 7.5 0 0 1-1.38-1.72c-.14-.25-.02-.38.11-.51.11-.11.25-.29.37-.43.12-.14.16-.25.25-.41.08-.16.04-.31-.02-.43-.06-.12-.55-1.33-.76-1.83-.2-.48-.4-.41-.55-.42l-.47-.01c-.16 0-.42.06-.64.31-.22.25-.84.82-.84 2.01s.86 2.33.98 2.49c.12.16 1.7 2.6 4.13 3.65.58.25 1.02.4 1.37.51.58.18 1.1.16 1.52.1.46-.07 1.47-.6 1.68-1.18.21-.58.21-1.07.14-1.18-.06-.1-.23-.16-.48-.29z"/></svg>
	</a>
</div>
<style>
#nlcta{position:fixed;bottom:20px;inset-inline-end:20px;z-index:99989;font-family:var(--font-sans,Heebo,system-ui,sans-serif);direction:rtl}
.nlcta-wa{display:grid;place-items:center;width:56px;height:56px;border-radius:50%;background:#25D366;box-shadow:0 10px 28px rgba(37,211,102,.5);transition:transform .2s,box-shadow .2s}
.nlcta-wa:hover{transform:translateY(-3px);box-shadow:0 14px 36px rgba(37,211,102,.6)}
@media(max-width:520px){#nlcta{bottom:14px;inset-inline-end:14px}.nlcta-wa{width:50px;height:50px}}
</style>
<script>
(function(){
	window.dataLayer=window.dataLayer||[];
	window.nadlanGA=window.nadlanGA||function(n,p){try{window.dataLayer.push(Object.assign({event:n},p||{}));}catch(e){}};
	var wa=document.querySelector('.nlcta-wa');
	if(wa)wa.addEventListener('click',function(){window.nadlanGA('whatsapp_click');});
})();
</script>
	<?php
}, 90 );

/* Public lead REST endpoint — kept (used by other modules: claim-prompt, AI concierge, etc.) */
add_action( 'rest_api_init', function () {
	register_rest_route( 'nadlan/v1', '/lead', array(
		'methods'             => 'POST',
		'permission_callback' => '__return_true',
		'callback'            => function ( $req ) {
			$p = $req->get_json_params() ?: array();
			$name  = sanitize_text_field( (string) ( $p['name'] ?? '' ) );
			$phone = preg_replace( '/[^0-9+]/', '', (string) ( $p['phone'] ?? '' ) );
			$email = sanitize_email( (string) ( $p['email'] ?? '' ) );
			$goal  = sanitize_text_field( (string) ( $p['goal'] ?? ( $p['topic'] ?? '' ) ) );
			$msg   = sanitize_textarea_field( (string) ( $p['message'] ?? '' ) );
			$src   = sanitize_text_field( (string) ( $p['source'] ?? '' ) );
			$hp    = (string) ( $p['company'] ?? '' );
			if ( $hp !== '' ) { return new WP_Error( 'spam', 'spam' ); }
			if ( ! $name || ( ! $phone && ! $email ) ) { return new WP_Error( 'invalid', 'נדרשים שם וטלפון.' ); }
			$ip = $_SERVER['REMOTE_ADDR'] ?? '0';
			$tk = 'nadlan_lead_rl_' . md5( $ip );
			$ct = (int) get_transient( $tk );
			if ( $ct >= 8 ) { return new WP_Error( 'rate', 'יותר מדי בקשות.' ); }
			set_transient( $tk, $ct + 1, HOUR_IN_SECONDS );
			$lid = wp_insert_post( array(
				'post_type'    => 'nadlan_lead',
				'post_status'  => 'private',
				'post_title'   => $name . ' — ' . ( $goal ?: 'general' ) . ' — ' . current_time( 'Y-m-d H:i' ),
				'post_content' => $msg,
			), true );
			if ( is_wp_error( $lid ) ) { return $lid; }
			update_post_meta( $lid, 'name', $name );
			update_post_meta( $lid, 'phone', $phone );
			if ( $email ) { update_post_meta( $lid, 'email', $email ); }
			update_post_meta( $lid, 'goal', $goal );
			if ( $src ) { update_post_meta( $lid, 'utm_source', $src ); }
			$admin = get_option( 'admin_email' );
			if ( $admin ) {
				$body  = "ליד חדש מהאתר\n\nשם: $name\nטלפון: $phone\nאימייל: $email\nנושא: $goal\nמקור: $src\n\nהודעה: $msg\n\n";
				$body .= "ניהול: " . admin_url( 'post.php?post=' . $lid . '&action=edit' );
				wp_mail( $admin, '[נדל"ן חכם] ליד חדש — ' . $name, $body );
			}
			return array( 'ok' => true, 'lead_id' => $lid );
		},
	) );
} );

/* Settings page — kept (for the WhatsApp number) */
add_action( 'admin_menu', function () {
	add_options_page( 'NadLan CTA + WhatsApp', 'NadLan CTA', 'manage_options', 'nadlan-cta', function () {
		if ( ! current_user_can( 'manage_options' ) ) { return; }
		if ( ! empty( $_POST['nadlan_cta_save'] ) && check_admin_referer( 'nadlan_cta_save' ) ) {
			update_option( 'nadlan_owner_whatsapp', preg_replace( '/[^0-9+]/', '', sanitize_text_field( wp_unslash( $_POST['wa'] ?? '' ) ) ) );
			echo '<div class="notice notice-success"><p>נשמר.</p></div>';
		}
		$wa = (string) get_option( 'nadlan_owner_whatsapp', '' );
		echo '<div class="wrap" style="direction:rtl;font-family:Heebo,sans-serif"><h1>NadLan CTA + WhatsApp</h1>';
		echo '<p style="background:#fff;border-inline-start:4px solid #DC2626;padding:10px 14px;color:#5a5a5a">הסטיקי-בר וה-pop-up בוטלו ב-v1.40.3 לבקשת הבעלים. נשאר רק כפתור WhatsApp צף.</p>';
		echo '<form method="post">';
		wp_nonce_field( 'nadlan_cta_save' );
		echo '<table class="form-table"><tr><th>WhatsApp Number (E.164)</th><td><input type="text" name="wa" value="' . esc_attr( $wa ) . '" style="width:280px" placeholder="972501234567"> <br><small>מספר טלפון להפנייה ל-WhatsApp. ריק = הכפתור יוסתר.</small></td></tr></table>';
		echo '<p class="submit"><button type="submit" name="nadlan_cta_save" class="button-primary">שמור</button></p></form></div>';
	} );
} );
