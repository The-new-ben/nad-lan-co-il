<?php
/**
 * nadlan-config - compounds (מתחמים): group projects under a development
 * compound (e.g., Sde Dov) with one archive page + filter facets by
 * developer / contractor / initiator. Always on (taxonomy registration is
 * harmless); front-end facets respect existing directory behavior.
 */

if ( ! defined( 'ABSPATH' ) ) { exit; }

add_action( 'init', function () {
	register_taxonomy( 'nadlan_compound', array( 'nadlan_project' ), array(
		'labels' => array( 'name' => 'מתחמים', 'singular_name' => 'מתחם', 'add_new_item' => 'הוספת מתחם' ),
		'public' => true, 'hierarchical' => true, 'show_in_rest' => true,
		'rewrite' => array( 'slug' => 'compound', 'with_front' => false ),
	) );
	// Filterable company fields on projects (developer already exists as developer_name).
	foreach ( array( 'developer_name' => 'יזם', 'contractor_name' => 'קבלן מבצע', 'architect_name' => 'אדריכל' ) as $key => $label ) {
		register_post_meta( 'nadlan_project', $key, array(
			'show_in_rest' => true, 'single' => true, 'type' => 'string',
			'sanitize_callback' => 'sanitize_text_field',
			'auth_callback' => function () { return current_user_can( 'edit_posts' ); },
		) );
	}
} );

// Compound archive: simple filter bar (developer/contractor) on top of the term archive.
add_action( 'pre_get_posts', function ( $q ) {
	if ( is_admin() || ! $q->is_main_query() || ! is_tax( 'nadlan_compound' ) ) { return; }
	$meta = array();
	foreach ( array( 'developer' => 'developer_name', 'contractor' => 'contractor_name' ) as $param => $key ) {
		$v = isset( $_GET[ $param ] ) ? sanitize_text_field( wp_unslash( $_GET[ $param ] ) ) : '';
		if ( $v !== '' ) { $meta[] = array( 'key' => $key, 'value' => $v, 'compare' => 'LIKE' ); }
	}
	if ( $meta ) { $q->set( 'meta_query', $meta ); }
	$q->set( 'nadlan_paid_placement_boost', 1 );
	$q->set( 'orderby', 'none' );
} );

if ( ! function_exists( 'nadlan_compound_filter_bar' ) ) {
	function nadlan_compound_filter_bar( $term_id ) {
		$devs = array(); $cons = array();
		$q = new WP_Query( array(
			'post_type' => 'nadlan_project', 'post_status' => 'publish', 'fields' => 'ids',
			'posts_per_page' => 200, 'no_found_rows' => true,
			'tax_query' => array( array( 'taxonomy' => 'nadlan_compound', 'terms' => (int) $term_id ) ),
		) );
		foreach ( $q->posts as $pid ) {
			$d = trim( (string) get_post_meta( $pid, 'developer_name', true ) );
			$c = trim( (string) get_post_meta( $pid, 'contractor_name', true ) );
			if ( $d !== '' ) { $devs[ $d ] = true; }
			if ( $c !== '' ) { $cons[ $c ] = true; }
		}
		wp_reset_postdata();
		if ( ! $devs && ! $cons ) { return ''; }
		$cur_d = sanitize_text_field( wp_unslash( $_GET['developer'] ?? '' ) );
		$cur_c = sanitize_text_field( wp_unslash( $_GET['contractor'] ?? '' ) );
		$h = '<form class="nlcmp-filter" method="get" dir="rtl" style="display:flex;gap:10px;flex-wrap:wrap;margin:16px 0">';
		if ( $devs ) {
			$h .= '<select name="developer" onchange="this.form.submit()"><option value="">כל היזמים</option>';
			foreach ( array_keys( $devs ) as $d ) { $h .= '<option value="' . esc_attr( $d ) . '" ' . selected( $cur_d, $d, false ) . '>' . esc_html( $d ) . '</option>'; }
			$h .= '</select>';
		}
		if ( $cons ) {
			$h .= '<select name="contractor" onchange="this.form.submit()"><option value="">כל הקבלנים</option>';
			foreach ( array_keys( $cons ) as $c ) { $h .= '<option value="' . esc_attr( $c ) . '" ' . selected( $cur_c, $c, false ) . '>' . esc_html( $c ) . '</option>'; }
			$h .= '</select>';
		}
		return $h . '</form>';
	}
}
add_shortcode( 'nadlan_compound_filter', function () {
	$term = get_queried_object();
	return ( $term && ! empty( $term->term_id ) ) ? nadlan_compound_filter_bar( $term->term_id ) : '';
} );

add_filter( 'nadlan_config_healthcheck', function ( $out ) {
	$terms = get_terms( array( 'taxonomy' => 'nadlan_compound', 'hide_empty' => false, 'fields' => 'count' ) );
	$out['compounds'] = array( 'taxonomy' => true, 'count' => is_wp_error( $terms ) ? 0 : (int) $terms );
	return $out;
} );
