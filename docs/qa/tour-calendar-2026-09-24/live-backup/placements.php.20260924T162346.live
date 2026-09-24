<?php
/**
 * Broker placements: a broker's ad card on chosen pages, as a managed mechanism (owner order 24.9.2026:
 * "Meital's card is a good idea, do it, but with a mechanism. Not just a card: something I can control after").
 *
 * A placement (NadLan Ops > "שיבוץ מתווכים") says WHO appears (a professional's card), WHERE (page paths, a
 * trailing * matches a whole section), WHEN (start and end dates) and HOW (after which section, the headline).
 * The card is always labelled as the broker's advertisement with the name, "מתווך"/"מתווכת" and the licence
 * number (ethics regulation 19), because the site itself is a publisher and never the broker (Brokers Law 2(c)).
 * Views and clicks go to the private insights table (inc/insights.php): place_view, place_click.
 *
 * Nothing shows until a placement is published AND active. An admin can preview a draft on its page with
 * ?nlpl_preview=<placement id>.
 *
 * 1.72.246: the card is the design system's BrokerFeatureCard (the same one as on /brokers/), under a "פרסומת" label,
 * with the broker's name as a paragraph so the article's outline stays the article's. The position can be a number of
 * sections or a word from a section heading ("מחיר": right after the prices section), and each page line in the
 * paths can carry its own position ("/property-value/ 4").
 */
if ( ! defined( 'ABSPATH' ) ) { exit; }

add_action( 'init', function () {
	register_post_type( 'nadlan_placement', array(
		'labels'          => array( 'name' => 'שיבוץ מתווכים', 'singular_name' => 'שיבוץ', 'add_new_item' => 'שיבוץ חדש', 'edit_item' => 'עריכת שיבוץ' ),
		'public'          => false,
		'show_ui'         => true,
		'show_in_menu'    => 'nadlan-ops',
		'show_in_rest'    => false,
		'supports'        => array( 'title' ),
		'capability_type' => 'page',
		'map_meta_cap'    => true,
	) );
}, 20 );

if ( ! function_exists( 'nadlan_pl_fields' ) ) {
	function nadlan_pl_fields() {
		return array(
			'pl_pro'      => 'מזהה הכרטיס של המתווך',
			'pl_paths'    => 'עמודים: נתיב בכל שורה, למשל /property-value/ או /north-tel-aviv/* (כוכבית = כל העמודים מתחת). אחרי הנתיב אפשר לכתוב מיקום לעמוד הזה, למשל /property-value/ 4',
			'pl_after_h2' => 'מיקום: אחרי כמה פרקים (מספר), או מילה מכותרת הפרק שאחריו הכרטיס יופיע (למשל מחיר); 0 = בסוף העמוד',
			'pl_headline' => 'כותרת הכרטיס (לא חובה)',
			'pl_ask'      => 'הטקסט המוכן בוואטסאפ (לא חובה)',
			'pl_start'    => 'מתחיל בתאריך (YYYY-MM-DD, לא חובה)',
			'pl_end'      => 'נגמר בתאריך (YYYY-MM-DD, לא חובה)',
			'pl_active'   => 'פעיל (1 או 0)',
		);
	}
}

add_action( 'add_meta_boxes', function () {
	add_meta_box( 'nadlan_pl_box', 'הגדרות השיבוץ', function ( $post ) {
		wp_nonce_field( 'nadlan_pl_save', 'nadlan_pl_nonce' );
		echo '<table class="form-table" dir="rtl">';
		foreach ( nadlan_pl_fields() as $k => $label ) {
			$v = (string) get_post_meta( $post->ID, $k, true );
			echo '<tr><th><label for="' . esc_attr( $k ) . '">' . esc_html( $label ) . '</label></th><td>';
			if ( 'pl_paths' === $k ) {
				echo '<textarea id="pl_paths" name="pl_paths" rows="5" style="width:100%;direction:ltr">' . esc_textarea( $v ) . '</textarea>';
			} else {
				echo '<input type="text" id="' . esc_attr( $k ) . '" name="' . esc_attr( $k ) . '" value="' . esc_attr( $v ) . '" style="width:100%">';
			}
			echo '</td></tr>';
		}
		echo '</table><p>תצוגה מקדימה לפני פרסום: לפתוח את העמוד עם <code>?nlpl_preview=' . (int) $post->ID . '</code> (רק למנהל).</p>';
	}, 'nadlan_placement', 'normal', 'high' );
} );

