<?php
/**
 * nadlan-config — Lead-magnet calculators (v1.19.0)
 *
 * Rulebook §9.3 calculator suite (mortgage + home-value already exist in
 * listings-ux/avm-deals). This adds the rest as client-side shortcodes, each a
 * lead funnel:
 *   [nadlan_calc_purchase_tax]   מס רכישה   (brackets, filterable + dated)
 *   [nadlan_calc_capital_gains]  מס שבח     (ESTIMATE only — heavy disclaimer)
 *   [nadlan_calc_yield]          תשואת שכירות (ברוטו/נטו)
 *   [nadlan_calc_equity]         הון עצמי נדרש (LTV per Bank of Israel)
 *   [nadlan_calc_total_cost]     עלות רכישה כוללת
 *
 * YMYL discipline: tax figures are FINANCIAL. Brackets live in a filterable PHP
 * array with an effective-date label + a visible "verify with רשות המסים" line +
 * authority link. Capital-gains is genuinely complex (linear calc + exemptions),
 * so that one is an explicit ESTIMATE with a lawyer/tax-advisor CTA, never a
 * definitive number.
 *
 * BLANK (owner/Cowork): the surrounding pillar-page Hebrew copy (H1, explainer,
 * FAQ, spokes) is written via the ChatGPT→Cowork batch; this module is the WIDGET.
 * Update brackets each January via the nadlan_purchase_tax_brackets filter.
 */

if ( ! defined( 'ABSPATH' ) ) { exit; }

/* ---- purchase-tax brackets (single residence, IL resident) — UPDATE ANNUALLY ----
 * Approximate brackets for the 16.1.2025–15.1.2026 year. Filterable so the owner/
 * Cowork can update without a code release. Always shown with the effective-date
 * label + a verify link.
 */
if ( ! function_exists( 'nadlan_purchase_tax_config' ) ) {
	function nadlan_purchase_tax_config() {
		return apply_filters( 'nadlan_purchase_tax_brackets', array(
			'effective' => '16.1.2025',
			'source'    => 'https://www.gov.il/he/departments/topics/purchase_tax',
			// single apartment (דירה יחידה): [ceiling, rate]; last = Infinity
			'single' => array(
				array( 1978745, 0.0 ),
				array( 2347040, 0.035 ),
				array( 6055070, 0.05 ),
				array( 20183565, 0.08 ),
				array( PHP_INT_MAX, 0.10 ),
			),
			// additional/investment apartment (דירה נוספת)
			'additional' => array(
				array( 6055070, 0.08 ),
				array( PHP_INT_MAX, 0.10 ),
			),
		) );
	}
}

/* expose brackets to JS so the math is transparent + auditable */
add_action( 'wp_footer', function () {
	if ( ! is_singular() && ! is_page() ) { return; }
	$cfg = nadlan_purchase_tax_config();
	echo '<script>window.NADLAN_PTAX=' . wp_json_encode( $cfg ) . ';</script>';
}, 5 );

/* shared lead-capture snippet appended to each calculator */
if ( ! function_exists( 'nadlan_calc_lead_js' ) ) {
	function nadlan_calc_lead_js( $topic ) {
		return 'function(name,phone,extra){fetch("' . esc_js( rest_url( 'nadlan/v1/lead' ) ) . '",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({name:name,phone:phone,topic:"' . esc_js( $topic ) . '",message:extra,source:"calculator"})});}';
	}
}

