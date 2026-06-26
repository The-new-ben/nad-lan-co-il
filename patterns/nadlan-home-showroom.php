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
				<span class="nlh-home-eyebrow">נדל״ן בישראל, פרויקטים ודירות חדשות</span>
				<h1 id="nlh-home-title">בודקים פרויקט, דירה וסביבה לפני שמתקדמים.</h1>
				<p class="nlh-home-lead">השוו פרויקטים חדשים, בדקו זמינות לפי קומה ונוף, ראו אומדן לא מחייב וקבלו תמונה ברורה יותר לפני שיחה עם נציג. מתאים לקונים בישראל וגם למשקיעים מחו״ל שרוצים להבין את המקום, המחיר והמסמכים לפני החלטה.</p>
				<form class="nlh-search-row nlh-home-inline-search">
					<div class="nlh-search-field">
						<label for="nlh-area">אזור</label>
						<input id="nlh-area" type="search" value="שדה דב, תל אביב" aria-label="אזור לחיפוש">
					</div>
					<div class="nlh-search-field">
						<label for="nlh-type">מה מחפשים</label>
						<select id="nlh-type" aria-label="סוג חיפוש">
							<option>דירות חדשות</option>
							<option>דירות להשקעה</option>
							<option>דירות ליד הים</option>
						</select>
					</div>
					<button type="button">בדקו עכשיו</button>
				</form>
				<div class="nlh-home-actions">
					<a class="nlh-home-button is-primary" href="#projects">השוו פרויקטים</a>
					<a class="nlh-home-button" href="#showroom">בחרו דירה לדוגמה</a>
				</div>
			</div>
		</section>

		<section class="nle-catalog" id="projects" aria-labelledby="nle-projects-title">
			<div class="nle-catalog-head">
				<div>
					<h2 id="nle-projects-title">פרויקטים שאפשר לבדוק עכשיו</h2>
					<p>בחרו פרויקט, עברו לדגם התלת ממדי, ואז בדקו דירה לפי קומה, נוף, שטח ואומדן מחיר. זה אזור הבחירה המרכזי של דף הבית, מיד אחרי פתיחת העמוד.</p>
					<p class="nle-note" data-nle-project-count>טוען פרויקטים</p>
				</div>
				<input class="nle-search" type="search" placeholder="חיפוש לפי פרויקט או אזור" data-nle-search>
			</div>
			<div class="nle-project-grid" data-nle-project-grid></div>
		</section>

		<section class="nlh-home-languages" aria-label="שפות למשקיעים מחו״ל">
			<strong>מידע לרוכשים מחו״ל, בשפה שמתאימה להם</strong>
			<span class="is-active">עברית</span>
			<a href="#english">English</a>
			<a href="#french">Français</a>
			<a href="#russian">Русский</a>
			<a href="#arabic">العربية</a>
		</section>

		<section class="nle-showroom" id="showroom" aria-label="בחירת דירה בפרויקט">
			<div class="nle-model">
				<div class="nle-model-head">
					<div>
						<span class="nle-badge" data-nle-project-location>רובע שדה דב</span>
						<h2 data-nle-project-title>טוען פרויקט</h2>
						<p data-nle-project-sub>טוען תיאור פרויקט</p>
					</div>
					<span class="nle-badge">סובבו מודל ובחרו דירה</span>
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
						<div class="nle-stat"><span>קומה</span><strong data-nle-unit-floor>--</strong></div>
					</header>
					<div class="nle-facts">
						<div class="nle-fact"><span>חדרים</span><strong data-nle-unit-rooms>--</strong></div>
						<div class="nle-fact"><span>שטח</span><strong data-nle-unit-sqm>--</strong></div>
						<div class="nle-fact"><span>נוף</span><strong data-nle-unit-view>--</strong></div>
						<div class="nle-fact"><span>אומדן</span><strong data-nle-unit-price>לפי פנייה</strong></div>
					</div>
					<div class="nle-tabs" role="tablist" aria-label="מידע על הדירה">
						<button class="is-active" type="button" data-nle-tab="plan">תוכנית</button>
						<button type="button" data-nle-tab="view">מבט</button>
						<button type="button" data-nle-tab="tour">סיור</button>
					</div>
					<div class="nle-panel" data-nle-panel>בחרו דירה כדי לראות מידע.</div>
					<p class="nle-note" data-nle-model-note></p>
				</article>

				<section class="nle-facade" aria-label="בחירת דירה מהירה">
					<strong>בחירת דירה מהירה</strong>
					<p class="nle-note">בחרו קומה או דירה כדי לראות שטח, חדרים, נוף, אומדן ותוכנית לפני פנייה.</p>
					<div class="nle-facade-grid" data-nle-facade-grid></div>
				</section>

				<form class="nle-contact" data-nle-form>
					<strong>רוצים לבדוק את הדירה?</strong>
					<input name="name" placeholder="שם מלא" autocomplete="name">
					<input name="phone" placeholder="טלפון" inputmode="tel" autocomplete="tel">
					<input type="hidden" name="unit" data-nle-selected-unit>
					<button type="submit">שליחת פנייה על הדירה</button>
					<p class="nle-note">הפנייה תישלח עם פרטי הדירה שנבחרה. הנתונים להמחשה ויש לאמת מחיר וזמינות מול היזם.</p>
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

		<section class="nlh-home-international" aria-labelledby="nlh-international-title">
			<div class="nlh-section-head">
				<span>רוכשים מחו״ל</span>
				<h2 id="nlh-international-title">מידע ברור גם באנגלית, צרפתית, רוסית וערבית</h2>
				<p>כל שפה תקבל בהמשך עמוד מלא משלה. בשלב הזה הכניסה הרב לשונית מציגה את ההבטחה לקונה בשפה שהוא מבין.</p>
			</div>
			<div class="nlh-language-grid">
				<article class="nlh-language-card" id="english" lang="en" dir="ltr">
					<span>English</span>
					<strong>Compare new projects in Israel before you call.</strong>
					<p>Check the location, apartment level, view, estimated price and next documents to review before speaking with a representative.</p>
				</article>
				<article class="nlh-language-card" id="french" lang="fr" dir="ltr">
					<span>Français</span>
					<strong>Comparer un projet avant de demander des détails.</strong>
					<p>Emplacement, étage, vue, estimation de prix et documents à vérifier sont réunis dans un parcours clair.</p>
				</article>
				<article class="nlh-language-card" id="russian" lang="ru" dir="ltr">
					<span>Русский</span>
					<strong>Сравните проект до первого звонка.</strong>
					<p>Расположение, этаж, вид, ориентир цены и документы собраны в одном понятном пути для покупателя.</p>
				</article>
				<article class="nlh-language-card" id="arabic" lang="ar" dir="rtl">
					<span>العربية</span>
					<strong>قارنوا المشروع قبل التواصل.</strong>
					<p>الموقع، الطابق، الإطلالة، تقدير السعر والمستندات الأساسية تظهر في مسار واضح قبل اتخاذ قرار.</p>
				</article>
			</div>
		</section>
	</main>
</div>
<!-- /wp:html -->
