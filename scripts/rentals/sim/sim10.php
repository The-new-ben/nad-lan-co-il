<?php
/**
 * HAD-383 - the 10-year simulation of the rentals module, on the REAL code.
 *
 * 120 months, day by day (1.10.2026 - 30.9.2036), a fixed seed, four
 * landlords in one database (1, 3, 15 and 200 apartments). Everything goes
 * through the module's own functions and REST routes (inc/rentals/*.php):
 * leases, the rent run, payments, cheques and bounces, tenants' reports from
 * their personal link, deposits under the Fair Rental Law, repairs and
 * vendors, renewals, early exits, evictions, write-offs, Hebrew and English,
 * deletion and the 30-day purge, export, erase, a key rotation, a salt change
 * and a lost key file.
 *
 * An independent ORACLE (its own calendar code on DateTimeImmutable, its own
 * books) says what every lease must owe; the engine is compared with it at
 * every month end, to the agora. Every check is counted; every failure is
 * written to out/report.json.
 *
 * php -d extension=pdo_sqlite -d extension=sodium sim10.php [--seed=N] [--years=10] [--out=DIR]
 */

error_reporting( E_ALL );
ini_set( 'memory_limit', '2048M' );
require __DIR__ . '/wp_shim.php';

$opt   = getopt( '', array( 'seed::', 'years::', 'out::', 'child::', 'db::', 'up::', 'cid::' ) );
$SEED  = (int) ( $opt['seed'] ?? 20261003 );
$YEARS = (int) ( $opt['years'] ?? 10 );
$OUT   = $opt['out'] ?? __DIR__ . '/out';

/* ---------- the clock ---------- */
$GLOBALS['SIM_T'] = gmmktime( 9, 0, 0, 10, 1, 2026 );
add_filter( 'nlrm_time', function () { return $GLOBALS['SIM_T']; } );
function day_set( $ymd ) { $GLOBALS['SIM_T'] = gmmktime( 9, 0, 0, (int) substr( $ymd, 5, 2 ), (int) substr( $ymd, 8, 2 ), (int) substr( $ymd, 0, 4 ) ); }
function today() { return gmdate( 'Y-m-d', $GLOBALS['SIM_T'] ); }

/* ---------- child processes: another request with another salt / no key file ---------- */
if ( ! empty( $opt['child'] ) ) {
	if ( 'nokey' === $opt['child'] ) { add_filter( 'nlrm_keyfile_path', function () { return $GLOBALS['sim_upload_dir'] . '/nlrm-private/.missing-key.php'; } ); }
	sim_boot( $opt['db'], $opt['up'] );
	$c = nlrm_get( 'contact', (int) $opt['cid'], (int) $GLOBALS['wpdb']->get_var( 'SELECT owner_id FROM wp_nlrm_contacts WHERE id = ' . (int) $opt['cid'] ) );
	echo json_encode( array( 'name' => $c ? $c['name'] : null, 'phone' => $c ? $c['phone'] : null, 'key_ok' => nlrm_key_ok(), 'src' => nlrm_keyring()['src'] ), JSON_UNESCAPED_UNICODE );
	exit;
}

/* ---------- a seeded generator (mulberry32), one stream per purpose ---------- */
class Rng {
	private $s;
	function __construct( $seed ) { $this->s = $seed & 0xffffffff; }
	function f() {
		$this->s = ( $this->s + 0x6D2B79F5 ) & 0xffffffff;
		$t = $this->s;
		$t = $this->mul( $t ^ ( $t >> 15 ), $t | 1 );
		$t ^= ( $t + $this->mul( $t ^ ( $t >> 7 ), $t | 61 ) ) & 0xffffffff;
		return ( ( $t ^ ( $t >> 14 ) ) & 0xffffffff ) / 4294967296;
	}
	private function mul( $a, $b ) { return (int) ( ( ( $a & 0xffff ) * $b + ( ( ( ( $a >> 16 ) * $b ) & 0xffff ) << 16 ) ) & 0xffffffff ); }
	function i( $lo, $hi ) { return $lo + (int) floor( $this->f() * ( $hi - $lo + 1 ) ); }
	function p( $prob ) { return $this->f() < $prob; }
	function pick( $arr ) { return $arr[ $this->i( 0, count( $arr ) - 1 ) ]; }
}
$R = new Rng( $SEED );

/* ---------- the consumer price index, monthly (input data, not logic) ---------- */
$YEARLY = array( 2024 => 3.2, 2025 => 3.0, 2026 => 2.8, 2027 => 2.5, 2028 => -1.2, 2029 => 4.8, 2030 => 5.6, 2031 => -0.6, 2032 => 1.8, 2033 => 2.2, 2034 => 2.0, 2035 => 2.4, 2036 => 1.5, 2037 => 2.0, 2038 => 2.0 );
$CPI = array();
$idx = 100.0;
$cr = new Rng( $SEED ^ 0x5a5a );
for ( $y = 2024; $y <= 2038; $y++ ) {
	for ( $m = 1; $m <= 12; $m++ ) {
		$idx = $idx * pow( 1 + $YEARLY[ $y ] / 100, 1 / 12 ) * ( 1 + ( $cr->f() - 0.5 ) * 0.004 );
		$CPI[ sprintf( '%04d-%02d', $y, $m ) ] = round( $idx, 1 );
	}
}
$GLOBALS['CPI'] = $CPI;
/* the CBS calculator is "down" in these months: the engine must charge, mark and settle later */
$GLOBALS['CPI_DOWN'] = array( '2028-07' => 1, '2031-02' => 1, '2034-11' => 1 );
function cpi_factor_raw( $from, $to ) {
	$a = $GLOBALS['CPI'][ substr( $from, 0, 7 ) ]; $b = $GLOBALS['CPI'][ substr( $to, 0, 7 ) ];
	return round( $b / $a * 1000, 2 ) / 1000; /* the CBS calculator answers 1000 -> x.xx */
}
add_filter( 'nlrm_cpi_factor', function ( $v, $from, $to ) {
	if ( isset( $GLOBALS['CPI_DOWN'][ substr( today(), 0, 7 ) ] ) ) { $GLOBALS['M']['cpi_down_calls']++; return new WP_Error( 'cbs', 'down' ); }
	return cpi_factor_raw( $from, $to );
}, 10, 3 );

/* ---------- the oracle: its own calendar, its own sums ---------- */
function o_add_months( $start, $k ) {
	$d = DateTimeImmutable::createFromFormat( '!Y-m-d', $start, new DateTimeZone( 'UTC' ) );
	$day = (int) $d->format( 'j' );
	$f = $d->modify( 'first day of this month' )->modify( '+' . (int) $k . ' months' );
	return $f->setDate( (int) $f->format( 'Y' ), (int) $f->format( 'n' ), min( $day, (int) $f->format( 't' ) ) )->format( 'Y-m-d' );
}
function o_days( $a, $b ) {
	$x = new DateTimeImmutable( $a . ' 00:00:00', new DateTimeZone( 'UTC' ) );
	$y = new DateTimeImmutable( $b . ' 00:00:00', new DateTimeZone( 'UTC' ) );
	return (int) $x->diff( $y )->format( '%r%a' );
}
function o_plus_days( $a, $n ) { return ( new DateTimeImmutable( $a . ' 00:00:00', new DateTimeZone( 'UTC' ) ) )->modify( ( $n >= 0 ? '+' : '' ) . $n . ' days' )->format( 'Y-m-d' ); }
function o_month_end( $a ) { return ( new DateTimeImmutable( $a, new DateTimeZone( 'UTC' ) ) )->format( 'Y-m-t' ); }
/* the periods the oracle expects, each with its amount in agorot */
function o_periods( $L, $horizon ) {
	$out = array();
	$end = $L['end_eff'] ?: $L['end'];
	for ( $k = 0; $k < 400; $k++ ) {
		$ps = o_add_months( $L['start'], $k );
		if ( $end && $ps > $end ) { break; }
		if ( $end && $ps === $end && $k > 0 && (int) substr( $ps, 8 ) < (int) substr( $L['start'], 8 ) ) { break; }
		$nx = o_add_months( $L['start'], $k + 1 );
		$due = substr( $ps, 0, 8 ) . sprintf( '%02d', $L['pay_day'] );
		if ( 0 === $k && $due < $L['start'] ) { $due = $L['start']; }
		if ( $due > $horizon ) { break; }
		if ( $L['track_from'] && $due < $L['track_from'] ) { continue; }
		$days = o_days( $ps, $nx );
		$used = ( $end && $end < o_plus_days( $nx, -1 ) ) ? o_days( $ps, $end ) + 1 : $days;
		$base = $L['rent'] * 100;
		$amt = $base;
		if ( 'cpi' === $L['link']['mode'] ) {
			$step = intdiv( $k, $L['link']['every'] ) * $L['link']['every'];
			if ( $step > 0 ) {
				$f = cpi_factor_raw( $L['link']['base_date'], o_add_months( $L['start'], $step ) );
				$new = $base * ( 1 + $L['link']['pct'] / 100 * ( $f - 1 ) );
				if ( $L['link']['floor'] ) { $new = max( $base, $new ); }
				$amt = (int) round( $new );
			}
		}
		if ( $used < $days ) { $amt = (int) round( $amt * $used / $days ); }
		$out[ substr( $ps, 0, 7 ) ] = array( 'k' => $k, 'start' => $ps, 'due' => $due, 'amount' => $amt, 'partial' => $used < $days );
	}
	return $out;
}

/* ---------- bookkeeping of the run ---------- */
$GLOBALS['M'] = array( 'checks' => 0, 'fails' => 0, 'fail_list' => array(), 'by' => array(), 'cpi_down_calls' => 0, 'perf' => array(), 'events' => array() );
function check( $name, $ok, $info = '' ) {
	$M = &$GLOBALS['M'];
	$M['checks']++;
	$M['by'][ $name ] = $M['by'][ $name ] ?? array( 0, 0 );
	if ( $ok ) { $M['by'][ $name ][0]++; return true; }
	$M['by'][ $name ][1]++;
	$M['fails']++;
	if ( count( $M['fail_list'] ) < 200 ) { $M['fail_list'][] = today() . ' ' . $name . ' ' . $info; }
	return false;
}
function count_ev( $k, $n = 1 ) { $GLOBALS['M']['events'][ $k ] = ( $GLOBALS['M']['events'][ $k ] ?? 0 ) + $n; }

