<?php
/**
 * Feature bar: make what we already built findable.
 *
 * The expensive problem on project pages was never missing features, it was
 * buried ones. The window view is a tab labelled with a compass direction, the
 * studio lives inside a unit panel you must first open, and the cinematic
 * designer had no link anywhere on the site at all. Work nobody can find is
 * work thrown away.
 *
 * The bar is IN FLOW, never floating or sticky - a deliberate owner call.
 *
 * Priority 11 is chosen, not default. The content pipeline on a project page
 * is crowded and every one of these prepends: breadcrumbs+directory (5),
 * pjx_top (7), showroom engine + facility chips (8), price band (9),
 * milestones (12), pjx_bottom (19), cards-render + legal notice (20), reviews
 * (22), profile-extras (23), glossary autolink (24), scheduler (28), tiers
 * (30). 11 lands after the showroom and chips and before the milestones band,
 * which puts the bar high on the page where it is seen. Anything at 24 or
 * later would have its links rewritten by the glossary autolinker.
 *
 * Nothing is ever hidden for being unavailable: a capability this project does
 * not have yet renders dimmed and labelled, so the gap is visible instead of
 * silently absent. Features are only ever added, never levelled down.
 *
 * @package nadlan-config
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

if ( ! function_exists( 'nadlan_fbar_items' ) ) {
	/**
	 * What this project can actually do, measured from its own data.
	 *
	 * The gating mirrors the engine exactly so the bar never promises something
	 * the showroom will not deliver:
	 *  - window view: engine.js requires lat && geo_confidence !== 'city'
	 *    && a mapbox token (showroom-engine.php)
	 *  - studio + unit picking: both need project_3d_units
	 */
	function nadlan_fbar_items( $id ) {
		$glb   = trim( (string) get_post_meta( $id, 'project_model_glb', true ) );
		$units = trim( (string) get_post_meta( $id, 'project_3d_units', true ) );
		$has_u = ( '' !== $units && '[]' !== $units );
		$lat   = (float) get_post_meta( $id, 'lat', true );
		$conf  = (string) get_post_meta( $id, 'geo_confidence', true );
		$mbox  = trim( (string) get_option( 'nadlan_mapbox_token', '' ) );
		$draw  = trim( (string) get_post_meta( $id, 'project_3d_drawings_json', true ) );
		$slug  = get_post_field( 'post_name', $id );

		/* V7 (owner order 22.8): membership is decided on the BASE slug so the
		   language siblings (-en/-fr/-ru/-ar) inherit their district tour, and
		   DUO — the Somail tour's own hero, whose slug never says "somail" —
		   is named explicitly. Foreign-language pages deep-link the tour's
		   built-in English UI (the tours speak he/en). */
		$base_slug = preg_replace( '/-(en|fr|ru|ar)$/', '', $slug );
		$is_foreign = ( $base_slug !== $slug );
		$lang_q     = $is_foreign ? '?lang=en' : '';

		$tour     = function_exists( 'nadlan_sdedov_tour_slugs' )
			&& in_array( $base_slug, (array) nadlan_sdedov_tour_slugs(), true );
		$tour_url = home_url( '/tour/sde-dov/' . $lang_q );
		$somail_family = ( false !== strpos( $base_slug, 'somail' ) || 'duo-tel-aviv' === $base_slug );
		if ( $somail_family ) {
			$tour     = true;
			$tour_url = home_url( '/tour/somail/' . $lang_q );
		}

		// Earth flyover: link the scene that covers this project's district.
		// The /earth/ pages are quota-guarded server-side (75/day), so a public
		// link degrades politely instead of burning the Google budget.
		$earth_scene = '';
		if ( $somail_family ) {
			$earth_scene = 'somail';
		} elseif ( false !== strpos( $base_slug, 'sde-dov' ) || 'rainbow-tel-aviv' === $base_slug ) {
			$earth_scene = 'sde-dov';
		}

		return array(
			array(
				'k'    => 'model',
				'icon' => '&#9635;',
				'lbl'  => 'המודל התלת ממדי',
				'sub'  => 'לסובב את הבניין',
				'on'   => ( '' !== $glb ),
				'to'   => '.nl-theater, .nl-stage',
			),
			array(
				'k'    => 'unit',
				'icon' => '&#9744;',
				'lbl'  => 'בחירת דירה',
				'sub'  => 'לפי קומה וכיוון',
				'on'   => $has_u,
				'to'   => '.nl-panel, .nl-theater, .nl-stage',
			),
			array(
				'k'    => 'view',
				'icon' => '&#9707;',
				'lbl'  => 'לראות מה רואים מהחלון',
				'sub'  => 'לפי גובה הקומה והכיוון',
				'on'   => ( $has_u && $lat && 'city' !== $conf && '' !== $mbox ),
				'to'   => '.nl-theater, .nl-stage',
			),
			array(
				'k'    => 'studio',
				'icon' => '&#9998;',
				'lbl'  => 'עיצוב הדירה',
				'sub'  => 'ריהוט, מידות והערות',
				'on'   => true,
				'href' => home_url( '/tour/designer/' ),
			),
			array(
				'k'    => 'tour',
				'icon' => '&#9873;',
				'lbl'  => 'סיור ברובע',
				'sub'  => 'הסביבה בתלת ממד',
				'on'   => $tour,
				'href' => $tour_url,
			),
			array(
				'k'    => 'earth',
				'icon' => '&#9992;',
				'lbl'  => 'טיסה מעל המתחם',
				'sub'  => 'כדור הארץ בתלת ממד אמיתי',
				'on'   => ( '' !== $earth_scene ),
				'href' => home_url( '/earth/' . ( '' !== $earth_scene ? $earth_scene : 'sde-dov' ) . '/' ),
			),
			array(
				'k'    => 'plans',
				'icon' => '&#9707;',
				'lbl'  => 'תוכניות',
				'sub'  => 'תשריטי דירות',
				'on'   => ( '' !== $draw && '[]' !== $draw ),
				'to'   => '.nl-theater, .nl-stage',
			),
		);
	}
}

