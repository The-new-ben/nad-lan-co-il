<?php
/**
 * nadlan-config - the smart daily email to the owner (HAD-260, 7.10.2026).
 *
 * Ben: "I get emails about leads every day, the same thing for months, it has to be smarter."
 * Until now two mails left every morning: "תזכורת יומית: 15 לידים ממתינים" (alerts.php,
 * nadlan_leads_daily: the same list every day, 13 of them system tests) and "סיכום יומי"
 * (lead-inbox.php, nadlan_inbox_daily_digest: five counters, sent even when everything is 0).
 *
 * This module replaces both with ONE mail at 08:00 site time:
 *   - the subject carries the numbers ("נדלן · 7.10 · 2 לידים חדשים · 1 החלטה מחכה לך");
 *   - new real leads of the last 24 hours: name, phone (call + WhatsApp links), source page, the question,
 *     a signed "סמן טופל" link;
 *   - a comparison with yesterday and with the same day last week;
 *   - "מחכה להחלטה שלך": every waiting item is listed ONCE (a real lead unhandled for 24h, a card claim,
 *     a review, an open referral, a listing waiting for approval, a failed payment). Later days show only
 *     a count of what is still open, so the mail never repeats the same list;
 *   - "תקלות": mails that failed (wp_mail returned false / wp_mail_failed), yesterday's digest that did not
 *     go out, failure events from the event log, a lead whose confirmation to the customer failed;
 *   - one link to the Lead Inbox.
 * System-test leads (names like בדיקה/test/QA/E2E, example/test mail domains, phones like 050000000X, or a
 * test meta flag) are filtered from the DISPLAY only. No lead is changed or deleted by this code.
 * When there is nothing new and nothing waiting, no mail is sent (flag nadlan_feature_smart_digest_quiet_send
 * sends one line "אין חדש, הכול שקט" instead).
 *
 * Switches (Settings > NadLan Features, no code needed):
 *   nadlan_feature_smart_digest          the new mail (default ON)
 *   nadlan_feature_legacy_daily_emails   the two old mails (default OFF; turn on to bring them back)
 *   nadlan_feature_smart_digest_quiet_send  send "אין חדש" on quiet days (default OFF)
 * Filters: nadlan_smart_digest_recipients (default: admin_email), nadlan_smart_digest_is_test,
 *          nadlan_smart_digest_click_counts, nadlan_smart_digest_data, nadlan_smart_digest_rereport_days.
 * The mail plugins and the sending settings are NOT touched here (Ben's decision).
 */

if ( ! defined( 'ABSPATH' ) ) { exit; }

/* ---------------------------------------------------------------------------------------------
 * Switches
 * ------------------------------------------------------------------------------------------- */

if ( ! function_exists( 'nadlan_smart_digest_on' ) ) {
	function nadlan_smart_digest_on() {
		return (bool) apply_filters( 'nadlan_smart_digest_enabled', '1' === (string) get_option( 'nadlan_feature_smart_digest', '1' ) );
	}
}

if ( ! function_exists( 'nadlan_smart_digest_legacy_on' ) ) {
	/** The two old daily mails (alerts.php nadlan_leads_daily, lead-inbox.php nadlan_inbox_daily_digest). */
	function nadlan_smart_digest_legacy_on() {
		return (bool) apply_filters( 'nadlan_legacy_daily_emails_enabled', '1' === (string) get_option( 'nadlan_feature_legacy_daily_emails', '0' ) );
	}
}

if ( ! function_exists( 'nadlan_smart_digest_quiet_send_on' ) ) {
	function nadlan_smart_digest_quiet_send_on() {
		return (bool) apply_filters( 'nadlan_smart_digest_send_when_quiet', '1' === (string) get_option( 'nadlan_feature_smart_digest_quiet_send', '0' ) );
	}
}

/* The new mail is ON by default, so its switch must exist as '1' for the features page to show it checked.
 * add_option() writes only when the option is missing; a saved '0' from the features page is kept. */
add_action( 'init', function () {
	if ( false === get_option( 'nadlan_feature_smart_digest', false ) ) {
		add_option( 'nadlan_feature_smart_digest', '1', '', false );
	}
}, 5 );

/* ---------------------------------------------------------------------------------------------
 * Pure helpers (no database): test-lead detection, phone links, subject, quiet check, HTML.
 * Covered by scripts/had-260/test_smart_digest.php.
 * ------------------------------------------------------------------------------------------- */

if ( ! function_exists( 'nadlan_sd_norm_phone' ) ) {
	/** Digits only, +972/972 folded to a leading 0. */
	function nadlan_sd_norm_phone( $phone ) {
		$d = preg_replace( '/\D+/', '', (string) $phone );
		if ( 0 === strpos( $d, '972' ) && strlen( $d ) >= 11 ) {
			$d = '0' . substr( $d, 3 );
		}
		return $d;
	}
}

if ( ! function_exists( 'nadlan_sd_is_test_lead' ) ) {
	/**
	 * Is this a system test? $lead: name, email, phone, title, flags (array of meta values that mark a test).
	 * Display filter only. Errs on the side of showing a lead: a real name that merely contains "test"
	 * inside a word (e.g. "Testa") is NOT a test.
	 */
	function nadlan_sd_is_test_lead( array $lead ) {
		foreach ( (array) ( $lead['flags'] ?? array() ) as $flag ) {
			if ( ! empty( $flag ) && ! in_array( strtolower( (string) $flag ), array( '0', 'no', 'false' ), true ) ) {
				return true;
			}
		}
		$text = ' ' . (string) ( $lead['name'] ?? '' ) . ' ' . (string) ( $lead['title'] ?? '' ) . ' ';
		// Hebrew markers: בדיקה/בדיקת/בדיקות, טסט, סינתטי, דמה, ניסיון מערכת.
		if ( preg_match( '/(בדיק|טסט|סינתטי|ליד\s*דמה|ניסיון\s*מערכת)/u', $text ) ) {
			return true;
		}
		// Latin markers as whole words: test, testing, qa, e2e, demo, dummy, codex, sandbox.
		if ( preg_match( '/(?<![a-z0-9])(test|tests|testing|qa|e2e|demo|dummy|codex|sandbox|synthetic)(?![a-z0-9])/i', $text ) ) {
			return true;
		}
		$email = strtolower( trim( (string) ( $lead['email'] ?? '' ) ) );
		if ( '' !== $email ) {
			if ( preg_match( '/@(example\.(com|org|net|test)|[a-z0-9.-]*\.(test|invalid|example)|mailinator\.com|test\.[a-z.]+)$/', $email ) ) {
				return true;
			}
			if ( preg_match( '/^(test|qa|e2e|demo|dummy|codex|noreply)([._+-][^@]*)?@/', $email ) || preg_match( '/\+(test|qa|e2e)[^@]*@/', $email ) ) {
				return true;
			}
		}
		$p = nadlan_sd_norm_phone( $lead['phone'] ?? '' );
		if ( '' !== $p ) {
			if ( preg_match( '/^05\d0{6}\d$/', $p ) ) { return true; }       // 050000000X, 052000000X ...
			if ( preg_match( '/^(\d)\1{6,}$/', $p ) ) { return true; }        // 0000000000, 1111111
			if ( false !== strpos( $p, '1234567' ) ) { return true; }         // 0501234567 and kin
		}
		return false;
	}
}

