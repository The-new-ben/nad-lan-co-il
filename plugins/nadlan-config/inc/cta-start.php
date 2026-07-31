<?php
/**
 * cta-start.php - the "start here" engagement layer (owner order 2026-07-13).
 *
 * "You can't find where you start... a button people cannot miss, not gold,
 *  not overflowing... where it's free, say it's free... engagement on all
 *  pages."
 *
 * One context-aware primary action per surface, rendered as a floating pill
 * (bottom-center, clear of the AI fab bottom-start and the WhatsApp fab
 * bottom-end). Terracotta - the site's action color, not gold. A surface that
 * already IS the action (the wizard page itself, checkout-like flows) gets
 * nothing. Filterable via nadlan_cta_start_map.
 */

if ( ! defined( 'ABSPATH' ) ) { exit; }

if ( ! function_exists( 'nadlan_cta_start_for_request' ) ) {
	// returns array( label, url, free_badge ) or null
	function nadlan_cta_start_for_request() {
		$map = array();
		if ( is_post_type_archive( 'nadlan_property' ) || is_singular( 'nadlan_property' ) ) {
			$map = array( 'פרסמו את הדירה שלכם', home_url( '/post-listing/' ), true );
		} elseif ( is_page( array( 'urban-renewal' ) ) || is_page( array( 'tama-38', 'pinui-binui' ) ) ) {
			$map = array( 'בדקו את הבניין שלכם', home_url( '/urban-renewal/check/' ), true );
		} elseif ( is_post_type_archive( 'nadlan_project' ) || is_singular( 'nadlan_project' ) ) {
			$map = array(); // project pages carry their own buy-flow CTA
		} elseif ( is_singular( 'nadlan_term' ) || is_post_type_archive( 'nadlan_term' ) ) {
			$map = array( 'מצאו איש מקצוע מומלץ', home_url( '/professionals/' ), false );
		} elseif ( is_post_type_archive( 'nadlan_professional' ) || is_singular( 'nadlan_professional' ) ) {
			$map = array(); // directory has its own contact actions
		} elseif ( is_page( 'rentals' ) || is_page( 'my-rentals' ) ) {
			$map = array(); // product landing owns its CTAs
		}
		$map = apply_filters( 'nadlan_cta_start_map', $map );
		return ( is_array( $map ) && count( $map ) >= 2 ) ? $map : null;
	}
}

add_action( 'wp_footer', function () {
	if ( is_admin() || is_front_page() ) { return; }
	$cta = nadlan_cta_start_for_request();
	if ( ! $cta ) { return; }
	list( $label, $url ) = $cta;
	$free = ! empty( $cta[2] );
	?>
<div class="nlcta-start" role="complementary" aria-label="התחילו כאן">
	<a href="<?php echo esc_url( $url ); ?>">
		<span class="nlcta-start__go">▶</span>
		<?php echo esc_html( $label ); ?>
		<?php if ( $free ) : ?><b>חינם</b><?php endif; ?>
	</a>
</div>
<style>
.nlcta-start{position:fixed;bottom:calc(env(safe-area-inset-bottom,0px) + 14px);left:50%;transform:translateX(-50%);z-index:99970;direction:rtl}
.nlcta-start a{display:inline-flex;align-items:center;gap:9px;background:#C2563A;color:#FAF7F1;text-decoration:none;font:700 14.5px/1 Heebo,sans-serif;border-radius:999px;padding:14px 22px;box-shadow:0 16px 38px -12px rgba(194,86,58,.6),0 2px 8px rgba(27,26,23,.18);border:1px solid rgba(250,247,241,.25);animation:nlctaIn .5s cubic-bezier(.22,1,.36,1)}
.nlcta-start a:hover{background:#A9482F}
.nlcta-start__go{font-size:10px;opacity:.85}
.nlcta-start b{background:#FAF7F1;color:#C2563A;border-radius:999px;padding:3px 9px;font-size:11.5px}
@keyframes nlctaIn{from{opacity:0;transform:translateY(16px)}to{opacity:1;transform:none}}
@media(max-width:560px){.nlcta-start a{font-size:13px;padding:12px 18px}}
@media print{.nlcta-start{display:none}}
</style>
	<?php
}, 60 );
