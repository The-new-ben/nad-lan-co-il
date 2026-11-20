<?php
/* Renders the sample lease with inc/rentals/lease.php under a tiny WordPress shim (no DB). */
define( 'ABSPATH', __DIR__ . '/' );
define( 'NLRM_DIR_ASSETS', __DIR__ . '/../../../plugins/nadlan-config/assets/rentals/' );
$U = array( 'unit' => array( 'id' => 11, 'property_id' => 1, 'label' => $argv[2] === 'en' ? 'Apt 7' : 'דירה 7', 'floor' => 3, 'rooms' => 3.0, 'meta' => array( 'furnished' => true, 'parking' => false, 'storage' => true ) ),
	'property' => array( 'id' => 1, 'address' => $argv[2] === 'en' ? '78 Arlozorov St' : 'ארלוזורוב 78', 'city' => $argv[2] === 'en' ? 'Tel Aviv-Yafo' : 'תל אביב-יפו' ),
	'contact' => array( 'id' => 101, 'name' => $argv[2] === 'en' ? 'The Levi family' : 'משפחת לוי', 'idno' => '' ) );
function nlrm_get( $e, $id, $o ) { global $U; return $U[ $e ] ?? null; }
function get_userdata( $id ) { return (object) array( 'display_name' => 'Dan' ); }
function get_user_meta( $id, $k, $s ) { return 'nlrm_display' === $k ? ( $GLOBALS['argv'][2] === 'en' ? 'Dan Cohen' : 'דני כהן' ) : ''; }
function nlrm_dec( $s ) { return ''; }
require __DIR__ . '/../../../plugins/nadlan-config/inc/rentals/lease.php';
$lease = json_decode( file_get_contents( $argv[1] ), true );
echo json_encode( nlrm_lease_text( 1, $lease, $argv[2] ), JSON_UNESCAPED_UNICODE );
