<?php
/**
 * nadlan-config - Chunk D automated lead nurture (v1.54.0).
 *
 * Ships dark behind nadlan_feature_lead_nurture. The flow starts only after
 * Chunk B lead E2E capture and reuses Chunk C score/handoff data when present.
 */

if ( ! defined( 'ABSPATH' ) ) { exit; }

if ( ! function_exists( 'nadlan_lead_nurture_enabled' ) ) {
	function nadlan_lead_nurture_enabled() {
		if ( get_option( 'nadlan_feature_lead_nurture', '0' ) !== '1' ) { return false; }
		if ( ! function_exists( 'nadlan_lead_e2e_enabled' ) || ! nadlan_lead_e2e_enabled() ) { return false; }
		return (bool) apply_filters( 'nadlan_lead_nurture_enabled', true );
	}
}

if ( ! function_exists( 'nadlan_lead_nurture_default_templates' ) ) {
	function nadlan_lead_nurture_default_templates() {
		$unsubscribe = "\n\nלהפסקת הודעות המשך: {{unsubscribe}}";
		return array(
			'hot'  => array(
				'day1'      => array(
					'delay'   => 1,
					'subject' => 'המשך טיפול בפנייה שלך לגבי {{card}}',
					'body'    => "שלום {{name}},\n\nבהמשך לפנייה שלך לגבי {{card}}, אנחנו רוצים לוודא שהפרטים הגיעו לגורם הנכון ושיש לך מענה ברור.\n\nאם התקציב ולוח הזמנים כבר מוגדרים, אפשר להשיב למייל הזה ונעדכן את בעל הכרטיס כדי לקדם שיחה ממוקדת בתוך 24 שעות." . $unsubscribe,
				),
				'day3'      => array(
					'delay'   => 3,
					'subject' => 'בדיקה קצרה לפני שמתקדמים',
					'body'    => "שלום {{name}},\n\nרצינו לבדוק אם עדיין רלוונטי להתקדם לגבי {{card}}. כדי לחבר אותך נכון, השאלה החשובה היא האם המהלך מתוכנן לחודש הקרוב או למועד מאוחר יותר.\n\nתשובה קצרה למייל הזה מספיקה כדי שנכוון את הטיפול." . $unsubscribe,
				),
				'day7'      => array(
					'delay'   => 7,
					'subject' => 'אפשר לעזור לסגור את השלב הבא?',
					'body'    => "שלום {{name}},\n\nעבר שבוע מאז הפנייה שלך לגבי {{card}}. אם עדיין יש עניין, אפשר להשיב עם מסגרת תקציב או יעד זמן ונעזור לקדם את השלב הבא בצורה מסודרת.\n\nאם זה כבר טופל, אפשר להתעלם או להסיר את הודעות ההמשך." . $unsubscribe,
				),
				'day14'     => array(
					'delay'   => 14,
					'subject' => 'סיכום ביניים לפנייה שלך',
					'body'    => "שלום {{name}},\n\nאנחנו סוגרים מעגל לגבי {{card}}. אם הנושא עדיין פתוח, נשמח לקבל תשובה אחת: האם העדיפות היא מחיר, זמינות או התאמה מקצועית.\n\nכך נוכל להעביר את המידע בצורה מדויקת יותר." . $unsubscribe,
				),
				'monthly_1' => array(
					'delay'   => 30,
					'subject' => 'בדיקה חודשית עדינה לגבי {{card}}',
					'body'    => "שלום {{name}},\n\nרק בודקים אם הצורך סביב {{card}} עדיין רלוונטי. אם כן, אפשר להשיב עם עדכון קצר ונחזיר את הפנייה למסלול טיפול.\n\nאם לא, לא צריך לעשות דבר." . $unsubscribe,
				),
			),
			'warm' => array(
				'day1'      => array(
					'delay'   => 1,
					'subject' => 'המשך לפנייה שלך בנדלן',
					'body'    => "שלום {{name}},\n\nקיבלנו את הפנייה שלך לגבי {{card}} ורצינו לעזור לדייק את ההמשך.\n\nמה יותר חשוב כרגע: מסגרת תקציב, זמינות בחודש הקרוב או התאמה מקצועית? תשובה קצרה תעזור לנו לקדם את הטיפול." . $unsubscribe,
				),
				'day3'      => array(
					'delay'   => 3,
					'subject' => 'שאלה אחת כדי לדייק את הטיפול',
					'body'    => "שלום {{name}},\n\nכדי להמשיך נכון לגבי {{card}}, אפשר להשיב עם מסגרת התקציב המשוערת או עם לוח הזמנים הרצוי.\n\nאנחנו שומרים את הפנייה פתוחה כדי שלא תאבד." . $unsubscribe,
				),
				'day7'      => array(
					'delay'   => 7,
					'subject' => 'האם הפנייה עדיין רלוונטית?',
					'body'    => "שלום {{name}},\n\nרצינו לוודא אם הפנייה לגבי {{card}} עדיין רלוונטית. אם כן, אפשר להשיב במילה אחת: עכשיו, בקרוב או בהמשך.\n\nנעדכן את הטיפול בהתאם." . $unsubscribe,
				),
				'day14'     => array(
					'delay'   => 14,
					'subject' => 'אפשר לסגור או להמשיך את הפנייה',
					'body'    => "שלום {{name}},\n\nאנחנו עושים סדר בפניות פתוחות. אם עדיין תרצה/י להמשיך לגבי {{card}}, אפשר להשיב עם השלב הבא הרצוי.\n\nאם זה כבר לא רלוונטי, לא נמשיך להעמיס." . $unsubscribe,
				),
				'monthly_1' => array(
					'delay'   => 30,
					'subject' => 'עדכון חודשי קצר',
					'body'    => "שלום {{name}},\n\nבודקים בעדינות אם הצורך סביב {{card}} חזר להיות רלוונטי. אם כן, אפשר להשיב ונחדש את הטיפול.\n\nאנחנו זמינים לעזור כשזה מתאים לך." . $unsubscribe,
				),
			),
			'cold' => array(
				'day7'      => array(
					'delay'   => 7,
					'subject' => 'בדיקה קצרה לגבי הפנייה שלך',
					'body'    => "שלום {{name}},\n\nרק בודקים אם הפנייה לגבי {{card}} עדיין פתוחה. אם כן, אפשר להשיב עם לוח הזמנים הרצוי ונעזור להמשיך.\n\nאם זה לא רלוונטי כרגע, לא צריך לעשות דבר." . $unsubscribe,
				),
				'day14'     => array(
					'delay'   => 14,
					'subject' => 'נסגור מעגל או נמשיך?',
					'body'    => "שלום {{name}},\n\nאנחנו סוגרים מעגל לגבי {{card}}. אם תרצה/י שנמשיך לטפל בזה, מספיק להשיב למייל הזה עם תקציב משוער או זמן יעד.\n\nאם לא, הפנייה תישאר שקטה." . $unsubscribe,
				),
				'monthly_1' => array(
					'delay'   => 30,
					'subject' => 'בדיקה חודשית שקטה',
					'body'    => "שלום {{name}},\n\nאם הצורך סביב {{card}} חזר להיות רלוונטי, אפשר להשיב ונעזור לפתוח את הטיפול מחדש.\n\nבלי תגובה, לא נעשה פעולה נוספת מעבר לעדכון חודשי שקט." . $unsubscribe,
				),
			),
		);
	}
}

