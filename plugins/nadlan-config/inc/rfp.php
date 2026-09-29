<?php
/**
 * nadlan-config - RFP document (buy-flow phase 2, research spec 2026-07-05)
 *
 * The buy-flow posts a structured request; this module turns it into a real,
 * shareable, printable RFP document the buyer can open immediately and the
 * owner can forward to the developer and advisors.
 *
 *  - POST /nadlan/v1/rfp        create the document (called by buyflow.js right
 *                               after the lead is accepted); returns {url}
 *  - GET  /nadlan/v1/rfp/<token> the rendered document (unguessable token)
 *
 * HONESTY LAWS: unit facts are re-read SERVER-SIDE from the project post (the
 * client payload only points at project slug + unit id); every money-shaped
 * line is estimate-labeled; advisors listed are real directory entries matched
 * by profession; the status timeline claims only what actually happened.
 */

if ( ! defined( 'ABSPATH' ) ) { exit; }

if ( ! function_exists( 'nadlan_rfp_lang_table' ) ) {
	function nadlan_rfp_lang_table( $lang ) {
		$T = array(
			'he' => array( 'dir' => 'rtl', 'doc' => 'מסמך בקשה להצעה', 'for' => 'עבור', 'date' => 'תאריך', 'valid' => 'בתוקף 30 יום', 'unit' => 'הדירה המבוקשת', 'project' => 'פרויקט', 'developer' => 'יזם', 'floor' => 'קומה', 'rooms' => 'חדרים', 'sqm' => 'שטח (מ"ר)', 'dirn' => 'כיוון', 'config' => 'הבקשה', 'finish' => 'רמת גימור', 'finish_std' => 'מפרט היזם', 'finish_up' => 'משודרג', 'finish_prem' => 'פרימיום', 'extras' => 'שירותים שצורפו לבקשה', 'none' => 'ללא תוספות, חיבור ישיר ליזם', 'advisors' => 'אנשי מקצוע מוצעים מהמאגר', 'adv_none' => 'צוות נדלן יתאם יועץ מתאים מהמאגר', 'status' => 'סטטוס הבקשה', 'st1' => 'הבקשה התקבלה במערכת', 'st2' => 'תיאום מול היזם', 'st3' => 'הצעה מרוכזת לרוכש', 'disc' => 'כל הנתונים במסמך זה הם אומדן ולידיעה בלבד. המסמך אינו הצעת מחיר, אינו התחייבות ואינו מסמך מכר. התמחור הסופי נקבע בהצעת היזם לפי מפרט המכר וחוזה הרכישה.', 'ex_designer' => 'מעצב/ת פנים', 'ex_lawyer' => 'עו"ד מקרקעין', 'ex_mortgage' => 'יועץ משכנתא', 'ex_inspect' => 'בדק בית', 'ex_furniture' => 'התעניינות בריהוט', 'print' => 'הדפסה / שמירה כ-PDF', 'back' => 'חזרה לעמוד הפרויקט', 'example' => 'דירה לדוגמה', 'design' => 'העיצוב לדירה', 'plan' => 'תוכנית', 'plan_v' => 'דירת דוגמה להמחשה · גרסה', 'src' => 'מקור', 'src_designer-3d' => 'הסטודיו התלת־ממדי (מטרים, ממרכז הדירה)', 'src_studio-2d' => 'הסטודיו הדו־ממדי (ס״מ, מהפינה העליונה)', 'choices' => 'בחירות', 'items' => 'ריהוט', 'u_m' => 'מטרים', 'u_cm' => 'ס״מ', 'notes' => 'הערות ובקשות', 'checks' => 'בדיקות מיקום (להמחשה בלבד)', 'design_disc' => 'התוכנית בסטודיו היא דירת דוגמה להמחשה. המיקומים נמסרים כפי שהקונה הציב אותם, בלי המרה לתוכנית אחרת. זו אינה תוכנית מכר ואינה בדיקה הנדסית.' ),
			'en' => array( 'dir' => 'ltr', 'doc' => 'Request for Proposal', 'for' => 'For', 'date' => 'Date', 'valid' => 'Valid 30 days', 'unit' => 'Requested apartment', 'project' => 'Project', 'developer' => 'Developer', 'floor' => 'Floor', 'rooms' => 'Rooms', 'sqm' => 'Area (sqm)', 'dirn' => 'Orientation', 'config' => 'The request', 'finish' => 'Finish level', 'finish_std' => 'Developer spec', 'finish_up' => 'Upgraded', 'finish_prem' => 'Premium', 'extras' => 'Services added to the request', 'none' => 'No add-ons, direct connection to the developer', 'advisors' => 'Suggested professionals from the directory', 'adv_none' => 'The NadLan team will match a suitable advisor', 'status' => 'Request status', 'st1' => 'Request received', 'st2' => 'Coordination with the developer', 'st3' => 'Consolidated proposal to the buyer', 'disc' => 'All figures in this document are estimates for information only. This document is not a quote, not a commitment and not a sale document. Final pricing is set in the developer proposal per the sale specification and purchase contract.', 'ex_designer' => 'Interior designer', 'ex_lawyer' => 'Real estate lawyer', 'ex_mortgage' => 'Mortgage advisor', 'ex_inspect' => 'Inspection (bedek)', 'ex_furniture' => 'Furniture interest', 'print' => 'Print / save as PDF', 'back' => 'Back to the project page', 'example' => 'Example apartment', 'design' => 'The design for this apartment', 'plan' => 'Plan', 'plan_v' => 'Illustrative example apartment · revision', 'src' => 'Source', 'src_designer-3d' => '3D studio (metres, from the flat centre)', 'src_studio-2d' => '2D studio (cm, from the top corner)', 'choices' => 'Choices', 'items' => 'Furniture', 'u_m' => 'm', 'u_cm' => 'cm', 'notes' => 'Notes and requests', 'checks' => 'Placement checks (illustrative only)', 'design_disc' => 'The studio plan is an illustrative example apartment. Positions are as the buyer placed them, not converted to any other plan. This is not a sale plan and not an engineering check.' ),
		);
		if ( isset( $T[ $lang ] ) ) { return $T[ $lang ]; }
		// fr/ru/ar fall back to the English document (Gulf + international buyers
		// read English; a Hebrew document to an Arabic-page buyer closes no circle).
		return $T[ in_array( $lang, array( 'fr', 'ru', 'ar' ), true ) ? 'en' : 'he' ];
	}
}

