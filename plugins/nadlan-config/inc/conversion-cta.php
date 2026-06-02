<?php
/**
 * nadlan-config — Conversion CTA layer (v1.40.0 / shark idea #1, #2, #5, #6)
 *
 * Four sitewide revenue-capture surfaces, lazy-loaded and dismissible:
 *  - Sticky bottom CTA bar (mobile + desktop) → mortgage-advisor lead
 *  - Exit-intent modal (desktop) → free-consult lead
 *  - WhatsApp click-to-chat floating button (uses owner phone option)
 *  - GA4 dataLayer events on every conversion touch (claim, quote, upgrade,
 *    review, sticky-cta, exit-intent, whatsapp). Funnel visible in Site Kit/GA4.
 *
 * All leads land in the existing /nadlan/v1/lead REST endpoint → nadlan_lead CPT
 * → owner gets the email. Zero spam to contractors. Honeypot + rate limit free
 * because the upstream endpoint already enforces them.
 *
 * Settings: option `nadlan_owner_whatsapp` (E.164 phone, default empty = hidden);
 * NADLAN_DISABLE_CONVERSION_CTA constant to kill the whole layer if needed.
 */
if ( ! defined( 'ABSPATH' ) ) { exit; }

if ( ! function_exists( 'nadlan_cta_enabled' ) ) {
	function nadlan_cta_enabled() {
		if ( defined( 'NADLAN_DISABLE_CONVERSION_CTA' ) && NADLAN_DISABLE_CONVERSION_CTA ) { return false; }
		if ( is_admin() || is_user_logged_in() ) { return false; }
		// don't double-render on the AI concierge widget's own pages or on REST
		if ( defined( 'REST_REQUEST' ) && REST_REQUEST ) { return false; }
		return true;
	}
}

if ( ! function_exists( 'nadlan_cta_whatsapp_number' ) ) {
	function nadlan_cta_whatsapp_number() {
		$raw = (string) get_option( 'nadlan_owner_whatsapp', '' );
		$raw = preg_replace( '/[^0-9+]/', '', $raw );
		return $raw;
	}
}