if ( ! function_exists( 'nadlan_fbar_css' ) ) {
	function nadlan_fbar_css() {
		return '.nlfb{margin:0 0 22px;padding:14px 16px;background:#FBF7EC;border:1px solid #E2DCD0;'
			. 'border-radius:14px;direction:rtl}'
			. '.nlfb-h{display:block;font:800 12px/1 Heebo,system-ui,sans-serif;color:#8A6A2F;'
			. 'letter-spacing:.05em;margin:0 0 11px}'
			. '.nlfb-row{display:grid;grid-template-columns:repeat(auto-fit,minmax(148px,1fr));gap:9px}'
			. '.nlfb-i{display:flex;gap:9px;align-items:flex-start;background:#fff;border:1px solid #E2DCD0;'
			. 'border-radius:11px;padding:10px 12px;text-decoration:none;color:#1B1A17;min-height:56px}'
			. '.nlfb-i b{display:block;font:700 13px/1.35 Heebo,system-ui,sans-serif;color:#1B1A17}'
			. '.nlfb-i s{display:block;font:400 11.5px/1.45 Heebo,system-ui,sans-serif;color:#6B6353;'
			. 'text-decoration:none;margin-top:2px}'
			. '.nlfb-i em{font-style:normal;font-size:15px;line-height:1.2;color:#B85410;flex:0 0 auto}'
			. 'a.nlfb-i:hover{border-color:#B85410;background:#FFFDF8}'
			. '.nlfb-i.off{opacity:.45;background:#F5F1E7;cursor:default}'
			. '.nlfb-i.off em{color:#8E877A}'
			. '.nlfb-i.off s::after{content:" · בקרוב"}'
			/* the window view is the one people never discover on their own */
			. '@media(prefers-reduced-motion:no-preference){'
			. '@keyframes nlfbPulse{0%,100%{box-shadow:0 0 0 0 rgba(184,84,16,0)}'
			. '50%{box-shadow:0 0 0 6px rgba(184,84,16,.16)}}'
			. 'a.nlfb-i[data-k="view"]{animation:nlfbPulse 2.8s ease-in-out infinite}'
			/* same nudge inside the showroom itself, on the tab and the CTA */
			. '.nl-tab[data-id="view"],.nl-btn--gold[data-act="winview"]{animation:nlfbPulse 2.8s ease-in-out infinite}'
			. '}'
			. '@media(max-width:520px){.nlfb-row{grid-template-columns:1fr 1fr}.nlfb-i{min-height:52px;padding:9px 10px}'
			. '.nlfb-i b{font-size:12.5px}.nlfb-i s{font-size:11px}}';
	}
}

