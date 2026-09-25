<?php
/**
 * Home v3, the top of the portal's home (design system version 31, 25.9.2026; the site loop H1.1; Linear HAD-297).
 *
 * On the Hebrew front page with the skin on:
 *  - the header: one row with the categories as menus (details panels that work without a script), the language menu
 *    and "פרסום מודעה"; on a phone a menu button opens the same panels as a sheet;
 *  - the hero: the site's coastline photo across the width (a portrait crop on phones), the H1 over the sea, the search;
 *  - the categories row;
 *  - an honest meta description with the live count (the old one promised availability by floor and view);
 *  - the first picture: a preload per media and this part's CSS in the head (the R6 lesson: 17 s on a mid Android).
 *
 * The skin's renderer (snippet x-skin-a) still prints every band below the hero. This file swaps only the top of its
 * output (the language bar, the browse bar and the old hero) and fails open: without its markers the page stays as it
 * was. The language homes (/en /fr /ru /ar) are untouched. ?hp=off shows the page without it.
 */

if ( ! function_exists( 'nadlan_hp_on' ) ) {
	function nadlan_hp_on() {
		static $on = null;
		if ( null !== $on ) { return $on; }
		if ( is_admin() || wp_doing_ajax() || ( defined( 'REST_REQUEST' ) && REST_REQUEST ) || ! is_front_page() ) { return $on = false; }
		if ( function_exists( 'nadlan_is_language_home' ) && nadlan_is_language_home() ) { return $on = false; }
		if ( ! function_exists( 'nadlan_skin_a_on' ) || ! nadlan_skin_a_on() ) { return $on = false; }
		if ( isset( $_GET['hp'] ) && 'off' === sanitize_key( wp_unslash( $_GET['hp'] ) ) ) { return $on = false; }
		return $on = ( 'off' !== get_option( 'nadlan_home_v3', 'on' ) );
	}
}

if ( ! function_exists( 'nadlan_hp_img' ) ) {
	function nadlan_hp_img( $f ) {
		return plugins_url( 'assets/home/' . $f, dirname( __FILE__ ) ) . '?ver=' . ( defined( 'NADLAN_CONFIG_VERSION' ) ? NADLAN_CONFIG_VERSION : '1' );
	}
}

if ( ! function_exists( 'nadlan_hp_counts' ) ) {
	/** Live counts: published projects as the catalogue counts them (no language siblings, no private journeys),
	 *  their distinct cities (kept for checks, not printed yet) and published professionals. Cached one hour. */
	function nadlan_hp_counts() {
		$k = 'nadlan_hp_counts_v1';
		$c = get_transient( $k );
		if ( is_array( $c ) ) { return $c; }
		global $wpdb;
		$private = " AND NOT EXISTS (SELECT 1 FROM {$wpdb->postmeta} x WHERE x.post_id=p.ID AND x.meta_key='_nadlan_private_unit_journey' AND x.meta_value='private-unit-journey-v2')";
		$where   = "p.post_type='nadlan_project' AND p.post_status='publish' AND p.post_name NOT REGEXP '-(en|fr|ru|ar)$'" . $private;
		$total   = (int) $wpdb->get_var( "SELECT COUNT(*) FROM {$wpdb->posts} p WHERE " . $where );
		$vals    = $wpdb->get_col( "SELECT DISTINCT pm.meta_value FROM {$wpdb->postmeta} pm INNER JOIN {$wpdb->posts} p ON p.ID=pm.post_id WHERE pm.meta_key='city' AND pm.meta_value<>'' AND " . $where );
		$names   = array();
		foreach ( (array) $vals as $v ) {
			$n = function_exists( 'nadlan_meta_norm' ) ? nadlan_meta_norm( $v ) : (string) $v;
			$n = trim( (string) preg_replace( '/[\s\-\x{05BE}]+/u', ' ', (string) $n ) );
			if ( '' !== $n && mb_strlen( $n ) <= 30 ) { $names[ $n ] = 1; }
		}
		$pros = wp_count_posts( 'nadlan_professional' );
		$c    = array( 'projects' => $total, 'cities' => count( $names ), 'pros' => isset( $pros->publish ) ? (int) $pros->publish : 0 );
		set_transient( $k, $c, HOUR_IN_SECONDS );
		return $c;
	}
}

if ( ! function_exists( 'nadlan_hp_icon' ) ) {
	function nadlan_hp_icon( $d ) {
		return '<svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="' . esc_attr( $d ) . '"/></svg>';
	}
}

if ( ! function_exists( 'nadlan_hp_panel' ) ) {
	/** One menu: a details element whose summary is the category; the panel holds columns of links and an optional card. */
	function nadlan_hp_panel( $label, $cols, $promo = '' ) {
		$h = '<details class="nlhp-dd"><summary class="nlhp-nav__item">' . esc_html( $label ) . ' <span class="nlhp-caret" aria-hidden="true"></span></summary><div class="nlhp-mega"><div class="nlhp-mega__in">';
		foreach ( $cols as $col ) {
			$h .= '<div class="nlhp-mega__col">';
			foreach ( $col as $grp ) {
				$h .= '<p class="nlhp-mega__h">' . esc_html( $grp[0] ) . '</p>';
				foreach ( $grp[1] as $l ) {
					$n  = isset( $l[2] ) && '' !== $l[2] ? '<span>' . esc_html( $l[2] ) . '</span>' : '';
					$h .= '<a href="' . esc_url( $l[1] ) . '"' . ( ! empty( $l[3] ) ? ' class="nlhp-mega__all"' : '' ) . '>' . esc_html( $l[0] ) . $n . '</a>';
				}
			}
			$h .= '</div>';
		}
		return $h . $promo . '</div></div></details>';
	}
}

