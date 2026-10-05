<?php
/**
 * DRAFT FOR MAIN'S REVIEW (HAD-436, 5.10.2026). NOT deployed, NOT in plugins/. Proposed home:
 * plugins/nadlan-config/inc/broker-exposure.php, added to the module list in nadlan-config.php next to 'brokers-list'.
 * Spec: docs/brokers/exposure-control-2026-10-05.md. Every surface reads it through function_exists() and nadlan_bx_on(),
 * so with the module missing or the option nadlan_bx_on = '0' every page is byte for byte what it is today.
 *
 * BrokerExposure: one source of truth for every place a broker shows (owner, 5.10.2026: "per broker, checkboxes for the
 * exposure level and which project pages; I raise or lower any broker at any time").
 *
 *   Store   one option, nadlan_broker_exposure: array( 'v' => 1, 'brokers' => array( <professional id> => entry ) ).
 *           entry = level (hidden | link | listed | projects | featured), projects (slug => languages), licence_ok,
 *           licence_note, menu, order, updated, by, log (the last 20 changes of this broker).
 *   Levels  a ladder; each level includes the ones under it:
 *           hidden    admins only (the card and the site pages are private)
 *           link      the broker's site is public by its address; nad-lan links to it from nowhere (the card stays private)
 *           listed    + the card is public: /brokers/ (by city), /professionals/, the profile page
 *           projects  + the BrokerSquare in the rail and the line in the "for sale" section of the checked project pages
 *           featured  + the BrokerFeatureCard at the top of /brokers/, first in every rail, and (when "menu" is ticked)
 *                     a named link in the header menu
 *   Gate    no public level without a licence number and a confirmed licence (Ben's tick, or the register's verified_at):
 *           reg. 19(a) puts the licence on every publication, and the site is a publisher, never a broker (s.2(c)).
 *   Legacy  a broker with no entry keeps today's behaviour (published = listed; tier pro/studio or pinned = featured; the
 *           stage config's 'rail' on the Hebrew page), EXCEPT a card created after the release (nadlan_bx_since), which
 *           starts hidden (a self-serve sign-up from x-broker-join starts at nadlan_bx_join_level, 'listed' until Ben says).
 *   Preview an administrator adds ?nlbx_preview=<id> (or =all) to any page and sees what the entry asks for, never cached;
 *           anonymous HTML never carries a hidden broker.
 */
if ( ! defined( 'ABSPATH' ) ) { exit; }

if ( ! function_exists( 'nadlan_bx_on' ) ) {
	function nadlan_bx_on() {
		return '1' === (string) get_option( 'nadlan_bx_on', '1' );
	}
}

if ( ! function_exists( 'nadlan_bx_levels' ) ) {
	/** key => array( rank, the label on the admin screen ). */
	function nadlan_bx_levels() {
		return array(
			'hidden'   => array( 0, 'מוסתר: רק מנהלים רואים' ),
			'link'     => array( 1, 'אתר בקישור ישיר בלבד' ),
			'listed'   => array( 2, 'במדריך המתווכים' ),
			'projects' => array( 3, 'גם בעמודי הפרויקטים שסומנו' ),
			'featured' => array( 4, 'מומלץ: ראשון בכל מקום' ),
		);
	}
}

if ( ! function_exists( 'nadlan_bx_langs' ) ) {
	function nadlan_bx_langs() { return array( 'he', 'en', 'fr', 'ru', 'ar' ); }
}

if ( ! function_exists( 'nadlan_bx_store' ) ) {
	/** The whole store, normalised once per request. $fresh = true after a write. */
	function nadlan_bx_store( $fresh = false ) {
		static $memo = null;
		if ( null !== $memo && ! $fresh ) { return $memo; }
		$raw  = get_option( 'nadlan_broker_exposure', array() );
		$raw  = is_array( $raw ) ? $raw : array();
		$out  = array( 'v' => 1, 'brokers' => array() );
		$lv   = nadlan_bx_levels();
		foreach ( (array) ( $raw['brokers'] ?? array() ) as $pro => $e ) {
			$pro = (int) $pro;
			if ( $pro <= 0 || ! is_array( $e ) ) { continue; }
			$projects = array();
			foreach ( (array) ( $e['projects'] ?? array() ) as $slug => $langs ) {
				$slug = sanitize_title( (string) $slug );
				$langs = array_values( array_intersect( nadlan_bx_langs(), array_map( 'strval', (array) $langs ) ) );
				if ( '' !== $slug && $langs ) { $projects[ $slug ] = $langs; }
			}
			$out['brokers'][ $pro ] = array(
				'level'        => isset( $lv[ (string) ( $e['level'] ?? '' ) ] ) ? (string) $e['level'] : 'hidden',
				'projects'     => $projects,
				'licence_ok'   => ! empty( $e['licence_ok'] ) ? 1 : 0,
				'licence_note' => (string) ( $e['licence_note'] ?? '' ),
				'menu'         => ! empty( $e['menu'] ) ? 1 : 0,
				'order'        => (int) ( $e['order'] ?? 50 ),
				'updated'      => (int) ( $e['updated'] ?? 0 ),
				'by'           => (int) ( $e['by'] ?? 0 ),
				'log'          => array_slice( (array) ( $e['log'] ?? array() ), 0, 20 ),
			);
		}
		$memo = $out;
		return $memo;
	}
}

if ( ! function_exists( 'nadlan_bx_entry' ) ) {
	function nadlan_bx_entry( $pro ) {
		$s = nadlan_bx_store();
		return $s['brokers'][ (int) $pro ] ?? null;
	}
}

if ( ! function_exists( 'nadlan_bx_is_broker' ) ) {
	function nadlan_bx_is_broker( $pro ) {
		$pro = (int) $pro;
		return $pro > 0 && 'nadlan_professional' === get_post_type( $pro ) && 'metavech' === (string) get_post_meta( $pro, 'profession', true );
	}
}

if ( ! function_exists( 'nadlan_bx_is_new' ) ) {
	/** A card created after the release: no entry means the default (hidden), not today's behaviour. */
	function nadlan_bx_is_new( $pro ) {
		$since = (int) get_option( 'nadlan_bx_since', 0 );
		if ( $since <= 0 ) { return false; }
		$t = strtotime( (string) get_post_field( 'post_date_gmt', (int) $pro ) . ' UTC' );
		return $t && $t >= $since;
	}
}

if ( ! function_exists( 'nadlan_bx_rank' ) ) {
	/** 0 hidden .. 4 featured. */
	function nadlan_bx_rank( $pro ) {
		$pro = (int) $pro;
		$e   = nadlan_bx_entry( $pro );
		$lv  = nadlan_bx_levels();
		if ( $e ) { return (int) $lv[ $e['level'] ][0]; }
		if ( nadlan_bx_is_new( $pro ) ) {
			if ( 'broker_join' === (string) get_post_meta( $pro, 'source', true ) ) {
				$j = (string) get_option( 'nadlan_bx_join_level', 'listed' );
				return isset( $lv[ $j ] ) ? (int) $lv[ $j ][0] : 2;
			}
			return 0;
		}
		// legacy: exactly what brokers-list.php and the stage config do today
		if ( 'publish' !== get_post_status( $pro ) ) { return 0; }
		$tier   = (string) get_post_meta( $pro, 'nl_tier', true );
		$pinned = in_array( (string) get_post_meta( $pro, 'is_pinned', true ), array( '1', 'yes', 'true', 'on' ), true );
		return ( $pinned || in_array( $tier, array( 'pro', 'studio' ), true ) ) ? 4 : 2;
	}
}

