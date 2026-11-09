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
	if ( '' === $host || '' === (string) get_option( 'nadlan_smtp_pass', '' ) ) { return; }  // 1.72.509: no key yet = keep sending through the server, never an SMTP without
	if ( ! nadlan_smtp_check() ) { return; } // 1.72.621 (HAD-687): a key Brevo refuses never stops the site's mail; it keeps going through the host a key
	$phpmailer->isSMTP();
	$phpmailer->Host       = $host;
	$phpmailer->Port       = (int) get_option( 'nadlan_smtp_port', 587 );
	$phpmailer->SMTPAuth   = true;
	$phpmailer->Username   = (string) get_option( 'nadlan_smtp_user', '' );
	$phpmailer->Password   = (string) get_option( 'nadlan_smtp_pass', '' );
	$secure                = (string) get_option( 'nadlan_smtp_secure', 'tls' );
	$phpmailer->SMTPSecure = in_array( $secure, array( 'tls', 'ssl' ), true ) ? $secure : 'tls';
}, PHP_INT_MAX );  // 1.72.619 (HAD-687): last, so WP Mail SMTP in "Default (none)" (it sets Mailer = 'mail' at priority 10) no longer sends the mail through the host instead of Brevo

/**
 * 1.72.621 (HAD-687): does the SMTP server accept the saved login and key? A real connect + TLS + AUTH, no message sent. The answer is
 * cached for a day (an hour after a refusal) and redone at once on every save of the settings screen. The key itself is never printed
 * or logged; only the server's answer is kept, for the screen.
 */
function nadlan_smtp_check( $force = false ) {
	$host   = (string) get_option( 'nadlan_smtp_host', '' );
	$user   = (string) get_option( 'nadlan_smtp_user', '' );
	$pass   = (string) get_option( 'nadlan_smtp_pass', '' );
	$port   = (int) get_option( 'nadlan_smtp_port', 587 );
	$secure = (string) get_option( 'nadlan_smtp_secure', 'tls' );
	if ( '' === $host || '' === $pass ) { return false; }
	$sig = md5( $host . '|' . $port . '|' . $secure . '|' . $user . '|' . $pass );
	$st  = (array) get_option( 'nadlan_smtp_state', array() );
	if ( ! $force && ( $st['sig'] ?? '' ) === $sig && (int) ( $st['t'] ?? 0 ) > time() - ( ! empty( $st['ok'] ) ? DAY_IN_SECONDS : HOUR_IN_SECONDS ) ) { return ! empty( $st['ok'] ); }
	if ( ! class_exists( 'PHPMailer\\PHPMailer\\SMTP' ) ) { require_once ABSPATH . WPINC . '/PHPMailer/SMTP.php'; require_once ABSPATH . WPINC . '/PHPMailer/Exception.php'; }
	$ok = false; $err = '';
	try {
		$smtp = new PHPMailer\PHPMailer\SMTP();
		$me   = (string) wp_parse_url( home_url(), PHP_URL_HOST );
		if ( $smtp->connect( ( 'ssl' === $secure ? 'ssl://' : '' ) . $host, $port, 10 ) && $smtp->hello( $me ) ) {
			if ( 'tls' === $secure && ! ( $smtp->startTLS() && $smtp->hello( $me ) ) ) { $err = 'TLS'; }
			else { $ok = (bool) $smtp->authenticate( $user, $pass ); }
		} else { $err = 'connect'; }
		if ( ! $ok && '' === $err ) { $e = (array) $smtp->getError(); $err = trim( (string) ( $e['smtp_code'] ?? '' ) . ' ' . (string) ( $e['error'] ?? '' ) . ' ' . (string) ( $e['detail'] ?? '' ) ); }
		$smtp->quit(); $smtp->close();
	} catch ( Exception $x ) { $err = $x->getMessage(); }
	update_option( 'nadlan_smtp_state', array( 'sig' => $sig, 't' => time(), 'ok' => $ok, 'err' => mb_substr( preg_replace( '/[^\p{L}\p{N}\s.,:;()\-\/]/u', '', $err ), 0, 160 ) ), false );
	return $ok;
}

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

/* 1.72.509 (Ben 23.10.2026, Brevo): a settings screen under Settings > "מייל יוצא" where the owner pastes the SMTP login and key
 * himself (agents never type or read keys). The key field is write-only: it is never printed back, an empty field keeps the saved
 * key. Brevo defaults: smtp-relay.brevo.com, 587, tls. A test button sends one message to the admin address and shows the result. */