if ( ! function_exists( 'nadlan_hp_header' ) ) {
	function nadlan_hp_header() {
		$c     = nadlan_hp_counts();
		$fmt   = function ( $n ) { return number_format( (int) $n ); };
		$u     = function ( $p ) { return home_url( $p ); };
		$facet = function_exists( 'nadlan_dir_project_facets' ) ? nadlan_dir_project_facets() : array();
		$pcity = array();
		foreach ( array_slice( (array) ( isset( $facet['cities'] ) ? $facet['cities'] : array() ), 0, 8 ) as $x ) {
			$pcity[] = array( $x['name'], $u( '/projects/?city=' . rawurlencode( $x['name'] ) ), $fmt( $x['n'] ) );
		}
		$lcity = array();
		$rcity = array();
		foreach ( ( function_exists( 'nadlan_hv2_cities' ) ? nadlan_hv2_cities( 14 ) : array() ) as $x ) {
			if ( empty( $x['properties'] ) || count( $lcity ) >= 8 ) { continue; }
			$lcity[] = array( 'דירות ב' . $x['name'], $u( '/properties/?city=' . rawurlencode( $x['name'] ) ) );
			$rcity[] = array( 'להשכרה ב' . $x['name'], $u( '/properties/?listing_type=rent&city=' . rawurlencode( $x['name'] ) ) );
		}
		$profs = array();
		foreach ( ( function_exists( 'nadlan_dir_professions_all' ) ? nadlan_dir_professions_all() : array() ) as $key => $p ) {
			$profs[] = array( $p['label'], $u( '/professionals/?profession=' . rawurlencode( $key ) ) );
		}
		$posts = array();
		foreach ( get_posts( array( 'post_type' => 'post', 'post_status' => 'publish', 'numberposts' => 4, 'suppress_filters' => false ) ) as $p ) {
			$posts[] = array( wp_strip_all_tags( get_the_title( $p ) ), get_permalink( $p ) );
		}
		$promo = '';
		$rb    = get_page_by_path( 'rainbow-tel-aviv', OBJECT, 'nadlan_project' );
		if ( $rb && 'publish' === $rb->post_status ) {
			$promo = '<a class="nlhp-mega__promo" href="' . esc_url( get_permalink( $rb ) ) . '"><img src="' . esc_url( plugins_url( 'assets/project-stage/rainbow/poster-716.jpg', dirname( __FILE__ ) ) ) . '" alt="הדמיה של פרויקט ריינבו תל אביב" width="716" height="660" loading="lazy" decoding="async"><span><small>סיור וירטואלי · הדמיה להמחשה</small><b>ריינבו תל אביב: בוחרים קומה ורואים את הנוף</b></span></a>';
		}
		$all_p = 'לכל ' . $fmt( $c['projects'] ) . ' הפרויקטים החדשים ←';

		$menus  = nadlan_hp_panel( 'פרויקטים חדשים', array(
			array( array( 'פרויקטים חדשים לפי עיר', $pcity ) ),
			array( array( 'לפי סוג', array( array( 'כל הפרויקטים החדשים', $u( '/projects/' ), $fmt( $c['projects'] ) ), array( 'פינוי־בינוי', $u( '/projects/?project_type=pinui_binui' ) ), array( 'תמ״א 38', $u( '/projects/?project_type=tama38' ) ), array( 'נדל״ן מסחרי', $u( '/commercial-real-estate/' ) ) ) ),
				array( 'אזורי ביקוש', array( array( 'רובע שדה דב', $u( '/sde-dov/' ) ), array( 'התחדשות עירונית', $u( '/urban-renewal/' ) ) ) ) ),
			array( array( 'סיורים וירטואליים', array( array( 'סיור ברובע שדה דב', $u( '/tour/sde-dov/' ) ), array( 'סיור במתחם סומייל', $u( '/tour/somail/' ) ), array( 'כל הסיורים', $u( '/tours/' ) ), array( $all_p, $u( '/projects/' ), '', 1 ) ) ) ),
		), $promo );
		$menus .= nadlan_hp_panel( 'דירות למכירה', array(
			array( array( 'דירות למכירה', array_merge( array( array( 'כל הדירות למכירה', $u( '/properties/?listing_type=sale' ) ) ), array_slice( $lcity, 0, 4 ) ) ) ),
			array( array( 'לפי עיר', array_slice( $lcity, 4 ) ) ),
			array( array( 'מפרסמים דירה?', array( array( 'פרסום מודעה חינם', $u( '/post-listing/' ) ), array( 'פרסום לבעלי מקצוע ויזמים', $u( '/advertise/' ) ), array( 'פרסום מודעה ←', $u( '/post-listing/' ), '', 1 ) ) ) ),
		) );
		$menus .= nadlan_hp_panel( 'דירות להשכרה', array(
			array( array( 'דירות להשכרה', array_merge( array( array( 'כל הדירות להשכרה', $u( '/properties/?listing_type=rent' ) ) ), array_slice( $rcity, 0, 4 ) ) ) ),
			array( array( 'לפי עיר', array_slice( $rcity, 4 ) ) ),
			array( array( 'לבעלי דירות', array( array( 'ניהול השכרה חינם', $u( '/my-rentals/' ) ), array( 'פרסום דירה להשכרה', $u( '/post-listing/' ) ) ) ) ),
		) );
		$menus .= nadlan_hp_panel( 'מחירי דירות', array(
			array( array( 'מחירי דירות לפי עיר', array( array( 'מחירון הדירות · כל הערים', $u( '/apartment-prices/' ) ), array( 'מחירי דירות בתל אביב', $u( '/tel-aviv-apartment-prices/' ) ), array( 'מחירי דירות בירושלים', $u( '/jerusalem-apartment-prices/' ) ), array( 'מחירי דירות בהרצליה', $u( '/herzliya-apartment-prices/' ) ), array( 'מחירי דירות ברמת גן', $u( '/ramat-gan-apartment-prices/' ) ), array( 'מחירי דירות בנתניה', $u( '/netanya-apartment-prices/' ) ) ) ) ),
			array( array( 'מחשבונים', array( array( 'מחשבון משכנתא', $u( '/mortgage-calculator/' ) ), array( 'מחשבון מס רכישה', $u( '/purchase-tax-calculator/' ) ), array( 'עלות עסקה מלאה', $u( '/apartment-purchase-cost-calculator/' ) ), array( 'כמה שווה הדירה שלי', $u( '/property-value-estimator/' ) ) ) ) ),
		) );
		$menus .= nadlan_hp_panel( 'סיורים וירטואליים', array(
			array( array( 'סיורים וירטואליים', array( array( 'כל הסיורים', $u( '/tours/' ) ), array( 'סיור רובע שדה דב', $u( '/tour/sde-dov/' ) ), array( 'סיור מתחם סומייל', $u( '/tour/somail/' ) ), array( 'מעצב הדירות', $u( '/tour/designer/' ) ) ) ) ),
			array( array( 'מהאוויר', array( array( 'הליקופטר שדה דב · צילום אמיתי', $u( '/earth/sde-dov/' ) ), array( 'הליקופטר סומייל', $u( '/earth/somail/' ) ), array( 'קטלוג הסיורים הווירטואליים', $u( '/premium/' ) ) ) ) ),
		), $promo );
		$menus .= nadlan_hp_panel( 'מגזין נדל״ן', array(
			array( array( 'מגזין נדל״ן', array( array( 'כל הכתבות והמדריכים', $u( '/guides/' ) ), array( 'קניית דירה: המדריך', $u( '/buying-apartment/' ) ), array( 'בדיקת נסח טאבו', $u( '/tabu-extract-check/' ) ), array( 'נדל״ן להשקעה', $u( '/investment/' ) ), array( 'מילון מונחים', $u( '/glossary/' ) ) ) ) ),
			array( array( 'כתבות אחרונות', $posts ) ),
		) );
		$menus .= nadlan_hp_panel( 'אנשי מקצוע', array(
			array( array( 'אנשי מקצוע לנדל״ן', array_slice( $profs, 0, 5 ) ) ),
			array( array( ' ', array_slice( $profs, 5 ) ) ),
			array( array( 'המאגר', array( array( 'כל המאגר', $u( '/professionals/' ), $fmt( $c['pros'] ) ), array( 'מתווכים', $u( '/brokers/' ) ), array( 'הצטרפות למאגר', $u( '/advertise/' ) ) ) ) ),
		) );
		$menus .= '<a class="nlhp-nav__item nlhp-nav__plain" href="' . esc_url( $u( '/global/' ) ) . '">נדל״ן בחו״ל</a>';

		$langs = function_exists( 'nadlan_lang_switcher' ) ? nadlan_lang_switcher() : '';
		$globe = '<svg viewBox="0 0 24 24" width="17" height="17" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c2.6 2.6 3.9 5.6 3.9 9s-1.3 6.4-3.9 9c-2.6-2.6-3.9-5.6-3.9-9S9.4 5.6 12 3z"/></svg>';
		ob_start();
		?>
<header class="nlhp-top" id="nlhp-top" role="banner">
	<div class="nlhp-top__in">
		<a class="nlhp-logo" href="<?php echo esc_url( home_url( '/' ) ); ?>" aria-label="NadLan, פורטל נדל״ן"><span class="nlhp-logo__mark" aria-hidden="true"><i><b style="height:9px"></b><b style="height:17px"></b><b style="height:12px"></b></i></span><span class="nlhp-logo__word">NadLan</span></a>
		<nav class="nlhp-nav" id="nlhp-nav" aria-label="קטגוריות נדל״ן">
			<div class="nlhp-sheet__head"><span>תפריט</span><button type="button" class="nlhp-sheet__close" data-nlhp-close aria-label="סגירת התפריט">×</button></div>
			<?php if ( $langs ) : ?><div class="nlhp-sheet__langs"><?php echo $langs; // phpcs:ignore -- built and escaped by nadlan_lang_switcher() ?></div><?php endif; ?>
			<?php echo $menus; // phpcs:ignore -- escaped above ?>
			<a class="nlhp-sheet__post" href="<?php echo esc_url( home_url( '/post-listing/' ) ); ?>">פרסום מודעה</a>
		</nav>
		<div class="nlhp-top__end">
			<?php if ( $langs ) : ?><details class="nlhp-dd nlhp-lang"><summary><?php echo $globe; // phpcs:ignore ?>עברית <span class="nlhp-caret" aria-hidden="true"></span></summary><div class="nlhp-lang__menu"><?php echo $langs; // phpcs:ignore ?></div></details><?php endif; ?>
			<a class="nlhp-post" href="<?php echo esc_url( home_url( '/post-listing/' ) ); ?>">פרסום מודעה</a>
			<a class="nlhp-ico nlhp-ico--search" href="#nlhp-hero" aria-label="חיפוש"><svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><circle cx="11" cy="11" r="6.5"/><path d="m20 20-4.2-4.2"/></svg></a>
			<button type="button" class="nlhp-ico nlhp-ico--menu" aria-controls="nlhp-nav" aria-expanded="false" aria-label="פתיחת התפריט"><svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16"/></svg></button>
		</div>
	</div>
</header>
		<?php
		return ob_get_clean();
	}
}

