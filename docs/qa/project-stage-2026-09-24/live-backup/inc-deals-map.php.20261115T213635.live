<?php
/**
 * nadlan-config - the developer deals map at the top of /developer-deals/ (HAD-743, Ben 15.11.2026: "בלי מתגים, תעלה").
 * Design: Claude Design canvas https://claude.ai/artifact/Rg8mHtQitrYSGF9McF1Bus (docs/design-lab/deals-map/).
 * Every deal carries the wording as published, the month it was published, its source and whether we confirmed it is still
 * offered; a deal that ended is kept in the archive, never on the map. Locations are approximate (city or neighbourhood).
 * Grey dots: our 1,003 project points (assets/deals/projects.json). JS: assets/deals/deals.js, CSS: assets/deals/deals.css.
 */

if ( ! defined( 'ABSPATH' ) ) { exit; }

if ( ! function_exists( 'nadlan_dm_deals' ) ) {
	/** The deals. k: pay | rent | loan | price | gift. first: share paid at signing; firstAbs: a sum; worth: published value in ILS. */
	function nadlan_dm_deals() {
		return array(
			array( 'id' => 'glilyam', 'dev' => 'גינדי', 'devFull' => 'גינדי החזקות', 'project' => 'גליל ים, הרצליה', 'city' => 'הרצליה', 'lat' => 32.1570, 'lng' => 34.8120, 'color' => '#14161A', 'k' => 'rent', 'kind' => 'שכר דירה עד האכלוס', 'short' => '10% ביד', 'terms' => 'תשלום שכר דירה ל-3 שנים, 10% הון ראשוני ו-30% הלוואת קבלן. 5 חדרים מ-5.28 מיליון ₪.', 'price' => 5280000, 'first' => 0.10, 'worth' => 360000, 'bar' => array( array( 10, 'חתימה', 'a' ), array( 30, 'הלוואת קבלן', 'b' ), array( 60, 'באכלוס', 'c' ) ), 'pub' => 'קיץ 2026', 'checked' => '', 'hot' => true ),
			array( 'id' => 'ytown', 'dev' => 'צרפתי', 'devFull' => 'צרפתי צבי ובניו', 'project' => 'Y TOWN, ז\'בוטינסקי 42, ראשון לציון', 'city' => 'ראשון לציון', 'lat' => 31.9900, 'lng' => 34.7800, 'color' => '#00897B', 'k' => 'rent', 'kind' => 'הטבה חודשית עד האכלוס', 'short' => 'עד 7,000 ₪ לחודש', 'terms' => 'הטבה של עד 7,000 ₪ בחודש לכ-4 שנים. דירות 3 ו-4 חדרים מכ-2.88 מיליון ₪.', 'price' => 2880000, 'worth' => 336000, 'bar' => array( array( 100, 'לפי לוח התשלומים', 'c' ) ), 'pub' => '2026', 'checked' => '15.11.2026', 'src' => 'https://www.yad2.co.il/yad1/project/12463' ),
			array( 'id' => 'benshemen', 'dev' => 'אאורה', 'devFull' => 'אאורה ישראל', 'project' => 'בן שמן, לוד', 'city' => 'לוד', 'lat' => 31.9540, 'lng' => 34.9050, 'color' => '#0B63B6', 'k' => 'pay', 'kind' => 'כניסה עם סכום קטן', 'short' => '550 אלף בכניסה', 'terms' => 'כניסה עם 550 אלף ₪, היתרה לאחר שנה וחצי. מ-2.68 מיליון ₪.', 'price' => 2680000, 'firstAbs' => 550000, 'bar' => array( array( 21, 'כניסה', 'a' ), array( 79, 'אחרי שנה וחצי', 'c' ) ), 'pub' => '2026', 'checked' => '' ),
			array( 'id' => 'noga', 'dev' => 'בראל', 'devFull' => 'קבוצת בראל', 'project' => 'NOGA, נוף הגליל', 'city' => 'נוף הגליל', 'lat' => 32.7150, 'lng' => 35.3300, 'color' => '#2E5BFF', 'k' => 'pay', 'kind' => '11/89 והלוואת קבלן', 'short' => '11/89', 'terms' => '11% בחוזה והיתרה באכלוס, ו-50% הלוואת קבלן. מ-1.26 מיליון ₪.', 'price' => 1260000, 'first' => 0.11, 'bar' => array( array( 11, 'חוזה', 'a' ), array( 50, 'הלוואת קבלן', 'b' ), array( 39, 'באכלוס', 'c' ) ), 'pub' => 'יוני 2026', 'checked' => '' ),
			array( 'id' => 'biltmore', 'dev' => 'י.ע.ז', 'devFull' => 'י.ע.ז', 'project' => 'Biltmore, תל אביב', 'city' => 'תל אביב', 'lat' => 32.0790, 'lng' => 34.7810, 'color' => '#8A1C5C', 'k' => 'pay', 'kind' => '0% בחתימה', 'short' => '0% בחתימה', 'terms' => '0% בחתימה. 5 חדרים ב-7.65 מיליון ₪.', 'price' => 7650000, 'first' => 0, 'bar' => array( array( 3, '', 'a' ), array( 97, 'לפי לוח התשלומים', 'c' ) ), 'pub' => 'יוני 2026', 'checked' => '' ),
			array( 'id' => 'east', 'dev' => 'EAST&TLV', 'devFull' => 'EAST&TLV', 'project' => 'EAST&TLV, תל אביב', 'city' => 'תל אביב', 'lat' => 32.0690, 'lng' => 34.8060, 'color' => '#5B3FA8', 'k' => 'pay', 'kind' => '50/50', 'short' => '50/50', 'terms' => '50% עכשיו, 50% בעוד שנתיים. המחיר לפי יחידה.', 'bar' => array( array( 50, 'עכשיו', 'a' ), array( 50, 'בעוד שנתיים', 'c' ) ), 'pub' => 'יוני 2026', 'checked' => '' ),
			array( 'id' => 'tzahala', 'dev' => 'דנקנר', 'devFull' => 'דנקנר קנלוב', 'project' => 'רמות צהלה, תל אביב', 'city' => 'תל אביב', 'lat' => 32.1170, 'lng' => 34.8330, 'color' => '#B4541A', 'k' => 'price', 'kind' => 'הנחה במחיר', 'short' => '250 אלף פחות', 'terms' => 'חזרה למחיר פריסייל בשתי דירות: 7.65 במקום 7.9 מיליון ₪.', 'price' => 7650000, 'worth' => 250000, 'bar' => array( array( 100, 'לפי לוח התשלומים', 'c' ) ), 'pub' => 'יוני 2026', 'checked' => '' ),
			array( 'id' => 'kata', 'dev' => 'קטה', 'devFull' => 'קטה גרופ', 'project' => 'פתח תקווה', 'city' => 'פתח תקווה', 'lat' => 32.0930, 'lng' => 34.8780, 'color' => '#2F6F2A', 'k' => 'gift', 'kind' => 'פטור מדמי ניהול', 'short' => 'דמי ניהול חינם', 'terms' => 'פטור מדמי ניהול ל-3 שנים. מ-2.71 מיליון ₪.', 'price' => 2710000, 'worth' => 25000, 'bar' => array( array( 100, 'לפי לוח התשלומים', 'c' ) ), 'pub' => 'יוני 2026', 'checked' => '' ),
			array( 'id' => 'sharet', 'dev' => 'רוטשטיין', 'devFull' => 'רוטשטיין', 'project' => 'שרת, תל אביב', 'city' => 'תל אביב', 'lat' => 32.0990, 'lng' => 34.7890, 'color' => '#1D3F8F', 'k' => 'gift', 'kind' => 'דירה מרוהטת', 'short' => 'מרוהטת', 'terms' => 'דירה מרוהטת. 4 חדרים מ-6.66 מיליון ₪.', 'price' => 6660000, 'bar' => array( array( 100, 'לפי לוח התשלומים', 'c' ) ), 'pub' => 'יוני 2026', 'checked' => '' ),
			array( 'id' => 'rayk', 'dev' => 'רייק', 'devFull' => 'רייק', 'project' => 'לוד', 'city' => 'לוד', 'lat' => 31.9480, 'lng' => 34.8880, 'color' => '#6D4C41', 'k' => 'price', 'kind' => 'הנחה ללוחמים', 'short' => 'הנחה ללוחמים', 'terms' => 'הנחה נוספת ללוחמים. מ-1.95 מיליון ₪.', 'price' => 1950000, 'bar' => array( array( 100, 'לפי לוח התשלומים', 'c' ) ), 'pub' => 'יוני 2026', 'checked' => '' ),
			array( 'id' => 'dona', 'dev' => 'דונה', 'devFull' => 'דונה', 'project' => 'חריש', 'city' => 'חריש', 'lat' => 32.4600, 'lng' => 35.0450, 'color' => '#7A6A00', 'k' => 'gift', 'kind' => 'מפרט משודרג', 'short' => 'מטבח ומיזוג', 'terms' => 'מטבח משודרג, מיזוג מרכזי ומפרט משופר. לא פורסם מחיר אחיד.', 'bar' => array( array( 100, 'לפי לוח התשלומים', 'c' ) ), 'pub' => 'יוני 2026', 'checked' => '' ),
			array( 'id' => 'isa', 'dev' => 'ISA ומאגמה', 'devFull' => 'ISA ומאגמה', 'project' => 'מבשרת ציון', 'city' => 'מבשרת ציון', 'lat' => 31.8000, 'lng' => 35.1500, 'color' => '#3E5C76', 'k' => 'rent', 'kind' => 'שכירות שהופכת לקנייה', 'short' => 'Rent-to-Own', 'terms' => 'שכירות שהיא גם אופציה לקנייה. לא פורסם מחיר אחיד.', 'bar' => array( array( 100, 'שכירות עם אופציה', 'c' ) ), 'pub' => 'יולי 2026', 'checked' => '' ),
		);
	}
}

