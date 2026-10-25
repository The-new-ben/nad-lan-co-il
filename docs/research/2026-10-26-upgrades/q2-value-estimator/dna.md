# Q2 · /property-value-estimator/ · page DNA and build spec

Research date: 25.10.2026 (SERPs pulled 19:22 to 19:23 UTC). Research only: nothing on the live site was changed, no Linear or Notion item was created.
No earlier research folder exists for this page; the tool's own data notes are in `docs/research/2026-10-07-city-prices/README.md` (the official price files behind the calculator) and were re-checked today.

Evidence classes: **SERP** (DataForSEO Google organic live advanced, Israel 2376, Hebrew, depth 20, raw JSON saved), **raw** (HTML as Google gets it, no scripts run, saved), **WebFetch** (pages that block plain fetch or render by script, read through WebFetch: yadata, dirobot, hoomy; madlan answered 403 and was not read), **API** (official data queried directly, saved), **GSC** (Search Console API, 25.7 to 23.10.2026), **code** (our repo), **unverified** (kept out of the spec).

Raw evidence (private, not in the repo):
- SERP JSON: `C:\Users\777\nad-lan\_private-research\2026-10-26-upgrades\serp\q2_*.json` and digest `q2_summary.txt`
- Competitor HTML: `C:\Users\777\nad-lan\_private-research\2026-10-26-upgrades\raw\q2\` (yadata redirected to a bot check, `yadata.html` is that challenge page, not content; we did not try to pass it)
- Official data: `C:\Users\777\nad-lan\_private-research\2026-10-26-upgrades\data\` (`settlement_5000.json`, `settlement_2660.json`, `neighborhood_buy_65210724.json`, `cbs_*.json`, `ckan_shamaim_*.json`, `gsc_query_page_90d.csv`)
- Baseline proof: `proof-before.md` in this folder.

---

## 1. Intents and keyword set

GSC, 90 days, this page: 4,102 impressions, 20 clicks, 235 queries (the page is the site's clear owner of the topic).

| # | Intent | Owned head term (GSC impr@pos) | Synonyms and long tail |
|---|---|---|---|
| 1 | Get a value for my apartment now, free, online | הערכת שווי דירה (461@20.6) | הערכת שווי נכס 450@20.5 · הערכת שווי 304@29.8 · בדיקת שווי נכס 167@19.6 · הערכת שווי דירה בחינם 140@24.7 · הערכת שווי נכסים 109@26.4 · הערכת נכס 89@22 · הערכת מחיר דירה 86@20 · הערכת שווי נכס באינטרנט 86@22 · הערכת נכס באינטרנט 82@19 · בדיקת שווי דירה 72@18 · הערכת שווי נכס חינם 3@23 |
| 2 | "How much is my place worth" (plain question form) | כמה שווה הדירה שלי (172@23.9) | כמה שווה הבית שלי 101@27 · כמה הדירה שלי שווה 21@25 · כמה שווה הדירה 9@22 · האם הדירה שלי שווה יותר 11@20 · כמה שווה הנכס שלי 3@22 |
| 3 | Seller: set the right asking price | איך יודעים מה מחיר השיווק הנכון לדירה? (131@24.6 + 116@20.3 in two spellings) | הערכת שווי דירה למכירה 91@15.9 · איך קובעים מחיר לנכס 40@20 · מחיר שיווק לנכס 21@18 · איך לתמחר דירה למכירה 9@17 · מחיר נכון למכירת דירה 9@22 · חישוב ערך דירה למכירה 9@11 |
| 4 | Calculator wording | מחשבון שווי דירה (title today) | מחשבון דירה 44@23 · מחשבון נדלן 42@22 · מחשבון מחיר דירה 15@15 · מחשבון הערכת שווי דירה 9@17 · מחשבון שמאות דירה 10@14 · מחשבון שווי דירה רשות המיסים 7@41 · מחיר דירה לפי כתובת 6@19 |
| 5 | Appraiser and life events | הערכת שמאי לדירה (55@33) | שמאות לדירה יד שניה 38@29 · הערכת שווי דירה למשכנתא 36@24 · כמה עולה שמאות לדירה 18@37 (and five spellings) · הערכת שווי דירה בירושה למכירה 15@32 · מחשבון הערכת שווי בגירושין 8@26 · הערכת שווי בית פרטי 49@17 · הערכת שווי נכס לפני קניה 39@20 · ירידת ערך נכס 26@44 |
| local | City and neighbourhood | | הערכת מחיר דירה בבת ים בחינם 81@20 · הערכת שווי דירה נווה אביבים 42@16 (+10) · כמה שווה הדירה שלי רמת אביב ג׳ 10@20 · רמת אביב הירוקה 7+4 · **יבנה: five queries, 44 impressions (the tool has no Yavne data today)** |

Where we stand in the live SERP (desktop unless noted): #15 for "הערכת שווי נכס" (title shown "מחשבון שווי דירה - נדלן"); not in the top 20 for "הערכת שווי דירה" (desktop and phone), "הערכת שווי", "כמה שווה הדירה שלי", "בדיקת שווי נכס", "הערכת שווי דירה בחינם", "איך יודעים מה מחיר השיווק הנכון לדירה?".

### Cannibalization (GSC + `url_word_audit.py`)
- `--token estimator`: `/property-value-estimator/` plus its `/ru/` and `/fr/` versions (language twins, not rivals).
- `--token value`: also `/property-value/` (the guide), `/property-value/luxury-apartments-tel-aviv/`, `/property-value/building-rights-check/`, two glossary pages. `--token valuation`: none.
- GSC: the estimator owns every head query. Small overlaps: `/property-value/` on "הערכת שווי נכס לפני קניה" (34@42 vs 39@20 for the estimator) and "איך קובעים מחיר לנכס" (2@75); `/investment/`, `/buy-or-rent/`, `/apartment-purchase-cost-calculator/` pick up "מחשבון נדלן / מחשבון דירה" at positions 58 to 99 (noise).
- **Ownership decision (no new URL, no redirect, no noindex):** the estimator owns intents 1 to 5. The guide `/property-value/` stays the long read and links to the estimator with the anchor "הערכת שווי דירה"; the estimator links to the guide as "מדריך הערכת שווי" (already there).

---

## 2. SERP snapshot

Union of what Google shows across the nine Q2 SERPs:
- **AI overview: present in all nine.** It answers with a list of free tools and the official deal data, and ends with "when you need an appraiser". Tools named, in this order almost every time: yadata (Yad2), the government real estate site (nadlan.gov.il, Tax Authority deals), Hoomy, Dirobot, Levi Itzhak price list, Madlan, AppraiseIt (30 ₪). For "הערכת שווי דירה בחינם" it adds the **govmap "מחשבון שווי נכס"** (settlement, neighbourhood, rooms, build year, area, floor). It quotes an appraisal cost "סביב 2,500 ש"ח" (unverified, from a private price list). For "הערכת שווי נכס" it lists the value factors: area, rooms, floor, elevator, air directions, condition, parking, storage, balcony, garden or roof, location, and planning or legal status including renewal plans.
- **People also ask (union, 24 questions; only some are on topic):** איך אני יכול לדעת כמה שווה הדירה שלי? · איך מחשבים שווי של דירה לפי כתובת? · מהי הערכת שווי דירה מבוססת AI? · האם יש מחשבון שווי דירה של מדלן? · איך אני יכול למצוא מידע על דירות שנמכרו? · איך מעריכים שווי נכס יד 2? · מהי התשואה הממוצעת על דירה בישראל? · מה מחיר השכירות? · מהו מחשבון השכירות של דירה? · איפה הכי זול לקנות דירה בישראל? · מהן הבדיקות שיש לבצע לפני קניית דירה? · and off-topic finance (DCF, NPV, business valuation, where to invest 50,000 ₪) for the bare "הערכת שווי".
- **Related / people also search (union):** הערכת שווי דירה מדלן · הערכת שווי דירה בחינם · הערכת שווי דירה יד 2 · מחשבון הערכת שווי דירה · מחיר דירה לפי כתובת · שווי דירה לפי קומה · מחשבון עליית ערך דירה · חישוב ערך דירה למכירה · הערכת שווי בית פרטי · הערכת שווי נכס מסחרי · הערכת שווי מגרש · הערכת שווי דירה להשכרה · מחירון נדלן · כמה שווה הדירה שלי רשות המיסים · מחשבון שכר דירה · מחשבון לקנות או לשכור דירה.
- **What Google wants to show:** a tool that gives a number for an address or a neighbourhood without friction, grounded in Tax Authority deals, plus a short "when to use an appraiser" and "what moves the value". Brand tools win; thin lead forms with an exact title (Landsman, Idan Tao, E&Y) also win on title match alone. No competitor in the top 20 shows the method, the source date and the formula together (our page shows the source and quarter, not yet the formula).

### Top 10 per query (raw: serp/q2_*.json; long dashes in quoted titles normalised to ·)

#### "הערכת שווי דירה" (desktop), retrieved 2026-10-25 19:22 UTC

| # | domain | title | url |
|---|---|---|---|
| 1 | idantao.co.il | הערכת מחיר דירה · הערכת שווי דירה מקצועית ומדויקת ... | https://idantao.co.il/הערכת-מחיר-דירה/ |
| 2 | www.ey-group.co.il | הערכת שווי דירה - כמה עולה שמאי | https://www.ey-group.co.il/הערכת-שווי-דירה/ |
| 3 | www.wecheck.co.il | מחשבון מדד שכר דירה - מבוסס בינה מלאכותית- WeCheck blog | https://www.wecheck.co.il/blog/מחשבון-מדד-שכר-דירה/ |
| 4 | www.habita.com | הערכת מחיר הנכס | https://www.habita.com/il/valuation |
| 5 | www.broker-re.co.il | חישוב שווי דירה - איך תדעו כמה הדירה שלכם באמת שווה? המדריך המלא | https://www.broker-re.co.il/workbooks/חישוב-שווי-דירה-איך-תדעו-כמה-הדירה-שלכ/ |
| 6 | bh-pk.co.il | איך להעריך שווי נכס לפני מכירה? | https://bh-pk.co.il/הערכת-שווי-נכס-לפני-מכירה/ |
| 7 | shovi-dira.com | שווי דירה - כמה שווה הדירה שלי? · מחירון דירות מדויק 2025 | https://shovi-dira.com/ |
| 8 | jackireg.com | כמה שווה הדירה שלכם? הערכת שווי בירושלים | https://jackireg.com/blog/home-valuation-service |
| 9 | www.ey-group.co.il | הערכת שווי שוק של דירה - E&Y | https://www.ey-group.co.il/הערכת-שווי-שוק-של-דירה/ |
| 10 | jackireg.com | כמה שווה הדירה שלכם? הערכת שווי בירושלים | https://jackireg.com/blog/home-valuation-service |

- nad-lan.co.il in this SERP: not in top 20
- People also ask: absent
- Related searches: מחשבון שכירות דירה · הערכת שווי דירה בחינם · הערכת שווי דירה מדלן · מחשבון מדד שכר דירה · מחשבון מדד שכר דירה הלשכה המרכזית לסטטיסטיקה · מחשבון שכירות יד 2 · מחשבון שכר דירה 2026 · מחירון שכירות דירות · מחשבון שכר דירה מדלן
- AI overview: present. Gist: כדי לקבל הערכת מחיר מדויקת לדירה בישראל, ניתן להיעזר במחשבונים אינטרנטיים מובילים המבוססים על עסקאות אמת, או בבדיקה ישירה במאגרים הרשמיים: ידאטה yadata מבית יד2 : מחשבון שווי נכס המציע אומדן מבוסס על מאגר הנתונים הגדול של יד2, כולל מגמות ביקוש והיצע בשוק. אתר הנדל"ן הממשלתי : מאגר רשמי של רשות המיסים המציג נתוני עסקאות אמת שבוצעו בפועל לפי כתובת, שכונה או רחוב. Hoomy : פלטפורמה להערכת שווי דירה אונליין המבוססת על נתו…
- AI overview sources: https://yadata.yad2.co.il/property-valuation · https://yadata.yad2.co.il/ · https://www.nadlan.gov.il/ · https://www.hoomy.co.il/estimation · https://www.dirobot.co.il/calculator · https://www.dirobot.co.il/ · https://levi-itzhak.co.il/realestate/ · https://www.madlan.co.il/propertyevaluation/

#### "הערכת שווי דירה" (mobile), retrieved 2026-10-25 19:22 UTC

| # | domain | title | url |
|---|---|---|---|
| 1 | www.ey-group.co.il | מחשבון הערכת שווי דירה | https://www.ey-group.co.il/מחשבון-הערכת-שווי-דירה-2/ |
| 2 | www.ey-group.co.il | הערכת שווי דירה - כמה עולה שמאי | https://www.ey-group.co.il/הערכת-שווי-דירה/ |
| 3 | bh-pk.co.il | איך להעריך שווי נכס לפני מכירה? | https://bh-pk.co.il/הערכת-שווי-נכס-לפני-מכירה/ |
| 4 | www.propio.co.il | מחשבון שווי דירה · הערכת שווי חינם תוך דקה - Propio | https://www.propio.co.il/valuation |
| 5 | www.habita.com | הערכת מחיר הנכס | https://www.habita.com/il/valuation |
| 6 | www.broker-re.co.il | חישוב שווי דירה - איך תדעו כמה הדירה שלכם באמת שווה? המדריך המלא | https://www.broker-re.co.il/workbooks/חישוב-שווי-דירה-איך-תדעו-כמה-הדירה-שלכ/ |
| 7 | www.ey-group.co.il | הערכת שווי נכס - E&Y שמאות מקרקעין I דוחות אפס | https://www.ey-group.co.il/הערכת-שווי-נכס/ |
| 8 | www.wecheck.co.il | מחשבון מדד שכר דירה - מבוסס בינה מלאכותית- WeCheck blog | https://www.wecheck.co.il/blog/מחשבון-מדד-שכר-דירה/ |
| 9 | www.midrag.co.il | הערכת שווי נכס - מחירון שמאי מקרקעין | https://www.midrag.co.il/Content/SubSectorPriceList/277 |
| 10 | www.ilnadlan.co.il | הערכת שווי נכס | https://www.ilnadlan.co.il/houseprice/ |

- nad-lan.co.il in this SERP: not in top 20
- People also ask: איפה הכי זול לקנות דירה בישראל? · מה מחיר השכירות? · מהי התשואה הממוצעת על דירה בישראל? · מהי הערכת שווי דירה מבוססת AI? · האם יש מחשבון שווי דירה של מדלן? · איך מחשבים שווי של דירה לפי כתובת? · מהו מחשבון השכירות של דירה? · איך אני יכול למצוא מידע על דירות שנמכרו? · איך מעריכים שווי נכס יד 2?
- Related searches: absent
- AI overview: present. Gist: כדי לקבל הערכת מחיר מדויקת לדירה בישראל, ניתן להיעזר במחשבונים אינטרנטיים מובילים המבוססים על עסקאות אמת, או בבדיקה ישירה במאגרים הרשמיים: ידאטה yadata מבית יד2 : מחשבון שווי נכס המציע אומדן מבוסס על מאגר הנתונים הגדול של יד2, כולל מגמות ביקוש והיצע בשוק. אתר הנדל"ן הממשלתי : מאגר רשמי של רשות המיסים המציג נתוני עסקאות אמת שבוצעו בפועל לפי כתובת, שכונה או רחוב. Hoomy : פלטפורמה להערכת שווי דירה אונליין המבוססת על נתו…
- AI overview sources: https://yadata.yad2.co.il/property-valuation · https://yadata.yad2.co.il/ · https://www.nadlan.gov.il/ · https://www.hoomy.co.il/estimation · https://www.dirobot.co.il/calculator · https://www.dirobot.co.il/ · https://levi-itzhak.co.il/realestate/ · https://www.madlan.co.il/propertyevaluation/

#### "הערכת שווי נכס" (desktop), retrieved 2026-10-25 19:22 UTC

| # | domain | title | url |
|---|---|---|---|
| 1 | www.wecheck.co.il | כמה שווה הדירה שלי? - מידע מקיף עם הצעות | https://www.wecheck.co.il/blog/כמה-שווה-הדירה-שלי/ |
| 2 | yasmint-law.com | כמה שווה הדירה שלי? מדריך להערכת שווי דירה | https://yasmint-law.com/appreciation-tax/כמה-שווה-הדירה-שלי/ |
| 3 | www.landsman.co | הערכת שווי נכס - Landsman | https://www.landsman.co/הערכת-שווי-נכס/ |
| 4 | www.govmap.gov.il | מחשבון שווי נכס | https://www.govmap.gov.il/sites/property_value.html |
| 5 | www.ey-group.co.il | הערכת שווי דירה - כמה עולה שמאי | https://www.ey-group.co.il/הערכת-שווי-דירה/ |
| 6 | www.ey-group.co.il | מחשבון הערכת שווי דירה | https://www.ey-group.co.il/מחשבון-הערכת-שווי-דירה-2/ |
| 7 | appraise.co.il | הערכת שווי דירה או נכס: כמה שווה הבית שלכם? מדריך · Appraise | https://appraise.co.il/apartment-valuation/ |
| 8 | www.ilnadlan.co.il | הערכת שווי נכס | https://www.ilnadlan.co.il/houseprice/ |
| 9 | afikil.co.il | איך שמאי מעריך דירה, מה המחיר ואיך מחשבים הערכת שווי דירה יד 2 | https://afikil.co.il/real-estate-appraisal/howappraiserworks/ |
| 10 | www.midrag.co.il | מחיר הערכת שווי נכס לדירה | https://www.midrag.co.il/Content/PriceList/264872 |

- nad-lan.co.il in this SERP: #15
- People also ask: absent
- Related searches: הערכת שווי דירה מדלן · הערכת שווי דירה בחינם · הערכת שווי נדלן · מחשבון לקנות או לשכור דירה · יד 2 מחשבון דירה · שווי דירה לפי קומה · הערכת שווי מגרש · מחשבון שכר דירה
- AI overview: present. Gist: הערכת שווי נכס בישראל מתבצעת כיום באמצעות כלים דיגיטליים מהירים לאומדן ראשוני, או על ידי שמאי מקרקעין מוסמך לקבלת שומה מחייבת (למשל לצורך משכנתאות או הליכים משפטיים). Yadata מבית יד2 : מציע מחשבון שווי נכס המבוסס על מאגר הנתונים הגדול של יד2, כולל מגמות ביקוש והיצע בשוק. מחירון לוי יצחק : מחשבון נדל"ן המביא בחשבון פרמטרים פרטניים כמו קומה, מעלית, חניה, כיווני אוויר וקרבה למוקדי עניין. דירובוט : מחשבון המבוסס על עסקאו…
- AI overview sources: https://www.dirobot.co.il/calculator · https://ecvalue.co.il/הערכות-שווי/ · https://yadata.yad2.co.il/property-valuation · https://yadata.yad2.co.il/ · https://levi-itzhak.co.il/realestate/ · https://www.dirobot.co.il/ · https://www.madlan.co.il/propertyevaluation/ · https://www.hoomy.co.il/estimation · https://moranatiasre.com/הערכת-שווי/

#### "הערכת שווי נכס" (mobile), retrieved 2026-10-25 19:23 UTC

| # | domain | title | url |
|---|---|---|---|
| 1 | www.wecheck.co.il | כמה שווה הדירה שלי? - מידע מקיף עם הצעות | https://www.wecheck.co.il/blog/כמה-שווה-הדירה-שלי/ |
| 2 | yasmint-law.com | כמה שווה הדירה שלי? מדריך להערכת שווי דירה | https://yasmint-law.com/appreciation-tax/כמה-שווה-הדירה-שלי/ |
| 3 | bh-pk.co.il | איך להעריך שווי נכס לפני מכירה? | https://bh-pk.co.il/הערכת-שווי-נכס-לפני-מכירה/ |
| 4 | www.govmap.gov.il | מחשבון שווי נכס | https://www.govmap.gov.il/sites/property_value.html |
| 5 | www.ey-group.co.il | הערכת שווי דירה - כמה עולה שמאי | https://www.ey-group.co.il/הערכת-שווי-דירה/ |
| 6 | www.appraiseit.co.il | כמה שווה הדירה שלי? בדיקה מיידית לפי כתובת · AppraiseIt - הערכת שווי ד | https://www.appraiseit.co.il/כמה-שווה-הדירה-שלי/ |
| 7 | appraise.co.il | הערכת שווי דירה או נכס: כמה שווה הבית שלכם? מדריך · Appraise | https://appraise.co.il/apartment-valuation/ |
| 8 | www.propio.co.il | מחשבון שווי דירה · הערכת שווי חינם תוך דקה - Propio | https://www.propio.co.il/valuation |
| 9 | afikil.co.il | איך שמאי מעריך דירה, מה המחיר ואיך מחשבים הערכת שווי דירה יד 2 | https://afikil.co.il/real-estate-appraisal/howappraiserworks/ |
| 10 | yadata.yad2.co.il | ידאטה · יד2 - כל המידע על שוק הנדל״ן בישראל | https://yadata.yad2.co.il/ |

- nad-lan.co.il in this SERP: not in top 20
- People also ask: איפה הכי זול לקנות דירה בישראל? · מהי שיטת השווי הנכסי? · מהי הערכת שווי DCF? · מהי הערכת שווי עסקים? · מהי נוסחת היוון תזרים מזומנים?
- Related searches: absent
- AI overview: present. Gist: הערכת שווי נכס בישראל מתבצעת כיום באמצעות כלים דיגיטליים מהירים לאומדן ראשוני, או על ידי שמאי מקרקעין מוסמך לקבלת שומה מחייבת (למשל לצורך משכנתאות או הליכים משפטיים). Yadata מבית יד2 : מציע מחשבון שווי נכס המבוסס על מאגר הנתונים הגדול של יד2, כולל מגמות ביקוש והיצע בשוק. מחירון לוי יצחק : מחשבון נדל"ן המביא בחשבון פרמטרים פרטניים כמו קומה, מעלית, חניה, כיווני אוויר וקרבה למוקדי עניין. דירובוט : מחשבון המבוסס על עסקאו…
- AI overview sources: https://www.dirobot.co.il/calculator · https://ecvalue.co.il/הערכות-שווי/ · https://yadata.yad2.co.il/property-valuation · https://yadata.yad2.co.il/ · https://levi-itzhak.co.il/realestate/ · https://www.dirobot.co.il/ · https://www.madlan.co.il/propertyevaluation/ · https://www.hoomy.co.il/estimation · https://moranatiasre.com/הערכת-שווי/

#### "הערכת שווי" (desktop), retrieved 2026-10-25 19:23 UTC

| # | domain | title | url |
|---|---|---|---|
| 1 | he.wikipedia.org | הערכת שווי | https://he.wikipedia.org/wiki/הערכת_שווי |
| 2 | yadata.yad2.co.il | מחשבון הנדל"ן yadata מבית יד2 · חישוב הערך לנכס שלך‏ | https://yadata.yad2.co.il/property-valuation |
| 3 | www.dirobot.co.il | מחשבון הערכת שווי נכסים | https://www.dirobot.co.il/calculator |
| 4 | www.madlan.co.il | הערכת שווי נכסים | https://www.madlan.co.il/propertyevaluation/ |
| 5 | harel-vered.co.il | הערכת שווי נכס · שמאי מקרקעין עו"ד הראל ורד · מחיר שוק מדויק | https://harel-vered.co.il/תחומי-התמחות-המשרד/property-valuation-process-principles-and-accuracy… |
| 6 | www.e-s-l.co.il | הערכות שווי · shirit - א.ש.ל יעוץ כלכלי עסקי | https://www.e-s-l.co.il/value |
| 7 | www.barlev-nadlan.co.il | הערכת שווי דירה בתל אביב · איך מעריכים שווי דירה למכירה בתל אביב | https://www.barlev-nadlan.co.il/מידע-מקיף/איך-מעריכים-שווי-דירה/ |
| 8 | yaron-neheman.co.il | הערכות שווי | https://yaron-neheman.co.il/הערכות-שווי-2/ |
| 9 | www.hoomy.co.il | Hoomy · הערכת שווי דירה חינם בכמה קליקים | https://www.hoomy.co.il/estimation |
| 10 | www.shovi.co.il | הערכת שווי נכסים · יניב רפאל - שמאי מקרקעין מעל 15 שנות ניסיון | https://www.shovi.co.il/הערכת-שווי-נכסים/ |

- nad-lan.co.il in this SERP: not in top 20
- People also ask: מהי הערכת שווי דירה מבוססת AI? · מהי הערכת שווי עסקים? · איך מחשבים שווי של דירה לפי כתובת? · מהי הערכת שווי DCF? · מהי שיטת השווי הנכסי? · מהי נוסחת היוון תזרים מזומנים? · מהי הנוסחה של NPV? · מהי הנוסחה לחישוב ריבית? · מהו ערך נוכחי?
- Related searches: הערכת שווי דירה בחינם · הערכת שווי דירה מדלן · הערכת שווי דירה יד 2 · מחשבון הערכת שווי דירה · הערכת שווי נכס · הערכת שווי בית פרטי · הערכת שווי יד 2 · הערכת שווי דירה להשכרה
- AI overview: present. Gist: הערכת שווי היא תהליך מקצועי לקביעת השווי הכלכלי של עסק, חברה, נייר ערך או נכס (כמו נדל"ן או נכסים לא מוחשיים) בנקודת זמן מסוימת. עסקים וחברות: לצורך מיזוגים ורכישות (M&A), גיוס הון, סכסוכי בעלי מניות, גירושין, דוחות פיננסיים ומס. נדל"ן ונכסים: קביעת שווי הוגן של דירה או נכס מקרקעין לצורך קנייה, מכירה או משכנתא. שיטת היוון תזרים המזומנים (DCF - Discounted Cash Flow): שיטה נפוצה המבוססת על תחזית רווחים ותזרימי מזומנים…
- AI overview sources: https://he.wikipedia.org/wiki/הערכת_שווי · https://www.ifrsconsulting.co.il/הערכת-שווי-מהי/ · https://actuar-ec.co.il/business-valuation/ · https://levi-itzhak.co.il/realestate/ · https://psagot.org/הערכת-שווי-דירה-המדריך-להערכת-שווי-דיר/ · https://www.dt-law.co.il/page.asp?PageID=656 · https://yadata.yad2.co.il/property-valuation · https://www.dirobot.co.il/calculator · https://www.madlan.co.il/propertyevaluation/

#### "כמה שווה הדירה שלי" (desktop), retrieved 2026-10-25 19:23 UTC

| # | domain | title | url |
|---|---|---|---|
| 1 | www.mumangroup.co.il | כמה שווה הדירה שלי? | https://www.mumangroup.co.il/magazine/כמה-שווה-הדירה-שלי/ |
| 2 | levhasharon-nadlan.co.il | הערכת שווי נכס - כמה באמת שווה הנכס שלכם | https://levhasharon-nadlan.co.il/הערכת-שווי-נכס/ |
| 3 | www.appraiseit.co.il | מחשבון דירות AppraiseIT · הערכת שווי דירה - רק ב 30 ש"ח | https://www.appraiseit.co.il/ |
| 4 | amitalgroup.com | הערכת שווי הדירה שלי לפני מכירה · שימוש באתר מדלן | https://amitalgroup.com/הערכת-שווי-הדירה-שלי-לפני-מכירה-שימו/ |
| 5 | harel-vered.co.il | כמה שווה הדירה שלי? הערכת שווי נכס על ידי שמאי | https://harel-vered.co.il/uncategorized/apartment-valuation-israel-guide/ |
| 6 | www.wecheck.co.il | מחשבון מדד שכר דירה - מבוסס בינה מלאכותית- WeCheck blog | https://www.wecheck.co.il/blog/מחשבון-מדד-שכר-דירה/ |
| 7 | azarovs.com | כיצד לקבוע את שווי הדירה | https://azarovs.com/iw/blog/how-to-determine-the-value-of-an-apartment |
| 8 | www.madlan.co.il | אזור - מידע ומחירי דירות שנמכרו בעיר | https://www.madlan.co.il/area-info/אזור-ישראל |
| 9 | www.meter.my | הערכת שווי דירה · מטר | https://www.meter.my/valuation |
| 10 | value.danandlan.co.il | מחשבון דירות באשקלון · כמה שווה הדירה שלי? - בדיקת שווי נכס | https://value.danandlan.co.il/check |

- nad-lan.co.il in this SERP: not in top 20
- People also ask: absent
- Related searches: כמה שווה הדירה שלי מדלן · כמה שווה הדירה שלי רשות המיסים · כמה עולה שכירות דירה · מחשבון שכר דירה הום · כמה עולה לקנות דירה · שווי דירה לפי קומה · סימולטור שכר דירה · הלמ ס שכר דירה
- AI overview: present. Gist: כדי לדעת כמה שווה הדירה שלך, אפשר להשתמש במחשבוני נדל"ן אינטרנטיים שמתבססים על עסקאות אמיתיות ומאגרים רשמיים, או להזמין שמאי מקרקעין. מחשבון הנדל"ן yadata מבית יד2 : מציע נתוני עסקאות, מגמות מחירים ומצב שוק (שוק קונים או מוכרים). הערכת שווי נכסים - מדלן : בודק מחירים לפי עסקאות ומודעות באותה הסביבה. Hoomy : פלטפורמה להערכת שווי מבוססת על נתונים ממשלתיים (רשות המיסים ומשרד המשפטים) ללא עלות. דירובוט : מחשבון שווי נכסי…
- AI overview sources: https://levi-itzhak.co.il/realestate/ · https://yasmint-law.com/appreciation-tax/כמה-שווה-הדירה-שלי/ · https://www.hoomy.co.il/estimation · https://yadata.yad2.co.il/property-valuation · https://yadata.yad2.co.il/ · https://www.madlan.co.il/propertyevaluation/ · https://www.dirobot.co.il/ · https://www.appraiseit.co.il/כמה-שווה-הדירה-שלי/

#### "בדיקת שווי נכס" (desktop), retrieved 2026-10-25 19:23 UTC

| # | domain | title | url |
|---|---|---|---|
| 1 | www.broker-re.co.il | חישוב שווי דירה - איך תדעו כמה הדירה שלכם באמת שווה? המדריך המלא | https://www.broker-re.co.il/workbooks/חישוב-שווי-דירה-איך-תדעו-כמה-הדירה-שלכ/ |
| 2 | www.landsman.co | הערכת שווי נכס - Landsman | https://www.landsman.co/הערכת-שווי-נכס/ |
| 3 | yasmint-law.com | כמה שווה הדירה שלי? מדריך להערכת שווי דירה | https://yasmint-law.com/appreciation-tax/כמה-שווה-הדירה-שלי/ |
| 4 | a-leaders.co.il | בדיקת שווי נכס - לידרס נדלן - Leaders נדל"ן | https://a-leaders.co.il/property-value/ |
| 5 | aharoninadlan.co.il | שאלון שווי שוק נכס חינם | https://aharoninadlan.co.il/שאלון-שווי-שוק-נכס/ |
| 6 | nofarmor.co.il | כמה שווה הדירה שלי? כך בודקים שווי דירה ומה חשוב לדעת | https://nofarmor.co.il/כמה-שווה-הדירה-שלי/ |
| 7 | levhasharon-nadlan.co.il | הערכת שווי נכס - כמה באמת שווה הנכס שלכם | https://levhasharon-nadlan.co.il/הערכת-שווי-נכס/ |
| 8 | www.midrag.co.il | מחיר הערכת שווי נכס לדירה יד שנייה | https://www.midrag.co.il/Content/PriceList/559019 |
| 9 | www.habita.com | הערכת מחיר הנכס | https://www.habita.com/il/valuation |
| 10 | www.gov.il | מידע על נכס · רשות מקרקעי ישראל | https://www.gov.il/he/service/property-information |

- nad-lan.co.il in this SERP: not in top 20
- People also ask: absent
- Related searches: הערכת שווי דירה מדלן · הערכת שווי דירה בחינם · מחשבון לקנות או לשכור דירה · מחירון נדלן · בדיקת מחירי שכירות דירות · מחיר דירה · לנדסמן נדלן · כמה עולה לשכור דירה
- AI overview: present. Gist: כדי לדעת כמה שווה הנכס שלכם, תוכלו להשתמש במחשבוני נדל "ן חינמיים המבוססים על עסקאות אמת ומאגרי מידע ממשלתיים, או לבדוק עסקאות דומות ישירות מול המדינה. מחשבון הנדל"ן yadata מבית יד2 : מחשבון המאזין לנתוני שוק, מרחקים ממוקדי עניין ועסקאות לפי כתובת. מחשבון נדל"ן - מחירון דירות לוי יצחק : בדיקת שווי דירה ומחירים של דירות שנמכרו בסביבה. דירובוט - מחשבון שווי נכס : אומדנים למחירי מכירה ושכירות המבוססים על נתונים ממאגר רש…
- AI overview sources: https://www.hoomy.co.il/estimation · https://www.wecheck.co.il/blog/כמה-שווה-הדירה-שלי/ · https://yadata.yad2.co.il/property-valuation · https://yadata.yad2.co.il/ · https://levi-itzhak.co.il/realestate/ · https://www.dirobot.co.il/ · https://www.nadlan.gov.il/ · https://www.madlan.co.il/propertyevaluation/ · https://yasmint-law.com/appreciation-tax/כמה-שווה-הדירה-שלי/

#### "הערכת שווי דירה בחינם" (desktop), retrieved 2026-10-25 19:23 UTC

| # | domain | title | url |
|---|---|---|---|
| 1 | www.landsman.co | הערכת שווי נכס - Landsman | https://www.landsman.co/הערכת-שווי-נכס/ |
| 2 | makovern.com | הערכת שווי של דירה או נכס | https://makovern.com/הערכת-שווי/ |
| 3 | www.govmap.gov.il | מחשבון שווי נכס | https://www.govmap.gov.il/sites/property_value.html |
| 4 | www.facebook.com | איך אפשר לבדוק מה ערך הבית שלי למכירה ? באיזה אתר ? או ... | https://www.facebook.com/groups/194140814113177/posts/2732106510316582/ |
| 5 | www.habita.com | הערכת מחיר הנכס | https://www.habita.com/il/valuation |
| 6 | moranatiasre.com | כמה שווה הבית שלי? הערכת שווי מקצועית עם ... | https://moranatiasre.com/כמה-שווה-הבית-שלי/ |
| 7 | app.hoomy.co.il | הערכת שווי דירה חינם | https://app.hoomy.co.il/estimation |
| 8 | www.appraiseit.co.il | מחיר דירה מדויק תוך שניות - חישובי עומק בגיבוי מומחי נדל"ן ולמידת מכונ | https://www.appraiseit.co.il/מחיר-דירה/ |
| 9 | idantao.co.il | הערכת מחיר דירה · הערכת שווי דירה מקצועית ומדויקת ... | https://idantao.co.il/הערכת-מחיר-דירה/ |
| 10 | idantao.co.il | הערכת מחיר דירה · הערכת שווי דירה מקצועית ומדויקת ... | https://idantao.co.il/הערכת-מחיר-דירה/ |

- nad-lan.co.il in this SERP: not in top 20
- People also ask: absent
- Related searches: הערכת שווי דירה מדלן · מחשבון שווי דירה · הערכת שווי דירה יד 2 · מחיר דירה לפי כתובת · איך לקבוע מחיר שכירות · מחשבון עליית ערך דירה · מחשבון מכירת דירה מחיר למשתכן · שווי דירה לפי קומה · מחשבון הערכת שווי דירה · איך להעריך שווי נכס · הערכת שווי מגרש
- AI overview: present. Gist: ניתן לקבל הערכת שווי דירה בחינם דרך מספר כלים דיגיטליים וגורמים בשוק : מחשבון שווי נכס ממשלתי: ניתן להזין את פרטי הנייד או הדירה (ישוב, שכונה, חדרים, שנת ייצור, שטח וקומה) ב- מחשבון שווי נכס של Govmap. בדיקת עסקאות אמיתיות: מומלץ לבדוק עסקאות קודמות שבוצעו בפועל באזור שלכם באתר רשות המסים או דרך מאגרי מידע כמו ביזפורטל. רשות המסים הערכה על ידי גורמי נדל"ן ומשרדי תיווך: חברות כמו Hoomy או Habita מציעות הערכת שווי והער…
- AI overview sources: https://www.hon.co.il/מחשבון-מחירי-הדירות/ · https://www.govmap.gov.il/sites/property_value.html · https://www.bizportal.co.il/realestates/news/article/20030124 · https://www.facebook.com/groups/194140814113177/posts/2732106510316582/ · https://www.habita.com/il/valuation · https://app.hoomy.co.il/estimation · https://www.appraiseit.co.il/מחיר-דירה/

#### "איך יודעים מה מחיר השיווק הנכון לדירה?" (desktop), retrieved 2026-10-25 19:23 UTC

| # | domain | title | url |
|---|---|---|---|
| 1 | www.a-g-m.co.il | איך קובעים מחיר שיווק לנכס? כמה שווה הדירה שלכם | https://www.a-g-m.co.il/כמה-שווה-הדירה-שלי/ |
| 2 | nadlanisraeli.co | איך יודעים מה מחיר השיווק הנכון לדירה? מדריך 4 שלבים 2026 | https://nadlanisraeli.co/איך-לקבוע-מחיר-לדירה-לפני-מכירה/ |
| 3 | ono-nadlan.co.il | איך קובעים מחיר שיווק לנכס? · אלי שאנן - אונו נדל"ן | https://ono-nadlan.co.il/marketing-price-for-property/ |
| 4 | harel-vered.co.il | איך יודעים מה מחיר השיווק הנכון לדירה | https://harel-vered.co.il/מאמרים/how-to-set-right-apartment-listing-price/ |
| 5 | purenadlan.co.il | מוכרים דירה? כך תגלו כמה הנכס שווה - כלים מקצועיים להערכת שווי ... | https://purenadlan.co.il/property-worth/ |
| 6 | evelinadlan.co.il | איך תדעו את מחיר השיווק הריאלי של הדירה שלכם? | https://evelinadlan.co.il/know8/ |
| 7 | bh-pk.co.il | איך להעריך שווי נכס לפני מכירה? | https://bh-pk.co.il/הערכת-שווי-נכס-לפני-מכירה/ |
| 8 | www.facebook.com | כשרואים מחיר שיווק של דירה כמה נהוג לתת הצעה ראשונית פחות ... | https://www.facebook.com/groups/tziporfinansit/posts/2135617453848959/ |
| 9 | www.wecheck.co.il | כמה שווה הדירה שלי? - מידע מקיף עם הצעות | https://www.wecheck.co.il/blog/כמה-שווה-הדירה-שלי/ |
| 10 | www.facebook.com | איך קובעים מה המחיר הנכון של הבית שלכם בשוק של 20206?** **טיפים ... | https://www.facebook.com/BARHOME.Boutique.Brokers/videos/איך-קובעים-מה-המחיר-הנכון-של-הבית-שלכם… |

- nad-lan.co.il in this SERP: not in top 20
- People also ask: איך אני יכול לדעת כמה שווה הדירה שלי? · איפה הכי זול לקנות דירה בישראל? · מהן הבדיקות שיש לבצע לפני קניית דירה? · איפה הכי כדאי להשקיע בדירה בישראל? · איפה אפשר למצוא דירות חדשות עד 1.2 מיליון שקל בישראל? · איזה בית השקעות הכי טוב בישראל? · איך להשקיע כסף בבנק? · איפה כדאי להשקיע 70 אלף שקל? · איפה להשקיע 50 אלף שקל?
- Related searches: absent
- AI overview: present. Gist: כדי לקבוע את מחיר השיווק הנכון לדירה, יש לבצע ניתוח שוק המבוסס על עסקאות אמיתיות, מאפייני הנכס והשוואה לסביבה. בדיקת עסקאות אמת (ניתוח שוק השוואתי): יש לבדוק מה היה מחיר המכירה בפועל של דירות דומות באותה שכונה או רחוב בחודשים האחרונים. ניתן להיעזר ב אתר רשות המיסים או במאגרי מידע ומחשבונים כגון מדלן ואתרים כמו לוי יצחק מחשבון נדל"ן. התאמה למאפייני הדירה הספציפית: גודל ומבנה: חישוב מחיר למטר מרובע ביחס לקומה, מעלית וח…
- AI overview sources: https://nadlanisraeli.co/איך-לקבוע-מחיר-לדירה-לפני-מכירה/ · https://www.a-g-m.co.il/כמה-שווה-הדירה-שלי/ · https://ono-nadlan.co.il/marketing-price-for-property/ · https://www.nadlanmaster.co.il/הערכת-שווי-דירה-כמה-שווה/ · https://levi-itzhak.co.il/realestate/ · https://purenadlan.co.il/property-worth/ · https://evelinadlan.co.il/know8/ · https://www.facebook.com/BARHOME.Boutique.Brokers/videos/איך-קובעים-מה-המחיר-הנכון-של-הבית-שלכם-בשוק-של-20206טיפים-חשובים-בסרטוןכולם-רוצי/4416121925304835/ · https://www.amitvered.co.il/קניית-דירה/

---

## 3. Competitor DNA (read in full)

### 3.1 wecheck.co.il · blog "כמה שווה הדירה שלי?" (#1 for "הערכת שווי נכס" on desktop and phone)
- **Placement:** title "כמה שווה הדירה שלי? - מידע מקיף עם הצעות - WeCheck blog" (55). H1 "כמה שווה הדירה שלי?". Counts: כמה שווה 5 · הערכת שווי 6 · הערכת שווי נכס 1 · הערכת שווי דירה 1 · שמאי 8.
- **Structure:** why knowing the value matters (six reasons) · tools and methods (appraiser with the three valuation approaches, brokers with comparative market analysis, online calculators; tips: Tax Authority deal data, the government real estate site, yadata, dirobot, madlan) · nine value factors · how to raise the value (with uplift percentages: renovation about 5%, safe room 5 to 8%, elevator about 6%, lobby about 4%, all **unsourced**) · pitfalls of each method · practical steps · equity-release loan CTA (up to 85% of value).
- **Size:** 1,997 words · 0 tables · 0 tools · 19 visuals (banners and images) · 2 official links. Published 19.11.2024, modified 9.3.2025 (stale).
- **Why it ranks:** a strong fintech domain, the exact question in title and H1, and a "tools and methods" outline that matches the AI overview's list almost line for line. Weak: no number, no data, no date, unsourced percentages.

### 3.2 landsman.co · "הערכת שווי נכס" (#1 "הערכת שווי דירה בחינם", #2 "בדיקת שווי נכס", #3 "הערכת שווי נכס")
- **Placement:** title "הערכת שווי נכס - Landsman" (25), H1 "הערכת שווי נכס". 246 words.
- **What it is:** a four-step lead form for a broker franchise: (1) address, (2) sale or rent, type (apartment, duplex, garden, penthouse, private house), floor 1 to 20+, rooms 1 to 10, parking 1 to 5, balcony, (3) 13 feature ticks (accessibility, renovated, storage, safe room, elevator, furnished, air conditioning, bars and more), (4) contact details and newsletter consent. **No result on screen**: an agent calls back.
- **Schema:** BreadcrumbList, WebPage. Published 12.1.2026.
- **Why it ranks:** exact-match title and H1, a large brand, and a form Google reads as a valuation tool. It wins "בחינם" without the word in the title.

### 3.3 govmap.gov.il · `/sites/property_value.html` "מחשבון שווי נכס" (#4 "הערכת שווי נכס", #3 "הערכת שווי דירה בחינם", named by the AI overview)
- **Inputs (from the page code):** settlement, neighbourhood, rooms (2 to 7 by halves), build year, area, floor, asset type (15 types, from "דירה בבית קומות" to "חנות"), tick "דירה מקבלן".
- **Method (from the page code):** one linear regression per neighbourhood: intercept + area + asset type + floor + rooms + build year (+ a new-from-contractor term). Output: "שווי מוערך לנכס" in ₪.
- **Catch:** a login window (user name and password) opens on load, so the public can not run it. 52 words, no schema.
- **Why it ranks:** the govmap.gov.il domain and an exact title. **Lesson:** Google and the AI overview already treat a transparent, per-neighbourhood estimate from official deals as the answer to this query; the government's own version is locked.

### 3.4 ey-group.co.il (E&Y appraisers) · "מחשבון הערכת שווי דירה" (#1 on phone for "הערכת שווי דירה") and "הערכת שווי דירה - כמה עולה שמאי" (#2 desktop and phone)
- Title and H1 exact ("מחשבון הערכת שווי דירה", 22 chars). About 350 words. **No calculator on the "calculator" page**, a callback form, an author box (named licensed appraiser, member of the appraisers' urban renewal committee). The guide page was last modified 19.12.2023.
- **Why it ranks:** exact titles, appraiser expertise signals (named licensed author), a domain full of appraisal pages. Thin content still wins on title match.

### 3.5 yadata.yad2.co.il · `/property-valuation` (#2 "הערכת שווי"; first source in every AI overview; read via WebFetch, plain fetch hits a bot check)
- Title "מחשבון הנדל"ן yadata מבית יד2 | חישוב הערך לנכס שלך", H1 "תהליך אפיון הנכס".
- **Inputs (the richest form in the SERP):** address · sale or rent · type (apartment, duplex, garden, penthouse, private house) · rooms 1 to 12+ by halves · size · condition (חדש מקבלן, חדש, משופץ, שמור, דרוש שיפוץ) · balconies 0 to 3 · parking 0 to 3 · storage, air conditioning, safe room, furnished, bars · building on pillars · floor · floors in the building · accessibility · elevator.
- No method, source or date on the page. About 450 words.
- **Why it ranks:** the Yad2 brand and its own listings data; the AI overview names it first.

### 3.6 dirobot.co.il · `/calculator` (#3 "הערכת שווי"; AI overview source; read via WebFetch)
- Title "מחשבון הערכת שווי נכסים | דירובוט", H1 "הערכת שווי אוטומטית לנכס".
- **Inputs:** city, street, house number, type (4), rooms, size, floor, condition (5), elevator, balcony, safe room, parking.
- **Outputs:** sale value range, monthly rent, recorded deals against asking prices, gross yield (extended report).
- **Sources claimed:** Tax Authority recorded deals, public sale listings, public rent listings. A method section ("שלושה אומדנים ממקורות נפרדים", "מגבלות שכדאי להכיר מראש").
- **Friction:** the result needs a login; 3 free estimates a month; PDF by plan. FAQ (5), HowTo, SoftwareApplication schema. 1,361 words raw.
- **Why it ranks:** a dedicated product with a method section, schema and AI overview mentions.

### 3.7 Also strong (short)
- **hoomy.co.il/estimation** (#9 "הערכת שווי"; AI overview): "חינם" in the title, address first (city, street, number), claims "רשות המיסים" and "משרד המשפטים" as sources; FAQPage and WebApplication schema; result screen not visible before continuing (WebFetch).
- **habita.com/il/valuation** (#4 and #5 on three queries): broker chain; free verbal valuation by visit, written valuation paid; contact form; 842 words; no tool.
- **idantao.co.il** (#1 desktop "הערכת שווי דירה"): appraiser firm; a 93-character title carrying both "הערכת מחיר דירה" and "הערכת שווי דירה"; factor list and "how to choose an appraiser" (check the licence); callback forms; modified 16.8.2026.
- **broker-re.co.il** (#1 "בדיקת שווי נכס"): a downloadable guide behind an email field; title "חישוב שווי דירה - איך תדעו כמה הדירה שלכם באמת שווה?".
- **madlan.co.il/propertyevaluation** (#4 "הערכת שווי"): answered 403 to both fetch methods; not read (unverified).

---

## 4. Union checklist (everything any competitor has, plus what none has)

| Item | Who has it | We have it today |
|---|---|---|
| Address input and one number back | yadata, dirobot, hoomy, propio, appraiseit; landsman (form only) | no (city, neighbourhood, rooms) |
| Property type (apartment, garden, penthouse, duplex, private house) | yadata, landsman, dirobot, govmap (15 types) | no |
| Rooms beyond 3 to 5 (2, 6, halves) | yadata, govmap, landsman | 3, 4, 5 only |
| Condition scale | yadata (5), dirobot (5) | condition adjustment % |
| Floor and floors in the building, elevator, pillars | yadata, govmap (floor), landsman | floor adjustment % |
| Balcony, parking, storage, safe room | yadata, dirobot, landsman | balcony area, parking, storage (no safe room) |
| Build year, new from a contractor | govmap, yadata (condition) | no |
| Value range, not a point | dirobot | yes |
| Asking price vs value | dirobot (deals vs asking) | yes |
| Rent estimate and gross yield | dirobot | no (other site tools) |
| Official deal medians by neighbourhood and rooms, with the quarter | **nobody but us** | yes (23 cities, 280 neighbourhoods with a median) |
| Method and limits section | dirobot, ours | yes |
| When to use an appraiser | wecheck, E&Y, idantao, ours | yes |
| Appraiser cost | E&Y page title, AI overview (2,500 ₪, unverified) | no |
| Check the appraiser's licence | idantao (advice only) | no |
| Value factors list | all | yes (table) |
| How to raise the value | wecheck (unsourced %) | no |
| List of tools and official sources | wecheck, AI overview | yes (sources section) |
| Mortgage, inheritance, divorce valuations | E&Y, wecheck mentions; GSC demand | partly (one paragraph) |
| FAQ | dirobot 5, hoomy, ours 5 | 5 |
| No sign-up, no phone | propio (claims), hoomy (unclear) | yes |
| **Value since you bought, by the CBS dwelling price index of your district** | **nobody** ("מחשבון עליית ערך דירה" is a related search) | no |
| **The official 5-year median series for your neighbourhood and room count** | **nobody** | no (latest quarter only) |
| **Three official anchors side by side, each with its formula and date** | **nobody** (govmap's regression is locked; AVMs are black boxes) | no |
| **Licence lookup against the Ministry of Justice register** | **nobody** | no |

---

## 5. Verified facts (for the spec)

| # | Fact | Source | Date / how |
|---|---|---|---|
| V1 | The Tax Authority deal summaries behind nadlan.gov.il are public JSON files per settlement and neighbourhood (`data.nadlan.gov.il/api/pages/settlement/buy/<code>.json`, `/neighborhood/buy/<id>.json`), version "20-08-2026", Last-Modified 20.8.2026 | data.nadlan.gov.il (official) | Tel Aviv file re-checked 25.10.2026: unchanged |
| V2 | Each file holds the median closed-deal price for 3, 4, 5 rooms and all apartments for **22 quarters (1-3.2021 to 4-6.2026)**, the city line and the Israel line | same | 25.10.2026 (API) |
| V3 | Israel median, 4 rooms: 2,072,000 ₪ (1-3.2026), 2,028,800 ₪ (4-6.2026), 2,113,300 ₪ (4-6.2025): **-4.0% in a year**. 3 rooms 1,677,400 ₪ and 5 rooms 2,822,700 ₪ in 4-6.2026 | same | 25.10.2026 (API) |
| V4 | Tel Aviv-Yafo median 1-3.2026: 3 rooms 4,225,800 ₪ · 4 rooms 5,229,800 ₪ · 5 rooms 7,497,700 ₪ | same | 25.10.2026 (API) |
| V5 | Yavne (2660) has a file: 4 rooms 2,473,700 ₪ in 1-3.2026 vs 2,319,300 ₪ in 1-3.2025 (+6.7%); 8 neighbourhoods. **Not in our tool today** | same | 25.10.2026 (API) |
| V6 | Our tool's data: 23 cities, 718 neighbourhoods listed, 280 with a median in the latest quarter; city medians by rooms as shown in the page table | `plugins/nadlan-config/assets/instruments/data/value.json` (file 20.8.2026, read 7.10.2026) and `docs/research/2026-10-07-city-prices/` | code |
| V7 | CBS dwelling price index (series 40010, base 1993 average = 100): **590.0 for July 2026**; -0.6% on the month; **-1.8% on the year**; +5.5% over 3 years; +26.8% over 5 years; peak 609.8 in January 2025, now 3.2% below it | api.cbs.gov.il/index/data/price?id=40010 | 25.10.2026 (API); our calc for 3y, 5y, peak |
| V8 | CBS dwelling price index by district, change to July 2026. 12 months: ירושלים -0.2% · צפון -0.8% · חיפה -1.4% · מרכז -2.7% · תל אביב -1.9% · דרום -1.5%. 5 years: +29.3% · +42.3% · +41.2% · +24.0% · +18.9% · +26.1% | CBS series 60000, 60100, 60200, 60300, 60400, 60500 | 25.10.2026 (API); our calc from the published values (district series start 2018) |
| V9 | CBS note on the index: an indicator of dwelling price changes, not part of the CPI; recent values are provisional and revised every month as more deals are reported | CBS catalog note for 40010 | 25.10.2026 (API) |
| V10 | Worked example (all official inputs): a 4-room flat bought at Yavne's median of 1-3.2021 (1,780,200 ₪) is about **2,305,900 ₪** by the Center district index (March 2021 to July 2026, +29.5%), about **2,341,800 ₪** by the national index (+31.5%), and the Yavne 4-room median itself is **2,473,700 ₪** in 1-3.2026 (+39.0%) | V2, V5, V7, V8 | our calc, 25.10.2026 |
| V11 | Ministry of Justice register "מאגר שמאי מקרקעין": **3,182 licensed real estate appraisers**; fields: name, licence number, file number, city (city filled for 376 only) | data.gov.il dataset `shamaim`, resource 8540534a-eccd-4568-a677-652d589ed172 | updated 24.10.2026; pulled 25.10.2026 (API) |
| V12 | govmap "מחשבון שווי נכס": per-neighbourhood regression on area, asset type, floor, rooms, build year, new-from-contractor; locked behind a login | govmap.gov.il/sites/property_value.html (page code) | raw, 25.10.2026 |
| V13 | The Tax Authority's own service page for deal data: "מאגר מידע נדל"ן" | gov.il/he/service/real_estate_information | SERP, 25.10.2026 |

**Unverified, kept out of the spec:** appraisal cost "about 2,500 ₪" (AI overview from a private price list), wecheck's uplift percentages, the files' "yield" and "priceIncreases" indexes (definition not published), dirobot or yadata accuracy, bank loan-to-value limits (not re-checked at boi.org.il today), madlan's tool (403).

---

## 6. Our page as Google gets it (raw HTML, `?x=` cache-buster, 25.10.2026)

- **Title:** "מחשבון שווי דירה - נדלן" (23 chars). Meta: "מחשבון שווי דירה: הערכת מחיר לפי נתוני עסקאות אמיתיות לפני קנייה או מכירה. כלי עזר לתמחור נכון. נדלן חכם."
- **H1:** "מחשבון שווי דירה", subtitle "טווח מחיר ראשוני לפני מכירה, קנייה או משא ומתן".
- **Answer paragraph:** "שווי דירה אינו נקבע לפי תחושה בלבד. המחיר מושפע מעסקאות דומות באזור..." (no "הערכת שווי" in it). A later paragraph gives the Q1 2026 medians (Tel Aviv 4 rooms 5,229,800 ₪, the Kikar Hamedina area 6,835,800 ₪, Haifa 1,597,500 ₪).
- **Tool `pval`** (`assets/instruments/tools/pval.js`): city (23) → neighbourhood or whole city → rooms 3/4/5 → official median; or area × price per m²; adjustments: balcony area × value per m², parking value, storage value, condition %, floor %, caution range %; asking price check. Output: estimated value, low and high, base, adjustments, price per m², asking price against value, source line.
- **Tables:** city medians by rooms (23 rows) and the value factors table (7 rows).
- **Sections (H2):** 13 article sections (how to start, how to use, what moves the price, official deals vs listings, when an appraiser, seller check, buyer check, mistakes, time on market, sources, FAQ, summary) and 9 city price link H2s (Tel Aviv, Neve Tzedek, Herzliya Pituach, Herzliya, Ramat Hasharon, Raanana, Kfar Shmaryahu, Savyon, Rishpon).
- **FAQ:** 5, visible and in schema. **Schema:** WebPage, SoftwareApplication (with Offer), FAQPage. dateModified 21.10.2026.
- **Size:** 2,555 words · 83 figures · 2 tables / 120 cells · 1 tool · 28 headings · 1 visual · 3 official links (nadlan.gov.il, gov.il, cbs.gov.il).

### Our gaps (ordered)
1. **Head terms missing where Google looks first:** "הערכת שווי דירה" 0 in title and H1 (2 in body); "הערכת שווי נכס" 0 anywhere; "חינם / בחינם" 0; the exact "כמה שווה הדירה שלי" 0. Depth is already ahead of every competitor (section 9), placement is the main reason we sit at 20 to 30.
2. **The seller question has no heading:** "איך יודעים מה מחיר השיווק הנכון לדירה?" brings 247 impressions in two spellings, plus "מחיר שיווק לנכס", "איך לתמחר דירה למכירה".
3. **Tool scope:** rooms 3 to 5 only; no property type (private house 49 impressions, garden, penthouse); no build year or safe room; 23 cities only (Yavne demand, V5).
4. **No "since you bought" answer**, although the related search "מחשבון עליית ערך דירה" appears and the official index is free (V7, V8).
5. **Latest quarter only**: the 22-quarter official series is unused.
6. **Visuals: 1** (wecheck 19, dirobot 12, landsman 11).
7. **FAQ: 5**, while GSC shows at least 20 question-shaped queries.
8. **No licence check for appraisers** (V11), and the mortgage, inheritance and divorce cases are one paragraph despite live demand.
9. **Title 23 chars**, under-used.

---

## 7. BUILD SPEC

### 7.1 Keep (additive law: nothing removed)
The `pval` tool and all its fields and outputs · the city medians table · the value factors table · every current article section and the 5 FAQ · the city price links block · SoftwareApplication, FAQPage, WebPage schema · links to `/property-value/` and to the appraiser page.

### 7.2 Title (≤60)
`הערכת שווי דירה בחינם: מחשבון שווי נכס לפי עסקאות אמת | נדלן` (60 chars: 53 + brand)
Carries הערכת שווי דירה · בחינם · שווי נכס · מחשבון · עסקאות.

### 7.3 H1
`הערכת שווי דירה: כמה שווה הדירה שלכם לפי עסקאות אמת` (51 chars)

### 7.4 Answer paragraph (53 words; the first sentence holds the head term)
> הערכת שווי דירה מתחילה במחיר שבו נמכרו בפועל דירות דומות בשכונה שלכם, לא במחיר המודעות. המחשבון מציג את המחיר החציוני של עסקאות שדווחו לרשות המסים לפי שכונה ומספר חדרים, מתאים אותו לשטח, לקומה, לחניה ולמצב הדירה, ובודק לפי מדד מחירי הדירות של הלמ"ס כמה השתנה ערך הנכס מאז שקניתם. בלי הרשמה ובלי טלפון.

Meta description (proposal): `הערכת שווי דירה ונכס בחינם, לפי עסקאות אמת של רשות המסים לכל שכונה ומספר חדרים, ובדיקה מול מדד מחירי הדירות של הלמ"ס. בלי הרשמה.`

