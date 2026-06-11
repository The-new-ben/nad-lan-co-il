<?php
/**
 * nadlan-config - interactive apartment picker (Tier 1: SVG overlay on the
 * project render). Click a unit, see details, send a lead into the existing
 * funnel. Ships dark behind nadlan_feature_project_3d.
 * Spec: docs/2026-06-11-listing-levelup-and-3d-spec-cited.md
 */

if ( ! defined( 'ABSPATH' ) ) { exit; }

if ( ! function_exists( 'nadlan_p3d_enabled' ) ) {
	function nadlan_p3d_enabled() {
		return (bool) apply_filters( 'nadlan_p3d_enabled', get_option( 'nadlan_feature_project_3d', '0' ) === '1' );
	}
}

if ( ! function_exists( 'nadlan_p3d_units' ) ) {
	function nadlan_p3d_units( $post_id ) {
		$raw = (string) get_post_meta( (int) $post_id, 'project_3d_units', true );
		$units = json_decode( $raw, true );
		if ( ! is_array( $units ) || ! $units ) { return array(); }
		$out = array();
		foreach ( $units as $u ) {
			if ( ! is_array( $u ) || empty( $u['id'] ) || empty( $u['points'] ) ) { continue; }
			$out[] = array(
				'id'      => sanitize_key( $u['id'] ),
				'points'  => preg_replace( '/[^0-9,. \-]/', '', (string) $u['points'] ),
				'floor'   => (int) ( $u['floor'] ?? 0 ),
				'rooms'   => (float) ( $u['rooms'] ?? 0 ),
				'sqm'     => (float) ( $u['sqm'] ?? 0 ),
				'balcony' => (float) ( $u['balcony'] ?? 0 ),
				'dir'     => sanitize_text_field( (string) ( $u['dir'] ?? '' ) ),
				'price'   => (float) ( $u['price'] ?? 0 ),
				'status'  => in_array( $u['status'] ?? '', array( 'available', 'reserved', 'sold' ), true ) ? $u['status'] : 'available',
				'plan'    => esc_url_raw( (string) ( $u['plan'] ?? '' ) ),
			);
		}
		return $out;
	}
}

if ( ! function_exists( 'nadlan_p3d_demo_units' ) ) {
	function nadlan_p3d_demo_units() {
		// 6-unit demo grid so the engine renders before real polygons arrive.
		$out = array();
		$statuses = array( 'available', 'available', 'reserved', 'available', 'sold', 'available' );
		for ( $i = 0; $i < 6; $i++ ) {
			$col = $i % 2; $row = (int) floor( $i / 2 );
			$x = 120 + $col * 390; $y = 60 + $row * 200;
			$out[] = array(
				'id' => 'demo' . ( $i + 1 ), 'points' => sprintf( '%d,%d %d,%d %d,%d %d,%d', $x, $y, $x + 350, $y, $x + 350, $y + 160, $x, $y + 160 ),
				'floor' => 6 - $row * 2, 'rooms' => 4 + $col, 'sqm' => 105 + $i * 7, 'balcony' => 12,
				'dir' => $col ? 'דרום-מערב' : 'צפון-מזרח', 'price' => 3200000 + $i * 350000,
				'status' => $statuses[ $i ], 'plan' => '',
			);
		}
		return $out;
	}
}

