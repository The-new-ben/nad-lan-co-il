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
	<?php if ( $src ) : ?><p class="nlterm-src"><?php echo esc_html( $src_lbl ); ?>: <a href="<?php echo esc_url( $src ); ?>" target="_blank" rel="noopener nofollow"><?php echo esc_html( wp_parse_url( $src, PHP_URL_HOST ) ?: $src ); ?></a></p><?php endif; ?>
</div>
<style>
.nlterm{margin:20px 0;font-family:var(--font-sans,Heebo,sans-serif)}
.nlterm-en{font-size:14px;color:#5C564D}.nlterm-en span{font-weight:600}
.nlterm-up{background:#FAF7F1;border-inline-start:3px solid #9C7A3C;padding:14px 18px;border-radius:4px;margin:14px 0}
.nlterm-up span{display:block;font-size:13px;color:#5C564D;margin-bottom:4px}
.nlterm-up a{color:#1B1A17;font-weight:600;text-decoration:none}
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

/* IndexNow ping for terms on publish */
add_action( 'save_post_nadlan_term', function ( $post_id, $post ) {
	if ( $post->post_status === 'publish' && function_exists( 'nadlan_config_indexnow_ping' ) ) {
		nadlan_config_indexnow_ping( get_permalink( $post_id ) );
	}
}, 20, 2 );
