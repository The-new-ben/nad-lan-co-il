<?php
/**
 * nadlan-config - public advertiser media kit (v1.41.3)
 *
 * /advertise/ is the customer-facing sales surface for the advertiser journey:
 * clear packages, fixed duration, billing CTAs, reporting promise, and policies.
 */
if ( ! defined( 'ABSPATH' ) ) { exit; }

add_action( 'init', function () {
	add_rewrite_rule( '^advertise/?$', 'index.php?nadlan_advertise=1', 'top' );
	add_rewrite_tag( '%nadlan_advertise%', '1' );
} );

add_action( 'init', function () {
	if ( get_option( 'nadlan_advertise_rewrite_v1' ) !== '1' ) {
		flush_rewrite_rules( false );
		update_option( 'nadlan_advertise_rewrite_v1', '1' );
	}
}, 99 );

if ( ! function_exists( 'nadlan_adv_is_page' ) ) {
	function nadlan_adv_is_page() {
		if ( get_query_var( 'nadlan_advertise' ) ) { return true; }
		return is_page() && get_post_field( 'post_name', get_queried_object_id() ) === 'advertise';
	}
}

add_action( 'template_redirect', function () {
	if ( ! get_query_var( 'nadlan_advertise' ) ) { return; }
	get_header();
	echo nadlan_adv_render();
	get_footer();
	exit;
}, 7 );

add_shortcode( 'nadlan_advertise', 'nadlan_adv_render' );

if ( ! function_exists( 'nadlan_adv_snapshot' ) ) {
	function nadlan_adv_snapshot() {
		$lead_q = new WP_Query( array(
			'post_type'      => 'nadlan_lead',
			'post_status'    => 'any',
			'posts_per_page' => 1,
			'fields'         => 'ids',
			'date_query'     => array(
				array( 'after' => '30 days ago' ),
			),
		) );
		$leads_30 = (int) $lead_q->found_posts;
		wp_reset_postdata();

		$views_q = new WP_Query( array(
			'post_type'      => array( 'nadlan_professional', 'nadlan_project', 'nadlan_property' ),
			'post_status'    => 'publish',
			'posts_per_page' => 250,
			'fields'         => 'ids',
			'meta_query'     => array(
				array( 'key' => 'view_count', 'compare' => 'EXISTS' ),
			),
		) );
		$views = 0;
		foreach ( $views_q->posts as $post_id ) {
			$views += max( 0, (int) get_post_meta( $post_id, 'view_count', true ) );
		}
		wp_reset_postdata();

		return array(
			'professionals' => (int) wp_count_posts( 'nadlan_professional' )->publish,
			'projects'      => (int) wp_count_posts( 'nadlan_project' )->publish,
			'properties'    => (int) wp_count_posts( 'nadlan_property' )->publish,
			'leads_30'      => $leads_30,
			'views'         => $views,
		);
	}
}

