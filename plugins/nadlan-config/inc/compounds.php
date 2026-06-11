<?php
/**
 * nadlan-config - compounds (מתחמים): group projects under a development
 * compound (e.g., Sde Dov) with one archive page + filter facets by
 * developer / contractor / initiator. Always on (taxonomy registration is
 * harmless); front-end facets respect existing directory behavior.
 */

if ( ! defined( 'ABSPATH' ) ) { exit; }

if ( ! defined( 'NADLAN_COMPOUND_SEED_VERSION' ) ) {
	define( 'NADLAN_COMPOUND_SEED_VERSION', 1 );
}

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

if ( ! function_exists( 'nadlan_compound_seed_has_marker' ) ) {
	function nadlan_compound_seed_has_marker( $value ) {
		$value = (string) $value;
		if ( $value === '' ) { return false; }
		return stripos( $value, 'rainbow' ) !== false || strpos( $value, 'קשת' ) !== false || strpos( $value, 'ריינבו' ) !== false;
	}
}

if ( ! function_exists( 'nadlan_compound_seed_project_matches' ) ) {
	function nadlan_compound_seed_project_matches( $post_id ) {
		$post_id = absint( $post_id );
		$post    = $post_id ? get_post( $post_id ) : null;
		if ( ! $post || $post->post_type !== 'nadlan_project' ) { return false; }
		if ( nadlan_compound_seed_has_marker( $post->post_title ) || nadlan_compound_seed_has_marker( $post->post_name ) ) {
			return true;
		}

		$meta = get_post_meta( $post_id );
		foreach ( $meta as $values ) {
			foreach ( (array) $values as $value ) {
				if ( is_array( $value ) || is_object( $value ) ) { continue; }
				if ( nadlan_compound_seed_has_marker( $value ) ) {
					return true;
				}
			}
		}
		return false;
	}
}

if ( ! function_exists( 'nadlan_compound_seed_find_rainbow_project' ) ) {
	function nadlan_compound_seed_find_rainbow_project() {
		$candidates = array();
		foreach ( array( 'Rainbow', 'קשת', 'ריינבו' ) as $term ) {
			$ids = get_posts( array(
				'post_type'      => 'nadlan_project',
				'post_status'    => 'any',
				's'              => $term,
				'fields'         => 'ids',
				'posts_per_page' => 20,
				'no_found_rows'  => true,
			) );
			$candidates = array_merge( $candidates, $ids );
		}

		if ( empty( $candidates ) ) {
			$candidates = get_posts( array(
				'post_type'      => 'nadlan_project',
				'post_status'    => 'any',
				'fields'         => 'ids',
				'posts_per_page' => 2000,
				'no_found_rows'  => true,
			) );
		}

		foreach ( array_unique( array_map( 'absint', $candidates ) ) as $post_id ) {
			if ( nadlan_compound_seed_project_matches( $post_id ) ) {
				return (int) $post_id;
			}
		}

		$fallback = get_post( 4464 );
		if ( $fallback && $fallback->post_type === 'nadlan_project' ) {
			return 4464;
		}
		return 0;
	}
}

if ( ! function_exists( 'nadlan_compound_seed' ) ) {
	function nadlan_compound_seed() {
		if ( get_option( 'nadlan_feature_compound_map', '0' ) !== '1' ) { return; }
		if ( (int) get_option( 'nadlan_compound_seeded', 0 ) >= NADLAN_COMPOUND_SEED_VERSION ) { return; }
		if ( ! taxonomy_exists( 'nadlan_compound' ) || ! post_type_exists( 'nadlan_project' ) ) { return; }

		$term    = get_term_by( 'slug', 'sde-dov', 'nadlan_compound' );
		$term_id = ( $term && ! is_wp_error( $term ) ) ? (int) $term->term_id : 0;
		if ( ! $term_id ) {
			$created = wp_insert_term( 'רובע שדה דב', 'nadlan_compound', array( 'slug' => 'sde-dov' ) );
			if ( is_wp_error( $created ) || empty( $created['term_id'] ) ) { return; }
			$term_id = (int) $created['term_id'];
		}

		$project_id = nadlan_compound_seed_find_rainbow_project();
		if ( ! $project_id ) { return; }

		$assigned = wp_set_object_terms( $project_id, array( $term_id ), 'nadlan_compound', true );
		if ( is_wp_error( $assigned ) ) { return; }

		update_option( 'nadlan_compound_seeded', NADLAN_COMPOUND_SEED_VERSION, false );
	}
}
add_action( 'admin_init', 'nadlan_compound_seed' );

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
