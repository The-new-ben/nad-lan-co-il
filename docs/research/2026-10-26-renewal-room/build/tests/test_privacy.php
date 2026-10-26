<?php
/**
 * PRIVACY TEST (RenewalRoomPro, 26.10.2026). Runs the room's real payload code (build/inc) through the WordPress stand-in.
 * Proves: a neighbour receives the building totals, the stage, the updates and THEIR OWN apartment only, and never another
 * apartment's note, contact note or owner names (nor the members list, the change log, staff names or user ids); the
 * committee sees statuses and document ticks but no names and no notes; outsiders and anonymous visitors get nothing; the
 * public demo route carries no private field. Run:  php build/tests/test_privacy.php
 */
error_reporting( E_ALL );
$B = dirname( __DIR__ );
$LIVE = dirname( $B ) . '/live-base';
require __DIR__ . '/wp-stub.php';
require __DIR__ . '/fixture.php';
stub_boot_room( $B, $LIVE );
$demo_json = getenv( 'RR_DEMO_JSON' ) ?: ( $B . '/preview/data/live-demo-payload.json' );
$ids = rr_seed( $demo_json );
$A = $ids['a'];

$pass = 0; $fail = 0; $log = array();
function ok( $cond, $name ) { global $pass, $fail, $log; if ( $cond ) { $pass++; $log[] = "PASS  $name"; } else { $fail++; $log[] = "FAIL  $name"; } }
function payload_as( $uid, $id ) { stub_as( $uid ); $r = stub_rest( 'GET', '/nadlan/v1/renewal-space/' . $id ); return $r; }
/** true if $needle appears in the JSON $hay, raw or JSON-escaped (a quote in Hebrew text, as in בחו"ל, is escaped in JSON) */
function in_json( $hay, $needle ) { return false !== mb_strpos( $hay, $needle ) || false !== mb_strpos( $hay, mb_substr( json_encode( $needle, JSON_UNESCAPED_UNICODE ), 1, -1 ) ); }
function has_key_deep( $x, $k ) { if ( ! is_array( $x ) ) { return false; } foreach ( $x as $kk => $v ) { if ( $kk === $k ) { return true; } if ( is_array( $v ) && has_key_deep( $v, $k ) ) { return true; } } return false; }

/* the private strings that exist in complex A (read straight from storage) */
$secret = array();
foreach ( nadlan_rr_apartments( $A ) as $a ) {
	if ( '' !== $a['note'] ) { $secret[ 'note:' . $a['note'] ] = $a['note']; }
	if ( '' !== $a['contact_note'] ) { $secret[ 'contact:' . $a['contact_note'] ] = $a['contact_note']; }
	foreach ( $a['owners'] as $o ) { $secret[ 'owner:' . $o['n'] ] = $o['n']; }
}
foreach ( array( RR_U_FIELD, RR_U_PM, RR_U_ORGADMIN ) as $u ) { $secret[ 'staff:' . $u ] = get_userdata( $u )->display_name; $secret[ 'staffmail:' . $u ] = get_userdata( $u )->user_email; }
$secret['other-member-mail'] = 'dayar-b2@example.net';
ok( count( $secret ) >= 20, 'fixture has private strings to look for (' . count( $secret ) . ')' );

/* 1. a manager (organizer staff) gets everything */
$r = payload_as( RR_U_FIELD, $A );
ok( 200 === $r[0], 'staff: GET room 200' );
$S = $r[1];
ok( 'org' === $S['role'] && $S['caps']['manage'], 'staff: role org, can manage' );
ok( 48 === count( $S['apartments'] ), 'staff: all 48 apartments' );
ok( has_key_deep( $S['apartments'], 'note' ) && has_key_deep( $S['apartments'], 'contact_note' ) && has_key_deep( $S['apartments'], 'owners' ), 'staff: notes, contact notes and owners present' );
ok( ! empty( $S['members'] ) && ! empty( $S['events_recent'] ), 'staff: members list and change log present' );
/* control: the same leak detector DOES find the private strings in the managers' payload (so a pass below means something) */
$SJ = json_encode( $S, JSON_UNESCAPED_UNICODE ); $found = 0;
foreach ( $secret as $k => $v ) { if ( 0 !== strpos( $k, 'staff' ) && in_json( $SJ, $v ) ) { $found++; } }
$nonstaff = count( array_filter( array_keys( $secret ), function ( $k ) { return 0 !== strpos( $k, 'staff' ); } ) );
ok( $found === $nonstaff, "control: the detector finds all $nonstaff note/contact/owner/member strings in the staff payload ($found)" );
file_put_contents( $B . '/preview/data/payload-staff.json', json_encode( $S, JSON_UNESCAPED_UNICODE | JSON_PRETTY_PRINT ) );

