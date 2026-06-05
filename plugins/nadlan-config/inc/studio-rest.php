<?php
/**
 * nadlan-config — Advertiser STUDIO REST (v1.41.0)
 *
 * Backend for the self-serve advertiser studio. Five endpoints:
 *   POST   /nadlan/v1/studio/<id>/save           — update fields + meta (owned cards)
 *   POST   /nadlan/v1/studio/<id>/upload         — drag-drop image upload
 *   POST   /nadlan/v1/studio/<id>/gallery/reorder — reorder photos
 *   POST   /nadlan/v1/studio/<id>/gallery/delete  — remove a photo
 *   POST   /nadlan/v1/studio/<id>/ai-copy         — AI copy assist (uses concierge if configured)
 *
 * Auth: caller must be logged-in (app password OK) and pass edit_post for the
 * card. Ownership still lives in owner_user_id + claim_status and is mapped by
 * map_meta_cap, so owners can edit only their own listings.
 * The 2,700 imported cold contractors are unaffected — only claimed cards have
 * an owner; only those can be edited.
 */
if ( ! defined( 'ABSPATH' ) ) { exit; }

if ( ! function_exists( 'nadlan_studio_can_edit' ) ) {
	function nadlan_studio_can_edit( $post_id ) {
		$post_id = (int) $post_id;
		if ( $post_id <= 0 ) { return false; }
		$post = get_post( $post_id );
		if ( ! $post ) { return false; }
		if ( ! in_array( $post->post_type, array( 'nadlan_professional', 'nadlan_project', 'nadlan_property' ), true ) ) { return false; }
		$uid = get_current_user_id();
		if ( $uid < 1 ) { return false; }
		if ( current_user_can( 'manage_options' ) ) { return true; }
		return current_user_can( 'edit_post', $post_id );
	}
}

if ( ! function_exists( 'nadlan_studio_supported_fields' ) ) {
	function nadlan_studio_supported_fields( $post_type ) {
		$common = array( 'tagline', 'description', 'city', 'address', 'phone', 'email', 'website',
			'lat', 'lng', 'social_facebook', 'social_instagram', 'social_tiktok', 'social_youtube',
			'video_url' );
		$by_type = array(
			'nadlan_professional' => array_merge( $common, array( 'classification', 'years_active', 'service_area' ) ),
			'nadlan_project'      => array_merge( $common, array( 'project_type', 'project_status', 'developer_name', 'num_units', 'start_year' ) ),
			'nadlan_property'     => array_merge( $common, array( 'listing_type', 'property_type', 'price', 'rooms', 'floor', 'size_sqm', 'parking', 'elevator' ) ),
		);
		return $by_type[ $post_type ] ?? $common;
	}
}

