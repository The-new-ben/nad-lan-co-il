<?php
/**
 * nadlan-config - RENEWAL ROOM PRO, server logic (26.10.2026, LOCAL BUILD, not released).
 *
 * Loaded by urban-space.php (require_once at its end). Adds to the live room, never removes from it:
 *
 *  ROLES        nadlan_rr_role(): admin > owner (opened the room) > org (staff of the organizing company that owns the room)
 *               > committee (a member the managers marked as committee) > neighbor (a member who joined by the link).
 *  PRIVACY      nadlan_rr_filter_payload(): managers get everything; the committee gets every apartment's status and
 *               document ticks but never a name, a note or a contact note; a neighbour gets the building totals, the
 *               stage, the updates and THEIR OWN apartment only (after a manager approved their claim). Whether a
 *               neighbour also sees the status colour of every apartment is a per-room setting (neighbor_grid): legacy
 *               committee rooms keep it on (the live room always showed it), organizer rooms start with it off.
 *  ONE SAVE     nadlan_rr_save_apartment(): one apartment per request, with its version number. The stored JSON is
 *               swapped only if nobody wrote in between (compare-and-swap on the meta row); another apartment saved
 *               meanwhile is merged, the SAME apartment saved meanwhile returns 409 with the fresh apartment.
 *  CHANGE LOG   one postmeta row per change (meta key renewal_apt_event, non-unique): who, when, field, from, to.
 *               Rows are only ever added; the room has no route that edits or deletes them. Notes and contact notes
 *               are logged as "changed" without their text (data minimisation).
 *  OWNERS       owners[] per apartment: name or initials, share, heir flag, signed flag. An apartment COUNTS as signed
 *               only when its status is "signed" and every listed owner signed (the careful rule; a lawyer confirms).
 *  THE LAW      nadlan_rr_law(): the three conditions of the statutory special majority (Pinui-Binui Law 2006, s. 1,
 *               read in urban-tools.php nadlan_ur_thresholds()): two thirds of the apartments in the complex, three
 *               fifths in each building (4 or 5 apartments: at least 3, with more than two owners), more than half of
 *               the common property in each building (only when every apartment's share from the Tabu is entered).
 *               Shown as facts about the room's data, never as "the majority was reached" legal advice.
 *  DEADLINES    dates the organizer or the lawyer enters (from the agreement or the law); the room counts the days.
 *               No legal period is hard-coded.
 *
 * Nothing here stores a file. ID copies and documents stay with the organizer (the live rule).
 */

if ( ! defined( 'ABSPATH' ) ) { exit; }

/* ---------- small helpers ---------- */
if ( ! function_exists( 'nadlan_rr_json' ) ) {
	function nadlan_rr_json( $id, $key, $default = array() ) {
		$v = json_decode( (string) get_post_meta( $id, $key, true ), true );
		return is_array( $v ) ? $v : $default;
	}
}
if ( ! function_exists( 'nadlan_rr_put_json' ) ) {
	function nadlan_rr_put_json( $id, $key, $value ) {
		return update_post_meta( $id, $key, wp_slash( wp_json_encode( $value, JSON_UNESCAPED_UNICODE ) ) );
	}
}
if ( ! function_exists( 'nadlan_rr_today_ts' ) ) {
	/** Local midnight today as a timestamp (the site's timezone, via current_time). */
	function nadlan_rr_today_ts() {
		return (int) strtotime( substr( current_time( 'mysql' ), 0, 10 ) . ' 00:00:00' );
	}
}
if ( ! function_exists( 'nadlan_rr_days_until' ) ) {
	function nadlan_rr_days_until( $ymd ) {
		$t = strtotime( (string) $ymd . ' 00:00:00' );
		if ( ! $t ) { return null; }
		return (int) round( ( $t - nadlan_rr_today_ts() ) / DAY_IN_SECONDS );
	}
}

