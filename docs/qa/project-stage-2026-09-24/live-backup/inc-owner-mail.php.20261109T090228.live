<?php
/**
 * OwnerMail v1 (HAD-687, Ben 8.11.2026 by voice: the daily mails are "סתם מנג'ס, זה לא נותן שום דבר ... שיהיה אפשר לבצע פעולות
 * דרך המייל"). Loaded from inc/alerts.php before owner-morning.php. Claude Design: DS component OwnerMail (README + preview).
 * Research, sources and the counted comparison: docs/research/2026-11-08-owner-mail/.
 *
 * 1. One lead card in every owner mail about a person: the name, the phone big and tappable, WhatsApp with a ready line, the page the
 *    person came from, what they asked about, and a heat score with its reasons (the points are shown, never a black box).
 * 2. Action buttons that work without signing in: "חזרתי אליו", "לא רלוונטי", "תזכיר לי מחר בבוקר", and per alert kind "השתק" for
 *    30 days (muted items still reach the morning mail; nothing is lost). Each link is signed (HMAC-SHA256 with the site's auth salt
 *    over action, lead, kind and expiry; 30 days). Opening a link never writes: mail scanners open links (the reason RFC 8058 asks
 *    for POST), so the link shows a page with the lead and one confirm button, and only that POST writes. Every write has an undo.
 * 3. One mail per lead: the plain copies that conversion-cta.php and ai-concierge.php send to the owner are held when this lead's
 *    card is already scheduled. Held mails are listed in the dashboard widget "מיילים לבעלים", never silently lost.
 * 4. The morning numbers (owner-morning.php): leads, sign-ups (the price window and the area alerts), property views, Google clicks
 *    (pushed once a day from the owner's computer by tools/ownermail/push_gsc.py; omitted when stale, never guessed) and paid orders,
 *    yesterday against the day before and the week.
 */
if ( ! defined( 'ABSPATH' ) ) { exit; }

