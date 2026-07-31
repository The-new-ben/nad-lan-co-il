<?php
/**
 * Batch 01 — real project images for the 10 worst archive cards (plugin edition).
 *
 * Moved here from the theme (2026-07-31): the theme never auto-deploys (static
 * chrome), so per the pipeline law all ongoing behavior — including these
 * images — ships inside this plugin. Images live at
 * assets/projects/batch-01/ within the plugin and ride the normal release zip.
 *
 * THE BUG THIS FIXES
 * When a project has no featured image and no photos_csv, the card falls back
 * to a rotation of generic theme images (directory.php `$theme_fallbacks`,
 * picked by `id % count`). An audit of the first 144 archive cards found 77
 * showing one of three place-specific stock photos — e.g. a Haifa project
 * illustrated with a Tel Aviv coastline. Batch 01 gives 10 of those projects
 * their own project-specific images (concept render + sketch with
 * source-verified badges, 1440x1080 WebP).
 *
 * HOW IT WIRES
 * One get_post_metadata filter supplies photos_csv (card image) and
 * project_model_poster (showroom sketch) for the mapped post IDs. Every
 * consumer — plugin directory card, theme card, showroom engine — reads those
 * same keys, so they all pick the images up at once.
 *
 * NON-DESTRUCTIVE: a real featured image wins (consumers check
 * has_post_thumbnail first) and a real stored meta value wins (checked below).
 * The batch steps aside the moment real developer material is uploaded.
 *
 * PROVENANCE: concept visualisations from planning data — NOT developer
 * material, NOT photographs. Badge figures are source-verified only; three
 * known unit-count conflicts are deliberately left OFF the images. Full trail:
 * docs/content/2026-07-31-project-images-batch-01.md in the repo.
 */
if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

if ( ! function_exists( 'nadlan_project_image_batch_map' ) ) {
	/** WordPress post ID => image basename (without -photo/-sketch suffix). */
	function nadlan_project_image_batch_map() {
		return array(
			5591 => '01-hagana-salvador-haifa',
			5590 => '02-ehad-haam-nahariya',
			5588 => '03-maale-gaaton-nahariya',
			5586 => '04-bialik-shimoni-beer-sheva',
			5585 => '05-ben-zvi-ramla',
			5583 => '06-haatzmaut-kiryat-bialik',
			3556 => '07-lev-hair-ramat-hasharon',
			3551 => '08-shvatei-israel-haifa',
			3545 => '09-reines-jerusalem',
			3543 => '10-yerushalayim-ness-ziona',
		);
	}
}

if ( ! function_exists( 'nadlan_project_image_batch_url' ) ) {
	/**
	 * Absolute URL for a batch image, or '' when not deployed (a partial
	 * deploy degrades to the old fallback, never a broken <img>).
	 *
	 * @param int    $post_id Project post ID.
	 * @param string $variant 'photo' or 'sketch'.
	 */
	function nadlan_project_image_batch_url( $post_id, $variant = 'photo' ) {
		$map     = nadlan_project_image_batch_map();
		$post_id = (int) $post_id;
		if ( ! isset( $map[ $post_id ] ) ) {
			return '';
		}
		$variant = ( 'sketch' === $variant ) ? 'sketch' : 'photo';
		$rel     = 'assets/projects/batch-01/' . $map[ $post_id ] . '-' . $variant . '.webp';
		$root    = dirname( __DIR__ ); // plugin root (this file lives in inc/)
		if ( ! file_exists( $root . '/' . $rel ) ) {
			return '';
		}
		return plugins_url( $rel, $root . '/nadlan-config.php' );
	}
}

/**
 * Supply photos_csv / project_model_poster for batch-01 projects that have no
 * real value of their own.
 */
add_filter(
	'get_post_metadata',
	function ( $value, $object_id, $meta_key, $single ) {
		if ( 'photos_csv' !== $meta_key && 'project_model_poster' !== $meta_key ) {
			return $value;
		}
		if ( null !== $value ) {
			return $value;
		}

		static $busy = false;
		if ( $busy ) {
			return $value;
		}

		$map       = nadlan_project_image_batch_map();
		$object_id = (int) $object_id;
		if ( ! isset( $map[ $object_id ] ) ) {
			return $value;
		}

		$busy     = true;
		$existing = trim( (string) get_post_meta( $object_id, $meta_key, true ) );
		$busy     = false;
		if ( '' !== $existing ) {
			return $value;
		}

		$url = nadlan_project_image_batch_url( $object_id, ( 'project_model_poster' === $meta_key ) ? 'sketch' : 'photo' );
		if ( '' === $url ) {
			return $value;
		}
		return $single ? $url : array( $url );
	},
	10,
	4
);
