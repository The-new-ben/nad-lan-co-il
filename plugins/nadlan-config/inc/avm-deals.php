<?php
/**
 * nadlan-config — Deal history + AVM + neighborhood data (v1.7.0)
 *
 * The Madlan-parity data layer. Three parts:
 *  1) A cached deals table ({prefix}nadlan_deals) — populated by an ETL adapter
 *     (govmap/nadlan endpoints, verified by Cowork mission M10) OR by a direct REST
 *     ingest so we are not blocked on reverse-engineering. NEVER call upstream
 *     per-pageview — always read from the cache.
 *  2) A comparable-sales AVM (hedonic-lite): median ₪/sqm of nearby comps × subject
 *     sqm, with a confidence score derived from comp count + dispersion (a forecast
 *     standard deviation, FSD-style). Degrades to "insufficient_data" when the table
 *     is sparse, so nothing breaks before deals are seeded.
 *  3) Neighborhood stats panel + a "what's my home worth" seller lead funnel.
 *
 * Method grounding (2025-26): AVMs combine comparable-sales + hedonic regression;
 * best practice exposes a confidence/FSD score and an explainable range. ML upgrade
 * (gradient boosting / SHAP explainability) is roadmap — see architecture skill.
 *
 * BLANKS (owner/legal): storing nadlan.gov.il price data needs ToS/legal sign-off
 * (docs/listings-questions.md A.6). The estimate is informational, not an appraisal.
 */

if ( ! defined( 'ABSPATH' ) ) { exit; }

const NADLAN_DEALS_DB_VERSION = '1';

/* ---- deals table ---- */
if ( ! function_exists( 'nadlan_deals_maybe_install' ) ) {
	function nadlan_deals_maybe_install() {
		if ( get_option( 'nadlan_deals_db_version' ) === NADLAN_DEALS_DB_VERSION ) { return; }
		global $wpdb;
		$table   = $wpdb->prefix . 'nadlan_deals';
		$charset = $wpdb->get_charset_collate();
		$sql = "CREATE TABLE $table (
			id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
			deal_key VARCHAR(64) NOT NULL,
			city VARCHAR(120) NULL,
			neighborhood VARCHAR(120) NULL,
			street VARCHAR(160) NULL,
			gush VARCHAR(20) NULL,
			helka VARCHAR(20) NULL,
			rooms DECIMAL(4,1) NULL,
			sqm INT NULL,
			price BIGINT NULL,
			price_per_sqm INT NULL,
			deal_date DATE NULL,
			lat DECIMAL(10,7) NULL,
			lng DECIMAL(10,7) NULL,
			source VARCHAR(40) NULL,
			created_at DATETIME NOT NULL,
			PRIMARY KEY (id),
			UNIQUE KEY deal_key (deal_key),
			KEY city_idx (city),
			KEY geo_idx (lat,lng),
			KEY date_idx (deal_date)
		) $charset;";
		require_once ABSPATH . 'wp-admin/includes/upgrade.php';
		dbDelta( $sql );
		update_option( 'nadlan_deals_db_version', NADLAN_DEALS_DB_VERSION, false );
	}
}
add_action( 'admin_init', 'nadlan_deals_maybe_install' );
register_activation_hook( dirname( __DIR__ ) . '/nadlan-config.php', 'nadlan_deals_maybe_install' );

/* ---- upsert a deal row (idempotent by deal_key) ---- */
if ( ! function_exists( 'nadlan_deals_upsert' ) ) {
	function nadlan_deals_upsert( $d ) {
		global $wpdb;
		$table = $wpdb->prefix . 'nadlan_deals';
		$price = isset( $d['price'] ) ? (int) $d['price'] : null;
		$sqm   = isset( $d['sqm'] ) ? (int) $d['sqm'] : null;
		$ppsqm = ( $price && $sqm ) ? (int) round( $price / $sqm ) : ( isset( $d['price_per_sqm'] ) ? (int) $d['price_per_sqm'] : null );
		$key   = isset( $d['deal_key'] ) ? (string) $d['deal_key']
			: md5( implode( '|', array( $d['gush'] ?? '', $d['helka'] ?? '', $d['deal_date'] ?? '', $price, $sqm, $d['street'] ?? '' ) ) );
		$row = array(
			'deal_key' => $key,
			'city' => $d['city'] ?? null, 'neighborhood' => $d['neighborhood'] ?? null,
			'street' => $d['street'] ?? null, 'gush' => $d['gush'] ?? null, 'helka' => $d['helka'] ?? null,
			'rooms' => isset( $d['rooms'] ) ? (float) $d['rooms'] : null, 'sqm' => $sqm,
			'price' => $price, 'price_per_sqm' => $ppsqm, 'deal_date' => $d['deal_date'] ?? null,
			'lat' => isset( $d['lat'] ) ? (float) $d['lat'] : null, 'lng' => isset( $d['lng'] ) ? (float) $d['lng'] : null,
			'source' => $d['source'] ?? 'ingest', 'created_at' => current_time( 'mysql' ),
		);
		// upsert
		$exists = $wpdb->get_var( $wpdb->prepare( "SELECT id FROM $table WHERE deal_key=%s", $key ) );
		if ( $exists ) { $wpdb->update( $table, $row, array( 'id' => $exists ) ); return (int) $exists; }
		$wpdb->insert( $table, $row );
		return (int) $wpdb->insert_id;
	}
}

