<?php
/**
 * nadlan-config - business metrics + autopilot snapshot (v1.49.0).
 *
 * Computes a daily, cached owner snapshot without requiring the draft billing,
 * lead-routing, auction, or AI branches to be present. When those branches land,
 * this module reads their logs/options automatically.
 */

if ( ! defined( 'ABSPATH' ) ) { exit; }

if ( ! function_exists( 'nadlan_metrics_card_types' ) ) {
	function nadlan_metrics_card_types() {
		$types = array( 'nadlan_professional', 'nadlan_project', 'nadlan_property' );
		return array_values( array_filter( $types, 'post_type_exists' ) );
	}
}

if ( ! function_exists( 'nadlan_metrics_money' ) ) {
	function nadlan_metrics_money( $amount ) {
		return '₪' . number_format( (float) $amount, 0 );
	}
}

if ( ! function_exists( 'nadlan_metrics_tier_amounts' ) ) {
	function nadlan_metrics_tier_amounts() {
		$amounts = array(
			'pro'             => (float) get_option( 'nadlan_metrics_mrr_pro', 349 ),
			'premier'         => (float) get_option( 'nadlan_metrics_mrr_premier', 749 ),
			'property pro'    => (float) get_option( 'nadlan_metrics_mrr_property_pro', 349 ),
			'project premier' => (float) get_option( 'nadlan_metrics_mrr_project_premier', 0 ),
		);
		return apply_filters( 'nadlan_metrics_tier_amounts', $amounts );
	}
}

if ( ! function_exists( 'nadlan_metrics_normalize_tier' ) ) {
	function nadlan_metrics_normalize_tier( $tier ) {
		$tier = strtolower( trim( wp_strip_all_tags( (string) $tier ) ) );
		$tier = preg_replace( '/[\s_-]+/', ' ', $tier );
		return trim( (string) $tier );
	}
}

if ( ! function_exists( 'nadlan_metrics_tier_amount' ) ) {
	function nadlan_metrics_tier_amount( $tier ) {
		$tier = nadlan_metrics_normalize_tier( $tier );
		$amounts = nadlan_metrics_tier_amounts();
		return isset( $amounts[ $tier ] ) ? max( 0, (float) $amounts[ $tier ] ) : 0.0;
	}
}

if ( ! function_exists( 'nadlan_metrics_paid_card_ids' ) ) {
	function nadlan_metrics_paid_card_ids() {
		$types = nadlan_metrics_card_types();
		if ( ! $types ) { return array(); }
		$q = new WP_Query( array(
			'post_type'              => $types,
			'post_status'            => 'any',
			'fields'                 => 'ids',
			'posts_per_page'         => -1,
			'no_found_rows'          => true,
			'update_post_meta_cache' => true,
			'update_post_term_cache' => false,
			'meta_query'             => array(
				array(
					'key'     => 'paid_tier',
					'value'   => array( 'pro', 'premier', 'property pro', 'project premier' ),
					'compare' => 'IN',
				),
			),
		) );
		return array_map( 'intval', (array) $q->posts );
	}
}

if ( ! function_exists( 'nadlan_metrics_gi_log' ) ) {
	function nadlan_metrics_gi_log() {
		$log = get_option( 'nadlan_gi_charge_log', array() );
		return is_array( $log ) ? $log : array();
	}
}

if ( ! function_exists( 'nadlan_metrics_recent_gi_cards' ) ) {
	function nadlan_metrics_recent_gi_cards( $days = 45 ) {
		$since = time() - max( 1, (int) $days ) * DAY_IN_SECONDS;
		$out = array();
		foreach ( nadlan_metrics_gi_log() as $row ) {
			if ( ! is_array( $row ) ) { continue; }
			$ts = (int) ( $row['ts'] ?? $row['t'] ?? 0 );
			$status = sanitize_key( (string) ( $row['status'] ?? '' ) );
			$card_id = (int) ( $row['card_id'] ?? 0 );
			if ( $card_id > 0 && $ts >= $since && $status === 'paid' ) {
				$out[ $card_id ] = true;
			}
		}
		return $out;
	}
}

