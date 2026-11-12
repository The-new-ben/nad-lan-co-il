<?php
/**
 * Pro forum (HAD-726): the trades a MEMBER can join as. Owner, 12.11.2026: "every person who does something relevant to a
 * building, also designers; I should not have to list them". The directory's own registry (nadlan_pro_groups() in
 * inc/pro-network.php, 34 professions) is kept as it is and every key there keeps its meaning; this list adds the trades the
 * directory never had. A member picks one trade (or writes his own, kept as free text for review).
 *
 * 'reg' names the public register a licence number can be checked against at join time (data.gov.il): contractors
 * (פנקס הקבלנים), brokers (פנקס המתווכים), appraisers (פנקס שמאי המקרקעין). No register = no "מאומת" mark, the member
 * still joins. Real-estate lawyers: listed, marked 'review' until the owner decides (Bar advertising rules, HAD-726).
 */
if ( ! defined( 'ABSPATH' ) ) { exit; }

if ( ! function_exists( 'nadlan_forum_trade_groups' ) ) {
	/** group => array( label, trades => key => array( label, plural, female, reg ) ) */
	function nadlan_forum_trade_groups() {
		$g = array(
			'plan'    => array( 'label' => 'תכנון, הנדסה וקרקע', 'trades' => array(
				'architect'           => array( 'אדריכל', 'אדריכלים', 'אדריכלית', '' ),
				'landscape_architect' => array( 'אדריכל נוף', 'אדריכלי נוף', 'אדריכלית נוף', '' ),
				'engineer'            => array( 'מהנדס בניין', 'מהנדסי בניין', 'מהנדסת בניין', '' ),
				'structural'          => array( 'מהנדס קונסטרוקציה', 'מהנדסי קונסטרוקציה', 'מהנדסת קונסטרוקציה', '' ),
				'soil_consultant'     => array( 'יועץ קרקע וביסוס', 'יועצי קרקע וביסוס', 'יועצת קרקע וביסוס', '' ),
				'soil_lab'            => array( 'מעבדת קרקע ובדיקות חומרים', 'מעבדות קרקע ובדיקות חומרים', 'מעבדת קרקע ובדיקות חומרים', '' ),
				'surveyor'            => array( 'מודד מוסמך', 'מודדים מוסמכים', 'מודדת מוסמכת', '' ),
				'urban_planner'       => array( 'מתכנן ערים', 'מתכנני ערים', 'מתכננת ערים', '' ),
				'permit_consultant'   => array( 'יועץ רישוי והיתרי בנייה', 'יועצי רישוי והיתרי בנייה', 'יועצת רישוי והיתרי בנייה', '' ),
				'quantity_surveyor'   => array( 'כמאי', 'כמאים', 'כמאית', '' ),
				'project_manager'     => array( 'מנהל פרויקט בנייה', 'מנהלי פרויקטי בנייה', 'מנהלת פרויקט בנייה', '' ),
				'mefakeach'           => array( 'מפקח בנייה', 'מפקחי בנייה', 'מפקחת בנייה', '' ),
				'bedek_bait'          => array( 'בדק בית', 'בודקי בית', 'בודקת בית', '' ),
				'electrical_engineer' => array( 'מהנדס חשמל', 'מהנדסי חשמל', 'מהנדסת חשמל', '' ),
				'plumbing_consultant' => array( 'יועץ אינסטלציה', 'יועצי אינסטלציה', 'יועצת אינסטלציה', '' ),
				'hvac_consultant'     => array( 'יועץ מיזוג אוויר', 'יועצי מיזוג אוויר', 'יועצת מיזוג אוויר', '' ),
				'safety_consultant'   => array( 'יועץ בטיחות', 'יועצי בטיחות', 'יועצת בטיחות', '' ),
				'fire_consultant'     => array( 'יועץ בטיחות אש', 'יועצי בטיחות אש', 'יועצת בטיחות אש', '' ),
				'acoustics'           => array( 'יועץ אקוסטיקה', 'יועצי אקוסטיקה', 'יועצת אקוסטיקה', '' ),
				'green_building'      => array( 'יועץ בנייה ירוקה ואנרגיה', 'יועצי בנייה ירוקה ואנרגיה', 'יועצת בנייה ירוקה ואנרגיה', '' ),
				'accessibility'       => array( 'יועץ נגישות', 'יועצי נגישות', 'יועצת נגישות', '' ),
				'traffic'             => array( 'יועץ תנועה', 'יועצי תנועה', 'יועצת תנועה', '' ),
				'shelter'             => array( 'יועץ מיגון וממ"ד', 'יועצי מיגון וממ"ד', 'יועצת מיגון וממ"ד', '' ),
			) ),
			'build'   => array( 'label' => 'בנייה וביצוע', 'trades' => array(
				'kablan'       => array( 'קבלן', 'קבלנים', 'קבלנית', 'contractors' ),
				'skeleton'     => array( 'קבלן שלד', 'קבלני שלד', 'קבלנית שלד', 'contractors' ),
				'finishing'    => array( 'קבלן גמר', 'קבלני גמר', 'קבלנית גמר', 'contractors' ),
				'renovation'   => array( 'קבלן שיפוצים', 'קבלני שיפוצים', 'קבלנית שיפוצים', 'contractors' ),
				'tama'         => array( 'קבלן תמ"א 38 והתחדשות עירונית', 'קבלני התחדשות עירונית', 'קבלנית התחדשות עירונית', 'contractors' ),
				'earthworks'   => array( 'עבודות עפר וקידוחים', 'עבודות עפר וקידוחים', 'עבודות עפר וקידוחים', 'contractors' ),
				'demolition'   => array( 'הריסה ופינוי', 'הריסה ופינוי', 'הריסה ופינוי', 'contractors' ),
				'concrete'     => array( 'בטון וטפסנות', 'בטון וטפסנות', 'בטון וטפסנות', 'contractors' ),
				'rebar'        => array( 'ברזלן', 'ברזלנים', 'ברזלנית', '' ),
				'plaster'      => array( 'טייח', 'טייחים', 'טייחת', '' ),
				'painter'      => array( 'צבע', 'צבעים', 'צבעית', '' ),
				'drywall'      => array( 'גבס ובנייה קלה', 'גבס ובנייה קלה', 'גבס ובנייה קלה', '' ),
				'stone'        => array( 'אבן ושיש', 'אבן ושיש', 'אבן ושיש', '' ),
				'roofing'      => array( 'גגות ורעפים', 'גגות ורעפים', 'גגות ורעפים', '' ),
				'waterproofing'=> array( 'איטום', 'אוטמים', 'איטום', '' ),
				'scaffolding'  => array( 'פיגומים', 'פיגומים', 'פיגומים', '' ),
				'cranes'       => array( 'עגורנים ומנופים', 'עגורנים ומנופים', 'עגורנים ומנופים', '' ),
				'developer'    => array( 'יזם', 'יזמים', 'יזמית', '' ),
			) ),
			'systems' => array( 'label' => 'מערכות הבניין', 'trades' => array(
				'electrician'  => array( 'חשמלאי', 'חשמלאים', 'חשמלאית', '' ),
				'plumber'      => array( 'אינסטלטור', 'אינסטלטורים', 'אינסטלטורית', '' ),
				'hvac'         => array( 'מיזוג אוויר', 'מיזוג אוויר', 'מיזוג אוויר', '' ),
				'elevators'    => array( 'מעליות', 'מעליות', 'מעליות', '' ),
				'gas'          => array( 'גז', 'טכנאי גז', 'גז', '' ),
				'fire_systems' => array( 'ספרינקלרים וכיבוי אש', 'ספרינקלרים וכיבוי אש', 'ספרינקלרים וכיבוי אש', '' ),
				'solar'        => array( 'מערכות סולאריות', 'מערכות סולאריות', 'מערכות סולאריות', '' ),
				'smart_home'   => array( 'בית חכם', 'בית חכם', 'בית חכם', '' ),
				'low_voltage'  => array( 'תקשורת ומתח נמוך', 'תקשורת ומתח נמוך', 'תקשורת ומתח נמוך', '' ),
				'security'     => array( 'מיגון ואבטחה', 'מיגון ואבטחה', 'מיגון ואבטחה', '' ),
				'drainage'     => array( 'ביוב וניקוז', 'ביוב וניקוז', 'ביוב וניקוז', '' ),
				'pools'        => array( 'בריכות', 'בריכות', 'בריכות', '' ),
			) ),
			'design'  => array( 'label' => 'עיצוב, גמרים וחוץ', 'trades' => array(
				'interior_designer' => array( 'מעצב פנים', 'מעצבי פנים', 'מעצבת פנים', '' ),
				'home_staging'      => array( 'הום סטיילינג', 'הום סטיילינג', 'הום סטיילינג', '' ),
				'renders'           => array( 'הדמיות ותלת ממד', 'הדמיות ותלת ממד', 'הדמיות ותלת ממד', '' ),
				'kitchens'          => array( 'מטבחים ונגרות', 'מטבחים ונגרות', 'מטבחים ונגרות', '' ),
				'carpenter'         => array( 'נגר', 'נגרים', 'נגרית', '' ),
				'metalwork'         => array( 'מסגר', 'מסגרים', 'מסגרית', '' ),
				'flooring'          => array( 'ריצוף וחיפוי', 'ריצוף וחיפוי', 'ריצוף וחיפוי', '' ),
				'windows'           => array( 'אלומיניום וחלונות', 'אלומיניום וחלונות', 'אלומיניום וחלונות', '' ),
				'glass'             => array( 'זכוכית ומקלחונים', 'זכוכית ומקלחונים', 'זכוכית ומקלחונים', '' ),
				'doors'             => array( 'דלתות', 'דלתות', 'דלתות', '' ),
				'lighting'          => array( 'תאורה', 'תאורה', 'תאורה', '' ),
				'furniture'         => array( 'רהיטים', 'רהיטים', 'רהיטים', '' ),
				'gardens'           => array( 'גינון ופיתוח חצר', 'גינון ופיתוח חצר', 'גינון ופיתוח חצר', '' ),
				'pergolas'          => array( 'פרגולות ודקים', 'פרגולות ודקים', 'פרגולות ודקים', '' ),
				'photographer'      => array( 'צלם אדריכלות ונדל"ן', 'צלמי אדריכלות ונדל"ן', 'צלמת אדריכלות ונדל"ן', '' ),
			) ),
			'deal'    => array( 'label' => 'קנייה, מכירה, מימון ומשפט', 'trades' => array(
				'metavech'       => array( 'מתווך', 'מתווכים', 'מתווכת', 'brokers' ),
				'shamai'         => array( 'שמאי מקרקעין', 'שמאי מקרקעין', 'שמאית מקרקעין', 'appraisers' ),
				'mashkanta'      => array( 'יועץ משכנתאות', 'יועצי משכנתאות', 'יועצת משכנתאות', '' ),
				'project_finance'=> array( 'ליווי פיננסי לפרויקטים', 'ליווי פיננסי לפרויקטים', 'ליווי פיננסי לפרויקטים', '' ),
				'marketing'      => array( 'שיווק פרויקטים', 'משווקי פרויקטים', 'משווקת פרויקטים', '' ),
				'accountant'     => array( 'רואה חשבון, מיסוי מקרקעין', 'רואי חשבון', 'רואת חשבון, מיסוי מקרקעין', '' ),
				'insurance'      => array( 'סוכן ביטוח דירה', 'סוכני ביטוח דירה', 'סוכנת ביטוח דירה', '' ),
				'actuary'        => array( 'אקטואר', 'אקטוארים', 'אקטוארית', '' ),
				'lawyer'         => array( 'עורך דין מקרקעין', 'עורכי דין מקרקעין', 'עורכת דין מקרקעין', 'review' ),
			) ),
			'living'  => array( 'label' => 'מגורים, ניהול ושירותים', 'trades' => array(
				'property_manager' => array( 'ניהול נכסים ובתים משותפים', 'ניהול נכסים', 'ניהול נכסים ובתים משותפים', '' ),
				'organizer'        => array( 'ארגון דיירים', 'ארגון דיירים', 'ארגון דיירים', '' ),
				'movers'           => array( 'הובלות', 'הובלות', 'הובלות', '' ),
				'cleaning'         => array( 'ניקיון אחרי בנייה', 'ניקיון', 'ניקיון אחרי בנייה', '' ),
				'handyman'         => array( 'הנדימן', 'הנדימנים', 'הנדימנית', '' ),
				'locksmith'        => array( 'מנעולן', 'מנעולנים', 'מנעולנית', '' ),
				'pest'             => array( 'הדברה', 'הדברה', 'הדברה', '' ),
			) ),
		);
		return function_exists( 'apply_filters' ) ? apply_filters( 'nadlan_forum_trade_groups', $g ) : $g;
	}
}