if ( ! function_exists( 'nadlan_lead_nurture_templates' ) ) {
	function nadlan_lead_nurture_templates() {
		$defaults = nadlan_lead_nurture_default_templates();
		$saved = get_option( 'nadlan_lead_nurture_templates', array() );
		if ( ! is_array( $saved ) ) { return $defaults; }
		foreach ( $defaults as $tier => $steps ) {
			foreach ( $steps as $step => $template ) {
				if ( isset( $saved[ $tier ][ $step ]['subject'] ) && trim( (string) $saved[ $tier ][ $step ]['subject'] ) !== '' ) {
					$defaults[ $tier ][ $step ]['subject'] = sanitize_text_field( (string) $saved[ $tier ][ $step ]['subject'] );
				}
				if ( isset( $saved[ $tier ][ $step ]['body'] ) && trim( (string) $saved[ $tier ][ $step ]['body'] ) !== '' ) {
					$defaults[ $tier ][ $step ]['body'] = sanitize_textarea_field( (string) $saved[ $tier ][ $step ]['body'] );
				}
			}
		}
		return $defaults;
	}
}

if ( ! function_exists( 'nadlan_lead_nurture_tier' ) ) {
	function nadlan_lead_nurture_tier( $lead_id ) {
		$tier = sanitize_key( (string) get_post_meta( (int) $lead_id, 'lead_ai_tier', true ) );
		if ( in_array( $tier, array( 'hot', 'warm', 'cold' ), true ) ) { return $tier; }
		$score = get_post_meta( (int) $lead_id, 'lead_score', true );
		if ( $score !== '' && is_numeric( $score ) ) {
			if ( function_exists( 'nadlan_lead_ai_tier' ) ) { return nadlan_lead_ai_tier( (int) $score ); }
			if ( (int) $score >= 70 ) { return 'hot'; }
			if ( (int) $score < 40 ) { return 'cold'; }
		}
		return 'warm';
	}
}

if ( ! function_exists( 'nadlan_lead_nurture_template_for' ) ) {
	function nadlan_lead_nurture_template_for( $tier, $step ) {
		$tier = in_array( sanitize_key( $tier ), array( 'hot', 'warm', 'cold' ), true ) ? sanitize_key( $tier ) : 'warm';
		$step = sanitize_key( (string) $step );
		$templates = nadlan_lead_nurture_templates();
		if ( isset( $templates[ $tier ][ $step ] ) ) { return $templates[ $tier ][ $step ]; }
		if ( strpos( $step, 'monthly_' ) === 0 && isset( $templates[ $tier ]['monthly_1'] ) ) {
			$template = $templates[ $tier ]['monthly_1'];
			$template['delay'] = 30;
			return $template;
		}
		return null;
	}
}

if ( ! function_exists( 'nadlan_lead_nurture_log' ) ) {
	function nadlan_lead_nurture_log( $entry ) {
		$entry = is_array( $entry ) ? $entry : array();
		$row = array(
			't'       => time(),
			'lead_id' => (int) ( $entry['lead_id'] ?? 0 ),
			'step'    => sanitize_key( (string) ( $entry['step'] ?? '' ) ),
			'status'  => sanitize_key( (string) ( $entry['status'] ?? '' ) ),
			'reason'  => sanitize_key( (string) ( $entry['reason'] ?? '' ) ),
			'tier'    => sanitize_key( (string) ( $entry['tier'] ?? '' ) ),
			'channel' => sanitize_key( (string) ( $entry['channel'] ?? 'email' ) ),
			'sent_at' => (int) ( $entry['sent_at'] ?? 0 ),
		);
		$log = get_option( 'nadlan_lead_nurture_log', array() );
		if ( ! is_array( $log ) ) { $log = array(); }
		array_unshift( $log, $row );
		update_option( 'nadlan_lead_nurture_log', array_slice( $log, 0, 1500 ), false );
		if ( function_exists( 'nadlan_log_event' ) ) {
			nadlan_log_event( 'lead_nurture', $row['status'] ?: 'event', 'ok', array(
				'lead_ref' => $row['lead_id'],
				'step'     => $row['step'],
				'reason'   => $row['reason'],
				'tier'     => $row['tier'],
			) );
		}
		return $row;
	}
}

