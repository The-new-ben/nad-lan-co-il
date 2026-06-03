<?php
/**
 * nadlan-config - Advertiser order bridge (v1.41.2)
 *
 * Keeps paid advertising orders aligned with the existing directory contract:
 * `paid_tier` is the only ranking/gating source of truth. The only card-level
 * meta added here is campaign_end, paid_order_id, and paid_product_id.
 */
if ( ! defined( 'ABSPATH' ) ) { exit; }

if ( ! function_exists( 'nadlan_ao_products' ) ) {
	function nadlan_ao_products() {
		$labels = function_exists( 'nadlan_ac_products' ) ? nadlan_ac_products() : array();
		$defs = array(
			476 => array( 'tier' => 'pro', 'post_type' => 'nadlan_professional', 'days' => 30 ),
			477 => array( 'tier' => 'premier', 'post_type' => 'nadlan_professional', 'days' => 30 ),
			489 => array( 'tier' => 'premier', 'post_type' => 'nadlan_project', 'days' => 180 ),
			490 => array( 'tier' => 'pro', 'post_type' => 'nadlan_property', 'days' => 60 ),
		);
		foreach ( $defs as $pid => $def ) {
			if ( isset( $labels[ $pid ] ) ) {
				$defs[ $pid ] = array_merge( $labels[ $pid ], $def );
			}
		}
		return $defs;
	}
}

if ( ! function_exists( 'nadlan_ao_product' ) ) {
	function nadlan_ao_product( $product_id ) {
		$products = nadlan_ao_products();
		$product_id = (int) $product_id;
		return isset( $products[ $product_id ] ) ? $products[ $product_id ] : null;
	}
}

if ( ! function_exists( 'nadlan_ao_card_matches_product' ) ) {
	function nadlan_ao_card_matches_product( $card_id, $product_id ) {
		$product = nadlan_ao_product( $product_id );
		$card_id = (int) $card_id;
		if ( ! $product || ! $card_id || ! get_post( $card_id ) ) { return false; }
		return get_post_type( $card_id ) === $product['post_type'];
	}
}

if ( ! function_exists( 'nadlan_ao_user_owns_card' ) ) {
	function nadlan_ao_user_owns_card( $card_id, $user_id ) {
		$owner = (int) get_post_meta( (int) $card_id, 'owner_user_id', true );
		return $owner > 0 && $owner === (int) $user_id;
	}
}

add_filter( 'woocommerce_add_cart_item_data', function ( $cart_item_data, $product_id ) {
	if ( ! nadlan_ao_product( $product_id ) ) { return $cart_item_data; }

	$card_id = isset( $_REQUEST['card_id'] ) ? absint( wp_unslash( $_REQUEST['card_id'] ) ) : 0;
	if ( $card_id && nadlan_ao_card_matches_product( $card_id, $product_id ) ) {
		$cart_item_data['nadlan_card_id'] = $card_id;
		$cart_item_data['nadlan_card_title'] = get_the_title( $card_id );
	}

	return $cart_item_data;
}, 10, 2 );

add_filter( 'woocommerce_get_item_data', function ( $item_data, $cart_item ) {
	if ( empty( $cart_item['nadlan_card_id'] ) ) { return $item_data; }
	$card_id = (int) $cart_item['nadlan_card_id'];
	$title = ! empty( $cart_item['nadlan_card_title'] ) ? (string) $cart_item['nadlan_card_title'] : get_the_title( $card_id );
	$item_data[] = array(
		'key'   => 'כרטיס לפרסום',
		'value' => esc_html( $title . ' #' . $card_id ),
	);
	return $item_data;
}, 10, 2 );

add_action( 'woocommerce_checkout_create_order_line_item', function ( $item, $cart_item_key, $values, $order ) {
	$product_id = (int) $item->get_product_id();
	if ( ! nadlan_ao_product( $product_id ) ) { return; }

	if ( ! empty( $values['nadlan_card_id'] ) && nadlan_ao_card_matches_product( (int) $values['nadlan_card_id'], $product_id ) ) {
		$card_id = (int) $values['nadlan_card_id'];
		$item->add_meta_data( '_nadlan_card_id', $card_id, true );
		$item->add_meta_data( 'כרטיס לפרסום', get_the_title( $card_id ) . ' #' . $card_id, true );
	}
}, 10, 4 );

if ( ! function_exists( 'nadlan_ao_order_item_card_id' ) ) {
	function nadlan_ao_order_item_card_id( $item ) {
		return (int) $item->get_meta( '_nadlan_card_id', true );
	}
}

