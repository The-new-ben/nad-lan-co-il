<?php
/**
 * Title: Ashira Sde Dov showroom v2
 * Slug: nadlan-revenue/project-showroom-ashira-v2
 * Categories: featured, media
 * Description: Clean v2 project showroom with a rotating context model and a separate apartment selector.
 *
 * @package WordPress
 * @subpackage NadLan_Revenue
 * @since NadLan Revenue 1.1.0
 */

$asset_base = trailingslashit( get_template_directory_uri() ) . 'assets/projects/ashira-sde-dov/';
?>
<!-- wp:html -->
<main class="nlv2-showroom" data-nlv2-showroom data-nlv2-project-title="Ashira Sde Dov" data-nlv2-endpoint="<?php echo esc_url( rest_url( 'nadlan/v1/lead' ) ); ?>">
	<p class="nlv2-breadcrumb">NadLan / פרויקטים / Ashira Sde Dov</p>

	<section class="nlv2-hero" aria-labelledby="nlv2-ashira-title">
		<figure class="nlv2-hero-media">
			<img src="<?php echo esc_url( $asset_base . 'ashira-hero-concept.jpg' ); ?>" alt="הדמיית Ashira בשדה דב עם הים, תחנת רידינג ומגדלי הרובע">
			<figcaption class="nlv2-hero-badge">מודל תלת ממד ובחירת דירה</figcaption>
		</figure>
		<div>
			<span class="nlv2-eyebrow">פרויקט חדש ברובע שדה דב</span>
			<h1 id="nlv2-ashira-title">דירות למכירה באשירה שדה דב</h1>
			<p>בדקו דירות לפי קומה, שטח, נוף וכיוון. סובבו את המודל כדי להבין את הסביבה, ואז בחרו דירה על החזית כדי לראות אומדן לא מחייב, תוכנית, מבט ודרך לפנייה.</p>
			<div class="nlv2-hero-actions">
				<a class="nlv2-button nlv2-button-primary" href="#nlv2-ashira-selector">בחרו דירה</a>
				<a class="nlv2-button" href="#nlv2-ashira-info">קראו על הפרויקט</a>
			</div>
		</div>
	</section>

	<section class="nlv2-product" id="nlv2-ashira-selector" aria-labelledby="nlv2-ashira-product-title">
		<header class="nlv2-product-head">
			<div>
				<h2 id="nlv2-ashira-product-title">בחרו דירה לפי קומה, נוף וזמינות</h2>
				<p>המודל מציג את ההקשר של הים, השמש והרובע. בחירת הדירה נעשית בחזית הקבועה שלצדו, כדי לראות את מיקום הדירה בבניין בצורה ברורה.</p>
			</div>
			<div class="nlv2-legend" aria-label="מקרא זמינות">
				<span><i class="nlv2-dot" style="--nlv2-status:#34d986"></i> זמינה</span>
				<span><i class="nlv2-dot" style="--nlv2-status:#f2c14e"></i> בבדיקה</span>
				<span><i class="nlv2-dot" style="--nlv2-status:#9aa0a6"></i> לא זמינה</span>
			</div>
		</header>

		<div class="nlv2-stage">
			<section class="nlv2-model" aria-label="מודל תלת ממד של סביבת הפרויקט">
				<model-viewer
					src="<?php echo esc_url( $asset_base . 'model-context.glb' ); ?>"
					poster="<?php echo esc_url( $asset_base . 'ashira-hero-concept.jpg' ); ?>"
					camera-controls
					auto-rotate
					auto-rotate-delay="2200"
					rotation-per-second="8deg"
					reveal="auto"
					loading="auto"
					camera-orbit="35deg 64deg 68m"
					min-camera-orbit="-Infinity 54deg auto"
					max-camera-orbit="Infinity 74deg auto"
					shadow-intensity="0.9"
					interaction-prompt="none"
					ar-status="not-presenting">
				</model-viewer>
				<div class="nlv2-model-caption">
					<strong>מודל סביבתי</strong>
					סובבו את המודל כדי להבין את מיקום הבניין ביחס לים, לשמש, לרידינג ולמגדלים הסמוכים. בחירת הדירה מתבצעת בחזית הלחיצה שמימין.
				</div>
			</section>

			<section class="nlv2-picker" aria-label="בחירת דירה על חזית הפרויקט">
				<h3>בחרו דירה על החזית</h3>
				<p class="nlv2-picker-note">הנתונים הם המחשה עד לקבלת מלאי רשמי. כל תא מייצג דירה או טיפוס דירה במיקום יחסי על החזית.</p>
				<div class="nlv2-facade">
					<img src="<?php echo esc_url( $asset_base . 'ashira-facade-concept.jpg' ); ?>" alt="חזית Ashira עם תאי דירות לבחירה">
					<button class="nlv2-cell is-featured is-active" style="left:42%;top:38%;--nlv2-status:#34d986" data-nlv2-unit data-unit-id="ashira-18-west" data-status-color="#34d986" data-status="זמינה לפנייה" data-title="דירה 18 מערב | 5 חדרים" data-rooms="5" data-sqm="132 מ״ר" data-floor="18" data-view="ים ורידינג" data-price="אומדן לפי פנייה" data-note="דירה גבוהה לכיוון מערב עם דגש על נוף לים. הנתונים להמחשה עד קבלת תוכנית ומלאי מאושרים." aria-pressed="true">18W<small>ים</small></button>
					<button class="nlv2-cell" style="left:58%;top:48%;--nlv2-status:#34d986" data-nlv2-unit data-unit-id="ashira-14-city" data-status-color="#34d986" data-status="זמינה לפנייה" data-title="דירה 14 עיר | 4 חדרים" data-rooms="4" data-sqm="104 מ״ר" data-floor="14" data-view="רובע שדה דב" data-price="אומדן לפי פנייה" data-note="דירה משפחתית במרכז החזית. יש לאמת מלאי, מחיר ותוכנית מול היזם לפני כל החלטה.">14C<small>עיר</small></button>
					<button class="nlv2-cell is-featured" style="left:32%;top:58%;--nlv2-status:#f2c14e" data-nlv2-unit data-unit-id="ashira-10-corner" data-status-color="#f2c14e" data-status="בבדיקת זמינות" data-title="דירה 10 פינתית | 4 חדרים" data-rooms="4" data-sqm="118 מ״ר" data-floor="10" data-view="ים וחצר" data-price="אומדן לפי פנייה" data-note="דירה פינתית עם מרפסת לכיוון מערב. הזמינות אינה מחייבת עד אימות מול היזם.">10P<small>פינה</small></button>
					<button class="nlv2-cell" style="left:66%;top:65%;--nlv2-status:#9aa0a6" data-nlv2-unit data-unit-id="ashira-07-sold" data-status-color="#9aa0a6" data-status="לא זמינה" data-title="דירה 7 | 3 חדרים" data-rooms="3" data-sqm="82 מ״ר" data-floor="7" data-view="מרקם עירוני" data-price="לא מוצג" data-note="סימון דירה שאינה זמינה, כדי להראות לקונה את מצב המלאי על החזית.">7A<small>סגור</small></button>
					<button class="nlv2-cell" style="left:48%;top:77%;--nlv2-status:#34d986" data-nlv2-unit data-unit-id="ashira-04-garden" data-status-color="#34d986" data-status="זמינה לפנייה" data-title="דירת גן 4 | 3 חדרים" data-rooms="3" data-sqm="92 מ״ר" data-floor="4" data-view="גן פנימי" data-price="אומדן לפי פנייה" data-note="טיפוס נמוך יותר עם חיבור לגינה ולרחוב. הנתונים להמחשה בלבד.">4G<small>גן</small></button>
				</div>
			</section>
		</div>

		<div class="nlv2-selected">
			<article class="nlv2-card" data-nlv2-card aria-live="polite">
				<header class="nlv2-card-header">
					<div>
						<span class="nlv2-status" data-nlv2-status>זמינה לפנייה</span>
						<h3 data-nlv2-title>דירה 18 מערב | 5 חדרים</h3>
					</div>
					<button class="nlv2-dismiss" type="button" data-nlv2-dismiss aria-label="סגירת פרטי הדירה">סגור</button>
				</header>
				<div class="nlv2-facts">
					<div class="nlv2-fact">חדרים<strong data-nlv2-rooms>5</strong></div>
					<div class="nlv2-fact">שטח<strong data-nlv2-sqm>132 מ״ר</strong></div>
					<div class="nlv2-fact">קומה<strong data-nlv2-floor>18</strong></div>
					<div class="nlv2-fact">נוף<strong data-nlv2-view>ים ורידינג</strong></div>
				</div>
				<p class="nlv2-card-copy"><strong data-nlv2-price>אומדן לפי פנייה</strong></p>
				<p class="nlv2-card-copy" data-nlv2-note>דירה גבוהה לכיוון מערב עם דגש על נוף לים. הנתונים להמחשה עד קבלת תוכנית ומלאי מאושרים.</p>
				<div class="nlv2-tabs" role="tablist" aria-label="מידע על הדירה">
					<button class="is-active" type="button" data-nlv2-tab="plan" aria-selected="true">תוכנית</button>
					<button type="button" data-nlv2-tab="view" aria-selected="false">מבט</button>
					<button type="button" data-nlv2-tab="tour" aria-selected="false">סיור פנים</button>
					<button type="button" data-nlv2-tab="contact" aria-selected="false">שיחה</button>
				</div>
				<div class="nlv2-panel" data-nlv2-panel>כאן תוצג תוכנית הדירה לאחר העלאת תוכנית מכר מאושרת.</div>
			</article>

			<aside class="nlv2-contact" aria-label="פנייה לגבי הדירה">
				<h3>רוצים לבדוק את הדירה?</h3>
				<form class="nlv2-form" data-nlv2-form>
					<input type="hidden" name="selected_unit" data-nlv2-selected-unit value="ashira-18-west">
					<label>שם מלא<input name="name" type="text" autocomplete="name" required></label>
					<label>טלפון<input name="phone" type="tel" autocomplete="tel"></label>
					<label>אימייל<input name="email" type="email" autocomplete="email"></label>
					<label>מועד רלוונטי<input name="timeline" type="text" placeholder="חודש קרוב / בהמשך"></label>
					<button type="submit">שלחו פנייה עם הדירה שנבחרה</button>
					<p class="nlv2-feedback" data-nlv2-feedback hidden></p>
				</form>
			</aside>
		</div>
	</section>

	<section class="nlv2-section" id="nlv2-ashira-info" aria-label="מידע על Ashira Sde Dov">
		<h2>מה חשוב לבדוק לפני שבוחרים דירה באשירה שדה דב?</h2>
		<p>בחירת דירה בפרויקט חדש מתחילה בשאלה פשוטה: איפה הדירה נמצאת בתוך הבניין ומה רואים ממנה. לכן הדף מחבר בין מודל סביבתי, חזית דירות לחיצה ופרטי דירה שממשיכים לפנייה אחת ברורה.</p>
		<div class="nlv2-data-grid">
			<div class="nlv2-data-card"><span>אזור</span><strong>רובע שדה דב</strong></div>
			<div class="nlv2-data-card"><span>תצוגה</span><strong>מודל וחזית</strong></div>
			<div class="nlv2-data-card"><span>סטטוס נתונים</span><strong>המחשה</strong></div>
		</div>
		<h2>איך בודקים דירה בדף?</h2>
		<p>מסובבים את המודל כדי להבין את הסביבה, בוחרים תא דירה על החזית, מקבלים פרטי קומה, חדרים, שטח ונוף, ואז פותחים תוכנית, מבט מהדירה או סיור פנים כאשר היזם מעלה מדיה מאושרת.</p>
		<h2>מה צריך לאמת לפני החלטה?</h2>
		<p class="nlv2-note">המודל, החזית, המלאי והאומדנים בדף זה הם המחשה. לפני התקדמות יש לאמת תוכניות מכר, מחירים, זמינות ומדיה מול היזם.</p>
	</section>
</main>
<!-- /wp:html -->