if ( ! function_exists( 'nadlan_adv_packages' ) ) {
	function nadlan_adv_packages() {
		return array(
			array(
				'id'       => 476,
				'name'     => 'Pro לבעלי מקצוע',
				'price'    => '₪349',
				'period'   => '30 יום',
				'audience' => 'קבלנים, עורכי דין, שמאים, יועצי משכנתאות ואנשי שירות',
				'promise'  => 'כרטיס פתוח עם פרטי קשר, תמונות, טופס פנייה וקידום מעל כרטיסי Free.',
				'proof'    => 'המערכת מודדת צפיות, פניות והשלמת כרטיס במרכז הפרסום.',
				'href'     => home_url( '/?add-to-cart=476&ref=advertise' ),
			),
			array(
				'id'       => 477,
				'name'     => 'Premier לבעלי מקצוע',
				'price'    => '₪749',
				'period'   => '30 יום',
				'audience' => 'מותגים מקומיים שרוצים להיות בחמישייה הראשונה בעיר/מקצוע.',
				'promise'  => 'כל Pro בתוספת תיעדוף גבוה יותר, תג פרימיום ומסלול לדוח חודשי.',
				'proof'    => 'לא מוכרים הבטחת תנועה; מוכרים מיקום, נכס דיגיטלי ודוח.',
				'href'     => home_url( '/?add-to-cart=477&ref=advertise' ),
			),
			array(
				'id'       => 489,
				'name'     => 'קמפיין פרויקט',
				'price'    => '₪3,990',
				'period'   => '6 חודשים',
				'audience' => 'יזמים ומנהלי שיווק לפרויקטים של התחדשות עירונית ובנייה חדשה.',
				'promise'  => 'עמוד פרויקט, הופעה ב-/projects/, טופס לידים, גלריה, מפה, סטטוס תכנון ודוח.',
				'proof'    => 'המסלול מתחבר לתשלום, לכרטיס פרויקט ולמרכז הפרסום אחרי checkout.',
				'href'     => home_url( '/?add-to-cart=489&ref=advertise' ),
			),
			array(
				'id'       => 490,
				'name'     => 'נכס מקודם',
				'price'    => '₪299',
				'period'   => '60 יום',
				'audience' => 'מוכרים פרטיים, משווקים וסוכנויות עם נכס אחד שצריך יותר נראות.',
				'promise'  => 'מודעת נכס עם גלריה, טופס פנייה, מיקום בולט ומדידת צפיות/פניות.',
				'proof'    => 'הקידום מוגבל בזמן כדי שלא תהיה “פרימיום לנצח” אחרי תשלום אחד.',
				'href'     => home_url( '/?add-to-cart=490&ref=advertise' ),
			),
		);
	}
}

