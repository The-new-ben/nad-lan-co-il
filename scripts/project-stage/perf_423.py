# -*- coding: utf-8 -*-
"""Release 1.72.423 (HAD-421 steps 2b + 3b, the Kikar loop turn 33, design v104.46):
(1) dashicons (wp-includes, 36 KB) loads for every visitor on our templates although no dashicons class is used in the page
    body (checked on /projects/hamedina/ 5.10). Visitors who are not signed in no longer get it on the same templates as
    nadlan_pms_off (projects, listings, brokers). Signed-in users keep it (the admin bar needs it). A style that depends on
    dashicons still pulls it in (dequeue, never deregister).
(2) The film videos reserve their frame before the poster arrives: aspect-ratio auto 16/9 (wide) and auto 9/16 (upright), so
    a lazy poster (1.72.421) no longer grows a 150 px box into a full player. "auto" lets the media's own ratio win once known.
Applied to the LIVE inc/project-stage.php text (what 1.72.422 wrote), each anchor exactly once."""

RELS = ["inc/project-stage.php"]
FILES = {}
TALL = ".nlws-film__v--tall{display:none;max-width:420px;margin:0 auto}"
TALL_NEW = TALL + ".nlws-film__v--wide{aspect-ratio:auto 16/9}.nlws-film__v--tall{aspect-ratio:auto 9/16}"
PMS_END = "\tadd_action( 'wp_print_footer_scripts', 'nadlan_pms_off', 1 );\n}\n"
DASH = """
if ( ! function_exists( 'nadlan_dash_off' ) ) {
	/** HAD-421 (5.10.2026): dashicons (36 KB) loads for every visitor, yet no dashicons class is used on our templates. Visitors
	 *  who are not signed in no longer get it on project pages, listings and the broker pages (the same templates as
	 *  nadlan_pms_off). Signed-in users keep it for the admin bar; a style that depends on it still pulls it in. */
	function nadlan_dash_off() {
		if ( is_admin() ) { return; }
		$types = array( 'nadlan_project', 'nadlan_property', 'nadlan_professional' );
		$ours  = is_singular( $types ) || is_post_type_archive( $types ) || is_page( 'brokers' );
		if ( ! $ours && is_page() ) {
			$dir  = get_page_by_path( 'brokers' );
			$ours = $dir && (int) wp_get_post_parent_id( get_queried_object_id() ) === (int) $dir->ID;
		}
		if ( ! $ours ) { return; }
		wp_dequeue_style( 'pms_block_themes_front_end_stylesheet' ); // the PMS stylesheet nadlan_pms_off missed
		if ( ! is_user_logged_in() ) {
			// wp-jquery-ui-dialog depends on dashicons and pulled it back in (the first 1.72.423 run rolled back); no jQuery UI
			// dialog script is on these pages, so its stylesheet styles nothing here
			wp_dequeue_style( 'wp-jquery-ui-dialog' );
			wp_dequeue_style( 'dashicons' );
		}
	}
	add_action( 'wp_enqueue_scripts', 'nadlan_dash_off', 9999 );
	add_action( 'wp_print_styles', 'nadlan_dash_off', 1 );         // a style enqueued after wp_enqueue_scripts (the 2nd run's lesson)
	add_action( 'wp_print_footer_scripts', 'nadlan_dash_off', 1 ); // a late style printed in the footer
}
"""


def apply(rel, txt):
    if "nadlan_dash_off" in txt:
        raise SystemExit("perf_423: already applied")
    for a in (TALL, PMS_END):
        if txt.count(a) != 1:
            raise SystemExit("perf_423: an anchor is there " + str(txt.count(a)) + " times: " + a.strip()[:60])
    return txt.replace(TALL, TALL_NEW).replace(PMS_END, PMS_END + DASH)
