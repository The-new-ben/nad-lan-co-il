<?php
/**
 * nadlan-config — Claim prompt on directory + profile (v1.40.0 / shark #11)
 *
 * Adds a contextual "this is my card?" prompt on every unclaimed professional
 * profile page. Contractors searching their own name (a common behavior — they
 * Google themselves) hit the profile and see a clear claim-this-card path
 * → claim → 30-day Pro trial → recurring revenue.
 *
 * The claim funnel itself already exists in inc/claim.php (created in v1.5.0).
 * This module just makes it impossible to miss.
 */
if ( ! defined( 'ABSPATH' ) ) { exit; }

if ( ! function_exists( 'nadlan_cp_render' ) ) {
	function nadlan_cp_render( $id ) {
		$claim = (string) get_post_meta( $id, 'claim_status', true );
		if ( $claim === 'verified' || $claim === 'pending' ) { return ''; } // only unclaimed
		$title = esc_attr( get_the_title( $id ) );
		ob_start(); ?>
<div class="nlcp" dir="rtl" id="nadlan-claim-prompt">
	<div class="nlcp-icon">🪪</div>
	<div class="nlcp-body">
		<h3>זה הכרטיס שלכם?</h3>
		<p>פתחנו לכם כרטיס בחינם ממאגר רשם הקבלנים הרשמי. רוצים לערוך, להוסיף תמונות, לקבל לידים? בקשו בעלות וקבלו <strong>30 ימי Pro חינם</strong>.</p>
	</div>
	<div class="nlcp-cta">
		<button type="button" class="nlcp-btn" onclick="nadlanClaimNow(<?php echo (int) $id; ?>,'<?php echo esc_js( get_the_title( $id ) ); ?>')">בקשת בעלות + 30 ימי Pro חינם</button>
	</div>
</div>
<style>
.nlcp{font-family:var(--font-sans,Heebo,sans-serif);direction:rtl;display:flex;gap:16px;align-items:center;flex-wrap:wrap;background:linear-gradient(135deg,#F5FBFF,#E7F3FF);border:1px solid rgba(37,99,235,.25);border-radius:14px;padding:18px 22px;margin:20px 0}
.nlcp-icon{font-size:38px;line-height:1}
.nlcp-body{flex:1;min-width:220px}
.nlcp-body h3{font-family:var(--font-serif,"Frank Ruhl Libre",serif);font-size:18px;font-weight:600;color:#1B1A17;margin:0 0 4px}
.nlcp-body p{font-size:13.5px;color:#5a5a5a;line-height:1.55;margin:0}
.nlcp-cta{min-width:200px}
.nlcp-btn{background:#2563EB;color:#fff;border:0;border-radius:10px;padding:12px 18px;font:inherit;font-weight:700;font-size:13.5px;cursor:pointer;transition:transform .15s,background .2s;width:100%}
.nlcp-btn:hover{background:#1d4ed8;transform:translateY(-2px)}
</style>
<script>
window.nadlanClaimNow=window.nadlanClaimNow||function(id,name){
	var n=prompt('שמכם המלא:');if(!n)return;
	var e=prompt('אימייל:');if(!e)return;
	var p=prompt('טלפון:');if(!p)return;
	fetch('<?php echo esc_js( rest_url( 'nadlan/v1/lead' ) ); ?>',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({name:n,email:e,phone:p,goal:'בקשת בעלות + 30 ימי Pro חינם',message:'כרטיס: '+name+' (#'+id+')',source:'claim-prompt'})})
		.then(function(r){return r.json();})
		.then(function(d){alert((d&&d.ok!==false)?'✓ הבקשה התקבלה. אנשי הצוות יחזרו אליכם תוך 24 שעות לאימות הזהות, ולאחר מכן יופעלו 30 ימי Pro חינם.':'שגיאה. נסו שוב.');try{(window.dataLayer=window.dataLayer||[]).push({event:'claim_request',card_id:id});}catch(e){}})
		.catch(function(){alert('שגיאה ברשת. נסו שוב.');});
};
</script>
<?php
		return ob_get_clean();
	}
}

add_filter( 'the_content', function ( $content ) {
	if ( ! is_singular( 'nadlan_professional' ) || ! in_the_loop() || ! is_main_query() ) { return $content; }
	return $content . nadlan_cp_render( get_the_ID() );
}, 24 );