if ( ! function_exists( 'nadlan_bx_publishable' ) ) {
	/**
	 * The licence gate for every public level. A legacy broker (no entry, card older than the release) keeps today's rule
	 * (published and not a demo), so /brokers/ does not change by a single card on release day.
	 */
	function nadlan_bx_publishable( $pro ) {
		$pro = (int) $pro;
		if ( get_post_meta( $pro, 'is_demo', true ) || 'demo_seed' === (string) get_post_meta( $pro, 'source', true ) ) { return false; }
		$e = nadlan_bx_entry( $pro );
		if ( ! $e && ! nadlan_bx_is_new( $pro ) ) { return true; }
		if ( '' === trim( (string) get_post_meta( $pro, 'license_number', true ) ) ) { return false; }
		if ( $e && $e['licence_ok'] ) { return true; }
		return function_exists( 'nadlan_dir_registry_verified' ) ? (bool) nadlan_dir_registry_verified( $pro ) : (int) get_post_meta( $pro, 'verified_at', true ) > 0;
	}
}

if ( ! function_exists( 'nadlan_bx_preview' ) ) {
	/** An administrator's preview of one broker (or all): ?nlbx_preview=<id>|all. Never cached. */
	function nadlan_bx_preview( $pro = 0 ) {
		static $nocache = false;
		if ( is_admin() || ! isset( $_GET['nlbx_preview'] ) || ! current_user_can( 'manage_options' ) ) { return false; } // phpcs:ignore WordPress.Security.NonceVerification
		$want = sanitize_key( wp_unslash( $_GET['nlbx_preview'] ) ); // phpcs:ignore WordPress.Security.NonceVerification
		if ( '' === $want ) { return false; }
		if ( ! $nocache ) {
			$nocache = true;
			do_action( 'litespeed_control_set_nocache', 'nadlan broker exposure preview' );
			if ( ! headers_sent() ) { nocache_headers(); header( 'X-LiteSpeed-Cache-Control: no-cache' ); }
		}
		return 'all' === $want || ( (int) $pro > 0 && (string) (int) $pro === $want ) || 0 === (int) $pro;
	}
}

if ( ! function_exists( 'nadlan_bx_projects_of' ) ) {
	/** slug => languages. The entry's ticks; with no entry, the stage config's Hebrew rail (today's behaviour). */
	function nadlan_bx_projects_of( $pro ) {
		$pro = (int) $pro;
		$e   = nadlan_bx_entry( $pro );
		if ( $e ) { return $e['projects']; }
		$out = array();
		foreach ( ( function_exists( 'nadlan_ps_config' ) ? nadlan_ps_config() : array() ) as $slug => $cfg ) {
			if ( in_array( $pro, array_map( 'intval', (array) ( $cfg['rail'] ?? array() ) ), true ) ) { $out[ $slug ] = array( 'he' ); }
		}
		return $out;
	}
}

if ( ! function_exists( 'nadlan_bx_can' ) ) {
	/**
	 * THE read API. $surface: site | card | directory | project | featured | menu. $project is a stage slug without the
	 * language suffix ('hamedina'), $lang one of he en fr ru ar.
	 */
	function nadlan_bx_can( $pro, $surface, $project = '', $lang = 'he' ) {
		$pro = (int) $pro;
		if ( ! nadlan_bx_is_broker( $pro ) ) { return false; }
		$need = array( 'site' => 1, 'card' => 2, 'directory' => 2, 'project' => 3, 'featured' => 4, 'menu' => 4 );
		if ( ! isset( $need[ $surface ] ) ) { return false; }
		$on_project = function () use ( $pro, $project, $lang ) {
			$p = nadlan_bx_projects_of( $pro );
			return '' !== $project && isset( $p[ $project ] ) && in_array( $lang, $p[ $project ], true );
		};
		if ( nadlan_bx_preview( $pro ) ) {
			// the preview shows what the entry asks for at any level: the ticked projects, the ticked menu, the directory, the site
			if ( 'project' === $surface ) { return $on_project(); }
			if ( 'menu' === $surface ) { $e = nadlan_bx_entry( $pro ); return $e && $e['menu']; }
			return true;
		}
		if ( nadlan_bx_rank( $pro ) < $need[ $surface ] || ! nadlan_bx_publishable( $pro ) ) { return false; }
		if ( 'project' === $surface ) { return $on_project(); }
		if ( 'menu' === $surface ) { $e = nadlan_bx_entry( $pro ); return $e && $e['menu']; }
		return true;
	}
}

if ( ! function_exists( 'nadlan_bx_project_brokers' ) ) {
	/** The brokers of a project page in a language: featured first, then the entry's order, at most 3. */
	function nadlan_bx_project_brokers( $slug, $lang = 'he' ) {
		$slug = preg_replace( '/-(en|fr|ru|ar)$/', '', (string) $slug );
		$cand = array_keys( nadlan_bx_store()['brokers'] );
		$cfg  = function_exists( 'nadlan_ps_config' ) ? nadlan_ps_config() : array();
		foreach ( (array) ( $cfg[ $slug ]['rail'] ?? array() ) as $legacy ) { $cand[] = (int) $legacy; }
		$ids = array();
		foreach ( array_unique( array_map( 'intval', $cand ) ) as $pro ) {
			if ( 'he' !== $lang && '' === trim( (string) get_post_meta( $pro, 'nl_name_en', true ) ) ) { continue; } // never Hebrew on a language page
			if ( nadlan_bx_can( $pro, 'project', $slug, $lang ) ) { $ids[] = $pro; }
		}
		usort( $ids, function ( $a, $b ) {
			$fa = nadlan_bx_rank( $a ) >= 4 ? 0 : 1;
			$fb = nadlan_bx_rank( $b ) >= 4 ? 0 : 1;
			if ( $fa !== $fb ) { return $fa - $fb; }
			$oa = (int) ( nadlan_bx_entry( $a )['order'] ?? 50 );
			$ob = (int) ( nadlan_bx_entry( $b )['order'] ?? 50 );
			return $oa === $ob ? $a - $b : $oa - $ob;
		} );
		return array_slice( $ids, 0, 3 );
	}
}

/* ------------------------------------------------------------------ words in five languages (DRAFT: the language gate
   and a native read come before release; Hebrew follows the existing BrokerSquare) */
