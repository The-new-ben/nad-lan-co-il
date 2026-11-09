# Keyword map and heading DNA for /projects/ (proposal, 9.11.2026)

Inputs: `serp.md`, `autocomplete.md`, `related.md`, `volumes.md`, and the site's own protected-keyword registry (`docs/seo/protected-keywords.json`, built 26.10.2026), which already names `/projects/` as owner of the core heads.
Rules applied: one phrase, one owner page; never trade a page that ranks for a guess; no redirects; no new URL without `tools/gsc/url_word_audit.py` and Ben's word; indexing decisions stay with Ben.

---

## 1. Owned by /projects/ (the hub)

Volumes are Google Ads monthly averages (see `volumes.md`); "n/m" = not measured this time.

| Group | Head phrase | Synonyms and variants the hub also carries | Volume | Registry |
|---|---|---|---|---|
| Core | **פרויקטים חדשים** | פרויקטים חדשים בישראל, פרויקט חדש, פרויקטים חדשים למגורים | 390 | owner /projects/ |
| Core | **דירות חדשות** | דירות חדשות למכירה (260), דירה חדשה (110) | 210 | owner /projects/ |
| Core | **דירות מקבלן** | דירה מקבלן (210), דירות חדשות מקבלן (170), דירה חדשה מקבלן (140), דירות למכירה מקבלן (30) | 210 | owner /projects/ |
| Core | פרויקטים בשיווק | פרויקטים חדשים בשיווק | 50 | new |
| Stage | **דירות על הנייר** | פרויקטים חדשים על הנייר (170), דירות על הנייר למכירה (140), פרויקטים על הנייר (50) | 210 | owner /projects/ |
| Stage | פרויקטים בפריסייל | דירות פריסייל (90), פרויקטים פריסייל (70). Not the bare "פריסייל" (mixed intent) | 160 | new |
| Stage | **דירות לאכלוס מיידי** (national) | דירות מקבלן לאכלוס מיידי, פרויקטים לאכלוס מיידי, דירות חדשות לאכלוס מיידי (90), דירות מוכנות מקבלן, פרויקטים מאוכלסים | 90+ (rest n/m) | new. **See the rule in section 3** |
| Deals | **דירות מקבלן במבצע** | פרויקטים חדשים במבצע, מבצעים דירות מקבלן, מבצעי קבלן, דירות מקבלן בהנחה, דירות אחרונות מקבלן | n/m | new |
| Terms | דירות 20 80 (the list side) | דירות מקבלן 20 80, פרויקטים 20 80, 10 90, ללא הצמדה | n/m | new |
| Budget | **דירות חדשות עד 1.2 מיליון** | פרויקטים חדשים עד 2 מיליון (140), דירות חדשות עד 2 מיליון, עד 1.5 / מיליון וחצי (70), עד מיליון שקל (50) | 320 | new; the hub's FAQ already wins snippets here |
| Region | פרויקטים חדשים במרכז | בצפון (50), בדרום, בשרון, במרכז הארץ, בירושלים והסביבה | 70 | new |
| City | פרויקטים חדשים בתל אביב | פרויקטים חדשים בתל אביב מחירים (50), דירות חדשות בתל אביב (90) | 320 | owner /projects/ (keep) |
| City | פרויקטים חדשים ב&lt;עיר&gt; for every city **without** its own page | ירושלים 480, פתח תקווה 260, ראשון לציון / חיפה / אשדוד / רחובות 210 each … | about 10,400 in total | new; served by the city filter and city chips with counts |
| Near | פרויקטים חדשים קרוב אליי | פרויקטים חדשים לידי (tool label only) | n/m | new |
| Market | מחירי דירות חדשות | דירות חדשות שנותרו למכירה, חודשי היצע | n/m | new |

**Do not target on the hub:** דירה לידי (a song), דירות למכירה (owner `/properties/`), מחיר למשתכן / דירה בהנחה (owner `/dira-behanacha/`), rentals ("דירות מקבלן להשכרה", "דירות חדשות להשכרה"; owner `/properties/` or the rentals module), competitor brands (מדלן, יד 1, יד 2).

