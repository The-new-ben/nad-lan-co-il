<?php
/**
 * nadlan-config - RENTALS v2: what a link holder sees and may do (HAD-383).
 *
 * tenant : his lease, what he owes and paid, how to pay, his repair
 *          requests, the documents the landlord shared, report a payment,
 *          open a repair request with a photo, write to the landlord, sign.
 * owner  : the landlord's own quick link (from his WhatsApp): today's list,
 *          mark rent paid, add an expense, move a repair along. No exports,
 *          no deletions, no team settings.
 * apply  : a prospect applies for a vacant apartment (the §11 notice is
 *          shown at the form and its version is stored with the record).
 * vendor : a professional sees one repair and updates it.
 * sign   : the lease text and the signature pad.
 */

if ( ! defined( 'ABSPATH' ) ) { exit; }

if ( ! function_exists( 'nlrm_landlord_card' ) ) {
	function nlrm_landlord_card( $owner ) {
		$u = get_userdata( $owner );
		$pay = (array) get_user_meta( $owner, 'nlrm_pay', true );
		return array(
			'name'  => (string) ( get_user_meta( $owner, 'nlrm_display', true ) ?: ( $u ? $u->display_name : '' ) ),
			'phone' => nlrm_phone( (string) get_user_meta( $owner, 'nlrm_phone', true ) ),
			'pay'   => array(
				'bank' => mb_substr( (string) ( $pay['bank'] ?? '' ), 0, 300 ),
				'bit'  => nlrm_phone( (string) ( $pay['bit'] ?? '' ) ),
				'link' => esc_url_raw( (string) ( $pay['link'] ?? '' ) ),
				'note' => mb_substr( (string) ( $pay['note'] ?? '' ), 0, 300 ),
			),
		);
	}
}

if ( ! function_exists( 'nlrm_lease_balance' ) ) {
	/* what the tenant sees: the balance over the WHOLE lease (never the last
	   rows only), and the last 60 lines of it with each charge's state */
	function nlrm_lease_balance( $owner, $lease_id ) {
		global $wpdb;
		$states = array();
		$m = nlrm_money( $owner, null, array( (int) $lease_id ), $states );
		$sum = $m[ (int) $lease_id ] ?? array( 'balance' => 0, 'deposit_held' => 0 );
		$rows = $wpdb->get_results( $wpdb->prepare( 'SELECT * FROM ' . nlrm_t( 'ledger' ) . " WHERE owner_id = %d AND lease_id = %d AND deleted_at IS NULL AND status <> 'void' ORDER BY COALESCE(due_date, paid_date) DESC, id DESC LIMIT 60", $owner, $lease_id ), ARRAY_A );
		$out = array_map( function ( $o ) { unset( $o['auto'] ); return $o; }, nlrm_ledger_rows( $rows, $states ) );
		return array( 'rows' => $out, 'balance' => (int) $sum['balance'], 'deposit_held' => (int) $sum['deposit_held'] );
	}
}

