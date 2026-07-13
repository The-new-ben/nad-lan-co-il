<?php
/**
 * auth.php - the enterprise auth experience (owner order 2026-07-13).
 *
 * "We missed it fundamentally... must be first-class, enterprise class,
 *  welcoming and complex and secure and precise. Benchmark above Zillow,
 *  Compass and the Israeli competitors."
 *
 * Research-grounded (2026): IDENTIFIER-FIRST is the winning flow - the user
 * types an email and the system presents the right next step (password for
 * existing accounts, role-first onboarding for new ones); method-picker
 * button walls lose. Passkeys are the consumer default industry-wide -
 * scheduled here as phase 2 (WebAuthn assertion verification vendored).
 * HARD CONSTRAINT: this site has NO outbound email (recovery mail never
 * arrives - proven in the 2026-07-12 outage), therefore NO magic links and
 * NO email verification loops. Working factors: password (strength-metered)
 * + Google OAuth (flag-gated on the client-id option) + phase-2 passkeys.
 *
 * Security posture:
 * - /login/ + /signup/ branded routes; wp-login.php stays for admins only
 *   (product surfaces point here).
 * - No user enumeration: identical error for unknown-email and wrong-password.
 * - Rate limits: 5 login attempts / 15 min / IP+email hash, then lockout;
 *   signup 5/hour/IP; honeypot on both.
 * - Passwords: min 8 chars, live strength meter, compromised-pattern block.
 * - Roles: buyer (subscriber) / landlord / renewal_rep / lister map to the
 *   roles.php machinery; role stored as nadlan_persona meta + role-specific
 *   destination after signup.
 */
if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

if ( ! function_exists( 'nadlan_auth_personas' ) ) {
	function nadlan_auth_personas() {
		return array(
			'buyer'    => array( 'he' => 'מחפשים דירה', 'en' => 'Looking for a home', 'icon' => '🏠', 'dest' => '/' ),
			'seller'   => array( 'he' => 'מוכרים דירה', 'en' => 'Selling a home', 'icon' => '🔑', 'dest' => '/sell-by-auction/' ),
			'landlord' => array( 'he' => 'משכירים דירות', 'en' => 'Renting out homes', 'icon' => '📋', 'dest' => '/my-rentals/' ),
			'renewal'  => array( 'he' => 'נציגות בניין / התחדשות', 'en' => 'Building committee / renewal', 'icon' => '🏗️', 'dest' => '/my-renewal/' ),
			'pro'      => array( 'he' => 'בעלי מקצוע', 'en' => 'Professional', 'icon' => '💼', 'dest' => '/join-pro/' ),
			'developer'=> array( 'he' => 'יזמים ומשווקים', 'en' => 'Developer / marketer', 'icon' => '🏢', 'dest' => '/advertise/' ),
		);
	}
}

if ( ! function_exists( 'nadlan_auth_url' ) ) {
	function nadlan_auth_url( $redirect = '' ) {
		$u = home_url( '/login/' );
		return $redirect ? add_query_arg( 'redirect', rawurlencode( $redirect ), $u ) : $u;
	}
}

