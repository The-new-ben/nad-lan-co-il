/* x-catalog-plus v2.0 (6.9.2026: map v2 thumbnail + full price map, surroundings on project pages;: price context on project pages;: status filter guard, city key, facts dedupe, free-text field, mobile order, overlay to body;, chunked string injection after v1.0 blanked the page for ~40 seconds, owner GO "מבצעים את כל התוכנית") - the projects catalog (/projects/) becomes a data page.
 * Additive layer over inc/directory.php: nothing in the base renderer is edited. Everything here is reversible by deactivating the snippet.
 *  1. Price context from Tax Authority transactions (uploads/nadlan-skin/deals-context-v1.json, built by tools/deals/build_deals_context.py):
 *     ₪/sqm in the city (and the street when the project address matches), deal counts and the period. Never extrapolated, always dated.
 *  2. Card enrichment (server side, in the HTML): full title, neighborhood, floors, completion year, developer, context line, "עוד פרטים".
 *  3. Booking-style search bar: city, status, type, size, "near me" (nearest city by geolocation), sort. REST route nadlan/v1/projects-plus.
 *  4. Sidebar price map (light, no WebGL) + the live drone map moved to the sidebar as an on-demand overlay so it never pushes the cards.
 *  5. Body copy with h2 sections, FAQ (+FAQPage schema), city links with keyword anchors, ItemList schema for the visible cards.
 * Honesty law: a figure appears only with its source and period; unknown fields are omitted, never announced. */

if ( ! function_exists( 'nadlan_cp_is_catalog' ) ) {
	function nadlan_cp_is_catalog() { return is_post_type_archive( 'nadlan_project' ) && ! is_admin(); }
}

/* ------------------------------------------------------------------ data */
if ( ! function_exists( 'nadlan_cp_data' ) ) {
	function nadlan_cp_data() {
		static $d = null;
		if ( null !== $d ) { return $d; }
		$c = get_transient( 'nadlan_cp_deals_v1' );
		if ( is_array( $c ) ) { return $d = $c; }
		$up = wp_get_upload_dir(); $p = trailingslashit( $up['basedir'] ) . 'nadlan-skin/deals-context-v1.json';
		$d = array();
		if ( file_exists( $p ) ) { $j = json_decode( (string) file_get_contents( $p ), true ); if ( is_array( $j ) && ! empty( $j['cities'] ) ) { $d = $j; } }
		set_transient( 'nadlan_cp_deals_v1', $d, 6 * HOUR_IN_SECONDS );
		return $d;
	}
}
if ( ! function_exists( 'nadlan_cp_city_key' ) ) {
	function nadlan_cp_city_key( $city ) {
		$c = trim( (string) $city );
		$c = str_replace( array( ' -', '- ', '-', '־' ), ' ', $c );
		$c = preg_replace( '/\s+/u', ' ', $c );
		$c = str_replace( array( 'הרצלייה', 'מודיעין מכבים רעות', 'פתח תקוה' ), array( 'הרצליה', 'מודיעין', 'פתח תקווה' ), $c );
		if ( 0 === mb_strpos( $c, 'תל אביב' ) ) { $c = 'תל אביב יפו'; }
		return trim( $c );
	}
}
if ( ! function_exists( 'nadlan_cp_city_data' ) ) {
	function nadlan_cp_city_data( $city ) {
		$d = nadlan_cp_data(); if ( empty( $d['cities'] ) ) { return null; }
		$k = nadlan_cp_city_key( $city ); if ( '' === $k ) { return null; }
		if ( isset( $d['cities'][ $k ] ) ) { return $d['cities'][ $k ] + array( 'key' => $k ); }
		foreach ( $d['cities'] as $name => $row ) { if ( false !== mb_strpos( $k, $name ) || false !== mb_strpos( $name, $k ) ) { return $row + array( 'key' => $name ); } }
		return null;
	}
}
if ( ! function_exists( 'nadlan_cp_period' ) ) {
	function nadlan_cp_period( $row ) {
		$f = (string) ( $row['period_from'] ?? '' ); $t = (string) ( $row['period_to'] ?? '' );
		$fmt = function ( $ym ) { if ( ! preg_match( '/^(\d{4})-(\d{2})$/', $ym, $m ) ) { return $ym; } return (int) $m[2] . '.' . $m[1]; };
		return $f && $t ? $fmt( $f ) . ' עד ' . $fmt( $t ) : '';
	}
}
if ( ! function_exists( 'nadlan_cp_context' ) ) {
	/** Context for one project: city ₪/sqm (+street when matched), deal count, period, project's own ₪/sqm meta when present. */
	function nadlan_cp_context( $id ) {
		$city = (string) get_post_meta( $id, 'city', true );
		$row  = nadlan_cp_city_data( $city );
		$out  = array( 'city' => nadlan_cp_city_key( $city ), 'row' => $row, 'street' => null, 'own' => (int) get_post_meta( $id, 'project_3d_avg_price_per_sqm', true ) );
		if ( $row && ! empty( $row['streets'] ) ) {
			$addr = (string) get_post_meta( $id, 'address', true );
			if ( '' !== $addr ) {
				foreach ( $row['streets'] as $street => $s ) { if ( mb_strlen( $street ) >= 3 && false !== mb_strpos( $addr, $street ) ) { $out['street'] = array( 'name' => $street ) + $s; break; } }
			}
		}
		return $out;
	}
}
if ( ! function_exists( 'nadlan_cp_nis' ) ) {
	function nadlan_cp_nis( $n ) { return number_format( (float) $n, 0, '.', ',' ) . ' ₪'; }
}

/* ------------------------------------------------------------------ status groups (real meta values are free text + english keys) */
if ( ! function_exists( 'nadlan_cp_status_groups' ) ) {
	function nadlan_cp_status_groups() {
		return array(
			'planning'     => array( 'label' => 'בתכנון',  'like' => array( 'planning', 'תכנון', 'תכנית מאושרת לפני מימוש', 'על הנייר' ) ),
			'permits'      => array( 'label' => 'בהיתרים', 'like' => array( 'permits', 'היתר' ) ),
			'marketing'    => array( 'label' => 'בשיווק',  'like' => array( 'marketing', 'pre_sale', 'שיווק', 'טרום מכירה' ) ),
			'construction' => array( 'label' => 'בבנייה',  'like' => array( 'construction', 'בהקמה', 'בבנייה', 'בבניה', 'במימוש' ) ),
			'completed'    => array( 'label' => 'הושלם',   'like' => array( 'completed', 'occupancy', 'הושלם', 'אכלוס', 'מאוכלס' ) ),
		);
	}
}
if ( ! function_exists( 'nadlan_cp_status_label' ) ) {
	function nadlan_cp_status_label( $s ) {
		$s = trim( (string) $s ); if ( '' === $s ) { return ''; }
		if ( function_exists( 'nadlan_dir_status_he' ) ) { $he = nadlan_dir_status_he( $s ); if ( '' !== $he ) { return $he; } }
		return preg_match( '/^[a-z0-9_\-]+$/', $s ) ? '' : $s;
	}
}

/* ------------------------------------------------------------------ cities: coordinates for "near me" and the price map */
if ( ! function_exists( 'nadlan_cp_city_coords' ) ) {
	function nadlan_cp_city_coords() {
		return array(
			'תל אביב יפו' => array( 32.0853, 34.7818 ), 'ירושלים' => array( 31.7683, 35.2137 ), 'חיפה' => array( 32.7940, 34.9896 ), 'ראשון לציון' => array( 31.9730, 34.7925 ),
			'פתח תקווה' => array( 32.0840, 34.8878 ), 'אשדוד' => array( 31.8014, 34.6435 ), 'נתניה' => array( 32.3215, 34.8532 ), 'באר שבע' => array( 31.2530, 34.7915 ),
			'בני ברק' => array( 32.0807, 34.8338 ), 'חולון' => array( 32.0158, 34.7874 ), 'רמת גן' => array( 32.0684, 34.8248 ), 'אשקלון' => array( 31.6688, 34.5743 ),
			'רחובות' => array( 31.8928, 34.8113 ), 'בת ים' => array( 32.0231, 34.7503 ), 'בית שמש' => array( 31.7514, 34.9886 ), 'כפר סבא' => array( 32.1750, 34.9070 ),
			'הרצליה' => array( 32.1663, 34.8433 ), 'חדרה' => array( 32.4340, 34.9197 ), 'מודיעין' => array( 31.8969, 35.0104 ), 'רעננה' => array( 32.1848, 34.8713 ),
			'גבעתיים' => array( 32.0723, 34.8125 ), 'נס ציונה' => array( 31.9293, 34.7987 ), 'רמלה' => array( 31.9297, 34.8668 ), 'לוד' => array( 31.9516, 34.8953 ),
			'נהריה' => array( 33.0058, 35.0949 ), 'עכו' => array( 32.9281, 35.0818 ), 'קרית ביאליק' => array( 32.8275, 35.0858 ), 'נשר' => array( 32.7683, 35.0432 ),
			'יקנעם עילית' => array( 32.6591, 35.1101 ), 'עפולה' => array( 32.6078, 35.2897 ), 'טבריה' => array( 32.7922, 35.5312 ), 'אילת' => array( 29.5577, 34.9519 ),
			'קרית אונו' => array( 32.0631, 34.8557 ), 'הוד השרון' => array( 32.1556, 34.8885 ), 'ראש העין' => array( 32.0956, 34.9567 ), 'יבנה' => array( 31.8781, 34.7389 ),
			'קרית גת' => array( 31.6100, 34.7642 ), 'אור יהודה' => array( 32.0292, 34.8564 ), 'חריש' => array( 32.4620, 35.0442 ), 'טירת כרמל' => array( 32.7606, 34.9717 ),
			'קרית מוצקין' => array( 32.8378, 35.0768 ), 'קרית ים' => array( 32.8496, 35.0691 ), 'נתיבות' => array( 31.4225, 34.5885 ), 'שוהם' => array( 31.9990, 34.9470 ),
		);
	}
}