/* ---- ETL adapter: pluggable remote fetch (Cowork's verified endpoint slots here) ----
 * Default returns []. Wire the real govmap/nadlan call via the filter once verified
 * (M10). Decoupled so the AVM works off the cache regardless of endpoint status.
 */
if ( ! function_exists( 'nadlan_deals_fetch_remote' ) ) {
	function nadlan_deals_fetch_remote( $lat, $lng, $radius_m = 500, $months = 24 ) {
		return apply_filters( 'nadlan_deals_remote', array(), $lat, $lng, $radius_m, $months );
	}
}

/* ---- REST ingest (admin) — Cowork can POST verified deals straight into the cache ----
 * POST /nadlan/v1/deals-ingest { deals:[ {gush,helka,city,rooms,sqm,price,deal_date,lat,lng,source}, ... ] }
 */
add_action( 'rest_api_init', function () {
	register_rest_route( 'nadlan/v1', '/deals-ingest', array(
		'methods' => 'POST',
		'permission_callback' => function () { return current_user_can( 'edit_posts' ); },
		'callback' => function ( $req ) {
			$p = $req->get_json_params(); if ( ! is_array( $p ) ) { $p = $req->get_params(); }
			$deals = $p['deals'] ?? array();
			$n = 0;
			foreach ( (array) $deals as $d ) { if ( is_array( $d ) ) { nadlan_deals_upsert( $d ); $n++; } }
			return new WP_REST_Response( array( 'ok' => true, 'ingested' => $n ), 200 );
		},
	) );
} );

/* ---- AVM: comparable-sales estimate with confidence ---- */
if ( ! function_exists( 'nadlan_avm_estimate' ) ) {
	function nadlan_avm_estimate( $args ) {
		global $wpdb;
		$table = $wpdb->prefix . 'nadlan_deals';
		$city  = $args['city'] ?? '';
		$sqm   = (int) ( $args['sqm'] ?? 0 );
		$rooms = (float) ( $args['rooms'] ?? 0 );
		if ( $sqm <= 0 || $city === '' ) {
			return array( 'ok' => false, 'reason' => 'need_city_and_sqm' );
		}
		// Comparable window: same city, sqm ±25%, rooms ±1, last 36 months, with ₪/sqm present.
		$min_sqm = (int) floor( $sqm * 0.75 ); $max_sqm = (int) ceil( $sqm * 1.25 );
		$where = "city=%s AND price_per_sqm>0 AND sqm BETWEEN %d AND %d AND deal_date >= DATE_SUB(CURDATE(), INTERVAL 36 MONTH)";
		$params = array( $city, $min_sqm, $max_sqm );
		if ( $rooms > 0 ) { $where .= " AND (rooms IS NULL OR rooms BETWEEN %f AND %f)"; $params[] = $rooms - 1; $params[] = $rooms + 1; }
		$ppsqms = $wpdb->get_col( $wpdb->prepare( "SELECT price_per_sqm FROM $table WHERE $where ORDER BY deal_date DESC LIMIT 200", $params ) );
		$ppsqms = array_map( 'floatval', array_filter( (array) $ppsqms ) );
		$n = count( $ppsqms );
		if ( $n < 5 ) {
			return array( 'ok' => false, 'reason' => 'insufficient_data', 'comp_count' => $n );
		}
		sort( $ppsqms );
		// Trim 10% tails for robustness
		$trim = (int) floor( $n * 0.1 );
		$core = array_slice( $ppsqms, $trim, max( 1, $n - 2 * $trim ) );
		$median = $core[ (int) floor( count( $core ) / 2 ) ];
		$mean   = array_sum( $core ) / count( $core );
		// Dispersion → confidence (coefficient of variation → FSD-like band)
		$var = 0.0; foreach ( $core as $v ) { $var += pow( $v - $mean, 2 ); }
		$sd  = sqrt( $var / count( $core ) );
		$cv  = $mean > 0 ? $sd / $mean : 1.0;            // lower = tighter market
		$confidence = max( 0.0, min( 1.0, 1 - $cv ) ) * min( 1.0, $n / 40 ); // also scales with sample size
		$est   = (int) round( $median * $sqm / 1000 ) * 1000;
		$band  = max( 0.05, min( 0.25, $cv ) );          // ± band 5%–25%
		return array(
			'ok' => true,
			'estimate'      => $est,
			'low'           => (int) round( $est * ( 1 - $band ) / 1000 ) * 1000,
			'high'          => (int) round( $est * ( 1 + $band ) / 1000 ) * 1000,
			'price_per_sqm' => (int) round( $median ),
			'comp_count'    => $n,
			'confidence'    => round( $confidence, 2 ),
		);
	}
}

