<?php
/**
 * nadlan-config - The encyclopedia WRITER (owner 2026-07-07: "something much
 * more sophisticated" than hand-feeding ChatGPT).
 *
 * A self-running editorial desk: every hour it picks staged skeleton drafts
 * (nadlan_term entries created by the intake), writes each one a full tiered
 * article through the site's own OpenAI key, validates it (word floor per
 * tier, dash law, clean HTML), and hands it to the publishing drip. The owner
 * feeds ontology batches; the site writes and publishes itself.
 *
 * Models routinely undershoot long-form word targets (measured 2026-07-06:
 * gpt-4o-mini returned 422 words against an 800-1300 brief, finish_reason
 * stop), so a draft below its tier floor gets ONE expand pass - the draft is
 * sent back with the measured count and the target, and the longer result
 * wins. After the expand pass a 10% tolerance applies (a 668-word article
 * against a 700 floor is a near-miss, not thin content); a real failure is
 * recorded, counted per entry, and an entry that failed 5 times is parked
 * (surfaced as "stuck" in the status endpoint) so it cannot block the queue
 * front and burn the API every tick.
 *
 * WP core gotcha (bit us 2026-07-06): wp_update_post on a draft whose
 * post_date_gmt is 0000-00-00 silently resets a passed post_date to "now"
 * unless edit_date is true - without it every "scheduled" article publishes
 * instantly. edit_date is mandatory on every drip hand-off.
 *
 * Controls (options): nadlan_enc_writer_enabled (1), nadlan_enc_writer_model
 * ('gpt-4o'), nadlan_enc_writer_daily (15 articles/day generation cap),
 * per-run cap 3 (keeps each cron tick short).
 * Status: GET /nadlan/v1/enc-writer-status.
 */

if ( ! defined( 'ABSPATH' ) ) { exit; }

add_action( 'init', function () {
	if ( ! wp_next_scheduled( 'nadlan_enc_writer_tick' ) ) {
		wp_schedule_event( time() + 600, 'hourly', 'nadlan_enc_writer_tick' );
	}
} );
add_action( 'nadlan_enc_writer_tick', 'nadlan_enc_writer_run' );

if ( ! function_exists( 'nadlan_enc_writer_run' ) ) {
	function nadlan_enc_writer_run() {
		if ( (int) get_option( 'nadlan_enc_writer_enabled', 1 ) !== 1 ) { return; }
		$key = function_exists( 'nadlan_ai_openai_key' ) ? nadlan_ai_openai_key() : (string) get_option( 'nadlan_ai_openai_key', '' );
		if ( $key === '' ) { return; }
		// daily generation cap
		$today = current_time( 'Y-m-d' );
		$stat  = get_option( 'nadlan_enc_writer_stat', array() );
		if ( ( $stat['date'] ?? '' ) !== $today ) { $stat = array( 'date' => $today, 'generated' => 0, 'failed' => 0 ); }
		$daily = max( 1, (int) get_option( 'nadlan_enc_writer_daily', 15 ) );
		$room  = $daily - (int) $stat['generated'];
		if ( $room <= 0 ) { return; }
		$batch = min( 3, $room );
		// skeletons: our entries (entity_type set) still below the article floor
		$q = new WP_Query( array(
			'post_type' => 'nadlan_term', 'post_status' => 'draft',
			'posts_per_page' => $batch * 2, 'orderby' => 'meta_value_num', 'meta_key' => 'enc_priority', 'order' => 'ASC',
			'fields' => 'ids', 'no_found_rows' => true,
			'meta_query' => array( array( 'key' => 'entity_type', 'compare' => 'EXISTS' ) ),
		) );
		$done = 0;
		foreach ( $q->posts as $pid ) {
			if ( $done >= $batch ) { break; }
			if ( (int) get_post_meta( $pid, 'enc_fail_count', true ) >= 5 ) { continue; } // stuck - needs a human look
			$words = count( preg_split( '/\s+/', trim( wp_strip_all_tags( (string) get_post_field( 'post_content', $pid ) ) ) ) );
			if ( $words >= 250 ) { continue; } // already written, awaiting drip elsewhere
			$ok = nadlan_enc_writer_write_one( $pid, $key );
			if ( $ok ) { $stat['generated']++; $done++; } else { $stat['failed']++; }
			update_option( 'nadlan_enc_writer_stat', $stat, false );
		}
	}
}