/* ------------------------------------------------------------------ card enrichment */
if ( ! function_exists( 'nadlan_cp_card_facts' ) ) {
	function nadlan_cp_card_facts( $id ) {
		$facts = array();
		$nb = trim( (string) get_post_meta( $id, 'neighborhood', true ) ); if ( $nb ) { $facts[] = array( 'שכונה', $nb ); }
		$fl = (int) get_post_meta( $id, 'num_floors', true ); if ( $fl > 0 ) { $facts[] = array( 'קומות', (string) $fl ); }
		$nbld = (int) get_post_meta( $id, 'num_buildings', true ); if ( $nbld > 1 ) { $facts[] = array( 'בניינים', (string) $nbld ); }
		$yr = (int) get_post_meta( $id, 'completion_year', true ); if ( $yr >= 2024 && $yr <= 2040 ) { $facts[] = array( 'אכלוס משוער', (string) $yr ); }
		$dev = trim( (string) get_post_meta( $id, 'developer_name', true ) ); if ( $dev ) { $facts[] = array( 'יזם', $dev ); }
		$arch = trim( (string) get_post_meta( $id, 'architect_name', true ) ); if ( $arch ) { $facts[] = array( 'אדריכל', $arch ); }
		$pt = (string) get_post_meta( $id, 'project_type', true );
		if ( function_exists( 'nadlan_dir_pt_meta' ) ) { $pm = nadlan_dir_pt_meta( $pt ); if ( ! empty( $pm['label'] ) && 'אחר' !== $pm['label'] ) { $facts[] = array( 'סוג', $pm['label'] ); } }
		return $facts;
	}
}
if ( ! function_exists( 'nadlan_cp_context_line' ) ) {
	function nadlan_cp_context_line( $ctx, $compact = true ) {
		$row = $ctx['row']; if ( ! $row || empty( $row['psqm_all'] ) ) { return ''; }
		$parts = array();
		$parts[] = 'מחיר למ"ר ב' . esc_html( $ctx['city'] ) . ': <b>' . esc_html( nadlan_cp_nis( $row['psqm_all'] ) ) . '</b>';
		if ( ! empty( $ctx['street']['psqm'] ) ) { $parts[] = 'ברחוב ' . esc_html( $ctx['street']['name'] ) . ': <b>' . esc_html( nadlan_cp_nis( $ctx['street']['psqm'] ) ) . '</b>'; }
		if ( $ctx['own'] > 5000 ) { $parts[] = 'בפרויקט: <b>' . esc_html( nadlan_cp_nis( $ctx['own'] ) ) . '</b>'; }
		$meta = number_format( (int) $row['deals_24m'] ) . ' עסקאות, ' . esc_html( nadlan_cp_period( $row ) );
		return '<p class="nlcp-ctx"><span class="nlcp-ctx__k" aria-hidden="true">₪</span><span>' . implode( ' · ', $parts ) . '</span><small>' . $meta . ' · רשות המסים</small></p>';
	}
}
if ( ! function_exists( 'nadlan_cp_more_html' ) ) {
	function nadlan_cp_more_html( $id, $ctx, $facts ) {
		$title = get_the_title( $id ); $url = get_permalink( $id );
		$city = (string) get_post_meta( $id, 'city', true ); $units = (int) get_post_meta( $id, 'num_units', true );
		$status = nadlan_cp_status_label( get_post_meta( $id, 'project_status', true ) );
		$addr = trim( (string) get_post_meta( $id, 'address', true ) );
		$rows = array();
		if ( $city ) { $rows[] = array( 'עיר', $city ); }
		if ( $addr ) { $rows[] = array( 'כתובת', $addr ); }
		if ( $status ) { $rows[] = array( 'סטטוס', $status ); }
		if ( $units > 0 ) { $rows[] = array( 'יחידות דיור', number_format( $units ) ); }
		foreach ( $facts as $f ) { $rows[] = $f; }
		$row = $ctx['row'];
		if ( $row && ! empty( $row['psqm_all'] ) ) {
			$rows[] = array( 'מחיר למ"ר בעיר', nadlan_cp_nis( $row['psqm_all'] ) . ' (' . number_format( (int) $row['deals_24m'] ) . ' עסקאות, ' . nadlan_cp_period( $row ) . ')' );
			if ( ! empty( $row['psqm_new'] ) && (int) $row['deals_new_24m'] >= 30 ) { $rows[] = array( 'מחיר למ"ר בפרויקטים חדשים בעיר', nadlan_cp_nis( $row['psqm_new'] ) . ' (' . number_format( (int) $row['deals_new_24m'] ) . ' עסקאות)' ); }
			foreach ( array( '3', '4', '5' ) as $r ) { if ( ! empty( $row['price_by_rooms'][ $r ] ) ) { $rows[] = array( 'דירת ' . $r . ' חדרים בעיר, חציון', nadlan_cp_nis( $row['price_by_rooms'][ $r ] ) ); } }
			if ( ! empty( $ctx['street']['psqm'] ) ) { $rows[] = array( 'מחיר למ"ר ברחוב ' . $ctx['street']['name'], nadlan_cp_nis( $ctx['street']['psqm'] ) . ' (' . (int) $ctx['street']['n'] . ' עסקאות)' ); }
		}
		$h  = '<details class="nlcp-more"><summary><span>עוד פרטים על ' . esc_html( wp_trim_words( $title, 4, '' ) ) . '</span><i aria-hidden="true">+</i></summary><div class="nlcp-more__in"><dl>';
		foreach ( $rows as $r ) { $h .= '<div><dt>' . esc_html( $r[0] ) . '</dt><dd>' . esc_html( $r[1] ) . '</dd></div>'; }
		$h .= '</dl>';
		if ( $row && ! empty( $row['psqm_all'] ) ) { $h .= '<p class="nlcp-src">מחירי הסביבה: עסקאות שדווחו לרשות המסים, דירות בבתי קומות, חציון. אינם מחיר הפרויקט.</p>'; }
		$h .= '<a class="nlcp-more__go" href="' . esc_url( $url ) . '">לעמוד הפרויקט</a></div></details>';
		return $h;
	}
}
if ( ! function_exists( 'nadlan_cp_enrich_cards' ) ) {
	/** Wrap every catalog card: full title alt, facts + context inside the card, "more" details outside the anchor.
	 *  Chunked string work (no regex across the whole document): PCRE backtrack limits blanked the page in v1.0. */
	function nadlan_cp_enrich_cards( $html ) {
		$marker = '<a class="nldc nldc-project';
		if ( false === strpos( $html, $marker ) ) { return $html; }
		try {
			$parts = explode( $marker, $html ); $out = $parts[0];
			for ( $i = 1, $n = count( $parts ); $i < $n; $i++ ) {
				$chunk = $marker . $parts[ $i ];
				$end = strpos( $chunk, '</a>' );
				if ( false === $end || ! preg_match( '~^<a class="nldc nldc-project[^"]*" href="([^"]+)"~u', $chunk, $m ) ) { $out .= $chunk; continue; }
				$card = substr( $chunk, 0, $end + 4 ); $rest = substr( $chunk, $end + 4 );
				$id = url_to_postid( html_entity_decode( $m[1] ) );
				if ( ! $id ) { $out .= $chunk; continue; }
				$title = get_the_title( $id );
				$ctx = nadlan_cp_context( $id ); $facts = nadlan_cp_card_facts( $id );
				$facts = array_values( array_filter( $facts, function ( $f ) use ( $card ) { return false === strpos( $card, '<dt>' . $f[0] . '</dt>' ); } ) );
				$inner = '';
				if ( $facts ) { $inner .= '<dl class="nlcp-facts">'; foreach ( array_slice( $facts, 0, 4 ) as $f ) { $inner .= '<div><dt>' . esc_html( $f[0] ) . '</dt><dd>' . esc_html( $f[1] ) . '</dd></div>'; } $inner .= '</dl>'; }
				$inner .= nadlan_cp_context_line( $ctx );
				$card = str_replace( 'alt="" loading="lazy"', 'alt="' . esc_attr( $title . ' · הדמיה להמחשה' ) . '" loading="lazy"', $card );
				$pos = strpos( $card, '<div class="nldcp-foot">' );
				if ( false !== $pos ) { $card = substr( $card, 0, $pos ) . $inner . substr( $card, $pos ); }
				$out .= '<article class="nlcp-card">' . $card . nadlan_cp_more_html( $id, $ctx, $facts ) . '</article>' . $rest;
			}
			return $out;
		} catch ( \Throwable $e ) { return $html; }
	}
}

/* ------------------------------------------------------------------ REST: projects-plus (status + near-me on top of the base query) */
add_action( 'rest_api_init', function () {
	register_rest_route( 'nadlan/v1', '/projects-plus', array(
		'methods' => 'GET', 'permission_callback' => '__return_true',
		'callback' => function ( $req ) {
			if ( ! function_exists( 'nadlan_dir_project_query' ) || ! function_exists( 'nadlan_dir_project_cards_html' ) ) { return new WP_Error( 'nocatalog', 'catalog unavailable', array( 'status' => 500 ) ); }
			$p = array(
				'q' => (string) $req->get_param( 'q' ), 'city' => (string) $req->get_param( 'city' ), 'project_type' => (string) $req->get_param( 'project_type' ),
				'min_units' => (int) $req->get_param( 'min_units' ), 'sort' => (string) $req->get_param( 'sort' ), 'paged' => (int) $req->get_param( 'paged' ), 'per_page' => (int) $req->get_param( 'per_page' ),
			);
			$status = sanitize_key( (string) $req->get_param( 'status' ) ); $groups = nadlan_cp_status_groups();
			$filter = null;
			if ( $status && isset( $groups[ $status ] ) ) {
				$likes = $groups[ $status ]['like'];
				$filter = function ( $args ) use ( $likes ) {
					$mq = ( isset( $args['meta_query'] ) && is_array( $args['meta_query'] ) ) ? $args['meta_query'] : array( 'relation' => 'AND' );
					$or = array( 'relation' => 'OR' ); foreach ( $likes as $l ) { $or[] = array( 'key' => 'project_status', 'value' => $l, 'compare' => 'LIKE' ); }
					$mq[] = $or; $args['meta_query'] = $mq; return $args;
				};
				add_filter( 'nadlan_cp_query_args', $filter );
			}
			$wq = nadlan_cp_project_query( $p );
			if ( $filter ) { remove_filter( 'nadlan_cp_query_args', $filter ); }
			$html = nadlan_cp_enrich_cards( nadlan_dir_project_cards_html( $wq ) );
			$out = array( 'ok' => true, 'html' => $html, 'total' => (int) $wq->found_posts, 'pages' => (int) $wq->max_num_pages, 'paged' => max( 1, $p['paged'] ) );
			wp_reset_postdata();
			return $out;
		},
	) );
} );
if ( ! function_exists( 'nadlan_cp_project_query' ) ) {
	/** Same query as the base catalog, with one hook for the extra status filter (the base builder has none). */
	function nadlan_cp_project_query( $p ) {
		$hook = function ( $q ) {
			if ( 'nadlan_project' !== $q->get( 'post_type' ) || ! $q->get( 'nadlan_no_lang_siblings' ) ) { return; }
			$args = apply_filters( 'nadlan_cp_query_args', array( 'meta_query' => $q->get( 'meta_query' ) ) );
			if ( ! empty( $args['meta_query'] ) ) { $q->set( 'meta_query', $args['meta_query'] ); }
		};
		add_action( 'pre_get_posts', $hook, 5 );
		$wq = nadlan_dir_project_query( $p );
		remove_action( 'pre_get_posts', $hook, 5 );
		return $wq;
	}
}

