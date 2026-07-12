<?php
/**
 * global-worlds.php - international investment worlds (owner order 2026-07-12).
 *
 * "Each location is a world, and real estate is a world that is wrapping it...
 *  the jewel of the crown... 3D model, attach the map, all the tools, the
 *  rental, professionals abroad, SEO first paragraph, schema, and let
 *  developers feed their materials easily like we do in the project."
 *
 * Architecture laws:
 * - SEPARATE CPT nadlan_intl (permalink /global/project/{slug}/) so the
 *   international catalog NEVER pollutes the Israeli surfaces (drone map,
 *   facets, archives, IndexNow) - zero meta_query patches on live queries.
 * - Worlds registry nadlan_gw_worlds() = the location "world" as data:
 *   SEO head, first paragraph, market facts, buying guide, FAQ - HE + EN,
 *   all-or-nothing per language. The registry is the substrate for the
 *   owner's planned per-location writing engine (a glossary-writer-style
 *   cron can append articles per world later).
 * - HONESTY: every market figure is labeled as a public-source estimate
 *   with its date, never advice; seeded projects carry the demo badge
 *   ("based on real market data, not a specific marketed project").
 * - Hierarchy: /global/ hub -> /global/{world}/ -> project singles.
 *   Country routes are whitelisted from the registry (no open regex).
 * - Feeding: normal wp-admin CPT + a labeled metabox (world, district,
 *   coords, price, specs, GLB) - the same "no secret meta keys" law as
 *   the showroom metabox.
 */
if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

if ( ! function_exists( 'nadlan_gw_on' ) ) {
	function nadlan_gw_on() { return get_option( 'nadlan_feature_global', '1' ) === '1'; }
}

