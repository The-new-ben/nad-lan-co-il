<?php
/**
 * nadlan-config - International campaign brief (v1.1.0, 7.11.2026, LOCAL, not live; 1.1.0: first-payment mode).
 *
 * Ben, 7.11.2026: a developer builds a campaign to sell a project to buyers abroad and in the diaspora in the planner
 * [nadlan_tool id="nlcamp"] (assets/instruments/tools/nlcamp.js), sees the plan and the price, and pays an annual subscription
 * before launch. This file is the server side of that planner and nothing more:
 *  - POST /wp-json/nadlan/v1/campaign-brief: the brief is checked field by field again (allow lists, the budget range and step,
 *    the split, the plan against the number of markets, contact fields, consent), saved as a PRIVATE post of the type
 *    nadlan_camp_brief (no public URL, not in REST, not in search), mailed to the site admin, and answered with a reference id
 *    (NLC-yymmdd-XXXX). Abuse guards without a nonce (the page is cached by the host, a nonce would go stale): a honeypot field,
 *    a minimum fill time, an Origin check, a body size cap, 5 briefs an hour per visitor and 60 a day for the site.
 *  - Why not an existing route: advertiser-orders.php and advertiser-center.php have no public route for a brief (only
 *    WooCommerce hooks and the admin lead status), and the public /lead route of conversion-cta.php files a BUYER lead, which
 *    starts the lead routing and the buyer nurture mails (lead-e2e / lead-nurture): wrong for a developer's order. Payment stays
 *    the shop's own WooCommerce + Morning checkout ("not a fifth payment system"): this file only stores the brief and prints the
 *    product links the planner opens.
 *  - window.NLCAMP_CONFIG before tools/nlcamp.js on pages that carry the tool: the REST address, the privacy page, the product
 *    link of each plan and its first payment. Products (hidden in the shop, 7.11.2026): full plans 8809 / 8810 / 8811 (36,000 /
 *    72,000 / 144,000), first payments of 18,000: 8822 / 8823 / 8824. The options nadlan_cb_product_one / _three / _flag hold the
 *    product the buyer is sent to; unset, the first-payment products 8822 / 8823 / 8824 (so the release needs no option write);
 *    0 = no product (the planner then says a payment link is sent the same day).
 *  - First-payment mode (Morning's terminal takes one charge of up to about 20,000; 25,000 is refused, tested 7.11): the option
 *    nadlan_cb_first_amount (default 18,000) is printed as firstPay of every plan it is below; the planner's button then pays that
 *    first part and says the rest is paid in parts of up to that amount through links we send. 0 = the full plan in one charge
 *    (set it to 0 and the products to 8809 / 8810 / 8811 once Morning raises the cap).
 *  - nadlan_cb_summary( $lang ): the plain summary the shortcode prints before the script runs (called from nadlan_nli_summary()).
 * Prices: the approved annual plans, ad spend separate and paid by the developer straight to the channels. No VAT wording
 * anywhere (the billing entity's VAT status is open). Language: no tech words, no long dashes.
 * Loaded from the module list of nadlan-config.php ('campaign-brief'), see the release note in
 * docs/research/2026-11-07-campaign-network/build/build-nlcamp/registry.php.txt.
 */
if ( ! defined( 'ABSPATH' ) ) { exit; }
if ( defined( 'NADLAN_CB_VERSION' ) ) { return; }
define( 'NADLAN_CB_VERSION', '1.1.0' );

