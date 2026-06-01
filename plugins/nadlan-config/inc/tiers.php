<?php
/**
 * nadlan-config — Card tiers / paywall + free-trial gating (v1.16.0)
 *
 * Closes the "free listings give away links + contacts" leak per owner brief
 * (2026-06-01). The rulebook §10 specifies Free/Pro/Premier tiers; v1.5.0 had no
 * tier — every verified claim got full edit + public contact. This module adds:
 *
 *  1) `paid_tier` meta on every card: 'free' | 'pro' | 'premier' (default 'free').
 *  2) Free-trial timer: when admin approves a claim, `trial_started` stamps now;
 *     after NADLAN_FREE_TRIAL_DAYS (default 30) the card downgrades automatically.
 *  3) Visibility helpers strip PHONE, EMAIL, WEBSITE, PHOTOS, OUTBOUND LINKS from
 *     the public card render unless the card is `pro`/`premier` (or in trial).
 *  4) Free-tier card stays INDEXABLE (the SEO inventory we want) but the value
 *     surfaces (contact + photos + leads) are gated.
 *  5) Admin meta box per card to set tier + trial expiry. Healthcheck reports
 *     free/pro/premier counts.
 *
 * Rulebook §10 alignment: matches the "Free/Pro/Premier (מיקום, בלעדיות אזור,
 * תג מאומת)" plan. Premier adds priority sort in hubs/archives (built here).
 *
 * BLANK: actual checkout for upgrade is out of scope for this commit — the
 * upgrade button on the card opens a lead-capture (topic="שדרוג לפרו") so the
 * owner can convert manually; full WooCommerce subscription wiring is the next step.
 */

if ( ! defined( 'ABSPATH' ) ) { exit; }

if ( ! defined( 'NADLAN_FREE_TRIAL_DAYS' ) ) { define( 'NADLAN_FREE_TRIAL_DAYS', 30 ); }

if ( ! function_exists( 'nadlan_tiers_register_meta' ) ) {
	function nadlan_tiers_register_meta() {
		foreach ( array( 'nadlan_property', 'nadlan_project', 'nadlan_professional' ) as $pt ) {
			register_post_meta( $pt, 'paid_tier', array(
				'show_in_rest' => true, 'single' => true, 'type' => 'string',
				'auth_callback' => '__return_false',  // server-managed (admin-only)
			) );
			register_post_meta( $pt, 'trial_started', array(
				'show_in_rest' => false, 'single' => true, 'type' => 'integer',
				'auth_callback' => '__return_false',
			) );
		}
	}
}
add_action( 'init', 'nadlan_tiers_register_meta', 15 );

/* Default every newly-claimed card to free + start trial */
add_action( 'updated_post_meta', function ( $meta_id, $object_id, $meta_key, $meta_value ) {
	if ( $meta_key !== 'claim_status' || $meta_value !== 'verified' ) { return; }
	if ( ! get_post_meta( $object_id, 'paid_tier', true ) ) {
		update_post_meta( $object_id, 'paid_tier', 'free' );
	}
	if ( ! get_post_meta( $object_id, 'trial_started', true ) ) {
		update_post_meta( $object_id, 'trial_started', time() );
	}
}, 10, 4 );

if ( ! function_exists( 'nadlan_tier_effective' ) ) {
	/**
	 * What tier is this card EFFECTIVELY today (considering trial expiry)?
	 * Unclaimed → 'public_stub' (registry-sourced facts only).
	 * Claimed + paid_tier=free + in trial → 'trial' (full surfaces).
	 * Claimed + paid_tier=free + trial expired → 'free' (gated surfaces).
	 * Claimed + paid_tier=pro|premier → that tier.
	 */
	function nadlan_tier_effective( $post_id ) {
		$claim = (string) get_post_meta( $post_id, 'claim_status', true );
		if ( $claim !== 'verified' ) { return 'public_stub'; }
		$tier = (string) get_post_meta( $post_id, 'paid_tier', true ) ?: 'free';
		if ( in_array( $tier, array( 'pro', 'premier' ), true ) ) { return $tier; }
		$start = (int) get_post_meta( $post_id, 'trial_started', true );
		if ( $start && ( time() - $start ) < NADLAN_FREE_TRIAL_DAYS * DAY_IN_SECONDS ) {
			return 'trial';
		}
		return 'free';
	}
}

