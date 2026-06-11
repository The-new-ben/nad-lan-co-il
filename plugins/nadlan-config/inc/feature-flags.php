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