if ( ! function_exists( 'nadlan_sd_phone_links' ) ) {
	/** array( 'tel' => 'tel:+97250...', 'wa' => 'https://wa.me/97250...' ) or empty strings. */
	function nadlan_sd_phone_links( $phone ) {
		$p = nadlan_sd_norm_phone( $phone );
		if ( strlen( $p ) < 9 ) {
			return array( 'tel' => '', 'wa' => '' );
		}
		$intl = '972' . ltrim( $p, '0' );
		return array( 'tel' => 'tel:+' . $intl, 'wa' => 'https://wa.me/' . $intl );
	}
}

if ( ! function_exists( 'nadlan_sd_count_phrase' ) ) {
	/** Hebrew count phrases: 0 / 1 / many. */
	function nadlan_sd_count_phrase( $n, $kind ) {
		$n = (int) $n;
		switch ( $kind ) {
			case 'leads':
				if ( 0 === $n ) { return 'אין לידים חדשים'; }
				return 1 === $n ? 'ליד חדש אחד' : $n . ' לידים חדשים';
			case 'decisions':
				return 1 === $n ? 'החלטה אחת מחכה לך' : $n . ' החלטות מחכות לך';
			case 'issues':
				return 1 === $n ? 'תקלה אחת' : $n . ' תקלות';
		}
		return (string) $n;
	}
}

if ( ! function_exists( 'nadlan_sd_is_quiet' ) ) {
	/** Quiet = no new real lead, no decision listed for the first time, no issue. */
	function nadlan_sd_is_quiet( array $data ) {
		return empty( $data['leads'] ) && empty( $data['decisions'] ) && empty( $data['issues'] );
	}
}

if ( ! function_exists( 'nadlan_sd_subject' ) ) {
	/** "נדלן · 7.10 · 2 לידים חדשים · 1 החלטה מחכה לך" - the numbers in the subject, so the mail need not be opened. */
	function nadlan_sd_subject( array $data ) {
		$parts = array( 'נדלן', (string) ( $data['date_label'] ?? '' ) );
		if ( nadlan_sd_is_quiet( $data ) ) {
			$parts[] = 'אין חדש, הכול שקט';
			return implode( ' · ', array_filter( $parts, 'strlen' ) );
		}
		$parts[] = nadlan_sd_count_phrase( count( (array) ( $data['leads'] ?? array() ) ), 'leads' );
		$d = count( (array) ( $data['decisions'] ?? array() ) );
		if ( $d > 0 ) { $parts[] = nadlan_sd_count_phrase( $d, 'decisions' ); }
		$i = count( (array) ( $data['issues'] ?? array() ) );
		if ( $i > 0 ) { $parts[] = nadlan_sd_count_phrase( $i, 'issues' ); }
		return implode( ' · ', array_filter( $parts, 'strlen' ) );
	}
}

if ( ! function_exists( 'nadlan_sd_delta' ) ) {
	/** "3 (אתמול 1, לפני שבוע 0)" with an arrow when it moved against yesterday. */
	function nadlan_sd_delta( array $triple ) {
		$t = (int) ( $triple[0] ?? 0 );
		$y = (int) ( $triple[1] ?? 0 );
		$w = (int) ( $triple[2] ?? 0 );
		$arrow = $t > $y ? ' ▲' : ( $t < $y ? ' ▼' : '' );
		return array( 'today' => $t, 'yesterday' => $y, 'week' => $w, 'arrow' => $arrow );
	}
}