add_action( 'save_post_nadlan_placement', function ( $post_id ) {
	if ( ! isset( $_POST['nadlan_pl_nonce'] ) || ! wp_verify_nonce( (string) $_POST['nadlan_pl_nonce'], 'nadlan_pl_save' ) ) { return; }
	if ( ! current_user_can( 'edit_post', $post_id ) || wp_is_post_revision( $post_id ) ) { return; }
	foreach ( array_keys( nadlan_pl_fields() ) as $k ) {
		if ( ! isset( $_POST[ $k ] ) ) { continue; }
		$v = wp_unslash( (string) $_POST[ $k ] );
		$v = 'pl_paths' === $k ? sanitize_textarea_field( $v ) : sanitize_text_field( $v );
		update_post_meta( $post_id, $k, $v );
	}
} );

if ( ! function_exists( 'nadlan_pl_match' ) ) {
	/** false when no line matches this page; else the position written after the matching path ('' when none). */
	function nadlan_pl_match( $paths, $here ) {
		$here = '/' . trim( (string) $here, '/' ) . '/';
		foreach ( preg_split( '/\R/', (string) $paths ) as $line ) {
			$parts = preg_split( '/\s+/u', trim( $line ), 2 );
			$p     = rawurldecode( (string) $parts[0] );
			$pos   = isset( $parts[1] ) ? trim( $parts[1] ) : '';
			if ( '' === $p ) { continue; }
			if ( '*' === substr( $p, -1 ) ) {
				// "/north-tel-aviv/*" is that page and every page under it, never "/north-tel-aviv-new-projects/"
				$pre = '/' . trim( substr( $p, 0, -1 ), '/' );
				$h   = rtrim( $here, '/' );
				if ( $h === $pre || 0 === strpos( $h, $pre . '/' ) ) { return $pos; }
			} elseif ( '/' . trim( $p, '/' ) . '/' === $here ) {
				return $pos;
			}
		}
		return false;
	}
}

if ( ! function_exists( 'nadlan_pl_path_matches' ) ) {
	function nadlan_pl_path_matches( $paths, $here ) {
		return false !== nadlan_pl_match( $paths, $here );
	}
}

if ( ! function_exists( 'nadlan_pl_for_request' ) ) {
	/** The placement for this page: an admin preview first, else the first active one whose paths match and whose dates cover today. */
	function nadlan_pl_for_request( $want = 'id' ) {
		static $memo = null;
		if ( null === $memo ) {
			$memo = array( 'id' => 0, 'pos' => '' );
			if ( ! is_admin() && is_singular() ) {
				$here = rawurldecode( (string) wp_parse_url( (string) ( $_SERVER['REQUEST_URI'] ?? '' ), PHP_URL_PATH ) );
				$pick = function ( $pid, $line_pos ) {
					$pos = false !== $line_pos && '' !== $line_pos ? $line_pos : (string) get_post_meta( $pid, 'pl_after_h2', true );
					return array( 'id' => (int) $pid, 'pos' => $pos );
				};
				if ( isset( $_GET['nlpl_preview'] ) && current_user_can( 'edit_pages' ) && 'nadlan_placement' === get_post_type( (int) $_GET['nlpl_preview'] ) ) {
					$pid  = (int) $_GET['nlpl_preview'];
					$memo = $pick( $pid, nadlan_pl_match( get_post_meta( $pid, 'pl_paths', true ), $here ) );
				} else {
					$ids = get_posts( array( 'post_type' => 'nadlan_placement', 'post_status' => 'publish', 'numberposts' => 50, 'fields' => 'ids',
						'orderby' => 'date', 'order' => 'ASC', 'meta_query' => array( array( 'key' => 'pl_active', 'value' => '1' ) ) ) );
					$today = current_time( 'Y-m-d' );
					foreach ( $ids as $pid ) {
						$s = (string) get_post_meta( $pid, 'pl_start', true );
						$e = (string) get_post_meta( $pid, 'pl_end', true );
						if ( ( '' !== $s && $today < $s ) || ( '' !== $e && $today > $e ) ) { continue; }
						$m = nadlan_pl_match( get_post_meta( $pid, 'pl_paths', true ), $here );
						if ( false !== $m ) { $memo = $pick( $pid, $m ); break; }
					}
				}
			}
		}
		return 'pos' === $want ? $memo['pos'] : $memo['id'];
	}
}