if ( ! function_exists( 'nadlan_hp_top' ) ) {
	/** The hero (photo, H1, search) and the categories row. Reuses the search tabs' script from home-v2 (.nlhv2-search). */
	function nadlan_hp_top() {
		$c      = nadlan_hp_counts();
		$n      = number_format( (int) $c['projects'] );
		$cities = function_exists( 'nadlan_hv2_cities' ) ? nadlan_hv2_cities( 12 ) : array();
		$tabs   = array(
			array( 'פרויקטים חדשים', '/projects/', '' ),
			array( 'דירות למכירה', '/properties/', 'listing_type=sale' ),
			array( 'דירות להשכרה', '/properties/', 'listing_type=rent' ),
			array( 'אנשי מקצוע', '/professionals/', '' ),
		);
		$pop    = array(
			array( 'פרויקטים חדשים בתל אביב', '/new-projects/new-projects-tel-aviv/' ),
			array( 'פרויקטים חדשים בשדה דב', '/sde-dov/' ),
			array( 'מחירי דירות בתל אביב', '/tel-aviv-apartment-prices/' ),
			array( 'דירות למכירה', '/properties/?listing_type=sale' ),
		);
		$cats   = array(
			array( 'פרויקטים חדשים', '/projects/', $n . ' פרויקטים', 'M6 21V5l6-2v18M12 21V8l6 2v11M4 21h16M9 8v.01M9 12v.01M9 16v.01M15 13v.01M15 17v.01' ),
			array( 'דירות למכירה', '/properties/?listing_type=sale', 'לפי עיר, חדרים ומחיר', 'M4 11l8-7 8 7v9H4zM10 20v-5h4v5' ),
			array( 'דירות להשכרה', '/properties/?listing_type=rent', 'לפי עיר, חדרים ומחיר', 'M14.5 9.5a3.5 3.5 0 1 0-.01 0M12 12l-8 8M6.5 17.5l2 2M8.5 15.5l2 2' ),
			array( 'מחירי דירות', '/apartment-prices/', 'עסקאות לפי עיר ורחוב', 'M4 20h16M7 16v-5M12 16V8M17 16v-8' ),
			array( 'סיורים וירטואליים', '/tours/', 'בפרויקטים החדשים', 'M12 3a9 9 0 1 0 .01 0M10 8.5v7l6-3.5z' ),
			array( 'התחדשות עירונית', '/urban-renewal/', 'פינוי־בינוי ותמ״א 38', 'M5 21V10l5-3v14M10 21V4l9 5v12M3 21h18' ),
			array( 'נדל״ן מסחרי', '/commercial-real-estate/', 'משרדים ושטחי מסחר', 'M4 8h16v12H4zM9 8V5h6v3M4 13h16' ),
			array( 'אנשי מקצוע', '/professionals/', number_format( (int) $c['pros'] ) . ' בעלי מקצוע', 'M12 12a4 4 0 1 0-.01 0M4 21c0-4 3.6-6 8-6s8 2 8 6' ),
		);
		ob_start();
		?>
<section class="nlhp-hero" id="nlhp-hero" aria-label="חיפוש נדל״ן" data-nlhp-projects="<?php echo (int) $c['projects']; ?>" data-nlhp-cities="<?php echo (int) $c['cities']; ?>">
	<picture>
		<source media="(max-width: 760px)" srcset="<?php echo esc_url( nadlan_hp_img( 'hero-m-780.jpg' ) ); ?> 780w" sizes="100vw">
		<img class="nlhp-hero__img" src="<?php echo esc_url( nadlan_hp_img( 'hero-d-1400.jpg' ) ); ?>" srcset="<?php echo esc_url( nadlan_hp_img( 'hero-d-1400.jpg' ) ); ?> 1400w, <?php echo esc_url( nadlan_hp_img( 'hero-d-1920.jpg' ) ); ?> 1920w" sizes="(max-width: 1440px) calc(100vw - 48px), 1392px" width="1392" height="540" alt="קו החוף של תל אביב מהאוויר" fetchpriority="high" decoding="async">
	</picture>
	<div class="nlhp-hero__body">
		<p class="nlhp-hero__kicker">פורטל הנדל״ן של ישראל</p>
		<h1>נדל״ן: פרויקטים חדשים, דירות למכירה ומחירי דירות</h1>
		<p class="nlhp-hero__lead"><span class="nlhp-n"><?php echo esc_html( $n ); ?></span> פרויקטים חדשים, דירות למכירה ולהשכרה, מחירי דירות מעסקאות שנמכרו, מחשבונים ומגזין נדל״ן.</p>
		<form class="nlhp-search nlhv2-search" action="<?php echo esc_url( home_url( '/projects/' ) ); ?>" method="get" role="search">
			<div class="nlhp-search__tabs nlhv2-tabs" role="tablist" aria-label="מה מחפשים">
				<?php foreach ( $tabs as $i => $t ) : ?><button type="button" role="tab" class="nlhp-search__tab<?php echo 0 === $i ? ' is-on' : ''; ?>" aria-selected="<?php echo 0 === $i ? 'true' : 'false'; ?>" data-action="<?php echo esc_url( home_url( $t[1] ) ); ?>" data-extra="<?php echo esc_attr( $t[2] ); ?>"><?php echo esc_html( $t[0] ); ?></button><?php endforeach; ?>
			</div>
			<div class="nlhp-search__row">
				<label class="nlhp-search__field"><svg viewBox="0 0 24 24" width="19" height="19" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><circle cx="11" cy="11" r="6.5"/><path d="m20 20-4.2-4.2"/></svg><input type="search" name="q" list="nlhp-cities" placeholder="עיר, שכונה, רחוב או פרויקט" aria-label="חיפוש: עיר, שכונה, רחוב או פרויקט"></label>
				<datalist id="nlhp-cities"><?php foreach ( $cities as $x ) { echo '<option value="' . esc_attr( $x['name'] ) . '">'; } ?></datalist>
				<button type="submit" class="nlhp-search__go">חיפוש</button>
			</div>
			<div class="nlhp-search__pop"><span>חיפושים נפוצים:</span><?php foreach ( $pop as $p ) : ?><a href="<?php echo esc_url( home_url( $p[1] ) ); ?>"><?php echo esc_html( $p[0] ); ?></a><?php endforeach; ?></div>
		</form>
	</div>
	<span class="nlhp-hero__cap">צילום אווירה: קו החוף של תל אביב</span>
</section>
<nav class="nlhp-cats" aria-label="מה מחפשים בנדל״ן">
	<?php foreach ( $cats as $k ) : ?><a class="nlhp-cat" href="<?php echo esc_url( home_url( $k[1] ) ); ?>"><span class="nlhp-cat__ico"><?php echo nadlan_hp_icon( $k[3] ); // phpcs:ignore ?></span><b><?php echo esc_html( $k[0] ); ?></b><span><?php echo esc_html( $k[2] ); ?></span></a><?php endforeach; ?>
</nav>
		<?php
		return ob_get_clean();
	}
}