/* ---------- buildings and apartments (legacy rooms are a complex of one building) ---------- */
if ( ! function_exists( 'nadlan_rr_buildings' ) ) {
	function nadlan_rr_buildings( $id ) {
		$b = nadlan_rr_json( $id, 'renewal_buildings' );
		$out = array();
		foreach ( $b as $i => $x ) {
			if ( ! is_array( $x ) || empty( $x['key'] ) ) { continue; }
			$out[] = array(
				'key'     => sanitize_key( $x['key'] ),
				'label'   => mb_substr( sanitize_text_field( (string) ( $x['label'] ?? '' ) ), 0, 40 ),
				'address' => mb_substr( sanitize_text_field( (string) ( $x['address'] ?? '' ) ), 0, 120 ),
				'floors'  => max( 1, min( 40, (int) ( $x['floors'] ?? 1 ) ) ),
				'upf'     => max( 1, min( 12, (int) ( $x['upf'] ?? 1 ) ) ),
			);
		}
		if ( ! $out ) {
			$out[] = array(
				'key'     => 'b1',
				'label'   => '',
				'address' => (string) get_post_meta( $id, 'address', true ),
				'floors'  => max( 1, (int) get_post_meta( $id, 'floors', true ) ),
				'upf'     => max( 1, (int) get_post_meta( $id, 'units_per_floor', true ) ),
			);
		}
		return $out;
	}
}
if ( ! function_exists( 'nadlan_rr_norm_apartment' ) ) {
	/** Adds the Pro fields to a stored apartment without changing what is there (legacy rows have none of them). */
	function nadlan_rr_norm_apartment( $a, $first_building = 'b1', $upf = 1 ) {
		if ( ! is_array( $a ) ) { return null; }
		$a['building'] = ! empty( $a['building'] ) ? sanitize_key( $a['building'] ) : $first_building;
		if ( empty( $a['num'] ) ) {
			$m = array();
			$a['num'] = preg_match( '/(\d+)/', (string) ( $a['label'] ?? '' ), $m ) ? (int) $m[1] : ( (int) ( $a['floor'] ?? 1 ) - 1 ) * max( 1, (int) $upf ) + (int) ( $a['pos'] ?? 0 ) + 1;
		}
		$a['num']          = (int) $a['num'];
		$a['owners']       = isset( $a['owners'] ) && is_array( $a['owners'] ) ? array_values( $a['owners'] ) : array();
		$a['common_share'] = (string) ( $a['common_share'] ?? '' );
		$a['v']            = (int) ( $a['v'] ?? 0 );
		$a['docs']         = isset( $a['docs'] ) && is_array( $a['docs'] ) ? $a['docs'] : array();
		foreach ( array( 'contact_note', 'note', 'label' ) as $k ) { $a[ $k ] = (string) ( $a[ $k ] ?? '' ); }
		$a['consent_status'] = (string) ( $a['consent_status'] ?? 'unreached' );
		return $a;
	}
}
if ( ! function_exists( 'nadlan_rr_apartments' ) ) {
	function nadlan_rr_apartments( $id, $raw_json = null ) {
		$raw = null === $raw_json ? json_decode( (string) get_post_meta( $id, 'renewal_apartments', true ), true ) : json_decode( (string) $raw_json, true );
		$raw = is_array( $raw ) ? $raw : array();
		$b = nadlan_rr_buildings( $id );
		$first = $b[0]['key'];
		$upf = array();
		foreach ( $b as $x ) { $upf[ $x['key'] ] = $x['upf']; }
		$out = array();
		foreach ( $raw as $a ) {
			$bk = ! empty( $a['building'] ) ? sanitize_key( $a['building'] ) : $first;
			$n = nadlan_rr_norm_apartment( $a, $first, $upf[ $bk ] ?? 1 );
			if ( $n ) { $out[] = $n; }
		}
		return $out;
	}
}

/* ---------- owners, shares, the careful count ---------- */
if ( ! function_exists( 'nadlan_rr_clean_owners' ) ) {
	function nadlan_rr_clean_owners( $raw ) {
		$out = array();
		foreach ( (array) $raw as $o ) {
			if ( ! is_array( $o ) ) { continue; }
			$n = mb_substr( trim( sanitize_text_field( (string) ( $o['n'] ?? '' ) ) ), 0, 40 );
			if ( '' === $n ) { continue; }
			$share = preg_replace( '/[^0-9\/\.%]/', '', (string) ( $o['share'] ?? '' ) );
			$out[] = array( 'n' => $n, 'share' => mb_substr( $share, 0, 12 ), 'heir' => ! empty( $o['heir'] ), 'signed' => ! empty( $o['signed'] ) );
			if ( count( $out ) >= 8 ) { break; }
		}
		return $out;
	}
}
if ( ! function_exists( 'nadlan_rr_share_val' ) ) {
	/** "28/1000" -> 0.028, "2.8%" -> 0.028, "0.028" -> 0.028; anything else -> null. */
	function nadlan_rr_share_val( $s ) {
		$s = trim( (string) $s );
		if ( '' === $s ) { return null; }
		$m = array();
		if ( preg_match( '/^(\d+(?:\.\d+)?)\s*\/\s*(\d+(?:\.\d+)?)$/', $s, $m ) ) { return (float) $m[2] > 0 ? (float) $m[1] / (float) $m[2] : null; }
		if ( preg_match( '/^(\d+(?:\.\d+)?)\s*%$/', $s, $m ) ) { return (float) $m[1] / 100; }
		if ( preg_match( '/^\d+(?:\.\d+)?$/', $s ) ) { $v = (float) $s; return $v <= 1 ? $v : null; }
		return null;
	}
}
if ( ! function_exists( 'nadlan_rr_counted' ) ) {
	/** Counts as signed: status "consented" AND every listed owner signed (no owners listed: the status alone). */
	function nadlan_rr_counted( $a ) {
		if ( 'consented' !== ( $a['consent_status'] ?? '' ) ) { return false; }
		foreach ( (array) ( $a['owners'] ?? array() ) as $o ) { if ( empty( $o['signed'] ) ) { return false; } }
		return true;
	}
}
if ( ! function_exists( 'nadlan_rr_shown_status' ) ) {
	/** The status painted on the facade: "partial" = marked signed but an owner has not signed yet. */
	function nadlan_rr_shown_status( $a ) {
		$s = (string) ( $a['consent_status'] ?? 'unreached' );
		return ( 'consented' === $s && ! nadlan_rr_counted( $a ) ) ? 'partial' : $s;
	}
}
if ( ! function_exists( 'nadlan_rr_counts' ) ) {
	function nadlan_rr_counts( $apts ) {
		$c = array( 'consented' => 0, 'partial' => 0, 'in_process' => 0, 'missing_docs' => 0, 'refused' => 0, 'unreached' => 0, 'total' => 0, 'yes' => 0, 'docs_missing_apts' => 0 );
		$keys = array_keys( nadlan_ur_doc_keys() );
		foreach ( $apts as $a ) {
			$s = nadlan_rr_shown_status( $a );
			if ( ! isset( $c[ $s ] ) ) { $s = 'unreached'; }
			$c[ $s ]++;
			$c['total']++;
			if ( nadlan_rr_counted( $a ) ) { $c['yes']++; }
			if ( ! in_array( $a['consent_status'], array( 'refused', 'unreached' ), true ) ) {
				foreach ( $keys as $k ) { if ( empty( $a['docs'][ $k ] ) ) { $c['docs_missing_apts']++; break; } }
			}
		}
		$c['pct'] = $c['total'] ? round( $c['yes'] / $c['total'] * 100, 1 ) : 0;
		return $c;
	}
}
if ( ! function_exists( 'nadlan_rr_docs_rollup' ) ) {
	/** Per document: how many of the apartments in contact (not unreached) have it ticked. */
	function nadlan_rr_docs_rollup( $apts ) {
		$keys = array_keys( nadlan_ur_doc_keys() );
		$per = array_fill_keys( $keys, 0 );
		$base = 0;
		foreach ( $apts as $a ) {
			if ( 'unreached' === $a['consent_status'] ) { continue; }
			$base++;
			foreach ( $keys as $k ) { if ( ! empty( $a['docs'][ $k ] ) ) { $per[ $k ]++; } }
		}
		return array( 'per' => $per, 'base' => $base );
	}
}

