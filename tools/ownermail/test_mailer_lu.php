<?php
// Local test of inc/mailer.php nadlan_mail_owner_lu() (1.72.627, HAD-687): mail whose every recipient is a site administrator carries
// the site's own List-Unsubscribe (the dashboard, no one-click), so Brevo adds none of its own; any other mail is left alone, and a
// header the caller set is never touched. Run: php tools/ownermail/test_mailer_lu.php
define( 'ABSPATH', __DIR__ );
define( 'DAY_IN_SECONDS', 86400 );
define( 'HOUR_IN_SECONDS', 3600 );
define( 'WPINC', 'wp-includes' );
$GLOBALS['ACT'] = array(); $GLOBALS['O'] = array( 'admin_email' => 'Owner@Example.com' );
function add_action( $h, $cb, $p = 10 ) { $GLOBALS['ACT'][ $h ][] = $cb; }
function remove_action() {}
function add_filter() {}
function register_rest_route() {}
function add_options_page() {}
function get_option( $k, $d = false ) { return $GLOBALS['O'][ $k ] ?? $d; }
function apply_filters( $h, $v ) { return $v; }
function admin_url( $p = '' ) { return 'https://nad-lan.co.il/wp-admin/' . $p; }
function get_users( $a ) { $GLOBALS['USERS_CALLS'] = ( $GLOBALS['USERS_CALLS'] ?? 0 ) + 1; return array( (object) array( 'user_email' => 'staff@example.com' ) ); }
class FakeMailer {
	public $to = array(), $cc = array(), $bcc = array(), $h = array(), $Sender = '', $from = '', $smtp = false;
	function getCustomHeaders() { return $this->h; }
	function addCustomHeader( $n, $v = null ) { $this->h[] = array( $n, $v ); }
	function getToAddresses() { return $this->to; }
	function getCcAddresses() { return $this->cc; }
	function getBccAddresses() { return $this->bcc; }
	function setFrom( $a, $n = '', $auto = true ) { $this->from = $a; }
	function isSMTP() { $this->smtp = true; }
}
require dirname( __DIR__, 2 ) . '/plugins/nadlan-config/inc/mailer.php';
$fails = 0; $n = 0;
function ok( $c, $what ) { global $fails, $n; $n++; if ( ! $c ) { $fails++; echo "FAIL: $what\n"; } }
function lu( $m ) { foreach ( $m->h as $x ) { if ( 'List-Unsubscribe' === $x[0] ) { return $x[1]; } } return null; }
function mk( $to, $cc = array(), $h = array() ) { $m = new FakeMailer(); foreach ( $to as $a ) { $m->to[] = array( $a, '' ); } foreach ( $cc as $a ) { $m->cc[] = array( $a, '' ); } $m->h = $h; return $m; }

// the owner alone (case and spaces ignored) gets the site's header, pointing at the dashboard, and no one-click
$m = mk( array( ' owner@example.COM ' ) ); ok( true === nadlan_mail_owner_lu( $m ), 'owner alone: added' );
ok( '<https://nad-lan.co.il/wp-admin/index.php>' === lu( $m ), 'owner alone: dashboard url' );
foreach ( $m->h as $x ) { ok( 0 !== strcasecmp( $x[0], 'List-Unsubscribe-Post' ), 'no one-click header' ); }
// another administrator, and owner + administrator together
ok( true === nadlan_mail_owner_lu( mk( array( 'staff@example.com' ) ) ), 'administrator: added' );
ok( true === nadlan_mail_owner_lu( mk( array( 'owner@example.com' ), array( 'staff@example.com' ) ) ), 'owner + admin cc: added' );
// anyone else, or a mix, is left alone (Brevo's own header there is the reader's real choice)
$m = mk( array( 'lead@example.org' ) ); ok( false === nadlan_mail_owner_lu( $m ) && null === lu( $m ), 'client: untouched' );
$m = mk( array( 'owner@example.com', 'lead@example.org' ) ); ok( false === nadlan_mail_owner_lu( $m ) && null === lu( $m ), 'owner + client: untouched' );
$m = mk( array( 'owner@example.com' ), array( 'lead@example.org' ) ); ok( false === nadlan_mail_owner_lu( $m ), 'owner + client cc: untouched' );
$m = mk( array() ); ok( false === nadlan_mail_owner_lu( $m ), 'no recipient: untouched' );
// a header the caller set is kept as it is, in any letter case
$m = mk( array( 'owner@example.com' ), array(), array( array( 'list-unsubscribe', '<https://x/u>' ) ) );
ok( false === nadlan_mail_owner_lu( $m ) && 1 === count( $m->h ), 'caller header kept' );
// force (the admin test route) adds it for any recipient, still once
$m = mk( array( 'lead@example.org' ) ); ok( true === nadlan_mail_owner_lu( $m, true ) && null !== lu( $m ), 'force: added' );
ok( false === nadlan_mail_owner_lu( $m, true ) && 1 === count( $m->h ), 'force twice: once' );
// the administrators are read once per request
ok( 1 === ( $GLOBALS['USERS_CALLS'] ?? 0 ), 'get_users once' );
// the real hook: no SMTP configured (host mail) still gets the header, and the From stays aligned
$hook = $GLOBALS['ACT']['phpmailer_init'][0];
$m = mk( array( 'owner@example.com' ) ); $hook( $m );
ok( null !== lu( $m ) && 'wordpress@nad-lan.co.il' === $m->from && false === $m->smtp, 'hook, host mail: header + from' );
$m = mk( array( 'lead@example.org' ) ); $hook( $m ); ok( null === lu( $m ), 'hook, client: untouched' );
echo $fails ? "FAILED $fails of $n\n" : "ALL $n PASSED\n";
exit( $fails ? 1 : 0 );
