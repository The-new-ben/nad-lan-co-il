<?php
/**
 * Title: Dimri Yama project showroom
 * Slug: nadlan-revenue/project-showroom-dimri-yama
 * Categories: featured, media
 * Description: Prototype project showroom with 3D context model, facade apartment picker, selected-unit card, and buyer-facing content blocks.
 *
 * @package WordPress
 * @subpackage NadLan_Revenue
 * @since NadLan Revenue 1.1.0
 */

$asset_base = trailingslashit( get_template_directory_uri() ) . 'assets/projects/dimri-yama/';
?>
<!-- wp:html -->
<main class="nlps-showroom-page" data-nlps-showroom data-nlps-project-title="דמרי ימה" data-nlps-endpoint="<?php echo esc_url( rest_url( 'nadlan/v1/lead' ) ); ?>">
	<p class="nlps-breadcrumbs">נדל״ן חכם / פרויקטים / DIMRI YAMA</p>
	<figure class="nlps-poster">
		<img src="<?php echo esc_url( $asset_base . 'poster-prototype.webp' ); ?>" alt="דמרי ימה בשדה דב - הדמיה רעיונית עם מודל תלת ממד ובחירת דירה">
		<figcaption><strong>דמרי ימה · שדה דב</strong><span>הדמיה רעיונית להמחשה בלבד</span></figcaption>
	</figure>

	<section class="nlps-intro" aria-labelledby="nlps-dimri-title">
		<span class="nlps-eyebrow">פרויקט חדש ברובע שדה דב</span>
		<h2 id="nlps-dimri-title">דמרי ימה · בחירת דירה במודל פרויקט</h2>
		<p>דמרי ימה ממוקם בין חוף תל אביב לפארק הירקון, עם ארבעה מבנים ושכבת תצוגה שמאפשרת לבחור דירה, לבדוק כיוון ונוף, ולפנות עם פרטי הדירה שנבחרה.</p>
	</section>

	<section class="nlps-shell" aria-labelledby="nlps-dimri-showroom-title">
		<div class="nlps-head">
			<div>
				<h2 id="nlps-dimri-showroom-title">תצוגת דירות: מודל וסימון חזית</h2>
				<p>המודל מציג את ההקשר: ים, שמש, פארק ומבנים. בחירת הדירה נעשית על חזית קבועה, כדי שהדירה תהיה חלק מהבניין ולא סימון צף.</p>
			</div>
			<div class="nlps-legend" aria-label="מקרא זמינות">
				<span><i class="nlps-swatch is-available"></i> זמינה</span>
				<span><i class="nlps-swatch is-reserved"></i> בבדיקה</span>
				<span><i class="nlps-swatch is-sold"></i> לא זמינה</span>
			</div>
		</div>

		<div class="nlps-grid">
			<section class="nlps-stage" aria-label="מודל תלת ממד של סביבת הפרויקט">
				<model-viewer
					src="<?php echo esc_url( $asset_base . 'model-prototype.glb' ); ?>"
					poster="<?php echo esc_url( $asset_base . 'poster-prototype.webp' ); ?>"
					camera-controls
					auto-rotate
					auto-rotate-delay="1800"
					rotation-per-second="10deg"
					reveal="auto"
					loading="auto"
					min-camera-orbit="-Infinity 45deg auto"
					max-camera-orbit="Infinity 78deg auto"
					camera-orbit="35deg 62deg 70m"
					shadow-intensity="0.8"
					interaction-prompt="none"
					ar-status="not-presenting">
				</model-viewer>
				<div class="nlps-stage-caption">
					<strong>מודל הקשר, לא בחירת דירה</strong>
					סובבו את המודל כדי להבין ים, פארק, שמש ומיקום. הדירות נבחרות בחזית הקבועה לידו.
				</div>
			</section>

			<section class="nlps-facade" aria-label="בחירת דירה על חזית הפרויקט">
				<div class="nlps-facade-title">
					<div>
						<h3>בחרו דירה על החזית</h3>
						<p>הנתונים כאן הם דוגמה בלבד עד קבלת מלאי רשמי מהיזם.</p>
					</div>
					<span class="nlps-chip">אב־טיפוס</span>
				</div>
				<div class="nlps-facade-plane">
					<img src="<?php echo esc_url( $asset_base . 'facade-prototype.svg' ); ?>" alt="">
					<button class="nlps-unit-cell is-recommended is-active" style="left:20.2%;top:53%;" data-nlps-unit data-unit-id="a-08-03" data-building="A" data-title="A-8 · קומה 8 · 3 חדרים" data-status="זמינה לפנייה" data-rooms="3" data-sqm="82 מ״ר" data-floor="8" data-view="כיוון ים" data-note="דירת דוגמה עם כיוון מערבי. אומדן לא מחייב עד קבלת מקור מאושר.">A-8</button>
					<button class="nlps-unit-cell is-recommended is-reserved" style="left:46%;top:34.5%;" data-nlps-unit data-unit-id="b-15-05" data-building="B" data-title="B-15 · קומה 15 · 5 חדרים" data-status="בבדיקת זמינות" data-rooms="5" data-sqm="132 מ״ר" data-floor="15" data-view="ים ורובע שדה דב" data-note="דירה משפחתית גדולה באגף גבוה. יש להחליף במלאי רשמי.">B-15</button>
					<button class="nlps-unit-cell is-reserved" style="left:69.8%;top:64%;" data-nlps-unit data-unit-id="c-06-04" data-building="C" data-title="C-6 · קומה 6 · 4 חדרים" data-status="שמורה לבדיקה" data-rooms="4" data-sqm="104 מ״ר" data-floor="6" data-view="חצר וכיוון ים" data-note="סימון המחשה. לא מלאי רשמי ולא הבטחת זמינות.">C-6</button>
					<button class="nlps-unit-cell" style="left:86.5%;top:76%;" data-nlps-unit data-unit-id="d-04-studio" data-building="D" data-title="D-4 · קומה 4 · סטודיו" data-status="זמינה לפנייה" data-rooms="סטודיו" data-sqm="42 מ״ר" data-floor="4" data-view="מרקם עירוני" data-note="דירת סטודיו לדוגמה לפי קטגוריות ציבוריות. נדרש אישור יזם.">D-4</button>
				</div>

				<article class="nlps-card" data-nlps-card aria-live="polite">
					<header>
						<div>
							<span class="nlps-chip" data-nlps-status>זמינה לפנייה</span>
							<h3 data-nlps-title>A-8 · קומה 8 · 3 חדרים</h3>
						</div>
						<button class="nlps-dismiss" type="button" data-nlps-dismiss aria-label="סגירת כרטיס הדירה">×</button>
					</header>
					<div class="nlps-facts">
						<div class="nlps-fact">חדרים<strong data-nlps-rooms>3</strong></div>
						<div class="nlps-fact">שטח<strong data-nlps-sqm>82 מ״ר</strong></div>
						<div class="nlps-fact">קומה<strong data-nlps-floor>8</strong></div>
						<div class="nlps-fact">נוף<strong data-nlps-view>כיוון ים</strong></div>
					</div>
					<p data-nlps-note>אומדן לא מחייב. יש להחליף במחיר ומלאי מאושרים לפני פרסום מסחרי.</p>
					<div class="nlps-tabs" role="tablist" aria-label="מידע על הדירה">
						<button class="is-active" type="button" data-nlps-tab="plan">תכנית</button>
						<button type="button" data-nlps-tab="tour">סיור פנים</button>
						<button type="button" data-nlps-tab="view">מבט מהדירה</button>
						<button class="nlps-cta" type="button" data-nlps-tab="contact">דברו איתנו</button>
					</div>
					<div class="nlps-media-panel" data-nlps-media-panel>תכנית הדירה תופיע כאן לאחר העלאת חומר מאושר. בינתיים זהו מקום שמור לתצוגה בסגנון Homes.com / Zillow.</div>
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
									<option value="יזם">היזם</option>
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
		<h2>מה בודקים לפני שבוחרים דירה בדמרי ימה?</h2>
		<p>בדיקה טובה מתחילה במיקום הדירה בתוך הבניין, כיוון האוויר, המרפסת, המבט לים או לפארק, והמרחק מהחלקים הציבוריים של המתחם. לכן תצוגת הדירות צריכה לחבר בין מודל הפרויקט לבין חזית בחירה ברורה.</p>
		<h2>מי עומד מאחורי הפרויקט?</h2>
		<p>לפי מקורות הפרויקט, דמרי ימה משויך לקבוצת דמרי, עם תכנון אדריכלי של רני זיס אדריכלים ועיצוב פנים מאת Kelly Hoppen CBE. יש לאמת כל פרט מסחרי מול היזם לפני קבלת החלטה.</p>
		<h2>מה חסר כדי להפוך את האב־טיפוס לרשמי?</h2>
		<p class="nlps-note">נדרשים מודל BIM או GLB רשמי, תכניות מאושרות, מלאי דירות, זמינות ומחירים מאושרים. עד אז, המודל והחזית הם המחשה שמראה את חוויית הבחירה העתידית.</p>
	</section>
</main>
<!-- /wp:html -->
