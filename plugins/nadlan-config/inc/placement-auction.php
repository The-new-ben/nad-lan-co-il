<?php
/**
 * nadlan-config - GAP 7 placement auction for scarce featured slots.
 */

if ( ! defined( 'ABSPATH' ) ) { exit; }

if ( ! function_exists( 'nadlan_revenue_event' ) ) {
	function nadlan_revenue_event( $type, $amount = 0, $meta = array() ) {
		do_action( 'nadlan_revenue_event', $type, $amount, $meta );
	}
}

if ( ! function_exists( 'nadlan_auction_card_post_types' ) ) {
	function nadlan_auction_card_post_types() {
		return array( 'nadlan_professional', 'nadlan_project', 'nadlan_property' );
	}
}

if ( ! function_exists( 'nadlan_auction_enabled' ) ) {
	function nadlan_auction_enabled() {
		return (bool) apply_filters( 'nadlan_auction_enabled', (bool) get_option( 'nadlan_auction_enabled', true ) );
	}
}

if ( ! function_exists( 'nadlan_auction_option_int' ) ) {
	function nadlan_auction_option_int( $key, $default, $min = 0, $max = 999999 ) {
		return max( $min, min( $max, (int) get_option( $key, $default ) ) );
	}
}

if ( ! function_exists( 'nadlan_auction_category_enabled' ) ) {
	function nadlan_auction_category_enabled( $category ) {
		$enabled = get_option( 'nadlan_auction_enabled_categories', array( 'professional', 'project', 'property' ) );
		if ( ! is_array( $enabled ) ) { $enabled = array( 'professional', 'project', 'property' ); }
		return in_array( sanitize_key( $category ), array_map( 'sanitize_key', $enabled ), true );
	}
}

if ( ! function_exists( 'nadlan_auction_area_key' ) ) {
	function nadlan_auction_area_key( $card_id ) {
		$card_id = (int) $card_id;
		$stored  = sanitize_title( (string) get_post_meta( $card_id, 'auction_area', true ) );
		if ( $stored !== '' ) { return apply_filters( 'nadlan_auction_area_key', $stored, $card_id ); }
		$city = sanitize_title( (string) get_post_meta( $card_id, 'city', true ) );
		if ( $city !== '' ) { return apply_filters( 'nadlan_auction_area_key', $city, $card_id ); }
		$lat = get_post_meta( $card_id, 'lat', true );
		$lng = get_post_meta( $card_id, 'lng', true );
		if ( is_numeric( $lat ) && is_numeric( $lng ) ) {
			return apply_filters( 'nadlan_auction_area_key', 'geo_' . round( (float) $lat, 1 ) . '_' . round( (float) $lng, 1 ), $card_id );
		}
		return apply_filters( 'nadlan_auction_area_key', 'sitewide', $card_id );
	}
}

if ( ! function_exists( 'nadlan_auction_category_key' ) ) {
	function nadlan_auction_category_key( $card_id ) {
		$card_id = (int) $card_id;
		$stored  = sanitize_key( (string) get_post_meta( $card_id, 'auction_category', true ) );
		if ( $stored !== '' ) { return apply_filters( 'nadlan_auction_category_key', $stored, $card_id ); }
		$type = get_post_type( $card_id );
		if ( $type === 'nadlan_professional' ) {
			return apply_filters( 'nadlan_auction_category_key', 'professional', $card_id );
		}
		if ( $type === 'nadlan_project' ) {
			return apply_filters( 'nadlan_auction_category_key', 'project', $card_id );
		}
		if ( $type === 'nadlan_property' ) {
			return apply_filters( 'nadlan_auction_category_key', 'property', $card_id );
		}
		return apply_filters( 'nadlan_auction_category_key', sanitize_key( (string) $type ), $card_id );
	}
}

if ( ! function_exists( 'nadlan_auction_slot_overrides' ) ) {
	function nadlan_auction_slot_overrides() {
		$raw = (string) get_option( 'nadlan_auction_slot_overrides', '' );
		$out = array();
		foreach ( preg_split( '/\r\n|\r|\n/', $raw ) as $line ) {
			$line = trim( $line );
			if ( $line === '' ) { continue; }
			$parts = array_map( 'trim', explode( '|', $line ) );
			if ( count( $parts ) !== 3 ) { continue; }
			$out[ sanitize_title( $parts[0] ) . '|' . sanitize_key( $parts[1] ) ] = max( 1, (int) $parts[2] );
		}
		return $out;
	}
}

