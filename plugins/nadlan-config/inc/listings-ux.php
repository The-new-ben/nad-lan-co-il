<?php
/**
 * nadlan-config - Listings engagement & conversion UX (v1.6.0)
 *
 * Best-in-class listing-page mechanics (Redfin/Zillow-grade), low-cost/no-API:
 *   - Similar listings (SQL on city + rooms±1 + price±15% + listing_type)
 *   - Favorites (REST for logged-in users; localStorage fallback handled client-side)
 *   - View counter + Days-on-Market badge (Redfin social-proof signal)
 *   - Mortgage / משכנתא calculator (client-side, ₪)  [nadlan_mortgage]
 *   - Schedule-viewing / WhatsApp contact CTA (reuses the /nadlan/v1/lead endpoint)
 *
 * Roadmap (NOT here - see docs/listings-questions.md §D): AVM + deal-history,
 * neighborhood panel, saved-search email alerts, school/planning overlays.
 */

if ( ! defined( 'ABSPATH' ) ) { exit; }

/* ---- view counter (debounced per IP) + days-on-market ---- */
if ( ! function_exists( 'nadlan_listing_track_view' ) ) {
	function nadlan_listing_track_view() {
		if ( ! is_singular( 'nadlan_property' ) ) { return; }
		$id  = get_queried_object_id();
		$ip  = isset( $_SERVER['REMOTE_ADDR'] ) ? md5( $_SERVER['REMOTE_ADDR'] . $id ) : 'x';
		$key = 'nadlan_v_' . $ip;
		if ( get_transient( $key ) ) { return; }
		set_transient( $key, 1, 6 * HOUR_IN_SECONDS );
		$c = (int) get_post_meta( $id, 'view_count', true );
		update_post_meta( $id, 'view_count', $c + 1 );
	}
}
add_action( 'template_redirect', 'nadlan_listing_track_view' );

if ( ! function_exists( 'nadlan_listing_days_on_market' ) ) {
	function nadlan_listing_days_on_market( $id ) {
		$pub = get_post_time( 'U', true, $id );
		return $pub ? max( 0, (int) floor( ( time() - $pub ) / DAY_IN_SECONDS ) ) : 0;
	}
}

/* ---- favorites REST (logged-in) ---- */
if ( ! function_exists( 'nadlan_fav_register_rest' ) ) {
	function nadlan_fav_register_rest() {
		register_rest_route( 'nadlan/v1', '/favorite', array(
			'methods' => 'POST',
			'permission_callback' => function () { return is_user_logged_in(); },
			'callback' => 'nadlan_fav_handler',
		) );
	}
}
add_action( 'rest_api_init', 'nadlan_fav_register_rest' );

if ( ! function_exists( 'nadlan_fav_handler' ) ) {
	function nadlan_fav_handler( $req ) {
		$p   = $req->get_json_params(); if ( ! is_array( $p ) ) { $p = $req->get_params(); }
		$pid = (int) ( $p['post_id'] ?? 0 );
		$act = sanitize_key( $p['action'] ?? 'add' );
		$uid = get_current_user_id();
		if ( ! $pid || get_post_type( $pid ) !== 'nadlan_property' ) {
			return new WP_REST_Response( array( 'ok' => false ), 400 );
		}
		$favs = (array) get_user_meta( $uid, 'nadlan_favorites', true );
		$favs = array_values( array_unique( array_filter( array_map( 'intval', $favs ) ) ) );
		if ( $act === 'remove' ) {
			$favs = array_values( array_diff( $favs, array( $pid ) ) );
		} else {
			$favs[] = $pid;
			$favs = array_values( array_unique( $favs ) );
		}
		update_user_meta( $uid, 'nadlan_favorites', $favs );
		return new WP_REST_Response( array( 'ok' => true, 'favorites' => $favs ), 200 );
	}
}