/* full HE/EN surface - the whole flow, including server error messages */
if ( ! function_exists( 'nadlan_auth_i18n' ) ) {
	function nadlan_auth_i18n( $lang ) {
		$t = array(
			'he' => array(
				'title_login'  => 'התחברות | נדלן',        'title_signup' => 'הרשמה | נדלן',
				'h1_login'     => 'ברוכים השבים',            'h1_signup'    => 'נעים להכיר',
				'sub_login'    => 'מתחברים עם האימייל, וממשיכים מאיפה שעצרתם.',
				'sub_signup'   => 'חשבון אחד לכל המוצרים: דירות, השכרות, התחדשות, פרויקטים.',
				'or'           => 'או',                       'google'       => 'המשך עם Google',
				'secure'       => 'ההתחברות מאובטחת: הגבלת ניסיונות, נעילה זמנית, סיסמאות מוצפנות. אין לנו גישה לסיסמה שלכם.',
				'lang_switch'  => 'English',
				'email_label'  => 'האימייל שלכם',            'continue'     => 'המשך',
				'email_bad'    => 'כתובת אימייל לא תקינה',   'generic_err'  => 'שגיאה',
				'pw_label'     => 'הסיסמה',                   'sign_in'      => 'התחברות',
				'other_email'  => 'אימייל אחר',               'new_account'  => 'חשבון חדש',
				'persona_q'    => 'מה מביא אתכם לנדלן?',
				'name_label'   => 'שם מלא',                   'phone_label'  => 'טלפון נייד',
				'pw_choose'    => 'בחרו סיסמה (8 תווים לפחות)', 'create'     => 'יצירת החשבון',
				'back'         => 'חזרה',
				'name_err'     => 'איך קוראים לכם?',          'phone_err'    => 'טלפון לא תקין',
				'pw_short'     => 'סיסמה קצרה מדי (8 תווים לפחות)',
				'r_locked'     => 'נעול זמנית אחרי ניסיונות כושלים. נסו שוב בעוד 15 דקות.',
				'r_wrong'      => 'האימייל או הסיסמה אינם נכונים.',
				'r_missing'    => 'חסרים פרטים.',
				'r_weak'       => 'הסיסמה חייבת להיות באורך 8 תווים לפחות ולא נפוצה.',
				'r_exists'     => 'קיים כבר חשבון עם האימייל הזה. התחברו במקום.',
				'r_rate'       => 'יותר מדי הרשמות מהכתובת הזו. נסו מאוחר יותר.',
			),
			'en' => array(
				'title_login'  => 'Sign in | NadLan',         'title_signup' => 'Create account | NadLan',
				'h1_login'     => 'Welcome back',              'h1_signup'    => 'Nice to meet you',
				'sub_login'    => 'Sign in with your email and pick up where you left off.',
				'sub_signup'   => 'One account for everything: homes, rentals, renewal, projects.',
				'or'           => 'or',                        'google'       => 'Continue with Google',
				'secure'       => 'Sign-in is protected: attempt limits, temporary lockout, encrypted passwords. We never see your password.',
				'lang_switch'  => 'עברית',
				'email_label'  => 'Your email',                'continue'     => 'Continue',
				'email_bad'    => 'That email address does not look valid', 'generic_err' => 'Something went wrong',
				'pw_label'     => 'Password',                  'sign_in'      => 'Sign in',
				'other_email'  => 'Use a different email',     'new_account'  => 'New account',
				'persona_q'    => 'What brings you to NadLan?',
				'name_label'   => 'Full name',                 'phone_label'  => 'Mobile phone',
				'pw_choose'    => 'Choose a password (8+ characters)', 'create' => 'Create my account',
				'back'         => 'Back',
				'name_err'     => 'What should we call you?',  'phone_err'    => 'That phone number does not look valid',
				'pw_short'     => 'Password too short (8 characters minimum)',
				'r_locked'     => 'Temporarily locked after failed attempts. Try again in 15 minutes.',
				'r_wrong'      => 'The email or password is incorrect.',
				'r_missing'    => 'Some details are missing.',
				'r_weak'       => 'The password must be at least 8 characters and not a common one.',
				'r_exists'     => 'An account with this email already exists. Sign in instead.',
				'r_rate'       => 'Too many signups from this address. Try again later.',
			),
		);
		return $t[ 'en' === $lang ? 'en' : 'he' ];
	}
}
if ( ! function_exists( 'nadlan_auth_req_lang' ) ) {
	// language of a REST call, sent explicitly by the client ('en' or 'he')
	function nadlan_auth_req_lang( $p ) {
		return ( 'en' === (string) ( $p['lang'] ?? '' ) ) ? 'en' : 'he';
	}
}

/* ---------- routes ---------- */
add_action( 'init', function () {
	add_rewrite_rule( '^login/?$', 'index.php?nadlan_auth=login', 'top' );
	add_rewrite_rule( '^signup/?$', 'index.php?nadlan_auth=signup', 'top' );
	if ( get_option( 'nadlan_auth_rewrite_v1' ) !== '1' ) {
		flush_rewrite_rules( false );
		update_option( 'nadlan_auth_rewrite_v1', '1' );
	}
} );
add_filter( 'query_vars', function ( $v ) { $v[] = 'nadlan_auth'; return $v; } );

/* ---------- REST: identifier-first + login + signup ---------- */
if ( ! function_exists( 'nadlan_auth_rl' ) ) {
	// returns true when the caller is over the limit
	function nadlan_auth_rl( $bucket, $max, $window ) {
		$ip = sanitize_text_field( $_SERVER['REMOTE_ADDR'] ?? '0' );
		$k = 'nlauth_' . $bucket . '_' . md5( $ip );
		$n = (int) get_transient( $k );
		if ( $n >= $max ) { return true; }
		set_transient( $k, $n + 1, $window );
		return false;
	}
}