if ( ! function_exists( 'nadlan_auction_slot_count' ) ) {
	function nadlan_auction_slot_count( $area, $category ) {
		$overrides = nadlan_auction_slot_overrides();
		$key = sanitize_title( $area ) . '|' . sanitize_key( $category );
		$count = isset( $overrides[ $key ] ) ? (int) $overrides[ $key ] : nadlan_auction_option_int( 'nadlan_auction_slots_default', 3, 1, 20 );
		return (int) apply_filters( 'nadlan_auction_slot_count', $count, $area, $category );
	}
}

if ( ! function_exists( 'nadlan_auction_paid_slot_count' ) ) {
	function nadlan_auction_paid_slot_count( $area, $category ) {
		$slots = nadlan_auction_slot_count( $area, $category );
		if ( get_option( 'nadlan_auction_quality_floor', '1' ) === '1' && $slots > 1 ) {
			return $slots - 1;
		}
		return $slots;
	}
}

if ( ! function_exists( 'nadlan_auction_tier_weight' ) ) {
	function nadlan_auction_tier_weight( $tier ) {
		if ( $tier === 'premier' ) { return 2; }
		if ( $tier === 'pro' ) { return 1; }
		return 0;
	}
}

if ( ! function_exists( 'nadlan_auction_quality_weight' ) ) {
	function nadlan_auction_quality_weight( $quality ) {
		return (string) $quality === 'enriched' ? 1 : 0;
	}
}

if ( ! function_exists( 'nadlan_auction_card_good_standing' ) ) {
	function nadlan_auction_card_good_standing( $card_id ) {
		$tier = (string) get_post_meta( (int) $card_id, 'paid_tier', true );
		if ( ! in_array( $tier, array( 'pro', 'premier' ), true ) ) { return false; }
		$dunning = (string) get_post_meta( (int) $card_id, 'dunning_state', true );
		if ( in_array( $dunning, array( 'retrying', 'lapsed' ), true ) ) { return false; }
		return (bool) apply_filters( 'nadlan_auction_card_good_standing', true, $card_id );
	}
}

if ( ! function_exists( 'nadlan_auction_candidates' ) ) {
	function nadlan_auction_candidates( $area, $category ) {
		$q = new WP_Query( array(
			'post_type'      => nadlan_auction_card_post_types(),
			'post_status'    => array( 'publish', 'pending', 'draft', 'private' ),
			'fields'         => 'ids',
			'posts_per_page' => 500,
			'meta_query'     => array(
				'relation' => 'AND',
				array( 'key' => 'auction_area', 'value' => sanitize_title( $area ) ),
				array( 'key' => 'auction_category', 'value' => sanitize_key( $category ) ),
				array( 'key' => 'auction_bid', 'value' => 0, 'compare' => '>', 'type' => 'NUMERIC' ),
			),
		) );
		$rows = array();
		foreach ( $q->posts as $card_id ) {
			if ( ! nadlan_auction_card_good_standing( $card_id ) ) { continue; }
			$rows[] = array(
				'card_id'      => (int) $card_id,
				'bid'          => (float) get_post_meta( $card_id, 'auction_bid', true ),
				'tier_weight'  => nadlan_auction_tier_weight( (string) get_post_meta( $card_id, 'paid_tier', true ) ),
				'quality'      => nadlan_auction_quality_weight( (string) get_post_meta( $card_id, 'data_quality', true ) ),
				'bid_at'       => (int) get_post_meta( $card_id, 'auction_bid_at', true ),
			);
		}
		wp_reset_postdata();
		usort( $rows, function ( $a, $b ) {
			if ( $a['bid'] !== $b['bid'] ) { return $a['bid'] < $b['bid'] ? 1 : -1; }
			if ( $a['tier_weight'] !== $b['tier_weight'] ) { return $b['tier_weight'] <=> $a['tier_weight']; }
			if ( $a['quality'] !== $b['quality'] ) { return $b['quality'] <=> $a['quality']; }
			return $a['bid_at'] <=> $b['bid_at'];
		} );
		return $rows;
	}
}

