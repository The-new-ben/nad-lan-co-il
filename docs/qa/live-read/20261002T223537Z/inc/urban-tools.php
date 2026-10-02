<?php
/**
 * nadlan-config - URBAN RENEWAL TOOLS (L2, 2026-07-11).
 *
 * Pillar-embedded decision tools, calculators.php discipline: client-side
 * widgets, filterable legal constants WITH effective dates + a gov.il verify
 * link, YMYL disclaimers on every output, no em/en dashes.
 *
 *  [nadlan_ur_consent_calc]  apartments + consents -> live % vs the three
 *                            legal thresholds, what unlocks at each
 *  [nadlan_ur_expectations]  honest non-binding "what owners usually get"
 *  [nadlan_ur_timeline]      the 10-stage strip (labels shared with L4)
 */

if ( ! defined( 'ABSPATH' ) ) { exit; }

if ( ! function_exists( 'nadlan_ur_thresholds' ) ) {
	function nadlan_ur_thresholds() {
		return apply_filters( 'nadlan_ur_thresholds', array(
			'effective' => '2024',
			'source'    => 'https://www.gov.il/he/departments/government_authority_for_urban_renewal',
			// קידום מתחם פינוי בינוי (חוק ההסדרים 2023)
			'pinui_binui_advance'    => 0.66,
			// תביעת דייר סרבן (בתוקף מ-2024, ירד מ-80%)
			'sue_refuser'            => 0.67,
			// רוב מיוחס בבניין בודד - דירות ורכוש משותף
			'single_building_units'  => 0.80,
			'single_building_common' => 0.75,
		) );
	}
}

if ( ! function_exists( 'nadlan_ur_ladder_labels' ) ) {
	/** The renewal stage ladder - shared by the L2 strip and the L4 space. */
	function nadlan_ur_ladder_labels() {
		return apply_filters( 'nadlan_ur_ladder_labels', array(
			'התארגנות ראשונית', 'בחירת נציגות', 'החתמות', 'בחירת אנשי מקצוע',
			'בחירת יזם', 'תב"ע ותכנון', 'היתר בנייה', 'פינוי', 'בנייה', 'מסירה ורישום',
		) );
	}
}

if ( ! function_exists( 'nadlan_ur_expectation_rows' ) ) {
	function nadlan_ur_expectation_rows() {
		return apply_filters( 'nadlan_ur_expectation_rows', array(
			array( 'דירה חדשה עם תוספת שטח', 'בהריסה ובנייה מקובל לראות תוספת של 12 עד 25 מ"ר לדירה, תלוי עסקה ועיר' ),
			array( 'ממ"ד', 'חדר ממוגן תקני, בדרך כלל כלול בתוספת השטח' ),
			array( 'מרפסת שמש', 'סדר גודל של 10 עד 12 מ"ר במרבית הפרויקטים החדשים' ),
			array( 'חניה ומחסן', 'תלוי תכנון ועיר; בפרויקטים חדשים לרוב חניה אחת לדירה' ),
			array( 'שכירות בתקופת הבנייה', 'מימון מלא על ידי היזם, בגובה שנקבע בהסכם עם מנגנון עדכון' ),
			array( 'בטוחות', 'ערבות חוק מכר, ערבות שכירות, ערבות בדק וערבות רישום' ),
		) );
	}
}

if ( ! function_exists( 'nadlan_ur_disclaimer' ) ) {
	function nadlan_ur_disclaimer() {
		$t = nadlan_ur_thresholds();
		return '<p class="nlur-disc">הנתונים אינם ייעוץ משפטי ואינם התחייבות. הרפים לפי הדין העדכני לשנת ' . esc_html( $t['effective'] ) .
			' ועשויים להשתנות; הרף המחייב נקבע לפי החוק ונסיבות הבניין. <a href="' . esc_url( $t['source'] ) . '" rel="nofollow noopener" target="_blank">אימות מול הרשות הממשלתית</a>. לפני כל צעד התייעצו עם עורך דין מטעם הדיירים.</p>';
	}
}

