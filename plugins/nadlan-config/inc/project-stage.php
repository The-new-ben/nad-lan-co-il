<?php
/**
 * ProjectStage: the top of a project page (owner, 24.9.2026: "Rainbow... what happens when you click a floor... the view
 * from outside... when you click a floor you see the beam on the map below, which way it faces, relative to the sea, the
 * city, the buildings... every page is a whole information system around the project"; later the same evening: "put
 * Rainbow inside the page... Meital at the side with a square you can click, and an empty square for brokers: 'do you
 * want to appear here?'... plans are very important"). From the design system (Claude Design artifact
 * L9Nqz7Viv7K3MYeZrBc9s8 version 10: ProjectStage, BrokerSquare, BrokerSlot).
 *
 *  - The page's one h1 (inc/showroom-engine.php prints it for machines only) becomes the visible title, with the developer
 *    and the quarter under it, right before the lead paragraph.
 *  - The building is in the first fold (design system version 14, 25.9.2026): one grid, where on a wide screen the text
 *    column (title, lead, the two buttons), the project's stage and the side rail stand side by side, and on a phone the
 *    stage comes right after the title and the buttons. The stage is a three.js scene of the project's buildings
 *    (assets/project-stage/<dir>/stage.js): the visitor picks a floor, then a point on that floor's ring, a direction. The
 *    rail holds a professional's square (an advertisement, labelled) and the empty square that invites professionals.
 *  - Then six sourced facts and where the project stands (the older progress band and the card's facts table are not
 *    printed on these pages: one of each).
 *  - Under the stage, side by side: the view from there (assets/project-stage/bridge.js: satellite with 3D buildings, the
 *    camera at the floor's estimated height) and the area map (#nlpjx-map), moved up from the bottom of the page; a beam
 *    on it turns to the chosen direction, so the direction is read against the sea, the city and the buildings. The
 *    beam is the engine's wedge drawn again from outside: engine.js is never touched, and nothing is drawn when the
 *    engine is on the page, so a page never has two beams.
 *  - A direction is said by what lies that way (the project's own sectors below, from the map), never in degrees.
 *  - "לקבלת תוכניות ומחירים" opens the site's WhatsApp with the project, the floor and the direction.
 * Everything is composed on the finished HTML (an outer output buffer, so it runs after catalog-plus has put the price
 * and surroundings blocks under the lead; they now follow the stage). It fails open: a missing anchor leaves the page as
 * it was. Nothing about apartments, prices or availability comes from the stage; the view is labelled an estimate. Only
 * in review mode (the owner's 30.8 order); a showroom page keeps its engine. Off switch: option nadlan_project_stage = '0'.
 */
if ( ! defined( 'ABSPATH' ) ) { exit; }

if ( ! function_exists( 'nadlan_ps_config' ) ) {
	/**
	 * slug => the stage for that project. bearing_offset aligns the scene's north with the real site. sectors: what lies
	 * in each direction from the building, true bearings clockwise from north, measured on the map from the building's
	 * coordinates (Rainbow 32.1032, 34.7844: the shore about 0.9 km west, Tel Baruch beach north, Tel Aviv University at
	 * 59°, Yarkon Park about 100°, the Azrieli towers at 167°, the Old North about 197°, the port at 243°).
	 */
	function nadlan_ps_config() {
		return array(
			'rainbow-tel-aviv' => array(
				'dir'            => 'rainbow',
				'mount'          => 'mountRainbowStage',
				'slice_note'     => 'בקומה 3 עד 5 דירות, לפי היזם (ביזפורטל, 7.2023).', // FloorSlice v87
				'basket_hint'    => 'לעזרה: המחיר הממוצע בדירות שנמכרו בפרויקט עד 3.2026 היה כ-81,800 ₪ למ״ר, לפי דוחות היזם. המחיר של דירה מסוימת מהנציג.', // BasketOne v86: shown as a hint, never multiplied into a price
				'bearing_offset' => 0,
				'name'           => 'ריינבו תל אביב',
				'name_en'        => 'Rainbow Tel Aviv',
				'developer'      => 'ישראל קנדה',
				'place'          => 'רובע שדה דב, צפון תל אביב',
				'rail'           => array( 7833 ),
				// the tower, not the lot's centre: lot 111's official outline (Tel Aviv plans layer, plan תע"א/תמ"ל3001(111),
				// 8,695 m², long north-south, turned 10° east) and the design plan's "north-east corner" put it about 46 m NNE of
				// the centre. The view from a floor and the beam start here.
				// ProjectFacts: six quick facts, each with its source (docs/research/2026-09-24-rainbow-run/rainbow-facts.md)
				'facts'          => array(
					array( 'מיקום', 'רובע שדה דב', 'צפון תל אביב, כ-700 מ׳ מהים' ),
					array( 'בניינים', 'מגדל 39 קומות', 'ובנייני בוטיק בני 9 קומות' ),
					// 275 of 459 sold by the developer's H1 2026 report (Globes 27.8.2026, docs/research/.../deep-research-rainbow.md)
					array( 'דירות', '459', '275 מהן נמכרו עד 6.2026, לפי דוחות היזם' ),
					array( 'תמהיל', '2 עד 5 חדרים', 'ופנטהאוזים, לפי השיווק' ),
					array( 'מחיר ממוצע', 'כ-81,800 ₪ למ״ר', 'דוחות היזם, עד 3.2026' ),
					array( 'מצב', 'בבנייה', 'אכלוס צפוי ב-2030' ),
				),
				// ProjectProgress: done, now, next (the design plan: decided 10.5.2023 subject to conditions, approved 17.1.2024 per
				// the municipality; the full permit 10.2025; occupancy per the project site, the last phase about mid 2030 per
				// Ashtrom's execution contract)
				'progress'       => array(
					array( 'תכנון', '1.2024', 'done' ),
					array( 'היתר בנייה', '10.2025', 'done' ),
					array( 'בבנייה', 'עכשיו', 'now' ),
					array( 'אכלוס', 'צפוי ב-2030', 'next' ),
				),
				// example apartments (the owner, 25.9.2026: "דירות לדוגמה עם כיוון, ועם תווית ברורה שהן לדוגמה"): one per side of
				// each tower floor, four in all, within the developer's "3 to 5 apartments per floor" (Bizportal 19.7.2023)
				'units'          => array( array( 'n', 0 ), array( 'e', 90 ), array( 's', 180 ), array( 'w', 270 ) ),
				// ProjectFilm v80 (5.10.2026, Ben: "everything is approved"): the film loop's v1 film, Hebrew here and English on the
				// language pages (film_en); 720p web copies, byte-checked (docs/qa/film-v1-projects/media.json)
				'film'           => array(
					'wide' => 'https://nad-lan.co.il/wp-content/uploads/2026/10/rainbow-tel-aviv-film-v1-he-16x9-1.mp4', 'tall' => 'https://nad-lan.co.il/wp-content/uploads/2026/10/rainbow-tel-aviv-film-v1-he-9x16-1.mp4',
					'poster_wide' => 'https://nad-lan.co.il/wp-content/uploads/2026/10/rainbow-tel-aviv-film-v1-he-16x9-poster.jpg', 'poster_tall' => 'https://nad-lan.co.il/wp-content/uploads/2026/10/rainbow-tel-aviv-film-v1-he-9x16-poster.jpg',
					'secs' => 54, 'date' => '2026-10-05', 'date_he' => '5.10.2026', 'lang' => 'he',
					'desc' => 'סרטון של 54 שניות על Rainbow תל אביב ברובע שדה דב: המיקום, המגדל ובנייני הבוטיק, הדירות, מועדון הדיירים, שלב הבנייה והנוף המשוער מהקומות. הדמיה להמחשה.',
				),
				'film_en'        => array(
					'wide' => 'https://nad-lan.co.il/wp-content/uploads/2026/10/rainbow-tel-aviv-film-v1-en-16x9-1.mp4', 'tall' => 'https://nad-lan.co.il/wp-content/uploads/2026/10/rainbow-tel-aviv-film-v1-en-9x16-1.mp4',
					'poster_wide' => 'https://nad-lan.co.il/wp-content/uploads/2026/10/rainbow-tel-aviv-film-v1-en-16x9-poster.jpg', 'poster_tall' => 'https://nad-lan.co.il/wp-content/uploads/2026/10/rainbow-tel-aviv-film-v1-en-9x16-poster.jpg',
					'secs' => 54, 'date' => '2026-10-05', 'date_he' => '5.10.2026', 'lang' => 'en', 'name' => 'Rainbow Tel Aviv',
					'desc' => 'A 54-second film on Rainbow Tel Aviv in the Sde Dov quarter: the location, the tower and the boutique buildings, the apartments, the residents\' club, the construction stage and the estimated view from the floors. Illustrative visualisation.',
				),
				// the floor card's line where no sold apartment is known: what the developer said about that height (Bizportal
				// 19.7.2023: two-room apartments "עד קומה 25 בערך"), and above it the project's range
				'low_up_to'      => 25,
				'low_note'       => 'בקומות עד 25 בערך יש גם דירות 2 חדרים, לפי היזם',
				'high_note'      => 'בפרויקט דירות 2 עד 5 חדרים, לפי פרסומי השיווק',
				// ProjectDeals: the sold apartments the sources tie to a floor (checked 25.9.2026 against the articles; the Tax
				// Authority's data as Globes published it on 29.11.2023; Bizportal 19.7.2023; Globes 9.7.2024). No buyer is named.
				// n = the tower floor the stage can open (0 = not a tower floor, or the floor was not published)
				'deals'          => array(
					array( 'floor' => 'אחת הגבוהות', 'n' => 0, 'bld' => 'מגדל', 'apt' => 'כמה דירות באותה קומה, לאיחוד לכ-550 מ״ר', 'price' => 'כ-50 מיליון ₪', 'psqm' => 'לא פורסם', 'date' => '7.2024', 'src' => 'גלובס', 'url' => 'https://www.globes.co.il/news/article.aspx?did=1001483864', 'via' => '' ),
					array( 'floor' => '13', 'n' => 13, 'bld' => 'מגדל', 'apt' => '3 חדרים · 98 מ״ר', 'price' => 'יותר מ-8 מיליון ₪', 'psqm' => 'מעל 81,600 ₪', 'date' => '9.2023', 'src' => 'גלובס', 'url' => 'https://www.globes.co.il/news/article.aspx?did=1001463064', 'via' => 'לפי רשות המסים', 'note' => 'בקומה הזו נמכרה דירת 3 חדרים, 98 מ״ר, ביותר מ-8 מיליון ₪ (9.2023)' ),
					array( 'floor' => '8', 'n' => 0, 'bld' => 'בניין בוטיק, מתוך 9', 'apt' => '6 חדרים · 182 מ״ר', 'price' => 'כ-21.7 מיליון ₪', 'psqm' => 'כ-119,200 ₪', 'date' => '9.2023', 'src' => 'גלובס', 'url' => 'https://www.globes.co.il/news/article.aspx?did=1001463064', 'via' => 'לפי רשות המסים' ),
					array( 'floor' => '8', 'n' => 0, 'bld' => 'בניין בוטיק, מתוך 9', 'apt' => '6 חדרים · 202 מ״ר', 'price' => '20 מיליון ₪', 'psqm' => 'כ-99,000 ₪', 'date' => '3.2023', 'src' => 'גלובס', 'url' => 'https://www.globes.co.il/news/article.aspx?did=1001463064', 'via' => 'לפי רשות המסים' ),
					array( 'floor' => '7', 'n' => 0, 'bld' => 'הבניין לא צוין', 'apt' => '5 חדרים · 133 מ״ר ומרפסת 17 מ״ר, עם נוף לים', 'price' => '10.18 מיליון ₪', 'psqm' => 'כ-76,500 ₪', 'date' => '7.2023', 'src' => 'ביזפורטל', 'url' => 'https://www.bizportal.co.il/realestates/news/article/816625', 'via' => '' ),
					array( 'floor' => '6', 'n' => 6, 'bld' => 'מגדל', 'apt' => '3 חדרים · 60 מ״ר, ללא חניה', 'price' => '4 מיליון ₪', 'psqm' => 'כ-66,700 ₪', 'date' => '10.2023', 'src' => 'גלובס', 'url' => 'https://www.globes.co.il/news/article.aspx?did=1001463064', 'via' => 'לפי רשות המסים', 'note' => 'בקומה הזו נמכרה דירת 3 חדרים, 60 מ״ר, ב-4 מיליון ₪ (10.2023)' ),
					array( 'floor' => '4', 'n' => 4, 'bld' => 'מגדל', 'apt' => 'חדר אחד · 32 מ״ר', 'price' => '3.1 מיליון ₪', 'psqm' => 'כ-96,900 ₪', 'date' => '7.2023', 'src' => 'גלובס', 'url' => 'https://www.globes.co.il/news/article.aspx?did=1001463064', 'via' => 'לפי רשות המסים', 'note' => 'בקומה הזו נמכרה דירת חדר, 32 מ״ר, ב-3.1 מיליון ₪ (7.2023)' ),
				),
				'deals_sum'      => array(
					array( '275 מתוך 459', 'דירות נמכרו עד 6.2026, לפי דוחות היזם' ),
					array( 'כ-81,800 ₪ למ״ר', 'המחיר הממוצע בדירות שנמכרו עד 3.2026, לפי דוחות היזם' ),
				),
				'tower_lat'      => 32.10354,
				'tower_lng'      => 34.78466,
				'sectors'        => array(
					array( 230, 345, 'לכיוון הים' ),
					array( 345, 30, 'לכיוון תל ברוך והרצליה' ),
					array( 30, 105, 'לכיוון רמת אביב והאוניברסיטה' ),
					array( 105, 150, 'לכיוון פארק הירקון' ),
					array( 150, 195, 'לכיוון מגדלי העיר' ),
					array( 195, 230, 'לכיוון הצפון הישן' ),
				),
			),
			// StageDuo v81 (28.9.2026): DUO on its official lot (docs/research/2026-09-28-stages/stage-geometry.md, section 3; the
			// proposal docs/research/2026-09-28-stages/duo-config-proposal.php.txt). The H1 carries the searched names (GSC 90 days:
			// "duo tel aviv", "duo תל אביב", "דואו", "מגדלי duo"); Ibn Gabirol and Arlozorov are in the line under it.
			'duo-tel-aviv' => array(
				// ProjectFilm v80 (5.10.2026, Ben: "everything is approved"): the film loop's v1 film, Hebrew here and English on the
				// language pages (film_en); 720p web copies, byte-checked (docs/qa/film-v1-projects/media.json)
				'film'           => array(
					'wide' => 'https://nad-lan.co.il/wp-content/uploads/2026/10/duo-tel-aviv-film-v1-he-16x9-1.mp4', 'tall' => 'https://nad-lan.co.il/wp-content/uploads/2026/10/duo-tel-aviv-film-v1-he-9x16-1.mp4',
					'poster_wide' => 'https://nad-lan.co.il/wp-content/uploads/2026/10/duo-tel-aviv-film-v1-he-16x9-poster.jpg', 'poster_tall' => 'https://nad-lan.co.il/wp-content/uploads/2026/10/duo-tel-aviv-film-v1-he-9x16-poster.jpg',
					'secs' => 54, 'date' => '2026-10-05', 'date_he' => '5.10.2026', 'lang' => 'he',
					'desc' => 'סרטון של 54 שניות על DUO תל אביב במתחם סומייל: המיקום, שני המגדלים, הדירות, המסחר, שלב הבנייה לפי דוח החברה והנוף המשוער מהקומות. הדמיה להמחשה.',
				),
				'film_en'        => array(
					'wide' => 'https://nad-lan.co.il/wp-content/uploads/2026/10/duo-tel-aviv-film-v1-en-16x9-1.mp4', 'tall' => 'https://nad-lan.co.il/wp-content/uploads/2026/10/duo-tel-aviv-film-v1-en-9x16-1.mp4',
					'poster_wide' => 'https://nad-lan.co.il/wp-content/uploads/2026/10/duo-tel-aviv-film-v1-en-16x9-poster.jpg', 'poster_tall' => 'https://nad-lan.co.il/wp-content/uploads/2026/10/duo-tel-aviv-film-v1-en-9x16-poster.jpg',
					'secs' => 54, 'date' => '2026-10-05', 'date_he' => '5.10.2026', 'lang' => 'en', 'name' => 'DUO Tel Aviv',
					'desc' => 'A 54-second film on DUO Tel Aviv in the Somail compound: the location, the two towers, the apartments, the retail, the construction stage per the company report and the estimated view from the floors. Illustrative visualisation.',
				),
				'dir'            => 'duo',
				'mount'          => 'mountDuoStage',
				'basket_hint'    => 'לעזרה: בחוזים שנחתמו בינואר עד יוני 2026 המחיר הממוצע היה כ-71,000 ₪ למ״ר לפני מע״מ, וכ-11 מיליון ₪ לדירה כולל מע״מ, לפי דוח החברה לרבעון השני של 2026. המחיר של דירה מסוימת מהנציג.', // BasketOne v86: shown as a hint, never multiplied into a price
				'bearing_offset' => 0,
				'name'           => 'מגדלי דואו תל אביב',
				'name_en'        => 'DUO Tel Aviv',
				'developer'      => 'אפריקה ישראל מגורים',
				'place'          => 'אבן גבירול פינת ארלוזורוב, מתחם סומייל',
				'rail'           => array(),
				'poster_alt'     => 'הדמיה של מגדלי דואו תל אביב: שני מגדלי מגורים, מבנה הלובי ביניהם ומבני המסחר במתחם',
				'src_line'       => 'מקורות הבמה: קו המגרש, קווי המגדלים והבניינים הקיימים סביבם לפי עיריית <span>תל אביב-יפו</span> (שכבות המגרשים, המבנים, הרחובות, השטחים הירוקים והעצים, 9.2026). הגבהים, החזית ומיקום המתקנים להמחשה.',
				// ProjectFacts: six quick facts, each with its source
				'facts'          => array(
					// the permit's addresses (GIS 772) and the site's boundaries (licensing decision 1-25-0172, 21.9.2025)
					array( 'מיקום', 'אבן גבירול פינת ארלוזורוב', 'מתחם סומייל, תל אביב' ),
					// Africa Israel Residences' report and the city's licensing: 54 floors, of them 50 residential
					array( 'בניינים', '2 מגדלים של 54 קומות', '50 קומות מגורים בכל מגדל' ),
					// permit 20210784 of 29.12.2021 (GIS 772); 510 of them are the partners' marketable share
					array( 'דירות', '668', 'לפי היתר הבנייה' ),
					// the developer's site (duo-tlv.com, residential-towers)
					array( 'בריכה', 'על גג מבנה הלובי', 'בין שני המגדלים, לפי אתר היזם' ),
					// licensing decision 1-25-0172 (21.9.2025): basements 1 to 5
					array( 'חניה', '5 קומות מרתף', 'לפי החלטת רשות הרישוי, 9.2025' ),
					// the page: completion planned 2027 by the company's report
					array( 'מצב', 'בבנייה', 'השלמה מתוכננת ב-2027, לפי דוח החברה' ),
				),
				'progress'       => array(
					array( 'תכנית', '7.2013', 'done' ),
					array( 'היתר בנייה', '12.2021', 'done' ),
					array( 'בבנייה', 'עכשיו', 'now' ),
					array( 'השלמה', 'מתוכננת ב-2027', 'next' ),
				),
				// example apartments (the owner, 25.9.2026): one per face of each tower floor; true bearings from the GIS footprints
				'units'          => array( array( 'n', 10 ), array( 'e', 100 ), array( 's', 190 ), array( 'w', 280 ) ),
				// DuoInside (28.9.2026): the example apartment's 360 rooms on floor 25 (scripts/interior/duo_interior.py), in DUO's own
				// words for each direction (the sectors below); floor 25's eye height is about 89 m by the stage's floors (3.3 m above the
				// lobby building)
				'tour'           => array(
					'dirs'       => array(
						// DuoRooms v92 (1.72.353): n, e and w from the north tower; s from the south tower (the north tower's south
						// face looks at the south tower 28 m away), said in the scene; H Infinity is drawn as a volume by its floors
						array( 'n', 'צפון', 'לכיוון נמל תל אביב והירקון', 'הנפח הבהיר הוא אייץ׳ אינפיניטי, שנמצא בבנייה, בגובה לפי מספר הקומות.' ),
						array( 'e', 'מזרח', 'לכיוון כיכר המדינה', '' ),
						array( 's', 'דרום', 'לכיוון כיכר רבין ומרכז העיר', 'הדירה הזו במגדל הדרומי: החזית הדרומית של המגדל הצפוני פונה אל המגדל הדרומי.' ),
						array( 'w', 'מערב', 'לכיוון הים', '' ),
					),
					'facing'     => 'מול הים, נמל תל אביב, כיכר המדינה ומרכז העיר',
					'height'     => 'בגובה של כ־89 מ׳',
					'view_src'   => 'הנוף בחלון בנוי מהבניינים הקיימים לפי שכבת המבנים של העירייה ומקו החוף.',
					'card_alt'   => 'הסלון בדירה לדוגמה בקומה 25 במגדלי דואו, מבט מערבה לכיוון הים (הדמיה)',
					'card_title' => 'קומה 25 · לכיוון הים',
				),
				// ProjectDeals (HAD-365, research docs/research/2026-09-28-duo/duo-deals.md): the signed sales tied to a floor, three, from
				// the company's report of 12.9.2021 as Merkaz HaNadlan (13.9.2021) and Globes (11.10.2021) quoted it: pre-sale sales to
				// the company's insiders, labelled so. The press names the buyers; we never do. Floor 43 and a penthouse (Israel Hayom,
				// 4.2021) were purchase requests, not contracts, and stay out. Price per m² calculated: the price over the net area.
				'deals_intro'    => 'הדירות שנמכרו בפרויקט ופורסמו עם הקומה שלהן, לפי דיווח החברה כפי שפורסם בעיתונות. לא כל העסקאות פורסמו, ועסקאות של בניינים שכנים אינן כאן.',
				'deals'          => array(
					array( 'floor' => '17', 'n' => 17, 'bld' => 'הבניין השני בפרויקט', 'apt' => '4 חדרים · כ-102 מ״ר ומרפסת כ-17 מ״ר, עם חניה', 'price' => 'כ-7.44 מיליון ₪', 'psqm' => 'כ-72,900 ₪', 'date' => '9.2021', 'src' => 'מרכז הנדל״ן', 'url' => 'https://www.nadlancenter.co.il/article/4320', 'via' => 'לפי דיווח החברה: מכירה מוקדמת לבעלי עניין', 'note' => 'בקומה הזו בבניין השני נמכרה במכירה המוקדמת דירת 4 חדרים, כ-102 מ״ר, בכ-7.44 מיליון ₪ (9.2021)' ),
					array( 'floor' => '16', 'n' => 16, 'bld' => 'הבניין השני בפרויקט', 'apt' => '4 חדרים · כ-102 מ״ר ומרפסת כ-17 מ״ר, עם חניה', 'price' => 'כ-7.33 מיליון ₪', 'psqm' => 'כ-71,900 ₪', 'date' => '9.2021', 'src' => 'מרכז הנדל״ן', 'url' => 'https://www.nadlancenter.co.il/article/4320', 'via' => 'לפי דיווח החברה: מכירה מוקדמת לבעלי עניין', 'note' => 'בקומה הזו בבניין השני נמכרה במכירה המוקדמת דירת 4 חדרים, כ-102 מ״ר, בכ-7.33 מיליון ₪ (9.2021)' ),
					array( 'floor' => '12', 'n' => 12, 'bld' => 'הבניין השני בפרויקט', 'apt' => '4 חדרים · כ-102 מ״ר ומרפסת כ-17 מ״ר, עם חניה', 'price' => 'כ-7.03 מיליון ₪', 'psqm' => 'כ-68,900 ₪', 'date' => '9.2021', 'src' => 'מרכז הנדל״ן', 'url' => 'https://www.nadlancenter.co.il/article/4320', 'via' => 'לפי דיווח החברה: מכירה מוקדמת לבעלי עניין', 'note' => 'בקומה הזו בבניין השני נמכרה במכירה המוקדמת דירת 4 חדרים, כ-102 מ״ר, בכ-7.03 מיליון ₪ (9.2021)' ),
				),
				// the developer's Q2 2026 report (https://res.afi-g.com/about/Documents/2026/Q2-2026.pdf): 1.3 (372 of 510, signed
				// contracts only), 7.13.2 (71K ₪/m² before VAT, contracts of 1-6.2026), 3.5 (12 units, 10,985K ₪ average incl. VAT)
				'deals_sum'      => array(
					array( '372 מתוך 510', 'דירות נמכרו עד 6.2026, לפי דוח היזם' ),
					array( 'כ-71,000 ₪ למ״ר', 'המחיר הממוצע לפני מע״מ בחוזים שנחתמו ב-1-6.2026, לפי דוח היזם' ),
					array( 'כ-11 מיליון ₪', 'המחיר הממוצע לדירה, כולל מע״מ, ב-12 הדירות שנמכרו ב-1-6.2026, לפי דוח היזם' ),
				),
				// the view and the beam start between the two towers (build_city_duo.py); each tower's centre is about 30 m away
				'tower_lat'      => 32.085658,
				'tower_lng'      => 34.783027,
				// true bearings from that point (the city's beach layer GIS 579, green areas GIS 503; 28.9.2026)
				'sectors'        => array(
					array( 235, 315, 'לכיוון הים' ),
					array( 315, 20, 'לכיוון נמל תל אביב והירקון' ),
					array( 20, 70, 'לכיוון פארק הירקון' ),
					array( 70, 120, 'לכיוון כיכר המדינה' ),
					array( 120, 180, 'לכיוון מגדלי עזריאלי ושרונה' ),
					array( 180, 235, 'לכיוון כיכר רבין ומרכז העיר' ),
				),
			),
			// StageSdeDov v82 (28.9.2026): Dimri Yama (lot 107) and Ashira (lot 101) on their official lots; the configs are the
			// prototypes' proposals (docs/research/2026-09-28-stages/dimri-config-proposal.php.txt, ashira-config-proposal.php.txt)
			'dimri-yama-sde-dov' => array(
				// ProjectFilm v80 (5.10.2026, Ben: "everything is approved"): the film loop's v1 film, Hebrew here and English on the
				// language pages (film_en); 720p web copies, byte-checked (docs/qa/film-v1-projects/media.json)
				'film'           => array(
					'wide' => 'https://nad-lan.co.il/wp-content/uploads/2026/10/dimri-yama-sde-dov-film-v1-he-16x9-1.mp4', 'tall' => 'https://nad-lan.co.il/wp-content/uploads/2026/10/dimri-yama-sde-dov-film-v1-he-9x16-1.mp4',
					'poster_wide' => 'https://nad-lan.co.il/wp-content/uploads/2026/10/dimri-yama-sde-dov-film-v1-he-16x9-poster.jpg', 'poster_tall' => 'https://nad-lan.co.il/wp-content/uploads/2026/10/dimri-yama-sde-dov-film-v1-he-9x16-poster.jpg',
					'secs' => 47, 'date' => '2026-10-05', 'date_he' => '5.10.2026', 'lang' => 'he',
					'desc' => 'סרטון של 47 שניות על דמרי ימה שדה דב במתחם אשכול: המיקום, המגדל, הדירות וחדרי המלון לפי היזם, שלב השיווק והנוף המשוער מהקומות. הדמיה להמחשה.',
				),
				'film_en'        => array(
					'wide' => 'https://nad-lan.co.il/wp-content/uploads/2026/10/dimri-yama-sde-dov-film-v1-en-16x9-1.mp4', 'tall' => 'https://nad-lan.co.il/wp-content/uploads/2026/10/dimri-yama-sde-dov-film-v1-en-9x16-1.mp4',
					'poster_wide' => 'https://nad-lan.co.il/wp-content/uploads/2026/10/dimri-yama-sde-dov-film-v1-en-16x9-poster.jpg', 'poster_tall' => 'https://nad-lan.co.il/wp-content/uploads/2026/10/dimri-yama-sde-dov-film-v1-en-9x16-poster.jpg',
					'secs' => 47, 'date' => '2026-10-05', 'date_he' => '5.10.2026', 'lang' => 'en', 'name' => 'Dimri Yama Sde Dov',
					'desc' => 'A 47-second film on Dimri Yama Sde Dov in the Eshkol compound: the location, the tower, the apartments and hotel rooms per the developer, the marketing stage and the estimated view from the floors. Illustrative visualisation.',
				),
				'dir'            => 'dimri',
				'mount'          => 'mountDimriStage',
				'basket_hint'    => 'לעזרה: מחיר הפתיחה שפורסם בפרויקט הוא מ-3.75 מיליון ₪. המחיר של דירה מסוימת מהנציג.', // BasketOne v86: shown as a hint, never multiplied into a price
				'bearing_offset' => 0,                      // the stage's north is true north; the lots' 11° turn is inside the scene
				'name'           => 'דמרי ימה שדה דב',
				'name_en'        => 'Dimri Yama Sde Dov',
				'developer'      => 'י.ח דמרי',
				'place'          => 'מתחם אשכול, רובע שדה דב',
				'rail'           => array(),
				'poster_alt'     => 'הדמיה של דמרי ימה ברובע שדה דב: מגדל, מגדלון ושני מבנים נמוכים סביב גינה, על מגרש 107',
				'src_line'       => 'מקורות הבמה: קו המגרש והבניינים הקיימים סביבו לפי עיריית <span>תל אביב-יפו</span> (שכבות המגרשים, המבנים, הרחובות, השטחים הירוקים והעצים, 9.2026); הבניינים במגרש, הקומות והגבהים לפי תכנית העיצוב (5.2023); קו החוף לפי OpenStreetMap. החזיתות ומיקום המתקנים להמחשה.',
				// ProjectFacts: six quick facts, each with its source
				'facts'          => array(
					// GIS 837 (lot 107, Eshkol); the distance: OpenStreetMap's coastline, 650-680 m (28.9.2026)
					array( 'מיקום', 'מתחם אשכול, רובע שדה דב', 'מגרש 107, כ-700 מ׳ מהים' ),
					// the design decision (10.5.2023): "מגדל בן 40, מגדלון בן 16 קומות ושני מבנים מרקמיים בני 9 קומות"
					// (the developer's 39 is the same tower without its technical floor)
					array( 'בניינים', 'מגדל של 40 קומות', 'מגדלון של 16 ושני מבנים של 9, לפי תכנית העיצוב' ),
					// the developer and the press (sdedov.co.il 22.12.2025), as the page gives them
					array( 'דירות', '458', 'וכ-70 חדרי מלון, לפי היזם' ),
					// the design decision: the tower at most 165 m above the ground
					array( 'גובה המגדל', 'עד 165 מ׳', 'לפי תכנית העיצוב' ),
					// the page: "המחיר שפורסם מתחיל מ-3.75 מיליון שקל"
					array( 'מחיר', 'מ-3.75 מיליון ₪', 'מחיר הפתיחה שפורסם' ),
					// the page's status row ('בשיווק') and its words: "המכירה המוקדמת החלה והבנייה החלה"
					array( 'מצב', 'בשיווק', 'המכירה המוקדמת והבנייה החלו, לפי הפרסומים' ),
				),
				// ProjectProgress: done, now, next (only dated steps; the page gives no occupancy date, so none is shown)
				'progress'       => array(
					array( 'תכנית עיצוב', '5.2023', 'done' ),   // the local committee, 10.5.2023 (in force 30.6.2025, GIS 528)
					array( 'דמרי רכשה את הפרויקט', '7.2024', 'done' ), // the page: "ביולי 2024 דמרי רכשה ... מחנן מור"
					array( 'שיווק ובנייה', 'עכשיו', 'now' ),     // the page: the pre-sale and the construction have started
				),
				// example apartments (the owner, 25.9.2026): one per face of each floor of the tower and of the mid-rise; the
				// faces' true bearings from the lot's grid (11° east of north; the design decision's drawing)
				'units'          => array( array( 'n', 11 ), array( 'e', 101 ), array( 's', 191 ), array( 'w', 281 ) ),
				// the view and the beam start at the tower's centre (research 1.3, DRAWING grade)
				'tower_lat'      => 32.104333,
				'tower_lng'      => 34.784114,
				// what lies that way, true bearings from the tower (28.9.2026): the nearest waterline 281° (OpenStreetMap),
				// Reading beach 294°, Tel Baruch beach 13°, Tel Aviv University 60°, Yarkon Park 104°, the Azrieli towers 167°,
				// the Old North 200°; the same sectors as Rainbow's, 150 m to the south
				'sectors'        => array(
					array( 230, 345, 'לכיוון הים' ),
					array( 345, 30, 'לכיוון תל ברוך והרצליה' ),
					array( 30, 105, 'לכיוון רמת אביב והאוניברסיטה' ),
					array( 105, 150, 'לכיוון פארק הירקון' ),
					array( 150, 195, 'לכיוון מגדלי העיר' ),
					array( 195, 230, 'לכיוון הצפון הישן' ),
				),
			),
			'ashira-sde-dov' => array(
				'dir'            => 'ashira',
				'mount'          => 'mountAshiraStage',
				'bearing_offset' => 0,                      // the stage's north is true north; the lots' 11° turn is inside the scene
				'name'           => 'פרויקט אשירה שדה דב',
				'name_en'        => 'Ashira Sde Dov',
				'developer'      => 'אביסרור משה ובניו',
				'place'          => 'מתחם אשכול, רובע שדה דב',
				'rail'           => array(),
				'poster_alt'     => 'הדמיה של פרויקט אשירה ברובע שדה דב: מגדל, מגדלון ושני בניינים נמוכים סביב חצר, על מגרש 101',
				'src_line'       => 'מקורות הבמה: קו המגרש והבניינים הקיימים סביבו לפי עיריית <span>תל אביב-יפו</span> (שכבות המגרשים, המבנים, הרחובות, השטחים הירוקים והעצים, 9.2026); הבניינים במגרש, הקומות והגבהים לפי תכנית העיצוב (5.2023); קו החוף לפי OpenStreetMap. החזיתות ומיקום המתקנים להמחשה.',
				// ProjectFacts: six quick facts, each with its source
				'facts'          => array(
					// GIS 837 (lot 101, Eshkol); the committee's agenda: Levi Eshkol St. on the east
					array( 'מיקום', 'מתחם אשכול, רובע שדה דב', 'מגרש 101, על רחוב לוי אשכול' ),
					// the design plan: "מגדל בן 35 קומות, מגדלון בן 16 קומות ושני מבנים מרקמיים בגובה 9 קומות" (the page's "8"
					// is the same buildings without the technical floor)
					array( 'בניינים', 'מגדל של 35 קומות', 'מגדלון של 16 ושני בניינים של 9, לפי תכנית העיצוב' ),
					// the design plan's table (p.181): 202 in the tower, 65 + 57 + 82 in the other three
					array( 'דירות', '406', '202 במגדל ו-204 בשלושת הבניינים האחרים, לפי תכנית העיצוב' ),
					// the design plan: the tower about 137 m (136 in its table)
					array( 'גובה המגדל', 'כ-137 מ׳', 'לפי תכנית העיצוב' ),
					// the design plan: the pool and the gyms underground; three residents' clubs (N2, S1, S2)
					array( 'מתקנים', 'בריכה וחדרי כושר', 'בקומת המרתף, ו-3 מועדוני דיירים, לפי תכנית העיצוב' ),
					// the page's status row ('בשיווק') and its words: the full permit reported in 3.2026, the works at the
					// foundations in spring 2026, the public target for completion 2030
					array( 'מצב', 'בשיווק', 'יסודות באביב 2026, יעד השלמה ב-2030, לפי הפרסומים' ),
				),
				// ProjectProgress: done, now, next (the page's dated facts and GIS 528)
				'progress'       => array(
					array( 'תכנית עיצוב', '5.2024', 'done' ),    // in force 12.5.2024 (GIS 528, id_taba 8209); discussed 3.5.2023
					array( 'היתר בנייה', '3.2026', 'done' ),     // the page: "היתר בנייה מלא דווח במרץ 2026"
					array( 'יסודות', 'אביב 2026', 'now' ),       // the page: "העבודות דווחו בשלב היסודות באביב 2026"
					array( 'השלמה', 'יעד 2030', 'next' ),        // the page: "היעד הפומבי להשלמה הוא 2030"
				),
				// example apartments (the owner, 25.9.2026): one per face of each floor of the tower and of the mid-rise; the
				// faces' true bearings from the lot's grid (11° east of north). The design plan: every tower balcony faces west.
				'units'          => array( array( 'n', 11 ), array( 'e', 101 ), array( 's', 191 ), array( 'w', 281 ) ),
				// the view and the beam start at the tower's centre (research 2.3: the base's centre, DRAWING grade; the plate
				// on it is drawn in the middle, as the plan's renders show)
				'tower_lat'      => 32.105479,
				'tower_lng'      => 34.787466,
				// what lies that way, true bearings from the tower (28.9.2026): the nearest waterline about 280° and 930 m
				// (OpenStreetMap), Tel Baruch beach 5°, Tel Aviv University 62°, Yarkon Park 109°, the Azrieli towers 173°,
				// the Old North 207°
				'sectors'        => array(
					array( 240, 340, 'לכיוון הים' ),
					array( 340, 30, 'לכיוון תל ברוך והרצליה' ),
					array( 30, 85, 'לכיוון רמת אביב והאוניברסיטה' ),
					array( 85, 140, 'לכיוון פארק הירקון' ),
					array( 140, 195, 'לכיוון מגדלי העיר' ),
					array( 195, 240, 'לכיוון הצפון הישן' ),
				),
			),
			// KikarHamedinaWorld v104 (30.9.2026, HAD-375): Kikar Hamedina Towers on the SHARED world module
			// (assets/project-stage/world/world.js, mountWorld), not a stage.js copy: one walkable scene of the whole area
			// (docs/design/kikar-hamedina/KikarHamedinaWorld-v104-README.md). Every fact below is in
			// docs/research/2026-09-30-kikar-hamedina/facts.md or area.md with its source. P9c: one example apartment ('examples'): no 'units', no
			// 360, no tour words (the world branch never prints Rainbow's). The URL word law: "hamedina" is owned by this page.
			'hamedina' => array(
				'dir'            => 'hamedina',
				'mount'          => 'mountWorld',
				'world'          => array(
					'data'   => 'world.json',
					'poster' => array( 'wide' => 'poster-1600', 'tall' => 'poster-800', 'w' => 1600, 'h' => 1000, 'tw' => 800 ),
					'mode'   => 'aerial',
					'season' => 9,
					'hour'   => 10,
					'pond'   => true, // the pond is sourced (Mako 24.9.2026: 1 m deep); its outline is drawn and labelled "הדמיה להמחשה בלבד"
					// P9c (design system v104.2): the example apartment that has pictures (Blender Cycles from the world's data,
					// docs/research/2026-09-30-kikar-hamedina/interiors-plan.md): tower C, floor 30, the side that faces 265.61° there;
					// it turns with the tower, so floors 27-33 show the same apartment (the album says the pictures are from floor 30).
					// Its files and times are in assets/project-stage/hamedina/tour/examples.json, read only on the button's press.
					'examples' => array(
						array( 'id' => 'c30w', 'tower' => 'C', 'floor' => 30, 'band' => array( 27, 33 ), 'bearing' => 265.61 ),
					),
				),
				'bearing_offset' => 0,
				'name'           => 'מגדלי כיכר המדינה',
				'name_en'        => 'Kikar Hamedina Towers',
				'h1_he'          => 'מגדלי כיכר המדינה, תל אביב', // the design's H1 (serp-dna.md): the searched name and the city
				'developer'      => 'בנייה: אלקטרה ואשטרום', // the developers are the landowners; Electra and Ashtrom build (Globes 14.12.2022)
				'place'          => 'כיכר המדינה, צפון תל אביב',
				'rail'           => array(),
				'poster_alt'     => 'הדמיה של מגדלי כיכר המדינה בתל אביב: שלושה מגדלים מסתובבים סביב הפארק והאגם, בלב טבעת הבניינים של הכיכר ובתוך העיר עד הים',
				'src_line'       => 'מקורות ההדמיה: הבניינים, הגבהים, הרחובות, הגנים והעצים לפי עיריית <span>תל אביב-יפו</span> (מידע גאוגרפי פתוח, 9.2026); המגדלים לפי קונטור הבניין במאגר העירייה והסיבוב שפורסם, 1.25 מעלות בכל קומה. מיקום האגם והמתקנים בפארק להמחשה בלבד.',
				// ProjectFacts: six quick facts, each with its source (facts.md 1.4, 1.5, 1.8; area.md 1)
				'facts'          => array(
					array( 'מיקום', 'כיכר המדינה, תל אביב', 'על טבעת רחוב ה׳ באייר, צפון העיר' ),
					array( 'מגדלים', '3 מגדלים מסתובבים', '40, 40 ו-37 קומות' ),
					array( 'דירות', '453', 'בממוצע כ-150 מ״ר לדירה' ),
					array( 'הסיבוב', '1.25 מעלות בכל קומה', 'כ-50 מעלות לאורך מגדל של 40 קומות' ),
					array( 'הפארק', 'כ-40 דונם', 'עם אגם אקולוגי, בית ספר ומרכז קהילתי' ),
					array( 'מצב', 'השלד הושלם', 'ב-23.4.2026' ),
				),
				// ProjectProgress: the plan in force 24.6.2013, the permit 12.2022 (Globes), the frame 23.4.2026 (TLV GIS 499); the
				// delivery is not one date: the statements are a dated table in the page's text (Ashtrom 2026 ... Bizportal end of 2028)
				'progress'       => array(
					array( 'תכנית', '6.2013', 'done' ),
					array( 'היתר בנייה', '12.2022', 'done' ),
					array( 'השלד הושלם', '4.2026', 'done' ),
					array( 'בבנייה', 'עכשיו', 'now' ),
					array( 'אכלוס', '2026 עד 2028', 'next' ),
				),
				// ProjectDeals: the three deals the press tied to a floor (Globes 2.5.2025, did=1001508911); which tower was not
				// published, so no row opens a floor (n = 0). No buyer is named.
				'deals_intro'    => 'מידע גלוי: שלוש העסקאות במגדלים שפורסמו עם הקומה שלהן, כולן דירות 4 חדרים של 140 מ״ר. באיזה מגדל נמכרה כל דירה לא פורסם, ולא כל העסקאות פורסמו.',
				'deals_nosrc'    => true, // 1.72.391: no source column on this page (the sources stay in facts.md)
				// 1.72.391 (V4): the basket's price hint (BasketOne v86: shown, never multiplied into a price), public information
				'basket_hint'    => 'מידע גלוי: דירות 4 חדרים של 140 מ״ר בקומות 38 ו-39 נמכרו ב-9.58 עד 10.63 מיליון ₪, כ-71,000 ₪ למ״ר. המחיר של דירה מסוימת מהנציג.',
				'deals'          => array(
					array( 'floor' => '38', 'n' => 0, 'bld' => 'המגדל לא פורסם', 'apt' => '4 חדרים · 140 מ״ר', 'price' => '10.63 מיליון ₪', 'psqm' => 'כ-75,900 ₪', 'date' => '12.2024', 'src' => 'גלובס', 'url' => 'https://www.globes.co.il/news/article.aspx?did=1001508911', 'via' => '' ),
					array( 'floor' => '39', 'n' => 0, 'bld' => 'המגדל לא פורסם', 'apt' => '4 חדרים · 140 מ״ר', 'price' => '9.59 מיליון ₪', 'psqm' => 'כ-68,500 ₪', 'date' => '5.2024', 'src' => 'גלובס', 'url' => 'https://www.globes.co.il/news/article.aspx?did=1001508911', 'via' => '' ),
					array( 'floor' => '38', 'n' => 0, 'bld' => 'המגדל לא פורסם', 'apt' => '4 חדרים · 140 מ״ר', 'price' => '9.58 מיליון ₪', 'psqm' => 'כ-68,400 ₪', 'date' => '4.2024', 'src' => 'גלובס', 'url' => 'https://www.globes.co.il/news/article.aspx?did=1001508911', 'via' => '' ),
				),
				// the area price line (facts.md 1.14 and 3): the towers' average per the press, the Tax Authority's deals around the square
				'deals_sum'      => array(
					array( '9.58 עד 10.63 מיליון ₪', 'שלוש דירות 4 חדרים בקומות 38 ו-39, 4.2024 עד 12.2024' ),
					array( 'כ-65,000 ₪ למ״ר', 'ממוצע העסקאות במגדלים, ובקומות הגבוהות ובפנטהאוזים 80,000 עד 150,000 ₪ למ״ר' ),
					array( '63,000 עד 66,000 ₪ למ״ר', 'רוב העסקאות סביב כיכר המדינה בשנה האחרונה' ),
				),
				// the plot centre (area.md 1: the area-weighted centre of plan 2500ב's lots 101, 201-208 and 303, TLV GIS 837)
				'tower_lat'      => 32.086758,
				'tower_lng'      => 34.789776,
				// what lies that way from the plot centre, true bearings (sight-landmarks.json, 30.9.2026): the sea 293°, the port 314°,
				// Reading 327-334°, Sportek 355°, Ramat Aviv 12°, the university 27°, Park HaYarkon 55°, Moshe Aviv 106°, Savidor 109°,
				// Azrieli 170-173°, Sarona 183°, Habima 213°, City Hall 238°
				'sectors'        => array(
					array( 250, 345, 'לכיוון הים ונמל תל אביב' ),
					array( 345, 70, 'לכיוון פארק הירקון ורמת אביב' ),
					array( 70, 140, 'לכיוון רמת גן ותחנת סבידור' ),
					array( 140, 200, 'לכיוון מגדלי עזריאלי' ),
					array( 200, 250, 'לכיוון כיכר רבין ומרכז העיר' ),
				),
				// the English page's own words (the world branch prints them directly: nothing waits for a dictionary)
				'i18n'           => array(
					'en' => array(
						'name'       => 'Kikar Hamedina Towers',
						'developer'  => 'Built by Electra and Ashtrom',
						'place'      => 'Kikar Hamedina, north Tel Aviv',
						'poster_alt' => 'Illustration of Kikar Hamedina Towers in Tel Aviv: three twisting towers around the park and the pond, inside the square’s ring of buildings, with the city stretching to the sea',
						'src_line'   => 'Sources of the illustration: buildings, heights, streets, gardens and trees from the <span>Tel Aviv-Yafo</span> municipality (open GIS data, 9.2026); the towers from the municipal building outline and the published turn of 1.25° per floor. The places of the pond and of the park’s features are illustrative.',
						'facts'      => array(
							array( 'Location', 'Kikar Hamedina, Tel Aviv', 'On the He Be’Iyar ring road, north Tel Aviv' ),
							array( 'Towers', '3 twisting towers', '40, 40 and 37 floors' ),
							array( 'Apartments', '453', 'About 150 m² on average' ),
							array( 'The twist', '1.25° per floor', 'About 50° over a 40-floor tower' ),
							array( 'The park', 'About 40 dunams', 'With an ecological pond, a school and a community centre' ),
							array( 'Status', 'Frame completed', 'On 23.4.2026' ),
						),
						'progress'   => array(
							array( 'Plan', '6.2013', 'done' ),
							array( 'Building permit', '12.2022', 'done' ),
							array( 'Frame completed', '4.2026', 'done' ),
							array( 'Construction', 'now', 'now' ),
							array( 'Occupancy', '2026 to 2028', 'next' ),
						),
					),
					// P8 (1.72.370): the French, Russian and Arabic pages (/projects/hamedina-fr/, -ru, -ar). The same facts as the
					// Hebrew and English, from facts.md; the names as their sources write them in that language
					'fr' => array(
						'name'       => 'Tours Kikar Hamedina',
						'developer'  => 'Construites par Electra et Ashtrom',
						'place'      => 'Kikar Hamedina, nord de Tel Aviv',
						'poster_alt' => 'Illustration des tours Kikar Hamedina à Tel Aviv : trois tours torsadées autour du parc et de l’étang, au cœur de l’anneau d’immeubles de la place, avec la ville jusqu’à la mer',
						'src_line'   => 'Sources de l’illustration : immeubles, hauteurs, rues, jardins et arbres d’après la municipalité de <span>Tel Aviv-Jaffa</span> (données géographiques ouvertes, 09/2026) ; les tours d’après leur contour dans les données municipales et la rotation publiée de 1,25° par étage. L’emplacement de l’étang et des équipements du parc est indicatif.',
						'facts'      => array(
							array( 'Adresse', 'Kikar Hamedina, Tel Aviv', 'Sur la rue circulaire He Be’Iyar, nord de Tel Aviv' ),
							array( 'Tours', '3 tours torsadées', '40, 40 et 37 étages' ),
							array( 'Appartements', '453', 'Environ 150 m² en moyenne' ),
							array( 'La torsion', '1,25° par étage', 'Environ 50° sur une tour de 40 étages' ),
							array( 'Le parc', 'Environ 4 hectares', 'Avec un étang écologique, une école et un centre communautaire' ),
							array( 'Avancement', 'Gros œuvre achevé', 'Le 23 avril 2026' ),
						),
						'progress'   => array(
							array( 'Plan', '06/2013', 'done' ),
							array( 'Permis de construire', '12/2022', 'done' ),
							array( 'Gros œuvre achevé', '04/2026', 'done' ),
							array( 'En construction', 'aujourd’hui', 'now' ),
							array( 'Livraison', 'de 2026 à 2028', 'next' ),
						),
					),
					'ru' => array(
						'name'       => 'Башни Кикар ха-Медина',
						'developer'  => 'Строят Electra и Ashtrom',
						'place'      => 'Кикар ха-Медина, север Тель-Авива',
						'poster_alt' => 'Иллюстрация башен Кикар ха-Медина в Тель-Авиве: три закрученные башни вокруг парка и пруда, в кольце зданий площади, и город до самого моря',
						'src_line'   => 'Источники иллюстрации: здания, высоты, улицы, скверы и деревья по данным муниципалитета <span>Тель-Авива-Яффо</span> (открытые геоданные, 09.2026); башни по контуру из данных муниципалитета и опубликованному повороту 1,25° на каждом этаже. Места пруда и объектов парка показаны условно.',
						'facts'      => array(
							array( 'Адрес', 'Кикар ха-Медина, Тель-Авив', 'На кольцевой улице площади, север города' ),
							array( 'Башни', '3 закрученные башни', '40, 40 и 37 этажей' ),
							array( 'Квартиры', '453', 'В среднем около 150 м²' ),
							array( 'Поворот', '1,25° на этаж', 'Около 50° на башню в 40 этажей' ),
							array( 'Парк', 'Около 40 дунамов', 'С экологическим прудом, школой и общинным центром' ),
							array( 'Статус', 'Каркас завершён', '23.04.2026' ),
						),
						'progress'   => array(
							array( 'План', '06.2013', 'done' ),
							array( 'Разрешение на строительство', '12.2022', 'done' ),
							array( 'Каркас завершён', '04.2026', 'done' ),
							array( 'Строительство', 'сейчас', 'now' ),
							array( 'Заселение', 'с 2026 по 2028 год', 'next' ),
						),
					),
					'ar' => array(
						'name'       => 'أبراج كيكار همدينا',
						'developer'  => 'البناء: Electra وAshtrom',
						'place'      => 'كيكار همدينا، شمال تل أبيب',
						'poster_alt' => 'رسم توضيحي لأبراج كيكار همدينا في تل أبيب: ثلاثة أبراج ملتفّة حول الحديقة والبركة، داخل حلقة مباني الميدان، والمدينة ممتدة حتى البحر',
						'src_line'   => 'مصادر الرسم التوضيحي: المباني والارتفاعات والشوارع والحدائق والأشجار وفق بلدية <span>تل أبيب يافا</span> (بيانات جغرافية مفتوحة، 9.2026)؛ الأبراج وفق مخطط المبنى لدى البلدية والدوران المنشور بمقدار 1.25 درجة في كل طابق. موقع البركة ومرافق الحديقة توضيحي.',
						'facts'      => array(
							array( 'الموقع', 'كيكار همدينا، تل أبيب', 'على الشارع الدائري حول الميدان، شمال المدينة' ),
							array( 'الأبراج', '3 أبراج ملتفّة', '40 و40 و37 طابقاً' ),
							array( 'الشقق', '453', 'بمتوسط نحو 150 م² للشقة' ),
							array( 'الدوران', '1.25 درجة في كل طابق', 'نحو 50 درجة على امتداد برج من 40 طابقاً' ),
							array( 'الحديقة', 'نحو 40 دونماً', 'مع بركة بيئية ومدرسة ومركز جماهيري' ),
							array( 'الوضع', 'اكتمل الهيكل', 'في 23.4.2026' ),
						),
						'progress'   => array(
							array( 'المخطط', '6.2013', 'done' ),
							array( 'رخصة البناء', '12.2022', 'done' ),
							array( 'اكتمال الهيكل', '4.2026', 'done' ),
							array( 'قيد البناء', 'الآن', 'now' ),
							array( 'السكن', 'بين 2026 و2028', 'next' ),
						),
					),
				),
			),
		);
	}
}

