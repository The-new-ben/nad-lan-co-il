<?php
/**
 * Developer-facing landing page and the direct film link.
 *
 * This is the surface a developer sees when we approach them, and it is
 * deliberately separated from /advertise/: that page carries a small sponsored
 * listing product, and a low price sitting next to an enterprise conversation
 * cheapens it. Nothing here quotes a price at all - pricing belongs in a
 * conversation, not on a page a competitor can read.
 *
 * Two routes:
 *   /developers/  the landing page, rendered through the theme
 *   /film/        the film on its own, for a link that cannot be missed
 *
 * @package nadlan-config
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

if ( ! function_exists( 'nadlan_dev_film_url' ) ) {
	/**
	 * Which cut is on air.
	 *
	 * Held in an option rather than hardcoded because the film gets re-rendered:
	 * the first 118s cut shipped at 600x338, which is a resolution the source
	 * never rendered rather than a compression artefact, so no re-encode could
	 * rescue it. Swapping masters must not need a deploy.
	 */
	function nadlan_dev_film_url() {
		$set = trim( (string) get_option( 'nadlan_film_url', '' ) );
		if ( '' !== $set ) {
			return $set;
		}
		$u = wp_get_upload_dir();
		return trailingslashit( $u['baseurl'] ) . '2026/08/nadlan-developer-film.mp4';
	}
}

if ( ! function_exists( 'nadlan_dev_page_css' ) ) {
	function nadlan_dev_page_css() {
		return '.nldev{max-width:1120px;margin:0 auto;padding:0 clamp(14px,3vw,26px);direction:rtl;font-family:Heebo,system-ui,sans-serif;color:#1B1A17}'
			. '.nldev-hero{text-align:center;padding:26px 0 8px}'
			. '.nldev-kicker{color:#8A6A2F;font:800 12.5px/1 Heebo,sans-serif;letter-spacing:.06em;margin:0 0 10px}'
			. '.nldev h1{font-family:"Frank Ruhl Libre",serif;font-size:clamp(1.7rem,1.2rem+2vw,2.6rem);line-height:1.2;margin:0 0 12px;color:#1B1A17!important}'
			. '.nldev-lede{font:400 16px/1.7 Heebo,sans-serif;color:#4A4335;max-width:760px;margin:0 auto 22px}'
			. '.nldev-film{position:relative;border-radius:18px;overflow:hidden;border:1px solid #D6C189;background:#14130F;margin:0 0 10px}'
			. '.nldev-film video{width:100%;height:auto;display:block}'
			. '.nldev-note{font:600 12.5px Heebo,sans-serif;color:#8E877A;text-align:center;margin:0 0 30px}'
			. '.nldev-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:16px;margin:0 0 30px}'
			. '.nldev-card{background:#FBF7EC;border:1px solid #E2DCD0;border-radius:14px;padding:18px 20px}'
			. '.nldev-card h3{font:800 15px/1.4 Heebo,sans-serif;margin:0 0 8px;color:#1B1A17!important}'
			. '.nldev-card p{font:400 14px/1.7 Heebo,sans-serif;color:#4A4335;margin:0}'
			. '.nldev-tours{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:14px;margin:0 0 30px}'
			. '.nldev-tour{display:block;background:linear-gradient(160deg,#211F19,#14130F);border-radius:14px;padding:20px 22px;text-decoration:none;border:1px solid #3A342A}'
			. '.nldev-tour b{display:block;color:#F4EEDE;font:800 16px Heebo,sans-serif;margin:0 0 6px}'
			. '.nldev-tour span{display:block;color:#C9C2B4;font:400 13.5px/1.6 Heebo,sans-serif}'
			. '.nldev-tour:hover{border-color:#C9A45C}'
			. '.nldev-honest{background:#F3EEE3;border:1px solid #E2DCD0;border-inline-start:4px solid #B85410;border-radius:12px;padding:16px 20px;margin:0 0 30px}'
			. '.nldev-honest p{font:400 14px/1.75 Heebo,sans-serif;color:#4A4335;margin:0 0 8px}'
			. '.nldev-honest p:last-child{margin:0}'
			. '.nldev-cta{text-align:center;padding:8px 0 40px}'
			. '.nldev-cta a{display:inline-block;background:#B85410;color:#fff;font:800 17px/1 Heebo,sans-serif;border-radius:10px;padding:15px 32px;text-decoration:none}'
			. '.nldev-cta a:hover{background:#9C4409;color:#fff}'
			. '.nldev-cta p{font:400 13.5px Heebo,sans-serif;color:#6B6353;margin:12px 0 0}'
			. '@media(max-width:700px){.nldev h1{font-size:1.55rem}}';
	}
}

