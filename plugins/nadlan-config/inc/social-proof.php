<?php
/**
 * nadlan-config — Social proof + "what's hot" widget (v1.40.0 / shark #14)
 *
 * Three trust signals appended to the homepage that convert undecided visitors:
 *  1. Live counters: "X בעלי מקצוע · Y פרויקטים · Z מונחים" (already in DB).
 *  2. "Just claimed" feed: the last 3 contractors who claimed their card —
 *     creates urgency for other contractors viewing the site ("they're moving").
 *  3. "What's popular this week" — top-viewed professionals (uses a simple
 *     post_meta view counter the directory cards stamp on click).
 *
 * Pure conversion psychology: numbers that grow + names that just acted are
 * the strongest social-proof on directory sites (Houzz, Thumbtack pattern).
 *
 * Shortcode: [nadlan_social_proof] for placement anywhere.
 */
if ( ! defined( 'ABSPATH' ) ) { exit; }

if ( ! function_exists( 'nadlan_sp_render' ) ) {
	function nadlan_sp_render() {
		$pros  = (int) wp_count_posts( 'nadlan_professional' )->publish;
		$proj  = (int) wp_count_posts( 'nadlan_project' )->publish;
		$terms = (int) wp_count_posts( 'nadlan_term' )->publish;

		// recently claimed (last 3 verified)
		$claimed = get_posts( array(
			'post_type' => 'nadlan_professional', 'post_status' => 'publish',
			'posts_per_page' => 3,
			'meta_query' => array( array( 'key' => 'claim_status', 'value' => 'verified' ) ),
			'orderby' => 'meta_value_num', 'meta_key' => 'verified_at', 'order' => 'DESC',
		) );

		// top-viewed (uses post_meta 'view_count' if present)
		$top = get_posts( array(
			'post_type' => 'nadlan_professional', 'post_status' => 'publish',
			'posts_per_page' => 4,
			'meta_query' => array( array( 'key' => 'view_count', 'value' => 0, 'type' => 'NUMERIC', 'compare' => '>' ) ),
			'orderby' => 'meta_value_num', 'meta_key' => 'view_count', 'order' => 'DESC',
		) );

		ob_start(); ?>
<section class="nlsp" dir="rtl">
	<div class="nlsp-stats">
		<div class="nlsp-stat"><b><?php echo number_format( $pros ); ?></b><span>בעלי מקצוע</span></div>
		<div class="nlsp-stat"><b><?php echo number_format( $proj ); ?></b><span>פרויקטים</span></div>
		<div class="nlsp-stat"><b><?php echo number_format( $terms ); ?></b><span>מונחים</span></div>
		<div class="nlsp-stat"><b>data.gov.il</b><span>מקור רשמי</span></div>
	</div>

	<?php if ( $claimed ) : ?>
	<div class="nlsp-block">
		<h3>הצטרפו לאחרונה</h3>
		<ul class="nlsp-list">
			<?php foreach ( $claimed as $c ) :
				$city = get_post_meta( $c->ID, 'city', true );
				$pm = function_exists( 'nadlan_dir_prof_meta' ) ? nadlan_dir_prof_meta( (string) get_post_meta( $c->ID, 'profession', true ) ) : array( 'label' => '', 'color' => '#9C7A3C' );
			?>
			<li><a href="<?php echo esc_url( get_permalink( $c ) ); ?>" style="--pc:<?php echo esc_attr( $pm['color'] ); ?>"><span class="nlsp-dot">●</span><b><?php echo esc_html( get_the_title( $c ) ); ?></b><span><?php echo esc_html( $pm['label'] ); ?> · <?php echo esc_html( $city ); ?></span></a></li>
			<?php endforeach; ?>
		</ul>
	</div>
	<?php endif; ?>

	<?php if ( $top ) : ?>
	<div class="nlsp-block">
		<h3>פופולריים השבוע</h3>
		<ul class="nlsp-list">
			<?php foreach ( $top as $c ) :
				$city = get_post_meta( $c->ID, 'city', true );
				$views = (int) get_post_meta( $c->ID, 'view_count', true );
			?>
			<li><a href="<?php echo esc_url( get_permalink( $c ) ); ?>"><span>🔥</span><b><?php echo esc_html( get_the_title( $c ) ); ?></b><span><?php echo esc_html( $city ); ?> · <?php echo number_format( $views ); ?> צפיות</span></a></li>
			<?php endforeach; ?>
		</ul>
	</div>
	<?php endif; ?>
</section>
<style>
.nlsp{font-family:var(--font-sans,Heebo,sans-serif);direction:rtl;max-width:1240px;margin:40px auto;padding:0 24px}
.nlsp-stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));gap:12px;background:linear-gradient(135deg,#1B1A17,#3a3329);color:#fff;border-radius:14px;padding:24px;margin-bottom:30px}
.nlsp-stat{text-align:center}
.nlsp-stat b{display:block;font-family:var(--font-serif,"Frank Ruhl Libre",serif);font-size:30px;color:#F3D9A6;line-height:1}
.nlsp-stat span{font-size:12px;color:rgba(255,255,255,.7);margin-top:4px;display:block}
.nlsp-block{margin:24px 0}
.nlsp-block h3{font-family:var(--font-serif,serif);font-size:18px;font-weight:600;color:#1B1A17;margin:0 0 12px}
.nlsp-list{list-style:none;padding:0;margin:0;display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:10px}
.nlsp-list a{display:flex;align-items:center;gap:10px;background:#fff;border:1px solid rgba(27,26,23,.1);border-radius:10px;padding:11px 14px;text-decoration:none;color:inherit;font-size:13.5px;transition:transform .15s,border-color .15s}
.nlsp-list a:hover{transform:translateY(-2px);border-color:var(--pc,#9C7A3C)}
.nlsp-list b{font-weight:600;color:#1B1A17;flex:1}
.nlsp-list a span:last-child{font-size:12px;color:#7a7a7a}
.nlsp-dot{color:#10b981;font-size:10px}
</style>
<?php
		return ob_get_clean();
	}
}

add_shortcode( 'nadlan_social_proof', 'nadlan_sp_render' );

/* Inject on the homepage at the end of content */
add_filter( 'the_content', function ( $content ) {
	if ( ! is_front_page() || ! in_the_loop() || ! is_main_query() ) { return $content; }
	return $content . nadlan_sp_render();
}, 55 );

/* Lightweight view counter on professional + project profile pages (no plugin needed) */
add_action( 'wp_head', function () {
	if ( ! is_singular( array( 'nadlan_professional', 'nadlan_project' ) ) ) { return; }
	$id = get_queried_object_id();
	if ( ! $id ) { return; }
	// throttle per-IP per-page per-hour
	$ip = $_SERVER['REMOTE_ADDR'] ?? '0';
	$tk = 'nlvc_' . $id . '_' . md5( $ip );
	if ( get_transient( $tk ) ) { return; }
	set_transient( $tk, 1, HOUR_IN_SECONDS );
	$v = (int) get_post_meta( $id, 'view_count', true );
	update_post_meta( $id, 'view_count', $v + 1 );
}, 999 );
