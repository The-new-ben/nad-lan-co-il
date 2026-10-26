<?php
/**
 * nadlan-config - URBAN RENEWAL TOOLS (L2, 2026-07-11).
 *
 * Pillar-embedded decision tools, calculators.php discipline: client-side
 * widgets, filterable legal constants WITH effective dates + a gov.il verify
 * link, YMYL disclaimers on every output, no em/en dashes.
 *
 *  [nadlan_ur_consent_calc]  apartments + consents -> the count condition of the
 *                            statutory special majority, never a full eligibility claim (HAD-396)
 *  [nadlan_ur_expectations]  what owners get, each row with its source
 *  [nadlan_ur_timeline]      the 10-stage strip (labels shared with L4)
 */

if ( ! defined( 'ABSPATH' ) ) { exit; }

if ( ! function_exists( 'nadlan_ur_thresholds' ) ) {
	function nadlan_ur_thresholds() {
		return apply_filters( 'nadlan_ur_thresholds', array(
			// HAD-396 round 2: the STATUTE, read directly on 3.10.2026 (Nevo, consolidated text current to 18.9.2023): חוק פינוי
			// ובינוי (עידוד מיזמי פינוי ובינוי), התשס"ו-2006, s. 1 "רוב מיוחס מבין בעלי הדירות": at least TWO THIRDS of all the
			// apartments in the cluster, AND (1) at least three fifths of the apartments in each building (a building of 4 or 5
			// apartments: at least 3, with more than two owners), AND (2) more than half of the common property in each building.
			// The calculator checks only the cluster count, as a fraction (50 apartments: 33 fail, 34 pass; 24: 16 pass), and
			// never claims the majority was reached: the two building conditions are shown as text. "66%" is a rounding.
			'effective'      => '18.9.2023',
			'checked'        => '3.10.2026',
			'source'         => 'https://www.nevo.co.il/law_html/law00/73988.htm',
			'majority_num'   => 2,
			'majority_den'   => 3,
			'building_num'   => 3,
			'building_den'   => 5,
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
			// HAD-396: every row carries its source (label, text, source name, source URL; competitors.md part ד, checked 3.10.2026).
			// The unsourced balcony size and the "usually included" safe room are gone.
			// round 2: every source below was read directly on 3.10.2026 (no proxy); the FAQ-only rows are gone or re-sourced to the statute
			array( 'תוספת שטח לדירה', 'במחשבון הכדאיות של הרשות הממשלתית להתחדשות עירונית, התוספת הממוצעת לדירת תמורה נבחרת בין 0 ל-30 מ"ר, וברירת המחדל היא 25 מ"ר.', 'paz21.com, מחשבון הכדאיות של הרשות הממשלתית', 'https://paz21.com/' ),
			array( 'מדיניות הרשות משנת 2020', '12 מ"ר ומרפסת לדירה. בדירה קטנה מ-52 מ"ר, תוספת של עד 25 מ"ר, כך שדירת התמורה תגיע ל-65 מ"ר לפחות.', 'מרכז הנדל"ן, 5.2.2020', 'https://www.nadlancenter.co.il/article/2265' ),
			array( 'חניה ומחסן', 'לפי אותה מדיניות, דירת התמורה כוללת חניה, ולרוב גם מחסן.', 'מרכז הנדל"ן, 5.2.2020', 'https://www.nadlancenter.co.il/article/2265' ),
			array( 'מגורים בתקופת הבנייה', 'אם לא הוצעו לבעל דירה מגורים חלופיים לתקופת הבנייה, סירובו לעסקה לא ייחשב בלתי סביר.', 'חוק פינוי ובינוי, סעיף 2(ב)(2)', 'https://www.nevo.co.il/law_html/law00/73988.htm' ),
			array( 'ערבויות', 'עסקת פינוי ובינוי כוללת התחייבות של היזם להעמיד ערבויות לטובת בעל הדירה, להבטחת התחייבויותיו לפי החוזה.', 'חוק פינוי ובינוי, סעיף 1, הגדרת "עסקת פינוי ובינוי"', 'https://www.nevo.co.il/law_html/law00/73988.htm' ),
			array( 'בעלי דירות מגיל 70', 'בעל דירה שגר בה, ושבמועד שבו היזם חתם על העסקה הראשונה בבניין מלאו לו 70 והוא גר בדירה שנתיים לפחות: אם לא הוצעה לו לפחות אחת מהחלופות שבחוק (למשל שתי דירות בשווי מצטבר דומה, או דירה קטנה יותר עם תשלומי איזון), סירובו לעסקה לא ייחשב בלתי סביר.', 'חוק פינוי ובינוי, סעיף 2(ב)(6)', 'https://www.nevo.co.il/law_html/law00/73988.htm' ),
		) );
	}
}

