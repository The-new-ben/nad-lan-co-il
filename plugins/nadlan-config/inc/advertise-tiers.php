<?php
/**
 * nadlan-config - Advertising tiers on /advertise/ (local patch 26.10.2026, not live).
 *
 * Ben, 26.10.2026: an advertiser clicks, picks a level of exposure and pays by himself, without Ben handling
 * it, and it must never hurt organic SEO. No new URL: the section rides the existing page /advertise/ (the
 * head word "advertise" is owned there), right before its "נדבר?" chapter, and is built only on products the
 * shop already sells (475 basic, 476 Pro, 477 Premier, 489 project campaign, 490 promoted property, the
 * content sponsorship in option nadlan_procard_product = 5403) plus two optional products Ben may create:
 * the area package (option nadlan_adt_area_product) and the advertiser story (option nadlan_adt_story_product).
 * Until an optional product exists, choosing it opens the "הזמנה בחשבונית" form (a lead with topic
 * "הזמנת פרסום בחשבונית"); the same form serves every choice while option nadlan_adt_checkout_live is not '1'.
 *
 * The self-serve path (?nladt_pick=476,5403): login, then the cart gets the chosen products with the card
 * attached (the user's own professional card; for the urban-renewal track a draft "ארגון דיירים" card is
 * opened when the user has none, and it is published when the payment activates it), then checkout.
 * Payment activation, auto-expiry and renewal invoices are the existing code (advertiser-orders.php,
 * pro-cards.php sponsorship, renewals.php). The area package also opens a DRAFT placement (placements.php)
 * with the dates filled; the pages are chosen and published by an admin, never automatically.
 *
 * SEO: the section adds no title, no H1 and no slug; its links are internal; paid surfaces follow
 * inc/ad-safety.php (patch 01, apply first). Language: no tech words, no long dashes (language-dna).
 * Design: NadLan Instruments tokens (ink #12202A, sea #2F6F86, deep #1F4B5C, line #D3DCE2; IBM Plex Sans
 * Hebrew + IBM Plex Mono). Preview: docs/research/2026-10-26-advertisers/advertise-tiers/preview.html.
 */
if ( ! defined( 'ABSPATH' ) ) { exit; }

if ( ! function_exists( 'nadlan_adt_checkout_live' ) ) {
	function nadlan_adt_checkout_live() { return '1' === (string) get_option( 'nadlan_adt_checkout_live', '0' ); }
}

if ( ! function_exists( 'nadlan_adt_extra' ) ) {
	/** The optional products: 0 until Ben creates them in WooCommerce. */
	function nadlan_adt_extra( $key ) {
		$opt = array( 'area' => 'nadlan_adt_area_product', 'story' => 'nadlan_adt_story_product' );
		return isset( $opt[ $key ] ) ? (int) get_option( $opt[ $key ], 0 ) : 0;
	}
}

if ( ! function_exists( 'nadlan_adt_price' ) ) {
	/** The live shop price when the product exists, else the listed fallback. */
	function nadlan_adt_price( $pid, $fallback ) {
		if ( $pid > 0 && function_exists( 'wc_get_product' ) ) {
			$p = wc_get_product( (int) $pid );
			if ( $p && '' !== (string) $p->get_price() ) { return (float) $p->get_price(); }
		}
		return (float) $fallback;
	}
}

if ( ! function_exists( 'nadlan_adt_tracks' ) ) {
	function nadlan_adt_tracks() {
		$spon  = (int) get_option( 'nadlan_procard_product', 5403 );
		$area  = nadlan_adt_extra( 'area' );
		$story = nadlan_adt_extra( 'story' );
		$basic = array( 'id' => 475, 'label' => 'כרטיס בסיסי', 'price' => 0, 'period' => 'ללא הגבלת זמן', 'small' => 'תמיד', 'meter' => 1 );
		$pro   = array( 'id' => 476, 'label' => 'פרופיל Pro', 'price' => nadlan_adt_price( 476, 349 ), 'period' => 'לחודש', 'small' => 'לחודש · הראשון חינם', 'first' => 'החודש הראשון חינם', 'meter' => 2,
			'feats' => array( 'טלפון ווואטסאפ גלויים', 'קישור לאתר שלכם', 'תמונות ותיאור מלא', 'פניות ישירות אליכם' ) );
		$prem  = array( 'id' => 477, 'label' => 'פרופיל Premier', 'price' => nadlan_adt_price( 477, 749 ), 'period' => 'לחודש', 'small' => 'לחודש', 'meter' => 3,
			'feats' => array( 'כל מה שב־Pro', 'קדימות בתוך המדריכים', 'תג פרופיל מאומת', 'צוות, פרויקטים וגלריה' ) );
		return array(
			'pro' => array(
				'tab' => 'בעלי מקצוע', 'who' => 'עורכי דין, שמאים, יועצי משכנתאות, בדק בית, אדריכלים ומעצבי פנים.', 'default' => 476,
				'levels' => array(
					$basic + array( 'sub' => 'שם, עיר ותחום במאגר אנשי המקצוע.' ),
					$pro + array( 'sub' => 'הפרופיל המלא שלכם, גלוי לכל מי שמחפש בתחום.' ),
					$prem + array( 'sub' => 'להוביל את התחום: קדימות בכרטיסי המומחים שבתוך המדריכים.' ),
				),
				'adds' => array(
					array( 'id' => $spon, 'label' => 'חסות על תחום תוכן', 'price' => nadlan_adt_price( $spon, 199 ), 'period' => 'ל־30 יום', 'small' => 'ל־30 יום', 'domain' => '1',
						'sub' => 'הכרטיס שלכם ראשון בכל המונחים והמדריכים של התחום שתבחרו, עם סימון "ממומן".' ),
				),
			),
			'renewal' => array(
				'tab' => 'התחדשות עירונית', 'who' => 'חברות מארגנות וליווי דיירים, עורכי דין ושמאים מטעם הדיירים, מפקחי בנייה.', 'default' => 477,
				'levels' => array(
					$basic + array( 'sub' => 'שם, עיר ותחום במאגר ארגון דיירים.' ),
					array_merge( $pro, array( 'sub' => 'פרופיל מלא עם הפרויקטים שאתם מלווים והדרך לפנות אליכם.', 'feats' => array( 'טלפון ווואטסאפ גלויים', 'קישור לאתר שלכם', 'הפרויקטים שאתם מלווים', 'פניות ישירות מנציגויות' ) ) ),
					array_merge( $prem, array( 'sub' => 'הכרטיס שלכם מוביל בכרטיסי המומחים שבתוך תכני ההתחדשות.' ) ),
					array( 'id' => $area ? $area : 'area', 'label' => 'חבילת אזור', 'price' => nadlan_adt_price( $area, 1490 ), 'period' => 'לחודש', 'small' => 'לחודש · מינימום 3', 'min' => 3, 'invoice' => $area ? '' : '1', 'meter' => 4, 'cities' => true,
						'sub' => 'Premier, ועוד כרטיס "פרסומת" בעמודי הערים שבהן אתם פועלים, ודוח חודשי פרטי.',
						'feats' => array( 'Premier כלול', 'עד 6 ערים לבחירתכם', 'מודעה אחת בעמוד, בלי צפיפות', 'דוח צפיות ופניות פרטי' ) ),
				),
				'adds' => array(
					array( 'id' => $spon, 'label' => 'חסות תחום: ליווי דיירים', 'price' => nadlan_adt_price( $spon, 199 ), 'period' => 'ל־30 יום', 'small' => 'ל־30 יום', 'domain' => 'organizer',
						'sub' => 'הכרטיס שלכם ראשון במונחים ובמדריכים של ארגון דיירים, עם סימון "ממומן".' ),
					array( 'id' => $story ? $story : 'story', 'label' => 'כתבת מפרסם בפרופיל', 'price' => nadlan_adt_price( $story, 1490 ), 'period' => 'חד פעמי', 'small' => 'חד פעמי', 'invoice' => '1',
						'sub' => 'כתבה בעברית ובאנגלית על החברה, כתובה בסטנדרט שלנו, בתוך הפרופיל שלכם ומסומנת "כתבת מפרסם".' ),
					array( 'id' => 'room', 'label' => 'חדר ניהול להתחדשות עירונית', 'price' => (int) get_option( 'nadlan_adt_room_price', 149 ), 'period' => 'למתחם לחודש', 'small' => 'למתחם לחודש · הראשון חינם', 'first' => 'החודש הראשון חינם', 'invoice' => '1', 'room' => '1',
						'sub' => 'לכל מתחם: מצב החתימה של כל דירה, המסמכים שחסרים, עשרת השלבים עם הצעד הבא, ועדכונים לדיירים בקישור אחד. לדיירים ולנציגות חינם.' ),
				),
			),
			'project' => array(
				'tab' => 'פרויקטים ונכסים', 'who' => 'יזמים, קבלנים וחברות שיווק, ובעלי נכס שרוצים במה.', 'default' => 490,
				'levels' => array(
					array( 'id' => 490, 'label' => 'נכס מקודם', 'price' => nadlan_adt_price( 490, 299 ), 'period' => 'ל־60 יום', 'small' => 'ל־60 יום', 'meter' => 2,
						'sub' => 'נכס בודד מודגש בתוצאות, עם תמונות, מיקום ופרטי קשר.' ),
					array( 'id' => 489, 'label' => 'קמפיין פרויקט', 'price' => nadlan_adt_price( 489, 3990 ), 'period' => 'ל־6 חודשים', 'small' => 'ל־6 חודשים', 'meter' => 3,
						'sub' => 'הפרויקט מובלט בקטלוג ובמפה, עם גלריה, תיאור מלא ופניות למתעניינים.', 'feats' => array( 'מובלט בקטלוג ובמפה', 'גלריה ותיאור מלא', 'פניות ברמת הדירה' ) ),
					array( 'id' => 'quote', 'label' => 'חוויית דגל לפרויקט', 'price' => null, 'period' => 'לפי היקף', 'small' => 'הצעה תוך יום עסקים', 'invoice' => '1', 'meter' => 4,
						'sub' => 'בחירת דירה מתוך הבניין, מפת סביבה וטופס פנייה ברמת הדירה. המחיר לפי היקף הפרויקט.' ),
				),
				'adds' => array(),
			),
		);
	}
}