if ( ! function_exists( 'nadlan_metrics_card_is_billable' ) ) {
	function nadlan_metrics_card_is_billable( $card_id, $tier, $recent_gi_cards ) {
		$card_id = (int) $card_id;
		if ( $card_id <= 0 ) { return false; }
		$is_billable = (int) get_post_meta( $card_id, 'paid_order_id', true ) > 0;
		if ( ! $is_billable && isset( $recent_gi_cards[ $card_id ] ) ) { $is_billable = true; }
		if ( ! $is_billable && (float) get_post_meta( $card_id, 'auction_bid', true ) > 0 ) { $is_billable = true; }
		if ( get_post_meta( $card_id, 'dunning_state', true ) === 'lapsed' ) { $is_billable = false; }
		return (bool) apply_filters( 'nadlan_metrics_card_is_billable', $is_billable, $card_id, $tier, $recent_gi_cards );
	}
}

if ( ! function_exists( 'nadlan_metrics_paid_summary' ) ) {
	function nadlan_metrics_paid_summary() {
		$ids = nadlan_metrics_paid_card_ids();
		$recent_gi = nadlan_metrics_recent_gi_cards( 45 );
		$amounts = nadlan_metrics_tier_amounts();
		$out = array(
			'active_paid_cards'    => count( $ids ),
			'billable_paid_cards'  => 0,
			'editorial_paid_cards' => 0,
			'mrr'                  => 0.0,
			'mrr_at_risk'          => 0.0,
			'by_tier'              => array(),
		);
		foreach ( $amounts as $tier => $amount ) {
			$out['by_tier'][ $tier ] = array( 'cards' => 0, 'billable' => 0, 'mrr' => 0.0 );
		}
		foreach ( $ids as $card_id ) {
			$tier = (string) get_post_meta( $card_id, 'paid_tier', true );
			$tier = nadlan_metrics_normalize_tier( $tier );
			if ( ! isset( $out['by_tier'][ $tier ] ) ) {
				$out['by_tier'][ $tier ] = array( 'cards' => 0, 'billable' => 0, 'mrr' => 0.0 );
			}
			$out['by_tier'][ $tier ]['cards']++;
			$amount = nadlan_metrics_tier_amount( $tier );
			$billable = nadlan_metrics_card_is_billable( $card_id, $tier, $recent_gi );
			if ( $billable ) {
				$out['billable_paid_cards']++;
				$out['by_tier'][ $tier ]['billable']++;
				$out['by_tier'][ $tier ]['mrr'] += $amount;
				$out['mrr'] += $amount;
			} else {
				$out['editorial_paid_cards']++;
			}
			if ( get_post_meta( $card_id, 'dunning_state', true ) === 'retrying' ) {
				$out['mrr_at_risk'] += $amount;
			}
		}
		return $out;
	}
}

if ( ! function_exists( 'nadlan_metrics_auction_summary' ) ) {
	function nadlan_metrics_auction_summary() {
		$types = nadlan_metrics_card_types();
		if ( ! $types ) {
			return array( 'commitment_mrr' => 0.0, 'active_bidders' => 0, 'active_contests' => 0, 'avg_winning_bid' => 0.0, 'fill_rate' => null );
		}
		$q = new WP_Query( array(
			'post_type'              => $types,
			'post_status'            => 'any',
			'fields'                 => 'ids',
			'posts_per_page'         => 500,
			'no_found_rows'          => true,
			'update_post_meta_cache' => true,
			'update_post_term_cache' => false,
			'meta_query'             => array(
				array( 'key' => 'auction_bid', 'value' => 0, 'compare' => '>', 'type' => 'NUMERIC' ),
			),
		) );
		$contests = array();
		$winning_bids = array();
		$commitment = 0.0;
		$winners = 0;
		foreach ( (array) $q->posts as $card_id ) {
			$area = (string) get_post_meta( $card_id, 'auction_area', true );
			$category = (string) get_post_meta( $card_id, 'auction_category', true );
			$key = sanitize_title( $area !== '' ? $area : 'unknown' ) . '|' . sanitize_key( $category !== '' ? $category : 'unknown' );
			$contests[ $key ] = true;
			if ( get_post_meta( $card_id, '_nadlan_auction_winner', true ) === '1' ) {
				$bid = (float) get_post_meta( $card_id, 'auction_next_cycle_amount', true );
				if ( $bid <= 0 ) { $bid = (float) get_post_meta( $card_id, 'auction_bid', true ); }
				$winning_bids[] = $bid;
				$commitment += $bid;
				$winners++;
			}
		}
		$slots_default = max( 1, (int) get_option( 'nadlan_auction_slots_default', 3 ) );
		$available_slots = max( 0, count( $contests ) * $slots_default );
		return array(
			'commitment_mrr'  => $commitment,
			'active_bidders'  => count( (array) $q->posts ),
			'active_contests' => count( $contests ),
			'avg_winning_bid' => $winning_bids ? round( array_sum( $winning_bids ) / count( $winning_bids ), 2 ) : 0.0,
			'fill_rate'       => $available_slots > 0 ? round( $winners / $available_slots, 3 ) : null,
		);
	}
}

