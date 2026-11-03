<?php
/**
 * nadlan-config - THE ENVIRONMENTAL-HAZARDS MAP TOOLS (HAD-670 R13e, 1.72.578; Claude Design v109.0 HazardMap). Ben, 3.11.2026 night:
 * "the awesome map: a very extensive page, the best in the world, a 3D map where people see where they are, 4-5 complex tools with
 * easy UX on mobile, practical for choosing where to live, professionals and prices, an honesty statement". Five instruments of one
 * family in assets/instruments/tools/hazards.js, on assets/instruments/data/hazards.json and hazards-lines.json
 * (tools/instruments/build_hazards_data.py: MoEP antennas with their measured share of the health threshold, PRTR plants, the
 * contaminated-land database, Ministry of Energy fuel stations, MoEP air stations, OpenStreetMap power lines, substations and plants;
 * no company, operator or plant name): hzmap, hzant, hzcompare, hzcity, hzplan. The page's figure, numbers, professionals and
 * honesty blocks get their CSS here, only on a page that holds one of the tools.
 * Loaded by inc/instruments.php (only if present, so a rollback that removes this file leaves the engine working).
 */
if ( ! defined( 'ABSPATH' ) ) { exit; }

if ( ! function_exists( 'nadlan_hz_tool_ids' ) ) {

	function nadlan_hz_tool_ids() { return array( 'hzmap', 'hzant', 'hzcompare', 'hzcity', 'hzplan' ); }

	add_filter( 'nadlan_nli_tools', function ( $tools ) {
		$rel = array( '/asbestos/' => 'אסבסט: איך מזהים ומה עושים', '/home-inspection/' => 'בדק בית', '/buying-apartment/' => 'מדריך קניית דירה', '/real-estate-lawyer/' => 'עורך דין לקניית דירה' );
		$pts = array( 'hazards.json' ); $all = array( 'hazards.json', 'hazards-lines.json' );
		// 1.72.579 (R13g): the English page /en/environmental-hazards/ prints the English name, kicker, description and related links
		$rel_en = array( '/en/asbestos/' => 'Asbestos in Israel', '/en/buy-property-in-israel/' => 'Buying property in Israel from abroad', '/en/sde-dov/contamination/' => 'The Sde Dov soil test map' );
		$tools['hzmap'] = array( 'file' => 'hazards', 'name' => 'מפת מפגעים סביבתיים לפי כתובת', 'cat' => 'ReferenceApplication', 'kicker' => 'מפה · מפגעים סביבתיים', 'data' => $all, 'related' => $rel,
			'desc' => 'לפי כתובת, מיקום או נגיעה במפה: כל אנטנה סלולרית עם הקרינה שנמדדה בה באחוזים מסף הבריאות, קווי מתח עליון, תחנות משנה, מפעלים שמדווחים על פליטות, תחנות דלק, אתרי קרקע ותחנות ניטור אוויר, ברדיוס של 100 עד 1,000 מטר, עם המרחק לכל אחד. מאגרי המשרד להגנת הסביבה, משרד האנרגיה ו-OpenStreetMap.',
			'en' => array( 'name' => 'Environmental hazards map by address', 'kicker' => 'Map · Environmental hazards', 'related' => $rel_en, 'desc' => 'By address, your location or a tap on the map: every cellular antenna with the radiation measured at it as a percentage of the health threshold, high-voltage lines, substations, plants that report emissions, fuel stations, soil sites and air monitoring stations, within 100 to 1,000 metres, with the distance to each. Registers of the Ministry of Environmental Protection, the Ministry of Energy and OpenStreetMap.' ) );
		$tools['hzant'] = array( 'file' => 'hazards', 'name' => 'בדיקת קרינה מאנטנות סלולריות ליד הבית', 'cat' => 'ReferenceApplication', 'kicker' => 'בדיקה · אנטנות סלולריות', 'data' => $pts, 'related' => $rel,
			'desc' => 'עשר האנטנות הסלולריות הקרובות לנקודה, עם המרחק, סוג האתר, התוצאה הגבוהה שנמדדה באחוזים מסף הבריאות ושנת הבדיקה האחרונה, לפי מאגר המשרד להגנת הסביבה (8,525 אתרים).',
			'en' => array( 'name' => 'Radiation measured at the cellular antennas near a home', 'kicker' => 'Check · Cellular antennas', 'related' => $rel_en, 'desc' => 'The ten cellular antennas nearest to a point, with the distance, the site type, the highest measured result as a percentage of the health threshold and the year of the last check, from the Ministry of Environmental Protection register (8,525 sites).' ) );
		$tools['hzcompare'] = array( 'file' => 'hazards', 'name' => 'השוואת מפגעים סביבתיים בין שתי כתובות', 'cat' => 'ReferenceApplication', 'kicker' => 'השוואה · שתי כתובות', 'data' => $all, 'related' => $rel,
			'desc' => 'שתי כתובות זו מול זו: האנטנות, קווי המתח, תחנות המשנה, המפעלים המדווחים ותחנות הדלק ברדיוס של 250 מטר, והקרוב מכל סוג.',
			'en' => array( 'name' => 'Compare environmental hazards at two addresses', 'kicker' => 'Compare · Two addresses', 'related' => $rel_en, 'desc' => 'Two addresses side by side: the antennas, power lines, substations, reporting plants and fuel stations within 250 metres, and the nearest of each kind.' ) );
		$tools['hzcity'] = array( 'file' => 'hazards', 'name' => 'אנטנות סלולריות, מפעלים ותחנות דלק לפי עיר', 'cat' => 'ReferenceApplication', 'kicker' => 'נתונים · לפי עיר', 'data' => $pts, 'related' => $rel,
			'desc' => 'לכל יישוב: מספר האנטנות הסלולריות הפעילות, הקרינה החציונית והגבוהה שנמדדה בהן מסף הבריאות, מספר המפעלים המדווחים ומספר תחנות הדלק.',
			'en' => array( 'name' => 'Cellular antennas, plants and fuel stations by town', 'kicker' => 'Data · By town', 'related' => $rel_en, 'desc' => 'For each town: the number of active cellular antennas, the median and highest radiation measured at them as a share of the health threshold, the number of reporting plants and of fuel stations.' ) );
		$tools['hzplan'] = array( 'file' => 'hazards', 'name' => 'תכנית בדיקה לדירה: קרינה, רעש, זיהום ומצב הבית', 'cat' => 'UtilitiesApplication', 'kicker' => 'תכנון · לפני שקונים', 'data' => array(), 'related' => $rel,
			'desc' => 'מסמנים מה יש ליד הדירה ומקבלים תכנית בדיקה: מודד קרינה בעל היתר, יועץ אקוסטי, יועץ סביבתי, בודק בית ועורך דין לתכנון ובנייה, מה כל אחד בודק, והמחיר במקום שבו פורסם.',
			'en' => array( 'name' => 'A check plan for a flat: radiation, noise, pollution and condition', 'kicker' => 'Plan · Before you buy', 'related' => $rel_en, 'desc' => 'Mark what is near the flat and get a check plan: a licensed radiation surveyor, an acoustic consultant, an environmental consultant, a home inspector and a planning lawyer, what each checks, and the price where one was published.' ) );
		return $tools;
	} );

	add_action( 'wp_head', function () {
		if ( ! function_exists( 'nadlan_nli_page_ids' ) || ! array_intersect( nadlan_nli_page_ids(), nadlan_hz_tool_ids() ) ) { return; }
		$f = '"IBM Plex Sans Hebrew","IBM Plex Sans",system-ui,sans-serif';
		echo '<style id="nadlan-hz-css">'
			// the page: buttons, the aerial figure with its labels, the numbers, the professionals, the sponsor slot, the honesty statement
			. 'html body .hzp-cta{display:flex;flex-wrap:wrap;gap:10px;margin:6px 0 20px}'
			. 'html body .hzp-cta a{display:inline-flex;align-items:center;min-height:44px;padding:10px 16px;border:1.5px solid #101820;border-radius:6px;color:#101820!important;text-decoration:none!important;font:600 15px/1.3 ' . $f . ';background:#fff}'
			. 'html body .hzp-cta a.is-main{background:#0f2733;border-color:#0f2733;color:#fff!important}'
			. '.hzf{position:relative;margin:0 0 10px!important;max-width:100%}.hzf img{display:block;width:100%;height:auto;border-radius:6px;background:#e9eef1}'
			. '.hzf-l{position:absolute;left:var(--x);top:var(--y);transform:translate(-50%,-100%);background:#0f2733;color:#fff;font:600 12.5px/1.25 ' . $f . ';padding:4px 8px;border-radius:3px;white-space:nowrap;pointer-events:none;box-shadow:0 0 0 2px var(--c,#fff)}'
			. '.hzf-l::after{content:"";position:absolute;left:50%;top:100%;width:2px;height:10px;background:var(--c,#fff);transform:translateX(-50%)}'
			. '.hzf-l .s{display:none}@media (max-width:640px){.hzf-l{font-size:11px;padding:3px 6px}.hzf-l .l{display:none}.hzf-l .s{display:inline}}'
			. 'html body .hzf-l b{font:inherit;color:inherit}'
			. 'html body .hzf figcaption{font:400 13px/1.5 ' . $f . ';color:#5f6b75;margin-top:6px}'
			. '.hzn{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));border:1px solid #d7dde2;border-radius:6px;overflow:hidden;margin:0 0 22px;background:#f4f6f8}'
			. '@media (min-width:860px){.hzn{grid-template-columns:repeat(4,minmax(0,1fr))}}'
			. '.hzn>div{padding:12px 14px;display:grid;gap:3px;border-inline-start:1px solid #d7dde2;border-bottom:1px solid #d7dde2;min-width:0}'
			. 'html body .hzn strong{font:600 21px/1.1 "IBM Plex Mono",ui-monospace,monospace;color:#0f2733}'
			. 'html body .hzn span{font:500 13px/1.35 ' . $f . ';color:#38434d}html body .hzn small{font:400 11.5px/1.3 ' . $f . ';color:#5f6b75}'
			. '.hzpros{display:grid;gap:10px;margin:8px 0 22px}@media (min-width:760px){.hzpros{grid-template-columns:repeat(2,minmax(0,1fr))}}'
			. '.hzpro{background:#fff;border:1px solid #d7dde2;border-radius:8px;padding:14px;display:grid;gap:6px;min-width:0}'
			. 'html body .hzpro p{margin:0!important;font:400 14.5px/1.55 ' . $f . ';color:#38434d}html body .hzpro p.t{font:600 16px/1.3 ' . $f . ';color:#101820}'
			. 'html body .hzpro p.m{font:600 13.5px/1.3 "IBM Plex Mono",ui-monospace,monospace;color:#0f2733}'
			. '.hzslot{border:1.5px dashed #9fb3bf;background:#f8fafb}html body .hzslot p.t{color:#0f2733}'
			. '.hzhonest{background:#0f2733;border-radius:8px;padding:18px;margin:8px 0 24px}'
			. 'html body .hzhonest h2{color:#fff!important;margin:0 0 10px!important;font:700 21px/1.3 ' . $f . '!important}'
			. 'html body .hzhonest li{color:#d6e3ea!important;font:400 15px/1.6 ' . $f . ';margin:0 0 8px}html body .hzhonest li strong{color:#fff!important}'
			// the tools
			. '.hzm__scope{background:#0f2733;border-radius:var(--nli-r-m);padding:12px;display:grid;gap:10px;position:relative}'
			. '.hzm__find{display:grid;grid-template-columns:1fr auto;gap:8px}.hzm__find input{grid-column:1/-1}'
			. '@media (min-width:640px){.hzm__find{grid-template-columns:1fr auto auto}.hzm__find input{grid-column:auto}}'
			. 'html body .nli .hzm__find input,html body .nli .hzc__f input{font:500 16px/1.2 var(--nli-sans);padding:12px;border:1px solid #2b5566!important;border-radius:6px;background:#fff!important;color:#101820;width:100%;box-sizing:border-box;margin:0;box-shadow:none!important;height:auto}'
			. 'html body .nli .hzm__go{min-height:44px;padding:0 18px;border:0;border-radius:6px;background:#fff;color:#0f2733;font:700 15px/1 var(--nli-sans);cursor:pointer}'
			. 'html body .nli .hzc__f .hzm__go{background:#0f2733;color:#fff}'
			. 'html body .nli .hzm__loc{min-height:44px;display:inline-flex;align-items:center;justify-content:center;gap:6px;padding:0 14px;border:1px solid #2b5566;border-radius:6px;background:#173645;color:#fff;font:600 14px/1 var(--nli-sans);cursor:pointer}'
			. '.hzm__loc svg{width:16px;height:16px}'
			. 'html body .nli p.hzm__where{margin:0!important;font:500 13.5px/1.4 var(--nli-sans);color:#d6e3ea}'
			. '.hzm__rad,.hzm__layers{display:flex;gap:6px;overflow-x:auto;padding-bottom:2px;-webkit-overflow-scrolling:touch}'
			. 'html body .nli .hzm__rad button,html body .nli .hzm__layers button{flex:0 0 auto;display:inline-flex;align-items:center;gap:6px;min-height:36px;padding:6px 12px;border:1px solid #2b5566;border-radius:999px;background:transparent;color:#fff;font:600 13px/1 var(--nli-sans);cursor:pointer;white-space:nowrap}'
			. 'html body .nli .hzm__rad button[aria-pressed="true"]{background:#fff;color:#0f2733}'
			. 'html body .nli .hzm__layers button[aria-pressed="false"]{opacity:.5}.hzm__layers i{width:10px;height:10px;border-radius:2px;display:inline-block}'
			. '.hzm__map{position:relative;height:min(62vh,520px);min-height:330px;border-radius:6px;overflow:hidden;background:#e9eef1}'
			. '.hzm__bar{display:flex;justify-content:flex-start}html body .nli .hzm__3d{min-height:36px;padding:0 14px;border:1px solid #2b5566;border-radius:6px;background:#173645;color:#fff;font:600 13px/1 var(--nli-sans);cursor:pointer}'
			. '.hzm__rep{margin:12px 0;position:relative}html body .nli p.hzm__k{margin:0 0 6px!important;font:600 12.5px/1.4 var(--nli-sans);letter-spacing:.03em;color:#0b8fb3}'
			. '.hzr{display:grid;grid-template-columns:14px minmax(0,1fr) auto;gap:10px;align-items:start;padding:10px 0;border-top:1px solid #edf0f2}'
			. '.hzr i{width:12px;height:12px;border-radius:2px;margin-top:4px}.hzr b{display:block;font:600 15px/1.3 var(--nli-sans);color:var(--nli-ink)}'
			. '.hzr span{font:400 13.5px/1.5 var(--nli-sans);color:var(--nli-ink2)}.hzr em{font-style:normal;font:600 13.5px/1.2 var(--nli-mono);color:var(--nli-ink);white-space:nowrap}'
			. '.hzr.none em{color:var(--nli-mute);font-family:var(--nli-sans);font-weight:500}'
			. '.hza__bar{display:block;height:6px;border-radius:1px;background:#6a4fd6;margin-top:5px;max-width:100%}'
			. '.hzc__f{display:grid;gap:8px;margin:0 0 12px}@media (min-width:640px){.hzc__f{grid-template-columns:1fr 1fr auto}}'
			. '.hzc__grid{display:grid;gap:12px}@media (min-width:760px){.hzc__grid{grid-template-columns:1fr 1fr}}.hzc__col{border:1px solid var(--nli-line);border-radius:6px;padding:10px 12px;min-width:0}'
			. '.hzy__grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:8px;margin:10px 0 6px}@media (min-width:760px){.hzy__grid{grid-template-columns:repeat(5,minmax(0,1fr))}}'
			. '.hzy__grid div{border:1px solid var(--nli-line);border-radius:6px;padding:10px;display:grid;gap:3px}.hzy__grid b{font:600 20px/1.1 var(--nli-mono);color:#0f2733}.hzy__grid span{font:400 12.5px/1.35 var(--nli-sans);color:var(--nli-ink2)}'
			. 'html body .nli .hzp__chips button[aria-pressed="true"]{background:#0f2733;border-color:#0f2733;color:#fff}'
			. '.hzp__out ol{margin:10px 0;padding-inline-start:20px;display:grid;gap:10px;font:400 14.5px/1.55 var(--nli-sans);color:var(--nli-ink2)}.hzp__out b{color:var(--nli-ink)}'
			. '.hzp__out em{font-style:normal;display:inline-block;margin-top:2px;font:600 13px/1.3 var(--nli-mono);color:#0f2733}'
			. '</style>';
	}, 31 );
}