if ( ! function_exists( 'nadlan_auction_rank' ) ) {
	function nadlan_auction_rank( $area, $category ) {
		$area     = sanitize_title( $area );
		$category = sanitize_key( $category );
		$cache_key = 'nadlan_auction_rank_' . md5( $area . '|' . $category );
		$cached = get_transient( $cache_key );
		if ( is_array( $cached ) ) { return $cached; }
		$rows = nadlan_auction_candidates( $area, $category );
		$slots = nadlan_auction_paid_slot_count( $area, $category );
		$reserve = (float) get_option( 'nadlan_auction_reserve', 0 );
		$increment = (float) get_option( 'nadlan_auction_increment', 50 );
		foreach ( $rows as $i => $row ) {
			$next_bid = isset( $rows[ $i + 1 ] ) ? (float) $rows[ $i + 1 ]['bid'] : 0;
			$rows[ $i ]['rank'] = $i + 1;
			$rows[ $i ]['winner'] = $i < $slots;
			$rows[ $i ]['clearing_price'] = $rows[ $i ]['winner'] ? max( $reserve, $next_bid + $increment ) : 0;
		}
		set_transient( $cache_key, $rows, 5 * MINUTE_IN_SECONDS );
		return $rows;
	}
}

if ( ! function_exists( 'nadlan_auction_clearing_price' ) ) {
	function nadlan_auction_clearing_price( $area, $category ) {
		$rank = nadlan_auction_rank( $area, $category );
		$slots = nadlan_auction_paid_slot_count( $area, $category );
		$reserve = (float) get_option( 'nadlan_auction_reserve', 0 );
		$increment = (float) get_option( 'nadlan_auction_increment', 50 );
		$next = isset( $rank[ $slots ] ) ? (float) $rank[ $slots ]['bid'] : 0;
		return max( $reserve, $next + $increment );
	}
}

if ( ! function_exists( 'nadlan_auction_clear_rank_cache' ) ) {
	function nadlan_auction_clear_rank_cache() {
		global $wpdb;
		$like = $wpdb->esc_like( '_transient_nadlan_auction_rank_' ) . '%';
		$timeout_like = $wpdb->esc_like( '_transient_timeout_nadlan_auction_rank_' ) . '%';
		$wpdb->query( $wpdb->prepare(
			"DELETE FROM {$wpdb->options} WHERE option_name LIKE %s OR option_name LIKE %s",
			$like,
			$timeout_like
		) );
	}
}

if ( ! function_exists( 'nadlan_auction_clear_area_winners' ) ) {
	function nadlan_auction_clear_area_winners( $area, $category ) {
		$q = new WP_Query( array(
			'post_type'      => nadlan_auction_card_post_types(),
			'post_status'    => 'any',
			'fields'         => 'ids',
			'posts_per_page' => 500,
			'meta_query'     => array(
				'relation' => 'AND',
				array( 'key' => 'auction_area', 'value' => sanitize_title( $area ) ),
				array( 'key' => 'auction_category', 'value' => sanitize_key( $category ) ),
				array( 'key' => '_nadlan_auction_winner', 'value' => '1' ),
			),
		) );
		foreach ( $q->posts as $card_id ) {
			update_post_meta( (int) $card_id, '_nadlan_auction_winner', '0' );
		}
		wp_reset_postdata();
	}
}

if ( ! function_exists( 'nadlan_auction_recompute' ) ) {
	function nadlan_auction_recompute( $area, $category ) {
		$area = sanitize_title( $area );
		$category = sanitize_key( $category );
		delete_transient( 'nadlan_auction_rank_' . md5( $area . '|' . $category ) );
		$rank = nadlan_auction_rank( $area, $category );
		$winners = array();
		nadlan_auction_clear_area_winners( $area, $category );
		foreach ( $rank as $row ) {
			update_post_meta( $row['card_id'], '_nadlan_auction_winner', $row['winner'] ? '1' : '0' );
			update_post_meta( $row['card_id'], 'auction_rank', (int) $row['rank'] );
			update_post_meta( $row['card_id'], 'auction_clearing_price', (float) $row['clearing_price'] );
			if ( $row['winner'] ) { $winners[] = $row; }
		}
		do_action( 'nadlan_auction_settled', $area, $winners );
		return $rank;
	}
}

