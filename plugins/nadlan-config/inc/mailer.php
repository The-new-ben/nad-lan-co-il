<?php
/**
 * nadlan-config - SMTP mailer (v1.72.192)
 *
 * Gmail marks the site's mail as spam: the web server sends raw PHP mail with
 * no DKIM signature, and uPress support will not enable DKIM for the domain
 * (owner, 2026-08-12). The fix is an authenticated external SMTP relay that
 * signs mail with an aligned DKIM key. This module routes every wp_mail
 * through that relay once credentials are configured:
 *
 *   nadlan_smtp_host / nadlan_smtp_port / nadlan_smtp_secure (tls|ssl)
 *   nadlan_smtp_user / nadlan_smtp_pass
 *   nadlan_mail_from / nadlan_mail_from_name
 *
 * Unconfigured (empty host) = untouched WordPress default, a safe no-op.
 * Admin-only test route: POST /nadlan/v1/mail-test {"to": "..."} sends a
 * probe message and reports transport + settings summary (never secrets).
 */

if ( ! defined( 'ABSPATH' ) ) { exit; }

add_action( 'phpmailer_init', function ( $phpmailer ) {
	/* ALWAYS align the envelope: the server IP is authorized in the domain's
	 * SPF, but the default Return-Path is the hosting user's address, which
	 * breaks DMARC alignment and lands mail in spam. Aligned SPF alone
	 * satisfies Gmail's minimum for low-volume transactional mail. */
	$from = (string) get_option( 'nadlan_mail_from', '' );
	if ( '' === $from ) { $from = 'wordpress@nad-lan.co.il'; }
	$phpmailer->setFrom( $from, (string) get_option( 'nadlan_mail_from_name', 'נדלן' ), false );
	$phpmailer->Sender = $from;

	/* Server-side DKIM: key generated on this server (selector "nadlan").
	 * Signing stays OFF until the DNS TXT is published and verified via
	 * /nadlan/v1/dkim-check - signing with an unpublished key would show
	 * dkim=fail, which is worse than no signature. */
	if ( 'on' === (string) get_option( 'nadlan_dkim_enabled', '' ) ) {
		$key = (string) get_option( 'nadlan_dkim_private_key', '' );
		if ( '' !== $key ) {
			$phpmailer->DKIM_domain         = 'nad-lan.co.il';
			$phpmailer->DKIM_selector       = (string) get_option( 'nadlan_dkim_selector', 'nadlan' );
			$phpmailer->DKIM_private_string = $key;
			$phpmailer->DKIM_identity       = $from;
		}
	}

	$host = (string) get_option( 'nadlan_smtp_host', '' );
	if ( '' === $host ) { return; }
	$phpmailer->isSMTP();
	$phpmailer->Host       = $host;
	$phpmailer->Port       = (int) get_option( 'nadlan_smtp_port', 587 );
	$phpmailer->SMTPAuth   = true;
	$phpmailer->Username   = (string) get_option( 'nadlan_smtp_user', '' );
	$phpmailer->Password   = (string) get_option( 'nadlan_smtp_pass', '' );
	$secure                = (string) get_option( 'nadlan_smtp_secure', 'tls' );
	$phpmailer->SMTPSecure = in_array( $secure, array( 'tls', 'ssl' ), true ) ? $secure : 'tls';
} );

/* One-time server-side DKIM key generation + the exact DNS record to publish.
 * Admin-only. Never returns the private key. */
