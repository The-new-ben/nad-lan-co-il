<?php
/**
 * nadlan-config - Directory importer (v1.5.0)
 *
 * Seeds the free directory cards from AUTHORITATIVE PUBLIC data (no API key):
 *   - Contractors  ← רשם הקבלנים open dataset on data.gov.il CKAN (~14k rows)
 *                    resource_id 4eb61bd6-18cf-4e7c-9f9c-e166dfa0a2d8
 *   - Urban-renewal projects ← מתחמי התחדשות עירונית (~938 compounds)
 *                    resource_id f65a0daf-f737-49c5-9424-d378d52104f5
 *
 * Idempotent: each card stores source_id (MISPAR_KABLAN / MisparMitham); re-running
 * updates rather than duplicates. Cards are created as data_quality=stub and get
 * noindexed until enriched (see inc/schema.php) so thin stubs never hit the index
 * or cannibalize keyword pages. A separate REST endpoint lets Cowork push the
 * ChatGPT-enriched original prose that flips a card to data_quality=enriched.
 *
 * Triggers: WP-CLI (`wp nadlan import contractors`), an admin batch button, and a
 * REST endpoint for enriched-content push. Runs in batches to avoid timeouts.
 */

if ( ! defined( 'ABSPATH' ) ) { exit; }

const NADLAN_CKAN_BASE       = 'https://data.gov.il/api/3/action/datastore_search';
const NADLAN_RES_CONTRACTORS = '4eb61bd6-18cf-4e7c-9f9c-e166dfa0a2d8';
const NADLAN_RES_URBAN       = 'f65a0daf-f737-49c5-9424-d378d52104f5';

/* ---- low-level CKAN fetch ---- */
if ( ! function_exists( 'nadlan_ckan_fetch' ) ) {
	function nadlan_ckan_fetch( $resource_id, $limit = 500, $offset = 0 ) {
		$url = add_query_arg( array(
			'resource_id' => $resource_id,
			'limit'       => (int) $limit,
			'offset'      => (int) $offset,
		), NADLAN_CKAN_BASE );
		$res = wp_remote_get( $url, array( 'timeout' => 25 ) );
		if ( is_wp_error( $res ) ) { return new WP_Error( 'ckan_http', $res->get_error_message() ); }
		$body = json_decode( wp_remote_retrieve_body( $res ), true );
		if ( empty( $body['success'] ) ) { return new WP_Error( 'ckan_fail', 'CKAN returned failure' ); }
		return array(
			'records' => $body['result']['records'] ?? array(),
			'total'   => (int) ( $body['result']['total'] ?? 0 ),
		);
	}
}

/* ---- upsert a card by source_id (create or update, never duplicate) ---- */
if ( ! function_exists( 'nadlan_card_upsert' ) ) {
	function nadlan_card_upsert( $post_type, $source, $source_id, $title, $meta, $body = '' ) {
		$existing = get_posts( array(
			'post_type' => $post_type, 'posts_per_page' => 1, 'fields' => 'ids',
			'post_status' => 'any',
			'meta_query' => array(
				array( 'key' => 'source', 'value' => $source ),
				array( 'key' => 'source_id', 'value' => (string) $source_id ),
			),
		) );
		// Normalize whitespace from the CKAN source (gov.il fields are space-padded).
		$nz = function ( $s ) { return is_string( $s ) ? trim( preg_replace( '/\s+/u', ' ', $s ) ) : $s; };
		$title = $nz( $title );
		foreach ( $meta as $mk => $mv ) { $meta[ $mk ] = $nz( $mv ); }
		$args = array(
			'post_type'   => $post_type,
			'post_status' => 'publish',
			'post_title'  => $title,
		);
		if ( $body !== '' ) { $args['post_content'] = $body; }
		if ( $existing ) {
			$args['ID'] = (int) $existing[0];
			// Do NOT overwrite owner-edited content once claimed/enriched.
			if ( get_post_meta( $args['ID'], 'claim_status', true ) === 'verified'
				|| get_post_meta( $args['ID'], 'data_quality', true ) === 'enriched' ) {
				unset( $args['post_content'], $args['post_title'] );
			}
			$id = wp_update_post( $args, true );
		} else {
			$id = wp_insert_post( $args, true );
		}
		if ( is_wp_error( $id ) ) { return $id; }
		update_post_meta( $id, 'source', $source );
		update_post_meta( $id, 'source_id', (string) $source_id );
		if ( get_post_meta( $id, 'data_quality', true ) === '' ) {
			update_post_meta( $id, 'data_quality', 'stub' );
		}
		foreach ( $meta as $k => $v ) {
			if ( $v !== '' && $v !== null ) { update_post_meta( $id, $k, $v ); }
		}
		return $id;
	}
}