/* ============================ the worlds registry ============================ */
if ( ! function_exists( 'nadlan_gw_worlds' ) ) {
	function nadlan_gw_worlds() {
		static $W = null;
		if ( null !== $W ) { return $W; }
		$W = array(

		'dubai' => array(
			'name_he' => 'דובאי', 'name_en' => 'Dubai', 'country_he' => 'איחוד האמירויות', 'country_en' => 'United Arab Emirates',
			'flag' => '🇦🇪', 'currency' => 'AED', 'center' => array( 55.2708, 25.2048 ), 'zoom' => 11,
			'title_he' => 'השקעות נדל"ן בדובאי: מחירים, תשואות, מיסים והמדריך המלא למשקיע הישראלי | נדלן',
			'title_en' => 'Dubai Real Estate Investment: Prices, Yields, Taxes and the Complete Guide | Nadlan',
			'desc_he'  => 'המדריך המלא להשקעה בדירה בדובאי: תשואות שכירות של 6%-9%, אפס מס רכוש שנתי, עלויות רכישה, אזורים מובילים (מרינה, JVC, ביזנס ביי), תהליך הקנייה מרחוק ופרויקטים בתלת ממד.',
			'desc_en'  => 'The complete guide to buying an apartment in Dubai: 6-9% rental yields, zero annual property tax, purchase costs, leading districts (Marina, JVC, Business Bay), the remote buying process and 3D projects.',
			'h1_he' => 'השקעות נדל"ן בדובאי: העולם המלא למשקיע',
			'h1_en' => 'Dubai Real Estate: the Complete Investor World',
			'intro_he' => 'דובאי הפכה בשנים האחרונות ליעד ההשקעה הזר הפופולרי ביותר בקרב משקיעי נדל"ן ישראלים, ולא במקרה: תשואות שכירות ברוטו של 6%-9% בשנה, אפס מס רכוש שנתי ואפס מס על הכנסות שכירות, שוק שקוף המנוהל על ידי רשות הקרקעות של דובאי (DLD), ותהליך רכישה שאפשר להשלים מרחוק בתוך שבועות. טיסה ישירה של שלוש שעות מתל אביב הופכת את הנכס לנגיש כמעט כמו דירה באילת. בעמוד הזה ריכזנו את כל מה שמשקיע ישראלי צריך: נתוני שוק עדכניים, עלויות אמיתיות כולל אגרת ה-DLD, האזורים המובילים, תהליך הקנייה שלב אחר שלב, הסיכונים שחייבים להכיר, ופרויקטים להמחשה שאפשר לחקור בתלת ממד ועל המפה - בדיוק כמו שאנחנו עושים לפרויקטים בישראל.',
			'intro_en' => 'Dubai has become the most popular foreign investment destination for Israeli real estate investors, and not by chance: gross rental yields of 6-9% a year, zero annual property tax and zero tax on rental income, a transparent market run by the Dubai Land Department (DLD), and a purchase process that can be completed remotely within weeks. A direct three-hour flight from Tel Aviv makes the asset almost as accessible as an apartment in Eilat. This page gathers everything an investor needs: current market data, the real costs including the DLD fee, the leading districts, the step-by-step buying process, the risks you must know, and illustrative projects you can explore in 3D and on the map - exactly as we do for projects in Israel.',
			'facts' => array(
				array( 'תשואת שכירות ברוטו', 'Gross rental yield', '6%-9% לשנה (JVC עד 9%, מרינה 5.5%-7%)', '6-9% a year (JVC up to 9%, Marina 5.5-7%)' ),
				array( 'מחיר ממוצע למ"ר', 'Average price per sqm', 'כ-20,000 AED (כ-5,400 דולר)', 'About AED 20,000 (~USD 5,400)' ),
				array( 'מס רכוש שנתי', 'Annual property tax', 'אין', 'None' ),
				array( 'מס על שכירות', 'Tax on rental income', 'אין (נכון ל-2026)', 'None (as of 2026)' ),
				array( 'אגרת רכישה (DLD)', 'Purchase fee (DLD)', '4% + אגרות רישום; סך עלויות עסקה 7%-10%', '4% + registration; total transaction costs 7-10%' ),
				array( 'בעלות לזרים', 'Foreign ownership', 'Freehold מלא באזורים ייעודיים', 'Full freehold in designated zones' ),
				array( 'ויזת זהב', 'Golden visa', 'החל מנכס של 2 מיליון AED', 'From AED 2M property value' ),
				array( 'אזורים מובילים למשקיעים', 'Top investor districts', 'JVC, ביזנס ביי, מרינה, דאונטאון', 'JVC, Business Bay, Marina, Downtown' ),
			),
			'guide' => array(
				array( 'איך קונים דירה בדובאי מישראל, שלב אחר שלב', 'How to buy in Dubai from Israel, step by step',
					array(
						'הרכישה בדובאי פשוטה ממה שנדמה: בוחרים אזור ופרויקט, חותמים על הסכם הזמנה (Reservation) עם פיקדון של 5%-10%, חותמים על הסכם מכר (SPA) הרשום ברשות הקרקעות, ומשלמים לפי אבני דרך של הבנייה. בפרויקטים על הנייר (Off-Plan) נהוגות תוכניות תשלום של 60/40 או 70/30 - חלק גדול מהתשלום רק במסירה. הכסף בפרויקטים מפוקחים יושב בחשבון נאמנות (Escrow) ייעודי לפרויקט לפי חוק, מה שמקטין דרמטית את סיכון היזם.',
						'ישראלים קונים בדובאי באופן חוקי ומקובל מאז הסכמי אברהם. אין דרישת אזרחות או תושבות, הרישום נעשה על שם הקונה בטאבו המקומי (Title Deed דיגיטלי), ואפשר להשלים את כל התהליך מרחוק באמצעות ייפוי כוח. מומלץ ללוות את העסקה בעורך דין מקומי ובסוכן מורשה DLD.',
					),
					array(
						'Buying in Dubai is simpler than it seems: choose a district and project, sign a reservation with a 5-10% deposit, sign the Sale and Purchase Agreement (SPA) registered with the Land Department, and pay by construction milestones. Off-plan projects typically carry 60/40 or 70/30 payment plans - a large share due only at handover. In regulated projects the money sits in a project-dedicated escrow account by law, dramatically reducing developer risk.',
						'Israelis have been buying in Dubai legally and routinely since the Abraham Accords. No citizenship or residency requirement, title is registered in the buyer\'s name (digital Title Deed), and the whole process can be completed remotely via power of attorney. A local lawyer and a DLD-licensed agent are recommended.',
					),
				),
				array( 'העלויות האמיתיות: ממחיר הדירה ועד הצ\'ק האחרון', 'The real costs: from list price to the last payment',
					array(
						'מעבר למחיר הנכס, תקצבו: אגרת העברה של 4% לרשות הקרקעות (DLD), דמי רישום ונאמן של כמה אלפי דירהם, עמלת תיווך של כ-2% (בפרויקטים חדשים משלם היזם לרוב), ודמי חיבור. סך עלויות העסקה נע בדרך כלל בין 7% ל-10% מהמחיר. בהחזקה שוטפת: דמי ניהול (Service Charge) של 12-25 AED למ"ר לשנה לפי רמת הבניין - זה הסעיף שהכי משפיע על התשואה נטו, ולכן חובה לבדוק אותו לפני חתימה.',
					),
					array(
						'Beyond the asset price, budget: the 4% DLD transfer fee, registration and trustee fees of a few thousand dirhams, about 2% agency commission (usually paid by the developer on new projects), and utility connections. Total transaction costs typically run 7-10% of price. Ongoing: service charges of AED 12-25 per sqm per year depending on building grade - the line item that most affects net yield, so check it before signing.',
					),
				),
				array( 'מה עם מיסים בישראל?', 'What about taxes back in Israel?',
					array(
						'דובאי לא גובה מס על השכירות ולא מס רכוש, אבל משקיע תושב ישראל חייב בדיווח ובמס בישראל על הכנסות מחו"ל: מסלול 15% על המחזור (ללא ניכוי הוצאות מלבד פחת) או מס שולי עם ניכוי הוצאות. ברווח הון במכירה - מס רווחי הון ישראלי. אין אמנת מס מלאה בין המדינות, לכן תכנון מס מראש עם רואה חשבון המתמחה בהשקעות חו"ל אינו המלצה - הוא חובה.',
					),
					array(
						'Dubai charges no rental or property tax, but an Israeli tax resident must report and pay Israeli tax on foreign income: the 15% turnover track (no expense deductions except depreciation) or marginal rate with deductions. Capital gains on sale are taxed in Israel. There is no full tax treaty between the countries, so advance planning with an accountant who specializes in foreign investments is not a recommendation - it is a must.',
					),
				),
				array( 'הסיכונים שאסור להתעלם מהם', 'The risks you must not ignore',
					array(
						'שוק דובאי עלה בחדות מאז 2021, והיצע גדול של דירות חדשות צפוי להימסר בשנים 2026-2028 - תרחיש של התמתנות מחירים ושכירויות הוא אפשרות ריאלית שכל משקיע חייב לתמחר. סיכונים נוספים: תנודתיות הדולר/דירהם מול השקל (הדירהם צמוד דולר), תלות ביזם בפרויקטים על הנייר (בדקו רישום Escrow ועבר ביצועי), דמי ניהול שעולים, ונזילות - מכירה מהירה עלולה לגרור הנחה. הנתונים בעמוד הם אומדני שוק להמחשה ואינם ייעוץ השקעות.',
					),
					array(
						'Dubai has risen sharply since 2021, and a large supply of new units is due for handover in 2026-2028 - price and rent moderation is a realistic scenario every investor must price in. Additional risks: USD/AED vs shekel volatility (the dirham is dollar-pegged), developer dependence in off-plan deals (verify escrow registration and delivery track record), rising service charges, and liquidity - a fast sale may require a discount. The figures on this page are market estimates for illustration, not investment advice.',
					),
				),
			),
			'faq' => array(
				array( 'האם ישראלים יכולים לקנות דירה בדובאי?', 'Can Israelis buy property in Dubai?', 'כן. מאז הסכמי אברהם ישראלים קונים בדובאי באופן חוקי ושגרתי, באזורי Freehold המיועדים לזרים, עם רישום מלא על שם הקונה.', 'Yes. Since the Abraham Accords Israelis buy in Dubai legally and routinely, in freehold zones designated for foreigners, with full title in the buyer\'s name.' ),
				array( 'כמה מס משלמים על דירה בדובאי?', 'How much tax on a Dubai apartment?', 'בדובאי: אפס מס רכוש ואפס מס שכירות (2026). בישראל: חובת דיווח ומס על ההכנסה - מסלול 15% על המחזור או מס שולי עם הוצאות.', 'In Dubai: zero property tax and zero rental tax (2026). In Israel: reporting duty and tax on the income - the 15% turnover track or marginal rate with expenses.' ),
				array( 'מה תקציב הכניסה הריאלי?', 'What is a realistic entry budget?', 'דירת חדר (1BR) באזור מבוקש כמו JVC מתחילה סביב 900 אלף עד 1.2 מיליון AED; במרינה ובדאונטאון המחירים גבוהים משמעותית. סך עלויות העסקה: הוסיפו 7%-10%.', 'A 1BR in a sought-after district like JVC starts around AED 900K-1.2M; Marina and Downtown run meaningfully higher. Add 7-10% total transaction costs.' ),
				array( 'האם אפשר לנהל את הדירה מרחוק?', 'Can the apartment be managed remotely?', 'כן, זו הנורמה: חברות ניהול גובות 5%-8% מהשכירות ומטפלות בהשכרה, גבייה ותחזוקה. את המעקב אפשר לנהל בכלי ניהול ההשכרות החינמי שלנו.', 'Yes, it is the norm: management firms charge 5-8% of rent and handle leasing, collection and maintenance. Track it all in our free rental manager.' ),
			),
			'src_he' => 'נתוני שוק: יולי 2026, מקורות פומביים (DLD, Global Property Guide, Property Finder, Khaleej Times). אומדנים להמחשה בלבד - לא ייעוץ השקעות, מס או משפט.',
			'src_en' => 'Market data: July 2026, public sources (DLD, Global Property Guide, Property Finder, Khaleej Times). Estimates for illustration only - not investment, tax or legal advice.',
		),

		'miami' => array(
			'name_he' => 'מיאמי', 'name_en' => 'Miami', 'country_he' => 'ארצות הברית', 'country_en' => 'United States',
			'flag' => '🇺🇸', 'currency' => 'USD', 'center' => array( -80.1918, 25.7743 ), 'zoom' => 11,
			'title_he' => 'השקעות נדל"ן במיאמי: קונדו בבריקל ואדג\'ווטר, מחירים, מיסים והמדריך לישראלים | נדלן',
			'title_en' => 'Miami Real Estate Investment: Brickell and Edgewater Condos, Prices, Taxes and the Guide | Nadlan',
			'desc_he'  => 'המדריך המלא להשקעה בקונדו במיאמי: מחירי פריקונסטרקשן 1,000-1,500 דולר לרגל, אזורי בריקל ואדג\'ווטר, מס רכוש, FIRPTA, תהליך הקנייה לזרים ופרויקטים בתלת ממד ועל המפה.',
			'desc_en'  => 'The complete Miami condo investment guide: preconstruction at USD 1,000-1,500 per sqft, Brickell and Edgewater, property tax, FIRPTA, the foreign buying process and projects in 3D and on the map.',
			'h1_he' => 'השקעות נדל"ן במיאמי: העולם המלא למשקיע',
			'h1_en' => 'Miami Real Estate: the Complete Investor World',
			'intro_he' => 'מיאמי היא שער הכניסה האמריקאי המועדף על משקיעים ישראלים: עיר ללא מס הכנסה מדינתי, עם הגירה חיובית עקבית מניו יורק ומאמריקה הלטינית, קהילה ישראלית ויהודית גדולה, וטיסות ישירות מתל אביב. שוק הקונדו החדש מתרכז בשכונות בריקל (ה"וול סטריט של הדרום") ואדג\'ווטר שעל קו המים, שם פרויקטי פריקונסטרקשן נמכרים ב-1,000 עד 1,500 דולר לרגל רבועה, עם לוחות תשלומים נוחים לאורך הבנייה. בעמוד הזה: נתוני השוק, העלויות המלאות כולל מס רכוש ו-FIRPTA, תהליך הרכישה לקונה זר שלב אחר שלב, הסיכונים, ופרויקטים להמחשה שאפשר לחקור בתלת ממד ועל המפה.',
			'intro_en' => 'Miami is the preferred American gateway for Israeli investors: no state income tax, consistent in-migration from New York and Latin America, a large Israeli and Jewish community, and direct flights from Tel Aviv. The new-condo market concentrates in Brickell ("the Wall Street of the South") and waterfront Edgewater, where preconstruction sells at USD 1,000-1,500 per square foot with construction-linked payment plans. On this page: market data, full costs including property tax and FIRPTA, the foreign buyer process step by step, the risks, and illustrative projects to explore in 3D and on the map.',
			'facts' => array(
				array( 'מחיר פריקונסטרקשן', 'Preconstruction pricing', '1,000-1,500 דולר לרגל רבועה (כ-10,800-16,000 דולר למ"ר)', 'USD 1,000-1,500 per sqft (~10,800-16,000 per sqm)' ),
				array( 'תשואת שכירות ברוטו', 'Gross rental yield', 'כ-5%-6.5% בשכירות ארוכה; גבוה יותר בקצרה (תלוי רישוי)', '~5-6.5% long-term; higher short-term (license dependent)' ),
				array( 'מס רכוש שנתי', 'Annual property tax', 'כ-1.8%-2.2% מהשווי המוערך (מיאמי-דייד)', '~1.8-2.2% of assessed value (Miami-Dade)' ),
				array( 'מס הכנסה מדינתי', 'State income tax', 'אין בפלורידה', 'None in Florida' ),
				array( 'עלויות סגירה', 'Closing costs', '3%-5% (בפרויקט חדש כולל Developer Fee)', '3-5% (new projects include developer fee)' ),
				array( 'FIRPTA במכירה', 'FIRPTA on sale', 'ניכוי במקור 15% לזרים (מתקזז מול המס בפועל)', '15% withholding for foreigners (credited against actual tax)' ),
				array( 'בעלות לזרים', 'Foreign ownership', 'חופשית; רבים קונים דרך LLC', 'Unrestricted; many buy via an LLC' ),
				array( 'שכונות מובילות', 'Leading districts', 'בריקל, אדג\'ווטר, דאונטאון, סאני אייל\'ס', 'Brickell, Edgewater, Downtown, Sunny Isles' ),
			),
			'guide' => array(
				array( 'תהליך הרכישה לקונה זר, שלב אחר שלב', 'The foreign buyer process, step by step',
					array(
						'בפרויקט פריקונסטרקשן חותמים על חוזה עם היזם ומשלמים לאורך הבנייה, בדרך כלל 20% בחתימה ועוד 30%-40% באבני דרך, והיתרה במסירה. הכספים מוחזקים בנאמנות לפי חוק פלורידה. קונה זר לא צריך אזרחות או ויזה; נדרשים דרכון, הוכחת מקור כספים, וחשבון להעברות. ליווי חובה: עורך דין נדל"ן מקומי (Real Estate Attorney) ורואה חשבון אמריקאי לפתיחת ITIN ותכנון המבנה - יחיד מול LLC.',
						'מימון לזרים קיים (Foreign National Loans) בדרך כלל עד 60%-70% מימון בריבית גבוהה מזו של אזרחים; רוב המשקיעים הישראלים בפריקונסטרקשן משלמים הון עצמי לאורך הבנייה ובוחנים מימון רק לקראת המסירה.',
					),
					array(
						'In preconstruction you sign with the developer and pay across construction: typically 20% at contract, another 30-40% at milestones, the balance at closing. Funds are held in escrow under Florida law. A foreign buyer needs no citizenship or visa; you need a passport, source-of-funds proof, and a wiring account. Mandatory team: a local real estate attorney and a US accountant for ITIN and structuring - individual vs LLC.',
						'Foreign national loans exist, usually up to 60-70% LTV at higher rates than citizens pay; most Israeli preconstruction buyers fund equity through construction and consider financing near closing.',
					),
				),
				array( 'העלויות המלאות: לא רק מחיר הדירה', 'The full costs: not just the sticker price',
					array(
						'תקצבו מעבר למחיר: עלויות סגירה של 3%-5% (בפרויקט חדש נהוג Developer Fee של כ-2% במקום חלק מהאגרות), מס רכוש שנתי של כ-2% מהשווי המוערך, דמי ועד בית (HOA) שבמגדלי יוקרה חדשים נעים בין 0.9 ל-1.5 דולר לרגל לחודש - סעיף מהותי לתשואה נטו, וביטוח. בהשכרה: דמי ניהול של 8%-10% לשכירות ארוכה. את כל המעקב השוטף אפשר לנהל בכלי ניהול ההשכרות שלנו.',
					),
					array(
						'Budget beyond price: closing costs of 3-5% (new projects often a ~2% developer fee replacing some charges), annual property tax around 2% of assessed value, HOA dues that in new luxury towers run USD 0.9-1.5 per sqft per month - a material net-yield item, and insurance. When renting: 8-10% management for long-term leases. Track it all in our rental manager.',
					),
				),
				array( 'מיסוי אמריקאי וישראלי: התמונה המלאה', 'US and Israeli tax: the full picture',
					array(
						'ארה"ב ממסה הכנסות שכירות של זרים (מדרגות רגילות על נטו אחרי הוצאות ופחת, בבחירת Net Election), ובמכירה חל FIRPTA - ניכוי במקור של 15% מהתמורה שמתקזז מול המס האמיתי. בישראל חלה חובת דיווח, ואמנת המס ישראל-ארה"ב מונעת כפל מס באמצעות זיכויים. מבנה ההחזקה (יחיד, LLC, שותפות) משפיע גם על מס עיזבון אמריקאי לזרים - נושא שחייבים לתכנן מראש עם מומחה.',
					),
					array(
						'The US taxes foreign rental income (regular brackets on net after expenses and depreciation, via the Net Election), and FIRPTA applies on sale - 15% withholding credited against actual tax. Israel requires reporting, and the US-Israel tax treaty prevents double taxation through credits. The holding structure (individual, LLC, partnership) also affects US estate tax for foreigners - plan it in advance with a specialist.',
					),
				),
				array( 'הסיכונים שאסור להתעלם מהם', 'The risks you must not ignore',
					array(
						'ביטוחים ועלויות ועד בית זינקו בפלורידה אחרי אסונות אקלים וחוקי בטיחות מבנים חדשים (אחרי סרפסייד) - בדקו את מצב קרן הרזרבה ודוח ה-Milestone Inspection של בניינים ותיקים, ובפרויקט חדש את איתנות היזם. סיכונים נוספים: היצע קונדו גבוה בדאונטאון, תלות בביקוש זר, שער דולר/שקל, ורגולציית שכירות קצרה שמשתנה בין עיריות. הנתונים בעמוד הם אומדני שוק להמחשה ואינם ייעוץ.',
					),
					array(
						'Insurance and HOA costs jumped in Florida after climate events and post-Surfside building-safety laws - check reserve funding and milestone inspection reports on older buildings, and developer strength on new ones. Additional risks: high downtown condo supply, dependence on foreign demand, USD/ILS swings, and short-term rental rules that vary by municipality. Figures on this page are market estimates for illustration, not advice.',
					),
				),
			),
			'faq' => array(
				array( 'האם ישראלי יכול לקנות דירה במיאמי בלי אזרחות?', 'Can an Israeli buy in Miami without citizenship?', 'כן. אין שום מגבלת אזרחות על בעלות נדל"ן בפלורידה. נדרשים דרכון, הוכחת מקור כספים ומבנה החזקה נכון (יחיד או LLC) שקובעים עם עורך דין ורואה חשבון.', 'Yes. Florida has no citizenship restriction on ownership. You need a passport, source-of-funds proof and the right structure (individual or LLC) set with an attorney and accountant.' ),
				array( 'מה ההבדל בין בריקל לאדג\'ווטר?', 'Brickell vs Edgewater?', 'בריקל היא מרכז עסקים צפוף ותוסס עם שכירות חזקה כל השנה; אדג\'ווטר שקטה יותר, על קו המים מול מפרץ ביסקיין, עם פרויקטים חדשים במחירי כניסה נמוכים במעט ופוטנציאל התחדשות.', 'Brickell is the dense, vibrant business core with strong year-round rental demand; Edgewater is calmer, on Biscayne Bay, with new projects at slightly lower entry prices and regeneration upside.' ),
				array( 'כמה מס רכוש משלמים בפועל?', 'How much property tax in practice?', 'במיאמי-דייד המס האפקטיבי הוא כ-2% מהשווי המוערך בשנה. על קונדו של מיליון דולר: סדר גודל של 20 אלף דולר בשנה - חובה לכלול בתחשיב התשואה.', 'Miami-Dade effective tax is about 2% of assessed value a year. On a USD 1M condo: roughly USD 20K a year - must be in your yield math.' ),
				array( 'האם שכירות קצרה (Airbnb) מותרת?', 'Is short-term rental (Airbnb) allowed?', 'תלוי בעירייה, באזור ובבניין: חלק מהמגדלים החדשים נבנים ייעודית לשכירות קצרה ואחרים אוסרים אותה בתקנון. בדקו את הרישוי לפני שקונים על בסיס תחזית Airbnb.', 'Depends on city, zone and building: some new towers are purpose-built for short-term rental, others prohibit it. Verify licensing before buying on an Airbnb forecast.' ),
			),
			'src_he' => 'נתוני שוק: יולי 2026, מקורות פומביים (Miami Association of Realtors, CondoBlackBook, נתוני פרויקטים מפורסמים). אומדנים להמחשה בלבד - לא ייעוץ השקעות, מס או משפט.',
			'src_en' => 'Market data: July 2026, public sources (Miami Association of Realtors, CondoBlackBook, published project data). Estimates for illustration only - not investment, tax or legal advice.',
		),

		'new-york' => array(
			'name_he' => 'ניו יורק', 'name_en' => 'New York', 'country_he' => 'ארצות הברית', 'country_en' => 'United States',
			'flag' => '🇺🇸', 'currency' => 'USD', 'center' => array( -73.9857, 40.7484 ), 'zoom' => 11,
			'title_he' => 'השקעות נדל"ן בניו יורק: קונדו במנהטן, ברוקלין ו-LIC, מיסים והמדריך לישראלים | נדלן',
			'title_en' => 'New York Real Estate Investment: Manhattan, Brooklyn and LIC Condos, Taxes and the Guide | Nadlan',
			'desc_he'  => 'המדריך המלא להשקעה בקונדו בניו יורק: מחירים בלונג איילנד סיטי, ברוקלין ומנהטן, מס רכישה (Mansion Tax), עלויות סגירה, תהליך הקנייה לזרים ופרויקטים בתלת ממד ועל המפה.',
			'desc_en'  => 'The complete New York condo guide: prices in Long Island City, Brooklyn and Manhattan, the mansion tax, closing costs, the foreign buying process and projects in 3D and on the map.',
			'h1_he' => 'השקעות נדל"ן בניו יורק: העולם המלא למשקיע',
			'h1_en' => 'New York Real Estate: the Complete Investor World',
			'intro_he' => 'ניו יורק היא ההשקעה הדפנסיבית של עולם הנדל"ן: שוק עמוק ונזיל שקולט הון גלובלי כבר מאה שנה, ביקוש שכירות כמעט בלתי נגמר, ושקיפות משפטית מהגבוהות בעולם. משקיעים ישראלים מתרכזים היום פחות במנהטן היקרה ויותר בלונג איילנד סיטי (LIC) שבקווינס - תחנת רכבת אחת ממידטאון - ובדאונטאון ברוקלין, שם קונדו חדש נמכר ב-1,100 עד 1,600 דולר לרגל, מול 2,000 ומעלה במנהטן. התשואה השוטפת נמוכה מדובאי או מיאמי (3%-4.5% ברוטו), אבל היציבות, הנזילות ופוטנציאל עליית הערך הם הסיבה שקונים כאן. בעמוד: הנתונים, מס ה-Mansion, עלויות הסגירה האמיתיות, התהליך לזר, הסיכונים, ופרויקטים להמחשה בתלת ממד ועל המפה.',
			'intro_en' => 'New York is real estate\'s defensive play: a deep, liquid market that has absorbed global capital for a century, near-endless rental demand, and world-leading legal transparency. Israeli investors now focus less on pricey Manhattan and more on Long Island City (LIC) in Queens - one subway stop from Midtown - and Downtown Brooklyn, where new condos sell at USD 1,100-1,600 per sqft versus 2,000+ in Manhattan. Running yields are lower than Dubai or Miami (3-4.5% gross), but stability, liquidity and appreciation are why capital buys here. On this page: the data, the mansion tax, real closing costs, the foreign buyer process, the risks, and illustrative projects in 3D and on the map.',
			'facts' => array(
				array( 'מחיר קונדו חדש', 'New condo pricing', 'LIC וברוקלין: 1,100-1,600 דולר לרגל; מנהטן: 2,000+', 'LIC and Brooklyn: USD 1,100-1,600 per sqft; Manhattan: 2,000+' ),
				array( 'תשואת שכירות ברוטו', 'Gross rental yield', 'כ-3%-4.5%; הסיפור הוא יציבות ועליית ערך', '~3-4.5%; the story is stability and appreciation' ),
				array( 'מס רכישה (Mansion Tax)', 'Mansion tax', '1% מעל מיליון דולר, מדורג עד 3.9% מעל 25 מיליון', '1% above USD 1M, tiered to 3.9% above 25M' ),
				array( 'עלויות סגירה לקונה', 'Buyer closing costs', 'כ-2%-5% (בפרויקט חדש הקונה נושא גם במסי ההעברה)', '~2-5% (new development buyers often absorb transfer taxes)' ),
				array( 'מס רכוש שנתי', 'Annual property tax', 'משתנה; בקונדו חדש לעיתים הקלת 421a/485x - בדקו לכל בניין', 'Varies; new condos sometimes carry 421a/485x abatements - check per building' ),
				array( 'FIRPTA במכירה', 'FIRPTA on sale', 'ניכוי במקור 15% לזרים (מתקזז מול המס בפועל)', '15% withholding for foreigners (credited against actual tax)' ),
				array( 'בעלות לזרים', 'Foreign ownership', 'חופשית בקונדו (לא בקואופ); רבים קונים דרך LLC', 'Unrestricted in condos (not co-ops); many buy via an LLC' ),
				array( 'שכונות מובילות למשקיעים', 'Leading investor districts', 'לונג איילנד סיטי, דאונטאון ברוקלין, ויליאמסבורג, פייננשל דיסטריקט', 'Long Island City, Downtown Brooklyn, Williamsburg, Financial District' ),
			),
			'guide' => array(
				array( 'קונדו, לא קואופ: מה קונים ואיך', 'Condo, not co-op: what to buy and how',
					array(
						'בניו יורק שני סוגי בעלות: קואופרטיב (Co-op), שבו ועד הבניין רשאי לפסול קונים ואוסר לרוב השכרה - לא מתאים למשקיע זר, וקונדומיניום (Condo) עם בעלות מלאה וחופש השכרה - זה מה שמשקיעים קונים. בפרויקט חדש חותמים על חוזה עם 10%-20% מקדמה המוחזקת בנאמנות, והיתרה בסגירה. אין מגבלת אזרחות; נדרשים דרכון, הוכחת הון ועורך דין נדל"ן ניו יורקי (חובה מעשית בכל עסקה בעיר).',
					),
					array(
						'New York has two ownership types: co-ops, where the board can reject buyers and usually bans renting - unsuitable for a foreign investor, and condominiums with full ownership and rental freedom - what investors buy. In new developments you sign with a 10-20% escrowed deposit, balance at closing. No citizenship restriction; you need a passport, proof of funds and a New York real estate attorney (a practical requirement in every NYC deal).',
					),
				),
				array( 'העלויות: Mansion Tax, סגירה והחזקה', 'The costs: mansion tax, closing and carry',
					array(
						'קונה משלם את מס ה-Mansion: 1% מהמחיר מעל מיליון דולר, במדרגות שמטפסות עד 3.9% מעל 25 מיליון. בפרויקט חדש נהוג שהקונה סופג גם את מסי ההעברה של המוכר (כ-1.8%-2.1%) - נקודת משא ומתן. הוסיפו שכר טרחה, טייטל וביטוח: סך הכל 2%-5%. בהחזקה: מס רכוש (בדקו אם לבניין הקלת מס פעילה וכמה שנים נותרו לה) ודמי Common Charges - בקונדו חדש 1-1.8 דולר לרגל לחודש.',
					),
					array(
						'Buyers pay the mansion tax: 1% of price above USD 1M, tiered up to 3.9% above 25M. In new developments buyers customarily absorb the seller\'s transfer taxes too (~1.8-2.1%) - a negotiation point. Add legal, title and insurance: 2-5% total. Carrying: property tax (check whether the building has an active abatement and how many years remain) and common charges - USD 1-1.8 per sqft per month in new condos.',
					),
				),
				array( 'מיסוי: אמנת המס עובדת לטובתכם', 'Tax: the treaty works in your favor',
					array(
						'הכנסות שכירות ממוסות בארה"ב במדרגות רגילות על הנטו (אחרי הוצאות, ריבית ופחת - שלרוב מאפסים את המס בשנים הראשונות), ובמכירה חלים מס רווחי הון פדרלי ומדינתי ו-FIRPTA כניכוי במקור. אמנת המס ישראל-ארה"ב מזכה את המס ששולם, כך שלא משלמים פעמיים. לזרים יש חשיפת מס עיזבון אמריקאי מעל פטור נמוך - זו הסיבה המרכזית שהחזקות גדולות מובנות דרך ישויות. תכנון מראש חובה.',
					),
					array(
						'Rental income is taxed in the US at regular brackets on net (after expenses, interest and depreciation - which often zero out early-year tax), and sales trigger federal and state capital gains with FIRPTA withholding. The US-Israel treaty credits tax paid, so you never pay twice. Foreigners face US estate-tax exposure above a low exemption - the main reason larger holdings are structured through entities. Advance planning is mandatory.',
					),
				),
				array( 'הסיכונים שאסור להתעלם מהם', 'The risks you must not ignore',
					array(
						'התשואה השוטפת נמוכה, ולכן עסקה ממונפת בריבית גבוהה עלולה להיות תזרימית שלילית - ניו יורק היא השקעת הון, לא תחליף פנסיה. סיכונים נוספים: מסי רכוש שעולים כשהקלות פגות, רגולציית שכירות (בעיקר בבניינים ישנים מפוקחים - עוד סיבה לקונדו חדש), עלויות תפעול גבוהות, ושער הדולר. הנתונים בעמוד הם אומדני שוק להמחשה ואינם ייעוץ.',
					),
					array(
						'Running yield is low, so a leveraged deal at high rates can be cash-flow negative - New York is a capital play, not a pension substitute. Additional risks: property taxes stepping up when abatements expire, rent regulation (mostly in older stabilized buildings - another reason for new condos), high operating costs, and the dollar rate. Figures on this page are market estimates for illustration, not advice.',
					),
				),
			),
			'faq' => array(
				array( 'למה לונג איילנד סיטי ולא מנהטן?', 'Why Long Island City over Manhattan?', 'אותו שוק שוכרים (עובדי מידטאון), תחנת רכבת אחת מגרנד סנטרל, אבל מחיר כניסה נמוך בכ-30%-40% ובניינים חדשים עם הקלות מס - התשואה פשוט טובה יותר.', 'The same tenant pool (Midtown workers), one subway stop from Grand Central, but 30-40% lower entry pricing and new buildings with tax abatements - the yield math is simply better.' ),
				array( 'האם זר יכול לקבל משכנתא בניו יורק?', 'Can a foreigner get a New York mortgage?', 'כן, במסלולי Foreign National: בדרך כלל עד 60%-70% מימון, בריבית גבוהה מזו של אזרחים ועם דרישות הון ונזילות גבוהות. חלק ניכר מהמשקיעים הזרים קונים במזומן ומממנים אחרי הסגירה.', 'Yes, via foreign national programs: typically up to 60-70% LTV at higher rates with strong reserve requirements. Many foreign investors buy cash and finance after closing.' ),
				array( 'מה זה בעצם ה-Mansion Tax?', 'What exactly is the mansion tax?', 'מס רכישה חד פעמי של מדינת ניו יורק על העסקה: 1% מהמחיר כשהוא עולה על מיליון דולר, במדרגות שמגיעות עד 3.9% מעל 25 מיליון. משולם על ידי הקונה בסגירה.', 'A one-time New York State purchase tax: 1% of price when it exceeds USD 1M, tiered to 3.9% above 25M. Paid by the buyer at closing.' ),
				array( 'קואופ זול יותר - למה לא לקנות קואופ?', 'Co-ops are cheaper - why not buy one?', 'כי ועד קואופ רשאי לפסול קונה בלי נימוק, דורש ראיונות ומסמכים אישיים, ולרוב אוסר השכרה - שלושה פסולים מוחלטים למשקיע זר. קונדו בלבד.', 'Because a co-op board can reject a buyer without cause, demands interviews and personal financials, and usually bans renting - three absolute disqualifiers for a foreign investor. Condos only.' ),
			),
			'src_he' => 'נתוני שוק: יולי 2026, מקורות פומביים (NYC Department of Finance, StreetEasy, נתוני פרויקטים מפורסמים). אומדנים להמחשה בלבד - לא ייעוץ השקעות, מס או משפט.',
			'src_en' => 'Market data: July 2026, public sources (NYC Department of Finance, StreetEasy, published project data). Estimates for illustration only - not investment, tax or legal advice.',
		),

		'london' => array(
			'name_he' => 'לונדון', 'name_en' => 'London', 'country_he' => 'בריטניה', 'country_en' => 'United Kingdom',
			'flag' => '🇬🇧', 'currency' => 'GBP', 'center' => array( -0.1276, 51.5074 ), 'zoom' => 11,
			'title_he' => 'השקעות נדל"ן בלונדון: מחירים, SDLT, אזורים והמדריך המלא למשקיע הישראלי | נדלן',
			'title_en' => 'London Property Investment: Prices, SDLT, Districts and the Complete Guide | Nadlan',
			'desc_he'  => 'המדריך המלא להשקעה בדירה בלונדון: מחירים באזורי Zone 2-3, מס הרכישה SDLT לתושבי חוץ, ליסהולד מול פריהולד, תהליך הרכישה ופרויקטים להמחשה בתלת ממד ועל המפה.',
			'desc_en'  => 'The complete London investment guide: Zone 2-3 pricing, SDLT for non-residents, leasehold vs freehold, the buying process and illustrative projects in 3D and on the map.',
			'h1_he' => 'השקעות נדל"ן בלונדון: העולם המלא למשקיע',
			'h1_en' => 'London Property: the Complete Investor World',
			'intro_he' => 'לונדון היא שוק הנדל"ן הבינלאומי הוותיק בעולם: מטבע חזק, מערכת משפט שמכבדת חוזים כבר מאות שנים, אוניברסיטאות שמושכות שוכרים מכל העולם, והיצע שתמיד מפגר אחרי הביקוש. משקיעים ישראלים מתרכזים היום פחות במרכז היוקרתי שהתייקר מדי, ויותר באזורי Zone 2-3 המתחדשים - קנרי וורף, סטרטפורד, באטרסי - שם דירה חדשה בפרויקט מתחילה סביב 550-800 אלף ליש"ט עם תשואות של 4%-5.5%. חשוב להכיר: מס הרכישה SDLT לתושב חוץ שקונה דירה נוספת מגיע למדרגות גבוהות, ורוב הדירות בבניינים נמכרות בליסהולד ולא בבעלות מלאה. בעמוד הזה: הנתונים, המיסים משני הצדדים, ליסהולד מול פריהולד, התהליך המלא, הסיכונים, ופרויקטים להמחשה בתלת ממד ועל המפה.',
			'intro_en' => 'London is the oldest international property market in the world: a strong currency, a legal system that has honored contracts for centuries, universities that pull tenants from everywhere, and supply that forever lags demand. Israeli investors now focus less on overpriced Prime Central and more on regenerating Zone 2-3 districts - Canary Wharf, Stratford, Battersea - where a new-build apartment starts around GBP 550-800K with 4-5.5% yields. Know this going in: non-resident SDLT on an additional dwelling reaches steep brackets, and most flats sell leasehold, not freehold. On this page: the data, taxes on both sides, leasehold vs freehold, the full process, the risks, and illustrative projects in 3D and on the map.',
			'facts' => array(
				array( 'מחיר דירה חדשה Zone 2-3', 'New-build price Zone 2-3', '550-800 אלף ליש"ט לדירת 1-2 חדרי שינה', 'GBP 550-800K for a 1-2 bed' ),
				array( 'תשואת שכירות ברוטו', 'Gross rental yield', 'כ-4%-5.5% באזורים המתחדשים', '~4-5.5% in regeneration zones' ),
				array( 'מס רכישה (SDLT) לתושב חוץ', 'SDLT for non-residents', 'מדרגות + 2% תוספת תושב חוץ + 5% דירה נוספת', 'Brackets + 2% non-resident + 5% additional dwelling' ),
				array( 'סוג הבעלות', 'Tenure', 'רוב הדירות ליסהולד (99-999 שנה); בדקו יתרה ודמי קרקע', 'Most flats leasehold (99-999 yrs); check term and ground rent' ),
				array( 'מס שנתי', 'Annual tax', 'Council Tax (משלם לרוב השוכר) + מס הכנסה על שכירות', 'Council tax (usually the tenant) + income tax on rent' ),
				array( 'ויזת זהב', 'Golden visa', 'אין (בוטלה ב-2022)', 'None (closed in 2022)' ),
				array( 'בעלות לזרים', 'Foreign ownership', 'חופשית; חברות זרות חייבות רישום שקיפות', 'Unrestricted; overseas entities need transparency registration' ),
				array( 'אזורים מובילים למשקיעים', 'Top investor districts', 'קנרי וורף, סטרטפורד, באטרסי, גריניץ', 'Canary Wharf, Stratford, Battersea, Greenwich' ),
			),
			'guide' => array(
				array( 'ליסהולד, פריהולד ומה שביניהם', 'Leasehold, freehold and what lies between',
					array(
						'רוב הדירות בבנייני מגורים בלונדון נמכרות בליסהולד: בעלות על הדירה לתקופה ארוכה (לרוב 125-999 שנה) בעוד הקרקע נשארת של בעל הפריהולד. שלושה דברים לבדוק לפני חתימה: יתרת שנות החכירה (מתחת ל-80 שנה הערך נפגע והארכה מתייקרת), דמי Ground Rent (רפורמות אחרונות איפסו אותם בחוזים חדשים), ודמי Service Charge שבמגדלים חדשים יכולים להגיע ל-4-7 ליש"ט לרגל לשנה. עסקה מלווה תמיד ב-Solicitor מקומי - תפקיד חובה בשיטה האנגלית.',
					),
					array(
						'Most London flats sell leasehold: you own the apartment for a long term (typically 125-999 years) while the land stays with the freeholder. Check three things before signing: remaining lease years (below 80 the value suffers and extension gets expensive), ground rent (recent reforms zeroed it in new contracts), and service charges that in new towers can reach GBP 4-7 per sqft a year. Every deal runs through a local solicitor - a mandatory role in the English system.',
					),
				),
				array( 'SDLT: המס שמפתיע משקיעים', 'SDLT: the tax that surprises investors',
					array(
						'מס הרכישה הבריטי (SDLT) הוא ההוצאה הגדולה של משקיע זר: מדרגות רגילות לפי מחיר, ומעליהן תוספת של 2% לתושב חוץ ותוספת דירה נוספת של 5%. על דירת 700 אלף ליש"ט, משקיע זר שזו לא דירתו היחידה ישלם עשרות אלפי ליש"ט - חובה להריץ את החישוב המדויק לפני הצעה. בהכנסות שכירות: מס הכנסה בריטי, ובמכירה מס רווחי הון לתושבי חוץ. אמנת המס ישראל-בריטניה מזכה את המס ששולם.',
					),
					array(
						'UK stamp duty (SDLT) is the foreign investor\'s biggest line item: standard brackets by price, plus a 2% non-resident surcharge and a 5% additional-dwelling surcharge. On a GBP 700K flat, a foreign investor with another home pays tens of thousands - run the exact calculation before offering. On rent: UK income tax; on sale, non-resident capital gains tax. The Israel-UK treaty credits tax paid.',
					),
				),
				array( 'הסיכונים שאסור להתעלם מהם', 'The risks you must not ignore',
					array(
						'התשואה השוטפת צנועה ומבנה העלויות (SDLT, דמי ניהול, ניהול השכרה) שוחק אותה - לונדון היא השקעת מטבע ויציבות, לא תזרים. עוד לבדוק: חשיפת ליש"ט/שקל, רגולציית שכירות מתהדקת, עלויות תיקון חיפויים בבניינים ישנים - קנו רק בניין עם אישור EWS1 תקין או חדש לגמרי, ושוק המכירה החוזרת של ליסהולד קצר. הנתונים בעמוד הם אומדני שוק להמחשה ואינם ייעוץ.',
					),
					array(
						'Running yield is modest and the cost stack (SDLT, service charges, management) erodes it - London is a currency-and-stability play, not cash flow. Also check: GBP/ILS exposure, tightening rental regulation, cladding remediation in older towers - buy only buildings with a clean EWS1 or brand new, and the resale market for short leaseholds. Figures on this page are market estimates for illustration, not advice.',
					),
				),
			),
			'faq' => array(
				array( 'האם כדאי לקנות דירה בלונדון בליסהולד?', 'Is a leasehold flat worth buying?', 'כן, זו הנורמה בלונדון - בתנאי שיתרת החכירה ארוכה (מעל 125 שנה בחוזה חדש), דמי הקרקע אפס או סמליים, ודמי הניהול סבירים ומגובים בתוכנית תחזוקה.', 'Yes, it is the London norm - provided the remaining term is long (125+ years on new contracts), ground rent is zero or peppercorn, and the service charge is reasonable and backed by a maintenance plan.' ),
				array( 'כמה SDLT ישלם משקיע ישראלי?', 'How much SDLT will an Israeli investor pay?', 'תלוי במחיר ובנסיבות: המדרגות הרגילות ועליהן 2% תושב חוץ ו-5% דירה נוספת. על 700 אלף ליש"ט זה בדרך כלל סדר גודל של 60-75 אלף ליש"ט - הריצו חישוב מדויק לפני כל הצעה.', 'Depends on price and circumstances: standard brackets plus 2% non-resident and 5% additional dwelling. On GBP 700K it typically lands around GBP 60-75K - run the exact number before any offer.' ),
				array( 'איפה משקיעים ישראלים קונים בלונדון?', 'Where do Israeli investors buy in London?', 'בעיקר באזורי ההתחדשות של Zone 2-3: קנרי וורף וסטרטפורד במזרח, באטרסי וניין אלמס בדרום - פרויקטים חדשים ליד תחבורה, במחירי כניסה נמוכים מהמרכז בשליש ויותר.', 'Mostly in Zone 2-3 regeneration districts: Canary Wharf and Stratford in the east, Battersea and Nine Elms in the south - new schemes near transport at a third or more below central pricing.' ),
			),
			'src_he' => 'נתוני שוק: יולי 2026, מקורות פומביים (HM Land Registry, Rightmove, gov.uk). אומדנים להמחשה בלבד - לא ייעוץ השקעות, מס או משפט.',
			'src_en' => 'Market data: July 2026, public sources (HM Land Registry, Rightmove, gov.uk). Estimates for illustration only - not investment, tax or legal advice.',
		),

		'greece' => array(
			'name_he' => 'יוון', 'name_en' => 'Greece', 'country_he' => 'יוון', 'country_en' => 'Greece',
			'flag' => '🇬🇷', 'currency' => 'EUR', 'center' => array( 23.7275, 37.9838 ), 'zoom' => 11,
			'title_he' => 'השקעות נדל"ן ביוון: אתונה, ויזת זהב, מחירים והמדריך המלא למשקיע הישראלי | נדלן',
			'title_en' => 'Greece Property Investment: Athens, the Golden Visa, Prices and the Complete Guide | Nadlan',
			'desc_he'  => 'המדריך המלא להשקעה בדירה ביוון: מחירי אתונה, ויזת הזהב האירופית, מס רכישה 3.09%, תשואות שכירות, תהליך הרכישה ופרויקטים להמחשה בתלת ממד ועל המפה.',
			'desc_en'  => 'The complete Greece investment guide: Athens prices, the EU golden visa, the 3.09% transfer tax, rental yields, the buying process and illustrative projects in 3D and on the map.',
			'h1_he' => 'השקעות נדל"ן ביוון: העולם המלא למשקיע',
			'h1_en' => 'Greece Property: the Complete Investor World',
			'intro_he' => 'יוון היא ההשקעה האירופית הקרובה: שעתיים טיסה מתל אביב, מחירים שעדיין נמוכים משמעותית ממערב אירופה למרות עליות חדות מאז 2018, תיירות ששוברת שיאים שנה אחרי שנה, וויזת הזהב - תושבות אירופית למשפחה כולה דרך רכישת נכס. הכתובת המרכזית היא אתונה: שכונות כמו קוקאקי, פנגראטי וגליפדה שעל החוף מציעות דירות משופצות ופרויקטים חדשים ב-2,500-4,500 אירו למ"ר, עם תשואות של 4%-6%. חשוב להכיר את מדרגות ויזת הזהב החדשות ואת מגבלות השכירות הקצרה שנכנסו לתוקף. בעמוד הזה: הנתונים, הוויזה, המיסים משני הצדדים, תהליך הרכישה עם עורך דין ונוטריון, הסיכונים, ופרויקטים להמחשה בתלת ממד ועל המפה.',
			'intro_en' => 'Greece is the near-Europe investment: a two-hour flight from Tel Aviv, prices still well below Western Europe despite sharp rises since 2018, record-breaking tourism year after year, and the golden visa - EU residency for the whole family through a property purchase. The main address is Athens: neighborhoods like Koukaki, Pangrati and coastal Glyfada offer renovated flats and new projects at EUR 2,500-4,500 per sqm with 4-6% yields. Know the new golden-visa thresholds and the short-term rental limits now in force. On this page: the data, the visa, taxes on both sides, the lawyer-and-notary purchase process, the risks, and illustrative projects in 3D and on the map.',
			'facts' => array(
				array( 'מחיר למ"ר באתונה', 'Athens price per sqm', '2,500-4,500 אירו (מרכז ופרברי חוף מבוקשים)', 'EUR 2,500-4,500 (center and prime coastal suburbs)' ),
				array( 'תשואת שכירות ברוטו', 'Gross rental yield', 'כ-4%-6%; שכירות קצרה גבוהה יותר אך מוגבלת רגולטורית', '~4-6%; short-term higher but regulation-capped' ),
				array( 'ויזת זהב', 'Golden visa', '800 אלף אירו באתונה/סלוניקי/איים מבוקשים; 400 אלף בשאר המדינה', 'EUR 800K in Athens/Thessaloniki/prime islands; 400K elsewhere' ),
				array( 'מס רכישה', 'Transfer tax', '3.09% (או מע"מ 24% בנכס חדש מהיזם - בדקו פטורים)', '3.09% (or 24% VAT on new-from-developer - check exemptions)' ),
				array( 'מס רכוש שנתי (ENFIA)', 'Annual property tax (ENFIA)', 'כמה מאות עד אלפי אירו, לפי הנכס', 'A few hundred to a few thousand EUR by asset' ),
				array( 'מס על שכירות', 'Tax on rent', 'מדורג: 15% עד 12 אלף אירו, ואז 35%/45%', 'Tiered: 15% to EUR 12K, then 35%/45%' ),
				array( 'בעלות לזרים', 'Foreign ownership', 'חופשית (הגבלות רק באזורי גבול)', 'Unrestricted (limits only in border zones)' ),
				array( 'אזורים מובילים', 'Top districts', 'אתונה: קוקאקי, פנגראטי, גליפדה; סלוניקי; האיים', 'Athens: Koukaki, Pangrati, Glyfada; Thessaloniki; the islands' ),
			),
			'guide' => array(
				array( 'תהליך הרכישה: עורך דין, נוטריון ומספר מס', 'The process: lawyer, notary and a tax number',
					array(
						'רכישה ביוון מתנהלת דרך שלושה גורמים: עורך דין מטעמכם שבודק את נסח הרישום ואת היעדר החובות (ביוון חובות ארנונה ומס נדבקים לנכס!), נוטריון שמאשר את חוזה המכר, ורואה חשבון שפותח לכם מספר מס יווני (AFM) - תנאי לכל עסקה. התהליך אורך בדרך כלל 6-10 שבועות ואפשר להשלימו בייפוי כוח מרחוק. בקניית נכס לוויזת זהב חשוב שהתשלום יעבור בערוץ בנקאי מתועד במלואו - זו דרישת הבקשה.',
					),
					array(
						'A Greek purchase runs through three roles: your lawyer, who checks title and the absence of debts (in Greece municipal and tax debts attach to the property!), the notary who certifies the deed, and an accountant who opens your Greek tax number (AFM) - a precondition for any deal. It typically takes 6-10 weeks and can be completed remotely by power of attorney. For a golden-visa purchase the payment must flow through fully documented banking channels - an application requirement.',
					),
				),
				array( 'ויזת הזהב: מה באמת מקבלים', 'The golden visa: what you actually get',
					array(
						'ויזת הזהב היוונית מעניקה תושבות מתחדשת לכל המשפחה (בני זוג, ילדים עד 21, הורים) עם חופש תנועה בשנגן - בלי דרישת מגורים בפועל. המדרגות כיום: 800 אלף אירו באזורי הביקוש (אתונה, סלוניקי, מיקונוס, סנטוריני ואיים גדולים) ו-400 אלף בשאר המדינה, עם מסלול חריג של 250 אלף בנכסים ייעודיים להשבחה או הסבה. חשוב: הוויזה אינה אזרחות ואינה מקנה זכות עבודה כשכיר ביוון; התאזרחות דורשת מגורים אמיתיים ושפה.',
					),
					array(
						'The Greek golden visa grants renewable residency to the whole family (spouse, children to 21, parents) with Schengen freedom of movement - and no actual stay requirement. Current thresholds: EUR 800K in demand zones (Athens, Thessaloniki, Mykonos, Santorini and major islands), 400K elsewhere, with a special 250K track for designated renovation or conversion assets. Important: the visa is not citizenship and does not allow salaried work in Greece; naturalization requires real residence and language.',
					),
				),
				array( 'הסיכונים שאסור להתעלם מהם', 'The risks you must not ignore',
					array(
						'השוק היווני עלה בחדות ומחירי מרכז אתונה כבר אינם מציאה; אל תקנו לפי מחירי 2018. בדקו: מגבלות שכירות קצרה חדשות במרכז אתונה, איכות בנייה בבניינים ישנים (רעידות אדמה - העדיפו בנייה מ-1985 ואילך או שיפוץ הנדסי מתועד), חובות שנדבקים לנכס, וביורוקרטיה איטית ברישום. מס ישראלי חל על ההכנסה לפי המסלולים הרגילים, עם זיכוי לפי אמנת המס. הנתונים להמחשה בלבד.',
					),
					array(
						'The Greek market rose sharply and central Athens is no longer a bargain; do not underwrite at 2018 prices. Check: new short-term rental limits in central Athens, build quality in older stock (earthquakes - prefer post-1985 construction or documented structural renovation), debts that attach to the asset, and slow registry bureaucracy. Israeli tax applies to the income under the usual tracks, with treaty credits. Figures for illustration only.',
					),
				),
			),
			'faq' => array(
				array( 'האם 250 אלף אירו עדיין מספיקים לוויזת זהב?', 'Is EUR 250K still enough for the golden visa?', 'רק במסלול מיוחד: נכסים המיועדים לשיפוץ מהותי או הסבה משימוש אחר, בתנאים מוגדרים. במסלול הרגיל: 800 אלף באזורי הביקוש או 400 אלף בשאר המדינה.', 'Only via the special track: assets designated for substantial renovation or use conversion, under defined terms. The standard track: 800K in demand zones or 400K elsewhere.' ),
				array( 'כמה עולה להחזיק דירה באתונה?', 'What does holding an Athens flat cost?', 'ENFIA שנתי (מאות עד אלפי אירו), דמי בניין צנועים יחסית, ביטוח, וניהול השכרה של 8%-10%. מס יווני על השכירות מ-15% ומעלה לפי מדרגות.', 'Annual ENFIA (hundreds to thousands of EUR), relatively modest building fees, insurance, and 8-10% rental management. Greek tax on rent from 15% up by bracket.' ),
				array( 'אתונה או האיים?', 'Athens or the islands?', 'אתונה = שוק שכירות עמוק כל השנה ונזילות; האיים = תשואת עונה גבוהה אך תלות מוחלטת בתיירות ובניהול מרחוק. למשקיע ראשון ביוון, אתונה היא נקודת הפתיחה הבטוחה.', 'Athens = deep year-round tenancy and liquidity; the islands = high seasonal yield but total dependence on tourism and remote management. For a first Greek investment, Athens is the safe starting point.' ),
			),
			'src_he' => 'נתוני שוק: יולי 2026, מקורות פומביים (Bank of Greece, Enterprise Greece, Spitogatos). אומדנים להמחשה בלבד - לא ייעוץ השקעות, מס או משפט.',
			'src_en' => 'Market data: July 2026, public sources (Bank of Greece, Enterprise Greece, Spitogatos). Estimates for illustration only - not investment, tax or legal advice.',
		),

		'thailand' => array(
			'name_he' => 'תאילנד', 'name_en' => 'Thailand', 'country_he' => 'תאילנד', 'country_en' => 'Thailand',
			'flag' => '🇹🇭', 'currency' => 'THB', 'center' => array( 100.5018, 13.7563 ), 'zoom' => 11,
			'title_he' => 'השקעות נדל"ן בתאילנד: קונדו בבנגקוק ופוקט, בעלות זרים, מחירים והמדריך המלא | נדלן',
			'title_en' => 'Thailand Property Investment: Bangkok and Phuket Condos, Foreign Ownership and the Guide | Nadlan',
			'desc_he'  => 'המדריך המלא להשקעה בקונדו בתאילנד: מכסת 49% לזרים, מחירי בנגקוק ופוקט, תשואות 5%-7%, מיסים, תהליך הרכישה ופרויקטים להמחשה בתלת ממד ועל המפה.',
			'desc_en'  => 'The complete Thailand condo guide: the 49% foreign quota, Bangkok and Phuket pricing, 5-7% yields, taxes, the buying process and illustrative projects in 3D and on the map.',
			'h1_he' => 'השקעות נדל"ן בתאילנד: העולם המלא למשקיע',
			'h1_en' => 'Thailand Property: the Complete Investor World',
			'intro_he' => 'תאילנד מציעה את יחס המחיר-חוויה הטוב באסיה למשקיע פרטי: קונדו חדש במרכז בנגקוק ב-80-150 אלף באט למ"ר (כ-2,200-4,200 דולר), תשואות ברוטו של 5%-7%, ותיירות של עשרות מיליוני מבקרים שמזינה את שוק השכירות בפוקט, פטאיה וקוסמוי. זר יכול להחזיק קונדו בבעלות מלאה על שמו - כל עוד חלקם של הזרים בבניין אינו עולה על 49%, המכסה שקובע החוק התאילנדי. קרקע ובתים פרטיים אי אפשר להחזיק ישירות - וכל מבנה עקיף שמציעים לכם דורש בדיקה משפטית קפדנית. בעמוד הזה: הנתונים, מכסת הזרים, המיסים, תהליך הרכישה כולל העברת המט"ח המתועדת, הסיכונים, ופרויקטים להמחשה בתלת ממד ועל המפה.',
			'intro_en' => 'Thailand offers Asia\'s best price-to-experience ratio for the private investor: new central-Bangkok condos at THB 80-150K per sqm (~USD 2,200-4,200), 5-7% gross yields, and tens of millions of tourists feeding the rental markets of Phuket, Pattaya and Samui. A foreigner can hold a condo freehold in their own name - as long as foreign ownership in the building does not exceed the 49% quota Thai law sets. Land and houses cannot be held directly - and any indirect structure offered to you needs strict legal review. On this page: the data, the quota, taxes, the process including the documented FX transfer, the risks, and illustrative projects in 3D and on the map.',
			'facts' => array(
				array( 'מחיר קונדו בבנגקוק', 'Bangkok condo pricing', '80-150 אלף באט למ"ר במרכז (סוקומווית, סאטורן)', 'THB 80-150K per sqm central (Sukhumvit, Sathorn)' ),
				array( 'תשואת שכירות ברוטו', 'Gross rental yield', 'כ-5%-7%; בפוקט עונתי וגבוה יותר', '~5-7%; Phuket seasonal and higher' ),
				array( 'בעלות זרים בקונדו', 'Foreign condo ownership', 'בעלות מלאה עד מכסת 49% זרים בבניין', 'Full freehold within the 49% building quota' ),
				array( 'קרקע ובתים', 'Land and houses', 'אסורים לבעלות זרה ישירה; חכירה 30 שנה בלבד', 'No direct foreign ownership; 30-year leasehold only' ),
				array( 'מיסי רכישה', 'Purchase taxes', 'העברה 2% (מתחלק לרוב) + אגרות; סך הכל נמוך יחסית', '2% transfer (usually split) + fees; comparatively low' ),
				array( 'מס רכוש שנתי', 'Annual property tax', 'נמוך מאוד (Land and Building Tax)', 'Very low (Land and Building Tax)' ),
				array( 'דרישת מט"ח', 'FX requirement', 'הכסף חייב להגיע מחו"ל במט"ח עם אישור FET', 'Funds must arrive from abroad in FX with an FET certificate' ),
				array( 'אזורים מובילים', 'Top districts', 'בנגקוק: סוקומווית, סאטורן, ראמה 9; פוקט: באנג טאו, קמאלה', 'Bangkok: Sukhumvit, Sathorn, Rama 9; Phuket: Bang Tao, Kamala' ),
			),
			'guide' => array(
				array( 'מכסת ה-49% והעברת המט"ח: שני הכללים שאסור לשבור', 'The 49% quota and the FX transfer: the two unbreakable rules',
					array(
						'החוק התאילנדי מתיר לזרים להחזיק עד 49% משטח הדירות בכל בניין קונדו. לפני חתימה, היזם או עורך הדין חייבים להציג אישור שנותרה מכסה זרה פנויה - בבניינים מבוקשים היא נגמרת. הכלל השני: את מלוא התמורה חייבים להעביר מחו"ל במטבע זר, והבנק המקומי מנפיק אישור FET - בלעדיו לא ירשמו את הדירה על שמכם וגם לא תוכלו להוציא את הכסף בחזרה במכירה. שמרו כל מסמך.',
					),
					array(
						'Thai law lets foreigners hold up to 49% of the apartment area in any condo building. Before signing, the developer or your lawyer must show that foreign quota remains - in sought-after buildings it runs out. The second rule: the full price must arrive from abroad in foreign currency, and the local bank issues an FET certificate - without it the unit cannot be registered in your name, and you cannot repatriate the money on sale. Keep every document.',
					),
				),
				array( 'בנגקוק מול פוקט: שני שווקים שונים', 'Bangkok vs Phuket: two different markets',
					array(
						'בנגקוק היא שוק שכירות אורבני יציב: שוכרים מקומיים ומגורי אקספטים ליד קווי הרכבת, חוזים שנתיים, ותנודתיות עונתית נמוכה - הבסיס הנכון להשקעה ראשונה. פוקט היא מכונת תיירות: תשואות עונתיות גבוהות בניהול מלונאי (תוכניות של 5%-7% "מובטחים" לתקופה - קראו את האותיות הקטנות), אבל תלות מוחלטת בתיירות ובמפעיל. משקיע שמרן יתחיל בבנגקוק; מחפש תשואה עונתית - פוקט עם מפעיל מוכח.',
					),
					array(
						'Bangkok is a stable urban rental market: local tenants and expats around the BTS/MRT lines, annual leases, low seasonality - the right base for a first investment. Phuket is a tourism machine: high seasonal returns under hotel management (programs "guaranteeing" 5-7% for a period - read the fine print), but total dependence on tourism and the operator. A conservative investor starts in Bangkok; yield hunters take Phuket with a proven operator.',
					),
				),
				array( 'הסיכונים שאסור להתעלם מהם', 'The risks you must not ignore',
					array(
						'הבאט תנודתי מול השקל ואין אמנת מס מלאה עם ישראל להכנסות אלה - תכנון מס ישראלי (מסלול 15% או שולי) חובה מראש. עוד: היצע קונדו גדול בבנגקוק שוחק עליית ערך, שוק יד שנייה איטי (זרים קונים כמעט רק חדש), הבטחות תשואה של יזמים חזקות בדיוק כמו היזם - בדקו איתנות, ומבני חכירה או חברה להחזקת קרקע לזרים הם שדה מוקשים משפטי. קנו קונדו במכסה, בבניין מיזם מוכר, ותחיו בשקט. הנתונים להמחשה בלבד.',
					),
					array(
						'The baht swings against the shekel and there is no full tax treaty with Israel covering this income - Israeli tax planning (15% track or marginal) is mandatory up front. Also: heavy Bangkok condo supply caps appreciation, the resale market is slow (foreigners buy almost only new), developer "guaranteed returns" are only as strong as the developer - verify strength, and leasehold or land-holding-company structures for foreigners are a legal minefield. Buy a freehold condo within quota, from an established developer, and sleep well. Figures for illustration only.',
					),
				),
			),
			'faq' => array(
				array( 'האם זר יכול להחזיק דירה בתאילנד על שמו?', 'Can a foreigner hold a Thai condo in their own name?', 'כן - קונדו בלבד, בבעלות מלאה, כל עוד סך הזרים בבניין עד 49% מהשטח. קרקע ובתים פרטיים - לא.', 'Yes - condos only, full freehold, as long as total foreign ownership in the building is within 49% of area. Land and houses - no.' ),
				array( 'מה זה אישור FET ולמה הוא קריטי?', 'What is the FET certificate and why is it critical?', 'אישור בנקאי שהכסף הגיע מחו"ל במט"ח לצורך רכישת הדירה. בלעדיו אין רישום בעלות לזר, ואי אפשר להחזיר את הכסף לחו"ל במכירה. שומרים אותו כמו את חוזה הרכישה.', 'A bank certificate that the funds arrived from abroad in FX for the purchase. Without it there is no foreign title registration, and no repatriation on sale. Guard it like the purchase contract.' ),
				array( 'האם הבטחות תשואה בפוקט אמינות?', 'Are Phuket guaranteed returns reliable?', 'הן התחייבות חוזית של היזם או המפעיל - חזקות בדיוק כמוהו. בדקו עבר ביצועי, מי המפעיל המלונאי, ומה קורה בתום תקופת ההבטחה. אל תקנו על בסיס ההבטחה בלבד.', 'They are a contractual promise by the developer or operator - exactly as strong as they are. Check delivery history, who the hotel operator is, and what happens when the guarantee period ends. Never buy on the guarantee alone.' ),
			),
			'src_he' => 'נתוני שוק: יולי 2026, מקורות פומביים (Bank of Thailand, CBRE Thailand, DDproperty). אומדנים להמחשה בלבד - לא ייעוץ השקעות, מס או משפט.',
			'src_en' => 'Market data: July 2026, public sources (Bank of Thailand, CBRE Thailand, DDproperty). Estimates for illustration only - not investment, tax or legal advice.',
		),

		'italy' => array(
			'name_he' => 'איטליה', 'name_en' => 'Italy', 'country_he' => 'איטליה', 'country_en' => 'Italy',
			'flag' => '🇮🇹', 'currency' => 'EUR', 'center' => array( 9.19, 45.4642 ), 'zoom' => 11,
			'title_he' => 'השקעות נדל"ן באיטליה: מילאנו, רומא והדרום, מיסים והמדריך המלא למשקיע הישראלי | נדלן',
			'title_en' => 'Italy Property Investment: Milan, Rome and the South, Taxes and the Complete Guide | Nadlan',
			'desc_he'  => 'המדריך המלא להשקעה בדירה באיטליה: מחירי מילאנו ורומא, מס רכישה 2%/9%, מס 7% לפנסיונרים בדרום, תהליך נוטריוני, תשואות ופרויקטים להמחשה בתלת ממד ועל המפה.',
			'desc_en'  => 'The complete Italy investment guide: Milan and Rome pricing, the 2%/9% purchase tax, the 7% southern flat tax, the notarial process, yields and illustrative projects in 3D and on the map.',
			'h1_he' => 'השקעות נדל"ן באיטליה: העולם המלא למשקיע',
			'h1_en' => 'Italy Property: the Complete Investor World',
			'intro_he' => 'איטליה מציעה למשקיע הישראלי שילוב שאין באירופה: מילאנו - בירת הכלכלה והאופנה עם שוק שכירות של סטודנטים ומנהלים ותשואות של 4%-6%, רומא - ביקוש תיירותי אינסופי במרכז ההיסטורי, והדרום - מחירים נמוכים דרמטית עם הטבת מס ייחודית של 7% שטוחים לפנסיונרים זרים שעוברים לגור בעיירות הקטנות. דירת שני חדרים במילאנו מתחילה סביב 250-400 אלף אירו באזורים המתחדשים (נולו, ביקוקה), ובדרום אפשר למצוא נכסים בעשרות אלפי אירו הדורשים שיפוץ. התהליך האיטלקי נוטריוני ומסודר אך איטי, והמיסוי תלוי מאוד בשאלה אם זו דירה ראשונה או השקעה. בעמוד: הנתונים, המיסים, התהליך, הסיכונים, ופרויקטים להמחשה בתלת ממד ועל המפה.',
			'intro_en' => 'Italy offers a combination Europe cannot match: Milan - the economic and fashion capital with a student-and-executive rental market and 4-6% yields, Rome - endless tourist demand in the historic center, and the South - dramatically low prices with a unique 7% flat tax for foreign pensioners relocating to small towns. A two-room Milan flat starts around EUR 250-400K in regenerating districts (NoLo, Bicocca), and southern assets can be found for tens of thousands needing renovation. The Italian process is notarial and orderly but slow, and taxation hinges on first-home vs investment status. On this page: the data, the taxes, the process, the risks, and illustrative projects in 3D and on the map.',
			'facts' => array(
				array( 'מחיר במילאנו', 'Milan pricing', '250-400 אלף אירו לדירת 2 חדרים באזורים מתחדשים', 'EUR 250-400K for a 2-room flat in regenerating districts' ),
				array( 'תשואת שכירות ברוטו', 'Gross rental yield', 'כ-4%-6% במילאנו; רומא מרכז - תיירותי', '~4-6% in Milan; central Rome - touristic' ),
				array( 'מס רכישה', 'Purchase tax', '9% מהערך הקדסטרלי (השקעה); 2% דירה ראשונה לתושב', '9% of cadastral value (investment); 2% first home for residents' ),
				array( 'מס 7% בדרום', 'The 7% southern flat tax', 'לפנסיונרים זרים שעוברים לעיירות עד 20 אלף תושבים בדרום - 7% על כלל ההכנסה מחו"ל ל-10 שנים', 'Foreign pensioners relocating to southern towns under 20K residents - 7% on all foreign income for 10 years' ),
				array( 'מס על שכירות', 'Tax on rent', 'מסלול שטוח נפוץ של 21% (Cedolare Secca)', 'The common flat 21% track (cedolare secca)' ),
				array( 'מס רכוש שנתי (IMU)', 'Annual property tax (IMU)', 'כ-0.5%-1.1% מהערך הקדסטרלי, על נכס שאינו דירה ראשונה', '~0.5-1.1% of cadastral value on non-primary homes' ),
				array( 'בעלות לזרים', 'Foreign ownership', 'חופשית לישראלים (הדדיות)', 'Unrestricted for Israelis (reciprocity)' ),
				array( 'אזורים מובילים', 'Top districts', 'מילאנו: נולו, ביקוקה, פורטה רומאנה; רומא: מרכז; הדרום: פוליה, סיציליה', 'Milan: NoLo, Bicocca, Porta Romana; Rome: center; South: Puglia, Sicily' ),
			),
			'guide' => array(
				array( 'התהליך האיטלקי: הסכם מוקדם, נוטריון וקדסטר', 'The Italian process: compromesso, notary and cadastre',
					array(
						'עסקה איטלקית נחתמת בשני שלבים: הסכם מוקדם (Compromesso) עם מקדמה של 10%-20% שנרשמת, ואז חוזה סופי (Rogito) בפני נוטריון - הדמות המרכזית בעסקה, שבודקת בעלות, שעבודים והתאמה תכנונית. לפני הכל תצטרכו מספר מס איטלקי (Codice Fiscale) - מנפיקים אותו גם בקונסוליה. שימו לב לערך הקדסטרלי: מסי הרכישה מחושבים ממנו ולא מהמחיר בפועל, ולכן המס האפקטיבי נמוך בהרבה מ-9% נומינלי ברוב העסקאות. אי-סדרים תכנוניים נפוצים בבניינים ישנים - עורך דין מטעמכם, נוסף לנוטריון, שווה כל אירו.',
					),
					array(
						'An Italian deal signs in two stages: the preliminary agreement (compromesso) with a registered 10-20% deposit, then the final deed (rogito) before a notary - the central figure, who verifies title, liens and planning compliance. Before anything you need a codice fiscale (Italian tax number) - issuable at a consulate too. Note the cadastral value: purchase taxes compute from it, not the actual price, so effective tax is far below the nominal 9% in most deals. Planning irregularities are common in older buildings - your own lawyer, alongside the notary, is worth every euro.',
					),
				),
				array( 'מילאנו, רומא או הדרום: שלוש אסטרטגיות', 'Milan, Rome or the South: three strategies',
					array(
						'מילאנו היא ההשקעה היציבה של איטליה: כלכלה חזקה, ביקוש שכירות עמוק, ואזורים מתחדשים סביב האוניברסיטאות וקווי המטרו החדשים. רומא מרכז - נכס תיירותי בשכירות קצרה (בכפוף לרגולציה המתהדקת). והדרום - פוליה, סיציליה, קלבריה - הוא סיפור אחר: מחירי כניסה נמוכים מאוד, לעיתים עם עלויות שיפוץ שעולות על מחיר הנכס, והטבת ה-7% שהופכת אותו למקלט מס אמיתי לפנסיונרים. אל תערבבו אסטרטגיות: תזרים במילאנו, תיירות ברומא, סגנון חיים ומס בדרום.',
					),
					array(
						'Milan is Italy\'s stable investment: a strong economy, deep rental demand, regenerating districts around the universities and new metro lines. Central Rome - a touristic short-let asset (subject to tightening regulation). And the South - Puglia, Sicily, Calabria - is a different story: very low entry prices, renovation costs sometimes exceeding the asset price, and the 7% benefit that makes it a genuine tax haven for pensioners. Do not mix strategies: cash flow in Milan, tourism in Rome, lifestyle-and-tax in the South.',
					),
				),
				array( 'הסיכונים שאסור להתעלם מהם', 'The risks you must not ignore',
					array(
						'איטליה איטית: רישום, היתרים ובתי משפט מתנהלים בקצב משלהם, ופינוי שוכר בעייתי יכול לקחת שנים - סננו שוכרים בקפדנות והעדיפו חוזה רשום במסלול הנכון. בדקו התחייבויות ועד בית ועבודות מאושרות בבניין (אתם יורשים החלטות שקדמו לכם), מצב סייסמי בדרום, ותכנון מס ישראלי לפי אמנת המס. נכסי "אירו אחד" ודומיהם הם פרויקט שיפוץ עם מחויבויות - לא השקעה פסיבית. הנתונים להמחשה בלבד.',
					),
					array(
						'Italy is slow: registration, permits and courts run at their own pace, and evicting a problematic tenant can take years - screen tenants rigorously and prefer a properly registered lease. Check condominium obligations and approved building works (you inherit decisions made before you), seismic status in the South, and Israeli tax planning under the treaty. "One euro" homes and their cousins are renovation projects with obligations - not passive investments. Figures for illustration only.',
					),
				),
			),
			'faq' => array(
				array( 'כמה מס רכישה משלמים בפועל?', 'How much purchase tax in practice?', 'השקעה ממוסה ב-9% מהערך הקדסטרלי - שנמוך בדרך כלל משמעותית ממחיר השוק, כך שהמס האפקטיבי על המחיר הוא לרוב 2%-4%. בנכס חדש מיזם: מע"מ 10% מהמחיר במקום.', 'Investments pay 9% of cadastral value - usually far below market price, so effective tax on price is typically 2-4%. New from a developer: 10% VAT on price instead.' ),
				array( 'מה באמת נותן מס ה-7% בדרום?', 'What does the 7% southern tax really give?', 'פנסיונר זר שמעביר את מושבו לעיירה דרומית של עד 20 אלף תושבים משלם 7% שטוחים על כלל הכנסותיו מחו"ל (כולל פנסיה ושכירות מנכסים בחו"ל) למשך 10 שנים. דורש מעבר מגורים אמיתי.', 'A foreign pensioner relocating residence to a southern town under 20K residents pays a flat 7% on all foreign income (pension and foreign rents included) for 10 years. Requires a genuine move.' ),
				array( 'קל לפנות שוכר באיטליה?', 'Is evicting a tenant easy in Italy?', 'לא. ההליך יכול להימשך זמן רב, במיוחד בחורף ובדירות מגורים. לכן: סינון קפדני, ערבויות, חוזה רשום במסלול הנכון, וביטוח שכירות - לפני החתימה, לא אחריה.', 'No. Proceedings can run long, especially in winter and residential lets. Hence: rigorous screening, guarantees, a properly registered lease and rent insurance - before signing, not after.' ),
			),
			'src_he' => 'נתוני שוק: יולי 2026, מקורות פומביים (Agenzia delle Entrate, Immobiliare.it, Idealista). אומדנים להמחשה בלבד - לא ייעוץ השקעות, מס או משפט.',
			'src_en' => 'Market data: July 2026, public sources (Agenzia delle Entrate, Immobiliare.it, Idealista). Estimates for illustration only - not investment, tax or legal advice.',
		),

		);
		return apply_filters( 'nadlan_gw_worlds', $W );
	}
}

