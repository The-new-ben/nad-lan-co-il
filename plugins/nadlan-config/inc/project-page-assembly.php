<?php
/**
 * nadlan-config - project page assembly seeds.
 *
 * One-shot, data-first enhancement for flagship project pages. It avoids
 * render-time wrappers so schema meta is present before wp_head and the
 * article body stays editable in WordPress.
 */

if ( ! defined( 'ABSPATH' ) ) { exit; }

if ( ! function_exists( 'nadlan_project_page_find_by_slug' ) ) {
	function nadlan_project_page_find_by_slug( $slug ) {
		$post = get_page_by_path( sanitize_title( (string) $slug ), OBJECT, 'nadlan_project' );
		return $post && $post->ID ? $post : null;
	}
}

if ( ! function_exists( 'nadlan_project_page_rainbow_faq' ) ) {
	function nadlan_project_page_rainbow_faq() {
		return array(
			array(
				'q' => 'מהו Rainbow Tel Aviv?',
				'a' => 'Rainbow Tel Aviv הוא פרויקט מגורים חדש במתחם שדה דב בתל אביב, של ישראל קנדה, הכולל מגדל מגורים גבוה ובנייני בוטיק במתחם חופי חדש.',
			),
			array(
				'q' => 'כמה דירות יש בפרויקט?',
				'a' => 'לפי שיווק היזם מדובר בכ-480 יחידות דיור. פרסומים תכנוניים ומקורות עירוניים ציינו גם 459 יחידות, ולכן בעמוד מוצגת הבחנה בין נתוני שיווק לבין נתוני היתר.',
			),
			array(
				'q' => 'האם המחירים בעמוד מחייבים?',
				'a' => 'לא. אומדני מחיר בעמוד מבוססים על עסקאות ודיווחים ציבוריים בלבד, ואינם הצעה, התחייבות או מחיר יזם. מחיר וזמינות מחייבים אימות מול היזם.',
			),
			array(
				'q' => 'מה אפשר לבדוק במודל התלת ממדי?',
				'a' => 'אפשר לבחור קומה ודירה, להשוות שטח, כיוון, נוף, אור ושמש, ולשלוח פנייה ממוקדת עם היחידה שנבחרה.',
			),
			array(
				'q' => 'האם אפשר להתחיל רכישה דרך העמוד?',
				'a' => 'העמוד מאפשר בדיקת רכישה לא מחייבת. לפני כל התחייבות נדרש אימות זמינות, מחיר, מסמכים ותנאים מול היזם ואנשי המקצוע הרלוונטיים.',
			),
			array(
				'q' => 'למי מתאים עמוד כזה?',
				'a' => 'העמוד מתאים לרוכשים, משקיעים, תושבי חוץ וליזמים שרוצים להציג פרויקט בצורה אינטראקטיבית, מדידה ומחוברת ללידים.',
			),
		);
	}
}

