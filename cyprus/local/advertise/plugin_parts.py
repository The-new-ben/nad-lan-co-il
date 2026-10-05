# -*- coding: utf-8 -*-
"""The "Advertise with us" part of the cy-project-experience plugin: PHP (page, shortcode, titles, assets) and the files
it serves. Used by build_plugin.py."""
import io, json, os
import page as advpage

LABELS = {
 'he': {'nav': 'פרסמו אצלנו', 'lineQ': 'מטעם הפרויקט?', 'lineA': 'שלחו לנו פרטים ותוכניות',
        'bandQ': 'יש לכם פרויקט ב{d}?', 'bandQAny': 'יש לכם פרויקט בקפריסין?', 'band': 'הציגו אותו על המפה, עם השכונה וכל מה שסביבו.',
        'districts': {'limassol': 'לימסול', 'paphos': 'פאפוס', 'larnaca': 'לרנקה'}},
 'en': {'nav': 'Advertise with us', 'lineQ': 'Representing this project?', 'lineA': 'Send us details and plans',
        'bandQ': 'Have a project in {d}?', 'bandQAny': 'Have a project in Cyprus?', 'band': 'Put it on the map, with its neighbourhood and everything around it.',
        'districts': {'limassol': 'Limassol', 'paphos': 'Paphos', 'larnaca': 'Larnaca'}},
}


def php_str(s):
    return "'" + s.replace('\\', '\\\\').replace("'", "\\'") + "'"


def adv_php():
    he, en = advpage.COPY['he'], advpage.COPY['en']
    texts = ("array(\n\t\t'he' => array( 'title' => " + php_str(he['title']) + ", 'seo_title' => " + php_str(he['seo_title']) + ", 'seo_desc' => " + php_str(he['seo_desc']) + " ),\n"
             "\t\t'en' => array( 'title' => " + php_str(en['title']) + ", 'seo_title' => " + php_str(en['seo_title']) + ", 'seo_desc' => " + php_str(en['seo_desc']) + " ),\n\t)")
    return """
/* ------------------------------------------------------------------ advertise with us */

define( 'CYPX_ADV_SLUG', 'advertise' );

/**
 * The advertiser page id (0 until it exists).
 *
 * @return int
 */
function cypx_adv_page_id() {
	return (int) get_option( 'cypx_adv_page', 0 );
}

/**
 * Page title and search texts in the visitor's language.
 *
 * @param string $key title|seo_title|seo_desc.
 * @return string
 */
function cypx_adv_text( $key ) {
	$t = """ + texts + """;
	$l = cypx_lang();
	return isset( $t[ $l ][ $key ] ) ? $t[ $l ][ $key ] : '';
}

// The advertiser page is a normal, editable WordPress page, created once (the first wp-admin load after activation).
add_action(
	'admin_init',
	function () {
		if ( cypx_adv_page_id() || ! current_user_can( 'publish_pages' ) ) {
			return;
		}
		$found = get_page_by_path( CYPX_ADV_SLUG, OBJECT, 'page' );
		if ( $found ) {
			update_option( 'cypx_adv_page', (int) $found->ID );
			return;
		}
		$id = wp_insert_post(
			array(
				'post_type'      => 'page',
				'post_status'    => 'publish',
				'post_name'      => CYPX_ADV_SLUG,
				'post_title'     => """ + php_str(he['title']) + """,
				'post_content'   => "<!-- wp:shortcode -->\\n[cy_advertise]\\n<!-- /wp:shortcode -->",
				'comment_status' => 'closed',
				'ping_status'    => 'closed',
			),
			true
		);
		if ( ! is_wp_error( $id ) && $id ) {
			update_option( 'cypx_adv_page', (int) $id );
		}
	}
);

add_shortcode(
	'cy_advertise',
	function () {
		$file = plugin_dir_path( __FILE__ ) . 'assets/advertise/page-' . cypx_lang() . '.html';
		return file_exists( $file ) ? (string) file_get_contents( $file ) : ''; // phpcs:ignore WordPress.WP.AlternativeFunctions
	}
);

add_filter(
	'the_title',
	function ( $title, $post_id = 0 ) {
		if ( ! is_admin() && $post_id && (int) $post_id === cypx_adv_page_id() && 'en' === cypx_lang() ) {
			return cypx_adv_text( 'title' );
		}
		return $title;
	},
	10,
	2
);

foreach ( array( 'rank_math/frontend/title' => 'seo_title', 'rank_math/frontend/description' => 'seo_desc' ) as $cypx_hook => $cypx_key ) {
	add_filter(
		$cypx_hook,
		function ( $value ) use ( $cypx_key ) {
			return ( cypx_adv_page_id() && is_page( cypx_adv_page_id() ) ) ? cypx_adv_text( $cypx_key ) : $value;
		}
	);
}

add_filter(
	'document_title_parts',
	function ( $parts ) {
		if ( cypx_adv_page_id() && is_page( cypx_adv_page_id() ) ) {
			$parts['title'] = cypx_adv_text( 'seo_title' );
			unset( $parts['site'], $parts['tagline'] );
		}
		return $parts;
	}
);

add_action(
	'wp_enqueue_scripts',
	function () {
		$base = plugin_dir_path( __FILE__ ) . 'assets/';
		$url  = plugin_dir_url( __FILE__ ) . 'assets/';
		if ( ! file_exists( $base . 'site/adv.js' ) ) {
			return;
		}
		$ver = CYPX_VERSION . '-' . substr( md5( (string) filemtime( $base . 'site/adv.js' ) . (string) filemtime( $base . 'site/adv.css' ) ), 0, 8 );
		wp_enqueue_style( 'cypx-adv', $url . 'site/adv.css', array(), $ver );
		wp_enqueue_script( 'cypx-adv', $url . 'site/adv.js', array(), $ver, array( 'in_footer' => true, 'strategy' => 'defer' ) );
		wp_add_inline_script(
			'cypx-adv',
			'window.CYPX_ADV=' . wp_json_encode(
				array(
					'url' => home_url( '/' . CYPX_ADV_SLUG . '/' ),
					'wa'  => '972525101555',
				)
			) . ';',
			'before'
		);
		if ( cypx_adv_page_id() && is_page( cypx_adv_page_id() ) ) {
			wp_enqueue_style( 'cypx-adv-page', $url . 'advertise/page.css', array(), $ver );
		}
	}
);
"""


