<?php
/* Review-vs-showroom mode per project (owner order 30.8.2026).
 * 'review' (default): editorial page only - de-stacked article, chips,
 *   notice, CTA. The interactive showroom layer (engine, payload, demo
 *   inventory, unit form, gallery, investor block) does not render.
 * 'showroom': the full engine experience - reserved for the conceptual
 *   flagship (Aurelia) and projects with a signed developer partnership.
 * Flip per project: post meta `project_mode` = review|showroom (in REST). */
if ( ! defined( 'ABSPATH' ) ) { exit; }

if ( ! function_exists( 'nadlan_project_mode' ) ) {
	function nadlan_project_mode( $post_id ) {
		$mode = (string) get_post_meta( (int) $post_id, 'project_mode', true );
		if ( 'showroom' !== $mode ) { $mode = 'review'; }
		return apply_filters( 'nadlan_project_mode', $mode, (int) $post_id );
	}
}

add_action( 'init', function () {
	register_post_meta( 'nadlan_project', 'project_mode', array(
		'type' => 'string', 'single' => true, 'show_in_rest' => true, 'default' => '',
		'sanitize_callback' => function ( $v ) { return in_array( $v, array( 'review', 'showroom' ), true ) ? $v : ''; },
		'auth_callback' => function () { return current_user_can( 'edit_posts' ); },
	) );
}, 11 );