if ( ! function_exists( 'nadlan_sd_render_html' ) ) {
	/** The mail body. Inline styles only (mail clients), RTL, plain Hebrew. */
	function nadlan_sd_render_html( array $data ) {
		$e   = function ( $s ) { return esc_html( (string) $s ); };
		$u   = function ( $s ) { return esc_url( (string) $s ); };
		$btn = 'display:inline-block;padding:6px 12px;border-radius:8px;text-decoration:none;font-size:13px;font-weight:600;margin:2px 0 2px 6px;';
		$h2  = 'font-size:16px;margin:24px 0 8px;color:#1B1A17;';
		$box = 'background:#FFFFFF;border:1px solid #E7E1D6;border-radius:12px;padding:12px 14px;margin:0 0 10px;';
		$muted = 'color:#6B655B;font-size:13px;';

		$o  = '<div dir="rtl" lang="he" style="font-family:Arial,Helvetica,sans-serif;background:#FAF7F1;padding:16px;color:#1B1A17;line-height:1.55;">';
		$o .= '<div style="max-width:620px;margin:0 auto;">';
		$o .= '<h1 style="font-size:20px;margin:0 0 4px;">' . $e( nadlan_sd_subject( $data ) ) . '</h1>';
		$o .= '<p style="' . $muted . 'margin:0 0 12px;">' . $e( (string) ( $data['window_label'] ?? 'ב-24 השעות האחרונות' ) ) . '</p>';

		$quiet = nadlan_sd_is_quiet( $data );
		if ( $quiet ) {
			$o .= '<div style="' . $box . '"><b>אין חדש, הכול שקט.</b> אין לידים חדשים, אין החלטה חדשה שמחכה לך ואין תקלות.</div>';
		}

		/* 1. new leads */
		$leads = (array) ( $data['leads'] ?? array() );
		if ( ! $quiet ) {
			$o .= '<h2 style="' . $h2 . '">לידים חדשים</h2>';
		}
		if ( ! $leads && ! $quiet ) {
			$o .= '<p style="' . $muted . '">לא נכנס ליד אמיתי חדש.</p>';
		}
		foreach ( $leads as $l ) {
			$links = nadlan_sd_phone_links( $l['phone'] ?? '' );
			$o .= '<div style="' . $box . '">';
			$o .= '<div style="font-size:16px;font-weight:700;">' . $e( $l['name'] ?: 'ללא שם' ) . '</div>';
			if ( ! empty( $l['phone'] ) ) {
				$o .= '<div dir="ltr" style="text-align:right;font-size:15px;margin:2px 0;">' . $e( $l['phone'] ) . '</div>';
			}
			if ( ! empty( $l['email'] ) ) {
				$o .= '<div dir="ltr" style="text-align:right;' . $muted . '">' . $e( $l['email'] ) . '</div>';
			}
			if ( ! empty( $l['page_title'] ) || ! empty( $l['page_url'] ) ) {
				$o .= '<div style="margin-top:4px;">מאיזה עמוד: ' . ( ! empty( $l['page_url'] )
					? '<a href="' . $u( $l['page_url'] ) . '" style="color:#1F4FB8;">' . $e( $l['page_title'] ?: $l['page_url'] ) . '</a>'
					: $e( $l['page_title'] ) ) . '</div>';
			}
			if ( ! empty( $l['question'] ) ) {
				$o .= '<div style="margin-top:4px;">מה שאל: ' . $e( $l['question'] ) . '</div>';
			}
			if ( ! empty( $l['ack_failed'] ) ) {
				$o .= '<div style="margin-top:4px;color:#A33;">מייל האישור ללקוח לא נשלח. כדאי להתקשר.</div>';
			}
			$o .= '<div style="margin-top:8px;">';
			if ( $links['tel'] ) { $o .= '<a href="' . $u( $links['tel'] ) . '" style="' . $btn . 'background:#1B1A17;color:#FFF;">חיוג</a>'; }
			if ( $links['wa'] )  { $o .= '<a href="' . $u( $links['wa'] ) . '" style="' . $btn . 'background:#1F8F4E;color:#FFF;">וואטסאפ</a>'; }
			if ( ! empty( $l['handled_url'] ) ) { $o .= '<a href="' . $u( $l['handled_url'] ) . '" style="' . $btn . 'background:#EFE9DD;color:#1B1A17;">סמן טופל</a>'; }
			if ( ! empty( $l['edit_url'] ) ) { $o .= '<a href="' . $u( $l['edit_url'] ) . '" style="' . $btn . 'color:#1F4FB8;">פרטים</a>'; }
			$o .= '</div></div>';
		}
		if ( ! empty( $data['test_hidden'] ) ) {
			$o .= '<p style="' . $muted . '">' . (int) $data['test_hidden'] . ' פניות בדיקה של המערכת הוסתרו מהרשימה.</p>';
		}

		/* 2. change vs yesterday and vs the same day last week */
		$rows = $quiet ? array() : (array) ( $data['compare'] ?? array() );
		if ( $rows ) {
			$o .= '<h2 style="' . $h2 . '">מה השתנה</h2>';
			$o .= '<table role="presentation" style="width:100%;border-collapse:collapse;background:#FFF;border:1px solid #E7E1D6;border-radius:12px;font-size:14px;">';
			$o .= '<tr style="background:#F3EEE4;"><th style="text-align:right;padding:8px;">&nbsp;</th><th style="padding:8px;">היום</th><th style="padding:8px;">אתמול</th><th style="padding:8px;">לפני שבוע</th></tr>';
			foreach ( $rows as $row ) {
				$d = nadlan_sd_delta( (array) ( $row['values'] ?? array() ) );
				$o .= '<tr><td style="padding:8px;border-top:1px solid #EEE;">' . $e( $row['label'] ?? '' ) . '</td>'
					. '<td style="padding:8px;border-top:1px solid #EEE;text-align:center;font-weight:700;">' . (int) $d['today'] . $e( $d['arrow'] ) . '</td>'
					. '<td style="padding:8px;border-top:1px solid #EEE;text-align:center;">' . (int) $d['yesterday'] . '</td>'
					. '<td style="padding:8px;border-top:1px solid #EEE;text-align:center;">' . (int) $d['week'] . '</td></tr>';
			}
			$o .= '</table>';
			if ( ! empty( $data['compare_note'] ) ) {
				$o .= '<p style="' . $muted . 'margin-top:6px;">' . $e( $data['compare_note'] ) . '</p>';
			}
		}

		/* 3. waiting for your decision (each item once) */
		$decisions = (array) ( $data['decisions'] ?? array() );
		$still     = (array) ( $data['still_open'] ?? array() );
		if ( $decisions || array_sum( array_map( 'intval', $still ) ) > 0 ) {
			$o .= '<h2 style="' . $h2 . '">מחכה להחלטה שלך</h2>';
			foreach ( $decisions as $d ) {
				$o .= '<div style="' . $box . '"><div>' . $e( $d['text'] ?? '' ) . '</div>';
				if ( ! empty( $d['detail'] ) ) { $o .= '<div style="' . $muted . '">' . $e( $d['detail'] ) . '</div>'; }
				if ( ! empty( $d['url'] ) ) {
					$o .= '<div style="margin-top:6px;"><a href="' . $u( $d['url'] ) . '" style="' . $btn . 'background:#1B1A17;color:#FFF;">' . $e( $d['cta'] ?? 'פתיחה' ) . '</a></div>';
				}
				$o .= '</div>';
			}
			$labels = array(
				'lead'     => 'לידים שעדיין לא טופלו',
				'claim'    => 'בקשות בעלות',
				'review'   => 'חוות דעת לאישור',
				'referral' => 'הפניות פתוחות',
				'listing'  => 'מודעות שמחכות לאישור',
				'payment'  => 'תשלומים שנכשלו',
			);
			$bits = array();
			foreach ( $still as $k => $n ) {
				if ( (int) $n > 0 ) { $bits[] = ( $labels[ $k ] ?? $k ) . ': ' . (int) $n; }
			}
			if ( $bits ) {
				$o .= '<p style="' . $muted . '">עדיין פתוח ממה שכבר דיווחתי (לא חוזר על הרשימה): ' . $e( implode( ' · ', $bits ) ) . '.</p>';
			}
		}

		/* 4. issues */
		$issues = (array) ( $data['issues'] ?? array() );
		if ( $issues ) {
			$o .= '<h2 style="' . $h2 . 'color:#A33;">תקלות</h2>';
			foreach ( $issues as $i ) {
				$o .= '<div style="' . $box . 'border-color:#E9C9C9;"><div>' . $e( $i['text'] ?? '' ) . '</div>';
				if ( ! empty( $i['detail'] ) ) { $o .= '<div style="' . $muted . '">' . $e( $i['detail'] ) . '</div>'; }
				$o .= '</div>';
			}
		}

		/* 5. the inbox */
		$o .= '<p style="margin-top:24px;"><a href="' . $u( $data['inbox_url'] ?? '' ) . '" style="' . $btn . 'background:#EFE9DD;color:#1B1A17;">לכל הפניות ב-Lead Inbox</a></p>';
		$o .= '<p style="' . $muted . 'margin-top:16px;">מייל אחד ביום, ב-08:00. פריט שמחכה להחלטה מופיע פעם אחת. כיבוי או החזרת המיילים הישנים: הגדרות > NadLan Features.</p>';
		$o .= '</div></div>';
		return $o;
	}
}