/* ---------- the statutory special majority (pinui-binui), per complex and per building ---------- */
if ( ! function_exists( 'nadlan_rr_law' ) ) {
	function nadlan_rr_law( $apts, $buildings, $track ) {
		$t = function_exists( 'nadlan_ur_thresholds' ) ? nadlan_ur_thresholds() : array( 'majority_num' => 2, 'majority_den' => 3, 'building_num' => 3, 'building_den' => 5, 'source' => '', 'checked' => '' );
		$num = (int) $t['majority_num']; $den = (int) $t['majority_den'];
		$bn = (int) $t['building_num']; $bd = (int) $t['building_den'];
		$total = count( $apts );
		$yes = 0;
		foreach ( $apts as $a ) { if ( nadlan_rr_counted( $a ) ) { $yes++; } }
		$need = $total ? (int) ceil( $num * $total / $den ) : 0; // exact fraction: 50 apartments need 34, 48 need 32
		$out = array(
			'applies' => 'pinui_binui' === $track,
			'complex' => array( 'total' => $total, 'yes' => $yes, 'need' => $need, 'short' => max( 0, $need - $yes ), 'met' => $total > 0 && $yes * $den >= $num * $total ),
			'buildings' => array(),
			'all_met' => null,
			'checked' => (string) ( $t['checked'] ?? '' ),
		);
		$known_all = true; $met_all = $out['complex']['met'];
		foreach ( $buildings as $b ) {
			$list = array_values( array_filter( $apts, function ( $a ) use ( $b ) { return $a['building'] === $b['key']; } ) );
			$n = count( $list ); $y = 0; $owners = array(); $no_owner_info = false; $shares_known = 0; $share_all = 0.0; $share_yes = 0.0;
			foreach ( $list as $a ) {
				$c = nadlan_rr_counted( $a );
				if ( $c ) {
					$y++;
					if ( ! $a['owners'] ) { $no_owner_info = true; }
					foreach ( (array) $a['owners'] as $o ) { $owners[ mb_strtolower( trim( (string) $o['n'] ) ) ] = 1; }
				}
				$sv = nadlan_rr_share_val( $a['common_share'] );
				if ( null !== $sv ) { $shares_known++; $share_all += $sv; if ( $c ) { $share_yes += $sv; } }
			}
			$row = array( 'key' => $b['key'], 'label' => $b['label'], 'address' => $b['address'], 'total' => $n, 'yes' => $y, 'rule' => 'three_fifths', 'need' => null, 'short' => null, 'met' => null, 'owners_rule' => null );
			if ( $n >= 6 ) {
				$row['need'] = (int) ceil( $bn * $n / $bd );
				$row['met'] = $y * $bd >= $bn * $n;
			} elseif ( $n >= 4 ) {
				// a building of 4 or 5 apartments: at least 3 apartments, and more than two owners among them
				$row['rule'] = 'small_building';
				$row['need'] = 3;
				$distinct = count( $owners );
				if ( $y < 3 ) {
					$row['owners_rule'] = null; $row['met'] = false;
				} elseif ( $distinct > 2 ) {
					$row['owners_rule'] = true; $row['met'] = true;
				} elseif ( $no_owner_info ) {
					$row['owners_rule'] = null; $row['met'] = null; // an apartment without owners entered: the room cannot tell
				} else {
					$row['owners_rule'] = false; $row['met'] = false;
				}
			} else {
				$row['rule'] = 'not_computed'; // fewer than 4 apartments: the room does not compute it, the lawyer does
			}
			if ( null !== $row['need'] ) { $row['short'] = max( 0, $row['need'] - $y ); }
			$row['common'] = array(
				'known'   => $n > 0 && $shares_known === $n,
				'missing' => $n - $shares_known,
				'pct_yes' => $share_all > 0 ? round( $share_yes / $share_all * 100, 1 ) : null,
				'met'     => ( $n > 0 && $shares_known === $n && $share_all > 0 ) ? ( $share_yes / $share_all > 0.5 ) : null,
			);
			if ( null === $row['met'] || null === $row['common']['met'] ) { $known_all = false; }
			if ( false === $row['met'] || false === $row['common']['met'] ) { $met_all = false; }
			$out['buildings'][] = $row;
		}
		$out['all_met'] = $met_all ? ( $known_all ? true : null ) : false;
		return $out;
	}
}