if ( ! function_exists( 'nadlan_ur_disclaimer' ) ) {
	function nadlan_ur_disclaimer() {
		$t = nadlan_ur_thresholds();
		return '<p class="nlur-disc">הנתונים אינם ייעוץ משפטי ואינם התחייבות. הגדרת הרוב המיוחס: סעיף 1 לחוק פינוי ובינוי (עידוד מיזמי פינוי ובינוי), התשס"ו-2006. הנוסח המחייב הוא החוק עצמו. לפני כל צעד התייעצו עם עורך דין מטעם הדיירים.</p>';
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
.nlur-cc__alt{font:400 12.5px/1.6 Heebo,sans-serif;color:#51483A;background:#F3EEE3;border-radius:10px;padding:10px 12px;margin:12px 0 0}
@media(max-width:560px){.nlur-exp td:first-child{white-space:normal}}
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
	data-num="<?php echo (int) $t['majority_num']; ?>" data-den="<?php echo (int) $t['majority_den']; ?>">
	<h3>מחשבון הסכמות: איפה הבניין שלכם עומד</h3>
	<p class="s">הזינו את מספר הדירות במקבץ (בניין אחד או כמה בניינים) ואת מספר הדירות שבעליהן כבר הסכימו, וראו כמה חסרות עד שני שלישים מהדירות במקבץ, אחד מתנאי הרוב המיוחס בפינוי בינוי.</p>
	<div class="nlur-cc__f">
		<label>סך הדירות<input type="number" id="nlur-cc-total" min="2" max="2000" inputmode="numeric" placeholder="לדוגמה: 24"></label>
		<label>מתוכן הסכימו<input type="number" id="nlur-cc-yes" min="0" max="2000" inputmode="numeric" placeholder="לדוגמה: 15"></label>
	</div>
	<div class="nlur-cc__pct" id="nlur-cc-pct" aria-live="polite">-</div>
	<div class="nlur-bar">
		<div class="nlur-bar__t"><span>שני שלישים מהדירות במקבץ</span><i>תנאי אחד מתוך שלושה</i></div>
		<div class="nlur-bar__w"><div class="nlur-bar__f"></div><div class="nlur-bar__m" style="inset-inline-start:<?php echo esc_attr( round( 100 * $t['majority_num'] / $t['majority_den'], 2 ) ); ?>%"></div></div>
		<div class="nlur-bar__note" data-open="מספר הדירות שהסכימו מגיע לשני שלישים מהדירות במקבץ. זה תנאי אחד: בדקו גם את שני התנאים שלמטה." data-closed="עוד {n} דירות עד שני שלישים מהדירות במקבץ"></div>
	</div>
	<p class="nlur-cc__alt">שני התנאים הנוספים של הרוב המיוחס, שהמחשבון לא בודק: לפחות שלוש חמישיות מהדירות בכל בניין שבמקבץ (בבניין של 4 או 5 דירות: לפחות 3 דירות, ויותר משני בעלי דירות), ויותר ממחצית הרכוש המשותף בכל בניין. בניין בודד שלא במתחם פינוי בינוי (חיזוק, או הריסה ובנייה) מתנהל לפי מסלול אחר, והרוב שלו לא מחושב כאן.</p>
	<?php echo nadlan_ur_disclaimer(); // phpcs:ignore WordPress.Security.EscapeOutput ?>
</div>
<script>
(function(){
	var box=document.querySelector(".nlur-cc");if(!box||box.dataset.nlurWired)return;box.dataset.nlurWired="1";
	var num=parseInt(box.dataset.num,10)||2,den=parseInt(box.dataset.den,10)||3;
	function calc(){
		var total=parseInt(document.getElementById("nlur-cc-total").value,10)||0;
		var yes=parseInt(document.getElementById("nlur-cc-yes").value,10)||0;
		if(yes>total)yes=total;
		var pct=total>0?yes/total:0;
		document.getElementById("nlur-cc-pct").textContent=total>0?(Math.round(pct*1000)/10)+"% ("+yes+" מתוך "+total+")":"-";
		box.querySelectorAll(".nlur-bar").forEach(function(b){
			var f=b.querySelector(".nlur-bar__f"),n=b.querySelector(".nlur-bar__note");
			f.style.width=Math.min(100,pct*100)+"%";
			// the statutory fraction, compared exactly: two thirds of 24 is 16; of 50, 34 (33 is 66% and falls short)
			var past=total>0&&yes*den>=num*total;
			b.classList.toggle("is-past",past);
			if(total>0){
				if(past){n.textContent=n.dataset.open}
				else{var need=Math.floor((num*total+den-1)/den)-yes;n.textContent=n.dataset.closed.replace("{n}",need)}
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
	$html .= '<div class="nlur-tool" dir="rtl"><h3>מה בעלי דירות מקבלים בפינוי בינוי</h3><p class="s">אלה אינם הבטחה: כל עסקה תלויה בעיר, במגרש ובכדאיות, והמספרים שלכם ייקבעו בשמאות ובמשא ומתן.</p><table class="nlur-exp">';
	foreach ( $rows as $r ) {
		// the row's source (columns 3-4) stays in the code and in docs/qa/had-396/editorial/record.md, not on the page (owner law 3.10.2026)
		$html .= '<tr><td>' . esc_html( $r[0] ) . '</td><td>' . esc_html( $r[1] ) . '</td></tr>';
	}
	$html .= '</table>' . nadlan_ur_disclaimer() . '</div>';
	return $html;
} );

add_shortcode( 'nadlan_ur_timeline', function () {
	$html = nadlan_ur_tools_css();
	$html .= '<div class="nlur-tool" dir="rtl"><h3>עשרת השלבים על ציר אחד</h3><p class="s">לפי דוח הרשות הממשלתית להתחדשות עירונית לשנת 2025, מאישור תוכנית פינוי בינוי ועד היתר הבנייה הראשון עברו בממוצע 4 שנים (28 מתחמים שקיבלו היתר ב-2025). השלב התכנוני הוא המשתנה הגדול בין פרויקט מהיר לאיטי.</p><div class="nlur-tl">';
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