/* ---------------------------------------------------------------------------------------------
 * The log: when the digest went out, whether wp_mail returned false, and mail failures in general.
 * Stored in two small non-autoloaded options (ring buffers). Nothing about recipients is stored.
 * ------------------------------------------------------------------------------------------- */

if ( ! function_exists( 'nadlan_sd_log_push' ) ) {
	function nadlan_sd_log_push( $option, array $row, $limit = 30 ) {
		$log = get_option( $option, array() );
		if ( ! is_array( $log ) ) { $log = array(); }
		$log[] = $row;
		if ( count( $log ) > $limit ) { $log = array_slice( $log, -1 * $limit ); }
		update_option( $option, $log, false );
	}
}

/* Any mail on the site that fails (wp_mail_failed) is remembered for tomorrow's "תקלות". Subject + error only. */
add_action( 'wp_mail_failed', function ( $error ) {
	if ( ! is_wp_error( $error ) ) { return; }
	$data = (array) $error->get_error_data();
	nadlan_sd_log_push( 'nadlan_smart_digest_mail_failures', array(
		'ts'      => time(),
		'subject' => mb_substr( sanitize_text_field( (string) ( $data['subject'] ?? '' ) ), 0, 120 ),
		'error'   => mb_substr( sanitize_text_field( (string) $error->get_error_message() ), 0, 160 ),
	), 50 );
} );

/* A failed subscription payment (greeninvoice-recurring.php) waits for a decision. */
add_action( 'nadlan_subscription_payment_failed', function ( $card_id = 0, $tier = '' ) {
	nadlan_sd_log_push( 'nadlan_smart_digest_payment_failures', array(
		'ts'      => time(),
		'card_id' => (int) $card_id,
		'tier'    => sanitize_text_field( (string) $tier ),
	), 50 );
}, 20, 2 );

/* ---------------------------------------------------------------------------------------------
 * "סמן טופל": a signed link (HMAC with the site salt), for a logged-in editor only.
 * It changes ONE lead, and only when Ben presses it: lead_status new -> contacted, with the audit entry.
 * ------------------------------------------------------------------------------------------- */

if ( ! function_exists( 'nadlan_sd_handled_sig' ) ) {
	function nadlan_sd_handled_sig( $lead_id ) {
		return substr( hash_hmac( 'sha256', 'nadlan_sd_handled|' . (int) $lead_id, wp_salt( 'auth' ) ), 0, 24 );
	}
}

if ( ! function_exists( 'nadlan_sd_handled_url' ) ) {
	function nadlan_sd_handled_url( $lead_id ) {
		return add_query_arg( array(
			'action' => 'nadlan_sd_handled',
			'lead'   => (int) $lead_id,
			'sig'    => nadlan_sd_handled_sig( $lead_id ),
		), admin_url( 'admin-post.php' ) );
	}
}

add_action( 'admin_post_nopriv_nadlan_sd_handled', function () {
	$back = add_query_arg( array(
		'action' => 'nadlan_sd_handled',
		'lead'   => isset( $_GET['lead'] ) ? absint( $_GET['lead'] ) : 0,
		'sig'    => isset( $_GET['sig'] ) ? sanitize_key( wp_unslash( $_GET['sig'] ) ) : '',
	), admin_url( 'admin-post.php' ) );
	wp_safe_redirect( wp_login_url( $back ) );
	exit;
} );

