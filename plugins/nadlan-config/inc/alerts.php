<?php
/**
 * nadlan-config - Owner alerts (v1.72.188)
 *
 * Owner law 2026-08-11: "alert on everything that is done in the system by
 * external users - I need to know what's going on." Instant email to the site
 * admin on: new user registration, new lead, card-claim request, advertiser
 * order link, any revenue webhook event. Plus a weekly digest of config gaps
 * (billing key missing, stale pending claims, cities newly qualifying for a
 * hub page) - alert-first, never auto-create.
 */

if ( ! defined( 'ABSPATH' ) ) { exit; }

if ( ! function_exists( 'nadlan_alert_mail' ) ) {
	function nadlan_alert_mail( $subject, $lines ) {
		$to = get_option( 'admin_email' );
		if ( ! $to ) { return; }
		$body = implode( "\n", array_map( 'wp_strip_all_tags', (array) $lines ) )
			. "\n\n-- nad-lan.co.il " . gmdate( 'Y-m-d H:i' ) . ' UTC';
		wp_mail( $to, '[נדלן] ' . $subject, $body );
	}
}

/* 1. someone registered on the site */
add_action( 'user_register', function ( $user_id ) {
	$u = get_user_by( 'id', $user_id );
	if ( ! $u ) { return; }
	nadlan_alert_mail( 'משתמש חדש נרשם לאתר', array(
		'נרשם משתמש חדש:',
		'שם: ' . $u->display_name,
		'אימייל: ' . $u->user_email,
		'תפקיד: ' . implode( ',', (array) $u->roles ),
		'ניהול: ' . admin_url( 'user-edit.php?user_id=' . $user_id ),
	) );
}, 20 );

/* 2. a new lead arrived */
add_action( 'wp_after_insert_post', function ( $post_id, $post, $update ) {
	if ( $update || ! $post || 'nadlan_lead' !== $post->post_type ) { return; }
	nadlan_alert_mail( 'ליד חדש התקבל', array(
		'התקבל ליד חדש: ' . $post->post_title,
		'מקור: ' . (string) get_post_meta( $post_id, 'source', true ),
		'טלפון: ' . (string) get_post_meta( $post_id, 'phone', true ),
		'אימייל: ' . (string) get_post_meta( $post_id, 'email', true ),
		'ניהול: ' . admin_url( 'edit.php?post_type=nadlan_lead' ),
	) );
}, 20, 3 );

/* 3. someone asked to claim a card */
$nadlan_alert_claim = function ( $meta_id, $object_id, $meta_key, $meta_value ) {
	if ( 'claim_status' !== $meta_key || 'pending' !== (string) $meta_value ) { return; }
	nadlan_alert_mail( 'בקשת בעלות חדשה על כרטיס', array(
		'מישהו ביקש בעלות על הכרטיס: ' . get_the_title( $object_id ),
		'כרטיס: ' . get_permalink( $object_id ),
		'שם: ' . (string) get_post_meta( $object_id, 'claim_name', true ),
		'אימייל: ' . (string) get_post_meta( $object_id, 'claim_email', true ),
		'טלפון: ' . (string) get_post_meta( $object_id, 'claim_phone', true ),
	) );
};
add_action( 'added_post_meta', $nadlan_alert_claim, 20, 4 );
add_action( 'updated_post_meta', $nadlan_alert_claim, 20, 4 );

/* 4. money events: order linked to a card, or a billing webhook fired */
add_action( 'nadlan_revenue_event', function ( $type, $amount = 0, $meta = array() ) {
	nadlan_alert_mail( 'אירוע חיוב: ' . $type, array(
		'סוג: ' . $type,
		'סכום: ' . $amount,
		'פרטים: ' . wp_json_encode( $meta, JSON_UNESCAPED_UNICODE ),
	) );
}, 20, 3 );

/* 5. weekly owner digest: config gaps + waiting items + qualifying cities */
add_action( 'init', function () {
	if ( ! wp_next_scheduled( 'nadlan_owner_digest' ) ) {
		wp_schedule_event( time() + DAY_IN_SECONDS, 'weekly', 'nadlan_owner_digest' );
	}
} );
add_action( 'nadlan_owner_digest', function () {
	global $wpdb;
	$lines = array( 'דוח שבועי - מה מחכה לטיפול:' );
	if ( '' === (string) get_option( 'nadlan_gi_webhook_secret', '' ) ) {
		$lines[] = '• מפתח הסליקה (GreenInvoice) עדיין לא מחובר - אי אפשר לקבל תשלומים.';
	}
	$pending = (int) $wpdb->get_var( "SELECT COUNT(*) FROM {$wpdb->postmeta} WHERE meta_key='claim_status' AND meta_value='pending'" );
	if ( $pending > 0 ) {
		$lines[] = '• ' . $pending . ' בקשות בעלות על כרטיסים ממתינות לאישור.';
	}
	$week_leads = (int) $wpdb->get_var( "SELECT COUNT(*) FROM {$wpdb->posts} WHERE post_type='nadlan_lead' AND post_date > DATE_SUB(NOW(), INTERVAL 7 DAY)" );
	$lines[] = '• לידים שהתקבלו השבוע: ' . $week_leads . '.';
	if ( function_exists( 'nadlan_hub_query' ) ) {
		$cities = $wpdb->get_results( "SELECT pm.meta_value AS city, COUNT(*) AS n FROM {$wpdb->postmeta} pm
			JOIN {$wpdb->posts} p ON p.ID = pm.post_id AND p.post_type='nadlan_project' AND p.post_status='publish'
			WHERE pm.meta_key='city' AND pm.meta_value<>'' GROUP BY pm.meta_value HAVING n >= 10 ORDER BY n DESC LIMIT 30" );
		$missing = array();
		foreach ( $cities as $c ) {
			if ( ! get_page_by_path( 'city/' . sanitize_title( $c->city ) . '/projects' ) ) {
				$missing[] = $c->city . ' (' . $c->n . ')';
			}
		}
		if ( $missing ) {
			$lines[] = '• ערים עם מספיק פרויקטים אך עדיין בלי עמוד עיר: ' . implode( ', ', array_slice( $missing, 0, 10 ) ) . '. עמוד חדש נוצר רק באישורך.';
		}
	}
	if ( count( $lines ) > 1 ) {
		nadlan_alert_mail( 'דוח שבועי לבעלים', $lines );
	}
} );
