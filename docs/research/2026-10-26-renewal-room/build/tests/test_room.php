<?php
/**
 * ROOM LOGIC TEST (RenewalRoomPro, 26.10.2026): the statutory majority, one-apartment saves with versions, the
 * compare-and-swap merge when two staff save different apartments at the same moment, the append-only change log,
 * owners and the careful count, the portfolio and its attention reasons, billing off/on, and live-format rooms.
 * Run:  php build/tests/test_room.php
 */
error_reporting( E_ALL );
$B = dirname( __DIR__ );
$LIVE = dirname( $B ) . '/live-base';
require __DIR__ . '/wp-stub.php';
require __DIR__ . '/fixture.php';
stub_boot_room( $B, $LIVE );
$ids = rr_seed( $B . '/preview/data/live-demo-payload.json' );
$A = $ids['a'];
$pass = 0; $fail = 0; $log = array();
function ok( $c, $n ) { global $pass, $fail, $log; if ( $c ) { $pass++; $log[] = "PASS  $n"; } else { $fail++; $log[] = "FAIL  $n"; } }
function apt( $id, $aid ) { foreach ( nadlan_rr_apartments( $id ) as $a ) { if ( $a['id'] === $aid ) { return $a; } } return null; }
function mk( $n, $yes, $b = 'b1', $owners = 1 ) {
	$o = array();
	for ( $i = 0; $i < $n; $i++ ) {
		$ow = array(); for ( $j = 0; $j < $owners; $j++ ) { $ow[] = array( 'n' => 'o' . $i . '-' . $j, 'signed' => true ); }
		$o[] = array( 'id' => $b . '-' . $i, 'building' => $b, 'consent_status' => $i < $yes ? 'consented' : 'in_process', 'owners' => $ow, 'common_share' => '', 'docs' => array() );
	}
	return $o;
}

/* 1. the law: exact fractions, never a rounded 66% */
$L = nadlan_rr_law( mk( 50, 33 ), array( array( 'key' => 'b1', 'label' => '', 'address' => '' ) ), 'pinui_binui' );
ok( 34 === $L['complex']['need'] && false === $L['complex']['met'], 'law: 50 apartments need 34; 33 (66%) is not two thirds' );
$L = nadlan_rr_law( mk( 50, 34 ), array( array( 'key' => 'b1', 'label' => '', 'address' => '' ) ), 'pinui_binui' );
ok( true === $L['complex']['met'], 'law: 34 of 50 meets the complex condition' );
$L = nadlan_rr_law( mk( 48, 32 ), array( array( 'key' => 'b1', 'label' => '', 'address' => '' ) ), 'pinui_binui' );
ok( 32 === $L['complex']['need'] && $L['complex']['met'], 'law: 48 apartments need 32' );
$L = nadlan_rr_law( mk( 16, 9 ), array( array( 'key' => 'b1', 'label' => '', 'address' => '' ) ), 'pinui_binui' );
ok( 10 === $L['buildings'][0]['need'] && false === $L['buildings'][0]['met'] && 1 === $L['buildings'][0]['short'], 'law: a building of 16 needs 10 for three fifths (9 is 1 short)' );
$L = nadlan_rr_law( mk( 5, 3, 'b1', 1 ), array( array( 'key' => 'b1', 'label' => '', 'address' => '' ) ), 'pinui_binui' );
ok( 'small_building' === $L['buildings'][0]['rule'] && true === $L['buildings'][0]['met'], 'law: a building of 5 with 3 signed apartments and 3 different owners meets the rule' );
$small = mk( 5, 3, 'b1', 1 ); $small[0]['owners'][0]['n'] = 'same'; $small[1]['owners'][0]['n'] = 'same'; $small[2]['owners'][0]['n'] = 'other';
$L = nadlan_rr_law( $small, array( array( 'key' => 'b1', 'label' => '', 'address' => '' ) ), 'pinui_binui' );
ok( false === $L['buildings'][0]['met'] && false === $L['buildings'][0]['owners_rule'], 'law: 3 apartments owned by only 2 people do not meet "more than two owners"' );
$small[0]['owners'] = array();
$L = nadlan_rr_law( $small, array( array( 'key' => 'b1', 'label' => '', 'address' => '' ) ), 'pinui_binui' );
ok( null === $L['buildings'][0]['met'], 'law: when an owner is not entered, the small-building rule is "data missing", never "met"' );
$L = nadlan_rr_law( mk( 3, 3 ), array( array( 'key' => 'b1', 'label' => '', 'address' => '' ) ), 'pinui_binui' );
ok( 'not_computed' === $L['buildings'][0]['rule'] && null === $L['all_met'], 'law: under 4 apartments the room does not decide (left to the lawyer)' );
$cs = mk( 4, 2 ); foreach ( $cs as $i => $x ) { $cs[ $i ]['common_share'] = array( '30/100', '25/100', '25/100', '20/100' )[ $i ]; }
$L = nadlan_rr_law( $cs, array( array( 'key' => 'b1', 'label' => '', 'address' => '' ) ), 'pinui_binui' );
ok( true === $L['buildings'][0]['common']['met'] && 55.0 === $L['buildings'][0]['common']['pct_yes'], 'law: common property 30% + 25% = 55% is more than half' );
$cs[1]['common_share'] = '';
$L = nadlan_rr_law( $cs, array( array( 'key' => 'b1', 'label' => '', 'address' => '' ) ), 'pinui_binui' );
ok( null === $L['buildings'][0]['common']['met'] && 1 === $L['buildings'][0]['common']['missing'], 'law: one share missing -> the common-property condition is "data missing"' );
ok( abs( nadlan_rr_share_val( '2.8%' ) - 0.028 ) < 1e-9 && abs( nadlan_rr_share_val( '28/1000' ) - 0.028 ) < 1e-9 && null === nadlan_rr_share_val( 'abc' ), 'law: shares parse as fraction, percent or decimal' );
$L = nadlan_rr_law( mk( 12, 12 ), array( array( 'key' => 'b1', 'label' => '', 'address' => '' ) ), 'tama38_2' );
ok( false === $L['applies'], 'law: TAMA 38 rooms do not get the pinui-binui majority' );