if ( ! function_exists( 'nadlan_forum_trades' ) ) {
	/** Flat key => array( label, plural, female, reg, group ). */
	function nadlan_forum_trades() {
		static $flat = null;
		if ( null !== $flat ) { return $flat; }
		$flat = array();
		foreach ( nadlan_forum_trade_groups() as $gk => $grp ) {
			foreach ( $grp['trades'] as $k => $t ) {
				$flat[ $k ] = array( 'label' => $t[0], 'plural' => $t[1], 'female' => $t[2], 'reg' => $t[3], 'group' => $gk );
			}
		}
		return $flat;
	}
}

if ( ! function_exists( 'nadlan_forum_trade_search' ) ) {
	/** Trades whose label contains every word of $q (Hebrew, case-free), best first. Pure: used by the join picker and tests. */
	function nadlan_forum_trade_search( $q, $limit = 8 ) {
		$q = trim( preg_replace( '/\s+/u', ' ', (string) $q ) );
		$out = array();
		if ( '' === $q ) { return $out; }
		$words = explode( ' ', $q );
		foreach ( nadlan_forum_trades() as $k => $t ) {
			$hay = $t['label'] . ' ' . $t['plural'] . ' ' . $t['female'];
			$ok = true;
			// strpos is byte-exact and safe for a UTF-8 substring test; no mbstring needed
			foreach ( $words as $w ) { if ( false === strpos( $hay, $w ) ) { $ok = false; break; } }
			if ( $ok ) { $out[ $k ] = ( 0 === strpos( $t['label'], $words[0] ) ) ? 0 : 1; }
		}
		asort( $out );
		return array_slice( array_keys( $out ), 0, max( 1, (int) $limit ) );
	}
}
