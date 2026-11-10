# -*- coding: utf-8 -*-
"""HAD-689 step 2: put the immediate-occupancy block (scripts/seo/had689_ready_block.php.txt) into inc/projects-hub.php, let the
body skip the marketing table when the top block printed it, split the hub assets (CSS early, JS at the end), insert the top
block after the catalog hero in inc/catalog-plus.php, and print the answer paragraph under the H1 in inc/directory.php.
Run once on the text that equals live; every anchor must match exactly once. python had689_apply_ready_block.py"""
import io, os, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(HERE))
INC = os.path.join(REPO, "plugins", "nadlan-config", "inc")
rd = lambda f: io.open(os.path.join(INC, f), encoding="utf-8").read()
def wr(f, s): io.open(os.path.join(INC, f), "w", encoding="utf-8", newline="\n").write(s)
def one(s, a, b, f):
    assert s.count(a) == 1, (f, s.count(a), a[:70])
    return s.replace(a, b)

# ---- projects-hub.php
s = rd("projects-hub.php")
assert "nadlan_ph_ready_html" not in s, "already applied"
block = io.open(os.path.join(HERE, "had689_ready_block.php.txt"), encoding="utf-8").read()
anchor = "/* ------------------------------------------------------------------------------------------------ the body after the grid */"
s = one(s, anchor, block + anchor, "hub")
s = one(s, "			function () { return nadlan_ph_market_html(); },\n",
        "			function () { return nadlan_ph_top_done() ? '' : nadlan_ph_market_html(); }, // HAD-689: the table sits above the catalog when the top block printed it\n", "hub")
s = one(s, "if ( ! function_exists( 'nadlan_ph_assets' ) ) {\n	function nadlan_ph_assets() {\n		return '<style id=\"nlph-css\">'",
        "if ( ! function_exists( 'nadlan_ph_assets_part' ) ) {\n"
        "	/** 'css' = the <style> of the hub, 'js' = its script. The top block prints the CSS early (HAD-689), so nothing above the catalog shows unstyled. */\n"
        "	function nadlan_ph_assets_part( $which ) {\n"
        "		$a = nadlan_ph_assets_raw(); $p = strpos( $a, '</style>' );\n"
        "		if ( false === $p ) { return 'css' === $which ? '' : $a; }\n"
        "		$p += 8;\n"
        "		return 'css' === $which ? substr( $a, 0, $p ) : substr( $a, $p );\n"
        "	}\n"
        "}\n"
        "if ( ! function_exists( 'nadlan_ph_assets' ) ) {\n"
        "	function nadlan_ph_assets() { return nadlan_ph_top_done() ? nadlan_ph_assets_part( 'js' ) : nadlan_ph_assets_raw(); }\n"
        "}\n"
        "if ( ! function_exists( 'nadlan_ph_assets_raw' ) ) {\n	function nadlan_ph_assets_raw() {\n		return '<style id=\"nlph-css\">'", "hub")
wr("projects-hub.php", s)

# ---- catalog-plus.php
c = rd("catalog-plus.php")
c = one(c, "	$pre = array( 'bar' => '', 'side' => '', 'body' => '', 'tail' => '' );",
        "	$pre = array( 'bar' => '', 'side' => '', 'top' => '', 'body' => '', 'tail' => '' );", "cp")
c = one(c, "		$pre['body'] = nadlan_cp_body_html( $facets );",
        "		$pre['top']  = function_exists( 'nadlan_ph_top_html' ) ? nadlan_ph_top_html() : ''; // HAD-689: built BEFORE the body, which then skips what the top printed\n"
        "		$pre['body'] = nadlan_cp_body_html( $facets );", "cp")
c = one(c, "			if ( false !== $p ) { $q = strpos( $h, '</header>', $p ); if ( false !== $q ) { $h = substr( $h, 0, $q ) . $pre['bar'] . substr( $h, $q ); } }",
        "			$top_in = false; // HAD-689: the immediate-occupancy section and the marketing table go right after the hero, above the catalog\n"
        "			if ( false !== $p ) { $q = strpos( $h, '</header>', $p ); if ( false !== $q ) { $h = substr( $h, 0, $q ) . $pre['bar'] . '</header>' . $pre['top'] . substr( $h, $q + 9 ); $top_in = true; } }", "cp")
