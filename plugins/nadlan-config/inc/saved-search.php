<?php
/**
 * nadlan-config - Saved searches + email alerts (v1.8.0)
 *
 * Zillow/Redfin-grade proactive alerts (no external API). A visitor saves a search
 * (city / rooms / price / type); we double-opt-in their email, then a daily cron
 * matches NEW listings against each confirmed search and emails the matches.
 *
 * Store: private CPT nadlan_saved_search (meta: email, user_id, params JSON,
 * confirmed, token, last_run). Double opt-in = anti-spam + consent hygiene.
 *
 * BLANK (owner): alert frequency default = daily; web-push + WhatsApp alerts are
 * roadmap (docs/listings-questions.md §D). Branded email template = TODO.
 */

if ( ! defined( 'ABSPATH' ) ) { exit; }

if ( ! function_exists( 'nadlan_ss_register_cpt' ) ) {
	function nadlan_ss_register_cpt() {
		register_post_type( 'nadlan_saved_search', array(
			'labels' => array( 'name' => 'NadLan Saved Searches', 'singular_name' => 'Saved Search' ),
			'public' => false, 'show_ui' => true, 'show_in_menu' => true,
			'menu_icon' => 'dashicons-search', 'menu_position' => 31,
			'supports' => array( 'title', 'custom-fields' ),
		) );
	}
}
add_action( 'init', 'nadlan_ss_register_cpt' );

/* ---- build a meta_query from saved params ---- */
if ( ! function_exists( 'nadlan_ss_meta_query' ) ) {
	function nadlan_ss_meta_query( $params ) {
		$mq = array( 'relation' => 'AND' );
		if ( ! empty( $params['city'] ) )        { $mq[] = array( 'key' => 'city', 'value' => sanitize_text_field( $params['city'] ) ); }
		if ( ! empty( $params['listing_type'] ) ){ $mq[] = array( 'key' => 'listing_type', 'value' => sanitize_text_field( $params['listing_type'] ) ); }
		if ( ! empty( $params['rooms_min'] ) )   { $mq[] = array( 'key' => 'rooms', 'value' => (float) $params['rooms_min'], 'type' => 'NUMERIC', 'compare' => '>=' ); }
		if ( ! empty( $params['price_max'] ) )   { $mq[] = array( 'key' => 'price', 'value' => (int) $params['price_max'], 'type' => 'NUMERIC', 'compare' => '<=' ); }
		if ( ! empty( $params['price_min'] ) )   { $mq[] = array( 'key' => 'price', 'value' => (int) $params['price_min'], 'type' => 'NUMERIC', 'compare' => '>=' ); }
		return $mq;
	}
}

/* ---- REST: save a search (double opt-in) ---- */
add_action( 'rest_api_init', function () {
	register_rest_route( 'nadlan/v1', '/saved-search', array(
		'methods' => 'POST', 'permission_callback' => '__return_true',
		'callback' => 'nadlan_ss_create',
	) );
	register_rest_route( 'nadlan/v1', '/saved-search/confirm', array(
		'methods' => 'GET', 'permission_callback' => '__return_true',
		'callback' => 'nadlan_ss_confirm',
	) );
} );

if ( ! function_exists( 'nadlan_ss_create' ) ) {
	function nadlan_ss_create( $req ) {
		$p = $req->get_json_params(); if ( ! is_array( $p ) ) { $p = $req->get_params(); }
		if ( ! empty( $p['company'] ) ) { return new WP_REST_Response( array( 'ok' => true ), 200 ); } // honeypot
		$email = isset( $p['email'] ) ? sanitize_email( wp_unslash( (string) $p['email'] ) ) : '';
		if ( ! is_email( $email ) ) { return new WP_REST_Response( array( 'ok' => false, 'error' => 'email' ), 400 ); }
		// rate-limit per IP
		$iph = isset( $_SERVER['REMOTE_ADDR'] ) ? md5( $_SERVER['REMOTE_ADDR'] . 'ss' ) : 'x';
		if ( (int) get_transient( 'nadlan_ssrl_' . $iph ) >= 5 ) { return new WP_REST_Response( array( 'ok' => false, 'error' => 'rate' ), 429 ); }
		set_transient( 'nadlan_ssrl_' . $iph, ( (int) get_transient( 'nadlan_ssrl_' . $iph ) ) + 1, 10 * MINUTE_IN_SECONDS );

		$params = array(
			'city'         => sanitize_text_field( $p['city'] ?? '' ),
			'listing_type' => sanitize_text_field( $p['listing_type'] ?? '' ),
			'rooms_min'    => (float) ( $p['rooms_min'] ?? 0 ),
			'price_min'    => (int) ( $p['price_min'] ?? 0 ),
			'price_max'    => (int) ( $p['price_max'] ?? 0 ),
		);
		$token = strtolower( bin2hex( random_bytes( 16 ) ) );
		$id = wp_insert_post( array(
			'post_type' => 'nadlan_saved_search', 'post_status' => 'publish',
			'post_title' => $email . ' - ' . ( $params['city'] ?: 'הכל' ),
		), true );
		if ( is_wp_error( $id ) ) { return new WP_REST_Response( array( 'ok' => false ), 500 ); }
		update_post_meta( $id, 'email', $email );
		update_post_meta( $id, 'user_id', get_current_user_id() );
		update_post_meta( $id, 'params', wp_json_encode( $params ) );
		update_post_meta( $id, 'confirmed', is_user_logged_in() ? 1 : 0 ); // logged-in = trusted
		update_post_meta( $id, 'token', $token );
		update_post_meta( $id, 'last_run', time() );

		if ( ! is_user_logged_in() ) {
			$link = add_query_arg( array( 'id' => $id, 'token' => $token ), rest_url( 'nadlan/v1/saved-search/confirm' ) );
			wp_mail( $email, 'אישור התראות נכסים - נדלן',
				"קיבלנו בקשה לקבלת התראות על נכסים חדשים התואמים לחיפוש שלך.\n\nלאישור לחצו:\n$link\n\nאם לא ביקשתם, התעלמו מהודעה זו." );
		}
		return new WP_REST_Response( array( 'ok' => true, 'id' => $id, 'confirm_required' => ! is_user_logged_in() ), 200 );
	}
}