if ( ! function_exists( 'nlrm_portal_payload' ) ) {
	function nlrm_portal_payload( $link ) {
		$o = $link['owner_id'];
		$base = array( 'purpose' => $link['purpose'], 'landlord' => nlrm_landlord_card( $o ), 'expires_at' => substr( $link['expires_at'], 0, 10 ) );
		if ( in_array( $link['purpose'], array( 'tenant', 'sign' ), true ) ) {
			$lease = nlrm_get( 'lease', $link['scope_id'], $o );
			if ( ! $lease || 'cancelled' === $lease['status'] ) { return nlrm_err( 'nlrm_link', 410, 'החוזה אינו פעיל.', 'This lease is not active.' ); }
			$unit = nlrm_get( 'unit', $lease['unit_id'], $o );
			$prop = $unit ? nlrm_get( 'property', $unit['property_id'], $o ) : null;
			$who  = $link['contact_id'] ? nlrm_get( 'contact', $link['contact_id'], $o ) : null;
			$terms = (array) $lease['terms'];
			$shared = array_map( 'intval', (array) ( $terms['shared_docs'] ?? array() ) );
			$docs = array_values( array_filter( nlrm_docs_meta( $o ), function ( $d ) use ( $shared ) { return in_array( (int) $d['id'], $shared, true ); } ) );
			$tickets = array_values( array_filter( nlrm_get_all( 'ticket', $o ), function ( $t ) use ( $unit ) { return $unit && (int) $t['unit_id'] === (int) $unit['id']; } ) );
			$tickets = array_map( function ( $t ) { unset( $t['vendor_id'], $t['cost'] ); return $t; }, $tickets );
			$bal = nlrm_lease_balance( $o, $lease['id'] );
			return $base + array(
				'tenant'   => $who ? array( 'name' => $who['name'], 'lang' => $who['lang'] ) : null,
				'property' => $prop ? array( 'address' => $prop['address'], 'city' => $prop['city'], 'floors' => $prop['floors'] ) : null,
				'unit'     => $unit ? array( 'label' => $unit['label'], 'floor' => $unit['floor'], 'rooms' => $unit['rooms'], 'sqm' => $unit['sqm'] ) : null,
				'lease'    => array( 'id' => $lease['id'], 'status' => $lease['status'], 'start_date' => $lease['start_date'], 'end_date' => $lease['end_date'], 'option_until' => $lease['option_until'], 'rent' => $lease['rent'], 'pay_day' => $lease['pay_day'], 'linkage' => $lease['linkage'], 'securities' => $lease['securities'], 'signing' => $lease['signing'] ?? new stdClass(), 'doc' => 'sign' === $link['purpose'] ? nlrm_lease_text( $o, $lease, ( $who['lang'] ?? 'he' ) ) : null ),
				'ledger'   => $bal['rows'],
				'balance'  => $bal['balance'],
				'deposit_held' => $bal['deposit_held'],
				'tickets'  => $tickets,
				'docs'     => $docs,
			);
		}
		if ( 'owner' === $link['purpose'] ) {
			$b = nlrm_bootstrap( $o );
			unset( $b['events'], $b['docs'] );
			foreach ( $b['contacts'] as &$c ) { unset( $c['idno'], $c['notes'] ); }
			return $base + $b;
		}
		if ( 'apply' === $link['purpose'] ) {
			$unit = nlrm_get( 'unit', $link['scope_id'], $o );
			$prop = $unit ? nlrm_get( 'property', $unit['property_id'], $o ) : null;
			$m = $unit ? (array) $unit['meta'] : array();
			return $base + array(
				'property' => $prop ? array( 'address' => $prop['address'], 'city' => $prop['city'] ) : null,
				'unit' => $unit ? array( 'label' => $unit['label'], 'floor' => $unit['floor'], 'rooms' => $unit['rooms'], 'sqm' => $unit['sqm'], 'asking_rent' => (int) ( $m['asking_rent'] ?? 0 ), 'available_from' => (string) ( $m['available_from'] ?? '' ) ) : null,
				'privacy_version' => NLRM_PRIVACY_VERSION,
			);
		}
		if ( 'vendor' === $link['purpose'] ) {
			$t = nlrm_get( 'ticket', $link['scope_id'], $o );
			if ( ! $t ) { return nlrm_err( 'nlrm_link', 410, 'הקריאה נסגרה.', 'This request was closed.' ); }
			$unit = nlrm_get( 'unit', $t['unit_id'], $o );
			$prop = $unit ? nlrm_get( 'property', $unit['property_id'], $o ) : ( $t['property_id'] ? nlrm_get( 'property', $t['property_id'], $o ) : null );
			$tm = (array) $t['meta'];
			$tenant = null;
			if ( ! empty( $tm['share_tenant'] ) && $unit ) {
				foreach ( nlrm_get_all( 'lease', $o, $GLOBALS['wpdb']->prepare( " AND status = 'active' AND unit_id = %d", $unit['id'] ) ) as $l ) {
					$tid = (int) ( ( (array) $l['parties'] )['tenants'][0] ?? 0 );
					if ( $tid ) { $c = nlrm_get( 'contact', $tid, $o ); if ( $c ) { $tenant = array( 'name' => $c['name'], 'phone' => $c['phone'] ); } }
				}
			}
			return $base + array(
				'ticket' => array( 'id' => $t['id'], 'title' => $t['title'], 'body' => $t['body'], 'category' => $t['category'], 'urgency' => $t['urgency'], 'status' => $t['status'], 'due_by' => $t['due_by'], 'opened_at' => $t['opened_at'] ),
				'property' => $prop ? array( 'address' => $prop['address'], 'city' => $prop['city'] ) : null,
				'unit' => $unit ? array( 'label' => $unit['label'], 'floor' => $unit['floor'] ) : null,
				'tenant' => $tenant,
			);
		}
		return nlrm_err( 'nlrm_link', 410, 'הקישור אינו בתוקף.', 'This link is no longer valid.' );
	}
}

