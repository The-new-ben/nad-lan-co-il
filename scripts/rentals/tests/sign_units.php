<?php
/* B22: a signature keeps the EXACT signed text. nlrm_sign stores the text the tenant saw, the name, the time, the drawn
   signature and the text's SHA-256 as an encrypted document of the lease; a later template change never alters it.
   php -d extension=pdo_sqlite -d extension=sodium scripts/rentals/tests/sign_units.php */
require __DIR__ . '/../sim/wp_shim.php';
$tmp = sys_get_temp_dir() . '/nlrm-sign-' . getmypid();
sim_boot( ':memory:', $tmp );
nlrm_install();
$ok = 0; $bad = 0;
function t( $name, $cond, $info = '' ) { global $ok, $bad; if ( $cond ) { $ok++; } else { $bad++; echo "FAIL $name $info\n"; } }

$O = 9;
$GLOBALS['sim_user'] = $O;
$p = nlrm_save( 'property', array( 'title' => '', 'address' => 'הרצל 1', 'city' => 'חיפה', 'floors' => 3, 'units_per_floor' => 2 ), $O );
$u = nlrm_save( 'unit', array( 'property_id' => $p['id'], 'label' => 'דירה 1', 'floor' => 1, 'pos' => 0 ), $O );
$c = nlrm_save( 'contact', array( 'kind' => 'tenant', 'name' => 'דנה <b>כהן</b>', 'phone' => '0501234567', 'lang' => 'he' ), $O );
$start = nlrm_today();
$l = nlrm_save( 'lease', array( 'unit_id' => $u['id'], 'status' => 'draft', 'start_date' => $start, 'end_date' => nlrm_add_days( nlrm_add_months( $start, 12 ), -1 ), 'rent' => 5200, 'pay_day' => 1,
	'linkage' => array( 'mode' => 'none' ), 'securities' => array(), 'parties' => array( 'tenants' => array( $c['id'] ) ), 'terms' => array( 'method' => 'transfer' ) ), $O );
$lk = nlrm_link_create( $O, 'sign', 'lease', (int) $l['id'], (int) $c['id'], 14 );
$row = $GLOBALS['wpdb']->get_row( $GLOBALS['wpdb']->prepare( 'SELECT * FROM ' . nlrm_t( 'links' ) . ' WHERE id = %d', $lk['id'] ), ARRAY_A );
$row['id'] = (int) $row['id']; $row['owner_id'] = (int) $row['owner_id']; $row['scope_id'] = (int) $row['scope_id']; $row['contact_id'] = (int) $row['contact_id'];
$png = 'data:image/png;base64,' . base64_encode( str_repeat( 'x', 300 ) );
$text_before = nlrm_lease_text( $O, nlrm_get( 'lease', (int) $l['id'], $O ), 'he' );
$res = nlrm_sign( $row, array( 'name' => 'דנה כהן', 'signature' => $png, 'agree' => 1 ) );
t( 'the tenant signs', is_array( $res ) && ! empty( $res['signed'] ), is_wp_error( $res ) ? $res->get_error_message() : json_encode( $res ) );
$lease = nlrm_get( 'lease', (int) $l['id'], $O );
$party = (array) ( (array) $lease['signing'] )['parties'][0];
t( 'the signing points to a document', ! empty( $party['doc_id'] ), json_encode( array_keys( $party ) ) );
$doc = $GLOBALS['wpdb']->get_row( $GLOBALS['wpdb']->prepare( 'SELECT * FROM ' . nlrm_t( 'docs' ) . ' WHERE id = %d', (int) ( $party['doc_id'] ?? 0 ) ), ARRAY_A );
t( 'a lease document, encrypted at rest, of this lease', $doc && 'lease' === $doc['kind'] && 'lease' === $doc['scope'] && (int) $doc['scope_id'] === (int) $l['id'] && 1 === (int) $doc['enc'] && 0 === strpos( $doc['mime'], 'text/html' ) );
$blob = file_get_contents( nlrm_private_dir() . $doc['path'] );
t( 'the file on disk is not readable text', false === strpos( $blob, 'הואיל' ) && false === strpos( $blob, 'דנה' ) );
$html = nlrm_blob_dec( $blob );
t( 'it holds the exact text: every clause heading', (bool) $html && count( array_filter( $text_before['sections'], function ( $s ) use ( $html ) { return false === strpos( $html, esc_html( $s['h'] ) ); } ) ) === 0 );
t( 'it holds the signer, the signature image and the fingerprint', $html && false !== strpos( $html, 'דנה כהן' ) && false !== strpos( $html, $png ) && false !== strpos( $html, $res['sha256'] ) );
t( 'the fingerprint is the signed text\'s', $res['sha256'] === hash( 'sha256', wp_json_encode( $text_before, JSON_UNESCAPED_UNICODE ) ) );
t( 'names are escaped (no markup from a contact)', false === strpos( $html, '<b>כהן</b>' ) );
t( 'the document sha256 matches its bytes', hash( 'sha256', $html ) === $doc['sha256'] );
/* the template changes later: the stored document does not */
$T = nlrm_json( 'lease' );
t( 'the template is versioned 2026-10-03.1', '2026-10-03.1' === $T['version'], $T['version'] );
t( 'clause numbers run in order', '1. ' === mb_substr( $text_before['sections'][1]['h'], 0, 3 ) );
echo "sign checks: $ok passed, $bad failed\n";
exit( $bad ? 1 : 0 );
