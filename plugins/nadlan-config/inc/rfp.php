<?php
/**
 * nadlan-config - RFP document (buy-flow phase 2, research spec 2026-07-05)
 *
 * The buy-flow posts a structured request; this module turns it into a real,
 * shareable, printable RFP document the buyer can open immediately and the
 * owner can forward to the developer and advisors.
 *
 *  - POST /nadlan/v1/rfp        create the document (called by buyflow.js right
 *                               after the lead is accepted); returns {url}
 *  - GET  /nadlan/v1/rfp/<token> the rendered document (unguessable token)
 *
 * HONESTY LAWS: unit facts are re-read SERVER-SIDE from the project post (the
 * client payload only points at project slug + unit id); every money-shaped
 * line is estimate-labeled; advisors listed are real directory entries matched
 * by profession; the status timeline claims only what actually happened.
 */

if ( ! defined( 'ABSPATH' ) ) { exit; }

if ( ! function_exists( 'nadlan_rfp_lang_table' ) ) {
	function nadlan_rfp_lang_table( $lang ) {
		$T = array(
			'he' => array( 'dir' => 'rtl', 'doc' => 'מסמך בקשה להצעה', 'for' => 'עבור', 'date' => 'תאריך', 'valid' => 'בתוקף 30 יום', 'unit' => 'הדירה המבוקשת', 'project' => 'פרויקט', 'developer' => 'יזם', 'floor' => 'קומה', 'rooms' => 'חדרים', 'sqm' => 'שטח (מ"ר)', 'dirn' => 'כיוון', 'config' => 'הבקשה', 'finish' => 'רמת גימור', 'finish_std' => 'מפרט היזם', 'finish_up' => 'משודרג', 'finish_prem' => 'פרימיום', 'extras' => 'שירותים שצורפו לבקשה', 'none' => 'ללא תוספות, חיבור ישיר ליזם', 'advisors' => 'אנשי מקצוע מוצעים מהמאגר', 'adv_none' => 'צוות נדלן יתאם יועץ מתאים מהמאגר', 'status' => 'סטטוס הבקשה', 'st1' => 'הבקשה התקבלה במערכת', 'st2' => 'תיאום מול היזם', 'st3' => 'הצעה מרוכזת לרוכש', 'disc' => 'כל הנתונים במסמך זה הם אומדן ולידיעה בלבד. המסמך אינו הצעת מחיר, אינו התחייבות ואינו מסמך מכר. התמחור הסופי נקבע בהצעת היזם לפי מפרט המכר וחוזה הרכישה.', 'ex_designer' => 'מעצב/ת פנים', 'ex_lawyer' => 'עו"ד מקרקעין', 'ex_mortgage' => 'יועץ משכנתא', 'ex_inspect' => 'בדק בית', 'ex_furniture' => 'התעניינות בריהוט', 'print' => 'הדפסה / שמירה כ-PDF', 'back' => 'חזרה לעמוד הפרויקט' ),
			'en' => array( 'dir' => 'ltr', 'doc' => 'Request for Proposal', 'for' => 'For', 'date' => 'Date', 'valid' => 'Valid 30 days', 'unit' => 'Requested apartment', 'project' => 'Project', 'developer' => 'Developer', 'floor' => 'Floor', 'rooms' => 'Rooms', 'sqm' => 'Area (sqm)', 'dirn' => 'Orientation', 'config' => 'The request', 'finish' => 'Finish level', 'finish_std' => 'Developer spec', 'finish_up' => 'Upgraded', 'finish_prem' => 'Premium', 'extras' => 'Services added to the request', 'none' => 'No add-ons, direct connection to the developer', 'advisors' => 'Suggested professionals from the directory', 'adv_none' => 'The NadLan team will match a suitable advisor', 'status' => 'Request status', 'st1' => 'Request received', 'st2' => 'Coordination with the developer', 'st3' => 'Consolidated proposal to the buyer', 'disc' => 'All figures in this document are estimates for information only. This document is not a quote, not a commitment and not a sale document. Final pricing is set in the developer proposal per the sale specification and purchase contract.', 'ex_designer' => 'Interior designer', 'ex_lawyer' => 'Real estate lawyer', 'ex_mortgage' => 'Mortgage advisor', 'ex_inspect' => 'Inspection (bedek)', 'ex_furniture' => 'Furniture interest', 'print' => 'Print / save as PDF', 'back' => 'Back to the project page' ),
		);
		if ( isset( $T[ $lang ] ) ) { return $T[ $lang ]; }
		return $T[ in_array( $lang, array( 'fr', 'ru' ), true ) ? 'en' : ( $lang === 'ar' ? 'he' : 'he' ) ];
	}
}

