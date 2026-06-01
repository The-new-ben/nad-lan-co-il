<?php
/**
 * nadlan-config — Auction engine (v1.5.0)
 *
 * Timed English auctions with proxy/auto-bid, hidden reserve, soft-close
 * anti-sniping, and buyer's premium. Modeled on Auction.com / Hubzu mechanics.
 *
 * Data model:
 *   - CPT `nadlan_auction` (meta below) links to a `nadlan_property`.
 *   - Custom table {prefix}nadlan_bids for row-level bid integrity (NOT post meta).
 *
 * Concurrency: bid placement is serialized per-auction via a MySQL GET_LOCK so two
 * simultaneous bids can't both "win" the same amount. All price math is server-side.
 *
 * TODO (flagged in docs/listings-questions.md): deposit holds + payment capture wire
 * into Grow/Meshulam; e-sign on win; true realtime (Pusher) instead of /state polling.
 */

if ( ! defined( 'ABSPATH' ) ) { exit; }

const NADLAN_AUCTION_DB_VERSION = '1';

/* ---- bids table (dbDelta, guarded by stored version) ---- */
if ( ! function_exists( 'nadlan_auction_maybe_install_table' ) ) {
	function nadlan_auction_maybe_install_table() {
		if ( get_option( 'nadlan_auction_db_version' ) === NADLAN_AUCTION_DB_VERSION ) { return; }
		global $wpdb;
		$table   = $wpdb->prefix . 'nadlan_bids';
		$charset = $wpdb->get_charset_collate();
		$sql = "CREATE TABLE $table (
			id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
			auction_id BIGINT UNSIGNED NOT NULL,
			user_id BIGINT UNSIGNED NOT NULL,
			amount DECIMAL(15,2) NOT NULL,
			max_amount DECIMAL(15,2) NULL,
			is_auto TINYINT(1) NOT NULL DEFAULT 0,
			is_seller_counter TINYINT(1) NOT NULL DEFAULT 0,
			status VARCHAR(16) NOT NULL DEFAULT 'active',
			ip_address VARCHAR(45) NULL,
			created_at DATETIME(6) NOT NULL,
			PRIMARY KEY (id),
			KEY auction_idx (auction_id),
			KEY user_idx (user_id)
		) $charset;";
		require_once ABSPATH . 'wp-admin/includes/upgrade.php';
		dbDelta( $sql );
		update_option( 'nadlan_auction_db_version', NADLAN_AUCTION_DB_VERSION, false );
	}
}
add_action( 'admin_init', 'nadlan_auction_maybe_install_table' );
register_activation_hook( dirname( __DIR__ ) . '/nadlan-config.php', 'nadlan_auction_maybe_install_table' );

/* ---- auction CPT + meta ---- */
if ( ! function_exists( 'nadlan_auction_register_cpt' ) ) {
	function nadlan_auction_register_cpt() {
		register_post_type( 'nadlan_auction', array(
			'labels'       => array( 'name' => 'NadLan Auctions', 'singular_name' => 'NadLan Auction' ),
			'public'       => true,
			'show_in_rest' => true,
			'has_archive'  => 'auctions',
			'rewrite'      => array( 'slug' => 'auctions' ),
			'menu_icon'    => 'dashicons-hammer',
			'menu_position'=> 30,
			'supports'     => array( 'title', 'editor', 'thumbnail', 'custom-fields', 'excerpt' ),
		) );
		$fields = array(
			'listing_id'           => 'integer',
			'start_time'           => 'string',  // ISO8601 UTC
			'end_time'             => 'string',  // mutable (soft-close extends)
			'starting_price'       => 'number',
			'reserve_price'        => 'number',  // hidden from public output
			'bid_increment'        => 'number',
			'buyers_premium_pct'   => 'number',
			'soft_close_window_sec'=> 'integer',
			'soft_close_extend_sec'=> 'integer',
			'status'               => 'string',  // scheduled|live|extended|ended|sold|reserve_not_met|cancelled
			'current_high_bid'     => 'number',
			'current_high_bidder'  => 'integer',
			'leader_max'           => 'number',  // server-only proxy ceiling of the leader
			'winning_bid_id'       => 'integer',
		);
		foreach ( $fields as $k => $type ) {
			// reserve_price + leader_max are server-only: never expose over REST.
			$expose = ! in_array( $k, array( 'reserve_price', 'leader_max' ), true );
			register_post_meta( 'nadlan_auction', $k, array(
				'show_in_rest'  => $expose,
				'single'        => true,
				'type'          => $type,
				'auth_callback' => function () { return current_user_can( 'edit_posts' ); },
			) );
		}
	}
}
add_action( 'init', 'nadlan_auction_register_cpt' );