add_action( 'rest_api_init', function () {

	$auth_owner = function ( $req ) {
		return nadlan_studio_can_edit( (int) ( $req['id'] ?? 0 ) ) ? true : new WP_Error( 'forbidden', 'forbidden', array( 'status' => 403 ) );
	};

	// SAVE — partial update of fields/meta. Strict allow-list per post type.
	register_rest_route( 'nadlan/v1', '/studio/(?P<id>\d+)/save', array(
		'methods'             => 'POST',
		'permission_callback' => $auth_owner,
		'callback'            => function ( $req ) {
			$id   = (int) $req['id'];
			$post = get_post( $id );
			$p    = $req->get_json_params() ?: array();
			$allowed = nadlan_studio_supported_fields( $post->post_type );

			// post title + content via post update if provided
			$upd = array( 'ID' => $id );
			if ( isset( $p['title'] ) ) {
				$t = sanitize_text_field( (string) $p['title'] );
				if ( $t !== '' ) { $upd['post_title'] = $t; }
			}
			if ( isset( $p['content_html'] ) ) {
				$upd['post_content'] = wp_kses_post( (string) $p['content_html'] );
			}
			if ( count( $upd ) > 1 ) { wp_update_post( $upd, true ); }

			$written = array();
			foreach ( $allowed as $k ) {
				if ( ! array_key_exists( $k, $p ) ) { continue; }
				$v = $p[ $k ];
				switch ( $k ) {
					case 'phone':
						$v = preg_replace( '/[^0-9+\- ]/', '', (string) $v );
						break;
					case 'email':
						$v = sanitize_email( (string) $v );
						break;
					case 'website':
					case 'video_url':
					case 'social_facebook':
					case 'social_instagram':
					case 'social_tiktok':
					case 'social_youtube':
						$v = esc_url_raw( (string) $v );
						break;
					case 'lat':
					case 'lng':
						$v = is_numeric( $v ) ? round( (float) $v, 6 ) : '';
						break;
					case 'price':
					case 'num_units':
					case 'floor':
					case 'size_sqm':
					case 'start_year':
					case 'years_active':
						$v = (int) $v;
						break;
					case 'rooms':
						$v = (float) $v;
						break;
					case 'parking':
					case 'elevator':
						$v = $v ? 1 : 0;
						break;
					case 'description':
					case 'tagline':
					case 'service_area':
						$v = sanitize_textarea_field( (string) $v );
						break;
					default:
						$v = sanitize_text_field( (string) $v );
				}
				update_post_meta( $id, $k, $v );
				$written[] = $k;
			}
			// auto-mark as enriched once we have a description + an image
			$has_desc  = mb_strlen( (string) get_post_meta( $id, 'description', true ) ) > 80;
			$has_photo = trim( (string) get_post_meta( $id, 'photos_csv', true ) ) !== '';
			if ( $has_desc && $has_photo ) {
				update_post_meta( $id, 'data_quality', 'enriched' );
			}
			// invalidate the social-proof cache so the homepage reflects the change
			delete_transient( 'nadlan_sp_block_v3' );

			return array( 'ok' => true, 'written' => $written, 'post_id' => $id );
		},
	) );

	// UPLOAD — accept multipart image, attach to post, append to photos_csv
	register_rest_route( 'nadlan/v1', '/studio/(?P<id>\d+)/upload', array(
		'methods'             => 'POST',
		'permission_callback' => $auth_owner,
		'callback'            => function ( $req ) {
			$id = (int) $req['id'];
			if ( empty( $_FILES['file'] ) ) { return new WP_Error( 'no_file', 'no_file', array( 'status' => 400 ) ); }
			require_once ABSPATH . 'wp-admin/includes/file.php';
			require_once ABSPATH . 'wp-admin/includes/media.php';
			require_once ABSPATH . 'wp-admin/includes/image.php';
			$file = $_FILES['file'];
			// hard guard: file type + size
			$type = wp_check_filetype( $file['name'] ?? '' );
			if ( ! in_array( strtolower( $type['ext'] ?? '' ), array( 'jpg', 'jpeg', 'png', 'webp', 'gif' ), true ) ) {
				return new WP_Error( 'bad_type', 'bad_type', array( 'status' => 415 ) );
			}
			if ( (int) ( $file['size'] ?? 0 ) > 10 * 1024 * 1024 ) {
				return new WP_Error( 'too_big', 'too_big', array( 'status' => 413 ) );
			}
			$attach_id = media_handle_upload( 'file', $id );
			if ( is_wp_error( $attach_id ) ) { return $attach_id; }
			$url = wp_get_attachment_url( $attach_id );

			// append to photos_csv (URL list)
			$existing = (string) get_post_meta( $id, 'photos_csv', true );
			$urls = array_filter( array_map( 'trim', explode( ',', $existing ) ) );
			if ( $url && ! in_array( $url, $urls, true ) ) { $urls[] = $url; }
			update_post_meta( $id, 'photos_csv', implode( ',', $urls ) );

			// first upload becomes the featured image
			if ( ! has_post_thumbnail( $id ) ) {
				set_post_thumbnail( $id, $attach_id );
			}
			return array( 'ok' => true, 'attachment_id' => $attach_id, 'url' => $url, 'photos_count' => count( $urls ) );
		},
	) );

	// REORDER — accept ordered list of URLs
	register_rest_route( 'nadlan/v1', '/studio/(?P<id>\d+)/gallery/reorder', array(
		'methods'             => 'POST',
		'permission_callback' => $auth_owner,
		'callback'            => function ( $req ) {
			$id = (int) $req['id'];
			$p  = $req->get_json_params() ?: array();
			$urls = isset( $p['urls'] ) && is_array( $p['urls'] ) ? array_map( 'esc_url_raw', $p['urls'] ) : array();
			update_post_meta( $id, 'photos_csv', implode( ',', array_filter( $urls ) ) );
			return array( 'ok' => true, 'count' => count( $urls ) );
		},
	) );

	// DELETE — remove URL from photos_csv (does NOT trash media library by default)
	register_rest_route( 'nadlan/v1', '/studio/(?P<id>\d+)/gallery/delete', array(
		'methods'             => 'POST',
		'permission_callback' => $auth_owner,
		'callback'            => function ( $req ) {
			$id = (int) $req['id'];
			$p  = $req->get_json_params() ?: array();
			$drop = esc_url_raw( (string) ( $p['url'] ?? '' ) );
			if ( ! $drop ) { return new WP_Error( 'invalid', 'invalid', array( 'status' => 400 ) ); }
			$existing = (string) get_post_meta( $id, 'photos_csv', true );
			$urls = array_values( array_filter( array_map( 'trim', explode( ',', $existing ) ), function ( $u ) use ( $drop ) { return $u && $u !== $drop; } ) );
			update_post_meta( $id, 'photos_csv', implode( ',', $urls ) );
			return array( 'ok' => true, 'count' => count( $urls ) );
		},
	) );

	// AI COPY — call the existing concierge with a "rewrite this" prompt
	register_rest_route( 'nadlan/v1', '/studio/(?P<id>\d+)/ai-copy', array(
		'methods'             => 'POST',
		'permission_callback' => $auth_owner,
		'callback'            => function ( $req ) {
			$p   = $req->get_json_params() ?: array();
			$src = sanitize_textarea_field( (string) ( $p['source'] ?? '' ) );
			$mode= sanitize_key( (string) ( $p['mode'] ?? 'improve' ) );
			if ( mb_strlen( $src ) < 5 ) { return new WP_Error( 'too_short', 'too_short', array( 'status' => 400 ) ); }
			if ( ! function_exists( 'nadlan_ai_enabled' ) || ! nadlan_ai_enabled() ) {
				return new WP_REST_Response( array( 'ok' => false, 'error' => 'AI_DISABLED', 'message' => 'הצ\'אט החכם לא פעיל. הזינו מפתח Anthropic ב-Settings → NadLan AI כדי להפעיל את עוזר הכתיבה.' ), 503 );
			}
			$prompts = array(
				'improve' => 'שפר את הטקסט הבא לתיאור מקצועי, חם, אמין ותמציתי (3-5 משפטים) לעסק נדל"ן. שמור על העובדות. אל תוסיף בלוטים שלא במקור. עברית פשוטה.',
				'shorter' => 'קצר את הטקסט הבא לעד 3 משפטים. שמור על העובדות.',
				'longer'  => 'הרחב את הטקסט הבא לתיאור עשיר ומפורט יותר (5-7 משפטים), בלי להמציא פרטים שלא קיימים.',
				'pro'     => 'הפוך את הטקסט הבא למקצועי ורשמי יותר.',
				'friendly'=> 'הפוך את הטקסט הבא לחם ואנושי יותר.',
			);
			$instruction = $prompts[ $mode ] ?? $prompts['improve'];
			$body = array(
				'model'      => apply_filters( 'nadlan_ai_model', 'claude-haiku-4-5' ),
				'max_tokens' => 600,
				'system'     => $instruction . " החזר רק את הטקסט המתוקן, בלי מבוא, בלי הסבר.",
				'messages'   => array( array( 'role' => 'user', 'content' => $src ) ),
			);
			$resp = wp_remote_post( 'https://api.anthropic.com/v1/messages', array(
				'headers' => array(
					'x-api-key' => nadlan_ai_key(),
					'anthropic-version' => '2023-06-01',
					'content-type' => 'application/json',
				),
				'body' => wp_json_encode( $body, JSON_UNESCAPED_UNICODE ),
				'timeout' => 30,
			) );
			if ( is_wp_error( $resp ) ) { return new WP_Error( 'upstream', $resp->get_error_message() ); }
			$data = json_decode( wp_remote_retrieve_body( $resp ), true );
			$out  = '';
			foreach ( (array) ( $data['content'] ?? array() ) as $block ) {
				if ( ( $block['type'] ?? '' ) === 'text' ) { $out .= $block['text']; }
			}
			return array( 'ok' => true, 'text' => trim( $out ) );
		},
	) );

	// GET — fetch the current snapshot to populate the editor on load
	register_rest_route( 'nadlan/v1', '/studio/(?P<id>\d+)', array(
		'methods'             => 'GET',
		'permission_callback' => $auth_owner,
		'callback'            => function ( $req ) {
			$id   = (int) $req['id'];
			$post = get_post( $id );
			$type = $post->post_type;
			$fields = nadlan_studio_supported_fields( $type );
			$out = array(
				'id'           => $id,
				'post_type'    => $type,
				'title'        => $post->post_title,
				'content_html' => $post->post_content,
				'permalink'    => get_permalink( $id ),
				'photos'       => array_values( array_filter( array_map( 'trim', explode( ',', (string) get_post_meta( $id, 'photos_csv', true ) ) ) ) ),
				'meta'         => array(),
			);
			foreach ( $fields as $k ) { $out['meta'][ $k ] = get_post_meta( $id, $k, true ); }
			return $out;
		},
	) );

	// LIST MY CARDS — for the advertiser dashboard
	register_rest_route( 'nadlan/v1', '/studio/mine', array(
		'methods'             => 'GET',
		'permission_callback' => function () { return is_user_logged_in() ? true : new WP_Error( 'forbidden', 'forbidden', array( 'status' => 403 ) ); },
		'callback'            => function () {
			$uid = get_current_user_id();
			$q = new WP_Query( array(
				'post_type'      => array( 'nadlan_professional', 'nadlan_project', 'nadlan_property' ),
				'post_status'    => 'publish',
				'posts_per_page' => 50,
				'meta_query'     => array( array( 'key' => 'owner_user_id', 'value' => (int) $uid ) ),
			) );
			$out = array();
			foreach ( $q->posts as $p ) {
				$views = (int) get_post_meta( $p->ID, 'view_count', true );
				$rating= (float) get_post_meta( $p->ID, 'rating', true );
				$revs  = (int) get_post_meta( $p->ID, 'reviews_count', true );
				$tier  = (string) get_post_meta( $p->ID, 'paid_tier', true ) ?: 'free';
				$photos= (string) get_post_meta( $p->ID, 'photos_csv', true );
				$out[] = array(
					'id' => $p->ID,
					'post_type' => $p->post_type,
					'title' => get_the_title( $p ),
					'permalink' => get_permalink( $p ),
					'tier' => $tier,
					'photos_count' => count( array_filter( explode( ',', $photos ) ) ),
					'views' => $views,
					'rating' => $rating,
					'reviews' => $revs,
				);
			}
			wp_reset_postdata();
			return array( 'ok' => true, 'cards' => $out );
		},
	) );

	/* CREATE — a logged-in user creates a brand-new listing they own.
	 * The "list your asset" entry point: a new advertiser who is NOT in the
	 * gov.il import can publish a property / project / professional card from
	 * scratch, then edit it in Studio. Owned immediately (owner_user_id +
	 * claim_status=verified) and starts as a stub (data_quality=stub →
	 * schema.php noindex guard keeps it out of the index until enriched). */
	register_rest_route( 'nadlan/v1', '/studio/create', array(
		'methods'             => 'POST',
		'permission_callback' => function () {
			return is_user_logged_in() ? true : new WP_Error( 'forbidden', 'יש להתחבר כדי לפרסם.', array( 'status' => 403 ) );
		},
		'callback'            => function ( $req ) {
			$uid = get_current_user_id();
			$p   = $req->get_json_params() ?: array();
			$type_map = array(
				'property'     => 'nadlan_property',
				'project'      => 'nadlan_project',
				'professional' => 'nadlan_professional',
			);
			$type = sanitize_key( (string) ( $p['type'] ?? '' ) );
			if ( ! isset( $type_map[ $type ] ) ) {
				return new WP_Error( 'bad_type', 'יש לבחור סוג פרסום.', array( 'status' => 400 ) );
			}
			$post_type = $type_map[ $type ];
			$title = trim( mb_substr( sanitize_text_field( (string) ( $p['title'] ?? '' ) ), 0, 120 ) );
			if ( $title === '' ) {
				$defaults = array( 'property' => 'נכס חדש', 'project' => 'פרויקט חדש', 'professional' => 'כרטיס בעל מקצוע' );
				$title = $defaults[ $type ];
			}
			// anti-abuse: max 10 new listings per user per day
			$rk = 'nadlan_studio_create_' . $uid;
			$ct = (int) get_transient( $rk );
			if ( $ct >= 10 && ! current_user_can( 'manage_options' ) ) {
				return new WP_Error( 'rate', 'הגעתם למספר הפרסומים המרבי להיום. נסו שוב מחר.', array( 'status' => 429 ) );
			}
			$new_id = wp_insert_post( array(
				'post_type'   => $post_type,
				'post_status' => 'publish',
				'post_title'  => $title,
				'post_author' => $uid,
			), true );
			if ( is_wp_error( $new_id ) ) { return $new_id; }
			update_post_meta( $new_id, 'owner_user_id', (int) $uid );
			update_post_meta( $new_id, 'claim_status', 'verified' );
			update_post_meta( $new_id, 'data_quality', 'stub' );
			update_post_meta( $new_id, 'paid_tier', 'free' );
			update_post_meta( $new_id, 'created_via', 'studio_self_serve' );
			if ( function_exists( 'nadlan_roles_assign_user' ) ) {
				nadlan_roles_assign_user( (int) $uid, true );
			}
			set_transient( $rk, $ct + 1, DAY_IN_SECONDS );
			return array(
				'ok'        => true,
				'id'        => $new_id,
				'post_type' => $post_type,
				'edit_url'  => home_url( '/studio/?id=' . $new_id ),
			);
		},
	) );
} );