add_action( 'rest_api_init', function () {
	register_rest_route( 'nadlan/v1', '/avm', array(
		'methods' => 'GET', 'permission_callback' => '__return_true',
		'callback' => function ( $req ) {
			return new WP_REST_Response( nadlan_avm_estimate( array(
				'city' => sanitize_text_field( (string) $req->get_param( 'city' ) ),
				'sqm'  => (int) $req->get_param( 'sqm' ),
				'rooms'=> (float) $req->get_param( 'rooms' ),
			) ), 200 );
		},
	) );
} );

/* ---- neighborhood / city stats ---- */
if ( ! function_exists( 'nadlan_neighborhood_stats' ) ) {
	function nadlan_neighborhood_stats( $city, $neighborhood = '' ) {
		global $wpdb;
		$table = $wpdb->prefix . 'nadlan_deals';
		$where = 'city=%s AND price_per_sqm>0'; $params = array( $city );
		if ( $neighborhood !== '' ) { $where .= ' AND neighborhood=%s'; $params[] = $neighborhood; }
		$row = $wpdb->get_row( $wpdb->prepare(
			"SELECT COUNT(*) n, AVG(price_per_sqm) avg_ppsqm, AVG(price) avg_price
			 FROM $table WHERE $where AND deal_date >= DATE_SUB(CURDATE(), INTERVAL 12 MONTH)", $params
		), ARRAY_A );
		return array(
			'deals_12m'    => (int) ( $row['n'] ?? 0 ),
			'avg_ppsqm'    => (int) round( (float) ( $row['avg_ppsqm'] ?? 0 ) ),
			'avg_price'    => (int) round( (float) ( $row['avg_price'] ?? 0 ) ),
		);
	}
}

/* ---- render: AVM + neighborhood on property single ---- */
add_filter( 'the_content', function ( $content ) {
	if ( ! ( is_singular( 'nadlan_property' ) && in_the_loop() && is_main_query() ) ) { return $content; }
	$id = get_the_ID();
	$est = nadlan_avm_estimate( array(
		'city' => get_post_meta( $id, 'city', true ),
		'sqm'  => (int) get_post_meta( $id, 'size_sqm', true ),
		'rooms'=> (float) get_post_meta( $id, 'rooms', true ),
	) );
	$stats = nadlan_neighborhood_stats( (string) get_post_meta( $id, 'city', true ) );
	if ( ! $est['ok'] && ( $stats['deals_12m'] === 0 ) ) { return $content; } // nothing to show yet
	ob_start(); ?>
<div class="nlavm" dir="rtl">
	<?php if ( $est['ok'] ) : ?>
	<h3>הערכת שווי (אומדן)</h3>
	<p class="nlavm-est">₪<?php echo number_format( $est['estimate'] ); ?>
		<span class="nlavm-band">טווח: ₪<?php echo number_format( $est['low'] ); ?>–₪<?php echo number_format( $est['high'] ); ?></span></p>
	<p class="nlavm-meta">מבוסס על <?php echo (int) $est['comp_count']; ?> עסקאות דומות · ₪<?php echo number_format( $est['price_per_sqm'] ); ?> למ"ר · רמת ביטחון <?php echo (int) round( $est['confidence'] * 100 ); ?>%</p>
	<p class="nlavm-disc">אומדן אוטומטי מבוסס נתוני עסקאות, אינו תחליף לשמאות מקרקעין.</p>
	<?php endif; ?>
	<?php if ( $stats['deals_12m'] > 0 ) : ?>
	<div class="nlavm-hood">
		<strong>שכונה/עיר — 12 חודשים אחרונים:</strong>
		<?php echo (int) $stats['deals_12m']; ?> עסקאות · ממוצע ₪<?php echo number_format( $stats['avg_ppsqm'] ); ?> למ"ר
	</div>
	<?php endif; ?>
</div>
	<?php
	return $content . ob_get_clean();
}, 21 );

