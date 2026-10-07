<?php
/**
 * nadlan-config - RENTALS v2: the money engine (HAD-383, 3.10.2026).
 *
 * The one place where shekels are computed. Every number the landlord, the
 * tenant portal and the reports show comes from here, over the FULL history
 * of a lease (never a truncated window), in agorot (integers, no floats in
 * the books). The browser has a line-by-line twin (rm-core.js N.mx) for the
 * sample account; scripts/rentals/sim proves both agree for 10 years.
 *
 * The books (table nlrm_ledger) are append-only:
 *  - a line is never deleted and its amount, kind and lease never change;
 *  - a mistake is voided (status 'void') and recorded again;
 *  - every money write carries a durable key (auto_key, UNIQUE per owner):
 *    'rent:L:Y-m' for a rent period, 'cref:...' for a user action, so a
 *    retry, a double tap or two tabs never write the same money twice.
 *
 * Kinds:  charge  - the tenant owes (rent, utilities, a bounced-cheque fee);
 *         payment - money from the tenant (or the deposit applied, method
 *                   'deposit'; or a write-off, method 'writeoff');
 *                   category 'deposit' = a security deposit received (held,
 *                   not income);
 *         refund  - money back to the tenant (category 'deposit' = the
 *                   deposit returned, §25י(ה): within 60 days);
 *         expense / income - the landlord's own books (no tenant balance).
 *
 * Statuses of a charge (open / partial / paid) are DERIVED, first in first
 * out, from the credits of its lease; the stored status matters only for
 * 'void'. A payment is 'paid', 'pending' (a post-dated cheque, a tenant's
 * report), 'deposited' (a cheque), 'bounced' or 'void'.
 */

if ( ! defined( 'ABSPATH' ) ) { exit; }

/* ---------- the clock (one source, so a test can move time) ---------- */
if ( ! function_exists( 'nlrm_time' ) ) {
	function nlrm_time() { return (int) apply_filters( 'nlrm_time', time() ); }
}
if ( ! function_exists( 'nlrm_today' ) ) {
	/* the landlord's calendar day, in Israel */
	function nlrm_today() {
		try {
			$d = new DateTime( '@' . nlrm_time() );
			$d->setTimezone( new DateTimeZone( 'Asia/Jerusalem' ) );
			return $d->format( 'Y-m-d' );
		} catch ( Exception $e ) {
			return gmdate( 'Y-m-d', nlrm_time() );
		}
	}
}

/* ---------- calendar arithmetic on Y-m-d strings (no time zones) ---------- */
if ( ! function_exists( 'nlrm_dim' ) ) {
	function nlrm_dim( $y, $m ) { return (int) gmdate( 't', gmmktime( 0, 0, 0, (int) $m, 1, (int) $y ) ); }
}
if ( ! function_exists( 'nlrm_add_months' ) ) {
	/* same day n months later, clamped to the month's last day (31.1 + 1 = 28/29.2);
	   always counted from the given date, never chained, so 31.1 + 2 = 31.3 */
	function nlrm_add_months( $iso, $n ) {
		$y = (int) substr( $iso, 0, 4 ); $m = (int) substr( $iso, 5, 2 ); $d = (int) substr( $iso, 8, 2 );
		$t = $y * 12 + ( $m - 1 ) + (int) $n;
		$y2 = (int) floor( $t / 12 ); $m2 = $t - $y2 * 12 + 1;
		return sprintf( '%04d-%02d-%02d', $y2, $m2, min( $d, nlrm_dim( $y2, $m2 ) ) );
	}
}
if ( ! function_exists( 'nlrm_add_days' ) ) {
	function nlrm_add_days( $iso, $n ) {
		return gmdate( 'Y-m-d', gmmktime( 0, 0, 0, (int) substr( $iso, 5, 2 ), (int) substr( $iso, 8, 2 ) + (int) $n, (int) substr( $iso, 0, 4 ) ) );
	}
}
if ( ! function_exists( 'nlrm_day_diff' ) ) {
	/* $b - $a in days */
	function nlrm_day_diff( $a, $b ) {
		$ta = gmmktime( 0, 0, 0, (int) substr( $a, 5, 2 ), (int) substr( $a, 8, 2 ), (int) substr( $a, 0, 4 ) );
		$tb = gmmktime( 0, 0, 0, (int) substr( $b, 5, 2 ), (int) substr( $b, 8, 2 ), (int) substr( $b, 0, 4 ) );
		return (int) round( ( $tb - $ta ) / 86400 );
	}
}
if ( ! function_exists( 'nlrm_month_end' ) ) {
	function nlrm_month_end( $iso ) { return substr( $iso, 0, 8 ) . sprintf( '%02d', nlrm_dim( substr( $iso, 0, 4 ), substr( $iso, 5, 2 ) ) ); }
}

/* ---------- the rent schedule of a lease ---------- */
if ( ! function_exists( 'nlrm_lease_periods' ) ) {
	/**
	 * The rent periods of a lease whose due date is on or before $horizon.
	 * Period k runs from start + k months (anchored on the start day) to the
	 * day before start + k + 1 months; the last one is cut at the end date
	 * and prorated by days. Rent is due on pay_day of the month in which the
	 * period starts (in advance, the Israeli norm); the first period is never
	 * due before the lease starts. Periods due before terms.track_from are
	 * not the system's business (a lease entered mid-way does not invent
	 * years of arrears).
	 */
	function nlrm_lease_periods( $l, $horizon ) {
		$l = (array) $l;
		$out = array();
		$start = isset( $l['start_date'] ) ? (string) $l['start_date'] : '';
		if ( ! preg_match( '/^\d{4}-\d{2}-\d{2}$/', $start ) ) { return $out; }
		$end = ! empty( $l['end_date'] ) ? (string) $l['end_date'] : '';
		$pd = max( 1, min( 28, (int) ( $l['pay_day'] ?? 1 ) ) );
		$terms = (array) ( $l['terms'] ?? array() );
		$from = ! empty( $terms['track_from'] ) && preg_match( '/^\d{4}-\d{2}-\d{2}$/', (string) $terms['track_from'] ) ? (string) $terms['track_from'] : '';
		for ( $k = 0; $k < 1200; $k++ ) {
			$ps = nlrm_add_months( $start, $k );
			if ( $end && $ps > $end ) { break; }
			/* a lease from the 29th-31st that ends on its anniversary where that day does not
			   exist (29.2.2028 to 28.2.2030): the clamped day closes the last period, no 1-day stub */
			if ( $end && $ps === $end && $k > 0 && (int) substr( $ps, 8 ) < (int) substr( $start, 8 ) ) { break; }
			$next = nlrm_add_months( $start, $k + 1 );
			$due = substr( $ps, 0, 8 ) . sprintf( '%02d', $pd );
			if ( 0 === $k && $due < $start ) { $due = $start; }
			if ( $due > $horizon ) { break; }
			if ( $from && $due < $from ) { continue; }
			$days = nlrm_day_diff( $ps, $next );
			$used = $days;
			if ( $end && $end < nlrm_add_days( $next, -1 ) ) { $used = nlrm_day_diff( $ps, $end ) + 1; }
			$out[] = array( 'k' => $k, 'start' => $ps, 'end' => nlrm_add_days( $next, -1 ), 'due' => $due, 'days' => $days, 'used' => $used, 'key' => 'rent:' . (int) ( $l['id'] ?? 0 ) . ':' . substr( $ps, 0, 7 ) );
		}
		return $out;
	}
}