/* ---------- the world ---------- */
@mkdir( $OUT, 0777, true );
$DB = $OUT . '/sim.db';
$UP = $OUT . '/uploads';
@unlink( $DB ); @unlink( $DB . '-wal' ); @unlink( $DB . '-shm' );
if ( is_dir( $UP ) ) { exec( 'rm -rf ' . escapeshellarg( $UP ) ); }
sim_boot( $DB, $UP );
nlrm_install();
check( 'install.version', NLRM_DB_VERSION === get_option( 'nlrm_db_version' ) );
check( 'install.key_from_file', 'file' === nlrm_keyring()['src'], nlrm_keyring()['src'] );
check( 'install.keycheck', nlrm_key_ok() );

$NAMES = array(
	'he' => array( 'נועה לוי', 'יוסי כהן', 'מיכל אברהם', 'דוד מזרחי', 'שירה פרץ', 'אורי ביטון', 'רוני דהן', 'תמר אזולאי', 'איתי פרידמן', 'ליאת שגיא', 'עומר גבאי', 'הדס רוזן' ),
	'en' => array( 'Daniel Brooks', 'Emma Clarke', 'Liam Walsh', 'Sophie Turner', 'Noah Fisher', 'Olivia Grant', 'Ethan Hughes', 'Mia Foster' ),
	'ru' => array( 'Анна Иванова', 'Дмитрий Козлов', 'Елена Смирнова', 'Игорь Волков' ),
	'ar' => array( 'סמיר חורי', 'ראניה עודה', 'Rami Haddad', 'Lina Nasser' ),
);
$W = array( 'owners' => array(), 'leases' => array(), 'units' => array(), 'queue' => array(), 'phone' => 500000000, 'ip' => 1,
	'tally' => array( 'cash_in' => 0, 'cash_out' => 0, 'income' => 0, 'expense' => 0 ), 'tickets' => array(), 'docs' => array(), 'deleted_contacts' => array(), 'pays' => 0 );

function q_add( $day, $fn ) { $GLOBALS['W']['queue'][ $day ][] = $fn; }
function as_owner( $o ) { $GLOBALS['sim_user'] = $o; }

/* a landlord: properties and units */
function make_owner( $oid, $label, $props, $rest = false ) {
	global $W;
	as_owner( $oid );
	update_user_meta( $oid, 'nlrm_plan', 'business' );
	update_user_meta( $oid, 'nlrm_idno_enc', nlrm_enc( '0' . ( 30000000 + $oid ) ) );
	$W['owners'][ $oid ] = array( 'label' => $label, 'props' => array(), 'units' => array(), 'rest' => $rest );
	foreach ( $props as $pi => $pp ) {
		$p = nlrm_save( 'property', array( 'title' => '', 'address' => $pp[0], 'city' => $pp[1], 'floors' => $pp[2], 'units_per_floor' => $pp[3], 'meta' => array( 'year_built' => 1990 + $pi ) ), $oid );
		$W['owners'][ $oid ]['props'][] = $p['id'];
		for ( $i = 0; $i < $pp[4]; $i++ ) {
			$u = nlrm_save( 'unit', array( 'property_id' => $p['id'], 'label' => 'דירה ' . ( $i + 1 ), 'floor' => 1 + intdiv( $i, max( 1, $pp[3] ) ), 'pos' => $i % max( 1, $pp[3] ), 'rooms' => 3 + ( $i % 3 ), 'sqm' => 70 + 5 * ( $i % 5 ) ), $oid );
			$W['owners'][ $oid ]['units'][] = $u['id'];
			$W['units'][ $u['id'] ] = array( 'owner' => $oid, 'prop' => $p['id'], 'lease' => 0, 'vacant_since' => null );
		}
	}
}

/* a tenant moves in: contact, lease, deposit, cheques, link */
function move_in( $oid, $uid, $start, $o = array() ) {
	global $W, $R, $NAMES;
	as_owner( $oid );
	$lang = $o['lang'] ?? ( $R->p( 0.7 ) ? 'he' : $R->pick( array( 'en', 'en', 'ru', 'ar' ) ) );
	$W['phone']++;
	$name = $R->pick( $NAMES[ $lang ] );
	$c = nlrm_save( 'contact', array( 'kind' => 'tenant', 'name' => $name, 'phone' => '0' . $W['phone'], 'email' => 't' . $W['phone'] . '@example.com', 'lang' => $lang, 'idno' => (string) ( 200000000 + $W['phone'] % 1000000 ), 'notes' => 'sim' ), $oid );
	$months = $o['months'] ?? $R->pick( array( 12, 12, 12, 24, 24, 36 ) );
	$end = $o['end'] ?? o_plus_days( o_add_months( $start, $months ), -1 );
	$rent = $o['rent'] ?? 100 * $R->i( 38, 95 );
	$pay_day = $o['pay_day'] ?? ( '01' === substr( $start, 8 ) ? $R->pick( array( 1, 1, 1, 5, 10 ) ) : min( 28, (int) substr( $start, 8 ) ) );
	$link = $o['link'] ?? ( $R->p( 0.5 ) ? array( 'mode' => 'cpi', 'every' => $R->pick( array( 12, 12, 6, 3 ) ), 'pct' => $R->pick( array( 100, 100, 50 ) ), 'floor' => $R->p( 0.7 ) ) : array( 'mode' => 'none', 'every' => 12, 'pct' => 100, 'floor' => true ) );
	$link['base_date'] = $start;
	$behavior = $o['behavior'] ?? $R->pick( array( 'good', 'good', 'good', 'good', 'late', 'partial', 'cheque', 'cheque', 'standing', 'bad' ) );
	$terms = array( 'method' => 'cheque' === $behavior ? 'cheque' : 'transfer' );
	if ( ! empty( $o['track_from'] ) ) { $terms['track_from'] = $o['track_from']; }
	$data = array( 'unit_id' => $uid, 'status' => 'active', 'start_date' => $start, 'end_date' => $end, 'rent' => $rent, 'pay_day' => $pay_day, 'linkage' => $link, 'securities' => array(), 'parties' => array( 'tenants' => array( $c['id'] ) ), 'terms' => $terms );
	if ( $W['owners'][ $oid ]['rest'] ) {
		$res = sim_rest( '/rm/save', array( 'entity' => 'lease', 'data' => $data, 'client_ref' => 'L' . $W['phone'] ) );
		check( 'rest.lease_pack', ! is_wp_error( $res ) && isset( $res['money'], $res['rows'] ) );
		$l = $res['row'];
	} else {
		$l = nlrm_save( 'lease', $data, $oid );
		nlrm_rent_run( $oid, null, $l['id'] );
	}
	$L = array( 'id' => $l['id'], 'owner' => $oid, 'unit' => $uid, 'tenant' => $c['id'], 'lang' => $lang, 'start' => $start, 'end' => $end, 'end_eff' => null, 'rent' => $rent,
		'pay_day' => $pay_day, 'link' => $link, 'track_from' => $o['track_from'] ?? null, 'behavior' => $behavior, 'next' => 0, 'credits' => 0, 'fees' => 0, 'refunds' => 0,
		'dep' => 0, 'status' => 'active', 'stop_k' => 'bad' === $behavior ? $R->i( 3, 18 ) : 999, 'pays' => array(), 'evict' => null, 'ip' => '10.0.' . intdiv( $W['ip'], 250 ) . '.' . ( $W['ip']++ % 250 + 1 ), 'decided' => false, 'early' => null, 'cheques' => array() );
	$W['leases'][ $l['id'] ] = $L;
	$W['units'][ $uid ]['lease'] = $l['id'];
	$W['units'][ $uid ]['vacant_since'] = null;
	/* the tenant's personal link (lives until the lease end + 60 days) */
	as_owner( $oid );
	$lk = sim_rest( '/rm/link', array( 'purpose' => 'tenant', 'scope' => 'lease', 'scope_id' => $l['id'], 'contact_id' => $c['id'] ) );
	$W['leases'][ $l['id'] ]['token'] = is_array( $lk ) ? substr( $lk['url'], strpos( $lk['url'], '=', strpos( $lk['url'], '#' ) ) + 1 ) : null;
	check( 'link.lasts_lease', is_array( $lk ) && $lk['expires_at'] >= o_plus_days( $end, 59 ), is_array( $lk ) ? $lk['expires_at'] . ' vs ' . $end : 'err' );
	/* a cash deposit (60%), never above the legal cap */
	if ( $R->p( 0.6 ) ) {
		$cap_months = max( 1, (int) round( o_days( $start, o_plus_days( $end, 1 ) ) / 30.44 ) );
		$cap = min( 3 * $rent * 100, (int) floor( $cap_months * $rent * 100 / 3 ) );
		if ( $R->p( 0.08 ) ) {
			$try = nlrm_deposit( $oid, $l['id'], 'receive', array( 'amount' => 4 * $rent, 'date' => $start ), null );
			check( 'deposit.cap_refused', is_wp_error( $try ) && 'nlrm_cap' === $try->code );
			count_ev( 'deposit_over_cap_refused' );
		}
		$amt = min( $cap, $R->i( 1, 3 ) * $rent * 100 );
		$d = nlrm_deposit( $oid, $l['id'], 'receive', array( 'amount' => $amt / 100, 'date' => $start, 'method' => 'transfer' ), 'cref:dep' . $l['id'] );
		if ( check( 'deposit.receive', ! is_wp_error( $d ), is_wp_error( $d ) ? $d->message : '' ) ) {
			$W['leases'][ $l['id'] ]['dep'] += $amt;
			$W['tally']['cash_in'] += $amt;
		}
	}
	/* post-dated cheques for the whole term (base rent) */
	if ( 'cheque' === $behavior ) {
		foreach ( o_periods( array_merge( $W['leases'][ $l['id'] ], array( 'link' => array( 'mode' => 'none' ) ) ), $end ) as $ym => $p ) {
			$ch = nlrm_pay( $oid, array( 'lease_id' => $l['id'], 'amount' => $p['amount'] / 100, 'paid_date' => $p['due'], 'method' => 'cheque', 'ref' => (string) ( 10000 + $W['pays'] ) ), 'cref:chq' . $l['id'] . $ym );
			$W['pays']++;
			if ( is_wp_error( $ch ) ) { check( 'cheque.record', false, $ch->message ); continue; }
			$W['leases'][ $l['id'] ]['cheques'][ $ym ] = array( 'id' => $ch['id'], 'amount' => $p['amount'], 'due' => $p['due'], 'st' => $ch['status'] );
			if ( 'deposited' === $ch['status'] || 'paid' === $ch['status'] ) { $W['leases'][ $l['id'] ]['credits'] += $p['amount']; $W['tally']['cash_in'] += $p['amount']; $W['tally']['income'] += $p['amount']; }
		}
	}
	count_ev( 'move_in' );
	return $l['id'];
}

