<?php
/**
 * nadlan-config — Branded archive grid for directory CPTs (v1.28.0)
 *
 * The nadlan_professional / nadlan_project / nadlan_property archives are now linked
 * from the homepage, nav, footer and /catalog/ — but they were rendering through the
 * theme's default archive loop, which shows these data-only CPTs (no editor body) as
 * blank/plain rows. With 1500+ imported professionals that looked broken.
 *
 * This module intercepts those archives (template_redirect, like city-hubs) and renders
 * a clean, branded, paginated CARD GRID built from the real meta — name, city,
 * classification, registry number, claim badge — matching the catalog skin. Facets bar
 * on top (reuses [nadlan_facets]). Keeps the theme header/footer so it stays on-brand.
 *
 * Opt-out: define NADLAN_DISABLE_ARCHIVE_GRID to fall back to the theme template.
 */

if ( ! defined( 'ABSPATH' ) ) { exit; }

if ( ! function_exists( 'nadlan_archive_grid_dispatch' ) ) {
	function nadlan_archive_grid_dispatch() {
		if ( defined( 'NADLAN_DISABLE_ARCHIVE_GRID' ) && NADLAN_DISABLE_ARCHIVE_GRID ) { return; }
		if ( ! is_post_type_archive( array( 'nadlan_professional', 'nadlan_project', 'nadlan_property' ) ) ) { return; }
		if ( is_admin() ) { return; }
		nadlan_archive_grid_render();
		exit;
	}
}
add_action( 'template_redirect', 'nadlan_archive_grid_dispatch', 6 );

if ( ! function_exists( 'nadlan_archive_grid_render' ) ) {
	function nadlan_archive_grid_render() {
		global $wp_query;
		$pt = get_query_var( 'post_type' );
		if ( is_array( $pt ) ) { $pt = reset( $pt ); }

		$meta = array(
			'nadlan_professional' => array(
				'h1'  => 'בעלי מקצוע רשומים',
				'sub' => 'קבלנים, שמאים ומפקחים מאומתים — מתוך פנקס הקבלנים הרשומים (gov.il). סינון לפי עיר, סיווג וענף.',
				'badge' => 'קבלן רשום',
			),
			'nadlan_project' => array(
				'h1'  => 'פרויקטים והתחדשות עירונית',
				'sub' => 'תמ״א 38, פינוי-בינוי ובנייה חדשה — מספר תוכנית, יזם, סטטוס ויחידות דיור.',
				'badge' => 'פרויקט',
			),
			'nadlan_property' => array(
				'h1'  => 'נכסים למכירה והשקעה',
				'sub' => 'דירות ובתים עם בדיקה משפטית מקדימה — מחיר, חדרים, מ״ר ושכונה.',
				'badge' => 'נכס',
			),
		);
		$L = $meta[ $pt ] ?? $meta['nadlan_professional'];
		$total = (int) $wp_query->found_posts;
		$paged = max( 1, (int) get_query_var( 'paged' ) );
		$pages = (int) $wp_query->max_num_pages;

		get_header();
		echo nadlan_archive_grid_css();
		?>
<div class="nlag" dir="rtl">
	<nav class="nlag-crumbs"><a href="<?php echo esc_url( home_url( '/' ) ); ?>">בית</a><span>›</span><span><?php echo esc_html( $L['h1'] ); ?></span></nav>
	<header class="nlag-head">
		<h1><?php echo esc_html( $L['h1'] ); ?></h1>
		<p class="nlag-sub"><?php echo esc_html( $L['sub'] ); ?></p>
		<p class="nlag-count"><strong><?php echo number_format( $total ); ?></strong> רשומות</p>
	</header>

	<?php if ( shortcode_exists( 'nadlan_facets' ) ) { echo do_shortcode( '[nadlan_facets type="' . esc_attr( $pt ) . '"]' ); } ?>

	<?php if ( have_posts() ) : ?>
	<div class="nlag-grid">
		<?php while ( have_posts() ) : the_post();
			$id   = get_the_ID();
			$city = trim( (string) get_post_meta( $id, 'city', true ) );
			echo '<a class="nlag-card" href="' . esc_url( get_permalink() ) . '">';
			echo '<span class="nlag-badge">' . esc_html( $L['badge'] ) . '</span>';
			echo '<h3>' . esc_html( get_the_title() ) . '</h3>';
			if ( $city ) { echo '<span class="nlag-city">' . esc_html( $city ) . '</span>'; }
			echo nadlan_archive_card_meta( $id, $pt );
			$claimed = get_post_meta( $id, 'claim_status', true ) === 'verified';
			if ( $claimed ) { echo '<span class="nlag-verified">✓ מאומת</span>'; }
			echo '<span class="nlag-go">לכרטיס ←</span>';
			echo '</a>';
		endwhile; ?>
	</div>

	<?php if ( $pages > 1 ) : ?>
	<nav class="nlag-pager">
		<?php
		echo paginate_links( array(
			'total'     => $pages,
			'current'   => $paged,
			'prev_text' => '← הקודם',
			'next_text' => 'הבא →',
			'mid_size'  => 2,
		) );
		?>
	</nav>
	<?php endif; ?>

	<?php else : ?>
	<p class="nlag-empty">לא נמצאו רשומות התואמות את הסינון. <a href="<?php echo esc_url( get_post_type_archive_link( $pt ) ); ?>">איפוס סינון</a></p>
	<?php endif; ?>
</div>
		<?php
		get_footer();
	}
}

