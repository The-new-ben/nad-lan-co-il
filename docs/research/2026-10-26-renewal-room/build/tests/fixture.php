<?php
/**
 * Sample data for the tests and the preview, built ONLY through the room's real REST routes (create, stage, one-apartment
 * saves on dated days, join, claim, approve, updates, deadlines), so the change log and the versions are what the code
 * writes. Everything is SAMPLE DATA ("נתוני דוגמה"): made-up streets ("רחוב הדוגמה"), initials for owners, example.org
 * emails. The organizer is "החברה המארגנת שלכם", never a real company.
 *
 *   rr_seed( $live_demo_json )  -> array of ids (org, complexes, rooms, users)
 */

const RR_U_ADMIN = 1, RR_U_ORGADMIN = 10, RR_U_FIELD = 11, RR_U_PM = 12, RR_U_NB = 20, RR_U_NB_PENDING = 21, RR_U_COMMITTEE = 22, RR_U_OUTSIDER = 30, RR_U_LEGACY = 40;

function rr_ok( $r, $what ) {
	if ( 200 !== $r[0] ) { file_put_contents( 'php://stderr', "seed step failed: $what -> " . json_encode( $r, JSON_UNESCAPED_UNICODE ) . "\n" ); exit( 2 ); }
	return $r[1];
}
function rr_users() {
	stub_user( RR_U_ADMIN, 'site-admin@example.org', 'מנהל האתר', array( 'manage_options' ) );
	stub_user( RR_U_ORGADMIN, 'michal@example.org', 'מיכל ל.' );
	stub_user( RR_U_FIELD, 'noa@example.org', 'נועה ש., רכזת שטח' );
	stub_user( RR_U_PM, 'avi@example.org', 'אבי מ., מנהל פרויקט' );
	stub_user( RR_U_NB, 'dayar7@example.net', 'דייר דירה 7' );
	stub_user( RR_U_NB_PENDING, 'dayar-b2@example.net', 'דיירת בבניין 2' );
	stub_user( RR_U_COMMITTEE, 'netzigut@example.net', 'חבר נציגות' );
	stub_user( RR_U_OUTSIDER, 'outsider@example.net', 'משתמש אחר' );
	stub_user( RR_U_LEGACY, 'vaad@example.net', 'ועד הבית' );
}

/* initials pool (no real names) */
function rr_initials( $i ) {
	$p = array( 'ר. כ.', 'מ. ל.', 'א. ב.', 'ש. ד.', 'י. פ.', 'נ. ג.', 'ת. ח.', 'ד. ס.', 'ע. מ.', 'ל. ר.', 'ב. ש.', 'ח. א.', 'ג. ו.', 'פ. ק.', 'ה. ז.', 'צ. ט.', 'ק. נ.', 'ס. ע.' );
	return $p[ $i % count( $p ) ];
}
/**
 * The plan of one building: a list of target states, top floor first is irrelevant; index = (floor-1)*upf + pos.
 * Codes: Y signed (all owners), P signed but one owner missing, I in process, D missing documents, R refused, U unreached.
 */