if ( ! function_exists( 'nadlan_auction_clauses' ) ) {
	function nadlan_auction_clauses( $clauses, $query ) {
		if ( ! nadlan_auction_enabled() || ! $query->get( 'nadlan_paid_placement_boost' ) ) {
			return $clauses;
		}
		global $wpdb;
		$alias = 'nadlan_auction_winner_pm';
		if ( strpos( $clauses['join'], " AS {$alias} " ) === false ) {
			$clauses['join'] .= $wpdb->prepare(
				" LEFT JOIN {$wpdb->postmeta} AS {$alias} ON ({$wpdb->posts}.ID = {$alias}.post_id AND {$alias}.meta_key = %s)",
				'_nadlan_auction_winner'
			);
		}
		$auction_order = "CASE {$alias}.meta_value WHEN '1' THEN 1 ELSE 0 END DESC";
		$clauses['orderby'] = $clauses['orderby'] ? $auction_order . ', ' . $clauses['orderby'] : $auction_order;
		return $clauses;
	}
}
add_filter( 'posts_clauses', 'nadlan_auction_clauses', 25, 2 );

if ( ! function_exists( 'nadlan_auction_rate_ok' ) ) {
	function nadlan_auction_rate_ok( $card_id, $user_id ) {
		$key = 'nadlan_auc_bid_' . (int) $card_id . '_' . (int) $user_id;
		if ( get_transient( $key ) ) { return false; }
		set_transient( $key, 1, 5 * MINUTE_IN_SECONDS );
		return true;
	}
}

add_action( 'rest_api_init', function () {
	register_rest_route( 'nadlan/v1', '/auction/bid', array(
		'methods'             => 'POST',
		'permission_callback' => function () { return is_user_logged_in() ? true : new WP_Error( 'forbidden', 'forbidden', array( 'status' => 403 ) ); },
		'callback'            => function ( $request ) {
			if ( ! nadlan_auction_enabled() ) { return new WP_Error( 'auction_disabled', 'auction_disabled', array( 'status' => 403 ) ); }
			$p = $request->get_json_params();
			if ( ! is_array( $p ) ) { $p = $request->get_params(); }
			$card_id = isset( $p['card_id'] ) ? absint( $p['card_id'] ) : 0;
			$bid = isset( $p['bid'] ) ? (float) $p['bid'] : 0;
			if ( ! $card_id || ! get_post( $card_id ) || ! in_array( get_post_type( $card_id ), nadlan_auction_card_post_types(), true ) ) {
				return new WP_Error( 'bad_card', 'bad_card', array( 'status' => 422 ) );
			}
			if ( ! current_user_can( 'edit_post', $card_id ) ) {
				return new WP_Error( 'forbidden', 'forbidden', array( 'status' => 403 ) );
			}
			if ( ! nadlan_auction_card_good_standing( $card_id ) ) {
				return new WP_Error( 'not_in_good_standing', 'not_in_good_standing', array( 'status' => 402 ) );
			}
			$area = nadlan_auction_area_key( $card_id );
			$category = nadlan_auction_category_key( $card_id );
			if ( ! nadlan_auction_category_enabled( $category ) ) {
				return new WP_Error( 'category_disabled', 'category_disabled', array( 'status' => 403 ) );
			}
			if ( ! nadlan_auction_rate_ok( $card_id, get_current_user_id() ) ) {
				return new WP_Error( 'rate_limited', 'rate_limited', array( 'status' => 429 ) );
			}
			$increment = (float) get_option( 'nadlan_auction_increment', 50 );
			$min = nadlan_auction_clearing_price( $area, $category ) + $increment;
			$current_bid = (float) get_post_meta( $card_id, 'auction_bid', true );
			if ( $bid <= $current_bid || $bid < $min ) {
				return new WP_Error( 'bid_too_low', 'bid_too_low', array( 'status' => 422, 'min_bid' => $min ) );
			}
			$old_rank = nadlan_auction_rank( $area, $category );
			$old_winners = array();
			foreach ( $old_rank as $row ) {
				if ( ! empty( $row['winner'] ) ) { $old_winners[] = (int) $row['card_id']; }
			}
			update_post_meta( $card_id, 'auction_bid', $bid );
			update_post_meta( $card_id, 'auction_area', $area );
			update_post_meta( $card_id, 'auction_category', $category );
			update_post_meta( $card_id, 'auction_bid_at', time() );
			update_post_meta( $card_id, 'auction_next_cycle_amount', $bid );
			update_post_meta( $card_id, 'auction_proration_policy', 'next_cycle' );
			nadlan_revenue_event( 'auction_bid_commitment', $bid, array( 'card_id' => $card_id, 'area' => $area, 'category' => $category ) );
			$new_rank = nadlan_auction_recompute( $area, $category );
			$new_winners = array();
			$own_rank = null;
			foreach ( $new_rank as $row ) {
				if ( ! empty( $row['winner'] ) ) { $new_winners[] = (int) $row['card_id']; }
				if ( (int) $row['card_id'] === $card_id ) { $own_rank = $row; }
			}
			foreach ( array_diff( $old_winners, $new_winners ) as $outbid_card ) {
				do_action( 'nadlan_auction_outbid', (int) $outbid_card, $area );
			}
			return array(
				'ok'             => true,
				'card_id'        => $card_id,
				'area'           => $area,
				'category'       => $category,
				'bid'            => $bid,
				'rank'           => $own_rank ? (int) $own_rank['rank'] : null,
				'winner'         => $own_rank ? (bool) $own_rank['winner'] : false,
				'clearing_price' => $own_rank ? (float) $own_rank['clearing_price'] : 0,
			);
		},
	) );
} );

