<?php
/**
 * The professionals network on screen (owner FOCUS, 24.9.2026): "פרגונים" between professionals, built only from the
 * design system (Claude Design artifact L9Nqz7Viv7K3MYeZrBc9s8, version 7: EndorsementStrip, FirgunForm,
 * ProfessionalCard, PageHeader). The rules and the table are in inc/pro-network.php.
 *
 *  1. On a professional's page: the endorsements they received ("פרגונים") and the professionals they recommend
 *     ("מיטל ממליצה על"). Nothing when there is none.
 *  2. /firgun/ ([nadlan_firgun]): a professional with a private link (?t=, the same token as the upload link) endorses
 *     a colleague who is on the site, or invites one who is not and sends the join link on WhatsApp. The invited
 *     (?inv=) see the endorsement that waits for them and join; anyone can ask to join (?join=1). A joined card is
 *     created as "pending": it goes up only after a check in wp-admin, and then the waiting endorsement attaches.
 *  3. wp-admin: on a professional with an upload link, the ready /firgun/ link to send them; a notice when joined
 *     cards wait for a check.
 * Display switch: option nadlan_pro_network_on = '1'.
 */
if ( ! defined( 'ABSPATH' ) ) { exit; }

const NADLAN_FG_CONSENT = 'firgun-join-2026-09-24';

if ( ! function_exists( 'nadlan_fg_on' ) ) {
	function nadlan_fg_on() { return '1' === (string) get_option( 'nadlan_pro_network_on', '0' ); }
}

if ( ! function_exists( 'nadlan_fg_icon_for' ) ) {
	/** The design system's profession mark for a profession key (assets/nlds/icons). */
	function nadlan_fg_icon_for( $key ) {
		$map = array(
			'metavech' => 'profession-broker', 'property_manager' => 'profession-broker', 'organizer' => 'profession-broker',
			'shamai' => 'profession-appraiser', 'surveyor' => 'profession-appraiser',
			'lawyer' => 'profession-lawyer', 'accountant' => 'profession-lawyer', 'actuary' => 'profession-lawyer', 'insurance' => 'profession-lawyer',
			'mashkanta' => 'profession-mortgage',
			'architect' => 'profession-architect', 'interior_designer' => 'profession-architect', 'urban_planner' => 'profession-architect',
			'engineer' => 'profession-inspector', 'mefakeach' => 'profession-inspector', 'bedek_bait' => 'profession-inspector',
			'kablan' => 'profession-contractor', 'renovation' => 'profession-contractor', 'waterproofing' => 'profession-contractor',
			'developer' => 'profession-developer',
		);
		return ( $map[ (string) $key ] ?? 'category-property' ) . '.svg';
	}
}

if ( ! function_exists( 'nadlan_fg_qualities_of' ) ) {
	function nadlan_fg_qualities_of( $csv ) {
		$all = function_exists( 'nadlan_endorse_qualities' ) ? nadlan_endorse_qualities() : array();
		$out = array();
		foreach ( array_filter( explode( ',', (string) $csv ) ) as $k ) {
			if ( isset( $all[ $k ] ) ) { $out[] = $all[ $k ]; }
		}
		return $out;
	}
}

if ( ! function_exists( 'nadlan_fg_person' ) ) {
	/** name, gendered profession label, gender ('f', 'm' or ''), for a card. */
	function nadlan_fg_person( $id ) {
		$key  = (string) get_post_meta( $id, 'profession', true );
		$name = function_exists( 'nadlan_prof_person_name' ) ? (string) nadlan_prof_person_name( $id ) : html_entity_decode( get_the_title( $id ), ENT_QUOTES, 'UTF-8' );
		$role = function_exists( 'nadlan_dir_prof_label' ) ? (string) nadlan_dir_prof_label( $key, $id ) : '';
		$g    = (string) get_post_meta( $id, 'nl_gender', true );
		return array( 'key' => $key, 'name' => $name, 'role' => $role, 'g' => in_array( $g, array( 'f', 'm' ), true ) ? $g : '' );
	}
}

if ( ! function_exists( 'nadlan_fg_item' ) ) {
	/** One EndorsementStrip card: the endorser, the qualities, the line. */
	function nadlan_fg_item( $from, $qualities_csv, $line ) {
		$p  = nadlan_fg_person( (int) $from );
		$ph = has_post_thumbnail( $from )
			? get_the_post_thumbnail( $from, 'thumbnail', array( 'class' => 'nlds-mono', 'alt' => '', 'loading' => 'lazy', 'style' => 'object-fit:cover' ) )
			: '<span class="nlds-mono" aria-hidden="true">' . esc_html( mb_substr( $p['name'], 0, 1 ) ) . '</span>';
		$qs = nadlan_fg_qualities_of( $qualities_csv );
		$h  = '<li class="nlds-endorse__item"><div class="nlds-endorse__who">' . $ph . '<div><a href="' . esc_url( get_permalink( $from ) ) . '">' . esc_html( $p['name'] ) . '</a>'
			. ( '' !== $p['role'] ? '<small>' . esc_html( $p['role'] ) . '</small>' : '' ) . '</div></div>';
		if ( $qs ) {
			$h .= '<div class="nlds-chips nlds-endorse__q">';
			foreach ( $qs as $q ) { $h .= '<span class="nlds-chip nlds-chip--fact">' . esc_html( $q ) . '</span>'; }
			$h .= '</div>';
		}
		if ( '' !== trim( (string) $line ) ) { $h .= '<p class="nlds-endorse__line">' . esc_html( $line ) . '</p>'; }
		return $h . '</li>';
	}
}

