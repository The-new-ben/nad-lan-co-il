<?php
/**
 * PricelistForm: "קבלו מחירון ותוכניות", the short lead form on the pages that bring the traffic (HAD-445, 6.10.2026).
 *
 * Why: the audit of 6.10.2026 found no form on the home page, /projects/, DUO, Rainbow, /sde-dov/ and /sde-dov/prices/,
 * only the WhatsApp pill, and lead_e2e received 0 leads in 7 days.
 *
 * What: two fields (name, phone) and one button, built from the design system's own form component (nlds.css:
 * .nlds-form, .nlds-field, .nlds-btn--primary), RTL, phone first. No new library.
 *
 * The lead path is the existing one, nothing new: POST /wp-json/nadlan/v1/lead (inc/conversion-cta.php), the same endpoint
 * the smart form, the calculators, the showroom and the claim prompt use. With lead_e2e on (it is, live) the endpoint hands
 * the lead to nadlan_lead_e2e_capture(): the nadlan_lead post, routing to the card owner, the admin notice, the visitor ack,
 * lead_ai and lead_nurture. Its protection is the one every public form on the site uses: the "company" honeypot, 8 posts per
 * IP per hour, server-side validation and the idempotency guard. No nonce: these pages are served from the page cache, and a
 * nonce printed into a cached page goes stale within a day; WordPress core then rejects the request (rest_cookie_invalid_nonce,
 * 403) for an anonymous visitor. The nonce-protected admin-post path (nadlan_lead) is not used for the same reason, and it
 * redirects the visitor to the home page.
 *
 * Where (each attach point fails open: no hook, no form, the page stays as it was):
 *  - home:      filter nadlan_hp_after_projects (inc/home-v3.php), right after the projects band;
 *  - /projects/: action nadlan_dir_projects_after_hero (inc/directory.php), right under the catalogue's header;
 *  - DUO, Rainbow: filter nadlan_ps_after_page (inc/project-stage.php), right after the page top; on a project page without
 *    the stage, at the end of the content;
 *  - /sde-dov/ and /sde-dov/prices/: the_content, before the page's second h2 (the opening answer stays untouched);
 *  - anywhere else: [nadlan_pricelist_form title="..." lead="..."].
 * Hebrew pages only (the words are Hebrew). Off switch: option nadlan_pricelist_form = '0'.
 */
if ( ! defined( 'ABSPATH' ) ) { exit; }

if ( ! function_exists( 'nadlan_plf_on' ) ) {
	function nadlan_plf_on() {
		if ( is_admin() || '0' === (string) get_option( 'nadlan_pricelist_form', '1' ) ) { return false; }
		if ( function_exists( 'nadlan_current_lang' ) && 'he' !== (string) nadlan_current_lang() ) { return false; }
		return true;
	}
}

if ( ! function_exists( 'nadlan_plf_project_slugs' ) ) {
	/** The project pages that carry the form. One line to extend it to more projects. */
	function nadlan_plf_project_slugs() {
		return (array) apply_filters( 'nadlan_plf_project_slugs', array( 'duo-tel-aviv', 'rainbow-tel-aviv' ) );
	}
}

if ( ! function_exists( 'nadlan_plf_page_paths' ) ) {
	/** The WordPress pages (by path) that carry the form, with the words for each. */
	function nadlan_plf_page_paths() {
		return (array) apply_filters( 'nadlan_plf_page_paths', array(
			'sde-dov'        => array(
				'ctx'   => 'sdedov',
				'title' => 'מחירון ותוכניות של הפרויקטים בשדה דב',
				'lead'  => 'השאירו שם וטלפון ונחזור אליכם עם המחירים והתוכניות העדכניים שבידינו לפרויקטים ברובע. בלי התחייבות.',
			),
			'sde-dov/prices' => array(
				'ctx'   => 'sdedov-prices',
				'title' => 'רוצים את המחירון העדכני של שדה דב?',
				'lead'  => 'השאירו שם וטלפון ונחזור אליכם עם מחירים ותוכניות לפי גודל הדירה והמתחם שמעניינים אתכם. בלי התחייבות.',
			),
		) );
	}
}