def viewport_php():
    return """
/* ------------------------------------------------------------------ phones on the atlas routes */

// The atlas routes (projects, catalogues, areas, streets) render through WordPress's classic theme-compat header,
// which prints no viewport tag, so phones draw them at desktop width (found live on 3.10.2026). The block-theme pages
// already print one, so add it only where the atlas route is active.
add_action(
	'wp_head',
	function () {
		if ( get_query_var( 'ca_view' ) ) {
			echo '<meta name="viewport" content="width=device-width, initial-scale=1" />' . "\\n";
		}
	},
	1
);
"""


def write_assets(root_dir, here):
    site = os.path.join(root_dir, 'assets', 'site')
    adv = os.path.join(root_dir, 'assets', 'advertise')
    os.makedirs(site, exist_ok=True)
    os.makedirs(adv, exist_ok=True)
    js = io.open(os.path.join(here, 'advertise', 'adv.js'), encoding='utf-8').read()
    old = 'const C=window.CYPX_ADV||{};'
    if js.count(old) != 1:
        raise SystemExit('adv.js: config line not found')
    js = js.replace(old, 'const C=Object.assign(' + json.dumps(LABELS, ensure_ascii=False) + ',window.CYPX_ADV||{});')
    io.open(os.path.join(site, 'adv.js'), 'w', encoding='utf-8', newline='\n').write(js)
    io.open(os.path.join(site, 'adv.css'), 'w', encoding='utf-8', newline='\n').write(io.open(os.path.join(here, 'advertise', 'adv.css'), encoding='utf-8').read())
    for lang in ('he', 'en'):
        io.open(os.path.join(adv, f'page-{lang}.html'), 'w', encoding='utf-8', newline='\n').write(advpage.render(lang))
    io.open(os.path.join(adv, 'page.css'), 'w', encoding='utf-8', newline='\n').write(advpage.CSS.strip() + '\n')