/* ------------------------------------------------------------------ body copy, FAQ, price map, schema */
if ( ! function_exists( 'nadlan_cp_city_hub_url' ) ) {
	function nadlan_cp_city_hub_url( $city ) {
		$hub = get_page_by_path( 'city/' . sanitize_title( $city ) . '/projects' );
		return ( $hub && 'publish' === $hub->post_status ) ? get_permalink( $hub ) : home_url( '/projects/?city=' . rawurlencode( $city ) );
	}
}
if ( ! function_exists( 'nadlan_cp_price_table' ) ) {
	function nadlan_cp_price_table( $facets ) {
		$d = nadlan_cp_data(); if ( empty( $d['cities'] ) ) { return ''; }
		$rows = array();
		foreach ( array_slice( (array) ( $facets['cities'] ?? array() ), 0, 40 ) as $c ) {
			$row = nadlan_cp_city_data( $c['name'] ); if ( ! $row || empty( $row['psqm_all'] ) ) { continue; }
			$rows[] = array( 'city' => $c['name'], 'n' => (int) $c['n'], 'row' => $row );
			if ( count( $rows ) >= 12 ) { break; }
		}
		if ( ! $rows ) { return ''; }
		$h = '<div class="nlcp-tablewrap"><table class="nlcp-table"><thead><tr><th>עיר</th><th>פרויקטים חדשים בקטלוג</th><th>מחיר למ"ר</th><th>דירת 4 חדרים, חציון</th><th>עסקאות</th><th>תקופה</th></tr></thead><tbody>';
		foreach ( $rows as $r ) {
			$row = $r['row'];
			$h .= '<tr><td><a href="' . esc_url( nadlan_cp_city_hub_url( $r['city'] ) ) . '">פרויקטים חדשים ב' . esc_html( $r['city'] ) . '</a></td><td>' . (int) $r['n'] . '</td><td>' . esc_html( nadlan_cp_nis( $row['psqm_all'] ) ) . '</td><td>' . ( ! empty( $row['price_by_rooms']['4'] ) ? esc_html( nadlan_cp_nis( $row['price_by_rooms']['4'] ) ) : '' ) . '</td><td>' . number_format( (int) $row['deals_24m'] ) . '</td><td>' . esc_html( nadlan_cp_period( $row ) ) . '</td></tr>';
		}
		$h .= '</tbody></table></div><p class="nlcp-src">המקור: עסקאות שדווחו לרשות המסים ופורסמו במאגר המידע הממשלתי. חציון של דירות בבתי קומות, 24 החודשים האחרונים שבמאגר לכל עיר. מחיר פרויקט ספציפי נקבע מול היזם.</p>';
		return $h;
	}
}
if ( ! function_exists( 'nadlan_cp_faq' ) ) {
	function nadlan_cp_faq() {
		return array(
			array( 'מה נחשב פרויקט חדש מקבלן?', 'פרויקט מגורים שנבנה או משווק על ידי יזם או קבלן, ובו הדירות נמכרות לראשונה: בנייה חדשה על מגרש פנוי, או דירות חדשות בפרויקט התחדשות עירונית מסוג פינוי בינוי ותמ"א 38.' ),
			array( 'מה ההבדל בין דירה חדשה מקבלן לדירה יד שנייה?', 'בדירה חדשה מקבלן מקבלים מפרט חדש, ערבות חוק המכר, אחריות ותקופת בדק. המחיר נקבע מול היזם ולא במשא ומתן עם דייר, ולוח התשלומים נפרס לפי קצב הבנייה.' ),
			array( 'איך בודקים פרויקט חדש לפני שחותמים?', 'בודקים שהקבלן רשום בפנקס הקבלנים, שיש היתר בנייה בתוקף, מה כולל המפרט הטכני, מה מועד המסירה ומה הפיצוי על איחור, ומה מחירי העסקאות בסביבה לפי רשות המסים.' ),
			array( 'מה ההבדל בין בנייה חדשה, פינוי בינוי ותמ"א 38?', 'בנייה חדשה היא פרויקט על מגרש פנוי. פינוי בינוי הורס בניינים ישנים ובונה מתחם חדש. תמ"א 38 מחזקת או הורסת ובונה בניין בודד. בכל השלושה נמכרות דירות חדשות מקבלן, אבל לוחות הזמנים והוודאות שונים.' ),
			array( 'איפה רואים מחירים של דירות חדשות?', 'בקטלוג מופיע לכל פרויקט מחיר למ"ר בעיר וברחוב לפי עסקאות שדווחו לרשות המסים, עם מספר העסקאות והתקופה. מחיר הדירה בפרויקט עצמו מתקבל מהיזם.' ),
		);
	}
}
if ( ! function_exists( 'nadlan_cp_body_html' ) ) {
	function nadlan_cp_body_html( $facets ) {
		$total = (int) ( $facets['total'] ?? 0 ); $cities = (array) ( $facets['cities'] ?? array() );
		$links = '';
		foreach ( array_slice( $cities, 0, 14 ) as $c ) { $links .= '<a href="' . esc_url( nadlan_cp_city_hub_url( $c['name'] ) ) . '">פרויקטים חדשים ב' . esc_html( $c['name'] ) . ' <i>' . (int) $c['n'] . '</i></a>'; }
		ob_start(); ?>
<section class="nlcp-body" aria-label="על פרויקטים חדשים בישראל">
	<div class="nlcp-prose">
		<h2>פרויקטים חדשים בישראל: מה יש בקטלוג</h2>
		<p>הקטלוג מרכז <?php echo number_format( $total ); ?> פרויקטים חדשים למגורים ב־<?php echo count( $cities ); ?> ערים: בנייה חדשה על מגרשים פנויים, פינוי בינוי ותמ"א 38. לכל פרויקט חדש כרטיס אחד עם הנתונים שידועים: עיר ושכונה, יזם, סטטוס, מספר יחידות הדיור, קומות ומועד אכלוס משוער, ולצדם מחיר למ"ר בסביבה לפי עסקאות שדווחו לרשות המסים. מה שלא ידוע לא מופיע.</p>
		<p>מחפשים דירות חדשות מקבלן בתל אביב, בירושלים, בחיפה או בבאר שבע? מסננים לפי עיר, סוג פרויקט, סטטוס וגודל, או לוחצים "קרוב אליי" ומקבלים את הפרויקטים החדשים באזור שלכם. כל כרטיס מוביל לעמוד הפרויקט עם בחירת דירה על הבניין, סיור וקשר ישיר ליזם.</p>
		<h2>דירה חדשה מקבלן: מה בודקים לפני שחותמים</h2>
		<ul>
			<li><strong>הקבלן רשום</strong> בפנקס הקבלנים ובסיווג המתאים לגובה הבניין. הקטלוג מסמן פרויקטים שאומתו מול הרשם.</li>
			<li><strong>היתר בנייה בתוקף</strong> ולא רק תכנית מאושרת. פרויקט על הנייר הוא הזדמנות, אבל גם סיכון של זמן.</li>
			<li><strong>ערבות חוק המכר</strong> על כל תשלום, ולוח תשלומים שנפרס לפי קצב הבנייה.</li>
			<li><strong>מפרט טכני מלא</strong>: ריצוף, מטבח, מיזוג, ממ"ד, חניה ומחסן. מה כלול ומה בתוספת.</li>
			<li><strong>מועד מסירה ופיצוי</strong> על איחור, כתובים בחוזה.</li>
			<li><strong>מחירי הסביבה</strong>: כמה עלו דירות דומות ברחוב ובעיר ב־24 החודשים האחרונים. הנתון מופיע בכל כרטיס בקטלוג.</li>
		</ul>
		<p>המדריך המלא: <a href="<?php echo esc_url( home_url( '/buying-new-apartment-developer-2026-negotiation/' ) ); ?>">איך קונים דירה חדשה מקבלן ב־2026: משא ומתן, מפרט וחוזה</a>. ולפני הפגישה עם היזם: <a href="<?php echo esc_url( home_url( '/buying-apartment/' ) ); ?>">מדריך קניית דירה</a> ו<a href="<?php echo esc_url( home_url( '/purchase-tax-calculator/' ) ); ?>">מחשבון מס רכישה</a>.</p>
		<h2>בנייה חדשה, פינוי בינוי ותמ"א 38: מה ההבדל לקונה</h2>
		<p><strong>בנייה חדשה</strong> היא פרויקט על מגרש פנוי, בדרך כלל בשכונה חדשה או ברובע מתפתח. לוח הזמנים ברור יחסית ואפשר לבחור דירה על הבניין מהשלב הראשון. <strong>פינוי בינוי</strong> הורס בניינים ישנים ובונה מתחם שלם במקומם: הרבה יחידות דיור, שכונה קיימת עם שירותים, ולוח זמנים שתלוי בהסכמות דיירים ובאישורים. <strong>תמ"א 38</strong> מחזקת או הורסת ובונה בניין בודד, ומוסיפה דירות חדשות מקבלן בלב שכונה ותיקה. בקטלוג כל פרויקט מסומן לפי הסוג שלו, ואפשר לסנן. למי שגר בבניין ישן: <a href="<?php echo esc_url( home_url( '/urban-renewal/' ) ); ?>">המדריך להתחדשות עירונית</a>.</p>
		<h2>מחירי דירות חדשות לפי עיר</h2>
		<p>הטבלה מציגה את מחיר המ"ר החציוני של דירות בבתי קומות בערים המובילות בקטלוג, לפי עסקאות שדווחו לרשות המסים, ולצדו כמה פרויקטים חדשים יש בכל עיר. זה קנה המידה שכדאי להחזיק ביד לפני שפותחים משא ומתן על דירה חדשה מקבלן.</p>
		<?php echo nadlan_cp_price_table( $facets ); // phpcs:ignore WordPress.Security.EscapeOutput ?>
		<h2>פרויקטים חדשים לפי עיר</h2>
		<div class="nlcp-citylinks"><?php echo $links; // phpcs:ignore WordPress.Security.EscapeOutput ?></div>
		<h2>שאלות על פרויקטים חדשים ודירות מקבלן</h2>
		<div class="nlcp-faq">
			<?php foreach ( nadlan_cp_faq() as $qa ) : ?>
			<details><summary><?php echo esc_html( $qa[0] ); ?></summary><p><?php echo esc_html( $qa[1] ); ?></p></details>
			<?php endforeach; ?>
		</div>
	</div>
</section>
		<?php
		return ob_get_clean();
	}
}
if ( ! function_exists( 'nadlan_cp_sidebar_html' ) ) {
	function nadlan_cp_sidebar_html( $facets ) {
		$d = nadlan_cp_data(); if ( empty( $d['cities'] ) ) { return ''; }
		$rows = array(); $max = 0;
		foreach ( array_slice( (array) ( $facets['cities'] ?? array() ), 0, 40 ) as $c ) {
			$row = nadlan_cp_city_data( $c['name'] ); if ( ! $row || empty( $row['psqm_all'] ) ) { continue; }
			$rows[] = array( 'city' => $c['name'], 'psqm' => (int) $row['psqm_all'], 'n' => (int) $c['n'] ); $max = max( $max, (int) $row['psqm_all'] );
			if ( count( $rows ) >= 12 ) { break; }
		}
		if ( ! $rows ) { return ''; }
		usort( $rows, function ( $a, $b ) { return $b['psqm'] - $a['psqm']; } );
		$h = '<div class="nldir-fgroup nlcp-pricemap"><h4>מפת מחירים: ₪ למ"ר לפי עיר</h4><ul>';
		foreach ( $rows as $r ) {
			$w = max( 8, round( $r['psqm'] / $max * 100 ) );
			$h .= '<li><button type="button" class="nlcp-pm" data-city="' . esc_attr( $r['city'] ) . '" title="הצגת ' . esc_attr( $r['n'] ) . ' פרויקטים חדשים ב' . esc_attr( $r['city'] ) . '"><span class="nlcp-pm__c">' . esc_html( $r['city'] ) . '</span><span class="nlcp-pm__bar"><i style="width:' . $w . '%"></i></span><span class="nlcp-pm__v">' . esc_html( number_format( $r['psqm'] ) ) . '</span></button></li>';
		}
		$h .= '</ul><p class="nlcp-src">חציון עסקאות, רשות המסים. לחיצה על עיר מסננת את הקטלוג.</p></div>';
		return $h;
	}
}
if ( ! function_exists( 'nadlan_cp_schema' ) ) {
	function nadlan_cp_schema( $facets ) {
		$items = array();
		if ( function_exists( 'nadlan_dir_project_query' ) ) {
			$wq = nadlan_dir_project_query( array( 'per_page' => 24, 'paged' => 1, 'sort' => 'featured' ) );
			$i = 0;
			foreach ( (array) $wq->posts as $p ) {
				$i++; $it = array( '@type' => 'ListItem', 'position' => $i, 'url' => get_permalink( $p ), 'name' => get_the_title( $p ) );
				$img = get_the_post_thumbnail_url( $p, 'large' ); if ( $img ) { $it['image'] = $img; }
				$items[] = $it;
			}
			wp_reset_postdata();
		}
		$g = array();
		if ( $items ) { $g[] = array( '@type' => 'ItemList', 'name' => 'פרויקטים חדשים בישראל', 'numberOfItems' => (int) ( $facets['total'] ?? count( $items ) ), 'itemListOrder' => 'https://schema.org/ItemListOrderDescending', 'itemListElement' => $items ); }
		$faq = array(); foreach ( nadlan_cp_faq() as $qa ) { $faq[] = array( '@type' => 'Question', 'name' => $qa[0], 'acceptedAnswer' => array( '@type' => 'Answer', 'text' => $qa[1] ) ); }
		$g[] = array( '@type' => 'FAQPage', 'mainEntity' => $faq );
		return '<script type="application/ld+json" class="nlcp-schema">' . wp_json_encode( array( '@context' => 'https://schema.org', '@graph' => $g ), JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES ) . '</script>';
	}
}

/* ------------------------------------------------------------------ search bar (Booking style) */
if ( ! function_exists( 'nadlan_cp_searchbar_html' ) ) {
	function nadlan_cp_searchbar_html( $facets ) {
		$cities = array_slice( (array) ( $facets['cities'] ?? array() ), 0, 40 );
		$types = function_exists( 'nadlan_dir_project_types' ) ? nadlan_dir_project_types() : array();
		ob_start(); ?>
<form class="nlcp-bar" id="nlcp-bar" role="search" aria-label="חיפוש פרויקטים חדשים">
	<label class="nlcp-f nlcp-f--q"><span>פרויקט או יזם</span><input type="search" name="q" placeholder="שם פרויקט, יזם או רחוב" autocomplete="off"></label>
	<label class="nlcp-f nlcp-f--city"><span>עיר</span><select name="city"><option value="">כל הערים</option><?php foreach ( $cities as $c ) : ?><option value="<?php echo esc_attr( $c['name'] ); ?>"><?php echo esc_html( $c['name'] ); ?> (<?php echo (int) $c['n']; ?>)</option><?php endforeach; ?></select></label>
	<label class="nlcp-f"><span>סטטוס</span><select name="status"><option value="">כל הסטטוסים</option><?php foreach ( nadlan_cp_status_groups() as $k => $g ) : ?><option value="<?php echo esc_attr( $k ); ?>"><?php echo esc_html( $g['label'] ); ?></option><?php endforeach; ?></select></label>
	<label class="nlcp-f"><span>סוג</span><select name="project_type"><option value="">כל הסוגים</option><?php foreach ( $types as $k => $t ) : if ( 'other' === $k ) { continue; } ?><option value="<?php echo esc_attr( $k ); ?>"><?php echo esc_html( $t['label'] ); ?></option><?php endforeach; ?></select></label>
	<label class="nlcp-f"><span>גודל</span><select name="min_units"><option value="">כל הגדלים</option><option value="20">מ־20 יח"ד</option><option value="50">מ־50 יח"ד</option><option value="100">מ־100 יח"ד</option><option value="300">מ־300 יח"ד</option></select></label>
	<label class="nlcp-f"><span>מיון</span><select name="sort"><option value="featured">מומלצים</option><option value="units">הכי הרבה יח"ד</option><option value="newest">חדש בקטלוג</option><option value="name">א׳ עד ת׳</option></select></label>
	<button type="button" class="nlcp-near" id="nlcp-near"><svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><circle cx="12" cy="12" r="3"/><path d="M12 2v3M12 19v3M2 12h3M19 12h3"/></svg>קרוב אליי</button>
	<button type="submit" class="nlcp-go">הצגת פרויקטים</button>
</form>
		<?php
		return ob_get_clean();
	}
}