add_action( 'rest_api_init', function () {
	register_rest_route( 'nadlan/v1', '/dkim-setup', array(
		'methods'             => 'POST',
		'permission_callback' => function () { return current_user_can( 'update_plugins' ); },
		'callback'            => function () {
			$selector = (string) get_option( 'nadlan_dkim_selector', 'nadlan' );
			$existing = (string) get_option( 'nadlan_dkim_public_key', '' );
			if ( '' === $existing ) {
				if ( ! function_exists( 'openssl_pkey_new' ) ) {
					return array( 'err' => 'openssl unavailable' );
				}
				$res = openssl_pkey_new( array( 'private_key_bits' => 2048, 'private_key_type' => OPENSSL_KEYTYPE_RSA ) );
				if ( ! $res ) { return array( 'err' => 'keygen failed' ); }
				openssl_pkey_export( $res, $priv );
				$det = openssl_pkey_get_details( $res );
				$pub = preg_replace( '/-----.*?-----|\s+/', '', $det['key'] );
				update_option( 'nadlan_dkim_private_key', $priv, false );
				update_option( 'nadlan_dkim_public_key', $pub, false );
				update_option( 'nadlan_dkim_selector', $selector, false );
				$existing = $pub;
			}
			return array(
				'selector'   => $selector,
				'dns_name'   => $selector . '._domainkey.nad-lan.co.il',
				'dns_type'   => 'TXT',
				'dns_value'  => 'v=DKIM1; k=rsa; p=' . $existing,
				'enabled'    => (string) get_option( 'nadlan_dkim_enabled', '' ),
			);
		},
	) );
	register_rest_route( 'nadlan/v1', '/dkim-check', array(
		'methods'             => 'POST',
		'permission_callback' => function () { return current_user_can( 'update_plugins' ); },
		'callback'            => function () {
			$selector = (string) get_option( 'nadlan_dkim_selector', 'nadlan' );
			$pub      = (string) get_option( 'nadlan_dkim_public_key', '' );
			if ( '' === $pub ) { return array( 'err' => 'run dkim-setup first' ); }
			$records = dns_get_record( $selector . '._domainkey.nad-lan.co.il', DNS_TXT );
			$found   = '';
			foreach ( (array) $records as $r ) {
				$txt = isset( $r['txt'] ) ? $r['txt'] : ( isset( $r['entries'] ) ? implode( '', $r['entries'] ) : '' );
				if ( false !== strpos( $txt, 'DKIM1' ) ) { $found = $txt; break; }
			}
			$match = ( '' !== $found && false !== strpos( str_replace( ' ', '', $found ), substr( $pub, 0, 60 ) ) );
			if ( $match ) { update_option( 'nadlan_dkim_enabled', 'on', false ); }
			return array( 'dns_found' => '' !== $found, 'key_match' => $match,
				'signing_enabled' => (string) get_option( 'nadlan_dkim_enabled', '' ) );
		},
	) );
} );

add_filter( 'wp_mail_from', function ( $f ) {
	$from = (string) get_option( 'nadlan_mail_from', '' );
	return '' !== $from && '' !== (string) get_option( 'nadlan_smtp_host', '' ) ? $from : $f;
} );

add_filter( 'wp_mail_from_name', function ( $n ) {
	$name = (string) get_option( 'nadlan_mail_from_name', '' );
	return '' !== $name && '' !== (string) get_option( 'nadlan_smtp_host', '' ) ? $name : $n;
} );

add_action( 'rest_api_init', function () {
	register_rest_route( 'nadlan/v1', '/mail-test', array(
		'methods'             => 'POST',
		'permission_callback' => function () { return current_user_can( 'update_plugins' ); },
		'callback'            => function ( $request ) {
			$to = sanitize_email( (string) $request->get_param( 'to' ) );
			if ( ! $to ) { $to = (string) get_option( 'admin_email' ); }
			$err = null;
			add_action( 'wp_mail_failed', function ( $e ) use ( &$err ) { $err = $e->get_error_message(); } );
			$sent = wp_mail(
				$to,
				'[נדלן] בדיקת ערוץ מייל ' . gmdate( 'H:i:s' ),
				"בדיקת מסירה מהאתר.\nאם ההודעה הזאת הגיעה לתיבה הראשית (לא ספאם) - הערוץ תקין.\nזמן: " . gmdate( 'c' )
			);
			return array(
				'sent'      => (bool) $sent,
				'error'     => $err,
				'transport' => ( '' !== (string) get_option( 'nadlan_smtp_host', '' ) ) ? 'smtp' : 'php-mail',
				'smtp_host' => (string) get_option( 'nadlan_smtp_host', '' ),
				'from'      => (string) get_option( 'nadlan_mail_from', '' ),
				'to'        => $to,
			);
		},
	) );
} );
