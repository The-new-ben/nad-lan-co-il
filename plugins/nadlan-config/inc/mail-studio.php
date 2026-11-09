<?php
/**
 * Mail studio, "דיוור נדל״ן" (HAD-687 part 2, Ben 9.11.2026 by voice: "תכין לי מייל שיהיה מקצועי ברמות הכי גבוהות ... ותעשה לי פלטפורמה
 * שאני יכול לשלוח את המיילים האלה, גם לעשות הפצות ... אל תעשה לי משהו נקודתי"). Loaded from inc/alerts.php. Claude Design: DS
 * component NadLanEmail. Research and the counted comparison: docs/research/2026-11-09-nadlan-email-system/.
 *
 * - Write: a personal mail to one person, or a distribution to the consented list; three looks (letter, listings, update); listings
 *   and projects picked by link or number become cards with their real facts (an unknown fact is left out); a live preview on a phone
 *   and a desktop width; a test to yourself first.
 * - Lists: a distribution goes only to people with a recorded advertising consent: the price window's consent line ("עדכוני מחירים
 *   ופרסומים") or an imported list whose consent the owner confirms. Ordinary leads (consent to handle their inquiry) and area-alert
 *   subscribers are service contacts and never get an advertisement.
 * - Israeli Communications Law 30A: a distribution carries "פרסומת" first in its subject and at the top of the mail, the sender's name
 *   and contact, and a refusal link honoured at once. Gmail/Yahoo bulk rules: List-Unsubscribe + List-Unsubscribe-Post (RFC 8058) on
 *   every distribution mail; the link opens a confirm page, a mail app's one-click POST unsubscribes at once.
 * - Businesses (1.72.622, Ben 9.11: "מערך ... ליזמים, למתווכים, לבעלי מקצוע"): a business address may get ONE invitation asking whether it
 *   agrees to receive offers (section 30A(ג)); the invitation carries no pitch and no film, only the question and two signed buttons.
 *   "כן" records the consent (wording, time) and tells the owner; "לא" or no answer = never mailed again. The offer with the film goes
 *   only to those who said yes, as a distribution with "פרסומת" in the subject.
 * - Sending: wp_mail, so through Brevo once its key is saved (inc/mailer.php). A queue sends at most N a minute and a daily cap
 *   (Brevo's free plan is 300 a day for the whole site). Brevo's log keeps deliveries, opens and clicks.
 */
if ( ! defined( 'ABSPATH' ) ) { exit; }