/* the header: the theme's header part is replaced on this page only */
add_filter( 'render_block', function ( $html, $block ) {
	if ( empty( $block['blockName'] ) || 'core/template-part' !== $block['blockName'] ) { return $html; }
	if ( ! isset( $block['attrs']['slug'] ) || 'header' !== $block['attrs']['slug'] || ! nadlan_hp_on() ) { return $html; }
	return nadlan_hp_header();
}, 20, 2 );

/* the top of the skin's home: from its language bar to the end of its old hero; everything after stays */
add_filter( 'the_content', function ( $content ) {
	if ( ! nadlan_hp_on() || ! in_the_loop() || ! is_main_query() ) { return $content; }
	$a = strpos( $content, '<div class="nlhv2-langbar">' );
	$h = strpos( $content, '<section class="nlsa-hero"' );
	if ( false === $h ) { return $content; }
	$e = strpos( $content, '</section>', $h );
	if ( false === $e ) { return $content; }
	$from = ( false !== $a && $a < $h ) ? $a : $h;
	return substr( $content, 0, $from ) . nadlan_hp_top() . substr( $content, $e + strlen( '</section>' ) );
}, PHP_INT_MAX - 1 );

/* an honest description with the live count, after the theme's (priority 40) */
if ( ! function_exists( 'nadlan_hp_desc' ) ) {
	function nadlan_hp_desc() {
		$c = nadlan_hp_counts();
		return 'נדל״ן בישראל: ' . number_format( (int) $c['projects'] ) . ' פרויקטים חדשים, דירות למכירה ולהשכרה, מחירי דירות לפי עיר ושכונה, מחשבון משכנתא ומס רכישה, מגזין נדל״ן ואנשי מקצוע.';
	}
}
if ( ! function_exists( 'nadlan_hp_front_he' ) ) {
	/** The Hebrew front page, whatever the switch: the honest description never depends on the new top being on. */
	function nadlan_hp_front_he() {
		return ! is_admin() && is_front_page() && ! ( function_exists( 'nadlan_is_language_home' ) && nadlan_is_language_home() );
	}
}
foreach ( array( 'wpseo_metadesc', 'wpseo_opengraph_desc', 'wpseo_twitter_description' ) as $nadlan_hp_f ) {
	add_filter( $nadlan_hp_f, function ( $d ) { return nadlan_hp_front_he() ? nadlan_hp_desc() : $d; }, 60 );
}
/* Yoast's WebPage piece carried "בחירת דירה מתוך הבניין", true for one project, not for the portal */
add_filter( 'wpseo_schema_webpage', function ( $data ) {
	if ( nadlan_hp_front_he() && is_array( $data ) ) { $data['description'] = nadlan_hp_desc(); }
	return $data;
}, 60 );
/* The theme's own front-page title and description are pluggable there (function_exists), and this plugin loads first.
   Its schema printed a WebPage named "…עם בחירת דירה בתלת ממד" and the old promise; now the page's real title (the one
   the tab already shows) and the honest description. */
