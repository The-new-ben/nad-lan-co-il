<?php
/* The tenant's personal page, as the REAL server answers it (portal.php nlrm_portal_payload),
   for a sample lease: written to docs/design-lab/rentals/portal-<lang>.json so the lab can show
   the page exactly (scripts/rentals/lab_portal.py). No real person: sample names, 050-000 numbers.
   php -d extension=pdo_sqlite -d extension=sodium scripts/rentals/portal_payload.php */
require __DIR__ . '/sim/wp_shim.php';
$GLOBALS['SIM_T'] = gmmktime( 9, 0, 0, (int) gmdate( 'n' ), (int) gmdate( 'j' ), (int) gmdate( 'Y' ) );
add_filter( 'nlrm_time', function () { return $GLOBALS['SIM_T']; } );
$tmp = sys_get_temp_dir() . '/nlrm-portal-' . getmypid();
sim_boot( ':memory:', $tmp );
nlrm_install();
$O = 1;
$GLOBALS['sim_user'] = $O;
update_user_meta( $O, 'nlrm_display', 'דני כהן' );
update_user_meta( $O, 'nlrm_phone', '972500000999' );
update_user_meta( $O, 'nlrm_pay', array( 'bank' => 'בנק לאומי, סניף 800, חשבון 12345678, דני כהן (דוגמה)', 'bit' => '972500000999', 'link' => '' ) );
$out = array();
foreach ( array( 'he', 'en' ) as $lang ) {
	$en = 'en' === $lang;
	update_user_meta( $O, 'nlrm_display', $en ? 'Dan Cohen' : 'דני כהן' );
	update_user_meta( $O, 'nlrm_pay', array( 'bank' => $en ? 'Bank Leumi, branch 800, account 12345678, Dan Cohen (sample)' : 'בנק לאומי, סניף 800, חשבון 12345678, דני כהן (דוגמה)', 'bit' => '972500000999', 'link' => '' ) );
	$p = nlrm_save( 'property', array( 'title' => '', 'address' => $en ? '78 Arlozorov St' : 'ארלוזורוב 78', 'city' => $en ? 'Tel Aviv-Yafo' : 'תל אביב-יפו', 'floors' => 5, 'units_per_floor' => 3 ), $O );
	$u = nlrm_save( 'unit', array( 'property_id' => $p['id'], 'label' => $en ? 'Apt 7' : 'דירה 7', 'floor' => 3, 'rooms' => 3, 'sqm' => 72 ), $O );
	$c = nlrm_save( 'contact', array( 'kind' => 'tenant', 'name' => $en ? 'Daniel Brooks' : 'משפחת לוי', 'phone' => '0500000101', 'lang' => $lang ), $O );
	$start = gmdate( 'Y-m-01', strtotime( '-7 months', $GLOBALS['SIM_T'] ) );
	$l = nlrm_save( 'lease', array( 'unit_id' => $u['id'], 'status' => 'active', 'start_date' => $start, 'end_date' => nlrm_add_days( nlrm_add_months( $start, 12 ), -1 ), 'rent' => 6400, 'pay_day' => 1,
		'linkage' => array( 'mode' => 'cpi', 'every' => 12, 'pct' => 100, 'floor' => true, 'base_date' => $start ), 'parties' => array( 'tenants' => array( $c['id'] ) ), 'terms' => array( 'method' => 'transfer' ) ), $O );
	nlrm_rent_run( $O );
	/* six months paid, this month reported by the tenant from his link (pending), the deposit held */
	$m = nlrm_money( $O, null, array( $l['id'] ) );
	for ( $i = 0; $i < 7; $i++ ) { nlrm_pay( $O, array( 'lease_id' => $l['id'], 'amount' => 6400, 'paid_date' => nlrm_add_days( nlrm_add_months( $start, $i ), 2 ), 'method' => 'transfer' ), 'cref:p' . $lang . $i ); }
	nlrm_deposit( $O, $l['id'], 'receive', array( 'amount' => 12800, 'date' => $start ), 'cref:d' . $lang );
	nlrm_pay( $O, array( 'lease_id' => $l['id'], 'amount' => 6400, 'paid_date' => nlrm_today(), 'method' => 'bit', 'status' => 'pending', 'note' => 'דווח על ידי השוכר · reported by the tenant' ), 'cref:r' . $lang );
	nlrm_save( 'ticket', array( 'property_id' => $p['id'], 'unit_id' => $u['id'], 'title' => $en ? 'Kitchen tap drips' : 'טפטוף בברז המטבח', 'body' => '', 'urgency' => 'standard', 'status' => 'scheduled', 'reporter' => 'tenant', 'due_by' => nlrm_add_days( nlrm_today(), 20 ), 'meta' => array( 'visit_at' => nlrm_add_days( nlrm_today(), 2 ) . ' 16:00' ) ), $O );
	$link = nlrm_link_create( $O, 'tenant', 'lease', $l['id'], $c['id'], 400 );
	$token = substr( $link['url'], strpos( $link['url'], '=', strpos( $link['url'], '#' ) ) + 1 );
	$_SERVER['HTTP_X_NLRM_LINK'] = $token;
	$_SERVER['REMOTE_ADDR'] = '10.9.9.' . ( 'he' === $lang ? 1 : 2 );
	$row = nlrm_link_from_request( array( 'tenant' ) );
	$out[ $lang ] = nlrm_portal_payload( $row );
}
$dir = dirname( __DIR__, 2 ) . '/docs/design-lab/rentals/';
foreach ( $out as $lang => $payload ) { file_put_contents( $dir . 'portal-' . $lang . '.json', json_encode( $payload, JSON_UNESCAPED_UNICODE | JSON_PRETTY_PRINT ) ); }
echo 'written: portal-he.json (balance ' . $out['he']['balance'] . '), portal-en.json (balance ' . $out['en']['balance'] . ")\n";
