<?php
/**
 * Sitewide legal notice.
 *
 * The catalogue names third-party developers, projects and marks that we do not
 * own, on pages that also collect buyer enquiries. Naming someone else's product
 * to refer to it is ordinary descriptive use, but that only holds while the site
 * makes three things unmistakable on every page: we are not the official site,
 * the marks belong to their owners and appear for identification, and the data
 * comes from public sources and binds nobody. The removal address is part of the
 * same posture - an operator who takes a project down on request is behaving
 * like a directory, not like an impostor.
 *
 * Rendered from wp_footer (not post content) because kses strips markup out of
 * bands, and the notice must not depend on any editor saving it.
 *
 * @package nadlan-config
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

if ( ! function_exists( 'nadlan_legal_notice_contact' ) ) {
	/**
	 * Removal/correction address. Defaults to the site admin address so the
	 * channel we promise is one that provably receives mail; override with the
	 * nadlan_legal_contact option once a dedicated mailbox exists.
	 */
	function nadlan_legal_notice_contact() {
		$mail = trim( (string) get_option( 'nadlan_legal_contact', '' ) );
		if ( '' === $mail ) {
			$mail = (string) get_option( 'admin_email', '' );
		}
		return is_email( $mail ) ? $mail : '';
	}
}

if ( ! function_exists( 'nadlan_legal_notice_strings' ) ) {
	function nadlan_legal_notice_strings( $lang ) {
		$all = array(
			'he' => array(
				"nad-lan.co.il הוא אתר עצמאי ואינו אתר רשמי של יזם, קבלן או חברת שיווק כלשהם, ואינו פועל מטעמם.",
				"שמות פרויקטים, שמות חברות וסימני מסחר שייכים לבעליהם ומוצגים לצורך זיהוי בלבד.",
				"המידע נאסף ממקורות גלויים, אינו מהווה הצעה, ייעוץ או התחייבות, ואינו תחליף לבדיקה מול היזם.",
				"לתיקון פרטים או להסרת פרויקט:",
			),
			'en' => array(
				"nad-lan.co.il is an independent website. It is not the official site of any developer, contractor or marketing company, and does not act on their behalf.",
				"Project names, company names and trademarks belong to their owners and are shown for identification only.",
				"Information is gathered from public sources. It is not an offer, advice or commitment, and does not replace verification with the developer.",
				"To correct details or remove a project:",
			),
			'fr' => array(
				"nad-lan.co.il est un site indépendant. Ce n'est pas le site officiel d'un promoteur, d'un constructeur ou d'une société de commercialisation, et il n'agit pas en leur nom.",
				"Les noms de projets, les noms de sociétés et les marques appartiennent à leurs propriétaires et sont affichés à des fins d'identification uniquement.",
				"Les informations proviennent de sources publiques. Elles ne constituent ni une offre, ni un conseil, ni un engagement, et ne remplacent pas une vérification auprès du promoteur.",
				"Pour corriger des informations ou retirer un projet :",
			),
			'ru' => array(
				"nad-lan.co.il - независимый сайт. Он не является официальным сайтом какого-либо застройщика, подрядчика или маркетинговой компании и не действует от их имени.",
				"Названия проектов, названия компаний и товарные знаки принадлежат их владельцам и указаны только для идентификации.",
				"Информация собрана из открытых источников. Она не является предложением, консультацией или обязательством и не заменяет проверку у застройщика.",
				"Для исправления данных или удаления проекта:",
			),
			'ar' => array(
				"nad-lan.co.il موقع مستقل، وليس الموقع الرسمي لأي مطوّر أو مقاول أو شركة تسويق، ولا يعمل بالنيابة عنهم.",
				"أسماء المشاريع وأسماء الشركات والعلامات التجارية مملوكة لأصحابها وتُعرض لغرض التعريف فقط.",
				"المعلومات مجمّعة من مصادر علنية، ولا تشكّل عرضًا أو استشارة أو التزامًا، ولا تغني عن التحقق لدى المطوّر.",
				"لتصحيح التفاصيل أو إزالة مشروع:",
			),
		);
		return isset( $all[ $lang ] ) ? $all[ $lang ] : $all['he'];
	}
}

