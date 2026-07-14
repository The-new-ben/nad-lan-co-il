<?php
/**
 * site-map.php - the curated HTML sitemap at /site-map/ (owner order 2026-07-12).
 *
 * "A good HTML sitemap for all the latest tools and products and pages...
 *  very smart... fits the SEO with the right hierarchy, easy to use, and
 *  NOT revealing all the website for scraping. Beautifully designed."
 *
 * The law of this page:
 * - CURATED HUBS ONLY (~45 links): products, archives, pillar pages, tools,
 *   guides, languages. Never a leaf dump - no per-project / per-listing /
 *   per-term enumeration. Leaves are reachable through their hubs; a scraper
 *   gets nothing here it could not get from the nav.
 * - Every link verified live before shipping (no dead links law).
 * - Live counts (projects/properties/professionals/terms) as trust chips.
 * - HE indexable + EN sibling via ?lang=en, self-canonical + hreflang pair.
 * - Design DNA: cream ground, white cards, hairline, gold kickers, Frank
 *   Ruhl titles; products carry the gold accent - they lead the page.
 */
if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

/* ---------- route ---------- */
add_action( 'init', function () {
	add_rewrite_rule( '^site-map/?$', 'index.php?nadlan_site_map=1', 'top' );
	// the pre-existing thin /sitemap/ WP page duplicated this surface - one canonical
	add_rewrite_rule( '^sitemap/?$', 'index.php?nadlan_site_map=301', 'top' );
	if ( get_option( 'nadlan_site_map_rewrite_v2' ) !== '1' ) {
		flush_rewrite_rules( false );
		update_option( 'nadlan_site_map_rewrite_v2', '1' );
	}
} );
add_filter( 'query_vars', function ( $v ) { $v[] = 'nadlan_site_map'; return $v; } );

if ( ! function_exists( 'nadlan_site_map_counts' ) ) {
	function nadlan_site_map_counts() {
		$c = get_transient( 'nadlan_site_map_counts' );
		if ( is_array( $c ) ) { return $c; }
		$get = function ( $pt ) { $n = wp_count_posts( $pt ); return isset( $n->publish ) ? (int) $n->publish : 0; };
		$c = array(
			'projects' => $get( 'nadlan_project' ),
			'props'    => $get( 'nadlan_property' ),
			'pros'     => $get( 'nadlan_professional' ),
			'terms'    => $get( 'nadlan_term' ),
		);
		set_transient( 'nadlan_site_map_counts', $c, 6 * HOUR_IN_SECONDS );
		return $c;
	}
}

