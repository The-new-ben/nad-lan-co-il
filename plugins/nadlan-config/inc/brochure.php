<?php
/**
 * nadlan-config - THE PER-APARTMENT BROCHURE (world-competitor gap #2,
 * owner-approved sequence 2026-07-07).
 *
 * A buyer picks apartment N in the 3D building and gets a branded, print-ready
 * one-pager of THAT apartment: floor, direction, size, price estimate with the
 * mortgage line, project facts, honest disclaimers, and a deep link straight
 * back to the same unit selected in the 3D model. Browsers print it to PDF -
 * zero server dependencies, works on shared hosting.
 *
 * GET /nadlan/v1/brochure?p=<project_id>&u=<unit_id>[&lang=he|en]
 *
 * MONETIZATION: meta `project_brochure_logo` (URL) puts the developer's logo
 * on the sheet - a paid placement; absent, the brand mark carries it.
 * Every render increments `nadlan_brochure_views` on the project - fuel for
 * the developer analytics story.
 */

if ( ! defined( 'ABSPATH' ) ) { exit; }

add_action( 'rest_api_init', function () {
	register_rest_route( 'nadlan/v1', '/brochure', array(
		'methods' => 'GET', 'permission_callback' => '__return_true',
		'callback' => 'nadlan_brochure_render',
	) );
} );

