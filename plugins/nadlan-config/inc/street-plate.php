<?php
/**
 * nadlan-config - the street sign on a project card that has no picture of its own (HAD-743).
 * 1.72.684 put a large sign over a mini map; Ben (15.11.2026) found it heavy and asked for a small sign on the brand picture,
 * which also advertises the site. So: the shared default picture stays (HAD-740), and a small municipal enamel sign with the
 * project's street and city hangs in its corner, with one line counting the REAL new projects within a kilometre (our own points,
 * assets/deals/projects.json, distinct places only). Design: Claude Design canvas board 7 (docs/design-lab/deals-map/).
 */

if ( ! defined( 'ABSPATH' ) ) { exit; }

if ( ! function_exists( 'nadlan_sp_points' ) ) {
	/** [[lng, lat], ...] distinct project places, read once per request. */
	function nadlan_sp_points() {
		static $pts = null;
		if ( null !== $pts ) { return $pts; }
		$pts = array();
		$f   = dirname( __DIR__ ) . '/assets/deals/projects.json';
		$raw = is_readable( $f ) ? json_decode( (string) file_get_contents( $f ), true ) : null; // phpcs:ignore WordPress.WP.AlternativeFunctions
		if ( ! is_array( $raw ) ) { return $pts; }
		$seen = array();
		foreach ( $raw as $p ) {
			if ( ! is_array( $p ) || ! isset( $p[0], $p[1] ) ) { continue; }
			$k = round( (float) $p[0], 5 ) . ',' . round( (float) $p[1], 5 );
			if ( isset( $seen[ $k ] ) ) { continue; }
			$seen[ $k ] = 1;
			$pts[] = array( (float) $p[0], (float) $p[1] );
		}
		return $pts;
	}
}

if ( ! function_exists( 'nadlan_sp_street' ) ) {
	/** The street (or place) name from the card title "רחוב, עיר: סוג", else the neighbourhood, else the city. */
	function nadlan_sp_street( $title, $hood, $city ) {
		$t = trim( wp_strip_all_tags( html_entity_decode( (string) $title, ENT_QUOTES, 'UTF-8' ) ) );
		if ( preg_match( '/^([^,:]{2,34})[,:]/u', $t, $m ) ) { return trim( $m[1] ); }
		if ( '' !== trim( (string) $hood ) ) { return trim( (string) $hood ); }
		return trim( (string) $city );
	}
}

if ( ! function_exists( 'nadlan_sp_count' ) ) {
	/** Distinct project places within 1 km of the point, the project itself left out. */
	function nadlan_sp_count( $lat, $lng ) {
		if ( ! $lat || ! $lng ) { return 0; }
		$n = 0; $k = cos( deg2rad( $lat ) ) * 111.32;
		foreach ( nadlan_sp_points() as $p ) {
			$dx = ( $p[0] - $lng ) * $k; $dy = ( $p[1] - $lat ) * 110.57;
			if ( abs( $dx ) < 0.0005 && abs( $dy ) < 0.0005 ) { continue; }
			if ( $dx * $dx + $dy * $dy <= 1.0 ) { $n++; }
		}
		return $n;
	}
}

if ( ! function_exists( 'nadlan_sp_html' ) ) {
	/** The overlay printed over the default picture: the small sign in the corner and the count line. '' when no name. */
	function nadlan_sp_html( $id, $kind_label = '' ) {
		$city = function_exists( 'nadlan_meta_norm' ) ? nadlan_meta_norm( get_post_meta( $id, 'city', true ) ) : (string) get_post_meta( $id, 'city', true );
		$street = nadlan_sp_street( get_the_title( $id ), (string) get_post_meta( $id, 'neighborhood', true ), $city );
		if ( '' === $street ) { return ''; }
		$sub = ( $street === $city ) ? 'ישראל' : $city;
		$len = function_exists( 'mb_strlen' ) ? mb_strlen( $street, 'UTF-8' ) : strlen( $street );
		$fs  = $len <= 9 ? 18 : ( $len <= 14 ? 15 : 13 );
		$n   = nadlan_sp_count( (float) get_post_meta( $id, 'lat', true ), (float) get_post_meta( $id, 'lng', true ) );
		ob_start(); ?>
<span class="nlsp" aria-hidden="true">
	<span class="nlsp-hang"><span class="nlsp-rod"></span>
		<span class="nlsp-sign"><span class="nlsp-glint"></span>
			<span class="nlsp-face"><span class="nlsp-st" style="font-size:<?php echo (int) $fs; ?>px"><?php echo esc_html( $street ); ?></span><span class="nlsp-rule"></span><span class="nlsp-city"><?php echo esc_html( $sub ); ?></span></span>
		</span>
	</span>
	<?php if ( $n > 0 ) : ?><span class="nlsp-count"><i></i><b><?php echo (int) $n; ?></b> פרויקטים חדשים בק״מ</span><?php endif; ?>
</span>
		<?php
		return (string) ob_get_clean();
	}
}

