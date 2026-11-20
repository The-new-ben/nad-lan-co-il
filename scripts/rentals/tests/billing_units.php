<?php
/* The landlord's subscription (inc/rentals/billing.php) against a stand-in WooCommerce:
   modes off/test/live, a paid order extends the plan once, stacking, grace, expiry,
   renewal orders once per cycle, the free limit only when billing is live.
   php -d extension=pdo_sqlite -d extension=sodium scripts/rentals/tests/billing_units.php */
require __DIR__ . '/../sim/wp_shim.php';

/* ---- a stand-in WooCommerce: products, orders, items ---- */
class FakeProduct {
	public $id; public $meta; public $price; public $status;
	function __construct( $id, $meta, $price, $status ) { $this->id = $id; $this->meta = $meta; $this->price = $price; $this->status = $status; }
	function get_id() { return $this->id; } function get_meta( $k ) { return $this->meta[ $k ] ?? ''; } function get_price() { return $this->price; } function get_status() { return $this->status; }
}
class FakeItem { public $p; public $q; function __construct( $p, $q = 1 ) { $this->p = $p; $this->q = $q; } function get_product() { return $this->p; } function get_quantity() { return $this->q; } }
class FakeOrder {
	public $id; public $user; public $items = array(); public $meta = array(); public $status = 'pending'; public $notes = array();
	function __construct( $id, $user ) { $this->id = $id; $this->user = $user; }
	function get_id() { return $this->id; } function get_customer_id() { return $this->user; } function get_items() { return $this->items; }
	function get_meta( $k ) { return $this->meta[ $k ] ?? ''; } function update_meta_data( $k, $v ) { $this->meta[ $k ] = $v; } function add_order_note( $n ) { $this->notes[] = $n; } function save() {}
	function add_product( $p, $q ) { $this->items[] = new FakeItem( $p, $q ); return count( $this->items ); }
	function set_address( $a, $t ) {} function get_address( $t ) { return array(); } function calculate_totals() {} function update_status( $s, $n = '' ) { $this->status = $s; } function get_status() { return $this->status; }
}
$GLOBALS['P'] = array( 501 => new FakeProduct( 501, array( '_nlrm_plan' => 'pro', '_nlrm_days' => 30 ), 39, 'draft' ), 502 => new FakeProduct( 502, array( '_nlrm_plan' => 'business' ), 199, 'draft' ) );
$GLOBALS['O'] = array();
function wc_get_products( $a ) { return array_values( $GLOBALS['P'] ); }
function wc_get_product( $id ) { return $GLOBALS['P'][ $id ] ?? null; }
function wc_get_order( $id ) { return $GLOBALS['O'][ $id ] ?? null; }
function wc_create_order( $a ) { $id = 9000 + count( $GLOBALS['O'] ); return $GLOBALS['O'][ $id ] = new FakeOrder( $id, $a['customer_id'] ); }
function wc_get_checkout_url() { return 'https://nad-lan.co.il/checkout/'; }
function add_query_arg( $args, $url ) { return $url . '?' . http_build_query( $args ); }

$GLOBALS['SIM_T'] = gmmktime( 9, 0, 0, 10, 3, 2026 );
add_filter( 'nlrm_time', function () { return $GLOBALS['SIM_T']; } );
$tmp = sys_get_temp_dir() . '/nlrm-bill-' . getmypid();
sim_boot( ':memory:', $tmp );
nlrm_install();
$ok = 0; $bad = 0;
function t( $name, $cond, $info = '' ) { global $ok, $bad; if ( $cond ) { $ok++; } else { $bad++; echo "FAIL $name $info\n"; } }
function order_for( $user, $pid, $q = 1 ) { $o = wc_create_order( array( 'customer_id' => $user ) ); $o->add_product( wc_get_product( $pid ), $q ); return $o; }
$U = 7;

/* off: nothing offered, nobody limited (the v1 promise) */
$p = nlrm_plan( $U );
t( 'off: plan free', 'free' === $p['id'] );
t( 'off: no limit enforced', 2000 === $p['limits']['units'], json_encode( $p['limits'] ) );
t( 'off: no offer', null === $p['offer'] );

/* test: administrators see the draft offer; others see nothing */
update_option( 'nlrm_billing', 'test' );
$GLOBALS['sim_admin'] = true;
$p = nlrm_plan( $U );
t( 'test: admin sees the draft offer', isset( $p['offer']['pro'], $p['offer']['business'] ) && 39.0 === $p['offer']['pro']['price'] && $p['offer']['pro']['test'] );
$GLOBALS['sim_admin'] = false;
t( 'test: a landlord sees nothing', null === nlrm_plan( $U )['offer'] );