/* ============================ CPT + metabox ============================ */
add_action( 'init', function () {
	register_post_type( 'nadlan_intl', array(
		'labels'       => array( 'name' => 'Global Projects', 'singular_name' => 'Global Project' ),
		'public'       => true,
		'has_archive'  => false,
		'show_in_rest' => false,
		'menu_icon'    => 'dashicons-admin-site-alt3',
		'supports'     => array( 'title', 'editor', 'thumbnail' ),
		'rewrite'      => array( 'slug' => 'global/project', 'with_front' => false ),
	) );
} );

add_action( 'add_meta_boxes', function () {
	add_meta_box( 'nadlan_gw_panel', 'פרויקט בינלאומי (Global World)', 'nadlan_gw_metabox_render', 'nadlan_intl', 'normal', 'high' );
} );

if ( ! function_exists( 'nadlan_gw_metabox_render' ) ) {
	function nadlan_gw_metabox_render( $post ) {
		wp_nonce_field( 'nadlan_gw_metabox', 'nadlan_gw_metabox_nonce' );
		$m = function ( $k ) use ( $post ) { return esc_attr( (string) get_post_meta( $post->ID, $k, true ) ); };
		$world = (string) get_post_meta( $post->ID, 'gw_world', true );
		?>
		<div dir="rtl" style="max-width:720px">
			<p><label style="font-weight:600">עולם (מיקום)</label><br>
			<select name="gw_world"><option value="">בחרו...</option>
			<?php foreach ( nadlan_gw_worlds() as $code => $w ) : ?>
				<option value="<?php echo esc_attr( $code ); ?>" <?php selected( $world, $code ); ?>><?php echo esc_html( $w['name_he'] ); ?></option>
			<?php endforeach; ?></select></p>
			<p><label style="font-weight:600">שכונה / רובע</label><br><input type="text" name="gw_district" value="<?php echo $m( 'gw_district' ); ?>" style="width:280px"> <label style="font-weight:600">שכונה EN</label> <input type="text" name="gw_district_en" value="<?php echo $m( 'gw_district_en' ); ?>" style="width:220px" dir="ltr"></p>
			<p><label>קו רוחב <input type="text" name="gw_lat" value="<?php echo $m( 'gw_lat' ); ?>" style="width:120px" dir="ltr"></label>
			<label>קו אורך <input type="text" name="gw_lng" value="<?php echo $m( 'gw_lng' ); ?>" style="width:120px" dir="ltr"></label></p>
			<p><label>מחיר החל מ- <input type="text" name="gw_price_from" value="<?php echo $m( 'gw_price_from' ); ?>" style="width:140px" dir="ltr" placeholder="950000"></label>
			<label>יח״ד <input type="number" name="gw_units" value="<?php echo $m( 'gw_units' ); ?>" style="width:80px"></label>
			<label>קומות <input type="number" name="gw_floors" value="<?php echo $m( 'gw_floors' ); ?>" style="width:80px"></label>
			<label>מסירה <input type="text" name="gw_delivery" value="<?php echo $m( 'gw_delivery' ); ?>" style="width:80px" placeholder="2027"></label></p>
			<p><label style="font-weight:600">הערת תשואה (עם תווית הגינות)</label><br><input type="text" name="gw_yield" value="<?php echo $m( 'gw_yield' ); ?>" style="width:100%"></p>
			<p><label style="font-weight:600">תיאור EN (פסקה)</label><br><textarea name="gw_about_en" style="width:100%;min-height:70px"><?php echo esc_textarea( (string) get_post_meta( $post->ID, 'gw_about_en', true ) ); ?></textarea></p>
			<p><label style="font-weight:600">כתובת GLB (ריק = המגדל הסטנדרטי)</label><br><input type="url" name="gw_glb" value="<?php echo $m( 'gw_glb' ); ?>" style="width:100%" dir="ltr"></p>
			<p><label style="font-weight:600">תוכנית תשלומים</label><br><input type="text" name="gw_payment" value="<?php echo $m( 'gw_payment' ); ?>" style="width:100%" placeholder="60/40 לאורך הבנייה"></p>
			<p><label style="font-weight:600">דמי ניהול / אחזקה</label><br><input type="text" name="gw_fees" value="<?php echo $m( 'gw_fees' ); ?>" style="width:100%"></p>
			<p><label style="font-weight:600">מתקנים וסביבה (שורה לכל פריט: עברית | English)</label><br><textarea name="gw_facilities" style="width:100%;min-height:80px" placeholder="בריכת אינפיניטי | Infinity pool"><?php
				$fac = json_decode( (string) get_post_meta( $post->ID, 'gw_facilities', true ), true );
				if ( is_array( $fac ) ) { foreach ( $fac as $f ) { echo esc_textarea( $f[0] . ' | ' . $f[1] ) . "\n"; } }
			?></textarea></p>
			<p><label style="font-weight:600">מלאי דירות (JSON; נזרע אוטומטית בפרויקט המחשה)</label><br><textarea name="gw_apartments" style="width:100%;min-height:80px" dir="ltr"><?php echo esc_textarea( (string) get_post_meta( $post->ID, 'gw_apartments', true ) ); ?></textarea>
			<span style="color:#666;font-size:12px">מערך של יחידות: {"id","floor","pos","dir","rooms","sqm","price","status","view_he","view_en"}. status: available/reserved/sold.</span></p>
			<p><label><input type="checkbox" name="gw_demo" value="1" <?php checked( get_post_meta( $post->ID, 'gw_demo', true ), '1' ); ?>> פרויקט להמחשה (מציג את תג ההגינות)</label></p>
		</div>
		<?php
	}
}