/* shared styles (printed once) */
if ( ! function_exists( 'nadlan_calc_styles' ) ) {
	function nadlan_calc_styles() {
		static $done = false; if ( $done ) { return ''; } $done = true;
		return '<style>
.nlcalc{max-width:520px;margin:20px 0;font-family:var(--font-sans,Heebo,sans-serif);direction:rtl}
.nlcalc h3{font-family:var(--font-serif,"Frank Ruhl Libre",serif);font-size:22px;margin:0 0 12px;color:#1B1A17}
.nlcalc label{display:block;font-size:13px;color:#5C564D;margin:10px 0 3px}
.nlcalc input,.nlcalc select{width:100%;padding:9px 0;border:0;border-bottom:1px solid #C9C0AE;background:transparent;font:inherit;font-size:16px;color:#1B1A17}
.nlcalc input:focus,.nlcalc select:focus{outline:none;border-bottom:1.5px solid #9C7A3C}
.nlcalc button{margin-top:14px;padding:11px 24px;background:#1B1A17;color:#FAF7F1;border:0;border-radius:4px;font:inherit;font-weight:500;cursor:pointer}
.nlcalc button:hover{background:#9C7A3C;color:#1B1A17}
.nlcalc-out{margin-top:16px;font-size:15px;font-variant-numeric:tabular-nums}
.nlcalc-big{font-size:30px;font-weight:700;color:#1B1A17;letter-spacing:-.02em}
.nlcalc-disc{font-size:12px;color:#999;margin-top:10px;border-top:1px solid #E2DCD0;padding-top:8px}
.nlcalc-disc a{color:#9C7A3C}
.nlcalc-cta{margin-top:12px;font-size:13px;background:#FAF7F1;border:1px solid #E2DCD0;border-radius:6px;padding:12px}
.nlcalc-cta input{border:1px solid #C9C0AE;border-radius:4px;padding:8px;margin:4px 0}
</style>';
	}
}

/* ===== 1. מס רכישה ===== */
add_shortcode( 'nadlan_calc_purchase_tax', function () {
	$cfg = nadlan_purchase_tax_config();
	ob_start(); echo nadlan_calc_styles(); ?>
<div class="nlcalc" id="nlptax">
	<h3>מחשבון מס רכישה</h3>
	<label>מחיר הנכס (₪)</label>
	<input type="number" id="ptax-price" value="2500000">
	<label>סוג הרכישה</label>
	<select id="ptax-type"><option value="single">דירה יחידה</option><option value="additional">דירה נוספת / להשקעה</option></select>
	<button onclick="nadlanPtax()">חשבו מס רכישה</button>
	<div class="nlcalc-out"></div>
	<p class="nlcalc-disc">המדרגות מעודכנות לתאריך <?php echo esc_html( $cfg['effective'] ); ?>. הן מתעדכנות מדי שנה; לאימות מול המקור הרשמי: <a href="<?php echo esc_url( $cfg['source'] ); ?>" target="_blank" rel="noopener nofollow">רשות המסים</a>. אומדן בלבד, אינו חוות דעת מס.</p>
</div>
<script>
function nadlanPtax(){
	var price=+document.getElementById('ptax-price').value||0, type=document.getElementById('ptax-type').value;
	var b=window.NADLAN_PTAX[type], tax=0, prev=0;
	for(var i=0;i<b.length;i++){var ceil=b[i][0],rate=b[i][1];var span=Math.max(0,Math.min(price,ceil)-prev);tax+=span*rate;prev=ceil;if(price<=ceil)break;}
	var eff=price>0?(tax/price*100):0;
	document.querySelector('#nlptax .nlcalc-out').innerHTML='מס רכישה משוער: <span class="nlcalc-big">₪'+Math.round(tax).toLocaleString()+'</span><br>שיעור אפקטיבי: '+eff.toFixed(2)+'%';
}
nadlanPtax();
</script>
	<?php return ob_get_clean();
} );

/* ===== 2. מס שבח (ESTIMATE — heavy disclaimer) ===== */
add_shortcode( 'nadlan_calc_capital_gains', function () {
	ob_start(); echo nadlan_calc_styles(); ?>
<div class="nlcalc" id="nlcgt">
	<h3>מחשבון מס שבח (אומדן)</h3>
	<label>מחיר מכירה (₪)</label><input type="number" id="cgt-sell" value="2800000">
	<label>מחיר רכישה מקורי (₪)</label><input type="number" id="cgt-buy" value="1800000">
	<label>הוצאות מוכרות (שיפוץ, עו"ד, תיווך) (₪)</label><input type="number" id="cgt-exp" value="120000">
	<button onclick="nadlanCgt()">חשבו אומדן</button>
	<div class="nlcalc-out"></div>
	<div class="nlcalc-cta">
		<strong>מס שבח מורכב</strong> (חישוב לינארי, פטורים, יום רכישה). זהו אומדן גס בלבד בשיעור 25% על השבח הריאלי. לחישוב מדויק ובדיקת זכאות לפטור, כדאי להתייעץ.
		<div><input type="text" id="cgt-name" placeholder="שם"><input type="tel" id="cgt-phone" placeholder="טלפון"></div>
		<button onclick="nadlanCgtLead()">קבלו בדיקת זכאות לפטור</button>
	</div>
	<p class="nlcalc-disc">אומדן בלבד, אינו חוות דעת מס. מקור המדרגות והפטורים: <a href="https://www.gov.il/he/departments/topics/betterment_tax" target="_blank" rel="noopener nofollow">רשות המסים</a>.</p>
</div>
<script>
function nadlanCgt(){
	var s=+document.getElementById('cgt-sell').value||0,b=+document.getElementById('cgt-buy').value||0,e=+document.getElementById('cgt-exp').value||0;
	var gain=Math.max(0,s-b-e), tax=gain*0.25;
	document.querySelector('#nlcgt .nlcalc-out').innerHTML='שבח (אומדן): ₪'+Math.round(gain).toLocaleString()+'<br>מס שבח משוער (25%): <span class="nlcalc-big">₪'+Math.round(tax).toLocaleString()+'</span><br><small style="color:#b4623f">לפני בדיקת פטורים. ייתכן שתהיו פטורים לחלוטין.</small>';
}
var nlCgtLead=<?php echo nadlan_calc_lead_js( 'מס שבח: בדיקת פטור' ); ?>;
function nadlanCgtLead(){var n=document.getElementById('cgt-name').value,p=document.getElementById('cgt-phone').value;if(!p){alert('נא להשאיר טלפון');return;}nlCgtLead(n,p,'מס שבח calculator');document.querySelector('#nlcgt .nlcalc-cta').innerHTML='✓ הבקשה התקבלה, ניצור קשר לבדיקת זכאות.';}
nadlanCgt();
</script>
	<?php return ob_get_clean();
} );

/* ===== 3. תשואת שכירות ===== */
add_shortcode( 'nadlan_calc_yield', function () {
	ob_start(); echo nadlan_calc_styles(); ?>
<div class="nlcalc" id="nlyield">
	<h3>מחשבון תשואת שכירות</h3>
	<label>מחיר הנכס (₪)</label><input type="number" id="y-price" value="1800000">
	<label>שכר דירה חודשי (₪)</label><input type="number" id="y-rent" value="5500">
	<label>הוצאות שנתיות (ועד, ביטוח, אחזקה, ארנונה) (₪)</label><input type="number" id="y-exp" value="6000">
	<button onclick="nadlanYield()">חשבו תשואה</button>
	<div class="nlcalc-out"></div>
	<p class="nlcalc-disc">תשואה ברוטו = שכר שנתי ÷ מחיר. נטו = (שכר שנתי פחות הוצאות) ÷ מחיר. אינו כולל מימון/מיסוי. אומדן בלבד.</p>
</div>
<script>
function nadlanYield(){
	var p=+document.getElementById('y-price').value||0,r=+document.getElementById('y-rent').value||0,e=+document.getElementById('y-exp').value||0;
	var annual=r*12, gross=p>0?annual/p*100:0, net=p>0?(annual-e)/p*100:0;
	document.querySelector('#nlyield .nlcalc-out').innerHTML='תשואה ברוטו: <span class="nlcalc-big">'+gross.toFixed(2)+'%</span><br>תשואה נטו: '+net.toFixed(2)+'% · הכנסה שנתית נטו: ₪'+Math.round(annual-e).toLocaleString();
}
nadlanYield();
</script>
	<?php return ob_get_clean();
} );

/* ===== 4. הון עצמי נדרש (LTV per Bank of Israel) ===== */
add_shortcode( 'nadlan_calc_equity', function () {
	ob_start(); echo nadlan_calc_styles(); ?>
<div class="nlcalc" id="nleq">
	<h3>מחשבון הון עצמי נדרש</h3>
	<label>מחיר הנכס (₪)</label><input type="number" id="eq-price" value="2200000">
	<label>סוג הרוכש</label>
	<select id="eq-type">
		<option value="0.75">דירה יחידה (עד 75% מימון)</option>
		<option value="0.70">דירה חליפית (עד 70% מימון)</option>
		<option value="0.50">משקיע / דירה נוספת (עד 50% מימון)</option>
	</select>
	<button onclick="nadlanEq()">חשבו הון עצמי</button>
	<div class="nlcalc-out"></div>
	<p class="nlcalc-disc">מגבלות המימון (LTV) לפי הוראות בנק ישראל. אינו כולל מס רכישה ועלויות נלוות (ראו מחשבון עלות כוללת). אומדן בלבד.</p>
</div>
<script>
function nadlanEq(){
	var p=+document.getElementById('eq-price').value||0,ltv=+document.getElementById('eq-type').value;
	var loan=p*ltv, eq=p-loan;
	document.querySelector('#nleq .nlcalc-out').innerHTML='הון עצמי מינימלי: <span class="nlcalc-big">₪'+Math.round(eq).toLocaleString()+'</span><br>('+Math.round((1-ltv)*100)+'% מהמחיר) · משכנתא מקסימלית: ₪'+Math.round(loan).toLocaleString();
}
nadlanEq();
</script>
	<?php return ob_get_clean();
} );

/* ===== 5. עלות רכישה כוללת ===== */
add_shortcode( 'nadlan_calc_total_cost', function () {
	ob_start(); echo nadlan_calc_styles(); ?>
<div class="nlcalc" id="nltc">
	<h3>מחשבון עלות רכישה כוללת</h3>
	<label>מחיר הנכס (₪)</label><input type="number" id="tc-price" value="2200000">
	<label>סוג רכישה</label>
	<select id="tc-type"><option value="single">דירה יחידה</option><option value="additional">דירה נוספת</option></select>
	<label>עו"ד (% מהמחיר, נפוץ 0.5%)</label><input type="number" id="tc-lawyer" value="0.5" step="0.1">
	<label>תיווך (% מהמחיר, נפוץ 2%; 0 אם אין)</label><input type="number" id="tc-broker" value="2" step="0.5">
	<button onclick="nadlanTc()">חשבו עלות כוללת</button>
	<div class="nlcalc-out"></div>
	<p class="nlcalc-disc">כולל מס רכישה (לפי המדרגות העדכניות), עו"ד ותיווך + מע"מ 18%, ושמאי/בדיקות (אומדן ₪3,000). אומדן בלבד.</p>
</div>
<script>
function nadlanTc(){
	var p=+document.getElementById('tc-price').value||0,type=document.getElementById('tc-type').value;
	var b=window.NADLAN_PTAX[type],ptax=0,prev=0;
	for(var i=0;i<b.length;i++){var c=b[i][0],r=b[i][1];ptax+=Math.max(0,Math.min(p,c)-prev)*r;prev=c;if(p<=c)break;}
	var vat=1.18;
	var lawyer=p*(+document.getElementById('tc-lawyer').value/100)*vat;
	var broker=p*(+document.getElementById('tc-broker').value/100)*vat;
	var misc=3000;
	var total=p+ptax+lawyer+broker+misc;
	document.querySelector('#nltc .nlcalc-out').innerHTML='עלות כוללת משוערת: <span class="nlcalc-big">₪'+Math.round(total).toLocaleString()+'</span><br>מתוכה מעבר למחיר: ₪'+Math.round(total-p).toLocaleString()+'<br><small>מס רכישה ₪'+Math.round(ptax).toLocaleString()+' · עו"ד ₪'+Math.round(lawyer).toLocaleString()+' · תיווך ₪'+Math.round(broker).toLocaleString()+' · בדיקות ₪'+misc.toLocaleString()+'</small>';
}
nadlanTc();
</script>
	<?php return ob_get_clean();
} );