/* ---------- money from tenants (each also feeds the oracle) ---------- */
function pay( $lid, $amount_ag, $method = 'transfer', $how = 'app' ) {
	global $W, $R;
	$L = &$W['leases'][ $lid ];
	$oid = $L['owner'];
	as_owner( $oid );
	$W['pays']++;
	$cref = 'p' . $W['pays'];
	$data = array( 'lease_id' => $lid, 'amount' => $amount_ag / 100, 'paid_date' => today(), 'method' => $method );
	if ( 'portal' === $how && ! empty( $L['token'] ) ) {
		$_SERVER['HTTP_X_NLRM_LINK'] = $L['token'];
		$_SERVER['REMOTE_ADDR'] = $L['ip'];
		$link = nlrm_link_from_request( array( 'tenant' ) );
		if ( ! check( 'portal.link_valid', (bool) $link, 'lease ' . $lid ) ) { $how = 'app'; }
		else {
			$res = nlrm_portal_act( $link, new WP_REST_Request( array( 'act' => 'paid', 'data' => array( 'amount' => $amount_ag / 100, 'date' => today(), 'method' => $method, 'ref' => 'T' . $W['pays'] ), 'client_ref' => $cref ) ) );
			/* the tenant taps twice */
			$again = nlrm_portal_act( $link, new WP_REST_Request( array( 'act' => 'paid', 'data' => array( 'amount' => $amount_ag / 100, 'date' => today(), 'method' => $method, 'ref' => 'T' . $W['pays'] ), 'client_ref' => $cref ) ) );
			check( 'portal.report_once', ! is_wp_error( $res ) && ! is_wp_error( $again ) && $res['payment']['id'] === $again['payment']['id'] );
			check( 'portal.report_pending', ! is_wp_error( $res ) && 'pending' === $res['payment']['status'] );
			$pid = is_wp_error( $res ) ? 0 : $res['payment']['id'];
			$W['tally']['cash_in'] += $amount_ag;
			/* the landlord confirms it in 1-3 days */
			q_add( o_plus_days( today(), $R->i( 1, 3 ) ), function () use ( $lid, $pid, $amount_ag ) {
				global $W;
				as_owner( $W['leases'][ $lid ]['owner'] );
				$r = nlrm_ledger_act( $W['leases'][ $lid ]['owner'], $pid, 'confirm', array() );
				if ( check( 'portal.confirm', ! is_wp_error( $r ) && 'paid' === $r['status'] ) ) {
					$W['leases'][ $lid ]['credits'] += $amount_ag;
					$W['tally']['income'] += $amount_ag;
				}
			} );
			count_ev( 'portal_reports' );
			return;
		}
	}
	if ( $W['owners'][ $oid ]['rest'] ) {
		$res = sim_rest( '/rm/pay', array( 'data' => $data, 'client_ref' => $cref ) );
		if ( 0 === $W['pays'] % 37 ) {
			$dup = sim_rest( '/rm/pay', array( 'data' => $data, 'client_ref' => $cref ) );
			check( 'rest.pay_retry_once', ! is_wp_error( $res ) && ! is_wp_error( $dup ) && $res['row']['id'] === $dup['row']['id'] );
			count_ev( 'retries_replayed' );
		}
		$row = is_wp_error( $res ) ? $res : $res['row'];
	} else {
		$row = nlrm_pay( $oid, $data, 'cref:' . $cref );
	}
	if ( check( 'pay.recorded', ! is_wp_error( $row ) && 'paid' === $row['status'], is_wp_error( $row ) ? $row->message : '' ) ) {
		$L['credits'] += $amount_ag;
		$W['tally']['cash_in'] += $amount_ag;
		$W['tally']['income'] += $amount_ag;
	}
}

/* ---------- each day ---------- */
function oracle_due_periods( $L ) { return o_periods( $L, o_month_end( today() ) ); }

function lease_day( $lid ) {
	global $W, $R;
	$L = &$W['leases'][ $lid ];
	$t = today();
	if ( 'active' !== $L['status'] ) {
		/* an ended lease's last cheques are still deposited */
		if ( 'cheque' === $L['behavior'] ) { deposit_cheques( $lid ); }
		return;
	}
	/* schedule the tenant's payment for each period that becomes due today */
	foreach ( o_periods( $L, $t ) as $ym => $p ) {
		if ( $p['k'] < $L['next'] ) { continue; }
		$L['next'] = $p['k'] + 1;
		$amt = $p['amount'];
		$beh = $L['behavior'];
		if ( 'bad' === $beh && $p['k'] >= $L['stop_k'] ) { continue; }
		if ( 'cheque' === $beh ) {
			$ch = $L['cheques'][ $ym ] ?? null;
			$diff = $amt - ( $ch ? $ch['amount'] : 0 );
			if ( $diff > 0 ) { q_add( o_plus_days( $p['due'] > $t ? $p['due'] : $t, $R->i( 1, 10 ) ), function () use ( $lid, $diff ) { pay( $lid, $diff, 'transfer' ); } ); }
			continue;
		}
		$when = $p['due'] > $t ? $p['due'] : $t;
		if ( 'good' === $beh || 'bad' === $beh ) {
			$how = $R->p( 0.2 ) ? 'portal' : 'app';
			$m = $R->pick( array( 'transfer', 'transfer', 'bit', 'paybox' ) );
			q_add( o_plus_days( $when, $R->i( 0, 3 ) ), function () use ( $lid, $amt, $m, $how ) { pay( $lid, $amt, $m, $how ); } );
		} elseif ( 'standing' === $beh ) {
			q_add( $when, function () use ( $lid, $amt ) { pay( $lid, $amt, 'standing' ); } );
		} elseif ( 'late' === $beh ) {
			q_add( o_plus_days( $when, $R->i( 5, 40 ) ), function () use ( $lid, $amt ) { pay( $lid, $amt, 'transfer' ); } );
		} elseif ( 'partial' === $beh ) {
			$part = (int) round( $amt * $R->i( 50, 90 ) / 100 );
			q_add( o_plus_days( $when, $R->i( 0, 5 ) ), function () use ( $lid, $part ) { pay( $lid, $part, 'bit' ); } );
			q_add( o_plus_days( $when, $R->i( 15, 45 ) ), function () use ( $lid, $amt, $part ) { pay( $lid, $amt - $part, 'transfer' ); } );
		}
	}
	if ( 'cheque' === $L['behavior'] ) { deposit_cheques( $lid ); }
	lease_after( $lid );
}
/* cheques: deposited on their date (or a day or two later); 3% bounce */
function deposit_cheques( $lid ) {
	global $W, $R;
	$L = &$W['leases'][ $lid ];
	$t = today();
	{
		foreach ( $L['cheques'] as $ym => &$c ) {
			if ( 'pending' !== $c['st'] || $c['due'] > $t ) { continue; }
			if ( $R->p( 0.4 ) && $c['due'] < $t ) { /* deposited today */ } elseif ( $c['due'] === $t && $R->p( 0.5 ) ) { continue; }
			as_owner( $L['owner'] );
			$r = nlrm_ledger_act( $L['owner'], $c['id'], 'deposit', array( 'date' => $t ) );
			if ( ! check( 'cheque.deposit', ! is_wp_error( $r ) && 'deposited' === $r['status'] ) ) { continue; }
			$c['st'] = 'deposited';
			$L['credits'] += $c['amount'];
			$W['tally']['cash_in'] += $c['amount'];
			$W['tally']['income'] += $c['amount'];
			if ( $R->p( 0.03 ) ) {
				$amtc = $c['amount'];
				$cid = $c['id'];
				q_add( o_plus_days( $t, $R->i( 2, 4 ) ), function () use ( $lid, $cid, $amtc, $ym ) {
					global $W, $R;
					$L = &$W['leases'][ $lid ];
					as_owner( $L['owner'] );
					$b = nlrm_ledger_act( $L['owner'], $cid, 'bounce', array( 'fee' => 25 ) );
					if ( check( 'cheque.bounce', ! is_wp_error( $b ) && 'bounced' === $b['status'] ) ) {
						$L['cheques'][ $ym ]['st'] = 'bounced';
						$L['credits'] -= $amtc;
						$L['fees'] += 2500;
						$W['tally']['cash_in'] -= $amtc;
						$W['tally']['income'] -= $amtc;
						count_ev( 'cheques_bounced' );
						/* the tenant pays it again, with the fee */
						q_add( o_plus_days( today(), $R->i( 3, 10 ) ), function () use ( $lid, $amtc ) { pay( $lid, $amtc + 2500, 'transfer' ); } );
					}
				} );
			}
		}
		unset( $c );
	}
}
function lease_after( $lid ) {
	global $W, $R;
	$L = &$W['leases'][ $lid ];
	$t = today();
	/* a bad payer: when two months are owed the eviction starts */
	if ( 'bad' === $L['behavior'] && 'active' === $L['status'] && ! $L['evict'] ) {
		$m = nlrm_money( $L['owner'], $t, array( $lid ) );
		if ( ( $m[ $lid ]['balance'] ?? 0 ) >= 2 * $L['rent'] * 100 ) {
			$L['evict'] = o_plus_days( $t, $R->i( 60, 150 ) );
			count_ev( 'evictions_started' );
		}
	}
	if ( $L['evict'] && $L['evict'] === $t && 'active' === $L['status'] ) { evict( $lid ); }
	/* an early exit agreed with the tenant (4% of leases) */
	if ( 'active' === $L['status'] && $L['early'] === $t ) { leave( $lid, $t, 'early' ); return; }
	/* the end of the term: renew (55%) or leave */
	if ( 'active' === $L['status'] && ! $L['decided'] && $t >= o_plus_days( $L['end'], -45 ) && 'bad' !== $L['behavior'] ) {
		$L['decided'] = $R->p( 0.55 ) ? 'renew' : 'leave';
	}
	if ( 'active' === $L['status'] && 'renew' === $L['decided'] && $t === o_plus_days( $L['end'], -20 ) ) { renew( $lid ); return; }
	if ( 'active' === $L['status'] && $t === $L['end'] && 'renew' !== $L['decided'] && ! $L['evict'] ) { leave( $lid, $t, 'term' ); return; }
}