if ( ! function_exists( 'nadlan_enc_writer_write_one' ) ) {
	function nadlan_enc_writer_write_one( $pid, $key ) {
		$title   = get_the_title( $pid );
		$g       = function ( $k ) use ( $pid ) { return (string) get_post_meta( $pid, $k, true ); };
		$prio    = max( 1, min( 3, (int) ( $g( 'enc_priority' ) ?: 2 ) ) );
		$targets = array( 1 => array( 800, 1300, 700 ), 2 => array( 450, 700, 400 ), 3 => array( 250, 400, 250 ) );
		list( $lo, $hi, $floor ) = $targets[ $prio ];
		$system = 'אתה עורך ראשי של אנציקלופדיה מקצועית לנדל"ן ובנייה בעברית, ברמת ויקיפדיה ומעלה. הקורא הוא איש מקצוע. כללים קשיחים: אפס עובדות מומצאות - נתון לא ודאי מושמט; אסור מקף ארוך מכל סוג (רק מקף רגיל); המונח האנגלי משולב בגוף הטקסט; HTML נקי בלבד: h2, h3, p, ul, li, table, tr, th, td; בלי h1, בלי כותרת פותחת (הכותרת קיימת בעמוד), בלי סיכום שיווקי, בלי פניות לקורא. פתח ישר בפסקת הגדרה. מבנה: הגדרה; רקע או מנגנון; מפרט טכני עם מספרים והפניות לתקן או לחוק כשקיימים; ההקשר הישראלי; "בפרויקט אמיתי" - איך זה פוגש איש מקצוע בפועל; דוגמה מספרית או נוסחה כשהערך מתאים; טעויות נפוצות; משפט סיום ענייני. כותרות הסעיפים ינוסחו באופן טבעי ומותאם לערך, לא כהעתקה של רשימת המבנה. בערכים על אנשים או חברות: עובדות ביוגרפיות ניטרליות עם תאריכים בלבד. אורך היעד: ' . $lo . ' עד ' . $hi . ' מילים. החזר אך ורק את גוף ה-HTML, בלי גדרות קוד.';
		$user = 'כתוב את הערך האנציקלופדי המלא עבור: "' . $title . '"' .
			( $g( 'name_en' ) ? ' (EN: ' . $g( 'name_en' ) . ')' : '' ) .
			( $g( 'entity_type' ) ? ' | סוג ערך: ' . $g( 'entity_type' ) : '' ) .
			( $g( 'enc_domain' ) ? ' | תחום: ' . $g( 'enc_domain' ) : '' ) .
			( get_post_field( 'post_excerpt', $pid ) ? ' | הגדרה בסיסית: ' . get_post_field( 'post_excerpt', $pid ) : '' ) .
			( $g( 'enc_related' ) ? ' | ערכים קשורים לשילוב בטקסט: ' . $g( 'enc_related' ) : '' ) .
			( $g( 'enc_sources' ) ? ' | כיווני מקורות: ' . $g( 'enc_sources' ) : '' ) .
			' | אורך מחייב: לפחות ' . $lo . ' מילים.';
		$call = function ( $messages ) use ( $key ) {
			$resp = wp_remote_post( 'https://api.openai.com/v1/chat/completions', array(
				'timeout' => 120,
				'headers' => array( 'Authorization' => 'Bearer ' . $key, 'Content-Type' => 'application/json' ),
				'body'    => wp_json_encode( array(
					'model'       => (string) get_option( 'nadlan_enc_writer_model', 'gpt-4o' ),
					'temperature' => 0.4,
					'max_tokens'  => 6000,
					'messages'    => $messages,
				) ),
			) );
			if ( is_wp_error( $resp ) || 200 !== wp_remote_retrieve_response_code( $resp ) ) { return ''; }
			$body = json_decode( wp_remote_retrieve_body( $resp ), true );
			$html = trim( (string) ( $body['choices'][0]['message']['content'] ?? '' ) );
			$html = preg_replace( '/^```(?:html)?|```$/m', '', $html );
			// dash law: character swap only
			$html = str_replace( array( "\u{2013}", "\u{2014}" ), '-', $html );
			return wp_kses_post( trim( $html ) );
		};
		$wc_of    = function ( $html ) { return count( preg_split( '/\s+/', trim( wp_strip_all_tags( $html ) ) ) ); };
		$messages = array(
			array( 'role' => 'system', 'content' => $system ),
			array( 'role' => 'user', 'content' => $user ),
		);
		$html = $call( $messages );
		$wc   = $wc_of( $html );
		if ( '' !== $html && $wc < $floor ) {
			// expand pass: the draft goes back with the measured shortfall
			$messages[] = array( 'role' => 'assistant', 'content' => $html );
			$messages[] = array( 'role' => 'user', 'content' => 'הערך מכיל כרגע ' . $wc . ' מילים בלבד והיעד הוא ' . $lo . ' עד ' . $hi . ' מילים. הרחב והעמק אותו: פרט את המנגנון הטכני, ההקשר הישראלי, דוגמה מספרית וטעויות נפוצות ככל שחסר, בלי מלל ריק ובלי עובדות מומצאות. החזר את הערך המלא והמורחב בלבד, באותם כללי HTML.' );
			$html2 = $call( $messages );
			if ( $wc_of( $html2 ) > $wc ) { $html = $html2; $wc = $wc_of( $html ); }
			$floor = (int) floor( $floor * 0.9 ); // post-expansion tolerance: a near-miss is not thin content
		}
		if ( '' === $html || $wc < $floor ) {
			update_option( 'nadlan_enc_writer_last_fail', array( 'pid' => $pid, 'title' => $title, 'words' => $wc, 'floor' => $floor, 'at' => current_time( 'mysql' ) ), false );
			update_post_meta( $pid, 'enc_fail_count', (int) get_post_meta( $pid, 'enc_fail_count', true ) + 1 );
			return false; // too thin for its tier - retry next tick
		}
		// the title lives in the page template - drop a duplicated opening heading
		$html = preg_replace( '/^\s*<h[23][^>]*>\s*' . preg_quote( $title, '/' ) . '\s*<\/h[23]>\s*/u', '', $html );
		// hand to the publishing drip: next slot after the latest scheduled term
		$per_day = 12;
		$latest  = get_posts( array( 'post_type' => 'nadlan_term', 'post_status' => 'future', 'posts_per_page' => 1, 'orderby' => 'date', 'order' => 'DESC', 'fields' => 'ids' ) );
		if ( $latest ) {
			$last_ts = strtotime( get_post_field( 'post_date', $latest[0] ) );
			$count_that_day = count( get_posts( array( 'post_type' => 'nadlan_term', 'post_status' => 'future', 'posts_per_page' => 50, 'fields' => 'ids',
				'date_query' => array( array( 'year' => (int) date( 'Y', $last_ts ), 'month' => (int) date( 'n', $last_ts ), 'day' => (int) date( 'j', $last_ts ) ) ) ) ) );
			$stamp = $count_that_day >= $per_day
				? strtotime( date( 'Y-m-d 09:00:00', $last_ts ) ) + DAY_IN_SECONDS
				: $last_ts + (int) round( 10 * HOUR_IN_SECONDS / $per_day );
		} else {
			$stamp = current_time( 'timestamp' ) + HOUR_IN_SECONDS;
		}
		if ( $stamp <= current_time( 'timestamp' ) ) { $stamp = current_time( 'timestamp' ) + HOUR_IN_SECONDS; }
		wp_update_post( array( 'ID' => $pid, 'post_content' => $html, 'post_status' => 'future', 'post_date' => date( 'Y-m-d H:i:s', $stamp ), 'edit_date' => true ) );
		update_post_meta( $pid, 'enc_written_by', 'site-writer:' . get_option( 'nadlan_enc_writer_model', 'gpt-4o' ) );
		update_post_meta( $pid, 'enc_written_words', $wc );
		return true;
	}
}

