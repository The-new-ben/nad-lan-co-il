<?php
/**
 * nadlan-config - RENTALS v2: carry over a landlord's v1 data (HAD-383).
 * v1 kept one JSON blob per building (post meta rm_units on the private CPT
 * nadlan_rentalprop). On the landlord's first v2 visit everything moves into
 * the v2 tables once: buildings, apartments, tenants, leases, the monthly
 * paid/open marks, repairs and notes. The v1 posts stay untouched (rollback).
 */

if ( ! defined( 'ABSPATH' ) ) { exit; }

if ( ! function_exists( 'nlrm_import_legacy' ) ) {
	function nlrm_import_legacy( $owner ) {
		if ( ! $owner || get_user_meta( $owner, 'nlrm_legacy_done', true ) ) { return 0; }
		$ids = get_posts( array( 'post_type' => 'nadlan_rentalprop', 'post_status' => 'any', 'posts_per_page' => 50, 'fields' => 'ids',
			'meta_query' => array( array( 'key' => 'owner_user_id', 'value' => $owner ) ) ) );
		$n = 0;
		foreach ( $ids as $pid ) {
			if ( '1' === (string) get_post_meta( $pid, 'is_demo', true ) || get_post_meta( $pid, 'nlrm_imported', true ) ) { continue; }
			$prop = nlrm_save( 'property', array(
				'address' => (string) get_post_meta( $pid, 'address', true ), 'city' => (string) get_post_meta( $pid, 'city', true ),
				'title' => get_post_field( 'post_title', $pid ), 'floors' => max( 1, (int) get_post_meta( $pid, 'floors', true ) ),
				'units_per_floor' => max( 1, (int) get_post_meta( $pid, 'units_per_floor', true ) ), 'meta' => array( 'from_v1' => (int) $pid ),
			), $owner, 'sys' );
			if ( is_wp_error( $prop ) ) { continue; }
			global $wpdb;
			$wpdb->update( nlrm_t( 'properties' ), array( 'legacy_id' => (int) $pid ), array( 'id' => $prop['id'] ) );
			$units = json_decode( (string) get_post_meta( $pid, 'rm_units', true ), true );
			foreach ( (array) $units as $u ) {
				if ( ! is_array( $u ) ) { continue; }
				$unit = nlrm_save( 'unit', array( 'property_id' => $prop['id'], 'label' => (string) ( $u['label'] ?? '' ), 'floor' => (int) ( $u['floor'] ?? 0 ), 'pos' => (int) ( $u['pos'] ?? 0 ), 'dir' => (string) ( $u['dir'] ?? '' ), 'meta' => array() ), $owner, 'sys' );
				if ( is_wp_error( $unit ) ) { continue; }
				$lease = null;
				if ( ! empty( $u['tenant_name'] ) ) {
					$c = nlrm_save( 'contact', array( 'kind' => 'tenant', 'name' => (string) $u['tenant_name'], 'phone' => (string) ( $u['tenant_phone'] ?? '' ), 'lang' => 'he' ), $owner, 'sys' );
					$sec = (array) ( $u['securities'] ?? array() );
					$lease = nlrm_save( 'lease', array(
						'unit_id' => $unit['id'], 'status' => 'active', 'start_date' => (string) ( $u['start'] ?? '' ), 'end_date' => (string) ( $u['end'] ?? '' ),
						'option_until' => (string) ( $u['option_until'] ?? '' ), 'rent' => (int) ( $u['rent'] ?? 0 ), 'pay_day' => 1,
						'linkage' => array( 'mode' => 'madad' === ( $u['linkage'] ?? '' ) ? 'cpi' : 'none', 'base_date' => (string) ( $u['start'] ?? '' ), 'every' => 12, 'pct' => (int) ( $u['linked_pct'] ?? 100 ), 'floor' => ! empty( $u['floor_clause'] ), 'base_index_v1' => (float) ( $u['base_index'] ?? 0 ) ),
						'securities' => array( 'deposit' => (int) ( $sec['deposit_amount'] ?? 0 ), 'guarantors' => ! empty( $sec['arev'] ), 'bank' => ! empty( $sec['bank'] ), 'cheque_held' => ! empty( $sec['check'] ), 'note_held' => ! empty( $sec['shtar'] ) ),
						'parties' => array( 'tenants' => is_wp_error( $c ) ? array() : array( $c['id'] ) ), 'terms' => array( 'method' => 'transfer', 'v1_docs' => (array) ( $u['docs'] ?? array() ) ),
					), $owner, 'sys' );
					if ( ! is_wp_error( $lease ) ) {
						foreach ( (array) ( $u['ledger'] ?? array() ) as $ym => $state ) {
							if ( ! preg_match( '/^\d{4}-\d{2}$/', (string) $ym ) ) { continue; }
							$key = 'rent:' . $lease['id'] . ':' . $ym;
							$wpdb->insert( nlrm_t( 'ledger' ), array( 'owner_id' => $owner, 'property_id' => $prop['id'], 'unit_id' => $unit['id'], 'lease_id' => $lease['id'], 'kind' => 'charge', 'category' => 'rent', 'amount' => (int) $lease['rent'] * 100, 'due_date' => $ym . '-01', 'status' => 'paid' === $state ? 'paid' : 'open', 'auto_key' => $key, 'created_at' => nlrm_now(), 'updated_at' => nlrm_now() ) );
							$cid = (int) $wpdb->insert_id;
							if ( 'paid' === $state ) {
								$wpdb->insert( nlrm_t( 'ledger' ), array( 'owner_id' => $owner, 'property_id' => $prop['id'], 'unit_id' => $unit['id'], 'lease_id' => $lease['id'], 'kind' => 'payment', 'category' => 'rent', 'amount' => (int) $lease['rent'] * 100, 'paid_date' => $ym . '-01', 'method' => 'transfer', 'status' => 'paid', 'applies_to' => $cid, 'note' => 'v1', 'created_at' => nlrm_now(), 'updated_at' => nlrm_now() ) );
							}
						}
					}
				}
				foreach ( (array) ( $u['maintenance'] ?? array() ) as $m ) {
					if ( ! is_array( $m ) || '' === trim( (string) ( $m['text'] ?? '' ) ) ) { continue; }
					$at = substr( (string) ( $m['at'] ?? '' ), 0, 10 ) ?: gmdate( 'Y-m-d' );
					$urg = 'urgent' === ( $m['urgency'] ?? '' ) ? 'urgent' : 'standard';
					nlrm_save( 'ticket', array( 'property_id' => $prop['id'], 'unit_id' => $unit['id'], 'title' => mb_substr( (string) $m['text'], 0, 160 ), 'urgency' => $urg, 'status' => 'done' === ( $m['status'] ?? '' ) ? 'done' : 'new', 'reporter' => 'owner', 'due_by' => gmdate( 'Y-m-d', strtotime( $at . ' +' . ( 'urgent' === $urg ? 3 : 30 ) . ' days' ) ), 'meta' => array( 'from_v1' => true ) ), $owner, 'sys' );
				}
				if ( ! empty( $u['note'] ) ) { nlrm_event( $owner, 'sys', $lease && ! is_wp_error( $lease ) ? 'lease' : 'unit', $lease && ! is_wp_error( $lease ) ? $lease['id'] : $unit['id'], 'note', '', (string) $u['note'], array( 'from_v1' => true ) ); }
			}
			update_post_meta( $pid, 'nlrm_imported', (int) $prop['id'] );
			$n++;
		}
		update_user_meta( $owner, 'nlrm_legacy_done', gmdate( 'c' ) );
		return $n;
	}
}