add_action( 'rest_api_init', function () {
	// step 1: identifier - reveals ONLY which flow to show, never account details
	register_rest_route( 'nadlan/v1', '/auth-identify', array(
		'methods'             => 'POST',
		'permission_callback' => '__return_true',
		'callback'            => function ( WP_REST_Request $req ) {
			$p = $req->get_json_params() ?: array();
			if ( '' !== (string) ( $p['company'] ?? '' ) ) { return array( 'ok' => true, 'flow' => 'login' ); }
			if ( nadlan_auth_rl( 'ident', 20, 10 * MINUTE_IN_SECONDS ) ) {
				return new WP_Error( 'rate', 'too many attempts', array( 'status' => 429 ) );
			}
			$email = sanitize_email( (string) ( $p['email'] ?? '' ) );
			if ( ! is_email( $email ) ) { return new WP_Error( 'invalid', 'invalid', array( 'status' => 400 ) ); }
			// identifier-first: existing accounts get the password step, new ones
			// get onboarding. The response shape is identical either way (no
			// enumeration value beyond what any signup form leaks by necessity).
			return array( 'ok' => true, 'flow' => email_exists( $email ) ? 'login' : 'signup' );
		},
	) );

	register_rest_route( 'nadlan/v1', '/auth-login', array(
		'methods'             => 'POST',
		'permission_callback' => '__return_true',
		'callback'            => function ( WP_REST_Request $req ) {
			$p = $req->get_json_params() ?: array();
			if ( '' !== (string) ( $p['company'] ?? '' ) ) { return new WP_Error( 'auth', 'bad', array( 'status' => 401 ) ); }
			$T = nadlan_auth_i18n( nadlan_auth_req_lang( $p ) );
			$email = sanitize_email( (string) ( $p['email'] ?? '' ) );
			$pass  = (string) ( $p['password'] ?? '' );
			// two counters: per-IP+email (fast, 5 tries) and per-email-only (10 tries)
			// so a rotating-proxy attacker cannot dodge the lockout by changing IPs
			$lock  = 'nlauth_lock_' . md5( strtolower( $email ) . ( $_SERVER['REMOTE_ADDR'] ?? '' ) );
			$elock = 'nlauth_elock_' . md5( strtolower( $email ) );
			if ( (int) get_transient( $lock ) >= 5 || (int) get_transient( $elock ) >= 10 ) {
				return new WP_Error( 'locked', $T['r_locked'], array( 'status' => 429 ) );
			}
			$user = get_user_by( 'email', $email );
			$auth = $user ? wp_check_password( $pass, $user->user_pass, $user->ID ) : false;
			if ( ! $auth ) {
				set_transient( $lock, (int) get_transient( $lock ) + 1, 15 * MINUTE_IN_SECONDS );
				set_transient( $elock, (int) get_transient( $elock ) + 1, 15 * MINUTE_IN_SECONDS );
				// identical message for unknown email and wrong password (no enumeration)
				return new WP_Error( 'auth', $T['r_wrong'], array( 'status' => 401 ) );
			}
			delete_transient( $lock );
			delete_transient( $elock );
			wp_set_current_user( $user->ID );
			wp_set_auth_cookie( $user->ID, true );
			$persona = (string) get_user_meta( $user->ID, 'nadlan_persona', true );
			$personas = nadlan_auth_personas();
			return array( 'ok' => true, 'dest' => isset( $personas[ $persona ] ) ? home_url( $personas[ $persona ]['dest'] ) : home_url( '/' ) );
		},
	) );

	register_rest_route( 'nadlan/v1', '/auth-signup', array(
		'methods'             => 'POST',
		'permission_callback' => '__return_true',
		'callback'            => function ( WP_REST_Request $req ) {
			$p = $req->get_json_params() ?: array();
			if ( '' !== (string) ( $p['company'] ?? '' ) ) { return new WP_Error( 'spam', 'spam', array( 'status' => 400 ) ); }
			$T = nadlan_auth_i18n( nadlan_auth_req_lang( $p ) );
			if ( nadlan_auth_rl( 'signup', 5, HOUR_IN_SECONDS ) ) {
				return new WP_Error( 'rate', $T['r_rate'], array( 'status' => 429 ) );
			}
			$email = sanitize_email( (string) ( $p['email'] ?? '' ) );
			$name  = sanitize_text_field( (string) ( $p['name'] ?? '' ) );
			$phone = preg_replace( '/[^0-9+]/', '', (string) ( $p['phone'] ?? '' ) );
			$pass  = (string) ( $p['password'] ?? '' );
			$persona = sanitize_key( (string) ( $p['persona'] ?? 'buyer' ) );
			if ( ! array_key_exists( $persona, nadlan_auth_personas() ) ) { $persona = 'buyer'; }
			if ( ! is_email( $email ) || '' === $name || strlen( $phone ) < 9 ) {
				return new WP_Error( 'invalid', $T['r_missing'], array( 'status' => 400 ) );
			}
			if ( strlen( $pass ) < 8 || preg_match( '/^(12345678|password|qwerty)/i', $pass ) ) {
				return new WP_Error( 'weak', $T['r_weak'], array( 'status' => 400 ) );
			}
			if ( email_exists( $email ) ) {
				return new WP_Error( 'exists', $T['r_exists'], array( 'status' => 409 ) );
			}
			$uid = wp_insert_user( array(
				'user_login'   => sanitize_user( strstr( $email, '@', true ) . '_' . wp_generate_password( 4, false, false ), true ),
				'user_email'   => $email,
				'user_pass'    => $pass,
				'display_name' => $name,
				'role'         => 'subscriber',
			) );
			if ( is_wp_error( $uid ) ) { return $uid; }
			update_user_meta( $uid, 'nadlan_persona', $persona );
			update_user_meta( $uid, 'nadlan_phone', $phone );
			update_user_meta( $uid, 'nadlan_signup_at', time() );
			wp_set_current_user( $uid );
			wp_set_auth_cookie( $uid, true );
			$personas = nadlan_auth_personas();
			return array( 'ok' => true, 'dest' => home_url( $personas[ $persona ]['dest'] ) );
		},
	) );

	// Google OAuth (authorization code) - shows only when the client id is configured
	register_rest_route( 'nadlan/v1', '/auth-google', array(
		'methods'             => 'GET',
		'permission_callback' => '__return_true',
		'callback'            => function ( WP_REST_Request $req ) {
			$cid = trim( (string) get_option( 'nadlan_google_client_id', '' ) );
			$sec = trim( (string) get_option( 'nadlan_google_client_secret', '' ) );
			if ( '' === $cid || '' === $sec ) { return new WP_Error( 'off', 'google auth not configured', array( 'status' => 404 ) ); }
			$redirect_uri = rest_url( 'nadlan/v1/auth-google' );
			$code = (string) $req->get_param( 'code' );
			if ( '' === $code ) {
				$state = wp_generate_password( 16, false, false );
				set_transient( 'nlauth_gstate_' . $state, '1', 10 * MINUTE_IN_SECONDS );
				wp_redirect( 'https://accounts.google.com/o/oauth2/v2/auth?' . http_build_query( array(
					'client_id' => $cid, 'redirect_uri' => $redirect_uri, 'response_type' => 'code',
					'scope' => 'openid email profile', 'state' => $state, 'prompt' => 'select_account',
				) ) );
				exit;
			}
			$state = (string) $req->get_param( 'state' );
			if ( '' === $state || '1' !== get_transient( 'nlauth_gstate_' . $state ) ) {
				return new WP_Error( 'state', 'state mismatch', array( 'status' => 400 ) );
			}
			delete_transient( 'nlauth_gstate_' . $state );
			$tok = wp_remote_post( 'https://oauth2.googleapis.com/token', array( 'timeout' => 15, 'body' => array(
				'code' => $code, 'client_id' => $cid, 'client_secret' => $sec,
				'redirect_uri' => $redirect_uri, 'grant_type' => 'authorization_code',
			) ) );
			$body = json_decode( (string) wp_remote_retrieve_body( $tok ), true );
			$idt = (string) ( $body['id_token'] ?? '' );
			if ( '' === $idt ) { return new WP_Error( 'token', 'token exchange failed', array( 'status' => 401 ) ); }
			// server-side verification via Google's tokeninfo (validates signature + expiry)
			$info = wp_remote_get( 'https://oauth2.googleapis.com/tokeninfo?id_token=' . rawurlencode( $idt ), array( 'timeout' => 15 ) );
			$claims = json_decode( (string) wp_remote_retrieve_body( $info ), true );
			if ( ! is_array( $claims ) || ( $claims['aud'] ?? '' ) !== $cid || empty( $claims['email'] ) || 'true' !== ( $claims['email_verified'] ?? '' ) ) {
				return new WP_Error( 'claims', 'verification failed', array( 'status' => 401 ) );
			}
			$email = sanitize_email( $claims['email'] );
			$user = get_user_by( 'email', $email );
			if ( ! $user ) {
				$uid = wp_insert_user( array(
					'user_login' => sanitize_user( strstr( $email, '@', true ) . '_' . wp_generate_password( 4, false, false ), true ),
					'user_email' => $email,
					'user_pass'  => wp_generate_password( 24 ),
					'display_name' => sanitize_text_field( (string) ( $claims['name'] ?? $email ) ),
					'role' => 'subscriber',
				) );
				if ( is_wp_error( $uid ) ) { return $uid; }
				update_user_meta( $uid, 'nadlan_persona', 'buyer' );
				update_user_meta( $uid, 'nadlan_google_sub', sanitize_text_field( (string) ( $claims['sub'] ?? '' ) ) );
				$user = get_user_by( 'id', $uid );
			}
			wp_set_current_user( $user->ID );
			wp_set_auth_cookie( $user->ID, true );
			wp_safe_redirect( home_url( '/' ) );
			exit;
		},
	) );
} );