/* ---- contractors importer (one batch) ---- */
if ( ! function_exists( 'nadlan_import_contractors_batch' ) ) {
	function nadlan_import_contractors_batch( $limit = 500, $offset = 0 ) {
		$data = nadlan_ckan_fetch( NADLAN_RES_CONTRACTORS, $limit, $offset );
		if ( is_wp_error( $data ) ) { return $data; }
		// Group rows by contractor number (a contractor holds multiple branch rows).
		$by_kablan = array();
		foreach ( $data['records'] as $r ) {
			$k = (string) ( $r['MISPAR_KABLAN'] ?? '' );
			if ( $k === '' ) { continue; }
			$by_kablan[ $k ][] = $r;
		}
		$count = 0;
		foreach ( $by_kablan as $kablan_no => $rows ) {
			$first = $rows[0];
			$branches = array();
			$max_sivug = 0;
			foreach ( $rows as $r ) {
				$anaf  = trim( (string) ( $r['TEUR_ANAF'] ?? '' ) );
				$sivug = (int) ( $r['SIVUG'] ?? 0 );
				if ( $anaf !== '' ) { $branches[] = $anaf . ( $sivug ? " (סיווג $sivug)" : '' ); }
				$max_sivug = max( $max_sivug, $sivug );
			}
			$city  = trim( (string) ( $first['SHEM_YISHUV'] ?? '' ) );
			$name  = trim( (string) ( $first['SHEM_YESHUT'] ?? '' ) ) ?: ( 'קבלן ' . $kablan_no );
			$addr  = trim( ( (string) ( $first['SHEM_REHOV'] ?? '' ) ) . ' ' . ( (string) ( $first['MISPAR_BAIT'] ?? '' ) ) );
			$meta = array(
				'profession'      => 'kablan',
				'registry_number' => $kablan_no,
				'classification'  => implode( ' · ', array_slice( array_unique( $branches ), 0, 12 ) ),
				'company_name'    => $name,
				'city'            => $city,
				'address'         => $addr,
				'phone'           => trim( (string) ( $first['MISPAR_TEL'] ?? '' ) ),
				'email'           => sanitize_email( (string) ( $first['EMAIL'] ?? '' ) ),
				'project_count'   => 0,
				'source'          => 'pinkas_hakablanim',
				'source_url'      => 'https://www.gov.il/apps/moch/rasham/home',
				'max_sivug'       => $max_sivug,
			);
			$res = nadlan_card_upsert( 'nadlan_professional', 'pinkas_hakablanim', $kablan_no, $name, $meta );
			if ( ! is_wp_error( $res ) ) { $count++; }
		}
		return array( 'imported' => $count, 'total' => $data['total'], 'next_offset' => $offset + $limit );
	}
}