if ( ! function_exists( 'nadlan_rfp_advisor_map' ) ) {
	function nadlan_rfp_advisor_map() {
		// filterable (2026-07-12): the urban-renewal flow adds its advisor kinds
		return apply_filters( 'nadlan_rfp_advisor_map', array(
			'designer' => array( 'interior_designer', 'architect' ),
			'lawyer'   => array( 'lawyer' ),
			'mortgage' => array( 'mashkanta' ),
			'inspect'  => array( 'bedek_bait', 'inspector' ),
		) );
	}
}

if ( ! function_exists( 'nadlan_rfp_match_advisors' ) ) {
	function nadlan_rfp_match_advisors( $extras ) {
		$map = nadlan_rfp_advisor_map();
		$out = array();
		foreach ( (array) $extras as $x ) {
			$x = sanitize_key( $x );
			if ( ! isset( $map[ $x ] ) ) { continue; }
			$q = new WP_Query( array(
				'post_type' => 'nadlan_professional', 'post_status' => 'publish',
				'posts_per_page' => 2, 'no_found_rows' => true, 'fields' => 'ids',
				// owner directive 2026-07-06: seeded profiles STAY matchable for the
				// demonstration phase (the directory badge marks them as demo data).
				// Re-add the reviews_verified exclusion before the marketing push.
				'meta_query' => array( array( 'key' => 'profession', 'value' => $map[ $x ], 'compare' => 'IN' ) ),
			) );
			$names = array();
			foreach ( $q->posts as $pid ) {
				$names[] = array(
					'name' => get_the_title( $pid ),
					'city' => (string) get_post_meta( $pid, 'city', true ),
					'url'  => get_permalink( $pid ),
				);
			}
			$out[ $x ] = $names;
		}
		return $out;
	}
}

/* ---------------------------------------------------------------------------
 * UnitDesignRequest (design system v102, 29.9.2026, HAD-346 Batch 2): one request per unit, with the buyer's whole design.
 * Codex reproduced three gaps in the callback below (handoff 29.9, RFP-01..03): the studio design reached the lead message
 * but not the document, an unknown non-empty unit was stored as null, and any lead id was linked without a check. Now:
 * the unit is resolved (inventory, else the stage's example units) or the request fails with nothing written; a design file
 * travels with its identity and is stored frozen in the document; a lead is linked only with the key its own creation
 * returned; and a repeated client_ref gets the same receipt, never a second document.
 * ------------------------------------------------------------------------- */
if ( ! function_exists( 'nadlan_rfp_unit_id' ) ) {
	/** a unit id as the stages and the inventory write it: letters, digits, '-' and '_', case kept (N-25-w is not n-25-w) */
	function nadlan_rfp_unit_id( $v ) {
		return substr( preg_replace( '/[^A-Za-z0-9_-]/', '', (string) $v ), 0, 96 );
	}
}

if ( ! function_exists( 'nadlan_rfp_lead_key' ) ) {
	/** the key /nadlan/v1/lead returns with a lead that names a project and a unit; only its holder can link a document to it */
	function nadlan_rfp_lead_key( $lead_id, $project, $unit ) {
		$msg = (int) $lead_id . '|' . sanitize_title( (string) $project ) . '|' . strtolower( nadlan_rfp_unit_id( $unit ) );
		return substr( hash_hmac( 'sha256', $msg, wp_salt( 'auth' ) . 'nadlan-rfp-lead' ), 0, 32 );
	}
}

if ( ! function_exists( 'nadlan_rfp_lead_key_for' ) ) {
	/** the key for a lead AS PERSISTED: issued only when the stored lead names exactly the requested project and unit
	 *  (a de-duplicated older lead of another unit gets no key for the new one) */
	function nadlan_rfp_lead_key_for( $lead_id, $project, $unit ) {
		$lead_id = (int) $lead_id;
		if ( $lead_id <= 0 || '' === (string) $project || '' === (string) $unit || 'nadlan_lead' !== get_post_type( $lead_id ) ) { return ''; }
		$lp = sanitize_title( (string) get_post_meta( $lead_id, 'project_slug', true ) );
		$lu = strtolower( nadlan_rfp_unit_id( (string) get_post_meta( $lead_id, 'unit', true ) ) );
		if ( $lp !== sanitize_title( (string) $project ) || $lu !== strtolower( nadlan_rfp_unit_id( $unit ) ) ) { return ''; }
		return nadlan_rfp_lead_key( $lead_id, $project, $unit );
	}
}

