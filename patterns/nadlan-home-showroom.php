<?php
/**
 * Title: NadLan home showroom
 * Slug: nadlan-revenue/nadlan-home-showroom
 * Categories: featured, media
 * Description: Buyer-first homepage opening with search, multi-project showroom, multilingual entry points and trust cards.
 *
 * @package WordPress
 * @subpackage NadLan_Revenue
 * @since NadLan Revenue 1.1.0
 */

$theme_uri   = trailingslashit( get_template_directory_uri() );
$projects_js = $theme_uri . 'assets/engine/projects.json';
?>
<!-- wp:html -->
<div class="nle-page nlh-home" data-nle-home-showroom data-nle-projects="<?php echo esc_url( $projects_js ); ?>" data-nle-asset-base="<?php echo esc_url( $theme_uri ); ?>">
	<main class="nlh-home-main">
		<section class="nlh-home-hero" aria-labelledby="nlh-home-title">
			<div class="nlh-home-panel">
				<span class="nlh-home-eyebrow" data-nle-home-text="hero_eyebrow">נדל״ן בישראל, פרויקטים ודירות חדשות</span>
				<h1 id="nlh-home-title" data-nle-home-text="hero_title">בודקים פרויקט, דירה וסביבה לפני שמתקדמים.</h1>
				<p class="nlh-home-lead" data-nle-home-text="hero_lead">השוו פרויקטים חדשים, בדקו זמינות לפי קומה ונוף, ראו אומדן לא מחייב וקבלו תמונה ברורה יותר לפני שיחה עם נציג. מתאים לקונים בישראל וגם למשקיעים מחו״ל שרוצים להבין את המקום, המחיר והמסמכים לפני החלטה.</p>
				<form class="nlh-search-row nlh-home-inline-search">
					<div class="nlh-search-field">
						<label for="nlh-area" data-nle-home-text="area_label">אזור</label>
						<input id="nlh-area" type="search" value="שדה דב, תל אביב" aria-label="אזור לחיפוש" data-nle-home-value="area_value" data-nle-home-aria="area_aria">
					</div>
					<div class="nlh-search-field">
						<label for="nlh-type" data-nle-home-text="type_label">מה מחפשים</label>
						<select id="nlh-type" aria-label="סוג חיפוש" data-nle-home-aria="type_aria">
							<option data-nle-home-text="type_new">דירות חדשות</option>
							<option data-nle-home-text="type_investment">דירות להשקעה</option>
							<option data-nle-home-text="type_sea">דירות ליד הים</option>
						</select>
					</div>
					<button type="button" data-nle-home-text="hero_search_button">בדקו עכשיו</button>
				</form>
				<div class="nlh-home-actions">
					<a class="nlh-home-button is-primary" href="#projects" data-nle-home-text="hero_projects_button">השוו פרויקטים</a>
					<a class="nlh-home-button" href="#showroom" data-nle-home-text="hero_showroom_button">בחרו דירה לדוגמה</a>
				</div>
			</div>
		</section>

		<section class="nle-catalog nlh-home-project-engine" id="projects" aria-labelledby="nle-projects-title">
			<div class="nlh-home-languages" aria-label="שפות למשקיעים מחו״ל">
				<strong class="nlh-lang-quiet" data-nle-home-text="language_prompt">שפה</strong>
				<button class="is-active" type="button" data-nle-lang="he" lang="he" dir="rtl">עברית</button>
				<button type="button" data-nle-lang="en" lang="en" dir="ltr">English</button>
				<button type="button" data-nle-lang="fr" lang="fr" dir="ltr">Français</button>
				<button type="button" data-nle-lang="ru" lang="ru" dir="ltr">Русский</button>
				<button type="button" data-nle-lang="ar" lang="ar" dir="rtl">العربية</button>
			</div>
			<div class="nle-catalog-head">
				<div>
					<span class="nlh-home-section-kicker" data-nle-home-text="catalog_kicker">בחירת פרויקט</span>
					<h2 id="nle-projects-title" data-nle-home-text="catalog_title">השוואת פרויקטים חדשים לפי דירה, נוף ואומדן</h2>
					<p data-nle-home-text="catalog_lead">בחרו פרויקט בשדה דב, עברו לתצוגת הדירות, ואז בדקו קומה, כיוון, שטח, נוף ואומדן מחיר לא מחייב לפני פנייה.</p>
					<p class="nle-note" data-nle-project-count>טוען פרויקטים</p>
				</div>
				<div class="nlh-project-tools">
					<label class="nlh-project-search">
						<span data-nle-home-text="project_search_label">חיפוש פרויקט</span>
						<input class="nle-search" type="search" placeholder="שם פרויקט או אזור" data-nle-search>
					</label>
					<div class="nlh-project-language-rail" aria-label="שפה למידע על פרויקטים">
						<a class="is-active" href="/projects/ashira-sde-dov/" data-nle-lang="he" lang="he" dir="rtl">עברית</a>
						<a href="/projects/ashira-sde-dov-en/" data-nle-lang="en" lang="en" dir="ltr">English</a>
						<a href="/projects/ashira-sde-dov-fr/" data-nle-lang="fr" lang="fr" dir="ltr">Français</a>
						<a href="/projects/ashira-sde-dov-ru/" data-nle-lang="ru" lang="ru" dir="ltr">Русский</a>
						<a href="/projects/ashira-sde-dov-ar/" data-nle-lang="ar" lang="ar" dir="rtl">العربية</a>
					</div>
				</div>
			</div>
			<div class="nle-project-grid" data-nle-project-grid></div>
			<p class="nlh-catalog-note" data-nle-home-text="catalog_note">בכל פרויקט מוצגים דגם תלת ממדי, בחירת דירות, אומדן מחיר לא מחייב, סביבת מגורים ודרך קצרה לפנייה על הדירה שנבחרה.</p>
		</section>

		<section class="nle-showroom" id="showroom" aria-label="בחירת דירה בפרויקט">
			<div class="nle-model">
				<div class="nle-model-head">
					<div>
						<span class="nle-badge" data-nle-project-location>רובע שדה דב</span>
						<h2 data-nle-project-title>טוען פרויקט</h2>
						<p data-nle-project-sub>טוען תיאור פרויקט</p>
					</div>
					<span class="nle-badge" data-nle-home-text="model_badge">סובבו מודל ובחרו דירה</span>
				</div>
				<div data-nle-model-wrap></div>
			</div>

			<aside class="nle-side" id="buyers">
				<article class="nle-unit-card" aria-live="polite">
					<header>
						<div>
							<span class="nle-status" data-nle-unit-status>זמינה</span>
							<h3 data-nle-unit-title>בחרו דירה</h3>
						</div>
						<div class="nle-stat"><span data-nle-label="floor">קומה</span><strong data-nle-unit-floor>--</strong></div>
					</header>
					<div class="nle-facts">
						<div class="nle-fact"><span data-nle-label="rooms">חדרים</span><strong data-nle-unit-rooms>--</strong></div>
						<div class="nle-fact"><span data-nle-label="area">שטח</span><strong data-nle-unit-sqm>--</strong></div>
						<div class="nle-fact"><span data-nle-label="view">נוף</span><strong data-nle-unit-view>--</strong></div>
						<div class="nle-fact"><span data-nle-label="estimate">אומדן</span><strong data-nle-unit-price>לפי פנייה</strong></div>
					</div>
					<div class="nle-tabs" role="tablist" aria-label="מידע על הדירה">
						<button class="is-active" type="button" data-nle-tab="plan" data-nle-label="plan">תוכנית</button>
						<button type="button" data-nle-tab="view" data-nle-label="unit_view">מבט</button>
						<button type="button" data-nle-tab="tour" data-nle-label="tour">סיור</button>
					</div>
					<div class="nle-panel" data-nle-panel>בחרו דירה כדי לראות מידע.</div>
					<p class="nle-note" data-nle-model-note></p>
				</article>

				<section class="nle-facade" aria-label="בחירת דירה מהירה">
					<strong data-nle-label="quick_pick">בחירת דירה מהירה</strong>
					<p class="nle-note" data-nle-label="quick_pick_note">בחרו קומה או דירה כדי לראות שטח, חדרים, נוף, אומדן ותוכנית לפני פנייה.</p>
					<div class="nle-facade-grid" data-nle-facade-grid></div>
				</section>

				<form class="nle-contact" data-nle-form>
					<strong data-nle-label="contact_title">רוצים לבדוק את הדירה?</strong>
					<input name="name" placeholder="שם מלא" autocomplete="name" data-nle-placeholder="name">
					<input name="phone" placeholder="טלפון" inputmode="tel" autocomplete="tel" data-nle-placeholder="phone">
					<input type="hidden" name="unit" data-nle-selected-unit>
					<button type="submit" data-nle-label="contact_button">שליחת פנייה על הדירה</button>
					<p class="nle-note" data-nle-label="contact_note">הפנייה תישלח עם פרטי הדירה שנבחרה. הנתונים להמחשה ויש לאמת מחיר וזמינות מול היזם.</p>
					<p class="nle-note" data-nle-feedback></p>
				</form>
			</aside>
		</section>

		<section class="nlh-home-trust" aria-label="מה בודקים לפני בחירה">
			<article>
				<span>זמינות</span>
				<strong>דירה לפי קומה ונוף</strong>
				<p>הבחירה מתחילה במיקום הדירה, לא רק בשם הפרויקט.</p>
			</article>
			<article>
				<span>מחיר</span>
				<strong>אומדן לא מחייב</strong>
				<p>המחיר מוצג בזהירות עד אימות מסמכים ומלאי מול היזם.</p>
			</article>
			<article>
				<span>סביבה</span>
				<strong>ים, תחבורה ושכונה</strong>
				<p>בודקים את החיים סביב הפרויקט לפני שמבקשים שיחה.</p>
			</article>
			<article>
				<span>שפות</span>
				<strong>עברית ושפות למשקיעים</strong>
				<p>המסלול הרב לשוני ייבנה כעמודים נפרדים עם קישורים הדדיים.</p>
			</article>
		</section>

		<section class="nlh-home-paths" aria-labelledby="nlh-home-paths-title">
			<div class="nlh-section-head">
				<span>לפני שמחליטים</span>
				<h2 id="nlh-home-paths-title">מה כדאי לבדוק בכל פרויקט חדש</h2>
				<p>העמוד נותן לקונים דרך קצרה להשוות פרויקטים, להבין את הדירה, ולראות אילו שאלות כדאי לשאול לפני פנייה.</p>
			</div>
			<div class="nlh-path-grid">
				<article>
					<span>01</span>
					<strong>זמינות ומיקום הדירה</strong>
					<p>בדקו באיזו קומה נמצאת הדירה, מה הכיוון שלה, האם הנוף פתוח, ואילו דירות דומות עדיין מוצגות בפרויקט.</p>
				</article>
				<article>
					<span>02</span>
					<strong>אומדן מחיר ועלויות נוספות</strong>
					<p>השוו אומדן לא מחייב, תנאי תשלום, מס רכישה, הצמדה למדד, חניה, מחסן ועלויות נלוות לפני קבלת החלטה.</p>
				</article>
				<article>
					<span>03</span>
					<strong>סביבה, תחבורה ושירותים</strong>
					<p>בדקו קרבה לים, פארקים, תחבורה ציבורית, בתי ספר, גני ילדים, מרכזים מסחריים ותוכניות עתידיות באזור.</p>
				</article>
				<article>
					<span>04</span>
					<strong>מסמכים לפני חתימה</strong>
					<p>לפני התחייבות, חשוב לבדוק מפרט, תוכנית מכר, לוח תשלומים, ערבויות, מועדי מסירה וזכויות בנייה.</p>
				</article>
			</div>
		</section>

		<section class="nlh-home-international" aria-labelledby="nlh-areas-title">
			<div class="nlh-section-head">
				<span>לפי אזור</span>
				<h2 id="nlh-areas-title">אזורי הביקוש</h2>
				<p>בחרו אזור כדי לראות פרויקטים, מחירים ועסקאות אחרונות באזור.</p>
			</div>
			<div class="nlh-language-grid">
				<a class="nlh-language-card" href="/sde-dov/">
					<span>אזור</span>
					<strong>רובע שדה דב</strong>
					<p>תל אביב, קו הים. הפרויקטים החדשים ביותר באזור.</p>
				</a>
				<a class="nlh-language-card" href="/ramat-aviv/">
					<span>אזור</span>
					<strong>רמת אביב</strong>
					<p>שכונה ותיקה ומבוססת בצפון תל אביב.</p>
				</a>
				<a class="nlh-language-card" href="/north-tel-aviv/">
					<span>אזור</span>
					<strong>צפון תל אביב</strong>
					<p>קרבה לים, פארק הירקון והעיר.</p>
				</a>
				<a class="nlh-language-card" href="/herzliya-pituach-apartment-prices/">
					<span>אזור</span>
					<strong>הרצליה פיתוח</strong>
					<p>קרבה לים ולמרינה, מגורי יוקרה.</p>
				</a>
			</div>
		</section>

		<section class="nlh-home-international" aria-labelledby="nlh-international-title">
			<div class="nlh-section-head">
				<span>נדל״ן בישראל</span>
				<h2 id="nlh-international-title">כל מה שצריך כדי לקנות דירה נכון</h2>
				<p>פרויקטים חדשים, מחשבוני עלות, מדריכי רכישה ואנשי מקצוע מאומתים, במקום אחד.</p>
			</div>
			<div class="nlh-language-grid">
				<a class="nlh-language-card" href="/projects/">
					<span>פרויקטים</span>
					<strong>פרויקטים חדשים ובחירת דירה</strong>
					<p>השוו פרויקטים, בדקו קומה, כיוון ונוף, וראו אומדן מחיר לא מחייב לפני פנייה.</p>
				</a>
				<a class="nlh-language-card" href="/mortgage-calculator/">
					<span>כלים</span>
					<strong>מחשבוני עלות לפני חתימה</strong>
					<p>משכנתא, מס רכישה ועלויות עסקה, כדי לדעת מה באמת צריך לפני התקדמות.</p>
				</a>
				<a class="nlh-language-card" href="/buying-apartment/">
					<span>מדריכים</span>
					<strong>מה לבדוק לפני שקונים</strong>
					<p>מדריכי רכישה, מסמכים, זכויות בנייה ובדיקות חשובות לפני חוזה.</p>
				</a>
				<a class="nlh-language-card" href="/professionals/">
					<span>אנשי מקצוע</span>
					<strong>בעלי מקצוע מאומתים</strong>
					<p>עורכי דין, שמאים ומפקחי בנייה לנדל״ן, לבדיקה בטוחה של העסקה.</p>
				</a>
			</div>
		</section>
	</main>
</div>
<!-- /wp:html -->