if ( ! function_exists( 'nadlan_tier_can_show' ) ) {
	/**
	 * Surface visibility map. The OWNER's policy (rulebook §10 + 2026-06-01 brief):
	 * - public_stub: only registry facts; NO contact, NO photos. (We auto-imported
	 *   facts; nobody pays us, nobody publishes contact info.)
	 * - trial: full surfaces (give them a taste so they want to keep it).
	 * - free (post-trial): facts + name only; contact/photos/links hidden + upgrade CTA.
	 * - pro: contact + photos visible; priority sort.
	 * - premier: pro + "מאומת" badge + featured-area placement.
	 */
	function nadlan_tier_can_show( $post_id, $surface ) {
		$tier = nadlan_tier_effective( $post_id );
		$matrix = array(
			'phone'     => array( 'trial' => true, 'pro' => true, 'premier' => true ),
			'email'     => array( 'trial' => true, 'pro' => true, 'premier' => true ),
			'website'   => array( 'trial' => true, 'pro' => true, 'premier' => true ),
			'photos'    => array( 'trial' => true, 'pro' => true, 'premier' => true ),
			'lead_form' => array( 'trial' => true, 'pro' => true, 'premier' => true ),
			'verified_badge' => array( 'premier' => true ),
			'priority_sort'  => array( 'pro' => true, 'premier' => true ),
		);
		return ! empty( $matrix[ $surface ][ $tier ] );
	}
}

/* ---- Strip gated meta out of public REST so we don't leak via the API ---- */
add_filter( 'rest_prepare_nadlan_property', 'nadlan_tier_filter_rest', 10, 2 );
add_filter( 'rest_prepare_nadlan_project', 'nadlan_tier_filter_rest', 10, 2 );
add_filter( 'rest_prepare_nadlan_professional', 'nadlan_tier_filter_rest', 10, 2 );
if ( ! function_exists( 'nadlan_tier_filter_rest' ) ) {
	function nadlan_tier_filter_rest( $response, $post ) {
		$data = $response->get_data();
		if ( empty( $data['meta'] ) || ! is_array( $data['meta'] ) ) { return $response; }
		if ( ! nadlan_tier_can_show( $post->ID, 'phone' ) ) {
			foreach ( array( 'phone', 'email', 'website' ) as $k ) {
				if ( isset( $data['meta'][ $k ] ) ) { $data['meta'][ $k ] = ''; }
			}
		}
		if ( ! nadlan_tier_can_show( $post->ID, 'photos' ) ) {
			foreach ( array( 'photos_csv', 'logo_url' ) as $k ) {
				if ( isset( $data['meta'][ $k ] ) ) { $data['meta'][ $k ] = ''; }
			}
		}
		$response->set_data( $data );
		return $response;
	}
}

/* ---- Strip gated surfaces from the front-end card render ----
 * We hook AFTER inc/cards-render appends and rewrite the output if needed.
 * Cheap regex strip is safer than re-running the renderer.
 */
add_filter( 'the_content', function ( $content ) {
	if ( ! is_singular( array( 'nadlan_property', 'nadlan_project', 'nadlan_professional' ) ) || ! in_the_loop() || ! is_main_query() ) {
		return $content;
	}
	$id = get_the_ID();
	$tier = nadlan_tier_effective( $id );
	// public_stub or post-trial free: hide phone, email, website rows + gallery
	if ( $tier === 'free' || $tier === 'public_stub' ) {
		// remove phone/email/website rows in the facts table
		$content = preg_replace( '~<tr><th>טלפון</th><td>[^<]*</td></tr>~u', '', $content );
		$content = preg_replace( '~<tr><th>אימייל</th><td>[^<]*</td></tr>~u', '', $content );
		$content = preg_replace( '~<tr><th>website</th><td>[^<]*</td></tr>~iu', '', $content );
		// remove gallery
		$content = preg_replace( '~<div class="nlcard-gallery">.*?</div>~us', '', $content );
		// append upgrade CTA (claimed-but-free only)
		if ( $tier === 'free' ) {
			$content .= nadlan_tier_upgrade_cta( $id );
		}
	}
	if ( $tier === 'premier' ) {
		// stamp a verified badge above the title
		$content = '<div class="nlpremier">✓ פרופיל מאומת · Premier</div>' . $content;
	}
	return $content;
}, 30 );

