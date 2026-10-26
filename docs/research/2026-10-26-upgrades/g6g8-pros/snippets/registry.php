<?php
/* NOT APPLIED. Four entries to paste inside the array of nadlan_nli_tools() in plugins/nadlan-config/inc/instruments.php, after 'pinui'
   (copy the lines between the two markers). Wrapped in a function here only so php -l and snippets/test_registry.php can check them.
   Every related link was 200 on 26.10.2026 and every anchor passed tools/seo/kw_guard.py (kw-guard.txt; the one WARN, "שמאי פינוי בינוי",
   is a qualified mention that points to the glossary). */
function nadlan_g6g8_registry_snippet() {
	return array(
			/* ---- paste from here ---- */
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
			/* ---- paste to here ---- */
	);
}