### 7.5 Section order (rendered, phones first: H1 → answer → CTAs → tool → facts → article)
1. H1 + answer paragraph.
2. CTAs: `בדקו את שווי הדירה עכשיו` (scrolls to the tool) · `מתי צריך שמאי` (anchor). Sitewide WhatsApp bar unchanged.
3. **The tool** (kept) with the moat panel (7.8) and the new fields: property type, rooms 2 to 6, all settlements that have an official file and GSC demand (start with Yavne), purchase month, year and price (optional).
4. H2 `שלוש בדיקות לשווי אחד`: how the three results are built, one line of formula each, the worked example V10 as table T3, infographic I3.
5. H2 `מחירי דירות לפי עיר ומספר חדרים`: table T1 + infographic I1.
6. H2 `כמה השתנו מחירי הדירות: מדד הלמ"ס לפי מחוז`: table T2 + infographic I2.
7. H2 `איך יודעים מה מחיר השיווק הנכון לדירה?`: the seller method (start from the three anchors, place the asking price on the range, why an asking price far above the range sits longer; no invented discount numbers).
8. H2 `מה משפיע על שווי דירה: קומה, חניה, מרפסת ומצב` (the existing factors table, kept).
9. H2 `איך מחשבים שווי של דירה לפי כתובת`: step by step on nadlan.gov.il (search by address, filter rooms and dates, read the deal list), what the list does not show (condition, renovation), table T4.
10. H2 `הערכת שווי על ידי שמאי מקרקעין`: kept section + H3 `הערכת שווי דירה למשכנתא` · H3 `הערכת שווי בירושה לפני מכירה` · H3 `הערכת שווי בגירושין` · H3 `איך בודקים שהשמאי מורשה` (the register lookup, V11) + table T5.
11. Existing sections kept in their order (official deals vs listings, seller check, buyer check, mistakes, time on market, sources).
12. H2 `שאלות נפוצות על הערכת שווי דירה` (7.9).
13. H2 `איך חישבנו ומאיפה הנתונים`: sources, file dates, formula, honesty lines.
14. The city price links block (kept), under one H2 `מחירי דירות לפי עיר`.

