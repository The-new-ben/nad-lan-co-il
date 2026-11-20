<?php
/**
 * nadlan-config - RENTALS v2: the REST API (HAD-383, 1.10.2026).
 *
 * Namespace nadlan/v1/rm/*. Two kinds of callers:
 *  - the landlord (and his team), logged in, cookie + X-WP-Nonce;
 *  - a link holder (tenant portal, the landlord's quick link from WhatsApp,
 *    an applicant, a signer), with a 256-bit token sent in the X-NLRM-Link
 *    header. The token travels after the '#' of the URL, so WhatsApp's link
 *    preview never sees it, it is stored only as a SHA-256 hash, it expires,
 *    it can be revoked, and every use is written to the timeline.
 */

if ( ! defined( 'ABSPATH' ) ) { exit; }

if ( ! function_exists( 'nlrm_lang' ) ) {
	function nlrm_lang( $raw = null ) {
		if ( null === $raw ) { $raw = isset( $_GET['lang'] ) ? sanitize_key( wp_unslash( $_GET['lang'] ) ) : ''; } // phpcs:ignore
		$raw = sanitize_key( (string) $raw );
		return in_array( $raw, nlrm_langs(), true ) ? $raw : 'he';
	}
}
if ( ! function_exists( 'nlrm_langs' ) ) {
	/* languages whose string table is complete; fr/ru/ar join when theirs is */
	function nlrm_langs() {
		$langs = array( 'he', 'en' );
		foreach ( array( 'fr', 'ru', 'ar' ) as $l ) {
			if ( file_exists( NLRM_DIR_ASSETS . 'i18n/' . $l . '.json' ) ) { $langs[] = $l; }
		}
		return $langs;
	}
}

if ( ! function_exists( 'nlrm_err' ) ) {
	function nlrm_err( $code, $status, $he, $en ) {
		$lang = isset( $_SERVER['HTTP_X_NLRM_LANG'] ) ? sanitize_key( wp_unslash( $_SERVER['HTTP_X_NLRM_LANG'] ) ) : 'he'; // phpcs:ignore
		return new WP_Error( $code, 'he' === $lang ? $he : $en, array( 'status' => $status ) );
	}
}

if ( ! function_exists( 'nlrm_ip_limited' ) ) {
	function nlrm_ip_limited( $bucket, $cap, $window ) {
		$ip  = isset( $_SERVER['REMOTE_ADDR'] ) ? (string) $_SERVER['REMOTE_ADDR'] : ''; // phpcs:ignore
		$key = 'nlrm_rl_' . $bucket . '_' . substr( hash( 'sha256', $ip . wp_salt( 'nonce' ) ), 0, 20 );
		$n   = (int) get_transient( $key );
		if ( $n >= $cap ) { return true; }
		set_transient( $key, $n + 1, $window );
		return false;
	}
}

/* ---------- links (magic links) ---------- */
if ( ! function_exists( 'nlrm_link_create' ) ) {
	function nlrm_link_create( $owner, $purpose, $scope, $scope_id, $contact_id, $days ) {
		global $wpdb;
		$raw   = random_bytes( 32 );
		$token = rtrim( strtr( base64_encode( $raw ), '+/', '-_' ), '=' );
		$days  = max( 1, min( 4000, (int) $days ) );
		$wpdb->insert( nlrm_t( 'links' ), array(
			'owner_id' => $owner, 'token_hash' => hash( 'sha256', $token ), 'purpose' => $purpose,
			'scope' => $scope, 'scope_id' => (int) $scope_id, 'contact_id' => (int) $contact_id,
			'expires_at' => gmdate( 'Y-m-d H:i:s', nlrm_time() + $days * DAY_IN_SECONDS ),
			'created_at' => nlrm_now(),
		) );
		$id = (int) $wpdb->insert_id;
		nlrm_event( $owner, '', $scope, $scope_id, 'link_new', '', '', array( 'link' => $id, 'purpose' => $purpose, 'days' => $days ) );
		$frag = array( 'tenant' => 't', 'owner' => 'q', 'apply' => 'a', 'sign' => 's', 'vendor' => 'v' );
		return array(
			'id' => $id,
			/* ?l=1 opens the link page even while v2 is for administrators and pilots only */
			'url' => home_url( '/my-rentals/?l=1' ) . '#' . ( $frag[ $purpose ] ?? 't' ) . '=' . $token,
			'expires_at' => gmdate( 'Y-m-d', nlrm_time() + $days * DAY_IN_SECONDS ),
		);
	}
}
if ( ! function_exists( 'nlrm_link_from_request' ) ) {
	/* the token from the X-NLRM-Link header -> the link row, or null */
	function nlrm_link_from_request( $purposes ) {
		$token = isset( $_SERVER['HTTP_X_NLRM_LINK'] ) ? (string) wp_unslash( $_SERVER['HTTP_X_NLRM_LINK'] ) : ''; // phpcs:ignore
		if ( ! preg_match( '/^[A-Za-z0-9_\-]{40,60}$/', $token ) ) { return null; }
		if ( nlrm_ip_limited( 'link', 300, HOUR_IN_SECONDS ) ) { return null; }
		global $wpdb;
		$row = $wpdb->get_row( $wpdb->prepare( 'SELECT * FROM ' . nlrm_t( 'links' ) . ' WHERE token_hash = %s', hash( 'sha256', $token ) ), ARRAY_A );
		if ( ! $row || $row['revoked_at'] || strtotime( $row['expires_at'] . ' UTC' ) < nlrm_time() ) { return null; }
		if ( ! in_array( $row['purpose'], (array) $purposes, true ) ) { return null; }
		if ( (int) $row['max_uses'] > 0 && (int) $row['uses'] >= (int) $row['max_uses'] ) { return null; }
		$wpdb->update( nlrm_t( 'links' ), array( 'uses' => (int) $row['uses'] + 1, 'last_used_at' => nlrm_now() ), array( 'id' => (int) $row['id'] ) );
		$row['id'] = (int) $row['id']; $row['owner_id'] = (int) $row['owner_id']; $row['scope_id'] = (int) $row['scope_id']; $row['contact_id'] = (int) $row['contact_id'];
		return $row;
	}
}