if ( ! function_exists( 'nadlan_auction_dashboard_context' ) ) {
	function nadlan_auction_dashboard_context( $card_id ) {
		$area = nadlan_auction_area_key( $card_id );
		$category = nadlan_auction_category_key( $card_id );
		$rank = nadlan_auction_rank( $area, $category );
		$mine = null;
		foreach ( $rank as $row ) {
			if ( (int) $row['card_id'] === (int) $card_id ) { $mine = $row; break; }
		}
		return array(
			'area' => $area,
			'category' => $category,
			'competitors' => count( $rank ),
			'slots' => nadlan_auction_slot_count( $area, $category ),
			'paid_slots' => nadlan_auction_paid_slot_count( $area, $category ),
			'rank' => $mine ? (int) $mine['rank'] : null,
			'winner' => $mine ? (bool) $mine['winner'] : false,
			'clearing_price' => $mine ? (float) $mine['clearing_price'] : nadlan_auction_clearing_price( $area, $category ),
		);
	}
}

if ( ! function_exists( 'nadlan_auction_admin_menu' ) ) {
	function nadlan_auction_admin_menu() {
		add_options_page( 'NadLan Placement Auction', 'NadLan Auction', 'manage_options', 'nadlan-placement-auction', 'nadlan_auction_admin_render' );
	}
}
add_action( 'admin_menu', 'nadlan_auction_admin_menu' );