if ( ! function_exists( 'nadlan_legal_notice_render' ) ) {
	function nadlan_legal_notice_render() {
		if ( is_admin() || is_feed() || is_embed() || ( defined( 'REST_REQUEST' ) && REST_REQUEST ) ) {
			return;
		}
		$lang  = function_exists( 'nadlan_current_lang' ) ? nadlan_current_lang() : 'he';
		$lines = nadlan_legal_notice_strings( $lang );
		$mail  = nadlan_legal_notice_contact();
		$rtl   = in_array( $lang, array( 'he', 'ar' ), true );

		echo '<aside class="nl-legal" dir="' . ( $rtl ? 'rtl' : 'ltr' ) . '" role="note">';
		echo '<div class="nl-legal-in"><p>';
		echo '<strong>' . esc_html( $lines[0] ) . '</strong> ';
		echo esc_html( $lines[1] ) . ' ' . esc_html( $lines[2] );
		if ( '' !== $mail ) {
			/* antispambot keeps the address clickable while defeating harvesters */
			echo ' ' . esc_html( $lines[3] ) . ' <a href="mailto:' . antispambot( $mail, 1 ) . '">' . antispambot( $mail ) . '</a>'; // phpcs:ignore WordPress.Security.EscapeOutput
		}
		echo '</p></div></aside>';
	}
}
add_action( 'wp_footer', 'nadlan_legal_notice_render', 5 );

/* Per-project non-affiliation notice.
 *
 * The footer notice covers the site; this one sits in the page body next to the
 * developer name, because that is where the law asks for it. In the Tommy Hilfiger
 * appeal the Supreme Court put a trader who names another company's mark under a
 * duty to state the absence of sponsorship "actively, continuously and at
 * reasonable frequency", and section 2(a)(10) of the Consumer Protection Law makes
 * sponsorship, encouragement or authorisation a material matter in its own right.
 * A line in the footer satisfies neither. Naming the developer where one is
 * recorded is the point: a generic notice does not dispel an impression about a
 * specific company.
 */
if ( ! function_exists( 'nadlan_project_notice_strings' ) ) {
	function nadlan_project_notice_strings( $lang ) {
		$all = array(
			'he' => array( "אתר עצמאי", "עמוד זה אינו האתר הרשמי של %s ואינו מופעל מטעמה. נדל״ן היא פלטפורמת מידע עצמאית, ללא קשר מסחרי עם היזם. הפרטים נאספו ממקורות גלויים ויש לאמת אותם מול היזם.", "עמוד זה אינו אתר רשמי של היזם ואינו מופעל מטעמו. נדל״ן היא פלטפורמת מידע עצמאית. הפרטים נאספו ממקורות גלויים ויש לאמת אותם מול היזם." ),
			'en' => array( "Independent site", "This page is not the official website of %s and is not operated on its behalf. NadLan is an independent information platform with no commercial connection to the developer. Details were gathered from public sources and should be verified with the developer.", "This page is not the developer’s official website and is not operated on its behalf. NadLan is an independent information platform. Details were gathered from public sources and should be verified with the developer." ),
			'fr' => array( "Site indépendant", "Cette page n’est pas le site officiel de %s et n’est pas exploitée en son nom. NadLan est une plateforme d’information indépendante, sans lien commercial avec le promoteur. Les informations proviennent de sources publiques et doivent être vérifiées auprès du promoteur.", "Cette page n’est pas le site officiel du promoteur et n’est pas exploitée en son nom. NadLan est une plateforme d’information indépendante. Les informations proviennent de sources publiques et doivent être vérifiées auprès du promoteur." ),
			'ru' => array( "Независимый сайт", "Эта страница не является официальным сайтом %s и не управляется от её имени. NadLan - независимая информационная платформа, не связанная с застройщиком коммерческими отношениями. Данные собраны из открытых источников и подлежат проверке у застройщика.", "Эта страница не является официальным сайтом застройщика и не управляется от его имени. NadLan - независимая информационная платформа. Данные собраны из открытых источников и подлежат проверке у застройщика." ),
			'ar' => array( "موقع مستقل", "هذه الصفحة ليست الموقع الرسمي لـ%s ولا تُدار بالنيابة عنها. NadLan منصّة معلومات مستقلة، ولا تربطها علاقة تجارية بالمطوّر. جُمعت التفاصيل من مصادر علنية ويجب التحقق منها لدى المطوّر.", "هذه الصفحة ليست الموقع الرسمي للمطوّر ولا تُدار بالنيابة عنه. NadLan منصّة معلومات مستقلة. جُمعت التفاصيل من مصادر علنية ويجب التحقق منها لدى المطوّر." ),
		);
		return isset( $all[ $lang ] ) ? $all[ $lang ] : $all['he'];
	}
}

