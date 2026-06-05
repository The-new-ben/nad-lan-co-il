<?php
/**
 * nadlan-config — Operations dashboard (v1.13.0)
 *
 * One admin page that surfaces ALL the moving parts at a glance:
 * leads (with drip-state breakdown), claims (pending/approved), auctions (live/
 * extended/sold), imports (cursor + counts), AVM cache size, deals count,
 * directory health, plugin version. Designed so the owner can manage the
 * whole system without hunting through 7 menus.
 *
 * NEW capability flag: 'manage_options' required. No data is exposed publicly.
 */

if ( ! defined( 'ABSPATH' ) ) { exit; }

add_action( 'admin_menu', function () {
	add_menu_page( 'NadLan Ops', 'NadLan Ops', 'manage_options', 'nadlan-ops',
		'nadlan_ops_render', 'dashicons-chart-bar', 24 );
} );

if ( ! function_exists( 'nadlan_ops_count' ) ) {
	function nadlan_ops_count( $post_type, $meta_key = '', $meta_value = '' ) {
		$args = array( 'post_type' => $post_type, 'posts_per_page' => 1, 'fields' => 'ids', 'post_status' => 'any' );
		if ( $meta_key !== '' ) { $args['meta_query'] = array( array( 'key' => $meta_key, 'value' => $meta_value ) ); }
		$q = new WP_Query( $args );
		return (int) $q->found_posts;
	}
}