add_action( 'save_post_nadlan_intl', function ( $post_id ) {
	if ( ! isset( $_POST['nadlan_gw_metabox_nonce'] )
		|| ! wp_verify_nonce( sanitize_text_field( wp_unslash( $_POST['nadlan_gw_metabox_nonce'] ) ), 'nadlan_gw_metabox' ) ) { return; }
	if ( defined( 'DOING_AUTOSAVE' ) && DOING_AUTOSAVE ) { return; }
	if ( ! current_user_can( 'edit_post', $post_id ) ) { return; }
	$world = isset( $_POST['gw_world'] ) ? sanitize_key( wp_unslash( $_POST['gw_world'] ) ) : '';
	update_post_meta( $post_id, 'gw_world', array_key_exists( $world, nadlan_gw_worlds() ) ? $world : '' );
	foreach ( array( 'gw_district', 'gw_district_en', 'gw_price_from', 'gw_delivery', 'gw_yield', 'gw_payment', 'gw_fees' ) as $k ) {
		update_post_meta( $post_id, $k, isset( $_POST[ $k ] ) ? sanitize_text_field( wp_unslash( $_POST[ $k ] ) ) : '' );
	}
	if ( isset( $_POST['gw_facilities'] ) ) {
		$fac = array();
		foreach ( explode( "\n", sanitize_textarea_field( wp_unslash( $_POST['gw_facilities'] ) ) ) as $line ) {
			$parts = array_map( 'trim', explode( '|', $line, 2 ) );
			if ( '' !== $parts[0] ) { $fac[] = array( $parts[0], isset( $parts[1] ) && '' !== $parts[1] ? $parts[1] : $parts[0] ); }
		}
		update_post_meta( $post_id, 'gw_facilities', wp_json_encode( array_slice( $fac, 0, 24 ), JSON_UNESCAPED_UNICODE ) );
	}
	if ( isset( $_POST['gw_apartments'] ) ) {
		$apts = json_decode( (string) wp_unslash( $_POST['gw_apartments'] ), true );
		update_post_meta( $post_id, 'gw_apartments', is_array( $apts ) ? wp_json_encode( nadlan_gw_clean_apartments( $apts ), JSON_UNESCAPED_UNICODE ) : '' );
	}
	foreach ( array( 'gw_lat', 'gw_lng' ) as $k ) {
		$v = isset( $_POST[ $k ] ) ? trim( sanitize_text_field( wp_unslash( $_POST[ $k ] ) ) ) : '';
		if ( '' === $v || is_numeric( $v ) ) { update_post_meta( $post_id, $k, $v ); }
	}
	update_post_meta( $post_id, 'gw_units', isset( $_POST['gw_units'] ) ? absint( $_POST['gw_units'] ) : 0 );
	update_post_meta( $post_id, 'gw_floors', isset( $_POST['gw_floors'] ) ? absint( $_POST['gw_floors'] ) : 0 );
	update_post_meta( $post_id, 'gw_about_en', isset( $_POST['gw_about_en'] ) ? sanitize_textarea_field( wp_unslash( $_POST['gw_about_en'] ) ) : '' );
	update_post_meta( $post_id, 'gw_glb', isset( $_POST['gw_glb'] ) ? esc_url_raw( wp_unslash( $_POST['gw_glb'] ) ) : '' );
	update_post_meta( $post_id, 'gw_demo', ! empty( $_POST['gw_demo'] ) ? '1' : '0' );
} );

