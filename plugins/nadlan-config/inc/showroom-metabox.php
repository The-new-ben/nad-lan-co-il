<?php
/**
 * Showroom control panel (meta box) for nadlan_project.
 *
 * Solves the owner's #1 pain: to configure a project's showroom you previously
 * had to open "Custom Fields", remember secret meta keys (nlp3d_use_engine, lat,
 * lng, project_model_glb, project_model_poster) and type raw values. This adds a
 * normal, labelled settings panel on the Project edit screen -- a checkbox and a
 * few text fields, no code. It writes the SAME meta keys the engine already reads
 * (see showroom-engine.php), so it just makes the existing wiring editable.
 *
 * Concept from Antigravity's buyer-journey work (2026-07-01); implemented cleanly
 * into the repo here with nonce + capability + sanitization.
 */
if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

add_action( 'add_meta_boxes', function () {
	add_meta_box(
		'nadlan_showroom_panel',
		'תצוגת פרויקט (Showroom תלת ממד / סקיצה)',
		'nadlan_showroom_metabox_render',
		'nadlan_project',
		'normal',
		'high'
	);
} );

function nadlan_showroom_metabox_render( $post ) {
	wp_nonce_field( 'nadlan_showroom_metabox', 'nadlan_showroom_metabox_nonce' );

	$enabled = get_post_meta( $post->ID, 'nlp3d_use_engine', true ) === '1';
	$lat     = (string) get_post_meta( $post->ID, 'lat', true );
	$lng     = (string) get_post_meta( $post->ID, 'lng', true );
	$glb     = (string) get_post_meta( $post->ID, 'project_model_glb', true );
	$poster  = (string) get_post_meta( $post->ID, 'project_model_poster', true );
	?>
	<style>
		.nadlan-sr-panel label { font-weight: 600; display: block; margin: 14px 0 4px; }
		.nadlan-sr-panel input[type="text"],
		.nadlan-sr-panel input[type="url"] { width: 100%; max-width: 640px; }
		.nadlan-sr-panel .desc { color: #666; font-size: 12px; margin: 3px 0 0; }
		.nadlan-sr-panel .row2 { display: flex; gap: 18px; flex-wrap: wrap; }
		.nadlan-sr-panel .row2 > div { flex: 1; min-width: 200px; }
	</style>
	<div class="nadlan-sr-panel" dir="rtl">
		<p>
			<label style="display:inline;font-weight:600;">
				<input type="checkbox" name="nadlan_sr_enable" value="1" <?php checked( $enabled ); ?>>
				הפעלת מנוע התצוגה (Showroom) בעמוד הפרויקט
			</label>
			<span class="desc">כשמסומן, עמוד הפרויקט מציג את בורר הדירות (תלת ממד או סקיצה) במקום התצוגה הישנה.</span>
		</p>

		<div class="row2">
			<div>
				<label for="nadlan_sr_lat">קו רוחב (Latitude)</label>
				<input type="text" id="nadlan_sr_lat" name="nadlan_sr_lat" value="<?php echo esc_attr( $lat ); ?>" placeholder="32.10557">
				<p class="desc">מהמפה של מדלן/גוגל. משמש למיקום הסימון במפה החיה.</p>
			</div>
			<div>
				<label for="nadlan_sr_lng">קו אורך (Longitude)</label>
				<input type="text" id="nadlan_sr_lng" name="nadlan_sr_lng" value="<?php echo esc_attr( $lng ); ?>" placeholder="34.78760">
			</div>
		</div>

		<label for="nadlan_sr_poster">כתובת תמונת הסקיצה / פוסטר</label>
		<input type="url" id="nadlan_sr_poster" name="nadlan_sr_poster" value="<?php echo esc_attr( $poster ); ?>" placeholder="https://…/sketch.jpg">
		<p class="desc">הסקיצה האדריכלית המוצגת לפני טעינת המודל (או במקומו). מומלץ להעלות למדיה ולהדביק כאן את הכתובת.</p>

		<label for="nadlan_sr_glb">כתובת מודל תלת ממד (GLB) - לא חובה</label>
		<input type="url" id="nadlan_sr_glb" name="nadlan_sr_glb" value="<?php echo esc_attr( $glb ); ?>" placeholder="https://…/model.glb">
		<p class="desc">אם ריק - התצוגה עוברת אוטומטית למצב סקיצה בלבד. אין צורך במודל כדי שהעמוד יעבוד.</p>
	</div>
	<?php
}

add_action( 'save_post_nadlan_project', function ( $post_id ) {
	if ( ! isset( $_POST['nadlan_showroom_metabox_nonce'] )
		|| ! wp_verify_nonce( sanitize_text_field( wp_unslash( $_POST['nadlan_showroom_metabox_nonce'] ) ), 'nadlan_showroom_metabox' ) ) {
		return;
	}
	if ( defined( 'DOING_AUTOSAVE' ) && DOING_AUTOSAVE ) {
		return;
	}
	if ( ! current_user_can( 'edit_post', $post_id ) ) {
		return;
	}

	update_post_meta( $post_id, 'nlp3d_use_engine', ! empty( $_POST['nadlan_sr_enable'] ) ? '1' : '0' );

	$lat = isset( $_POST['nadlan_sr_lat'] ) ? trim( sanitize_text_field( wp_unslash( $_POST['nadlan_sr_lat'] ) ) ) : '';
	$lng = isset( $_POST['nadlan_sr_lng'] ) ? trim( sanitize_text_field( wp_unslash( $_POST['nadlan_sr_lng'] ) ) ) : '';
	// Only accept plausible numeric coordinates; never store garbage that would misplace the pin.
	if ( $lat === '' || is_numeric( $lat ) ) { update_post_meta( $post_id, 'lat', $lat ); }
	if ( $lng === '' || is_numeric( $lng ) ) { update_post_meta( $post_id, 'lng', $lng ); }

	$poster = isset( $_POST['nadlan_sr_poster'] ) ? esc_url_raw( trim( (string) wp_unslash( $_POST['nadlan_sr_poster'] ) ) ) : '';
	$glb    = isset( $_POST['nadlan_sr_glb'] ) ? esc_url_raw( trim( (string) wp_unslash( $_POST['nadlan_sr_glb'] ) ) ) : '';
	update_post_meta( $post_id, 'project_model_poster', $poster );
	update_post_meta( $post_id, 'project_model_glb', $glb );
} );