/* ---------- roles ---------- */
if ( ! function_exists( 'nadlan_rr_member_of' ) ) {
	/** The member record of a user in a room (matched by email, as the live join flow stores it), or null. */
	function nadlan_rr_member_of( $id, $uid ) {
		$u = get_userdata( (int) $uid );
		if ( ! $u || empty( $u->user_email ) ) { return null; }
		foreach ( nadlan_ur_members( $id ) as $i => $m ) {
			if ( isset( $m['email'] ) && strtolower( $m['email'] ) === strtolower( $u->user_email ) ) { $m['_i'] = $i; return $m; }
		}
		return null;
	}
}
if ( ! function_exists( 'nadlan_rr_role' ) ) {
	function nadlan_rr_role( $id, $uid = null ) {
		$uid = null === $uid ? get_current_user_id() : (int) $uid;
		if ( $uid <= 0 ) { return ''; }
		if ( user_can( $uid, 'manage_options' ) ) { return 'admin'; }
		if ( (int) get_post_meta( $id, 'owner_user_id', true ) === $uid ) { return 'owner'; }
		$org = (int) get_post_meta( $id, 'org_id', true );
		if ( $org && function_exists( 'nadlan_rr_org_staff_role' ) && nadlan_rr_org_staff_role( $org, $uid ) ) { return 'org'; }
		$m = nadlan_rr_member_of( $id, $uid );
		if ( $m ) { return ( 'committee' === ( $m['role'] ?? '' ) ) ? 'committee' : 'neighbor'; }
		return '';
	}
}
if ( ! function_exists( 'nadlan_rr_is_manager' ) ) {
	function nadlan_rr_is_manager( $role ) { return in_array( $role, array( 'admin', 'owner', 'org' ), true ); }
}
if ( ! function_exists( 'nadlan_rr_room_active' ) ) {
	/** An organizer room whose account lapsed turns read-only (billing is off by default, so this is true). */
	function nadlan_rr_room_active( $id ) {
		$org = (int) get_post_meta( $id, 'org_id', true );
		if ( ! $org || ! function_exists( 'nadlan_rr_org_active' ) ) { return true; }
		return nadlan_rr_org_active( $org );
	}
}
if ( ! function_exists( 'nadlan_rr_neighbor_grid' ) ) {
	function nadlan_rr_neighbor_grid( $id ) {
		$g = (string) get_post_meta( $id, 'neighbor_grid', true );
		if ( in_array( $g, array( 'statuses', 'totals' ), true ) ) { return $g; }
		return (int) get_post_meta( $id, 'org_id', true ) ? 'totals' : 'statuses';
	}
}

/* ---------- the change log (append-only rows) ---------- */
if ( ! function_exists( 'nadlan_rr_log_event' ) ) {
	function nadlan_rr_log_event( $id, $apt, $field, $from, $to, $v = 0 ) {
		$u = wp_get_current_user();
		$ev = array(
			'apt'  => (string) $apt,
			'at'   => current_time( 'mysql' ),
			'by'   => (int) get_current_user_id(),
			'who'  => ( $u && $u->exists() ) ? mb_substr( (string) $u->display_name, 0, 60 ) : '',
			'role' => nadlan_rr_role( $id ),
			'f'    => (string) $field,
			'from' => $from,
			'to'   => $to,
			'v'    => (int) $v,
		);
		add_post_meta( $id, 'renewal_apt_event', wp_slash( wp_json_encode( $ev, JSON_UNESCAPED_UNICODE ) ), false );
		return $ev;
	}
}
if ( ! function_exists( 'nadlan_rr_events' ) ) {
	/** Newest first. $apt null = the whole room. */
	function nadlan_rr_events( $id, $apt = null, $limit = 60 ) {
		$rows = get_post_meta( $id, 'renewal_apt_event', false );
		$out = array();
		foreach ( (array) $rows as $r ) {
			$e = is_array( $r ) ? $r : json_decode( (string) $r, true );
			if ( ! is_array( $e ) ) { continue; }
			if ( null !== $apt && (string) ( $e['apt'] ?? '' ) !== (string) $apt ) { continue; }
			$out[] = $e;
		}
		$out = array_reverse( $out );
		return array_slice( $out, 0, max( 1, (int) $limit ) );
	}
}