if ( ! function_exists( 'nadlan_fbar_render' ) ) {
	function nadlan_fbar_render( $content ) {
		if ( ! is_singular( 'nadlan_project' ) || ! in_the_loop() || ! is_main_query() ) {
			return $content;
		}
		/* Presence check rather than a static flag, because this runs twice on
		   purpose - see the second add_filter below. */
		if ( false !== strpos( $content, 'class="nlfb"' ) ) {
			return $content;
		}

		$items = nadlan_fbar_items( get_the_ID() );
		$nlfb_head = "מה אפשר לעשות כאן";
		$nlfb_aria = "מה אפשר לעשות בעמוד הזה";
		/* Review mode (owner order 31.8.2026): chips that scroll to engine
		 * elements are dead on review pages - keep only real destinations,
		 * and speak as the independent reviewer, in the page's own language.
		 * The tools are OUR technology offering, never the developer's. */
		if ( function_exists( 'nadlan_project_mode' ) && 'showroom' !== nadlan_project_mode( get_the_ID() ) ) {
			$items = array_values( array_filter( $items, function ( $it ) { return ! empty( $it['href'] ); } ) );
			if ( ! $items ) { return $content; }
			$nlfb_lang = function_exists( 'nadlan_project_self_lang' ) ? nadlan_project_self_lang() : '';
			if ( '' === $nlfb_lang ) { $nlfb_lang = 'he'; }
			$nlfb_t = array(
				'he' => array( 'head' => "הכלים שלנו לבדיקת הפרויקט", 'aria' => "כלי הבדיקה של נדלן",
					'studio' => array( "מעצב הדירות שלנו", "בודקים ריהוט, מידות ומרחקים" ),
					'tour'   => array( "סיור תלת ממדי ברובע", "הסביבה של הפרויקט, בהפקת נדלן" ),
					'earth'  => array( "טיסה מעל האזור", "הדמיית כדור הארץ שלנו" ) ),
				'en' => array( 'head' => "Our project research tools", 'aria' => "NadLan research tools",
					'studio' => array( "Our apartment designer", "Test furniture, sizes and distances" ),
					'tour'   => array( "3D district tour", "The project area, produced by NadLan" ),
					'earth'  => array( "Flight over the area", "Our 3D Earth experience" ) ),
				'fr' => array( 'head' => "Nos outils d'étude du projet", 'aria' => "Outils NadLan",
					'studio' => array( "Notre studio d'aménagement", "Meubles, dimensions et distances" ),
					'tour'   => array( "Visite 3D du quartier", "Le secteur du projet, par NadLan" ),
					'earth'  => array( "Survol du secteur", "Notre expérience Terre 3D" ) ),
				'ru' => array( 'head' => "Наши инструменты проверки проекта", 'aria' => "Инструменты NadLan",
					'studio' => array( "Наш дизайнер квартир", "Мебель, размеры и расстояния" ),
					'tour'   => array( "3D-тур по району", "Окружение проекта от NadLan" ),
					'earth'  => array( "Полёт над районом", "Наш 3D-глобус" ) ),
				'ar' => array( 'head' => "أدواتنا لفحص المشروع", 'aria' => "أدوات نادلان",
					'studio' => array( "مصمم الشقق لدينا", "أثاث ومقاسات ومسافات" ),
					'tour'   => array( "جولة ثلاثية الأبعاد في الحي", "محيط المشروع من إنتاج نادلان" ),
					'earth'  => array( "تحليق فوق المنطقة", "تجربة الأرض ثلاثية الأبعاد لدينا" ) ),
			);
			$nlfb_v = isset( $nlfb_t[ $nlfb_lang ] ) ? $nlfb_t[ $nlfb_lang ] : $nlfb_t['he'];
			$nlfb_head = $nlfb_v['head'];
			$nlfb_aria = $nlfb_v['aria'];
			foreach ( $items as $nlfb_i => $nlfb_it ) {
				if ( isset( $nlfb_v[ $nlfb_it['k'] ] ) ) {
					$items[ $nlfb_i ]['lbl'] = $nlfb_v[ $nlfb_it['k'] ][0];
					$items[ $nlfb_i ]['sub'] = $nlfb_v[ $nlfb_it['k'] ][1];
				}
			}
		}
		$html  = '<nav class="nlfb" aria-label="' . esc_attr( $nlfb_aria ) . '">'
			. '<b class="nlfb-h">' . esc_html( $nlfb_head ) . '</b><div class="nlfb-row">';

		foreach ( $items as $it ) {
			$inner = '<em aria-hidden="true">' . $it['icon'] . '</em><span><b>' . esc_html( $it['lbl'] )
				. '</b><s>' . esc_html( $it['sub'] ) . '</s></span>';

			if ( ! $it['on'] ) {
				$html .= '<span class="nlfb-i off" data-k="' . esc_attr( $it['k'] ) . '">' . $inner . '</span>';
				continue;
			}
			$href = isset( $it['href'] ) ? $it['href'] : '#';
			$to   = isset( $it['to'] ) ? ' data-to="' . esc_attr( $it['to'] ) . '"' : '';
			$html .= '<a class="nlfb-i" data-k="' . esc_attr( $it['k'] ) . '" href="' . esc_url( $href ) . '"' . $to . '>'
				. $inner . '</a>';
		}

		$html .= '</div></nav>';
		return $html . $content;
	}
}
add_filter( 'the_content', 'nadlan_fbar_render', 11 );

