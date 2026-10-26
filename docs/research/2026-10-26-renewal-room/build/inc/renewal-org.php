<?php
/**
 * nadlan-config - RENEWAL ROOM PRO, the organizing company's account (26.10.2026, LOCAL BUILD, not released).
 *
 *  ACCOUNT    private post type nadlan_renewal_org: name, staff (user ids with admin/staff role, one meta row per staff
 *             member for lookups), plan and paid_until. A room joins an account through its org_id meta; a complex is
 *             ONE room with several buildings inside (renewal_buildings), so the stage, the updates, the invite link and
 *             the two-thirds count stay per complex, and every live one-building room keeps working as is.
 *  PORTFOLIO  GET /renewal-org/{id}/portfolio (and /renewal-org/mine/portfolio for a manager without an account):
 *             per complex the counts, the stage, apartments missing a document, the last activity, the coming deadline
 *             and the reasons it needs attention (codes; the words are in the room's language pack).
 *  BILLING    a WooCommerce product per active complex per month, on the advertiser-orders.php pattern: payment extends
 *             paid_until, a daily check lapses it, a renewal invoice three days before. OFF until option
 *             nadlan_rr_billing_on = '1' AND option nadlan_rr_org_product holds the product id (Ben sets the price).
 *             While off, every account is active. A lapsed account turns its rooms read-only; nothing is ever deleted,
 *             and the rooms stay free for residents and committees.
 */

if ( ! defined( 'ABSPATH' ) ) { exit; }

add_action( 'init', function () {
	register_post_type( 'nadlan_renewal_org', array(
		'labels'              => array( 'name' => 'חברות מארגנות', 'singular_name' => 'חברה מארגנת' ),
		'public'              => false,
		'show_ui'             => true,
		'show_in_rest'        => false,
		'exclude_from_search' => true,
		'publicly_queryable'  => false,
		'rewrite'             => false,
		'has_archive'         => false,
		'show_in_menu'        => 'edit.php?post_type=nadlan_project',
		'supports'            => array( 'title' ),
		'capability_type'     => 'post',
		'map_meta_cap'        => true,
	) );
} );