if ( ! function_exists( 'nadlan_ss_confirm' ) ) {
	function nadlan_ss_confirm( $req ) {
		$id = (int) $req->get_param( 'id' );
		$token = sanitize_text_field( (string) $req->get_param( 'token' ) );
		if ( $id && get_post_type( $id ) === 'nadlan_saved_search'
			&& hash_equals( (string) get_post_meta( $id, 'token', true ), $token ) ) {
			update_post_meta( $id, 'confirmed', 1 );
			wp_safe_redirect( home_url( '/?saved_search=confirmed' ) );
			exit;
		}
		wp_safe_redirect( home_url( '/?saved_search=invalid' ) );
		exit;
	}
}

/* ---- daily cron: match new listings, email ---- */
if ( ! function_exists( 'nadlan_ss_run_alerts' ) ) {
	function nadlan_ss_run_alerts() {
		$searches = get_posts( array( 'post_type' => 'nadlan_saved_search', 'posts_per_page' => 500,
			'meta_query' => array( array( 'key' => 'confirmed', 'value' => 1 ) ) ) );
		foreach ( $searches as $s ) {
			$email  = (string) get_post_meta( $s->ID, 'email', true );
			if ( ! is_email( $email ) ) { continue; }
			$params = json_decode( (string) get_post_meta( $s->ID, 'params', true ), true ) ?: array();
			$last   = (int) get_post_meta( $s->ID, 'last_run', true ) ?: ( time() - DAY_IN_SECONDS );
			$q = new WP_Query( array(
				'post_type' => 'nadlan_property', 'posts_per_page' => 20, 'no_found_rows' => true,
				'date_query' => array( array( 'after' => gmdate( 'Y-m-d H:i:s', $last ), 'column' => 'post_date_gmt' ) ),
				'meta_query' => nadlan_ss_meta_query( $params ),
			) );
			if ( $q->have_posts() ) {
				$lines = "נכסים חדשים התואמים לחיפוש שלך:\n\n";
				foreach ( $q->posts as $p ) {
					$price = get_post_meta( $p->ID, 'price', true );
					$lines .= '• ' . get_the_title( $p ) . ( $price ? ' - ₪' . number_format( (float) $price ) : '' ) . "\n  " . get_permalink( $p ) . "\n";
				}
				$lines .= "\nלהסרה מההתראות השיבו למייל זה.";
				wp_mail( $email, 'נכסים חדשים - נדלן', $lines );
			}
			update_post_meta( $s->ID, 'last_run', time() );
			wp_reset_postdata();
		}
	}
}
add_action( 'nadlan_ss_daily', 'nadlan_ss_run_alerts' );
if ( ! wp_next_scheduled( 'nadlan_ss_daily' ) ) {
	wp_schedule_event( time() + 3600, 'daily', 'nadlan_ss_daily' );
}

/* ---- shortcode: save-search form ---- */
add_shortcode( 'nadlan_save_search', function () {
	ob_start(); ?>
<form class="nlss" dir="rtl" onsubmit="return nadlanSaveSearch(this)">
	<h3>קבלו התראה על נכסים חדשים</h3>
	<input type="text" name="city" placeholder="עיר">
	<input type="number" name="rooms_min" placeholder="חדרים (מינ')" step="0.5">
	<input type="number" name="price_max" placeholder="מחיר מקסימלי">
	<input type="email" name="email" placeholder="אימייל" required>
	<input type="text" name="company" style="position:absolute;left:-9999px" tabindex="-1" aria-hidden="true">
	<button type="submit">שמרו חיפוש</button>
	<span class="nlss-msg"></span>
</form>
<script>
function nadlanSaveSearch(f){
	var d={city:f.city.value,rooms_min:+f.rooms_min.value,price_max:+f.price_max.value,email:f.email.value,company:f.company.value};
	var msg=f.querySelector('.nlss-msg');
	fetch('<?php echo esc_url_raw( rest_url( 'nadlan/v1/saved-search' ) ); ?>',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(d)})
	.then(function(r){return r.json();}).then(function(j){
		if(j.ok){f.reset();msg.textContent=j.confirm_required?'✓ שלחנו מייל לאישור ההרשמה.':'✓ נרשמת לקבלת התראות.';msg.style.color='#2e7d32';}
		else{msg.textContent='שגיאה, בדקו את האימייל.';msg.style.color='#c00';}
	}).catch(function(){msg.textContent='שגיאת רשת.';msg.style.color='#c00';});
	return false;
}
</script>
<style>.nlss{max-width:380px;margin:18px 0;font-family:var(--font-sans,Heebo,sans-serif)}.nlss input{display:block;width:100%;margin:6px 0;padding:10px;border:1px solid #ccc;border-radius:4px}.nlss button{padding:11px 22px;background:#1B1A17;color:#FAF7F1;border:0;border-radius:4px;cursor:pointer}.nlss button:hover{background:#9C7A3C;color:#1B1A17}.nlss-msg{display:block;margin-top:8px;font-size:14px}</style>
	<?php
	return ob_get_clean();
} );
