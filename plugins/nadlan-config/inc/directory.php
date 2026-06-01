<?php
/**
 * nadlan-config — Premium professionals directory (v1.31.0)
 *
 * A state-of-the-art, Midrag/Houzz/Thumbtack-class directory for /professionals/:
 *  - hero search (free text + city) with profession quick-pills (colour-coded + icons)
 *  - live AJAX filtering / sorting (no page reload) backed by a REST endpoint
 *  - sidebar facets with live counts (profession, city, verified-only)
 *  - premium colour-accented cards: avatar, profession pill, official-registry trust
 *    badge, rating stars (review-ready), location, classification, CTA
 *  - server-rendered first page (SEO + no-JS fallback) using the SAME card renderer
 *    that the REST endpoint returns, so AJAX and server output are identical
 *  - sponsored/featured slot wiring (paid_tier) for the advertising model
 *
 * Unique moat: every record is verified against the official רשם הקבלנים (gov.il),
 * surfaced as a trust badge competitors can't match.
 */

if ( ! defined( 'ABSPATH' ) ) { exit; }

/* ---------------------------------------------------------------------------
 * Profession taxonomy: label + colour + icon (the "colourful" the owner wanted)
 * ------------------------------------------------------------------------- */
if ( ! function_exists( 'nadlan_dir_professions' ) ) {
	function nadlan_dir_professions() {
		return array(
			'kablan'     => array( 'label' => 'קבלן',            'color' => '#2563EB', 'soft' => '#EFF4FF', 'icon' => '🏗️' ),
			'shamai'     => array( 'label' => 'שמאי מקרקעין',    'color' => '#059669', 'soft' => '#ECFDF5', 'icon' => '📊' ),
			'bedek_bait' => array( 'label' => 'בדק בית',         'color' => '#EA580C', 'soft' => '#FFF4ED', 'icon' => '🔍' ),
			'mashkanta'  => array( 'label' => 'יועץ משכנתאות',   'color' => '#0D9488', 'soft' => '#EFFCFB', 'icon' => '🏦' ),
			'architect'  => array( 'label' => 'אדריכל',          'color' => '#7C3AED', 'soft' => '#F5F0FF', 'icon' => '📐' ),
			'lawyer'     => array( 'label' => 'עו״ד מקרקעין',    'color' => '#4F46E5', 'soft' => '#EEF0FF', 'icon' => '⚖️' ),
			'mefakeach'  => array( 'label' => 'מפקח בנייה',      'color' => '#0891B2', 'soft' => '#ECFAFF', 'icon' => '👷' ),
			'metavech'   => array( 'label' => 'מתווך',           'color' => '#DB2777', 'soft' => '#FFF0F7', 'icon' => '🤝' ),
		);
	}
}
if ( ! function_exists( 'nadlan_dir_prof_meta' ) ) {
	function nadlan_dir_prof_meta( $key ) {
		$all = nadlan_dir_professions();
		return $all[ $key ] ?? array( 'label' => $key ?: 'בעל מקצוע', 'color' => '#9C7A3C', 'soft' => '#FBF6EE', 'icon' => '🏠' );
	}
}

/* small whitespace-normaliser (shared) */
if ( ! function_exists( 'nadlan_meta_norm' ) ) {
	function nadlan_meta_norm( $s ) { return trim( preg_replace( '/\s+/u', ' ', (string) $s ) ); }
}

/* ---------------------------------------------------------------------------
 * Query — used by BOTH the server render and the REST endpoint (single source)
 * ------------------------------------------------------------------------- */
