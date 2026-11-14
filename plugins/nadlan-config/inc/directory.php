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

/* get_header() on this block theme falls back to WP's theme-compat header,
 * which prints the site name as an <h1> - a second h1 on archive templates
 * that already print their own. Demote the compat h1 to a <p> (same markup
 * position, no visual change). Fails open: pattern absent => output as-is. */
if ( ! function_exists( 'nadlan_dir_header_single_h1' ) ) {
	function nadlan_dir_header_single_h1() {
		ob_start();
		get_header();
		$html  = ob_get_clean();
		$fixed = preg_replace( '#(<div id="headerimg">\s*)<h1>(<a[^>]*>.*?</a>)</h1>#su', '$1<p class="nl-compat-brand">$2</p>', $html, 1 );
		if ( null !== $fixed ) {
			/* the compat header is plain unstyled text above the real block header - hide it */
			$fixed = str_replace( '<div id="header" ', '<div id="header" style="display:none" ', $fixed );
			$fixed = str_replace( '<div id="header">', '<div id="header" style="display:none">', $fixed );
			/* ...and the compat <hr /> right after it, which drew a stray line and an empty strip above the site header (24.9.2026) */
			$hr_off = preg_replace( '#(<div id="header" style="display:none"[^>]*>.*?</div>\s*</div>\s*)<hr\s*/?>#su', '$1', $fixed, 1 );
			if ( null !== $hr_off ) { $fixed = $hr_off; }
		}
		echo null !== $fixed ? $fixed : $html;
	}
}

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
if ( ! function_exists( 'nadlan_dir_prof_plural' ) ) {
	/** The filter pills speak in the plural (design system ProfessionalCard v41): "קבלנים 2,699", not "קבלן 2,699". */
	function nadlan_dir_prof_plural( $key, $label ) {
		$pl = array( 'kablan' => 'קבלנים', 'shamai' => 'שמאי מקרקעין', 'bedek_bait' => 'בודקי בית', 'mashkanta' => 'יועצי משכנתאות', 'architect' => 'אדריכלים', 'lawyer' => 'עורכי דין מקרקעין', 'mefakeach' => 'מפקחי בנייה', 'metavech' => 'מתווכים' );
		return isset( $pl[ $key ] ) ? $pl[ $key ] : $label;
	}
}
if ( ! function_exists( 'nadlan_dir_professions_all' ) ) {
	function nadlan_dir_professions_all() {
		$all = nadlan_dir_professions();
		if ( function_exists( 'nadlan_prof_extra_professions' ) ) { $all = array_merge( $all, nadlan_prof_extra_professions() ); }
		return $all;
	}
}
if ( ! function_exists( 'nadlan_dir_prof_meta' ) ) {
	function nadlan_dir_prof_meta( $key ) {
		// FULL map incl. extras (interior_designer, engineer...) - the base-only
		// lookup leaked raw machine enums onto buyer-facing cards (audit 2026-07-06).
		$all = nadlan_dir_professions_all();
		if ( isset( $all[ $key ] ) ) { return $all[ $key ]; }
		// every profession of a home (pro-network.php): a key the directory lists do not know still gets its Hebrew label
		if ( function_exists( 'nadlan_pro_registry' ) ) {
			$reg = nadlan_pro_registry();
			if ( isset( $reg[ $key ] ) ) { return array( 'label' => $reg[ $key ]['label'], 'color' => '#2F6F86', 'soft' => '#EEF4F6', 'icon' => 'profession-contractor' ); }
		}
		// never print a machine token; a Hebrew free-text value may pass through
		$label = ( $key !== '' && ! preg_match( '/^[a-z0-9_\-]+$/', $key ) ) ? $key : 'בעל/ת מקצוע';
		return array( 'label' => $label, 'color' => '#9C7A3C', 'soft' => '#FBF6EE', 'icon' => 'profession-broker' );
	}
}

if ( ! function_exists( 'nadlan_dir_prof_label' ) ) {
	/** The profession label in the card holder's grammatical gender (meta nl_gender: f|m), when the card states it (HAD-249). */
	function nadlan_dir_prof_label( $key, $id = 0 ) {
		$key = (string) $key;
		$pm  = nadlan_dir_prof_meta( $key );
		$g   = $id ? (string) get_post_meta( (int) $id, 'nl_gender', true ) : '';
		// the brokers register gives no gender: a card imported from it names the field, not the person (24.9.2026)
		if ( 'metavech' === $key && 'f' !== $g && 'm' !== $g ) { return 'תיווך נדל״ן'; }
		if ( 'f' !== $g && 'm' !== $g ) { return $pm['label']; }
		$forms = array(
			'metavech'          => array( 'm' => 'מתווך', 'f' => 'מתווכת' ),
			'shamai'            => array( 'm' => 'שמאי מקרקעין', 'f' => 'שמאית מקרקעין' ),
			'mashkanta'         => array( 'm' => 'יועץ משכנתאות', 'f' => 'יועצת משכנתאות' ),
			'architect'         => array( 'm' => 'אדריכל', 'f' => 'אדריכלית' ),
			'mefakeach'         => array( 'm' => 'מפקח בנייה', 'f' => 'מפקחת בנייה' ),
			'kablan'            => array( 'm' => 'קבלן', 'f' => 'קבלנית' ),
			'interior_designer' => array( 'm' => 'מעצב פנים', 'f' => 'מעצבת פנים' ),
			'engineer'          => array( 'm' => 'מהנדס בניין', 'f' => 'מהנדסת בניין' ),
			'surveyor'          => array( 'm' => 'מודד מוסמך', 'f' => 'מודדת מוסמכת' ),
			'urban_planner'     => array( 'm' => 'מתכנן ערים', 'f' => 'מתכננת ערים' ),
		);
		if ( isset( $forms[ $key ][ $g ] ) ) { return $forms[ $key ][ $g ]; }
		if ( function_exists( 'nadlan_pro_registry' ) ) {
			$reg = nadlan_pro_registry();
			if ( isset( $reg[ $key ] ) ) { return 'f' === $g ? $reg[ $key ]['female'] : $reg[ $key ]['label']; }
		}
		return $pm['label'];
	}
}

if ( ! function_exists( 'nadlan_dir_registry_sources' ) ) {
	/** Card sources that ARE an official register: a card imported from one is verified by where it came from. */
	function nadlan_dir_registry_sources() {
		return (array) apply_filters( 'nadlan_dir_registry_sources', array( 'pinkas_hakablanim', 'metavhim' ) );
	}
}

