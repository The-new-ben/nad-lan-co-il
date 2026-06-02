<?php
/**
 * nadlan-config — Glossary / encyclopedia engine ("מילון נדל"ן") (v1.17.0)
 *
 * The home for the Wikipedia-orphan term project (skills/content-encyclopedia-
 * glossary-plan.md). Each term = a definitional micro-spoke that ranks for a
 * low-competition "מהו X" query and passes link equity UP to a money pillar.
 *
 *  - CPT `nadlan_term` (/glossary/<slug>/) + taxonomy nadlan_term_cat
 *    (construction/planning/law/finance/appraisal/professions/deal-types).
 *  - Per-term render: definition + "מה זה אומר בפועל" practical block + source
 *    line + cross-link UP to the pillar it feeds (the silo rule, rulebook §6).
 *  - DefinedTerm + DefinedTermSet JSON-LD (GEO/AI-citation bait).
 *  - A-Z + category glossary index at /glossary/.
 *  - Thin-content noindex until enriched (same anti-thin discipline as cards).
 *  - REST enrich endpoint reuse: import-enrich already accepts nadlan_term? No —
 *    extend it; here we add the term to the allowed types for enrichment.
 *
 * Cannibalization (rulebook §3.6 + skills/content-encyclopedia-glossary-plan.md §2):
 * a term gets an indexable page ONLY if its intent differs from every existing
 * pillar/spoke focus keyword. Definitional intent ("מהו X") ≠ transactional. The
 * `related_pillar` meta enforces the upward link.
 */

if ( ! defined( 'ABSPATH' ) ) { exit; }

const NADLAN_TERM_WORD_FLOOR = 800;

if ( ! function_exists( 'nadlan_glossary_word_count' ) ) {
	function nadlan_glossary_word_count( $content ) {
		$text = trim( wp_strip_all_tags( (string) $content ) );
		if ( $text === '' ) { return 0; }
		return count( preg_split( '/\s+/', $text ) );
	}
}

if ( ! function_exists( 'nadlan_glossary_is_indexable_term' ) ) {
	function nadlan_glossary_is_indexable_term( $id ) {
		$words = nadlan_glossary_word_count( get_post_field( 'post_content', $id ) );
		$quality = get_post_meta( $id, 'data_quality', true );
		return $words >= NADLAN_TERM_WORD_FLOOR && in_array( $quality, array( 'worldclass', 'approved' ), true );
	}
}

if ( ! function_exists( 'nadlan_glossary_has_non_ascii_slug' ) ) {
	function nadlan_glossary_has_non_ascii_slug( $slug ) {
		$decoded = rawurldecode( (string) $slug );
		return (bool) preg_match( '/[^\x20-\x7E]/', $decoded );
	}
}

if ( ! function_exists( 'nadlan_glossary_ascii_slug_base' ) ) {
	function nadlan_glossary_ascii_slug_base( $text, $fallback = 'real-estate-term' ) {
		$text = wp_strip_all_tags( html_entity_decode( (string) $text, ENT_QUOTES, 'UTF-8' ) );
		$text = strtr( $text, array(
			'א' => 'a', 'ב' => 'b', 'ג' => 'g', 'ד' => 'd', 'ה' => 'h', 'ו' => 'v', 'ז' => 'z',
			'ח' => 'h', 'ט' => 't', 'י' => 'y', 'כ' => 'k', 'ך' => 'k', 'ל' => 'l', 'מ' => 'm',
			'ם' => 'm', 'נ' => 'n', 'ן' => 'n', 'ס' => 's', 'ע' => 'a', 'פ' => 'p', 'ף' => 'p',
			'צ' => 'ts', 'ץ' => 'ts', 'ק' => 'k', 'ר' => 'r', 'ש' => 'sh', 'ת' => 't',
			'׳' => '', '״' => '', '"' => '', "'" => '', '`' => '',
		) );
		$text = remove_accents( $text );
		$text = strtolower( $text );
		$text = preg_replace( '/[^a-z0-9]+/', '-', $text );
		$text = trim( (string) $text, '-' );
		if ( strlen( $text ) > 80 ) {
			$text = trim( substr( $text, 0, 80 ), '-' );
		}
		return $text !== '' ? $text : $fallback;
	}
}