function settle_deposit_later( $lid, $end ) {
	global $W, $R;
	$L = $W['leases'][ $lid ];
	if ( $L['dep'] <= 0 ) { return; }
	$day = o_plus_days( $end, $R->i( 10, 55 ) );
	q_add( $day, function () use ( $lid, $end ) {
		global $W, $R;
		$L = &$W['leases'][ $lid ];
		as_owner( $L['owner'] );
		$m = nlrm_money( $L['owner'], today(), array( $lid ) );
		check( 'deposit.held_matches', ( $m[ $lid ]['deposit_held'] ?? 0 ) === $L['dep'], ( $m[ $lid ]['deposit_held'] ?? 0 ) . ' vs ' . $L['dep'] );
		/* first what the tenant still owes, then damage (30%), then the rest back */
		$owe = max( 0, $m[ $lid ]['balance'] ?? 0 );
		if ( $owe > 0 ) {
			$use = min( $owe, $L['dep'] );
			$a = nlrm_deposit( $L['owner'], $lid, 'apply', array( 'amount' => $use / 100, 'category' => 'rent', 'note' => 'unpaid rent' ), 'cref:da' . $lid );
			if ( check( 'deposit.apply_debt', ! is_wp_error( $a ) ) ) { $L['dep'] -= $use; $L['credits'] += $use; $W['tally']['income'] += $use; count_ev( 'deposit_applied_to_debt' ); }
		}
		if ( $L['dep'] > 0 && $R->p( 0.3 ) ) {
			$dmg = min( $L['dep'], 100 * $R->i( 3, 25 ) * 100 / 100 );
			/* the damage is charged, then paid from the deposit */
			$ch = nlrm_book( $L['owner'], array( 'kind' => 'charge', 'lease_id' => $lid, 'category' => 'repair', 'amount' => $dmg, 'due_date' => today(), 'note' => 'damage' ), 'cref:dc' . $lid );
			$a = nlrm_deposit( $L['owner'], $lid, 'apply', array( 'amount' => $dmg / 100, 'category' => 'repair', 'note' => 'damage' ), 'cref:dd' . $lid );
			if ( check( 'deposit.damage', ! is_wp_error( $ch ) && ! is_wp_error( $a ) ) ) { $L['fees'] += $dmg; $L['dep'] -= $dmg; $L['credits'] += $dmg; $W['tally']['income'] += $dmg; count_ev( 'deposit_damage_deductions' ); }
		}
		if ( $L['dep'] > 0 ) {
			$r = nlrm_deposit( $L['owner'], $lid, 'return', array( 'amount' => $L['dep'] / 100, 'method' => 'transfer' ), 'cref:dr' . $lid );
			if ( check( 'deposit.return', ! is_wp_error( $r ) ) ) { $W['tally']['cash_out'] += $L['dep']; $L['dep'] = 0; count_ev( 'deposits_returned' ); }
		}
		check( 'deposit.within_60_days', o_days( $end, today() ) <= 60 );
		$m = nlrm_money( $L['owner'], today(), array( $lid ) );
		check( 'deposit.zero_after_return', 0 === ( $m[ $lid ]['deposit_held'] ?? -1 ), (string) ( $m[ $lid ]['deposit_held'] ?? 'x' ) );
	} );
}

function leave( $lid, $date, $reason ) {
	global $W, $R;
	$L = &$W['leases'][ $lid ];
	as_owner( $L['owner'] );
	$pre = $W['owners'][ $L['owner'] ]['rest'] ? sim_rest( '/rm/lease-end', array( 'lease_id' => $lid, 'data' => array( 'date' => $date, 'reason' => $reason ) ) ) : nlrm_lease_end( $L['owner'], $lid, array( 'date' => $date, 'reason' => $reason ) );
	if ( ! check( 'lease.end', ! is_wp_error( $pre ), is_wp_error( $pre ) ? $pre->message : '' ) ) { return; }
	$L['status'] = 'ended';
	$L['end_eff'] = $date;
	/* cheques for periods after the end go back to the tenant (voided) */
	foreach ( $L['cheques'] as $ym => &$c ) {
		if ( 'pending' === $c['st'] && $c['due'] > $date ) {
			$v = nlrm_ledger_act( $L['owner'], $c['id'], 'void', array( 'reason' => 'returned to the tenant' ) );
			if ( check( 'cheque.return_void', ! is_wp_error( $v ) ) ) { $c['st'] = 'void'; }
		}
	}
	unset( $c );
	count_ev( 'leases_ended_' . $reason );
	/* a credit (a whole cheque for a part month) goes back to the tenant */
	q_add( o_plus_days( $date, $R->i( 3, 9 ) ), function () use ( $lid ) {
		global $W;
		$L = &$W['leases'][ $lid ];
		as_owner( $L['owner'] );
		$m = nlrm_money( $L['owner'], today(), array( $lid ) );
		$credit = -( $m[ $lid ]['balance'] ?? 0 ) - ( $m[ $lid ]['future'] ?? 0 );
		if ( $credit > 0 ) {
			$r = nlrm_refund_credit( $L['owner'], $lid, array( 'amount' => $credit / 100 ), 'cref:rc' . $lid );
			if ( check( 'refund.credit', ! is_wp_error( $r ) ) ) { $L['refunds'] += $credit; $W['tally']['cash_out'] += $credit; $W['tally']['income'] -= $credit; count_ev( 'credits_refunded' ); }
		}
	} );
	settle_deposit_later( $lid, $date );
	/* vacancy, then the next tenant */
	$uid = $L['unit'];
	$W['units'][ $uid ]['lease'] = 0;
	$W['units'][ $uid ]['vacant_since'] = $date;
	$next = o_plus_days( $date, $R->i( 1, 90 ) );
	$r = $R->f();
	if ( $r < 0.7 ) { $next = o_add_months( substr( $next, 0, 8 ) . '01', 1 ); } elseif ( $r < 0.85 ) { $next = substr( $next, 0, 8 ) . '15'; }
	$oid = $L['owner'];
	$rent = (int) ( $L['rent'] * ( 1 + $R->i( -3, 8 ) / 100 ) );
	q_add( $next, function () use ( $oid, $uid, $next, $rent ) { move_in( $oid, $uid, $next, array( 'rent' => $rent ) ); } );
}

function renew( $lid ) {
	global $W, $R;
	$L = &$W['leases'][ $lid ];
	as_owner( $L['owner'] );
	$months = $R->pick( array( 12, 12, 24 ) );
	$start = o_plus_days( $L['end'], 1 );
	$end = o_plus_days( o_add_months( $start, $months ), -1 );
	$rent = 'cpi' === $L['link']['mode'] ? $L['rent'] : (int) round( $L['rent'] * ( 1 + $R->i( -2, 6 ) / 100 ) );
	$args = array( 'start_date' => $start, 'end_date' => $end, 'rent' => $rent );
	$res = $W['owners'][ $L['owner'] ]['rest'] ? sim_rest( '/rm/lease-renew', array( 'lease_id' => $lid, 'data' => $args, 'client_ref' => 'R' . $lid ) ) : nlrm_lease_renew( $L['owner'], $lid, $args, 'cref:R' . $lid );
	if ( ! check( 'lease.renew', ! is_wp_error( $res ), is_wp_error( $res ) ? $res->message : '' ) ) { return; }
	$new = isset( $res['lease'] ) ? $res['lease'] : $res;
	$nid = (int) $new['id'];
	check( 'renew.new_lease_active', 'active' === $new['status'] && $new['start_date'] === $start );
	$old = $L;
	$L['status'] = 'ended';
	$L['end_eff'] = $L['end'];
	$NL = $old;
	$NL['id'] = $nid; $NL['start'] = $start; $NL['end'] = $end; $NL['end_eff'] = null; $NL['rent'] = $rent; $NL['next'] = 0; $NL['credits'] = 0; $NL['fees'] = 0; $NL['refunds'] = 0;
	$NL['link']['base_date'] = $start; $NL['track_from'] = null; $NL['decided'] = false; $NL['cheques'] = array(); $NL['status'] = 'active';
	/* the deposit moved with the tenant */
	$NL['dep'] = $old['dep'];
	$L['dep'] = 0;
	/* the old lease may still owe or be owed; its books stay with it */
	$W['leases'][ $nid ] = $NL;
	$W['units'][ $L['unit'] ]['lease'] = $nid;
	/* new cheques for a cheque payer */
	if ( 'cheque' === $NL['behavior'] ) {
		foreach ( o_periods( array_merge( $NL, array( 'link' => array( 'mode' => 'none' ) ) ), $end ) as $ym => $p ) {
			$ch = nlrm_pay( $NL['owner'], array( 'lease_id' => $nid, 'amount' => $p['amount'] / 100, 'paid_date' => $p['due'], 'method' => 'cheque', 'ref' => (string) ( 10000 + $W['pays']++ ) ), 'cref:chq' . $nid . $ym );
			if ( ! is_wp_error( $ch ) ) { $W['leases'][ $nid ]['cheques'][ $ym ] = array( 'id' => $ch['id'], 'amount' => $p['amount'], 'due' => $p['due'], 'st' => $ch['status'] ); }
		}
	}
	$lk = sim_rest( '/rm/link', array( 'purpose' => 'tenant', 'scope' => 'lease', 'scope_id' => $nid, 'contact_id' => $NL['tenant'] ) );
	$W['leases'][ $nid ]['token'] = is_array( $lk ) ? substr( $lk['url'], strpos( $lk['url'], '=', strpos( $lk['url'], '#' ) ) + 1 ) : null;
	count_ev( 'renewals' );
	if ( $R->p( 0.04 ) ) { $W['leases'][ $nid ]['early'] = o_plus_days( $start, $R->i( 60, max( 61, o_days( $start, $end ) - 30 ) ) ); }
}

