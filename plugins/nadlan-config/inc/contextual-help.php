<?php
/**
 * nadlan-config - Chunk F contextual help framework (v1.56.0).
 *
 * Ships dark behind nadlan_feature_help. OFF means no scripts, no styles,
 * no pointers, no tooltip markup, and existing admin screens keep their
 * current behavior.
 */

if ( ! defined( 'ABSPATH' ) ) { exit; }

if ( ! function_exists( 'nadlan_help_enabled' ) ) {
	function nadlan_help_enabled() {
		return (bool) apply_filters( 'nadlan_help_enabled', get_option( 'nadlan_feature_help', '0' ) === '1' );
	}
}

if ( ! function_exists( 'nadlan_help_strings' ) ) {
	function nadlan_help_strings() {
		$admin = admin_url();
		$strings = array(
			'_common' => array(
				'learn_more_label' => array(
					'tooltip'       => 'מידע נוסף',
					'learn_more_url'=> '',
					'pointer_text'  => '',
					'help_tab_html' => '',
				),
			),
			'settings_page_nadlan-lead-e2e' => array(
				'_screen' => array(
					'tab_title'     => 'עזרה ללידים',
					'tooltip'       => 'מסלול הלידים המלא שולח אישור ללקוח ומנתב את הפנייה לבעל הכרטיס המתאים.',
					'learn_more_url'=> $admin . 'options-general.php?page=nadlan-lead-e2e',
					'pointer_text'  => 'כאן מפעילים את מסלול הלידים המלא ומוודאים שהלקוח מקבל אישור ברור לפני שנוצר טיפול מכירתי.',
					'help_tab_html' => '<p>המסך הזה שולט במסלול הליד מקצה לקצה. השאירו את הדגל כבוי עד שהבדיקה מלאה, ואז הפעילו בהדרגה.</p>',
				),
				'nadlan_feature_lead_e2e' => array(
					'selector'      => 'input[name="nadlan_feature_lead_e2e"]',
					'tooltip'       => 'הדגל מפעיל אישור ללקוח, ניתוב לבעל הכרטיס, תיבת פניות ומדדי תגובה. כשהוא כבוי, המסלול הישן נשאר כפי שהיה.',
					'learn_more_url'=> $admin . 'options-general.php?page=nadlan-lead-e2e',
					'pointer_text'  => 'הפעילו רק אחרי בדיקת G1-G8. הדגל נועד להפעלה בטוחה, לא לשינוי פתאומי.',
					'help_tab_html' => '<p>בדקו דגל כבוי, דגל פעיל, כפילויות, הרשאות וניתוב לפני שמאפשרים שימוש רציף.</p>',
				),
				'nadlan_lead_ack_message' => array(
					'selector'      => 'textarea[name="nadlan_lead_ack_message"]',
					'tooltip'       => 'ההודעה צריכה להזכיר את הכרטיס, לתת מסגרת זמן קונקרטית, ולשאול שאלה אחת שמקדמת את הטיפול.',
					'learn_more_url'=> $admin . 'options-general.php?page=nadlan-lead-e2e',
					'pointer_text'  => 'שמרו על הודעה קצרה וברורה. הלקוח צריך להבין שקיבלנו את הפנייה ומה יקרה עכשיו.',
					'help_tab_html' => '<p>השתמשו בטוקנים {{name}}, {{card}}, {{site}}, {{url}} כדי לשמור על הודעה אישית בלי לכתוב מידע ידני.</p>',
				),
			),
			'settings_page_nadlan-lead-ai' => array(
				'_screen' => array(
					'tab_title'     => 'עזרה ל-AI לידים',
					'tooltip'       => 'ה-AI מסווג לידים רק כשהדגל פעיל ומפתח OpenAI מוגדר.',
					'learn_more_url'=> $admin . 'options-general.php?page=nadlan-lead-ai',
					'pointer_text'  => 'התחילו מהדגל ומהתקרה לכל ליד. המערכת לא סוגרת עסקה לבד, רק מסווגת ומעבירה לאדם כשצריך.',
					'help_tab_html' => '<p>ה-AI חייב לענות רק מתוך מקורות האתר או להימנע. ליד עם ביטחון נמוך עובר לטיפול אנושי.</p>',
				),
				'nadlan_feature_lead_ai_qualify' => array(
					'selector'      => 'input[name="nadlan_feature_lead_ai_qualify"]',
					'tooltip'       => 'כשהדגל כבוי או שאין מפתח OpenAI, לא מתבצעת קריאת AI.',
					'learn_more_url'=> $admin . 'options-general.php?page=nadlan-lead-ai',
					'pointer_text'  => 'זהו מתג כהה. הפעלה מלאה מגיעה רק אחרי בדיקת עלות, ניתוב ואי-המצאת עובדות.',
					'help_tab_html' => '<p>בדקו תמיד שאין קריאת AI כשהדגל כבוי או כשהמפתח חסר.</p>',
				),
				'nadlan_lead_ai_token_cap_per_lead' => array(
					'selector'      => 'input[name="nadlan_lead_ai_token_cap_per_lead"]',
					'tooltip'       => 'תקרה לכל ליד מגנה מהוצאה חריגה לפני הקריאה לספק.',
					'learn_more_url'=> $admin . 'options-general.php?page=nadlan-lead-ai',
					'pointer_text'  => 'תקרה נמוכה מדי תפגע באיכות. תקרה גבוהה מדי מסכנת תקציב. התחילו שמרני.',
					'help_tab_html' => '<p>התקרה לכל ליד מצטרפת לתקרות היומיות הקיימות.</p>',
				),
			),
			'settings_page_nadlan-lead-nurture' => array(
				'_screen' => array(
					'tab_title'     => 'עזרה לטיפוח לידים',
					'tooltip'       => 'רצף ההמשך שולח מיילים רק ללידים שלא נעצרו ולא ביקשו הסרה.',
					'learn_more_url'=> $admin . 'options-general.php?page=nadlan-lead-nurture',
					'pointer_text'  => 'הדבר החשוב כאן הוא עצירה בזמן. ליד שטופל, נסגר או ביקש אדם לא ממשיך לקבל רצף.',
					'help_tab_html' => '<p>בדקו שהרצף עוצר על תגובת לקוח, שינוי סטטוס, הסרה או העברה לאדם.</p>',
				),
				'nadlan_feature_lead_nurture' => array(
					'selector'      => 'input[name="nadlan_feature_lead_nurture"]',
					'tooltip'       => 'הדגל מפעיל תזמון הודעות המשך. כשהוא כבוי, לא מתוזמנות הודעות חדשות.',
					'learn_more_url'=> $admin . 'options-general.php?page=nadlan-lead-nurture',
					'pointer_text'  => 'הפעילו רק אחרי שהסרה, עצירה וכפילויות נבדקו.',
					'help_tab_html' => '<p>רצף טוב מגדיל תגובה בלי לרדוף אחרי לקוחות שכבר בטיפול.</p>',
				),
				'nadlan_lead_nurture_monthly_max' => array(
					'selector'      => 'input[name="nadlan_lead_nurture_monthly_max"]',
					'tooltip'       => 'מגבלה חודשית מונעת עומס על לקוח שנשאר ברצף לטווח ארוך.',
					'learn_more_url'=> $admin . 'options-general.php?page=nadlan-lead-nurture',
					'pointer_text'  => 'רצף איכותי מרגיש כמו שירות, לא כמו הצפה.',
					'help_tab_html' => '<p>שמרו על תדירות נמוכה לאחר יום 14, במיוחד ללידים קרים.</p>',
				),
			),
			'settings_page_nadlan-ai' => array(
				'_screen' => array(
					'tab_title'     => 'עזרה ל-AI',
					'tooltip'       => 'מסך זה שולט בספק, תקרות שימוש ומפתחות שמורים.',
					'learn_more_url'=> $admin . 'options-general.php?page=nadlan-ai',
					'pointer_text'  => 'התחילו מהתקרה היומית הכללית. היא מגינה על העסק גם אם תנועה חריגה נכנסת לאתר.',
					'help_tab_html' => '<p>אל תדביקו מפתח חדש אלא אם מחליפים מפתח קיים. תקרות נבדקות לפני קריאה לספק.</p>',
				),
				'daily_token_cap_global' => array(
					'selector'      => 'input[name="daily_token_cap_global"]',
					'tooltip'       => 'התקרה הכללית היא בלם תקציבי לכל שימושי ה-AI יחד.',
					'learn_more_url'=> $admin . 'options-general.php?page=nadlan-ai',
					'pointer_text'  => 'אם מגיעים לתקרה, עדיף לעצור תשובות AI מאשר להפתיע את התקציב.',
					'help_tab_html' => '<p>השתמשו בתקרה כללית בנוסף לתקרה לפי IP או לפי ליד.</p>',
				),
				'enabled' => array(
					'selector'      => 'input[name="enabled"]',
					'tooltip'       => 'מציג או מסתיר את ווידגט ה-AI באתר. זה לא מחליף את תקרות השימוש.',
					'learn_more_url'=> $admin . 'options-general.php?page=nadlan-ai',
					'pointer_text'  => 'הצגה באתר צריכה לבוא רק אחרי שתוכן המקורות מוכן.',
					'help_tab_html' => '<p>אם אין מקורות טובים, הבוט צריך להימנע ולהציע חיבור לאדם.</p>',
				),
			),
			'settings_page_nadlan-gi-recurring' => array(
				'_screen' => array(
					'tab_title'     => 'עזרה לחיובים',
					'tooltip'       => 'מסך זה שולט ב-IPN, קישור חיוב ובדיקת התאמות מול Morning.',
					'learn_more_url'=> $admin . 'options-general.php?page=nadlan-gi-recurring',
					'pointer_text'  => 'בדקו חתימה לפני כל פעולה עסקית. IPN לא מאומת יכול להפוך לזיכוי חינם.',
					'help_tab_html' => '<p>סודות נשמרים כאפשרויות ואינם מוצגים חזרה למסך. החלפה מתבצעת רק כשמכניסים ערך חדש.</p>',
				),
				'nadlan_gi_ipn_secret_new' => array(
					'selector'      => 'input[name="nadlan_gi_ipn_secret_new"]',
					'tooltip'       => 'הסוד משמש לאימות הודעות IPN. לא מציגים אותו אחרי שמירה.',
					'learn_more_url'=> $admin . 'options-general.php?page=nadlan-gi-recurring',
					'pointer_text'  => 'הדביקו סוד חדש רק כשמחליפים. השדה ריק בכוונה כדי לא לחשוף סוד.',
					'help_tab_html' => '<p>IPN נכשל צריך להיעצר לפני לוגיקה עסקית.</p>',
				),
				'nadlan_gi_reconcile_url' => array(
					'selector'      => 'input[name="nadlan_gi_reconcile_url"]',
					'tooltip'       => 'כתובת התאמות מאפשרת להשלים חיובים שה-webhook לא מסר.',
					'learn_more_url'=> $admin . 'options-general.php?page=nadlan-gi-recurring',
					'pointer_text'  => 'התאמות יומיות הן רשת ביטחון, לא תחליף לחתימת IPN.',
					'help_tab_html' => '<p>שמרו כתובת מאובטחת ומתועדת כדי להקטין דליפות הכנסה.</p>',
				),
			),
			'settings_page_nadlan-placement-auction' => array(
				'_screen' => array(
					'tab_title'     => 'עזרה למכרז חשיפה',
					'tooltip'       => 'מכרז החשיפה מגביל מקומות מובילים ויוצר תחרות מבוקרת בין מפרסמים.',
					'learn_more_url'=> $admin . 'options-general.php?page=nadlan-placement-auction',
					'pointer_text'  => 'מספר המקומות והרצפה קובעים את רמת המחסור. התחילו קטן ומדדו מילוי.',
					'help_tab_html' => '<p>מכרז טוב לא מוחק איכות אורגנית. שמרו מקום אחד לרוטציה איכותית כשהאפשרות פעילה.</p>',
				),
				'nadlan_auction_slots_default' => array(
					'selector'      => 'input[name="nadlan_auction_slots_default"]',
					'tooltip'       => 'מספר המקומות המובילים בכל אזור וקטגוריה. פחות מקומות מגדילים מחסור.',
					'learn_more_url'=> $admin . 'options-general.php?page=nadlan-placement-auction',
					'pointer_text'  => 'ברירת מחדל של שלושה מקומות שומרת על תחרות בלי לקבור את השוק.',
					'help_tab_html' => '<p>בדקו מילוי, הצעות זוכות ושיעור נטישה לפני הגדלת מספר המקומות.</p>',
				),
				'nadlan_auction_slot_overrides' => array(
					'selector'      => 'textarea[name="nadlan_auction_slot_overrides"]',
					'tooltip'       => 'החרגות מאפשרות מספר מקומות שונה לאזור או קטגוריה מסוימים.',
					'learn_more_url'=> $admin . 'options-general.php?page=nadlan-placement-auction',
					'pointer_text'  => 'השתמשו בהחרגות רק כשיש סיבה עסקית ברורה.',
					'help_tab_html' => '<p>פורמט שורה: area|category|slots.</p>',
				),
			),
			'nadlan-ops_page_nadlan-admin-control' => array(
				'_screen' => array(
					'tab_title'     => 'עזרה לבקרת לקוחות',
					'tooltip'       => 'בקרת לקוחות מיועדת לתיקון כרטיסים, מיקום וחשיפה בלי לשנות את ציון האיכות האורגני.',
					'learn_more_url'=> $admin . 'admin.php?page=nadlan-admin-control',
					'pointer_text'  => 'התחילו בשדות המיקום והמשקל. פעולות קידום זמניות חייבות לקבל תוקף.',
					'help_tab_html' => '<p>כל שינוי נרשם ביומן. צפייה כלקוח לא עוקפת הרשאות, והיא קריאה בלבד כברירת מחדל.</p>',
				),
				'priority_weight' => array(
					'selector'      => 'input[name="nadlan_admin_control[priority_weight]"]',
					'tooltip'       => 'משקל 0-100 משפיע על חשיפה רק כשדגל בקרת הלקוחות פעיל. הוא לא משנה את הציון האורגני.',
					'learn_more_url'=> $admin . 'admin.php?page=nadlan-admin-control',
					'pointer_text'  => 'משקל גבוה הוא החלטה מערכתית. תעדו למה הוא ניתן והגדירו תוקף לקידום זמני.',
					'help_tab_html' => '<p>המשקל מתחבר למיקום בתוצאות בזמן שאילתה, לצד paid placement ומכרז חשיפה.</p>',
				),
				'references' => array(
					'selector'      => 'textarea[name="nadlan_admin_control[references]"]',
					'tooltip'       => 'קישורי אסמכתה נשמרים כמערך label/url ועוברים esc_url_raw.',
					'learn_more_url'=> $admin . 'admin.php?page=nadlan-admin-control',
					'pointer_text'  => 'העדיפו מקורות רשמיים או עמודי יזם. אל תכניסו מידע פרטי.',
					'help_tab_html' => '<p>אפשר להכניס JSON או שורות label|url. המערכת שומרת עד 20 קישורים.</p>',
				),
				'impersonation' => array(
					'selector'      => 'input[name="target_user_id"]',
					'tooltip'       => 'צפייה כמפרסם מוגבלת ל-30 דקות וקריאה בלבד כברירת מחדל.',
					'learn_more_url'=> $admin . 'admin.php?page=nadlan-admin-control',
					'pointer_text'  => 'הפעלת כתיבה זמנית היא פעולה מפורשת ונרשמת ביומן.',
					'help_tab_html' => '<p>התחזות לא עוקפת בעלות. היא רק מאפשרת לראות מה הלקוח רואה.</p>',
				),
				'audit_empty' => array(
					'tooltip'       => 'אין עדיין שינויים ביומן.',
					'learn_more_url'=> $admin . 'admin.php?page=nadlan-admin-control',
					'pointer_text'  => 'שינוי ראשון בכרטיס ייצור כאן שורת ביקורת.',
					'help_tab_html' => '<p>היומן מציג מי שינה, איזה שדה השתנה, ומה היה לפני ואחרי.</p>',
					'empty_status'  => 'אין עדיין שינויים ביומן',
					'empty_cue'     => 'אחרי שמירה של שדה או פעולה מרוכזת, תופיע כאן שורת ביקורת עם ערך ישן וחדש.',
					'empty_action_label' => 'פתחו כרטיס לבדיקה',
				),
				'cards_empty' => array(
					'tooltip'       => 'אין כרטיסים שמתאימים לסינון.',
					'learn_more_url'=> $admin . 'admin.php?page=nadlan-admin-control',
					'pointer_text'  => 'שנו סינון או בדקו שהמשתמש מחזיק בכרטיסים.',
					'help_tab_html' => '<p>מפעיל שאינו מנהל רואה רק כרטיסים שיש לו הרשאת עריכה עליהם.</p>',
					'empty_status'  => 'אין כרטיסים להצגה',
					'empty_cue'     => 'נסו להסיר סינון, לבחור סוג אחר, או לוודא שהמפעיל מחזיק בהרשאת עריכה לכרטיס.',
					'empty_action_label' => 'נקה סינון',
				),
			),
			'toplevel_page_nadlan-inbox' => array(
				'_screen' => array(
					'tab_title'     => 'עזרה לתיבת פניות',
					'tooltip'       => 'תיבת הפניות מרכזת לידים, הפניות, ביקורות ותשלומים אחרונים.',
					'learn_more_url'=> $admin . 'admin.php?page=nadlan-inbox',
					'pointer_text'  => 'המסך הזה הוא נקודת הבקרה היומית. התחילו מהפעולות הממתינות.',
					'help_tab_html' => '<p>אם אין פניות, בדקו שהטפסים והניתוב פעילים ושאירועי ליד נרשמים.</p>',
				),
				'recent_leads_empty' => array(
					'tooltip'       => 'אין לידים להצגה כרגע.',
					'learn_more_url'=> $admin . 'admin.php?page=nadlan-inbox',
					'pointer_text'  => 'אחרי שהאתר יקבל פנייה, היא תופיע כאן עם מקור ופרטי קשר.',
					'help_tab_html' => '<p>השתמשו ב-QA של Chunk B כדי ליצור ליד בדיקה ולוודא שהוא נכנס לתיבה.</p>',
					'empty_status'  => 'אין לידים עדיין',
					'empty_cue'     => 'ליד ראשון יופיע כאן אחרי שליחת טופס באתר או דרך נקודת REST מאושרת.',
					'empty_action_label' => 'פתחו את הגדרות הלידים',
					'empty_action_url' => $admin . 'options-general.php?page=nadlan-lead-e2e',
				),
			),
			'toplevel_page_nadlan-ops' => array(
				'_screen' => array(
					'tab_title'     => 'עזרה ל-Ops',
					'tooltip'       => 'לוח Ops נותן מבט מהיר על לידים, חיובים, מכרזים ובריאות המערכת.',
					'learn_more_url'=> $admin . 'admin.php?page=nadlan-ops',
					'pointer_text'  => 'השתמשו בלוח הזה כדי לראות את העסק בלי לפתוח עשרה מסכים.',
					'help_tab_html' => '<p>מדדים חריגים כאן הם סימן לפתוח את מסך המקור: לידים, חיובים, AI או מכרז חשיפה.</p>',
				),
			),
			'settings_page_nadlan-cta' => array(
				'_screen' => array(
					'tab_title'     => 'עזרה ל-CTA',
					'tooltip'       => 'כאן מגדירים וואטסאפ וקריאות לפעולה באתר.',
					'learn_more_url'=> $admin . 'options-general.php?page=nadlan-cta',
					'pointer_text'  => 'בדקו שמספר הוואטסאפ נכון לפני הפעלה רחבה.',
					'help_tab_html' => '<p>קריאת פעולה טובה קצרה, ברורה, ומובילה למסלול ליד מדיד.</p>',
				),
			),
		);
		return apply_filters( 'nadlan_help_strings', $strings );
	}
}

