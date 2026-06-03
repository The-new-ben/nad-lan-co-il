<?php
/**
 * nadlan-config — Public profile extras (v1.41.0)
 *
 * Renders the new studio fields (social icons + video embed) on single
 * professional/project/property pages, just below the body content.
 * Photos already render via cards-render.php's gallery (reads photos_csv).
 */
if ( ! defined( 'ABSPATH' ) ) { exit; }

if ( ! function_exists( 'nadlan_pe_video_embed' ) ) {
	function nadlan_pe_video_embed( $url ) {
		$url = esc_url_raw( $url );
		if ( ! $url ) { return ''; }
		// YouTube
		if ( preg_match( '~youtu(?:\.be|be\.com)/(?:watch\?v=)?([A-Za-z0-9_-]{6,})~', $url, $m ) ) {
			$id = $m[1];
			return '<div class="nlpe-video"><iframe src="https://www.youtube.com/embed/' . esc_attr( $id ) . '" loading="lazy" allow="accelerometer; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe></div>';
		}
		// Vimeo
		if ( preg_match( '~vimeo\.com/(\d+)~', $url, $m ) ) {
			return '<div class="nlpe-video"><iframe src="https://player.vimeo.com/video/' . esc_attr( $m[1] ) . '" loading="lazy" allow="autoplay; fullscreen; picture-in-picture" allowfullscreen></iframe></div>';
		}
		return '';
	}
}

if ( ! function_exists( 'nadlan_pe_render' ) ) {
	function nadlan_pe_render( $id ) {
		$socials = array(
			'social_facebook'  => array( 'Facebook',  '📘', '#1877F2' ),
			'social_instagram' => array( 'Instagram', '📸', '#E4405F' ),
			'social_tiktok'    => array( 'TikTok',    '🎵', '#000' ),
			'social_youtube'   => array( 'YouTube',   '▶',  '#FF0000' ),
		);
		$links = '';
		foreach ( $socials as $key => $info ) {
			$url = (string) get_post_meta( $id, $key, true );
			if ( ! $url ) { continue; }
			$links .= '<a class="nlpe-soc" href="' . esc_url( $url ) . '" target="_blank" rel="noopener" style="--c:' . esc_attr( $info[2] ) . '"><span>' . esc_html( $info[1] ) . '</span>' . esc_html( $info[0] ) . '</a>';
		}
		$website = (string) get_post_meta( $id, 'website', true );
		if ( $website ) {
			$links .= '<a class="nlpe-soc" href="' . esc_url( $website ) . '" target="_blank" rel="noopener" style="--c:#9C7A3C"><span>🌐</span>אתר</a>';
		}
		$video_html = nadlan_pe_video_embed( (string) get_post_meta( $id, 'video_url', true ) );
		if ( ! $links && ! $video_html ) { return ''; }
		ob_start(); ?>
<section class="nlpe" dir="rtl">
	<?php if ( $links ) : ?><div class="nlpe-socials"><?php echo $links; ?></div><?php endif; ?>
	<?php if ( $video_html ) : ?><?php echo $video_html; ?><?php endif; ?>
</section>
<style>
.nlpe{font-family:var(--font-sans,Heebo,sans-serif);direction:rtl;margin:24px 0;display:flex;flex-direction:column;gap:18px}
.nlpe-socials{display:flex;gap:10px;flex-wrap:wrap}
.nlpe-soc{display:inline-flex;align-items:center;gap:8px;background:var(--c,#9C7A3C);color:#fff;padding:10px 18px;border-radius:24px;text-decoration:none;font-weight:600;font-size:13.5px;transition:transform .15s,filter .2s}
.nlpe-soc:hover{transform:translateY(-2px);filter:brightness(1.1)}
.nlpe-soc span{font-size:16px}
.nlpe-video{position:relative;aspect-ratio:16/9;border-radius:14px;overflow:hidden;background:#000}
.nlpe-video iframe{position:absolute;inset:0;width:100%;height:100%;border:0}
</style>
<?php
		return ob_get_clean();
	}
}

add_filter( 'the_content', function ( $content ) {
	if ( ! is_singular( array( 'nadlan_professional', 'nadlan_project', 'nadlan_property' ) ) || ! in_the_loop() || ! is_main_query() ) { return $content; }
	return $content . nadlan_pe_render( get_the_ID() );
}, 23 );
