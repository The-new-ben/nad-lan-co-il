<?php
/**
 * DealSign: the signing room of a developer cooperation (HAD-495, the owner's order of 12.10.2026).
 *
 * A licensed broker who works with nad-lan.co.il (first: Meital Katsir, licence 3131540) offers developers a package: the
 * project's showroom on the site (a fixed advertising fee, the live product 489) and her escort of buyers to the signing.
 * Her fear, in the owner's words: she works hard and then the developer says "this client came from somewhere else". This
 * module gives her a binding, timestamped paper trail:
 *  - the broker's private office (?nlsg_office=<token>): she creates a cooperation agreement for a developer, signs it with a
 *    drawn signature, and sends the developer a link on WhatsApp or by mail;
 *  - the developer's signing page (?nlsg_sign=<token>): the two documents (the cooperation agreement and brokerage order with
 *    the broker, the advertising order with nad-lan.co.il), the company's details, a drawn signature; a signed copy for both;
 *  - client registration (from the office): name, project, the server's time; the developer's review page (?nlsg_rev=<token>)
 *    confirms, or objects within 2 business days with an earlier dated record; silence makes it final for 12 months.
 * Evidence kept for every act: the server time (UTC and Israel), the IP, the browser, the SHA-256 of the exact text signed.
 * The signed agreement is the s.9 written order of the Brokers Law (research: docs/research/2026-10-12-broker-developer-model).
 * nad-lan.co.il is never presented as a broker here: the brokerage is the broker's, in her name and licence.
 *
 * Storage: private post types nadlan_sgdeal and nadlan_sgreg (no REST exposure, no front-end query), the brokers in the
 * option nadlan_sg_brokers (not autoloaded). Tokens are 32 hex characters. No robots meta is added: indexing is the owner's
 * decision; the pages answer only to an unguessable token and are linked from nowhere.
 * Admin REST (manage_options): POST /nadlan/v1/sg/broker, GET /nadlan/v1/sg/admin.
 */
if ( ! defined( 'ABSPATH' ) ) { exit; }