function evict( $lid ) {
	global $W, $R;
	$L = &$W['leases'][ $lid ];
	$t = today();
	as_owner( $L['owner'] );
	$res = nlrm_lease_end( $L['owner'], $lid, array( 'date' => $t, 'reason' => 'eviction' ) );
	if ( ! check( 'eviction.end', ! is_wp_error( $res ), is_wp_error( $res ) ? $res->message : '' ) ) { return; }
	check( 'eviction.overstay_charged', $res['end_date'] === $t, $res['end_date'] . ' vs ' . $t );
	$L['status'] = 'ended';
	$L['end_eff'] = $t;
	count_ev( 'evictions' );
	settle_deposit_later( $lid, $t );
	/* a guarantor pays part (40%), the rest is written off after 6 months */
	if ( $R->p( 0.4 ) ) {
		q_add( o_plus_days( $t, $R->i( 70, 120 ) ), function () use ( $lid ) {
			global $W, $R;
			$L = $W['leases'][ $lid ];
			$m = nlrm_money( $L['owner'], today(), array( $lid ) );
			$bal = $m[ $lid ]['balance'] ?? 0;
			if ( $bal > 0 ) { pay( $lid, (int) round( $bal * $R->i( 30, 80 ) / 100 ), 'transfer' ); count_ev( 'guarantor_payments' ); }
		} );
	}
	q_add( o_plus_days( $t, 180 ), function () use ( $lid ) {
		global $W;
		$L = &$W['leases'][ $lid ];
		as_owner( $L['owner'] );
		$m = nlrm_money( $L['owner'], today(), array( $lid ) );
		$bal = $m[ $lid ]['balance'] ?? 0;
		if ( $bal > 0 ) {
			$w = nlrm_writeoff( $L['owner'], $lid, array( 'note' => 'after eviction' ), 'cref:wo' . $lid );
			if ( check( 'writeoff', ! is_wp_error( $w ) ) ) { $L['credits'] += $bal; count_ev( 'writeoffs' ); count_ev( 'writeoff_agorot', $bal ); }
			$m = nlrm_money( $L['owner'], today(), array( $lid ) );
			check( 'writeoff.closes_balance', 0 === ( $m[ $lid ]['balance'] ?? -1 ) );
		}
	} );
	$uid = $L['unit'];
	$W['units'][ $uid ]['lease'] = 0;
	$W['units'][ $uid ]['vacant_since'] = $t;
	$oid = $L['owner'];
	$next = o_add_months( substr( o_plus_days( $t, $R->i( 20, 60 ) ), 0, 8 ) . '01', 1 );
	$rent = $L['rent'];
	q_add( $next, function () use ( $oid, $uid, $next, $rent ) { move_in( $oid, $uid, $next, array( 'rent' => $rent ) ); } );
}

/* ---------- repairs and vendors (Fair Rental Law §25ח: 3 days urgent, 30 days otherwise) ---------- */
$TK = array(
	array( 'אין מים חמים בכלל', 'urgent' ), array( 'No hot water at all', 'urgent' ), array( 'טפטוף בברז המטבח', 'standard' ), array( 'מזגן לא מקרר', 'standard' ),
	array( 'דליפת מים מהתקרה', 'urgent' ), array( 'the AC is noisy', 'standard' ), array( 'Не работает розетка в спальне', 'standard' ), array( 'הדלת לא ננעלת', 'urgent' ),
);
function repairs_day( $oid ) {
	global $W, $R, $TK;
	foreach ( $W['owners'][ $oid ]['units'] as $uid ) {
		if ( ! $R->p( 0.0015 ) ) { continue; }
		$tk = $R->pick( $TK );
		$lid = $W['units'][ $uid ]['lease'];
		as_owner( $oid );
		if ( $lid && ! empty( $W['leases'][ $lid ]['token'] ) && $R->p( 0.6 ) ) {
			$_SERVER['HTTP_X_NLRM_LINK'] = $W['leases'][ $lid ]['token'];
			$_SERVER['REMOTE_ADDR'] = $W['leases'][ $lid ]['ip'];
			$link = nlrm_link_from_request( array( 'tenant' ) );
			if ( ! $link ) { check( 'portal.link_valid', false, 'repair ' . $lid ); continue; }
			$res = nlrm_portal_act( $link, new WP_REST_Request( array( 'act' => 'ticket', 'data' => array( 'title' => $tk[0], 'body' => 'sim' ) ) ) );
			$t = is_wp_error( $res ) ? $res : $res['ticket'];
		} else {
			$urg = nlrm_triage( $tk[0] )['urgency'];
			$t = nlrm_save( 'ticket', array( 'property_id' => $W['units'][ $uid ]['prop'], 'unit_id' => $uid, 'title' => $tk[0], 'body' => 'sim', 'urgency' => $urg, 'status' => 'new', 'reporter' => 'owner', 'due_by' => nlrm_add_days( today(), 'urgent' === $urg ? 3 : 30 ) ), $oid );
		}
		if ( ! check( 'ticket.open', ! is_wp_error( $t ) ) ) { continue; }
		check( 'ticket.triage', $t['urgency'] === $tk[1], $tk[0] . ' -> ' . $t['urgency'] );
		check( 'ticket.legal_timer', $t['due_by'] === o_plus_days( today(), 'urgent' === $t['urgency'] ? 3 : 30 ), $t['due_by'] );
		$fix = 'urgent' === $t['urgency'] ? $R->i( 0, 4 ) : $R->i( 2, 35 );
		$tid = $t['id'];
		$cost = 100 * $R->i( 2, 30 );
		$W['tickets'][ $tid ] = array( 'due' => $t['due_by'], 'owner' => $oid );
		q_add( o_plus_days( today(), $fix ), function () use ( $tid, $oid, $cost, $uid ) {
			global $W;
			as_owner( $oid );
			$v = nlrm_save( 'ticket', array( 'id' => $tid, 'status' => 'done', 'cost' => $cost / 100 ), $oid );
			if ( ! check( 'ticket.close', ! is_wp_error( $v ) && 'done' === $v['status'] && $v['closed_at'] ) ) { return; }
			$late = today() > $W['tickets'][ $tid ]['due'];
			count_ev( $late ? 'repairs_late' : 'repairs_on_time' );
			$e = nlrm_book( $oid, array( 'kind' => 'expense', 'unit_id' => $uid, 'category' => 'repair', 'amount' => $cost, 'paid_date' => today(), 'note' => 'ticket ' . $tid ), 'cref:tk' . $tid );
			if ( check( 'expense.repair', ! is_wp_error( $e ) ) ) { $W['tally']['expense'] += $cost; }
		} );
		count_ev( 'repairs' );
	}
}
function expenses_day( $oid ) {
	global $W, $R;
	$t = today();
	if ( '01' !== substr( $t, 8 ) ) { return; }
	as_owner( $oid );
	foreach ( $W['owners'][ $oid ]['props'] as $i => $pid ) {
		$vaad = 100 * ( 2 + $i % 4 ) * 100;
		$e = nlrm_book( $oid, array( 'kind' => 'expense', 'property_id' => $pid, 'category' => 'vaad', 'amount' => $vaad, 'paid_date' => $t ), 'cref:v' . $pid . $t );
		if ( ! is_wp_error( $e ) ) { $W['tally']['expense'] += $vaad; }
		if ( (int) substr( $t, 5, 2 ) === 1 + $i % 12 ) {
			$ins = 100 * ( 900 + 50 * $i );
			$e = nlrm_book( $oid, array( 'kind' => 'expense', 'property_id' => $pid, 'category' => 'insurance', 'amount' => $ins, 'paid_date' => $t ), 'cref:i' . $pid . $t );
			if ( ! is_wp_error( $e ) ) { $W['tally']['expense'] += $ins; }
		}
	}
	/* municipal tax while an apartment is empty (every second month) */
	if ( 1 === (int) substr( $t, 5, 2 ) % 2 ) {
		foreach ( $W['owners'][ $oid ]['units'] as $uid ) {
			if ( $W['units'][ $uid ]['lease'] ) { continue; }
			$e = nlrm_book( $oid, array( 'kind' => 'expense', 'unit_id' => $uid, 'category' => 'arnona', 'amount' => 52000, 'paid_date' => $t ), 'cref:a' . $uid . $t );
			if ( ! is_wp_error( $e ) ) { $W['tally']['expense'] += 52000; count_ev( 'arnona_vacant' ); }
		}
	}
}