if ( ! function_exists( 'nadlan_ur_tools_css' ) ) {
	function nadlan_ur_tools_css() {
		static $done = false;
		if ( $done ) { return ''; }
		$done = true;
		return '<style>
.nlur-tool{background:#FFFFFF;border:1px solid #E2DCD0;border-radius:16px;padding:22px;margin:26px 0}
.nlur-tool h3{font-family:"Frank Ruhl Libre",Georgia,serif;color:#1B1A17;margin:0 0 4px;font-size:1.25rem}
.nlur-tool .s{color:#6D665C;font:400 13.5px/1.5 Heebo,sans-serif;margin:0 0 14px}
.nlur-cc__f{display:flex;gap:10px;flex-wrap:wrap;margin-bottom:14px}
.nlur-cc__f label{display:flex;flex-direction:column;gap:5px;font:600 12.5px Heebo,sans-serif;color:#51483A;flex:1;min-width:130px}
.nlur-cc__f input{border:1px solid #E2DCD0;border-radius:10px;padding:12px 14px;font:600 16px Heebo,sans-serif;background:#FAF7F1;width:100%}
.nlur-cc__pct{font-family:"Frank Ruhl Libre",Georgia,serif;font-size:2rem;color:#1B1A17;margin:4px 0 12px}
.nlur-bar{margin:10px 0}
.nlur-bar__t{display:flex;justify-content:space-between;font:600 13px Heebo,sans-serif;color:#3A352C;margin-bottom:5px}
.nlur-bar__t i{font-style:normal;color:#6D665C;font-weight:400}
.nlur-bar__w{height:10px;background:#F3EEE3;border-radius:999px;position:relative;overflow:hidden}
.nlur-bar__f{position:absolute;inset-block:0;inset-inline-start:0;background:#A79E8D;border-radius:999px;transition:width .4s ease,background .3s}
.nlur-bar.is-past .nlur-bar__f{background:#517048}
.nlur-bar__m{position:absolute;inset-block:-3px;width:2px;background:#1B1A17;opacity:.5}
.nlur-bar__note{font:400 12px/1.5 Heebo,sans-serif;color:#6D665C;margin-top:4px}
.nlur-bar.is-past .nlur-bar__note{color:#517048;font-weight:600}
.nlur-disc{font:400 11.5px/1.6 Heebo,sans-serif;color:#8E877A;border-top:1px solid #F3EEE3;padding-top:10px;margin:14px 0 0}
.nlur-exp{width:100%;border-collapse:collapse}
.nlur-exp td{border-bottom:1px solid #F3EEE3;padding:10px 6px;font:400 14px/1.55 Heebo,sans-serif;color:#3A352C;vertical-align:top}
.nlur-exp td:first-child{font-weight:700;color:#1B1A17;white-space:nowrap;padding-inline-end:14px}
.nlur-tl{display:flex;gap:4px;overflow-x:auto;padding:6px 0;counter-reset:nlurtl}
.nlur-tl span{flex:1;min-width:86px;text-align:center;font:600 11.5px/1.35 Heebo,sans-serif;color:#51483A;background:#F3EEE3;border:1px solid #E2DCD0;border-radius:10px;padding:10px 6px;position:relative;counter-increment:nlurtl}
.nlur-tl span::before{content:counter(nlurtl);display:block;font-family:"Frank Ruhl Libre",Georgia,serif;font-size:1rem;color:#9C7A3C;margin-bottom:2px}
@media(max-width:700px){.nlur-cc__f{flex-direction:column}}
</style>';
	}
}

add_shortcode( 'nadlan_ur_consent_calc', function () {
	$t = nadlan_ur_thresholds();
	ob_start();
	echo nadlan_ur_tools_css(); // phpcs:ignore WordPress.Security.EscapeOutput
	?>
<div class="nlur-tool nlur-cc" dir="rtl"
	data-adv="<?php echo esc_attr( $t['pinui_binui_advance'] ); ?>"
	data-sue="<?php echo esc_attr( $t['sue_refuser'] ); ?>"
	data-single="<?php echo esc_attr( $t['single_building_units'] ); ?>">
	<h3>מחשבון הסכמות: איפה הבניין שלכם עומד</h3>
	<p class="s">הזינו את מספר הדירות בבניין או במתחם ואת מספר בעלי הדירות שכבר הסכימו, וראו מה נפתח בכל רף לפי הדין העדכני.</p>
	<div class="nlur-cc__f">
		<label>סך הדירות<input type="number" id="nlur-cc-total" min="2" max="2000" inputmode="numeric" placeholder="לדוגמה: 24"></label>
		<label>מתוכן הסכימו<input type="number" id="nlur-cc-yes" min="0" max="2000" inputmode="numeric" placeholder="לדוגמה: 15"></label>
	</div>
	<div class="nlur-cc__pct" id="nlur-cc-pct" aria-live="polite">-</div>
	<div class="nlur-bar" data-th="adv">
		<div class="nlur-bar__t"><span>קידום מתחם פינוי בינוי</span><i>רף 66%</i></div>
		<div class="nlur-bar__w"><div class="nlur-bar__f"></div><div class="nlur-bar__m" style="inset-inline-start:66%"></div></div>
		<div class="nlur-bar__note" data-open="אפשר לקדם הכרזה והליכים סטטוטוריים במתחם" data-closed="עוד {n} בעלי דירות עד הרף"></div>
	</div>
	<div class="nlur-bar" data-th="sue">
		<div class="nlur-bar__t"><span>תביעת דייר סרבן</span><i>רף 67%</i></div>
		<div class="nlur-bar__w"><div class="nlur-bar__f"></div><div class="nlur-bar__m" style="inset-inline-start:67%"></div></div>
		<div class="nlur-bar__note" data-open="אפשר לפנות להליך משפטי נגד סירוב בלתי סביר" data-closed="עוד {n} בעלי דירות עד הרף"></div>
	</div>
	<div class="nlur-bar" data-th="single">
		<div class="nlur-bar__t"><span>רוב מיוחס בבניין בודד</span><i>רף 80% מהדירות (וגם 75% מהרכוש המשותף)</i></div>
		<div class="nlur-bar__w"><div class="nlur-bar__f"></div><div class="nlur-bar__m" style="inset-inline-start:80%"></div></div>
		<div class="nlur-bar__note" data-open="רף הדירות הושג; יש לוודא גם 75% מהרכוש המשותף מול נסחי הטאבו" data-closed="עוד {n} בעלי דירות עד הרף"></div>
	</div>
	<?php echo nadlan_ur_disclaimer(); // phpcs:ignore WordPress.Security.EscapeOutput ?>
</div>
<script>
(function(){
	var box=document.querySelector(".nlur-cc");if(!box||box.dataset.nlurWired)return;box.dataset.nlurWired="1";
	var ths={adv:parseFloat(box.dataset.adv),sue:parseFloat(box.dataset.sue),single:parseFloat(box.dataset.single)};
	function calc(){
		var total=parseInt(document.getElementById("nlur-cc-total").value,10)||0;
		var yes=parseInt(document.getElementById("nlur-cc-yes").value,10)||0;
		if(yes>total)yes=total;
		var pct=total>0?yes/total:0;
		document.getElementById("nlur-cc-pct").textContent=total>0?(Math.round(pct*1000)/10)+"% ("+yes+" מתוך "+total+")":"-";
		box.querySelectorAll(".nlur-bar").forEach(function(b){
			var th=ths[b.dataset.th],f=b.querySelector(".nlur-bar__f"),n=b.querySelector(".nlur-bar__note");
			f.style.width=Math.min(100,pct*100)+"%";
			var past=total>0&&pct>=th;
			b.classList.toggle("is-past",past);
			if(total>0){
				if(past){n.textContent=n.dataset.open}
				else{var need=Math.ceil(th*total)-yes;n.textContent=n.dataset.closed.replace("{n}",need)}
			}else{n.textContent=""}
		});
	}
	["nlur-cc-total","nlur-cc-yes"].forEach(function(id){document.getElementById(id).addEventListener("input",calc)});
})();
</script>
	<?php
	return ob_get_clean();
} );

add_shortcode( 'nadlan_ur_expectations', function () {
	$rows = nadlan_ur_expectation_rows();
	$html = nadlan_ur_tools_css();
	$html .= '<div class="nlur-tool" dir="rtl"><h3>מה מקובל לראות בעסקאות: טווחי ציפיות</h3><p class="s">טווחים מקובלים בפרויקטים של הריסה ובנייה באזורי ביקוש. אלה אינם הבטחה: כל עסקה תלויה בעיר, במגרש ובכדאיות, והמספרים שלכם ייקבעו בשמאות ובמשא ומתן.</p><table class="nlur-exp">';
	foreach ( $rows as $r ) {
		$html .= '<tr><td>' . esc_html( $r[0] ) . '</td><td>' . esc_html( $r[1] ) . '</td></tr>';
	}
	$html .= '</table>' . nadlan_ur_disclaimer() . '</div>';
	return $html;
} );

add_shortcode( 'nadlan_ur_timeline', function () {
	$html = nadlan_ur_tools_css();
	$html .= '<div class="nlur-tool" dir="rtl"><h3>עשרת השלבים על ציר אחד</h3><p class="s">הממוצע הארצי מהתארגנות עד מפתח מתקרב לעשור. השלב התכנוני הוא המשתנה הגדול בין פרויקט מהיר לאיטי.</p><div class="nlur-tl">';
	foreach ( nadlan_ur_ladder_labels() as $l ) {
		$html .= '<span>' . esc_html( $l ) . '</span>';
	}
	$html .= '</div>' . nadlan_ur_disclaimer() . '</div>';
	return $html;
} );

/* healthcheck visibility */
add_filter( 'nadlan_config_healthcheck', function ( $out ) {
	$t = nadlan_ur_thresholds();
	$out['urban_renewal'] = array( 'tools' => true, 'thresholds_effective' => $t['effective'] );
	return $out;
} );
