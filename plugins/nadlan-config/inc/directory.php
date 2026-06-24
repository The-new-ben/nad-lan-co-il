<?php
/**
 * nadlan-config  -  Premium professionals directory (v1.31.0)
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
			'kablan'     => array( 'label' => 'קבלן',            'color' => '#334236', 'soft' => '#F1F4EE', 'icon' => 'profession-contractor' ),
			'shamai'     => array( 'label' => 'שמאי מקרקעין',    'color' => '#183C3C', 'soft' => '#EFF4F4', 'icon' => 'profession-appraiser' ),
			'bedek_bait' => array( 'label' => 'בדק בית',         'color' => '#9F6F54', 'soft' => '#F8F0EA', 'icon' => 'profession-inspector' ),
			'mashkanta'  => array( 'label' => 'יועץ משכנתאות',   'color' => '#334236', 'soft' => '#F1F4EE', 'icon' => 'profession-mortgage' ),
			'architect'  => array( 'label' => 'אדריכל',          'color' => '#183C3C', 'soft' => '#EFF4F4', 'icon' => 'profession-architect' ),
			'lawyer'     => array( 'label' => 'עו״ד מקרקעין',    'color' => '#11110F', 'soft' => '#EFEDE7', 'icon' => 'profession-lawyer' ),
			'mefakeach'  => array( 'label' => 'מפקח בנייה',      'color' => '#9F6F54', 'soft' => '#F8F0EA', 'icon' => 'profession-inspector' ),
			'metavech'   => array( 'label' => 'מתווך',           'color' => '#9C7A3C', 'soft' => '#FBF6EE', 'icon' => 'profession-broker' ),
		);
	}
}
if ( ! function_exists( 'nadlan_dir_prof_meta' ) ) {
	function nadlan_dir_prof_meta( $key ) {
		$all = nadlan_dir_professions();
		return $all[ $key ] ?? array( 'label' => $key ?: 'בעל מקצוע', 'color' => '#9C7A3C', 'soft' => '#FBF6EE', 'icon' => 'profession-broker' );
	}
}

/* small whitespace-normaliser (shared) */
if ( ! function_exists( 'nadlan_meta_norm' ) ) {
	function nadlan_meta_norm( $s ) { return trim( preg_replace( '/\s+/u', ' ', (string) $s ) ); }
}

if ( ! function_exists( 'nadlan_dir_use_paid_placement_boost' ) ) {
	function nadlan_dir_use_paid_placement_boost( $args ) {
		$args['orderby']                      = 'none';
		$args['nadlan_paid_placement_boost'] = 1;
		return $args;
	}
}

if ( ! function_exists( 'nadlan_dir_paid_placement_clauses' ) ) {
	function nadlan_dir_paid_placement_clauses( $clauses, $query ) {
		if ( ! $query->get( 'nadlan_paid_placement_boost' ) ) {
			return $clauses;
		}

		global $wpdb;
		$alias = 'nadlan_paid_tier_pm';
		if ( strpos( $clauses['join'], " AS {$alias} " ) === false ) {
			$clauses['join'] .= $wpdb->prepare(
				" LEFT JOIN {$wpdb->postmeta} AS {$alias} ON ({$wpdb->posts}.ID = {$alias}.post_id AND {$alias}.meta_key = %s)",
				'paid_tier'
			);
		}
		$clauses['orderby'] = "CASE {$alias}.meta_value WHEN 'premier' THEN 2 WHEN 'pro' THEN 1 ELSE 0 END DESC, {$wpdb->posts}.menu_order ASC, {$wpdb->posts}.post_date DESC, {$wpdb->posts}.ID DESC";
		return $clauses;
	}
}
add_filter( 'posts_clauses', 'nadlan_dir_paid_placement_clauses', 20, 2 );

/* ---------------------------------------------------------------------------
 * Query  -  used by BOTH the server render and the REST endpoint (single source)
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
				$args = nadlan_dir_use_paid_placement_boost( $args );
				break;
		}
		return new WP_Query( $args );
	}
}

/* ---------------------------------------------------------------------------
 * Card renderer  -  the ONE place a professional card is built
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
		$distance = apply_filters( 'nadlan_geo_card_distance', null, $id );
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
		<span class="nldc-av" aria-hidden="true"><svg class="nl-mark" viewBox="0 0 48 48"><use href="#<?php echo esc_attr( $pm['icon'] ); ?>"></use></svg></span>
		<div class="nldc-id">
			<h3 class="nldc-name"><?php echo esc_html( $title ); ?></h3>
			<span class="nldc-pill"><?php echo esc_html( $pm['label'] ); ?></span>
			<?php if ( $verified ) : ?><span class="nldc-vf">✓ מאומת</span><?php endif; ?>
		</div>
	</div>
	<?php echo $stars; ?>
	<div class="nldc-meta">
		<?php if ( $city ) : ?><span class="nldc-city"><svg class="nl-ico" aria-hidden="true" viewBox="0 0 16 16"><path fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" d="M8 14s5-4.5 5-8.5A5 5 0 1 0 3 5.5C3 9.5 8 14 8 14z"/><circle cx="8" cy="5.5" r="1.8" fill="none" stroke="currentColor" stroke-width="1.4"/></svg><?php echo esc_html( $city ); ?></span><?php endif; ?>
		<?php if ( $distance !== null && $distance !== '' ) : ?><span class="nldc-distance"><?php echo esc_html( number_format_i18n( (float) $distance, 1 ) ); ?> ק״מ</span><?php endif; ?>
		<?php if ( $cls ) : ?><span class="nldc-cls"><?php echo esc_html( $cls ); ?></span><?php endif; ?>
	</div>
	<div class="nldc-foot">
		<?php if ( $reg ) : ?><span class="nldc-reg"><svg class="nl-ico" aria-hidden="true" viewBox="0 0 16 16"><path fill="none" stroke="currentColor" stroke-width="1.4" stroke-linejoin="round" d="M8 1.5l5.5 2v4c0 3.5-2.5 6-5.5 7-3-1-5.5-3.5-5.5-7v-4l5.5-2z"/><path fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round" d="M5.5 8l2 2 3-4"/></svg>רשם הקבלנים #<?php echo esc_html( $reg ); ?></span><?php endif; ?>
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
		return apply_filters( 'nadlan_dir_cards_html', $out, 'nadlan_professional' );
	}
}

/* ---------------------------------------------------------------------------
 * Facet counts (cached)  -  profession counts + top cities
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
		return 'מאגר בעלי מקצוע בנדל״ן: קבלנים, שמאים, יועצים מאומתים | נדל״ן חכם';
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
		if ( function_exists( 'block_template_part' ) ) { block_template_part( 'header' ); }
		echo nadlan_dir_css();
		?>
<div class="nldir" dir="rtl"
	data-rest="<?php echo esc_url( rest_url( 'nadlan/v1/directory' ) ); ?>"
	data-state="<?php echo esc_attr( wp_json_encode( $state ) ); ?>">

	<!-- HERO -->
	<header class="nldir-hero">
		<nav class="nldir-crumbs"><a href="<?php echo esc_url( home_url( '/' ) ); ?>">בית</a> › <span>בעלי מקצוע</span></nav>
		<h1>מצאו בעל מקצוע מאומת לנדל״ן</h1>
		<p class="nldir-lead">קבלנים, שמאים, יועצי משכנתאות ועו״ד: <strong><?php echo number_format( $facets['total'] ); ?></strong> בעלי מקצוע, מאומתים מול פנקס הקבלנים הרשמי (gov.il).</p>
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
				<span class="nldir-pill-mark" aria-hidden="true"><svg viewBox="0 0 48 48"><use href="#<?php echo esc_attr( $pm['icon'] ); ?>"></use></svg></span><?php echo esc_html( $pm['label'] ); ?> <i><?php echo number_format( $n ); ?></i>
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
		// Block theme footer: get_footer() is a noop when there's no footer.php,
		// so explicitly render the theme's footer template part first.
		if ( function_exists( 'block_template_part' ) ) { block_template_part( 'footer' ); }
		get_footer();
	}
}

/* ---------------------------------------------------------------------------
 * Single professional PROFILE  -  premium colour header + "similar pros"
 * (prepended/appended around the existing facts table from cards-render.php)
 * ------------------------------------------------------------------------- */
