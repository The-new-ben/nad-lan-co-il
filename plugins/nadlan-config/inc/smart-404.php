<?php
/**
 * nadlan-config - Smart 404 (owner-approved, SEO session 2026-08-18).
 *
 * WHY: ~905 dead URLs are still known to Google - mostly the 2026-08-11
 * ghost-page cleanup (rewrite ghosts under /city/<city>/<kind>/ that were fed
 * to Google by a private sitemap and then deleted, per the owner's no-ghosts
 * law) plus old slugs. Owner law: NO redirects, ever. So the 404 itself
 * becomes useful: read the broken URL, recognize a city hinted in it, and
 * offer the live pages + search. The response stays a TRUE 404 (honest to
 * crawlers); only the body helps the human onward.
 */

if ( ! defined( 'ABSPATH' ) ) { exit; }

if ( ! function_exists( 'nadlan_smart404_city_map' ) ) {
	/** City display name => live dash-canonical projects page path (all 200-verified 2026-08-18). */
	function nadlan_smart404_city_map() {
		return array(
			'תל אביב'    => 'תל-אביב-יפו',
			'תל-אביב'    => 'תל-אביב-יפו',
			'רמת גן'     => 'רמת-גן',
			'רמת-גן'     => 'רמת-גן',
			'ראשון לציון' => 'ראשון-לציון',
			'ראשון-לציון' => 'ראשון-לציון',
			'חיפה'       => 'חיפה',
			'נתניה'      => 'נתניה',
			'הרצליה'     => 'הרצליה',
			'כפר סבא'    => 'כפר-סבא',
			'כפר-סבא'    => 'כפר-סבא',
			'קרית אונו'  => 'קרית-אונו',
			'קרית-אונו'  => 'קרית-אונו',
			'בת ים'      => 'בת-ים',
			'בת-ים'      => 'בת-ים',
			'באר שבע'    => 'באר-שבע',
			'באר-שבע'    => 'באר-שבע',
			'אשקלון'     => 'אשקלון',
			'פתח תקוה'   => 'פתח-תקוה',
			'פתח-תקוה'   => 'פתח-תקוה',
			'פתח תקווה'  => 'פתח-תקוה',
		);
	}
}

add_action( 'template_redirect', function () {
	if ( is_admin() || ! is_404() ) { return; }

	$req  = isset( $_SERVER['REQUEST_URI'] ) ? (string) $_SERVER['REQUEST_URI'] : '';
	$path = urldecode( (string) parse_url( $req, PHP_URL_PATH ) );

	$city_label = '';
	$city_slug  = '';
	foreach ( nadlan_smart404_city_map() as $needle => $slug ) {
		if ( false !== mb_strpos( $path, $needle ) ) {
			$city_label = str_replace( '-', ' ', $needle );
			$city_slug  = $slug;
			break;
		}
	}

	/* status is already 404 (set by WP) - we only replace the body. */
	if ( function_exists( 'nadlan_dir_header_single_h1' ) ) {
		nadlan_dir_header_single_h1();
	} else {
		get_header();
	}
	if ( function_exists( 'block_template_part' ) ) { block_template_part( 'header' ); }
	?>
<div class="nlsf" dir="rtl">
<style>
.nlsf{max-width:760px;margin:0 auto;padding:48px 18px 70px;font-family:Heebo,system-ui,sans-serif;color:#1B1A17}
.nlsf h1{font-size:30px;margin:0 0 8px}
.nlsf .nlsf-sub{color:#6b6354;font-size:16.5px;margin:0 0 22px;line-height:1.6}
.nlsf .nlsf-city{background:#FAF7F1;border:1px solid #E2DCD0;border-radius:14px;padding:16px 18px;margin:0 0 16px;font-size:17px}
.nlsf .nlsf-city a{color:#9C7A3C;font-weight:800}
.nlsf form{display:flex;gap:8px;margin:0 0 24px}
.nlsf input[type=search]{flex:1;padding:12px;border:1px solid #E2DCD0;border-radius:10px;font-size:16px;background:#fff}
.nlsf button{background:#C2563A;color:#fff;font-weight:800;border:0;border-radius:10px;padding:12px 24px;font-size:16px;cursor:pointer}
.nlsf .nlsf-links{display:grid;grid-template-columns:repeat(auto-fit,minmax(210px,1fr));gap:12px}
.nlsf .nlsf-links a{display:block;background:#FAF7F1;border:1px solid #E2DCD0;border-radius:12px;padding:14px;text-decoration:none;color:#1B1A17;font-weight:700;font-size:15.5px}
.nlsf .nlsf-links a span{display:block;color:#6b6354;font-weight:400;font-size:13px;margin-top:4px}
.nlsf .nlsf-links a:hover{border-color:#9C7A3C}
</style>
	<h1>העמוד הזה כבר לא כאן</h1>
	<p class="nlsf-sub">אבל מה שחיפשתם כנראה כן. הקטלוג סודר מחדש - הנה הדרכים המהירות להגיע למקום הנכון.</p>
	<?php if ( $city_slug ) : ?>
	<div class="nlsf-city">חיפשתם משהו ב<strong><?php echo esc_html( $city_label ); ?></strong>?
		<a href="<?php echo esc_url( home_url( '/city/' . $city_slug . '/projects/' ) ); ?>">כל הפרויקטים ב<?php echo esc_html( $city_label ); ?> ←</a>
	</div>
	<?php endif; ?>
	<form role="search" method="get" action="<?php echo esc_url( home_url( '/' ) ); ?>">
		<input type="search" name="s" placeholder="חפשו פרויקט, עיר או נושא" aria-label="חיפוש">
		<button type="submit">חיפוש</button>
	</form>
	<div class="nlsf-links">
		<a href="<?php echo esc_url( home_url( '/projects/' ) ); ?>">כל הפרויקטים החדשים<span>976 פרויקטים לפי עיר, יזם וסטטוס</span></a>
		<a href="<?php echo esc_url( home_url( '/sde-dov/' ) ); ?>">רובע שדה דב<span>המדריך המלא + כל הפרויקטים</span></a>
		<a href="<?php echo esc_url( home_url( '/property-value-estimator/' ) ); ?>">מחשבון שווי דירה<span>הערכת מחיר לפני קנייה או מכירה</span></a>
		<a href="<?php echo esc_url( home_url( '/mortgage-calculator/' ) ); ?>">מחשבון משכנתא<span>החזר חודשי, ריבית ותמהיל</span></a>
	</div>
</div>
	<?php
	if ( function_exists( 'block_template_part' ) ) { block_template_part( 'footer' ); }
	get_footer();
	exit;
}, 6 );