add_action( 'admin_post_nadlan_sd_handled', function () {
	$lead_id = isset( $_GET['lead'] ) ? absint( $_GET['lead'] ) : 0;
	$sig     = isset( $_GET['sig'] ) ? sanitize_key( wp_unslash( $_GET['sig'] ) ) : '';
	$lead    = $lead_id ? get_post( $lead_id ) : null;
	if ( ! $lead || 'nadlan_lead' !== $lead->post_type || ! hash_equals( nadlan_sd_handled_sig( $lead_id ), $sig ) ) {
		wp_die( 'הקישור לא תקין.', 'נדלן', array( 'response' => 403 ) );
	}
	if ( ! current_user_can( 'edit_posts' ) ) {
		wp_die( 'אין הרשאה.', 'נדלן', array( 'response' => 403 ) );
	}
	$old = sanitize_key( (string) get_post_meta( $lead_id, 'lead_status', true ) );
	if ( '' === $old ) { $old = 'new'; }
	if ( 'new' === $old ) {
		update_post_meta( $lead_id, 'lead_status', 'contacted' );
		if ( (int) get_post_meta( $lead_id, 'lead_first_response_at', true ) <= 0 ) {
			update_post_meta( $lead_id, 'lead_first_response_at', time() );
			update_post_meta( $lead_id, 'lead_first_response_user_id', get_current_user_id() );
		}
		if ( function_exists( 'nadlan_lead_e2e_audit' ) ) {
			nadlan_lead_e2e_audit( array(
				'lead_id' => $lead_id,
				'card_id' => (int) get_post_meta( $lead_id, 'lead_card_id', true ),
				'user_id' => get_current_user_id(),
				'old'     => $old,
				'new'     => 'contacted',
				'note'    => 'smart digest: marked handled',
			) );
		}
	}
	wp_safe_redirect( add_query_arg( 'nadlan_sd_done', 1, admin_url( 'post.php?post=' . $lead_id . '&action=edit' ) ) );
	exit;
} );

add_action( 'admin_notices', function () {
	if ( empty( $_GET['nadlan_sd_done'] ) ) { return; }
	echo '<div class="notice notice-success is-dismissible" style="direction:rtl"><p>הליד סומן כטופל (נוצר קשר).</p></div>';
} );

/* ---------------------------------------------------------------------------------------------
 * Collecting the data (WordPress).
 * ------------------------------------------------------------------------------------------- */

if ( ! function_exists( 'nadlan_sd_lead_row' ) ) {
	/** One nadlan_lead post as the plain array the pure helpers expect. */
	function nadlan_sd_lead_row( $post ) {
		$id = (int) $post->ID;
		$m  = function ( $k ) use ( $id ) { return (string) get_post_meta( $id, $k, true ); };
		$card_id = (int) $m( 'project_wp_id' );
		if ( ! $card_id ) { $card_id = (int) $m( 'lead_card_id' ); }
		$page_title = '';
		$page_url   = '';
		if ( $card_id > 0 && get_post( $card_id ) ) {
			$page_title = get_the_title( $card_id );
			$page_url   = get_permalink( $card_id );
		} elseif ( '' !== $m( 'source_url' ) ) {
			$page_url   = $m( 'source_url' );
			$page_title = $m( 'project_title' ) !== '' ? $m( 'project_title' ) : urldecode( (string) wp_parse_url( $page_url, PHP_URL_PATH ) );
		} else {
			$page_title = $m( 'project_title' ) !== '' ? $m( 'project_title' ) : ( $m( 'utm_source' ) !== '' ? 'מקור: ' . $m( 'utm_source' ) : '' );
		}
		$question = trim( wp_strip_all_tags( (string) $post->post_content ) );
		if ( '' === $question ) { $question = $m( 'message' ); }
		$extra = array_filter( array( $m( 'goal' ), $m( 'unit' ) !== '' ? 'דירה ' . $m( 'unit' ) : '', $m( 'rooms' ) !== '' ? $m( 'rooms' ) . ' חדרים' : '', $m( 'budget' ) !== '' ? 'תקציב ' . $m( 'budget' ) : '' ) );
		if ( $extra ) { $question = trim( $question . ( '' !== $question ? ' · ' : '' ) . implode( ' · ', $extra ) ); }
		$status = sanitize_key( $m( 'lead_status' ) );
		return array(
			'id'          => $id,
			'created'     => (int) get_post_time( 'U', true, $post ),
			'name'        => $m( 'name' ),
			'phone'       => $m( 'phone' ),
			'email'       => $m( 'email' ),
			'title'       => (string) $post->post_title,
			'flags'       => array( $m( 'is_test' ), $m( 'lead_is_test' ), $m( '_nadlan_test' ), $m( 'lead_test' ) ),
			'status'      => '' === $status ? 'new' : $status,
			'page_title'  => (string) $page_title,
			'page_url'    => (string) $page_url,
			'question'    => mb_substr( $question, 0, 240 ),
			'ack_failed'  => 'failed' === $m( 'lead_ack_status' ),
			'handled_url' => nadlan_sd_handled_url( $id ),
			'edit_url'    => admin_url( 'post.php?post=' . $id . '&action=edit' ),
		);
	}
}

if ( ! function_exists( 'nadlan_sd_is_test_row' ) ) {
	function nadlan_sd_is_test_row( array $row ) {
		return (bool) apply_filters( 'nadlan_smart_digest_is_test', nadlan_sd_is_test_lead( $row ), $row );
	}
}

if ( ! function_exists( 'nadlan_sd_posts_between' ) ) {
	/** Posts of $type created between $from and $to (GMT timestamps). */
	function nadlan_sd_posts_between( $type, $from, $to, $statuses = 'any' ) {
		return get_posts( array(
			'post_type'        => $type,
			'post_status'      => $statuses,
			'numberposts'      => 300,
			'suppress_filters' => true,
			'date_query'       => array( array(
				'column'    => 'post_date_gmt',
				'after'     => gmdate( 'Y-m-d H:i:s', (int) $from ),
				'before'    => gmdate( 'Y-m-d H:i:s', (int) $to ),
				'inclusive' => false,
			) ),
		) );
	}
}

if ( ! function_exists( 'nadlan_sd_real_leads_between' ) ) {
	function nadlan_sd_real_leads_between( $from, $to, &$tests = 0 ) {
		$out = array();
		foreach ( nadlan_sd_posts_between( 'nadlan_lead', $from, $to ) as $p ) {
			$row = nadlan_sd_lead_row( $p );
			if ( nadlan_sd_is_test_row( $row ) ) { $tests++; continue; }
			$out[] = $row;
		}
		return $out;
	}
}

