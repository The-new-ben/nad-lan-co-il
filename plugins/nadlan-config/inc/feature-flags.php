<?php
/**
 * nadlan-config - master feature switchboard. Always visible to admins so dark
 * features can be turned on without hunting per-module pages.
 */

if ( ! defined( 'ABSPATH' ) ) { exit; }

if ( ! function_exists( 'nadlan_feature_flags_list' ) ) {
	function nadlan_feature_flags_list() {
		return array(
			'nadlan_feature_lead_e2e'        => array( 'label' => 'מסלול לידים מלא', 'desc' => 'קליטה, אישור מיידי ללקוח, ניתוב לבעל הכרטיס, תיבת פניות וסטטוסים.' ),
			'nadlan_feature_lead_ai_qualify' => array( 'label' => 'סיווג לידים חכם (AI)', 'desc' => 'דירוג אוטומטי, מענה מבוסס תוכן האתר והעברה לנציג בעת הצורך. דורש מפתח OpenAI ומסלול הלידים פעיל.' ),
			'nadlan_feature_lead_nurture'    => array( 'label' => 'מעקב אוטומטי אחרי לידים', 'desc' => 'רצף הודעות המשך בימים 1/3/7/14 עם עצירה אוטומטית בכל תגובה.' ),
			'nadlan_feature_admin_control'   => array( 'label' => 'מסך ניהול לקוחות', 'desc' => 'עריכת מיקום, קישורים ועדיפויות לכל כרטיס, יומן שינויים וצפייה כלקוח.' ),
			'nadlan_feature_project_3d'  => array( 'label' => 'בחירת דירות אינטראקטיבית', 'desc' => 'מפת דירות לחיצה על הדמיית הפרויקט: פרטי דירה, סטטוס ושליחת פנייה ישירה ליזם.' ),
			'nadlan_feature_compound_map' => array( 'label' => 'מפת מתחם תלת-ממדית', 'desc' => 'מפת רחפן תלת-ממדית למתחמי פרויקטים, עם סימון פרויקטים וקישור לכרטיס.' ),
			'nadlan_feature_offers'      => array( 'label' => 'הצעות מחיר לנכסים', 'desc' => 'קונים מגישים הצעות לא מחייבות, המוכר משווה ובוחר. ללא עמלת הצלחה.' ),
			'nadlan_feature_help'            => array( 'label' => 'עזרה מובנית במסכים', 'desc' => 'הסברים קצרים ליד כל שדה ומדריכי מסך.' ),
		);
	}
}

add_action( 'admin_menu', function () {
	add_options_page( 'NadLan Features', 'NadLan Features', 'manage_options', 'nadlan-features', 'nadlan_feature_flags_page' );
} );

if ( ! function_exists( 'nadlan_feature_flags_page' ) ) {
	function nadlan_feature_flags_page() {
		if ( ! current_user_can( 'manage_options' ) ) { return; }
		$flags = nadlan_feature_flags_list();
		if ( isset( $_POST['nadlan_features_save'] ) && check_admin_referer( 'nadlan_features' ) ) {
			foreach ( $flags as $key => $meta ) {
				update_option( $key, ! empty( $_POST[ $key ] ) ? '1' : '0', false );
			}
			if ( ! empty( $_POST['nadlan_mapbox_token_clear'] ) ) {
				delete_option( 'nadlan_mapbox_token' );
			} else {
				$mapbox_token = isset( $_POST['nadlan_mapbox_token'] ) ? sanitize_text_field( wp_unslash( $_POST['nadlan_mapbox_token'] ) ) : '';
				if ( $mapbox_token !== '' ) {
					update_option( 'nadlan_mapbox_token', $mapbox_token, false );
				}
			}
			echo '<div class="updated"><p>נשמר. בדקו את ה-healthcheck לאימות.</p></div>';
		}
		echo '<div class="wrap"><h1>NadLan Features</h1><p>הפעלה מדורגת: מומלץ להדליק יכולת אחת, לבדוק, ואז להמשיך.</p>';
		echo '<form method="post">';
		wp_nonce_field( 'nadlan_features' );
		echo '<input type="hidden" name="nadlan_features_save" value="1"><table class="form-table">';
		foreach ( $flags as $key => $meta ) {
			$on = get_option( $key, '0' ) === '1';
			echo '<tr><th scope="row">' . esc_html( $meta['label'] ) . '</th><td><label><input type="checkbox" name="' . esc_attr( $key ) . '" value="1" ' . checked( $on, true, false ) . '> פעיל</label><p class="description">' . esc_html( $meta['desc'] ) . ' <code>' . esc_html( $key ) . '</code></p></td></tr>';
		}
		$mapbox_ready = get_option( 'nadlan_mapbox_token', '' ) !== '';
		echo '<tr><th scope="row">Mapbox</th><td>';
		echo '<label>מפתח מפה חדש<br><input type="password" name="nadlan_mapbox_token" value="" class="regular-text" autocomplete="off" placeholder="' . esc_attr( $mapbox_ready ? 'מפתח מוגדר, הדביקו חדש להחלפה' : 'הדביקו Mapbox public token' ) . '"></label>';
		echo '<p class="description">' . esc_html( $mapbox_ready ? 'מפתח מפה מוגדר. הוא אינו מוצג כאן מחדש.' : 'נדרש להפעלת מפת המתחם. בלי מפתח, המשתמשים יראו הודעה ידידותית.' ) . '</p>';
		if ( $mapbox_ready ) {
			echo '<label><input type="checkbox" name="nadlan_mapbox_token_clear" value="1"> מחיקת מפתח המפה</label>';
		}
		echo '</td></tr>';
		echo '</table>';
		submit_button( 'שמור הגדרות' );
		echo '</form><p><a href="' . esc_url( home_url( '/wp-json/nadlan/v1/healthcheck' ) ) . '" target="_blank">בדיקת מצב חי (healthcheck)</a></p></div>';
	}
}

add_filter( 'nadlan_config_healthcheck', function ( $out ) {
	$state = array();
	foreach ( nadlan_feature_flags_list() as $key => $meta ) {
		$state[ str_replace( 'nadlan_feature_', '', $key ) ] = get_option( $key, '0' ) === '1';
	}
	$out['feature_flags'] = $state;
	return $out;
} );