if ( ! function_exists( 'nadlan_lead_nurture_fields' ) ) {
	function nadlan_lead_nurture_fields( $lead_id ) {
		if ( function_exists( 'nadlan_lead_ai_fields' ) ) { return nadlan_lead_ai_fields( $lead_id ); }
		$keys = array( 'name', 'phone', 'email', 'goal', 'city', 'budget', 'timeline', 'message', 'source_url', 'utm_source', 'utm_campaign' );
		$out = array();
		foreach ( $keys as $key ) {
			$out[ $key ] = get_post_meta( (int) $lead_id, $key, true );
		}
		if ( empty( $out['message'] ) ) {
			$post = get_post( (int) $lead_id );
			$out['message'] = $post ? $post->post_content : '';
		}
		$out['email'] = sanitize_email( (string) $out['email'] );
		$out['phone'] = preg_replace( '/[^0-9+]/', '', (string) $out['phone'] );
		$out['message'] = sanitize_textarea_field( (string) $out['message'] );
		foreach ( array( 'name', 'goal', 'city', 'budget', 'timeline', 'utm_source', 'utm_campaign' ) as $key ) {
			$out[ $key ] = sanitize_text_field( (string) $out[ $key ] );
		}
		$out['source_url'] = esc_url_raw( (string) $out['source_url'] );
		return $out;
	}
}

if ( ! function_exists( 'nadlan_lead_nurture_card_title' ) ) {
	function nadlan_lead_nurture_card_title( $lead_id ) {
		$card_id = (int) get_post_meta( (int) $lead_id, 'lead_card_id', true );
		$title = $card_id ? trim( wp_strip_all_tags( (string) get_the_title( $card_id ), true ) ) : '';
		return $title !== '' ? $title : 'פנייתך';
	}
}

if ( ! function_exists( 'nadlan_lead_nurture_secret' ) ) {
	function nadlan_lead_nurture_secret( $lead_id ) {
		$lead_id = absint( $lead_id );
		$token = (string) get_post_meta( $lead_id, 'lead_nurture_unsub_token', true );
		if ( $token === '' ) {
			$token = function_exists( 'wp_generate_password' ) ? wp_generate_password( 32, false, false ) : strtolower( bin2hex( random_bytes( 16 ) ) );
			update_post_meta( $lead_id, 'lead_nurture_unsub_token', $token );
		}
		return $token;
	}
}

if ( ! function_exists( 'nadlan_lead_nurture_signed_token' ) ) {
	function nadlan_lead_nurture_signed_token( $lead_id ) {
		$lead_id = absint( $lead_id );
		$secret = nadlan_lead_nurture_secret( $lead_id );
		$sig = hash_hmac( 'sha256', $lead_id . '|' . $secret, wp_salt( 'auth' ) );
		return $secret . '.' . $sig;
	}
}

if ( ! function_exists( 'nadlan_lead_nurture_verify_token' ) ) {
	function nadlan_lead_nurture_verify_token( $lead_id, $signed_token ) {
		$lead_id = absint( $lead_id );
		$signed_token = sanitize_text_field( (string) $signed_token );
		if ( ! $lead_id || $signed_token === '' || strpos( $signed_token, '.' ) === false ) { return false; }
		list( $secret, $sig ) = array_pad( explode( '.', $signed_token, 2 ), 2, '' );
		$expected_secret = (string) get_post_meta( $lead_id, 'lead_nurture_unsub_token', true );
		if ( $expected_secret === '' || ! hash_equals( $expected_secret, $secret ) ) { return false; }
		$expected_sig = hash_hmac( 'sha256', $lead_id . '|' . $secret, wp_salt( 'auth' ) );
		return hash_equals( $expected_sig, $sig );
	}
}

if ( ! function_exists( 'nadlan_lead_nurture_unsubscribe_url' ) ) {
	function nadlan_lead_nurture_unsubscribe_url( $lead_id ) {
		return add_query_arg( array(
			'lead'  => absint( $lead_id ),
			'token' => rawurlencode( nadlan_lead_nurture_signed_token( $lead_id ) ),
		), rest_url( 'nadlan/v1/nurture/unsubscribe' ) );
	}
}

if ( ! function_exists( 'nadlan_lead_nurture_replace_tokens' ) ) {
	function nadlan_lead_nurture_replace_tokens( $text, $lead_id, $fields = null ) {
		$fields = is_array( $fields ) ? $fields : nadlan_lead_nurture_fields( $lead_id );
		$replacements = array(
			'{{name}}'        => trim( (string) ( $fields['name'] ?? '' ) ) !== '' ? trim( (string) $fields['name'] ) : 'שלום',
			'{{card}}'        => nadlan_lead_nurture_card_title( $lead_id ),
			'{{site}}'        => get_bloginfo( 'name' ),
			'{{url}}'         => home_url( '/' ),
			'{{unsubscribe}}' => nadlan_lead_nurture_unsubscribe_url( $lead_id ),
		);
		return strtr( (string) $text, $replacements );
	}
}

if ( ! function_exists( 'nadlan_lead_nurture_scheduled_steps' ) ) {
	function nadlan_lead_nurture_scheduled_steps( $lead_id ) {
		$steps = get_post_meta( (int) $lead_id, 'lead_nurture_scheduled_steps', true );
		return is_array( $steps ) ? $steps : array();
	}
}