### 7.6 Tables (each with its real data source)
| ID | Table | Columns | Source |
|---|---|---|---|
| T1 | מחיר חציוני לפי עיר וחדרים | עיר · 3 חדרים · 4 חדרים · 5 חדרים · רבעון · שינוי בשנה (4 חדרים) | data.nadlan.gov.il settlement files (V1, V2); the existing 23 rows + Yavne + an Israel row with both quarters (V3) |
| T2 | מדד מחירי הדירות לפי מחוז | מחוז · שינוי ב-12 חודשים · ב-3 שנים · ב-5 שנים · מהשיא | CBS 40010 and 60000 to 60500 (V7, V8) |
| T3 | שלוש הבדיקות, דוגמה | בדיקה · נוסחה · תוצאה · תאריך הנתון | V10 (Yavne 4 rooms, bought at the 1-3.2021 median) |
| T4 | איפה בודקים מה | מקור · מה הוא נותן · מה הוא לא נותן | nadlan.gov.il, gov.il real_estate_information, CBS index, MoJ register, our tool |
| T5 | מחשבון או שמאי | מטרה (מכירה, קנייה, משכנתא, ירושה, גירושין, בית משפט) · מספיקה הערכה ראשונית? · מי מזמין · מסמך שנדרש | method table; no prices (cost unverified) |
| kept | גורמים שמשפיעים על המחיר | (existing 7 rows) | existing |