/* ---- helpers ---- */
if ( ! function_exists( 'nadlan_auction_increment' ) ) {
	function nadlan_auction_increment( $auction_id ) {
		$inc = (float) get_post_meta( $auction_id, 'bid_increment', true );
		return $inc > 0 ? $inc : 1000.0; // sane default ₪1,000
	}
}
if ( ! function_exists( 'nadlan_auction_min_next' ) ) {
	function nadlan_auction_min_next( $auction_id ) {
		$high = (float) get_post_meta( $auction_id, 'current_high_bid', true );
		if ( $high <= 0 ) {
			return (float) get_post_meta( $auction_id, 'starting_price', true );
		}
		return $high + nadlan_auction_increment( $auction_id );
	}
}
if ( ! function_exists( 'nadlan_auction_effective_status' ) ) {
	/** Derive live/ended from clock without waiting for cron. */
	function nadlan_auction_effective_status( $auction_id ) {
		$status = (string) get_post_meta( $auction_id, 'status', true );
		if ( in_array( $status, array( 'sold', 'reserve_not_met', 'ended', 'cancelled' ), true ) ) {
			return $status;
		}
		$now   = time();
		$start = strtotime( (string) get_post_meta( $auction_id, 'start_time', true ) );
		$end   = strtotime( (string) get_post_meta( $auction_id, 'end_time', true ) );
		if ( $start && $now < $start ) { return 'scheduled'; }
		if ( $end && $now >= $end )    { return 'ended'; }
		return 'live';
	}
}

/* ---- REST: auctions/v1 ---- */
if ( ! function_exists( 'nadlan_auction_register_rest' ) ) {
	function nadlan_auction_register_rest() {
		register_rest_route( 'auctions/v1', '/(?P<id>\d+)/state', array(
			'methods' => 'GET', 'permission_callback' => '__return_true',
			'callback' => 'nadlan_auction_rest_state',
		) );
		register_rest_route( 'auctions/v1', '/(?P<id>\d+)/bids', array(
			array( 'methods' => 'GET', 'permission_callback' => '__return_true',
				'callback' => 'nadlan_auction_rest_bid_history' ),
			array( 'methods' => 'POST', 'permission_callback' => function () { return is_user_logged_in(); },
				'callback' => 'nadlan_auction_rest_place_bid' ),
		) );
	}
}
add_action( 'rest_api_init', 'nadlan_auction_register_rest' );

if ( ! function_exists( 'nadlan_auction_rest_state' ) ) {
	function nadlan_auction_rest_state( $req ) {
		$id = (int) $req['id'];
		if ( get_post_type( $id ) !== 'nadlan_auction' ) {
			return new WP_REST_Response( array( 'ok' => false ), 404 );
		}
		$reserve = (float) get_post_meta( $id, 'reserve_price', true );
		$high    = (float) get_post_meta( $id, 'current_high_bid', true );
		return new WP_REST_Response( array(
			'ok'           => true,
			'status'       => nadlan_auction_effective_status( $id ),
			'current_high' => $high,
			'min_next'     => nadlan_auction_min_next( $id ),
			'end_time'     => get_post_meta( $id, 'end_time', true ),
			'reserve_met'  => ( $reserve > 0 ) ? ( $high >= $reserve ) : true,
			'premium_pct'  => (float) get_post_meta( $id, 'buyers_premium_pct', true ),
		), 200 );
	}
}

