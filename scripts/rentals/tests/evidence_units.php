<?php
/* The evidence file's server side (HAD-401): /rm/evidence returns the WHOLE history of one lease
   (every ledger line from the first month, every event of the lease and its tenant), sorted by time,
   and only to the lease's own landlord. The screen's bootstrap holds 150 events and the books from
   January of last year, which is not enough for an eviction file.
   php -d extension=pdo_sqlite -d extension=sodium scripts/rentals/tests/evidence_units.php */
require __DIR__ . '/../sim/wp_shim.php';
$tmp = sys_get_temp_dir() . '/nlrm-evid-' . getmypid();
sim_boot( ':memory:', $tmp );
nlrm_install();
$ok = 0; $bad = 0;
function t( $name, $cond, $info = '' ) { global $ok, $bad; if ( $cond ) { $ok++; } else { $bad++; echo "FAIL $name $info\n"; } }

$O = 9;
$GLOBALS['sim_user'] = $O;
$today = nlrm_today();
$start = ( (int) substr( $today, 0, 4 ) - 3 ) . '-01-01';
$p = nlrm_save( 'property', array( 'title' => '', 'address' => 'הרצל 1', 'city' => 'חיפה', 'floors' => 3, 'units_per_floor' => 2 ), $O );
$u = nlrm_save( 'unit', array( 'property_id' => $p['id'], 'label' => 'דירה 1', 'floor' => 1, 'pos' => 0 ), $O );
$c = nlrm_save( 'contact', array( 'kind' => 'tenant', 'name' => 'שוכר בדיקה', 'phone' => '0501234567' ), $O );
$l = nlrm_save( 'lease', array( 'unit_id' => $u['id'], 'status' => 'active', 'start_date' => $start, 'end_date' => nlrm_add_days( nlrm_add_months( $start, 48 ), -1 ), 'rent' => 5000, 'pay_day' => 1,
	'linkage' => array( 'mode' => 'none', 'every' => 12, 'pct' => 100, 'floor' => true, 'base_date' => $start ), 'securities' => array(), 'parties' => array( 'tenants' => array( $c['id'] ) ), 'terms' => array( 'method' => 'transfer' ) ), $O );
nlrm_rent_run( $O, $today, (int) $l['id'] );
/* the first two years paid month by month (closed lines older than January of last year: not in the screen's window) */
for ( $k = 0; $k < 24; $k++ ) { $r = nlrm_pay( $O, array( 'lease_id' => (int) $l['id'], 'amount' => 5000, 'paid_date' => nlrm_add_months( $start, $k ), 'method' => 'transfer' ), 'cref:evid-' . $k ); }
for ( $i = 0; $i < 220; $i++ ) { nlrm_event( $O, '', 'lease', (int) $l['id'], 'msg_out', 'whatsapp', 'הודעה ' . $i, array() ); }
for ( $i = 0; $i < 30; $i++ ) { nlrm_event( $O, '', 'contact', (int) $c['id'], 'note', '', 'הערה ' . $i, array() ); }

$charges = (int) $GLOBALS['wpdb']->get_var( $GLOBALS['wpdb']->prepare( 'SELECT COUNT(*) FROM ' . nlrm_t( 'ledger' ) . " WHERE lease_id = %d AND kind = 'charge'", $l['id'] ) );
$boot = nlrm_bootstrap( $O );
$boot_rows = count( array_filter( $boot['ledger'], function ( $r ) use ( $l ) { return (int) $r['lease_id'] === (int) $l['id']; } ) );
$ev = sim_rest( '/rm/evidence', array( 'lease_id' => $l['id'] ) );
t( 'the route answers the landlord', is_array( $ev ) && isset( $ev['rows'], $ev['events'] ), is_wp_error( $ev ) ? $ev->get_error_message() : '' );
t( 'every ledger line of the lease, from the first month', count( $ev['rows'] ) === $charges + 24, count( $ev['rows'] ) . ' vs ' . ( $charges + 24 ) );
t( 'more than the screen holds (the 3-year-old lines)', count( $ev['rows'] ) > $boot_rows, count( $ev['rows'] ) . ' > ' . $boot_rows );
t( 'the payment from the first day is there', (bool) array_filter( $ev['rows'], function ( $r ) use ( $start ) { return 'payment' === $r['kind'] && $start === $r['paid_date']; } ) );
t( 'every event of the lease and the tenant (250 + the system ones)', count( $ev['events'] ) >= 250, count( $ev['events'] ) );
t( 'more events than the screen holds', count( $ev['events'] ) > count( $boot['events'] ), count( $ev['events'] ) . ' > ' . count( $boot['events'] ) );
$sorted = true; for ( $i = 1; $i < count( $ev['events'] ); $i++ ) { if ( $ev['events'][ $i ]['at'] < $ev['events'][ $i - 1 ]['at'] ) { $sorted = false; } }
t( 'events in time order', $sorted );
t( 'event bodies decrypted', (bool) array_filter( $ev['events'], function ( $e ) { return 'הודעה 0' === $e['body']; } ) );
t( 'the balance comes with it', isset( $ev['money'] ) );
$GLOBALS['sim_user'] = 10;
$no = sim_rest( '/rm/evidence', array( 'lease_id' => $l['id'] ) );
t( 'another landlord gets nothing', is_wp_error( $no ) && 403 === ( $no->data['status'] ?? 0 ), is_wp_error( $no ) ? $no->get_error_code() : 'answered' );
$GLOBALS['sim_user'] = 0;
$no = sim_rest( '/rm/evidence', array( 'lease_id' => $l['id'] ) );
t( 'a visitor gets nothing', is_wp_error( $no ) );
echo "evidence checks: $ok passed, $bad failed\n";
exit( $bad ? 1 : 0 );