/* ---------- account and staff ---------- */
if ( ! function_exists( 'nadlan_rr_org_ok' ) ) {
	function nadlan_rr_org_ok( $org ) {
		$p = get_post( (int) $org );
		return $p && 'nadlan_renewal_org' === $p->post_type && 'trash' !== $p->post_status;
	}
}
if ( ! function_exists( 'nadlan_rr_org_staff' ) ) {
	function nadlan_rr_org_staff( $org ) {
		$s = json_decode( (string) get_post_meta( (int) $org, 'org_staff', true ), true );
		return is_array( $s ) ? $s : array();
	}
}
if ( ! function_exists( 'nadlan_rr_org_staff_role' ) ) {
	/** 'admin' | 'staff' | '' */
	function nadlan_rr_org_staff_role( $org, $uid ) {
		if ( ! nadlan_rr_org_ok( $org ) ) { return ''; }
		foreach ( nadlan_rr_org_staff( $org ) as $s ) {
			if ( (int) ( $s['user_id'] ?? 0 ) === (int) $uid && (int) $uid > 0 ) { return 'admin' === ( $s['role'] ?? '' ) ? 'admin' : 'staff'; }
		}
		return '';
	}
}
if ( ! function_exists( 'nadlan_rr_user_orgs' ) ) {
	function nadlan_rr_user_orgs( $uid ) {
		if ( (int) $uid <= 0 ) { return array(); }
		$ids = get_posts( array( 'post_type' => 'nadlan_renewal_org', 'post_status' => 'any', 'posts_per_page' => 20, 'fields' => 'ids',
			'meta_query' => array( array( 'key' => 'org_staff_uid', 'value' => (int) $uid ) ) ) );
		return array_values( array_filter( array_map( 'intval', $ids ), function ( $o ) use ( $uid ) { return '' !== nadlan_rr_org_staff_role( $o, $uid ); } ) );
	}
}
if ( ! function_exists( 'nadlan_rr_org_set_staff' ) ) {
	function nadlan_rr_org_set_staff( $org, $uid, $role ) {
		$staff = array_values( array_filter( nadlan_rr_org_staff( $org ), function ( $s ) use ( $uid ) { return (int) ( $s['user_id'] ?? 0 ) !== (int) $uid; } ) );
		delete_post_meta( $org, 'org_staff_uid', (int) $uid );
		if ( in_array( $role, array( 'admin', 'staff' ), true ) ) {
			$staff[] = array( 'user_id' => (int) $uid, 'role' => $role, 'at' => current_time( 'mysql' ) );
			add_post_meta( $org, 'org_staff_uid', (int) $uid, false );
		}
		update_post_meta( $org, 'org_staff', wp_slash( wp_json_encode( $staff, JSON_UNESCAPED_UNICODE ) ) );
		return $staff;
	}
}
if ( ! function_exists( 'nadlan_rr_billing_on' ) ) {
	function nadlan_rr_billing_on() { return '1' === (string) get_option( 'nadlan_rr_billing_on', '0' ) && (int) get_option( 'nadlan_rr_org_product', 0 ) > 0; }
}
if ( ! function_exists( 'nadlan_rr_org_active' ) ) {
	function nadlan_rr_org_active( $org ) {
		if ( ! nadlan_rr_billing_on() ) { return true; }
		$plan = (string) get_post_meta( (int) $org, 'org_plan', true );
		if ( 'comp' === $plan ) { return true; } // complimentary, set by the site admin
		return (int) get_post_meta( (int) $org, 'org_paid_until', true ) >= current_time( 'timestamp' );
	}
}
if ( ! function_exists( 'nadlan_rr_org_rooms' ) ) {
	function nadlan_rr_org_rooms( $org ) {
		return array_map( 'intval', get_posts( array( 'post_type' => 'nadlan_renewal', 'post_status' => 'any', 'posts_per_page' => 200, 'fields' => 'ids',
			'meta_query' => array( array( 'key' => 'org_id', 'value' => (int) $org ) ) ) ) );
	}
}
if ( ! function_exists( 'nadlan_rr_org_public' ) ) {
	/** What the room shows about the account (name, staff count, active). */
	function nadlan_rr_org_public( $org ) {
		if ( ! $org || ! nadlan_rr_org_ok( $org ) ) { return null; }
		return array( 'id' => (int) $org, 'name' => html_entity_decode( (string) get_post_field( 'post_title', $org ), ENT_QUOTES, 'UTF-8' ),
			'staff' => count( nadlan_rr_org_staff( $org ) ), 'active' => nadlan_rr_org_active( $org ) );
	}
}

