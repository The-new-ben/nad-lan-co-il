<?php
/**
 * nadlan-config — Site-wide premium UI overlay (v1.42.0)
 *
 * One module that lifts the catalog/profile/micro-UI from "default WP directory" to
 * an editorial real-estate experience without rewriting directory.php / cards-render.php.
 *
 * Ships:
 *   1. An inline SVG sprite (profession marks + small UI icons) injected once in
 *      wp_footer, so existing card markup can do <svg><use href="#profession-..."/></svg>.
 *   2. A high-priority CSS layer that:
 *        - retunes palette + typography to the ink/charcoal/champagne system
 *        - replaces the bright pill avatars with calm monogram-style marks
 *        - upgrades buttons, chips, sponsored slots, FAB, profile shell
 *        - fixes mobile data-tables (article tables forcing 400-677px layout at 390px)
 *        - enforces 44px tap targets for header/footer/glossary/nav
 *        - re-anchors the floating CTA to the visual viewport (safe-area)
 *
 * Boundary: this module ONLY adds CSS + sprite + a small profile-shell decorator. It
 * does NOT touch routes, REST, lead pipes, billing, schema, or any business logic.
 */
if ( ! defined( 'ABSPATH' ) ) { exit; }

if ( ! function_exists( 'nadlan_premium_enabled' ) ) {
	function nadlan_premium_enabled() {
		if ( defined( 'NADLAN_DISABLE_PREMIUM_UI' ) && NADLAN_DISABLE_PREMIUM_UI ) { return false; }
		if ( is_admin() ) { return false; }
		if ( defined( 'REST_REQUEST' ) && REST_REQUEST ) { return false; }
		return true;
	}
}

/* ---------- 1. SVG sprite: profession marks + tiny UI glyphs --------------- */
if ( ! function_exists( 'nadlan_premium_sprite' ) ) {
	function nadlan_premium_sprite() {
		// Inlined once per page. IDs match directory.php's $pm['icon'] values
		// (profession-contractor, profession-architect, ...). Lines only, currentColor.
		return <<<'SVG'
<svg id="nl-premium-sprite" width="0" height="0" style="position:absolute;visibility:hidden;overflow:hidden" aria-hidden="true" focusable="false"><defs>
<symbol id="profession-contractor" viewBox="0 0 48 48"><path fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" d="M8 38h32M12 38V22l12-8 12 8v16M18 38V28h12v10M14 22l10-6 10 6"/></symbol>
<symbol id="profession-architect" viewBox="0 0 48 48"><path fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" d="M10 36h28M15 36V14l9-5 9 5v22M19 36V20h10v16M19 25h10M13 18l11-6 11 6"/></symbol>
<symbol id="profession-lawyer" viewBox="0 0 48 48"><path fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" d="M24 8v32M12 14h24M16 14l-4 12h8l-4-12M32 14l-4 12h8l-4-12M14 40h20"/></symbol>
<symbol id="profession-appraiser" viewBox="0 0 48 48"><path fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" d="M10 38h28M14 38V22M22 38V14M30 38V26M38 38V18M8 12l8-4 8 5 8-3 8 4"/></symbol>
<symbol id="profession-developer" viewBox="0 0 48 48"><path fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" d="M8 40h32M14 40V12h8v28M22 40V20h8v20M30 40V26h8v14M14 16h8M14 22h8M22 24h8M22 30h8M30 30h8M30 34h8"/></symbol>
<symbol id="profession-mortgage" viewBox="0 0 48 48"><path fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" d="M8 38h32M10 22h28L24 10zM14 22v16M20 22v16M28 22v16M34 22v16"/></symbol>
<symbol id="profession-inspector" viewBox="0 0 48 48"><path fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" d="M30 30l8 8M21 33a12 12 0 1 1 0-24 12 12 0 0 1 0 24zM15 21h12M21 15v12"/></symbol>
<symbol id="profession-broker" viewBox="0 0 48 48"><path fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" d="M24 8a8 8 0 0 1 8 8c0 6-8 14-8 14s-8-8-8-14a8 8 0 0 1 8-8zM24 16v0M16 36h16M14 40h20"/><circle cx="24" cy="16" r="2.5" fill="none" stroke="currentColor" stroke-width="1.6"/></symbol>
<symbol id="category-project" viewBox="0 0 48 48"><path fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" d="M8 40h32M14 40V18l10-6 10 6v22M20 40V28h8v12M18 22h12M18 28h2M28 28h2"/></symbol>
<symbol id="category-property" viewBox="0 0 48 48"><path fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" d="M8 40h32M12 40V22l12-10 12 10v18M18 40V28h12v12M22 22h4"/></symbol>
</defs></svg>
SVG;
	}
}