if ( ! function_exists( 'nadlan_lead_nurture_has_state' ) ) {
	function nadlan_lead_nurture_has_state( $lead_id ) {
		$state = sanitize_key( (string) get_post_meta( (int) $lead_id, 'lead_nurture_state', true ) );
		return in_array( $state, array( 'active', 'stopped' ), true ) || ! empty( nadlan_lead_nurture_scheduled_steps( $lead_id ) );
	}
}

if ( ! function_exists( 'nadlan_lead_nurture_update_scheduled_steps' ) ) {
	function nadlan_lead_nurture_update_scheduled_steps( $lead_id, $steps ) {
		$clean = array();
		foreach ( (array) $steps as $step => $due ) {
			$step = sanitize_key( (string) $step );
			$due = (int) $due;
			if ( $step !== '' && $due > 0 ) { $clean[ $step ] = $due; }
		}
		update_post_meta( (int) $lead_id, 'lead_nurture_scheduled_steps', $clean );
	}
}

if ( ! function_exists( 'nadlan_lead_nurture_remove_scheduled_step' ) ) {
	function nadlan_lead_nurture_remove_scheduled_step( $lead_id, $step ) {
		$steps = nadlan_lead_nurture_scheduled_steps( $lead_id );
		unset( $steps[ sanitize_key( (string) $step ) ] );
		nadlan_lead_nurture_update_scheduled_steps( $lead_id, $steps );
	}
}

if ( ! function_exists( 'nadlan_lead_nurture_stop_reason' ) ) {
	function nadlan_lead_nurture_stop_reason( $lead_id ) {
		$lead_id = absint( $lead_id );
		if ( ! $lead_id || get_post_type( $lead_id ) !== 'nadlan_lead' ) { return ''; }
		if ( (int) get_post_meta( $lead_id, 'lead_nurture_unsubscribed_at', true ) > 0 ) { return 'unsubscribe'; }
		$status = sanitize_key( (string) get_post_meta( $lead_id, 'lead_status', true ) );
		if ( in_array( $status, array( 'contacted', 'won', 'lost' ), true ) ) { return 'status_' . $status; }
		if ( (int) get_post_meta( $lead_id, 'lead_ai_handoff', true ) > 0 ) { return 'ai_handoff'; }
		foreach ( array( 'lead_replied_at', 'lead_reply_received_at', 'lead_has_reply' ) as $key ) {
			if ( (string) get_post_meta( $lead_id, $key, true ) !== '' && (int) get_post_meta( $lead_id, $key, true ) !== 0 ) {
				return 'reply';
			}
		}
		return '';
	}
}

if ( ! function_exists( 'nadlan_lead_nurture_unschedule' ) ) {
	function nadlan_lead_nurture_unschedule( $lead_id ) {
		$lead_id = absint( $lead_id );
		foreach ( array_keys( nadlan_lead_nurture_scheduled_steps( $lead_id ) ) as $step ) {
			$args = array( $lead_id, sanitize_key( $step ) );
			while ( $ts = wp_next_scheduled( 'nadlan_lead_nurture_send_touch', $args ) ) {
				wp_unschedule_event( $ts, 'nadlan_lead_nurture_send_touch', $args );
			}
		}
		nadlan_lead_nurture_update_scheduled_steps( $lead_id, array() );
	}
}

if ( ! function_exists( 'nadlan_lead_nurture_stop' ) ) {
	function nadlan_lead_nurture_stop( $lead_id, $reason ) {
		$lead_id = absint( $lead_id );
		if ( ! $lead_id || get_post_type( $lead_id ) !== 'nadlan_lead' ) { return false; }
		$reason = sanitize_key( (string) $reason );
		if ( $reason === '' ) { $reason = 'stopped'; }
		if ( get_post_meta( $lead_id, 'lead_nurture_state', true ) === 'stopped' ) { return true; }
		update_post_meta( $lead_id, 'lead_nurture_state', 'stopped' );
		update_post_meta( $lead_id, 'lead_nurture_stop_reason', $reason );
		update_post_meta( $lead_id, 'lead_nurture_stopped_at', time() );
		nadlan_lead_nurture_unschedule( $lead_id );
		nadlan_lead_nurture_log( array(
			'lead_id' => $lead_id,
			'status'  => 'stopped',
			'reason'  => $reason,
			'tier'    => nadlan_lead_nurture_tier( $lead_id ),
		) );
		return true;
	}
}

if ( ! function_exists( 'nadlan_lead_nurture_schedule_step' ) ) {
	function nadlan_lead_nurture_schedule_step( $lead_id, $step, $due_ts, $tier = '' ) {
		$lead_id = absint( $lead_id );
		$step = sanitize_key( (string) $step );
		$due_ts = (int) $due_ts;
		if ( ! $lead_id || $step === '' || $due_ts <= 0 ) { return false; }
		if ( get_post_meta( $lead_id, '_nadlan_lead_nurture_sent_' . $step, true ) !== '' ) { return false; }
		$steps = nadlan_lead_nurture_scheduled_steps( $lead_id );
		if ( isset( $steps[ $step ] ) ) {
			if ( ! wp_next_scheduled( 'nadlan_lead_nurture_send_touch', array( $lead_id, $step ) ) ) {
				wp_schedule_single_event( (int) $steps[ $step ], 'nadlan_lead_nurture_send_touch', array( $lead_id, $step ) );
			}
			return true;
		}
		$steps[ $step ] = $due_ts;
		nadlan_lead_nurture_update_scheduled_steps( $lead_id, $steps );
		if ( ! wp_next_scheduled( 'nadlan_lead_nurture_send_touch', array( $lead_id, $step ) ) ) {
			wp_schedule_single_event( $due_ts, 'nadlan_lead_nurture_send_touch', array( $lead_id, $step ) );
		}
		nadlan_lead_nurture_log( array(
			'lead_id' => $lead_id,
			'step'    => $step,
			'status'  => 'scheduled',
			'tier'    => $tier !== '' ? $tier : nadlan_lead_nurture_tier( $lead_id ),
		) );
		return true;
	}
}