if ( ! function_exists( 'nadlan_pl_card' ) ) {
	function nadlan_pl_card( $pl ) {
		$pro = (int) get_post_meta( $pl, 'pl_pro', true );
		if ( $pro <= 0 || 'nadlan_professional' !== get_post_type( $pro ) || 'publish' !== get_post_status( $pro ) || ! function_exists( 'nadlan_bl_feature_card' ) ) { return ''; }
		$name  = function_exists( 'nadlan_prof_person_name' ) ? (string) nadlan_prof_person_name( $pro ) : get_the_title( $pro );
		$first = (string) strtok( $name, ' ' );
		$ask   = trim( (string) get_post_meta( $pl, 'pl_ask', true ) );
		$ask   = '' !== $ask ? $ask : 'שלום ' . $first . ', הגעתי מאתר נדלן ואשמח להתייעץ על דירה';
		$slot  = 'pl-' . (int) $pl;
		$inner = nadlan_bl_feature_card( $pro, array(
			'name_tag'   => 'p',
			'wa_label'   => 'התייעצות בוואטסאפ',
			'wa_text'    => $ask,
			'site_label' => 'לנכסים של ' . $first,
			'line'       => trim( (string) get_post_meta( $pl, 'pl_headline', true ) ),
			'link_attrs' => ' data-nl-ev="place_click" data-nl-slot="' . esc_attr( $slot ) . '"',
		) );
		if ( '' === trim( $inner ) ) { return ''; }
		// the label is the law: the site is a publisher, and this is the broker's advertisement (name and licence are in the card)
		return '<aside class="nlds nlpl" dir="rtl" lang="he" data-pl="' . (int) $pl . '" data-pro="' . (int) $pro . '" data-post="' . (int) get_queried_object_id() . '" aria-label="' . esc_attr( 'פרסומת: ' . $name ) . '">'
			. '<p class="nlds-kicker nlpl-tag">פרסומת</p>' . $inner . '</aside>';
	}
}

if ( ! function_exists( 'nadlan_pl_insert' ) ) {
	/**
	 * Puts the card where the placement says: after N sections (the end when the page has fewer), or after the first
	 * section whose heading has the word. A page without such a section gets no card: an advertisement dropped
	 * under the sources list is worth less than none.
	 */
	function nadlan_pl_insert( $content, $card, $pos ) {
		$pos = trim( (string) $pos );
		if ( '' === $pos || '0' === $pos ) { return $content . $card; }
		if ( preg_match( '/^\d+$/', $pos ) ) {
			// before the (n+1)th section heading, so the card closes the n-th section
			$n   = (int) $pos;
			$at  = false;
			$off = 0;
			for ( $i = 0; $i <= $n; $i++ ) {
				$at = strpos( $content, '<h2', $off );
				if ( false === $at ) { break; }
				$off = $at + 3;
			}
			return false !== $at && $at > 0 ? substr( $content, 0, $at ) . $card . substr( $content, $at ) : $content . $card;
		}
		if ( preg_match_all( '/<h2\b[^>]*>(.*?)<\/h2>/is', $content, $m, PREG_OFFSET_CAPTURE ) ) {
			foreach ( $m[1] as $k => $h ) {
				$text = html_entity_decode( wp_strip_all_tags( $h[0] ), ENT_QUOTES, 'UTF-8' );
				if ( false === mb_stripos( $text, $pos ) ) { continue; }
				if ( isset( $m[0][ $k + 1 ] ) ) {
					$at = $m[0][ $k + 1 ][1];
					return substr( $content, 0, $at ) . $card . substr( $content, $at );
				}
				return $content . $card; // the matching section is the last one
			}
		}
		return $content;
	}
}

add_filter( 'the_content', function ( $content ) {
	if ( ! in_the_loop() || ! is_main_query() ) { return $content; }
	$pl = nadlan_pl_for_request();
	if ( ! $pl ) { return $content; }
	$card = nadlan_pl_card( $pl );
	if ( '' === $card ) { return $content; }
	return nadlan_pl_insert( $content, $card, nadlan_pl_for_request( 'pos' ) );
}, 40 );

add_action( 'wp_footer', function () {
	if ( ! nadlan_pl_for_request() ) { return; }
	$url = esc_url_raw( rest_url( 'nadlan/v1/ev' ) );
	echo "\n<style id=\"nadlan-placement-css\">:root body .nlds.nlpl{display:grid!important;gap:var(--nlds-space-10)!important;margin-block:32px!important;clear:both}:root body .nlds.nlpl .nlpl-tag{color:var(--nlds-sa-ink2)!important;font-weight:600!important}</style>\n";
	echo "<script id=\"nadlan-placement-ev\">(function(){if(!navigator.sendBeacon)return;var u=" . wp_json_encode( $url ) . ";function s(c,e){try{navigator.sendBeacon(u,new Blob([JSON.stringify({e:e,pro:+c.dataset.pro,post:+c.dataset.post,slot:'pl-'+c.dataset.pl})],{type:'application/json'}))}catch(_){}}document.querySelectorAll('.nlpl').forEach(function(c){if('IntersectionObserver' in window){var o=new IntersectionObserver(function(x){if(x[0].isIntersecting){s(c,'place_view');o.disconnect()}},{threshold:.5});o.observe(c)}else{s(c,'place_view')}c.addEventListener('click',function(v){if(v.target.closest('[data-nl-ev]'))s(c,'place_click')})})})();</script>\n";
}, 41 );