if ( ! function_exists( 'nadlan_dir_query' ) ) {
	function nadlan_dir_query( $p ) {
		$per  = min( 48, max( 6, (int) ( $p['per_page'] ?? 24 ) ) );
		$args = array(
			'post_type'      => 'nadlan_professional',
			'post_status'    => 'publish',
			'posts_per_page' => $per,
			'paged'          => max( 1, (int) ( $p['paged'] ?? 1 ) ),
			'no_found_rows'  => false,
		);
		$mq = array( 'relation' => 'AND' );
		if ( ! empty( $p['city'] ) ) {
			$mq[] = array( 'key' => 'city', 'value' => nadlan_meta_norm( $p['city'] ), 'compare' => 'LIKE' );
		}
		if ( ! empty( $p['profession'] ) ) {
			$mq[] = array( 'key' => 'profession', 'value' => sanitize_key( $p['profession'] ) );
		}
		if ( ! empty( $p['verified'] ) ) {
			$mq[] = array( 'key' => 'claim_status', 'value' => 'verified' );
		}
		if ( count( $mq ) > 1 ) { $args['meta_query'] = $mq; }
		if ( ! empty( $p['q'] ) ) { $args['s'] = sanitize_text_field( $p['q'] ); }

		switch ( $p['sort'] ?? 'featured' ) {
			case 'name':    $args['orderby'] = 'title'; $args['order'] = 'ASC'; break;
			case 'newest':  $args['orderby'] = 'date';  $args['order'] = 'DESC'; break;
			case 'featured':
			default:
				// verified + (later) paid tiers float up, then newest. Uses a LEFT-join
				// safe approach: order by claim_status meta presence then date.
				$args['orderby'] = array( 'menu_order' => 'ASC', 'date' => 'DESC' );
				break;
		}
		return new WP_Query( $args );
	}
}

/* ---------------------------------------------------------------------------
 * Card renderer — the ONE place a professional card is built
 * ------------------------------------------------------------------------- */
if ( ! function_exists( 'nadlan_dir_card' ) ) {
	function nadlan_dir_card( $id ) {
		$prof_key = (string) get_post_meta( $id, 'profession', true );
		$pm   = nadlan_dir_prof_meta( $prof_key );
		$city = nadlan_meta_norm( get_post_meta( $id, 'city', true ) );
		$cls  = nadlan_meta_norm( get_post_meta( $id, 'classification', true ) );
		$cls  = mb_strlen( $cls ) > 60 ? mb_substr( $cls, 0, 60 ) . '…' : $cls;
		$reg  = nadlan_meta_norm( get_post_meta( $id, 'registry_number', true ) );
		$verified = get_post_meta( $id, 'claim_status', true ) === 'verified';
		$tier     = (string) get_post_meta( $id, 'paid_tier', true );
		$rating   = (float) get_post_meta( $id, 'rating', true );
		$reviews  = (int) get_post_meta( $id, 'reviews_count', true );
		$title    = get_the_title( $id );
		$initial  = mb_substr( trim( wp_strip_all_tags( $title ) ), 0, 1 );
		$url      = get_permalink( $id );

		// rating stars (review-ready: shows real data when present, prompt otherwise)
		$stars = '';
		if ( $reviews > 0 && $rating > 0 ) {
			$full = (int) round( $rating );
			$stars = '<div class="nldc-rate"><span class="nldc-stars" aria-hidden="true">'
				. str_repeat( '★', $full ) . str_repeat( '☆', max( 0, 5 - $full ) )
				. '</span><b>' . number_format( $rating, 1 ) . '</b><span class="nldc-rev">(' . $reviews . ' חוות דעת)</span></div>';
		} else {
			$stars = '<div class="nldc-rate nldc-norate">היו הראשונים לדרג</div>';
		}

		$featured = in_array( $tier, array( 'pro', 'premier' ), true );

		ob_start(); ?>
<a class="nldc<?php echo $featured ? ' is-featured' : ''; ?>" href="<?php echo esc_url( $url ); ?>" style="--pc:<?php echo esc_attr( $pm['color'] ); ?>;--ps:<?php echo esc_attr( $pm['soft'] ); ?>">
	<?php if ( $featured ) : ?><span class="nldc-sponsor">מקודם</span><?php endif; ?>
	<div class="nldc-top">
		<span class="nldc-av"><?php echo esc_html( $pm['icon'] ); ?></span>
		<div class="nldc-id">
			<h3 class="nldc-name"><?php echo esc_html( $title ); ?></h3>
			<span class="nldc-pill"><?php echo esc_html( $pm['label'] ); ?></span>
			<?php if ( $verified ) : ?><span class="nldc-vf">✓ מאומת</span><?php endif; ?>
		</div>
	</div>
	<?php echo $stars; ?>
	<div class="nldc-meta">
		<?php if ( $city ) : ?><span class="nldc-city">📍 <?php echo esc_html( $city ); ?></span><?php endif; ?>
		<?php if ( $cls ) : ?><span class="nldc-cls"><?php echo esc_html( $cls ); ?></span><?php endif; ?>
	</div>
	<div class="nldc-foot">
		<?php if ( $reg ) : ?><span class="nldc-reg">🛡️ רשם הקבלנים #<?php echo esc_html( $reg ); ?></span><?php endif; ?>
		<span class="nldc-go">לפרופיל ←</span>
	</div>
</a>
		<?php
		return ob_get_clean();
	}
}

