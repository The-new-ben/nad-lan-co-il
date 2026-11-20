<?php
/* Unit checks for inc/rentals/store.php and portal.php helpers, on the sim shim (SQLite in memory). */
require __DIR__ . '/../sim/wp_shim.php';
$tmp = sys_get_temp_dir() . '/nlrm-units-' . getmypid();
sim_boot( ':memory:', $tmp );
nlrm_install();
$ok = 0; $bad = 0;
function t( $name, $cond, $info = '' ) { global $ok, $bad; if ( $cond ) { $ok++; } else { $bad++; echo "FAIL $name $info\n"; } }
$s = 'דני כהן · 050-1234567 · Daniel';
$e = nlrm_enc( $s ); t( 'enc prefix names the key', 0 === strpos( $e, ( function_exists( 'sodium_crypto_secretbox' ) ? 's2:' : 'g2:' ) . nlrm_keyring()['cur'] . ':' ), $e );
t( 'enc round trip', nlrm_dec( $e ) === $s );
t( 'enc is randomised', nlrm_enc( $s ) !== $e );
t( 'enc empty', '' === nlrm_enc( '' ) && '' === nlrm_dec( '' ) );
t( 'dec garbage', '' === nlrm_dec( 's1:AAAA' ) );
$iv = random_bytes( 12 ); $tag = ''; $c = openssl_encrypt( $s, 'aes-256-gcm', nlrm_key(), OPENSSL_RAW_DATA, $iv, $tag );
t( 'gcm path decodes', nlrm_dec( 'g2:' . nlrm_keyring()['cur'] . ':' . base64_encode( $iv . $tag . $c ) ) === $s );
$iv = random_bytes( 12 ); $tag = ''; $c = openssl_encrypt( $s, 'aes-256-gcm', nlrm_key_legacy(), OPENSSL_RAW_DATA, $iv, $tag );
t( 'first-build data (g1, salts key) still reads', nlrm_dec( 'g1:' . base64_encode( $iv . $tag . $c ) ) === $s );
$n = random_bytes( 24 );
t( 'first-build data (s1, salts key) still reads', nlrm_dec( 's1:' . base64_encode( $n . sodium_crypto_secretbox( $s, $n, nlrm_key_legacy() ) ) ) === $s );
t( 'key lives in a file, not the database', 'file' === nlrm_keyring()['src'] && is_file( nlrm_keyfile_path() ) && 0 === strpos( file_get_contents( nlrm_keyfile_path() ), '<?php exit; ?>' ) );
t( 'blob round trip', 'bytes' === nlrm_blob_dec( nlrm_blob_enc( 'bytes' ) ) );
t( 'hash stable + case-insensitive', nlrm_hash( 'A@B.com' ) === nlrm_hash( 'a@b.com ' ) );
foreach ( array( array( '050-123-4567', '972501234567' ), array( '+972 50 123 4567', '972501234567' ), array( '0044 7700 900123', '447700900123' ), array( '972501234567', '972501234567' ), array( '', '' ) ) as $p ) { t( 'phone ' . $p[0], nlrm_phone( $p[0] ) === $p[1], nlrm_phone( $p[0] ) ); }
t( 'date ok', '2026-10-01' === nlrm_date( '2026-10-01' ) ); t( 'date bad', null === nlrm_date( '1/10/2026' ) );
$j = nlrm_clean_json( array( 'a' => '<b>x</b>', 'deep' => array( array( array( array( array( array( 'z' ) ) ) ) ) ), 'bad key!' => 1 ) );
t( 'json strips tags', 'x' === $j['a'] ); t( 'json key cleaned', isset( $j['badkey'] ) ); t( 'json depth capped', null === $j['deep'][0][0][0][0] );
foreach ( array( array( 'אין מים חמים בכלל', 'boiler', 'urgent' ), array( 'No hot water at all', 'boiler', 'urgent' ), array( 'טפטוף בברז המטבח', 'plumbing', 'standard' ), array( 'ריח גז במטבח', 'general', 'urgent' ), array( 'the AC is noisy', 'general', 'standard' ), array( 'מזגן לא מקרר', 'ac', 'standard' ),
	array( 'דליפת מים מהתקרה', 'roof', 'urgent' ), array( 'הדלת לא ננעלת', 'locks', 'urgent' ), array( 'Не работает розетка в спальне', 'electric', 'standard' ), array( 'нет горячей воды', 'boiler', 'urgent' ), array( 'رائحة غاز في المطبخ', 'general', 'urgent' ) ) as $c ) {
	$r = nlrm_triage( $c[0] ); t( 'triage ' . $c[0], $r['urgency'] === $c[2] && $r['category'] === $c[1], json_encode( $r, JSON_UNESCAPED_UNICODE ) );
}
echo "unit checks: $ok passed, $bad failed\n";