if ( ! function_exists( 'nlrm_cpi_factor' ) ) {
	/* index factor between two dates: a test or a mirror may answer through the
	   'nlrm_cpi_factor' filter; otherwise the CBS calculator (cached). */
	function nlrm_cpi_factor( $from, $to ) {
		$f = apply_filters( 'nlrm_cpi_factor', null, $from, $to );
		if ( null !== $f ) { return $f; }
		$c = nlrm_cpi_calc( 1000, $from, $to );
		return is_wp_error( $c ) ? $c : (float) $c['factor'];
	}
}

if ( ! function_exists( 'nlrm_period_amount' ) ) {
	/**
	 * Agorot due for period $p of lease $l. Linkage to the CPI (מדד המחירים
	 * לצרכן): every `every` months from the start the rent becomes
	 * rent x (1 + pct x (index factor - 1)) from base_date to the adjustment
	 * date (never compounded, always from the base). With `floor` the rent
	 * never drops below the base when the index falls. If the index is not
	 * available right now the base is charged and the line is marked
	 * 'cpi?...' so a later run posts the exact difference (never silent).
	 * Returns array( amount, note ).
	 */
	function nlrm_period_amount( $l, $p ) {
		$l = (array) $l;
		$base = (int) round( (float) $l['rent'] * 100 );
		$amount = $base;
		$note = '';
		$link = (array) ( $l['linkage'] ?? array() );
		if ( ! empty( $link['mode'] ) && 'cpi' === $link['mode'] ) {
			$every = max( 1, (int) ( $link['every'] ?? 12 ) );
			$step = (int) floor( $p['k'] / $every ) * $every;
			if ( $step > 0 ) {
				$bdate = ! empty( $link['base_date'] ) ? (string) $link['base_date'] : (string) $l['start_date'];
				$adj = nlrm_add_months( (string) $l['start_date'], $step );
				$f = nlrm_cpi_factor( $bdate, $adj );
				if ( is_wp_error( $f ) || ! is_numeric( $f ) || $f <= 0 ) {
					$note = 'cpi?' . $bdate . '>' . $adj;
				} else {
					$pct = max( 0, min( 100, (float) ( $link['pct'] ?? 100 ) ) ) / 100;
					$new = $base * ( 1 + $pct * ( (float) $f - 1 ) );
					if ( ! isset( $link['floor'] ) || $link['floor'] ) { $new = max( $base, $new ); }
					$amount = (int) round( $new );
					$note = 'cpi ' . $bdate . '>' . $adj . ' ' . sprintf( '%+.2f%%', ( (float) $f - 1 ) * 100 );
				}
			}
		}
		if ( $p['used'] < $p['days'] ) {
			$amount = (int) round( $amount * $p['used'] / $p['days'] );
			$note = trim( $note . ' ' . $p['used'] . '/' . $p['days'] );
		}
		return array( $amount, $note );
	}
}

/* ---------- writes that can never be doubled ---------- */
if ( ! function_exists( 'nlrm_insert_once' ) ) {
	/* INSERT IGNORE on the (owner_id, auto_key) unique key: returns the new id,
	   or the id of the line that already holds the key (0 on a real failure) */
	function nlrm_insert_once( $row ) {
		global $wpdb;
		$t = nlrm_t( 'ledger' );
		$now = nlrm_now();
		$row = array_merge( array( 'created_at' => $now, 'updated_at' => $now ), $row );
		$cols = array_keys( $row );
		$ph = array();
		$vals = array();
		foreach ( $row as $v ) {
			if ( null === $v ) { $ph[] = 'NULL'; continue; }
			$ph[] = is_int( $v ) ? '%d' : '%s';
			$vals[] = $v;
		}
		$sql = 'INSERT IGNORE INTO ' . $t . ' (`' . implode( '`,`', $cols ) . '`) VALUES (' . implode( ',', $ph ) . ')';
		$wpdb->query( $vals ? $wpdb->prepare( $sql, $vals ) : $sql );
		if ( $wpdb->rows_affected > 0 && $wpdb->insert_id ) { return (int) $wpdb->insert_id; }
		if ( ! empty( $row['auto_key'] ) ) {
			return (int) $wpdb->get_var( $wpdb->prepare( 'SELECT id FROM ' . $t . ' WHERE owner_id = %d AND auto_key = %s', (int) $row['owner_id'], (string) $row['auto_key'] ) );
		}
		return 0;
	}
}
if ( ! function_exists( 'nlrm_cref' ) ) {
	/* the durable key of one user action */
	function nlrm_cref( $raw, $suffix = '' ) {
		$c = substr( preg_replace( '/[^A-Za-z0-9_\-]/', '', (string) $raw ), 0, 40 );
		return '' === $c ? null : 'cref:' . $c . ( $suffix ? ':' . $suffix : '' );
	}
}

