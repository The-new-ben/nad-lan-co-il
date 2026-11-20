<?php
/* The landlord's e-mail alerts (HAD-401): an urgent repair and a signed lease at once; a reported payment, a message, an applicant
   and a done repair in one summary a day; a replayed report told once; off in Settings means no mail; never a phone or an ID.
   php -d extension=pdo_sqlite -d extension=sodium scripts/rentals/tests/notify_units.php */
require __DIR__ . '/../sim/wp_shim.php';
$tmp = sys_get_temp_dir() . '/nlrm-ntf-' . getmypid();
sim_boot( ':memory:', $tmp );
nlrm_install();
$ok = 0; $bad = 0;
function t( $name, $cond, $info = '' ) { global $ok, $bad; if ( $cond ) { $ok++; } else { $bad++; echo "FAIL $name $info\n"; } }

$O = 9;
$GLOBALS['sim_user'] = $O;
$p = nlrm_save( 'property', array( 'title' => '', 'address' => 'הרצל 1', 'city' => 'חיפה', 'floors' => 3, 'units_per_floor' => 2 ), $O );
$u = nlrm_save( 'unit', array( 'property_id' => $p['id'], 'label' => 'דירה 4', 'floor' => 2, 'pos' => 0 ), $O );
$c = nlrm_save( 'contact', array( 'kind' => 'tenant', 'name' => 'דנה כהן', 'phone' => '0501234567', 'idno' => '123456782', 'lang' => 'he' ), $O );
$l = nlrm_save( 'lease', array( 'unit_id' => $u['id'], 'status' => 'active', 'start_date' => nlrm_today(), 'end_date' => nlrm_add_days( nlrm_add_months( nlrm_today(), 12 ), -1 ), 'rent' => 5200, 'pay_day' => 1,
	'linkage' => array( 'mode' => 'none' ), 'securities' => array(), 'parties' => array( 'tenants' => array( $c['id'] ) ), 'terms' => array( 'method' => 'transfer' ) ), $O );
$lk = nlrm_link_create( $O, 'tenant', 'lease', (int) $l['id'], (int) $c['id'], 400 );
$row = $GLOBALS['wpdb']->get_row( $GLOBALS['wpdb']->prepare( 'SELECT * FROM ' . nlrm_t( 'links' ) . ' WHERE id = %d', $lk['id'] ), ARRAY_A );
foreach ( array( 'id', 'owner_id', 'scope_id', 'contact_id' ) as $k ) { $row[ $k ] = (int) $row[ $k ]; }
$act = function ( $act, $data, $ref = '' ) use ( $row ) { return nlrm_portal_act( $row, new WP_REST_Request( array( 'act' => $act, 'data' => $data, 'client_ref' => $ref ) ) ); };

$GLOBALS['sim_mail'] = array();
$act( 'ticket', array( 'title' => 'אין מים חמים בכלל' ) );
t( 'an urgent repair is mailed at once', 1 === count( $GLOBALS['sim_mail'] ) && false !== strpos( $GLOBALS['sim_mail'][0]['subject'], 'תקלה דחופה' ) && 'owner9@example.com' === $GLOBALS['sim_mail'][0]['to'], json_encode( $GLOBALS['sim_mail'], JSON_UNESCAPED_UNICODE ) );
t( 'it says where and the 3-day rule', false !== strpos( $GLOBALS['sim_mail'][0]['body'], 'דירה 4, הרצל 1' ) && false !== strpos( $GLOBALS['sim_mail'][0]['body'], '3 ימים' ) );
$act( 'ticket', array( 'title' => 'טפטוף בברז המטבח' ) );
$act( 'paid', array( 'amount' => 5200, 'date' => nlrm_today(), 'method' => 'transfer' ), 'c-pay-1' );
$act( 'paid', array( 'amount' => 5200, 'date' => nlrm_today(), 'method' => 'transfer' ), 'c-pay-1' ); /* the same tap, replayed */
$act( 'message', array( 'body' => 'שלום, הברז תוקן? תודה' ) );
t( 'standard events wait for the summary', 1 === count( $GLOBALS['sim_mail'] ) );
$q = (array) get_user_meta( $O, 'nlrm_notify_q', true );
t( 'three queued (the replayed payment once)', 3 === count( $q ), count( $q ) );
nlrm_notify_digest();
t( 'one summary mail', 2 === count( $GLOBALS['sim_mail'] ) && false !== strpos( $GLOBALS['sim_mail'][1]['subject'], '3 עדכונים' ), $GLOBALS['sim_mail'][1]['subject'] ?? '' );
$body = $GLOBALS['sim_mail'][1]['body'] ?? '';
t( 'the summary tells the payment, the repair and the message', false !== strpos( $body, '5,200 ₪' ) && false !== strpos( $body, 'טפטוף' ) && false !== strpos( $body, 'הברז תוקן' ) );
t( 'no phone and no ID number in any mail', ! array_filter( $GLOBALS['sim_mail'], function ( $m ) { return false !== strpos( $m['body'], '0501234567' ) || false !== strpos( $m['body'], '972501234567' ) || false !== strpos( $m['body'], '123456782' ); } ) );
t( 'the queue is empty after the summary', ! get_user_meta( $O, 'nlrm_notify_q', true ) );
nlrm_notify_digest();
t( 'no empty summary', 2 === count( $GLOBALS['sim_mail'] ) );
/* English landlord */
update_user_meta( $O, 'nlrm_lang', 'en' );
$act( 'ticket', array( 'title' => 'gas smell in the kitchen' ) );
t( 'in the landlord\'s language (en)', false !== strpos( end( $GLOBALS['sim_mail'] )['subject'], 'Urgent repair' ), end( $GLOBALS['sim_mail'] )['subject'] );
/* off */
update_user_meta( $O, 'nlrm_notify', 'off' );
$n = count( $GLOBALS['sim_mail'] );
$act( 'ticket', array( 'title' => 'אין מים חמים' ) );
$act( 'message', array( 'body' => 'hello' ) );
nlrm_notify_digest();
t( 'off in Settings: no mail at all', count( $GLOBALS['sim_mail'] ) === $n );
/* the setting through /rm/me */
$GLOBALS['sim_admin'] = false;
t( '/rm/me tells the setting', false === nlrm_me( $O )['notify'] );
echo "notify checks: $ok passed, $bad failed\n";
exit( $bad ? 1 : 0 );