function rr_plan( $id, $bkey, $codes, $shares, &$k, $day0 ) {
	$notes = array( 'D' => 'ירושה: ממתינים לצו קיום צוואה', 'R' => 'ביקשו פגישה עם עורך הדין של הדיירים', 'I' => 'מתלבטים, לחזור אחרי האסיפה' );
	$contacts = array( 'מעדיפים וואטסאפ בערב', 'שיחה עם הבת, ימי שלישי', 'בעלים בחו"ל, דרך ייפוי כוח', 'להתקשר אחרי 18:00' );
	$staff = array( RR_U_FIELD, RR_U_PM );
	$apts = nadlan_rr_apartments( $id );
	$mine = array_values( array_filter( $apts, function ( $a ) use ( $bkey ) { return $a['building'] === $bkey; } ) );
	foreach ( $mine as $i => $a ) {
		$c = $codes[ $i ] ?? 'U';
		$k++;
		if ( 'U' === $c ) {
			if ( null !== $shares && isset( $shares[ $i ] ) ) { rr_save( $id, $a['id'], array( 'common_share' => $shares[ $i ] ), $staff[ $k % 2 ], $day0 ); }
			continue;
		}
		$n_owners = ( 0 === $k % 5 ) ? 2 : ( ( 0 === $k % 17 ) ? 3 : 1 );
		if ( 'P' === $c ) { $n_owners = 2; }
		$owners = array();
		for ( $o = 0; $o < $n_owners; $o++ ) {
			$owners[] = array( 'n' => rr_initials( $k * 3 + $o ), 'share' => $n_owners > 1 ? '1/' . $n_owners : '', 'heir' => 3 === $n_owners, 'signed' => false );
		}
		$day = $day0 + ( $k % 9 );
		// 1. first contact: in process, owners entered, a contact note
		rr_save( $id, $a['id'], array( 'consent_status' => 'in_process', 'owners' => $owners, 'contact_note' => $contacts[ $k % 4 ],
			'docs' => array( 'id_copy' => true ) ) + ( null !== $shares && isset( $shares[ $i ] ) ? array( 'common_share' => $shares[ $i ] ) : array() ), $staff[ $k % 2 ], $day );
		if ( 'I' === $c ) { if ( 0 === $k % 3 ) { rr_save( $id, $a['id'], array( 'note' => $notes['I'] ), $staff[ ( $k + 1 ) % 2 ], $day + 6 ); } continue; }
		if ( 'D' === $c ) { rr_save( $id, $a['id'], array( 'consent_status' => 'missing_docs', 'note' => $notes['D'] ), $staff[ ( $k + 1 ) % 2 ], $day + 9 ); continue; }
		if ( 'R' === $c ) { rr_save( $id, $a['id'], array( 'consent_status' => 'refused', 'note' => $notes['R'] ), $staff[ ( $k + 1 ) % 2 ], $day + 12 ); continue; }
		// signed: the owners sign (one stays unsigned for P), then status signed and the documents
		foreach ( $owners as $o => $ow ) { $owners[ $o ]['signed'] = ! ( 'P' === $c && 1 === $o ); }
		rr_save( $id, $a['id'], array( 'owners' => $owners, 'consent_status' => 'consented',
			'docs' => array( 'id_copy' => true, 'ownership_nesach' => 0 !== $k % 4, 'signed_agreement' => true, 'poa' => 0 !== $k % 3 ) ), $staff[ ( $k + 1 ) % 2 ], $day + 14 + ( $k % 11 ) );
	}
}
function rr_save( $id, $apt, $patch, $uid, $day ) {
	stub_as( $uid );
	stub_now( date( 'Y-m-d', strtotime( '2026-08-31 +' . (int) $day . ' days' ) ) . ' ' . sprintf( '%02d:%02d:00', 9 + ( $day % 9 ), ( $day * 7 ) % 60 ) );
	$cur = null;
	foreach ( nadlan_rr_apartments( $id ) as $a ) { if ( $a['id'] === $apt ) { $cur = $a; } }
	$r = stub_rest( 'POST', '/nadlan/v1/renewal-space/' . $id . '/apartment/' . $apt, $patch + array( 'v' => $cur['v'] ) );
	return rr_ok( $r, "save $apt" );
}