if ( ! function_exists( 'nadlan_auction_admin_render' ) ) {
	function nadlan_auction_admin_render() {
		if ( ! current_user_can( 'manage_options' ) ) { return; }
		if ( isset( $_POST['nadlan_auction_save'] ) && check_admin_referer( 'nadlan_auction_settings' ) ) {
			update_option( 'nadlan_auction_enabled', isset( $_POST['nadlan_auction_enabled'] ) ? '1' : '0', false );
			update_option( 'nadlan_auction_quality_floor', isset( $_POST['nadlan_auction_quality_floor'] ) ? '1' : '0', false );
			update_option( 'nadlan_auction_slots_default', max( 1, min( 20, (int) ( $_POST['nadlan_auction_slots_default'] ?? 3 ) ) ), false );
			update_option( 'nadlan_auction_reserve', max( 0, (float) ( $_POST['nadlan_auction_reserve'] ?? 0 ) ), false );
			update_option( 'nadlan_auction_increment', max( 1, (float) ( $_POST['nadlan_auction_increment'] ?? 50 ) ), false );
			$enabled = array();
			foreach ( array( 'professional', 'project', 'property' ) as $cat ) {
				if ( isset( $_POST[ 'nadlan_auction_cat_' . $cat ] ) ) { $enabled[] = $cat; }
			}
			update_option( 'nadlan_auction_enabled_categories', $enabled, false );
			$overrides = isset( $_POST['nadlan_auction_slot_overrides'] ) ? sanitize_textarea_field( wp_unslash( $_POST['nadlan_auction_slot_overrides'] ) ) : '';
			update_option( 'nadlan_auction_slot_overrides', $overrides, false );
			nadlan_auction_clear_rank_cache();
			echo '<div class="updated"><p>Settings saved.</p></div>';
		}
		$enabled_cats = get_option( 'nadlan_auction_enabled_categories', array( 'professional', 'project', 'property' ) );
		if ( ! is_array( $enabled_cats ) ) { $enabled_cats = array(); }
		?>
		<div class="wrap">
			<h1>NadLan placement auction</h1>
			<form method="post">
				<?php wp_nonce_field( 'nadlan_auction_settings' ); ?>
				<input type="hidden" name="nadlan_auction_save" value="1">
				<table class="form-table" role="presentation">
					<tr><th scope="row">Auction enabled</th><td><label><input type="checkbox" name="nadlan_auction_enabled" value="1" <?php checked( nadlan_auction_enabled() ); ?>> Enabled</label></td></tr>
					<tr><th scope="row">Default slots per area/category</th><td><input type="number" min="1" max="20" name="nadlan_auction_slots_default" value="<?php echo (int) nadlan_auction_option_int( 'nadlan_auction_slots_default', 3, 1, 20 ); ?>"></td></tr>
					<tr><th scope="row">Reserve price</th><td><input type="number" min="0" step="1" name="nadlan_auction_reserve" value="<?php echo esc_attr( (string) get_option( 'nadlan_auction_reserve', 0 ) ); ?>"></td></tr>
					<tr><th scope="row">Minimum increment</th><td><input type="number" min="1" step="1" name="nadlan_auction_increment" value="<?php echo esc_attr( (string) get_option( 'nadlan_auction_increment', 50 ) ); ?>"></td></tr>
					<tr><th scope="row">Quality floor</th><td><label><input type="checkbox" name="nadlan_auction_quality_floor" value="1" <?php checked( get_option( 'nadlan_auction_quality_floor', '1' ), '1' ); ?>> Reserve one slot for new/high-quality organic rotation</label></td></tr>
					<tr><th scope="row">Enabled categories</th><td><?php foreach ( array( 'professional', 'project', 'property' ) as $cat ) : ?><label style="margin-left:12px"><input type="checkbox" name="nadlan_auction_cat_<?php echo esc_attr( $cat ); ?>" value="1" <?php checked( in_array( $cat, $enabled_cats, true ) ); ?>> <?php echo esc_html( $cat ); ?></label><?php endforeach; ?></td></tr>
					<tr><th scope="row">Slot overrides</th><td><textarea name="nadlan_auction_slot_overrides" rows="5" class="large-text" placeholder="tel-aviv|project|3"><?php echo esc_textarea( (string) get_option( 'nadlan_auction_slot_overrides', '' ) ); ?></textarea><p class="description">One per line: area|category|slots.</p></td></tr>
				</table>
				<?php submit_button( 'Save settings' ); ?>
			</form>
		</div>
		<?php
	}
}

add_filter( 'nadlan_config_healthcheck', function ( $out ) {
	$q = new WP_Query( array(
		'post_type'      => nadlan_auction_card_post_types(),
		'post_status'    => 'any',
		'fields'         => 'ids',
		'posts_per_page' => 500,
		'meta_query'     => array( array( 'key' => 'auction_bid', 'value' => 0, 'compare' => '>', 'type' => 'NUMERIC' ) ),
	) );
	$contests = array();
	$winning_bids = array();
	foreach ( $q->posts as $card_id ) {
		$area = nadlan_auction_area_key( $card_id );
		$category = nadlan_auction_category_key( $card_id );
		$key = $area . '|' . $category;
		if ( ! isset( $contests[ $key ] ) ) { $contests[ $key ] = 0; }
		$contests[ $key ]++;
		if ( get_post_meta( $card_id, '_nadlan_auction_winner', true ) === '1' ) {
			$winning_bids[] = (float) get_post_meta( $card_id, 'auction_bid', true );
		}
	}
	wp_reset_postdata();
	$active = 0;
	foreach ( $contests as $count ) {
		if ( $count > 1 ) { $active++; }
	}
	$out['auction'] = array(
		'enabled'          => nadlan_auction_enabled(),
		'active_contests'  => $active,
		'avg_winning_bid'  => $winning_bids ? round( array_sum( $winning_bids ) / count( $winning_bids ), 2 ) : 0,
	);
	return $out;
} );