if ( ! function_exists( 'nadlan_rfp_advisor_map' ) ) {
	function nadlan_rfp_advisor_map() {
		return array(
			'designer' => array( 'interior_designer', 'architect' ),
			'lawyer'   => array( 'lawyer' ),
			'mortgage' => array( 'mashkanta' ),
			'inspect'  => array( 'bedek_bait', 'inspector' ),
		);
	}
}

if ( ! function_exists( 'nadlan_rfp_match_advisors' ) ) {
	function nadlan_rfp_match_advisors( $extras ) {
		$map = nadlan_rfp_advisor_map();
		$out = array();
		foreach ( (array) $extras as $x ) {
			$x = sanitize_key( $x );
			if ( ! isset( $map[ $x ] ) ) { continue; }
			$q = new WP_Query( array(
				'post_type' => 'nadlan_professional', 'post_status' => 'publish',
				'posts_per_page' => 2, 'no_found_rows' => true, 'fields' => 'ids',
				// honesty guard (#34 follow-up): profiles carrying seeded ratings
				// (rating meta without reviews_verified) are demo dressing for the
				// directory - they must never be named in a real buyer's document.
				'meta_query' => array( 'relation' => 'AND',
					array( 'key' => 'profession', 'value' => $map[ $x ], 'compare' => 'IN' ),
					array( 'relation' => 'OR',
						array( 'key' => 'rating', 'compare' => 'NOT EXISTS' ),
						array( 'key' => 'reviews_verified', 'value' => '1' ),
					),
				),
			) );
			$names = array();
			foreach ( $q->posts as $pid ) {
				$names[] = array(
					'name' => get_the_title( $pid ),
					'city' => (string) get_post_meta( $pid, 'city', true ),
					'url'  => get_permalink( $pid ),
				);
			}
			$out[ $x ] = $names;
		}
		return $out;
	}
}