if ( ! function_exists( 'nadlan_glossary_ascii_post_slug' ) ) {
	function nadlan_glossary_ascii_post_slug( $title, $term_en = '', $post_id = 0, $status = 'publish' ) {
		$source = trim( (string) $term_en ) !== '' ? $term_en : $title;
		$base = nadlan_glossary_ascii_slug_base( $source, 'real-estate-term' . ( $post_id ? '-' . (int) $post_id : '' ) );
		return wp_unique_post_slug( $base, (int) $post_id, $status, 'nadlan_term', 0 );
	}
}

if ( ! function_exists( 'nadlan_glossary_store_redirect' ) ) {
	function nadlan_glossary_store_redirect( $kind, $old_slug, $target ) {
		$old_slug = trim( rawurldecode( (string) $old_slug ), '/' );
		$target   = esc_url_raw( $target );
		if ( $old_slug === '' || $target === '' ) { return; }
		$map = get_option( 'nadlan_glossary_redirect_map', array() );
		if ( ! is_array( $map ) ) { $map = array(); }
		$map[ $kind . ':' . $old_slug ] = $target;
		update_option( 'nadlan_glossary_redirect_map', $map, false );
	}
}

if ( ! function_exists( 'nadlan_glossary_redirect_old_slugs' ) ) {
	function nadlan_glossary_redirect_old_slugs() {
		$path = isset( $_SERVER['REQUEST_URI'] ) ? wp_parse_url( (string) $_SERVER['REQUEST_URI'], PHP_URL_PATH ) : '';
		if ( ! $path ) { return; }
		$decoded = trim( rawurldecode( $path ), '/' );
		if ( strpos( $decoded, 'glossary/' ) === 0 ) {
			$key = 'term:' . substr( $decoded, strlen( 'glossary/' ) );
		} elseif ( strpos( $decoded, 'glossary-category/' ) === 0 ) {
			$key = 'category:' . substr( $decoded, strlen( 'glossary-category/' ) );
		} else {
			return;
		}
		$map = get_option( 'nadlan_glossary_redirect_map', array() );
		if ( is_array( $map ) && ! empty( $map[ $key ] ) ) {
			wp_safe_redirect( $map[ $key ], 301, 'nadlan-config' );
			exit;
		}
	}
}
add_action( 'template_redirect', 'nadlan_glossary_redirect_old_slugs', 1 );