if ( ! function_exists( 'nadlan_ms_opt' ) ) {

	/* ---------- settings ---------- */
	function nadlan_ms_opt( $k = null ) {
		$u = wp_get_current_user();
		$d = array(
			'from_name' => 'נדל״ן',
			'reply_to'  => (string) get_option( 'admin_email' ),
			'sig_name'  => $u && $u->exists() ? (string) $u->display_name : 'נדל״ן',
			'sig_role'  => 'נדל״ן · מידע ונתונים על נדל״ן בישראל',
			'sig_phone' => '',
			'sig_wa'    => '',
			'sig_photo' => '',
			'biz_line'  => 'נדל״ן (nad-lan.co.il) · info@nad-lan.co.il',
			'per_min'   => 20,
			'day_cap'   => 250,
		);
		$o = wp_parse_args( (array) get_option( 'nadlan_ms_opts', array() ), $d );
		return null === $k ? $o : ( $o[ $k ] ?? '' );
	}

	/* ---------- tables ---------- */
	function nadlan_ms_t( $n ) { global $wpdb; return $wpdb->prefix . 'nadlan_ms_' . $n; }
	function nadlan_ms_db() {
		if ( '3' === get_option( 'nadlan_ms_db' ) ) { return; }
		global $wpdb;
		require_once ABSPATH . 'wp-admin/includes/upgrade.php';
		$c = $wpdb->get_charset_collate();
		dbDelta( 'CREATE TABLE ' . nadlan_ms_t( 'contacts' ) . " (
			id bigint(20) unsigned NOT NULL AUTO_INCREMENT,
			email varchar(190) NOT NULL,
			name varchar(120) NOT NULL DEFAULT '',
			source varchar(80) NOT NULL DEFAULT '',
			consent varchar(10) NOT NULL DEFAULT 'service',
			consent_text text NULL,
			consent_at datetime NULL,
			unsub_at datetime NULL,
			kind varchar(12) NOT NULL DEFAULT 'client',
			company varchar(120) NOT NULL DEFAULT '',
			invited_at datetime NULL,
			answer varchar(6) NOT NULL DEFAULT '',
			answered_at datetime NULL,
			created_at datetime NOT NULL,
			PRIMARY KEY  (id),
			UNIQUE KEY email (email)
		) $c;" );
		dbDelta( 'CREATE TABLE ' . nadlan_ms_t( 'queue' ) . " (
			id bigint(20) unsigned NOT NULL AUTO_INCREMENT,
			campaign bigint(20) unsigned NOT NULL,
			email varchar(190) NOT NULL,
			name varchar(120) NOT NULL DEFAULT '',
			status varchar(10) NOT NULL DEFAULT 'wait',
			err varchar(190) NOT NULL DEFAULT '',
			sent_at datetime NULL,
			PRIMARY KEY  (id),
			KEY camp (campaign,status)
		) $c;" );
		update_option( 'nadlan_ms_db', '3', false );
	}
	add_action( 'admin_init', 'nadlan_ms_db' );

	add_action( 'init', function () {
		register_post_type( 'nadlan_ms_campaign', array( 'public' => false, 'show_ui' => false, 'label' => 'דיוור', 'supports' => array( 'title' ) ) );
	} );

	/* ---------- the text: blank line = paragraph, "- " = bullet, "## " = subheading, **bold**, links; {שם} = the first name ---------- */
	function nadlan_ms_text( $raw, $first ) {
		$raw   = str_replace( array( "\r\n", "\r" ), "\n", (string) $raw );
		$raw   = str_replace( array( '{שם}', '{name}' ), "\x01", $raw );
		$raw   = str_replace( array( '{חברה}', '{company}' ), (string) ( $GLOBALS['nadlan_ms_company'] ?? '' ), $raw );
		$P     = 'margin:0 0 16px;font-size:17px;line-height:28px;color:#23313B';
		$inline = function ( $s ) use ( $first ) {
			$s = esc_html( $s );
			$s = preg_replace( '/\*\*(.+?)\*\*/u', '<strong style="color:#12202A">$1</strong>', $s );
			$s = preg_replace_callback( '#\bhttps?://[^\s<]+#u', function ( $m ) {
				$u = rtrim( html_entity_decode( $m[0] ), '.,;)' );
				return '<a href="' . esc_url( $u ) . '" style="color:#1F4B5C;text-decoration:underline">' . esc_html( preg_replace( '#^https?://(www\.)?#', '', rawurldecode( $u ) ) ) . '</a>';
			}, $s );
			return str_replace( "\x01", esc_html( $first ), $s );
		};
		$out = '';
		foreach ( preg_split( "/\n\s*\n/", trim( $raw ) ) as $blk ) {
			$lines = array_values( array_filter( array_map( 'trim', explode( "\n", $blk ) ), 'strlen' ) );
			if ( ! $lines ) { continue; }
			if ( 0 === strpos( $lines[0], '## ' ) ) {
				$out .= '<h2 style="margin:24px 0 10px;font-size:21px;line-height:28px;font-weight:800;color:#12202A">' . $inline( substr( $lines[0], 3 ) ) . '</h2>';
				array_shift( $lines );
				if ( ! $lines ) { continue; }
			}
			if ( count( array_filter( $lines, function ( $l ) { return 0 === strpos( $l, '- ' ); } ) ) === count( $lines ) ) {
				$out .= '<ul style="margin:0 0 16px;padding:0 22px 0 0;font-size:17px;line-height:28px;color:#23313B">';
				foreach ( $lines as $l ) { $out .= '<li style="margin:0 0 6px">' . $inline( substr( $l, 2 ) ) . '</li>'; }
				$out .= '</ul>';
			} else {
				$out .= '<p style="' . $P . '">' . implode( '<br>', array_map( $inline, $lines ) ) . '</p>';
			}
		}
		return $out;
	}

	/* ---------- listings and projects as cards (real facts only; an unknown fact is left out) ---------- */
	function nadlan_ms_resolve( $raw ) {
		$ids = array();
		foreach ( preg_split( '/[\s,]+/', (string) $raw ) as $t ) {
			$t = trim( $t );
			if ( '' === $t ) { continue; }
			$id = ctype_digit( $t ) ? (int) $t : url_to_postid( $t );
			$p  = $id ? get_post( $id ) : null;
			if ( $p && 'publish' === $p->post_status && in_array( $p->post_type, array( 'nadlan_property', 'nadlan_project', 'nadlan_intl' ), true ) ) { $ids[] = $id; }
		}
		return array_slice( array_values( array_unique( $ids ) ), 0, 6 );
	}
	function nadlan_ms_item( $id ) {
		$m   = function ( $k ) use ( $id ) { return trim( (string) get_post_meta( $id, $k, true ) ); };
		$img = (string) get_the_post_thumbnail_url( $id, 'large' );
		if ( '' === $img && function_exists( 'nadlan_nf_thumbs' ) ) { $th = nadlan_nf_thumbs( array( $id ) ); $img = (string) ( $th[ $id ] ?? '' ); }
		$facts = array();
		$price = '';
		if ( 'nadlan_property' === get_post_type( $id ) ) {
			$where = trim( $m( 'neighborhood' ) . ( $m( 'neighborhood' ) && $m( 'city' ) ? ', ' : '' ) . $m( 'city' ) );
			if ( '' !== $where ) { $facts[] = $where; }
			if ( (float) $m( 'rooms' ) > 0 ) { $facts[] = rtrim( rtrim( number_format( (float) $m( 'rooms' ), 1 ), '0' ), '.' ) . ' חדרים'; }
			if ( (float) $m( 'size_sqm' ) > 0 ) { $facts[] = (int) round( (float) $m( 'size_sqm' ) ) . ' מ״ר'; }
			$pr = (float) preg_replace( '/[^\d.]/', '', $m( 'price' ) );
			if ( $pr > 0 ) { $price = number_format( $pr ) . ' ₪' . ( 'rent' === $m( 'listing_type' ) ? ' לחודש' : '' ); }
		} else {
			if ( '' !== $m( 'city' ) ) { $facts[] = $m( 'city' ); }
			if ( '' !== $m( 'developer_name' ) ) { $facts[] = 'יזם: ' . $m( 'developer_name' ); }
			if ( (int) $m( 'num_units' ) > 0 ) { $facts[] = (int) $m( 'num_units' ) . ' יח״ד'; }
			$pm = (float) preg_replace( '/[^\d.]/', '', $m( 'price_min' ) );
			if ( $pm > 0 ) { $price = 'החל מ־' . number_format( $pm ) . ' ₪'; }
		}
		return array( 'title' => wp_strip_all_tags( html_entity_decode( get_the_title( $id ), ENT_QUOTES, 'UTF-8' ) ), 'url' => get_permalink( $id ), 'img' => $img, 'facts' => $facts, 'price' => $price );
	}

	/* ---------- the mail (NadLanEmail v1): 600px single column, RTL, one primary button, accessible, light and dark ---------- */
	function nadlan_ms_btn( $url, $label, $primary = true ) {
		$bg = $primary ? '#2F6F86' : '#FFFFFF'; $fg = $primary ? '#FFFFFF' : '#1F4B5C'; $bd = $primary ? '#2F6F86' : '#2F6F86';
		return '<table role="presentation" cellpadding="0" cellspacing="0" style="margin:8px 0 8px auto"><tr><td style="border-radius:8px;background:' . $bg . '">'
			. '<a href="' . esc_url( $url ) . '" style="display:inline-block;padding:15px 28px;border:1px solid ' . $bd . ';border-radius:8px;font-size:' . ( $primary ? '18px' : '16px' ) . ';line-height:22px;font-weight:700;color:' . $fg . ';text-decoration:none">' . esc_html( $label ) . '</a></td></tr></table>';
	}
	/**
	 * $f: look (letter|listings|update), subject, pre, title, greeting, body, figure, figure_cap, items, cta_text, cta_url, sign (bool), ad (bool)
	 * $first: the recipient's first name ('' when unknown); $unsub: the refusal link (distribution only) or ''
	 */
	function nadlan_ms_render( $f, $first = '', $unsub = '', $ctx = array() ) {
		$o     = nadlan_ms_opt();
		$GLOBALS['nadlan_ms_company'] = (string) ( $ctx['company'] ?? '' );
		$invite = 'invite' === ( $f['kind'] ?? '' );
		$look  = in_array( $f['look'] ?? '', array( 'letter', 'listings', 'update' ), true ) ? $f['look'] : 'letter';
		$ad    = ! empty( $f['ad'] );
		$subj  = (string) ( $f['subject'] ?? '' );
		$font  = "Assistant,'Segoe UI',Arial,Helvetica,sans-serif";
		$greet = trim( str_replace( array( '{שם}', '{name}', '{חברה}', '{company}' ), array( $first, $first, (string) ( $ctx['company'] ?? '' ), (string) ( $ctx['company'] ?? '' ) ), (string) ( $f['greeting'] ?? '' ) ) );
		$greet = preg_replace( '/\s+,/u', ',', preg_replace( '/\s{2,}/u', ' ', $greet ) );
		$logo  = function_exists( 'get_site_icon_url' ) ? (string) get_site_icon_url( 96 ) : '';
		$rows  = '';
		if ( $ad ) { $rows .= '<tr><td class="px" style="padding:18px 32px 0"><span style="display:inline-block;padding:2px 10px;border:1px solid #C5CFD7;border-radius:999px;font-size:12px;line-height:18px;color:#5E6A75">פרסומת</span></td></tr>'; }
		if ( 'update' === $look && '' !== trim( (string) ( $f['figure'] ?? '' ) ) ) {
			$rows .= '<tr><td class="px" style="padding:22px 32px 0"><table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:#10262F;border-radius:10px"><tr><td style="padding:20px 22px">'
				. '<div dir="ltr" style="text-align:right;font-size:44px;line-height:48px;font-weight:800;color:#FFFFFF">' . esc_html( $f['figure'] ) . '</div>'
				. '<div style="font-size:15px;line-height:22px;color:#CFE3EA;margin-top:4px">' . esc_html( (string) ( $f['figure_cap'] ?? '' ) ) . '</div></td></tr></table></td></tr>';
		}
		if ( '' !== trim( (string) ( $f['title'] ?? '' ) ) ) {
			$rows .= '<tr><td class="px" style="padding:26px 32px 4px"><h1 class="h1 ink" style="margin:0;font-size:30px;line-height:38px;font-weight:800;color:#12202A">' . esc_html( $f['title'] ) . '</h1></td></tr>';
		}
		$rows .= '<tr><td class="px ink" style="padding:18px 32px 4px;font-size:17px;line-height:28px;color:#23313B">'
			. ( '' !== $greet ? '<p style="margin:0 0 16px;font-size:17px;line-height:28px;color:#23313B">' . esc_html( $greet ) . '</p>' : '' )
			. nadlan_ms_text( $f['body'] ?? '', $first ) . '</td></tr>';
		if ( ! empty( $f['film'] ) && ! $invite ) { // the film: a large poster that opens the film's page, then a clear button (mail apps do not play video)
			$fu = (string) ( $f['film_url'] ?? '' ); $fp = (string) ( $f['film_poster'] ?? '' );
			$rows .= '<tr><td class="px" style="padding:8px 32px 6px"><a href="' . esc_url( $fu ) . '"><img src="' . esc_url( $fp ) . '" width="534" alt="' . esc_attr( '' !== trim( (string) ( $f['film_cap'] ?? '' ) ) ? $f['film_cap'] : 'הסרטון של נדל״ן' ) . '" style="display:block;width:100%;max-width:534px;height:auto;border:0;border-radius:10px"></a>'
				. nadlan_ms_btn( $fu, '▶ לצפייה בסרטון', false )
				. ( '' !== trim( (string) ( $f['film_cap'] ?? '' ) ) ? '<div class="mute" style="font-size:14px;line-height:20px;color:#5E6A75">' . esc_html( $f['film_cap'] ) . '</div>' : '' ) . '</td></tr>';
		}
		if ( $invite ) { // the one question, two signed answers
			$rows .= '<tr><td class="px" style="padding:6px 32px 18px"><table role="presentation" cellpadding="0" cellspacing="0" style="margin:0 0 0 auto"><tr><td style="padding:0 0 0 10px">'
				. nadlan_ms_btn( (string) ( $ctx['yes'] ?? '#' ), 'כן, אשמח לקבל' ) . '</td><td>' . nadlan_ms_btn( (string) ( $ctx['no'] ?? '#' ), 'לא, תודה', false ) . '</td></tr></table></td></tr>';
		}
		foreach ( (array) ( $f['items'] ?? array() ) as $id ) {
			$it = nadlan_ms_item( (int) $id );
			$rows .= '<tr><td class="px" style="padding:6px 32px 14px"><table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="border:1px solid #E3E8EC;border-radius:10px;overflow:hidden">'
				. ( $it['img'] ? '<tr><td><a href="' . esc_url( $it['url'] ) . '"><img src="' . esc_url( $it['img'] ) . '" width="534" alt="' . esc_attr( $it['title'] ) . '" style="display:block;width:100%;max-width:534px;height:auto;border:0;border-radius:10px 10px 0 0"></a></td></tr>' : '' )
				. '<tr><td style="padding:16px 18px">'
				. '<div class="ink" style="font-size:20px;line-height:26px;font-weight:700;color:#12202A">' . esc_html( $it['title'] ) . '</div>'
				. ( $it['facts'] ? '<div class="mute" style="font-size:15px;line-height:22px;color:#5E6A75;margin-top:4px">' . esc_html( implode( ' · ', $it['facts'] ) ) . '</div>' : '' )
				. ( '' !== $it['price'] ? '<div dir="rtl" class="ink" style="font-size:22px;line-height:28px;font-weight:800;color:#12202A;margin-top:8px">' . esc_html( $it['price'] ) . '</div>' : '' )
				. '<div style="margin-top:10px"><a href="' . esc_url( $it['url'] ) . '" style="font-size:16px;font-weight:700;color:#1F4B5C">לכל הפרטים ←</a></div>'
				. '</td></tr></table></td></tr>';
		}
		if ( '' !== trim( (string) ( $f['cta_text'] ?? '' ) ) && '' !== trim( (string) ( $f['cta_url'] ?? '' ) ) ) {
			$rows .= '<tr><td class="px" style="padding:8px 32px 18px">' . nadlan_ms_btn( $f['cta_url'], $f['cta_text'] ) . '</td></tr>';
		}
		if ( ! empty( $f['sign'] ) ) {
			$wa  = preg_replace( '/\D+/', '', (string) $o['sig_wa'] );
			if ( $wa && 0 === strpos( $wa, '0' ) ) { $wa = '972' . substr( $wa, 1 ); }
			$ph  = preg_replace( '/[^\d+]/', '', (string) $o['sig_phone'] );
			$lnk = array_filter( array(
				$ph ? '<a href="' . esc_url( 'tel:' . $ph, array( 'tel' ) ) . '" style="color:#1F4B5C;text-decoration:none" dir="ltr">' . esc_html( $o['sig_phone'] ) . '</a>' : '',
				$wa ? '<a href="https://wa.me/' . esc_attr( $wa ) . '" style="color:#0F7A63;text-decoration:none">וואטסאפ</a>' : '',
				'<a href="' . esc_url( home_url( '/' ) ) . '" style="color:#1F4B5C;text-decoration:none">nad-lan.co.il</a>',
			) );
			$rows .= '<tr><td class="px" style="padding:6px 32px 24px"><table role="presentation" cellpadding="0" cellspacing="0" style="border-top:1px solid #E3E8EC;padding-top:16px;width:100%"><tr>'
				. ( $o['sig_photo'] ? '<td width="72" valign="top" style="padding:16px 0 0 14px"><img src="' . esc_url( $o['sig_photo'] ) . '" width="64" height="64" alt="' . esc_attr( $o['sig_name'] ) . '" style="display:block;width:64px;height:64px;border-radius:50%;border:0"></td>' : '' )
				. '<td valign="top" style="padding-top:16px"><div class="ink" style="font-size:17px;line-height:24px;font-weight:700;color:#12202A">' . esc_html( $o['sig_name'] ) . '</div>'
				. '<div class="mute" style="font-size:14px;line-height:20px;color:#5E6A75">' . esc_html( $o['sig_role'] ) . '</div>'
				. '<div style="font-size:15px;line-height:22px;margin-top:6px">' . implode( ' &nbsp;·&nbsp; ', $lnk ) . '</div></td></tr></table></td></tr>';
		}
		$foot = $invite
			? 'שלחנו את ההודעה הזאת פעם אחת בלבד' . ( ! empty( $ctx['company'] ) ? ', לכתובת העסקית של ' . esc_html( $ctx['company'] ) : '' ) . '. אם לא תענו, לא נפנה שוב. ' . ( $unsub ? '<a href="' . esc_url( $unsub ) . '" style="color:#3E4C58;text-decoration:underline">להסרה</a>.' : '' )
			: ( $ad
			? 'קיבלת את המייל כי נרשמת לעדכונים ולפרסומים מנדל״ן. ' . ( $unsub ? '<a href="' . esc_url( $unsub ) . '" style="color:#3E4C58;text-decoration:underline">להסרה מרשימת התפוצה</a>' : 'להסרה מרשימת התפוצה: הקישור האישי יופיע כאן' ) . '. ההסרה מיידית.'
			: 'המייל נשלח אליך באופן אישי מנדל״ן. אפשר פשוט להשיב למייל הזה.' );
		$pre = str_replace( array( '{שם}', '{name}', '{חברה}', '{company}' ), array( $first, $first, (string) ( $ctx['company'] ?? '' ), (string) ( $ctx['company'] ?? '' ) ), (string) ( $f['pre'] ?? '' ) );
		return '<!doctype html><html lang="he" dir="rtl" xmlns="http://www.w3.org/1999/xhtml"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
			. '<meta name="x-apple-disable-message-reformatting"><meta name="color-scheme" content="light dark"><meta name="supported-color-schemes" content="light dark"><title>' . esc_html( $subj ) . '</title>'
			. '<link href="https://fonts.googleapis.com/css2?family=Assistant:wght@400;700;800&amp;display=swap" rel="stylesheet">'
			. '<style>body{margin:0;padding:0}a{color:#1F4B5C}@media (max-width:620px){.px{padding-left:20px!important;padding-right:20px!important}.h1{font-size:26px!important;line-height:33px!important}}'
			. '@media (prefers-color-scheme:dark){.bg{background:#0B1A20!important}.card{background:#13262E!important}.ink,.ink p,.ink li{color:#E8EEF1!important}.mute{color:#AAB7BF!important}}</style></head>'
			. '<body class="bg" style="margin:0;padding:0;background:#EEF2F4;font-family:' . $font . '">'
			. '<div style="display:none;max-height:0;overflow:hidden;opacity:0;color:transparent">' . esc_html( $pre ) . str_repeat( '&#847;&zwnj;&nbsp;', 110 ) . '</div>'
			. '<div role="article" aria-roledescription="email" aria-label="' . esc_attr( $subj ) . '" lang="he" dir="rtl">'
			. '<table role="presentation" width="100%" cellpadding="0" cellspacing="0" class="bg" style="background:#EEF2F4"><tr><td align="center" style="padding:24px 10px">'
			. '<table role="presentation" width="100%" cellpadding="0" cellspacing="0" dir="rtl" style="max-width:600px;text-align:right;font-family:' . $font . '">'
			. '<tr><td style="background:#10262F;border-radius:12px 12px 0 0;padding:16px 32px" class="px"><table role="presentation" width="100%" cellpadding="0" cellspacing="0"><tr>'
			. '<td style="vertical-align:middle">' . ( $logo ? '<img src="' . esc_url( $logo ) . '" width="32" height="32" alt="" style="display:inline-block;vertical-align:middle;width:32px;height:32px;border-radius:7px;border:0;margin-left:10px">' : '' )
			. '<span style="vertical-align:middle;font-size:24px;line-height:32px;font-weight:800;color:#FFFFFF;letter-spacing:.3px">נדל״ן</span></td>'
			. '<td align="left" style="vertical-align:middle;font-size:13px;color:#CFE3EA">nad-lan.co.il</td></tr></table></td></tr>'
			. '<tr><td class="card" style="background:#FFFFFF;border:1px solid #D3DCE2;border-top:0;border-radius:0 0 12px 12px"><table role="presentation" width="100%" cellpadding="0" cellspacing="0">' . $rows . '</table></td></tr>'
			. '<tr><td class="px mute" style="padding:18px 32px 8px;font-size:13px;line-height:20px;color:#5E6A75">' . $foot . '<br>' . esc_html( $o['biz_line'] ) . '</td></tr>'
			. '</table></td></tr></table></div></body></html>';
	}
	function nadlan_ms_plain( $f, $first = '', $unsub = '', $ctx = array() ) {
		$ph = array( '{שם}', '{name}', '{חברה}', '{company}' ); $co = (string) ( $ctx['company'] ?? '' ); $rp = array( $first, $first, $co, $co );
		$t = trim( (string) ( $f['title'] ?? '' ) ) . "\n\n" . trim( str_replace( $ph, $rp, (string) ( $f['greeting'] ?? '' ) ) ) . "\n\n" . str_replace( $ph, $rp, preg_replace( '/\*\*(.+?)\*\*/u', '$1', (string) ( $f['body'] ?? '' ) ) );
		if ( ! empty( $ctx['yes'] ) ) { $t .= "\n\nכן, אשמח לקבל: " . $ctx['yes'] . "\nלא, תודה: " . $ctx['no']; }
		foreach ( (array) ( $f['items'] ?? array() ) as $id ) { $it = nadlan_ms_item( (int) $id ); $t .= "\n\n" . $it['title'] . ( $it['facts'] ? ' · ' . implode( ' · ', $it['facts'] ) : '' ) . ( $it['price'] ? ' · ' . $it['price'] : '' ) . "\n" . $it['url']; }
		if ( ! empty( $f['cta_url'] ) ) { $t .= "\n\n" . ( $f['cta_text'] ?? '' ) . ': ' . $f['cta_url']; }
		if ( $unsub ) { $t .= "\n\nלהסרה מרשימת התפוצה: " . $unsub; }
		return trim( $t ) . "\n\n" . nadlan_ms_opt( 'biz_line' );
	}

	/* ---------- the form fields, cleaned ---------- */
	function nadlan_ms_fields( $p ) {
		$s = function ( $k, $max = 300 ) use ( $p ) { return mb_substr( sanitize_text_field( wp_unslash( (string) ( $p[ $k ] ?? '' ) ) ), 0, $max ); };
		$f = array(
			'kind'       => in_array( $p['kind'] ?? '', array( 'dist', 'invite' ), true ) ? $p['kind'] : 'personal',
			'seg'        => in_array( $p['seg'] ?? '', array( 'client', 'developer', 'broker', 'pro' ), true ) ? $p['seg'] : 'all',
			'film'       => ! empty( $p['film'] ),
			'film_url'   => esc_url_raw( (string) ( $p['film_url'] ?? '' ) ),
			'film_poster'=> esc_url_raw( (string) ( $p['film_poster'] ?? '' ) ),
			'look'       => in_array( $p['look'] ?? '', array( 'letter', 'listings', 'update' ), true ) ? $p['look'] : 'letter',
			'to'         => sanitize_email( (string) ( $p['to'] ?? '' ) ),
			'to_name'    => $s( 'to_name', 80 ),
			'subject'    => $s( 'subject', 150 ),
			'pre'        => $s( 'pre', 200 ),
			'title'      => $s( 'title', 140 ),
			'greeting'   => $s( 'greeting', 120 ),
			'body'       => mb_substr( sanitize_textarea_field( wp_unslash( (string) ( $p['body'] ?? '' ) ) ), 0, 8000 ),
			'figure'     => $s( 'figure', 24 ),
			'figure_cap' => $s( 'figure_cap', 120 ),
			'film_cap'   => $s( 'film_cap', 140 ),
			'items_raw'  => mb_substr( sanitize_textarea_field( wp_unslash( (string) ( $p['items'] ?? '' ) ) ), 0, 2000 ),
			'cta_text'   => $s( 'cta_text', 60 ),
			'cta_url'    => esc_url_raw( (string) ( $p['cta_url'] ?? '' ) ),
			'sign'       => ! empty( $p['sign'] ),
		);
		$f['items'] = nadlan_ms_resolve( $f['items_raw'] );
		$f['ad']    = 'dist' === $f['kind'];
		if ( 'invite' === $f['kind'] ) { $f['look'] = 'letter'; $f['items'] = array(); $f['film'] = false; $f['cta_text'] = ''; if ( 'all' === $f['seg'] ) { $f['seg'] = 'developer'; } } // no pitch in an invitation
		if ( $f['ad'] && '' !== $f['subject'] && 0 !== mb_strpos( $f['subject'], 'פרסומת' ) ) { $f['subject'] = 'פרסומת: ' . $f['subject']; } // 30A: first in the subject
		return $f;
	}

	/* ---------- sending ---------- */
	function nadlan_ms_unsub_sig( $email ) { return substr( hash_hmac( 'sha256', 'nlms|unsub|' . strtolower( trim( $email ) ), wp_salt( 'auth' ) ), 0, 24 ); }
	function nadlan_ms_unsub_url( $email ) { return add_query_arg( array( 'e' => rawurlencode( strtolower( trim( $email ) ) ), 's' => nadlan_ms_unsub_sig( $email ) ), rest_url( 'nadlan/v1/ms-unsub' ) ); }
	function nadlan_ms_send_one( $to, $f, $first, $unsub, $tag, $ctx = array() ) {
		$fn   = (string) nadlan_ms_opt( 'from_name' );
		$text = nadlan_ms_plain( $f, $first, $unsub, $ctx );
		$subj = str_replace( array( '{שם}', '{name}', '{חברה}', '{company}' ), array( $first, $first, (string) ( $ctx['company'] ?? '' ), (string) ( $ctx['company'] ?? '' ) ), (string) $f['subject'] );
		$hook = function ( $pm ) use ( $fn, $text ) { $pm->FromName = $fn; $pm->AltBody = $text; };
		add_action( 'phpmailer_init', $hook, PHP_INT_MAX ); // after inc/mailer.php's From (same priority, added later)
		$h = array( 'Content-Type: text/html; charset=UTF-8', 'X-NadLan-Mail: ' . $tag );
		if ( nadlan_ms_opt( 'reply_to' ) ) { $h[] = 'Reply-To: ' . nadlan_ms_opt( 'reply_to' ); }
		if ( $unsub ) { $h[] = 'List-Unsubscribe: <' . esc_url_raw( $unsub ) . '>'; $h[] = 'List-Unsubscribe-Post: List-Unsubscribe=One-Click'; }
		$err = '';
		$fail = function ( $e ) use ( &$err ) { $err = is_wp_error( $e ) ? $e->get_error_message() : 'failed'; };
		add_action( 'wp_mail_failed', $fail );
		$ok = (bool) wp_mail( $to, $subj, nadlan_ms_render( $f, $first, $unsub, $ctx ), $h );
		remove_action( 'wp_mail_failed', $fail );
		remove_action( 'phpmailer_init', $hook, PHP_INT_MAX );
		return $ok ? '' : ( $err ? $err : 'failed' );
	}
	function nadlan_ms_first( $name ) { $p = preg_split( '/\s+/u', trim( (string) $name ) ); return (string) ( $p[0] ?? '' ); }
	function nadlan_ms_day_count( $add = 0 ) {
		$d = (array) get_option( 'nadlan_ms_day', array() );
		$t = wp_date( 'Y-m-d' );
		if ( ( $d['d'] ?? '' ) !== $t ) { $d = array( 'd' => $t, 'n' => 0 ); }
		if ( $add ) { $d['n'] += $add; update_option( 'nadlan_ms_day', $d, false ); }
		return (int) $d['n'];
	}
	/** The audience of a distribution: advertising consent, not unsubscribed. */
	function nadlan_ms_audience( $seg = 'all' ) {
		global $wpdb;
		$w = 'all' === $seg ? '' : $wpdb->prepare( ' AND kind = %s', $seg );
		return (array) $wpdb->get_results( 'SELECT email, name, company FROM ' . nadlan_ms_t( 'contacts' ) . " WHERE consent = 'ad' AND unsub_at IS NULL$w ORDER BY id" );
	}
	/** Businesses that may still get their one invitation: never invited, never answered, not removed. */
	function nadlan_ms_invitees( $seg ) {
		global $wpdb;
		return (array) $wpdb->get_results( $wpdb->prepare( 'SELECT email, name, company FROM ' . nadlan_ms_t( 'contacts' ) . " WHERE consent = 'invite' AND invited_at IS NULL AND answer = '' AND unsub_at IS NULL AND kind = %s ORDER BY id", $seg ) );
	}
	function nadlan_ms_ans_sig( $a, $email ) { return substr( hash_hmac( 'sha256', 'nlms|ans|' . $a . '|' . strtolower( trim( $email ) ), wp_salt( 'auth' ) ), 0, 24 ); }
	function nadlan_ms_ans_url( $a, $email ) { return add_query_arg( array( 'a' => $a, 'e' => rawurlencode( strtolower( trim( $email ) ) ), 's' => nadlan_ms_ans_sig( $a, $email ) ), rest_url( 'nadlan/v1/ms-answer' ) ); }
	/** One minute's work of the queue. */
	function nadlan_ms_tick() {
		global $wpdb;
		$q   = nadlan_ms_t( 'queue' );
		$cap = max( 0, (int) nadlan_ms_opt( 'day_cap' ) - nadlan_ms_day_count() );
		$n   = min( max( 1, (int) nadlan_ms_opt( 'per_min' ) ), $cap );
		if ( $n < 1 ) { return array( 'sent' => 0, 'cap' => true ); }
		$rows = $wpdb->get_results( $wpdb->prepare( "SELECT * FROM $q WHERE status = 'wait' ORDER BY id LIMIT %d", $n ) );
		$done = 0;
		$cache = array();
		foreach ( $rows as $r ) {
			if ( ! $wpdb->update( $q, array( 'status' => 'busy' ), array( 'id' => $r->id, 'status' => 'wait' ) ) ) { continue; } // another tick took it
			$unsubbed = $wpdb->get_var( $wpdb->prepare( 'SELECT unsub_at FROM ' . nadlan_ms_t( 'contacts' ) . ' WHERE email = %s', $r->email ) );
			if ( $unsubbed ) { $wpdb->update( $q, array( 'status' => 'skip', 'err' => 'unsubscribed' ), array( 'id' => $r->id ) ); continue; }
			if ( ! isset( $cache[ $r->campaign ] ) ) { $cache[ $r->campaign ] = json_decode( (string) get_post_meta( $r->campaign, 'ms_fields', true ), true ); }
			$f = $cache[ $r->campaign ];
			if ( ! is_array( $f ) ) { $wpdb->update( $q, array( 'status' => 'fail', 'err' => 'campaign gone' ), array( 'id' => $r->id ) ); continue; }
			$c   = $wpdb->get_row( $wpdb->prepare( 'SELECT company, invited_at, answer FROM ' . nadlan_ms_t( 'contacts' ) . ' WHERE email = %s', $r->email ) );
			$ctx = array( 'company' => $c ? (string) $c->company : '' );
			if ( 'invite' === ( $f['kind'] ?? '' ) ) {
				if ( ! $c || $c->invited_at || '' !== $c->answer ) { $wpdb->update( $q, array( 'status' => 'skip', 'err' => 'already invited' ), array( 'id' => $r->id ) ); continue; } // one invitation, ever
				$ctx['yes'] = nadlan_ms_ans_url( 'yes', $r->email ); $ctx['no'] = nadlan_ms_ans_url( 'no', $r->email );
				$wpdb->update( nadlan_ms_t( 'contacts' ), array( 'invited_at' => current_time( 'mysql', true ) ), array( 'email' => $r->email ) );
			}
			$err = nadlan_ms_send_one( $r->email, $f, nadlan_ms_first( $r->name ), nadlan_ms_unsub_url( $r->email ), 'dist-' . $r->campaign, $ctx );
			$wpdb->update( $q, array( 'status' => $err ? 'fail' : 'sent', 'err' => mb_substr( $err, 0, 180 ), 'sent_at' => current_time( 'mysql', true ) ), array( 'id' => $r->id ) );
			$done++;
		}
		if ( $done ) { nadlan_ms_day_count( $done ); }
		if ( ! (int) $wpdb->get_var( "SELECT COUNT(*) FROM $q WHERE status = 'wait'" ) ) { wp_clear_scheduled_hook( 'nadlan_ms_tick' ); }
		return array( 'sent' => $done, 'cap' => $cap <= $done );
	}
	add_filter( 'cron_schedules', function ( $s ) { $s['nadlan_ms_min'] = array( 'interval' => 60, 'display' => 'every minute (mail studio)' ); return $s; } );
	add_action( 'nadlan_ms_tick', 'nadlan_ms_tick' );

	/* ---------- the audience: the price window's consented sign-ups, imported lists ---------- */
	function nadlan_ms_add_contact( $email, $name, $source, $consent, $text, $at = '', $kind = 'client', $company = '' ) {
		global $wpdb;
		$email = strtolower( trim( (string) $email ) );
		if ( ! is_email( $email ) ) { return 'bad'; }
		$t   = nadlan_ms_t( 'contacts' );
		$cur = $wpdb->get_row( $wpdb->prepare( "SELECT id, consent FROM $t WHERE email = %s", $email ) );
		if ( $cur ) {
			if ( 'invite' === $consent ) { return 'same'; } // an invitation never lowers or resets an existing record
			if ( 'ad' === $consent && 'ad' !== $cur->consent ) { $wpdb->update( $t, array( 'consent' => 'ad', 'consent_text' => $text, 'consent_at' => $at ? $at : current_time( 'mysql', true ), 'source' => $source ), array( 'id' => $cur->id ) ); return 'up'; }
			return 'same';
		}
		$wpdb->insert( $t, array( 'email' => $email, 'name' => mb_substr( (string) $name, 0, 120 ), 'kind' => in_array( $kind, array( 'client', 'developer', 'broker', 'pro' ), true ) ? $kind : 'client', 'company' => mb_substr( (string) $company, 0, 120 ), 'source' => $source, 'consent' => $consent, 'consent_text' => $text, 'consent_at' => $at ? $at : current_time( 'mysql', true ), 'created_at' => current_time( 'mysql', true ) ) );
		return 'new';
	}
	function nadlan_ms_sync() {
		$n = array( 'new' => 0, 'up' => 0, 'same' => 0, 'bad' => 0 );
		$ids = get_posts( array( 'post_type' => 'nadlan_lead', 'post_status' => 'any', 'numberposts' => -1, 'fields' => 'ids', 'suppress_filters' => true,
			'meta_query' => array( array( 'key' => 'consent_text', 'value' => 'פרסומ', 'compare' => 'LIKE' ) ) ) );
		foreach ( $ids as $id ) {
			if ( ! get_post_meta( $id, 'consent', true ) ) { continue; }
			$r = nadlan_ms_add_contact( get_post_meta( $id, 'email', true ), get_post_meta( $id, 'name', true ), 'price_alert #' . $id, 'ad', (string) get_post_meta( $id, 'consent_text', true ), (string) get_post_meta( $id, 'consent_recorded', true ) );
			$n[ $r ]++;
		}
		update_option( 'nadlan_ms_synced', time(), false );
		return $n;
	}

	/* ---------- the refusal link ---------- */
	function nadlan_ms_unsub_route( WP_REST_Request $req ) {
		global $wpdb;
		$e  = strtolower( trim( rawurldecode( (string) $req->get_param( 'e' ) ) ) );
		$ok = is_email( $e ) && hash_equals( nadlan_ms_unsub_sig( $e ), (string) $req->get_param( 's' ) );
		$one_click = 'POST' === $req->get_method() && false !== strpos( (string) $req->get_body(), 'One-Click' );
		if ( $ok && 'POST' === $req->get_method() ) {
			$t = nadlan_ms_t( 'contacts' );
			if ( $wpdb->get_var( $wpdb->prepare( "SELECT id FROM $t WHERE email = %s", $e ) ) ) {
				$wpdb->query( $wpdb->prepare( "UPDATE $t SET unsub_at = %s WHERE email = %s AND unsub_at IS NULL", current_time( 'mysql', true ), $e ) );
			} else {
				$wpdb->insert( $t, array( 'email' => $e, 'source' => 'unsubscribe', 'consent' => 'none', 'created_at' => current_time( 'mysql', true ), 'unsub_at' => current_time( 'mysql', true ) ) );
			}
		}
		if ( $one_click ) { return new WP_REST_Response( array( 'ok' => (bool) $ok ), 200 ); }
		nocache_headers();
		do_action( 'litespeed_control_set_nocache', 'nadlan mail studio unsubscribe' );
		header( 'Content-Type: text/html; charset=utf-8' );
		$body = ! $ok ? '<h1>הקישור אינו בתוקף</h1><p>אפשר לכתוב ל־info@nad-lan.co.il ונסיר אתכם מיד.</p>'
			: ( 'POST' === $req->get_method() ? '<h1>הוסרתם מרשימת התפוצה</h1><p>לא יישלחו אליכם עוד פרסומות מנדל״ן לכתובת ' . esc_html( $e ) . '.</p>'
			: '<h1>להסיר את ' . esc_html( $e ) . ' מרשימת התפוצה?</h1><form method="post" action="' . esc_url( nadlan_ms_unsub_url( $e ) ) . '"><button type="submit">כן, הסירו אותי</button></form><p class="f">פתיחת הקישור לא שינתה כלום. הלחיצה מסירה מיד.</p>' );
		echo '<!doctype html><html lang="he" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>הסרה מרשימת התפוצה · נדל״ן</title>'
			. '<style>body{margin:0;background:#EEF2F4;font:17px/1.6 Arial,sans-serif;color:#12202A}main{max-width:560px;margin:40px auto;background:#fff;border:1px solid #D3DCE2;border-radius:12px;padding:24px}'
			. 'h1{font-size:24px;margin:0 0 12px}p{color:#3E4C58}.f{font-size:14px;color:#5E6A75}button{min-height:50px;padding:0 24px;border:0;border-radius:8px;background:#10262F;color:#fff;font:700 17px Arial;cursor:pointer}</style></head>'
			. '<body><main><div style="font-weight:800;font-size:20px;margin-bottom:12px">נדל״ן</div>' . $body . '</main></body></html>';
		exit;
	}

	/** "כן" or "לא" to the one invitation. GET shows the question again (mail scanners open links); the POST records the answer. */
	function nadlan_ms_answer_route( WP_REST_Request $req ) {
		global $wpdb;
		$a  = 'yes' === $req->get_param( 'a' ) ? 'yes' : 'no';
		$e  = strtolower( trim( rawurldecode( (string) $req->get_param( 'e' ) ) ) );
		$t  = nadlan_ms_t( 'contacts' );
		$c  = is_email( $e ) && hash_equals( nadlan_ms_ans_sig( $a, $e ), (string) $req->get_param( 's' ) ) ? $wpdb->get_row( $wpdb->prepare( "SELECT * FROM $t WHERE email = %s", $e ) ) : null;
		$co = $c && '' !== $c->company ? $c->company : '';
		if ( $c && 'POST' === $req->get_method() ) {
			$now = current_time( 'mysql', true );
			if ( 'yes' === $a ) {
				$text = 'השיב/ה "כן, אשמח לקבל" להזמנה מנדל״ן: מסכים/ה לקבל עדכונים, הצעות ופרסומים מנדל״ן במייל. אפשר להסיר בכל רגע.';
				$wpdb->update( $t, array( 'consent' => 'ad', 'consent_text' => $text, 'consent_at' => $now, 'answer' => 'yes', 'answered_at' => $now, 'unsub_at' => null ), array( 'id' => $c->id ) );
				if ( function_exists( 'nadlan_omx_send' ) && function_exists( 'nadlan_omx_doc' ) ) {
					$who = trim( $c->name . ( $co ? ' · ' . $co : '' ) );
					nadlan_omx_send( 'כן מעסק · ' . $who, nadlan_omx_doc( $who . ' אישר/ה לקבל הצעות', nadlan_omx_strip( 'נדל״ן · תשובה להזמנה' ),
						'<tr><td style="padding:16px 18px"><div style="font-size:20px;font-weight:700">' . esc_html( $who ) . '</div><div style="font-size:15px;margin:6px 0 12px">אמר/ה "כן, אשמח לקבל". אפשר לשלוח עכשיו את ההצעה עם הסרטון.</div>'
						. nadlan_omx_btn( admin_url( 'admin.php?page=nadlan-mail-studio' ), 'לשליחת ההצעה', '#2F6F86' ) . nadlan_omx_btn( 'mailto:' . $c->email, 'מייל', '#FFFFFF', '#12202A', '#C5CFD7' ) . '</td></tr>',
						'ההסכמה נשמרה עם הנוסח והשעה, ברשימת התפוצה של "דיוור נדל״ן".' ), $who . ' said yes', 'b2b' );
				}
			} else {
				$wpdb->update( $t, array( 'answer' => 'no', 'answered_at' => $now, 'unsub_at' => $now ), array( 'id' => $c->id ) );
			}
		}
		nocache_headers();
		do_action( 'litespeed_control_set_nocache', 'nadlan mail studio answer' );
		header( 'Content-Type: text/html; charset=utf-8' );
		$body = ! $c ? '<h1>הקישור אינו בתוקף</h1><p>אפשר לכתוב ל־info@nad-lan.co.il.</p>'
			: ( 'POST' === $req->get_method()
				? ( 'yes' === $a ? '<h1>תודה!</h1><p>נשלח אליכם בקרוב את הפרטים' . ( $co ? ' בשביל ' . esc_html( $co ) : '' ) . '. בכל מייל יהיה קישור להסרה.</p>' : '<h1>קיבלנו, תודה</h1><p>לא נפנה אליכם שוב.</p>' )
				: '<h1>' . ( 'yes' === $a ? 'לאשר שתשמחו לקבל מנדל״ן עדכונים והצעות במייל?' : 'לא לקבל מנדל״ן עוד פניות?' ) . '</h1><form method="post" action="' . esc_url( nadlan_ms_ans_url( $a, $e ) ) . '"><button type="submit">' . ( 'yes' === $a ? 'כן, אשמח לקבל' : 'כן, לא לפנות שוב' ) . '</button></form><p class="f">פתיחת הקישור לא שינתה כלום. הלחיצה שומרת.</p>' );
		echo '<!doctype html><html lang="he" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>נדל״ן</title>'
			. '<style>body{margin:0;background:#EEF2F4;font:17px/1.6 Arial,sans-serif;color:#12202A}main{max-width:560px;margin:40px auto;background:#fff;border:1px solid #D3DCE2;border-radius:12px;padding:24px}'
			. 'h1{font-size:24px;margin:0 0 12px}p{color:#3E4C58}.f{font-size:14px;color:#5E6A75}button{min-height:50px;padding:0 24px;border:0;border-radius:8px;background:#10262F;color:#fff;font:700 17px Arial;cursor:pointer}</style></head>'
			. '<body><main><div style="font-weight:800;font-size:20px;margin-bottom:12px">נדל״ן</div>' . $body . '</main></body></html>';
		exit;
	}

	/* ---------- the admin routes ---------- */
	add_action( 'rest_api_init', function () {
		nadlan_ms_db(); // 1.72.623: the tables exist before any route writes (a first import over REST, before any admin visit, had nowhere to land)
		$admin = function () { return current_user_can( 'manage_options' ); };
		register_rest_route( 'nadlan/v1', '/ms-answer', array( 'methods' => array( 'GET', 'POST' ), 'permission_callback' => '__return_true', 'callback' => 'nadlan_ms_answer_route' ) );
		register_rest_route( 'nadlan/v1', '/ms-unsub', array( 'methods' => array( 'GET', 'POST' ), 'permission_callback' => '__return_true', 'callback' => 'nadlan_ms_unsub_route' ) );
		register_rest_route( 'nadlan/v1', '/ms/preview', array( 'methods' => 'POST', 'permission_callback' => $admin, 'callback' => function ( $r ) {
			$f = nadlan_ms_fields( $r->get_params() );
			$first = 'personal' !== $f['kind'] ? 'דנה' : nadlan_ms_first( $f['to_name'] );
			$ctx   = 'invite' === $f['kind'] ? array( 'company' => 'חברה לדוגמה', 'yes' => '#', 'no' => '#' ) : array();
			$aud   = 'invite' === $f['kind'] ? nadlan_ms_invitees( $f['seg'] ) : nadlan_ms_audience( $f['seg'] );
			return array( 'html' => nadlan_ms_render( $f, $first, 'personal' !== $f['kind'] ? nadlan_ms_unsub_url( 'preview@nad-lan.co.il' ) : '', $ctx ), 'subject' => $f['subject'], 'items' => count( $f['items'] ),
				'audience' => count( $aud ), 'bytes' => strlen( nadlan_ms_render( $f, $first, '', $ctx ) ) );
		} ) );
		register_rest_route( 'nadlan/v1', '/ms/test', array( 'methods' => 'POST', 'permission_callback' => $admin, 'callback' => function ( $r ) {
			$f  = nadlan_ms_fields( $r->get_params() );
			$to = sanitize_email( (string) $r->get_param( 'test_to' ) );
			if ( ! is_email( $to ) ) { $to = wp_get_current_user()->user_email; }
			if ( '' === $f['subject'] ) { return new WP_Error( 'subject', 'חסר נושא', array( 'status' => 422 ) ); }
			$f['subject'] = 'בדיקה · ' . $f['subject'];
			$ctx = 'invite' === $f['kind'] ? array( 'company' => 'חברה לדוגמה', 'yes' => home_url( '/' ), 'no' => home_url( '/' ) ) : array();
			$err = nadlan_ms_send_one( $to, $f, 'personal' !== $f['kind'] ? 'דנה' : nadlan_ms_first( $f['to_name'] ), 'personal' !== $f['kind'] ? nadlan_ms_unsub_url( $to ) : '', 'test', $ctx );
			return array( 'ok' => '' === $err, 'to' => $to, 'err' => $err );
		} ) );
		register_rest_route( 'nadlan/v1', '/ms/send', array( 'methods' => 'POST', 'permission_callback' => $admin, 'callback' => function ( $r ) {
			global $wpdb;
			$f = nadlan_ms_fields( $r->get_params() );
			if ( '' === $f['subject'] || ( '' === trim( $f['body'] ) && ! $f['items'] ) ) { return new WP_Error( 'empty', 'חסרים נושא ותוכן', array( 'status' => 422 ) ); }
			$cid = wp_insert_post( array( 'post_type' => 'nadlan_ms_campaign', 'post_status' => 'private', 'post_title' => $f['subject'] ) );
			update_post_meta( $cid, 'ms_fields', wp_slash( wp_json_encode( $f, JSON_UNESCAPED_UNICODE ) ) );
			update_post_meta( $cid, 'ms_kind', 'personal' === $f['kind'] ? 'personal' : 'dist' );
			update_post_meta( $cid, 'ms_seg', $f['kind'] . ':' . $f['seg'] );
			if ( 'personal' === $f['kind'] ) {
				if ( ! is_email( $f['to'] ) ) { return new WP_Error( 'to', 'כתובת המייל לא תקינה', array( 'status' => 422 ) ); }
				$err = nadlan_ms_send_one( $f['to'], $f, nadlan_ms_first( $f['to_name'] ), '', 'personal-' . $cid );
				update_post_meta( $cid, 'ms_to', $f['to'] );
				update_post_meta( $cid, 'ms_result', $err ? 'נכשל: ' . $err : 'נשלח' );
				nadlan_ms_day_count( $err ? 0 : 1 );
				return array( 'ok' => '' === $err, 'err' => $err, 'campaign' => $cid );
			}
			if ( empty( $r->get_param( 'confirm' ) ) ) { return new WP_Error( 'confirm', 'צריך לאשר את ההפצה', array( 'status' => 422 ) ); }
			$aud = 'invite' === $f['kind'] ? nadlan_ms_invitees( $f['seg'] ) : nadlan_ms_audience( $f['seg'] );
			if ( ! $aud ) { return new WP_Error( 'empty_list', 'invite' === $f['kind'] ? 'אין עסקים מהסוג הזה שעוד לא קיבלו הזמנה' : 'אין ברשימה אף אחד עם הסכמה לקבל פרסומות', array( 'status' => 422 ) ); }
			$q = nadlan_ms_t( 'queue' );
			foreach ( $aud as $a ) { $wpdb->insert( $q, array( 'campaign' => $cid, 'email' => $a->email, 'name' => (string) $a->name, 'status' => 'wait' ) ); }
			update_post_meta( $cid, 'ms_total', count( $aud ) );
			if ( ! wp_next_scheduled( 'nadlan_ms_tick' ) ) { wp_schedule_event( time() + 5, 'nadlan_ms_min', 'nadlan_ms_tick' ); }
			$t = nadlan_ms_tick();
			return array( 'ok' => true, 'campaign' => $cid, 'total' => count( $aud ), 'first_batch' => $t['sent'] );
		} ) );
		register_rest_route( 'nadlan/v1', '/ms/tick', array( 'methods' => 'POST', 'permission_callback' => $admin, 'callback' => function () { return nadlan_ms_tick(); } ) );
		register_rest_route( 'nadlan/v1', '/ms/sync', array( 'methods' => 'POST', 'permission_callback' => $admin, 'callback' => function () { return nadlan_ms_sync(); } ) );
		register_rest_route( 'nadlan/v1', '/ms/import', array( 'methods' => 'POST', 'permission_callback' => $admin, 'callback' => function ( $r ) {
			$kind  = in_array( $r->get_param( 'kind' ), array( 'client', 'developer', 'broker', 'pro' ), true ) ? $r->get_param( 'kind' ) : 'client';
			$basis = 'business' === $r->get_param( 'basis' ) && 'client' !== $kind ? 'invite' : 'ad';
			if ( 'ad' === $basis && empty( $r->get_param( 'consent_ok' ) ) ) { return new WP_Error( 'consent', 'צריך לאשר שיש לכולם הסכמה מתועדת', array( 'status' => 422 ) ); }
			if ( 'invite' === $basis && empty( $r->get_param( 'business_ok' ) ) ) { return new WP_Error( 'business', 'צריך לאשר שאלה כתובות של עסקים', array( 'status' => 422 ) ); }
			$src  = mb_substr( sanitize_text_field( (string) $r->get_param( 'source' ) ), 0, 60 );
			$text = 'invite' === $basis ? 'כתובת עסקית: הזמנה אחת בלבד לשאלה אם להסכים לקבל הצעות (סעיף 30א(ג))' : mb_substr( sanitize_text_field( (string) $r->get_param( 'consent_text' ) ), 0, 300 );
			if ( '' === $src || '' === $text ) { return new WP_Error( 'source', 'צריך לכתוב מאיפה הרשימה ומה נוסח ההסכמה', array( 'status' => 422 ) ); }
			$n = array( 'new' => 0, 'up' => 0, 'same' => 0, 'bad' => 0 );
			foreach ( preg_split( '/\r\n|\r|\n/', (string) $r->get_param( 'rows' ) ) as $line ) {
				$c = str_getcsv( $line );
				if ( ! isset( $c[0] ) || '' === trim( $c[0] ) ) { continue; }
				$em = isset( $c[1] ) && is_email( trim( $c[1] ) ) && ! is_email( trim( $c[0] ) ) ? array( trim( $c[1] ), trim( $c[0] ) ) : array( trim( $c[0] ), trim( $c[1] ?? '' ) );
				$n[ nadlan_ms_add_contact( $em[0], $em[1], 'import: ' . $src, $basis, $text, '', $kind, trim( (string) ( $c[2] ?? '' ) ) ) ]++;
			}
			return $n;
		} ) );
	} );
	add_filter( 'nadlan_hardening_public_post_routes', function ( $r ) { $r[] = '#^/nadlan/v1/ms-unsub$#'; $r[] = '#^/nadlan/v1/ms-answer$#'; return $r; } );

	/* ---------- the admin screen ---------- */
	add_action( 'admin_menu', function () {
		add_menu_page( 'דיוור נדל״ן', 'דיוור נדל״ן', 'manage_options', 'nadlan-mail-studio', 'nadlan_ms_screen', 'dashicons-email-alt', 26 );
	} );
	add_action( 'admin_enqueue_scripts', function ( $hook ) {
		if ( 'toplevel_page_nadlan-mail-studio' !== $hook ) { return; }
		$base = plugins_url( 'assets/mail-studio/', dirname( __DIR__ ) . '/nadlan-config.php' );
		$ver  = defined( 'NADLAN_CONFIG_VERSION' ) ? NADLAN_CONFIG_VERSION : '1';
		wp_enqueue_style( 'nadlan-ms', $base . 'studio.css', array(), $ver );
		wp_enqueue_script( 'nadlan-ms', $base . 'studio.js', array(), $ver, true );
		wp_localize_script( 'nadlan-ms', 'NLMS', array( 'root' => esc_url_raw( rest_url( 'nadlan/v1/' ) ), 'nonce' => wp_create_nonce( 'wp_rest' ), 'me' => wp_get_current_user()->user_email ) );
	} );
	function nadlan_ms_screen() {
		global $wpdb;
		if ( ! current_user_can( 'manage_options' ) ) { return; }
		nadlan_ms_db();
		$tab = sanitize_key( $_GET['tab'] ?? 'write' );
		if ( 'settings' === $tab && isset( $_POST['nadlan_ms_save'] ) && check_admin_referer( 'nadlan_ms_settings' ) ) {
			$o = nadlan_ms_opt();
			foreach ( array( 'from_name', 'reply_to', 'sig_name', 'sig_role', 'sig_phone', 'sig_wa', 'sig_photo', 'biz_line' ) as $k ) { $o[ $k ] = sanitize_text_field( wp_unslash( (string) ( $_POST[ $k ] ?? '' ) ) ); }
			$o['reply_to']  = sanitize_email( $o['reply_to'] );
			$o['sig_photo'] = esc_url_raw( $o['sig_photo'] );
			$o['per_min']   = max( 1, min( 60, (int) ( $_POST['per_min'] ?? 20 ) ) );
			$o['day_cap']   = max( 1, min( 5000, (int) ( $_POST['day_cap'] ?? 250 ) ) );
			update_option( 'nadlan_ms_opts', $o, false );
			echo '<div class="notice notice-success"><p>נשמר.</p></div>';
		}
		$ct  = nadlan_ms_t( 'contacts' );
		$ad  = (int) $wpdb->get_var( "SELECT COUNT(*) FROM $ct WHERE consent = 'ad' AND unsub_at IS NULL" );
		$tabs = array( 'write' => 'כתיבה ושליחה', 'lists' => 'רשימת התפוצה (' . $ad . ')', 'sent' => 'נשלחו', 'settings' => 'הגדרות וחתימה' );
		echo '<div class="wrap nlms" dir="rtl"><h1>דיוור נדל״ן</h1><nav class="nav-tab-wrapper">';
		foreach ( $tabs as $k => $l ) { echo '<a class="nav-tab' . ( $k === $tab ? ' nav-tab-active' : '' ) . '" href="' . esc_url( admin_url( 'admin.php?page=nadlan-mail-studio&tab=' . $k ) ) . '">' . esc_html( $l ) . '</a>'; }
		echo '</nav>';
		if ( 'write' === $tab ) {
			$v = function ( $k ) { return esc_attr( sanitize_text_field( wp_unslash( (string) ( $_GET[ $k ] ?? '' ) ) ) ); };
			echo '<div class="nlms-grid"><form id="nlms-form" class="nlms-form" onsubmit="return false">'
				. '<fieldset class="nlms-kind"><legend>מה שולחים</legend><label><input type="radio" name="kind" value="personal" checked> מייל אישי לאדם אחד</label> <label><input type="radio" name="kind" value="dist"> הפצה לרשימה (' . $ad . ' עם הסכמה)</label> <label><input type="radio" name="kind" value="invite"> הזמנה לעסקים (פעם אחת)</label></fieldset>'
				. '<label class="nlms-seg" hidden>למי<select name="seg"><option value="all">כולם</option><option value="client">לקוחות</option><option value="developer">יזמים</option><option value="broker">מתווכים</option><option value="pro">בעלי מקצוע</option></select></label>'
				. '<p class="nlms-invite-note" hidden>הזמנה לעסק נשלחת פעם אחת בלבד, בלי הצעה ובלי סרטון: רק שאלה אם הם מסכימים לקבל הצעות, ושני כפתורים. מי שעונה "כן" נכנס לרשימה, ותקבל על זה מייל. מי שלא עונה לא יקבל עוד פנייה. <button type="button" class="button" id="nlms-fill">מילוי נוסח מומלץ</button></p>'
				. '<div class="nlms-personal"><label>אל (מייל)<input type="email" name="to" dir="ltr" value="' . $v( 'to' ) . '"></label><label>שם הנמען<input name="to_name" value="' . $v( 'to_name' ) . '"></label></div>'
				. '<p class="nlms-dist-note" hidden>הפצה נשלחת רק למי שנתן הסכמה לקבל פרסומות. הנושא יתחיל אוטומטית ב"פרסומת:", ובכל מייל יהיה קישור הסרה אישי, כמו שהחוק דורש.</p>'
				. '<fieldset><legend>מראה</legend><label><input type="radio" name="look" value="letter" checked> מכתב</label> <label><input type="radio" name="look" value="listings"> נכסים ופרויקטים</label> <label><input type="radio" name="look" value="update"> עדכון עם נתון</label></fieldset>'
				. '<label>נושא<input name="subject" maxlength="150" required></label>'
				. '<label>שורת תצוגה מקדימה <small>(מה שמופיע בתיבה ליד הנושא)</small><input name="pre" maxlength="200"></label>'
				. '<label>כותרת גדולה<input name="title" maxlength="140"></label>'
				. '<label>פתיחה<input name="greeting" value="שלום {שם},"></label>'
				. '<label>הטקסט <small>שורה ריקה = פסקה חדשה · "- " בתחילת שורה = רשימה · "## " = כותרת משנה · **מודגש** · {שם} = שם הנמען</small><textarea name="body" rows="10"></textarea></label>'
				. '<div class="nlms-update" hidden><label>נתון מרכזי <small>(למשל -1.8%)</small><input name="figure" maxlength="24" dir="ltr"></label><label>מה הנתון אומר<input name="figure_cap" maxlength="120"></label></div>'
				. '<label class="nlms-items">נכסים ופרויקטים <small>קישור או מספר, אחד בשורה (עד 6)</small><textarea name="items" rows="3" dir="ltr"></textarea></label>'
				. '<fieldset class="nlms-filmbox"><legend><label><input type="checkbox" name="film" value="1"> להוסיף את הסרטון</label></legend><label>לאן הסרטון מוביל<input name="film_url" dir="ltr" value="' . esc_attr( home_url( '/marketing/#film' ) ) . '"></label><label>תמונת הסרטון<input name="film_poster" dir="ltr" value="' . esc_attr( home_url( '/wp-content/uploads/2026/11/developer-film-v3-poster.jpg' ) ) . '"></label><label>שורה מתחת <small>(בסרטון: מה רואים בו)</small><input name="film_cap" maxlength="140"></label></fieldset>'
				. '<div class="nlms-row"><label>כפתור<input name="cta_text" maxlength="60" placeholder="לדוגמה: לכל הפרטים"></label><label>לאן הכפתור מוביל<input name="cta_url" dir="ltr" placeholder="https://nad-lan.co.il/..."></label></div>'
				. '<label class="nlms-check"><input type="checkbox" name="sign" value="1" checked> להוסיף חתימה</label>'
				. '<div class="nlms-actions"><button class="button" id="nlms-test">שליחת בדיקה אליי</button> <button class="button button-primary button-hero" id="nlms-send">שליחה</button><span id="nlms-msg" role="status" aria-live="polite"></span></div>'
				. '</form><div class="nlms-preview"><div class="nlms-pv-bar"><button type="button" class="button" data-w="390">טלפון</button><button type="button" class="button" data-w="640">מחשב</button><span id="nlms-meta"></span></div><iframe id="nlms-frame" title="תצוגה מקדימה של המייל"></iframe></div></div>';
		} elseif ( 'lists' === $tab ) {
			$rows = $wpdb->get_results( "SELECT * FROM $ct ORDER BY id DESC LIMIT 100" );
			$by   = $wpdb->get_results( "SELECT consent, SUM(unsub_at IS NULL) live, SUM(unsub_at IS NOT NULL) gone FROM $ct GROUP BY consent" );
			echo '<div class="nlms-box"><h2>מי ברשימה</h2><p>';
			foreach ( $by as $b ) { echo esc_html( array( 'ad' => 'הסכמה לפרסומות', 'service' => 'שירות בלבד', 'none' => 'ביקשו הסרה', 'invite' => 'עסקים להזמנה' )[ $b->consent ] ?? $b->consent ) . ': <b>' . (int) $b->live . '</b>' . ( (int) $b->gone ? ' (הוסרו ' . (int) $b->gone . ')' : '' ) . ' &nbsp; '; }
			echo '</p><p><button class="button button-primary" id="nlms-sync">ייבוא הנרשמים מחלון עדכוני המחירים</button> <span id="nlms-sync-msg" role="status"></span><br><small>רק מי שסימן "אני רוצה לקבל מנדל״ן עדכוני מחירים ופרסומים". לידים רגילים לא נכנסים: הם הסכימו רק לטיפול בפנייה.</small></p></div>'
				. '<div class="nlms-box"><h2>ייבוא רשימה</h2><form id="nlms-import" onsubmit="return false"><label>מי ברשימה<select name="kind"><option value="client">לקוחות</option><option value="developer">יזמים</option><option value="broker">מתווכים</option><option value="pro">בעלי מקצוע</option></select></label>'
				. '<fieldset><legend>על מה מבוסס הקשר</legend><label><input type="radio" name="basis" value="consent" checked> יש להם הסכמה מתועדת לקבל פרסומות</label><br><label><input type="radio" name="basis" value="business"> כתובות של עסקים, בלי הסכמה עדיין: יקבלו רק הזמנה אחת</label></fieldset>'
				. '<label><input type="checkbox" name="business_ok" value="1"> אלה כתובות של עסקים, לא של אנשים פרטיים</label>'
				. '<label>מאיפה הרשימה<input name="source" required placeholder="למשל: אירוע משקיעים 10.11"></label>'
				. '<label>מה נוסח ההסכמה שהם נתנו<input name="consent_text" required placeholder="למשל: אני מאשר/ת לקבל עדכונים ופרסומים מנדל״ן"></label>'
				. '<label>הכתובות <small>שורה לכל אחד: מייל, שם, חברה (אפשר להדביק מאקסל)</small><textarea name="rows" rows="6" dir="ltr"></textarea></label>'
				. '<label class="nlms-check"><input type="checkbox" name="consent_ok" value="1"> לכל מי שברשימה יש הסכמה מתועדת לקבל פרסומות מנדל״ן (חוק התקשורת, סעיף 30א)</label>'
				. '<button class="button button-primary" id="nlms-import-go">ייבוא</button> <span id="nlms-import-msg" role="status"></span></form></div>'
				. '<table class="widefat striped"><thead><tr><th>מייל</th><th>שם</th><th>חברה</th><th>סוג</th><th>מקור</th><th>הסכמה</th><th>מתי</th><th>מצב</th></tr></thead><tbody>';
			foreach ( $rows as $r ) {
				echo '<tr><td dir="ltr">' . esc_html( $r->email ) . '</td><td>' . esc_html( $r->name ) . '</td><td>' . esc_html( (string) $r->company ) . '</td><td>' . esc_html( array( 'client' => 'לקוח', 'developer' => 'יזם', 'broker' => 'מתווך', 'pro' => 'בעל מקצוע' )[ $r->kind ] ?? $r->kind ) . '</td><td>' . esc_html( $r->source ) . '</td><td title="' . esc_attr( (string) $r->consent_text ) . '">' . esc_html( array( 'ad' => 'פרסומות', 'service' => 'שירות', 'none' => 'אין', 'invite' => ( $r->invited_at ? 'הוזמן' : 'הזמנה אחת' ) . ( $r->answer ? ' · ענה ' . ( 'yes' === $r->answer ? 'כן' : 'לא' ) : '' ) )[ $r->consent ] ?? $r->consent ) . '</td><td>' . esc_html( $r->consent_at ? get_date_from_gmt( $r->consent_at, 'j.n.Y' ) : '' ) . '</td><td>' . ( $r->unsub_at ? 'הוסר ' . esc_html( get_date_from_gmt( $r->unsub_at, 'j.n' ) ) : 'פעיל' ) . '</td></tr>';
			}
			echo '</tbody></table>';
		} elseif ( 'sent' === $tab ) {
			$q = nadlan_ms_t( 'queue' );
			echo '<table class="widefat striped"><thead><tr><th>מתי</th><th>נושא</th><th>סוג</th><th>אל</th><th>נשלחו</th><th>נכשלו</th><th>ממתינים</th></tr></thead><tbody>';
			foreach ( get_posts( array( 'post_type' => 'nadlan_ms_campaign', 'post_status' => 'private', 'numberposts' => 50 ) ) as $c ) {
				$k = get_post_meta( $c->ID, 'ms_kind', true );
				$s = 'dist' === $k ? $wpdb->get_row( $wpdb->prepare( "SELECT SUM(status='sent') s, SUM(status='fail') f, SUM(status IN ('wait','busy')) w FROM $q WHERE campaign = %d", $c->ID ) ) : null;
				echo '<tr><td>' . esc_html( get_the_date( 'j.n.Y H:i', $c ) ) . '</td><td>' . esc_html( $c->post_title ) . '</td><td>' . ( 'dist' === $k ? 'הפצה' : 'אישי' ) . '</td><td dir="ltr">' . esc_html( 'dist' === $k ? (string) get_post_meta( $c->ID, 'ms_total', true ) . ' נמענים' : (string) get_post_meta( $c->ID, 'ms_to', true ) ) . '</td>'
					. '<td>' . ( $s ? (int) $s->s : esc_html( (string) get_post_meta( $c->ID, 'ms_result', true ) ) ) . '</td><td>' . ( $s ? (int) $s->f : '' ) . '</td><td>' . ( $s ? (int) $s->w : '' ) . '</td></tr>';
			}
			echo '</tbody></table><p>נשלחו היום: ' . (int) nadlan_ms_day_count() . ' מתוך ' . (int) nadlan_ms_opt( 'day_cap' ) . '. פתיחות והקלקות לכל מייל: ביומן של Brevo (Transactional › Logs).</p>';
		} else {
			$o = nadlan_ms_opt();
			$f = function ( $k, $l, $hint = '', $ltr = false ) use ( $o ) { return '<label>' . esc_html( $l ) . ( $hint ? ' <small>' . esc_html( $hint ) . '</small>' : '' ) . '<input name="' . esc_attr( $k ) . '" value="' . esc_attr( (string) $o[ $k ] ) . '"' . ( $ltr ? ' dir="ltr"' : '' ) . '></label>'; };
			echo '<form method="post" class="nlms-form nlms-settings">' . wp_nonce_field( 'nadlan_ms_settings', '_wpnonce', true, false )
				. $f( 'from_name', 'שם השולח', 'מה שהנמען רואה בתיבה' ) . $f( 'reply_to', 'תשובות יגיעו אל', '', true )
				. '<h2>חתימה</h2>' . $f( 'sig_name', 'שם' ) . $f( 'sig_role', 'תפקיד' ) . $f( 'sig_phone', 'טלפון', '', true ) . $f( 'sig_wa', 'וואטסאפ', 'מספר', true ) . $f( 'sig_photo', 'תמונה', 'קישור לתמונה מרובעת', true )
				. '<h2>זיהוי השולח בפרסומת</h2>' . $f( 'biz_line', 'שורת זיהוי', 'שם וכתובת ליצירת קשר, מופיע בתחתית כל מייל' )
				. '<h2>קצב שליחה</h2><label>בדקה<input type="number" name="per_min" min="1" max="60" value="' . (int) $o['per_min'] . '"></label><label>ביום, מקסימום <small>בתוכנית החינמית של Brevo יש 300 ביום לכל האתר</small><input type="number" name="day_cap" min="1" max="5000" value="' . (int) $o['day_cap'] . '"></label>'
				. '<p><button class="button button-primary" name="nadlan_ms_save" value="1">שמירה</button></p></form>';
		}
		echo '</div>';
	}
}