if ( ! function_exists( 'nadlan_adt_money' ) ) {
	function nadlan_adt_money( $n ) { return null === $n ? 'לפי היקף' : '₪' . number_format( (float) $n, 0, '.', ',' ); }
}

if ( ! function_exists( 'nadlan_adt_cities' ) ) {
	function nadlan_adt_cities() {
		return (array) apply_filters( 'nadlan_adt_cities', array( 'רעננה', 'כפר סבא', 'הוד השרון', 'הרצליה', 'פתח תקווה', 'תל אביב יפו', 'רמת גן', 'גבעתיים', 'חולון', 'בת ים', 'ירושלים', 'חיפה' ) );
	}
}

if ( ! function_exists( 'nadlan_adt_item_attrs' ) ) {
	function nadlan_adt_item_attrs( $it ) {
		$a  = ' value="' . esc_attr( (string) $it['id'] ) . '" data-label="' . esc_attr( $it['label'] ) . '"';
		$a .= ' data-price="' . ( null === $it['price'] ? '' : esc_attr( (string) (float) $it['price'] ) ) . '" data-period="' . esc_attr( $it['period'] ) . '"';
		foreach ( array( 'first', 'min', 'invoice', 'domain' ) as $k ) {
			if ( ! empty( $it[ $k ] ) ) { $a .= ' data-' . $k . '="' . esc_attr( (string) $it[ $k ] ) . '"'; }
		}
		return $a;
	}
}