if ( ! function_exists( 'nlrm_portal_act' ) ) {
	function nlrm_portal_act( $link, WP_REST_Request $r ) {
		$o = $link['owner_id'];
		$actor = 'link:' . $link['id'];
		$act = sanitize_key( (string) $r->get_param( 'act' ) );
		$d = (array) $r->get_param( 'data' );

		if ( 'tenant' === $link['purpose'] ) {
			$lease = nlrm_get( 'lease', $link['scope_id'], $o );
			if ( ! $lease ) { return nlrm_err( 'nlrm_link', 410, 'החוזה אינו פעיל.', 'This lease is not active.' ); }
			$unit = nlrm_get( 'unit', $lease['unit_id'], $o );
			if ( 'ticket' === $act ) {
				$title = mb_substr( sanitize_text_field( (string) ( $d['title'] ?? '' ) ), 0, 160 );
				if ( '' === $title ) { return nlrm_err( 'nlrm_bad', 400, 'כתבו במשפט אחד מה התקלה.', 'Describe the problem in one sentence.' ); }
				$tri = nlrm_triage( $title . ' ' . (string) ( $d['body'] ?? '' ) );
				$urg = in_array( $d['urgency'] ?? '', array( 'urgent', 'standard' ), true ) ? $d['urgency'] : $tri['urgency'];
				$days = 'urgent' === $urg ? 3 : 30;
				$t = nlrm_save( 'ticket', array(
					'property_id' => $unit ? $unit['property_id'] : 0, 'unit_id' => $lease['unit_id'], 'title' => $title,
					'body' => (string) ( $d['body'] ?? '' ), 'category' => $tri['category'], 'urgency' => $urg, 'status' => 'new',
					'reporter' => 'tenant', 'due_by' => nlrm_add_days( nlrm_today(), $days ),
					'meta' => array( 'triage' => $tri, 'via' => 'portal' ),
				), $o, $actor );
				if ( ! is_wp_error( $t ) ) { nlrm_notify( $o, 'urgent' === $urg ? 'ticket_urgent' : 'ticket', array( 'where' => nlrm_notify_where( $o, $lease['unit_id'] ), 'title' => $title ) ); }
				return is_wp_error( $t ) ? $t : array( 'ticket' => $t );
			}
			if ( 'paid' === $act ) {
				$amount = (float) ( $d['amount'] ?? 0 );
				if ( $amount <= 0 ) { return nlrm_err( 'nlrm_bad', 400, 'מה הסכום ששולם?', 'How much was paid?' ); }
				$date = nlrm_date( $d['date'] ?? '' ) ?: nlrm_today();
				/* one tap = one report: the app's client_ref, else the report's own fingerprint */
				$cref = nlrm_cref( $r->get_param( 'client_ref' ), 'l' . $link['id'] ) ?: 'tp:' . $lease['id'] . ':' . substr( hash( 'sha256', round( $amount * 100 ) . '|' . $date . '|' . ( $d['method'] ?? '' ) . '|' . ( $d['ref'] ?? '' ) ), 0, 24 );
				$p = nlrm_pay( $o, array(
					'lease_id' => $lease['id'], 'amount' => $amount, 'paid_date' => $date, 'method' => (string) ( $d['method'] ?? 'transfer' ),
					'ref' => (string) ( $d['ref'] ?? '' ), 'status' => 'pending', 'note' => 'דווח על ידי השוכר · reported by the tenant',
				), $cref, $actor );
				if ( ! is_wp_error( $p ) ) { nlrm_notify( $o, 'paid', array( 'id' => (int) $p['id'], 'where' => nlrm_notify_where( $o, $lease['unit_id'] ), 'amount' => number_format( $amount ) . ' ₪', 'date' => $date ) ); }
				return is_wp_error( $p ) ? $p : array( 'payment' => $p );
			}
			if ( 'message' === $act ) {
				$body = sanitize_textarea_field( (string) ( $d['body'] ?? '' ) );
				if ( '' === trim( $body ) ) { return nlrm_err( 'nlrm_bad', 400, 'ההודעה ריקה.', 'The message is empty.' ); }
				nlrm_event( $o, $actor, 'lease', $lease['id'], 'msg_in', 'portal', $body, array() );
				nlrm_notify( $o, 'message', array( 'where' => nlrm_notify_where( $o, $lease['unit_id'] ), 'text' => mb_substr( $body, 0, 300 ) ) );
				return array( 'sent' => true );
			}
		}

		if ( in_array( $link['purpose'], array( 'tenant', 'sign' ), true ) && 'sign' === $act ) {
			return nlrm_sign( $link, $d );
		}

		if ( 'owner' === $link['purpose'] ) {
			if ( 'mark_paid' === $act ) {
				$c = nlrm_get( 'ledger', (int) ( $d['charge_id'] ?? 0 ), $o );
				if ( ! $c || 'charge' !== $c['kind'] || ! $c['lease_id'] ) { return nlrm_err( 'nlrm_404', 404, 'החיוב לא נמצא.', 'Charge not found.' ); }
				$p = nlrm_pay( $o, array(
					'lease_id' => $c['lease_id'], 'category' => $c['category'], 'amount' => isset( $d['amount'] ) ? (float) $d['amount'] : $c['amount'] / 100,
					'paid_date' => nlrm_date( $d['date'] ?? '' ) ?: nlrm_today(), 'method' => (string) ( $d['method'] ?? 'transfer' ),
					'ref' => (string) ( $d['ref'] ?? '' ), 'applies_to' => $c['id'],
				), nlrm_cref( $r->get_param( 'client_ref' ), 'q' . $link['id'] ) ?: 'qp:' . $c['id'], $actor );
				return is_wp_error( $p ) ? $p : array( 'payment' => $p );
			}
			if ( 'confirm' === $act ) {
				$p = nlrm_ledger_act( $o, (int) ( $d['id'] ?? 0 ), 'confirm', array(), $actor );
				return is_wp_error( $p ) ? $p : array( 'payment' => $p );
			}
			if ( 'expense' === $act ) {
				$e = nlrm_book( $o, array(
					'property_id' => (int) ( $d['property_id'] ?? 0 ), 'unit_id' => (int) ( $d['unit_id'] ?? 0 ), 'kind' => 'expense',
					'category' => (string) ( $d['category'] ?? 'other' ), 'amount' => (int) round( (float) ( $d['amount'] ?? 0 ) * 100 ),
					'paid_date' => nlrm_date( $d['date'] ?? '' ) ?: nlrm_today(), 'note' => (string) ( $d['note'] ?? '' ),
				), nlrm_cref( $r->get_param( 'client_ref' ), 'q' . $link['id'] ), $actor );
				return is_wp_error( $e ) ? $e : array( 'expense' => $e );
			}
			if ( 'ticket_status' === $act ) {
				$t = nlrm_save( 'ticket', array( 'id' => (int) ( $d['id'] ?? 0 ), 'status' => (string) ( $d['status'] ?? 'progress' ) ), $o, $actor );
				return is_wp_error( $t ) ? $t : array( 'ticket' => $t );
			}
		}

		if ( 'apply' === $link['purpose'] && 'apply' === $act ) {
			$name = mb_substr( sanitize_text_field( (string) ( $d['name'] ?? '' ) ), 0, 120 );
			$phone = nlrm_phone( (string) ( $d['phone'] ?? '' ) );
			if ( '' === $name || strlen( $phone ) < 9 || empty( $d['privacy_ok'] ) ) {
				return nlrm_err( 'nlrm_bad', 400, 'נדרשים שם, טלפון ואישור שקראתם את הודעת הפרטיות.', 'Name, phone and confirming the privacy notice are required.' );
			}
			$c = nlrm_save( 'contact', array(
				'kind' => 'prospect', 'stage' => 'applied', 'name' => $name, 'phone' => $phone, 'email' => (string) ( $d['email'] ?? '' ),
				'lang' => (string) ( $d['lang'] ?? 'he' ), 'notes' => (string) ( $d['notes'] ?? '' ),
				'meta' => array( 'unit_id' => $link['scope_id'], 'link_id' => $link['id'], 'privacy' => array( 'version' => NLRM_PRIVACY_VERSION, 'at' => nlrm_now() ),
					'household' => mb_substr( sanitize_text_field( (string) ( $d['household'] ?? '' ) ), 0, 120 ), 'move_in' => nlrm_date( $d['move_in'] ?? '' ), 'pets' => ! empty( $d['pets'] ) ),
			), $o, $actor );
			if ( ! is_wp_error( $c ) ) { nlrm_notify( $o, 'applied', array( 'where' => nlrm_notify_where( $o, $link['scope_id'] ), 'name' => $name ) ); }
			return is_wp_error( $c ) ? $c : array( 'contact_id' => $c['id'] );
		}

		if ( 'vendor' === $link['purpose'] && 'vendor_update' === $act ) {
			$status = in_array( $d['status'] ?? '', array( 'scheduled', 'progress', 'waiting', 'done' ), true ) ? $d['status'] : 'progress';
			$t = nlrm_save( 'ticket', array( 'id' => $link['scope_id'], 'status' => $status ) + ( isset( $d['cost'] ) ? array( 'cost' => (int) $d['cost'] ) : array() ), $o, $actor );
			if ( ! empty( $d['note'] ) ) { nlrm_event( $o, $actor, 'ticket', $link['scope_id'], 'msg_in', 'portal', sanitize_textarea_field( (string) $d['note'] ), array( 'status' => $status ) ); }
			if ( ! is_wp_error( $t ) && 'done' === $status ) { nlrm_notify( $o, 'vendor_done', array( 'title' => (string) ( $t['title'] ?? '' ) ) ); }
			return is_wp_error( $t ) ? $t : array( 'ticket' => $t );
		}

		return nlrm_err( 'nlrm_bad', 400, 'פעולה לא מוכרת.', 'Unknown action.' );
	}
}