if ( ! function_exists( 'nadlan_cb_plans' ) ) {
	/** The approved annual plans (Ben 7.11.2026). markets: how many the plan carries, 0 = no limit. product: WooCommerce id or 0. */
	function nadlan_cb_plans() {
		return apply_filters( 'nadlan_cb_plans', array(
			'one'   => array( 'he' => 'שוק אחד', 'en' => 'One market', 'price' => 36000, 'markets' => 1, 'product' => nadlan_cb_product_opt( 'one', 8822 ) ),
			'three' => array( 'he' => 'שלושה שווקים', 'en' => 'Three markets', 'price' => 72000, 'markets' => 3, 'product' => nadlan_cb_product_opt( 'three', 8823 ) ),
			'flag'  => array( 'he' => 'פרויקט דגל', 'en' => 'Flagship', 'price' => 144000, 'markets' => 0, 'product' => nadlan_cb_product_opt( 'flag', 8824 ) ),
		) );
	}
	/** The product a plan sends the buyer to: the option when it is set (0 = none), else the first-payment product of 7.11.2026. */
	function nadlan_cb_product_opt( $k, $default ) {
		$v = get_option( 'nadlan_cb_product_' . $k, false );
		return ( false === $v || '' === $v || null === $v ) ? (int) $default : max( 0, (int) $v );
	}
	/** The first charge (Morning takes up to about 20,000 in one charge): the option, default 18,000; 0 = the full plan at once. */
	function nadlan_cb_first_amount() {
		$v = get_option( 'nadlan_cb_first_amount', false );
		return ( false === $v || '' === $v || null === $v ) ? 18000 : max( 0, (int) $v );
	}
	/** The first payment of one plan, or null when the plan is paid in one charge (the option 0, or not below the price). */
	function nadlan_cb_first_pay( $plan ) {
		$f = nadlan_cb_first_amount();
		return $f > 0 && $f < (int) $plan['price'] ? $f : null;
	}

	/** Markets and communities: id => languages and names (the same list and order as NLCAMP.MARKETS). */
	function nadlan_cb_markets() {
		return array(
			'fr'   => array( 'langs' => array( 'fr' ), 'he' => 'צרפת', 'en' => 'France' ),
			'us'   => array( 'langs' => array( 'en' ), 'he' => 'ארצות הברית', 'en' => 'USA' ),
			'uk'   => array( 'langs' => array( 'en' ), 'he' => 'בריטניה', 'en' => 'UK' ),
			'ca'   => array( 'langs' => array( 'en', 'fr' ), 'he' => 'קנדה', 'en' => 'Canada' ),
			'be'   => array( 'langs' => array( 'fr' ), 'he' => 'בלגיה', 'en' => 'Belgium' ),
			'ch'   => array( 'langs' => array( 'fr' ), 'he' => 'שווייץ', 'en' => 'Switzerland' ),
			'za'   => array( 'langs' => array( 'en' ), 'he' => 'דרום אפריקה', 'en' => 'South Africa' ),
			'au'   => array( 'langs' => array( 'en' ), 'he' => 'אוסטרליה', 'en' => 'Australia' ),
			'ru'   => array( 'langs' => array( 'ru' ), 'he' => 'דוברי רוסית', 'en' => 'Russian speakers' ),
			'olim' => array( 'langs' => array( 'en', 'fr', 'ru' ), 'he' => 'עולים חדשים בישראל', 'en' => 'Olim in Israel' ),
		);
	}
	function nadlan_cb_langs() { return array( 'en' => array( 'he' => 'אנגלית', 'en' => 'English' ), 'fr' => array( 'he' => 'צרפתית', 'en' => 'French' ), 'ru' => array( 'he' => 'רוסית', 'en' => 'Russian' ) ); }
	function nadlan_cb_buyers() {
		return array(
			'home'    => array( 'he' => 'בית בישראל לעלייה או לחופשות', 'en' => 'A home in Israel for aliyah or holidays' ),
			'invest'  => array( 'he' => 'משקיעים, להשכרה', 'en' => 'Investors (rental)' ),
			'parents' => array( 'he' => 'הורים לילדים שגרים בישראל', 'en' => 'Parents of children living in Israel' ),
			'luxury'  => array( 'he' => 'יוקרה: פנטהאוזים ודירות גן', 'en' => 'Luxury: penthouses and garden apartments' ),
		);
	}
	function nadlan_cb_channels() { return array( 'meta' => 'Meta', 'google' => 'Google', 'press' => 'עיתונות קהילתית וניוזלטרים', 'boards' => 'אתרי נדלן בינלאומיים' ); }
	function nadlan_cb_budget() { return array( 'min' => 3000, 'max' => 60000, 'step' => 1000 ); }
	function nadlan_cb_kinds() { return array( 'new' => 'פרויקט חדש', 'existing' => 'פרויקט שכבר יש לו עמוד בנדלן' ); }

	/** The languages a set of markets implies, in the fixed order en, fr, ru. */
	function nadlan_cb_langs_of( $markets ) {
		$all = nadlan_cb_markets(); $on = array();
		foreach ( (array) $markets as $m ) { if ( isset( $all[ $m ] ) ) { foreach ( $all[ $m ]['langs'] as $l ) { $on[ $l ] = 1; } } }
		return array_values( array_filter( array_keys( nadlan_cb_langs() ), function ( $l ) use ( $on ) { return isset( $on[ $l ] ); } ) );
	}

	/** The plan the planner recommends for n markets: 1 one, 2-3 three, 4+ flagship. */
	function nadlan_cb_recommend( $n ) { return $n >= 4 ? 'flag' : ( $n >= 2 ? 'three' : ( 1 === $n ? 'one' : '' ) ); }

	function nadlan_cb_len( $s ) { return function_exists( 'mb_strlen' ) ? mb_strlen( $s, 'UTF-8' ) : strlen( $s ); }
	function nadlan_cb_cut( $s, $n ) { return function_exists( 'mb_substr' ) ? mb_substr( $s, 0, $n, 'UTF-8' ) : substr( $s, 0, $n ); }
	function nadlan_cb_bad( $field, $msg ) { return new WP_Error( 'nlc_invalid', $msg, array( 'status' => 400, 'field' => $field ) ); }

	/**
	 * Every field of a brief, checked again on the server. Returns the clean brief, or a WP_Error naming the first bad field.
	 * Nothing the browser computed is trusted: the languages, the yearly budget and the plan price are computed here.
	 */
	function nadlan_cb_clean( $p ) {
		if ( ! is_array( $p ) ) { return nadlan_cb_bad( '', 'Bad request.' ); }
		$mk = nadlan_cb_markets(); $plans = nadlan_cb_plans(); $bud = nadlan_cb_budget();
		$ask = array_map( 'sanitize_key', array_map( 'strval', array_slice( (array) ( $p['markets'] ?? array() ), 0, 20 ) ) );
		$markets = array_values( array_filter( array_keys( $mk ), function ( $id ) use ( $ask ) { return in_array( $id, $ask, true ); } ) );  // the fixed order
		if ( ! $markets ) { return nadlan_cb_bad( 'markets', 'Choose at least one market.' ); }
		$buyer = sanitize_key( (string) ( $p['buyer'] ?? '' ) );
		if ( ! isset( nadlan_cb_buyers()[ $buyer ] ) ) { return nadlan_cb_bad( 'buyer', 'Choose the buyers.' ); }
		$budget = $p['budget'] ?? null;
		if ( ! is_numeric( $budget ) || (float) $budget != (int) $budget ) { return nadlan_cb_bad( 'budget', 'Bad budget.' ); }
		$budget = (int) $budget;
		if ( $budget < $bud['min'] || $budget > $bud['max'] || 0 !== $budget % $bud['step'] ) { return nadlan_cb_bad( 'budget', 'Bad budget.' ); }
		$sh = array_values( (array) ( $p['shares'] ?? array() ) ); $shares = array();
		if ( 4 !== count( $sh ) ) { return nadlan_cb_bad( 'split', 'Bad split.' ); }
		foreach ( $sh as $x ) { if ( ! is_numeric( $x ) || (int) $x < 0 || (int) $x > 100 || 0 !== (int) $x % 5 ) { return nadlan_cb_bad( 'split', 'Bad split.' ); } $shares[] = (int) $x; }
		if ( 100 !== array_sum( $shares ) ) { return nadlan_cb_bad( 'split', 'The split must add up to 100.' ); }
		$kind = sanitize_key( (string) ( $p['kind'] ?? '' ) );
		if ( ! isset( nadlan_cb_kinds()[ $kind ] ) ) { return nadlan_cb_bad( 'kind', 'Choose the project.' ); }
		$project = nadlan_cb_cut( sanitize_text_field( (string) ( $p['project'] ?? '' ) ), 200 );
		if ( 'existing' === $kind && nadlan_cb_len( $project ) < 2 ) { return nadlan_cb_bad( 'ref', 'Name the project page.' ); }
		$plan = sanitize_key( (string) ( $p['plan'] ?? '' ) );
		if ( ! isset( $plans[ $plan ] ) ) { return nadlan_cb_bad( 'plan', 'Choose a plan.' ); }
		if ( $plans[ $plan ]['markets'] > 0 && count( $markets ) > $plans[ $plan ]['markets'] ) { return nadlan_cb_bad( 'plan', 'The plan carries fewer markets.' ); }
		$name = nadlan_cb_cut( sanitize_text_field( (string) ( $p['name'] ?? '' ) ), 120 );
		if ( nadlan_cb_len( $name ) < 2 ) { return nadlan_cb_bad( 'name', 'Write the name.' ); }
		$company = nadlan_cb_cut( sanitize_text_field( (string) ( $p['company'] ?? '' ) ), 120 );
		if ( nadlan_cb_len( $company ) < 2 ) { return nadlan_cb_bad( 'company', 'Write the company.' ); }
		$phone = preg_replace( '/[\s\-().]/', '', (string) ( $p['phone'] ?? '' ) );
		if ( ! preg_match( '/^\+?\d{9,15}$/', $phone ) ) { return nadlan_cb_bad( 'phone', 'Write a phone number.' ); }
		$email = sanitize_email( (string) ( $p['email'] ?? '' ) );
		if ( ! $email || ! is_email( $email ) ) { return nadlan_cb_bad( 'email', 'Write an email address.' ); }
		if ( true !== ( $p['consent'] ?? null ) ) { return nadlan_cb_bad( 'consent', 'Consent is required.' ); }
		$lang = 'en' === ( $p['lang'] ?? '' ) ? 'en' : 'he';
		$page = (string) ( $p['page'] ?? '' );
		$page = '/' === substr( $page, 0, 1 ) ? nadlan_cb_cut( sanitize_text_field( $page ), 200 ) : '';
		return array(
			'markets' => $markets, 'langs' => nadlan_cb_langs_of( $markets ), 'buyer' => $buyer, 'budget' => $budget, 'yearly' => 12 * $budget,
			'shares' => array_combine( array_keys( nadlan_cb_channels() ), $shares ), 'kind' => $kind, 'project' => $project, 'plan' => $plan,
			'price' => (int) $plans[ $plan ]['price'], 'recommended' => nadlan_cb_recommend( count( $markets ) ), 'name' => $name, 'company' => $company,
			'phone' => $phone, 'email' => $email, 'consent' => true, 'consent_text' => nadlan_cb_cut( sanitize_textarea_field( (string) ( $p['consent_text'] ?? '' ) ), 600 ),
			'lang' => $lang, 'page' => $page,
		);
	}

	/** A plain Hebrew text of a brief (the post content and the admin mail). */
	function nadlan_cb_text( $c, $ref ) {
		$mk = nadlan_cb_markets(); $lg = nadlan_cb_langs(); $plans = nadlan_cb_plans(); $ch = nadlan_cb_channels(); $by = nadlan_cb_buyers(); $kd = nadlan_cb_kinds();
		$nf = function ( $n ) { return number_format( (float) $n, 0, '.', ',' ); };
		$split = array(); foreach ( $c['shares'] as $k => $v ) { $split[] = $ch[ $k ] . ' ' . $v . '%'; }
		$l = array(
			'מספר התוכנית: ' . $ref,
			'שווקים וקהילות: ' . implode( ', ', array_map( function ( $m ) use ( $mk ) { return $mk[ $m ]['he']; }, $c['markets'] ) ),
			'שפות: ' . implode( ', ', array_map( function ( $x ) use ( $lg ) { return $lg[ $x ]['he']; }, $c['langs'] ) ),
			'הקונים: ' . $by[ $c['buyer'] ]['he'],
			'תקציב פרסום: ' . $nf( $c['budget'] ) . ' ₪ בחודש, ' . $nf( $c['yearly'] ) . ' ₪ בשנה (משולם ישירות לערוצים)',
			'חלוקה: ' . implode( ', ', $split ),
			'הפרויקט: ' . $kd[ $c['kind'] ] . ( '' !== $c['project'] ? ', ' . $c['project'] : '' ),
			'התוכנית: ' . $plans[ $c['plan'] ]['he'] . ', ' . $nf( $c['price'] ) . ' ₪ לשנה' . ( $c['plan'] !== $c['recommended'] ? ' (המומלצת לפי מספר השווקים: ' . $plans[ $c['recommended'] ]['he'] . ')' : '' ),
			'',
			'שם: ' . $c['name'], 'חברה: ' . $c['company'], 'טלפון: ' . $c['phone'], 'אימייל: ' . $c['email'],
			'שפת הפנייה: ' . ( 'en' === $c['lang'] ? 'אנגלית' : 'עברית' ) . ( '' !== $c['page'] ? ', מהעמוד ' . $c['page'] : '' ),
			'הסכמה לחזרה בטלפון, בוואטסאפ ובאימייל: כן',
		);
		return implode( "\n", $l );
	}

	/** A new reference id, unique among the saved briefs: NLC-yymmdd-XXXX. */
	function nadlan_cb_new_ref() {
		for ( $i = 0; $i < 6; $i++ ) {
			$ref = 'NLC-' . gmdate( 'ymd' ) . '-' . strtoupper( bin2hex( random_bytes( 2 + ( $i > 2 ? 1 : 0 ) ) ) );
			$dup = get_posts( array( 'post_type' => 'nadlan_camp_brief', 'post_status' => 'any', 'posts_per_page' => 1, 'fields' => 'ids', 'no_found_rows' => true,
				'meta_query' => array( array( 'key' => '_nlc_ref', 'value' => $ref ) ) ) );
			if ( ! $dup ) { return $ref; }
		}
		return 'NLC-' . gmdate( 'ymd' ) . '-' . strtoupper( bin2hex( random_bytes( 4 ) ) );
	}

	/** A counter in a transient: false once $max is reached inside the window. */
	function nadlan_cb_limit( $bucket, $max, $window ) {
		$k = 'nadlan_cb_rl_' . md5( (string) $bucket );
		$n = (int) get_transient( $k );
		if ( $n >= $max ) { return false; }
		set_transient( $k, $n + 1, $window );
		return true;
	}
	function nadlan_cb_client() {
		if ( function_exists( 'nadlan_hardening_client_key' ) ) { return nadlan_hardening_client_key(); }
		return 'ip' . md5( substr( (string) ( $_SERVER['REMOTE_ADDR'] ?? '' ), 0, 80 ) ); // phpcs:ignore -- hashed, never stored
	}
	/** A browser request from another site is refused; a request without Origin (old browser, server) is allowed, and limited. */
	function nadlan_cb_same_origin( $req ) {
		$o = (string) $req->get_header( 'origin' );
		if ( '' === $o || 'null' === $o ) { return '' === $o; }
		$h = strtolower( (string) wp_parse_url( $o, PHP_URL_HOST ) ); $me = strtolower( (string) wp_parse_url( home_url( '/' ), PHP_URL_HOST ) );
		$strip = function ( $x ) { return preg_replace( '/^www\./', '', $x ); };
		return '' !== $h && $strip( $h ) === $strip( $me );
	}

	/** POST /wp-json/nadlan/v1/campaign-brief */
	function nadlan_cb_rest( $req ) {
		$raw = (string) $req->get_body();
		if ( strlen( $raw ) > 8192 ) { return new WP_Error( 'nlc_too_big', 'Request too large.', array( 'status' => 413 ) ); }
		if ( ! nadlan_cb_same_origin( $req ) ) { return new WP_Error( 'nlc_origin', 'Forbidden.', array( 'status' => 403 ) ); }
		$p = json_decode( $raw, true );
		if ( ! is_array( $p ) ) { return new WP_Error( 'nlc_bad', 'Bad request.', array( 'status' => 400 ) ); }
		if ( '' !== trim( (string) ( $p['hp'] ?? '' ) ) || (int) ( $p['t'] ?? 0 ) < 2000 ) { return new WP_Error( 'nlc_spam', 'Request rejected.', array( 'status' => 400 ) ); }
		if ( ! nadlan_cb_limit( 'c|' . nadlan_cb_client(), 5, HOUR_IN_SECONDS ) || ! nadlan_cb_limit( 'day|' . gmdate( 'Ymd' ), 60, DAY_IN_SECONDS ) ) {
			return new WP_Error( 'nlc_rate', 'Too many requests.', array( 'status' => 429 ) );
		}
		$c = nadlan_cb_clean( $p );
		if ( is_wp_error( $c ) ) { return $c; }
		$ref = nadlan_cb_new_ref(); $plans = nadlan_cb_plans(); $text = nadlan_cb_text( $c, $ref );
		$id = wp_insert_post( array( 'post_type' => 'nadlan_camp_brief', 'post_status' => 'private', 'post_title' => $ref . ' · ' . $c['company'] . ' · ' . $plans[ $c['plan'] ]['he'], 'post_content' => $text ), true );
		if ( is_wp_error( $id ) || ! $id ) { return new WP_Error( 'nlc_store', 'Could not save.', array( 'status' => 500 ) ); }
		update_post_meta( $id, '_nlc_ref', $ref );
		update_post_meta( $id, '_nlc_status', 'new' );  // new -> payment link sent -> paid -> live (set by hand for now)
		update_post_meta( $id, '_nlc_brief', wp_slash( wp_json_encode( $c, JSON_UNESCAPED_UNICODE ) ) );
		update_post_meta( $id, '_nlc_consent_at', gmdate( 'c' ) );
		$to = apply_filters( 'nadlan_cb_notify_to', get_option( 'admin_email' ) );
		if ( $to ) {
			$pl = $plans[ $c['plan'] ]; $fp = nadlan_cb_first_pay( $pl ); $nf = function ( $n ) { return number_format( (float) $n, 0, '.', ',' ); };
			$pay = $pl['product'] <= 0 ? 'עוד אין מוצר לתוכנית הזו בחנות: לשלוח ללקוח קישור לתשלום עוד היום (הובטח לו).'
				: ( $fp ? 'הלקוח קיבל כפתור לתשלום ראשון של ' . $nf( $fp ) . ' ₪ (מוצר ' . (int) $pl['product'] . '). את היתרה, ' . $nf( $pl['price'] - $fp ) . ' ₪, לשלוח לו בקישורים של עד ' . $nf( $fp ) . ' ₪ (הובטח לו).'
					: 'הלקוח קיבל כפתור לתשלום המלא (מוצר ' . (int) $pl['product'] . ').' );
			wp_mail( $to, '[נדלן] תוכנית קמפיין בינלאומי ' . $ref . ' · ' . $c['company'], $text . "\n\n" . $pay . "\nניהול: " . admin_url( 'post.php?post=' . (int) $id . '&action=edit' ) );
		}
		return new WP_REST_Response( array( 'ok' => true, 'ref' => $ref, 'plan' => $c['plan'], 'price' => $c['price'] ), 201 );
	}

	/** The summary the shortcode prints before the script runs (search engines, AI answers, readers without JS). */
	function nadlan_cb_summary( $lang = 'he' ) {
		$en = 'en' === $lang; $plans = nadlan_cb_plans(); $mk = nadlan_cb_markets(); $lg = nadlan_cb_langs(); $b = nadlan_cb_budget();
		$k = $en ? 'en' : 'he';
		$nf = function ( $n ) { return '<bdi>' . esc_html( number_format( (float) $n, 0, '.', ',' ) ) . '</bdi>'; };
		$names = array_map( function ( $m ) use ( $k ) { return esc_html( $m[ $k ] ); }, array_values( $mk ) );
		$last = array_pop( $names );
		$langs = array_map( function ( $x ) use ( $k ) { return esc_html( $x[ $k ] ); }, array_values( $lg ) );
		if ( $en ) {
			$pl = array(); foreach ( $plans as $p ) { $pl[] = esc_html( $p['en'] ) . ' ₪' . $nf( $p['price'] ) . ' a year'; }
			return '<p>A planner for property developers who sell to buyers abroad and in the diaspora: choose the markets and communities ('
				. implode( ', ', $names ) . ' and ' . $last . '), the buyers you want, a monthly ad budget and the project, and see the plan and its price before you send it. '
				. 'The campaign speaks to buyers in their own language (' . implode( ', ', $langs ) . '); ads are aimed by country, city and language, plus community press and newsletters. '
				. 'The leads land on your project page on NadLan, with the 3D tour, and every lead reaches you on WhatsApp with what the buyer opened in the project. '
				. 'Three annual plans: ' . implode( '; ', $pl ) . '. The ad budget, from ₪' . $nf( $b['min'] ) . ' to ₪' . $nf( $b['max'] ) . ' a month, is paid by you straight to Meta, Google and the other channels, and is not part of the plan price. '
				. 'The subscription is paid before the campaign goes live.</p>';
		}
		$pl = array(); foreach ( $plans as $p ) { $pl[] = esc_html( $p['he'] ) . ' ' . $nf( $p['price'] ) . ' ₪ לשנה'; }
		return '<p>מתכנן קמפיין ליזמים שמוכרים לקונים בחו״ל ובתפוצות: בוחרים שווקים וקהילות (' . implode( ', ', $names ) . ' ו' . $last . '), את הקונים שאתם מחפשים, '
			. 'תקציב פרסום חודשי ואת הפרויקט, ורואים את התוכנית ואת המחיר לפני ששולחים. הקמפיין מדבר עם הקונים בשפה שלהם (' . implode( ', ', $langs ) . '), '
			. 'והפרסום מכוון לפי מדינה, עיר ושפה, ובעיתונות ובניוזלטרים של הקהילות. הפניות מגיעות לעמוד הפרויקט שלכם בנדלן, עם הסיור התלת־ממדי, '
			. 'וכל פנייה מגיעה אליכם בוואטסאפ עם מה שהקונה פתח בפרויקט. שלוש תוכניות שנתיות: ' . implode( '; ', $pl ) . '. '
			. 'תקציב הפרסום, בין ' . $nf( $b['min'] ) . ' ל־' . $nf( $b['max'] ) . ' ₪ בחודש, משולם על ידכם ישירות ל־Meta, ל־Google ולשאר הערוצים, ואינו חלק ממחיר התוכנית. '
			. 'המנוי משולם לפני שהקמפיין יוצא לדרך.</p>';
	}

	/** The product link of a plan: the shop's own checkout with the product added. */
	function nadlan_cb_product_url( $pid ) {
		$base = function_exists( 'wc_get_checkout_url' ) ? wc_get_checkout_url() : home_url( '/checkout/' );
		return add_query_arg( 'add-to-cart', (int) $pid, $base );
	}
}