if ( ! function_exists( 'nadlan_sd_collect' ) ) {
	/**
	 * Everything the mail shows. $dry = true does not mark items as reported (preview).
	 * Decision items are keyed (type:id). An item is listed the first time it is seen; afterwards it only
	 * counts in "still open", unless nadlan_smart_digest_rereport_days (default 0 = never) has passed.
	 */
	function nadlan_sd_collect( $now = 0, $dry = false ) {
		global $wpdb;
		$now   = $now ? (int) $now : time();
		$day   = DAY_IN_SECONDS;
		$tests = 0;
		$data  = array(
			'now'          => $now,
			'date_label'   => wp_date( 'j.n', $now ),
			'window_label' => 'מ-' . wp_date( 'j.n H:i', $now - $day ) . ' עד ' . wp_date( 'j.n H:i', $now ),
			'inbox_url'    => admin_url( 'admin.php?page=nadlan-inbox' ),
			'leads'        => array(),
			'test_hidden'  => 0,
			'compare'      => array(),
			'compare_note' => '',
			'decisions'    => array(),
			'still_open'   => array(),
			'issues'       => array(),
		);

		/* 1. new real leads, last 24 hours */
		$data['leads']       = nadlan_sd_real_leads_between( $now - $day, $now, $tests );
		$data['test_hidden'] = $tests;

		/* 2. comparison: today / yesterday / same day last week */
		$ignore = 0;
		$leads_y = count( nadlan_sd_real_leads_between( $now - 2 * $day, $now - $day, $ignore ) );
		$leads_w = count( nadlan_sd_real_leads_between( $now - 8 * $day, $now - 7 * $day, $ignore ) );
		$data['compare'][] = array( 'label' => 'לידים אמיתיים', 'values' => array( count( $data['leads'] ), $leads_y, $leads_w ) );
		$listing = function ( $from, $to ) {
			return count( nadlan_sd_posts_between( 'nadlan_property', $from, $to, array( 'publish', 'pending', 'private' ) ) );
		};
		$data['compare'][] = array( 'label' => 'מודעות חדשות', 'values' => array( $listing( $now - $day, $now ), $listing( $now - 2 * $day, $now - $day ), $listing( $now - 8 * $day, $now - 7 * $day ) ) );
		/* WhatsApp / call clicks are measured only in GA4 today (conversion-cta.php, cta-sheet.php send
		 * whatsapp_click to GA4; nothing is stored on the site). A future counter can feed this filter:
		 * array( 'wa' => array( today, yesterday, week ), 'call' => array( ... ) ). */
		$clicks = apply_filters( 'nadlan_smart_digest_click_counts', null, $now );
		if ( is_array( $clicks ) ) {
			if ( isset( $clicks['wa'] ) )   { $data['compare'][] = array( 'label' => 'לחיצות וואטסאפ', 'values' => (array) $clicks['wa'] ); }
			if ( isset( $clicks['call'] ) ) { $data['compare'][] = array( 'label' => 'לחיצות חיוג', 'values' => (array) $clicks['call'] ); }
		} else {
			$data['compare_note'] = 'לחיצות וואטסאפ וחיוג נמדדות כרגע רק ב-Google Analytics, לא באתר, ולכן לא מופיעות כאן.';
		}

		/* 3. waiting for a decision */
		$items = array();
		// a real lead still "new" for over 24 hours
		$stale = get_posts( array(
			'post_type'        => 'nadlan_lead',
			'post_status'      => 'any',
			'numberposts'      => 100,
			'suppress_filters' => true,
			'date_query'       => array( array( 'column' => 'post_date_gmt', 'before' => gmdate( 'Y-m-d H:i:s', $now - $day ) ) ),
			'meta_query'       => array( array( 'key' => 'lead_status', 'value' => 'new' ) ),
		) );
		foreach ( $stale as $p ) {
			$row = nadlan_sd_lead_row( $p );
			if ( nadlan_sd_is_test_row( $row ) ) { continue; }
			$age = max( 1, (int) floor( ( $now - $row['created'] ) / $day ) );
			$items[] = array(
				'key'    => 'lead:' . $row['id'],
				'kind'   => 'lead',
				'text'   => 'ליד שעדיין לא טופל: ' . ( $row['name'] ?: 'ללא שם' ) . ( $row['phone'] ? ' (' . $row['phone'] . ')' : '' ),
				'detail' => 'נכנס לפני ' . $age . ' ימים' . ( $row['page_title'] ? ', מתוך ' . $row['page_title'] : '' ) . '. סמן טופל, או פתח וסגור אותו.',
				'url'    => $row['handled_url'],
				'cta'    => 'סמן טופל',
			);
		}
		// card claims (the card's claim_status = pending)
		$claims = $wpdb->get_col( "SELECT post_id FROM {$wpdb->postmeta} WHERE meta_key='claim_status' AND meta_value='pending' LIMIT 50" );
		foreach ( (array) $claims as $cid ) {
			$cid = (int) $cid;
			$items[] = array(
				'key'    => 'claim:' . $cid,
				'kind'   => 'claim',
				'text'   => 'בקשת בעלות על כרטיס: ' . get_the_title( $cid ),
				'detail' => trim( (string) get_post_meta( $cid, 'claim_name', true ) . ' ' . (string) get_post_meta( $cid, 'claim_phone', true ) ),
				'url'    => admin_url( 'edit.php?post_type=nadlan_claim' ),
				'cta'    => 'לאשר או לדחות',
			);
		}
		// reviews waiting for moderation
		foreach ( get_posts( array( 'post_type' => 'nadlan_review', 'post_status' => 'pending', 'numberposts' => 50, 'suppress_filters' => true ) ) as $p ) {
			$items[] = array(
				'key'  => 'review:' . $p->ID,
				'kind' => 'review',
				'text' => 'חוות דעת לאישור: ' . $p->post_title,
				'url'  => admin_url( 'post.php?post=' . (int) $p->ID . '&action=edit' ),
				'cta'  => 'לאשר או לדחות',
			);
		}
		// open referrals (Lead Ledger)
		foreach ( get_posts( array(
			'post_type'        => 'nadlan_referral',
			'post_status'      => 'any',
			'numberposts'      => 50,
			'suppress_filters' => true,
			'meta_query'       => array( array( 'key' => 'status', 'value' => array( 'new', 'routed', 'accepted', 'in_progress' ), 'compare' => 'IN' ) ),
		) ) as $p ) {
			$items[] = array(
				'key'    => 'referral:' . $p->ID,
				'kind'   => 'referral',
				'text'   => 'הפניה פתוחה: ' . $p->post_title,
				'detail' => 'מצב: ' . strtr( (string) get_post_meta( $p->ID, 'status', true ), array( 'in_progress' => 'בטיפול', 'new' => 'חדשה', 'routed' => 'הועברה', 'accepted' => 'התקבלה' ) ),
				'url'    => admin_url( 'post.php?post=' . (int) $p->ID . '&action=edit' ),
				'cta'    => 'לעדכן מצב',
			);
		}
		// listings waiting for approval
		foreach ( get_posts( array( 'post_type' => 'nadlan_property', 'post_status' => 'pending', 'numberposts' => 50, 'suppress_filters' => true ) ) as $p ) {
			$items[] = array(
				'key'  => 'listing:' . $p->ID,
				'kind' => 'listing',
				'text' => 'מודעה מחכה לאישור: ' . $p->post_title,
				'url'  => admin_url( 'post.php?post=' . (int) $p->ID . '&action=edit' ),
				'cta'  => 'לאשר או לדחות',
			);
		}
		// failed payments in the last 24 hours (logged by the hook above) and failed Woo orders
		foreach ( (array) get_option( 'nadlan_smart_digest_payment_failures', array() ) as $f ) {
			if ( (int) ( $f['ts'] ?? 0 ) < $now - $day ) { continue; }
			$items[] = array(
				'key'  => 'payment:' . (int) $f['ts'] . ':' . (int) ( $f['card_id'] ?? 0 ),
				'kind' => 'payment',
				'text' => 'תשלום מנוי נכשל: ' . ( ! empty( $f['card_id'] ) ? get_the_title( (int) $f['card_id'] ) : 'כרטיס לא ידוע' ) . ( ! empty( $f['tier'] ) ? ' (' . $f['tier'] . ')' : '' ),
				'url'  => ! empty( $f['card_id'] ) ? admin_url( 'post.php?post=' . (int) $f['card_id'] . '&action=edit' ) : '',
				'cta'  => 'לבדוק',
			);
		}
		if ( function_exists( 'wc_get_orders' ) ) {
			foreach ( (array) wc_get_orders( array( 'status' => array( 'failed' ), 'date_created' => '>' . ( $now - $day ), 'limit' => 20 ) ) as $o ) {
				$items[] = array(
					'key'  => 'payment:wc' . (int) $o->get_id(),
					'kind' => 'payment',
					'text' => 'הזמנה שהתשלום שלה נכשל: #' . (int) $o->get_id(),
					'url'  => admin_url( 'post.php?post=' . (int) $o->get_id() . '&action=edit' ),
					'cta'  => 'לבדוק',
				);
			}
		}

		$seen     = get_option( 'nadlan_smart_digest_seen', array() );
		if ( ! is_array( $seen ) ) { $seen = array(); }
		$rereport = max( 0, (int) apply_filters( 'nadlan_smart_digest_rereport_days', 0 ) ) * $day;
		$open_keys = array();
		foreach ( $items as $it ) {
			$open_keys[ $it['key'] ] = true;
			$last = (int) ( $seen[ $it['key'] ] ?? 0 );
			if ( $last <= 0 || ( $rereport > 0 && $now - $last >= $rereport ) ) {
				$data['decisions'][] = $it;
				$seen[ $it['key'] ] = $now;
			} else {
				$data['still_open'][ $it['kind'] ] = (int) ( $data['still_open'][ $it['kind'] ] ?? 0 ) + 1;
			}
		}
		if ( ! $dry ) {
			// forget what is closed, so it is reported again if it ever reopens
			update_option( 'nadlan_smart_digest_seen', array_intersect_key( $seen, $open_keys ), false );
		}

		/* 4. issues */
		$log  = (array) get_option( 'nadlan_smart_digest_log', array() );
		$last = $log ? end( $log ) : null;
		if ( is_array( $last ) && empty( $last['ok'] ) && (int) ( $last['ts'] ?? 0 ) >= $now - 2 * $day ) {
			$data['issues'][] = array( 'text' => 'המייל היומי של ' . wp_date( 'j.n', (int) $last['ts'] ) . ' לא נשלח (wp_mail החזיר false).', 'detail' => (string) ( $last['error'] ?? '' ) );
		} elseif ( is_array( $last ) && (int) ( $last['ts'] ?? 0 ) < $now - 30 * HOUR_IN_SECONDS ) {
			$data['issues'][] = array( 'text' => 'המייל היומי לא רץ מאז ' . wp_date( 'j.n H:i', (int) $last['ts'] ) . '. ייתכן שה-cron של האתר לא רץ.' );
		}
		$fails = array();
		foreach ( (array) get_option( 'nadlan_smart_digest_mail_failures', array() ) as $f ) {
			if ( (int) ( $f['ts'] ?? 0 ) < $now - $day ) { continue; }
			$fails[] = $f;
		}
		if ( $fails ) {
			$subjects = array_unique( array_filter( array_map( function ( $f ) { return (string) ( $f['subject'] ?? '' ); }, $fails ) ) );
			$data['issues'][] = array(
				'text'   => count( $fails ) . ' מיילים מהאתר לא נשלחו ב-24 השעות האחרונות.',
				'detail' => ( $subjects ? 'למשל: ' . implode( ' | ', array_slice( $subjects, 0, 3 ) ) . '. ' : '' ) . 'שגיאה: ' . (string) ( end( $fails )['error'] ?? '' ),
			);
		}
		$events = array();
		foreach ( (array) get_option( 'nadlan_event_log', array() ) as $ev ) {
			if ( ! is_array( $ev ) || (int) ( $ev['ts'] ?? 0 ) < $now - $day ) { continue; }
			if ( ! in_array( (string) ( $ev['status'] ?? '' ), array( 'fail', 'error', 'critical' ), true ) ) { continue; }
			$k = (string) ( $ev['channel'] ?? '' ) . ' / ' . (string) ( $ev['id'] ?? '' );
			$events[ $k ] = (int) ( $events[ $k ] ?? 0 ) + 1;
		}
		if ( $events ) {
			arsort( $events );
			$bits = array();
			foreach ( array_slice( $events, 0, 5, true ) as $k => $n ) { $bits[] = $k . ' (' . $n . ')'; }
			$data['issues'][] = array( 'text' => 'כשלים ביומן האירועים של האתר (טפסים, שליחות, חיבורים).', 'detail' => implode( ' · ', $bits ) );
		}
		foreach ( $data['leads'] as $l ) {
			if ( ! empty( $l['ack_failed'] ) ) {
				$data['issues'][] = array( 'text' => 'מייל האישור ללקוח לא נשלח לליד של ' . ( $l['name'] ?: 'ללא שם' ) . '.', 'detail' => 'הליד נשמר, אבל הלקוח לא קיבל אישור. כדאי לחזור אליו בטלפון.' );
			}
		}

		return apply_filters( 'nadlan_smart_digest_data', $data, $now, $dry );
	}
}

