# -*- coding: utf-8 -*-
"""Release 1.72.420 (HAD-421 step 1, the Kikar loop turn 30, design v104.43): Paid Member Subscriptions prints js.stripe.com
(~250 KB) plus pms-front-end, pms-stripe-script, pms-frontend-discount-code-js and its stylesheet on every page, including
404s. Our own templates hold no PMS form: project pages and the projects catalogue, listings and the listings archive, the
brokers directory and every broker site under it. Those pages drop the PMS scripts and style. A page whose own content
carries a PMS shortcode keeps them; every other page is unchanged (the PMS pages, /login/, /my-account/, /pricing/).
Applied to the LIVE inc/project-stage.php text, after the 1.72.418 caption route (anchor exactly once)."""

RELS = ["inc/project-stage.php"]
FILES = {}
ANCHOR = "\tadd_action( 'rest_api_init', 'nadlan_ps_film_cc_route' );\n}\n"
FUNC = """
if ( ! function_exists( 'nadlan_pms_off' ) ) {
	/** HAD-421 (5.10.2026, phone speed): Paid Member Subscriptions prints Stripe (js.stripe.com, about 250 KB) and three more
	 *  scripts plus its stylesheet on every page. Our own templates hold no PMS form, so they drop them: project pages and the
	 *  catalogue, listings and their archive, the brokers directory and the broker sites under it. A page whose content carries
	 *  a PMS shortcode keeps them. Dequeued, never deregistered, so a script that depends on one still pulls it in. */
	function nadlan_pms_off() {
		if ( is_admin() ) { return; }
		$types = array( 'nadlan_project', 'nadlan_property', 'nadlan_professional' );
		$ours  = is_singular( $types ) || is_post_type_archive( $types ) || is_page( 'brokers' );
		if ( ! $ours && is_page() ) {
			$dir  = get_page_by_path( 'brokers' );
			$ours = $dir && (int) wp_get_post_parent_id( get_queried_object_id() ) === (int) $dir->ID;
		}
		if ( ! $ours ) { return; }
		$p = get_post( get_queried_object_id() );
		if ( $p instanceof WP_Post && false !== strpos( (string) $p->post_content, '[pms-' ) ) { return; }
		foreach ( array( 'pms-stripe-js', 'pms-stripe-script', 'pms-front-end', 'pms-frontend-discount-code-js' ) as $h ) { wp_dequeue_script( $h ); }
		wp_dequeue_style( 'pms-style-front-end' );
	}
	add_action( 'wp_enqueue_scripts', 'nadlan_pms_off', 9999 );
	add_action( 'wp_print_footer_scripts', 'nadlan_pms_off', 1 );
}
"""


def apply(rel, txt):
    if "nadlan_pms_off" in txt:
        raise SystemExit("perf_420: already applied")
    if txt.count(ANCHOR) != 1:
        raise SystemExit("perf_420: the caption-route anchor is there " + str(txt.count(ANCHOR)) + " times")
    return txt.replace(ANCHOR, ANCHOR + FUNC)