/* Second pass, and it is not belt-and-braces.
 *
 * inc/utopia-sde-dov.php registers a filter at PHP_INT_MAX that DISCARDS the
 * incoming $content and rebuilds the page from post_content. Measured live:
 * the five UTOPIA pages showed no feature bar at all, and the same silently
 * happens to every other module that contributed earlier. Any future module
 * that rebuilds content wholesale would do the same to us.
 *
 * Running again at PHP_INT_MAX - with this module loaded AFTER utopia so it
 * wins the same-priority tie - repairs the page instead of arguing with it.
 * The presence check makes it a no-op everywhere else.
 *
 * Owner law 2026-08-07: content first, tools after. A blind prepend put
 * "מה אפשר לעשות כאן" as the FIRST thing a visitor (and Google) read on
 * utopia. The repair pass now inserts the bar AFTER the first substantive
 * paragraph of the rebuilt page (skipping a leading notice aside), falling
 * back to prepend only when no paragraph is found.
 */
if ( ! function_exists( 'nadlan_fbar_repair' ) ) {
	function nadlan_fbar_repair( $content ) {
		if ( ! is_singular( 'nadlan_project' ) || ! in_the_loop() || ! is_main_query() ) {
			return $content;
		}
		if ( false !== strpos( $content, 'class="nlfb"' ) ) {
			return $content;
		}
		$bar = nadlan_fbar_render( '' );
		if ( '' === $bar ) {
			return $content;
		}
		$off = 0;
		if ( preg_match( '/^\s*<aside class="nl-projnotice".*?<\/aside>/s', $content, $m ) ) {
			$off = strlen( $m[0] );
		}
		$p = strpos( $content, '</p>', $off );
		if ( false !== $p && $p < 4000 ) {
			return substr( $content, 0, $p + 4 ) . $bar . substr( $content, $p + 4 );
		}
		return $bar . $content;
	}
}
add_filter( 'the_content', 'nadlan_fbar_repair', PHP_INT_MAX );

add_action( 'wp_enqueue_scripts', function () {
	if ( ! is_singular( 'nadlan_project' ) ) {
		return;
	}
	wp_register_style( 'nadlan-feature-bar', false, array(), NADLAN_CONFIG_VERSION );
	wp_enqueue_style( 'nadlan-feature-bar' );
	wp_add_inline_style( 'nadlan-feature-bar', nadlan_fbar_css() );

	/* Scrolling to the showroom is done here rather than with a plain #anchor
	   because the engine markup carries no stable id, and adding one would mean
	   editing the shared engine. Selector list, first match wins. */
	wp_register_script( 'nadlan-feature-bar', '', array(), NADLAN_CONFIG_VERSION, true );
	wp_enqueue_script( 'nadlan-feature-bar' );
	wp_add_inline_script(
		'nadlan-feature-bar',
		'document.addEventListener("click",function(e){'
		. 'var a=e.target.closest&&e.target.closest(".nlfb-i[data-to]");if(!a)return;'
		. 'var t=document.querySelector(a.getAttribute("data-to"));if(!t)return;'
		. 'e.preventDefault();t.scrollIntoView({behavior:"smooth",block:"start"});'
		. '});'
	);
}, 20 );
