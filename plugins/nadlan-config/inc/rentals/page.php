<?php
/**
 * nadlan-config - RENTALS v2: the /my-rentals/ page (HAD-383, 1.10.2026).
 *
 * One URL, three faces (no new URL, URL-word law):
 *  - a visitor sees the public landing (indexable, he + en via ?lang=en with
 *    hreflang, as v1) with the full app running on sample data;
 *  - a logged-in landlord sees his app (private, no-cache, as v1);
 *  - anyone arriving with a personal link (#t= #s= #a= #v= #q=) sees the
 *    link page; the fragment never reaches the server or a link preview.
 */

if ( ! defined( 'ABSPATH' ) ) { exit; }

if ( ! function_exists( 'nlrm_me' ) ) {
	function nlrm_me( $owner ) {
		$u = get_userdata( $owner );
		$pay = (array) get_user_meta( $owner, 'nlrm_pay', true );
		return array(
			'display' => (string) ( get_user_meta( $owner, 'nlrm_display', true ) ?: ( $u ? $u->display_name : '' ) ),
			'phone'   => nlrm_phone( (string) get_user_meta( $owner, 'nlrm_phone', true ) ),
			'pay'     => array( 'bank' => (string) ( $pay['bank'] ?? '' ), 'bit' => nlrm_phone( (string) ( $pay['bit'] ?? '' ) ), 'link' => (string) ( $pay['link'] ?? '' ) ),
			'notify'  => 'off' !== (string) get_user_meta( $owner, 'nlrm_notify', true ),
		);
	}
}

add_action( 'rest_api_init', function () {
	register_rest_route( 'nadlan/v1', '/rm/me', array(
		'methods' => 'POST',
		'permission_callback' => function () { return nadlan_rm_on() && is_user_logged_in() && 'owner' === nlrm_role(); },
		'callback' => function ( WP_REST_Request $r ) {
			$o = nlrm_owner();
			if ( null !== $r->get_param( 'display' ) ) { update_user_meta( $o, 'nlrm_display', mb_substr( sanitize_text_field( (string) $r->get_param( 'display' ) ), 0, 80 ) ); }
			if ( null !== $r->get_param( 'phone' ) ) { update_user_meta( $o, 'nlrm_phone', nlrm_phone( (string) $r->get_param( 'phone' ) ) ); }
			if ( null !== $r->get_param( 'pay' ) ) {
				$p = (array) $r->get_param( 'pay' );
				update_user_meta( $o, 'nlrm_pay', array( 'bank' => mb_substr( sanitize_textarea_field( (string) ( $p['bank'] ?? '' ) ), 0, 300 ), 'bit' => nlrm_phone( (string) ( $p['bit'] ?? '' ) ), 'link' => esc_url_raw( (string) ( $p['link'] ?? '' ) ) ) );
			}
			if ( null !== $r->get_param( 'notify' ) ) { update_user_meta( $o, 'nlrm_notify', $r->get_param( 'notify' ) ? 'on' : 'off' ); }
			if ( in_array( (string) $r->get_param( 'lang' ), array( 'he', 'en' ), true ) ) { update_user_meta( $o, 'nlrm_lang', (string) $r->get_param( 'lang' ) ); }
			if ( null !== $r->get_param( 'idno' ) ) { update_user_meta( $o, 'nlrm_idno_enc', nlrm_enc( mb_substr( sanitize_text_field( (string) $r->get_param( 'idno' ) ), 0, 20 ) ) ); }
			nlrm_event( $o, '', '', 0, 'settings', '', '', array() );
			return nlrm_me( $o );
		},
	) );
} );

if ( ! function_exists( 'nlrm_assets' ) ) {
	function nlrm_assets( $with_demo ) {
		$v = defined( 'NADLAN_CONFIG_VERSION' ) ? NADLAN_CONFIG_VERSION : '2';
		wp_enqueue_style( 'nlrm', NLRM_URL_ASSETS . 'rm.css', array(), $v );
		wp_enqueue_script( 'nlrm-core', NLRM_URL_ASSETS . 'rm-core.js', array(), $v, true );
		wp_enqueue_script( 'nlrm-demo', NLRM_URL_ASSETS . 'rm-demo.js', array( 'nlrm-core' ), $v, true ); /* also in the app: "look at a sample file first" */
		foreach ( array( 'views', 'drawers', 'lease', 'import', 'portal', 'boot' ) as $f ) {
			wp_enqueue_script( 'nlrm-' . $f, NLRM_URL_ASSETS . 'rm-' . $f . '.js', array( 'nlrm-core' ), $v, true );
		}
		add_action( 'wp_head', function () use ( $v ) {
			echo '<script type="importmap" id="nlrm-importmap">{"imports":{"three":"https://cdn.jsdelivr.net/npm/three@0.170.0/build/three.module.js","three/addons/":"https://cdn.jsdelivr.net/npm/three@0.170.0/examples/jsm/"}}</script>' . "\n";
			echo '<script type="module" src="' . esc_url( NLRM_URL_ASSETS . 'rm-3d.js?ver=' . rawurlencode( $v ) ) . '"></script>' . "\n";
		}, 2 );
	}
}

