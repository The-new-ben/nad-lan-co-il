<?php
/**
 * Front page template.
 */
get_header();
?>
<main id="main" class="site-main">
    <section class="hero">
        <div class="container hero-grid">
            <div>
                <p class="eyebrow">נדל״ן, משכנתאות ומיסוי בלי לנחש</p>
                <h1>הדרך החכמה לקבל החלטה לפני שקונים, מוכרים או משקיעים בנדל״ן</h1>
                <p class="hero-copy">מחשבונים, מדריכים ובדיקת התאמה ראשונית שמחברים בין כוונת החיפוש שלך לבין אנשי מקצוע, מימון ובדיקות שיכולים לחסוך כסף אמיתי.</p>
                <div class="hero-actions">
                    <a class="button" href="#lead">בדיקת התאמה בחינם</a>
                    <a class="button secondary" href="#tools">למחשבוני נדל״ן</a>
                </div>
                <div class="metrics" aria-label="מדדי אמון">
                    <div class="metric"><strong>מס רכישה</strong><span>להתחיל מהמספרים</span></div>
                    <div class="metric"><strong>משכנתא</strong><span>לבדוק יכולת לפני חתימה</span></div>
                    <div class="metric"><strong>עורך דין</strong><span>לצמצם סיכון בעסקה</span></div>
                </div>
            </div>
            <aside id="lead" class="lead-card" aria-label="טופס ליד נדלן">
                <h2>מה המהלך הנדל״ני שלך?</h2>
                <p>נשמור את הפנייה במערכת ונחזור עם ניתוב ראשוני לפי הצורך.</p>
                <?php if (isset($_GET['lead']) && $_GET['lead'] === 'received') : ?>
                    <p class="notice">הפנייה התקבלה. נחזור אליך בהקדם.</p>
                <?php endif; ?>
                <form class="form-grid" method="post" action="<?php echo esc_url(admin_url('admin-post.php')); ?>">
                    <input type="hidden" name="action" value="nadlan_lead">
                    <?php wp_nonce_field('nadlan_lead', 'nadlan_nonce'); ?>
                    <div class="field"><label for="lead_name">שם מלא</label><input id="lead_name" name="lead_name" autocomplete="name" required></div>
                    <div class="field"><label for="lead_phone">טלפון</label><input id="lead_phone" name="lead_phone" autocomplete="tel" required></div>
                    <div class="field"><label for="lead_email">אימייל</label><input id="lead_email" name="lead_email" type="email" autocomplete="email"></div>
                    <div class="field"><label for="lead_goal">מה צריך?</label><select id="lead_goal" name="lead_goal"><option>קניית דירה</option><option>מכירת דירה</option><option>השקעה</option><option>משכנתא</option><option>מס רכישה</option><option>בדיקה משפטית</option></select></div>
                    <div class="field"><label for="lead_city">אזור / עיר</label><input id="lead_city" name="lead_city" placeholder="לדוגמה: תל אביב, חיפה, באר שבע"></div>
                    <div class="field"><label for="lead_budget">תקציב משוער</label><input id="lead_budget" name="lead_budget" placeholder="לדוגמה: 2,000,000 ש״ח"></div>
                    <div class="field"><label for="lead_timeline">מתי זה רלוונטי?</label><select id="lead_timeline" name="lead_timeline"><option>מיידי</option><option>בחודש הקרוב</option><option>3 חודשים</option><option>רק בודק/ת כרגע</option></select></div>
                    <div class="field"><label for="lead_message">פרטים נוספים</label><textarea id="lead_message" name="lead_message"></textarea></div>
                    <button class="button" type="submit">שליחת בדיקה</button>
                    <p class="notice">אין לראות במידע ייעוץ משפטי, מיסויי או פיננסי. הפנייה מיועדת לבדיקה ראשונית בלבד.</p>
                </form>
            </aside>
        </div>
    </section>

    <section id="tools" class="section tools-band">
        <div class="container">
            <div class="section-head">
                <h2>כלים שמביאים לידים עם כוונת קנייה</h2>
                <p>מחשבונים וכלי החלטה הם נקודת הכניסה לתנועה מסחרית: המשתמש כבר קרוב לעסקה וצריך תשובה.</p>
            </div>
            <div class="cards">
                <article class="card"><h3>מחשבון מס רכישה</h3><p>עמוד יעד ראשון: חישוב מהיר, הסבר מדרגות, ואז ניתוב לעורך דין/יועץ מס.</p><a href="/purchase-tax-calculator/">לתכנון העמוד</a></article>
                <article class="card"><h3>בדיקת יכולת משכנתא</h3><p>טופס מובנה שמייצר ליד ליועץ משכנתאות ומדריך למימון נכון.</p><a href="/mortgage-check/">לתכנון העמוד</a></article>
                <article class="card"><h3>צ׳קליסט קניית דירה</h3><p>נכס להורדה שמייצר אימיילים ומסווג משתמשים לפי שלב בעסקה.</p><a href="/buying-checklist/">לתכנון העמוד</a></article>
            </div>
        </div>
    </section>

    <section class="section">
        <div class="container">
            <div class="section-head">
                <h2>מסלולי כסף ראשונים</h2>
                <p>העמודים הראשונים צריכים להתחרות על מילים קשות אבל רווחיות, עם מבנה שממיר.</p>
            </div>
            <div class="cards">
                <article class="card"><h3>קניית דירה</h3><p>מדריכים, בדיקות, עורך דין, מיסוי ומשכנתא.</p><a href="/buying-apartment/">לראות מבנה</a></article>
                <article class="card"><h3>דירה להשקעה</h3><p>אזורים, תשואה, סיכונים, מס וניתוב לשיחה.</p><a href="/investment-apartment/">לראות מבנה</a></article>
                <article class="card"><h3>עורך דין מקרקעין</h3><p>עמוד שירות מסחרי עם טופס סינון לידים.</p><a href="/real-estate-lawyer/">לראות מבנה</a></article>
            </div>
        </div>
    </section>
</main>
<?php
get_footer();