if ( ! function_exists( 'nadlan_ao_apply_paid_order' ) ) {
	function nadlan_ao_apply_paid_order( $order_id ) {
		if ( ! function_exists( 'wc_get_order' ) ) { return; }
		$order = wc_get_order( $order_id );
		if ( ! $order ) { return; }
		foreach ( $order->get_items() as $item ) {
			nadlan_ao_apply_order_item( $order, $item, false );
		}
	}
}
add_action( 'woocommerce_payment_complete', 'nadlan_ao_apply_paid_order', 20 );

if ( ! function_exists( 'nadlan_ao_apply_order_item' ) ) {
	function nadlan_ao_apply_order_item( $order, $item, $allow_admin = false ) {
		$product_id = (int) $item->get_product_id();
		$product = nadlan_ao_product( $product_id );
		if ( ! $product ) { return array( 'ok' => false, 'code' => 'not_ad_product' ); }

		$card_id = nadlan_ao_order_item_card_id( $item );
		if ( ! $card_id ) { return array( 'ok' => false, 'code' => 'needs_card' ); }
		if ( ! nadlan_ao_card_matches_product( $card_id, $product_id ) ) {
			return array( 'ok' => false, 'code' => 'wrong_card_type' );
		}

		$customer_id = (int) $order->get_customer_id();
		if ( ! $allow_admin && ! nadlan_ao_user_owns_card( $card_id, $customer_id ) ) {
			$order->add_order_note( 'Nadlan advertiser order paid but not activated: card #' . $card_id . ' is not owned by customer #' . $customer_id . '.' );
			return array( 'ok' => false, 'code' => 'ownership_mismatch' );
		}

		if ( (int) get_post_meta( $card_id, 'paid_order_id', true ) === (int) $order->get_id()
			&& (int) get_post_meta( $card_id, 'paid_product_id', true ) === $product_id ) {
			return array( 'ok' => true, 'code' => 'already_applied', 'card_id' => $card_id );
		}

		$now = current_time( 'timestamp' );
		$current_end = (int) get_post_meta( $card_id, 'campaign_end', true );
		$start = max( $now, $current_end );
		$end = $start + ( (int) $product['days'] * DAY_IN_SECONDS );

		update_post_meta( $card_id, 'paid_tier', (string) $product['tier'] );
		update_post_meta( $card_id, 'campaign_end', $end );
		update_post_meta( $card_id, 'paid_order_id', (int) $order->get_id() );
		update_post_meta( $card_id, 'paid_product_id', $product_id );

		$order->add_order_note( 'Nadlan advertiser tier activated for card #' . $card_id . ': ' . $product['tier'] . ' until ' . date_i18n( 'd/m/Y', $end ) . '.' );
		do_action( 'nadlan_advertiser_paid_tier_activated', $card_id, $order, $item, $end );
		return array( 'ok' => true, 'code' => 'activated', 'card_id' => $card_id, 'campaign_end' => $end );
	}
}

if ( ! function_exists( 'nadlan_ao_schedule_downgrade_cron' ) ) {
	function nadlan_ao_schedule_downgrade_cron() {
		if ( ! wp_next_scheduled( 'nadlan_ao_daily_downgrade' ) ) {
			wp_schedule_event( time() + HOUR_IN_SECONDS, 'daily', 'nadlan_ao_daily_downgrade' );
		}
	}
}
add_action( 'init', 'nadlan_ao_schedule_downgrade_cron' );

if ( ! function_exists( 'nadlan_ao_daily_downgrade' ) ) {
	function nadlan_ao_daily_downgrade() {
		$now = current_time( 'timestamp' );
		$q = new WP_Query( array(
			'post_type'      => array( 'nadlan_professional', 'nadlan_project', 'nadlan_property' ),
			'post_status'    => array( 'publish', 'pending', 'draft', 'private' ),
			'fields'         => 'ids',
			'posts_per_page' => 500,
			'meta_query'     => array(
				'relation' => 'AND',
				array( 'key' => 'campaign_end', 'value' => $now, 'compare' => '<', 'type' => 'NUMERIC' ),
				array( 'key' => 'paid_order_id', 'value' => 0, 'compare' => '>', 'type' => 'NUMERIC' ),
				array( 'key' => 'paid_tier', 'value' => array( 'pro', 'premier' ), 'compare' => 'IN' ),
			),
		) );
		foreach ( $q->posts as $post_id ) {
			update_post_meta( $post_id, 'paid_tier', 'free' );
			do_action( 'nadlan_advertiser_paid_tier_expired', (int) $post_id );
		}
		wp_reset_postdata();
	}
}
add_action( 'nadlan_ao_daily_downgrade', 'nadlan_ao_daily_downgrade' );