/* 2. an approved neighbour (apartment 7, building 1), organizer room default = totals only */
$r = payload_as( RR_U_NB, $A );
ok( 200 === $r[0], 'neighbour: GET room 200' );
$N = $r[1];
$NJ = json_encode( $N, JSON_UNESCAPED_UNICODE );
ok( 'neighbor' === $N['role'] && ! $N['caps']['manage'] && ! $N['caps']['private'], 'neighbour: role neighbor, no manage, no private' );
ok( 'totals' === $N['settings']['neighbor_grid'] && 0 === count( $N['apartments'] ), 'neighbour: organizer room shows totals only (0 apartments in the grid)' );
ok( 1 === count( $N['mine'] ) && 'b1-f2-3' === $N['mine'][0]['id'], 'neighbour: exactly their own apartment (b1-f2-3)' );
ok( ! has_key_deep( $N['mine'], 'owners' ) && ! has_key_deep( $N['mine'], 'note' ) && ! has_key_deep( $N['mine'], 'contact_note' ), 'neighbour: own apartment without owner names, note or contact note' );
ok( isset( $N['counts']['total'] ) && 48 === $N['counts']['total'] && isset( $N['law']['complex'] ), 'neighbour: building totals and the law block present' );
ok( ! isset( $N['members'] ) && ! isset( $N['events_recent'] ) && ! isset( $N['join_url'] ) && ! isset( $N['deadlines'] ), 'neighbour: no members, change log, invite link or deadlines' );
$leaks = array(); foreach ( $secret as $k => $v ) { if ( in_json( $NJ, $v ) ) { $leaks[] = $k; } }
ok( ! $leaks, 'neighbour JSON contains none of ' . count( $secret ) . ' private strings' . ( $leaks ? ' LEAKS: ' . implode( ', ', array_slice( $leaks, 0, 5 ) ) : '' ) );
ok( false === strpos( $NJ, '"by"' ) && false === strpos( $NJ, '"by_name"' ) && false === strpos( $NJ, '"updated_by"' ), 'neighbour: no user ids or author names on updates and stages' );
ok( false === strpos( $NJ, 'common_share' ) && false === strpos( $NJ, '"v":' ), 'neighbour: no common-property shares, no versions' );
file_put_contents( $B . '/preview/data/payload-neighbor.json', json_encode( $N, JSON_UNESCAPED_UNICODE | JSON_PRETTY_PRINT ) );

/* 3. the same neighbour when the organizer lets neighbours see every apartment's status */
stub_as( RR_U_FIELD );
ok( 200 === stub_rest( 'POST', '/nadlan/v1/renewal-space/' . $A . '/settings', array( 'neighbor_grid' => 'statuses' ) )[0], 'staff: switch neighbour grid to statuses' );
$r = payload_as( RR_U_NB, $A ); $N2 = $r[1]; $N2J = json_encode( $N2, JSON_UNESCAPED_UNICODE );
ok( 48 === count( $N2['apartments'] ), 'neighbour (statuses mode): 48 cells' );
$bad = 0; foreach ( $N2['apartments'] as $a ) { foreach ( array( 'note', 'contact_note', 'owners', 'common_share', 'v', 'docs', 'updated_by' ) as $k ) { if ( array_key_exists( $k, $a ) ) { $bad++; } } }
ok( 0 === $bad, 'neighbour (statuses mode): every cell carries only id, building, floor, number and status' );
$leaks = array(); foreach ( $secret as $k => $v ) { if ( in_json( $N2J, $v ) ) { $leaks[] = $k; } }
ok( ! $leaks, 'neighbour (statuses mode) JSON contains no private string' . ( $leaks ? ' LEAKS: ' . implode( ', ', $leaks ) : '' ) );
stub_as( RR_U_FIELD ); stub_rest( 'POST', '/nadlan/v1/renewal-space/' . $A . '/settings', array( 'neighbor_grid' => 'totals' ) );

/* 4. a neighbour whose claim waits for approval */
$r = payload_as( RR_U_NB_PENDING, $A ); $P = $r[1];
ok( 0 === count( $P['mine'] ) && 'pending' === $P['my_claim']['state'], 'pending neighbour: no apartment shown until approved' );
$leaks = array(); foreach ( $secret as $k => $v ) { if ( 'other-member-mail' !== $k && in_json( json_encode( $P, JSON_UNESCAPED_UNICODE ), $v ) ) { $leaks[] = $k; } }
ok( ! $leaks, 'pending neighbour JSON contains no private string' );
file_put_contents( $B . '/preview/data/payload-neighbor-pending.json', json_encode( $P, JSON_UNESCAPED_UNICODE | JSON_PRETTY_PRINT ) );

