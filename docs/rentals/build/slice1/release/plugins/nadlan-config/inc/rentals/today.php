<?php
/**
 * nadlan-config - RENTALS v2, slice 1 (HAD-795): the endpoints the one-press jobs of the "Today" screen need.
 *
 * Only what rest.php does not already give:
 *  - POST /rm/today/repair        a repair together with its first photo, in ONE request (camera first, no form);
 *  - POST /rm/today/index-confirm the landlord's confirmation of an index (CPI) update, as an event in the apartment's journal
 *                                 (kind index_confirmed; never a ledger line: no money moves, the books count ledger rows only).
 * "Rent received in one press" needs no new route: POST /rm/pay already takes the lease, the amount and the date
 * in one call, and the screen sends the expected amount and today's date.
 *
 * Same rules as rest.php: the module switch, a logged-in account, the owner's data only, writers only (owner or
 * manager), nothing is written while the data key is missing, the WordPress REST nonce, one client_ref per user
 * action so a retry never doubles. Photos are stored by nlrm_doc_store (encrypted at rest like every upload).
 * Nothing here sends anything to a tenant.
 */

if ( ! defined( 'ABSPATH' ) ) { exit; }

add_action( 'rest_api_init', function () {
	if ( ! function_exists( 'nlrm_owner' ) || ! function_exists( 'nlrm_save' ) ) { return; }
	$ns = 'nadlan/v1';
	$owner_ok = function () {
		if ( ! nadlan_rm_on() || ! is_user_logged_in() ) { return false; }
		nlrm_maybe_install();
		return nlrm_owner() > 0;
	};
	/* nothing is written while the data key is missing (see nlrm_key_ok) */
	$writer_ok = function () use ( $owner_ok ) { return $owner_ok() && nlrm_can_write() && nlrm_key_ok(); };

	/* ---------- a repair with its first photo ---------- */
	register_rest_route( $ns, '/rm/today/repair', array(
		'methods' => 'POST', 'permission_callback' => $writer_ok,
		'callback' => function ( WP_REST_Request $r ) {
			$o   = nlrm_owner();
			$uid = (int) $r->get_param( 'unit_id' );
			if ( ! nlrm_owns( 'unit', $uid, $o ) ) { return nlrm_err( 'nlrm_forbidden', 403, 'לא נמצא.', 'Not found.' ); }
			/* idempotency, the same key family as /rm/save: a retry returns the repair already saved */
			$cref = preg_replace( '/[^A-Za-z0-9_\-]/', '', (string) $r->get_param( 'client_ref' ) );
			$ckey = $cref ? 'nlrm_cref_' . $o . '_' . substr( $cref, 0, 40 ) : '';
			if ( $ckey ) {
				$seen = get_transient( $ckey );
				if ( is_array( $seen ) && ! empty( $seen['id'] ) && 'ticket' === ( $seen['entity'] ?? '' ) ) {
					$prev = nlrm_get( 'ticket', (int) $seen['id'], $o );
					if ( $prev ) { return array( 'ticket' => $prev, 'doc' => isset( $seen['doc'] ) ? $seen['doc'] : null, 'again' => true ); }
				}
			}
			/* the photo is checked BEFORE the repair exists, so a bad file never leaves an empty repair behind */
			$files = $r->get_file_params();
			$file  = isset( $files['file'] ) ? $files['file'] : array();
			if ( empty( $file['tmp_name'] ) || ! is_uploaded_file( $file['tmp_name'] ) ) { return nlrm_err( 'nlrm_nofile', 400, 'לא התקבלה תמונה.', 'No photo received.' ); }
			if ( (int) $file['size'] > 15 * 1024 * 1024 ) { return nlrm_err( 'nlrm_big', 400, 'תמונה עד 15MB.', 'Photos up to 15 MB.' ); }
			$check = wp_check_filetype_and_ext( $file['tmp_name'], $file['name'] );
			if ( empty( $check['ext'] ) || ! in_array( strtolower( $check['ext'] ), array( 'jpg', 'jpeg', 'png', 'webp', 'heic' ), true ) ) {
				return nlrm_err( 'nlrm_type', 400, 'צריך לצלם או לבחור תמונה.', 'Please take or choose a photo.' );
			}
			$unit  = nlrm_get( 'unit', $uid, $o );
			$title = mb_substr( sanitize_text_field( (string) $r->get_param( 'title' ) ), 0, 160 );
			if ( '' === $title ) { $title = 'תקלה חדשה'; }
			$meta = array( 'via' => 'today-camera' );
			$aid  = sanitize_key( (string) $r->get_param( 'asset' ) );
			if ( $aid ) {
				foreach ( (array) ( ( (array) $unit['meta'] )['assets'] ?? array() ) as $a ) { if ( (string) ( $a['id'] ?? '' ) === $aid ) { $meta['asset'] = $aid; break; } }
			}
			$t = nlrm_save( 'ticket', array(
				'property_id' => (int) $unit['property_id'], 'unit_id' => $uid, 'title' => $title, 'category' => 'general',
				'urgency' => 'standard', 'status' => 'new', 'reporter' => 'owner', 'due_by' => nlrm_add_days( nlrm_today(), 30 ), 'meta' => $meta,
			), $o, 'u:' . get_current_user_id() );
			if ( is_wp_error( $t ) ) { return $t; }
			$doc = nlrm_doc_store( $o, $file, 'ticket', (int) $t['id'], 'photo', 'u:' . get_current_user_id() );
			if ( is_wp_error( $doc ) ) {
				nlrm_delete( 'ticket', (int) $t['id'], $o, 'u:' . get_current_user_id() ); /* soft delete: no repair without its photo */
				return $doc;
			}
			if ( $ckey ) { set_transient( $ckey, array( 'entity' => 'ticket', 'id' => (int) $t['id'], 'doc' => $doc ), 30 * MINUTE_IN_SECONDS ); }
			return array( 'ticket' => $t, 'doc' => $doc );
		},
	) );

	/* ---------- the confirmation of an index update ---------- */
	/* An event in the apartment's journal (the same table and helper as the repair and lease events), never a ledger line:
	   the money engine already applies the lease's linkage to the future charges, so nothing here moves money, and reports,
	   CSV and the books count ledger rows only. */
	register_rest_route( $ns, '/rm/today/index-confirm', array(
		'methods' => 'POST', 'permission_callback' => $writer_ok,
		'callback' => function ( WP_REST_Request $r ) {
			$o     = nlrm_owner();
			$lid   = (int) $r->get_param( 'lease_id' );
			$lease = nlrm_get( 'lease', $lid, $o );
			if ( ! $lease ) { return nlrm_err( 'nlrm_404', 404, 'החוזה לא נמצא.', 'Lease not found.' ); }
			$link = (array) ( $lease['linkage'] ?? array() );
			if ( 'cpi' !== ( $link['mode'] ?? '' ) ) { return nlrm_err( 'nlrm_nolink', 409, 'שכר הדירה בחוזה הזה אינו צמוד למדד.', 'This lease is not linked to the index.' ); }
			$base = (float) $r->get_param( 'base_index' );
			$appl = (float) $r->get_param( 'applied_index' );
			if ( $base <= 0 || $appl <= 0 || $base > 100000 || $appl > 100000 ) { return nlrm_err( 'nlrm_bad', 400, 'חסר מספר מדד.', 'An index number is missing.' ); }
			$ym = (string) $r->get_param( 'start_month' );
			if ( ! preg_match( '/^\d{4}-(0[1-9]|1[0-2])$/', $ym ) ) { return nlrm_err( 'nlrm_bad', 400, 'באיזה חודש מתחיל שכר הדירה החדש?', 'Which month does the new rent start?' ); }
			if ( ! empty( $lease['start_date'] ) && $ym < substr( (string) $lease['start_date'], 0, 7 ) ) { return nlrm_err( 'nlrm_bad', 400, 'החודש לפני תחילת החוזה.', 'That month is before the lease starts.' ); }
			if ( ! empty( $lease['end_date'] ) && $ym > substr( (string) $lease['end_date'], 0, 7 ) ) { return nlrm_err( 'nlrm_bad', 400, 'החודש אחרי סוף החוזה.', 'That month is after the lease ends.' ); }
			/* the amount is computed here by the contract's own rule (the formula of nlrm_period_amount); the screen's number must agree */
			$old = (int) round( (float) $lease['rent'] * 100 );
			$pct = max( 0, min( 100, (float) ( $link['pct'] ?? 100 ) ) ) / 100;
			$new = $old * ( 1 + $pct * ( $appl / $base - 1 ) );
			if ( ! isset( $link['floor'] ) || $link['floor'] ) { $new = max( $old, $new ); }
			$new = (int) round( $new );
			if ( abs( (float) $r->get_param( 'new_amount' ) * 100 - $new ) > 100 ) { return nlrm_err( 'nlrm_idx_mismatch', 409, 'הסכום לא מתאים לחישוב לפי החוזה. נסו שוב.', 'The amount does not match the contract calculation. Please try again.' ); }
			$cref = substr( preg_replace( '/[^A-Za-z0-9_\-]/', '', (string) $r->get_param( 'client_ref' ) ), 0, 40 );
			if ( '' === $cref ) { return nlrm_err( 'nlrm_bad', 400, 'חסר מזהה פעולה.', 'Missing action id.' ); }
			$info = array( 'lease_id' => $lid, 'start_month' => $ym, 'base_index' => $base, 'applied_index' => $appl, 'old_amount' => $old, 'new_amount' => $new );
			/* a retry of the same action returns the event already written (amounts in agorot) */
			foreach ( nlrm_events( $o, 'lease', $lid, 300 ) as $e ) {
				if ( 'index_confirmed' === $e['type'] && (string) ( ( (array) $e['meta'] )['client_ref'] ?? '' ) === $cref ) { return array( 'lease_id' => $lid, 'event' => $e, 'index' => $info, 'again' => true ); }
			}
			$id = nlrm_event( $o, 'u:' . get_current_user_id(), 'lease', $lid, 'index_confirmed', '', '', array_merge( $info, array( 'client_ref' => $cref ) ) );
			if ( ! $id ) { return nlrm_err( 'nlrm_db', 500, 'השמירה נכשלה, נסו שוב.', 'Saving failed, please try again.' ); }
			$ev = null;
			foreach ( nlrm_events( $o, 'lease', $lid, 20 ) as $e ) { if ( (int) $e['id'] === (int) $id ) { $ev = $e; break; } }
			return array( 'lease_id' => $lid, 'event' => $ev, 'index' => $info );
		},
	) );
} );