/* The stage's first picture in the page's own HTML (design system ProjectStage, version 29): a phone-sized file and the
   full one; the head's preload names the same set, and the stage's script adopts this very image as its poster. */
if ( ! function_exists( 'nadlan_ps_poster_set' ) ) {
	function nadlan_ps_poster_set( $ps ) {
		$base  = 'assets/project-stage/' . $ps['dir'] . '/';
		$v     = '?ver=' . nadlan_ps_ver();
		$full  = plugins_url( $base . 'poster.jpg', dirname( __FILE__ ) ) . $v;
		$small = is_readable( dirname( __DIR__ ) . '/' . $base . 'poster-716.jpg' ) ? plugins_url( $base . 'poster-716.jpg', dirname( __FILE__ ) ) . $v : '';
		return array(
			'src'    => $full,
			'srcset' => '' !== $small ? $small . ' 716w, ' . $full . ' 1432w' : '',
			'sizes'  => '(max-width: 1099px) calc(100vw - 32px), 716px',
		);
	}
}

if ( ! function_exists( 'nadlan_ps_current' ) ) {
	function nadlan_ps_current() {
		static $memo = false;
		if ( false !== $memo ) { return $memo; }
		$memo = null;
		if ( '0' === (string) get_option( 'nadlan_project_stage', '1' ) || is_admin() || ! is_singular( 'nadlan_project' ) ) { return $memo; }
		$id   = (int) get_queried_object_id();
		$slug = (string) get_post_field( 'post_name', $id );
		$all  = nadlan_ps_config();
		// HAD-361: a project's language page (<slug>-en|fr|ru|ar) takes the Hebrew page's stage, in its own language
		// (inc/lang-pages.php on the server, assets/project-stage/i18n-dom.js in the browser); what is Hebrew-only stays
		// out (the film, the rail, the deals table, the basket). Behind nadlan_ps_langs_on() until the dictionary is complete.
		$lang = 'he';
		if ( ! isset( $all[ $slug ] ) && preg_match( '/^(.+)-(en|fr|ru|ar)$/', $slug, $lm ) && isset( $all[ $lm[1] ] ) && nadlan_ps_langs_on() ) {
			$slug = $lm[1];
			$lang = $lm[2];
		}
		if ( ! isset( $all[ $slug ] ) ) { return $memo; }
		if ( function_exists( 'nadlan_project_mode' ) && 'showroom' === nadlan_project_mode( $id ) ) { return $memo; } // the engine has the page
		if ( post_password_required( $id ) || get_post_meta( $id, '_nadlan_private_unit_journey', true ) ) { return $memo; }
		// KikarHamedinaWorld v104: a project on the shared world module needs the module and its world data, not a stage.js
		$world = ! empty( $all[ $slug ]['world'] );
		$file  = dirname( __DIR__ ) . '/assets/project-stage/' . ( $world ? 'world/world.js' : $all[ $slug ]['dir'] . '/stage.js' );
		if ( ! file_exists( $file ) || ( $world && ! is_readable( dirname( __DIR__ ) . '/assets/project-stage/' . $all[ $slug ]['dir'] . '/world.json' ) ) ) { return $memo; }
		$memo = array_merge( $all[ $slug ], array( 'id' => $id, 'slug' => $slug, 'lang' => $lang ) );
		if ( 'he' !== $lang ) {
			$fe = $memo['film_en'] ?? null; // ProjectFilm v80: a project with an English film shows it on its language pages
			unset( $memo['film'], $memo['deals'], $memo['deals_sum'], $memo['basket_hint'] );
			if ( ! empty( $fe['wide'] ) ) { $memo['film'] = $fe; }
			$memo['rail'] = array();
		}
		return $memo;
	}
}