if ( ! function_exists( 'nadlan_dir_enqueue_professional_quote_script' ) ) {
	function nadlan_dir_enqueue_professional_quote_script() {
		static $done = false;
		if ( $done ) {
			return;
		}
		$done = true;
		$rest = esc_url_raw( rest_url( 'nadlan/v1/referral/route' ) );
		wp_register_script( 'nadlan-professional-quote', '', array(), '1.61.0', true );
		wp_enqueue_script( 'nadlan-professional-quote' );
		wp_add_inline_script(
			'nadlan-professional-quote',
			'window.nadlanProQuote=window.nadlanProQuote||function(id,name){var n=window.prompt("שמכם:");if(!n)return;var p=window.prompt("טלפון ליצירת קשר:");if(!p)return;window.fetch("' . esc_js( $rest ) . '",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({customer_name:n,customer_phone:p,partner_id:id,topic:"הצעת מחיר - "+name,source_url:window.location.href,notify_partner:0})}).then(function(r){return r.json();}).then(function(d){window.alert((d&&d.ok)?"הבקשה נשלחה. נחזור אליכם עם פרטים.":"שגיאה, נסו שוב.");}).catch(function(){window.alert("שגיאה, נסו שוב.");});};document.addEventListener("click",function(e){var btn=e.target.closest("[data-nadlan-professional-quote]");if(!btn)return;window.nadlanProQuote(parseInt(btn.dataset.partnerId||"0",10),btn.dataset.partnerTitle||"בעל המקצוע");});',
			'after'
		);
	}
}

