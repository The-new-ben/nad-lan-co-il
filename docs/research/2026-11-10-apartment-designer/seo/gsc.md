# nad-lan.co.il in Google Search Console: design, designer and planning queries

Property: `sc-domain:nad-lan.co.il` (the URL-prefix property `https://nad-lan.co.il/` returns 403 for this token; the domain property works).
Window: 10.8.2026 to 9.11.2026, dimensions query + page, full pagination, 9,737 rows in total. Pulled 10.11.2026 with `gsc_api.py query` (read-only).
Filter: query contains עיצוב, מעצב, פנים, תכנון, הדמיה, design, designer, סטיילינג, שינויי דיירים, מטבח, סלון, תלת מימד or 3d.
Note: GSC hides anonymised low-volume queries in query+page reports, so zero here means no reported row, not proven zero demand.

## Bottom line

- nad-lan has **no impressions at all** for the head queries of this page: עיצוב דירה, עיצוב פנים, מעצב/ת פנים, מעצב פנים מחיר, ייעוץ עיצוב, עיצוב דירה בתלת מימד, תוכנה/אפליקציה לעיצוב דירה, הדמיה לדירה, הום סטיילינג, תכנון מטבח, עיצוב סלון. The field is open; no existing page is protected by traffic on these heads.
- The only design-flavoured impressions go to `/interior-design-trends-2026-israel/` (7 single-impression queries about 2026 trends, positions 54 to 74).
- `תכנון` matches are almost all planning-law queries (תכנון ובנייה, תכנית מפורטת, רישוי) on glossary pages. They are a different intent (statutory planning) and must stay with the glossary.
- Tenant-changes price queries (`מחירון דקל שינויי דיירים`, 15 + 5 + 2 impressions) land on `/glossary/מחירון-דקל-לבנייה-ותשתיות/`.
- `/tour/designer/` has **no GSC rows**. It is live (HTTP 200) but carries `<meta name="robots" content="noindex">` and no canonical, and it is not in the sitemap. Reported as a finding only; nothing was changed.

## Existing nad-lan pages that sit next to this page's intents (cannibalisation guard)

| URL | Title / H1 (live, 10.11.2026) | Intent it owns | GSC 90 days | What the new page must do |
|---|---|---|---|---|
| `/guides/new-apartment-buyer-changes/` | שינויי דיירים בדירה חדשה מקבלן, מדריך מעשי / H1 שינויי דיירים ושדרוגים בדירה חדשה מקבלן (4,725 words, 7 tables) | **שינויי דיירים** (all variants: מה זה, מחיר, בדירה מקבלן, טיפים) | 0 rows | Do not target שינויי דיירים. Link to it from the contractor-apartment section. |
| `/guides/new-apartment-sale-specification/` | מפרט מכר דירה חדשה: איך לקרוא תוכניות לפני חתימה | מפרט מכר, תכנית מכר | 25 rows, 275 impr (תכנית מכר דירה 40, pos 28) | Link when the engine imports a sale plan. Do not target תכנית מכר. |
| `/glossary/מחירון-דקל-לבנייה-ותשתיות/` | מחירון דקל | מחירון דקל, incl. מחירון דקל שינויי דיירים | 76 rows, 2,635 impr | Do not target מחירון דקל. Link from price sections. |
| `/interior-design-trends-2026-israel/` | עיצוב פנים 2026: הצבעים, החומרים והטרנדים שנכנסים לדירות החדשות (330 words) | טרנדים בעיצוב הבית 2026, עיצוב בתים 2026 | 7 rows, 7 impr | Do not target 2026 trends; link to it from the styles section. Its URL owns the head word `interior`. |
| `/renovation-contractor/` | קבלן שיפוצים לפני קניית דירה (H2: מתי צריך אדריכל, מעצב או מפקח בנייה?) | קבלן שיפוצים, הצעת מחיר קבלן | 0 rows | Link for renovation execution. Do not target קבלן שיפוצים. |
| `/architect-building-permit/` | אדריכל והיתר בנייה (H3: מתי צריך אדריכל ומתי מספיק מעצב פנים?) | אדריכל, היתר בנייה, עלות אדריכל | 3 rows, 12 impr (עלות אדריכל שיפוץ בית, pos 17) | Overlap on the question אדריכל או מעצב פנים. See intent-map.md for the decision. |
| `/tours/` | סיורים תלת ממדיים בפרויקטים חדשים (H2: מעצב הדירות) | 3D tours of projects | 8 rows, 22 impr | Links to the designer demo; keep. |
| `/tour/designer/` | מעצבים את הבית — דירת דוגמה ברובע שדה דב (noindex) | the current designer demo (engine prototype) | 0 rows | Finding only. Not in the index, so it does not compete. |
| `/glossary-category/interior-design/` | ארכיון interior-design (glossary taxonomy: gypsum boards etc.) | glossary archive | 1 row | Owns the token pair `interior-design` in a URL. |
| `/professionals/demo-dana-barak-design/` | demo professional profile (interior designer) | directory demo | 0 rows | Possible destination for a designer directory block. |

