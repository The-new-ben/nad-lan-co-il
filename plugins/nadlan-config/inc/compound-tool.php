<?php
/**
 * nadlan-config - COMPOUND TOOL (HAD-642, Ben 31.10.2026): the upgraded page of an urban-renewal compound from the government
 * registry, one compound at a time. Claude Design v105.2, component CompoundDecision.
 *
 * On an upgraded compound (nadlan_cv2_on):
 *  - the page opens with its title and an answer paragraph (the post's own "שורה תחתונה", lifted by ProjectTitle in
 *    inc/project-stage.php), then the tool;
 *  - [nadlan_compound_tool] renders the tool from the compound's own registry row and its city's registry numbers
 *    (data/renewal-stats.json): what an owner usually gets, how many signatures are missing for two thirds, five checks
 *    before buying, and the compound against its city;
 *  - the strips that do not belong to a compound in planning step aside in their own modules (milestones, feature bar,
 *    project experience, facts card), each with a one-line guard that calls nadlan_cv2_on();
 *  - the search title names the compound, its city and "פינוי בינוי".
 * Honesty: every number is the registry's or a source accepted in UrbanRenewalHonesty (the 2020 policy, the authority's
 * calculator, the statute's two thirds, the authority's 2025 report). Unknown values are omitted, never shown as 0.
 * Which compounds: the option nadlan_cv2_ids (default: הגפן 8-10, post 2415). Ben approves before any other compound.
 */
if ( ! defined( 'ABSPATH' ) ) { exit; }

if ( ! function_exists( 'nadlan_cv2_ids' ) ) {
	function nadlan_cv2_ids() {
		$ids = get_option( 'nadlan_cv2_ids', null );
		if ( ! is_array( $ids ) ) { $ids = array( 2415 ); }
		return array_map( 'intval', (array) apply_filters( 'nadlan_cv2_ids', $ids ) );
	}
}

if ( ! function_exists( 'nadlan_cv2_on' ) ) {
	/** true on the singular page of an upgraded compound (or for a given post id) */
	function nadlan_cv2_on( $id = 0 ) {
		$id = (int) $id;
		if ( ! $id ) {
			if ( is_admin() || ! is_singular( 'nadlan_project' ) ) { return false; }
			$id = (int) get_queried_object_id();
		}
		if ( ! $id || 'urban_renewal' !== (string) get_post_meta( $id, 'source', true ) ) { return false; }
		return in_array( $id, nadlan_cv2_ids(), true );
	}
}

if ( ! function_exists( 'nadlan_cv2_stats' ) ) {
	/** the registry file's numbers (built by tools from data.gov.il, the file of 15.8.2026) */
	function nadlan_cv2_stats() {
		static $s = null;
		if ( null !== $s ) { return $s; }
		$s  = array();
		$fn = dirname( __DIR__ ) . '/data/renewal-stats.json';
		if ( is_readable( $fn ) ) {
			$d = json_decode( (string) file_get_contents( $fn ), true );
			if ( is_array( $d ) && ! empty( $d['file'] ) ) { $s = $d['file']; }
		}
		return $s;
	}
}

if ( ! function_exists( 'nadlan_cv2_city' ) ) {
	/** the city's registry numbers, the median multiplier of its approved compounds and this compound's size rank */
	function nadlan_cv2_city( $city, $ex, $prop ) {
		$st  = nadlan_cv2_stats();
		$out = array();
		if ( ! $st || '' === $city ) { return $out; }
		$cities = (array) ( $st['cities'] ?? array() );
		usort( $cities, function ( $a, $b ) { return (int) ( $b['n'] ?? 0 ) <=> (int) ( $a['n'] ?? 0 ); } );
		foreach ( $cities as $i => $c ) {
			if ( (string) ( $c['city'] ?? '' ) === $city ) {
				$out = $c;
				$out['rank']  = $i + 1;
				$out['of']    = count( $cities );
				break;
			}
		}
		$mults = array();
		$sizes = array();
		foreach ( (array) ( $st['approved'] ?? array() ) as $a ) {
			if ( (string) ( $a['city'] ?? '' ) !== $city ) { continue; }
			$e = (int) ( $a['ex'] ?? 0 );
			$p = (int) ( $a['prop'] ?? 0 );
			if ( $e > 0 && $p > 0 ) { $mults[] = $p / $e; }
			if ( $p > 0 ) { $sizes[] = $p; }
		}
		if ( $mults ) {
			sort( $mults );
			$n = count( $mults );
			$out['med_mult'] = 0 === $n % 2 ? ( $mults[ $n / 2 - 1 ] + $mults[ $n / 2 ] ) / 2 : $mults[ intdiv( $n, 2 ) ];
			$out['approved_n'] = $n;
		}
		if ( $sizes && $prop > 0 ) {
			rsort( $sizes );
			$pos = array_search( $prop, $sizes, true );
			if ( false !== $pos ) { $out['size_rank'] = $pos + 1; $out['size_of'] = count( $sizes ); }
		}
		$ne = (int) ( $st['existing'] ?? 0 );
		$np = (int) ( $st['proposed'] ?? 0 );
		if ( $ne > 0 && $np > 0 ) { $out['nat_mult'] = $np / $ne; $out['nat_n'] = (int) ( $st['total'] ?? 0 ); }
		$out['file_date'] = (string) ( $st['last_modified'] ?? '' );
		return $out;
	}
}