if ( ! function_exists( 'nadlan_p3d_render' ) ) {
	function nadlan_p3d_render( $post_id ) {
		if ( ! nadlan_p3d_enabled() ) { return ''; }
		$post_id = (int) $post_id;
		$image = esc_url( (string) get_post_meta( $post_id, 'project_3d_image', true ) );
		$units = nadlan_p3d_units( $post_id );
		$demo = false;
		if ( ! $units ) { $units = nadlan_p3d_demo_units(); $demo = true; }
		$vb = sanitize_text_field( (string) get_post_meta( $post_id, 'project_3d_viewbox', true ) );
		if ( $vb === '' ) { $vb = '0 0 1000 540'; }
		$labels = array( 'available' => 'זמינה', 'reserved' => 'שמורה', 'sold' => 'נמכרה' );
		$json = wp_json_encode( $units, JSON_UNESCAPED_UNICODE );
		ob_start(); ?>
<div class="nlp3d" dir="rtl" data-project="<?php echo esc_attr( $post_id ); ?>">
	<div class="nlp3d-head"><h3>בחרו דירה בפרויקט</h3>
		<div class="nlp3d-legend"><span class="nlp3d-lg av">זמינה</span><span class="nlp3d-lg rs">שמורה</span><span class="nlp3d-lg sd">נמכרה</span></div>
		<?php if ( $demo ) : ?><p class="nlp3d-demo-note">תצוגת הדגמה. תוכניות הדירות המלאות יעלו בקרוב.</p><?php endif; ?>
	</div>
	<div class="nlp3d-stage">
		<?php if ( $image ) : ?><img class="nlp3d-img" src="<?php echo $image; ?>" alt="הדמיית הפרויקט" loading="lazy"><?php endif; ?>
		<svg class="nlp3d-svg" viewBox="<?php echo esc_attr( $vb ); ?>" preserveAspectRatio="xMidYMid meet" role="group" aria-label="מפת דירות אינטראקטיבית">
			<?php foreach ( $units as $u ) : ?>
			<polygon class="nlp3d-unit st-<?php echo esc_attr( $u['status'] ); ?>" points="<?php echo esc_attr( $u['points'] ); ?>" data-unit="<?php echo esc_attr( $u['id'] ); ?>" tabindex="0" role="button" aria-label="דירה, קומה <?php echo esc_attr( $u['floor'] ); ?>, <?php echo esc_attr( $u['rooms'] ); ?> חדרים, <?php echo esc_attr( $labels[ $u['status'] ] ); ?>"></polygon>
			<?php endforeach; ?>
		</svg>
	</div>
	<aside class="nlp3d-panel" hidden>
		<button class="nlp3d-close" aria-label="סגור">×</button>
		<h4 class="nlp3d-t"></h4>
		<dl class="nlp3d-facts"></dl>
		<a class="nlp3d-plan" href="#" target="_blank" rel="noopener" hidden>תוכנית הדירה</a>
		<form class="nlp3d-lead">
			<p class="nlp3d-cta-line">מתעניינים בדירה הזו? נחבר אתכם ישירות ליזם.</p>
			<input type="text" name="name" placeholder="שם" required>
			<input type="tel" name="phone" placeholder="טלפון" required>
			<input type="email" name="email" placeholder="אימייל">
			<button type="submit" class="nlp3d-send">דברו איתי על הדירה</button>
			<input type="text" name="company" class="nlp3d-hp" tabindex="-1" autocomplete="off" aria-hidden="true">
			<p class="nlp3d-ok" hidden>קיבלנו את הפנייה. נציג יחזור אליכם בתוך 24 שעות.</p>
		</form>
	</aside>
	<script type="application/json" class="nlp3d-data"><?php echo $json; ?></script>
</div>
		<?php
		return ob_get_clean();
	}
}

add_shortcode( 'nadlan_project_3d', function ( $atts ) {
	$atts = shortcode_atts( array( 'id' => get_the_ID() ), $atts );
	return nadlan_p3d_render( (int) $atts['id'] );
} );