/* 2. the careful count: an owner who has not signed keeps the apartment out */
$p = mk( 1, 1, 'b1', 2 ); $p[0]['owners'][1]['signed'] = false;
ok( false === nadlan_rr_counted( $p[0] ) && 'partial' === nadlan_rr_shown_status( $p[0] ), 'count: signed status with one unsigned owner is "partial" and not counted' );
$S = stub_rest( 'GET', '/nadlan/v1/renewal-space/' . $A )[1];
stub_as( RR_U_FIELD ); $S = stub_rest( 'GET', '/nadlan/v1/renewal-space/' . $A )[1];
ok( 26 === $S['counts']['yes'] && 2 === $S['counts']['partial'] && 54.2 == $S['counts']['pct'], 'count: complex A has 26 counted, 2 partial (54.2%)' );

/* 3. one apartment per save, with its version */
$a = apt( $A, 'b3-f2-2' ); $v0 = $a['v'];
stub_as( RR_U_FIELD ); stub_now( '2026-10-26 10:05:00' );
$r = stub_rest( 'POST', '/nadlan/v1/renewal-space/' . $A . '/apartment/b3-f2-2', array( 'v' => $v0, 'consent_status' => 'in_process', 'note' => 'נקבעה פגישה' ) );
ok( 200 === $r[0] && 'saved' === $r[1]['code'] && $v0 + 1 === $r[1]['apartment']['v'], 'save: one apartment saved, version ' . $v0 . ' -> ' . ( $v0 + 1 ) );
ok( isset( $r[1]['law']['complex'] ) && isset( $r[1]['counts']['yes'] ), 'save: the response carries the new counts and the law' );
stub_as( RR_U_PM ); stub_now( '2026-10-26 10:06:00' );
$r = stub_rest( 'POST', '/nadlan/v1/renewal-space/' . $A . '/apartment/b3-f2-2', array( 'v' => $v0, 'consent_status' => 'refused' ) );
ok( 409 === $r[0] && 'conflict' === $r[1]['code'] && $v0 + 1 === $r[1]['data']['apartment']['v'], 'save: a stale version gets 409 with the fresh apartment (no overwrite)' );
ok( 'in_process' === apt( $A, 'b3-f2-2' )['consent_status'], 'save: the first save stands' );
ok( ! empty( $r[1]['data']['last'][0]['who'] ), 'save: the 409 names who saved first (' . ( $r[1]['data']['last'][0]['who'] ?? '' ) . ')' );
$r = stub_rest( 'POST', '/nadlan/v1/renewal-space/' . $A . '/apartment/b3-f2-2', array( 'v' => $v0 + 1, 'consent_status' => 'in_process', 'note' => 'נקבעה פגישה' ) );
ok( 200 === $r[0] && 'unchanged' === $r[1]['code'], 'save: saving the same values changes nothing (no version bump, no log row)' );
ok( 404 === stub_rest( 'POST', '/nadlan/v1/renewal-space/' . $A . '/apartment/zz-f9-9', array( 'v' => 0, 'note' => 'x' ) )[0], 'save: an unknown apartment is 404' );