/* status for the owner + agents */
add_action( 'rest_api_init', function () {
	register_rest_route( 'nadlan/v1', '/enc-writer-status', array(
		'methods' => 'GET', 'permission_callback' => '__return_true',
		'callback' => function () {
			$count = function ( $status ) {
				$q = new WP_Query( array( 'post_type' => 'nadlan_term', 'post_status' => $status, 'posts_per_page' => 1, 'fields' => 'ids' ) );
				return (int) $q->found_posts;
			};
			return array(
				'enabled'   => (int) get_option( 'nadlan_enc_writer_enabled', 1 ),
				'model'     => (string) get_option( 'nadlan_enc_writer_model', 'gpt-4o' ),
				'daily_cap' => (int) get_option( 'nadlan_enc_writer_daily', 15 ),
				'today'     => get_option( 'nadlan_enc_writer_stat', array() ),
				'last_fail' => get_option( 'nadlan_enc_writer_last_fail', null ),
				'stuck'     => (int) ( new WP_Query( array( 'post_type' => 'nadlan_term', 'post_status' => 'draft', 'posts_per_page' => 1, 'fields' => 'ids',
					'meta_query' => array( array( 'key' => 'enc_fail_count', 'value' => 5, 'compare' => '>=', 'type' => 'NUMERIC' ) ) ) ) )->found_posts,
				'skeletons_waiting' => $count( 'draft' ),
				'scheduled_to_publish' => $count( 'future' ),
				'published' => $count( 'publish' ),
			);
		},
	) );
} );