if ( ! function_exists( 'nadlan_ps_close' ) ) {
	/** The offset just after the element that opens at $start closes (nesting of the same tag counted); 0 if none. */
	function nadlan_ps_close( $html, $start, $tag ) {
		$depth = 0;
		$pos   = $start;
		while ( preg_match( '#<(/?)' . $tag . '\b[^>]*>#i', $html, $m, PREG_OFFSET_CAPTURE, $pos ) ) {
			$depth += '/' === $m[1][0] ? -1 : 1;
			$pos    = $m[0][1] + strlen( $m[0][0] );
			if ( 0 === $depth ) { return $pos; }
		}
		return 0;
	}
}

if ( ! function_exists( 'nadlan_ps_ver' ) ) {
	function nadlan_ps_ver() { return defined( 'NADLAN_CONFIG_VERSION' ) ? NADLAN_CONFIG_VERSION : '1'; }
}

if ( ! function_exists( 'nadlan_ps_square' ) ) {
	/** BrokerSquare: a professional's square in the rail; the whole square opens the profile, the button opens WhatsApp. */
	function nadlan_ps_square( $pid, $ps ) {
		$pid = (int) $pid;
		if ( $pid <= 0 || 'nadlan_professional' !== get_post_type( $pid ) || 'publish' !== get_post_status( $pid ) ) { return ''; }
		$name  = function_exists( 'nadlan_prof_person_name' ) ? (string) nadlan_prof_person_name( $pid ) : get_the_title( $pid );
		$role  = function_exists( 'nadlan_dir_prof_label' ) ? (string) nadlan_dir_prof_label( (string) get_post_meta( $pid, 'profession', true ), $pid ) : '';
		$lic   = trim( (string) get_post_meta( $pid, 'license_number', true ) );
		$areas = array_slice( array_filter( array_map( 'trim', explode( ',', (string) get_post_meta( $pid, 'areas_served', true ) ) ) ), 0, 3 );
		$wa    = function_exists( 'nadlan_prof_wa_digits' ) ? (string) nadlan_prof_wa_digits( (string) get_post_meta( $pid, 'phone', true ) ) : '';
		$site  = (int) get_post_meta( $pid, 'nl_site_he', true );
		$href  = $site > 0 && 'publish' === get_post_status( $site ) ? get_permalink( $site ) : get_permalink( $pid );
		$photo = has_post_thumbnail( $pid ) ? get_the_post_thumbnail( $pid, 'medium_large', array( 'alt' => $name, 'loading' => 'lazy' ) ) : '<span class="nlds-mono" aria-hidden="true">' . esc_html( mb_substr( $name, 0, 1 ) ) . '</span>';
		$text  = 'שלום ' . $name . ', ראיתי את הכרטיס שלך בעמוד של ' . $ps['name'] . ' באתר nad-lan.co.il ואשמח להתייעץ';
		$ev    = ' data-nlps-ev="rail" data-nlps-pro="' . $pid . '"';
		$h  = '<div class="nlds"><article class="nlbsq">';
		$h .= '<figure class="nlbsq__photo"><span class="nlbsq__ad">פרסומת</span>' . $photo . '</figure>';
		$h .= '<div class="nlbsq__body"><h3 class="nlbsq__name"><a href="' . esc_url( $href ) . '"' . $ev . '>' . esc_html( $name ) . '</a></h3>';
		$h .= '<p class="nlbsq__role">' . ( '' !== $role ? '<b>' . esc_html( $role ) . '</b>' : '' ) . ( $areas ? ( '' !== $role ? ' · ' : '' ) . esc_html( implode( ', ', $areas ) ) : '' ) . '</p>';
		if ( '' !== $lic ) { $h .= '<p class="nlbsq__lic">רישיון תיווך <span class="nlds-num">' . esc_html( $lic ) . '</span></p>'; }
		$recs = function_exists( 'nadlan_endorse_counts' ) ? ( nadlan_endorse_counts( array( $pid ) )[ $pid ] ?? 0 ) : 0;
		if ( $recs > 0 ) { $h .= '<p class="nlbsq__recs">' . nadlan_endorse_count_html( $recs, true ) . '</p>'; }
		$h .= '<div class="nlbsq__cta">';
		$h .= '' !== $wa
			? '<a class="nlds-btn nlds-btn--primary" target="_blank" rel="noopener" href="https://wa.me/' . esc_attr( $wa ) . '?text=' . rawurlencode( $text ) . '"' . $ev . ' data-nlps-wa="1">' . ( function_exists( 'nlds_icon' ) ? nlds_icon( 'whatsapp' ) : '' ) . '<span>התייעצות בוואטסאפ</span></a>'
			: '<a class="nlds-btn nlds-btn--secondary" href="' . esc_url( $href ) . '"' . $ev . '><span>לכרטיס המלא</span></a>';
		$h .= '</div></div></article></div>';
		return $h;
	}
}

if ( ! function_exists( 'nadlan_ps_slot' ) ) {
	/** BrokerSlot: the empty square, an open invitation to professionals (the join form with the licence check is on /brokers/). */
	function nadlan_ps_slot() {
		return '<div class="nlds"><div class="nlbslot">'
			. '<span class="nlbslot__icon" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><path d="M12 5v14M5 12h14"/></svg></span>'
			. '<p class="nlbslot__title">רוצה להופיע כאן?</p>'
			. '<p class="nlbslot__text">מתווכים ואנשי מקצוע באזור: הכרטיס שלכם ליד הפרויקט, מול מי שבודק אותו עכשיו.</p>'
			. '<a class="nlbslot__cta" href="' . esc_url( home_url( '/brokers/#join' ) ) . '" data-nlps-ev="slot">לפרטים ולהצטרפות</a>'
			. '</div></div>';
	}
}

if ( ! function_exists( 'nadlan_ps_deals' ) ) {
	/** ProjectDeals (design system, 25.9.2026): the sold apartments the sources tie to a floor, each row with its source; a
	 *  tower row opens that floor on the stage. Nothing is printed without at least two deals. No buyer is ever named. */
	function nadlan_ps_deals( $ps ) {
		$rows = (array) ( $ps['deals'] ?? array() );
		if ( count( $rows ) < 2 ) { return ''; }
		$h  = '<div class="nlds nlps-dealswrap" dir="rtl" lang="he"><section class="nlpd" id="nlps-deals" aria-labelledby="nlpd-t">';
		$h .= '<div class="nlpd__head"><p class="nlds-kicker">עסקאות בפרויקט</p><h2 class="nlpd__title" id="nlpd-t">דירות שנמכרו ב' . esc_html( $ps['name'] ) . ', לפי קומה</h2>';
		// the sources' own words per project (DuoInside, 28.9.2026: DUO's rows come from the company's report, not the Tax Authority)
		$intro = ! empty( $ps['deals_intro'] ) ? (string) $ps['deals_intro'] : 'הדירות שנמכרו בפרויקט ופורסמו עם הקומה שלהן, לפי נתוני רשות המסים כפי שפורסמו בעיתונות. לא כל העסקאות פורסמו, ועסקאות של בניינים שכנים אינן כאן.';
		$h .= '<p class="nlpd__intro">' . esc_html( $intro ) . '</p></div>';
		if ( ! empty( $ps['deals_sum'] ) ) {
			$h .= '<ul class="nlpd__sum">';
			foreach ( (array) $ps['deals_sum'] as $t ) { $h .= '<li><b>' . esc_html( $t[0] ) . '</b><span>' . esc_html( $t[1] ) . '</span></li>'; }
			$h .= '</ul>';
		}
		$nosrc = ! empty( $ps['deals_nosrc'] ); // 1.72.391: a page that names no sources (Kikar Hamedina) drops the column
		$h .= '<table class="nlpd__table"><thead><tr><th scope="col">קומה</th><th scope="col">הדירה</th><th scope="col">מחיר</th><th scope="col">למ״ר</th><th scope="col">מועד</th>' . ( $nosrc ? '' : '<th scope="col">מקור</th>' ) . '<th scope="col"><span class="nlpd__sr">בבמה</span></th></tr></thead><tbody>';
		foreach ( $rows as $d ) {
			$n   = (int) ( $d['n'] ?? 0 );
			$src = '<a href="' . esc_url( $d['url'] ) . '" target="_blank" rel="noopener">' . esc_html( $d['src'] ) . '</a>' . ( ! empty( $d['via'] ) ? ', ' . esc_html( $d['via'] ) : '' );
			$h  .= '<tr><td class="nlpd__floor"><b>' . esc_html( $d['floor'] ) . '</b><span>' . esc_html( $d['bld'] ) . '</span></td>'
				. '<td>' . esc_html( $d['apt'] ) . '</td><td>' . esc_html( $d['price'] ) . '</td><td>' . esc_html( $d['psqm'] ) . '</td>'
				. '<td>' . esc_html( $d['date'] ) . '</td>' . ( $nosrc ? '' : '<td class="nlpd__src">' . $src . '</td>' )
				. '<td>' . ( $n > 0 ? '<button class="nlpd__go" type="button" data-nlps-floor="' . $n . '" aria-label="' . esc_attr( 'קומה ' . $n . ' במגדל, בבמה' ) . '">לקומה במגדל</button>' : '' ) . '</td></tr>';
		}
		$h .= '</tbody></table><p class="nlpd__note">המחיר למ״ר מחושב: המחיר שפורסם חלקי שטח הדירה, בלי המרפסת והחניה.</p></section></div>';
		return $h;
	}
}

if ( ! function_exists( 'nadlan_ps_parts' ) ) {
	/** The pieces the page top is composed of. $h1 is the page's own h1 text; $map the moved area map section. */
	function nadlan_ps_parts( $ps, $h1, $map ) {
		if ( ! empty( $ps['world'] ) && function_exists( 'nadlan_ps_world_parts' ) ) { return nadlan_ps_world_parts( $ps, $h1, $map ); } // KikarHamedinaWorld v104
		$id  = (int) $ps['id'];
		$wa  = function_exists( 'nadlan_cta_whatsapp_number' ) ? preg_replace( '/\D/', '', (string) nadlan_cta_whatsapp_number() ) : '';
		$sec = array();
		foreach ( (array) $ps['sectors'] as $s ) { $sec[] = array( (float) $s[0], (float) $s[1], (string) $s[2] ); }
		$cfg = array(
			'stage'         => plugins_url( 'assets/project-stage/' . $ps['dir'] . '/stage.js', dirname( __FILE__ ) ) . '?ver=' . nadlan_ps_ver(),
			'poster'        => plugins_url( 'assets/project-stage/' . $ps['dir'] . '/poster.jpg', dirname( __FILE__ ) ) . '?ver=' . nadlan_ps_ver(),
			'mount'         => (string) $ps['mount'],
			'bearingOffset' => (float) $ps['bearing_offset'],
			'lat'           => ! empty( $ps['tower_lat'] ) ? (float) $ps['tower_lat'] : (float) get_post_meta( $id, 'lat', true ),
			'lng'           => ! empty( $ps['tower_lng'] ) ? (float) $ps['tower_lng'] : (float) get_post_meta( $id, 'lng', true ),
			'token'         => (string) get_option( 'nadlan_mapbox_token', '' ),
			'wa'            => $wa,
			'name'          => (string) $ps['name'],
			'sectors'       => $sec,
		);
		// example apartments and the floor card's sourced lines (a sold apartment on that tower floor, else the developer's words)
		if ( ! empty( $ps['units'] ) ) { $cfg['units'] = array_values( (array) $ps['units'] ); }
		$notes = array();
		foreach ( (array) ( $ps['deals'] ?? array() ) as $d ) {
			if ( ! empty( $d['n'] ) && ! empty( $d['note'] ) ) { $notes[ (string) (int) $d['n'] ] = (string) $d['note']; }
		}
		if ( $notes ) { $cfg['notes'] = $notes; }
		if ( ! empty( $ps['low_note'] ) ) { $cfg['lowNote'] = (string) $ps['low_note']; $cfg['lowUpTo'] = (int) ( $ps['low_up_to'] ?? 0 ); }
		if ( ! empty( $ps['high_note'] ) ) { $cfg['highNote'] = (string) $ps['high_note']; }
		// FloorSlice v87: the project's own sourced line under the floor's plan (apartments per floor, as published)
		if ( ! empty( $ps['slice_note'] ) ) { $cfg['sliceNote'] = (string) $ps['slice_note']; }
		// the project's facilities (design system FacilityHotspots v72): sourced cards pinned on the model, in the project's folder
		$ff = dirname( __DIR__ ) . '/assets/project-stage/' . $ps['dir'] . '/facilities.json';
		if ( is_readable( $ff ) ) {
			$fj = json_decode( (string) file_get_contents( $ff ), true );
			if ( is_array( $fj ) && ! empty( $fj['facilities'] ) ) { $cfg['facilities'] = array_values( (array) $fj['facilities'] ); }
			// BuildingWalk v96: the building's walk between the 360 rooms (the doors' positions, the where-to list's words)
			if ( ! empty( $cfg['facilities'] ) && ! empty( $fj['walk'] ) && is_array( $fj['walk'] ) ) { $cfg['walk'] = $fj['walk']; }
		}
		// AreaLife v97: the place registry beside the stage (scripts/project-stage/build_places_<project>.py); the browser loads it
		if ( is_readable( dirname( __DIR__ ) . '/assets/project-stage/' . $ps['dir'] . '/places.json' ) ) { $cfg['places'] = 1; }
		// the quarter around the building (design system QuarterPins): built offline into the project's folder
		// (scripts/project-stage/build_quarter_rainbow.py); a missing or broken file leaves the stage as it was
		$qf = dirname( __DIR__ ) . '/assets/project-stage/' . $ps['dir'] . '/quarter.json';
		if ( is_readable( $qf ) ) {
			$q = json_decode( (string) file_get_contents( $qf ), true );
			if ( is_array( $q ) && ( ! empty( $q['projects'] ) || ! empty( $q['places'] ) ) ) {
				$cfg['quarter'] = array( 'projects' => array_values( (array) ( $q['projects'] ?? array() ) ), 'places' => array_values( (array) ( $q['places'] ?? array() ) ), 'note' => (string) ( $q['note'] ?? '' ) );
			}
		}
		$hero = '';
		$cta  = '';
		if ( '' !== $h1 ) {
			$en   = (string) ( $ps['name_en'] ?? '' );
			// the kicker is a div, so the lead stays the first paragraph after the h1 (the recipe, row 5)
			$hero = '<header class="nlds nlps-herowrap" dir="rtl" lang="he"><div class="nlps-hero">'
				. ( 'he' !== ( $ps['lang'] ?? 'he' )
					? '<h1 id="nl-project-page-title" class="nlps-h1">' . esc_html( $h1 ) . '</h1>' // the language page's own title
					: '<h1 id="nl-project-page-title" class="nlps-h1">' . esc_html( $ps['name'] ) . ( '' !== $en ? ' <span class="nlps-h1__en" lang="en">' . esc_html( $en ) . '</span>' : '' ) . '</h1>' )
				. ( ! empty( $ps['developer'] ) || ! empty( $ps['place'] ) ? '<div class="nlps-kicker">' . ( ! empty( $ps['developer'] ) ? '<b>' . esc_html( $ps['developer'] ) . '</b>' : '' ) . ( ! empty( $ps['developer'] ) && ! empty( $ps['place'] ) ? ' · ' : '' ) . esc_html( (string) ( $ps['place'] ?? '' ) ) . '</div>' : '' )
				. '</div></header>';
			// the WhatsApp message in the page's language on a language page (HAD-361, 1.72.350), the project by its Latin name
			$pl    = (string) ( $ps['lang'] ?? 'he' );
			$wa_tx = 'שלום, אשמח לקבל תוכניות ומחירים ב' . $ps['name'] . ' (nad-lan.co.il)';
			if ( 'he' !== $pl ) {
				$pn  = function_exists( 'nadlan_lp_tr' ) ? nadlan_lp_tr( (string) $ps['name'], $pl ) : null;
				$pn  = null !== $pn ? $pn : ( '' !== $en ? $en : (string) $ps['name'] );
				$tpl = array(
					'en' => 'Hello, I would like plans and prices for %s (nad-lan.co.il)',
					'fr' => 'Bonjour, je souhaite recevoir les plans et les prix de %s (nad-lan.co.il)',
					'ru' => 'Здравствуйте, хочу получить планировки и цены: %s (nad-lan.co.il)',
					'ar' => 'مرحباً، أودّ الحصول على المخططات والأسعار في %s (nad-lan.co.il)',
				);
				if ( isset( $tpl[ $pl ] ) ) { $wa_tx = sprintf( $tpl[ $pl ], $pn ); }
			}
			$cta  = '<div class="nlds nlps-ctawrap" dir="rtl" lang="he"><div class="nlps-hero__cta">'
				. ( '' !== $wa ? '<a class="nlds-btn nlds-btn--primary" target="_blank" rel="noopener" data-nlps-ev="hero-wa" href="https://wa.me/' . esc_attr( $wa ) . '?text=' . rawurlencode( $wa_tx ) . '">' . ( function_exists( 'nlds_icon' ) ? nlds_icon( 'whatsapp' ) : '' ) . '<span>לקבלת תוכניות ומחירים</span></a>' : '' )
				. '<a class="nlds-btn nlds-btn--secondary" href="#nlps-t" data-nlps-ev="hero-pick"><span>לבחירת קומה</span></a>'
				// VideoCall v73: a video call with NadLan's team, booked in the scheduler's band at the page's end
				. ( function_exists( 'nadlan_sched_on' ) && nadlan_sched_on() && '1' !== get_post_meta( $id, 'nadlan_sched_off', true ) ? '<a class="nlds-btn nlds-btn--secondary nlps-hero__video" href="#nlsch" data-nlps-ev="hero-video"><span>שיחת וידאו עם נציג</span></a>' : '' )
				// ProjectFilm v79: the film opens in a dialog (printed in the footer); nothing loads until it is pressed
				. ( ! empty( $ps['film']['wide'] ) ? '<a class="nlds-btn nlds-btn--secondary nlps-hero__film" href="#nlfilm" data-nlps-ev="hero-film" aria-haspopup="dialog"><span class="nlps-film__pl" aria-hidden="true"></span><span>' . esc_html( nadlan_ps_film_t( $ps )['btn'] ) . ' <small>· ' . (int) $ps['film']['secs'] . ' ' . esc_html( nadlan_ps_film_t( $ps )['secs'] ) . '</small></span></a>' : '' )
				. '</div></div>';
		}
		$rail = '';
		foreach ( (array) ( $ps['rail'] ?? array() ) as $pid ) { $rail .= nadlan_ps_square( $pid, $ps ); }
		if ( 'he' === ( $ps['lang'] ?? 'he' ) ) { $rail .= nadlan_ps_slot(); }
		$view = '<div class="nlds nlps-viewwrap"><div class="nlps-view" id="nlps-view">'
			. '<div class="nlps-view__head"><p class="nlds-kicker" id="nlps-view-k">הנוף מהקומה</p><h3 class="nlps-view__title" id="nlps-view-t">' . ( ! empty( $ps['units'] ) ? 'בחרו קומה ודירה לדוגמה' : 'בחרו קומה וכיוון' ) . '</h3></div>'
			. '<div class="nlps-view__map nlps-stand" id="nlps-view-map" role="img" aria-label="מבט משוער מהקומה לכיוון שנבחר"><span id="nlps-view-empty">' . ( ! empty( $ps['units'] ) ? 'בחרו קומה במגדל ודירה לדוגמה בטבעת שלה, והנוף מהדירה יופיע כאן.' : 'בחרו קומה במגדל ונקודה בטבעת שלה, והנוף מהגובה ומהכיוון האלה יופיע כאן.' ) . '</span></div>'
			. '<p class="nlps-view__cap" id="nlps-view-cap" hidden></p>'
			// what lies that way (design system ProjectStage version 35): filled by the bridge from quarter.json, per direction
			. ( ! empty( $cfg['quarter'] ) ? '<div class="nlps-near" id="nlps-near" hidden></div>' : '' )
			. '<div class="nlps-view__cta" id="nlps-view-cta" hidden>'
			. ( '' !== $wa ? '<a class="nlds-btn nlds-btn--primary" id="nlps-wa" target="_blank" rel="noopener" href="https://wa.me/' . esc_attr( $wa ) . '">' . ( function_exists( 'nlds_icon' ) ? nlds_icon( 'whatsapp' ) : '' ) . '<span>לקבלת תוכניות ומחירים</span></a>' : '' )
			. ( '' !== $map ? '<a class="nlds-btn nlds-btn--secondary" id="nlps-tomap" href="#nlpjx-map"><span>הכיוון על המפה</span></a>' : '' ) . '</div>'
			. '</div></div>';
		// the stage keeps a section heading for the page's outline (h1, then this h2), read by screen readers only: on the
		// page itself the stage sits next to the title, which says it all
		// the stage's sources, always visible and in the page's HTML, when the real city stands around the building (StageCity)
		$src = is_readable( dirname( __DIR__ ) . '/assets/project-stage/' . $ps['dir'] . '/city.json' )
			? '<p class="nlps-src">' . ( ! empty( $ps['src_line'] ) ? wp_kses( (string) $ps['src_line'], array( 'span' => array() ) ) : 'מקורות הבמה: קו המגרש והבניינים הקיימים סביבו לפי עיריית <span>תל אביב-יפו</span> (שכבות התוכניות והמבנים, 9.2026); הפרויקטים ברובע לפי העמודים שלהם באתר.' ) . '</p>'
			: '';
		// the quarter's legend (design system QuarterPins, version 23): what stands today, what is being built, what is selling,
		// what is at the permit stage; each project's group from its page, counted here; the building itself counts when it is
		// being built. Not a year-by-year view: most pages give no completion year, and a guessed year is not shown.
		$legend = '';
		if ( ! empty( $cfg['quarter']['projects'] ) ) {
			$n = array( 'building' => 0, 'selling' => 0, 'permit' => 0 );
			foreach ( (array) $cfg['quarter']['projects'] as $qp ) {
				$ph = isset( $qp['phase'] ) ? (string) $qp['phase'] : '';
				if ( isset( $n[ $ph ] ) ) {
					$n[ $ph ]++;
				}
			}
			foreach ( (array) ( $ps['facts'] ?? array() ) as $f ) { // the building itself, by the page's own status row
				if ( isset( $f[0], $f[1] ) && 'מצב' === $f[0] && false !== strpos( (string) $f[1], 'בבנייה' ) ) {
					$n['building']++;
					break;
				}
			}
			$today = 0;
			$cfile = dirname( __DIR__ ) . '/assets/project-stage/' . $ps['dir'] . '/city.json';
			if ( is_readable( $cfile ) ) {
				$cj    = json_decode( (string) file_get_contents( $cfile ), true );
				$today = is_array( $cj ) && ! empty( $cj['b'] ) ? count( $cj['b'] ) : 0;
			}
			$chip   = function ( $key, $label, $count ) {
				return '<button type="button" class="qp-chip" data-nlps-phase="' . esc_attr( $key ) . '" aria-pressed="false"><i class="qp-dot qp-dot--' . esc_attr( $key ) . '"></i>' . esc_html( $label )
					. ( '' !== (string) $count ? ' <span class="qp-chip__n">' . esc_html( (string) $count ) . '</span>' : '' ) . '</button>';
			};
			$legend = '<div class="qp-legend" role="group" aria-label="' . esc_attr( 'מה סביב ' . $ps['name'] ) . '">'
				. ( ! empty( $cfg['facilities'] ) ? $chip( 'facilities', 'מתקנים בפרויקט', count( $cfg['facilities'] ) ) : '' )
				. ( $today ? $chip( 'today', 'קיים היום', number_format( $today ) . ' בניינים' ) : '' )
				. ( $n['building'] ? $chip( 'building', 'בבנייה', $n['building'] ) : '' )
				. ( $n['selling'] ? $chip( 'selling', 'בשיווק', $n['selling'] ) : '' )
				. ( $n['permit'] ? $chip( 'permit', 'בשלב ההיתר', $n['permit'] ) : '' )
				. '<p class="qp-legend__note">המצב של כל פרויקט לפי העמוד שלו באתר, 9.2026. שנת אכלוס מוצגת רק כשהעמוד נותן אותה.</p></div>';
		}
		// the first picture, painted with the page (it no longer waits for the scripts; 9.1 s on a mid Android before)
		$pset = nadlan_ps_poster_set( $ps );
		$ssr  = '<img class="nlps-ssr-poster" src="' . esc_url( $pset['src'] ) . '"'
			. ( '' !== $pset['srcset'] ? ' srcset="' . esc_attr( $pset['srcset'] ) . '" sizes="' . esc_attr( $pset['sizes'] ) . '"' : '' )
			. ' width="1432" height="1320" alt="' . esc_attr( ! empty( $ps['poster_alt'] ) ? (string) $ps['poster_alt'] : 'הדמיה של פרויקט ' . $ps['name'] . ', מגדל ובנייני בוטיק סביב גינה' ) . '" fetchpriority="high" decoding="async">';
		$has_inside = is_readable( dirname( __DIR__ ) . '/assets/project-stage/' . $ps['dir'] . '/tour/living-25w-card.jpg' );
		$stagebox = '<div class="nlps-stagebox"><h2 class="nlps-srt" id="nlps-t">סיור וירטואלי: הקומות והנוף</h2>'
			. '<section class="nlps-stage" id="nlps" aria-labelledby="nlps-t" data-cfg="' . esc_attr( wp_json_encode( $cfg ) ) . '"><div class="nlps-stage__mount" id="nlps-stage">' . $ssr . '</div>'
			// StageFacilities v95 (28.9.2026): the facilities on the model itself; the owner did not find them behind the
			// legend's chip under the stage ("I didn't see facilities in Rainbow, how do you click it"). The same
			// data-nlps-phase as the chip, so bridge.js keeps the two in step.
			. ( ! empty( $cfg['facilities'] ) ? '<button type="button" class="nlps-facbtn" data-nlps-phase="facilities" aria-pressed="false"><i aria-hidden="true">✦</i>המתקנים בפרויקט <b>' . (int) count( $cfg['facilities'] ) . '</b></button>' : '' )
			. '</section>'
			. '<div class="nlds">' . ( ! empty( $ps['units'] )
				// the steps under the stage (design system ProjectStage version 33): what the page can do, each a button
				? '<ol class="nlps-steps" aria-label="מה אפשר לעשות כאן">'
					. '<li><button type="button" class="nlps-step" data-nlps-step="floor" aria-current="step"><i>1</i>בוחרים קומה</button></li>'
					. '<li><button type="button" class="nlps-step" data-nlps-step="view"><i>2</i>הנוף והמפה</button></li>'
					. ( $has_inside ? '<li><button type="button" class="nlps-step" data-nlps-step="inside"><i>3</i>נכנסים לדירה</button></li>' : '' )
					. '<li><button type="button" class="nlps-step" data-nlps-step="design"><i>' . ( $has_inside ? '4' : '3' ) . '</i>מעצבים את הדירה</button></li></ol>'
				: '<p class="nlps-hint" id="nlps-hint">בחרו קומה במגדל, ואחר כך נקודה בטבעת הקומה כדי לבחור כיוון.</p>' ) . $legend . $src . '</div></div>';
		$rail  = '<aside class="nlps-rail" aria-label="אנשי מקצוע באזור">' . $rail . '</aside>';
		$below = '<div class="nlps-below' . ( '' === $map ? ' nlps-below--solo' : '' ) . '">' . $view . $map . '</div>';
		$facts = '';
		if ( ! empty( $ps['facts'] ) || ! empty( $ps['progress'] ) ) {
			$facts = '<div class="nlds nlps-factswrap" dir="rtl" lang="he">';
			if ( ! empty( $ps['facts'] ) ) {
				$facts .= '<div class="nlpf" role="list" aria-label="עובדות בקצרה">';
				foreach ( (array) $ps['facts'] as $f ) {
					$facts .= '<div class="nlpf__item" role="listitem"><p class="nlpf__k">' . esc_html( $f[0] ) . '</p><p class="nlpf__v">' . esc_html( $f[1] ) . '</p>' . ( ! empty( $f[2] ) ? '<p class="nlpf__s">' . esc_html( $f[2] ) . '</p>' : '' ) . '</div>';
				}
				$facts .= '</div>';
			}
			if ( ! empty( $ps['progress'] ) ) {
				$facts .= '<ol class="nlprog" aria-label="שלב הפרויקט">';
				foreach ( (array) $ps['progress'] as $st ) {
					$cls = 'done' === $st[2] ? ' is-done' : ( 'now' === $st[2] ? ' is-now' : '' );
					$facts .= '<li class="nlprog__step' . $cls . '"' . ( 'now' === $st[2] ? ' aria-current="step"' : '' ) . '><b>' . esc_html( $st[0] ) . '</b>' . esc_html( $st[1] ) . '</li>';
				}
				$facts .= '</ol>';
			}
			$facts .= '</div>';
		}
		// the example apartment from the inside (design system ApartmentTour, versions 24-25): floor 25 in the tower's four
		// directions, each titled with the page's own words for what lies that way; only the pictures that are on the server
		$tour  = '';
		$tdir  = 'assets/project-stage/' . $ps['dir'] . '/tour/';
		if ( is_readable( dirname( __DIR__ ) . '/' . $tdir . 'living-25w-card.jpg' ) ) {
			$turl   = plugins_url( $tdir, dirname( __FILE__ ) );
			$tv     = '?ver=' . nadlan_ps_ver();
			// the words are the project's own (DuoInside, 28.9.2026: 'tour' in the config); without them, Rainbow's
			$tc     = (array) ( $ps['tour'] ?? array() );
			$planned = 'הנפחים השקופים הם פרויקטים מתוכננים ברובע, בגובה לפי מספר הקומות.';
			$dirs   = ! empty( $tc['dirs'] ) ? (array) $tc['dirs'] : array(
				array( 'n', 'צפון', 'לכיוון תל ברוך והרצליה', $planned ),
				array( 'e', 'מזרח', 'לכיוון רמת אביב והאוניברסיטה', $planned ),
				array( 's', 'דרום', 'לכיוון מגדלי העיר', $planned ),
				array( 'w', 'מערב', 'לכיוון הים', '' ),
			);
			$cd     = (string) ( $tc['card_dir'] ?? 'w' );
			// each direction in the living room and on the balcony (version 26), where its picture is on the server
			$spots  = array( array( 'living', 'בסלון', '' ), array( 'balcony', 'במרפסת', 'במרפסת, ' ) );
			// the stage draws the tower's balconies as its marketing shows them (waves up to 3.6 m); the design plan
			// (10.5.2023) limits the tower's balconies to 2 m: the balcony scenes say so, so no buyer takes the size as given
			$balnote = 'עומק המרפסת בציור להמחשה בלבד: לפי תכנית העיצוב (5.2023), מרפסות המגדל בולטות עד 2 מ׳.';
			$scenes = array();
			$bal    = false;
			foreach ( array( 25, 10, 36 ) as $fl ) {
			foreach ( $dirs as $dd ) {
				foreach ( $spots as $sp ) {
					if ( ! is_readable( dirname( __DIR__ ) . '/' . $tdir . $sp[0] . '-' . $fl . $dd[0] . '.jpg' ) ) {
						continue;
					}
					$bal      = $bal || 'balcony' === $sp[0];
					// ApartmentStyles v80: the design styles rendered for this room (Blender, scripts/interior/render_styles.py)
					$sts = array();
					foreach ( array( array( 'warm', 'עץ חם', 'פרקט אלון, מטבח אגוז, פשתן' ), array( 'light', 'בהיר', 'אלון לבן, מטבח מרווה' ), array( 'stone', 'אבן', 'אבן אפורה, עור קוניאק' ) ) as $st ) {
						$sb = $sp[0] . '-' . $fl . $dd[0] . '-' . $st[0];
						if ( is_readable( dirname( __DIR__ ) . '/' . $tdir . $sb . '.jpg' ) ) {
							$sts[] = array( 'id' => $st[0], 'label' => $st[1], 'sub' => $st[2], 'src' => $turl . $sb . '.jpg' . $tv, 'small' => $turl . $sb . '-2k.jpg' . $tv, 'thumb' => $turl . $sb . '-thumb.jpg' . $tv );
						}
					}
					if ( $sts ) {
						array_unshift( $sts, array( 'id' => 'bare', 'label' => 'כמו במסירה', 'sub' => 'ריק, אריחים בהירים', 'thumb' => $turl . $sp[0] . '-' . $fl . $dd[0] . '-bare-thumb.jpg' . $tv ) );
					}
					$scenes[] = array(
						'id'        => $dd[0] . ( 'living' === $sp[0] ? '' : '-' . $sp[0] ),
						'dir'       => $dd[0],
						'dirLabel'  => $dd[1],
						'spot'      => $sp[0],
						'spotLabel' => $sp[1],
						'title'     => 'קומה ' . $fl . ' · ' . $sp[2] . $dd[2],
						'src'       => $turl . $sp[0] . '-' . $fl . $dd[0] . '.jpg' . $tv,
						'small'     => $turl . $sp[0] . '-' . $fl . $dd[0] . '-2k.jpg' . $tv,
						'note'      => trim( ( 'balcony' === $sp[0] ? $balnote . ' ' : '' ) . $dd[3] ),
						'floor'     => $fl,
						'styles'    => $sts,
					);
				}
			}
			}
			// the floors that have pictures, low to high ("קומות 10, 25 ו־36")
			$fls = array_values( array_unique( array_map( function ( $x ) { return (int) $x['floor']; }, $scenes ) ) );
			sort( $fls );
			$fln = count( $fls ) > 1 ? 'קומות ' . implode( ', ', array_slice( $fls, 0, -1 ) ) . ' ו־' . end( $fls ) : 'קומה 25';
			$n25 = count( array_filter( $scenes, function ( $x ) { return 25 === (int) $x['floor']; } ) );
			$tour = '<div class="nlds nlps-tourwrap" dir="rtl" lang="he"><section class="nlat" id="nlps-tour" aria-labelledby="nlat-t">'
				. '<div class="nlat__media"><img src="' . esc_url( $turl . 'living-25' . $cd . '-card.jpg' . $tv ) . '" alt="' . esc_attr( (string) ( $tc['card_alt'] ?? 'הסלון בדירה לדוגמה בקומה 25, מבט אל הים (הדמיה)' ) ) . '" width="1200" height="675" loading="lazy" decoding="async"><span class="nlds-sample">דירה לדוגמה</span></div>'
				. '<div class="nlat__body"><p class="nlds-kicker">הדירה לדוגמה מבפנים</p>'
				. '<h2 class="nlat__title" id="nlat-t">' . esc_html( $fln ) . ( $n25 > 1 ? ', בארבעת הכיוונים' : ' · ' . esc_html( (string) ( $tc['one_dir'] ?? 'לכיוון הים' ) ) ) . '</h2>'
				. '<p class="nlat__text">סלון ומטבח פתוח כמו במסירה, בלי ריהוט, ' . ( count( $fls ) > 1 ? 'ב' . esc_html( $fln ) : esc_html( (string) ( $tc['height'] ?? 'בגובה של כ־99 מ׳' ) ) )
				. ( $n25 > 1 ? ': ' . esc_html( (string) ( $tc['facing'] ?? 'מול הים, תל ברוך, רמת אביב ומגדלי העיר' ) ) . ( $bal ? ', מהסלון ומהמרפסת' : '' ) : '' )
				. '. ' . esc_html( (string) ( $tc['view_src'] ?? 'הנוף בחלון בנוי מהבניינים הקיימים לפי שכבת המבנים של העירייה, מהפרויקטים המתוכננים ברובע כנפחים שקופים, מקו החוף ומהים.' ) ) . '</p>'
				. '<button type="button" class="nlds-btn nlds-btn--primary nlat__go" data-nlps-tour="' . esc_url( $turl . 'living-25' . $cd . '.jpg' . $tv ) . '" data-nlps-tour-small="' . esc_url( $turl . 'living-25' . $cd . '-2k.jpg' . $tv ) . '" data-nlps-tour-title="' . esc_attr( (string) ( $tc['card_title'] ?? 'קומה 25 · לכיוון הים' ) ) . '" data-nlps-tour-scenes="' . esc_attr( wp_json_encode( $scenes ) ) . '"><span>להיכנס לדירה · 360°</span></button>'
				. '<p class="nlat__note">הדמיית פנים להמחשה בלבד: החלוקה, הגמרים והנוף משוערים ואינם לפי תוכנית מכר.</p></div></section></div>';
		}
		return array( 'hero' => $hero, 'cta' => $cta, 'stagebox' => $stagebox, 'rail' => $rail, 'facts' => $facts, 'below' => $below, 'tour' => $tour, 'deals' => nadlan_ps_deals( $ps ) );
	}
}