if ( ! function_exists( 'nadlan_ao_campaign_badge' ) ) {
	function nadlan_ao_campaign_badge( $card_id ) {
		$tier = (string) get_post_meta( (int) $card_id, 'paid_tier', true );
		$end = (int) get_post_meta( (int) $card_id, 'campaign_end', true );
		if ( ! in_array( $tier, array( 'pro', 'premier' ), true ) || ! $end ) { return ''; }
		$class = $end > current_time( 'timestamp' ) ? 'nlac-muted' : 'nlac-muted';
		$text = $end > current_time( 'timestamp' ) ? 'פרסום פעיל עד ' : 'תקופת הפרסום הסתיימה ב-';
		return '<div class="' . esc_attr( $class ) . '">' . esc_html( $text . date_i18n( 'd/m/Y', $end ) ) . '</div>';
	}
}

if ( ! function_exists( 'nadlan_ao_order_summary' ) ) {
	function nadlan_ao_order_summary( $order ) {
		$parts = array();
		foreach ( $order->get_items() as $item ) {
			$product_id = (int) $item->get_product_id();
			$product = nadlan_ao_product( $product_id );
			if ( ! $product ) { continue; }
			$card_id = nadlan_ao_order_item_card_id( $item );
			$text = ! empty( $product['label'] ) ? (string) $product['label'] : 'מסלול פרסום';
			$text .= $card_id ? ' · ' . get_the_title( $card_id ) . ' #' . $card_id : ' · ממתין לחיבור כרטיס';
			$parts[] = '<div class="nlac-muted">' . esc_html( $text ) . '</div>';
		}
		return $parts ? implode( '', $parts ) : '';
	}
}

if ( ! function_exists( 'nadlan_ao_matching_cards' ) ) {
	function nadlan_ao_matching_cards( $cards, $product_id ) {
		$matches = array();
		foreach ( (array) $cards as $card ) {
			if ( nadlan_ao_card_matches_product( $card->ID, $product_id ) ) {
				$matches[] = $card;
			}
		}
		return $matches;
	}
}

if ( ! function_exists( 'nadlan_ao_unlinked_items' ) ) {
	function nadlan_ao_unlinked_items( $orders, $cards = array() ) {
		$items = array();
		$owned_card_ids = array();
		foreach ( (array) $cards as $card ) {
			if ( isset( $card->ID ) ) { $owned_card_ids[] = (int) $card->ID; }
		}
		foreach ( (array) $orders as $order ) {
			foreach ( $order->get_items() as $item ) {
				$product_id = (int) $item->get_product_id();
				if ( ! nadlan_ao_product( $product_id ) ) { continue; }
				$card_id = nadlan_ao_order_item_card_id( $item );
				if ( $card_id
					&& nadlan_ao_card_matches_product( $card_id, $product_id )
					&& ( ! $owned_card_ids || in_array( $card_id, $owned_card_ids, true ) ) ) {
					continue;
				}
				$items[] = array( 'order' => $order, 'item' => $item, 'product_id' => $product_id );
			}
		}
		return $items;
	}
}

