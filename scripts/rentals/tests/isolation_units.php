<?php
/* Two landlords, synthetic data only (the audience decision package, 3.10.2026): landlord B can neither read nor change anything of
   landlord A through the REST routes, the link holders stay inside their scope, a visitor gets nothing, and each export holds only
   its owner's rows. Runs the REAL permission callbacks and handlers on the sim shim (SQLite).
   php -d extension=pdo_sqlite -d extension=sodium scripts/rentals/tests/isolation_units.php */
require __DIR__ . '/../sim/wp_shim.php';
$tmp = sys_get_temp_dir() . '/nlrm-iso-' . getmypid();
sim_boot( ':memory:', $tmp );
nlrm_install();
$ok = 0; $bad = 0;
function t( $name, $cond, $info = '' ) { global $ok, $bad; if ( $cond ) { $ok++; } else { $bad++; echo "FAIL $name $info\n"; } }
function err_status( $r ) { return is_wp_error( $r ) ? (int) ( $r->data['status'] ?? 0 ) : 0; }

/* landlord A (9) and landlord B (10), each with a building, an apartment, a tenant, a lease, a ticket, a link */
function make( $o, $tag ) {
	$GLOBALS['sim_user'] = $o;
	$p = nlrm_save( 'property', array( 'title' => '', 'address' => "רחוב $tag 1", 'city' => 'עיר', 'floors' => 2, 'units_per_floor' => 2 ), $o );
	$u = nlrm_save( 'unit', array( 'property_id' => $p['id'], 'label' => "דירה $tag", 'floor' => 1, 'pos' => 0 ), $o );
	$c = nlrm_save( 'contact', array( 'kind' => 'tenant', 'name' => "שוכר $tag", 'phone' => '05000000' . $o, 'idno' => '00000000' . $o, 'lang' => 'he' ), $o );
	$l = nlrm_save( 'lease', array( 'unit_id' => $u['id'], 'status' => 'active', 'start_date' => nlrm_today(), 'end_date' => nlrm_add_days( nlrm_add_months( nlrm_today(), 12 ), -1 ), 'rent' => 4000 + $o, 'pay_day' => 1,
		'linkage' => array( 'mode' => 'none' ), 'securities' => array(), 'parties' => array( 'tenants' => array( $c['id'] ) ), 'terms' => array( 'method' => 'transfer' ) ), $o );
	nlrm_rent_run( $o, nlrm_today(), (int) $l['id'] );
	$tk = nlrm_save( 'ticket', array( 'property_id' => $p['id'], 'unit_id' => $u['id'], 'title' => "תקלה $tag", 'status' => 'new', 'urgency' => 'standard', 'category' => 'general' ), $o );
	$lk = nlrm_link_create( $o, 'tenant', 'lease', (int) $l['id'], (int) $c['id'], 400 );
	$vk = nlrm_link_create( $o, 'vendor', 'ticket', (int) $tk['id'], 0, 14 );
	return compact( 'p', 'u', 'c', 'l', 'tk', 'lk', 'vk' );
}
$A = make( 9, 'A' );
$B = make( 10, 'B' );
function linkrow( $id ) {
	$r = $GLOBALS['wpdb']->get_row( $GLOBALS['wpdb']->prepare( 'SELECT * FROM ' . nlrm_t( 'links' ) . ' WHERE id = %d', $id ), ARRAY_A );
	foreach ( array( 'id', 'owner_id', 'scope_id', 'contact_id' ) as $k ) { $r[ $k ] = (int) $r[ $k ]; }
	return $r;
}