/* ---------- the rent run ---------- */
if ( ! function_exists( 'nlrm_rent_run' ) ) {
	/**
	 * Writes every missing rent charge, up to the end of the current month,
	 * for active leases and for leases that ended in the last 13 months (so a
	 * period missed before the end is still charged). Idempotent: the unique
	 * key makes a second run, or two at once, a no-op. Also settles charges
	 * whose CPI was not available when they were written.
	 */
	function nlrm_rent_run( $owner, $today = null, $lease_id = 0 ) {
		global $wpdb;
		$today = $today ?: nlrm_today();
		$horizon = nlrm_month_end( $today );
		$w = $wpdb->prepare( " AND (status = 'active' OR (status = 'ended' AND end_date >= %s))", nlrm_add_months( $today, -13 ) );
		if ( $lease_id ) { $w .= $wpdb->prepare( ' AND id = %d', $lease_id ); }
		$leases = nlrm_get_all( 'lease', $owner, $w );
		if ( ! $leases ) { return 0; }
		$ids = array_map( function ( $l ) { return (int) $l['id']; }, $leases );
		$have = array_flip( (array) $wpdb->get_col( $wpdb->prepare( 'SELECT auto_key FROM ' . nlrm_t( 'ledger' ) . ' WHERE owner_id = %d AND auto_key LIKE %s AND lease_id IN (' . implode( ',', $ids ) . ')', $owner, 'rent:%' ) ) );
		$units = array();
		foreach ( nlrm_get_all( 'unit', $owner ) as $u ) { $units[ $u['id'] ] = $u; }
		$made = 0;
		foreach ( $leases as $l ) {
			if ( (int) $l['rent'] <= 0 ) { continue; }
			foreach ( nlrm_lease_periods( $l, $horizon ) as $p ) {
				if ( isset( $have[ $p['key'] ] ) ) { continue; }
				list( $amount, $note ) = nlrm_period_amount( $l, $p );
				$u = $units[ $l['unit_id'] ] ?? array( 'property_id' => 0 );
				$id = nlrm_insert_once( array(
					'owner_id' => (int) $owner, 'property_id' => (int) $u['property_id'], 'unit_id' => (int) $l['unit_id'], 'lease_id' => (int) $l['id'],
					'kind' => 'charge', 'category' => 'rent', 'amount' => (int) $amount, 'due_date' => $p['due'], 'status' => 'open',
					'auto_key' => $p['key'], 'note' => mb_substr( $note, 0, 255 ),
				) );
				if ( $id ) { $made++; $have[ $p['key'] ] = 1; }
			}
		}
		nlrm_cpi_settle( $owner, $leases );
		return $made;
	}
}
if ( ! function_exists( 'nlrm_cpi_settle' ) ) {
	/* charges written without the index: post the exact difference once it is known */
	function nlrm_cpi_settle( $owner, $leases ) {
		global $wpdb;
		$rows = $wpdb->get_results( $wpdb->prepare( 'SELECT * FROM ' . nlrm_t( 'ledger' ) . " WHERE owner_id = %d AND kind = 'charge' AND status <> 'void' AND note LIKE %s", $owner, 'cpi?%' ), ARRAY_A );
		if ( ! $rows ) { return 0; }
		$by = array();
		foreach ( $leases as $l ) { $by[ (int) $l['id'] ] = $l; }
		$n = 0;
		foreach ( $rows as $r ) {
			$l = $by[ (int) $r['lease_id'] ] ?? nlrm_get( 'lease', (int) $r['lease_id'], $owner );
			if ( ! $l ) { continue; }
			if ( ! preg_match( '/^rent:\d+:(\d{4}-\d{2})/', (string) $r['auto_key'], $mm ) ) { continue; }
			$p = null;
			foreach ( nlrm_lease_periods( array_merge( $l, array( 'end_date' => null, 'terms' => array() ) ), nlrm_month_end( (string) $r['due_date'] ) ) as $q ) {
				if ( substr( $q['start'], 0, 7 ) === $mm[1] ) { $p = $q; break; }
			}
			if ( ! $p ) { continue; }
			/* a prorated line keeps its days (written in its note as used/days) */
			if ( preg_match( '/ (\d+)\/(\d+)$/', (string) $r['note'], $dd ) ) { $p['used'] = (int) $dd[1]; $p['days'] = (int) $dd[2]; }
			list( $amount, $note ) = nlrm_period_amount( $l, $p );
			if ( 0 === strpos( $note, 'cpi?' ) ) { continue; }
			$diff = (int) $amount - (int) $r['amount'];
			if ( 0 !== $diff ) {
				nlrm_insert_once( array(
					'owner_id' => (int) $owner, 'property_id' => (int) $r['property_id'], 'unit_id' => (int) $r['unit_id'], 'lease_id' => (int) $r['lease_id'],
					'kind' => 'charge', 'category' => 'rent', 'amount' => $diff, 'due_date' => $r['due_date'], 'status' => 'open',
					'auto_key' => 'cpiadj:' . (int) $r['id'], 'note' => mb_substr( 'cpi+ ' . $note, 0, 255 ),
				) );
			}
			$wpdb->update( nlrm_t( 'ledger' ), array( 'note' => mb_substr( 'cpi= ' . $note, 0, 255 ), 'updated_at' => nlrm_now() ), array( 'id' => (int) $r['id'], 'owner_id' => (int) $owner ) );
			$n++;
		}
		return $n;
	}
}

/* ---------- balances, first in first out ---------- */
if ( ! function_exists( 'nlrm_money_fold' ) ) {
	/**
	 * The pure core (the browser's N.mx.fold is its line-by-line twin):
	 * $rows = every ledger line of ONE lease (any order). Returns the lease's
	 * summary in agorot and the derived state of each charge.
	 */
	function nlrm_money_fold( $rows, $today ) {
		$s = array( 'due' => 0, 'future' => 0, 'credit' => 0, 'balance' => 0, 'pending' => 0, 'pending_n' => 0, 'deposit_in' => 0, 'deposit_out' => 0, 'deposit_applied' => 0, 'deposit_held' => 0, 'writeoff' => 0, 'refunded' => 0, 'oldest_due' => null, 'late_days' => 0, 'open_n' => 0 );
		$charges = array();
		foreach ( $rows as $r ) {
			$r = (array) $r;
			$st = (string) $r['status']; $kind = (string) $r['kind']; $a = (int) $r['amount'];
			if ( 'void' === $st ) { continue; }
			if ( 'charge' === $kind ) {
				if ( empty( $r['due_date'] ) || $r['due_date'] <= $today ) { $s['due'] += $a; } else { $s['future'] += $a; }
				$charges[] = array( 'id' => (int) $r['id'], 'due' => (string) ( $r['due_date'] ?: '0000-00-00' ), 'amount' => $a );
			} elseif ( 'payment' === $kind ) {
				$ok = 'paid' === $st || 'deposited' === $st;
				if ( 'deposit' === $r['category'] ) { if ( $ok ) { $s['deposit_in'] += $a; } continue; }
				if ( $ok ) {
					$s['credit'] += $a;
					if ( 'deposit' === $r['method'] ) { $s['deposit_applied'] += $a; }
					if ( 'writeoff' === $r['method'] ) { $s['writeoff'] += $a; }
				} elseif ( 'pending' === $st ) { $s['pending'] += $a; $s['pending_n']++; }
			} elseif ( 'refund' === $kind ) {
				/* money back: the deposit, or a credit the tenant had (an overpayment) */
				if ( 'deposit' === $r['category'] ) { $s['deposit_out'] += $a; } else { $s['credit'] -= $a; $s['refunded'] += $a; }
			}
		}
		$s['balance'] = $s['due'] - $s['credit'];
		$s['deposit_held'] = $s['deposit_in'] - $s['deposit_out'] - $s['deposit_applied'];
		usort( $charges, function ( $x, $y ) { return strcmp( $x['due'], $y['due'] ) ?: ( $x['id'] - $y['id'] ); } );
		$left = $s['credit'];
		$state = array();
		foreach ( $charges as $c ) {
			if ( $c['amount'] <= 0 ) { $state[ $c['id'] ] = array( 'paid', $c['amount'] ); $left -= $c['amount']; continue; }
			$cover = max( 0, min( $c['amount'], $left ) );
			$left -= $cover;
			$st = $cover >= $c['amount'] ? 'paid' : ( $cover > 0 ? 'partial' : 'open' );
			$state[ $c['id'] ] = array( $st, $cover );
			if ( 'paid' !== $st && $c['due'] <= $today ) {
				$s['open_n']++;
				if ( null === $s['oldest_due'] ) { $s['oldest_due'] = '0000-00-00' === $c['due'] ? null : $c['due']; }
			}
		}
		if ( $s['oldest_due'] && $s['balance'] > 0 ) { $s['late_days'] = max( 0, nlrm_day_diff( $s['oldest_due'], $today ) ); }
		return array( 'sum' => $s, 'state' => $state );
	}
}