if ( ! function_exists( 'nadlan_ao_render_link_box' ) ) {
	function nadlan_ao_render_link_box( $orders, $cards ) {
		if ( ! function_exists( 'wc_get_order' ) ) { return ''; }
		$items = nadlan_ao_unlinked_items( $orders, $cards );
		if ( ! $items ) { return ''; }
		ob_start();
		?>
		<div class="nlac-card">
			<h3 class="nlac-card-title">חיבור רכישות לכרטיסים</h3>
			<p class="nlac-muted">רכישה שלא מחוברת לכרטיס לא יכולה להפעיל את המיקום והדוח. בחרו את הכרטיס המתאים כדי לפתוח את תקופת הפרסום.</p>
			<?php foreach ( $items as $row ) :
				$order = $row['order'];
				$item = $row['item'];
				$product = nadlan_ao_product( $row['product_id'] );
				$matches = nadlan_ao_matching_cards( $cards, $row['product_id'] );
				?>
				<div class="nlac-order">
					<strong>#<?php echo (int) $order->get_id(); ?> · <?php echo esc_html( ! empty( $product['label'] ) ? $product['label'] : 'מסלול פרסום' ); ?></strong>
					<?php if ( ! $matches ) : ?>
						<div class="nlac-muted">אין עדיין כרטיס מתאים בחשבון הזה. קודם מחפשים כרטיס קיים, מבקשים בעלות, או מקימים פרויקט חדש.</div>
					<?php else : ?>
						<form method="post" action="<?php echo esc_url( admin_url( 'admin-post.php' ) ); ?>" style="display:flex;gap:8px;flex-wrap:wrap;margin-top:10px">
							<input type="hidden" name="action" value="nadlan_ac_link_order_item">
							<input type="hidden" name="order_id" value="<?php echo (int) $order->get_id(); ?>">
							<input type="hidden" name="item_id" value="<?php echo (int) $item->get_id(); ?>">
							<?php wp_nonce_field( 'nadlan_ac_link_order_item_' . $order->get_id() . '_' . $item->get_id(), 'nadlan_ac_link_nonce' ); ?>
							<select name="card_id" style="min-height:44px;border:1px solid #E2DCD0;border-radius:6px;padding:0 10px;min-width:220px">
								<?php foreach ( $matches as $card ) : ?>
									<option value="<?php echo (int) $card->ID; ?>"><?php echo esc_html( get_the_title( $card ) . ' #' . $card->ID ); ?></option>
								<?php endforeach; ?>
							</select>
							<button class="nlac-btn gold" type="submit">חברו והפעילו</button>
						</form>
					<?php endif; ?>
				</div>
			<?php endforeach; ?>
		</div>
		<?php
		return ob_get_clean();
	}
}

add_action( 'admin_post_nadlan_ac_link_order_item', function () {
	if ( ! is_user_logged_in() || ! function_exists( 'wc_get_order' ) ) { wp_die( 'login required' ); }
	$order_id = isset( $_POST['order_id'] ) ? absint( wp_unslash( $_POST['order_id'] ) ) : 0;
	$item_id = isset( $_POST['item_id'] ) ? absint( wp_unslash( $_POST['item_id'] ) ) : 0;
	$card_id = isset( $_POST['card_id'] ) ? absint( wp_unslash( $_POST['card_id'] ) ) : 0;
	$nonce = isset( $_POST['nadlan_ac_link_nonce'] ) ? sanitize_text_field( wp_unslash( $_POST['nadlan_ac_link_nonce'] ) ) : '';
	if ( ! $order_id || ! $item_id || ! $card_id || ! wp_verify_nonce( $nonce, 'nadlan_ac_link_order_item_' . $order_id . '_' . $item_id ) ) {
		wp_die( 'bad request' );
	}

	$order = wc_get_order( $order_id );
	if ( ! $order ) { wp_die( 'order not found' ); }
	$is_admin = current_user_can( 'manage_options' );
	if ( ! $is_admin && (int) $order->get_customer_id() !== get_current_user_id() ) {
		wp_die( 'not your order' );
	}

	$item = $order->get_item( $item_id );
	if ( ! $item ) { wp_die( 'item not found' ); }
	$product_id = (int) $item->get_product_id();
	if ( ! nadlan_ao_product( $product_id ) || ! nadlan_ao_card_matches_product( $card_id, $product_id ) ) {
		wp_die( 'card does not match product' );
	}
	if ( ! $is_admin && ! nadlan_ao_user_owns_card( $card_id, get_current_user_id() ) ) {
		wp_die( 'claim this card before linking the purchase' );
	}

	$item->update_meta_data( '_nadlan_card_id', $card_id );
	$item->update_meta_data( 'כרטיס לפרסום', get_the_title( $card_id ) . ' #' . $card_id );
	$item->save();
	$order->add_order_note( 'Nadlan advertiser item linked to card #' . $card_id . ' from Advertiser Center.' );
	if ( is_callable( array( $order, 'is_paid' ) ) && $order->is_paid() ) {
		nadlan_ao_apply_order_item( $order, $item, $is_admin );
	}

	wp_safe_redirect( add_query_arg( 'linked', '1', home_url( '/advertiser-center/' ) ) );
	exit;
} );

add_filter( 'nadlan_config_healthcheck', function ( $out ) {
	$out['advertiser_order_bridge'] = array(
		'activation_hook' => 'woocommerce_payment_complete',
		'uses_paid_tier' => true,
		'card_meta' => array( 'campaign_end', 'paid_order_id', 'paid_product_id' ),
		'daily_downgrade_cron' => (bool) wp_next_scheduled( 'nadlan_ao_daily_downgrade' ),
		'durations_days' => array( 476 => 30, 477 => 30, 489 => 180, 490 => 60 ),
	);
	return $out;
} );