/* ---------- the month-end audit: engine vs oracle, to the agora ---------- */
function audit( $oid, $deep = false ) {
	global $W, $wpdb;
	$t = today();
	$states = array();
	$money = nlrm_money( $oid, $t, null, $states );
	foreach ( $W['leases'] as $lid => $L ) {
		if ( $L['owner'] !== $oid ) { continue; }
		$per = oracle_due_periods( $L );
		$due = 0;
		foreach ( $per as $p ) { if ( $p['due'] <= $t ) { $due += $p['amount']; } }
		$fees = $L['fees'];
		$exp_bal = $due + $fees - $L['credits'] + $L['refunds'];
		$m = $money[ $lid ] ?? array( 'balance' => 0, 'deposit_held' => 0 );
		/* a line still waiting for the index is excused this month only */
		$pend = (int) $wpdb->get_var( $wpdb->prepare( "SELECT COUNT(*) FROM wp_nlrm_ledger WHERE owner_id = %d AND lease_id = %d AND note LIKE 'cpi?%%' AND status <> 'void'", $oid, $lid ) );
		if ( $pend ) { count_ev( 'audits_waiting_for_cpi' ); continue; }
		check( 'books.balance_to_agora', $m['balance'] === $exp_bal, "lease $lid engine {$m['balance']} oracle $exp_bal (due $due fees $fees credits {$L['credits']} refunds {$L['refunds']})" );
		check( 'books.deposit_held', $m['deposit_held'] === $L['dep'], "lease $lid engine {$m['deposit_held']} oracle {$L['dep']}" );
		if ( $deep ) {
			/* each period: exactly one live line (or a line and its CPI difference) and the right amount */
			$rows = $wpdb->get_results( $wpdb->prepare( "SELECT id, auto_key, amount FROM wp_nlrm_ledger WHERE owner_id = %d AND lease_id = %d AND kind = 'charge' AND category = 'rent' AND status <> 'void'", $oid, $lid ), ARRAY_A );
			$by = array(); $idym = array();
			foreach ( $rows as $r ) {
				if ( preg_match( '/^rent:\d+:(\d{4}-\d{2})/', $r['auto_key'], $mm ) ) { $by[ $mm[1] ][] = (int) $r['amount']; $idym[ (int) $r['id'] ] = $mm[1]; }
			}
			foreach ( $rows as $r ) { if ( preg_match( '/^cpiadj:(\d+)$/', $r['auto_key'], $mm ) && isset( $idym[ (int) $mm[1] ] ) ) { $by[ $idym[ (int) $mm[1] ] ][] = (int) $r['amount']; } }
			foreach ( $per as $ym => $p ) {
				$lines = $by[ $ym ] ?? array();
				check( 'books.one_charge_per_period', count( array_filter( $lines, function ( $a ) { return true; } ) ) >= 1 && count( $lines ) <= 2, "lease $lid $ym lines " . count( $lines ) );
				check( 'books.period_amount', array_sum( $lines ) === $p['amount'], "lease $lid $ym engine " . array_sum( $lines ) . ' oracle ' . $p['amount'] . ( $p['partial'] ? ' partial' : '' ) );
				unset( $by[ $ym ] );
			}
			check( 'books.no_extra_periods', ! $by, "lease $lid extra " . implode( ',', array_keys( $by ) ) );
		}
	}
	/* the cash the tenants handed over equals the books' cash lines */
	/* cash = recorded money, plus tenants' reports not yet confirmed (the money did move); a post-dated cheque is not cash until deposited */
	$in = (int) $wpdb->get_var( $wpdb->prepare( "SELECT COALESCE(SUM(amount),0) FROM wp_nlrm_ledger WHERE owner_id = %d AND kind = 'payment' AND (status IN ('paid','deposited') OR (status = 'pending' AND method <> 'cheque')) AND method NOT IN ('deposit','writeoff','renewal')", $oid ) );
	$out = (int) $wpdb->get_var( $wpdb->prepare( "SELECT COALESCE(SUM(amount),0) FROM wp_nlrm_ledger WHERE owner_id = %d AND kind = 'refund' AND status <> 'void' AND method <> 'renewal'", $oid ) );
	$GLOBALS['W']['books_cash'][ $oid ] = array( $in, $out );
}
function audit_cash() {
	global $W;
	$in = 0; $out = 0;
	foreach ( $W['books_cash'] ?? array() as $x ) { $in += $x[0]; $out += $x[1]; }
	check( 'books.cash_in_equals_tenants_paid', $in === $W['tally']['cash_in'], "books $in tenants {$W['tally']['cash_in']}" );
	check( 'books.cash_out_equals_refunds', $out === $W['tally']['cash_out'], "books $out refunds {$W['tally']['cash_out']}" );
}
function audit_stats() {
	global $W;
	$inc = 0; $exp = 0;
	foreach ( array_keys( $W['owners'] ) as $oid ) {
		foreach ( nlrm_stats( $oid, '2000-01-01' ) as $ym => $s ) { $inc += $s['income']; $exp += $s['expense']; }
	}
	check( 'reports.income_equals_oracle', $inc === $W['tally']['income'], "stats $inc oracle {$W['tally']['income']}" );
	check( 'reports.expense_equals_oracle', $exp === $W['tally']['expense'], "stats $exp oracle {$W['tally']['expense']}" );
}
function perf( $label ) {
	global $W, $wpdb;
	$big = 4;
	as_owner( $big );
	$q0 = $wpdb->queries; $t0 = microtime( true );
	$b = sim_rest( '/rm/boot' );
	$t1 = microtime( true );
	delete_transient( 'nlrm_ran_' . $big );
	$t2 = microtime( true );
	$made = nlrm_rent_run( $big );
	$t3 = microtime( true );
	nlrm_money( $big );
	$t4 = microtime( true );
	$json = json_encode( $b, JSON_UNESCAPED_UNICODE );
	$GLOBALS['M']['perf'][ $label ] = array( 'boot_ms' => round( ( $t1 - $t0 ) * 1000 ), 'boot_queries' => $wpdb->queries - $q0, 'boot_kb' => round( strlen( $json ) / 1024 ), 'boot_gzip_kb' => round( strlen( gzencode( $json, 6 ) ) / 1024 ), 'ledger_rows_total' => (int) $wpdb->get_var( 'SELECT COUNT(*) FROM wp_nlrm_ledger WHERE owner_id = ' . $big ), 'ledger_rows_sent' => count( $b['ledger'] ), 'rent_run_ms' => round( ( $t3 - $t2 ) * 1000 ), 'rent_run_new' => $made, 'money_ms' => round( ( $t4 - $t3 ) * 1000 ) );
	check( 'perf.boot_under_3s', ( $t1 - $t0 ) < 3, (string) round( $t1 - $t0, 2 ) );
	check( 'perf.second_run_writes_nothing', 0 === $made, (string) $made );
}

/* ---------- the four landlords ---------- */
make_owner( 1, '1 apartment', array( array( 'הרצל 12', 'חולון', 4, 2, 1 ) ) );
make_owner( 2, '3 apartments', array( array( 'ביאליק 40', 'רמת גן', 5, 3, 3 ) ) );
make_owner( 3, '15 apartments', array( array( 'ז\'בוטינסקי 100', 'פתח תקווה', 8, 2, 9 ), array( 'Dizengoff 210', 'Tel Aviv', 6, 1, 6 ) ), true );
make_owner( 4, '200 apartments', array(
	array( 'דרך מנחם בגין 50', 'תל אביב', 20, 5, 30 ), array( 'הרצל 80', 'ראשון לציון', 12, 3, 25 ), array( 'שדרות ירושלים 5', 'יפו', 10, 3, 25 ), array( 'Ben Yehuda 70', 'Tel Aviv', 9, 3, 25 ),
	array( 'העצמאות 33', 'חיפה', 8, 4, 25 ), array( 'יפו 120', 'ירושלים', 7, 4, 25 ), array( 'רגר 15', 'באר שבע', 6, 4, 20 ), array( 'הנשיא 9', 'נתניה', 5, 5, 25 ) ) );
check( 'world.units', 219 === count( $W['units'] ), (string) count( $W['units'] ) );

day_set( '2026-10-01' );
/* P1: one apartment, an old lease entered mid-way (onboarding): no invented arrears */
$u1 = $W['owners'][1]['units'][0];
$lid_import = move_in( 1, $u1, '2024-06-01', array( 'months' => 36, 'rent' => 5200, 'pay_day' => 1, 'behavior' => 'good', 'lang' => 'he', 'track_from' => '2026-10-01', 'link' => array( 'mode' => 'cpi', 'every' => 12, 'pct' => 100, 'floor' => true ) ) );
$m = nlrm_money( 1, '2026-10-01', array( $lid_import ) );
check( 'onboarding.no_invented_arrears', ( $m[ $lid_import ]['due'] ?? -1 ) <= 5200 * 100 * 1.1 && ( $m[ $lid_import ]['due'] ?? 0 ) > 0, json_encode( $m[ $lid_import ] ?? null ) );
/* P2: three apartments, mixed */
move_in( 2, $W['owners'][2]['units'][0], '2026-10-01', array( 'behavior' => 'cheque', 'lang' => 'he' ) );
move_in( 2, $W['owners'][2]['units'][1], '2026-10-15', array( 'behavior' => 'late', 'lang' => 'en', 'pay_day' => 15 ) );
move_in( 2, $W['owners'][2]['units'][2], '2026-11-01', array( 'behavior' => 'partial', 'lang' => 'ru' ) );
/* P3: fifteen apartments through the REST routes, with the calendar's traps */
$p3 = $W['owners'][3]['units'];
$special = array(
	array( '2026-10-01', array( 'behavior' => 'good', 'lang' => 'he', 'months' => 60, 'link' => array( 'mode' => 'cpi', 'every' => 6, 'pct' => 100, 'floor' => false ) ) ), /* deflation passes through */
	array( '2026-11-15', array( 'behavior' => 'good', 'lang' => 'en', 'months' => 12, 'pay_day' => 15 ) ),                                                                 /* 15th to 14th: 12 periods, not 13 */
	array( '2027-01-31', array( 'behavior' => 'standing', 'lang' => 'he', 'months' => 12, 'pay_day' => 28 ) ),                                                            /* 31st: Feb is 28 */
	array( '2028-02-29', array( 'behavior' => 'good', 'lang' => 'ar', 'months' => 24, 'pay_day' => 28 ) ),                                                               /* the leap day */
	array( '2026-10-01', array( 'behavior' => 'bad', 'lang' => 'he' ) ),
	array( '2026-10-01', array( 'behavior' => 'cheque', 'lang' => 'he', 'link' => array( 'mode' => 'cpi', 'every' => 12, 'pct' => 50, 'floor' => true ) ) ),
);
foreach ( $p3 as $i => $uid ) {
	if ( isset( $special[ $i ] ) ) {
		if ( $special[ $i ][0] > today() ) { $s = $special[ $i ]; q_add( $s[0], function () use ( $uid, $s ) { move_in( 3, $uid, $s[0], $s[1] ); } ); }
		else { move_in( 3, $uid, $special[ $i ][0], $special[ $i ][1] ); }
	} else {
		move_in( 3, $uid, $R->pick( array( '2026-10-01', '2026-10-01', '2026-10-15', '2026-11-01' ) ) > today() ? '2026-10-01' : '2026-10-01' );
	}
}
/* P4: two hundred apartments; 85% let on day one, the rest within 4 months; some imported mid-lease */
foreach ( $W['owners'][4]['units'] as $i => $uid ) {
	if ( $R->p( 0.85 ) ) {
		if ( $R->p( 0.25 ) ) {
			$st = o_add_months( '2026-10-01', -$R->i( 2, 20 ) );
			move_in( 4, $uid, $st, array( 'track_from' => '2026-10-01', 'months' => 36 ) );
		} else {
			move_in( 4, $uid, '2026-10-01' );
		}
	} else {
		$d = o_add_months( '2026-10-01', $R->i( 1, 4 ) );
		q_add( $d, function () use ( $uid, $d ) { move_in( 4, $uid, $d ); } );
	}
}
foreach ( $W['leases'] as $lid => $L ) { if ( $R->p( 0.04 ) ) { $W['leases'][ $lid ]['early'] = o_plus_days( $L['start'], $R->i( 60, max( 61, o_days( $L['start'], $L['end'] ) - 30 ) ) ); } }

