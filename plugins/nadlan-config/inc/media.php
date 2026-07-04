<?php
/**
 * nadlan-config - Rich media: 3D tour / video / floorplan (v1.10.0)
 *
 * 2026 reality (research): Matterport DROPPED by Zillow in Oct 2025 after the
 * CoStar acquisition; KUULA is the recommended free/affordable 3D tour platform
 * (Zillow-approved provider). We support Kuula iframe (JS-style for iOS+perf),
 * generic any-iframe (YouTube/Vimeo/CloudPano/Panoee), and a floorplan image/PDF.
 *
 * Adds three meta fields to nadlan_property (REST-exposed) - they were declared
 * in catalog-meta's parent module sparsely; here we ensure tour_url, video_url,
 * floorplan_url are registered + render a tabbed media block on single views.
 */

if ( ! defined( 'ABSPATH' ) ) { exit; }

if ( ! function_exists( 'nadlan_media_register_meta' ) ) {
	function nadlan_media_register_meta() {
		foreach ( array( 'tour_url' => 'string', 'video_url' => 'string', 'floorplan_url' => 'string' ) as $k => $t ) {
			register_post_meta( 'nadlan_property', $k, array(
				'show_in_rest' => true, 'single' => true, 'type' => $t,
				'auth_callback' => function ( $allowed, $meta_key, $post_id ) { return current_user_can( 'edit_post', (int) $post_id ); },
			) );
		}
	}
}
add_action( 'init', 'nadlan_media_register_meta', 14 );

/* ---- helper: extract Kuula post id from a Kuula URL ---- */
if ( ! function_exists( 'nadlan_media_kuula_id' ) ) {
	function nadlan_media_kuula_id( $url ) {
		if ( preg_match( '~kuula\.co/(?:post|share)/(?:([A-Za-z0-9]+)|collection/[A-Za-z0-9]+\?\S*card=([A-Za-z0-9]+))~i', $url, $m ) ) {
			return $m[1] ?: ( $m[2] ?? '' );
		}
		return '';
	}
}

if ( ! function_exists( 'nadlan_media_render' ) ) {
	function nadlan_media_render( $id ) {
		$tour  = (string) get_post_meta( $id, 'tour_url', true );
		$video = (string) get_post_meta( $id, 'video_url', true );
		$plan  = (string) get_post_meta( $id, 'floorplan_url', true );
		if ( ! $tour && ! $video && ! $plan ) { return ''; }
		$tabs = array();
		if ( $tour ) {
			$kid = nadlan_media_kuula_id( $tour );
			if ( $kid ) {
				$iframe = '<iframe class="nlmedia-frame" allowfullscreen allow="xr-spatial-tracking;gyroscope;accelerometer;fullscreen" scrolling="no" frameborder="0" src="https://kuula.co/share/' . esc_attr( $kid ) . '?fs=1&vr=0&autop=0&thumbs=1"></iframe>';
			} else {
				$iframe = '<iframe class="nlmedia-frame" allowfullscreen allow="xr-spatial-tracking;gyroscope;accelerometer;fullscreen" src="' . esc_url( $tour ) . '"></iframe>';
			}
			$tabs['tour'] = array( 'label' => 'סיור 3D', 'html' => $iframe );
		}
		if ( $video ) {
			$embed = wp_oembed_get( $video ) ?: '<iframe class="nlmedia-frame" allowfullscreen src="' . esc_url( $video ) . '"></iframe>';
			$tabs['video'] = array( 'label' => 'וידאו', 'html' => $embed );
		}
		if ( $plan ) {
			$html = ( preg_match( '~\.pdf(\?|$)~i', $plan ) )
				? '<iframe class="nlmedia-frame nlmedia-pdf" src="' . esc_url( $plan ) . '"></iframe>'
				: '<a href="' . esc_url( $plan ) . '" target="_blank" rel="noopener"><img loading="lazy" src="' . esc_url( $plan ) . '" alt="תכנית הדירה" class="nlmedia-plan"></a>';
			$tabs['plan'] = array( 'label' => 'תכנית הדירה', 'html' => $html );
		}
		ob_start(); ?>
<div class="nlmedia" dir="rtl">
	<div class="nlmedia-tabs">
		<?php $first = true; foreach ( $tabs as $k => $t ) : ?>
			<button class="nlmedia-tab<?php echo $first ? ' on' : ''; ?>" onclick="nadlanMediaTab(this,'<?php echo esc_js( $k ); ?>')"><?php echo esc_html( $t['label'] ); ?></button>
		<?php $first = false; endforeach; ?>
	</div>
	<?php $first = true; foreach ( $tabs as $k => $t ) : ?>
		<div class="nlmedia-pane<?php echo $first ? ' on' : ''; ?>" data-k="<?php echo esc_attr( $k ); ?>"><?php echo $t['html']; // already escaped/oembed ?></div>
	<?php $first = false; endforeach; ?>
</div>
<script>
function nadlanMediaTab(btn,k){
	var box=btn.closest('.nlmedia');
	box.querySelectorAll('.nlmedia-tab').forEach(function(b){b.classList.toggle('on',b===btn);});
	box.querySelectorAll('.nlmedia-pane').forEach(function(p){p.classList.toggle('on',p.dataset.k===k);});
}
</script>
<style>
.nlmedia{margin:18px 0}
.nlmedia-tabs{display:flex;gap:4px;margin-bottom:10px}
.nlmedia-tab{padding:8px 16px;border:1px solid rgba(27,26,23,.15);background:#fff;border-radius:4px;cursor:pointer;font:inherit}
.nlmedia-tab.on{background:#1B1A17;color:#FAF7F1;border-color:#1B1A17}
.nlmedia-pane{display:none}
.nlmedia-pane.on{display:block}
.nlmedia-frame{width:100%;aspect-ratio:16/9;border:0;border-radius:6px}
.nlmedia-pdf{aspect-ratio:1/1.2}
.nlmedia-plan{max-width:100%;border-radius:6px}
</style>
		<?php
		return ob_get_clean();
	}
}

/* Append media to property single (above the listings-ux engagement block) */
add_filter( 'the_content', function ( $content ) {
	if ( ! ( is_singular( 'nadlan_property' ) && in_the_loop() && is_main_query() ) ) { return $content; }
	return $content . nadlan_media_render( get_the_ID() );
}, 19 );

/* JSON-LD VideoObject when a video is present */
add_action( 'wp_head', function () {
	if ( ! is_singular( 'nadlan_property' ) ) { return; }
	$v = (string) get_post_meta( get_queried_object_id(), 'video_url', true );
	if ( ! $v ) { return; }
	echo "\n<script type=\"application/ld+json\">" . wp_json_encode( array(
		'@context' => 'https://schema.org', '@type' => 'VideoObject',
		'name' => get_the_title(), 'contentUrl' => $v,
		'thumbnailUrl' => get_the_post_thumbnail_url() ?: home_url( '/' ),
		'uploadDate' => get_the_date( 'c' ),
	), JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES ) . "</script>\n";
}, 21 );