if ( ! function_exists( 'nadlan_ops_render' ) ) {
	function nadlan_ops_render() {
		if ( ! current_user_can( 'manage_options' ) ) { wp_die( 'forbidden' ); }
		global $wpdb;
		$leads_total = nadlan_ops_count( 'nadlan_lead' );
		$drip = array(
			'active' => nadlan_ops_count( 'nadlan_lead', 'drip_state', 'active' ),
			'mid'    => nadlan_ops_count( 'nadlan_lead', 'drip_state', 'mid' ),
			'long'   => nadlan_ops_count( 'nadlan_lead', 'drip_state', 'long' ),
			'optout' => nadlan_ops_count( 'nadlan_lead', 'drip_state', 'optout' ),
		);
		$claims = array(
			'pending'  => nadlan_ops_count( 'nadlan_claim', 'claim_state', 'pending' ),
			'approved' => nadlan_ops_count( 'nadlan_claim', 'claim_state', 'approved' ),
		);
		$cards = array(
			'professionals' => nadlan_ops_count( 'nadlan_professional' ),
			'projects'      => nadlan_ops_count( 'nadlan_project' ),
			'properties'    => nadlan_ops_count( 'nadlan_property' ),
			'auctions'      => nadlan_ops_count( 'nadlan_auction' ),
		);
		$claimed = array(
			'professionals' => nadlan_ops_count( 'nadlan_professional', 'claim_status', 'verified' ),
			'projects'      => nadlan_ops_count( 'nadlan_project', 'claim_status', 'verified' ),
			'properties'    => nadlan_ops_count( 'nadlan_property', 'claim_status', 'verified' ),
		);
		$enriched = array(
			'professionals' => nadlan_ops_count( 'nadlan_professional', 'data_quality', 'enriched' ),
			'projects'      => nadlan_ops_count( 'nadlan_project', 'data_quality', 'enriched' ),
		);
		$auctions = array(
			'live'     => nadlan_ops_count( 'nadlan_auction', 'status', 'live' ),
			'extended' => nadlan_ops_count( 'nadlan_auction', 'status', 'extended' ),
			'sold'     => nadlan_ops_count( 'nadlan_auction', 'status', 'sold' ),
			'reserve'  => nadlan_ops_count( 'nadlan_auction', 'status', 'reserve_not_met' ),
		);
		$import_kab   = (int) get_option( 'nadlan_import_offset_contractors', 0 );
		$import_urban = (int) get_option( 'nadlan_import_offset_urban', 0 );
		$deals_count  = (int) $wpdb->get_var( "SELECT COUNT(*) FROM {$wpdb->prefix}nadlan_deals" );
		$bids_count   = (int) $wpdb->get_var( "SELECT COUNT(*) FROM {$wpdb->prefix}nadlan_bids" );
		$ss_total     = nadlan_ops_count( 'nadlan_saved_search' );
		$esign_total  = nadlan_ops_count( 'nadlan_esign' );
		?>
<style>
.nlops{max-width:1100px}
.nlops h1{font-size:24px}
.nlops-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:14px;margin:20px 0}
.nlops-card{background:#fff;border:1px solid #c3c4c7;border-radius:6px;padding:16px}
.nlops-card h2{font-size:14px;margin:0 0 10px;color:#1d2327}
.nlops-row{display:flex;justify-content:space-between;padding:5px 0;border-bottom:1px dashed #ddd;font-size:13px}
.nlops-row:last-child{border:0}
.nlops-row strong{color:#2271b1}
.nlops-links a{display:inline-block;margin-inline-end:10px;font-size:12px}
.nlops-warn{color:#b32d2e}
</style>
<div class="wrap nlops">
	<h1>NadLan Ops</h1>
	<p class="description">Snapshot of leads, claims, cards, imports, auctions and data layer. Live values from the DB.</p>
	<div class="nlops-grid">

		<div class="nlops-card">
			<h2>Leads (drip)</h2>
			<div class="nlops-row"><span>Total</span><strong><?php echo (int) $leads_total; ?></strong></div>
			<div class="nlops-row"><span>active (0-14d)</span><strong><?php echo (int) $drip['active']; ?></strong></div>
			<div class="nlops-row"><span>mid (15d-6mo)</span><strong><?php echo (int) $drip['mid']; ?></strong></div>
			<div class="nlops-row"><span>long (6-18mo)</span><strong><?php echo (int) $drip['long']; ?></strong></div>
			<div class="nlops-row"><span>opted-out</span><strong><?php echo (int) $drip['optout']; ?></strong></div>
			<p class="nlops-links"><a href="<?php echo esc_url( admin_url( 'edit.php?post_type=nadlan_lead' ) ); ?>">Manage leads →</a></p>
		</div>

		<div class="nlops-card">
			<h2>Claims (free-card → owner)</h2>
			<div class="nlops-row"><span>pending review</span><strong class="<?php echo $claims['pending'] > 0 ? 'nlops-warn' : ''; ?>"><?php echo (int) $claims['pending']; ?></strong></div>
			<div class="nlops-row"><span>approved</span><strong><?php echo (int) $claims['approved']; ?></strong></div>
			<p class="nlops-links"><a href="<?php echo esc_url( admin_url( 'edit.php?post_type=nadlan_claim' ) ); ?>">Review claims →</a></p>
		</div>

		<div class="nlops-card">
			<h2>Directory cards</h2>
			<div class="nlops-row"><span>contractors</span><strong><?php echo (int) $cards['professionals']; ?></strong></div>
			<div class="nlops-row"><span>… verified owners</span><strong><?php echo (int) $claimed['professionals']; ?></strong></div>
			<div class="nlops-row"><span>… enriched content</span><strong><?php echo (int) $enriched['professionals']; ?></strong></div>
			<div class="nlops-row"><span>projects</span><strong><?php echo (int) $cards['projects']; ?></strong></div>
			<div class="nlops-row"><span>… verified / enriched</span><strong><?php echo (int) $claimed['projects']; ?> / <?php echo (int) $enriched['projects']; ?></strong></div>
			<div class="nlops-row"><span>properties (listings)</span><strong><?php echo (int) $cards['properties']; ?></strong></div>
		</div>

		<div class="nlops-card">
			<h2>Imports (data.gov.il)</h2>
			<div class="nlops-row"><span>contractors offset</span><strong><?php echo (int) $import_kab; ?></strong></div>
			<div class="nlops-row"><span>urban-renewal offset</span><strong><?php echo (int) $import_urban; ?></strong></div>
			<p class="nlops-links">Use Dashboard → NadLan Directory Import widget, or <code>wp nadlan import contractors|urban</code>.</p>
		</div>

		<div class="nlops-card">
			<h2>Auctions</h2>
			<div class="nlops-row"><span>live</span><strong><?php echo (int) $auctions['live']; ?></strong></div>
			<div class="nlops-row"><span>extended (soft-close)</span><strong><?php echo (int) $auctions['extended']; ?></strong></div>
			<div class="nlops-row"><span>sold</span><strong><?php echo (int) $auctions['sold']; ?></strong></div>
			<div class="nlops-row"><span>reserve not met</span><strong><?php echo (int) $auctions['reserve']; ?></strong></div>
			<div class="nlops-row"><span>total bids placed</span><strong><?php echo (int) $bids_count; ?></strong></div>
			<p class="nlops-links"><a href="<?php echo esc_url( admin_url( 'edit.php?post_type=nadlan_auction' ) ); ?>">Manage auctions →</a></p>
		</div>

		<div class="nlops-card">
			<h2>Data layer</h2>
			<div class="nlops-row"><span>deals cached (AVM)</span><strong><?php echo (int) $deals_count; ?></strong></div>
			<div class="nlops-row"><span>saved searches</span><strong><?php echo (int) $ss_total; ?></strong></div>
			<div class="nlops-row"><span>e-sign requests</span><strong><?php echo (int) $esign_total; ?></strong></div>
			<p class="nlops-links">
				<a href="<?php echo esc_url( rest_url( 'nadlan/v1/healthcheck' ) ); ?>" target="_blank">healthcheck JSON →</a>
			</p>
		</div>

	</div>
	<?php do_action( 'nadlan_ops_after_grid' ); ?>
</div>
		<?php
	}
}