/* type-specific card meta line */
if ( ! function_exists( 'nadlan_meta_norm' ) ) {
	/* collapse the whitespace padding gov.il leaves in CKAN fields */
	function nadlan_meta_norm( $s ) { return trim( preg_replace( '/\s+/u', ' ', (string) $s ) ); }
}
if ( ! function_exists( 'nadlan_archive_card_meta' ) ) {
	function nadlan_archive_card_meta( $id, $pt ) {
		if ( $pt === 'nadlan_professional' ) {
			$cls = nadlan_meta_norm( get_post_meta( $id, 'classification', true ) );
			$reg = nadlan_meta_norm( get_post_meta( $id, 'registry_number', true ) );
			$cls = mb_strlen( $cls ) > 46 ? mb_substr( $cls, 0, 46 ) . '…' : $cls;
			$out = $cls ? '<span class="nlag-spec">' . esc_html( $cls ) . '</span>' : '';
			$out .= $reg ? '<span class="nlag-reg">רשם הקבלנים #' . esc_html( $reg ) . '</span>' : '';
			return $out;
		}
		if ( $pt === 'nadlan_project' ) {
			$u  = (int) get_post_meta( $id, 'num_units', true );
			$st = nadlan_meta_norm( get_post_meta( $id, 'project_status', true ) );
			$bits = array_filter( array( $u ? $u . ' יח״ד' : '', $st ) );
			return $bits ? '<span class="nlag-spec">' . esc_html( implode( ' · ', $bits ) ) . '</span>' : '';
		}
		// property
		$pr = (float) get_post_meta( $id, 'price', true );
		$rm = get_post_meta( $id, 'rooms', true );
		$sq = get_post_meta( $id, 'size_sqm', true );
		$bits = array_filter( array( $rm ? $rm . " חד'" : '', $sq ? $sq . ' מ״ר' : '' ) );
		$out  = $pr ? '<span class="nlag-price">₪' . number_format( $pr ) . '</span>' : '';
		$out .= $bits ? '<span class="nlag-spec">' . esc_html( implode( ' · ', $bits ) ) . '</span>' : '';
		return $out;
	}
}

if ( ! function_exists( 'nadlan_archive_grid_css' ) ) {
	function nadlan_archive_grid_css() {
		return '<style>
.nlag{font-family:var(--font-sans,Heebo,sans-serif);max-width:1240px;margin:0 auto;padding:28px 24px 48px;direction:rtl;color:#1B1A17}
.nlag-crumbs{font-size:13px;color:#9a9a9a;margin-bottom:14px}
.nlag-crumbs a{color:#9C7A3C;text-decoration:none}.nlag-crumbs span{margin:0 6px}
.nlag-head{margin-bottom:22px}
.nlag-head h1{font-family:var(--font-serif,"Frank Ruhl Libre",serif);font-weight:500;font-size:34px;margin:0 0 8px;letter-spacing:-.015em}
.nlag-sub{font-size:15px;color:#6b6b6b;margin:0 0 8px;max-width:720px;line-height:1.6}
.nlag-count{font-size:14px;color:#5a5a5a;margin:0}.nlag-count strong{color:#9C7A3C;font-size:16px}
.nlag-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:16px;margin:22px 0}
.nlag-card{position:relative;display:flex;flex-direction:column;gap:6px;background:linear-gradient(135deg,#fff,#FBF9F5);border:1px solid rgba(27,26,23,.1);border-radius:14px;padding:20px;text-decoration:none;color:inherit;transition:transform .22s,box-shadow .22s,border-color .22s;min-height:170px}
.nlag-card:hover{transform:translateY(-5px);box-shadow:0 14px 32px rgba(27,26,23,.12);border-color:rgba(156,122,60,.45)}
.nlag-badge{align-self:flex-start;background:linear-gradient(135deg,#9C7A3C,#B89254);color:#fff;font-size:10px;letter-spacing:.1em;font-weight:600;padding:4px 10px;border-radius:20px}
.nlag-card h3{font-family:var(--font-serif,serif);font-weight:500;font-size:18px;margin:6px 0 2px;line-height:1.35}
.nlag-city{font-size:12px;letter-spacing:.08em;color:#9C7A3C;font-weight:600}
.nlag-spec{font-size:12.5px;color:#5a5a5a;line-height:1.5}
.nlag-reg{font-size:11px;color:#999}
.nlag-price{font-family:var(--font-serif,serif);font-size:18px;color:#1B1A17;font-weight:500}
.nlag-verified{font-size:11px;color:#2e7d32;font-weight:600}
.nlag-go{margin-top:auto;color:#9C7A3C;font-weight:600;font-size:13px;transition:transform .2s}
.nlag-card:hover .nlag-go{transform:translateX(-4px)}
.nlag-pager{display:flex;justify-content:center;gap:6px;flex-wrap:wrap;margin-top:30px}
.nlag-pager .page-numbers{display:inline-block;padding:9px 14px;border:1px solid rgba(27,26,23,.14);border-radius:8px;text-decoration:none;color:#1B1A17;font-size:14px}
.nlag-pager .page-numbers.current{background:#1B1A17;color:#FAF7F1;border-color:#1B1A17}
.nlag-pager a.page-numbers:hover{background:#9C7A3C;color:#fff;border-color:#9C7A3C}
.nlag-empty{text-align:center;padding:40px;color:#6b6b6b}
.nlag-empty a{color:#9C7A3C}
@media(max-width:600px){.nlag-head h1{font-size:27px}.nlag-grid{grid-template-columns:repeat(2,1fr);gap:12px}.nlag-card{padding:16px;min-height:150px}}
</style>';
	}
}