if ( ! function_exists( 'nadlan_auction_rest_bid_history' ) ) {
	function nadlan_auction_rest_bid_history( $req ) {
		global $wpdb;
		$id    = (int) $req['id'];
		$table = $wpdb->prefix . 'nadlan_bids';
		$rows  = $wpdb->get_results( $wpdb->prepare(
			"SELECT amount, user_id, is_seller_counter, created_at FROM $table
			 WHERE auction_id = %d AND is_auto = 0 ORDER BY id DESC LIMIT 50", $id
		) );
		$out = array();
		foreach ( (array) $rows as $r ) {
			$u = get_userdata( $r->user_id );
			$mask = $u ? mb_substr( $u->display_name, 0, 1 ) . '***' : 'מתמודד';
			$out[] = array(
				'amount' => (float) $r->amount,
				'bidder' => $r->is_seller_counter ? 'מוכר (הצעת רצפה)' : $mask,
				'time'   => $r->created_at,
			);
		}
		return new WP_REST_Response( array( 'ok' => true, 'bids' => $out ), 200 );
	}
}

/**
 * Place a bid (proxy/auto-bid + soft-close). Serialized per-auction via GET_LOCK.
 */
if ( ! function_exists( 'nadlan_auction_rest_place_bid' ) ) {
	function nadlan_auction_rest_place_bid( $req ) {
		global $wpdb;
		$id   = (int) $req['id'];
		$user = get_current_user_id();
		if ( get_post_type( $id ) !== 'nadlan_auction' ) {
			return new WP_REST_Response( array( 'ok' => false, 'error' => 'no_auction' ), 404 );
		}
		$p   = $req->get_json_params(); if ( ! is_array( $p ) ) { $p = $req->get_params(); }
		$max = isset( $p['max_amount'] ) ? (float) $p['max_amount'] : 0.0;
		$amt = isset( $p['amount'] ) ? (float) $p['amount'] : 0.0;
		if ( $max <= 0 ) { $max = $amt; }          // manual bid: max == amount
		if ( $max <= 0 ) {
			return new WP_REST_Response( array( 'ok' => false, 'error' => 'no_amount' ), 400 );
		}

		// Rate-limit per user
		$rl = 'nadlan_bidrl_' . $user;
		if ( (int) get_transient( $rl ) >= 20 ) {
			return new WP_REST_Response( array( 'ok' => false, 'error' => 'rate' ), 429 );
		}
		set_transient( $rl, ( (int) get_transient( $rl ) ) + 1, MINUTE_IN_SECONDS );

		$lock = 'nadlan_auc_' . $id;
		$got  = (int) $wpdb->get_var( $wpdb->prepare( 'SELECT GET_LOCK(%s, 5)', $lock ) );
		if ( $got !== 1 ) {
			return new WP_REST_Response( array( 'ok' => false, 'error' => 'busy' ), 409 );
		}
		try {
			if ( nadlan_auction_effective_status( $id ) !== 'live' && nadlan_auction_effective_status( $id ) !== 'extended' ) {
				return new WP_REST_Response( array( 'ok' => false, 'error' => 'not_live' ), 409 );
			}
			$min_next = nadlan_auction_min_next( $id );
			if ( $max < $min_next ) {
				return new WP_REST_Response( array( 'ok' => false, 'error' => 'too_low', 'min_next' => $min_next ), 400 );
			}
			$table   = $wpdb->prefix . 'nadlan_bids';
			$now     = current_time( 'mysql' );
			$inc     = nadlan_auction_increment( $id );
			$cur_high   = (float) get_post_meta( $id, 'current_high_bid', true );
			$cur_bidder = (int) get_post_meta( $id, 'current_high_bidder', true );
			$leader_max = (float) get_post_meta( $id, 'leader_max', true );
			$ip = isset( $_SERVER['REMOTE_ADDR'] ) ? substr( (string) $_SERVER['REMOTE_ADDR'], 0, 45 ) : null;

			$insert = function( $amount, $maxv, $auto ) use ( $wpdb, $table, $id, $user, $now, $ip ) {
				$wpdb->insert( $table, array(
					'auction_id' => $id, 'user_id' => $user, 'amount' => $amount,
					'max_amount' => $maxv, 'is_auto' => $auto ? 1 : 0,
					'status' => 'active', 'ip_address' => $ip, 'created_at' => $now,
				) );
				return (int) $wpdb->insert_id;
			};

			if ( $cur_bidder === 0 || $cur_high <= 0 ) {
				// First bid: display at starting price, hold proxy max.
				$display = max( $min_next, (float) get_post_meta( $id, 'starting_price', true ) );
				$bid_id  = $insert( $display, $max, false );
				$new_high = $display; $new_bidder = $user; $new_leadermax = $max;
			} elseif ( $cur_bidder === $user ) {
				// Same leader raising their own proxy ceiling.
				$display = $cur_high; $bid_id = $insert( $display, $max, false );
				$new_high = $cur_high; $new_bidder = $user; $new_leadermax = max( $leader_max, $max );
			} elseif ( $max <= $leader_max ) {
				// Challenger can't beat leader's proxy: leader auto-bids to min($leader_max, max+inc).
				$insert( $max, $max, false );                                  // challenger record (outbid)
				$display = min( $leader_max, $max + $inc );
				$bid_id  = $insert( $display, $leader_max, true );             // leader auto-bid
				$wpdb->update( $table, array( 'status' => 'winning' ), array( 'id' => $bid_id ) );
				$new_high = $display; $new_bidder = $cur_bidder; $new_leadermax = $leader_max;
			} else {
				// Challenger beats leader: challenger leads at min(max, leader_max+inc).
				$display = min( $max, $leader_max + $inc );
				$bid_id  = $insert( $display, $max, false );
				$new_high = $display; $new_bidder = $user; $new_leadermax = $max;
			}

			update_post_meta( $id, 'current_high_bid', $new_high );
			update_post_meta( $id, 'current_high_bidder', $new_bidder );
			update_post_meta( $id, 'leader_max', $new_leadermax );

			// Soft-close anti-sniping
			$end    = strtotime( (string) get_post_meta( $id, 'end_time', true ) );
			$window = (int) get_post_meta( $id, 'soft_close_window_sec', true ) ?: 120;
			$extend = (int) get_post_meta( $id, 'soft_close_extend_sec', true ) ?: 120;
			$extended = false;
			if ( $end && ( $end - time() ) <= $window ) {
				$new_end = gmdate( 'c', time() + $extend );
				update_post_meta( $id, 'end_time', $new_end );
				update_post_meta( $id, 'status', 'extended' );
				$extended = true;
			}
			do_action( 'nadlan_auction_bid_placed', $id, $user, $new_high );

			return new WP_REST_Response( array(
				'ok' => true, 'leading' => ( $new_bidder === $user ),
				'current_high' => $new_high, 'min_next' => $new_high + $inc,
				'end_time' => get_post_meta( $id, 'end_time', true ), 'extended' => $extended,
			), 200 );
		} finally {
			$wpdb->query( $wpdb->prepare( 'SELECT RELEASE_LOCK(%s)', $lock ) );
		}
	}
}