/* ---- urban-renewal projects importer (one batch) ---- */
if ( ! function_exists( 'nadlan_import_urban_batch' ) ) {
	function nadlan_import_urban_batch( $limit = 500, $offset = 0 ) {
		$data = nadlan_ckan_fetch( NADLAN_RES_URBAN, $limit, $offset );
		if ( is_wp_error( $data ) ) { return $data; }
		$count = 0;
		foreach ( $data['records'] as $r ) {
			$mid  = (string) ( $r['MisparMitham'] ?? '' );
			if ( $mid === '' ) { continue; }
			$name = trim( (string) ( $r['ShemMitcham'] ?? '' ) ) ?: ( 'מתחם התחדשות ' . $mid );
			$meta = array(
				'project_type'    => ( strpos( (string) ( $r['Maslul'] ?? '' ), 'פינוי' ) !== false ) ? 'pinui_binui' : 'tama38',
				'project_status'  => (string) ( $r['Status'] ?? '' ),
				'city'            => trim( (string) ( $r['Yeshuv'] ?? '' ) ),
				'num_units'       => (int) ( $r['YachadMutza'] ?? 0 ),
				'completion_year' => (int) ( $r['ShnatMatanTokef'] ?? 0 ),
				'source'          => 'urban_renewal',
				'source_url'      => (string) ( $r['KishurLatar'] ?? 'https://www.gov.il/he/pages/mappat-hitchadshut-ironit' ),
				'plan_number'     => (string) ( $r['MisparTochnit'] ?? '' ),
				'units_existing'  => (int) ( $r['YachadKayam'] ?? 0 ),
				'units_added'     => (int) ( $r['YachadTosafti'] ?? 0 ),
			);
			$res = nadlan_card_upsert( 'nadlan_project', 'urban_renewal', $mid, $name, $meta );
			if ( ! is_wp_error( $res ) ) { $count++; }
		}
		return array( 'imported' => $count, 'total' => $data['total'], 'next_offset' => $offset + $limit );
	}
}

/* ---- admin batch runner (button-driven, cursor stored in options) ---- */
if ( ! function_exists( 'nadlan_import_admin_run' ) ) {
	function nadlan_import_admin_run() {
		if ( ! current_user_can( 'manage_options' ) ) { wp_die( 'forbidden' ); }
		$which = isset( $_GET['which'] ) ? sanitize_key( $_GET['which'] ) : 'contractors';
		check_admin_referer( 'nadlan_import_' . $which );
		$opt    = 'nadlan_import_offset_' . $which;
		$offset = (int) get_option( $opt, 0 );
		$result = ( $which === 'urban' )
			? nadlan_import_urban_batch( 500, $offset )
			: nadlan_import_contractors_batch( 500, $offset );
		if ( is_wp_error( $result ) ) {
			wp_safe_redirect( admin_url( 'index.php?nadlan_import=error&msg=' . rawurlencode( $result->get_error_message() ) ) );
			exit;
		}
		$next = ( $result['next_offset'] >= $result['total'] ) ? 0 : $result['next_offset'];
		update_option( $opt, $next, false );
		wp_safe_redirect( admin_url( 'index.php?nadlan_import=ok&imported=' . $result['imported'] . '&next=' . $next . '&total=' . $result['total'] ) );
		exit;
	}
}
add_action( 'admin_post_nadlan_import_run', 'nadlan_import_admin_run' );

/* Dashboard widget with the import buttons + progress */
if ( ! function_exists( 'nadlan_import_dashboard' ) ) {
	function nadlan_import_dashboard() {
		wp_add_dashboard_widget( 'nadlan_import_widget', 'NadLan Directory Import', function () {
			foreach ( array( 'contractors' => 'קבלנים (רשם הקבלנים)', 'urban' => 'התחדשות עירונית' ) as $which => $label ) {
				$offset = (int) get_option( 'nadlan_import_offset_' . $which, 0 );
				$url = wp_nonce_url( admin_url( 'admin-post.php?action=nadlan_import_run&which=' . $which ), 'nadlan_import_' . $which );
				echo '<p><strong>' . esc_html( $label ) . '</strong> - next offset: ' . (int) $offset
					. ' &nbsp;<a class="button" href="' . esc_url( $url ) . '">Import next 500</a></p>';
			}
			echo '<p style="color:#666">Each click imports/updates 500 records (idempotent). Repeat until offset returns to 0. Stubs are noindexed until enriched.</p>';
		} );
	}
}
add_action( 'wp_dashboard_setup', 'nadlan_import_dashboard' );

/* ---- REST: enriched-content push (admin) - Cowork/ChatGPT pipeline ----
 * POST /nadlan/v1/import-enrich  { post_id, content, meta:{}, data_quality:"enriched" }
 */