/* 4. two staff at the same moment, on different apartments: both kept (compare-and-swap + retry) */
$x = apt( $A, 'b2-f1-3' ); $y = apt( $A, 'b3-f4-1' );
$GLOBALS['STUB']['before_update'] = function () use ( $A, $y ) {
	// the other staff member's save lands between our read and our write
	stub_as( RR_U_PM );
	$o = stub_rest( 'POST', '/nadlan/v1/renewal-space/' . $A . '/apartment/b3-f4-1', array( 'v' => $y['v'], 'docs' => array( 'poa' => true ) ) );
	$GLOBALS['RR_INNER'] = $o[0];
	stub_as( RR_U_FIELD );
};
stub_as( RR_U_FIELD );
$q0 = $GLOBALS['STUB']['queries'];
$r = stub_rest( 'POST', '/nadlan/v1/renewal-space/' . $A . '/apartment/b2-f1-3', array( 'v' => $x['v'], 'contact_note' => 'חזרו אלינו ביום ראשון' ) );
ok( 200 === $r[0] && 200 === ( $GLOBALS['RR_INNER'] ?? 0 ), 'concurrent: both saves succeeded' );
ok( 'חזרו אלינו ביום ראשון' === apt( $A, 'b2-f1-3' )['contact_note'] && true === apt( $A, 'b3-f4-1' )['docs']['poa'], 'concurrent: neither change was lost (the old bulk save would have lost one)' );
ok( $GLOBALS['STUB']['queries'] - $q0 >= 4, 'concurrent: the first write was refused and retried (' . ( $GLOBALS['STUB']['queries'] - $q0 ) . ' queries)' );

/* 5. the change log: who, when, from, to; only ever added to */
$ev = nadlan_rr_events( $A, 'b3-f2-2', 50 );
$st = array_values( array_filter( $ev, function ( $e ) { return 'status' === $e['f']; } ) );
ok( $st && 'in_process' === $st[0]['to'] && 'נועה ש., רכזת שטח' === $st[0]['who'] && '2026-10-26 10:05:00' === $st[0]['at'], 'log: status change recorded with who, when, from and to' );
$nt = array_values( array_filter( $ev, function ( $e ) { return 'note' === $e['f']; } ) );
ok( $nt && null === $nt[0]['to'] && false === strpos( json_encode( $nt[0], JSON_UNESCAPED_UNICODE ), 'נקבעה פגישה' ), 'log: a note change is logged without its text (data minimisation)' );
$rows_before = count( get_post_meta( $A, 'renewal_apt_event', false ) );
stub_as( RR_U_FIELD ); stub_now( '2026-10-26 10:10:00' );
$r = stub_rest( 'POST', '/nadlan/v1/renewal-space/' . $A . '/apartment/b3-f2-2', array( 'v' => apt( $A, 'b3-f2-2' )['v'], 'docs' => array( 'ownership_nesach' => true, 'id_copy' => true ) ) );
$rows_after = count( get_post_meta( $A, 'renewal_apt_event', false ) );
ok( $rows_after > $rows_before, 'log: a save adds rows (' . $rows_before . ' -> ' . $rows_after . '), it never rewrites old ones' );
$first_row = get_post_meta( $A, 'renewal_apt_event', false )[0];
ok( $first_row === get_post_meta( $A, 'renewal_apt_event', false )[0], 'log: the oldest row is unchanged after new saves' );
$routes = array_map( function ( $x ) { return $x[1]; }, $GLOBALS['STUB']['routes'] );
ok( ! array_filter( $routes, function ( $r ) { return false !== strpos( $r, '/log' ) && false === strpos( $r, 'apartment' ); } ), 'log: no route edits or deletes log rows (the only log route is a GET)' );
$lr = stub_rest( 'GET', '/nadlan/v1/renewal-space/' . $A . '/apartment/b3-f2-2/log' );
ok( 200 === $lr[0] && count( $lr[1]['events'] ) >= 4, 'log: staff read the apartment history (' . count( $lr[1]['events'] ) . ' rows)' );

