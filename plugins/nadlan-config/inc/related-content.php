<?php
/**
 * nadlan-config - RELATED CONTENT FLOATS + PRO DOSSIER (2026-07-11).
 *
 * The anti-thin-content layer (owner order): float genuinely related site
 * content - glossary terms, guides/news, calculators - into the two thinnest
 * surfaces (listings, professional profiles), the way pro-cards.php floats
 * sponsored professionals into articles. One restrained band, token-matched,
 * cached, collapses when there is nothing honest to show.
 *
 * Plus the real thin-fix for profiles: an AI-written DOSSIER (domain explainer
 * for the profession - what they do in a deal, how to choose one, FAQ). The
 * writer is an admin-gated REST batch (runs ONLY on owner trigger, uses the
 * ai-brain judge/refine pipeline); the renderer ships now and shows the meta
 * when present. Honesty law: general domain content only - the prompt forbids
 * inventing facts about the specific person.
 *
 * Kill switch: option nadlan_relcontent_enabled ('1' default).
 */

if ( ! defined( 'ABSPATH' ) ) { exit; }

if ( ! function_exists( 'nadlan_relc_on' ) ) {
	function nadlan_relc_on() { return get_option( 'nadlan_relcontent_enabled', '1' ) === '1'; }
}

if ( ! function_exists( 'nadlan_relc_terms' ) ) {
	/** Glossary terms matched to a post by title/city tokens (12h cache). */
	function nadlan_relc_terms( $post_id, $limit = 3 ) {
		$key = 'nadlan_relc_t_' . $post_id;
		$hit = get_transient( $key );
		if ( is_array( $hit ) ) { return $hit; }
		$tokens = array();
		foreach ( preg_split( '/[\s,\-\x{05be}]+/u', get_the_title( $post_id ) . ' ' . (string) get_post_meta( $post_id, 'city', true ) . ' ' . (string) get_post_meta( $post_id, 'profession', true ) ) as $tk ) {
			if ( mb_strlen( $tk ) >= 3 && ! is_numeric( $tk ) ) { $tokens[] = $tk; }
			if ( count( $tokens ) >= 4 ) { break; }
		}
		$found = array();
		// domain seed by CPT so the band is useful even when tokens miss
		$seed = get_post_type( $post_id ) === 'nadlan_professional'
			? array( 'ליווי משפטי', 'שמאות', 'משכנתא', 'בדק בית', 'תיווך' )
			: array( 'מס רכישה', 'טופס 4', 'הון עצמי', 'רישום בטאבו', 'הערת אזהרה' );
		foreach ( array_merge( $tokens, $seed ) as $tk ) {
			if ( count( $found ) >= $limit ) { break; }
			$q = get_posts( array( 'post_type' => 'nadlan_term', 'posts_per_page' => 1, 's' => $tk, 'fields' => 'ids', 'no_found_rows' => true ) );
			foreach ( $q as $tid ) { if ( ! isset( $found[ $tid ] ) ) { $found[ $tid ] = true; } }
		}
		$out = array();
		foreach ( array_keys( $found ) as $tid ) {
			$out[] = array( 'title' => get_the_title( $tid ), 'url' => get_permalink( $tid ) );
		}
		set_transient( $key, $out, 12 * HOUR_IN_SECONDS );
		return $out;
	}
}

if ( ! function_exists( 'nadlan_relc_band' ) ) {
	function nadlan_relc_band( $post_id ) {
		$type  = get_post_type( $post_id );
		$cards = array();
		foreach ( nadlan_relc_terms( $post_id ) as $t ) {
			$cards[] = array( 'k' => nadlan_i18n( 'rc_term' ), 'title' => $t['title'], 'url' => $t['url'] );
		}
		if ( 'nadlan_property' === $type ) {
			$cards[] = array( 'k' => nadlan_i18n( 'rc_tool' ), 'title' => nadlan_i18n( 'rc_calc_mortgage' ), 'url' => home_url( '/mortgage-calculator/' ) );
			$cards[] = array( 'k' => nadlan_i18n( 'rc_tool' ), 'title' => nadlan_i18n( 'rc_calc_ptax' ), 'url' => home_url( '/purchase-tax-calculator/' ) );
			$cards[] = array( 'k' => nadlan_i18n( 'rc_guide' ), 'title' => nadlan_i18n( 'rc_guide_buy' ), 'url' => home_url( '/buying-apartment/' ) );
		} else {
			// profiles already carry their tools block - float fresh NEWS instead
			$news = get_posts( array( 'posts_per_page' => 3, 'category_name' => 'nadlan-news', 'no_found_rows' => true ) );
			foreach ( $news as $n ) {
				$cards[] = array( 'k' => nadlan_i18n( 'rc_news' ), 'title' => get_the_title( $n ), 'url' => get_permalink( $n ) );
			}
		}
		$cards = array_slice( array_filter( $cards, function ( $c ) { return '' !== trim( (string) $c['title'] ); } ), 0, 6 );
		if ( count( $cards ) < 2 ) { return ''; }
		$html = '<section class="nlrc"><header><span class="nlrc-k">' . esc_html( nadlan_i18n( 'rc_kicker' ) ) . '</span><h2>' . esc_html( nadlan_i18n( 'rc_title' ) ) . '</h2></header><div class="nlrc-grid">';
		foreach ( $cards as $c ) {
			$html .= '<a class="nlrc-card" href="' . esc_url( $c['url'] ) . '"><i>' . esc_html( $c['k'] ) . '</i><b>' . esc_html( $c['title'] ) . '</b></a>';
		}
		$html .= '</div></section>';
		$html .= '<style>.nlrc{margin:34px 0 8px;padding:22px 0 4px;border-top:1px solid #E2DCD0}.nlrc header{margin-bottom:14px}.nlrc-k{display:block;color:#9C7A3C;font:600 12px/1 Heebo,sans-serif;letter-spacing:.08em;text-transform:uppercase}.nlrc h2{font-family:"Frank Ruhl Libre",Georgia,serif;color:#1B1A17;font-size:1.4rem;margin:6px 0 0}.nlrc-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:10px}.nlrc-card{display:flex;flex-direction:column;gap:6px;background:#FFFFFF;border:1px solid #E2DCD0;border-radius:12px;padding:14px 16px;text-decoration:none;transition:border-color .2s}.nlrc-card:hover{border-color:#9C7A3C}.nlrc-card i{font-style:normal;font:600 10.5px/1 Heebo,sans-serif;color:#9C7A3C;letter-spacing:.06em;text-transform:uppercase}.nlrc-card b{font:600 14.5px/1.4 Heebo,sans-serif;color:#1B1A17}</style>';
		return $html;
	}
}

