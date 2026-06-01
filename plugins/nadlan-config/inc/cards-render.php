<?php
/**
 * nadlan-config — Card front-end render (v1.5.0)
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
		$g = function ( $k ) use ( $id ) { return trim( (string) get_post_meta( $id, $k, true ) ); };
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
			$pt_map = array( 'tama38' => 'תמ"א 38', 'pinui_binui' => 'פינוי-בינוי', 'new' => 'בנייה חדשה',
				'mehir_lamishtaken' => 'מחיר למשתכן', 'other' => 'אחר' );
			$rows['סוג פרויקט']   = $pt_map[ $g( 'project_type' ) ] ?? $g( 'project_type' );
			$rows['סטטוס']        = $g( 'project_status' );
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

	<?php if ( $claim_status !== 'verified' ) : ?>
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
.nlcard{margin:24px 0;font-family:var(--font-sans,Heebo,sans-serif)}
.nlcard-facts{width:100%;border-collapse:collapse;margin:0 0 18px}
.nlcard-facts th,.nlcard-facts td{text-align:right;padding:9px 12px;border-bottom:1px solid rgba(27,26,23,.1);font-size:15px}
.nlcard-facts th{color:#6b6b6b;font-weight:500;width:42%;white-space:nowrap}
.nlcard-gallery{display:grid;grid-template-columns:repeat(auto-fill,minmax(120px,1fr));gap:8px;margin:0 0 18px}
.nlcard-gallery img{width:100%;height:110px;object-fit:cover;border-radius:4px}
.nlcard-claim{background:#FAF7F1;border:1px solid rgba(27,26,23,.12);border-radius:6px;padding:20px;margin:18px 0}
.nlcard-claim strong{font-size:17px}
.nlcard-claim p{font-size:14px;color:#555;margin:6px 0 12px}
.nlcard-claim-form{display:grid;gap:8px;max-width:420px}
.nlcard-claim-form input{padding:10px;border:1px solid rgba(27,26,23,.2);border-radius:4px;font:inherit}
.nlcard-claim-form button{padding:11px;background:#1B1A17;color:#FAF7F1;border:0;border-radius:4px;font-weight:500;cursor:pointer}
.nlcard-claim-form button:hover{background:#9C7A3C;color:#1B1A17}
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
