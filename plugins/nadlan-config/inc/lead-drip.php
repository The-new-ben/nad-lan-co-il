<?php
/**
 * nadlan-config — Lead nurture drip engine (v1.12.0)
 *
 * 2026 best-practice (research): segmented state machine —
 *   new → active (0-14d) → mid (15d-6mo) → long (6-18mo); auto-respond < 2 min;
 *   5-8 emails over 30-60d for standard drip; demote if no engagement; opt-out
 *   on every email; SMS is higher-OR but defer (provider TODO).
 *
 * Wires onto nadlan_lead post creation: stamps drip_state=new + nudges into
 * 'active'. Cron checks daily, sends due steps (Hebrew, RTL-aware mailto-style),
 * advances state, demotes silent leads.
 *
 * BLANKS: SMS/WhatsApp channel (Twilio/local), engagement tracking pixel (privacy
 * decision — IL Privacy Protection Law), branded HTML template, A leads escalation
 * to phone. Default = email only, opt-out link mandatory.
 */

if ( ! defined( 'ABSPATH' ) ) { exit; }

if ( ! function_exists( 'nadlan_drip_steps' ) ) {
	/** Sequence: array of {delay_days, subject, body_template}. {NAME}/{OPTOUT}/{CITY}/{GOAL} substituted. */
	function nadlan_drip_steps() {
		return apply_filters( 'nadlan_drip_steps', array(
			array( 'delay' => 0,  'subject' => 'שלום ל{NAME} — קיבלנו את הפנייה שלך',
				'body' => "שלום {NAME},\n\nתודה שפנית לנדלן. נחזור אליך בהקדם בנוגע ל-{GOAL}.\n\nבינתיים תוכל לקבל אומדן שווי, להשוות נכסים ולהירשם להתראות על דירות חדשות:\nhttps://nad-lan.co.il/\n\nלהסרה מההתראות: {OPTOUT}" ),
			array( 'delay' => 2,  'subject' => '5 דברים שכדאי לבדוק לפני חתימת חוזה דירה',
				'body' => "שלום {NAME},\n\nלפני שחותמים על חוזה, יש כמה דגלים אדומים נפוצים — הערת אזהרה, פיגורי תשלום, חריגות בנייה ועוד. הכנו לך מדריך קצר:\nhttps://nad-lan.co.il/real-estate-lawyer/\n\nואם כבר יש חוזה ביד — ביקורת ב-48 שעות: https://nad-lan.co.il/contract-audit/\n\nלהסרה: {OPTOUT}" ),
			array( 'delay' => 5,  'subject' => 'דירות חדשות ב{CITY}',
				'body' => "שלום {NAME},\n\nרוצה לקבל התראה אוטומטית על דירות חדשות ב{CITY}? הירשם כאן:\nhttps://nad-lan.co.il/?saved=1\n\nלהסרה: {OPTOUT}" ),
			array( 'delay' => 14, 'subject' => 'איך הולך החיפוש?',
				'body' => "שלום {NAME},\n\nרצינו לבדוק איך מתקדם החיפוש. נשמח לעזור — השב/י למייל זה או חייג/י 052-510-1555.\n\nלהסרה: {OPTOUT}" ),
			array( 'delay' => 30, 'subject' => 'עדכון שוק חודשי',
				'body' => "שלום {NAME},\n\nעדכון חודשי על מחירי דירות ועסקאות באזורך נמצא כאן:\nhttps://nad-lan.co.il/\n\nלהסרה: {OPTOUT}" ),
			array( 'delay' => 60, 'subject' => 'עדיין מחפש/ת?',
				'body' => "שלום {NAME},\n\nאם החיפוש עוד פעיל — הנה כלים שיעזרו: הערכת שווי, ביקורת חוזה, השוואת נכסים.\nhttps://nad-lan.co.il/\n\nלהסרה: {OPTOUT}" ),
		) );
	}
}

/* On lead creation: stamp drip state + send immediate ack */
add_action( 'wp_insert_post', function ( $post_id, $post, $update ) {
	if ( $update ) { return; }
	// OFF by default since 2026-07-02 (module audit): this legacy drip overlapped
	// the e2e acknowledgement + nurture sequences, double-emailing every lead.
	if ( get_option( 'nadlan_feature_lead_drip', '0' ) !== '1' ) { return; }
	if ( ( $post->post_type ?? '' ) !== 'nadlan_lead' ) { return; }
	$email = (string) get_post_meta( $post_id, 'email', true );
	if ( ! is_email( $email ) ) { return; }
	update_post_meta( $post_id, 'drip_state', 'active' );
	update_post_meta( $post_id, 'drip_step', 0 );
	update_post_meta( $post_id, 'drip_started', time() );
	nadlan_drip_send( $post_id, 0 ); // step 0 immediately (welcome)
}, 30, 3 );