if ( ! function_exists( 'nadlan_bx_t' ) ) {
	function nadlan_bx_t( $lang, $k ) {
		static $T = array(
			'he' => array( 'ad' => 'פרסומת', 'role_m' => 'מתווך במקרקעין', 'role_f' => 'מתווכת במקרקעין', 'lic' => 'רישיון', 'wa' => 'התייעצות בוואטסאפ',
				'site' => 'לאתר של %s', 'strip' => 'מתווכים שפעילים ב%s', 'preview' => 'תצוגה למנהל בלבד', 'rail' => 'אנשי מקצוע באזור',
				'wa_text' => 'שלום %1$s, ראיתי את הכרטיס שלך בעמוד של %2$s באתר nad-lan.co.il ואשמח להתייעץ' ),
			'en' => array( 'ad' => 'Advertisement', 'role_m' => 'Licensed real estate broker', 'role_f' => 'Licensed real estate broker', 'lic' => 'licence no.', 'wa' => 'Chat on WhatsApp',
				'site' => '%s’s site', 'strip' => 'Brokers active in %s', 'preview' => 'Admin preview only', 'rail' => 'Professionals in the area',
				'wa_text' => 'Hello %1$s, I saw your card on the %2$s page on nad-lan.co.il and would like to talk' ),
			'fr' => array( 'ad' => 'Publicité', 'role_m' => 'Agent immobilier agréé', 'role_f' => 'Agente immobilière agréée', 'lic' => 'licence n°', 'wa' => 'Écrire sur WhatsApp',
				'site' => 'Le site de %s', 'strip' => 'Agents immobiliers actifs : %s', 'preview' => 'Aperçu administrateur', 'rail' => 'Professionnels du quartier',
				'wa_text' => 'Bonjour %1$s, j’ai vu votre fiche sur la page %2$s de nad-lan.co.il et je souhaite échanger' ),
			'ru' => array( 'ad' => 'Реклама', 'role_m' => 'Лицензированный риелтор', 'role_f' => 'Лицензированный риелтор', 'lic' => 'лицензия №', 'wa' => 'Написать в WhatsApp',
				'site' => 'Сайт: %s', 'strip' => 'Риелторы проекта «%s»', 'preview' => 'Только для администратора', 'rail' => 'Специалисты района',
				'wa_text' => 'Здравствуйте, %1$s! Я увидел вашу карточку на странице «%2$s» на nad-lan.co.il и хочу проконсультироваться' ),
			'ar' => array( 'ad' => 'إعلان', 'role_m' => 'وسيط عقاري مرخّص', 'role_f' => 'وسيطة عقارية مرخّصة', 'lic' => 'رخصة رقم', 'wa' => 'تواصل عبر واتساب',
				'site' => 'موقع %s', 'strip' => 'وسطاء عقاريون يعملون في %s', 'preview' => 'معاينة للمدير فقط', 'rail' => 'مختصون في المنطقة',
				'wa_text' => 'مرحباً %1$s، رأيت بطاقتك في صفحة %2$s على nad-lan.co.il وأودّ الاستفسار' ),
		);
		$lang = isset( $T[ $lang ] ) ? $lang : 'en';
		return $T[ $lang ][ $k ] ?? '';
	}
}

if ( ! function_exists( 'nadlan_bx_name' ) ) {
	/** The broker's name in a language; '' when that language has none (the caller then skips the broker). */
	function nadlan_bx_name( $pro, $lang ) {
		$m  = function ( $k ) use ( $pro ) { return trim( (string) get_post_meta( (int) $pro, $k, true ) ); };
		if ( 'he' === $lang ) {
			if ( '' !== $m( 'nl_name_he' ) ) { return $m( 'nl_name_he' ); }
			return function_exists( 'nadlan_prof_person_name' ) ? (string) nadlan_prof_person_name( (int) $pro ) : get_the_title( (int) $pro );
		}
		if ( 'ru' === $lang && '' !== $m( 'nl_name_ru' ) ) { return $m( 'nl_name_ru' ); }
		return $m( 'nl_name_en' );
	}
}

if ( ! function_exists( 'nadlan_bx_brand' ) ) {
	function nadlan_bx_brand( $pro, $lang ) {
		$he = trim( (string) get_post_meta( (int) $pro, 'company_name', true ) );
		if ( 'he' === $lang ) { return $he; }
		$en = trim( (string) get_post_meta( (int) $pro, 'nl_brand_en', true ) );
		return '' !== $en ? $en : ( preg_match( '/\p{Hebrew}/u', $he ) ? '' : $he );
	}
}

if ( ! function_exists( 'nadlan_bx_site_url' ) ) {
	/** The broker's site in the reader's language, else English, else Hebrew; a private page only in the preview. */
	function nadlan_bx_site_url( $pro, $lang = 'he' ) {
		$order = array( 'he' => array( 'he' ), 'en' => array( 'en', 'he' ), 'fr' => array( 'fr', 'en', 'he' ), 'ru' => array( 'ru', 'en', 'he' ), 'ar' => array( 'en', 'he' ) );
		$ok    = nadlan_bx_preview( $pro ) ? array( 'publish', 'private' ) : array( 'publish' );
		foreach ( $order[ $lang ] ?? array( 'en', 'he' ) as $l ) {
			$id = (int) get_post_meta( (int) $pro, 'nl_site_' . $l, true );
			if ( $id > 0 && in_array( get_post_status( $id ), $ok, true ) && nadlan_bx_can( $pro, 'site' ) ) { return (string) get_permalink( $id ); }
		}
		return nadlan_bx_can( $pro, 'card' ) ? (string) get_permalink( (int) $pro ) : '';
	}
}

if ( ! function_exists( 'nadlan_bx_licence_line' ) ) {
	/** Reg. 19(a): "<role> · licence <n>", in the reader's language. */
	function nadlan_bx_licence_line( $pro, $lang ) {
		$lic = trim( (string) get_post_meta( (int) $pro, 'license_number', true ) );
		$f   = 'f' === (string) get_post_meta( (int) $pro, 'nl_gender', true );
		$role = nadlan_bx_t( $lang, $f ? 'role_f' : 'role_m' );
		return '' === $lic ? $role : $role . ' · ' . nadlan_bx_t( $lang, 'lic' ) . ' ' . $lic;
	}
}

if ( ! function_exists( 'nadlan_bx_project_name' ) ) {
	function nadlan_bx_project_name( $ps, $lang ) {
		if ( 'he' === $lang ) { return (string) ( $ps['name'] ?? '' ); }
		if ( ! empty( $ps['i18n'][ $lang ]['name'] ) ) { return (string) $ps['i18n'][ $lang ]['name']; }
		return (string) ( $ps['name_en'] ?? '' );
	}
}

if ( ! function_exists( 'nadlan_bx_areas' ) ) {
	/** The broker's areas in a language (areas_served in Hebrew, nl_areas_<lang> elsewhere, English for Arabic); never Hebrew off he. */
	function nadlan_bx_areas( $pro, $lang, $max = 3 ) {
		$k = 'he' === $lang ? 'areas_served' : 'nl_areas_' . ( 'ar' === $lang ? 'en' : $lang );
		$a = array_filter( array_map( 'trim', explode( ',', (string) get_post_meta( (int) $pro, $k, true ) ) ) );
		if ( ! $a && 'he' !== $lang ) { $a = array_filter( array_map( 'trim', explode( ',', (string) get_post_meta( (int) $pro, 'nl_areas_en', true ) ) ) ); }
		if ( 'he' !== $lang ) { $a = array_filter( $a, function ( $x ) { return ! preg_match( '/\p{Hebrew}/u', $x ); } ); }
		return array_slice( array_values( $a ), 0, $max );
	}
}