if ( ! function_exists( 'nadlan_brochure_render' ) ) {
	function nadlan_brochure_render( WP_REST_Request $req ) {
		$pid  = (int) $req->get_param( 'p' );
		$uid  = sanitize_text_field( (string) $req->get_param( 'u' ) );
		$lang = in_array( $req->get_param( 'lang' ), array( 'he', 'en' ), true ) ? $req->get_param( 'lang' ) : 'he';
		$post = get_post( $pid );
		if ( ! $post || 'nadlan_project' !== $post->post_type || 'publish' !== $post->post_status ) {
			return new WP_Error( 'not_found', 'project not found', array( 'status' => 404 ) );
		}
		$units = function_exists( 'nadlan_showroom_engine_json_meta' ) ? nadlan_showroom_engine_json_meta( $pid, 'project_3d_units' ) : array();
		$unit  = null;
		foreach ( (array) $units as $u ) {
			if ( isset( $u['id'] ) && (string) $u['id'] === $uid ) { $unit = $u; break; }
		}
		if ( ! $unit ) {
			return new WP_Error( 'not_found', 'unit not found', array( 'status' => 404 ) );
		}
		update_post_meta( $pid, 'nadlan_brochure_views', (int) get_post_meta( $pid, 'nadlan_brochure_views', true ) + 1 );

		$he = 'he' === $lang;
		$T = $he ? array(
			'kind' => 'עמוד דירה', 'project' => 'הפרויקט', 'apt' => 'דירה', 'floor' => 'קומה',
			'rooms' => 'חדרים', 'sqm' => 'שטח', 'balcony' => 'מרפסת', 'dir' => 'כיוון אוויר',
			'view' => 'נוף', 'status' => 'סטטוס', 'est' => 'אומדן מחיר', 'on_request' => 'אומדן לפי פנייה',
			'mortgage' => 'החזר חודשי משוער', 'mortgage_note' => 'לפי מימון 70%, 25 שנה, ריבית 5% - אומדן בלבד, אינו הצעת מימון.',
			'back' => 'לצפייה בדירה בתלת ממד באתר:', 'print' => 'הדפסה / שמירה כ-PDF',
			'disc' => 'המסמך להתרשמות בלבד ואינו מהווה הצעה, מצג או התחייבות. הנתונים באחריות היזם וכפופים לתוכניות המכר המאושרות. הדמיות להמחשה.',
			'status_available' => 'זמינה', 'status_reserved' => 'בעדיפות', 'status_sold' => 'נמכרה',
			'generated' => 'הופק מתוך nad-lan.co.il',
		) : array(
			'kind' => 'Apartment one-pager', 'project' => 'Project', 'apt' => 'Apartment', 'floor' => 'Floor',
			'rooms' => 'Rooms', 'sqm' => 'Area', 'balcony' => 'Balcony', 'dir' => 'Orientation',
			'view' => 'View', 'status' => 'Status', 'est' => 'Price estimate', 'on_request' => 'Estimate on request',
			'mortgage' => 'Estimated monthly payment', 'mortgage_note' => '70% financing, 25 years, 5% interest - an estimate only, not a financing offer.',
			'back' => 'View this apartment in 3D:', 'print' => 'Print / Save as PDF',
			'disc' => 'For impression only; not an offer, representation or commitment. Data is the developer\'s responsibility and subject to approved sale plans. Renderings are illustrative.',
			'status_available' => 'Available', 'status_reserved' => 'On hold', 'status_sold' => 'Sold',
			'generated' => 'Generated from nad-lan.co.il',
		);

		$g      = function ( $k ) use ( $unit ) { return isset( $unit[ $k ] ) ? $unit[ $k ] : ''; };
		$price  = (float) $g( 'price' );
		$mort   = '';
		if ( $price > 1000 ) {
			$r = 0.05 / 12; $n = 300; $L = $price * 0.7;
			$mort = number_format( round( $L * $r / ( 1 - pow( 1 + $r, -$n ) ) ) );
		}
		$poster = esc_url( (string) get_post_meta( $pid, 'project_model_poster', true ) ?: (string) get_post_meta( $pid, 'project_3d_image', true ) );
		$logo   = esc_url( (string) get_post_meta( $pid, 'project_brochure_logo', true ) );
		$city   = (string) get_post_meta( $pid, 'city', true );
		$deep   = esc_url( add_query_arg( array( 'unit' => $uid, 'lang' => $lang ), get_permalink( $pid ) ) );
		$status = $T[ 'status_' . ( in_array( $g( 'status' ), array( 'available', 'reserved', 'sold' ), true ) ? $g( 'status' ) : 'available' ) ];
		$dirmap = array( 'west' => $he ? 'מערב' : 'West', 'east' => $he ? 'מזרח' : 'East', 'north' => $he ? 'צפון' : 'North', 'south' => $he ? 'דרום' : 'South',
			'south-west' => $he ? 'דרום-מערב' : 'South-West', 'north-west' => $he ? 'צפון-מערב' : 'North-West', 'south-east' => $he ? 'דרום-מזרח' : 'South-East', 'north-east' => $he ? 'צפון-מזרח' : 'North-East' );
		$dir = isset( $dirmap[ $g( 'dir' ) ] ) ? $dirmap[ $g( 'dir' ) ] : (string) $g( 'dir' );

		$rows = array();
		if ( $g( 'floor' ) !== '' ) { $rows[] = array( $T['floor'], (string) $g( 'floor' ) ); }
		if ( $g( 'rooms' ) !== '' ) { $rows[] = array( $T['rooms'], (string) $g( 'rooms' ) ); }
		if ( $g( 'sqm' ) ) { $rows[] = array( $T['sqm'], $g( 'sqm' ) . ' ' . ( $he ? 'מ"ר' : 'sqm' ) ); }
		if ( $g( 'balcony' ) ) { $rows[] = array( $T['balcony'], $g( 'balcony' ) . ' ' . ( $he ? 'מ"ר' : 'sqm' ) ); }
		if ( $dir ) { $rows[] = array( $T['dir'], $dir ); }
		if ( $g( 'view' ) ) { $rows[] = array( $T['view'], (string) $g( 'view' ) ); }
		$rows[] = array( $T['status'], $status );

		$dirattr = $he ? 'rtl' : 'ltr';
		ob_start();
		?>
<!doctype html><html lang="<?php echo esc_attr( $lang ); ?>" dir="<?php echo esc_attr( $dirattr ); ?>"><head>
<meta charset="utf-8"><meta name="robots" content="noindex,nofollow"><meta name="viewport" content="width=device-width,initial-scale=1">
<title><?php echo esc_html( $T['apt'] . ' ' . $g( 'label' ) . ' · ' . get_the_title( $pid ) ); ?></title>
<link href="https://fonts.googleapis.com/css2?family=Frank+Ruhl+Libre:wght@700;900&family=Heebo:wght@400;600;700&display=swap" rel="stylesheet">
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:Heebo,sans-serif;background:#E9E4D8;color:#1B1A17}
.sheet{max-width:800px;margin:18px auto;background:#FAF7F1;border:1px solid #D6C189;box-shadow:0 20px 50px -25px rgba(27,26,23,.4)}
.band{height:10px;background:#9C7A3C}
.head{display:flex;justify-content:space-between;align-items:center;padding:26px 34px 8px}
.head .kind{font:700 11px/1 Heebo;letter-spacing:.16em;color:#9C7A3C;text-transform:uppercase}
.head h1{font-family:"Frank Ruhl Libre",serif;font-weight:900;font-size:2rem;margin-top:6px}
.head .city{color:#6D665C;font-size:14px;margin-top:2px}
.logo{max-height:56px;max-width:150px;object-fit:contain}
.brand-mark{width:46px;height:46px}
.hero{margin:16px 34px;border-radius:12px;overflow:hidden;background:#14130F;aspect-ratio:16/8}
.hero img{width:100%;height:100%;object-fit:contain;display:block}
.aptline{display:flex;align-items:baseline;gap:12px;padding:6px 34px 0}
.aptline b{font-family:"Frank Ruhl Libre",serif;font-size:1.5rem}
.aptline .price{margin-inline-start:auto;font:800 1.5rem/1 Heebo;color:#9C7A3C}
.grid{display:grid;grid-template-columns:repeat(3,1fr);gap:1px;background:#E2DCD0;border:1px solid #E2DCD0;border-radius:12px;overflow:hidden;margin:16px 34px}
.cell{background:#fff;padding:13px 15px}
.cell .k{font:600 11px/1 Heebo;color:#6D665C;letter-spacing:.06em}
.cell .v{font:700 16px/1.3 Heebo;margin-top:4px}
.mort{margin:0 34px;background:#F3EEE3;border:1px solid #E2DCD0;border-radius:12px;padding:14px 18px}
.mort b{font-size:17px}
.mort span{display:block;font-size:11.5px;color:#6D665C;margin-top:3px}
.back{margin:16px 34px;padding:14px 18px;border:1.5px dashed #9C7A3C;border-radius:12px;font-size:13.5px}
.back a{color:#9C7A3C;font-weight:700;word-break:break-all}
.disc{margin:14px 34px;color:#8A8378;font-size:10.5px;line-height:1.5}
.foot{display:flex;justify-content:space-between;align-items:center;padding:12px 34px 22px;color:#6D665C;font-size:12px}
.printbtn{position:fixed;bottom:22px;inset-inline-end:22px;background:#1B1A17;color:#FAF7F1;font:700 14px/1 Heebo;border:0;border-radius:12px;padding:15px 22px;cursor:pointer;box-shadow:0 14px 30px -12px rgba(0,0,0,.5)}
.printbtn:hover{background:#9C7A3C}
@media print{body{background:#fff}.sheet{margin:0;border:0;box-shadow:none;max-width:none}.printbtn{display:none}@page{margin:8mm}}
</style></head><body>
<div class="sheet">
	<div class="band"></div>
	<div class="head">
		<div>
			<div class="kind"><?php echo esc_html( $T['kind'] ); ?></div>
			<h1><?php echo esc_html( get_the_title( $pid ) ); ?></h1>
			<div class="city"><?php echo esc_html( $city ); ?></div>
		</div>
		<?php if ( $logo ) : ?><img class="logo" src="<?php echo $logo; ?>" alt=""><?php else : ?>
		<svg class="brand-mark" viewBox="0 0 64 64"><rect width="64" height="64" rx="14" fill="#14130F"/><rect x="14" y="27" width="10" height="23" fill="#9C7A3C" opacity=".55"/><rect x="27" y="13" width="10" height="37" fill="#9C7A3C"/><rect x="40" y="33" width="10" height="17" fill="#9C7A3C" opacity=".75"/><rect x="12" y="50" width="40" height="2.4" fill="#E9D9A8"/></svg>
		<?php endif; ?>
	</div>
	<?php if ( $poster ) : ?><div class="hero"><img src="<?php echo $poster; ?>" alt=""></div><?php endif; ?>
	<div class="aptline"><b><?php echo esc_html( $T['apt'] . ' ' . $g( 'label' ) ); ?></b>
		<span class="price"><?php echo $price > 1000 ? '₪' . esc_html( number_format( $price ) ) : esc_html( $T['on_request'] ); ?></span></div>
	<div class="grid"><?php foreach ( $rows as $r ) : ?><div class="cell"><div class="k"><?php echo esc_html( $r[0] ); ?></div><div class="v"><?php echo esc_html( $r[1] ); ?></div></div><?php endforeach; ?></div>
	<?php if ( $mort ) : ?><div class="mort"><b><?php echo esc_html( $T['mortgage'] ); ?>: ₪<?php echo esc_html( $mort ); ?></b><span><?php echo esc_html( $T['mortgage_note'] ); ?></span></div><?php endif; ?>
	<div class="back"><?php echo esc_html( $T['back'] ); ?> <a href="<?php echo $deep; ?>"><?php echo $deep; ?></a></div>
	<p class="disc"><?php echo esc_html( $T['disc'] ); ?></p>
	<div class="foot"><span><?php echo esc_html( $T['generated'] ); ?></span><span><?php echo esc_html( wp_date( 'd/m/Y' ) ); ?></span></div>
</div>
<button type="button" class="printbtn" onclick="window.print()"><?php echo esc_html( $T['print'] ); ?></button>
</body></html>
		<?php
		$html = ob_get_clean();
		header( 'Content-Type: text/html; charset=utf-8' );
		echo $html; // phpcs:ignore WordPress.Security.EscapeOutput
		exit;
	}
}
