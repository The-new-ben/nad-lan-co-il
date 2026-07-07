<?php
/**
 * nadlan-config - THE AI BRAIN (2026-07-07, owner order: "make the AI brain
 * much, much smarter, prompted inside to get the best outputs").
 *
 * A thin, research-backed pipeline layer on top of nadlan_ai_chat(). Each
 * primitive implements a published technique with measured gains:
 *
 *  1. nadlan_brain_house_rules()  - a shared "constitution" appended to every
 *     system prompt: grounding-only answers (RAG discipline - Lewis et al.
 *     2020, arXiv:2005.11401), honesty laws, Hebrew register, dash law.
 *  2. nadlan_brain_judge()        - LLM-as-a-Judge rubric scoring (Zheng et
 *     al. 2023, MT-Bench, arXiv:2306.05685): score a draft 1-10 against an
 *     explicit rubric, return issues.
 *  3. nadlan_brain_refine()       - Self-Refine (Madaan et al. 2023,
 *     arXiv:2303.17651): feed the judge's critique back for one revision
 *     pass (~20% avg preference gain across tasks in the paper).
 *  4. nadlan_brain_vote()         - Self-Consistency (Wang et al. 2022,
 *     arXiv:2203.11171): sample N answers, majority-vote the label. Used
 *     SELECTIVELY (only when confidence is low) to stay cost-aware.
 *
 * Everything is gated: option nadlan_brain_enabled (default on) and the
 * provider's own cost caps still apply to every extra call. Failures fall
 * back to the unrefined draft - the brain can only improve, never block.
 */

if ( ! defined( 'ABSPATH' ) ) { exit; }

if ( ! function_exists( 'nadlan_brain_on' ) ) {
	function nadlan_brain_on() {
		return function_exists( 'nadlan_ai_chat' ) && get_option( 'nadlan_brain_enabled', '1' ) === '1';
	}
}

if ( ! function_exists( 'nadlan_brain_house_rules' ) ) {
	function nadlan_brain_house_rules() {
		return "\n\nחוקי יסוד (עדיפות עליונה): " .
			'ענה אך ורק מתוך המידע שסופק לך בהקשר; נתון שאינו מופיע בו - אמור שאינו ידוע, לעולם אל תמציא. ' .
			'אל תבטיח הבטחות בשם יזם או בעל מקצוע. מחירים ולוחות זמנים הם באחריות היזם בלבד. ' .
			'אסור מקף ארוך מכל סוג - רק מקף רגיל. ' .
			'כתיבה עניינית ומקצועית, בלי סופרלטיבים שיווקיים ריקים. ' .
			'אם המשתמש כותב באנגלית - ענה באנגלית באותה משמעת בדיוק.';
	}
}

if ( ! function_exists( 'nadlan_brain_judge' ) ) {
	/**
	 * LLM-as-a-Judge (Zheng et al. 2023): score a draft against a rubric.
	 * Returns array( 'score' => float 1-10, 'issues' => string ) or WP_Error.
	 */
	function nadlan_brain_judge( $draft, $rubric, $max_tokens = 350 ) {
		if ( ! nadlan_brain_on() ) { return new WP_Error( 'brain_off', 'brain disabled' ); }
		$system = 'אתה שופט איכות קפדני של תוכן מקצועי. קיבלת טיוטה ומחוון (rubric). ' .
			'דרג את הטיוטה מ-1 עד 10 מול המחוון בלבד, ופרט עד 4 ליקויים קונקרטיים הניתנים לתיקון. ' .
			'החזר JSON בלבד: {"score": <number>, "issues": "<string>"}';
		$user = "המחוון:\n" . $rubric . "\n\nהטיוטה:\n" . $draft;
		$out  = nadlan_ai_chat( $system, array( array( 'role' => 'user', 'content' => $user ) ), $max_tokens );
		if ( is_wp_error( $out ) ) { return $out; }
		$txt = is_array( $out ) ? (string) ( $out['text'] ?? $out['content'] ?? '' ) : (string) $out;
		if ( preg_match( '/\{.*\}/s', $txt, $m ) ) {
			$j = json_decode( $m[0], true );
			if ( is_array( $j ) && isset( $j['score'] ) ) {
				return array( 'score' => max( 1, min( 10, (float) $j['score'] ) ), 'issues' => (string) ( $j['issues'] ?? '' ) );
			}
		}
		return new WP_Error( 'brain_judge_parse', 'unparseable judge output' );
	}
}