if ( ! function_exists( 'nadlan_rfp_create' ) ) {
	function nadlan_rfp_create( WP_REST_Request $req ) {
		$p = $req->get_json_params();
		if ( ! is_array( $p ) ) { return new WP_Error( 'bad_request', 'invalid payload', array( 'status' => 400 ) ); }
		$slug    = sanitize_title( (string) ( $p['project'] ?? '' ) );
		$unit_id = sanitize_key( (string) ( $p['unit'] ?? '' ) );
		$lang    = in_array( ( $p['lang'] ?? 'he' ), array( 'he', 'en', 'fr', 'ru', 'ar' ), true ) ? $p['lang'] : 'he';
		$post    = $slug ? get_page_by_path( $slug, OBJECT, 'nadlan_project' ) : null;
		if ( ! $post ) { return new WP_Error( 'not_found', 'project not found', array( 'status' => 404 ) ); }
		// server-side unit facts - the client only points, never dictates
		$unit = null;
		$units = json_decode( (string) get_post_meta( $post->ID, 'project_3d_units', true ), true );
		foreach ( (array) $units as $u ) { if ( isset( $u['id'] ) && $u['id'] === $unit_id ) { $unit = $u; break; } }
		$finish = in_array( ( $p['finish'] ?? 'std' ), array( 'std', 'up', 'prem' ), true ) ? $p['finish'] : 'std';
		$extras = array_values( array_intersect( array_map( 'sanitize_key', (array) ( $p['extras'] ?? array() ) ), array_keys( nadlan_rfp_advisor_map() + array( 'furniture' => 1 ) ) ) );
		$first  = sanitize_text_field( (string) ( $p['name'] ?? '' ) );
		$token  = strtolower( wp_generate_password( 24, false, false ) );
		$doc = array(
			'token'     => $token,
			'created'   => gmdate( 'c' ),
			'lang'      => $lang,
			'project'   => array( 'id' => $post->ID, 'slug' => $slug, 'name' => get_the_title( $post->ID ), 'developer' => (string) get_post_meta( $post->ID, 'developer_name', true ), 'url' => get_permalink( $post->ID ) ),
			'unit'      => $unit ? array( 'id' => $unit['id'], 'label' => (string) ( $unit['label'] ?? '' ), 'floor' => (int) ( $unit['floor'] ?? 0 ), 'rooms' => (float) ( $unit['rooms'] ?? 0 ), 'sqm' => (float) ( $unit['sqm'] ?? 0 ), 'dir' => (string) ( $unit['dir'] ?? '' ) ) : null,
			'finish'    => $finish,
			'extras'    => $extras,
			'advisors'  => nadlan_rfp_match_advisors( $extras ),
			'buyer'     => array( 'first' => $first ),
			'lead_id'   => (int) ( $p['lead_id'] ?? 0 ),
			'status'    => 1,
		);
		$rid = wp_insert_post( array(
			'post_type' => 'nadlan_rfp', 'post_status' => 'private',
			'post_title' => 'RFP ' . $slug . ' ' . $unit_id . ' ' . gmdate( 'Y-m-d H:i' ),
			'post_content' => wp_slash( wp_json_encode( $doc, JSON_UNESCAPED_UNICODE ) ),
		), true );
		if ( is_wp_error( $rid ) ) { return $rid; }
		update_post_meta( $rid, 'rfp_token', $token );
		if ( $doc['lead_id'] ) { update_post_meta( $doc['lead_id'], 'rfp_id', $rid ); }
		return rest_ensure_response( array( 'ok' => true, 'url' => rest_url( 'nadlan/v1/rfp/' . $token ) ) );
	}
}