if ( ! function_exists( 'nadlan_lead_nurture_schedule_for_lead' ) ) {
	function nadlan_lead_nurture_schedule_for_lead( $lead_id, $card_id = 0, $fields = array(), $route = array() ) {
		$lead_id = absint( $lead_id );
		if ( ! $lead_id || get_post_type( $lead_id ) !== 'nadlan_lead' ) { return false; }
		if ( ! nadlan_lead_nurture_enabled() ) { return false; }
		$stop = nadlan_lead_nurture_stop_reason( $lead_id );
		if ( $stop !== '' ) { return nadlan_lead_nurture_stop( $lead_id, $stop ); }
		if ( get_post_meta( $lead_id, 'lead_nurture_state', true ) === 'active' ) { return true; }
		$lead_fields = nadlan_lead_nurture_fields( $lead_id );
		if ( ! is_email( $lead_fields['email'] ) ) {
			update_post_meta( $lead_id, 'lead_nurture_state', 'stopped' );
			update_post_meta( $lead_id, 'lead_nurture_stop_reason', 'no_email' );
			nadlan_lead_nurture_log( array( 'lead_id' => $lead_id, 'status' => 'stopped', 'reason' => 'no_email' ) );
			return false;
		}
		$tier = nadlan_lead_nurture_tier( $lead_id );
		$templates = nadlan_lead_nurture_templates();
		if ( empty( $templates[ $tier ] ) ) { $tier = 'warm'; }
		update_post_meta( $lead_id, 'lead_nurture_state', 'active' );
		update_post_meta( $lead_id, 'lead_nurture_started_at', time() );
		update_post_meta( $lead_id, 'lead_nurture_tier', $tier );
		foreach ( $templates[ $tier ] as $step => $template ) {
			$delay = max( 1, (int) ( $template['delay'] ?? 1 ) );
			nadlan_lead_nurture_schedule_step( $lead_id, $step, time() + ( $delay * DAY_IN_SECONDS ), $tier );
		}
		do_action( 'nadlan_lead_nurture_scheduled', $lead_id, $tier );
		return true;
	}
}
add_action( 'nadlan_lead_e2e_captured', 'nadlan_lead_nurture_schedule_for_lead', 40, 4 );

if ( ! function_exists( 'nadlan_lead_nurture_send_touch' ) ) {
	function nadlan_lead_nurture_send_touch( $lead_id, $step ) {
		$lead_id = absint( $lead_id );
		$step = sanitize_key( (string) $step );
		if ( ! $lead_id || $step === '' || get_post_type( $lead_id ) !== 'nadlan_lead' ) { return false; }
		if ( ! nadlan_lead_nurture_enabled() ) {
			nadlan_lead_nurture_log( array( 'lead_id' => $lead_id, 'step' => $step, 'status' => 'skipped', 'reason' => 'feature_off' ) );
			return false;
		}
		$stop = nadlan_lead_nurture_stop_reason( $lead_id );
		if ( $stop !== '' ) { return nadlan_lead_nurture_stop( $lead_id, $stop ); }
		if ( get_post_meta( $lead_id, 'lead_nurture_state', true ) !== 'active' ) {
			nadlan_lead_nurture_log( array( 'lead_id' => $lead_id, 'step' => $step, 'status' => 'skipped', 'reason' => 'not_active' ) );
			return false;
		}
		$guard_key = '_nadlan_lead_nurture_sent_' . $step;
		if ( ! add_post_meta( $lead_id, $guard_key, time(), true ) ) {
			nadlan_lead_nurture_log( array( 'lead_id' => $lead_id, 'step' => $step, 'status' => 'skipped', 'reason' => 'duplicate' ) );
			return false;
		}
		nadlan_lead_nurture_remove_scheduled_step( $lead_id, $step );
		$tier = nadlan_lead_nurture_tier( $lead_id );
		$template = nadlan_lead_nurture_template_for( $tier, $step );
		if ( ! $template ) {
			nadlan_lead_nurture_log( array( 'lead_id' => $lead_id, 'step' => $step, 'status' => 'failed', 'reason' => 'template_missing', 'tier' => $tier ) );
			return false;
		}
		$fields = nadlan_lead_nurture_fields( $lead_id );
		$email = sanitize_email( (string) ( $fields['email'] ?? '' ) );
		if ( ! is_email( $email ) ) {
			nadlan_lead_nurture_stop( $lead_id, 'no_email' );
			return false;
		}
		$subject = nadlan_lead_nurture_replace_tokens( (string) $template['subject'], $lead_id, $fields );
		$body = nadlan_lead_nurture_replace_tokens( (string) $template['body'], $lead_id, $fields );
		$unsubscribe = nadlan_lead_nurture_unsubscribe_url( $lead_id );
		if ( strpos( $body, $unsubscribe ) === false ) {
			$body .= "\n\nלהפסקת הודעות המשך: " . $unsubscribe;
		}
		$card_id = (int) get_post_meta( $lead_id, 'lead_card_id', true );
		$headers = array( 'Content-Type: text/plain; charset=UTF-8' );
		$send_fields = $fields;
		$send_fields['_delivery_context'] = 'lead_nurture';
		$send_fields['_delivery_subject'] = $subject;
		$send_fields['_recipient_email'] = $email;
		$send_fields['_nurture_step'] = $step;
		$sent = apply_filters( 'nadlan_lead_deliver', false, 0, $lead_id, $card_id, $body, $send_fields, $headers );
		if ( is_wp_error( $sent ) ) { $sent = false; }
		if ( ! $sent ) { $sent = wp_mail( $email, $subject, $body, $headers ); }
		update_post_meta( $lead_id, 'lead_nurture_last_step', $step );
		update_post_meta( $lead_id, 'lead_nurture_last_sent_at', time() );
		nadlan_lead_nurture_log( array(
			'lead_id' => $lead_id,
			'step'    => $step,
			'status'  => $sent ? 'sent' : 'failed',
			'reason'  => $sent ? '' : 'mail_failed',
			'tier'    => $tier,
			'sent_at' => $sent ? time() : 0,
		) );
		if ( $sent ) {
			do_action( 'nadlan_lead_nurture_touch', $lead_id, $step );
			if ( strpos( $step, 'monthly_' ) === 0 ) {
				$max = max( 1, min( 24, (int) get_option( 'nadlan_lead_nurture_monthly_max', 6 ) ) );
				$current = (int) str_replace( 'monthly_', '', $step );
				if ( $current > 0 && $current < $max && nadlan_lead_nurture_stop_reason( $lead_id ) === '' ) {
					nadlan_lead_nurture_schedule_step( $lead_id, 'monthly_' . ( $current + 1 ), time() + 30 * DAY_IN_SECONDS, $tier );
				}
			}
		}
		return (bool) $sent;
	}
}
add_action( 'nadlan_lead_nurture_send_touch', 'nadlan_lead_nurture_send_touch', 10, 2 );

