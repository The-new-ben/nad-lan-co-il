<?php
/**
 * nadlan-config - Buy-vs-Rent decision engine + apartment deal analyzer (v1.71.4)
 *
 * Two traffic-magnet tools, NYT-methodology with the Israeli layer no one else has:
 *   [nadlan_buy_vs_rent]   year-by-year simulation: buying (mortgage, purchase tax
 *                          from the dated brackets in calculators.php, upkeep,
 *                          appreciation, selling costs) vs renting AND investing the
 *                          equity + monthly difference. Net-worth curves on canvas,
 *                          break-even year, verdict, sensitivity chips.
 *   [nadlan_deal_check]    "is this apartment a good buy" analyzer: price/sqm vs the
 *                          user's area benchmark, yield vs alternatives, leverage
 *                          stress, total acquisition cost. Letter-grade verdict +
 *                          what-to-check list + AI deep-analysis lead funnel.
 *
 * YMYL discipline: every figure is an estimate with visible assumptions the user
 * controls; purchase tax carries its effective date + verify link; no result is
 * presented as advice. No long dashes anywhere (owner law).
 */

if ( ! defined( 'ABSPATH' ) ) { exit; }

if ( ! function_exists( 'nadlan_bvr_styles' ) ) {
	function nadlan_bvr_styles() {
		static $done = false; if ( $done ) { return ''; } $done = true;
		return '<style>
.nlbvr{max-width:880px;margin:24px auto;font-family:var(--font-sans,Heebo,sans-serif);direction:rtl;color:#1B1A17}
.nlbvr h3{font-family:var(--font-serif,"Frank Ruhl Libre",serif);font-size:24px;margin:0 0 6px}
.nlbvr .sub{font-size:13.5px;color:#5C564D;margin:0 0 18px}
.nlbvr .grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(190px,1fr));gap:14px 22px;background:#fff;border:1px solid #E2DCD0;border-radius:14px;padding:20px 22px}
.nlbvr .grid h4{grid-column:1/-1;margin:6px 0 0;font-size:12px;letter-spacing:.12em;color:#9C7A3C;text-transform:uppercase;font-weight:700}
.nlbvr label{display:block;font-size:12.5px;color:#5C564D}
.nlbvr input,.nlbvr select{width:100%;padding:8px 0;border:0;border-bottom:1px solid #C9C0AE;background:transparent;font:inherit;font-size:15.5px}
.nlbvr input:focus{outline:none;border-bottom:1.5px solid #9C7A3C}
.nlbvr .run{margin-top:16px;padding:12px 30px;background:#C2563A;color:#fff;border:0;border-radius:999px;font:inherit;font-weight:700;font-size:15px;cursor:pointer}
.nlbvr .run:hover{filter:brightness(1.06)}
.nlbvr-verdict{margin-top:18px;background:#14130F;color:#FAF7F1;border-radius:14px;padding:20px 24px;display:none}
.nlbvr-verdict .v{font-family:var(--font-serif,serif);font-size:26px;color:#E6D4AE}
.nlbvr-verdict .d{font-size:14px;color:#CFC6B4;margin-top:6px;line-height:1.6}
.nlbvr-stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:10px;margin-top:14px}
.nlbvr-stats div{background:rgba(250,247,241,.07);border-radius:10px;padding:10px 12px}
.nlbvr-stats b{display:block;font-size:19px;font-variant-numeric:tabular-nums}
.nlbvr-stats span{font-size:11.5px;color:#B9AF9C}
.nlbvr-chart{margin-top:16px;background:#fff;border:1px solid #E2DCD0;border-radius:14px;padding:14px;display:none}
.nlbvr-chart canvas{width:100%;height:260px}
.nlbvr-legend{font-size:12px;color:#5C564D;display:flex;gap:16px;padding:4px 6px}
.nlbvr-legend i{display:inline-block;width:12px;height:3px;vertical-align:middle;margin-inline-end:5px}
.nlbvr-sens{display:flex;flex-wrap:wrap;gap:8px;margin-top:12px}
.nlbvr-sens span{font-size:12px;background:#F3EEE3;border:1px solid #E2DCD0;border-radius:999px;padding:5px 12px}
.nlbvr-disc{font-size:12px;color:#8B8272;margin-top:12px;line-height:1.6}
.nlbvr-disc a{color:#9C7A3C}
.nlbvr-score{display:flex;align-items:center;gap:18px;margin-top:18px;background:#14130F;color:#FAF7F1;border-radius:14px;padding:20px 24px;display:none}
.nlbvr-grade{font-family:var(--font-serif,serif);font-size:56px;color:#E6D4AE;min-width:80px;text-align:center}
.nlbvr-bars{flex:1}
.nlbvr-bar{margin:7px 0}
.nlbvr-bar label{color:#CFC6B4;font-size:12px;display:flex;justify-content:space-between}
.nlbvr-bar .tr{height:7px;background:rgba(250,247,241,.12);border-radius:99px;overflow:hidden}
.nlbvr-bar .fl{height:100%;border-radius:99px;background:#9C7A3C;transition:width .6s}
.nlbvr-checks{margin-top:14px;background:#fff;border:1px solid #E2DCD0;border-radius:14px;padding:16px 20px;font-size:14px;display:none}
.nlbvr-checks li{margin:6px 0}
.nlbvr-ai{margin-top:14px;background:#F3EEE3;border:1px solid #E2DCD0;border-radius:14px;padding:16px 20px;display:none}
.nlbvr-ai input{border:1px solid #C9C0AE;border-radius:6px;padding:9px;margin:4px 6px 4px 0;font:inherit;width:auto}
.nlbvr-ai button{padding:9px 20px;background:#1B1A17;color:#FAF7F1;border:0;border-radius:999px;font:inherit;cursor:pointer}
@media(max-width:640px){.nlbvr-score{flex-direction:column}}
</style>';
	}
}

if ( ! function_exists( 'nadlan_bvr_ptax_js' ) ) {
	function nadlan_bvr_ptax_js() {
		static $done = false; if ( $done ) { return ''; } $done = true;
		$tax = function_exists( 'nadlan_purchase_tax_config' ) ? nadlan_purchase_tax_config() : array( 'single' => array() );
		return '<script>var NL_PTAX=' . wp_json_encode( isset( $tax['single'] ) ? $tax['single'] : array() )
			. ';function nlPtaxCalc(p){var t=0,prev=0;for(var i=0;i<NL_PTAX.length;i++){var c=NL_PTAX[i][0],r=NL_PTAX[i][1];if(p>prev){t+=(Math.min(p,c)-prev)*r;prev=c;}else break;}if(p>prev&&NL_PTAX.length){t+=(p-prev)*NL_PTAX[NL_PTAX.length-1][1];}return Math.round(t);}</script>';
	}
}

/* ============================= 1. BUY vs RENT ============================= */
add_shortcode( 'nadlan_buy_vs_rent', function () {
	$tax = function_exists( 'nadlan_purchase_tax_config' ) ? nadlan_purchase_tax_config() : array( 'effective' => '', 'source' => '', 'single' => array() );
	$eff = esc_html( isset( $tax['effective'] ) ? $tax['effective'] : '' );
	nadlan_bvr_mark( 'bvr' );
	ob_start(); echo nadlan_bvr_styles(); ?>
<div class="nlbvr" id="nlbvr">
  <h3>קנייה או שכירות: סימולציה מלאה, שנה אחר שנה</h3>
  <p class="sub">לא רק "כמה עולה משכנתא": המנוע מחשב גם מה היה קורה לכסף שלכם אילו נשאר מושקע. שנו כל הנחה ובדקו את הרגישות.</p>
  <div class="grid">
    <h4>הדירה</h4>
    <div><label>מחיר הדירה (₪)</label><input id="bv_price" type="number" value="2500000" step="50000"></div>
    <div><label>הון עצמי (₪)</label><input id="bv_equity" type="number" value="750000" step="10000"></div>
    <div><label>ריבית משכנתא שנתית (%)</label><input id="bv_rate" type="number" value="5.0" step="0.1"></div>
    <div><label>תקופת משכנתא (שנים)</label><input id="bv_term" type="number" value="25" step="1"></div>
    <h4>עלויות בעלות</h4>
    <div><label>ועד בית + תחזוקה (₪ לחודש)</label><input id="bv_upkeep" type="number" value="1200" step="100"></div>
    <div><label>עליית ערך שנתית (%)</label><input id="bv_appr" type="number" value="3.5" step="0.1"></div>
    <div><label>עלות מכירה עתידית (%)</label><input id="bv_sellc" type="number" value="3" step="0.5"></div>
    <div><label>עו"ד ותיווך בקנייה (%)</label><input id="bv_buyc" type="number" value="1.5" step="0.25"></div>
    <h4>החלופה: שכירות + השקעה</h4>
    <div><label>שכר דירה מקביל (₪ לחודש)</label><input id="bv_rent" type="number" value="7500" step="100"></div>
    <div><label>עליית שכירות שנתית (%)</label><input id="bv_rentg" type="number" value="3" step="0.1"></div>
    <div><label>תשואת השקעה שנתית (%)</label><input id="bv_inv" type="number" value="6" step="0.1"></div>
    <div><label>אופק (שנים)</label><input id="bv_years" type="number" value="15" step="1"></div>
  </div>
  <button class="run" onclick="nlBvrRun()">חשבו לי</button>
  <div class="nlbvr-verdict" id="bv_verdict"></div>
  <div class="nlbvr-chart" id="bv_chartwrap">
    <div class="nlbvr-legend"><span><i style="background:#9C7A3C"></i>שווי נקי בקנייה</span><span><i style="background:#C2563A"></i>שווי נקי בשכירות + השקעה</span></div>
    <canvas id="bv_chart" width="820" height="260"></canvas>
  </div>
  <div class="nlbvr-sens" id="bv_sens"></div>
  <p class="nlbvr-disc">מס רכישה מחושב אוטומטית לפי מדרגות דירה יחידה בתוקף מ-<?php echo $eff; ?> (<a href="<?php echo esc_url( $tax['source'] ); ?>" rel="nofollow noopener" target="_blank">לאימות מול רשות המסים</a>). כל התוצאות אומדן להשוואה בלבד ואינן ייעוץ השקעות, מס או משכנתא. רווחי השקעה חושבו בניכוי 25% מס רווח הון.</p>
</div>

<?php return ob_get_clean();
} );

/* ============================= 2. DEAL CHECK ============================= */
add_shortcode( 'nadlan_deal_check', function () {
	nadlan_bvr_mark( 'deal' );
	ob_start(); echo nadlan_bvr_styles(); ?>
<div class="nlbvr" id="nldeal">
  <h3>בדיקת כדאיות לדירה ספציפית</h3>
  <p class="sub">מזינים את נתוני הדירה ומקבלים ציון משוקלל: מחיר מול השוק, תשואה, עומס מימון ועלות רכישה מלאה, עם רשימת בדיקות לפני החלטה.</p>
  <div class="grid">
    <h4>הדירה הנבדקת</h4>
    <div><label>מחיר מבוקש (₪)</label><input id="dc_price" type="number" value="2400000" step="10000"></div>
    <div><label>שטח (מ"ר)</label><input id="dc_sqm" type="number" value="85" step="1"></div>
    <div><label>שכ"ד חודשי צפוי (₪)</label><input id="dc_rent" type="number" value="6500" step="100"></div>
    <div><label>מחיר ממוצע למ"ר באזור (₪)</label><input id="dc_area" type="number" value="30000" step="500"></div>
    <h4>המימון שלכם</h4>
    <div><label>הון עצמי (₪)</label><input id="dc_equity" type="number" value="720000" step="10000"></div>
    <div><label>הכנסה חודשית נטו של משק הבית (₪)</label><input id="dc_income" type="number" value="24000" step="500"></div>
    <div><label>ריבית משכנתא (%)</label><input id="dc_rate" type="number" value="5.0" step="0.1"></div>
    <div><label>תקופה (שנים)</label><input id="dc_term" type="number" value="25" step="1"></div>
  </div>
  <button class="run" onclick="nlDealRun()">בדקו את הדירה</button>
  <div class="nlbvr-score" id="dc_score"><div class="nlbvr-grade" id="dc_grade"></div><div class="nlbvr-bars" id="dc_bars"></div></div>
  <div class="nlbvr-checks" id="dc_checks"></div>
  <div class="nlbvr-ai" id="dc_ai">
    <b>רוצים ניתוח עומק עם AI ובדיקת השוואה לפרויקטים באזור?</b>
    <div style="margin-top:8px"><input id="dc_name" placeholder="שם"><input id="dc_phone" placeholder="טלפון"><button onclick="nlDealLead()">שלחו לי ניתוח מלא</button></div>
    <div style="font-size:12px;color:#8B8272;margin-top:6px">הניתוח נעשה על נתוני עסקאות אמיתיים ונשלח עם הסתייגויות מלאות. ללא עלות וללא התחייבות.</div>
  </div>
  <p class="nlbvr-disc">מס רכישה לפי מדרגות דירה יחידה בתוקף; אם זו אינה דירתכם היחידה המס גבוה משמעותית. הציון הוא כלי סינון ראשוני בלבד ואינו ייעוץ; לפני עסקה בודקים שמאי, עו"ד ויועץ משכנתאות.</p>
</div>

<?php return ob_get_clean();
} );

/* JS printed in wp_footer, NOT in post content: WordPress content filters
   (texturize/entities) corrupt inline scripts inside the_content. */
if ( ! function_exists( 'nadlan_bvr_mark' ) ) {
	function nadlan_bvr_mark( $which ) {
		static $need = array(); $need[ $which ] = true; return $need;
	}
	function nadlan_bvr_need() { return nadlan_bvr_mark( '_probe' ); }
}
add_action( 'wp_footer', function () {
	$need = nadlan_bvr_mark( '_probe' );
	if ( empty( $need['bvr'] ) && empty( $need['deal'] ) ) { return; }
	echo nadlan_bvr_ptax_js();
	if ( ! empty( $need['bvr'] ) ) { ?>
<script>
function nlBvrRun(){
 var P=+bv_price.value,E=+bv_equity.value,r=+bv_rate.value/100,T=+bv_term.value,up=+bv_upkeep.value,
     g=+bv_appr.value/100,sc=+bv_sellc.value/100,bc=+bv_buyc.value/100,R0=+bv_rent.value,rg=+bv_rentg.value/100,
     inv=+bv_inv.value/100,N=Math.max(2,Math.min(40,+bv_years.value));
 var tax=nlPtaxCalc(P),oneoff=tax+P*bc,loan=P-E;
 if(loan<0){loan=0}
 var mr=r/12,n=T*12,pay=loan>0?loan*mr/(1-Math.pow(1+mr,-n)):0;
 var bal=loan,val=P,rent=R0,port=E+oneoff> P?0:(E>0?E+oneoff:0);
 // renter starts with the SAME cash the buyer spent: equity + tax + closing
 port=E+oneoff;
 var buyC=[],rentC=[],be=null;
 for(var y=1;y<=N;y++){
   for(var m=0;m<12;m++){var i2=bal*mr;var pr=Math.min(pay-i2,bal);bal-=pr;
     var ownerOut=pay+up, renterOut=rent;
     var diff=ownerOut-renterOut;               // if owning costs more, renter invests the diff
     port=port*Math.pow(1+inv,1/12)+(diff>0?diff:0);
     if(diff<0){ /* renting costs more: renter pays from pocket like the owner does */ }
   }
   val*=1+g; rent*=1+rg;
   var gains=port-(E+oneoff); var netPort=port-Math.max(0,gains)*0.25;
   var buyNet=val*(1-sc)-bal;
   buyC.push(buyNet); rentC.push(netPort);
   if(be===null&&buyNet>netPort)be=y;
 }
 var last=N-1,adv=buyC[last]-rentC[last];
 var v=document.getElementById('bv_verdict');v.style.display='block';
 var nf=function(x){return Math.round(x).toLocaleString('he-IL')};
 v.innerHTML='<div class="v">'+(adv>0?'באופק של '+N+' שנים: הקנייה מובילה':'באופק של '+N+' שנים: השכירות + השקעה מובילה')+'</div>'
  +'<div class="d">'+(adv>0?'היתרון הנקי לקנייה: כ-'+nf(Math.abs(adv))+' ₪.':'היתרון הנקי לשוכר המשקיע: כ-'+nf(Math.abs(adv))+' ₪.')
  +(be?' נקודת האיזון: בערך בשנה ה-'+be+'.':' באופק שנבחר הקנייה לא עוקפת את החלופה.')+'</div>'
  +'<div class="nlbvr-stats">'
  +'<div><b>'+nf(pay)+' ₪</b><span>החזר חודשי</span></div>'
  +'<div><b>'+nf(tax)+' ₪</b><span>מס רכישה (דירה יחידה)</span></div>'
  +'<div><b>'+nf(buyC[last])+' ₪</b><span>שווי נקי בקנייה בסוף התקופה</span></div>'
  +'<div><b>'+nf(rentC[last])+' ₪</b><span>שווי נקי בשכירות + השקעה</span></div>'
  +'</div>';
 // chart
 var w=document.getElementById('bv_chartwrap');w.style.display='block';
 var c=document.getElementById('bv_chart'),x=c.getContext('2d');x.clearRect(0,0,c.width,c.height);
 var all=buyC.concat(rentC),mx=Math.max.apply(null,all)*1.05,mn=Math.min(0,Math.min.apply(null,all));
 var X=function(i){return 40+(c.width-60)*i/(N-1)},Y=function(v2){return c.height-24-(c.height-44)*(v2-mn)/(mx-mn)};
 x.strokeStyle='#E2DCD0';x.beginPath();x.moveTo(40,Y(0));x.lineTo(c.width-20,Y(0));x.stroke();
 x.fillStyle='#8B8272';x.font='11px Heebo';
 for(var yy=0;yy<N;yy+=Math.ceil(N/8)){x.fillText(''+(yy+1),X(yy)-4,c.height-8);}
 var draw=function(arr,col){x.strokeStyle=col;x.lineWidth=2.5;x.beginPath();arr.forEach(function(v2,i){i?x.lineTo(X(i),Y(v2)):x.moveTo(X(i),Y(v2))});x.stroke();};
 draw(buyC,'#9C7A3C');draw(rentC,'#C2563A');
 if(be){x.fillStyle='#5B7A52';x.beginPath();x.arc(X(be-1),Y(buyC[be-1]),5,0,7);x.fill();x.fillText('איזון',X(be-1)-14,Y(buyC[be-1])-10);}
 // sensitivity
 var s=document.getElementById('bv_sens');s.innerHTML='';
 [['אם עליית הערך תהיה '+((+bv_appr.value)-1)+'%',-0.01],['אם עליית הערך תהיה '+((+bv_appr.value)+1)+'%',0.01]].forEach(function(t){
   var val2=P,bal2=loan,port2=E+oneoff,rent2=R0;
   for(var y2=1;y2<=N;y2++){for(var m2=0;m2<12;m2++){var i3=bal2*mr;bal2-=Math.min(pay-i3,bal2);var d2=pay+up-rent2;port2=port2*Math.pow(1+inv,1/12)+(d2>0?d2:0);}val2*=1+g+t[1];rent2*=1+rg;}
   var g2=port2-(E+oneoff);var np2=port2-Math.max(0,g2)*0.25;var a2=val2*(1-sc)-bal2-np2;
   s.appendChild(Object.assign(document.createElement('span'),{textContent:t[0]+': '+(a2>0?'קנייה מובילה ב-':'שכירות מובילה ב-')+Math.round(Math.abs(a2)).toLocaleString('he-IL')+' ₪'}));
 });
}
</script>
<?php }
	if ( ! empty( $need['deal'] ) ) {
		$lead = function_exists( 'nadlan_calc_lead_js' ) ? nadlan_calc_lead_js( 'AI deal analysis' ) : 'function(){}';
		?>
<script>
var nlDealSend=<?php echo $lead; ?>;
function nlDealRun(){
 var P=+dc_price.value,S=+dc_sqm.value,R=+dc_rent.value,A=+dc_area.value,E=+dc_equity.value,I=+dc_income.value,
     r=+dc_rate.value/100/12,n=+dc_term.value*12;
 var psm=P/S, delta=(psm-A)/A;                       // price vs market
 var tax=nlPtaxCalc(P); var closing=P*0.015+tax;
 var loan=Math.max(0,P-E), pay=loan>0?loan*r/(1-Math.pow(1+r,-n)):0;
 var yieldG=R*12/P*100, dti=pay/Math.max(1,I)*100, ltv=loan/P*100;
 // scores 0..100
 var sPrice=Math.max(0,Math.min(100,50-delta*400));          // 12.5% over market -> 0
 var sYield=Math.max(0,Math.min(100,(yieldG-1.5)/(4.5-1.5)*100));
 var sDti=Math.max(0,Math.min(100,(40-dti)/(40-15)*100));
 var sLtv=Math.max(0,Math.min(100,(75-ltv)/40*100+40));
 var total=Math.round(sPrice*0.35+sYield*0.25+sDti*0.25+sLtv*0.15);
 var grade=total>=85?'A':total>=70?'B':total>=55?'C':total>=40?'D':'E';
 var box=document.getElementById('dc_score');box.style.display='flex';
 document.getElementById('dc_grade').textContent=grade;
 var nf=function(x){return Math.round(x).toLocaleString('he-IL')};
 var bars=[['מחיר מול השוק ('+nf(psm)+' ₪ למ"ר מול '+nf(A)+')',sPrice],
   ['תשואת שכירות ברוטו ('+yieldG.toFixed(1)+'%)',sYield],
   ['עומס החזר מההכנסה ('+dti.toFixed(0)+'%)',sDti],
   ['מינוף ('+ltv.toFixed(0)+'% מימון)',sLtv]];
 document.getElementById('dc_bars').innerHTML=bars.map(function(b){
   return '<div class="nlbvr-bar"><label><span>'+b[0]+'</span><span>'+Math.round(b[1])+'</span></label><div class="tr"><div class="fl" style="width:'+b[1]+'%"></div></div></div>';}).join('');
 var ch=document.getElementById('dc_checks');ch.style.display='block';
 var items=['עלות רכישה מלאה: כ-'+nf(P+closing)+' ₪ (כולל מס רכישה '+nf(tax)+' ₪ ועלויות נלוות).',
   'החזר חודשי משוער: '+nf(pay)+' ₪ ('+dti.toFixed(0)+'% מההכנסה. מעל 33% נחשב עומס גבוה).'];
 if(delta>0.07)items.push('המחיר גבוה בכ-'+(delta*100).toFixed(0)+'% מהממוצע שהזנתם לאזור: דרשו הצדקה (קומה, נוף, מפרט) או משא ומתן.');
 if(delta<-0.07)items.push('המחיר נמוך משמעותית מהשוק: בדקו רישום, שעבודים, מצב פיזי וליקויים נסתרים.');
 if(yieldG<2.5)items.push('התשואה נמוכה מפיקדונות חסרי סיכון: ההיגיון כאן הוא השבחה או מגורים, לא תזרים.');
 items.push('בדקו תב"ע סביב הנכס: מה ייבנה מול החלונות בחמש השנים הקרובות.');
 ch.innerHTML='<b>רשימת הבדיקות שלכם:</b><ul>'+items.map(function(i){return '<li>'+i+'</li>'}).join('')+'</ul>';
 document.getElementById('dc_ai').style.display='block';
}
function nlDealLead(){var nm=document.getElementById('dc_name').value,ph=document.getElementById('dc_phone').value;
 if(!ph){alert('נא להשאיר טלפון');return;}
 nlDealSend(nm,ph,'deal-check: price='+dc_price.value+' sqm='+dc_sqm.value+' rent='+dc_rent.value+' area='+dc_area.value);
 document.getElementById('dc_ai').innerHTML='✓ קיבלנו. ניתוח מלא יישלח אליכם בהקדם.';}
</script>
<?php }
}, 60 );