/* ---------- private documents (encrypted at rest) ---------- */
if ( ! function_exists( 'nlrm_private_dir' ) ) {
	function nlrm_private_dir() {
		$up  = wp_upload_dir( null, false );
		$dir = trailingslashit( $up['basedir'] ) . 'nlrm-private/';
		if ( ! is_dir( $dir ) ) {
			wp_mkdir_p( $dir );
			@file_put_contents( $dir . '.htaccess', "Require all denied\nDeny from all\n" ); // phpcs:ignore
			@file_put_contents( $dir . 'index.php', "<?php // Silence.\n" ); // phpcs:ignore
		}
		return $dir;
	}
}
if ( ! function_exists( 'nlrm_doc_store' ) ) {
	function nlrm_doc_store( $owner, $file, $scope, $scope_id, $kind, $actor ) {
		if ( empty( $file['tmp_name'] ) || ! is_uploaded_file( $file['tmp_name'] ) ) {
			return nlrm_err( 'nlrm_nofile', 400, 'לא התקבל קובץ.', 'No file received.' );
		}
		if ( (int) $file['size'] > 15 * 1024 * 1024 ) { return nlrm_err( 'nlrm_big', 400, 'קובץ עד 15MB.', 'Files up to 15 MB.' ); }
		$check = wp_check_filetype_and_ext( $file['tmp_name'], $file['name'] );
		$ok = array( 'jpg', 'jpeg', 'png', 'webp', 'heic', 'pdf', 'doc', 'docx', 'xls', 'xlsx', 'txt' );
		if ( empty( $check['ext'] ) || ! in_array( strtolower( $check['ext'] ), $ok, true ) ) {
			return nlrm_err( 'nlrm_type', 400, 'סוג הקובץ אינו נתמך: תמונה, PDF, Word או Excel.', 'Unsupported file: image, PDF, Word or Excel.' );
		}
		$plan = nlrm_plan( $owner );
		global $wpdb;
		$used = (int) $wpdb->get_var( $wpdb->prepare( 'SELECT COALESCE(SUM(size),0) FROM ' . nlrm_t( 'docs' ) . ' WHERE owner_id = %d AND deleted_at IS NULL', $owner ) );
		if ( $used + (int) $file['size'] > $plan['limits']['docs_mb'] * 1024 * 1024 ) {
			return nlrm_err( 'nlrm_quota', 402, 'נגמר המקום לקבצים בחבילה הנוכחית.', 'Your plan\'s file storage is full.' );
		}
		$bytes = file_get_contents( $file['tmp_name'] ); // phpcs:ignore
		$sha   = hash( 'sha256', $bytes );
		$dir   = nlrm_private_dir() . (int) $owner . '/';
		wp_mkdir_p( $dir );
		$rel   = (int) $owner . '/' . wp_generate_password( 32, false, false ) . '.bin';
		$blob  = nlrm_blob_enc( $bytes );
		if ( false === file_put_contents( nlrm_private_dir() . $rel, $blob ) ) { // phpcs:ignore
			return nlrm_err( 'nlrm_write', 500, 'השמירה נכשלה, נסו שוב.', 'Saving failed, please try again.' );
		}
		$wpdb->insert( nlrm_t( 'docs' ), array(
			'owner_id' => $owner, 'scope' => $scope, 'scope_id' => (int) $scope_id, 'kind' => $kind,
			'name' => mb_substr( sanitize_file_name( (string) $file['name'] ), 0, 160 ), 'mime' => (string) $check['type'],
			'size' => (int) $file['size'], 'path' => $rel, 'sha256' => $sha, 'enc' => 1,
			'created_by' => mb_substr( (string) $actor, 0, 24 ), 'created_at' => nlrm_now(),
		) );
		$id = (int) $wpdb->insert_id;
		nlrm_event( $owner, $actor, $scope, $scope_id, 'doc_new', '', '', array( 'doc' => $id, 'kind' => $kind ) );
		return array( 'id' => $id, 'scope' => $scope, 'scope_id' => (int) $scope_id, 'kind' => $kind, 'name' => mb_substr( sanitize_file_name( (string) $file['name'] ), 0, 160 ), 'mime' => (string) $check['type'], 'size' => (int) $file['size'], 'created_by' => $actor, 'created_at' => nlrm_now() );
	}
}
if ( ! function_exists( 'nlrm_doc_store_bytes' ) ) {
	/* a document the system makes itself (a signed lease): encrypted at rest like an upload, never refused for quota */
	function nlrm_doc_store_bytes( $owner, $bytes, $name, $mime, $scope, $scope_id, $kind, $actor ) {
		global $wpdb;
		$dir = nlrm_private_dir() . (int) $owner . '/';
		wp_mkdir_p( $dir );
		$rel = (int) $owner . '/' . wp_generate_password( 32, false, false ) . '.bin';
		if ( false === file_put_contents( nlrm_private_dir() . $rel, nlrm_blob_enc( $bytes ) ) ) { return 0; } // phpcs:ignore
		$wpdb->insert( nlrm_t( 'docs' ), array(
			'owner_id' => $owner, 'scope' => $scope, 'scope_id' => (int) $scope_id, 'kind' => $kind,
			'name' => mb_substr( sanitize_file_name( (string) $name ), 0, 160 ), 'mime' => $mime, 'size' => strlen( $bytes ), 'path' => $rel,
			'sha256' => hash( 'sha256', $bytes ), 'enc' => 1, 'created_by' => mb_substr( (string) $actor, 0, 24 ), 'created_at' => nlrm_now(),
		) );
		$id = (int) $wpdb->insert_id;
		nlrm_event( $owner, $actor, $scope, $scope_id, 'doc_new', '', '', array( 'doc' => $id, 'kind' => $kind ) );
		return $id;
	}
}
if ( ! function_exists( 'nlrm_lease_signed_html' ) ) {
	/* the signed lease as one self-contained page: the exact text, the signer, the time, the signature, the text's sha256 */
	function nlrm_lease_signed_html( $text, $signer, $at, $img, $hash ) {
		$he  = 'he' === ( $text['lang'] ?? 'he' );
		$h   = '<!doctype html><html lang="' . ( $he ? 'he' : 'en' ) . '" dir="' . ( $he ? 'rtl' : 'ltr' ) . '"><head><meta charset="utf-8"><title>' . esc_html( (string) ( $text['title'] ?? '' ) ) . '</title>';
		$h  .= '<style>body{font-family:Arial,sans-serif;max-width:800px;margin:28px auto;padding:0 18px;color:#14212b;line-height:1.65}h1{font-size:24px}h2{font-size:17px;margin:20px 0 6px}.sig{margin-top:28px;border-top:1px solid #ccc;padding-top:12px}.sig img{max-width:320px;border:1px solid #ddd;background:#fff}.hash{font:12px monospace;color:#555;word-break:break-all;direction:ltr;unicode-bidi:isolate}</style></head><body>';
		$h  .= '<h1>' . esc_html( (string) ( $text['title'] ?? '' ) ) . '</h1><p>' . nl2br( esc_html( (string) ( $text['intro'] ?? '' ) ) ) . '</p>';
		foreach ( (array) ( $text['sections'] ?? array() ) as $s ) {
			$h .= '<h2>' . esc_html( (string) $s['h'] ) . '</h2>';
			foreach ( (array) $s['ps'] as $p ) { $h .= '<p>' . nl2br( esc_html( (string) $p ) ) . '</p>'; }
		}
		$h .= '<div class="sig"><p><b>' . esc_html( $he ? 'נחתם על ידי' : 'Signed by' ) . ':</b> ' . esc_html( $signer ) . ' · ' . esc_html( $at ) . ' (UTC)</p>';
		$h .= '<p><img alt="" src="' . esc_attr( $img ) . '"></p>';
		$h .= '<p class="hash">' . esc_html( ( $he ? 'טביעת הטקסט (SHA-256)' : 'Text fingerprint (SHA-256)' ) . ': ' . $hash ) . '</p>';
		$h .= '<p>' . esc_html( (string) ( $text['footer'] ?? '' ) ) . ' · ' . esc_html( (string) ( $text['version'] ?? '' ) ) . '</p></div></body></html>';
		return $h;
	}
}
if ( ! function_exists( 'nlrm_doc_stream' ) ) {
	function nlrm_doc_stream( $row, $inline ) {
		$blob = @file_get_contents( nlrm_private_dir() . $row['path'] ); // phpcs:ignore
		if ( false === $blob ) { status_header( 404 ); exit; }
		$out = nlrm_blob_dec( $blob );
		if ( false === $out ) { status_header( 409 ); exit; }
		nocache_headers();
		header( 'Content-Type: ' . ( $row['mime'] ?: 'application/octet-stream' ) );
		header( 'Content-Length: ' . strlen( $out ) );
		header( 'X-Content-Type-Options: nosniff' );
		if ( 0 === strpos( (string) $row['mime'], 'text/html' ) ) { header( "Content-Security-Policy: default-src 'none'; img-src data:; style-src 'unsafe-inline'; sandbox" ); } // a stored page shows, never runs
		header( 'Content-Disposition: ' . ( $inline ? 'inline' : 'attachment' ) . '; filename="' . rawurlencode( $row['name'] ) . '"' );
		echo $out; // phpcs:ignore
		exit;
	}
}