if ( ! function_exists( 'nadlan_metrics_lead_summary' ) ) {
	function nadlan_metrics_lead_summary() {
		$since = time() - 7 * DAY_IN_SECONDS;
		$q = new WP_Query( array(
			'post_type'      => 'nadlan_lead',
			'post_status'    => 'any',
			'fields'         => 'ids',
			'posts_per_page' => 1,
			'no_found_rows'  => false,
			'date_query'     => array( array( 'after' => gmdate( 'Y-m-d H:i:s', $since ), 'inclusive' => true ) ),
		) );
		$lead_log = get_option( 'nadlan_lead_log', array() );
		$attempted = 0;
		$delivered = 0;
		if ( is_array( $lead_log ) ) {
			foreach ( $lead_log as $row ) {
				if ( ! is_array( $row ) ) { continue; }
				$ts = (int) ( $row['ts'] ?? $row['t'] ?? $row['time'] ?? 0 );
				if ( $ts && $ts < $since ) { continue; }
				$status = sanitize_key( (string) ( $row['status'] ?? '' ) );
				$attempted++;
				if ( $status === 'delivered_owner' || $status === 'delivered' ) { $delivered++; }
			}
		}
		return array(
			'leads_7d'       => (int) $q->found_posts,
			'route_attempts' => $attempted,
			'delivered'      => $delivered,
			'delivery_rate'  => $attempted > 0 ? round( $delivered / $attempted, 3 ) : null,
		);
	}
}

if ( ! function_exists( 'nadlan_metrics_activation_summary' ) ) {
	function nadlan_metrics_activation_summary() {
		if ( ! class_exists( 'WP_User_Query' ) ) {
			return array( 'new_signups_7d' => 0, 'activated_7d' => 0, 'activation_rate' => null );
		}
		$types = nadlan_metrics_card_types();
		if ( ! $types ) {
			return array( 'new_signups_7d' => 0, 'activated_7d' => 0, 'activation_rate' => null );
		}
		$since = gmdate( 'Y-m-d H:i:s', time() - 7 * DAY_IN_SECONDS );
		$users = new WP_User_Query( array(
			'fields'     => 'ID',
			'number'     => 500,
			'date_query' => array( array( 'after' => $since, 'inclusive' => true ) ),
		) );
		$user_ids = array_map( 'intval', (array) $users->get_results() );
		$activated = 0;
		foreach ( $user_ids as $user_id ) {
			$q = new WP_Query( array(
				'post_type'      => $types,
				'post_status'    => 'publish',
				'fields'         => 'ids',
				'posts_per_page' => 1,
				'no_found_rows'  => true,
				'meta_query'     => array( array( 'key' => 'owner_user_id', 'value' => $user_id, 'type' => 'NUMERIC' ) ),
			) );
			if ( $q->posts ) { $activated++; }
		}
		$total = count( $user_ids );
		return array(
			'new_signups_7d' => $total,
			'activated_7d'   => $activated,
			'activation_rate'=> $total > 0 ? round( $activated / $total, 3 ) : null,
		);
	}
}

if ( ! function_exists( 'nadlan_metrics_ai_summary' ) ) {
	function nadlan_metrics_ai_summary() {
		if ( function_exists( 'nadlan_ai_quality_stats' ) ) {
			$stats = nadlan_ai_quality_stats( 7 );
			return array(
				'deflection_7d'   => $stats['deflection'] ?? null,
				'escalations_7d'  => $stats['escalations'] ?? 0,
				'grounded_rate'   => $stats['grounded_rate'] ?? null,
				'automation_rate' => $stats['automation_rate'] ?? null,
			);
		}
		return array( 'deflection_7d' => null, 'escalations_7d' => 0, 'grounded_rate' => null, 'automation_rate' => null );
	}
}