if ( ! function_exists( 'nadlan_drip_optout_token' ) ) {
	function nadlan_drip_optout_token( $lead_id ) {
		$t = (string) get_post_meta( $lead_id, 'optout_token', true );
		if ( ! $t ) { $t = strtolower( bin2hex( random_bytes( 16 ) ) ); update_post_meta( $lead_id, 'optout_token', $t ); }
		return $t;
	}
}

if ( ! function_exists( 'nadlan_drip_send' ) ) {
	function nadlan_drip_send( $lead_id, $step_idx ) {
		if ( get_post_meta( $lead_id, 'drip_state', true ) === 'optout' ) { return; }
		$steps = nadlan_drip_steps();
		if ( ! isset( $steps[ $step_idx ] ) ) { return; }
		$s = $steps[ $step_idx ];
		$email = (string) get_post_meta( $lead_id, 'email', true );
		if ( ! is_email( $email ) ) { return; }
		$name  = (string) get_post_meta( $lead_id, 'name', true ) ?: 'שלום';
		$city  = (string) get_post_meta( $lead_id, 'city', true ) ?: 'אזורך';
		$goal  = (string) get_post_meta( $lead_id, 'goal', true ) ?: (string) get_post_meta( $lead_id, 'topic', true ) ?: 'פנייתך';
		$opt   = add_query_arg( array( 'lead' => $lead_id, 'tok' => nadlan_drip_optout_token( $lead_id ) ),
			rest_url( 'nadlan/v1/drip-optout' ) );
		$repl  = array( '{NAME}' => $name, '{CITY}' => $city, '{GOAL}' => $goal, '{OPTOUT}' => $opt );
		$subject = strtr( $s['subject'], $repl );
		$body    = strtr( $s['body'], $repl );
		wp_mail( $email, $subject, $body, array( 'Content-Type: text/plain; charset=UTF-8' ) );
		update_post_meta( $lead_id, 'drip_step', $step_idx + 1 );
		update_post_meta( $lead_id, 'drip_last_sent', time() );
	}
}

/* Opt-out REST */
add_action( 'rest_api_init', function () {
	register_rest_route( 'nadlan/v1', '/drip-optout', array(
		'methods' => 'GET', 'permission_callback' => '__return_true',
		'callback' => function ( $req ) {
			$id = (int) $req->get_param( 'lead' );
			$t  = sanitize_text_field( (string) $req->get_param( 'tok' ) );
			if ( $id && hash_equals( (string) get_post_meta( $id, 'optout_token', true ), $t ) ) {
				update_post_meta( $id, 'drip_state', 'optout' );
				wp_safe_redirect( home_url( '/?drip=removed' ) ); exit;
			}
			wp_safe_redirect( home_url( '/?drip=invalid' ) ); exit;
		},
	) );
} );

/* Daily cron — send due steps + state transitions */
add_action( 'nadlan_drip_daily', function () {
	$steps = nadlan_drip_steps();
	$leads = get_posts( array( 'post_type' => 'nadlan_lead', 'posts_per_page' => 500, 'post_status' => 'private',
		'meta_query' => array( array( 'key' => 'drip_state', 'value' => array( 'active', 'mid', 'long' ), 'compare' => 'IN' ) ) ) );
	foreach ( $leads as $lead ) {
		$state   = (string) get_post_meta( $lead->ID, 'drip_state', true );
		$step    = (int) get_post_meta( $lead->ID, 'drip_step', true );
		$started = (int) get_post_meta( $lead->ID, 'drip_started', true ) ?: get_post_time( 'U', true, $lead );
		$age_d   = (int) floor( ( time() - $started ) / DAY_IN_SECONDS );
		if ( isset( $steps[ $step ] ) && $age_d >= (int) $steps[ $step ]['delay'] ) {
			nadlan_drip_send( $lead->ID, $step );
		}
		// State transitions
		if ( $age_d > 14 && $state === 'active' )  { update_post_meta( $lead->ID, 'drip_state', 'mid' ); }
		if ( $age_d > 180 && $state !== 'long' )   { update_post_meta( $lead->ID, 'drip_state', 'long' ); }
		if ( $age_d > 540 )                        { update_post_meta( $lead->ID, 'drip_state', 'archive' ); }
	}
} );
if ( ! wp_next_scheduled( 'nadlan_drip_daily' ) ) {
	wp_schedule_event( time() + 3600, 'daily', 'nadlan_drip_daily' );
}
