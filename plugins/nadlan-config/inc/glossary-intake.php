<?php
/**
 * nadlan-config - Encyclopedia intake + drip scheduler (owner mega-project
 * 2026-07-06: the professional real-estate encyclopedia, "better than the UK
 * one").
 *
 * Extends the existing glossary engine (inc/glossary.php, CPT nadlan_term)
 * with what the full-world encyclopedia needs:
 *
 *  1) ENTITY FIELDS: name_en (the attached English term - doubles the search
 *     surface and serves professional olim) and entity_type (term / material /
 *     tool / method / role / regulation / standard / person / organization /
 *     publication / formula / software).
 *  2) INTAKE ENDPOINT: POST /nadlan/v1/glossary-intake (admin app-password)
 *     accepts a JSON array of entries. Entries WITH content are scheduled as
 *     FUTURE posts on a drip (default 12/day spread across working hours -
 *     steady human cadence, never a bulk dump); entries without content are
 *     created as drafts awaiting their article. Duplicate titles are skipped.
 *  3) EN-TERM CHIP: term pages render the English term under the title.
 *
 * The drip is the anti-"scaled content abuse" discipline: quality-gated
 * batches at a believable cadence, with the existing thin-content guard and
 * autolinker doing their jobs on each published term.
 */

if ( ! defined( 'ABSPATH' ) ) { exit; }

const NADLAN_ENC_TYPES = array( 'term', 'material', 'tool', 'method', 'role', 'regulation', 'standard', 'person', 'organization', 'publication', 'formula', 'software' );

add_action( 'init', function () {
	foreach ( array( 'name_en', 'entity_type', 'enc_domain', 'enc_sources', 'enc_related' ) as $key ) {
		register_post_meta( 'nadlan_term', $key, array(
			'show_in_rest' => true, 'single' => true, 'type' => 'string',
			'sanitize_callback' => 'sanitize_text_field',
			'auth_callback' => function () { return current_user_can( 'edit_posts' ); },
		) );
	}
}, 11 );