/* ============================ routes ============================ */
add_action( 'init', function () {
	$codes = implode( '|', array_map( 'preg_quote', array_keys( nadlan_gw_worlds() ) ) );
	add_rewrite_rule( '^global/?$', 'index.php?nadlan_gw_hub=1', 'top' );
	add_rewrite_rule( '^global/(' . $codes . ')/?$', 'index.php?nadlan_gw_world=$matches[1]', 'top' );
	if ( get_option( 'nadlan_gw_rewrite_v1' ) !== '1' ) {
		flush_rewrite_rules( false );
		update_option( 'nadlan_gw_rewrite_v1', '1' );
	}
} );
add_filter( 'query_vars', function ( $v ) { $v[] = 'nadlan_gw_hub'; $v[] = 'nadlan_gw_world'; return $v; } );

if ( ! function_exists( 'nadlan_gw_clean_apartments' ) ) {
	function nadlan_gw_clean_apartments( $raw ) {
		if ( ! is_array( $raw ) ) { return array(); }
		$out = array();
		foreach ( array_slice( $raw, 0, 60 ) as $a ) {
			if ( ! is_array( $a ) ) { continue; }
			$out[] = array(
				'id'      => sanitize_key( (string) ( $a['id'] ?? '' ) ),
				'floor'   => max( 0, (int) ( $a['floor'] ?? 0 ) ),
				'pos'     => max( 0, min( 2, (int) ( $a['pos'] ?? 0 ) ) ),
				'dir'     => in_array( ( $a['dir'] ?? '' ), array( 'west', 'east', 'north', 'south' ), true ) ? $a['dir'] : 'west',
				'rooms'   => max( 1, min( 6, (int) ( $a['rooms'] ?? 1 ) ) ),
				'sqm'     => max( 0, (int) ( $a['sqm'] ?? 0 ) ),
				'price'   => max( 0, (float) ( $a['price'] ?? 0 ) ),
				'status'  => in_array( ( $a['status'] ?? '' ), array( 'available', 'reserved', 'sold' ), true ) ? $a['status'] : 'available',
				'view_he' => sanitize_text_field( (string) ( $a['view_he'] ?? '' ) ),
				'view_en' => sanitize_text_field( (string) ( $a['view_en'] ?? '' ) ),
			);
		}
		return $out;
	}
}

if ( ! function_exists( 'nadlan_gw_projects_for' ) ) {
	function nadlan_gw_projects_for( $code ) {
		$q = new WP_Query( array(
			'post_type' => 'nadlan_intl', 'post_status' => 'publish', 'posts_per_page' => 24,
			'no_found_rows' => true, 'meta_key' => 'gw_world', 'meta_value' => $code,
		) );
		return $q->posts;
	}
}

if ( ! function_exists( 'nadlan_gw_lang' ) ) {
	function nadlan_gw_lang() {
		return ( isset( $_GET['lang'] ) && 'en' === sanitize_key( wp_unslash( $_GET['lang'] ) ) ) ? 'en' : 'he';
	}
}

if ( ! function_exists( 'nadlan_gw_head' ) ) {
	function nadlan_gw_head( $title, $desc, $he_url, $en_url, $lang, $schema = array() ) {
		add_filter( 'pre_get_document_title', function () use ( $title ) { return $title; }, 99 );
		add_action( 'wp_head', function () use ( $desc, $he_url, $en_url, $lang, $schema ) {
			$self = 'en' === $lang ? $en_url : $he_url;
			echo '<meta name="description" content="' . esc_attr( $desc ) . '">' . "\n";
			echo '<link rel="canonical" href="' . esc_url( $self ) . '">' . "\n";
			echo '<link rel="alternate" hreflang="he" href="' . esc_url( $he_url ) . '">' . "\n";
			echo '<link rel="alternate" hreflang="en" href="' . esc_url( $en_url ) . '">' . "\n";
			echo '<link rel="alternate" hreflang="x-default" href="' . esc_url( $he_url ) . '">' . "\n";
			foreach ( $schema as $s ) {
				echo '<script type="application/ld+json">' . wp_json_encode( $s, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES ) . '</script>' . "\n";
			}
		}, 4 );
	}
}

/* ============================ the hub /global/ ============================ */
add_action( 'template_redirect', function () {
	if ( ! get_query_var( 'nadlan_gw_hub' ) ) { return; }
	if ( ! nadlan_gw_on() ) { wp_safe_redirect( home_url( '/' ) ); exit; }
	$lang = nadlan_gw_lang();
	$en = ( 'en' === $lang );
	$he_url = home_url( '/global/' ); $en_url = home_url( '/global/?lang=en' );
	$title = $en ? 'International Real Estate Investment Worlds: Dubai, Miami, New York | Nadlan'
		: 'השקעות נדל"ן בחו"ל: דובאי, מיאמי, ניו יורק - העולמות המלאים למשקיע הישראלי | נדלן';
	$desc = $en ? 'Every location is a full world: market data, taxes, the buying process, illustrative projects in 3D and on the map. Dubai, Miami and New York for the Israeli investor.'
		: 'כל מיקום הוא עולם שלם: נתוני שוק, מיסים, תהליך רכישה, פרויקטים להמחשה בתלת ממד ועל המפה. דובאי, מיאמי וניו יורק למשקיע הישראלי.';
	nadlan_gw_head( $title, $desc, $he_url, $en_url, $lang, array( array(
		'@context' => 'https://schema.org', '@type' => 'CollectionPage', 'name' => $title, 'description' => $desc, 'url' => $en ? $en_url : $he_url,
	) ) );
	get_header();
	nadlan_gw_css();
	?>
<div class="nlgw" dir="<?php echo $en ? 'ltr' : 'rtl'; ?>" lang="<?php echo esc_attr( $lang ); ?>">
	<header class="nlgw-head">
		<p class="nlgw-kicker"><?php echo $en ? 'Nadlan Global' : 'נדלן גלובל'; ?></p>
		<h1><?php echo $en ? 'International investment: every location is a world' : 'השקעות נדל"ן בחו"ל: כל מיקום הוא עולם שלם'; ?></h1>
		<p class="sub"><?php echo $en
			? 'The same standard we set in Israel, abroad: honest market data, the full buying process, taxes on both sides, and illustrative projects you can explore in 3D and on the map. No hype, no fine print.'
			: 'אותו סטנדרט שקבענו בישראל, בחו"ל: נתוני שוק הגונים, תהליך הרכישה המלא, המיסים בשני הצדדים, ופרויקטים להמחשה שחוקרים בתלת ממד ועל המפה. בלי הייפ ובלי אותיות קטנות.'; ?></p>
		<p class="nlgw-lang"><a href="<?php echo esc_url( $en ? $he_url : $en_url ); ?>"><?php echo $en ? 'עברית' : 'English'; ?></a></p>
	</header>
	<div class="nlgw-worlds">
	<?php foreach ( nadlan_gw_worlds() as $code => $w ) :
		$n = count( nadlan_gw_projects_for( $code ) ); ?>
		<a class="nlgw-world" href="<?php echo esc_url( home_url( '/global/' . $code . '/' . ( $en ? '?lang=en' : '' ) ) ); ?>">
			<span class="flag"><?php echo esc_html( $w['flag'] ); ?></span>
			<b><?php echo esc_html( $en ? $w['name_en'] : $w['name_he'] ); ?></b>
			<i><?php echo esc_html( $en ? $w['country_en'] : $w['country_he'] ); ?></i>
			<span class="row"><?php echo esc_html( $en ? $w['facts'][0][3] : $w['facts'][0][2] ); ?></span>
			<?php if ( $n ) : ?><span class="chip"><?php echo (int) $n; ?> <?php echo $en ? 'illustrative projects' : 'פרויקטים להמחשה'; ?></span><?php endif; ?>
		</a>
	<?php endforeach; ?>
	</div>
	<section class="nlgw-devcta">
		<h2><?php echo $en ? 'Developers and agents abroad: put your project on this stage' : 'יזמים וסוכנים בחו"ל: הפרויקט שלכם על הבמה הזו'; ?></h2>
		<p><?php echo $en ? 'A living 3D model, a real map, honest data - the way we present projects in Israel. Feed your materials the same easy way.' : 'מודל תלת ממדי חי, מפה אמיתית ונתונים הגונים - כמו שאנחנו מציגים פרויקטים בישראל. הזנת החומרים פשוטה בדיוק כמו בפרויקט ישראלי.'; ?></p>
		<a class="btn" href="<?php echo esc_url( home_url( '/advertise/' ) ); ?>"><?php echo $en ? 'Get in touch' : 'דברו איתנו'; ?></a>
	</section>
	<p class="nlgw-honest"><?php echo $en
		? 'All figures on the world pages are public-source estimates for illustration (July 2026) - not investment, tax or legal advice. Illustrative projects are based on real market data and are not specific marketed projects.'
		: 'כל הנתונים בעמודי העולמות הם אומדנים ממקורות פומביים להמחשה (יולי 2026) - לא ייעוץ השקעות, מס או משפט. הפרויקטים להמחשה מבוססים על נתוני שוק אמיתיים ואינם פרויקט ספציפי בשיווק.'; ?></p>
</div>
	<?php
	get_footer();
	exit;
} );

/* ============================ a world /global/{code}/ ============================ */
add_action( 'template_redirect', function () {
	$code = get_query_var( 'nadlan_gw_world' );
	if ( ! $code ) { return; }
	if ( ! nadlan_gw_on() ) { wp_safe_redirect( home_url( '/' ) ); exit; }
	$W = nadlan_gw_worlds();
	if ( ! isset( $W[ $code ] ) ) { wp_safe_redirect( home_url( '/global/' ) ); exit; }
	$w = $W[ $code ];
	$lang = nadlan_gw_lang();
	$en = ( 'en' === $lang );
	$L = function ( $he, $en_v ) use ( $en ) { return $en ? $en_v : $he; };
	$he_url = home_url( '/global/' . $code . '/' ); $en_url = home_url( '/global/' . $code . '/?lang=en' );
	$faq_schema = array( '@context' => 'https://schema.org', '@type' => 'FAQPage', 'mainEntity' => array() );
	foreach ( $w['faq'] as $f ) {
		$faq_schema['mainEntity'][] = array( '@type' => 'Question', 'name' => $en ? $f[1] : $f[0],
			'acceptedAnswer' => array( '@type' => 'Answer', 'text' => $en ? $f[3] : $f[2] ) );
	}
	$crumbs = array( '@context' => 'https://schema.org', '@type' => 'BreadcrumbList', 'itemListElement' => array(
		array( '@type' => 'ListItem', 'position' => 1, 'name' => $L( 'נדלן', 'Nadlan' ), 'item' => home_url( '/' ) ),
		array( '@type' => 'ListItem', 'position' => 2, 'name' => $L( 'השקעות בחו"ל', 'Global' ), 'item' => home_url( '/global/' ) ),
		array( '@type' => 'ListItem', 'position' => 3, 'name' => $en ? $w['name_en'] : $w['name_he'], 'item' => $he_url ),
	) );
	$place = array( '@context' => 'https://schema.org', '@type' => 'Place', 'name' => $en ? $w['name_en'] : $w['name_he'],
		'address' => array( '@type' => 'PostalAddress', 'addressCountry' => $w['country_en'] ),
		'geo' => array( '@type' => 'GeoCoordinates', 'latitude' => $w['center'][1], 'longitude' => $w['center'][0] ) );
	nadlan_gw_head( $en ? $w['title_en'] : $w['title_he'], $en ? $w['desc_en'] : $w['desc_he'], $he_url, $en_url, $lang, array( $faq_schema, $crumbs, $place ) );
	$projects = nadlan_gw_projects_for( $code );
	$token = function_exists( 'nadlan_mapbox_token' ) ? trim( (string) nadlan_mapbox_token() ) : '';
	get_header();
	nadlan_gw_css();
	?>
<div class="nlgw" dir="<?php echo $en ? 'ltr' : 'rtl'; ?>" lang="<?php echo esc_attr( $lang ); ?>">
	<nav class="nlgw-crumbs"><a href="<?php echo esc_url( home_url( '/global/' . ( $en ? '?lang=en' : '' ) ) ); ?>"><?php echo $L( 'השקעות בחו"ל', 'Global' ); ?></a> / <span><?php echo esc_html( $en ? $w['name_en'] : $w['name_he'] ); ?></span></nav>
	<header class="nlgw-head nlgw-head--world">
		<p class="nlgw-kicker"><?php echo esc_html( $w['flag'] . ' ' . ( $en ? $w['country_en'] : $w['country_he'] ) ); ?></p>
		<h1><?php echo esc_html( $en ? $w['h1_en'] : $w['h1_he'] ); ?></h1>
		<p class="nlgw-lang"><a href="<?php echo esc_url( $en ? $he_url : $en_url ); ?>"><?php echo $en ? 'עברית' : 'English'; ?></a></p>
	</header>
	<p class="nlgw-intro"><?php echo esc_html( $en ? $w['intro_en'] : $w['intro_he'] ); ?></p>

	<section class="nlgw-facts">
		<h2><?php echo $L( 'המספרים של ' . $w['name_he'], $w['name_en'] . ' by the numbers' ); ?></h2>
		<p class="note"><?php echo esc_html( $en ? $w['src_en'] : $w['src_he'] ); ?></p>
		<div class="grid">
		<?php foreach ( $w['facts'] as $f ) : ?>
			<div class="cell"><i><?php echo esc_html( $en ? $f[1] : $f[0] ); ?></i><b><?php echo esc_html( $en ? $f[3] : $f[2] ); ?></b></div>
		<?php endforeach; ?>
		</div>
	</section>

	<?php if ( $projects ) : ?>
	<section class="nlgw-projects">
		<h2><?php echo $L( 'פרויקטים להמחשה: לחקור בתלת ממד ועל המפה', 'Illustrative projects: explore in 3D and on the map' ); ?></h2>
		<p class="note"><?php echo $L( 'מבוססים על נתוני שוק אמיתיים; אינם פרויקט ספציפי בשיווק.', 'Based on real market data; not specific marketed projects.' ); ?></p>
		<div class="cards">
		<?php foreach ( $projects as $p ) :
			$pf = (string) get_post_meta( $p->ID, 'gw_price_from', true );
			$dt = (string) get_post_meta( $p->ID, ( $en ? 'gw_district_en' : 'gw_district' ), true );
			$un = (int) get_post_meta( $p->ID, 'gw_units', true );
			$fl = (int) get_post_meta( $p->ID, 'gw_floors', true );
			$dl = (string) get_post_meta( $p->ID, 'gw_delivery', true ); ?>
			<a class="card" href="<?php echo esc_url( get_permalink( $p ) . ( $en ? '?lang=en' : '' ) ); ?>">
				<b><?php echo esc_html( $p->post_title ); ?></b>
				<i><?php echo esc_html( trim( $dt . ( $dl ? ' · ' . $dl : '' ) ) ); ?></i>
				<span class="specs"><?php if ( $fl ) : ?><?php echo (int) $fl; ?> <?php echo $L( 'קומות', 'floors' ); ?> · <?php endif; ?><?php if ( $un ) : ?><?php echo (int) $un; ?> <?php echo $L( 'יח״ד', 'units' ); ?><?php endif; ?></span>
				<?php if ( $pf ) : ?><span class="price"><?php echo $L( 'החל מ-', 'From ' ); ?><?php echo esc_html( number_format( (float) $pf ) . ' ' . $w['currency'] ); ?></span><?php endif; ?>
				<span class="go"><?php echo $L( 'לעולם הפרויקט ←', 'Enter the project →' ); ?></span>
			</a>
		<?php endforeach; ?>
		</div>
	</section>
	<?php endif; ?>

	<?php if ( $token && $projects ) : ?>
	<section class="nlgw-map">
		<h2><?php echo $L( 'על המפה', 'On the map' ); ?></h2>
		<div id="nlgw-map" class="mapbox" data-token="<?php echo esc_attr( $token ); ?>"
			data-center="<?php echo esc_attr( $w['center'][0] . ',' . $w['center'][1] ); ?>" data-zoom="<?php echo esc_attr( $w['zoom'] ); ?>"
			data-pins="<?php echo esc_attr( wp_json_encode( array_values( array_filter( array_map( function ( $p ) use ( $en ) {
				$lat = (float) get_post_meta( $p->ID, 'gw_lat', true ); $lng = (float) get_post_meta( $p->ID, 'gw_lng', true );
				if ( ! $lat || ! $lng ) { return null; }
				return array( 't' => $p->post_title, 'u' => get_permalink( $p ) . ( $en ? '?lang=en' : '' ), 'lat' => $lat, 'lng' => $lng );
			}, $projects ) ) ), JSON_UNESCAPED_UNICODE ) ); ?>"></div>
	</section>
	<?php endif; ?>

	<section class="nlgw-guide">
	<?php foreach ( $w['guide'] as $g ) : ?>
		<h2><?php echo esc_html( $en ? $g[1] : $g[0] ); ?></h2>
		<?php foreach ( ( $en ? $g[3] : $g[2] ) as $para ) : ?><p><?php echo esc_html( $para ); ?></p><?php endforeach; ?>
	<?php endforeach; ?>
	</section>

	<section class="nlgw-tools">
		<h2><?php echo $L( 'הכלים שלנו עובדים גם כאן', 'Our tools work here too' ); ?></h2>
		<div class="row">
			<a href="<?php echo esc_url( home_url( '/my-rentals/' . ( $en ? '?lang=en' : '' ) ) ); ?>"><b><?php echo $L( 'קניתם? נהלו את הנכס', 'Bought? Manage the asset' ); ?></b><i><?php echo $L( 'ניהול השכרות חינם: מעקב תשלומים, חוזה, מסמכים', 'Free rental manager: payments, lease, documents' ); ?></i></a>
			<a href="<?php echo esc_url( home_url( '/mortgage-calculator/' ) ); ?>"><b><?php echo $L( 'מחשבון משכנתא', 'Mortgage calculator' ); ?></b><i><?php echo $L( 'לתכנון המימון מהצד הישראלי', 'Plan the Israeli-side financing' ); ?></i></a>
			<a href="<?php echo esc_url( home_url( '/professionals/?profession=lawyer' ) ); ?>"><b><?php echo $L( 'ליווי מקצועי', 'Professional guidance' ); ?></b><i><?php echo $L( 'עו"ד ורו"ח המלווים ישראלים בעסקאות חו"ל', 'Lawyers and accountants for cross-border deals' ); ?></i></a>
		</div>
	</section>

	<section class="nlgw-faq">
		<h2><?php echo $L( 'שאלות נפוצות', 'Frequently asked questions' ); ?></h2>
		<?php foreach ( $w['faq'] as $f ) : ?>
		<details><summary><?php echo esc_html( $en ? $f[1] : $f[0] ); ?></summary><p><?php echo esc_html( $en ? $f[3] : $f[2] ); ?></p></details>
		<?php endforeach; ?>
	</section>

	<section class="nlgw-lead">
		<h2><?php echo $L( 'רוצים ליווי בהשקעה ב' . $w['name_he'] . '?', 'Want guidance on a ' . $w['name_en'] . ' investment?' ); ?></h2>
		<p><?php echo $L( 'השאירו פרטים ונחבר אתכם לגורם מקצועי מתאים. בלי התחייבות.', 'Leave your details and we will connect you with the right professional. No commitment.' ); ?></p>
		<form id="nlgw-lead-form">
			<input type="text" name="name" placeholder="<?php echo esc_attr( $L( 'שם מלא', 'Full name' ) ); ?>" required>
			<input type="tel" name="phone" placeholder="<?php echo esc_attr( $L( 'טלפון', 'Phone' ) ); ?>" required>
			<input type="text" name="company" tabindex="-1" autocomplete="off" style="position:absolute;left:-9999px;width:1px;height:1px;opacity:0">
			<button type="submit"><?php echo $L( 'דברו איתי', 'Contact me' ); ?></button>
			<span class="ok" hidden><?php echo $L( 'קיבלנו! נחזור אליכם.', 'Got it! We will be in touch.' ); ?></span>
		</form>
	</section>
	<p class="nlgw-honest"><?php echo esc_html( $en ? $w['src_en'] : $w['src_he'] ); ?></p>