if ( ! function_exists( 'nadlan_rfp_render' ) ) {
	function nadlan_rfp_render( WP_REST_Request $req ) {
		$token = strtolower( preg_replace( '/[^a-z0-9]/i', '', (string) $req['token'] ) );
		$q = new WP_Query( array( 'post_type' => 'nadlan_rfp', 'post_status' => 'private', 'posts_per_page' => 1, 'no_found_rows' => true, 'fields' => 'ids', 'meta_key' => 'rfp_token', 'meta_value' => $token ) );
		if ( ! $q->posts ) { status_header( 404 ); echo 'Not found'; exit; }
		$doc = json_decode( get_post_field( 'post_content', $q->posts[0] ), true );
		if ( ! is_array( $doc ) ) { status_header( 410 ); echo 'Gone'; exit; }
		$T = nadlan_rfp_lang_table( $doc['lang'] );
		$u = $doc['unit']; $pr = $doc['project'];
		$exlbl = array( 'designer' => $T['ex_designer'], 'lawyer' => $T['ex_lawyer'], 'mortgage' => $T['ex_mortgage'], 'inspect' => $T['ex_inspect'], 'furniture' => $T['ex_furniture'] );
		$rid   = strtoupper( substr( $doc['token'], 0, 8 ) );
		header( 'Content-Type: text/html; charset=utf-8' );
		header( 'X-Robots-Tag: noindex' );
		?>
<!doctype html><html lang="<?php echo esc_attr( $doc['lang'] ); ?>" dir="<?php echo esc_attr( $T['dir'] ); ?>"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="robots" content="noindex">
<title><?php echo esc_html( $T['doc'] . ' ' . $rid ); ?></title>
<link href="https://fonts.googleapis.com/css2?family=Frank+Ruhl+Libre:wght@500;700&family=Heebo:wght@400;600;700&display=swap" rel="stylesheet">
<style>
body{margin:0;background:#EDE8DC;font-family:Heebo,system-ui,sans-serif;color:#1B1A17;padding:26px 14px}
.doc{max-width:760px;margin:0 auto;background:#FAF7F1;border:1px solid #E2DCD0;border-radius:16px;padding:34px 38px;box-shadow:0 10px 40px rgba(27,26,23,.12)}
h1{font-family:"Frank Ruhl Libre",serif;font-size:1.7rem;margin:0}
.mast{display:flex;justify-content:space-between;align-items:flex-start;gap:14px;border-bottom:2px solid #9C7A3C;padding-bottom:16px}
.mast .meta{text-align:end;font-size:12.5px;color:#6D665C;line-height:1.7}
.brand{font-family:"Frank Ruhl Libre",serif;font-weight:700;color:#9C7A3C;letter-spacing:.4px}
h2{font-family:"Frank Ruhl Libre",serif;font-size:1.05rem;margin:26px 0 10px;color:#1B1A17}
h2::after{content:"";display:block;width:44px;height:2px;background:#9C7A3C;margin-top:5px}
table{width:100%;border-collapse:collapse;font-size:14px}
td{padding:8px 10px;border-bottom:1px solid #EFE9DD}
td:first-child{color:#6D665C;width:38%}
.pill{display:inline-block;border:1px solid #9C7A3C;color:#7c5f2c;border-radius:999px;padding:4px 12px;font-size:12.5px;font-weight:600;margin:0 0 6px 6px;background:#F7F1E3}
.adv{border:1px solid #E2DCD0;border-radius:10px;background:#fff;padding:10px 14px;margin:7px 0;font-size:13.5px}
.adv small{color:#6D665C}
.tl{list-style:none;padding:0;margin:8px 0 0}
.tl li{display:flex;align-items:center;gap:10px;padding:7px 0;font-size:13.5px;color:#A79E8D}
.tl li .d{width:18px;height:18px;border-radius:50%;border:2px solid #D8CFBB;flex-shrink:0}
.tl li.on{color:#1B1A17;font-weight:600}
.tl li.on .d{background:#517048;border-color:#517048}
.disc{margin-top:26px;border-top:1px solid #E2DCD0;padding-top:14px;font-size:11.5px;color:#6D665C;line-height:1.65}
.bar{display:flex;gap:10px;justify-content:center;margin:18px auto 0;max-width:760px}
.bar a,.bar button{font:600 13.5px Heebo,sans-serif;border-radius:10px;padding:11px 18px;cursor:pointer;text-decoration:none;border:1px solid #E2DCD0;background:#fff;color:#1B1A17}
@media print{body{background:#fff;padding:0}.doc{border:0;box-shadow:none}.bar{display:none}}
</style></head><body>
<div class="doc">
	<div class="mast">
		<div><div class="brand">NadLan · nad-lan.co.il</div><h1><?php echo esc_html( $T['doc'] ); ?></h1>
		<?php if ( ! empty( $doc['buyer']['first'] ) ) : ?><div style="margin-top:5px;font-size:13.5px;color:#6D665C"><?php echo esc_html( $T['for'] . ': ' . $doc['buyer']['first'] ); ?></div><?php endif; ?></div>
		<div class="meta">ID <?php echo esc_html( $rid ); ?><br><?php echo esc_html( $T['date'] . ': ' . gmdate( 'd.m.Y', strtotime( $doc['created'] ) ) ); ?><br><?php echo esc_html( $T['valid'] ); ?></div>
	</div>
	<h2><?php echo esc_html( $T['unit'] ); ?></h2>
	<table>
		<tr><td><?php echo esc_html( $T['project'] ); ?></td><td><a href="<?php echo esc_url( $pr['url'] ); ?>" style="color:#1B1A17;font-weight:600"><?php echo esc_html( $pr['name'] ); ?></a></td></tr>
		<?php if ( $pr['developer'] ) : ?><tr><td><?php echo esc_html( $T['developer'] ); ?></td><td><?php echo esc_html( $pr['developer'] ); ?></td></tr><?php endif; ?>
		<?php if ( $u ) : ?>
		<tr><td><?php echo esc_html( $T['unit'] ); ?></td><td><?php echo esc_html( $u['label'] ?: $u['id'] ); ?></td></tr>
		<tr><td><?php echo esc_html( $T['floor'] ); ?></td><td><?php echo esc_html( $u['floor'] ); ?></td></tr>
		<tr><td><?php echo esc_html( $T['rooms'] ); ?></td><td><?php echo esc_html( $u['rooms'] ); ?></td></tr>
		<?php if ( $u['sqm'] ) : ?><tr><td><?php echo esc_html( $T['sqm'] ); ?></td><td><?php echo esc_html( $u['sqm'] ); ?></td></tr><?php endif; ?>
		<?php if ( $u['dir'] ) : ?><tr><td><?php echo esc_html( $T['dirn'] ); ?></td><td><?php echo esc_html( $u['dir'] ); ?></td></tr><?php endif; ?>
		<?php endif; ?>
	</table>
	<h2><?php echo esc_html( $T['config'] ); ?></h2>
	<table><tr><td><?php echo esc_html( $T['finish'] ); ?></td><td><?php echo esc_html( $T[ 'finish_' . $doc['finish'] ] ); ?></td></tr></table>
	<div style="margin-top:12px">
	<?php if ( $doc['extras'] ) : foreach ( $doc['extras'] as $x ) : ?><span class="pill"><?php echo esc_html( $exlbl[ $x ] ?? $x ); ?></span><?php endforeach; else : ?>
		<span style="font-size:13px;color:#6D665C"><?php echo esc_html( $T['none'] ); ?></span>
	<?php endif; ?>
	</div>
	<?php $has_adv = array_filter( (array) $doc['advisors'] ); if ( $doc['extras'] && array_intersect( $doc['extras'], array_keys( nadlan_rfp_advisor_map() ) ) ) : ?>
	<h2><?php echo esc_html( $T['advisors'] ); ?></h2>
	<?php if ( $has_adv ) : foreach ( $doc['advisors'] as $cat => $rows ) : foreach ( $rows as $a ) : ?>
		<div class="adv"><b><?php echo esc_html( $a['name'] ); ?></b> · <?php echo esc_html( $exlbl[ $cat ] ?? $cat ); ?><?php if ( $a['city'] ) : ?> <small>· <?php echo esc_html( $a['city'] ); ?></small><?php endif; ?></div>
	<?php endforeach; endforeach; else : ?>
		<div class="adv"><?php echo esc_html( $T['adv_none'] ); ?></div>
	<?php endif; endif; ?>
	<h2><?php echo esc_html( $T['status'] ); ?></h2>
	<ol class="tl">
		<li class="on"><span class="d"></span><?php echo esc_html( $T['st1'] ); ?></li>
		<li<?php echo (int) $doc['status'] >= 2 ? ' class="on"' : ''; ?>><span class="d"></span><?php echo esc_html( $T['st2'] ); ?></li>
		<li<?php echo (int) $doc['status'] >= 3 ? ' class="on"' : ''; ?>><span class="d"></span><?php echo esc_html( $T['st3'] ); ?></li>
	</ol>
	<p class="disc"><?php echo esc_html( $T['disc'] ); ?></p>
</div>
<div class="bar"><button onclick="window.print()"><?php echo esc_html( $T['print'] ); ?></button><a href="<?php echo esc_url( $pr['url'] ); ?>"><?php echo esc_html( $T['back'] ); ?></a></div>
</body></html>
		<?php
		exit;
	}
}

add_action( 'init', function () {
	register_post_type( 'nadlan_rfp', array(
		'label' => 'RFP documents', 'public' => false, 'show_ui' => true, 'show_in_menu' => 'edit.php?post_type=nadlan_project',
		'supports' => array( 'title' ), 'capability_type' => 'post', 'map_meta_cap' => true,
	) );
} );

add_action( 'rest_api_init', function () {
	register_rest_route( 'nadlan/v1', '/rfp', array(
		'methods' => 'POST', 'permission_callback' => '__return_true', 'callback' => 'nadlan_rfp_create',
	) );
	register_rest_route( 'nadlan/v1', '/rfp/(?P<token>[a-zA-Z0-9]{16,32})', array(
		'methods' => 'GET', 'permission_callback' => '__return_true', 'callback' => 'nadlan_rfp_render',
	) );
} );