if ( ! function_exists( 'nadlan_project_page_rainbow_seo_block' ) ) {
	function nadlan_project_page_rainbow_seo_block() {
		$faq = nadlan_project_page_rainbow_faq();
		ob_start();
		?>
<!-- wp:html -->
<!-- nadlan-rainbow-seo-v1610-start -->
<section class="nadlan-guide nadlan-rainbow-seo" dir="rtl">
	<div class="nadlan-guide__byline">עודכן ביוני 2026 · מקורות: אתר Rainbow, ישראל קנדה, שדה דב, גלובס, כלכליסט וביזפורטל</div>
	<div class="nadlan-guide__note">
		<strong>שורה תחתונה למשקיע ולרוכש:</strong>
		<p>Rainbow Tel Aviv הוא אחד מפרויקטי הדגל של שדה דב. העמוד הזה מרכז מידע ציבורי, אומדני מחיר לא מחייבים ותצוגת בחירה אינטראקטיבית, כדי לעזור להבין קומות, כיוונים, קו נוף והמשך בדיקה לפני פנייה ליזם.</p>
	</div>
	<div class="nadlan-guide__cards">
		<article>
			<span>מיקום</span>
			<strong>שדה דב, תל אביב-יפו</strong>
			<p>מתחם חופי חדש בצפון תל אביב, באזור שדה התעופה לשעבר, בקרבה לים, לפארקים מתוכננים ולצירי תחבורה עתידיים.</p>
		</article>
		<article>
			<span>יזם</span>
			<strong>ישראל קנדה</strong>
			<p>הפרויקט משווק כמתחם מגורים חדש עם מגדל גבוה, בנייני בוטיק, שטחי מסחר ושירותים לדיירים.</p>
		</article>
		<article>
			<span>דירות</span>
			<strong>כ-480 לפי שיווק היזם</strong>
			<p>יש להציג בשקיפות גם את הפער מול נתוני היתר שפורסמו סביב 459 יחידות. אמת לפני שיווק.</p>
		</article>
		<article>
			<span>מחיר</span>
			<strong>אומדן ציבורי בלבד</strong>
			<p>דיווחים ציבוריים הציגו עסקאות סביב עשרות אלפי שקלים למ"ר, אך מחיר וזמינות מחייבים אישור יזם.</p>
		</article>
	</div>
	<section class="nadlan-guide__section">
		<h2>דירות למכירה ב-Rainbow Tel Aviv: מחיר, זמינות ובדיקת עסקה</h2>
		<p>מי שמחפש דירות למכירה ב-Rainbow Tel Aviv מחפש בדרך כלל שלושה דברים: מחיר, זמינות ותחושת ביטחון לפני פנייה. לכן העמוד מציג מודל בחירה, אומדן מחיר לא מחייב כאשר יש מקור ציבורי, ושדות פנייה שמאפשרים לשמור את הקומה, היחידה, הכיוון, השטח והכוונה של המתעניין.</p>
		<p>מחיר הדירה אינו מוצג כהצעה מחייבת. לפי פרסומים בגלובס, כלכליסט וביזפורטל, עסקאות בשדה דב ובריינבו דווחו בטווחי מחיר גבוהים במיוחד, עם שונות לפי קומה, כיוון, שטח, מרפסת ומועד העסקה. כל אומדן כזה צריך להיבדק מול היזם, חוזה המכר והיועצים המקצועיים לפני החלטה.</p>
	</section>
	<section class="nadlan-guide__section">
		<h2>למה המודל התלת ממדי חשוב לרוכשים וליזמים</h2>
		<p>רוכש לא קונה רק מספר חדרים. הוא מנסה להבין איפה הדירה יושבת במגדל, לאיזה כיוון היא פונה, מה רואים מהמרפסת, כמה אור יש, ומה השלב הבא אם זה מתאים. לכן תצוגת הפרויקט מחברת בין המודל, בחירת יחידה, אומדן לא מחייב, ליווי מקצועי ופנייה מסודרת.</p>
		<p>ליזם או מנהל שיווק, זה יוצר עמוד מכירה מדיד: כל לחיצה על דירה, צפייה במבט, בקשת תוכנית או בדיקת רכישה יכולה להיכנס לפאנל הלידים במקום להיעלם בשיחת WhatsApp לא מתועדת.</p>
	</section>
	<section class="nadlan-guide__section">
		<h2>שאלות נפוצות על Rainbow Tel Aviv</h2>
		<div class="nadlan-guide__faq">
			<?php foreach ( $faq as $row ) : ?>
				<details>
					<summary><?php echo esc_html( $row['q'] ); ?></summary>
					<p><?php echo esc_html( $row['a'] ); ?></p>
				</details>
			<?php endforeach; ?>
		</div>
	</section>
	<div class="nadlan-guide__disclaimer">המידע בעמוד מבוסס על מקורות ציבוריים ועל המחשה מקורית. אין לראות בו ייעוץ, הצעה, התחייבות, תכנית מכר או נתון זמינות רשמי. כל מחיר, דירה, תוכנית ותנאי רכישה מחייבים בדיקה ואישור מול היזם ואנשי המקצוע.</div>
	<p class="nadlan-guide__sources">מקורות לעיון: <a href="https://rainbow-telaviv.com/" rel="nofollow noopener" target="_blank">Rainbow Tel Aviv</a>, <a href="https://www.israel-canada.co.il/projects/tel-aviv/rainbow" rel="nofollow noopener" target="_blank">ישראל קנדה</a>, <a href="https://sdedov.co.il/project/rainbow/" rel="nofollow noopener" target="_blank">Sde Dov</a>, <a href="https://www.globes.co.il/news/article.aspx?did=1001511649" rel="nofollow noopener" target="_blank">גלובס</a>, <a href="https://www.calcalist.co.il/market/article/bj9leo2fxx" rel="nofollow noopener" target="_blank">כלכליסט</a>, <a href="https://www.bizportal.co.il/realestates/news/article/20033505" rel="nofollow noopener" target="_blank">ביזפורטל</a>.</p>
</section>
<!-- nadlan-rainbow-seo-v1610-end -->
<!-- /wp:html -->
		<?php
		return trim( ob_get_clean() );
	}
}

