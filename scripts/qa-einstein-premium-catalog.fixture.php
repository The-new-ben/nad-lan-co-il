<?php
declare(strict_types=1);

define( 'ABSPATH', __DIR__ );
define( 'OBJECT', 'OBJECT' );

function apply_filters( $tag, $value ) { return $value; }
function add_shortcode( $tag, $callback ) { return true; }
function add_action( $tag, $callback, $priority = 10, $accepted_args = 1 ) { return true; }

$GLOBALS['nl_test_meta'] = array();
function get_post_meta( $post_id, $key, $single = false ) {
	return $GLOBALS['nl_test_meta'][ (int) $post_id ][ (string) $key ] ?? '';
}

require dirname( __DIR__ ) . '/plugins/nadlan-config/inc/premium-catalog.php';

function nl_assert( $condition, $message ) {
	if ( ! $condition ) {
		fwrite( STDERR, "FAIL: {$message}\n" );
		exit( 1 );
	}
}

$matches = array_values( array_filter( nadlan_premium_catalog_data(), static function ( $row ) {
	return isset( $row['slug'] ) && 'einstein-tower' === $row['slug'];
} ) );

nl_assert( 1 === count( $matches ), 'Einstein must have exactly one premium-catalog record.' );
$row = $matches[0];
nl_assert( 28 === $row['floors'] && 215 === $row['units'], 'Canonical building/unit facts must match the project record.' );
nl_assert( array() === $row['rooms'], 'No room mix may be inferred before verified inventory.' );
nl_assert( false === $row['sea'] && false === $row['park'] && false === $row['marina'], 'Location filters must not be inferred.' );
nl_assert( 'private_stage' === $row['catalog_state'], 'New flagship record must begin in private-stage state.' );

$post = (object) array( 'ID' => 4867 );
nl_assert( false === nadlan_pc_row_public_ready( $row, $post ), 'Private-stage row must stay out of the public catalog before promotion.' );
$GLOBALS['nl_test_meta'][4867]['_nl_flagship_v3_ready'] = '1';
nl_assert( true === nadlan_pc_row_public_ready( $row, $post ), 'Exact reviewed promotion meta must unlock the catalog row.' );

$legacy = array( 'slug' => 'rainbow-tel-aviv' );
nl_assert( true === nadlan_pc_row_public_ready( $legacy, $post ), 'Existing catalog rows must remain compatible.' );

echo "PASS Einstein premium catalog: one canonical staged row, no inferred unit/location filters, exact reviewed promotion gate, legacy rows unchanged.\n";