if ( ! function_exists( 'nadlan_ps_compose' ) ) {
	/** The page top, composed on the finished HTML. Fails open: any missing anchor returns the page unchanged. */
	function nadlan_ps_compose( $html, $ps ) {
		if ( ! is_string( $html ) || false !== strpos( $html, 'id="nlps"' ) ) { return $html; }
		$b = strpos( $html, '<body' );
		if ( false === $b ) { return $html; }
		$a = strpos( $html, '<div class="nl-lead">', $b );
		if ( false === $a && function_exists( 'nadlan_pt_synth_lead' ) ) { // StageDuo v81: DUO's paragraph is the article's bottom line
			$sl = nadlan_pt_synth_lead( $html, $b );
			if ( false !== $sl ) {
				$html = $sl[0];
				$a    = strpos( $html, '<div class="nl-lead">', $b );
			}
		}
		if ( false === $a ) { return $html; }
		$lead_end = nadlan_ps_close( $html, $a, 'div' );
		if ( ! $lead_end ) { return $html; }
		// the area map leaves its place at the bottom: it comes back next to the view from the floor
		$map = '';
		if ( preg_match( '#<section\b[^>]*\bid="nlpjx-map"#', $html, $m, PREG_OFFSET_CAPTURE, $lead_end ) ) {
			$s = $m[0][1];
			$e = nadlan_ps_close( $html, $s, 'section' );
			if ( $e ) {
				$map  = substr( $html, $s, $e - $s );
				$html = substr( $html, 0, $s ) . substr( $html, $e );
			}
		}
		// the page's one h1 (printed for machines only) becomes the visible title before the lead
		$h1 = '';
		if ( preg_match( '#<h1\b[^>]*\bid="nl-project-page-title"[^>]*>(.*?)</h1>#s', $html, $m, PREG_OFFSET_CAPTURE, $b ) ) {
			$h1   = trim( wp_strip_all_tags( $m[1][0] ) );
			$html = substr( $html, 0, $m[0][1] ) . substr( $html, $m[0][1] + strlen( $m[0][0] ) );
			if ( $m[0][1] < $a ) { $a -= strlen( $m[0][0] ); $lead_end -= strlen( $m[0][0] ); }
		}
		$parts = nadlan_ps_parts( $ps, $h1, $map );
		if ( '' === $h1 && false === stripos( substr( $html, $b ), '<h1' ) ) { return $html; } // never leave the page without its h1
		// the price band's note pointed down to the map; the map is now above it (and "המפה החיה" is off the word list)
		$html = str_replace( 'כל המחירים, המוסדות והתוכניות - על המפה החיה למטה ←', 'כל המחירים, המוסדות והתוכניות על מפת האזור ←', $html );
		// the non-affiliation notice is not moved: the owner's order of 29.8.2026 keeps it out of the snippet zone, opening
		// the article section (inc/legal-notice.php), and the public-source audit checks exactly that. (1.72.259 had lifted
		// it under the facts, after the recipe's row 6; the audit caught it on 25.9.)
		// one grid (design system version 14): the text column, the stage and the rail share the first fold; the source
		// order stays title, lead, buttons, stage, rail, facts, view and map
		$lead = substr( $html, $a, $lead_end - $a );
		$page = '<div class="nlps-page' . ( ! empty( $ps['world'] ) ? ' nlps-page--world' : '' ) . '" dir="rtl" lang="he">' . $parts['hero'] . $lead . $parts['cta'] . ( $parts['prices'] ?? '' ) . $parts['stagebox'] . $parts['rail'] . $parts['facts'] . $parts['below'] . $parts['tour'] . $parts['deals'] . ( function_exists( 'nadlan_ps_world_film' ) ? nadlan_ps_world_film( $ps ) : '' ) . '</div>'; // v104.28: the film, after the deals, outside the post content
		$html = substr( $html, 0, $a ) . $page . substr( $html, $lead_end );
		// one FAQPage schema, from the page's own visible questions and answers (the recipe, row 25): the first
		// "שאלות נפוצות" section that really holds question and answer pairs
		$body = substr( $html, (int) strpos( $html, '<body' ) );
		if ( false === strpos( $html, '"FAQPage"' ) && preg_match_all( '#<h2[^>]*>\s*שאלות נפוצות[^<]*</h2>(.*?)(?=<h2|</article>|$)#su', $body, $secs ) ) {
			foreach ( $secs[1] as $sec ) {
				$qa = array();
				if ( preg_match_all( '#<h3[^>]*>(.*?)</h3>\s*<p[^>]*>(.*?)</p>#su', $sec, $pairs, PREG_SET_ORDER ) ) {
					foreach ( array_slice( $pairs, 0, 12 ) as $pr ) {
						$q   = trim( wp_strip_all_tags( $pr[1] ) );
						$ans = trim( wp_strip_all_tags( $pr[2] ) );
						if ( '' !== $q && '' !== $ans ) { $qa[] = array( '@type' => 'Question', 'name' => $q, 'acceptedAnswer' => array( '@type' => 'Answer', 'text' => $ans ) ); }
					}
				}
				if ( count( $qa ) >= 2 ) {
					$ld = '<script type="application/ld+json" id="nadlan-ps-faq">' . wp_json_encode( array( '@context' => 'https://schema.org', '@type' => 'FAQPage', 'mainEntity' => $qa ), JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES ) . '</script>';
					$hp = strpos( $html, '</head>' );
					if ( false !== $hp ) { $html = substr( $html, 0, $hp ) . $ld . "\n" . substr( $html, $hp ); }
					break;
				}
			}
		}
		return $html;
	}
}

/* KikarHamedinaWorld (design system v104, 30.9.2026, HAD-375): a project page on the SHARED world module
   (assets/project-stage/world/world.js, mountWorld) instead of a per-project stage.js copy. The page keeps the fleet's order
   (checklist C1-C8: the H1, the answer paragraph, the buttons, the stage, the map, the facts, the tools, the article); the world
   is one walkable scene of the whole area with four ways in (the aerial view, a walk, a tower's floor and view with the sun,
   what is nearby). Everything here runs only for a config with 'world' (Kikar Hamedina today): the four stage projects never
   reach it, so their pages stay byte for byte as they were. There is no bridge.js on these pages: the world draws its own view
   from the floor and sets window.__nlpsPick for the WhatsApp source line. The example apartment (P9c, design system v104.2)
   opens from the world's floor view (world/example.js and the fleet's 360 viewer, loaded on the press); there is no steps row. */