add_action( 'admin_menu', function () {
	add_options_page( 'מייל יוצא', 'מייל יוצא (Brevo)', 'manage_options', 'nadlan-mail', function () {
		if ( ! current_user_can( 'manage_options' ) ) { return; }
		$msg = '';
		if ( isset( $_POST['nadlan_mail_nonce'] ) && wp_verify_nonce( sanitize_text_field( wp_unslash( $_POST['nadlan_mail_nonce'] ) ), 'nadlan_mail' ) ) {
			$host = sanitize_text_field( wp_unslash( $_POST['smtp_host'] ?? '' ) );
			update_option( 'nadlan_smtp_host', $host, false );
			update_option( 'nadlan_smtp_port', max( 1, (int) ( $_POST['smtp_port'] ?? 587 ) ), false );
			update_option( 'nadlan_smtp_secure', in_array( $_POST['smtp_secure'] ?? 'tls', array( 'tls', 'ssl' ), true ) ? $_POST['smtp_secure'] : 'tls', false );
			update_option( 'nadlan_smtp_user', sanitize_text_field( wp_unslash( $_POST['smtp_user'] ?? '' ) ), false );
			$key = trim( (string) wp_unslash( $_POST['smtp_pass'] ?? '' ) );
			if ( '' !== $key ) { update_option( 'nadlan_smtp_pass', $key, false ); }
			update_option( 'nadlan_mail_from', sanitize_email( wp_unslash( $_POST['mail_from'] ?? '' ) ), false );
			update_option( 'nadlan_mail_from_name', sanitize_text_field( wp_unslash( $_POST['mail_from_name'] ?? '' ) ), false );
			$msg = 'נשמר.';
			if ( '' !== $host && '' !== (string) get_option( 'nadlan_smtp_pass', '' ) ) {
				$msg .= nadlan_smtp_check( true ) ? ' Brevo אישר את ה־Login ואת המפתח. מעכשיו המיילים של האתר יוצאים דרך Brevo.'
					: ' Brevo לא אישר את ה־Login והמפתח (' . (string) ( get_option( 'nadlan_smtp_state' )['err'] ?? '' ) . '). המיילים ממשיכים לצאת דרך שרת האחסון, כך ששום מייל לא הולך לאיבוד. ב־Brevo: Generate a new SMTP key, ולהעתיק את המפתח המלא מהחלון שנפתח מיד אחרי היצירה (רק שם הוא מופיע במלואו), ולהדביק כאן.';
			}
			if ( ! empty( $_POST['send_test'] ) ) {
				$err = null; add_action( 'wp_mail_failed', function ( $e ) use ( &$err ) { $err = $e->get_error_message(); } );
				$ok = wp_mail( get_option( 'admin_email' ), '[נדלן] בדיקת שליחה דרך ' . ( $host ? $host : 'השרת' ), 'אם המייל הזה הגיע לתיבה הראשית, השליחה עובדת. ' . wp_date( 'j.n.Y H:i' ) );
				$msg .= $ok ? ' מייל בדיקה נשלח אל ' . get_option( 'admin_email' ) . '.' : ' השליחה נכשלה: ' . esc_html( (string) $err );
			}
		}
		$v = function ( $k, $d = '' ) { return esc_attr( (string) get_option( $k, $d ) ); };
		$has_key = '' !== (string) get_option( 'nadlan_smtp_pass', '' );
		echo '<div class="wrap" dir="rtl"><h1>מייל יוצא</h1>';
		if ( $msg ) { echo '<div class="notice notice-info"><p>' . esc_html( $msg ) . '</p></div>'; }
		echo '<p>כל המיילים של האתר יוצאים דרך שירות השליחה שמוגדר כאן, במקום דרך שרת האחסון (שמוגבל בכמות ביום). בברבו: Settings › SMTP &amp; API › SMTP. מעתיקים את ה־Login ואת המפתח, ומדביקים כאן.</p>';
		echo '<form method="post">' . wp_nonce_field( 'nadlan_mail', 'nadlan_mail_nonce', true, false ) . '<table class="form-table" role="presentation">';
		echo '<tr><th>שרת</th><td><input name="smtp_host" class="regular-text" dir="ltr" value="' . $v( 'nadlan_smtp_host', 'smtp-relay.brevo.com' ) . '"> <input name="smtp_port" size="4" dir="ltr" value="' . $v( 'nadlan_smtp_port', '587' ) . '"> <select name="smtp_secure"><option value="tls">tls</option><option value="ssl"' . selected( get_option( 'nadlan_smtp_secure', 'tls' ), 'ssl', false ) . '>ssl</option></select><p class="description">להשאיר ריק כדי לחזור לשליחה דרך שרת האחסון.</p></td></tr>';
		echo '<tr><th>Login</th><td><input name="smtp_user" class="regular-text" dir="ltr" autocomplete="off" value="' . $v( 'nadlan_smtp_user' ) . '"></td></tr>';
		echo '<tr><th>מפתח SMTP</th><td><input name="smtp_pass" type="password" class="regular-text" dir="ltr" autocomplete="new-password" value="" placeholder="' . ( $has_key ? 'שמור. השאירו ריק כדי לא לשנות' : 'הדביקו כאן את המפתח' ) . '"></td></tr>';
		echo '<tr><th>כתובת השולח</th><td><input name="mail_from" class="regular-text" dir="ltr" value="' . $v( 'nadlan_mail_from' ) . '" placeholder="info@nad-lan.co.il"><p class="description">כתובת בדומיין שאומת בברבו.</p></td></tr>';
		echo '<tr><th>שם השולח</th><td><input name="mail_from_name" class="regular-text" value="' . $v( 'nadlan_mail_from_name', 'נדלן' ) . '"></td></tr>';
		echo '</table><p><button class="button button-primary">שמירה</button> <button class="button" name="send_test" value="1">שמירה ושליחת מייל בדיקה</button></p></form>';
		$st = (array) get_option( 'nadlan_smtp_state', array() );
		$live = '' !== (string) get_option( 'nadlan_smtp_host', '' ) && $has_key && ! empty( $st['ok'] );
		echo '<p style="font-size:15px">מצב עכשיו: <b style="color:' . ( $live ? '#0F7A63' : '#B42318' ) . '">' . ( $live ? 'שולח דרך ' . esc_html( (string) get_option( 'nadlan_smtp_host' ) ) . ' (המפתח אושר ' . esc_html( wp_date( 'j.n H:i', (int) ( $st['t'] ?? 0 ) ) ) . ')' : 'שולח דרך שרת האחסון' . ( $has_key && ! empty( $st['t'] ) ? '. Brevo לא אישר את המפתח השמור' : '' ) ) . '</b>.</p></div>';
	} );
} );