/* ---------- compare-and-swap on one meta row (the room's apartments JSON) ---------- */
if ( ! function_exists( 'nadlan_rr_meta_raw' ) ) {
	/** The stored value straight from the table (no object cache), or null when there is no row. */
	function nadlan_rr_meta_raw( $id, $key ) {
		global $wpdb;
		$v = $wpdb->get_var( $wpdb->prepare( "SELECT meta_value FROM {$wpdb->postmeta} WHERE post_id = %d AND meta_key = %s ORDER BY meta_id ASC LIMIT 1", (int) $id, (string) $key ) );
		return null === $v ? null : (string) $v;
	}
}
if ( ! function_exists( 'nadlan_rr_meta_cas' ) ) {
	/** Writes $new only if the row still holds $old (compared by MD5, exact bytes). True on success. */
	function nadlan_rr_meta_cas( $id, $key, $old, $new ) {
		global $wpdb;
		if ( null === $old ) { return (bool) add_post_meta( $id, $key, wp_slash( $new ), true ); }
		if ( $old === $new ) { return true; }
		$n = $wpdb->query( $wpdb->prepare( "UPDATE {$wpdb->postmeta} SET meta_value = %s WHERE post_id = %d AND meta_key = %s AND MD5(meta_value) = %s", (string) $new, (int) $id, (string) $key, md5( (string) $old ) ) );
		wp_cache_delete( (int) $id, 'post_meta' );
		return 1 === (int) $n;
	}
}

/* ---------- one apartment per save ---------- */
if ( ! function_exists( 'nadlan_rr_apply_patch' ) ) {
	/** Returns array( new apartment, list of changes ). Only keys present in $patch are touched. */
	function nadlan_rr_apply_patch( $cur, $patch ) {
		$new = $cur; $ch = array();
		$statuses = array_keys( nadlan_ur_consent_statuses() );
		if ( isset( $patch['consent_status'] ) && in_array( $patch['consent_status'], $statuses, true ) && $patch['consent_status'] !== $cur['consent_status'] ) {
			$ch[] = array( 'status', $cur['consent_status'], $patch['consent_status'] );
			$new['consent_status'] = $patch['consent_status'];
		}
		if ( isset( $patch['docs'] ) && is_array( $patch['docs'] ) ) {
			foreach ( array_keys( nadlan_ur_doc_keys() ) as $k ) {
				if ( ! array_key_exists( $k, $patch['docs'] ) ) { continue; }
				$was = ! empty( $cur['docs'][ $k ] ); $now = ! empty( $patch['docs'][ $k ] );
				if ( $was !== $now ) { $ch[] = array( 'doc:' . $k, $was, $now ); }
				$new['docs'][ $k ] = $now;
			}
		}
		if ( isset( $patch['note'] ) ) {
			$v = mb_substr( sanitize_text_field( (string) $patch['note'] ), 0, 400 );
			if ( $v !== $cur['note'] ) { $ch[] = array( 'note', null, null ); $new['note'] = $v; }
		}
		if ( isset( $patch['contact_note'] ) ) {
			$v = mb_substr( sanitize_text_field( (string) $patch['contact_note'] ), 0, 200 );
			if ( $v !== $cur['contact_note'] ) { $ch[] = array( 'contact', null, null ); $new['contact_note'] = $v; }
		}
		if ( isset( $patch['owners'] ) ) {
			$o = nadlan_rr_clean_owners( $patch['owners'] );
			if ( wp_json_encode( $o ) !== wp_json_encode( $cur['owners'] ) ) {
				$sig = function ( $l ) { $s = 0; foreach ( $l as $x ) { if ( ! empty( $x['signed'] ) ) { $s++; } } return array( 'n' => count( $l ), 'signed' => $s ); };
				$ch[] = array( 'owners', $sig( $cur['owners'] ), $sig( $o ) );
				$new['owners'] = $o;
			}
		}
		if ( isset( $patch['common_share'] ) ) {
			$v = mb_substr( preg_replace( '/[^0-9\/\.%]/', '', (string) $patch['common_share'] ), 0, 16 );
			if ( $v !== $cur['common_share'] ) { $ch[] = array( 'common', $cur['common_share'], $v ); $new['common_share'] = $v; }
		}
		return array( $new, $ch );
	}
}
if ( ! function_exists( 'nadlan_rr_save_apartment' ) ) {
	/**
	 * @return array ok(bool), code(saved|unchanged|conflict|not_found|busy), apartment, changes
	 */
	function nadlan_rr_save_apartment( $id, $apt_id, $patch, $client_v ) {
		$apt_id = sanitize_key( (string) $apt_id );
		for ( $try = 0; $try < 5; $try++ ) {
			$raw = nadlan_rr_meta_raw( $id, 'renewal_apartments' );
			$stored = json_decode( (string) $raw, true );
			$stored = is_array( $stored ) ? $stored : array();
			$idx = null;
			foreach ( $stored as $i => $a ) { if ( isset( $a['id'] ) && (string) $a['id'] === $apt_id ) { $idx = $i; break; } }
			if ( null === $idx ) { return array( 'ok' => false, 'code' => 'not_found' ); }
			$norm = nadlan_rr_apartments( $id, wp_json_encode( array( $stored[ $idx ] ) ) );
			$cur = $norm[0];
			if ( (int) $cur['v'] !== (int) $client_v ) {
				return array( 'ok' => false, 'code' => 'conflict', 'apartment' => $cur, 'last' => nadlan_rr_events( $id, $apt_id, 1 ) );
			}
			list( $new, $changes ) = nadlan_rr_apply_patch( $cur, (array) $patch );
			if ( ! $changes ) { return array( 'ok' => true, 'code' => 'unchanged', 'apartment' => $cur, 'changes' => array() ); }
			$new['v'] = (int) $cur['v'] + 1;
			$new['updated'] = current_time( 'mysql' );
			$new['updated_by'] = (int) get_current_user_id();
			$stored[ $idx ] = $new;
			$json = wp_json_encode( array_values( $stored ), JSON_UNESCAPED_UNICODE );
			if ( nadlan_rr_meta_cas( $id, 'renewal_apartments', $raw, $json ) ) {
				foreach ( $changes as $c ) { nadlan_rr_log_event( $id, $apt_id, $c[0], $c[1], $c[2], $new['v'] ); }
				update_post_meta( $id, 'renewal_last_activity', current_time( 'mysql' ) );
				return array( 'ok' => true, 'code' => 'saved', 'apartment' => $new, 'changes' => $changes );
			}
			// somebody wrote between our read and our write: read again. Their change to ANOTHER apartment is kept
			// (we re-apply our one-apartment patch on top); their change to THIS apartment bumps v -> conflict above.
		}
		return array( 'ok' => false, 'code' => 'busy' );
	}
}