/* ---------- the portfolio row of one complex ---------- */
if ( ! function_exists( 'nadlan_rr_portfolio_row' ) ) {
	function nadlan_rr_portfolio_row( $id ) {
		$apts = nadlan_rr_apartments( $id );
		$b = nadlan_rr_buildings( $id );
		$track = (string) get_post_meta( $id, 'track', true );
		$c = nadlan_rr_counts( $apts );
		$law = nadlan_rr_law( $apts, $b, $track );
		$ups = (array) json_decode( (string) get_post_meta( $id, 'renewal_updates', true ), true );
		$last = (string) get_post_meta( $id, 'renewal_last_activity', true );
		foreach ( $ups as $u ) { if ( ! empty( $u['at'] ) && empty( $u['auto'] ) && $u['at'] > $last ) { $last = $u['at']; } }
		foreach ( $apts as $a ) { if ( ! empty( $a['updated'] ) && ! empty( $a['v'] ) && $a['updated'] > $last ) { $last = $a['updated']; } }
		if ( '' === $last ) { $last = (string) get_post_field( 'post_date', $id ); }
		$idle = $last ? max( 0, (int) floor( ( nadlan_rr_today_ts() - strtotime( substr( $last, 0, 10 ) . ' 00:00:00' ) ) / DAY_IN_SECONDS ) ) : null;
		$dl = nadlan_rr_deadlines( $id ); $next = null;
		foreach ( $dl as $d ) { if ( null !== $d['days'] && $d['days'] >= -30 ) { $next = $d; break; } }
		$why = array();
		if ( $c['total'] && $c['refused'] / $c['total'] >= 0.07 ) { $why[] = array( 'code' => 'refused', 'n' => $c['refused'] ); }
		if ( $c['total'] && $c['unreached'] / $c['total'] >= 0.2 ) { $why[] = array( 'code' => 'unreached', 'n' => $c['unreached'] ); }
		if ( null !== $idle && $idle > 14 ) { $why[] = array( 'code' => 'idle', 'n' => $idle ); }
		if ( $next && $next['days'] <= 30 ) { $why[] = array( 'code' => $next['days'] < 0 ? 'deadline_passed' : 'deadline', 'n' => abs( (int) $next['days'] ), 'label' => $next['label'] ); }
		$addr = $b[0]['address'];
		return array(
			'id' => (int) $id,
			'name' => (string) get_post_meta( $id, 'complex_name', true ) ?: html_entity_decode( (string) get_post_field( 'post_title', $id ), ENT_QUOTES, 'UTF-8' ),
			'city' => (string) get_post_meta( $id, 'city', true ),
			'street' => (string) get_post_meta( $id, 'street_line', true ) ?: $addr,
			'track' => $track,
			'stage' => (int) get_post_meta( $id, 'renewal_stage', true ),
			'buildings' => count( $b ),
			'counts' => $c,
			'law' => array( 'applies' => $law['applies'], 'short' => $law['complex']['short'], 'need' => $law['complex']['need'], 'all_met' => $law['all_met'],
				'buildings_short' => count( array_filter( $law['buildings'], function ( $x ) { return false === $x['met']; } ) ) ),
			'last_activity' => substr( $last, 0, 10 ),
			'idle_days' => $idle,
			'next_deadline' => $next ? array( 'label' => $next['label'], 'date' => $next['date'], 'days' => $next['days'] ) : null,
			'attention' => $why,
			'is_sample' => '1' === (string) get_post_meta( $id, 'is_sample', true ),
		);
	}
}