/* ---------- e-signature with an evidence trail ---------- */
if ( ! function_exists( 'nlrm_sig_png_ok' ) ) {
	/* B23: the drawn signature as a PNG data URL, 200 to 400,000 base64 characters. A {200,400000} quantifier does not compile
	   in PCRE2 (the limit is 65,535), so preg_match returned false and every signature was refused: length is checked apart. */
	function nlrm_sig_png_ok( $img ) {
		$pre = 'data:image/png;base64,';
		if ( 0 !== strpos( $img, $pre ) ) { return false; }
		$b = substr( $img, strlen( $pre ) );
		$n = strlen( $b );
		$core = rtrim( $b, '=' );
		/* no regex over a long string: the alphabet by strspn, at most two '=' of padding */
		return $n >= 200 && $n <= 400000 && $n - strlen( $core ) <= 2 && strspn( $core, 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/' ) === strlen( $core );
	}
}
if ( ! function_exists( 'nlrm_sign' ) ) {
	/* A simple electronic signature (Electronic Signature Law 2001, s.1):
	   the drawn signature, the typed full name, the exact text signed
	   (SHA-256), the time, the link it came through and a hashed IP. */
	function nlrm_sign( $link, $d ) {
		$o = $link['owner_id'];
		$lease = nlrm_get( 'lease', $link['scope_id'], $o );
		if ( ! $lease ) { return nlrm_err( 'nlrm_link', 410, 'החוזה אינו פעיל.', 'This lease is not active.' ); }
		$name = mb_substr( sanitize_text_field( (string) ( $d['name'] ?? '' ) ), 0, 120 );
		$img  = (string) ( $d['signature'] ?? '' );
		if ( '' === $name || empty( $d['agree'] ) || ! nlrm_sig_png_ok( $img ) ) {
			return nlrm_err( 'nlrm_bad', 400, 'נדרשים שם מלא, חתימה ואישור שקראתם את החוזה.', 'Full name, a signature and confirming you read the lease are required.' );
		}
		$who = $link['contact_id'] ? nlrm_get( 'contact', $link['contact_id'], $o ) : null;
		$text = nlrm_lease_text( $o, $lease, $who['lang'] ?? 'he' );
		$hash = hash( 'sha256', wp_json_encode( $text, JSON_UNESCAPED_UNICODE ) );
		global $wpdb;
		$signing = (array) ( $lease['signing'] ?? array() );
		$signing['parties'] = (array) ( $signing['parties'] ?? array() );
		$ip = isset( $_SERVER['REMOTE_ADDR'] ) ? (string) $_SERVER['REMOTE_ADDR'] : ''; // phpcs:ignore
		$signing['parties'][] = array(
			'contact_id' => $link['contact_id'], 'name' => $name, 'role' => 'tenant', 'at' => nlrm_now(),
			'text_sha256' => $hash, 'link' => $link['id'], 'ip_hash' => substr( hash( 'sha256', $ip . wp_salt( 'nonce' ) ), 0, 24 ),
			'ua' => mb_substr( isset( $_SERVER['HTTP_USER_AGENT'] ) ? sanitize_text_field( wp_unslash( $_SERVER['HTTP_USER_AGENT'] ) ) : '', 0, 160 ), // phpcs:ignore
			'sig_enc' => nlrm_enc( $img ),
		);
		$wpdb->update( nlrm_t( 'leases' ), array( 'signing' => wp_json_encode( $signing, JSON_UNESCAPED_UNICODE ), 'updated_at' => nlrm_now() ), array( 'id' => $lease['id'], 'owner_id' => $o ) );
		/* B22: the exact signed text kept as an encrypted document of the lease (a later template change never alters it) */
		if ( function_exists( 'nlrm_doc_store_bytes' ) && function_exists( 'nlrm_lease_signed_html' ) ) {
			$doc = nlrm_doc_store_bytes( $o, nlrm_lease_signed_html( $text, $name, nlrm_now(), $img, $hash ), ( 'he' === ( $text['lang'] ?? 'he' ) ? 'חוזה-חתום-' : 'signed-lease-' ) . (int) $lease['id'] . '-' . gmdate( 'Ymd-His', nlrm_time() ) . '.html', 'text/html; charset=utf-8', 'lease', (int) $lease['id'], 'lease', 'link:' . $link['id'] );
			if ( $doc ) {
				$signing['parties'][ count( $signing['parties'] ) - 1 ]['doc_id'] = $doc;
				$wpdb->update( nlrm_t( 'leases' ), array( 'signing' => wp_json_encode( $signing, JSON_UNESCAPED_UNICODE ) ), array( 'id' => $lease['id'], 'owner_id' => $o ) );
			}
		}
		nlrm_event( $o, 'link:' . $link['id'], 'lease', $lease['id'], 'sign', 'portal', $name, array( 'sha256' => $hash ) );
		nlrm_notify( $o, 'signed', array( 'where' => nlrm_notify_where( $o, $lease['unit_id'] ), 'name' => $name ) );
		return array( 'signed' => true, 'sha256' => $hash, 'at' => nlrm_now() );
	}
}

/* ---------- triage: rules first (always works), AI when available ---------- */
if ( ! function_exists( 'nlrm_triage' ) ) {
	/* the shared rule table (assets/rentals/i18n/triage.json), the same one the
	   app reads (rm-drawers.js N.triage): one answer on both sides */
	function nlrm_triage( $text ) {
		$t = mb_strtolower( (string) $text );
		$tb = nlrm_json( 'triage' );
		$cat = 'general';
		foreach ( (array) ( $tb['categories'] ?? array() ) as $c ) {
			foreach ( (array) $c[1] as $w ) { if ( false !== mb_strpos( $t, mb_strtolower( $w ) ) ) { $cat = $c[0]; break 2; } }
		}
		$urg = 'standard';
		foreach ( (array) ( $tb['urgent'] ?? array() ) as $w ) { if ( false !== mb_strpos( $t, mb_strtolower( $w ) ) ) { $urg = 'urgent'; break; } }
		$pro = (array) ( $tb['pro_he'] ?? array() );
		return array( 'category' => $cat, 'urgency' => $urg, 'pro' => $pro[ $cat ] ?? ( $pro['general'] ?? '' ), 'by' => 'rules' );
	}
}

/* ---------- the landlord's e-mail alerts (HAD-401: a tenant reported a payment, opened a repair or wrote, and nobody knew) ----------
   An urgent repair and a signed lease are sent at once; everything else waits for one summary a day (nlrm_daily_run).
   On by default, off in Settings (user meta nlrm_notify = 'off'). Never a phone number or an ID number in a mail. */
if ( ! function_exists( 'nlrm_notify_on' ) ) {
	function nlrm_notify_on( $owner ) { return 'off' !== (string) get_user_meta( $owner, 'nlrm_notify', true ); }
}
if ( ! function_exists( 'nlrm_notify_lang' ) ) {
	function nlrm_notify_lang( $owner ) {
		$l = (string) get_user_meta( $owner, 'nlrm_lang', true );
		if ( in_array( $l, array( 'he', 'en' ), true ) ) { return $l; }
		$loc = function_exists( 'get_user_locale' ) ? (string) get_user_locale( $owner ) : 'he_IL';
		return 0 === strpos( $loc, 'he' ) ? 'he' : 'en';
	}
}
if ( ! function_exists( 'nlrm_notify_where' ) ) {
	function nlrm_notify_where( $owner, $unit_id ) {
		$u = $unit_id ? nlrm_get( 'unit', (int) $unit_id, $owner ) : null;
		$p = $u ? nlrm_get( 'property', (int) $u['property_id'], $owner ) : null;
		return trim( ( $u ? $u['label'] : '' ) . ( $p ? ', ' . $p['address'] : '' ), ', ' );
	}
}
if ( ! function_exists( 'nlrm_notify_line' ) ) {
	function nlrm_notify_line( $kind, $v, $lang ) {
		$he = 'he' === $lang;
		$w = (string) ( $v['where'] ?? '' );
		switch ( $kind ) {
			case 'ticket_urgent': return $he ? "{$w}: תקלה דחופה: " . $v['title'] . '. לפי החוק מתקנים תקלה כזו תוך 3 ימים.' : "{$w}: an urgent repair: " . $v['title'] . '. By law such a repair is due within 3 days.';
			case 'ticket': return $he ? "{$w}: תקלה חדשה: " . $v['title'] : "{$w}: a new repair: " . $v['title'];
			case 'paid': return $he ? "{$w}: השוכר דיווח על תשלום של " . $v['amount'] . ' (' . $v['date'] . '). מאשרים כשהכסף נכנס.' : "{$w}: the tenant reported a payment of " . $v['amount'] . ' (' . $v['date'] . '). Confirm it when the money arrives.';
			case 'message': return $he ? "{$w}: הודעה מהשוכר: " . $v['text'] : "{$w}: a message from the tenant: " . $v['text'];
			case 'signed': return $he ? "{$w}: " . $v['name'] . ' חתם על החוזה. העותק החתום שמור במסמכי הדירה.' : "{$w}: " . $v['name'] . ' signed the lease. The signed copy is in the apartment\'s documents.';
			case 'applied': return $he ? "{$w}: מועמד חדש לשכירות: " . $v['name'] : "{$w}: a new applicant: " . $v['name'];
			case 'vendor_done': return $he ? 'בעל המקצוע עדכן שהתקלה טופלה: ' . $v['title'] : 'The professional reported the repair done: ' . $v['title'];
		}
		return '';
	}
}
if ( ! function_exists( 'nlrm_notify_send' ) ) {
	function nlrm_notify_send( $owner, $subject, $lines ) {
		$u = get_userdata( $owner );
		$to = $u && ! empty( $u->user_email ) ? (string) $u->user_email : '';
		if ( ! $to || ! $lines ) { return false; }
		$he = 'he' === nlrm_notify_lang( $owner );
		$body = implode( "\n\n", $lines ) . "\n\n" . ( $he ? 'לפתוח את ניהול ההשכרות: ' : 'Open your rentals: ' ) . home_url( '/my-rentals/' ) . "\n" .
			( $he ? 'אפשר לכבות את ההתראות בהגדרות.' : 'You can turn these alerts off in Settings.' );
		return (bool) wp_mail( $to, $subject, $body );
	}
}
if ( ! function_exists( 'nlrm_notify' ) ) {
	function nlrm_notify( $owner, $kind, $v ) {
		$owner = (int) $owner;
		if ( ! $owner || ! nlrm_notify_on( $owner ) ) { return; }
		$lang = nlrm_notify_lang( $owner );
		if ( in_array( $kind, array( 'ticket_urgent', 'signed' ), true ) ) {
			$k = 'nlrm_ntf_' . $owner . '_' . gmdate( 'Ymd', nlrm_time() );
			$n = (int) get_transient( $k );
			if ( $n < 20 ) { /* at most 20 immediate mails a day; the rest go to the summary */
				set_transient( $k, $n + 1, DAY_IN_SECONDS );
				$subj = 'ticket_urgent' === $kind ? ( 'he' === $lang ? 'תקלה דחופה: ' : 'Urgent repair: ' ) . ( $v['where'] ?? '' ) : ( 'he' === $lang ? 'החוזה נחתם: ' : 'Lease signed: ' ) . ( $v['where'] ?? '' );
				nlrm_notify_send( $owner, $subj, array( nlrm_notify_line( $kind, $v, $lang ) ) );
				return;
			}
		}
		$q = array_values( array_filter( (array) get_user_meta( $owner, 'nlrm_notify_q', true ) ) );
		/* a replayed report (the same ledger line) is told once */
		foreach ( $q as $it ) { if ( isset( $v['id'] ) && ( $it['kind'] ?? '' ) === $kind && (int) ( $it['v']['id'] ?? 0 ) === (int) $v['id'] ) { return; } }
		$q[] = array( 'kind' => $kind, 'v' => $v, 'at' => nlrm_now() );
		update_user_meta( $owner, 'nlrm_notify_q', array_slice( $q, -200 ) );
	}
}
if ( ! function_exists( 'nlrm_notify_digest' ) ) {
	/* once a day: one mail per landlord with everything queued, then the queue is empty */
	function nlrm_notify_digest() {
		global $wpdb;
		$ids = $wpdb->get_col( $wpdb->prepare( "SELECT user_id FROM {$wpdb->usermeta} WHERE meta_key = %s", 'nlrm_notify_q' ) );
		foreach ( (array) $ids as $o ) {
			$o = (int) $o;
			$q = (array) get_user_meta( $o, 'nlrm_notify_q', true );
			delete_user_meta( $o, 'nlrm_notify_q' );
			if ( ! $q || ! nlrm_notify_on( $o ) ) { continue; }
			$lang = nlrm_notify_lang( $o );
			$lines = array_values( array_filter( array_map( function ( $it ) use ( $lang ) { return nlrm_notify_line( (string) ( $it['kind'] ?? '' ), (array) ( $it['v'] ?? array() ), $lang ); }, $q ) ) );
			$subj = 'he' === $lang ? 'ניהול השכרות: ' . count( $lines ) . ' עדכונים' : 'Rentals: ' . count( $lines ) . ' updates';
			nlrm_notify_send( $o, $subj, $lines );
		}
	}
}