if ( ! function_exists( 'nadlan_ps_world_words' ) ) {
	/** The page top's own words in the page's language: Hebrew, English, French, Russian and Arabic (P8, 1.72.370). */
	function nadlan_ps_world_words( $lang ) {
		$w = array(
			'he' => array(
				'wa'    => 'לקבלת פרטים נוספים בוואטסאפ', // v104.31 (HAD-382): "ייעוץ חינם" only on the floating bar
				'wa_tx' => 'שלום, אשמח לפרטים נוספים על %s (nad-lan.co.il)',
				'sale'  => 'דירות למכירה במגדלים',
				'tour'  => 'סיור וירטואלי בכיכר',
				'stage' => 'סיור וירטואלי ב%s: המגדלים, הקומות והנוף',
				'hint'  => 'בחרו מגדל, קומה ודירה לפי כיוון, וראו את תוכנית הקומה, את מחירי העסקאות ואת הנוף מהחלונות. אפשר גם לצאת לסיור ברגל בכיכר ובפארק, ולגלות מה נמצא במרחק הליכה.',
				'facts' => 'עובדות בקצרה',
				'prog'  => 'שלב הפרויקט',
				'rail'  => 'אנשי מקצוע באזור',
			),
			'en' => array(
				'wa'    => 'More details on WhatsApp',
				'wa_tx' => 'Hello, I would like more details on %s (nad-lan.co.il)',
				'sale'  => 'Apartments for sale in the towers',
				'tour'  => 'Virtual tour of the square',
				'stage' => 'Virtual tour of %s: the towers, the floors and the view',
				'hint'  => 'Choose a tower, a floor and an apartment by its direction to see the floor plan, the deal prices and the view from its windows. Or take a walk around the square and the park, and discover what lies within walking distance.',
				'facts' => 'Key facts',
				'prog'  => 'Project stage',
				'rail'  => 'Professionals in the area',
			),
			// P8 (1.72.370): written for each reader, not word for word from the English
			'fr' => array(
				'wa'    => 'Plus de détails sur WhatsApp',
				'wa_tx' => 'Bonjour, je souhaite plus de détails sur les %s (nad-lan.co.il)',
				'sale'  => 'Appartements à vendre dans les tours',
				'tour'  => 'Visite virtuelle de la place',
				'stage' => 'Visite virtuelle des %s : les tours, les étages et la vue',
				'hint'  => 'Choisissez une tour, un étage et un appartement selon son orientation pour voir le plan de l’étage, les prix des ventes et la vue depuis ses fenêtres. Promenez-vous aussi sur la place et dans le parc, et découvrez tout ce qui se trouve à quelques pas.',
				'facts' => 'En bref',
				'prog'  => 'Avancement du projet',
				'rail'  => 'Professionnels du quartier',
			),
			'ru' => array(
				'wa'    => 'Подробнее в WhatsApp',
				'wa_tx' => 'Здравствуйте, хочу узнать подробнее о проекте «%s» (nad-lan.co.il)',
				'sale'  => 'Квартиры на продажу в башнях',
				'tour'  => 'Виртуальная прогулка по площади',
				'stage' => 'Виртуальная прогулка: %s, этажи и вид из окон',
				'hint'  => 'Выберите башню, этаж и квартиру по стороне света, чтобы увидеть план этажа, цены сделок и вид из её окон. Можно также прогуляться по площади и парку и узнать, что находится в шаговой доступности.',
				'facts' => 'Коротко о проекте',
				'prog'  => 'Этап проекта',
				'rail'  => 'Специалисты района',
			),
			'ar' => array(
				'wa'    => 'مزيد من التفاصيل عبر واتساب',
				'wa_tx' => 'مرحباً، أود الحصول على مزيد من التفاصيل حول %s (nad-lan.co.il)',
				'sale'  => 'شقق للبيع في الأبراج',
				'tour'  => 'جولة افتراضية في الميدان',
				'stage' => 'جولة افتراضية في %s: الأبراج والطوابق والإطلالة',
				'hint'  => 'اختاروا برجاً وطابقاً وشقة حسب اتجاهها لتروا مخطط الطابق وأسعار الصفقات والإطلالة من نوافذها. ويمكنكم أيضاً التجول سيراً في الميدان والحديقة واكتشاف كل ما يقع على مسافة قريبة.',
				'facts' => 'باختصار',
				'prog'  => 'مرحلة المشروع',
				'rail'  => 'مختصون في المنطقة',
			),
		);
		return isset( $w[ $lang ] ) ? $w[ $lang ] : $w['en'];
	}
}
if ( ! function_exists( 'nadlan_ps_world_media' ) ) {
	/** The world's first picture: a wide frame for screens over 700 px and an upright one for phones (the same scene). */
	function nadlan_ps_world_media( $ps ) {
		$base = 'assets/project-stage/' . $ps['dir'] . '/';
		$v    = '?ver=' . nadlan_ps_ver();
		$pw   = (array) ( $ps['world']['poster'] ?? array() );
		$wide = (string) ( $pw['wide'] ?? 'poster-1600' );
		$tall = (string) ( $pw['tall'] ?? 'poster-800' );
		return array(
			'jpg'  => plugins_url( $base . $wide . '.jpg', dirname( __FILE__ ) ) . $v,
			'wide' => plugins_url( $base . $wide . '.webp', dirname( __FILE__ ) ) . $v,
			'tall' => plugins_url( $base . $tall . '.webp', dirname( __FILE__ ) ) . $v,
			'w'    => (int) ( $pw['w'] ?? 1600 ),
			'h'    => (int) ( $pw['h'] ?? 1000 ),
			'tw'   => (int) ( $pw['tw'] ?? 800 ),
		);
	}
}
if ( ! function_exists( 'nadlan_ps_world_parts' ) ) {
	/** The pieces of a world page's top, in the same keys as nadlan_ps_parts(); $h1 is the page's own h1 text. */
	function nadlan_ps_world_parts( $ps, $h1, $map ) {
		$lang = (string) ( $ps['lang'] ?? 'he' );
		$he   = 'he' === $lang;
		$tl   = in_array( $lang, array( 'he', 'en', 'fr', 'ru', 'ar' ), true ) ? $lang : 'en'; // P8 (1.72.370): fr, ru and ar speak their own language
		$L    = $he ? $ps : array_merge( $ps, (array) ( $ps['i18n'][ $lang ] ?? ( $ps['i18n']['en'] ?? array() ) ) );
		$T    = nadlan_ps_world_words( $tl );
		$la   = ' dir="' . ( in_array( $lang, array( 'he', 'ar' ), true ) ? 'rtl' : 'ltr' ) . '" lang="' . esc_attr( $lang ) . '"';
		$wa   = function_exists( 'nadlan_cta_whatsapp_number' ) ? preg_replace( '/\D/', '', (string) nadlan_cta_whatsapp_number() ) : '';
		$name = (string) $L['name'];
		$link = '' !== $wa ? 'https://wa.me/' . $wa . '?text=' . rawurlencode( sprintf( $T['wa_tx'], $name ) ) : '';
		$m    = nadlan_ps_world_media( $ps );
		$v    = '?ver=' . nadlan_ps_ver();
		$base = 'assets/project-stage/' . $ps['dir'] . '/';
		$pw   = (array) $ps['world'];
		$alt  = (string) ( $L['poster_alt'] ?? $name );
		$cfg  = array(
			'world'  => plugins_url( 'assets/project-stage/world/world.js', dirname( __FILE__ ) ) . $v,
			'data'   => plugins_url( $base . (string) ( $pw['data'] ?? 'world.json' ), dirname( __FILE__ ) ) . $v,
			'places' => is_readable( dirname( __DIR__ ) . '/' . $base . 'places.json' ) ? plugins_url( $base . 'places.json', dirname( __FILE__ ) ) . $v : '',
			'lang'   => $tl,
			'name'   => $name,
			'wa'     => $link,
			'mode'   => (string) ( $pw['mode'] ?? 'aerial' ),
			'season' => (int) ( $pw['season'] ?? 9 ),
			'hour'   => (int) ( $pw['hour'] ?? 10 ),
			'pond'   => ! array_key_exists( 'pond', $pw ) || ! empty( $pw['pond'] ),
			// P9c (v104.2): which tower, floors and side have an example apartment; its manifest loads only on the press
			'examples' => ! empty( $pw['examples'] ) && is_readable( dirname( __DIR__ ) . '/' . $base . 'tour/examples.json' )
				? array( 'url' => plugins_url( $base . 'tour/examples.json', dirname( __FILE__ ) ) . $v, 'list' => array_values( (array) $pw['examples'] ) ) : null,
			'poster' => array( 'src' => $m['jpg'], 'srcset' => $m['tall'] . ' ' . $m['tw'] . 'w, ' . $m['wide'] . ' ' . $m['w'] . 'w', 'sizes' => '(max-width:700px) 228px, 70vw' /* v104.45 (HAD-421): phones pick the 800 file the page's picture already loaded */, 'alt' => $alt ),
		);
		$hero = '';
		$cta  = '';
		if ( '' !== $h1 ) {
			$en   = (string) ( $ps['name_en'] ?? '' );
			$hero = '<header class="nlds nlps-herowrap"' . $la . '><div class="nlps-hero">'
				. ( $he
					? '<h1 id="nl-project-page-title" class="nlps-h1">' . esc_html( (string) ( $ps['h1_he'] ?? $ps['name'] ) ) . ( '' !== $en ? ' <span class="nlps-h1__en" lang="en">' . esc_html( $en ) . '</span>' : '' ) . '</h1>'
					: '<h1 id="nl-project-page-title" class="nlps-h1">' . esc_html( $h1 ) . '</h1>' ) // the language page's own title
				. ( ! empty( $L['developer'] ) || ! empty( $L['place'] ) ? '<div class="nlps-kicker">' . ( ! empty( $L['developer'] ) ? '<b>' . esc_html( $L['developer'] ) . '</b>' : '' ) . ( ! empty( $L['developer'] ) && ! empty( $L['place'] ) ? ' · ' : '' ) . esc_html( (string) ( $L['place'] ?? '' ) ) . '</div>' : '' )
				. '</div></header>';
			// the design's three buttons: free advice on WhatsApp (one tap), the apartments for sale, the virtual tour
			$cta  = '<div class="nlds nlps-ctawrap"' . $la . '><div class="nlps-hero__cta">'
				. ( '' !== $wa ? '<a class="nlds-btn nlds-btn--primary" target="_blank" rel="noopener" data-nlps-ev="hero-wa" href="https://wa.me/' . esc_attr( $wa ) . '?text=' . rawurlencode( sprintf( $T['wa_tx'], $name ) ) . '">' . ( function_exists( 'nlds_icon' ) ? nlds_icon( 'whatsapp' ) : '' ) . '<span>' . esc_html( $T['wa'] ) . '</span></a>' : '' )
				. '<a class="nlds-btn nlds-btn--secondary" href="#nlws-sale" data-nlps-ev="hero-sale"><span>' . esc_html( $T['sale'] ) . '</span></a>'
				. '<a class="nlds-btn nlds-btn--secondary" href="#nlps-t" data-nlps-ev="hero-world"><span>' . esc_html( $T['tour'] ) . '</span></a>'
				. '</div></div>';
		}
		// the first picture, painted with the page (a wide frame, an upright one on phones); the world adopts the same files
		$pic = '<picture class="nlps-ssr-pic"><source media="(max-width:700px)" type="image/webp" srcset="' . esc_url( $m['tall'] ) . '"><source type="image/webp" srcset="' . esc_url( $m['wide'] ) . '">'
			. '<img class="nlps-ssr-poster" src="' . esc_url( $m['jpg'] ) . '" width="' . (int) $m['w'] . '" height="' . (int) $m['h'] . '" alt="' . esc_attr( $alt ) . '" fetchpriority="high" decoding="async"></picture>';
		$src = ! empty( $L['src_line'] ) ? '<p class="nlps-src">' . wp_kses( (string) $L['src_line'], array( 'span' => array() ) ) . '</p>' : '';
		$stagebox = '<div class="nlps-stagebox"><h2 class="nlps-srt" id="nlps-t">' . esc_html( sprintf( $T['stage'], $name ) ) . '</h2>'
			. '<section class="nlps-stage nlps-stage--world" id="nlps" aria-labelledby="nlps-t" data-cfg="' . esc_attr( wp_json_encode( $cfg ) ) . '"><div class="nlps-stage__mount" id="nlps-stage">' . $pic . '</div></section>'
			. '<div class="nlds"' . $la . '><p class="nlps-hint" id="nlps-hint">' . esc_html( $T['hint'] ) . '</p>' . $src . '</div></div>';
		$rail = '';
		foreach ( (array) ( $ps['rail'] ?? array() ) as $pid ) { $rail .= nadlan_ps_square( $pid, $ps ); }
		if ( $he ) { $rail .= nadlan_ps_slot(); }
		$rail = '' !== $rail ? '<aside class="nlps-rail" aria-label="' . esc_attr( $T['rail'] ) . '">' . $rail . '</aside>' : '';
		$facts = '';
		if ( ! empty( $L['facts'] ) || ! empty( $L['progress'] ) ) {
			$facts = '<div class="nlds nlps-factswrap"' . $la . '>';
			if ( ! empty( $L['facts'] ) ) {
				$facts .= '<div class="nlpf" role="list" aria-label="' . esc_attr( $T['facts'] ) . '">';
				foreach ( (array) $L['facts'] as $f ) {
					$facts .= '<div class="nlpf__item" role="listitem"><p class="nlpf__k">' . esc_html( $f[0] ) . '</p><p class="nlpf__v">' . esc_html( $f[1] ) . '</p>' . ( ! empty( $f[2] ) ? '<p class="nlpf__s">' . esc_html( $f[2] ) . '</p>' : '' ) . '</div>';
				}
				$facts .= '</div>';
			}
			if ( ! empty( $L['progress'] ) ) {
				$facts .= '<ol class="nlprog" aria-label="' . esc_attr( $T['prog'] ) . '">';
				foreach ( (array) $L['progress'] as $st ) {
					$cls = 'done' === $st[2] ? ' is-done' : ( 'now' === $st[2] ? ' is-now' : '' );
					$facts .= '<li class="nlprog__step' . $cls . '"' . ( 'now' === $st[2] ? ' aria-current="step"' : '' ) . '><b>' . esc_html( $st[0] ) . '</b>' . esc_html( $st[1] ) . '</li>';
				}
				$facts .= '</ol>';
			}
			$facts .= '</div>';
		}
		// one map on the page (the recipe, row 18): the area map, right under the world; the view from a floor is in the world itself
		$below = '' !== $map ? '<div class="nlps-below nlps-below--solo">' . $map . '</div>' : '';
		return array( 'hero' => $hero, 'cta' => $cta, 'prices' => ( $he && function_exists( 'nadlan_pg_render' ) ) ? nadlan_pg_render( $ps, $wa ) : '', // PriceGuide v1
			'stagebox' => $stagebox, 'rail' => $rail, 'facts' => $facts, 'below' => $below, 'tour' => '', 'deals' => $he ? nadlan_ps_deals( $ps ) : '' );
	}
}
if ( ! function_exists( 'nadlan_ps_world_head' ) ) {
	/** The world page's head: the first picture, fetched at once (the phone's or the wide one); three.js waits for intent. */
	function nadlan_ps_world_head( $ps ) {
		$m = nadlan_ps_world_media( $ps );
		echo '<link rel="preload" as="image" type="image/webp" href="' . esc_url( $m['tall'] ) . '" media="(max-width:700px)" fetchpriority="high">' . "\n";
		echo '<link rel="preload" as="image" type="image/webp" href="' . esc_url( $m['wide'] ) . '" media="(min-width:701px)" fetchpriority="high">' . "\n";
		// v104.47 (HAD-421): the world's three biggest files start at once, at low priority, so the network is never idle while
		// the page paints; mount() still runs on intent and finds them in the cache (the same URLs as the stage's data-cfg)
		$v    = '?ver=' . nadlan_ps_ver();
		$base = 'assets/project-stage/' . $ps['dir'] . '/';
		$pw   = (array) $ps['world'];
		echo '<link rel="modulepreload" href="https://cdn.jsdelivr.net/npm/three@0.170.0/build/three.module.js" crossorigin fetchpriority="low">' . "\n";
		echo '<link rel="modulepreload" href="' . esc_url( plugins_url( 'assets/project-stage/world/world.js', dirname( __FILE__ ) ) . $v ) . '" fetchpriority="low">' . "\n";
		echo '<link rel="preload" as="fetch" href="' . esc_url( plugins_url( $base . (string) ( $pw['data'] ?? 'world.json' ), dirname( __FILE__ ) ) . $v ) . '" crossorigin fetchpriority="low">' . "\n";
	}
}
if ( ! function_exists( 'nadlan_ps_world_script' ) ) {
	/** The world on the page: mountWorld() once the page has painted (idle after load); the 3D itself starts when the stage is
	 *  in view or on the tour button. The consult links in the page's text (#nlws-wa) open the same WhatsApp message. */
	function nadlan_ps_world_script( $ps ) {
		$js = <<<'NLWJS'
const root = document.getElementById('nlps'), host = document.getElementById('nlps-stage');
let c = {};
try { c = JSON.parse((root && root.dataset.cfg) || '{}'); } catch (e) { c = {}; }
const ga = (n, p) => { try { if (window.nadlanGA) window.nadlanGA(n, Object.assign({ project: c.name || '' }, p || {})); } catch (e) { /* none */ } };
let P = null;
function mount() {
  if (P) return P;
  P = import(c.world).then((m) => {
    const w = m.mountWorld(host, { dataUrl: c.data, placesUrl: c.places || null, lang: c.lang, name: c.name, wa: c.wa || null, poster: c.poster,
      intent: 'visible', mode: c.mode, season: c.season, hour: c.hour, pond: c.pond !== false, examples: c.examples || null });
    window.__nlpsWorld = w;
    // the page's own first picture steps aside once the world's copy of it (the same files) is painted
    const own = host.querySelector('.nlps-ssr-pic'), wp = host.querySelector('.nlw-poster');
    const drop = () => { if (own && own.parentNode) own.remove(); };
    if (wp && wp.decode) wp.decode().then(drop, () => setTimeout(drop, 1500)); else setTimeout(drop, 1500);
    return w;
  }).catch((e) => { console.warn('[world]', e); P = null; return null; });
  return P;
}
if (root && host && c.world) {
  const later = () => ('requestIdleCallback' in window ? requestIdleCallback(mount, { timeout: 2000 }) : setTimeout(mount, 200));
  // v104.51 (HAD-421, A/B): ?nlwboot=early mounts once the document is parsed (this module runs before DOMContentLoaded)
  // instead of after window load; without the switch the default below is unchanged until the A/B is measured
  if (/[?&]nlwboot=early(&|$)/.test(location.search)) { if ('requestIdleCallback' in window) requestIdleCallback(mount, { timeout: 600 }); else setTimeout(mount, 0); }
  else if (document.readyState === 'complete') later(); else addEventListener('load', later, { once: true });
  document.addEventListener('click', (e) => {
    const a = e.target && e.target.closest ? e.target.closest('[data-nlps-ev="hero-world"],[data-nlps-ev="hero-sale"]') : null;
    if (!a) return;
    const ev = a.getAttribute('data-nlps-ev');
    ga('stage_step', { step: ev });
    if (ev !== 'hero-world') return;
    // the whole world in view, its foot at the screen's foot (clear of the site's sticky header), then the walk
    e.preventDefault();
    root.scrollIntoView({ block: 'end', behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth' });
    mount().then((w) => { if (w) w.setMode('walk', 'user'); });
  });
  if (c.wa) for (const a of document.querySelectorAll('a[href="#nlws-wa"]')) { a.href = c.wa; a.target = '_blank'; a.rel = 'noopener'; }
  addEventListener('nl:floor', (e) => { const d = e.detail || {}; if (d.source === 'user') ga('stage_floor', { tower: d.tower, floor: d.floor }); });
  addEventListener('nl:facing', (e) => { const d = e.detail || {}; if (d.source === 'user') ga('stage_facing', { tower: d.tower, floor: d.floor, facing: d.facing }); });
  addEventListener('nl:example', (e) => { const d = e.detail || {}; if (d.open) ga('stage_example', { tower: d.tower, floor: d.floor, facing: d.facing, example: d.id }); });
  /* AccessibleCorner (design system v104.2, P9c): the accessibility button (inc/accessibility.php) keeps its bottom corner (the
     owner, 25.9.2026). On this page the world's tab bar and sheet, and the page top's buttons, pass under that corner as the
     visitor scrolls (the first tab "מבט על" on the Hebrew phone's first screen); there the button takes the nearest free place
     above its corner, in its own column, and comes back when the corner is free. It never moves onto the answer paragraph: with no
     free place clear of it, it stays in its corner. It measures from its corner (its own lift is taken out), so it never
     flickers; while its panel is open it does not move. */
  (() => {
    const box = document.getElementById('nla11y'), btn = document.getElementById('nla11y-btn');
    if (!box || !btn) return;
    const CTRL = '.nlps-hero__cta a,#nlps .nlw-top button,#nlps .nlw-panel button,#nlps .nlw-panel input,#nlps .nlw-panel a,#nlps .nlw-card button,#nlps .nlw-card a,#nlps .nlw-compass button,#nlps .nlw-enter,#nlps summary';
    let lift = 0, raf = 0;
    const fit = () => {
      raf = 0;
      const pan = document.getElementById('nla11y-panel');
      if (pan && !pan.hidden) return; if (getComputedStyle(document.body).getPropertyValue('--nlcta-band').trim() === '1') { if (lift) { lift = 0; box.style.transform = ''; } return; } // ConsultBand (v104.25): the band at the foot holds the button
      if (document.querySelector('#nlps .nlw--full')) return; // the world fills the screen above the page: nothing to clear
      const r = btn.getBoundingClientRect();
      if (!r.width) return;
      const h = r.height, t0 = r.top + lift, l = r.left - 6, rr = r.right + 6, vh = innerHeight;
      const col = (q) => q.height && q.right > l && q.left < rr && q.bottom > 0 && q.top < vh;
      const hard = [...document.querySelectorAll(CTRL)].map((e) => e.getBoundingClientRect()).filter(col).map((q) => [q.top - 8, q.bottom + 8]);
      const soft = [...document.querySelectorAll('.nl-lead')].map((e) => e.getBoundingClientRect()).filter(col).map((q) => [q.top - 4, q.bottom + 4]);
      const hit = (t, L) => L.some(([a, b]) => t < b && t + h > a);
      let best = 0;
      if (hit(t0, hard)) {
        best = 0;
        for (let d = 4; d <= vh * 0.5; d += 4) { const t = t0 - d; if (t < 76) break; if (!hit(t, hard)) { best = hit(t, soft) ? 0 : d; break; } }
      }
      if (best !== lift) { lift = best; box.style.transform = lift ? 'translateY(' + (-lift) + 'px)' : ''; }
    };
    const ask = () => { if (!raf) raf = requestAnimationFrame(fit); };
    box.style.transition = matchMedia('(prefers-reduced-motion: reduce)').matches ? '' : 'transform .18s ease';
    addEventListener('scroll', ask, { passive: true });
    addEventListener('resize', ask);
    for (const ev of ['nl:floor', 'nl:facing', 'nl:example', 'load']) addEventListener(ev, ask);
    document.addEventListener('click', () => setTimeout(ask, 80), true);
    setTimeout(ask, 1200); setTimeout(ask, 3000);
    ask();
  })();
}
NLWJS;
		return "\n" . '<script type="module" id="nadlan-ps-world">' . "\n" . $js . '</script>' . "\n";
	}
}
/* The world page's own layout and the style of its text sections (.nlws: the facts table, the prices, when it is ready, the
   timeline, the park, the square, the transport and the FAQ in the post's content), after the stage pages' layout. */
add_action( 'wp_head', function () {
	$ps = nadlan_ps_current();
	if ( ! $ps || empty( $ps['world'] ) ) { return; }
	$pc = 'html body.nlpc-project-page .nlpc-main .wp-block-post-content.is-layout-constrained > section.nlws';
	echo '<style id="nadlan-ps-world-css">'
		// the first fold: the text column and the world side by side (no rail column: the world needs the width); the
		// professionals' square goes to the end of the page top
		. ':root body .nlps-page.nlps-page--world{grid-template-columns:minmax(300px,380px) minmax(0,1fr);grid-template-areas:"hero stage" "lead stage" "cta stage" "prices prices" "below below" "facts facts" "deals deals" "rail rail"}'
		. ':root body .nlps-page--world>.nlps-rail{grid-template-columns:repeat(auto-fill,minmax(240px,320px));margin-top:6px!important}'
		. ':root body .nlps-page--world .nlps-stage--world{height:clamp(560px,calc(100svh - 190px),760px)}'
		. ':root body .nlps-stage--world .nlps-ssr-pic{position:absolute;inset:0;display:block}'
		. ':root body .nlps-stage--world .nlps-ssr-poster{object-position:50% 50%}'
		. ':root body .nlps-stage--world .nlw:not(.nlw--full){background:transparent}'
		. ':root body .nlps-page--world .nlds .nlps-hint{margin:10px 0 0}'
		. ':root body .nlps-page--world #nlps-t,:root body section.nlws{scroll-margin-top:120px}'
		. '@media(max-width:1099px){:root body .nlps-page.nlps-page--world{grid-template-columns:minmax(0,1fr);grid-template-areas:"hero" "lead" "cta" "stage" "prices" "below" "facts" "deals" "rail"}:root body .nlps-page--world .nlps-stage--world{height:68svh;min-height:440px}}'
		. '@media(max-width:600px){:root body .nlps-page--world .nlps-stage--world{height:72svh;min-height:460px}}'
		// PhoneFirstScreen (design system v104.1, P9a): on phones a landing lane (50px + the grid's gap) between the page top's
		// buttons and the world. The WhatsApp bar (50px, 10px clear on each side of it) parks there while the world's tab bar passes
		// its resting place, instead of rising onto the third button ("סיור וירטואלי בכיכר"); conversion-cta.php counts the page
		// top's buttons as controls and takes the free place nearest the bar's resting place
		. '@media(max-width:600px){:root body .nlps-page--world>.nlps-stagebox{margin-top:50px!important}}'
		// ArabicFirstScreen (design system v104.2, P9c): the Arabic answer paragraph is about three lines longer, so on a phone its
		// buttons sat where the WhatsApp bar rests and the bar rose onto the paragraph's last lines. A 50px lane above the buttons:
		// the bar, blocked by them, parks between the paragraph and the buttons, clear of both
		. '@media(max-width:600px){:root body .nlps-page--world .nlps-ctawrap[lang="ar"]{margin-top:50px!important}}'
		// the text sections: a reading column, tables as spec sheets with the source under each value, the timeline, the FAQ
		. $pc . '{max-width:min(880px,calc(100% - 24px))!important;margin:0 auto 36px!important;padding:0 16px!important;box-sizing:border-box}'
		. ':root body .nlws h2{margin:0 0 10px!important;font:600 clamp(22px,2.4vw,28px)/1.25 "Noto Serif Hebrew","Frank Ruhl Libre",Georgia,serif!important;color:#1B1A17!important;text-wrap:balance}'
		. ':root body .nlws h3{margin:18px 0 6px!important;font:600 18px/1.4 Heebo,Assistant,sans-serif!important;color:#1B1A17!important}'
		. ':root body .nlws p{max-width:none!important;margin:0 0 12px!important;font-size:16px!important;line-height:1.75!important;color:#2A2823}'
		. ':root body .nlws p.nlws-k{margin:0 0 4px!important;font:700 12.5px/1.4 Heebo,Assistant,sans-serif!important;letter-spacing:.06em;color:#8A6A2E!important}'
		. ':root body .nlws p.nlws-note{font-size:13.5px!important;line-height:1.6!important;color:#6B6558!important}'
		. ':root body .nlws a{color:#6B4E1E;text-underline-offset:3px}'
		. ':root body .nlws table{width:100%!important;margin:12px 0 20px!important;background:#fff!important;border:1px solid #E2DCD0!important;border-radius:16px!important;border-collapse:separate!important;border-spacing:0!important;overflow:hidden!important;box-shadow:0 1px 2px rgba(27,26,23,.04)!important}'
		. ':root body .nlws table :is(th,td){padding:12px 16px!important;background:none!important;border:0!important;border-top:1px solid #EFE9DD!important;text-align:start!important;vertical-align:top!important;font-size:15px!important;line-height:1.6!important;color:#1B1A17!important}'
		. ':root body .nlws table tr:first-child>:is(th,td){border-top:0!important}'
		. ':root body .nlws table thead th{background:#FAF7F1!important;font-size:12.5px!important;font-weight:700!important;color:#8A6A2E!important}'
		. ':root body .nlws table thead+tbody tr:first-child>:is(th,td){border-top:1px solid #E2DCD0!important}'
		. ':root body .nlws table tbody th{width:28%!important;font-size:13.5px!important;font-weight:700!important;color:#8A6A2E!important}'
		. ':root body .nlws table td small{display:block!important;margin-top:3px!important;font-size:12.5px!important;font-weight:400!important;line-height:1.5!important;color:#6B6558!important}'
		. ':root body .nlws ol.nlws-time{list-style:none!important;margin:14px 0 20px!important;padding:0!important;border-inline-start:2px solid #E2DCD0}'
		. ':root body .nlws ol.nlws-time li{position:relative;margin:0 0 14px!important;padding:0 18px!important;font-size:15.5px;line-height:1.6;color:#2A2823}'
		. ':root body .nlws ol.nlws-time li::before{content:"";position:absolute;inset-inline-start:-7px;top:6px;width:12px;height:12px;border-radius:50%;background:#FAF7F1;border:2px solid #9C7A3C;box-sizing:border-box}'
		. ':root body .nlws ol.nlws-time li.is-now::before{background:#9C7A3C}'
		. ':root body .nlws ol.nlws-time li b{display:block;font-size:13.5px;color:#8A6A2E;font-weight:700}'
		. ':root body .nlws ul.nlws-list{margin:8px 0 16px!important;padding-inline-start:20px!important}:root body .nlws ul.nlws-list li{margin:0 0 6px!important;font-size:15.5px;line-height:1.65}'
		. ':root body .nlws a.nlws-wa{display:inline-flex;align-items:center;justify-content:center;min-height:46px;padding:0 22px;border-radius:999px;background:#0F7A63;color:#fff!important;font:700 15.5px/1 Heebo,Assistant,sans-serif;text-decoration:none!important;margin:4px 0 8px}'
		. ':root body .nlws.nlws-faq h3{margin:0!important;padding-top:18px!important;border-top:1px solid #E2DCD0!important}'
		. ':root body .nlws.nlws-faq h2+h3{padding-top:6px!important;border-top:0!important}'
		. ':root body .nlws.nlws-faq h3+p{margin:6px 0 18px!important}'
		. '@media(max-width:600px){'
		. ':root body .nlws table{display:block!important;padding:2px 14px!important}:root body .nlws table :is(thead,tbody){display:block!important}'
		. ':root body .nlws table tr{display:grid!important;grid-template-columns:minmax(0,1fr)!important;gap:2px!important;margin:0!important;padding:11px 0!important;background:none!important;border:0!important;border-top:1px solid #EFE9DD!important;border-radius:0!important;box-shadow:none!important}'
		. ':root body .nlws table :is(thead,tbody) tr:first-child,:root body .nlws table thead+tbody tr:first-child{border-top:0!important}'
		. ':root body .nlws table thead+tbody tr:first-child>:is(th,td){border-top:0!important}'
		// a row of three or more cells: its first cell a heading line, the others two by two (ProjectDossier v67's phone rows)
		. ':root body .nlws table tr:has(>:nth-child(3)){grid-template-columns:minmax(0,1fr) minmax(0,1fr)!important;gap:4px 14px!important}'
		. ':root body .nlws table tr:has(>:nth-child(3))>:first-child{grid-column:1/-1!important;font-weight:700!important}'
		. ':root body .nlws table :is(th,td){display:block!important;width:auto!important;padding:0!important;border:0!important;border-bottom:0!important;font-size:14.5px!important}'
		. ':root body .nlws table thead{display:none!important}'
		. ':root body .nlws p{font-size:15.5px!important}}'
		. '</style>' . "\n";
	// P9a (1.72.371): the Russian page's Cyrillic in the house type. The site's faces have no Cyrillic, so Russian fell back to the
	// system's (Segoe UI, Georgia, Arial). Each family gains the Cyrillic of its own design family: Assistant's Latin is Source Sans,
	// Noto Serif Hebrew's is Noto Serif, Heebo's is Roboto; Frank Ruhl Libre takes Noto Serif too (Google Fonts, SIL Open Font
	// License). The same weights the site declares (a weight the site does not declare would take the Latin with it); only the
	// Cyrillic range is fetched, and only when Cyrillic is on screen (unicode-range); only on this page; font-display swap.
	if ( 'ru' === (string) ( $ps['lang'] ?? '' ) ) {
		$cyr = 'U+0301,U+0400-045F,U+0490-0491,U+04B0-04B1,U+2116';
		$gs  = 'https://fonts.gstatic.com/s/';
		$fam = array(
			'Assistant'         => array( $gs . 'sourcesans3/v19/nwpStKy2OAdR1K-IwhWudF-R3wsaZfrc.woff2', array( 300, 400, 600, 700 ) ),
			'Noto Serif Hebrew' => array( $gs . 'notoserif/v33/ga6daw1J5X9T9RW6j9bNVls-hfgvz8JcMofYTYf-D33Esw.woff2', array( 500, 600, 700 ) ),
			'Heebo'             => array( $gs . 'roboto/v51/KFO7CnqEu92Fr1ME7kSn66aGLdTylUAMa3iUBGEe.woff2', array( 300, 400, 500, 700 ) ),
			'Frank Ruhl Libre'  => array( $gs . 'notoserif/v33/ga6daw1J5X9T9RW6j9bNVls-hfgvz8JcMofYTYf-D33Esw.woff2', array( 400, 500, 700, 900 ) ),
		);
		$css = '';
		foreach ( $fam as $name => $f ) {
			foreach ( $f[1] as $wt ) {
				$css .= "@font-face{font-family:'" . $name . "';font-style:normal;font-weight:" . (int) $wt . ';font-display:swap;src:url(' . $f[0] . ") format('woff2');unicode-range:" . $cyr . '}';
			}
		}
		echo '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>' . "\n" . '<style id="nadlan-ps-world-cyr">' . $css . '</style>' . "\n";
	}
}, 1000 );

/* The visible H1 of a project page without a stage (design system ProjectTitle, version 39; Linear HAD-332; checklist C1).
   On these pages the one H1 was printed for screen readers only, after the answer paragraph, the prices and the notice.
   Here it becomes visible, with the same text, and moves right before the answer paragraph. Fails open: no paragraph or
   no H1 leaves the page exactly as it was. */
if ( ! function_exists( 'nadlan_pt_on' ) ) {
	function nadlan_pt_on() {
		static $on = null;
		if ( null !== $on ) { return $on; }
		$on = false;
		if ( is_admin() || ! is_singular( 'nadlan_project' ) || nadlan_ps_current() ) { return $on; } // Rainbow has its own hero
		$id = (int) get_queried_object_id();
		if ( ! $id || post_password_required( $id ) || get_post_meta( $id, '_nadlan_private_unit_journey', true ) ) { return $on; }
		// ProjectTitle v50 (28.9.2026): showroom pages (Aurelia, DUO) and the language pages too; the compose fails open
		return $on = true;
	}
}
if ( ! function_exists( 'nadlan_pt_synth_lead' ) ) {
	/** ProjectTitle v50: no answer paragraph (DUO), but the article's "שורה תחתונה": its words, as they are, right after the
	 *  breadcrumbs; the article keeps every word. Returns array( $html, $lead_offset ) or false (the page stays as it is).
	 *  Used by the title compose and, from StageDuo v81, by the stage compose on a stage page with no paragraph of its own. */
	function nadlan_pt_synth_lead( $html, $b ) {
		if ( ! preg_match( '#<div class="bottom-line">(.*?)</div>#s', $html, $bl, PREG_OFFSET_CAPTURE, $b ) ) { return false; }
		$txt = trim( preg_replace( '/\s+/u', ' ', wp_strip_all_tags( preg_replace( '#<strong>\s*שורה תחתונה:?\s*</strong>#u', '', $bl[1][0] ) ) ) );
		$nav = strpos( $html, '<nav class="nlptop"', $b );
		$end = false === $nav ? false : strpos( $html, '</nav>', $nav );
		if ( mb_strlen( $txt ) < 60 || false === $end ) { return false; }
		$end += 6;
		// the article's block, now the answer at the top, is not shown a second time a screen below (it stays in the source)
		$html = substr( $html, 0, $bl[0][1] ) . '<div class="bottom-line" data-nl-lead="1">' . substr( $html, $bl[0][1] + strlen( '<div class="bottom-line">' ) );
		$html = substr( $html, 0, $end ) . '<div class="nl-lead"><p>' . esc_html( $txt ) . '</p></div>' . substr( $html, $end );
		return array( $html, $end );
	}
}
if ( ! function_exists( 'nadlan_pt_compose' ) ) {
	function nadlan_pt_compose( $html ) {
		if ( ! is_string( $html ) || false !== strpos( $html, 'class="nlpt-h1"' ) ) { return $html; }
		$b = strpos( $html, '<body' );
		if ( false === $b ) { return $html; }
		$lead = strpos( $html, '<div class="nl-lead">', $b );
		if ( false === $lead ) {
			$sl = nadlan_pt_synth_lead( $html, $b );
			if ( false === $sl ) { return $html; }
			list( $html, $lead ) = $sl;
		}
		if ( ! preg_match( '#<h1\b[^>]*\bid="nl-project-page-title"[^>]*>(.*?)</h1>#s', $html, $m, PREG_OFFSET_CAPTURE, $b ) ) { return $html; }
		$text = trim( $m[1][0] );
		if ( '' === $text ) { return $html; }
		$h1 = '<h1 id="nl-project-page-title" class="nlpt-h1">' . $text . '</h1>';
		$at = $m[0][1];
		$len = strlen( $m[0][0] );
		if ( $at > $lead ) {
			$html = substr( $html, 0, $at ) . substr( $html, $at + $len ); // out of its place after the paragraph
			$html = substr( $html, 0, $lead ) . $h1 . substr( $html, $lead ); // in, right before it
		} else {
			$html = substr( $html, 0, $at ) . substr( $html, $at + $len );
			$lead -= $len;
			$html = substr( $html, 0, $lead ) . $h1 . substr( $html, $lead );
		}
		return $html;
	}
}
add_action( 'template_redirect', function () {
	if ( ! nadlan_pt_on() ) { return; }
	ob_start( function ( $html ) {
		try {
			return nadlan_pt_compose( $html );
		} catch ( \Throwable $e ) {
			return $html;
		}
	} );
}, 0 );
add_action( 'wp_head', function () {
	if ( ! nadlan_pt_on() ) { return; }
	echo '<style id="nadlan-pt-css">:root body h1.nlpt-h1{font-family:"Frank Ruhl Libre","Noto Serif Hebrew",Georgia,serif!important;font-weight:600!important;font-size:34px!important;line-height:1.15!important;color:#14212b!important;margin:18px 0 12px!important;padding:0 26px!important;box-sizing:border-box;text-wrap:balance;text-align:start!important;letter-spacing:-.01em;max-width:none!important}'
		. ':root body .bottom-line[data-nl-lead]{display:none!important}'
		. '@media(max-width:760px){:root body h1.nlpt-h1{font-size:27px!important;margin:14px 0 10px!important;padding:0 16px!important}}</style>' . "\n";
}, 999 );

/* The project page checklist, where a person editing a project meets it (the owner, 27.9.2026: "inject it where everyone
   working on the project meets it"). The full list: docs/checklists/PROJECT-PAGE-CHECKLIST.md in the repository. */
add_action( 'add_meta_boxes', function () {
	add_meta_box( 'nadlan-ps-checklist', 'צ׳קליסט עמוד פרויקט: התוכן קודם', function () {
		$rows = array(
			'כותרת H1 אחת: שם הפרויקט בעברית ובאנגלית.',
			'מיד אחריה פסקת התשובה (4-7 שורות): השם, היזם, המקום המדויק, המצב, התמהיל, מחיר אמיתי עם מקור ותאריך.',
			'הסדר בכל מסך, גם בטלפון: כותרת, פסקה, כפתורים, הבמה, הנוף והמפה, העובדות, המאמר. שום דבר טכני לפני הפסקה.',
			'הבמה מיד אחרי הפסקה, לא בסוף העמוד. המפה צמודה מתחת לבמה.',
			'נתוני שיווק כפי שפורסמו, עם המקור. לא ממציאים מלאי, מחיר, כיוון או תוכנית. הדמיה מסומנת "להמחשה".',
			'המאמר המלא נשאר אחרי הכלים ולא מתקצר.',
			'כל שינוי חזותי עובר קודם ב-Claude Design.',
		);
		echo '<ol style="margin:0 18px 8px 0;padding:0;line-height:1.5">';
		foreach ( $rows as $r ) { echo '<li style="margin:0 0 6px">' . esc_html( $r ) . '</li>'; }
		echo '</ol><p style="margin:0"><a href="' . esc_url( 'https://github.com/The-new-ben/nad-lan-co-il/blob/claude/production-truth-1.72.212/docs/checklists/PROJECT-PAGE-CHECKLIST.md' ) . '" target="_blank" rel="noopener">הצ׳קליסט המלא</a></p>';
	}, 'nadlan_project', 'side', 'high' );
} );

/* An outer output buffer: started before catalog-plus's (template_redirect priority 1), so it runs after it. */
add_action( 'template_redirect', function () {
	$ps = nadlan_ps_current();
	if ( ! $ps ) { return; }
	ob_start( function ( $html ) use ( $ps ) {
		try {
			return nadlan_ps_compose( $html, $ps );
		} catch ( \Throwable $e ) {
			return $html;
		}
	} );
}, 0 );

/* three.js by the stage's own import map: in <head>, before any module script */
add_action( 'wp_head', function () {
	if ( ! nadlan_ps_current() ) { return; }
	echo "\n" . '<script type="importmap" id="nadlan-ps-importmap">{"imports":{"three":"https://cdn.jsdelivr.net/npm/three@0.170.0/build/three.module.js","three/addons/":"https://cdn.jsdelivr.net/npm/three@0.170.0/examples/jsm/"}}</script>' . "\n";
	$ps   = nadlan_ps_current();
	// KikarHamedinaWorld v104: on a world page three.js and the world load on intent, after the page has painted: the head holds
	// the import map and the first picture only
	if ( ! empty( $ps['world'] ) && function_exists( 'nadlan_ps_world_head' ) ) { nadlan_ps_world_head( $ps ); return; }
	echo '<link rel="modulepreload" href="https://cdn.jsdelivr.net/npm/three@0.170.0/build/three.module.js" crossorigin>' . "\n";
	$pset = nadlan_ps_poster_set( $ps );
	// the same set as the page's first picture (design system ProjectStage, version 29), so it is fetched once
	echo '<link rel="preload" as="image" href="' . esc_url( $pset['src'] ) . '"'
		. ( '' !== $pset['srcset'] ? ' imagesrcset="' . esc_attr( $pset['srcset'] ) . '" imagesizes="' . esc_attr( $pset['sizes'] ) . '"' : '' )
		. ' fetchpriority="high">' . "\n";
	// the stage's script itself, early and quietly: it used to start downloading only after every other script had run
	echo '<link rel="modulepreload" href="' . esc_url( plugins_url( 'assets/project-stage/' . $ps['dir'] . '/stage.js', dirname( __FILE__ ) ) . '?ver=' . nadlan_ps_ver() ) . '" fetchpriority="low">' . "\n";
}, 1 );

add_action( 'wp_footer', function () {
	if ( ! nadlan_ps_current() ) { return; }
	$wps = nadlan_ps_current();
	if ( ! empty( $wps['world'] ) && function_exists( 'nadlan_ps_world_script' ) ) { echo nadlan_ps_world_script( $wps ); return; } // KikarHamedinaWorld v104: the world draws its own floor view
	$src = plugins_url( 'assets/project-stage/bridge.js', dirname( __FILE__ ) ) . '?ver=' . nadlan_ps_ver();
	echo "\n" . '<script type="module" id="nadlan-ps-bridge" src="' . esc_url( $src ) . '"></script>' . "\n";
}, 60 );

/* The page's layout (the grid, the stage's box and the rest) at the very end of the head (design system ProjectStage,
   version 29): in the footer it came last, so on a slow phone the stage sat low and small until the whole page had
   arrived (the first picture showed at 7 s). The rules win by their :root body selectors and !important, not by order. */
add_action( 'wp_head', function () {
	if ( ! nadlan_ps_current() ) { return; }
	/* the layout is the design system's (ProjectStage, version 14: the building in the first fold); it lives here because
	   the grid also holds the area map, which must stay outside the design system's scope (its resets would reach the
	   map's own controls), and the theme's lead. The skin forces a box on the lead, and the theme a width and margins on
	   everything in the content, several with !important: inside the grid they are set back, with a longer selector and
	   !important. */
	// HAD-361: on a left-to-right language page the design system's blocks read left to right (nlds.css fixes rtl on .nlds)
	$ps_l = nadlan_ps_current();
	if ( $ps_l && in_array( $ps_l['lang'] ?? 'he', array( 'en', 'fr', 'ru' ), true ) ) { echo '<style id="nadlan-ps-ltr">:root body .nlds{direction:ltr!important}</style>' . "
"; }
	echo '<style id="nadlan-ps-css">'
		. ':root body .nlps-page{box-sizing:border-box!important;width:100%!important;max-width:none!important;margin:6px 0 30px!important;padding:0 clamp(12px,2vw,20px)!important;display:grid!important;grid-template-columns:minmax(300px,380px) minmax(0,1fr) 260px;grid-template-areas:"hero stage rail" "lead stage rail" "cta stage rail" "below below below" "facts facts facts" "tour tour tour" "deals deals deals";grid-template-rows:auto auto 1fr;column-gap:22px;row-gap:14px;align-items:start}'
		. ':root body .nlps-page>*{min-width:0;max-width:none!important;margin:0!important;box-sizing:border-box}'
		. ':root body .nlps-page>.nlps-herowrap{grid-area:hero;padding:0!important}'
		. ':root body .nlps-page>.nl-lead{grid-area:lead;background:none!important;border:0!important;border-radius:0!important;box-shadow:none!important;padding:0!important}'
		. ':root body .nlps-page>.nl-lead>p{max-width:none!important;margin:0!important;font-size:16.5px!important;line-height:1.75!important;color:var(--nlds-sa-ink,#1B1A17)}'
		. ':root body .nlps-page>.nlps-ctawrap{grid-area:cta}'
		. ':root body .nlds .nlps-ctawrap .nlps-hero__cta{margin-top:0!important}'
		. ':root body .nlds .nlps-ctawrap .nlps-hero__cta .nlds-btn{flex:1 1 auto!important;justify-content:center!important}'
		. ':root body .nlps-page>.nlps-stagebox{grid-area:stage;display:grid;gap:10px}'
		// StageFacilities v95: the facilities pill on the model, top corner on the reading side, above the stage's own layer
		. ':root body .nlps-stage{position:relative}'
		. ':root body .nlps-stage>.nlps-facbtn{position:absolute;top:12px;inset-inline-start:12px;z-index:6;display:inline-flex;align-items:center;gap:8px;min-height:44px;padding:0 16px;border-radius:999px;border:1px solid rgba(20,33,43,.14);background:rgba(250,247,241,.94);color:#14212B;font:700 14.5px/1 Heebo,Assistant,sans-serif;box-shadow:0 6px 18px rgba(20,33,43,.14);cursor:pointer;-webkit-backdrop-filter:blur(6px);backdrop-filter:blur(6px)}'
		. ':root body .nlps-stage:has(>.nlps-facbtn) .rbs-hint{top:66px}'
		. ':root body .nlps-stage>.nlps-facbtn i{font-style:normal;color:#9C7A3C}'
		. ':root body .nlps-stage>.nlps-facbtn b{display:inline-grid;place-items:center;min-width:22px;height:22px;border-radius:999px;background:#1F4B5C;color:#fff;font-size:12.5px}'
		. ':root body .nlps-stage>.nlps-facbtn[aria-pressed="true"]{background:#1F4B5C;color:#fff;border-color:#1F4B5C}'
		. ':root body .nlps-stage>.nlps-facbtn[aria-pressed="true"] i{color:#E8C572}:root body .nlps-stage>.nlps-facbtn[aria-pressed="true"] b{background:#fff;color:#1F4B5C}'
		. ':root body .nlps-page>.nlps-rail{grid-area:rail;display:grid;gap:14px;align-content:start}'
		. ':root body .nlps-page>.nlps-factswrap{grid-area:facts;padding:0!important;margin-top:10px!important}'
		// the theme's sitewide sheet has its own older ".nlpf" (1120px wide, auto margins, a deep shadow): not here
		. ':root body .nlps-page .nlds .nlpf{width:auto!important;margin:0!important;box-shadow:none!important}'
		. ':root body .nlps-page>.nlps-dealswrap{grid-area:deals;padding:0!important;margin-top:10px!important}:root body .nlps-page>.nlps-tourwrap{grid-area:tour;padding:0!important;margin-top:10px!important}'
		// one map per page (the recipe, row 18): the area map stands next to the view, so the surroundings band's static map, a
		// second way into the price map, is not shown; its tiles take the whole width
		. ':root body .nlcp-surr .nlcp-surr__map{display:none!important}'
		. ':root body .nlcp-surr .nlcp-surr__grid{grid-template-columns:minmax(0,1fr)!important}'
		. ':root body .nlcp-surr .nlcp-surr__tiles{grid-template-columns:repeat(auto-fit,minmax(210px,1fr))!important}'
		. ':root body .nlps-page>.nlps-below{grid-area:below;display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:16px;align-items:stretch;margin-top:10px!important}'
		. '.nlps-below--solo{grid-template-columns:minmax(0,1fr)!important}'
		. '.nlps-below>#nlpjx-map{margin:0!important;min-width:0;max-width:none!important}'
		. '.nlps-stage{position:relative;width:100%;height:clamp(520px,calc(100svh - 240px),700px);border-radius:16px;overflow:hidden;background:var(--nlds-sa-paper,#F7F6F2);border:1px solid var(--nlds-sa-line,#E3E1DA);margin:0}'
		. '.nlps-stage__mount{position:absolute;inset:0}'
		. ':root body .nlps-stage .nlps-ssr-poster{position:absolute;inset:0;width:100%!important;height:100%!important;max-width:none!important;object-fit:cover;object-position:44% 50%;display:block;border:0;margin:0!important;border-radius:0!important;box-shadow:none!important}'
		. ':root body .nlps-srt{position:absolute!important;width:1px!important;height:1px!important;padding:0!important;margin:-1px!important;overflow:hidden!important;clip:rect(0,0,0,0)!important;white-space:nowrap!important;border:0!important}'
		. ':root body .nlds .nlps-hint[hidden],:root body .nlds .nlps-view__cap[hidden],:root body .nlds .nlps-view__cta[hidden],:root body .nlds #nlps-view-empty[hidden]{display:none!important}'
		. ':root body .nlds .nlps-view__map.nlps-stand{cursor:default}'
		// the labels in the view from the floor (version 35): the quarter's places and projects, at their positions
		. ':root body .nlds .nlps-near[hidden]{display:none!important}'
		. '.nlps-vpin{display:inline-flex;align-items:center;gap:6px;white-space:nowrap;background:rgba(255,255,255,.94);color:#14212b;font:700 12.5px/1 Assistant,Arial,sans-serif;border-radius:999px;padding:6px 10px;box-shadow:0 2px 8px rgba(0,0,0,.2);pointer-events:none}'
		. '.nlps-vpin i{width:8px;height:8px;border-radius:50%;display:inline-block;flex:none}.nlps-vpin--project{background:rgba(20,33,43,.9);color:#fff}'
		. ':root body .nlds .nlbsq__photo img{width:100%!important;height:100%!important;object-fit:cover!important;object-position:50% 24%!important}'
		. ':root body .nlps-rail .nlds .nlbslot{min-height:0!important}'
		. '@media(max-width:1279px){:root body .nlps-page{grid-template-columns:minmax(280px,360px) minmax(0,1fr);grid-template-areas:"hero stage" "lead stage" "cta stage" "below below" "facts facts" "tour tour" "deals deals" "rail rail"}:root body .nlps-page>.nlps-rail{grid-template-columns:repeat(2,minmax(0,300px));margin-top:6px!important}}'
		. '@media(max-width:1099px){:root body .nlps-page{grid-template-columns:minmax(0,1fr);grid-template-rows:none;grid-template-areas:"hero" "lead" "cta" "stage" "below" "facts" "tour" "deals" "rail";column-gap:0}:root body .nlps-page>.nlps-below{grid-template-columns:minmax(0,1fr)}:root body .nlps-page>.nlps-rail{grid-template-columns:minmax(0,1fr) minmax(0,1fr)}.nlps-stage{height:62svh;min-height:380px}}'
		. '@media(max-width:600px){.nlps-stage{height:70svh;min-height:360px}:root body .nlps-page{padding:0 12px!important;row-gap:12px}:root body .nlps-page>.nlps-rail{gap:12px}:root body .nlps-page>.nl-lead>p{font-size:16px!important}}'
		. ':root body .bottom-line[data-nl-lead]{display:none!important}' // StageDuo v81: the article's bottom line is the paragraph above
		. '</style>' . "\n";
}, 999 );

if ( ! function_exists( 'nadlan_pg_render' ) ) {
	/** PriceGuide v1 (design system 7.10.2026, HAD-433): the price list and the price calculator, right after the opening
	 *  paragraph and the buttons. Kikar HaMedina in Hebrew only for now. The markup comes from
	 *  scripts/project-stage/price_guide/render.py with hamedina.json (every number has its source there). */
	function nadlan_pg_render( $ps, $wa ) {
		static $done = false;
		if ( $done || 'hamedina' !== (string) ( $ps['slug'] ?? '' ) ) { return ''; }
		$done = true;
		$wa   = preg_replace( '/\D/', '', (string) $wa );
		$html = <<<'NLPG_HTML'
<section class="nlds nlpg" id="nlpg" aria-labelledby="nlpg-t" dir="rtl" lang="he"><div class="nlpg__in"><header class="nlpg__head"><p class="nlds-kicker">מחירון · עודכן <span class="nlds-num">7.10.2026</span></p><h2 class="nlpg__title" id="nlpg-t">כמה עולה דירה במגדלי כיכר המדינה</h2><p class="nlpg__answer">דירה במגדלי כיכר המדינה נמכרת בממוצע בכ-<span class="nlds-num">65,000</span> ₪ למ״ר, לפי ההערכות שפורסמו באוקטובר <span class="nlds-num">2026.</span> בקומות <span class="nlds-num">38-39</span> נרשמו עסקאות של <span class="nlds-num">9.58</span> עד <span class="nlds-num">10.63</span> מיליון ₪ לדירת <span class="nlds-num">4</span> חדרים בשטח <span class="nlds-num">140</span> מ״ר, כ-<span class="nlds-num">68,000</span> עד <span class="nlds-num">76,000</span> ₪ למ״ר. בשכונה שסביב הכיכר, חציון העסקאות ברבעון הראשון של <span class="nlds-num">2026</span> היה <span class="nlds-num">4.94</span> מיליון ₪ לדירת <span class="nlds-num">3</span> חדרים, <span class="nlds-num">6.84</span> מיליון ל-<span class="nlds-num">4</span> חדרים ו-<span class="nlds-num">8.46</span> מיליון ל-<span class="nlds-num">5</span> חדרים. בבניינים החדשים סביב הכיכר המחיר ירד מ-<span class="nlds-num">70,000-75,000</span> ₪ למ״ר בשיא ל-<span class="nlds-num">63,000-68,000</span> ₪.</p></header><ul class="nlpg__tiles"><li><b>כ-<span class="nlds-num">65,000</span> ₪</b><span>למ״ר, ממוצע העסקאות במגדלים לפי ההערכות</span><i><span class="nlds-num">10.2026</span></i></li><li><b><span class="nlds-num">9.58-10.63</span> מיליון ₪</b><span><span class="nlds-num">3</span> עסקאות, <span class="nlds-num">4</span> חדרים, <span class="nlds-num">140</span> מ״ר, קומות <span class="nlds-num">38-39</span></span><i><span class="nlds-num">4-12.2024</span></i></li><li><b><span class="nlds-num">63,000-68,000</span> ₪</b><span>למ״ר בבניינים החדשים סביב הכיכר</span><i><span class="nlds-num">10.2026</span></i></li></ul><div class="nlpg__grid"><div class="nlpg__list"><table class="nlpg__table"><caption class="nlpg__cap">המחירון</caption><thead><tr><th scope="col">הנכס</th><th scope="col">₪ למ״ר</th><th scope="col">מחיר הדירה, ₪</th><th scope="col">הנתון</th><th scope="col">מועד</th></tr></thead><tbody class="nlpg__grp"><tr class="nlpg__gh"><th colspan="5" scope="colgroup">במגדלי כיכר המדינה</th></tr><tr><th scope="row"><b>ממוצע העסקאות במגדלים</b><span>כ-<span class="nlds-num">10</span> עד <span class="nlds-num">20</span> דירות או זכויות נמכרו עד היום, לפי ההערכות</span></th><td data-l="₪ למ״ר">כ-<span class="nlds-num">65,000</span></td><td data-l="מחיר"><span class="nlpg__na" aria-label="לא פורסם">·</span></td><td data-l="הנתון"><span class="nlpg__k nlpg__k--est">הערכה</span></td><td data-l="מועד"><span class="nlds-num">10.2026</span></td></tr><tr><th scope="row"><b><span class="nlds-num">4</span> חדרים, <span class="nlds-num">140</span> מ״ר, קומות <span class="nlds-num">38-39</span></b><span>שלוש עסקאות</span></th><td data-l="₪ למ״ר"><span class="nlds-num">68,400-75,900</span></td><td data-l="מחיר"><span class="nlds-num">9.58-10.63</span> מיליון</td><td data-l="הנתון"><span class="nlpg__k nlpg__k--deal">עסקה</span></td><td data-l="מועד"><span class="nlds-num">4-12.2024</span></td></tr><tr><th scope="row"><b>העסקאות היקרות במגדלים</b><span>בחלק מהעסקאות</span></th><td data-l="₪ למ״ר">מעל <span class="nlds-num">80,000</span></td><td data-l="מחיר"><span class="nlpg__na" aria-label="לא פורסם">·</span></td><td data-l="הנתון"><span class="nlpg__k nlpg__k--deal">עסקה</span></td><td data-l="מועד"><span class="nlds-num">10.2026</span></td></tr><tr><th scope="row"><b>זכויות לדירת <span class="nlds-num">148</span> מ״ר, קומה נמוכה</b><span>מודעה</span></th><td data-l="₪ למ״ר">כ-<span class="nlds-num">42,600</span></td><td data-l="מחיר">כ-<span class="nlds-num">6.3</span> מיליון</td><td data-l="הנתון"><span class="nlpg__k nlpg__k--ask">מחיר מבוקש</span></td><td data-l="מועד"><span class="nlds-num">4.2025</span></td></tr><tr><th scope="row"><b>דירה בקומה <span class="nlds-num">12</span></b><span>מודעה</span></th><td data-l="₪ למ״ר"><span class="nlpg__na" aria-label="לא פורסם">·</span></td><td data-l="מחיר"><span class="nlds-num">10.3</span> מיליון</td><td data-l="הנתון"><span class="nlpg__k nlpg__k--ask">מחיר מבוקש</span></td><td data-l="מועד"><span class="nlds-num">4.2025</span></td></tr><tr><th scope="row"><b>פנטהאוז בקומה <span class="nlds-num">39</span></b><span>מודעה</span></th><td data-l="₪ למ״ר"><span class="nlpg__na" aria-label="לא פורסם">·</span></td><td data-l="מחיר"><span class="nlds-num">43</span> מיליון</td><td data-l="הנתון"><span class="nlpg__k nlpg__k--ask">מחיר מבוקש</span></td><td data-l="מועד"><span class="nlds-num">4.2025</span></td></tr></tbody><tbody class="nlpg__grp nlpg__grp--more"><tr class="nlpg__gh"><th colspan="5" scope="colgroup">חציון העסקאות בשכונה, רבעון ראשון 2026</th></tr><tr><th scope="row"><b><span class="nlds-num">3</span> חדרים</b><span>בכל תל אביב יפו: <span class="nlds-num">4.23</span> מיליון</span></th><td data-l="₪ למ״ר"><span class="nlpg__na" aria-label="לא פורסם">·</span></td><td data-l="מחיר"><span class="nlds-num">4.94</span> מיליון</td><td data-l="הנתון"><span class="nlpg__k nlpg__k--med">חציון עסקאות</span></td><td data-l="מועד"><span class="nlds-num">1-3.2026</span></td></tr><tr><th scope="row"><b><span class="nlds-num">4</span> חדרים</b><span>בכל תל אביב יפו: <span class="nlds-num">5.23</span> מיליון</span></th><td data-l="₪ למ״ר"><span class="nlpg__na" aria-label="לא פורסם">·</span></td><td data-l="מחיר"><span class="nlds-num">6.84</span> מיליון</td><td data-l="הנתון"><span class="nlpg__k nlpg__k--med">חציון עסקאות</span></td><td data-l="מועד"><span class="nlds-num">1-3.2026</span></td></tr><tr><th scope="row"><b><span class="nlds-num">5</span> חדרים</b><span>בכל תל אביב יפו: <span class="nlds-num">7.50</span> מיליון</span></th><td data-l="₪ למ״ר"><span class="nlpg__na" aria-label="לא פורסם">·</span></td><td data-l="מחיר"><span class="nlds-num">8.46</span> מיליון</td><td data-l="הנתון"><span class="nlpg__k nlpg__k--med">חציון עסקאות</span></td><td data-l="מועד"><span class="nlds-num">1-3.2026</span></td></tr></tbody><tbody class="nlpg__grp nlpg__grp--more"><tr class="nlpg__gh"><th colspan="5" scope="colgroup">סביב הכיכר, רובע 4</th></tr><tr><th scope="row"><b>בניינים חדשים, פרויקטים ששווקו לאחרונה</b><span>בשיא: <span class="nlds-num">70,000-75,000</span> ₪ למ״ר</span></th><td data-l="₪ למ״ר"><span class="nlds-num">63,000-68,000</span></td><td data-l="מחיר"><span class="nlpg__na" aria-label="לא פורסם">·</span></td><td data-l="הנתון"><span class="nlpg__k nlpg__k--mkt">מחיר שיווק</span></td><td data-l="מועד"><span class="nlds-num">10.2026</span></td></tr><tr><th scope="row"><b>פנטהאוזים ודירות גן</b><span>דירות גדולות עם שטח חוץ</span></th><td data-l="₪ למ״ר"><span class="nlds-num">80,000-110,000</span></td><td data-l="מחיר"><span class="nlpg__na" aria-label="לא פורסם">·</span></td><td data-l="הנתון"><span class="nlpg__k nlpg__k--deal">עסקה</span></td><td data-l="מועד"><span class="nlds-num">10.2026</span></td></tr><tr><th scope="row"><b><span class="nlds-num">3-4</span> חדרים בבניינים קיימים</b><span>ארבע עסקאות, <span class="nlds-num">70-110</span> מ״ר</span></th><td data-l="₪ למ״ר"><span class="nlds-num">59,000-76,000</span></td><td data-l="מחיר"><span class="nlds-num">4.75-8.4</span> מיליון</td><td data-l="הנתון"><span class="nlpg__k nlpg__k--deal">עסקה</span></td><td data-l="מועד"><span class="nlds-num">2026</span></td></tr><tr><th scope="row"><b>דירות חדשות למכירה בטבעת הכיכר</b><span><span class="nlds-num">142-161</span> מ״ר, קומות <span class="nlds-num">12</span> ו-<span class="nlds-num">23</span></span></th><td data-l="₪ למ״ר"><span class="nlds-num">79,000-90,000</span></td><td data-l="מחיר"><span class="nlds-num">11.25-14.5</span> מיליון</td><td data-l="הנתון"><span class="nlpg__k nlpg__k--ask">מחיר מבוקש</span></td><td data-l="מועד"><span class="nlds-num">10.2026</span></td></tr><tr><th scope="row"><b>דירה בבניין ותיק בטבעת הכיכר</b><span><span class="nlds-num">107</span> מ״ר, כנראה לשיפוץ</span></th><td data-l="₪ למ״ר">כ-<span class="nlds-num">43,000</span></td><td data-l="מחיר"><span class="nlds-num">4.59</span> מיליון</td><td data-l="הנתון"><span class="nlpg__k nlpg__k--ask">מחיר מבוקש</span></td><td data-l="מועד"><span class="nlds-num">10.2026</span></td></tr></tbody><tbody class="nlpg__grp nlpg__grp--more"><tr class="nlpg__gh"><th colspan="5" scope="colgroup">להשוואה</th></tr><tr><th scope="row"><b>תל אביב יפו, כל העיר</b><span>חציון של <span class="nlds-num">2,432</span> עסקאות</span></th><td data-l="₪ למ״ר"><span class="nlds-num">52,856</span></td><td data-l="מחיר"><span class="nlpg__na" aria-label="לא פורסם">·</span></td><td data-l="הנתון"><span class="nlpg__k nlpg__k--deal">עסקה</span></td><td data-l="מועד"><span class="nlds-num">10.2023-10.2025</span></td></tr></tbody></table><button class="nlpg__more" type="button" aria-expanded="false"><span class="nlpg__mt">לכל המחירון: סביב הכיכר ולהשוואה <span class="nlds-num">(9)</span></span><span class="nlpg__mp">למחירון המלא <span class="nlds-num">(15)</span></span></button></div><form class="nlpg__calc" data-cfg="{&quot;modes&quot;:[{&quot;id&quot;:&quot;tower&quot;,&quot;label&quot;:&quot;במגדלים&quot;,&quot;floor&quot;:true,&quot;lo_floor1&quot;:58000,&quot;hi_floor39&quot;:72000,&quot;band&quot;:0.07,&quot;why&quot;:&quot;אומדן לפי הקומה: בין כ-58,000 ₪ למ״ר בקומות הנמוכות לכ-72,000 ₪ בקומות 38-39, סביב הממוצע של כ-65,000 ₪. העסקאות שפורסמו בקומות 38-39: 68,400-75,900 ₪ למ״ר.&quot;},{&quot;id&quot;:&quot;new&quot;,&quot;label&quot;:&quot;בניין חדש בסביבה&quot;,&quot;lo&quot;:63000,&quot;hi&quot;:68000,&quot;why&quot;:&quot;המחירים בפרויקטים חדשים סביב הכיכר ששווקו לאחרונה.&quot;},{&quot;id&quot;:&quot;resale&quot;,&quot;label&quot;:&quot;דירה קיימת בסביבה&quot;,&quot;lo&quot;:59000,&quot;hi&quot;:76000,&quot;why&quot;:&quot;עסקאות 2026 בדירות 3-4 חדרים בבניינים קיימים סביב הכיכר.&quot;},{&quot;id&quot;:&quot;premium&quot;,&quot;label&quot;:&quot;פנטהאוז או דירת גן&quot;,&quot;lo&quot;:80000,&quot;hi&quot;:110000,&quot;why&quot;:&quot;דירות גדולות, פנטהאוזים ודירות גן עם שטח חוץ סביב הכיכר.&quot;}],&quot;deals&quot;:[[38,68400],[39,68500],[38,75900]],&quot;avg&quot;:65000,&quot;ta&quot;:52856,&quot;tax1&quot;:[[1978745,0],[2347040,0.035],[6055070,0.05],[20183565,0.08],[null,0.1]],&quot;tax2&quot;:[[6055070,0.08],[null,0.1]],&quot;wa&quot;:&quot;{{WA}}&quot;}" novalidate><h3 class="nlpg__ct">מחשבון מחיר דירה בכיכר המדינה</h3><fieldset class="nlpg__f"><legend>איפה הדירה</legend><div class="nlpg__seg"><label><input type="radio" name="nlpg-m" value="tower" checked><span>במגדלים</span></label><label><input type="radio" name="nlpg-m" value="new"><span>בניין חדש בסביבה</span></label><label><input type="radio" name="nlpg-m" value="resale"><span>דירה קיימת בסביבה</span></label><label><input type="radio" name="nlpg-m" value="premium"><span>פנטהאוז או דירת גן</span></label></div></fieldset><div class="nlpg__f"><label for="nlpg-a">שטח הדירה</label><div class="nlpg__rng"><input type="range" id="nlpg-a" data-pg="a" min="50" max="300" step="5" value="140"><output data-pg="ao" for="nlpg-a"><span class="nlds-num">140</span> מ״ר</output></div></div><div class="nlpg__f" data-pg="fl"><label for="nlpg-fs">קומה</label><div class="nlpg__rng"><input type="range" id="nlpg-fs" data-pg="fs" min="1" max="40" step="1" value="20"><output data-pg="fo" for="nlpg-fs">קומה <span class="nlds-num">20</span></output></div></div><fieldset class="nlpg__f"><legend>מס רכישה</legend><div class="nlpg__seg nlpg__seg--2"><label><input type="radio" name="nlpg-t" value="single" checked><span>דירה יחידה</span></label><label><input type="radio" name="nlpg-t" value="more"><span>דירה נוספת</span></label></div></fieldset><div class="nlpg__out" aria-live="polite" aria-atomic="true"><p class="nlpg__ol">אומדן מחיר</p><p class="nlpg__big" data-pg="p"><span class="nlds-num">8.46-9.74</span> מיליון ₪</p><p class="nlpg__pm" data-pg="pm">כ-<span class="nlds-num">60,400-69,600</span> ₪ למ״ר</p><svg class="nlpg__chart" data-pg="ch" viewBox="0 0 340 138" direction="ltr" role="img" focusable="false"><title>המחיר למ״ר לפי הקומה במגדלים, עם העסקאות שפורסמו</title></svg><dl class="nlpg__rows"><div><dt>מס רכישה</dt><dd data-pg="tx">כ-<span class="nlds-num">442,000</span> ₪</dd></div><div><dt>סה״כ עם מס רכישה</dt><dd data-pg="tt">כ-<span class="nlds-num">9.54</span> מיליון ₪</dd></div></dl><p class="nlpg__why" data-pg="why">אומדן לפי הקומה: בין כ-<span class="nlds-num">58,000</span> ₪ למ״ר בקומות הנמוכות לכ-<span class="nlds-num">72,000</span> ₪ בקומות <span class="nlds-num">38-39,</span> סביב הממוצע של כ-<span class="nlds-num">65,000</span> ₪. העסקאות שפורסמו בקומות <span class="nlds-num">38-39</span>: <span class="nlds-num">68,400-75,900</span> ₪ למ״ר.</p></div><a class="nlds-btn nlds-btn--primary nlpg__wa" data-pg="wa" target="_blank" rel="noopener" data-nlps-ev="pg-wa" href="https://wa.me/{{WA}}?text=">לקבלת פרטים נוספים בוואטסאפ</a><p class="nlpg__links"><a href="https://nad-lan.co.il/apartment-purchase-cost-calculator/">לכל עלויות הקנייה ←</a><a href="https://nad-lan.co.il/mortgage-calculator/">לחישוב המשכנתא ←</a></p><p class="nlpg__fine">אומדן לא מחייב, לפי העסקאות והמחירים שפורסמו עד <span class="nlds-num">7.10.2026</span>. במודעות של דירות יקרות, המחיר המבוקש גבוה בדרך כלל ב-<span class="nlds-num">5</span>%-<span class="nlds-num">10</span>% מהמחיר שנסגר בפועל. המחיר נקבע מול המוכר.</p></form></div><p class="nlpg__src">המחירון מבוסס על עסקאות שדווחו לרשות המסים ופורסמו, על הערכות של שמאים ואנשי מקצוע באזור ועל מודעות למכירה. מחיר מבוקש מסומן בנפרד ואינו מחיר סגירה. עודכן <span class="nlds-num">7.10.2026.</span></p></div></section>
NLPG_HTML;
		$css  = <<<'NLPG_CSS'
.nlpg{--pg-sea:var(--nlds-sa-sea,#2f6f86);--pg-seah:var(--nlds-sa-seah,#255c70);--pg-ink:var(--nlds-sa-ink,#14212b);--pg-ink2:var(--nlds-sa-ink2,#3b4753);--pg-line:var(--nlds-sa-line,#e3e1da);--pg-paper:var(--nlds-sa-paper,#f7f6f2);--pg-sand:var(--nlds-sa-sand,#eee9dd);--pg-surf:var(--nlds-sa-surf,#fff);--pg-deep:var(--nlds-sa-deep,#1f4b5c);--pg-serif:var(--nlds-font-serif,"Noto Serif Hebrew","David Libre",Georgia,serif);--pg-sans:var(--nlds-font-sans,Assistant,"Segoe UI",Arial,sans-serif);display:block !important;container-type:inline-size !important;container-name:nlpg !important;margin:clamp(18px,3vw,34px) auto 0 !important;max-width:var(--nlds-container,1240px) !important;padding:0 clamp(16px,3vw,32px) !important;box-sizing:border-box !important;font-family:var(--pg-sans) !important;color:var(--pg-ink) !important}
.nlpg *,.nlpg *::before,.nlpg *::after{box-sizing:border-box !important}
.nlps-page>.nlpg{grid-area:prices !important;margin:6px 0 0 !important;padding:0 !important;max-width:none !important;width:auto !important}
.nlpg .nlds-num{font-size:inherit !important;font-weight:inherit !important;color:inherit !important;direction:ltr !important;unicode-bidi:isolate !important;display:inline-block !important;font-variant-numeric:tabular-nums lining-nums !important}
.nlpg .nlpg__in{display:grid !important;gap:var(--nlds-space-18,18px) !important;background:var(--pg-surf) !important;border:1px solid var(--pg-line) !important;border-radius:var(--nlds-radius-22,22px) !important;padding:clamp(18px,3vw,34px) !important}
.nlpg .nlpg__head{display:grid !important;gap:8px !important}
.nlpg .nlpg__title{font-family:var(--pg-serif) !important;font-weight:600 !important;font-size:clamp(23px,1.2rem + 1.1vw,31px) !important;line-height:1.22 !important;letter-spacing:-.005em !important;color:var(--pg-ink) !important;margin:0 !important;text-wrap:balance !important}
.nlpg .nlpg__answer{font-size:clamp(15.5px,1rem + .15vw,17px) !important;line-height:1.7 !important;color:var(--pg-ink2) !important;margin:0 !important;max-width:78ch !important}
.nlpg .nlpg__tiles{display:grid !important;grid-template-columns:repeat(3,minmax(0,1fr)) !important;gap:var(--nlds-space-12,12px) !important;margin:0 !important;padding:0 !important;list-style:none !important}
.nlpg .nlpg__tiles li{display:grid !important;gap:3px !important;align-content:start !important;padding:14px 16px !important;background:var(--pg-paper) !important;border:1px solid var(--pg-line) !important;border-radius:var(--nlds-radius-14,14px) !important;margin:0 !important}
.nlpg .nlpg__tiles b{font-family:var(--pg-serif) !important;font-size:clamp(20px,1rem + .9vw,25px) !important;font-weight:600 !important;line-height:1.2 !important;color:var(--pg-ink) !important}
.nlpg .nlpg__tiles li>span{font-size:13.5px !important;line-height:1.45 !important;color:var(--pg-ink2) !important}
.nlpg .nlpg__tiles i{font-style:normal !important;font-size:12.5px !important;color:var(--pg-ink2) !important}
.nlpg .nlpg__grid{display:grid !important;grid-template-columns:minmax(0,1.25fr) minmax(300px,1fr) !important;gap:clamp(16px,2.4vw,28px) !important;align-items:start !important}
.nlpg .nlpg__list{display:grid !important;gap:10px !important;min-width:0 !important}
.nlpg .nlpg__table{width:100% !important;border-collapse:collapse !important;font-size:14.5px !important;line-height:1.45 !important;margin:0 !important;background:transparent !important}
.nlpg .nlpg__cap{caption-side:top !important;text-align:start !important;font-family:var(--pg-serif) !important;font-weight:600 !important;font-size:19px !important;color:var(--pg-ink) !important;padding:0 0 6px !important}
.nlpg .nlpg__table thead th{text-align:start !important;font-size:12px !important;font-weight:700 !important;letter-spacing:.03em !important;color:var(--pg-ink2) !important;padding:8px !important;border-bottom:1px solid var(--pg-line) !important;white-space:nowrap !important;background:transparent !important}
.nlpg .nlpg__table td,.nlpg .nlpg__table tbody th{padding:10px 8px !important;border-bottom:1px solid var(--pg-line) !important;vertical-align:middle !important;color:var(--pg-ink) !important;text-align:start !important;background:transparent !important;font-weight:400 !important}
.nlpg .nlpg__table tbody th b{display:block !important;font-weight:600 !important;font-size:14.5px !important;color:var(--pg-ink) !important}
.nlpg .nlpg__table tbody th>span{display:block !important;font-size:12.5px !important;color:var(--pg-ink2) !important;margin-top:1px !important}
.nlpg .nlpg__table td{white-space:nowrap !important;font-variant-numeric:tabular-nums !important}
.nlpg .nlpg__gh th{padding:16px 8px 6px !important;font-family:var(--pg-serif) !important;font-weight:600 !important;font-size:15.5px !important;color:var(--pg-deep) !important;border-bottom:1px solid var(--pg-line) !important;background:transparent !important}
.nlpg .nlpg__grp:first-of-type .nlpg__gh th{padding-top:8px !important}
.nlpg .nlpg__na{color:var(--pg-ink2) !important}
.nlpg .nlpg__k{display:inline-block !important;font-size:12px !important;font-weight:600 !important;line-height:1 !important;padding:5px 9px !important;border-radius:999px !important;border:1px solid var(--pg-line) !important;color:var(--pg-ink2) !important;background:var(--pg-surf) !important;white-space:nowrap !important}
.nlpg .nlpg__k--deal{background:#e6f0f3 !important;border-color:#c8dde4 !important;color:var(--pg-deep) !important}
.nlpg .nlpg__k--ask{background:var(--pg-sand) !important;border-color:#ddd5c3 !important;color:#4a4232 !important}
.nlpg .nlpg__k--med{background:#eef3ee !important;border-color:#cfdccf !important;color:#2c4a35 !important}
.nlpg .nlpg__k--est,.nlpg .nlpg__k--mkt{background:var(--pg-paper) !important;border-style:dashed !important;color:var(--pg-ink2) !important}
.nlpg:not(.is-open) .nlpg__grp--more{display:none !important}
.nlpg .nlpg__more{justify-self:start !important;font:600 14.5px/1.2 var(--pg-sans) !important;color:var(--pg-sea) !important;background:transparent !important;border:1px solid var(--pg-line) !important;border-radius:999px !important;padding:10px 16px !important;min-height:44px !important;cursor:pointer !important}
.nlpg .nlpg__more:hover{border-color:var(--pg-sea) !important;background:var(--pg-paper) !important}
.nlpg.is-open .nlpg__more{display:none !important}
.nlpg .nlpg__mp{display:none !important}
.nlpg .nlpg__calc{display:grid !important;gap:14px !important;background:var(--pg-paper) !important;border:1px solid var(--pg-line) !important;border-radius:var(--nlds-radius-16,16px) !important;padding:clamp(16px,2vw,22px) !important;box-shadow:var(--nlds-shadow-price-card,0 8px 24px rgba(17,17,15,.07),0 2px 6px rgba(17,17,15,.04)) !important;margin:0 !important}
.nlpg .nlpg__ct{font-family:var(--pg-serif) !important;font-weight:600 !important;font-size:19px !important;line-height:1.3 !important;color:var(--pg-ink) !important;margin:0 !important}
.nlpg .nlpg__f{display:grid !important;gap:7px !important;border:0 !important;margin:0 !important;padding:0 !important;min-width:0 !important}
.nlpg .nlpg__f legend,.nlpg .nlpg__f>label{font-size:13.5px !important;font-weight:700 !important;color:var(--pg-ink2) !important;padding:0 !important;margin:0 0 7px !important}
.nlpg .nlpg__seg{display:flex !important;flex-wrap:wrap !important;gap:6px !important}
.nlpg .nlpg__seg label{position:relative !important;margin:0 !important;cursor:pointer !important}
.nlpg .nlpg__seg input{position:absolute !important;opacity:0 !important;inset:0 !important;margin:0 !important;cursor:pointer !important}
.nlpg .nlpg__seg label>span{display:inline-flex !important;align-items:center !important;min-height:40px !important;padding:8px 14px !important;border-radius:999px !important;border:1px solid var(--pg-line) !important;background:var(--pg-surf) !important;font-size:14.5px !important;font-weight:600 !important;color:var(--pg-ink) !important;transition:background .2s,border-color .2s,color .2s !important}
.nlpg .nlpg__seg label:hover>span{border-color:var(--pg-sea) !important}
.nlpg .nlpg__seg input:checked+span{background:var(--pg-sea) !important;border-color:var(--pg-sea) !important;color:var(--nlds-on-sea,#fff) !important}
.nlpg .nlpg__seg input:focus-visible+span{outline:2px solid var(--pg-sea) !important;outline-offset:3px !important}
.nlpg .nlpg__rng{display:flex !important;align-items:center !important;gap:12px !important}
.nlpg .nlpg__rng input[type=range]{flex:1 1 auto !important;min-width:0 !important;height:44px !important;margin:0 !important;accent-color:var(--pg-sea) !important;background:transparent !important;cursor:pointer !important}
.nlpg .nlpg__rng output{flex:0 0 auto !important;min-width:86px !important;text-align:center !important;font-weight:700 !important;font-size:15px !important;color:var(--pg-ink) !important;background:var(--pg-surf) !important;border:1px solid var(--pg-line) !important;border-radius:10px !important;padding:7px 10px !important}
.nlpg .nlpg__f[hidden]{display:none !important}
.nlpg .nlpg__out{display:grid !important;gap:4px !important;background:var(--pg-surf) !important;border:1px solid var(--pg-line) !important;border-radius:14px !important;padding:14px 16px !important}
.nlpg .nlpg__ol{font-size:12.5px !important;font-weight:700 !important;letter-spacing:.04em !important;color:var(--pg-sea) !important;margin:0 !important}
.nlpg .nlpg__big{font-family:var(--pg-serif) !important;font-weight:600 !important;font-size:clamp(25px,1.1rem + 1.3vw,32px) !important;line-height:1.15 !important;color:var(--pg-ink) !important;margin:0 !important}
.nlpg .nlpg__pm{font-size:14.5px !important;color:var(--pg-ink2) !important;margin:0 0 4px !important}
.nlpg .nlpg__chart{direction:ltr !important;display:block !important;width:100% !important;height:auto !important;max-width:100% !important;margin:4px 0 2px !important;overflow:visible !important}
.nlpg .nlpg__chart text{font-family:var(--pg-sans) !important;font-size:10.5px !important;fill:var(--pg-ink2) !important}
.nlpg .nlpg__rows{display:grid !important;gap:2px !important;margin:6px 0 0 !important;padding:8px 0 0 !important;border-top:1px solid var(--pg-line) !important}
.nlpg .nlpg__rows div{display:flex !important;justify-content:space-between !important;gap:12px !important;font-size:14.5px !important}
.nlpg .nlpg__rows dt{color:var(--pg-ink2) !important;font-weight:400 !important;margin:0 !important}
.nlpg .nlpg__rows dd{margin:0 !important;font-weight:700 !important;color:var(--pg-ink) !important}
.nlpg .nlpg__why{font-size:12.5px !important;line-height:1.5 !important;color:var(--pg-ink2) !important;margin:6px 0 0 !important}
.nlpg .nlpg__wa{display:flex !important;align-items:center !important;justify-content:center !important;width:100% !important;min-height:52px !important;margin:0 !important;padding:10px 22px !important;border-radius:999px !important;background:var(--pg-sea) !important;border:1px solid var(--pg-sea) !important;color:var(--nlds-on-sea,#fff) !important;font:700 16.5px/1.2 var(--pg-sans) !important;text-decoration:none !important;text-align:center !important}
.nlpg .nlpg__wa:hover{background:var(--pg-seah) !important;border-color:var(--pg-seah) !important}
.nlpg .nlpg__wa:focus-visible{outline:2px solid var(--pg-sea) !important;outline-offset:3px !important}
.nlpg .nlpg__links{display:flex !important;flex-wrap:wrap !important;gap:6px 18px !important;margin:0 !important;font-size:14.5px !important}
.nlpg .nlpg__links a{color:var(--pg-sea) !important;font-weight:600 !important;text-decoration:underline !important;text-decoration-color:var(--nlds-link-underline,rgba(47,111,134,.4)) !important;text-underline-offset:3px !important;min-height:44px !important;display:inline-flex !important;align-items:center !important}
.nlpg .nlpg__fine{font-size:12.5px !important;line-height:1.55 !important;color:var(--pg-ink2) !important;margin:0 !important}
.nlpg .nlpg__src{font-size:12.5px !important;line-height:1.55 !important;color:var(--pg-ink2) !important;margin:0 !important;max-width:90ch !important}
@container nlpg (max-width:860px){
 .nlpg .nlpg__grid{grid-template-columns:minmax(0,1fr) !important}
 .nlpg .nlpg__calc{order:-1 !important}
}
@container nlpg (max-width:620px){
 .nlpg .nlpg__tiles{grid-template-columns:minmax(0,1fr) !important}
 .nlpg .nlpg__tiles li{grid-template-columns:auto 1fr !important;column-gap:12px !important;align-items:baseline !important;padding:11px 14px !important}
 .nlpg .nlpg__tiles li>span{grid-column:1/-1 !important}
 .nlpg .nlpg__tiles li i{grid-row:1 !important;grid-column:2 !important;justify-self:end !important}
 .nlpg .nlpg__table thead{display:none !important}
 .nlpg .nlpg__table,.nlpg .nlpg__table tbody,.nlpg .nlpg__table tr{display:block !important;width:100% !important}
 .nlpg .nlpg__table tbody tr:not(.nlpg__gh){display:grid !important;grid-template-columns:1fr 1fr !important;gap:4px 12px !important;padding:12px 0 !important;border-bottom:1px solid var(--pg-line) !important}
 .nlpg .nlpg__table tbody tr:not(.nlpg__gh) th{grid-column:1/-1 !important;padding:0 !important;border:0 !important}
 .nlpg .nlpg__table td{display:block !important;padding:0 !important;border:0 !important;white-space:normal !important}
 .nlpg .nlpg__table td::before{content:attr(data-l) !important;display:block !important;font-size:11.5px !important;font-weight:700 !important;color:var(--pg-ink2) !important}
 .nlpg .nlpg__gh th{display:block !important;padding:14px 0 4px !important}
 .nlpg .nlpg__seg label>span{min-height:44px !important}
 .nlpg .nlpg__in{border-radius:var(--nlds-radius-16,16px) !important;padding:16px !important}
 .nlpg:not(.is-open) .nlpg__table{display:none !important}
 .nlpg .nlpg__mt{display:none !important}
 .nlpg .nlpg__mp{display:inline !important}
 .nlpg .nlpg__more{justify-self:stretch !important}
 .nlpg .nlpg__chart text{font-size:12.5px !important}
}
@container nlpg (min-width:861px){.nlpg:not(.is-open) .nlpg__grp--more{display:table-row-group !important}.nlpg .nlpg__more{display:none !important}}
@media (prefers-reduced-motion:reduce){.nlpg .nlpg__seg label>span{transition:none !important}}
NLPG_CSS;
		$js   = <<<'NLPG_JS'
(function(){var NS='http://www.w3.org/2000/svg';
var nf=function(n){return new Intl.NumberFormat('he-IL',{maximumFractionDigits:0}).format(Math.round(n/100)*100)};
var mil=function(n){return (n/1e6).toFixed(2).replace(/\.?0+$/,'')};
var isl=function(s){return '<span class="nlds-num">'+s+'</span>'};
function tax(p,br){var a=0,prev=0;for(var i=0;i<br.length;i++){var cap=br[i][0],r=br[i][1],top=cap===null?p:Math.min(p,cap);if(top>prev)a+=(top-prev)*r;if(cap===null||p<=cap)break;prev=cap}return a}
function el(t,a,txt){var e=document.createElementNS(NS,t);for(var k in a)e.setAttribute(k,a[k]);if(txt!=null)e.textContent=txt;return e}
function one(root){var f=root.querySelector('.nlpg__calc');if(!f||f.__nlpg)return;f.__nlpg=1;var C;try{C=JSON.parse(f.getAttribute('data-cfg'))}catch(e){return}
 var q=function(k){return f.querySelector('[data-pg="'+k+'"]')};
 var val=function(n){var x=f.querySelector('input[name^="'+n+'"]:checked');return x?x.value:''};
 var mode=function(){var id=val('nlpg-m');for(var i=0;i<C.modes.length;i++)if(C.modes[i].id===id)return C.modes[i];return C.modes[0]};
 function draw(m,lo,hi,floor){var s=q('ch');if(!s)return;while(s.lastChild&&s.lastChild.nodeName!=='title')s.removeChild(s.lastChild);
  var L=44,R=330,T=12,B=112;
  if(m.floor){var y0=50000,y1=82000,X=function(fl){return L+(fl-1)*(R-L)/39},Y=function(v){return B-(v-y0)*(B-T)/(y1-y0)};
   var up=[],dn=[];for(var fl=1;fl<=40;fl++){var p=m.lo_floor1+(fl-1)*(m.hi_floor39-m.lo_floor1)/38;up.push(X(fl)+','+Y(p*(1+m.band)));dn.unshift(X(fl)+','+Y(p*(1-m.band)))}
   [[60000,'60,000'],[70000,'70,000'],[80000,'80,000']].forEach(function(g){s.appendChild(el('line',{x1:L,x2:R,y1:Y(g[0]),y2:Y(g[0]),stroke:'#e3e1da','stroke-width':1}));s.appendChild(el('text',{x:L-6,y:Y(g[0])+3.5,'text-anchor':'end'},g[1]))});
   s.appendChild(el('polygon',{points:up.concat(dn).join(' '),fill:'rgba(47,111,134,.14)'}));
   s.appendChild(el('line',{x1:L,x2:R,y1:Y(C.avg),y2:Y(C.avg),stroke:'#1f4b5c','stroke-width':1.2,'stroke-dasharray':'4 3'}));
   s.appendChild(el('text',{x:L+4,y:Y(C.avg)-5,'text-anchor':'start'},'ממוצע העסקאות, כ-65,000'));
   var fx=X(floor),pm=(lo+hi)/2;s.appendChild(el('line',{x1:fx,x2:fx,y1:T-4,y2:B,stroke:'#2f6f86','stroke-width':1.5}));
   s.appendChild(el('circle',{cx:fx,cy:Y(pm),r:5.5,fill:'#2f6f86',stroke:'#fff','stroke-width':2}));
   C.deals.forEach(function(d){s.appendChild(el('circle',{cx:X(d[0]),cy:Y(d[1]),r:4,fill:'#fff',stroke:'#14212b','stroke-width':1.6}))});
   s.appendChild(el('text',{x:X(36.6),y:Y(77600),'text-anchor':'end'},'עסקאות שפורסמו'));
   s.appendChild(el('text',{x:L,y:B+16,'text-anchor':'start'},'קומה 1'));s.appendChild(el('text',{x:R,y:B+16,'text-anchor':'end'},'קומה 40'));
   s.appendChild(el('text',{x:(L+R)/2,y:B+16,'text-anchor':'middle'},'₪ למ״ר לפי הקומה'));
   s.setAttribute('aria-label','אומדן של '+nf(lo)+' עד '+nf(hi)+' ₪ למ״ר בקומה '+floor+', מול ממוצע העסקאות במגדלים, כ-65,000 ₪');
  }else{var x0=40000,x1=115000,X2=function(v){return L+(v-x0)*(R-L)/(x1-x0)};
   [['הבחירה שלכם',m.lo,m.hi,1],['מגדלי כיכר המדינה, ממוצע',C.avg,C.avg,0],['תל אביב יפו, חציון',C.ta,C.ta,0]].forEach(function(r,i){var y=24+i*36;
    s.appendChild(el('text',{x:R,y:y-9,'text-anchor':'end'},r[0]));
    s.appendChild(el('line',{x1:X2(x0),x2:X2(x1),y1:y,y2:y,stroke:'#e3e1da','stroke-width':6,'stroke-linecap':'round'}));
    if(r[3]){s.appendChild(el('line',{x1:X2(r[1]),x2:X2(r[2]),y1:y,y2:y,stroke:'#2f6f86','stroke-width':8,'stroke-linecap':'round'}));
     s.appendChild(el('text',{x:X2(r[1]),y:y+17,'text-anchor':'middle'},nf(r[1])));s.appendChild(el('text',{x:X2(r[2]),y:y+17,'text-anchor':'middle'},nf(r[2])))}
    else{s.appendChild(el('circle',{cx:X2(r[1]),cy:y,r:5.5,fill:'#1f4b5c',stroke:'#fff','stroke-width':2}));s.appendChild(el('text',{x:X2(r[1]),y:y+17,'text-anchor':'middle'},nf(r[1])))}});
   s.setAttribute('aria-label',m.label+': '+nf(m.lo)+' עד '+nf(m.hi)+' ₪ למ״ר, מול ממוצע המגדלים כ-65,000 ₪ ותל אביב יפו 52,856 ₪');
  }}
 function run(){var m=mode(),a=+q('a').value,fl=+q('fs').value,lo,hi;
  q('fl').hidden=!m.floor;q('ao').innerHTML=isl(a)+' מ״ר';q('fo').innerHTML='קומה '+isl(fl);
  if(m.floor){var p=m.lo_floor1+(fl-1)*(m.hi_floor39-m.lo_floor1)/38;lo=p*(1-m.band);hi=p*(1+m.band)}else{lo=m.lo;hi=m.hi}
  var mid=(lo+hi)/2*a,t=tax(mid,val('nlpg-t')==='more'?C.tax2:C.tax1);
  q('p').innerHTML=isl(mil(lo*a)+'-'+mil(hi*a))+' מיליון ₪';q('pm').innerHTML='כ-'+isl(nf(lo)+'-'+nf(hi))+' ₪ למ״ר';
  q('tx').innerHTML='כ-'+isl(new Intl.NumberFormat('he-IL').format(Math.round(t/1000)*1000))+' ₪';q('tt').innerHTML='כ-'+isl(mil(mid+t))+' מיליון ₪';
  q('why').textContent=m.why;draw(m,lo,hi,fl);
  var w=q('wa');if(w&&C.wa){var tx='שלום, בדקתי במחירון של מגדלי כיכר המדינה: '+m.label+', '+a+' מ״ר'+(m.floor?', קומה '+fl:'')+', אומדן '+mil(lo*a)+'-'+mil(hi*a)+' מיליון ₪. אשמח לפרטים נוספים (nad-lan.co.il)';w.href='https://wa.me/'+C.wa+'?text='+encodeURIComponent(tx)}}
 f.addEventListener('input',run);f.addEventListener('change',run);f.addEventListener('submit',function(e){e.preventDefault()});
 var mb=root.querySelector('.nlpg__more');if(mb)mb.addEventListener('click',function(){root.classList.add('is-open');mb.setAttribute('aria-expanded','true');var g=root.querySelector('.nlpg__grp--more .nlpg__gh th');if(g){g.setAttribute('tabindex','-1');g.focus({preventScroll:true})}});
 run()}
var all=document.querySelectorAll('.nlpg');for(var i=0;i<all.length;i++)one(all[i])})();
NLPG_JS;
		if ( '' === $wa ) {
			$html = (string) preg_replace( '#<a class="nlds-btn nlds-btn--primary nlpg__wa"[^>]*>.*?</a>#s', '', $html );
			$html = str_replace( '&quot;wa&quot;:&quot;{{WA}}&quot;', '&quot;wa&quot;:&quot;&quot;', $html );
		}
		return '<style id="nlpg-css">' . $css . '</style>' . str_replace( '{{WA}}', $wa, $html ) . '<script id="nlpg-js">' . $js . '</script>';
	}
}

if ( ! function_exists( 'nadlan_ps_film_t' ) ) {
	/** ProjectFilm v80 (5.10.2026): the film's button and player strings in the page's language (he, en, fr, ru, ar); the language
	 *  pages show the English film, and fr/ru/ar say so. */
	function nadlan_ps_film_t( $ps ) {
		$l = (string) ( $ps['lang'] ?? 'he' );
		$T = array(
			'he' => array( 'btn' => 'סרטון הפרויקט', 'secs' => 'שניות', 'upd' => 'עודכן', 'note' => 'הדמיה להמחשה. כל נתון עם המקור שלו.', 'close' => 'סגירה', 'dir' => 'rtl' ),
			'en' => array( 'btn' => 'Project film', 'secs' => 'seconds', 'upd' => 'updated', 'note' => 'Illustrative visualisation. Every figure has its source.', 'close' => 'Close', 'dir' => 'ltr' ),
			'fr' => array( 'btn' => 'Film du projet', 'secs' => 'secondes', 'upd' => 'mis à jour le', 'note' => 'Visualisation illustrative. Film en anglais.', 'close' => 'Fermer', 'dir' => 'ltr' ),
			'ru' => array( 'btn' => 'Фильм о проекте', 'secs' => 'сек.', 'upd' => 'обновлено', 'note' => 'Иллюстративная визуализация. Фильм на английском языке.', 'close' => 'Закрыть', 'dir' => 'ltr' ),
			'ar' => array( 'btn' => 'فيلم المشروع', 'secs' => 'ثانية', 'upd' => 'آخر تحديث', 'note' => 'تصور توضيحي. الفيلم باللغة الإنجليزية.', 'close' => 'إغلاق', 'dir' => 'rtl' ),
		);
		if ( ! isset( $T[ $l ] ) ) { $l = 'he'; }
		return $T[ $l ] + array( 'lang' => $l );
	}
}

/* ProjectFilm v79 (design system, 28.9.2026): the project's film in a dialog, and a VideoObject for search. The button is in
   the hero's button row; the dialog loads the wide film on screens over 700 px and the upright one on phones, only when the
   button is pressed, and plays it (the visitor chose it). Escape, the close button and the veil close it. */
add_action( 'wp_head', function () {
	$ps = nadlan_ps_current();
	if ( ! $ps || empty( $ps['film']['wide'] ) ) { return; }
	$f = $ps['film'];
	$ld = array(
		'@context' => 'https://schema.org', '@type' => 'VideoObject',
		'name' => (string) ( 'he' === nadlan_ps_film_t( $ps )['lang'] ? $ps['name'] : ( $f['name'] ?? $ps['name'] ) ) . ': ' . nadlan_ps_film_t( $ps )['btn'], 'description' => (string) $f['desc'],
		'thumbnailUrl' => array( $f['poster_wide'], $f['poster_tall'] ), 'uploadDate' => $f['date'] . 'T09:00:00+03:00',
		'duration' => 'PT' . (int) $f['secs'] . 'S', 'contentUrl' => $f['wide'], 'inLanguage' => (string) ( $f['lang'] ?? 'he' ),
		'publisher' => array( '@type' => 'Organization', 'name' => 'נדל״ן', 'url' => home_url( '/' ) ),
	);
	echo '<script type="application/ld+json" id="nadlan-ps-film">' . wp_json_encode( $ld, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES ) . '</script>' . "\n";
	echo '<style id="nadlan-ps-film-css">'
		. ':root body .nlds .nlps-hero__film{gap:10px}'
		. ':root body .nlds .nlps-hero__film small{font-weight:600;color:#6B6558}'
		. '.nlps-film__pl{width:26px;height:26px;border-radius:50%;background:#1F4B5C;display:inline-grid;place-items:center;flex:none}'
		. '.nlps-film__pl::before{content:"";margin-left:3px;border-style:solid;border-width:6px 0 6px 10px;border-color:transparent transparent transparent #fff}'
		. 'dialog.nlfilm{padding:0;border:0;background:transparent;width:min(1100px,calc(100vw - 32px));max-width:none;max-height:calc(100svh - 32px);overflow:visible}'
		. 'dialog.nlfilm::backdrop{background:rgba(20,19,15,.82)}'
		. '.nlfilm-box{position:relative;border-radius:18px;overflow:hidden;background:#14130F;box-shadow:0 30px 80px rgba(0,0,0,.5)}'
		. '.nlfilm-v{display:block;width:100%;height:auto;max-height:calc(100svh - 176px);background:#14130F}'
		. '.nlfilm-bar{display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:6px 14px;padding:12px 16px;background:#FAF7F1;font:600 14px/1.45 Heebo,Assistant,sans-serif;color:#3B4753}'
		. '.nlfilm-bar b{color:#1B1A17;font-weight:700}'
		. '.nlfilm-x{position:absolute;top:-56px;inset-inline-end:0;z-index:2;width:44px;height:44px;border-radius:50%;border:0;background:rgba(250,247,241,.95);color:#1B1A17;font:700 20px/44px Heebo,sans-serif;cursor:pointer;padding:0}'
		. '@media(max-width:700px){dialog.nlfilm{width:min(420px,calc(100vw - 24px))}.nlfilm-bar{font-size:13px}}'
		. '</style>' . "\n";
}, 998 );
add_action( 'wp_footer', function () {
	$ps = nadlan_ps_current();
	if ( ! $ps || empty( $ps['film']['wide'] ) ) { return; }
	$f = $ps['film'];
	$ft = nadlan_ps_film_t( $ps ); // ProjectFilm v80: the player in the page's language
	$fn = 'he' === $ft['lang'] ? $ps['name'] : (string) ( $f['name'] ?? $ps['name'] );
	echo '<dialog id="nlfilm" class="nlfilm" dir="' . esc_attr( $ft['dir'] ) . '" lang="' . esc_attr( $ft['lang'] ) . '" aria-label="' . esc_attr( $ft['btn'] . ': ' . $fn ) . '"'
		. ' data-wide="' . esc_url( $f['wide'] ) . '" data-tall="' . esc_url( $f['tall'] ) . '" data-pw="' . esc_url( $f['poster_wide'] ) . '" data-pt="' . esc_url( $f['poster_tall'] ) . '">'
		. '<button type="button" class="nlfilm-x" aria-label="' . esc_attr( $ft['close'] ) . '">&#10005;</button><div class="nlfilm-box">'
		. '<video class="nlfilm-v" controls playsinline preload="none"></video>'
		. '<div class="nlfilm-bar"><span><b>' . esc_html( $fn ) . '</b> · ' . esc_html( $ft['btn'] ) . ' · ' . (int) $f['secs'] . ' ' . esc_html( $ft['secs'] ) . ' · ' . esc_html( $ft['upd'] ) . ' ' . esc_html( $f['date_he'] ) . '</span><span>' . esc_html( $ft['note'] ) . '</span></div>'
		. '</div></dialog>'
		. '<script id="nadlan-ps-film-js">(function(){var d=document.getElementById("nlfilm");if(!d||!d.showModal)return;var v=d.querySelector("video");'
		. 'function open(e){if(e)e.preventDefault();var tall=window.matchMedia("(max-width:700px)").matches;var src=d.getAttribute(tall?"data-tall":"data-wide");'
		. 'if(v.getAttribute("src")!==src){v.setAttribute("poster",d.getAttribute(tall?"data-pt":"data-pw"));v.setAttribute("src",src);}'
		. 'd.showModal();var p=v.play();if(p&&p.catch)p.catch(function(){});}'
		. 'document.addEventListener("click",function(e){var a=e.target&&e.target.closest?e.target.closest("[data-nlps-ev=hero-film]"):null;if(a)open(e);});'
		. 'd.querySelector(".nlfilm-x").addEventListener("click",function(){d.close();});'
		. 'd.addEventListener("click",function(e){if(e.target===d)d.close();});'
		. 'd.addEventListener("close",function(){v.pause();});'
		. 'if(location.hash==="#nlfilm")setTimeout(open,600);})();</script>' . "\n";
}, 50 );

if ( ! function_exists( 'nadlan_ps_world_film' ) ) {
	/** KikarHamedinaWorld v104.28 (3.10.2026, the owner's order: "English goes to all the foreign languages and Hebrew to the Hebrew
	 *  ... somewhere downstairs"): the project's film after the deals, in the page's language. A native video with no autoplay and
	 *  no download until pressed (preload none); the wide film over 700 px, the upright one on phones; labelled as an illustration.
	 *  Hebrew film on the Hebrew page, the English film on en/fr/ru/ar. No VideoObject while the film is a draft for his decision. */
	function nadlan_ps_world_film( $ps ) {
		if ( empty( $ps['world'] ) || 'hamedina' !== (string) ( $ps['slug'] ?? '' ) ) { return ''; }
		$lang = (string) ( $ps['lang'] ?? 'he' );
		$T = array(
			'he' => array( 'הסרט של כיכר המדינה', 'דקה וחצי על הפרויקט: בחירת הדירה, הנוף מהקומות, העיצוב, המתקנים והסביבה.', 'הדמיה להמחשה', 'rtl' ),
			'en' => array( 'The Kikar Hamedina film', 'Ninety seconds on the project: choosing an apartment, the view from the floors, the finishes, the facilities and the area.', 'Illustrative visualisation', 'ltr' ),
			'fr' => array( 'Le film de Kikar Hamedina', 'Une minute et demie sur le projet : le choix d’un appartement, la vue depuis les étages, les finitions, les équipements et le quartier. Film en anglais.', 'Visualisation illustrative', 'ltr' ),
			'ru' => array( 'Фильм о Кикар ха-Медина', 'Полторы минуты о проекте: выбор квартиры, вид с этажей, отделка, удобства и район. Фильм на английском языке.', 'Иллюстративная визуализация', 'ltr' ),
			'ar' => array( 'فيلم كيكار همدينا', 'دقيقة ونصف عن المشروع: اختيار الشقة، الإطلالة من الطوابق، التشطيبات، المرافق والمنطقة. الفيلم باللغة الإنجليزية.', 'تصور توضيحي', 'rtl' ),
		);
		if ( ! isset( $T[ $lang ] ) ) { $lang = 'he'; }
		$t = $T[ $lang ];
		$k = 'he' === $lang ? 'he' : 'en';
		$u = 'https://nad-lan.co.il/wp-content/uploads/2026/10/kikar-hamedina-film-';
		$v = function ( $f, $cls ) use ( $u, $k ) {
			return '<video class="nlws-film__v nlws-film__v--' . $cls . '" controls playsinline preload="none" data-nlposter="' . esc_url( $u . $k . '-' . $f . '-preview-poster.jpg' ) . '">'
				. '<source src="' . esc_url( $u . $k . '-' . $f . '-preview.mp4' ) . '" type="video/mp4">'
				. '<track kind="captions" srclang="' . $k . '" label="' . ( 'he' === $k ? 'עברית' : 'English' ) . '" src="' . esc_url( rest_url( 'nadlan/v1/film-cc/v1-' . $k ) ) . '"></video>'; // v104.42
		};
		return '<section class="nlws-film" id="nlws-film" dir="' . $t[3] . '" lang="' . esc_attr( $lang ) . '" aria-labelledby="nlws-film-h">'
			. '<h2 id="nlws-film-h">' . esc_html( $t[0] ) . '</h2><p class="nlws-film__p">' . esc_html( $t[1] ) . '</p>'
			. nadlan_ps_world_film_v2( $k, $t[2] ) // v104.40: the narrated v2 film leads (Ben, 3.10 evening)
			. '<h3 class="nlws-film__v1h">' . esc_html( array( 'he' => 'הגרסה הראשונה', 'en' => 'The first version', 'fr' => 'La première version', 'ru' => 'Первая версия', 'ar' => 'النسخة الأولى' )[ $lang ] ?? 'הגרסה הראשונה' ) . '</h3>'
			. '<figure class="nlws-film__fig">' . $v( '16x9', 'wide' ) . $v( '9x16', 'tall' ) . '<figcaption>' . esc_html( $t[2] ) . '</figcaption></figure>'
			. nadlan_ps_world_facilities_clip( $lang, $k ) . '</section>' // v104.36: the facilities clip, labelled before play (option B)
			. '<style id="nlws-film-css">:root body .nlps-page>.nlws-film{grid-column:1/-1;width:100%;box-sizing:border-box}.nlws-film{max-width:1100px;margin:40px auto 8px;padding:0 16px}.nlws-film h2{margin:0 0 6px}'
			. '.nlws-film__p{margin:0 0 14px;max-width:62ch;color:#4A5560}.nlws-film__fig{margin:0}'
			. '.nlws-film__v{display:block;width:100%;height:auto;border-radius:16px;background:#14130F}'
			. '.nlws-film__v--tall{display:none;max-width:420px;margin:0 auto}.nlws-film__v--wide{aspect-ratio:auto 16/9}.nlws-film__v--tall{aspect-ratio:auto 9/16}'
			. '@media(max-width:700px){.nlws-film__v--wide{display:none}.nlws-film__v--tall{display:block}}'
			. '.nlws-film figcaption{margin-top:8px;font-size:13px;color:#6B6558}</style>'
			. '<script id="nlws-film-lazy">(function(){var vs=document.querySelectorAll("video[data-nlposter]");if(!vs.length)return;var set=function(v){if(!v.getAttribute("poster")){v.setAttribute("poster",v.getAttribute("data-nlposter"));}};if(!("IntersectionObserver" in window)){for(var i=0;i<vs.length;i++){set(vs[i]);}return;}var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){set(e.target);io.unobserve(e.target);}});},{rootMargin:"800px 0px"});for(var j=0;j<vs.length;j++){io.observe(vs[j]);}})();</script>'; // v104.44 lazy posters (HAD-421)
	}
}

if ( ! function_exists( 'nadlan_ps_world_facilities_clip' ) ) {
	/** KikarHamedinaWorld v104.36 (3.10.2026, the film, option B; Maya's film-safe-slice verdict): the 19.7 s facilities clip
	 *  (pool, gym, spa, car park; our own rooms, no map layer; music only) under the film. The label is above the player, so it
	 *  is read before play. Facilities posters only; preload none, no autoplay. The URLs are the uploaded files, byte-checked. */
	function nadlan_ps_world_facilities_clip( $lang, $k ) {
		$F = array(
			'he' => array( 'המתקנים בבניין: בריכה, חדר כושר, ספא וחניון', 'הדמיית מתקנים להמחשה: לא צילום ולא מפרט רשמי, ואינה סיור מלא בפרויקט.' ),
			'en' => array( "The building's facilities: pool, gym, spa and car park", 'An illustrative visualisation of the facilities: not footage, not an official specification, and not a full tour of the project.' ),
			'fr' => array( "Les équipements de l'immeuble : piscine, salle de sport, spa et parking", "Une visualisation illustrative des équipements : ni un tournage, ni une spécification officielle, ni une visite complète du projet. Libellés en anglais." ),
			'ru' => array( 'Удобства в здании: бассейн, спортзал, спа и паркинг', 'Иллюстративная визуализация удобств: не съёмка, не официальная спецификация и не полный тур по проекту. Подписи на английском.' ),
			'ar' => array( 'مرافق المبنى: المسبح، النادي الرياضي، السبا وموقف السيارات', 'تصوّر توضيحي للمرافق: ليس تصويرًا حقيقيًا ولا مواصفات رسمية، وليس جولة كاملة في المشروع. التسميات بالإنجليزية.' ),
		);
		$f = isset( $F[ $lang ] ) ? $F[ $lang ] : $F['he'];
		$src = array(
			'he' => array( '16x9' => array( 'https://nad-lan.co.il/wp-content/uploads/2026/10/kikar-hamedina-facilities-he-16x9-1.mp4', 'https://nad-lan.co.il/wp-content/uploads/2026/10/kikar-hamedina-facilities-he-16x9-poster.jpg' ), '9x16' => array( 'https://nad-lan.co.il/wp-content/uploads/2026/10/kikar-hamedina-facilities-he-9x16-1.mp4', 'https://nad-lan.co.il/wp-content/uploads/2026/10/kikar-hamedina-facilities-he-9x16-poster.jpg' ) ),
			'en' => array( '16x9' => array( 'https://nad-lan.co.il/wp-content/uploads/2026/10/kikar-hamedina-facilities-en-16x9-1.mp4', 'https://nad-lan.co.il/wp-content/uploads/2026/10/kikar-hamedina-facilities-en-16x9-poster.jpg' ), '9x16' => array( 'https://nad-lan.co.il/wp-content/uploads/2026/10/kikar-hamedina-facilities-en-9x16-1.mp4', 'https://nad-lan.co.il/wp-content/uploads/2026/10/kikar-hamedina-facilities-en-9x16-poster.jpg' ) ),
		);
		$s = $src[ 'he' === $k ? 'he' : 'en' ];
		$v = function ( $fmt, $cls ) use ( $s ) {
			return '<video class="nlws-film__v nlws-film__v--' . $cls . '" controls playsinline preload="none" data-nlposter="' . esc_url( $s[ $fmt ][1] ) . '">'
				. '<source src="' . esc_url( $s[ $fmt ][0] ) . '" type="video/mp4"></video>';
		};
		return '<div class="nlws-film__fac" id="nlws-facilities"><h3>' . esc_html( $f[0] ) . '</h3><p class="nlws-film__lbl">' . esc_html( $f[1] ) . '</p>'
			. '<figure class="nlws-film__fig">' . $v( '16x9', 'wide' ) . $v( '9x16', 'tall' ) . '</figure></div>'
			. '<style id="nlws-fac-css">.nlws-film__fac{margin-top:28px}.nlws-film__fac h3{margin:0 0 6px;font-size:20px}'
			. '.nlws-film__lbl{margin:0 0 12px;max-width:62ch;font-size:14px;color:#4A4740;background:#F3EEE3;border-radius:10px;padding:8px 12px}'
			. '.nlws-film__fac .nlws-film__v--tall{max-width:360px}</style>';
	}
}

if ( ! function_exists( 'nadlan_ps_world_film_v2' ) ) {
	/** KikarHamedinaWorld v104.40 (3.10.2026 evening, Ben: "upload everything, with the narration too"; nothing about credit on the
	 *  page): the narrated v2 film leads the film section. Hebrew on he, English elsewhere; preload none, no autoplay; the film's own
	 *  title-card poster. The wide film over 700 px, the upright one on phones (the same pattern as V1). */
	function nadlan_ps_world_film_v2( $k, $cap ) {
		$s = array( 'he' => array( '16x9' => array( 'https://nad-lan.co.il/wp-content/uploads/2026/10/kikar-hamedina-film-v2-he-16x9-1.mp4', 'https://nad-lan.co.il/wp-content/uploads/2026/10/kikar-hamedina-film-v2-he-16x9-poster.jpg' ), '9x16' => array( 'https://nad-lan.co.il/wp-content/uploads/2026/10/kikar-hamedina-film-v2-he-9x16-1.mp4', 'https://nad-lan.co.il/wp-content/uploads/2026/10/kikar-hamedina-film-v2-he-9x16-poster.jpg' ) ),
			'en' => array( '16x9' => array( 'https://nad-lan.co.il/wp-content/uploads/2026/10/kikar-hamedina-film-v2-en-16x9-1.mp4', 'https://nad-lan.co.il/wp-content/uploads/2026/10/kikar-hamedina-film-v2-en-16x9-poster.jpg' ), '9x16' => array( 'https://nad-lan.co.il/wp-content/uploads/2026/10/kikar-hamedina-film-v2-en-9x16-1.mp4', 'https://nad-lan.co.il/wp-content/uploads/2026/10/kikar-hamedina-film-v2-en-9x16-poster.jpg' ) ) );
		$cl = 'he' === $k ? 'he' : 'en';
		$f = $s[ $cl ];
		// v104.41: captions in the narration's language, off by default (the player's CC button)
		$cc = '<track kind="captions" srclang="' . $cl . '" label="' . ( 'he' === $cl ? 'עברית' : 'English' ) . '" src="' . esc_url( rest_url( 'nadlan/v1/film-cc/' . $cl ) ) . '">';
		$v = function ( $fmt, $cls ) use ( $f, $cc ) {
			return '<video class="nlws-film__v nlws-film__v--' . $cls . '" controls playsinline preload="none" data-nlposter="' . esc_url( $f[ $fmt ][1] ) . '">'
				. '<source src="' . esc_url( $f[ $fmt ][0] ) . '" type="video/mp4">' . $cc . '</video>';
		};
		return '<figure class="nlws-film__fig nlws-film__v2" id="nlws-film-v2">' . $v( '16x9', 'wide' ) . $v( '9x16', 'tall' ) . '<figcaption>' . esc_html( $cap ) . '</figcaption></figure>'
			. '<style id="nlws-v2-css">.nlws-film__v2{margin:0 0 26px}.nlws-film__v1h{margin:8px 0;font-size:18px}.nlws-film video::cue{font-family:Heebo,Arial,sans-serif;color:#FAF7F1;background:rgba(27,26,23,.82)}</style>';
	}
}

if ( ! function_exists( 'nadlan_ps_film_cc_route' ) ) {
	/** v104.41 (3.10.2026 night): the narrated film's captions as text/vtt. The uploads folder serves .vtt as
	 *  application/octet-stream, which a browser may refuse for a <track>; this route serves the same media file
	 *  (he 8172, en 8173) with the caption type. Public and read-only, like the file itself. */
	function nadlan_ps_film_cc_route() {
		register_rest_route( 'nadlan/v1', '/film-cc/(?P<lang>he|en|v1-he|v1-en)', array(
			'methods'             => 'GET',
			'permission_callback' => '__return_true',
			'callback'            => function ( $r ) {
				$id = array( 'he' => 8172, 'en' => 8173, 'v1-he' => 8174, 'v1-en' => 8175 )[ (string) $r['lang'] ] ?? 0;
				$p  = $id ? get_attached_file( $id ) : '';
				$t  = ( $p && is_readable( $p ) ) ? (string) file_get_contents( $p ) : '';
				if ( 0 !== strpos( $t, 'WEBVTT' ) ) {
					return new WP_Error( 'nadlan_film_cc', 'not found', array( 'status' => 404 ) );
				}
				header( 'Content-Type: text/vtt; charset=utf-8' );
				header( 'Cache-Control: public, max-age=86400' );
				echo $t; // a caption file from the media library, served as it is
				exit;
			},
		) );
	}
	add_action( 'rest_api_init', 'nadlan_ps_film_cc_route' );
}

if ( ! function_exists( 'nadlan_pms_off' ) ) {
	/** HAD-421 (5.10.2026, phone speed): Paid Member Subscriptions prints Stripe (js.stripe.com, about 250 KB) and three more
	 *  scripts plus its stylesheet on every page. Our own templates hold no PMS form, so they drop them: project pages and the
	 *  catalogue, listings and their archive, the brokers directory and the broker sites under it. A page whose content carries
	 *  a PMS shortcode keeps them. Dequeued, never deregistered, so a script that depends on one still pulls it in. */
	function nadlan_pms_off() {
		if ( is_admin() ) { return; }
		$types = array( 'nadlan_project', 'nadlan_property', 'nadlan_professional' );
		$ours  = is_singular( $types ) || is_post_type_archive( $types ) || is_page( 'brokers' );
		if ( ! $ours && is_page() ) {
			$dir  = get_page_by_path( 'brokers' );
			$ours = $dir && (int) wp_get_post_parent_id( get_queried_object_id() ) === (int) $dir->ID;
		}
		if ( ! $ours ) { return; }
		$p = get_post( get_queried_object_id() );
		if ( $p instanceof WP_Post && false !== strpos( (string) $p->post_content, '[pms-' ) ) { return; }
		foreach ( array( 'pms-stripe-js', 'pms-stripe-script', 'pms-front-end', 'pms-frontend-discount-code-js' ) as $h ) { wp_dequeue_script( $h ); }
		wp_dequeue_style( 'pms-style-front-end' );
	}
	add_action( 'wp_enqueue_scripts', 'nadlan_pms_off', 9999 );
	add_action( 'wp_print_footer_scripts', 'nadlan_pms_off', 1 );
}

if ( ! function_exists( 'nadlan_dash_off' ) ) {
	/** HAD-421 (5.10.2026): dashicons (36 KB) loads for every visitor, yet no dashicons class is used on our templates. Visitors
	 *  who are not signed in no longer get it on project pages, listings and the broker pages (the same templates as
	 *  nadlan_pms_off). Signed-in users keep it for the admin bar; a style that depends on it still pulls it in. */
	function nadlan_dash_off() {
		if ( is_admin() ) { return; }
		$types = array( 'nadlan_project', 'nadlan_property', 'nadlan_professional' );
		$ours  = is_singular( $types ) || is_post_type_archive( $types ) || is_page( 'brokers' );
		if ( ! $ours && is_page() ) {
			$dir  = get_page_by_path( 'brokers' );
			$ours = $dir && (int) wp_get_post_parent_id( get_queried_object_id() ) === (int) $dir->ID;
		}
		if ( ! $ours ) { return; }
		wp_dequeue_style( 'pms_block_themes_front_end_stylesheet' ); // the PMS stylesheet nadlan_pms_off missed
		if ( ! is_user_logged_in() ) {
			// wp-jquery-ui-dialog depends on dashicons and pulled it back in (the first 1.72.423 run rolled back); no jQuery UI
			// dialog script is on these pages, so its stylesheet styles nothing here
			wp_dequeue_style( 'wp-jquery-ui-dialog' );
			wp_dequeue_style( 'dashicons' );
		}
	}
	add_action( 'wp_enqueue_scripts', 'nadlan_dash_off', 9999 );
	add_action( 'wp_print_styles', 'nadlan_dash_off', 1 );         // a style enqueued after wp_enqueue_scripts (the 2nd run's lesson)
	add_action( 'wp_print_footer_scripts', 'nadlan_dash_off', 1 ); // a late style printed in the footer
}

if ( ! function_exists( 'nadlan_leaflet_css_async' ) ) {
	/** HAD-421 (5.10.2026): on a project page the area map is far below the stage, yet leaflet.css (unpkg.com, a third origin)
	 *  blocked the first paint behind a new connection. Here it loads without blocking (media print, switched to all on load),
	 *  with a noscript copy. Other templates keep the plain tag. */
	function nadlan_leaflet_css_async( $tag, $handle, $href, $media ) {
		if ( 'leaflet' !== $handle || is_admin() || ! is_singular( 'nadlan_project' ) || false !== strpos( $tag, 'onload=' ) ) { return $tag; }
		$async = str_replace( "media='" . $media . "'", "media='print' onload=\"this.media='all'\"", $tag );
		if ( $async === $tag ) { return $tag; }
		return $async . '<noscript>' . trim( $tag ) . '</noscript>' . "\n";
	}
	add_filter( 'style_loader_tag', 'nadlan_leaflet_css_async', 10, 4 );
}

if ( ! function_exists( 'nadlan_leaflet_off' ) ) {
	/** HAD-421 (5.10.2026): a project page with a Mapbox token renders the Mapbox area map; the Leaflet fallback element is
	 *  printed only without a token (project-experience.php), yet Leaflet js + css loaded anyway as a dependency of
	 *  nadlan-pjx-js. With a token, the dependency is dropped and Leaflet is not loaded; the inline code is guarded by window.L. */
	function nadlan_leaflet_off() {
		if ( is_admin() || ! is_singular( 'nadlan_project' ) ) { return; }
		if ( ! function_exists( 'nadlan_mapbox_token' ) || '' === (string) nadlan_mapbox_token() ) { return; }
		$ws = wp_scripts();
		if ( isset( $ws->registered['nadlan-pjx-js'] ) ) {
			$ws->registered['nadlan-pjx-js']->deps = array_values( array_diff( (array) $ws->registered['nadlan-pjx-js']->deps, array( 'leaflet' ) ) );
		}
		wp_dequeue_script( 'leaflet' );
		wp_dequeue_style( 'leaflet' );
	}
	add_action( 'wp_enqueue_scripts', 'nadlan_leaflet_off', 9999 );
}

if ( ! function_exists( 'nadlan_theme_css_once' ) ) {
	/** HAD-421 (5.10.2026): the parent theme printed style.min.css early and the child theme printed the identical style.css
	 *  later in the head (the same 287 rules). The later copy wins every rule, so the earlier handle keeps its place for its
	 *  dependents but prints no file. Only when the child's copy is really on the page. */
	function nadlan_theme_css_once() {
		if ( is_admin() ) { return; }
		$ws = wp_styles();
		if ( ! isset( $ws->registered['nadlan-revenue-style'], $ws->registered['nlpc-parent-style'] ) ) { return; }
		if ( ! wp_style_is( 'nlpc-parent-style', 'enqueued' ) ) { return; }
		$early = (string) $ws->registered['nadlan-revenue-style']->src;
		$late  = (string) $ws->registered['nlpc-parent-style']->src;
		if ( false === strpos( $early, '/themes/nadlan-revenue/style.min.css' ) || false === strpos( $late, '/themes/nadlan-revenue/style.css' ) ) { return; }
		$ws->registered['nadlan-revenue-style']->src = false;
	}
	add_action( 'wp_print_styles', 'nadlan_theme_css_once', 1 );
}

if ( ! function_exists( 'nadlan_ps_langs_on' ) ) {
	/** HAD-361: the stage on the language pages. On for everyone since 1.72.351 (StageLanguages v90: the rendered audit of
	 *  16 pages, the phone and content-order checks passed); option nadlan_ps_langs = '0' turns it off, ?nlstage=1 previews. */
	function nadlan_ps_langs_on() {
		if ( '1' === (string) get_option( 'nadlan_ps_langs', '1' ) ) { return true; }
		return isset( $_GET['nlstage'] ) && '1' === sanitize_key( wp_unslash( $_GET['nlstage'] ) ); // phpcs:ignore
	}
}

/* HAD-361: on a language page with a stage, the dictionary for the browser's translator and the translator itself, as a
   classic script during parsing, so it watches the page before the stage's modules (deferred) draw anything. */
add_action( 'wp_footer', function () {
	$ps = nadlan_ps_current();
	if ( ! $ps || 'he' === ( $ps['lang'] ?? 'he' ) || ! empty( $ps['world'] ) ) { return; } // KikarHamedinaWorld v104: the world speaks the page's language itself
	$lang = (string) $ps['lang'];
	$out  = array( 'lang' => $lang, 'exact' => array(), 'names' => array(), 'patterns' => array() );
	foreach ( array( 'lang-pages.json', 'stage-dict.json' ) as $f ) {
		$p = dirname( __DIR__ ) . '/i18n/' . $f;
		$d = is_readable( $p ) ? json_decode( (string) file_get_contents( $p ), true ) : null;
		if ( ! is_array( $d ) ) { continue; }
		foreach ( (array) ( $d['exact'] ?? array() ) as $he => $tr ) { if ( isset( $tr[ $lang ] ) ) { $out['exact'][ $he ] = (string) $tr[ $lang ]; } }
		foreach ( (array) ( $d['names'] ?? array() ) as $he => $tr ) { if ( isset( $tr[ $lang ] ) ) { $out['names'][ $he ] = (string) $tr[ $lang ]; } }
		foreach ( (array) ( $d['patterns'] ?? array() ) as $pt ) { if ( ! empty( $pt['re'] ) && isset( $pt[ $lang ] ) ) { $out['patterns'][] = array( 're' => (string) $pt['re'], 'tr' => (string) $pt[ $lang ] ); } }
	}
	echo '<script type="application/json" id="nadlan-stage-i18n">' . wp_json_encode( $out, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES | JSON_HEX_TAG ) . '</script>' . "
";
	$js = dirname( __DIR__ ) . '/assets/project-stage/i18n-dom.js';
	if ( is_readable( $js ) ) { echo '<script id="nadlan-stage-i18n-js">' . str_replace( '</', '<\/', (string) file_get_contents( $js ) ) . '</script>' . "
"; } // phpcs:ignore -- inline: '</' escaped so nothing closes the script early
}, 5 );
