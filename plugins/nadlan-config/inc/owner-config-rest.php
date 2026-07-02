<?php
/**
 * nadlan-config — Owner-config REST + preferred-partners auto-route (v1.40.1)
 *
 * Two things at once:
 *  A) Expose `nadlan_owner_whatsapp` and `nadlan_preferred_partners` for REST
 *     writes by authenticated admins (app password OK). Auth: manage_options.
 *     This lets any agent (Claude/Codex/Cowork) set/seed these without
 *     navigating WP-admin. The admin pages still own the UI; this is just
 *     the API surface.
 *  B) Close the v1.40.0 gap: actually USE the preferred-partners list when a
 *     lead is routed through the Lead Ledger without a partner_id, OR when
 *     the lead is generic (concierge / sticky CTA). The picker
 *     `nadlan_pp_pick()` already exists; this wires it in.
 *
 * Safety: still NEVER cold-emails the 2,700 imported contractors. Only people
 * listed under `nadlan_preferred_partners` ever receive routed leads.
 */
if ( ! defined( 'ABSPATH' ) ) { exit; }

/* -------------------------------------------------------------------------
 * A) REST endpoints for owner-config writes (auth: manage_options)
 * ------------------------------------------------------------------------- */
add_action( 'rest_api_init', function () {

	$auth = function () {
		return current_user_can( 'manage_options' );
	};

	// GET/POST WhatsApp owner number
	register_rest_route( 'nadlan/v1', '/owner/whatsapp', array(
		array(
			'methods' => 'GET',
			'permission_callback' => $auth,
			'callback' => function () {
				return array( 'whatsapp' => (string) get_option( 'nadlan_owner_whatsapp', '' ) );
			},
		),
		array(
			'methods' => 'POST',
			'permission_callback' => $auth,
			'callback' => function ( $req ) {
				$p = $req->get_json_params() ?: array();
				$num = preg_replace( '/[^0-9+]/', '', (string) ( $p['whatsapp'] ?? '' ) );
				update_option( 'nadlan_owner_whatsapp', $num );
				return array( 'ok' => true, 'whatsapp' => $num );
			},
		),
	) );

	// GET/POST preferred partners list (full replace)
	register_rest_route( 'nadlan/v1', '/owner/partners', array(
		array(
			'methods' => 'GET',
			'permission_callback' => $auth,
			'callback' => function () {
				return array( 'partners' => function_exists( 'nadlan_pp_list' ) ? nadlan_pp_list() : array() );
			},
		),
		array(
			'methods' => 'POST',
			'permission_callback' => $auth,
			'callback' => function ( $req ) {
				$p = $req->get_json_params() ?: array();
				$rows = isset( $p['partners'] ) && is_array( $p['partners'] ) ? $p['partners'] : array();
				$clean = array();
				foreach ( $rows as $r ) {
					$name  = sanitize_text_field( (string) ( $r['name'] ?? '' ) );
					$email = sanitize_email( (string) ( $r['email'] ?? '' ) );
					if ( ! $name || ! $email ) { continue; }
					$clean[] = array(
						'name'  => $name,
						'email' => $email,
						'phone' => preg_replace( '/[^0-9+]/', '', (string) ( $r['phone'] ?? '' ) ),
						'profession' => sanitize_key( (string) ( $r['profession'] ?? '' ) ),
						'city'  => sanitize_text_field( (string) ( $r['city'] ?? '' ) ),
						'pct'   => max( 0.0, min( 100.0, (float) ( $r['pct'] ?? 25 ) ) ),
					);
				}
				update_option( 'nadlan_preferred_partners', wp_json_encode( $clean, JSON_UNESCAPED_UNICODE ) );
				return array( 'ok' => true, 'count' => count( $clean ), 'partners' => $clean );
			},
		),
	) );
} );

