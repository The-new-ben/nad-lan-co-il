<?php
/**
 * Batch 01 — real project images for the 10 worst offender cards.
 *
 * THE BUG THIS FIXES
 * The archive/card grid falls back to a rotation of 5 generic theme images
 * (see plugins/nadlan-config/inc/directory.php ~line 713, `$theme_fallbacks`
 * picked by `id % 5`) whenever a project has no featured image and no
 * `photos_csv`. An audit of the first 144 archive cards found 77 of them
 * showing one of just three generic images:
 *   architectural-model.jpg (26), sea-view-interior.jpg (26),
 *   tel-aviv-coast-skyline.jpg (25).
 * A Haifa project rendering a Tel Aviv coastline is worse than no image.
 *
 * THE FIX (no wp-admin clicking required)
 * Batch 01 delivered 10 project-specific images (concept renders + sketch
 * variants with verified planning badges), sized 1440x1080 WebP, committed to
 * this theme at assets/projects/batch-01/. Every consumer of a project image
 * already reads the same two meta keys, so a single `get_post_metadata` filter
 * supplies them for these 10 posts and the whole chain picks it up:
 *   - photos_csv          -> theme card media + plugin directory card
 *   - project_model_poster -> showroom sketch/poster
 *
 * DELIBERATELY NON-DESTRUCTIVE
 * A real featured image always wins: both consumers check has_post_thumbnail()
 * BEFORE photos_csv. A real stored photos_csv/poster value also wins (checked
 * below). So this only fills a gap, and quietly steps aside the moment real
 * developer material is uploaded.
 *
 * PROVENANCE / HONESTY
 * These are concept visualisations made for NadLan from planning data, NOT
 * official developer material and NOT photographs of a built building. Badge
 * text on the sketch variants is limited to figures verified against a
 * planning/municipal/developer source. Full source list and confidence levels:
 * docs/content/2026-07-31-project-images-batch-01.md.
 *
 * Source batch: Google Drive "NadLan-Projects-Batch-01-10-Worst-2026-07-31",
 * manifest 00-BATCH-MANIFEST-HE.md + 00-GALLERY-MAP.csv.
 */
if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

if ( ! function_exists( 'nadlan_project_image_batch_map' ) ) {
	/**
	 * WordPress post ID => image basename (without the -photo/-sketch suffix).
	 * IDs come from the batch gallery map, verified against the live site.
	 */
	function nadlan_project_image_batch_map() {
		return array(
			5591 => '01-hagana-salvador-haifa',        // הגנה/סלוודור, חיפה
			5590 => '02-ehad-haam-nahariya',           // אחד העם 33-35, נהריה
			5588 => '03-maale-gaaton-nahariya',        // מעלה געתון, נהריה
			5586 => '04-bialik-shimoni-beer-sheva',    // ביאליק שמעוני, באר שבע
			5585 => '05-ben-zvi-ramla',                // בן צבי, רמלה
			5583 => '06-haatzmaut-kiryat-bialik',      // העצמאות, קריית ביאליק
			3556 => '07-lev-hair-ramat-hasharon',      // לב העיר סוקולוב, רמת השרון
			3551 => '08-shvatei-israel-haifa',         // שבטי ישראל 30-34, חיפה
			3545 => '09-reines-jerusalem',             // מתחם ריינס, ירושלים
			3543 => '10-yerushalayim-ness-ziona',      // מתחם ירושלים, נס ציונה
		);
	}
}

if ( ! function_exists( 'nadlan_project_image_batch_url' ) ) {
	/**
	 * Absolute URL for a batch image, or '' when the file is not deployed yet.
	 * The file_exists() guard means a partial deploy degrades to the old
	 * fallback instead of emitting a broken image.
	 *
	 * @param int    $post_id Project post ID.
	 * @param string $variant 'photo' or 'sketch'.
	 */
	function nadlan_project_image_batch_url( $post_id, $variant = 'photo' ) {
		$map = nadlan_project_image_batch_map();
		$post_id = (int) $post_id;
		if ( ! isset( $map[ $post_id ] ) ) {
			return '';
		}
		$variant  = ( $variant === 'sketch' ) ? 'sketch' : 'photo';
		$relative = 'assets/projects/batch-01/' . $map[ $post_id ] . '-' . $variant . '.webp';
		if ( ! file_exists( get_theme_file_path( $relative ) ) ) {
			return '';
		}
		return get_theme_file_uri( $relative );
	}
}

/**
 * Supply photos_csv / project_model_poster for batch-01 projects that have no
 * real value of their own. Runs on the raw metadata read so every consumer
 * (theme card, plugin directory card, showroom engine) is covered at once.
 */
add_filter(
	'get_post_metadata',
	function ( $value, $object_id, $meta_key, $single ) {
		if ( $meta_key !== 'photos_csv' && $meta_key !== 'project_model_poster' ) {
			return $value;
		}
		if ( null !== $value ) {
			return $value; // another filter already answered.
		}

		static $busy = false;
		if ( $busy ) {
			return $value; // re-entry guard for the real-value lookup below.
		}

		$map = nadlan_project_image_batch_map();
		$object_id = (int) $object_id;
		if ( ! isset( $map[ $object_id ] ) ) {
			return $value;
		}

		// A real stored value always wins over the batch image.
		$busy = true;
		$existing = trim( (string) get_post_meta( $object_id, $meta_key, true ) );
		$busy = false;
		if ( $existing !== '' ) {
			return $value;
		}

		$variant = ( $meta_key === 'project_model_poster' ) ? 'sketch' : 'photo';
		$url     = nadlan_project_image_batch_url( $object_id, $variant );
		if ( $url === '' ) {
			return $value;
		}

		return $single ? $url : array( $url );
	},
	10,
	4
);
