# -*- coding: utf-8 -*-
"""Release 1.72.427 (HAD-421 step 8, the Kikar loop turn 37, design v104.50): the theme's base stylesheet is loaded once.
Every page printed it twice: the parent theme's 'nadlan-revenue-style' (themes/nadlan-revenue/style.min.css, 50.5 KB) early in
the head, and the child theme's 'nlpc-parent-style' (themes/nadlan-revenue/style.css, 52.6 KB) further down. Compared 5.10: the
same 287 rules, the same 8 @media blocks and 15 @font-face; the only differences are a space before !important, '*:focus'
against ':focus' and the order inside one selector list. The later identical copy already wins every rule, so the earlier one
is dead weight on the critical path. Here the earlier handle keeps its place (other stylesheets depend on it, and a dequeued
dependency is pulled back) but its src becomes false, so it prints no file. The guard runs only when the child's copy is on
the page and both sources are the expected files; otherwise nothing changes.
Applied to the LIVE inc/project-stage.php text (what 1.72.426 wrote), after nadlan_leaflet_off (anchor exactly once)."""

RELS = ["inc/project-stage.php"]
FILES = {}
ANCHOR = "\tadd_action( 'wp_enqueue_scripts', 'nadlan_leaflet_off', 9999 );\n}\n"
FUNC = """
if ( ! function_exists( 'nadlan_theme_css_once' ) ) {
	/** HAD-421 (5.10.2026): the parent theme printed style.min.css early and the child theme printed the identical style.css
	 *  later in the head (the same 287 rules). The later copy wins every rule, so the earlier handle keeps its place for its
	 *  dependents but prints no file. Only when the child's copy is really on the page. */
	function nadlan_theme_css_once() {
		if ( is_admin() ) { return; }
		$ws = wp_styles();
		if ( ! isset( $ws->registered['nadlan-revenue-style'], $ws->registered['nlpc-parent-style'] ) ) { return; }
		if ( ! wp_style_is( 'nlpc-parent-style', 'enqueued' ) ) { return; }
		$early = (string) $ws->registered['nadlan-revenue-style']->src;
		$late  = (string) $ws->registered['nlpc-parent-style']->src;
		if ( false === strpos( $early, '/themes/nadlan-revenue/style.min.css' ) || false === strpos( $late, '/themes/nadlan-revenue/style.css' ) ) { return; }
		$ws->registered['nadlan-revenue-style']->src = false;
	}
	add_action( 'wp_print_styles', 'nadlan_theme_css_once', 1 );
}
"""


def apply(rel, txt):
    if "nadlan_theme_css_once" in txt:
        raise SystemExit("perf_427: already applied")
    if txt.count(ANCHOR) != 1:
        raise SystemExit("perf_427: the leaflet-off anchor is there " + str(txt.count(ANCHOR)) + " times")
    return txt.replace(ANCHOR, ANCHOR + FUNC)