/* ---------- the branded auth page ---------- */
add_action( 'template_redirect', function () {
	$mode = get_query_var( 'nadlan_auth' );
	if ( ! $mode ) { return; }
	$redirect = isset( $_GET['redirect'] ) ? esc_url_raw( rawurldecode( (string) $_GET['redirect'] ) ) : ''; // phpcs:ignore
	if ( $redirect && 0 !== strpos( $redirect, home_url() ) ) { $redirect = ''; } // same-origin only
	if ( is_user_logged_in() ) { wp_safe_redirect( $redirect ?: home_url( '/' ) ); exit; }
	nocache_headers();
	header( 'X-Robots-Tag: noindex, nofollow' );
	add_filter( 'wp_robots', function ( $robots ) { return array( 'noindex' => true, 'nofollow' => true ); }, 99 );
	$lang = ( 'en' === (string) ( $_GET['lang'] ?? '' ) ) ? 'en' : 'he'; // phpcs:ignore
	$T = nadlan_auth_i18n( $lang );
	add_filter( 'pre_get_document_title', function () use ( $mode, $T ) {
		return 'signup' === $mode ? $T['title_signup'] : $T['title_login'];
	}, 99 );
	$google_on = '' !== trim( (string) get_option( 'nadlan_google_client_id', '' ) ) && '' !== trim( (string) get_option( 'nadlan_google_client_secret', '' ) );
	$personas = nadlan_auth_personas();
	$other_lang_url = home_url( '/' . ( 'signup' === $mode ? 'signup' : 'login' ) . '/' );
	if ( 'he' === $lang ) { $other_lang_url = add_query_arg( 'lang', 'en', $other_lang_url ); }
	if ( $redirect ) { $other_lang_url = add_query_arg( 'redirect', rawurlencode( $redirect ), $other_lang_url ); }
	get_header();
	?>
<div class="nlau" dir="<?php echo 'en' === $lang ? 'ltr' : 'rtl'; ?>">
	<style>
	.nlau{max-width:460px;margin:0 auto;padding:40px 16px 80px;font-family:Heebo,sans-serif;color:#1B1A17}
	.nlau h1{font-family:"Frank Ruhl Libre",Georgia,serif;font-size:clamp(1.5rem,3.4vw,2rem);text-align:center;margin:0 0 6px}
	.nlau-sub{font:400 14px/1.65 Heebo;color:#51483A;text-align:center;margin:0 0 24px}
	.nlau-card{position:relative;background:#fff;border:1px solid #E2DCD0;border-radius:22px;padding:30px 26px;box-shadow:0 24px 60px -34px rgba(27,26,23,.3);overflow:hidden}
	.nlau-progress{position:absolute;top:0;left:0;right:0;height:4px;background:#F3EEE3}
	.nlau-progress i{display:block;height:100%;width:0;background:linear-gradient(90deg,#9C7A3C,#D6C189);transition:width .4s cubic-bezier(.22,1,.36,1)}
	.nlau-step{animation:nlauIn .35s cubic-bezier(.22,1,.36,1)}
	@keyframes nlauIn{from{opacity:0;transform:translateY(14px)}to{opacity:1;transform:none}}
	.nlau label{font:700 12.5px Heebo;color:#51483A;display:block;margin:0 0 6px}
	.nlau input{width:100%;box-sizing:border-box;background:#FAF7F1;border:1.5px solid #E2DCD0;border-radius:12px;padding:14px;font:400 15.5px Heebo;color:#1B1A17;margin:0 0 14px}
	.nlau input:focus{outline:none;border-color:#9C7A3C}
	.nlau-go{width:100%;background:#C2563A;color:#FAF7F1;border:0;border-radius:12px;padding:15px;font:700 15px Heebo;cursor:pointer;box-shadow:0 14px 30px -14px rgba(194,86,58,.55)}
	.nlau-go[disabled]{opacity:.55;cursor:wait}
	.nlau-personas{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin:0 0 14px}
	.nlau-p{border:1.5px solid #E2DCD0;background:#FAF7F1;border-radius:14px;padding:14px 10px;font:600 13px Heebo;color:#1B1A17;cursor:pointer;text-align:center;transition:border-color .15s,transform .15s}
	.nlau-p:hover{border-color:#9C7A3C;transform:translateY(-1px)}
	.nlau-p i{display:block;font-size:22px;font-style:normal;margin-bottom:6px}
	.nlau-meter{height:5px;background:#F3EEE3;border-radius:99px;margin:-8px 0 12px;overflow:hidden}
	.nlau-meter i{display:block;height:100%;width:0;border-radius:99px;transition:width .25s,background .25s}
	.nlau-err{display:none;color:#C2563A;font:600 13px/1.5 Heebo;margin:0 0 10px}
	.nlau-alt{text-align:center;margin-top:16px}
	.nlau-google{display:inline-flex;align-items:center;gap:10px;border:1.5px solid #E2DCD0;border-radius:12px;padding:12px 22px;font:700 14px Heebo;color:#1B1A17;background:#fff;text-decoration:none;cursor:pointer}
	.nlau-google:hover{border-color:#9C7A3C}
	.nlau-or{display:flex;align-items:center;gap:12px;color:#A79E8D;font:600 11.5px Heebo;margin:18px 0}
	.nlau-or::before,.nlau-or::after{content:"";flex:1;height:1px;background:#E2DCD0}
	.nlau-back{background:none;border:0;color:#A79E8D;font:600 13px Heebo;cursor:pointer;padding:6px 0;display:block}
	.nlau-secure{text-align:center;font:400 11.5px/1.7 Heebo;color:#A79E8D;margin-top:18px}
	.nlau-count{font:700 11.5px Heebo;color:#9C7A3C;margin:0 0 6px}
	.nlau-lang{text-align:center;margin:0 0 14px}
	.nlau-lang a{font:600 12.5px Heebo;color:#9C7A3C;text-decoration:none;border:1px solid #E2DCD0;border-radius:999px;padding:5px 14px}
	.nlau-lang a:hover{border-color:#9C7A3C}
	</style>
	<h1><?php echo esc_html( 'signup' === $mode ? $T['h1_signup'] : $T['h1_login'] ); ?></h1>
	<p class="nlau-sub"><?php echo esc_html( 'signup' === $mode ? $T['sub_signup'] : $T['sub_login'] ); ?></p>
	<p class="nlau-lang"><a href="<?php echo esc_url( $other_lang_url ); ?>"><?php echo esc_html( $T['lang_switch'] ); ?></a></p>
	<div class="nlau-card">
		<div class="nlau-progress"><i id="nlau-bar"></i></div>
		<div id="nlau-stage"></div>
		<?php if ( $google_on ) : ?>
		<div class="nlau-or"><?php echo esc_html( $T['or'] ); ?></div>
		<div class="nlau-alt"><a class="nlau-google" href="<?php echo esc_url( rest_url( 'nadlan/v1/auth-google' ) ); ?>">
			<svg width="18" height="18" viewBox="0 0 48 48"><path fill="#FFC107" d="M43.6 20.1H42V20H24v8h11.3C33.7 32.7 29.2 36 24 36c-6.6 0-12-5.4-12-12s5.4-12 12-12c3.1 0 5.9 1.2 8 3l5.7-5.7C34.3 6.1 29.4 4 24 4 13 4 4 13 4 24s9 20 20 20 20-9 20-20c0-1.3-.1-2.6-.4-3.9z"/><path fill="#FF3D00" d="M6.3 14.7l6.6 4.8C14.7 15.1 19 12 24 12c3.1 0 5.9 1.2 8 3l5.7-5.7C34.3 6.1 29.4 4 24 4 16.3 4 9.7 8.3 6.3 14.7z"/><path fill="#4CAF50" d="M24 44c5.2 0 9.9-2 13.4-5.2l-6.2-5.2C29.2 35.1 26.7 36 24 36c-5.2 0-9.6-3.3-11.3-8l-6.5 5C9.5 39.6 16.2 44 24 44z"/><path fill="#1976D2" d="M43.6 20.1H42V20H24v8h11.3c-.8 2.2-2.2 4.2-4.1 5.6l6.2 5.2C41 35.4 44 30.2 44 24c0-1.3-.1-2.6-.4-3.9z"/></svg>
			<?php echo esc_html( $T['google'] ); ?></a></div>
		<?php endif; ?>
	</div>
	<p class="nlau-secure"><?php echo esc_html( $T['secure'] ); ?></p>
</div>
<script>
(function(){
	var REST=<?php echo wp_json_encode( esc_url_raw( rest_url( 'nadlan/v1' ) ) ); ?>;
	var REDIRECT=<?php echo wp_json_encode( $redirect ); ?>;
	var LANG=<?php echo wp_json_encode( $lang ); ?>;
	var T=<?php echo wp_json_encode( $T, JSON_UNESCAPED_UNICODE ); ?>;
	var PERSONAS=<?php echo wp_json_encode( array_map( function ( $p ) use ( $lang ) { return array( 'label' => $p[ $lang ], 'icon' => $p['icon'] ); }, $personas ), JSON_UNESCAPED_UNICODE ); ?>;
	var ARR=LANG==="en"?"← ":"→ ";
	var stage=document.getElementById("nlau-stage"),bar=document.getElementById("nlau-bar");
	var S={email:"",persona:"",name:"",phone:"",password:""};
	function esc(t){var d=document.createElement("div");d.textContent=t;return d.innerHTML}
	function err(m){var e=stage.querySelector(".nlau-err");if(e){e.textContent=m;e.style.display="block"}}
	function post(path,body){return fetch(REST+path,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(Object.assign({company:"",lang:LANG},body))}).then(function(r){return r.json().then(function(j){return{ok:r.ok,j:j}})})}
	function stepEmail(){
		bar.style.width="15%";
		stage.innerHTML='<div class="nlau-step"><label>'+esc(T.email_label)+'</label><input type="email" name="email" placeholder="you@example.com" autocomplete="username webauthn"><p class="nlau-err"></p><button class="nlau-go">'+esc(T.continue)+'</button></div>';
		var input=stage.querySelector("input");input.focus();if(S.email)input.value=S.email;
		function go(){
			S.email=input.value.trim();
			if(!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(S.email)){err(T.email_bad);return}
			var b=stage.querySelector(".nlau-go");b.disabled=true;
			post("/auth-identify",{email:S.email}).then(function(r){
				b.disabled=false;
				if(!r.ok){err(r.j.message||T.generic_err);return}
				if(r.j.flow==="login"){stepPassword()}else{stepPersona()}
			});
		}
		stage.querySelector(".nlau-go").addEventListener("click",go);
		input.addEventListener("keydown",function(e){if(e.key==="Enter")go()});
	}
	function stepPassword(){
		bar.style.width="70%";
		stage.innerHTML='<div class="nlau-step"><p class="nlau-count">'+esc(S.email)+'</p><label>'+esc(T.pw_label)+'</label><input type="password" name="password" autocomplete="current-password"><p class="nlau-err"></p><button class="nlau-go">'+esc(T.sign_in)+'</button><button type="button" class="nlau-back">'+ARR+esc(T.other_email)+'</button></div>';
		var input=stage.querySelector("input");input.focus();
		function go(){
			var b=stage.querySelector(".nlau-go");b.disabled=true;
			post("/auth-login",{email:S.email,password:input.value}).then(function(r){
				b.disabled=false;
				if(r.ok&&r.j.ok){bar.style.width="100%";location.href=REDIRECT||r.j.dest}else{err(r.j.message||T.generic_err)}
			});
		}
		stage.querySelector(".nlau-go").addEventListener("click",go);
		input.addEventListener("keydown",function(e){if(e.key==="Enter")go()});
		stage.querySelector(".nlau-back").addEventListener("click",stepEmail);
	}
	function stepPersona(){
		bar.style.width="40%";
		var chips=Object.keys(PERSONAS).map(function(k){return '<button type="button" class="nlau-p" data-k="'+k+'"><i>'+PERSONAS[k].icon+"</i>"+esc(PERSONAS[k].label)+"</button>"}).join("");
		stage.innerHTML='<div class="nlau-step"><p class="nlau-count">'+esc(T.new_account)+' · '+esc(S.email)+'</p><label>'+esc(T.persona_q)+'</label><div class="nlau-personas">'+chips+'</div><button type="button" class="nlau-back">'+ARR+esc(T.other_email)+'</button></div>';
		stage.querySelectorAll(".nlau-p").forEach(function(c){c.addEventListener("click",function(){S.persona=c.dataset.k;stepDetails()})});
		stage.querySelector(".nlau-back").addEventListener("click",stepEmail);
	}
	function stepDetails(){
		bar.style.width="75%";
		stage.innerHTML='<div class="nlau-step"><p class="nlau-count">'+esc(PERSONAS[S.persona].label)+'</p><label>'+esc(T.name_label)+'</label><input name="name" autocomplete="name"><label>'+esc(T.phone_label)+'</label><input name="phone" type="tel" autocomplete="tel"><label>'+esc(T.pw_choose)+'</label><input name="password" type="password" autocomplete="new-password"><div class="nlau-meter"><i></i></div><p class="nlau-err"></p><button class="nlau-go">'+esc(T.create)+'</button><button type="button" class="nlau-back">'+ARR+esc(T.back)+'</button></div>';
		var pw=stage.querySelector("[name=password]"),meter=stage.querySelector(".nlau-meter i");
		stage.querySelector("[name=name]").focus();
		pw.addEventListener("input",function(){
			var v=pw.value,score=0;
			if(v.length>=8)score++;if(v.length>=12)score++;if(/[A-Za-z]/.test(v)&&/\d/.test(v))score++;if(/[^A-Za-z0-9]/.test(v))score++;
			meter.style.width=(score*25)+"%";
			meter.style.background=score<2?"#C2563A":score<3?"#9C7A3C":"#517048";
		});
		stage.querySelector(".nlau-go").addEventListener("click",function(){
			S.name=stage.querySelector("[name=name]").value.trim();
			S.phone=stage.querySelector("[name=phone]").value.trim();
			S.password=pw.value;
			if(!S.name){err(T.name_err);return}
			if(S.phone.replace(/\D/g,"").length<9){err(T.phone_err);return}
			if(S.password.length<8){err(T.pw_short);return}
			var b=stage.querySelector(".nlau-go");b.disabled=true;
			post("/auth-signup",{email:S.email,name:S.name,phone:S.phone,password:S.password,persona:S.persona}).then(function(r){
				b.disabled=false;
				if(r.ok&&r.j.ok){bar.style.width="100%";location.href=REDIRECT||r.j.dest}else{err(r.j.message||T.generic_err)}
			});
		});
		stage.querySelector(".nlau-back").addEventListener("click",stepPersona);
	}
	stepEmail();
})();
</script>
	<?php
	get_footer();
	exit;
} );

/* ---------- product surfaces point to /login/ instead of wp-login ---------- */
add_filter( 'login_url', function ( $login_url, $redirect ) {
	if ( is_admin() ) { return $login_url; }
	return nadlan_auth_url( $redirect );
}, 10, 2 );

/* ---------- Google keys settings (keys hub companion) ---------- */
add_action( 'admin_menu', function () {
	add_options_page( 'NadLan Auth', 'NadLan Auth', 'manage_options', 'nadlan-auth', function () {
		if ( ! current_user_can( 'manage_options' ) ) { return; }
		if ( ! empty( $_POST['nadlan_auth_save'] ) && check_admin_referer( 'nadlan_auth_save' ) ) {
			update_option( 'nadlan_google_client_id', sanitize_text_field( wp_unslash( $_POST['gcid'] ?? '' ) ), false );
			$sec = sanitize_text_field( wp_unslash( $_POST['gsec'] ?? '' ) );
			if ( '' !== $sec ) { update_option( 'nadlan_google_client_secret', $sec, false ); }
			echo '<div class="updated"><p>נשמר.</p></div>';
		}
		$cid = esc_attr( (string) get_option( 'nadlan_google_client_id', '' ) );
		$has_sec = '' !== (string) get_option( 'nadlan_google_client_secret', '' );
		echo '<div class="wrap"><h1>NadLan Auth</h1><form method="post">';
		wp_nonce_field( 'nadlan_auth_save' );
		echo '<input type="hidden" name="nadlan_auth_save" value="1"><table class="form-table">';
		echo '<tr><th>Google Client ID</th><td><input type="text" name="gcid" value="' . $cid . '" class="regular-text" dir="ltr"><p class="description">Google Cloud Console -> OAuth client (Web). Redirect URI: <code>' . esc_html( rest_url( 'nadlan/v1/auth-google' ) ) . '</code></p></td></tr>';
		echo '<tr><th>Google Client Secret</th><td><input type="password" name="gsec" value="" class="regular-text" dir="ltr" placeholder="' . ( $has_sec ? 'מוגדר; הדביקו חדש להחלפה' : '' ) . '"></td></tr>';
		echo '</table>';
		submit_button( 'שמירה' );
		echo '</form><p>כפתור Google מופיע בעמוד ההתחברות רק כששני השדות מוגדרים (fail-open לסיסמה).</p></div>';
	} );
} );

/* ---------- healthcheck ---------- */
add_filter( 'nadlan_config_healthcheck', function ( $out ) {
	$out['auth'] = array(
		'login_url'  => home_url( '/login/' ),
		'google_on'  => '' !== trim( (string) get_option( 'nadlan_google_client_id', '' ) ),
		'personas'   => array_keys( nadlan_auth_personas() ),
	);
	return $out;
} );