/* ---------- deadlines (entered by people, counted by the room) ---------- */
if ( ! function_exists( 'nadlan_rr_deadlines' ) ) {
	function nadlan_rr_deadlines( $id ) {
		$out = array();
		foreach ( nadlan_rr_json( $id, 'renewal_deadlines' ) as $d ) {
			if ( empty( $d['id'] ) || empty( $d['date'] ) ) { continue; }
			$d['days'] = nadlan_rr_days_until( $d['date'] );
			$out[] = $d;
		}
		usort( $out, function ( $a, $b ) { return strcmp( $a['date'], $b['date'] ); } );
		return $out;
	}
}

/* ---------- the role-filtered payload ---------- */
if ( ! function_exists( 'nadlan_rr_filter_payload' ) ) {
	function nadlan_rr_filter_payload( $p, $role, $id ) {
		$mgr    = nadlan_rr_is_manager( $role );
		$active = nadlan_rr_room_active( $id );
		$grid   = nadlan_rr_neighbor_grid( $id );
		$p['role'] = $role ? $role : 'none';
		$p['caps'] = array(
			'manage'       => $mgr && $active,
			'post_updates' => ( $mgr && $active ) || 'committee' === $role,
			'see_grid'     => $mgr || in_array( $role, array( 'committee', 'demo' ), true ) || ( 'neighbor' === $role && 'statuses' === $grid ),
			'private'      => $mgr,
			'claim'        => in_array( $role, array( 'neighbor', 'committee' ), true ),
			'read_only'    => $mgr && ! $active,
		);
		$p['can_manage'] = $p['caps']['manage']; // the live key, kept for the cached old script
		$p['settings'] = array( 'neighbor_grid' => $grid );
		if ( $mgr ) {
			$p['members'] = array_map( function ( $m ) { unset( $m['_i'] ); return $m; }, nadlan_ur_members( $id ) );
			$p['events_recent'] = nadlan_rr_events( $id, null, 40 );
			$tok = (string) get_post_meta( $id, 'invite_token', true );
			$p['join_url'] = $tok ? home_url( '/my-renewal/?join=' . rawurlencode( $tok ) ) : '';
			return $p;
		}
		// everybody else: no names, no notes, no contact notes, no shares, no versions, no user ids
		$keep = array( 'id', 'building', 'floor', 'pos', 'dir', 'num', 'label', 'consent_status' );
		$docs_too = in_array( $role, array( 'committee', 'demo' ), true );
		$mine = array(); $claim = null;
		if ( in_array( $role, array( 'neighbor', 'committee' ), true ) ) {
			$m = nadlan_rr_member_of( $id, get_current_user_id() );
			if ( $m && ! empty( $m['claim_apt'] ) ) {
				$claim = array( 'apt' => (string) $m['claim_apt'], 'state' => ! empty( $m['approved'] ) ? 'approved' : ( ! empty( $m['rejected'] ) ? 'rejected' : 'pending' ) );
			}
		}
		$apts = array();
		foreach ( (array) $p['apartments'] as $a ) {
			if ( $claim && 'approved' === $claim['state'] && (string) $a['id'] === $claim['apt'] ) {
				$signed = 0;
				foreach ( (array) $a['owners'] as $o ) { if ( ! empty( $o['signed'] ) ) { $signed++; } }
				$mine[] = array(
					'id' => $a['id'], 'building' => $a['building'], 'num' => $a['num'], 'floor' => $a['floor'], 'label' => $a['label'],
					'consent_status' => $a['consent_status'], 'shown' => nadlan_rr_shown_status( $a ), 'docs' => $a['docs'],
					'owners_n' => count( (array) $a['owners'] ), 'owners_signed' => $signed,
				);
			}
			if ( $p['caps']['see_grid'] ) {
				$row = array_intersect_key( $a, array_flip( $keep ) );
				$row['shown'] = nadlan_rr_shown_status( $a );
				if ( $docs_too ) { $row['docs'] = $a['docs']; }
				$apts[] = $row;
			}
		}
		$p['apartments'] = $apts;
		$p['mine'] = $mine;
		$p['my_claim'] = $claim;
		// the claim picker needs the apartment numbers per building, never their status
		$p['claim_options'] = array();
		if ( $p['caps']['claim'] ) {
			foreach ( nadlan_rr_buildings( $id ) as $b ) {
				$p['claim_options'][ $b['key'] ] = array();
			}
			foreach ( nadlan_rr_apartments( $id ) as $a ) { $p['claim_options'][ $a['building'] ][] = array( 'id' => $a['id'], 'num' => $a['num'], 'floor' => $a['floor'] ); }
		}
		if ( 'committee' !== $role ) { unset( $p['deadlines'] ); }
		unset( $p['members'], $p['events_recent'], $p['join_url'] );
		$p['updates'] = array_map( function ( $u ) { unset( $u['by'], $u['by_name'] ); return $u; }, (array) $p['updates'] );
		$p['stage_log'] = array_map( function ( $l ) { unset( $l['by'] ); return $l; }, (array) $p['stage_log'] );
		return $p;
	}
}