/* ---- "what's my home worth" seller lead funnel shortcode ---- */
add_shortcode( 'nadlan_home_value', function () {
	ob_start(); ?>
<div class="nlhv" dir="rtl">
	<h3>כמה שווה הדירה שלכם?</h3>
	<form onsubmit="return nadlanHomeValue(this)">
		<input type="text" name="city" placeholder="עיר" required>
		<input type="number" name="sqm" placeholder="מ&quot;ר" required>
		<input type="number" name="rooms" placeholder="חדרים" step="0.5">
		<input type="text" name="name" placeholder="שם">
		<input type="tel" name="phone" placeholder="טלפון (לקבלת הערכה מורחבת)">
		<input type="text" name="company" style="position:absolute;left:-9999px" tabindex="-1" aria-hidden="true">
		<button type="submit">קבלו אומדן</button>
	</form>
	<p class="nlhv-out"></p>
</div>
<script>
function nadlanHomeValue(f){
	var out=f.parentNode.querySelector('.nlhv-out');
	var qs='city='+encodeURIComponent(f.city.value)+'&sqm='+(+f.sqm.value)+'&rooms='+(+f.rooms.value);
	fetch('<?php echo esc_url_raw( rest_url( 'nadlan/v1/avm' ) ); ?>?'+qs).then(function(r){return r.json();}).then(function(j){
		if(j.ok){out.innerHTML='אומדן: <strong>₪'+j.estimate.toLocaleString()+'</strong> (טווח ₪'+j.low.toLocaleString()+'–₪'+j.high.toLocaleString()+', '+j.comp_count+' עסקאות). אומדן אוטומטי, אינו שמאות.';}
		else{out.textContent='אין מספיק נתונים לאזור הזה עדיין. השאירו טלפון ונחזור עם הערכה.';}
		// capture as lead if phone provided
		if(f.phone.value){fetch('<?php echo esc_url_raw( rest_url( 'nadlan/v1/lead' ) ); ?>',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({name:f.name.value,phone:f.phone.value,topic:'הערכת שווי',message:f.city.value+' '+f.sqm.value+'מ"ר '+f.rooms.value+'חד',source:'home-value-tool',company:f.company.value})});}
	}).catch(function(){out.textContent='שגיאה, נסו שוב.';});
	return false;
}
</script>
	<?php
	return ob_get_clean();
} );

/* scoped styles for AVM block */
add_action( 'wp_footer', function () {
	if ( ! is_singular( 'nadlan_property' ) && ! is_page() ) { return; }
	echo '<style>
.nlavm{margin:22px 0;padding:18px;border:1px solid rgba(27,26,23,.12);border-radius:8px;background:#FAF7F1;font-family:var(--font-sans,Heebo,sans-serif)}
.nlavm-est{font-size:26px;font-weight:700;color:#1B1A17;margin:4px 0}
.nlavm-band{font-size:14px;font-weight:400;color:#777;display:block}
.nlavm-meta{font-size:13px;color:#555}
.nlavm-disc{font-size:12px;color:#999}
.nlavm-hood{margin-top:10px;font-size:14px;border-top:1px solid rgba(27,26,23,.1);padding-top:10px}
.nlhv input{display:block;width:100%;max-width:360px;margin:6px 0;padding:10px;border:1px solid #ccc;border-radius:4px}
.nlhv button{padding:11px 22px;background:#1B1A17;color:#FAF7F1;border:0;border-radius:4px;cursor:pointer}
.nlhv-out{margin-top:10px;font-size:15px}
</style>';
} );
