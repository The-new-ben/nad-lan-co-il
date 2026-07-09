<?php
/**
 * nadlan-config - Card front-end render (v1.5.0)
 *
 * Appends to single card views (project / professional / property):
 *   - a facts/stats table built from meta (the "Wikipedia-style" data block),
 *   - a media gallery from photos_csv,
 *   - a CLAIM CTA (if unclaimed) that posts to /nadlan/v1/claim,
 *   - a provenance line (source + last updated).
 * Also registers a [nadlan_card] shortcode and a [nadlan_directory] index list.
 *
 * Theme-safe: appends via the_content (does not fight block templates) and ships
 * scoped inline CSS/JS only on card views.
 */

if ( ! defined( 'ABSPATH' ) ) { exit; }

if ( ! function_exists( 'nadlan_card_fact_rows' ) ) {
	function nadlan_card_fact_rows( $id, $type ) {
		$g = function ( $k ) use ( $id ) { return trim( preg_replace( '/\s+/u', ' ', (string) get_post_meta( $id, $k, true ) ) ); };
		$rows = array();
		if ( $type === 'nadlan_professional' ) {
			$prof_map = array( 'kablan' => 'קבלן רשום', 'shamai' => 'שמאי מקרקעין', 'bedek_bait' => 'בדק בית',
				'mashkanta' => 'יועץ משכנתאות', 'architect' => 'אדריכל', 'lawyer' => 'עו"ד מקרקעין', 'inspector' => 'מפקח בנייה' );
			$rows['סוג']               = $prof_map[ $g( 'profession' ) ] ?? $g( 'profession' );
			$rows['מספר רשם הקבלנים']  = $g( 'registry_number' );
			$rows['סיווג וענפים']      = $g( 'classification' );
			$rows['עיר']               = $g( 'city' );
			$rows['כתובת']             = $g( 'address' );
			$rows['ותק (שנים)']        = $g( 'years_active' );
			$rows['פרויקטים']          = (int) $g( 'project_count' ) ?: '';
		} elseif ( $type === 'nadlan_project' ) {
			// Design audit 2026-07-02 (D3): NEVER leak raw machine enums like
			// "new_build" to buyers - map every known value, hide unknown slugs.
			$pt_map = array( 'tama38' => 'תמ"א 38', 'pinui_binui' => 'פינוי-בינוי', 'new' => 'בנייה חדשה',
				'new_build' => 'בנייה חדשה', 'mehir_lamishtaken' => 'מחיר למשתכן', 'other' => 'אחר' );
			$st_map = array( 'planning' => 'בתכנון', 'permits' => 'בהיתרים', 'pre_sale' => 'טרום מכירה',
				'marketing' => 'בשיווק', 'construction' => 'בבנייה', 'completed' => 'הושלם', 'occupancy' => 'באכלוס' );
			$label  = function ( $v, $map ) {
				if ( isset( $map[ $v ] ) ) { return $map[ $v ]; }
				return preg_match( '/^[a-z0-9_\-]+$/', (string) $v ) ? '' : $v; // hide raw slugs
			};
			$rows['סוג פרויקט']   = $label( $g( 'project_type' ), $pt_map );
			$rows['סטטוס']        = $label( $g( 'project_status' ), $st_map );
			$rows['עיר']          = $g( 'city' );
			$rows['יזם']          = $g( 'developer_name' );
			$rows['קבלן']         = $g( 'contractor_name' );
			$rows['יחידות דיור']  = (int) $g( 'num_units' ) ?: '';
			$rows['יח"ד קיימות']  = (int) $g( 'units_existing' ) ?: '';
			$rows['יח"ד נוספות']  = (int) $g( 'units_added' ) ?: '';
			$rows['מספר תוכנית']  = $g( 'plan_number' );
			$rows['שנת תוקף']     = (int) $g( 'completion_year' ) ?: '';
		} else { // property
			$rows['סוג']      = $g( 'property_type' );
			$rows['עסקה']     = $g( 'listing_type' );
			$rows['מחיר']     = $g( 'price' ) ? '₪' . number_format( (float) $g( 'price' ) ) : '';
			$rows['חדרים']    = $g( 'rooms' );
			$rows['מ"ר']      = $g( 'size_sqm' );
			$rows['קומה']     = $g( 'floor' );
			$rows['עיר']      = $g( 'city' );
		}
		return array_filter( $rows, function ( $v ) { return $v !== '' && $v !== null; } );
	}
}