if ( ! function_exists( 'nadlan_brain_refine' ) ) {
	/**
	 * Self-Refine (Madaan et al. 2023): judge, then revise once when the
	 * score is under the bar. Returns the better text (never worse: falls
	 * back to the draft on any failure).
	 * Returns array( 'text' => string, 'score' => float|null, 'refined' => bool ).
	 */
	function nadlan_brain_refine( $system, $draft, $rubric, $max_tokens = 4000, $bar = 8.0 ) {
		$res = array( 'text' => $draft, 'score' => null, 'refined' => false );
		if ( ! nadlan_brain_on() || '' === trim( (string) $draft ) ) { return $res; }
		$judge = nadlan_brain_judge( $draft, $rubric );
		if ( is_wp_error( $judge ) ) { return $res; }
		$res['score'] = $judge['score'];
		if ( $judge['score'] >= $bar || '' === trim( $judge['issues'] ) ) { return $res; }
		$user = "הטיוטה שלך קיבלה ביקורת מעורך מומחה. תקן את הליקויים הבאים בלבד, בלי לשנות את מה שכבר טוב, ושמור על כל כללי המערכת:\n" .
			$judge['issues'] . "\n\nהטיוטה:\n" . $draft . "\n\nהחזר את הגרסה המתוקנת המלאה בלבד.";
		$out = nadlan_ai_chat( (string) $system . nadlan_brain_house_rules(), array( array( 'role' => 'user', 'content' => $user ) ), $max_tokens );
		if ( is_wp_error( $out ) ) { return $res; }
		$txt = is_array( $out ) ? (string) ( $out['text'] ?? $out['content'] ?? '' ) : (string) $out;
		// accept only a plausible revision (guards against truncation regressions)
		if ( function_exists( 'mb_strlen' ) ? mb_strlen( $txt ) > mb_strlen( $draft ) * 0.7 : strlen( $txt ) > strlen( $draft ) * 0.7 ) {
			$res['text']    = $txt;
			$res['refined'] = true;
		}
		return $res;
	}
}

if ( ! function_exists( 'nadlan_brain_vote' ) ) {
	/**
	 * Selective Self-Consistency (Wang et al. 2022): sample the same
	 * classification N times and majority-vote a specific field. Use only
	 * when a single pass reports low confidence - accuracy where it matters,
	 * cost discipline everywhere else.
	 * $extract: callable(string raw) => string|null label.
	 * Returns array( 'label' => string|null, 'agreement' => float, 'n' => int ).
	 */
	function nadlan_brain_vote( $system, $messages, $extract, $n = 3, $max_tokens = 700 ) {
		$labels = array();
		if ( ! nadlan_brain_on() ) { return array( 'label' => null, 'agreement' => 0, 'n' => 0 ); }
		$n = max( 2, min( 5, (int) $n ) );
		for ( $i = 0; $i < $n; $i++ ) {
			$out = nadlan_ai_chat( $system, $messages, $max_tokens );
			if ( is_wp_error( $out ) ) { break; }
			$txt = is_array( $out ) ? (string) ( $out['text'] ?? $out['content'] ?? '' ) : (string) $out;
			$l   = call_user_func( $extract, $txt );
			if ( null !== $l && '' !== $l ) { $labels[] = (string) $l; }
		}
		if ( ! $labels ) { return array( 'label' => null, 'agreement' => 0, 'n' => 0 ); }
		$counts = array_count_values( $labels );
		arsort( $counts );
		$top = array_key_first( $counts );
		return array( 'label' => $top, 'agreement' => $counts[ $top ] / count( $labels ), 'n' => count( $labels ) );
	}
}

/* healthcheck visibility */
add_filter( 'nadlan_config_healthcheck', function ( $out ) {
	$out['ai_brain'] = array(
		'enabled'    => nadlan_brain_on(),
		'primitives' => array( 'house_rules', 'judge (Zheng 2023)', 'refine (Madaan 2023)', 'vote (Wang 2022)' ),
	);
	return $out;
} );