if ( ! function_exists( 'nadlan_adv_render' ) ) {
	function nadlan_adv_render() {
		$snapshot = nadlan_adv_snapshot();
		$hero_img = function_exists( 'get_theme_file_uri' ) ? get_theme_file_uri( 'assets/branding/og-default.jpg' ) : '';
		ob_start();
		?>
<main class="nladv" dir="rtl">
	<section class="nladv-hero"<?php echo $hero_img ? ' style="--nladv-hero:url(' . esc_url( $hero_img ) . ')"' : ''; ?>>
		<div class="nladv-hero-inner">
			<p class="nladv-kicker">פרסום נדל"ן שמודדים</p>
			<h1>פרסמו פרויקט, כרטיס מקצועי או נכס - עם תשלום, עריכה ודוח במקום אחד</h1>
			<p class="nladv-lede">נדל"ן חכם מוכר נכס דיגיטלי, מיקום, תקופה ודיווח. בלי הבטחות תנועה ריקות, בלי “חשיפה” לא מוגדרת, ובלי תשלום שהופך לפרימיום לנצח.</p>
			<div class="nladv-actions">
				<a class="nladv-btn gold" href="#packages">מסלולי פרסום</a>
				<a class="nladv-btn ghost" href="<?php echo esc_url( home_url( '/advertiser-center/' ) ); ?>">מרכז הפרסום</a>
			</div>
		</div>
	</section>

	<section class="nladv-band nladv-snapshot" aria-label="תמונת מצב">
		<div><strong><?php echo number_format_i18n( $snapshot['professionals'] ); ?></strong><span>כרטיסי בעלי מקצוע</span></div>
		<div><strong><?php echo number_format_i18n( $snapshot['projects'] ); ?></strong><span>פרויקטים במאגר</span></div>
		<div><strong><?php echo number_format_i18n( $snapshot['properties'] ); ?></strong><span>נכסים זמינים</span></div>
		<div><strong><?php echo number_format_i18n( $snapshot['leads_30'] ); ?></strong><span>פניות שנוצרו ב-30 יום</span></div>
		<div><strong><?php echo number_format_i18n( $snapshot['views'] ); ?></strong><span>צפיות פנימיות מצטברות</span></div>
	</section>

	<section class="nladv-section">
		<div class="nladv-head">
			<p class="nladv-kicker">מה מקבלים</p>
			<h2>חבילות עם נכס, מיקום, תקופה ודוח</h2>
			<p>העמוד הזה נכתב בשביל מנהלי שיווק ואנשי מקצוע ששואלים את השאלה הנכונה: “מה בדיוק קורה אחרי שאני משלם?”</p>
		</div>
		<div id="packages" class="nladv-packages">
			<?php foreach ( nadlan_adv_packages() as $pkg ) : ?>
				<article class="nladv-package">
					<div class="nladv-package-top">
						<span class="nladv-pill">מוצר <?php echo (int) $pkg['id']; ?></span>
						<h3><?php echo esc_html( $pkg['name'] ); ?></h3>
						<div class="nladv-price"><?php echo esc_html( $pkg['price'] ); ?> <small><?php echo esc_html( $pkg['period'] ); ?></small></div>
					</div>
					<p class="nladv-muted"><?php echo esc_html( $pkg['audience'] ); ?></p>
					<ul>
						<li><?php echo esc_html( $pkg['promise'] ); ?></li>
						<li><?php echo esc_html( $pkg['proof'] ); ?></li>
					</ul>
					<a class="nladv-card-btn" href="<?php echo esc_url( $pkg['href'] ); ?>">התחילו</a>
				</article>
			<?php endforeach; ?>
		</div>
	</section>

	<section class="nladv-band nladv-flow">
		<div><b>1</b><span>בוחרים מסלול</span></div>
		<div><b>2</b><span>משלמים ב-WooCommerce</span></div>
		<div><b>3</b><span>מחברים לכרטיס או פרויקט</span></div>
		<div><b>4</b><span>מעלים תמונות ופרטים ב-Studio</span></div>
		<div><b>5</b><span>מקבלים פניות ודוח</span></div>
	</section>

	<section class="nladv-section nladv-grid2">
		<div>
			<p class="nladv-kicker">סטנדרט פרימיום</p>
			<h2>מה נדרש כדי שהפרסום יראה יוקרתי</h2>
			<ul class="nladv-checks">
				<li>תמונת hero או הדמיה איכותית.</li>
				<li>גלריה, מפה, וידאו או סיור תלת-ממדי אם קיים.</li>
				<li>תיאור ברור: למי זה מתאים, איפה זה נמצא, ומה הסטטוס.</li>
				<li>פרטי קשר, טופס ליד, וואטסאפ או טלפון לפי המסלול.</li>
				<li>תג אימות כשבדקנו בעלות, רישיון או זהות עסקית.</li>
			</ul>
		</div>
		<div class="nladv-report">
			<p class="nladv-kicker">דיווח</p>
			<h2>הדוח שהמפרסם צריך לראות</h2>
			<p>מרכז הפרסום מציג כרטיסים, הזמנות, צפיות, פניות, השלמת פרופיל ותאריכי קמפיין. השלב הבא הוא PDF/אימייל חודשי עם מקורות תנועה, קליקים, לידים והמלצה אחת לפעולה.</p>
			<a class="nladv-btn dark" href="<?php echo esc_url( home_url( '/advertiser-center/' ) ); ?>">פתחו מרכז פרסום</a>
		</div>
	</section>

	<section class="nladv-section nladv-policy">
		<p class="nladv-kicker">כללים שמגינים על שני הצדדים</p>
		<h2>בלי קסמים מזויפים. כן מערכת שמוכרת, מודדת ומשפרת.</h2>
		<div class="nladv-policy-grid">
			<p><strong>אין הבטחת תנועה בשלב הזה.</strong> אנחנו מציגים תמונת מצב אמיתית ומוכרים נכס, מיקום ותקופה.</p>
			<p><strong>קמפיין מוגבל בזמן.</strong> תשלום חד-פעמי לא יוצר Pro קבוע; יש תאריך סיום ודירוג יורד חזרה.</p>
			<p><strong>תוכן ממומן מסומן.</strong> כל כתבה או חסות תסומן כתוכן שיווקי או ממומן.</p>
			<p><strong>תקלה במיקום מזכה בהארכה.</strong> אם לא סיפקנו את המיקום/התקופה בגלל באג, מאריכים בהתאם.</p>
		</div>
	</section>
</main>
<?php echo nadlan_adv_css(); ?>
		<?php
		return ob_get_clean();
	}
}