### 7.7 Infographics (2 to 3)
- **I1 Five years of official medians**: line chart, 22 quarters, your city or neighbourhood and room count against Israel; shown inside the tool result, and on the page for Israel and the top cities. Data V2.
- **I2 District index**: paired bars per CBS district, 12 months and 5 years, with the national line. Data V7, V8.
- **I3 The three anchors**: one horizontal scale with the three estimates as markers, the shaded range between them, and the asking price as a pin. Data: the visitor's inputs + V2, V7, V8.
Design note for the builder: palette from survey and land-registry paper (registry blue, stamp red for the asking price pin, graphite grid on white), Hebrew data face chosen for figures (tabular numerals), not the cream, brass or purple default.

### 7.8 THE MOAT: "שווי היום לפי מחיר הקנייה שלכם, בשלוש בדיקות רשמיות"
- **What it is:** one screen that answers "how much is my flat worth now" from three independent official anchors, each with its formula and date, with no sign-up and no phone number. Nobody in the SERP does this: AVMs give one black-box number behind a login, a fee or a callback (dirobot login and 3 a month, AppraiseIt 30 ₪, Landsman, Habita, E&Y forms), the government's regression is locked (V12), and the articles give no number.
- **Inputs:** city · neighbourhood · property type · rooms · size (optional) · purchase month and year (optional) · purchase price (optional) · asking price (optional).
- **Outputs:**
  - A. The official median for the neighbourhood (or the city when the neighbourhood has none) and room count, latest quarter, with the 22-quarter chart (I1).
  - B. Purchase price × (CBS district dwelling index now ÷ index in the purchase month); before 2018, the national index 40010.
  - C. Purchase price × (official median now ÷ official median in the purchase quarter), when both quarters exist.
  - D. The existing adjusted estimate (size, floor, parking, balcony, storage, condition).
  - The range from the lowest to the highest available anchor, the asking price placed on it, and one plain sentence when the anchors disagree (for example a neighbourhood median that jumped because more new flats sold that quarter).
  - When an anchor is missing, say which one and why ("אין חציון לשכונה ברבעון הזה, מוצג חציון העיר").