add_filter( 'the_content', function ( $content ) {
	if ( ! nadlan_relc_on() || ! is_singular( array( 'nadlan_property', 'nadlan_professional' ) ) || ! in_the_loop() || ! is_main_query() ) { return $content; }
	return $content . nadlan_relc_band( get_the_ID() );
}, 21 );

/* ---------------- the professional dossier ---------------- */

add_filter( 'the_content', function ( $content ) {
	if ( ! is_singular( 'nadlan_professional' ) || ! in_the_loop() || ! is_main_query() ) { return $content; }
	$d = trim( (string) get_post_meta( get_the_ID(), 'prof_dossier', true ) );
	if ( '' === $d ) { return $content; }
	return $content . '<section class="nlrc nlrc--dossier"><header><span class="nlrc-k">' . esc_html( nadlan_i18n( 'rc_dossier_k' ) ) . '</span><h2>' . esc_html( nadlan_i18n( 'rc_dossier_t' ) ) . '</h2></header><div class="nlrc-prose">' . wp_kses_post( $d ) . '</div><style>.nlrc-prose{font:400 15.5px/1.75 Heebo,sans-serif;color:#3A352C;max-width:74ch}.nlrc-prose h3{font-family:"Frank Ruhl Libre",Georgia,serif;color:#1B1A17;margin:20px 0 8px}</style></section>';
}, 8 );

add_action( 'rest_api_init', function () {
	register_rest_route( 'nadlan/v1', '/prof-dossier-generate', array(
		'methods'             => 'POST',
		'permission_callback' => function () { return current_user_can( 'manage_options' ); },
		'callback'            => function ( $req ) {
			if ( ! function_exists( 'nadlan_ai_chat' ) ) { return new WP_Error( 'no_ai', 'ai provider absent', array( 'status' => 500 ) ); }
			$n   = max( 1, min( 10, (int) $req->get_param( 'n' ) ?: 3 ) );
			$ids = get_posts( array( 'post_type' => 'nadlan_professional', 'posts_per_page' => $n, 'fields' => 'ids',
				'meta_query' => array( array( 'key' => 'prof_dossier', 'compare' => 'NOT EXISTS' ) ) ) );
			$done = array();
			foreach ( $ids as $pid ) {
				$prof = (string) get_post_meta( $pid, 'profession', true );
				$city = (string) get_post_meta( $pid, 'city', true );
				$system = 'אתה עורך תוכן מקצועי של פורטל נדלן ישראלי. כתוב פרק ידע כללי על תחום המקצוע, בעברית מקצועית וברורה. ' .
					'אסור להמציא עובדות על בעל המקצוע הספציפי - כתוב רק על התחום עצמו. אסור מקף ארוך - רק מקף רגיל.' .
					( function_exists( 'nadlan_brain_house_rules' ) ? nadlan_brain_house_rules() : '' );
				$user = 'כתוב 350-550 מילים בפורמט HTML פשוט (<h3> ו-<p> בלבד) על תחום: ' . ( $prof ?: 'איש מקצוע בנדלן' ) .
					( $city ? ' (הקשר עירוני: ' . $city . ')' : '' ) .
					'. מבנה: מה בעל המקצוע הזה עושה בעסקת נדלן; מתי חובה או מומלץ לערב אותו; איך בוחרים נכון (3-4 קריטריונים); שאלה נפוצה אחת עם תשובה קצרה.';
				$out = nadlan_ai_chat( $system, array( array( 'role' => 'user', 'content' => $user ) ), 1600 );
				if ( is_wp_error( $out ) ) { continue; }
				$txt = is_array( $out ) ? (string) ( $out['text'] ?? $out['content'] ?? '' ) : (string) $out;
				if ( function_exists( 'nadlan_brain_refine' ) ) {
					$r = nadlan_brain_refine( $system, $txt, 'דיוק מקצועי, אפס המצאות על האדם הספציפי, עברית תקינה, מבנה לפי ההנחיה, ללא מקף ארוך', 1600 );
					$txt = $r['text'];
				}
				$txt = trim( $txt );
				if ( mb_strlen( wp_strip_all_tags( $txt ) ) < 200 ) { continue; }
				update_post_meta( $pid, 'prof_dossier', wp_kses_post( $txt ) );
				$done[] = $pid;
			}
			return array( 'generated' => $done, 'remaining_without' => max( 0, count( get_posts( array( 'post_type' => 'nadlan_professional', 'posts_per_page' => -1, 'fields' => 'ids', 'meta_query' => array( array( 'key' => 'prof_dossier', 'compare' => 'NOT EXISTS' ) ) ) ) ) ) );
		},
	) );
} );

/* healthcheck visibility */
add_filter( 'nadlan_config_healthcheck', function ( $out ) {
	$out['related_content'] = array( 'enabled' => nadlan_relc_on() );
	return $out;
} );