if ( ! function_exists( 'nadlan_glossary_migrate_ascii_slugs' ) ) {
	function nadlan_glossary_migrate_ascii_slugs() {
		if ( get_option( 'nadlan_glossary_ascii_slugs_1350' ) ) { return; }
		if ( ! current_user_can( 'manage_options' ) ) { return; }

		$terms = get_posts( array(
			'post_type'      => 'nadlan_term',
			'post_status'    => 'any',
			'posts_per_page' => 1000,
			'fields'         => 'ids',
		) );
		foreach ( $terms as $id ) {
			$old = get_post_field( 'post_name', $id );
			if ( ! nadlan_glossary_has_non_ascii_slug( $old ) ) { continue; }
			$new = nadlan_glossary_ascii_post_slug(
				get_the_title( $id ),
				get_post_meta( $id, 'term_en', true ),
				$id,
				get_post_status( $id )
			);
			if ( $new && $new !== $old ) {
				nadlan_glossary_store_redirect( 'term', $old, home_url( '/glossary/' . $new . '/' ) );
				update_post_meta( $id, '_nadlan_old_glossary_slug', rawurldecode( $old ) );
				wp_update_post( array( 'ID' => $id, 'post_name' => $new ) );
			}
		}

		$cats = get_terms( array( 'taxonomy' => 'nadlan_term_cat', 'hide_empty' => false ) );
		if ( ! is_wp_error( $cats ) ) {
			foreach ( $cats as $cat ) {
				if ( ! nadlan_glossary_has_non_ascii_slug( $cat->slug ) ) { continue; }
				$base = nadlan_glossary_ascii_slug_base( $cat->name, 'glossary-category-' . (int) $cat->term_id );
				$slug = $base;
				$i = 2;
				while ( ( $exists = term_exists( $slug, 'nadlan_term_cat' ) ) && (int) ( is_array( $exists ) ? $exists['term_id'] : $exists ) !== (int) $cat->term_id ) {
					$slug = $base . '-' . $i;
					$i++;
				}
				nadlan_glossary_store_redirect( 'category', $cat->slug, home_url( '/glossary-category/' . $slug . '/' ) );
				wp_update_term( $cat->term_id, 'nadlan_term_cat', array( 'slug' => $slug ) );
			}
		}

		update_option( 'nadlan_glossary_ascii_slugs_1350', gmdate( 'c' ), false );
		delete_transient( 'nadlan_autolink_map' );
		flush_rewrite_rules( false );
	}
}
add_action( 'admin_init', 'nadlan_glossary_migrate_ascii_slugs' );

if ( ! function_exists( 'nadlan_glossary_register' ) ) {
	function nadlan_glossary_register() {
		register_post_type( 'nadlan_term', array(
			'labels' => array( 'name' => 'NadLan Glossary', 'singular_name' => 'NadLan Term' ),
			'public' => true, 'show_in_rest' => true,
			'has_archive' => 'glossary', 'rewrite' => array( 'slug' => 'glossary' ),
			'menu_icon' => 'dashicons-book-alt', 'menu_position' => 33,
			'supports' => array( 'title', 'editor', 'thumbnail', 'custom-fields', 'excerpt' ),
		) );
		register_taxonomy( 'nadlan_term_cat', array( 'nadlan_term' ), array(
			'public' => true, 'hierarchical' => true, 'show_in_rest' => true,
			'rewrite' => array( 'slug' => 'glossary-category' ),
			'labels' => array( 'name' => 'Term Categories', 'singular_name' => 'Term Category' ),
		) );
		$fields = array(
			'term_en'        => 'string',  // English equivalent
			'wikipedia_en'   => 'string',  // EN Wikipedia URL (the orphan source)
			'wikipedia_he'   => 'string',  // HE Wikipedia URL if it exists (then SKIP indexing — collision)
			'related_pillar' => 'string',  // URL of the money pillar this term links UP to
			'related_anchor' => 'string',  // anchor text for the up-link
			'source_url'     => 'string',  // gov/authority citation
			'source_label'   => 'string',
			'data_quality'   => 'string',  // stub|enriched
		);
		foreach ( $fields as $k => $t ) {
			register_post_meta( 'nadlan_term', $k, array(
				'show_in_rest' => true, 'single' => true, 'type' => $t,
				'auth_callback' => function () { return current_user_can( 'edit_posts' ); },
			) );
		}
	}
}
add_action( 'init', 'nadlan_glossary_register' );

/* thin-content noindex for stub terms */
add_filter( 'wp_robots', function ( $r ) {
	if ( ! is_singular( 'nadlan_term' ) ) { return $r; }
	$id = get_queried_object_id();
	if ( ! nadlan_glossary_is_indexable_term( $id ) ) {
		$r['noindex'] = true; $r['follow'] = true; unset( $r['index'] );
	}
	return $r;
}, 20 );

