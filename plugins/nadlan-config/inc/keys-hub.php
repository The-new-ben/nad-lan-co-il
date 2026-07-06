<?php
/**
 * nadlan-config - Keys & Connections Hub (v1.69.94)
 *
 * ONE admin page for every external key and switch (owner request 2026-07-02:
 * "I'm sick and tired of looking for places to put keys"). Stores into the
 * SAME option names every module already reads, so nothing else changes:
 *   AI:      nadlan_ai_provider, nadlan_ai_openai_key, nadlan_ai_anthropic_key,
 *            nadlan_ai_enabled (master), nadlan_ai_widget_enabled (chat bubble)
 *   Mapbox:  nadlan_mapbox_token
 *   Media:   nadlan_home_video_url
 *   Contact: nadlan_whatsapp_e164, nadlan_phone
 *   Billing: nadlan_gi_api_key, nadlan_gi_ipn_secret (morning/greeninvoice)
 *
 * Secrets are keep-if-blank (an empty field never wipes a stored key) and are
 * never echoed back. Toggles + non-secret fields are also registered on the
 * REST settings endpoint so the agent can manage them; secret keys are NOT
 * REST-exposed and can only be set from this page.
 */

if ( ! defined( 'ABSPATH' ) ) { exit; }

if ( ! function_exists( 'nadlan_keys_hub_fields' ) ) {
	function nadlan_keys_hub_fields() {
		return array(
			'ai' => array( 'title' => 'בינה מלאכותית', 'fields' => array(
				array( 'nadlan_ai_provider', 'ספק ברירת מחדל', 'radio', array( 'openai' => 'OpenAI', 'anthropic' => 'Anthropic (Claude)' ) ),
				array( 'nadlan_ai_openai_key', 'OpenAI API Key', 'secret', 'sk-proj-...' ),
				array( 'nadlan_ai_anthropic_key', 'Anthropic (Claude) API Key', 'secret', 'sk-ant-...' ),
				array( 'nadlan_ai_enabled', 'AI פעיל (אשף מודעות, סיוע חכם, ניתוב פניות)', 'toggle', null ),
				array( 'nadlan_ai_widget_enabled', 'בועת צ׳אט צפה באתר (נפרד מה-AI עצמו)', 'toggle', null ),
			) ),
			'maps' => array( 'title' => 'מפות', 'fields' => array(
				array( 'nadlan_mapbox_token', 'Mapbox Token ציבורי (pk.)', 'text', 'pk.xxxx' ),
			) ),
			'media' => array( 'title' => 'מדיה', 'fields' => array(
				array( 'nadlan_home_video_url', 'סרטון עמוד הבית (YouTube / Vimeo / MP4)', 'text', 'https://...' ),
			) ),
			'contact' => array( 'title' => 'יצירת קשר', 'fields' => array(
				array( 'nadlan_whatsapp_e164', 'וואטסאפ (בינלאומי, ללא +)', 'text', '972525101555' ),
				array( 'nadlan_phone', 'טלפון לתצוגה', 'text', '052-510-1555' ),
			) ),
			'billing' => array( 'title' => 'סליקה וחשבוניות (morning)', 'fields' => array(
				array( 'nadlan_gi_api_key', 'morning / greeninvoice API Key', 'secret', '' ),
				array( 'nadlan_gi_ipn_secret', 'IPN Secret', 'secret', '' ),
			) ),
		);
	}
}

if ( ! function_exists( 'nadlan_keys_hub_secret_names' ) ) {
	function nadlan_keys_hub_secret_names() {
		$out = array();
		foreach ( nadlan_keys_hub_fields() as $sec ) {
			foreach ( $sec['fields'] as $f ) { if ( $f[2] === 'secret' ) { $out[] = $f[0]; } }
		}
		return $out;
	}
}

/* Non-secret fields + toggles on the REST settings endpoint (admin-auth only). */
add_action( 'rest_api_init', function () {
	foreach ( array( 'nadlan_ai_provider', 'nadlan_mapbox_token', 'nadlan_home_video_url', 'nadlan_whatsapp_e164', 'nadlan_phone' ) as $opt ) {
		register_setting( 'general', $opt, array( 'type' => 'string', 'sanitize_callback' => 'sanitize_text_field', 'default' => '', 'show_in_rest' => true ) );
	}
	register_setting( 'general', 'nadlan_ai_enabled', array( 'type' => 'integer', 'default' => 1, 'show_in_rest' => true ) );
	register_setting( 'general', 'nadlan_ai_widget_enabled', array( 'type' => 'string', 'default' => '0', 'show_in_rest' => true ) );
} );

add_action( 'admin_menu', function () {
	add_menu_page( 'נדלן: מפתחות וחיבורים', 'נדלן מפתחות', 'manage_options', 'nadlan-keys', 'nadlan_keys_hub_page', 'dashicons-admin-network', 59 );
} );