if ( ! function_exists( 'nadlan_adt_render' ) ) {
	function nadlan_adt_render() {
		$tracks = nadlan_adt_tracks();
		$h  = '<section class="nladt" id="nladt" dir="rtl" lang="he" data-live="' . ( nadlan_adt_checkout_live() ? '1' : '0' ) . '" data-cart="' . esc_url( home_url( '/' ) ) . '" data-lead="' . esc_url( rest_url( 'nadlan/v1/lead' ) ) . '">';
		$h .= '<header class="nladt__head"><div><p class="nladt__kick">מסלולי פרסום ומחירים</p><h2>בוחרים את רמת החשיפה, משלמים, והפרסום עולה</h2>'
			. '<p class="nladt__lead">כל מסלול מופעל מיד אחרי התשלום ונגמר לבד בסוף התקופה, אלא אם בחרתם לחדש. בלי חוזה ובלי התחייבות. כל מודעה מסומנת "פרסומת" או "ממומן", כדי שהקוראים ידעו, וכדי שזה יישאר הוגן.</p></div>';
		$h .= '<div class="nladt__tracks" role="group" aria-label="סוג המפרסם">';
		$first = true;
		foreach ( $tracks as $key => $t ) {
			$h .= '<button type="button" data-track="' . esc_attr( $key ) . '" aria-pressed="' . ( $first ? 'true' : 'false' ) . '">' . esc_html( $t['tab'] ) . '</button>';
			$first = false;
		}
		$h .= '</div></header><div class="nladt__body"><div>';
		$first = true;
		foreach ( $tracks as $key => $t ) {
			$h .= '<div class="nladt__track" data-panel="' . esc_attr( $key ) . '"' . ( $first ? '' : ' hidden' ) . '><p class="nladt__who">' . esc_html( $t['who'] ) . '</p>';
			if ( 'renewal' === $key ) {
				$h .= '<div class="nladt__pack" data-pack><p class="nladt__kick">החבילה המלאה לחברה מארגנת</p><h3>פרסום, תוכן וחדר ניהול לכל המתחמים שלכם</h3><ul>'
					. '<li><b>פרופיל Premier</b> בקטגוריית ארגון דיירים, עם הצוות והפרויקטים שאתם מלווים</li>'
					. '<li><b>חסות "ליווי דיירים"</b>: הכרטיס שלכם ראשון במדריכים ובמונחים של התחום</li>'
					. '<li><b>כתבת מפרסם</b> בעברית ובאנגלית בתוך הפרופיל, מסומנת "כתבת מפרסם"</li>'
					. '<li><b>חדר הניהול</b> לכל מתחם, והחודש הראשון חינם (<a href="' . esc_url( home_url( '/my-renewal/' ) ) . '">כך נראה חדר לדוגמה</a>)</li></ul>'
					. '<button type="button" class="nladt__packgo" data-pack-go>בחירת החבילה המלאה</button></div>';
			}
			$h .= '<ul class="nladt__ladder">';
			foreach ( $t['levels'] as $i => $lv ) {
				$rid = 'nladt-' . $key . '-' . $i;
				$chk = (string) $lv['id'] === (string) $t['default'] ? ' checked' : '';
				$h .= '<li class="nladt__lvl"><input type="radio" name="nladt-' . esc_attr( $key ) . '" id="' . esc_attr( $rid ) . '"' . nadlan_adt_item_attrs( $lv ) . $chk . '>'
					. '<label for="' . esc_attr( $rid ) . '"><span class="nladt__dot"></span><span><span class="nladt__name">' . esc_html( $lv['label'] ) . '</span><span class="nladt__sub">' . esc_html( $lv['sub'] ) . '</span></span>'
					. '<span class="nladt__price"><b>' . esc_html( nadlan_adt_money( $lv['price'] ) ) . '</b><small>' . esc_html( $lv['small'] ) . '</small></span>';
				if ( ! empty( $lv['feats'] ) ) {
					$h .= '<ul class="nladt__feat">';
					foreach ( $lv['feats'] as $f ) { $h .= '<li>' . esc_html( $f ) . '</li>'; }
					$h .= '</ul>';
				}
				$h .= '<span class="nladt__meter" aria-hidden="true">';
				for ( $m = 1; $m <= 4; $m++ ) { $h .= '<i' . ( $m <= (int) $lv['meter'] ? ' class="on"' : '' ) . '></i>'; }
				$h .= '<span>חשיפה ' . (int) $lv['meter'] . '/4</span></span>';
				if ( ! empty( $lv['cities'] ) ) {
					$h .= '<span class="nladt__cities" data-cities hidden><p>בחרו עד 6 ערים</p><span class="nladt__chips">';
					foreach ( nadlan_adt_cities() as $c ) { $h .= '<label class="nladt__chip"><input type="checkbox" value="' . esc_attr( $c ) . '"><span>' . esc_html( $c ) . '</span></label>'; }
					$h .= '</span></span>';
				}
				$h .= '</label></li>';
			}
			$h .= '</ul>';
			if ( $t['adds'] ) {
				$h .= '<div class="nladt__adds"><h3>תוספות</h3>';
				foreach ( $t['adds'] as $ad ) {
					$h .= '<label class="nladt__add"><input type="checkbox"' . nadlan_adt_item_attrs( $ad ) . '><span class="nladt__box"></span><span><span class="nladt__name">' . esc_html( $ad['label'] ) . '</span><span class="nladt__sub">' . esc_html( $ad['sub'] ) . '</span></span>'
						. '<span class="nladt__price"><b>' . esc_html( nadlan_adt_money( $ad['price'] ) ) . '</b><small>' . esc_html( $ad['small'] ) . '</small></span></label>';
				}
				$h .= '</div>';
			}
			$h .= '</div>';
			$first = false;
		}
		$h .= '</div><aside class="nladt__sum" aria-live="polite"><h3>ההזמנה שלכם</h3><ul class="nladt__rows" data-rows></ul>'
			. '<div class="nladt__total"><span>לתשלום היום</span><b data-total>₪0</b></div><p class="nladt__renew" data-renew></p>'
			. '<a class="nladt__go" data-go href="#nladt">להמשך ולתשלום</a><p class="nladt__pay" data-pay>אשראי · Bit · Google Pay · Apple Pay · חשבונית מס למייל</p>'
			. '<p class="nladt__note">צריך חשבון באתר. אם עוד אין לכם כרטיס, פותחים אחד בדקה אחרי התשלום, והפרסום נדלק עליו.</p></aside></div>';
		$h .= '<ol class="nladt__steps" aria-label="איך זה עובד">'
			. '<li class="nladt__step"><b>01</b><strong>בוחרים מסלול</strong><p>רמת חשיפה, תוספות, ובחבילת אזור גם את הערים.</p></li>'
			. ( nadlan_adt_checkout_live()
				? '<li class="nladt__step"><b>02</b><strong>משלמים באתר</strong><p>אשראי, Bit או ארנק דיגיטלי. החשבונית מגיעה למייל.</p></li>'
				: '<li class="nladt__step"><b>02</b><strong>מקבלים חשבונית</strong><p>שולחים הזמנה בלחיצה, והחשבונית מגיעה למייל. משלמים בהעברה או באשראי בטלפון.</p></li>' )
			. '<li class="nladt__step"><b>03</b><strong>' . ( nadlan_adt_checkout_live() ? 'הפרסום עולה מיד' : 'הפרסום עולה עם התשלום' ) . '</strong><p>על הכרטיס שלכם, עם התאריך שבו התקופה נגמרת, ב<a href="' . esc_url( home_url( '/advertiser-center/' ) ) . '">מרכז הפרסום</a>.</p></li>'
			. '<li class="nladt__step"><b>04</b><strong>מחדשים או עוצרים</strong><p>שלושה ימים לפני הסוף מגיעה חשבונית חידוש. לא שילמתם, הפרסום יורד לבד.</p></li></ol>';
		$h .= '<div class="nladt__fair"><div><h3>ככה זה נשאר הוגן</h3><ul>'
			. '<li>כל כרטיס בתשלום מסומן "ממומן" או "פרסומת", בכל מקום שהוא מופיע.</li>'
			. '<li>הקישור לאתר שלכם מסומן כקישור פרסומי, כמו שגוגל מבקש מכל אתר.</li>'
			. '<li>עד שלוש מודעות בעמוד, ומודעת אזור אחת בלבד בכל עמוד.</li>'
			. '<li>המדריכים שלנו נשארים בלי תוכן ממומן. הסיפור שלכם נמצא בפרופיל שלכם.</li>'
			. '<li>נתונים שהחברה מוסרת על עצמה מוצגים "לדברי החברה".</li>'
			. '<li>דירוג וביקורות לא נקנים בכסף.</li></ul></div>'
			. '<div class="nladt__spec" aria-label="כך נראית מודעה בתוך מדריך"><small>כך נראית מודעה בתוך מדריך</small>'
			. '<p class="nladt__guide">אחרי שבוחרים נציגות, הצעד הבא הוא עורך דין ושמאי מטעם הדיירים. את שכרם משלם היזם, והבחירה נשארת שלכם.</p>'
			. '<div class="nladt__ad"><span class="nladt__adtag">פרסומת</span><strong>שם החברה · ארגון דיירים</strong><span>רעננה, כפר סבא, הוד השרון</span></div></div></div>';
		$h .= '<p class="nladt__fine">המחירים כפי שהם מופיעים בחנות האתר. נדלן היא אתר תוכן ופרסום: אינה מתווכת, אינה צד להתקשרות בין המפרסם ללקוחותיו, ואינה ממליצה על מפרסם מסוים. <a href="' . esc_url( home_url( '/join-pro/' ) ) . '">כל המסלולים והמחירים</a></p>';
		$h .= '<dialog data-dlg><form method="dialog" data-form><h3>הזמנה בחשבונית</h3><p data-dlg-what></p>'
			. '<label>שם מלא<input name="name" autocomplete="name" required></label>'
			. '<label>טלפון<input name="phone" type="tel" autocomplete="tel" inputmode="tel" required></label>'
			. '<label>אימייל לחשבונית<input name="email" type="email" autocomplete="email"></label>'
			. '<input name="company" tabindex="-1" autocomplete="off" aria-hidden="true" style="position:absolute;left:-9999px;width:1px;height:1px">'
			. '<p class="nladt__priv">הפרטים משמשים רק להכנת החשבונית ולחזרה אליכם, ולא מועברים לאף אחד. <a href="' . esc_url( home_url( '/privacy/' ) ) . '">מדיניות הפרטיות</a></p>'
			. '<div class="nladt__msg" data-msg aria-live="polite"></div>'
			. '<div class="row"><button type="submit" class="nladt__send" value="send">שלחו הזמנה</button><button type="button" class="nladt__x" data-close>ביטול</button></div></form></dialog>';
		$h .= '</section>';
		$h .= '<style id="nladt-css">' . nadlan_adt_css() . '</style>';
		$h .= '<script id="nladt-js">' . nadlan_adt_js() . '</script>';
		return $h;
	}
}