if ( ! function_exists( 'nadlan_bx_square_html' ) ) {
	/**
	 * BrokerSquare in the page's language. The Hebrew output keeps today's nadlan_ps_square content (role and areas, the
	 * licence, the recommendations) and adds the office name to the role line; the other languages say the same in theirs.
	 */
	function nadlan_bx_square_html( $pro, $ps ) {
		$pro  = (int) $pro;
		$lang = (string) ( $ps['lang'] ?? 'he' );
		$slug = (string) ( $ps['slug'] ?? '' );
		if ( ! nadlan_bx_can( $pro, 'project', $slug, $lang ) ) { return ''; }
		$name = nadlan_bx_name( $pro, $lang );
		$href = nadlan_bx_site_url( $pro, $lang );
		if ( '' === $name || '' === $href ) { return ''; }
		$he    = 'he' === $lang;
		$rtl   = in_array( $lang, array( 'he', 'ar' ), true );
		$brand = nadlan_bx_brand( $pro, $lang );
		$f     = 'f' === (string) get_post_meta( $pro, 'nl_gender', true );
		$role  = $he && function_exists( 'nadlan_dir_prof_label' ) ? (string) nadlan_dir_prof_label( 'metavech', $pro ) : nadlan_bx_t( $lang, $f ? 'role_f' : 'role_m' );
		$areas = nadlan_bx_areas( $pro, $lang );
		$lic   = trim( (string) get_post_meta( $pro, 'license_number', true ) );
		$first = (string) preg_split( '/\s+/u', $name )[0];
		$wa    = function_exists( 'nadlan_prof_wa_digits' ) ? (string) nadlan_prof_wa_digits( (string) get_post_meta( $pro, 'phone', true ) ) : '';
		$text  = $he ? 'שלום ' . $name . ', ראיתי את הכרטיס שלך בעמוד של ' . (string) ( $ps['name'] ?? '' ) . ' באתר nad-lan.co.il ואשמח להתייעץ' // today's words
			: sprintf( nadlan_bx_t( $lang, 'wa_text' ), $first, nadlan_bx_project_name( $ps, $lang ) );
		$photo = has_post_thumbnail( $pro ) ? get_the_post_thumbnail( $pro, 'medium_large', array( 'alt' => $name, 'loading' => 'lazy' ) ) : '<span class="nlds-mono" aria-hidden="true">' . esc_html( mb_substr( $name, 0, 1 ) ) . '</span>';
		$ev    = ' data-nlps-ev="rail" data-nlps-pro="' . $pro . '" data-nlbx-slot="' . esc_attr( 'bx-' . $slug . '-' . $lang ) . '"';
		$prev  = nadlan_bx_rank( $pro ) < 3 || ! nadlan_bx_publishable( $pro ) ? '<span class="nlbx-preview">' . esc_html( nadlan_bx_t( $lang, 'preview' ) ) . '</span>' : '';
		$GLOBALS['nadlan_bx_on_page'] = true;
		$h  = '<div class="nlds" dir="' . ( $rtl ? 'rtl' : 'ltr' ) . '" lang="' . esc_attr( $lang ) . '"><article class="nlbsq" data-nlbx="' . $pro . '">';
		$h .= '<figure class="nlbsq__photo"><span class="nlbsq__ad">' . esc_html( nadlan_bx_t( $lang, 'ad' ) ) . '</span>' . $prev . $photo . '</figure>';
		$h .= '<div class="nlbsq__body"><h3 class="nlbsq__name"><a href="' . esc_url( $href ) . '"' . $ev . '>' . esc_html( $name ) . '</a></h3>';
		$h .= '<p class="nlbsq__role"><b>' . esc_html( $role ) . '</b>' . ( '' !== $brand ? ' · ' . esc_html( $brand ) : '' ) . ( $areas ? ' · ' . esc_html( implode( ', ', $areas ) ) : '' ) . '</p>';
		if ( '' !== $lic ) { $h .= '<p class="nlbsq__lic">' . ( $he ? 'רישיון תיווך' : esc_html( ucfirst( nadlan_bx_t( $lang, 'lic' ) ) ) ) . ' <span class="nlds-num">' . esc_html( $lic ) . '</span></p>'; }
		$recs = $he && function_exists( 'nadlan_endorse_counts' ) ? ( nadlan_endorse_counts( array( $pro ) )[ $pro ] ?? 0 ) : 0;
		if ( $recs > 0 && function_exists( 'nadlan_endorse_count_html' ) ) { $h .= '<p class="nlbsq__recs">' . nadlan_endorse_count_html( $recs, true ) . '</p>'; }
		$h .= '<div class="nlbsq__cta">';
		$h .= '' !== $wa
			? '<a class="nlds-btn nlds-btn--primary" target="_blank" rel="noopener" href="https://wa.me/' . esc_attr( $wa ) . '?text=' . rawurlencode( $text ) . '"' . $ev . ' data-nlps-wa="1">' . ( function_exists( 'nlds_icon' ) ? nlds_icon( 'whatsapp' ) : '' ) . '<span>' . esc_html( nadlan_bx_t( $lang, 'wa' ) ) . '</span></a>'
			: '';
		// the site button: the owner's order is "a click opens his mini-site" (the name already does; this is the obvious one)
		$h .= '<a class="nlds-btn nlds-btn--secondary" href="' . esc_url( $href ) . '"' . $ev . '><span>' . esc_html( sprintf( nadlan_bx_t( $lang, 'site' ), $first ) ) . '</span></a>';
		$h .= '</div></div></article></div>';
		return $h;
	}
}

if ( ! function_exists( 'nadlan_bx_strip_html' ) ) {
	/** The line in the article's "for sale" section: who sells in the towers, one row per broker, each row to the site. */
	function nadlan_bx_strip_html( $ids, $ps ) {
		$lang = (string) ( $ps['lang'] ?? 'he' );
		$rows = '';
		foreach ( (array) $ids as $pro ) {
			$name = nadlan_bx_name( $pro, $lang );
			$href = nadlan_bx_site_url( $pro, $lang );
			if ( '' === $name || '' === $href ) { continue; }
			$brand = nadlan_bx_brand( $pro, $lang );
			$first = (string) preg_split( '/\s+/u', $name )[0];
			$ev    = ' data-nlbx-ev="strip" data-nlps-pro="' . (int) $pro . '" data-nlbx-slot="' . esc_attr( 'bx-' . $ps['slug'] . '-' . $lang . '-sale' ) . '"';
			$rows .= '<li class="nlbx-strip__row" data-nlbx="' . (int) $pro . '"><p class="nlbx-strip__who"><a href="' . esc_url( $href ) . '"' . $ev . '><b>' . esc_html( $name ) . '</b></a>'
				. ( '' !== $brand ? ' · ' . esc_html( $brand ) : '' ) . '<br><small>' . esc_html( nadlan_bx_licence_line( $pro, $lang ) ) . '</small></p>'
				. '<a class="nlds-btn nlds-btn--secondary" href="' . esc_url( $href ) . '"' . $ev . '><span>' . esc_html( sprintf( nadlan_bx_t( $lang, 'site' ), $first ) ) . '</span></a></li>';
		}
		if ( '' === $rows ) { return ''; }
		$GLOBALS['nadlan_bx_on_page'] = true;
		$rtl = in_array( $lang, array( 'he', 'ar' ), true );
		return '<aside class="nlds nlbx-strip" dir="' . ( $rtl ? 'rtl' : 'ltr' ) . '" lang="' . esc_attr( $lang ) . '" aria-label="' . esc_attr( sprintf( nadlan_bx_t( $lang, 'strip' ), nadlan_bx_project_name( $ps, $lang ) ) ) . '">'
			. '<p class="nlds-kicker nlbx-strip__ad">' . esc_html( nadlan_bx_t( $lang, 'ad' ) ) . '</p>'
			. '<p class="nlbx-strip__h">' . esc_html( sprintf( nadlan_bx_t( $lang, 'strip' ), nadlan_bx_project_name( $ps, $lang ) ) ) . '</p>'
			. '<ul class="nlbx-strip__list">' . $rows . '</ul></aside>';
	}
}