/* ---------------- intake + drip ---------------- */
add_action( 'rest_api_init', function () {
	register_rest_route( 'nadlan/v1', '/glossary-intake', array(
		'methods' => 'POST',
		'permission_callback' => function () { return current_user_can( 'update_plugins' ); },
		'callback' => function ( WP_REST_Request $req ) {
			$p = $req->get_json_params();
			$entries = isset( $p['entries'] ) && is_array( $p['entries'] ) ? $p['entries'] : ( is_array( $p ) ? $p : array() );
			$per_day = max( 1, min( 50, (int) ( $p['per_day'] ?? 12 ) ) );
			$created = 0; $scheduled = 0; $drafted = 0; $skipped = 0; $first = ''; $last = '';
			// resume the drip after the latest already-scheduled term
			$latest = get_posts( array( 'post_type' => 'nadlan_term', 'post_status' => 'future', 'posts_per_page' => 1, 'orderby' => 'date', 'order' => 'DESC', 'fields' => 'ids' ) );
			$cursor = $latest ? strtotime( get_post_field( 'post_date', $latest[0] ) ) : current_time( 'timestamp' );
			$slot = 0;
			foreach ( $entries as $e ) {
				$title = sanitize_text_field( (string) ( $e['name_he'] ?? '' ) );
				if ( $title === '' ) { $skipped++; continue; }
				$content = (string) ( $e['content_html'] ?? '' );
				// STAGE-2 PATH: an existing DRAFT with thin content + an incoming
				// article = fill the draft and put it on the drip. A published or
				// already-scheduled term is never touched (no silent overwrites).
				$found = get_page_by_title( $title, OBJECT, 'nadlan_term' );
				$fill_id = 0;
				if ( $found ) {
					$existing_words = count( preg_split( '/\s+/', trim( wp_strip_all_tags( (string) $found->post_content ) ) ) );
					if ( 'draft' === $found->post_status && $existing_words < 250 && trim( wp_strip_all_tags( $content ) ) !== '' ) {
						$fill_id = (int) $found->ID;
					} else { $skipped++; continue; }
				}
				// Wikipedia-depth gate (owner 2026-07-07): only a real article enters
				// the publishing drip; anything shorter stays a private draft.
				$content_words = count( preg_split( '/\s+/', trim( wp_strip_all_tags( $content ) ) ) );
				$has_content = $content_words >= 250;
				$args = array(
					'post_type'    => 'nadlan_term',
					'post_title'   => $title,
					'post_content' => wp_kses_post( $content !== '' ? $content : (string) ( $e['def'] ?? '' ) ),
					'post_excerpt' => sanitize_text_field( (string) ( $e['def'] ?? '' ) ),
					'post_status'  => 'draft',
				);
				if ( $has_content ) {
					// next drip slot: per_day posts spread 09:00-19:00, skip to next day when full
					$slot++;
					$day_offset  = (int) floor( ( $slot - 1 ) / $per_day );
					$in_day      = ( $slot - 1 ) % $per_day;
					$base        = strtotime( date( 'Y-m-d 09:00:00', $cursor ) ) + $day_offset * DAY_IN_SECONDS;
					$stamp       = $base + (int) round( $in_day * ( 10 * HOUR_IN_SECONDS / max( 1, $per_day ) ) );
					if ( $stamp <= current_time( 'timestamp' ) ) { $stamp = current_time( 'timestamp' ) + $slot * 600; }
					$args['post_status'] = 'future';
					$args['post_date']   = date( 'Y-m-d H:i:s', $stamp );
					if ( $first === '' ) { $first = $args['post_date']; }
					$last = $args['post_date'];
				}
				if ( $fill_id ) { $args['ID'] = $fill_id; }
				$pid = $fill_id ? wp_update_post( $args ) : wp_insert_post( $args );
				if ( is_wp_error( $pid ) || ! $pid ) { $skipped++; continue; }
				$pid = $fill_id ? $fill_id : $pid;
				$created++;
				if ( $has_content ) { $scheduled++; } else { $drafted++; }
				foreach ( array( 'name_en', 'entity_type', 'enc_domain', 'enc_sources', 'enc_related' ) as $mk ) {
					$src = str_replace( 'enc_', '', $mk );
					$v = sanitize_text_field( (string) ( $e[ $mk ] ?? $e[ $src ] ?? '' ) );
					if ( $mk === 'entity_type' && ! in_array( $v, NADLAN_ENC_TYPES, true ) ) { $v = 'term'; }
					if ( $v !== '' ) { update_post_meta( $pid, $mk, $v ); }
				}
				$domain = sanitize_text_field( (string) ( $e['domain'] ?? '' ) );
				if ( $domain !== '' && taxonomy_exists( 'nadlan_term_cat' ) ) {
					wp_set_object_terms( $pid, $domain, 'nadlan_term_cat', false );
				}
			}
			return new WP_REST_Response( array(
				'ok' => true, 'created' => $created, 'scheduled' => $scheduled,
				'drafted' => $drafted, 'skipped_dupes_or_empty' => $skipped,
				'first_publish' => $first, 'last_publish' => $last, 'per_day' => $per_day,
			), 200 );
		},
	) );
} );

/* ---------------- the English term on the page ---------------- */
add_filter( 'the_content', function ( $content ) {
	if ( ! is_singular( 'nadlan_term' ) || ! in_the_loop() || ! is_main_query() ) { return $content; }
	$en   = (string) get_post_meta( get_the_ID(), 'name_en', true );
	$type = (string) get_post_meta( get_the_ID(), 'entity_type', true );
	if ( $en === '' ) { return $content; }
	$chip = '<p class="nl-term-en" style="margin:0 0 14px"><span style="display:inline-block;font:600 13px/1 Heebo,sans-serif;color:#6D665C;background:#F3EEE3;border:1px solid #D6C189;border-radius:999px;padding:6px 14px" dir="ltr">EN: ' . esc_html( $en ) . ( $type && $type !== 'term' ? ' · ' . esc_html( $type ) : '' ) . '</span></p>';
	return $chip . $content;
}, 8 );