if ( ! function_exists( 'nadlan_adt_css' ) ) {
	function nadlan_adt_css() {
		return <<<'NLADTCSS'
.nladt{--g:#F6F8F9;--s:#FFFFFF;--ink:#12202A;--ink2:#3E4C58;--mute:#5E6A75;--line:#D3DCE2;--sea:#2F6F86;--deep:#1F4B5C;
  --tint:#E9F1F4;--warn:#C42550;--r:6px;--sans:"IBM Plex Sans Hebrew","IBM Plex Sans",system-ui,sans-serif;--mono:"IBM Plex Mono",ui-monospace,monospace;
  direction:rtl;font-family:var(--sans);color:var(--ink2);max-width:1120px;margin:26px auto 34px;padding:0 16px;clear:both}
.nladt *{box-sizing:border-box}
.nladt [hidden]{display:none!important}
.nladt p a,.nladt li a{color:var(--deep);text-decoration:underline;text-underline-offset:2px}
html body .nladt h2,html body .nladt h3,html body .nladt h4{color:var(--ink)!important;font-family:var(--sans)!important;letter-spacing:0}
.nladt__head{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:10px 24px;align-items:end;border-top:2px solid var(--ink);padding-top:16px}
.nladt__kick{font:600 13px/1 var(--sans);color:var(--sea);margin:0 0 8px}
.nladt__head h2{font:700 clamp(23px,3.2vw,32px)/1.25 var(--sans)!important;margin:0 0 8px}
.nladt__lead{font:400 15px/1.7 var(--sans);margin:0;max-width:720px}
.nladt__tracks{display:flex;gap:0;border:1px solid var(--ink);border-radius:var(--r);overflow:hidden;align-self:end}
.nladt__tracks button{appearance:none;border:0;border-inline-start:1px solid var(--ink);background:var(--s);color:var(--ink);font:600 13.5px/1 var(--sans);padding:12px 14px;min-height:44px;cursor:pointer;white-space:nowrap}
.nladt__tracks button:first-child{border-inline-start:0}
.nladt__tracks button[aria-pressed="true"]{background:var(--ink);color:#fff}
.nladt__tracks button:focus-visible,.nladt button:focus-visible,.nladt a:focus-visible,.nladt input:focus-visible+span{outline:2px solid var(--sea);outline-offset:2px}
.nladt__body{display:grid;grid-template-columns:minmax(0,1fr) 340px;gap:22px;margin-top:20px;align-items:start}
.nladt__who{font:500 13.5px/1.6 var(--sans);color:var(--mute);margin:0 0 10px}
.nladt__pack{border:1.5px solid var(--deep);border-radius:var(--r);background:var(--s);padding:16px 16px 14px;margin:0 0 16px}
.nladt__pack h3{font:700 19px/1.35 var(--sans)!important;margin:0 0 10px}
.nladt__pack ul{list-style:none;margin:0 0 14px;padding:0;display:grid;gap:7px}
.nladt__pack li{font:400 14px/1.6 var(--sans);color:var(--ink2);padding-inline-start:16px;position:relative}
.nladt__pack li::before{content:"";position:absolute;inset-inline-start:0;top:.55em;width:7px;height:7px;background:var(--deep)}
.nladt__pack li b{color:var(--ink);font-weight:700}
html body .nladt .nladt__packgo{appearance:none;border:0;border-radius:var(--r);background:var(--deep);color:#fff!important;font:700 15px/1 var(--sans);padding:14px 18px;min-height:48px;cursor:pointer;width:100%}
html body .nladt a.nladt__go,html body .nladt a.nladt__go:visited{color:#fff!important;text-decoration:none!important}
.nladt__priv{font:400 12.5px/1.6 var(--sans);color:var(--mute);margin:4px 0 8px}
.nladt__ladder{list-style:none;margin:0;padding:0;border-top:1px solid var(--line)}
.nladt__lvl{position:relative;border-bottom:1px solid var(--line);background:var(--s)}
.nladt__lvl label{display:grid;grid-template-columns:28px minmax(0,1fr) auto;gap:4px 14px;padding:16px 14px 16px 16px;cursor:pointer;align-items:start}
.nladt__lvl input{position:absolute;opacity:0;pointer-events:none}
.nladt__dot{width:20px;height:20px;border:1.5px solid var(--ink2);border-radius:50%;margin-top:3px;display:grid;place-items:center}
.nladt__dot::after{content:"";width:10px;height:10px;border-radius:50%;background:transparent}
.nladt__lvl input:checked~label .nladt__dot{border-color:var(--sea)}
.nladt__lvl input:checked~label .nladt__dot::after{background:var(--sea)}
.nladt__lvl:has(input:checked){background:var(--tint);box-shadow:inset -3px 0 0 var(--sea)}
.nladt__name{font:700 16.5px/1.3 var(--sans);color:var(--ink);margin:0}
.nladt__sub{display:block;font:400 13.5px/1.6 var(--sans);color:var(--ink2);margin-top:3px}
.nladt__feat{grid-column:2/4;display:flex;flex-wrap:wrap;gap:6px 14px;margin:8px 0 0;padding:0;list-style:none}
.nladt__feat li{font:400 13px/1.5 var(--sans);color:var(--ink2);padding-inline-start:14px;position:relative}
.nladt__feat li::before{content:"";position:absolute;inset-inline-start:0;top:.5em;width:6px;height:6px;background:var(--sea)}
.nladt__price{text-align:left;direction:ltr;white-space:nowrap}
.nladt__price b{display:block;font:600 21px/1.1 var(--mono);color:var(--ink)}
.nladt__price small{display:block;direction:rtl;text-align:left;font:500 12px/1.4 var(--sans);color:var(--mute);margin-top:3px}
.nladt__meter{grid-column:2/4;display:flex;gap:3px;margin-top:10px;align-items:center}
.nladt__meter i{display:block;height:6px;flex:0 0 26px;background:var(--line)}
.nladt__meter i.on{background:var(--deep)}
.nladt__meter span{font:500 12px/1 var(--sans);color:var(--mute);margin-inline-start:8px}
.nladt__cities{grid-column:2/4;margin-top:10px}
.nladt__cities p{font:500 12.5px/1.5 var(--sans);color:var(--mute);margin:0 0 6px}
.nladt__chips{display:flex;flex-wrap:wrap;gap:6px}
.nladt__chip{position:relative}
.nladt__chip input{position:absolute;opacity:0}
.nladt__chip span{display:inline-block;border:1px solid var(--line);background:var(--s);border-radius:3px;padding:7px 10px;font:500 12.5px/1 var(--sans);color:var(--ink2);cursor:pointer;min-height:32px}
.nladt__chip input:checked+span{background:var(--deep);border-color:var(--deep);color:#fff}
.nladt__adds{margin-top:18px}
.nladt__adds h3{font:700 14px/1.3 var(--sans)!important;margin:0 0 8px}
.nladt__add{display:grid;grid-template-columns:28px minmax(0,1fr) auto;gap:4px 14px;align-items:start;border:1px solid var(--line);background:var(--s);border-radius:var(--r);padding:13px 14px;margin-bottom:8px;cursor:pointer;position:relative}
.nladt__add input{position:absolute;opacity:0}
.nladt__box{width:20px;height:20px;border:1.5px solid var(--ink2);border-radius:3px;margin-top:2px;display:grid;place-items:center;color:#fff;font:700 13px/1 var(--sans)}
.nladt__add:has(input:checked){border-color:var(--sea);background:var(--tint)}
.nladt__add:has(input:checked) .nladt__box{background:var(--sea);border-color:var(--sea)}
.nladt__add:has(input:checked) .nladt__box::after{content:"✓"}
.nladt__sum{position:sticky;top:76px;border:1px solid var(--ink);border-radius:var(--r);background:var(--s);padding:18px}
.nladt__sum h3{font:700 15px/1.3 var(--sans)!important;margin:0 0 12px}
.nladt__rows{margin:0;padding:0;list-style:none;border-top:1px solid var(--line)}
.nladt__rows li{display:flex;justify-content:space-between;gap:12px;padding:9px 0;border-bottom:1px solid var(--line);font:400 13.5px/1.45 var(--sans)}
.nladt__rows li b{font:600 13.5px/1.45 var(--mono);color:var(--ink);direction:ltr;white-space:nowrap}
.nladt__total{display:flex;justify-content:space-between;align-items:baseline;margin:12px 0 4px}
.nladt__total span{font:600 13.5px/1 var(--sans);color:var(--ink)}
.nladt__total b{font:600 26px/1 var(--mono);color:var(--ink);direction:ltr}
.nladt__renew{font:400 12.5px/1.55 var(--sans);color:var(--mute);margin:6px 0 14px}
.nladt__go{display:flex;align-items:center;justify-content:center;gap:8px;width:100%;min-height:48px;border:0;border-radius:var(--r);background:var(--sea);color:#fff!important;font:700 15px/1 var(--sans);text-decoration:none!important;cursor:pointer}
.nladt__go:hover{background:var(--deep)}
.nladt__go.is-inv{background:var(--ink)}
.nladt__pay{font:500 12px/1.5 var(--sans);color:var(--mute);margin:10px 0 0;text-align:center}
.nladt__note{font:400 12px/1.55 var(--sans);color:var(--mute);margin:10px 0 0;border-top:1px dashed var(--line);padding-top:10px}
.nladt__steps{list-style:none;padding:0;display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:0;margin:26px 0 0;border:1px solid var(--line);border-radius:var(--r);background:var(--s);counter-reset:s}
.nladt__step{padding:14px 16px;border-inline-start:1px solid var(--line)}
.nladt__step:first-child{border-inline-start:0}
.nladt__step b{display:block;font:600 12px/1 var(--mono);color:var(--sea);margin-bottom:7px}
.nladt__step strong{display:block;font:700 14px/1.35 var(--sans);color:var(--ink);margin-bottom:4px}
.nladt__step p{font:400 13px/1.55 var(--sans);margin:0}
.nladt__fair{display:grid;grid-template-columns:minmax(0,1.15fr) minmax(0,.85fr);gap:22px;margin-top:22px;align-items:start}
.nladt__fair h3{font:700 16px/1.3 var(--sans)!important;margin:0 0 8px}
.nladt__fair ul{margin:0;padding:0;list-style:none}
.nladt__fair li{font:400 13.5px/1.6 var(--sans);padding:7px 0 7px;border-bottom:1px solid var(--line);padding-inline-start:18px;position:relative}
.nladt__fair li::before{content:"";position:absolute;inset-inline-start:2px;top:15px;width:8px;height:8px;border:1.5px solid var(--sea);border-radius:50%}
.nladt__spec{border:1px solid var(--line);background:var(--s);border-radius:var(--r);padding:14px}
.nladt__spec small{display:block;font:600 12px/1.4 var(--sans);color:var(--mute);margin-bottom:8px}
.nladt__guide{font:400 13px/1.7 var(--sans);color:var(--ink2);margin:0 0 10px}
.nladt__ad{border:1px solid var(--ink);border-radius:4px;padding:11px 12px}
.nladt__ad .nladt__adtag{display:inline-block;font:600 11px/1 var(--sans);color:var(--ink);border:1px solid var(--ink);border-radius:2px;padding:3px 6px;margin-bottom:7px}
.nladt__ad strong{display:block;font:700 14px/1.3 var(--sans);color:var(--ink)}
.nladt__ad span{display:block;font:400 12.5px/1.5 var(--sans);color:var(--mute)}
.nladt__fine{font:400 12px/1.6 var(--sans);color:var(--mute);margin:16px 0 0}
.nladt dialog{border:1px solid var(--ink);border-radius:var(--r);padding:20px;max-width:420px;width:calc(100% - 32px);color:var(--ink2);font-family:var(--sans)}
.nladt dialog::backdrop{background:rgba(18,32,42,.45)}
.nladt dialog h3{font:700 17px/1.3 var(--sans)!important;margin:0 0 6px}
.nladt dialog p{font:400 13.5px/1.6 var(--sans);margin:0 0 12px}
.nladt dialog label{display:block;font:600 12.5px/1.4 var(--sans);color:var(--ink);margin:0 0 10px}
.nladt dialog input{display:block;width:100%;margin-top:5px;min-height:44px;border:1px solid var(--line);border-radius:4px;padding:9px 10px;font:400 15px/1.2 var(--sans);color:var(--ink);background:#fff}
.nladt dialog .row{display:flex;gap:8px;margin-top:6px}
.nladt dialog .row button{flex:1;min-height:46px;border-radius:var(--r);font:700 14px/1 var(--sans);cursor:pointer}
.nladt__send{background:var(--ink);color:#fff;border:0}
.nladt__x{background:#fff;color:var(--ink);border:1px solid var(--line)}
.nladt__msg{font:500 13px/1.5 var(--sans);color:var(--deep);min-height:18px}
@media (max-width:900px){.nladt__body{grid-template-columns:1fr}.nladt__sum{position:static}.nladt__head{grid-template-columns:1fr}.nladt__tracks{justify-self:start}}
@media (max-width:760px){.nladt__steps{grid-template-columns:1fr 1fr}.nladt__step:nth-child(3){border-inline-start:0}.nladt__step:nth-child(n+3){border-top:1px solid var(--line)}.nladt__fair{grid-template-columns:1fr}}
@media (max-width:520px){.nladt__tracks{width:100%}.nladt__tracks button{flex:1;padding:12px 6px;font-size:12.5px;white-space:normal;line-height:1.2}
  .nladt__lvl label{grid-template-columns:24px minmax(0,1fr);padding:14px 12px}.nladt__price{grid-column:2;text-align:right;direction:rtl;display:flex;gap:8px;align-items:baseline}
  .nladt__price b{display:inline;direction:ltr}.nladt__price small{display:inline;margin:0}.nladt__feat,.nladt__meter,.nladt__cities{grid-column:1/3}
  .nladt__add{grid-template-columns:24px minmax(0,1fr)}.nladt__add .nladt__price{grid-column:2}.nladt__steps{grid-template-columns:1fr}.nladt__step{border-inline-start:0;border-top:1px solid var(--line)}.nladt__step:first-child{border-top:0}}
/* 1.72.536 (Ben 26.10: "make it look like the site"): the site's own faces and cards, as on the home page */
.nladt{--sans:"Assistant","Segoe UI",Arial,sans-serif;--mono:"Assistant","Segoe UI",Arial,sans-serif;--serif:"Noto Serif Hebrew","David Libre",Georgia,serif;
  --ink:#14212B;--line:#E3E8EC;--r:12px;font-family:var(--sans);margin:44px auto 40px}
.nladt__head{border-top:0;padding-top:0}
html body .nladt .nladt__head h2{font:600 clamp(26px,3.4vw,36px)/1.25 var(--serif)!important}
html body .nladt h3{font-family:var(--serif)!important;font-weight:600!important}
.nladt__kick{font:700 14px/1 var(--sans);color:var(--sea)}
.nladt__lead{font:400 16.5px/1.7 var(--sans);color:var(--ink2)}
.nladt__tracks{border:1px solid var(--line);background:#fff;border-radius:14px;padding:5px;gap:4px;box-shadow:0 10px 30px -22px rgba(20,33,43,.55)}
.nladt__tracks button{border:0!important;border-radius:10px;font:700 14.5px/1 var(--sans);color:var(--ink2)}
.nladt__tracks button[aria-pressed="true"]{background:var(--ink);color:#fff}
.nladt__ladder{border:1px solid var(--line);border-radius:14px;overflow:hidden;background:#fff}
.nladt__lvl:last-child{border-bottom:0}
.nladt__lvl:has(input:checked){background:#EEF4F6;box-shadow:inset -4px 0 0 var(--deep)}
.nladt__name{font:700 17.5px/1.3 var(--sans)}
.nladt__sub{font:400 14.5px/1.6 var(--sans)}
.nladt__feat li{font-size:14px}
.nladt__price b{font:800 23px/1.1 var(--sans);font-variant-numeric:tabular-nums}
.nladt__price small{font-size:12.5px}
.nladt__adds h3{font-size:17px!important}
.nladt__add{border-radius:12px;background:#fff}
.nladt__sum{border:1px solid var(--line);border-radius:16px;box-shadow:0 18px 40px -28px rgba(20,33,43,.55);padding:20px}
.nladt__sum h3{font-size:19px!important}
.nladt__rows li{font-size:14.5px}.nladt__rows li b{font:700 14.5px/1.45 var(--sans);font-variant-numeric:tabular-nums}
.nladt__total b{font:800 30px/1 var(--sans);font-variant-numeric:tabular-nums}
.nladt__go{border-radius:10px;background:var(--deep);font-size:16px}.nladt__go.is-inv{background:var(--deep)}.nladt__go:hover{background:var(--ink)}
.nladt__steps{border-radius:14px;background:#fff}
.nladt__step b{font:800 13px/1 var(--sans);color:var(--sea)}
.nladt__step strong{font-size:15.5px}.nladt__step p{font-size:14px}
.nladt__fair h3{font-size:19px!important}.nladt__fair li{font-size:14.5px}
.nladt__spec,.nladt__pack{border-radius:14px;background:#fff}
.nladt__pack{border:1px solid var(--line);box-shadow:inset -4px 0 0 var(--deep)}
.nladt__pack h3{font-size:21px!important}.nladt__pack li{font-size:15px}
html body .nladt .nladt__packgo{border-radius:10px}
.nladt dialog{border:1px solid var(--line);border-radius:16px}
.nladt dialog input{border-radius:8px}
.nladt__send{background:var(--deep)}
NLADTCSS;
	}
}

if ( ! function_exists( 'nadlan_adt_js' ) ) {
	function nadlan_adt_js() {
		return <<<'NLADTJS'
(function () {
  var root = document.getElementById("nladt");
  if (!root) { return; }
  var nis = function (n) { return "₪" + Number(n).toLocaleString("en-US"); };
  var tracks = root.querySelectorAll("[data-track]");
  var panels = root.querySelectorAll("[data-panel]");
  var rows = root.querySelector("[data-rows]");
  var total = root.querySelector("[data-total]");
  var renew = root.querySelector("[data-renew]");
  var go = root.querySelector("[data-go]");
  var pay = root.querySelector("[data-pay]");
  var dlg = root.querySelector("[data-dlg]");
  var cur = "pro";
  function panel() { return root.querySelector('[data-panel="' + cur + '"]'); }
  function show(t) {
    if (!root.querySelector('[data-panel="' + t + '"]')) { t = "pro"; }
    cur = t;
    tracks.forEach(function (b) { b.setAttribute("aria-pressed", b.dataset.track === t ? "true" : "false"); });
    panels.forEach(function (p) { p.hidden = p.dataset.panel !== t; });
    sum();
  }
  function sum() {
    var p = panel(), lvl = p.querySelector('input[type="radio"]:checked');
    var adds = [].slice.call(p.querySelectorAll('.nladt__adds input:checked'));
    var cities = [].slice.call(p.querySelectorAll('[data-cities] input:checked')).map(function (i) { return i.value; });
    var cBox = p.querySelector("[data-cities]");
    if (cBox) { cBox.hidden = !(lvl && lvl.value === "area"); }
    var html = "", today = 0, invoice = false, monthly = 0, parts = [];
    var items = lvl ? [lvl].concat(adds) : adds;
    items.forEach(function (i) {
      var price = i.dataset.price === "" ? null : Number(i.dataset.price);
      var line = price === null ? i.dataset.period : nis(price) + " " + i.dataset.period;
      if (i.dataset.first) { line += " · " + i.dataset.first; }
      if (i.dataset.min) { line = nis(price) + " × " + i.dataset.min; }
      html += "<li><span>" + i.dataset.label + "</span><b>" + line + "</b></li>";
      if (i.dataset.invoice) { invoice = true; }
      if (price !== null) {
        var due = i.dataset.first ? 0 : price * (Number(i.dataset.min) || 1);
        today += due;
        if (i.dataset.period === "לחודש") { monthly += price; }
      }
      if (i.dataset.invoice) { parts.push(i.value); } else if (i.value !== "475") { parts.push(i.value); }
    });
    if (cities.length) { html += "<li><span>ערים</span><b style=\"font-family:inherit\">" + cities.join(", ") + "</b></li>"; }
    rows.innerHTML = html;
    total.textContent = lvl && lvl.dataset.price === "" ? "הצעה" : nis(today);
    renew.textContent = monthly ? "אחר כך " + nis(monthly) + " לחודש, עם חשבונית חידוש לאישור בכל חודש. עוצרים מתי שרוצים." : (lvl && lvl.value === "475" && !adds.length ? "חינם, בלי כרטיס אשראי." : "תשלום אחד לתקופה. בסופה הפרסום יורד לבד.");
    var live = root.dataset.live === "1";
    var useInvoice = invoice || !live;
    go.classList.toggle("is-inv", useInvoice);
    if (lvl && lvl.value === "475" && !adds.length) {
      go.textContent = "פתיחת כרטיס חינם";
      go.href = root.dataset.cart + "?add-to-cart=475&ref=advertise-tiers";
      go.dataset.inv = "";
      pay.textContent = "בלי תשלום";
      return;
    }
    go.textContent = useInvoice ? "הזמנה בחשבונית" : "להמשך ולתשלום";
    go.dataset.inv = useInvoice ? "1" : "";
    go.dataset.what = items.map(function (i) { return i.dataset.label; }).join(" + ") + (cities.length ? " (" + cities.join(", ") + ")" : "");
    var q = "?nladt_pick=" + encodeURIComponent(parts.join(",")) + "&nladt_track=" + cur + "&ref=advertise-tiers";
    if (cities.length) { q += "&nladt_cities=" + encodeURIComponent(cities.join(",")); }
    var dom = adds.filter(function (i) { return i.dataset.domain; })[0];
    if (dom && dom.dataset.domain !== "1") { q += "&sponsor_domains=" + encodeURIComponent(dom.dataset.domain); }
    go.href = useInvoice ? "#" : root.dataset.cart + q;
    pay.textContent = useInvoice ? "חשבונית מס למייל, תשלום בהעברה או באשראי בטלפון" : "אשראי · Bit · Google Pay · Apple Pay · חשבונית מס למייל";
  }
  var packGo = root.querySelector("[data-pack-go]");
  if (packGo) {
    packGo.addEventListener("click", function () {
      var p = root.querySelector('[data-panel="renewal"]');
      var prem = p.querySelector('input[type="radio"][value="477"]'); if (prem) { prem.checked = true; }
      p.querySelectorAll(".nladt__adds input").forEach(function (i) { i.checked = true; });
      sum();
      var s = root.querySelector(".nladt__sum"); if (s && s.scrollIntoView) { s.scrollIntoView({ behavior: "smooth", block: "start" }); }
    });
  }
  tracks.forEach(function (b) { b.addEventListener("click", function () { show(b.dataset.track); if (history.replaceState) { history.replaceState(null, "", "#" + (b.dataset.track === "pro" ? "nladt" : b.dataset.track)); } }); });
  root.addEventListener("change", function (e) {
    var c = e.target.closest("[data-cities] input");
    if (c && c.checked && panel().querySelectorAll("[data-cities] input:checked").length > 6) { c.checked = false; }
    sum();
  });
  go.addEventListener("click", function (e) {
    if (!go.dataset.inv) { return; }
    e.preventDefault();
    root.querySelector("[data-dlg-what]").textContent = go.dataset.what + ". נשלח חשבונית למייל, והפרסום יעלה עם התשלום.";
    root.querySelector("[data-msg]").textContent = "";
    if (dlg.showModal) { dlg.showModal(); } else { dlg.setAttribute("open", ""); }
  });
  root.querySelector("[data-close]").addEventListener("click", function () { dlg.close ? dlg.close() : dlg.removeAttribute("open"); });
  root.querySelector("[data-form]").addEventListener("submit", function (e) {
    e.preventDefault();
    var f = e.target, msg = root.querySelector("[data-msg]");
    if (!f.name.value || !f.phone.value) { msg.textContent = "נא למלא שם וטלפון."; return; }
    var body = { name: f.name.value, phone: f.phone.value, email: f.email.value, topic: "הזמנת פרסום בחשבונית", message: go.dataset.what, source: "advertise-tiers" };
    if (root.dataset.preview === "1") { msg.textContent = "תצוגה מקומית: ההזמנה לא נשלחה."; return; }
    msg.textContent = "שולחים...";
    fetch(root.dataset.lead, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body) })
      .then(function (r) { if (!r.ok) { throw r; } msg.textContent = "קיבלנו. החשבונית תגיע למייל עוד היום."; })
      .catch(function () { msg.textContent = "לא נשלח. אפשר לכתוב לנו בוואטסאפ."; });
  });
  var h = (location.hash || "").replace("#", "");
  show(h === "renewal" || h === "project" ? h : "pro");
  window.addEventListener("hashchange", function () {
    var k = (location.hash || "").replace("#", "");
    if (k !== "pro" && k !== "renewal" && k !== "project") { return; }
    show(k);
    if (root.scrollIntoView) { root.scrollIntoView({ behavior: "smooth", block: "start" }); }
  });
})();
NLADTJS;
	}
}

/* the section enters /advertise/ right before its "נדבר?" chapter (after "what you get" and "what we need") */
add_filter( 'the_content', function ( $content ) {
	if ( ! is_page( 'advertise' ) || is_admin() || ! in_the_loop() || ! is_main_query() ) { return $content; }
	if ( '1' !== (string) get_option( 'nadlan_adt_enabled', '1' ) ) { return $content; }
	$section = nadlan_adt_render();
	if ( false !== strpos( $content, '<div id="nladt-slot"></div>' ) ) {
		return str_replace( '<div id="nladt-slot"></div>', $section, $content );
	}
	if ( preg_match( '/<h2\b[^>]*>(?:(?!<\/h2>).)*נדבר/us', $content, $m, PREG_OFFSET_CAPTURE ) ) {
		$at = (int) $m[0][1];
		return substr( $content, 0, $at ) . $section . substr( $content, $at );
	}
	return $content . $section;
}, 21 );

/* ---------- the self-serve pick: login, cart with the card attached, checkout ---------- */
if ( ! function_exists( 'nadlan_adt_owned_card' ) ) {
	function nadlan_adt_owned_card( $uid, $post_type ) {
		$ids = get_posts( array( 'post_type' => $post_type, 'post_status' => array( 'publish', 'draft', 'pending' ), 'posts_per_page' => 2, 'fields' => 'ids',
			'meta_query' => array( array( 'key' => 'owner_user_id', 'value' => (int) $uid ) ) ) );
		return 1 === count( $ids ) ? (int) $ids[0] : 0; // one card = obvious; several = the advertiser center asks which one
	}
}

if ( ! function_exists( 'nadlan_adt_draft_organizer_card' ) ) {
	/** A draft "ארגון דיירים" card for a new urban-renewal advertiser; published only when a payment activates it. */
	function nadlan_adt_draft_organizer_card( $uid ) {
		$u  = get_userdata( (int) $uid );
		$id = wp_insert_post( array( 'post_type' => 'nadlan_professional', 'post_status' => 'draft', 'post_author' => (int) $uid,
			'post_title' => $u && $u->display_name ? $u->display_name : 'כרטיס ארגון דיירים' ), true );
		if ( is_wp_error( $id ) ) { return 0; }
		update_post_meta( $id, 'owner_user_id', (int) $uid );
		update_post_meta( $id, 'claim_status', 'verified' );
		update_post_meta( $id, 'data_quality', 'stub' );
		update_post_meta( $id, 'paid_tier', 'free' );
		update_post_meta( $id, 'profession', 'organizer' );
		update_post_meta( $id, 'created_via', 'advertise_tiers' );
		return (int) $id;
	}
}

add_action( 'wp_loaded', function () {
	if ( empty( $_GET['nladt_pick'] ) || is_admin() || ! function_exists( 'WC' ) ) { return; } // phpcs:ignore
	if ( ! nadlan_adt_checkout_live() && ! current_user_can( 'manage_options' ) ) { wp_safe_redirect( home_url( '/advertise/#nladt' ) ); exit; }
	$spon    = (int) get_option( 'nadlan_procard_product', 5403 );
	$allowed = array_filter( array( 475, 476, 477, 489, 490, $spon, nadlan_adt_extra( 'area' ), nadlan_adt_extra( 'story' ) ) );
	$ids     = array_values( array_unique( array_intersect( array_map( 'absint', explode( ',', sanitize_text_field( wp_unslash( $_GET['nladt_pick'] ) ) ) ), $allowed ) ) ); // phpcs:ignore
	if ( ! $ids ) { return; }
	$track   = isset( $_GET['nladt_track'] ) ? sanitize_key( wp_unslash( $_GET['nladt_track'] ) ) : ''; // phpcs:ignore
	$cities  = isset( $_GET['nladt_cities'] ) ? sanitize_text_field( wp_unslash( $_GET['nladt_cities'] ) ) : ''; // phpcs:ignore
	$domains = isset( $_GET['sponsor_domains'] ) ? sanitize_text_field( wp_unslash( $_GET['sponsor_domains'] ) ) : ''; // phpcs:ignore
	if ( ! is_user_logged_in() ) {
		$back = add_query_arg( array_filter( array( 'nladt_pick' => implode( ',', $ids ), 'nladt_track' => $track, 'nladt_cities' => $cities, 'sponsor_domains' => $domains ) ), home_url( '/' ) );
		wp_safe_redirect( wp_login_url( $back ) );
		exit;
	}
	$uid = get_current_user_id();
	$pro = nadlan_adt_owned_card( $uid, 'nadlan_professional' );
	if ( ! $pro && 'renewal' === $track ) { $pro = nadlan_adt_draft_organizer_card( $uid ); }
	if ( null === WC()->cart && function_exists( 'wc_load_cart' ) ) { wc_load_cart(); }
	if ( ! WC()->cart ) { return; }
	foreach ( $ids as $pid ) {
		$type = 489 === $pid ? 'nadlan_project' : ( 490 === $pid ? 'nadlan_property' : 'nadlan_professional' );
		$card = 'nadlan_professional' === $type ? $pro : nadlan_adt_owned_card( $uid, $type );
		$_REQUEST['card_id'] = $card;              // read by advertiser-orders.php (woocommerce_add_cart_item_data)
		$_GET['sponsor_card'] = $card;             // read by pro-cards.php for the content sponsorship
		$_REQUEST['nladt_cities'] = $cities;       // read below for the area package
		WC()->cart->add_to_cart( $pid, 1 );
	}
	wp_safe_redirect( wc_get_checkout_url() );
	exit;
}, 20 );

/* the area package keeps the chosen cities on the order line, for the admin who places the cards */
add_filter( 'woocommerce_add_cart_item_data', function ( $data, $product_id ) {
	$area = nadlan_adt_extra( 'area' );
	if ( $area && (int) $product_id === $area && ! empty( $_REQUEST['nladt_cities'] ) ) { // phpcs:ignore
		$data['nadlan_area_cities'] = mb_substr( sanitize_text_field( wp_unslash( $_REQUEST['nladt_cities'] ) ), 0, 200 ); // phpcs:ignore
	}
	return $data;
}, 11, 2 );
add_action( 'woocommerce_checkout_create_order_line_item', function ( $item, $key, $values ) {
	if ( ! empty( $values['nadlan_area_cities'] ) ) { $item->add_meta_data( 'ערי החבילה', $values['nadlan_area_cities'], true ); }
}, 11, 3 );

/* on activation: a draft card opened by the pick is published; the area package opens a draft placement */
add_action( 'nadlan_advertiser_paid_tier_activated', function ( $card_id, $order, $item, $end ) {
	$card_id = (int) $card_id;
	if ( 'draft' === get_post_status( $card_id ) && 'advertise_tiers' === (string) get_post_meta( $card_id, 'created_via', true ) ) {
		wp_update_post( array( 'ID' => $card_id, 'post_status' => 'publish' ) );
	}
	$area = nadlan_adt_extra( 'area' );
	if ( ! $area || ! $item || (int) $item->get_product_id() !== $area ) { return; }
	$pl = wp_insert_post( array( 'post_type' => 'nadlan_placement', 'post_status' => 'draft',
		'post_title' => 'חבילת אזור: ' . get_the_title( $card_id ) . ' עד ' . wp_date( 'd/m/Y', (int) $end ) ), true );
	if ( is_wp_error( $pl ) ) { return; }
	update_post_meta( $pl, 'pl_pro', $card_id );
	update_post_meta( $pl, 'pl_start', current_time( 'Y-m-d' ) );
	update_post_meta( $pl, 'pl_end', wp_date( 'Y-m-d', (int) $end ) );
	update_post_meta( $pl, 'pl_active', '1' );
	update_post_meta( $pl, 'pl_headline', '' );
	update_post_meta( $pl, 'pl_paths', '' ); // the admin writes the city pages, then publishes
	if ( $order ) { $order->add_order_note( 'Area package: draft placement #' . (int) $pl . ' opened for the admin (cities: ' . (string) $item->get_meta( 'ערי החבילה' ) . ').' ); }
}, 10, 4 );

add_filter( 'nadlan_config_healthcheck', function ( $out ) {
	$out['advertise_tiers'] = array(
		'enabled'       => '1' === (string) get_option( 'nadlan_adt_enabled', '1' ),
		'checkout_live' => nadlan_adt_checkout_live(),
		'area_product'  => nadlan_adt_extra( 'area' ),
		'story_product' => nadlan_adt_extra( 'story' ),
	);
	return $out;
} );