if ( ! function_exists( 'nadlan_lead_nurture_tick' ) ) {
	function nadlan_lead_nurture_tick() {
		if ( ! nadlan_lead_nurture_enabled() ) { return; }
		$q = new WP_Query( array(
			'post_type'              => 'nadlan_lead',
			'post_status'            => 'any',
			'fields'                 => 'ids',
			'posts_per_page'         => 200,
			'no_found_rows'          => true,
			'update_post_meta_cache' => true,
			'meta_query'             => array( array( 'key' => 'lead_nurture_state', 'value' => 'active' ) ),
		) );
		$now = time();
		foreach ( (array) $q->posts as $lead_id ) {
			$stop = nadlan_lead_nurture_stop_reason( $lead_id );
			if ( $stop !== '' ) {
				nadlan_lead_nurture_stop( $lead_id, $stop );
				continue;
			}
			foreach ( nadlan_lead_nurture_scheduled_steps( $lead_id ) as $step => $due ) {
				if ( (int) $due <= $now ) {
					nadlan_lead_nurture_send_touch( $lead_id, $step );
				}
			}
		}
	}
}
add_action( 'nadlan_lead_nurture_tick', 'nadlan_lead_nurture_tick' );

if ( ! function_exists( 'nadlan_lead_nurture_ensure_cron' ) ) {
	function nadlan_lead_nurture_ensure_cron() {
		if ( nadlan_lead_nurture_enabled() ) {
			if ( ! wp_next_scheduled( 'nadlan_lead_nurture_tick' ) ) {
				wp_schedule_event( time() + HOUR_IN_SECONDS, 'hourly', 'nadlan_lead_nurture_tick' );
			}
			return;
		}
		while ( $ts = wp_next_scheduled( 'nadlan_lead_nurture_tick' ) ) {
			wp_unschedule_event( $ts, 'nadlan_lead_nurture_tick' );
		}
	}
}
add_action( 'init', 'nadlan_lead_nurture_ensure_cron' );

if ( ! function_exists( 'nadlan_lead_nurture_meta_changed' ) ) {
	function nadlan_lead_nurture_meta_changed( $meta_id, $object_id, $meta_key, $meta_value ) {
		$lead_id = absint( $object_id );
		if ( ! $lead_id || get_post_type( $lead_id ) !== 'nadlan_lead' ) { return; }
		if ( ! nadlan_lead_nurture_enabled() && ! nadlan_lead_nurture_has_state( $lead_id ) ) { return; }
		$key = (string) $meta_key;
		if ( $key === 'lead_status' ) {
			$status = sanitize_key( (string) $meta_value );
			if ( in_array( $status, array( 'contacted', 'won', 'lost' ), true ) ) {
				nadlan_lead_nurture_stop( $lead_id, 'status_' . $status );
			}
			return;
		}
		if ( $key === 'lead_ai_handoff' && (int) $meta_value > 0 ) {
			nadlan_lead_nurture_stop( $lead_id, 'ai_handoff' );
			return;
		}
		if ( in_array( $key, array( 'lead_replied_at', 'lead_reply_received_at', 'lead_has_reply' ), true ) && (string) $meta_value !== '' && (int) $meta_value !== 0 ) {
			nadlan_lead_nurture_stop( $lead_id, 'reply' );
			return;
		}
		if ( $key === 'lead_nurture_unsubscribed_at' && (int) $meta_value > 0 ) {
			nadlan_lead_nurture_stop( $lead_id, 'unsubscribe' );
		}
	}
}
add_action( 'added_post_meta', 'nadlan_lead_nurture_meta_changed', 10, 4 );
add_action( 'updated_post_meta', 'nadlan_lead_nurture_meta_changed', 10, 4 );
add_action( 'nadlan_lead_ai_handoff', function ( $lead_id ) {
	if ( nadlan_lead_nurture_enabled() || nadlan_lead_nurture_has_state( $lead_id ) ) {
		nadlan_lead_nurture_stop( $lead_id, 'ai_handoff' );
	}
}, 10, 1 );
add_action( 'nadlan_lead_replied', function ( $lead_id ) {
	if ( nadlan_lead_nurture_enabled() || nadlan_lead_nurture_has_state( $lead_id ) ) {
		nadlan_lead_nurture_stop( $lead_id, 'reply' );
	}
}, 10, 1 );