- **Data:** data.nadlan.gov.il settlement and neighbourhood files (official, public, no token; refresh when Last-Modified changes) · CBS API series 40010 and 60000 to 60500 (official; monthly) · settlement → CBS district from the CBS localities list on data.gov.il.
- **Honesty rules:** every number with its quarter or month; the CBS values are provisional and revised (V9), say so once; never call the result a valuation (שומה); the line "הערכה ראשונית, לא חוות דעת שמאית" stays.

### 7.9 FAQ (20 questions in searchers' words, from PAA, related searches and GSC)
1. איך אני יכול לדעת כמה שווה הדירה שלי?
2. האם הערכת שווי דירה באתר היא בחינם?
3. איך מחשבים שווי של דירה לפי כתובת?
4. איך יודעים מה מחיר השיווק הנכון לדירה?
5. איך אני יכול למצוא מידע על דירות שנמכרו?
6. מה ההבדל בין מחיר מבוקש במודעה למחיר שבו הדירה נמכרה?
7. מהי הערכת שווי דירה מבוססת AI, ובמה היא שונה מחישוב לפי עסקאות?
8. האם יש מחשבון שווי דירה של רשות המסים?
9. כמה עלה ערך הדירה שלי מאז שקניתי אותה?
10. האם מחירי הדירות ירדו בשנה האחרונה?
11. מתי צריך שמאי מקרקעין ולא מחשבון?
12. כמה עולה שמאי לדירה?
13. איך בודקים שהשמאי מורשה?
14. במה שונה הערכת שווי דירה למשכנתא?
15. איך מעריכים שווי דירה בירושה לפני מכירה?
16. האם מחשבון מספיק להערכת שווי בגירושין?
17. כמה משפיעה הקומה על שווי הדירה?
18. כמה מוסיפים חניה, מחסן ומרפסת לשווי?
19. האם המחשבון מתאים להערכת שווי בית פרטי?
20. למה מוצג חציון של העיר ולא של השכונה שלי?
Answer rules: 2 to 4 sentences, numbers only from section 5 with their date. Q8: say that the Tax Authority publishes the deals on the government real estate site, and that the public calculator page on govmap opens behind a login (V12). Q10: CBS, July 2026, -1.8% on the year, peak January 2025 (V7). Q12: no number (unverified); say the fee is agreed with the appraiser and depends on the property and the purpose, ask for a written quote, and check the licence (V11). Q17 and Q18: method only, no percentages.

