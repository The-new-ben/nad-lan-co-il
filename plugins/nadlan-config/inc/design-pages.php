<?php
/**
 * nadlan-config - THE DESIGN PAGES (HAD-707, 11.11.2026; Ben: "neutral listing now ... build and upload the three pages").
 *
 *  - /profession/מעצב-פנים/ is a real WordPress page (child of the page "profession"). The taxonomy rule for
 *    /profession/<term>/ answers that address first, so the request is handed to the page when it is published.
 *    Nothing else changes: every other /profession/<term>/ keeps going to its term archive.
 *  - [nadlan_designers] prints the NEUTRAL list of interior-design studios from assets/designer/data/designers.json:
 *    business name, city, region, fields of work, one line from the business's own site and a link to that site.
 *    No ranking, no reviews, no photos, no phone numbers. Every card says the record was made from public information
 *    and that the business is not a partner, and carries an "update or remove" link (Ben chose this on 11.11.2026).
 *
 * Loaded from inc/designer.php only if present. Nothing runs at load time except hook registration.
 */
if ( ! defined( 'ABSPATH' ) ) { exit; }

if ( ! function_exists( 'nadlan_dpg_designers_slug' ) ) {

	function nadlan_dpg_designers_slug() { return 'מעצב-פנים'; }

	/** the published page at profession/מעצב-פנים, or 0 */
	function nadlan_dpg_designers_page_id() {
		static $id = null;
		if ( null !== $id ) { return $id; }
		$id = 0;
		$p  = get_page_by_path( 'profession/' . nadlan_dpg_designers_slug(), OBJECT, 'page' );
		if ( $p && 'publish' === $p->post_status ) { $id = (int) $p->ID; }
		return $id;
	}

	add_filter( 'request', function ( $qv ) {
		if ( ! is_array( $qv ) || empty( $qv['nadlan_profession'] ) || is_admin() ) { return $qv; }
		if ( nadlan_dpg_designers_slug() !== rawurldecode( (string) $qv['nadlan_profession'] ) ) { return $qv; }
		$id = nadlan_dpg_designers_page_id();
		return $id ? array( 'page_id' => $id ) : $qv;
	}, 20 );

	/** the public list, read once per request */
	function nadlan_dpg_designers_data() {
		static $d = null;
		if ( null !== $d ) { return $d; }
		$f = dirname( __DIR__ ) . '/assets/designer/data/designers.json';
		$j = is_readable( $f ) ? json_decode( (string) file_get_contents( $f ), true ) : null;
		$d = ( is_array( $j ) && ! empty( $j['records'] ) && is_array( $j['records'] ) ) ? $j : array( 'records' => array(), 'regions' => array(), 'specialities' => array(), 'checked_he' => '' );
		return $d;
	}

	function nadlan_dpg_designers_shortcode() {
		if ( ! empty( $GLOBALS['nadlan_dpg_list_done'] ) ) { return ''; } // one list per page
		$d    = nadlan_dpg_designers_data();
		$recs = $d['records'];
		if ( ! $recs ) { return ''; }
		$GLOBALS['nadlan_dpg_list_done'] = true;
		$spec    = is_array( $d['specialities'] ?? null ) ? $d['specialities'] : array();
		$regions = is_array( $d['regions'] ?? null ) ? $d['regions'] : array();
		$checked = (string) ( $d['checked_he'] ?? '' );
		$mail    = antispambot( 'info@nad-lan.co.il' );

		$by_region = array();
		$by_spec   = array();
		foreach ( $recs as $r ) {
			$rg = (string) ( $r['region'] ?? '' );
			$by_region[ $rg ] = ( $by_region[ $rg ] ?? 0 ) + 1;
			foreach ( (array) ( $r['specialities'] ?? array() ) as $s ) { $by_spec[ $s ] = ( $by_spec[ $s ] ?? 0 ) + 1; }
		}

		$o  = '<div class="nlds-dir" data-nlds-dir>';
		$o .= '<div class="nlds-dir__f" role="group" aria-label="סינון לפי אזור"><span class="nlds-dir__fl">אזור</span>';
		$o .= '<button type="button" class="nlds-chip" data-f="region" data-v="" aria-pressed="true">כל הארץ <b>' . count( $recs ) . '</b></button>';
		foreach ( $regions as $rg ) {
			if ( empty( $by_region[ $rg ] ) ) { continue; }
			$o .= '<button type="button" class="nlds-chip" data-f="region" data-v="' . esc_attr( $rg ) . '" aria-pressed="false">' . esc_html( $rg ) . ' <b>' . (int) $by_region[ $rg ] . '</b></button>';
		}
		$o .= '</div><div class="nlds-dir__f" role="group" aria-label="סינון לפי תחום"><span class="nlds-dir__fl">תחום</span>';
		$o .= '<button type="button" class="nlds-chip" data-f="spec" data-v="" aria-pressed="true">כל התחומים</button>';
		foreach ( $spec as $k => $label ) {
			if ( empty( $by_spec[ $k ] ) ) { continue; }
			$o .= '<button type="button" class="nlds-chip" data-f="spec" data-v="' . esc_attr( $k ) . '" aria-pressed="false">' . esc_html( $label ) . ' <b>' . (int) $by_spec[ $k ] . '</b></button>';
		}
		$o .= '</div><p class="nlds-dir__count" aria-live="polite">מוצגים <b data-nlds-shown>' . count( $recs ) . '</b> מתוך ' . count( $recs ) . ' · הסדר לפי א״ב, לא דירוג</p>';
		$o .= '<ol class="nlds-dir__list">';
		$n = 0; $ld = array();
		foreach ( $recs as $r ) {
			$name = trim( (string) ( $r['name'] ?? '' ) );
			$url  = esc_url( (string) ( $r['url'] ?? '' ), array( 'https', 'http' ) );
			if ( '' === $name || '' === $url ) { continue; }
			$n++;
			$tags = '';
			foreach ( (array) ( $r['specialities'] ?? array() ) as $s ) { if ( isset( $spec[ $s ] ) ) { $tags .= '<li>' . esc_html( $spec[ $s ] ) . '</li>'; } }
			$subject = rawurlencode( 'עדכון או הסרה מרשימת מעצבי הפנים: ' . $name );
			$o .= '<li class="nlds-rec" data-region="' . esc_attr( (string) ( $r['region'] ?? '' ) ) . '" data-spec="' . esc_attr( implode( ' ', (array) ( $r['specialities'] ?? array() ) ) ) . '">'
				. '<span class="nlds-rec__n" aria-hidden="true">' . sprintf( '%02d', $n ) . '</span>'
				. '<p class="nlds-rec__name">' . esc_html( $name ) . '</p>'
				. '<p class="nlds-rec__place">' . esc_html( (string) ( $r['city'] ?? '' ) ) . ' · ' . esc_html( (string) ( $r['region'] ?? '' ) ) . '</p>'
				. ( $tags ? '<ul class="nlds-rec__tags">' . $tags . '</ul>' : '' )
				. ( ! empty( $r['line'] ) ? '<p class="nlds-rec__line">' . esc_html( (string) $r['line'] ) . '</p>' : '' )
				. '<p class="nlds-rec__go"><a href="' . $url . '" target="_blank" rel="noopener">לאתר של העסק<span aria-hidden="true"> ↖</span></a></p>'
				. '<p class="nlds-rec__foot">הפרופיל נוצר ממידע ציבורי. העסק אינו שותף של האתר.' . ( $checked ? ' נבדק: ' . esc_html( $checked ) . '.' : '' )
				. ' <a href="mailto:' . esc_attr( $mail ) . '?subject=' . $subject . '">לעסק הזה? עדכון או הסרה</a></p>'
				. '</li>';
			$ld[] = array( '@type' => 'ListItem', 'position' => $n, 'name' => $name, 'url' => (string) $r['url'] );
		}
		$o .= '</ol><p class="nlds-dir__none" hidden>אין ברשימה עסק שמתאים לשני הסינונים יחד. נסו אזור אחר או תחום אחר.</p></div>';
		$o .= '<script>(function(){var d=document.querySelector("[data-nlds-dir]");if(!d)return;var st={region:"",spec:""};'
			. 'var recs=[].slice.call(d.querySelectorAll(".nlds-rec")),shown=d.querySelector("[data-nlds-shown]"),none=d.querySelector(".nlds-dir__none");'
			. 'd.addEventListener("click",function(e){var b=e.target.closest(".nlds-chip");if(!b)return;st[b.dataset.f]=b.dataset.v;'
			. '[].forEach.call(d.querySelectorAll(\'.nlds-chip[data-f="\'+b.dataset.f+\'"]\'),function(x){x.setAttribute("aria-pressed",String(x===b));});'
			. 'var n=0;recs.forEach(function(r){var ok=(!st.region||r.dataset.region===st.region)&&(!st.spec||(" "+r.dataset.spec+" ").indexOf(" "+st.spec+" ")>-1);r.hidden=!ok;if(ok)n++;});'
			. 'shown.textContent=n;none.hidden=n>0;});})();</script>';
		if ( $ld ) {
			$o .= '<script type="application/ld+json">' . wp_json_encode( array( '@context' => 'https://schema.org', '@type' => 'ItemList', 'name' => 'סטודיואים לעיצוב פנים בישראל: רשימה ניטרלית', 'numberOfItems' => count( $ld ), 'itemListOrder' => 'https://schema.org/ItemListUnordered', 'itemListElement' => $ld ), JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES | JSON_HEX_TAG ) . '</script>';
		}
		return $o;
	}

	add_action( 'init', function () { add_shortcode( 'nadlan_designers', 'nadlan_dpg_designers_shortcode' ); } );
}