if ( ! function_exists( 'nadlan_site_map_strings' ) ) {
	function nadlan_site_map_strings( $lang ) {
		$he = array(
			'title'      => 'מפת האתר: כל המוצרים, הכלים והמדריכים | נדלן',
			'desc'       => 'כל מה שיש בנדלן במקום אחד: בחירת דירה בתלת ממד, חדר התחדשות עירונית, ניהול השכרות, מחשבונים, מאגר בעלי מקצוע, מילון מונחים ומדריכים.',
			'kicker'     => 'מפת האתר',
			'h1'         => 'כל מה שיש בנדלן, במקום אחד',
			'sub'        => 'העמוד מרכז את המוצרים, הכלים והמדריכים הראשיים. מתוך כל מרכז מגיעים לכל עמוד באתר.',
			'stat_projects' => 'פרויקטים חדשים', 'stat_props' => 'נכסים', 'stat_pros' => 'בעלי מקצוע', 'stat_terms' => 'מונחים במילון',
			'product'    => 'מוצר',
			's_products' => 'המוצרים', 's_products_d' => 'מה שרק נדלן נותן: כל חוויה היא מוצר חי, בחינם.',
			's_projects' => 'פרויקטים חדשים', 's_projects_d' => 'כל פרויקט הוא מודל תלת ממדי חי: קומות, דירות, שמש ונוף.',
			's_props'    => 'דירות למכירה ולהשכרה', 's_props_d' => 'לוח נכסים עם מפה, השוואות ופרסום חינם.',
			's_renewal'  => 'התחדשות עירונית', 's_renewal_d' => 'המרכז המלא לבעלי דירות: מדריכים, בדיקה וחדר פרויקט.',
			's_pros'     => 'בעלי מקצוע', 's_pros_d' => 'מאגר מאומת מול נתוני gov.il.',
			's_tools'    => 'מחשבונים וכלים', 's_tools_d' => 'כל החישובים לפני קנייה, בחינם ובלי הרשמה.',
			's_know'     => 'ידע ומדריכים', 's_know_d' => 'תוכן מקצועי כתוב לעומק, בלי קיצורי דרך.',
			's_langs'    => 'שפות', 's_langs_d' => 'האתר מדבר חמש שפות.',
			's_global'   => 'השקעות בחו"ל', 's_global_d' => 'כל מיקום הוא עולם שלם: נתונים, מיסים, תהליך ופרויקטים בתלת ממד.',
			'l_globalhub'=> 'כל היעדים', 'l_gw_dubai' => 'השקעות נדל"ן בדובאי', 'l_gw_miami' => 'השקעות נדל"ן במיאמי', 'l_gw_ny' => 'השקעות נדל"ן בניו יורק',
		'l_gw_cyprus' => 'השקעות נדל"ן בקפריסין', 'l_gw_london' => 'השקעות נדל"ן בלונדון', 'l_gw_greece' => 'השקעות נדל"ן ביוון', 'l_gw_italy' => 'השקעות נדל"ן באיטליה', 'l_gw_thailand' => 'השקעות נדל"ן בתאילנד',
		'l_str_hub' => 'השוואת יעדי Airbnb בחו"ל', 'l_str_note' => 'מדריכי השכרה לטווח קצר: קפריסין, דובאי, יוון, איטליה, ספרד, פורטוגל, תאילנד',
		's_guides2' => 'מוקדי ידע נוספים', 's_guides2_d' => 'אשכולות התוכן המלאים: משפט, מיסוי, מסחרי, מכירה והשקעה.',
		'l_hub_lawyer' => 'עורך דין מקרקעין: המדריכים המלאים', 'l_hub_tax' => 'מיסוי נדל"ן ויועצי מס', 'l_hub_sell' => 'מכירת דירה: המדריך המלא', 'l_hub_comm' => 'נדל"ן מסחרי להשקעה', 'l_hub_invest' => 'נדל"ן להשקעה בישראל', 'l_hub_newproj' => 'פרויקטים חדשים: מדריכי רכישה מקבלן', 'l_hub_auction' => 'מכירת דירה במכרז דיגיטלי',
			'l_3d'       => 'בחירת דירה מתוך הבניין בתלת ממד', 'l_3d_n' => 'כל הפרויקטים',
			'l_myrenewal'=> 'חדר ההתחדשות של הבניין שלכם', 'l_urcheck' => 'בדיקת כדאיות התחדשות חינם',
			'l_myrentals'=> 'ניהול השכרות לבעלי דירות', 'l_studio' => 'סטודיו לעיצוב הדירה',
			'l_sched'    => 'תיאום סיורים ופגישות ביומן', 'l_sched_n' => 'בכל עמוד פרויקט, נכס ובעל מקצוע',
			'l_myappts'  => 'הפגישות שלי (אזור אישי)',
			'l_advcenter'=> 'מרכז המפרסמים', 'l_joinpro' => 'הצטרפות בעלי מקצוע ויזמים', 'l_advertise' => 'פרסום באתר',
			'l_allproj'  => 'כל הפרויקטים החדשים', 'l_bycity' => 'לפי עיר:', 'l_tama' => 'פרויקטי תמ״א 38', 'l_pinui' => 'פרויקטי פינוי בינוי',
			'l_examples' => 'דוגמאות חיות:',
			'l_allprops' => 'כל הנכסים', 'l_post' => 'פרסום דירה בחינם', 'l_compare' => 'השוואת נכסים',
			'l_urpillar' => 'התחדשות עירונית: המדריך המלא', 'l_urtama' => 'תמ״א 38', 'l_urpinui' => 'פינוי בינוי',
			'l_uralt'    => 'מה במקום תמ״א 38?', 'l_urmap' => 'מפת מתחמי ההתחדשות', 'l_uren' => 'Urban Renewal in English',
			'l_allpros'  => 'המאגר המלא', 'l_lawyer' => 'עורכי דין מקרקעין', 'l_shamai' => 'שמאי מקרקעין',
			'l_mortgage' => 'מחשבון משכנתא', 'l_tax' => 'מחשבון מס רכישה', 'l_cost' => 'עלות קנייה מלאה',
			'l_value'    => 'הערכת שווי נכס', 'l_tabu' => 'בדיקת נסח טאבו',
			'l_glossary' => 'מילון המונחים', 'l_buying' => 'מדריך קנייה מקבלן', 'l_invest' => 'מדריך השקעות נדל״ן',
			'honest'     => 'העמוד מציג את המרכזים הראשיים בלבד; כל עמודי הפרויקטים, הנכסים, בעלי המקצוע והמונחים נגישים מתוך המרכזים.',
		);
		$en = array(
			'title'      => 'Site Map: Every Product, Tool and Guide | Nadlan',
			'desc'       => 'Everything on Nadlan in one place: 3D apartment selection, the urban renewal room, free rental management, calculators, the professionals directory, glossary and guides.',
			'kicker'     => 'Site map',
			'h1'         => 'Everything on Nadlan, in one place',
			'sub'        => 'This page gathers the main products, tools and guides. Every page on the site is reachable from these hubs.',
			'stat_projects' => 'new projects', 'stat_props' => 'listings', 'stat_pros' => 'professionals', 'stat_terms' => 'glossary terms',
			'product'    => 'Product',
			's_products' => 'The products', 's_products_d' => 'What only Nadlan offers: every experience is a living product, free.',
			's_projects' => 'New projects', 's_projects_d' => 'Every project is a living 3D model: floors, apartments, sun and view.',
			's_props'    => 'Apartments for sale and rent', 's_props_d' => 'A listings board with a map, comparisons and free posting.',
			's_renewal'  => 'Urban renewal', 's_renewal_d' => 'The full center for homeowners: guides, a feasibility check and a project room.',
			's_pros'     => 'Professionals', 's_pros_d' => 'A directory verified against gov.il data.',
			's_tools'    => 'Calculators and tools', 's_tools_d' => 'Every pre-purchase calculation, free, no signup.',
			's_know'     => 'Knowledge and guides', 's_know_d' => 'Professional content written in depth, no shortcuts.',
			's_langs'    => 'Languages', 's_langs_d' => 'The site speaks five languages.',
			's_global'   => 'Global investment', 's_global_d' => 'Every location is a full world: data, taxes, process and 3D projects.',
			'l_globalhub'=> 'All destinations', 'l_gw_dubai' => 'Dubai real estate investment', 'l_gw_miami' => 'Miami real estate investment', 'l_gw_ny' => 'New York real estate investment',
		'l_gw_cyprus' => 'Cyprus real estate investment', 'l_gw_london' => 'London real estate investment', 'l_gw_greece' => 'Greece real estate investment', 'l_gw_italy' => 'Italy real estate investment', 'l_gw_thailand' => 'Thailand real estate investment',
		'l_str_hub' => 'Airbnb abroad: destination comparison', 'l_str_note' => 'Short-term-rental guides: Cyprus, Dubai, Greece, Italy, Spain, Portugal, Thailand',
		's_guides2' => 'More knowledge hubs', 's_guides2_d' => 'The full content clusters: legal, tax, commercial, selling and investing.',
		'l_hub_lawyer' => 'Real estate lawyer guides', 'l_hub_tax' => 'Real estate tax guides', 'l_hub_sell' => 'Selling an apartment: the full guide', 'l_hub_comm' => 'Commercial real estate investment', 'l_hub_invest' => 'Investment real estate in Israel', 'l_hub_newproj' => 'New projects: buying from a developer', 'l_hub_auction' => 'Sell by digital auction',
			'l_3d'       => 'Choose your apartment from inside the 3D building', 'l_3d_n' => 'all projects',
			'l_myrenewal'=> 'Your building\'s renewal room', 'l_urcheck' => 'Free renewal feasibility check',
			'l_myrentals'=> 'Rental management for landlords', 'l_studio' => 'The apartment design studio',
			'l_sched'    => 'Book tours and meetings on the calendar', 'l_sched_n' => 'on every project, listing and professional page',
			'l_myappts'  => 'My appointments (personal area)',
			'l_advcenter'=> 'The advertiser center', 'l_joinpro' => 'Join as a professional or developer', 'l_advertise' => 'Advertise on Nadlan',
			'l_allproj'  => 'All new projects', 'l_bycity' => 'By city:', 'l_tama' => 'TAMA 38 projects', 'l_pinui' => 'Pinui-Binui projects',
			'l_examples' => 'Live examples:',
			'l_allprops' => 'All listings', 'l_post' => 'Post a listing for free', 'l_compare' => 'Compare properties',
			'l_urpillar' => 'Urban renewal: the complete guide', 'l_urtama' => 'TAMA 38', 'l_urpinui' => 'Pinui-Binui',
			'l_uralt'    => 'What replaces TAMA 38?', 'l_urmap' => 'The renewal compounds map', 'l_uren' => 'Urban Renewal in English',
			'l_allpros'  => 'The full directory', 'l_lawyer' => 'Real estate lawyers', 'l_shamai' => 'Property appraisers',
			'l_mortgage' => 'Mortgage calculator', 'l_tax' => 'Purchase tax calculator', 'l_cost' => 'Full purchase cost',
			'l_value'    => 'Property value estimator', 'l_tabu' => 'Tabu extract check',
			'l_glossary' => 'The real estate glossary', 'l_buying' => 'Buying from a developer: the guide', 'l_invest' => 'Real estate investment guide',
			'honest'     => 'This page lists the main hubs only; every project, listing, professional and term page is reachable from its hub.',
		);
		return 'en' === $lang ? $en : $he;
	}
}