/* ---- closing job (cron every minute; on-page countdown also re-checks) ---- */
if ( ! function_exists( 'nadlan_auction_cron_close' ) ) {
	function nadlan_auction_cron_close() {
		$due = get_posts( array(
			'post_type' => 'nadlan_auction', 'posts_per_page' => 50, 'fields' => 'ids',
			'meta_query' => array(
				array( 'key' => 'status', 'value' => array( 'live', 'extended', 'scheduled' ), 'compare' => 'IN' ),
			),
		) );
		foreach ( (array) $due as $id ) {
			if ( nadlan_auction_effective_status( $id ) !== 'ended' ) { continue; }
			$high    = (float) get_post_meta( $id, 'current_high_bid', true );
			$reserve = (float) get_post_meta( $id, 'reserve_price', true );
			if ( $high > 0 && ( $reserve <= 0 || $high >= $reserve ) ) {
				update_post_meta( $id, 'status', 'sold' );
			} else {
				update_post_meta( $id, 'status', $high > 0 ? 'reserve_not_met' : 'ended' );
			}
			do_action( 'nadlan_auction_closed', $id );
		}
	}
}
add_action( 'nadlan_auction_close_event', 'nadlan_auction_cron_close' );
if ( ! wp_next_scheduled( 'nadlan_auction_close_event' ) ) {
	wp_schedule_event( time() + 60, 'hourly', 'nadlan_auction_close_event' );
}