if ( ! function_exists( 'nadlan_fg_procard' ) ) {
	/** ProfessionalCard for any profession, with one quality in the foot. */
	function nadlan_fg_procard( $id, $chip = '' ) {
		$p    = nadlan_fg_person( (int) $id );
		$city = trim( (string) get_post_meta( $id, 'city', true ) );
		$icon = function_exists( 'nlds_asset_url' ) ? nlds_asset_url( 'icons/' . nadlan_fg_icon_for( $p['key'] ) ) : '';
		$pin  = function_exists( 'nlds_asset_url' ) ? nlds_asset_url( 'icons/card-pin.svg' ) : '';
		return '<a class="nlds-procard" href="' . esc_url( get_permalink( $id ) ) . '"><div class="nlds-procard__top"><span class="nlds-procard__av" aria-hidden="true"><img src="' . esc_url( $icon ) . '" alt="" width="32" height="32"></span>'
			. '<div class="nlds-procard__id"><h3 class="nlds-procard__name">' . esc_html( html_entity_decode( get_the_title( $id ), ENT_QUOTES, 'UTF-8' ) ) . '</h3>'
			. ( '' !== $p['role'] ? '<span class="nlds-procard__pill">' . esc_html( $p['role'] ) . '</span>' : '' ) . '</div></div>'
			. ( '' !== $city ? '<div class="nlds-procard__meta"><span class="nlds-procard__city"><img src="' . esc_url( $pin ) . '" alt="" width="16" height="16">' . esc_html( $city ) . '</span></div>' : '' )
			. '<div class="nlds-procard__foot">' . ( '' !== $chip ? '<span class="nlds-chip nlds-chip--fact">' . esc_html( $chip ) . '</span>' : '<span></span>' ) . '<span class="nlds-procard__go">לפרופיל ←</span></div></a>';
	}
}

if ( ! function_exists( 'nadlan_fg_strip' ) ) {
	/** On a professional's page: EndorsementStrip (received) and its given direction. '' when there is nothing. */
	function nadlan_fg_strip( $id, $person = '' ) {
		if ( ! nadlan_fg_on() || ! function_exists( 'nadlan_endorse_list' ) ) { return ''; }
		$recv  = nadlan_endorse_list( (int) $id, 'received', 12 );
		$given = nadlan_endorse_list( (int) $id, 'given', 6 );
		if ( ! $recv && ! $given ) { return ''; }
		$h = '<div class="nlds nlpp-network" dir="rtl" lang="he">';
		if ( $recv ) {
			$h .= '<section class="nlds-endorse" aria-labelledby="nlfg-recv"><div class="nlds-endorse__head"><h2 class="nlds-endorse__title" id="nlfg-recv">פרגונים</h2>'
				. '<a class="nlds-btn nlds-btn--quiet nlds-btn--sm" href="' . esc_url( home_url( '/firgun/' ) ) . '">איך מפרגנים ←</a></div><ul class="nlds-endorse__list">';
			foreach ( array_slice( $recv, 0, 3 ) as $r ) { $h .= nadlan_fg_item( (int) $r['from_pro'], $r['qualities'], $r['line'] ); }
			$h .= '</ul>';
			if ( count( $recv ) > 3 ) {
				$h .= '<details class="nlfg-more"><summary class="nlds-btn nlds-btn--quiet">עוד פרגונים ←</summary><ul class="nlds-endorse__list">';
				foreach ( array_slice( $recv, 3 ) as $r ) { $h .= nadlan_fg_item( (int) $r['from_pro'], $r['qualities'], $r['line'] ); }
				$h .= '</ul></details>';
			}
			$h .= '</section>';
		}
		if ( $given ) {
			$me    = nadlan_fg_person( (int) $id );
			$first = (string) strtok( '' !== $person ? $person : $me['name'], ' ' );
			$title = 'f' === $me['g'] ? $first . ' ממליצה על' : ( 'm' === $me['g'] ? $first . ' ממליץ על' : 'ההמלצות של ' . $first );
			$h    .= '<section class="nlds-endorse nlds-endorse--given" aria-labelledby="nlfg-given"><div class="nlds-endorse__head"><h2 class="nlds-endorse__title" id="nlfg-given">' . esc_html( $title ) . '</h2></div><div class="nlds-dgrid">';
			foreach ( $given as $r ) {
				$q  = nadlan_fg_qualities_of( $r['qualities'] );
				$h .= nadlan_fg_procard( (int) $r['to_pro'], $q ? $q[0] : '' );
			}
			$h .= '</div></section>';
		}
		return $h . '</div>';
	}
}

/* ---------------- /firgun/ ---------------- */
if ( ! function_exists( 'nadlan_fg_profession_options' ) ) {
	function nadlan_fg_profession_options( $selected = '' ) {
		$o = '<option value="">בחירת מקצוע</option>';
		foreach ( nadlan_pro_groups() as $g ) {
			$o .= '<optgroup label="' . esc_attr( $g['label'] ) . '">';
			foreach ( $g['professions'] as $k => $f ) {
				$o .= '<option value="' . esc_attr( $k ) . '"' . selected( $selected, $k, false ) . '>' . esc_html( $f[0] ) . '</option>';
			}
			$o .= '</optgroup>';
		}
		return $o;
	}
}