/* -------------------------------------------------------------------------
 * B) Wire preferred-partners into the lead-routing layer
 *
 * When a user submits via /nadlan/v1/lead (the generic capture used by the
 * sticky bar, exit-intent modal, claim prompt, AI concierge handoff), and the
 * goal/topic mentions a profession we cover, route a COPY of the lead-email
 * to the best-matching preferred partner. This is opt-in per lead — controlled
 * by the post-meta the existing /lead endpoint already writes.
 * ------------------------------------------------------------------------- */
add_action( 'save_post_nadlan_lead', function ( $lead_id, $post ) {
	if ( wp_is_post_revision( $lead_id ) || wp_is_post_autosave( $lead_id ) ) { return; }
	if ( get_post_meta( $lead_id, 'preferred_routed', true ) ) { return; } // already routed
	if ( ! function_exists( 'nadlan_pp_list' ) || ! function_exists( 'nadlan_pp_pick' ) ) { return; }
	if ( ! nadlan_pp_list() ) { return; } // owner has no partners set yet — no-op

	$goal = trim( (string) get_post_meta( $lead_id, 'goal', true ) );
	$msg  = trim( (string) get_post_meta( $lead_id, 'message', true ) );
	$city = trim( (string) get_post_meta( $lead_id, 'city', true ) );
	$blob = $goal . ' ' . $msg;

	$profession_map = array(
		'kablan'     => array( 'קבלן', 'בנייה', 'שיפוץ' ),
		'shamai'     => array( 'שמאי', 'הערכת שווי' ),
		'bedek_bait' => array( 'בדק בית', 'בדיקת בית' ),
		'mashkanta'  => array( 'משכנתא', 'מימון', 'יועץ משכנתא' ),
		'architect'  => array( 'אדריכל', 'תכנון', 'פרוגרמה' ),
		'lawyer'     => array( 'עורך דין', 'עו"ד', 'עו״ד', 'משפט', 'נסח', 'טאבו', 'חוזה', 'הסכם' ),
		'mefakeach'  => array( 'מפקח', 'פיקוח' ),
		'metavech'   => array( 'מתווך', 'תיווך' ),
	);
	$prof = '';
	foreach ( $profession_map as $k => $keywords ) {
		foreach ( $keywords as $kw ) {
			if ( mb_stripos( $blob, $kw ) !== false ) { $prof = $k; break 2; }
		}
	}
	$pick = nadlan_pp_pick( $prof, $city );
	if ( ! $pick || empty( $pick['email'] ) ) { return; }

	// Build a partner-friendly email. Customer phone is sent verbatim so they can call.
	$name  = (string) get_post_meta( $lead_id, 'name', true );
	$phone = (string) get_post_meta( $lead_id, 'phone', true );
	$src   = (string) get_post_meta( $lead_id, 'utm_source', true );
	$pct   = (float) ( $pick['pct'] ?? 25 );

	$body  = "שלום " . ( $pick['name'] ?? '' ) . ",\n\n";
	$body .= "התקבל ליד חדש שמתאים לתחום ההתמחות שלך, דרך מערכת נדלן.\n\n";
	$body .= "לקוח: $name\nטלפון: $phone\n";
	if ( $goal ) { $body .= "נושא: $goal\n"; }
	if ( $msg )  { $body .= "פרטים: $msg\n"; }
	if ( $src )  { $body .= "מקור: $src\n"; }
	$body .= "\n— תנאי שיתוף הפעולה: עמלה של $pct% מהעסקה הסגורה, משולמת בתוך 14 יום מסגירה.\n";
	$body .= "— נא לחזור ללקוח תוך 24 שעות.\n\n";
	$body .= "מערכת נדלן · nad-lan.co.il";

	$ok = wp_mail( $pick['email'], '[נדלן] ליד חדש בתחום שלך — ' . $name, $body );

	update_post_meta( $lead_id, 'preferred_routed', $pick['email'] );
	update_post_meta( $lead_id, 'preferred_pct', $pct );
	update_post_meta( $lead_id, 'matched_profession', $prof );
}, 30, 2 );