if ( ! function_exists( 'nadlan_rfp_lead_ok' ) ) {
	/** a lead may be linked when the key matches and the lead itself names the same project and unit */
	function nadlan_rfp_lead_ok( $lead_id, $key, $project, $unit ) {
		$lead_id = (int) $lead_id;
		$key     = (string) $key;
		if ( $lead_id <= 0 || '' === $key || ! hash_equals( nadlan_rfp_lead_key( $lead_id, $project, $unit ), $key ) ) { return false; }
		if ( 'nadlan_lead' !== get_post_type( $lead_id ) ) { return false; }
		$lp = (string) get_post_meta( $lead_id, 'project_slug', true );
		$lu = (string) get_post_meta( $lead_id, 'unit', true );
		return sanitize_title( $lp ) === sanitize_title( (string) $project ) && strtolower( nadlan_rfp_unit_id( $lu ) ) === strtolower( nadlan_rfp_unit_id( $unit ) );
	}
}

if ( ! function_exists( 'nadlan_rfp_clean_design' ) ) {
	/**
	 * The buyer's design file for one unit, cleaned and capped. The two studios keep their own layers: the 2D studio's plan
	 * in cm from the top-left corner with degrees, the 3D designer's space in metres from the flat's centre with radians;
	 * nothing is converted between them (no mapped transform exists). Geometry checks are kept apart and are lights only.
	 */
	function nadlan_rfp_clean_design( $d ) {
		if ( ! is_array( $d ) ) { return null; }
		$num = function ( $v, $lo, $hi ) { $v = is_numeric( $v ) ? (float) $v : 0.0; return round( max( $lo, min( $hi, $v ) ), 3 ); };
		// a rotation is periodic: brought into one turn, never clamped (the designer adds a quarter turn per press, so 12 presses
		// are 3π; a clamp at 7 turned the piece by 139°, Codex RFP-B2-DRAFT). Radians to (-π, π], degrees to [0, 360).
		$rad = function ( $v ) { $v = is_numeric( $v ) ? (float) $v : 0.0; if ( ! is_finite( $v ) ) { return 0.0; } $r = atan2( sin( $v ), cos( $v ) ); $r = round( $r <= -M_PI + 1e-9 ? M_PI : $r, 6 ); return $r > M_PI ? M_PI : $r; };
		$deg = function ( $v ) { $v = is_numeric( $v ) ? (float) $v : 0.0; if ( ! is_finite( $v ) ) { return 0.0; } $d = fmod( fmod( $v, 360.0 ) + 360.0, 360.0 ); return round( $d >= 360.0 ? 0.0 : $d, 3 ); };
		$txt = function ( $v, $n ) { return mb_substr( sanitize_textarea_field( (string) $v ), 0, $n ); };
		$out = array(
			'schema'            => 'nadlan-unit-design',
			'v'                 => 1,
			'project'           => sanitize_title( (string) ( $d['project'] ?? '' ) ),
			'unit_id'           => nadlan_rfp_unit_id( $d['unit_id'] ?? '' ),
			'geometry_revision' => substr( preg_replace( '/[^A-Za-z0-9._:-]/', '', (string) ( $d['geometry_revision'] ?? '' ) ), 0, 80 ),
			'source'            => in_array( ( $d['source'] ?? '' ), array( 'designer-3d', 'studio-2d' ), true ) ? $d['source'] : '',
			'layers'            => array(),
			'notes'             => array(),
			'choices'           => array(),
			'mood'              => sanitize_key( (string) ( $d['mood'] ?? '' ) ),
			'checks'            => null,
		);
		$layers = is_array( $d['layers'] ?? null ) ? $d['layers'] : array();
		if ( isset( $layers['plan2d']['items'] ) && is_array( $layers['plan2d']['items'] ) ) {
			$items = array();
			foreach ( array_slice( $layers['plan2d']['items'], 0, 60 ) as $it ) {
				if ( ! is_array( $it ) ) { continue; }
				$items[] = array( 'uid' => sanitize_key( (string) ( $it['uid'] ?? '' ) ), 'type' => sanitize_key( (string) ( $it['type'] ?? '' ) ), 'label' => $txt( $it['label'] ?? '', 60 ),
					'x' => $num( $it['x'] ?? 0, -5000, 5000 ), 'y' => $num( $it['y'] ?? 0, -5000, 5000 ), 'rot' => $deg( $it['rot'] ?? 0 ),
					'note' => $txt( $it['note'] ?? '', 200 ) );
			}
			$out['layers']['plan2d'] = array( 'units' => 'cm', 'origin' => 'top-left', 'rot' => 'deg', 'items' => $items );
		}
		if ( isset( $layers['space3d']['items'] ) && is_array( $layers['space3d']['items'] ) ) {
			$items = array();
			foreach ( array_slice( $layers['space3d']['items'], 0, 60 ) as $it ) {
				if ( ! is_array( $it ) ) { continue; }
				$items[] = array( 'id' => sanitize_key( (string) ( $it['id'] ?? '' ) ), 'kind' => sanitize_key( (string) ( $it['kind'] ?? '' ) ),
					'label' => $txt( $it['label'] ?? '', 60 ), 'room' => $txt( $it['room'] ?? '', 40 ),
					'x' => $num( $it['x'] ?? 0, -100, 100 ), 'z' => $num( $it['z'] ?? 0, -100, 100 ), 'ry' => $rad( $it['ry'] ?? 0 ) );
			}
			$out['layers']['space3d'] = array( 'units' => 'm', 'origin' => 'centre', 'rot' => 'rad', 'items' => $items );
		}
		foreach ( array_slice( is_array( $d['notes'] ?? null ) ? $d['notes'] : array(), 0, 80 ) as $n ) {
			if ( ! is_array( $n ) || '' === trim( (string) ( $n['text'] ?? '' ) ) ) { continue; }
			$tg = is_array( $n['target'] ?? null ) ? $n['target'] : array();
			$out['notes'][] = array(
				'target' => array( 'kind' => in_array( ( $tg['kind'] ?? '' ), array( 'element', 'item', 'general' ), true ) ? $tg['kind'] : 'general', 'id' => sanitize_key( (string) ( $tg['id'] ?? '' ) ) ),
				'label'  => $txt( $n['label'] ?? '', 80 ),
				'text'   => $txt( $n['text'], 400 ),
			);
		}
		foreach ( array_slice( is_array( $d['choices'] ?? null ) ? $d['choices'] : array(), 0, 20 ) as $c ) {
			if ( ! is_array( $c ) ) { continue; }
			$out['choices'][] = array( 'cat' => sanitize_key( (string) ( $c['cat'] ?? '' ) ), 'label' => $txt( $c['label'] ?? '', 60 ), 'pick' => $txt( $c['pick'] ?? '', 80 ) );
		}
		if ( is_array( $d['checks'] ?? null ) ) {
			$w = array();
			foreach ( array_slice( is_array( $d['checks']['warnings'] ?? null ) ? $d['checks']['warnings'] : array(), 0, 40 ) as $x ) {
				if ( is_array( $x ) ) { $w[] = array( 'code' => sanitize_key( (string) ( $x['code'] ?? '' ) ), 'item' => sanitize_key( (string) ( $x['item'] ?? '' ) ), 'message' => $txt( $x['message'] ?? '', 200 ) ); }
			}
			$out['checks'] = array( 'performed_checks' => array_values( array_map( 'sanitize_key', array_slice( (array) ( $d['checks']['performed_checks'] ?? array() ), 0, 20 ) ) ), 'warnings' => $w );
		}
		return $out;
	}
}