if ( ! function_exists( 'nadlan_help_screen_entries' ) ) {
	function nadlan_help_screen_entries( $screen_id = '' ) {
		$screen_id = sanitize_key( (string) $screen_id );
		$all = nadlan_help_strings();
		return isset( $all[ $screen_id ] ) && is_array( $all[ $screen_id ] ) ? $all[ $screen_id ] : array();
	}
}

if ( ! function_exists( 'nadlan_help_common_text' ) ) {
	function nadlan_help_common_text( $field, $key = 'tooltip', $fallback = '' ) {
		$strings = nadlan_help_strings();
		if ( isset( $strings['_common'][ $field ][ $key ] ) ) {
			return (string) $strings['_common'][ $field ][ $key ];
		}
		return (string) $fallback;
	}
}

if ( ! function_exists( 'nadlan_help_strings_count' ) ) {
	function nadlan_help_strings_count() {
		$count = 0;
		foreach ( nadlan_help_strings() as $entries ) {
			$count += is_array( $entries ) ? count( $entries ) : 0;
		}
		return $count;
	}
}

if ( ! function_exists( 'nadlan_help_current_screen_id' ) ) {
	function nadlan_help_current_screen_id() {
		if ( ! function_exists( 'get_current_screen' ) ) { return ''; }
		$screen = get_current_screen();
		return $screen && ! empty( $screen->id ) ? sanitize_key( $screen->id ) : '';
	}
}