if ( ! function_exists( 'nadlan_plf_render' ) ) {
	/**
	 * The form. $a: ctx (a short key, part of the lead's source), title, lead, card_id, project_slug, project_title,
	 * class (extra classes on the section).
	 */
	function nadlan_plf_render( $a = array() ) {
		$a = wp_parse_args( (array) $a, array(
			'ctx'           => 'page',
			'title'         => 'קבלו מחירון ותוכניות',
			'lead'          => 'השאירו שם וטלפון ונחזור אליכם עם המחירים והתוכניות העדכניים שבידינו. בלי התחייבות.',
			'card_id'       => 0,
			'project_slug'  => '',
			'project_title' => '',
			'class'         => '',
		) );
		static $n = 0;
		$n++;
		$ctx  = sanitize_key( (string) $a['ctx'] );
		$id   = 'nlplf-' . $ctx . ( $n > 1 ? '-' . $n : '' );
		$priv = function_exists( 'get_privacy_policy_url' ) ? (string) get_privacy_policy_url() : '';
		if ( '' === $priv ) { $priv = home_url( '/privacy/' ); }
		$consent = 'בלחיצה על הכפתור אתם מבקשים שנחזור אליכם בטלפון או בוואטסאפ לגבי הבקשה הזו.';
		$card    = absint( $a['card_id'] );
		ob_start();
		?>
<section class="nlds nlplf<?php echo '' !== $a['class'] ? ' ' . esc_attr( $a['class'] ) : ''; ?>" id="<?php echo esc_attr( $id ); ?>" dir="rtl" lang="he" aria-labelledby="<?php echo esc_attr( $id ); ?>-h">
	<form class="nlds-form nlplf__form" novalidate
		data-plf-rest="<?php echo esc_url( rest_url( 'nadlan/v1/lead' ) ); ?>"
		data-plf-src="<?php echo esc_attr( 'pricelist-form-' . $ctx ); ?>"
		data-plf-card="<?php echo esc_attr( (string) $card ); ?>"
		data-plf-slug="<?php echo esc_attr( sanitize_title( (string) $a['project_slug'] ) ); ?>"
		data-plf-title="<?php echo esc_attr( (string) $a['project_title'] ); ?>"
		data-plf-consent="<?php echo esc_attr( $consent ); ?>">
		<h2 class="nlds-form__title" id="<?php echo esc_attr( $id ); ?>-h"><?php echo esc_html( (string) $a['title'] ); ?></h2>
		<p class="nlds-form__lead"><?php echo esc_html( (string) $a['lead'] ); ?></p>
		<div class="nlplf__row">
			<div class="nlds-field">
				<label for="<?php echo esc_attr( $id ); ?>-name">שם<span class="nlds-field__req" aria-hidden="true">*</span></label>
				<input id="<?php echo esc_attr( $id ); ?>-name" name="name" type="text" autocomplete="name" maxlength="80" required aria-describedby="<?php echo esc_attr( $id ); ?>-msg">
			</div>
			<div class="nlds-field">
				<label for="<?php echo esc_attr( $id ); ?>-phone">טלפון<span class="nlds-field__req" aria-hidden="true">*</span></label>
				<input id="<?php echo esc_attr( $id ); ?>-phone" name="phone" type="tel" inputmode="tel" autocomplete="tel" dir="ltr" maxlength="20" required placeholder="050-0000000" aria-describedby="<?php echo esc_attr( $id ); ?>-msg">
			</div>
		</div>
		<div class="nlplf__hp" aria-hidden="true"><label>חברה <input name="company" type="text" tabindex="-1" autocomplete="off"></label></div>
		<button type="submit" class="nlds-btn nlds-btn--primary nlplf__go">קבלו מחירון ותוכניות</button>
		<p class="nlplf__msg" id="<?php echo esc_attr( $id ); ?>-msg" role="status" aria-live="polite"></p>
		<p class="nlds-field__hint nlplf__note"><?php echo esc_html( $consent ); ?> <a href="<?php echo esc_url( $priv ); ?>">מדיניות פרטיות</a></p>
	</form>
</section>
		<?php
		$html = (string) ob_get_clean();
		return $html . nadlan_plf_assets_once();
	}
}

