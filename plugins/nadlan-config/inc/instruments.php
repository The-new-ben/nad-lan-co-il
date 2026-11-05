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
				'desc' => 'מחשב את מס הרכישה על דירה לפי המדרגות של רשות המסים בכל המסלולים: דירה יחידה, דירה נוספת, עולה חדש, תושב חוץ, נכה, קרקע ומתנה לקרוב, ועד מתי כל שיעור בתוקף; מתי מדווחים ומשלמים ומה עולה כל שבוע של איחור; שני קונים לפי המעמד של כל אחד; חלון ההטבה לעולה ותקנה 12 מול 12א; ולמשפרי דיור עד מתי למכור את הדירה הקודמת, כולל הארכת המלחמה.',
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
				'data' => array( 'value.json', 'value-series.json' ),  // 1.72.526: the 22-quarter official series and the CBS dwelling index (pval v2, three anchors)
				'related' => array( '/apartment-prices/' => 'מחירון הדירות לפי עיר', '/purchase-tax-calculator/' => 'מחשבון מס רכישה', '/apartment-purchase-cost-calculator/' => 'עלות רכישה כוללת', '/projects/hamedina/' => 'דירות במגדלי כיכר המדינה' ),
			),
			'arnona' => array(
				'name' => 'מחשבון ארנונה תל אביב 2026', 'cat' => 'FinanceApplication', 'kicker' => 'מחשבון · ארנונה',
				'desc' => 'ארנונה למגורים בתל אביב-יפו לשנת 2026 לפי צו הארנונה של העירייה: אזור, סוג הבניין לפי שנת הבנייה, שטח הדירה עם המרפסות, הנחות ותשלום דו־חודשי.',
				'data' => array( 'arnona-tlv.json' ),
				'related' => array( '/apartment-purchase-cost-calculator/' => 'עלות רכישה כוללת', '/property-value-estimator/' => 'מחשבון שווי דירה', '/tel-aviv-apartment-prices/' => 'מחירי דירות בתל אביב', '/projects/hamedina/' => 'דירות במגדלי כיכר המדינה' ),
			),
			/* 1.72.524 (HAD-601, U3): nrm v2, your Israeli borrowing limit by passport and paycheck; still English only (phase 1) */
			'nrm' => array(
				'only' => 'en', 'name' => 'Israel mortgage calculator for foreigners', 'cat' => 'FinanceApplication', 'kicker' => 'Calculator · Israeli mortgage',
				'desc' => 'Your Israeli borrowing limit by passport and paycheck: the Bank of Israel loan cap by citizenship (50% for a non-citizen, 75% for an Israeli citizen or registered oleh buying the only home in Israel, 70% for a replacement home), the payment tested against your income at 50% and at one third in your own currency, the purchase tax by residency (foreign resident, Israeli resident, oleh), the cash to close, and the payment in dollars, euros or pounds with a 10% move in the shekel, at the Bank of Israel rates of the day.',
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
			/* 1.72.506 (HAD-592): the condo-documents family, one file tools/condo.js; condo.json from official sources (fee 2026, Land Law, drawing rules) */
			'condo' => array(
				'file' => 'condo', 'name' => 'איזה מסמך בבית המשותף עונה על השאלה שלכם', 'cat' => 'ReferenceApplication', 'kicker' => 'תשריט · צו · תקנון',
				'desc' => 'לחיצה על שאלה של קונה (חניה, מחסן, גג, חצר, מרפסת, זכויות בנייה, הוצאות ועד, שטח הדירה, תשריט מאושר, בניין לא רשום) מדליקה את החלק בתשריט לדוגמה ואומרת באיזה מסמך מחפשים, מה בודקים, מה הדגל האדום ומה המקור בחוק, ואיך מזמינים את תיק הבית המשותף ב־39 ₪.',
				'data' => array( 'condo.json' ),
				'related' => array( '/tabu-extract-check/' => 'בדיקת נסח טאבו', '/apartment-buying-checklist/' => 'רשימת בדיקות לפני קניית דירה', '/real-estate-lawyer/' => 'עורך דין מקרקעין', '/guides/new-project-parking/' => 'חניה בפרויקט חדש' ),
			),
			'condomaj' => array(
				'file' => 'condo', 'name' => 'מחשבון רוב בבית משותף', 'cat' => 'UtilitiesApplication', 'kicker' => 'מחשבון · רוב בבית משותף',
				'desc' => 'כמה בעלי דירות צריכים להסכים לרישום בית משותף, לתקנון מוסכם, להצמדת חניה או גג, להרחבת דירה ולבניית ממ״ד, לפי חוק המקרקעין ומספר הדירות בבניין.',
				'data' => array( 'condo.json' ),
				'related' => array( '/urban-renewal/tama-38-rights-obligations/' => 'זכויות וחובות בתמ״א 38', '/property-value/building-rights-check/' => 'בדיקת זכויות בנייה' ),
			),
			/* 1.72.521 (HAD-601, Q6): the gypsum wall calculator of the red board term; gwall.json from the manufacturer and supplier sites (25.10.2026) */
			'gwall' => array(
				'name' => 'מחשבון קיר גבס ורוד: כמה לוחות, משקל ועלות', 'cat' => 'UtilitiesApplication', 'kicker' => 'מחשבון · קיר גבס',
				'desc' => 'לפי מקום הקיר, דרישת האש מהיועץ, אורך, גובה, צדדים ושכבות: איזה לוח מתאים (ורוד, משולב, מיוחד לאש או לא לחוץ), כמה לוחות להזמין לפי שטח ולפי תוכנית חיתוך, כמה הם שוקלים לפי טבלת הספק, כמה הם עולים אצל ארבעה ספקים, המחיצה שנבדקה כשיש כזאת, והמסמכים לבקש מהקבלן.',
				'data' => array( 'gwall.json' ),
				'related' => array( '/glossary/%D7%9C%D7%95%D7%97-%D7%92%D7%91%D7%A1-%D7%99%D7%A8%D7%95%D7%A7/' => 'לוח גבס ירוק', '/glossary/%D7%98%D7%99%D7%97-%D7%92%D7%91%D7%A1/' => 'טיח גבס', '/home-inspection/' => 'בדק בית', '/new-projects/construction-input-index/' => 'מדד תשומות הבנייה' ),
			),
			/* 1.72.522 (HAD-601, Q5): "ת"י 466 והדירה שלי"; t466.json from the Standards Institution pages (25.10.2026) */
			't466' => array(
				'name' => 'איזה חלק של ת״י 466 חל אצלכם: בדיקה לפי המצב', 'cat' => 'ReferenceApplication', 'kicker' => 'בדיקה · ת״י 466',
				'desc' => 'לפי המצב (דירה חדשה מקבלן וסוג התקרות, פתיחת קיר בשיפוץ, בית פרטי, סדק או ברזל חשוף, תקרות דרוכות, טרומיות או לוח״דים): אילו חלקים של חוקת הבטון חלים, המהדורה שבתוקף ומחיר כל חלק במכון התקנים, מי אחראי, מה לשאול, איזה תקן עובד לצידו ואיפה קוראים את התקן בלי תשלום, עם חתך בניין שמסמן את האלמנטים.',
				'data' => array( 't466.json' ),
				'related' => array( '/glossary/%D7%AA%D7%99-118/' => 'ת״י 118', '/glossary/%D7%A7%D7%95%D7%A0%D7%A1%D7%98%D7%A8%D7%95%D7%A7%D7%98%D7%95%D7%A8/' => 'קונסטרוקטור', '/home-inspection/' => 'בדק בית', '/real-estate-lawyer/construction-defects-lawsuit/' => 'ליקויי בנייה' ),
			),
			/* G2 (HAD-601 round 2): "הבניין שלכם בפינוי בינוי"; pinui.json from the Pinui Binui law, the 2025 authority report and gov.il (tools/urban/build_g2g3_data.py, 26.10.2026) + the tracker */
			'pinui' => array(
				'name' => 'הבניין שלכם בפינוי בינוי: הרוב לפי החוק, מה מגיע לכם וכמה זמן', 'cat' => 'ReferenceApplication', 'kicker' => 'מחשבון · פינוי בינוי',
				'desc' => 'לפי חוק פינוי ובינוי בנוסחו היום: הרוב המיוחס בניין אחר בניין (שני שלישים במקבץ, שלוש חמישיות בכל בניין), מה חסר, מתי אפשר לבקש שמאי של הרשות בחינם, תקרת השטח לפטור ממס לדירה שלכם, החלופות לבני 70 ו-75, המועדים שהחוק נותן ליזם מהעסקה הראשונה, והשלב של המתחם אצל הרשות עם השנים מאז אישור התכנית מול הממוצע של הרשות.',
				'data' => array( 'pinui.json', 'renewal-track.json' ),
				'related' => array( '/urban-renewal/' => 'התחדשות עירונית', '/urban-renewal/map/' => 'מפת התחדשות עירונית', '/urban-renewal/check/' => 'בדיקת בניין חינמית', '/glossary/dayar-sarvan/' => 'דייר סרבן', '/glossary/shamai-pinui-binui/' => 'שמאי פינוי בינוי', '/my-renewal/' => 'חדר פרויקט לנציגות' ),
			),
			/* G3: "התחדשות עירונית בעיר שלכם"; urcity.json from the 2025 authority report (annex A, TAMA 38 by city) + the tracker */
			'urcity' => array(
				'name' => 'התחדשות עירונית בעיר שלכם: מתחמים, מסלולים ותמ"א 38', 'cat' => 'ReferenceApplication', 'kicker' => 'מפה · התחדשות עירונית',
				'desc' => 'לכל עיר: המתחמים במפת הרשות הממשלתית להתחדשות עירונית לפי שלב ומסלול, הדירות היום ואחרי הבנייה והמכפיל, מה זז מאז הבדיקה הקודמת, ומה דוח הרשות לשנת 2025 אומר על תמ"א 38 בעיר (התכנית המחליפה, ההארכה, הזמן מבקשה להיתר, הדירות שנמכרו). לבניין: איזה מסלול נשאר פתוח, פינוי בינוי, תמ"א 38 או תכנית לרישוי מהיר, וכמה חתימות צריך. והשוואת כל הערים.',
				'data' => array( 'urcity.json', 'renewal-track.json' ),
				'related' => array( '/urban-renewal/pinui-binui/' => 'פינוי בינוי', '/urban-renewal/tama-38/' => 'תמ"א 38', '/urban-renewal/tama-38-alternatives/' => 'מה במקום תמ"א 38', '/urban-renewal/map/' => 'מפת התחדשות עירונית', '/urban-renewal/check/' => 'בדיקת בניין חינמית' ),
			),
			/* G6 (HAD-601 round 3, 26.10.2026): the owner page /home-inspection/ ("בדק בית" 2,900/mo); bedek.json from the Sale (Apartments) Law
			   schedule and the published price pages, built and checked by tools/instruments/build_pros_data.py */
			'bedek' => array(
				'name' => 'בדק בית: עד מתי הקבלן אחראי, מתי לבדוק וכמה זה עולה', 'cat' => 'UtilitiesApplication', 'kicker' => 'מחשבון · בדק בית',
				'desc' => 'לפי סוג הליקוי ויום המסירה: תקופת הבדק לפי התוספת לחוק המכר (דירות), שלוש שנות האחריות שאחריה, מי צריך להוכיח מה, עד מתי להודיע לקבלן על ליקוי שנראה במסירה, כלל התיקון החוזר והזכויות של קונה משנה; לוח הבדיקות מיום המסירה; וכל המחירים שפורסמו לבדק בית לפי סוג הנכס, עם התאריך והאם הם כוללים מע״מ.',
				'data' => array( 'bedek.json' ),
				'related' => array( '/real-estate-lawyer/sale-of-apartments-law/' => 'חוק המכר', '/real-estate-lawyer/construction-defects-lawsuit/' => 'תביעת ליקויי בנייה', '/glossary/%D7%AA%D7%99-466/' => 'ת״י 466', '/new-projects/contractor-delay-compensation/' => 'פיצוי על איחור במסירה', '/real-estate-appraiser/' => 'שמאי מקרקעין', '/real-estate-lawyer/' => 'עורך דין מקרקעין' ),
			),
			/* G7: the owner page /real-estate-appraiser/ ("שמאי מקרקעין" 2,400/mo); shamai.json from the Appraisers Law, the planning law, the 2009
			   decisive-appraiser fee regulations, Kol Zchut on bank appraisals, the Ministry of Justice register and exam file (data.gov.il) */
			'shamai' => array(
				'file' => 'shamai', 'name' => 'איזה שמאי אתם צריכים, מי משלם, מה המועד וכמה זה עולה', 'cat' => 'ReferenceApplication', 'kicker' => 'מחשבון · שמאי מקרקעין',
				'desc' => 'לפי מטרת השומה (משכנתא, לפני חתימה, היטל השבחה, תכנית שפגעה בשווי, ירושה, התחדשות עירונית ועוד): מי מזמין את השמאי ומי משלם, המועד בחוק מהתאריך שלכם (45 ימים לערר או לבקשת שמאי מכריע, 3 שנים לתביעה לפי סעיף 197), המחירים שפורסמו עם התאריך, ושכר השמאי המכריע לפי התקנות.',
				'data' => array( 'shamai.json' ),
				'related' => array( '/glossary/%D7%A9%D7%9E%D7%90%D7%99-%D7%9E%D7%9B%D7%A8%D7%99%D7%A2/' => 'שמאי מכריע', '/real-estate-tax-advisor/betterment-levy-appeal/' => 'ערר על היטל השבחה', '/glossary/shamai-pinui-binui/' => 'שמאי פינוי בינוי', '/property-value-estimator/' => 'מחשבון שווי דירה', '/mortgage-calculator/' => 'מחשבון משכנתא', '/real-estate-lawyer/' => 'עורך דין מקרקעין' ),
			),
			'shamaireg' => array(
				'file' => 'shamai', 'name' => 'האם השמאי רשום בפנקס? חיפוש לפי שם או מספר רישיון', 'cat' => 'UtilitiesApplication', 'kicker' => 'חיפוש · פנקס שמאי המקרקעין',
				'desc' => 'חיפוש לפי שם או מספר רישיון במאגר שמאי המקרקעין של משרד המשפטים באתר data.gov.il. החיפוש נשלח למאגר הרשמי ברגע שמחפשים, והרשימה לא נשמרת באתר. לפי חוק שמאי מקרקעין, רק מי שרשום בפנקס רשאי לעשות שומת מקרקעין בשכר.',
				'data' => array( 'shamai.json' ),
				'related' => array( '/real-estate-appraiser/' => 'שמאי מקרקעין', '/glossary/%D7%A9%D7%9E%D7%90%D7%99-%D7%9E%D7%9B%D7%A8%D7%99%D7%A2/' => 'שמאי מכריע', '/property-value-estimator/' => 'מחשבון שווי דירה' ),
			),
			/* G8: the owner page /real-estate-lawyer/ ("עורך דין מקרקעין" 1,600/mo); orechdin.json from Sale Law s.6ג and the 2014 regulations with
			   the 2026 notice, the Bar's recommended minimum tariff (2026 amounts), the Land Fees regulations (2026), rule 14, and published fees */
			'orechdin' => array(
				'name' => 'עורך דין מקרקעין: כמה זה עולה, מה מותר לקבלן לגבות ומה המועדים', 'cat' => 'FinanceApplication', 'kicker' => 'מחשבון · עורך דין מקרקעין',
				'desc' => 'לפי סוג העסקה והמחיר: שכר הטרחה שמשרדים פרסמו ב-2026 לצד התעריף המינימלי המומלץ של לשכת עורכי הדין, כמה מותר לקבלן לגבות מכם על עורך הדין שלו (5,915 ₪ או 0.5% מהמחיר, הנמוך מביניהם, ועוד מע״מ), אגרות רשם המקרקעין ל-2026, וצעדי העסקה עם מועדי ההצהרה ומס הרכישה מיום החתימה. מידע כללי, לא ייעוץ משפטי.',
				'data' => array( 'orechdin.json', 'ptax.json' ),
				'related' => array( '/purchase-tax-calculator/' => 'מחשבון מס רכישה', '/apartment-purchase-cost-calculator/' => 'מחשבון עלות רכישה כוללת', '/real-estate-lawyer/sale-of-apartments-law/' => 'חוק המכר', '/home-inspection/' => 'בדק בית', '/real-estate-appraiser/' => 'שמאי מקרקעין', '/mortgage-calculator/' => 'מחשבון משכנתא' ),
			),
			/* G5 (26.10.2026): the owner page /דירות-להשכרה/ ("דירות להשכרה" / "דירה להשכרה"); data rent.json (data.nadlan.gov.il rent files
			   20-08-2026, CBS table 4.9 Q2 2026, CBS rent index 120460, the Rental and Loan Law sign 6, Kol Zchut tax pages 22.2.2026) */
			'rentfair' => array(
				'name' => 'כמה שכר דירה הוגן לדירה הזאת', 'cat' => 'FinanceApplication', 'kicker' => 'בדיקה · שכר דירה',
				'desc' => 'שכר הדירה שמבקשים מכם או שאתם מבקשים, מול שכר הדירה החציוני הרשמי בעיר לפי מספר החדרים (72 ערים), מול השכונה (945 שכונות), מול הממוצע של הלמ״ס עם טעות הדגימה ומול החציון הארצי; הערובה המרבית שמותר לבקש לפי חוק השכירות והשאילה, מועדי התיקון וההודעות, ושלושת מסלולי המס של המשכיר ל־2026.',
				'data' => array( 'rent.json' ),
				'related' => array( '/real-estate-lawyer/residential-lease-agreement/' => 'חוזה שכירות דירה', '/cpi-calculator/' => 'מחשבון הצמדה למדד', '/buy-vs-rent/' => 'מחשבון קנייה מול שכירות', '/my-rentals/' => 'ניהול נכסים מושכרים' ),
			),
			/* G1 (26.10.2026): /dira-behanacha/ upgrade, two tools in one file tools/dirafit.js; data dira-round.json (official lottery
			   file + the ministry's releases of 25.5, 23.6 and 2.8.2026 + gov.il rules + invest.json), boi-mortgage.json, ptax.json */
			'dirafit' => array(
				'file' => 'dirafit', 'name' => 'דירה בהנחה: מי זכאי ואיפה הכי כדאי להירשם', 'cat' => 'UtilitiesApplication', 'kicker' => 'בדיקה אישית · דירה בהנחה',
				'desc' => 'בדיקת זכאות לדירה בהנחה (מחיר למשתכן) לפי ההגדרות של משרד הבינוי והשיכון: חסר דירה, משפר דיור או לא זכאי, עדיפות מילואים ובני מקום, ושלוש הערים שנתנו הכי הרבה דירות לכל משק בית שנרשם בהגרלה ה־11, לצד הסיכוי בכל עיר בקובץ הרשמי.',
				'data' => array( 'dira-round.json' ),
				'related' => array( '/mortgage-calculator/' => 'מחשבון משכנתא', '/apartment-purchase-cost-calculator/' => 'עלות רכישה כוללת', '/new-projects/presale-apartment/' => 'דירה על הנייר', '/real-estate-lawyer/' => 'עורך דין מקרקעין' ),
			),
			'diracost' => array(
				'file' => 'dirafit', 'name' => 'דירה בהנחה: המחיר מול מחירי העסקאות בעיר', 'cat' => 'FinanceApplication', 'kicker' => 'מחשבון · דירה בהנחה',
				'desc' => 'מחיר הדירה מההגרלה לפי המחיר למ״ר והשטח, עם מע״מ, מול חציון העסקאות של דירות באותו גודל בעיר, ההון העצמי לפי כללי התוכנית (75%, מסלול השמאי, מענק 40,000 או 60,000 ₪) וההחזר החודשי בריבית הממוצעת של בנק ישראל.',
				'data' => array( 'dira-round.json', 'boi-mortgage.json', 'ptax.json' ),
				'related' => array( '/mortgage-calculator/' => 'מחשבון משכנתא', '/apartment-prices/' => 'מחירי דירות בישראל', '/new-projects/construction-input-index/' => 'הצמדה למדד תשומות הבנייה', '/purchase-tax-calculator/' => 'מחשבון מס רכישה' ),
			),
			/* S1 (HAD-601 loop, Sde Dov hub moat): "כל מגרש ברובע שדה דב"; sdplan.json from the Tel Aviv GIS (plots 837, plans and design plans 528, permits 772, construction sites 499, green line stations 764), the Israel Land Authority tender files and the OSM waterline (docs/research/2026-10-26-upgrades/s1-sde-dov/build_s1_data.py, 26.10.2026) */
			'sdplan' => array(
				'name' => 'כל מגרש ברובע שדה דב: מי זכה בו, בכמה, ובאיזה שלב הוא היום', 'cat' => 'ReferenceApplication', 'kicker' => 'מגרש אחר מגרש · רובע שדה דב',
				'desc' => 'לכל אחד מ־73 המגרשים למגורים, למלונאות ולתעסוקה ברובע שדה דב: היעוד והשטח בתכנית, מכרז רשות מקרקעי ישראל (הזוכה כפי שנרשם, יחידות הדיור, מספר ההצעות, סכום הזכייה והוצאות הפיתוח, וקרקע ופיתוח ליחידת דיור), תכנית העיצוב האדריכלי ותאריך אישורה, בקשה להיתר, היתר ותחילת עבודות לפי העירייה, תחנת הקו הירוק הקרובה והמרחק מהים, ובפרויקט שבשיווק: המחיר שדווח. מפה של כל מתחם לפי השלב הרשמי, וטבלה שמסדרים לפי שלב, הצעות, מחיר קרקע ליחידה או מרחק.',
				'data' => array( 'sdplan.json' ),
				'related' => array( '/sde-dov/prices/' => 'מחירי דירות בשדה דב', '/sde-dov/eshkol/' => 'מתחם אשכול', '/sde-dov/merkaz/' => 'מתחם המרכז', '/sde-dov/tzafon/' => 'מתחם הצפון', '/sde-dov/transport/' => 'תחבורה והקו הירוק', '/purchase-tax-calculator/' => 'מחשבון מס רכישה' ),
			),
			/* 1.72.528 (HAD-601, Q1 moat): "יומן המתחמים", the complex tracker of /urban-renewal/map/; renewal-track.json from the authority's map, the data.gov.il file, our import and XPLAN (tools/urban/build_renewal_track.py, 26.10.2026) */
			'urtrack' => array(
				'name' => 'יומן המתחמים: מה השלב של המתחם שלכם, ומה השתנה בו', 'cat' => 'ReferenceApplication', 'kicker' => 'יומן · התחדשות עירונית',
				'desc' => 'לכל מתחם התחדשות עירונית: השלב והמסלול אצל הרשות הממשלתית להתחדשות עירונית היום, השלב בקובץ data.gov.il ובייבוא שלנו, כמה דירות יש היום וכמה יהיו אחרי הבנייה והמכפיל, מספר התכנית ותאריכי ההפקדה והאישור, ממתי המתחם מופיע במאגר וכל שינוי שראינו בין הבדיקות עם תאריך הבדיקה. חיפוש לפי עיר, שם מתחם, רחוב או מספר תכנית, וטבלה של כל מה שזז במאגר.',
				'data' => array( 'renewal-track.json' ),
				'related' => array( '/urban-renewal/' => 'המדריך להתחדשות עירונית', '/urban-renewal/check/' => 'בדיקת בניין חינמית', '/urban-renewal/pinui-binui/' => 'פינוי בינוי', '/urban-renewal/tama-38/' => 'תמ״א 38 והחלופות', '/my-renewal/' => 'חדר פרויקט לנציגות' ),
			),
			/* 1.72.522 (HAD-601, Q3): the Dekel price-list family, one file tools/dekel.js; dekel.json from dekel.co.il (25.10.2026), no Dekel price stored */
			'dkpick' => array(
				'file' => 'dekel', 'name' => 'איזה מחירון דקל מתאים לעבודה שלכם', 'cat' => 'ReferenceApplication', 'kicker' => 'בחירה · מחירון דקל',
				'desc' => 'לפי סוג העבודה וההיקף הכספי: איזה מחירון של דקל מתאים (בנייה ותשתיות, שיפוצים ואחזקה, הסכמי מסגרת, בנייה פרטית, שינויי דיירים, שיפוץ דירות או המחשבון למ״ר), כמה פרקים וסעיפים יש בו, והאם ההיקף בתוך הטווח שהמחירים שלו מכוונים אליו.',
				'data' => array( 'dekel.json' ),
				'related' => array( '/glossary/%D7%9B%D7%AA%D7%91-%D7%9B%D7%9E%D7%95%D7%99%D7%95%D7%AA/' => 'כתב כמויות', '/glossary/%D7%A4%D7%A7%D7%95%D7%93%D7%AA-%D7%A9%D7%99%D7%A0%D7%95%D7%99%D7%99%D7%9D/' => 'פקודת שינויים', '/new-projects/construction-input-index/' => 'מדד תשומות הבנייה' ),
			),
			'dkquote' => array(
				'file' => 'dekel', 'name' => 'בדיקת הצעת מחיר של קבלן מול מחירון דקל', 'cat' => 'UtilitiesApplication', 'kicker' => 'בדיקה · הצעת מחיר מול דקל',
				'desc' => 'סעיף אחר סעיף: הכמות, מחיר היחידה בדקל מהמנוי שלכם ומחיר היחידה בהצעה, סך ההפרש בשקלים ובאחוזים, והשאלות לקבלן לפי הכללים של דקל: פינוי עד 15 ק״מ בלי אגרת הטמנה, ברזל הזיון בנפרד, תוספת לאזור מרוחק ולעבודת לילה.',
				'data' => array( 'dekel.json' ),
				'related' => array( '/glossary/%D7%97%D7%A9%D7%91%D7%95%D7%9F-%D7%97%D7%9C%D7%A7%D7%99/' => 'חשבון חלקי', '/professionals/' => 'מאגר בעלי המקצוע' ),
			),
			/* 1.72.525 (HAD-601, Q4): dktool (which Dekel software fits a role) and dkboq (a BOQ line builder with the reader's own prices), tools/dekel.js */
			'dktool' => array(
				'file' => 'dekel', 'name' => 'איזה כלי של דקל מתאים לכם', 'cat' => 'ReferenceApplication', 'kicker' => 'בחירה · תוכנת דקל',
				'desc' => 'לפי התפקיד בפרויקט (רוכש דירה בשינויי דיירים, קבלן שיפוצים, מפקח או מנהל פרויקט, רשות שמוציאה מכרז, יזם או שמאי, מנהל נכסים): אילו כלים של דקל מתאימים, מה עושים בכל אחד, הכתובת הרשמית מתוך מפת האתר של דקל, ואיזה מחירון של דקל עומד מאחוריהם.',
				'data' => array( 'dekel.json' ),
				'related' => array( '/glossary/%D7%9E%D7%97%D7%99%D7%A8%D7%95%D7%9F-%D7%93%D7%A7%D7%9C-%D7%9C%D7%91%D7%A0%D7%99%D7%99%D7%94-%D7%95%D7%AA%D7%A9%D7%AA%D7%99%D7%95%D7%AA/' => 'מחירון דקל לבנייה ותשתיות', '/glossary/%D7%9B%D7%AA%D7%91-%D7%9B%D7%9E%D7%95%D7%99%D7%95%D7%AA/' => 'כתב כמויות' ),
			),
			'dkboq' => array(
				'file' => 'dekel', 'name' => 'כתב כמויות בפורמט דקל: נסו בעצמכם', 'cat' => 'UtilitiesApplication', 'kicker' => 'מחשבון · כתב כמויות',
				'desc' => 'סעיפים בפורמט של דקל (פרק.תת פרק.סעיף) עם כמות ומחיר יחידה שמקלידים מהמנוי או מהצעה: סיכום לכל פרק, בצ"מ לבחירה, מע"מ שאפשר לשנות וסך הכול. אין במחשבון מחירים של דקל.',
				'data' => array( 'dekel.json' ),
				'related' => array( '/glossary/%D7%97%D7%A9%D7%91%D7%95%D7%9F-%D7%97%D7%9C%D7%A7%D7%99/' => 'חשבון חלקי', '/glossary/%D7%A4%D7%A7%D7%95%D7%93%D7%AA-%D7%A9%D7%99%D7%A0%D7%95%D7%99%D7%99%D7%9D/' => 'פקודת שינויים' ),
			),
			/* 1.72.523 (HAD-601, U1): Mortgage 2.0, a custom surface; boi-mortgage.json from Bank of Israel and CBS (25.10.2026), every value dated */
			'mortgage' => array(
				'name' => 'מחשבון משכנתא לפי מסלולים', 'cat' => 'FinanceApplication', 'kicker' => 'מחשבון · משכנתא',
				'desc' => 'מחשבון משכנתא לפי מסלולים: החזר ראשון, ההחזר הגבוה הצפוי, ריבית, הצמדה ולוח סילוקין, לפי סכום, לפי החזר חודשי או לפי מחיר והון עצמי; שלושת הסלים האחידים של בנק ישראל, בדיקת התמהיל מול הוראה 329, פירעון מוקדם עם הערכת העמלה, והשוואת ההצעה מהבנק לריבית הממוצעת שבנק ישראל פרסם לאותו מסלול ולאותה תקופה.',
				'data' => array( 'boi-mortgage.json' ),
				'related' => array( '/mortgage-calculator/mortgage-repayment-capacity/' => 'כמה משכנתא אפשר לקחת', '/mortgage-calculator/mortgage-interest-rates/' => 'ריבית משכנתא היום', '/mortgage-calculator/mortgage-ltv-ratio/' => 'אחוז מימון', '/mortgage-calculator/reverse-mortgage/' => 'מחשבון משכנתא הפוכה', '/mortgage-refinance/' => 'מחזור משכנתא', '/mortgage-calculator/mortgage-for-any-purpose/' => 'משכנתא לכל מטרה', '/purchase-tax-calculator/' => 'מחשבון מס רכישה', '/apartment-purchase-cost-calculator/' => 'עלות רכישה כוללת' ),
			),
			/* 1.72.587 (HAD-675): the quick mortgage calculator at the top of /mortgage-calculator/; boi-mortgage.json v2 (BoI by bank) */
			'mquick' => array(
				'name' => 'מחשבון משכנתא מהיר', 'cat' => 'FinanceApplication', 'kicker' => 'מחשבון · משכנתא',
				'desc' => 'מחשבון משכנתא מהיר: ההחזר החודשי הראשון, סך ההחזרים והריבית לפי סכום המשכנתא, לפי מחיר הדירה וההון העצמי או לפי ההחזר החודשי שמתאים לכם, ל־15 עד 30 שנה, בתמהיל ובריבית הממוצעים של כל הבנקים או של בנק אחד, לפי נתוני בנק ישראל לחודש האחרון.',
				'data' => array( 'boi-mortgage.json' ),
			),
			/* 1.72.523 (HAD-601, U2): the yield and cash-flow map; invest.json from 148 nadlan.gov.il files (20.8.2026), BoI 4.62% (8.2026) */
			'invest' => array(
				'name' => 'מפת התשואה והתזרים', 'cat' => 'FinanceApplication', 'kicker' => 'מחשבון · נדל״ן להשקעה',
				'desc' => 'דירה להשקעה בכל עיר לפי החציונים הרשמיים של אתר הנדל״ן הממשלתי, לפי מספר החדרים: תשואה ברוטו, משכנתא של 50% בריבית הממוצעת של בנק ישראל, תזרים חודשי לפני ואחרי ההוצאות שלכם, הון עצמי עם מס רכישה של דירה נוספת, שלושת מסלולי המס על שכר הדירה, כמה מהמחיר שכר הדירה לבדו מחזיק, ובדיקה לפי הון עצמי: אילו ערים עובדות.',
				'data' => array( 'invest.json' ),
				'related' => array( '/investment-property-mortgage/' => 'משכנתא לדירה להשקעה', '/purchase-tax-calculator/' => 'מחשבון מס רכישה', '/apartment-purchase-cost-calculator/' => 'עלות רכישה כוללת', '/investment/real-estate-yield/' => 'איך מחשבים תשואה', '/apartment-prices/' => 'מחירי הדירות לפי עיר' ),
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
		// 1.72.513: a page built in PHP (the /projects/ catalog, inc/projects-hub.php) names the tools it prints
		$ids = array_values( array_intersect( (array) apply_filters( 'nadlan_nli_page_ids', $ids ), array_keys( nadlan_nli_tools() ) ) );
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
				. '. נכה (תקנה 11): 0.5%, ובדירה יחידה עד 2,500,000 ₪ פטור עד המדרגה הראשונה. קרקע ונכס שאינו מגורים: 6%. מתנה לקרוב: שליש מהמס. משפרי דיור נחשבים דירה יחידה אם ימכרו את הדירה הקודמת תוך 24 חודשים (רכישה מ־1.6.2025). המס מחושב על שווי הדירה כולה, וקונה של חלק משלם לפי החלק שלו. מדווחים תוך 30 יום מהעסקה ומשלמים תוך 60 יום, או מאוחר יותר כשהחזקה ורוב התשלום נדחים (סעיף 51); איחור בתשלום: 0.2% מהמס לכל שבוע ועוד הצמדה וריבית.</p>';
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
		if ( 'condo' === $id || 'condomaj' === $id ) {  // 1.72.506: the answers as plain text and tables (the drawing needs the script)
			$path = dirname( __DIR__ ) . '/assets/instruments/data/condo.json';
			$c = is_readable( $path ) ? json_decode( (string) file_get_contents( $path ), true ) : null;
			if ( ! is_array( $c ) || empty( $c['chips'] ) ) { return ''; }
			if ( 'condomaj' === $id ) {
				$t = '<table><caption>מי צריך להסכים בבית משותף, לפי חוק המקרקעין</caption><thead><tr><th>הפעולה</th><th>מי צריך להסכים</th><th>המקור</th></tr></thead><tbody>';
				foreach ( $c['maj'] as $m ) { $t .= '<tr><td>' . esc_html( $m['he'] ) . '</td><td>' . esc_html( $m['rule'] ) . '</td><td>' . esc_html( $m['src'] ) . '</td></tr>'; }
				return '<p>העברת הצמדה קיימת מדירה לדירה באותו בניין אינה דורשת את הסכמת השכנים, ונעשית בתיקון צו הבית המשותף.</p>' . $t . '</tbody></table>';
			}
			$f = $c['fee'];
			$t = '<p>מזמינים את תיק הבית המשותף באתר הממשלתי לפי גוש וחלקה או לפי מספר התיק: ' . (int) $f['order'] . ' ₪ להזמנה (תעריף ' . (int) $f['year'] . '), וקישור להורדה מגיע בדואר האלקטרוני תוך 24 שעות. עיון בתיק הנייר בלשכה: ' . (int) $f['physical'] . ' ₪.</p>';
			$t .= '<table><caption>איזה מסמך עונה על איזו שאלה</caption><thead><tr><th>השאלה</th><th>באיזה מסמך ואיפה</th><th>דגל אדום</th></tr></thead><tbody>';
			foreach ( $c['chips'] as $q ) { $t .= '<tr><td>' . esc_html( $q['he'] ) . '</td><td>' . esc_html( $q['doc'] ) . '</td><td>' . esc_html( $q['flag'] ) . '</td></tr>'; }
			return $t . '</tbody></table>';
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
		if ( 'gwall' === $id ) {  // 1.72.521: common walls as a plain table (the same count as tools/gwall.js: the larger of area with 10% waste and the cut plan)
			$path = dirname( __DIR__ ) . '/assets/instruments/data/gwall.json';
			$g = is_readable( $path ) ? json_decode( (string) file_get_contents( $path ), true ) : null;
			if ( ! is_array( $g ) || empty( $g['kgBoard'] ) ) { return ''; }
			$wd = (float) $g['width']; $e = 1e-9;
			$cnt = function ( $L, $H, $n, $lb ) use ( $wd, $e ) {
				$area = (int) ceil( $L * $H * $n * 1.1 / ( $wd * $lb ) - $e );
				$nf = (int) floor( $L / $wd + $e ); $wp = $L - $nf * $wd; $fh = (int) floor( $H / $lb + $e ); $rh = $H - $fh * $lb;
				if ( $wp < 0.01 ) { $wp = 0; } if ( $rh < 0.01 ) { $rh = 0; }
				$cut = $n * $nf * $fh;
				if ( $rh ) { $cut += (int) ceil( $n * $nf / floor( $lb / $rh + $e ) - $e ); }
				if ( $wp ) { $cut += (int) ceil( $n * $fh / floor( $wd / $wp + $e ) - $e ); }
				if ( $wp && $rh ) { $cut += (int) ceil( $n / ( floor( $wd / $wp + $e ) * floor( $lb / $rh + $e ) ) - $e ); }
				return max( $area, $cut );
			};
			$walls = array( array( 3, 2.6, 2, 1, '2.60' ), array( 4, 2.6, 2, 2, '2.60' ), array( 5, 2.8, 2, 2, '2.80' ), array( 10, 3, 1, 1, '3.00' ), array( 100, 3, 1, 1, '3.00' ) );
			$t = '<table><caption>כמה לוחות גבס ורודים של 12.5 מ״מ להזמין לקירות נפוצים (10% פחת)</caption><thead><tr><th>הקיר</th><th>צדדים ושכבות</th><th>לוח</th><th>לוחות</th><th>משקל</th><th>עלות לפי רוטנברג</th></tr></thead><tbody>';
			foreach ( $walls as $w ) {
				list( $L, $H, $s, $ly, $sz ) = $w; $n = $cnt( $L, $H, $s * $ly, (float) $sz ); $kg = $g['kgBoard']['12.5'][ $sz ];
				$pr = isset( $g['price']['fr']['12.5'][ $sz ] ) && 0 === strpos( $g['price']['fr']['12.5'][ $sz ]['src'], 'רוטנברג' ) ? $g['price']['fr']['12.5'][ $sz ]['v'] : 0;
				$t .= '<tr><td>' . esc_html( $L . ' × ' . $H ) . ' מ׳</td><td>' . ( 2 === $s ? 'שני צדדים' : 'צד אחד' ) . ', ' . ( 2 === $ly ? 'שתי שכבות' : 'שכבה אחת' ) . '</td><td>' . esc_html( $sz ) . ' × 1.20</td><td>' . $n . '</td><td>כ־' . number_format( $n * $kg ) . ' ק״ג</td><td>' . ( $pr ? '₪' . number_format( round( $n * $pr ) ) : 'לפי הצעת מחיר' ) . '</td></tr>';
			}
			return '<p>לוח גבס ורוד (מעכב בעירה, FR) לשימוש פנימי, ברוחב 1.20 מ׳. משקל לפי טבלת הספק: 27 ק״ג ללוח 2.60 של 12.5 מ״מ. מחיר אצל רוטנברג ב־25.10.2026: 80.8 ₪ ללוח 2.60 כולל מע״מ. את מספר דקות העמידות באש מקבל הקיר כולו בבדיקה לפי ת״י 931, לא הלוח: לבקש מהקבלן תעודת בדיקה של המחיצה, סיווג לפי ת״י 755 ותו תקן לפי ת״י 1490 חלק 1.</p>' . $t . '</tbody></table>';
		}
		if ( 'pinui' === $id ) {  // G2 /urban-renewal/pinui-binui/: the law's majorities for common building sizes, the 1ד clock, the tax ceiling
			$path = dirname( __DIR__ ) . '/assets/instruments/data/pinui.json';
			$d = is_readable( $path ) ? json_decode( (string) file_get_contents( $path ), true ) : null;
			if ( ! is_array( $d ) || empty( $d['law'] ) ) { return ''; }
			$k = $d['key2025']; $avg = end( $d['series']['approval_to_permit'] );
			$need = function ( $u ) { return ( $u >= 4 && $u <= 5 ) ? 3 : (int) ceil( $u * 3 / 5 - 1e-9 ); };
			$p = '<p>פינוי בינוי לפי חוק פינוי ובינוי (עידוד מיזמי פינוי ובינוי), התשס"ו-2006: רוב מיוחס הוא בעלים של שני שלישים לפחות מהדירות במקבץ, שלוש חמישיות לפחות מהדירות בכל בניין (בבניין של 4 או 5 דירות: 3 דירות ויותר משני בעלי דירות), ויותר ממחצית הרכוש המשותף בכל בניין. '
				. 'בעלי יותר משתי חמישיות מהדירות ומהרכוש המשותף בכל בניין יכולים לבקש מהרשות שמאי פינוי ובינוי בחינם. מהעסקה הראשונה: חצי מבעלי הדירות בתוך שנתיים, שלוש חמישיות בתוך 4 שנים ותכנית בתוך 4.5 שנים, אחרת רוב באסיפה כללית יכול לאפשר ביטול. '
				. 'תקרת הפטור ממס לדירת התמורה: הגבוה מבין 120 מ"ר, 150% מהשווי בניכוי הזכויות שעוברות ליזם, או 50% יותר עד 200 מ"ר. ב-2025 אושרו ' . (int) $k['pb_plans'] . ' תכניות עם ' . number_format( (int) $k['pb_units'] ) . ' דירות, ומאישור תכנית עד היתר ראשון עברו בממוצע ' . esc_html( number_format( (float) $avg[1], 1 ) ) . ' שנים (' . (int) $avg[2] . ' מתחמים, הרשות הממשלתית להתחדשות עירונית).</p>';
			$p .= '<table><caption>כמה חתימות צריך בבניין, לפי מספר הדירות</caption><thead><tr><th>דירות בבניין</th><th>שלוש חמישיות</th><th>שני שלישים (כל המקבץ)</th><th>יותר משתי חמישיות (שמאי הרשות)</th></tr></thead><tbody>';
			foreach ( array( 4, 5, 8, 12, 16, 24, 32, 48 ) as $u ) {
				$p .= '<tr><td>' . $u . '</td><td>' . $need( $u ) . '</td><td>' . (int) ceil( $u * 2 / 3 - 1e-9 ) . '</td><td>' . ( (int) floor( $u * 2 / 5 + 1e-9 ) + 1 ) . '</td></tr>';
			}
			return $p . '</tbody></table>';
		}
		if ( 'urcity' === $id ) {  // G3 /urban-renewal/: the complexes per city on the authority's map and the TAMA 38 line of the 2025 report
			$base = dirname( __DIR__ ) . '/assets/instruments/data/';
			$u = is_readable( $base . 'urcity.json' ) ? json_decode( (string) file_get_contents( $base . 'urcity.json' ), true ) : null;
			$t = is_readable( $base . 'renewal-track.json' ) ? json_decode( (string) file_get_contents( $base . 'renewal-track.json' ), true ) : null;
			if ( ! is_array( $u ) || ! is_array( $t ) || empty( $t['recs'] ) ) { return ''; }
			$lm = -1; foreach ( $t['snaps'] as $i => $s ) { if ( 'map' === $s['k'] ) { $lm = $i; } }
			if ( $lm < 0 ) { return ''; }
			$dt = function ( $iso ) { $p = explode( '-', (string) $iso ); return 3 === count( $p ) ? (int) $p[2] . '.' . (int) $p[1] . '.' . $p[0] : (string) $iso; };
			$c = array(); $n = 0; $appr = 0;
			foreach ( $t['recs'] as $r ) {
				$s = (int) $r['s'][ $lm ]; if ( -1 === $s ) { continue; }
				$x = $r['c']; if ( ! isset( $c[ $x ] ) ) { $c[ $x ] = array( 'n' => 0, 'a' => 0, 'p' => 0, 'pe' => 0, 'pp' => 0 ); }
				$c[ $x ]['n']++; $n++; if ( $s >= 3 ) { $c[ $x ]['a']++; $appr++; }
				$c[ $x ]['p'] += (int) ( $r['p'] ?? 0 ); if ( ! empty( $r['e'] ) && ! empty( $r['p'] ) ) { $c[ $x ]['pe'] += (int) $r['e']; $c[ $x ]['pp'] += (int) $r['p']; }
			}
			uasort( $c, function ( $a, $b ) { return $b['n'] <=> $a['n']; } );
			$tama = array(); foreach ( $u['replace'] as $r ) { $tama[ $r['c'] ] = preg_replace( '/^בבדיקה /u', 'בשלב בדיקה ', (string) $r['st'] ) . ( $r['ext'] ? '' : '; בלי הארכה לתמ"א 38' ); }
			$p = '<p>מתחמי התחדשות עירונית במפת הרשות הממשלתית להתחדשות עירונית, ' . esc_html( $dt( $t['snaps'][ $lm ]['d'] ) ) . ': ' . number_format( $n ) . ' מתחמים ב-' . count( $c ) . ' ערים, ' . number_format( $appr ) . ' מהם בתכנית מאושרת או במימוש. '
				. 'שלושה מסלולים: פינוי בינוי של מתחם, תמ"א 38 לבניין, ותכנית לרישוי מהיר לפי סעיף 145א1. תמ"א 38 פקעה באוקטובר 2023, ובערים שמקדמות תכנית מחליפה הוארכה עד מאי 2026 או עד אישור התכנית, המוקדם מביניהם (דוח הרשות לשנת 2025).</p>';
			$p .= '<table><caption>הערים עם הכי הרבה מתחמים</caption><thead><tr><th>עיר</th><th>מתחמים</th><th>מאושרת או במימוש</th><th>דירות אחרי הבנייה</th><th>מכפיל (חישוב שלנו)</th><th>תמ"א 38 בעיר</th></tr></thead><tbody>';
			foreach ( array_slice( $c, 0, 20, true ) as $x => $v ) {
				$p .= '<tr><td>' . esc_html( $x ) . '</td><td>' . $v['n'] . '</td><td>' . $v['a'] . '</td><td>' . number_format( $v['p'] ) . '</td><td>' . ( $v['pe'] ? esc_html( number_format( $v['pp'] / $v['pe'], 2 ) ) : '' ) . '</td><td>' . esc_html( $tama[ $x ] ?? '' ) . '</td></tr>';
			}
			return $p . '</tbody></table>';
		}
		if ( 'bedek' === $id ) {  // G6 /home-inspection/: the law's periods for every defect type and the published price ranges
			$path = dirname( __DIR__ ) . '/assets/instruments/data/bedek.json';
			$d = is_readable( $path ) ? json_decode( (string) file_get_contents( $path ), true ) : null;
			if ( ! is_array( $d ) || empty( $d['law']['items'] ) ) { return ''; }
			$yrs = function ( $y ) { return 1 === (int) $y ? 'שנה' : (int) $y . ' שנים'; };
			$env = function ( $kind, $rooms = null ) use ( $d ) { $lo = PHP_INT_MAX; $hi = 0; foreach ( $d['prices'] as $s ) { foreach ( $s['rows'] as $r ) { if ( $r[0] !== $kind ) { continue; } if ( null !== $rooms && ! empty( $r[4] ) && ( $rooms < $r[4][0] || $rooms > $r[4][1] ) ) { continue; } $lo = min( $lo, $r[2] ); $hi = max( $hi, $r[3] ); } } return array( $lo, $hi ); };
			$a4 = $env( 'apt', 4 ); $h = $env( 'house' );
			$p = '<p>בדק בית לפי חוק המכר (דירות), התשל"ג-1973: לכל סוג ליקוי תקופת בדק מיום המסירה, ואחריה ' . (int) $d['law']['warranty_y'] . ' שנות אחריות. בתקופת הבדק הקבלן אחראי אלא אם יוכיח שהליקוי נגרם בידי הקונה; '
				. 'בתקופת האחריות הקונה צריך להראות שמקור הליקוי בתכנון, בעבודה או בחומרים. ליקוי יסודי בשלד: ' . (int) $d['law']['struct_y'] . ' שנה. ליקוי שאפשר היה לראות במסירה: הודעה לקבלן בתוך שנה. '
				. 'קונה משנה נהנה מאותן תקופות, מהמסירה לקונה הראשון. מחירים שפורסמו לבדק בית: דירת 4 חדרים ' . number_format( $a4[0] ) . ' עד ' . number_format( $a4[1] ) . ' ₪, בית פרטי ' . number_format( $h[0] ) . ' עד ' . number_format( $h[1] ) . ' ₪ (במידרג כולל מע"מ; אצל השאר לא צוין).</p>';
			$p .= '<table><caption>תקופות הבדק והאחריות לפי סוג הליקוי</caption><thead><tr><th>סוג הליקוי</th><th>תקופת בדק</th><th>הקבלן אחראי בסך הכול</th></tr></thead><tbody>';
			foreach ( $d['law']['items'] as $it ) { $p .= '<tr><td>' . esc_html( $it['law'] ) . '</td><td>' . esc_html( $yrs( $it['y'] ) ) . '</td><td>' . esc_html( ( (int) $it['y'] + (int) $d['law']['warranty_y'] ) . ' שנים' ) . '</td></tr>'; }
			$p .= '<tr><td>אי התאמה יסודית בשלד וביציבות</td><td>' . (int) $d['law']['struct_y'] . ' שנה</td><td>' . (int) $d['law']['struct_y'] . ' שנה</td></tr>';
			return $p . '</tbody></table>';
		}
		if ( 'shamai' === $id || 'shamaireg' === $id ) {  // G7 /real-estate-appraiser/: who orders and pays, the deadlines, the decisive appraiser's fee, the register
			$path = dirname( __DIR__ ) . '/assets/instruments/data/shamai.json';
			$d = is_readable( $path ) ? json_decode( (string) file_get_contents( $path ), true ) : null;
			if ( ! is_array( $d ) || empty( $d['purposes'] ) ) { return ''; }
			$r = $d['register']; $dt = function ( $iso ) { $x = explode( '-', (string) $iso ); return 3 === count( $x ) ? (int) $x[2] . '.' . (int) $x[1] . '.' . $x[0] : (string) $iso; };
			if ( 'shamaireg' === $id ) {
				return '<p>פנקס שמאי המקרקעין של משרד המשפטים: ' . number_format( (int) $r['count'] ) . ' שמאים מורשים (עודכן ' . esc_html( $dt( $r['updated'] ) ) . '). לפי חוק שמאי מקרקעין, שמאי מקרקעין הוא מי שרשום בפנקס, '
					. 'ורק הוא רשאי לעשות שומת מקרקעין בשכר. בודקים שמאי לפי שם או מספר רישיון במאגר הרשמי: <a href="' . esc_url( $r['page'] ) . '">מאגר שמאי מקרקעין ב-data.gov.il</a>.</p>';
			}
			$fee = function ( $a ) use ( $d ) { $f = 0; foreach ( $d['decisive']['table'] as $b ) { $hi = $b[1] ? $b[1] : PHP_INT_MAX; if ( $a > $b[0] ) { $f += ( min( $a, $hi ) - $b[0] ) * $b[2]; } } return max( $d['decisive']['min'], min( $d['decisive']['max'], $f ) ); };
			$p = '<p>שמאי מקרקעין: ' . number_format( (int) $r['count'] ) . ' שמאים רשומים בפנקס של משרד המשפטים. ערר על היטל השבחה או בקשה לשמאי מכריע: בתוך ' . (int) $d['decisive']['appeal_days'] . ' ימים מהיום שהשומה הובאה לידיעת החייב. '
				. 'תביעה לפי סעיף 197: בתוך ' . (int) $d['s197_years'] . ' שנים מתחילת תוקף התכנית. שכר שמאי מכריע לפי התקנות: 3% עד 500,000 ₪, 2% עד מיליון, 1% עד 2 מיליון ו-0.5% מעל, לפחות ' . number_format( (int) $d['decisive']['min'] ) . ' ₪ ולכל היותר '
				. number_format( (int) $d['decisive']['max'] ) . ' ₪, ועוד מע"מ, מחצית לכל צד. על השבחה של מיליון ₪: ' . number_format( $fee( 1000000 ) ) . ' ₪.</p>';
			$p .= '<table><caption>איזו שומה צריך: מי מזמין, מי משלם ומה המועד</caption><thead><tr><th>מטרה</th><th>מי מזמין</th><th>מי משלם</th><th>מועד בחוק</th></tr></thead><tbody>';
			foreach ( $d['purposes'] as $x ) {
				$dl = empty( $x['deadline'] ) ? 'אין' : ( ! empty( $x['deadline']['days'] ) ? (int) $x['deadline']['days'] . ' ימים' : (int) $x['deadline']['years'] . ' שנים' );
				$p .= '<tr><td>' . esc_html( $x['label'] ) . '</td><td>' . esc_html( $x['who_s'] ) . '</td><td>' . esc_html( $x['pay_s'] ) . '</td><td>' . esc_html( $dl ) . '</td></tr>';
			}
			return $p . '</tbody></table>';
		}
		if ( 'orechdin' === $id ) {  // G8 /real-estate-lawyer/: the developer's-lawyer cap by price, the Bar's recommended tariff, the registry fees
			$path = dirname( __DIR__ ) . '/assets/instruments/data/orechdin.json';
			$d = is_readable( $path ) ? json_decode( (string) file_get_contents( $path ), true ) : null;
			if ( ! is_array( $d ) || empty( $d['cap'] ) ) { return ''; }
			$c = $d['cap']; $t = $d['tariff']; $f = array(); foreach ( $d['land'] as $x ) { $f[ $x[0] ] = $x[2]; }
			$tar = function ( $v ) use ( $t ) { if ( $v > $t['top'] ) { return $t['top_min']; } $s = 0; foreach ( $t['tiers'] as $b ) { if ( $v > $b[0] ) { $s += ( min( $v, $b[1] ) - $b[0] ) * $b[2]; } } return max( $t['min'], $s ); };
			$p = '<p>עורך דין מקרקעין: משרדים פרסמו ב-2026 שכר טרחה של כ-0.5% ממחיר הדירה ועוד מע"מ, עד 1%, עם מינימום של כ-5,000 עד 6,000 ₪. התעריף המינימלי המומלץ של לשכת עורכי הדין (המלצה שאינה מחייבת) לעריכת חוזה על 2 מיליון ₪: '
				. number_format( $tar( 2000000 ) ) . ' ₪. בדירה חדשה הקבלן רשאי לגבות מהקונה על עורך הדין שלו לכל היותר ' . number_format( (int) $c['fixed'] ) . ' ₪ (' . (int) $c['year'] . ') או 0.5% מהמחיר, הנמוך מביניהם, ועוד מע"מ, ועוד עד '
				. number_format( (int) $c['list_fee'] ) . ' ₪ לניהול רשימת הזכויות; מעל ' . number_format( (int) $c['ceiling'] ) . ' ₪ אין תקרה. אגרות הטאבו: הערת אזהרה ' . (int) $f['warn'] . ' ₪, רישום מכר ' . (int) $f['sale'] . ' ₪, רישום משכנתה ' . (int) $f['mortgage'] . ' ₪. '
				. 'הצהרה לרשות המסים בתוך 30 יום ומס רכישה בתוך 60 יום. המידע כללי ואינו ייעוץ משפטי.</p>';
			$p .= '<table><caption>מה מותר לקבלן לגבות על עורך הדין שלו, לפי מחיר הדירה</caption><thead><tr><th>מחיר הדירה</th><th>המרבי לפני מע"מ</th></tr></thead><tbody>';
			foreach ( array( 1000000, 1500000, 2000000, 3000000, 4000000, 5000000 ) as $v ) { $m = $v > $c['ceiling'] ? 'אין תקרה' : number_format( min( $c['fixed'], $v * $c['pct'] ) ) . ' ₪'; $p .= '<tr><td>' . number_format( $v ) . ' ₪</td><td>' . esc_html( $m ) . '</td></tr>'; }
			return $p . '</tbody></table>';
		}
		if ( 'rentfair' === $id ) {  // G5: national medians by size, the CBS average of the 18 cities, the guarantee cap and the tax ceiling, from rent.json
			$path = dirname( __DIR__ ) . '/assets/instruments/data/rent.json';
			$x = is_readable( $path ) ? json_decode( (string) file_get_contents( $path ), true ) : null;
			if ( ! is_array( $x ) || empty( $x['cities'] ) ) { return ''; }
			$f = function ( $n ) { return esc_html( number_format( (float) $n ) ); };
			$n = $x['nat']['r']; $q = $n['4']['q']; $qm = array( '03' => 'ינואר עד מרץ', '06' => 'אפריל עד יוני', '09' => 'יולי עד ספטמבר', '12' => 'אוקטובר עד דצמבר' );
			$ql = $qm[ substr( $q, 5, 2 ) ] . ' ' . substr( $q, 0, 4 );
			$h = '<p>שכר הדירה החציוני בישראל, ' . esc_html( $ql ) . ' (אתר הנדל״ן הממשלתי): ' . $f( $n['3']['v'] ) . ' ₪ לדירת 3 חדרים, ' . $f( $n['4']['v'] ) . ' ₪ ל־4 חדרים, ' . $f( $n['5']['v'] ) . ' ₪ ל־5 חדרים. '
				. 'הערובה שמותר לבקש כשהיא עולה לשוכר כסף: הנמוך מבין 3 חודשי שכירות ושליש משכר הדירה לכל התקופה. פטור ממס למשכיר ב־' . (int) $x['tax']['year'] . ': עד ' . $f( $x['tax']['ceiling'] ) . ' ₪ בחודש.</p>'
				. '<table><thead><tr><th>עיר</th><th>3 חדרים</th><th>4 חדרים</th><th>5 חדרים</th><th>ממוצע הלמ״ס, כל הגדלים</th></tr></thead><tbody>';
			foreach ( $x['cities'] as $c ) {
				if ( empty( $c['cbs']['total'] ) ) { continue; }  // the 18 cities the CBS measures; the full 72 are in the page's own table
				$cell = function ( $k ) use ( $c, $f ) { return isset( $c['r'][ $k ] ) ? $f( $c['r'][ $k ]['v'] ) . ' ₪' : ''; };
				$h .= '<tr><td>' . esc_html( $c['n'] ) . '</td><td>' . $cell( '3' ) . '</td><td>' . $cell( '4' ) . '</td><td>' . $cell( '5' ) . '</td><td>' . $f( $c['cbs']['total']['a'] ) . ' ₪</td></tr>';
			}
			return $h . '</tbody></table>';
		}
		if ( 'dirafit' === $id || 'diracost' === $id ) { // G1: round 11 by town and the rules, from dira-round.json
			$path = dirname( __DIR__ ) . '/assets/instruments/data/dira-round.json';
			$x = is_readable( $path ) ? json_decode( (string) file_get_contents( $path ), true ) : null;
			if ( ! is_array( $x ) || empty( $x['towns'] ) ) { return ''; }
			$r = $x['r11']; $f = function ( $n, $d = 0 ) { return esc_html( number_format( (float) $n, $d ) ); };
			if ( 'dirafit' === $id ) {
				$t = $x['towns']; usort( $t, function ( $a, $b ) { return $b['per100'] <=> $a['per100']; } );
				$rest = ( $r['units'] - $r['res_wins'] ) / max( 1, $r['households'] - $r['res_regs'] );
				$h = '<p>מי זכאי לדירה בהנחה: חסרי דירה (בלי דירה, או עד שליש דירה, ב־3 השנים האחרונות) שהם זוג נשוי או ידועים בציבור, זוג שמתחתן בתוך 3 חודשים, יחידים מגיל 35, הורה עם ילד רווק מתחת לגיל 21, נכים ואלמנים מגיל 21. משפרי דיור נרשמים רק להגרלות המשך. לא זכאים: מי שהחזיק שתי דירות במקביל, מי שכבר קנה בתוכנית של מחיר מפוקח, וחברי קיבוץ. אישור זכאות: 200 ₪, עד 10 ימי עבודה. בהגרלה ה־11 נרשמו '
					. $f( $r['households'] ) . ' משקי בית ל־' . $f( $r['units'] ) . ' דירות ב־19 יישובים; זכו ' . $f( 100 * $r['units'] / $r['households'], 1 ) . '% מכלל משקי הבית, '
					. $f( 100 * $r['res_wins'] / $r['res_regs'], 1 ) . '% ממשרתי המילואים ו־' . $f( 100 * $rest, 1 ) . '% מכל השאר (החישוב שלנו, לפי משרד הבינוי והשיכון).</p>'
					. '<table><thead><tr><th>עיר</th><th>דירות</th><th>משקי בית שנרשמו</th><th>דירות לכל 100 נרשמים</th><th>הסיכוי בהגרלה בקובץ</th><th>בני מקום בקובץ</th></tr></thead><tbody>';
				foreach ( $t as $c ) {
					$o = $c['hist']['odds']; $l = $c['hist']['lodds'];
					$h .= '<tr><td>' . esc_html( $c['n'] ) . '</td><td>' . $f( $c['units'] ) . '</td><td>' . $f( $c['hh'] ) . '</td><td>' . $f( $c['per100'], $c['per100'] < 1 ? 2 : 1 ) . '</td><td>'
						. ( null === $o ? 'אין' : $f( 100 * $o, 2 ) . '%' ) . '</td><td>' . ( null === $l ? 'אין' : $f( 100 * $l, 2 ) . '%' ) . '</td></tr>';
				}
				return $h . '</tbody></table>';
			}
			$h = '<p>המימון של זוכה בדירה בהנחה: משכנתא עד 75% מהמחיר, או לפי שווי שמאי באישור בנק ישראל עם 100,000 ₪ הון עצמי לפחות ושווי עד 2.1 מיליון ₪; מענק של 40,000 או 60,000 ₪ ביישובים מזכים. המחיר למ״ר בהגרלה מוצג לפני מע״מ. המחיר האחרון בקובץ הרשמי מול חציון העסקאות של דירות 4 חדרים בעיר, לדירה של 100 מ״ר עם מע״מ (החישוב שלנו):</p>'
				. '<table><thead><tr><th>עיר</th><th>מחיר למ״ר</th><th>תאריך</th><th>דירת 100 מ״ר עם מע״מ</th><th>חציון 4 חדרים</th><th>הפער</th></tr></thead><tbody>';
			foreach ( $x['towns'] as $c ) {
				if ( empty( $c['pm'] ) || empty( $c['mkt']['4'] ) || $c['pm']['date'] < '2024-01-01' ) { continue; }
				$p = $c['pm']['v'] * 100 * 1.18; $m = $c['mkt']['4']['price'];
				$h .= '<tr><td>' . esc_html( $c['n'] ) . '</td><td>' . $f( $c['pm']['v'] ) . ' ₪</td><td>' . esc_html( date_i18n( 'j.n.Y', strtotime( $c['pm']['date'] ) ) ) . '</td><td>' . $f( $p ) . ' ₪</td><td>' . $f( $m ) . ' ₪</td><td>' . $f( 100 * ( $m - $p ) / $m, 1 ) . '%</td></tr>';
			}
			return $h . '</tbody></table>';
		}
		if ( 'sdplan' === $id ) {  // S1 (Sde Dov hub moat): every plot of the district with its stage, as plain text (the map needs the script)
			$path = dirname( __DIR__ ) . '/assets/instruments/data/sdplan.json';
			$d = is_readable( $path ) ? json_decode( (string) file_get_contents( $path ), true ) : null;
			if ( ! is_array( $d ) || empty( $d['plots'] ) || empty( $d['stages'] ) ) { return ''; }
			$dt = function ( $iso ) { $p = explode( '-', (string) $iso ); return 3 === count( $p ) ? (int) $p[2] . '.' . (int) $p[1] . '.' . $p[0] : (string) $iso; };
			$cn = array( 'eshkol' => 'מתחם אשכול', 'merkaz' => 'מרכז הרובע', 'tzafon' => 'צפון הרובע' );
			$use = array( 'res' => 'מגורים', 'special' => 'דיור מוגן ודיור מיוחד', 'hotel' => 'מלונאות', 'biz' => 'תעסוקה ומסחר' );
			$st = $d['stages']; $by = array_fill( 0, count( $st ), 0 ); $units = 0; $open = 0;
			$num = function ( $id ) { return (int) preg_replace( '/\D/', '', (string) $id ); };
			foreach ( $d['plots'] as $r ) {
				$by[ (int) $r['s'] ]++;
				if ( ! empty( $r['open'] ) ) { $open++; }
				if ( ! empty( $r['t']['units'] ) ) {
					$first = true; foreach ( (array) ( $r['t']['with'] ?? array() ) as $w ) { if ( $num( $w ) < $num( $r['id'] ) ) { $first = false; } }
					if ( $first ) { $units += (int) $r['t']['units']; }
				}
			}
			$cell = function ( $r ) use ( $st, $dt ) {
				$s = $st[ (int) $r['s'] ];
				if ( ! empty( $r['open'] ) ) { return $s . ', מכרז פתוח עד ' . $dt( $r['open']['close'] ); }
				if ( ! empty( $r['nobid'] ) && empty( $r['t'] ) ) { return $s . ', מכרז בלי הצעות'; }
				if ( 5 === (int) $r['s'] && ! empty( $r['works']['start'] ) ) { return $s . ' מ-' . $dt( $r['works']['start'] ); }
				if ( 4 === (int) $r['s'] && ! empty( $r['permit']['first'] ) ) { return $s . ' ' . $dt( $r['permit']['first'] ); }
				if ( 3 === (int) $r['s'] && ! empty( $r['req']['open'] ) ) { return $s . ' ' . $dt( $r['req']['open'] ); }
				if ( 2 === (int) $r['s'] && ! empty( $r['design'] ) ) { return $s . ' ' . $dt( $r['design'] ); }
				if ( 1 === (int) $r['s'] && ! empty( $r['t']['close'] ) ) { return $s . ' ' . $dt( $r['t']['close'] ); }
				return $s;
			};
			$who = function ( $r ) use ( $use ) {
				if ( ! empty( $r['p']['n'] ) ) { return $r['p']['n']; }
				if ( ! empty( $r['t']['winner'] ) ) { return $r['t']['winner']; }
				if ( ! empty( $r['open'] ) ) { return 'במכרז פתוח'; }
				if ( ! empty( $r['nobid'] ) ) { return 'לא הוגשו הצעות'; }
				return $use[ $r['use'] ] ?? '';
			};
			$parts = array(); foreach ( $st as $i => $s ) { if ( $by[ $i ] ) { $parts[] = $s . ': ' . number_format( $by[ $i ] ); } }
			$p = '<p>רובע שדה דב, ' . esc_html( $dt( $d['built'] ) ) . ': ' . number_format( count( $d['plots'] ) ) . ' מגרשים למגורים, למלונאות ולתעסוקה בשלוש התכניות (תמ״ל/3001, תא/1/4444, תא/2/4444). '
				. esc_html( implode( '; ', $parts ) ) . '. במכרזי רשות מקרקעי ישראל שווקו ' . number_format( $units ) . ' יחידות דיור, ו־' . number_format( $open ) . ' מגרשים במכרז פתוח. '
				. 'השלב הוא הרישום הרשמי האחרון: תוצאות המכרז, תכנית העיצוב, הבקשה להיתר, ההיתר ותחילת העבודות לפי העירייה. המרחקים בקו אווירי. אין כאן מועד מסירה או אכלוס.</p>';
			$t = '<table><caption>כל המגרשים ברובע שדה דב והשלב שלהם (' . count( $d['plots'] ) . ')</caption><thead><tr><th>מגרש</th><th>מתחם</th><th>פרויקט או זוכה</th><th>יח״ד</th><th>השלב היום</th><th>תחנת הקו הירוק הקרובה</th></tr></thead><tbody>';
			$order = array( 'eshkol' => 0, 'merkaz' => 1, 'tzafon' => 2 ); $rows = $d['plots'];
			usort( $rows, function ( $a, $b ) use ( $order, $num ) { return ( $order[ $a['c'] ] - $order[ $b['c'] ] ) ?: ( $num( $a['id'] ) - $num( $b['id'] ) ); } );
			foreach ( $rows as $r ) {
				$u = ! empty( $r['t']['units'] ) ? number_format( (int) $r['t']['units'] ) : ( ! empty( $r['open']['units'] ) ? number_format( (int) $r['open']['units'] ) : '' );
				$t .= '<tr><td>' . esc_html( $r['id'] ) . '</td><td>' . esc_html( $cn[ $r['c'] ] ?? '' ) . '</td><td>' . esc_html( $who( $r ) ) . '</td><td>' . $u . '</td><td>' . esc_html( $cell( $r ) ) . '</td><td>' . esc_html( $r['st'][0] . ', כ־' . number_format( (int) $r['st'][1] ) . ' מ׳' ) . '</td></tr>';
			}
			return $p . $t . '</tbody></table>';
		}
		if ( 'urtrack' === $id ) {  // 1.72.528 (Q1 moat): the "מה זז במאגר" count line and every change between the snapshots (T8), the words of tools/urtrack.js
			$path = dirname( __DIR__ ) . '/assets/instruments/data/renewal-track.json';
			$d = is_readable( $path ) ? json_decode( (string) file_get_contents( $path ), true ) : null;
			if ( ! is_array( $d ) || empty( $d['recs'] ) || empty( $d['agg'] ) ) { return ''; }
			$dt = function ( $iso ) { $p = explode( '-', (string) $iso ); return 3 === count( $p ) ? (int) $p[2] . '.' . (int) $p[1] . '.' . $p[0] : (string) $iso; };
			$st = array( 'ללא שלב', 'תכנון ראשוני', 'תכנון סטטוטורי', 'תכנית מאושרת', 'במימוש', 'אחרי רישוי' );
			$kind = array( 'new' => 'נוסף', 'up' => 'עלה שלב', 'down' => 'ירד שלב', 'chg' => 'השלב השתנה', 'gone' => 'ירד מהרשימה', 'back' => 'חזר לרשימה', 'trk' => 'המסלול השתנה', 'renum' => 'מספר מתחם חדש' );
			$order = array( 'up' => 0, 'new' => 1, 'down' => 2, 'chg' => 3, 'trk' => 4, 'renum' => 5, 'back' => 6, 'gone' => 7 );
			$s = function ( $i ) use ( $st ) { return $st[ max( 0, (int) $i ) ]; };
			$ft = function ( $c ) use ( $s, $d ) {
				switch ( $c[1] ) {
					case 'new':
					case 'back': return 'נכנס: ' . $s( $c[3] );
					case 'gone': return 'אחרון: ' . $s( $c[2] );
					case 'trk': return $d['tracks'][ (int) $c[2] ] . ' ← ' . $d['tracks'][ (int) $c[3] ];
					case 'renum': return $c[2] . ' ← ' . $c[3];
					default: return $s( $c[2] ) . ' ← ' . $s( $c[3] );
				}
			};
			$rows = array();
			foreach ( $d['recs'] as $r ) { foreach ( (array) ( $r['ch'] ?? array() ) as $c ) { $rows[] = array( $r, $c ); } }
			usort( $rows, function ( $x, $y ) use ( $order ) {
				return strcmp( $y[1][0], $x[1][0] ) ?: ( ( $order[ $x[1][1] ] ?? 9 ) - ( $order[ $y[1][1] ] ?? 9 ) ) ?: strcmp( $x[0]['c'], $y[0]['c'] ) ?: strcmp( $x[0]['n'], $y[0]['n'] );
			} );
			$a = $d['agg'];
			$pl = function ( $n, $one, $many ) { return number_format( (int) $n ) . ' ' . ( 1 === (int) $n ? $one : $many ); };
			$p = array( ( 1 === (int) $a['added'] ? 'נוסף ' : 'נוספו ' ) . $pl( $a['added'], 'מתחם', 'מתחמים' ), $pl( $a['up'], 'עלה שלב', 'עלו שלב' ) );
			if ( ! empty( $a['down'] ) ) { $p[] = $pl( $a['down'], 'ירד שלב', 'ירדו שלב' ); }
			if ( ! empty( $a['chg'] ) ) { $p[] = $pl( $a['chg'], 'שינה שלב', 'שינו שלב' ); }
			if ( ! empty( $a['gone'] ) ) { $p[] = $pl( $a['gone'], 'לא מופיע עוד', 'לא מופיעים עוד' ); }
			if ( ! empty( $a['renum'] ) ) { $p[] = $pl( $a['renum'], 'קיבל מספר מתחם חדש', 'קיבלו מספר מתחם חדש' ); }
			$last = array_pop( $p );
			$line = 'מאז ' . $dt( $a['since'] ) . ' ' . ( $p ? implode( ', ', $p ) . ' ו-' : '' ) . $last . ' (קובץ data.gov.il מול מפת הרשות של ' . $dt( $a['to'] ) . ').';
			$snaps = array(); $now = 0;
			foreach ( $d['snaps'] as $x ) { $snaps[] = $x['label'] . ' ' . $dt( $x['d'] ); if ( 'map' === $x['k'] ) { $now = (int) $x['n']; } }
			$t = '<table><caption>מה זז במאגר: כל השינויים בין הבדיקות (' . count( $rows ) . ')</caption><thead><tr><th>מתחם</th><th>עיר</th><th>מה השתנה</th><th>משלב ← לשלב</th><th>תאריך הבדיקה</th></tr></thead><tbody>';
			foreach ( $rows as $x ) {
				$t .= '<tr><td>' . esc_html( $x[0]['n'] ) . '</td><td>' . esc_html( $x[0]['c'] ) . '</td><td>' . esc_html( $kind[ $x[1][1] ] ?? $x[1][1] ) . '</td><td>' . esc_html( $ft( $x[1] ) ) . '</td><td>' . esc_html( $dt( $x[1][0] ) ) . '</td></tr>';
			}
			return '<p>' . esc_html( $line ) . ' במפת הרשות היום ' . number_format( $now ) . ' מתחמים. הבדיקות: ' . esc_html( implode( ', ', $snaps ) ) . '. כל שינוי מתוארך לבדיקה הראשונה שבה ראינו אותו. אין כאן שנת התחלת בנייה או אכלוס: המקורות לא מפרסמים אותן.</p>' . $t . '</tbody></table>';
		}
		if ( 't466' === $id ) {  // 1.72.522: which part of the concrete code governs each element, as plain text (the drawing needs the script)
			$path = dirname( __DIR__ ) . '/assets/instruments/data/t466.json';
			$d = is_readable( $path ) ? json_decode( (string) file_get_contents( $path ), true ) : null;
			if ( ! is_array( $d ) || empty( $d['parts'] ) ) { return ''; }
			$p = $d['parts'];
			$rows = array( array( 'כל המבנה', '1' ), array( 'יסודות, עמודים ותקרות יצוקות', '2' ), array( 'תקרה או קורה דרוכה', '3' ), array( 'חזית ואלמנטים טרומיים', '4' ), array( 'תקרת לוח״דים (מטבלות חלולות)', '5' ) );
			$t = '<table><caption>איזה חלק של ת״י 466 חל על כל אלמנט בבניין (לפי מכון התקנים, 25.10.2026)</caption><thead><tr><th>האלמנט</th><th>החלק</th><th>מהדורה בתוקף</th><th>מחיר במכון התקנים</th></tr></thead><tbody>';
			foreach ( $rows as $r ) { $x = $p[ $r[1] ]; $t .= '<tr><td>' . esc_html( $r[0] ) . '</td><td>חלק ' . esc_html( $r[1] ) . ': ' . esc_html( $x['name'] ) . '</td><td>' . esc_html( $x['ed'] ) . '</td><td>' . esc_html( number_format( $x['price'], 2 ) ) . ' ₪</td></tr>'; }
			return '<p>חלק 1 של חוקת הבטון חל על כל המבנה, וחלק 2 על רכיבי הבטון המזוין והלא מזוין. לתקרות דרוכות חל חלק 3, לאלמנטים טרומיים חלק 4 ולתקרות מטבלות חלולות חלק 5. את התקן קונים במכון התקנים או קוראים בו בלי תשלום במרכז המידע, ' . esc_html( $d['sii']['addr'] ) . ', בתיאום מראש.</p>' . $t . '</tbody></table>';
		}
		if ( 'dkpick' === $id || 'dkquote' === $id ) {  // 1.72.522: the Dekel rules as plain text; no Dekel price is stored or shown
			$path = dirname( __DIR__ ) . '/assets/instruments/data/dekel.json';
			$d = is_readable( $path ) ? json_decode( (string) file_get_contents( $path ), true ) : null;
			if ( ! is_array( $d ) || empty( $d['lists'] ) ) { return ''; }
			if ( 'dkquote' === $id ) {
				$r = $d['rules'];
				$t = '<table><caption>מה לבדוק בהצעת מחיר מול מחירון דקל (לפי אתר דקל, 25.10.2026)</caption><thead><tr><th>הנושא</th><th>מה קובע דקל</th><th>מה לשאול את הקבלן</th></tr></thead><tbody>';
				foreach ( array( array( 'מה כלול במחיר', $r['incl'], 'מה לא כלול בסעיף?' ), array( 'הריסה ופינוי', $r['demo'], 'מי משלם את אגרת ההטמנה?' ), array( 'ברזל לבטון', $r['steel'], 'האם הברזל כלול במחיר הבטון?' ),
					array( 'אזור מרוחק', $r['remote'], 'מה התוספת שחושבה?' ), array( 'לילה, שבת וחג', $r['night'], 'האם התוספת מופיעה בנפרד?' ), array( 'מהדורה', $r['monthly'], 'לפי איזו מהדורה התמחור?' ) ) as $x ) {
					$t .= '<tr><td>' . esc_html( $x[0] ) . '</td><td>' . esc_html( $x[1] ) . '</td><td>' . esc_html( $x[2] ) . '</td></tr>';
				}
				return '<p>מחירון דקל הוא מחיר ייחוס, לא חוזה. משווים כל סעיף בהצעה למחיר היחידה בדקל מהמהדורה של אותו חודש, ובודקים את הכללים של דקל עצמו.</p>' . $t . '</tbody></table>';
			}
			$t = '<table><caption>איזה מחירון של דקל לאיזו עבודה (לפי אתר דקל, 25.10.2026)</caption><thead><tr><th>העבודה</th><th>המחירון</th><th>היקף שהמחירים מכוונים אליו</th></tr></thead><tbody>';
			foreach ( $d['kinds'] as $k ) { $l = $d['lists'][ $k['list'] ]; $t .= '<tr><td>' . esc_html( $k['label'] ) . '</td><td>' . esc_html( $l['name'] ) . '</td><td>' . ( ! empty( $l['min'] ) ? esc_html( number_format( $l['min'] ) . ' עד ' . number_format( $l['max'] ) ) . ' ₪' : '' ) . '</td></tr>'; }
			return '<p>מחירון דקל לבנייה ותשתיות כולל ' . (int) $d['lists']['build']['ch'] . ' פרקים ו' . esc_html( $d['lists']['build']['items'] ) . ' סעיפים, ומתעדכן בכל 1 לחודש. מחיר כל סעיף כולל עבודה, חומרים ורווח קבלן. הגישה במנוי בתשלום: ' . esc_html( $d['contact'] ) . '.</p>' . $t . '</tbody></table>';
		}
		// 1.72.587 (HAD-675): the quick calculator as plain text (inc/mortgage-market.php)
		if ( 'mquick' === $id ) { return function_exists( 'nadlan_mm_quick_summary' ) ? nadlan_mm_quick_summary() : ''; }
		// 1.72.523 (HAD-601, U1): Mortgage 2.0 as plain text
		if ( 'mortgage' === $id ) {
			$path = dirname( __DIR__ ) . '/assets/instruments/data/boi-mortgage.json';
			$d = is_readable( $path ) ? json_decode( (string) file_get_contents( $path ), true ) : null;
			if ( ! is_array( $d ) || empty( $d['rates'] ) ) { return ''; }
			$m = $d['market']['month']; $mm = (int) substr( $m, 5 ) . '.' . substr( $m, 0, 4 );
			return '<p>ריבית ממוצעת במשכנתאות חדשות לפי בנק ישראל (' . esc_html( $mm ) . '): קבועה לא צמודה ' . esc_html( number_format( $d['rates']['fixed_nl']['rate'], 2 ) ) . '%, קבועה צמודה '
				. esc_html( number_format( $d['rates']['fixed_cpi']['rate'], 2 ) ) . '%, משתנה צמודה ' . esc_html( number_format( $d['rates']['var_cpi']['rate'], 2 ) ) . '%. ריבית בנק ישראל '
				. esc_html( number_format( $d['policy']['rate'], 2 ) ) . '%, פריים ' . esc_html( number_format( $d['policy']['prime'], 2 ) ) . '%. ' . esc_html( number_format( $d['market']['loans'] ) ) . ' משכנתאות חדשות בחודש, בממוצע '
				. esc_html( number_format( $d['market']['avg_loan'] ) ) . ' ₪ למשכנתא.</p>';
		}
		if ( 'invest' === $id ) {  // U2 /investment/: the yield and cash-flow map as text and a table
			$path = dirname( __DIR__ ) . '/assets/instruments/data/invest.json';
			$x = is_readable( $path ) ? json_decode( (string) file_get_contents( $path ), true ) : null;
			if ( ! is_array( $x ) || empty( $x['rows'] ) ) { return ''; }
			$L = $x['rules']; $rate = (float) $L['rates'][0]['rate']; $r = $rate / 1200; $af = ( 1 - pow( 1 + $r, -300 ) ) / $r;
			$qm = array( '03' => 'ינואר עד מרץ', '06' => 'אפריל עד יוני', '09' => 'יולי עד ספטמבר', '12' => 'אוקטובר עד דצמבר' );
			$hm = array( 'ינואר', 'פברואר', 'מרץ', 'אפריל', 'מאי', 'יוני', 'יולי', 'אוגוסט', 'ספטמבר', 'אוקטובר', 'נובמבר', 'דצמבר' );
			$ql = function ( $q ) use ( $qm ) { $p = explode( '-', $q ); return ( isset( $qm[ $p[1] ] ) ? $qm[ $p[1] ] : $p[1] ) . ' ' . $p[0]; };
			$list = array(); $g = array(); $pos = 0;
			foreach ( $x['rows'] as $c ) {
				if ( ! empty( $c['nat'] ) || empty( $c['r']['4'] ) || $x['cityQ'] !== $c['r']['4']['q'] ) { continue; }
				$p = $c['r']['4']; $pay = 0.5 * $p['price'] / $af; $g[] = $p['rent'] * 12 / $p['price']; if ( $p['rent'] > $pay ) { $pos++; }
				$list[] = array( $c['n'], $p['rent'], $p['price'], $p['rent'] * 12 / $p['price'], $pay, $p['rent'] * $af / $p['price'] );
			}
			$n = count( $list ); if ( ! $n ) { return ''; }
			usort( $list, function ( $a, $b ) { return $b[5] <=> $a[5]; } );
			sort( $g ); $med = $n % 2 ? $g[ intdiv( $n, 2 ) ] : ( $g[ $n / 2 - 1 ] + $g[ $n / 2 ] ) / 2;
			$nat = $x['rows'][0]['r']['4']; $pm = explode( '-', $L['ratesPeriod'] ); $ex = $L['ptax']['extra'];
			$rows = '';
			foreach ( $list as $c ) { $rows .= '<tr><td>' . esc_html( $c[0] ) . '</td><td>' . number_format( $c[1] ) . '</td><td>' . number_format( $c[2] ) . '</td><td>' . number_format( 100 * $c[3], 2 ) . '%</td><td>' . number_format( round( $c[4] ) ) . '</td><td>' . number_format( 100 * $c[5], 1 ) . '%</td></tr>'; }
			return '<p>תשואה ברוטו על דירת 4 חדרים לפי החציונים הרשמיים של אתר הנדל״ן הממשלתי, ' . esc_html( $ql( $x['cityQ'] ) ) . ' (החישוב שלנו): חציון של ' . number_format( 100 * $med, 1 ) . '% ב־' . $n . ' ערים. בחציון הארצי של '
				. esc_html( $ql( $nat['q'] ) ) . ': מחיר ' . number_format( $nat['price'] ) . ' ₪, שכר דירה ' . number_format( $nat['rent'] ) . ' ₪, תשואה ברוטו ' . number_format( 100 * $nat['rent'] * 12 / $nat['price'], 2 ) . '%. במשכנתא של 50% לדירה נוספת, 25 שנה בריבית '
				. number_format( $rate, 2 ) . '% (הממוצע של בנק ישראל ב' . esc_html( $hm[ (int) $pm[1] - 1 ] . ' ' . $pm[0] ) . '), כל 100,000 ₪ עולים ' . number_format( round( 100000 / $af ) ) . ' ₪ בחודש, ושכר הדירה מכסה את ההחזר ב־' . $pos . ' מתוך ' . $n
				. ' ערים. מס רכישה על דירה נוספת: ' . number_format( 100 * $ex[0][1] ) . '% עד ' . number_format( $ex[0][0] ) . ' ₪ ו־' . number_format( 100 * $ex[1][1] ) . '% מעל, עד ' . esc_html( date_i18n( 'j.n.Y', strtotime( $L['ptax']['until']['extra'] ) ) ) . '.</p>'
				. '<table><caption>כמה מהדירה שכר הדירה קונה: ' . $n . ' ערים, 4 חדרים, ' . esc_html( $ql( $x['cityQ'] ) ) . ', משכנתא 50% ל־25 שנה בריבית ' . number_format( $rate, 2 ) . '% (החישוב שלנו)</caption><thead><tr><th>עיר</th><th>שכר דירה חציוני (₪)</th><th>מחיר חציוני (₪)</th><th>תשואה ברוטו</th><th>החזר חודשי (₪)</th><th>כמה מהדירה שכר הדירה קונה</th></tr></thead><tbody>' . $rows . '</tbody></table>';
		}
		if ( 'dktool' === $id || 'dkboq' === $id ) {  // 1.72.525: the Dekel software map as plain text; no Dekel price is stored or shown
			$path = dirname( __DIR__ ) . '/assets/instruments/data/dekel.json';
			$d = is_readable( $path ) ? json_decode( (string) file_get_contents( $path ), true ) : null;
			if ( ! is_array( $d ) || empty( $d['sw'] ) ) { return ''; }
			if ( 'dkboq' === $id ) {
				return '<p>קוד סעיף במחירון דקל בנוי מפרק, תת פרק וסעיף, למשל 68.035.0010 במסמכי מכרז. העלות של שורה בכתב כמויות היא הכמות כפול מחיר היחידה מהמהדורה של החודש; לסיכום מוסיפים בצ"מ, אם רוצים, ומע"מ של ' . (int) $d['vat'] . '%. את מחירי היחידה של דקל מקבלים במנוי: ' . esc_html( $d['contact'] ) . '.</p>';
			}
			$t = '<table><caption>הכלים של דקל לפי שלב בפרויקט (לפי מפת האתר של דקל, 25.10.2026)</caption><thead><tr><th>שלב</th><th>הכלי</th><th>מה עושים בו</th><th>כתובת</th></tr></thead><tbody>';
			foreach ( $d['sw'] as $s ) { $t .= '<tr><td>' . esc_html( $s['stage'] ) . '</td><td>' . esc_html( $s['name'] ) . '</td><td>' . esc_html( $s['what'] ) . '</td><td>' . esc_html( '' !== $s['url'] ? $s['url'] : 'דרך דקל בענן' ) . '</td></tr>'; }
			return '<p>דקל תוכנה היא ' . esc_html( $d['company']['name'] ) . ', החברה בקבוצת דקל (' . esc_html( $d['company']['city'] ) . ') שמפתחת את תוכנות התמחור והניהול של הקבוצה. המוצר המרכזי הוא תוכנת דקל בענן, שבה מכינים כתבי כמויות לפי מחירוני דקל. המחיר נקבע בהצעה לפי היקף.</p>' . $t . '</tbody></table>';
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
			$dir = dirname( __DIR__ ) . '/assets/instruments/data/';
			$rd  = function ( $f ) use ( $dir ) { $p = $dir . $f; $x = is_readable( $p ) ? json_decode( (string) file_get_contents( $p ), true ) : null; return is_array( $x ) ? $x : array(); };
			$n = $rd( 'nrm.json' ); $x = $rd( 'boi-fx.json' ); $t = $rd( 'ptax.json' );
			if ( empty( $n['ltv_by_status'] ) || empty( $t['tracks']['foreign'] ) ) { return ''; }
			$c = $n['ltv_by_status']; $r = array(); foreach ( (array) $n['rates'] as $k ) { $r[ $k['id'] ] = $k['rate']; }
			$pct = function ( $v ) { return rtrim( rtrim( number_format( (float) $v, 2 ), '0' ), '.' ) . '%'; };
			$day = function ( $iso ) { return gmdate( 'j M Y', strtotime( $iso . ' UTC' ) ); };
			$f   = $t['tracks']['foreign'];
			$fx  = ! empty( $x['fx']['USD'] ) ? ' Bank of Israel representative rates on ' . esc_html( $day( $x['fx']['USD']['date'] ) ) . ': 1 USD = ILS ' . esc_html( $x['fx']['USD']['rate'] ) . ', 1 EUR = ILS ' . esc_html( $x['fx']['EUR']['rate'] ) . ', 1 GBP = ILS ' . esc_html( $x['fx']['GBP']['rate'] ) . '.' : '';
			return '<p>Bank of Israel Directive 329 sizes an Israeli mortgage by citizenship: up to ' . $pct( 100 * $c['foreign'] ) . ' of the value for a buyer who is not an Israeli citizen (any home a non-citizen buys is an investment home), '
				. $pct( 100 * $c['cit_first'] ) . ' for an Israeli citizen or registered oleh buying the only home in Israel, ' . $pct( 100 * $c['cit_sell'] ) . ' for a replacement home and ' . $pct( 100 * $c['cit_own'] ) . ' for a citizen who already owns one. '
				. 'The payment may not pass 50% of disposable income, the variable part 66.66% of the loan, the term 30 years. Average rates on new mortgages, ' . esc_html( gmdate( 'F Y', strtotime( $n['rates_month'] . '-01 UTC' ) ) ) . ': fixed not linked ' . $pct( $r['fixed'] )
				. ', fixed CPI-linked ' . $pct( $r['linked'] ) . ', foreign currency loans ' . $pct( $n['fx_track']['rate'] ) . '. Prime ' . $pct( $n['prime'] ) . ' (Bank of Israel rate ' . $pct( $n['boi_rate'] ) . ' since ' . esc_html( $day( $n['boi_rate_from'] ) ) . ', next decision ' . esc_html( $day( $n['next_decision'] ) ) . '). '
				. 'Purchase tax is set by residency: a foreign resident pays ' . $pct( 100 * $f[0][1] ) . ' up to ILS ' . number_format( $f[0][0] ) . ' and ' . $pct( 100 * $f[1][1] ) . ' above, until ' . esc_html( $day( $t['valid']['foreign'] ) ) . '.' . $fx . '</p>';
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
		foreach ( array( 'city', 'hood', 'town', 'rooms', 'track', 'period', 'method', 'preset', 'region', 'kind', 'price', 'view', 'cx' ) as $k ) { if ( isset( $atts[ $k ] ) && '' !== $atts[ $k ] ) { $set[ $k ] = in_array( $k, array( 'rooms', 'price' ), true ) ? (int) $atts[ $k ] : sanitize_text_field( $atts[ $k ] ); } }  // 1.72.498: preset (a ready case of the tool), region, kind, price
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
		// 1.72.513: on an archive get_permalink() and get_post() are the first card's; the page is the archive itself, and its FAQ is printed elsewhere
		$arch = is_post_type_archive() ? get_post_type_archive_link( (string) get_query_var( 'post_type' ) ) : '';
		foreach ( $ids as $id ) {
			$lang = nadlan_nli_tool_lang( $tools[ $id ] ); $t = nadlan_nli_t( $tools[ $id ], $lang );  // HAD-534 (d): name, description and inLanguage follow the page
			$out[] = array( '@type' => 'SoftwareApplication', 'name' => $t['name'], 'description' => $t['desc'], 'applicationCategory' => $t['cat'], 'operatingSystem' => 'Any',
				'inLanguage' => $lang, 'url' => $arch ? $arch : get_permalink(), 'isAccessibleForFree' => true, 'offers' => array( '@type' => 'Offer', 'price' => '0', 'priceCurrency' => 'ILS' ),
				'publisher' => array( '@type' => 'Organization', 'name' => 'nad-lan.co.il', 'url' => home_url( '/' ) ) );
		}
		$p = $arch ? null : get_post(); $faq = $p && 'nadlan_term' !== $p->post_type ? nadlan_nli_faq( $p->post_content ) : array();  // 1.72.521: a glossary term prints its FAQPage in inc/term-faq-schema.php (one FAQPage per page)
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

/* 1.72.533 (G5): the [nadlan_rent_listings] shortcode of /דירות-להשכרה/; loaded only if present, so a rollback that removes it leaves this file working */
if ( file_exists( __DIR__ . '/rent-listings.php' ) ) { require_once __DIR__ . '/rent-listings.php'; }

/* 1.72.575 (HAD-668): the asbestos page tools (asbcheck, asbcost, asbmap, asbwho); loaded only if present, so a rollback that removes it leaves this file working */
if ( file_exists( __DIR__ . '/asbestos-tools.php' ) ) { require_once __DIR__ . '/asbestos-tools.php'; }

/* 1.72.577 (HAD-669): the Tel Aviv garden-apartments tools (gdnworth, gdnmap, gdnstreet, gdnground) and [nadlan_garden_listings]; loaded only if present */
if ( file_exists( __DIR__ . '/garden-tools.php' ) ) { require_once __DIR__ . '/garden-tools.php'; }

/* 1.72.578 (HAD-670): the environmental-hazards map tools (hzmap, hzant, hzcompare, hzcity, hzplan); loaded only if present */
if ( file_exists( __DIR__ . '/hazards-tools.php' ) ) { require_once __DIR__ . '/hazards-tools.php'; }