if ( ! function_exists( 'nadlan_import_register_rest' ) ) {
	function nadlan_import_register_rest() {
		register_rest_route( 'nadlan/v1', '/import-enrich', array(
			'methods'  => 'POST',
			'permission_callback' => function () { return current_user_can( 'edit_posts' ); },
			'callback' => 'nadlan_import_enrich_handler',
		) );
	}
}
add_action( 'rest_api_init', 'nadlan_import_register_rest' );

/* ---- REST: HEADLESS import runner (v1.23.0) ----
 * Lets the catalog be populated via Application Password / Basic Auth - no browser,
 * no dashboard button. Runs N batches of 500 server-side per call (capped so we stay
 * inside PHP max_execution_time), advances the stored cursor, returns progress so the
 * caller can loop until done. Idempotent (re-imports update existing cards by registry
 * key, same as the batch functions).
 *
 *   POST /nadlan/v1/import-run  { "which": "contractors"|"urban", "batches": 3, "reset": false }
 *   -> { ok, which, imported_this_call, offset, total, done }
 */
if ( ! function_exists( 'nadlan_import_run_handler' ) ) {
	function nadlan_import_run_handler( $req ) {
		$p     = $req->get_json_params(); if ( ! is_array( $p ) ) { $p = $req->get_params(); }
		$which = ( ( $p['which'] ?? 'contractors' ) === 'urban' ) ? 'urban' : 'contractors';
		$batches = max( 1, min( 8, (int) ( $p['batches'] ?? 3 ) ) ); // hard cap 8 × 500 = 4000/call
		$opt   = 'nadlan_import_offset_' . $which;
		if ( ! empty( $p['reset'] ) ) { update_option( $opt, 0, false ); }
		$offset = (int) get_option( $opt, 0 );
		$imported = 0; $total = 0;
		for ( $i = 0; $i < $batches; $i++ ) {
			$r = ( $which === 'urban' )
				? nadlan_import_urban_batch( 500, $offset )
				: nadlan_import_contractors_batch( 500, $offset );
			if ( is_wp_error( $r ) ) {
				return new WP_REST_Response( array( 'ok' => false, 'error' => $r->get_error_message(), 'offset' => $offset ), 502 );
			}
			$imported += (int) $r['imported'];
			$total     = (int) $r['total'];
			$offset    = (int) $r['next_offset'];
			if ( $offset >= $total ) { break; } // reached the end
		}
		$done = ( $offset >= $total );
		update_option( $opt, $done ? 0 : $offset, false );
		return new WP_REST_Response( array(
			'ok' => true, 'which' => $which,
			'imported_this_call' => $imported,
			'offset' => $done ? $total : $offset,
			'total' => $total, 'done' => $done,
		), 200 );
	}
}
add_action( 'rest_api_init', function () {
	register_rest_route( 'nadlan/v1', '/import-run', array(
		'methods'             => 'POST',
		'permission_callback' => function () { return current_user_can( 'manage_options' ); },
		'callback'            => 'nadlan_import_run_handler',
	) );
} );

if ( ! function_exists( 'nadlan_import_enrich_handler' ) ) {
	function nadlan_import_enrich_handler( $req ) {
		$p  = $req->get_json_params(); if ( ! is_array( $p ) ) { $p = $req->get_params(); }
		$id = (int) ( $p['post_id'] ?? 0 );
		$allowed = apply_filters( 'nadlan_import_enrich_types', array( 'nadlan_project', 'nadlan_professional', 'nadlan_property' ) );
		if ( ! $id || ! in_array( get_post_type( $id ), $allowed, true ) ) {
			return new WP_REST_Response( array( 'ok' => false, 'error' => 'bad_card' ), 400 );
		}
		if ( ! empty( $p['content'] ) ) {
			wp_update_post( array( 'ID' => $id, 'post_content' => wp_kses_post( $p['content'] ) ) );
		}
		if ( ! empty( $p['meta'] ) && is_array( $p['meta'] ) ) {
			foreach ( $p['meta'] as $k => $v ) {
				update_post_meta( $id, sanitize_key( $k ), sanitize_text_field( (string) $v ) );
			}
		}
		update_post_meta( $id, 'data_quality', 'enriched' );
		if ( function_exists( 'nadlan_config_indexnow_ping' ) ) {
			nadlan_config_indexnow_ping( get_permalink( $id ) ); // now worth indexing
		}
		return new WP_REST_Response( array( 'ok' => true, 'id' => $id ), 200 );
	}
}