add_action( 'template_redirect', function () {
	$smv = get_query_var( 'nadlan_site_map' );
	if ( ! $smv ) { return; }
	if ( '301' === (string) $smv ) { wp_redirect( home_url( '/site-map/' ), 301 ); exit; }
	$lang = ( isset( $_GET['lang'] ) && 'en' === sanitize_key( wp_unslash( $_GET['lang'] ) ) ) ? 'en' : 'he';
	$T = nadlan_site_map_strings( $lang );
	$C = nadlan_site_map_counts();
	$en = ( 'en' === $lang );
	$he_url = home_url( '/site-map/' );
	$en_url = home_url( '/site-map/?lang=en' );
	$self   = $en ? $en_url : $he_url;

	add_filter( 'pre_get_document_title', function () use ( $T ) { return $T['title']; }, 99 );
	add_action( 'wp_head', function () use ( $T, $self, $he_url, $en_url ) {
		echo '<meta name="description" content="' . esc_attr( $T['desc'] ) . '">' . "\n";
		echo '<link rel="canonical" href="' . esc_url( $self ) . '">' . "\n";
		echo '<link rel="alternate" hreflang="he" href="' . esc_url( $he_url ) . '">' . "\n";
		echo '<link rel="alternate" hreflang="en" href="' . esc_url( $en_url ) . '">' . "\n";
		echo '<link rel="alternate" hreflang="x-default" href="' . esc_url( $he_url ) . '">' . "\n";
		echo '<script type="application/ld+json">' . wp_json_encode( array(
			'@context' => 'https://schema.org', '@type' => 'CollectionPage',
			'name' => $T['h1'], 'description' => $T['desc'], 'url' => $self,
		), JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES ) . '</script>' . "\n";
	}, 4 );

	$u = function ( $p ) { return esc_url( home_url( $p ) ); };
	$cities = array( 'תל אביב-יפו', 'ירושלים', 'חיפה', 'רמת גן', 'נתניה', 'בת ים' );
	$city_lbl = $en ? array( 'Tel Aviv', 'Jerusalem', 'Haifa', 'Ramat Gan', 'Netanya', 'Bat Yam' ) : $cities;

	get_header();
	?>
<div class="nlsm" dir="<?php echo $en ? 'ltr' : 'rtl'; ?>" lang="<?php echo esc_attr( $lang ); ?>">
	<style>
	.nlsm{max-width:1160px;margin:0 auto;padding:26px 16px 70px;font-family:Heebo,sans-serif;color:#1B1A17}
	.nlsm h1,.nlsm h2{font-family:"Frank Ruhl Libre",Georgia,serif}
	.nlsm-head{text-align:center;padding:26px 0 8px}
	.nlsm-kicker{font:700 12.5px Heebo;letter-spacing:.06em;color:#9C7A3C;text-transform:uppercase;margin:0 0 10px}
	.nlsm-head h1{font-size:clamp(1.6rem,3.6vw,2.35rem);margin:0 0 10px;line-height:1.28}
	.nlsm-head .sub{color:#51483A;font:400 15px/1.7 Heebo;max-width:620px;margin:0 auto}
	.nlsm-lang{margin-top:14px}
	.nlsm-lang a{color:#9C7A3C;font:600 13px Heebo;text-decoration:none;border:1px solid #E2DCD0;border-radius:999px;padding:7px 14px}
	.nlsm-stats{display:flex;gap:12px;justify-content:center;flex-wrap:wrap;margin:26px 0 34px}
	.nlsm-stat{background:#F3EEE3;border:1px solid #E2DCD0;border-radius:14px;padding:12px 20px;text-align:center;min-width:120px}
	.nlsm-stat b{display:block;font:800 22px "Frank Ruhl Libre",serif;color:#1B1A17}
	.nlsm-stat span{font:600 12px Heebo;color:#8E877A}
	.nlsm-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(330px,1fr));gap:16px}
	.nlsm-card{background:#fff;border:1px solid #E2DCD0;border-radius:16px;padding:22px;transition:border-color .2s}
	.nlsm-card:hover{border-color:#9C7A3C}
	.nlsm-card--product{border:1.5px solid #D6C189;background:linear-gradient(180deg,#FDFBF6,#fff)}
	.nlsm-card h2{display:flex;align-items:center;gap:10px;font-size:1.18rem;margin:0 0 4px}
	.nlsm-card h2 svg{width:20px;height:20px;color:#9C7A3C;flex:0 0 auto}
	.nlsm-chip{font:700 10.5px Heebo;letter-spacing:.05em;color:#14130F;background:#D6C189;border-radius:6px;padding:3px 7px;margin-inline-start:auto;text-transform:uppercase}
	.nlsm-note{font:400 11px/1.5 Heebo;color:#A79E8D;display:block}
	.nlsm-card .d{font:400 13px/1.6 Heebo;color:#8E877A;margin:0 0 14px}
	.nlsm-card ul{list-style:none;margin:0;padding:0}
	.nlsm-card li{padding:6px 0;border-top:1px solid #F3EEE3;font:400 14px/1.5 Heebo}
	.nlsm-card li:first-child{border-top:0}
	.nlsm-card a{color:#1B1A17;text-decoration:none;font-weight:600}
	.nlsm-card a:hover{color:#9C7A3C}
	.nlsm-card li i{font-style:normal;color:#A79E8D;font-size:12px;display:block}
	.nlsm-inline a{display:inline-block;margin-inline-end:4px;font-weight:600;color:#51483A!important;font-size:13px;background:#F3EEE3;border:1px solid #E2DCD0;border-radius:999px;padding:5px 11px;margin-top:5px}
	.nlsm-inline a:hover{border-color:#9C7A3C;color:#9C7A3C!important}
	.nlsm-inline .lbl{font:600 12.5px Heebo;color:#8E877A}
	.nlsm-honest{text-align:center;font:400 12.5px/1.7 Heebo;color:#8E877A;max-width:640px;margin:36px auto 0}
	</style>

	<header class="nlsm-head">
		<p class="nlsm-kicker"><?php echo esc_html( $T['kicker'] ); ?></p>
		<h1><?php echo esc_html( $T['h1'] ); ?></h1>
		<p class="sub"><?php echo esc_html( $T['sub'] ); ?></p>
		<p class="nlsm-lang"><a href="<?php echo esc_url( $en ? $he_url : $en_url ); ?>"><?php echo $en ? 'עברית' : 'English'; ?></a></p>
	</header>

	<div class="nlsm-stats">
		<div class="nlsm-stat"><b><?php echo number_format( $C['projects'] ); ?></b><span><?php echo esc_html( $T['stat_projects'] ); ?></span></div>
		<div class="nlsm-stat"><b><?php echo number_format( $C['props'] ); ?></b><span><?php echo esc_html( $T['stat_props'] ); ?></span></div>
		<div class="nlsm-stat"><b><?php echo number_format( $C['pros'] ); ?></b><span><?php echo esc_html( $T['stat_pros'] ); ?></span></div>
		<?php if ( $C['terms'] ) : ?><div class="nlsm-stat"><b><?php echo number_format( $C['terms'] ); ?></b><span><?php echo esc_html( $T['stat_terms'] ); ?></span></div><?php endif; ?>
	</div>

	<div class="nlsm-grid">

		<section class="nlsm-card nlsm-card--product">
			<h2><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" aria-hidden="true"><path d="M4 21V8l8-5 8 5v13"/><path d="M9 21v-6h6v6"/><path d="M9 12h.01M15 12h.01"/></svg><?php echo esc_html( $T['s_products'] ); ?><span class="nlsm-chip"><?php echo esc_html( $T['product'] ); ?></span></h2>
			<p class="d"><?php echo esc_html( $T['s_products_d'] ); ?></p>
			<ul>
				<li><a href="<?php echo $u( '/projects/' ); ?>"><?php echo esc_html( $T['l_3d'] ); ?></a></li>
				<li><a href="<?php echo $u( '/my-renewal/' ); ?>"><?php echo esc_html( $T['l_myrenewal'] ); ?></a></li>
				<li><a href="<?php echo $u( '/my-rentals/' . ( $en ? '?lang=en' : '' ) ); ?>"><?php echo esc_html( $T['l_myrentals'] ); ?></a></li>
				<li><a href="<?php echo $u( '/studio/' ); ?>"><?php echo esc_html( $T['l_studio'] ); ?></a></li>
				<li><a href="<?php echo $u( '/my-appointments/' ); ?>"><?php echo esc_html( $T['l_sched'] ); ?></a><i><?php echo esc_html( $T['l_sched_n'] ); ?></i></li>
				<li><a href="<?php echo $u( '/advertiser-center/' ); ?>"><?php echo esc_html( $T['l_advcenter'] ); ?></a></li>
			</ul>
		</section>

		<section class="nlsm-card">
			<h2><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" aria-hidden="true"><path d="M3 21h18M6 21V5l6-3 6 3v16"/><path d="M9 9h.01M15 9h.01M9 13h.01M15 13h.01M9 17h.01M15 17h.01"/></svg><?php echo esc_html( $T['s_projects'] ); ?></h2>
			<p class="d"><?php echo esc_html( $T['s_projects_d'] ); ?></p>
			<ul>
				<li><a href="<?php echo $u( '/projects/' ); ?>"><?php echo esc_html( $T['l_allproj'] ); ?></a></li>
				<li><a href="<?php echo $u( '/projects/?project_type=tama38' ); ?>"><?php echo esc_html( $T['l_tama'] ); ?></a></li>
				<li><a href="<?php echo $u( '/projects/?project_type=pinui_binui' ); ?>"><?php echo esc_html( $T['l_pinui'] ); ?></a></li>
				<li class="nlsm-inline"><span class="lbl"><?php echo esc_html( $T['l_bycity'] ); ?></span><br>
					<?php foreach ( $cities as $i => $c ) : ?><a href="<?php echo $u( '/projects/?city=' . rawurlencode( $c ) ); ?>"><?php echo esc_html( $city_lbl[ $i ] ); ?></a><?php endforeach; ?>
				</li>
			</ul>
		</section>

		<section class="nlsm-card">
			<h2><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" aria-hidden="true"><path d="M3 11l9-8 9 8"/><path d="M5 9v12h14V9"/><path d="M10 21v-6h4v6"/></svg><?php echo esc_html( $T['s_props'] ); ?></h2>
			<p class="d"><?php echo esc_html( $T['s_props_d'] ); ?></p>
			<ul>
				<li><a href="<?php echo $u( '/properties/' ); ?>"><?php echo esc_html( $T['l_allprops'] ); ?></a></li>
				<li><a href="<?php echo $u( '/post-listing/' ); ?>"><?php echo esc_html( $T['l_post'] ); ?></a></li>
				<li><a href="<?php echo $u( '/compare/' ); ?>"><?php echo esc_html( $T['l_compare'] ); ?></a></li>
				<li class="nlsm-inline"><span class="lbl"><?php echo esc_html( $T['l_bycity'] ); ?></span><br>
					<?php foreach ( array_slice( $cities, 0, 4 ) as $i => $c ) : ?><a href="<?php echo $u( '/properties/?city=' . rawurlencode( $c ) ); ?>"><?php echo esc_html( $city_lbl[ $i ] ); ?></a><?php endforeach; ?>
				</li>
			</ul>
		</section>

		<section class="nlsm-card nlsm-card--product">
			<h2><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" aria-hidden="true"><path d="M4 21V10l5-4V3h6v3l5 4v11"/><path d="M12 21v-5"/><path d="M8 13h.01M16 13h.01M12 10h.01"/></svg><?php echo esc_html( $T['s_renewal'] ); ?><span class="nlsm-chip"><?php echo esc_html( $T['product'] ); ?></span></h2>
			<p class="d"><?php echo esc_html( $T['s_renewal_d'] ); ?></p>
			<ul>
				<li><a href="<?php echo $u( '/urban-renewal/' ); ?>"><?php echo esc_html( $T['l_urpillar'] ); ?></a></li>
				<li><a href="<?php echo $u( '/urban-renewal/check/' ); ?>"><?php echo esc_html( $T['l_urcheck'] ); ?></a></li>
				<li><a href="<?php echo $u( '/urban-renewal/tama-38/' ); ?>"><?php echo esc_html( $T['l_urtama'] ); ?></a></li>
				<li><a href="<?php echo $u( '/urban-renewal/pinui-binui/' ); ?>"><?php echo esc_html( $T['l_urpinui'] ); ?></a></li>
				<li><a href="<?php echo $u( '/urban-renewal/tama-38-alternatives/' ); ?>"><?php echo esc_html( $T['l_uralt'] ); ?></a></li>
				<li><a href="<?php echo $u( '/urban-renewal/map/' ); ?>"><?php echo esc_html( $T['l_urmap'] ); ?></a></li>
				<li><a href="<?php echo $u( '/urban-renewal/english-guide/' ); ?>"><?php echo esc_html( $T['l_uren'] ); ?></a></li>
			</ul>
		</section>

		<section class="nlsm-card">
			<h2><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" aria-hidden="true"><circle cx="9" cy="8" r="3.2"/><path d="M3.5 20c.6-3.2 2.8-5 5.5-5s4.9 1.8 5.5 5"/><path d="M16 4.5a3.2 3.2 0 010 7"/><path d="M17.5 15c2 .5 3.2 2 3.5 5"/></svg><?php echo esc_html( $T['s_pros'] ); ?></h2>
			<p class="d"><?php echo esc_html( $T['s_pros_d'] ); ?></p>
			<ul>
				<li><a href="<?php echo $u( '/professionals/' ); ?>"><?php echo esc_html( $T['l_allpros'] ); ?></a></li>
				<li><a href="<?php echo $u( '/professionals/?profession=lawyer' ); ?>"><?php echo esc_html( $T['l_lawyer'] ); ?></a></li>
				<li><a href="<?php echo $u( '/professionals/?profession=shamai' ); ?>"><?php echo esc_html( $T['l_shamai'] ); ?></a></li>
				<li><a href="<?php echo $u( '/join-pro/' ); ?>"><?php echo esc_html( $T['l_joinpro'] ); ?></a></li>
				<li><a href="<?php echo $u( '/advertise/' ); ?>"><?php echo esc_html( $T['l_advertise'] ); ?></a></li>
			</ul>
		</section>

		<section class="nlsm-card">
			<h2><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" aria-hidden="true"><rect x="4" y="3" width="16" height="18" rx="2"/><path d="M8 7h8M8 11h3M13 11h3M8 15h3M13 15h3"/></svg><?php echo esc_html( $T['s_tools'] ); ?></h2>
			<p class="d"><?php echo esc_html( $T['s_tools_d'] ); ?></p>
			<ul>
				<li><a href="<?php echo $u( '/mortgage-calculator/' ); ?>"><?php echo esc_html( $T['l_mortgage'] ); ?></a></li>
				<li><a href="<?php echo $u( '/purchase-tax-calculator/' ); ?>"><?php echo esc_html( $T['l_tax'] ); ?></a></li>
				<li><a href="<?php echo $u( '/apartment-purchase-cost-calculator/' ); ?>"><?php echo esc_html( $T['l_cost'] ); ?></a></li>
				<li><a href="<?php echo $u( '/property-value-estimator/' ); ?>"><?php echo esc_html( $T['l_value'] ); ?></a></li>
				<li><a href="<?php echo $u( '/tabu-extract-check/' ); ?>"><?php echo esc_html( $T['l_tabu'] ); ?></a></li>
			</ul>
		</section>

		<section class="nlsm-card">
			<h2><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" aria-hidden="true"><path d="M4 19.5V5a2 2 0 012-2h13v17H6a2 2 0 00-2 2z"/><path d="M4 19.5A2 2 0 016 17.5h13"/><path d="M9 7h6M9 11h4"/></svg><?php echo esc_html( $T['s_know'] ); ?></h2>
			<p class="d"><?php echo esc_html( $T['s_know_d'] ); ?></p>
			<ul>
				<li><a href="<?php echo $u( '/glossary/' ); ?>"><?php echo esc_html( $T['l_glossary'] ); ?></a></li>
				<li><a href="<?php echo $u( '/buying-apartment/' ); ?>"><?php echo esc_html( $T['l_buying'] ); ?></a></li>
				<li><a href="<?php echo $u( '/investment/' ); ?>"><?php echo esc_html( $T['l_invest'] ); ?></a></li>
			</ul>
		</section>

		<section class="nlsm-card nlsm-card--product">
			<h2><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M12 3v3m0 12v3M5.6 5.6l2.1 2.1m8.6 8.6l2.1 2.1M3 12h3m12 0h3M5.6 18.4l2.1-2.1m8.6-8.6l2.1-2.1"/></svg><?php echo esc_html( $T['s_global'] ); ?><span class="nlsm-chip"><?php echo esc_html( $T['product'] ); ?></span></h2>
			<p class="d"><?php echo esc_html( $T['s_global_d'] ); ?></p>
			<ul>
				<li><a href="<?php echo $u( '/global/' . ( $en ? '?lang=en' : '' ) ); ?>"><?php echo esc_html( $T['l_globalhub'] ); ?></a></li>
				<li><a href="<?php echo $u( '/global/dubai/' . ( $en ? '?lang=en' : '' ) ); ?>"><?php echo esc_html( $T['l_gw_dubai'] ); ?></a></li>
				<li><a href="<?php echo $u( '/global/miami/' . ( $en ? '?lang=en' : '' ) ); ?>"><?php echo esc_html( $T['l_gw_miami'] ); ?></a></li>
				<li><a href="<?php echo $u( '/global/new-york/' . ( $en ? '?lang=en' : '' ) ); ?>"><?php echo esc_html( $T['l_gw_ny'] ); ?></a></li>
				<li><a href="<?php echo $u( '/global/cyprus/' . ( $en ? '?lang=en' : '' ) ); ?>"><?php echo esc_html( $T['l_gw_cyprus'] ); ?></a></li>
				<li><a href="<?php echo $u( '/global/london/' . ( $en ? '?lang=en' : '' ) ); ?>"><?php echo esc_html( $T['l_gw_london'] ); ?></a></li>
				<li><a href="<?php echo $u( '/global/greece/' . ( $en ? '?lang=en' : '' ) ); ?>"><?php echo esc_html( $T['l_gw_greece'] ); ?></a></li>
				<li><a href="<?php echo $u( '/global/italy/' . ( $en ? '?lang=en' : '' ) ); ?>"><?php echo esc_html( $T['l_gw_italy'] ); ?></a></li>
				<li><a href="<?php echo $u( '/global/thailand/' . ( $en ? '?lang=en' : '' ) ); ?>"><?php echo esc_html( $T['l_gw_thailand'] ); ?></a></li>
				<li><a href="<?php echo $u( '/short-term-rentals-abroad/' ); ?>"><?php echo esc_html( $T['l_str_hub'] ); ?></a> <span class="nlsm-note"><?php echo esc_html( $T['l_str_note'] ); ?></span></li>
			</ul>
		</section>

		<section class="nlsm-card">
			<h2><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" aria-hidden="true"><path d="M4 19.5A2.5 2.5 0 016.5 17H20M4 19.5A2.5 2.5 0 006.5 22H20V2H6.5A2.5 2.5 0 004 4.5v15z"/></svg><?php echo esc_html( $T['s_guides2'] ); ?></h2>
			<p class="d"><?php echo esc_html( $T['s_guides2_d'] ); ?></p>
			<ul>
				<li><a href="<?php echo $u( '/investment/' ); ?>"><?php echo esc_html( $T['l_hub_invest'] ); ?></a></li>
				<li><a href="<?php echo $u( '/real-estate-lawyer/' ); ?>"><?php echo esc_html( $T['l_hub_lawyer'] ); ?></a></li>
				<li><a href="<?php echo $u( '/real-estate-tax-advisor/' ); ?>"><?php echo esc_html( $T['l_hub_tax'] ); ?></a></li>
				<li><a href="<?php echo $u( '/selling-apartment/' ); ?>"><?php echo esc_html( $T['l_hub_sell'] ); ?></a></li>
				<li><a href="<?php echo $u( '/commercial-real-estate/' ); ?>"><?php echo esc_html( $T['l_hub_comm'] ); ?></a></li>
				<li><a href="<?php echo $u( '/new-projects/' ); ?>"><?php echo esc_html( $T['l_hub_newproj'] ); ?></a></li>
				<li><a href="<?php echo $u( '/sell-by-auction/' ); ?>"><?php echo esc_html( $T['l_hub_auction'] ); ?></a></li>
			</ul>
		</section>

		<section class="nlsm-card">
			<h2><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c2.5 2.6 3.8 5.7 3.8 9S14.5 18.4 12 21c-2.5-2.6-3.8-5.7-3.8-9S9.5 5.6 12 3z"/></svg><?php echo esc_html( $T['s_langs'] ); ?></h2>
			<p class="d"><?php echo esc_html( $T['s_langs_d'] ); ?></p>
			<ul>
				<li><a href="<?php echo $u( '/en/' ); ?>">English</a></li>
				<li><a href="<?php echo $u( '/fr/' ); ?>">Français</a></li>
				<li><a href="<?php echo $u( '/ru/' ); ?>">Русский</a></li>
				<li><a href="<?php echo $u( '/ar/' ); ?>">العربية</a></li>
			</ul>
		</section>

	</div>

	<p class="nlsm-honest"><?php echo esc_html( $T['honest'] ); ?></p>
</div>
	<?php
	get_footer();
	exit;
} );