if ( ! function_exists( 'nadlan_project_page_seed_rainbow' ) ) {
	function nadlan_project_page_seed_rainbow() {
		if ( get_option( 'nadlan_rainbow_seed_v1610' ) ) {
			return;
		}
		$post = nadlan_project_page_find_by_slug( 'rainbow-tel-aviv' );
		if ( ! $post ) {
			return;
		}
		$post_id = (int) $post->ID;
		$faq = nadlan_project_page_rainbow_faq();
		$meta = array(
			'amenities' => 'בריכת אינפיניטי, בריכה למבוגרים בלבד, ספא, חדר כושר, מתחמי עבודה, בית קפה, חללי ילדים, קרבה לים, פארקים מתוכננים, תחבורה עתידית',
			'official_site_url' => 'https://rainbow-telaviv.com/,https://www.israel-canada.co.il/projects/tel-aviv/rainbow,https://sdedov.co.il/project/rainbow/',
			'price_range' => 'אומדן ציבורי לא מחייב: פרסומים ב-2025-2026 הציגו עסקאות בשדה דב ובריינבו סביב כ-75,000-92,000 ש"ח למ"ר, עם שונות לפי קומה, כיוון ומועד. מחיר וזמינות מחייבים אישור יזם.',
			'price_min' => '5500000',
			'price_max' => '16000000',
			'project_faq_json' => wp_json_encode( $faq, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES ),
			'project_3d_avg_price_per_sqm' => '82000',
			'project_3d_price_source_note' => 'אומדן לא מחייב לפי דיווחים ציבוריים בגלובס, כלכליסט וביזפורטל בשנים 2025-2026. נדרש אימות מול היזם.',
		);
		foreach ( $meta as $key => $value ) {
			update_post_meta( $post_id, $key, $value );
		}
		$content = (string) $post->post_content;
		if ( strpos( $content, 'nadlan-rainbow-seo-v1610-start' ) === false ) {
			wp_update_post( array(
				'ID'           => $post_id,
				'post_content' => nadlan_project_page_rainbow_seo_block() . "\n\n" . $content,
			) );
		}
		update_option( 'nadlan_rainbow_seed_v1610', time(), false );
	}
}
add_action( 'init', 'nadlan_project_page_seed_rainbow', 30 );

add_filter( 'nadlan_config_healthcheck', function ( $out ) {
	$post = nadlan_project_page_find_by_slug( 'rainbow-tel-aviv' );
	$out['project_page_assembly'] = array(
		'loaded'       => true,
		'rainbow_id'   => $post ? (int) $post->ID : 0,
		'rainbow_seed' => (bool) get_option( 'nadlan_rainbow_seed_v1610' ),
		'faq_meta'     => $post ? ( get_post_meta( (int) $post->ID, 'project_faq_json', true ) !== '' ) : false,
		'price_meta'   => $post ? ( get_post_meta( (int) $post->ID, 'price_range', true ) !== '' ) : false,
	);
	return $out;
} );