if ( ! function_exists( 'nadlan_card_render' ) ) {
	function nadlan_card_render( $id ) {
		$type = get_post_type( $id );
		$rows = nadlan_card_fact_rows( $id, $type );
		$claim_status = get_post_meta( $id, 'claim_status', true ) ?: 'unclaimed';
		$source = get_post_meta( $id, 'source', true );
		ob_start(); ?>
<div class="nlcard" dir="rtl">
	<?php if ( $rows ) : ?>
	<table class="nlcard-facts"><tbody>
		<?php foreach ( $rows as $k => $v ) : ?>
		<tr><th><?php echo esc_html( $k ); ?></th><td><?php echo esc_html( $v ); ?></td></tr>
		<?php endforeach; ?>
	</tbody></table>
	<?php endif; ?>

	<?php
	$photos = array_filter( array_map( 'trim', explode( ',', (string) get_post_meta( $id, 'photos_csv', true ) ) ) );
	if ( $photos ) : ?>
	<div class="nlcard-gallery">
		<?php foreach ( array_slice( $photos, 0, 12 ) as $src ) : ?>
			<a href="<?php echo esc_url( $src ); ?>" target="_blank" rel="noopener"><img src="<?php echo esc_url( $src ); ?>" loading="lazy" alt="<?php echo esc_attr( get_the_title( $id ) ); ?>"></a>
		<?php endforeach; ?>
	</div>
	<?php endif; ?>

	<?php
	// Design audit 2026-07-02 (D4): a "claim this card" pitch is a B2B message
	// on a buyer-facing flagship. Never show it where the showroom engine runs.
	$claim_allowed = ! ( $type === 'nadlan_project'
		&& function_exists( 'nadlan_showroom_engine_active_for' )
		&& nadlan_showroom_engine_active_for( $id ) );
	if ( $claim_allowed && $claim_status !== 'verified' ) : ?>
	<div class="nlcard-claim">
		<strong>זה הכרטיס שלכם?</strong>
		<p>פתחנו לכם כרטיס בחינם. רוצים להוסיף תמונות, לעדכן פרטים ולהשתמש בו ככלי שיווקי? בקשו בעלות והכרטיס יעבור לניהולכם.</p>
		<?php if ( $claim_status === 'pending' ) : ?>
			<p class="nlcard-pending">✓ בקשת בעלות התקבלה וממתינה לאישור.</p>
		<?php else : ?>
		<form class="nlcard-claim-form" onsubmit="return nadlanClaim(this,<?php echo (int) $id; ?>)">
			<input type="text" name="name" placeholder="שם מלא" required>
			<input type="tel" name="phone" placeholder="טלפון">
			<input type="email" name="email" placeholder="אימייל" required>
			<input type="text" name="company" class="nlcard-hp" tabindex="-1" autocomplete="off" aria-hidden="true">
			<button type="submit">בקשו בעלות על הכרטיס</button>
			<span class="nlcard-claim-msg"></span>
		</form>
		<?php endif; ?>
	</div>
	<?php endif; ?>

	<?php if ( $source ) : ?>
	<p class="nlcard-source">המקור: <?php echo esc_html( $source === 'pinkas_hakablanim' ? 'פנקס הקבלנים הרשומים, data.gov.il' : ( $source === 'urban_renewal' ? 'מאגר התחדשות עירונית, data.gov.il' : $source ) ); ?> · עודכן <?php echo esc_html( get_the_modified_date( 'd/m/Y', $id ) ); ?></p>
	<?php endif; ?>
</div>
		<?php
		return ob_get_clean();
	}
}

/* Append to card content on single views */
if ( ! function_exists( 'nadlan_card_append_content' ) ) {
	function nadlan_card_append_content( $content ) {
		if ( is_singular( array( 'nadlan_project', 'nadlan_professional', 'nadlan_property' ) ) && in_the_loop() && is_main_query() ) {
			if ( is_singular( 'nadlan_project' ) && function_exists( 'nadlan_showroom_engine_composed_for' ) && nadlan_showroom_engine_composed_for( get_the_ID() ) ) { return $content; }
			$content .= nadlan_card_render( get_the_ID() );
		}
		return $content;
	}
}
add_filter( 'the_content', 'nadlan_card_append_content', 20 );