if ( ! function_exists( 'nadlan_dev_page_render' ) ) {
	function nadlan_dev_page_render() {
		$film   = esc_url( nadlan_dev_film_url() );
		$somail = esc_url( home_url( '/tour/somail/' ) );
		$sdedov = esc_url( home_url( '/tour/sde-dov/' ) );

		ob_start(); ?>
<div class="nldev">
	<div class="nldev-hero">
		<p class="nldev-kicker">ליזמים ולחברות בנייה</p>
		<h1>שכבת שיווק דיגיטלית לפרויקטים שלכם</h1>
		<p class="nldev-lede">nad-lan.co.il ממפה את פרויקטי הנדל&quot;ן בישראל ומציג אותם בסביבה תלת ממדית, שבה המתעניין בוחר בניין, קומה וכיוון, מבין את הסביבה, ומגיע לצוות המכירות שלכם כשהוא כבר יודע מה מעניין אותו.</p>
	</div>

	<div class="nldev-film">
		<video controls preload="metadata" playsinline src="<?php echo $film; ?>"></video>
	</div>
	<p class="nldev-note">שתי דקות שמסבירות את הרעיון</p>

	<div class="nldev-grid">
		<div class="nldev-card">
			<h3>סטודיו לניהול הפרויקט</h3>
			<p>חברה שמצטרפת מקבלת אזור אישי שבו אפשר לעדכן נתונים, להוסיף חומרים רשמיים, לעדכן סטטוס יחידות ולתקשר ישירות עם המתעניינים.</p>
		</div>
		<div class="nldev-card">
			<h3>הפניות מגיעות אליכם בלבד</h3>
			<p>אנחנו לא מתווכים ואין לנו עניין בניהול הפניות. פנייה שמגיעה דרך עמוד הפרויקט עוברת אליכם, ואינה נמסרת לאף גורם אחר.</p>
		</div>
		<div class="nldev-card">
			<h3>חמש שפות</h3>
			<p>עברית, אנגלית, צרפתית, רוסית וערבית. התוכן נכתב בכל שפה בנפרד ולא מתורגם מילולית, כדי להגיע גם לקונים ומשקיעים מחוץ לישראל.</p>
		</div>
		<div class="nldev-card">
			<h3>כל הפרויקטים בחוויה אחת</h3>
			<p>אפשר לחבר את כל הפרויקטים של חברה לסיור אחד, כך שרוכש נע ביניהם באותה סביבה במקום לחפש כל פרויקט בנפרד.</p>
		</div>
	</div>

	<div class="nldev-tours">
		<a class="nldev-tour" href="<?php echo $somail; ?>">
			<b>מתחם סומייל</b>
			<span>סיור תלת ממדי במתחם, כולל הסביבה והרחובות</span>
		</a>
		<a class="nldev-tour" href="<?php echo $sdedov; ?>">
			<b>רובע שדה דב</b>
			<span>סיור עם מעבר בין המצב הקיים לתכנון העתידי</span>
		</a>
	</div>

	<div class="nldev-honest">
		<p>האתר נמצא בהקמה. כל המידע המוצג כרגע נאסף ממקורות גלויים ברשת ומקושר למקורותיו, ונתונים שאינם רשמיים מסומנים כהמחשה או כאומדן.</p>
		<p>אנחנו לא אתר רשמי של אף יזם ואיננו פועלים מטעמו. חברה שמבקשת לתקן פרט או להסיר פרויקט מהמערכת, נעשה זאת מיד וללא כל תנאי.</p>
	</div>

	<div class="nldev-cta">
		<a href="mailto:info@nad-lan.co.il?subject=פנייה%20מעמוד%20היזמים">דברו איתנו</a>
		<p>info@nad-lan.co.il</p>
	</div>
</div>
		<?php
		return ob_get_clean();
	}
}

add_shortcode( 'nadlan_developers', function () {
	wp_register_style( 'nadlan-developers', false, array(), NADLAN_CONFIG_VERSION );
	wp_enqueue_style( 'nadlan-developers' );
	wp_add_inline_style( 'nadlan-developers', nadlan_dev_page_css() );
	return nadlan_dev_page_render();
} );

/* /film/ - the film on its own, so a single link cannot be missed or mistaken
   for a download. Served standalone rather than through the theme: nothing
   competes with it on the page. */
add_action( 'init', function () {
	add_rewrite_rule( '^film/?$', 'index.php?nadlan_film=1', 'top' );
	if ( get_option( 'nadlan_film_route_flushed' ) !== NADLAN_CONFIG_VERSION ) {
		flush_rewrite_rules( false );
		update_option( 'nadlan_film_route_flushed', NADLAN_CONFIG_VERSION );
	}
} );

add_filter( 'query_vars', function ( $vars ) {
	$vars[] = 'nadlan_film';
	return $vars;
} );

add_action( 'template_redirect', function () {
	if ( ! get_query_var( 'nadlan_film' ) ) {
		return;
	}
	$film = esc_url( nadlan_dev_film_url() );
	$dev  = esc_url( home_url( '/developers/' ) );
	header( 'Content-Type: text/html; charset=utf-8' );
	?><!DOCTYPE html>
<html lang="he" dir="rtl"><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex,follow">
<title>nad-lan.co.il · סרטון היכרות ליזמים</title>
<style>
html,body{margin:0;padding:0;background:#14130F;color:#F4EEDE;font-family:Heebo,system-ui,sans-serif;min-height:100%}
.wrap{max-width:1000px;margin:0 auto;padding:28px 18px 40px;text-align:center}
h1{font-size:19px;font-weight:800;margin:0 0 18px;color:#F4EEDE}
video{width:100%;height:auto;display:block;border-radius:14px;border:1px solid #3A342A;background:#000}
a.more{display:inline-block;margin-top:22px;background:#B85410;color:#fff;font-weight:800;font-size:16px;border-radius:10px;padding:14px 30px;text-decoration:none}
a.more:hover{background:#9C4409}
p.sub{color:#9B948A;font-size:13px;margin:14px 0 0}
</style>
</head><body>
<div class="wrap">
<h1>nad-lan.co.il · שכבת שיווק דיגיטלית לפרויקטים</h1>
<video controls autoplay muted playsinline preload="metadata" src="<?php echo $film; ?>"></video>
<a class="more" href="<?php echo $dev; ?>">למידע נוסף ליזמים</a>
<p class="sub">info@nad-lan.co.il</p>
</div>
</body></html>
	<?php
	exit;
} );