add_action( 'init', function () {
	register_post_type( 'nadlan_camp_brief', array(
		'label' => 'תוכניות קמפיין בינלאומי', 'public' => false, 'publicly_queryable' => false, 'exclude_from_search' => true, 'show_ui' => true,
		'show_in_menu' => 'edit.php?post_type=nadlan_project', 'show_in_rest' => false, 'rewrite' => false, 'query_var' => false,
		'supports' => array( 'title' ), 'capability_type' => 'post', 'map_meta_cap' => true,
	) );
} );

add_action( 'rest_api_init', function () {
	register_rest_route( 'nadlan/v1', '/campaign-brief', array( 'methods' => 'POST', 'permission_callback' => '__return_true', 'callback' => 'nadlan_cb_rest' ) );
} );

/* the brief, read only, on its edit screen */
add_action( 'add_meta_boxes_nadlan_camp_brief', function ( $post ) {
	add_meta_box( 'nadlan-cb-brief', 'התוכנית', function ( $p ) {
		echo '<pre style="white-space:pre-wrap;direction:rtl;text-align:right;font:14px/1.6 system-ui,sans-serif;margin:0">' . esc_html( (string) $p->post_content ) . '</pre>';
		echo '<p>מצב: <code>' . esc_html( (string) get_post_meta( $p->ID, '_nlc_status', true ) ) . '</code></p>';
	}, null, 'normal', 'high' );
} );