if ( ! function_exists( 'nlrm_money' ) ) {
	/* summaries of every lease of an owner (or of the given leases), from the full books */
	function nlrm_money( $owner, $today = null, $lease_ids = null, &$states = null ) {
		global $wpdb;
		$today = $today ?: nlrm_today();
		$w = '';
		if ( is_array( $lease_ids ) ) {
			$lease_ids = array_values( array_filter( array_map( 'intval', $lease_ids ) ) );
			if ( ! $lease_ids ) { return array(); }
			$w = ' AND lease_id IN (' . implode( ',', $lease_ids ) . ')';
		}
		$rows = $wpdb->get_results( $wpdb->prepare( 'SELECT id, lease_id, kind, category, method, status, amount, due_date FROM ' . nlrm_t( 'ledger' ) . " WHERE owner_id = %d AND lease_id > 0 AND status <> 'void'" . $w, $owner ), ARRAY_A );
		$by = array();
		foreach ( (array) $rows as $r ) { $by[ (int) $r['lease_id'] ][] = $r; }
		$out = array();
		$states = array();
		foreach ( $by as $lid => $list ) {
			$f = nlrm_money_fold( $list, $today );
			$out[ $lid ] = $f['sum'];
			$states += $f['state'];
		}
		return $out;
	}
}

/* ---------- the money actions (REST and the owner's quick link use these) ---------- */
if ( ! function_exists( 'nlrm_ledger_line' ) ) {
	function nlrm_ledger_line( $owner, $lease, $row, $cref, $actor ) {
		$lease = (array) $lease;
		$u = nlrm_get( 'unit', (int) $lease['unit_id'], $owner );
		$id = nlrm_insert_once( array_merge( array(
			'owner_id' => (int) $owner, 'property_id' => $u ? (int) $u['property_id'] : 0, 'unit_id' => (int) $lease['unit_id'], 'lease_id' => (int) $lease['id'],
			'status' => 'paid', 'auto_key' => $cref,
		), $row ) );
		if ( ! $id ) { return nlrm_err( 'nlrm_db', 500, 'השמירה נכשלה, נסו שוב.', 'Saving failed, please try again.' ); }
		nlrm_event( $owner, $actor, 'ledger', $id, 'money', '', '', array( 'kind' => $row['kind'], 'amount' => (int) $row['amount'], 'lease' => (int) $lease['id'] ) );
		return nlrm_get( 'ledger', $id, $owner );
	}
}
if ( ! function_exists( 'nlrm_pay' ) ) {
	/**
	 * A payment against a lease. $in: amount (shekels, decimals allowed),
	 * paid_date, method, ref, note, category (default rent), status override
	 * 'pending' (a tenant's report). A cheque dated in the future is
	 * 'pending' until deposited; it is not a credit before that.
	 */
	function nlrm_pay( $owner, $in, $cref = null, $actor = '' ) {
		$in = (array) $in;
		$lease = nlrm_get( 'lease', (int) ( $in['lease_id'] ?? 0 ), $owner );
		if ( ! $lease ) { return nlrm_err( 'nlrm_404', 404, 'החוזה לא נמצא.', 'Lease not found.' ); }
		$ag = (int) round( (float) ( $in['amount'] ?? 0 ) * 100 );
		if ( $ag <= 0 || $ag > 100000000 ) { return nlrm_err( 'nlrm_bad', 400, 'מה הסכום ששולם?', 'How much was paid?' ); }
		$methods = array( 'transfer', 'cheque', 'bit', 'paybox', 'cash', 'card', 'standing', 'other' );
		$method = in_array( (string) ( $in['method'] ?? '' ), $methods, true ) ? (string) $in['method'] : 'transfer';
		$date = nlrm_date( (string) ( $in['paid_date'] ?? '' ) ) ?: nlrm_today();
		$status = 'paid';
		$due = null;
		if ( 'cheque' === $method ) { $due = $date; if ( $date > nlrm_today() ) { $status = 'pending'; } }
		if ( isset( $in['status'] ) && 'pending' === $in['status'] ) { $status = 'pending'; }
		$cats = array( 'rent', 'water', 'electric', 'gas', 'arnona', 'vaad', 'repair', 'fee', 'other' );
		$cat = (string) ( $in['category'] ?? 'rent' );
		if ( ! in_array( $cat, $cats, true ) ) { $cat = 'rent'; }
		return nlrm_ledger_line( $owner, $lease, array(
			'kind' => 'payment', 'category' => $cat, 'amount' => $ag, 'paid_date' => 'pending' === $status && 'cheque' === $method ? null : $date,
			'due_date' => $due, 'method' => $method, 'ref' => mb_substr( sanitize_text_field( (string) ( $in['ref'] ?? '' ) ), 0, 40 ),
			'status' => $status, 'applies_to' => (int) ( $in['applies_to'] ?? 0 ), 'note' => mb_substr( sanitize_text_field( (string) ( $in['note'] ?? '' ) ), 0, 255 ),
		), $cref, $actor );
	}
}
if ( ! function_exists( 'nlrm_ledger_act' ) ) {
	/**
	 * deposit  : a pending cheque was deposited (paid_date = the day);
	 * confirm  : a pending report is confirmed as received;
	 * bounce   : a cheque came back (no longer a credit; optional bank fee
	 *            charged to the tenant as a separate line);
	 * void     : any line, with a reason; the books keep both.
	 */
	function nlrm_ledger_act( $owner, $id, $act, $in = array(), $actor = '' ) {
		global $wpdb;
		$in = (array) $in;
		$r = nlrm_get( 'ledger', (int) $id, $owner );
		if ( ! $r ) { return nlrm_err( 'nlrm_404', 404, 'השורה לא נמצאה.', 'Line not found.' ); }
		$t = nlrm_t( 'ledger' );
		$now = nlrm_now();
		$day = nlrm_date( (string) ( $in['date'] ?? '' ) ) ?: nlrm_today();
		if ( 'deposit' === $act || 'confirm' === $act ) {
			if ( 'payment' !== $r['kind'] || 'pending' !== $r['status'] ) { return nlrm_err( 'nlrm_state', 409, 'התשלום כבר עודכן.', 'This payment was already updated.' ); }
			$new = 'cheque' === $r['method'] ? 'deposited' : 'paid';
			$wpdb->update( $t, array( 'status' => $new, 'paid_date' => $r['paid_date'] ?: ( 'cheque' === $r['method'] ? $day : ( $r['paid_date'] ?: $day ) ), 'updated_at' => $now ), array( 'id' => $r['id'], 'owner_id' => $owner, 'status' => 'pending' ) );
		} elseif ( 'bounce' === $act ) {
			if ( 'payment' !== $r['kind'] || ! in_array( $r['status'], array( 'pending', 'deposited', 'paid' ), true ) ) { return nlrm_err( 'nlrm_state', 409, 'אפשר לסמן כחוזר רק תשלום שנרשם.', 'Only a recorded payment can bounce.' ); }
			$wpdb->update( $t, array( 'status' => 'bounced', 'updated_at' => $now ), array( 'id' => $r['id'], 'owner_id' => $owner ) );
			$fee = (int) round( (float) ( $in['fee'] ?? 0 ) * 100 );
			if ( $fee > 0 && $r['lease_id'] ) {
				$lease = nlrm_get( 'lease', (int) $r['lease_id'], $owner );
				if ( $lease ) {
					nlrm_ledger_line( $owner, $lease, array( 'kind' => 'charge', 'category' => 'fee', 'amount' => $fee, 'due_date' => $day, 'status' => 'open', 'applies_to' => (int) $r['id'], 'note' => 'bounce ' . $r['ref'] ), 'bounce:' . (int) $r['id'], $actor );
				}
			}
		} elseif ( 'void' === $act ) {
			if ( 'void' === $r['status'] ) { return $r; }
			$why = mb_substr( sanitize_text_field( (string) ( $in['reason'] ?? '' ) ), 0, 200 );
			if ( '' === $why ) { return nlrm_err( 'nlrm_bad', 400, 'מה הסיבה לביטול?', 'Why is it voided?' ); }
			$wpdb->update( $t, array( 'status' => 'void', 'note' => mb_substr( trim( $r['note'] . ' · void: ' . $why ), 0, 255 ), 'updated_at' => $now ), array( 'id' => $r['id'], 'owner_id' => $owner ) );
		} else {
			return nlrm_err( 'nlrm_bad', 400, 'פעולה לא מוכרת.', 'Unknown action.' );
		}
		nlrm_event( $owner, $actor, 'ledger', $r['id'], 'money_' . $act, '', '', array( 'lease' => (int) $r['lease_id'] ) );
		return nlrm_get( 'ledger', $r['id'], $owner );
	}
}