if ( ! function_exists( 'nadlan_help_empty_state' ) ) {
	function nadlan_help_empty_state( $screen_id, $field, $args = array() ) {
		if ( ! nadlan_help_enabled() ) { return ''; }
		$entry = nadlan_help_screen_entries( $screen_id );
		$item = isset( $entry[ $field ] ) && is_array( $entry[ $field ] ) ? $entry[ $field ] : array();
		if ( ! $item ) { return ''; }
		$status = isset( $args['status'] ) ? $args['status'] : ( $item['empty_status'] ?? $item['tooltip'] ?? '' );
		$cue = isset( $args['cue'] ) ? $args['cue'] : ( $item['empty_cue'] ?? $item['pointer_text'] ?? '' );
		$label = isset( $args['action_label'] ) ? $args['action_label'] : ( $item['empty_action_label'] ?? '' );
		$url = isset( $args['action_url'] ) ? $args['action_url'] : ( $item['empty_action_url'] ?? $item['learn_more_url'] ?? '' );
		if ( $status === '' && $cue === '' ) { return ''; }
		$html  = '<div class="nadlan-help-empty-state" dir="rtl">';
		$html .= '<strong>' . esc_html( $status ) . '</strong>';
		if ( $cue !== '' ) {
			$html .= '<p>' . esc_html( $cue ) . '</p>';
		}
		if ( $label !== '' && $url !== '' ) {
			$html .= '<a class="button button-secondary" href="' . esc_url( $url ) . '">' . esc_html( $label ) . '</a>';
		}
		$html .= '</div>';
		return $html;
	}
}