/* a few encrypted documents per landlord (for the key rotation) */
foreach ( array( 1, 2, 3, 4 ) as $oid ) {
	for ( $i = 0; $i < 3; $i++ ) {
		$bytes = 'PDF-sim ' . $oid . '-' . $i . ' ' . str_repeat( 'חוזה שכירות ', 50 );
		$rel = $oid . '/doc' . $i . '.bin';
		@mkdir( nlrm_private_dir() . $oid, 0777, true );
		file_put_contents( nlrm_private_dir() . $rel, nlrm_blob_enc( $bytes ) );
		$wpdb->insert( nlrm_t( 'docs' ), array( 'owner_id' => $oid, 'scope' => 'property', 'scope_id' => $W['owners'][ $oid ]['props'][0], 'kind' => 'lease', 'name' => 'doc' . $i . '.pdf', 'mime' => 'application/pdf', 'size' => strlen( $bytes ), 'path' => $rel, 'sha256' => hash( 'sha256', $bytes ), 'enc' => 1, 'created_by' => 'sim', 'created_at' => nlrm_now() ) );
		$W['docs'][] = array( 'path' => $rel, 'sha' => hash( 'sha256', $bytes ) );
	}
}

/* ---------- the timeline ---------- */
$T0 = microtime( true );
$end_day = o_plus_days( o_add_months( '2026-10-01', 12 * $YEARS ), -1 );
$day = '2026-10-01';
$rot_done = false; $del_done = false;
while ( $day <= $end_day ) {
	day_set( $day );
	$dd = (int) substr( $day, 8 );
	/* the daily job (cron): rent for everyone, the purge */
	if ( in_array( $dd, array( 1, 8, 15, 22 ), true ) ) {
		nlrm_daily_run();
		/* a second run the same day writes nothing */
		if ( 15 === $dd && '01' === substr( $day, 5, 2 ) ) {
			$n = 0; foreach ( array( 1, 2, 3, 4 ) as $o ) { $n += nlrm_rent_run( $o ); }
			check( 'rent_run.idempotent', 0 === $n, (string) $n );
		}
	}
	foreach ( $W['queue'][ $day ] ?? array() as $fn ) { $fn(); }
	unset( $W['queue'][ $day ] );
	foreach ( array_keys( $W['leases'] ) as $lid ) { lease_day( $lid ); }
	foreach ( array( 1, 2, 3, 4 ) as $oid ) { expenses_day( $oid ); repairs_day( $oid ); }

	/* year 4: three former tenants are deleted; 30 days later they are gone */
	if ( ! $del_done && $day >= '2030-04-01' ) {
		$del_done = true;
		as_owner( 3 );
		$gone = array();
		foreach ( $W['leases'] as $lid => $L ) {
			if ( 3 === $L['owner'] && 'ended' === $L['status'] && count( $gone ) < 3 && ! in_array( $L['tenant'], $gone, true ) ) {
				$still = false;
				foreach ( $W['leases'] as $L2 ) { if ( $L2['tenant'] === $L['tenant'] && 'active' === $L2['status'] ) { $still = true; } }
				if ( $still ) { continue; }
				$r = sim_rest( '/rm/delete', array( 'entity' => 'contact', 'id' => $L['tenant'] ) );
				if ( check( 'privacy.delete_contact', is_array( $r ) && ! empty( $r['deleted'] ) ) ) { $gone[] = $L['tenant']; }
			}
		}
		$W['deleted_contacts'] = $gone;
		$ids_before = array_map( 'intval', $wpdb->get_col( 'SELECT id FROM wp_nlrm_ledger WHERE owner_id = 3' ) );
		$r = sim_rest( '/rm/delete', array( 'entity' => 'ledger', 'id' => (int) $wpdb->get_var( 'SELECT id FROM wp_nlrm_ledger WHERE owner_id = 3 LIMIT 1' ) ) );
		check( 'books.delete_refused', is_wp_error( $r ) && 'nlrm_books' === $r->code );
		q_add( o_plus_days( $day, 31 ), function () use ( $gone, $ids_before ) {
			global $wpdb;
			nlrm_purge();
			foreach ( $gone as $cid ) { check( 'privacy.purged_after_30_days', null === $wpdb->get_var( 'SELECT id FROM wp_nlrm_contacts WHERE id = ' . (int) $cid ) ); }
			/* the purge removes people, never a line of the books (tax records) */
			$after = array_flip( array_map( 'intval', $wpdb->get_col( 'SELECT id FROM wp_nlrm_ledger WHERE owner_id = 3' ) ) );
			$missing = 0;
			foreach ( $ids_before as $id ) { if ( ! isset( $after[ $id ] ) ) { $missing++; } }
			check( 'privacy.purge_keeps_books', 0 === $missing, "$missing lines missing" );
		} );
	}

	/* year 5: the data key is rotated; nothing changes for anyone */
	if ( ! $rot_done && $day >= '2031-06-01' ) {
		$rot_done = true;
		$snap = array();
		foreach ( $wpdb->get_results( 'SELECT id, owner_id FROM wp_nlrm_contacts', ARRAY_A ) as $c ) { $x = nlrm_get( 'contact', (int) $c['id'], (int) $c['owner_id'] ); $snap[ $c['id'] ] = $x['name'] . '|' . $x['phone'] . '|' . $x['email'] . '|' . $x['idno']; }
		$tsnap = array();
		foreach ( $wpdb->get_results( 'SELECT id, owner_id FROM wp_nlrm_tickets', ARRAY_A ) as $c ) { $x = nlrm_get( 'ticket', (int) $c['id'], (int) $c['owner_id'] ); $tsnap[ $c['id'] ] = $x['body']; }
		$idno1 = nlrm_dec( get_user_meta( 1, 'nlrm_idno_enc', true ) );
		$old_kid = nlrm_keyring()['cur'];
		$hash_before = nlrm_hash( '972500000001' );
		$kid = nlrm_rotate_begin();
		check( 'key.rotate_begin', is_string( $kid ) && $kid !== $old_kid );
		$steps = 0;
		$t0 = microtime( true );
		while ( nlrm_rotate_step( 400 ) && $steps < 10000 ) { $steps++; }
		$GLOBALS['M']['rotation'] = array( 'contacts' => count( $snap ), 'tickets' => count( $tsnap ), 'steps' => $steps + 1, 'seconds' => round( microtime( true ) - $t0, 2 ) );
		nlrm_keyring( true );
		$same = 0; $diff = 0;
		foreach ( $snap as $id => $v ) { $x = nlrm_get( 'contact', (int) $id, (int) $wpdb->get_var( 'SELECT owner_id FROM wp_nlrm_contacts WHERE id = ' . (int) $id ) ); ( $x['name'] . '|' . $x['phone'] . '|' . $x['email'] . '|' . $x['idno'] === $v ) ? $same++ : $diff++; }
		check( 'key.rotation_contacts_identical', 0 === $diff && $same === count( $snap ), "$same same, $diff differ" );
		$td = 0; foreach ( $tsnap as $id => $v ) { $x = nlrm_get( 'ticket', (int) $id, (int) $wpdb->get_var( 'SELECT owner_id FROM wp_nlrm_tickets WHERE id = ' . (int) $id ) ); if ( $x['body'] !== $v ) { $td++; } }
		check( 'key.rotation_tickets_identical', 0 === $td, "$td differ" );
		$left = (int) $wpdb->get_var( $wpdb->prepare( "SELECT COUNT(*) FROM wp_nlrm_contacts WHERE name_enc <> '' AND name_enc NOT LIKE %s", 's2:' . $kid . ':%' ) );
		check( 'key.rotation_all_reencrypted', 0 === $left, "$left left" );
		check( 'key.rotation_landlord_idno', nlrm_dec( get_user_meta( 1, 'nlrm_idno_enc', true ) ) === $idno1 );
		check( 'key.rotation_blind_index_stable', nlrm_hash( '972500000001' ) === $hash_before );
		$okd = 0; foreach ( $W['docs'] as $d ) { $p = nlrm_blob_dec( file_get_contents( nlrm_private_dir() . $d['path'] ) ); if ( false !== $p && hash( 'sha256', $p ) === $d['sha'] && nlrm_blob_kid( file_get_contents( nlrm_private_dir() . $d['path'] ) ) === $kid ) { $okd++; } }
		check( 'key.rotation_files', $okd === count( $W['docs'] ), "$okd of " . count( $W['docs'] ) );
		check( 'key.keycheck_after_rotation', nlrm_key_ok() );
		count_ev( 'key_rotations' );
	}

	/* month end: the audit */
	if ( $day === o_month_end( $day ) ) {
		$deep = '09' === substr( $day, 5, 2 ) || '03' === substr( $day, 5, 2 );
		foreach ( array( 1, 2, 3, 4 ) as $oid ) { audit( $oid, $deep ); }
		audit_cash();
		if ( '09' === substr( $day, 5, 2 ) ) {
			audit_stats();
			perf( substr( $day, 0, 4 ) );
			/* Hebrew and English: the lease text and the tenant's page */
			foreach ( array( 'he', 'en' ) as $lg ) {
				$any = null; foreach ( $W['leases'] as $L ) { if ( 'active' === $L['status'] && 3 === $L['owner'] ) { $any = $L; break; } }
				if ( $any ) {
					$lease = nlrm_get( 'lease', $any['id'], 3 );
					$txt = nlrm_lease_text( 3, $lease, $lg );
					$flat = json_encode( $txt, JSON_UNESCAPED_UNICODE );
					check( 'i18n.lease_text_' . $lg, ! empty( $txt['sections'] ) && false !== strpos( $flat, number_format( $any['rent'] ) ), substr( $flat, 0, 80 ) );
					check( 'i18n.lease_text_script_' . $lg, 'he' === $lg ? (bool) preg_match( '/\p{Hebrew}/u', $txt['title'] ?? '' ) : ! preg_match( '/\p{Hebrew}/u', $txt['title'] ?? '' ), $txt['title'] ?? '' );
					$_SERVER['HTTP_X_NLRM_LINK'] = $any['token'];
					$_SERVER['REMOTE_ADDR'] = $any['ip'];
					$link = nlrm_link_from_request( array( 'tenant' ) );
					if ( check( 'portal.link_valid', (bool) $link, 'yearly' ) ) {
						$pp = nlrm_portal_payload( $link );
						$mm = nlrm_money( 3, today(), array( $any['id'] ) );
						check( 'portal.balance_is_books', ! is_wp_error( $pp ) && $pp['balance'] === ( $mm[ $any['id'] ]['balance'] ?? null ), is_wp_error( $pp ) ? $pp->message : $pp['balance'] . ' vs ' . ( $mm[ $any['id'] ]['balance'] ?? 'x' ) );
					}
					$_SERVER['HTTP_X_NLRM_LANG'] = $lg;
					$e = nlrm_err( 'x', 400, 'שגיאה', 'Error' );
					check( 'i18n.errors_' . $lg, ( 'he' === $lg ? 'שגיאה' : 'Error' ) === $e->message );
				}
			}
			fwrite( STDERR, sprintf( "%s  checks %d  fails %d  ledger %d  %.0fs\n", $day, $GLOBALS['M']['checks'], $GLOBALS['M']['fails'], (int) $wpdb->get_var( 'SELECT COUNT(*) FROM wp_nlrm_ledger' ), microtime( true ) - $T0 ) );
		}
	}
	$day = o_plus_days( $day, 1 );
}