/* window.NLCAMP_CONFIG before tools/nlcamp.js (enqueued by inc/instruments.php at priority 20 as nadlan-nli-nlcamp) */
add_action( 'wp_enqueue_scripts', function () {
	if ( ! function_exists( 'wp_script_is' ) || ! wp_script_is( 'nadlan-nli-nlcamp', 'enqueued' ) ) { return; }
	$cfg = array( 'endpoint' => esc_url_raw( rest_url( 'nadlan/v1/campaign-brief' ) ), 'plans' => array() );
	$priv = function_exists( 'get_privacy_policy_url' ) ? get_privacy_policy_url() : '';
	$cfg['privacy'] = esc_url_raw( $priv ? $priv : home_url( '/privacy/' ) );
	foreach ( nadlan_cb_plans() as $k => $pl ) { $cfg['plans'][ $k ] = array( 'productUrl' => $pl['product'] > 0 ? esc_url_raw( nadlan_cb_product_url( $pl['product'] ) ) : null, 'firstPay' => nadlan_cb_first_pay( $pl ) ); }
	wp_add_inline_script( 'nadlan-nli-nlcamp', 'window.NLCAMP_CONFIG=' . wp_json_encode( $cfg, JSON_UNESCAPED_SLASHES ) . ';', 'before' );
}, 21 );

add_filter( 'nadlan_config_healthcheck', function ( $out ) {
	$pr = array(); foreach ( nadlan_cb_plans() as $k => $p ) { $pr[ $k ] = (int) $p['product']; }
	$out['campaign_brief'] = array( 'version' => NADLAN_CB_VERSION, 'products' => $pr, 'first_amount' => nadlan_cb_first_amount() );
	return $out;
} );