if ( ! function_exists( 'nadlan_metrics_churn_summary' ) ) {
	function nadlan_metrics_churn_summary( $mrr, $mrr_at_risk ) {
		$month_key = 'nadlan_metrics_month_start_mrr_' . gmdate( 'Ym' );
		$start = get_option( $month_key, null );
		if ( $start === null || $start === false || $start === '' ) {
			update_option( $month_key, (float) $mrr, false );
			$start = null;
		} else {
			$start = (float) $start;
		}
		$lost_mrr = 0.0;
		$since = time() - 30 * DAY_IN_SECONDS;
		$types = nadlan_metrics_card_types();
		if ( $types ) {
			$lapsed = new WP_Query( array(
				'post_type'      => $types,
				'post_status'    => 'any',
				'fields'         => 'ids',
				'posts_per_page' => 500,
				'no_found_rows'  => true,
				'meta_query'     => array(
					array( 'key' => 'gi_lapsed_at', 'value' => $since, 'compare' => '>=', 'type' => 'NUMERIC' ),
				),
			) );
			foreach ( (array) $lapsed->posts as $card_id ) {
				$tier = (string) get_post_meta( $card_id, 'dunning_tier', true );
				if ( $tier === '' ) { $tier = (string) get_post_meta( $card_id, 'paid_tier', true ); }
				$lost_mrr += nadlan_metrics_tier_amount( $tier );
			}
		}
		$revenue_churn = ( $start && $start > 0 ) ? round( $lost_mrr / $start, 3 ) : null;
		$net_mrr_churn = ( $start && $start > 0 ) ? round( ( $lost_mrr - max( 0, $mrr - $start ) ) / $start, 3 ) : null;
		$nrr = ( $start && $start > 0 ) ? round( ( $start + max( 0, $mrr - $start ) - $lost_mrr ) / $start, 3 ) : null;
		return array(
			'start_mrr'       => $start,
			'lost_mrr_30d'    => $lost_mrr,
			'revenue_churn'   => $revenue_churn,
			'logo_churn'      => null,
			'net_mrr_churn'   => $net_mrr_churn,
			'nrr'             => $nrr,
			'mrr_at_risk'     => $mrr_at_risk,
		);
	}
}

if ( ! function_exists( 'nadlan_metrics_order_summary' ) ) {
	function nadlan_metrics_order_summary() {
		$out = array( 'orders_30d' => 0, 'revenue_30d' => 0.0 );
		if ( ! function_exists( 'wc_get_orders' ) ) { return $out; }
		$orders = wc_get_orders( array(
			'limit'        => 100,
			'status'       => array( 'completed', 'processing' ),
			'date_created' => '>' . gmdate( 'Y-m-d', time() - 30 * DAY_IN_SECONDS ),
			'return'       => 'objects',
		) );
		foreach ( (array) $orders as $order ) {
			if ( is_object( $order ) && method_exists( $order, 'get_total' ) ) {
				$out['orders_30d']++;
				$out['revenue_30d'] += (float) $order->get_total();
			}
		}
		return $out;
	}
}

if ( ! function_exists( 'nadlan_metrics_snapshot' ) ) {
	function nadlan_metrics_snapshot( $force = false ) {
		$key = 'nadlan_metrics_snapshot_' . gmdate( 'Ymd' );
		if ( ! $force ) {
			$cached = get_transient( $key );
			if ( is_array( $cached ) ) { return $cached; }
		}
		$paid = nadlan_metrics_paid_summary();
		$auction = nadlan_metrics_auction_summary();
		$mrr = (float) $paid['mrr'] + (float) $auction['commitment_mrr'];
		$lead = nadlan_metrics_lead_summary();
		$activation = nadlan_metrics_activation_summary();
		$orders = nadlan_metrics_order_summary();
		$ai = nadlan_metrics_ai_summary();
		$churn = nadlan_metrics_churn_summary( $mrr, (float) $paid['mrr_at_risk'] );

		$snapshot = array(
			'generated_at'          => time(),
			'mrr'                   => $mrr,
			'active_paid_cards'     => (int) $paid['active_paid_cards'],
			'billable_paid_cards'   => (int) $paid['billable_paid_cards'],
			'editorial_paid_cards'  => (int) $paid['editorial_paid_cards'],
			'paid_by_tier'          => $paid['by_tier'],
			'orders_30d'            => $orders['orders_30d'],
			'revenue_30d'           => $orders['revenue_30d'],
			'new_signups_7d'        => $activation['new_signups_7d'],
			'activation_rate_7d'    => $activation['activation_rate'],
			'lead_volume_7d'        => $lead['leads_7d'],
			'lead_delivery_rate_7d' => $lead['delivery_rate'],
			'ai_deflection_7d'      => $ai['deflection_7d'],
			'ai_escalations_7d'     => $ai['escalations_7d'],
			'auction_revenue_mrr'   => $auction['commitment_mrr'],
			'auction_fill_rate'     => $auction['fill_rate'],
			'auction_avg_bid'       => $auction['avg_winning_bid'],
			'auction_contests'      => $auction['active_contests'],
			'churn'                 => $churn,
		);
		$snapshot = apply_filters( 'nadlan_metrics_snapshot', $snapshot );
		set_transient( $key, $snapshot, DAY_IN_SECONDS );
		update_option( $key, $snapshot, false );
		do_action( 'nadlan_metrics_snapshot_created', $snapshot );
		return $snapshot;
	}
}