if ( ! function_exists( 'nadlan_cv2_num' ) ) {
	function nadlan_cv2_num( $v, $dec = 0 ) {
		return '<span class="nlct-n">' . esc_html( number_format( (float) $v, $dec ) ) . '</span>';
	}
}

if ( ! function_exists( 'nadlan_cv2_tool' ) ) {
	function nadlan_cv2_tool( $id ) {
		$g      = function ( $k ) use ( $id ) { return trim( preg_replace( '/\s+/u', ' ', (string) get_post_meta( $id, $k, true ) ) ); };
		$city   = $g( 'city' );
		$status = $g( 'project_status' );
		$plan   = $g( 'plan_number' );
		$link   = $g( 'source_url' );
		$ex     = (int) $g( 'units_existing' );
		$prop   = (int) $g( 'num_units' );
		$add    = (int) $g( 'units_added' );
		$year   = (int) $g( 'completion_year' );
		$track  = $g( 'renewal_track' );
		if ( $ex <= 0 || $prop <= 0 ) { return ''; }
		$name   = trim( preg_replace( '/\s*,.*$/u', '', wp_strip_all_tags( html_entity_decode( get_the_title( $id ), ENT_QUOTES, 'UTF-8' ) ) ) );
		$approved = false !== mb_strpos( $status, 'מאושרת' );
		$cs     = nadlan_cv2_city( $city, $ex, $prop );
		$mult   = $prop / $ex;
		$need   = (int) ceil( 2 * $ex / 3 );
		$wa     = function_exists( 'nadlan_cta_whatsapp_number' ) ? nadlan_cta_whatsapp_number() : '';
		$msg    = 'שלום, אשמח לקבל עדכונים על מתחם הפינוי בינוי ' . $name . ( '' !== $city ? ' ב' . $city : '' ) . '.';
		$date   = '';
		if ( ! empty( $cs['file_date'] ) && preg_match( '/^(\d{4})-(\d{2})-(\d{2})/', $cs['file_date'], $m ) ) {
			$date = (int) $m[3] . '.' . (int) $m[2] . '.' . $m[1];
		}
		$tracks = array( 'misui' => 'מוכרז במסלול מיסוי', 'rashuyot' => 'מוכרז במסלול רשויות', 'terem_huchraz' => 'טרם הוכרז' );
		$nm     = '<span class="nlct-nm">' . esc_html( $name ) . '</span>';
		ob_start();
		?>
<section class="nlct" dir="rtl" id="nlct" aria-labelledby="nlct-h">
	<p class="nlct-kick"><?php echo esc_html( $name ); ?> · פינוי בינוי</p>
	<h2 id="nlct-h" class="nlct-h2">פינוי בינוי ב<?php echo $nm; ?>: מה זה אומר לכם</h2>
	<div class="nlct-cta">
		<?php if ( '' !== $wa ) : ?><a class="nlct-wa" data-nl-whatsapp href="https://wa.me/<?php echo esc_attr( $wa ); ?>?text=<?php echo rawurlencode( $msg ); ?>" target="_blank" rel="noopener">לקבלת עדכונים על המתחם בוואטסאפ</a><?php endif; ?>
		<a class="nlct-line" href="<?php echo esc_url( home_url( '/urban-renewal/check/' ) ); ?>">בדיקת מתחם: האם הבניין שלכם בפנים?</a>
	</div>
	<div class="nlct-tabs" role="tablist" aria-label="<?php echo esc_attr( 'מה מעניין אתכם ב' . $name ); ?>">
		<button type="button" class="nlct-tab" role="tab" id="nlct-ta" aria-controls="nlct-pa" aria-selected="true">יש לי דירה כאן</button>
		<button type="button" class="nlct-tab" role="tab" id="nlct-tb" aria-controls="nlct-pb" aria-selected="false" tabindex="-1">שוקלים לקנות</button>
		<button type="button" class="nlct-tab" role="tab" id="nlct-tc" aria-controls="nlct-pc" aria-selected="false" tabindex="-1">במספרים</button>
	</div>

	<div class="nlct-pane" id="nlct-pa" role="tabpanel" aria-labelledby="nlct-ta">
		<h3 class="nlct-h3">מחשבון: איזו דירה תקבלו ב<?php echo $nm; ?></h3>
		<label class="nlct-q" for="nlct-size">גודל הדירה שלכם היום</label>
		<div class="nlct-val"><b class="nlct-n" id="nlct-sz">65</b> מ״ר</div>
		<input type="range" min="35" max="140" step="1" value="65" id="nlct-size" class="nlct-range">
		<div class="nlct-scale"><span>35</span><span>140</span></div>
		<div class="nlct-out" aria-live="polite">
			<p class="nlct-k">בדרך כלל בפינוי בינוי</p>
			<p class="nlct-v">דירה חדשה של כ-<span class="nlct-n" id="nlct-lo">77</span> עד <span class="nlct-n" id="nlct-hi">90</span> מ״ר</p>
			<p class="nlct-s" id="nlct-note">ועוד מרפסת וחניה, ובדרך כלל גם מחסן. התוספת בפועל נקבעת בהסכם עם היזם.</p>
		</div>
		<p class="nlct-fine">הטווח: תוספת של 12 מ״ר ומרפסת לפי מדיניות 2020, עד תוספת של 25 מ״ר, ברירת המחדל במחשבון הרשות להתחדשות עירונית (טווח 0 עד 30).</p>

		<h3 class="nlct-h3">חתימות ב<?php echo $nm; ?>: כמה חסרות</h3>
		<p class="nlct-q" id="nlct-sigq">כמה דירות במתחם כבר חתמו?</p>
		<div class="nlct-step" role="group" aria-labelledby="nlct-sigq">
			<button type="button" class="nlct-sb" data-d="-1" aria-label="פחות">−</button>
			<output class="nlct-n" id="nlct-sig"><?php echo (int) floor( $ex * 0.4 ); ?></output>
			<button type="button" class="nlct-sb" data-d="1" aria-label="יותר">+</button>
		</div>
		<div class="nlct-bar" aria-hidden="true"><i id="nlct-fill"></i><b style="inset-inline-start:66.667%"></b></div>
		<div class="nlct-out" aria-live="polite">
			<p class="nlct-v nlct-v--s" id="nlct-need"></p>
			<p class="nlct-s"><?php echo nadlan_cv2_num( $need ); ?> מתוך <?php echo nadlan_cv2_num( $ex ); ?> הדירות במתחם הן שני שלישים. זה תנאי אחד מתוך שלושה: בכל בניין גם לפחות שלוש חמישיות מהדירות, ויותר ממחצית הרכוש המשותף.</p>
		</div>
		<?php if ( $approved ) : ?>
		<div class="nlct-time"><b class="nlct-n">4</b><span>שנים בממוצע מאישור התכנית ועד ההיתר הראשון, לפי דוח הרשות להתחדשות עירונית לשנת 2025 (28 מתחמים).</span></div>
		<?php endif; ?>
	</div>

	<div class="nlct-pane" id="nlct-pb" role="tabpanel" aria-labelledby="nlct-tb" hidden>
		<h3 class="nlct-h3">קונים דירה ב<?php echo $nm; ?>? חמש בדיקות לפני</h3>
		<ol class="nlct-checks">
			<li><span><b>מי היזם, והאם נחתם הסכם</b> עם בעלי הדירות. נציגות הבעלים במתחם יודעת.</span></li>
			<li><span><b>כמה חתמו.</b> שני שלישים מ-<?php echo nadlan_cv2_num( $ex ); ?> הדירות הם <?php echo nadlan_cv2_num( $need ); ?>.</span></li>
			<li><span><b>מה ההסכם נותן לדירה הזו</b>: גודל, קומה, חניה ומחסן.</span></li>
			<li><span><b>נסח טאבו</b>: הערות אזהרה לטובת היזם, ומשכנתאות.</span></li>
			<li><span><b>שמאי מקרקעין</b>: שווי הדירה היום, לפני שמסכמים מחיר.</span></li>
		</ol>
		<div class="nlct-links">
			<a href="<?php echo esc_url( home_url( '/apartment-purchase-cost-calculator/' ) ); ?>">כל העלויות שמסביב למחיר הדירה <span>←</span></a>
			<a href="<?php echo esc_url( home_url( '/urban-renewal/pinui-binui-tenant-guide/' ) ); ?>">מדריך פינוי בינוי לבעלי דירות <span>←</span></a>
			<?php if ( '' !== $city ) : ?><a href="<?php echo esc_url( home_url( '/professionals/?city=' . rawurlencode( $city ) ) ); ?>">עורכי דין מקרקעין ושמאים ב<?php echo esc_html( $city ); ?> <span>←</span></a><?php endif; ?>
		</div>
	</div>

	<div class="nlct-pane" id="nlct-pc" role="tabpanel" aria-labelledby="nlct-tc" hidden>
		<h3 class="nlct-h3"><?php echo $nm; ?> מול <?php echo esc_html( '' !== $city ? $city : 'העיר' ); ?></h3>
		<p class="nlct-q"><?php echo nadlan_cv2_num( $ex ); ?> דירות היום, <?php echo nadlan_cv2_num( $prop ); ?> בתכנית</p>
		<div class="nlct-grid" aria-hidden="true"><?php for ( $i = 0; $i < min( $prop, 260 ); $i++ ) { echo $i < $ex ? '<i class="f"></i>' : '<i></i>'; } ?></div>
		<div class="nlct-legend"><span class="f">דירות קיימות</span><span>דירות נוספות</span></div>
		<?php
		$rows = array( array( $name, $mult, true ) );
		if ( ! empty( $cs['med_mult'] ) ) { $rows[] = array( 'חציון ' . $city . '*', $cs['med_mult'], false ); }
		if ( ! empty( $cs['nat_mult'] ) ) { $rows[] = array( 'כל המאגר', $cs['nat_mult'], false ); }
		$max = max( array_map( function ( $r ) { return $r[1]; }, $rows ) );
		?>
		<p class="nlct-q">המכפיל: כמה דירות בתכנית על כל דירה קיימת</p>
		<div class="nlct-cmp">
			<?php foreach ( $rows as $r ) : ?>
			<div<?php echo $r[2] ? ' class="me"' : ''; ?>><span><?php echo esc_html( $r[0] ); ?></span><em style="width:<?php echo esc_attr( round( $r[1] / $max * 100 ) ); ?>%"></em><strong><?php echo nadlan_cv2_num( $r[1], 1 ); ?></strong></div>
			<?php endforeach; ?>
		</div>
		<?php if ( ! empty( $cs['med_mult'] ) ) : ?>
		<p class="nlct-fine">* <?php echo nadlan_cv2_num( (int) $cs['approved_n'] ); ?> המתחמים ב<?php echo esc_html( $city ); ?> עם תכנית מאושרת<?php echo ! empty( $cs['size_rank'] ) ? '. ' . $nm . ' הוא ה-' . (int) $cs['size_rank'] . ' בגודלו מתוכם' : ''; ?>.</p>
		<?php endif; ?>
		<?php if ( '' !== $plan ) : ?>
		<?php if ( '' !== $link && false !== strpos( $link, 'iplan.gov.il' ) ) : ?><a class="nlct-stamp" href="<?php echo esc_url( $link ); ?>" target="_blank" rel="noopener"><small>תכנית</small><b><?php echo esc_html( $plan ); ?></b></a>
		<?php else : ?><div class="nlct-stamp"><small>תכנית</small><b><?php echo esc_html( $plan ); ?></b></div><?php endif; ?>
		<?php endif; ?>
	</div>

	<h2 class="nlct-h2 nlct-h2--s"><?php echo $nm; ?> בנתונים</h2>
	<dl class="nlct-dl">
		<div><dt>סוג</dt><dd>פינוי בינוי</dd></div>
		<?php if ( '' !== $status ) : ?><div><dt>שלב</dt><dd><?php echo esc_html( $status ); ?></dd></div><?php endif; ?>
		<?php if ( isset( $tracks[ $track ] ) ) : ?><div><dt>מסלול</dt><dd><?php echo esc_html( $tracks[ $track ] ); ?></dd></div><?php endif; ?>
		<div><dt>דירות היום</dt><dd><?php echo nadlan_cv2_num( $ex ); ?></dd></div>
		<div><dt>דירות בתכנית</dt><dd><?php echo nadlan_cv2_num( $prop ); ?></dd></div>
		<?php if ( $add > 0 ) : ?><div><dt>דירות נוספות</dt><dd><?php echo nadlan_cv2_num( $add ); ?></dd></div><?php endif; ?>
		<div><dt>מכפיל</dt><dd><?php echo nadlan_cv2_num( $mult, 1 ); ?></dd></div>
		<?php if ( '' !== $plan ) : ?><div><dt>מספר תכנית</dt><dd><span class="nlct-n"><?php echo esc_html( $plan ); ?></span></dd></div><?php endif; ?>
		<?php if ( $approved && $year >= 1965 && $year <= (int) gmdate( 'Y' ) ) : ?><div><dt>שנת תוקף התכנית</dt><dd><span class="nlct-n"><?php echo (int) $year; ?></span></dd></div><?php endif; ?>
	</dl>
	<p class="nlct-src">לפי מאגר הרשות הממשלתית להתחדשות עירונית (data.gov.il)<?php echo '' !== $date ? ', עדכון הקובץ ' . esc_html( $date ) : ''; ?>.</p>

	<?php if ( ! empty( $cs['n'] ) ) : ?>
	<h2 class="nlct-h2 nlct-h2--s">התחדשות עירונית ב<?php echo esc_html( $city ); ?></h2>
	<div class="nlct-city">
		<div><b><?php echo nadlan_cv2_num( (int) $cs['n'] ); ?></b><span>מתחמים במאגר<?php echo ! empty( $cs['rank'] ) && (int) $cs['rank'] <= 10 ? ', המקום ה-' . (int) $cs['rank'] . ' בארץ' : ''; ?></span></div>
		<?php if ( ! empty( $cs['approved'] ) ) : ?><div><b><?php echo nadlan_cv2_num( (int) $cs['approved'] ); ?></b><span>עם תכנית מאושרת</span></div><?php endif; ?>
		<?php if ( ! empty( $cs['permits'] ) ) : ?><div><b><?php echo nadlan_cv2_num( (int) $cs['permits'] ); ?></b><span>דירות עם היתר</span></div><?php endif; ?>
		<?php if ( ! empty( $cs['tax'] ) ) : ?><div><b><?php echo nadlan_cv2_num( (int) $cs['tax'] ); ?></b><span>מוכרזים במסלול מיסוי</span></div><?php endif; ?>
	</div>
	<div class="nlct-links nlct-links--row">
		<a href="<?php echo esc_url( home_url( '/urban-renewal/pinui-binui/' ) ); ?>">פינוי בינוי: כל מה שצריך לדעת <span>←</span></a>
		<a href="<?php echo esc_url( home_url( '/urban-renewal/map/' ) ); ?>">מפת מתחמי ההתחדשות לפי עיר <span>←</span></a>
	</div>
	<?php endif; ?>
</section>
<script>
(function(){
	var r=document.getElementById('nlct');if(!r||r.getAttribute('data-on'))return;r.setAttribute('data-on','1');
	var tabs=[].slice.call(r.querySelectorAll('.nlct-tab'));
	function sel(t){tabs.forEach(function(x){var on=x===t;x.setAttribute('aria-selected',on?'true':'false');x.tabIndex=on?0:-1;document.getElementById(x.getAttribute('aria-controls')).hidden=!on;});}
	tabs.forEach(function(t,i){t.addEventListener('click',function(){sel(t);});t.addEventListener('keydown',function(e){var k=e.key,j=-1;if(k==='ArrowLeft')j=(i+1)%tabs.length;else if(k==='ArrowRight')j=(i-1+tabs.length)%tabs.length;if(j>-1){e.preventDefault();sel(tabs[j]);tabs[j].focus();}});});
	var s=document.getElementById('nlct-size');
	function up(){var v=+s.value;document.getElementById('nlct-sz').textContent=v;document.getElementById('nlct-lo').textContent=v+12;document.getElementById('nlct-hi').textContent=v+25;
		document.getElementById('nlct-note').textContent=(v<52?'בדירה מתחת ל-52 מ״ר המדיניות מאפשרת תוספת של עד 25 מ״ר. ':'')+'ועוד מרפסת וחניה, ובדרך כלל גם מחסן. התוספת בפועל נקבעת בהסכם עם היזם.';}
	s.addEventListener('input',up);up();
	var N=<?php echo (int) $ex; ?>,need=<?php echo (int) $need; ?>,o=document.getElementById('nlct-sig'),sig=+o.textContent;
	function sg(){o.textContent=sig;document.getElementById('nlct-fill').style.width=(sig/N*100)+'%';var m=need-sig;document.getElementById('nlct-need').textContent=m>0?('עוד '+m+(m===1?' דירה':' דירות')+' עד שני שלישים'):'מספר הדירות שחתמו מגיע לשני שלישים';}
	[].forEach.call(r.querySelectorAll('.nlct-sb'),function(b){b.addEventListener('click',function(){sig=Math.max(0,Math.min(N,sig+(+b.getAttribute('data-d'))));sg();});});
	sg();
})();
</script>
		<?php
		return (string) ob_get_clean();
	}
}