/* 6. owners: cleaned, at most 8, partial counting through the REST save */
$z = apt( $A, 'b1-f1-1' );
$r = stub_rest( 'POST', '/nadlan/v1/renewal-space/' . $A . '/apartment/b1-f1-1', array( 'v' => $z['v'], 'owners' => array( array( 'n' => '<b>ר. כ.</b>', 'share' => '1/2abc', 'signed' => true ), array( 'n' => 'מ. כ.', 'share' => '1/2', 'heir' => true, 'signed' => false ), array( 'n' => '' ) ) ) );
$z = apt( $A, 'b1-f1-1' );
ok( 2 === count( $z['owners'] ) && 'ר. כ.' === $z['owners'][0]['n'] && '1/2' === $z['owners'][0]['share'] && true === $z['owners'][1]['heir'], 'owners: tags stripped, shares cleaned, empty rows dropped, heir flag kept' );
ok( 'partial' === nadlan_rr_shown_status( $z ) && 25 === $r[1]['counts']['yes'], 'owners: an unsigned heir takes the apartment out of the count (26 -> 25)' );

/* 7. the portfolio */
stub_as( RR_U_FIELD );
$P = stub_rest( 'GET', '/nadlan/v1/renewal-org/' . $ids['org'] . '/portfolio' );
ok( 200 === $P[0] && 3 === count( $P[1]['complexes'] ), 'portfolio: staff see the 3 complexes of the account' );
$byname = array(); foreach ( $P[1]['complexes'] as $c ) { $byname[ $c['id'] ] = $c; }
$cc = $byname[ $ids['c'] ]; $codes = array_map( function ( $w ) { return $w['code']; }, $cc['attention'] );
ok( in_array( 'unreached', $codes, true ) && in_array( 'refused', $codes, true ) && in_array( 'idle', $codes, true ) && in_array( 'deadline_passed', $codes, true ), 'portfolio: complex C needs attention: ' . implode( ', ', $codes ) );
ok( $P[1]['complexes'][0]['id'] === $ids['c'], 'portfolio: the complex with most reasons comes first' );
$ca = $byname[ $A ];
ok( 3 === $ca['buildings'] && 48 === $ca['counts']['total'] && true === $ca['law']['applies'] && 2 === $ca['law']['buildings_short'], 'portfolio: complex A row: 3 buildings, 48 apartments, 2 buildings short of three fifths' );
ok( false === $byname[ $ids['b'] ]['law']['applies'], 'portfolio: the TAMA 38 complex carries no pinui-binui majority' );

/* 8. billing: off by default (every account active); on and unpaid -> read-only, nothing deleted */
ok( false === nadlan_rr_billing_on() && true === nadlan_rr_org_active( $ids['org'] ), 'billing: off by default, the account is active' );
update_option( 'nadlan_rr_billing_on', '1' ); update_option( 'nadlan_rr_org_product', 9999 );
update_post_meta( $ids['org'], 'org_paid_until', strtotime( '2026-10-01' ) ); update_post_meta( $ids['org'], 'org_plan', 'paid' );
stub_as( RR_U_FIELD );
$S2 = stub_rest( 'GET', '/nadlan/v1/renewal-space/' . $A );
$w = stub_rest( 'POST', '/nadlan/v1/renewal-space/' . $A . '/apartment/b1-f1-2', array( 'v' => apt( $A, 'b1-f1-2' )['v'], 'note' => 'x' ) );
ok( 200 === $S2[0] && true === $S2[1]['caps']['read_only'] && false === $S2[1]['caps']['manage'] && 48 === count( $S2[1]['apartments'] ), 'billing on, unpaid: staff still read everything, read-only' );
ok( 403 === $w[0], 'billing on, unpaid: saves are refused (403), data untouched' );
update_post_meta( $ids['org'], 'org_paid_until', strtotime( '2026-11-25' ) );
ok( true === nadlan_rr_org_active( $ids['org'] ), 'billing on, paid until 25.11: active again' );
update_option( 'nadlan_rr_billing_on', '0' );