/* live: draft products are never offered; the free limit applies */
update_option( 'nlrm_billing', 'live' );
$p = nlrm_plan( $U );
t( 'live: drafts are not offered', null === $p['offer'] );
t( 'live: free limit 3', 3 === $p['limits']['units'] );
$GLOBALS['P'][501]->status = 'publish';
nlrm_billing_products( true );
t( 'live: a published product is offered with its buy link', false !== strpos( (string) ( nlrm_plan( $U )['offer']['pro']['buy'] ?? '' ), 'add-to-cart=501' ) );

/* a paid order: pro for 30 days, once */
$o = order_for( $U, 501 );
t( 'order applied', 1 === nlrm_billing_apply_order( $o->get_id() ) );
t( 'order applied only once', 0 === nlrm_billing_apply_order( $o->get_id() ) );
$p = nlrm_plan( $U );
t( 'pro until +30 days', 'pro' === $p['id'] && '2026-11-02' === $p['until'] && 50 === $p['limits']['units'], json_encode( $p ) );
/* paying again before the end stacks from the end, never from today */
$GLOBALS['SIM_T'] += 20 * DAY_IN_SECONDS;
nlrm_billing_apply_order( order_for( $U, 501 )->get_id() );
t( 'stacks from the current end', '2026-12-02' === nlrm_plan( $U )['until'], nlrm_plan( $U )['until'] );
/* a renewal order three days before the end, once per cycle */
$GLOBALS['SIM_T'] = gmmktime( 9, 0, 0, 11, 30, 2026 );
$n1 = nlrm_billing_renewals(); $n2 = nlrm_billing_renewals();
t( 'one renewal order per cycle', 1 === $n1 && 0 === $n2, "$n1 $n2" );
$rid = (int) get_user_meta( $U, 'nlrm_plan_renewal', true );
t( 'the renewal is pending, for the same product', $rid && 'pending' === wc_get_order( $rid )->get_status() && 501 === wc_get_order( $rid )->items[0]->get_product()->get_id() );
/* the end passes unpaid: grace, then free (nothing deleted) */
$GLOBALS['SIM_T'] = gmmktime( 9, 0, 0, 12, 5, 2026 );
t( 'grace after the end', 'grace' === nlrm_plan( $U )['state'] && 'pro' === nlrm_plan( $U )['id'] );
$GLOBALS['SIM_T'] = gmmktime( 9, 0, 0, 12, 12, 2026 );
t( 'free after the grace', 'free' === nlrm_plan( $U )['id'] && 'expired' === nlrm_plan( $U )['state'] );
/* the late renewal is paid: active again from the payment date */
nlrm_billing_apply_order( $rid );
t( 'a late payment reactivates from today', 'pro' === nlrm_plan( $U )['id'] && '2027-01-11' === nlrm_plan( $U )['until'], nlrm_plan( $U )['until'] );

/* the free limit through the REST route (live, free account): the 4th apartment is refused, nothing deleted */
$W = 8;
$GLOBALS['sim_user'] = $W;
$pr = nlrm_save( 'property', array( 'title' => 'x', 'address' => 'a', 'city' => 'c', 'floors' => 2, 'units_per_floor' => 2 ), $W );
for ( $i = 0; $i < 3; $i++ ) { sim_rest( '/rm/save', array( 'entity' => 'unit', 'data' => array( 'property_id' => $pr['id'], 'label' => 'u' . $i ) ) ); }
$r = sim_rest( '/rm/save', array( 'entity' => 'unit', 'data' => array( 'property_id' => $pr['id'], 'label' => 'u4' ) ) );
t( 'live free: 4th apartment refused with 402', is_wp_error( $r ) && 402 === ( $r->data['status'] ?? 0 ) );
update_option( 'nlrm_billing', 'off' );
$r = sim_rest( '/rm/save', array( 'entity' => 'unit', 'data' => array( 'property_id' => $pr['id'], 'label' => 'u4' ) ) );
t( 'billing off: no limit', ! is_wp_error( $r ) );
/* the site grants a plan (a pilot) */
$GLOBALS['sim_admin'] = true;
$g = sim_rest( '/rm/plan-grant', array( 'user_id' => $W, 'plan' => 'business', 'days' => 0 ) );
t( 'grant: business with no end', is_array( $g ) && 'business' === $g['id'] && null === $g['until'] );
$GLOBALS['sim_admin'] = false;
t( 'grant: only administrators', is_wp_error( sim_rest( '/rm/plan-grant', array( 'user_id' => $W, 'plan' => 'business' ) ) ) );
echo "billing checks: $ok passed, $bad failed\n";
exit( $bad ? 1 : 0 );