if ( ! function_exists( 'nlrm_sec_cap' ) ) {
	/* חוק השכירות והשאילה §25י(ב): all securities together are at most the lower of
	   3 months' rent or a third of the rent for the whole term (agorot) */
	function nlrm_sec_cap( $lease ) {
		$lease = (array) $lease;
		$rent = (int) round( (float) $lease['rent'] * 100 );
		if ( $rent <= 0 ) { return 0; }
		$months = 12;
		if ( ! empty( $lease['start_date'] ) && ! empty( $lease['end_date'] ) ) {
			$months = max( 1, (int) round( nlrm_day_diff( $lease['start_date'], nlrm_add_days( $lease['end_date'], 1 ) ) / 30.44 ) );
		}
		return (int) min( 3 * $rent, (int) floor( $months * $rent / 3 ) );
	}
}
if ( ! function_exists( 'nlrm_deposit' ) ) {
	/**
	 * The security deposit (cash held by the landlord):
	 *  receive : money in, held, not income; refused above the legal cap;
	 *  apply   : part of it pays a debt (unpaid rent, damage, bills, §25י(ג));
	 *  return  : money back to the tenant (§25י(ה): within 60 days of the
	 *            apartment being returned).
	 */
	function nlrm_deposit( $owner, $lease_id, $act, $in, $cref = null, $actor = '' ) {
		$in = (array) $in;
		$lease = nlrm_get( 'lease', (int) $lease_id, $owner );
		if ( ! $lease ) { return nlrm_err( 'nlrm_404', 404, 'החוזה לא נמצא.', 'Lease not found.' ); }
		$ag = (int) round( (float) ( $in['amount'] ?? 0 ) * 100 );
		if ( $ag <= 0 ) { return nlrm_err( 'nlrm_bad', 400, 'מה הסכום?', 'What is the amount?' ); }
		$m = nlrm_money( $owner, null, array( $lease['id'] ) );
		$held = (int) ( $m[ $lease['id'] ]['deposit_held'] ?? 0 );
		$date = nlrm_date( (string) ( $in['date'] ?? '' ) ) ?: nlrm_today();
		$note = mb_substr( sanitize_text_field( (string) ( $in['note'] ?? '' ) ), 0, 255 );
		if ( 'receive' === $act ) {
			$cap = nlrm_sec_cap( $lease );
			$other = (int) round( ( (float) ( ( (array) $lease['securities'] )['cheque'] ?? 0 ) ) * 100 );
			if ( $cap > 0 && $held + $ag + $other > $cap ) {
				return nlrm_err( 'nlrm_cap', 409, 'לפי חוק השכירות ההוגנת כל הביטחונות יחד הם עד ' . number_format( $cap / 100 ) . ' ₪ (הנמוך מ-3 חודשי שכירות ושליש מכל התקופה).', 'Under the Fair Rental Law all securities together are capped at ₪' . number_format( $cap / 100 ) . ' (the lower of 3 months\' rent and a third of the whole term).' );
			}
			$method = in_array( (string) ( $in['method'] ?? '' ), array( 'transfer', 'cheque', 'cash', 'bit', 'other', 'renewal' ), true ) ? (string) $in['method'] : 'transfer';
			return nlrm_ledger_line( $owner, $lease, array( 'kind' => 'payment', 'category' => 'deposit', 'amount' => $ag, 'paid_date' => $date, 'method' => $method, 'note' => $note ), $cref, $actor );
		}
		if ( $ag > $held ) {
			return nlrm_err( 'nlrm_held', 409, 'הסכום גדול מהפיקדון שמוחזק (' . number_format( $held / 100, 2 ) . ' ₪).', 'More than the deposit held (₪' . number_format( $held / 100, 2 ) . ').' );
		}
		if ( 'apply' === $act ) {
			$cats = array( 'rent', 'repair', 'water', 'electric', 'gas', 'arnona', 'vaad', 'other' );
			$cat = (string) ( $in['category'] ?? 'rent' );
		if ( ! in_array( $cat, $cats, true ) ) { $cat = 'rent'; }
			return nlrm_ledger_line( $owner, $lease, array( 'kind' => 'payment', 'category' => $cat, 'amount' => $ag, 'paid_date' => $date, 'method' => 'deposit', 'note' => $note ), $cref, $actor );
		}
		if ( 'return' === $act ) {
			$method = in_array( (string) ( $in['method'] ?? '' ), array( 'transfer', 'cheque', 'cash', 'bit', 'other', 'renewal' ), true ) ? (string) $in['method'] : 'transfer';
			return nlrm_ledger_line( $owner, $lease, array( 'kind' => 'refund', 'category' => 'deposit', 'amount' => $ag, 'paid_date' => $date, 'method' => $method, 'note' => $note ), $cref, $actor );
		}
		return nlrm_err( 'nlrm_bad', 400, 'פעולה לא מוכרת.', 'Unknown action.' );
	}
}