add_action( 'wp_footer', function () {
	if ( ! nadlan_cta_enabled() ) { return; }
	$wa = nadlan_cta_whatsapp_number();
	$lead_rest = esc_js( rest_url( 'nadlan/v1/lead' ) );
	?>
<div id="nlcta" dir="rtl" data-lead="<?php echo $lead_rest; ?>">
	<!-- sticky bottom bar -->
	<div class="nlcta-bar" hidden>
		<button class="nlcta-bar-close" aria-label="סגור">×</button>
		<strong>חוסכים על משכנתא?</strong>
		<span>בדיקה חינם תוך 60 שניות.</span>
		<button class="nlcta-bar-cta" type="button">בדקו עכשיו</button>
	</div>
	<!-- exit-intent modal -->
	<div class="nlcta-modal-wrap" hidden role="dialog" aria-modal="true" aria-labelledby="nlcta-mh">
		<div class="nlcta-modal">
			<button class="nlcta-modal-x" aria-label="סגור">×</button>
			<div class="nlcta-modal-eyebrow">לפני שאתם הולכים</div>
			<h3 id="nlcta-mh">בדיקה ראשונית חינם</h3>
			<p>השאירו פרטים — נחזור אליכם תוך 24 שעות עם בדיקה ראשונית של העסקה / המשכנתא / הזכויות.</p>
			<form class="nlcta-form">
				<input type="text" name="name" placeholder="שם מלא" required>
				<input type="tel" name="phone" placeholder="טלפון" required>
				<input type="text" name="company" class="nlcta-hp" tabindex="-1" autocomplete="off" aria-hidden="true">
				<button type="submit">שליחה</button>
				<span class="nlcta-msg" aria-live="polite"></span>
			</form>
			<small>פרטיכם לא יועברו לצד שלישי ללא אישורכם.</small>
		</div>
	</div>
	<?php if ( $wa ) : ?>
	<!-- WhatsApp click-to-chat -->
	<a class="nlcta-wa" href="https://wa.me/<?php echo esc_attr( $wa ); ?>?text=<?php echo rawurlencode( 'שלום, ראיתי את האתר נדל"ן חכם ואשמח להתייעצות.' ); ?>" target="_blank" rel="noopener" aria-label="WhatsApp">
		<svg viewBox="0 0 24 24" width="22" height="22" fill="#fff"><path d="M12.04 2c-5.46 0-9.91 4.45-9.91 9.91 0 1.75.46 3.45 1.32 4.95L2 22l5.25-1.38a9.9 9.9 0 0 0 4.79 1.22h.01c5.46 0 9.91-4.45 9.91-9.91 0-2.65-1.03-5.14-2.9-7.01A9.85 9.85 0 0 0 12.04 2zm0 18.15h-.01a8.22 8.22 0 0 1-4.19-1.15l-.3-.18-3.11.82.83-3.04-.2-.31a8.22 8.22 0 0 1-1.26-4.38c0-4.54 3.7-8.24 8.25-8.24 2.2 0 4.27.86 5.83 2.42a8.18 8.18 0 0 1 2.41 5.83c0 4.54-3.7 8.24-8.25 8.24zm4.52-6.16c-.25-.12-1.47-.72-1.7-.81-.22-.08-.39-.12-.55.13-.16.25-.62.81-.76.97-.14.17-.28.19-.53.06-.25-.13-1.05-.39-2-1.23a7.5 7.5 0 0 1-1.38-1.72c-.14-.25-.02-.38.11-.51.11-.11.25-.29.37-.43.12-.14.16-.25.25-.41.08-.16.04-.31-.02-.43-.06-.12-.55-1.33-.76-1.83-.2-.48-.4-.41-.55-.42l-.47-.01c-.16 0-.42.06-.64.31-.22.25-.84.82-.84 2.01s.86 2.33.98 2.49c.12.16 1.7 2.6 4.13 3.65.58.25 1.02.4 1.37.51.58.18 1.1.16 1.52.1.46-.07 1.47-.6 1.68-1.18.21-.58.21-1.07.14-1.18-.06-.1-.23-.16-.48-.29z"/></svg>
	</a>
	<?php endif; ?>
</div>
<style>
#nlcta{font-family:var(--font-sans,Heebo,system-ui,sans-serif);direction:rtl}
/* sticky bar */
.nlcta-bar{position:fixed;inset-block-end:0;inset-inline-start:0;inset-inline-end:0;z-index:99990;display:flex;align-items:center;gap:12px;padding:12px 18px;background:linear-gradient(135deg,#1B1A17,#3a3329);color:#fff;box-shadow:0 -8px 24px rgba(0,0,0,.18);animation:nlctaSlideUp .35s ease-out}
.nlcta-bar strong{font-size:14px}.nlcta-bar span{font-size:13px;color:rgba(255,255,255,.78);flex:1}
.nlcta-bar-close{background:none;border:0;color:rgba(255,255,255,.7);font-size:22px;cursor:pointer;line-height:1;padding:0 4px}
.nlcta-bar-cta{background:linear-gradient(135deg,#9C7A3C,#B89254);color:#fff;border:0;border-radius:8px;padding:10px 18px;font:inherit;font-weight:700;font-size:13.5px;cursor:pointer;white-space:nowrap}
.nlcta-bar-cta:hover{filter:brightness(1.08)}
@keyframes nlctaSlideUp{from{transform:translateY(100%)}to{transform:none}}
@media(max-width:520px){.nlcta-bar{flex-wrap:wrap;padding:10px 14px}.nlcta-bar span{flex:1 1 100%;font-size:12px}}
/* exit modal */
.nlcta-modal-wrap{position:fixed;inset:0;z-index:99991;background:rgba(0,0,0,.55);display:flex;align-items:center;justify-content:center;padding:20px;backdrop-filter:blur(4px);animation:nlctaFade .25s}
.nlcta-modal{background:#fff;max-width:440px;width:100%;border-radius:18px;padding:30px;box-shadow:0 30px 70px rgba(0,0,0,.35);position:relative;animation:nlctaPop .3s cubic-bezier(.2,.8,.2,1)}
@keyframes nlctaFade{from{opacity:0}}
@keyframes nlctaPop{from{transform:scale(.94);opacity:0}to{transform:none;opacity:1}}
.nlcta-modal-x{position:absolute;inset-block-start:14px;inset-inline-end:14px;background:none;border:0;font-size:26px;color:#9a9a9a;cursor:pointer;line-height:1}
.nlcta-modal-eyebrow{font-size:11px;letter-spacing:.16em;color:#9C7A3C;font-weight:700;text-transform:uppercase;margin-bottom:6px}
.nlcta-modal h3{font-family:var(--font-serif,"Frank Ruhl Libre",serif);font-size:24px;font-weight:600;color:#1B1A17;margin:0 0 10px}
.nlcta-modal p{font-size:14px;color:#5a5a5a;line-height:1.6;margin:0 0 18px}
.nlcta-form{display:grid;gap:9px}
.nlcta-form input[type=text],.nlcta-form input[type=tel]{border:1px solid rgba(27,26,23,.16);border-radius:10px;padding:12px;font:inherit}
.nlcta-form button[type=submit]{background:linear-gradient(135deg,#9C7A3C,#B89254);color:#fff;border:0;border-radius:10px;padding:13px;font:inherit;font-weight:700;cursor:pointer}
.nlcta-hp{position:absolute;left:-9999px;width:1px;opacity:0}
.nlcta-msg{font-size:13px;padding-top:4px;color:#059669}.nlcta-msg.is-err{color:#B91C1C}
.nlcta-modal small{display:block;margin-top:12px;font-size:11px;color:#9a9a9a}
/* whatsapp */
.nlcta-wa{position:fixed;inset-block-end:78px;inset-inline-end:20px;z-index:99989;width:56px;height:56px;border-radius:50%;background:#25D366;display:grid;place-items:center;box-shadow:0 10px 28px rgba(37,211,102,.5);transition:transform .2s,box-shadow .2s}
.nlcta-wa:hover{transform:translateY(-3px);box-shadow:0 14px 36px rgba(37,211,102,.6)}
@media(max-width:520px){.nlcta-wa{inset-block-end:84px;inset-inline-end:14px;width:50px;height:50px}}
</style>
<script>
(function(){
	var root=document.getElementById('nlcta');if(!root)return;
	var LEAD=root.dataset.lead;
	var bar=root.querySelector('.nlcta-bar'),modalWrap=root.querySelector('.nlcta-modal-wrap');
	var modalShown=sessionStorage.getItem('nlcta_modal')==='1';
	var barShown=sessionStorage.getItem('nlcta_bar')==='1';
	function ga(name,payload){try{(window.dataLayer=window.dataLayer||[]).push(Object.assign({event:name},payload||{}));}catch(e){}}
	// expose for other plugin scripts (claim/upgrade/review buttons)
	window.nadlanGA=window.nadlanGA||ga;
	function showBar(){if(barShown||!bar)return;bar.hidden=false;ga('cta_bar_shown',{location:location.pathname});}
	function showModal(){if(modalShown||!modalWrap)return;modalWrap.hidden=false;modalShown=true;sessionStorage.setItem('nlcta_modal','1');ga('cta_exit_intent_shown');}
	// sticky bar: show after 7s on first session page
	setTimeout(showBar,7000);
	if(bar){
		bar.querySelector('.nlcta-bar-close').addEventListener('click',function(){bar.hidden=true;sessionStorage.setItem('nlcta_bar','1');ga('cta_bar_dismissed');});
		bar.querySelector('.nlcta-bar-cta').addEventListener('click',function(){ga('cta_bar_click');showModal();});
	}
	// exit intent (desktop only — mouseleave to top)
	if(window.matchMedia&&!window.matchMedia('(pointer:coarse)').matches){
		document.addEventListener('mouseout',function(e){if(!e.relatedTarget&&e.clientY<20)showModal();});
	}
	// modal interactions
	if(modalWrap){
		var form=modalWrap.querySelector('.nlcta-form'),msg=modalWrap.querySelector('.nlcta-msg');
		modalWrap.querySelector('.nlcta-modal-x').addEventListener('click',function(){modalWrap.hidden=true;ga('cta_modal_dismissed');});
		modalWrap.addEventListener('click',function(e){if(e.target===modalWrap){modalWrap.hidden=true;ga('cta_modal_dismissed');}});
		form.addEventListener('submit',function(e){
			e.preventDefault();
			var fd=new FormData(form),data={topic:'בדיקה ראשונית — exit intent'};
			fd.forEach(function(v,k){data[k]=v;});
			if(data.company){return;} // honeypot
			msg.className='nlcta-msg';msg.textContent='שולח…';
			fetch(LEAD,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({name:data.name,phone:data.phone,goal:'בדיקה ראשונית',message:'מקור: '+location.pathname,source:'exit-intent'})})
				.then(function(r){return r.json();})
				.then(function(d){msg.textContent=(d&&d.ok!==false)?'✓ תודה! נחזור אליכם בהקדם.':'שגיאה. נסו שוב.';if(d)ga('cta_lead_submitted',{src:'exit_intent'});form.reset();setTimeout(function(){modalWrap.hidden=true;},2200);})
				.catch(function(){msg.className='nlcta-msg is-err';msg.textContent='שגיאת רשת.';});
		});
	}
	// WhatsApp click → GA
	var wa=root.querySelector('.nlcta-wa');if(wa)wa.addEventListener('click',function(){ga('whatsapp_click');});
})();
</script>
	<?php
}, 90 );

/* Public lead REST endpoint — wraps the existing handler so a JSON POST works
 * (the legacy admin_post one needs form fields + nonce). Owner gets email. */
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

/* Settings page for the WhatsApp number + CTA toggles */
add_action( 'admin_menu', function () {
	add_options_page( 'NadLan CTA + WhatsApp', 'NadLan CTA', 'manage_options', 'nadlan-cta', function () {
		if ( ! current_user_can( 'manage_options' ) ) { return; }
		if ( ! empty( $_POST['nadlan_cta_save'] ) && check_admin_referer( 'nadlan_cta_save' ) ) {
			update_option( 'nadlan_owner_whatsapp', preg_replace( '/[^0-9+]/', '', sanitize_text_field( wp_unslash( $_POST['wa'] ?? '' ) ) ) );
			echo '<div class="notice notice-success"><p>נשמר.</p></div>';
		}
		$wa = (string) get_option( 'nadlan_owner_whatsapp', '' );
		echo '<div class="wrap" style="direction:rtl;font-family:Heebo,sans-serif"><h1>NadLan CTA + WhatsApp</h1>';
		echo '<form method="post">';
		wp_nonce_field( 'nadlan_cta_save' );
		echo '<table class="form-table"><tr><th>WhatsApp Number (E.164)</th><td><input type="text" name="wa" value="' . esc_attr( $wa ) . '" placeholder="972501234567" style="width:280px"> <br><small>מספר טלפון להפנייה ל-WhatsApp. דוגמה: 972501234567. ריק = יוסתר.</small></td></tr></table>';
		echo '<p class="submit"><button type="submit" name="nadlan_cta_save" class="button-primary">שמור</button></p></form></div>';
	} );
} );