if ( ! function_exists( 'nadlan_adv_css' ) ) {
	function nadlan_adv_css() {
		return '<style>
.nladv{font-family:var(--font-sans,Heebo,Arial,sans-serif);color:#1B1A17;background:#fff;direction:rtl}
.nladv *{box-sizing:border-box}
.nladv-hero{min-height:520px;background-image:linear-gradient(90deg,rgba(7,34,39,.9),rgba(7,34,39,.66),rgba(7,34,39,.22)),var(--nladv-hero);background-size:cover;background-position:center;display:flex;align-items:center}
.nladv-hero-inner{width:min(1180px,calc(100% - 40px));margin:0 auto;color:#fff;padding:56px 0}
.nladv-kicker{margin:0 0 10px;color:#B89254;font-size:12px;font-weight:800;letter-spacing:.08em;text-transform:uppercase}
.nladv-hero h1{font-family:var(--font-serif,"Frank Ruhl Libre",serif);font-size:clamp(38px,5vw,68px);line-height:1.04;max-width:850px;margin:0 0 18px;font-weight:700;letter-spacing:0}
.nladv-lede{font-size:18px;line-height:1.75;max-width:760px;margin:0 0 26px;color:#F5F0E7}
.nladv-actions{display:flex;gap:12px;flex-wrap:wrap}
.nladv-btn,.nladv-card-btn{display:inline-flex;align-items:center;justify-content:center;min-height:44px;border-radius:6px;padding:12px 20px;text-decoration:none;font-weight:800;border:1px solid transparent}
.nladv-btn.gold,.nladv-card-btn{background:#B89254;color:#101817}
.nladv-btn.dark{background:#102323;color:#fff}
.nladv-btn.ghost{background:rgba(255,255,255,.08);border-color:rgba(255,255,255,.5);color:#fff}
.nladv-band{width:min(1180px,calc(100% - 32px));margin:24px auto;display:grid;gap:12px}
.nladv-snapshot{grid-template-columns:repeat(5,1fr)}
.nladv-snapshot div,.nladv-flow div{border:1px solid #E4DDD1;border-radius:8px;padding:18px;background:#FBFAF7}
.nladv-snapshot strong{display:block;font-size:28px;color:#123B3B}
.nladv-snapshot span,.nladv-flow span,.nladv-muted{color:#5F6764;font-size:14px;line-height:1.6}
.nladv-section{width:min(1180px,calc(100% - 32px));margin:64px auto}
.nladv-head{max-width:760px;margin:0 auto 26px;text-align:center}
.nladv-head h2,.nladv-grid2 h2,.nladv-policy h2{font-family:var(--font-serif,"Frank Ruhl Libre",serif);font-size:34px;line-height:1.18;margin:0 0 10px;color:#102323;letter-spacing:0}
.nladv-head p{margin:0;color:#5F6764;line-height:1.7}
.nladv-packages{display:grid;grid-template-columns:repeat(4,1fr);gap:14px}
.nladv-package{border:1px solid #E4DDD1;border-radius:8px;background:#fff;padding:22px;display:flex;flex-direction:column;min-height:390px;box-shadow:0 8px 24px rgba(16,35,35,.06)}
.nladv-package h3{font-size:22px;line-height:1.25;margin:10px 0;color:#102323}
.nladv-pill{display:inline-flex;align-items:center;background:#EEF5F3;color:#123B3B;border-radius:999px;padding:5px 10px;font-size:12px;font-weight:800}
.nladv-price{font-size:31px;font-weight:900;color:#B89254;margin:4px 0 12px}
.nladv-price small{font-size:13px;color:#5F6764}
.nladv-package ul,.nladv-checks{padding:0 18px 0 0;margin:14px 0 22px;color:#243331;line-height:1.65}
.nladv-package li,.nladv-checks li{margin:0 0 8px}
.nladv-card-btn{margin-top:auto}
.nladv-flow{grid-template-columns:repeat(5,1fr);align-items:stretch}
.nladv-flow b{display:inline-flex;width:30px;height:30px;align-items:center;justify-content:center;border-radius:999px;background:#123B3B;color:#fff;margin-left:8px}
.nladv-grid2{display:grid;grid-template-columns:1.1fr .9fr;gap:28px;align-items:start}
.nladv-report{border:1px solid #D6E2DF;border-radius:8px;background:#F3F8F7;padding:28px}
.nladv-report p{line-height:1.75;color:#3B4845}
.nladv-policy{border-top:1px solid #E4DDD1;padding-top:38px}
.nladv-policy-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:14px}
.nladv-policy-grid p{border:1px solid #E4DDD1;border-radius:8px;padding:18px;margin:0;line-height:1.65;background:#fff}
.nladv-policy-grid strong{display:block;color:#102323;margin-bottom:6px}
@media(max-width:960px){.nladv-snapshot,.nladv-packages,.nladv-flow,.nladv-policy-grid{grid-template-columns:repeat(2,1fr)}.nladv-grid2{grid-template-columns:1fr}.nladv-hero{min-height:480px}}
@media(max-width:600px){.nladv-hero{min-height:560px}.nladv-snapshot,.nladv-packages,.nladv-flow,.nladv-policy-grid{grid-template-columns:1fr}.nladv-section{margin:44px auto}.nladv-hero-inner{width:min(100% - 28px,1180px)}}
</style>';
	}
}

add_filter( 'pre_get_document_title', function ( $title ) {
	if ( nadlan_adv_is_page() ) {
		return 'פרסום פרויקטים ובעלי מקצוע בנדל"ן חכם';
	}
	return $title;
}, 24 );

add_filter( 'wpseo_metadesc', function ( $desc ) {
	if ( nadlan_adv_is_page() ) {
		return 'מסלולי פרסום בנדל"ן חכם: כרטיסי Pro/Premier, קמפיין פרויקט, נכס מקודם, תשלום, עריכה, מדידה ודיווח במקום אחד.';
	}
	return $desc;
}, 24 );

add_action( 'wp_head', function () {
	if ( ! nadlan_adv_is_page() ) { return; }
	$offers = array();
	foreach ( nadlan_adv_packages() as $pkg ) {
		$offers[] = array(
			'@type' => 'Offer',
			'name' => $pkg['name'],
			'url' => $pkg['href'],
			'priceCurrency' => 'ILS',
			'price' => preg_replace( '/[^\d.]/', '', $pkg['price'] ),
			'availability' => 'https://schema.org/InStock',
		);
	}
	$ld = array(
		'@context' => 'https://schema.org',
		'@type' => 'Service',
		'name' => 'פרסום נדל"ן חכם',
		'provider' => array( '@type' => 'Organization', 'name' => 'נדל"ן חכם', 'url' => home_url( '/' ) ),
		'serviceType' => 'Real estate advertising',
		'offers' => $offers,
	);
	echo "\n<script type=\"application/ld+json\">" . wp_json_encode( $ld, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES ) . "</script>\n";
}, 26 );

add_filter( 'nadlan_config_healthcheck', function ( $out ) {
	$out['advertise_page'] = array(
		'route' => home_url( '/advertise/' ),
		'shortcode' => '[nadlan_advertise]',
		'products' => array( 476, 477, 489, 490 ),
		'honest_metrics' => true,
	);
	return $out;
} );
