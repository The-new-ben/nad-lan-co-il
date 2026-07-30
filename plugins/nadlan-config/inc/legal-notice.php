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

if ( ! function_exists( 'nadlan_legal_notice_css' ) ) {
	function nadlan_legal_notice_css() {
		if ( is_admin() ) {
			return;
		}
		wp_register_style( 'nadlan-legal-notice', false, array(), NADLAN_CONFIG_VERSION );
		wp_enqueue_style( 'nadlan-legal-notice' );
		wp_add_inline_style(
			'nadlan-legal-notice',
			'.nl-legal{background:#14130F;color:#9B948A;padding:18px 0;margin:0}'
			. '.nl-legal-in{max-width:1240px;margin:0 auto;padding:0 clamp(14px,3vw,26px)}'
			. '.nl-legal p{margin:0;font:400 12.5px/1.75 Heebo,system-ui,sans-serif;max-width:1000px}'
			. '.nl-legal strong{color:#C9C2B4;font-weight:700}'
			. '.nl-legal a{color:#D8C79A;text-decoration:underline}'
			. '.nl-legal a:hover{color:#F2C14E}'
		);
	}
}
add_action( 'wp_enqueue_scripts', 'nadlan_legal_notice_css', 20 );
