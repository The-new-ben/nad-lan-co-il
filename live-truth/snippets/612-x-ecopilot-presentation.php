
/* x-ecopilot-presentation v1.0 (30.8.2026, owner meeting): the two EcoCity pilot
 * pages hide blocks that read as broken or contradict the verified facts -
 * default-walk media (old-building photos), demo-unit inventory, empty price
 * and surroundings bands, and the derived 8/8 hero stats. Everything else
 * (plate hero, lead, 3D theater, live map, FAQ, form, article) stays.
 * Rollback: deactivate this snippet. */
if ( ! function_exists( 'nadlan_ecopilot_presentation_css' ) ) {
	function nadlan_ecopilot_presentation_css() {
		if ( ! is_singular( 'nadlan_project' ) ) { return; }
		$pid = (int) get_queried_object_id();
		if ( ! in_array( $pid, array( 6693, 6694 ), true ) ) { return; }
		echo '<style id="nl-ecopilot-presentation">'
			. 'body.single-nadlan_project #media,'
			. 'body.single-nadlan_project #inventory,'
			. 'body.single-nadlan_project #price,'
			. 'body.single-nadlan_project #nlpjx-price,'
			. 'body.single-nadlan_project #nlpjx-world,'
			. 'body.single-nadlan_project .nlw-ch,'
			. 'body.single-nadlan_project .nl-hero__facts,'
			. 'body.single-nadlan_project .nl-hero__cta [data-id="inventory"]'
			. '{display:none!important}'
			. '</style>';
	}
	add_action( 'wp_head', 'nadlan_ecopilot_presentation_css', 130 );
}
