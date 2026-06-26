<?php
/**
 * Title: Ashira Sde Dov project showroom
 * Slug: nadlan-revenue/project-showroom-ashira-sde-dov
 * Categories: featured, media
 * Description: Project showroom pattern with 3D context model, fixed facade apartment picker, buyer content, and editable media slots.
 *
 * @package WordPress
 * @subpackage NadLan_Revenue
 * @since NadLan Revenue 1.1.0
 */

$asset_base = trailingslashit( get_template_directory_uri() ) . 'assets/projects/ashira-sde-dov/';
?>
<!-- wp:html -->
<main class="nlps-showroom-page nlps-showroom-ashira" data-nlps-showroom data-nlps-project-title="Ashira שדה דב" data-nlps-endpoint="<?php echo esc_url( rest_url( 'nadlan/v1/lead' ) ); ?>">
	<p class="nlps-breadcrumbs">NadLan / פרויקטים / Ashira שדה דב</p>

	<figure class="nlps-poster">
		<img src="<?php echo esc_url( $asset_base . 'poster-prototype.svg' ); ?>" alt="Ashira שדה דב בתל אביב - הדמיית פרויקט עם אפשרות תלת מימד ובחירת דירה">
		<figcaption><strong>Ashira שדה דב</strong><span>הדמיה מקורית להמחשה, לא חומר רשמי</span></figcaption>
	</figure>

	<section class="nlps-intro" aria-labelledby="nlps-ashira-title">
		<span class="nlps-eyebrow">פרויקט חדש ברובע שדה דב</span>
		<h1 id="nlps-ashira-title">דירות למכירה ב-Ashira שדה דב</h1>
		<p>Ashira שדה דב הוא פרויקט מגורים של אביסרור בצפון תל אביב, בסביבה שמחברת חוף, פארק, מסחר ותכנון עירוני חדש. כאן אפשר לראות מודל תלת ממדי להמחשה, לבחור דירה על חזית קבועה, לבדוק כיוון, קומה, שטח ואומדן מחיר, ואז לפנות עם הדירה שנבחרה.</p>
	</section>

	<section class="nlps-shell" aria-labelledby="nlps-ashira-showroom-title">
		<div class="nlps-head">
			<div>
				<h2 id="nlps-ashira-showroom-title">תצוגת דירות: מודל מסתובב לצד חזית בחירה</h2>
				<p>המודל משמש להבנת הסביבה: ים, שמש, מרחקים ובינוי סמוך. בחירת הדירה נעשית על חזית קבועה עם תאי דירות, כדי שהבחירה תהיה ברורה, נגישה ולא תלויה בזווית הסיבוב.</p>
			</div>
			<div class="nlps-legend" aria-label="מקרא זמינות">
				<span><i class="nlps-swatch is-available"></i> זמינה</span>
				<span><i class="nlps-swatch is-reserved"></i> בבדיקה</span>
				<span><i class="nlps-swatch is-sold"></i> לא זמינה</span>
			</div>
		</div>

		<div class="nlps-grid">
			<section class="nlps-stage" aria-label="מודל תלת ממדי של סביבת הפרויקט">
				<model-viewer
					src="<?php echo esc_url( $asset_base . 'model-prototype.glb' ); ?>"
					camera-controls
					auto-rotate
					auto-rotate-delay="2400"
					rotation-per-second="5deg"
					reveal="auto"
					loading="auto"
					min-camera-orbit="-Infinity 62deg 30m"
					max-camera-orbit="Infinity 62deg 54m"
					camera-target="-1m 16m 0m"
					camera-orbit="-34deg 62deg 34m"
					field-of-view="22deg"
					min-field-of-view="18deg"
					max-field-of-view="32deg"
					exposure="1.35"
					shadow-intensity="0.9"
					interaction-prompt="none"
					ar-status="not-presenting"
					style="background-image:url('<?php echo esc_url( $asset_base . 'model-context-prototype.svg' ); ?>');background-size:cover;background-position:center;background-repeat:no-repeat;background-color:#0a3433;">
				</model-viewer>
				<div class="nlps-stage-caption">
					<strong>מודל סביבה, לא בחירת דירה</strong>
					סובבו ימינה ושמאלה כדי להבין ים, שמש, פארק ומבנים סמוכים. הדירות נבחרות בחזית הקבועה שלצד המודל.
				</div>
			</section>

			<section class="nlps-facade" aria-label="בחירת דירה על חזית הפרויקט">
				<div class="nlps-facade-title">
					<div>
						<h3>בחרו דירה על החזית</h3>
						<p>כל תא מייצג דירה לדוגמה: קומה, כיוון, שטח, זמינות ואומדן מחיר. מלאי רשמי יחליף את נתוני ההמחשה.</p>
					</div>
					<span class="nlps-chip">המחשה</span>
				</div>
				<div class="nlps-facade-plane">
					<img src="<?php echo esc_url( $asset_base . 'facade-prototype.svg' ); ?>" alt="">
					<button class="nlps-unit-cell is-recommended is-active" style="left:29%;top:17.25%;width:9.6%;height:4.1%;" data-nlps-unit data-unit-id="ashira-18-04" data-building="מגדל" data-title="דירה 18-04 · קומה 18 · 4 חדרים" data-status="זמינה לפנייה" data-rooms="4" data-sqm="112 מ״ר" data-floor="18" data-view="מערב · נוף לים" data-note="אומדן לא מחייב: כ-5.32 מיליון ₪. קומה גבוהה בכיוון מערב, בכפוף לאימות רשמי של קו הראייה.">18-04</button>
					<button class="nlps-unit-cell" style="left:40.4%;top:17.25%;width:9.6%;height:4.1%;" data-nlps-unit data-unit-id="ashira-18-05" data-building="מגדל" data-title="דירה 18-05 · קומה 18 · 3 חדרים" data-status="זמינה לפנייה" data-rooms="3" data-sqm="98 מ״ר" data-floor="18" data-view="ים ורובע שדה דב" data-note="אומדן לא מחייב: כ-4.89 מיליון ₪. כיוון מערבי-צפוני משוער עד קבלת מלאי רשמי.">18-05</button>
					<button class="nlps-unit-cell is-reserved is-recommended" style="left:28.7%;top:34.5%;width:9.8%;height:4.2%;" data-nlps-unit data-unit-id="ashira-15-02" data-building="מגדל" data-title="דירה 15-02 · קומה 15 · 5 חדרים" data-status="בבדיקת זמינות" data-rooms="5" data-sqm="132 מ״ר" data-floor="15" data-view="ים · פארק · רובע" data-note="אומדן לא מחייב: כ-6.41 מיליון ₪. דירה משפחתית גדולה; יש לאמת מרפסת, כיוונים ומחסן.">15-02</button>
					<button class="nlps-unit-cell is-recommended" style="left:53%;top:43%;width:10%;height:4.3%;" data-nlps-unit data-unit-id="ashira-14-04" data-building="מגדל" data-title="דירה 14-04 · קומה 14 · 4 חדרים" data-status="זמינה לפנייה" data-rooms="4" data-sqm="118 מ״ר" data-floor="14" data-view="מערב · ים" data-note="אומדן לא מחייב: כ-5.58 מיליון ₪. דירת דוגמה שמדגימה בחירה מתוך החזית.">14-04</button>
					<button class="nlps-unit-cell" style="left:39.6%;top:55.75%;width:10.4%;height:4.5%;" data-nlps-unit data-unit-id="ashira-12-03" data-building="מגדל" data-title="דירה 12-03 · קומה 12 · 3 חדרים" data-status="זמינה לפנייה" data-rooms="3" data-sqm="87 מ״ר" data-floor="12" data-view="רובע שדה דב" data-note="אומדן לא מחייב: כ-4.21 מיליון ₪. כיוון עירוני משוער עד קבלת נתונים רשמיים.">12-03</button>
				</div>

				<article class="nlps-card" data-nlps-card aria-live="polite">
					<header>
						<div>
							<span class="nlps-chip" data-nlps-status>זמינה לפנייה</span>
							<h3 data-nlps-title>דירה 18-04 · קומה 18 · 4 חדרים</h3>
						</div>
						<button class="nlps-dismiss" type="button" data-nlps-dismiss aria-label="סגירת כרטיס הדירה">סגור</button>
					</header>
					<div class="nlps-facts">
						<div class="nlps-fact">חדרים<strong data-nlps-rooms>4</strong></div>
						<div class="nlps-fact">שטח<strong data-nlps-sqm>112 מ״ר</strong></div>
						<div class="nlps-fact">קומה<strong data-nlps-floor>18</strong></div>
						<div class="nlps-fact">נוף<strong data-nlps-view>מערב · נוף לים</strong></div>
					</div>
					<p data-nlps-note>אומדן לא מחייב: כ-5.32 מיליון ₪. קומה גבוהה בכיוון מערב, בכפוף לאימות רשמי של קו הראייה.</p>
					<div class="nlps-tabs" role="tablist" aria-label="מידע על הדירה">
						<button class="is-active" type="button" data-nlps-tab="plan">תוכנית</button>
						<button type="button" data-nlps-tab="tour">סיור פנים</button>
						<button type="button" data-nlps-tab="view">מבט מהדירה</button>
						<button class="nlps-cta" type="button" data-nlps-tab="contact">דברו איתנו</button>
					</div>
					<div class="nlps-media-panel" data-nlps-media-panel>כאן תופיע תוכנית הדירה הרשמית או המחשה מאושרת. זהו מקום שמור לתצוגה בסגנון Homes.com / Zillow.</div>
					<form class="nlps-lead-form" data-nlps-lead-form>
						<p class="nlps-form-title">רוצים להתקדם עם הדירה שנבחרה?</p>
						<div class="nlps-form-grid">
							<label>שם מלא<input name="name" type="text" autocomplete="name" required></label>
							<label>טלפון<input name="phone" type="tel" autocomplete="tel"></label>
							<label>אימייל<input name="email" type="email" autocomplete="email"></label>
							<label>מסגרת תקציב<input name="budget" type="text" inputmode="numeric" placeholder="לדוגמה 4.5-5.2 מיליון"></label>
							<label>מועד רלוונטי<input name="timeline" type="text" placeholder="חודש קרוב / בהמשך"></label>
							<label>עם מי תרצו לדבר?
								<select name="advisor">
									<option value="היזם">היזם</option>
									<option value="יועץ רכישה">יועץ רכישה</option>
									<option value="משכנתאות">משכנתאות</option>
									<option value="עו״ד נדל״ן">עו״ד נדל״ן</option>
								</select>
							</label>
						</div>
						<input class="nlps-hp" name="company" type="text" tabindex="-1" autocomplete="off" aria-hidden="true">
						<div class="nlps-lead-actions">
							<button class="nlps-primary" type="submit" data-nlps-intent="callback">דברו איתנו על הדירה</button>
							<button type="submit" data-nlps-intent="purchase">בדיקת רכישה לא מחייבת</button>
						</div>
						<p class="nlps-legal">הפנייה נשלחת עם פרטי הדירה שנבחרה. הנתונים בעמוד הם להמחשה עד אימות מול היזם.</p>
						<p class="nlps-ok" data-nlps-ok hidden></p>
					</form>
				</article>
			</section>
		</div>
	</section>

	<section class="nlps-content" aria-label="מידע על הפרויקט">
		<h2>מה בודקים לפני שבוחרים דירה ב-Ashira שדה דב?</h2>
		<p>בחירת דירה בפרויקט חדש מתחילה בשילוב בין קומה, כיוון, שטח, מרפסת, סביבת הבניין וקו ראייה. לכן התצוגה מחברת בין מודל סביבה מסתובב לבין חזית בחירה קבועה: המודל מסביר את ההקשר, והחזית מאפשרת לבחור דירה בפועל.</p>
		<div class="nlps-resource-grid" aria-label="חומרי פרויקט">
			<article class="nlps-resource-card">
				<span>01</span>
				<h3>וידאו יזם</h3>
				<p>מקום שמור לסרטון YouTube או Vimeo רשמי של היזם. הסרטון ייטען רק כאשר קיים קישור מאושר.</p>
			</article>
			<article class="nlps-resource-card">
				<span>02</span>
				<h3>גלריית הדמיות</h3>
				<p>מקום לתמונות חוץ, לובי, דירה לדוגמה וחללים משותפים, בלי להעמיס על פתיחת העמוד.</p>
			</article>
			<article class="nlps-resource-card">
				<span>03</span>
				<h3>סיור פנים</h3>
				<p>קישור עתידי לסיור בסגנון Matterport או Homes.com, כאשר יש חומר מאושר לכל דירה או טיפוס דירה.</p>
			</article>
		</div>

		<h2>סביבת שדה דב למשפחה ולמשקיע</h2>
		<p>רובע שדה דב מתוכנן כאזור חוף עירוני חדש בצפון תל אביב, עם שילוב של מגורים, שטחים ציבוריים, מסחר ותנועה עירונית. לקונה חשוב להבין לא רק את הדירה, אלא גם את מה שרואים מהקומה, איך השמש פוגעת בחזית ומה המרחק לשירותים יומיומיים.</p>
		<table class="nlps-table">
			<tbody>
				<tr><th>מערב</th><td>ים, טיילת וכיוון חוף</td></tr>
				<tr><th>דרום</th><td>פארק הירקון ונמל תל אביב</td></tr>
				<tr><th>מזרח</th><td>מרקם עירוני, מסחר ותנועה עתידית</td></tr>
				<tr><th>צפון</th><td>המשך רובע שדה דב וצפון תל אביב</td></tr>
			</tbody>
		</table>

		<h2>מה חסר כדי להפוך את ההמחשה לרשמית?</h2>
		<p class="nlps-note">נדרשים מודל BIM או GLB רשמי, תוכניות מאושרות, מלאי דירות, זמינות ומחירים מאושרים. עד אז, המודל והחזית הם המחשה שמראה את חוויית הבחירה העתידית ואינה מחליפה בדיקה מול היזם.</p>

		<h2>שפות וקהל בינלאומי</h2>
		<p>העמוד בנוי כך שאפשר לשכפל אותו לעמודים נפרדים בעברית, אנגלית, צרפתית, רוסית וערבית. לכל שפה נדרש מחקר ביטויים, כותרת, תיאור, FAQ ותוכן מקומי, כדי שהעמוד ידבר לקורא בשפה שלו בלי לערבב מסרים.</p>
		<div class="nlps-lang-row" aria-label="שפות מתוכננות">
			<span>עברית</span><span>English</span><span>Français</span><span>Русский</span><span>العربية</span>
		</div>
	</section>
</main>
<!-- /wp:html -->
