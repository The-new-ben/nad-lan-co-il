<?php
/**
 * NadLan Instruments (HAD-527, Ben 14.10.2026): the engine of the tools program. A page holds [nadlan_tool id="…"]; this
 * module loads the engine (assets/instruments/core.css + core.js), the tool's own logic (assets/instruments/tools/<id>.js) and
 * its official data (assets/instruments/data/*.json, built by tools/instruments/build_index_data.py), only on pages that use a
 * tool, with the fonts of the design system "NadLan Instruments" (https://claude.ai/artifact/ATybPAavyDEkAzH7cdg1bB:
 * Karantina, IBM Plex Sans Hebrew, IBM Plex Mono). Before the script runs, the shortcode prints a plain summary with the real
 * numbers (for search engines and AI answers); the script replaces it with the live instrument. Every tool also prints its
 * related tools (the organ: tools link each other and the guides), and the page gets SoftwareApplication JSON-LD.
 */
if ( ! defined( 'ABSPATH' ) ) { exit; }


if ( ! function_exists( 'nadlan_nli_tools' ) ) {

	/** The registry: id => name, description, data files, related links (path => label). */
	function nadlan_nli_tools() {
		return apply_filters( 'nadlan_nli_tools', array(
			'indexation' => array(
				'name' => 'מחשבון הצמדה למדד תשומות הבנייה', 'cat' => 'FinanceApplication',
				'desc' => 'מחשב את תוספת ההצמדה של דירה מקבלן לפי לוח התשלומים, כללי חוק המכר (תיקון 9) והמדד הרשמי של הלשכה המרכזית לסטטיסטיקה.',
				'data' => array( 'cbs-200010.json' ),
				'related' => array( '/new-projects/contractor-delay-compensation/' => 'פיצוי על איחור במסירה', '/cpi-calculator/' => 'הצמדה למדד המחירים לצרכן', '/purchase-tax-calculator/' => 'מחשבון מס רכישה', '/mortgage-calculator/' => 'מחשבון משכנתא', '/apartment-purchase-cost-calculator/' => 'עלות רכישה כוללת', '/apartment-prices/' => 'מחירון הדירות לפי עיר' ),
			),
			'delay' => array(
				'name' => 'מחשבון פיצוי על איחור במסירת דירה', 'cat' => 'FinanceApplication',
				'desc' => 'מחשב את הפיצוי לפי סעיף 5א לחוק המכר (דירות), חודש אחרי חודש, לפי מועד החתימה, מועד המסירה בחוזה ודמי השכירות באזור.',
				'data' => array(),
				'related' => array( '/new-projects/construction-input-index/' => 'הצמדה למדד תשומות הבנייה', '/cpi-calculator/' => 'הצמדה למדד המחירים לצרכן', '/apartment-prices/' => 'מחירון הדירות לפי עיר', '/purchase-tax-calculator/' => 'מחשבון מס רכישה', '/mortgage-calculator/' => 'מחשבון משכנתא' ),
			),
			'cpi' => array(
				'name' => 'מחשבון הצמדה למדד המחירים לצרכן', 'cat' => 'FinanceApplication',
				'desc' => 'מצמיד סכום, שכר דירה או חוב למדד המחירים לצרכן של הלשכה המרכזית לסטטיסטיקה, לפי המדד הידוע או המדד בגין, עם ריבית לפי הצורך.',
				'data' => array( 'cbs-120010.json' ),
				'related' => array( '/new-projects/construction-input-index/' => 'הצמדה למדד תשומות הבנייה', '/mortgage-calculator/mortgage-interest-rates/' => 'ריבית בנק ישראל והפריים', '/mortgage-calculator/' => 'מחשבון משכנתא', '/apartment-prices/' => 'מחירון הדירות לפי עיר', '/new-projects/contractor-delay-compensation/' => 'פיצוי על איחור במסירה' ),
			),
			'warranty' => array(
				'name' => 'שעון הבדק והאחריות של חוק המכר', 'cat' => 'UtilitiesApplication',
				'desc' => 'מתאריך מסירת הדירה: לכל סוג ליקוי לפי התוספת לחוק המכר, מתי נגמרות תקופת הבדק ותקופת האחריות, וכמה ימים נשארו.',
				'data' => array(),
				'related' => array( '/home-inspection/' => 'בדק בית', '/new-projects/contractor-delay-compensation/' => 'פיצוי על איחור במסירה', '/new-projects/construction-input-index/' => 'הצמדה למדד תשומות הבנייה', '/cpi-calculator/' => 'הצמדה למדד המחירים לצרכן' ),
			),
			'soilmap' => array(
				'name' => 'מפת בדיקות הקרקע בשדה דב', 'cat' => 'ReferenceApplication', 'kicker' => 'מפה · שדה דב',
				'desc' => 'מפה תלת־ממדית של מגרשי רובע שדה דב: לכל מגרש שפורסם עליו סקר קרקע, פי כמה ריכוז ה־PFOS מעל ערך הסף, באיזה עומק, כמה קידוחים חרגו, והדו"ח עצמו. בדיקה לפי מספר מגרש או פרויקט.',
				'data' => array( 'sde-dov-soil.json' ),
				'related' => array( '/sde-dov/' => 'המדריך לשדה דב', '/sde-dov/prices/' => 'מחירי הדירות בשדה דב', '/real-estate-lawyer/construction-defects-lawsuit/' => 'שעון הבדק והאחריות', '/new-projects/construction-input-index/' => 'הצמדה למדד תשומות הבנייה' ),
				'en' => array(  // HAD-534 (d): the English page /en/sde-dov/contamination/
					'name' => 'Sde Dov soil test map', 'kicker' => 'Map · Sde Dov',
					'desc' => 'A 3D map of the Sde Dov district plots: for every plot with a published soil survey, how many times the PFOS value is above the threshold, at what depth, how many boreholes exceeded it, and the report itself. Check any plot by its number.',
					'related' => array( '/en/sde-dov/' => 'The Sde Dov guide', '/en/sde-dov/prices/' => 'Sde Dov apartment prices', '/en/north-tel-aviv/' => 'North Tel Aviv real estate', '/en/buy-property-in-israel/' => 'Buying property in Israel from abroad' ),
				),
			),
			'pfas' => array(
				'name' => 'מחשבון PFAS: פי כמה מעל ערך הסף', 'cat' => 'UtilitiesApplication', 'kicker' => 'מחשבון · קרקע',
				'desc' => 'ממיר ריכוז של PFOS, PFOA או PFHxS מדו"ח סקר קרקע (ננוגרם, מיקרוגרם או מיליגרם לק"ג) לפי כמה הוא מעל ערך הסף למגע ישיר שמשמש בדו"חות של שדה דב, ומשווה לשיאים שפורסמו.',
				'data' => array( 'sde-dov-soil.json' ),
				'related' => array( '/sde-dov/' => 'המדריך לשדה דב', '/sde-dov/prices/' => 'מחירי הדירות בשדה דב' ),
				'en' => array(
					'name' => 'PFAS calculator: how many times the threshold', 'kicker' => 'Calculator · Soil',
					'desc' => 'Converts a PFOS, PFOA or PFHxS concentration from a soil survey report (ng, µg or mg per kg) into how many times the direct-contact threshold used in the Sde Dov reports, and compares it with the published peaks.',
					'related' => array( '/en/sde-dov/' => 'The Sde Dov guide', '/en/sde-dov/prices/' => 'Sde Dov apartment prices' ),
				),
			),
			'soilask' => array(
				'name' => 'מכתב שאלות ליזם על הקרקע במגרש', 'cat' => 'UtilitiesApplication', 'kicker' => 'מחולל · שדה דב',
				'desc' => 'מכתב מוכן ליזם על מצב הקרקע במגרש בשדה דב: נפתח במה שפורסם על המגרש ושואל על הדיגום לפי הנחיות 12.2.2026, הדו"ח המלא, אימוץ הממצאים, תכנית הטיפול, מועד המסירה, העלות והחוזה. מכתב מלא או הודעת וואטסאפ.',
				'data' => array( 'sde-dov-soil.json' ),
				'related' => array( '/real-estate-lawyer/' => 'עורך דין לקניית דירה', '/new-projects/contractor-delay-compensation/' => 'פיצוי על איחור במסירה', '/sde-dov/' => 'המדריך לשדה דב' ),
				'en' => array(
					'name' => 'A letter of soil questions for the developer', 'kicker' => 'Generator · Sde Dov',
					'desc' => 'A ready letter to the developer about the soil on a Sde Dov plot: it opens with what was published about the plot and asks about sampling under the 12 Feb 2026 guidelines, the full report, the adoption of the findings, the treatment plan, the delivery date, the cost and the contract. A full letter or a WhatsApp message, in English or in Hebrew.',
					'related' => array( '/en/buy-property-in-israel/' => 'Buying property in Israel from abroad', '/en/guides/new-apartment-sale-specification/' => 'The sale specification of a new apartment', '/en/sde-dov/' => 'The Sde Dov guide' ),
				),
			),
			'prime' => array(
				'name' => 'מחשבון ריבית הפריים וההחזר החודשי', 'cat' => 'FinanceApplication',
				'desc' => 'מראה את ריבית בנק ישראל והפריים היום, את ההחזר החודשי במסלול הפריים, וכמה הוא משתנה בכל שינוי של רבע אחוז בריבית.',
				'data' => array( 'boi-rate.json' ),
				'related' => array( '/mortgage-calculator/' => 'מחשבון משכנתא', '/cpi-calculator/' => 'הצמדה למדד המחירים לצרכן', '/apartment-purchase-cost-calculator/' => 'עלות רכישה כוללת', '/apartment-prices/' => 'מחירון הדירות לפי עיר' ),
			),
			'ptax' => array(
				'name' => 'מחשבון מס רכישה', 'cat' => 'FinanceApplication', 'kicker' => 'מחשבון · מס רכישה',
				'desc' => 'מחשב את מס הרכישה על דירה לפי המדרגות של רשות המסים בכל המסלולים: דירה יחידה, דירה נוספת, עולה חדש, תושב חוץ, נכה, קרקע ומתנה לקרוב, ועד מתי כל שיעור בתוקף; למשפרי דיור גם עד מתי למכור את הדירה הקודמת, כולל הארכת המלחמה.',
				'data' => array( 'ptax.json' ),
				'related' => array( '/apartment-purchase-cost-calculator/' => 'עלות רכישה כוללת', '/mortgage-calculator/' => 'מחשבון משכנתא', '/real-estate-lawyer/' => 'עורך דין לקניית דירה', '/projects/hamedina/' => 'דירות במגדלי כיכר המדינה' ),
			),
			'pcost' => array(
				'name' => 'מחשבון עלות רכישה כוללת', 'cat' => 'FinanceApplication', 'kicker' => 'מחשבון · קניית דירה',
				'desc' => 'כמה כסף צריך באמת כדי לקנות דירה: מס רכישה לפי המסלול, עורך דין ותיווך עם מע״מ, שמאי, בדיקות ופתיחת תיק, מעבר ושיפוץ, וההון העצמי שנשאר אחרי המשכנתא, עם שיעור המימון המרבי של בנק ישראל.',
				'data' => array( 'ptax.json', 'cost.json' ),
				'related' => array( '/purchase-tax-calculator/' => 'מחשבון מס רכישה', '/mortgage-calculator/' => 'מחשבון משכנתא', '/buying-apartment/' => 'מדריך קניית דירה', '/projects/hamedina/' => 'דירות במגדלי כיכר המדינה' ),
			),
			'pval' => array(
				'name' => 'מחשבון שווי דירה', 'cat' => 'FinanceApplication', 'kicker' => 'מחשבון · שווי דירה',
				'desc' => 'כמה שווה דירה לפי העסקאות שנסגרו: המחיר החציוני לפי מספר החדרים בשכונה או בעיר (נתוני רשות המסים), עם התאמות למצב, לקומה ולבניין, טווח זהירות ובדיקת מחיר מבוקש, או חישוב לפי מחיר למ״ר.',
				'data' => array( 'value.json' ),
				'related' => array( '/apartment-prices/' => 'מחירון הדירות לפי עיר', '/purchase-tax-calculator/' => 'מחשבון מס רכישה', '/apartment-purchase-cost-calculator/' => 'עלות רכישה כוללת', '/projects/hamedina/' => 'דירות במגדלי כיכר המדינה' ),
			),
			'arnona' => array(
				'name' => 'מחשבון ארנונה תל אביב 2026', 'cat' => 'FinanceApplication', 'kicker' => 'מחשבון · ארנונה',
				'desc' => 'ארנונה למגורים בתל אביב-יפו לשנת 2026 לפי צו הארנונה של העירייה: אזור, סוג הבניין לפי שנת הבנייה, שטח הדירה עם המרפסות, הנחות ותשלום דו־חודשי.',
				'data' => array( 'arnona-tlv.json' ),
				'related' => array( '/apartment-purchase-cost-calculator/' => 'עלות רכישה כוללת', '/property-value-estimator/' => 'מחשבון שווי דירה', '/tel-aviv-apartment-prices/' => 'מחירי דירות בתל אביב', '/projects/hamedina/' => 'דירות במגדלי כיכר המדינה' ),
			),
			'nrm' => array(
				'only' => 'en', 'name' => 'Israeli mortgage calculator for non-residents', 'cat' => 'FinanceApplication', 'kicker' => 'Calculator · Israeli mortgage',
				'desc' => 'An Israeli mortgage for a buyer abroad: the 50% loan cap for non-residents, the monthly payment at the average rate by track, the purchase tax a foreign resident pays, the closing costs, and all of it in US dollars, euros or pounds at the Bank of Israel rate.',
				'data' => array( 'ptax.json', 'nrm.json', 'boi-fx.json' ),
				'related' => array( '/israel-purchase-tax-foreign-residents/' => 'Purchase tax for foreign residents', '/en/buy-property-in-israel/' => 'Buying a home in Israel from abroad', '/en/north-tel-aviv/' => 'North Tel Aviv', '/projects/hamedina-en/' => 'Kikar HaMedina towers' ),
			),
			'afford' => array(
				'name' => 'מחשבון כושר החזר: איזו דירה אפשר לקנות', 'cat' => 'FinanceApplication', 'kicker' => 'מחשבון · כושר החזר',
				'desc' => 'מחיר הדירה הגבוה ביותר שמשק בית יכול לקנות: ההחזר החודשי מול ההכנסה הפנויה (עד 50% לפי בנק ישראל) וההון העצמי מול המקדמה, מס הרכישה ועורך הדין, לפי שיעור המימון המרבי של כל מסלול.',
				'data' => array( 'ptax.json', 'cost.json', 'nrm.json' ),
				'related' => array( '/mortgage-calculator/' => 'מחשבון משכנתא', '/apartment-purchase-cost-calculator/' => 'עלות רכישה כוללת', '/purchase-tax-calculator/' => 'מחשבון מס רכישה', '/projects/hamedina/' => 'דירות במגדלי כיכר המדינה' ),
			),
			'dira' => array(
				'name' => 'דירה בהנחה: מה הסיכוי לזכות בהגרלה', 'cat' => 'FinanceApplication', 'kicker' => 'מחשבון · דירה בהנחה',
				'desc' => 'הסיכוי לזכות בהגרלות דירה בהנחה (מחיר למשתכן) לפי עיר, מהקובץ הרשמי של התוכנית: כמה נרשמו וכמה זכו בכל הגרלה, הדירות, המחיר למ״ר והיזם, גם במסלול בני מקום.',
				'data' => array( 'dira.json' ),
				'related' => array( '/mortgage-calculator/' => 'מחשבון משכנתא', '/mortgage-calculator/mortgage-repayment-capacity/' => 'כמה משכנתא אפשר לקחת', '/apartment-purchase-cost-calculator/' => 'עלות רכישה כוללת', '/apartment-prices/' => 'מחירי דירות בישראל' ),
			),
			/* 1.72.499 (HAD-592): the Greece family, one file tools/greece.js; data greece.json (facts with sources) + the BoI rate */
			'grbuy' => array(
				'file' => 'greece', 'name' => 'מחשבון עלות קניית דירה ביוון', 'cat' => 'FinanceApplication', 'kicker' => 'מחשבון · קניית דירה ביוון',
				'desc' => 'כמה כסף צריך להביא כדי לקנות דירה ביוון, ביורו ובשקלים: מס העברה 3.09% או מע״מ 24%, נוטריון לפי המדרגות, קדסטר, עורך דין ומתווך עם מע״מ יווני, משכנתא מבנק יווני, והשוואה להצעה של 15.45% לקונים מחוץ לאיחוד מ־1.7.2027.',
				'data' => array( 'greece.json', 'boi-fx.json' ),
				'related' => array( '/global/greece/' => 'נדל״ן ביוון', '/athens-apartments/' => 'דירה באתונה', '/acquisition-greece/' => 'קניית דירה ביוון', '/taxation-greece-israel/' => 'מיסוי דירה ביוון' ),
			),
			'grgv' => array(
				'file' => 'greece', 'name' => 'בדיקת זכאות לגולדן ויזה ביוון', 'cat' => 'UtilitiesApplication', 'kicker' => 'בדיקה · גולדן ויזה ביוון',
				'desc' => 'האם נכס ביוון מזכה בגולדן ויזה לפי החוק של 2024: הסף לפי אזור (800, 400 או 250 אלף אירו), נכס אחד של 120 מ״ר, איסור השכרה לטווח קצר, והאגרות לכל המשפחה.',
				'data' => array( 'greece.json', 'boi-fx.json' ),
				'related' => array( '/global/greece/' => 'נדל״ן ביוון', '/acquisition-greece/' => 'קניית דירה ביוון', '/athens-apartments/' => 'דירה באתונה' ),
			),
			'gryield' => array(
				'file' => 'greece', 'name' => 'מחשבון תשואה נטו לדירה ביוון', 'cat' => 'FinanceApplication', 'kicker' => 'מחשבון · תשואה ביוון',
				'desc' => 'כמה נשאר ביד מדירה מושכרת ביוון: שכירות ותפוסה, ניהול, דמי בניין וביטוח, ENFIA לפי טבלאות החוק, מס השכירות ביוון לפי מדרגות 2026, והמס בישראל בשלוש הדרכים: לפי האמנה, מסלול 15% ומסלול רגיל עם זיכוי.',
				'data' => array( 'greece.json', 'boi-fx.json' ),
				'related' => array( '/taxation-greece-israel/' => 'מיסוי דירה ביוון', '/athens-apartments/' => 'דירה באתונה', '/short-term-rentals-abroad/short-term-rentals-greece/' => 'השכרה לטווח קצר ביוון', '/investment-property-cashflow-calculator/' => 'תזרים דירה להשקעה' ),
			),
			/* 1.72.501 (HAD-592, Ben's Greece price list): the price family, one file tools/grprice.js; greece-prices.json (263 places, sources in the research), greece-map.json (Natural Earth) */
			'grmap' => array(
				'file' => 'grprice', 'name' => 'מפת מחירי הנדל״ן ביוון', 'cat' => 'ReferenceApplication', 'kicker' => 'מפה · מחירון יוון',
				'desc' => 'מפה של יוון עם המחיר המבוקש למ״ר ב־250 מקומות: אזורים, ערים, איים ושכונות באתונה ובסלוניקי. לחיצה על מקום מראה מחיר ביורו ובשקלים, דירה של 70 מ״ר, שכירות, תשואה, שינוי בשנה, סף הגולדן ויזה, אזור גבול והקפאת Airbnb, ואפשר להשוות שלושה מקומות.',
				'data' => array( 'greece-prices.json', 'greece-map.json', 'boi-fx.json' ),
				'related' => array( '/global/greece/' => 'נדל״ן ביוון', '/athens-apartments/' => 'מחירי אתונה לפי אזור', '/acquisition-greece/' => 'מחשבון עלות הקנייה', '/taxation-greece-israel/' => 'מיסוי דירה ביוון' ),
			),
			'grbudget' => array(
				'file' => 'grprice', 'name' => 'כמה מטרים מקבלים ביוון בכל תקציב', 'cat' => 'FinanceApplication', 'kicker' => 'מחשבון · מה מקבלים בתקציב',
				'desc' => 'תקציב ביורו או בשקלים, אחרי עלויות הקנייה ביוון: כמה מ״ר הוא קונה בכל אחד מ־250 המקומות, מהגדול לקטן, עם סף הגולדן ויזה בכל מקום.',
				'data' => array( 'greece-prices.json', 'boi-fx.json' ),
				'related' => array( '/acquisition-greece/' => 'עלויות הקנייה ביוון', '/global/greece/' => 'נדל״ן ביוון' ),
			),
			'grisrael' => array(
				'file' => 'grprice', 'name' => 'הדירה שלכם בישראל, ביוון', 'cat' => 'FinanceApplication', 'kicker' => 'השוואה · ישראל מול יוון',
				'desc' => 'המחיר החציוני הרשמי של דירה בעיר בישראל לפי מספר החדרים, ביורו לפי שער בנק ישראל, וכמה מ״ר הוא קונה בכל מקום ביוון אחרי עלויות הקנייה.',
				'data' => array( 'greece-prices.json', 'boi-fx.json', 'value.json' ),
				'related' => array( '/apartment-prices/' => 'מחירי הדירות בישראל', '/property-value-estimator/' => 'מחשבון שווי דירה' ),
			),
			/* 1.72.504 (HAD-592): the registered-contractor check, one file tools/pinkas.js; the search runs on the server (inc/pinkas.php), pinkas-meta.json is the small public part */
			'pinkas' => array(
				'file' => 'pinkas', 'name' => 'בדיקת קבלן רשום בפנקס הקבלנים', 'cat' => 'UtilitiesApplication', 'kicker' => 'חיפוש · פנקס הקבלנים',
				'desc' => 'חיפוש בכל 17,874 הקבלנים הרשומים בפנקס הקבלנים של משרד הבינוי והשיכון, לפי שם, מספר קבלן, ח״פ, עיר, ענף וסיווג. לכל קבלן: הענפים, הקבוצה והסיווג, הסכום שהסיווג מתיר באתר אחד לפי הטבלה שבתוקף, הגבלות, וקישור לרשומה הרשמית. בודק עבודה: האם החוק מחייב קבלן רשום ובאיזה סיווג.',
				'data' => array( 'pinkas-meta.json' ),
				'related' => array( '/professionals/' => 'מאגר בעלי המקצוע', '/renovation-contractor/' => 'קבלן שיפוצים', '/home-inspection/' => 'בדק בית', '/new-projects/construction-input-index/' => 'מדד תשומות הבנייה', '/new-projects/contractor-delay-compensation/' => 'פיצוי על איחור במסירה' ),
			),
			'sivug' => array(
				'file' => 'pinkas', 'name' => 'טבלת סיווג קבלנים: כמה מותר לכל סיווג', 'cat' => 'ReferenceApplication', 'kicker' => 'טבלה · סיווג קבלנים',
				'desc' => 'הסכום המרבי שקבלן רשום רשאי לבצע באתר אחד בכל קבוצה (א, ב, ג) ובכל סיווג (ק, 1 עד 5), לפי הטבלה הרשמית שבתוקף מ־1.10.2026 ועד 1.4.2027, ומה הסיווג שעבודה בסכום מסוים דורשת.',
				'data' => array( 'pinkas-meta.json' ),
				'related' => array( '/new-projects/construction-input-index/' => 'מדד תשומות הבנייה', '/professionals/' => 'מאגר בעלי המקצוע' ),
			),
		) );
	}

	function nadlan_nli_url( $rel ) { return plugins_url( 'assets/instruments/' . $rel, dirname( __DIR__ ) . '/nadlan-config.php' ); } // the plugin root, not inc/
	function nadlan_nli_ver() { return defined( 'NADLAN_CONFIG_VERSION' ) ? NADLAN_CONFIG_VERSION : '1'; }

	/** HAD-534 (d): the page language, 'en' on /en/ pages (inc/page-lang.php: the top ancestor slug), else 'he'. */
	function nadlan_nli_lang() { return function_exists( 'nadlan_pglang_lang' ) && 'en' === nadlan_pglang_lang() ? 'en' : 'he'; }
	/** A tool speaks the page language only when it carries that language block; otherwise it stays Hebrew (and RTL). */
	function nadlan_nli_tool_lang( $t ) { if ( ! empty( $t['only'] ) ) { return $t['only']; } return 'en' === nadlan_nli_lang() && ! empty( $t['en'] ) ? 'en' : 'he'; }  // 'only' (21.10.2026): an English tool inside an English post that sits on a Hebrew root path
	function nadlan_nli_t( $t, $lang ) { return 'en' === $lang && ! empty( $t['en'] ) ? array_merge( $t, $t['en'] ) : $t; }

	/** The ids of the tools in a post's content. */
	function nadlan_nli_ids_in( $content ) {
		if ( false === strpos( (string) $content, '[nadlan_tool' ) ) { return array(); }
		preg_match_all( '/\[nadlan_tool\s+id="([a-z0-9-]+)"/', $content, $m );
		return array_values( array_intersect( array_unique( $m[1] ), array_keys( nadlan_nli_tools() ) ) );
	}

	function nadlan_nli_page_ids() {
		static $ids = null;
		if ( null !== $ids ) { return $ids; }
		$ids = array();
		if ( is_singular() ) { $p = get_post(); if ( $p ) { $ids = nadlan_nli_ids_in( $p->post_content ); } }
		return $ids;
	}

	/** One official series as data for the summary. */
	function nadlan_nli_series( $file ) {
		$path = dirname( __DIR__ ) . '/assets/instruments/data/' . $file;
		if ( ! is_readable( $path ) ) { return null; }
		$d = json_decode( (string) file_get_contents( $path ), true );
		return is_array( $d ) && ! empty( $d['months'] ) ? $d : null;
	}

	add_action( 'wp_enqueue_scripts', function () {
		$ids = nadlan_nli_page_ids();
		if ( ! $ids ) { return; }
		$v = nadlan_nli_ver();
		$tl = nadlan_nli_tools(); $en_tool = false; foreach ( $ids as $x ) { if ( isset( $tl[ $x ]['only'] ) && 'en' === $tl[ $x ]['only'] ) { $en_tool = true; } }
		$fonts = ( 'en' === nadlan_nli_lang() || $en_tool )  // English pages: the Latin Plex faces (+ Plex Hebrew 400 for a Hebrew letter inside the page)
			? 'https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Sans+Condensed:wght@600&family=IBM+Plex+Sans+Hebrew:wght@400&family=IBM+Plex+Mono:wght@400;500&display=swap'
			: 'https://fonts.googleapis.com/css2?family=Karantina:wght@700&family=IBM+Plex+Sans+Hebrew:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap';
		wp_enqueue_style( 'nadlan-nli-fonts', $fonts, array(), null );
		wp_enqueue_style( 'nadlan-nli', nadlan_nli_url( 'core.css' ), array(), $v );
		wp_enqueue_script( 'nadlan-nli', nadlan_nli_url( 'core.js' ), array(), $v, true );
		// 1.72.499: tools of one family share a file ('file' => 'greece': grbuy, grgv, gryield ... in tools/greece.js), loaded once
		$files = array(); foreach ( $ids as $id ) { $files[ ! empty( $tl[ $id ]['file'] ) ? $tl[ $id ]['file'] : $id ] = 1; }
		foreach ( array_keys( $files ) as $f ) { wp_enqueue_script( 'nadlan-nli-' . $f, nadlan_nli_url( 'tools/' . $f . '.js' ), array( 'nadlan-nli' ), $v, true ); }
	}, 20 );

	add_filter( 'script_loader_tag', function ( $tag, $handle ) {
		return 0 === strpos( $handle, 'nadlan-nli' ) && false === strpos( $tag, ' defer' ) ? str_replace( ' src=', ' defer src=', $tag ) : $tag;
	}, 10, 2 );

	/** The summary printed before the script runs: the real numbers, for readers without JS, search engines and AI. */
	function nadlan_nli_summary( $id, $lang = 'he' ) {
		if ( 'en' === $lang ) { return nadlan_nli_summary_en( $id ); }
		if ( 'indexation' === $id ) {
			$d = nadlan_nli_series( 'cbs-200010.json' );
			if ( ! $d ) { return ''; }
			$ks = array_keys( $d['months'] ); $l = end( $ks ); $p = $ks[ count( $ks ) - 2 ];
			$y = ( (int) substr( $l, 0, 4 ) - 1 ) . substr( $l, 4 );
			$m1 = $d['months'][ $l ] / $d['months'][ $p ] - 1; $m12 = isset( $d['months'][ $y ] ) ? $d['months'][ $l ] / $d['months'][ $y ] - 1 : null;
			$lm = (int) substr( $l, 5 ) . '.' . substr( $l, 0, 4 );
			return '<p>מדד מחירי תשומה בבנייה למגורים, הנתון האחרון שפרסמה הלשכה המרכזית לסטטיסטיקה: ' . esc_html( $lm ) . '. שינוי בחודש: ' . esc_html( number_format( $m1 * 100, 1 ) ) . '%'
				. ( null !== $m12 ? '. שינוי ב־12 חודשים: ' . esc_html( number_format( $m12 * 100, 1 ) ) . '%' : '' ) . '. בחוזה מ־7.7.2022: 20% מהמחיר המשולמים בחתימה אינם צמודים, ומכל תשלום אחר מותר להצמיד עד מחצית, ורק עד מועד המסירה שבחוזה.</p>';
		}
		if ( 'cpi' === $id ) {
			$d = nadlan_nli_series( 'cbs-120010.json' );
			if ( ! $d ) { return ''; }
			$ks = array_keys( $d['months'] ); $l = end( $ks ); $p = $ks[ count( $ks ) - 2 ];
			$y = ( (int) substr( $l, 0, 4 ) - 1 ) . substr( $l, 4 );
			$m1 = $d['months'][ $l ] / $d['months'][ $p ] - 1; $m12 = isset( $d['months'][ $y ] ) ? $d['months'][ $l ] / $d['months'][ $y ] - 1 : null;
			return '<p>מדד המחירים לצרכן, הנתון האחרון שפרסמה הלשכה המרכזית לסטטיסטיקה: ' . esc_html( (int) substr( $l, 5 ) . '.' . substr( $l, 0, 4 ) ) . ' (בסיס ' . esc_html( $d['base'] ) . '). שינוי בחודש: ' . esc_html( number_format( $m1 * 100, 1 ) ) . '%'
				. ( null !== $m12 ? '. שינוי ב־12 חודשים: ' . esc_html( number_format( $m12 * 100, 1 ) ) . '%' : '' ) . '. המדד מתפרסם ב־15 בכל חודש, בשעה 18:30, עבור החודש הקודם.</p>';
		}
		if ( 'prime' === $id ) {
			$path = dirname( __DIR__ ) . '/assets/instruments/data/boi-rate.json';
			$b = is_readable( $path ) ? json_decode( (string) file_get_contents( $path ), true ) : null;
			if ( ! is_array( $b ) || empty( $b['changes'] ) ) { return ''; }
			$c = $b['changes']; $l = end( $c );
			return '<p>ריבית בנק ישראל: ' . esc_html( number_format( (float) $b['rate'], 2 ) ) . '%. ריבית הפריים: ' . esc_html( number_format( (float) $b['prime'], 2 ) ) . '% (ריבית בנק ישראל ועוד 1.5%). בתוקף מ־'
				. esc_html( date_i18n( 'j.n.Y', strtotime( $l['from'] ) ) ) . ', לפי בנק ישראל, נכון ל־' . esc_html( date_i18n( 'j.n.Y', strtotime( $b['asof'] ) ) ) . '.</p>';
		}
		if ( 'warranty' === $id ) {
			return '<p>לפי חוק המכר (דירות): תקופת הבדק מתחילה ביום מסירת הדירה ונמשכת בין שנה ל־7 שנים לפי סוג הליקוי (צנרת ואיטום 4 שנים, סדקים מעל 1.5 מ״מ 5 שנים, חיפויי חוץ 7 שנים), ואחריה 3 שנות אחריות. ליקוי יסודי בנשיאת המבנה: 20 שנה. ליקוי שנראה כבר במסירה: מודיעים לקבלן תוך שנה.</p>';
		}
		if ( 'soilmap' === $id || 'pfas' === $id ) {
			$path = dirname( __DIR__ ) . '/assets/instruments/data/sde-dov-soil.json';
			$s = is_readable( $path ) ? json_decode( (string) file_get_contents( $path ), true ) : null;
			if ( ! is_array( $s ) || empty( $s['records'] ) ) { return ''; }
			$rep = array_values( array_filter( $s['records'], function ( $r ) { return 'published_report' === $r['status'] && ! empty( $r['pfosMax'] ); } ) );
			usort( $rep, function ( $a, $b ) { return $b['pfosX'] <=> $a['pfosX']; } );
			$holes = 0; $over = 0; foreach ( $rep as $r ) { $holes += (int) $r['holes']; $over += (int) $r['pfosHoles']; }
			$th = $s['thresholds'];
			$p = '<p>לפי דו"חות סקרי הקרקע שפורסמו במאגר המשרד להגנת הסביבה, נכון ל־' . esc_html( date_i18n( 'j.n.Y', strtotime( $s['built'] ) ) ) . ': ' . count( $rep ) . ' מגרשים בשדה דב עם דו"ח, ' . $over . ' מתוך ' . $holes
				. ' קידוחים עם ערך PFOS מעל ערך הסף. הערך הגבוה: מגרש ' . esc_html( $rep[0]['plot'] ) . ', פי ' . esc_html( number_format( $rep[0]['pfosX'] ) ) . ' מערך הסף למגע ישיר (PFOS ' . esc_html( number_format( $th['pfos'], 1 ) ) . ' ננוגרם לק"ג).</p>';
			if ( 'pfas' === $id ) { return $p; }
			$p .= '<table><thead><tr><th>מגרש</th><th>שיא PFOS (ננוגרם לק"ג)</th><th>פי כמה מהסף</th><th>קידוחים מעל ערך הסף</th></tr></thead><tbody>';
			foreach ( $rep as $r ) { $p .= '<tr><td>' . esc_html( $r['plot'] ) . '</td><td>' . esc_html( number_format( $r['pfosMax'] ) ) . '</td><td>' . esc_html( number_format( $r['pfosX'], $r['pfosX'] < 10 ? 1 : 0 ) ) . '</td><td>' . (int) $r['pfosHoles'] . ' מתוך ' . (int) $r['holes'] . '</td></tr>'; }
			return $p . '</tbody></table>';
		}
		if ( 'soilask' === $id ) {
			return '<p>השאלות שכדאי לשאול את היזם על הקרקע במגרש בשדה דב: האם המגרש נדגם לפי ההנחיות של המשרד להגנת הסביבה מ־12.2.2026; את דו"ח סקר הקרקע המלא; האם המשרד אימץ את הממצאים בכתב; אם נמצאה חריגה, האם תכנית הטיפול אושרה; האם הטיפול עלול לדחות את מועד המסירה; מי נושא בעלות; ואילו תנאים יש בהיתר.</p>';
		}
		if ( 'afford' === $id ) {
			return '<p>כמה דירה אפשר לקנות: לפי בנק ישראל ההחזר החודשי של משכנתא לא יעלה על 50% מההכנסה הפנויה, ורוב הבנקים מעדיפים עד 35% עד 40%. הבנק מממן עד 75% מהשווי בדירה יחידה ועד 50% בדירה נוספת או לתושב חוץ, ואת השאר, יחד עם מס הרכישה ועורך הדין, צריך להביא מההון העצמי. לדוגמה, משק בית עם הכנסה נטו של 25,000 ₪, החזר של 35% מההכנסה וריבית של 4.62% ל־25 שנה, יכול לקחת משכנתא של כ־1,555,000 ₪.</p>';
		}
		if ( 'dira' === $id ) { // site gap #3: the town ranking from the official lottery file, for readers without scripts and for search engines
			$path = dirname( __DIR__ ) . '/assets/instruments/data/dira.json';
			$x = is_readable( $path ) ? json_decode( (string) file_get_contents( $path ), true ) : null;
			if ( ! is_array( $x ) || empty( $x['towns'] ) ) { return ''; }
			$rank = array();
			foreach ( $x['towns'] as $town => $rows ) {
				$odds = array(); $subs = 0; $wins = 0;
				foreach ( $rows as $r ) { if ( $r[5] > 0 ) { $odds[] = $r[6] / $r[5]; $subs += $r[5]; $wins += $r[6]; } }
				if ( count( $odds ) < 3 ) { continue; }
				sort( $odds ); $n = count( $odds ); $m = $n % 2 ? $odds[ intdiv( $n, 2 ) ] : ( $odds[ $n / 2 - 1 ] + $odds[ $n / 2 ] ) / 2;
				$rank[] = array( $town, $n, $subs, $wins, $m );
			}
			usort( $rank, function ( $a, $b ) { return $b[4] <=> $a[4]; } );
			$rows = '';
			foreach ( $rank as $r ) { $rows .= '<tr><td>' . esc_html( $r[0] ) . '</td><td>' . (int) $r[1] . '</td><td>' . esc_html( number_format( $r[2] ) ) . '</td><td>' . esc_html( number_format( $r[3] ) ) . '</td><td>' . esc_html( number_format( 100 * $r[4], $r[4] < 0.01 ? 2 : 1 ) ) . '%</td></tr>'; }
			return '<p>בהגרלות דירה בהנחה (מחיר למשתכן) זכו ' . esc_html( number_format( 100 * $x['wins'] / max( 1, $x['subs'] ), 2 ) ) . ' על כל 100 נרשמים, לפי הקובץ הרשמי של התוכנית (' . (int) $x['n'] . ' הגרלות, עודכן ' . esc_html( date_i18n( 'j.n.Y', strtotime( $x['updated'] ) ) ) . '). הסיכוי בהגרלה טיפוסית בכל עיר, מהגבוה לנמוך (ערים עם 3 הגרלות ומעלה):</p><table><thead><tr><th>עיר</th><th>הגרלות</th><th>נרשמים</th><th>זוכים</th><th>סיכוי</th></tr></thead><tbody>' . $rows . '</tbody></table>';
		}
		if ( 'arnona' === $id ) {
			return '<p>ארנונה למגורים בתל אביב-יפו לשנת 2026, לפי צו הארנונה של העירייה (₪ למ״ר לשנה), בבניין שהושלם מ־2022 ואילך: אזור 1, דירה עד 140 מ״ר 112.99 ומעל 140 מ״ר 139.60; אזור 2, 90.71 ו־108.98; אזור 3, 78.39; אזורים 4 ו־5, 64.42. מעל 140 מ״ר כל הדירה מחויבת בתעריף הגבוה. מרפסות נכללות בשטח, חניה לא. עולה חדש: 50% על עד 100 מ״ר ל־12 חודשים.</p>';
		}
		if ( 'pval' === $id ) {
			$path = dirname( __DIR__ ) . '/assets/instruments/data/value.json';
			$x = is_readable( $path ) ? json_decode( (string) file_get_contents( $path ), true ) : null;
			if ( ! is_array( $x ) || empty( $x['cities'] ) ) { return ''; }
			$rows = '';
			foreach ( $x['cities'] as $name => $c ) { $rows .= '<tr><td>' . esc_html( $name ) . '</td><td>' . ( $c['r3'] ? esc_html( number_format( $c['r3'] ) ) : '-' ) . '</td><td>' . ( $c['r4'] ? esc_html( number_format( $c['r4'] ) ) : '-' ) . '</td><td>' . ( $c['r5'] ? esc_html( number_format( $c['r5'] ) ) : '-' ) . '</td></tr>'; }
			return '<p>המחיר החציוני של דירות שנמכרו לפי מספר החדרים, ברבעון האחרון שפורסם לכל עיר (ברובן 1-3.2026), לפי נתוני רשות המסים (₪):</p><table><thead><tr><th>עיר</th><th>3 חדרים</th><th>4 חדרים</th><th>5 חדרים</th></tr></thead><tbody>' . $rows . '</tbody></table>';
		}
		if ( 'pcost' === $id ) {
			return '<p>מה נכנס לעלות של קניית דירה מעבר למחיר: מס רכישה לפי המדרגות של רשות המסים (בדירה יחידה אין מס עד 1,978,745 ₪), עורך דין בדרך כלל 0.5% עד 1% מהמחיר ותיווך מקובל 2%, שניהם ועוד מע״מ 18%, שמאי לבנק 350 עד 950 ₪, בדק בית 1,500 עד 2,500 ₪, ופתיחת תיק משכנתא עד 360 ₪. בנק ישראל מאפשר משכנתא עד 75% משווי דירה יחידה ועד 50% בדירה נוספת או לתושב חוץ.</p>';
		}
		if ( 'ptax' === $id ) {
			$path = dirname( __DIR__ ) . '/assets/instruments/data/ptax.json';
			$x = is_readable( $path ) ? json_decode( (string) file_get_contents( $path ), true ) : null;
			if ( ! is_array( $x ) || empty( $x['tracks']['single'] ) ) { return ''; }
			$fmt = function ( $br ) { $o = array(); $lo = 0; foreach ( $br as $b ) { $o[] = number_format( $b[1] * 100, $b[1] * 100 == (int) ( $b[1] * 100 ) ? 0 : 1 ) . '% ' . ( null === $b[0] ? 'מעל ' . number_format( $lo ) . ' ₪' : 'עד ' . number_format( $b[0] ) . ' ₪' ); $lo = $b[0]; } return implode( ', ', $o ); };
			// 1.72.500: each track with its own end date (instruction 1/2026): the only-home brackets are frozen, the additional-home rate is a temporary order
			$vu = isset( $x['valid'] ) ? $x['valid'] : array( 'single' => $x['frozen_until'], 'extra' => $x['frozen_until'] );
			return '<p>מדרגות מס רכישה על דירת מגורים לפי רשות המסים (הוראת ביצוע 1/2026). דירה יחידה, מוקפאות עד ' . esc_html( date_i18n( 'j.n.Y', strtotime( $vu['single'] ) ) ) . ': ' . esc_html( $fmt( $x['tracks']['single'] ) )
				. '. דירה נוספת, תושב חוץ וחברה, הוראת שעה עד ' . esc_html( date_i18n( 'j.n.Y', strtotime( $vu['extra'] ) ) ) . ': ' . esc_html( $fmt( $x['tracks']['extra'] ) ) . '. עולה חדש (תקנה 12א, עד 20,183,565 ₪): ' . esc_html( $fmt( $x['tracks']['oleh'] ) )
				. '. נכה (תקנה 11): 0.5%, ובדירה יחידה עד 2,500,000 ₪ פטור עד המדרגה הראשונה. קרקע ונכס שאינו מגורים: 6%. מתנה לקרוב: שליש מהמס. משפרי דיור נחשבים דירה יחידה אם ימכרו את הדירה הקודמת תוך 24 חודשים (רכישה מ־1.6.2025). המס מחושב על שווי הדירה כולה, וקונה של חלק משלם לפי החלק שלו.</p>';
		}
		if ( 'grbuy' === $id ) {
			return '<p>עלויות קניית דירה ביוון, לפי החוק באוקטובר 2026: מס העברה 3.09% על המחיר או על השווי האובייקטיבי, הגבוה מביניהם, ומשלם הקונה לפני החתימה. בדירה חדשה מע״מ 24%, או 3.09% אם היזם ביקש השעיה (בתוקף עד 31.12.2026). נוטריון 0.8% עד 120,000 אירו, 0.7% עד 380,000 ו־0.65% עד 2 מיליון, ועוד 20 אירו ומע״מ 24%. רישום בקדסטר 0.5% ועוד 20 אירו. עורך דין לרוב 0.5% עד 1.5% ומתווך כ־2%, שניהם ועוד מע״מ 24%. סך העלויות כ־5.8% בלי מתווך וכ־8.3% עם מתווך. משרד האוצר היווני הציע מס העברה של 15.45% לקונים פרטיים שתושבי המס שלהם מחוץ לאיחוד, כולל ישראלים, בחוזים מ־1.7.2027; זו הצעת חוק בהערות ציבור עד 1.11.2026.</p>';
		}
		if ( 'grgv' === $id ) {
			return '<p>גולדן ויזה ביוון לפי חוק 5100/2024: 800,000 אירו באטיקה, ביחידת סלוניקי, במיקונוס, בסנטוריני ובכל אי עם יותר מ־3,100 תושבים (כולל כרתים, רודוס וקורפו); 400,000 אירו בשאר יוון; בשני המסלולים נכס אחד של 120 מ״ר לפחות. 250,000 אירו רק בהסבה של נכס מסחרי למגורים או בשיקום מבנה לשימור. נכס של גולדן ויזה אסור בהשכרה לטווח קצר (קנס 50,000 אירו וביטול ההיתר). ההיתר ל־5 שנים ומתחדש; אגרה 2,000 אירו למבקש ו־150 אירו לכל בן משפחה.</p>';
		}
		if ( 'gryield' === $id ) {
			return '<p>מס על שכירות ביוון מ־2026, גם למי שלא גר ביוון, אחרי ניכוי קבוע של 5%: 15% עד 12,000 אירו בשנה, 25% עד 24,000, 35% עד 36,000 ו־45% מעל. ENFIA, מס הרכוש השנתי, לפי השטח ומחיר האזור: מ־2 עד 16.20 אירו למ״ר, כפול מקדמי הגיל והקומה, עם הנחה של 20% לדירה מבוטחת. בישראל: לפי הנוסח האנגלי של אמנת המס, השכירות חייבת במס רק ביוון; רשות המסים לא פרסמה עמדה. מי שמשלם בישראל בוחר בין מסלול 15% על השכירות (בלי הוצאות ובלי זיכוי) למסלול רגיל לפי המדרגות, עם זיכוי על המס ששולם ביוון.</p>';
		}
		if ( in_array( $id, array( 'grmap', 'grbudget', 'grisrael' ), true ) ) {  // 1.72.501: the whole Greece price list as plain text, for readers without scripts, search engines and AI answers
			$path = dirname( __DIR__ ) . '/assets/instruments/data/greece-prices.json';
			$g = is_readable( $path ) ? json_decode( (string) file_get_contents( $path ), true ) : null;
			if ( ! is_array( $g ) || empty( $g['places'] ) ) { return ''; }
			$pl = array_values( array_filter( $g['places'], function ( $p ) { return 'none' !== $p['z']; } ) );
			usort( $pl, function ( $a, $b ) { return $b['m2'] <=> $a['m2']; } );
			$n = $g['national'];
			$p0 = '<p>המחיר המבוקש הממוצע לדירה ביוון: ' . number_format( $n['m2'] ) . ' אירו למ״ר (' . esc_html( $n['src'] . ', ' . $n['per'] ) . ', ' . ( $n['yoy'] >= 0 ? '+' : '' ) . esc_html( number_format( 100 * $n['yoy'], 1 ) ) . '% בשנה), ושכירות של ' . esc_html( number_format( $n['rent'], 2 ) ) . ' אירו למ״ר לחודש. מחירים מבוקשים במודעות; בעסקאות נסגר לרוב פחות.</p>';
			$by = array(); foreach ( $pl as $p ) { $by[ $p['id'] ] = $p; }
			$m2 = function ( $eur, $id ) use ( $by ) { return isset( $by[ $id ] ) ? number_format( $eur / 1.0826 / $by[ $id ]['m2'] ) : ''; };
			if ( 'grbudget' === $id ) {
				return '<p>מה מקבלים ביוון בתקציב של 150,000 אירו, אחרי עלויות קנייה של כ־8.3%: כ־' . $m2( 150000, 'ath-centre' ) . ' מ״ר במרכז אתונה, ' . $m2( 150000, 'thess-municipality' ) . ' מ״ר בסלוניקי, '
					. $m2( 150000, 'chania' ) . ' מ״ר בחאניה ו־' . $m2( 150000, 'mykonos' ) . ' מ״ר במיקונוס, לפי המחיר המבוקש למ״ר בכל מקום.</p>';
			}
			if ( 'grisrael' === $id ) {
				return '<p>הדירה שלכם בישראל, ביוון: המחשבון לוקח את המחיר החציוני הרשמי של דירה בעיר בישראל לפי מספר החדרים (רשות המסים), ממיר אותו ליורו לפי שער בנק ישראל, מוריד את עלויות הקנייה ביוון, ומראה כמה מ״ר הוא קונה בכל אחד מ־' . count( $pl ) . ' המקומות.</p>';
			}
			$gv = function ( $c ) { return 800 === $c ? '800,000 €' : ( 400 === $c ? '400,000 €' : ( 0 === $c ? 'לפי המקום' : 'לבדיקה' ) ); };
			$rows = '';
			foreach ( $pl as $p ) {
				$rows .= '<tr><td>' . esc_html( $p['he'] ) . '</td><td>' . number_format( $p['m2'] ) . '</td><td>' . ( isset( $p['yoy'] ) && null !== $p['yoy'] ? esc_html( number_format( 100 * $p['yoy'], 1 ) ) . '%' : '' ) . '</td><td>' . ( isset( $p['rent'] ) ? esc_html( number_format( $p['rent'], 1 ) ) : '' ) . '</td><td>' . ( isset( $p['y'] ) ? esc_html( number_format( 100 * $p['y'], 1 ) ) . '%' : '' ) . '</td><td>' . esc_html( $gv( $p['gv'] ) ) . '</td><td>' . esc_html( $p['src'] . ', ' . $p['per'] ) . '</td></tr>';
			}
			return $p0 . '<table><caption>מחירון נדל״ן ביוון: ' . count( $pl ) . ' מקומות, מחיר מבוקש באירו למ״ר</caption><thead><tr><th>מקום</th><th>אירו למ״ר</th><th>שינוי בשנה</th><th>שכירות למ״ר לחודש</th><th>תשואה ברוטו</th><th>גולדן ויזה</th><th>מקור ותקופה</th></tr></thead><tbody>' . $rows . '</tbody></table>';
		}
		if ( 'pinkas' === $id || 'sivug' === $id ) {  // 1.72.504: the rules and the table in force as plain text (the search itself needs the script)
			$path = dirname( __DIR__ ) . '/assets/instruments/data/pinkas-meta.json';
			$m = is_readable( $path ) ? json_decode( (string) file_get_contents( $path ), true ) : null;
			if ( ! is_array( $m ) || empty( $m['table'] ) ) { return ''; }
			$t = $m['table']; $d = function ( $s ) { return date_i18n( 'j.n.Y', strtotime( $s ) ); };
			$amt = function ( $v ) { return $v ? number_format( $v ) . ' אלף ₪' : 'ללא הגבלה'; };
			$tab = '<table><caption>טבלת סיווג הקבלנים בתוקף מ־' . esc_html( $d( $t['from'] ) ) . ' עד ' . esc_html( $d( $t['to'] ) ) . ': הסכום המרבי באתר אחד, לפני מע״מ</caption><thead><tr><th>סיווג</th><th>קבוצה א</th><th>קבוצה ב</th><th>קבוצה ג</th><th>בנייה למגורים</th></tr></thead><tbody>';
			foreach ( array( 'ק', '1', '2', '3', '4', '5' ) as $lv ) {
				$tab .= '<tr><td>' . $lv . '</td><td>' . ( isset( $t['א'][ $lv ] ) ? $amt( $t['א'][ $lv ] ) : '' ) . '</td><td>' . ( isset( $t['ב'][ $lv ] ) ? $amt( $t['ב'][ $lv ] ) : '' ) . '</td><td>' . ( isset( $t['ג'][ $lv ] ) ? $amt( $t['ג'][ $lv ] ) : '' ) . '</td><td>'
					. ( isset( $t['sqm'][ $lv ] ) ? ( $t['sqm'][ $lv ] ? number_format( $t['sqm'][ $lv ] ) . ' מ״ר' : 'ללא הגבלה' ) : '' ) . '</td></tr>';
			}
			$tab .= '</tbody></table>';
			if ( 'sivug' === $id ) { return '<p>סיווג ק קיים רק בענף השיפוצים (131). הסכומים מתעדכנים ב־1 באפריל וב־1 באוקטובר לפי מדד תשומות הבנייה למגורים.</p>' . $tab; }
			$s = $m['stats'];
			return '<p>בפנקס הקבלנים של משרד הבינוי והשיכון רשומים ' . number_format( $s['contractors'] ) . ' קבלנים (' . number_format( $s['companies'] ) . ' חברות) ב־' . number_format( $s['cities'] ) . ' ערים ויישובים וב־' . (int) $s['branches']
				. ' ענפים, לפי המאגר הפתוח ב־data.gov.il נכון ל־' . esc_html( $d( $m['asof'] ) ) . '. עבודה בענף ראשי בהיקף של יותר מ־' . number_format( $m['thr']['main'] ) . ' ₪, או בענף משנה, למשל שיפוצים, ביותר מ־' . number_format( $m['thr']['sub'] )
				. ' ₪, מותרת רק לקבלן רשום. לפני חתימה בודקים ברשומה הרשמית של הקבלן ב־gov.il שהוא רשום בענף הנכון, שהסיווג שלו מכסה את העבודה, ושהוא לא מוקפא, מוחרג או מותלה.</p>' . $tab;
		}
		if ( 'delay' === $id ) {
			return '<p>פיצוי על איחור במסירה לפי סעיף 5א לחוק המכר (דירות): בחוזה מ־7.7.2022, אחרי חודש חסד, דמי שכירות של דירה דומה בחודשים 2 עד 4, דמי שכירות כפול 1.25 בחודשים 5 עד 10, וכפול 1.5 מהחודש ה־11. בחוזה עד 6.7.2022, כשהאיחור עובר 60 ימים, דמי שכירות כפול 1.5 מהמועד שבחוזה ועד סוף החודש השמיני, ומהחודש התשיעי כפול 1.25.</p>';
		}
		return '';
	}

	/** HAD-534 (d): the same summaries in English, for the tools that carry an 'en' block. Dates with gmdate (English month
	 *  names whatever the site locale). The same numbers as the Hebrew, from the same data file. */
	function nadlan_nli_summary_en( $id ) {
		if ( 'nrm' === $id ) {
			$path = dirname( __DIR__ ) . '/assets/instruments/data/boi-fx.json';
			$x = is_readable( $path ) ? json_decode( (string) file_get_contents( $path ), true ) : null;
			$fx = is_array( $x ) && ! empty( $x['fx']['USD'] ) ? ' Bank of Israel representative rates on ' . esc_html( $x['fx']['USD']['date'] ) . ': 1 USD = ' . esc_html( $x['fx']['USD']['rate'] ) . ' ILS, 1 EUR = ' . esc_html( $x['fx']['EUR']['rate'] ) . ' ILS, 1 GBP = ' . esc_html( $x['fx']['GBP']['rate'] ) . ' ILS.' : '';
			return '<p>An Israeli bank can lend a non-resident up to 50% of the property value. A foreign resident pays purchase tax of 8% up to ILS 6,055,070 and 10% above. The average rate on new fixed, non-linked mortgages was 4.62% in August 2026.' . $fx . '</p>';
		}
		if ( 'soilmap' === $id || 'pfas' === $id ) {
			$path = dirname( __DIR__ ) . '/assets/instruments/data/sde-dov-soil.json';
			$s = is_readable( $path ) ? json_decode( (string) file_get_contents( $path ), true ) : null;
			if ( ! is_array( $s ) || empty( $s['records'] ) ) { return ''; }
			$rep = array_values( array_filter( $s['records'], function ( $r ) { return 'published_report' === $r['status'] && ! empty( $r['pfosMax'] ); } ) );
			usort( $rep, function ( $a, $b ) { return $b['pfosX'] <=> $a['pfosX']; } );
			$holes = 0; $over = 0; foreach ( $rep as $r ) { $holes += (int) $r['holes']; $over += (int) $r['pfosHoles']; }
			$th = $s['thresholds'];
			$p = '<p>According to the soil survey reports published in the Ministry of Environmental Protection database, as of ' . esc_html( gmdate( 'j M Y', strtotime( $s['built'] . ' UTC' ) ) ) . ': ' . count( $rep ) . ' plots in Sde Dov with a report, ' . $over . ' of ' . $holes
				. ' boreholes with a PFOS value above the threshold. The highest value: plot ' . esc_html( $rep[0]['plot'] ) . ', ' . esc_html( number_format( $rep[0]['pfosX'] ) ) . ' times the direct-contact threshold (PFOS ' . esc_html( number_format( $th['pfos'], 1 ) ) . ' ng/kg).</p>';
			if ( 'pfas' === $id ) { return $p; }
			$p .= '<table><thead><tr><th>Plot</th><th>PFOS peak (ng/kg)</th><th>Times the threshold</th><th>Boreholes above the threshold</th></tr></thead><tbody>';
			foreach ( $rep as $r ) { $p .= '<tr><td>' . esc_html( $r['plot'] ) . '</td><td>' . esc_html( number_format( $r['pfosMax'] ) ) . '</td><td>' . esc_html( number_format( $r['pfosX'], $r['pfosX'] < 10 ? 1 : 0 ) ) . '</td><td>' . (int) $r['pfosHoles'] . ' of ' . (int) $r['holes'] . '</td></tr>'; }
			return $p . '</tbody></table>';
		}
		if ( 'soilask' === $id ) {
			return '<p>The questions to ask the developer about the soil on a Sde Dov plot: whether the plot was sampled under the Ministry of Environmental Protection guidelines of 12 Feb 2026; the full soil survey report; whether the Ministry adopted the findings in writing; if an exceedance was found, whether the treatment plan was approved; whether the treatment could delay the delivery date; who bears the cost; and what conditions the permit sets.</p>';
		}
		return '';
	}

	add_shortcode( 'nadlan_tool', function ( $atts ) {
		$a = shortcode_atts( array( 'id' => '' ), $atts );
		$set = array(); // the page's own case: [nadlan_tool id="pval" city="ירושלים" hood="65209775" rooms="4"], [nadlan_tool id="dira" town="חיפה"]
		foreach ( array( 'city', 'hood', 'town', 'rooms', 'track', 'period', 'method', 'preset', 'region', 'kind', 'price' ) as $k ) { if ( isset( $atts[ $k ] ) && '' !== $atts[ $k ] ) { $set[ $k ] = in_array( $k, array( 'rooms', 'price' ), true ) ? (int) $atts[ $k ] : sanitize_text_field( $atts[ $k ] ); } }  // 1.72.498: preset (a ready case of the tool), region, kind, price
		$tools = nadlan_nli_tools();
		$id = sanitize_key( $a['id'] );
		if ( ! isset( $tools[ $id ] ) ) { return ''; }
		$lang = nadlan_nli_tool_lang( $tools[ $id ] ); $en = 'en' === $lang;  // HAD-534 (d): English + LTR on /en/ pages, for tools with an 'en' block
		$t = nadlan_nli_t( $tools[ $id ], $lang );
		$data = implode( ',', array_map( function ( $f ) { return esc_url( nadlan_nli_url( 'data/' . $f ) . '?ver=' . nadlan_nli_ver() ); }, $t['data'] ) );
		$h = '<section class="nli" dir="' . ( $en ? 'ltr' : 'rtl' ) . '" lang="' . $lang . '" aria-label="' . esc_attr( $t['name'] ) . '"><div class="nli-host" data-nli="' . esc_attr( $id ) . '"' . ( $data ? ' data-nli-data="' . $data . '"' : '' ) . ( $set ? ' data-nli-set="' . esc_attr( wp_json_encode( $set, JSON_UNESCAPED_UNICODE ) ) . '"' : '' ) . '>'
			. '<div class="nli__panel"><p class="nli__kicker">' . esc_html( isset( $t['kicker'] ) ? $t['kicker'] : ( $en ? 'Calculator' : 'מחשבון' ) ) . '</p><h2 class="nli__title">' . esc_html( $t['name'] ) . '</h2>' . nadlan_nli_summary( $id, $lang ) . '</div></div>';
		if ( ! empty( $t['related'] ) ) {
			$h .= $en ? '<nav class="nli__rel" aria-label="Related tools and guides"><span>Related:</span>' : '<nav class="nli__rel" aria-label="כלים קשורים"><span>כלים קשורים:</span>';
			foreach ( $t['related'] as $path => $label ) { $h .= ' <a href="' . esc_url( home_url( $path ) ) . '">' . esc_html( $label ) . '</a>'; }
			$h .= '</nav>';
		}
		return $h . '</section>';
	} );

	/** FAQPage from the page's own "שאלות נפוצות" section (h3 question, then its paragraphs), for search engines and AI answers. */
	function nadlan_nli_faq( $html ) {
		$html = preg_replace( '/<!--.*?-->/s', '', (string) $html );
		if ( ! preg_match( '/<h2[^>]*>\s*(?:שאלות נפוצות|Frequently asked questions)[^<]{0,60}<\/h2>(.*?)(?=<h2|$)/su', $html, $m ) ) { return array(); }
		preg_match_all( '/<h3[^>]*>(.*?)<\/h3>\s*((?:<p[^>]*>.*?<\/p>\s*)+)/su', $m[1], $qa, PREG_SET_ORDER );
		$out = array();
		foreach ( $qa as $x ) { $q = trim( wp_strip_all_tags( $x[1] ) ); $a = trim( preg_replace( '/\s+/u', ' ', wp_strip_all_tags( $x[2] ) ) ); if ( $q && $a ) { $out[] = array( '@type' => 'Question', 'name' => $q, 'acceptedAnswer' => array( '@type' => 'Answer', 'text' => $a ) ); } }
		return count( $out ) >= 2 ? $out : array();
	}

	add_action( 'wp_head', function () {
		$ids = nadlan_nli_page_ids();
		if ( ! $ids ) { return; }
		$tools = nadlan_nli_tools(); $out = array();
		foreach ( $ids as $id ) {
			$lang = nadlan_nli_tool_lang( $tools[ $id ] ); $t = nadlan_nli_t( $tools[ $id ], $lang );  // HAD-534 (d): name, description and inLanguage follow the page
			$out[] = array( '@type' => 'SoftwareApplication', 'name' => $t['name'], 'description' => $t['desc'], 'applicationCategory' => $t['cat'], 'operatingSystem' => 'Any',
				'inLanguage' => $lang, 'url' => get_permalink(), 'isAccessibleForFree' => true, 'offers' => array( '@type' => 'Offer', 'price' => '0', 'priceCurrency' => 'ILS' ),
				'publisher' => array( '@type' => 'Organization', 'name' => 'nad-lan.co.il', 'url' => home_url( '/' ) ) );
		}
		$p = get_post(); $faq = $p ? nadlan_nli_faq( $p->post_content ) : array();
		if ( $faq ) { $out[] = array( '@type' => 'FAQPage', 'url' => get_permalink(), 'mainEntity' => $faq ); }
		echo '<script type="application/ld+json" id="nadlan-nli-ld">' . wp_json_encode( array( '@context' => 'https://schema.org', '@graph' => $out ), JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES ) . '</script>' . "\n";
	}, 30 );
}