/* ---------- REST (the new routes; the live ones stay in urban-space.php) ---------- */
add_action( 'rest_api_init', function () {
	$mng = function ( $req ) { return is_user_logged_in() && nadlan_ur_space_on() && nadlan_ur_space_ok( (int) $req['id'] ) && nadlan_ur_can_manage( (int) $req['id'] ); };
	$view = function ( $req ) { return is_user_logged_in() && nadlan_ur_space_on() && nadlan_ur_space_ok( (int) $req['id'] ) && nadlan_ur_can_view( (int) $req['id'] ); };

	/* one apartment, with its version; 409 when somebody saved the same apartment first */
	register_rest_route( 'nadlan/v1', '/renewal-space/(?P<id>\d+)/apartment/(?P<apt>[a-z0-9_-]{1,40})', array(
		'methods' => 'POST', 'permission_callback' => $mng,
		'callback' => function ( WP_REST_Request $req ) {
			$id = (int) $req['id'];
			if ( function_exists( 'nadlan_ur_rate_limited' ) && nadlan_ur_rate_limited( 'aptsave', 1500, HOUR_IN_SECONDS ) ) {
				return new WP_Error( 'rate_limited', 'too many saves', array( 'status' => 429 ) );
			}
			$patch = array();
			foreach ( array( 'consent_status', 'docs', 'note', 'contact_note', 'owners', 'common_share' ) as $k ) {
				$v = $req->get_param( $k );
				if ( null !== $v ) { $patch[ $k ] = $v; }
			}
			$r = nadlan_rr_save_apartment( $id, (string) $req['apt'], $patch, (int) $req->get_param( 'v' ) );
			if ( ! $r['ok'] ) {
				$status = 'conflict' === $r['code'] ? 409 : ( 'not_found' === $r['code'] ? 404 : 503 );
				return new WP_Error( $r['code'], $r['code'], array( 'status' => $status, 'apartment' => $r['apartment'] ?? null, 'last' => $r['last'] ?? array() ) );
			}
			$apts = nadlan_rr_apartments( $id );
			$b = nadlan_rr_buildings( $id );
			return array(
				'ok' => true, 'code' => $r['code'], 'apartment' => $r['apartment'],
				'counts' => nadlan_rr_counts( $apts ),
				'law' => nadlan_rr_law( $apts, $b, (string) get_post_meta( $id, 'track', true ) ),
				'docs_rollup' => nadlan_rr_docs_rollup( $apts ),
				'events' => nadlan_rr_events( $id, (string) $req['apt'], 30 ),
			);
		},
	) );

	register_rest_route( 'nadlan/v1', '/renewal-space/(?P<id>\d+)/apartment/(?P<apt>[a-z0-9_-]{1,40})/log', array(
		'methods' => 'GET', 'permission_callback' => $mng,
		'callback' => function ( $req ) { return array( 'events' => nadlan_rr_events( (int) $req['id'], sanitize_key( (string) $req['apt'] ), 200 ) ); },
	) );

	/* a neighbour says which apartment is theirs; a manager approves it (or the room auto-approves, an option, off) */
	register_rest_route( 'nadlan/v1', '/renewal-space/(?P<id>\d+)/claim', array(
		'methods' => 'POST', 'permission_callback' => $view,
		'callback' => function ( WP_REST_Request $req ) {
			$id = (int) $req['id'];
			$m = nadlan_rr_member_of( $id, get_current_user_id() );
			if ( ! $m ) { return new WP_Error( 'not_member', 'not a member', array( 'status' => 403 ) ); }
			$apt = sanitize_key( (string) $req->get_param( 'apt' ) );
			$ok = false;
			foreach ( nadlan_rr_apartments( $id ) as $a ) { if ( $a['id'] === $apt ) { $ok = true; break; } }
			if ( ! $ok ) { return new WP_Error( 'bad_apt', 'no such apartment', array( 'status' => 400 ) ); }
			$members = nadlan_ur_members( $id );
			$i = $m['_i'];
			$members[ $i ]['claim_apt'] = $apt;
			$members[ $i ]['claim_at'] = current_time( 'mysql' );
			$members[ $i ]['approved'] = '1' === (string) get_option( 'nadlan_rr_claim_autoapprove', '0' );
			unset( $members[ $i ]['rejected'] );
			nadlan_rr_put_json( $id, 'member_emails', $members );
			return nadlan_ur_space_payload( $id, nadlan_ur_req_lang( (string) $req->get_param( 'lang' ) ) );
		},
	) );

	/* managers: approve or reject a claim, make a member committee or neighbour, or remove them */
	register_rest_route( 'nadlan/v1', '/renewal-space/(?P<id>\d+)/member', array(
		'methods' => 'POST', 'permission_callback' => $mng,
		'callback' => function ( WP_REST_Request $req ) {
			$id = (int) $req['id'];
			$email = strtolower( sanitize_email( (string) $req->get_param( 'email' ) ) );
			$act = sanitize_key( (string) $req->get_param( 'action' ) );
			$members = nadlan_ur_members( $id ); $hit = null;
			foreach ( $members as $i => $m ) { if ( strtolower( $m['email'] ?? '' ) === $email ) { $hit = $i; break; } }
			if ( null === $hit ) { return new WP_Error( 'not_found', 'no such member', array( 'status' => 404 ) ); }
			$apt = (string) ( $members[ $hit ]['claim_apt'] ?? '' );
			if ( 'approve' === $act && $apt ) {
				$members[ $hit ]['approved'] = true; unset( $members[ $hit ]['rejected'] );
				$members[ $hit ]['approved_by'] = get_current_user_id(); $members[ $hit ]['approved_at'] = current_time( 'mysql' );
				nadlan_rr_log_event( $id, $apt, 'claim', null, 'approved' );
			} elseif ( 'reject' === $act ) {
				$members[ $hit ]['approved'] = false; $members[ $hit ]['rejected'] = true;
				if ( $apt ) { nadlan_rr_log_event( $id, $apt, 'claim', null, 'rejected' ); }
			} elseif ( in_array( $act, array( 'committee', 'neighbor' ), true ) ) {
				$members[ $hit ]['role'] = $act;
			} elseif ( 'remove' === $act ) {
				array_splice( $members, $hit, 1 );
			} else {
				return new WP_Error( 'bad_action', 'unknown action', array( 'status' => 400 ) );
			}
			nadlan_rr_put_json( $id, 'member_emails', array_values( $members ) );
			return nadlan_ur_space_payload( $id, nadlan_ur_req_lang( (string) $req->get_param( 'lang' ) ) );
		},
	) );

	/* deadlines: add or remove a dated item */
	register_rest_route( 'nadlan/v1', '/renewal-space/(?P<id>\d+)/deadline', array(
		'methods' => 'POST', 'permission_callback' => $mng,
		'callback' => function ( WP_REST_Request $req ) {
			$id = (int) $req['id'];
			$list = nadlan_rr_json( $id, 'renewal_deadlines' );
			if ( 'remove' === sanitize_key( (string) $req->get_param( 'action' ) ) ) {
				$did = sanitize_key( (string) $req->get_param( 'did' ) );
				$list = array_values( array_filter( $list, function ( $d ) use ( $did ) { return ( $d['id'] ?? '' ) !== $did; } ) );
			} else {
				$label = mb_substr( sanitize_text_field( (string) $req->get_param( 'label' ) ), 0, 80 );
				$date = (string) $req->get_param( 'date' );
				if ( '' === $label || ! preg_match( '/^\d{4}-\d{2}-\d{2}$/', $date ) ) { return new WP_Error( 'bad_request', 'label and date', array( 'status' => 400 ) ); }
				if ( count( $list ) >= 30 ) { return new WP_Error( 'too_many', 'up to 30', array( 'status' => 400 ) ); }
				$list[] = array( 'id' => strtolower( wp_generate_password( 8, false, false ) ), 'label' => $label, 'date' => $date,
					'note' => mb_substr( sanitize_text_field( (string) $req->get_param( 'note' ) ), 0, 160 ), 'by' => get_current_user_id(), 'at' => current_time( 'mysql' ) );
			}
			nadlan_rr_put_json( $id, 'renewal_deadlines', $list );
			return nadlan_ur_space_payload( $id, nadlan_ur_req_lang( (string) $req->get_param( 'lang' ) ) );
		},
	) );

	/* room settings a manager can change */
	register_rest_route( 'nadlan/v1', '/renewal-space/(?P<id>\d+)/settings', array(
		'methods' => 'POST', 'permission_callback' => $mng,
		'callback' => function ( WP_REST_Request $req ) {
			$id = (int) $req['id'];
			$g = (string) $req->get_param( 'neighbor_grid' );
			if ( in_array( $g, array( 'statuses', 'totals' ), true ) ) { update_post_meta( $id, 'neighbor_grid', $g ); }
			return nadlan_ur_space_payload( $id, nadlan_ur_req_lang( (string) $req->get_param( 'lang' ) ) );
		},
	) );
} );

if ( ! defined( 'NADLAN_RR_LOADED' ) ) { define( 'NADLAN_RR_LOADED', '1' ); }
if ( file_exists( __DIR__ . '/renewal-org.php' ) ) { require_once __DIR__ . '/renewal-org.php'; }