add_action( 'wp_enqueue_scripts', function () {
	if ( ! nadlan_p3d_enabled() ) { return; }
	wp_register_style( 'nadlan-p3d', '', array(), '1.57.0' );
	wp_enqueue_style( 'nadlan-p3d' );
	wp_add_inline_style( 'nadlan-p3d', '.nlp3d{margin:32px 0;border:1px solid #e3d9c4;border-radius:14px;padding:18px;background:#fffdf8}.nlp3d-head{display:flex;flex-wrap:wrap;align-items:center;gap:12px;justify-content:space-between}.nlp3d-legend{display:flex;gap:10px;font-size:13px}.nlp3d-lg{padding:3px 10px;border-radius:20px}.nlp3d-lg.av{background:#e8f6ec;color:#176b35}.nlp3d-lg.rs{background:#fff3df;color:#92600a}.nlp3d-lg.sd{background:#f0f0f0;color:#777}.nlp3d-demo-note{flex-basis:100%;font-size:12px;color:#8a7a55;margin:0}.nlp3d-stage{position:relative;margin-top:12px}.nlp3d-img{display:block;width:100%;border-radius:10px}.nlp3d-svg{position:absolute;inset:0;width:100%;height:100%}.nlp3d-stage:not(:has(img)) .nlp3d-svg{position:static;background:#f5efe2;border-radius:10px;min-height:300px}.nlp3d-unit{fill:rgba(23,107,53,.28);stroke:#176b35;stroke-width:2;cursor:pointer;transition:fill .15s}.nlp3d-unit:hover,.nlp3d-unit:focus{fill:rgba(23,107,53,.55);outline:none}.nlp3d-unit.st-reserved{fill:rgba(216,144,16,.3);stroke:#b97f10}.nlp3d-unit.st-sold{fill:rgba(120,120,120,.35);stroke:#888;cursor:not-allowed}.nlp3d-panel{position:relative;margin-top:14px;border:1px solid #e3d9c4;border-radius:12px;padding:16px;background:#fff}.nlp3d-close{position:absolute;top:8px;left:10px;border:0;background:none;font-size:22px;cursor:pointer}.nlp3d-facts{display:grid;grid-template-columns:repeat(auto-fit,minmax(120px,1fr));gap:8px;margin:10px 0}.nlp3d-facts div{background:#faf6ec;border-radius:8px;padding:8px 10px;font-size:14px}.nlp3d-facts dt{font-size:12px;color:#8a7a55}.nlp3d-facts dd{margin:0;font-weight:700}.nlp3d-lead{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-top:8px}.nlp3d-cta-line,.nlp3d-ok{grid-column:1/-1;margin:0}.nlp3d-lead input{padding:10px;border:1px solid #ddd1b8;border-radius:8px}.nlp3d-send{grid-column:1/-1;padding:12px;border:0;border-radius:10px;background:#176b35;color:#fff;font-weight:700;cursor:pointer}.nlp3d-hp{position:absolute;left:-9999px}.nlp3d-ok{color:#176b35;font-weight:700}@media(max-width:600px){.nlp3d-lead{grid-template-columns:1fr}}' );
	wp_register_script( 'nadlan-p3d', '', array(), '1.57.0', true );
	wp_enqueue_script( 'nadlan-p3d' );
	$rest = esc_url_raw( rest_url( 'nadlan/v1/lead' ) );
	wp_add_inline_script( 'nadlan-p3d', 'document.querySelectorAll(".nlp3d").forEach(function(w){var data={};try{data=JSON.parse(w.querySelector(".nlp3d-data").textContent)}catch(e){}var byId={};data.forEach(function(u){byId[u.id]=u});var panel=w.querySelector(".nlp3d-panel"),title=w.querySelector(".nlp3d-t"),facts=w.querySelector(".nlp3d-facts"),plan=w.querySelector(".nlp3d-plan"),form=w.querySelector(".nlp3d-lead"),ok=w.querySelector(".nlp3d-ok"),cur=null;function fmt(n){return new Intl.NumberFormat("he-IL").format(n)}function open(u){cur=u;title.textContent="דירת "+u.rooms+" חדרים, קומה "+u.floor;facts.innerHTML="";[["שטח",u.sqm+" מ\\u05f4ר"],["מרפסת",u.balcony+" מ\\u05f4ר"],["כיוון",u.dir||"-"],["מחיר",u.price?"\\u20aa"+fmt(u.price):"לפי פנייה"],["סטטוס",u.status==="available"?"זמינה":u.status==="reserved"?"שמורה":"נמכרה"]].forEach(function(p){var d=document.createElement("div");d.innerHTML="<dt>"+p[0]+"</dt><dd>"+p[1]+"</dd>";facts.appendChild(d)});if(u.plan){plan.href=u.plan;plan.hidden=false}else{plan.hidden=true}ok.hidden=true;form.hidden=u.status==="sold";panel.hidden=false;panel.scrollIntoView({behavior:"smooth",block:"nearest"})}w.querySelectorAll(".nlp3d-unit").forEach(function(p){function h(){var u=byId[p.dataset.unit];if(u&&u.status!=="sold")open(u);else if(u)open(u)}p.addEventListener("click",h);p.addEventListener("keydown",function(e){if(e.key==="Enter"||e.key===" "){e.preventDefault();h()}})});w.querySelector(".nlp3d-close").addEventListener("click",function(){panel.hidden=true});form.addEventListener("submit",function(e){e.preventDefault();var fd=new FormData(form);var msg="פנייה מבחירת דירה אינטראקטיבית: דירת "+(cur?cur.rooms:"")+" חדרים, קומה "+(cur?cur.floor:"")+", "+(cur?cur.sqm:"")+" מ\\u05f4ר"+(cur&&cur.price?", מחיר מבוקש \\u20aa"+fmt(cur.price):"");fetch("'+$rest+'",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({card_id:parseInt(w.dataset.project,10),name:fd.get("name"),phone:fd.get("phone"),email:fd.get("email"),message:msg,company:fd.get("company"),source:"project_3d",unit:cur?cur.id:""})}).then(function(r){return r.json()}).then(function(){ok.hidden=false;form.querySelector(".nlp3d-send").disabled=true}).catch(function(){ok.textContent="שליחה נכשלה, נסו שוב או חייגו אלינו.";ok.hidden=false})});});' );
} );