if ( ! function_exists( 'nadlan_revenue_home_seo_title' ) ) {
	function nadlan_revenue_home_seo_title() {
		return 'נדלן - דירות למכירה, פרויקטים חדשים ומחירי דירות בישראל';
	}
}
if ( ! function_exists( 'nadlan_revenue_home_seo_description' ) ) {
	function nadlan_revenue_home_seo_description() {
		return nadlan_hp_desc();
	}
}

/* The home shows no 3D viewer and no payment form, yet the theme's old home showroom (model-viewer, 285 KB) and the
   membership plugin's Stripe library (262 KB) loaded here, on a phone, while the first picture waited (live 25.9:
   LCP 5.1-5.4 s with them). A link that carries the membership plugin's own parameters keeps everything. */
/* At print time, not by dequeue: other scripts list them as dependencies, so WordPress printed them anyway (1.72.274
   was rolled back by its own check for exactly that). */
if ( ! function_exists( 'nadlan_hp_pms_link' ) ) {
	function nadlan_hp_pms_link() {
		foreach ( array_keys( (array) $_GET ) as $k ) { if ( 0 === strpos( (string) $k, 'pms' ) ) { return true; } }
		return false;
	}
}
add_filter( 'script_loader_tag', function ( $tag, $handle ) {
	static $drop = array( 'nadlan-model-viewer', 'nadlan-mv-ux', 'nadlan-showroom-engine', 'pms-stripe-js', 'pms-stripe-script' );
	if ( ! in_array( $handle, $drop, true ) || ! nadlan_hp_on() ) { return $tag; }
	if ( 0 === strpos( $handle, 'pms-' ) && nadlan_hp_pms_link() ) { return $tag; }
	return '<!-- ' . esc_html( $handle ) . ': not needed on the home -->' . "\n";
}, 99, 2 );
add_filter( 'style_loader_tag', function ( $tag, $handle ) {
	if ( ! in_array( $handle, array( 'nadlan-showroom-engine', 'nadlan-home-showroom' ), true ) || ! nadlan_hp_on() ) { return $tag; }
	return '';
}, 99, 2 );

/* the first picture: one preload per media (the phone's portrait crop, the desktop's wide crop), fetched once */
add_action( 'wp_head', function () {
	if ( ! nadlan_hp_on() ) { return; }
	echo '<link rel="preload" as="image" href="' . esc_url( nadlan_hp_img( 'hero-m-780.jpg' ) ) . '" imagesrcset="' . esc_url( nadlan_hp_img( 'hero-m-780.jpg' ) ) . ' 780w" imagesizes="100vw" media="(max-width: 760px)" fetchpriority="high">' . "\n";
	echo '<link rel="preload" as="image" href="' . esc_url( nadlan_hp_img( 'hero-d-1400.jpg' ) ) . '" imagesrcset="' . esc_url( nadlan_hp_img( 'hero-d-1400.jpg' ) ) . ' 1400w, ' . esc_url( nadlan_hp_img( 'hero-d-1920.jpg' ) ) . ' 1920w" imagesizes="(max-width: 1440px) calc(100vw - 48px), 1392px" media="(min-width: 761px)" fetchpriority="high">' . "\n";
}, 2 );