/* 5. the committee: statuses and document ticks, no names, no notes */
$r = payload_as( RR_U_COMMITTEE, $A ); $C = $r[1]; $CJ = json_encode( $C, JSON_UNESCAPED_UNICODE );
ok( 'committee' === $C['role'] && $C['caps']['post_updates'] && ! $C['caps']['manage'], 'committee: posts updates, cannot manage' );
ok( 48 === count( $C['apartments'] ) && has_key_deep( $C['apartments'], 'docs' ), 'committee: 48 cells with document ticks' );
ok( ! has_key_deep( $C['apartments'], 'note' ) && ! has_key_deep( $C['apartments'], 'contact_note' ) && ! has_key_deep( $C['apartments'], 'owners' ), 'committee: no notes, contact notes or owners' );
$leaks = array(); foreach ( $secret as $k => $v ) { if ( in_json( $CJ, $v ) ) { $leaks[] = $k; } }
ok( ! $leaks, 'committee JSON contains no private string' . ( $leaks ? ' LEAKS: ' . implode( ', ', $leaks ) : '' ) );
file_put_contents( $B . '/preview/data/payload-committee.json', json_encode( $C, JSON_UNESCAPED_UNICODE | JSON_PRETTY_PRINT ) );

/* 6. writes by role */
stub_as( RR_U_NB );
ok( 403 === stub_rest( 'POST', '/nadlan/v1/renewal-space/' . $A . '/apartment/b1-f2-3', array( 'consent_status' => 'refused', 'v' => 9 ) )[0], 'neighbour cannot save an apartment (403)' );
ok( 403 === stub_rest( 'POST', '/nadlan/v1/renewal-space/' . $A . '/update', array( 'text' => 'x' ) )[0], 'neighbour cannot post an update (403)' );
ok( 403 === stub_rest( 'GET', '/nadlan/v1/renewal-space/' . $A . '/apartment/b1-f2-3/log' )[0], 'neighbour cannot read the change log (403)' );
stub_as( RR_U_COMMITTEE );
ok( 403 === stub_rest( 'POST', '/nadlan/v1/renewal-space/' . $A . '/apartment/b1-f1-1', array( 'consent_status' => 'refused', 'v' => 1 ) )[0], 'committee cannot save an apartment (403)' );
ok( 200 === stub_rest( 'POST', '/nadlan/v1/renewal-space/' . $A . '/update', array( 'text' => 'עדכון מהנציגות: האסיפה הבאה תתקיים בבניין 2.' ) )[0], 'committee can post an update (200)' );
ok( 403 === stub_rest( 'POST', '/nadlan/v1/renewal-space/' . $A . '/member', array( 'email' => 'dayar-b2@example.net', 'action' => 'approve' ) )[0], 'committee cannot approve claims (403)' );
stub_as( RR_U_OUTSIDER );
ok( 403 === payload_as( RR_U_OUTSIDER, $A )[0], 'a logged-in outsider cannot open the room (403)' );
ok( 403 === stub_rest( 'GET', '/nadlan/v1/renewal-org/' . $ids['org'] . '/portfolio' )[0], 'an outsider cannot read the portfolio (403)' );
stub_as( 0 );
ok( 401 === stub_rest( 'GET', '/nadlan/v1/renewal-space/' . $A )[0], 'anonymous cannot open the room (401)' );
stub_as( RR_U_NB );
ok( 403 === stub_rest( 'GET', '/nadlan/v1/renewal-org/' . $ids['org'] . '/portfolio' )[0], 'a neighbour cannot read the portfolio (403)' );
stub_as( RR_U_LEGACY );
ok( 403 === payload_as( RR_U_LEGACY, $A )[0], 'another room\'s owner cannot open this room (403)' );

/* 7. the public demo route */
if ( $ids['demo'] ) {
	stub_as( 0 ); delete_transient( 'nlur_demo_payload_he' );
	$r = stub_rest( 'GET', '/nadlan/v1/renewal-demo' ); $D = $r[1];
	ok( 200 === $r[0] && 12 === count( $D['apartments'] ), 'demo: public, 12 apartments of the live sample room' );
	ok( ! has_key_deep( $D['apartments'], 'note' ) && ! has_key_deep( $D['apartments'], 'contact_note' ) && ! has_key_deep( $D['apartments'], 'owners' ) && false === $D['can_manage'], 'demo: no private field, not editable' );
	ok( false === strpos( json_encode( $D ), '"by"' ), 'demo: no user ids' );
	file_put_contents( $B . '/preview/data/payload-demo.json', json_encode( $D, JSON_UNESCAPED_UNICODE | JSON_PRETTY_PRINT ) );
}

echo implode( "\n", $log ), "\n\n", "privacy: $pass passed, $fail failed\n";
exit( $fail ? 1 : 0 );