c = one(c, "			if ( false !== $j ) { $h = substr( $h, 0, $j ) . $pre['body'] . substr( $h, $j ); }",
        "			if ( false !== $j ) { $h = substr( $h, 0, $j ) . ( $top_in ? '' : $pre['top'] ) . $pre['body'] . substr( $h, $j ); } // the top block is never lost: below the grid if the hero was not found", "cp")
wr("catalog-plus.php", c)

# ---- directory.php
d = rd("directory.php")
old_lead = "		<p class=\"nldir-lead\"><strong><?php echo number_format( $facets['total'] ); ?></strong> פרויקטים בקטלוג<?php echo esc_html( $nlpc_mix ); ?>, לפי עיר, יזם וסטטוס. בעלי דירות בבניין ישן? <a href=\"<?php echo esc_url( home_url( '/urban-renewal/' ) ); ?>\">המדריך המלא להתחדשות עירונית</a>.</p>\n"
assert d.count(old_lead) == 1, d.count(old_lead)
# the answer first (HAD-689); the catalogue's make-up moves next to the catalogue it describes
d = d.replace(old_lead,
    "		<?php $nlph_answer = ( function_exists( 'nadlan_ph_answer_html' ) && function_exists( 'nadlan_cp_is_catalog' ) && (int) $state['paged'] < 2 ) ? nadlan_ph_answer_html() : ''; // HAD-689: what is on the market today, by stage\n"
    "		echo $nlph_answer; // phpcs:ignore\n"
    "		ob_start(); ?>\n" + old_lead.replace('<p class="nldir-lead">', '<p class="nldir-lead nldir-catlead">') +
    "		<?php $nlph_catlead = ob_get_clean(); if ( '' === $nlph_answer ) { echo $nlph_catlead; $nlph_catlead = ''; } // phpcs:ignore ?>\n")
d = one(d, "כאן רואים את כל הפרויקטים החדשים בישראל לפי עיר, יזם ושלב. מתחת לקטלוג: פרויקטים בשיווק עם המחיר שפרסם היזם,",
        "כאן רואים את כל הפרויקטים החדשים בישראל לפי עיר, יזם ושלב. בעמוד הזה: דירות חדשות לאכלוס מיידי, פרויקטים בשיווק עם המחיר שפרסם היזם,", "dir")
d = one(d, "<nav class=\"nldir-jump\" aria-label=\"בעמוד הזה\"><?php echo function_exists( 'nadlan_ph_market' )",
        "<nav class=\"nldir-jump\" aria-label=\"בעמוד הזה\"><?php echo '' !== $nlph_answer ? '<a href=\"#nlph-ready\">לאכלוס מיידי</a>' : ''; ?><?php echo function_exists( 'nadlan_ph_market' )", "dir")
# the catalogue lead, above the catalogue grid (projects archive only: the second nldir-main in the file)
main_tag = "		<main class=\"nldir-main\">\n			<div class=\"nldir-bar\">\n				<h2 class=\"nldir-count\" style=\"font:inherit;font-size:15px;margin:0;color:inherit;line-height:inherit\"><strong id=\"nldir-total\"><?php echo number_format( $total ); ?></strong> פרויקטים בקטלוג</h2>"
d = one(d, main_tag, main_tag.replace("		<main class=\"nldir-main\">\n",
        "		<main class=\"nldir-main\">\n			<?php echo isset( $nlph_catlead ) ? str_replace( 'class=\"nldir-lead nldir-catlead\"', 'class=\"nldir-lead nldir-catlead\" style=\"font-size:15px;line-height:1.6;margin:0 0 12px\"', $nlph_catlead ) : ''; // phpcs:ignore HAD-689: the catalogue's make-up, next to the catalogue ?>\n"), "dir")
wr("directory.php", d)
print("applied: projects-hub.php, catalog-plus.php, directory.php")