/* the top's CSS, at the end of the head so it wins over the skin and the theme */
add_action( 'wp_head', function () {
	if ( ! nadlan_hp_on() ) { return; }
	$css = <<<'NLHPCSS'
body:has(#nlhp-top) .nlhv2-langbar,body:has(#nlhp-top) .nlhv2-browse{display:none!important}
html:has(#nlhp-top),html:has(#nlhp-top) body,body:has(#nlhp-top) .wp-site-blocks{overflow-x:clip!important;overflow-y:visible!important}
body:has(#nlhp-top) main.nlpc-main{padding-top:0!important}
body:has(#nlhp-top) .nlhv2-renewal,body:has(#nlhp-top) .nlhv2-rentals{content-visibility:auto;contain-intrinsic-size:auto 560px}
.nlhp-top{position:sticky;top:0;z-index:60;background:#fff;border-bottom:1px solid #e3e1da;font-family:Assistant,"Segoe UI",Arial,sans-serif;direction:rtl}
body.admin-bar .nlhp-top{top:32px}
.nlhp-top *,.nlhp-top *::before,.nlhp-top *::after,.nlhp-hero *,.nlhp-cats *{box-sizing:border-box}
.nlhp-top a{text-decoration:none!important}
.nlhp-top__in{display:flex;align-items:stretch;gap:22px;height:68px;max-width:1440px;margin:0 auto;padding:0 24px}
.nlhp-logo{display:flex;align-items:center;gap:10px;flex:none;color:#14212b!important}
.nlhp-logo__mark{width:38px;height:38px;border-radius:10px;background:#2f6f86;display:grid;place-items:center}
.nlhp-logo__mark i{display:flex;align-items:flex-end;gap:3px;height:17px}
.nlhp-logo__mark i b{display:block;width:4px;background:#fff;border-radius:1px}
.nlhp-logo__word{font:700 24px/1 "Noto Serif Hebrew",Georgia,serif;letter-spacing:-.01em;color:#14212b}
.nlhp-nav{display:flex;align-items:stretch;flex:1;min-width:0}
.nlhp-dd{position:static}
.nlhp-dd>summary{list-style:none;cursor:pointer}
.nlhp-dd>summary::-webkit-details-marker{display:none}
.nlhp-nav__item{display:flex;align-items:center;gap:6px;height:100%;padding:0 10px;font:600 15px/1 Assistant,"Segoe UI",Arial,sans-serif;color:#14212b!important;white-space:nowrap;border-bottom:2px solid transparent}
.nlhp-dd[open]>.nlhp-nav__item,.nlhp-nav__item:hover{color:#2f6f86!important;border-bottom-color:#2f6f86}
.nlhp-caret{display:inline-block;width:7px;height:7px;border-right:1.6px solid currentColor;border-bottom:1.6px solid currentColor;transform:translateY(-3px) rotate(45deg);opacity:.6}
.nlhp-dd[open] .nlhp-caret{transform:translateY(1px) rotate(225deg)}
.nlhp-top__end{display:flex;align-items:center;gap:8px;flex:none}
.nlhp-lang{position:relative}
.nlhp-lang>summary{display:inline-flex;align-items:center;gap:7px;height:38px;padding:0 12px;border-radius:999px;font:600 14px/1 Assistant,"Segoe UI",Arial,sans-serif;color:#3b4753}
.nlhp-lang__menu{position:absolute;top:calc(100% + 8px);left:0;min-width:170px;padding:6px;background:#fff;border:1px solid #e3e1da;border-radius:14px;box-shadow:0 14px 34px rgba(20,33,43,.12);z-index:70}
.nlhp-lang__menu .nlhv2-langs{display:grid!important;gap:2px!important;padding:0!important;background:none!important;border:0!important}
.nlhp-lang__menu a{display:block!important;padding:9px 12px!important;border-radius:10px!important;font:600 14.5px/1.2 Assistant,Arial,sans-serif!important;color:#14212b!important;background:none!important;border:0!important;text-align:start}
.nlhp-lang__menu a.on{background:#eee9dd!important}
.nlhp-post{display:inline-flex;align-items:center;height:40px;padding:0 18px;border-radius:999px;border:1.5px solid #14212b;font:700 14.5px/1 Assistant,"Segoe UI",Arial,sans-serif;color:#14212b!important;white-space:nowrap}
.nlhp-post:hover{background:#14212b;color:#fff!important}
.nlhp-ico{display:none;width:44px;height:44px;border-radius:12px;align-items:center;justify-content:center;color:#14212b!important;background:none;border:0;padding:0;cursor:pointer}
.nlhp-mega{position:absolute;inset-inline:0;top:100%;background:#fff;border-bottom:1px solid #e3e1da;box-shadow:0 18px 34px rgba(20,33,43,.10);z-index:65}
.nlhp-mega__in{display:grid;grid-template-columns:repeat(3,minmax(0,1fr)) 360px;gap:36px;max-width:1440px;margin:0 auto;padding:26px 24px 30px}
.nlhp-mega__col{min-width:0}
.nlhp-mega__h{font:700 12.5px/1 Assistant,Arial,sans-serif!important;letter-spacing:.07em;color:#6b7680!important;margin:0 0 10px!important;min-height:12.5px}
.nlhp-mega__col a{display:flex;justify-content:space-between;gap:10px;padding:8px 0;font:500 15.5px/1.3 Assistant,Arial,sans-serif;color:#14212b!important;border-bottom:1px solid #e3e1da}
.nlhp-mega__col a:hover{color:#2f6f86!important}
.nlhp-mega__col a span{color:#6b7680;font-size:13.5px;font-variant-numeric:tabular-nums}
.nlhp-mega__col .nlhp-mega__h+a{margin-top:0}
.nlhp-mega__col a+.nlhp-mega__h{margin-top:22px!important}
.nlhp-mega__col a.nlhp-mega__all{border:0;margin-top:12px;font-weight:700;color:#2f6f86!important}
.nlhp-mega__promo{display:grid;grid-template-rows:180px auto;border-radius:16px;overflow:hidden;border:1px solid #e3e1da;background:#fff;color:#14212b!important;grid-column:4}
.nlhp-mega__promo img{width:100%;height:100%;object-fit:cover;object-position:50% 40%;display:block}
.nlhp-mega__promo span{display:grid;gap:4px;padding:13px 16px 15px}
.nlhp-mega__promo small{font:500 13px/1.3 Assistant,Arial,sans-serif;color:#3b4753}
.nlhp-mega__promo b{font:600 18px/1.3 "Noto Serif Hebrew",Georgia,serif}
.nlhp-sheet__head,.nlhp-sheet__langs,.nlhp-sheet__post{display:none}
#nlhp-hero{position:relative;margin:20px 0 0;min-height:540px;border-radius:22px;overflow:hidden;display:flex;justify-content:flex-end;align-items:center;color:#fff;background:#1b3a47;direction:rtl}
#nlhp-hero picture{display:contents}
#nlhp-hero .nlhp-hero__img{position:absolute;inset:0;width:100%;height:100%;max-width:none;object-fit:cover;object-position:50% 42%;margin:0;border-radius:0}
#nlhp-hero::before{content:"";position:absolute;inset:0;z-index:1;background:linear-gradient(to right,rgba(10,28,36,.80) 0%,rgba(10,28,36,.58) 36%,rgba(10,28,36,.10) 62%,rgba(10,28,36,0) 75%)}
#nlhp-hero .nlhp-hero__body{position:relative;z-index:2;width:min(660px,100%);margin-inline-end:52px;padding:44px 0}
#nlhp-hero .nlhp-hero__kicker{font:700 13px/1 Assistant,Arial,sans-serif!important;letter-spacing:.08em;color:rgba(255,255,255,.86)!important;margin:0 0 14px!important}
#nlhp-hero h1{font:600 46px/1.12 "Noto Serif Hebrew",Georgia,serif!important;letter-spacing:-.005em;color:#fff!important;margin:0 0 12px!important;text-wrap:balance;text-align:start}
#nlhp-hero .nlhp-hero__lead{font:400 17.5px/1.55 Assistant,Arial,sans-serif!important;color:rgba(255,255,255,.93)!important;margin:0 0 22px!important;max-width:36em}
#nlhp-hero .nlhp-hero__cap{position:absolute;z-index:2;bottom:12px;right:16px;font:500 12px/1 Assistant,Arial,sans-serif;color:rgba(255,255,255,.82);text-shadow:0 1px 2px rgba(0,0,0,.45)}
.nlhp-n{direction:ltr;unicode-bidi:isolate;font-variant-numeric:tabular-nums}
#nlhp-hero .nlhp-search{max-width:none;margin:0;background:#fff;color:#14212b;border-radius:18px;padding:8px;box-shadow:0 20px 44px rgba(6,20,26,.30)}
#nlhp-hero .nlhp-search__tabs{display:flex;flex-wrap:nowrap;gap:4px;margin:0;padding:2px 2px 8px;overflow-x:auto;scrollbar-width:none}
#nlhp-hero .nlhp-search__tab{flex:none;display:inline-flex;align-items:center;min-height:0;height:34px;padding:0 15px;border:0;border-radius:999px;background:transparent;font:600 14.5px/1 Assistant,Arial,sans-serif;color:#3b4753;cursor:pointer}
#nlhp-hero .nlhp-search__tab.is-on{background:#14212b;color:#fff}
#nlhp-hero .nlhp-search__row{display:flex;gap:8px}
#nlhp-hero .nlhp-search__field{flex:1;min-width:0;display:flex;align-items:center;gap:10px;height:54px;margin:0;padding:0 16px;border-radius:12px;border:1px solid #e3e1da;background:#fbfaf7;color:#3b4753}
#nlhp-hero .nlhp-search__field input{flex:1;min-width:0;height:100%;border:0!important;background:transparent!important;box-shadow:none!important;outline:0;padding:0!important;margin:0;font:400 16.5px/1 Assistant,Arial,sans-serif;color:#14212b}
#nlhp-hero .nlhp-search__field:focus-within{border-color:#2f6f86;box-shadow:0 0 0 3px rgba(47,111,134,.18)}
#nlhp-hero .nlhp-search__go{flex:none;height:54px;padding:0 28px;border:0;border-radius:12px;background:#2f6f86;color:#fff;font:700 16.5px/1 Assistant,Arial,sans-serif;cursor:pointer}
#nlhp-hero .nlhp-search__go:hover{background:#255c70}
#nlhp-hero .nlhp-search__pop{display:flex;flex-wrap:wrap;align-items:center;gap:6px 14px;padding:12px 8px 4px;font:600 14px/1.3 Assistant,Arial,sans-serif}
#nlhp-hero .nlhp-search__pop span{color:#6b7680;font-weight:500}
#nlhp-hero .nlhp-search__pop a{color:#2f6f86!important;text-decoration:none!important;border-bottom:1px solid rgba(47,111,134,.4)}
.nlhp-cats{display:grid;grid-template-columns:repeat(8,minmax(0,1fr));gap:10px;margin:16px 0 0;direction:rtl}
.nlhp-cat{display:grid;gap:7px;align-content:start;padding:14px 14px 13px;background:#fff;border:1px solid #e3e1da;border-radius:14px;color:#14212b!important;text-decoration:none!important}
.nlhp-cat:hover{border-color:#2f6f86;box-shadow:0 12px 30px rgba(20,33,43,.08)}
.nlhp-cat__ico{width:40px;height:40px;border-radius:11px;background:#e8f1f3;display:grid;place-items:center;color:#1f4b5c}
.nlhp-cat b{font:700 15.5px/1.2 Assistant,Arial,sans-serif;color:#14212b}
.nlhp-cat>span:last-child{font:400 13px/1.3 Assistant,Arial,sans-serif;color:#6b7680}
@media (max-width:1360px){.nlhp-nav__plain{display:none}.nlhp-nav__item{padding:0 8px;font-size:14.5px}.nlhp-mega__in{grid-template-columns:repeat(3,minmax(0,1fr)) 300px}}
@media (max-width:1180px){.nlhp-top__in{gap:14px}.nlhp-nav__item{padding:0 6px;font-size:14px}.nlhp-lang>summary{padding:0 8px}.nlhp-cats{grid-template-columns:repeat(4,minmax(0,1fr))}}
@media (max-width:1060px){
.nlhp-top__in{height:60px}
.nlhp-ico{display:inline-flex}.nlhp-post,.nlhp-lang{display:none}
.nlhp-nav{display:none;position:fixed;inset:0;z-index:80;flex-direction:column;background:#fff;overflow-y:auto;overscroll-behavior:contain}
.nlhp-top.is-open .nlhp-nav{display:flex}
.nlhp-sheet__head{display:flex;align-items:center;justify-content:space-between;height:56px;padding:0 16px;border-bottom:1px solid #e3e1da;font:700 17px/1 Assistant,Arial,sans-serif;color:#14212b;flex:none;position:sticky;top:0;z-index:2;background:#fff}
.nlhp-sheet__close{width:44px;height:44px;border:0;background:none;font:400 30px/1 Arial,sans-serif;color:#14212b;cursor:pointer}
.nlhp-sheet__langs{display:block;padding:12px 16px;border-bottom:1px solid #e3e1da;flex:none}
.nlhp-sheet__langs .nlhv2-langs{display:flex!important;flex-wrap:nowrap!important;gap:6px!important;overflow-x:auto;padding:0!important;background:none!important;border:0!important}
.nlhp-sheet__langs a{flex:none;height:34px!important;padding:0 12px!important;border-radius:999px!important;display:inline-flex!important;align-items:center;border:1px solid #e3e1da!important;font:600 13.5px/1 Assistant,Arial,sans-serif!important;color:#3b4753!important;background:#fff!important}
.nlhp-sheet__langs a.on{background:#14212b!important;color:#fff!important;border-color:#14212b!important}
.nlhp-nav .nlhp-dd{border-bottom:1px solid #e3e1da}
.nlhp-nav .nlhp-nav__item{height:auto;min-height:54px;padding:0 16px;justify-content:space-between;font-size:16.5px;font-weight:700;border:0}
.nlhp-nav .nlhp-nav__plain{display:flex;border-bottom:1px solid #e3e1da}
.nlhp-nav .nlhp-mega{position:static;box-shadow:none;border:0}
.nlhp-nav .nlhp-mega__in{grid-template-columns:1fr 1fr;gap:0 14px;padding:0 16px 14px}
.nlhp-nav .nlhp-mega__col{display:contents}
.nlhp-nav .nlhp-mega__h{display:none}
.nlhp-nav .nlhp-mega__col a{font-size:15px;padding:10px 0}
.nlhp-nav .nlhp-mega__col a span{display:none}
.nlhp-nav .nlhp-mega__promo{display:none}
.nlhp-sheet__post{display:flex;align-items:center;justify-content:center;flex:none;height:48px;margin:16px;border-radius:999px;background:#2f6f86;color:#fff!important;font:700 16px/1 Assistant,Arial,sans-serif}
body.nlhp-lock{overflow:hidden}
}
@media (max-width:760px){
.nlhp-top__in{height:56px;padding:0 12px 0 8px}
.nlhp-logo__mark{width:32px;height:32px;border-radius:9px}.nlhp-logo__word{font-size:21px}
#nlhp-hero{margin:0;margin-inline:calc(50% - 50vw);min-height:470px;border-radius:0;display:block;padding:26px 16px 30px}
#nlhp-hero .nlhp-hero__img{object-position:50% 30%}
#nlhp-hero::before{background:linear-gradient(to bottom,rgba(10,28,36,.84) 0%,rgba(10,28,36,.74) 42%,rgba(10,28,36,.40) 68%,rgba(10,28,36,.12) 100%)}
#nlhp-hero .nlhp-hero__body{margin:0;padding:0;width:auto}
#nlhp-hero .nlhp-hero__kicker{font-size:12px!important;margin-bottom:10px!important}
#nlhp-hero h1{font-size:29px!important;line-height:1.16!important;margin-bottom:8px!important;text-shadow:0 1px 3px rgba(0,0,0,.35)}
#nlhp-hero .nlhp-hero__lead{font-size:15px!important;line-height:1.5!important;margin-bottom:16px!important;text-shadow:0 1px 3px rgba(0,0,0,.35)}
#nlhp-hero .nlhp-search{border-radius:16px;padding:6px}
#nlhp-hero .nlhp-search__tab{height:32px;padding:0 12px;font-size:14px}
#nlhp-hero .nlhp-search__row{flex-direction:column;gap:6px}
#nlhp-hero .nlhp-search__field{flex:none;height:50px}
#nlhp-hero .nlhp-search__field input{font-size:16px}
#nlhp-hero .nlhp-search__go{height:48px;width:100%}
#nlhp-hero .nlhp-search__pop{display:none}
#nlhp-hero .nlhp-hero__cap{bottom:8px;right:auto;left:12px;font-size:11px}
.nlhp-cats{grid-template-columns:repeat(4,minmax(0,1fr));gap:8px;margin-top:14px}
.nlhp-cat{justify-items:center;text-align:center;gap:6px;padding:10px 4px 9px;font-size:12.5px}
.nlhp-cat__ico{width:36px;height:36px;border-radius:10px}
.nlhp-cat b{font-size:12.5px;font-weight:600}
.nlhp-cat>span:last-child{display:none}
}
@media (prefers-reduced-motion:reduce){.nlhp-cat{transition:none}}
NLHPCSS;
	echo '<style id="nadlan-hp-css">' . $css . '</style>' . "\n";
}, 999 );

/* the menus: one open at a time, hover opens on a mouse, Esc and a click outside close; the phone's sheet */
add_action( 'wp_footer', function () {
	if ( ! nadlan_hp_on() ) { return; }
	$js = <<<'NLHPJS'
(function(){var top=document.getElementById("nlhp-top");if(!top)return;var dds=[].slice.call(top.querySelectorAll(".nlhp-dd"));
var fine=window.matchMedia("(hover: hover) and (pointer: fine)");var wide=window.matchMedia("(min-width: 1061px)");
function closeAll(ex){dds.forEach(function(d){if(d!==ex)d.open=false;});}
dds.forEach(function(d){d.addEventListener("toggle",function(){if(d.open&&wide.matches)closeAll(d);});
var t=null;d.addEventListener("mouseenter",function(){if(!fine.matches||!wide.matches)return;clearTimeout(t);t=setTimeout(function(){closeAll(d);d.open=true;},90);});
d.addEventListener("mouseleave",function(){if(!fine.matches||!wide.matches)return;clearTimeout(t);t=setTimeout(function(){d.open=false;},180);});
var sm=d.querySelector("summary");if(sm)sm.addEventListener("click",function(e){if(!fine.matches||!wide.matches||e.detail===0)return;e.preventDefault();clearTimeout(t);closeAll(d);d.open=true;});});
document.addEventListener("click",function(e){if(!top.contains(e.target))closeAll(null);});
var btn=top.querySelector(".nlhp-ico--menu");function sheet(o){top.classList.toggle("is-open",o);document.body.classList.toggle("nlhp-lock",o);if(btn)btn.setAttribute("aria-expanded",o?"true":"false");if(!o)closeAll(null);}
if(btn)btn.addEventListener("click",function(){sheet(!top.classList.contains("is-open"));});
var cl=top.querySelector("[data-nlhp-close]");if(cl)cl.addEventListener("click",function(){sheet(false);if(btn)btn.focus();});
document.addEventListener("keydown",function(e){if(e.key!=="Escape")return;var o=dds.filter(function(d){return d.open;})[0];if(top.classList.contains("is-open")){sheet(false);if(btn)btn.focus();}else if(o){o.open=false;var s=o.querySelector("summary");if(s)s.focus();}});
var sr=top.querySelector(".nlhp-ico--search");if(sr)sr.addEventListener("click",function(e){var i=document.querySelector("#nlhp-hero input[name=q]");if(!i)return;e.preventDefault();i.scrollIntoView({block:"center"});setTimeout(function(){i.focus();},250);});
[].slice.call(document.querySelectorAll("#nlhp-hero .nlhp-search__tab")).forEach(function(b,i,all){b.addEventListener("click",function(){all.forEach(function(x){x.setAttribute("aria-selected",x===b?"true":"false");});});});
})();
NLHPJS;
	echo '<script id="nadlan-hp-js">' . $js . '</script>' . "\n";
}, 99 );
