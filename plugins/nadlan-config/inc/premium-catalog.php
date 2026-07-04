<?php
/**
 * nadlan-config - Premium project catalog (v1.71.6)
 *
 * [nadlan_premium_catalog]: the curated tier. Only projects that pass the full
 * experience gate appear here: complete article in 5 languages, selectable 3D,
 * facade, verified facts. Booking-style filters (facilities, rooms, delivery,
 * near sea) + recent-deals line per card + language links. This is both the
 * flagship UX and a monetization product (developers pay to be in the premium
 * tier). The big /projects/ catalog (900+) stays as the wide SEO net.
 *
 * JS prints in wp_footer (content filters corrupt inline scripts). No long dashes.
 */

if ( ! defined( 'ABSPATH' ) ) { exit; }

if ( ! function_exists( 'nadlan_premium_catalog_data' ) ) {
	function nadlan_premium_catalog_data() {
		/* Curated tier, verified figures from the canonical DB (data/projects/).
		   Filterable so future projects join without a code release. */
		return apply_filters( 'nadlan_premium_catalog_projects', array(
			array(
				'slug' => 'rainbow-tel-aviv', 'name' => 'Rainbow תל אביב', 'dev' => 'ישראל קנדה',
				'area' => 'רובע שדה דב, קו ראשון לחוף', 'floors' => 39, 'units' => 459, 'delivery' => '2027',
				'price_note' => 'ממוצע נמכרות: 80,300 ₪ למ"ר כולל מע"מ (דוח שנתי 2025)',
				'rooms' => array( 3, 4, 5 ), 'sea' => true,
				'fac' => array( 'לגונה ובריכות', 'ספא', 'חדר כושר', 'קולנוע', "קונסיירז'", 'מסחר', 'חניון', 'ממ"ד' ),
				'deal' => 'נמכרו 270 מתוך 459 (59%) עד סוף 2025, לפי דיווח רשמי',
			),
			array(
				'slug' => 'ashira-sde-dov', 'name' => 'ASHIRA שדה דב', 'dev' => 'אביסרור',
				'area' => 'רובע שדה דב, מול הים', 'floors' => 35, 'units' => 406, 'delivery' => '2028',
				'price_note' => 'אומדן אזור: כ-75,000 ₪ למ"ר (מדלן, לאימות מול היזם)',
				'rooms' => array( 2, 3, 4, 5 ), 'sea' => true,
				'fac' => array( 'בריכה', 'ספא', 'חדר כושר', 'קולנוע', "לאונג'", 'אזורי ילדים', 'חניון', 'ממ"ד' ),
				'deal' => '4 בניינים במדרוג 8/8/16/35 קומות, תכנון אבנר ישר',
			),
			array(
				'slug' => 'dimri-yama-sde-dov', 'name' => 'Dimri Yama שדה דב', 'dev' => 'י.ח דמרי',
				'area' => 'רובע שדה דב', 'floors' => 39, 'units' => 458, 'delivery' => '2028',
				'price_note' => 'טרם פורסם מחירון; עוגן אזורי: 80,300 ₪ למ"ר (Rainbow, דיווח רשמי)',
				'rooms' => array( 3, 4, 5 ), 'sea' => true,
				'fac' => array( 'בריכה', 'חדר כושר', 'לובי Kelly Hoppen', 'אזורי ילדים', 'חניון', 'ממ"ד' ),
				'deal' => 'עיצוב פנים בחתימת Kelly Hoppen CBE',
			),
		) );
	}
}