/* ---- similar listings ---- */
if ( ! function_exists( 'nadlan_listing_similar' ) ) {
	function nadlan_listing_similar( $id, $limit = 4 ) {
		$city  = (string) get_post_meta( $id, 'city', true );
		$rooms = (float) get_post_meta( $id, 'rooms', true );
		$price = (float) get_post_meta( $id, 'price', true );
		$ltype = (string) get_post_meta( $id, 'listing_type', true );
		$meta  = array( 'relation' => 'AND' );
		if ( $ltype ) { $meta[] = array( 'key' => 'listing_type', 'value' => $ltype ); }
		if ( $rooms ) { $meta[] = array( 'key' => 'rooms', 'value' => array( $rooms - 1, $rooms + 1 ), 'type' => 'NUMERIC', 'compare' => 'BETWEEN' ); }
		if ( $price ) { $meta[] = array( 'key' => 'price', 'value' => array( (int) ( $price * 0.85 ), (int) ( $price * 1.15 ) ), 'type' => 'NUMERIC', 'compare' => 'BETWEEN' ); }
		$q = new WP_Query( array(
			'post_type' => 'nadlan_property', 'posts_per_page' => $limit + 1,
			'post__not_in' => array( $id ), 'no_found_rows' => true,
			'meta_query' => ( function () use ( $meta, $city ) {
				// Audit fix 2026-07-02: the old tax_query was dead code, so "similar
				// listings" ignored location entirely. City is a meta field here.
				if ( $city !== '' ) { $meta[] = array( 'key' => 'city', 'value' => $city ); }
				return count( $meta ) > 1 ? $meta : array();
			} )(),
		) );
		$out = array();
		foreach ( $q->posts as $p ) {
			if ( count( $out ) >= $limit ) { break; }
			$out[] = $p;
		}
		wp_reset_postdata();
		return $out;
	}
}

/* ---- append engagement block to property single ---- */
if ( ! function_exists( 'nadlan_listing_append' ) ) {
	function nadlan_listing_append( $content ) {
		if ( ! ( is_singular( 'nadlan_property' ) && in_the_loop() && is_main_query() ) ) { return $content; }
		$id    = get_the_ID();
		$dom   = nadlan_listing_days_on_market( $id );
		$views = (int) get_post_meta( $id, 'view_count', true );
		$phone = (string) get_post_meta( $id, 'phone', true );
		ob_start(); ?>
<div class="nlx" dir="rtl">
	<div class="nlx-signals">
		<span class="nlx-badge">🗓️ <?php echo (int) $dom; ?> ימים באתר</span>
		<span class="nlx-badge">👁️ <?php echo (int) $views; ?> צפיות</span>
		<button class="nlx-fav" data-id="<?php echo (int) $id; ?>" onclick="nadlanFav(this)">♡ שמירה</button>
	</div>

	<div class="nlx-cta">
		<a class="nlx-btn nlx-wa" target="_blank" rel="noopener"
		   href="https://wa.me/<?php echo esc_attr( preg_replace( '/\D+/', '', (string) get_option( 'nadlan_whatsapp_e164', '972525101555' ) ) ); ?>?text=<?php echo rawurlencode( 'היי, מעוניין/ת בנכס: ' . get_the_title( $id ) . ' ' . get_permalink( $id ) ); ?>">וואטסאפ</a>
		<button class="nlx-btn" onclick="document.getElementById('nlx-visit-<?php echo (int) $id; ?>').classList.toggle('on')">תיאום ביקור</button>
	</div>
	<form id="nlx-visit-<?php echo (int) $id; ?>" class="nlx-visit" onsubmit="return nadlanVisit(this,<?php echo (int) $id; ?>)">
		<input type="text" name="name" placeholder="שם" required>
		<input type="tel" name="phone" placeholder="טלפון" required>
		<input type="date" name="date">
		<input type="text" name="company" class="nlx-hp" tabindex="-1" autocomplete="off" aria-hidden="true">
		<button type="submit">שלחו בקשת ביקור</button>
		<span class="nlx-msg"></span>
	</form>

	<?php /* V7 (owner order 22.8): the 3D tours reach the sale/rent pages too */ ?>
	<a class="nlx-tours" href="<?php echo esc_url( home_url( '/tours/' ) ); ?>">
		<b>🏙️ רוצים להרגיש את השכונה לפני שמתקשרים?</b>
		<span>סיורים תלת־ממדיים חיים — טיסה, הליכה ברחוב וקריינות · כל הסיורים במקום אחד ←</span>
	</a>

	<?php $sim = nadlan_listing_similar( $id ); if ( $sim ) : ?>
	<h3 class="nlx-h">נכסים דומים</h3>
	<div class="nlx-similar">
		<?php foreach ( $sim as $p ) :
			$pp = (float) get_post_meta( $p->ID, 'price', true );
			$rr = get_post_meta( $p->ID, 'rooms', true );
			$sq = get_post_meta( $p->ID, 'size_sqm', true ); ?>
		<a class="nlx-sim" href="<?php echo esc_url( get_permalink( $p ) ); ?>">
			<?php echo has_post_thumbnail( $p ) ? get_the_post_thumbnail( $p, 'medium' ) : ''; ?>
			<span class="nlx-sim-t"><?php echo esc_html( get_the_title( $p ) ); ?></span>
			<span class="nlx-sim-p"><?php echo $pp ? '₪' . number_format( $pp ) : ''; ?></span>
			<span class="nlx-sim-m"><?php echo esc_html( trim( ( $rr ? "$rr חד' · " : '' ) . ( $sq ? "$sq מ\"ר" : '' ), ' ·' ) ); ?></span>
		</a>
		<?php endforeach; ?>
	</div>
	<?php endif; ?>
</div>
		<?php
		return $content . ob_get_clean();
	}
}
add_filter( 'the_content', 'nadlan_listing_append', 22 );