if ( ! function_exists( 'nadlan_sg_projects' ) ) {

	/** The projects a broker can open an agreement on; 'other' takes a free name. */
	function nadlan_sg_projects() {
		return array(
			'ashira'  => array( 'name' => 'אשירה שדה דב', 'dev' => 'אביסרור משה ובניו', 'asset' => 'פרויקט אשירה (ASHIRA), מגרש 101, מתחם אשכול, רובע שדה דב, תל אביב-יפו', 'url' => '/projects/ashira-sde-dov/' ),
			'rainbow' => array( 'name' => 'ריינבו תל אביב', 'dev' => 'ישראל קנדה', 'asset' => 'פרויקט ריינבו (Rainbow Tel Aviv), רובע שדה דב, תל אביב-יפו', 'url' => '/projects/rainbow-tel-aviv/' ),
			'dimri'   => array( 'name' => 'דמרי ימה שדה דב', 'dev' => 'י.ח. דמרי', 'asset' => 'פרויקט דמרי ימה (DIMRI YAMA), רובע שדה דב, תל אביב-יפו', 'url' => '/projects/dimri-yama-sde-dov/' ),
		);
	}

	function nadlan_sg_token() { return bin2hex( random_bytes( 16 ) ); }
	function nadlan_sg_valid( $t ) { return is_string( $t ) && preg_match( '/^[a-f0-9]{32}$/', $t ) ? $t : ''; }
	function nadlan_sg_ip() { return isset( $_SERVER['REMOTE_ADDR'] ) ? sanitize_text_field( wp_unslash( $_SERVER['REMOTE_ADDR'] ) ) : ''; }
	function nadlan_sg_ua() { return isset( $_SERVER['HTTP_USER_AGENT'] ) ? substr( sanitize_text_field( wp_unslash( $_SERVER['HTTP_USER_AGENT'] ) ), 0, 300 ) : ''; }
	function nadlan_sg_il( $ts ) { return wp_date( 'd.m.Y H:i', (int) $ts, new DateTimeZone( 'Asia/Jerusalem' ) ); }
	function nadlan_sg_url( $k, $t ) { return add_query_arg( $k, $t, home_url( '/' ) ); }

	/** The brokers: token => profile. Kept out of autoload. */
	function nadlan_sg_brokers() { $b = get_option( 'nadlan_sg_brokers', array() ); return is_array( $b ) ? $b : array(); }
	function nadlan_sg_broker( $token ) { $b = nadlan_sg_brokers(); $token = nadlan_sg_valid( $token ); return ( $token && isset( $b[ $token ] ) ) ? $b[ $token ] : null; }

	/** One post by its token meta. */
	function nadlan_sg_find( $type, $key, $token ) {
		$token = nadlan_sg_valid( $token );
		if ( ! $token ) { return 0; }
		$ids = get_posts( array( 'post_type' => $type, 'post_status' => 'any', 'numberposts' => 1, 'fields' => 'ids', 'no_found_rows' => true, 'suppress_filters' => true, 'meta_key' => $key, 'meta_value' => $token ) );
		return $ids ? (int) $ids[0] : 0;
	}

	/** A small per-IP limit on every public write. */
	function nadlan_sg_limit( $what, $max = 30 ) {
		$k = 'nlsg_rl_' . md5( $what . '|' . nadlan_sg_ip() );
		$n = (int) get_transient( $k );
		if ( $n >= $max ) { return false; }
		set_transient( $k, $n + 1, HOUR_IN_SECONDS );
		return true;
	}

	/** A drawn signature: a PNG data URL, decoded and size-checked, or ''. */
	function nadlan_sg_sig( $s ) {
		$s = is_string( $s ) ? $s : '';
		if ( 0 !== strpos( $s, 'data:image/png;base64,' ) || strlen( $s ) > 420000 ) { return ''; }
		$raw = base64_decode( substr( $s, 22 ), true );
		if ( false === $raw || substr( $raw, 0, 8 ) !== "\x89PNG\r\n\x1a\n" || strlen( $raw ) < 600 ) { return ''; }
		return 'data:image/png;base64,' . base64_encode( $raw );
	}

	/** Two business days (Sunday to Thursday) after a moment. */
	function nadlan_sg_deadline( $ts ) {
		$d = (int) $ts; $n = 0;
		while ( $n < 2 ) {
			$d += DAY_IN_SECONDS;
			$w = (int) wp_date( 'w', $d, new DateTimeZone( 'Asia/Jerusalem' ) );
			if ( 5 !== $w && 6 !== $w ) { $n++; }
		}
		return $d;
	}

	/** The evidence of one act. */
	function nadlan_sg_act( $extra = array() ) {
		$t = time();
		return array_merge( array( 'ts' => $t, 'utc' => gmdate( 'c', $t ), 'il' => nadlan_sg_il( $t ), 'ip' => nadlan_sg_ip(), 'ua' => nadlan_sg_ua() ), $extra );
	}

	/* ------------------------------------------------------------------ the documents */

	/** Document A: the cooperation agreement and brokerage order (the broker and the developer). */
	function nadlan_sg_doc_a( $d ) {
		$tpl = <<<'HTML'
<h2>הסכם שיתוף פעולה והזמנת שירותי תיווך</h2>
<p><b>בין:</b> {DEV}, ח.פ. {DEVNUM}, מכתובת {DEVADDR}, באמצעות מורשי החתימה שלה ("החברה");</p>
<p><b>לבין:</b> {BNAME}, ת.ז. {BID}, מתווכת מקרקעין מורשית, רישיון מס׳ {BLIC}, הפועלת בשם {BOFFICE} ("המתווכת").</p>
<p><b>הואיל</b> והחברה משווקת יחידות דיור ומסחר בפרויקט, ומפרסמת אותו באתר nad-lan.co.il בהזמנה נפרדת; <b>והואיל</b> והמתווכת מבקשת להציג לחברה לקוחות לרכישת יחידות בפרויקט, והחברה מעוניינת בכך לפי התנאים שלהלן; <b>לפיכך הוסכם בין הצדדים כדלקמן:</b></p>
<ol>
<li><b>הגדרות.</b> "הפרויקט": {ASSET}, על כל יחידותיו. "לקוח": אדם שהמתווכת רשמה לפי סעיף 3, לרבות בן או בת זוגו, ותאגיד בשליטתו. "עסקה": חתימה על הסכם רכישה של יחידה בפרויקט בין החברה לבין לקוח. "יום עסקים": ראשון עד חמישי, למעט חג וערב חג.</li>
<li><b>ההזמנה.</b> החברה מזמינה מהמתווכת שירותי תיווך להצגת לקוחות לרכישת יחידות בפרויקט. הסכם זה הוא הזמנה בכתב לפי סעיף 9 לחוק המתווכים במקרקעין, התשנ"ו-1996. ההזמנה אינה בלעדית: החברה רשאית לשווק את הפרויקט בעצמה ובאמצעות אחרים, בכפוף לזכויות המתווכת לגבי לקוחות רשומים.</li>
<li><b>רישום לקוח.</b> לפני מסירת פרטי לקוח לחברה, תשלח המתווכת הודעת רישום הכוללת את שם הלקוח, את הפרויקט ואת מועד הרישום, באמצעות קישור הרישום המאובטח שמופק באתר nad-lan.co.il, אל: {REGTO}. מועד הרישום הוא המועד המתועד בשרת.</li>
<li><b>בדיקה והתנגדות.</b> בתוך 2 ימי עסקים ממועד הרישום רשאית החברה להודיע, בקישור הרישום, שהלקוח כבר רשום אצלה, בצירוף תיעוד מתוארך שקודם למועד הרישום, כגון פנייה, פגישה או הצעת מחיר. רישום מוקדם ומתועד כזה גובר, והלקוח לא ייחשב לקוח של המתווכת. לא נמסרה הודעה כזו בתוך המועד, הרישום סופי.</li>
<li><b>תקופת הגנה.</b> 12 חודשים ממועד הרישום. נחתמה עסקה עם לקוח רשום בתקופה זו, בכל דרך ובאמצעות כל גורם, ישולם למתווכת שכר התיווך שבסעיף 6.</li>
<li><b>שכר התיווך.</b> {RATE}% מהתמורה הנקובה בהסכם הרכישה, לפני מע״מ, בתוספת מע״מ כדין. התשלום תוך 30 יום ממועד חתימת הסכם הרכישה, כנגד חשבונית מס. בוטל הסכם הרכישה בתוך תקופת ביטול על פי דין, לא ישולם שכר תיווך, ואם שולם יוחזר.</li>
<li><b>אופן העבודה.</b> המתווכת תציג ללקוח את הפרויקט, תתאם פגישות עם צוות המכירות ותלווה אותו עד החתימה. המחירים, התנאים והחומרים נקבעים על ידי החברה בלבד, והמתווכת לא תציג מצגים בשם החברה מעבר לחומרים שמסרה לה.</li>
<li><b>גילוי ללקוח.</b> המתווכת תגלה ללקוח בכתב שהיא מקבלת שכר מהחברה. המתווכת לא תגבה מהלקוח דמי תיווך על אותה עסקה, אלא בגילוי מלא ובכתב לחברה.</li>
<li><b>פרטיות.</b> פרטי לקוח יימסרו לחברה רק בהסכמתו, וישמשו רק לצורך העסקה.</li>
<li><b>תקופה וסיום.</b> ההסכם בתוקף 12 חודשים ומתחדש מאליו. כל צד רשאי לסיימו בהודעה של 30 יום. הסיום אינו פוגע בזכויות לגבי לקוחות שנרשמו לפני מועד הסיום, לכל תקופת ההגנה שלהם.</li>
<li><b>חתימה אלקטרונית.</b> הצדדים מסכימים שחתימה אלקטרונית על הסכם זה ועל הודעות הרישום, בקישור המאובטח, מחייבת כחתימה בכתב. רשומות הקישור (מועד, כתובת רשת וטביעת המסמך) והעותק החתום שמופק לשני הצדדים ישמשו ראיה למועדים ולתוכן.</li>
<li><b>כללי.</b> האתר nad-lan.co.il אינו צד להסכם זה ואינו פועל כמתווך. כל שינוי בהסכם בכתב בלבד. סמכות השיפוט הבלעדית לבתי המשפט בתל אביב-יפו.</li>
</ol>
HTML;
		return strtr( $tpl, nadlan_sg_fields( $d ) );
	}

	/** Document B: the advertising order (the developer and nad-lan.co.il). */
	function nadlan_sg_doc_b( $d ) {
		$tpl = <<<'HTML'
<h2>הזמנת פרסום · אולם התצוגה של {PNAME} ב-nad-lan.co.il</h2>
<p><b>המזמינה:</b> {DEV}, ח.פ. {DEVNUM}. <b>המסלול שנבחר:</b> {PLAN}.</p>
<ol>
<li><b>השירות.</b> עמוד הפרויקט באתר nad-lan.co.il בעברית, אנגלית, צרפתית, רוסית וערבית: סיור וירטואלי בפרויקט ובחירת דירה לפי קומה וכיוון, הנוף מהדירה, השכונה על מפה אחת, סרטי הצגה, חדר צפייה משותף, טופס פנייה ותיאום שיחה, ואזור אישי לעדכון חומרים ולקבלת פניות.</li>
<li><b>המחיר.</b> חודש אחד 3,990 ₪, 3 חודשים 10,990 ₪, 6 חודשים 19,990 ₪, כולל מע״מ, כפי שמפורסם באתר. התשלום מראש לכל תקופה, כנגד חשבונית.</li>
<li><b>תוכן.</b> החברה תמסור חומרים רשמיים ותאשר את העמוד. הדמיות מסומנות "להמחשה בלבד". מחירים ומלאי מוצגים רק כפי שהחברה מסרה או כפי שפורסמו, עם מקור ותאריך.</li>
<li><b>פניות.</b> פניות מעמוד הפרויקט מועברות לחברה, ובמסגרת השיתוף עם {BNAME} גם אליה, בהסכמת הפונה.</li>
<li><b>בלי התחייבות לתוצאה.</b> האתר אינו מתחייב לכמות פניות, למכירות או לתוצאה עסקית, ואינו גובה עמלה על מכירה.</li>
<li><b>תקופה.</b> לפי המסלול שנבחר, החידוש בהודעה בכתב. ההזמנה נכנסת לתוקף עם אישורה על ידי nad-lan.co.il והוצאת החשבונית.</li>
<li><b>האתר אינו מתווך.</b> nad-lan.co.il הוא אתר פרסום עצמאי, אינו מציג עצמו כמתווך ואינו מייצג אף צד.</li>
</ol>
HTML;
		return strtr( $tpl, nadlan_sg_fields( $d ) );
	}

	/** The fields of a deal, escaped; empty developer fields read "יושלם בחתימה". */
	function nadlan_sg_fields( $d ) {
		$e = function ( $k, $fill = 'יושלם בחתימה' ) use ( $d ) { $v = isset( $d[ $k ] ) ? trim( (string) $d[ $k ] ) : ''; return '' === $v ? '<i>' . $fill . '</i>' : esc_html( $v ); };
		$plans = array( '1' => 'חודש אחד, 3,990 ₪', '3' => '3 חודשים, 10,990 ₪', '6' => '6 חודשים, 19,990 ₪' );
		return array(
			'{DEV}' => $e( 'dev' ), '{DEVNUM}' => $e( 'devnum' ), '{DEVADDR}' => $e( 'devaddr' ), '{ASSET}' => $e( 'asset' ), '{PNAME}' => $e( 'pname' ),
			'{BNAME}' => $e( 'bname' ), '{BID}' => $e( 'bid' ), '{BLIC}' => $e( 'blic' ), '{BOFFICE}' => $e( 'boffice' ), '{REGTO}' => $e( 'regto' ),
			'{RATE}' => $e( 'rate' ), '{PLAN}' => isset( $plans[ (string) ( $d['plan'] ?? '' ) ] ) ? $plans[ (string) $d['plan'] ] : '<i>יבחר בחתימה</i>',
		);
	}

	/* ------------------------------------------------------------------ storage */

	add_action( 'init', function () {
		foreach ( array( 'nadlan_sgdeal' => 'הסכמי שיתוף', 'nadlan_sgreg' => 'רישומי לקוחות' ) as $pt => $label ) {
			register_post_type( $pt, array(
				'label' => $label, 'public' => false, 'publicly_queryable' => false, 'exclude_from_search' => true, 'show_ui' => false,
				'show_in_rest' => false, 'rewrite' => false, 'query_var' => false, 'supports' => array( 'title' ), 'can_export' => false,
			) );
		}
	} );

	function nadlan_sg_deal( $id ) {
		$m = get_post_meta( $id, '_nlsg', true );
		return is_array( $m ) ? $m : array();
	}

	/* ------------------------------------------------------------------ REST */

	add_action( 'rest_api_init', function () {
		$ns = 'nadlan/v1';
		$pub = '__return_true';
		register_rest_route( $ns, '/sg/broker', array( 'methods' => 'POST', 'permission_callback' => function () { return current_user_can( 'manage_options' ); }, 'callback' => 'nadlan_sg_rest_broker' ) );
		register_rest_route( $ns, '/sg/admin', array( 'methods' => 'GET', 'permission_callback' => function () { return current_user_can( 'manage_options' ); }, 'callback' => 'nadlan_sg_rest_admin' ) );
		register_rest_route( $ns, '/sg/deal', array( 'methods' => 'POST', 'permission_callback' => $pub, 'callback' => 'nadlan_sg_rest_deal' ) );
		register_rest_route( $ns, '/sg/sign', array( 'methods' => 'POST', 'permission_callback' => $pub, 'callback' => 'nadlan_sg_rest_sign' ) );
		register_rest_route( $ns, '/sg/reg', array( 'methods' => 'POST', 'permission_callback' => $pub, 'callback' => 'nadlan_sg_rest_reg' ) );
		register_rest_route( $ns, '/sg/rev', array( 'methods' => 'POST', 'permission_callback' => $pub, 'callback' => 'nadlan_sg_rest_rev' ) );
	} );

	function nadlan_sg_err( $msg, $code = 400 ) { return new WP_REST_Response( array( 'ok' => false, 'error' => $msg ), $code ); }
	function nadlan_sg_txt( $r, $k, $max = 160 ) { return mb_substr( trim( sanitize_text_field( (string) $r->get_param( $k ) ) ), 0, $max ); }

	/** Admin: create or update a broker; returns the office link. */
	function nadlan_sg_rest_broker( WP_REST_Request $r ) {
		$b = nadlan_sg_brokers();
		$tok = nadlan_sg_valid( (string) $r->get_param( 'token' ) );
		if ( ! $tok ) { $tok = nadlan_sg_token(); }
		$b[ $tok ] = array( 'name' => nadlan_sg_txt( $r, 'name' ), 'office' => nadlan_sg_txt( $r, 'office' ), 'lic' => nadlan_sg_txt( $r, 'lic', 20 ), 'phone' => nadlan_sg_txt( $r, 'phone', 30 ), 'email' => sanitize_email( (string) $r->get_param( 'email' ) ) );
		update_option( 'nadlan_sg_brokers', $b, false );
		return array( 'ok' => true, 'token' => $tok, 'office' => nadlan_sg_url( 'nlsg_office', $tok ) );
	}

	/** Admin: everything, for the owner's ledger. */
	function nadlan_sg_rest_admin() {
		$out = array( 'deals' => array(), 'regs' => array() );
		foreach ( get_posts( array( 'post_type' => 'nadlan_sgdeal', 'post_status' => 'any', 'numberposts' => 200, 'suppress_filters' => true ) ) as $p ) {
			$d = nadlan_sg_deal( $p->ID ); unset( $d['doc_a'], $d['doc_b'] );
			foreach ( array( 'bsig', 'dsig' ) as $k ) { if ( ! empty( $d[ $k ]['img'] ) ) { $d[ $k ]['img'] = '(png ' . strlen( $d[ $k ]['img'] ) . ')'; } }
			$out['deals'][] = array( 'id' => $p->ID, 'title' => $p->post_title, 'sign' => nadlan_sg_url( 'nlsg_sign', $d['token'] ?? '' ), 'data' => $d );
		}
		foreach ( get_posts( array( 'post_type' => 'nadlan_sgreg', 'post_status' => 'any', 'numberposts' => 500, 'suppress_filters' => true ) ) as $p ) {
			$out['regs'][] = array( 'id' => $p->ID, 'title' => $p->post_title, 'data' => nadlan_sg_deal( $p->ID ) );
		}
		return $out;
	}

	/** The broker opens an agreement for a developer and signs it. */
	function nadlan_sg_rest_deal( WP_REST_Request $r ) {
		if ( ! nadlan_sg_limit( 'deal', 20 ) ) { return nadlan_sg_err( 'יותר מדי ניסיונות. נסו שוב בעוד שעה.', 429 ); }
		$office = nadlan_sg_valid( (string) $r->get_param( 'office' ) );
		$b = nadlan_sg_broker( $office );
		if ( ! $b ) { return nadlan_sg_err( 'הקישור אינו תקף.', 403 ); }
		$pk = sanitize_key( (string) $r->get_param( 'project' ) );
		$pp = nadlan_sg_projects();
		if ( 'other' === $pk ) {
			$pname = nadlan_sg_txt( $r, 'pname' ); $asset = nadlan_sg_txt( $r, 'asset', 240 );
			if ( '' === $pname || '' === $asset ) { return nadlan_sg_err( 'חסרים שם הפרויקט ומיקומו.' ); }
		} elseif ( isset( $pp[ $pk ] ) ) {
			$pname = $pp[ $pk ]['name']; $asset = $pp[ $pk ]['asset'];
		} else {
			return nadlan_sg_err( 'בחרו פרויקט.' );
		}
		$rate = str_replace( ',', '.', nadlan_sg_txt( $r, 'rate', 8 ) );
		if ( ! preg_match( '/^\d{1,2}(\.\d{1,2})?$/', $rate ) || (float) $rate <= 0 || (float) $rate > 10 ) { return nadlan_sg_err( 'שיעור שכר התיווך צריך להיות מספר בין 0.1 ל־10.' ); }
		$dev = nadlan_sg_txt( $r, 'dev' ); $regto = nadlan_sg_txt( $r, 'regto', 120 ); $bid = nadlan_sg_txt( $r, 'bid', 12 ); $sname = nadlan_sg_txt( $r, 'signer' );
		if ( '' === $dev ) { return nadlan_sg_err( 'חסר שם החברה.' ); }
		if ( '' === $regto ) { return nadlan_sg_err( 'חסרים המייל או הוואטסאפ של החברה לרישום לקוחות.' ); }
		if ( ! preg_match( '/^\d{5,9}$/', $bid ) ) { return nadlan_sg_err( 'מספר תעודת הזהות לא תקין.' ); }
		if ( '' === $sname ) { return nadlan_sg_err( 'חסר שם החותמת.' ); }
		if ( ! $r->get_param( 'agree' ) ) { return nadlan_sg_err( 'יש לאשר את נוסח ההסכם.' ); }
		$sig = nadlan_sg_sig( (string) $r->get_param( 'sig' ) );
		if ( ! $sig ) { return nadlan_sg_err( 'חסרה חתימה.' ); }
		$d = array(
			'v' => 1, 'office' => $office, 'project' => $pk, 'pname' => $pname, 'asset' => $asset, 'dev' => $dev, 'devnum' => '', 'devaddr' => '',
			'regto' => $regto, 'rate' => $rate, 'bname' => $b['name'], 'bid' => $bid, 'blic' => $b['lic'], 'boffice' => $b['office'],
			'token' => nadlan_sg_token(), 'status' => 'sent', 'created' => nadlan_sg_act(),
		);
		$d['doc_a_draft'] = nadlan_sg_doc_a( $d );
		$d['bsig'] = nadlan_sg_act( array( 'name' => $sname, 'img' => $sig, 'hash' => hash( 'sha256', $d['doc_a_draft'] ) ) );
		$id = wp_insert_post( array( 'post_type' => 'nadlan_sgdeal', 'post_status' => 'private', 'post_title' => $pname . ' · ' . $dev ), true );
		if ( is_wp_error( $id ) ) { return nadlan_sg_err( 'השמירה נכשלה. נסו שוב.', 500 ); }
		update_post_meta( $id, '_nlsg', $d );
		update_post_meta( $id, '_nlsg_token', $d['token'] );
		update_post_meta( $id, '_nlsg_office', $office );
		$url = nadlan_sg_url( 'nlsg_sign', $d['token'] );
		return array( 'ok' => true, 'id' => $id, 'url' => $url, 'wa' => 'https://wa.me/?text=' . rawurlencode( "שלום, מצורף הסכם שיתוף הפעולה לפרויקט {$pname}, לעיון ולחתימה דיגיטלית:\n{$url}\n{$b['name']}, {$b['office']}" ) );
	}

	/** The developer signs both documents. */
	function nadlan_sg_rest_sign( WP_REST_Request $r ) {
		if ( ! nadlan_sg_limit( 'sign', 20 ) ) { return nadlan_sg_err( 'יותר מדי ניסיונות. נסו שוב בעוד שעה.', 429 ); }
		$id = nadlan_sg_find( 'nadlan_sgdeal', '_nlsg_token', (string) $r->get_param( 'token' ) );
		if ( ! $id ) { return nadlan_sg_err( 'הקישור אינו תקף.', 404 ); }
		$d = nadlan_sg_deal( $id );
		if ( 'signed' === ( $d['status'] ?? '' ) ) { return nadlan_sg_err( 'ההסכם כבר נחתם.', 409 ); }
		$f = array( 'devnum' => nadlan_sg_txt( $r, 'devnum', 12 ), 'devaddr' => nadlan_sg_txt( $r, 'devaddr', 160 ), 'name' => nadlan_sg_txt( $r, 'name' ), 'role' => nadlan_sg_txt( $r, 'role' ), 'email' => sanitize_email( (string) $r->get_param( 'email' ) ), 'phone' => nadlan_sg_txt( $r, 'phone', 30 ) );
		$plan = (string) $r->get_param( 'plan' );
		if ( ! preg_match( '/^\d{8,9}$/', $f['devnum'] ) ) { return nadlan_sg_err( 'מספר החברה (ח.פ.) לא תקין.' ); }
		if ( '' === $f['devaddr'] || '' === $f['name'] || '' === $f['role'] ) { return nadlan_sg_err( 'חסרים פרטים: כתובת החברה, שם החותם ותפקידו.' ); }
		if ( ! is_email( $f['email'] ) ) { return nadlan_sg_err( 'כתובת המייל לא תקינה.' ); }
		if ( ! in_array( $plan, array( '1', '3', '6' ), true ) ) { return nadlan_sg_err( 'בחרו מסלול פרסום.' ); }
		if ( ! $r->get_param( 'agree_a' ) || ! $r->get_param( 'agree_b' ) ) { return nadlan_sg_err( 'יש לאשר את שני המסמכים.' ); }
		$sig = nadlan_sg_sig( (string) $r->get_param( 'sig' ) );
		if ( ! $sig ) { return nadlan_sg_err( 'חסרה חתימה.' ); }
		$d['devnum'] = $f['devnum']; $d['devaddr'] = $f['devaddr']; $d['plan'] = $plan;
		$d['doc_a'] = nadlan_sg_doc_a( $d ); $d['doc_b'] = nadlan_sg_doc_b( $d );
		$d['dsig'] = nadlan_sg_act( array( 'name' => $f['name'], 'role' => $f['role'], 'email' => $f['email'], 'phone' => $f['phone'], 'img' => $sig, 'hash_a' => hash( 'sha256', $d['doc_a'] ), 'hash_b' => hash( 'sha256', $d['doc_b'] ) ) );
		$d['status'] = 'signed';
		update_post_meta( $id, '_nlsg', $d );
		$copy = nadlan_sg_url( 'nlsg_sign', $d['token'] );
		$b = nadlan_sg_broker( $d['office'] );
		$subj = 'הסכם שיתוף פעולה נחתם · ' . $d['pname'];
		$body = "ההסכם לפרויקט {$d['pname']} נחתם בתאריך {$d['dsig']['il']} (שעון ישראל).\nהעותק החתום: {$copy}\n";
		foreach ( array_filter( array( $f['email'], $b['email'] ?? '', get_option( 'admin_email' ) ) ) as $to ) { @wp_mail( $to, $subj, $body ); }
		return array( 'ok' => true, 'copy' => $copy );
	}

	/** The broker registers a client under an agreement. */
	function nadlan_sg_rest_reg( WP_REST_Request $r ) {
		if ( ! nadlan_sg_limit( 'reg', 40 ) ) { return nadlan_sg_err( 'יותר מדי ניסיונות. נסו שוב בעוד שעה.', 429 ); }
		$office = nadlan_sg_valid( (string) $r->get_param( 'office' ) );
		$b = nadlan_sg_broker( $office );
		if ( ! $b ) { return nadlan_sg_err( 'הקישור אינו תקף.', 403 ); }
		$did = (int) $r->get_param( 'deal' );
		$d = $did ? nadlan_sg_deal( $did ) : array();
		if ( ! $d || ( $d['office'] ?? '' ) !== $office ) { return nadlan_sg_err( 'בחרו הסכם.' ); }
		$client = nadlan_sg_txt( $r, 'client' ); $tail = nadlan_sg_txt( $r, 'tail', 4 ); $want = nadlan_sg_txt( $r, 'want', 240 );
		if ( '' === $client ) { return nadlan_sg_err( 'חסר שם הלקוח.' ); }
		if ( ! preg_match( '/^\d{3,4}$/', $tail ) ) { return nadlan_sg_err( 'ספרות הטלפון האחרונות: 3 או 4 ספרות.' ); }
		if ( ! $r->get_param( 'consent' ) ) { return nadlan_sg_err( 'יש לאשר שהלקוח הסכים וקיבל גילוי.' ); }
		$g = array( 'deal' => $did, 'office' => $office, 'pname' => $d['pname'], 'dev' => $d['dev'], 'client' => $client, 'tail' => $tail, 'want' => $want,
			'token' => nadlan_sg_token(), 'created' => nadlan_sg_act(), 'deal_signed' => 'signed' === ( $d['status'] ?? '' ) );
		$g['deadline'] = nadlan_sg_deadline( $g['created']['ts'] );
		$g['hash'] = hash( 'sha256', wp_json_encode( array( $g['pname'], $g['dev'], $g['client'], $g['tail'], $g['want'], $g['created']['utc'] ) ) );
		$id = wp_insert_post( array( 'post_type' => 'nadlan_sgreg', 'post_status' => 'private', 'post_title' => $client . ' · ' . $d['pname'] ), true );
		if ( is_wp_error( $id ) ) { return nadlan_sg_err( 'השמירה נכשלה. נסו שוב.', 500 ); }
		update_post_meta( $id, '_nlsg', $g );
		update_post_meta( $id, '_nlsg_token', $g['token'] );
		update_post_meta( $id, '_nlsg_office', $office );
		$url = nadlan_sg_url( 'nlsg_rev', $g['token'] );
		if ( is_email( $d['regto'] ) ) { @wp_mail( $d['regto'], 'רישום לקוח · ' . $d['pname'], "רישום לקוח לפי הסכם שיתוף הפעולה, מאת {$b['name']}:\n{$client}, פרויקט {$d['pname']}, {$g['created']['il']}.\nלבדיקה, לאישור או להתנגדות עד " . nadlan_sg_il( $g['deadline'] ) . ":\n{$url}\n" ); }
		return array( 'ok' => true, 'id' => $id, 'url' => $url, 'deadline' => nadlan_sg_il( $g['deadline'] ),
			'wa' => 'https://wa.me/?text=' . rawurlencode( "רישום לקוח לפי הסכם שיתוף הפעולה, פרויקט {$d['pname']}:\n{$client}, נרשם ב־{$g['created']['il']}.\nלבדיקה ולאישור, עד " . nadlan_sg_il( $g['deadline'] ) . ":\n{$url}\n{$b['name']}, {$b['office']}" ) );
	}

	/** The developer confirms a registration, or objects with an earlier dated record, within the deadline. */
	function nadlan_sg_rest_rev( WP_REST_Request $r ) {
		if ( ! nadlan_sg_limit( 'rev', 30 ) ) { return nadlan_sg_err( 'יותר מדי ניסיונות. נסו שוב בעוד שעה.', 429 ); }
		$id = nadlan_sg_find( 'nadlan_sgreg', '_nlsg_token', (string) $r->get_param( 'token' ) );
		if ( ! $id ) { return nadlan_sg_err( 'הקישור אינו תקף.', 404 ); }
		$g = nadlan_sg_deal( $id );
		if ( ! empty( $g['action'] ) ) { return nadlan_sg_err( 'הרישום כבר טופל.', 409 ); }
		$act = (string) $r->get_param( 'act' ); $name = nadlan_sg_txt( $r, 'name' );
		if ( '' === $name ) { return nadlan_sg_err( 'חסר שם.' ); }
		if ( 'object' === $act ) {
			if ( time() > (int) $g['deadline'] ) { return nadlan_sg_err( 'המועד להתנגדות עבר, והרישום סופי.', 409 ); }
			$when = nadlan_sg_txt( $r, 'when', 20 ); $note = nadlan_sg_txt( $r, 'note', 400 );
			if ( ! preg_match( '/^\d{4}-\d{2}-\d{2}$/', $when ) || strtotime( $when ) > (int) $g['created']['ts'] ) { return nadlan_sg_err( 'תאריך הרישום המוקדם צריך להיות לפני מועד הרישום.' ); }
			if ( mb_strlen( $note ) < 10 ) { return nadlan_sg_err( 'פרטו את התיעוד: פנייה, פגישה או הצעת מחיר.' ); }
			$g['action'] = nadlan_sg_act( array( 'act' => 'object', 'name' => $name, 'when' => $when, 'note' => $note ) );
		} elseif ( 'confirm' === $act ) {
			$g['action'] = nadlan_sg_act( array( 'act' => 'confirm', 'name' => $name ) );
		} else {
			return nadlan_sg_err( 'בחרו פעולה.' );
		}
		update_post_meta( $id, '_nlsg', $g );
		$b = nadlan_sg_broker( $g['office'] );
		if ( ! empty( $b['email'] ) ) { @wp_mail( $b['email'], 'עדכון רישום · ' . $g['client'], ( 'object' === $act ? 'החברה הודיעה על רישום מוקדם' : 'החברה אישרה את הרישום' ) . " · {$g['client']} · {$g['pname']} · {$g['action']['il']}" ); }
		return array( 'ok' => true );
	}

	/** A registration's state for display. */
	function nadlan_sg_reg_state( $g ) {
		if ( ! empty( $g['action']['act'] ) ) {
			return 'object' === $g['action']['act'] ? array( 'obj', 'רישום מוקדם אצל החברה' ) : array( 'ok', 'אושר על ידי החברה' );
		}
		return time() > (int) $g['deadline'] ? array( 'ok', 'סופי · מוגן עד ' . wp_date( 'd.m.Y', strtotime( '+12 months', (int) $g['created']['ts'] ), new DateTimeZone( 'Asia/Jerusalem' ) ) ) : array( 'wait', 'בבדיקה עד ' . nadlan_sg_il( $g['deadline'] ) );
	}

	/* ------------------------------------------------------------------ pages */

	add_action( 'template_redirect', function () {
		foreach ( array( 'nlsg_office', 'nlsg_sign', 'nlsg_rev' ) as $k ) {
			if ( isset( $_GET[ $k ] ) ) {
				$t = nadlan_sg_valid( sanitize_text_field( wp_unslash( $_GET[ $k ] ) ) );
				nocache_headers();
				header( 'Content-Type: text/html; charset=utf-8' );
				header( 'Referrer-Policy: no-referrer' );
				echo nadlan_sg_render( $k, $t ); // phpcs:ignore WordPress.Security.EscapeOutput -- built from escaped parts
				exit;
			}
		}
	}, 0 );

	function nadlan_sg_render( $k, $t ) {
		if ( 'nlsg_office' === $k ) {
			$b = nadlan_sg_broker( $t );
			return $b ? nadlan_sg_shell( 'המשרד של ' . $b['name'], nadlan_sg_office( $t, $b ) ) : nadlan_sg_shell( 'הקישור אינו תקף', nadlan_sg_dead() );
		}
		if ( 'nlsg_sign' === $k ) {
			$id = nadlan_sg_find( 'nadlan_sgdeal', '_nlsg_token', $t );
			return $id ? nadlan_sg_shell( 'הסכם שיתוף פעולה', nadlan_sg_signpage( $id, nadlan_sg_deal( $id ) ) ) : nadlan_sg_shell( 'הקישור אינו תקף', nadlan_sg_dead() );
		}
		$id = nadlan_sg_find( 'nadlan_sgreg', '_nlsg_token', $t );
		if ( ! $id ) { return nadlan_sg_shell( 'הקישור אינו תקף', nadlan_sg_dead() ); }
		$g = nadlan_sg_deal( $id );
		if ( empty( $g['opened'] ) ) { $g['opened'] = nadlan_sg_act(); update_post_meta( $id, '_nlsg', $g ); }
		return nadlan_sg_shell( 'רישום לקוח', nadlan_sg_revpage( $t, $g ) );
	}

	function nadlan_sg_dead() { status_header( 404 ); return '<main class="w"><div class="card"><h1>הקישור אינו תקף</h1><p>ייתכן שהקישור הועתק חלקית. בקשו קישור חדש ממי ששלח אותו.</p></div></main>'; }

	function nadlan_sg_head( $kick, $title, $sub = '' ) {
		return '<header class="hd"><div class="w"><div class="brand">nad-lan.co.il</div><div class="kick">' . esc_html( $kick ) . '</div><h1>' . esc_html( $title ) . '</h1>' . ( $sub ? '<p class="sub">' . $sub . '</p>' : '' ) . '</div></header>';
	}

	function nadlan_sg_sigpad( $label ) {
		return '<div class="f"><label>' . esc_html( $label ) . '</label><div class="pad"><canvas width="900" height="260" data-sig></canvas><button type="button" class="clr" data-clear>ניקוי</button><span class="hint">חתמו כאן באצבע או בעכבר</span></div></div>';
	}

	function nadlan_sg_office( $tok, $b ) {
		$pp = nadlan_sg_projects();
		$opts = '';
		foreach ( $pp as $k => $p ) { $opts .= '<option value="' . esc_attr( $k ) . '">' . esc_html( $p['name'] . ' · ' . $p['dev'] ) . '</option>'; }
		$opts .= '<option value="other">פרויקט אחר</option>';
		$deals = get_posts( array( 'post_type' => 'nadlan_sgdeal', 'post_status' => 'any', 'numberposts' => 100, 'suppress_filters' => true, 'meta_key' => '_nlsg_office', 'meta_value' => $tok ) );
		$regs = get_posts( array( 'post_type' => 'nadlan_sgreg', 'post_status' => 'any', 'numberposts' => 200, 'suppress_filters' => true, 'meta_key' => '_nlsg_office', 'meta_value' => $tok ) );
		$dl = ''; $dopt = '';
		foreach ( $deals as $p ) {
			$d = nadlan_sg_deal( $p->ID ); $u = nadlan_sg_url( 'nlsg_sign', $d['token'] );
			$signed = 'signed' === ( $d['status'] ?? '' );
			$dl .= '<tr><td><b>' . esc_html( $d['pname'] ) . '</b><br>' . esc_html( $d['dev'] ) . '</td><td>' . esc_html( $d['rate'] ) . '%</td><td><span class="st ' . ( $signed ? 'ok' : 'wait' ) . '">' . ( $signed ? 'נחתם ' . esc_html( $d['dsig']['il'] ) : 'ממתין לחתימת החברה' ) . '</span></td><td><a href="' . esc_url( $u ) . '" target="_blank" rel="noopener">' . ( $signed ? 'העותק החתום' : 'קישור החתימה' ) . '</a> · <a href="' . esc_url( 'https://wa.me/?text=' . rawurlencode( 'הסכם שיתוף הפעולה לפרויקט ' . $d['pname'] . ":\n" . $u ) ) . '" target="_blank" rel="noopener">וואטסאפ</a></td></tr>';
			$dopt .= '<option value="' . (int) $p->ID . '">' . esc_html( $d['pname'] . ' · ' . $d['dev'] . ( $signed ? '' : ' (טרם נחתם)' ) ) . '</option>';
		}
		$rl = '';
		foreach ( $regs as $p ) {
			$g = nadlan_sg_deal( $p->ID ); list( $cls, $lab ) = nadlan_sg_reg_state( $g ); $u = nadlan_sg_url( 'nlsg_rev', $g['token'] );
			$rl .= '<tr><td><b>' . esc_html( $g['client'] ) . '</b> · ' . esc_html( $g['tail'] ) . '<br>' . esc_html( $g['pname'] ) . '</td><td>' . esc_html( $g['created']['il'] ) . '</td><td><span class="st ' . $cls . '">' . esc_html( $lab ) . '</span>' . ( ! empty( $g['opened'] ) ? '<br><small>נפתח אצל החברה ' . esc_html( $g['opened']['il'] ) . '</small>' : '' ) . '</td><td><a href="' . esc_url( $u ) . '" target="_blank" rel="noopener">קישור הבדיקה</a></td></tr>';
		}
		$h = nadlan_sg_head( $b['office'] . ' · מתווכת מורשית, רישיון ' . $b['lic'], 'המשרד של ' . $b['name'], 'הסכמי שיתוף עם יזמים ורישום לקוחות. כל פעולה נשמרת עם חותמת זמן.' );
		$h .= '<main class="w"><nav class="tabs"><a href="#deals" class="on" data-tab="deals">הסכמים</a><a href="#regs" data-tab="regs">רישום לקוח</a></nav>';
		$h .= '<section id="deals" class="tab on"><div class="card"><h2>הסכם חדש עם יזם</h2><form data-form="deal">'
			. '<input type="hidden" name="office" value="' . esc_attr( $tok ) . '">'
			. '<div class="f"><label>הפרויקט</label><select name="project" data-proj>' . $opts . '</select></div>'
			. '<div class="other" hidden><div class="f"><label>שם הפרויקט</label><input name="pname"></div><div class="f"><label>מיקום הפרויקט (כפי שיופיע בהסכם)</label><input name="asset"></div></div>'
			. '<div class="row"><div class="f"><label>שם החברה (היזם)</label><input name="dev" required data-dev></div><div class="f"><label>שכר התיווך, אחוז לפני מע״מ</label><input name="rate" inputmode="decimal" placeholder="למשל 1.5" required></div></div>'
			. '<div class="f"><label>לאן נשלחים רישומי לקוחות (מייל או וואטסאפ של החברה)</label><input name="regto" required></div>'
			. '<div class="row"><div class="f"><label>השם המלא שלך</label><input name="signer" value="' . esc_attr( $b['name'] ) . '" required></div><div class="f"><label>תעודת זהות</label><input name="bid" inputmode="numeric" required></div></div>'
			. '<details class="doc"><summary>נוסח ההסכם</summary><div class="docbody">' . nadlan_sg_doc_a( array( 'bname' => $b['name'], 'blic' => $b['lic'], 'boffice' => $b['office'], 'dev' => '', 'asset' => '', 'rate' => '', 'regto' => '', 'bid' => '' ) ) . '</div></details>'
			. '<label class="chk"><input type="checkbox" name="agree" value="1" required> קראתי את נוסח ההסכם, ואני חותמת עליו בחתימה אלקטרונית מחייבת.</label>'
			. nadlan_sg_sigpad( 'החתימה שלך' )
			. '<button class="btn">חתימה והפקת קישור ליזם</button><div class="msg" data-msg></div></form></div>'
			. '<div class="card"><h2>ההסכמים שלך</h2>' . ( $dl ? '<div class="tw"><table><tr><th>פרויקט</th><th>שכר</th><th>מצב</th><th></th></tr>' . $dl . '</table></div>' : '<p class="muted">עוד אין הסכמים.</p>' ) . '</div></section>';
		$h .= '<section id="regs" class="tab"><div class="card"><h2>רישום לקוח</h2><p class="muted">רושמים לפני שמוסרים פרטים. לחברה 2 ימי עסקים לבדיקה, ואז הלקוח שלך ל־12 חודשים בפרויקט.</p>'
			. ( $dopt ? '<form data-form="reg"><input type="hidden" name="office" value="' . esc_attr( $tok ) . '">'
			. '<div class="f"><label>ההסכם</label><select name="deal">' . $dopt . '</select></div>'
			. '<div class="row"><div class="f"><label>שם הלקוח</label><input name="client" required></div><div class="f"><label>4 הספרות האחרונות בטלפון שלו</label><input name="tail" inputmode="numeric" maxlength="4" required></div></div>'
			. '<div class="f"><label>מה מעניין אותו (לא חובה)</label><input name="want" placeholder="קומה, כיוון, מספר חדרים"></div>'
			. '<label class="chk"><input type="checkbox" name="consent" value="1" required> הלקוח הסכים שאציג אותו לחברה, וקיבל ממני גילוי בכתב שהחברה משלמת לי.</label>'
			. '<button class="btn">רישום ושליחה לחברה</button><div class="msg" data-msg></div></form>' : '<p class="muted">קודם פותחים הסכם עם היזם.</p>' )
			. '</div><div class="card"><h2>הלקוחות הרשומים</h2>' . ( $rl ? '<div class="tw"><table><tr><th>לקוח</th><th>נרשם</th><th>מצב</th><th></th></tr>' . $rl . '</table></div>' : '<p class="muted">עוד אין רישומים.</p>' ) . '</div></section></main>';
		return $h;
	}

	function nadlan_sg_signpage( $id, $d ) {
		$signed = 'signed' === ( $d['status'] ?? '' );
		$sigs = '<div class="sigs"><div><img src="' . esc_attr( $d['bsig']['img'] ) . '" alt=""><b>' . esc_html( $d['bsig']['name'] ) . '</b><small>' . esc_html( $d['bname'] . ' · רישיון ' . $d['blic'] ) . '<br>נחתם ' . esc_html( $d['bsig']['il'] ) . '</small></div>';
		if ( $signed ) {
			$sigs .= '<div><img src="' . esc_attr( $d['dsig']['img'] ) . '" alt=""><b>' . esc_html( $d['dsig']['name'] ) . '</b><small>' . esc_html( $d['dsig']['role'] . ' · ' . $d['dev'] ) . '<br>נחתם ' . esc_html( $d['dsig']['il'] ) . '</small></div>';
		}
		$sigs .= '</div>';
		$h = nadlan_sg_head( $d['pname'] . ' · ' . $d['bname'] . ', מתווכת מורשית, רישיון ' . $d['blic'], $signed ? 'ההסכם נחתם' : 'הסכם שיתוף פעולה לחתימה', $signed ? 'זה העותק החתום. שמרו את הקישור, או הדפיסו ושמרו כקובץ.' : 'שני מסמכים: ההסכם עם ' . esc_html( $d['bname'] ) . ' והזמנת הפרסום באתר. חתימה אחת, ועותק חתום לשני הצדדים.' );
		$h .= '<main class="w">';
		if ( $signed ) {
			$h .= '<div class="card doc"><div class="docbody">' . $d['doc_a'] . '</div>' . $sigs . '<p class="ev">טביעת המסמך (SHA-256): ' . esc_html( $d['dsig']['hash_a'] ) . '</p></div>';
			$h .= '<div class="card doc"><div class="docbody">' . $d['doc_b'] . '</div><div class="sigs"><div><img src="' . esc_attr( $d['dsig']['img'] ) . '" alt=""><b>' . esc_html( $d['dsig']['name'] ) . '</b><small>' . esc_html( $d['dsig']['role'] . ' · ' . $d['dev'] ) . '<br>נחתם ' . esc_html( $d['dsig']['il'] ) . '</small></div></div><p class="ev">טביעת המסמך (SHA-256): ' . esc_html( $d['dsig']['hash_b'] ) . '</p></div>';
			$h .= '<div class="card noprint"><button class="btn" type="button" onclick="window.print()">הדפסה או שמירה כקובץ</button></div></main>';
			return $h;
		}
		$h .= '<div class="card doc"><div class="kick">מסמך 1 מתוך 2</div><div class="docbody">' . nadlan_sg_doc_a( $d ) . '</div>' . $sigs . '</div>';
		$h .= '<div class="card doc"><div class="kick">מסמך 2 מתוך 2</div><div class="docbody">' . nadlan_sg_doc_b( $d ) . '</div></div>';
		$h .= '<div class="card"><h2>פרטי החברה והחתימה</h2><form data-form="sign"><input type="hidden" name="token" value="' . esc_attr( $d['token'] ) . '">'
			. '<div class="row"><div class="f"><label>ח.פ.</label><input name="devnum" inputmode="numeric" required></div><div class="f"><label>כתובת החברה</label><input name="devaddr" required></div></div>'
			. '<div class="row"><div class="f"><label>שם מורשה החתימה</label><input name="name" required></div><div class="f"><label>תפקיד</label><input name="role" required></div></div>'
			. '<div class="row"><div class="f"><label>מייל לעותק החתום</label><input name="email" type="email" required></div><div class="f"><label>טלפון</label><input name="phone" inputmode="tel"></div></div>'
			. '<div class="f"><label>מסלול הפרסום</label><div class="plans"><label><input type="radio" name="plan" value="1" required> חודש אחד · 3,990 ₪</label><label><input type="radio" name="plan" value="3"> 3 חודשים · 10,990 ₪</label><label><input type="radio" name="plan" value="6"> 6 חודשים · 19,990 ₪</label></div><small class="muted">כולל מע״מ, כפי שמפורסם באתר.</small></div>'
			. '<label class="chk"><input type="checkbox" name="agree_a" value="1" required> קראתי את הסכם שיתוף הפעולה והזמנת שירותי התיווך, ואני מוסמך/ת לחתום עליו בשם החברה.</label>'
			. '<label class="chk"><input type="checkbox" name="agree_b" value="1" required> קראתי את הזמנת הפרסום, ואני מוסמך/ת לחתום עליה בשם החברה.</label>'
			. nadlan_sg_sigpad( 'חתימת מורשה החתימה' )
			. '<p class="muted">החתימה האלקטרונית מחייבת כחתימה בכתב. נשמרים המועד, כתובת הרשת וטביעת המסמך, ועותק חתום נשלח לשני הצדדים.</p>'
			. '<button class="btn">חתימה על שני המסמכים</button><div class="msg" data-msg></div></form></div></main>';
		return $h;
	}

	function nadlan_sg_revpage( $tok, $g ) {
		list( $cls, $lab ) = nadlan_sg_reg_state( $g );
		$h = nadlan_sg_head( $g['pname'] . ' · ' . $g['dev'], 'רישום לקוח', 'לפי הסכם שיתוף הפעולה. לחברה 2 ימי עסקים לבדיקה.' );
		$h .= '<main class="w"><div class="card"><table class="kv">'
			. '<tr><th>הלקוח</th><td>' . esc_html( $g['client'] ) . ' · טלפון המסתיים ב־' . esc_html( $g['tail'] ) . '</td></tr>'
			. '<tr><th>הפרויקט</th><td>' . esc_html( $g['pname'] ) . '</td></tr>'
			. ( '' !== $g['want'] ? '<tr><th>מה מעניין אותו</th><td>' . esc_html( $g['want'] ) . '</td></tr>' : '' )
			. '<tr><th>מועד הרישום</th><td>' . esc_html( $g['created']['il'] ) . ' (שעון ישראל)</td></tr>'
			. '<tr><th>מועד אחרון לבדיקה</th><td>' . esc_html( nadlan_sg_il( $g['deadline'] ) ) . '</td></tr>'
			. '<tr><th>מצב</th><td><span class="st ' . $cls . '">' . esc_html( $lab ) . '</span></td></tr></table>'
			. ( empty( $g['deal_signed'] ) ? '<p class="muted">ההסכם לפרויקט עוד לא נחתם על ידי החברה. הרישום נשמר עם חותמת זמן.</p>' : '' ) . '</div>';
		if ( empty( $g['action'] ) && time() <= (int) $g['deadline'] ) {
			$h .= '<div class="card"><h2>הבדיקה שלכם</h2><form data-form="rev"><input type="hidden" name="token" value="' . esc_attr( $tok ) . '">'
				. '<div class="f"><label>השם שלך</label><input name="name" required></div>'
				. '<div class="plans"><label><input type="radio" name="act" value="confirm" required data-act> הלקוח אינו רשום אצלנו. מאשרים את הרישום.</label><label><input type="radio" name="act" value="object" data-act> הלקוח כבר רשום אצלנו, לפני מועד הרישום.</label></div>'
				. '<div class="obj" hidden><div class="row"><div class="f"><label>תאריך הרישום המוקדם</label><input type="date" name="when"></div><div class="f"><label>התיעוד (פנייה, פגישה או הצעת מחיר)</label><input name="note"></div></div></div>'
				. '<button class="btn">שליחה</button><div class="msg" data-msg></div></form></div>';
		} elseif ( ! empty( $g['action'] ) ) {
			$a = $g['action'];
			$h .= '<div class="card"><p>' . ( 'object' === $a['act'] ? 'החברה הודיעה על רישום מוקדם מתאריך ' . esc_html( $a['when'] ) . ': ' . esc_html( $a['note'] ) : 'החברה אישרה את הרישום' ) . ' · ' . esc_html( $a['name'] ) . ' · ' . esc_html( $a['il'] ) . '</p></div>';
		}
		return $h . '</main>';
	}

	function nadlan_sg_shell( $title, $body ) {
		$rest = esc_url_raw( rest_url( 'nadlan/v1/sg/' ) );
		$css = <<<'CSS'
:root{--paper:#FAF7F1;--band:#F3EEE3;--hair:#E2DCD0;--ink:#1B1A17;--ink2:#3F3A33;--mute:#7A7266;--gold:#9C7A3C;--gold2:#C9A66B;--brown:#231A12;--ok:#2F6B4A;--warn:#9C6A1C;--bad:#9B3A2A}
*{box-sizing:border-box}html,body{margin:0;background:var(--paper);color:var(--ink)}body{font:16px/1.65 "Heebo",Arial,sans-serif;direction:rtl}
.w{max-width:880px;margin:0 auto;padding:0 16px}.hd{background:var(--brown);color:#EFE7D8;padding:34px 0 30px;margin-bottom:22px}
.brand{font-size:13px;letter-spacing:.14em;color:var(--gold2)}.kick{font-size:13px;letter-spacing:.1em;color:var(--gold);margin:12px 0 6px}.hd .kick{color:#BFB29C}
h1,h2{font-family:"Frank Ruhl Libre",Georgia,serif;line-height:1.2;margin:0 0 10px;text-wrap:balance}h1{font-size:34px;color:#F7F1E6}h2{font-size:23px}
.sub{color:#D9CFBF;margin:4px 0 0}.card{background:#fff;border:1px solid var(--hair);border-radius:16px;padding:22px 20px;margin:0 0 18px}
.muted,small{color:var(--mute)}.tabs{display:flex;gap:8px;margin:0 0 16px}.tabs a{padding:9px 18px;border-radius:99px;border:1px solid var(--hair);color:var(--ink);text-decoration:none;background:#fff}.tabs a.on{background:var(--brown);color:#F7F1E6;border-color:var(--brown)}
.tab{display:none}.tab.on{display:block}.f{margin:0 0 14px}.f label{display:block;font-size:14px;font-weight:500;margin:0 0 5px}
input,select{width:100%;font:inherit;padding:11px 12px;border:1px solid #D6CEBF;border-radius:10px;background:#fff;color:var(--ink)}input:focus,select:focus{outline:2px solid var(--gold2);outline-offset:1px}
.row{display:grid;grid-template-columns:1fr 1fr;gap:12px}@media(max-width:620px){.row{grid-template-columns:1fr}h1{font-size:27px}}
.chk{display:flex;gap:10px;align-items:flex-start;margin:0 0 12px;font-size:15px}.chk input,.plans input{width:auto;margin-top:5px}
.plans{display:grid;gap:8px}.plans label{display:flex;gap:10px;align-items:flex-start;border:1px solid var(--hair);border-radius:10px;padding:10px 12px;background:var(--paper)}
.pad{position:relative;border:1px dashed var(--gold);border-radius:12px;background:var(--paper)}.pad canvas{display:block;width:100%;height:150px;touch-action:none;cursor:crosshair}
.pad .clr{position:absolute;left:8px;top:8px;font:inherit;font-size:13px;border:1px solid var(--hair);background:#fff;border-radius:99px;padding:3px 12px;cursor:pointer}.pad .hint{position:absolute;right:12px;bottom:8px;font-size:12px;color:var(--mute);pointer-events:none}
.btn{display:inline-block;font:inherit;font-weight:500;background:var(--brown);color:#F7F1E6;border:0;border-radius:99px;padding:13px 26px;cursor:pointer;min-height:48px}.btn:disabled{opacity:.6}
.msg{margin-top:12px;font-size:15px}.msg.err{color:var(--bad)}.msg.ok{color:var(--ok)}.msg a{color:var(--gold);font-weight:500;word-break:break-all}
.doc .docbody{font-size:15px;color:var(--ink2)}.doc .docbody h2{font-size:21px;color:var(--ink)}.doc ol{padding-right:22px;margin:0}.doc li{margin:0 0 8px}.doc i{color:var(--gold);font-style:normal;border-bottom:1px dotted var(--gold)}
details.doc{border:1px solid var(--hair);border-radius:12px;padding:10px 14px;margin:0 0 14px;background:var(--paper)}details.doc summary{cursor:pointer;font-weight:500}
.sigs{display:flex;flex-wrap:wrap;gap:22px;margin-top:16px;border-top:1px solid var(--hair);padding-top:14px}.sigs div{flex:1 1 220px}.sigs img{display:block;max-width:100%;height:80px;object-fit:contain;object-position:right}.sigs b{display:block}
.ev{font-size:12px;color:var(--mute);word-break:break-all;margin-top:10px}table{width:100%;border-collapse:collapse;font-size:14px}.tw{overflow-x:auto}th,td{text-align:right;padding:9px 8px;border-bottom:1px solid var(--hair);vertical-align:top}th{font-weight:500;color:var(--mute)}
.kv th{width:34%}.st{display:inline-block;border-radius:99px;padding:2px 10px;font-size:13px}.st.ok{background:#E3EFE7;color:var(--ok)}.st.wait{background:#F5ECDA;color:var(--warn)}.st.obj{background:#F4E1DC;color:var(--bad)}
a{color:var(--gold)}@media print{.hd{background:none;color:var(--ink)}.hd h1{color:var(--ink)}.noprint,.tabs{display:none}.card{border:0;padding:0}}
CSS;
		$js = <<<'JS'
(function(){var R=document.body.getAttribute('data-rest');
document.querySelectorAll('[data-tab]').forEach(function(a){a.addEventListener('click',function(e){e.preventDefault();document.querySelectorAll('[data-tab]').forEach(function(x){x.classList.toggle('on',x===a)});document.querySelectorAll('.tab').forEach(function(s){s.classList.toggle('on',s.id===a.getAttribute('data-tab'))})})});
document.querySelectorAll('[data-proj]').forEach(function(s){var o=s.form.querySelector('.other');s.addEventListener('change',function(){o.hidden=s.value!=='other'})});
document.querySelectorAll('[data-act]').forEach(function(r){r.addEventListener('change',function(){var o=r.form.querySelector('.obj');if(o)o.hidden=r.form.act.value!=='object'})});
document.querySelectorAll('canvas[data-sig]').forEach(function(c){var x=c.getContext('2d'),d=false,n=0;x.lineWidth=3.2;x.lineCap='round';x.lineJoin='round';x.strokeStyle='#1B1A17';
function p(e){var b=c.getBoundingClientRect();return[(e.clientX-b.left)*c.width/b.width,(e.clientY-b.top)*c.height/b.height]}
c.addEventListener('pointerdown',function(e){d=true;c.setPointerCapture(e.pointerId);var q=p(e);x.beginPath();x.moveTo(q[0],q[1]);n++});
c.addEventListener('pointermove',function(e){if(!d)return;var q=p(e);x.lineTo(q[0],q[1]);x.stroke()});
['pointerup','pointercancel','pointerleave'].forEach(function(t){c.addEventListener(t,function(){d=false})});
c.parentNode.querySelector('[data-clear]').addEventListener('click',function(){x.clearRect(0,0,c.width,c.height);n=0});c._n=function(){return n}});
document.querySelectorAll('form[data-form]').forEach(function(f){f.addEventListener('submit',function(e){e.preventDefault();var m=f.querySelector('[data-msg]'),b=f.querySelector('.btn'),o={};
new FormData(f).forEach(function(v,k){o[k]=v});var c=f.querySelector('canvas[data-sig]');if(c){if(!c._n()){m.className='msg err';m.textContent='חסרה חתימה.';return}o.sig=c.toDataURL('image/png')}
b.disabled=true;m.className='msg';m.textContent='שולחים...';
fetch(R+f.getAttribute('data-form'),{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(o)}).then(function(r){return r.json()}).then(function(j){b.disabled=false;
if(!j.ok){m.className='msg err';m.textContent=j.error||'משהו השתבש. נסו שוב.';return}
if(j.copy){location.href=j.copy;return}
if(j.url){m.className='msg ok';m.innerHTML='';var t=document.createElement('div');t.textContent=(j.deadline?'נרשם. מועד אחרון לבדיקה: '+j.deadline+'. ':'נחתם. ')+'הקישור לחברה:';var a=document.createElement('a');a.href=j.url;a.textContent=j.url;a.target='_blank';var w=document.createElement('a');w.href=j.wa;w.target='_blank';w.rel='noopener';w.className='btn';w.style.marginTop='10px';w.textContent='שליחה בוואטסאפ';m.appendChild(t);m.appendChild(a);m.appendChild(document.createElement('br'));m.appendChild(w);return}
m.className='msg ok';m.textContent='נשלח. תודה.';setTimeout(function(){location.reload()},1200)}).catch(function(){b.disabled=false;m.className='msg err';m.textContent='אין חיבור. נסו שוב.'})})});
})();
JS;
		return '<!doctype html><html lang="he" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>' . esc_html( $title ) . ' · nad-lan.co.il</title>'
			. '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Frank+Ruhl+Libre:wght@500;700&family=Heebo:wght@400;500;700&display=swap" rel="stylesheet">'
			. '<style>' . $css . '</style></head><body data-rest="' . esc_attr( $rest ) . '">' . $body . '<script>' . $js . '</script></body></html>';
	}
}
