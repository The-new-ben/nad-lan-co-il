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
	$from = (string) get_option( 'nadlan_mail_from', '' );
	if ( '' !== $from ) {
		$phpmailer->setFrom( $from, (string) get_option( 'nadlan_mail_from_name', 'נדלן' ), false );
		$phpmailer->Sender = $from; /* envelope alignment for SPF/DMARC */
	}
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