if ( ! function_exists( 'nadlan_dir_registry_verified' ) ) {
	/** "Verified in the register" = a recorded check (verified_at) or an official-register source. A filled field alone is not a check (HAD-249). */
	function nadlan_dir_registry_verified( $id ) {
		return (int) get_post_meta( (int) $id, 'verified_at', true ) > 0
			|| in_array( (string) get_post_meta( (int) $id, 'source', true ), nadlan_dir_registry_sources(), true );
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

if ( ! function_exists( 'nadlan_dir_own_project_slugs' ) ) {
	/** The projects we present ourselves, in the order they lead the catalog: every project with our own stage and 3D page
	 *  (read from the stage config, so a new one joins by itself), then the flagship pages that are built differently. */
	function nadlan_dir_own_project_slugs() {
		$lead  = array( 'rainbow-tel-aviv', 'duo-tel-aviv', 'ashira-sde-dov', 'dimri-yama-sde-dov', 'h-infinity-somail-tel-aviv', 'hamedina', 'einstein-tower' );
		$stage = function_exists( 'nadlan_ps_config' ) ? array_keys( (array) nadlan_ps_config() ) : array();
		$out   = array();
		foreach ( array_merge( $lead, $stage ) as $s ) { $s = sanitize_title( (string) $s ); if ( '' !== $s && ! in_array( $s, $out, true ) ) { $out[] = $s; } }
		return (array) apply_filters( 'nadlan_dir_own_project_slugs', $out );
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
		$paid = "CASE {$alias}.meta_value WHEN 'premier' THEN 2 WHEN 'pro' THEN 1 ELSE 0 END DESC";
		if ( 'nadlan_project' === $query->get( 'post_type' ) ) {
			/* HAD-689 (Ben, 10.11.2026: "הפרויקטים שלנו, התלת מימד שלנו, הפרויקטים החזקים שלנו... הם בעדיפות", and the results open
			 * with pictures). After the paid tiers the projects catalog now puts: the projects we present ourselves (our own stage and
			 * 3D pages), then projects that have a picture of their own, then Tel Aviv, then the newest. Before this the order was by
			 * date alone, so the renewal compounds added last pushed Ashira, Dimri Yama, H Infinity and Einstein to the third page. */
			$own = function_exists( 'nadlan_dir_own_project_slugs' ) ? nadlan_dir_own_project_slugs() : array();
			$own_sql = '';
			if ( $own ) {
				$in = "'" . implode( "','", array_map( 'esc_sql', $own ) ) . "'";
				$own_sql = "CASE WHEN FIELD({$wpdb->posts}.post_name,{$in}) = 0 THEN 9999 ELSE FIELD({$wpdb->posts}.post_name,{$in}) END ASC, ";
			}
			foreach ( array( 'nadlan_thumb_pm' => '_thumbnail_id', 'nadlan_city_pm' => 'city' ) as $a => $k ) {
				if ( strpos( $clauses['join'], " AS {$a} " ) === false ) {
					$clauses['join'] .= $wpdb->prepare( " LEFT JOIN {$wpdb->postmeta} AS {$a} ON ({$wpdb->posts}.ID = {$a}.post_id AND {$a}.meta_key = %s)", $k );
				}
			}
			$clauses['orderby'] = $paid . ', ' . $own_sql
				. "CASE WHEN COALESCE(nadlan_thumb_pm.meta_value,'') IN ('','0') THEN 1 ELSE 0 END ASC, "
				. "CASE WHEN nadlan_city_pm.meta_value LIKE 'תל אביב%' THEN 0 ELSE 1 END ASC, "
				. "{$wpdb->posts}.menu_order ASC, {$wpdb->posts}.post_date DESC, {$wpdb->posts}.ID DESC";
			return $clauses;
		}
		$clauses['orderby'] = $paid . ", {$wpdb->posts}.menu_order ASC, {$wpdb->posts}.post_date DESC, {$wpdb->posts}.ID DESC";
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
	function nadlan_dir_card( $id, $args = array() ) {
		// $args['foot']: extra HTML under the trust labels (v99: the recommendations count on /brokers/, a quality on /firgun/)
		// design system ProCard v98 (28.9.2026): a card of the professionals' network - a cover with the profession's
		// architectural pattern, a portrait or a designed monogram, the strongest register fact, separate trust labels and
		// two actions (open the profile, save). The facts and labels come from inc/pro-card.php; nothing is invented.
		$prof_key = (string) get_post_meta( $id, 'profession', true );
		$pm       = nadlan_dir_prof_meta( $prof_key );
		$city     = nadlan_meta_norm( get_post_meta( $id, 'city', true ) );
		$tier     = (string) get_post_meta( $id, 'paid_tier', true );
		$distance = apply_filters( 'nadlan_geo_card_distance', null, $id );
		$rating   = (float) get_post_meta( $id, 'rating', true );
		$reviews  = (int) get_post_meta( $id, 'reviews_count', true );
		$title    = trim( wp_strip_all_tags( get_the_title( $id ) ) );
		$url      = get_permalink( $id );
		$verified = 'verified' === (string) get_post_meta( $id, 'claim_status', true );
		$is_demo  = (bool) get_post_meta( $id, 'is_demo', true ); // a showcase of the paid profile (v43): it says so
		$featured = in_array( $tier, array( 'pro', 'premier' ), true );
		$src      = (string) get_post_meta( $id, 'source', true );

		$parts = preg_split( '/\s+·\s+/u', $title, 2 );
		$pname = $parts[0];
		$biz   = isset( $parts[1] ) ? $parts[1] : nadlan_meta_norm( get_post_meta( $id, 'company_name', true ) );
		if ( $biz === $pname ) { $biz = ''; } // the register repeats a private person's name as the business
		$photo = has_post_thumbnail( $id ) ? get_the_post_thumbnail( $id, 'thumbnail', array( 'alt' => '', 'loading' => 'lazy', 'decoding' => 'async' ) ) : '';
		$role  = nadlan_dir_prof_label( $prof_key, $id ) . ( $city ? ' · ' . $city : '' )
			. ( null !== $distance && '' !== $distance ? ' · ' . number_format_i18n( (float) $distance, 1 ) . ' ק״מ' : '' );
		// a showcase card (is_demo) carries seeded numbers: it shows the design, never a figure
		$fact  = ( ! $is_demo && function_exists( 'nadlan_pc_fact' ) ) ? nadlan_pc_fact( $id, $prof_key ) : null;
		$trust = function_exists( 'nadlan_pc_trust' ) ? nadlan_pc_trust( $id, $prof_key ) : array();
		if ( $is_demo ) {
			$state = '<span class="nlpn-state is-demo"><i></i>פרופיל לדוגמה</span>';
		} elseif ( $verified ) {
			$state = '<span class="nlpn-state is-live"><i></i>פרופיל פעיל</span>';
		} elseif ( in_array( $src, array( 'pinkas_hakablanim', 'metavhim' ), true ) ) {
			$state = '<span class="nlpn-state"><i></i>מהפנקס הרשמי</span>';
		} else {
			$state = '';
		}
		// stars only from real, verified reviews (the seeded demo ratings are not shown on the network's cards)
		$stars = ( $reviews > 0 && $rating > 0 && get_post_meta( $id, 'reviews_verified', true ) )
			? '<p class="nlpn-rate"><b>★ ' . esc_html( number_format( $rating, 1 ) ) . '</b> · ' . (int) $reviews . ' חוות דעת</p>' : '';
		$mark = '<svg class="nl-mark" viewBox="0 0 48 48"><use href="#' . esc_attr( $pm['icon'] ) . '"></use></svg>';
		ob_start(); ?>
<article class="nlpn<?php echo $featured ? ' is-featured' : ''; ?><?php echo $is_demo ? ' is-demo' : ''; ?>" style="--pc:<?php echo esc_attr( $pm['color'] ); ?>;--ps:<?php echo esc_attr( $pm['soft'] ); ?>">
	<div class="nlpn-cover" aria-hidden="true"><?php echo $state; // phpcs:ignore ?><span class="nlpn-emb"><?php echo $mark; // phpcs:ignore ?></span></div>
	<div class="nlpn-av" aria-hidden="true"><?php echo $photo ? $photo : '<span class="nlpn-mono">' . esc_html( nadlan_pc_mono( $pname ) ) . '</span>'; // phpcs:ignore ?><i class="nlpn-mk"><?php echo $mark; // phpcs:ignore ?></i></div>
	<div class="nlpn-body">
		<h3 class="nlpn-name"><a href="<?php echo esc_url( $url ); ?>"><?php echo esc_html( $pname ); ?></a></h3>
		<?php if ( '' !== $biz ) : ?><p class="nlpn-biz"><?php echo esc_html( $biz ); ?></p><?php endif; ?>
		<p class="nlpn-role"><?php echo esc_html( $role ); ?></p>
		<?php if ( $fact ) : ?><p class="nlpn-fact"><small><?php echo esc_html( $fact[0] ); ?></small><?php echo esc_html( $fact[1] ); ?></p><?php endif; ?>
		<?php if ( $trust ) : ?><ul class="nlpn-trust"><?php foreach ( $trust as $t ) : ?><li<?php echo $t[1] ? ' class="' . esc_attr( $t[1] ) . '"' : ''; ?>><?php echo wp_kses( $t[0], array( 'b' => array() ) ); ?></li><?php endforeach; ?></ul><?php endif; ?>
		<?php echo $stars; // phpcs:ignore ?>
		<?php if ( ! empty( $args['foot'] ) ) : ?><div class="nlpn-foot"><?php echo $args['foot']; // phpcs:ignore -- built from escaped parts by the caller ?></div><?php endif; ?>
		<div class="nlpn-act">
			<a class="nlpn-go" href="<?php echo esc_url( $url ); ?>" tabindex="-1" aria-hidden="true">לפרופיל</a>
			<button type="button" class="nlpn-save" aria-pressed="false" aria-label="שמירה" data-id="<?php echo (int) $id; ?>" data-name="<?php echo esc_attr( $pname ); ?>" data-url="<?php echo esc_url( $url ); ?>" data-role="<?php echo esc_attr( $role ); ?>"><?php echo nadlan_pc_save_icon(); // phpcs:ignore ?></button>
			<?php if ( $featured ) : ?><span class="nlpn-ad">מקודם</span><?php endif; ?>
		</div>
	</div>
</article>
		<?php
		return ( function_exists( 'nadlan_pc_assets' ) ? nadlan_pc_assets() : '' ) . ob_get_clean();
	}
}

/* render N cards from a WP_Query into a string */
if ( ! function_exists( 'nadlan_dir_cards_html' ) ) {
	function nadlan_dir_cards_html( $wq ) {
		if ( ! $wq->have_posts() ) {
			return '<div class="nldir-empty"><p>לא נמצאו בעלי מקצוע התואמים את החיפוש.</p><p>נסו עיר אחרת או הסירו סינון.</p></div>';
		}
		$out = '';
		// the real professionals first, the demo showcases after them (design system ProfessionalCard v43)
		$real = array(); $demo = array();
		foreach ( $wq->posts as $p ) { if ( get_post_meta( $p->ID, 'is_demo', true ) ) { $demo[] = $p; } else { $real[] = $p; } }
		foreach ( array_merge( $real, $demo ) as $p ) { $out .= nadlan_dir_card( $p->ID ); }
		return apply_filters( 'nadlan_dir_cards_html', $out, 'nadlan_professional' );
	}
}

/* ---------------------------------------------------------------------------
 * Facet counts (cached)  -  profession counts + top cities
 * ------------------------------------------------------------------------- */
if ( ! function_exists( 'nadlan_dir_facet_counts' ) ) {
	function nadlan_dir_facet_counts() {
		$k = 'nadlan_dir_facets_v2'; // v2 (28.9.2026): demo showcases are not counted as professionals (design system v43)
		$c = get_transient( $k );
		if ( is_array( $c ) ) { return $c; }
		global $wpdb;
		$nodemo = "NOT EXISTS (SELECT 1 FROM {$wpdb->postmeta} d WHERE d.post_id=p.ID AND d.meta_key='is_demo' AND d.meta_value IN ('1','true'))";
		$prof = $wpdb->get_results(
			"SELECT pm.meta_value v, COUNT(*) n FROM {$wpdb->postmeta} pm
			 INNER JOIN {$wpdb->posts} p ON p.ID=pm.post_id
			 WHERE pm.meta_key='profession' AND pm.meta_value<>'' AND p.post_type='nadlan_professional' AND p.post_status='publish' AND $nodemo
			 GROUP BY pm.meta_value", ARRAY_A );
		$cities = $wpdb->get_results(
			"SELECT pm.meta_value v, COUNT(*) n FROM {$wpdb->postmeta} pm
			 INNER JOIN {$wpdb->posts} p ON p.ID=pm.post_id
			 WHERE pm.meta_key='city' AND pm.meta_value<>'' AND p.post_type='nadlan_professional' AND p.post_status='publish' AND $nodemo
			 GROUP BY pm.meta_value ORDER BY n DESC LIMIT 24", ARRAY_A );
		$out = array(
			'professions' => array(),
			'cities'      => array(),
			'total'       => (int) $wpdb->get_var( "SELECT COUNT(*) FROM {$wpdb->posts} p WHERE p.post_type='nadlan_professional' AND p.post_status='publish' AND $nodemo" ),
		);
		foreach ( (array) $prof as $r )   { $out['professions'][ $r['v'] ] = (int) $r['n']; }
		foreach ( (array) $cities as $r ) { $out['cities'][] = array( 'name' => nadlan_meta_norm( $r['v'] ), 'n' => (int) $r['n'] ); }
		set_transient( $k, $out, HOUR_IN_SECONDS );
		return $out;
	}
}
add_action( 'save_post_nadlan_professional', function () { delete_transient( 'nadlan_dir_facets_v2' ); delete_transient( 'nadlan_dir_sources_v1' ); } );

/* ---------------------------------------------------------------------------
 * The directory headline says only what the sources say (HAD-249, 24.9.2026):
 * contractors imported from the contractors register, brokers whose licence was
 * checked in the brokers register. Sample cards are not counted as professionals.
 * ------------------------------------------------------------------------- */
if ( ! function_exists( 'nadlan_dir_source_counts' ) ) {
	function nadlan_dir_source_counts() {
		$k = 'nadlan_dir_sources_v1';
		$c = get_transient( $k );
		if ( is_array( $c ) ) { return $c; }
		global $wpdb;
		$p   = $wpdb->posts;
		$pm  = $wpdb->postmeta;
		$reg = array_map( 'esc_sql', nadlan_dir_registry_sources() );
		$in  = "'" . implode( "','", $reg ) . "'";
		$demo = "NOT EXISTS (SELECT 1 FROM $pm d WHERE d.post_id=x.ID AND d.meta_key='is_demo' AND d.meta_value IN ('1','true'))";
		$real = (int) $wpdb->get_var( "SELECT COUNT(*) FROM $p x WHERE x.post_type='nadlan_professional' AND x.post_status='publish' AND $demo" );
		$contractors = (int) $wpdb->get_var( "SELECT COUNT(*) FROM $p x JOIN $pm s ON s.post_id=x.ID AND s.meta_key='source' AND s.meta_value='pinkas_hakablanim' WHERE x.post_type='nadlan_professional' AND x.post_status='publish' AND $demo" );
		$brokers = $wpdb->get_col( "SELECT COALESCE(g.meta_value,'') FROM $p x
			JOIN $pm f ON f.post_id=x.ID AND f.meta_key='profession' AND f.meta_value='metavech'
			LEFT JOIN $pm v ON v.post_id=x.ID AND v.meta_key='verified_at'
			LEFT JOIN $pm s ON s.post_id=x.ID AND s.meta_key='source'
			LEFT JOIN $pm g ON g.post_id=x.ID AND g.meta_key='nl_gender'
			WHERE x.post_type='nadlan_professional' AND x.post_status='publish' AND $demo
			AND ( v.meta_value+0 > 0 OR s.meta_value IN ($in) )" );
		$c = array( 'real' => $real, 'contractors' => $contractors, 'brokers' => count( $brokers ), 'broker_gender' => 1 === count( $brokers ) ? (string) $brokers[0] : '' );
		set_transient( $k, $c, HOUR_IN_SECONDS );
		return $c;
	}
}
$nadlan_dir_sources_flush = function ( $meta_id, $object_id, $meta_key ) {
	if ( in_array( $meta_key, array( 'verified_at', 'source', 'profession', 'nl_gender', 'is_demo' ), true ) && 'nadlan_professional' === get_post_type( $object_id ) ) {
		delete_transient( 'nadlan_dir_sources_v1' );
	}
};
add_action( 'added_post_meta', $nadlan_dir_sources_flush, 10, 3 );
add_action( 'updated_post_meta', $nadlan_dir_sources_flush, 10, 3 );
unset( $nadlan_dir_sources_flush );

if ( ! function_exists( 'nadlan_dir_sources_lead' ) ) {
	function nadlan_dir_sources_lead() {
		$c = nadlan_dir_source_counts();
		$n = function ( $v ) { return '<strong>' . esc_html( number_format( (int) $v ) ) . '</strong>'; };
		$parts = array();
		if ( $c['contractors'] > 0 ) {
			$parts[] = $n( $c['contractors'] ) . ' קבלנים רשומים מפנקס הקבלנים (gov.il)';
		}
		if ( $c['brokers'] > 0 ) {
			$who = 1 === (int) $c['brokers'] ? ( 'f' === $c['broker_gender'] ? 'מתווכת אחת' : 'מתווך אחד' ) : $n( $c['brokers'] ) . ' מתווכים';
			$parts[] = $who . ' עם רישיון שנבדק בפנקס המתווכים של משרד המשפטים';
		}
		if ( ! $parts ) { return 'בעלי מקצוע לנדל״ן, לפי עיר והתמחות.'; }
		$last = array_pop( $parts );
		if ( $parts ) {
			$last = ( 1 === (int) $c['brokers'] ? 'ו' : 'ו-' ) . $last;
			$list = implode( ', ', $parts ) . ' ' . $last;
		} else {
			$list = $last;
		}
		// no grand total here: the results bar counts every published card (sample cards too, HAD-248), and two different totals read as a contradiction
		return 'במאגר ' . $list . '.';
	}
}

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
/* Professionals archive had no meta description. */
add_filter( 'wpseo_metadesc', function ( $desc ) {
	if ( ! is_post_type_archive( 'nadlan_professional' ) || $desc ) { return $desc; }
	return 'מאגר בעלי מקצוע לנדל"ן בישראל: קבלנים רשומים מפנקס gov.il, מתווכים, שמאים, עורכי דין, יועצי משכנתאות, בדק בית ומעצבים. חיפוש לפי עיר והתמחות ויצירת קשר ישירה.';
}, 25 );
add_filter( 'pre_get_document_title', function ( $t ) {
	if ( is_post_type_archive( 'nadlan_professional' ) ) {
		return 'מאגר בעלי מקצוע בנדל״ן: קבלנים, מתווכים, שמאים ויועצים | נדלן';
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

		nadlan_dir_header_single_h1();
		if ( function_exists( 'block_template_part' ) ) { block_template_part( 'header' ); }
		echo nadlan_dir_css();
		?>
<div class="nldir" dir="rtl"
	data-rest="<?php echo esc_url( rest_url( 'nadlan/v1/directory' ) ); ?>"
	data-state="<?php echo esc_attr( wp_json_encode( $state ) ); ?>">

	<!-- HERO -->
	<header class="nldir-hero">
		<nav class="nldir-crumbs"><a href="<?php echo esc_url( home_url( '/' ) ); ?>">בית</a> › <span>בעלי מקצוע</span></nav>
		<h1>מצאו בעל מקצוע לנדל״ן</h1>
		<p class="nldir-lead"><?php echo nadlan_dir_sources_lead(); // phpcs:ignore - built from escaped parts ?></p>
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
				<span class="nldir-pill-mark" aria-hidden="true"><svg viewBox="0 0 48 48"><use href="#<?php echo esc_attr( $pm['icon'] ); ?>"></use></svg></span><?php echo esc_html( nadlan_dir_prof_plural( $key, $pm['label'] ) ); ?> <i><?php echo number_format( $n ); ?></i>
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
						<option value="name"<?php selected( $state['sort'], 'name' ); ?>>א׳-ת׳</option>
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
		// a private person from a public register who has not taken over the profile: the quote goes through the site (v98)
		if ( function_exists( 'nadlan_pc_is_private' ) && nadlan_pc_is_private( $id ) ) { $phone = ''; }
		$verified = get_post_meta( $id, 'claim_status', true ) === 'verified';
		$rating   = (float) get_post_meta( $id, 'rating', true );
		$reviews  = (int) get_post_meta( $id, 'reviews_count', true );
		$title    = get_the_title( $id );
		$prof_key = (string) get_post_meta( $id, 'profession', true );
		$broker   = ( 'metavech' === $prof_key );
		$own_wa   = ( $broker && function_exists( 'nadlan_prof_wa_digits' ) ) ? nadlan_prof_wa_digits( $phone ) : '';
		$person   = function_exists( 'nadlan_prof_person_name' ) ? nadlan_prof_person_name( $id ) : $title;
		if ( ! $broker ) { nadlan_dir_enqueue_professional_quote_script(); }

		// no reviews = no line: "טרם התקבלו חוות דעת" announced missing information on nearly every card (honesty law, HAD-249)
		// stars only from real, verified reviews, as on the network's cards: a seeded rating is not shown even with a "נתוני דוגמה" tag (HAD-396)
		$stars = ( $reviews > 0 && $rating > 0 && get_post_meta( $id, 'reviews_verified', true ) )
			? '<span class="nlpf-stars">' . str_repeat( '★', (int) round( $rating ) ) . str_repeat( '☆', max( 0, 5 - (int) round( $rating ) ) ) . '</span> <b>' . number_format( $rating, 1 ) . '</b> <span class="nlpf-rev">(' . $reviews . ' חוות דעת)</span>'
			: '';

		ob_start(); ?>
<div class="nlpf" dir="rtl" style="--pc:<?php echo esc_attr( $pm['color'] ); ?>;--ps:<?php echo esc_attr( $pm['soft'] ); ?>">
	<div class="nlpf-banner"></div>
	<div class="nlpf-head">
		<span class="nlpf-av" aria-hidden="true"><svg class="nl-mark" viewBox="0 0 48 48"><use href="#<?php echo esc_attr( $pm['icon'] ); ?>"></use></svg></span>
		<div class="nlpf-id">
			<div class="nlpf-badges">
				<span class="nlpf-pill"><?php echo esc_html( nadlan_dir_prof_label( $prof_key, $id ) ); ?></span>
				<?php if ( $verified ) : ?><span class="nlpf-vf">✓ בעלות מאומתת</span><?php endif; ?>
				<?php if ( $reg ) : ?><span class="nlpf-reg"><svg class="nl-ico" aria-hidden="true" viewBox="0 0 16 16"><path fill="none" stroke="currentColor" stroke-width="1.4" stroke-linejoin="round" d="M8 1.5l5.5 2v4c0 3.5-2.5 6-5.5 7-3-1-5.5-3.5-5.5-7v-4l5.5-2z"/><path fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round" d="M5.5 8l2 2 3-4"/></svg>רשם הקבלנים #<?php echo esc_html( $reg ); ?></span><?php endif; ?>
			</div>
			<h1 class="nlpf-name"><?php echo esc_html( $title ); ?></h1>
			<div class="nlpf-sub">
				<?php if ( $city ) : ?><span><svg class="nl-ico" aria-hidden="true" viewBox="0 0 16 16"><path fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" d="M8 14s5-4.5 5-8.5A5 5 0 1 0 3 5.5C3 9.5 8 14 8 14z"/><circle cx="8" cy="5.5" r="1.8" fill="none" stroke="currentColor" stroke-width="1.4"/></svg><?php echo esc_html( $city ); ?></span><?php endif; ?>
				<?php if ( $cls ) : ?><span><?php echo esc_html( $cls ); ?></span><?php endif; ?>
			</div>
			<?php if ( '' !== $stars ) : ?><div class="nlpf-rate"><?php echo $stars; ?></div><?php endif; ?>
		</div>
		<div class="nlpf-cta">
			<?php if ( $phone ) : ?><a class="nlpf-call" href="tel:<?php echo esc_attr( preg_replace( '/[^0-9+]/', '', $phone ) ); ?>"><svg class="nl-ico" aria-hidden="true" viewBox="0 0 16 16"><path fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" d="M5.5 2.5c.3 1 .7 2 1.2 2.8.2.3.1.7-.1 1l-.9.9c.7 1.4 1.8 2.5 3.2 3.2l.9-.9c.3-.2.7-.3 1-.1.8.5 1.8.9 2.8 1.2.4.1.6.5.6.9V14a1 1 0 0 1-1.1 1A11.5 11.5 0 0 1 2 4.1 1 1 0 0 1 3 3h1.6c.4 0 .8.2.9.6z"/></svg>התקשרו</a><?php endif; ?>
			<?php if ( $broker ) : /* a broker gets viewings, not quotes; straight to the broker (HAD-249) */ ?>
				<?php if ( $own_wa ) : ?><a class="nlpf-quote" target="_blank" rel="noopener" href="https://wa.me/<?php echo esc_attr( $own_wa ); ?>?text=<?php echo rawurlencode( 'שלום ' . $person . ', אשמח לתאם סיור באחד הנכסים שלך (nad-lan.co.il)' ); ?>">תיאום סיור</a><?php endif; ?>
			<?php else : ?>
			<button type="button" class="nlpf-quote" data-nadlan-professional-quote data-partner-id="<?php echo (int) $id; ?>" data-partner-title="<?php echo esc_attr( $title ); ?>">בקשת הצעת מחיר</button>
			<?php endif; ?>
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
.nlpf-rate{font-size:14px}.nlpf-stars{color:#F5A623;letter-spacing:1px}.nlpf-rev{color:#9a9a9a;font-size:12.5px}.nlpf-norate{color:#b9b4a9;font-style:italic;font-size:13px}.nlpf-demo{display:inline-block;font-size:10.5px;font-weight:600;color:#8a7444;background:#F3EEE3;border:1px solid #D6C189;border-radius:5px;padding:1px 7px;vertical-align:1px}
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
		if ( 'metavech' === $prof ) {
			// a broker's card offers other brokers, never contractors, and never a sample card (HAD-249)
			$mq = array(
				'relation' => 'AND',
				array( 'key' => 'profession', 'value' => 'metavech' ),
				array( 'relation' => 'OR', array( 'key' => 'is_demo', 'compare' => 'NOT EXISTS' ), array( 'key' => 'is_demo', 'value' => array( '1', 'true' ), 'compare' => 'NOT IN' ) ),
			);
		} else {
			if ( $prof ) { $mq[] = array( 'key' => 'profession', 'value' => $prof ); }
			if ( $city ) { $mq[] = array( 'key' => 'city', 'value' => $city, 'compare' => 'LIKE' ); }
			if ( count( $mq ) < 2 ) { return ''; }
		}
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
	/* One header per card (owner 24.9.2026): the profile hero (professional-profile.php, priority 6) is the header and
	 * carries the only H1; this second header, with its own H1 and breadcrumb-like band, is no longer printed. The
	 * quote script it enqueued still loads, because the hero's "קבלו הצעת מחיר" button runs on it. */
	$id = get_the_ID();
	if ( 'metavech' !== (string) get_post_meta( $id, 'profession', true ) ) { nadlan_dir_enqueue_professional_quote_script(); }
	$sim = nadlan_dir_similar( $id );
	return $content . ( function_exists( 'nadlan_pp_shield' ) && '' !== $sim ? nadlan_pp_shield( $sim ) : $sim ); // shielded from wpautop (professional-profile.php)
}, 5 );

/* v1.37.0: clean document title for the glossary (nadlan_term) archive  - 
 * was showing the default "ארכיון NadLan Glossary". */
add_filter( 'get_the_archive_title', function ( $t ) {
	if ( is_post_type_archive( 'nadlan_term' ) ) { return 'מילון מונחי נדל״ן'; }
	return $t;
}, 30 );
add_filter( 'pre_get_document_title', function ( $t ) {
	if ( is_post_type_archive( 'nadlan_term' ) ) {
		return 'מילון מונחי נדל״ן | מושגים, מיסוי, משכנתאות ובנייה | נדלן';
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
		$status = nadlan_dir_status_he( $status );
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
	/* Owner evidence 2026-08-09: on showroom-engine pages this header was
	 * re-attached AFTER the theater, rendering a second "page start" (dark
	 * banner, floating icon card, repeated title, CTA) in the middle of every
	 * project. The engine owns page identity there - including the <h1> - so
	 * this header now renders only where the engine does not. */
	if ( function_exists( 'nadlan_showroom_engine_active_for' )
		&& nadlan_showroom_engine_active_for( get_the_ID() ) ) {
		return $content;
	}
	return nadlan_dir_project_profile_header( get_the_ID() ) . $content;
}, 5 );

/* =========================================================================
 * PROJECTS premium directory (v1.36.0  -  the one that was lost from v1.33)
 * ========================================================================= */


if ( ! function_exists( 'nadlan_dir_status_he' ) ) {
	/* Audit 2026-07-02 (D3 family): never print raw machine enums to visitors. */
	function nadlan_dir_status_he( $status ) {
		$map = array( 'planning' => 'בתכנון', 'permits' => 'בהיתרים', 'pre_sale' => 'טרום מכירה',
			'marketing' => 'בשיווק', 'construction' => 'בבנייה', 'completed' => 'הושלם', 'occupancy' => 'באכלוס' );
		if ( isset( $map[ $status ] ) ) { return $map[ $status ]; }
		return preg_match( '/^[a-z0-9_\-]+$/', (string) $status ) ? '' : $status;
	}
}

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
			// Language siblings (-en/-fr/-ru/-ar) are hreflang alternates of their
			// base project, NEVER catalog entries: as cards they read as garbled
			// mixed-language duplicates (owner audit 2026-07-05).
			'nadlan_no_lang_siblings' => true,
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

/* HAD-700 (10.11.2026): the catalog query (several joins on postmeta, a CASE order, SQL_CALC_FOUND_ROWS) took 2.4 to 3 seconds
 * and ran twice in one page view (the grid and the ItemList schema): 5.4 of the page's 7.5 seconds, measured on the server.
 * Identical SQL now runs once. Its raw result (the ids in order, and the total) is kept for the request and for five minutes in a
 * transient, and every stored result is dropped when a project is saved. On a hit WordPress continues exactly as after a real
 * run (the same filters see the same posts), so the order, the totals and the pages are the query's own. Searches are not kept. */
if ( ! defined( 'NADLAN_DIR_CATALOG_CACHE_LIVE' ) ) { define( 'NADLAN_DIR_CATALOG_CACHE_LIVE', true ); } // on since 1.72.638: a hit and the same order and totals were both measured live behind ?nldc=1 on 1.72.637
if ( ! function_exists( 'nadlan_dir_catalog_cache_ver' ) ) {
	function nadlan_dir_catalog_cache_ver() { return (int) get_option( 'nadlan_dir_catalog_cache_ver', 1 ); }
	function nadlan_dir_catalog_cache_key( $q ) {
		if ( ! NADLAN_DIR_CATALOG_CACHE_LIVE && '1' !== (string) ( $_GET['nldc'] ?? '' ) ) { return ''; } // phpcs:ignore WordPress.Security.NonceVerification.Recommended
		if ( is_admin() || ! $q->get( 'nadlan_no_lang_siblings' ) || 'nadlan_project' !== $q->get( 'post_type' ) ) { return ''; }
		if ( $q->get( 's' ) || $q->get( 'no_found_rows' ) || $q->get( 'suppress_filters' ) || in_array( (string) $q->get( 'fields' ), array( 'ids', 'id=>parent' ), true ) ) { return ''; }
		$sql = (string) $q->request;
		if ( '' === $sql || false !== stripos( $sql, 'RAND(' ) ) { return ''; }
		/* the placement rules put the current second inside the SQL ("promo_until >= <now>"), so the text was never the same twice, not even
		 * inside one page view (measured live behind ?nldc=1 on 10.11.2026: no hit at all). A time within a day of now counts as one
		 * five-minute step in the key. */
		$now = time();
		$sql = (string) preg_replace_callback( '/\b\d{10}\b/', function ( $m ) use ( $now ) { return abs( (int) $m[0] - $now ) < DAY_IN_SECONDS ? 'T' . (int) floor( $now / 300 ) : $m[0]; }, $sql );
		return 'nldc_' . md5( nadlan_dir_catalog_cache_ver() . '|' . (int) $q->get( 'posts_per_page' ) . '|' . $sql );
	}
	add_action( 'save_post_nadlan_project', function () { update_option( 'nadlan_dir_catalog_cache_ver', nadlan_dir_catalog_cache_ver() + 1, true ); } );
	add_filter( 'posts_pre_query', function ( $posts, $q ) {
		if ( null !== $posts ) { return $posts; }
		$k = nadlan_dir_catalog_cache_key( $q );
		if ( '' === $k ) { return $posts; }
		$hit = isset( $GLOBALS['nadlan_dir_catalog_mem'][ $k ] ) ? $GLOBALS['nadlan_dir_catalog_mem'][ $k ] : get_transient( $k );
		if ( ! is_array( $hit ) || ! isset( $hit['ids'], $hit['found'] ) || ! is_array( $hit['ids'] ) ) { $q->nadlan_dir_catalog_store = $k; return $posts; }
		$GLOBALS['nadlan_dir_catalog_mem'][ $k ] = $hit;
		$ids = array_map( 'intval', $hit['ids'] );
		if ( $ids ) { _prime_post_caches( $ids, true, true ); }
		$per = (int) $q->get( 'posts_per_page' );
		$q->found_posts   = (int) $hit['found'];
		$q->max_num_pages = $per > 0 ? (int) ceil( $q->found_posts / $per ) : ( $q->found_posts ? 1 : 0 );
		return $ids;
	}, 5, 2 );
	add_filter( 'posts_results', function ( $posts, $q ) {
		if ( empty( $q->nadlan_dir_catalog_store ) || ! is_array( $posts ) ) { return $posts; }
		$k = (string) $q->nadlan_dir_catalog_store; $q->nadlan_dir_catalog_store = '';
		$ids = array(); foreach ( $posts as $p ) { $ids[] = (int) ( is_object( $p ) ? $p->ID : $p ); }
		$hit = array( 'ids' => $ids, 'found' => (int) $q->found_posts );
		$GLOBALS['nadlan_dir_catalog_mem'][ $k ] = $hit;
		set_transient( $k, $hit, 5 * MINUTE_IN_SECONDS );
		return $posts;
	}, -99999, 2 );
}

/* HAD-700 (10.11.2026): inc/tiers.php adds "paid_tier EXISTS OR paid_tier NOT EXISTS" to the main query of every catalog archive.
 * The clause is always true, so it filters nothing, but it adds two postmeta joins (one without a key) and a GROUP BY; on the project
 * archive the main query and the members plugin's copy of it (pmsc_exclude_post_from_query) took 0.5 s each (measured live with the
 * 1.72.633 profiler). The grid has its own query; this drops only that always-true clause from the project archive's main query. */
add_action( 'pre_get_posts', function ( $q ) {
	if ( is_admin() || ! $q->is_main_query() || ! $q->is_post_type_archive( 'nadlan_project' ) ) { return; }
	$mq = $q->get( 'meta_query' );
	if ( ! is_array( $mq ) || ! $mq ) { return; }
	$out = array();
	foreach ( $mq as $k => $c ) {
		if ( is_array( $c ) && 3 === count( $c ) && 'OR' === strtoupper( (string) ( $c['relation'] ?? '' ) ) && isset( $c[0], $c[1] ) && is_array( $c[0] ) && is_array( $c[1] )
			&& 'paid_tier' === ( $c[0]['key'] ?? '' ) && 'paid_tier' === ( $c[1]['key'] ?? '' ) && ! isset( $c[0]['value'] ) && ! isset( $c[1]['value'] )
			&& 'EXISTS' === strtoupper( (string) ( $c[0]['compare'] ?? '' ) ) && 'NOT EXISTS' === strtoupper( (string) ( $c[1]['compare'] ?? '' ) ) ) {
			continue;
		}
		$out[ $k ] = $c;
	}
	if ( count( $out ) !== count( $mq ) ) { $q->set( 'meta_query', $out ); }
}, 10 );

/* Exclude hreflang language siblings from any query that opts in. */
add_filter( 'posts_where', function ( $where, $q ) {
	if ( $q->get( 'nadlan_no_lang_siblings' ) ) {
		global $wpdb;
		$where .= " AND {$wpdb->posts}.post_name NOT REGEXP '-(en|fr|ru|ar)$'";
	}
	return $where;
}, 10, 2 );

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
		$status = nadlan_dir_status_he( $status );
		$dev    = nadlan_meta_norm( get_post_meta( $id, 'developer_name', true ) );
		$tier   = (string) get_post_meta( $id, 'paid_tier', true );
		$distance = apply_filters( 'nadlan_geo_card_distance', null, $id );
		$featured = in_array( $tier, array( 'pro', 'premier' ), true );

		// owner-uploaded photo wins; otherwise we render an original architectural
		// concept SVG (no stock photo, no faces). Alternate skyline vs tower by ID
		// for visual variety across the grid.
		$photo_url = '';
		if ( has_post_thumbnail( $id ) ) {
			$photo_url = get_the_post_thumbnail_url( $id, 'large' );
		} else {
			$photos = array_filter( array_map( 'trim', explode( ',', (string) get_post_meta( $id, 'photos_csv', true ) ) ) );
			foreach ( $photos as $p ) {
				if ( preg_match( '~^https?://~i', $p ) ) { $photo_url = $p; break; }
			}
		}
		$is_real_photo = $photo_url !== '';
		/* HAD-740: a project with no picture of its own: its Hebrew page's picture (language pages), else the default picture chosen in
		 * Settings > Media. null (gate closed, no option, media gone) = the old behaviour below, exactly. */
		$pd = ( ! $is_real_photo && function_exists( 'nadlan_pd_pick' ) ) ? nadlan_pd_pick( $id ) : null;
		if ( $pd ) { $photo_url = (string) $pd['url']; }
		if ( ! $is_real_photo && ! $pd ) {
			// Rotate 5 real architectural photos from the theme (luxurious, varied)
			// rather than 2 dark concept SVGs so the catalog grid never reads as
			// identical empty blocks. Falls back to the bundled concept SVG if the
			// theme is not present (defensive).
			// SKETCH-ONLY (2026-07-31): the three photo-realistic files that used
			// to rotate here are place-specific, so a Haifa or Be'er Sheva project
			// was illustrated with a Tel Aviv coastline or a sea-view interior
			// (77 of the first 144 archive cards audited). Only the neutral
			// blueprint/sketch files remain: they never claim a place that is not
			// the project's, and they match the house rule of sketches over
			// AI photo-realism.
			$theme_fallbacks = array(
				'tel-aviv-skyline-blueprint.jpg',
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
		$floors = (int) get_post_meta( $id, 'floors', true );
		/* HAD-694 (card per the approved canvas PhoneV2 + Fit, 10.11.2026): the picture box is 8:5; a 4:3 plate fills it from the top
		 * (its drawn strip of facts falls below the box, and the same facts stay as text on the card), a square plate stays whole.
		 * The stage and deal come only from a market row that links to this very page (no name guessing). */
		$slug   = (string) get_post_field( 'post_name', $id );
		$own    = function_exists( 'nadlan_dir_own_project_slugs' ) && in_array( $slug, nadlan_dir_own_project_slugs(), true );
		$mrow   = function_exists( 'nadlan_dir_market_row' ) ? nadlan_dir_market_row( $slug ) : null;
		$img_w  = 0; $img_h = 0;
		if ( $is_real_photo && has_post_thumbnail( $id ) ) {
			$src = wp_get_attachment_image_src( get_post_thumbnail_id( $id ), 'large' );
			if ( is_array( $src ) ) { $img_w = (int) $src[1]; $img_h = (int) $src[2]; }
		}
		if ( $pd ) { $img_w = (int) $pd['w']; $img_h = (int) $pd['h']; }
		$fill = $img_w > 0 && $img_h > 0 && ( $img_w / $img_h ) > 1.25;
		$tags = array();
		if ( $mrow ) {
			$mst = array( 'immediate' => array( 'לאכלוס מיידי', 'is-ready' ), 'near_occupancy' => array( 'אכלוס קרוב', 'is-ready' ), 'construction' => array( 'בבנייה', 'is-build' ), 'marketing' => array( 'בשיווק', 'is-sale' ), 'presale' => array( 'פריסייל', 'is-sale' ) );
			if ( isset( $mst[ (string) ( $mrow['status'] ?? '' ) ] ) ) { $tags[] = $mst[ (string) $mrow['status'] ]; }
			if ( ! empty( $mrow['deal'] ) ) { $tags[] = array( 'במבצע', 'is-deal' ); }
		}
		$rooms = '';
		if ( $mrow && ! empty( $mrow['rooms'] ) && preg_match( '/^\s*(\d+(?:\.5)?)\s*-\s*(\d+(?:\.5)?)/', (string) $mrow['rooms'], $rm ) ) { $rooms = $rm[1] . ' עד ' . $rm[2] . ' חדרים'; }
		// Magazine card (v1.69.69): Lovable MagazineCard design ported to the live
		// "Quiet Luxury" tokens. Stat row uses only real, present meta - never fake data.
		$stats = array();
		if ( $units > 0 )  { $stats[] = array( 'יח״ד', number_format( $units ) ); }
		if ( $floors > 0 ) { $stats[] = array( 'קומות', (string) $floors ); }
		if ( $status && ! $tags ) { $stats[] = array( 'סטטוס', $status ); }
		if ( '' !== $rooms && count( $stats ) < 3 ) { $stats[] = array( 'חדרים', $rooms ); }
		if ( ( $distance !== null && $distance !== '' ) && count( $stats ) < 3 ) { $stats[] = array( 'מרחק', number_format_i18n( (float) $distance, 1 ) . ' ק״מ' ); }
		$stats = array_slice( $stats, 0, 3 );
		ob_start(); ?>
<a class="nldc nldc-project has-media<?php echo $featured ? ' is-featured' : ''; ?><?php echo $own ? ' is-own' : ''; ?>" href="<?php echo esc_url( get_permalink( $id ) ); ?>" style="--pc:<?php echo esc_attr( $pm['color'] ); ?>;--ps:<?php echo esc_attr( $pm['soft'] ); ?>">
	<div class="nldc-media<?php echo $pd ? ( 'twin' === $pd['kind'] ? ' has-real-photo' : ' has-default-pic' ) : ( $is_real_photo ? ' has-real-photo' : ' has-concept-art' ); ?><?php echo $fill ? ' is-fill' : ''; ?>">
		<img src="<?php echo esc_url( $photo_url ); ?>" alt="<?php echo $pd ? esc_attr( (string) $pd['alt'] ) : ''; ?>" loading="lazy" decoding="async"<?php echo $img_w > 0 ? ' width="' . (int) $img_w . '" height="' . (int) $img_h . '"' : ''; ?><?php echo ( $pd && '' !== (string) $pd['srcset'] ) ? ' srcset="' . esc_attr( (string) $pd['srcset'] ) . '" sizes="' . esc_attr( (string) $pd['sizes'] ) . '"' : ''; ?>>
		<?php if ( $featured ) : ?><span class="nldcp-badge">מקודם</span><?php endif; ?>
		<?php if ( $pm['label'] !== 'אחר' && ! ( $pd && 'default' === $pd['kind'] ) ) : /* "other" is a machine fallback, not a badge a buyer should read; HAD-740: nothing printed over the default picture (its type stays in the facts row as "סוג") */ ?><span class="nldcp-type"><?php echo esc_html( $pm['label'] ); ?></span><?php endif; ?>
		<?php if ( $tags ) : ?><span class="nldcp-tags"><?php foreach ( $tags as $t ) : ?><b class="nldcp-tag <?php echo esc_attr( $t[1] ); ?>"><?php echo esc_html( $t[0] ); ?></b><?php endforeach; ?></span><?php endif; ?>
	</div>
	<div class="nldcp-body">
		<div class="nldcp-head">
			<h3 class="nldcp-name" dir="auto"><?php echo esc_html( get_the_title( $id ) ); ?></h3>
			<?php if ( $city ) : ?><span class="nldcp-city"><?php echo esc_html( $city ); ?></span><?php endif; ?>
		</div>
		<?php if ( $stats ) : ?>
		<dl class="nldcp-stats">
			<?php foreach ( $stats as $s ) : ?><div<?php echo in_array( $s[0], array( 'סטטוס', 'חדרים' ), true ) ? ' class="is-word"' : ''; ?>><dt><?php echo esc_html( $s[0] ); ?></dt><dd><?php echo esc_html( $s[1] ); ?></dd></div><?php endforeach; ?>
		</dl>
		<?php endif; ?>
		<?php if ( function_exists( 'nadlan_fc_for_project' ) && ( $fac_keys = nadlan_fc_for_project( $id ) ) ) :
			/* facility chips (owner 2026-07-29): Booking-style at-a-glance. [data-fac]
			   spans, NOT anchors - the whole card is an <a>; the site-wide nlfc handler
			   deep-links each chip to /premium/?fac=. No facility data = no row. */ ?>
		<?php echo nadlan_fc_chips_html( $fac_keys, array( 'limit' => 4, 'link' => false, 'class' => 'nlfc-oncard' ) ); // phpcs:ignore WordPress.Security.EscapeOutput ?>
		<?php endif; ?>
		<div class="nldcp-foot">
			<span class="nldcp-cta"><?php echo $own ? 'לסיור בפרויקט' : 'לפרטי הפרויקט'; ?></span>
		</div>
	</div>
</a>
<?php
		return ob_get_clean();
	}
}

if ( ! function_exists( 'nadlan_dir_quickfilter_html' ) ) {
	/** HAD-694 (canvas PhoneV2, approved 10.11.2026): on a phone the long search form (353 px) and the map thumbnail (300 px) put the
	 * first project card at 1,468 px. A short row of filter chips replaces them on narrow screens; "כל הסינונים" opens the same full
	 * form and the map, so nothing is lost. The chips drive the form's own fields, so the results, the address and the totals are the
	 * form's. Desktop keeps the form as it is. Also the card look of the canvas (8:5 picture, tags, fact chips). */
	function nadlan_dir_quickfilter_html( $facets ) {
		$tlv = 0;
		foreach ( (array) ( $facets['cities'] ?? array() ) as $c ) { if ( isset( $c['name'] ) && false !== mb_strpos( (string) $c['name'], 'תל אביב' ) ) { $tlv = (int) $c['n']; $tlv_name = (string) $c['name']; break; } }
		$nb = (int) ( $facets['types']['new_build'] ?? 0 );
		$chips = array();
		if ( $tlv > 0 ) { $chips[] = '<button type="button" data-k="city" data-v="' . esc_attr( $tlv_name ) . '">תל אביב יפו · ' . number_format( $tlv ) . '</button>'; }
		$chips[] = '<button type="button" data-k="status" data-v="marketing">בשיווק</button>';
		$chips[] = '<button type="button" data-k="status" data-v="construction">בבנייה</button>';
		if ( $nb > 0 ) { $chips[] = '<button type="button" data-k="project_type" data-v="new_build">בנייה חדשה · ' . number_format( $nb ) . '</button>'; }
		$chips[] = '<button type="button" data-a="near">קרוב אליי</button>';
		$chips[] = '<button type="button" data-a="map">מפה</button>';
		$chips[] = '<button type="button" data-a="all" class="nlqf-all" aria-expanded="false">כל הסינונים</button>';
		$css = '<style id="nlqf-css">'
			. '.nlqf{display:none}.nldir[data-mode="projects"] .nldir-jump{min-width:0;max-width:100%}'
			. '@media (max-width:760px){'
			. '.nldir[data-mode="projects"] .nlqf{min-width:0;max-width:calc(100% + 32px);display:flex;gap:8px;overflow-x:auto;-webkit-overflow-scrolling:touch;scrollbar-width:none;margin:2px -16px 6px;padding:2px 16px 4px}'
			. '.nldir .nlqf::-webkit-scrollbar{display:none}'
			. '.nldir .nlqf button{flex:0 0 auto;min-height:44px!important;padding:0 14px!important;margin:0!important;border-radius:22px!important;border:1px solid #C9D3DA!important;background:#fff!important;color:#0F1D26!important;font:500 15px/1 "IBM Plex Sans Hebrew",Heebo,system-ui,sans-serif!important;box-shadow:none!important;text-transform:none!important;letter-spacing:0!important;white-space:nowrap}'
			. '.nldir .nlqf button.is-on{background:#0E4C63!important;border-color:#0E4C63!important;color:#fff!important;font-weight:600!important}'
			. '.nldir .nlqf button.nlqf-all{border-color:#0E4C63!important;color:#0E4C63!important;font-weight:600!important}'
			. '.nldir[data-mode="projects"]:not(.is-qf-open) .nlcp-herogrid,.nldir[data-mode="projects"]:not(.is-qf-open) .nldir-pills{display:none!important}'
			. '.nldir[data-mode="projects"] .nlcp-note:empty{display:none}'
			. '.nldir[data-mode="projects"] .nldir-main{display:flex!important;flex-direction:column!important}'
			. '.nldir[data-mode="projects"] .nldir-main>.nldir-catlead{order:3;margin:16px 0 0!important}'
			. '}'
			. '.nldir-results .nldc-project .nldc-media{aspect-ratio:8/5!important}'
			. '.nldir-results .nldc-project .nldc-media.is-fill{background:#E3EEF2}'
			. '.nldir-results .nldc-project .nldc-media.is-fill img{object-fit:cover!important;object-position:50% 0!important;padding:0!important}'
			. '.nldc-project .nldc-media.has-default-pic{background:#E3EEF2}.nldc-project .nldc-media.has-default-pic img{object-fit:cover;object-position:50% 50%;padding:0}'
			. '.nldc-project .nldcp-tags{position:absolute;inset-block-start:10px;inset-inline-end:10px;display:flex;flex-wrap:wrap;gap:6px;justify-content:flex-end;max-width:70%}'
			. '.nldc-project .nldcp-tag{font:600 13px/1 "IBM Plex Sans Hebrew",Heebo,system-ui,sans-serif;padding:6px 10px;border-radius:6px;color:#fff;background:#0E4C63}'
			. '.nldc-project .nldcp-tag.is-ready{background:#1B6B3C}.nldc-project .nldcp-tag.is-sale{background:#0F1D26}'
			. '.nldc-project .nldcp-tag.is-deal{background:#E9E9F7;color:#2B2A72;box-shadow:inset 0 0 0 1px #3B3A8F}'
			. '.nldir-results .nldc-project .nldcp-stats{display:flex;flex-wrap:wrap;gap:6px;grid-template-columns:none;margin:10px 0 0;padding-top:0;border-top:0}'
			. '.nldir-results .nldc-project .nldcp-stats>div{display:flex;flex-direction:row-reverse;justify-content:flex-end;gap:4px;align-items:baseline;background:#E3EEF2;color:#0A3A4C;border-radius:6px;padding:5px 10px}'
			. '.nldir-results .nldc-project .nldcp-stats dt,.nldir-results .nldc-project .nldcp-stats dd{margin:0;font-size:13px;font-weight:600;color:#0A3A4C;white-space:nowrap}'
			. '.nldir-results .nldc-project .nldcp-stats dt{font-weight:500}'
			. '.nldir-results .nldc-project .nldcp-stats>div.is-word dt{display:none}'
			. '.nldir-results .nldc-project .nldcp-cta{min-height:44px;display:flex;align-items:center;justify-content:center;font-size:15px;border-radius:10px;background:#0F1D26}'
			. '</style>';
		$js = '<script id="nlqf-js">(function(){var r=document.querySelector(\'.nldir[data-mode="projects"]\'),q=r&&r.querySelector(".nlqf");if(!q)return;'
			. 'function bar(){return document.getElementById("nlcp-bar");}'
			. 'function mark(){var b=bar();q.querySelectorAll("button[data-k]").forEach(function(c){var el=b&&b.elements[c.dataset.k];c.classList.toggle("is-on",!!el&&el.value===c.dataset.v);c.setAttribute("aria-pressed",c.classList.contains("is-on")?"true":"false");});}'
			. 'function open(on){r.classList.toggle("is-qf-open",on);var a=q.querySelector(".nlqf-all");if(a){a.classList.toggle("is-on",on);a.setAttribute("aria-expanded",on?"true":"false");}}'
			. 'q.addEventListener("click",function(e){var c=e.target.closest("button");if(!c)return;var b=bar();'
			. 'if(c.dataset.k){var el=b&&b.elements[c.dataset.k];if(!el){open(true);return;}el.value=(el.value===c.dataset.v)?"":c.dataset.v;el.dispatchEvent(new Event("change",{bubbles:true}));mark();return;}'
			. 'if(c.dataset.a==="near"){var n=document.getElementById("nlcp-near");if(n){n.click();}return;}'
			. 'if(c.dataset.a==="map"){var m=document.querySelector(".nlcp-mapthumb");if(m){m.click();}else{open(true);}return;}'
			. 'if(c.dataset.a==="all"){var on=!r.classList.contains("is-qf-open");open(on);if(on&&b){b.scrollIntoView({block:"start",behavior:"smooth"});}}});'
			. 'if(document.readyState==="loading"){document.addEventListener("DOMContentLoaded",mark);}else{mark();}'
			. 'document.addEventListener("change",function(e){if(e.target.closest&&e.target.closest("#nlcp-bar"))setTimeout(mark,0);});})();</script>';
		return $css . '<div class="nlqf" role="group" aria-label="סינון הפרויקטים">' . implode( '', $chips ) . '</div>' . $js;
	}
}

if ( ! function_exists( 'nadlan_dir_itemlist_item' ) ) {
	/** HAD-698: one ListItem of the catalog's ItemList, typed as an ApartmentComplex, carrying only what the card itself shows:
	 * the name, the picture, the address or neighbourhood and city, the number of homes, the developer, the stage, and a price only
	 * when the developer's published "from" price is on the market row that links to this page. Called by snippet 661. */
	function nadlan_dir_itemlist_item( $id, $position ) {
		$id   = (int) $id;
		$url  = get_permalink( $id );
		$item = array( '@type' => 'ApartmentComplex', 'name' => wp_strip_all_tags( get_the_title( $id ) ), 'url' => $url );
		$img  = get_the_post_thumbnail_url( $id, 'large' ); if ( $img ) { $item['image'] = $img; }
		$city = function_exists( 'nadlan_meta_norm' ) ? nadlan_meta_norm( get_post_meta( $id, 'city', true ) ) : trim( (string) get_post_meta( $id, 'city', true ) );
		$addr = trim( (string) get_post_meta( $id, 'address', true ) );
		$hood = trim( (string) get_post_meta( $id, 'neighborhood', true ) );
		if ( '' !== $city || '' !== $addr ) {
			$pa = array( '@type' => 'PostalAddress', 'addressCountry' => 'IL' );
			if ( '' !== $city ) { $pa['addressLocality'] = $city; }
			if ( '' !== $addr ) { $pa['streetAddress'] = $addr; } elseif ( '' !== $hood ) { $pa['streetAddress'] = $hood; }
			$item['address'] = $pa;
		}
		$units = (int) get_post_meta( $id, 'num_units', true );
		if ( $units > 0 ) { $item['numberOfAccommodationUnits'] = $units; }
		$props = array();
		$dev = trim( (string) get_post_meta( $id, 'developer_name', true ) );
		if ( '' !== $dev ) { $props[] = array( '@type' => 'PropertyValue', 'name' => 'יזם', 'value' => $dev ); }
		$slug = (string) get_post_field( 'post_name', $id );
		$row  = function_exists( 'nadlan_dir_market_row' ) ? nadlan_dir_market_row( $slug ) : null;
		$sth  = array( 'immediate' => 'לאכלוס מיידי', 'near_occupancy' => 'אכלוס קרוב', 'construction' => 'בבנייה', 'marketing' => 'בשיווק', 'presale' => 'פריסייל' );
		$stage = $row && isset( $sth[ (string) ( $row['status'] ?? '' ) ] ) ? $sth[ (string) $row['status'] ] : ( function_exists( 'nadlan_dir_status_he' ) ? nadlan_dir_status_he( nadlan_meta_norm( get_post_meta( $id, 'project_status', true ) ) ) : '' );
		if ( '' !== (string) $stage ) { $props[] = array( '@type' => 'PropertyValue', 'name' => 'שלב', 'value' => (string) $stage ); }
		if ( $props ) { $item['additionalProperty'] = $props; }
		if ( $row && (int) ( $row['price_from'] ?? 0 ) > 0 ) {
			$item['offers'] = array( '@type' => 'Offer', 'price' => (int) $row['price_from'], 'priceCurrency' => 'ILS', 'url' => $url, 'description' => 'החל מ' );
		}
		return array( '@type' => 'ListItem', 'position' => (int) $position, 'item' => $item );
	}
}

if ( ! function_exists( 'nadlan_dir_market_row' ) ) {
	/** HAD-694: the market row (data/projects-market.json) whose own link is /projects/<slug>/, or null. Exact links only. */
	function nadlan_dir_market_row( $slug ) {
		static $map = null;
		if ( null === $map ) {
			$map = array();
			$m = function_exists( 'nadlan_ph_market' ) ? nadlan_ph_market() : array();
			foreach ( (array) ( $m['projects'] ?? array() ) as $r ) {
				if ( is_array( $r ) && preg_match( '~^/projects/([^/?#]+)/$~', (string) ( $r['url'] ?? '' ), $mm ) ) { $map[ rawurldecode( $mm[1] ) ] = $r; }
			}
		}
		return isset( $map[ (string) $slug ] ) ? $map[ (string) $slug ] : null;
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
		$k = 'nadlan_dir_projfacets_v4';
		$c = get_transient( $k );
		if ( is_array( $c ) ) { return $c; }
		global $wpdb;
		$private_sql = " AND NOT EXISTS (SELECT 1 FROM {$wpdb->postmeta} private_v2 WHERE private_v2.post_id=p.ID AND private_v2.meta_key='_nadlan_private_unit_journey' AND private_v2.meta_value='private-unit-journey-v2')";
		$types  = $wpdb->get_results( "SELECT pm.meta_value v, COUNT(*) n FROM {$wpdb->postmeta} pm INNER JOIN {$wpdb->posts} p ON p.ID=pm.post_id WHERE pm.meta_key='project_type' AND pm.meta_value<>'' AND p.post_type='nadlan_project' AND p.post_status='publish' AND p.post_name NOT REGEXP '-(en|fr|ru|ar)$'" . $private_sql . ' GROUP BY pm.meta_value', ARRAY_A );
		$cities = $wpdb->get_results( "SELECT pm.meta_value v, COUNT(*) n FROM {$wpdb->postmeta} pm INNER JOIN {$wpdb->posts} p ON p.ID=pm.post_id WHERE pm.meta_key='city' AND pm.meta_value<>'' AND p.post_type='nadlan_project' AND p.post_status='publish' AND p.post_name NOT REGEXP '-(en|fr|ru|ar)$'" . $private_sql . ' GROUP BY pm.meta_value ORDER BY n DESC LIMIT 30', ARRAY_A ); // 1.72.513 (F5): 18 left Be'er Sheva (14 projects) out
		$out = array( 'types' => array(), 'cities' => array(), 'total' => (int) $wpdb->get_var( "SELECT COUNT(*) FROM {$wpdb->posts} p WHERE p.post_type='nadlan_project' AND p.post_status='publish' AND p.post_name NOT REGEXP '-(en|fr|ru|ar)$'" . $private_sql ) );
		foreach ( (array) $types as $r )  { $out['types'][ $r['v'] ] = (int) $r['n']; }
		foreach ( (array) $cities as $r ) { $out['cities'][] = array( 'name' => nadlan_meta_norm( $r['v'] ), 'n' => (int) $r['n'] ); }
		set_transient( $k, $out, HOUR_IN_SECONDS );
		return $out;
	}
}
add_action( 'save_post_nadlan_project', function () {
	delete_transient( 'nadlan_dir_projfacets_v2' );
	delete_transient( 'nadlan_dir_projfacets_v3' );
	delete_transient( 'nadlan_dir_projfacets_v4' );
} );

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
	if ( is_post_type_archive( 'nadlan_project' ) )  { return 'פרויקטים חדשים ודירות חדשות בישראל'; } // HAD-689: the words of Google's page 1 for פרויקטים חדשים
	if ( is_post_type_archive( 'nadlan_property' ) ) { return 'דירות ונכסים'; }
	return $t;
} );
add_filter( 'pre_get_document_title', function ( $t ) {
	if ( is_post_type_archive( 'nadlan_project' ) ) {
		/* de-cannibalized 2026-07-11: the head terms התחדשות עירונית / תמ״א /
		   פינוי בינוי moved to their P0 owner, the /urban-renewal/ pillar */
		/* HAD-689 (Ben 9.11.2026): the title copies the words Google's page 1 uses for פרויקטים חדשים (Yad2 #1 "פרויקטים ודירות
		   חדשות ... - מעודכן ל-2026", Madlan #2 "דירות ופרויקטים חדשים בישראל", nadlan.com "דירות חדשות, פרויקטים חדשים") */
		return 'פרויקטים חדשים ודירות חדשות למכירה בישראל - מעודכן ל-2026 | נדלן';
	}
	return $t;
}, 20 );
/* The catalog had NO meta description (SERP showed scraped card fragments). */
add_filter( 'wpseo_metadesc', function ( $desc ) {
	if ( ! is_post_type_archive( 'nadlan_project' ) || $desc ) { return $desc; }
	return 'כל הפרויקטים החדשים ודירות מקבלן בישראל בקטלוג אחד. חיפוש לפי עיר, יזם וסטטוס, ומידע מסודר על כל פרויקט לפני הפגישה עם היזם.';
}, 25 );

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
			'paged' => max( 1, (int) ( $_GET['paged'] ?? 1 ), (int) get_query_var( 'paged' ) ), // 1.72.513 (F1): /projects/page/2/ showed page 1 again
			'per_page' => 24,
		);
		$wq = nadlan_dir_project_query( $state );
		$total = (int) $wq->found_posts;
		$cards = nadlan_dir_project_cards_html( $wq );
		wp_reset_postdata();

		nadlan_dir_header_single_h1();
		if ( function_exists( 'block_template_part' ) ) { block_template_part( 'header' ); }
		echo nadlan_dir_css();
		// ProjectCard v49: the enrichment's "סוג" repeats the badge on the image; it goes (also on cards "הצגת עוד" adds)
		echo '<script id="nadlan-pc49">(function(){function d(r){(r||document).querySelectorAll(".nldc-project").forEach(function(c){var t=c.querySelector(".nldcp-type");if(!t)return;c.querySelectorAll(".nlcp-facts > div").forEach(function(f){var dt=f.querySelector("dt"),dd=f.querySelector("dd");if(dt&&dd&&dt.textContent.trim()==="סוג"&&dd.textContent.trim()===t.textContent.trim()){var l=f.parentNode;f.remove();if(l&&!l.children.length)l.remove();}});var s=c.parentNode&&c.nextElementSibling&&c.nextElementSibling.querySelector(".nlcp-more summary span");if(s){s.textContent=s.textContent.replace(/\\s+[-\\u2013]\\s*$/,"");}});}'
			. 'function go(){d();var g=document.querySelector(".nldir-results");if(g&&window.MutationObserver){new MutationObserver(function(){d(g);}).observe(g,{childList:true});}}'
			. 'if(document.readyState==="loading"){document.addEventListener("DOMContentLoaded",go);}else{go();}})();</script>';
		?>
<div class="nldir" dir="rtl" data-mode="projects"
	data-rest="<?php echo esc_url( rest_url( 'nadlan/v1/projects' ) ); ?>"
	data-state="<?php echo esc_attr( wp_json_encode( $state ) ); ?>">
	<header class="nldir-hero">
		<nav class="nldir-crumbs"><a href="<?php echo esc_url( home_url( '/' ) ); ?>">בית</a> › <span>פרויקטים</span></nav>
		<h1>פרויקטים חדשים ודירות חדשות בישראל</h1>
		<?php /* ProjectCard v49: the catalog's true make-up from the live counts (942 of 975 are urban-renewal compounds in planning) */
		$nlpc_nouns = array( 'pinui_binui' => 'מתחמי פינוי בינוי', 'new_build' => 'פרויקטים בבנייה חדשה', 'tama38' => 'פרויקטי תמ״א 38', 'urban' => 'פרויקטי התחדשות עירונית' );
		$nlpc_parts = array(); $nlpc_types = (array) ( $facets['types'] ?? array() ); arsort( $nlpc_types );
		foreach ( $nlpc_types as $nlpc_k => $nlpc_n ) { if ( isset( $nlpc_nouns[ $nlpc_k ] ) && (int) $nlpc_n > 0 ) { $nlpc_parts[] = number_format( (int) $nlpc_n ) . ' ' . $nlpc_nouns[ $nlpc_k ]; } }
		$nlpc_last = count( $nlpc_parts ) > 1 ? array_pop( $nlpc_parts ) : '';
		$nlpc_mix  = $nlpc_parts ? ': ' . implode( ', ', $nlpc_parts ) . ( '' !== $nlpc_last ? ' ו־' . $nlpc_last : '' ) : ''; ?>
		<?php $nlph_answer = ( function_exists( 'nadlan_ph_answer_html' ) && function_exists( 'nadlan_ph_top_wanted' ) && nadlan_ph_top_wanted() ) ? nadlan_ph_answer_html() : ''; // HAD-689: what is on the market today, by stage
		echo $nlph_answer; // phpcs:ignore
		ob_start(); ?>
		<p class="nldir-lead nldir-catlead"><strong><?php echo number_format( $facets['total'] ); ?></strong> פרויקטים בקטלוג<?php echo esc_html( $nlpc_mix ); ?>, לפי עיר, יזם וסטטוס. בעלי דירות בבניין ישן? <a href="<?php echo esc_url( home_url( '/urban-renewal/' ) ); ?>">המדריך המלא להתחדשות עירונית</a>.</p>
		<?php $nlph_catlead = ob_get_clean(); if ( '' === $nlph_answer ) { echo $nlph_catlead; $nlph_catlead = ''; } // phpcs:ignore ?>
		<?php if ( function_exists( 'nadlan_ph_body' ) && function_exists( 'nadlan_cp_is_catalog' ) && (int) $state['paged'] < 2 ) : /* 1.72.513 the hub: the answer first, then a way into every section below the grid */ ?>
		<?php ob_start(); ?>
		<p class="nldir-lead nldir-intro">מחפשים פרויקט חדש או דירה חדשה מקבלן? כאן רואים את כל הפרויקטים החדשים בישראל לפי עיר, יזם ושלב. <?php echo '' !== $nlph_answer ? 'בעמוד הזה: דירות חדשות לאכלוס מיידי,' : 'מתחת לקטלוג:'; ?> פרויקטים בשיווק עם המחיר שפרסם היזם, פרויקטים חדשים בתל אביב לפי אזור, מחירי עסקאות בכל עיר, לוח הזמנים מהיתר הבנייה ועד המפתח, מחשבונים ותשע בדיקות לפני שחותמים. עודכן ב־<?php echo esc_html( date_i18n( 'j.n.Y', strtotime( defined( 'NADLAN_PH_UPDATED_HE' ) ? NADLAN_PH_UPDATED_HE : NADLAN_PH_UPDATED ) ) ); ?>.</p>
		<?php $nlph_intro = ob_get_clean(); if ( '' === $nlph_answer ) { echo $nlph_intro; $nlph_intro = ''; } // phpcs:ignore HAD-689 (Ben 10.11.2026): on the main view the cards come first; this paragraph opens the sections under them ?>
		<nav class="nldir-jump" aria-label="בעמוד הזה"><?php echo '' !== $nlph_answer ? '<a href="#nlph-ready">לאכלוס מיידי</a>' : ''; ?><?php echo function_exists( 'nadlan_ph_market' ) && ! empty( nadlan_ph_market()['projects'] ) ? '<a href="#nlph-market">בשיווק עכשיו</a>' : ''; ?><a href="#nlph-tlv">פרויקטים בתל אביב</a><a href="#nlph-prices">מחירים לפי עיר</a><a href="#nlph-timeline">מהיתר למפתח</a><a href="#nlph-pay">תשלומים והצמדה</a><a href="#nlph-tools">מחשבונים</a><a href="#nlph-checks">בדיקות לפני חתימה</a><a href="#nlph-faq">שאלות נפוצות</a></nav>
		<?php echo function_exists( 'nadlan_phl_langs' ) ? nadlan_phl_langs( 'he' ) : ''; // the same catalog in English, Russian, French ?>
		<style>.nldir-jump{display:flex;gap:6px;overflow-x:auto;-webkit-overflow-scrolling:touch;scrollbar-width:none;margin:2px 0 12px;padding-bottom:2px}.nldir-jump::-webkit-scrollbar{display:none}.nldir-jump a{flex:0 0 auto;font:500 14px/1 "IBM Plex Sans Hebrew",Heebo,system-ui,sans-serif;color:#14213D;text-decoration:none;border:1px solid #C9D3DC;background:#fff;border-radius:999px;padding:9px 13px}.nldir-jump a:hover{border-color:#14213D}html{scroll-padding-top:90px}</style>
		<?php else : ?>
		<p class="nldir-lead nldir-intro">מחפשים דירה חדשה מקבלן? כאן בודקים כל פרויקט לפני הפגישה עם היזם: סטטוס בנייה, יחידות, מיקום וכל מה שחשוב לדעת לפני שמתקדמים.</p>
		<?php endif; ?>
		<?php echo function_exists( 'nadlan_dir_quickfilter_html' ) ? nadlan_dir_quickfilter_html( $facets ) : ''; // phpcs:ignore HAD-694: the short filter row on phones ?>
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
<?php echo function_exists( 'nadlan_drone_map_band' ) ? nadlan_drone_map_band() : ''; // phpcs:ignore ?>

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
			<?php echo isset( $nlph_catlead ) ? str_replace( 'class="nldir-lead nldir-catlead"', 'class="nldir-lead nldir-catlead" style="font-size:15px;line-height:1.6;margin:0 0 12px"', $nlph_catlead ) : ''; // phpcs:ignore HAD-689: the catalogue's make-up, next to the catalogue ?>
			<div class="nldir-bar">
				<h2 class="nldir-count" style="font:inherit;font-size:15px;margin:0;color:inherit;line-height:inherit"><strong id="nldir-total"><?php echo number_format( $total ); ?></strong> פרויקטים בקטלוג</h2><?php /* 1.72.513 (F8): an H2 above the grid */ ?>
				<div class="nldir-chips" id="nldir-chips"></div>
				<label class="nldir-sortw">מיון:
					<select id="nldir-sort">
						<option value="featured"<?php selected( $state['sort'], 'featured' ); ?>>מומלצים</option>
						<option value="units"<?php selected( $state['sort'], 'units' ); ?>>הכי הרבה יח״ד</option>
						<option value="newest"<?php selected( $state['sort'], 'newest' ); ?>>חדש</option>
						<option value="name"<?php selected( $state['sort'], 'name' ); ?>>א׳-ת׳</option>
					</select>
				</label>
			</div>
			<div class="nldir-results" id="nldir-results"><?php echo $cards; ?></div>
			<div class="nldir-more-wrap"><button type="button" class="nldir-more" id="nldir-more"<?php echo $wq->max_num_pages > 1 ? '' : ' style="display:none"'; ?>>הצגת עוד</button></div>
		</main>
	</div>
<?php /* HAD-689 (Ben 10.11.2026): the project cards with their pictures open the page; דירות חדשות לאכלוס מיידי and the marketing table follow them */
echo ! empty( $nlph_intro ) ? '<div class="nldir-after" style="max-width:1180px;margin:18px auto 0;padding:0 16px">' . $nlph_intro . '</div>' : ''; // phpcs:ignore
echo function_exists( 'nadlan_ph_top_html' ) ? nadlan_ph_top_html() : ''; // phpcs:ignore ?>
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
require_once __DIR__ . '/projects-hub.php'; // 1.72.513: the /projects/ hub (body after the grid, FAQ, tools)
if ( is_readable( __DIR__ . '/project-default-image.php' ) ) { require_once __DIR__ . '/project-default-image.php'; } // 1.72.677 HAD-740: the default card picture (Settings > Media)