if ( ! function_exists( 'nlrm_lease_end' ) ) {
	/**
	 * The tenant leaves (end of term, early exit, eviction, renewal into a
	 * new lease). Rent stops at $date: periods after it are voided, the
	 * period it falls in is prorated by days (unless 'prorate' is false: the
	 * full period stays). The lease becomes 'ended'; whatever the tenant
	 * still owes stays on the books (a former tenant's debt is never hidden)
	 * and the deposit clock (60 days) starts.
	 */
	function nlrm_lease_end( $owner, $lease_id, $in, $actor = '' ) {
		global $wpdb;
		$in = (array) $in;
		$l = nlrm_get( 'lease', (int) $lease_id, $owner );
		if ( ! $l ) { return nlrm_err( 'nlrm_404', 404, 'החוזה לא נמצא.', 'Lease not found.' ); }
		if ( 'ended' === $l['status'] ) { return $l; }
		$date = nlrm_date( (string) ( $in['date'] ?? '' ) ) ?: nlrm_today();
		if ( $l['start_date'] && $date < nlrm_add_days( $l['start_date'], -1 ) ) { return nlrm_err( 'nlrm_bad', 400, 'תאריך הסיום לפני תחילת החוזה.', 'The end date is before the lease started.' ); }
		$reason = in_array( (string) ( $in['reason'] ?? '' ), array( 'term', 'early', 'eviction', 'mutual', 'renewal' ), true ) ? (string) $in['reason'] : 'term';
		$prorate = ! isset( $in['prorate'] ) || ! empty( $in['prorate'] );
		/* rent runs until the apartment is returned (an overstay is charged as use
		   fees at the same rent); without proration the period it falls in is whole */
		$new_end = $date;
		$walk = $l['start_date'] ? nlrm_lease_periods( array_merge( $l, array( 'end_date' => null, 'terms' => array() ) ), nlrm_month_end( nlrm_add_months( $date, 2 ) ) ) : array();
		$periods = array();
		foreach ( $walk as $p ) {
			$periods[ $p['key'] ] = $p;
			if ( ! $prorate && $p['start'] <= $date && $p['end'] >= $date ) { $new_end = $p['end']; }
		}
		$terms = (array) $l['terms'];
		$terms['ended'] = array( 'date' => $date, 'reason' => $reason, 'contract_end' => $l['end_date'], 'charged_to' => $new_end, 'at' => nlrm_now(), 'deposit_due' => nlrm_add_days( $date, 60 ) );
		$wpdb->update( nlrm_t( 'leases' ), array( 'status' => 'ended', 'end_date' => $new_end, 'terms' => wp_json_encode( nlrm_clean_json( $terms ), JSON_UNESCAPED_UNICODE ), 'updated_at' => nlrm_now() ), array( 'id' => $l['id'], 'owner_id' => $owner ) );
		$l2 = nlrm_get( 'lease', $l['id'], $owner );
		/* the books: lines of periods after the end are voided; a whole line of the
		   last period is replaced by its prorated amount */
		$charges = $wpdb->get_results( $wpdb->prepare( 'SELECT * FROM ' . nlrm_t( 'ledger' ) . " WHERE owner_id = %d AND lease_id = %d AND kind = 'charge' AND category = 'rent' AND status <> 'void' AND auto_key LIKE %s", $owner, $l['id'], 'rent:%' ), ARRAY_A );
		$voided = array();
		foreach ( (array) $charges as $c ) {
			$key = preg_replace( '/:p$/', '', (string) $c['auto_key'] );
			$p = $periods[ $key ] ?? null;
			if ( ! $p || $p['start'] > $new_end ) {
				$wpdb->update( nlrm_t( 'ledger' ), array( 'status' => 'void', 'note' => mb_substr( trim( $c['note'] . ' · void: after end ' . $new_end ), 0, 255 ), 'updated_at' => nlrm_now() ), array( 'id' => $c['id'], 'owner_id' => $owner ) );
				$voided[] = (int) $c['id'];
			} elseif ( $p['end'] > $new_end && $key === $c['auto_key'] ) {
				$q = $p; $q['used'] = nlrm_day_diff( $p['start'], $new_end ) + 1;
				list( $amount, $note ) = nlrm_period_amount( $l2, $q );
				if ( (int) $amount !== (int) $c['amount'] ) {
					$wpdb->update( nlrm_t( 'ledger' ), array( 'status' => 'void', 'note' => mb_substr( trim( $c['note'] . ' · void: prorated to ' . $new_end ), 0, 255 ), 'updated_at' => nlrm_now() ), array( 'id' => $c['id'], 'owner_id' => $owner ) );
					$voided[] = (int) $c['id'];
					nlrm_insert_once( array(
						'owner_id' => (int) $owner, 'property_id' => (int) $c['property_id'], 'unit_id' => (int) $c['unit_id'], 'lease_id' => (int) $l['id'],
						'kind' => 'charge', 'category' => 'rent', 'amount' => (int) $amount, 'due_date' => $c['due_date'], 'status' => 'open',
						'auto_key' => $c['auto_key'] . ':p', 'note' => mb_substr( $note, 0, 255 ),
					) );
				}
			}
		}
		/* a CPI difference follows the line it corrected */
		if ( $voided ) {
			foreach ( (array) $wpdb->get_results( $wpdb->prepare( 'SELECT id, auto_key FROM ' . nlrm_t( 'ledger' ) . " WHERE owner_id = %d AND lease_id = %d AND auto_key LIKE %s AND status <> 'void'", $owner, $l['id'], 'cpiadj:%' ), ARRAY_A ) as $a ) {
				if ( in_array( (int) substr( $a['auto_key'], 7 ), $voided, true ) ) {
					$wpdb->update( nlrm_t( 'ledger' ), array( 'status' => 'void', 'updated_at' => nlrm_now() ), array( 'id' => (int) $a['id'], 'owner_id' => $owner ) );
				}
			}
		}
		/* every period up to the end exists (an overstay adds its periods) */
		nlrm_rent_run( $owner, max( nlrm_today(), $new_end ), $l['id'] );
		nlrm_event( $owner, $actor, 'lease', $l['id'], 'lease_end', '', '', array( 'date' => $date, 'reason' => $reason ) );
		return nlrm_get( 'lease', $l['id'], $owner );
	}
}

