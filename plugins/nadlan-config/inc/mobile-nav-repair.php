<?php
/**
 * Mobile navigation repair for the platform header.
 *
 * THE BUG (found live 2026-08-03, owner report "the hamburger is strange,
 * something is on, no way to open it"): the child theme ships a
 * .nlpc-nav-toggle button (three empty spans) with NO css and NO js - it
 * renders as a 15x5px unstyled speck that does nothing. The parent theme's
 * rescue injector (nlpc-header-nav-inject.js) would have built a working
 * hamburger, but it guards with "if (.nlpc-nav-toggle exists) return" - it
 * checks EXISTENCE where it means FUNCTIONING, sees the broken speck, and
 * bails. Meanwhile nlpc-header-parent-override.css hides .nlpc-primary-nav
 * below 760px with !important. Net result on phones: no menu at all.
 *
 * THE FIX, from the plugin because themes have no deploy pipeline: make the
 * child theme's own toggle work. The click toggles the SAME
 * is-nav-open-injected class the parent override sheet already styles, so
 * the open panel reuses the design that is already live; the css below
 * duplicates the essential open-state rules anyway, so the repair stands
 * even on a page where that sheet is missing. If the injected toggle ever
 * appears (theme fixed properly), this module steps aside.
 *
 * @package nadlan-config
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

add_action( 'wp_enqueue_scripts', function () {
	$css = '
.nlpc-nav-toggle{display:none;width:42px;height:42px;border:1px solid var(--nlp-border,#D9D2C4);
 border-radius:2px;background:#FFF;align-items:center;justify-content:center;flex-direction:column;
 gap:4px;cursor:pointer;padding:0}
.nlpc-nav-toggle span{display:block;width:20px;height:2px;background:var(--nlp-ink,#1B1A17);
 border-radius:1px;transition:transform .2s,opacity .2s}
.nlpc-site-header.is-nav-open-injected .nlpc-nav-toggle span:nth-child(1){transform:translateY(6px) rotate(45deg)}
.nlpc-site-header.is-nav-open-injected .nlpc-nav-toggle span:nth-child(2){opacity:0}
.nlpc-site-header.is-nav-open-injected .nlpc-nav-toggle span:nth-child(3){transform:translateY(-6px) rotate(-45deg)}
@media(max-width:760px){
 .nlpc-nav-toggle{display:inline-flex}
 /* The owner wants the menu text VISIBLE on mobile, not only behind a tap.
    platform.css already designed the closed state as a swipeable pill row
    (order:3, overflow-x:auto, hidden scrollbar); the parent override sheet
    killed it with display:none !important in favour of a hamburger that was
    never injected. Both affordances now live together: the row shows the
    top destinations at a glance, the hamburger opens the full vertical
    list. This rule must outrank the override sheet, hence the doubled
    class and the 99 enqueue priority that prints us after the theme. */
 .nlpc-site-header .nlpc-primary-nav.nlpc-primary-nav{display:flex!important}
 .nlpc-site-header.is-nav-open-injected .nlpc-primary-nav{grid-column:1/-1;
  flex-direction:column;align-items:stretch;overflow-x:visible;gap:2px;padding:10px 0 4px;
  border-top:1px solid var(--nlp-border,#D9D2C4)}
 .nlpc-site-header.is-nav-open-injected .nlpc-primary-nav a{min-height:46px;display:flex;
  align-items:center;font-size:15px;border-bottom:1px solid var(--nlp-border,#D9D2C4)}
}
@media(min-width:761px){.nlpc-nav-toggle{display:none!important}}';
	wp_register_style( 'nadlan-mnav', false, array(), NADLAN_CONFIG_VERSION );
	wp_enqueue_style( 'nadlan-mnav' );
	wp_add_inline_style( 'nadlan-mnav', $css );
}, 99 );

add_action( 'wp_footer', function () {
	?>
<script>
(function () {
	'use strict';
	var header = document.querySelector('.nlpc-site-header');
	if (!header) { return; }
	/* the parent theme's injected toggle carries its own working js */
	if (header.querySelector('.nlpc-nav-toggle-injected')) { return; }
	var toggle = header.querySelector('.nlpc-nav-toggle');
	var nav = header.querySelector('.nlpc-primary-nav');
	if (!toggle || !nav) { return; }
	function isOpen() { return header.classList.contains('is-nav-open-injected'); }
	function setOpen(open) {
		header.classList.toggle('is-nav-open-injected', open);
		toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
	}
	toggle.addEventListener('click', function (e) { e.preventDefault(); setOpen(!isOpen()); });
	document.addEventListener('keydown', function (e) {
		if ('Escape' === e.key && isOpen()) { setOpen(false); }
	});
	document.addEventListener('click', function (e) {
		if (isOpen() && !header.contains(e.target)) { setOpen(false); }
	});
	nav.addEventListener('click', function (e) {
		if (e.target.closest && e.target.closest('a')) { setOpen(false); }
	});
	window.addEventListener('resize', function () {
		if (window.innerWidth > 760 && isOpen()) { setOpen(false); }
	});
})();
</script>
	<?php
}, 20 );