// Auto-append the picker on project pages that have 3D meta (or demo flag).
add_filter( 'the_content', function ( $content ) {
	if ( ! nadlan_p3d_enabled() || ! is_singular( 'nadlan_project' ) || ! in_the_loop() || ! is_main_query() ) { return $content; }
	$pid = get_the_ID();
	if ( get_post_meta( $pid, 'project_3d_image', true ) === '' && get_post_meta( $pid, 'project_3d_units', true ) === '' && get_post_meta( $pid, 'project_3d_demo', true ) !== '1' ) { return $content; }
	return $content . nadlan_p3d_render( $pid );
}, 30 );

// Admin metabox: paste render URL + units JSON + viewBox on a project.
add_action( 'add_meta_boxes', function () {
	if ( ! nadlan_p3d_enabled() ) { return; }
	add_meta_box( 'nadlan-p3d', 'בחירת דירות אינטראקטיבית (3D)', function ( $post ) {
		wp_nonce_field( 'nadlan_p3d_save', 'nadlan_p3d_nonce' );
		$img = esc_attr( (string) get_post_meta( $post->ID, 'project_3d_image', true ) );
		$vb  = esc_attr( (string) get_post_meta( $post->ID, 'project_3d_viewbox', true ) );
		$js  = esc_textarea( (string) get_post_meta( $post->ID, 'project_3d_units', true ) );
		$dm  = get_post_meta( $post->ID, 'project_3d_demo', true ) === '1';
		echo '<p><label>כתובת תמונת ההדמיה (חזית/חתך)<br><input type="url" name="project_3d_image" value="' . $img . '" class="widefat"></label></p>';
		echo '<p><label>viewBox (ברירת מחדל 0 0 1000 540)<br><input type="text" name="project_3d_viewbox" value="' . $vb . '" class="widefat"></label></p>';
		echo '<p><label>יחידות (JSON: id, points, floor, rooms, sqm, balcony, dir, price, status, plan)<br><textarea name="project_3d_units" rows="8" class="widefat code">' . $js . '</textarea></label></p>';
		echo '<p><label><input type="checkbox" name="project_3d_demo" value="1" ' . checked( $dm, true, false ) . '> הצג תצוגת הדגמה גם בלי נתונים</label></p>';
	}, 'nadlan_project', 'normal' );
} );
add_action( 'save_post_nadlan_project', function ( $post_id ) {
	if ( ! isset( $_POST['nadlan_p3d_nonce'] ) || ! wp_verify_nonce( $_POST['nadlan_p3d_nonce'], 'nadlan_p3d_save' ) ) { return; }
	if ( defined( 'DOING_AUTOSAVE' ) && DOING_AUTOSAVE ) { return; }
	if ( ! current_user_can( 'edit_post', $post_id ) ) { return; }
	update_post_meta( $post_id, 'project_3d_image', esc_url_raw( wp_unslash( $_POST['project_3d_image'] ?? '' ) ) );
	update_post_meta( $post_id, 'project_3d_viewbox', sanitize_text_field( wp_unslash( $_POST['project_3d_viewbox'] ?? '' ) ) );
	$units = (string) wp_unslash( $_POST['project_3d_units'] ?? '' );
	update_post_meta( $post_id, 'project_3d_units', json_decode( $units ) !== null || $units === '' ? $units : '' );
	update_post_meta( $post_id, 'project_3d_demo', ! empty( $_POST['project_3d_demo'] ) ? '1' : '0' );
} );

add_filter( 'nadlan_config_healthcheck', function ( $out ) {
	$q = new WP_Query( array( 'post_type' => 'nadlan_project', 'post_status' => 'any', 'fields' => 'ids', 'posts_per_page' => 1, 'meta_query' => array( 'relation' => 'OR', array( 'key' => 'project_3d_units', 'compare' => 'EXISTS' ), array( 'key' => 'project_3d_demo', 'value' => '1' ) ) ) );
	$out['project_3d'] = array( 'enabled' => nadlan_p3d_enabled(), 'projects_with_3d' => (int) $q->found_posts );
	wp_reset_postdata();
	return $out;
} );