if ( ! function_exists( 'nadlan_fg_quality_chips' ) ) {
	function nadlan_fg_quality_chips() {
		$h = '';
		foreach ( nadlan_endorse_qualities() as $k => $label ) {
			$h .= '<button type="button" class="nlds-chip nlds-chip--filter" aria-pressed="false" data-q="' . esc_attr( $k ) . '">' . esc_html( $label ) . '</button>';
		}
		return $h;
	}
}

if ( ! function_exists( 'nadlan_fg_line_field' ) ) {
	function nadlan_fg_line_field( $id ) {
		// the design system's order: the qualities first, then the one line
		return '<div class="nlds-field"><span class="nlds-field__label">תכונות בולטות<span class="nlds-field__opt"> (עד שלוש)</span></span><div class="nlds-chips">' . nadlan_fg_quality_chips() . '</div></div>'
			. '<div class="nlds-field"><label for="' . esc_attr( $id ) . '">משפט אחד במילים שלכם <span class="nlds-field__opt">(לא חובה)</span></label>'
			. '<textarea id="' . esc_attr( $id ) . '" rows="2" maxlength="140" data-fg-line></textarea>'
			. '<span class="nlds-field__count"><span class="nlds-num" data-count>0</span> מתוך <span class="nlds-num">140</span> תווים</span></div>';
	}
}

if ( ! function_exists( 'nadlan_fg_join_form' ) ) {
	function nadlan_fg_join_form( $invite = null ) {
		$contact = function_exists( 'nl_join_contact' ) ? (string) nl_join_contact() : '';
		$prof    = $invite ? (string) $invite['invite_prof'] : '';
		$h  = '<form class="nlds-form" data-fg="join" id="nlfg-join" novalidate>';
		$h .= '<h2 class="nlds-form__title">' . ( $invite ? 'פרגון מחכה לך' : 'הצטרפות לאנשי המקצוע באתר' ) . '</h2>';
		if ( $invite ) {
			$h .= '<ul class="nlds-endorse__list nlds-endorse__list--one">' . nadlan_fg_item( (int) $invite['from_pro'], $invite['qualities'], $invite['line'] ) . '</ul>';
			$h .= '<p class="nlds-form__lead">כדי שהפרגון יופיע, נפתח לך כרטיס באתר. זה בחינם.</p>';
		} else {
			$h .= '<p class="nlds-form__lead">כרטיס באתר בחינם: השם, המקצוע, העיר והנייד, ופרגונים מאנשי מקצוע שעבדו איתך. מתווכים פותחים אתר מלא עם בדיקת רישיון <a href="' . esc_url( home_url( '/brokers/#join' ) ) . '">בעמוד המתווכים</a>.</p>';
		}
		$h .= '<div class="nlds-field"><label for="nlfg-jn">השם כפי שיופיע<span class="nlds-field__req" aria-hidden="true">*</span></label><input id="nlfg-jn" type="text" maxlength="80" autocomplete="name" data-fg-f="name"' . ( $invite ? ' value="' . esc_attr( $invite['invite_name'] ) . '"' : '' ) . '></div>';
		$h .= '<div class="nlds-field"><label for="nlfg-jp">מקצוע<span class="nlds-field__req" aria-hidden="true">*</span></label><select id="nlfg-jp" data-fg-f="profession">' . nadlan_fg_profession_options( $prof ) . '</select></div>';
		$h .= '<div class="nlds-field" data-fg-gender-row hidden><label for="nlfg-jg">כך יופיע המקצוע</label><select id="nlfg-jg" data-fg-f="gender"></select></div>';
		$h .= '<div class="nlds-field"><label for="nlfg-jc">עיר<span class="nlds-field__req" aria-hidden="true">*</span></label><input id="nlfg-jc" type="text" maxlength="40" autocomplete="address-level2" data-fg-f="city"></div>';
		$h .= '<div class="nlds-field"><label for="nlfg-jt">נייד<span class="nlds-field__req" aria-hidden="true">*</span></label><input id="nlfg-jt" type="tel" inputmode="tel" maxlength="20" autocomplete="tel" data-fg-f="phone"></div>';
		$h .= '<div class="nlds-field"><label for="nlfg-je">מייל <span class="nlds-field__opt">(לא מתפרסם)</span></label><input id="nlfg-je" type="email" maxlength="100" autocomplete="email" data-fg-f="email"></div>';
		$h .= '<div class="nlds-field"><label for="nlfg-jl">מספר רישיון או רישום <span class="nlds-field__opt">(לא חובה)</span></label><input id="nlfg-jl" type="text" maxlength="20" data-fg-f="licence"></div>';
		$h .= '<input type="text" class="nlfg-hp" name="company" tabindex="-1" autocomplete="off" aria-hidden="true" data-fg-f="hp">';
		$h .= '<details class="nlds-priv"><summary>מה קורה עם הפרטים</summary><p>נדלן (nad-lan.co.il) משתמשת בפרטים כדי לפתוח לך כרטיס באתר. השם, המקצוע, העיר, הנייד ומספר הרישיון (אם נמסר) יופיעו בכרטיס אחרי בדיקה; המייל לא מתפרסם. הפרטים לא נמסרים לאחרים. אפשר לבקש תיקון או מחיקה בכל עת'
			. ( '' !== $contact ? ': <a href="mailto:' . esc_attr( $contact ) . '">' . esc_html( $contact ) . '</a>' : '' ) . '.</p></details>';
		$h .= '<label class="nlds-consent"><input type="checkbox" data-fg-f="consent"><span>אני מסכים/ה שנדלן תשמור את הפרטים ותפתח לי כרטיס באתר.</span></label>';
		$h .= '<button type="submit" class="nlds-btn nlds-btn--primary">הצטרפות</button><div class="nlds-msg" role="status" hidden data-fg-msg></div></form>';
		return $h;
	}
}