if ( ! function_exists( 'nlrm_lease_renew' ) ) {
	/**
	 * A new term for the same tenant (an option exercised or a new deal): the
	 * old lease ends the day before, a new lease starts with the new rent and
	 * dates, the parties and securities carry over, and a cash deposit moves
	 * with two visible lines (returned on the old, received on the new).
	 */
	function nlrm_lease_renew( $owner, $lease_id, $in, $cref = null, $actor = '' ) {
		$in = (array) $in;
		$old = nlrm_get( 'lease', (int) $lease_id, $owner );
		if ( ! $old ) { return nlrm_err( 'nlrm_404', 404, 'החוזה לא נמצא.', 'Lease not found.' ); }
		if ( $cref ) {
			$prev = (int) ( ( (array) $old['terms'] )['renewed_by'] ?? 0 );
			if ( $prev ) { return nlrm_get( 'lease', $prev, $owner ); }
		}
		$start = nlrm_date( (string) ( $in['start_date'] ?? '' ) ) ?: ( $old['end_date'] ? nlrm_add_days( $old['end_date'], 1 ) : nlrm_today() );
		$end = nlrm_date( (string) ( $in['end_date'] ?? '' ) ) ?: nlrm_add_days( nlrm_add_months( $start, 12 ), -1 );
		$rent = isset( $in['rent'] ) ? (float) $in['rent'] : (float) $old['rent'];
		if ( $rent <= 0 || $end < $start ) { return nlrm_err( 'nlrm_bad', 400, 'בדקו את התאריכים ואת שכר הדירה.', 'Check the dates and the rent.' ); }
		$m = nlrm_money( $owner, null, array( $old['id'] ) );
		$held = (int) ( $m[ $old['id'] ]['deposit_held'] ?? 0 );
		nlrm_lease_end( $owner, $old['id'], array( 'date' => nlrm_add_days( $start, -1 ), 'reason' => 'renewal', 'prorate' => true ), $actor );
		$link = (array) $old['linkage'];
		if ( isset( $in['linkage'] ) && is_array( $in['linkage'] ) ) { $link = array_merge( $link, $in['linkage'] ); }
		if ( ! empty( $link['mode'] ) && 'cpi' === $link['mode'] ) { $link['base_date'] = $start; }
		$terms = (array) $old['terms'];
		unset( $terms['ended'], $terms['renewed_by'], $terms['track_from'], $terms['sign_sent'] );
		$terms['renews'] = (int) $old['id'];
		$new = nlrm_save( 'lease', array(
			'unit_id' => (int) $old['unit_id'], 'status' => 'active', 'start_date' => $start, 'end_date' => $end,
			'option_until' => nlrm_date( (string) ( $in['option_until'] ?? '' ) ), 'rent' => (int) round( $rent ), 'pay_day' => (int) ( $in['pay_day'] ?? $old['pay_day'] ),
			'linkage' => $link, 'securities' => (array) $old['securities'], 'parties' => (array) $old['parties'], 'terms' => $terms,
		), $owner, $actor );
		if ( is_wp_error( $new ) ) { return $new; }
		$old2 = nlrm_get( 'lease', $old['id'], $owner );
		$ot = (array) $old2['terms']; $ot['renewed_by'] = (int) $new['id'];
		$GLOBALS['wpdb']->update( nlrm_t( 'leases' ), array( 'terms' => wp_json_encode( nlrm_clean_json( $ot ), JSON_UNESCAPED_UNICODE ) ), array( 'id' => $old['id'], 'owner_id' => $owner ) );
		if ( $held > 0 ) {
			$day = $start;
			nlrm_ledger_line( $owner, $old, array( 'kind' => 'refund', 'category' => 'deposit', 'amount' => $held, 'paid_date' => $day, 'method' => 'renewal', 'note' => '→ #' . $new['id'] ), 'renew-out:' . (int) $old['id'], $actor );
			nlrm_ledger_line( $owner, $new, array( 'kind' => 'payment', 'category' => 'deposit', 'amount' => $held, 'paid_date' => $day, 'method' => 'renewal', 'note' => '← #' . $old['id'] ), 'renew-in:' . (int) $new['id'], $actor );
		}
		nlrm_rent_run( $owner, null, $new['id'] );
		nlrm_event( $owner, $actor, 'lease', $new['id'], 'lease_renew', '', '', array( 'from' => (int) $old['id'] ) );
		return nlrm_get( 'lease', $new['id'], $owner );
	}
}

if ( ! function_exists( 'nlrm_book' ) ) {
	/**
	 * A line the landlord writes himself: an expense or other income of his
	 * own books, or an extra charge to a tenant (water, a repair he caused).
	 * Payments, deposits and refunds have their own actions above.
	 */
	function nlrm_book( $owner, $in, $cref = null, $actor = '' ) {
		$in = (array) $in;
		$kind = in_array( (string) ( $in['kind'] ?? '' ), array( 'expense', 'income', 'charge' ), true ) ? (string) $in['kind'] : '';
		if ( ! $kind ) { return nlrm_err( 'nlrm_bad', 400, 'סוג שורה לא מוכר.', 'Unknown line type.' ); }
		$row = nlrm_clean_row( 'ledger', array_intersect_key( $in, array_flip( array( 'property_id', 'unit_id', 'lease_id', 'category', 'amount', 'due_date', 'paid_date', 'method', 'ref', 'note', 'doc_id' ) ) ), $owner );
		if ( is_wp_error( $row ) ) { return $row; }
		if ( (int) ( $row['amount'] ?? 0 ) <= 0 ) { return nlrm_err( 'nlrm_bad', 400, 'מה הסכום?', 'What is the amount?' ); }
		if ( in_array( $row['method'] ?? '', array( 'deposit', 'writeoff', 'renewal' ), true ) ) { $row['method'] = 'other'; }
		if ( 'charge' === $kind ) {
			$lease = nlrm_get( 'lease', (int) ( $row['lease_id'] ?? 0 ), $owner );
			if ( ! $lease ) { return nlrm_err( 'nlrm_404', 404, 'לחיוב צריך חוזה.', 'A charge needs a lease.' ); }
			$u = nlrm_get( 'unit', (int) $lease['unit_id'], $owner );
			$row['unit_id'] = (int) $lease['unit_id'];
			$row['property_id'] = $u ? (int) $u['property_id'] : 0;
			$row['status'] = 'open';
			$row['due_date'] = $row['due_date'] ?? nlrm_today();
			$row['paid_date'] = null;
		} else {
			if ( ! empty( $row['unit_id'] ) && empty( $row['property_id'] ) ) {
				$u = nlrm_get( 'unit', (int) $row['unit_id'], $owner );
				$row['property_id'] = $u ? (int) $u['property_id'] : 0;
			}
			$row['status'] = 'paid';
			$row['paid_date'] = $row['paid_date'] ?? nlrm_today();
		}
		$row['kind'] = $kind;
		$row['owner_id'] = (int) $owner;
		$row['auto_key'] = $cref;
		$id = nlrm_insert_once( $row );
		if ( ! $id ) { return nlrm_err( 'nlrm_db', 500, 'השמירה נכשלה, נסו שוב.', 'Saving failed, please try again.' ); }
		nlrm_event( $owner, $actor, 'ledger', $id, 'money', '', '', array( 'kind' => $kind, 'amount' => (int) $row['amount'] ) );
		return nlrm_get( 'ledger', $id, $owner );
	}
}
if ( ! function_exists( 'nlrm_refund_credit' ) ) {
	/* the tenant paid more than he owed (a cheque for a month he did not stay,
	   say): the landlord gives the difference back, up to the credit */
	function nlrm_refund_credit( $owner, $lease_id, $in, $cref = null, $actor = '' ) {
		$in = (array) $in;
		$lease = nlrm_get( 'lease', (int) $lease_id, $owner );
		if ( ! $lease ) { return nlrm_err( 'nlrm_404', 404, 'החוזה לא נמצא.', 'Lease not found.' ); }
		$m = nlrm_money( $owner, null, array( $lease['id'] ) );
		$credit = -(int) ( $m[ $lease['id'] ]['balance'] ?? 0 ) - (int) ( $m[ $lease['id'] ]['future'] ?? 0 );
		$ag = (int) round( (float) ( $in['amount'] ?? 0 ) * 100 );
		if ( $ag <= 0 || $ag > $credit ) { return nlrm_err( 'nlrm_bad', 400, 'אפשר להחזיר עד גובה הזכות של השוכר.', 'You can refund up to the credit the tenant has.' ); }
		$method = in_array( (string) ( $in['method'] ?? '' ), array( 'transfer', 'cheque', 'cash', 'bit', 'other' ), true ) ? (string) $in['method'] : 'transfer';
		return nlrm_ledger_line( $owner, $lease, array( 'kind' => 'refund', 'category' => 'rent', 'amount' => $ag, 'paid_date' => nlrm_date( (string) ( $in['date'] ?? '' ) ) ?: nlrm_today(), 'method' => $method, 'note' => mb_substr( sanitize_text_field( (string) ( $in['note'] ?? '' ) ), 0, 255 ) ), $cref, $actor );
	}
}
if ( ! function_exists( 'nlrm_writeoff' ) ) {
	/* the landlord gives up a debt (after an eviction, say): a credit that is
	   not income, so the balance closes and the reports stay true */
	function nlrm_writeoff( $owner, $lease_id, $in, $cref = null, $actor = '' ) {
		$in = (array) $in;
		$lease = nlrm_get( 'lease', (int) $lease_id, $owner );
		if ( ! $lease ) { return nlrm_err( 'nlrm_404', 404, 'החוזה לא נמצא.', 'Lease not found.' ); }
		$m = nlrm_money( $owner, null, array( $lease['id'] ) );
		$bal = (int) ( $m[ $lease['id'] ]['balance'] ?? 0 );
		$ag = isset( $in['amount'] ) ? (int) round( (float) $in['amount'] * 100 ) : $bal;
		if ( $ag <= 0 || $ag > $bal ) { return nlrm_err( 'nlrm_bad', 400, 'אפשר למחוק עד גובה החוב.', 'You can write off up to the debt.' ); }
		return nlrm_ledger_line( $owner, $lease, array( 'kind' => 'payment', 'category' => 'rent', 'amount' => $ag, 'paid_date' => nlrm_date( (string) ( $in['date'] ?? '' ) ) ?: nlrm_today(), 'method' => 'writeoff', 'note' => mb_substr( sanitize_text_field( (string) ( $in['note'] ?? '' ) ), 0, 255 ) ), $cref, $actor );
	}
}