if ( ! function_exists( 'nadlan_help_tooltip' ) ) {
	function nadlan_help_tooltip( $screen_id, $field ) {
		if ( ! nadlan_help_enabled() ) { return ''; }
		$entries = nadlan_help_screen_entries( $screen_id );
		if ( empty( $entries[ $field ]['tooltip'] ) ) { return ''; }
		$id = 'nadlan-help-' . sanitize_key( $screen_id . '-' . $field );
		$html  = '<button type="button" class="nadlan-help-tip" aria-describedby="' . esc_attr( $id ) . '" aria-expanded="false">?</button>';
		$html .= '<span id="' . esc_attr( $id ) . '" class="nadlan-help-tooltip" role="tooltip" hidden>' . esc_html( $entries[ $field ]['tooltip'] );
		if ( ! empty( $entries[ $field ]['learn_more_url'] ) ) {
			$learn_more = nadlan_help_common_text( 'learn_more_label', 'tooltip', '' );
			if ( $learn_more !== '' ) {
				$html .= ' <a href="' . esc_url( $entries[ $field ]['learn_more_url'] ) . '">' . esc_html( $learn_more ) . '</a>';
			}
		}
		$html .= '</span>';
		return $html;
	}
}

add_action( 'current_screen', function ( $screen ) {
	if ( ! nadlan_help_enabled() || ! $screen || empty( $screen->id ) ) { return; }
	$entries = nadlan_help_screen_entries( $screen->id );
	if ( ! $entries ) { return; }
	$screen_entry = isset( $entries['_screen'] ) && is_array( $entries['_screen'] ) ? $entries['_screen'] : array();
	$content = '';
	foreach ( $entries as $field => $entry ) {
		if ( $field === '_screen' || empty( $entry['help_tab_html'] ) ) { continue; }
		$content .= wp_kses_post( $entry['help_tab_html'] );
	}
	if ( $content === '' && ! empty( $screen_entry['help_tab_html'] ) ) {
		$content = wp_kses_post( $screen_entry['help_tab_html'] );
	}
	if ( $content === '' ) { return; }
	$screen->add_help_tab( array(
		'id'      => 'nadlan-contextual-help',
		'title'   => sanitize_text_field( (string) ( $screen_entry['tab_title'] ?? 'NadLan' ) ),
		'content' => '<div dir="rtl" class="nadlan-help-tab">' . $content . '</div>',
	) );
} );