/* ---------- REST ---------- */
add_action( 'rest_api_init', function () {
	register_rest_route( 'nadlan/v1', '/renewal-org/(?P<org>\d+|mine)/portfolio', array(
		'methods' => 'GET',
		'permission_callback' => function ( $req ) {
			if ( ! is_user_logged_in() || ! nadlan_ur_space_on() ) { return false; }
			if ( 'mine' === (string) $req['org'] ) { return true; }
			return current_user_can( 'manage_options' ) || '' !== nadlan_rr_org_staff_role( (int) $req['org'], get_current_user_id() );
		},
		'callback' => function ( $req ) {
			$uid = get_current_user_id();
			if ( 'mine' === (string) $req['org'] ) {
				$ids = array_map( 'intval', get_posts( array( 'post_type' => 'nadlan_renewal', 'post_status' => 'any', 'posts_per_page' => 60, 'fields' => 'ids',
					'meta_query' => array( array( 'key' => 'owner_user_id', 'value' => $uid ) ) ) ) );
				$org = null;
			} else {
				$ids = nadlan_rr_org_rooms( (int) $req['org'] );
				$org = nadlan_rr_org_public( (int) $req['org'] );
			}
			$rows = array();
			foreach ( $ids as $id ) { if ( nadlan_ur_space_ok( $id ) ) { $rows[] = nadlan_rr_portfolio_row( $id ); } }
			usort( $rows, function ( $a, $b ) { return count( $b['attention'] ) <=> count( $a['attention'] ) ?: strcmp( $a['name'], $b['name'] ); } );
			$meta = nadlan_ur_stage_meta( nadlan_ur_req_lang( (string) $req->get_param( 'lang' ) ) );
			return array( 'org' => $org, 'complexes' => $rows, 'today' => substr( current_time( 'mysql' ), 0, 10 ),
				'ladder' => array_column( $meta, 'label' ), 'first_action' => array_map( function ( $m ) { return $m['actions'][0] ?? ''; }, $meta ),
				'can_create' => ! $org || $org['active'], 'org_role' => $org ? nadlan_rr_org_staff_role( $org['id'], $uid ) : '' );
		},
	) );

	/* the site admin opens an account for a company and names its first admin (by the email of an existing user) */
	register_rest_route( 'nadlan/v1', '/renewal-org', array(
		'methods' => 'POST',
		'permission_callback' => function () { return current_user_can( 'manage_options' ); },
		'callback' => function ( WP_REST_Request $req ) {
			$name = mb_substr( sanitize_text_field( (string) $req->get_param( 'name' ) ), 0, 80 );
			$u = get_user_by( 'email', sanitize_email( (string) $req->get_param( 'admin_email' ) ) );
			if ( '' === $name || ! $u ) { return new WP_Error( 'bad_request', 'name and an existing user email', array( 'status' => 400 ) ); }
			$org = wp_insert_post( array( 'post_type' => 'nadlan_renewal_org', 'post_status' => 'private', 'post_title' => $name ), true );
			if ( is_wp_error( $org ) ) { return $org; }
			update_post_meta( $org, 'org_plan', sanitize_key( (string) $req->get_param( 'plan' ) ) ?: 'trial' );
			update_post_meta( $org, 'org_paid_until', 0 );
			nadlan_rr_org_set_staff( $org, $u->ID, 'admin' );
			return nadlan_rr_org_public( $org );
		},
	) );

	/* the account's admin adds or removes staff (existing site users, by email) */
	register_rest_route( 'nadlan/v1', '/renewal-org/(?P<org>\d+)/staff', array(
		'methods' => array( 'GET', 'POST' ),
		'permission_callback' => function ( $req ) {
			return is_user_logged_in() && ( current_user_can( 'manage_options' ) || 'admin' === nadlan_rr_org_staff_role( (int) $req['org'], get_current_user_id() )
				|| ( 'GET' === $req->get_method() && '' !== nadlan_rr_org_staff_role( (int) $req['org'], get_current_user_id() ) ) );
		},
		'callback' => function ( WP_REST_Request $req ) {
			$org = (int) $req['org'];
			if ( 'POST' === $req->get_method() ) {
				$u = get_user_by( 'email', sanitize_email( (string) $req->get_param( 'email' ) ) );
				if ( ! $u ) { return new WP_Error( 'no_user', 'the person needs a site account first', array( 'status' => 404 ) ); }
				$role = sanitize_key( (string) $req->get_param( 'role' ) );
				if ( (int) $u->ID === get_current_user_id() && 'admin' !== $role && ! current_user_can( 'manage_options' ) ) {
					return new WP_Error( 'self', 'an admin cannot remove themselves', array( 'status' => 400 ) );
				}
				nadlan_rr_org_set_staff( $org, $u->ID, $role );
			}
			$out = array();
			foreach ( nadlan_rr_org_staff( $org ) as $s ) {
				$u = get_userdata( (int) $s['user_id'] );
				if ( $u ) { $out[] = array( 'name' => $u->display_name, 'email' => $u->user_email, 'role' => $s['role'] ); }
			}
			return array( 'org' => nadlan_rr_org_public( $org ), 'staff' => $out );
		},
	) );
} );

/* ---------- billing: OFF until Ben sets the product and the switch ---------- */
add_filter( 'woocommerce_add_cart_item_data', function ( $data, $product_id ) {
	if ( ! nadlan_rr_billing_on() || (int) $product_id !== (int) get_option( 'nadlan_rr_org_product', 0 ) ) { return $data; }
	$org = isset( $_REQUEST['org_id'] ) ? absint( wp_unslash( $_REQUEST['org_id'] ) ) : 0; // phpcs:ignore WordPress.Security.NonceVerification
	if ( $org && 'admin' === nadlan_rr_org_staff_role( $org, get_current_user_id() ) ) {
		$data['nadlan_org_id'] = $org;
	}
	return $data;
}, 10, 2 );

add_action( 'woocommerce_checkout_create_order_line_item', function ( $item, $key, $values ) {
	if ( ! nadlan_rr_billing_on() || empty( $values['nadlan_org_id'] ) ) { return; }
	$item->add_meta_data( '_nadlan_org_id', (int) $values['nadlan_org_id'], true );
	$item->add_meta_data( 'חדר ניהול לחברה מארגנת', get_the_title( (int) $values['nadlan_org_id'] ), true );
}, 10, 3 );