/* ---------- 2. Premium CSS overlay ---------------------------------------- */
if ( ! function_exists( 'nadlan_premium_css' ) ) {
	function nadlan_premium_css() {
		$asset = function ( $file ) {
			return plugins_url( 'assets/concept/' . $file, dirname( __DIR__ ) . '/nadlan-config.php' );
		};
		$css = <<<'CSS'
<style id="nl-premium-ui">
/* ===== Premium tokens (site-wide) ===== */
:root{
	--nl-ink:#11110F; --nl-charcoal:#2B2924; --nl-warm:#6D665C;
	--nl-hairline:#DDD6C8; --nl-surface:#FAF8F3; --nl-card:#FFFFFF; --nl-band:#F3EFE7;
	--nl-gold:#9C7A3C; --nl-champagne:#D7C39A; --nl-olive:#334236; --nl-sea:#183C3C; --nl-clay:#9F6F54;
	--nl-radius:8px; --nl-radius-lg:12px;
	--nl-shadow-sm:0 1px 2px rgba(17,17,15,.04),0 1px 1px rgba(17,17,15,.04);
	--nl-shadow-md:0 8px 24px rgba(17,17,15,.07),0 2px 6px rgba(17,17,15,.04);
	--nl-shadow-lg:0 20px 50px rgba(17,17,15,.12);
	--nl-focus:0 0 0 2px #fff,0 0 0 4px var(--nl-gold);
}

/* ===== Catalog card system upgrade ===== */
.nldir-results .nldc{
	border-radius:var(--nl-radius-lg)!important;
	border:1px solid var(--nl-hairline)!important;
	padding:22px 22px 20px!important;
	box-shadow:var(--nl-shadow-sm);
	transition:transform .25s cubic-bezier(.2,.8,.2,1),box-shadow .25s,border-color .25s;
}
.nldir-results .nldc::before{height:3px!important;opacity:.85!important;background:var(--pc,var(--nl-gold))!important}
.nldir-results .nldc:hover{
	transform:translateY(-3px);
	box-shadow:var(--nl-shadow-md);
	border-color:var(--pc,var(--nl-gold));
}
.nldir-results .nldc.is-featured{
	border-color:var(--pc,var(--nl-gold));
	box-shadow:0 1px 2px rgba(17,17,15,.04),0 14px 36px color-mix(in srgb,var(--pc,#9C7A3C) 15%,transparent);
}
.nldir-results .nldc.is-featured::before{height:4px!important;background:linear-gradient(90deg,var(--pc,var(--nl-gold)),var(--nl-champagne))!important;opacity:1!important}

/* ----- AVATAR: profession SVG mark replaces emoji ----- */
.nldc-av{
	width:56px!important;height:56px!important;
	border-radius:14px!important;
	background:var(--ps,var(--nl-band))!important;
	box-shadow:inset 0 0 0 1px color-mix(in srgb,var(--pc,#9C7A3C) 20%,transparent)!important;
	color:var(--pc,var(--nl-ink));
	font-size:0!important; /* kills any leftover text node */
	display:grid;place-items:center;
}
.nldc-av .nl-mark{width:32px;height:32px;color:var(--pc,var(--nl-ink));display:block}

/* ----- TYPOGRAPHY ----- */
.nldc-name{
	font-family:var(--font-serif,"Frank Ruhl Libre",serif)!important;
	font-weight:600!important;font-size:18px!important;
	letter-spacing:-.01em;color:var(--nl-ink)!important;line-height:1.2!important;
}

/* ----- PILL: calm, not loud ----- */
.nldc-pill{
	background:transparent!important;
	color:var(--nl-warm)!important;
	font-size:11.5px!important;font-weight:600!important;letter-spacing:.04em;
	text-transform:none!important;
	padding:0!important;border-radius:0!important;
	border-block-end:1px solid var(--pc,var(--nl-hairline))!important;
	padding-bottom:2px!important;display:inline-block!important;margin-top:2px;
}

/* ----- VERIFIED chip ----- */
.nldc-vf{
	color:var(--nl-olive)!important;
	font-size:11.5px!important;font-weight:700!important;
	background:#F1F4EE;padding:2px 8px;border-radius:20px;
	margin-inline-start:6px;display:inline-block;
}

/* ----- RATING / EMPTY review ----- */
.nldc-rate{font-size:13px;color:var(--nl-warm)}
.nldc-rate.nldc-norate{
	color:var(--nl-warm)!important;font-size:12.5px!important;
	background:transparent!important;padding:0!important;
}
.nldc-stars{color:var(--nl-gold)!important;letter-spacing:1.5px}

/* ----- META row ----- */
.nldc-meta{display:flex;flex-direction:column;gap:6px;font-size:13.5px;color:var(--nl-charcoal)}
.nldc-city,.nldc-cls{display:inline-flex!important;align-items:center;gap:6px;color:var(--nl-charcoal)!important}
.nl-ico{width:14px;height:14px;flex:none;color:var(--nl-warm);display:inline-block;vertical-align:middle}

/* ----- FOOT ----- */
.nldc-foot{display:flex;justify-content:space-between;align-items:center;border-top:1px solid var(--nl-hairline)!important;padding-top:12px!important;margin-top:auto}
.nldc-reg{display:inline-flex;align-items:center;gap:6px;font-size:11.5px;color:var(--nl-warm)!important}
.nldc-reg .nl-ico{color:var(--nl-olive)}
.nldc-go{font-weight:700!important;color:var(--pc,var(--nl-gold))!important;font-size:13px;letter-spacing:.02em}

/* ----- SPONSORED label (real cards) ----- */
.nldc-sponsor{
	background:linear-gradient(135deg,var(--nl-gold),var(--nl-champagne))!important;
	color:#fff!important;font-size:10px!important;font-weight:700!important;
	letter-spacing:.12em!important;padding:4px 11px!important;border-radius:30px!important;
}

/* ----- SPONSORED SLOT (empty/upsell card) — proper premium product ----- */
.nldc-sponsored-spot{
	background:linear-gradient(180deg,#FBF9F5,#F3EFE7)!important;
	border:1px solid var(--nl-champagne)!important;
	text-align:center;display:flex!important;flex-direction:column;
	min-height:240px;
	position:relative;
	overflow:hidden;
}
.nldc-sponsored-spot::after{
	content:"";position:absolute;inset:0;
	background:radial-gradient(120% 80% at 50% -20%,rgba(215,195,154,.35),transparent 60%);
	pointer-events:none;
}
.nldc-sponsored-spot::before{background:linear-gradient(90deg,var(--nl-gold),var(--nl-champagne))!important;opacity:1!important;height:4px!important}
.nldc-sponsor-slot{position:relative!important;inset:auto!important;align-self:center;margin:6px auto 10px!important}
.nldc-sponsored-body{display:flex;flex-direction:column;align-items:center;gap:8px;padding:8px 0;position:relative}
.nldc-sponsored-mark{width:48px;height:48px;color:var(--nl-gold);display:block;margin-bottom:4px}
.nldc-sponsored-h{font-size:17px!important;margin:4px 0 2px!important;color:var(--nl-ink)!important}
.nldc-sponsored-p{font-size:13px!important;color:var(--nl-warm);margin:0;line-height:1.55;max-width:240px}
.nldc-sponsored-foot{font-size:11.5px;color:var(--nl-warm)}
.nldc-sponsored-foot a{color:var(--nl-gold);font-weight:600;text-decoration:none}

/* ===== HERO + filters: less "cyber dashboard", more editorial ===== */
.nldir-hero{
	background:
		radial-gradient(80% 100% at 15% 0%,rgba(51,66,54,.55),transparent 55%),
		radial-gradient(80% 100% at 85% 10%,rgba(24,60,60,.5),transparent 55%),
		linear-gradient(135deg,#17170F,#1F1E18 60%,#17170F)!important;
}
.nldir-hero h1{font-family:var(--font-serif,"Frank Ruhl Libre",serif)!important;font-weight:600!important;letter-spacing:-.02em}
.nldir-search{box-shadow:var(--nl-shadow-lg)!important;border-radius:14px!important;padding:6px!important}
.nldir-search button{
	background:linear-gradient(135deg,var(--nl-gold),#B89254)!important;
	font-weight:700;letter-spacing:.02em;
	min-height:44px;
}
.nldir-pill{
	min-height:40px;
	background:rgba(255,255,255,.08)!important;
	border:1px solid rgba(255,255,255,.18)!important;
	font-size:13px!important;font-weight:600!important;letter-spacing:.02em;
}
.nldir-pill:hover{background:rgba(255,255,255,.16)!important}
.nldir-pill.is-on{background:#fff!important;color:var(--nl-ink)!important;border-color:#fff!important}

/* ===== Filter sidebar: quiet, premium ===== */
.nldir-fgroup h4{color:var(--nl-gold)!important;font-size:11px!important;letter-spacing:.16em!important}
.nldir-check{
	min-height:44px;border-radius:10px!important;font-size:14px!important;
	border-color:var(--nl-hairline)!important;
}
.nldir-check:hover{background:var(--nl-band)!important;border-color:var(--nl-gold)!important;color:var(--nl-ink)}
.nldir-cityb{min-height:40px;border-radius:8px!important;font-size:13.5px!important}
.nldir-cityb.is-on,.nldir-cityb:hover{background:var(--nl-band)!important;color:var(--nl-ink)!important}

/* ===== Results bar / chips ===== */
.nldir-count strong{color:var(--nl-gold)!important;font-size:18px!important;font-weight:700}
.nldir-chip{
	background:#fff!important;border:1px solid var(--nl-hairline)!important;
	border-radius:20px!important;font-size:12.5px!important;
	color:var(--nl-charcoal);
}
.nldir-chip button{
	color:var(--nl-warm)!important;font-size:18px!important;line-height:1!important;
	width:24px;height:24px;display:inline-grid;place-items:center;border-radius:50%!important;
	transition:background .15s,color .15s;
}
.nldir-chip button:hover{background:var(--nl-band)!important;color:var(--nl-ink)!important}
.nldir-sortw select{
	min-height:40px;border:1px solid var(--nl-hairline)!important;
	border-radius:8px!important;background:#fff!important;
	padding:0 14px!important;font-weight:600;
}

/* ===== Single-profile shell upgrades ===== */
.nlpf-banner{
	background:
		radial-gradient(80% 100% at 20% 0%,rgba(215,195,154,.35),transparent 55%),
		linear-gradient(135deg,#F3EFE7,#FAF8F3 60%,#F3EFE7)!important;
	border-bottom:1px solid var(--nl-hairline)!important;
}
.nlpf-av{
	background:var(--nl-band)!important;
	border:4px solid #fff!important;
	box-shadow:var(--nl-shadow-md);
	color:var(--pc,var(--nl-ink));
	font-size:0!important; /* kills the leftover sprite-id text node */
	display:grid;place-items:center;
}
.nlpf-av .nl-mark{width:46px;height:46px;color:var(--pc,var(--nl-ink));display:block}
.nlpf-sub span{display:inline-flex;align-items:center;gap:6px}
.nlpf-reg .nl-ico{color:var(--nl-olive)}
.nlpf-call .nl-ico{width:16px;height:16px}
.nlpf-pill{
	background:transparent!important;color:var(--nl-warm)!important;
	border-bottom:1px solid var(--nl-gold)!important;
	border-radius:0!important;padding:0 0 2px!important;
	font-size:12px!important;letter-spacing:.04em;
}
.nlpf-reg{
	background:#F1F4EE!important;color:var(--nl-olive)!important;
	border-radius:20px!important;padding:4px 12px!important;font-size:11.5px!important;font-weight:700;
}
.nlpremier{
	background:linear-gradient(135deg,var(--nl-gold),var(--nl-champagne))!important;
	color:#fff!important;font-weight:700!important;letter-spacing:.08em;
	padding:5px 14px!important;border-radius:30px!important;font-size:11px!important;
}

/* ===== Profile CTAs (call, quote, claim) — premium button grammar ===== */
.nlpf-call,.nlpf-quote,.nlcp-btn,.nlfab-btn{
	min-height:48px!important;
	border-radius:12px!important;
	font-weight:700!important;letter-spacing:.02em;
	transition:transform .15s,box-shadow .2s,filter .2s;
}
.nlpf-call,.nlcp-btn{
	background:linear-gradient(135deg,var(--nl-ink),var(--nl-charcoal))!important;
	color:#fff!important;border:0!important;
	box-shadow:var(--nl-shadow-md);
}
.nlpf-call:hover,.nlcp-btn:hover{transform:translateY(-1px);filter:brightness(1.1)}
.nlpf-quote{
	background:#fff!important;color:var(--nl-ink)!important;
	border:1px solid var(--nl-ink)!important;
}
.nlpf-quote:hover{background:var(--nl-band)!important}

/* Empty review on profile: hide the loud "be first to rate" copy */
.nlpf-norate{
	background:transparent!important;color:var(--nl-warm)!important;
	font-size:13px!important;padding:0!important;border:0!important;
}

/* ===== Empty / claim states ===== */
.nlcp{
	background:linear-gradient(180deg,#FAF8F3,#F3EFE7)!important;
	border:1px solid var(--nl-hairline)!important;
	border-radius:var(--nl-radius-lg)!important;
}
.nlcp-icon{filter:grayscale(1) brightness(.6) opacity(.6)}
.nlcp-body h3{font-family:var(--font-serif,"Frank Ruhl Libre",serif)!important;color:var(--nl-ink)!important}

/* ===== FLOATING WHATSAPP CTA — re-anchor to visual viewport ===== */
#nlcta{
	bottom:max(20px,env(safe-area-inset-bottom,20px))!important;
	inset-inline-end:max(20px,env(safe-area-inset-right,20px))!important;
	z-index:99989;
}
.nlcta-wa{box-shadow:0 14px 36px rgba(37,211,102,.45)!important}
.nlcta-wa:hover{box-shadow:0 18px 44px rgba(37,211,102,.55)!important}

/* ===== Profile-extras social chips: ink/calm, not bright brand colors ===== */
.nlpe-soc{
	background:var(--nl-ink)!important;color:#fff!important;
	min-height:44px;border-radius:26px!important;
	font-weight:600!important;letter-spacing:.02em;
	transition:transform .15s,filter .2s;
}
.nlpe-soc:hover{transform:translateY(-2px);filter:brightness(1.15)}
.nlpe-soc svg{width:16px;height:16px;display:block;color:#fff}

/* ===== Site-wide buttons (Woo, WP blocks, generic) ===== */
.woocommerce a.button,
.woocommerce button.button,
.woocommerce input.button,
.wc-block-components-button,
.wp-block-button__link,
.wp-element-button{
	min-height:48px!important;
	border-radius:12px!important;
	padding:12px 22px!important;
	font-weight:700!important;letter-spacing:.02em!important;
	font-family:var(--font-sans,Heebo,system-ui,sans-serif)!important;
	background:linear-gradient(135deg,var(--nl-ink),var(--nl-charcoal))!important;
	color:#fff!important;
	border:0!important;
	box-shadow:var(--nl-shadow-sm);
	transition:transform .15s,box-shadow .2s,filter .2s!important;
}
.woocommerce a.button:hover,
.woocommerce button.button:hover,
.wc-block-components-button:hover,
.wp-block-button__link:hover,
.wp-element-button:hover{
	transform:translateY(-1px);
	box-shadow:var(--nl-shadow-md);
	filter:brightness(1.1);
}
.woocommerce a.button.alt,
.woocommerce button.button.alt,
.wc-block-components-button.contained{
	background:linear-gradient(135deg,var(--nl-gold),#B89254)!important;
}

/* ===== Focus visibility (a11y) ===== */
.nldc:focus-visible,.nldir-pill:focus-visible,.nldir-cityb:focus-visible,
.nlpf-call:focus-visible,.nlpf-quote:focus-visible,.nlcp-btn:focus-visible,
.woocommerce a.button:focus-visible,.wp-element-button:focus-visible,
.nlfab-btn:focus-visible,.nlcta-wa:focus-visible{
	outline:none!important;box-shadow:var(--nl-focus)!important;
}

/* ===== MOBILE (390px-first) =====
   Article tables are the dominant cause of horizontal overflow on /mortgage-*,
   /selling-*, /new-projects/*, /real-estate-lawyer/* article pages. Convert to
   stacked label/value cards when columns make the table wider than the viewport. */
@media (max-width:600px){
	/* hard stop on horizontal scroll */
	html,body{overflow-x:hidden!important}

	/* Article tables → stacked rows (label cells become row headings) */
	.entry-content table,
	article table,
	.wp-block-table table,
	.wp-block-table figure table{
		display:block!important;width:100%!important;border-collapse:collapse;
	}
	.entry-content table thead,
	article table thead,
	.wp-block-table thead{display:none!important}
	.entry-content table tr,
	article table tr,
	.wp-block-table tr{
		display:block!important;
		border:1px solid var(--nl-hairline)!important;
		border-radius:10px!important;
		margin:0 0 12px!important;
		padding:6px 12px!important;
		background:#fff!important;
		box-shadow:var(--nl-shadow-sm);
	}
	.entry-content table td,
	.entry-content table th,
	article table td,
	article table th,
	.wp-block-table td,
	.wp-block-table th{
		display:block!important;width:100%!important;
		padding:8px 0!important;border:0!important;
		border-bottom:1px dashed var(--nl-hairline)!important;
		font-size:15px!important;line-height:1.5!important;
		text-align:start!important;
	}
	.entry-content table tr td:last-child,
	article table tr td:last-child,
	.wp-block-table tr td:last-child{border-bottom:0!important}
	/* first cell becomes a heading-like label */
	.entry-content table tr td:first-child,
	article table tr td:first-child,
	.wp-block-table tr td:first-child{
		font-weight:700!important;color:var(--nl-ink)!important;font-size:13.5px!important;
		text-transform:none;letter-spacing:.02em;
	}

	/* Tap targets: hamburger, footer/nav links, glossary inline links */
	button.wp-block-navigation__responsive-container-open,
	button.wp-block-navigation__responsive-container-close{
		min-width:44px!important;min-height:44px!important;
	}
	.wp-block-navigation a,
	.wp-block-navigation__container a,
	footer a,
	.site-footer a{
		min-height:44px;display:inline-flex;align-items:center;
		padding:6px 8px!important;
	}
	.nadlan-gloss-link{
		display:inline-block;line-height:44px!important;padding:0 2px;
	}

	/* Floating CTA bar (.nlfab) — re-anchor to visual viewport, no overflow */
	.nlfab{
		position:fixed!important;
		left:0!important;right:0!important;bottom:0!important;
		max-width:100vw!important;
		padding:10px max(14px,env(safe-area-inset-right,14px)) max(10px,env(safe-area-inset-bottom,10px)) max(14px,env(safe-area-inset-left,14px))!important;
		background:rgba(255,255,255,.96)!important;backdrop-filter:blur(10px);
		border-top:1px solid var(--nl-hairline)!important;
		box-shadow:0 -8px 24px rgba(17,17,15,.08)!important;
		z-index:99988;
	}
	.nlfab-btn{
		min-height:44px!important;flex:1!important;
		font-size:14.5px!important;
	}

	/* Catalog cards stack cleanly at 390 */
	.nldir-results{grid-template-columns:1fr!important;gap:12px!important}
	.nldir-results .nldc{padding:18px!important}
	.nldc-name{font-size:17px!important}

	/* Hero filter pills size */
	.nldir-pill{font-size:12.5px!important;min-height:40px}

	/* Body min text size */
	.entry-content p,.entry-content li{font-size:16px!important;line-height:1.7!important}
}

/* ===== Concept-art card media (project/property only — never professionals) ===== */
.nldir-results .nldc.has-media{
	padding:0!important;
	border-radius:18px!important;
	overflow:hidden;
	background:linear-gradient(180deg,#fff,#FBF8F1)!important;
	box-shadow:var(--nl-shadow-md);
}
.nldir-results .nldc.has-media::before{display:none!important}
.nldir-results .nldc.has-media .nldc-top,
.nldir-results .nldc.has-media .nldc-meta,
.nldir-results .nldc.has-media .nldc-foot{padding-inline:20px}
.nldir-results .nldc.has-media .nldc-top{padding-top:16px}
.nldir-results .nldc.has-media .nldc-foot{padding-bottom:16px}
.nldc-media{
	position:relative;
	aspect-ratio:16/10;
	overflow:hidden;
	background:#0B1717;
	border-bottom:1px solid var(--nl-hairline);
}
.nldc-media img{
	width:100%;height:100%;
	object-fit:cover;
	display:block;
	transition:transform .35s cubic-bezier(.2,.8,.2,1);
}
.nldir-results .nldc.has-media:hover .nldc-media img{transform:scale(1.035)}
.nldc-media.has-concept-art{background:#0B1717}
.nldc-media.has-concept-art img{object-fit:contain;padding:6px}
.nldc-media.has-real-photo::after{
	content:"";position:absolute;inset:0;
	background:linear-gradient(180deg,transparent 55%,rgba(11,23,23,.55));
	pointer-events:none;
}
.nldc-media-label{
	position:absolute;
	inset-block-start:12px;inset-inline-start:12px;
	font-family:var(--font-sans,Heebo,sans-serif);
	font-size:11px;font-weight:700;letter-spacing:.08em;
	padding:5px 11px;
	color:#0B1717;
	background:linear-gradient(135deg,#F4DFAA,#D7C39A);
	border-radius:30px;
	box-shadow:0 6px 18px rgba(0,0,0,.25);
}

/* ===== Single profile hero — original concept skyline (replaces flat gradient) ===== */
.nlpf-banner{
	background:
		linear-gradient(180deg,rgba(7,19,19,.55),rgba(7,19,19,.85)),
		url("CONCEPT_SKYLINE_URL") center/cover no-repeat,
		linear-gradient(135deg,#0B1F1F,#113332)!important;
	min-height:140px!important;
}

/* ===== Hero (directory + homepage) — subtle concept skyline backdrop ===== */
.nldir-hero{position:relative}
.nldir-hero::before{
	content:"";
	position:absolute;inset:0;
	background:url("CONCEPT_HERO_URL") center/cover no-repeat;
	opacity:.22;
	mix-blend-mode:screen;
	pointer-events:none;
}

/* ===== Reduced motion ===== */
@media (prefers-reduced-motion:reduce){
	.nldir-results .nldc,.nldir-search button,.nlpf-call,.nlpf-quote,
	.nlcp-btn,.nlfab-btn,.woocommerce a.button,.wp-element-button{
		transition:none!important;
	}
	.nldir-results .nldc:hover{transform:none!important}
	.nldir-results .nldc.has-media:hover .nldc-media img{transform:none!important}
}
</style>
CSS;
		return strtr( $css, array(
			'CONCEPT_SKYLINE_URL' => esc_url( $asset( 'skyline-telaviv-line.svg' ) ),
			'CONCEPT_HERO_URL'    => esc_url( $asset( 'hero-coast-concept.svg' ) ),
		) );
	}
}

/* ---------- 3. Inject sprite + CSS in <head>/footer ----------------------- */
add_action( 'wp_head', function () {
	if ( ! nadlan_premium_enabled() ) { return; }
	echo nadlan_premium_css(); // styles, no user data
}, 999 );

add_action( 'wp_footer', function () {
	if ( ! nadlan_premium_enabled() ) { return; }
	echo nadlan_premium_sprite(); // static SVG defs, no user data
}, 1 );
