# -*- coding: utf-8 -*-
"""Round R part 2 (HAD-675, 9.11.2026): phone speed on the pages that hold [nadlan_mortgage_market] (/mortgage-calculator/ and its
English twin), measured with tools/lcp_probe.mjs variants (scratchpad mc/cls*):
  - the H1 face (Noto Serif Hebrew) and the body face (Assistant) arrived at ~5.4 s on a slow phone: the H1 went from 2 to 3 lines
    and the lead lost a line after the first paint = CLS 0.179. Preconnect + preload of their Hebrew variable files (one file per
    family, every weight): CLS 0.068 in the test.
  - Stripe v3 (280 KB) and three Paid Member Subscriptions scripts are classic blocking scripts in the footer, BEFORE the site's
    WhatsApp bar, so the bar was drawn only after Stripe arrived (~14 s) and became the LCP. Ben (6.11): keep Stripe on this page.
    They stay; they get `defer` (they still load and run, in the same order, after the page is parsed). Only data-defining inline
    scripts follow them (PMS_States, pms, pms_discount_object), so nothing breaks.
The font URLs are read from Google's CSS once a week (transient), with the URLs of 9.11.2026 as the fallback.
Appends one block to inc/mortgage-market.php (CRLF kept). python patch_mm2.py [--dry]"""
import io, os, sys
H = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(H, "..", "..", "..", ".."))
F = os.path.join(REPO, "plugins", "nadlan-config", "inc", "mortgage-market.php")
src0 = io.open(F, encoding="utf-8", newline="").read(); CRLF = chr(13) + chr(10) in src0
src = src0.replace(chr(13) + chr(10), chr(10))
assert "nadlan_mm_million_rows" in src, "run patch_mm.py first"
assert "nadlan_mm_font_preload" not in src, "already patched"
BLOCK = r'''
/* 1.72.615 (HAD-675): phone speed on the pages that hold the market section. Fonts first, blocking payment scripts deferred. */
if ( ! function_exists( 'nadlan_mm_speed_page' ) ) {
	function nadlan_mm_speed_page() {
		static $on = null;
		if ( null !== $on ) { return $on; }
		$p = is_singular() ? get_post() : null;
		$on = $p && false !== strpos( (string) $p->post_content, '[nadlan_mortgage_market' );
		return $on;
	}

	/** The two Hebrew variable font files the first screen paints with (H1: Noto Serif Hebrew, text: Assistant). */
	function nadlan_mm_font_preload() {
		$urls = get_transient( 'nadlan_mm_font_preload_v1' );
		if ( is_array( $urls ) && 2 === count( $urls ) ) { return $urls; }
		$urls = array(
			'https://fonts.gstatic.com/s/notoserifhebrew/v30/k3k5o9MMPvpLmixYH7euCwmkS9DohjX1-kRyiqyBqIxnoLbD-VBM2jVkL3Lr.woff2',
			'https://fonts.gstatic.com/s/assistant/v24/2sDcZGJYnIjSi6H75xkzamW5Kb8VZBHR.woff2',
		);
		$ttl = DAY_IN_SECONDS;
		$res = wp_remote_get( 'https://fonts.googleapis.com/css2?family=Noto+Serif+Hebrew:wght@500;600;700&family=Assistant:wght@300;400;600;700&display=swap',
			array( 'timeout' => 3, 'user-agent' => 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0 Safari/537.36' ) );
		if ( ! is_wp_error( $res ) && 200 === (int) wp_remote_retrieve_response_code( $res ) ) {
			$css = (string) wp_remote_retrieve_body( $res ); $found = array();
			foreach ( array( 'Noto Serif Hebrew', 'Assistant' ) as $fam ) {
				if ( preg_match( "#/\\* hebrew \\*/\\s*@font-face\\s*\\{[^}]*font-family:\\s*'" . preg_quote( $fam, '#' ) . "'[^}]*src:\\s*url\\((https://fonts\\.gstatic\\.com/[^)]+\\.woff2)\\)#", $css, $m ) ) { $found[] = $m[1]; }
			}
			if ( 2 === count( $found ) ) { $urls = $found; $ttl = WEEK_IN_SECONDS; }
		}
		set_transient( 'nadlan_mm_font_preload_v1', $urls, $ttl );
		return $urls;
	}

	add_action( 'wp_head', function () {
		if ( ! nadlan_mm_speed_page() ) { return; }
		echo '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>' . "\n";
		foreach ( nadlan_mm_font_preload() as $u ) { echo '<link rel="preload" href="' . esc_url( $u ) . '" as="font" type="font/woff2" crossorigin>' . "\n"; }
	}, 2 );

	add_filter( 'script_loader_tag', function ( $tag, $handle, $src ) {
		if ( ! nadlan_mm_speed_page() || ! preg_match( '#js\.stripe\.com/v3|/plugins/paid-member-subscriptions/#', (string) $src ) ) { return $tag; }
		return preg_replace_callback( '#<script\b([^>]*)\bsrc=(["\'])([^"\']+)\2([^>]*)>#', function ( $m ) {
			if ( ! preg_match( '#js\.stripe\.com/v3|/plugins/paid-member-subscriptions/#', $m[3] ) || preg_match( '#\b(async|defer)\b#', $m[1] . $m[4] ) ) { return $m[0]; }
			return '<script' . $m[1] . 'src=' . $m[2] . $m[3] . $m[2] . $m[4] . ' defer>';
		}, $tag );
	}, 20, 3 );
}
'''
src = src.rstrip("\n") + "\n" + BLOCK
print("mortgage-market.php +%d bytes" % len(BLOCK.encode("utf-8")))
if "--dry" not in sys.argv:
    io.open(F, "w", encoding="utf-8", newline="").write(src.replace(chr(10), chr(13) + chr(10)) if CRLF else src)
    print("written")