if ( ! function_exists( 'nadlan_project_notice_render' ) ) {
	function nadlan_project_notice_render( $content ) {
		if ( ! is_singular( 'nadlan_project' ) || ! in_the_loop() || ! is_main_query() ) {
			return $content;
		}
		static $done = false;
		if ( $done ) {
			return $content;
		}
		$done = true;
		$lang = function_exists( 'nadlan_current_lang' ) ? nadlan_current_lang() : 'he';
		$str  = nadlan_project_notice_strings( $lang );
		$dev  = trim( (string) get_post_meta( get_the_ID(), 'developer_name', true ) );
		$text = ( '' !== $dev ) ? sprintf( $str[1], $dev ) : $str[2];
		$rtl  = in_array( $lang, array( 'he', 'ar' ), true );
		$html = '<aside class="nl-projnotice" dir="' . ( $rtl ? 'rtl' : 'ltr' ) . '" role="note">'
			. '<b>' . esc_html( $str[0] ) . '</b><span>' . esc_html( $text ) . '</span></aside>';
		return $html . $content;
	}
}
/* Priority 20, deliberately: the showroom prepends at 10, the project profile at 5
 * and the price band at 9, each in front of whatever is already there. Running
 * first would bury this notice under all of them - which is exactly where it
 * landed on the first attempt, some 2,900px BELOW the enquiry form. Running last
 * puts it at the very top, ahead of the decision point. */
add_filter( 'the_content', 'nadlan_project_notice_render', 20 );

/* INTENT-FIRST ORDER (owner law, 2026-08-05).
 *
 * Measured live on ashira: the first text Google reads was this notice, then a
 * second disclaimer, and the article's own opening paragraph appeared nowhere
 * in the first eight text blocks. A page whose opening text is disclaimers
 * ranks as a page about disclaimers.
 *
 * The repair keeps the legal duty intact and reorders the page: the article's
 * first substantive paragraph moves to the very top, and the notice sits
 * DIRECTLY UNDER it - still high, still before any decision point, still
 * naming the developer. Mechanics: at priority 0 (before any module prepends
 * and before wpautop) the lead paragraph is cut out of the base content and
 * parked; at priority 21 (right after the notice prepended at 20) the page is
 * recomposed as lead, notice, everything else. If extraction fails on a page,
 * nothing moves and the notice stays at the top - the legal placement never
 * silently disappears. UTOPIA pages rebuild their content wholesale at
 * PHP_INT_MAX and discard this arrangement; their curated page already opens
 * with substance, so that is fine.
 */
if ( ! function_exists( 'nadlan_lead_is_provenance' ) ) {
	/* Editorial plumbing is not buyer content. Found live 2026-08-07: DUO's
	   page OPENED with "נערך עבור nad-lan.co.il על בסיס דוסייה, מקורות: ..."
	   and rainbow's with "עודכן ביוני 2026 · מקורות:" - the extractor had
	   faithfully promoted the sourcing note to the lead. These lines belong at
	   the bottom of the page, always. */
	function nadlan_lead_is_provenance( $plain ) {
		return (bool) preg_match(
			'/^(נערך עבור|עודכן ב|מקורות\s*[::]|על בסיס דוסיי|Sources\s*[::]|Compiled for)|^[^.]{0,40}(מקורות\s*[::])/u',
			trim( $plain )
		);
	}
}