### 7.10 Honesty target (from `proof-before.md`, raw HTML counts, 25.10.2026 21:32)
| Metric | Ours now | Best competitor (who) | Twelve competitors combined | Target after build |
|---|---|---|---|---|
| words | 2,555 | 1,997 (wecheck) | 5,570 | ≥ 3,500 (keep the lead, do not pad) |
| figures | 83 | 39 (landsman) | 104 | ≥ 250 (T1 with Yavne and YoY, T2, T3) |
| tables | 2 | 0 | 0 | ≥ 6 |
| cells | 120 | 0 | 0 | ≥ 250 |
| tools | 1 | 1 (propio, hoomy) | 2 | 1 tool with the moat panel (counted once) |
| faq | 5 | 5 (dirobot) | 16 | 20 visible = 20 in schema |
| headings | 28 | 24 (habita) | 89 | ≥ 40 |
| visuals | **1** (behind) | **19 (wecheck)** | 74 | ≥ 20: I1 to I3 plus charts inside the result; the honesty statement names this metric until we pass it |
| official sources | 3 | 2 (wecheck) | 2 | ≥ 6 (nadlan.gov.il, data.nadlan.gov.il, gov.il real_estate_information, CBS, data.gov.il register, govmap) |
| freshness | modified 21.10.2026; data 1-3.2026 (cities) | modified 16.8.2026 (dirobot, idantao) | | show both quarters (cities 1-3.2026, Israel 4-6.2026) and the CBS month (July 2026) |

Note on the count: raw HTML undercounts the script-rendered tools (yadata, madlan and the result screens of hoomy and dirobot are not in it). The honesty statement says the counts are of the page as Google first receives it.