if ( ! function_exists( 'nadlan_dm_archive' ) ) {
	function nadlan_dm_archive() {
		return array(
			array( 'אאורה וחבר, רמת השרון, חדרה, קריית אונו', '15/85 ופטור מהצמדה', 'ימי המכירה היו 24 עד 28.8.2026' ),
			array( 'אביב מליסרון', 'ריבית 0.99% על עד 30% מהמחיר', 'תקנון המבצע היה עד 31.5.2026' ),
			array( 'פרשקובסקי, שישה פרויקטים', 'מכרז הצעות חסויות', 'המכרז נסגר באוגוסט 2026' ),
			array( 'גינדי VOGUE, שדה דב', 'מחיר פתיחה של 49 אלף ₪ למ"ר', 'מבצע 2025' ),
		);
	}
}

if ( ! function_exists( 'nadlan_dm_is_page' ) ) {
	function nadlan_dm_is_page() {
		if ( ! is_page() ) { return false; }
		$p = get_queried_object();
		return $p && 'developer-deals' === $p->post_name && ! preg_match( '~/(en|fr|ru|ar)/~', (string) ( $_SERVER['REQUEST_URI'] ?? '' ) );
	}
}

if ( ! function_exists( 'nadlan_dm_fmt' ) ) {
	function nadlan_dm_fmt( $n ) {
		$n = (float) $n;
		return $n >= 1000000 ? rtrim( rtrim( number_format( $n / 1000000, 2, '.', '' ), '0' ), '.' ) . ' מיליון ₪' : number_format( round( $n / 1000 ) ) . ' אלף ₪';
	}
}