add_action( 'pre_get_posts', function ( $q ) {
	if ( is_admin() || ! $q->is_main_query() ) { return; }
	if ( ! $q->is_post_type_archive( 'nadlan_term' ) ) { return; }
	$q->set( 'meta_query', array(
		array(
			'key'     => 'data_quality',
			'value'   => array( 'worldclass', 'approved' ),
			'compare' => 'IN',
		),
	) );
} );

add_filter( 'wpseo_sitemap_entry', function ( $url, $type, $object ) {
	if ( is_object( $object ) && isset( $object->post_type, $object->ID ) && $object->post_type === 'nadlan_term' ) {
		return nadlan_glossary_is_indexable_term( $object->ID ) ? $url : false;
	}
	return $url;
}, 10, 3 );

/* related terms (same nadlan_term_cat, excluding self), cached 12h per term */
if ( ! function_exists( 'nadlan_glossary_related_terms' ) ) {
	function nadlan_glossary_related_terms( $id, $limit = 6 ) {
		$ck = 'nadlan_relterms_' . $id;
		$cached = get_transient( $ck );
		if ( is_array( $cached ) ) { return array_map( 'get_post', $cached ); }
		$cats = wp_get_object_terms( $id, 'nadlan_term_cat', array( 'fields' => 'ids' ) );
		if ( is_wp_error( $cats ) || ! $cats ) { return array(); }
		$siblings = get_posts( array(
			'post_type'      => 'nadlan_term',
			'post_status'    => 'publish',
			'posts_per_page' => $limit * 3,
			'post__not_in'   => array( $id ),
			'orderby'        => 'rand',
			'tax_query'      => array( array(
				'taxonomy' => 'nadlan_term_cat', 'field' => 'term_id', 'terms' => $cats,
			) ),
		) );
		$siblings = array_slice( array_filter( $siblings, function ( $post ) {
			return nadlan_glossary_is_indexable_term( $post->ID );
		} ), 0, $limit );
		set_transient( $ck, wp_list_pluck( $siblings, 'ID' ), 12 * HOUR_IN_SECONDS );
		return $siblings;
	}
}