if ( ! function_exists( 'nadlan_omx_sig' ) ) {

	/** The alert kinds a mute can silence (instant mail only; the morning mail still lists them). */
	function nadlan_omx_kinds() {
		return array(
			'lead'        => 'לידים מטפסים באתר',
			'price_alert' => 'נרשמים לחלון עדכוני המחירים',
			'concierge'   => 'פניות מהיועץ באתר',
			'hot'         => 'מבקרים חמים בנכסים (וואטסאפ, טלפון, מבקר חוזר)',
		);
	}

	/* ---------- signed links ---------- */
	function nadlan_omx_sig( $a, $l, $k, $e ) {
		return substr( hash_hmac( 'sha256', 'nlomx|' . $a . '|' . (int) $l . '|' . $k . '|' . (int) $e, wp_salt( 'auth' ) ), 0, 32 );
	}
	function nadlan_omx_url( $a, $l = 0, $k = '' ) {
		$e = time() + 30 * DAY_IN_SECONDS;
		return add_query_arg( array( 'a' => $a, 'l' => (int) $l, 'k' => $k, 'e' => $e, 's' => nadlan_omx_sig( $a, $l, $k, $e ) ), rest_url( 'nadlan/v1/om-act' ) );
	}
	function nadlan_omx_check( $a, $l, $k, $e, $s ) {
		return (int) $e >= time() && is_string( $s ) && 32 === strlen( $s ) && hash_equals( nadlan_omx_sig( $a, $l, $k, $e ), $s );
	}

	/* ---------- the lead ---------- */
	function nadlan_omx_m( $lid, $k ) { return trim( (string) get_post_meta( (int) $lid, $k, true ) ); }

	function nadlan_omx_lead_kind( $lid ) {
		$u = nadlan_omx_m( $lid, 'utm_source' );
		if ( 'price_alert' === $u ) { return 'price_alert'; }
		if ( false !== stripos( $u . ' ' . nadlan_omx_m( $lid, 'lead_e2e_context' ), 'concierge' ) ) { return 'concierge'; }
		return 'lead';
	}
	function nadlan_omx_muted( $k ) {
		$m = (array) get_option( 'nadlan_omx_mute', array() );
		return ! empty( $m[ $k ] ) && (int) $m[ $k ] > time();
	}
	function nadlan_omx_mute( $k, $on ) {
		$m = (array) get_option( 'nadlan_omx_mute', array() );
		if ( $on ) { $m[ $k ] = time() + 30 * DAY_IN_SECONDS; } else { unset( $m[ $k ] ); }
		update_option( 'nadlan_omx_mute', $m, false );
	}

	/** array( wa.me number, tel number with +, the phone as shown ) */
	function nadlan_omx_phone( $raw ) {
		$raw = trim( (string) $raw );
		$d   = preg_replace( '/\D+/', '', $raw );
		if ( strlen( $d ) < 7 ) { return array( '', '', $raw ); }
		if ( 0 === strpos( $raw, '+' ) || 0 === strpos( $d, '972' ) ) { $intl = $d; } elseif ( 0 === strpos( $d, '0' ) ) { $intl = '972' . substr( $d, 1 ); } else { $intl = $d; }
		$local  = 0 === strpos( $intl, '972' ) ? '0' . substr( $intl, 3 ) : '+' . $intl;
		$pretty = preg_match( '/^0(5\d|7\d)(\d{3})(\d{4})$/', $local, $m ) ? '0' . $m[1] . '-' . $m[2] . '-' . $m[3]
			: ( preg_match( '/^0(\d)(\d{3})(\d{4})$/', $local, $m ) ? '0' . $m[1] . '-' . $m[2] . '-' . $m[3] : $local );
		return array( $intl, '+' . $intl, $pretty );
	}

	/** Earlier leads with the same phone (last 9 digits), newest first. */
	function nadlan_omx_prev_leads( $lid ) {
		$ph = preg_replace( '/\D+/', '', nadlan_omx_m( $lid, 'phone' ) );
		if ( strlen( $ph ) < 9 ) { return array(); }
		global $wpdb;
		$like = '%' . $wpdb->esc_like( substr( $ph, -9 ) ) . '%';
		return array_map( 'intval', (array) $wpdb->get_col( $wpdb->prepare(
			"SELECT p.ID FROM {$wpdb->posts} p JOIN {$wpdb->postmeta} m ON m.post_id = p.ID AND m.meta_key = 'phone'
			WHERE p.post_type = 'nadlan_lead' AND p.ID <> %d AND p.post_status NOT IN ('trash','auto-draft')
			AND REPLACE(REPLACE(REPLACE(m.meta_value,'-',''),' ',''),'+','') LIKE %s ORDER BY p.ID DESC LIMIT 10", (int) $lid, $like ) ) );
	}

	/** The heat score: 15 to start, points per signal, each reason shown in the mail. */
	function nadlan_omx_heat( $lid ) {
		$pts  = array();
		$txt  = trim( wp_strip_all_tags( (string) get_post_field( 'post_content', $lid ) ) );
		$goal = nadlan_omx_m( $lid, 'goal' ) . ' ' . nadlan_omx_m( $lid, 'topic' );
		if ( '1' === nadlan_omx_m( $lid, 'pa_callback' ) || preg_match( '/שיחה|להתקשר|שיחת/u', $goal ) ) { $pts['בקשה לשיחה'] = 25; }
		if ( mb_strlen( $txt ) >= 15 ) { $pts['הודעה בכתב'] = 15; }
		if ( nadlan_omx_m( $lid, 'unit' ) || nadlan_omx_m( $lid, 'rooms' ) || nadlan_omx_m( $lid, 'budget' ) || nadlan_omx_m( $lid, 'floor' ) ) { $pts['שאלה על דירה, חדרים או תקציב'] = 20; }
		if ( (int) nadlan_omx_m( $lid, 'project_wp_id' ) ) { $pts['פנייה מתוך עמוד פרויקט או נכס'] = 10; }
		if ( is_email( nadlan_omx_m( $lid, 'email' ) ) && nadlan_omx_m( $lid, 'phone' ) ) { $pts['טלפון וגם מייל'] = 5; }
		$prev = nadlan_omx_prev_leads( $lid );
		if ( $prev ) { $pts[ 'פנייה חוזרת (עוד ' . count( $prev ) . ' בעבר)' ] = 10; }
		$ai = nadlan_omx_m( $lid, 'lead_score' );
		if ( is_numeric( $ai ) ) { $pts[ 'הניתוח האוטומטי: ' . (int) $ai ] = (int) round( max( 0, min( 100, (float) $ai ) ) * 0.25 ); }
		$score = (int) min( 100, 15 + array_sum( $pts ) );
		return array( 'score' => $score, 'level' => $score >= 70 ? 'hot' : ( $score >= 45 ? 'warm' : 'cold' ), 'why' => $pts );
	}

	function nadlan_omx_where( $lid ) {
		$pid = (int) nadlan_omx_m( $lid, 'project_wp_id' );
		$t   = $pid ? get_the_title( $pid ) : nadlan_omx_m( $lid, 'project_title' );
		return wp_strip_all_tags( html_entity_decode( (string) $t, ENT_QUOTES, 'UTF-8' ) );
	}

	/** The ready WhatsApp line (Ben's words rule: neutral, he edits it before sending; filter nadlan_omx_wa_text). */
	function nadlan_omx_wa_text( $lid ) {
		$first = preg_split( '/\s+/u', nadlan_omx_m( $lid, 'name' ) )[0] ?? '';
		$where = nadlan_omx_where( $lid );
		$t = 'שלום' . ( '' !== $first ? ' ' . $first : '' ) . ', קיבלנו את הפנייה שלך באתר נדל״ן' . ( '' !== $where ? ' לגבי ' . $where : '' ) . '. מתי נוח לדבר?';
		return (string) apply_filters( 'nadlan_omx_wa_text', $t, $lid );
	}

	function nadlan_omx_facts( $lid ) {
		$f   = array();
		$pid = (int) nadlan_omx_m( $lid, 'project_wp_id' );
		$src = nadlan_omx_m( $lid, 'source_url' );
		$wh  = nadlan_omx_where( $lid );
		$url = $src ? $src : ( $pid ? get_permalink( $pid ) : '' );
		if ( $url ) {
			$path = rawurldecode( (string) wp_parse_url( $url, PHP_URL_PATH ) );
			$f['מאיזה עמוד'] = array( '' !== $wh ? $wh : ( $path ? $path : $url ), $url );
		} elseif ( '' !== $wh ) {
			$f['מאיזה עמוד'] = $wh;
		}
		if ( nadlan_omx_m( $lid, 'goal' ) ) { $f['מה ביקש'] = nadlan_omx_m( $lid, 'goal' ); }
		$want = array_filter( array(
			nadlan_omx_m( $lid, 'rooms' ) ? nadlan_omx_m( $lid, 'rooms' ) . ' חדרים' : '',
			nadlan_omx_m( $lid, 'budget' ) ? 'תקציב ' . nadlan_omx_m( $lid, 'budget' ) : '',
			nadlan_omx_m( $lid, 'unit' ) ? 'דירה ' . nadlan_omx_m( $lid, 'unit' ) : '',
			nadlan_omx_m( $lid, 'floor' ) ? 'קומה ' . nadlan_omx_m( $lid, 'floor' ) : '',
			nadlan_omx_m( $lid, 'timeline' ) ? 'מתי: ' . nadlan_omx_m( $lid, 'timeline' ) : '',
		) );
		if ( $want ) { $f['מה עניין אותו'] = implode( ' · ', $want ); }
		$city = nadlan_omx_m( $lid, 'city' );
		if ( '' === $city && $pid ) { $city = trim( (string) get_post_meta( $pid, 'city', true ) ); }
		if ( '' !== $city ) { $f['עיר'] = $city; }
		$msg = trim( wp_strip_all_tags( (string) get_post_field( 'post_content', $lid ) ) );
		if ( '' !== $msg ) { $f['ההודעה'] = mb_substr( $msg, 0, 300 ); }
		$u   = nadlan_omx_m( $lid, 'utm_source' );
		$lab = array( 'price_alert' => 'חלון עדכוני המחירים', 'google' => 'גוגל', 'facebook' => 'פייסבוק', 'instagram' => 'אינסטגרם', 'whatsapp' => 'וואטסאפ' );
		if ( '' !== $u ) { $f['מקור'] = $lab[ $u ] ?? $u; }
		$prev = nadlan_omx_prev_leads( $lid );
		if ( $prev ) {
			$p0 = $prev[0];
			$f['פנה כבר'] = count( $prev ) . ' פעמים · האחרונה ' . get_the_date( 'j.n.Y', $p0 ) . ( '' !== nadlan_omx_where( $p0 ) ? ' · ' . nadlan_omx_where( $p0 ) : '' );
		}
		return $f;
	}

	/* ---------- the mail parts (OwnerMail DS: slate ink, survey teal, registry green; Arial, as mail clients load no web font) ---------- */
	function nadlan_omx_btn( $href, $label, $bg, $fg = '#FFFFFF', $bd = '' ) {
		return '<a href="' . esc_url( $href, array( 'http', 'https', 'tel', 'mailto' ) ) . '" style="display:inline-block;margin:0 0 8px 6px;padding:14px 16px;background:' . $bg . ';color:' . $fg
			. ';border:1px solid ' . ( $bd ? $bd : $bg ) . ';border-radius:6px;font-size:15px;line-height:20px;font-weight:700;text-decoration:none">' . esc_html( $label ) . '</a>';
	}
	function nadlan_omx_heat_color( $lvl ) {
		return array( 'hot' => array( '#B42318', 'חם' ), 'warm' => array( '#2F6F86', 'פושר' ), 'cold' => array( '#5E6A75', 'קר' ) )[ $lvl ] ?? array( '#5E6A75', 'קר' );
	}
	function nadlan_omx_chip( $h ) {
		$c = nadlan_omx_heat_color( $h['level'] );
		return '<span style="display:inline-block;padding:3px 10px;border-radius:999px;background:' . $c[0] . ';color:#FFFFFF;font-size:13px;font-weight:700;white-space:nowrap">' . $c[1] . ' · ' . (int) $h['score'] . '</span>';
	}
	function nadlan_omx_heat_bar( $h ) {
		$c = nadlan_omx_heat_color( $h['level'] );
		$n = (int) round( $h['score'] / 10 );
		$cells = '';
		for ( $i = 1; $i <= 10; $i++ ) { $cells .= '<td style="width:10%;height:6px;padding:0 0 0 2px"><div style="height:6px;border-radius:2px;background:' . ( $i <= $n ? $c[0] : '#E3E8EC' ) . '"></div></td>'; }
		$why = array();
		foreach ( $h['why'] as $k => $v ) { $why[] = esc_html( $k ) . ' <span style="color:#5E6A75">+' . (int) $v . '</span>'; }
		return '<table role="presentation" width="100%" cellpadding="0" cellspacing="0" dir="rtl"><tr>' . $cells . '</tr></table>'
			. '<div style="font-size:13px;line-height:20px;color:#3E4C58;margin-top:6px"><b style="color:' . $c[0] . '">' . $c[1] . ' ' . (int) $h['score'] . '/100</b>'
			. ( $why ? ' · ' . implode( ' · ', $why ) : ' · פנייה בסיסית, בלי סימני עניין נוספים' ) . '</div>';
	}

	/** The lead card rows (the name, the phone, call and WhatsApp, the heat, the facts); $actions adds the signed buttons. */
	function nadlan_omx_card( $lid, $actions = true ) {
		list( $intl, $tel, $pretty ) = nadlan_omx_phone( nadlan_omx_m( $lid, 'phone' ) );
		$name  = nadlan_omx_m( $lid, 'name' );
		$email = is_email( nadlan_omx_m( $lid, 'email' ) ) ? nadlan_omx_m( $lid, 'email' ) : '';
		$h     = nadlan_omx_heat( $lid );
		$o = '<tr><td style="padding:16px 18px 4px"><div style="font-size:20px;line-height:26px;font-weight:700">' . esc_html( '' !== $name ? $name : 'פונה בלי שם' ) . '</div>';
		if ( $intl ) {
			$o .= '<div dir="ltr" style="font-size:34px;line-height:42px;font-weight:800;letter-spacing:.5px;margin:4px 0 10px;text-align:right"><a href="' . esc_url( 'tel:' . $tel, array( 'tel' ) ) . '" style="color:#12202A;text-decoration:none">' . esc_html( $pretty ) . '</a></div>'
				. nadlan_omx_btn( 'tel:' . $tel, 'התקשר עכשיו', '#2F6F86' )
				. nadlan_omx_btn( 'https://wa.me/' . $intl . '?text=' . rawurlencode( nadlan_omx_wa_text( $lid ) ), 'וואטסאפ עם הודעה מוכנה', '#0F7A63' );
		} elseif ( '' !== $pretty ) {
			$o .= '<div style="font-size:18px;margin:4px 0 10px">' . esc_html( $pretty ) . '</div>';
		}
		if ( $email ) { $o .= nadlan_omx_btn( 'mailto:' . $email, 'מייל', '#FFFFFF', '#12202A', '#C5CFD7' ); }
		$o .= '</td></tr><tr><td style="padding:6px 18px 12px">' . nadlan_omx_heat_bar( $h ) . '</td></tr>';
		$o .= '<tr><td style="padding:0 18px 10px"><table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="border-top:1px solid #E3E8EC">';
		foreach ( nadlan_omx_facts( $lid ) as $k => $v ) {
			$val = is_array( $v ) ? '<a href="' . esc_url( $v[1] ) . '" style="color:#1F4B5C">' . esc_html( $v[0] ) . '</a>' : nl2br( esc_html( $v ) );
			$o .= '<tr><td valign="top" style="padding:8px 0 8px 12px;width:104px;color:#5E6A75;font-size:13px;border-bottom:1px solid #E3E8EC">' . esc_html( $k ) . '</td>'
				. '<td style="padding:8px 0;font-size:15px;line-height:22px;border-bottom:1px solid #E3E8EC">' . $val . '</td></tr>';
		}
		$o .= '</table></td></tr>';
		if ( $actions ) {
			$o .= '<tr><td style="padding:12px 18px 6px;background:#F6F8F9;border-top:1px solid #E3E8EC"><div style="font-size:13px;color:#3E4C58;margin:0 0 8px">אחרי שטיפלת, לחיצה אחת מעדכנת את הליד באתר, בלי להיכנס:</div>'
				. nadlan_omx_btn( nadlan_omx_url( 'contacted', $lid ), '✓ חזרתי אליו', '#12202A' )
				. nadlan_omx_btn( nadlan_omx_url( 'lost', $lid ), 'לא רלוונטי', '#FFFFFF', '#3E4C58', '#C5CFD7' )
				. nadlan_omx_btn( nadlan_omx_url( 'snooze', $lid ), 'תזכיר לי מחר בבוקר', '#FFFFFF', '#1F4B5C', '#2F6F86' ) . '</td></tr>';
		}
		return $o;
	}

	/** The whole mail: a hidden preview line, the dark strip, the body rows, the small footer. */
	function nadlan_omx_doc( $pre, $strip, $rows, $foot ) {
		return '<!doctype html><html lang="he" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="color-scheme" content="light only"><title>נדל״ן</title></head>'
			. '<body style="margin:0;padding:0;background:#EEF2F4"><div style="display:none;max-height:0;overflow:hidden;opacity:0">' . esc_html( $pre ) . '</div>'
			. '<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:#EEF2F4"><tr><td align="center" style="padding:16px 8px">'
			. '<table role="presentation" width="100%" cellpadding="0" cellspacing="0" dir="rtl" style="max-width:580px;background:#FFFFFF;border:1px solid #D3DCE2;border-radius:10px;font-family:Arial,\'Segoe UI\',Helvetica,sans-serif;color:#12202A;text-align:right">'
			. '<tr><td style="background:#10262F;border-radius:10px 10px 0 0;padding:12px 18px;color:#CFE3EA;font-size:13px;font-weight:700">' . $strip . '</td></tr>'
			. $rows
			. '<tr><td style="padding:12px 18px 16px;border-top:1px solid #E3E8EC;color:#5E6A75;font-size:12px;line-height:18px">' . $foot . '</td></tr>'
			. '</table></td></tr></table></body></html>';
	}
	function nadlan_omx_strip( $left, $right = '' ) {
		return '<table role="presentation" width="100%" cellpadding="0" cellspacing="0"><tr><td style="color:#CFE3EA;font-size:13px;font-weight:700">' . $left . '</td>'
			. ( '' !== $right ? '<td align="left" style="white-space:nowrap">' . $right . '</td>' : '' ) . '</tr></table>';
	}
	function nadlan_omx_mute_link( $k ) {
		$kinds = nadlan_omx_kinds();
		return '<a href="' . esc_url( nadlan_omx_url( 'mute', 0, $k ) ) . '" style="color:#5E6A75">השתק התראות מיידיות על ' . esc_html( $kinds[ $k ] ?? $k ) . ' ל־30 יום</a> (הן יגיעו רק במייל הבוקר)';
	}

	/** array( html, text, subject ) of the instant lead mail. */
	function nadlan_omx_lead_mail( $lid, $title = 'ליד חדש' ) {
		$h = nadlan_omx_heat( $lid );
		list( $intl, $tel, $pretty ) = nadlan_omx_phone( nadlan_omx_m( $lid, 'phone' ) );
		$k     = nadlan_omx_lead_kind( $lid );
		$kinds = nadlan_omx_kinds();
		$name  = nadlan_omx_m( $lid, 'name' );
		$wh    = nadlan_omx_where( $lid );
		$when  = (int) get_post_time( 'U', true, $lid );
		$c     = nadlan_omx_heat_color( $h['level'] );
		$rows  = nadlan_omx_card( $lid, true )
			. '<tr><td style="padding:8px 18px 4px;font-size:13px;line-height:20px;color:#3E4C58">התקבל ב־' . esc_html( wp_date( 'H:i', $when ) ) . ' (' . esc_html( $kinds[ $k ] ) . '). כדאי לחזור בתוך 5 דקות: אז הסיכוי לתפוס את הפונה הכי גבוה.</td></tr>';
		$foot = 'קיבלת את המייל כי השאירו פרטים באתר. ליד מגיע מיד, כל השאר מחכה למייל הבוקר ב־08:00.<br>'
			. nadlan_omx_mute_link( $k ) . ' · <a href="' . esc_url( admin_url( 'post.php?post=' . (int) $lid . '&action=edit' ) ) . '" style="color:#5E6A75">פתיחה בניהול</a>';
		$html = nadlan_omx_doc( trim( $name . ' · ' . $pretty . ' · ' . $wh . ' · ' . $c[1] . ' ' . $h['score'] ), nadlan_omx_strip( 'נדל״ן · ' . esc_html( $title ) . ' · ' . esc_html( wp_date( 'H:i', $when ) ), nadlan_omx_chip( $h ) ), $rows, $foot );
		$text = implode( "\n", array_filter( array(
			$title . ' · ' . $c[1] . ' ' . $h['score'] . '/100',
			$name, $pretty,
			$intl ? 'חיוג: tel:' . $tel : '',
			$intl ? 'וואטסאפ: https://wa.me/' . $intl . '?text=' . rawurlencode( nadlan_omx_wa_text( $lid ) ) : '',
			'' !== $wh ? 'עמוד: ' . $wh : '',
			'',
			'חזרתי אליו: ' . nadlan_omx_url( 'contacted', $lid ),
			'לא רלוונטי: ' . nadlan_omx_url( 'lost', $lid ),
			'תזכיר לי מחר בבוקר: ' . nadlan_omx_url( 'snooze', $lid ),
		), 'strlen' ) );
		$subj = 'ליד ' . $c[1] . ' · ' . ( '' !== $name ? $name : 'בלי שם' ) . ( '' !== $pretty ? ' · ' . $pretty : '' ) . ( '' !== $wh ? ' · ' . $wh : '' );
		if ( 'ליד חדש' !== $title ) { $subj = $title . ' · ' . $subj; }
		return array( $html, $text, $subj );
	}

	/** wp_mail with a plain-text twin and a kind header; every send is logged for the dashboard widget. */
	function nadlan_omx_send( $subj, $html, $text, $kind, $to = '' ) {
		$to = $to ? $to : get_option( 'admin_email' );
		if ( ! $to ) { return false; }
		$alt = function ( $pm ) use ( $text ) { $pm->AltBody = $text; };
		add_action( 'phpmailer_init', $alt, 99 );
		$ok = (bool) wp_mail( $to, $subj, $html, array( 'Content-Type: text/html; charset=UTF-8', 'X-NadLan-Mail: owner-' . sanitize_key( $kind ) ) );
		remove_action( 'phpmailer_init', $alt, 99 );
		nadlan_omx_log( $kind, $subj, $ok ? 'sent' : 'failed' );
		return $ok;
	}
	function nadlan_omx_log( $kind, $subj, $res ) {
		$g = (array) get_option( 'nadlan_omx_log', array() );
		array_unshift( $g, array( 't' => time(), 'k' => sanitize_key( $kind ), 's' => mb_substr( wp_strip_all_tags( (string) $subj ), 0, 140 ), 'r' => sanitize_key( $res ) ) );
		update_option( 'nadlan_omx_log', array_slice( $g, 0, 60 ), false );
	}

	/** The instant lead mail: once per lead; a muted kind waits for the morning mail instead. */
	function nadlan_omx_lead_alert( $lid, $force = false ) {
		$l = get_post( (int) $lid );
		if ( ! $l || 'nadlan_lead' !== $l->post_type ) { return false; }
		if ( ! $force && get_post_meta( $l->ID, 'lead_omx_alert', true ) ) { return false; }
		$k = nadlan_omx_lead_kind( $l->ID );
		if ( ! $force && nadlan_omx_muted( $k ) ) {
			update_post_meta( $l->ID, 'lead_omx_alert', 'muted ' . gmdate( 'Y-m-d H:i' ) );
			nadlan_omx_log( $k, nadlan_omx_m( $l->ID, 'name' ), 'muted' );
			return false;
		}
		list( $html, $text, $subj ) = nadlan_omx_lead_mail( $l->ID, $force ? 'דוגמה' : 'ליד חדש' );
		$ok = nadlan_omx_send( $subj, $html, $text, $k );
		if ( ! $force ) { update_post_meta( $l->ID, 'lead_omx_alert', ( $ok ? 'sent ' : 'failed ' ) . gmdate( 'Y-m-d H:i' ) ); }
		return $ok;
	}

	/* ---------- the actions ---------- */
	function nadlan_omx_set_status( $lid, $new ) {
		$old = sanitize_key( (string) get_post_meta( $lid, 'lead_status', true ) );
		if ( '' === $old ) { $old = 'new'; }
		set_transient( 'nadlan_omx_undo_' . (int) $lid, array( 'st' => $old, 'fr' => (int) get_post_meta( $lid, 'lead_first_response_at', true ) ), 30 * DAY_IN_SECONDS );
		if ( 'new' !== $new && (int) get_post_meta( $lid, 'lead_first_response_at', true ) <= 0 ) {
			update_post_meta( $lid, 'lead_first_response_at', time() );
			update_post_meta( $lid, 'lead_first_response_via', 'owner-mail' );
		}
		if ( $new !== $old ) {
			update_post_meta( $lid, 'lead_status', $new );
			if ( function_exists( 'nadlan_lead_e2e_audit' ) ) {
				nadlan_lead_e2e_audit( array( 'lead_id' => $lid, 'card_id' => (int) get_post_meta( $lid, 'lead_card_id', true ), 'user_id' => 0, 'old' => $old, 'new' => $new, 'note' => 'owner-mail' ) );
			}
		}
		return $old;
	}
	/** Undo: the status and the first-response time as they were before the last mail action. */
	function nadlan_omx_undo( $lid ) {
		$u = get_transient( 'nadlan_omx_undo_' . (int) $lid );
		$st = is_array( $u ) && ! empty( $u['st'] ) ? sanitize_key( $u['st'] ) : 'new';
		$old = sanitize_key( (string) get_post_meta( $lid, 'lead_status', true ) );
		if ( is_array( $u ) && empty( $u['fr'] ) && 'owner-mail' === get_post_meta( $lid, 'lead_first_response_via', true ) ) {
			delete_post_meta( $lid, 'lead_first_response_at' );
			delete_post_meta( $lid, 'lead_first_response_via' );
		}
		if ( $st !== $old ) {
			update_post_meta( $lid, 'lead_status', $st );
			if ( function_exists( 'nadlan_lead_e2e_audit' ) ) {
				nadlan_lead_e2e_audit( array( 'lead_id' => $lid, 'card_id' => (int) get_post_meta( $lid, 'lead_card_id', true ), 'user_id' => 0, 'old' => $old, 'new' => $st, 'note' => 'owner-mail undo' ) );
			}
		}
		delete_transient( 'nadlan_omx_undo_' . (int) $lid );
		return $st;
	}
	/** "Tomorrow morning": before 06:00 that is this morning's mail, otherwise tomorrow's. */
	function nadlan_omx_snooze_day() {
		return (int) wp_date( 'G' ) < 6 ? wp_date( 'Y-m-d' ) : wp_date( 'Y-m-d', time() + DAY_IN_SECONDS );
	}

	function nadlan_omx_page( $title, $body ) {
		nocache_headers();
		do_action( 'litespeed_control_set_nocache', 'nadlan owner mail action' );
		status_header( 200 );
		header( 'Content-Type: text/html; charset=utf-8' );
		echo '<!doctype html><html lang="he" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>' . esc_html( $title ) . ' · נדל״ן</title>'
			. '<style>body{margin:0;background:#EEF2F4;color:#12202A;font:16px/1.6 Arial,"Segoe UI",sans-serif}main{max-width:580px;margin:0 auto;padding:18px 12px 64px}'
			. '.top{background:#10262F;color:#CFE3EA;border-radius:10px 10px 0 0;padding:12px 18px;font-weight:700;font-size:14px}.box{background:#fff;border:1px solid #D3DCE2;border-radius:10px}'
			. '.in{padding:16px 18px}h1{margin:0 0 8px;font-size:26px;line-height:1.25}p{margin:0 0 12px;color:#3E4C58}.go,.alt{display:inline-flex;align-items:center;justify-content:center;min-height:52px;padding:0 22px;border-radius:6px;font:700 17px/1.2 Arial,sans-serif;text-decoration:none;cursor:pointer;border:1px solid #12202A;background:#12202A;color:#fff;margin:0 0 10px 8px}'
			. '.alt{background:#fff;color:#1F4B5C;border-color:#2F6F86}.fine{font-size:13px;color:#5E6A75}form{display:inline}table{border-collapse:collapse}:focus-visible{outline:3px solid #2F6F86;outline-offset:2px}</style></head>'
			. '<body><main><div class="box"><div class="top">נדל״ן · פעולה מהמייל</div><div class="in"><h1>' . esc_html( $title ) . '</h1>' . $body . '</div></div></main></body></html>';
		exit;
	}
	function nadlan_omx_page_lead( $lid ) {
		return '<table role="presentation" width="100%" style="margin:0 0 12px;border:1px solid #E3E8EC;border-radius:8px">' . nadlan_omx_card( $lid, false ) . '</table>';
	}
	function nadlan_omx_form( $a, $l, $k, $label, $class = 'go' ) {
		$e = time() + 30 * DAY_IN_SECONDS;
		$u = add_query_arg( array( 'a' => $a, 'l' => (int) $l, 'k' => $k, 'e' => $e, 's' => nadlan_omx_sig( $a, $l, $k, $e ) ), rest_url( 'nadlan/v1/om-act' ) );
		return '<form method="post" action="' . esc_url( $u ) . '"><button class="' . esc_attr( $class ) . '" type="submit">' . esc_html( $label ) . '</button></form>';
	}

	function nadlan_omx_act_route( WP_REST_Request $req ) {
		$a = sanitize_key( (string) $req->get_param( 'a' ) );
		$l = absint( $req->get_param( 'l' ) );
		$k = sanitize_key( (string) $req->get_param( 'k' ) );
		$e = absint( $req->get_param( 'e' ) );
		$s = (string) $req->get_param( 's' );
		$kinds = nadlan_omx_kinds();
		$ask = array( 'contacted' => 'כן, חזרתי אליו', 'lost' => 'כן, לא רלוונטי', 'snooze' => 'כן, תזכיר לי מחר בבוקר', 'undo' => 'כן, החזר כמו שהיה',
			'unsnooze' => 'כן, בטל את התזכורת', 'mute' => 'כן, השתק ל־30 יום', 'unmute' => 'כן, בטל את ההשתקה' );
		$lead_act = in_array( $a, array( 'contacted', 'lost', 'snooze', 'undo', 'unsnooze' ), true );
		$valid = isset( $ask[ $a ] ) && nadlan_omx_check( $a, $l, $k, $e, $s ) && ( $lead_act ? 'nadlan_lead' === get_post_type( $l ) : isset( $kinds[ $k ] ) );
		if ( ! $valid ) {
			nadlan_omx_page( 'הקישור אינו בתוקף', '<p>ייתכן שעברו יותר מ־30 יום מאז המייל, או שהקישור נקטע. אפשר לעדכן את הליד מתוך הניהול.</p><p><a class="alt" href="' . esc_url( admin_url( 'edit.php?post_type=nadlan_lead' ) ) . '">לרשימת הלידים</a></p>' );
		}
		$name = $lead_act ? nadlan_omx_m( $l, 'name' ) : '';
		if ( 'POST' !== $req->get_method() ) { // opening the link changes nothing: one tap on the button writes
			$q = array( 'contacted' => 'לסמן שחזרת אל ' . $name . '?', 'lost' => 'לסמן את ' . $name . ' כלא רלוונטי?', 'snooze' => 'להזכיר לך על ' . $name . ' במייל של מחר בבוקר?',
				'undo' => 'להחזיר את ' . $name . ' למצב הקודם?', 'unsnooze' => 'לבטל את התזכורת על ' . $name . '?',
				'mute' => 'להשתיק ל־30 יום התראות מיידיות על ' . ( $kinds[ $k ] ?? '' ) . '?', 'unmute' => 'לחזור לקבל מיד התראות על ' . ( $kinds[ $k ] ?? '' ) . '?' );
			$body = ( $lead_act ? nadlan_omx_page_lead( $l ) : '<p>' . ( 'mute' === $a ? 'הן לא יאבדו: כל אחת תופיע במייל הבוקר ב־08:00. אפשר לבטל בכל רגע.' : 'כל התראה מהסוג הזה תגיע שוב מיד כשהיא קורית.' ) . '</p>' )
				. nadlan_omx_form( $a, $l, $k, $ask[ $a ] ) . '<p class="fine">פתיחת הקישור לא שינתה כלום. רק הלחיצה על הכפתור שומרת.</p>';
			nadlan_omx_page( $q[ $a ], $body );
		}
		$day = '';
		switch ( $a ) {
			case 'contacted':
			case 'lost':
				nadlan_omx_set_status( $l, $a );
				delete_post_meta( $l, 'lead_omx_snooze' );
				break;
			case 'undo':
				nadlan_omx_undo( $l );
				break;
			case 'snooze':
				$day = nadlan_omx_snooze_day();
				update_post_meta( $l, 'lead_omx_snooze', $day );
				break;
			case 'unsnooze':
				delete_post_meta( $l, 'lead_omx_snooze' );
				break;
			case 'mute':
			case 'unmute':
				nadlan_omx_mute( $k, 'mute' === $a );
				break;
		}
		nadlan_omx_log( $lead_act ? nadlan_omx_lead_kind( $l ) : $k, ( $lead_act ? '#' . $l . ' ' : $k . ' ' ) . $a, 'action' );
		$done = array(
			'contacted' => array( 'נשמר: חזרת אל ' . $name, 'הליד סומן "חזרו אליו". הוא לא יופיע יותר במייל הבוקר.', 'undo', 'בטל, החזר כמו שהיה' ),
			'lost'      => array( 'נשמר: ' . $name . ' לא רלוונטי', 'הליד סגור. הוא לא יופיע יותר במייל הבוקר.', 'undo', 'בטל, החזר כמו שהיה' ),
			'undo'      => array( 'הוחזר כמו שהיה', 'הליד חזר למצב שלפני הלחיצה.', '', '' ),
			'snooze'    => array( 'נזכיר לך מחר בבוקר', 'הליד יופיע בראש מייל הבוקר של ' . ( $day ? wp_date( 'j.n', strtotime( $day . ' 12:00:00' ) ) : '' ) . ', עם כפתורי חיוג ווואטסאפ.', 'unsnooze', 'בטל את התזכורת' ),
			'unsnooze'  => array( 'התזכורת בוטלה', 'הליד לא יופיע בראש מייל הבוקר.', '', '' ),
			'mute'      => array( 'הושתק ל־30 יום', 'התראות מיידיות על ' . ( $kinds[ $k ] ?? '' ) . ' לא יגיעו עד ' . wp_date( 'j.n', time() + 30 * DAY_IN_SECONDS ) . '. כל אחת תופיע במייל הבוקר.', 'unmute', 'בטל את ההשתקה' ),
			'unmute'    => array( 'ההשתקה בוטלה', 'התראות על ' . ( $kinds[ $k ] ?? '' ) . ' יגיעו שוב מיד.', 'mute', 'השתק שוב' ),
		)[ $a ];
		$body = ( $lead_act ? nadlan_omx_page_lead( $l ) : '' ) . '<p>' . esc_html( $done[1] ) . '</p>' . ( $done[2] ? nadlan_omx_form( $done[2], $l, $k, $done[3], 'alt' ) : '' );
		nadlan_omx_page( $done[0], $body );
	}

	/* ---------- one mail per lead: hold the plain copies when the card is on its way ---------- */
	add_filter( 'pre_wp_mail', function ( $ret, $atts ) {
		if ( null !== $ret || ! is_array( $atts ) ) { return $ret; }
		$admin = (string) get_option( 'admin_email' );
		$to    = is_array( $atts['to'] ?? '' ) ? implode( ',', $atts['to'] ) : (string) ( $atts['to'] ?? '' );
		$subj  = (string) ( $atts['subject'] ?? '' );
		if ( '' === $admin || false === stripos( $to, $admin ) ) { return $ret; }
		if ( 0 !== strpos( $subj, '[נדלן] ליד חדש - ' ) && 0 !== strpos( $subj, '[Concierge] פנייה חדשה - ' ) ) { return $ret; }
		if ( ! preg_match( '/post\.php\?post=(\d+)&action=edit/', (string) ( $atts['message'] ?? '' ), $mm ) ) { return $ret; }
		$lid = (int) $mm[1];
		if ( 'nadlan_lead' !== get_post_type( $lid ) || ! wp_next_scheduled( 'nadlan_lead_rich_alert', array( $lid ) ) ) { return $ret; }
		nadlan_omx_log( 'dup', $subj, 'held' );
		return true;
	}, 10, 2 );

	/* ---------- the morning numbers ---------- */
	/** Rows: label, yesterday, the day before, the last 7 days, the action url and label. Google rows only when fresh. */
	function nadlan_omx_kpis( $y ) {
		global $wpdb;
		$p   = wp_date( 'Y-m-d', strtotime( $y . ' 12:00:00' ) - DAY_IN_SECONDS );
		$w0  = wp_date( 'Y-m-d', strtotime( $y . ' 12:00:00' ) - 6 * DAY_IN_SECONDS );
		$lead = function ( $a, $b, $pa ) use ( $wpdb ) {
			return (int) $wpdb->get_var( $wpdb->prepare( "SELECT COUNT(DISTINCT p.ID) FROM {$wpdb->posts} p LEFT JOIN {$wpdb->postmeta} u ON u.post_id = p.ID AND u.meta_key = 'utm_source'
				WHERE p.post_type = 'nadlan_lead' AND p.post_status NOT IN ('trash','auto-draft') AND p.post_date BETWEEN %s AND %s AND "
				. ( $pa ? "u.meta_value = 'price_alert'" : "(u.meta_value IS NULL OR u.meta_value <> 'price_alert')" ), $a . ' 00:00:00', $b . ' 23:59:59' ) );
		};
		$na = function ( $a, $b ) use ( $wpdb ) {
			return (int) $wpdb->get_var( $wpdb->prepare( "SELECT COUNT(DISTINCT p.ID) FROM {$wpdb->posts} p
				JOIN {$wpdb->postmeta} k ON k.post_id = p.ID AND k.meta_key = 'kind' AND k.meta_value = 'nf'
				JOIN {$wpdb->postmeta} c ON c.post_id = p.ID AND c.meta_key = 'confirmed' AND c.meta_value = '1'
				WHERE p.post_type = 'nadlan_saved_search' AND p.post_date BETWEEN %s AND %s", $a . ' 00:00:00', $b . ' 23:59:59' ) );
		};
		$t  = $wpdb->prefix . 'nadlan_pview';
		$pv = function ( $a, $b, $ev ) use ( $wpdb, $t ) {
			return (int) $wpdb->get_var( $wpdb->prepare( "SELECT COUNT(*) FROM $t WHERE day BETWEEN %s AND %s AND ev " . ( 'tap' === $ev ? "IN ('wa','tel')" : "= 'view'" ), $a, $b ) );
		};
		$rows = array(
			array( 'לידים', $lead( $y, $y, false ), $lead( $p, $p, false ), $lead( $w0, $y, false ), admin_url( 'edit.php?post_type=nadlan_lead' ), 'לרשימת הלידים' ),
			array( 'נרשמים לעדכוני מחירים', $lead( $y, $y, true ), $lead( $p, $p, true ), $lead( $w0, $y, true ), admin_url( 'options-general.php?page=nadlan-nudge' ), 'לרשימה (Excel)' ),
			array( 'מנויים להתראות אזור', $na( $y, $y ), $na( $p, $p ), $na( $w0, $y ), admin_url( 'options-general.php?page=nadlan-mail' ), 'להגדרות ההתראות' ),
			array( 'צפיות בנכסים', $pv( $y, $y, 'view' ), $pv( $p, $p, 'view' ), $pv( $w0, $y, 'view' ), admin_url( 'admin.php?page=nadlan-inbox' ), 'לתיבה' ),
			array( 'לחיצות וואטסאפ וטלפון בנכסים', $pv( $y, $y, 'tap' ), $pv( $p, $p, 'tap' ), $pv( $w0, $y, 'tap' ), admin_url( 'admin.php?page=nadlan-inbox' ), 'לתיבה' ),
		);
		$resp = function ( $a, $b ) use ( $wpdb ) {
			$m = array();
			foreach ( (array) $wpdb->get_results( $wpdb->prepare( "SELECT p.post_date_gmt d, f.meta_value r FROM {$wpdb->posts} p JOIN {$wpdb->postmeta} f ON f.post_id = p.ID AND f.meta_key = 'lead_first_response_at'
				WHERE p.post_type = 'nadlan_lead' AND p.post_status NOT IN ('trash','auto-draft') AND p.post_date BETWEEN %s AND %s", $a . ' 00:00:00', $b . ' 23:59:59' ) ) as $x ) {
				$s = (int) $x->r - (int) strtotime( $x->d . ' UTC' );
				if ( (int) $x->r > 0 && $s >= 0 ) { $m[] = $s; }
			}
			return $m ? (int) round( array_sum( $m ) / count( $m ) / 60 ) : null;
		};
		$ry = $resp( $y, $y ); $rp = $resp( $p, $p ); $rw = $resp( $w0, $y );
		if ( null !== $ry || null !== $rp ) {
			$rows[] = array( 'זמן חזרה ממוצע לליד (דקות)', (int) $ry, (int) $rp, (int) $rw, admin_url( 'edit.php?post_type=nadlan_lead' ), 'לרשימת הלידים', true );
		}
		if ( function_exists( 'wc_get_orders' ) ) {
			$rev = function ( $a, $b ) {
				try {
					$s = ( new DateTime( $a . ' 00:00:00', wp_timezone() ) )->getTimestamp();
					$f = ( new DateTime( $b . ' 23:59:59', wp_timezone() ) )->getTimestamp();
					$sum = 0.0;
					foreach ( (array) wc_get_orders( array( 'limit' => 200, 'status' => array( 'wc-processing', 'wc-completed' ), 'date_paid' => $s . '...' . $f ) ) as $o ) { $sum += (float) $o->get_total(); }
					return (int) round( $sum );
				} catch ( Exception $e ) { return 0; }
			};
			$rows[] = array( 'הכנסות (₪)', $rev( $y, $y ), $rev( $p, $p ), $rev( $w0, $y ), admin_url( 'admin.php?page=wc-orders' ), 'להזמנות' );
		}
		$g = (array) get_option( 'nadlan_omx_gsc', array() );
		$d = (array) ( $g['days'] ?? array() );
		if ( count( $d ) >= 2 && ! empty( $g['at'] ) && (int) $g['at'] > time() - 3 * DAY_IN_SECONDS ) {
			ksort( $d );
			$keys = array_keys( $d );
			$last = end( $keys );
			$prev = $keys[ count( $keys ) - 2 ];
			$c7   = 0;
			foreach ( array_slice( $keys, -7 ) as $kk ) { $c7 += (int) $d[ $kk ]['c']; }
			$rows[] = array( 'קליקים מגוגל (' . wp_date( 'j.n', strtotime( $last . ' 12:00:00' ) ) . ', הנתון האחרון שגוגל פרסם)', (int) $d[ $last ]['c'], (int) $d[ $prev ]['c'], $c7,
				'https://search.google.com/search-console/performance/search-analytics?resource_id=sc-domain%3Anad-lan.co.il', 'ל־Search Console' );
			$rows[] = array( 'הופעות בגוגל', (int) $d[ $last ]['i'], (int) $d[ $prev ]['i'], array_sum( array_map( function ( $kk ) use ( $d ) { return (int) $d[ $kk ]['i']; }, array_slice( $keys, -7 ) ) ),
				'https://search.google.com/search-console/performance/search-analytics?resource_id=sc-domain%3Anad-lan.co.il', 'ל־Search Console' );
		}
		return $rows;
	}
	function nadlan_omx_delta( $a, $b, $lower_is_better = false ) {
		$d = (int) $a - (int) $b;
		if ( 0 === $d ) { return '<span style="color:#5E6A75">ללא שינוי</span>'; }
		$pct  = (int) $b > 0 && abs( $d ) >= 10 ? ' (' . ( $d > 0 ? '+' : '' ) . (int) round( 100 * $d / (int) $b ) . '%)' : '';
		$good = $lower_is_better ? $d < 0 : $d > 0;
		return '<span dir="ltr" style="color:' . ( $good ? '#0F7A63' : '#B42318' ) . ';font-weight:700">' . ( $d > 0 ? '▲ +' : '▼ ' ) . number_format_i18n( $d ) . $pct . '</span>';
	}

	/* ---------- the GSC push from the owner's computer, a sample send, the preview ---------- */
	function nadlan_omx_metrics_route( WP_REST_Request $req ) {
		$p = $req->get_json_params();
		$days = array();
		foreach ( (array) ( is_array( $p ) ? ( $p['gsc'] ?? array() ) : array() ) as $d => $v ) {
			if ( preg_match( '/^\d{4}-\d{2}-\d{2}$/', (string) $d ) && is_array( $v ) ) { $days[ (string) $d ] = array( 'c' => (int) ( $v['clicks'] ?? 0 ), 'i' => (int) ( $v['impressions'] ?? 0 ) ); }
		}
		if ( ! $days ) { return new WP_Error( 'empty', 'empty', array( 'status' => 422 ) ); }
		$old = (array) get_option( 'nadlan_omx_gsc', array() );
		$all = array_merge( (array) ( $old['days'] ?? array() ), $days );
		ksort( $all );
		$all = array_slice( $all, -60, null, true );
		update_option( 'nadlan_omx_gsc', array( 'days' => $all, 'at' => time() ), false );
		return array( 'ok' => true, 'days' => count( $all ), 'last' => array_key_last( $all ) );
	}
	function nadlan_omx_sample_route( WP_REST_Request $req ) {
		$w = sanitize_key( (string) $req->get_param( 'which' ) );
		if ( 'lead' === $w ) {
			$l = absint( $req->get_param( 'l' ) );
			if ( ! $l ) { // l=0: the latest lead already handled (contacted, won or lost), so a test never touches an open lead
				$h = get_posts( array( 'post_type' => 'nadlan_lead', 'post_status' => 'any', 'numberposts' => 1, 'fields' => 'ids',
					'meta_query' => array( array( 'key' => 'lead_status', 'value' => array( 'contacted', 'won', 'lost' ), 'compare' => 'IN' ) ) ) );
				$l = $h ? (int) $h[0] : 0;
			}
			return array( 'ok' => 'nadlan_lead' === get_post_type( $l ) && nadlan_omx_lead_alert( $l, true ), 'lead' => $l, 'status' => nadlan_omx_m( $l, 'lead_status' ) );
		}
		if ( 'morning' === $w && function_exists( 'nadlan_om_send' ) ) {
			$h = nadlan_om_send( true, (string) $req->get_param( 'day' ), false );
			return array( 'ok' => '' !== $h, 'bytes' => strlen( $h ) );
		}
		return new WP_Error( 'which', 'which', array( 'status' => 422 ) );
	}
	add_action( 'rest_api_init', function () {
		register_rest_route( 'nadlan/v1', '/om-act', array( 'methods' => array( 'GET', 'POST' ), 'permission_callback' => '__return_true', 'callback' => 'nadlan_omx_act_route' ) );
		$admin = function () { return current_user_can( 'manage_options' ); };
		register_rest_route( 'nadlan/v1', '/om-metrics', array( 'methods' => 'POST', 'permission_callback' => $admin, 'callback' => 'nadlan_omx_metrics_route' ) );
		register_rest_route( 'nadlan/v1', '/om-sample', array( 'methods' => 'POST', 'permission_callback' => $admin, 'callback' => 'nadlan_omx_sample_route' ) );
		register_rest_route( 'nadlan/v1', '/om-lead-preview', array( 'methods' => 'GET', 'permission_callback' => $admin, 'callback' => function ( $r ) {
			$l = absint( $r->get_param( 'l' ) );
			if ( 'nadlan_lead' !== get_post_type( $l ) ) { return new WP_Error( 'lead', 'lead', array( 'status' => 404 ) ); }
			list( $html, $text, $subj ) = nadlan_omx_lead_mail( $l );
			return array( 'subject' => $subj, 'html' => $html, 'text' => $text, 'heat' => nadlan_omx_heat( $l ), 'status' => nadlan_omx_m( $l, 'lead_status' ),
				'snooze' => nadlan_omx_m( $l, 'lead_omx_snooze' ), 'first_response_via' => nadlan_omx_m( $l, 'lead_first_response_via' ),
				'mutes' => (array) get_option( 'nadlan_omx_mute', array() ), 'log' => array_slice( (array) get_option( 'nadlan_omx_log', array() ), 0, 8 ) );
		} ) );
	} );
	add_filter( 'nadlan_hardening_public_post_routes', function ( $r ) { $r[] = '#^/nadlan/v1/om-act$#'; return $r; } );

	/* ---------- the dashboard widget: what was sent, held, muted ---------- */
	add_action( 'wp_dashboard_setup', function () {
		if ( ! current_user_can( 'manage_options' ) ) { return; }
		wp_add_dashboard_widget( 'nadlan_omx', 'מיילים לבעלים', function () {
			$res = array( 'sent' => 'נשלח', 'failed' => 'נכשל', 'held' => 'עותק כפול נעצר', 'muted' => 'מושתק, במייל הבוקר', 'action' => 'פעולה מהמייל', 'skipped_empty' => 'בוקר בלי חדש, לא נשלח', 'skipped_repeat' => 'בוקר זהה לאתמול, לא נשלח' );
			echo '<table class="widefat striped" style="font-size:12px"><tbody>';
			foreach ( array_slice( (array) get_option( 'nadlan_omx_log', array() ), 0, 15 ) as $x ) {
				echo '<tr><td style="white-space:nowrap">' . esc_html( wp_date( 'j.n H:i', (int) $x['t'] ) ) . '</td><td>' . esc_html( $res[ $x['r'] ] ?? $x['r'] ) . '</td><td>' . esc_html( $x['s'] ) . '</td></tr>';
			}
			echo '</tbody></table>';
			$m = array_filter( (array) get_option( 'nadlan_omx_mute', array() ), function ( $t ) { return (int) $t > time(); } );
			$kinds = nadlan_omx_kinds();
			foreach ( $m as $k => $t ) { echo '<p>מושתק עד ' . esc_html( wp_date( 'j.n', (int) $t ) ) . ': ' . esc_html( $kinds[ $k ] ?? $k ) . ' · <a href="' . esc_url( nadlan_omx_url( 'unmute', 0, $k ) ) . '">בטל</a></p>'; }
		} );
	} );
}