if ( ! function_exists( 'nadlan_metrics_pct' ) ) {
	function nadlan_metrics_pct( $value ) {
		return $value === null ? 'אין נתונים' : number_format( (float) $value * 100, 1 ) . '%';
	}
}

if ( ! function_exists( 'nadlan_metrics_render_ops_panel' ) ) {
	function nadlan_metrics_render_ops_panel() {
		if ( ! current_user_can( 'manage_options' ) ) { return; }
		$m = nadlan_metrics_snapshot();
		$lead_e2e = isset( $m['lead_e2e'] ) && is_array( $m['lead_e2e'] ) ? $m['lead_e2e'] : ( function_exists( 'nadlan_lead_e2e_metrics' ) ? nadlan_lead_e2e_metrics( 7 ) : array() );
		?>
		<h2 style="margin-top:28px">Autopilot</h2>
		<p class="description">Snapshot יומי: הכנסות חוזרות, סיכון נטישה, פניות, הפעלה, AI ומכרזי חשיפה.</p>
		<div class="nlops-grid">
			<div class="nlops-card">
				<h2>Revenue</h2>
				<div class="nlops-row"><span>MRR</span><strong><?php echo esc_html( nadlan_metrics_money( $m['mrr'] ) ); ?></strong></div>
				<div class="nlops-row"><span>Revenue 30d</span><strong><?php echo esc_html( nadlan_metrics_money( $m['revenue_30d'] ) ); ?></strong></div>
				<div class="nlops-row"><span>Orders 30d</span><strong><?php echo (int) $m['orders_30d']; ?></strong></div>
				<div class="nlops-row"><span>MRR at risk</span><strong class="<?php echo (float) $m['churn']['mrr_at_risk'] > 0 ? 'nlops-warn' : ''; ?>"><?php echo esc_html( nadlan_metrics_money( $m['churn']['mrr_at_risk'] ) ); ?></strong></div>
			</div>
			<div class="nlops-card">
				<h2>Paid base</h2>
				<div class="nlops-row"><span>Paid-tier cards</span><strong><?php echo (int) $m['active_paid_cards']; ?></strong></div>
				<div class="nlops-row"><span>Billable cards</span><strong><?php echo (int) $m['billable_paid_cards']; ?></strong></div>
				<div class="nlops-row"><span>Editorial premium</span><strong><?php echo (int) $m['editorial_paid_cards']; ?></strong></div>
				<div class="nlops-row"><span>New signups 7d</span><strong><?php echo (int) $m['new_signups_7d']; ?></strong></div>
			</div>
			<div class="nlops-card">
				<h2>Growth</h2>
				<div class="nlops-row"><span>Activation 7d</span><strong><?php echo esc_html( nadlan_metrics_pct( $m['activation_rate_7d'] ) ); ?></strong></div>
				<div class="nlops-row"><span>Leads 7d</span><strong><?php echo (int) $m['lead_volume_7d']; ?></strong></div>
				<div class="nlops-row"><span>Lead delivery</span><strong><?php echo esc_html( nadlan_metrics_pct( $m['lead_delivery_rate_7d'] ) ); ?></strong></div>
				<div class="nlops-row"><span>אישור ללקוח</span><strong><?php echo esc_html( nadlan_metrics_pct( $lead_e2e['ack_rate'] ?? null ) ); ?></strong></div>
				<div class="nlops-row"><span>תגובה ממוצעת</span><strong><?php echo isset( $lead_e2e['avg_response_minutes'] ) && $lead_e2e['avg_response_minutes'] !== null ? esc_html( number_format_i18n( (float) $lead_e2e['avg_response_minutes'], 1 ) . ' דקות' ) : 'אין נתונים'; ?></strong></div>
				<div class="nlops-row"><span>AI deflection</span><strong><?php echo esc_html( nadlan_metrics_pct( $m['ai_deflection_7d'] ) ); ?></strong></div>
			</div>
			<div class="nlops-card">
				<h2>Churn and NRR</h2>
				<div class="nlops-row"><span>Revenue churn</span><strong><?php echo esc_html( nadlan_metrics_pct( $m['churn']['revenue_churn'] ) ); ?></strong></div>
				<div class="nlops-row"><span>Net MRR churn</span><strong><?php echo esc_html( nadlan_metrics_pct( $m['churn']['net_mrr_churn'] ) ); ?></strong></div>
				<div class="nlops-row"><span>NRR</span><strong><?php echo esc_html( nadlan_metrics_pct( $m['churn']['nrr'] ) ); ?></strong></div>
				<div class="nlops-row"><span>Lost MRR 30d</span><strong><?php echo esc_html( nadlan_metrics_money( $m['churn']['lost_mrr_30d'] ) ); ?></strong></div>
			</div>
			<div class="nlops-card">
				<h2>Auction</h2>
				<div class="nlops-row"><span>Committed MRR</span><strong><?php echo esc_html( nadlan_metrics_money( $m['auction_revenue_mrr'] ) ); ?></strong></div>
				<div class="nlops-row"><span>Active contests</span><strong><?php echo (int) $m['auction_contests']; ?></strong></div>
				<div class="nlops-row"><span>Avg winning bid</span><strong><?php echo esc_html( nadlan_metrics_money( $m['auction_avg_bid'] ) ); ?></strong></div>
				<div class="nlops-row"><span>Fill rate</span><strong><?php echo esc_html( nadlan_metrics_pct( $m['auction_fill_rate'] ) ); ?></strong></div>
			</div>
		</div>
		<?php
	}
}
add_action( 'nadlan_ops_after_grid', 'nadlan_metrics_render_ops_panel' );