if ( ! function_exists( 'nadlan_fg_page' ) ) {
	function nadlan_fg_page() {
		$token  = isset( $_GET['t'] ) ? sanitize_key( wp_unslash( (string) $_GET['t'] ) ) : '';
		$inv    = isset( $_GET['inv'] ) ? sanitize_key( wp_unslash( (string) $_GET['inv'] ) ) : '';
		$me     = 0;
		if ( '' !== $token && function_exists( 'nl_drop_broker_by_token' ) ) {
			$b  = nl_drop_broker_by_token( $token );
			$me = is_array( $b ) && ! empty( $b['id'] ) ? (int) $b['id'] : 0;
		}
		$invite = null;
		if ( '' !== $inv && preg_match( '/^[a-z0-9]{24}$/', $inv ) && function_exists( 'nadlan_endorse_table' ) ) {
			global $wpdb;
			$row    = $wpdb->get_row( $wpdb->prepare( 'SELECT * FROM ' . nadlan_endorse_table() . " WHERE invite_token = %s AND status = 'invited' LIMIT 1", $inv ), ARRAY_A );
			$invite = ( $row && 'publish' === get_post_status( (int) $row['from_pro'] ) ) ? $row : null;
		}
		$reg   = nadlan_pro_registry();
		$forms = array();
		foreach ( $reg as $k => $r ) { $forms[ $k ] = array( $r['label'], $r['female'] ); }
		$cfg = array( 'search' => esc_url_raw( rest_url( 'nadlan/v1/pros/search' ) ), 'endorse' => esc_url_raw( rest_url( 'nadlan/v1/endorse' ) ), 'join' => esc_url_raw( rest_url( 'nadlan/v1/pros/join' ) ),
			'token' => $me ? $token : '', 'me' => $me, 'inv' => $invite ? $inv : '', 'forms' => $forms );
		$wa = function_exists( 'nlds_icon' ) ? nlds_icon( 'whatsapp' ) : '';

		$h  = '<div class="nlds nlfg" id="nlfg" dir="rtl" lang="he" data-cfg="' . esc_attr( wp_json_encode( $cfg ) ) . '">';
		$h .= '<header class="nlds-pagehead"><nav class="nlds-crumbs" aria-label="ניווט"><a href="' . esc_url( home_url( '/' ) ) . '">בית</a><span class="nlds-crumbs__sep" aria-hidden="true">›</span>'
			. '<a href="' . esc_url( home_url( '/professionals/' ) ) . '">אנשי מקצוע</a><span class="nlds-crumbs__sep" aria-hidden="true">›</span><span aria-current="page">פרגונים</span></nav>'
			. '<h1 class="nlds-pagehead__title">פרגונים בין אנשי מקצוע</h1>'
			. '<p class="nlds-pagehead__lead">מתווכים, שמאים, עורכי דין, יועצי משכנתאות ואנשי מקצוע בכל תחום של הבית ממליצים זה על זה. רק מילים טובות: עד שלוש תכונות ומשפט אחד, בלי כוכבים ובלי ציונים.</p></header>';

		if ( $me ) {
			$p  = nadlan_fg_person( $me );
			$h .= '<form class="nlds-form" data-fg="give" novalidate><h2 class="nlds-form__title">פרגון לאיש מקצוע</h2>'
				. '<p class="nlds-form__lead">מפרגנים בשם ' . esc_html( $p['name'] ) . '. הפרגון יופיע בעמוד של מי שקיבל אותו, ובעמוד שלך תחת ההמלצות שלך.</p>'
				. '<div class="nlds-field"><label for="nlfg-q">למי מפרגנים<span class="nlds-field__req" aria-hidden="true">*</span></label>'
				. '<input id="nlfg-q" type="search" autocomplete="off" placeholder="שם, לפחות שתי אותיות" data-fg-q>'
				. '<ul class="nlds-pick" role="listbox" aria-label="תוצאות" data-fg-list hidden></ul>'
				. '<div class="nlds-pick__chosen" data-fg-chosen hidden><span data-fg-name></span><button type="button" class="nlds-btn nlds-btn--quiet nlds-btn--sm" data-fg-change>החלפה</button></div></div>'
				. nadlan_fg_line_field( 'nlfg-line' )
				. '<button type="submit" class="nlds-btn nlds-btn--primary">שליחת הפרגון</button><div class="nlds-msg" role="status" hidden data-fg-msg></div>'
				. '<div class="nlds-form__alt"><button type="button" class="nlds-btn nlds-btn--quiet" data-fg-switch="invite">לא מוצאים? הזמינו</button></div></form>';
			$h .= '<form class="nlds-form" data-fg="invite" novalidate hidden><h2 class="nlds-form__title">הזמנה לאיש מקצוע שעוד לא באתר</h2>'
				. '<p class="nlds-form__lead">הפרגון יחכה לו או לה. תקבלו קישור לשלוח בוואטסאפ; כשהכרטיס יעלה לאתר, הפרגון יופיע בו.</p>'
				. '<div class="nlds-field"><label for="nlfg-in">שם<span class="nlds-field__req" aria-hidden="true">*</span></label><input id="nlfg-in" type="text" maxlength="80" data-fg-iname></div>'
				. '<div class="nlds-field"><label for="nlfg-ip">מקצוע<span class="nlds-field__req" aria-hidden="true">*</span></label><select id="nlfg-ip" data-fg-iprof>' . nadlan_fg_profession_options() . '</select></div>'
				. nadlan_fg_line_field( 'nlfg-iline' )
				. '<button type="submit" class="nlds-btn nlds-btn--primary">יצירת הזמנה</button><div class="nlds-msg" role="status" hidden data-fg-msg></div>'
				. '<div class="nlds-form__alt"><button type="button" class="nlds-btn nlds-btn--quiet" data-fg-switch="give">חזרה לפרגון לאיש מקצוע באתר</button></div></form>';
			$h .= '<div class="nlds-form" data-fg="sent" hidden><h2 class="nlds-form__title">ההזמנה מוכנה</h2><p class="nlds-form__lead" data-fg-sent-lead></p>'
				. '<a class="nlds-btn nlds-btn--primary" target="_blank" rel="noopener" href="#" data-fg-wa>' . $wa . '<span>שליחה בוואטסאפ</span></a>'
				. '<div class="nlds-form__alt"><button type="button" class="nlds-btn nlds-btn--quiet" data-fg-copy>העתקת הקישור</button></div></div>';
		} elseif ( $invite || isset( $_GET['join'] ) ) {
			$h .= nadlan_fg_join_form( $invite );
		} else {
			if ( '' !== $token || '' !== $inv ) {
				$h .= '<div class="nlds-msg" role="status">הקישור לא תקין או שכבר השתמשו בו. אפשר להצטרף כאן, או לבקש קישור חדש.</div>';
			}
			$h .= '<div class="nlfg-intro"><p>פרגון הוא המלצה של איש מקצוע על איש מקצוע אחר שעבד איתו: עד שלוש תכונות מרשימה קבועה של מילים טובות, ומשפט אחד. הפרגונים מופיעים בעמוד של מי שקיבל אותם, ובעמוד של מי שנתן אותם מופיעים אנשי המקצוע שהוא ממליץ עליהם.</p>'
				. '<p>כבר יש לכם כרטיס באתר? הפרגון נשלח מהקישור האישי שקיבלתם מאיתנו.</p>'
				. '<div class="nlfg-ctas"><a class="nlds-btn nlds-btn--primary" href="' . esc_url( add_query_arg( 'join', '1', home_url( '/firgun/' ) ) ) . '#nlfg-join">הצטרפות לאנשי המקצוע באתר</a>'
				. '<a class="nlds-btn nlds-btn--secondary" href="' . esc_url( home_url( '/brokers/#join' ) ) . '">מתווכים: פתיחת אתר בחינם</a></div></div>';
		}
		return $h . '</div>';
	}
}