## All matching query + page rows (74 rows, sorted by impressions)

| Impr | Clicks | Pos | Query | Page |
|---:|---:|---:|---|---|
| 175 | 0 | 24.3 | תכנון מפורט | `/glossary/תכנית-מפורטת/` |
| 65 | 0 | 9.4 | התוספת השלישית לחוק התכנון והבניה | `/glossary/התוספת-השלישית-לחוק-התכנון-והבנייה/` |
| 31 | 0 | 43.3 | תכנון יסודות | `/glossary/raft-foundation/` |
| 30 | 0 | 33.2 | תכנון מגדלי מגורים | `/projects/` |
| 29 | 0 | 65.7 | תכנון משכנתא | `/mortgage-calculator/` |
| 29 | 0 | 26.8 | תקנות התכנון והבניה רישוי בניה | `/glossary/תקנות-התכנון-והבנייה-רישוי-בנייה-תשע/` |
| 27 | 0 | 31.5 | תקנות התכנון והבנייה רישוי בנייה | `/glossary/תקנות-התכנון-והבנייה-רישוי-בנייה-תשע/` |
| 26 | 0 | 28.2 | תקנות התכנון והבנייה (רישוי בנייה) | `/glossary/תקנות-התכנון-והבנייה-רישוי-בנייה-תשע/` |
| 24 | 0 | 13.5 | תקנות התכנון והבניה 2016 | `/glossary/תקנות-התכנון-והבנייה-רישוי-בנייה-תשע/` |
| 22 | 0 | 31.2 | תקנות התכנון והבניה בקשה להיתר תנאיו ואגרות​ | `/glossary/תקנות-התכנון-והבנייה-בקשה-להיתר-תנאיו/` |
| 19 | 0 | 28.5 | תקנות התכנון והבניה רישוי | `/glossary/תקנות-התכנון-והבנייה-רישוי-בנייה-תשע/` |
| 19 | 0 | 30.7 | תקנות התכנון והבניה רישוי בניה​ | `/glossary/תקנות-התכנון-והבנייה-רישוי-בנייה-תשע/` |
| 17 | 0 | 28.4 | פרויקטים בתכנון | `/projects/` |
| 15 | 0 | 19.1 | מחירון דקל שינויי דיירים | `/glossary/מחירון-דקל-לבנייה-ותשתיות/` |
| 14 | 0 | 35.2 | תכנון בטון | `/construction-engineering-guide/` |
| 13 | 0 | 36.7 | תכנון מבנים מתועשים | `/construction-engineering-guide/` |
| 11 | 0 | 18.3 | תכנון פרויקטים התחדשות עירונית מתחמית | `/urban-renewal/map/` |
| 8 | 0 | 37.1 | הדמייה תמ"א 38 | `/urban-renewal/tama-38/` |
| 8 | 0 | 16.5 | קונסטרוקטור לתכנון ממד | `/glossary/קונסטרוקטור/` |
| 8 | 0 | 44.0 | תכנון ורישוי | `/glossary/תקנות-התכנון-והבנייה-רישוי-בנייה-תשע/` |
| 7 | 0 | 9.4 | חוק התכנון והבניה התוספת השלישית | `/glossary/התוספת-השלישית-לחוק-התכנון-והבנייה/` |
| 6 | 0 | 4.2 | תוספת שלישית לחוק התכנון והבניה | `/glossary/התוספת-השלישית-לחוק-התכנון-והבנייה/` |
| 6 | 0 | 56.0 | תקנות התכנון והבניה | `/glossary/תקנות-התכנון-והבנייה-בקשה-להיתר-תנאיו/` |
| 5 | 0 | 26.4 | דקל שינויי דיירים | `/glossary/מחירון-דקל-לבנייה-ותשתיות/` |
| 4 | 0 | 94.8 | הדמייה תמ"א 38 | `/glossary/tama-38-term/` |
| 4 | 0 | 13.0 | קונסטרוקטור לתכנון ממ"ד | `/glossary/קונסטרוקטור/` |
| 4 | 0 | 36.0 | תכנון ורישוי | `/glossary/תקנות-המהנדסים-והאדריכלים-רישוי-וייח/` |
| 3 | 0 | 30.3 | מגדלי יו מבפנים | `/projects/yoo-tel-aviv/` |
| 3 | 0 | 13.0 | מד שטח פנים | `/glossary/מד-לייזר/` |
| 3 | 0 | 10.0 | מצא לי פרויקטים למגורים חדשים עם דגש על סביבה ירוקה ותכנון מודרני. | `/projects/הנטקה/` |
| 3 | 0 | 87.0 | תכנון מבנה מסחרי | `/commercial-real-estate/` |
| 3 | 0 | 36.0 | תקנות התכנון והבנייה | `/glossary/תקנות-התכנון-והבנייה-בקשה-להיתר-תנאיו/` |
| 2 | 1 | 19.5 | חוק התכנון והבניה תוספת שלישית | `/glossary/התוספת-השלישית-לחוק-התכנון-והבנייה/` |
| 2 | 1 | 9.5 | מחירון דקל שינויי דיירים pdf | `/glossary/מחירון-דקל-לבנייה-ותשתיות/` |
| 2 | 0 | 52.5 | מינהל התכנון רישוי זמין | `/glossary/רישוי-זמין/` |
| 2 | 0 | 6.0 | פרויקטים בתכנון | `/urban-renewal/map/` |
| 2 | 0 | 22.5 | תכנון בעסקאות נדל ן | `/apartment-deal-check/` |
| 2 | 0 | 70.0 | תכנון הוצאות ברכישת דירה | `/buying-apartment/` |
| 2 | 0 | 92.0 | תכנון מגדלי מגורים | `/site-map/` |
| 2 | 0 | 31.0 | תכנון קונסטרוקטיבי | `/glossary/קונסטרוקטור/` |
| 2 | 0 | 29.5 | תקנות התכנון והבניה בקשה להיתר תנאיו ואגרות | `/glossary/תקנות-התכנון-והבנייה-בקשה-להיתר-תנאיו/` |
| 2 | 0 | 14.0 | תקנות התכנון והבניה בקשה להיתר תנאיו ואגרות תש ל 1970 | `/glossary/תקנות-התכנון-והבנייה-בקשה-להיתר-תנאיו/` |
| 2 | 0 | 49.0 | תקנות התכנון והבניה נבו | `/glossary/תקנות-התכנון-והבנייה-בקשה-להיתר-תנאיו/` |
| 2 | 0 | 38.0 | תקנות תכנון ובניה | `/glossary/תקנות-התכנון-והבנייה-בקשה-להיתר-תנאיו/` |
| 1 | 0 | 37.0 | בקרת תכנון | `/glossary/תוכנית-בקרת-איכות/` |
| 1 | 0 | 18.0 | התוספת השלישית לחוק התכנון והבניה היטל השבחה | `/glossary/התוספת-השלישית-לחוק-התכנון-והבנייה/` |
| 1 | 0 | 18.0 | התוספת השלישית לחוק התכנון והבנייה | `/glossary/התוספת-השלישית-לחוק-התכנון-והבנייה/` |
| 1 | 0 | 64.0 | טרנדים בעיצוב הבית 2026 | `/interior-design-trends-2026-israel/` |
| 1 | 0 | 74.0 | טרנדים חדשים בעיצוב סלון 2026 | `/interior-design-trends-2026-israel/` |
| 1 | 0 | 56.0 | טרנדים לעיצוב הבית לשנת 2026 | `/interior-design-trends-2026-israel/` |
| 1 | 0 | 34.0 | מבנה פשוט חוק התכנון והבניה | `/glossary/תקנות-המהנדסים-והאדריכלים-רישוי-וייח/` |
| 1 | 0 | 61.0 | מגמות בעיצוב כורסאות לשנת 2026 | `/interior-design-trends-2026-israel/` |
| 1 | 0 | 24.0 | מינהל התכנון מכוני בקרה | `/glossary/מכוני-בקרה/` |
| 1 | 0 | 28.0 | מכון בקרה מנהל התכנון | `/glossary/מכוני-בקרה/` |
| 1 | 0 | 78.0 | מנהל התכנון רישוי זמין | `/glossary/רישוי-זמין/` |
| 1 | 0 | 62.0 | מערכת רישוי זמין מנהל התכנון | `/glossary/רישוי-זמין/` |
| 1 | 0 | 55.0 | עיצוב בתים 2026 | `/interior-design-trends-2026-israel/` |
| 1 | 0 | 16.0 | פרויקטים בתכנון | `/projects/אור-גנים/` |
| 1 | 0 | 9.0 | פרויקטים בתכנון | `/projects/יפת/` |
| 1 | 0 | 30.0 | פרויקטים בתכנון | `/projects/?city=באר שבע` |
| 1 | 0 | 14.0 | קירוי איילון הדמיה | `/tel-aviv-plans/ayalon-roof/` |
| 1 | 0 | 9.0 | שדה דב הדמיה | `/sde-dov/` |
| 1 | 0 | 75.0 | תוכנה לתכנון קונסטרוקציה | `/glossary/פרימברה-p6/` |
| 1 | 0 | 13.0 | תכנון איטום | `/glossary/יועץ-איטום/` |
| 1 | 0 | 88.0 | תכנון בעסקאות נדל ן | `/my-rentals/` |
| 1 | 0 | 82.0 | תכנון בעסקאות נדל ן | `/site-map/` |
| 1 | 0 | 71.0 | תכנון הוצאות ברכישת דירה | `/apartment-purchase-cost-calculator/` |
| 1 | 0 | 11.0 | תכנון וביצוע מיזמי נדל"ן | `/projects/הקרן/` |
| 1 | 0 | 50.0 | תכנון וביצוע מיזמי נדל"ן | `/tel-aviv-plans/how-planning-works/` |
| 1 | 0 | 10.0 | תכנון ובנייה | `/glossary/תקנות-התכנון-והבנייה-רישוי-בנייה-תשע/` |
| 1 | 0 | 12.0 | תכנון מבנים מתועשים | `/glossary/precast-element/` |
| 1 | 0 | 33.0 | תקנות התכנון והבניה בקשה להיתר | `/glossary/תקנות-התכנון-והבנייה-בקשה-להיתר-תנאיו/` |
| 1 | 0 | 50.0 | תקנות התכנון והבניה טופס 4 גישה לגג | `/real-estate-lawyer/form-4-occupancy-permit/` |
| 1 | 0 | 22.0 | תקנות התכנון והבנייה בקשה להיתר תנאיו ואגרות | `/glossary/תקנות-התכנון-והבנייה-בקשה-להיתר-תנאיו/` |

Raw source: the full 9,737-row export stays in the session scratchpad; only the filtered rows are copied here.