/* ---- v1.23.0: SELF-SEEDING background importer ----
 * So the catalog populates itself after the plugin updates - no button, no endpoint
 * call, no owner action. On each load we check a tiny flag; if the directory is still
 * sparse, we schedule a wp-cron single event that imports ONE batch (500) of each
 * dataset and reschedules itself until the cursor wraps, then marks itself done.
 * Driven by normal site traffic via wp-cron, so it never blocks a page render.
 */
const NADLAN_AUTOSEED_TARGET = 1500; // stop auto-seeding once we have this many professionals

if ( ! function_exists( 'nadlan_autoseed_maybe_schedule' ) ) {
	function nadlan_autoseed_maybe_schedule() {
		if ( get_option( 'nadlan_autoseed_done' ) === '1' ) { return; }
		if ( wp_next_scheduled( 'nadlan_autoseed_tick' ) ) { return; }
		// Already have enough? mark done.
		$have = (int) wp_count_posts( 'nadlan_professional' )->publish;
		if ( $have >= NADLAN_AUTOSEED_TARGET ) { update_option( 'nadlan_autoseed_done', '1', false ); return; }
		wp_schedule_single_event( time() + 60, 'nadlan_autoseed_tick' );
	}
}
add_action( 'init', 'nadlan_autoseed_maybe_schedule', 5 );

if ( ! function_exists( 'nadlan_autoseed_tick' ) ) {
	function nadlan_autoseed_tick() {
		// One batch of each dataset per tick (keeps each cron run well under the time limit).
		$any_more = false;
		foreach ( array( 'contractors', 'urban' ) as $which ) {
			$opt    = 'nadlan_import_offset_' . $which;
			$offset = (int) get_option( $opt, 0 );
			$r = ( $which === 'urban' )
				? nadlan_import_urban_batch( 500, $offset )
				: nadlan_import_contractors_batch( 500, $offset );
			if ( is_wp_error( $r ) ) { continue; }
			$next = ( $r['next_offset'] >= $r['total'] ) ? 0 : $r['next_offset'];
			update_option( $opt, $next, false );
			if ( $next !== 0 ) { $any_more = true; }
		}
		$have = (int) wp_count_posts( 'nadlan_professional' )->publish;
		if ( $any_more && $have < NADLAN_AUTOSEED_TARGET ) {
			wp_schedule_single_event( time() + 120, 'nadlan_autoseed_tick' ); // keep going, spaced out
		} else {
			update_option( 'nadlan_autoseed_done', '1', false );
		}
	}
}
add_action( 'nadlan_autoseed_tick', 'nadlan_autoseed_tick' );

/* ---- WP-CLI: `wp nadlan import contractors|urban [--all]` ---- */
if ( defined( 'WP_CLI' ) && WP_CLI ) {
	WP_CLI::add_command( 'nadlan import', function ( $args ) {
		$which = $args[0] ?? 'contractors';
		$offset = 0; $grand = 0;
		do {
			$r = ( $which === 'urban' )
				? nadlan_import_urban_batch( 500, $offset )
				: nadlan_import_contractors_batch( 500, $offset );
			if ( is_wp_error( $r ) ) { WP_CLI::error( $r->get_error_message() ); }
			$grand += $r['imported'];
			WP_CLI::log( "offset $offset → imported {$r['imported']} (total {$r['total']})" );
			$offset = $r['next_offset'];
		} while ( $offset < $r['total'] );
		WP_CLI::success( "Done: $grand cards upserted ($which)." );
	} );
}