if ( ! function_exists( 'nadlan_rfp_receipt' ) ) {
	/** what the buyer's screen may claim: a server reference and the document, for this unit */
	function nadlan_rfp_receipt( $rid, $doc, $duplicate ) {
		$design = is_array( $doc['design'] ?? null ) ? $doc['design'] : array();
		return array(
			'ok'                => true,
			'url'               => rest_url( 'nadlan/v1/rfp/' . $doc['token'] ),
			'ref'               => strtoupper( substr( (string) $doc['token'], 0, 8 ) ),
			'unit'              => is_array( $doc['unit'] ?? null ) ? (string) $doc['unit']['id'] : '',
			'geometry_revision' => (string) ( $design['geometry_revision'] ?? '' ),
			'notes'             => count( (array) ( $design['notes'] ?? array() ) ),
			'items'             => count( (array) ( $design['layers']['plan2d']['items'] ?? array() ) ) + count( (array) ( $design['layers']['space3d']['items'] ?? array() ) ),
			'lead_linked'       => ! empty( $doc['lead_id'] ),
			'duplicate'         => (bool) $duplicate,
		);
	}
}

if ( ! function_exists( 'nadlan_rfp_create' ) ) {
	function nadlan_rfp_create( WP_REST_Request $req ) {
		$p = $req->get_json_params();
		if ( ! is_array( $p ) ) { return new WP_Error( 'bad_request', 'invalid payload', array( 'status' => 400 ) ); }
		$slug    = sanitize_title( (string) ( $p['project'] ?? '' ) );
		$unit_id = nadlan_rfp_unit_id( $p['unit'] ?? '' );
		$lang    = in_array( ( $p['lang'] ?? '' ), array( 'he', 'en', 'fr', 'ru', 'ar' ), true ) ? $p['lang'] : 'he'; // a missing lang was null
		$post    = $slug ? get_page_by_path( $slug, OBJECT, 'nadlan_project' ) : null;
		if ( ! $post ) { return new WP_Error( 'not_found', 'project not found', array( 'status' => 404 ) ); }
		/* Resolve the marker before reading inventory/title/permalink and before
		 * generating a token or row. The private journey intentionally has no RFP
		 * surface; this endpoint must be as opaque as a missing project. */
		if ( ( function_exists( 'nadlan_unit_journey_is_private_lab' )
				&& nadlan_unit_journey_is_private_lab( $post->ID ) )
			|| 'private-unit-journey-v2' === (string) get_post_meta( $post->ID, '_nadlan_private_unit_journey', true ) ) {
			return new WP_Error( 'not_found', 'project not found', array( 'status' => 404 ) );
		}
		/* Also makes a minimal privacy probe mutation-proof if the guard above is
		 * ever regressed: no unit pointer, no document creation. */
		if ( '' === $unit_id ) {
			return new WP_Error( 'bad_request', 'unit required', array( 'status' => 400 ) );
		}
		// server-side unit facts - the client only points, never dictates: the project's inventory, else the stage's example
		// apartments (inc/project-stage.php); an id in neither is refused with nothing written (RFP-02: it used to become null)
		$unit = null;
		$units = json_decode( (string) get_post_meta( $post->ID, 'project_3d_units', true ), true );
		foreach ( (array) $units as $u ) { if ( isset( $u['id'] ) && (string) $u['id'] === $unit_id ) { $unit = $u; break; } }
		if ( ! $unit && function_exists( 'nadlan_ps_unit_resolve' ) ) {
			$ex = nadlan_ps_unit_resolve( $slug, $unit_id );
			if ( $ex ) { $unit = array( 'id' => $ex['id'], 'label' => $ex['label'], 'floor' => $ex['floor'], 'rooms' => 0, 'sqm' => 0, 'dir' => '', 'example' => true ); }
		}
		if ( ! $unit ) {
			return new WP_Error( 'unit_unknown', 'unit not found in this project', array( 'status' => 422 ) );
		}
		$unit_id = (string) $unit['id'];
		// the design file, when one came: its identity must be this request's project and unit (409, nothing written, otherwise)
		$design = null;
		if ( isset( $p['design'] ) && null !== $p['design'] ) {
			$design = nadlan_rfp_clean_design( $p['design'] );
			if ( ! $design || $design['project'] !== $slug || strtolower( $design['unit_id'] ) !== strtolower( $unit_id ) ) {
				return new WP_Error( 'design_mismatch', 'the design belongs to another unit', array( 'status' => 409 ) );
			}
			$design['unit_id'] = $unit_id;
		}
		$finish = in_array( ( $p['finish'] ?? '' ), array( 'std', 'up', 'prem' ), true ) ? $p['finish'] : 'std';
		$extras = array_values( array_intersect( array_map( 'sanitize_key', (array) ( $p['extras'] ?? array() ) ), array_keys( nadlan_rfp_advisor_map() + array( 'furniture' => 1 ) ) ) );
		$first  = sanitize_text_field( (string) ( $p['name'] ?? '' ) );
		/* One client_ref, one document, one content (Codex RFP-B2-DRAFT, 29.9):
		 *  - the reference is written INTO the document row (post_name 'rfp-<ref>', in the same insert): no moment exists when the
		 *    document is there and its reference is not;
		 *  - the lock is claimed BEFORE the final look, so an attempt that finished while this one waited is found, not repeated;
		 *    a lock older than two minutes belongs to an attempt that died, and is taken over (then everything is looked at again);
		 *  - the reference is bound to its content (a fingerprint): the same reference with other content is refused (409), never
		 *    answered with the old receipt. New content needs a new reference. */
		$client_ref = preg_replace( '/[^a-z0-9]/', '', strtolower( (string) ( $p['client_ref'] ?? '' ) ) );
		$client_ref = strlen( $client_ref ) >= 12 ? substr( $client_ref, 0, 40 ) : '';
		$client_fp  = hash( 'sha256', (string) wp_json_encode( array( $slug, strtolower( $unit_id ), $design, $finish, $extras, $first ) ) );
		$lock       = 'nadlan_rfp_lock_' . $client_ref;
		$find       = function () use ( $client_ref ) { $hit = get_page_by_path( 'rfp-' . $client_ref, OBJECT, 'nadlan_rfp' ); return $hit ? (int) $hit->ID : 0; };
		$replay     = function ( $pid ) use ( $slug, $unit_id, $client_fp ) {
			$old = json_decode( (string) get_post_field( 'post_content', $pid ), true );
			if ( ! is_array( $old ) || ( $old['project']['slug'] ?? '' ) !== $slug || strtolower( (string) ( $old['unit']['id'] ?? '' ) ) !== strtolower( $unit_id ) ) {
				return new WP_Error( 'client_ref_taken', 'this request reference belongs to another unit', array( 'status' => 409 ) );
			}
			if ( ( $old['client_fp'] ?? '' ) !== $client_fp ) {
				return new WP_Error( 'client_ref_conflict', 'this request reference was used for other content', array( 'status' => 409 ) );
			}
			return rest_ensure_response( nadlan_rfp_receipt( $pid, $old, true ) );
		};
		if ( $client_ref ) {
			$hit = $find();
			if ( $hit ) { return $replay( $hit ); }
			if ( ! add_option( $lock, time(), '', 'no' ) ) {
				$since = (int) get_option( $lock, 0 );
				if ( $since && time() - $since < 120 ) {
					return new WP_Error( 'in_progress', 'the same request is being created', array( 'status' => 409 ) );
				}
				delete_option( $lock );
				if ( ! add_option( $lock, time(), '', 'no' ) ) {
					return new WP_Error( 'in_progress', 'the same request is being created', array( 'status' => 409 ) );
				}
			}
			$hit = $find(); // after the lock: a document made meanwhile is returned, never made twice
			if ( $hit ) { delete_option( $lock ); return $replay( $hit ); }
		}
		$token  = strtolower( wp_generate_password( 24, false, false ) );
		// RFP-03: a lead is linked only with the key that lead's own creation returned, for this project and unit
		$lead_id = nadlan_rfp_lead_ok( $p['lead_id'] ?? 0, $p['lead_key'] ?? '', $slug, $unit_id ) ? (int) $p['lead_id'] : 0;
		$doc = array(
			'token'      => $token,
			'created'    => gmdate( 'c' ),
			'lang'       => $lang,
			'project'    => array( 'id' => $post->ID, 'slug' => $slug, 'name' => get_the_title( $post->ID ), 'developer' => (string) get_post_meta( $post->ID, 'developer_name', true ), 'url' => get_permalink( $post->ID ) ),
			'unit'       => array( 'id' => $unit['id'], 'label' => (string) ( $unit['label'] ?? '' ), 'floor' => (int) ( $unit['floor'] ?? 0 ), 'rooms' => (float) ( $unit['rooms'] ?? 0 ), 'sqm' => (float) ( $unit['sqm'] ?? 0 ), 'dir' => (string) ( $unit['dir'] ?? '' ), 'example' => ! empty( $unit['example'] ) ),
			'finish'     => $finish,
			'extras'     => $extras,
			'advisors'   => nadlan_rfp_match_advisors( $extras ),
			'buyer'      => array( 'first' => $first ),
			'lead_id'    => $lead_id,
			'client_ref' => $client_ref,
			'client_fp'  => $client_ref ? $client_fp : '',
			'design'     => $design,
			'status'     => 1,
		);
		$rid = wp_insert_post( array(
			'post_type' => 'nadlan_rfp', 'post_status' => 'private',
			'post_title' => 'RFP ' . $slug . ' ' . $unit_id . ' ' . gmdate( 'Y-m-d H:i' ),
			'post_name' => $client_ref ? 'rfp-' . $client_ref : '',
			'post_content' => wp_slash( wp_json_encode( $doc, JSON_UNESCAPED_UNICODE ) ),
		), true );
		if ( $client_ref ) { delete_option( $lock ); } // the row already carries the reference: a later attempt finds it
		if ( is_wp_error( $rid ) ) { return $rid; }
		update_post_meta( $rid, 'rfp_token', $token );
		if ( $client_ref ) { update_post_meta( $rid, 'rfp_client_ref', $client_ref ); }
		if ( $lead_id ) { update_post_meta( $lead_id, 'rfp_id', $rid ); }
		return rest_ensure_response( nadlan_rfp_receipt( $rid, $doc, false ) );
	}
}