if ( ! function_exists( 'nadlan_bx_strip_insert' ) ) {
	/**
	 * Called by nadlan_ps_compose() on the finished HTML. Inside section#nlws-sale: right after the paragraph that links to
	 * the brokers directory (/brokers/, /en/brokers/ ...), else before the section closes. Fails open: no section, no line.
	 */
	function nadlan_bx_strip_insert( $html, $ps ) {
		if ( ! nadlan_bx_on() || '0' === (string) get_option( 'nadlan_bx_strip', '1' ) || ! is_string( $html ) || false !== strpos( $html, 'class="nlds nlbx-strip"' ) ) { return $html; }
		$at = strpos( $html, 'id="nlws-sale"' );
		if ( false === $at ) { return $html; }
		$start = strrpos( substr( $html, 0, $at ), '<section' );
		if ( false === $start || ! function_exists( 'nadlan_ps_close' ) ) { return $html; }
		$end = nadlan_ps_close( $html, $start, 'section' );
		if ( ! $end ) { return $html; }
		$ids = nadlan_bx_project_brokers( (string) ( $ps['slug'] ?? '' ), (string) ( $ps['lang'] ?? 'he' ) );
		if ( ! $ids ) { return $html; }
		$strip = nadlan_bx_strip_html( $ids, $ps );
		if ( '' === $strip ) { return $html; }
		$sec = substr( $html, $start, $end - $start );
		$pos = false;
		if ( preg_match( '#href="[^"]*/brokers/"#', $sec, $m, PREG_OFFSET_CAPTURE ) ) {
			$p = strpos( $sec, '</p>', $m[0][1] );
			if ( false !== $p ) { $pos = $start + $p + 4; }
		}
		if ( false === $pos ) { $pos = $end - strlen( '</section>' ); }
		return substr( $html, 0, $pos ) . $strip . substr( $html, $pos );
	}
}

if ( ! function_exists( 'nadlan_bx_menu_links' ) ) {
	/** Header menu ("אנשי מקצוע" > "המאגר"): the featured brokers whose "menu" box is ticked, each to the site. */
	function nadlan_bx_menu_links( $lang = 'he' ) {
		if ( ! nadlan_bx_on() ) { return array(); }
		$out = array();
		foreach ( array_keys( nadlan_bx_store()['brokers'] ) as $pro ) {
			if ( ! nadlan_bx_can( $pro, 'menu' ) ) { continue; } // in a preview: the ticked box; otherwise featured + ticked + licence
			$name = nadlan_bx_name( $pro, $lang );
			$url  = nadlan_bx_site_url( $pro, $lang );
			if ( '' !== $name && '' !== $url ) { $out[ (int) ( nadlan_bx_entry( $pro )['order'] ?? 50 ) * 100000 + $pro ] = array( $name, $url ); }
		}
		ksort( $out );
		return array_slice( array_values( $out ), 0, 4 );
	}
}

/* The licence line on a handcrafted broker site (a page with nl_broker_site): the page holds <!--nlbx:licence--> and the
   line is read from the card at render time, so a licence confirmed later needs no rebuild of the page. */
add_filter( 'the_content', function ( $html ) {
	if ( ! nadlan_bx_on() || false === strpos( (string) $html, '<!--nlbx:licence-->' ) || ! is_page() ) { return $html; }
	$pid = (int) get_queried_object_id();
	$pro = (int) get_post_meta( $pid, 'nl_broker_site', true );
	if ( ! $pro ) { return $html; }
	$lang = (string) get_post_meta( $pid, 'nl_lang', true );
	$lang = in_array( $lang, nadlan_bx_langs(), true ) ? $lang : 'he';
	$lic  = trim( (string) get_post_meta( $pro, 'license_number', true ) );
	$line = '' !== $lic ? esc_html( nadlan_bx_licence_line( $pro, $lang ) ) : ( current_user_can( 'manage_options' ) ? '<mark>רישיון: ממתין לאישור של בן</mark>' : '' );
	return str_replace( '<!--nlbx:licence-->', $line, (string) $html );
}, 27 );

/* Rail and line clicks on pages without bridge.js (the world pages): GA, and the private insights table (place_view and
   place_click, the slot says which project and language). The insights endpoint drops events of an unpublished card. */
add_action( 'wp_footer', function () {
	if ( empty( $GLOBALS['nadlan_bx_on_page'] ) ) { return; }
	$url = esc_url_raw( rest_url( 'nadlan/v1/ev' ) );
	echo "\n<style id=\"nadlan-bx-css\">:root body .nlds .nlbx-preview{position:absolute;inset-block-start:8px;inset-inline-end:8px;z-index:2;padding:2px 8px;border-radius:999px;background:#7a1f1f;color:#fff;font:600 12px/1.6 Assistant,Arial,sans-serif}"
		. ':root body .nlds .nlbsq__lic{margin:2px 0 0!important;font-size:13px!important;color:var(--nlds-sa-ink2)!important}'
		. ':root body .nlds.nlbx-strip{margin:18px 0 22px!important;padding:14px 16px!important;border:1px solid var(--nlds-sa-line)!important;border-radius:var(--nlds-radius-16)!important;background:var(--nlds-sa-surf)!important}'
		. ':root body .nlbx-strip .nlbx-strip__h{margin:2px 0 10px!important;font-weight:700!important}:root body .nlbx-strip .nlbx-strip__list{list-style:none!important;margin:0!important;padding:0!important;display:grid;gap:10px}'
		. ':root body .nlbx-strip .nlbx-strip__row{display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:8px 14px}:root body .nlbx-strip .nlbx-strip__who{margin:0!important}'
		. ':root body .nlbx-strip .nlds-btn{min-height:44px}</style>' . "\n";
	echo '<script id="nadlan-bx-ev">(function(){var u=' . wp_json_encode( $url ) . ',post=' . (int) get_queried_object_id() . ';'
		. 'function b(e,pro,slot){if(!navigator.sendBeacon||!pro)return;try{navigator.sendBeacon(u,new Blob([JSON.stringify({e:e,pro:+pro,post:post,slot:slot})],{type:"application/json"}))}catch(_){}}'
		. 'document.querySelectorAll("[data-nlbx]").forEach(function(c){var a=c.querySelector("[data-nlbx-slot]");if(!a)return;var s=a.getAttribute("data-nlbx-slot");'
		. 'if("IntersectionObserver" in window){var o=new IntersectionObserver(function(x){if(x[0].isIntersecting){b("place_view",c.getAttribute("data-nlbx"),s);o.disconnect()}},{threshold:.5});o.observe(c)}});'
		. 'document.addEventListener("click",function(e){var a=e.target&&e.target.closest?e.target.closest("[data-nlbx-slot]"):null;if(!a)return;var pro=a.getAttribute("data-nlps-pro");'
		// GA: bridge.js already reports the rail on the four stage pages; here the world pages (no bridge.js) and the line
		. 'b("place_click",pro,a.getAttribute("data-nlbx-slot"));var strip=a.hasAttribute("data-nlbx-ev"),world=!!document.querySelector(".nlps-stage--world");'
		. 'if((strip||world)&&window.nadlanGA){try{window.nadlanGA(a.hasAttribute("data-nlps-wa")?"whatsapp_click":"pro_click",{source:strip?"project-sale":"project-rail",pro:pro})}catch(_){}}});})();</script>' . "\n";
}, 42 );