if ( ! function_exists( 'nadlan_sp_assets' ) ) {
	/** CSS and the one-time swing script, printed once per page before the first sign. */
	function nadlan_sp_assets() {
		static $done = false;
		if ( $done ) { return ''; }
		$done = true;
		$css = '.nldc-media.has-plate{position:relative;container-type:inline-size}'
			. '.nlsp{position:absolute;inset:0;pointer-events:none;font-family:"IBM Plex Sans Hebrew",Heebo,system-ui,sans-serif;direction:rtl}'
			. '.nlsp-hang{position:absolute;top:16px;right:12px;display:block;transform-origin:50% -12px;zoom:var(--sz,1)}'
			. '.nlsp.is-in .nlsp-hang{animation:nlsp-swing 1.6s cubic-bezier(.25,.8,.3,1) both}'
			. '.nlsp-rod{position:absolute;top:-12px;left:50%;width:3px;height:14px;margin-left:-1.5px;background:linear-gradient(#B9C3CA,#6F7E88);border-radius:1px}'
			. '.nlsp-sign{position:relative;display:block;background:linear-gradient(180deg,#2A4FA8 0%,#1D3F8F 55%,#183679 100%);border-radius:7px;padding:3px;box-shadow:inset 0 1px 0 rgba(255,255,255,.35),0 6px 14px rgba(15,29,38,.35);overflow:hidden}'
			. '.nlsp-glint{position:absolute;top:0;bottom:0;left:-45%;width:34%;background:linear-gradient(90deg,transparent,rgba(255,255,255,.26),transparent);transform:skewX(-18deg);animation:nlsp-glint 6s ease-in-out 2s infinite}'
			. '.nlsp-face{display:flex;flex-direction:column;align-items:center;border:1.5px solid #F4F6FA;border-radius:4px;padding:4px 12px 3px;color:#fff;max-width:170px}'
			. '.nlsp-st{font-weight:700;line-height:1.05;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;max-width:150px;text-shadow:0 1px 0 rgba(0,0,0,.2)}'
			. '.nlsp-rule{display:block;width:100%;height:1px;background:rgba(255,255,255,.6);margin:2px 0 1px}'
			. '.nlsp-city{font-size:10px;font-weight:500}'
			. '.nlsp-count{position:absolute;bottom:8px;right:8px;display:flex;align-items:center;gap:5px;background:rgba(15,29,38,.72);color:#fff;border-radius:999px;padding:4px 9px 4px 7px;font-size:11px;-webkit-backdrop-filter:blur(4px);backdrop-filter:blur(4px)}'
			. '.nlsp-count i{width:7px;height:7px;border-radius:50%;background:#fff;box-shadow:0 0 0 2px rgba(255,255,255,.3)}.nlsp-count b{font-family:"IBM Plex Mono",monospace}'
			. '@container (max-width:280px){.nlsp-hang{--sz:.82}}@container (max-width:220px){.nlsp-hang{--sz:.7}.nlsp-count{display:none}}'
			. '@keyframes nlsp-swing{0%{transform:rotate(-7deg) translateY(-8px);opacity:0}35%{transform:rotate(3deg);opacity:1}60%{transform:rotate(-1.4deg)}80%{transform:rotate(.5deg)}100%{transform:rotate(0)}}'
			. '@keyframes nlsp-glint{0%,65%{left:-45%}100%{left:125%}}'
			. '@media (prefers-reduced-motion:reduce){.nlsp *{animation:none!important}}';
		$js = 'document.addEventListener("DOMContentLoaded",function(){if(window.matchMedia&&matchMedia("(prefers-reduced-motion: reduce)").matches){return;}var L=[].slice.call(document.querySelectorAll(".nlsp"));if(!L.length||!("IntersectionObserver" in window)){return;}'
			. 'var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add("is-in");io.unobserve(e.target);}});},{threshold:.4});L.forEach(function(p){io.observe(p);});});';
		return '<style id="nlsp-css">' . $css . '</style><script id="nlsp-js">' . $js . '</script>';
	}
}