add_shortcode( 'nadlan_compound_tool', function () {
	$id = (int) get_the_ID();
	if ( ! $id || 'urban_renewal' !== (string) get_post_meta( $id, 'source', true ) ) { return ''; }
	return nadlan_cv2_tool( $id );
} );

/* the page's styles, only where the tool can render */
add_action( 'wp_head', function () {
	if ( ! nadlan_cv2_on() ) { return; }
	echo '<style id="nadlan-cv2-css">'
		. '.nlct{--ink:#14212b;--ink2:#3b4753;--mute:#6b7680;--line:#e3e1da;--sea:#2f6f86;--seah:#255c70;--deep:#1f4b5c;--sand:#eee9dd;--paper:#f7f6f2;--wa:#0f7a63;'
		. 'font-family:Assistant,Heebo,"Segoe UI",Arial,sans-serif;color:var(--ink);background:#fff;border:1px solid var(--line);border-radius:22px;padding:18px;margin:6px 0 26px;display:grid;gap:14px;max-width:760px}'
		. '.nlct .nlct-n{direction:ltr;unicode-bidi:isolate;font-variant-numeric:tabular-nums}'
		. '.nlct .nlct-kick{margin:0;font:700 12.5px/1.3 Assistant,Heebo,sans-serif;letter-spacing:.02em;color:var(--sea)}'
		. 'html body .nlct h2.nlct-h2{margin:0;font:600 clamp(20px,4.6vw,24px)/1.25 "Noto Serif Hebrew","Frank Ruhl Libre",Georgia,serif!important;color:var(--ink)!important;text-wrap:balance}'
		. 'html body .nlct h2.nlct-h2--s{font-size:19px!important;margin-top:8px}'
		. 'html body .nlct h3.nlct-h3{margin:4px 0 0;font:600 17px/1.3 "Noto Serif Hebrew","Frank Ruhl Libre",Georgia,serif!important;color:var(--ink)!important}'
		. '.nlct .nlct-cta{display:grid;gap:8px}'
		. 'html body .nlct a.nlct-wa{display:flex;align-items:center;justify-content:center;min-height:48px;border-radius:999px;background:var(--wa);color:#fff!important;font:700 15.5px/1.2 Assistant,Heebo,sans-serif;text-decoration:none!important;box-shadow:0 10px 24px rgba(15,122,99,.30);padding:0 16px;text-align:center}'
		. 'html body .nlct a.nlct-line{display:flex;align-items:center;justify-content:center;min-height:46px;border-radius:999px;border:1px solid var(--line);background:#fff;color:var(--ink)!important;font:700 14.5px/1.2 Assistant,Heebo,sans-serif;text-decoration:none!important;padding:0 14px;text-align:center}'
		. '.nlct .nlct-tabs{display:grid;grid-template-columns:repeat(3,1fr);gap:4px;padding:4px;border-radius:999px;background:var(--sand)}'
		. '.nlct .nlct-tab{min-height:42px;border:0;border-radius:999px;background:transparent;font:700 14px/1.15 Assistant,Heebo,sans-serif;color:var(--ink2);cursor:pointer;padding:0 6px}'
		. '.nlct .nlct-tab[aria-selected=true]{background:#fff;color:var(--ink);box-shadow:0 1px 2px rgba(20,33,43,.08)}'
		. '.nlct .nlct-tab:focus-visible,.nlct .nlct-sb:focus-visible,.nlct .nlct-range:focus-visible{outline:2px solid var(--sea);outline-offset:3px}'
		. '.nlct .nlct-pane{display:grid;gap:12px}.nlct .nlct-pane[hidden]{display:none}'
		. '.nlct .nlct-q{display:block;margin:0;font:700 14.5px/1.4 Assistant,Heebo,sans-serif;color:var(--ink)}'
		. '.nlct .nlct-val{font:600 15px/1 Assistant,Heebo,sans-serif;color:var(--ink2)}.nlct .nlct-val b{font:600 28px/1 "Noto Serif Hebrew",Georgia,serif;color:var(--ink)}'
		. '.nlct .nlct-range{width:100%;height:30px;accent-color:var(--sea);margin:0}'
		. '.nlct .nlct-scale{display:flex;justify-content:space-between;font-size:12px;color:var(--mute);margin-top:-6px}'
		. '.nlct .nlct-out{border:1.5px dashed var(--sea);border-radius:16px;padding:14px;display:grid;gap:6px;background:var(--paper)}'
		. '.nlct .nlct-k{margin:0;font:700 12.5px/1.3 Assistant,Heebo,sans-serif;color:var(--sea)}'
		. '.nlct .nlct-v{margin:0;font:600 22px/1.25 "Noto Serif Hebrew",Georgia,serif;color:var(--ink)}.nlct .nlct-v--s{font-size:20px}'
		. '.nlct .nlct-s{margin:0;font-size:14px;line-height:1.55;color:var(--ink2)}'
		. '.nlct .nlct-fine{margin:0;font-size:12.5px;line-height:1.55;color:var(--ink2)}'
		. '.nlct .nlct-step{display:grid;grid-template-columns:52px 1fr 52px;align-items:center;gap:8px}'
		. '.nlct .nlct-sb{height:50px;border-radius:14px;border:1px solid var(--line);background:#fff;font:600 24px/1 Assistant,sans-serif;color:var(--ink);cursor:pointer;touch-action:manipulation}'
		. '.nlct .nlct-step output{text-align:center;font:600 30px/1 "Noto Serif Hebrew",Georgia,serif}'
		. '.nlct .nlct-bar{height:12px;border-radius:999px;background:var(--sand);position:relative;overflow:hidden}'
		. '.nlct .nlct-bar i{position:absolute;inset-block:0;inset-inline-start:0;width:0;background:var(--sea);border-radius:999px;transition:width .25s}'
		. '.nlct .nlct-bar b{position:absolute;inset-block:-3px;width:2px;background:var(--ink)}'
		. '.nlct .nlct-time{display:flex;gap:12px;align-items:center;padding:12px 14px;border-radius:14px;background:var(--sand)}'
		. '.nlct .nlct-time b{flex:none;font:600 32px/1 "Noto Serif Hebrew",Georgia,serif}.nlct .nlct-time span{font-size:13.5px;line-height:1.5;color:var(--ink2)}'
		. '.nlct .nlct-checks{margin:0;padding:0;list-style:none;display:grid;gap:8px;counter-reset:c}'
		. '.nlct .nlct-checks li{counter-increment:c;display:grid;grid-template-columns:28px 1fr;gap:10px;align-items:start;padding:10px 12px;border:1px solid var(--line);border-radius:14px;background:#fff;font-size:14.5px;line-height:1.5;color:var(--ink2)}'
		. '.nlct .nlct-checks li::before{content:counter(c);display:grid;place-items:center;width:28px;height:28px;border-radius:50%;background:var(--sea);color:#fff;font:700 13px/1 Assistant,sans-serif}'
		. '.nlct .nlct-checks b{color:var(--ink)}'
		. '.nlct .nlct-links{display:grid;gap:6px}.nlct .nlct-links--row{grid-template-columns:repeat(auto-fit,minmax(220px,1fr))}'
		. 'html body .nlct .nlct-links a{display:flex;justify-content:space-between;align-items:center;gap:10px;min-height:46px;padding:0 14px;border:1px solid var(--line);border-radius:14px;background:#fff;color:var(--ink)!important;text-decoration:none!important;font:600 14.5px/1.3 Assistant,Heebo,sans-serif}'
		. 'html body .nlct .nlct-links a span{color:var(--sea)}'
		. '.nlct .nlct-grid{display:grid;grid-template-columns:repeat(13,1fr);gap:3px;max-width:420px}'
		. '.nlct .nlct-grid i{aspect-ratio:1;border-radius:3px;border:1.5px solid var(--sea)}.nlct .nlct-grid i.f{background:var(--sea)}'
		. '.nlct .nlct-legend{display:flex;gap:14px;flex-wrap:wrap;font-size:12.5px;color:var(--ink2)}'
		. '.nlct .nlct-legend span::before{content:"";display:inline-block;width:10px;height:10px;border-radius:2px;border:1.5px solid var(--sea);margin-inline-end:6px;vertical-align:-1px}.nlct .nlct-legend span.f::before{background:var(--sea)}'
		. '.nlct .nlct-cmp{display:grid;gap:8px}.nlct .nlct-cmp div{display:grid;grid-template-columns:minmax(96px,130px) 1fr 40px;gap:8px;align-items:center;font-size:13.5px;color:var(--ink2)}'
		. '.nlct .nlct-cmp em{font-style:normal;height:10px;border-radius:999px;background:#7fa7b5}.nlct .nlct-cmp div.me em{background:var(--sea)}.nlct .nlct-cmp div.me{color:var(--ink);font-weight:700}'
		. '.nlct .nlct-cmp strong{font:600 16px/1 "Noto Serif Hebrew",Georgia,serif;color:var(--ink);text-align:end}'
		. 'html body .nlct .nlct-stamp{justify-self:start;display:grid;gap:2px;padding:10px 14px;border:1.5px dashed var(--sea);border-radius:10px;transform:rotate(-1.2deg);text-decoration:none!important;color:var(--ink)!important}'
		. '.nlct .nlct-stamp small{font:700 11.5px/1.2 Assistant,sans-serif;letter-spacing:.06em;color:var(--sea)}.nlct .nlct-stamp b{font:600 17px/1.2 ui-monospace,Consolas,monospace;direction:ltr;text-align:right}'
		. '.nlct .nlct-dl{margin:0;display:grid;border:1px solid var(--line);border-radius:14px;overflow:hidden;background:#fff}'
		. '.nlct .nlct-dl>div{display:grid;grid-template-columns:44% 1fr;border-bottom:1px solid var(--line)}.nlct .nlct-dl>div:last-child{border-bottom:0}'
		. 'html body .nlct .nlct-dl dt,html body .nlct .nlct-dl dd{margin:0!important;padding:9px 12px!important;font-size:14.5px!important;line-height:1.45!important}'
		. 'html body .nlct .nlct-dl dt{font-weight:600!important;color:var(--ink2)!important}html body .nlct .nlct-dl dd{font-weight:700!important;color:var(--ink)!important}'
		. '.nlct .nlct-src{margin:0;font-size:12.5px;line-height:1.55;color:var(--ink2)}'
		. '.nlct .nlct-city{display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));gap:8px}'
		. '.nlct .nlct-city div{background:var(--paper);border:1px solid var(--line);border-radius:14px;padding:10px 12px}'
		. '.nlct .nlct-city b{display:block;font:600 22px/1.2 "Noto Serif Hebrew",Georgia,serif;color:var(--ink)}.nlct .nlct-city div>span{font-size:13px;color:var(--ink2)}'
		. 'html body .nlct h2.nlct-h2,html body .nlct h3.nlct-h3{border:0!important;padding:0!important;margin:0!important;text-align:start!important;letter-spacing:0!important}'
		. 'html body .nlct h2.nlct-h2::before,html body .nlct h2.nlct-h2::after,html body .nlct h3.nlct-h3::before,html body .nlct h3.nlct-h3::after{content:none!important;display:none!important}'
		. 'html body .nlct h2.nlct-h2{font-size:clamp(20px,4.6vw,24px)!important;line-height:1.25!important}html body .nlct h2.nlct-h2--s{font-size:19px!important;margin-top:8px!important}html body .nlct h3.nlct-h3{font-size:17px!important;margin-top:4px!important}'
		. 'html body .nlct p{margin:0!important}html body .nlct p.nlct-kick{color:var(--sea)!important}.nlct .nlct-nm{white-space:nowrap;unicode-bidi:isolate}'
		. 'html body .nlct .nlct-city b{display:block!important;font:600 22px/1.2 "Noto Serif Hebrew",Georgia,serif!important;color:var(--ink)!important}html body .nlct .nlct-val b{font:600 28px/1 "Noto Serif Hebrew",Georgia,serif!important}html body .nlct .nlct-time b{font:600 32px/1 "Noto Serif Hebrew",Georgia,serif!important}'
		. 'html body .nlct ol.nlct-checks{margin:0!important;padding:0!important}html body .nlct ol.nlct-checks li{margin:0!important}'
		. 'html body .nlct p.nlct-v{font:600 22px/1.25 "Noto Serif Hebrew",Georgia,serif!important;color:var(--ink)!important}html body .nlct p.nlct-v--s{font-size:20px!important}'
		. 'html body .nlct p.nlct-k{font:700 12.5px/1.3 Assistant,Heebo,sans-serif!important;color:var(--sea)!important}html body .nlct p.nlct-s{font-size:14px!important;line-height:1.55!important;color:var(--ink2)!important}'
		. 'html body .nlct p.nlct-fine,html body .nlct p.nlct-src{font-size:12.5px!important;line-height:1.55!important;color:var(--ink2)!important}html body .nlct p.nlct-q,html body .nlct label.nlct-q{font:700 14.5px/1.4 Assistant,Heebo,sans-serif!important;color:var(--ink)!important}'
		. 'html body .nlct .nlct-city b .nlct-n,html body .nlct .nlct-v .nlct-n{font:inherit!important}'
		. '@media(max-width:520px){.nlct{padding:14px;border-radius:18px}.nlct .nlct-tab{font-size:13.5px}}'
		. '@media(prefers-reduced-motion:reduce){.nlct .nlct-bar i{transition:none}}'
		. '</style>';
}, 30 );