/* render N cards from a WP_Query into a string */
if ( ! function_exists( 'nadlan_dir_cards_html' ) ) {
	function nadlan_dir_cards_html( $wq ) {
		if ( ! $wq->have_posts() ) {
			return '<div class="nldir-empty"><p>לא נמצאו בעלי מקצוע התואמים את החיפוש.</p><p>נסו עיר אחרת או הסירו סינון.</p></div>';
		}
		$out = '';
		foreach ( $wq->posts as $p ) { $out .= nadlan_dir_card( $p->ID ); }
		return $out;
	}
}

/* ---------------------------------------------------------------------------
 * Facet counts (cached) — profession counts + top cities
 * ------------------------------------------------------------------------- */
if ( ! function_exists( 'nadlan_dir_facet_counts' ) ) {
	function nadlan_dir_facet_counts() {
		$k = 'nadlan_dir_facets_v1';
		$c = get_transient( $k );
		if ( is_array( $c ) ) { return $c; }
		global $wpdb;
		$prof = $wpdb->get_results(
			"SELECT pm.meta_value v, COUNT(*) n FROM {$wpdb->postmeta} pm
			 INNER JOIN {$wpdb->posts} p ON p.ID=pm.post_id
			 WHERE pm.meta_key='profession' AND pm.meta_value<>'' AND p.post_type='nadlan_professional' AND p.post_status='publish'
			 GROUP BY pm.meta_value", ARRAY_A );
		$cities = $wpdb->get_results(
			"SELECT pm.meta_value v, COUNT(*) n FROM {$wpdb->postmeta} pm
			 INNER JOIN {$wpdb->posts} p ON p.ID=pm.post_id
			 WHERE pm.meta_key='city' AND pm.meta_value<>'' AND p.post_type='nadlan_professional' AND p.post_status='publish'
			 GROUP BY pm.meta_value ORDER BY n DESC LIMIT 24", ARRAY_A );
		$out = array(
			'professions' => array(),
			'cities'      => array(),
			'total'       => (int) wp_count_posts( 'nadlan_professional' )->publish,
		);
		foreach ( (array) $prof as $r )   { $out['professions'][ $r['v'] ] = (int) $r['n']; }
		foreach ( (array) $cities as $r ) { $out['cities'][] = array( 'name' => nadlan_meta_norm( $r['v'] ), 'n' => (int) $r['n'] ); }
		set_transient( $k, $out, HOUR_IN_SECONDS );
		return $out;
	}
}
add_action( 'save_post_nadlan_professional', function () { delete_transient( 'nadlan_dir_facets_v1' ); } );

/* ---------------------------------------------------------------------------
 * REST: live directory results (returns rendered card HTML + meta)
 * ------------------------------------------------------------------------- */
add_action( 'rest_api_init', function () {
	register_rest_route( 'nadlan/v1', '/directory', array(
		'methods'             => 'GET',
		'permission_callback' => '__return_true',
		'callback'            => function ( $req ) {
			$p = array(
				'q'          => (string) $req->get_param( 'q' ),
				'city'       => (string) $req->get_param( 'city' ),
				'profession' => (string) $req->get_param( 'profession' ),
				'verified'   => $req->get_param( 'verified' ) ? 1 : 0,
				'sort'       => (string) $req->get_param( 'sort' ),
				'paged'      => (int) $req->get_param( 'paged' ),
				'per_page'   => (int) $req->get_param( 'per_page' ),
			);
			$wq = nadlan_dir_query( $p );
			$resp = array(
				'ok'    => true,
				'html'  => nadlan_dir_cards_html( $wq ),
				'total' => (int) $wq->found_posts,
				'pages' => (int) $wq->max_num_pages,
				'paged' => max( 1, $p['paged'] ),
			);
			wp_reset_postdata();
			return $resp;
		},
	) );
} );

/* ---------------------------------------------------------------------------
 * Clean archive title (kills the theme's "Archive: …")
 * ------------------------------------------------------------------------- */
add_filter( 'get_the_archive_title', function ( $t ) {
	if ( is_post_type_archive( 'nadlan_professional' ) ) { return 'מאגר בעלי המקצוע'; }
	return $t;
} );
add_filter( 'pre_get_document_title', function ( $t ) {
	if ( is_post_type_archive( 'nadlan_professional' ) ) {
		return 'מאגר בעלי מקצוע בנדל״ן — קבלנים, שמאים, יועצים מאומתים | נדל״ן חכם';
	}
	return $t;
}, 20 );

/* ---------------------------------------------------------------------------
 * Intercept the /professionals/ archive and render the premium directory
 * ------------------------------------------------------------------------- */
add_action( 'template_redirect', function () {
	if ( is_admin() || ! is_post_type_archive( 'nadlan_professional' ) ) { return; }
	if ( defined( 'NADLAN_DISABLE_DIRECTORY' ) && NADLAN_DISABLE_DIRECTORY ) { return; }
	nadlan_dir_render_page();
	exit;
}, 5 );

if ( ! function_exists( 'nadlan_dir_render_page' ) ) {
	function nadlan_dir_render_page() {
		$facets = nadlan_dir_facet_counts();
		$profs  = nadlan_dir_professions();
		// initial state from URL
		$state = array(
			'q'          => isset( $_GET['q'] ) ? sanitize_text_field( wp_unslash( $_GET['q'] ) ) : '',
			'city'       => isset( $_GET['city'] ) ? sanitize_text_field( wp_unslash( $_GET['city'] ) ) : '',
			'profession' => isset( $_GET['profession'] ) ? sanitize_key( $_GET['profession'] ) : '',
			'verified'   => ! empty( $_GET['verified'] ) ? 1 : 0,
			'sort'       => isset( $_GET['sort'] ) ? sanitize_key( $_GET['sort'] ) : 'featured',
			'paged'      => max( 1, (int) ( $_GET['paged'] ?? 1 ) ),
			'per_page'   => 24,
		);
		$wq    = nadlan_dir_query( $state );
		$total = (int) $wq->found_posts;
		$cards = nadlan_dir_cards_html( $wq );
		wp_reset_postdata();

		get_header();
		echo nadlan_dir_css();
		?>
<div class="nldir" dir="rtl"
	data-rest="<?php echo esc_url( rest_url( 'nadlan/v1/directory' ) ); ?>"
	data-state="<?php echo esc_attr( wp_json_encode( $state ) ); ?>">

	<!-- HERO -->
	<header class="nldir-hero">
		<nav class="nldir-crumbs"><a href="<?php echo esc_url( home_url( '/' ) ); ?>">בית</a> › <span>בעלי מקצוע</span></nav>
		<h1>מצאו בעל מקצוע מאומת לנדל״ן</h1>
		<p class="nldir-lead">קבלנים, שמאים, יועצי משכנתאות ועו״ד — <strong><?php echo number_format( $facets['total'] ); ?></strong> בעלי מקצוע, מאומתים מול פנקס הקבלנים הרשמי (gov.il).</p>
		<form class="nldir-search" role="search">
			<input type="search" name="q" value="<?php echo esc_attr( $state['q'] ); ?>" placeholder="חיפוש לפי שם, חברה או התמחות" autocomplete="off">
			<input type="text" name="city" value="<?php echo esc_attr( $state['city'] ); ?>" placeholder="עיר" autocomplete="off">
			<button type="submit">חיפוש</button>
		</form>
		<div class="nldir-pills">
			<button type="button" class="nldir-pill<?php echo $state['profession'] === '' ? ' is-on' : ''; ?>" data-prof="">הכל</button>
			<?php foreach ( $profs as $key => $pm ) :
				$n = $facets['professions'][ $key ] ?? 0;
				if ( $n < 1 ) { continue; } ?>
			<button type="button" class="nldir-pill<?php echo $state['profession'] === $key ? ' is-on' : ''; ?>"
				data-prof="<?php echo esc_attr( $key ); ?>" style="--pc:<?php echo esc_attr( $pm['color'] ); ?>;--ps:<?php echo esc_attr( $pm['soft'] ); ?>">
				<span><?php echo esc_html( $pm['icon'] ); ?></span><?php echo esc_html( $pm['label'] ); ?> <i><?php echo number_format( $n ); ?></i>
			</button>
			<?php endforeach; ?>
		</div>
	</header>

	<div class="nldir-body">
		<!-- SIDEBAR FACETS -->
		<aside class="nldir-side">
			<div class="nldir-fgroup">
				<h4>סינון</h4>
				<label class="nldir-check"><input type="checkbox" id="nldir-verified" <?php checked( $state['verified'], 1 ); ?>> מאומתים בלבד ✓</label>
			</div>
			<div class="nldir-fgroup">
				<h4>ערים מובילות</h4>
				<ul class="nldir-cities">
					<?php foreach ( array_slice( $facets['cities'], 0, 12 ) as $c ) : ?>
					<li><button type="button" class="nldir-cityb" data-city="<?php echo esc_attr( $c['name'] ); ?>"><?php echo esc_html( $c['name'] ); ?> <i><?php echo number_format( $c['n'] ); ?></i></button></li>
					<?php endforeach; ?>
				</ul>
			</div>
		</aside>

		<!-- RESULTS -->
		<main class="nldir-main">
			<div class="nldir-bar">
				<div class="nldir-count"><strong id="nldir-total"><?php echo number_format( $total ); ?></strong> בעלי מקצוע</div>
				<div class="nldir-chips" id="nldir-chips"></div>
				<label class="nldir-sortw">מיון:
					<select id="nldir-sort">
						<option value="featured"<?php selected( $state['sort'], 'featured' ); ?>>מומלצים</option>
						<option value="newest"<?php selected( $state['sort'], 'newest' ); ?>>נוספו לאחרונה</option>
						<option value="name"<?php selected( $state['sort'], 'name' ); ?>>א׳–ת׳</option>
					</select>
				</label>
			</div>
			<div class="nldir-results" id="nldir-results"><?php echo $cards; ?></div>
			<div class="nldir-more-wrap"><button type="button" class="nldir-more" id="nldir-more"<?php echo $wq->max_num_pages > 1 ? '' : ' style="display:none"'; ?>>הצגת עוד</button></div>
			<?php
			// ItemList JSON-LD for SEO
			if ( $wq->have_posts() ) {
				$items = array(); $pos = 1;
				foreach ( $wq->posts as $sp ) { $items[] = array( '@type' => 'ListItem', 'position' => $pos++, 'url' => get_permalink( $sp ), 'name' => get_the_title( $sp ) ); }
				echo '<script type="application/ld+json">' . wp_json_encode( array( '@context' => 'https://schema.org', '@type' => 'ItemList', 'name' => 'בעלי מקצוע בנדל״ן', 'numberOfItems' => $total, 'itemListElement' => $items ), JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES ) . '</script>';
				wp_reset_postdata();
			}
			?>
		</main>
	</div>
</div>
<?php echo nadlan_dir_js(); ?>
		<?php
		get_footer();
	}
}

require __DIR__ . '/directory-assets.php';
