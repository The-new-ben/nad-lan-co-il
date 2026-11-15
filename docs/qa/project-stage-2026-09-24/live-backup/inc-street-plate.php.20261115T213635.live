<?php
/**
 * nadlan-config - the street sign on a project card that has no picture of its own (HAD-743, Ben 15.11.2026:
 * "שלטי הרחובות ... ממש ברמה"). Replaces the shared default picture: a municipal enamel sign with the project's street and city,
 * hung over a small map of the REAL new projects around it (our own points, assets/deals/projects.json, distinct places only),
 * a one-kilometre ring, north arrow and a counted line "N פרויקטים חדשים בקילומטר". No image request at all.
 * Design: Claude Design canvas https://claude.ai/artifact/Rg8mHtQitrYSGF9McF1Bus board 6 (docs/design-lab/deals-map/).
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

if ( ! function_exists( 'nadlan_sp_html' ) ) {
	function nadlan_sp_html( $id, $kind_label = '' ) {
		$lat  = (float) get_post_meta( $id, 'lat', true );
		$lng  = (float) get_post_meta( $id, 'lng', true );
		$city = function_exists( 'nadlan_meta_norm' ) ? nadlan_meta_norm( get_post_meta( $id, 'city', true ) ) : (string) get_post_meta( $id, 'city', true );
		$hood = (string) get_post_meta( $id, 'neighborhood', true );
		$street = nadlan_sp_street( get_the_title( $id ), $hood, $city );
		if ( '' === $street ) { return ''; }
		$sub = ( $street === $city ) ? 'ישראל' : $city;
		$len = function_exists( 'mb_strlen' ) ? mb_strlen( $street, 'UTF-8' ) : strlen( $street );
		$fs  = $len <= 7 ? 31 : ( $len <= 11 ? 27 : ( $len <= 15 ? 23 : 19 ) );
		$dots = ''; $n = 0;
		$cx = 179; $cy = 150; $s = 120; // 1 km = 120 px; the project's point sits under the sign
		if ( $lat && $lng ) {
			$k = cos( deg2rad( $lat ) ) * 111.32;
			foreach ( nadlan_sp_points() as $p ) {
				$dx = ( $p[0] - $lng ) * $k; $dy = ( $p[1] - $lat ) * 110.57;
				if ( abs( $dx ) < 0.0005 && abs( $dy ) < 0.0005 ) { continue; } // the project itself
				$d = sqrt( $dx * $dx + $dy * $dy );
				if ( $d <= 1.0 ) { $n++; }
				$x = (int) round( $cx + $dx * $s ); $y = (int) round( $cy - $dy * $s );
				if ( $x >= 4 && $x <= 354 && $y >= 4 && $y <= 220 ) { $dots .= 'M' . $x . ' ' . $y . 'h0'; }
			}
		}
		$label = $street . ', ' . $city . ( $n > 0 ? '. ' . $n . ' פרויקטים חדשים ברדיוס קילומטר' : '' );
		ob_start(); ?>
<div class="nlsp" role="img" aria-label="<?php echo esc_attr( $label ); ?>">
	<svg class="nlsp-map" viewBox="0 0 358 224" preserveAspectRatio="xMidYMid slice" aria-hidden="true" focusable="false">
		<rect width="358" height="224" fill="url(#nlsp-grid)" opacity=".55"/>
		<?php if ( $lat && $lng ) : ?>
		<circle cx="<?php echo (int) $cx; ?>" cy="<?php echo (int) $cy; ?>" r="<?php echo (int) $s; ?>" class="nlsp-ring"/>
		<?php if ( '' !== $dots ) : ?><path d="<?php echo esc_attr( $dots ); ?>" class="nlsp-dots"/><path d="<?php echo esc_attr( $dots ); ?>" class="nlsp-dots-in"/><?php endif; ?>
		<circle cx="<?php echo (int) $cx; ?>" cy="<?php echo (int) $cy; ?>" r="6" class="nlsp-ping"/>
		<circle cx="<?php echo (int) $cx; ?>" cy="<?php echo (int) $cy; ?>" r="5" class="nlsp-me"/>
		<text x="300" y="214" class="nlsp-scale">1 ק״מ</text>
		<?php endif; ?>
		<g transform="translate(20 22)" class="nlsp-north"><path d="M0 -10 L5 3 L0 0 L-5 3 Z"/><text x="0" y="14">N</text></g>
	</svg>
	<div class="nlsp-hang" aria-hidden="true">
		<span class="nlsp-rod"></span><span class="nlsp-rod is-b"></span>
		<div class="nlsp-sign"><span class="nlsp-glint"></span>
			<div class="nlsp-face"><i class="nlsp-screw"></i><i class="nlsp-screw is-b"></i>
				<span class="nlsp-st" style="font-size:<?php echo (int) $fs; ?>px"><?php echo esc_html( $street ); ?></span>
				<span class="nlsp-rule"></span>
				<span class="nlsp-city"><?php echo esc_html( $sub ); ?></span>
			</div>
		</div>
	</div>
	<?php if ( $n > 0 ) : ?><span class="nlsp-count"><i></i><b><?php echo (int) $n; ?></b> פרויקטים חדשים בק״מ</span><?php endif; ?>
	<?php if ( '' !== $kind_label && 'אחר' !== $kind_label ) : ?><span class="nlsp-kind"><?php echo esc_html( $kind_label ); ?></span><?php endif; ?>
</div>
		<?php
		return (string) ob_get_clean();
	}
}

if ( ! function_exists( 'nadlan_sp_assets' ) ) {
	/** CSS, the shared grid pattern and the small motion script, printed once per page before the first sign. */
	function nadlan_sp_assets() {
		static $done = false;
		if ( $done ) { return ''; }
		$done = true;
		$css = '.nldc-media.has-plate{container-type:inline-size}.nlsp{position:absolute;inset:0;overflow:hidden;background:radial-gradient(120% 90% at 50% 62%,#F4F7F9 0%,#E2E9EE 70%,#D6DFE5 100%);font-family:"IBM Plex Sans Hebrew",Heebo,system-ui,sans-serif;direction:rtl;perspective:700px}'
			. '.nlsp-map{position:absolute;inset:0;width:100%;height:100%}'
			. '.nlsp-ring{fill:none;stroke:#0E4C63;stroke-width:1;stroke-dasharray:3 5;opacity:.42}'
			. '.nlsp-dots{fill:none;stroke:#5E7684;stroke-width:7;stroke-linecap:round;animation:nlsp-tw 2.6s ease-in-out infinite}'
			. '.nlsp-dots-in{fill:none;stroke:#fff;stroke-width:2.6;stroke-linecap:round}'
			. '.nlsp-me{fill:#C8102E;stroke:#fff;stroke-width:2}'
			. '.nlsp-ping{fill:none;stroke:#C8102E;stroke-width:2;transform-origin:center;transform-box:fill-box;animation:nlsp-ping 2.2s ease-out infinite}'
			. '.nlsp-scale{font:500 10px "IBM Plex Mono",monospace;fill:#0E4C63;opacity:.8}'
			. '.nlsp-north path{fill:#0F1D26}.nlsp-north text{font:500 9px "IBM Plex Mono",monospace;fill:#0F1D26;text-anchor:middle}'
			. '.nlsp-hang{position:absolute;top:22px;left:50%;width:240px;margin-left:-120px;zoom:var(--sz,1);display:flex;justify-content:center;transform-origin:50% -24px;transform:rotateX(var(--rx,0deg)) rotateY(var(--ry,0deg));transition:transform .25s ease-out;will-change:transform}'
			. '.nlsp.is-in .nlsp-hang{animation:nlsp-swing 1.7s cubic-bezier(.25,.8,.3,1) both}'
			. '.nlsp.is-tap .nlsp-hang{animation:nlsp-hop .45s cubic-bezier(.3,1.6,.5,1)}'
			. '.nlsp-rod{position:absolute;top:-24px;left:58px;width:2px;height:28px;background:linear-gradient(#A7B2B9,#6F7E88);border-radius:1px}.nlsp-rod.is-b{left:auto;right:58px}'
			. '.nlsp-sign{position:relative;background:linear-gradient(180deg,#2A4FA8 0%,#1D3F8F 55%,#183679 100%);border-radius:9px;padding:5px;box-shadow:inset 0 1px 0 rgba(255,255,255,.35),inset 0 -2px 0 rgba(0,0,0,.18),0 10px 22px rgba(15,29,38,.32),0 2px 4px rgba(15,29,38,.25);overflow:hidden;max-width:236px}'
			. '.nlsp-glint{position:absolute;top:0;bottom:0;left:calc(var(--gx,-40%));width:34%;background:linear-gradient(90deg,transparent,rgba(255,255,255,.24),transparent);transform:skewX(-18deg);pointer-events:none;animation:nlsp-glint 5.5s ease-in-out 2s infinite}'
			. '.nlsp-face{position:relative;border:2px solid #F4F6FA;border-radius:5px;padding:7px 20px 6px;display:flex;flex-direction:column;align-items:center;gap:2px;color:#fff;min-width:150px}'
			. '.nlsp-screw{position:absolute;top:50%;right:5px;width:5px;height:5px;margin-top:-2.5px;border-radius:50%;background:radial-gradient(circle at 35% 35%,#F2F4F7,#8A96A0)}.nlsp-screw.is-b{right:auto;left:5px}'
			. '.nlsp-st{font-weight:700;line-height:1.05;letter-spacing:-.3px;text-shadow:0 1px 0 rgba(0,0,0,.18);white-space:nowrap;max-width:200px;overflow:hidden;text-overflow:ellipsis}'
			. '.nlsp-rule{width:100%;height:1.5px;background:rgba(255,255,255,.6);margin:4px 0 3px}'
			. '.nlsp-city{font-size:12px;font-weight:500;letter-spacing:.4px;opacity:.95}'
			. '.nlsp-count{position:absolute;bottom:10px;right:10px;display:flex;align-items:center;gap:6px;background:rgba(255,255,255,.94);border:1px solid #D3DBE0;border-radius:999px;padding:4px 10px 4px 8px;font-size:12px;color:#0F1D26;box-shadow:0 2px 6px rgba(15,29,38,.08)}'
			. '.nlsp-count i{width:8px;height:8px;border-radius:50%;background:#5E7684;box-shadow:0 0 0 2px #fff,0 0 0 3px #5E7684}.nlsp-count b{font-family:"IBM Plex Mono",monospace}'
			. '.nlsp-kind{position:absolute;top:8px;right:8px;background:#fff;color:#0E4C63;border:1px solid #0E4C63;border-radius:6px;padding:3px 8px;font-size:11px;font-weight:600}'
			. '.nldc-media.has-plate{position:relative;background:#E2E9EE}'
			. '@container (max-width:330px){.nlsp-hang{--sz:.82}}@container (max-width:280px){.nlsp-hang{--sz:.7;top:18px}.nlsp-kind{display:none}}@container (max-width:230px){.nlsp-hang{--sz:.6}}'
			. '@keyframes nlsp-tw{0%,100%{opacity:.4}50%{opacity:1}}'
			. '@keyframes nlsp-ping{0%{transform:scale(1);opacity:.6}100%{transform:scale(4.2);opacity:0}}'
			. '@keyframes nlsp-swing{0%{transform:rotate(6deg) translateY(-16px);opacity:0}28%{transform:rotate(-3.2deg);opacity:1}52%{transform:rotate(1.7deg)}74%{transform:rotate(-.7deg)}100%{transform:rotate(0)}}'
			. '@keyframes nlsp-hop{0%{transform:translateY(0)}40%{transform:translateY(-7px) rotate(-1.5deg)}100%{transform:translateY(0)}}'
			. '@keyframes nlsp-glint{0%,62%{left:-40%}100%{left:120%}}'
			. '@media (prefers-reduced-motion:reduce){.nlsp *{animation:none!important;transition:none!important}}';
		$js = '(function(){var R=window.matchMedia&&matchMedia("(prefers-reduced-motion: reduce)").matches;var L=[].slice.call(document.querySelectorAll(".nlsp"));if(!L.length||R){return;}'
			. 'if("IntersectionObserver" in window){var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add("is-in");io.unobserve(e.target);}});},{threshold:.35});L.forEach(function(p){io.observe(p);});}'
			. 'var fine=window.matchMedia&&matchMedia("(hover:hover) and (pointer:fine)").matches;'
			. 'L.forEach(function(p){var c=p.closest(".nldc")||p;'
			. 'if(fine){c.addEventListener("pointermove",function(ev){var r=p.getBoundingClientRect(),x=(ev.clientX-r.left)/r.width-.5,y=(ev.clientY-r.top)/r.height-.5;p.classList.remove("is-in");p.style.setProperty("--ry",(x*14).toFixed(2)+"deg");p.style.setProperty("--rx",(-y*10).toFixed(2)+"deg");});'
			. 'c.addEventListener("pointerleave",function(){p.style.setProperty("--ry","0deg");p.style.setProperty("--rx","0deg");});}'
			. 'else{c.addEventListener("touchstart",function(){p.classList.remove("is-in","is-tap");void p.offsetWidth;p.classList.add("is-tap");},{passive:true});}});})();';
		return '<style id="nlsp-css">' . $css . '</style>'
			. '<svg width="0" height="0" style="position:absolute" aria-hidden="true" focusable="false"><defs><pattern id="nlsp-grid" width="22" height="22" patternUnits="userSpaceOnUse"><path d="M22 0H0V22" fill="none" stroke="#C9D4DB" stroke-width=".6"/></pattern></defs></svg>'
			. '<script id="nlsp-js">document.addEventListener("DOMContentLoaded",function(){' . $js . '});</script>';
	}
}