/* ---------------------------------------------------------------------------------------------
 * Sending, and the schedule (08:00 site time, wp_timezone()).
 * ------------------------------------------------------------------------------------------- */

if ( ! function_exists( 'nadlan_sd_recipients' ) ) {
	function nadlan_sd_recipients() {
		$to = apply_filters( 'nadlan_smart_digest_recipients', array( get_option( 'admin_email' ) ) );
		return array_values( array_filter( array_map( 'sanitize_email', (array) $to ), 'is_email' ) );
	}
}

if ( ! function_exists( 'nadlan_sd_send' ) ) {
	function nadlan_sd_send( $now = 0 ) {
		if ( ! nadlan_smart_digest_on() ) { return false; }
		$now  = $now ? (int) $now : time();
		$data = nadlan_sd_collect( $now, false );
		$to   = nadlan_sd_recipients();
		if ( nadlan_sd_is_quiet( $data ) && ! nadlan_smart_digest_quiet_send_on() ) {
			nadlan_sd_log_push( 'nadlan_smart_digest_log', array( 'ts' => $now, 'ok' => true, 'quiet' => true, 'sent' => false ) );
			return true;
		}
		if ( ! $to ) {
			nadlan_sd_log_push( 'nadlan_smart_digest_log', array( 'ts' => $now, 'ok' => false, 'error' => 'no recipient' ) );
			return false;
		}
		$err = '';
		$catch = function ( $e ) use ( &$err ) { if ( is_wp_error( $e ) ) { $err = mb_substr( sanitize_text_field( $e->get_error_message() ), 0, 160 ); } };
		add_action( 'wp_mail_failed', $catch, 5 );
		$ok = wp_mail( $to, nadlan_sd_subject( $data ), nadlan_sd_render_html( $data ), array( 'Content-Type: text/html; charset=UTF-8' ) );
		remove_action( 'wp_mail_failed', $catch, 5 );
		nadlan_sd_log_push( 'nadlan_smart_digest_log', array(
			'ts'        => $now,
			'ok'        => (bool) $ok,
			'sent'      => true,
			'leads'     => count( $data['leads'] ),
			'decisions' => count( $data['decisions'] ),
			'issues'    => count( $data['issues'] ),
			'error'     => $ok ? '' : ( $err ?: 'wp_mail returned false' ),
		) );
		if ( function_exists( 'nadlan_log_event' ) ) {
			nadlan_log_event( 'smart_digest', 'daily', $ok ? 'ok' : 'fail', array( 'leads' => count( $data['leads'] ), 'decisions' => count( $data['decisions'] ) ) );
		}
		return (bool) $ok;
	}
}