if ( ! function_exists( 'nadlan_keys_hub_page' ) ) {
	function nadlan_keys_hub_page() {
		if ( ! current_user_can( 'manage_options' ) ) { return; }
		$saved = false;
		if ( isset( $_POST['nadlan_keys_save'] ) && check_admin_referer( 'nadlan_keys_hub' ) ) {
			foreach ( nadlan_keys_hub_fields() as $sec ) {
				foreach ( $sec['fields'] as $f ) {
					list( $opt, , $type ) = $f;
					if ( $type === 'toggle' ) {
						update_option( $opt, isset( $_POST[ $opt ] ) ? 1 : 0 );
						continue;
					}
					if ( ! isset( $_POST[ $opt ] ) ) { continue; }
					$val = trim( sanitize_text_field( wp_unslash( $_POST[ $opt ] ) ) );
					if ( $type === 'secret' ) {
						if ( ! empty( $_POST[ 'clear_' . $opt ] ) ) { update_option( $opt, '' ); continue; }
						if ( $val === '' ) { continue; } // keep-if-blank
					}
					update_option( $opt, $val );
				}
			}
			$saved = true;
		}
		echo '<div class="wrap" dir="rtl"><h1>נדלן: מפתחות וחיבורים</h1>';
		echo '<p>כל המפתחות של האתר במקום אחד. שדות סודיים לא מוצגים חזרה: שדה ריק שומר על המפתח הקיים.</p>';
		if ( $saved ) { echo '<div class="notice notice-success"><p>נשמר.</p></div>'; }
		echo '<form method="post">';
		wp_nonce_field( 'nadlan_keys_hub' );
		foreach ( nadlan_keys_hub_fields() as $sec ) {
			echo '<h2>' . esc_html( $sec['title'] ) . '</h2><table class="form-table">';
			foreach ( $sec['fields'] as $f ) {
				list( $opt, $label, $type, $extra ) = array_pad( $f, 4, null );
				echo '<tr><th>' . esc_html( $label ) . '</th><td>';
				if ( $type === 'toggle' ) {
					printf( '<label><input type="checkbox" name="%1$s" %2$s> פעיל</label>', esc_attr( $opt ), checked( (int) get_option( $opt, $opt === 'nadlan_ai_enabled' ? 1 : 0 ), 1, false ) );
				} elseif ( $type === 'radio' && is_array( $extra ) ) {
					$cur = (string) get_option( $opt, array_key_first( $extra ) );
					foreach ( $extra as $val => $lbl ) {
						printf( '<label style="margin-inline-end:16px"><input type="radio" name="%1$s" value="%2$s" %3$s> %4$s</label>', esc_attr( $opt ), esc_attr( $val ), checked( $cur, $val, false ), esc_html( $lbl ) );
					}
				} elseif ( $type === 'secret' ) {
					$has = (string) get_option( $opt, '' ) !== '';
					printf( '<input type="password" name="%1$s" value="" class="regular-text" dir="ltr" placeholder="%2$s" autocomplete="new-password"> <span style="color:%3$s;font-weight:600">%4$s</span><br><label><input type="checkbox" name="clear_%1$s" value="1"> מחק מפתח שמור</label>',
						esc_attr( $opt ), esc_attr( (string) $extra ), $has ? '#2e7d32' : '#b91c1c', $has ? '✓ מפתח שמור' : 'לא הוגדר' );
				} else {
					printf( '<input type="text" name="%1$s" value="%2$s" class="regular-text" dir="ltr" placeholder="%3$s">', esc_attr( $opt ), esc_attr( (string) get_option( $opt, '' ) ), esc_attr( (string) $extra ) );
				}
				echo '</td></tr>';
			}
			echo '</table>';
		}
		echo '<p class="submit"><button type="submit" name="nadlan_keys_save" value="1" class="button-primary">שמור הכל</button></p></form>';
		echo '<hr><p style="color:#666">סטטוס: Mapbox ' . ( nadlan_mapbox_token() ? 'מחובר' : 'חסר' )
			. ' · AI ' . ( function_exists( 'nadlan_ai_enabled' ) && nadlan_ai_enabled() ? 'פעיל' : 'כבוי' )
			. ' · סרטון בית ' . ( get_option( 'nadlan_home_video_url' ) ? 'מוגדר' : 'ריק' ) . '</p></div>';
	}
}

/* Direct key handoff (owner ask 2026-07-06): a protected REST endpoint so the
 * owner can push API keys from his own machine (PowerShell/curl) without
 * touching wp-admin and without keys ever passing through chat or the repo.
 * Auth: WordPress application password of an admin (manage_options). */
add_action( 'rest_api_init', function () {
	register_rest_route( 'nadlan/v1', '/keys', array(
		'methods'  => 'POST',
		'permission_callback' => function () { return current_user_can( 'manage_options' ); },
		'callback' => function ( WP_REST_Request $req ) {
			$allowed = array(
				'openai_key'    => 'nadlan_ai_openai_key',
				'anthropic_key' => 'nadlan_ai_anthropic_key',
				'mapbox_token'  => 'nadlan_mapbox_token',
			);
			$saved = array();
			foreach ( $allowed as $in => $opt ) {
				$v = (string) $req->get_param( $in );
				if ( $v !== '' ) { update_option( $opt, trim( $v ), false ); $saved[] = $in; }
			}
			if ( ! $saved ) { return new WP_REST_Response( array( 'ok' => false, 'error' => 'no recognized key field' ), 400 ); }
			// never echo the key back - confirm by prefix + length only
			$probe = (string) get_option( 'nadlan_ai_openai_key', '' );
			return new WP_REST_Response( array(
				'ok' => true, 'saved' => $saved,
				'openai_key_present' => $probe !== '',
				'openai_key_shape'   => $probe !== '' ? ( substr( $probe, 0, 6 ) . '... (' . strlen( $probe ) . ' chars)' ) : '',
			), 200 );
		},
	) );
} );