if ( ! function_exists( 'nadlan_lead_nurture_rate_limit' ) ) {
	function nadlan_lead_nurture_rate_limit() {
		if ( function_exists( 'nadlan_hardening_rate_limit' ) ) {
			return nadlan_hardening_rate_limit( 'nurture_unsubscribe', 8, MINUTE_IN_SECONDS );
		}
		$ip = isset( $_SERVER['REMOTE_ADDR'] ) ? sanitize_text_field( wp_unslash( $_SERVER['REMOTE_ADDR'] ) ) : '0.0.0.0';
		$key = 'nadlan_nurture_unsub_rl_' . md5( $ip );
		$count = (int) get_transient( $key );
		if ( $count >= 8 ) { return false; }
		set_transient( $key, $count + 1, MINUTE_IN_SECONDS );
		return true;
	}
}

if ( ! function_exists( 'nadlan_lead_nurture_rest_unsubscribe' ) ) {
	function nadlan_lead_nurture_rest_unsubscribe( WP_REST_Request $req ) {
		if ( ! nadlan_lead_nurture_rate_limit() ) {
			return new WP_Error( 'rate_limited', 'rate_limited', array( 'status' => 429 ) );
		}
		$lead_id = absint( $req->get_param( 'lead' ) );
		$token = sanitize_text_field( (string) $req->get_param( 'token' ) );
		if ( ! $lead_id || get_post_type( $lead_id ) !== 'nadlan_lead' || $token === '' ) {
			return new WP_Error( 'invalid', 'invalid', array( 'status' => 422 ) );
		}
		if ( ! nadlan_lead_nurture_verify_token( $lead_id, $token ) ) {
			return new WP_Error( 'forbidden', 'forbidden', array( 'status' => 403 ) );
		}
		update_post_meta( $lead_id, 'lead_nurture_unsubscribed_at', time() );
		nadlan_lead_nurture_stop( $lead_id, 'unsubscribe' );
		return new WP_REST_Response( array(
			'ok'      => true,
			'lead_id' => $lead_id,
			'status'  => 'unsubscribed',
		), 200 );
	}
}

add_action( 'rest_api_init', function () {
	register_rest_route( 'nadlan/v1', '/nurture/unsubscribe', array(
		'methods'             => 'GET',
		'permission_callback' => '__return_true',
		'callback'            => 'nadlan_lead_nurture_rest_unsubscribe',
	) );
} );

if ( ! function_exists( 'nadlan_lead_nurture_metrics' ) ) {
	function nadlan_lead_nurture_metrics( $days = 7 ) {
		$days = max( 1, (int) $days );
		$since = time() - $days * DAY_IN_SECONDS;
		$log = get_option( 'nadlan_lead_nurture_log', array() );
		if ( ! is_array( $log ) ) { $log = array(); }
		$out = array(
			'loaded'            => true,
			'enabled'           => nadlan_lead_nurture_enabled(),
			'flag_on'           => get_option( 'nadlan_feature_lead_nurture', '0' ) === '1',
			'scheduled'         => 0,
			'sent'              => 0,
			'failed'            => 0,
			'skipped'           => 0,
			'stopped_by_reason' => array(),
			'log_entries'       => count( $log ),
		);
		foreach ( $log as $row ) {
			if ( ! is_array( $row ) || (int) ( $row['t'] ?? 0 ) < $since ) { continue; }
			$status = sanitize_key( (string) ( $row['status'] ?? '' ) );
			if ( isset( $out[ $status ] ) && is_int( $out[ $status ] ) ) { $out[ $status ]++; }
			if ( $status === 'stopped' ) {
				$reason = sanitize_key( (string) ( $row['reason'] ?? 'stopped' ) );
				if ( $reason === '' ) { $reason = 'stopped'; }
				if ( ! isset( $out['stopped_by_reason'][ $reason ] ) ) { $out['stopped_by_reason'][ $reason ] = 0; }
				$out['stopped_by_reason'][ $reason ]++;
			}
		}
		foreach ( array( 'active', 'stopped' ) as $state ) {
			$q = new WP_Query( array(
				'post_type'      => 'nadlan_lead',
				'post_status'    => 'any',
				'fields'         => 'ids',
				'posts_per_page' => 1,
				'no_found_rows'  => false,
				'meta_query'     => array( array( 'key' => 'lead_nurture_state', 'value' => $state ) ),
			) );
			$out[ $state ] = (int) $q->found_posts;
		}
		return $out;
	}
}

add_filter( 'nadlan_config_healthcheck', function ( $out ) {
	$out['lead_nurture'] = nadlan_lead_nurture_metrics( 7 );
	return $out;
} );

add_filter( 'nadlan_metrics_snapshot', function ( $snapshot ) {
	$m = nadlan_lead_nurture_metrics( 7 );
	$snapshot['lead_nurture'] = $m;
	$snapshot['lead_nurture_sent_7d'] = $m['sent'];
	$snapshot['lead_nurture_scheduled_7d'] = $m['scheduled'];
	return $snapshot;
} );