if ( ! function_exists( 'nadlan_sd_next_0800' ) ) {
	function nadlan_sd_next_0800( $now = 0 ) {
		$tz  = wp_timezone();
		$now = $now ? (int) $now : time();
		$at  = new DateTime( '@' . $now );
		$at->setTimezone( $tz );
		$at->setTime( 8, 0, 0 );
		if ( $at->getTimestamp() <= $now ) { $at->modify( '+1 day' ); }
		return $at->getTimestamp();
	}
}

add_action( 'init', function () {
	if ( ! wp_next_scheduled( 'nadlan_smart_digest_daily' ) ) {
		wp_schedule_event( nadlan_sd_next_0800(), 'daily', 'nadlan_smart_digest_daily' );
	}
} );
add_action( 'nadlan_smart_digest_daily', 'nadlan_sd_send' );

/* Preview for an admin, without sending and without marking anything as reported:
 * /wp-admin/admin-post.php?action=nadlan_sd_preview */
add_action( 'admin_post_nadlan_sd_preview', function () {
	if ( ! current_user_can( 'manage_options' ) ) { wp_die( 'אין הרשאה.', 'נדלן', array( 'response' => 403 ) ); }
	nocache_headers();
	header( 'Content-Type: text/html; charset=UTF-8' );
	$data = nadlan_sd_collect( time(), true );
	echo '<!doctype html><meta charset="utf-8"><title>' . esc_html( nadlan_sd_subject( $data ) ) . '</title>';
	echo nadlan_sd_render_html( $data ); // phpcs:ignore WordPress.Security.EscapeOutput -- escaped inside.
	exit;
} );

add_filter( 'nadlan_config_healthcheck', function ( $out ) {
	$log  = (array) get_option( 'nadlan_smart_digest_log', array() );
	$last = $log ? end( $log ) : null;
	$out['smart_digest'] = array(
		'on'        => nadlan_smart_digest_on(),
		'legacy_on' => nadlan_smart_digest_legacy_on(),
		'next'      => wp_next_scheduled( 'nadlan_smart_digest_daily' ) ? gmdate( 'c', (int) wp_next_scheduled( 'nadlan_smart_digest_daily' ) ) : null,
		'last_ts'   => is_array( $last ) ? gmdate( 'c', (int) ( $last['ts'] ?? 0 ) ) : null,
		'last_ok'   => is_array( $last ) ? (bool) ( $last['ok'] ?? false ) : null,
	);
	return $out;
} );