</div>
<script>
(function(){
	var f=document.getElementById("nlgw-lead-form");
	if(f){f.addEventListener("submit",function(e){e.preventDefault();
		var fd=new FormData(f);
		fetch("<?php echo esc_url( rest_url( 'nadlan/v1/lead' ) ); ?>",{method:"POST",headers:{"Content-Type":"application/json"},
			body:JSON.stringify({name:fd.get("name"),phone:fd.get("phone"),goal:"global-<?php echo esc_js( $code ); ?>",source:"global-world",company:fd.get("company")})})
		.then(function(r){if(r.ok){f.querySelector(".ok").hidden=false;f.querySelector("button").disabled=true;}});
	});}
	var m=document.getElementById("nlgw-map");
	if(m&&m.dataset.token){
		var s=document.createElement("script");s.src="https://api.mapbox.com/mapbox-gl-js/v3.5.1/mapbox-gl.js";
		var css=document.createElement("link");css.rel="stylesheet";css.href="https://api.mapbox.com/mapbox-gl-js/v3.5.1/mapbox-gl.css";
		document.head.appendChild(css);
		s.onload=function(){
			mapboxgl.accessToken=m.dataset.token;
			var c=m.dataset.center.split(",");
			var map=new mapboxgl.Map({container:"nlgw-map",style:"mapbox://styles/mapbox/light-v11",center:[parseFloat(c[0]),parseFloat(c[1])],zoom:parseFloat(m.dataset.zoom),cooperativeGestures:true});
			map.addControl(new mapboxgl.NavigationControl());
			var pins=[];try{pins=JSON.parse(m.dataset.pins||"[]")}catch(e){}
			pins.forEach(function(p){
				var el=document.createElement("div");
				el.style.cssText="background:#C2563A;border:2px solid #FAF7F1;width:16px;height:16px;border-radius:50%;cursor:pointer;box-shadow:0 2px 8px rgba(0,0,0,.35)";
				new mapboxgl.Marker({element:el}).setLngLat([p.lng,p.lat])
					.setPopup(new mapboxgl.Popup({offset:12}).setHTML('<b style="font:700 13px Heebo">'+p.t+'</b><br><a href="'+p.u+'" style="color:#9C7A3C;font:600 12px Heebo">&larr;</a>'))
					.addTo(map);
			});
		};
		document.head.appendChild(s);
	}
})();
</script>
	<?php
	get_footer();
	exit;
} );