if ( ! function_exists( 'nadlan_rr_apply_paid_order' ) ) {
	/** One line item = one complex for 30 days; quantity N = N complexes. Idempotent per order. */
	function nadlan_rr_apply_paid_order( $order_id ) {
		if ( ! nadlan_rr_billing_on() || ! function_exists( 'wc_get_order' ) ) { return; }
		$order = wc_get_order( $order_id );
		if ( ! $order ) { return; }
		foreach ( $order->get_items() as $item ) {
			if ( (int) $item->get_product_id() !== (int) get_option( 'nadlan_rr_org_product', 0 ) ) { continue; }
			$org = (int) $item->get_meta( '_nadlan_org_id', true );
			if ( ! $org || ! nadlan_rr_org_ok( $org ) ) { continue; }
			$done = array_map( 'intval', (array) get_post_meta( $org, 'org_paid_order', false ) );
			if ( in_array( (int) $order->get_id(), $done, true ) ) { continue; }
			$start = max( current_time( 'timestamp' ), (int) get_post_meta( $org, 'org_paid_until', true ) );
			$end = $start + 30 * DAY_IN_SECONDS;
			update_post_meta( $org, 'org_paid_until', $end );
			update_post_meta( $org, 'org_plan', 'paid' );
			update_post_meta( $org, 'org_complexes_paid', max( 1, (int) $item->get_quantity() ) );
			add_post_meta( $org, 'org_paid_order', (int) $order->get_id(), false );
			$order->add_order_note( 'Nadlan renewal room account #' . $org . ' active until ' . date_i18n( 'd/m/Y', $end ) . '.' );
		}
	}
}
add_action( 'woocommerce_payment_complete', 'nadlan_rr_apply_paid_order', 21 );

add_action( 'init', function () {
	if ( nadlan_rr_billing_on() && ! wp_next_scheduled( 'nadlan_rr_org_daily' ) ) {
		wp_schedule_event( time() + HOUR_IN_SECONDS, 'daily', 'nadlan_rr_org_daily' );
	}
} );
add_action( 'nadlan_rr_org_daily', function () {
	if ( ! nadlan_rr_billing_on() || ! function_exists( 'wc_create_order' ) ) { return; }
	$now = current_time( 'timestamp' );
	$orgs = get_posts( array( 'post_type' => 'nadlan_renewal_org', 'post_status' => 'any', 'posts_per_page' => 200, 'fields' => 'ids',
		'meta_query' => array( array( 'key' => 'org_plan', 'value' => 'paid' ) ) ) );
	foreach ( $orgs as $org ) {
		$until = (int) get_post_meta( $org, 'org_paid_until', true );
		if ( $until < $now ) { update_post_meta( $org, 'org_plan', 'lapsed' ); continue; } // read-only, nothing deleted
		if ( $until - $now > 3 * DAY_IN_SECONDS || (int) get_post_meta( $org, 'org_renewal_cycle', true ) === $until ) { continue; }
		$staff = nadlan_rr_org_staff( $org ); $admin = 0;
		foreach ( $staff as $s ) { if ( 'admin' === $s['role'] ) { $admin = (int) $s['user_id']; break; } }
		if ( ! $admin ) { continue; }
		$active = count( nadlan_rr_org_rooms( $org ) );
		$order = wc_create_order( array( 'customer_id' => $admin ) );
		if ( is_wp_error( $order ) ) { continue; }
		$iid = $order->add_product( wc_get_product( (int) get_option( 'nadlan_rr_org_product', 0 ) ), max( 1, $active ) );
		if ( $iid && ( $it = $order->get_item( $iid ) ) ) { $it->add_meta_data( '_nadlan_org_id', (int) $org, true ); $it->save(); }
		$order->calculate_totals();
		$order->update_status( 'pending', 'Nadlan renewal room account #' . $org . ': monthly renewal for ' . $active . ' complexes.' );
		$order->save();
		update_post_meta( $org, 'org_renewal_cycle', $until );
		if ( function_exists( 'WC' ) && WC()->mailer() ) {
			$m = WC()->mailer()->get_emails();
			if ( isset( $m['WC_Email_Customer_Invoice'] ) ) { $m['WC_Email_Customer_Invoice']->trigger( $order->get_id(), $order ); }
		}
	}
} );

add_filter( 'nadlan_config_healthcheck', function ( $out ) {
	$out['renewal_room_pro'] = array( 'loaded' => true, 'billing_on' => nadlan_rr_billing_on() );
	return $out;
} );