add_shortcode( 'nadlan_firgun', function () {
	return function_exists( 'nadlan_pro_groups' ) && function_exists( 'nadlan_endorse_qualities' ) ? nadlan_fg_page() : '';
} );

add_action( 'wp_footer', function () {
	if ( ! is_singular() || false === strpos( (string) get_post_field( 'post_content', get_queried_object_id() ), '[nadlan_firgun]' ) ) { return; }
	echo "\n<style id=\"nadlan-firgun-css\">:root body .nlfg{display:grid!important;gap:var(--nlds-space-22)!important;margin-block-end:40px!important}"
		. ':root body .nlfg .nlfg-intro{display:grid!important;gap:var(--nlds-space-12)!important;max-width:760px}'
		. ':root body .nlfg .nlfg-intro p{font-size:16.5px!important;line-height:1.65!important;color:var(--nlds-sa-ink2)!important;margin:0!important}'
		. ':root body .nlfg .nlfg-ctas{display:flex!important;flex-wrap:wrap!important;gap:var(--nlds-space-10)!important;margin-top:6px!important}'
		. ':root body .nlfg .nlfg-hp{position:absolute!important;left:-9999px!important;width:1px!important;height:1px!important;overflow:hidden!important}'
		. ':root body .nlfg .nlds-form{width:100%!important}'
		. ':root body .nlfg .nlds-form__lead a{color:var(--nlds-sa-sea)!important;font-weight:600!important}</style>' . "\n";
	?>
<script id="nadlan-firgun-js">
(function () {
	var root = document.getElementById('nlfg'); if (!root) return;
	var cfg = {}; try { cfg = JSON.parse(root.getAttribute('data-cfg') || '{}'); } catch (e) {}
	function one(s, el) { return (el || root).querySelector(s); }
	function all(s, el) { return Array.prototype.slice.call((el || root).querySelectorAll(s)); }
	function say(form, text, ok) { var m = one('[data-fg-msg]', form); if (!m) return; m.textContent = text; m.className = 'nlds-msg' + (ok ? ' nlds-msg--ok' : ''); m.hidden = false; }
	function post(url, body) {
		return fetch(url, { method: 'POST', headers: { 'Content-Type': 'application/json' }, credentials: 'omit', body: JSON.stringify(body) })
			.then(function (r) { return r.json().then(function (j) { return { ok: r.ok, j: j || {} }; }, function () { return { ok: false, j: {} }; }); });
	}
	var oops = 'משהו לא עבד. נסו שוב בעוד רגע.';
	function wire(form) {
		all('.nlds-chip--filter', form).forEach(function (c) {
			c.addEventListener('click', function () {
				var on = c.getAttribute('aria-pressed') === 'true';
				if (!on && all('.nlds-chip--filter[aria-pressed="true"]', form).length >= 3) return;
				c.setAttribute('aria-pressed', on ? 'false' : 'true');
			});
		});
		all('[data-fg-line]', form).forEach(function (ta) {
			var out = ta.parentNode.querySelector('[data-count]');
			var f = function () { if (out) out.textContent = ta.value.length; };
			ta.addEventListener('input', f); f();
		});
	}
	function qualities(form) { return all('.nlds-chip--filter[aria-pressed="true"]', form).map(function (c) { return c.getAttribute('data-q'); }); }
	function line(form) { var t = one('[data-fg-line]', form); return t ? t.value.trim() : ''; }
	var give = one('[data-fg="give"]'), invite = one('[data-fg="invite"]'), sent = one('[data-fg="sent"]');
	all('[data-fg-switch]').forEach(function (b) {
		b.addEventListener('click', function () {
			var to = b.getAttribute('data-fg-switch');
			if (give) give.hidden = to !== 'give';
			if (invite) invite.hidden = to !== 'invite';
			if (sent) sent.hidden = true;
			var f = to === 'give' ? give : invite; if (f) { var i = f.querySelector('input'); if (i) i.focus(); }
		});
	});
	if (give) {
		wire(give);
		var q = one('[data-fg-q]', give), list = one('[data-fg-list]', give), chosen = one('[data-fg-chosen]', give), to = 0, toName = '', timer = 0;
		function pick(r) {
			to = r.id; toName = r.name;
			one('[data-fg-name]', chosen).textContent = r.name + (r.profession ? ' · ' + r.profession : '');
			chosen.hidden = false; q.hidden = true; list.hidden = true;
		}
		one('[data-fg-change]', give).addEventListener('click', function () { to = 0; chosen.hidden = true; q.hidden = false; q.value = ''; q.focus(); });
		q.addEventListener('input', function () {
			clearTimeout(timer);
			var v = q.value.trim();
			if (v.length < 2) { list.hidden = true; list.innerHTML = ''; return; }
			timer = setTimeout(function () {
				fetch(cfg.search + '?q=' + encodeURIComponent(v), { credentials: 'omit' }).then(function (r) { return r.json(); }).then(function (rows) {
					list.innerHTML = '';
					(rows || []).filter(function (r) { return r.id !== cfg.me; }).forEach(function (r) {
						var li = document.createElement('li'), b = document.createElement('button'), a = document.createElement('span'), s = document.createElement('small');
						b.type = 'button'; b.className = 'nlds-pick__item'; b.setAttribute('role', 'option');
						a.textContent = r.name; s.textContent = [r.profession, r.city].filter(Boolean).join(' · ');
						b.appendChild(a); b.appendChild(s); li.appendChild(b); list.appendChild(li);
						b.addEventListener('click', function () { pick(r); });
					});
					if (!list.children.length) { var li = document.createElement('li'), n = document.createElement('span'); n.className = 'nlds-pick__item'; n.textContent = 'לא נמצא. אפשר להזמין למטה.'; li.appendChild(n); list.appendChild(li); }
					list.hidden = false;
				}).catch(function () {});
			}, 250);
		});
		give.addEventListener('submit', function (e) {
			e.preventDefault();
			if (!to) { say(give, 'בחרו למי מפרגנים מתוך הרשימה.'); return; }
			if (!qualities(give).length && !line(give)) { say(give, 'בחרו תכונה אחת לפחות או כתבו משפט.'); return; }
			var btn = give.querySelector('[type="submit"]'); btn.disabled = true;
			post(cfg.endorse, { token: cfg.token, to: to, qualities: qualities(give), line: line(give) }).then(function (r) {
				btn.disabled = false;
				if (r.ok && r.j.ok) { say(give, 'הפרגון נשלח ויופיע בעמוד של ' + toName + '.', true); }
				else { say(give, r.j.message || oops); }
			}, function () { btn.disabled = false; say(give, oops); });
		});
	}
	if (invite) {
		wire(invite);
		invite.addEventListener('submit', function (e) {
			e.preventDefault();
			var name = one('[data-fg-iname]', invite).value.trim(), prof = one('[data-fg-iprof]', invite).value;
			if (name.length < 2 || !prof) { say(invite, 'חסרים פרטים. כל השדות המסומנים הם חובה.'); return; }
			if (!qualities(invite).length && !line(invite)) { say(invite, 'בחרו תכונה אחת לפחות או כתבו משפט.'); return; }
			var btn = invite.querySelector('[type="submit"]'); btn.disabled = true;
			post(cfg.endorse, { token: cfg.token, to: 0, invite_name: name, invite_profession: prof, qualities: qualities(invite), line: line(invite) }).then(function (r) {
				btn.disabled = false;
				if (!(r.ok && r.j.ok && r.j.join_url)) { say(invite, r.j.message || oops); return; }
				var url = r.j.join_url, text = 'פירגנתי לך באתר נדלן. הפרגון מחכה לך כאן: ' + url;
				one('[data-fg-sent-lead]', sent).textContent = 'שלחו אותה ל' + name + '. כשהכרטיס יעלה לאתר, הפרגון יופיע בו.';
				one('[data-fg-wa]', sent).setAttribute('href', 'https://wa.me/?text=' + encodeURIComponent(text));
				one('[data-fg-copy]', sent).onclick = function () {
					var b = this, done = function () { b.textContent = 'הקישור הועתק'; }, show = function () { b.textContent = url; b.style.direction = 'ltr'; };
					if (navigator.clipboard && navigator.clipboard.writeText) { navigator.clipboard.writeText(url).then(done, show); } else { show(); }
				};
				invite.hidden = true; sent.hidden = false;
			}, function () { btn.disabled = false; say(invite, oops); });
		});
	}
	var join = one('[data-fg="join"]');
	if (join) {
		var f = function (k) { return one('[data-fg-f="' + k + '"]', join); };
		var prof = f('profession'), gRow = one('[data-fg-gender-row]', join), gSel = f('gender');
		function genders() {
			var forms = (cfg.forms || {})[prof.value];
			gSel.innerHTML = '';
			if (!forms || forms[0] === forms[1]) { gRow.hidden = true; return; }
			[['m', forms[0]], ['f', forms[1]]].forEach(function (o) { var op = document.createElement('option'); op.value = o[0]; op.textContent = o[1]; gSel.appendChild(op); });
			gRow.hidden = false;
		}
		prof.addEventListener('change', genders); genders();
		join.addEventListener('submit', function (e) {
			e.preventDefault();
			var body = { name: f('name').value.trim(), profession: prof.value, gender: gRow.hidden ? '' : gSel.value, city: f('city').value.trim(), phone: f('phone').value.trim(),
				email: f('email').value.trim(), licence: f('licence').value.trim(), company: f('hp').value, consent: f('consent').checked ? 1 : 0, inv: cfg.inv || '' };
			if (body.name.length < 2 || !body.profession || body.city.length < 2 || !body.phone) { say(join, 'חסרים פרטים. כל השדות המסומנים הם חובה.'); return; }
			if (!/^0?5\d[\s-]?\d{3}[\s-]?\d{4}$/.test(body.phone.replace(/^\+?972/, '0'))) { say(join, 'צריך מספר נייד ישראלי.'); return; }
			if (!body.consent) { say(join, 'צריך לסמן את ההסכמה.'); return; }
			var btn = join.querySelector('[type="submit"]'); btn.disabled = true;
			post(cfg.join, body).then(function (r) {
				if (r.ok && r.j.ok) { say(join, 'הפרטים התקבלו. הכרטיס שלך יעלה לאתר אחרי בדיקה' + (cfg.inv ? ', והפרגון יופיע בו.' : '.'), true); all('input, select, textarea, button', join).forEach(function (x) { x.disabled = true; }); }
				else { btn.disabled = false; say(join, r.j.message || oops); }
			}, function () { btn.disabled = false; say(join, oops); });
		});
	}
})();
</script>
	<?php
}, 50 );