if ( ! function_exists( 'nadlan_rfp_render' ) ) {
	function nadlan_rfp_render( WP_REST_Request $req ) {
		$token = strtolower( preg_replace( '/[^a-z0-9]/i', '', (string) $req['token'] ) );
		$q = new WP_Query( array( 'post_type' => 'nadlan_rfp', 'post_status' => 'private', 'posts_per_page' => 1, 'no_found_rows' => true, 'fields' => 'ids', 'meta_key' => 'rfp_token', 'meta_value' => $token ) );
		if ( ! $q->posts ) { status_header( 404 ); echo 'Not found'; exit; }
		$doc = json_decode( get_post_field( 'post_content', $q->posts[0] ), true );
		if ( ! is_array( $doc ) ) { status_header( 410 ); echo 'Gone'; exit; }
		$project_id = isset( $doc['project']['id'] ) ? (int) $doc['project']['id'] : 0;
		if ( $project_id && (
			( function_exists( 'nadlan_unit_journey_is_private_lab' )
				&& nadlan_unit_journey_is_private_lab( $project_id ) )
			|| 'private-unit-journey-v2' === (string) get_post_meta( $project_id, '_nadlan_private_unit_journey', true )
		) ) {
			status_header( 404 );
			echo 'Not found';
			exit;
		}
		$T = nadlan_rfp_lang_table( $doc['lang'] );
		$u = $doc['unit']; $pr = $doc['project'];
		$exlbl = array( 'designer' => $T['ex_designer'], 'lawyer' => $T['ex_lawyer'], 'mortgage' => $T['ex_mortgage'], 'inspect' => $T['ex_inspect'], 'furniture' => $T['ex_furniture'] );
		$rid   = strtoupper( substr( $doc['token'], 0, 8 ) );
		header( 'Content-Type: text/html; charset=utf-8' );
		header( 'X-Robots-Tag: noindex' );
		?>
<!doctype html><html lang="<?php echo esc_attr( $doc['lang'] ); ?>" dir="<?php echo esc_attr( $T['dir'] ); ?>"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="robots" content="noindex">
<title><?php echo esc_html( $T['doc'] . ' ' . $rid ); ?></title>
<link href="https://fonts.googleapis.com/css2?family=Frank+Ruhl+Libre:wght@500;700&family=Heebo:wght@400;600;700&display=swap" rel="stylesheet">
<style>
body{margin:0;background:#EDE8DC;font-family:Heebo,system-ui,sans-serif;color:#1B1A17;padding:26px 14px}
.doc{max-width:760px;margin:0 auto;background:#FAF7F1;border:1px solid #E2DCD0;border-radius:16px;padding:34px 38px;box-shadow:0 10px 40px rgba(27,26,23,.12)}
h1{font-family:"Frank Ruhl Libre",serif;font-size:1.7rem;margin:0}
.mast{display:flex;justify-content:space-between;align-items:flex-start;gap:14px;border-bottom:2px solid #9C7A3C;padding-bottom:16px}
.mast .meta{text-align:end;font-size:12.5px;color:#6D665C;line-height:1.7}
.brand{font-family:"Frank Ruhl Libre",serif;font-weight:700;color:#9C7A3C;letter-spacing:.4px}
h2{font-family:"Frank Ruhl Libre",serif;font-size:1.05rem;margin:26px 0 10px;color:#1B1A17}
h2::after{content:"";display:block;width:44px;height:2px;background:#9C7A3C;margin-top:5px}
table{width:100%;border-collapse:collapse;font-size:14px}
td{padding:8px 10px;border-bottom:1px solid #EFE9DD}
td:first-child{color:#6D665C;width:38%}
.pill{display:inline-block;border:1px solid #9C7A3C;color:#7c5f2c;border-radius:999px;padding:4px 12px;font-size:12.5px;font-weight:600;margin:0 0 6px 6px;background:#F7F1E3}
.adv{border:1px solid #E2DCD0;border-radius:10px;background:#fff;padding:10px 14px;margin:7px 0;font-size:13.5px}
.adv small{color:#6D665C}
.tl{list-style:none;padding:0;margin:8px 0 0}
.tl li{display:flex;align-items:center;gap:10px;padding:7px 0;font-size:13.5px;color:#A79E8D}
.tl li .d{width:18px;height:18px;border-radius:50%;border:2px solid #D8CFBB;flex-shrink:0}
.tl li.on{color:#1B1A17;font-weight:600}
.tl li.on .d{background:#517048;border-color:#517048}
.disc{margin-top:26px;border-top:1px solid #E2DCD0;padding-top:14px;font-size:11.5px;color:#6D665C;line-height:1.65}
.bar{display:flex;gap:10px;justify-content:center;margin:18px auto 0;max-width:760px}
.bar a,.bar button{font:600 13.5px Heebo,sans-serif;border-radius:10px;padding:11px 18px;cursor:pointer;text-decoration:none;border:1px solid #E2DCD0;background:#fff;color:#1B1A17}
@media print{body{background:#fff;padding:0}.doc{border:0;box-shadow:none}.bar{display:none}}
</style></head><body>
<div class="doc">
	<div class="mast">
		<div><div class="brand">NadLan · nad-lan.co.il</div><h1><?php echo esc_html( $T['doc'] ); ?></h1>
		<?php if ( ! empty( $doc['buyer']['first'] ) ) : ?><div style="margin-top:5px;font-size:13.5px;color:#6D665C"><?php echo esc_html( $T['for'] . ': ' . $doc['buyer']['first'] ); ?></div><?php endif; ?></div>
		<div class="meta">ID <?php echo esc_html( $rid ); ?><br><?php echo esc_html( $T['date'] . ': ' . gmdate( 'd.m.Y', strtotime( $doc['created'] ) ) ); ?><br><?php echo esc_html( $T['valid'] ); ?></div>
	</div>
	<h2><?php echo esc_html( $T['unit'] ); ?></h2>
	<table>
		<tr><td><?php echo esc_html( $T['project'] ); ?></td><td><a href="<?php echo esc_url( $pr['url'] ); ?>" style="color:#1B1A17;font-weight:600"><?php echo esc_html( $pr['name'] ); ?></a></td></tr>
		<?php if ( $pr['developer'] ) : ?><tr><td><?php echo esc_html( $T['developer'] ); ?></td><td><?php echo esc_html( $pr['developer'] ); ?></td></tr><?php endif; ?>
		<?php if ( $u ) : ?>
		<tr><td><?php echo esc_html( $T['unit'] ); ?></td><td><bdi dir="ltr"><?php echo esc_html( $u['label'] ?: $u['id'] ); ?></bdi><?php echo ! empty( $u['example'] ) ? esc_html( ' · ' . $T['example'] ) : ''; ?></td></tr>
		<tr><td><?php echo esc_html( $T['floor'] ); ?></td><td><?php echo esc_html( $u['floor'] ); ?></td></tr>
		<?php if ( $u['rooms'] ) : ?><tr><td><?php echo esc_html( $T['rooms'] ); ?></td><td><?php echo esc_html( $u['rooms'] ); ?></td></tr><?php endif; ?>
		<?php if ( $u['sqm'] ) : ?><tr><td><?php echo esc_html( $T['sqm'] ); ?></td><td><?php echo esc_html( $u['sqm'] ); ?></td></tr><?php endif; ?>
		<?php if ( $u['dir'] ) : ?><tr><td><?php echo esc_html( $T['dirn'] ); ?></td><td><?php echo esc_html( $u['dir'] ); ?></td></tr><?php endif; ?>
		<?php endif; ?>
	</table>
	<h2><?php echo esc_html( $T['config'] ); ?></h2>
	<table><tr><td><?php echo esc_html( $T['finish'] ); ?></td><td><?php echo esc_html( $T[ 'finish_' . $doc['finish'] ] ); ?></td></tr></table>
	<div style="margin-top:12px">
	<?php if ( $doc['extras'] ) : foreach ( $doc['extras'] as $x ) : ?><span class="pill"><?php echo esc_html( $exlbl[ $x ] ?? $x ); ?></span><?php endforeach; else : ?>
		<span style="font-size:13px;color:#6D665C"><?php echo esc_html( $T['none'] ); ?></span>
	<?php endif; ?>
	</div>
	<?php $dz = is_array( $doc['design'] ?? null ) ? $doc['design'] : null; if ( $dz ) : /* UnitDesignRequest v102: the buyer's whole design, frozen */ ?>
	<h2><?php echo esc_html( $T['design'] ); ?></h2>
	<table>
		<?php if ( $dz['geometry_revision'] ) : ?><tr><td><?php echo esc_html( $T['plan'] ); ?></td><td><?php echo esc_html( $T['plan_v'] ); ?> <bdi dir="ltr"><?php echo esc_html( $dz['geometry_revision'] ); ?></bdi></td></tr><?php endif; ?>
		<?php if ( $dz['source'] ) : ?><tr><td><?php echo esc_html( $T['src'] ); ?></td><td><?php echo esc_html( $T[ 'src_' . $dz['source'] ] ?? $dz['source'] ); ?></td></tr><?php endif; ?>
		<?php if ( $dz['choices'] ) : ?><tr><td><?php echo esc_html( $T['choices'] ); ?></td><td><?php echo esc_html( implode( ' · ', array_map( function ( $c ) { return $c['label'] . ': ' . $c['pick']; }, $dz['choices'] ) ) ); ?></td></tr><?php endif; ?>
		<?php foreach ( array( 'space3d', 'plan2d' ) as $lk ) : if ( empty( $dz['layers'][ $lk ]['items'] ) ) { continue; } $ly = $dz['layers'][ $lk ]; ?>
		<tr><td><?php echo esc_html( $T['items'] . ' (' . ( $T[ 'u_' . $ly['units'] ] ?? $ly['units'] ) . ')' ); ?></td><td><?php foreach ( $ly['items'] as $it ) {
			if ( 'space3d' === $lk ) { echo esc_html( ( $it['label'] ?: $it['kind'] ) . ( $it['room'] ? ' · ' . $it['room'] : '' ) . ' · ' ) . '<bdi dir="ltr">' . esc_html( 'x ' . $it['x'] . ', z ' . $it['z'] . ' · ' . round( rad2deg( (float) $it['ry'] ) ) . '°' ) . '</bdi>'; }
			else { echo esc_html( ( $it['label'] ?: $it['type'] ) . ' · ' ) . '<bdi dir="ltr">' . esc_html( 'x ' . $it['x'] . ', y ' . $it['y'] . ' · ' . $it['rot'] . '°' ) . '</bdi>' . ( $it['note'] ? esc_html( ' · ' . $it['note'] ) : '' ); }
			echo '<br>'; } ?></td></tr>
		<?php endforeach; ?>
	</table>
	<?php if ( $dz['notes'] ) : ?><h2><?php echo esc_html( $T['notes'] . ' (' . count( $dz['notes'] ) . ')' ); ?></h2>
		<?php foreach ( $dz['notes'] as $n ) : ?><div class="adv"><?php if ( $n['label'] ) : ?><b><?php echo esc_html( $n['label'] ); ?></b> · <?php endif; ?><?php echo esc_html( $n['text'] ); ?></div><?php endforeach; ?>
	<?php endif; ?>
	<?php if ( ! empty( $dz['checks']['warnings'] ) ) : ?><h2><?php echo esc_html( $T['checks'] ); ?></h2>
		<?php foreach ( $dz['checks']['warnings'] as $w ) : ?><div class="adv"><small><?php echo esc_html( $w['message'] ?: $w['code'] ); ?></small></div><?php endforeach; ?>
	<?php endif; ?>
	<p class="disc" style="margin-top:12px"><?php echo esc_html( $T['design_disc'] ); ?></p>
	<?php endif; ?>
	<?php $has_adv = array_filter( (array) $doc['advisors'] ); if ( $doc['extras'] && array_intersect( $doc['extras'], array_keys( nadlan_rfp_advisor_map() ) ) ) : ?>
	<h2><?php echo esc_html( $T['advisors'] ); ?></h2>
	<?php if ( $has_adv ) : foreach ( $doc['advisors'] as $cat => $rows ) : foreach ( $rows as $a ) : ?>
		<div class="adv"><b><?php echo esc_html( $a['name'] ); ?></b> · <?php echo esc_html( $exlbl[ $cat ] ?? $cat ); ?><?php if ( $a['city'] ) : ?> <small>· <?php echo esc_html( $a['city'] ); ?></small><?php endif; ?></div>
	<?php endforeach; endforeach; else : ?>
		<div class="adv"><?php echo esc_html( $T['adv_none'] ); ?></div>
	<?php endif; endif; ?>
	<h2><?php echo esc_html( $T['status'] ); ?></h2>
	<ol class="tl">
		<li class="on"><span class="d"></span><?php echo esc_html( $T['st1'] ); ?></li>
		<li<?php echo (int) $doc['status'] >= 2 ? ' class="on"' : ''; ?>><span class="d"></span><?php echo esc_html( $T['st2'] ); ?></li>
		<li<?php echo (int) $doc['status'] >= 3 ? ' class="on"' : ''; ?>><span class="d"></span><?php echo esc_html( $T['st3'] ); ?></li>
	</ol>
	<p class="disc"><?php echo esc_html( $T['disc'] ); ?></p>
</div>
<?php /* v102: back to the project page with the same unit open (?unit=, which the stage and the engine both restore) */ $back = ( $u && ! empty( $u['id'] ) ) ? add_query_arg( 'unit', rawurlencode( (string) $u['id'] ), $pr['url'] ) : $pr['url']; ?>
<div class="bar"><button onclick="window.print()"><?php echo esc_html( $T['print'] ); ?></button><a href="<?php echo esc_url( $back ); ?>"><?php echo esc_html( $T['back'] ); ?></a></div>
</body></html>
		<?php
		exit;
	}
}

add_action( 'init', function () {
	register_post_type( 'nadlan_rfp', array(
		'label' => 'RFP documents', 'public' => false, 'show_ui' => true, 'show_in_menu' => 'edit.php?post_type=nadlan_project',
		'supports' => array( 'title' ), 'capability_type' => 'post', 'map_meta_cap' => true,
	) );
} );

add_action( 'rest_api_init', function () {
	register_rest_route( 'nadlan/v1', '/rfp', array(
		'methods' => 'POST', 'permission_callback' => '__return_true', 'callback' => 'nadlan_rfp_create',
	) );
	register_rest_route( 'nadlan/v1', '/rfp/(?P<token>[a-zA-Z0-9]{16,32})', array(
		'methods' => 'GET', 'permission_callback' => '__return_true', 'callback' => 'nadlan_rfp_render',
	) );
} );