/* ------------------------------------------------------------------ CSS + JS (printed once on the catalog) */
if ( ! function_exists( 'nadlan_cp_assets' ) ) {
	function nadlan_cp_assets() {
		$coords = wp_json_encode( nadlan_cp_city_coords(), JSON_UNESCAPED_UNICODE );
		$rest = esc_url( rest_url( 'nadlan/v1/projects-plus' ) );
		return <<<HTML
<style id="nlcp-css">
.nlcp-card{display:flex;flex-direction:column;gap:0;min-width:0}
.nlcp-card>.nldc{flex:1 1 auto;border-bottom-left-radius:0!important;border-bottom-right-radius:0!important}
.nlcp-card .nldcp-name{white-space:normal!important;overflow:visible!important;text-overflow:clip!important;display:-webkit-box!important;-webkit-line-clamp:2;-webkit-box-orient:vertical;line-height:1.25!important}
.nlcp-card .nldcp-stats dd{white-space:normal!important;overflow:visible!important;text-overflow:clip!important}
.nlcp-facts{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:6px 12px;margin:0 0 10px;padding:10px 0 0;border-top:1px dashed var(--sa-line,#E3E1DA)}
.nlcp-facts div{min-width:0}.nlcp-facts dt{font-size:11px;color:var(--sa-mute,#6B7680);margin:0}.nlcp-facts dd{margin:0;font-size:13px;font-weight:600;color:var(--sa-ink,#14212B);overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.nlcp-ctx{display:grid;grid-template-columns:auto 1fr;gap:2px 8px;align-items:start;margin:0 0 10px;padding:9px 10px;background:var(--sa-sand,#EEE9DD);border-radius:10px;font-size:12.5px;line-height:1.35;color:var(--sa-ink2,#3B4753)}
.nlcp-ctx__k{grid-row:1/3;width:22px;height:22px;border-radius:50%;background:var(--sa-deep,#1F4B5C);color:#fff;display:grid;place-items:center;font-weight:700;font-size:12px}
.nlcp-ctx b{color:var(--sa-ink,#14212B)}.nlcp-ctx small{grid-column:2;color:var(--sa-mute,#6B7680);font-size:11px}
.nlcp-more{background:var(--sa-surf,#fff);border:1px solid var(--sa-line,#E3E1DA);border-top:0;border-radius:0 0 16px 16px;margin-top:-1px}
.nlcp-more summary{list-style:none;cursor:pointer;display:flex;justify-content:space-between;align-items:center;padding:9px 16px;font-size:13px;font-weight:700;color:var(--sa-sea,#2F6F86)}
.nlcp-more summary::-webkit-details-marker{display:none}.nlcp-more summary i{font-style:normal;font-size:16px;line-height:1}
.nlcp-more[open] summary i{transform:rotate(45deg)}
.nlcp-more__in{padding:4px 16px 14px}.nlcp-more__in dl{margin:0;display:grid;gap:6px}.nlcp-more__in dl div{display:flex;justify-content:space-between;gap:10px;font-size:12.5px;border-bottom:1px dotted var(--sa-line,#E3E1DA);padding-bottom:4px}
.nlcp-more__in dt{color:var(--sa-mute,#6B7680);flex:0 0 auto}.nlcp-more__in dd{margin:0;text-align:left;color:var(--sa-ink,#14212B);font-weight:600}
.nlcp-more__go{display:inline-block;margin-top:10px;font-weight:700;color:var(--sa-sea,#2F6F86)}
.nlcp-src{font-size:11.5px;color:var(--sa-mute,#6B7680);margin:8px 0 0;line-height:1.4}
.nldir[data-mode="projects"] .nldir-hero>form.nldir-search{display:none!important}
.nlcp-f input{font:inherit;font-size:14px;padding:9px 10px;border:1px solid var(--sa-line,#E3E1DA);border-radius:9px;background:#fff;color:var(--sa-ink,#14212B);min-width:0;max-width:100%}
@media(max-width:900px){.nldir[data-mode="projects"] .nldir-body{display:flex!important;flex-direction:column!important}.nldir[data-mode="projects"] .nldir-side{order:2!important}.nldir[data-mode="projects"] .nldir-main{order:1!important}.nlcp-pricemap ul{max-height:260px;overflow:auto}}
.nlcp-bar{display:grid;grid-template-columns:1.4fr 1.2fr 1fr 1fr 1fr 1fr auto auto;gap:8px;align-items:end;max-width:1180px;margin:14px auto 0;padding:12px;background:var(--sa-surf,#fff);border:1px solid var(--sa-line,#E3E1DA);border-radius:14px;box-shadow:0 12px 30px rgba(20,33,43,.06);text-align:start}
.nlcp-f{display:flex;flex-direction:column;gap:4px;min-width:0}.nlcp-f span{font-size:11px;color:var(--sa-mute,#6B7680);font-weight:600}
.nlcp-f select{font:inherit;font-size:14px;padding:9px 10px;border:1px solid var(--sa-line,#E3E1DA);border-radius:9px;background:#fff;color:var(--sa-ink,#14212B);min-width:0;max-width:100%}
.nlcp-near,.nlcp-go{font:inherit;font-weight:700;font-size:14px;border-radius:999px;padding:10px 16px;cursor:pointer;white-space:nowrap;display:inline-flex;align-items:center;gap:6px}
.nlcp-near{background:#fff;border:1px solid var(--sa-line,#E3E1DA);color:var(--sa-deep,#1F4B5C)}.nlcp-near.is-busy{opacity:.6}
.nlcp-go{background:var(--sa-sea,#2F6F86);border:0;color:#fff}
.nlcp-note{max-width:1180px;margin:8px auto 0;font-size:12.5px;color:var(--sa-mute,#6B7680);text-align:start;min-height:1em}
@media(max-width:1000px){.nlcp-bar{grid-template-columns:1fr 1fr 1fr}.nlcp-f--q{grid-column:1/-1}}
@media(max-width:560px){.nlcp-bar{grid-template-columns:1fr 1fr}.nlcp-f--q,.nlcp-go{grid-column:1/-1}}
.nlcp-pricemap ul{list-style:none;margin:0;padding:0;display:grid;gap:6px}
.nlcp-pm{width:100%;display:grid;grid-template-columns:1fr 70px auto;gap:8px;align-items:center;background:#fff;border:1px solid var(--sa-line,#E3E1DA);border-radius:10px;padding:7px 10px;font:inherit;font-size:12.5px;cursor:pointer;text-align:start;color:var(--sa-ink,#14212B)}
.nlcp-pm:hover{border-color:var(--sa-sea,#2F6F86)}.nlcp-pm.is-on{background:var(--sa-deep,#1F4B5C);color:#fff}
.nlcp-pm__bar{height:6px;background:var(--sa-sand,#EEE9DD);border-radius:3px;overflow:hidden}.nlcp-pm__bar i{display:block;height:100%;background:var(--sa-sea,#2F6F86)}
.nlcp-pm__v{font-variant-numeric:tabular-nums;font-weight:700;font-size:12px}
.nlcp-mapcard{margin-bottom:14px}.nlcp-mapcard .nldrone{margin:0!important;padding:0!important}
.nlcp-mapcard .nldrone-toggle{width:100%;justify-content:space-between}
.nldrone-stage.nlcp-overlay{position:fixed!important;top:4vh!important;bottom:4vh!important;left:3vw!important;right:3vw!important;width:auto!important;max-width:none!important;z-index:9999;background:#fff;border-radius:18px;box-shadow:0 30px 80px rgba(0,0,0,.35);padding:56px 14px 14px;display:flex!important;flex-direction:column;margin:0!important}
.nldrone-stage.nlcp-overlay .nldrone-map{flex:1;height:auto!important;min-height:60vh;width:100%!important;max-width:none!important}
.nlcp-mapclose{position:fixed;top:calc(4vh + 10px);inset-inline-start:calc(3vw + 10px);z-index:10000;border:0;border-radius:999px;background:var(--sa-deep,#1F4B5C);color:#fff;font:inherit;font-weight:700;padding:8px 14px;cursor:pointer;display:none}
.nlcp-mapclose.is-on{display:block}
.nlcp-body{max-width:1240px;margin:36px auto 10px;padding:0 4px}
.nlcp-prose{background:var(--sa-surf,#fff);border:1px solid var(--sa-line,#E3E1DA);border-radius:22px;padding:clamp(18px,3vw,36px)}
.nlcp-prose h2{font-family:var(--sa-serif,'Noto Serif Hebrew',serif);font-size:clamp(20px,2.2vw,26px);margin:26px 0 10px;color:var(--sa-ink,#14212B)}
.nlcp-prose h2:first-child{margin-top:0}.nlcp-prose p,.nlcp-prose li{font-size:15.5px;line-height:1.7;color:var(--sa-ink2,#3B4753)}
.nlcp-prose ul{padding-inline-start:20px}.nlcp-prose a{color:var(--sa-sea,#2F6F86);font-weight:600}
.nlcp-tablewrap{overflow-x:auto}@media(max-width:640px){.nlcp-table th,.nlcp-table td{white-space:normal;padding:7px 6px;font-size:12.5px}}.nlcp-table{width:100%;border-collapse:collapse;font-size:14px}.nlcp-table th,.nlcp-table td{padding:9px 10px;border-bottom:1px solid var(--sa-line,#E3E1DA);text-align:start;white-space:nowrap}
.nlcp-table th{font-size:12px;color:var(--sa-mute,#6B7680);font-weight:600}.nlcp-table td:nth-child(n+2){font-variant-numeric:tabular-nums}
.nlcp-citylinks{display:flex;flex-wrap:wrap;gap:8px}.nlcp-citylinks a{border:1px solid var(--sa-line,#E3E1DA);border-radius:999px;padding:7px 12px;font-size:13.5px;text-decoration:none;background:#fff}.nlcp-citylinks a i{font-style:normal;color:var(--sa-mute,#6B7680);font-size:12px;margin-inline-start:4px}
.nlcp-faq details{border-bottom:1px solid var(--sa-line,#E3E1DA);padding:10px 0}.nlcp-faq summary{cursor:pointer;font-weight:700;font-size:15.5px;color:var(--sa-ink,#14212B)}.nlcp-faq p{margin:8px 0 0}
</style>
<script id="nlcp-js">
(function(){
	var root=document.querySelector('.nldir[data-mode="projects"]');if(!root)return;
	var REST='$rest',COORDS=$coords;
	var results=root.querySelector('#nldir-results'),totalEl=root.querySelector('#nldir-total'),moreBtn=root.querySelector('#nldir-more');
	var bar=document.getElementById('nlcp-bar'),note=document.getElementById('nlcp-note');
	var st={q:'',city:'',status:'',project_type:'',min_units:'',sort:'featured',paged:1},req=0;
	var FIELDS=['q','city','status','project_type','min_units','sort'];
	try{var p0=new URLSearchParams(location.search);['city','status','project_type','min_units','sort','q'].forEach(function(k){if(p0.get(k))st[k]=p0.get(k);});}catch(e){}
	function sync(){if(!bar)return;FIELDS.forEach(function(k){var el=bar.elements[k];if(el)el.value=st[k]||(k==='sort'?'featured':'');});document.querySelectorAll('.nlcp-pm').forEach(function(b){b.classList.toggle('is-on',b.dataset.city===st.city);});}
	function url(){var p=new URLSearchParams();Object.keys(st).forEach(function(k){if(st[k]&&!(k==='sort'&&st[k]==='featured')&&k!=='paged')p.set(k,st[k]);});history.replaceState(null,'',location.pathname+(p.toString()?'?'+p:''));}
	function load(append){var my=++req;results.classList.add('is-loading');var p=new URLSearchParams();Object.keys(st).forEach(function(k){if(st[k])p.set(k,st[k]);});p.set('per_page','24');
		fetch(REST+'?'+p.toString(),{headers:{Accept:'application/json'}}).then(function(r){return r.json();}).then(function(d){if(my!==req)return;results.classList.remove('is-loading');if(!d||!d.ok)return;
			if(append)results.insertAdjacentHTML('beforeend',d.html);else results.innerHTML=d.html;
			if(totalEl)totalEl.textContent=Number(d.total).toLocaleString('he-IL');if(moreBtn)moreBtn.style.display=(d.paged<d.pages)?'':'none';
			if(!append){var y=results.getBoundingClientRect().top+window.scrollY-120;if(window.scrollY>y+200||document.activeElement&&document.activeElement.closest('#nlcp-bar'))window.scrollTo({top:y,behavior:'smooth'});}
		}).catch(function(){results.classList.remove('is-loading');});}
	if(bar){bar.addEventListener('submit',function(e){e.preventDefault();FIELDS.forEach(function(k){st[k]=bar.elements[k].value.trim();});st.paged=1;url();sync();load(false);});
		bar.addEventListener('change',function(e){if(e.target.tagName==='SELECT'){st[e.target.name]=e.target.value;st.paged=1;url();sync();load(false);}});}
	document.querySelectorAll('.nlcp-pm').forEach(function(b){b.addEventListener('click',function(){st.city=(st.city===b.dataset.city)?'':b.dataset.city;st.paged=1;url();sync();load(false);});});
	var near=document.getElementById('nlcp-near');
	if(near){near.addEventListener('click',function(){if(!navigator.geolocation){if(note)note.textContent='הדפדפן לא משתף מיקום. בחרו עיר מהרשימה.';return;}near.classList.add('is-busy');if(note)note.textContent='מאתרים את העיר הקרובה אליכם...';
		navigator.geolocation.getCurrentPosition(function(pos){near.classList.remove('is-busy');var la=pos.coords.latitude,lo=pos.coords.longitude,best=null,bd=1e9;Object.keys(COORDS).forEach(function(c){var d=Math.hypot((COORDS[c][0]-la)*111,(COORDS[c][1]-lo)*94);if(d<bd){bd=d;best=c;}});
			if(!best)return;var opt=bar&&Array.prototype.find.call(bar.elements.city.options,function(o){return o.value===best||o.value.indexOf(best)===0||best.indexOf(o.value)===0;});st.city=opt?opt.value:best;st.paged=1;url();sync();load(false);if(note)note.textContent='פרויקטים חדשים ב'+st.city+', כ־'+Math.round(bd)+' ק"מ מכם.';},
			function(){near.classList.remove('is-busy');if(note)note.textContent='לא התקבל מיקום. בחרו עיר מהרשימה.';},{timeout:8000,maximumAge:600000});});}
	var drone=document.querySelector('.nlcp-mapcard .nldrone');
	if(drone){var stage=drone.querySelector('.nldrone-stage'),tog=drone.querySelector('.nldrone-toggle');var close=document.createElement('button');close.type='button';close.className='nlcp-mapclose';close.textContent='סגירת המפה';document.body.appendChild(close);
		var home=stage&&stage.parentNode,homeNext=stage&&stage.nextSibling;
		var obs=new MutationObserver(function(){var open=stage&&!stage.hasAttribute('hidden');close.classList.toggle('is-on',!!open);document.body.style.overflow=open?'hidden':'';
			if(open&&stage.parentNode!==document.body){stage.classList.add('nlcp-overlay');document.body.appendChild(stage);window.dispatchEvent(new Event('resize'));}
			else if(!open&&stage.parentNode===document.body&&home){stage.classList.remove('nlcp-overlay');home.insertBefore(stage,homeNext&&homeNext.parentNode===home?homeNext:null);}});if(stage)obs.observe(stage,{attributes:true,attributeFilter:['hidden']});
		close.addEventListener('click',function(){if(tog)tog.click();else if(stage)stage.setAttribute('hidden','');});}
	sync();
})();
</script>
HTML;
	}
}

/* ------------------------------------------------------------------ output buffering on the catalog: inject everything, edit nothing */
add_action( 'template_redirect', function () {
	if ( ! nadlan_cp_is_catalog() ) { return; }
	/* everything that touches the database happens here, before output; the buffer callback only moves strings and never fails closed */
	$pre = array( 'bar' => '', 'side' => '', 'body' => '', 'tail' => '' );
	try {
		$facets = function_exists( 'nadlan_dir_project_facets' ) ? nadlan_dir_project_facets() : array();
		$thumb = function_exists( 'nadlan_cp_map_thumb_html' ) ? nadlan_cp_map_thumb_html() : '';
		$pre['bar']  = '<div class="nlcp-herogrid">' . nadlan_cp_searchbar_html( $facets ) . $thumb . '</div><p class="nlcp-note" id="nlcp-note" aria-live="polite"></p>';
		$pre['side'] = nadlan_cp_sidebar_html( $facets );
		$pre['body'] = nadlan_cp_body_html( $facets );
		$pre['tail'] = nadlan_cp_assets() . ( function_exists( 'nadlan_cp_map_shell_html' ) ? nadlan_cp_map_shell_html() . nadlan_cp_map_assets( $facets ) : '' ) . nadlan_cp_schema( $facets );
	} catch ( \Throwable $e ) { return; }
	ob_start( function ( $html ) use ( $pre ) {
		try {
			if ( ! is_string( $html ) || false === strpos( $html, 'data-mode="projects"' ) ) { return $html; }
			$h = nadlan_cp_enrich_cards( $html );
			$h = str_replace( 'data-rest="' . esc_url( rest_url( 'nadlan/v1/projects' ) ) . '"', 'data-rest="' . esc_url( rest_url( 'nadlan/v1/projects-plus' ) ) . '"', $h );
			/* search bar: right after the pills, before the hero closes */
			$p = strpos( $h, '<div class="nldir-pills">' );
			if ( false !== $p ) { $q = strpos( $h, '</header>', $p ); if ( false !== $q ) { $h = substr( $h, 0, $q ) . $pre['bar'] . substr( $h, $q ); } }
			/* drone band out of the flow into the sidebar */
			$drone = ''; $a = strpos( $h, '<section class="nldrone nldrone--toggle"' );
			if ( false !== $a ) {
				$b = strpos( $h, '</section>', $a );
				if ( false !== $b ) {
					$b += 10;
					/* the band prints its own <style> and <script> right after; carry them along */
					foreach ( array( '<style>', '<script>' ) as $tag ) {
						$t = strpos( $h, $tag, $b );
						if ( false !== $t && $t - $b < 40 ) { $close = strpos( $h, '</' . substr( $tag, 1 ), $t ); if ( false !== $close ) { $b = $close + strlen( $tag ) + 1; } }
					}
					$drone = substr( $h, $a, $b - $a ); $h = substr( $h, 0, $a ) . substr( $h, $b );
				}
			}
			$side = $pre['side']; /* the drone band is retired on the catalog: the new map (thumbnail + full map) replaces it */
			$s = strpos( $h, '<aside class="nldir-side">' );
			if ( $side && false !== $s ) { $s += strlen( '<aside class="nldir-side">' ); $h = substr( $h, 0, $s ) . $side . substr( $h, $s ); }
			/* body copy below the results */
			$j = strpos( $h, '<script id="nldir-js">' );
			if ( false !== $j ) { $h = substr( $h, 0, $j ) . $pre['body'] . substr( $h, $j ); }
			$k = strrpos( $h, '</body>' );
			if ( false !== $k ) { $h = substr( $h, 0, $k ) . $pre['tail'] . substr( $h, $k ); }
			return $h;
		} catch ( \Throwable $e ) { return $html; }
	} );
}, 1 );


/* ------------------------------------------------------------------ project pages: the same price context under the lead paragraph */
if ( ! function_exists( 'nadlan_cp_project_ctx_html' ) ) {
	function nadlan_cp_project_ctx_html( $id ) {
		$ctx = nadlan_cp_context( $id ); $row = $ctx['row'];
		if ( ! $row || empty( $row['psqm_all'] ) ) { return ''; }
		$city = $ctx['city'];
		$tiles = array( array( 'מחיר למ"ר ב' . $city, nadlan_cp_nis( $row['psqm_all'] ), number_format( (int) $row['deals_24m'] ) . ' עסקאות' ) );
		if ( ! empty( $ctx['street']['psqm'] ) ) { $tiles[] = array( 'ברחוב ' . $ctx['street']['name'], nadlan_cp_nis( $ctx['street']['psqm'] ), (int) $ctx['street']['n'] . ' עסקאות' ); }
		if ( $ctx['own'] > 5000 ) { $tiles[] = array( 'בפרויקט, לפי היזם', nadlan_cp_nis( $ctx['own'] ) . ' למ"ר', 'לא מחייב' ); }
		foreach ( array( '3', '4', '5' ) as $r ) { if ( ! empty( $row['price_by_rooms'][ $r ] ) && count( $tiles ) < 5 ) { $tiles[] = array( 'דירת ' . $r . ' חדרים ב' . $city . ', חציון', nadlan_cp_nis( $row['price_by_rooms'][ $r ] ), 'יד שנייה וחדש' ); } }
		$years = ''; if ( ! empty( $row['psqm_by_year'] ) ) { $ys = array_filter( $row['psqm_by_year'] ); if ( count( $ys ) >= 3 ) { $first = reset( $ys ); $last = end( $ys ); $k = array_keys( $ys ); $chg = $first ? round( ( $last / $first - 1 ) * 100 ) : null; if ( null !== $chg ) { $years = 'מ־' . $k[0] . ' עד ' . end( $k ) . ': ' . ( $chg >= 0 ? '+' : '' ) . $chg . '% במחיר למ"ר בעיר.'; } } }
		$h  = '<aside class="nlcp-projctx" dir="rtl" aria-label="מחירי הסביבה"><div class="nlcp-projctx__head"><span class="nlcp-projctx__k">מחירי הסביבה</span><h2>כמה עולה דירה ב' . esc_html( $city ) . '?</h2><p>עסקאות שדווחו לרשות המסים, ' . esc_html( nadlan_cp_period( $row ) ) . '. חציון של דירות בבתי קומות. ' . esc_html( $years ) . '</p></div><div class="nlcp-projctx__tiles">';
		foreach ( $tiles as $t ) { $h .= '<div class="nlcp-tile"><small>' . esc_html( $t[0] ) . '</small><b>' . esc_html( $t[1] ) . '</b><span>' . esc_html( $t[2] ) . '</span></div>'; }
		$h .= '</div><p class="nlcp-src">המחירים הם של הסביבה, לא של הדירות בפרויקט. מחיר הדירה נקבע מול היזם. <a href="' . esc_url( nadlan_cp_city_hub_url( (string) get_post_meta( $id, 'city', true ) ) ) . '">עוד פרויקטים חדשים ב' . esc_html( $city ) . '</a> · <a href="' . esc_url( home_url( '/projects/' ) ) . '">כל הפרויקטים החדשים</a></p></aside>';
		$h .= '<style>.nlcp-projctx{max-width:1180px;margin:18px auto 22px;padding:20px clamp(16px,2.5vw,28px);background:var(--sa-surf,#fff);border:1px solid var(--sa-line,#E3E1DA);border-radius:18px}.nlcp-projctx__k{display:inline-block;font-size:11.5px;font-weight:700;letter-spacing:.08em;color:var(--sa-sea,#2F6F86);margin-bottom:6px}.nlcp-projctx h2{margin:0 0 6px;font-family:var(--sa-serif,"Noto Serif Hebrew",serif);font-size:clamp(20px,2.2vw,26px);color:var(--sa-ink,#14212B)}.nlcp-projctx__head p{margin:0 0 14px;color:var(--sa-ink2,#3B4753);font-size:14.5px;line-height:1.55}.nlcp-projctx__tiles{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:10px}.nlcp-tile{background:var(--sa-sand,#EEE9DD);border-radius:12px;padding:12px 14px;display:flex;flex-direction:column;gap:3px}.nlcp-tile small{font-size:12px;color:var(--sa-ink2,#3B4753)}.nlcp-tile b{font-size:20px;color:var(--sa-ink,#14212B);font-variant-numeric:tabular-nums}.nlcp-tile span{font-size:11.5px;color:var(--sa-mute,#6B7680)}.nlcp-projctx .nlcp-src{font-size:12px;color:var(--sa-mute,#6B7680);margin-top:12px}.nlcp-projctx .nlcp-src a{color:var(--sa-sea,#2F6F86);font-weight:600}</style>';
		return $h;
	}
}
add_action( 'template_redirect', function () {
	if ( is_admin() || ! is_singular( 'nadlan_project' ) ) { return; }
	$id = get_queried_object_id(); if ( ! $id ) { return; }
	if ( get_post_meta( $id, '_nadlan_private_unit_journey', true ) ) { return; }
	$block = nadlan_cp_project_ctx_html( $id ) . ( function_exists( 'nadlan_cp_surroundings_html' ) ? nadlan_cp_surroundings_html( $id ) : '' ); if ( '' === $block ) { return; }
	ob_start( function ( $html ) use ( $block ) {
		try {
			if ( ! is_string( $html ) ) { return $html; }
			$a = strpos( $html, '<div class="nl-lead">' );
			if ( false === $a ) { return $html; }
			$b = strpos( $html, '</div>', $a ); if ( false === $b ) { return $html; }
			$b += 6;
			return substr( $html, 0, $b ) . $block . substr( $html, $b );
		} catch ( \Throwable $e ) { return $html; }
	} );
}, 1 );

/* healthcheck marker (read by the deploy verify) */
add_filter( 'nadlan_config_healthcheck', function ( $out ) { $out['catalog_plus'] = array( 'version' => '1.0', 'deals_cities' => count( (array) ( nadlan_cp_data()['cities'] ?? array() ) ) ); return $out; } );

/* x-catalog-plus · map v2 (6.9.2026, owner: "small square on top, click opens a real map centred where I am, prices on the pins, heat map")
 * Concatenated after catalog-plus.php by scripts/catalog-plus/deploycp.py. Additive; nothing here edits the drone map module.
 *  - Thumbnail: a Mapbox static image (light style) with HTML price chips projected onto it (Web Mercator, in JS). One <a>, one image.
 *  - Full map (opens on click, Mapbox GL loaded on demand): project pins as price pills (Booking pattern), clusters, mini card,
 *    heat: Tel Aviv neighborhoods choropleth (₪/sqm from Tax Authority deals) + city circles for the other 19 cities, "near me", pulse.
 *  - Project pages: "מה קורה מסביב" from find-place (schools, light rail, parks, active construction, plans) + a static mini map. */

if ( ! function_exists( 'nadlan_cp_mapbox_token' ) ) {
	function nadlan_cp_mapbox_token() { return trim( (string) get_option( 'nadlan_mapbox_token', '' ) ); }
}
if ( ! function_exists( 'nadlan_cp_uploads_url' ) ) {
	function nadlan_cp_uploads_url( $file ) { $up = wp_get_upload_dir(); return trailingslashit( $up['baseurl'] ) . 'nadlan-skin/' . $file; }
}
if ( ! function_exists( 'nadlan_cp_uploads_path' ) ) {
	function nadlan_cp_uploads_path( $file ) { $up = wp_get_upload_dir(); return trailingslashit( $up['basedir'] ) . 'nadlan-skin/' . $file; }
}
if ( ! function_exists( 'nadlan_cp_map_cities' ) ) {
	/** Cities with coordinates + ₪/sqm + project count: the data behind the thumbnail chips and the city heat circles. */
	function nadlan_cp_map_cities( $facets ) {
		$coords = nadlan_cp_city_coords(); $counts = array();
		foreach ( (array) ( $facets['cities'] ?? array() ) as $c ) { $counts[ nadlan_cp_city_key( $c['name'] ) ] = (int) $c['n']; }
		$out = array();
		foreach ( $coords as $name => $ll ) {
			$row = nadlan_cp_city_data( $name ); $n = $counts[ nadlan_cp_city_key( $name ) ] ?? 0;
			if ( ! $row && ! $n ) { continue; }
			$out[] = array( 'name' => $name, 'lat' => $ll[0], 'lng' => $ll[1], 'psqm' => $row ? (int) $row['psqm_all'] : 0, 'deals' => $row ? (int) $row['deals_24m'] : 0, 'period' => $row ? nadlan_cp_period( $row ) : '', 'n' => $n, 'url' => nadlan_cp_city_hub_url( $name ) );
		}
		usort( $out, function ( $a, $b ) { return $b['n'] - $a['n']; } );
		return $out;
	}
}
if ( ! function_exists( 'nadlan_cp_map_thumb_html' ) ) {
	function nadlan_cp_map_thumb_html() {
		$tok = nadlan_cp_mapbox_token(); if ( '' === $tok ) { return ''; }
		/* portrait crop of the whole country; chips are placed by JS from the same center/zoom */
		$src = 'https://api.mapbox.com/styles/v1/mapbox/light-v11/static/34.88,32.02,7.15,0/240x240@2x?access_token=' . rawurlencode( $tok ) . '&attribution=false&logo=false';
		return '<a class="nlcp-mapthumb" id="nlcp-mapthumb" href="#map" data-center="34.88,32.02" data-zoom="7.15" data-w="240" data-h="240" aria-label="פתיחת מפת הפרויקטים והמחירים">'
			. '<img src="' . esc_url( $src ) . '" alt="מפת פרויקטים חדשים ומחיר למ״ר לפי עיר" width="240" height="240" loading="eager" decoding="async" referrerpolicy="no-referrer-when-downgrade">'
			. '<span class="nlcp-mapthumb__chips" aria-hidden="true"></span>'
			. '<span class="nlcp-mapthumb__cta"><b>מפת מחירים ופרויקטים</b><small>מחיר למ״ר על כל פרויקט · לחיצה פותחת</small></span>'
			. '<span class="nlcp-mapthumb__near"><svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><circle cx="12" cy="12" r="3"/><path d="M12 2v3M12 19v3M2 12h3M19 12h3"/></svg>פרויקטים לידי</span></a>';
	}
}
if ( ! function_exists( 'nadlan_cp_map_shell_html' ) ) {
	function nadlan_cp_map_shell_html() {
		return '<div class="nlcp-map" id="nlcp-map" hidden role="dialog" aria-modal="true" aria-label="מפת הפרויקטים והמחירים">'
			. '<div class="nlcp-map__bar"><button type="button" class="nlcp-map__close" id="nlcp-map-close">סגירה</button>'
			. '<div class="nlcp-map__title"><b>מפת פרויקטים חדשים ומחירים</b><span id="nlcp-map-sub">מחיר למ״ר בסביבת כל פרויקט, לפי עסקאות שדווחו לרשות המסים</span></div>'
			. '<div class="nlcp-map__tools"><button type="button" class="nlcp-map__tool" id="nlcp-map-near">פרויקטים לידי</button>'
			. '<label class="nlcp-map__tool nlcp-map__toggle"><input type="checkbox" id="nlcp-map-heat" checked> מפת חום מחירים</label></div></div>'
			. '<div class="nlcp-map__stage" id="nlcp-map-stage"></div>'
			. '<div class="nlcp-map__legend" id="nlcp-map-legend"><span>₪ למ״ר</span><i style="background:#DCEBF0"></i><small>עד 20K</small><i style="background:#9CC4D1"></i><small>30K</small><i style="background:#5F98AB"></i><small>45K</small><i style="background:#2F6F86"></i><small>60K</small><i style="background:#1F4B5C"></i><small>70K+</small></div>'
			. '<aside class="nlcp-map__card" id="nlcp-map-card" hidden></aside></div>';
	}
}
if ( ! function_exists( 'nadlan_cp_map_assets' ) ) {
	function nadlan_cp_map_assets( $facets ) {
		$cities = wp_json_encode( nadlan_cp_map_cities( $facets ), JSON_UNESCAPED_UNICODE );
		$cfg = wp_json_encode( array(
			'token' => nadlan_cp_mapbox_token(), 'projects' => esc_url_raw( rest_url( 'nadlan/v1/project-map' ) ),
			'hoods' => file_exists( nadlan_cp_uploads_path( 'tlv-neighborhoods-psqm.geojson' ) ) ? nadlan_cp_uploads_url( 'tlv-neighborhoods-psqm.geojson' ) : '',
			'gl' => 'https://api.mapbox.com/mapbox-gl-js/v3.7.0/mapbox-gl.js', 'glcss' => 'https://api.mapbox.com/mapbox-gl-js/v3.7.0/mapbox-gl.css', 'rtl' => 'https://api.mapbox.com/mapbox-gl-js/plugins/mapbox-gl-rtl-text/v0.3.0/mapbox-gl-rtl-text.js',
		), JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES );
		return <<<HTML
<style id="nlcp-map-css">
.nlcp-herogrid{display:grid;grid-template-columns:minmax(0,1fr) 240px;gap:14px;max-width:1180px;margin:14px auto 0;align-items:stretch}
.nlcp-herogrid .nlcp-bar{margin:0}
.nlcp-herogrid{align-items:start}
.nlcp-mapthumb{position:relative;display:block;border-radius:14px;overflow:hidden;border:1px solid var(--sa-line,#E3E1DA);background:#EAF0F2;text-decoration:none;color:inherit;aspect-ratio:1/1;width:100%;box-shadow:0 12px 30px rgba(20,33,43,.06)}
.nlcp-mapthumb img{position:absolute;inset:0;width:100%;height:100%;object-fit:fill;display:block;filter:saturate(.85)}
.nlcp-mapthumb__chips{position:absolute;inset:0}
.nlcp-chip{position:absolute;transform:translate(-50%,-100%);background:var(--sa-deep,#1F4B5C);color:#fff;font-size:10.5px;font-weight:700;padding:2px 6px;border-radius:999px;white-space:nowrap;box-shadow:0 2px 6px rgba(0,0,0,.25);font-variant-numeric:tabular-nums}
.nlcp-chip::after{content:"";position:absolute;left:50%;bottom:-4px;width:6px;height:6px;background:inherit;transform:translateX(-50%) rotate(45deg)}
.nlcp-chip--hot{background:var(--sa-sea,#2F6F86)}
.nlcp-mapthumb__cta{position:absolute;inset-inline:10px;bottom:10px;background:rgba(255,255,255,.94);border-radius:10px;padding:8px 10px;display:flex;flex-direction:column;gap:1px}
.nlcp-mapthumb__cta b{font-size:13px;color:var(--sa-ink,#14212B)}.nlcp-mapthumb__cta small{font-size:11px;color:var(--sa-mute,#6B7680)}
.nlcp-mapthumb__near{position:absolute;top:10px;inset-inline-start:10px;background:var(--sa-sea,#2F6F86);color:#fff;font-size:11.5px;font-weight:700;padding:5px 9px;border-radius:999px;display:inline-flex;gap:5px;align-items:center}
.nlcp-mapthumb:hover img{filter:saturate(1)}
@media(max-width:1000px){.nlcp-herogrid{grid-template-columns:1fr}.nlcp-mapthumb{max-width:300px;margin:0 auto}}
.nlcp-map{position:fixed;inset:0;z-index:99999;background:#F7F6F2;display:flex;flex-direction:column}
.nlcp-map[hidden]{display:none}
.nlcp-map__bar{display:flex;align-items:center;gap:12px;padding:10px 14px;background:#fff;border-bottom:1px solid var(--sa-line,#E3E1DA);flex-wrap:wrap}
.nlcp-map__title{flex:1;min-width:200px;display:flex;flex-direction:column}.nlcp-map__title b{font-size:15px;color:var(--sa-ink,#14212B)}.nlcp-map__title span{font-size:12px;color:var(--sa-mute,#6B7680)}
.nlcp-map__close{border:0;border-radius:999px;background:var(--sa-deep,#1F4B5C);color:#fff;font:inherit;font-weight:700;padding:8px 14px;cursor:pointer}
.nlcp-map__tools{display:flex;gap:8px;align-items:center}
.nlcp-map__tool{border:1px solid var(--sa-line,#E3E1DA);background:#fff;border-radius:999px;padding:7px 12px;font:inherit;font-size:13px;font-weight:600;color:var(--sa-deep,#1F4B5C);cursor:pointer;display:inline-flex;align-items:center;gap:6px}
.nlcp-map__tool.is-busy{opacity:.6}
.nlcp-map__stage{flex:1;min-height:0}
.nlcp-map__legend{position:absolute;bottom:14px;inset-inline-start:14px;background:rgba(255,255,255,.95);border:1px solid var(--sa-line,#E3E1DA);border-radius:10px;padding:7px 10px;display:flex;align-items:center;gap:5px;font-size:11px;color:var(--sa-ink2,#3B4753)}
.nlcp-map__legend i{width:16px;height:10px;border-radius:2px;display:inline-block}.nlcp-map__legend span{font-weight:700;margin-inline-end:4px}
.nlcp-map__card{position:absolute;top:70px;inset-inline-end:14px;width:300px;max-width:calc(100vw - 28px);background:#fff;border:1px solid var(--sa-line,#E3E1DA);border-radius:14px;box-shadow:0 20px 50px rgba(0,0,0,.18);overflow:hidden;z-index:2}
.nlcp-map__card[hidden]{display:none}
.nlcp-map__card img{width:100%;height:150px;object-fit:cover;display:block}
.nlcp-map__card .in{padding:12px 14px}.nlcp-map__card h3{margin:0 0 4px;font-size:15px;line-height:1.3;color:var(--sa-ink,#14212B)}
.nlcp-map__card .meta{font-size:12.5px;color:var(--sa-ink2,#3B4753);display:flex;flex-wrap:wrap;gap:4px 10px;margin-bottom:8px}
.nlcp-map__card .ctx{background:var(--sa-sand,#EEE9DD);border-radius:9px;padding:8px 10px;font-size:12.5px;margin-bottom:10px}.nlcp-map__card .ctx b{color:var(--sa-ink,#14212B)}
.nlcp-map__card a.go{display:inline-block;background:var(--sa-sea,#2F6F86);color:#fff;border-radius:999px;padding:8px 14px;font-weight:700;font-size:13px;text-decoration:none}
.nlcp-map__card .x{position:absolute;top:8px;inset-inline-start:8px;border:0;border-radius:50%;width:28px;height:28px;background:rgba(255,255,255,.9);cursor:pointer;font-size:16px;line-height:1}
.mapboxgl-marker{width:auto!important;max-width:none!important}
.nlcp-pin{display:inline-block;width:max-content;max-width:none;background:var(--sa-deep,#1F4B5C);color:#fff;border-radius:999px;padding:3px 8px;font:700 12px/1.3 Assistant,Heebo,sans-serif;white-space:nowrap;box-shadow:0 3px 10px rgba(0,0,0,.28);cursor:pointer;font-variant-numeric:tabular-nums;border:2px solid #fff}
.mapboxgl-marker.nlcp-pin.is-dot{width:13px!important;min-width:13px;height:13px;padding:0;border-radius:50%;background:var(--sa-sea,#2F6F86)!important;border-color:#fff!important}.nlcp-pin.is-dot:hover{box-shadow:0 0 0 4px rgba(47,111,134,.25)}.nlcp-pin.is-dot::after{display:none}
/* escaping: Code Snippets strips one slash level, the PHP heredoc another; write \\n here to get 
 in JS. never set position on .nlcp-pin/.nlcp-cluster: Mapbox positions markers with position:absolute + transform; a relative pin lands hundreds of px off its coordinate */
.nlcp-pin::after{content:"";position:absolute;left:50%;bottom:-6px;width:8px;height:8px;background:var(--sa-deep,#1F4B5C);transform:translateX(-50%) rotate(45deg)}
.nlcp-pin.is-featured{background:var(--sa-sea,#2F6F86)}.nlcp-pin.is-featured::after{background:var(--sa-sea,#2F6F86)}
.nlcp-pin.is-city{background:#fff;color:var(--sa-deep,#1F4B5C);border-color:var(--sa-deep,#1F4B5C)}.nlcp-pin.is-city::after{background:#fff}
.nlcp-pin.is-active{background:#C2563A}.nlcp-pin.is-active::after{background:#C2563A}
.nlcp-pin.is-pulse::before{content:"";position:absolute;inset:-6px;border-radius:999px;border:2px solid var(--sa-sea,#2F6F86);animation:nlcpPulse 1.4s ease-out 3}
@keyframes nlcpPulse{0%{transform:scale(.9);opacity:.9}100%{transform:scale(1.8);opacity:0}}
@media(max-width:640px){.nlcp-map__bar{gap:8px;padding:8px 10px}.nlcp-map__close{order:0;padding:7px 12px;font-size:13px}.nlcp-map__tools{order:1;margin-inline-start:auto}.nlcp-map__tool{padding:6px 9px;font-size:12px}.nlcp-map__title{order:2;flex:1 1 100%;min-width:0}.nlcp-map__title b{font-size:14px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}.nlcp-map__title span{font-size:11.5px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}.nlcp-map__card{top:auto;bottom:14px;inset-inline-end:14px;inset-inline-start:14px;width:auto;max-width:none}.nlcp-map__legend{bottom:auto;top:132px;padding:5px 8px}}
.nlcp-cluster{display:grid;width:38px!important;height:38px;border-radius:50%;background:var(--sa-deep,#1F4B5C);color:#fff;display:grid;place-items:center;font:700 13px Assistant,Heebo,sans-serif;border:3px solid #fff;box-shadow:0 3px 10px rgba(0,0,0,.25);cursor:pointer}
.mapboxgl-popup{z-index:3}
body.nlcp-map-open{overflow:hidden}
</style>
<script id="nlcp-map-js">
(function(){
	var CFG=$cfg, CITIES=$cities;
	var thumb=document.getElementById('nlcp-mapthumb'), shell=document.getElementById('nlcp-map');
	if(!thumb||!shell||!CFG.token)return;
	/* --- thumbnail chips: Web Mercator projection onto the static image --- */
	function proj(lng,lat,z){var s=256*Math.pow(2,z);var x=(lng+180)/360*s;var r=lat*Math.PI/180;var y=(1-Math.log(Math.tan(r)+1/Math.cos(r))/Math.PI)/2*s;return [x,y];}
	function placeChips(){var c=thumb.dataset.center.split(',').map(Number),z=+thumb.dataset.zoom,W=+thumb.dataset.w,H=+thumb.dataset.h;var box=thumb.getBoundingClientRect();var sx=box.width/W,sy=box.height/H;var cen=proj(c[0],c[1],z);var host=thumb.querySelector('.nlcp-mapthumb__chips');host.innerHTML='';
		var max=Math.max.apply(null,CITIES.map(function(x){return x.psqm||0;}));
		var placed=[];
		CITIES.filter(function(x){return x.psqm>0;}).slice(0,14).forEach(function(x){var p=proj(x.lng,x.lat,z);var px=(W/2+(p[0]-cen[0]))*sx,py=(H/2+(p[1]-cen[1]))*sy;if(px<36||py<44||px>box.width-36||py>box.height-66)return;if(placed.some(function(q){return Math.abs(q[0]-px)<70&&Math.abs(q[1]-py)<18;}))return;placed.push([px,py]);var el=document.createElement('span');el.className='nlcp-chip'+(x.psqm>=max*.8?' nlcp-chip--hot':'');el.style.left=px+'px';el.style.top=py+'px';el.textContent=x.name+' '+Math.round(x.psqm/1000)+'K';host.appendChild(el);});}
	placeChips();window.addEventListener('resize',placeChips);
	/* --- full map --- */
	var map=null,markers={},loaded=false,active=null,cardEl=document.getElementById('nlcp-map-card'),catalogState=function(){try{return new URLSearchParams(location.search).get('city')||'';}catch(e){return '';}};
	function loadScript(src){return new Promise(function(res,rej){if(document.querySelector('script[src="'+src+'"]'))return res();var s=document.createElement('script');s.src=src;s.onload=res;s.onerror=rej;document.head.appendChild(s);});}
	function loadCss(href){if(document.querySelector('link[href="'+href+'"]'))return;var l=document.createElement('link');l.rel='stylesheet';l.href=href;document.head.appendChild(l);}
	function color(p){return p>=70000?'#1F4B5C':p>=60000?'#2F6F86':p>=45000?'#5F98AB':p>=30000?'#9CC4D1':p>0?'#DCEBF0':'#EEE9DD';}
	function nis(n){return Number(n).toLocaleString('he-IL')+' ₪';}
	function cityOf(name){var k=(name||'').replace(/[-־]/g,' ').replace(/\s+/g,' ').trim();if(!k)return null;if(k.indexOf('תל אביב')===0)k='תל אביב יפו';k=k.replace('הרצלייה','הרצליה').replace('פתח תקוה','פתח תקווה');return CITIES.find(function(c){return c.name===k||k.indexOf(c.name)===0||c.name.indexOf(k)===0;});}
	function open(opts){opts=opts||{};shell.hidden=false;document.body.classList.add('nlcp-map-open');if(map){setTimeout(function(){try{map.resize();}catch(e){}},50);}if(!loaded){loaded=true;loadCss(CFG.glcss);loadScript(CFG.gl).then(function(){return loadScript(CFG.rtl).catch(function(){});}).then(function(){boot(opts);}).catch(function(){document.getElementById('nlcp-map-sub').textContent='המפה לא נטענה. נסו שוב או המשיכו ברשימה.';});}else if(map){focus(opts);}}
	function close(){shell.hidden=true;document.body.classList.remove('nlcp-map-open');if(location.hash.indexOf('#map')===0)history.replaceState(null,'',location.pathname+location.search);}
	function boot(opts){mapboxgl.accessToken=CFG.token;try{if(mapboxgl.getRTLTextPluginStatus&&mapboxgl.getRTLTextPluginStatus()==='unavailable')mapboxgl.setRTLTextPlugin(CFG.rtl,null,true);}catch(e){}
		var stage=document.getElementById('nlcp-map-stage');stage.innerHTML='';
		map=new mapboxgl.Map({container:stage,style:'mapbox://styles/mapbox/light-v11',center:[34.85,32.0],zoom:8.2,attributionControl:true,cooperativeGestures:false});
		window.NLCP_MAP.map=map;
		map.on('error',function(e){console.warn('nlcp-map error: '+(e&&e.error&&e.error.message||e)+' | src='+(e&&e.sourceId||'-')+' | keys='+Object.keys(e||{}).join(',')+' | type='+(e&&e.error&&e.error.name||'')+(e&&e.error&&e.error.stack?' | '+String(e.error.stack).split('\\n').slice(0,3).join(' / '):''));});
		map.addControl(new mapboxgl.NavigationControl({showCompass:false}),'top-left');
		var built=false;function build(){if(built)return;built=true;try{addHeat();}catch(e){console.warn('nlcp heat',e);}try{addProjects(opts);}catch(e){console.warn('nlcp projects',e);}}
		map.on('load',build);map.once('idle',build);map.on('style.load',function(){build();});setTimeout(function(){build();},5000);
		[150,600,1500].forEach(function(t){setTimeout(function(){try{map.resize();}catch(e){}},t);});
	}
	function addHeat(){
		map.addSource('nlcp-cities',{type:'geojson',data:{type:'FeatureCollection',features:CITIES.filter(function(c){return c.psqm>0;}).map(function(c){return {type:'Feature',properties:{name:c.name,psqm:c.psqm,n:c.n,color:color(c.psqm),r:Math.max(10,Math.min(34,6+Math.sqrt(c.n)*2.6))},geometry:{type:'Point',coordinates:[c.lng,c.lat]}};})}});
		map.addLayer({id:'nlcp-city-heat',type:'circle',source:'nlcp-cities',paint:{'circle-color':['get','color'],'circle-radius':['interpolate',['linear'],['zoom'],6,['get','r'],11,['*',['get','r'],2.2],13,1],'circle-opacity':['interpolate',['linear'],['zoom'],6,.55,11,.35,12.5,0],'circle-blur':.6}});
		map.addLayer({id:'nlcp-city-label',type:'symbol',source:'nlcp-cities',minzoom:6.5,maxzoom:12,layout:{'text-field':['concat',['get','name'],'\\n',['number-format',['get','psqm'],{'locale':'he','max-fraction-digits':0}],' ₪'],'text-size':11,'text-offset':[0,0],'text-font':['DIN Pro Medium','Arial Unicode MS Regular']},paint:{'text-color':'#14212B','text-halo-color':'#fff','text-halo-width':1.2}});
		if(CFG.hoods){map.addSource('nlcp-hoods',{type:'geojson',data:CFG.hoods});
			map.addLayer({id:'nlcp-hoods-fill',type:'fill',source:'nlcp-hoods',minzoom:10.5,paint:{'fill-color':['case',['>',['coalesce',['get','psqm'],0],0],['interpolate',['linear'],['get','psqm'],20000,'#DCEBF0',30000,'#9CC4D1',45000,'#5F98AB',60000,'#2F6F86',75000,'#1F4B5C'],'#EEE9DD'],'fill-opacity':.42}},'nlcp-city-heat');
			map.addLayer({id:'nlcp-hoods-line',type:'line',source:'nlcp-hoods',minzoom:10.5,paint:{'line-color':'#fff','line-width':1}});
			map.addLayer({id:'nlcp-hoods-label',type:'symbol',source:'nlcp-hoods',minzoom:12,layout:{'text-field':['case',['>',['coalesce',['get','psqm'],0],0],['concat',['get','name'],'\\n',['number-format',['get','psqm'],{'locale':'he','max-fraction-digits':0}],' ₪'],['get','name']],'text-size':11,'text-font':['DIN Pro Medium','Arial Unicode MS Regular']},paint:{'text-color':'#14212B','text-halo-color':'#fff','text-halo-width':1.4}});
			map.on('click','nlcp-hoods-fill',function(e){var p=e.features[0].properties;if(!p.psqm)return;new mapboxgl.Popup({closeButton:true,offset:6}).setLngLat(e.lngLat).setHTML('<div style="font:13px Assistant,Heebo,sans-serif;direction:rtl"><b>'+p.name+'</b><br>מחיר למ״ר: <b>'+nis(p.psqm)+'</b><br><small>'+p.deals_24m+' עסקאות, '+p.period_from+' עד '+p.period_to+(p.price_4r?'<br>דירת 4 חדרים, חציון: '+nis(p.price_4r):'')+'</small></div>').addTo(map);});}
		var heat=document.getElementById('nlcp-map-heat');heat.addEventListener('change',function(){var v=heat.checked?'visible':'none';['nlcp-city-heat','nlcp-city-label','nlcp-hoods-fill','nlcp-hoods-line','nlcp-hoods-label'].forEach(function(id){if(map.getLayer(id))map.setLayoutProperty(id,'visibility',v);});});
	}
	function addProjects(opts){fetch(CFG.projects,{headers:{Accept:'application/json'}}).then(function(r){return r.json();}).then(function(d){var items=(d&&d.items)||[];
			var feats=items.filter(function(p){return p.lat&&p.lng;}).map(function(p){var c=cityOf(p.city);var ctx=p.psqm>0?p.psqm:(c?c.psqm:0);return {type:'Feature',properties:{id:p.id,title:p.title,url:p.url,city:p.city,img:p.img||p.poster||'',units:p.units||0,status:p.status||'',own:p.psqm>0?1:0,psqm:ctx,featured:p.featured?1:0},geometry:{type:'Point',coordinates:[+p.lng,+p.lat]}};});
			map.addSource('nlcp-proj',{type:'geojson',data:{type:'FeatureCollection',features:feats},cluster:true,clusterMaxZoom:11,clusterRadius:38  /* integer only: a fractional maxZoom makes supercluster throw 'Invalid array length' */});
			map.addLayer({id:'nlcp-proj-hidden',type:'circle',source:'nlcp-proj',paint:{'circle-opacity':0,'circle-radius':1}});
			map.on('sourcedata',function(e){if(e&&e.sourceId==='nlcp-proj')sync();});map.on('moveend',sync);map.on('idle',sync);sync();focus(opts);map.once('idle',function(){if(!opts.project&&!opts.lnglat)setTimeout(function(){pulseIn(map.getBounds());},300);});
		}).catch(function(){document.getElementById('nlcp-map-sub').textContent='רשימת הפרויקטים לא נטענה למפה.';});}
	function sync(){if(!map.getSource('nlcp-proj')||!map.isSourceLoaded('nlcp-proj'))return;var feats=map.querySourceFeatures('nlcp-proj');var keep={};
		feats.forEach(function(f){var p=f.properties,id=p.cluster?'c'+p.cluster_id:'p'+p.id;keep[id]=1;if(markers[id])return;var el=document.createElement('div');
			if(p.cluster){el.className='nlcp-cluster';el.textContent=p.point_count;el.addEventListener('click',function(){map.getSource('nlcp-proj').getClusterExpansionZoom(p.cluster_id,function(err,z){if(err)return;map.easeTo({center:f.geometry.coordinates,zoom:z+.4});});});}
			else{el.className='nlcp-pin'+(p.featured?' is-featured':'')+(p.own?'':' is-city is-dot');el.innerHTML=p.own?('<b>'+Math.round(p.psqm/1000)+'K</b> ₪/מ״ר'):'';el.title=p.title;el.addEventListener('click',function(){showCard(f);});}
			markers[id]=new mapboxgl.Marker({element:el,anchor:(p.cluster||!p.own)?'center':'bottom'}).setLngLat(f.geometry.coordinates).addTo(map);});
		Object.keys(markers).forEach(function(id){if(!keep[id]){markers[id].remove();delete markers[id];}});}
	function showCard(f){var p=f.properties;active=p.id;document.querySelectorAll('.nlcp-pin.is-active').forEach(function(e){e.classList.remove('is-active');});var m=markers['p'+p.id];if(m)m.getElement().classList.add('is-active');
		var c=cityOf(p.city);var ctx=p.own?('מחיר למ״ר בפרויקט, לפי היזם: <b>'+nis(p.psqm)+'</b>'+(c&&c.psqm?'<br>בעיר: '+nis(c.psqm):'')):(c&&c.psqm?'מחיר למ״ר ב'+c.name+': <b>'+nis(c.psqm)+'</b><br><small>'+c.deals.toLocaleString('he-IL')+' עסקאות, '+c.period+' · רשות המסים</small>':'');
		cardEl.innerHTML='<button type="button" class="x" aria-label="סגירה">×</button>'+(p.img?'<img src="'+p.img+'" alt="">':'')+'<div class="in"><h3>'+p.title+'</h3><div class="meta">'+(p.city?'<span>'+p.city+'</span>':'')+(p.units?'<span>'+p.units+' יח״ד</span>':'')+'</div>'+(ctx?'<div class="ctx">'+ctx+'</div>':'')+'<a class="go" href="'+p.url+'">לעמוד הפרויקט</a></div>';
		cardEl.hidden=false;cardEl.querySelector('.x').addEventListener('click',function(){cardEl.hidden=true;});map.easeTo({center:f.geometry.coordinates,offset:[0,60]});}
	function pulseIn(bounds){setTimeout(function(){Object.keys(markers).forEach(function(id){if(id[0]!=='p')return;var ll=markers[id].getLngLat();if(bounds.contains(ll))markers[id].getElement().classList.add('is-pulse');});setTimeout(function(){document.querySelectorAll('.nlcp-pin.is-pulse').forEach(function(e){e.classList.remove('is-pulse');});},4500);},700);}
	function focus(opts){if(!map)return;var sub=document.getElementById('nlcp-map-sub');
		if(opts.project){var f=(map.getSource('nlcp-proj')&&map.getSource('nlcp-proj')._data.features||[]).find(function(x){return String(x.properties.id)===String(opts.project);});if(f){map.jumpTo({center:f.geometry.coordinates,zoom:14.5});setTimeout(function(){showCard(f);var m=markers['p'+f.properties.id];if(m)m.getElement().classList.add('is-pulse');},900);return;}}
		if(opts.lnglat){map.flyTo({center:opts.lnglat,zoom:13,speed:1.4});sub.textContent='הפרויקטים החדשים סביב המיקום שלכם.';map.once('moveend',function(){pulseIn(map.getBounds());});return;}
		var city=cityOf(opts.city||catalogState());if(city){map.flyTo({center:[city.lng,city.lat],zoom:city.name==='תל אביב יפו'?12.3:12,speed:1.4});sub.textContent='פרויקטים חדשים ב'+city.name+(city.psqm?' · מחיר למ״ר בעיר: '+nis(city.psqm):'');map.once('moveend',function(){pulseIn(map.getBounds());});}
		else{map.fitBounds([[34.25,29.45],[35.9,33.35]],{padding:20,duration:0});}}
	function near(btn){if(!navigator.geolocation){open({});return;}btn&&btn.classList.add('is-busy');navigator.geolocation.getCurrentPosition(function(pos){btn&&btn.classList.remove('is-busy');open({lnglat:[pos.coords.longitude,pos.coords.latitude]});},function(){btn&&btn.classList.remove('is-busy');open({});},{timeout:8000,maximumAge:600000});}
	thumb.addEventListener('click',function(e){e.preventDefault();if(e.target.closest('.nlcp-mapthumb__near')){near(e.target.closest('.nlcp-mapthumb__near'));return;}history.replaceState(null,'',location.pathname+location.search+'#map');open({});});
	document.getElementById('nlcp-map-close').addEventListener('click',close);
	document.getElementById('nlcp-map-near').addEventListener('click',function(){near(this);});
	document.addEventListener('keydown',function(e){if(e.key==='Escape'&&!shell.hidden)close();});
	var pm=document.querySelector('.nlcp-pricemap');if(pm){var b=document.createElement('button');b.type='button';b.className='nlcp-near';b.style.marginTop='8px';b.textContent='פתיחת המפה המלאה';b.addEventListener('click',function(){open({});});pm.appendChild(b);}
	if(location.hash.indexOf('#map')===0){var hm=location.hash.match(/^#map(?:=(\d+))?/);var go=function(){setTimeout(function(){open(hm&&hm[1]?{project:hm[1]}:{});},250);};if(document.readyState==='complete')go();else window.addEventListener('load',go);}
	window.NLCP_MAP={open:open,close:close};
})();
</script>
HTML;
	}
}

/* ------------------------------------------------------------------ project pages: what surrounds the project (find-place) */
if ( ! function_exists( 'nadlan_cp_surroundings' ) ) {
	function nadlan_cp_surroundings( $id ) {
		static $d = null;
		if ( null === $d ) {
			$d = get_transient( 'nadlan_cp_surr_v1' );
			if ( ! is_array( $d ) ) { $p = nadlan_cp_uploads_path( 'project-surroundings-v1.json' ); $d = file_exists( $p ) ? (array) json_decode( (string) file_get_contents( $p ), true ) : array(); set_transient( 'nadlan_cp_surr_v1', $d, 6 * HOUR_IN_SECONDS ); }
		}
		return $d['projects'][ (string) $id ] ?? null;
	}
}
if ( ! function_exists( 'nadlan_cp_plan_status_he' ) ) {
	function nadlan_cp_plan_status_he( $s ) { $m = array( 'approved' => 'מאושרת', 'in_force' => 'בתוקף', 'deposited' => 'בהפקדה', 'in_progress' => 'בתהליך', 'proposed' => 'מוצעת', 'not_applicable' => '' ); return $m[ (string) $s ] ?? (string) $s; }
}
if ( ! function_exists( 'nadlan_cp_surroundings_html' ) ) {
	function nadlan_cp_surroundings_html( $id ) {
		$s = nadlan_cp_surroundings( $id ); if ( ! $s ) { return ''; }
		$lat = (float) get_post_meta( $id, 'lat', true ); $lng = (float) get_post_meta( $id, 'lng', true ); $tok = nadlan_cp_mapbox_token();
		$tiles = array();
		if ( ! empty( $s['rail'] ) ) { $r = $s['rail']; $tiles[] = array( 'רכבת קלה', $r['name'], $r['operational'] ? 'פעילה, ' . $r['m'] . ' מ׳ הליכה' : ( 'approved' === ( $r['planning'] ?? '' ) ? 'מאושרת, ' . $r['m'] . ' מ׳' : $r['m'] . ' מ׳' ) ); }
		if ( ! empty( $s['schools'] ) ) { $names = array_map( function ( $x ) { return str_replace( 'בית הספר ', '', $x['name'] ); }, array_slice( $s['schools'], 0, 3 ) ); $tiles[] = array( 'בתי ספר במרחק הליכה', implode( ' · ', $names ), count( $s['schools'] ) . ' עד 900 מ׳' ); }
		if ( ! empty( $s['kindergartens_600m'] ) ) { $tiles[] = array( 'גני ילדים', (string) $s['kindergartens_600m'], 'עד 600 מ׳' ); }
		if ( ! empty( $s['parks'] ) ) { $tiles[] = array( 'פארקים וחופים', implode( ' · ', array_map( function ( $x ) { return $x['name']; }, $s['parks'] ) ), $s['parks'][0]['m'] . ' מ׳ לקרוב' ); }
		if ( ! empty( $s['construction'] ) ) { $c = $s['construction']; $tiles[] = array( 'בנייה מסביב', $c['active_500m'] . ' אתרים פעילים', 'ברדיוס 500 מ׳ · הקרוב: ' . $c['nearest']['name'] . ', ' . $c['nearest']['m'] . ' מ׳' ); }
		if ( ! empty( $s['plans'] ) ) { $p = $s['plans'][0]; $tiles[] = array( 'תכנון עתידי', $p['name'], trim( nadlan_cp_plan_status_he( $p['status'] ) . ( $p['inside'] ? ' · הפרויקט בתחום התוכנית' : '' ) ) ); }
		if ( ! $tiles ) { return ''; }
		$nb = ! empty( $s['neighborhood'] ) ? $s['neighborhood'] : '';
		if ( $nb && "'" === mb_substr( $nb, 0, 1 ) ) { $nb = mb_substr( $nb, 1 ) . "'"; }
		$img = '';
		if ( $tok && $lat && $lng ) {
			$src = 'https://api.mapbox.com/styles/v1/mapbox/light-v11/static/pin-l+2F6F86(' . $lng . ',' . $lat . ')/' . $lng . ',' . $lat . ',14.2,0/640x300@2x?access_token=' . rawurlencode( $tok ) . '&attribution=false&logo=false';
			$img = '<a class="nlcp-surr__map" href="' . esc_url( home_url( '/projects/#map=' . (int) $id ) ) . '"><img src="' . esc_url( $src ) . '" alt="מפת הסביבה של ' . esc_attr( get_the_title( $id ) ) . ( $nb ? ', ' . esc_attr( $nb ) : '' ) . '" width="640" height="300" loading="lazy" decoding="async"><span>פתיחת המפה עם המחירים מסביב</span></a>';
		}
		$h  = '<section class="nlcp-surr" dir="rtl" aria-label="מה קורה מסביב"><div class="nlcp-surr__head"><span class="nlcp-projctx__k">מה קורה מסביב</span><h2>' . ( $nb ? 'הסביבה: ' . esc_html( $nb ) : 'הסביבה של הפרויקט' ) . '</h2><p>מה שקיים ומה שמתוכנן במרחק הליכה: תחבורה, חינוך, פארקים, בנייה ותוכניות. מקור: find-place, שכבות מידע עירוניות וממשלתיות.</p></div><div class="nlcp-surr__grid">' . $img . '<div class="nlcp-surr__tiles">';
		foreach ( $tiles as $t ) { $h .= '<div class="nlcp-tile"><small>' . esc_html( $t[0] ) . '</small><b>' . esc_html( $t[1] ) . '</b><span>' . esc_html( $t[2] ) . '</span></div>'; }
		$h .= '</div></div></section>';
		$h .= '<style>.nlcp-surr{max-width:1180px;margin:0 auto 22px;padding:20px clamp(16px,2.5vw,28px);background:var(--sa-surf,#fff);border:1px solid var(--sa-line,#E3E1DA);border-radius:18px}.nlcp-surr h2{margin:0 0 6px;font-family:var(--sa-serif,"Noto Serif Hebrew",serif);font-size:clamp(20px,2.2vw,26px);color:var(--sa-ink,#14212B)}.nlcp-surr__head p{margin:0 0 14px;color:var(--sa-ink2,#3B4753);font-size:14.5px;line-height:1.55}.nlcp-surr__grid{display:grid;grid-template-columns:minmax(0,1.1fr) minmax(0,1fr);gap:14px;align-items:start}.nlcp-surr__map{position:relative;display:block;border-radius:14px;overflow:hidden;border:1px solid var(--sa-line,#E3E1DA)}.nlcp-surr__map img{display:block;width:100%;height:auto}.nlcp-surr__map span{position:absolute;bottom:10px;inset-inline-start:10px;background:var(--sa-sea,#2F6F86);color:#fff;font-size:12.5px;font-weight:700;padding:6px 12px;border-radius:999px}.nlcp-surr__tiles{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px}.nlcp-surr .nlcp-tile b{font-size:15px;line-height:1.3}@media(max-width:800px){.nlcp-surr__grid{grid-template-columns:1fr}}</style>';
		return $h;
	}
}