if ( ! function_exists( 'nadlan_plf_assets_once' ) ) {
	/** The few layout rules the design system's form does not carry, and the submit script; printed once per page. */
	function nadlan_plf_assets_once() {
		static $done = false;
		if ( $done ) { return ''; }
		$done = true;
		ob_start();
		?>
<style id="nadlan-plf-css">
:root body .nlds.nlplf{margin:32px auto!important;padding:0 16px!important;max-width:760px!important;box-sizing:border-box}
:root body .nlds.nlplf .nlds-form{margin:0 auto!important;box-sizing:border-box}
:root body .nlds.nlplf .nlds-form__title{margin-top:0!important}
.nlplf__row{display:grid;grid-template-columns:minmax(0,1fr);gap:0 14px}
@media(min-width:600px){.nlplf__row{grid-template-columns:minmax(0,1fr) minmax(0,1fr)}}
:root body .nlds.nlplf .nlds-field input{box-sizing:border-box}
:root body .nlds.nlplf .nlds-field input[type=tel]{text-align:right}
.nlplf__hp{position:absolute!important;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);clip-path:inset(50%);white-space:nowrap}
.nlplf__msg{margin:10px 0 0;font-size:15px;line-height:1.5;font-weight:600;color:#3b4753}
.nlplf__msg:empty{display:none}
.nlplf__msg.is-bad{color:#a3361f}
:root body .nlds.nlplf .nlplf__note{margin-top:10px!important}
:root body .nlds.nlplf .nlplf__note a{color:inherit;text-decoration:underline}
.nlplf__done{text-align:center;padding:8px 0}
.nlplf__done:focus{outline:none}
.nlplf__done b{display:block;font-size:20px;line-height:1.3;color:#14212b;margin:0 0 6px}
.nlplf__done span{font-size:15px;line-height:1.55;color:#3b4753}
:root body .nlds.nlplf .nlplf__go[disabled]{opacity:.65;cursor:default}
.nlhp-band.nlplf{margin-top:40px!important}
</style>
<script id="nadlan-plf-js">
(function(){
	function digits(s){return String(s||'').replace(/[^0-9+]/g,'');}
	function okPhone(s){var d=digits(s).replace(/^\+?972/,'0');return /^0\d{8,9}$/.test(d);}
	function boot(f){
		if(f.getAttribute('data-plf-on')){return;}
		f.setAttribute('data-plf-on','1');
		var nm=f.querySelector('[name=name]'),ph=f.querySelector('[name=phone]'),hp=f.querySelector('[name=company]'),go=f.querySelector('.nlplf__go'),msg=f.querySelector('.nlplf__msg'),label=go?go.textContent:'';
		function say(t,bad){msg.textContent=t;msg.classList.toggle('is-bad',!!bad);}
		[nm,ph].forEach(function(el){el.addEventListener('input',function(){el.removeAttribute('aria-invalid');});});
		f.addEventListener('submit',function(e){
			e.preventDefault();
			var name=(nm.value||'').trim(),phone=(ph.value||'').trim(),bad=null;
			nm.removeAttribute('aria-invalid');ph.removeAttribute('aria-invalid');
			if(name.length<2){nm.setAttribute('aria-invalid','true');bad=nm;say('נא לכתוב שם.',true);}
			else if(!okPhone(phone)){ph.setAttribute('aria-invalid','true');bad=ph;say('נא לכתוב מספר טלפון ישראלי, למשל 050-1234567.',true);}
			if(bad){bad.focus();return;}
			go.disabled=true;go.textContent='שולחים...';say('');
			var title=f.getAttribute('data-plf-title')||'',card=parseInt(f.getAttribute('data-plf-card')||'0',10)||0;
			var body={name:name,phone:digits(phone),goal:'מחירון ותוכניות',source:f.getAttribute('data-plf-src')||'pricelist-form',
				message:'בקשת מחירון ותוכניות'+(title?': '+title:'')+' | עמוד: '+location.href.split('#')[0],
				project_slug:f.getAttribute('data-plf-slug')||'',project_title:title,
				consent:1,consent_text:f.getAttribute('data-plf-consent')||'',company:hp?hp.value:''};
			if(card>0){body.card_id=card;}
			fetch(f.getAttribute('data-plf-rest'),{method:'POST',headers:{'Content-Type':'application/json'},credentials:'same-origin',body:JSON.stringify(body)})
			.then(function(r){return r.json().catch(function(){return {};}).then(function(j){return {s:r.status,j:j};});})
			.then(function(x){
				if(x.s>=200&&x.s<300&&x.j&&x.j.ok){
					f.innerHTML='<div class="nlplf__done" tabindex="-1"><b>קיבלנו, תודה.</b><span>נחזור אליכם בהקדם עם המחירון והתוכניות.</span></div>';
					var d=f.querySelector('.nlplf__done');if(d){d.focus();}
					if(window.nadlanGA){window.nadlanGA('generate_lead',{form:'pricelist',src:body.source});}
					return;
				}
				go.disabled=false;go.textContent=label;
				say(x.s===429?'נשלחו מכאן הרבה בקשות בשעה האחרונה. נסו שוב מאוחר יותר, או כתבו לנו בוואטסאפ.':'משהו השתבש בשליחה. נסו שוב בעוד רגע, או כתבו לנו בוואטסאפ.',true);
			})
			.catch(function(){go.disabled=false;go.textContent=label;say('אין חיבור כרגע. נסו שוב בעוד רגע, או כתבו לנו בוואטסאפ.',true);});
		});
	}
	function all(){[].forEach.call(document.querySelectorAll('form.nlplf__form'),boot);}
	if(document.readyState==='loading'){document.addEventListener('DOMContentLoaded',all);}else{all();}
})();
</script>
		<?php
		return (string) ob_get_clean();
	}
}

/* ---------- attach points ---------- */

/* the home page: right after the projects band (inc/home-v3.php) */
add_filter( 'nadlan_hp_after_projects', function ( $html ) {
	if ( ! nadlan_plf_on() ) { return $html; }
	return $html . nadlan_plf_render( array(
		'ctx'   => 'home',
		'class' => 'nlhp-band',
		'title' => 'קבלו מחירון ותוכניות לפרויקטים חדשים',
		'lead'  => 'השאירו שם וטלפון ונחזור אליכם עם המחירים והתוכניות העדכניים שבידינו לפרויקט או לאזור שמעניינים אתכם. בלי התחייבות.',
	) );
} );

/* /projects/: right under the catalogue's header (inc/directory.php) */
add_action( 'nadlan_dir_projects_after_hero', function () {
	if ( ! nadlan_plf_on() ) { return; }
	echo nadlan_plf_render( array( // phpcs:ignore -- escaped inside
		'ctx'   => 'projects',
		'title' => 'קבלו מחירון ותוכניות',
		'lead'  => 'מצאתם פרויקט שמעניין אתכם? השאירו שם וטלפון ונחזור אליכם עם המחירים והתוכניות העדכניים שבידינו. בלי התחייבות.',
	) );
} );

if ( ! function_exists( 'nadlan_plf_project_form' ) ) {
	/** The form for the project page being shown, or '' when this project does not carry it. */
	function nadlan_plf_project_form( $id, $slug ) {
		$id   = (int) $id;
		$slug = (string) $slug;
		if ( ! $id || ! in_array( $slug, nadlan_plf_project_slugs(), true ) ) { return ''; }
		$name = trim( wp_strip_all_tags( (string) get_the_title( $id ) ) );
		return nadlan_plf_render( array(
			'ctx'           => 'project',
			'title'         => '' !== $name ? 'מחירון ותוכניות של ' . $name : 'קבלו מחירון ותוכניות',
			'lead'          => 'השאירו שם וטלפון ונחזור אליכם עם המחירים והתוכניות העדכניים שבידינו לפרויקט. בלי התחייבות.',
			'card_id'       => $id,
			'project_slug'  => $slug,
			'project_title' => $name,
		) );
	}
}

/* DUO, Rainbow: right after the page top that inc/project-stage.php composes */
add_filter( 'nadlan_ps_after_page', function ( $html, $ps ) {
	if ( ! nadlan_plf_on() || ! is_array( $ps ) || 'he' !== (string) ( $ps['lang'] ?? 'he' ) ) { return $html; }
	return $html . nadlan_plf_project_form( (int) ( $ps['id'] ?? 0 ), (string) ( $ps['slug'] ?? '' ) );
}, 10, 2 );

/* the same projects without the stage (stage off, or a showroom page): at the end of the content */
add_filter( 'the_content', function ( $content ) {
	if ( ! is_singular( 'nadlan_project' ) || ! in_the_loop() || ! is_main_query() || ! nadlan_plf_on() ) { return $content; }
	if ( function_exists( 'nadlan_ps_current' ) && nadlan_ps_current() ) { return $content; } // the stage's hook places it
	$id = (int) get_the_ID();
	return $content . nadlan_plf_project_form( $id, (string) get_post_field( 'post_name', $id ) );
}, 40 );

/* /sde-dov/ and /sde-dov/prices/: before the second h2, so the opening answer stays as it is; no second h2, at the end */
add_filter( 'the_content', function ( $content ) {
	if ( ! is_page() || ! in_the_loop() || ! is_main_query() || ! nadlan_plf_on() ) { return $content; }
	$paths = nadlan_plf_page_paths();
	$path  = (string) get_page_uri( (int) get_the_ID() );
	if ( ! isset( $paths[ $path ] ) || false !== strpos( (string) $content, 'class="nlds nlplf' ) ) { return $content; }
	$form = nadlan_plf_render( $paths[ $path ] );
	if ( preg_match_all( '#<h2[\s>]#i', (string) $content, $m, PREG_OFFSET_CAPTURE ) && count( $m[0] ) >= 2 ) {
		$at = (int) $m[0][1][1];
		return substr( $content, 0, $at ) . $form . substr( $content, $at );
	}
	return $content . $form;
}, 22 );

/* any other page: [nadlan_pricelist_form title="..." lead="..."] */
add_shortcode( 'nadlan_pricelist_form', function ( $atts ) {
	if ( ! nadlan_plf_on() ) { return ''; }
	$atts = shortcode_atts( array( 'title' => '', 'lead' => '', 'ctx' => 'shortcode' ), (array) $atts, 'nadlan_pricelist_form' );
	$args = array( 'ctx' => sanitize_key( $atts['ctx'] ) );
	if ( '' !== $atts['title'] ) { $args['title'] = sanitize_text_field( $atts['title'] ); }
	if ( '' !== $atts['lead'] ) { $args['lead'] = sanitize_text_field( $atts['lead'] ); }
	if ( is_singular( 'nadlan_project' ) ) {
		$args['card_id']       = (int) get_the_ID();
		$args['project_slug']  = (string) get_post_field( 'post_name', get_the_ID() );
		$args['project_title'] = trim( wp_strip_all_tags( (string) get_the_title() ) );
	}
	return nadlan_plf_render( $args );
} );
