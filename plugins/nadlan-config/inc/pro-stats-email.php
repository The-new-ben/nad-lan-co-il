<?php
/**
 * nadlan-config - MONTHLY PRO STATS EMAIL (retention moat, built 2026-07-07).
 *
 * Advertisers who see their numbers renew. Once a month every claimed,
 * published professional card's owner gets a short honest report: profile
 * views, leads, content impressions (procard_impressions - renders inside
 * encyclopedia/guide pages), and sponsorship status with a renewal path.
 *
 * OWNER LAW - emails/deliverability come LAST: sending is OFF until the
 * option `nadlan_pro_stats_email_enabled` is set to '1'. Until then the
 * module only exposes an admin-gated PREVIEW endpoint so the email can be
 * verified without a single message leaving the site:
 *
 *   GET /nadlan/v1/pro-stats-preview?card=<id>   (manage_options)
 */

if ( ! defined( 'ABSPATH' ) ) { exit; }

if ( ! function_exists( 'nadlan_pro_stats_html' ) ) {
	function nadlan_pro_stats_html( $card_id ) {
		$views = (int) get_post_meta( $card_id, 'view_count', true );
		$imps  = (int) get_post_meta( $card_id, 'procard_impressions', true );
		$leads = function_exists( 'nadlan_ac_lead_count' ) ? (int) nadlan_ac_lead_count( $card_id ) : 0;
		$spon  = (int) get_post_meta( $card_id, 'procard_sponsor_until', true );
		$tier  = (string) get_post_meta( $card_id, 'paid_tier', true );
		$name  = get_the_title( $card_id );
		$rows  = array(
			array( 'צפיות בכרטיס', $views ),
			array( 'פניות שהתקבלו', $leads ),
			array( 'הופעות בתכני התחום', $imps ),
		);
		$tr = '';
		foreach ( $rows as $r ) {
			$tr .= '<tr><td style="padding:10px 14px;border-bottom:1px solid #E2DCD0;font:400 14px Heebo,Arial,sans-serif;color:#51483A">' . esc_html( $r[0] ) . '</td><td style="padding:10px 14px;border-bottom:1px solid #E2DCD0;font:700 16px Heebo,Arial,sans-serif;color:#1B1A17" align="left">' . number_format_i18n( $r[1] ) . '</td></tr>';
		}
		if ( $spon >= time() ) {
			$sline = 'חסות תוכן פעילה עד ' . wp_date( 'd/m/Y', $spon ) . '.';
		} elseif ( $spon > 0 ) {
			$sline = 'חסות התוכן שלכם הסתיימה - חידוש מחזיר את הכרטיס להוביל את תכני התחום.';
		} else {
			$sline = 'חדש: חסות על תחום תוכן מציגה את הכרטיס ראשון בכל מונחי האנציקלופדיה והמדריכים של התחום.';
		}
		return '<div dir="rtl" style="max-width:560px;margin:0 auto;background:#FAF7F1;border:1px solid #E2DCD0;border-radius:14px;overflow:hidden">' .
			'<div style="background:#14130F;color:#FAF7F1;padding:22px 24px;font:700 19px \'Frank Ruhl Libre\',Georgia,serif">הדוח החודשי שלכם - ' . esc_html( $name ) . '</div>' .
			'<div style="padding:20px 24px">' .
			'<p style="font:400 14px/1.6 Heebo,Arial,sans-serif;color:#51483A;margin:0 0 14px">כך עבד הכרטיס שלכם בנדלן בחודש האחרון (מסלול ' . esc_html( $tier ?: 'free' ) . '):</p>' .
			'<table width="100%" cellspacing="0" cellpadding="0" style="background:#fff;border:1px solid #E2DCD0;border-radius:10px">' . $tr . '</table>' .
			'<p style="font:600 13.5px/1.6 Heebo,Arial,sans-serif;color:#8A6B2F;margin:16px 0 6px">' . esc_html( $sline ) . '</p>' .
			'<p style="margin:18px 0 4px"><a href="' . esc_url( home_url( '/advertiser-center/' ) ) . '" style="display:inline-block;background:#9C7A3C;color:#FAF7F1;font:700 14px Heebo,Arial,sans-serif;border-radius:10px;padding:12px 18px;text-decoration:none">למרכז הפרסום המלא</a> ' .
			'<a href="' . esc_url( home_url( '/advertise/#nlspon' ) ) . '" style="display:inline-block;background:#fff;border:1.5px solid #9C7A3C;color:#8A6B2F;font:700 14px Heebo,Arial,sans-serif;border-radius:10px;padding:11px 18px;text-decoration:none;margin-inline-start:8px">חסות תחום - ₪199</a></p>' .
			'<p style="font:400 11.5px/1.6 Heebo,Arial,sans-serif;color:#6D665C;margin:14px 0 0">הנתונים נמדדים באתר nad-lan.co.il בלבד. אפשר לבטל את הדוח בהגדרות מרכז הפרסום.</p>' .
			'</div></div>';
	}
}

