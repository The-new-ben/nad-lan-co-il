<?php
/**
 * nadlan-config - MILESTONE CHANGE NOTIFICATIONS (2026-07-07).
 *
 * The other half of the Lennar/Buildertrend retention pattern: when a
 * project's reported stage ADVANCES (project_status meta change that maps to
 * a later lifecycle stage), every buyer who inquired about that project gets
 * a short honest update with a link back to the project page.
 *
 * OWNER LAW - emails/deliverability LAST: sending is OFF until
 * `nadlan_milestone_notify_enabled` is '1'. Until then the module only
 * RECORDS the pending notifications (option queue, capped) so nothing is
 * lost and the owner can flip the switch after SMTP work. Admin preview:
 *   GET /nadlan/v1/milestone-notify-queue   (manage_options)
 */

if ( ! defined( 'ABSPATH' ) ) { exit; }

add_action( 'updated_post_meta', function ( $meta_id, $post_id, $meta_key, $meta_value ) {
	if ( 'project_status' !== $meta_key || 'nadlan_project' !== get_post_type( $post_id ) ) { return; }
	if ( ! function_exists( 'nadlan_ms_stage_of' ) ) { return; }
	$new_stage = nadlan_ms_stage_of( (string) $meta_value );
	$old_stage = (int) get_post_meta( $post_id, '_nadlan_ms_last_stage', true );
	update_post_meta( $post_id, '_nadlan_ms_last_stage', max( 0, $new_stage ) );
	// only a real ADVANCE notifies - corrections backward stay silent
	if ( $new_stage < 0 || $new_stage <= $old_stage ) { return; }

	// collect the project's inquirers (leads carrying this project's slug)
	$slug  = get_post( $post_id )->post_name;
	$leads = get_posts( array(
		'post_type' => 'nadlan_lead', 'post_status' => 'any', 'posts_per_page' => 300, 'fields' => 'ids',
		'meta_query' => array( 'relation' => 'OR',
			array( 'key' => 'project_slug', 'value' => $slug ),
			array( 'key' => 'lead_card_id', 'value' => $post_id, 'type' => 'NUMERIC' ),
		),
	) );
	$emails = array();
	foreach ( $leads as $lid ) {
		$e = sanitize_email( (string) get_post_meta( $lid, 'email', true ) );
		if ( is_email( $e ) ) { $emails[ $e ] = true; }
	}
	if ( ! $emails ) { return; }

	$labels = array( 'תכנון', 'היתר בנייה', 'שיווק ומכירות', 'בנייה', 'טופס 4 ומסירה' );
	$title  = get_the_title( $post_id );
	$stage_label = $labels[ min( $new_stage, 4 ) ];
	$entry = array(
		'project'  => $slug,
		'title'    => $title,
		'stage'    => $stage_label,
		'status'   => trim( (string) $meta_value ),
		'emails'   => count( $emails ),
		'at'       => current_time( 'mysql' ),
	);

	if ( get_option( 'nadlan_milestone_notify_enabled', '0' ) === '1' ) {
		$subject = 'עדכון מהפרויקט ' . $title . ': ' . $stage_label;
		$body = '<div dir="rtl" style="font-family:Heebo,Arial,sans-serif;max-width:540px;margin:0 auto">' .
			'<h2 style="font-family:\'Frank Ruhl Libre\',Georgia,serif;color:#1B1A17">' . esc_html( $title ) . ' התקדם לשלב: ' . esc_html( $stage_label ) . '</h2>' .
			'<p style="color:#51483A;line-height:1.7">התעניינתם בפרויקט הזה בנדלן, אז רצינו שתדעו ראשונים. השלב כפי שדווח לפרויקט; לוחות הזמנים באחריות היזם.</p>' .
			'<p><a href="' . esc_url( get_permalink( $post_id ) ) . '" style="display:inline-block;background:#9C7A3C;color:#FAF7F1;font-weight:700;border-radius:10px;padding:12px 18px;text-decoration:none">לעמוד הפרויקט המעודכן</a></p>' .
			'<p style="font-size:11.5px;color:#6D665C">קיבלתם עדכון זה כי השארתם פנייה על הפרויקט באתר nad-lan.co.il.</p></div>';
		foreach ( array_keys( $emails ) as $to ) {
			wp_mail( $to, $subject, $body, array( 'Content-Type: text/html; charset=UTF-8' ) );
		}
		$entry['sent'] = true;
	} else {
		$entry['sent'] = false;
	}
	$q = (array) get_option( 'nadlan_ms_notify_log', array() );
	array_unshift( $q, $entry );
	update_option( 'nadlan_ms_notify_log', array_slice( $q, 0, 40 ), false );
}, 10, 4 );

add_action( 'rest_api_init', function () {
	register_rest_route( 'nadlan/v1', '/milestone-notify-queue', array(
		'methods' => 'GET',
		'permission_callback' => function () { return current_user_can( 'manage_options' ); },
		'callback' => function () {
			return new WP_REST_Response( array(
				'enabled' => get_option( 'nadlan_milestone_notify_enabled', '0' ) === '1',
				'log'     => (array) get_option( 'nadlan_ms_notify_log', array() ),
			), 200 );
		},
	) );
} );
