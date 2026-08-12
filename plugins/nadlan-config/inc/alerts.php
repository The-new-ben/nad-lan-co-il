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

/* 2. a new lead arrived - rich alert, delayed 2 minutes so the AI
 * qualification and card routing (which run seconds after insert) are
 * included. Owner law 2026-08-12: full context + one-tap actions, no
 * promises, no nagging ladder. */
add_action( 'wp_after_insert_post', function ( $post_id, $post, $update ) {
	if ( $update || ! $post || 'nadlan_lead' !== $post->post_type ) { return; }
	wp_schedule_single_event( time() + 120, 'nadlan_lead_rich_alert', array( (int) $post_id ) );
}, 20, 3 );

add_action( 'nadlan_lead_rich_alert', function ( $lead_id ) {
	global $wpdb;
	$l = get_post( $lead_id );
	if ( ! $l || 'nadlan_lead' !== $l->post_type ) { return; }
	$m = function ( $k ) use ( $lead_id ) { return (string) get_post_meta( $lead_id, $k, true ); };
	$phone = preg_replace( '/\D+/', '', $m( 'phone' ) );
	$wa    = $phone ? ( '972' . ltrim( $phone, '0' ) ) : '';
	$lines = array(
		'שם: ' . $m( 'name' ),
		'טלפון: ' . $m( 'phone' ) . ( $phone ? '  |  חיוג: tel:' . $phone . '  |  וואטסאפ: https://wa.me/' . $wa : '' ),
		'אימייל: ' . $m( 'email' ),
		'הודעה: ' . mb_substr( wp_strip_all_tags( $l->post_content ), 0, 200 ),
		'',
	);
	$card_id = (int) $m( 'project_wp_id' );
	if ( $card_id > 0 ) {
		$g = function ( $k ) use ( $card_id ) { return (string) get_post_meta( $card_id, $k, true ); };
		$lines[] = 'הפרויקט: ' . get_the_title( $card_id );
		$lines[] = 'עמוד: ' . get_permalink( $card_id );
		$lines[] = 'עיר: ' . $g( 'city' ) . ' | יזם: ' . ( $g( 'developer_name' ) ?: 'לא ידוע' )
			. ' | יח״ד: ' . $g( 'num_units' ) . ' | כרטיס: ' . ( $g( 'claim_status' ) ?: 'לא נתבע' );
	} elseif ( '' !== $m( 'project_title' ) ) {
		$lines[] = 'הפרויקט (לא זוהה כרטיס): ' . $m( 'project_title' );
	}
	$score = $m( 'lead_score' );
	if ( '' !== $score ) {
		$lines[] = '';
		$lines[] = 'ניתוח AI: ציון ' . $score . ' | דירוג ' . $m( 'lead_ai_tier' )
			. ( $m( 'lead_ai_missing_field' ) ? ' | חסר: ' . $m( 'lead_ai_missing_field' ) : '' );
	}
	$dup = $phone ? (int) $wpdb->get_var( $wpdb->prepare(
		"SELECT COUNT(*) FROM {$wpdb->postmeta} WHERE meta_key='phone' AND meta_value=%s", $m( 'phone' ) ) ) : 0;
	$lines[] = 'אמינות: טלפון נראה ' . $dup . ' פעמים | מקור: ' . ( $m( 'utm_source' ) ?: '-' )
		. ' | אישור אוטומטי לפונה: ' . ( 'sent' === $m( 'lead_ack_status' ) ? 'נשלח' : 'לא נשלח' );
	$lines[] = '';
	$lines[] = 'ניהול הליד: ' . admin_url( 'post.php?post=' . $lead_id . '&action=edit' );
	nadlan_alert_mail( 'ליד חדש: ' . $m( 'name' ) . ( $card_id > 0 ? ' - ' . get_the_title( $card_id ) : '' ), $lines );
} );

/* 2b. one daily reminder, morning only, no nagging: leads still "new" from
 * yesterday or earlier. */
add_action( 'init', function () {
	if ( ! wp_next_scheduled( 'nadlan_leads_daily' ) ) {
		wp_schedule_event( strtotime( 'tomorrow 07:00' ), 'daily', 'nadlan_leads_daily' );
	}
} );
add_action( 'nadlan_leads_daily', function () {
	$stale = get_posts( array( 'post_type' => 'nadlan_lead', 'post_status' => 'any', 'numberposts' => 20,
		'date_query' => array( array( 'before' => '20 hours ago' ) ),
		'meta_query' => array( array( 'key' => 'lead_status', 'value' => 'new' ) ) ) );
	if ( ! $stale ) { return; }
	$lines = array( 'לידים שעדיין מסומנים "חדש" ולא טופלו:' );
	foreach ( $stale as $l ) {
		$lines[] = '• ' . get_post_meta( $l->ID, 'name', true ) . ' | ' . get_post_meta( $l->ID, 'phone', true )
			. ' | ' . $l->post_date . ' | ' . admin_url( 'post.php?post=' . $l->ID . '&action=edit' );
	}
	nadlan_alert_mail( 'תזכורת יומית: ' . count( $stale ) . ' לידים ממתינים', $lines );
} );

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