/* ---------------- joining: a pending card, checked in wp-admin before it goes up ---------------- */
add_action( 'rest_api_init', function () {
	register_rest_route( 'nadlan/v1', '/pros/join', array(
		'methods' => 'POST', 'permission_callback' => '__return_true',
		'callback' => function ( WP_REST_Request $req ) {
			if ( '' !== (string) $req->get_param( 'company' ) ) { return array( 'ok' => 1 ); } // the hidden field: a bot, answered quietly
			if ( ! nadlan_fg_on() ) { return new WP_Error( 'off', 'ההצטרפות סגורה כרגע', array( 'status' => 400 ) ); }
			$day = gmdate( 'Ymd' );
			$who = hash( 'sha256', $day . '|' . ( $_SERVER['REMOTE_ADDR'] ?? '' ) . '|' . wp_salt( 'nonce' ) ); // not stored: only a daily counter key
			$mine = (int) get_transient( 'nlfgj_' . substr( $who, 0, 32 ) );
			$all  = (int) get_option( 'nlfgj_day_' . $day, 0 );
			if ( $mine >= 5 || $all >= 60 ) { return new WP_Error( 'rate', 'נסו שוב מחר', array( 'status' => 429 ) ); }
			$name  = mb_substr( sanitize_text_field( (string) $req->get_param( 'name' ) ), 0, 80 );
			$prof  = sanitize_key( (string) $req->get_param( 'profession' ) );
			$city  = mb_substr( sanitize_text_field( (string) $req->get_param( 'city' ) ), 0, 40 );
			$phone = preg_replace( '/[^\d+]/', '', (string) $req->get_param( 'phone' ) );
			$email = sanitize_email( (string) $req->get_param( 'email' ) );
			$lic   = mb_substr( preg_replace( '/[^\p{L}\p{N}\/-]/u', '', (string) $req->get_param( 'licence' ) ), 0, 20 );
			$g     = (string) $req->get_param( 'gender' );
			$inv   = sanitize_key( (string) $req->get_param( 'inv' ) );
			$reg   = nadlan_pro_registry();
			$wa    = function_exists( 'nadlan_prof_wa_digits' ) ? nadlan_prof_wa_digits( $phone ) : '';
			if ( mb_strlen( $name ) < 2 || ! isset( $reg[ $prof ] ) || mb_strlen( $city ) < 2 ) { return new WP_Error( 'missing', 'חסרים פרטים. כל השדות המסומנים הם חובה.', array( 'status' => 400 ) ); }
			if ( '' === $wa || 0 !== strpos( $wa, '9725' ) ) { return new WP_Error( 'phone', 'צריך מספר נייד ישראלי.', array( 'status' => 400 ) ); }
			if ( '' !== $email && ! is_email( $email ) ) { return new WP_Error( 'email', 'כתובת המייל לא נראית תקינה.', array( 'status' => 400 ) ); }
			if ( 1 !== (int) $req->get_param( 'consent' ) ) { return new WP_Error( 'consent', 'צריך לסמן את ההסכמה.', array( 'status' => 400 ) ); }
			$dupe = get_posts( array( 'post_type' => 'nadlan_professional', 'post_status' => array( 'pending', 'draft' ), 'numberposts' => 1, 'fields' => 'ids',
				'meta_query' => array( array( 'key' => 'phone', 'value' => '0' . substr( $wa, 3 ) ), array( 'key' => 'source', 'value' => 'firgun_join' ) ) ) );
			if ( $dupe ) { return array( 'ok' => 1 ); } // already waiting for a check
			$id = wp_insert_post( array( 'post_type' => 'nadlan_professional', 'post_status' => 'pending', 'post_title' => $name ), true );
			if ( is_wp_error( $id ) ) { return new WP_Error( 'save', 'משהו לא עבד. נסו שוב בעוד רגע.', array( 'status' => 500 ) ); }
			update_post_meta( $id, 'profession', $prof );
			update_post_meta( $id, 'city', $city );
			update_post_meta( $id, 'phone', '0' . substr( $wa, 3 ) );
			update_post_meta( $id, 'source', 'firgun_join' );
			if ( in_array( $g, array( 'f', 'm' ), true ) ) { update_post_meta( $id, 'nl_gender', $g ); }
			if ( '' !== $email ) { update_post_meta( $id, '_nl_email', $email ); }
			if ( '' !== $lic ) { update_post_meta( $id, 'metavech' === $prof ? 'license_number' : 'registry_number', $lic ); }
			if ( preg_match( '/^[a-z0-9]{24}$/', $inv ) ) { update_post_meta( $id, '_nl_invite_token', $inv ); }
			update_post_meta( $id, '_nl_join', wp_json_encode( array( 'at' => gmdate( 'c' ), 'consent' => NADLAN_FG_CONSENT, 'invited' => '' !== $inv ) ) );
			set_transient( 'nlfgj_' . substr( $who, 0, 32 ), $mine + 1, DAY_IN_SECONDS );
			update_option( 'nlfgj_day_' . $day, $all + 1, false );
			return array( 'ok' => 1 );
		},
	) );
} );