/* ================================================================== writes: the admin screen is the only writer */

if ( ! function_exists( 'nadlan_bx_set_status' ) ) {
	/**
	 * A status flip without re-saving the content (a broker site holds <style> and JSON-LD that a re-save through kses
	 * could strip). Only publish <-> private; a draft or a trashed page is never touched.
	 */
	function nadlan_bx_set_status( $id, $want ) {
		global $wpdb;
		$id  = (int) $id;
		$old = (string) get_post_status( $id );
		if ( $id <= 0 || $old === $want || ! in_array( $old, array( 'publish', 'private' ), true ) ) { return null; }
		$wpdb->update( $wpdb->posts, array( 'post_status' => $want ), array( 'ID' => $id ) );
		clean_post_cache( $id );
		wp_transition_post_status( $want, $old, get_post( $id ) );
		return array( $old, $want );
	}
}

if ( ! function_exists( 'nadlan_bx_sync_status' ) ) {
	/** The card is public from 'listed', the site pages from 'link'; under that both are private. */
	function nadlan_bx_sync_status( $pro, $rank ) {
		$done = array();
		$c    = nadlan_bx_set_status( $pro, $rank >= 2 ? 'publish' : 'private' );
		if ( $c ) { $done[ (int) $pro ] = $c; }
		foreach ( array( 'he', 'en', 'ru', 'fr' ) as $l ) {
			$sid = (int) get_post_meta( (int) $pro, 'nl_site_' . $l, true );
			if ( $sid > 0 ) {
				$s = nadlan_bx_set_status( $sid, $rank >= 1 ? 'publish' : 'private' );
				if ( $s ) { $done[ $sid ] = $s; }
			}
		}
		return $done;
	}
}

if ( ! function_exists( 'nadlan_bx_purge' ) ) {
	/** The pages a change touches; a change in the directory, the featured set or the menu clears the whole cache. */
	function nadlan_bx_purge( $pro, $projects, $all ) {
		$ids = array( (int) $pro );
		foreach ( array( 'he', 'en', 'ru', 'fr' ) as $l ) { $ids[] = (int) get_post_meta( (int) $pro, 'nl_site_' . $l, true ); }
		foreach ( (array) $projects as $slug ) {
			foreach ( array( '', '-en', '-fr', '-ru', '-ar' ) as $suf ) {
				$p = get_page_by_path( $slug . $suf, OBJECT, 'nadlan_project' );
				if ( $p ) { $ids[] = (int) $p->ID; }
			}
		}
		foreach ( array( 'brokers', 'en/brokers', 'ru/brokers', 'fr/brokers', 'professionals' ) as $path ) {
			$p = get_page_by_path( $path, OBJECT, 'page' );
			if ( $p ) { $ids[] = (int) $p->ID; }
		}
		foreach ( array_unique( array_filter( $ids ) ) as $id ) {
			clean_post_cache( $id );
			do_action( 'litespeed_purge_post', $id );
			$u = get_permalink( $id );
			if ( $u ) { do_action( 'litespeed_purge_url', $u ); }
		}
		if ( $all ) { do_action( 'litespeed_purge_all' ); }
	}
}

if ( ! function_exists( 'nadlan_bx_save' ) ) {
	/** Validates, applies the licence gate, writes the store, flips the statuses, logs, purges. Returns '' or an error word. */
	function nadlan_bx_save( $pro, $in ) {
		$pro = (int) $pro;
		if ( ! current_user_can( 'manage_options' ) ) { return 'forbidden'; }
		if ( ! nadlan_bx_is_broker( $pro ) ) { return 'not_a_broker'; }
		$lv     = nadlan_bx_levels();
		$store  = get_option( 'nadlan_broker_exposure', array() );
		$store  = is_array( $store ) ? $store : array();
		$store['v'] = 1;
		$before = nadlan_bx_entry( $pro );
		$old_rank = nadlan_bx_rank( $pro );
		$level  = isset( $lv[ (string) ( $in['level'] ?? '' ) ] ) ? (string) $in['level'] : 'hidden';
		$projects = array();
		foreach ( (array) ( $in['projects'] ?? array() ) as $slug => $langs ) {
			$slug  = sanitize_title( (string) $slug );
			$langs = array_values( array_intersect( nadlan_bx_langs(), array_map( 'sanitize_key', (array) $langs ) ) );
			if ( '' !== $slug && $langs ) { $projects[ $slug ] = $langs; }
		}
		$entry = array(
			'level'        => $level,
			'projects'     => $projects,
			'licence_ok'   => ! empty( $in['licence_ok'] ) ? 1 : 0,
			'licence_note' => mb_substr( sanitize_text_field( (string) ( $in['licence_note'] ?? '' ) ), 0, 200 ),
			'menu'         => ! empty( $in['menu'] ) ? 1 : 0,
			'order'        => max( 0, min( 999, (int) ( $in['order'] ?? 50 ) ) ),
			'updated'      => time(),
			'by'           => get_current_user_id(),
			'log'          => (array) ( $before['log'] ?? array() ),
		);
		// the licence gate, before anything is written
		$licence = trim( (string) get_post_meta( $pro, 'license_number', true ) );
		$registry = function_exists( 'nadlan_dir_registry_verified' ) && nadlan_dir_registry_verified( $pro );
		if ( $lv[ $level ][0] >= 1 && ( '' === $licence || ( ! $entry['licence_ok'] && ! $registry ) ) ) {
			return 'licence';
		}
		$store['brokers'][ $pro ] = $entry;
		$new_rank = (int) $lv[ $level ][0];
		array_unshift( $store['brokers'][ $pro ]['log'], array( 't' => time(), 'by' => get_current_user_id(), 'from' => $before ? $before['level'] : 'legacy:' . $old_rank, 'to' => $level, 'projects' => $projects ) );
		$store['brokers'][ $pro ]['log'] = array_slice( $store['brokers'][ $pro ]['log'], 0, 20 );
		update_option( 'nadlan_broker_exposure', $store, true );
		nadlan_bx_store( true );
		$flips = nadlan_bx_sync_status( $pro, $new_rank );
		if ( $flips ) {
			// the previous statuses ride in the log, so a rollback can put them back exactly
			$store['brokers'][ $pro ]['log'][0]['flips'] = $flips;
			update_option( 'nadlan_broker_exposure', $store, true );
			nadlan_bx_store( true );
		}
		if ( function_exists( 'nadlan_admin_control_audit' ) ) {
			nadlan_admin_control_audit( array( 'action' => 'broker_exposure', 'card_id' => $pro, 'field' => 'exposure',
				'old' => wp_json_encode( $before ? array( $before['level'], $before['projects'], $before['menu'] ) : array( 'legacy', $old_rank ) ),
				'new' => wp_json_encode( array( $level, $projects, $entry['menu'] ) ) ) );
		}
		$touched  = array_unique( array_merge( array_keys( (array) ( $before['projects'] ?? array() ) ), array_keys( $projects ) ) );
		$crossed  = ( $old_rank >= 2 ) !== ( $new_rank >= 2 ) || ( $old_rank >= 4 ) !== ( $new_rank >= 4 ) || (int) ( $before['menu'] ?? 0 ) !== $entry['menu'];
		nadlan_bx_purge( $pro, $touched, $crossed );
		return '';
	}
}