add_shortcode( 'nadlan_premium_catalog', function () {
	nadlan_bvr_mark_pc();
	$rows = nadlan_premium_catalog_data();
	$fkeys = array( 'בריכה', 'ספא', 'חדר כושר', 'קולנוע', "קונסיירז'", 'לגונה', "לאונג'", 'אזורי ילדים', 'מסחר', 'חניון', 'ממ"ד' );
	ob_start(); ?>
<style>
.nlpc{max-width:1060px;margin:10px auto;font-family:var(--font-sans,Heebo,sans-serif);direction:rtl;color:#1B1A17}
.nlpc .bar{display:flex;flex-wrap:wrap;gap:8px;margin:14px 0 6px;align-items:center}
.nlpc .lbl{font-size:11.5px;letter-spacing:.12em;color:#9C7A3C;font-weight:700;margin-inline-end:4px}
.nlpc .f,.nlpc .fr{background:#fff;border:1px solid #E2DCD0;border-radius:999px;padding:7px 15px;font:inherit;font-size:13.5px;cursor:pointer}
.nlpc .f.on,.nlpc .fr.on{background:#1B1A17;color:#fff;border-color:#1B1A17}
.nlpc .count{font-size:13px;color:#5C564D;margin:6px 0 14px}
.nlpc-card{display:grid;grid-template-columns:260px 1fr;background:#fff;border:1px solid #E2DCD0;border-radius:16px;overflow:hidden;margin-bottom:16px;box-shadow:0 14px 34px rgba(27,26,23,.06)}
.nlpc-card.hide{display:none}
.nlpc-media{background:#14130F center/cover no-repeat;min-height:210px;position:relative}
.nlpc-media em{position:absolute;bottom:10px;inset-inline-start:10px;font-style:normal;font-size:11px;background:rgba(20,19,15,.82);color:#E6D4AE;border-radius:6px;padding:4px 10px}
.nlpc-body{padding:18px 22px}
.nlpc-body h3{font-family:var(--font-serif,"Frank Ruhl Libre",serif);font-size:1.35rem;margin:0}
.nlpc-meta{font-size:13.5px;color:#5C564D;margin:3px 0 8px}
.nlpc-price{font-size:13px;color:#1B1A17;background:#F3EEE3;border-radius:8px;padding:6px 10px;display:inline-block}
.nlpc-fac{display:flex;flex-wrap:wrap;gap:6px;margin:10px 0}
.nlpc-fac span{font-size:12px;background:#FAF7F1;border:1px solid #E2DCD0;border-radius:999px;padding:4px 10px}
.nlpc-deal{font-size:12.5px;color:#5C564D;border-top:1px dashed #E2DCD0;padding-top:8px}
.nlpc-foot{display:flex;justify-content:space-between;align-items:center;margin-top:10px;flex-wrap:wrap;gap:8px}
.nlpc-langs{display:flex;gap:4px}
.nlpc-langs a{font-size:11px;border:1px solid #E2DCD0;border-radius:6px;padding:3px 7px;text-decoration:none;color:#5C564D}
.nlpc-go{color:#C2563A;font-weight:700;text-decoration:none;font-size:14.5px}
.nlpc-join{background:#14130F;color:#FAF7F1;border-radius:16px;padding:22px 26px;margin-top:8px}
.nlpc-join b{font-family:var(--font-serif,serif);font-size:1.2rem;color:#E6D4AE}
.nlpc-join p{font-size:13.5px;color:#CFC6B4;margin:6px 0 0}
@media(max-width:700px){.nlpc-card{grid-template-columns:1fr}}
</style>
<div class="nlpc" id="nlpc">
  <div class="bar"><span class="lbl">מתקנים</span>
  <?php foreach ( $fkeys as $i => $k ) : ?><button class="f" data-fi="<?php echo (int) $i; ?>"><?php echo esc_html( $k ); ?></button><?php endforeach; ?>
  </div>
  <div class="bar"><span class="lbl">חדרים</span>
    <button class="fr" data-r="3">3</button><button class="fr" data-r="4">4</button><button class="fr" data-r="5">5</button>
    <span class="lbl" style="margin-inline-start:12px">אכלוס</span>
    <button class="fr" data-d="2027">2027</button><button class="fr" data-d="2028">2028</button>
    <button class="fr" data-sea="1" style="margin-inline-start:12px">קרוב לים</button>
  </div>
  <div class="count" id="nlpc_count"></div>
  <?php foreach ( $rows as $p ) :
    $post = get_page_by_path( $p['slug'], OBJECT, 'nadlan_project' );
    if ( ! $post ) { continue; }
    $link   = get_permalink( $post );
    $poster = esc_url( (string) get_post_meta( $post->ID, 'project_model_poster', true ) );
    $fattrs = '';
    foreach ( $fkeys as $i => $k ) { foreach ( $p['fac'] as $f ) { if ( strpos( $f, $k ) !== false ) { $fattrs .= ' data-f' . $i . '="1"'; break; } } }
    $langs = array();
    foreach ( array( 'HE' => '', 'EN' => '-en', 'FR' => '-fr', 'RU' => '-ru', 'AR' => '-ar' ) as $ll => $suf ) {
      $sib = get_page_by_path( $p['slug'] . $suf, OBJECT, 'nadlan_project' );
      if ( $sib && 'publish' === get_post_status( $sib ) ) { $langs[ $ll ] = get_permalink( $sib ); }
    }
  ?>
  <article class="nlpc-card" data-rooms="<?php echo esc_attr( implode( ',', $p['rooms'] ) ); ?>" data-delivery="<?php echo esc_attr( $p['delivery'] ); ?>" data-sea="<?php echo $p['sea'] ? 1 : 0; ?>"<?php echo $fattrs; ?>>
    <div class="nlpc-media" style="background-image:url('<?php echo $poster; ?>')"><em>בחירת דירה בתלת ממד</em></div>
    <div class="nlpc-body">
      <h3><?php echo esc_html( $p['name'] ); ?></h3>
      <div class="nlpc-meta"><?php echo esc_html( $p['dev'] . ' · ' . $p['area'] . ' · ' . $p['floors'] . ' קומות · ' . $p['units'] . ' דירות · אכלוס ' . $p['delivery'] ); ?></div>
      <span class="nlpc-price"><?php echo esc_html( $p['price_note'] ); ?></span>
      <div class="nlpc-fac"><?php foreach ( $p['fac'] as $f ) { echo '<span>' . esc_html( $f ) . '</span>'; } ?></div>
      <div class="nlpc-deal"><?php echo esc_html( $p['deal'] ); ?></div>
      <div class="nlpc-foot">
        <a class="nlpc-go" href="<?php echo esc_url( $link ); ?>">לעמוד המלא: מודל, חזית, מאמר ומפה ←</a>
        <div class="nlpc-langs"><?php foreach ( $langs as $ll => $lu ) { echo '<a href="' . esc_url( $lu ) . '">' . esc_html( $ll ) . '</a>'; } ?></div>
      </div>
    </div>
  </article>
  <?php endforeach; ?>
  <div class="nlpc-join"><b>הפרויקט שלכם שייך לכאן?</b>
    <p>הקטלוג הפרימיום כולל רק פרויקטים עם חוויית בחירה מלאה: מודל תלת ממדי אינטראקטיבי, מאמר מקיף בחמש שפות, נתונים מאומתים ומפה חכמה. יזמים ומשווקים מוזמנים לפנות דרך <a href="/contact/" style="color:#E6D4AE">צור קשר</a>.</p>
  </div>
</div>
<?php return ob_get_clean();
} );

if ( ! function_exists( 'nadlan_bvr_mark_pc' ) ) {
	function nadlan_bvr_mark_pc() { static $on = false; $prev = $on; $on = true; return $prev; }
	function nadlan_pc_needed() { return nadlan_bvr_mark_pc() || false; }
}
add_action( 'wp_footer', function () {
	static $checked = false; if ( $checked ) { return; } $checked = true;
	/* only print if the shortcode ran on this request */
	if ( ! nadlan_bvr_mark_pc() ) { return; }
	?>
<script>
(function(){
var st={f:new Set(),r:new Set(),d:new Set(),sea:false};
function apply(){var n=0;
 document.querySelectorAll('.nlpc-card').forEach(function(c){var ok=true;
  st.f.forEach(function(i){if(!c.hasAttribute('data-f'+i))ok=false});
  if(st.r.size){var rs=c.dataset.rooms.split(',');var hit=false;st.r.forEach(function(r){if(rs.indexOf(r)>=0)hit=true});if(!hit)ok=false}
  if(st.d.size&&!st.d.has(c.dataset.delivery))ok=false;
  if(st.sea&&c.dataset.sea!=='1')ok=false;
  c.classList.toggle('hide',!ok);if(ok)n++;});
 var el=document.getElementById('nlpc_count');if(el)el.textContent=n+' פרויקטים מתאימים';}
document.querySelectorAll('#nlpc .f').forEach(function(b){b.onclick=function(){var i=b.dataset.fi;b.classList.toggle('on');b.classList.contains('on')?st.f.add(i):st.f['delete'](i);apply();};});
document.querySelectorAll('#nlpc .fr[data-r]').forEach(function(b){b.onclick=function(){b.classList.toggle('on');b.classList.contains('on')?st.r.add(b.dataset.r):st.r['delete'](b.dataset.r);apply();};});
document.querySelectorAll('#nlpc .fr[data-d]').forEach(function(b){b.onclick=function(){b.classList.toggle('on');b.classList.contains('on')?st.d.add(b.dataset.d):st.d['delete'](b.dataset.d);apply();};});
var sb=document.querySelector('#nlpc [data-sea]');if(sb)sb.onclick=function(){sb.classList.toggle('on');st.sea=sb.classList.contains('on');apply();};
apply();
})();
</script>
<?php }, 61 );