/* ============================ shared css ============================ */
if ( ! function_exists( 'nadlan_gw_css' ) ) {
	function nadlan_gw_css() {
		?>
<style>
.nlgw{max-width:1080px;margin:0 auto;padding:24px 16px 70px;font-family:Heebo,sans-serif;color:#1B1A17}
.nlgw h1,.nlgw h2{font-family:"Frank Ruhl Libre",Georgia,serif}
.nlgw-crumbs{font:600 12.5px Heebo;color:#8E877A;margin-bottom:8px}
.nlgw-crumbs a{color:#9C7A3C;text-decoration:none}
.nlgw-head{text-align:center;padding:24px 0 6px}
.nlgw-head--world{padding-top:8px}
.nlgw-kicker{font:700 12.5px Heebo;letter-spacing:.06em;color:#9C7A3C;text-transform:uppercase;margin:0 0 10px}
.nlgw-head h1{font-size:clamp(1.6rem,3.6vw,2.35rem);margin:0 0 10px;line-height:1.28}
.nlgw-head .sub{color:#51483A;font:400 15px/1.75 Heebo;max-width:660px;margin:0 auto}
.nlgw-lang a{color:#9C7A3C;font:600 13px Heebo;text-decoration:none;border:1px solid #E2DCD0;border-radius:999px;padding:6px 13px}
.nlgw-intro{font:400 15.5px/1.85 Heebo;color:#37322A;max-width:760px;margin:18px auto 30px;text-align:start}
.nlgw-worlds{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:16px;margin:26px 0}
.nlgw-world{display:flex;flex-direction:column;gap:6px;background:#fff;border:1.5px solid #D6C189;border-radius:18px;padding:24px;text-decoration:none;color:#1B1A17;transition:transform .18s,border-color .18s}
.nlgw-world:hover{transform:translateY(-2px);border-color:#9C7A3C}
.nlgw-world .flag{font-size:26px}
.nlgw-world b{font:700 20px "Frank Ruhl Libre",serif}
.nlgw-world i{font:600 12px Heebo;color:#8E877A;font-style:normal}
.nlgw-world .row{font:400 13px/1.5 Heebo;color:#51483A}
.nlgw-world .chip{align-self:flex-start;background:#F3EEE3;border:1px solid #E2DCD0;border-radius:999px;padding:5px 11px;font:600 11.5px Heebo;color:#51483A;margin-top:4px}
.nlgw-facts{background:#F3EEE3;border:1px solid #E2DCD0;border-radius:22px;padding:24px;margin:26px 0}
.nlgw-facts h2{margin:0 0 4px;font-size:1.3rem}
.nlgw-facts .note,.nlgw-projects .note{font:400 12px/1.6 Heebo;color:#8E877A;margin:0 0 14px}
.nlgw-facts .grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:10px}
.nlgw-facts .cell{background:#fff;border:1px solid #E2DCD0;border-radius:12px;padding:12px 14px}
.nlgw-facts .cell i{display:block;font:600 11.5px Heebo;color:#8E877A;font-style:normal;margin-bottom:3px}
.nlgw-facts .cell b{font:700 13.5px/1.45 Heebo;color:#1B1A17}
.nlgw-projects{margin:30px 0}
.nlgw-projects h2{font-size:1.35rem;margin:0 0 4px}
.nlgw-projects .cards{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:14px}
.nlgw-projects .card{display:flex;flex-direction:column;gap:5px;background:#fff;border:1px solid #E2DCD0;border-radius:16px;padding:20px;text-decoration:none;color:#1B1A17;transition:border-color .18s,transform .18s}
.nlgw-projects .card:hover{border-color:#9C7A3C;transform:translateY(-2px)}
.nlgw-projects .card b{font:700 16.5px "Frank Ruhl Libre",serif}
.nlgw-projects .card i{font:600 12px Heebo;color:#8E877A;font-style:normal}
.nlgw-projects .card .specs{font:400 12.5px Heebo;color:#51483A}
.nlgw-projects .card .price{font:800 14px Heebo;color:#C2563A;margin-top:2px}
.nlgw-projects .card .go{font:700 12.5px Heebo;color:#9C7A3C;margin-top:6px}
.nlgw-map{margin:28px 0}
.nlgw-map h2{font-size:1.3rem;margin:0 0 10px}
.nlgw-map .mapbox{height:420px;border-radius:18px;overflow:hidden;border:1px solid #D6C189;background:#EFEAE0}
.nlgw-guide{max-width:760px;margin:34px auto}
.nlgw-guide h2{font-size:1.35rem;margin:26px 0 10px}
.nlgw-guide p{font:400 15px/1.85 Heebo;color:#37322A;margin:0 0 12px}
.nlgw-tools{margin:30px 0}
.nlgw-tools h2{font-size:1.3rem;margin:0 0 12px}
.nlgw-tools .row{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:12px}
.nlgw-tools a{display:block;background:#fff;border:1px solid #E2DCD0;border-radius:14px;padding:16px 18px;text-decoration:none;color:#1B1A17}
.nlgw-tools a:hover{border-color:#9C7A3C}
.nlgw-tools b{display:block;font:700 14.5px Heebo;margin-bottom:3px}
.nlgw-tools i{font:400 12.5px/1.5 Heebo;color:#8E877A;font-style:normal}
.nlgw-faq{max-width:760px;margin:30px auto}
.nlgw-faq h2{font-size:1.3rem;margin:0 0 12px}
.nlgw-faq details{background:#fff;border:1px solid #E2DCD0;border-radius:12px;padding:14px 18px;margin-bottom:8px}
.nlgw-faq summary{font:700 14px Heebo;cursor:pointer;color:#1B1A17}
.nlgw-faq p{font:400 13.5px/1.75 Heebo;color:#51483A;margin:10px 0 0}
.nlgw-lead{background:#F3EEE3;border:1px solid #E2DCD0;border-radius:22px;padding:26px;margin:30px 0;text-align:center}
.nlgw-lead h2{font-size:1.3rem;margin:0 0 6px}
.nlgw-lead p{font:400 14px Heebo;color:#51483A;margin:0 0 14px}
.nlgw-lead form{display:flex;gap:10px;justify-content:center;flex-wrap:wrap;position:relative}
.nlgw-lead input{background:#fff;border:1px solid #E2DCD0;border-radius:10px;padding:12px 14px;font:400 14px Heebo;min-width:180px}
.nlgw-lead button{background:#C2563A;color:#FAF7F1;border:0;border-radius:12px;padding:12px 26px;font:700 14.5px Heebo;cursor:pointer;box-shadow:0 14px 30px -14px rgba(194,86,58,.55)}
.nlgw-lead .ok{display:block;width:100%;color:#517048;font:700 13.5px Heebo;margin-top:8px}
.nlgw-devcta{background:#14130F;border-radius:22px;padding:34px 26px;margin:34px 0;text-align:center;color:#FAF7F1}
.nlgw-devcta h2{color:#FAF7F1;font-size:1.35rem;margin:0 0 8px}
.nlgw-devcta p{color:#CDC5B4;font:400 14px/1.7 Heebo;max-width:560px;margin:0 auto 16px}
.nlgw-devcta .btn{display:inline-block;background:#C2563A;color:#FAF7F1;border-radius:12px;padding:13px 28px;font:700 14.5px Heebo;text-decoration:none}
.nlgw-honest{text-align:center;font:400 12px/1.7 Heebo;color:#8E877A;max-width:680px;margin:28px auto 0}
@media(max-width:640px){.nlgw-map .mapbox{height:320px}}
</style>
		<?php
	}
}

/* ============================ intl project single ============================ */
add_filter( 'the_content', function ( $content ) {
	if ( ! nadlan_gw_on() || ! is_singular( 'nadlan_intl' ) || ! in_the_loop() || ! is_main_query() ) { return $content; }
	static $done = false;
	if ( $done ) { return $content; }
	$done = true;
	$id = get_the_ID();
	$lang = nadlan_gw_lang();
	$en = ( 'en' === $lang );
	$L = function ( $he, $en_v ) use ( $en ) { return $en ? $en_v : $he; };
	$code = (string) get_post_meta( $id, 'gw_world', true );
	$W = nadlan_gw_worlds();
	$w = isset( $W[ $code ] ) ? $W[ $code ] : null;
	$district = (string) get_post_meta( $id, ( $en ? 'gw_district_en' : 'gw_district' ), true );
	$pf = (string) get_post_meta( $id, 'gw_price_from', true );
	$units = (int) get_post_meta( $id, 'gw_units', true );
	$floors = (int) get_post_meta( $id, 'gw_floors', true );
	$delivery = (string) get_post_meta( $id, 'gw_delivery', true );
	$yield_n = (string) get_post_meta( $id, 'gw_yield', true );
	$lat = (float) get_post_meta( $id, 'gw_lat', true );
	$lng = (float) get_post_meta( $id, 'gw_lng', true );
	$demo = get_post_meta( $id, 'gw_demo', true ) === '1';
	$about_en = (string) get_post_meta( $id, 'gw_about_en', true );
	$glb = (string) get_post_meta( $id, 'gw_glb', true );
	if ( '' === $glb && function_exists( 'nadlan_showroom_engine_base_url' ) ) {
		$glb = nadlan_showroom_engine_base_url() . 'models/flagship-tower.glb';
	}
	$token = function_exists( 'nadlan_mapbox_token' ) ? trim( (string) nadlan_mapbox_token() ) : '';
	nadlan_gw_css();
	ob_start();
	?>
<div class="nlgw nlgw--single" dir="<?php echo $en ? 'ltr' : 'rtl'; ?>">
	<?php if ( $w ) : ?><nav class="nlgw-crumbs"><a href="<?php echo esc_url( home_url( '/global/' . ( $en ? '?lang=en' : '' ) ) ); ?>"><?php echo $L( 'השקעות בחו"ל', 'Global' ); ?></a> / <a href="<?php echo esc_url( home_url( '/global/' . $code . '/' . ( $en ? '?lang=en' : '' ) ) ); ?>"><?php echo esc_html( $en ? $w['name_en'] : $w['name_he'] ); ?></a></nav><?php endif; ?>
	<?php if ( $demo ) : ?><p style="background:#F3EEE3;border:1px solid #D6C189;border-radius:12px;padding:10px 16px;font:600 12.5px Heebo;color:#51483A;display:inline-block"><?php echo $L( 'פרויקט להמחשה על בסיס נתוני שוק אמיתיים - אינו פרויקט ספציפי בשיווק', 'An illustrative project based on real market data - not a specific marketed project' ); ?></p><?php endif; ?>

	<div class="nlgw-facts" style="margin-top:14px">
		<div class="grid">
			<?php if ( $district ) : ?><div class="cell"><i><?php echo $L( 'מיקום', 'Location' ); ?></i><b><?php echo esc_html( $district . ( $w ? ', ' . ( $en ? $w['name_en'] : $w['name_he'] ) : '' ) ); ?></b></div><?php endif; ?>
			<?php if ( $pf && $w ) : ?><div class="cell"><i><?php echo $L( 'מחיר החל מ-', 'From' ); ?></i><b><?php echo esc_html( number_format( (float) $pf ) . ' ' . $w['currency'] ); ?></b></div><?php endif; ?>
			<?php if ( $floors ) : ?><div class="cell"><i><?php echo $L( 'קומות', 'Floors' ); ?></i><b><?php echo (int) $floors; ?></b></div><?php endif; ?>
			<?php if ( $units ) : ?><div class="cell"><i><?php echo $L( 'יח״ד', 'Units' ); ?></i><b><?php echo (int) $units; ?></b></div><?php endif; ?>
			<?php if ( $delivery ) : ?><div class="cell"><i><?php echo $L( 'מסירה', 'Delivery' ); ?></i><b><?php echo esc_html( $delivery ); ?></b></div><?php endif; ?>
			<?php if ( $yield_n ) : ?><div class="cell"><i><?php echo $L( 'הערת תשואה', 'Yield note' ); ?></i><b><?php echo esc_html( $yield_n ); ?></b></div><?php endif; ?>
			<?php $pay = (string) get_post_meta( $id, 'gw_payment', true ); if ( $pay ) : ?><div class="cell"><i><?php echo $L( 'תוכנית תשלומים', 'Payment plan' ); ?></i><b><?php echo esc_html( $pay ); ?></b></div><?php endif; ?>
			<?php $fee = (string) get_post_meta( $id, 'gw_fees', true ); if ( $fee ) : ?><div class="cell"><i><?php echo $L( 'דמי ניהול', 'Service charges' ); ?></i><b><?php echo esc_html( $fee ); ?></b></div><?php endif; ?>
		</div>
	</div>

	<?php
	$apts = nadlan_gw_clean_apartments( json_decode( (string) get_post_meta( $id, 'gw_apartments', true ), true ) );
	if ( $glb ) :
		// hotspot geometry for flagship-tower.glb [118 x 154.5 x 104.7]
		$tw_h = 150.0; $tw_hx = 50.0; $tw_hz = 42.0;
		$fh = $floors > 0 ? min( 3.4, ( $tw_h * 0.88 ) / max( 1, $floors ) ) : 3.05;
		$dirv = array( 'west' => array( -$tw_hx, 0 ), 'east' => array( $tw_hx, 0 ), 'north' => array( 0, $tw_hz ), 'south' => array( 0, -$tw_hz ) );
		$st_lbl = array( 'available' => $L( 'זמינה', 'Available' ), 'reserved' => $L( 'שמורה', 'Reserved' ), 'sold' => $L( 'נמכרה', 'Sold' ) );
	?>
	<?php if ( $apts ) : ?>
	<h2 style="font-family:'Frank Ruhl Libre',serif;font-size:1.35rem;margin:26px 0 4px"><?php echo $L( 'בחרו דירה מתוך הבניין', 'Choose your apartment from inside the building' ); ?></h2>
	<p style="font:400 13px/1.6 Heebo;color:#8E877A;margin:0 0 10px"><?php echo $L( 'לחצו על נקודה במגדל או סננו לפי קומה. מלאי ומחירים להמחשה.', 'Tap a dot on the tower or filter by floor. Inventory and prices are illustrative.' ); ?></p>
	<div id="nlgw-floors" style="display:flex;gap:8px;flex-wrap:wrap;margin:0 0 10px"></div>
	<?php endif; ?>
	<div style="position:relative;height:56vh;min-height:420px;max-height:620px;border-radius:18px;overflow:hidden;background:radial-gradient(ellipse at 50% 30%,#26221733 0%,transparent 65%),#14130F;border:1px solid #2A251B;margin:0 0 14px">
		<model-viewer id="nlgw-mv" src="<?php echo esc_url( $glb ); ?>" camera-controls disable-zoom <?php echo $apts ? '' : 'auto-rotate rotation-per-second="9deg"'; ?>
			style="width:100%;height:100%;direction:ltr;background:transparent;touch-action:pan-y"
			camera-orbit="-25deg 76deg 170m" min-camera-orbit="auto auto 90m" max-camera-orbit="auto auto 260m" exposure="0.95" shadow-intensity="0.6">
			<?php $hi = 0; foreach ( $apts as $a ) :
				$v = $dirv[ $a['dir'] ];
				$perp = ( 0 === $v[0] ) ? array( 1, 0 ) : array( 0, 1 );
				$off = ( $a['pos'] - 1 ) * 13;
				$x = $v[0] + $perp[0] * $off;
				$z = $v[1] + $perp[1] * $off;
				$y = $a['floor'] * $fh + $fh * 0.5;
				$hi++; ?>
			<button class="nlgw-hot nlgw-hot--<?php echo esc_attr( $a['status'] ); ?>" slot="hotspot-<?php echo (int) $hi; ?>"
				data-position="<?php echo esc_attr( round( $x, 1 ) . ' ' . round( $y, 1 ) . ' ' . round( $z, 1 ) ); ?>"
				data-normal="<?php echo esc_attr( ( 0 === $v[1] ? ( $v[0] > 0 ? '1 0 0' : '-1 0 0' ) : ( $v[1] > 0 ? '0 0 1' : '0 0 -1' ) ) ); ?>"
				data-visibility-attribute="visible" data-floor="<?php echo (int) $a['floor']; ?>"
				data-apt="<?php echo esc_attr( wp_json_encode( $a, JSON_UNESCAPED_UNICODE ) ); ?>"><?php echo (int) $a['rooms']; ?></button>
			<?php endforeach; ?>
		</model-viewer>
		<p style="position:absolute;bottom:10px;inset-inline-start:14px;color:#CDC5B4;font:600 11.5px Heebo;margin:0;text-shadow:0 1px 3px rgba(0,0,0,.6)"><?php echo $L( 'הדמיה עקרונית להמחשת הבניין - לא המבנה הסופי', 'A conceptual model for illustration - not the final building' ); ?></p>
		<?php if ( $apts ) : ?>
		<div style="position:absolute;top:12px;inset-inline-start:14px;display:flex;gap:10px;font:600 11px Heebo;color:#E9E2D2;text-shadow:0 1px 3px rgba(0,0,0,.7)">
			<span><i style="display:inline-block;width:10px;height:10px;border-radius:50%;background:#E9D9A8;margin-inline-end:4px"></i><?php echo esc_html( $st_lbl['available'] ); ?></span>
			<span><i style="display:inline-block;width:10px;height:10px;border-radius:50%;background:#A79E8D;margin-inline-end:4px"></i><?php echo esc_html( $st_lbl['reserved'] ); ?></span>
			<span><i style="display:inline-block;width:10px;height:10px;border-radius:50%;background:#51483A;margin-inline-end:4px"></i><?php echo esc_html( $st_lbl['sold'] ); ?></span>
		</div>
		<?php endif; ?>
	</div>
	<style>
	.nlgw-hot{width:26px;height:26px;border-radius:50%;border:2px solid #FAF7F1;color:#14130F;font:800 11px Heebo;cursor:pointer;box-shadow:0 2px 8px rgba(0,0,0,.5)}
	.nlgw-hot--available{background:#E9D9A8}
	.nlgw-hot--reserved{background:#A79E8D;color:#FAF7F1}
	.nlgw-hot--sold{background:#51483A;color:#A79E8D}
	.nlgw-hot[hidden]{display:none}
	.nlgw-fl{border:1px solid #E2DCD0;border-radius:999px;padding:8px 14px;font:600 12.5px Heebo;color:#51483A;background:#fff;cursor:pointer}
	.nlgw-fl.is-on{background:#1B1A17;color:#FAF7F1;border-color:#1B1A17}
	#nlgw-apt-panel{display:none;background:#fff;border:1.5px solid #D6C189;border-radius:16px;padding:20px;margin:0 0 18px}
	#nlgw-apt-panel.is-open{display:block}
	#nlgw-apt-panel h3{font-family:"Frank Ruhl Libre",serif;margin:0 0 8px}
	#nlgw-apt-panel .row{display:flex;gap:16px;flex-wrap:wrap;font:400 13.5px Heebo;color:#51483A;margin:0 0 12px}
	#nlgw-apt-panel .row b{color:#1B1A17}
	#nlgw-apt-panel .acts a{display:inline-block;border-radius:12px;padding:11px 18px;font:700 13.5px Heebo;text-decoration:none;margin-inline-end:8px}
	#nlgw-apt-panel .acts .a1{background:#C2563A;color:#FAF7F1}
	#nlgw-apt-panel .acts .a2{border:1.5px solid #9C7A3C;color:#9C7A3C;background:#fff}
	</style>
	<div id="nlgw-apt-panel"></div>
	<?php if ( $apts ) : ?>
	<script>
	(function(){
		var mv=document.getElementById("nlgw-mv"),panel=document.getElementById("nlgw-apt-panel"),flbar=document.getElementById("nlgw-floors");
		var EN=<?php echo $en ? 'true' : 'false'; ?>;
		var T={fl:EN?"Floor":"קומה",all:EN?"All floors":"כל הקומות",rooms:EN?"rooms":"חדרים",sqm:EN?"sqm":'מ"ר',view:EN?"View":"נוף",price:EN?"Illustrative price":"מחיר להמחשה",st:{available:EN?"Available":"זמינה",reserved:EN?"Reserved":"שמורה",sold:EN?"Sold":"נמכרה"},design:EN?"Design this apartment":"לעצב את הדירה בסטודיו",ask:EN?"Ask about this apartment":"רוצה פרטים על הדירה",cur:<?php echo wp_json_encode( $w ? $w['currency'] : '' ); ?>};
		var hots=[].slice.call(mv.querySelectorAll(".nlgw-hot"));
		var floors=[];hots.forEach(function(h){var f=parseInt(h.dataset.floor,10);if(floors.indexOf(f)<0)floors.push(f)});floors.sort(function(a,b){return a-b});
		function chip(label,f){var b=document.createElement("button");b.type="button";b.className="nlgw-fl"+(f===null?" is-on":"");b.textContent=label;
			b.addEventListener("click",function(){flbar.querySelectorAll(".nlgw-fl").forEach(function(x){x.classList.remove("is-on")});b.classList.add("is-on");
				hots.forEach(function(h){h.hidden=(f!==null&&parseInt(h.dataset.floor,10)!==f)});});
			flbar.appendChild(b);}
		chip(T.all,null);floors.forEach(function(f){chip(T.fl+" "+f,f)});
		hots.forEach(function(h){h.addEventListener("click",function(){
			var a={};try{a=JSON.parse(h.dataset.apt)}catch(e){return}
			var view=EN?(a.view_en||a.view_he):(a.view_he||"");
			panel.innerHTML="<h3>"+(EN?"Apartment ":"דירה ")+a.id.toUpperCase()+" · "+T.fl+" "+a.floor+" <span style='font:700 12px Heebo;color:"+(a.status==="available"?"#517048":a.status==="reserved"?"#9C7A3C":"#C2563A")+"'>"+T.st[a.status]+"</span></h3>"
				+"<div class='row'><span><b>"+a.rooms+"</b> "+T.rooms+"</span><span><b>"+a.sqm+"</b> "+T.sqm+"</span>"+(view?"<span>"+T.view+": <b>"+view+"</b></span>":"")
				+(a.price?"<span>"+T.price+": <b style='color:#C2563A'>"+Number(a.price).toLocaleString()+" "+T.cur+"</b></span>":"")+"</div>"
				+"<div class='acts'><a class='a1' href='#nlgw-lead-form'>"+T.ask+"</a><a class='a2' href='<?php echo esc_url( home_url( '/studio/' ) ); ?>'>"+T.design+"</a></div>";
			panel.classList.add("is-open");
			panel.scrollIntoView({behavior:"smooth",block:"nearest"});
			var nameInput=document.querySelector("#nlgw-lead-form input[name=name]");
			var noteHolder=document.getElementById("nlgw-lead-form");
			if(noteHolder){noteHolder.dataset.apt=a.id;}
		});});
	})();
	</script>
	<?php endif; ?>
	<script type="module" src="https://ajax.googleapis.com/ajax/libs/model-viewer/3.5.0/model-viewer.min.js"></script>
	<?php endif; ?>

	<?php
	$fac = json_decode( (string) get_post_meta( $id, 'gw_facilities', true ), true );
	if ( is_array( $fac ) && $fac ) : ?>
	<h2 style="font-family:'Frank Ruhl Libre',serif;font-size:1.25rem;margin:20px 0 8px"><?php echo $L( 'מתקנים ומה שמסביב', 'Facilities and what is around' ); ?></h2>
	<div style="display:flex;gap:8px;flex-wrap:wrap;margin:0 0 18px">
		<?php foreach ( $fac as $f ) : ?><span style="background:#F3EEE3;border:1px solid #E2DCD0;border-radius:999px;padding:8px 14px;font:600 12.5px Heebo;color:#51483A"><?php echo esc_html( $en ? $f[1] : $f[0] ); ?></span><?php endforeach; ?>
	</div>
	<?php endif; ?>

	<?php if ( $en && $about_en ) : ?><p style="font:400 15px/1.85 Heebo;color:#37322A;max-width:760px"><?php echo esc_html( $about_en ); ?></p><?php endif; ?>

	<?php if ( $token && $lat && $lng ) : ?>
	<div class="nlgw-map"><h2><?php echo $L( 'מה מסביב', 'What is around' ); ?></h2>
		<div id="nlgw-map" class="mapbox" data-token="<?php echo esc_attr( $token ); ?>" data-center="<?php echo esc_attr( $lng . ',' . $lat ); ?>" data-zoom="14"
			data-pins="<?php echo esc_attr( wp_json_encode( array( array( 't' => get_the_title( $id ), 'u' => '#', 'lat' => $lat, 'lng' => $lng ) ), JSON_UNESCAPED_UNICODE ) ); ?>"></div>
	</div>
	<script>
	(function(){
		var m=document.getElementById("nlgw-map");
		if(!m)return;
		var s=document.createElement("script");s.src="https://api.mapbox.com/mapbox-gl-js/v3.5.1/mapbox-gl.js";
		var css=document.createElement("link");css.rel="stylesheet";css.href="https://api.mapbox.com/mapbox-gl-js/v3.5.1/mapbox-gl.css";
		document.head.appendChild(css);
		s.onload=function(){
			mapboxgl.accessToken=m.dataset.token;
			var c=m.dataset.center.split(",");
			var map=new mapboxgl.Map({container:"nlgw-map",style:"mapbox://styles/mapbox/light-v11",center:[parseFloat(c[0]),parseFloat(c[1])],zoom:parseFloat(m.dataset.zoom),cooperativeGestures:true});
			map.addControl(new mapboxgl.NavigationControl());
			var pins=[];try{pins=JSON.parse(m.dataset.pins||"[]")}catch(e){}
			pins.forEach(function(p){
				var el=document.createElement("div");
				el.style.cssText="background:#C2563A;border:2px solid #FAF7F1;width:18px;height:18px;border-radius:50%;box-shadow:0 2px 8px rgba(0,0,0,.35)";
				new mapboxgl.Marker({element:el}).setLngLat([p.lng,p.lat]).addTo(map);
			});
		};
		document.head.appendChild(s);
	})();
	</script>
	<?php endif; ?>

	<section class="nlgw-lead">
		<h2><?php echo $L( 'רוצים לשמוע עוד על השקעה כזו?', 'Want to hear more about an investment like this?' ); ?></h2>
		<form id="nlgw-lead-form">
			<input type="text" name="name" placeholder="<?php echo esc_attr( $L( 'שם מלא', 'Full name' ) ); ?>" required>
			<input type="tel" name="phone" placeholder="<?php echo esc_attr( $L( 'טלפון', 'Phone' ) ); ?>" required>
			<input type="text" name="company" tabindex="-1" autocomplete="off" style="position:absolute;left:-9999px;width:1px;height:1px;opacity:0">
			<button type="submit"><?php echo $L( 'דברו איתי', 'Contact me' ); ?></button>
			<span class="ok" hidden><?php echo $L( 'קיבלנו! נחזור אליכם.', 'Got it! We will be in touch.' ); ?></span>
		</form>
	</section>
	<script>
	(function(){var f=document.getElementById("nlgw-lead-form");
	if(f){f.addEventListener("submit",function(e){e.preventDefault();
		var fd=new FormData(f);
		fetch("<?php echo esc_url( rest_url( 'nadlan/v1/lead' ) ); ?>",{method:"POST",headers:{"Content-Type":"application/json"},
			body:JSON.stringify({name:fd.get("name"),phone:fd.get("phone"),goal:"global-project-<?php echo esc_js( $code ); ?>",message:<?php echo wp_json_encode( get_the_title( $id ) ); ?>,source:"global-project",company:fd.get("company")})})
		.then(function(r){if(r.ok){f.querySelector(".ok").hidden=false;f.querySelector("button").disabled=true;}});
	});}})();
	</script>
</div>
	<?php
	return ob_get_clean() . $content;
}, 7 );

/* noindex the intl single only when it is a demo AND thin; demo singles stay indexable
   (they carry real guide value) - but hreflang/canonical for them: self-canonical. */
add_action( 'wp_head', function () {
	if ( ! is_singular( 'nadlan_intl' ) ) { return; }
	$self = get_permalink();
	echo '<link rel="canonical" href="' . esc_url( $self ) . '">' . "\n";
	echo '<link rel="alternate" hreflang="he" href="' . esc_url( $self ) . '">' . "\n";
	echo '<link rel="alternate" hreflang="en" href="' . esc_url( add_query_arg( 'lang', 'en', $self ) ) . '">' . "\n";
	echo '<link rel="alternate" hreflang="x-default" href="' . esc_url( $self ) . '">' . "\n";
}, 4 );

/* ============================ demo seeder (admin) ============================ */
add_action( 'rest_api_init', function () {
	register_rest_route( 'nadlan/v1', '/gw-seed', array(
		'methods'             => 'POST',
		'permission_callback' => function () { return current_user_can( 'manage_options' ); },
		'callback'            => function () {
			$rows = array(
				array( 'slug' => 'marina-west-tower-dubai', 'title' => 'מגדל מרינה ווסט - דובאי מרינה', 'world' => 'dubai', 'district' => 'דובאי מרינה', 'district_en' => 'Dubai Marina', 'lat' => 25.0805, 'lng' => 55.1403, 'price' => '2400000', 'units' => 280, 'floors' => 42, 'delivery' => '2027', 'yield' => 'אומדן ברוטו 5.5%-7% (ממוצע אזורי, לא הבטחה)',
					'about' => 'מגדל מגורים על טיילת המרינה של דובאי: דירות 1-3 חדרים עם נוף למרינה ולים, בריכת אינפיניטי, חדר כושר וקומת מסחר. תוכנית תשלומים 60/40 לאורך הבנייה, חשבון נאמנות מפוקח DLD. מבוסס על פרופיל פרויקטים אמיתיים באזור; להמחשה.',
					'about_en' => 'A residential tower on the Dubai Marina promenade: 1-3 bedroom apartments with marina and sea views, infinity pool, gym and a retail podium. 60/40 construction-linked payment plan, DLD-supervised escrow. Based on the profile of real projects in the district; for illustration.' ),
				array( 'slug' => 'garden-residence-jvc-dubai', 'title' => 'גארדן רזידנס JVC - דובאי', 'world' => 'dubai', 'district' => 'ג\'ומיירה וילג\' סירקל (JVC)', 'district_en' => 'Jumeirah Village Circle (JVC)', 'lat' => 25.0602, 'lng' => 55.2094, 'price' => '950000', 'units' => 180, 'floors' => 24, 'delivery' => '2027', 'yield' => 'אומדן ברוטו 7%-9% (האזור המוביל בתשואות, לא הבטחה)',
					'about' => 'בניין בוטיק בשכונת JVC, אזור התשואות המוביל של דובאי: סטודיו ודירות 1-2 חדרים סביב חצר גינה, מחירי כניסה מהנמוכים בעיר ותפוסת שכירות גבוהה. מתאים למשקיע תזרים ראשון בדובאי. מבוסס על פרופיל פרויקטים אמיתיים באזור; להמחשה.',
					'about_en' => 'A boutique building in JVC, Dubai\'s leading yield district: studios and 1-2 bedroom units around a garden courtyard, among the lowest entry prices in the city with high rental occupancy. A fit for a first cash-flow investment in Dubai. Based on real project profiles in the district; for illustration.' ),
				array( 'slug' => 'edgewater-bay-residences-miami', 'title' => 'אדג\'ווטר ביי רזידנסס - מיאמי', 'world' => 'miami', 'district' => 'אדג\'ווטר', 'district_en' => 'Edgewater', 'lat' => 25.7959, 'lng' => -80.1878, 'price' => '780000', 'units' => 220, 'floors' => 38, 'delivery' => '2028', 'yield' => 'אומדן ברוטו 5%-6% בשכירות ארוכה (לא הבטחה)',
					'about' => 'מגדל חדש על קו המים של מפרץ ביסקיין בשכונת אדג\'ווטר: דירות 1-3 חדרים עם מרפסות עמוקות מול המים, בריכה על הגג ומועדון דיירים. תשלומים לאורך הבנייה בנאמנות לפי חוק פלורידה. מבוסס על פרופיל פרויקטים אמיתיים באזור; להמחשה.',
					'about_en' => 'A new tower on the Biscayne Bay waterline in Edgewater: 1-3 bedroom residences with deep water-facing balconies, rooftop pool and residents club. Construction-linked payments held in escrow under Florida law. Based on real project profiles in the district; for illustration.' ),
				array( 'slug' => 'brickell-park-tower-miami', 'title' => 'בריקל פארק טאואר - מיאמי', 'world' => 'miami', 'district' => 'בריקל', 'district_en' => 'Brickell', 'lat' => 25.7617, 'lng' => -80.1918, 'price' => '995000', 'units' => 320, 'floors' => 52, 'delivery' => '2028', 'yield' => 'אומדן ברוטו 5%-6.5%; פוטנציאל שכירות קצרה תלוי רישוי (לא הבטחה)',
					'about' => 'מגדל בלב בריקל, הרובע הפיננסי של מיאמי: דירות סטודיו עד 3 חדרים, קומות אמנטיס כפולות, ומרחק הליכה מ-Brickell City Centre. ביקוש שכירות חזק כל השנה מעובדי הפיננסים. מבוסס על פרופיל פרויקטים אמיתיים באזור; להמחשה.',
					'about_en' => 'A tower in the heart of Brickell, Miami\'s financial district: studio to 3-bedroom residences, double amenity floors, walking distance to Brickell City Centre. Strong year-round tenant demand from finance workers. Based on real project profiles in the district; for illustration.' ),
				array( 'slug' => 'lic-skyline-condos-new-york', 'title' => 'LIC סקייליין קונדוס - ניו יורק', 'world' => 'new-york', 'district' => 'לונג איילנד סיטי, קווינס', 'district_en' => 'Long Island City, Queens', 'lat' => 40.7447, 'lng' => -73.9485, 'price' => '890000', 'units' => 190, 'floors' => 28, 'delivery' => '2026', 'yield' => 'אומדן ברוטו 3.5%-4.5% (שוק יציבות, לא תשואה - לא הבטחה)',
					'about' => 'קונדומיניום חדש בלונג איילנד סיטי, תחנת רכבת אחת ממידטאון מנהטן: דירות סטודיו עד 2 חדרים עם נוף לסקייליין, חדר כושר ורופטופ. בניין עם הקלת מס פעילה - בדקו את יתרת השנים. מבוסס על פרופיל פרויקטים אמיתיים באזור; להמחשה.',
					'about_en' => 'A new condominium in Long Island City, one subway stop from Midtown Manhattan: studio to 2-bedroom homes with skyline views, gym and rooftop. The building carries an active tax abatement - verify remaining years. Based on real project profiles in the district; for illustration.' ),
				array( 'slug' => 'brooklyn-point-heights-new-york', 'title' => 'ברוקלין פוינט הייטס - ניו יורק', 'world' => 'new-york', 'district' => 'דאונטאון ברוקלין', 'district_en' => 'Downtown Brooklyn', 'lat' => 40.6935, 'lng' => -73.9866, 'price' => '1150000', 'units' => 260, 'floors' => 45, 'delivery' => '2027', 'yield' => 'אומדן ברוטו 3.5%-4.5% (שוק יציבות, לא תשואה - לא הבטחה)',
					'about' => 'מגדל קונדו בדאונטאון ברוקלין, אזור שהפך למרכז מגורים צעיר ותוסס: דירות 1-3 חדרים, בריכה בקומה גבוהה ונוף למנהטן. גישה לשמונה קווי רכבת תחתית. מבוסס על פרופיל פרויקטים אמיתיים באזור; להמחשה.',
					'about_en' => 'A condo tower in Downtown Brooklyn, now a young and vibrant residential hub: 1-3 bedroom homes, a high-floor pool and Manhattan views. Access to eight subway lines. Based on real project profiles in the district; for illustration.' ),
			);
			$rows = array_merge( $rows, array(
				array( 'slug' => 'canary-riverside-heights-london', 'title' => 'קנרי ריברסייד הייטס - לונדון', 'world' => 'london', 'district' => 'קנרי וורף', 'district_en' => 'Canary Wharf', 'lat' => 51.5054, 'lng' => -0.0235, 'price' => '585000', 'units' => 240, 'floors' => 40, 'delivery' => '2027', 'yield' => 'אומדן ברוטו 4.5%-5.5% (ממוצע אזורי, לא הבטחה)', 'payment' => '10% בחתימה, 10% אחרי שנה, יתרה במסירה', 'fees' => 'כ-5 ליש"ט לרגל לשנה',
					'about' => 'מגדל מגורים על קו המים בקנרי וורף, רובע הפיננסים המזרחי של לונדון: דירות 1-3 חדרי שינה עם נוף לנהר ולסקייליין, חדר כושר, לאונג\' דיירים וקומת עבודה משותפת. ליסהולד 999 שנה, דמי קרקע אפס. מבוסס על פרופיל פרויקטים אמיתיים באזור; להמחשה.',
					'about_en' => 'A waterline residential tower in Canary Wharf, London\'s eastern financial district: 1-3 bed apartments with river and skyline views, gym, residents lounge and a co-working floor. 999-year lease, zero ground rent. Based on real project profiles in the district; for illustration.',
					'fac' => array( array( 'לאונג\' דיירים', 'Residents lounge' ), array( 'חדר כושר', 'Gym' ), array( 'קומת עבודה משותפת', 'Co-working floor' ), array( 'שומר 24/7', '24/7 concierge' ), array( 'תחנת Jubilee במרחק 6 דקות', 'Jubilee line 6 min away' ), array( 'טיילת נהר', 'River promenade' ) ) ),
				array( 'slug' => 'stratford-park-gate-london', 'title' => 'סטרטפורד פארק גייט - לונדון', 'world' => 'london', 'district' => 'סטרטפורד', 'district_en' => 'Stratford', 'lat' => 51.5416, 'lng' => -0.0042, 'price' => '495000', 'units' => 320, 'floors' => 30, 'delivery' => '2028', 'yield' => 'אומדן ברוטו 5%-5.5% (אזור התחדשות, לא הבטחה)', 'payment' => '10% בחתימה, יתרה במסירה', 'fees' => 'כ-4 ליש"ט לרגל לשנה',
					'about' => 'פרויקט מגורים מול הפארק האולימפי בסטרטפורד, מוקד ההתחדשות הגדול של מזרח לונדון: דירות 1-2 חדרי שינה במחירי הכניסה הנוחים בעיר, תחבורה מכל הכיוונים (Elizabeth Line, Jubilee, Overground) וקמפוסים של אוניברסיטאות בהליכה. מבוסס על פרופיל פרויקטים אמיתיים באזור; להמחשה.',
					'about_en' => 'A residential scheme facing the Olympic Park in Stratford, East London\'s biggest regeneration hub: 1-2 beds at the city\'s friendliest entry prices, transport in every direction (Elizabeth Line, Jubilee, Overground) and university campuses on foot. Based on real project profiles in the district; for illustration.',
					'fac' => array( array( 'מול הפארק האולימפי', 'Facing the Olympic Park' ), array( 'Elizabeth Line בהליכה', 'Elizabeth Line on foot' ), array( 'גינת גג', 'Roof garden' ), array( 'חדר כושר', 'Gym' ), array( 'קניון Westfield צמוד', 'Westfield mall adjacent' ) ) ),
				array( 'slug' => 'koukaki-athens-residence', 'title' => 'רזידנס קוקאקי - אתונה', 'world' => 'greece', 'district' => 'קוקאקי, אתונה', 'district_en' => 'Koukaki, Athens', 'lat' => 37.9634, 'lng' => 23.7239, 'price' => '295000', 'units' => 36, 'floors' => 7, 'delivery' => '2027', 'yield' => 'אומדן ברוטו 4.5%-6% (מרכז אתונה, לא הבטחה)', 'payment' => '30% בחתימה, יתרה באבני דרך', 'fees' => 'דמי בניין נמוכים יחסית',
					'about' => 'בניין בוטיק בשכונת קוקאקי שלרגלי האקרופוליס - השכונה המבוקשת ביותר באתונה לשכירות תיירותית ולצעירים: דירות 1-3 חדרים עם מרפסות, גג משותף עם נוף לאקרופוליס, והליכה לתחנת מטרו. מתאים גם למסלול ויזת זהב בצירוף נכס נוסף. מבוסס על פרופיל פרויקטים אמיתיים באזור; להמחשה.',
					'about_en' => 'A boutique building in Koukaki at the foot of the Acropolis - Athens\' most sought-after neighborhood for tourist lets and young renters: 1-3 room flats with balconies, a shared rooftop with Acropolis views, and a metro stop on foot. Golden-visa compatible combined with an additional asset. Based on real project profiles in the district; for illustration.',
					'fac' => array( array( 'גג משותף עם נוף לאקרופוליס', 'Rooftop with Acropolis view' ), array( 'מטרו בהליכה', 'Metro on foot' ), array( 'מרפסות לכל דירה', 'Balconies throughout' ), array( 'שכונת הקפה של אתונה', 'Athens\' cafe quarter' ) ) ),
				array( 'slug' => 'glyfada-coast-suites-athens', 'title' => 'גליפדה קוסט סוויטס - אתונה', 'world' => 'greece', 'district' => 'גליפדה, הריביירה האתונאית', 'district_en' => 'Glyfada, Athens Riviera', 'lat' => 37.8622, 'lng' => 23.7544, 'price' => '520000', 'units' => 48, 'floors' => 6, 'delivery' => '2027', 'yield' => 'אומדן ברוטו 4%-5.5%; שכירות קצרה עונתית גבוהה יותר (לא הבטחה)', 'payment' => '30/70 לאורך הבנייה', 'fees' => 'דמי בניין + אחזקת בריכה',
					'about' => 'פרויקט יוקרה בגליפדה שעל הריביירה האתונאית, 300 מטר מהחוף: דירות 2-4 חדרים עם מרפסות שמש עמוקות, בריכה משותפת וחניון. האזור המועדף על משפחות ישראליות ומשקיעי ויזת זהב. מבוסס על פרופיל פרויקטים אמיתיים באזור; להמחשה.',
					'about_en' => 'A premium scheme in Glyfada on the Athens Riviera, 300 meters from the beach: 2-4 room homes with deep sun balconies, a shared pool and parking. The area of choice for Israeli families and golden-visa investors. Based on real project profiles in the district; for illustration.',
					'fac' => array( array( 'חוף במרחק 300 מטר', 'Beach 300m away' ), array( 'בריכה משותפת', 'Shared pool' ), array( 'חניון תת קרקעי', 'Underground parking' ), array( 'מרינה וטיילת', 'Marina and promenade' ), array( 'בתי ספר בינלאומיים', 'International schools' ) ) ),
				array( 'slug' => 'sukhumvit-sky-residence-bangkok', 'title' => 'סוקומווית סקיי רזידנס - בנגקוק', 'world' => 'thailand', 'district' => 'סוקומווית, בנגקוק', 'district_en' => 'Sukhumvit, Bangkok', 'lat' => 13.7308, 'lng' => 100.5697, 'price' => '4900000', 'units' => 420, 'floors' => 45, 'delivery' => '2027', 'yield' => 'אומדן ברוטו 5%-6.5% (מרכז בנגקוק, לא הבטחה)', 'payment' => '25% לאורך הבנייה, 75% במסירה', 'fees' => 'כ-60-80 באט למ"ר לחודש',
					'about' => 'מגדל קונדו על ציר סוקומווית, במרחק הליכה מתחנת BTS: סטודיו ודירות 1-2 חדרים, בריכת אינפיניטי בקומה 40, סקיי לאונג\' וחדר כושר. במכסת הזרים - רישום Freehold מלא על שם הקונה. מבוסס על פרופיל פרויקטים אמיתיים באזור; להמחשה.',
					'about_en' => 'A condo tower on the Sukhumvit corridor, walking distance to a BTS station: studios and 1-2 bed units, a 40th-floor infinity pool, sky lounge and gym. Within the foreign quota - full freehold registration in the buyer\'s name. Based on real project profiles in the district; for illustration.',
					'fac' => array( array( 'בריכת אינפיניטי בקומה 40', '40th floor infinity pool' ), array( 'תחנת BTS בהליכה', 'BTS station on foot' ), array( 'סקיי לאונג\'', 'Sky lounge' ), array( 'חדר כושר', 'Gym' ), array( 'שומר 24/7', '24/7 security' ) ) ),
				array( 'slug' => 'bang-tao-garden-villas-phuket', 'title' => 'באנג טאו גארדן קונדוס - פוקט', 'world' => 'thailand', 'district' => 'באנג טאו, פוקט', 'district_en' => 'Bang Tao, Phuket', 'lat' => 7.9936, 'lng' => 98.2933, 'price' => '3600000', 'units' => 96, 'floors' => 7, 'delivery' => '2027', 'yield' => 'תוכנית ניהול מלונאי; תשואה עונתית - קראו את החוזה (לא הבטחה)', 'payment' => '30/70 לאורך הבנייה', 'fees' => 'דמי ניהול מלונאי לפי חוזה',
					'about' => 'קומפלקס קונדו נמוך בשכונת באנג טאו שבחוף המערבי של פוקט, 700 מטר מהים: דירות סטודיו עד 2 חדרים סביב בריכות שחייה, בניהול מלונאי עם תוכנית השכרה. Freehold במכסת הזרים. מבוסס על פרופיל פרויקטים אמיתיים באזור; להמחשה.',
					'about_en' => 'A low-rise condo complex in Bang Tao on Phuket\'s west coast, 700m from the sea: studio to 2-bed units around swimming pools, hotel-managed with a rental program. Freehold within the foreign quota. Based on real project profiles in the district; for illustration.',
					'fac' => array( array( 'חוף באנג טאו 700 מטר', 'Bang Tao beach 700m' ), array( 'שלוש בריכות', 'Three pools' ), array( 'ניהול מלונאי', 'Hotel management' ), array( 'מסעדות וביץ\' קלאבים', 'Restaurants and beach clubs' ) ) ),
				array( 'slug' => 'nolo-district-residence-milan', 'title' => 'נולו דיסטריקט רזידנס - מילאנו', 'world' => 'italy', 'district' => 'נולו, מילאנו', 'district_en' => 'NoLo, Milan', 'lat' => 45.4949, 'lng' => 9.2183, 'price' => '310000', 'units' => 58, 'floors' => 9, 'delivery' => '2027', 'yield' => 'אומדן ברוטו 4.5%-6% (אזור מתחדש, לא הבטחה)', 'payment' => 'הסכם מוקדם 15%, יתרה ברוגיטו', 'fees' => 'ועד בית כ-1,500-2,500 אירו לשנה',
					'about' => 'פרויקט מגורים בשכונת נולו המתחדשת של מילאנו, האזור שהפך למוקד הצעירים והסטודיו: דירות 1-3 חדרים עם מרפסות, חצר פנימית ירוקה וחניית אופניים, ליד מטרו קו 1. ביקוש שכירות חזק מסטודנטים ואנשי הייטק. מבוסס על פרופיל פרויקטים אמיתיים באזור; להמחשה.',
					'about_en' => 'A residential scheme in Milan\'s regenerating NoLo district, the new hub for young renters and studios: 1-3 room flats with balconies, a green inner courtyard and bike parking, near Metro line 1. Strong tenant demand from students and tech workers. Based on real project profiles in the district; for illustration.',
					'fac' => array( array( 'מטרו קו 1 בהליכה', 'Metro line 1 on foot' ), array( 'חצר פנימית ירוקה', 'Green inner courtyard' ), array( 'חניית אופניים', 'Bike parking' ), array( 'שכונת הגלריות והקפה', 'The gallery-and-cafe quarter' ) ) ),
				array( 'slug' => 'porta-romana-garden-milan', 'title' => 'פורטה רומאנה גארדן - מילאנו', 'world' => 'italy', 'district' => 'פורטה רומאנה, מילאנו', 'district_en' => 'Porta Romana, Milan', 'lat' => 45.4494, 'lng' => 9.2042, 'price' => '440000', 'units' => 72, 'floors' => 11, 'delivery' => '2028', 'yield' => 'אומדן ברוטו 4%-5% (אזור הכפר האולימפי, לא הבטחה)', 'payment' => 'הסכם מוקדם 20%, יתרה ברוגיטו', 'fees' => 'ועד בית כ-2,000-3,000 אירו לשנה',
					'about' => 'פרויקט חדש ליד מתחם הכפר האולימפי של פורטה רומאנה - פרויקט ההתחדשות הגדול של דרום מילאנו: דירות 2-3 חדרים עם לוג\'יות, גינה משותפת וקומת מסחר. אזור שמושך השקעות ענק לקראת העשור הקרוב. מבוסס על פרופיל פרויקטים אמיתיים באזור; להמחשה.',
					'about_en' => 'A new scheme near the Porta Romana Olympic Village compound - southern Milan\'s biggest regeneration play: 2-3 room homes with loggias, a shared garden and a retail floor. A district drawing massive investment into the coming decade. Based on real project profiles in the district; for illustration.',
					'fac' => array( array( 'מתחם הכפר האולימפי', 'The Olympic Village compound' ), array( 'גינה משותפת', 'Shared garden' ), array( 'לוג\'יות שמש', 'Sun loggias' ), array( 'קומת מסחר', 'Retail floor' ), array( 'מטרו קו 3', 'Metro line 3' ) ) ),
			) );
			// generated inventory: honest, price-scaled apartments per project
			$gen_apts = function ( $r ) {
				$floors = (int) $r['floors'];
				$base = (float) $r['price'];
				$views = array(
					'west' => array( 'he' => 'מערב', 'en' => 'West' ), 'east' => array( 'he' => 'מזרח', 'en' => 'East' ),
					'north' => array( 'he' => 'צפון', 'en' => 'North' ), 'south' => array( 'he' => 'דרום', 'en' => 'South' ),
				);
				$dirs = array( 'west', 'south', 'east', 'north' );
				$steps = max( 4, min( 6, (int) floor( $floors / 4 ) ) );
				$apts = array();
				$i = 0;
				for ( $s = 1; $s <= $steps; $s++ ) {
					$floor = max( 2, (int) round( $floors * $s / ( $steps + 1 ) ) );
					for ( $u = 0; $u < 2; $u++ ) {
						$i++;
						$rooms = 1 + ( ( $s + $u ) % 3 );
						$sqm = 48 + $rooms * 26 + ( $u * 6 );
						$price = round( $base * ( 1 + 0.22 * ( $rooms - 1 ) + 0.005 * $floor ), -3 );
						$status = ( 0 === $i % 5 ) ? 'sold' : ( ( 0 === $i % 3 ) ? 'reserved' : 'available' );
						$dir = $dirs[ ( $s + $u ) % 4 ];
						$apts[] = array(
							'id' => 'u' . $floor . chr( 97 + $u ), 'floor' => $floor, 'pos' => ( $i % 3 ),
							'dir' => $dir, 'rooms' => $rooms, 'sqm' => $sqm, 'price' => $price, 'status' => $status,
							'view_he' => $views[ $dir ]['he'], 'view_en' => $views[ $dir ]['en'],
						);
					}
				}
				return $apts;
			};
			$default_pay = array( 'dubai' => '60/40 לאורך הבנייה', 'miami' => '20% בחתימה, אבני דרך, יתרה בסגירה', 'new-york' => '10%-20% מקדמה בנאמנות, יתרה בסגירה' );
			$default_fac = array(
				'dubai' => array( array( 'בריכת אינפיניטי', 'Infinity pool' ), array( 'חדר כושר', 'Gym' ), array( 'קומת מסחר', 'Retail podium' ), array( 'שומר 24/7', '24/7 security' ) ),
				'miami' => array( array( 'בריכה על הגג', 'Rooftop pool' ), array( 'מועדון דיירים', 'Residents club' ), array( 'חדר כושר', 'Gym' ), array( 'שירותי קונסיירז', 'Concierge' ) ),
				'new-york' => array( array( 'רופטופ עם נוף', 'View rooftop' ), array( 'חדר כושר', 'Gym' ), array( 'לובי 24/7', '24/7 lobby' ), array( 'חדר אופניים', 'Bike room' ) ),
			);
			$refresh = '1' === (string) ( $_GET['refresh'] ?? '' ); // phpcs:ignore
			$made = array();
			foreach ( $rows as $r ) {
				$exists = get_page_by_path( $r['slug'], OBJECT, 'nadlan_intl' );
				if ( $exists && ! $refresh ) { $made[] = array( 'slug' => $r['slug'], 'id' => $exists->ID, 'existed' => true ); continue; }
				if ( $exists ) {
					$pid = $exists->ID;
				} else {
					$pid = wp_insert_post( array(
						'post_type' => 'nadlan_intl', 'post_status' => 'publish',
						'post_name' => $r['slug'], 'post_title' => $r['title'],
						'post_content' => '<p>' . esc_html( $r['about'] ) . '</p>',
					), true );
					if ( is_wp_error( $pid ) ) { return $pid; }
				}
				update_post_meta( $pid, 'gw_world', $r['world'] );
				update_post_meta( $pid, 'gw_district', $r['district'] );
				update_post_meta( $pid, 'gw_district_en', $r['district_en'] );
				update_post_meta( $pid, 'gw_lat', $r['lat'] );
				update_post_meta( $pid, 'gw_lng', $r['lng'] );
				update_post_meta( $pid, 'gw_price_from', $r['price'] );
				update_post_meta( $pid, 'gw_units', $r['units'] );
				update_post_meta( $pid, 'gw_floors', $r['floors'] );
				update_post_meta( $pid, 'gw_delivery', $r['delivery'] );
				update_post_meta( $pid, 'gw_yield', $r['yield'] );
				update_post_meta( $pid, 'gw_about_en', $r['about_en'] );
				update_post_meta( $pid, 'gw_payment', isset( $r['payment'] ) ? $r['payment'] : ( $default_pay[ $r['world'] ] ?? '' ) );
				if ( isset( $r['fees'] ) ) { update_post_meta( $pid, 'gw_fees', $r['fees'] ); }
				$fac = isset( $r['fac'] ) ? $r['fac'] : ( $default_fac[ $r['world'] ] ?? array() );
				update_post_meta( $pid, 'gw_facilities', wp_json_encode( $fac, JSON_UNESCAPED_UNICODE ) );
				update_post_meta( $pid, 'gw_apartments', wp_json_encode( nadlan_gw_clean_apartments( $gen_apts( $r ) ), JSON_UNESCAPED_UNICODE ) );
				update_post_meta( $pid, 'gw_demo', '1' );
				$made[] = array( 'slug' => $r['slug'], 'id' => $pid, 'existed' => (bool) $exists );
			}
			flush_rewrite_rules( false );
			return array( 'ok' => true, 'projects' => $made );
		},
	) );
} );

/* ============================ healthcheck ============================ */
add_filter( 'nadlan_config_healthcheck', function ( $out ) {
	$n = wp_count_posts( 'nadlan_intl' );
	$out['global_worlds'] = array(
		'on'     => nadlan_gw_on(),
		'worlds' => array_keys( nadlan_gw_worlds() ),
		'projects' => isset( $n->publish ) ? (int) $n->publish : 0,
	);
	return $out;
} );