/* ---------------------------------------------------------------------------------------------------------------------
 * AI and search-engine discovery (1.72.498, HAD-592, Ben 22.10.2026: "make sure they index on all the search engines and
 * on the AI bots"). Two public files, nothing else changes:
 *  - /llms.txt: a reading list for AI assistants (the llms.txt convention): what the site is, where the official numbers
 *    come from, and links to the calculators, price pages, guides and projects. The tool pages are found by their
 *    [nadlan_tool] shortcode, so a new tool page joins the list by itself (cached 6 hours).
 *  - /<key>.txt: the IndexNow key file. IndexNow tells Bing, Yandex, Seznam and Naver about a new or changed URL at once;
 *    the publishing scripts post the URLs to https://api.indexnow.org with this key (the key is public by design).
 * robots.txt already allows every crawler (checked 22.10.2026); it is not touched here.
 * ------------------------------------------------------------------------------------------------------------------- */
if ( ! defined( 'NADLAN_INDEXNOW_KEY' ) ) { define( 'NADLAN_INDEXNOW_KEY', 'f25cb29869da9a9709dedcde8a7efc7a' ); }

if ( ! function_exists( 'nadlan_llms_txt' ) ) {
	function nadlan_llms_txt() {
		$cached = get_transient( 'nadlan_llms_txt_v1' );
		if ( is_string( $cached ) && '' !== $cached ) { return $cached; }
		global $wpdb;
		$line = function ( $id, $desc = '' ) {
			$t = trim( html_entity_decode( wp_strip_all_tags( get_the_title( $id ) ), ENT_QUOTES, 'UTF-8' ) );
			return '- [' . $t . '](' . get_permalink( $id ) . ')' . ( '' !== $desc ? ': ' . $desc : '' ) . "\n";
		};
		$by_path = function ( $path ) { $p = get_page_by_path( trim( $path, '/' ) ); return ( $p && 'publish' === $p->post_status ) ? $p->ID : 0; };
		$o  = "# nad-lan.co.il (נדל\"ן)\n\n";
		$o .= "> Israeli real-estate portal, Hebrew first with English, French, Russian and Arabic pages: new building projects, official apartment prices by city and neighbourhood, free calculators (purchase tax, total purchase cost, home value, mortgage, arnona, index linkage), buying and selling guides, and guides to buying property abroad for Israelis. Prices come from the deals reported to the Israel Tax Authority (data.nadlan.gov.il) and other official sources, each with its date on the page.\n\n";
		$o .= "Notes for assistants: numbers on the pages are dated; quote the date with the number. Calculators open on a worked example and recompute in the browser; the page also prints the key figures as plain text.\n\n";
		$o .= "## Calculators\n";
		$tools = function_exists( 'nadlan_nli_tools' ) ? nadlan_nli_tools() : array();
		foreach ( $tools as $tid => $t ) {
			$pid = (int) $wpdb->get_var( $wpdb->prepare( "SELECT ID FROM {$wpdb->posts} WHERE post_status='publish' AND post_type IN ('page','post') AND post_content LIKE %s ORDER BY ID ASC LIMIT 1", '%' . $wpdb->esc_like( '[nadlan_tool id="' . $tid . '"' ) . '%' ) );
			if ( $pid ) { $o .= '- [' . $t['name'] . '](' . get_permalink( $pid ) . '): ' . $t['desc'] . "\n"; }
		}
		$o .= "\n## Apartment prices (official medians)\n";
		foreach ( array( 'apartment-prices' ) as $p ) { if ( $id = $by_path( $p ) ) { $o .= $line( $id, 'every city with a price page, by rooms and quarter' ); } }
		$cities = $wpdb->get_col( "SELECT ID FROM {$wpdb->posts} WHERE post_status='publish' AND post_type='page' AND post_name LIKE '%-apartment-prices' ORDER BY menu_order, ID LIMIT 60" );
		foreach ( $cities as $id ) { $o .= $line( (int) $id ); }
		$o .= "\n## Guides\n";
		foreach ( array( 'buying-apartment', 'selling-apartment', 'real-estate-lawyer', 'real-estate-tax-advisor', 'mortgage-calculator', 'urban-renewal/map', 'dira-behanacha', 'tabu-extract-check', 'home-inspection', 'investment-apartment', 'sde-dov', 'glossary' ) as $p ) {
			if ( $id = $by_path( $p ) ) { $o .= $line( $id ); }
		}
		$o .= "\n## Buying property abroad\n";
		$abroad = $wpdb->get_col( "SELECT ID FROM {$wpdb->posts} WHERE post_status='publish' AND post_type='page' AND post_content LIKE '%[nadlan_crumbs%' ORDER BY ID LIMIT 80" );
		foreach ( array( 'short-term-rentals-abroad' ) as $p ) { if ( $id = $by_path( $p ) ) { $o .= $line( $id ); } }
		foreach ( $abroad as $id ) { $o .= $line( (int) $id ); }
		$o .= "\n## New projects\n";
		$o .= '- [פרויקטים חדשים](' . home_url( '/projects/' ) . "): the catalog of new building projects in Israel\n";
		foreach ( array( 'projects/hamedina', 'projects/rainbow-tel-aviv', 'projects/duo-tel-aviv', 'projects/dimri-yama-sde-dov', 'projects/ashira-sde-dov', 'projects/h-infinity-somail-tel-aviv', 'projects/einstein-tower' ) as $p ) {
			$pp = get_page_by_path( basename( $p ), OBJECT, 'nadlan_project' );
			if ( $pp && 'publish' === $pp->post_status ) { $o .= $line( $pp->ID ); }
		}
		$o .= "\n## Other languages\n";
		foreach ( array( 'en' => 'English', 'fr' => 'Français', 'ru' => 'Русский', 'ar' => 'العربية' ) as $p => $n ) { if ( $id = $by_path( $p ) ) { $o .= '- [' . $n . '](' . get_permalink( $id ) . ")\n"; } }
		set_transient( 'nadlan_llms_txt_v1', $o, 6 * HOUR_IN_SECONDS );
		return $o;
	}
}
add_action( 'parse_request', function ( $wp ) {
	$req = isset( $wp->request ) ? (string) $wp->request : '';
	if ( 'llms.txt' === $req ) {
		status_header( 200 ); header( 'Content-Type: text/plain; charset=utf-8' ); header( 'Cache-Control: public, max-age=3600' );
		echo nadlan_llms_txt(); exit;
	}
	if ( NADLAN_INDEXNOW_KEY . '.txt' === $req ) {
		status_header( 200 ); header( 'Content-Type: text/plain; charset=utf-8' ); echo NADLAN_INDEXNOW_KEY; exit;
	}
}, 0 );
/* a page published or updated drops the cached list */
add_action( 'save_post_page', function () { delete_transient( 'nadlan_llms_txt_v1' ); } );

/* 1.72.504 (HAD-592): the registered-contractor check, its REST search route */
require_once __DIR__ . '/pinkas.php';