if ( ! function_exists( 'nadlan_dir_profile_header' ) ) {
	function nadlan_dir_profile_header( $id ) {
		$pm   = nadlan_dir_prof_meta( (string) get_post_meta( $id, 'profession', true ) );
		$city = nadlan_meta_norm( get_post_meta( $id, 'city', true ) );
		$cls  = nadlan_meta_norm( get_post_meta( $id, 'classification', true ) );
		$reg  = nadlan_meta_norm( get_post_meta( $id, 'registry_number', true ) );
		$phone= nadlan_meta_norm( get_post_meta( $id, 'phone', true ) );
		$verified = get_post_meta( $id, 'claim_status', true ) === 'verified';
		$rating   = (float) get_post_meta( $id, 'rating', true );
		$reviews  = (int) get_post_meta( $id, 'reviews_count', true );
		$title    = get_the_title( $id );
		nadlan_dir_enqueue_professional_quote_script();

		$stars = ( $reviews > 0 && $rating > 0 )
			? '<span class="nlpf-stars">' . str_repeat( '★', (int) round( $rating ) ) . str_repeat( '☆', max( 0, 5 - (int) round( $rating ) ) ) . '</span> <b>' . number_format( $rating, 1 ) . '</b> <span class="nlpf-rev">(' . $reviews . ' חוות דעת)</span>'
			: '<span class="nlpf-norate">טרם התקבלו חוות דעת. היו הראשונים לדרג.</span>';

		ob_start(); ?>
<div class="nlpf" dir="rtl" style="--pc:<?php echo esc_attr( $pm['color'] ); ?>;--ps:<?php echo esc_attr( $pm['soft'] ); ?>">
	<div class="nlpf-banner"></div>
	<div class="nlpf-head">
		<span class="nlpf-av" aria-hidden="true"><svg class="nl-mark" viewBox="0 0 48 48"><use href="#<?php echo esc_attr( $pm['icon'] ); ?>"></use></svg></span>
		<div class="nlpf-id">
			<div class="nlpf-badges">
				<span class="nlpf-pill"><?php echo esc_html( $pm['label'] ); ?></span>
				<?php if ( $verified ) : ?><span class="nlpf-vf">✓ בעלות מאומתת</span><?php endif; ?>
				<?php if ( $reg ) : ?><span class="nlpf-reg"><svg class="nl-ico" aria-hidden="true" viewBox="0 0 16 16"><path fill="none" stroke="currentColor" stroke-width="1.4" stroke-linejoin="round" d="M8 1.5l5.5 2v4c0 3.5-2.5 6-5.5 7-3-1-5.5-3.5-5.5-7v-4l5.5-2z"/><path fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round" d="M5.5 8l2 2 3-4"/></svg>רשם הקבלנים #<?php echo esc_html( $reg ); ?></span><?php endif; ?>
			</div>
			<h1 class="nlpf-name"><?php echo esc_html( $title ); ?></h1>
			<div class="nlpf-sub">
				<?php if ( $city ) : ?><span><svg class="nl-ico" aria-hidden="true" viewBox="0 0 16 16"><path fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" d="M8 14s5-4.5 5-8.5A5 5 0 1 0 3 5.5C3 9.5 8 14 8 14z"/><circle cx="8" cy="5.5" r="1.8" fill="none" stroke="currentColor" stroke-width="1.4"/></svg><?php echo esc_html( $city ); ?></span><?php endif; ?>
				<?php if ( $cls ) : ?><span><?php echo esc_html( $cls ); ?></span><?php endif; ?>
			</div>
			<div class="nlpf-rate"><?php echo $stars; ?></div>
		</div>
		<div class="nlpf-cta">
			<?php if ( $phone ) : ?><a class="nlpf-call" href="tel:<?php echo esc_attr( preg_replace( '/[^0-9+]/', '', $phone ) ); ?>"><svg class="nl-ico" aria-hidden="true" viewBox="0 0 16 16"><path fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" d="M5.5 2.5c.3 1 .7 2 1.2 2.8.2.3.1.7-.1 1l-.9.9c.7 1.4 1.8 2.5 3.2 3.2l.9-.9c.3-.2.7-.3 1-.1.8.5 1.8.9 2.8 1.2.4.1.6.5.6.9V14a1 1 0 0 1-1.1 1A11.5 11.5 0 0 1 2 4.1 1 1 0 0 1 3 3h1.6c.4 0 .8.2.9.6z"/></svg>התקשרו</a><?php endif; ?>
			<button type="button" class="nlpf-quote" data-nadlan-professional-quote data-partner-id="<?php echo (int) $id; ?>" data-partner-title="<?php echo esc_attr( $title ); ?>">בקשת הצעת מחיר</button>
		</div>
	</div>
</div>
<style>
.nlpf{font-family:var(--font-sans,Heebo,sans-serif);border:1px solid rgba(27,26,23,.1);border-radius:18px;overflow:hidden;margin:0 0 26px;background:#fff;direction:rtl}
.nlpf-banner{height:90px;background:linear-gradient(120deg,var(--pc),color-mix(in srgb,var(--pc) 55%,#1B1A17))}
.nlpf-head{display:flex;gap:18px;align-items:flex-start;padding:0 24px 22px;margin-top:-34px;flex-wrap:wrap}
.nlpf-av{flex:none;width:84px;height:84px;border-radius:20px;display:grid;place-items:center;font-size:42px;background:var(--ps);border:4px solid #fff;box-shadow:0 8px 20px rgba(0,0,0,.12)}
.nlpf-id{flex:1;min-width:200px;padding-top:42px}
.nlpf-badges{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:8px}
.nlpf-pill{background:var(--ps);color:var(--pc);font-weight:700;font-size:12.5px;padding:4px 12px;border-radius:20px}
.nlpf-vf{color:#059669;font-weight:700;font-size:12.5px;background:#ECFDF5;padding:4px 12px;border-radius:20px}
.nlpf-reg{color:#7a7a7a;font-weight:600;font-size:11.5px;background:#F6F4F0;padding:4px 12px;border-radius:20px}
.nlpf-name{font-family:var(--font-serif,"Frank Ruhl Libre",serif);font-weight:600;font-size:clamp(24px,4vw,34px);margin:0 0 8px;line-height:1.15;color:#1B1A17}
.nlpf-sub{display:flex;gap:16px;flex-wrap:wrap;color:#5a5a5a;font-size:14px;margin-bottom:8px}
.nlpf-sub span:first-child{font-weight:600;color:#1B1A17}
.nlpf-rate{font-size:14px}.nlpf-stars{color:#F5A623;letter-spacing:1px}.nlpf-rev{color:#9a9a9a;font-size:12.5px}.nlpf-norate{color:#b9b4a9;font-style:italic;font-size:13px}
.nlpf-cta{display:flex;flex-direction:column;gap:9px;padding-top:46px;min-width:170px}
.nlpf-call,.nlpf-quote{text-align:center;border-radius:10px;padding:13px 22px;font:inherit;font-weight:700;font-size:14.5px;cursor:pointer;text-decoration:none;border:0;transition:transform .15s,filter .2s}
.nlpf-call{background:#fff;color:var(--pc);border:1.5px solid var(--pc)}
.nlpf-quote{background:linear-gradient(135deg,var(--pc),color-mix(in srgb,var(--pc) 70%,#000));color:#fff}
.nlpf-call:hover,.nlpf-quote:hover{transform:translateY(-2px);filter:brightness(1.05)}
@media(max-width:640px){.nlpf-cta{width:100%;flex-direction:row}.nlpf-call,.nlpf-quote{flex:1}}
</style>
		<?php
		return ob_get_clean();
	}
}

/* "Similar professionals"  -  same profession or city, for internal linking */
if ( ! function_exists( 'nadlan_dir_similar' ) ) {
	function nadlan_dir_similar( $id ) {
		$prof = (string) get_post_meta( $id, 'profession', true );
		$city = nadlan_meta_norm( get_post_meta( $id, 'city', true ) );
		$mq = array( 'relation' => 'OR' );
		if ( $prof ) { $mq[] = array( 'key' => 'profession', 'value' => $prof ); }
		if ( $city ) { $mq[] = array( 'key' => 'city', 'value' => $city, 'compare' => 'LIKE' ); }
		if ( count( $mq ) < 2 ) { return ''; }
		$q = new WP_Query( array(
			'post_type' => 'nadlan_professional', 'post_status' => 'publish',
			'posts_per_page' => 4, 'post__not_in' => array( $id ),
			'orderby' => 'rand', 'meta_query' => $mq, 'no_found_rows' => true,
		) );
		if ( ! $q->have_posts() ) { return ''; }
		$cards = '';
		foreach ( $q->posts as $p ) { $cards .= nadlan_dir_card( $p->ID ); }
		wp_reset_postdata();
		return '<section class="nldir nldir-similar" dir="rtl"><h2 style="font-family:var(--font-serif,serif);font-weight:600;font-size:24px;margin:34px 0 16px;color:#1B1A17">בעלי מקצוע דומים</h2><div class="nldir-results">' . $cards . '</div></section>' . nadlan_dir_css();
	}
}

add_filter( 'the_content', function ( $content ) {
	if ( ! is_singular( 'nadlan_professional' ) || ! in_the_loop() || ! is_main_query() ) { return $content; }
	return nadlan_dir_profile_header( get_the_ID() ) . $content . nadlan_dir_similar( get_the_ID() );
}, 5 );

/* v1.37.0: clean document title for the glossary (nadlan_term) archive  - 
 * was showing the default "ארכיון NadLan Glossary". */
add_filter( 'get_the_archive_title', function ( $t ) {
	if ( is_post_type_archive( 'nadlan_term' ) ) { return 'מילון מונחי נדל״ן'; }
	return $t;
}, 30 );
add_filter( 'pre_get_document_title', function ( $t ) {
	if ( is_post_type_archive( 'nadlan_term' ) ) {
		return 'מילון מונחי נדל״ן | מושגים, מיסוי, משכנתאות ובנייה | נדל״ן חכם';
	}
	return $t;
}, 20 );

/* v1.37.0: premium profile header for single PROJECT pages (parity with
 * professionals  -  they were rendering bare). Uses nadlan_dir_pt_meta defined
 * in the projects section below (runtime call, so order is fine). */
if ( ! function_exists( 'nadlan_dir_enqueue_project_quote_script' ) ) {
	function nadlan_dir_enqueue_project_quote_script() {
		static $done = false;
		if ( $done ) {
			return;
		}
		$done = true;
		wp_register_script( 'nadlan-project-profile-quote', '', array(), '1.61.0', true );
		wp_enqueue_script( 'nadlan-project-profile-quote' );
		$rest = esc_url_raw( rest_url( 'nadlan/v1/lead' ) );
		wp_add_inline_script(
			'nadlan-project-profile-quote',
			'window.nadlanProjQuote=window.nadlanProjQuote||function(id,name){var n=window.prompt("שמכם:");if(!n)return;var p=window.prompt("טלפון ליצירת קשר:");if(!p)return;window.fetch("' . esc_js( $rest ) . '",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({name:n,phone:p,topic:"מידע על פרויקט",message:"פנייה לגבי: "+name+" (#"+id+")",source:"project-profile",card_id:id})}).then(function(){window.alert("הבקשה נשלחה. נחזור אליכם עם פרטים.");}).catch(function(){window.alert("שגיאה, נסו שוב.");});};document.addEventListener("click",function(e){var btn=e.target.closest("[data-nadlan-project-quote]");if(!btn)return;window.nadlanProjQuote(parseInt(btn.dataset.cardId||"0",10),btn.dataset.cardTitle||"הפרויקט");});',
			'after'
		);
	}
}
if ( ! function_exists( 'nadlan_dir_project_profile_header' ) ) {
	function nadlan_dir_project_profile_header( $id ) {
		nadlan_dir_enqueue_project_quote_script();
		$pm     = nadlan_dir_pt_meta( (string) get_post_meta( $id, 'project_type', true ) );
		$city   = nadlan_meta_norm( get_post_meta( $id, 'city', true ) );
		$units  = (int) get_post_meta( $id, 'num_units', true );
		$status = nadlan_meta_norm( get_post_meta( $id, 'project_status', true ) );
		$dev    = nadlan_meta_norm( get_post_meta( $id, 'developer_name', true ) );
		$addr   = nadlan_meta_norm( get_post_meta( $id, 'address', true ) );
		$title  = get_the_title( $id );
		ob_start(); ?>
<div class="nlpf" dir="rtl" style="--pc:<?php echo esc_attr( $pm['color'] ); ?>;--ps:<?php echo esc_attr( $pm['soft'] ); ?>">
	<div class="nlpf-banner"></div>
	<div class="nlpf-head">
		<span class="nlpf-av" aria-hidden="true"><svg class="nl-mark" viewBox="0 0 48 48"><use href="#<?php echo esc_attr( $pm['icon'] ); ?>"></use></svg></span>
		<div class="nlpf-id">
			<div class="nlpf-badges">
				<span class="nlpf-pill"><?php echo esc_html( $pm['label'] ); ?></span>
				<span class="nlpf-reg"><svg class="nl-ico" aria-hidden="true" viewBox="0 0 16 16"><path fill="none" stroke="currentColor" stroke-width="1.4" stroke-linejoin="round" d="M8 1.5l5.5 2v4c0 3.5-2.5 6-5.5 7-3-1-5.5-3.5-5.5-7v-4l5.5-2z"/><path fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round" d="M5.5 8l2 2 3-4"/></svg>מאגר התחדשות עירונית · data.gov.il</span>
			</div>
			<h1 class="nlpf-name"><?php echo esc_html( $title ); ?></h1>
			<div class="nlpf-sub">
				<?php if ( $city ) : ?><span><svg class="nl-ico" aria-hidden="true" viewBox="0 0 16 16"><path fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" d="M8 14s5-4.5 5-8.5A5 5 0 1 0 3 5.5C3 9.5 8 14 8 14z"/><circle cx="8" cy="5.5" r="1.8" fill="none" stroke="currentColor" stroke-width="1.4"/></svg><?php echo esc_html( $city ); ?><?php echo $addr ? ', ' . esc_html( $addr ) : ''; ?></span><?php endif; ?>
				<?php if ( $units > 0 ) : ?><span><svg class="nl-ico" aria-hidden="true" viewBox="0 0 16 16"><path fill="none" stroke="currentColor" stroke-width="1.4" stroke-linejoin="round" d="M2 7l6-5 6 5v7H2zM6.5 14v-4h3v4"/></svg><?php echo number_format( $units ); ?> יח״ד</span><?php endif; ?>
				<?php if ( $status ) : ?><span><svg class="nl-ico" aria-hidden="true" viewBox="0 0 16 16"><rect x="3" y="2" width="10" height="12" rx="1.5" fill="none" stroke="currentColor" stroke-width="1.4"/><path fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" d="M6 6h4M6 9h4"/></svg><?php echo esc_html( $status ); ?></span><?php endif; ?>
				<?php if ( $dev ) : ?><span><svg class="nl-ico" aria-hidden="true" viewBox="0 0 16 16"><circle cx="8" cy="5.5" r="2.5" fill="none" stroke="currentColor" stroke-width="1.4"/><path fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" d="M3 14c.5-2.5 2.5-4 5-4s4.5 1.5 5 4"/></svg><?php echo esc_html( $dev ); ?></span><?php endif; ?>
			</div>
		</div>
		<div class="nlpf-cta">
			<button type="button" class="nlpf-quote" data-nadlan-project-quote data-card-id="<?php echo (int) $id; ?>" data-card-title="<?php echo esc_attr( $title ); ?>">קבלת מידע על הפרויקט</button>
		</div>
	</div>
</div>
<style>
.nlpf{font-family:var(--font-sans,Heebo,sans-serif);border:1px solid rgba(27,26,23,.1);border-radius:18px;overflow:hidden;margin:0 0 26px;background:#fff;direction:rtl}
.nlpf-banner{height:90px;background:linear-gradient(120deg,var(--pc),color-mix(in srgb,var(--pc) 55%,#1B1A17))}
.nlpf-head{display:flex;gap:18px;align-items:flex-start;padding:0 24px 22px;margin-top:-34px;flex-wrap:wrap}
.nlpf-av{flex:none;width:84px;height:84px;border-radius:20px;display:grid;place-items:center;font-size:42px;background:var(--ps);border:4px solid #fff;box-shadow:0 8px 20px rgba(0,0,0,.12)}
.nlpf-id{flex:1;min-width:200px;padding-top:42px}
.nlpf-badges{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:8px}
.nlpf-pill{background:var(--ps);color:var(--pc);font-weight:700;font-size:12.5px;padding:4px 12px;border-radius:20px}
.nlpf-reg{color:#7a7a7a;font-weight:600;font-size:11.5px;background:#F6F4F0;padding:4px 12px;border-radius:20px}
.nlpf-name{font-family:var(--font-serif,"Frank Ruhl Libre",serif);font-weight:600;font-size:clamp(24px,4vw,34px);margin:0 0 8px;line-height:1.15;color:#1B1A17}
.nlpf-sub{display:flex;gap:16px;flex-wrap:wrap;color:#5a5a5a;font-size:14px;margin-bottom:8px}
.nlpf-sub span:first-child{font-weight:600;color:#1B1A17}
.nlpf-cta{display:flex;flex-direction:column;gap:9px;padding-top:46px;min-width:170px}
.nlpf-quote{text-align:center;border-radius:10px;padding:13px 22px;font:inherit;font-weight:700;font-size:14.5px;cursor:pointer;border:0;background:linear-gradient(135deg,var(--pc),color-mix(in srgb,var(--pc) 70%,#000));color:#fff;transition:transform .15s,filter .2s}
.nlpf-quote:hover{transform:translateY(-2px);filter:brightness(1.05)}
@media(max-width:640px){.nlpf-cta{width:100%}.nlpf-quote{flex:1}}
</style>
<?php
		return ob_get_clean();
	}
}
add_filter( 'the_content', function ( $content ) {
	if ( ! is_singular( 'nadlan_project' ) || ! in_the_loop() || ! is_main_query() ) { return $content; }
	return nadlan_dir_project_profile_header( get_the_ID() ) . $content;
}, 5 );

/* =========================================================================
 * PROJECTS premium directory (v1.36.0  -  the one that was lost from v1.33)
 * ========================================================================= */

if ( ! function_exists( 'nadlan_dir_project_types' ) ) {
	function nadlan_dir_project_types() {
		return array(
			'tama38'      => array( 'label' => 'תמ״א 38',        'color' => '#9F6F54', 'soft' => '#F8F0EA', 'icon' => 'category-project' ),
			'pinui_binui' => array( 'label' => 'פינוי בינוי',     'color' => '#183C3C', 'soft' => '#EFF4F4', 'icon' => 'category-project' ),
			'new_build'   => array( 'label' => 'בנייה חדשה',      'color' => '#334236', 'soft' => '#F1F4EE', 'icon' => 'profession-developer' ),
			'urban'       => array( 'label' => 'התחדשות עירונית', 'color' => '#334236', 'soft' => '#F1F4EE', 'icon' => 'category-project' ),
			'other'       => array( 'label' => 'אחר',             'color' => '#9C7A3C', 'soft' => '#FBF6EE', 'icon' => 'category-project' ),
		);
	}
}
if ( ! function_exists( 'nadlan_dir_pt_meta' ) ) {
	function nadlan_dir_pt_meta( $key ) {
		$a = nadlan_dir_project_types();
		return $a[ $key ] ?? $a['other'];
	}
}

if ( ! function_exists( 'nadlan_dir_project_query' ) ) {
	function nadlan_dir_project_query( $p ) {
		$per = min( 48, max( 6, (int) ( $p['per_page'] ?? 24 ) ) );
		$args = array(
			'post_type' => 'nadlan_project', 'post_status' => 'publish',
			'posts_per_page' => $per, 'paged' => max( 1, (int) ( $p['paged'] ?? 1 ) ),
		);
		$mq = array( 'relation' => 'AND' );
		if ( ! empty( $p['city'] ) ) {
			$mq[] = array( 'key' => 'city', 'value' => nadlan_meta_norm( $p['city'] ), 'compare' => 'LIKE' );
		}
		if ( ! empty( $p['project_type'] ) ) {
			$mq[] = array( 'key' => 'project_type', 'value' => sanitize_key( $p['project_type'] ) );
		}
		if ( ! empty( $p['min_units'] ) ) {
			$mq[] = array( 'key' => 'num_units', 'value' => (int) $p['min_units'], 'type' => 'NUMERIC', 'compare' => '>=' );
		}
		if ( count( $mq ) > 1 ) { $args['meta_query'] = $mq; }
		if ( ! empty( $p['q'] ) ) { $args['s'] = sanitize_text_field( $p['q'] ); }
		switch ( $p['sort'] ?? 'featured' ) {
			case 'units':  $args['meta_key'] = 'num_units'; $args['orderby'] = 'meta_value_num'; $args['order'] = 'DESC'; break;
			case 'newest': $args['orderby'] = 'date'; $args['order'] = 'DESC'; break;
			case 'name':   $args['orderby'] = 'title'; $args['order'] = 'ASC'; break;
			default:       $args = nadlan_dir_use_paid_placement_boost( $args );
		}
		return new WP_Query( $args );
	}
}

if ( ! function_exists( 'nadlan_concept_asset_url' ) ) {
	function nadlan_concept_asset_url( $file ) {
		return plugins_url( 'assets/concept/' . ltrim( (string) $file, '/' ), dirname( __DIR__ ) . '/nadlan-config.php' );
	}
}

if ( ! function_exists( 'nadlan_dir_project_card' ) ) {
	function nadlan_dir_project_card( $id ) {
		$pm     = nadlan_dir_pt_meta( (string) get_post_meta( $id, 'project_type', true ) );
		$city   = nadlan_meta_norm( get_post_meta( $id, 'city', true ) );
		$units  = (int) get_post_meta( $id, 'num_units', true );
		$status = nadlan_meta_norm( get_post_meta( $id, 'project_status', true ) );
		$dev    = nadlan_meta_norm( get_post_meta( $id, 'developer_name', true ) );
		$tier   = (string) get_post_meta( $id, 'paid_tier', true );
		$distance = apply_filters( 'nadlan_geo_card_distance', null, $id );
		$featured = in_array( $tier, array( 'pro', 'premier' ), true );

		// owner-uploaded photo wins; otherwise we render an original architectural
		// concept SVG (no stock photo, no faces). Alternate skyline vs tower by ID
		// for visual variety across the grid.
		$photo_url = '';
		if ( has_post_thumbnail( $id ) ) {
			$photo_url = get_the_post_thumbnail_url( $id, 'medium_large' );
		} else {
			$photos = array_filter( array_map( 'trim', explode( ',', (string) get_post_meta( $id, 'photos_csv', true ) ) ) );
			foreach ( $photos as $p ) {
				if ( preg_match( '~^https?://~i', $p ) ) { $photo_url = $p; break; }
			}
		}
		$is_real_photo = $photo_url !== '';
		if ( ! $is_real_photo ) {
			// Rotate 5 real architectural photos from the theme (luxurious, varied)
			// rather than 2 dark concept SVGs so the catalog grid never reads as
			// identical empty blocks. Falls back to the bundled concept SVG if the
			// theme is not present (defensive).
			$theme_fallbacks = array(
				'tel-aviv-coast-skyline.jpg',
				'sea-view-interior.jpg',
				'tel-aviv-skyline-blueprint.jpg',
				'architectural-model.jpg',
				'blueprint-desk.jpg',
			);
			$pick = $theme_fallbacks[ absint( $id ) % count( $theme_fallbacks ) ];
			$theme_path = function_exists( 'get_theme_file_path' )
				? get_theme_file_path( 'assets/premium-site/' . $pick ) : '';
			if ( $theme_path && file_exists( $theme_path ) ) {
				$photo_url = get_theme_file_uri( 'assets/premium-site/' . $pick );
			} else {
				$concept_files = array( 'skyline-telaviv-line.svg', 'project-concept.svg' );
				$photo_url = nadlan_concept_asset_url( $concept_files[ absint( $id ) % count( $concept_files ) ] );
			}
		}
		ob_start(); ?>
<a class="nldc has-media<?php echo $featured ? ' is-featured' : ''; ?>" href="<?php echo esc_url( get_permalink( $id ) ); ?>" style="--pc:<?php echo esc_attr( $pm['color'] ); ?>;--ps:<?php echo esc_attr( $pm['soft'] ); ?>">
	<?php if ( $featured ) : ?><span class="nldc-sponsor">מקודם</span><?php endif; ?>
	<div class="nldc-media<?php echo $is_real_photo ? ' has-real-photo' : ' has-concept-art'; ?>">
		<img src="<?php echo esc_url( $photo_url ); ?>" alt="" loading="lazy" decoding="async">
		<span class="nldc-media-label"><?php echo esc_html( $pm['label'] ); ?></span>
	</div>
	<div class="nldc-top">
		<span class="nldc-av" aria-hidden="true"><svg class="nl-mark" viewBox="0 0 48 48"><use href="#<?php echo esc_attr( $pm['icon'] ); ?>"></use></svg></span>
		<div class="nldc-id">
			<h3 class="nldc-name"><?php echo esc_html( get_the_title( $id ) ); ?></h3>
			<span class="nldc-pill"><?php echo esc_html( $pm['label'] ); ?></span>
		</div>
	</div>
	<div class="nldc-meta">
		<?php if ( $city ) : ?><span class="nldc-city"><svg class="nl-ico" aria-hidden="true" viewBox="0 0 16 16"><path fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" d="M8 14s5-4.5 5-8.5A5 5 0 1 0 3 5.5C3 9.5 8 14 8 14z"/><circle cx="8" cy="5.5" r="1.8" fill="none" stroke="currentColor" stroke-width="1.4"/></svg><?php echo esc_html( $city ); ?></span><?php endif; ?>
		<?php if ( $distance !== null && $distance !== '' ) : ?><span class="nldc-distance"><?php echo esc_html( number_format_i18n( (float) $distance, 1 ) ); ?> ק״מ</span><?php endif; ?>
		<?php if ( $units > 0 ) : ?><span class="nldc-cls"><svg class="nl-ico" aria-hidden="true" viewBox="0 0 16 16"><path fill="none" stroke="currentColor" stroke-width="1.4" stroke-linejoin="round" d="M2 7l6-5 6 5v7H2zM6.5 14v-4h3v4"/></svg><?php echo number_format( $units ); ?> יח״ד<?php echo $status ? ' · ' . esc_html( $status ) : ''; ?></span><?php endif; ?>
		<?php if ( $dev ) : ?><span class="nldc-cls"><svg class="nl-ico" aria-hidden="true" viewBox="0 0 16 16"><circle cx="8" cy="5.5" r="2.5" fill="none" stroke="currentColor" stroke-width="1.4"/><path fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" d="M3 14c.5-2.5 2.5-4 5-4s4.5 1.5 5 4"/></svg><?php echo esc_html( $dev ); ?></span><?php endif; ?>
	</div>
	<div class="nldc-foot">
		<span class="nldc-reg"><svg class="nl-ico" aria-hidden="true" viewBox="0 0 16 16"><path fill="none" stroke="currentColor" stroke-width="1.4" stroke-linejoin="round" d="M8 1.5l5.5 2v4c0 3.5-2.5 6-5.5 7-3-1-5.5-3.5-5.5-7v-4l5.5-2z"/><path fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round" d="M5.5 8l2 2 3-4"/></svg>data.gov.il</span>
		<span class="nldc-go">לפרטים ←</span>
	</div>
</a>
<?php
		return ob_get_clean();
	}
}

if ( ! function_exists( 'nadlan_dir_project_cards_html' ) ) {
	function nadlan_dir_project_cards_html( $wq ) {
		if ( ! $wq->have_posts() ) { return '<div class="nldir-empty"><p>לא נמצאו פרויקטים התואמים.</p><p>נסו עיר אחרת או הסירו סינון.</p></div>'; }
		$out = '';
		foreach ( $wq->posts as $p ) { $out .= nadlan_dir_project_card( $p->ID ); }
		return apply_filters( 'nadlan_dir_cards_html', $out, 'nadlan_project' );
	}
}

if ( ! function_exists( 'nadlan_dir_project_facets' ) ) {
	function nadlan_dir_project_facets() {
		$k = 'nadlan_dir_projfacets_v1';
		$c = get_transient( $k );
		if ( is_array( $c ) ) { return $c; }
		global $wpdb;
		$types  = $wpdb->get_results( "SELECT pm.meta_value v, COUNT(*) n FROM {$wpdb->postmeta} pm INNER JOIN {$wpdb->posts} p ON p.ID=pm.post_id WHERE pm.meta_key='project_type' AND pm.meta_value<>'' AND p.post_type='nadlan_project' AND p.post_status='publish' GROUP BY pm.meta_value", ARRAY_A );
		$cities = $wpdb->get_results( "SELECT pm.meta_value v, COUNT(*) n FROM {$wpdb->postmeta} pm INNER JOIN {$wpdb->posts} p ON p.ID=pm.post_id WHERE pm.meta_key='city' AND pm.meta_value<>'' AND p.post_type='nadlan_project' AND p.post_status='publish' GROUP BY pm.meta_value ORDER BY n DESC LIMIT 18", ARRAY_A );
		$out = array( 'types' => array(), 'cities' => array(), 'total' => (int) wp_count_posts( 'nadlan_project' )->publish );
		foreach ( (array) $types as $r )  { $out['types'][ $r['v'] ] = (int) $r['n']; }
		foreach ( (array) $cities as $r ) { $out['cities'][] = array( 'name' => nadlan_meta_norm( $r['v'] ), 'n' => (int) $r['n'] ); }
		set_transient( $k, $out, HOUR_IN_SECONDS );
		return $out;
	}
}
add_action( 'save_post_nadlan_project', function () { delete_transient( 'nadlan_dir_projfacets_v1' ); } );

add_action( 'rest_api_init', function () {
	register_rest_route( 'nadlan/v1', '/projects', array(
		'methods' => 'GET', 'permission_callback' => '__return_true',
		'callback' => function ( $req ) {
			$p = array(
				'q' => (string) $req->get_param( 'q' ),
				'city' => (string) $req->get_param( 'city' ),
				'project_type' => (string) $req->get_param( 'project_type' ),
				'min_units' => (int) $req->get_param( 'min_units' ),
				'sort' => (string) $req->get_param( 'sort' ),
				'paged' => (int) $req->get_param( 'paged' ),
				'per_page' => (int) $req->get_param( 'per_page' ),
			);
			$wq = nadlan_dir_project_query( $p );
			$out = array( 'ok' => true, 'html' => nadlan_dir_project_cards_html( $wq ), 'total' => (int) $wq->found_posts, 'pages' => (int) $wq->max_num_pages, 'paged' => max( 1, $p['paged'] ) );
			wp_reset_postdata();
			return $out;
		},
	) );
} );

add_filter( 'get_the_archive_title', function ( $t ) {
	if ( is_post_type_archive( 'nadlan_project' ) )  { return 'פרויקטים והתחדשות עירונית'; }
	if ( is_post_type_archive( 'nadlan_property' ) ) { return 'דירות ונכסים'; }
	return $t;
} );
add_filter( 'pre_get_document_title', function ( $t ) {
	if ( is_post_type_archive( 'nadlan_project' ) ) {
		return 'פרויקטים חדשים והתחדשות עירונית | תמ״א 38, פינוי בינוי | נדל״ן חכם';
	}
	return $t;
}, 20 );

if ( ! function_exists( 'nadlan_dir_archive_viewport_meta' ) ) {
	function nadlan_dir_archive_viewport_meta() {
		if ( ! is_post_type_archive( array( 'nadlan_project', 'nadlan_property', 'nadlan_professional' ) ) ) {
			return;
		}
		echo "\n<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">\n";
	}
}
add_action( 'wp_head', 'nadlan_dir_archive_viewport_meta', 0 );

add_action( 'template_redirect', function () {
	if ( is_admin() || ! is_post_type_archive( 'nadlan_project' ) ) { return; }
	if ( defined( 'NADLAN_DISABLE_DIRECTORY' ) && NADLAN_DISABLE_DIRECTORY ) { return; }
	nadlan_dir_project_page();
	exit;
}, 5 );

if ( ! function_exists( 'nadlan_dir_project_page' ) ) {
	function nadlan_dir_project_page() {
		$facets = nadlan_dir_project_facets();
		$types  = nadlan_dir_project_types();
		$state  = array(
			'q' => isset( $_GET['q'] ) ? sanitize_text_field( wp_unslash( $_GET['q'] ) ) : '',
			'city' => isset( $_GET['city'] ) ? sanitize_text_field( wp_unslash( $_GET['city'] ) ) : '',
			'project_type' => isset( $_GET['project_type'] ) ? sanitize_key( $_GET['project_type'] ) : '',
			'min_units' => isset( $_GET['min_units'] ) ? (int) $_GET['min_units'] : 0,
			'sort' => isset( $_GET['sort'] ) ? sanitize_key( $_GET['sort'] ) : 'featured',
			'paged' => max( 1, (int) ( $_GET['paged'] ?? 1 ) ),
			'per_page' => 24,
		);
		$wq = nadlan_dir_project_query( $state );
		$total = (int) $wq->found_posts;
		$cards = nadlan_dir_project_cards_html( $wq );
		wp_reset_postdata();

		get_header();
		if ( function_exists( 'block_template_part' ) ) { block_template_part( 'header' ); }
		echo nadlan_dir_css();
		?>
<div class="nldir" dir="rtl" data-mode="projects"
	data-rest="<?php echo esc_url( rest_url( 'nadlan/v1/projects' ) ); ?>"
	data-state="<?php echo esc_attr( wp_json_encode( $state ) ); ?>">
	<header class="nldir-hero">
		<nav class="nldir-crumbs"><a href="<?php echo esc_url( home_url( '/' ) ); ?>">בית</a> › <span>פרויקטים</span></nav>
		<h1>פרויקטים והתחדשות עירונית</h1>
		<p class="nldir-lead"><strong><?php echo number_format( $facets['total'] ); ?></strong> פרויקטים: תמ״א 38, פינוי בינוי ובנייה חדשה, ממאגר התחדשות עירונית הרשמי.</p>
		<form class="nldir-search" role="search">
			<input type="search" name="q" value="<?php echo esc_attr( $state['q'] ); ?>" placeholder="חיפוש לפי שם פרויקט או יזם" autocomplete="off">
			<input type="text" name="city" value="<?php echo esc_attr( $state['city'] ); ?>" placeholder="עיר" autocomplete="off">
			<button type="submit">חיפוש</button>
		</form>
		<div class="nldir-pills">
			<button type="button" class="nldir-pill<?php echo $state['project_type'] === '' ? ' is-on' : ''; ?>" data-prof="">הכל</button>
			<?php foreach ( $types as $key => $pm ) :
				$n = $facets['types'][ $key ] ?? 0;
				if ( $n < 1 ) { continue; } ?>
			<button type="button" class="nldir-pill<?php echo $state['project_type'] === $key ? ' is-on' : ''; ?>"
				data-prof="<?php echo esc_attr( $key ); ?>" style="--pc:<?php echo esc_attr( $pm['color'] ); ?>;--ps:<?php echo esc_attr( $pm['soft'] ); ?>">
				<span class="nldir-pill-mark" aria-hidden="true"><svg viewBox="0 0 48 48"><use href="#<?php echo esc_attr( $pm['icon'] ); ?>"></use></svg></span><?php echo esc_html( $pm['label'] ); ?> <i><?php echo number_format( $n ); ?></i>
			</button>
			<?php endforeach; ?>
		</div>
	</header>
	<div class="nldir-body">
		<aside class="nldir-side">
			<div class="nldir-fgroup"><h4>ערים מובילות</h4>
				<ul class="nldir-cities">
					<?php foreach ( array_slice( $facets['cities'], 0, 12 ) as $c ) : ?>
					<li><button type="button" class="nldir-cityb" data-city="<?php echo esc_attr( $c['name'] ); ?>"><?php echo esc_html( $c['name'] ); ?> <i><?php echo number_format( $c['n'] ); ?></i></button></li>
					<?php endforeach; ?>
				</ul>
			</div>
		</aside>
		<main class="nldir-main">
			<div class="nldir-bar">
				<div class="nldir-count"><strong id="nldir-total"><?php echo number_format( $total ); ?></strong> פרויקטים</div>
				<div class="nldir-chips" id="nldir-chips"></div>
				<label class="nldir-sortw">מיון:
					<select id="nldir-sort">
						<option value="featured"<?php selected( $state['sort'], 'featured' ); ?>>מומלצים</option>
						<option value="units"<?php selected( $state['sort'], 'units' ); ?>>הכי הרבה יח״ד</option>
						<option value="newest"<?php selected( $state['sort'], 'newest' ); ?>>חדש</option>
						<option value="name"<?php selected( $state['sort'], 'name' ); ?>>א׳–ת׳</option>
					</select>
				</label>
			</div>
			<div class="nldir-results" id="nldir-results"><?php echo $cards; ?></div>
			<div class="nldir-more-wrap"><button type="button" class="nldir-more" id="nldir-more"<?php echo $wq->max_num_pages > 1 ? '' : ' style="display:none"'; ?>>הצגת עוד</button></div>
		</main>
	</div>
</div>
<?php echo nadlan_dir_js(); ?>
		<?php
		// Block theme footer: get_footer() is a noop when there's no footer.php,
		// so explicitly render the theme's footer template part first.
		if ( function_exists( 'block_template_part' ) ) { block_template_part( 'footer' ); }
		get_footer();
	}
}

require __DIR__ . '/directory-assets.php';