## 2. Owned by child pages (their own city or project topic only)

| Page | Owns | Must not lead with |
|---|---|---|
| `/new-projects/new-projects-tel-aviv/` | אכלוס מיידי בתל אביב, דירות חדשות לאכלוס מיידי תל אביב, דירות חדשות באכלוס מיידי בתל אביב, and for now the bare "אכלוס מיידי" / "דירות באכלוס מיידי", where it already ranks on page one | "פרויקטים חדשים" as a head (registry gives "פרויקטים חדשים בתל אביב" to the hub) |
| `/new-projects/north-tel-aviv-new-projects/` | פרויקטים חדשים בצפון תל אביב (20), הצפון הישן / החדש / בבלי / כוכב הצפון / רמת אביב as project areas | **Registry conflict:** the registry names `/projects/` as owner of "פרויקטים חדשים בצפון תל אביב" while this page carries it in title and H1. Recommendation: make this page the owner (exact topic) and update the registry. Ben decides |
| `/herzliya-projects/` | פרויקטים חדשים בהרצליה (110), פרויקטים בהרצליה (70), הרצליה פיתוח, המרינה, על הנייר בהרצליה | the generic "פרויקטים על הנייר" |
| `/sde-dov/` and its compound pages | שדה דב פרויקטים (390), פרויקט שדה דב מחירים (110), compound names | generic heads |
| `/projects/<project>/` (Duo, H Infinity, Rainbow, `/projects/hamedina/` …) | the project's name, "פרויקט X מחירים" (e.g. פרויקט כיכר המדינה 170) | generic heads |
| `/new-projects/` (the buying-from-a-developer guide) | קניית דירה מקבלן, מה בודקים בדירה מקבלן, דירה על הנייר (singular, informational: 210), קניית דירה על הנייר (50), עסקה 20 80 / קניית דירה 20 80 (the explanation) | any list, finder or "פרויקטים חדשים" head; it should link to the hub with the exact phrase "פרויקטים חדשים" |
| `/buying-apartment/` | קניית דירה and its stages | new-projects heads |
| `/apartment-prices/` and city price pages | מחירי דירות, מחירי דירות ב&lt;עיר&gt;, and "מחירי דירות חדשות ב&lt;עיר&gt;" where a city price page exists | the national new-projects heads |
| `/urban-renewal/`, `/urban-renewal/map/` | פינוי בינוי, התחדשות עירונית, פרויקטי פינוי בינוי, the 975 compounds in planning | "פרויקטים חדשים" |
| `/glossary/tofes-4/` | טופס 4, אישור אכלוס | "אכלוס מיידי" |
| Home `/` | נדל״ן, נדלן | "פרויקטים חדשים" as its first phrase (today it is in the title and H1; keep it second and link to the hub, change only after the keyword-guard check and Ben's word) |

Future city project pages for Jerusalem, Petah Tikva, Rishon, Haifa, Ashdod and Rehovot (210-480 a month each) would win more than a hub filter. They are new URLs: run `url_word_audit.py`, then ask Ben. The old `/city/<city>/projects/` pages are 410 and must stay as they are (no redirects).

## 3. The immediate-occupancy rule (protects the one page that ranks)
- The Tel Aviv page is the only nad-lan page on page one in this family, on 5 immediate-occupancy result pages, and Google localises the bare phrase to Tel Aviv.
- So the hub carries **"דירות לאכלוס מיידי"** in an **H2, a filter chip and the answer paragraph**, with a national count. It does **not** put "אכלוס מיידי" in its title or H1 for now.
- The hub's immediate-occupancy section links to the Tel Aviv page with the anchor "דירות חדשות לאכלוס מיידי בתל אביב".
- Re-check with page-level Search Console data about 6 weeks after release. If the hub starts ranking for the bare phrase while the Tel Aviv page holds its places, the title can be widened then.

---

## 4. Heading DNA (rendered order: phones first)

Order law: H1 → answer paragraph → CTAs (the filter bar) → the list → map → facts → tools → article → FAQ.

**Title (about 55 characters):** פרויקטים חדשים ודירות מקבלן 2026: מחירים, על הנייר ומבצעים | נדלן
**Meta description (built from live counts and a check date):** "566 פרויקטים בשיווק, 348 עם מחיר 'החל מ' שפרסם היזם, 85 באכלוס מיידי או קרוב, 39 בפריסייל ו־64 עם מבצע או תנאי תשלום. סינון לפי עיר, תקציב ושלב, ומחיר העסקאות בכל עיר." (the numbers are today's `projects-market.json`; print them from the data, never by hand)

**H1:** פרויקטים חדשים ודירות חדשות מקבלן בישראל

**Answer paragraph (2-3 sentences, before anything technical):**
How many projects are on the market today, split by stage (on paper / presale, marketing and construction, near occupancy, immediate occupancy), how many have a published starting price, and that next to each price we show what flats in the same city really sold for. One line sends owners of old buildings to the urban-renewal guide.
This is the "count + filter" pattern Google rewards on Yad2 and Madlan, with something neither has: the deal price beside the marketing price.

**CTA bar:** stage chips (על הנייר / פריסייל · בשיווק ובבנייה · אכלוס קרוב · אכלוס מיידי), budget ceiling (עד 1.2M · 1.5M · 2M · 3M · ללא), city with counts, rooms, "במבצע", "קרוב אליי", "התראה על פרויקטים חדשים".

**H2 set (proposed wording):**
1. פרויקטים בשיווק עכשיו: מחיר החל מ, חדרים, שלב ומועד מסירה (the main list and table)
2. דירות לאכלוס מיידי ואכלוס קרוב בכל הארץ
3. פרויקטים על הנייר ופריסייל: כמה חוסכים ומה הסיכון
4. דירות מקבלן במבצע: 20/80, ללא הצמדה ודחיית תשלום, וכמה זה שווה בשקלים
5. דירות חדשות לפי תקציב: עד 1.2 מיליון, עד 2 מיליון ומעלה
6. פרויקטים חדשים לפי אזור ועיר (מרכז, שרון, ירושלים, צפון, דרום; city chips with counts)
7. פרויקטים חדשים קרוב אליי (the near-me tool)
8. מחירי דירות חדשות לפי עיר: מחיר השיווק מול מחיר העסקאות
9. שוק הדירות החדשות החודש: מלאי, מכירות וחודשי היצע (dated; answers the news intent the AI box reaches for)
10. לפני שחותמים: מחשבונים ובדיקות לדירה מקבלן (the 7 existing tools, kept)
11. מתחמי פינוי בינוי ותמ״א 38 בתכנון (the 975 compounds, kept, relabelled and moved below the buying list; link to `/urban-renewal/`)
12. שאלות נפוצות על פרויקטים חדשים ודירות מקבלן (keep the questions Google already quotes; add: מה ההבדל בין אכלוס מיידי לאכלוס קרוב, כמה שווה מבצע 20/80, איפה יש דירות חדשות עד 1.2 מיליון, איך יודעים שמחיר הקבלן גבוה מדי)

**Word rules from the research**
- Use the **"ל"** form: "לאכלוס מיידי" (Google rewrites "באכלוס" to it; suggest only lives in this form).
- Say "דירות חדשות" next to "פרויקטים חדשים" in the H1 and the first paragraph (as word families, "דירות חדשות" is about 2.5 times larger in Trends).
- Name budgets as people type them: "עד 1.2 מיליון", "עד 2 מיליון", "עד מיליון שקל".
- Deals by their real names: "20/80", "10/90", "ללא הצמדה למדד", "דחיית תשלום", "ריהוט מתנה". Never invent a deal; print the developer's text, its source and its check date.
- Every count, price and date on the page is printed from data with a "נכון ל־" date. Unknown stays out.