/* ---------- the reports: totals by month, from the full books ---------- */
if ( ! function_exists( 'nlrm_stats' ) ) {
	/**
	 * Income = money that became the landlord's: payments except deposits
	 * received and write-offs (a deposit applied to a debt IS income then).
	 * Expenses = the landlord's own expenses. Deposits are a liability and
	 * never appear in either.
	 */
	function nlrm_stats( $owner, $from = null ) {
		global $wpdb;
		$from = $from ?: nlrm_add_months( substr( nlrm_today(), 0, 8 ) . '01', -119 );
		$rows = $wpdb->get_results( $wpdb->prepare(
			'SELECT SUBSTR(COALESCE(paid_date, due_date), 1, 7) AS ym, kind, category, method, property_id, SUM(amount) AS s FROM ' . nlrm_t( 'ledger' ) .
			" WHERE owner_id = %d AND status IN ('paid','deposited') AND kind IN ('payment','expense','income','refund') AND COALESCE(paid_date, due_date) >= %s GROUP BY ym, kind, category, method, property_id",
			$owner, $from ), ARRAY_A );
		$out = array();
		foreach ( (array) $rows as $r ) {
			$ym = (string) $r['ym'];
			if ( ! isset( $out[ $ym ] ) ) { $out[ $ym ] = array( 'income' => 0, 'expense' => 0, 'by_cat' => array(), 'by_prop' => array() ); }
			$s = (int) $r['s'];
			if ( 'refund' === $r['kind'] ) {
				/* an overpayment given back is not income; a deposit returned never was */
				if ( 'deposit' === $r['category'] ) { continue; }
				$out[ $ym ]['income'] -= $s;
				$out[ $ym ]['by_cat'][ $r['category'] ] = ( $out[ $ym ]['by_cat'][ $r['category'] ] ?? 0 ) - $s;
				$out[ $ym ]['by_prop'][ (int) $r['property_id'] ] = ( $out[ $ym ]['by_prop'][ (int) $r['property_id'] ] ?? 0 ) - $s;
			} elseif ( 'expense' === $r['kind'] ) {
				$out[ $ym ]['expense'] += $s;
				$out[ $ym ]['by_cat'][ $r['category'] ] = ( $out[ $ym ]['by_cat'][ $r['category'] ] ?? 0 ) - $s;
				$out[ $ym ]['by_prop'][ (int) $r['property_id'] ] = ( $out[ $ym ]['by_prop'][ (int) $r['property_id'] ] ?? 0 ) - $s;
			} else {
				if ( 'deposit' === $r['category'] || 'writeoff' === $r['method'] ) { continue; }
				$out[ $ym ]['income'] += $s;
				$out[ $ym ]['by_cat'][ $r['category'] ] = ( $out[ $ym ]['by_cat'][ $r['category'] ] ?? 0 ) + $s;
				$out[ $ym ]['by_prop'][ (int) $r['property_id'] ] = ( $out[ $ym ]['by_prop'][ (int) $r['property_id'] ] ?? 0 ) + $s;
			}
		}
		ksort( $out );
		return $out;
	}
}

/* ---------- the daily job: rent for everyone, and the 30-day purge ---------- */
add_action( 'nlrm_daily', function () {
	if ( function_exists( 'nadlan_rm_on' ) && ! nadlan_rm_on() ) { return; }
	nlrm_daily_run();
} );
if ( ! function_exists( 'nlrm_daily_run' ) ) {
	function nlrm_daily_run() {
		global $wpdb;
		if ( get_option( 'nlrm_db_version' ) !== NLRM_DB_VERSION ) { return; }
		foreach ( (array) $wpdb->get_col( 'SELECT DISTINCT owner_id FROM ' . nlrm_t( 'leases' ) . " WHERE status IN ('active','ended') AND deleted_at IS NULL" ) as $o ) {
			nlrm_rent_run( (int) $o );
		}
		if ( function_exists( 'nlrm_notify_digest' ) ) { nlrm_notify_digest(); }
		nlrm_purge();
	}
}
if ( ! function_exists( 'nlrm_purge' ) ) {
	/* what a landlord deleted is gone for good after 30 days: personal data,
	   files, links. The books are never deleted (tax records, 7 years). */
	function nlrm_purge( $days = 30 ) {
		global $wpdb;
		$cut = gmdate( 'Y-m-d H:i:s', nlrm_time() - (int) $days * 86400 );
		$n = 0;
		foreach ( (array) $wpdb->get_results( $wpdb->prepare( 'SELECT id, path FROM ' . nlrm_t( 'docs' ) . ' WHERE deleted_at IS NOT NULL AND deleted_at < %s', $cut ), ARRAY_A ) as $d ) {
			if ( function_exists( 'nlrm_private_dir' ) && $d['path'] ) { @unlink( nlrm_private_dir() . $d['path'] ); } // phpcs:ignore
			$n += (int) $wpdb->delete( nlrm_t( 'docs' ), array( 'id' => (int) $d['id'] ) );
		}
		foreach ( array( 'contacts', 'tickets', 'units', 'properties', 'leases' ) as $t ) {
			$n += (int) $wpdb->query( $wpdb->prepare( 'DELETE FROM ' . nlrm_t( $t ) . ' WHERE deleted_at IS NOT NULL AND deleted_at < %s', $cut ) );
		}
		$n += (int) $wpdb->query( $wpdb->prepare( 'DELETE FROM ' . nlrm_t( 'links' ) . ' WHERE expires_at < %s', gmdate( 'Y-m-d H:i:s', nlrm_time() - 400 * 86400 ) ) );
		return $n;
	}
}
add_action( 'init', function () {
	if ( function_exists( 'wp_next_scheduled' ) && ! wp_next_scheduled( 'nlrm_daily' ) ) {
		wp_schedule_event( time() + 600, 'daily', 'nlrm_daily' );
	}
} );