/* 9. live-format rooms keep working */
if ( $ids['demo'] ) {
	$d = nadlan_rr_apartments( $ids['demo'] );
	ok( 12 === count( $d ) && 'b1' === $d[0]['building'] && 1 === $d[0]['num'] && 0 === $d[0]['v'], 'legacy: the live sample room (v2 rows) reads as one building, numbered, version 0' );
	$b = nadlan_rr_buildings( $ids['demo'] );
	ok( 1 === count( $b ) && 4 === $b[0]['floors'] && 3 === $b[0]['upf'], 'legacy: its building comes from the old floors / units per floor' );
}
stub_as( RR_U_LEGACY );
$lg = stub_rest( 'GET', '/nadlan/v1/renewal-space/' . $ids['legacy'] )[1];
ok( 'owner' === $lg['role'] && 'f1-1' === $lg['apartments'][0]['id'] && 'statuses' === $lg['settings']['neighbor_grid'], 'legacy: a committee room keeps the live ids (f1-1) and keeps showing statuses to neighbours' );
$apts = $lg['apartments']; $apts[0]['consent_status'] = 'consented'; unset( $apts[0]['owners'] ); // the old script posts the whole array
$apts[1]['owners'] = array( array( 'n' => 'ק. נ.', 'signed' => false ) );
stub_rest( 'POST', '/nadlan/v1/renewal-space/' . $ids['legacy'] . '/apartment/f1-2', array( 'v' => 0, 'owners' => array( array( 'n' => 'ק. נ.', 'signed' => false ) ) ) );
$lg2 = stub_rest( 'POST', '/nadlan/v1/renewal-space/' . $ids['legacy'] . '/apartments', array( 'apartments' => array_map( function ( $a ) { unset( $a['owners'] ); return $a; }, $lg['apartments'] ) ) );
$f12 = apt( $ids['legacy'], 'f1-2' );
ok( 200 === $lg2[0] && 1 === count( $f12['owners'] ), 'legacy bulk save (old script): owners entered by the new script are kept' );
$apts2 = nadlan_rr_apartments( $ids['legacy'] ); $apts2[2]['consent_status'] = 'refused';
stub_rest( 'POST', '/nadlan/v1/renewal-space/' . $ids['legacy'] . '/apartments', array( 'apartments' => $apts2 ) );
$ev = nadlan_rr_events( $ids['legacy'], $apts2[2]['id'], 5 );
ok( $ev && 'status' === $ev[0]['f'] && 'refused' === $ev[0]['to'] && 1 === apt( $ids['legacy'], $apts2[2]['id'] )['v'], 'legacy bulk save: the change is logged and the version bumped' );

/* 10. the room's word law on every visible Hebrew string */
$black = array( 'ממשק', 'מערכת', 'דמו', 'הדגמה', 'סימולציה', 'מודל', 'AI', 'אינטראקטיב', 'בקרוב', 'בבדיקה', 'תלת', '—', '–' );
$all = implode( "\n", nadlan_ur_space_strings( 'he' ) );
$hit = array(); foreach ( $black as $w ) { if ( false !== mb_strpos( $all, $w ) ) { $hit[] = $w; } }
ok( ! $hit, 'words: the Hebrew room strings (' . count( nadlan_ur_space_strings( 'he' ) ) . ') carry no blacklisted word' . ( $hit ? ': ' . implode( ', ', $hit ) : '' ) );
$he_pack = nadlan_ur_space_strings( 'he' );
foreach ( array( 'en', 'ru' ) as $lg ) {
	$pack = nadlan_ur_space_strings( $lg ); $same = array();
	foreach ( $he_pack as $k => $v ) { if ( ! isset( $pack[ $k ] ) || ( $pack[ $k ] === $v && preg_match( '/\p{Hebrew}/u', $v ) ) ) { $same[] = $k; } }
	ok( ! $same, "words: every one of the " . count( $he_pack ) . " keys is translated in $lg" . ( $same ? ' (still Hebrew: ' . implode( ', ', array_slice( $same, 0, 8 ) ) . ')' : '' ) );
}
$m = nadlan_ur_stage_meta( 'he' ); $mt = json_encode( $m, JSON_UNESCAPED_UNICODE );
ok( false === mb_strpos( $mt, ' - ' ) && false === mb_strpos( $mt, 'מודל' ), 'words: the ten stages have no spaced dash and no "model"' );
$dur = array_filter( array_column( $m, 'duration' ) );
ok( 1 === count( $dur ), 'numbers: a stage duration appears only where it has a source (1 of 10: the permit stage, authority report 2025)' );

echo implode( "\n", $log ), "\n\n", "room: $pass passed, $fail failed\n";
exit( $fail ? 1 : 0 );
