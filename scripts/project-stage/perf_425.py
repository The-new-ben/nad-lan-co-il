# -*- coding: utf-8 -*-
"""Release 1.72.425 (HAD-421 step 6, the Kikar loop turn 35, design v104.48): the area map's stylesheet stops blocking the
first paint on project pages. leaflet.css comes from unpkg.com, a third origin: on a slow phone link the browser must open a new
connection (DNS + TCP + TLS, ~3-4 round trips at 150 ms) before it may draw anything, for a map that sits far below the stage.
On nadlan_project singles the leaflet stylesheet is printed as media="print" and switched to "all" once loaded, with a
<noscript> copy for browsers without scripts. Elsewhere (the home's map band, listings, profiles) nothing changes.
Applied to the LIVE inc/project-stage.php text (what 1.72.424 wrote), after nadlan_dash_off (anchor exactly once)."""

RELS = ["inc/project-stage.php"]
FILES = {}
ANCHOR = "\tadd_action( 'wp_print_footer_scripts', 'nadlan_dash_off', 1 ); // a late style printed in the footer\n}\n"
FUNC = """
if ( ! function_exists( 'nadlan_leaflet_css_async' ) ) {
	/** HAD-421 (5.10.2026): on a project page the area map is far below the stage, yet leaflet.css (unpkg.com, a third origin)
	 *  blocked the first paint behind a new connection. Here it loads without blocking (media print, switched to all on load),
	 *  with a noscript copy. Other templates keep the plain tag. */
	function nadlan_leaflet_css_async( $tag, $handle, $href, $media ) {
		if ( 'leaflet' !== $handle || is_admin() || ! is_singular( 'nadlan_project' ) || false !== strpos( $tag, 'onload=' ) ) { return $tag; }
		$async = str_replace( "media='" . $media . "'", "media='print' onload=\\"this.media='all'\\"", $tag );
		if ( $async === $tag ) { return $tag; }
		return $async . '<noscript>' . trim( $tag ) . '</noscript>' . "\\n";
	}
	add_filter( 'style_loader_tag', 'nadlan_leaflet_css_async', 10, 4 );
}
"""


def apply(rel, txt):
    if "nadlan_leaflet_css_async" in txt:
        raise SystemExit("perf_425: already applied")
    if txt.count(ANCHOR) != 1:
        raise SystemExit("perf_425: the dash_off anchor is there " + str(txt.count(ANCHOR)) + " times")
    return txt.replace(ANCHOR, ANCHOR + FUNC)