/* Shortcode */
add_shortcode( 'nadlan_card', function ( $atts ) {
	$a = shortcode_atts( array( 'id' => get_the_ID() ), $atts );
	return nadlan_card_render( (int) $a['id'] );
} );

/* Scoped assets (only on card views) */
if ( ! function_exists( 'nadlan_card_assets' ) ) {
	function nadlan_card_assets() {
		if ( ! is_singular( array( 'nadlan_project', 'nadlan_professional', 'nadlan_property' ) ) ) { return; }
		?>
<style>
.nlcard{margin:24px 0;font-family:var(--font-sans,Heebo,sans-serif);--nl-gold:#9C7A3C;--nl-ink:#1B1A17;--nl-cream:#FAF7F1}
/* shiny facts table inside a rounded card */
.nlcard-facts{width:100%;border-collapse:separate;border-spacing:0;margin:0 0 20px;background:#fff;border:1px solid rgba(27,26,23,.1);border-radius:14px;overflow:hidden;box-shadow:0 6px 20px rgba(27,26,23,.05)}
.nlcard-facts th,.nlcard-facts td{text-align:right;padding:13px 18px;border-bottom:1px solid rgba(27,26,23,.07);font-size:15px}
.nlcard-facts tr:last-child th,.nlcard-facts tr:last-child td{border-bottom:0}
.nlcard-facts tr:nth-child(even) th,.nlcard-facts tr:nth-child(even) td{background:#FBF9F5}
.nlcard-facts th{color:#6b6b6b;font-weight:500;width:42%;white-space:nowrap}
.nlcard-facts td{font-weight:600;color:var(--nl-ink)}
.nlcard-gallery{display:grid;grid-template-columns:repeat(auto-fill,minmax(130px,1fr));gap:10px;margin:0 0 20px}
.nlcard-gallery a{overflow:hidden;border-radius:10px;display:block}
.nlcard-gallery img{width:100%;height:120px;object-fit:cover;transition:transform .4s ease;display:block}
.nlcard-gallery a:hover img{transform:scale(1.08)}
.nlcard-claim{background:linear-gradient(135deg,#FAF7F1,#F3ECE0);border:1px solid rgba(156,122,60,.25);border-radius:14px;padding:24px;margin:18px 0;box-shadow:0 6px 20px rgba(156,122,60,.08)}
.nlcard-claim strong{font-size:18px;color:var(--nl-ink)}
.nlcard-claim p{font-size:14px;color:#555;margin:6px 0 14px}
.nlcard-claim-form{display:grid;gap:8px;max-width:420px}
.nlcard-claim-form input{padding:11px;border:1px solid rgba(27,26,23,.18);border-radius:8px;font:inherit}
.nlcard-claim-form button{padding:12px;background:var(--nl-ink);color:var(--nl-cream);border:0;border-radius:8px;font-weight:600;cursor:pointer;transition:background .2s,color .2s}
.nlcard-claim-form button:hover{background:var(--nl-gold);color:#fff}
.nlcard-hp{position:absolute;left:-9999px}
.nlcard-claim-msg{font-size:13px}
.nlcard-pending{color:#2e7d32;font-weight:500}
.nlcard-source{font-size:12px;color:#999;margin-top:10px}
</style>
<script>
function nadlanClaim(f,id){
	var d={post_id:id,name:f.name.value,phone:f.phone.value,email:f.email.value,company:f.company.value};
	var msg=f.querySelector('.nlcard-claim-msg');
	fetch('<?php echo esc_url_raw( rest_url( 'nadlan/v1/claim' ) ); ?>',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(d)})
	.then(function(r){return r.json();}).then(function(j){
		if(j.ok){f.style.display='none';msg.textContent='✓ הבקשה נשלחה. ניצור קשר לאימות הבעלות.';msg.style.color='#2e7d32';}
		else{msg.textContent='שגיאה, נסו שוב.';msg.style.color='#c00';}
	}).catch(function(){msg.textContent='שגיאת רשת.';msg.style.color='#c00';});
	return false;
}
</script>
		<?php
	}
}
add_action( 'wp_footer', 'nadlan_card_assets' );