if ( ! function_exists( 'nadlan_dm_render' ) ) {
	function nadlan_dm_render() {
		$deals = nadlan_dm_deals();
		$wa    = preg_replace( '/\D+/', '', (string) get_option( 'nadlan_whatsapp_e164', '972525101555' ) );
		$base  = plugins_url( 'assets/deals/', dirname( __FILE__ ) );
		$data  = array(
			'deals'     => $deals,
			'hotId'     => 'glilyam',
			'wa'        => $wa,
			'pointsUrl' => $base . 'projects.json?v=1',
			'mlJs'      => 'https://cdnjs.cloudflare.com/ajax/libs/maplibre-gl/5.24.0/maplibre-gl.js',
			'mlCss'     => 'https://cdnjs.cloudflare.com/ajax/libs/maplibre-gl/5.24.0/maplibre-gl.css',
			'style'     => 'https://tiles.openfreemap.org/styles/positron',
		);
		$kinds = array( 'all' => 'הכל', 'pay' => '10/90, 20/80 ותשלומים', 'rent' => 'שכר דירה עד האכלוס', 'price' => 'הנחה במחיר', 'gift' => 'מתנות ופטורים' );
		$waq   = function ( $t ) use ( $wa ) { return 'https://wa.me/' . $wa . '?text=' . rawurlencode( $t ); };
		ob_start();
		?>
<section id="nldm" class="nldm" dir="rtl" aria-label="מפת מבצעי הקבלנים">
	<p class="nldm-lead">כל מבצעי הקבלנים על מפה אחת: 20/80 ו-10/90, הלוואת קבלן, שכר דירה עד האכלוס, הנחות במחיר ופטורים. לכל מבצע כתוב מה בדיוק פורסם ומתי, כמה צריך ביד ביום החתימה, כמה הוא שווה בשקלים, ואם בדקנו שהוא עדיין בתוקף.</p>
	<div class="nldm-live"><span class="nldm-pulse" aria-hidden="true"></span><span><b><?php echo (int) count( $deals ); ?></b> מבצעים על המפה · <b><?php echo (int) count( nadlan_dm_archive() ); ?></b> בארכיון · עודכן 15.11.2026</span></div>
	<div class="nldm-ctas">
		<a class="nldm-btn is-main" href="<?php echo esc_url( $waq( 'היי, אשמח למחירון מעודכן ולתנאי המבצעים של הקבלנים' ) ); ?>" target="_blank" rel="noopener">בקשו מחירון מעודכן</a>
		<a class="nldm-btn" href="<?php echo esc_url( $waq( 'היי, אשמח להתייעץ עם יועץ משכנתאות על מבצע קבלן' ) ); ?>" target="_blank" rel="noopener">ייעוץ משכנתא חינם</a>
	</div>

	<div class="nldm-cash">
		<div class="nldm-cash-top"><label for="nldm-cash">כמה יש לכם ביד היום?</label><output id="nldm-cash-out" for="nldm-cash">600 אלף ₪</output></div>
		<input id="nldm-cash" type="range" min="0" max="1500000" step="10000" value="600000">
		<div class="nldm-legend" aria-live="polite"><span class="nldm-think" hidden><i></i><i></i><i></i> מחשב</span><span class="nldm-lg is-fit">מתאים לכם: <b data-n="fit">0</b></span><span class="nldm-lg is-no">צריך יותר: <b data-n="no">0</b></span><span class="nldm-lg is-unk">בקשו מחיר: <b data-n="unk">0</b></span></div>
	</div>

	<nav class="nldm-chips" aria-label="סוג המבצע">
		<?php foreach ( $kinds as $k => $l ) : ?><button type="button" data-k="<?php echo esc_attr( $k ); ?>"<?php echo 'all' === $k ? ' class="is-on" aria-pressed="true"' : ' aria-pressed="false"'; ?>><?php echo esc_html( $l ); ?></button><?php endforeach; ?>
	</nav>

	<div class="nldm-stage">
		<div id="nldm-map" class="nldm-map" role="region" aria-label="מפה תלת ממדית של המבצעים"><div class="nldm-map-wait"><span></span><span></span><span></span></div></div>
		<div class="nldm-mapbar">
			<button type="button" data-act="tilt">מבט מלמעלה</button>
			<button type="button" data-act="all">כל הארץ</button>
			<button type="button" data-act="near">קרוב אליי</button>
		</div>
		<p class="nldm-mapnote">נקודה אפורה: פרויקט חדש מהמאגר שלנו, לחצו עליה לכרטיס שלו. מיקומי המבצעים משוערים, לפי העיר או השכונה.</p>
	</div>

	<article class="nldm-sheet" aria-live="polite">
		<div class="nldm-sheet-head"><span class="nldm-chip" data-f="init"></span><div><span class="nldm-sub" data-f="sub"></span><h2 data-f="project"></h2><span class="nldm-kind" data-f="kind"></span></div></div>
		<blockquote class="nldm-terms"><small>כפי שפורסם</small><span data-f="terms"></span></blockquote>
		<div class="nldm-when"><b>מתי משלמים</b><div class="nldm-bar" data-f="bar"></div></div>
		<div class="nldm-nums">
			<div><small>מחיר מ-</small><b data-f="price"></b></div>
			<div><small>ביד בחתימה</small><b data-f="need"></b></div>
			<div class="is-worth"><small>שווה בשקלים</small><b data-f="worth"></b></div>
		</div>
		<p class="nldm-check" data-f="check"></p>
		<div class="nldm-act">
			<a class="nldm-btn is-main" data-f="wa1" target="_blank" rel="noopener" href="#">בדקו אם המבצע בתוקף וקבלו מחירון</a>
			<a class="nldm-btn" data-f="wa2" target="_blank" rel="noopener" href="#">משכנתא והשלמת הון למבצע הזה</a>
		</div>
		<div class="nldm-tools">
			<a href="/mortgage-calculator/"><b>מחשבון משכנתא</b><span>ההחזר החודשי עם המבצע</span></a>
			<a href="/purchase-tax-calculator/"><b>מחשבון מס רכישה</b><span>כמה מס על הדירה</span></a>
			<a href="/projects/"><b>כל הפרויקטים החדשים</b><span>דירות מקבלן עם מחירים ומפה</span></a>
			<a href="/my-rentals/"><b>קונים להשקעה?</b><span>ניהול השכירות עלינו</span></a>
		</div>
	</article>

	<section class="nldm-list" aria-label="כל המבצעים">
		<h2>כל מבצעי הקבלנים, מהמתאים לכם ביותר</h2>
		<ol>
		<?php foreach ( $deals as $d ) : ?>
			<li data-id="<?php echo esc_attr( $d['id'] ); ?>"><button type="button" data-pick="<?php echo esc_attr( $d['id'] ); ?>"><span class="nldm-dot" style="background:<?php echo esc_attr( $d['color'] ); ?>"></span><span class="nldm-li"><b><?php echo esc_html( $d['project'] ); ?></b><span><?php echo esc_html( $d['devFull'] . ' · ' . $d['kind'] . ' · פורסם ' . $d['pub'] ); ?></span><span class="nldm-li-terms"><?php echo esc_html( $d['terms'] ); ?></span></span><span class="nldm-need"></span></button></li>
		<?php endforeach; ?>
		</ol>
	</section>

	<section class="nldm-expert" aria-label="התייעצות עם מומחה">
		<h2>מצאתם מבצע? אל תחתמו לבד</h2>
		<p>מבצע של קבלן משנה בעיקר מתי משלמים. לפני שחותמים כדאי לבדוק שלושה דברים: האם הבנק יאשר משכנתא למבנה התשלומים, מה המחיר בלי המבצע, ומה כתוב בחוזה על ההצמדה.</p>
		<div class="nldm-expert-grid">
			<a href="<?php echo esc_url( $waq( 'היי, אשמח לייעוץ משכנתא למבצע קבלן (20/80 או 10/90)' ) ); ?>" target="_blank" rel="noopener"><b>יועץ משכנתאות</b><span>האם הבנק יאשר את מבנה התשלומים</span></a>
			<a href="<?php echo esc_url( $waq( 'היי, אשמח לשמוע על הלוואה להשלמת הון לדירה מקבלן' ) ); ?>" target="_blank" rel="noopener"><b>השלמת הון</b><span>הלוואה לסכום שחסר ביום החתימה</span></a>
			<a href="<?php echo esc_url( $waq( 'היי, אשמח לבדיקה של חוזה מקבלן לפני חתימה' ) ); ?>" target="_blank" rel="noopener"><b>בדיקה לפני חתימה</b><span>עורך דין ושמאי על החוזה והמחיר</span></a>
		</div>
	</section>

	<section class="nldm-archive" aria-label="ארכיון מבצעים שהסתיימו">
		<h2>ארכיון: מבצעים שהסתיימו</h2>
		<ul>
		<?php foreach ( nadlan_dm_archive() as $a ) : ?><li><b><?php echo esc_html( $a[0] ); ?></b> · <?php echo esc_html( $a[1] ); ?> · <span><?php echo esc_html( $a[2] ); ?></span></li><?php endforeach; ?>
		</ul>
	</section>
	<script type="application/json" id="nldm-data"><?php echo wp_json_encode( $data, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES | JSON_HEX_TAG ); ?></script>
</section>
		<?php
		return (string) ob_get_clean();
	}
}

add_filter( 'the_content', function ( $content ) {
	if ( ! in_the_loop() || ! is_main_query() || ! nadlan_dm_is_page() || false !== strpos( $content, 'id="nldm"' ) ) { return $content; }
	$at = stripos( $content, '</h1>' );
	if ( false === $at ) { return nadlan_dm_render() . $content; }
	$at += 5; // the article opens with its own h1: the map goes right under it (H1 -> answer -> CTAs -> stage)
	return substr( $content, 0, $at ) . nadlan_dm_render() . substr( $content, $at );
}, 6 );

add_action( 'wp_enqueue_scripts', function () {
	if ( ! nadlan_dm_is_page() ) { return; }
	$base = plugins_url( 'assets/deals/', dirname( __FILE__ ) );
	$dir  = dirname( __DIR__ ) . '/assets/deals/';
	wp_enqueue_style( 'nadlan-deals-map', $base . 'deals.css', array(), (string) @filemtime( $dir . 'deals.css' ) );
	wp_enqueue_script( 'nadlan-deals-map', $base . 'deals.js', array(), (string) @filemtime( $dir . 'deals.js' ), true );
} );