/* the waiting endorsement attaches when the joined card goes up */
add_action( 'transition_post_status', function ( $new, $old, $post ) {
	if ( 'publish' !== $new || 'publish' === $old || ! $post || 'nadlan_professional' !== $post->post_type ) { return; }
	$tok = (string) get_post_meta( $post->ID, '_nl_invite_token', true );
	if ( '' !== $tok && function_exists( 'nadlan_endorse_attach_invite' ) ) {
		nadlan_endorse_attach_invite( $tok, $post->ID );
		delete_post_meta( $post->ID, '_nl_invite_token' );
	}
}, 10, 3 );

/* wp-admin: the ready /firgun/ link on a professional with an upload link, and a notice for cards waiting for a check */
add_action( 'add_meta_boxes_nadlan_professional', function ( $post ) {
	$tok = (string) get_post_meta( $post->ID, '_nl_drop_token', true );
	if ( '' === $tok || '1' !== (string) get_post_meta( $post->ID, 'nl_drop_on', true ) ) { return; }
	add_meta_box( 'nlfg_link_box', 'פרגונים: הקישור האישי', function ( $post ) use ( $tok ) {
		$url = add_query_arg( 't', $tok, home_url( '/firgun/' ) );
		echo '<p style="margin:0 0 4px">הקישור ששולחים לבעל המקצוע כדי לפרגן ולהזמין:</p><input type="text" readonly value="' . esc_attr( $url ) . '" style="width:100%;direction:ltr" onclick="this.select()">';
		echo '<p class="description">אותו קוד כמו בקישור השליחה. קישור חדש בתיבת הנכסים מחליף גם את זה.</p>';
	}, 'nadlan_professional', 'side', 'default' );
} );
add_action( 'admin_notices', function () {
	if ( ! current_user_can( 'edit_others_posts' ) ) { return; }
	$n = count( get_posts( array( 'post_type' => 'nadlan_professional', 'post_status' => 'pending', 'numberposts' => 50, 'fields' => 'ids',
		'meta_query' => array( array( 'key' => 'source', 'value' => 'firgun_join' ) ) ) ) );
	if ( $n < 1 ) { return; }
	echo '<div class="notice notice-info"><p>' . esc_html( $n . ' אנשי מקצוע ביקשו להצטרף דרך הפרגונים וממתינים לבדיקה.' ) . ' <a href="' . esc_url( admin_url( 'edit.php?post_type=nadlan_professional&post_status=pending' ) ) . '">לבדיקה</a></p></div>';
} );