if ( ! function_exists( 'nadlan_lead_extract' ) ) {
	function nadlan_lead_extract( $content ) {
		if ( ! is_singular( 'nadlan_project' ) || ! in_the_loop() || ! is_main_query() ) {
			return $content;
		}
		if ( isset( $GLOBALS['nl_lead_html'] ) ) {
			return $content;
		}
		/* Scan WHOLE <p> elements wherever they sit. Dossier-seeded pages nest
		   the opening inside <section><article><header> wrappers with a
		   <p class="byline"> provenance line first (DUO, live 2026-08-07) - an
		   anchored from-the-start scan misses all of it, and the pre-169 code
		   even promoted the byline WITH broken wrapper markup as the lead.
		   Cutting complete <p> elements leaves any wrappers intact. */
		$lead   = '';
		$parked = array();
		$rest   = $content;
		$offset = 0;
		for ( $i = 0; $i < 8; $i++ ) {
			if ( ! preg_match( '/<p\b[^>]*>.*?<\/p>/is', $rest, $m, PREG_OFFSET_CAPTURE, $offset ) ) {
				break;
			}
			$block = $m[0][0];
			$pos   = $m[0][1];
			if ( $pos > 2500 ) {
				break;
			}
			$plain    = trim( wp_strip_all_tags( $block ) );
			$byline   = false !== stripos( $block, 'class="byline"' ) || false !== stripos( $block, "class='byline'" );
			if ( $byline || nadlan_lead_is_provenance( $plain ) ) {
				$parked[] = $block;
				$rest     = substr( $rest, 0, $pos ) . substr( $rest, $pos + strlen( $block ) );
				$offset   = $pos;
				continue;
			}
			if ( mb_strlen( $plain ) >= 100 && '[' !== substr( $plain, 0, 1 ) ) {
				$lead = $block;
				$rest = substr( $rest, 0, $pos ) . substr( $rest, $pos + strlen( $block ) );
				break;
			}
			/* short or unclassified paragraph: leave it, keep scanning past it */
			$offset = $pos + strlen( $block );
		}
		if ( $parked ) {
			$rest .= "\n" . '<div class="nl-provenance">' . implode( "\n", $parked ) . '</div>';
		}
		if ( '' === $lead ) {
			/* provenance may still have been parked - keep that even without a lead */
			return $parked ? $rest : $content;
		}
		$GLOBALS['nl_lead_html'] = '<div class="nl-lead">' . $lead . '</div>';
		return $rest;
	}
}
add_filter( 'the_content', 'nadlan_lead_extract', 0 );

if ( ! function_exists( 'nadlan_lead_recompose' ) ) {
	function nadlan_lead_recompose( $content ) {
		if ( empty( $GLOBALS['nl_lead_html'] ) || ! is_singular( 'nadlan_project' ) || ! in_the_loop() || ! is_main_query() ) {
			return $content;
		}
		$lead = $GLOBALS['nl_lead_html'];
		unset( $GLOBALS['nl_lead_html'] );
		$notice = '';
		if ( 0 === strpos( $content, '<aside class="nl-projnotice"' ) ) {
			$end     = strpos( $content, '</aside>' );
			if ( false !== $end ) {
				$notice  = substr( $content, 0, $end + 8 );
				$content = substr( $content, $end + 8 );
			}
		}
		return $lead . $notice . $content;
	}
}
add_filter( 'the_content', 'nadlan_lead_recompose', 21 );

if ( ! function_exists( 'nadlan_legal_notice_css' ) ) {
	function nadlan_legal_notice_css() {
		if ( is_admin() ) {
			return;
		}
		wp_register_style( 'nadlan-legal-notice', false, array(), NADLAN_CONFIG_VERSION );
		wp_enqueue_style( 'nadlan-legal-notice' );
		wp_add_inline_style(
			'nadlan-legal-notice',
			'.nl-provenance{margin-top:26px;padding-top:12px;border-top:1px dashed #D9D2C4;'
			. 'font-size:12px;line-height:1.6;color:#8E877A}'
			. '.nl-legal{background:#14130F;color:#9B948A;padding:18px 0;margin:0}'
			. '.nl-legal-in{max-width:1240px;margin:0 auto;padding:0 clamp(14px,3vw,26px)}'
			. '.nl-legal p{margin:0;font:400 12.5px/1.75 Heebo,system-ui,sans-serif;max-width:1000px}'
			. '.nl-legal strong{color:#C9C2B4;font-weight:700}'
			. '.nl-legal a{color:#D8C79A;text-decoration:underline}'
			. '.nl-legal a:hover{color:#F2C14E}'
			. '.nl-projnotice{display:flex;gap:10px;align-items:baseline;flex-wrap:wrap;background:#FBF7EC;border:1px solid #E2DCD0;border-inline-start:4px solid #B85410;border-radius:12px;padding:12px 16px;margin:0 0 20px}'
			. '.nl-projnotice b{color:#8A3F0C;font:800 12.5px Heebo,system-ui,sans-serif;white-space:nowrap}'
			. '.nl-projnotice span{color:#4A4335;font:400 13px/1.65 Heebo,system-ui,sans-serif}'
		);
	}
}
add_action( 'wp_enqueue_scripts', 'nadlan_legal_notice_css', 20 );