/* ---- mortgage calculator shortcode ---- */
add_shortcode( 'nadlan_mortgage', function () {
	ob_start(); ?>
<div class="nlmort" dir="rtl">
	<h3>מחשבון משכנתא</h3>
	<label>סכום הלוואה (₪) <input type="number" id="nlm-amt" value="1000000"></label>
	<label>ריבית שנתית (%) <input type="number" id="nlm-rate" value="4.5" step="0.1"></label>
	<label>תקופה (שנים) <input type="number" id="nlm-years" value="25"></label>
	<button onclick="nadlanMort()">חשבו</button>
	<p class="nlm-out"></p>
</div>
<script>
function nadlanMort(){
	var P=+document.getElementById('nlm-amt').value, r=(+document.getElementById('nlm-rate').value)/100/12, n=(+document.getElementById('nlm-years').value)*12;
	var m = r>0 ? P*r/(1-Math.pow(1+r,-n)) : P/n;
	document.querySelector('.nlmort .nlm-out').textContent='החזר חודשי משוער: ₪'+Math.round(m).toLocaleString()+' · סה"כ החזר: ₪'+Math.round(m*n).toLocaleString();
}
</script>
	<?php
	return ob_get_clean();
} );

/* ---- scoped assets for property views ---- */
if ( ! function_exists( 'nadlan_listing_assets' ) ) {
	function nadlan_listing_assets() {
		if ( ! is_singular( 'nadlan_property' ) ) { return; }
		?>
<style>
.nlx{margin:24px 0;font-family:var(--font-sans,Heebo,sans-serif)}
.nlx-signals{display:flex;gap:10px;flex-wrap:wrap;margin-bottom:14px}
.nlx-badge,.nlx-fav{background:#FAF7F1;border:1px solid rgba(27,26,23,.12);border-radius:20px;padding:6px 14px;font-size:14px;cursor:default}
.nlx-fav{cursor:pointer}
.nlx-cta{display:flex;gap:10px;margin-bottom:10px}
.nlx-btn{padding:12px 22px;border:0;border-radius:4px;font:inherit;font-weight:500;cursor:pointer;background:#1B1A17;color:#FAF7F1;text-decoration:none;display:inline-block}
.nlx-btn:hover{background:#9C7A3C;color:#1B1A17}
.nlx-wa{background:#25D366;color:#fff}
.nlx-visit{display:none;grid-template-columns:1fr 1fr;gap:8px;max-width:480px;margin:8px 0 18px}
.nlx-visit.on{display:grid}
.nlx-tours{display:block;background:#FBF7EC;border:1px solid #E2DCD0;border-radius:12px;padding:14px 16px;margin:14px 0 18px;text-decoration:none;color:#1B1A17}
.nlx-tours b{display:block;font-weight:700;font-size:14.5px;margin-bottom:3px}
.nlx-tours span{display:block;font-size:13px;color:#6B6353;line-height:1.55}
.nlx-tours:hover{border-color:#B85410;background:#FFFDF8}
.nlx-visit input{padding:10px;border:1px solid rgba(27,26,23,.2);border-radius:4px;font:inherit}
.nlx-visit button{grid-column:1/-1;padding:11px;background:#1B1A17;color:#FAF7F1;border:0;border-radius:4px;cursor:pointer}
.nlx-hp{position:absolute;left:-9999px}
.nlx-h{margin:22px 0 12px}
.nlx-similar{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:12px}
.nlx-sim{display:block;text-decoration:none;color:inherit;border:1px solid rgba(27,26,23,.1);border-radius:6px;overflow:hidden}
.nlx-sim img{width:100%;height:110px;object-fit:cover;display:block}
.nlx-sim span{display:block;padding:2px 10px}
.nlx-sim-t{font-weight:500;padding-top:8px!important}
.nlx-sim-p{color:#9C7A3C;font-weight:600}
.nlx-sim-m{color:#777;font-size:13px;padding-bottom:8px!important}
.nlmort label{display:block;margin:6px 0}
.nlmort input{margin-inline-start:8px;padding:6px;border:1px solid #ccc;border-radius:4px}
.nlm-out{font-weight:600;margin-top:10px}
</style>
<script>
function nadlanFav(b){
	fetch('<?php echo esc_url_raw( rest_url( 'nadlan/v1/favorite' ) ); ?>',{method:'POST',headers:{'Content-Type':'application/json','X-WP-Nonce':'<?php echo esc_js( wp_create_nonce( 'wp_rest' ) ); ?>'},body:JSON.stringify({post_id:+b.dataset.id,action:b.dataset.on?'remove':'add'})})
	.then(function(r){return r.json();}).then(function(j){
		if(j.ok){b.dataset.on=b.dataset.on?'':'1';b.textContent=b.dataset.on?'♥ נשמר':'♡ שמירה';}
		else{ // guest fallback: localStorage
			var f=JSON.parse(localStorage.getItem('nadlan_fav')||'[]');var id=+b.dataset.id;
			if(f.indexOf(id)<0){f.push(id);b.textContent='♥ נשמר';}else{f=f.filter(function(x){return x!=id;});b.textContent='♡ שמירה';}
			localStorage.setItem('nadlan_fav',JSON.stringify(f));
		}
	}).catch(function(){
		var f=JSON.parse(localStorage.getItem('nadlan_fav')||'[]');var id=+b.dataset.id;
		if(f.indexOf(id)<0){f.push(id);b.textContent='♥ נשמר';}else{f=f.filter(function(x){return x!=id;});b.textContent='♡ שמירה';}
		localStorage.setItem('nadlan_fav',JSON.stringify(f));
	});
}
function nadlanVisit(f,id){
	var d={name:f.name.value,phone:f.phone.value,topic:'תיאום ביקור',message:'תאריך מבוקש: '+f.date.value,source:'property:'+id,company:f.company.value,card_id:id};
	var msg=f.querySelector('.nlx-msg');
	fetch('<?php echo esc_url_raw( rest_url( 'nadlan/v1/lead' ) ); ?>',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(d)})
	.then(function(r){return r.json();}).then(function(j){
		if(j.ok){f.reset();msg.textContent='✓ הבקשה נשלחה, ניצור קשר לתיאום.';msg.style.color='#2e7d32';}
		else{msg.textContent='שגיאה, נסו שוב.';msg.style.color='#c00';}
	}).catch(function(){msg.textContent='שגיאת רשת.';msg.style.color='#c00';});
	return false;
}
</script>
		<?php
	}
}
add_action( 'wp_footer', 'nadlan_listing_assets' );