/* B, logged in, aims at A's things */
$GLOBALS['sim_user'] = 10; $GLOBALS['sim_admin'] = false;
t( 'B cannot read A\'s lease books (/rm/ledger)', 403 === err_status( sim_rest( '/rm/ledger', array( 'lease_id' => $A['l']['id'] ) ) ) );
t( 'B cannot read A\'s evidence file (/rm/evidence)', 403 === err_status( sim_rest( '/rm/evidence', array( 'lease_id' => $A['l']['id'] ) ) ) );
$r = sim_rest( '/rm/pay', array( 'data' => array( 'lease_id' => $A['l']['id'], 'amount' => 100 ), 'client_ref' => 'x1' ) );
t( 'B cannot post a payment on A\'s lease (/rm/pay)', is_wp_error( $r ), is_wp_error( $r ) ? $r->get_error_code() : 'accepted' );
$r = sim_rest( '/rm/save', array( 'entity' => 'unit', 'data' => array( 'id' => $A['u']['id'], 'label' => 'hijack' ) ) );
t( 'B cannot change A\'s apartment (/rm/save)', is_wp_error( $r ) && 'hijack' !== nlrm_get( 'unit', (int) $A['u']['id'], 9 )['label'] );
$r = sim_rest( '/rm/save', array( 'entity' => 'contact', 'data' => array( 'id' => $A['c']['id'], 'name' => 'hijack' ) ) );
t( 'B cannot change A\'s tenant (/rm/save)', is_wp_error( $r ) );
$r = sim_rest( '/rm/delete', array( 'entity' => 'ticket', 'id' => $A['tk']['id'] ) );
t( 'B cannot delete A\'s repair (/rm/delete)', nlrm_get( 'ticket', (int) $A['tk']['id'], 9 ) && 'deleted' !== ( nlrm_get( 'ticket', (int) $A['tk']['id'], 9 )['status'] ?? '' ) );
$r = sim_rest( '/rm/link-revoke', array( 'id' => $A['lk']['id'] ) );
t( 'B cannot cancel A\'s tenant link (/rm/link-revoke)', is_array( $r ) && false === $r['revoked'] && ! linkrow( $A['lk']['id'] )['revoked_at'] );
$r = sim_rest( '/rm/lease-end', array( 'lease_id' => $A['l']['id'], 'data' => array( 'date' => nlrm_today() ) ) );
t( 'B cannot end A\'s lease (/rm/lease-end)', is_wp_error( $r ) && 'active' === nlrm_get( 'lease', (int) $A['l']['id'], 9 )['status'] );
$boot = sim_rest( '/rm/boot', array() );
$flat = json_encode( $boot, JSON_UNESCAPED_UNICODE );
t( 'B\'s boot holds none of A\'s rows', is_array( $boot ) && false === strpos( $flat, 'רחוב A 1' ) && false === strpos( $flat, 'שוכר A' ) && false !== strpos( $flat, 'רחוב B 1' ) );
$ex = sim_rest( '/rm/export', array() );
$flat = json_encode( $ex, JSON_UNESCAPED_UNICODE );
t( 'B\'s export holds none of A\'s rows', is_array( $ex ) && false === strpos( $flat, 'שוכר A' ) && false === strpos( $flat, '"lease_id":' . (int) $A['l']['id'] . ',' ) );
$links = sim_rest( '/rm/links', array() );
t( 'B\'s links list holds only B\'s links', is_array( $links ) && ! array_filter( $links['links'], function ( $k ) use ( $A ) { return (int) $k['id'] === (int) $A['lk']['id'] || (int) $k['id'] === (int) $A['vk']['id']; } ) );

/* link holders stay inside their scope */
$GLOBALS['sim_user'] = 0;
$pl = nlrm_portal_payload( linkrow( $A['lk']['id'] ) );
$flat = json_encode( $pl, JSON_UNESCAPED_UNICODE );
t( 'A\'s tenant link shows A\'s lease only', false !== strpos( $flat, 'דירה A' ) && false === strpos( $flat, 'דירה B' ) && false === strpos( $flat, 'שוכר B' ) );
t( 'the tenant page never shows an ID number', false === strpos( $flat, '000000009' ) && false === strpos( $flat, '0000000010' ) );
$r = nlrm_portal_act( linkrow( $A['lk']['id'] ), new WP_REST_Request( array( 'act' => 'vendor_update', 'data' => array( 'status' => 'done' ) ) ) );
t( 'a tenant link cannot act as a professional', is_wp_error( $r ) );
$r = nlrm_portal_act( linkrow( $A['vk']['id'] ), new WP_REST_Request( array( 'act' => 'vendor_update', 'data' => array( 'status' => 'done', 'id' => $B['tk']['id'] ) ) ) );
t( 'A\'s professional link updates A\'s repair only (an id in the request is ignored)', 'done' === nlrm_get( 'ticket', (int) $A['tk']['id'], 9 )['status'] && 'done' !== nlrm_get( 'ticket', (int) $B['tk']['id'], 10 )['status'] );
$r = nlrm_portal_act( linkrow( $A['vk']['id'] ), new WP_REST_Request( array( 'act' => 'paid', 'data' => array( 'amount' => 100 ) ) ) );
t( 'a professional link cannot report a payment', is_wp_error( $r ) );
/* a cancelled or foreign token gets nothing */
$GLOBALS['sim_user'] = 9;
sim_rest( '/rm/link-revoke', array( 'id' => $A['lk']['id'] ) );
$GLOBALS['sim_user'] = 0;
$_SERVER['HTTP_X_NLRM_LINK'] = str_repeat( 'A', 43 );
t( 'an unknown token opens nothing', null === nlrm_link_from_request( array( 'tenant' ) ) );
unset( $_SERVER['HTTP_X_NLRM_LINK'] );

/* a visitor (not logged in) gets nothing from the landlord routes */
foreach ( array( '/rm/boot', '/rm/export', '/rm/links' ) as $route ) {
	t( "a visitor gets nothing from $route", is_wp_error( sim_rest( $route, array() ) ) );
}
t( 'a visitor cannot write (/rm/save)', is_wp_error( sim_rest( '/rm/save', array( 'entity' => 'unit', 'data' => array( 'label' => 'x' ) ) ) ) );
echo "isolation checks: $ok passed, $bad failed\n";
exit( $bad ? 1 : 0 );