/* ---------- the end: salt change, lost key, export, erase, parity dump ---------- */
$cid = (int) $wpdb->get_var( 'SELECT id FROM wp_nlrm_contacts WHERE owner_id = 3 ORDER BY id DESC LIMIT 1' );
$c = nlrm_get( 'contact', $cid, 3 );
$php = PHP_BINARY . ' -d extension=pdo_sqlite -d extension=sodium ' . escapeshellarg( __FILE__ ) . ' --child=%s --db=' . escapeshellarg( $DB ) . ' --up=' . escapeshellarg( $UP ) . ' --cid=' . $cid;
putenv( 'SIM_SALT=rotated-by-a-security-plugin' );
$salt = json_decode( (string) shell_exec( sprintf( $php, 'salt' ) ), true );
putenv( 'SIM_SALT' );
check( 'key.survives_salt_change', is_array( $salt ) && $salt['name'] === $c['name'] && $salt['key_ok'], json_encode( $salt, JSON_UNESCAPED_UNICODE ) );
$nokey = json_decode( (string) shell_exec( sprintf( $php, 'nokey' ) ), true );
check( 'key.lost_file_refuses_writes', is_array( $nokey ) && false === $nokey['key_ok'], json_encode( $nokey, JSON_UNESCAPED_UNICODE ) );
as_owner( 3 );
$exp = sim_rest( '/rm/export' );
$all = (int) $wpdb->get_var( 'SELECT COUNT(*) FROM wp_nlrm_ledger WHERE owner_id = 3' );
check( 'export.every_ledger_line', is_array( $exp ) && count( $exp['ledger'] ) === $all, count( $exp['ledger'] ?? array() ) . ' vs ' . $all );
check( 'export.has_money_and_stats', is_array( $exp ) && ! empty( (array) $exp['money'] ) && ! empty( (array) $exp['stats'] ) );
file_put_contents( $OUT . '/export-landlord-15.json', json_encode( $exp, JSON_UNESCAPED_UNICODE ) );
$before = array();
foreach ( array( 2, 3, 4 ) as $o ) { $before[ $o ] = (int) $wpdb->get_var( 'SELECT COUNT(*) FROM wp_nlrm_ledger WHERE owner_id = ' . $o ); }
as_owner( 1 );
$no = sim_rest( '/rm/erase', array( 'confirm' => 'yes' ) );
check( 'erase.needs_explicit_word', is_wp_error( $no ) );
$er = sim_rest( '/rm/erase', array( 'confirm' => 'ERASE' ) );
$left = 0;
foreach ( array( 'properties', 'units', 'contacts', 'leases', 'ledger', 'tickets', 'docs', 'events', 'links', 'tasks', 'members' ) as $t ) { $left += (int) $wpdb->get_var( 'SELECT COUNT(*) FROM wp_nlrm_' . $t . ' WHERE owner_id = 1' ); }
check( 'erase.everything_of_one_landlord', is_array( $er ) && 0 === $left, "$left rows left" );
$same = true; foreach ( $before as $o => $n ) { if ( (int) $wpdb->get_var( 'SELECT COUNT(*) FROM wp_nlrm_ledger WHERE owner_id = ' . $o ) !== $n ) { $same = false; } }
check( 'erase.others_untouched', $same );

/* for the browser twin (rm-core.js N.mx): every lease's lines and the PHP answer */
$parity = array( 'today' => today(), 'leases' => array() );
foreach ( array( 2, 3, 4 ) as $o ) {
	$mm = nlrm_money( $o, today() );
	$rows = $wpdb->get_results( $wpdb->prepare( 'SELECT id, lease_id, kind, category, method, status, amount, due_date FROM wp_nlrm_ledger WHERE owner_id = %d AND lease_id > 0', $o ), ARRAY_A );
	$by = array(); foreach ( $rows as $r ) { $by[ $r['lease_id'] ][] = $r; }
	foreach ( $by as $lid => $list ) { $parity['leases'][] = array( 'id' => (int) $lid, 'rows' => $list, 'php' => $mm[ $lid ] ?? null ); }
}
file_put_contents( $OUT . '/parity.json', json_encode( $parity ) );

/* the report */
$M = $GLOBALS['M'];
$M['seed'] = $SEED;
$M['years'] = $YEARS;
$M['seconds'] = round( microtime( true ) - $T0 );
$M['totals'] = array(
	'leases' => count( $W['leases'] ), 'ledger_lines' => (int) $wpdb->get_var( 'SELECT COUNT(*) FROM wp_nlrm_ledger' ), 'events' => (int) $wpdb->get_var( 'SELECT COUNT(*) FROM wp_nlrm_events' ),
	'tickets' => (int) $wpdb->get_var( 'SELECT COUNT(*) FROM wp_nlrm_tickets' ), 'contacts' => (int) $wpdb->get_var( 'SELECT COUNT(*) FROM wp_nlrm_contacts' ),
	'cash_in_agorot' => $W['tally']['cash_in'], 'cash_out_agorot' => $W['tally']['cash_out'], 'income_agorot' => $W['tally']['income'], 'expense_agorot' => $W['tally']['expense'],
	'void_lines' => (int) $wpdb->get_var( "SELECT COUNT(*) FROM wp_nlrm_ledger WHERE status = 'void'" ), 'cpi_settled' => (int) $wpdb->get_var( "SELECT COUNT(*) FROM wp_nlrm_ledger WHERE auto_key LIKE 'cpiadj:%'" ),
	'cpi_unsettled' => (int) $wpdb->get_var( "SELECT COUNT(*) FROM wp_nlrm_ledger WHERE note LIKE 'cpi?%' AND status <> 'void'" ), 'prorated_lines' => (int) $wpdb->get_var( "SELECT COUNT(*) FROM wp_nlrm_ledger WHERE auto_key LIKE 'rent:%:p' OR (kind = 'charge' AND note LIKE '% %/%' AND auto_key LIKE 'rent:%')" ),
	'db_mb' => round( filesize( $DB ) / 1048576, 1 ),
);
check( 'cpi.everything_settled', 0 === $M['totals']['cpi_unsettled'], (string) $M['totals']['cpi_unsettled'] );
$M['passed'] = $M['checks'] - $M['fails'];
file_put_contents( $OUT . '/report.json', json_encode( $M, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE ) );
printf( "\nSEED %d  YEARS %d  CHECKS %d  PASSED %d  FAILED %d  (%ds)\n", $SEED, $YEARS, $M['checks'], $M['passed'], $M['fails'], $M['seconds'] );
foreach ( array_slice( $M['fail_list'], 0, 40 ) as $f ) { echo "  FAIL $f\n"; }
exit( $M['fails'] ? 1 : 0 );