if ( ! function_exists( 'nadlan_bx_seed' ) ) {
	/**
	 * Called ONCE by the release runner through its bridge (never on load): the release time (cards created after it start
	 * hidden) and the entries that keep today's live state byte for byte. $entries: id => entry (see the spec, "migration").
	 */
	function nadlan_bx_seed( $entries ) {
		if ( ! current_user_can( 'manage_options' ) ) { return false; }
		if ( (int) get_option( 'nadlan_bx_since', 0 ) <= 0 ) { update_option( 'nadlan_bx_since', time(), true ); }
		$store = get_option( 'nadlan_broker_exposure', array() );
		$store = is_array( $store ) ? $store : array();
		$store['v'] = 1;
		foreach ( (array) $entries as $pro => $e ) {
			if ( ! isset( $store['brokers'][ (int) $pro ] ) ) { $store['brokers'][ (int) $pro ] = (array) $e + array( 'updated' => time(), 'by' => get_current_user_id(), 'log' => array() ); }
		}
		update_option( 'nadlan_broker_exposure', $store, true );
		nadlan_bx_store( true );
		return true;
	}
}

/* ================================================================== the admin screen: NadLan Ops > חשיפת מתווכים */

add_action( 'admin_menu', function () {
	if ( ! nadlan_bx_on() ) { return; }
	add_submenu_page( 'nadlan-ops', 'חשיפת מתווכים', 'חשיפת מתווכים', 'manage_options', 'nadlan-broker-exposure', 'nadlan_bx_screen' );
}, 31 );

add_action( 'admin_post_nadlan_bx_save', function () {
	if ( ! current_user_can( 'manage_options' ) ) { wp_die( 'forbidden' ); }
	check_admin_referer( 'nadlan_bx_save' );
	$pro = absint( $_POST['pro'] ?? 0 );
	$in  = array(
		'level'        => sanitize_key( wp_unslash( $_POST['level'] ?? 'hidden' ) ),
		'projects'     => isset( $_POST['projects'] ) && is_array( $_POST['projects'] ) ? wp_unslash( $_POST['projects'] ) : array(), // phpcs:ignore -- sanitised in nadlan_bx_save
		'licence_ok'   => ! empty( $_POST['licence_ok'] ),
		'licence_note' => sanitize_text_field( wp_unslash( $_POST['licence_note'] ?? '' ) ),
		'menu'         => ! empty( $_POST['menu'] ),
		'order'        => absint( $_POST['order'] ?? 50 ),
	);
	$err = nadlan_bx_save( $pro, $in );
	wp_safe_redirect( add_query_arg( array( 'page' => 'nadlan-broker-exposure', 'bx' => '' === $err ? 'saved' : $err, 'pro' => $pro ), admin_url( 'admin.php' ) ) . '#bx-' . $pro );
	exit;
} );

if ( ! function_exists( 'nadlan_bx_screen_brokers' ) ) {
	/** Every broker with an entry, every broker with a site or a paid plan or a pin, and the search results. */
	function nadlan_bx_screen_brokers( $s = '' ) {
		$ids = array_keys( nadlan_bx_store()['brokers'] );
		$base = array( 'post_type' => 'nadlan_professional', 'post_status' => array( 'publish', 'private', 'draft', 'pending' ), 'numberposts' => 200, 'fields' => 'ids', 'no_found_rows' => true, 'suppress_filters' => true );
		$ids = array_merge( $ids, get_posts( $base + array( 'meta_query' => array( 'relation' => 'AND',
			array( 'key' => 'profession', 'value' => 'metavech' ),
			array( 'relation' => 'OR',
				array( 'key' => 'nl_site_he', 'value' => '', 'compare' => '!=' ),
				array( 'key' => 'source', 'value' => array( 'broker_minisite', 'broker_join' ), 'compare' => 'IN' ),
				array( 'key' => 'nl_tier', 'value' => array( 'pro', 'studio' ), 'compare' => 'IN' ),
				array( 'key' => 'is_pinned', 'value' => '1' ) ) ) ) ) );
		if ( '' !== $s ) {
			$ids = array_merge( $ids, get_posts( $base + array( 's' => $s, 'numberposts' => 20, 'meta_query' => array( array( 'key' => 'profession', 'value' => 'metavech' ) ) ) ) );
			if ( preg_match( '/^\d{4,9}$/', $s ) ) {
				$ids = array_merge( $ids, get_posts( $base + array( 'numberposts' => 5, 'meta_query' => array( array( 'key' => 'license_number', 'value' => $s ) ) ) ) );
			}
		}
		return array_values( array_unique( array_map( 'intval', $ids ) ) );
	}
}