if ( ! function_exists( 'nadlan_metrics_schedule_digest' ) ) {
	function nadlan_metrics_schedule_digest() {
		if ( ! wp_next_scheduled( 'nadlan_metrics_daily_digest' ) ) {
			wp_schedule_event( time() + HOUR_IN_SECONDS, 'daily', 'nadlan_metrics_daily_digest' );
		}
	}
}
add_action( 'init', 'nadlan_metrics_schedule_digest' );

if ( ! function_exists( 'nadlan_metrics_send_digest' ) ) {
	function nadlan_metrics_send_digest() {
		if ( ! apply_filters( 'nadlan_metrics_digest_enabled', false ) ) { return; }
		$m = nadlan_metrics_snapshot();
		$recipients = apply_filters( 'nadlan_metrics_digest_recipients', array( get_option( 'admin_email' ) ), $m );
		$recipients = array_values( array_filter( array_map( 'sanitize_email', (array) $recipients ) ) );
		if ( ! $recipients ) { return; }
		$subject = apply_filters( 'nadlan_metrics_digest_subject', 'NadLan daily business snapshot', $m );
		$body = sprintf(
			"MRR: %s\nActive paid: %d\nMRR at risk: %s\nLeads 7d: %d\nActivation 7d: %s\nAuction MRR: %s\n",
			nadlan_metrics_money( $m['mrr'] ),
			(int) $m['active_paid_cards'],
			nadlan_metrics_money( $m['churn']['mrr_at_risk'] ),
			(int) $m['lead_volume_7d'],
			nadlan_metrics_pct( $m['activation_rate_7d'] ),
			nadlan_metrics_money( $m['auction_revenue_mrr'] )
		);
		$body = apply_filters( 'nadlan_metrics_digest_body', $body, $m );
		wp_mail( $recipients, $subject, $body );
	}
}
add_action( 'nadlan_metrics_daily_digest', 'nadlan_metrics_send_digest' );

add_filter( 'nadlan_config_healthcheck', function ( $out ) {
	$m = nadlan_metrics_snapshot();
	$out['business'] = array(
		'mrr'           => (float) $m['mrr'],
		'net_churn'     => $m['churn']['net_mrr_churn'],
		'nrr'           => $m['churn']['nrr'],
		'mrr_at_risk'   => (float) $m['churn']['mrr_at_risk'],
		'active_paid'   => (int) $m['active_paid_cards'],
		'lead_volume_7d'=> (int) $m['lead_volume_7d'],
	);
	return $out;
} );