/* ---------- CBS (הלשכה המרכזית לסטטיסטיקה) linkage calculator, cached ---------- */
if ( ! function_exists( 'nlrm_cpi_calc' ) ) {
	/* amount in shekels from $from (Y-m-d) to $to (Y-m-d) by the known CPI,
	   via the CBS public calculator. Returns array or WP_Error. */
	function nlrm_cpi_calc( $amount, $from, $to ) {
		$from = nlrm_date( $from ); $to = nlrm_date( $to );
		if ( ! $from || ! $to || $amount <= 0 ) { return new WP_Error( 'nlrm_cpi_args', 'bad args' ); }
		$key = 'nlrm_cpi_' . md5( $from . '|' . $to );
		$f = get_transient( $key );
		if ( ! is_array( $f ) ) {
			$fd = gmdate( 'm-d-Y', strtotime( $from ) ); $td = gmdate( 'm-d-Y', strtotime( $to ) );
			$url = 'https://api.cbs.gov.il/index/data/calculator/120010?value=1000&date=' . $fd . '&toDate=' . $td . '&format=json&download=false';
			/* the CBS API answers browsers; WordPress's default agent was refused from the host (1.72.404 probe) */
			$args = array( 'timeout' => 20, 'redirection' => 2, 'headers' => array( 'User-Agent' => 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36 nad-lan.co.il', 'Accept' => 'application/json' ) );
			$r = wp_remote_get( $url, $args );
			if ( is_wp_error( $r ) || 200 !== (int) wp_remote_retrieve_response_code( $r ) ) {
				set_transient( 'nlrm_cpi_last_error', is_wp_error( $r ) ? $r->get_error_message() : 'http ' . wp_remote_retrieve_response_code( $r ), DAY_IN_SECONDS );
				return new WP_Error( 'nlrm_cpi_down', 'CBS unavailable' );
			}
			$j = json_decode( wp_remote_retrieve_body( $r ), true );
			if ( empty( $j['answer']['to_value'] ) ) { return new WP_Error( 'nlrm_cpi_empty', 'CBS empty' ); }
			$f = array(
				'factor' => (float) $j['answer']['to_value'] / 1000,
				'from_index_date' => (string) ( $j['answer']['from_index_date'] ?? '' ), 'from_index_value' => (float) ( $j['answer']['from_index_value'] ?? 0 ),
				'to_index_date' => (string) ( $j['answer']['to_index_date'] ?? '' ), 'to_index_value' => (float) ( $j['answer']['to_index_value'] ?? 0 ),
				'change_percent' => (float) ( $j['answer']['change_percent'] ?? 0 ),
			);
			set_transient( $key, $f, 12 * HOUR_IN_SECONDS );
		}
		$f['amount'] = round( $amount * $f['factor'], 2 );
		$f['source'] = 'הלשכה המרכזית לסטטיסטיקה · מחשבון הצמדה';
		return $f;
	}
}

/* ---------- export: the whole account, every table, every line ---------- */
if ( ! function_exists( 'nlrm_export' ) ) {
	function nlrm_export( $owner ) {
		global $wpdb;
		$b = nlrm_bootstrap( $owner );
		$states = array();
		nlrm_money( $owner, null, null, $states );
		$b['ledger'] = nlrm_ledger_rows( $wpdb->get_results( $wpdb->prepare( 'SELECT * FROM ' . nlrm_t( 'ledger' ) . ' WHERE owner_id = %d ORDER BY id ASC', $owner ), ARRAY_A ), $states );
		$b['events'] = nlrm_events( $owner, '', 0, 1000000 );
		$b['links'] = $wpdb->get_results( $wpdb->prepare( 'SELECT id, purpose, scope, scope_id, contact_id, expires_at, uses, revoked_at, created_at, last_used_at FROM ' . nlrm_t( 'links' ) . ' WHERE owner_id = %d ORDER BY id ASC', $owner ), ARRAY_A );
		$b['stats'] = (object) nlrm_stats( $owner, '1970-01-01' );
		$b['exported_at'] = nlrm_now();
		$b['format'] = 'nlrm-export-2';
		return $b;
	}
}

/* ---------- REST routes ---------- */
add_action( 'rest_api_init', function () {
	$ns = 'nadlan/v1';
	$owner_ok = function () {
		if ( ! nadlan_rm_on() || ! is_user_logged_in() ) { return false; }
		nlrm_maybe_install();
		return nlrm_owner() > 0;
	};
	/* nothing is written while the data key is missing (see nlrm_key_ok) */
	$writer_ok = function () use ( $owner_ok ) { return $owner_ok() && nlrm_can_write() && nlrm_key_ok(); };

	register_rest_route( $ns, '/rm/boot', array(
		'methods' => 'GET', 'permission_callback' => $owner_ok,
		'callback' => function () {
			$o = nlrm_owner();
			if ( function_exists( 'nlrm_import_legacy' ) && 'owner' === nlrm_role() ) { nlrm_import_legacy( $o ); }
			$ran = 'nlrm_ran_' . $o;
			if ( get_transient( $ran ) !== nlrm_today() && nlrm_key_ok() ) {
				nlrm_rent_run( $o );
				set_transient( $ran, nlrm_today(), DAY_IN_SECONDS );
			}
			return nlrm_bootstrap( $o );
		},
	) );

	register_rest_route( $ns, '/rm/save', array(
		'methods' => 'POST', 'permission_callback' => $writer_ok,
		'callback' => function ( WP_REST_Request $r ) {
			$o = nlrm_owner();
			$entity = sanitize_key( (string) $r->get_param( 'entity' ) );
			$data   = (array) $r->get_param( 'data' );
			if ( 'unit' === $entity && empty( $data['id'] ) ) {
				$plan = nlrm_plan( $o );
				global $wpdb;
				$n = (int) $wpdb->get_var( $wpdb->prepare( 'SELECT COUNT(*) FROM ' . nlrm_t( 'units' ) . ' WHERE owner_id = %d AND deleted_at IS NULL', $o ) );
				if ( $n >= $plan['limits']['units'] ) {
					return nlrm_err( 'nlrm_plan_units', 402, 'הגעתם למספר הדירות בחבילה החינמית. אפשר לשדרג בכל רגע.', 'You reached the free plan\'s apartment limit. Upgrade any time.' );
				}
			}
			/* idempotency: the app sends one client_ref per user action; a retry
			   after a timeout returns the row already saved instead of a duplicate */
			$cref = preg_replace( '/[^A-Za-z0-9_\-]/', '', (string) $r->get_param( 'client_ref' ) );
			$ckey = $cref ? 'nlrm_cref_' . $o . '_' . substr( $cref, 0, 40 ) : '';
			if ( $ckey ) {
				$seen = get_transient( $ckey );
				if ( is_array( $seen ) && ! empty( $seen['id'] ) ) { $prev = nlrm_get( $seen['entity'], (int) $seen['id'], $o ); if ( $prev ) { return $prev; } }
			}
			if ( 'ledger' === $entity ) {
				/* the books: a new line is an expense, income or an extra charge
				   (payments, deposits and corrections have their own routes);
				   an existing line may only get its note, reference or file */
				if ( empty( $data['id'] ) ) {
					$res = nlrm_book( $o, $data, nlrm_cref( $cref ) );
					return is_wp_error( $res ) || empty( $res['lease_id'] ) ? $res : nlrm_lease_pack( $o, $res['lease_id'], array( 'row' => $res ) );
				}
				$data = array_intersect_key( $data, array_flip( array( 'id', 'note', 'ref', 'doc_id' ) ) );
			}
			$res = nlrm_save( $entity, $data, $o );
			if ( ! is_wp_error( $res ) && $ckey ) { set_transient( $ckey, array( 'entity' => $entity, 'id' => (int) $res['id'] ), 30 * MINUTE_IN_SECONDS ); }
			if ( ! is_wp_error( $res ) && 'lease' === $entity ) {
				nlrm_rent_run( $o, null, (int) $res['id'] );
				return nlrm_lease_pack( $o, $res['id'], array( 'row' => nlrm_get( 'lease', $res['id'], $o ) ) );
			}
			return $res;
		},
	) );

	register_rest_route( $ns, '/rm/delete', array(
		'methods' => 'POST', 'permission_callback' => $writer_ok,
		'callback' => function ( WP_REST_Request $r ) {
			if ( 'ledger' === sanitize_key( (string) $r->get_param( 'entity' ) ) ) {
				return nlrm_err( 'nlrm_books', 409, 'שורה בספרים לא נמחקת: מבטלים אותה ורושמים מחדש.', 'A line in the books is never deleted: void it and record it again.' );
			}
			$ok = nlrm_delete( sanitize_key( (string) $r->get_param( 'entity' ) ), (int) $r->get_param( 'id' ), nlrm_owner() );
			return $ok ? array( 'deleted' => true ) : nlrm_err( 'nlrm_forbidden', 403, 'לא נמצא.', 'Not found.' );
		},
	) );

	register_rest_route( $ns, '/rm/event', array(
		'methods' => 'POST', 'permission_callback' => $writer_ok,
		'callback' => function ( WP_REST_Request $r ) {
			$o = nlrm_owner();
			$scope = sanitize_key( (string) $r->get_param( 'scope' ) );
			$sid = (int) $r->get_param( 'scope_id' );
			$ents = array( 'property' => 'property', 'unit' => 'unit', 'lease' => 'lease', 'contact' => 'contact', 'ticket' => 'ticket' );
			if ( ! isset( $ents[ $scope ] ) || ! nlrm_owns( $ents[ $scope ], $sid, $o ) ) { return nlrm_err( 'nlrm_forbidden', 403, 'לא נמצא.', 'Not found.' ); }
			$type = in_array( $r->get_param( 'type' ), array( 'note', 'msg_out', 'msg_in', 'call', 'visit' ), true ) ? (string) $r->get_param( 'type' ) : 'note';
			$ch = in_array( $r->get_param( 'channel' ), array( 'whatsapp', 'email', 'sms', 'phone', 'inperson', '' ), true ) ? (string) $r->get_param( 'channel' ) : '';
			$id = nlrm_event( $o, '', $scope, $sid, $type, $ch, sanitize_textarea_field( (string) $r->get_param( 'body' ) ), (array) $r->get_param( 'meta' ) );
			return nlrm_events( $o, $scope, $sid, 1 )[0] ?? array( 'id' => $id );
		},
	) );

	register_rest_route( $ns, '/rm/doc', array(
		'methods' => 'POST', 'permission_callback' => $writer_ok,
		'callback' => function ( WP_REST_Request $r ) {
			$o = nlrm_owner();
			$scope = sanitize_key( (string) $r->get_param( 'scope' ) );
			$sid = (int) $r->get_param( 'scope_id' );
			$ents = array( 'property' => 'property', 'unit' => 'unit', 'lease' => 'lease', 'contact' => 'contact', 'ticket' => 'ticket' );
			if ( ! isset( $ents[ $scope ] ) || ! nlrm_owns( $ents[ $scope ], $sid, $o ) ) { return nlrm_err( 'nlrm_forbidden', 403, 'לא נמצא.', 'Not found.' ); }
			$kinds = array( 'lease', 'id', 'payslip', 'bank', 'protocol', 'photo', 'receipt', 'invoice', 'insurance', 'nesach', 'cheque', 'plan', 'other' );
			$kind = in_array( $r->get_param( 'kind' ), $kinds, true ) ? (string) $r->get_param( 'kind' ) : 'other';
			$files = $r->get_file_params();
			return nlrm_doc_store( $o, $files['file'] ?? array(), $scope, $sid, $kind, 'u:' . get_current_user_id() );
		},
	) );

	register_rest_route( $ns, '/rm/doc/(?P<id>\d+)', array(
		'methods' => 'GET', 'permission_callback' => '__return_true',
		'callback' => function ( WP_REST_Request $r ) {
			global $wpdb;
			$row = $wpdb->get_row( $wpdb->prepare( 'SELECT * FROM ' . nlrm_t( 'docs' ) . ' WHERE id = %d AND deleted_at IS NULL', (int) $r['id'] ), ARRAY_A );
			if ( ! $row ) { return nlrm_err( 'nlrm_404', 404, 'לא נמצא.', 'Not found.' ); }
			$allowed = false;
			if ( is_user_logged_in() && nlrm_owner() === (int) $row['owner_id'] ) {
				$allowed = wp_verify_nonce( (string) $r->get_param( '_n' ), 'nlrm_doc_' . $row['id'] ) || wp_verify_nonce( (string) $r->get_header( 'x_wp_nonce' ), 'wp_rest' );
			}
			if ( ! $allowed ) {
				$link = nlrm_link_from_request( array( 'tenant' ) );
				if ( $link && (int) $link['owner_id'] === (int) $row['owner_id'] ) {
					$shared = (array) json_decode( (string) $wpdb->get_var( $wpdb->prepare( 'SELECT terms FROM ' . nlrm_t( 'leases' ) . ' WHERE id = %d', $link['scope_id'] ) ), true );
					$allowed = in_array( (int) $row['id'], array_map( 'intval', (array) ( $shared['shared_docs'] ?? array() ) ), true );
				}
			}
			if ( ! $allowed ) { return nlrm_err( 'nlrm_forbidden', 403, 'אין הרשאה.', 'Not allowed.' ); }
			nlrm_doc_stream( $row, '1' === (string) $r->get_param( 'inline' ) );
		},
	) );

	register_rest_route( $ns, '/rm/doc-delete', array(
		'methods' => 'POST', 'permission_callback' => $writer_ok,
		'callback' => function ( WP_REST_Request $r ) {
			global $wpdb;
			$o = nlrm_owner();
			$n = $wpdb->update( nlrm_t( 'docs' ), array( 'deleted_at' => nlrm_now() ), array( 'id' => (int) $r->get_param( 'id' ), 'owner_id' => $o ) );
			return array( 'deleted' => (bool) $n );
		},
	) );

	register_rest_route( $ns, '/rm/link', array(
		'methods' => 'POST', 'permission_callback' => $writer_ok,
		'callback' => function ( WP_REST_Request $r ) {
			$o = nlrm_owner();
			$purpose = in_array( $r->get_param( 'purpose' ), array( 'tenant', 'owner', 'apply', 'sign', 'vendor' ), true ) ? (string) $r->get_param( 'purpose' ) : 'tenant';
			$scope = sanitize_key( (string) $r->get_param( 'scope' ) );
			$sid = (int) $r->get_param( 'scope_id' );
			$need = array( 'tenant' => 'lease', 'sign' => 'lease', 'apply' => 'unit', 'vendor' => 'ticket', 'owner' => '' );
			if ( $need[ $purpose ] && ( $scope !== $need[ $purpose ] || ! nlrm_owns( $scope, $sid, $o ) ) ) {
				return nlrm_err( 'nlrm_forbidden', 403, 'לא נמצא.', 'Not found.' );
			}
			if ( 'owner' === $purpose && 'owner' !== nlrm_role() ) { return nlrm_err( 'nlrm_forbidden', 403, 'רק בעל החשבון.', 'Account owner only.' ); }
			$days = array( 'tenant' => 365, 'owner' => 14, 'apply' => 30, 'sign' => 14, 'vendor' => 30 );
			$n = $days[ $purpose ];
			if ( 'tenant' === $purpose ) {
				/* the tenant's link lives as long as the lease, plus the 60 days of the deposit */
				$l = nlrm_get( 'lease', $sid, $o );
				if ( $l && $l['end_date'] ) { $n = max( 30, nlrm_day_diff( nlrm_today(), nlrm_add_days( $l['end_date'], 60 ) ) ); }
			}
			return nlrm_link_create( $o, $purpose, $scope, $sid, (int) $r->get_param( 'contact_id' ), $n );
		},
	) );

	register_rest_route( $ns, '/rm/links', array(
		'methods' => 'GET', 'permission_callback' => $owner_ok,
		'callback' => function () {
			global $wpdb;
			$rows = $wpdb->get_results( $wpdb->prepare( 'SELECT id, purpose, scope, scope_id, contact_id, expires_at, uses, revoked_at, created_at, last_used_at FROM ' . nlrm_t( 'links' ) . ' WHERE owner_id = %d ORDER BY id DESC LIMIT 300', nlrm_owner() ), ARRAY_A );
			return array( 'links' => $rows );
		},
	) );

	register_rest_route( $ns, '/rm/link-revoke', array(
		'methods' => 'POST', 'permission_callback' => $writer_ok,
		'callback' => function ( WP_REST_Request $r ) {
			global $wpdb;
			$o = nlrm_owner();
			$n = $wpdb->update( nlrm_t( 'links' ), array( 'revoked_at' => nlrm_now() ), array( 'id' => (int) $r->get_param( 'id' ), 'owner_id' => $o ) );
			nlrm_event( $o, '', '', 0, 'link_revoke', '', '', array( 'link' => (int) $r->get_param( 'id' ) ) );
			return array( 'revoked' => (bool) $n );
		},
	) );

	register_rest_route( $ns, '/rm/cpi', array(
		'methods' => 'GET', 'permission_callback' => function () { return nadlan_rm_on() && ! nlrm_ip_limited( 'cpi', 120, HOUR_IN_SECONDS ); },
		'callback' => function ( WP_REST_Request $r ) {
			$res = nlrm_cpi_calc( (float) $r->get_param( 'amount' ), (string) $r->get_param( 'from' ), (string) $r->get_param( 'to' ) );
			return is_wp_error( $res ) ? nlrm_err( 'nlrm_cpi', 503, 'נתוני הלמ"ס אינם זמינים כרגע.', 'CBS data is not available right now.' ) : $res;
		},
	) );

	register_rest_route( $ns, '/rm/export', array(
		'methods' => 'GET', 'permission_callback' => $owner_ok,
		'callback' => function () {
			$o = nlrm_owner();
			nlrm_event( $o, '', '', 0, 'export', '', '', array() );
			return nlrm_export( $o );
		},
	) );

	register_rest_route( $ns, '/rm/erase', array(
		'methods' => 'POST', 'permission_callback' => $owner_ok,
		'callback' => function ( WP_REST_Request $r ) {
			if ( 'owner' !== nlrm_role() || 'ERASE' !== (string) $r->get_param( 'confirm' ) ) {
				return nlrm_err( 'nlrm_confirm', 400, 'נדרש אישור מפורש.', 'Explicit confirmation required.' );
			}
			global $wpdb;
			$o = nlrm_owner();
			foreach ( $wpdb->get_col( $wpdb->prepare( 'SELECT path FROM ' . nlrm_t( 'docs' ) . ' WHERE owner_id = %d', $o ) ) as $p ) {
				@unlink( nlrm_private_dir() . $p ); // phpcs:ignore
			}
			foreach ( array( 'properties', 'units', 'contacts', 'leases', 'ledger', 'tickets', 'docs', 'events', 'links', 'tasks', 'members' ) as $t ) {
				$wpdb->delete( nlrm_t( $t ), array( 'owner_id' => $o ) );
			}
			return array( 'erased' => true );
		},
	) );

	/* ---------- money (the books are written only through these) ---------- */
	$money_route = function ( $path, $fn ) use ( $ns, $writer_ok ) {
		register_rest_route( $ns, $path, array( 'methods' => 'POST', 'permission_callback' => $writer_ok, 'callback' => $fn ) );
	};
	$pack = function ( $o, $res, $lease_id ) {
		if ( is_wp_error( $res ) ) { return $res; }
		return nlrm_lease_pack( $o, $lease_id, array( 'row' => $res ) );
	};
	$money_route( '/rm/pay', function ( WP_REST_Request $r ) use ( $pack ) {
		$o = nlrm_owner();
		$d = (array) $r->get_param( 'data' );
		$res = nlrm_pay( $o, $d, nlrm_cref( $r->get_param( 'client_ref' ) ), 'u:' . get_current_user_id() );
		return $pack( $o, $res, (int) ( $d['lease_id'] ?? 0 ) );
	} );
	$money_route( '/rm/ledger-act', function ( WP_REST_Request $r ) use ( $pack ) {
		$o = nlrm_owner();
		$res = nlrm_ledger_act( $o, (int) $r->get_param( 'id' ), sanitize_key( (string) $r->get_param( 'act' ) ), (array) $r->get_param( 'data' ), 'u:' . get_current_user_id() );
		return $pack( $o, $res, is_wp_error( $res ) ? 0 : (int) $res['lease_id'] );
	} );
	$money_route( '/rm/deposit', function ( WP_REST_Request $r ) use ( $pack ) {
		$o = nlrm_owner();
		$lid = (int) $r->get_param( 'lease_id' );
		$res = nlrm_deposit( $o, $lid, sanitize_key( (string) $r->get_param( 'act' ) ), (array) $r->get_param( 'data' ), nlrm_cref( $r->get_param( 'client_ref' ) ), 'u:' . get_current_user_id() );
		return $pack( $o, $res, $lid );
	} );
	$money_route( '/rm/writeoff', function ( WP_REST_Request $r ) use ( $pack ) {
		$o = nlrm_owner();
		$lid = (int) $r->get_param( 'lease_id' );
		$res = nlrm_writeoff( $o, $lid, (array) $r->get_param( 'data' ), nlrm_cref( $r->get_param( 'client_ref' ) ), 'u:' . get_current_user_id() );
		return $pack( $o, $res, $lid );
	} );
	$money_route( '/rm/refund', function ( WP_REST_Request $r ) use ( $pack ) {
		$o = nlrm_owner();
		$lid = (int) $r->get_param( 'lease_id' );
		$res = nlrm_refund_credit( $o, $lid, (array) $r->get_param( 'data' ), nlrm_cref( $r->get_param( 'client_ref' ) ), 'u:' . get_current_user_id() );
		return $pack( $o, $res, $lid );
	} );
	$money_route( '/rm/lease-end', function ( WP_REST_Request $r ) {
		$o = nlrm_owner();
		$lid = (int) $r->get_param( 'lease_id' );
		$res = nlrm_lease_end( $o, $lid, (array) $r->get_param( 'data' ), 'u:' . get_current_user_id() );
		return is_wp_error( $res ) ? $res : nlrm_lease_pack( $o, $lid );
	} );
	$money_route( '/rm/lease-renew', function ( WP_REST_Request $r ) {
		$o = nlrm_owner();
		$lid = (int) $r->get_param( 'lease_id' );
		$res = nlrm_lease_renew( $o, $lid, (array) $r->get_param( 'data' ), nlrm_cref( $r->get_param( 'client_ref' ) ), 'u:' . get_current_user_id() );
		if ( is_wp_error( $res ) ) { return $res; }
		$new = nlrm_lease_pack( $o, (int) $res['id'] );
		$new['old'] = nlrm_lease_pack( $o, $lid );
		return $new;
	} );
	register_rest_route( $ns, '/rm/ledger', array(
		'methods' => 'GET', 'permission_callback' => $owner_ok,
		'callback' => function ( WP_REST_Request $r ) {
			$o = nlrm_owner();
			$lid = (int) $r->get_param( 'lease_id' );
			if ( ! nlrm_owns( 'lease', $lid, $o ) ) { return nlrm_err( 'nlrm_forbidden', 403, 'לא נמצא.', 'Not found.' ); }
			return nlrm_lease_pack( $o, $lid );
		},
	) );

	/* the evidence file: every line of the lease's books and every event of the lease and its tenants, from the first day */
	register_rest_route( $ns, '/rm/evidence', array(
		'methods' => 'GET', 'permission_callback' => $owner_ok,
		'callback' => function ( WP_REST_Request $r ) {
			$o = nlrm_owner();
			$lid = (int) $r->get_param( 'lease_id' );
			if ( ! nlrm_owns( 'lease', $lid, $o ) ) { return nlrm_err( 'nlrm_forbidden', 403, 'לא נמצא.', 'Not found.' ); }
			$pack = nlrm_lease_pack( $o, $lid );
			$ev = nlrm_events( $o, 'lease', $lid, 50000 );
			$parties = (array) ( $pack['lease']['parties'] ?? array() );
			foreach ( array_slice( (array) ( $parties['tenants'] ?? array() ), 0, 6 ) as $cid ) {
				if ( (int) $cid ) { $ev = array_merge( $ev, nlrm_events( $o, 'contact', (int) $cid, 50000 ) ); }
			}
			usort( $ev, function ( $a, $b ) { return strcmp( $a['at'], $b['at'] ) ?: ( $a['id'] - $b['id'] ); } );
			$pack['events'] = $ev;
			return $pack;
		},
	) );

	/* ---------- link holders ---------- */
	register_rest_route( $ns, '/rm/portal', array(
		'methods' => 'GET', 'permission_callback' => function () { return nadlan_rm_on(); },
		'callback' => function () {
			nlrm_maybe_install();
			$link = nlrm_link_from_request( array( 'tenant', 'owner', 'apply', 'sign', 'vendor' ) );
			if ( ! $link ) { return nlrm_err( 'nlrm_link', 410, 'הקישור אינו בתוקף. בקשו קישור חדש מבעל הדירה.', 'This link is no longer valid. Ask your landlord for a new one.' ); }
			return nlrm_portal_payload( $link );
		},
	) );

	register_rest_route( $ns, '/rm/portal/act', array(
		'methods' => 'POST', 'permission_callback' => function () { return nadlan_rm_on(); },
		'callback' => function ( WP_REST_Request $r ) {
			$link = nlrm_link_from_request( array( 'tenant', 'owner', 'apply', 'sign', 'vendor' ) );
			if ( ! $link ) { return nlrm_err( 'nlrm_link', 410, 'הקישור אינו בתוקף.', 'This link is no longer valid.' ); }
			if ( nlrm_ip_limited( 'act', 60, HOUR_IN_SECONDS ) ) { return nlrm_err( 'nlrm_rl', 429, 'יותר מדי פעולות, נסו בעוד שעה.', 'Too many actions, try again in an hour.' ); }
			return nlrm_portal_act( $link, $r );
		},
	) );

	register_rest_route( $ns, '/rm/portal/doc', array(
		'methods' => 'POST', 'permission_callback' => function () { return nadlan_rm_on(); },
		'callback' => function ( WP_REST_Request $r ) {
			$link = nlrm_link_from_request( array( 'tenant', 'apply', 'vendor' ) );
			if ( ! $link ) { return nlrm_err( 'nlrm_link', 410, 'הקישור אינו בתוקף.', 'This link is no longer valid.' ); }
			if ( nlrm_ip_limited( 'pdoc', 30, HOUR_IN_SECONDS ) ) { return nlrm_err( 'nlrm_rl', 429, 'יותר מדי קבצים, נסו בעוד שעה.', 'Too many files, try again in an hour.' ); }
			$files = $r->get_file_params();
			$kind = in_array( $r->get_param( 'kind' ), array( 'photo', 'id', 'payslip', 'bank', 'receipt', 'other' ), true ) ? (string) $r->get_param( 'kind' ) : 'other';
			$scope = 'apply' === $link['purpose'] ? 'contact' : ( 'vendor' === $link['purpose'] ? 'ticket' : 'lease' );
			$sid = 'apply' === $link['purpose'] ? (int) $r->get_param( 'contact_id' ) : $link['scope_id'];
			if ( 'apply' === $link['purpose'] ) {
				$c = nlrm_get( 'contact', $sid, $link['owner_id'] );
				if ( ! $c || (int) ( ( (array) $c['meta'] )['link_id'] ?? 0 ) !== (int) $link['id'] ) { return nlrm_err( 'nlrm_forbidden', 403, 'לא נמצא.', 'Not found.' ); }
			}
			return nlrm_doc_store( $link['owner_id'], $files['file'] ?? array(), $scope, $sid, $kind, 'link:' . $link['id'] );
		},
	) );
} );