if ( ! function_exists( 'nlrm_render_page' ) ) {
	function nlrm_render_page( $mode, $lang ) {
		$en = 'en' === $lang;
		$he_url = home_url( '/my-rentals/' );
		$en_url = home_url( '/my-rentals/?lang=en' );
		$self = $en ? $en_url : $he_url;
		header( 'Referrer-Policy: same-origin' );
		if ( 'app' === $mode ) {
			nocache_headers();
			header( 'X-Robots-Tag: noindex, nofollow' ); /* unchanged from v1: a private, logged-in view */
		} else {
			$title = $en ? 'Manage Your Own Rental in Israel, Free: Leases, Rent and Repairs in One Place | NadLan' : 'ניהול השכרות בעצמכם, בחינם: חוזים, שכר דירה ותקלות במקום אחד | נדלן';
			$desc = $en
				? 'Manage your own rental in Israel, free, in English or Hebrew: leases with e-signature, rent and cheque tracking, CPI linkage from the CBS, repairs with legal deadlines, encrypted documents, a WhatsApp link for every tenant, and a full guide.'
				: 'ניהול השכרות בעצמכם, בחינם: חוזה וחתימה דיגיטלית, מעקב שכר דירה וצ\'קים, הצמדה למדד מהלמ"ס, תקלות עם המועד שבחוק, מסמכים מוצפנים, קישור בוואטסאפ לכל שוכר ומדריך מלא.';
			add_filter( 'pre_get_document_title', function () use ( $title ) { return $title; }, 99 );
			add_action( 'wp_head', function () use ( $desc, $self, $he_url, $en_url ) {
				echo '<meta name="description" content="' . esc_attr( $desc ) . '">' . "\n";
				echo '<link rel="canonical" href="' . esc_url( $self ) . '">' . "\n";
				echo '<link rel="alternate" hreflang="he" href="' . esc_url( $he_url ) . '">' . "\n";
				echo '<link rel="alternate" hreflang="en" href="' . esc_url( $en_url ) . '">' . "\n";
				echo '<link rel="alternate" hreflang="x-default" href="' . esc_url( $he_url ) . '">' . "\n";
			}, 4 );
		}
		nlrm_assets( 'app' !== $mode );
		$o = 'app' === $mode ? nlrm_owner() : 0;
		$he = nlrm_json( 'he' ); $enj = nlrm_json( 'en' );
		$cfg = array(
			'mode' => $mode, 'lang' => $lang, 'rest' => esc_url_raw( rest_url( 'nadlan/v1' ) ),
			'nonce' => is_user_logged_in() ? wp_create_nonce( 'wp_rest' ) : '',
			'me' => $o ? nlrm_me( $o ) : null,
			'mapbox' => function_exists( 'nadlan_mapbox_token' ) ? nadlan_mapbox_token() : '',
			'urls' => array( 'pros' => home_url( '/professionals/' ), 'wizard' => home_url( '/post-listing/' ), 'login' => wp_login_url( $self ), 'self' => $self ),
			'langUrls' => array( 'he' => $he_url, 'en' => $en_url ),
			'triage' => nlrm_json( 'triage' ),
			'assets' => NLRM_URL_ASSETS, 'ver' => defined( 'NADLAN_CONFIG_VERSION' ) ? NADLAN_CONFIG_VERSION : '',
		);
		/* one H1: the block theme's compat header prints the site name as an h1 (directory.php demotes it) */
		if ( function_exists( 'nadlan_dir_header_single_h1' ) ) { nadlan_dir_header_single_h1(); } else { get_header(); }
		$dir = $en ? 'ltr' : 'rtl';
		?>
<main class="nlrm-page" dir="<?php echo esc_attr( $dir ); ?>" lang="<?php echo esc_attr( $lang ); ?>">
<script type="application/json" id="nlrm-cfg"><?php echo wp_json_encode( $cfg, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES ); ?></script>
<script type="application/json" id="nlrm-i18n"><?php echo wp_json_encode( array( 'he' => $he, 'en' => $enj ), JSON_UNESCAPED_UNICODE ); ?></script>
<script type="application/json" id="nlrm-lease"><?php echo wp_json_encode( nlrm_json( 'lease' ), JSON_UNESCAPED_UNICODE ); ?></script>
<?php if ( 'app' === $mode ) : ?>
	<h1 class="nlrm-h1"><?php echo esc_html( $en ? 'My rental properties' : 'הנכסים המושכרים שלי' ); ?></h1>
	<div id="nlrm-root" data-mode="app"></div>
<?php else : ?>
	<header class="nlrm-hero" id="nlrm-hero">
		<p class="nlrm-kicker"><?php echo esc_html( $en ? 'For landlords who manage their own rentals' : 'לבעלי דירות שמנהלים את ההשכרה בעצמם' ); ?></p>
		<h1><?php echo esc_html( $en ? 'Manage your own rental: the lease, the rent and the repairs in one place' : 'ניהול השכרות בעצמכם: החוזה, שכר הדירה והתקלות במקום אחד' ); ?></h1>
		<p class="nlrm-hero-lead"><?php echo esc_html( $en
			? 'A digital file for every apartment you rent out: the lease and its signature, rent and cheques, CPI linkage from the Central Bureau of Statistics, repairs with the deadline the law gives, and documents stored encrypted. Each tenant gets a personal WhatsApp link: no app, no password. In English and in Hebrew.'
			: 'תיק דיגיטלי לכל דירה מושכרת: החוזה והחתימה, שכר הדירה והצ\'קים, הצמדה למדד מהלשכה המרכזית לסטטיסטיקה, תקלות עם המועד שהחוק נותן לתיקון, ומסמכים שנשמרים מוצפנים. כל שוכר מקבל קישור אישי בוואטסאפ, בלי אפליקציה ובלי סיסמה. בעברית ובאנגלית.' ); ?></p>
		<div class="nlrm-hero-ctas">
			<a class="nlrm-btn nlrm-btn--primary" href="<?php echo esc_url( is_user_logged_in() ? $self : wp_login_url( $self ) ); ?>"><?php echo esc_html( $en ? 'Start managing, free' : 'מתחילים לנהל, בחינם' ); ?></a>
			<a class="nlrm-btn nlrm-btn--secondary" href="#nlrm-sample"><?php echo esc_html( $en ? 'See a landlord\'s file' : 'לתיק לדוגמה' ); ?></a>
			<a class="nlrm-btn nlrm-btn--quiet" href="<?php echo esc_url( $en ? $he_url : $en_url ); ?>" lang="<?php echo $en ? 'he' : 'en'; ?>"><?php echo $en ? 'עברית' : 'English'; ?></a>
		</div>
		<ul class="nlrm-hero-facts">
			<li><?php echo esc_html( $en ? 'Rent goes straight from the tenant to you, never through us' : 'שכר הדירה עובר ישירות מהשוכר אליכם, לא דרכנו' ); ?></li>
			<li><?php echo esc_html( $en ? 'Fair Rental Law rules built in: the deposit cap, 3 and 30 repair days, 90 and 60 notice days' : 'כללי חוק השכירות בפנים: תקרת הביטחונות, 3 ו-30 ימים לתיקון, 90 ו-60 ימי הודעה' ); ?></li>
			<li><?php echo esc_html( $en ? 'Tenants\' details are encrypted and private to you' : 'פרטי השוכרים מוצפנים ופרטיים לכם בלבד' ); ?></li>
		</ul>
	</header>
	<section class="nlrm-sample" id="nlrm-sample" aria-labelledby="nlrm-sample-h">
		<h2 id="nlrm-sample-h"><?php echo esc_html( $en ? 'A landlord\'s file with five apartments' : 'תיק של בעל דירות עם חמש דירות' ); ?></h2>
		<p class="nlrm-hero-lead"><?php echo esc_html( $en ? 'Tap anything: an apartment in the building, a tenant, a payment, a repair. Sample data; nothing is sent.' : 'לחצו על הכול: דירה בבניין, שוכר, תשלום, תקלה. נתוני דוגמה, שום דבר לא נשלח.' ); ?></p>
		<div id="nlrm-root" data-mode="demo"></div>
	</section>
	<?php
	/* the public guide (HAD-383): server-rendered in the page's language from assets/rentals/guide/<lang>.html */
	$gf = NLRM_DIR_ASSETS . 'guide/' . ( $en ? 'en' : 'he' ) . '.html';
	if ( is_readable( $gf ) ) {
		echo '<link rel="stylesheet" href="' . esc_url( NLRM_URL_ASSETS . 'guide/guide.css?ver=' . rawurlencode( defined( 'NADLAN_CONFIG_VERSION' ) ? NADLAN_CONFIG_VERSION : '1' ) ) . '">' . "
";
		echo wp_kses_post( (string) file_get_contents( $gf ) ); // phpcs:ignore
	}
	?>
	<section class="nlrm-faq">
		<h2><?php echo esc_html( $en ? 'Questions landlords ask' : 'שאלות של בעלי דירות' ); ?></h2>
		<?php
		$faq = $en ? array(
			array( 'Does the rent go through NadLan?', 'No. Rent goes straight from the tenant to you, by transfer, standing order, Bit or cheques. NadLan tracks it, reminds and reconciles; your tenant can report "I paid" from the personal link and you confirm it.' ),
			array( 'Can my tenant use it in English?', 'Yes. Every tenant has a language: the portal, the lease translation and every WhatsApp message are in that language, while you work in yours.' ),
			array( 'Who sees my tenants\' details?', 'Inside rental management, your account: names, phones, ID numbers and documents are stored encrypted, and each tenant sees through his personal link only what belongs to his own lease. You can download everything or delete it at any time.' ),
			array( 'Is the lease legally valid with an electronic signature?', 'A lease may be signed electronically. The signature is kept with the exact text signed, its date and time. The template follows the Rental and Borrowing Law; for a complex deal, a lawyer\'s review is worth it.' ),
		) : array(
			array( 'שכר הדירה עובר דרך נדלן?', 'לא. שכר הדירה עובר ישירות מהשוכר אליכם, בהעברה, בהוראת קבע, בביט או בצ\'קים. נדלן עוקבת, מזכירה ומתאימה, והשוכר יכול לדווח "שילמתי" מהקישור האישי ואתם מאשרים.' ),
			array( 'השוכר שלי מדבר אנגלית. זה עובד?', 'כן. לכל שוכר יש שפה: הפורטל, תרגום החוזה וכל הודעת וואטסאפ אליו כתובים בשפה שלו, ואתם עובדים בשפה שלכם.' ),
			array( 'מי רואה את פרטי השוכרים?', 'בתוך ניהול ההשכרות, החשבון שלכם: שמות, טלפונים, תעודות זהות ומסמכים נשמרים מוצפנים, וכל שוכר רואה דרך הקישור האישי שלו רק את מה ששייך לחוזה שלו. אפשר להוריד את כל המידע או למחוק אותו בכל רגע.' ),
			array( 'חוזה שנחתם בחתימה דיגיטלית תקף?', 'אפשר לחתום על חוזה שכירות חתימה אלקטרונית. החתימה נשמרת יחד עם הנוסח המדויק, התאריך והשעה. התבנית בנויה לפי חוק השכירות והשאילה, ובעסקה מורכבת כדאי לעבור עליה עם עורך דין.' ),
		);
		foreach ( $faq as $qa ) { echo '<details><summary>' . esc_html( $qa[0] ) . '</summary><p>' . esc_html( $qa[1] ) . '</p></details>'; }
		?>
		<script type="application/ld+json"><?php echo wp_json_encode( array( '@context' => 'https://schema.org', '@type' => 'FAQPage', 'mainEntity' => array_map( function ( $qa ) { return array( '@type' => 'Question', 'name' => $qa[0], 'acceptedAnswer' => array( '@type' => 'Answer', 'text' => $qa[1] ) ); }, $faq ) ), JSON_UNESCAPED_UNICODE ); ?></script>
	</section>
	<p class="nlrm-legal"><?php echo esc_html( $en ? 'Tax and CPI figures are estimates; the binding figures come from the Tax Authority and the lease.' : 'נתוני המס וההצמדה הם אומדן; המספרים המחייבים הם של רשות המסים ושל החוזה.' ); ?></p>
<?php endif; ?>
</main>
<?php
		get_footer();
	}
}