if ( ! function_exists( 'nadlan_bx_screen' ) ) {
	function nadlan_bx_screen() {
		if ( ! current_user_can( 'manage_options' ) ) { wp_die( 'forbidden' ); }
		$s     = isset( $_GET['s'] ) ? sanitize_text_field( wp_unslash( $_GET['s'] ) ) : ''; // phpcs:ignore
		$note  = isset( $_GET['bx'] ) ? sanitize_key( wp_unslash( $_GET['bx'] ) ) : ''; // phpcs:ignore
		$notes = array( 'saved' => array( 'success', 'נשמר. העמודים שהשתנו נוקו מהמטמון.' ), 'licence' => array( 'error', 'לא נשמר: לרמה ציבורית צריך מספר רישיון בכרטיס, וסימון "בדקתי את הרישיון" או אימות מהפנקס.' ),
			'forbidden' => array( 'error', 'אין הרשאה.' ), 'not_a_broker' => array( 'error', 'הכרטיס אינו של מתווך.' ) );
		$lv    = nadlan_bx_levels();
		$cfg   = function_exists( 'nadlan_ps_config' ) ? nadlan_ps_config() : array();
		echo '<div class="wrap" dir="rtl"><h1>חשיפת מתווכים</h1>';
		echo '<p>לכל מתווך: באיזו רמה הוא מופיע ובאילו עמודי פרויקט. כל רמה כוללת את מה שמתחתיה. ההחלטה כאן היא המקור היחיד לכל מקום שבו מתווך מופיע באתר. ההורדה ל"מוסתר" הופכת את האתר והכרטיס לפרטיים, ולכן גם מוציאה אותם ממפת האתר של גוגל.</p>';
		if ( isset( $notes[ $note ] ) ) { echo '<div class="notice notice-' . esc_attr( $notes[ $note ][0] ) . '"><p>' . esc_html( $notes[ $note ][1] ) . '</p></div>'; }
		echo '<form method="get"><input type="hidden" name="page" value="nadlan-broker-exposure"><p><input type="search" name="s" value="' . esc_attr( $s ) . '" placeholder="הוספת מתווך: שם או מספר רישיון"> <button class="button">חיפוש</button></p></form>';
		echo '<table class="widefat striped"><thead><tr><th>מתווך</th><th>רישיון</th><th>רמה</th><th>עמודי פרויקט</th><th>תפריט וסדר</th><th>תצוגה למנהל</th><th></th></tr></thead><tbody>';
		foreach ( nadlan_bx_screen_brokers( $s ) as $pro ) {
			if ( ! nadlan_bx_is_broker( $pro ) ) { continue; }
			$e     = nadlan_bx_entry( $pro );
			$rank  = nadlan_bx_rank( $pro );
			$cur   = $e ? $e['level'] : array_search( $rank, array_map( function ( $x ) { return $x[0]; }, $lv ), true );
			$lic   = trim( (string) get_post_meta( $pro, 'license_number', true ) );
			$reg   = function_exists( 'nadlan_dir_registry_verified' ) && nadlan_dir_registry_verified( $pro );
			$gate  = '' !== $lic && ( ( $e && $e['licence_ok'] ) || $reg );
			$proj  = nadlan_bx_projects_of( $pro );
			$form  = 'bxf-' . $pro;
			echo '<tr id="bx-' . (int) $pro . '"><td><b>' . esc_html( nadlan_bx_name( $pro, 'he' ) ) . '</b><br><small>' . esc_html( (string) get_post_meta( $pro, 'company_name', true ) ) . ' · #' . (int) $pro . ' · ' . esc_html( (string) get_post_status( $pro ) ) . ( $e ? '' : ' · ללא הגדרה (כמו היום)' ) . '</small></td>';
			echo '<td>' . ( '' !== $lic ? esc_html( $lic ) : '<b style="color:#a00">חסר</b>' ) . ( $reg ? '<br><small>מאומת בפנקס</small>' : '' )
				. '<br><label><input form="' . $form . '" type="checkbox" name="licence_ok" value="1"' . checked( $e && $e['licence_ok'], true, false ) . '> בדקתי את הרישיון</label>'
				. '<br><input form="' . $form . '" type="text" name="licence_note" value="' . esc_attr( $e['licence_note'] ?? '' ) . '" placeholder="איך ומתי נבדק" style="width:100%"></td>';
			echo '<td>';
			foreach ( $lv as $k => $row ) {
				$dis = $row[0] >= 1 && '' === $lic ? ' disabled' : '';
				echo '<label style="display:block"><input form="' . $form . '" type="radio" name="level" value="' . esc_attr( $k ) . '"' . checked( $cur, $k, false ) . $dis . '> ' . esc_html( $row[1] ) . '</label>';
			}
			if ( ! $gate ) { echo '<small style="color:#a00">רמה ציבורית נפתחת רק אחרי בדיקת רישיון.</small>'; }
			echo '</td><td>';
			foreach ( $cfg as $slug => $c ) {
				$on = isset( $proj[ $slug ] );
				echo '<fieldset style="margin:0 0 6px"><label><b><input form="' . $form . '" type="checkbox" class="bx-proj" data-slug="' . esc_attr( $slug ) . '"' . checked( $on, true, false ) . '> ' . esc_html( (string) ( $c['name'] ?? $slug ) ) . '</b></label><br>';
				foreach ( nadlan_bx_langs() as $l ) {
					$lon = $on ? in_array( $l, $proj[ $slug ], true ) : true; // a project ticked for the first time takes all five languages
					echo '<label style="margin-inline-end:6px"><input form="' . $form . '" type="checkbox" name="projects[' . esc_attr( $slug ) . '][]" value="' . esc_attr( $l ) . '"' . checked( $lon, true, false ) . '> ' . esc_html( $l ) . '</label>';
				}
				echo '</fieldset>';
			}
			echo '</td><td><label><input form="' . $form . '" type="checkbox" name="menu" value="1"' . checked( $e && $e['menu'], true, false ) . '> בתפריט (רק ברמת "מומלץ")</label><br>סדר <input form="' . $form . '" type="number" name="order" value="' . (int) ( $e['order'] ?? 50 ) . '" min="0" max="999" style="width:70px"></td>';
			echo '<td>';
			$links = array( 'הכרטיס' => get_permalink( $pro ) );
			foreach ( array( 'he' => 'האתר', 'en' => 'האתר באנגלית' ) as $l => $t ) { $sid = (int) get_post_meta( $pro, 'nl_site_' . $l, true ); if ( $sid ) { $links[ $t ] = get_permalink( $sid ); } }
			$links['/brokers/'] = add_query_arg( 'nlbx_preview', $pro, home_url( '/brokers/' ) );
			foreach ( array_keys( $proj ) as $slug ) {
				$p = get_page_by_path( $slug, OBJECT, 'nadlan_project' );
				if ( $p ) { $links[ (string) ( $cfg[ $slug ]['name'] ?? $slug ) ] = add_query_arg( 'nlbx_preview', $pro, get_permalink( $p ) ); }
			}
			foreach ( $links as $t => $u ) { echo '<a href="' . esc_url( $u ) . '" target="_blank" rel="noopener">' . esc_html( $t ) . '</a><br>'; }
			echo '</td><td><form id="' . $form . '" method="post" action="' . esc_url( admin_url( 'admin-post.php' ) ) . '">';
			wp_nonce_field( 'nadlan_bx_save' );
			echo '<input type="hidden" name="action" value="nadlan_bx_save"><input type="hidden" name="pro" value="' . (int) $pro . '"><button class="button button-primary">שמירה</button></form>';
			if ( $e && ! empty( $e['log'][0] ) ) { echo '<small>שונה ' . esc_html( wp_date( 'j.n.Y H:i', (int) $e['log'][0]['t'] ) ) . ': ' . esc_html( (string) $e['log'][0]['from'] . ' ← ' . (string) $e['log'][0]['to'] ) . '</small>'; }
			echo '</td></tr>';
		}
		echo '</tbody></table>';
		// a project's language boxes count only when the project itself is ticked
		echo '<script>document.querySelectorAll(".bx-proj").forEach(function(p){function f(){p.closest("fieldset").querySelectorAll("input[name^=projects]").forEach(function(x){x.disabled=!p.checked;});}p.addEventListener("change",f);f();});</script>';
		echo '</div>';
	}
}

add_filter( 'nadlan_config_healthcheck', function ( $out ) {
	$s = nadlan_bx_store();
	$by = array();
	foreach ( $s['brokers'] as $e ) { $by[ $e['level'] ] = ( $by[ $e['level'] ] ?? 0 ) + 1; }
	$out['broker_exposure'] = array( 'on' => nadlan_bx_on(), 'since' => (int) get_option( 'nadlan_bx_since', 0 ), 'entries' => count( $s['brokers'] ), 'by_level' => $by, 'strip' => '0' !== (string) get_option( 'nadlan_bx_strip', '1' ) );
	return $out;
} );