if ( ! function_exists( 'nadlan_help_items_for_js' ) ) {
	function nadlan_help_items_for_js( $screen_id ) {
		$out = array();
		foreach ( nadlan_help_screen_entries( $screen_id ) as $field => $entry ) {
			if ( $field === '_screen' || empty( $entry['selector'] ) || empty( $entry['tooltip'] ) ) { continue; }
			$out[] = array(
				'field'          => sanitize_key( (string) $field ),
				'selector'       => (string) $entry['selector'],
				'tooltip'        => sanitize_text_field( (string) $entry['tooltip'] ),
				'learn_more_url' => ! empty( $entry['learn_more_url'] ) ? esc_url_raw( (string) $entry['learn_more_url'] ) : '',
				'pointer_text'   => ! empty( $entry['pointer_text'] ) ? sanitize_text_field( (string) $entry['pointer_text'] ) : '',
			);
		}
		return $out;
	}
}

add_action( 'admin_enqueue_scripts', function () {
	if ( ! nadlan_help_enabled() ) { return; }
	$screen_id = nadlan_help_current_screen_id();
	$entries = nadlan_help_screen_entries( $screen_id );
	if ( ! $entries ) { return; }
	$items = nadlan_help_items_for_js( $screen_id );

	wp_register_style( 'nadlan-contextual-help', '', array(), '1.56.0' );
	wp_enqueue_style( 'nadlan-contextual-help' );
	if ( ! $items ) {
		wp_add_inline_style( 'nadlan-contextual-help', <<<'CSS'
.nadlan-help-empty-state{padding:18px;border:1px solid #d6c49f;border-radius:8px;background:#fffdf7;color:#1d2327;text-align:center;font-size:14px;line-height:1.55}
.nadlan-help-empty-state strong{display:block;font-size:16px;margin-bottom:6px}
.nadlan-help-empty-state p{margin:0 0 12px}
.nadlan-help-tab{font-size:14px;line-height:1.65}
CSS
		);
		return;
	}

	wp_enqueue_script( 'jquery' );
	wp_enqueue_script( 'wp-pointer' );
	wp_enqueue_style( 'wp-pointer' );
	wp_register_script( 'nadlan-contextual-help', '', array( 'jquery', 'wp-pointer' ), '1.56.0', true );
	wp_enqueue_script( 'nadlan-contextual-help' );

	$pointer_id = 'nadlan_' . sanitize_key( str_replace( '-', '_', $screen_id ) );
	$dismissed = array_filter( array_map( 'trim', explode( ',', (string) get_user_meta( get_current_user_id(), 'dismissed_wp_pointers', true ) ) ) );
	$data = array(
		'screen'      => $screen_id,
		'items'       => $items,
		'pointerId'   => $pointer_id,
		'dismissed'   => in_array( $pointer_id, $dismissed, true ),
		'nonce'       => wp_create_nonce( 'nadlan_help_dismiss' ),
		'ajaxUrl'     => admin_url( 'admin-ajax.php' ),
		'learnMore'   => nadlan_help_common_text( 'learn_more_label', 'tooltip', '' ),
		'pointerTitle'=> isset( $entries['_screen']['tab_title'] ) ? sanitize_text_field( (string) $entries['_screen']['tab_title'] ) : 'NadLan',
	);
	wp_add_inline_script( 'nadlan-contextual-help', 'window.nadlanHelp=' . wp_json_encode( $data, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES ) . ';', 'before' );
	wp_add_inline_script( 'nadlan-contextual-help', <<<'JS'
(function($){
	'use strict';
	var cfg = window.nadlanHelp || {};
	var openTip = null;
	function closeTips(){
		$('.nadlan-help-tooltip').attr('hidden', true);
		$('.nadlan-help-tip').attr('aria-expanded', 'false');
		openTip = null;
	}
	function renderTooltip(item, index){
		var $target = $(item.selector).first();
		if (!$target.length || $target.data('nadlan-help-ready')) { return; }
		$target.data('nadlan-help-ready', true);
		var id = 'nadlan-help-tip-' + cfg.screen + '-' + item.field + '-' + index;
		var $button = $('<button type="button" class="nadlan-help-tip" aria-expanded="false"></button>')
			.attr('aria-describedby', id)
			.text('?');
		var $tip = $('<span class="nadlan-help-tooltip" role="tooltip" hidden></span>')
			.attr('id', id)
			.text(item.tooltip || '');
		if (item.learn_more_url) {
			var learnMore = cfg.learnMore || '';
			if (learnMore) {
				$tip.append(' ').append($('<a></a>').attr('href', item.learn_more_url).text(learnMore));
			}
		}
		var $anchor = $target.closest('label');
		if (!$anchor.length) { $anchor = $target; }
		$anchor.after($tip).after($button);
		$button.on('mouseenter focus click', function(e){
			if (e.type === 'click') { e.preventDefault(); }
			if (openTip && openTip[0] !== $tip[0]) { closeTips(); }
			$tip.removeAttr('hidden');
			$button.attr('aria-expanded', 'true');
			openTip = $tip;
		});
		$button.on('mouseleave blur', function(){
			window.setTimeout(function(){
				if (!$button.is(':focus') && !$button.is(':hover')) {
					$tip.attr('hidden', true);
					$button.attr('aria-expanded', 'false');
				}
			}, 120);
		});
	}
	function dismissPointer(pointerId){
		$.post(cfg.ajaxUrl, {
			action: 'nadlan_help_dismiss_pointer',
			pointer: pointerId,
			nonce: cfg.nonce
		});
	}
	$(document).on('keydown', function(e){
		if (e.key === 'Escape' || e.keyCode === 27) { closeTips(); }
	});
	$(function(){
		(cfg.items || []).forEach(renderTooltip);
		if (!cfg.dismissed && $.fn.pointer && (cfg.items || []).length) {
			var pointerItem = (cfg.items || []).filter(function(item){ return item.pointer_text; })[0];
			if (pointerItem) {
				var $target = $(pointerItem.selector).first();
				if ($target.length) {
					$target.pointer({
						content: '<h3>' + $('<div>').text(cfg.pointerTitle || 'NadLan').html() + '</h3><p>' + $('<div>').text(pointerItem.pointer_text).html() + '</p>',
						position: { edge: 'top', align: 'right' },
						close: function(){ dismissPointer(cfg.pointerId); }
					}).pointer('open');
				}
			}
		}
	});
})(jQuery);
JS
	);
	wp_add_inline_style( 'nadlan-contextual-help', <<<'CSS'
.nadlan-help-tip{display:inline-flex;align-items:center;justify-content:center;width:24px;height:24px;margin-inline-start:8px;border:1px solid #9c7a3c;border-radius:50%;background:#fffaf0;color:#6f5524;font:700 14px/1 system-ui;cursor:pointer;vertical-align:middle}
.nadlan-help-tip:focus-visible{outline:2px solid #1d4ed8;outline-offset:2px}
.nadlan-help-tooltip{display:inline-block;max-width:360px;margin-inline-start:8px;padding:9px 11px;border:1px solid #d6c49f;border-radius:8px;background:#fffdf7;color:#1d2327;box-shadow:0 8px 22px rgba(0,0,0,.09);font-size:14px;line-height:1.55;vertical-align:middle}
.nadlan-help-tooltip[hidden]{display:none}
.nadlan-help-tooltip a{color:#7c5a16;font-weight:700}
.nadlan-help-empty-state{padding:18px;border:1px solid #d6c49f;border-radius:8px;background:#fffdf7;color:#1d2327;text-align:center;font-size:14px;line-height:1.55}
.nadlan-help-empty-state strong{display:block;font-size:16px;margin-bottom:6px}
.nadlan-help-empty-state p{margin:0 0 12px}
.nadlan-help-tab{font-size:14px;line-height:1.65}
CSS
	);
} );

add_action( 'wp_ajax_nadlan_help_dismiss_pointer', function () {
	check_ajax_referer( 'nadlan_help_dismiss', 'nonce' );
	$pointer = isset( $_POST['pointer'] ) ? sanitize_key( wp_unslash( $_POST['pointer'] ) ) : '';
	if ( $pointer === '' || strpos( $pointer, 'nadlan_' ) !== 0 ) {
		wp_send_json_error( array( 'message' => 'bad_pointer' ), 400 );
	}
	$user_id = get_current_user_id();
	if ( ! $user_id ) {
		wp_send_json_error( array( 'message' => 'forbidden' ), 403 );
	}
	$dismissed = array_filter( array_map( 'trim', explode( ',', (string) get_user_meta( $user_id, 'dismissed_wp_pointers', true ) ) ) );
	if ( ! in_array( $pointer, $dismissed, true ) ) {
		$dismissed[] = $pointer;
		update_user_meta( $user_id, 'dismissed_wp_pointers', implode( ',', array_unique( $dismissed ) ) );
	}
	wp_send_json_success( array( 'pointer' => $pointer ) );
} );

add_filter( 'nadlan_config_healthcheck', function ( $out ) {
	$out['help'] = array(
		'loaded'        => true,
		'enabled'       => nadlan_help_enabled(),
		'strings_count' => nadlan_help_strings_count(),
		'screens_count' => count( nadlan_help_strings() ),
	);
	return $out;
} );