function rr_seed( $live_demo_json = null ) {
	rr_users();
	stub_now( '2026-06-01 09:00:00' );
	// the account: opened by the site admin, then its admin adds two staff members
	stub_as( RR_U_ADMIN );
	$org = rr_ok( stub_rest( 'POST', '/nadlan/v1/renewal-org', array( 'name' => 'החברה המארגנת שלכם', 'admin_email' => 'michal@example.org' ) ), 'org' );
	$org_id = $org['id'];
	stub_as( RR_U_ORGADMIN );
	rr_ok( stub_rest( 'POST', '/nadlan/v1/renewal-org/' . $org_id . '/staff', array( 'email' => 'noa@example.org', 'role' => 'staff' ) ), 'staff noa' );
	rr_ok( stub_rest( 'POST', '/nadlan/v1/renewal-org/' . $org_id . '/staff', array( 'email' => 'avi@example.org', 'role' => 'staff' ) ), 'staff avi' );

	// complex A: Petah Tikva, pinui-binui, 3 buildings x 16 = 48 apartments
	stub_now( '2026-06-10 10:00:00' );
	$a = rr_ok( stub_rest( 'POST', '/nadlan/v1/renewal-space', array( 'org_id' => $org_id, 'name' => 'מתחם הדוגמה', 'city' => 'פתח תקווה', 'track' => 'pinui_binui',
		'buildings' => array(
			array( 'label' => 'בניין 1', 'address' => 'רחוב הדוגמה 2', 'floors' => 4, 'upf' => 4 ),
			array( 'label' => 'בניין 2', 'address' => 'רחוב הדוגמה 4', 'floors' => 4, 'upf' => 4 ),
			array( 'label' => 'בניין 3', 'address' => 'רחוב הדוגמה 6', 'floors' => 4, 'upf' => 4 ),
		) ) ), 'complex A' )['id'];
	update_post_meta( $a, 'street_line', 'רחוב הדוגמה 2 עד 6' );
	// complex B: Kfar Saba, TAMA 38 demolish and rebuild, one building of 12
	$b = rr_ok( stub_rest( 'POST', '/nadlan/v1/renewal-space', array( 'org_id' => $org_id, 'name' => 'בניין הדוגמה 8', 'city' => 'כפר סבא', 'track' => 'tama38_2',
		'buildings' => array( array( 'label' => 'בניין', 'address' => 'רחוב הדוגמה 8', 'floors' => 4, 'upf' => 3 ) ) ) ), 'complex B' )['id'];
	// complex C: Hod HaSharon, pinui-binui, 2 buildings x 12 = 24, an early stage that needs attention
	$c = rr_ok( stub_rest( 'POST', '/nadlan/v1/renewal-space', array( 'org_id' => $org_id, 'name' => 'מתחם השקמים לדוגמה', 'city' => 'הוד השרון', 'track' => 'pinui_binui',
		'buildings' => array(
			array( 'label' => 'בניין א', 'address' => 'רחוב הדוגמה 1', 'floors' => 3, 'upf' => 4 ),
			array( 'label' => 'בניין ב', 'address' => 'רחוב הדוגמה 3', 'floors' => 3, 'upf' => 4 ),
		) ) ), 'complex C' )['id'];
	update_post_meta( $c, 'street_line', 'רחוב הדוגמה 1 עד 3' );
	foreach ( array( $a, $b, $c ) as $x ) { update_post_meta( $x, 'is_sample', '1' ); }

	// stages, as the staff set them on the day
	stub_as( RR_U_PM );
	foreach ( array( array( $a, 1, '2026-08-01 10:00:00' ), array( $a, 2, '2026-09-15 10:00:00' ), array( $b, 1, '2026-07-01 10:00:00' ), array( $b, 2, '2026-08-01 10:00:00' ), array( $b, 3, '2026-10-05 10:00:00' ), array( $c, 1, '2026-09-20 10:00:00' ) ) as $s ) {
		stub_now( $s[2] );
		rr_ok( stub_rest( 'POST', '/nadlan/v1/renewal-space/' . $s[0] . '/stage', array( 'stage' => $s[1] ) ), 'stage' );
	}

	// apartments, one save at a time, on dated days (September to late October)
	$k = 0;
	$sh1 = array(); for ( $i = 0; $i < 16; $i++ ) { $sh1[] = ( $i < 8 ? '62' : '63' ) . '/1000'; }
	$sh2 = array(); for ( $i = 0; $i < 10; $i++ ) { $sh2[] = '62/1000'; }
	rr_plan( $a, 'b1', str_split( 'YYYYUYYIYYPDYYIY' ), $sh1, $k, 5 );
	rr_plan( $a, 'b2', str_split( 'YYIYUYYRYDYPYIUY' ), $sh2, $k, 12 );
	rr_plan( $a, 'b3', str_split( 'YURYIDYUYUDYRIUY' ), null, $k, 20 );
	rr_plan( $b, 'b1', str_split( 'YYYYIYYDYUYY' ), null, $k, 2 );
	rr_plan( $c, 'b1', str_split( 'YUUIURUUYUDU' ), null, $k, 1 );
	rr_plan( $c, 'b2', str_split( 'UYUIUUYRUIUU' ), null, $k, 3 );

	// neighbours join with the invite link, claim their apartment; staff approve one, one waits; one is committee
	stub_as( RR_U_FIELD ); stub_now( '2026-10-02 12:00:00' );
	$join = rr_ok( stub_rest( 'POST', '/nadlan/v1/renewal-space/' . $a . '/invite' ), 'invite' );
	$tok = substr( $join['join_url'], strrpos( $join['join_url'], '=' ) + 1 );
	foreach ( array( array( RR_U_NB, 'b1-f2-3' ), array( RR_U_NB_PENDING, 'b2-f3-2' ), array( RR_U_COMMITTEE, 'b3-f1-1' ) ) as $j ) {
		stub_as( $j[0] );
		rr_ok( stub_rest( 'POST', '/nadlan/v1/renewal-join/' . $tok ), 'join' );
		rr_ok( stub_rest( 'POST', '/nadlan/v1/renewal-space/' . $a . '/claim', array( 'apt' => $j[1] ) ), 'claim' );
	}
	stub_as( RR_U_FIELD ); stub_now( '2026-10-03 09:30:00' );
	rr_ok( stub_rest( 'POST', '/nadlan/v1/renewal-space/' . $a . '/member', array( 'email' => 'dayar7@example.net', 'action' => 'approve' ) ), 'approve nb' );
	rr_ok( stub_rest( 'POST', '/nadlan/v1/renewal-space/' . $a . '/member', array( 'email' => 'netzigut@example.net', 'action' => 'approve' ) ), 'approve committee' );
	rr_ok( stub_rest( 'POST', '/nadlan/v1/renewal-space/' . $a . '/member', array( 'email' => 'netzigut@example.net', 'action' => 'committee' ) ), 'make committee' );

	// updates (oldest first) and deadlines
	$ups = array(
		array( $a, '2026-09-15 20:00:00', RR_U_PM, 'הנציגות נבחרה: שלושה נציגים, אחד מכל בניין. הפרוטוקול נשלח לכל הדיירים.' ),
		array( $a, '2026-10-20 11:00:00', RR_U_FIELD, 'נסחי טאבו התקבלו לעוד דירות בבניין 1. תודה לכל מי ששלח.' ),
		array( $a, '2026-10-24 18:00:00', RR_U_FIELD, 'אסיפת דיירים ביום שני 3.11 בשעה 19:00 בלובי של בניין 2. על סדר היום: מצב ההחתמות ושאלות לעורך הדין של הדיירים.' ),
		array( $b, '2026-10-06 10:00:00', RR_U_PM, 'הנציגות קיבלה שלוש הצעות מעורכי דין מטעם הדיירים. ההשוואה תוצג באסיפה.' ),
		array( $c, '2026-09-20 19:00:00', RR_U_PM, 'אסיפת דיירים ראשונה התקיימה. מתחילים לאסוף פרטי קשר של כל בעלי הדירות.' ),
	);
	foreach ( $ups as $u ) { stub_as( $u[2] ); stub_now( $u[1] ); rr_ok( stub_rest( 'POST', '/nadlan/v1/renewal-space/' . $u[0] . '/update', array( 'text' => $u[3] ) ), 'update' ); }
	stub_now( '2026-10-25 16:00:00' ); stub_as( RR_U_PM );
	rr_ok( stub_rest( 'POST', '/nadlan/v1/renewal-space/' . $a . '/deadline', array( 'label' => 'סוף תקופת ההחתמה לפי ההסכם עם החברה המארגנת', 'date' => '2026-11-20' ) ), 'dl1' );
	rr_ok( stub_rest( 'POST', '/nadlan/v1/renewal-space/' . $a . '/deadline', array( 'label' => 'אסיפת דיירים בלובי של בניין 2', 'date' => '2026-11-03' ) ), 'dl2' );
	rr_ok( stub_rest( 'POST', '/nadlan/v1/renewal-space/' . $c . '/deadline', array( 'label' => 'חידוש כתב המינוי של הנציגות', 'date' => '2026-10-20' ) ), 'dl3' );
	// complex C was last touched on 4.10: no activity since (it needs attention)
	update_post_meta( $c, 'renewal_last_activity', '2026-10-04 10:00:00' );

	// a committee room of one building, opened by a residents' committee (no organizer)
	stub_as( RR_U_LEGACY ); stub_now( '2026-09-01 10:00:00' );
	$legacy = rr_ok( stub_rest( 'POST', '/nadlan/v1/renewal-space', array( 'city' => 'גבעתיים', 'address' => 'רחוב הדוגמה 11', 'floors' => 3, 'units_per_floor' => 3, 'track' => 'tama38_1' ) ), 'legacy' )['id'];
	update_post_meta( $legacy, 'is_sample', '1' );

	// the public sample room exactly as the live site stores it (the v2 format, no Pro fields): proves legacy rows work
	$demo = 0;
	if ( $live_demo_json && is_readable( $live_demo_json ) ) {
		$d = json_decode( file_get_contents( $live_demo_json ), true );
		stub_as( RR_U_ADMIN ); stub_now( '2026-06-30 10:00:00' );
		$demo = wp_insert_post( array( 'post_type' => 'nadlan_renewal', 'post_status' => 'private', 'post_title' => $d['title'] ) );
		foreach ( array( 'address' => $d['address'], 'city' => $d['city'], 'floors' => $d['floors'], 'units_per_floor' => $d['units_per_floor'], 'track' => $d['track'], 'renewal_stage' => $d['stage'], 'is_demo' => '1' ) as $mk => $mv ) { update_post_meta( $demo, $mk, $mv ); }
		update_post_meta( $demo, 'renewal_apartments', json_encode( $d['apartments'], JSON_UNESCAPED_UNICODE ) );
		update_post_meta( $demo, 'renewal_updates', json_encode( $d['updates'], JSON_UNESCAPED_UNICODE ) );
		update_post_meta( $demo, 'renewal_stage_log', json_encode( array_reverse( $d['stage_log'] ), JSON_UNESCAPED_UNICODE ) );
	}
	stub_now( '2026-10-26 10:00:00' );
	stub_as( 0 );
	return array( 'org' => $org_id, 'a' => $a, 'b' => $b, 'c' => $c, 'legacy' => $legacy, 'demo' => $demo );
}
