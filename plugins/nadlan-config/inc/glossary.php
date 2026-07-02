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

const NADLAN_TERM_WORD_FLOOR = 60;

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
	$enriched = get_post_meta( $id, 'data_quality', true ) === 'enriched';
	$words = max(
		str_word_count( wp_strip_all_tags( (string) get_post_field( 'post_content', $id ) ) ),
		count( preg_split( '/\s+/', trim( wp_strip_all_tags( (string) get_post_field( 'post_content', $id ) ) ) ) )
	);
	if ( ! $enriched && $words < NADLAN_TERM_WORD_FLOOR ) {
		$r['noindex'] = true; $r['follow'] = true; unset( $r['index'] );
	}
	return $r;
}, 20 );

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
			'posts_per_page' => $limit,
			'post__not_in'   => array( $id ),
			'orderby'        => 'rand',
			'tax_query'      => array( array(
				'taxonomy' => 'nadlan_term_cat', 'field' => 'term_id', 'terms' => $cats,
			) ),
		) );
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
		'inDefinedTermSet' => array( '@type' => 'DefinedTermSet', 'name' => 'מילון נדל"ן — נדלן', 'url' => home_url( '/glossary/' ) ),
		'sameAs' => get_post_meta( $id, 'wikipedia_en', true ) ?: null,
	) );
	echo "\n<script type=\"application/ld+json\">" . wp_json_encode( $data, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES ) . "</script>\n";
}, 20 );

/* /glossary/ index: grouped A-Z + by category (overrides archive body via content filter on the archive description is hard; use a shortcode the archive template or a page can host) */
add_shortcode( 'nadlan_glossary_index', function () {
	$terms = get_posts( array( 'post_type' => 'nadlan_term', 'posts_per_page' => 1000, 'orderby' => 'title', 'order' => 'ASC' ) );
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
		$status = ( ( $p['status'] ?? 'publish' ) === 'draft' ) ? 'draft' : 'publish';
		$args = array(
			'post_type'    => 'nadlan_term',
			'post_status'  => $status,
			'post_title'   => $title,
			'post_content' => wp_kses_post( $body ),
		);
		if ( ! empty( $p['excerpt'] ) ) { $args['post_excerpt'] = sanitize_text_field( (string) $p['excerpt'] ); }
		if ( $existing ) {
			$args['ID'] = (int) $existing[0]->ID;
			$id = wp_update_post( $args, true );
		} else {
			$id = wp_insert_post( $args, true );
		}
		if ( is_wp_error( $id ) ) {
			return new WP_REST_Response( array( 'ok' => false, 'error' => 'save_failed', 'detail' => $id->get_error_message() ), 500 );
		}
		// Meta map
		$meta_keys = array( 'term_en', 'wikipedia_en', 'wikipedia_he', 'related_pillar', 'related_anchor', 'source_url', 'source_label' );
		foreach ( $meta_keys as $k ) {
			if ( isset( $p[ $k ] ) && $p[ $k ] !== '' ) {
				update_post_meta( $id, $k, sanitize_text_field( (string) $p[ $k ] ) );
			}
		}
		update_post_meta( $id, 'data_quality', 'enriched' );
		// Category assignment
		if ( ! empty( $p['term_cat'] ) ) {
			$cats = is_array( $p['term_cat'] ) ? $p['term_cat'] : array( $p['term_cat'] );
			$term_ids = array();
			foreach ( $cats as $c ) {
				$c = trim( (string) $c );
				if ( $c === '' ) { continue; }
				$t = term_exists( $c, 'nadlan_term_cat' );
				if ( ! $t ) { $t = wp_insert_term( $c, 'nadlan_term_cat' ); }
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
