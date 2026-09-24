<?php
/**
 * Layout fixes that belong to no single module (24.9.2026).
 *
 * RTL full-width content on phones. The theme's nadlan-premium-revenue.css gives .wp-block-post-content
 * width:100% and max-width:100% under 700px. On single listing, professional and glossary pages that block is
 * also .alignfull inside a padded group, so WordPress pulls it out with -24px margins on both sides. Width
 * 100% plus both margins over-constrains the box, and in RTL the browser drops the left margin: the text sat
 * 72px from the left edge and 24px from the right (Meital's listing article measured 294px wide on a 390px
 * phone; the owner: "the article is too narrow"). Letting the width be automatic restores 24px on both sides.
 */
if ( ! defined( 'ABSPATH' ) ) { exit; }

add_action( 'wp_head', function () {
	echo "\n<style id=\"nadlan-layout-fixes\">@media (max-width:700px){.has-global-padding>.wp-block-post-content.alignfull{width:auto!important;max-width:none!important}}</style>\n";
}, 99 );