/* render: practical block + source + up-link, appended to the definition */
add_filter( 'the_content', function ( $content ) {
	if ( ! ( is_singular( 'nadlan_term' ) && in_the_loop() && is_main_query() ) ) { return $content; }
	$id = get_the_ID();
	$g = function ( $k ) use ( $id ) { return trim( (string) get_post_meta( $id, $k, true ) ); };
	$pillar = $g( 'related_pillar' );
	$anchor = $g( 'related_anchor' ) ?: 'קראו את המדריך המלא';
	$src    = $g( 'source_url' );
	$src_lbl= $g( 'source_label' ) ?: 'מקור';
	$en     = $g( 'term_en' );
	ob_start(); ?>
<div class="nlterm" dir="rtl">
	<?php if ( $en ) : ?><p class="nlterm-en">באנגלית: <span><?php echo esc_html( $en ); ?></span></p><?php endif; ?>
	<?php if ( $pillar ) : ?>
	<div class="nlterm-up">
		<span>רוצים להעמיק?</span>
		<a href="<?php echo esc_url( $pillar ); ?>"><?php echo esc_html( $anchor ); ?></a>
	</div>
	<?php endif; ?>
	<?php
	/* Related terms: siblings in the same category — builds the topical cluster
	 * (internal-link equity) on every published term. Cached per-term for 12h. */
	$related = nadlan_glossary_related_terms( $id );
	if ( $related ) : ?>
	<div class="nlterm-rel">
		<span>מונחים קשורים</span>
		<ul><?php foreach ( $related as $rt ) : ?>
			<li><a href="<?php echo esc_url( get_permalink( $rt ) ); ?>"><?php echo esc_html( get_the_title( $rt ) ); ?></a></li>
		<?php endforeach; ?></ul>
	</div>
	<?php endif; ?>
	<?php if ( $src ) : ?><p class="nlterm-src"><?php echo esc_html( $src_lbl ); ?>: <a href="<?php echo esc_url( $src ); ?>" target="_blank" rel="noopener nofollow"><?php echo esc_html( wp_parse_url( $src, PHP_URL_HOST ) ?: $src ); ?></a></p><?php endif; ?>
</div>
<style>
.nlterm{margin:20px 0;font-family:var(--font-sans,Heebo,sans-serif)}
.nlterm-en{font-size:14px;color:#5C564D}.nlterm-en span{font-weight:600}
.nlterm-up{background:#FAF7F1;border-inline-start:3px solid #9C7A3C;padding:14px 18px;border-radius:4px;margin:14px 0}
.nlterm-up span{display:block;font-size:13px;color:#5C564D;margin-bottom:4px}
.nlterm-up a{color:#1B1A17;font-weight:600;text-decoration:none}
.nlterm-rel{margin:14px 0}
.nlterm-rel span{display:block;font-size:13px;color:#5C564D;margin-bottom:6px;font-weight:600}
.nlterm-rel ul{list-style:none;padding:0;margin:0;display:flex;flex-wrap:wrap;gap:8px}
.nlterm-rel li a{display:inline-block;background:#F2EEE6;color:#1B1A17;padding:5px 12px;border-radius:14px;font-size:13px;text-decoration:none}
.nlterm-rel li a:hover{background:#9C7A3C;color:#fff}
.nlterm-src{font-size:12px;color:#999}
</style>
	<?php
	return $content . ob_get_clean();
}, 20 );

/* DefinedTerm JSON-LD */
add_action( 'wp_head', function () {
	if ( ! is_singular( 'nadlan_term' ) ) { return; }
	$id = get_queried_object_id();
	$data = array_filter( array(
		'@context' => 'https://schema.org', '@type' => 'DefinedTerm',
		'name' => get_the_title( $id ),
		'description' => wp_strip_all_tags( get_the_excerpt( $id ) ) ?: null,
		'url' => get_permalink( $id ),
		'inDefinedTermSet' => array( '@type' => 'DefinedTermSet', 'name' => 'מילון נדל"ן — נדל"ן חכם', 'url' => home_url( '/glossary/' ) ),
		'sameAs' => get_post_meta( $id, 'wikipedia_en', true ) ?: null,
	) );
	echo "\n<script type=\"application/ld+json\">" . wp_json_encode( $data, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES ) . "</script>\n";
}, 20 );

/* /glossary/ index: grouped A-Z + by category (overrides archive body via content filter on the archive description is hard; use a shortcode the archive template or a page can host) */
add_shortcode( 'nadlan_glossary_index', function () {
	$terms = get_posts( array( 'post_type' => 'nadlan_term', 'posts_per_page' => 1000, 'orderby' => 'title', 'order' => 'ASC' ) );
	$terms = array_filter( $terms, function ( $term ) {
		return nadlan_glossary_is_indexable_term( $term->ID );
	} );
	if ( ! $terms ) { return '<p dir="rtl">המילון בבנייה.</p>'; }
	$groups = array();
	foreach ( $terms as $t ) {
		$first = mb_substr( get_the_title( $t ), 0, 1 );
		$groups[ $first ][] = $t;
	}
	ob_start(); ?>
<div class="nlgloss" dir="rtl">
	<?php foreach ( $groups as $letter => $items ) : ?>
	<section class="nlgloss-g">
		<h2><?php echo esc_html( $letter ); ?></h2>
		<ul><?php foreach ( $items as $t ) : ?>
			<li><a href="<?php echo esc_url( get_permalink( $t ) ); ?>"><?php echo esc_html( get_the_title( $t ) ); ?></a></li>
		<?php endforeach; ?></ul>
	</section>
	<?php endforeach; ?>
</div>
<style>
.nlgloss{column-count:3;column-gap:32px;font-family:var(--font-sans,Heebo,sans-serif)}
@media(max-width:780px){.nlgloss{column-count:1}}
.nlgloss-g{break-inside:avoid;margin-bottom:18px}
.nlgloss-g h2{font-size:22px;color:#9C7A3C;margin:0 0 8px;border-bottom:1px solid #E2DCD0;padding-bottom:4px}
.nlgloss-g ul{list-style:none;padding:0;margin:0}
.nlgloss-g li{padding:3px 0}
.nlgloss-g a{color:#1B1A17;text-decoration:none;font-size:15px}
.nlgloss-g a:hover{color:#9C7A3C}
</style>
	<?php
	return ob_get_clean();
} );

/* allow nadlan_term in the import-enrich REST allowlist (extends inc/import.php behaviour) */
add_filter( 'nadlan_import_enrich_types', function ( $types ) {
	$types[] = 'nadlan_term';
	return $types;
} );

/* ---- v1.20.0 ONE-SHOT PUBLISH: removes Cowork friction ----
 * Was: 3 separate REST calls per term (POST wp/v2/nadlan_term → POST nadlan/v1/
 * import-enrich → POST wp/v2/nadlan_term?status=publish), each with a different
 * auth surface (browser nonce vs Application Password); keeps breaking when the
 * Chrome extension drops.
 *
 * Now: a single POST /nadlan/v1/glossary-publish that does the whole publish in
 * one auth-able call (works with Application Password / Basic Auth — NO browser
 * needed). Idempotent: if a term with the same title (or `term_en`) already exists
 * it UPDATES instead of duplicating. Returns the post_id + permalink.
 *
 * Payload:
 *   {
 *     "title": "כלונסאות",                   // required Hebrew term
 *     "content_html": "<p>...</p>",            // required, will be wp_kses_post'd
 *     "term_en":       "Pile (deep foundation)",
 *     "wikipedia_en":  "https://en.wikipedia.org/wiki/Deep_foundation",
 *     "related_pillar":"https://nad-lan.co.il/real-estate-lawyer/",
 *     "related_anchor":"מדריך עורך דין מקרקעין",
 *     "source_url":    "https://...",
 *     "source_label":  "תקן ישראלי 940",
 *     "term_cat":      ["בנייה וקונסטרוקציה"],  // optional
 *     "excerpt":       "...",                  // optional, for meta description
 *     "status":        "publish"               // default 'publish'; 'draft' for prep
 *   }
 */
add_action( 'rest_api_init', function () {
	register_rest_route( 'nadlan/v1', '/glossary-publish', array(
		'methods'             => 'POST',
		'permission_callback' => function () { return current_user_can( 'edit_posts' ); },
		'callback'            => 'nadlan_glossary_one_shot_publish',
	) );
} );

if ( ! function_exists( 'nadlan_glossary_one_shot_publish' ) ) {
	function nadlan_glossary_one_shot_publish( $req ) {
		$p = $req->get_json_params(); if ( ! is_array( $p ) ) { $p = $req->get_params(); }
		$title = trim( (string) ( $p['title'] ?? '' ) );
		$body  = (string) ( $p['content_html'] ?? '' );
		if ( $title === '' || trim( wp_strip_all_tags( $body ) ) === '' ) {
			return new WP_REST_Response( array( 'ok' => false, 'error' => 'need_title_and_content' ), 400 );
		}
		// Idempotency: dedupe by exact title, or by term_en if provided.
		$existing = get_posts( array(
			'post_type'   => 'nadlan_term',
			'title'       => $title,
			'posts_per_page' => 1,
			'post_status' => 'any',
		) );
		if ( ! $existing && ! empty( $p['term_en'] ) ) {
			$existing = get_posts( array(
				'post_type' => 'nadlan_term', 'posts_per_page' => 1, 'post_status' => 'any',
				'meta_query' => array( array( 'key' => 'term_en', 'value' => $p['term_en'] ) ),
			) );
		}
		$words = nadlan_glossary_word_count( $body );
		$status = ( ( $p['status'] ?? 'publish' ) === 'draft' || $words < NADLAN_TERM_WORD_FLOOR ) ? 'draft' : 'publish';
		$existing_id = $existing ? (int) $existing[0]->ID : 0;
		$old_slug = $existing_id ? get_post_field( 'post_name', $existing_id ) : '';
		$ascii_slug = nadlan_glossary_ascii_post_slug( $title, (string) ( $p['term_en'] ?? '' ), $existing_id, $status );
		$args = array(
			'post_type'    => 'nadlan_term',
			'post_status'  => $status,
			'post_title'   => $title,
			'post_content' => wp_kses_post( $body ),
			'post_name'    => $ascii_slug,
		);
		if ( ! empty( $p['excerpt'] ) ) { $args['post_excerpt'] = sanitize_text_field( (string) $p['excerpt'] ); }
		if ( $existing ) {
			$args['ID'] = $existing_id;
			$id = wp_update_post( $args, true );
		} else {
			$id = wp_insert_post( $args, true );
		}
		if ( is_wp_error( $id ) ) {
			return new WP_REST_Response( array( 'ok' => false, 'error' => 'save_failed', 'detail' => $id->get_error_message() ), 500 );
		}
		if ( $old_slug && $old_slug !== get_post_field( 'post_name', $id ) && nadlan_glossary_has_non_ascii_slug( $old_slug ) ) {
			nadlan_glossary_store_redirect( 'term', $old_slug, get_permalink( $id ) );
			update_post_meta( $id, '_nadlan_old_glossary_slug', rawurldecode( $old_slug ) );
		}
		// Meta map
		$meta_keys = array( 'term_en', 'wikipedia_en', 'wikipedia_he', 'related_pillar', 'related_anchor', 'source_url', 'source_label' );
		foreach ( $meta_keys as $k ) {
			if ( isset( $p[ $k ] ) && $p[ $k ] !== '' ) {
				update_post_meta( $id, $k, sanitize_text_field( (string) $p[ $k ] ) );
			}
		}
		update_post_meta( $id, 'data_quality', $words >= NADLAN_TERM_WORD_FLOOR ? 'needs_review' : 'thin_draft' );
		// Category assignment
		if ( ! empty( $p['term_cat'] ) ) {
			$cats = is_array( $p['term_cat'] ) ? $p['term_cat'] : array( $p['term_cat'] );
			$term_ids = array();
			foreach ( $cats as $c ) {
				$c = trim( (string) $c );
				if ( $c === '' ) { continue; }
				$t = term_exists( $c, 'nadlan_term_cat' );
				if ( ! $t ) {
					$t = wp_insert_term( $c, 'nadlan_term_cat', array(
						'slug' => nadlan_glossary_ascii_slug_base( $c, 'glossary-category' ),
					) );
				}
				if ( ! is_wp_error( $t ) ) { $term_ids[] = (int) ( is_array( $t ) ? $t['term_id'] : $t ); }
			}
			if ( $term_ids ) { wp_set_object_terms( $id, $term_ids, 'nadlan_term_cat' ); }
		}
		// IndexNow ping (only on real publish)
		if ( $status === 'publish' && function_exists( 'nadlan_config_indexnow_ping' ) ) {
			nadlan_config_indexnow_ping( get_permalink( $id ) );
		}
		return new WP_REST_Response( array(
			'ok' => true,
			'id' => (int) $id,
			'url' => get_permalink( $id ),
			'status' => get_post_status( $id ),
			'was_update' => (bool) $existing,
		), 200 );
	}
}

/* IndexNow ping for terms on publish */
add_action( 'save_post_nadlan_term', function ( $post_id, $post ) {
	if ( $post->post_status === 'publish' && function_exists( 'nadlan_config_indexnow_ping' ) ) {
		nadlan_config_indexnow_ping( get_permalink( $post_id ) );
	}
}, 20, 2 );