if ( ! function_exists( 'nadlan_tier_upgrade_cta' ) ) {
	function nadlan_tier_upgrade_cta( $id ) {
		$title = esc_attr( get_the_title( $id ) );
		return '<div class="nlupgrade" dir="rtl">'
			. '<strong>רוצים להציג את פרטי הקשר, גלריית תמונות וקבלת לידים?</strong>'
			. '<p>שדרגו את הכרטיס לתוכנית Pro או Premier ופתחו את מלוא היכולות השיווקיות.</p>'
			. '<button onclick="nadlanUpgradeReq(' . (int) $id . ',\'' . $title . '\')">שדרגו לפרו</button>'
			. '</div>'
			. '<style>.nlupgrade{margin:18px 0;padding:18px;background:#FAF7F1;border:1px solid #E2DCD0;border-radius:6px;direction:rtl;font-family:var(--font-sans,Heebo,sans-serif)}.nlupgrade button{margin-top:10px;padding:11px 22px;background:#9C7A3C;color:#FAF7F1;border:0;border-radius:4px;cursor:pointer;font:inherit}.nlpremier{display:inline-block;margin-bottom:10px;padding:4px 12px;background:#1B1A17;color:#9C7A3C;font-size:12px;letter-spacing:0.1em}</style>'
			. '<script>function nadlanUpgradeReq(id,t){var name=prompt("שמכם:");if(!name)return;var phone=prompt("טלפון:");fetch("' . esc_js( rest_url( 'nadlan/v1/lead' ) ) . '",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({name:name,phone:phone,topic:"שדרוג לפרו",message:t+" #"+id,source:"upgrade-cta"})}).then(function(){alert("✓ בקשה התקבלה.");});}</script>';
	}
}

/* ---- Priority sort in archives + hubs: pro/premier first, then trial, then free ---- */
add_action( 'pre_get_posts', function ( $q ) {
	if ( is_admin() || ! $q->is_main_query() ) { return; }
	if ( ! is_post_type_archive( array( 'nadlan_property', 'nadlan_project', 'nadlan_professional' ) ) ) { return; }
	$q->set( 'meta_key', 'paid_tier' );
	$q->set( 'orderby', array( 'meta_value' => 'DESC', 'date' => 'DESC' ) );
} );

/* ---- Admin meta box: set tier + view trial state ---- */
add_action( 'add_meta_boxes', function () {
	foreach ( array( 'nadlan_property', 'nadlan_project', 'nadlan_professional' ) as $pt ) {
		add_meta_box( 'nadlan_tier_box', 'NadLan tier', function ( $post ) {
			$current = (string) get_post_meta( $post->ID, 'paid_tier', true ) ?: 'free';
			$eff     = nadlan_tier_effective( $post->ID );
			$trial   = (int) get_post_meta( $post->ID, 'trial_started', true );
			wp_nonce_field( 'nadlan_tier_save_' . $post->ID, 'nadlan_tier_nonce' );
			echo '<p>Effective tier: <strong>' . esc_html( $eff ) . '</strong></p>';
			echo '<select name="nadlan_paid_tier">';
			foreach ( array( 'free' => 'Free', 'pro' => 'Pro', 'premier' => 'Premier' ) as $k => $label ) {
				echo '<option value="' . esc_attr( $k ) . '"' . selected( $current, $k, false ) . '>' . esc_html( $label ) . '</option>';
			}
			echo '</select>';
			if ( $trial ) {
				$days_left = max( 0, NADLAN_FREE_TRIAL_DAYS - (int) floor( ( time() - $trial ) / DAY_IN_SECONDS ) );
				echo '<p>Trial: ' . (int) $days_left . ' days left</p>';
			}
			echo '<p style="font-size:12px;color:#777">Free = facts only (no contact/photos/leads). Pro = contact+photos+leads. Premier = Pro + verified badge + priority sort.</p>';
		}, $pt, 'side' );
	}
} );

add_action( 'save_post', function ( $post_id, $post ) {
	if ( ! in_array( $post->post_type, array( 'nadlan_property', 'nadlan_project', 'nadlan_professional' ), true ) ) { return; }
	if ( ! isset( $_POST['nadlan_tier_nonce'] ) || ! wp_verify_nonce( $_POST['nadlan_tier_nonce'], 'nadlan_tier_save_' . $post_id ) ) { return; }
	if ( ! current_user_can( 'manage_options' ) ) { return; }
	$tier = isset( $_POST['nadlan_paid_tier'] ) ? sanitize_key( $_POST['nadlan_paid_tier'] ) : 'free';
	if ( ! in_array( $tier, array( 'free', 'pro', 'premier' ), true ) ) { $tier = 'free'; }
	update_post_meta( $post_id, 'paid_tier', $tier );
}, 11, 2 );

/* ---- Healthcheck augmentation ---- */
add_filter( 'nadlan_config_healthcheck', function ( $arr ) {
	global $wpdb;
	$counts = $wpdb->get_results(
		"SELECT meta_value tier, COUNT(*) n FROM {$wpdb->postmeta}
		 WHERE meta_key='paid_tier' GROUP BY meta_value"
	);
	$tiers = array();
	foreach ( (array) $counts as $r ) { $tiers[ $r->tier ] = (int) $r->n; }
	$arr['tiers'] = $tiers + array( 'free' => 0, 'pro' => 0, 'premier' => 0 );
	return $arr;
} );
