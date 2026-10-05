# -*- coding: utf-8 -*-
"""Release 1.72.426 (HAD-421 step 7, the Kikar loop turn 36, design v104.49): no Leaflet on project pages that show the Mapbox
area map. project-experience.php prints the Mapbox map (#nlpjx-unimap) whenever nadlan_mapbox_token() is set, and the Leaflet
fallback (#nlpjx-leaflet) only without a token; yet Leaflet js + css (unpkg.com) loaded on every project page with lat/lng,
pulled in as a dependency of nadlan-pjx-js. Measured 5.10: 0 Leaflet maps on hamedina and rainbow after a full scroll; the
inline map code is guarded (if(m&&window.L)). With a token: the dependency is dropped and Leaflet is not loaded. Without a
token nothing changes (the fallback keeps its library). The Mapbox map and the beam are untouched.
Applied to the LIVE inc/project-stage.php text (what 1.72.425 wrote), after nadlan_leaflet_css_async (anchor exactly once)."""

RELS = ["inc/project-stage.php"]
FILES = {}
ANCHOR = "\tadd_filter( 'style_loader_tag', 'nadlan_leaflet_css_async', 10, 4 );\n}\n"
FUNC = """
if ( ! function_exists( 'nadlan_leaflet_off' ) ) {
	/** HAD-421 (5.10.2026): a project page with a Mapbox token renders the Mapbox area map; the Leaflet fallback element is
	 *  printed only without a token (project-experience.php), yet Leaflet js + css loaded anyway as a dependency of
	 *  nadlan-pjx-js. With a token, the dependency is dropped and Leaflet is not loaded; the inline code is guarded by window.L. */
	function nadlan_leaflet_off() {
		if ( is_admin() || ! is_singular( 'nadlan_project' ) ) { return; }
		if ( ! function_exists( 'nadlan_mapbox_token' ) || '' === (string) nadlan_mapbox_token() ) { return; }
		$ws = wp_scripts();
		if ( isset( $ws->registered['nadlan-pjx-js'] ) ) {
			$ws->registered['nadlan-pjx-js']->deps = array_values( array_diff( (array) $ws->registered['nadlan-pjx-js']->deps, array( 'leaflet' ) ) );
		}
		wp_dequeue_script( 'leaflet' );
		wp_dequeue_style( 'leaflet' );
	}
	add_action( 'wp_enqueue_scripts', 'nadlan_leaflet_off', 9999 );
}
"""


def apply(rel, txt):
    if "nadlan_leaflet_off" in txt:
        raise SystemExit("perf_426: already applied")
    if txt.count(ANCHOR) != 1:
        raise SystemExit("perf_426: the leaflet-css anchor is there " + str(txt.count(ANCHOR)) + " times")
    return txt.replace(ANCHOR, ANCHOR + FUNC)