if ( ! function_exists( 'nadlan_lead_nurture_render_ops_panel' ) ) {
	function nadlan_lead_nurture_render_ops_panel() {
		if ( ! current_user_can( 'manage_options' ) ) { return; }
		$m = nadlan_lead_nurture_metrics( 7 );
		?>
		<h2 style="margin-top:28px">Lead Nurture</h2>
		<p class="description">רצף הודעות המשך לפניות שלא קיבלו מענה, עם עצירה אוטומטית כשיש תגובה, סטטוס או הסרה.</p>
		<div class="nlops-grid">
			<div class="nlops-card">
				<h2>מצב רצף המשך</h2>
				<div class="nlops-row"><span>דגל הפעלה</span><strong><?php echo $m['flag_on'] ? 'ON' : 'OFF'; ?></strong></div>
				<div class="nlops-row"><span>תוזמנו 7 ימים</span><strong><?php echo (int) $m['scheduled']; ?></strong></div>
				<div class="nlops-row"><span>נשלחו 7 ימים</span><strong><?php echo (int) $m['sent']; ?></strong></div>
				<div class="nlops-row"><span>פעילים עכשיו</span><strong><?php echo (int) $m['active']; ?></strong></div>
				<div class="nlops-row"><span>נעצרו</span><strong><?php echo (int) $m['stopped']; ?></strong></div>
				<?php foreach ( (array) $m['stopped_by_reason'] as $reason => $count ) : ?>
					<div class="nlops-row"><span><?php echo esc_html( 'עצירה: ' . $reason ); ?></span><strong><?php echo (int) $count; ?></strong></div>
				<?php endforeach; ?>
			</div>
		</div>
		<?php
	}
}
add_action( 'nadlan_ops_after_grid', 'nadlan_lead_nurture_render_ops_panel', 37 );

add_action( 'admin_menu', function () {
	add_options_page( 'NadLan Lead Nurture', 'NadLan Lead Nurture', 'manage_options', 'nadlan-lead-nurture', 'nadlan_lead_nurture_settings_page' );
} );

if ( ! function_exists( 'nadlan_lead_nurture_settings_page' ) ) {
	function nadlan_lead_nurture_settings_page() {
		if ( ! current_user_can( 'manage_options' ) ) { return; }
		$defaults = nadlan_lead_nurture_default_templates();
		if ( ! empty( $_POST['nadlan_lead_nurture_save'] ) && check_admin_referer( 'nadlan_lead_nurture_save' ) ) {
			update_option( 'nadlan_feature_lead_nurture', ! empty( $_POST['nadlan_feature_lead_nurture'] ) ? '1' : '0', false );
			$monthly_max = isset( $_POST['nadlan_lead_nurture_monthly_max'] ) ? absint( wp_unslash( $_POST['nadlan_lead_nurture_monthly_max'] ) ) : 6;
			update_option( 'nadlan_lead_nurture_monthly_max', max( 1, min( 24, $monthly_max ) ), false );
			$posted = isset( $_POST['nadlan_lead_nurture_templates'] ) && is_array( $_POST['nadlan_lead_nurture_templates'] ) ? wp_unslash( $_POST['nadlan_lead_nurture_templates'] ) : array();
			$saved = array();
			foreach ( $defaults as $tier => $steps ) {
				foreach ( $steps as $step => $template ) {
					$subject = isset( $posted[ $tier ][ $step ]['subject'] ) ? sanitize_text_field( (string) $posted[ $tier ][ $step ]['subject'] ) : (string) $template['subject'];
					$body = isset( $posted[ $tier ][ $step ]['body'] ) ? sanitize_textarea_field( (string) $posted[ $tier ][ $step ]['body'] ) : (string) $template['body'];
					$saved[ $tier ][ $step ] = array( 'subject' => $subject, 'body' => $body );
				}
			}
			update_option( 'nadlan_lead_nurture_templates', $saved, false );
			echo '<div class="notice notice-success"><p>נשמר.</p></div>';
		}
		$enabled = get_option( 'nadlan_feature_lead_nurture', '0' ) === '1';
		$monthly_max = max( 1, min( 24, (int) get_option( 'nadlan_lead_nurture_monthly_max', 6 ) ) );
		$templates = nadlan_lead_nurture_templates();
		?>
		<div class="wrap" dir="rtl">
			<h1>NadLan Lead Nurture</h1>
			<form method="post">
				<?php wp_nonce_field( 'nadlan_lead_nurture_save' ); ?>
				<table class="form-table" role="presentation">
					<tr>
						<th scope="row">הפעלת רצף המשך</th>
						<td><label><input type="checkbox" name="nadlan_feature_lead_nurture" value="1" <?php checked( $enabled ); ?>> פעיל</label><p class="description">כבוי כברירת מחדל. כשהוא כבוי, לא מתוזמנות הודעות המשך חדשות.</p></td>
					</tr>
					<tr>
						<th scope="row">מספר הודעות חודשיות מקסימלי</th>
						<td><input type="number" min="1" max="24" name="nadlan_lead_nurture_monthly_max" value="<?php echo esc_attr( $monthly_max ); ?>"></td>
					</tr>
				</table>
				<h2>תבניות לפי חום הפנייה ושלב</h2>
				<p class="description">אפשר להשתמש ב-{{name}}, {{card}}, {{site}}, {{url}}, {{unsubscribe}}. קישור הסרה מתווסף אוטומטית גם אם הוסר מהתבנית.</p>
				<?php foreach ( $templates as $tier => $steps ) : ?>
					<h3><?php echo esc_html( strtoupper( $tier ) ); ?></h3>
					<?php foreach ( $steps as $step => $template ) : ?>
						<h4><?php echo esc_html( $step ); ?></h4>
						<p><input type="text" class="large-text" name="nadlan_lead_nurture_templates[<?php echo esc_attr( $tier ); ?>][<?php echo esc_attr( $step ); ?>][subject]" value="<?php echo esc_attr( $template['subject'] ); ?>"></p>
						<p><textarea class="large-text code" rows="5" name="nadlan_lead_nurture_templates[<?php echo esc_attr( $tier ); ?>][<?php echo esc_attr( $step ); ?>][body]"><?php echo esc_textarea( $template['body'] ); ?></textarea></p>
					<?php endforeach; ?>
				<?php endforeach; ?>
				<p class="submit"><button type="submit" name="nadlan_lead_nurture_save" value="1" class="button button-primary">שמור</button></p>
			</form>
		</div>
		<?php
	}
}