/* the search title and description of an upgraded compound: its name, its city and "פינוי בינוי" (after bulk-project-seo) */
if ( ! function_exists( 'nadlan_cv2_title' ) ) {
	function nadlan_cv2_title( $title ) {
		if ( ! nadlan_cv2_on() ) { return $title; }
		$id    = (int) get_queried_object_id();
		$name  = trim( wp_strip_all_tags( html_entity_decode( get_the_title( $id ), ENT_QUOTES, 'UTF-8' ) ) );
		$units = (int) get_post_meta( $id, 'num_units', true );
		if ( false === mb_strpos( $name, 'פינוי בינוי' ) ) { $name .= ': פינוי בינוי'; }
		return $name . ( $units > 0 ? ', ' . number_format( $units ) . ' דירות בתכנית' : '' ) . ' | נדל״ן';
	}
}
add_filter( 'wpseo_title', 'nadlan_cv2_title', 50 );
add_filter( 'pre_get_document_title', 'nadlan_cv2_title', 50 );
add_filter( 'wpseo_opengraph_title', 'nadlan_cv2_title', 50 );
if ( ! function_exists( 'nadlan_cv2_desc' ) ) {
	function nadlan_cv2_desc( $desc ) {
		if ( ! nadlan_cv2_on() ) { return $desc; }
		$id   = (int) get_queried_object_id();
		$name = trim( preg_replace( '/\s*,.*$/u', '', wp_strip_all_tags( html_entity_decode( get_the_title( $id ), ENT_QUOTES, 'UTF-8' ) ) ) );
		$city = trim( (string) get_post_meta( $id, 'city', true ) );
		$ex   = (int) get_post_meta( $id, 'units_existing', true );
		$prop = (int) get_post_meta( $id, 'num_units', true );
		$plan = trim( (string) get_post_meta( $id, 'plan_number', true ) );
		$st   = trim( preg_replace( '/\s+/u', ' ', (string) get_post_meta( $id, 'project_status', true ) ) );
		$d = 'מתחם פינוי בינוי ' . $name . ( '' !== $city ? ' ב' . $city : '' ) . ':';
		$d .= '' !== $plan ? ' תכנית ' . $plan . ( '' !== $st ? ' (' . $st . ')' : '' ) . ',' : '';
		$d .= ( $ex > 0 && $prop > 0 ) ? ' ' . number_format( $ex ) . ' דירות היום ו-' . number_format( $prop ) . ' בתכנית.' : '';
		return trim( $d ) . ' כמה מקבלים, כמה חתימות חסרות ומה לבדוק לפני קנייה.';
	}
}
add_filter( 'wpseo_metadesc', 'nadlan_cv2_desc', 99 );
add_filter( 'wpseo_opengraph_desc', 'nadlan_cv2_desc', 99 );

/* the scheduler's per-project switch is readable and writable through REST (so the compound's video call can be turned
   off the documented way, nadlan_sched_off = 1, by an authenticated editor) */
add_action( 'init', function () {
	register_post_meta( 'nadlan_project', 'nadlan_sched_off', array(
		'show_in_rest'  => true,
		'single'        => true,
		'type'          => 'string',
		'auth_callback' => function ( $allowed, $meta_key, $post_id ) { return current_user_can( 'edit_post', (int) $post_id ); },
	) );
}, 20 );
