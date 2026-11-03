<?php
/**
 * nadlan-config - THE ASBESTOS PAGE TOOLS (HAD-668 R11e, 1.72.575; Claude Design v107.0 AsbestosHub). Ben, 3.11.2026: "the best
 * asbestos page in the world: tools, price guides, scientific data, all the authorities, an image, a map". Four instruments of
 * one family in assets/instruments/tools/asbestos.js, on the data file assets/instruments/data/asbestos.json
 * (tools/instruments/build_asbestos_data.py): asbcheck (what do I have, what do I do), asbcost (the price guide), asbmap (the
 * Western Galilee sites) and asbwho (who to call, by town). They join the engine's registry through its own filter, and the
 * page's figure, hazard line and numbers panel get their CSS here, only on a page that holds one of the tools.
 * Loaded by inc/instruments.php (only if present, so a rollback that removes this file leaves the engine working).
 */
if ( ! defined( 'ABSPATH' ) ) { exit; }

if ( ! function_exists( 'nadlan_asb_tool_ids' ) ) {

	function nadlan_asb_tool_ids() { return array( 'asbcheck', 'asbcost', 'asbmap', 'asbwho' ); }

	add_filter( 'nadlan_nli_tools', function ( $tools ) {
		$rel_he = array( '/home-inspection/' => 'בדק בית', '/buying-apartment/' => 'מדריך קניית דירה', '/real-estate-lawyer/' => 'עורך דין לקניית דירה', '/apartment-purchase-cost-calculator/' => 'עלות רכישה כוללת' );
		$rel_en = array( '/en/buy-property-in-israel/' => 'Buying property in Israel from abroad', '/en/sde-dov/contamination/' => 'The Sde Dov soil test map' );
		$d = array( 'asbestos.json' );
		$tools['asbcheck'] = array(
			'file' => 'asbestos', 'name' => 'מה יש לי ומה עושים: בדיקת אסבסט בבית', 'cat' => 'UtilitiesApplication', 'kicker' => 'בדיקה · אסבסט בבית', 'data' => $d, 'related' => $rel_he,
			'desc' => 'בוחרים מה מצאתם (גג, צינור, אדנית, ציפוי מרוסס, שברים אחרי שרפה) ובאיזה מצב הוא, ומקבלים את הצעדים לפי ההנחיות של המשרד להגנת הסביבה, מי מורשה לטפל, והאם צריך היתר.',
			'en' => array( 'name' => 'What do I have, and what do I do: an asbestos check at home', 'kicker' => 'Check · Asbestos at home', 'related' => $rel_en,
				'desc' => 'Choose what you found (a roof, a pipe, a planter, a sprayed coating, debris after a fire) and its state, and get the steps under the Ministry of Environmental Protection guidance, who is licensed to deal with it, and whether a permit is needed.' ),
		);
		$tools['asbcost'] = array(
			'file' => 'asbestos', 'name' => 'מחשבון עלות פינוי אסבסט', 'cat' => 'FinanceApplication', 'kicker' => 'מחשבון · פינוי אסבסט', 'data' => $d, 'related' => $rel_he,
			'desc' => 'הערכת עלות לפינוי לוחות אסבסט-צמנט שבורים, חומר מתפורר אחרי שרפה או החלפת גג אסבסט: מחיר הייחוס של מכרז המשרד להגנת הסביבה (50 ₪ למ״ר, 1,600 ₪ למ״ק, לפי מרכז המחקר של הכנסת, 7.2023) והטווחים המסחריים שפורסמו.',
			'en' => array( 'name' => 'Asbestos removal cost calculator', 'kicker' => 'Calculator · Asbestos removal', 'related' => $rel_en,
				'desc' => 'An estimate for removing broken asbestos-cement sheets, crumbled material after a fire, or replacing an asbestos roof: the Ministry of Environmental Protection tender reference price (NIS 50 per m², NIS 1,600 per m³, per the Knesset Research and Information Center, 7.2023) and the published commercial ranges.' ),
		);
		$tools['asbmap'] = array(
			'file' => 'asbestos', 'name' => 'מפת אתרי האסבסט בגליל המערבי', 'cat' => 'ReferenceApplication', 'kicker' => 'מפה · הגליל המערבי', 'data' => $d, 'related' => $rel_he,
			'desc' => '348 האתרים של פרויקט ניקוי הקרקעות מאסבסט פריך בגליל המערבי, לפי השכבה של המשרד להגנת הסביבה: 234 נוקו ולא ידוע על אסבסט שנותר, 101 נוקו וידוע שנותר אסבסט תחת התשתיות, 13 טרם נוקו. לפי יישוב.',
			'en' => array( 'name' => 'Map of the asbestos sites in Western Galilee', 'kicker' => 'Map · Western Galilee', 'related' => $rel_en,
				'desc' => 'The 348 sites of the Western Galilee friable-asbestos soil clean-up project, from the Ministry of Environmental Protection layer: 234 cleaned with no asbestos known to remain, 101 cleaned with asbestos known to remain under the infrastructure, 13 not yet cleaned. By locality.' ),
		);
		$tools['asbwho'] = array(
			'file' => 'asbestos', 'name' => 'למי פונים באסבסט, לפי העיר', 'cat' => 'ReferenceApplication', 'kicker' => 'איתור · למי פונים', 'data' => $d, 'related' => $rel_he,
			'desc' => 'לכל אחת מ־255 הרשויות המקומיות: היחידה הסביבתית שלה (רשימת המשרד להגנת הסביבה), כמה בעלי רישיון אסבסט רשומים במחוז לפי סוג הרישיון, אתרי ההטמנה המורשים והמוקדים ‎*6911 ו־106.',
			'en' => array( 'name' => 'Who to call about asbestos, by town', 'kicker' => 'Finder · Who to call', 'related' => $rel_en,
				'desc' => 'For each of the 255 local authorities: its environmental unit (the Ministry of Environmental Protection list), how many asbestos licence holders are registered in its district by licence type, the licensed landfill sites and the hotlines *6911 and 106.' ),
		);
		return $tools;
	} );

	add_action( 'wp_head', function () {
		if ( ! function_exists( 'nadlan_nli_page_ids' ) || ! array_intersect( nadlan_nli_page_ids(), nadlan_asb_tool_ids() ) ) { return; }
		// the page's own surfaces (figure, hazard line, numbers) and the tools' extra parts; fibre-cement greys and the hazard-tag yellow
		echo '<style id="nadlan-asb-css">'
			. '.asbp{--asb-ink:#121417;--asb-cement:#6e7276;--asb-sheet:#f3f4f3;--asb-line:#d5d8d6;--asb-tag:#f2c230;--asb-ok:#3f7d5a;--asb-amber:#c9831a;--asb-red:#b23a2e}'
			. 'html body .asbp-tag{display:inline-flex;align-items:center;gap:8px;margin:0 0 14px!important;padding:6px 12px;background:#121417;color:#f2c230!important;font:600 14px/1.3 "IBM Plex Sans Hebrew","IBM Plex Sans",system-ui,sans-serif!important;border-radius:2px}'
			. 'html body .asbp-tag b{color:#fff}'
			. '.asbp-cta{display:flex;flex-wrap:wrap;gap:10px;margin:6px 0 22px}'
			. 'html body .asbp-cta a{display:inline-flex;align-items:center;min-height:44px;padding:10px 16px;border:1px solid #121417;border-radius:2px;color:#121417!important;text-decoration:none!important;font:600 15px/1.3 "IBM Plex Sans Hebrew","IBM Plex Sans",system-ui,sans-serif;background:#fff}'
			. 'html body .asbp-cta a.is-main{background:#121417;color:#fff!important}'
			. '.asbh{position:relative;margin:0 0 8px!important;max-width:100%}.asbh img{display:block;width:100%;height:auto;border-radius:4px;background:#f3f4f3}'
			. '.asbh-l{position:absolute;left:var(--x);top:var(--y);transform:translate(-50%,-100%);background:#121417;color:#fff;font:600 12.5px/1.25 "IBM Plex Sans Hebrew","IBM Plex Sans",system-ui,sans-serif;padding:4px 8px;border-radius:2px;white-space:nowrap;pointer-events:none;box-shadow:0 0 0 2px #f2c230}'
			. '.asbh-l::after{content:"";position:absolute;left:50%;top:100%;width:2px;height:10px;background:#f2c230;transform:translateX(-50%)}'
			. '.asbh-l.is-b{transform:translate(-50%,0)}.asbh-l.is-b::after{top:auto;bottom:100%}'
			. 'html body .asbh-l b{font:inherit;color:inherit}.asbh-l .s{display:none}@media (max-width:640px){.asbh-l{font-size:11px;padding:3px 6px}.asbh-l .l{display:none}.asbh-l .s{display:inline}}'
			. 'html body .asbh figcaption{font:400 13px/1.5 "IBM Plex Sans Hebrew","IBM Plex Sans",system-ui,sans-serif;color:#4a4f53;margin-top:6px}'
			. '.asbn{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:1px;background:#3a3f43;border-radius:4px;overflow:hidden;margin:18px 0 26px}'
			. '@media (min-width:860px){.asbn{grid-template-columns:repeat(4,minmax(0,1fr))}}'
			. '.asbn>div{background:#121417;padding:14px 14px 12px;display:grid;gap:4px;min-width:0}'
			. 'html body .asbn strong{font:600 26px/1.1 "IBM Plex Mono",ui-monospace,monospace;color:#f2c230}'
			. 'html body .asbn span{font:500 13.5px/1.35 "IBM Plex Sans Hebrew","IBM Plex Sans",system-ui,sans-serif;color:#fff}'
			. 'html body .asbn small{font:400 11.5px/1.35 "IBM Plex Sans Hebrew","IBM Plex Sans",system-ui,sans-serif;color:#a9acab}'
			. '.asbx__q{display:grid;gap:6px;margin:0 0 12px;position:relative}.asbx__q>span{font:500 13px/18px var(--nli-sans);color:var(--nli-ink)}'
			. 'html body .nli .asbx__chips button[aria-pressed="true"],html body .nli .asbm__chips button[aria-pressed="true"]{background:#121417;border-color:#121417;color:#fff}'
			. '.asbx__out{border:1px solid var(--nli-line);border-top:4px solid #6e7276;border-radius:var(--nli-r-m);padding:14px 16px;margin:6px 0 12px;position:relative;background:#fff}'
			. '.asbx__out.is-low{border-top-color:#3f7d5a}.asbx__out.is-mid{border-top-color:#c9831a}.asbx__out.is-high{border-top-color:#b23a2e}.asbx__out.is-ask{border-top-color:#2f6f86}'
			. 'html body .nli p.asbx__lv{font:600 18px/1.35 var(--nli-sans);color:var(--nli-ink);margin:0 0 10px}'
			. 'html body .nli p.asbx__h{font:600 13px/18px var(--nli-sans);letter-spacing:.04em;color:var(--nli-sea);margin:12px 0 4px}'
			. 'html body .nli .asbx__out ol,html body .nli .asbw__fix ul{margin:0;padding-inline-start:20px;display:grid;gap:6px;font:400 15px/1.55 var(--nli-sans);color:var(--nli-ink2)}'
			. 'html body .nli .asbx__out p,html body .nli .asbw__card p{margin:0;font:400 15px/1.55 var(--nli-sans);color:var(--nli-ink2)}'
			. '.asbm__map{position:relative;height:min(64vh,540px);min-height:340px;border:1px solid var(--nli-line);border-radius:var(--nli-r-m);overflow:hidden;margin:10px 0;background:#eef0ef}'
			. '.asbm__dot{display:inline-block;width:10px;height:10px;border-radius:50%;margin-inline-end:6px;vertical-align:-1px}'
			. '.asbw__out{display:grid;gap:12px;margin:12px 0;position:relative}@media (min-width:860px){.asbw__out{grid-template-columns:minmax(0,1fr) minmax(0,1.3fr)}}'
			. '.asbw__card,.asbw__bars,.asbw__fix{border:1px solid var(--nli-line);border-radius:var(--nli-r-m);padding:14px 16px;background:#fff;min-width:0;position:relative}'
			. 'html body .nli p.asbw__name{font:600 19px/1.3 var(--nli-sans)!important;color:var(--nli-ink)!important;margin:0 0 6px!important}'
			. '.asbw__bar{display:grid;grid-template-columns:minmax(0,1.4fr) minmax(0,2fr) 40px;gap:8px;align-items:center;font:400 13.5px/1.35 var(--nli-sans);margin:4px 0}'
			. '.asbw__bar i{display:block;height:10px;background:#6e7276;border-radius:1px;min-width:2px}.asbw__bar b{font:500 14px/1 var(--nli-mono);color:var(--nli-ink);text-align:end}'
			. 'html body .nli .asbw__fix ul span{color:var(--nli-mute)}'
			. '</style>';
	}, 31 );
}