/* admin-gated preview: verify the email without sending anything */
add_action( 'rest_api_init', function () {
	register_rest_route( 'nadlan/v1', '/pro-stats-preview', array(
		'methods' => 'GET',
		'permission_callback' => function () { return current_user_can( 'manage_options' ); },
		'callback' => function ( WP_REST_Request $req ) {
			$id = (int) $req->get_param( 'card' );
			$p  = get_post( $id );
			if ( ! $p || 'nadlan_professional' !== $p->post_type ) {
				return new WP_Error( 'not_found', 'professional not found', array( 'status' => 404 ) );
			}
			return new WP_REST_Response( array( 'ok' => true, 'html' => nadlan_pro_stats_html( $id ) ), 200 );
		},
	) );
} );

/* monthly send - ARMED ONLY when the owner flips the flag (emails LAST law) */
add_action( 'init', function () {
	$on = get_option( 'nadlan_pro_stats_email_enabled', '0' ) === '1';
	$scheduled = wp_next_scheduled( 'nadlan_pro_stats_email' );
	if ( $on && ! $scheduled ) {
		wp_schedule_event( strtotime( 'first day of next month 09:10' ), 'monthly', 'nadlan_pro_stats_email' );
	} elseif ( ! $on && $scheduled ) {
		wp_unschedule_event( $scheduled, 'nadlan_pro_stats_email' );
	}
}, 20 );

add_filter( 'cron_schedules', function ( $s ) {
	if ( ! isset( $s['monthly'] ) ) {
		$s['monthly'] = array( 'interval' => 30 * DAY_IN_SECONDS, 'display' => 'Monthly' );
	}
	return $s;
} );

add_action( 'nadlan_pro_stats_email', function () {
	if ( get_option( 'nadlan_pro_stats_email_enabled', '0' ) !== '1' ) { return; }
	$cards = get_posts( array(
		'post_type' => 'nadlan_professional', 'post_status' => 'publish', 'posts_per_page' => 200, 'fields' => 'ids',
		'meta_query' => array( array( 'key' => 'owner_user_id', 'compare' => 'EXISTS' ) ),
	) );
	foreach ( $cards as $id ) {
		$uid  = (int) get_post_meta( $id, 'owner_user_id', true );
		$user = $uid ? get_user_by( 'id', $uid ) : null;
		if ( ! $user || ! is_email( $user->user_email ) ) { continue; }
		if ( get_user_meta( $uid, 'nadlan_stats_email_optout', true ) ) { continue; }
		wp_mail(
			$user->user_email,
			'הדוח החודשי של הכרטיס שלכם בנדלן - ' . get_the_title( $id ),
			nadlan_pro_stats_html( $id ),
			array( 'Content-Type: text/html; charset=UTF-8' )
		);
	}
} );
