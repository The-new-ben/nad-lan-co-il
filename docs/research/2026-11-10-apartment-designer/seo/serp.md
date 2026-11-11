# Google Israel SERP DNA: apartment design hub (HAD-701)

Captured 10.11.2026, 20:39 to 20:55 Israel time, on google.co.il with `hl=iw&gl=il`, desktop, in the owner's Chrome (device gmktec), signed-in profile. One page of results per query. Raw JSON per query: `serp-raw/serp-desktop-*.json`.

## How this was captured, and what is missing

- **DataForSEO could not be used.** The account balance on 10.11.2026 is -$0.0013; every paid call returns `40200 Payment Required` (checked with `appendix/user_data` and one autocomplete call, both free). So there is **no** DataForSEO SERP JSON, **no** Google Ads volume, and **no mobile SERP** in this pack. Money spent: **$0.00**.
- SERPs were read manually in the owner's Chrome, as the `google-israel-manual-search` skill prefers. A small script in the page extracted organic titles and URLs, People Also Ask (`data-q`), related searches (אנשים חיפשו גם), the AI block (Google Israel labels it **תקציר מ-AI**), its source links, ads and module flags. No CAPTCHA appeared.
- Mobile: the browser tool cannot change the user agent, so mobile SERPs were not captured. Next run, after a DataForSEO top-up: `serp_research.py` with `m:` prefixes.
- AI block sources: the script collects every outbound link inside the AI block container. For `עיצוב דירה` the container also held the image pack, so its source list includes image results (noted in the raw file).
- Organic results per page were 7 to 9 (Google Israel now shows fewer blue links on page 1).

## Cost ledger (DataForSEO and other paid calls)

| # | Call | Result | Cost |
|---:|---|---|---:|
| 1 | GET /v3/appendix/user_data (script) | balance -0.0013 USD | $0 (free endpoint) |
| 2 | POST /v3/serp/google/autocomplete/live/advanced, `עיצוב דירה` (script) | HTTP 402, 40200 Payment Required | $0 |
| 3 | Same call through the dataforseo MCP tool | 40200 Payment Required | $0 |
| 4 | Google Ads Keyword Planner in the owner's Chrome | no Google Ads account on the signed-in profile; stopped, nothing created | $0 |
| | **Total** | | **$0.00** |

Free sources used instead: Google's public autocomplete endpoint (the one the browser calls; `client=chrome&hl=iw&gl=il`, 888 requests, 0 errors, paced at about 3 per second), manual SERP reading in the owner's Chrome (23 queries), and plain page fetches with a desktop Chrome user agent.

## DNA in one screen

| Query | AI block | PAA | Who wins page 1 | Dominant title pattern |
|---|---|---|---|---|
| עיצוב דירה | yes | - | magazines (bvd, baitvenoy, mako), designer portfolios, Pinterest | עיצוב דירות - ... / איך לעצב את הבית לבד? |
| עיצוב פנים | yes | - | Wikipedia, magazines (bvd, pnim), designer homepages, OpenU studies | brand + עיצוב פנים |
| מעצב פנים | yes | - | designer homepages + directories (midrag, shiplus, daniel-m) | מעצב/ת פנים ב<עיר> / מעצבות פנים מומלצות |
| מעצבת פנים | yes | - | designer homepages + midrag + shiplus | <שם> מעצבת פנים - ... |
| מעצב פנים מחיר | yes | - | price guides: midrag, 6 designer/college blogs, Facebook group | כמה עולה מעצבת פנים? ... 2026 |
| כמה עולה מעצב פנים | yes | 4 | same set as מעצב פנים מחיר (+ sdsd contractor-apartment cost) | כמה עולה מעצבת פנים? / כמה עולה עיצוב פנים? |
| מחיר מעצבת פנים למטר | yes | - | same set as מעצב פנים מחיר | כמה עולה מעצבת פנים? 150-450 ₪ למ"ר (מחירון 2026) |
| ייעוץ עיצוב | no | - | designer service pages for a consultation meeting + midrag | פגישת ייעוץ עיצוב פנים ... |
| ייעוץ עיצוב פנים מחיר | yes | - | the price set again (midrag, shimrit, inandout, ultimaschool, mayakedem) + zirat one-time consult | כמה עולה ... / ייעוץ עיצוב פנים חד-פעמי: מה מקבלים, כמה זה עולה |
| עיצוב דירה בתלת מימד | yes | - | AI/3D SaaS (aihouse, redesignai) + rendering studios | הדמיות תלת מימד ... / המדריך המלא לעיצוב הבית בתלת מימד |
| תכנון דירה | yes | - | designer article, contractor-apartment planner, online planning service, ArcGIS (דירה להשכיר) | תכנון דירה - ... איך מתכננים נכון |
| הדמיה לדירה | yes | 4 | rendering studios | הדמיות / הדמיית בתים |
| שרטוט דירה אונליין | yes | - | AI tools (redesignai, aihouse, luw, genroom, roomsgpt, capcut) + IKEA planners | שרטוט AI חינמי ... / כלי תכנון אונליין |
| אפליקציה לעיצוב דירה | yes | - | app stores (Google Play x2, App Store), homeplanner, capcut, shiplus | <app> - אפליקציות ב-Google Play |
| תוכנה לעיצוב דירה | yes | 4 | bvd list article, app stores, IKEA, redesignai, genroom | 16 תוכנות לעיצוב הבית / 5 כלי עיצוב חדרים AI חינמיים |
| עיצוב דירה ai | yes | - | AI tools (redesignai, genroom, Adobe Firefly, roomsgpt) | עיצוב פנים AI ... חינם |
| עיצוב דירה קטנה | yes | - | Pinterest, ynet guide, bvd, pickinteri, IKEA | המדריך הגדול/השלם לעיצוב דירה קטנה |
| עיצוב דירה חדשה מקבלן | yes | - | designer service pages + midrag tip | עיצוב דירת קבלן ... |
| שינויי דיירים | yes | 4 | tenant-change coordinators | שינויי דיירים ... מדריך / ליווי |
| תכנון מטבח | yes | 4 | kitchen makers' guides + IKEA planner + midrag | תכנון מטבח ... המדריך |
| עיצוב סלון | yes | - | Pinterest, WALLS, IKEA rooms, ida-home, genroom AI, pickinteri, bvd | עיצוב סלון: 60 סלונים מעוצבים לפי סגנון |
| הום סטיילינג | yes | 4 | stylists + courses (Shenkar, my-college) + midrag price | הום סטיילינג: הלבשת הבית ... |
| אדריכל או מעצב פנים | yes | - | comparison articles by designers + shiplus + forum | אדריכל או מעצב פנים - את מי ... צריכים? |

### What the DNA says

1. **Price is one intent.** `מעצב פנים מחיר`, `כמה עולה מעצב פנים`, `מחיר מעצבת פנים למטר` and `ייעוץ עיצוב פנים מחיר` return the same URLs (midrag 15364, shimrit pricing guide, studio-id, meitalyaakov, inandout, ultimaschool, mayakedem). One owner page for all of them.
2. **Consulting as a service is a different SERP.** `ייעוץ עיצוב` (no price word) returns service pages for a consultation meeting and has no AI block. Its price question folds into the price intent.
3. **Tool intents cluster.** `עיצוב דירה בתלת מימד`, `תוכנה לעיצוב דירה`, `אפליקציה לעיצוב דירה`, `שרטוט דירה אונליין`, `עיצוב דירה ai` share redesignai, genroom, roomsgpt, aihouse, IKEA planners and app-store pages. No Israeli real-estate site appears. An in-page planner that works in Hebrew is the answer type Google already rewards here.
4. **Nobody on page 1 combines tool + price + guide.** The magazines have inspiration, the designers have service pages, the SaaS tools have a tool, midrag has prices. That gap is the hub's opening.
5. **AI blocks quote prices with sources.** For the price queries the AI block lists consultation, hourly, per-room and per-apartment ranges and cites meitalyaakov, studio-id, ultimaschool, midrag, sdsd, inandout, ziratadrichalut, shimrit. A clear dated price table with its basis is what gets cited.
6. **PAA appears rarely** (6 of 23 queries). The questions that do appear are recorded below and used in heading-evidence.md.
7. **Facebook groups rank on price and app queries** (home4y group posts). Real people ask: how much for a 3-storey house, which app is accurate. The page should answer those concrete cases.
8. **Ads are thin:** only moransofer.co.il on `עיצוב דירה` and `עיצוב פנים`. Low commercial ad pressure on these heads.

## People Also Ask (verbatim)

- **כמה עולה מעצב פנים**: כמה עולה לעצב מטבח? / כמה מרוויח מעצב פנים בממוצע? / מה המחיר של אדריכלות ועיצוב פנים? / מה המחירים של הום סטיילינג?
- **הדמיה לדירה**: איפה אפשר למצוא משרדי עיצוב פנים? / איפה הכי טוב ללמוד עיצוב פנים בישראל? / מה המחיר של ייעוץ עיצוב פנים? / מהו עיצוב פנים?
- **תוכנה לעיצוב דירה**: מהי תוכנה טובה לעיצוב חדר? / מהי תוכנה טובה לעיצוב פנים? / מהי תוכנה טובה לעיצוב מטבחים? / מהי תוכנה לעיצוב הבית בחינם בעברית?
- **שינויי דיירים**: מה המחיר של שינויי דיירים? / מהי האחריות של הקבלן על הדירה לפי חוק המכר? / מהו פינוי בינוי? / האם קיים מחירון דקל לשינויי דיירים בפורמט PDF?
- **תכנון מטבח**: מהי תוכנה טובה לעיצוב מטבח? / מהו הגובה הסטנדרטי של ארונות מטבח מהרצפה? / מהם כלי תכנון המטבח של איקאה? / איך לתכנן מטבח?
- **הום סטיילינג**: האם יש קורס הום סטיילינג קצר? / האם יש קורס הום סטיילינג אונליין? / איפה הכי כדאי ללמוד עיצוב פנים בישראל? / כמה עולה קורס הום סטיילינג?

## Related searches, אנשים חיפשו גם (verbatim)

- **עיצוב דירה**: עיצוב דירה ai · עיצוב דירה 120 מטר · עיצוב פנים דירות · עיצוב בתים פרטיים תמונות · עיצוב פנים מגזין · אתר עיצוב פנים · בניין ודיור דירות מעוצבות · עיצוב דירה קטנה
- **עיצוב פנים**: עיצוב פנים לימודים · עיצוב פנים תמונות · עיצוב פנים לבית · אתר עיצוב פנים · עיצוב פנים ai · עיצוב פנים מגזין · עיצוב פנים באנגלית · עיצוב פנים מחיר
- **מעצב פנים**: מעצב פנים לימודים · מעצב פנים מומלץ · מעצבי פנים מובילים בישראל · עיצוב פנים יוקרתי · מעצב פנים מחיר · עיצוב פנים לבית · מעצבת פנים במרכז · דניאל מעצב פנים
- **מעצבת פנים**: מעצבת פנים לימודים · מעצבת פנים במרכז · מעצבת פנים מחיר · מעצבת פנים מומלצת במרכז · מעצבת פנים חרדית · מעצבת פנים בירושלים · מעצבת פנים מתחילה · מעצבת פנים תל אביב
- **מעצב פנים מחיר**: דוגמא להצעת מחיר עיצוב פנים · מעצבת פנים מומלצת · מעצבת פנים שכר · מעצבת פנים מתחילה · מעצבת פנים בירושלים · כמה מרוויחה מעצבת פנים עצמאית · מעצבת פנים מידרג · מיכל מעצבת פנים
- **כמה עולה מעצב פנים**: דוגמא להצעת מחיר עיצוב פנים · מעצבת פנים מומלצת · כמה מרוויחה מעצבת פנים עצמאית · מעצבת פנים בירושלים · מעצבת פנים מתחילה · מעצבת פנים שכר · מידרג עיצוב פנים · מיכל מעצבת פנים
- **מחיר מעצבת פנים למטר**: דוגמא להצעת מחיר עיצוב פנים · מעצבת פנים מומלצת · עלות מעצבת פנים · מעצבת פנים מתחילה · מעצבת פנים שכר · מעצבת פנים בירושלים · מעצבת פנים מידרג · מיכל מעצבת פנים
- **ייעוץ עיצוב**: פגישת ייעוץ עיצוב פנים מחיר · אתר עיצוב פנים · עיצוב פנים סלון חרדי · אדריכלית פנים · מעצבת · מעצבת פנים במרכז · מעצבי פנים · מגזין דיור
- **ייעוץ עיצוב פנים מחיר**: דוגמא להצעת מחיר עיצוב פנים · מעצבת פנים מומלצת · מידרג עיצוב פנים · מעצבת פנים שכר · מחיר עיצוב מטבח · מעצבת פנים מתחילה · מעצבת פנים בירושלים · כמה מרוויחה מעצבת פנים עצמאית
- **עיצוב דירה בתלת מימד**: עיצוב תלת מימד אונליין · הדמיית דירה תלת מימד חינם · תוכנה לעיצוב הבית חינם בעברית · עיצוב תלת מימד חינם · תוכנת שרטוט תלת מימד עברית · תוכנת עיצוב פנים חינמית · תוכנת עיצוב פנים של גוגל · שרטוט דירה אונליין
- **תכנון דירה**: שרטוט אדריכלי של דירה · תמל 3010 מנהל התכנון · אפליקציה לתכנון דירה · תוכניות אדריכליות בחינם · איתור תוכנית דירה · תמל 3011 גדרה · תמל 3015 ראשון לציון · תוכנית אדריכלית לדוגמא
- **הדמיה לדירה**: הדמיות אדריכליות · הדמיות תלת מימד · הדמיות אדריכליות ai · הדמיות עיצוב פנים · חברת הדמיות · הדמיות עיצוב פנים אונליין · משרד הדמיות · הדמיות ריאליסטיות
- **שרטוט דירה אונליין**: Ai לעיצוב הבית חינם · תכנון אדריכלי ai חינם · הדמיית חדר אונליין · תכנון מטבח אונליין איקאה · תכנון ארון אונליין · תוכנה לעיצוב הבית חינם בעברית · עיצוב פנים ai בחינם · עיצוב תלת מימד אונליין
- **אפליקציה לעיצוב דירה**: תוכנה לעיצוב הבית חינם בעברית · אפליקציה לעיצוב הבית חינם · אפליקציה לעיצוב הבית בעברית · Ai לעיצוב הבית חינם · אפליקציה לעיצוב הבית ai · תוכנה לעיצוב חדר חינם · עיצוב פנים ai בחינם · תוכנת עיצוב פנים של גוגל
- **תוכנה לעיצוב דירה**: אפליקציה לעיצוב הבית חינם · אפליקציה לעיצוב הבית בעברית · Ai לעיצוב הבית חינם · תוכנה לעיצוב הבית להורדה חינם · אפליקציה לעיצוב פנים חינם · אפליקציה לעיצוב הבית ai · תוכנה לעיצוב חדר חינם · אפליקציה לעיצוב חדר
- **עיצוב דירה ai**: Ai לעיצוב הבית חינם · רידיזיין ai · תוכנה לעיצוב הבית חינם בעברית · עיצוב AI בחינם · תכנון אדריכלי ai חינם · הדמיית מטבח ai חינם · עיצוב מטבח ai · אפליקציית ai לעיצוב הבית חינם
- **עיצוב דירה קטנה**: עיצוב דירה קטנה 50 מטר · עיצוב דירה קטנה 30 מטר · עיצוב דירות קטנות 70 מטר · איקאה עיצוב דירה קטנה · עיצוב דירות קטנות 40 מ ר · עיצוב דירת חדר קטנה · עיצוב בתים קטנים תמונות · עיצוב דירת סטודיו קטנה
- **עיצוב דירה חדשה מקבלן**: עיצוב דירת קבלן 5 חדרים · עיצוב דירת קבלן 4 חדרים · עיצוב דירת קבלן 3 חדרים
- **שינויי דיירים**: שינויי דיירים דרושים · קורס שינויי דיירים · מחירון דקל שינויי דיירים · פתיחת תיק שינויי דיירים · מתאמת שינויי דיירים שכר · תיאום שינויי דיירים · שינויי דיירים בדירה מקבלן · טיפים לשינויי דיירים
- **תכנון מטבח**: תכנון מטבח אונליין · תכנון מטבח אונליין איקאה · כלי תכנון מטבח · תכנון מטבח תוכנה חינם · תכנון מטבח מידות · כלי תכנון מטבח איקאה · עקרונות תכנון מטבח · תכנון מטבח קטן
- **עיצוב סלון**: עיצוב סלון מודרני יוקרתי · פינטרסט עיצוב סלון מודרני · עיצוב סלון תמונות · עיצוב סלון מודרני תמונות · פינטרסט עיצוב סלון קטן · עיצוב סלון מאורך · עיצוב סלון 2026 · עיצוב סלון גדול
- **הום סטיילינג**: הום סטיילינג חנות · קורס הום סטיילינג אונליין · הום סטיילינג מומלצים · לימודי הום סטיילינג המלצות · קורס הום סטיילינג ירושלים · מעצבת הום סטיילינג · הום סטיילינג דרושים · הום סטיילינג מחירים

## Per-query results

### עיצוב דירה

Captured 2026-11-10T20:40:04.398Z · modules: images, videos, alsoSearched · ads: www.moransofer.co.il

| # | Title (verbatim) | URL |
|---:|---|---|
| 1 | עיצוב דירות - המדור שיעזור לכם לעשות את זה נכון | https://www.bvd.co.il/design-homes/apartments/ |
| 2 | עיצוב פנים מקבל כיוון דרך חדרים, חומרים וסיפורי בתים שונים | https://www.baitvenoy.co.il/עיצוב |
| 3 | 88 רעיונות של עיצוב | עיצוב, דירה קטנטנה, פנים המשרד | https://www.pinterest.com/kerenorharl0082/עיצוב/ |
| 4 | מעצבת פנים הדר דור (Dordesign) – עיצוב פנים מרהיב, מעל 20 שנות ... | https://www.dordesign.co.il/ |
| 5 | צפון תל אביב: אח ואחות, שני סגנונות שונים ודירה אחת | https://www.mako.co.il/living-architecture/local/Article-8482bea0a7fb1a1026.htm |
| 6 | איך לעצב את הבית לבד? מדריך פרקטי לעיצוב פנים עצמאי בסטייל | https://www.rossetto.co.il/איך-לעצב-את-הבית-לבד/ |
| 7 | עיצוב פנים מודרני יוקרתי - נטע לי וטל נוי - Neta-li and Tal Noy | https://netalinoy.com/project_cat/עיצוב-פנים-מודרני-יוקרתי/ |
| 8 | עיצוב דירות | עיצוב פנים לדירה עם מעצבי פנים מומחים | https://www.keinan-arch.com/project_type/עיצוב-פנים/עיצוב-דירות/ |

**AI block (תקציר מ-AI)**, first lines: עיצוב דירות הוא תהליך של תכנון, ארגון והלבשת החלל במטרה ליצור סביבת מגורים פונקציונלית, נוחה ואסתטית המותאמת לאורח החיים של הדיירים. שמרית אוחיון עקרונות מרכזיים בעיצוב דירות תכנון פונקציונלי: התאמת החלל לצרכים היומיומיים (כמו משולש עבודה במטבח, פתרונות אחסון נסתרים וזרימה נכונה בין החדרים). בחירת סגנון עיצובי: גיבוש שפה אחידה לדירה – כגון מודרני, נורדי (סקנדינבי), כפרי, תעשייתי, וואבי-סאבי או אקלקטי. חומריות ותאורה:...

AI block links: shimrit-design.co.il, bvd.co.il, ida-home.co.il, baitvenoy.co.il, youtube.com, instagram.com, pinterest.com, keinan-arch.com, benshoam.com, shirleystein.co.il, asafurniture.co.il, bettyj.co.il, smb-arch.com, midrag.co.il, lirazbdesign.co.il

### עיצוב פנים

Captured 2026-11-10T20:41:12.899Z · modules: images, videos, local, alsoSearched · ads: www.moransofer.co.il

| # | Title (verbatim) | URL |
|---:|---|---|
| 1 | עיצוב פנים | https://he.wikipedia.org/wiki/עיצוב_פנים |
| 2 | מעצב פנים ניצן הורוביץ - עיצוב פנים דירות יוקרה | עיצוב בתי יוקרה | https://nhdesign.co.il/ |
| 3 | בניין ודיור | המגזין המוביל לאדריכלות, עיצוב פנים, עיצוב הבית | https://www.bvd.co.il/ |
| 4 | PNIM | מגזין עיצוב פנים ואדריכלות בישראל | https://www.pnim.co.il/ |
| 5 | עיצוב פנים ואדריכלות [פרוייקטים 2026] מעצבת פנים ענבל ברקוביץ | https://www.design-inbal.co.il/ |
| 6 | Neta-li & Tal Noy - עיצוב פנים ואדריכלות ברמה מתקדמת | https://netalinoy.com/ |
| 7 | מעצבת פנים הדר דור (Dordesign) – עיצוב פנים מרהיב, מעל 20 שנות ... | https://www.dordesign.co.il/ |
| 8 | המרכז ללימודי עיצוב פנים | דיפלומה | https://www.openu.ac.il/diploma/diploma-13_1.html |

**AI block (תקציר מ-AI)**, first lines: עיצוב פנים הוא המקצוע והאמנות של תכנון, ארגון ושיפור חללים פנימיים בבניינים (כמו דירות, בתים פרטיים, משרדים וחללים מסחריים) כדי ליצור סביבה נוחה, בריאה, פונקציונלית ואסתטית. ויקיפדיה +1 מה כולל תהליך עיצוב הפנים? תכנון וחלוקת מרחב: שרטוט והעמדה של קירות, פתחים ורהיטים בהתאם לצרכי הדיירים או המשתמשים. חומרים ותאורה: בחירה של ריצוף, חיפויים, בדים, צבעים ופתרונות תאורה שמשפיעים על האווירה בחלל. נגרות בהתאמה אישית: תכנון...

AI block links: he.wikipedia.org, hit.ac.il, pnim.co.il, bvd.co.il

### מעצב פנים

Captured 2026-11-10T20:44 · modules: img, vid, local · ads: none

| # | Title (verbatim) | URL |
|---:|---|---|
| 1 | מעצב פנים בתל אביב והמרכז | https://www.niryefet.com/tel-aviv |
| 2 | מעצב פנים ניצן הורוביץ - עיצוב פנים דירות יוקרה | עיצוב בתי יוקרה | https://nhdesign.co.il/ |
| 3 | מעצבת פנים בתל אביב ובמרכז - נטע-לי וטל נוי | https://netalinoy.com/מעצבת-פנים-בתל-אביב/ |
| 4 | דניאל מיכאלי: נבחרת מעצבי פנים ואדריכלים מובילים בישראל | https://www.daniel-m.co.il/ |
| 5 | מעצבות פנים מומלצות - 4500 חוות דעת באתר ... | https://www.midrag.co.il/Content/SectorPortal/67 |
| 6 | ליעד יוסף מעצב פנים‎ (@liadyosef_designer) | https://www.instagram.com/liadyosef_designer/ |
| 7 | מעצבי פנים שבדקנו במרכז | https://www.shiplus.co.il/בעלי-מקצוע-כלליים/מעצבי-פנים/המרכז/ |
| 8 | PNIM | מגזין עיצוב פנים ואדריכלות בישראל | https://www.pnim.co.il/ |

**AI block (תקציר מ-AI)**, first lines: מעצב פנים הוא איש מקצוע המתמחה בתכנון, עיצוב וארגון של חללים פנימיים במבנים (כגון דירות, בתים פרטיים, משרדים, חנויות ומסעדות) כדי ליצור סביבה אסתטית, בטוחה ופונקציונלית המותאמת לצרכי הדיירים או המשתמשים. ויקיפדיה +1 מה כולל תפקידו של מעצב הפנים? תכנון החלל: חלוקה מחדש של חדרים, הזזת או הריסת קירות (במידת הצורך ובכפוף להנחיות הנדסיות), ותכנון מעברים ותנועה בחלל. התאמה תקציבית ולוחות זמנים: בניית תקציב מפורט לפרויקט, ק...

AI block links: he.wikipedia.org, ys-design.co.il, shiplus.co.il, midrag.co.il, daniel-m.co.il, facebook.com

### מעצבת פנים

Captured 2026-11-10T20:46 · modules: img, vid, local · ads: none

| # | Title (verbatim) | URL |
|---:|---|---|
| 1 | עיצוב פנים ואדריכלות [פרוייקטים 2026] מעצבת פנים ענבל ברקוביץ | https://www.design-inbal.co.il/ |
| 2 | יפעת ירושלמי - מעצבת פנים המתמחה בעיצוב פנים יוקרתי | https://www.yifatdesign.co.il/ |
| 3 | מעצבות פנים מומלצות - 4500 חוות דעת באתר ... | https://www.midrag.co.il/Content/SectorPortal/67 |
| 4 | sharondaviddesigner - שרון דוד / עיצוב פנים / מעצבת פנים | https://www.instagram.com/sharondaviddesigner/?hl=he |
| 5 | חיה אורצל מעצבת פנים - עיצוב פנים לדירות ולעסקים | https://www.chayaorzel.co.il/ |
| 6 | מעצבת פנים עם סגנון יוקרתי והתאמה אישית - אלה מורגן עיצוב פנים | https://www.elamorgan.co.il/ |
| 7 | מעצבת פנים | מורן רוזנברג מעצבת פנים לבתים בשלבי בנייה ושיפוץ | https://moranrozenberg.co.il/ |
| 8 | מעצבי פנים מומלצים בתל אביב והסביבה | https://www.shiplus.co.il/בעלי-מקצוע-כלליים/מעצבי-פנים/תל-אביב-יפו/ |

**AI block (תקציר מ-AI)**, first lines: מעצבת פנים היא אמונה על תכנון, הלבשה ועיצוב של חללים פנימיים בבתים, דירות, משרדים ועסקים, תוך התאמה של המבנה לצרכים הפרקטיים והאסתטיים של הלקוחות. חיה אורצל מעצבת פנים שירותים מרכזיים של מעצבת פנים תכנון ושיפוצים מקיפים: שינוי מבני של הבית, העמדת קירות, תכנון אינסטלציה, חשמל ותאורה. עיצוב דירות קבלן: ליווי בשינויי דיירים מול הקבלן ובחירת חומרי גמר (ריצוף, כלים סניטריים, מטבחים). הום סטיילינג (הלבשת הבית): בחירת ריהוט...

AI block links: chayaorzel.co.il, hilahstyling.com, tovicohen.com, bvd.co.il, midrag.co.il, instagram.com, design-inbal.co.il, mikapertsovsky.com, liz-zomer.com, yifatdesign.co.il

### מעצב פנים מחיר

Captured 2026-11-10T20:46 · modules: img, vid, local · ads: none

| # | Title (verbatim) | URL |
|---:|---|---|
| 1 | מעצבת פנים מחיר | כל המחירים של מעצבות פנים - במידרג | https://www.midrag.co.il/Content/Price/15364 |
| 2 | כמה עולה מעצבת פנים? מדריך מחירים ושירותים | https://www.shimrit-design.co.il/interior-design-pricing-guide |
| 3 | כמה עולה מעצבת פנים? 150-450 ₪ למ"ר (מחירון 2026) | https://studio-id.co.il/כמה-עולה-מעצבת-פנים/ |
| 4 | כמה עולה מעצבת פנים? מחירים שקופים ואמיתיים לשנת 2026 | https://meitalyaakov.co.il/interior-designer-cost-2026/ |
| 5 | כמה עולה עיצוב פנים? מחירון מלא וסקירת תקציב 2026 | https://inandout.co.il/interior-design-cost/ |
| 6 | כמה עולה לעצב דירה בשנת 2026? פירוט מחירים בישראל | https://ultimaschool.co.il/magazine/כמה-עולה-לעצב-דירה-בשנת-2026-פירוט-מחירים-ב/ |
| 7 | מנסה להבין עלויות... כמה עולה מעצב.ת פנים לשיפוץ בית 3 קומות, ... | https://www.facebook.com/groups/home4y/posts/3985757208359907/ |
| 8 | כמה עולה עיצוב פנים? המדריך המלא לתכנון התקציב (2026) | https://mayakedem.com/מאמרים/כמה-עולה-עיצוב-פנים/ |

**AI block (תקציר מ-AI)**, first lines: עלות מעצבת פנים בישראל משתנה בהתאם לסוג השירות, היקף הפרויקט ושיטת התמחור. מיטל יעקב - מעצבת פנים +1 לפי סוג שירות או גודל הנכס פגישת ייעוץ חד-פעמית: 300 – 1,000 ₪ (לעיתים מקוזז מהעלות הכוללת אם ממשיכים לחוזה). תמחור לפי שעה: 150 – 600 ₪ לשעה (מעצבים מתחילים: 150 – 250 ₪; מעצבים מנוסים או במרכז הארץ: 350 – 600 ₪). חדר בודד / הום סטיילינג נקודתי: 1,500 – 10,000 ₪. דירת 3 חדרים (~80 מ"ר): 20,000 – 35,000 ₪. דירת 4 חדרי...

AI block links: meitalyaakov.co.il, studio-id.co.il, ultimaschool.co.il, midrag.co.il, sdsd.co.il, inandout.co.il, ziratadrichalut.co.il, shimrit-design.co.il, liz-zomer.com, qualityinteriordesign.com

### כמה עולה מעצב פנים

Captured 2026-11-10T20:47 · modules: paa_by_data_q, img, vid · ads: none

| # | Title (verbatim) | URL |
|---:|---|---|
| 1 | מעצבת פנים מחיר | כל המחירים של מעצבות פנים - במידרג | https://www.midrag.co.il/Content/Price/15364 |
| 2 | כמה עולה מעצבת פנים? מדריך מחירים ושירותים | https://www.shimrit-design.co.il/interior-design-pricing-guide |
| 3 | כמה עולה מעצבת פנים? 150-450 ₪ למ"ר (מחירון 2026) | https://studio-id.co.il/כמה-עולה-מעצבת-פנים/ |
| 4 | עלות מעצב פנים לדירת קבלן 2026 | מדריך מחירים | https://sdsd.co.il/interior-designer-for-contractor-apartment-cost/ |
| 5 | מנסה להבין עלויות... כמה עולה מעצב.ת פנים לשיפוץ בית 3 קומות, ... | https://www.facebook.com/groups/home4y/posts/3985757208359907/ |
| 6 | כמה עולה עיצוב פנים? מחירון מלא וסקירת תקציב 2026 | https://inandout.co.il/interior-design-cost/ |
| 7 | כמה עולה לעצב דירה בשנת 2026? פירוט מחירים בישראל | https://ultimaschool.co.il/magazine/כמה-עולה-לעצב-דירה-בשנת-2026-פירוט-מחירים-ב/ |
| 8 | כמה עולה מעצבת פנים? מחירים שקופים ואמיתיים לשנת 2026 | https://meitalyaakov.co.il/interior-designer-cost-2026/ |
| 9 | כמה עולה עיצוב פנים? המדריך המלא לתכנון התקציב (2026) | https://mayakedem.com/מאמרים/כמה-עולה-עיצוב-פנים/ |

**AI block (תקציר מ-AI)**, first lines: עלות מעצבת פנים בישראל משתנה בהתאם לסוג השירות, היקף הפרויקט ושיטת התמחור. מיטל יעקב - מעצבת פנים +1 לפי סוג שירות או גודל הנכס פגישת ייעוץ חד-פעמית: 300 – 1,000 ₪ (לעיתים מקוזז מהעלות הכוללת אם ממשיכים לחוזה). תמחור לפי שעה: 150 – 600 ₪ לשעה (מעצבים מתחילים: 150 – 250 ₪; מעצבים מנוסים או במרכז הארץ: 350 – 600 ₪). חדר בודד / הום סטיילינג נקודתי: 1,500 – 10,000 ₪. דירת 3 חדרים (~80 מ"ר): 20,000 – 35,000 ₪. דירת 4 חדרי...

AI block links: meitalyaakov.co.il, studio-id.co.il, ultimaschool.co.il, midrag.co.il, sdsd.co.il, inandout.co.il, ziratadrichalut.co.il, shimrit-design.co.il

### מחיר מעצבת פנים למטר

Captured 2026-11-10T20:54 · modules: img, vid · ads: none

| # | Title (verbatim) | URL |
|---:|---|---|
| 1 | מעצבת פנים מחיר | כל המחירים של מעצבות פנים - במידרג | https://www.midrag.co.il/Content/Price/15364 |
| 2 | כמה עולה מעצבת פנים? מדריך מחירים ושירותים | https://www.shimrit-design.co.il/interior-design-pricing-guide |
| 3 | כמה עולה מעצבת פנים? 150-450 ₪ למ"ר (מחירון 2026) | https://studio-id.co.il/כמה-עולה-מעצבת-פנים/ |
| 4 | כמה עולה מעצבת פנים? מחירים שקופים ואמיתיים לשנת 2026 | https://meitalyaakov.co.il/interior-designer-cost-2026/ |
| 5 | כמה עולה עיצוב פנים? מחירון מלא וסקירת תקציב 2026 | https://inandout.co.il/interior-design-cost/ |
| 6 | כמה עולה לעצב דירה בשנת 2026? פירוט מחירים בישראל | https://ultimaschool.co.il/magazine/כמה-עולה-לעצב-דירה-בשנת-2026-פירוט-מחירים-ב/ |
| 7 | מה המחיר למעצבת פנים לבניית בית מאפס של בערך 200 מ"ר? ... | https://www.facebook.com/groups/1552858994986548/posts/3935850846687339/ |
| 8 | מחירון מעצבת פנים 2025 - Gonen Oshri | https://gonenoshri.com/מחירון-מעצבת-פנים-2025-כמה-זה-באמת-עולה-ו/ |

**AI block (תקציר מ-AI)**, first lines: עלות מעצבת פנים לפי מטר רבוע (מ"ר) בישראל נעשית בדרך כלל באחת משתי רמות ליווי, לפי מחירון עיצוב הפנים העדכני של Studio ID: תכנון ועיצוב בלבד (ללא פיקוח צמוד): 150 – 300 ₪ למ"ר (כולל תוכניות עבודה, בחירת חומרים והדמיות). תכנון וליווי מלא (כולל פיקוח וביקורים באתר): 250 – 500 ₪ למ"ר. זירת האדריכלות דוגמה לחישוב (דירת 4 חדרים בשטח של כ-100 מ"ר): תכנון ועיצוב בלבד: 15,000 – 30,000 ₪ תכנון וליווי מלא: 25,000 – 50,000 ₪ זי...

AI block links: studio-id.co.il, ziratadrichalut.co.il, shimrit-design.co.il, midrag.co.il, meitalyaakov.co.il, estifergan.co.il, midrag.co.il, goldistudio.com

### ייעוץ עיצוב

Captured 2026-11-10T20:47 · modules: img, vid, local · ads: none

| # | Title (verbatim) | URL |
|---:|---|---|
| 1 | שירותים - studioa - יפעת אברמסון | https://design-studioa.com/מסלולים/ |
| 2 | פגישת ייעוץ עיצוב פנים לשדרוג הבית - מקצועי וממוקד | https://www.shimrit-design.co.il/interior-design-project-management |
| 3 | ייעוץ עיצוב פנים | המלצות וחוות דעת על מעצבות פנים | https://www.midrag.co.il/Search/Results?ntla=K1564I7F554GJ29Q70SV65L3NM4809534486E7 |
| 4 | מורן פרי עיצוב פנים | פגישת ייעוץ לעיצוב הבית | https://www.studio-perri.co.il/meeting |
| 5 | פגישת יעוץ לתכנון ועיצוב פנים | https://www.yifatdesign.co.il/שרותי-המשרד/פגישת-יעוץ-לתכנון-ועיצוב-פנים/ |
| 6 | ייעוץ לפני רכישת נכס | ייעוץ להערכת תקציב לצורך שיפוץ | https://www.q-design.co.il/שירותי-הסטודיו/שרותי-ייעוץ-עיצוב-פנים/ |
| 7 | ייעוץ עיצוב פנים: המדריך המלא לפגישה עם מעצבת פנים - סטודיו מיכל | http://michal.studio/blog/interior-design-consulting |
| 8 | פגישת ייעוץ לעיצוב פנים | כך תחסכו עלויות מיותרות | https://shirishalom.com/consultation/ |

**AI block:** none on this query.

### ייעוץ עיצוב פנים מחיר

Captured 2026-11-10T20:48 · modules: img, vid · ads: none

| # | Title (verbatim) | URL |
|---:|---|---|
| 1 | מעצבת פנים מחיר | כל המחירים של מעצבות פנים - במידרג | https://www.midrag.co.il/Content/Price/15364 |
| 2 | מחירון עיצוב פנים | עיצוב פנים מחיר | https://www.goldistudio.com/עיצוב-פנים-מחיר/ |
| 3 | כמה עולה מעצבת פנים? מדריך מחירים ושירותים | https://www.shimrit-design.co.il/interior-design-pricing-guide |
| 4 | שלום לכולם, מה המחיר שנהוג לשלם על פגישת ייעוץ עם מעצבת ... | https://www.facebook.com/groups/2321376998117581/posts/3646063335648934/ |
| 5 | כמה עולה עיצוב פנים? מחירון מלא וסקירת תקציב 2026 | https://inandout.co.il/interior-design-cost/ |
| 6 | מחירון | https://bethameatzvot.co.il/מחירון-אקסטרא/ |
| 7 | כמה עולה לעצב דירה בשנת 2026? פירוט מחירים בישראל | https://ultimaschool.co.il/magazine/כמה-עולה-לעצב-דירה-בשנת-2026-פירוט-מחירים-ב/ |
| 8 | כמה עולה עיצוב פנים? המדריך המלא לתכנון התקציב (2026) | https://mayakedem.com/מאמרים/כמה-עולה-עיצוב-פנים/ |
| 9 | ייעוץ עיצוב פנים חד-פעמי: מה מקבלים, כמה זה עולה ומתי זה מספיק | https://www.ziratadrichalut.co.il/blog/one-time-design-consultation |

**AI block (תקציר מ-AI)**, first lines: עלות ייעוץ עיצוב פנים נעה בדרך כלל בין 300 ל-600 ש"ח לשעה, או בין 800 ל-2,500 ש"ח לפגישת ייעוץ ממוקדת של כמה שעות בבית. זירת האדריכלות +1 מחירון ייעוץ ושירותים נפוצים: שעת ייעוץ / עבודה: 250 – 600 ש"ח לשעה (מעצבים מתחילים: 250–400 ש"ח; מעצבים מנוסים: 500–1,000 ש"ח לשעה). פגישת ייעוץ חד-פעמית (כשעתיים-שלוש): 800 – 2,500 ש"ח (לעתים כוללת הכנה מראש, סקיצה או רשימת קניות). חבילות ייעוץ מורחבות (למשל ייעוץ + יום רכישות): ...

AI block links: ziratadrichalut.co.il, bethameatzvot.co.il, midrag.co.il, facebook.com, inandout.co.il, basic-living.co.il, meitalyaakov.co.il, goldistudio.com

### עיצוב דירה בתלת מימד

Captured 2026-11-10T20:49 · modules: img, vid · ads: none

| # | Title (verbatim) | URL |
|---:|---|---|
| 1 | תוכנת עיצוב וייצור פנים תלת-ממדית המונעת על ידי בינה מלאכותית | https://www.aihouse.com/he |
| 2 | הדמיות תלת מימד לבתים ברמה הגבוהה ביותר | https://studio-vida.co.il/הדמיות-תלת-מימד-לבתים/ |
| 3 | עיצוב הבית בעזרת תוכנת הדמיה תלת מימד | https://rollinom.com/he/what-is-a-virtual-tour-he/ |
| 4 | הדמיה בית פרטי | Homega 3D - טכנולוגיות תלת מימד | https://www.homega3d.com/הדמיות-פנים/הדמיה-בית-פרטי/ |
| 5 | הדמיית פנים מעוצבת: המדריך המלא לעיצוב הבית בתלת מימד (2026) | https://realitech.co.il/3d-interior-design-visualization-guide/ |
| 6 | סטודיו שרטוט: מתוכנית דירה לתלת־ממד ולעיצוב הבית | https://www.redesignai.co.il/blog/סטודיו-שרטוט-מתוכנית-דירה-לתלת-ממד |
| 7 | הדמיות תלת מימד | https://www.saf.co.il/noa/prd_1510 |

**AI block (תקציר מ-AI)**, first lines: עיצוב דירה בתלת-ממד מאפשר לכם לראות את החלל, הריהוט, הצבעים והתאורה בצורה ויזואלית מדויקת עוד לפני תחילת השיפוץ או רכישת הריהוט, ובכך למנוע טעויות יקרות. סטודיו וידה +1 כלים ופלטפורמות מובילות לעיצוב דירה בתלת-ממד כלים מבוססי בינה מלאכותית (AI) ואונליין: Luw.ai: מחולל תוכניות קומה וסטודיו לתלת-ממד המאפשר להקליד תיאור מילים (לשלב גודל, חדרים ומטבח) וה-AI מייצר קירות, דלתות ותוכנית בקנה מידה. Homiwork: מאפשר להעלות תוכ...

AI block links: studio-vida.co.il, luw.ai, homiwork.com, aihouse.com, colman.ac.il

### תכנון דירה

Captured 2026-11-10T20:49 · modules: img, vid · ads: none

| # | Title (verbatim) | URL |
|---:|---|---|
| 1 | תכנון דירה - נטע-לי וטל נוי - איך מתכננים נכון בשנת 2026? | https://netalinoy.com/תכנון-דירה/ |
| 2 | תכנון דירות קבלן ושינויי דיירים | Plan My Space | https://www.planmyspace.co.il/ |
| 3 | עמוד קידום תכנון | https://www.renten.co.il/עמוד-קידום-תכנון/ |
| 4 | מתחמים בתכנון דירה להשכיר - ציבורי | https://experience.arcgis.com/experience/ae17378796204e8780bb164c94611f92 |
| 5 | תכנון אונליין | https://www.archonline.co.il/ |
| 6 | תכנון בית פרטי – התהליך המלא | טל רוזין - משרד אדריכלים במרכז | https://talrozin.com/he/תכנון-בית-פרטי-התהליך/ |
| 7 | תכניות אדריכליות וסקיצות לתכנון ובניית בית פרטי בישראל - שבלול | https://www.shablul.net/YG |
| 8 | 7 רעיונות של תוכניות דירה | דירה, עיצוב, תכנון | https://www.pinterest.com/adiwerker/תוכניות-דירה/ |

**AI block (תקציר מ-AI)**, first lines: תכנון דירה נכון מתחיל בהבנה מעמיקה של הצרכים היומיומיים של בני הבית, ניצול חכם של המרחב ומעבר מסודר בין שלבי העבודה. netalinoy.com שלבים מרכזיים בתכנון דירה הגדרת צרכים ותקציב: מיפוי כמות האנשים, אורח החיים, מקומות אחסון נדרשים והגדרת מסגרת תקציבית ברורה. תכנון פונקציונלי (פריסת חלל): סידור מחדש של הקירות, המעברים, והמיקום של המטבח, חדרי הרחצה והחדרים הפרטיים. ניתן להיעזר בשירותי תכנון מקוונים כמו תכנון אונליין או מע...

AI block links: netalinoy.com, archonline.co.il, cplan.co.il, youtube.com, planmyspace.co.il, midrag.co.il, renten.co.il, experience.arcgis.com

Video results: עיצוב דירה קטנה - חמישה טיפים לעיצוב דירה קטנה (YouTube, אתר מידרג, 13 בנוב׳ 2023, with key moments)

### הדמיה לדירה

Captured 2026-11-10T20:49 · modules: paa_by_data_q, img, vid · ads: none

| # | Title (verbatim) | URL |
|---:|---|---|
| 1 | הדמיות - Maya Design | https://mayahdesign.co.il/פרויקטים-2/ |
| 2 | הדמיית בתים | https://kesem3d.com/הדמיית-בתים/ |
| 3 | הדמיות בתים פרטיים: המדריך המלא להדמיה לפני הבנייה | SD | https://sdsd.co.il/private-home-visualization/ |
| 4 | סטודיו מעיין גולן - הדמיות אדריכליות | הדמיות ממוחשבות | הדמיות תלת ... | https://studiomaayan.co.il/ |
| 5 | הדמיה אדריכלית לבית פרטי: מה אפשר לראות לפני שמתחילים לבנות? | https://clararegen.com/הדמיה-אדריכלית-לבית-פרטי/ |
| 6 | פרויקט הדמייה לבית מגורים - טובה וצילה משרד אדריכלות | https://www.r-d-arch.co.il/avada_portfolio/פרויקט-הדמייה-לבית-מגורים/ |
| 7 | הדמיות - DuetHome - דואט | https://www.duet-home-design.co.il/הדמיות/ |

**AI block (תקציר מ-AI)**, first lines: הדמיה לדירה היא המחשה ויזואלית בתלת-ממד של תוכניות האדריכלות או עיצוב הפנים, המאפשרת לראות את החלל (סלון, מטבח, חדרים) בצורה מציאותית עוד לפני תחילת הבנייה או השיפוץ. קסם הדמיות +1 סוגי הדמיות ועלויות נפוצות הדמיה בסיסית: מודל תלת-מימד פשוט המציג את מבנה החלל, ולרוב נכלל כחלק מן התכנון האדריכלי. הדמיה פוטוריאליסטית (ריאליסטית): תמונה מציאותית ברמה גבוהה של חומרים, תאורה וריהוט. המחיר נע לרוב בין 1,000 ל-4,000 ₪ לתמונ...

AI block links: kesem3d.com, redesignai.co.il, shop.homexpert.co.il, clararegen.com, midrag.co.il, instagram.com, studiomaayan.co.il, mayahdesign.co.il

### שרטוט דירה אונליין

Captured 2026-11-10T20:55 · modules: img, vid · ads: none

| # | Title (verbatim) | URL |
|---:|---|---|
| 1 | רידיזיין AI - עיצוב פנים AI בעברית | עוזר אישי ללא עלות | https://www.redesignai.co.il/ |
| 2 | תוכנת עיצוב וייצור פנים תלת-ממדית המונעת על ידי בינה מלאכותית | https://www.aihouse.com/he |
| 3 | שרטוט AI חינמי: הפכו שרטוטים למציאות באופן מיידי | https://luw.ai/he/sketch-ai |
| 4 | כלי תכנון אונליין | https://www.ikea.com/il/he/planners/ |
| 5 | עיצוב חדרים AI — מייקאובר לכל חדר תוך שניות | https://genroom.io/he/room-design |
| 6 | עיצוב פנים בחינם בעזרת AI מתוך תמונה. - RoomsGPT | https://www.roomsgpt.io/he |
| 7 | מחולל עיצוב פנים מבוסס AI: עיצוב מחדש של חדרים בשניות ללא תשלום | https://www.capcut.com/he-il/tools/ai-interior-design-generator |

**AI block (תקציר מ-AI)**, first lines: לשרטוט ותכנון דירה אונליין קיימים מספר כלים מובילים, בהתאם לצורך שלכם (שרטוט מדויק מאפס, עיצוב פנים באמצעות בינה מלאכותית, או מיקום רהיטים): כלים לשרטוט ותכנון תלת-ממד ומבנה (Floor Plans) RoomSketcher: כלי אונליין ותיק ופופולרי שמאפשר לשרטט תוכניות דירה, להוסיף מידות ולראות תצוגה בתלת-ממד (עם בסיס חינמי ואפשרויות מתקדמות בתשלום). שיפוצים פלוס Homestyler: פלטפורמה מבוססת דפדפן (בעלת ממשק בעברית) המבוססת על הטכנולוגיה ...

AI block links: shiplus.co.il, ikea.com, luw.ai, genroom.io, roomsgpt.io, redesignai.co.il, aihouse.com, archonline.co.il

Video results: an excellent AI tool for inspiration for your living room design (YouTube, שחר גולן) / שרטוט אונליין, תוכנת שרטוט אונליין, שרטוט דירה אונליין (YouTube, לימודי עיצוב גרפי)

### אפליקציה לעיצוב דירה

Captured 2026-11-10T20:50 · modules: img, vid · ads: none

| # | Title (verbatim) | URL |
|---:|---|---|
| 1 | Room Planner: עיצוב פנים - אפליקציות ב-Google Play | https://play.google.com/store/apps/details (id stripped) |
| 2 | Home Planner — האפליקציה הקלה לעיצוב הבית ב-3D עם כלי AI | https://homeplannerapp.com/he/ |
| 3 | מחפשת אפליקציה לעיצוב הבית מדויקת עד כמה שאפשר אם אפשרות ... | https://www.facebook.com/groups/home4y/posts/3997816500487311/ |
| 4 | היישום Home AI - בינה לעיצוב פנים - App Store - Apple | https://apps.apple.com/il/app/home-ai-בינה-לעיצוב-פנים/id6464476667 |
| 5 | HomeByMe - אפליקציות ב-Google Play | https://play.google.com/store/apps/details (id stripped) |
| 6 | 7 האפליקציות המובילות לעיצוב פנים בעזרת בינה מלאכותית | https://www.capcut.com/he-il/resource/ai-interior-design-app |
| 7 | אפליקציות לעיצוב הבית - עזרים מומלצים לשיפוץ | https://www.shiplus.co.il/מאמרים/עיצוב-פנים/אפליקציות-לשיפוץ-הבית.html |

**AI block (תקציר מ-AI)**, first lines: קיימות מספר אפליקציות וכלי בינה מלאכותית מומלצים לעיצוב הבית, תכנון תלת-ממדי והדמיות: רידיזיין AI: כלי עיצוב פנים ונוף בעברית המאפשר להעלות תמונה או שרטוט תלת-ממדי כדי לקבל הדמיות של חללים, סלונים ומטבחים. Home Planner: אפליקציה לתכנון חדרים ב-3D, קביעת מידות קיר מדויקות והצבת פריטי ריהוט מתוך מאגר גדול. Planner 5D: אפליקציה פופולרית לתכנון תוכניות קומה בדו-ממד ובתלת-ממד והדמיות מציאותיות של הבית. Houzz: מיועדת בעיקר...

AI block links: redesignai.co.il, homeplannerapp.com, easytap.co.il, shiplus.co.il, facebook.com, adira.co.il, softwarecompare.co.il, softwarecompare.co.il

Video results: אפליקציה לעיצוב הבית בחינם – הדמיה אדריכלית בפלאפון / עיצוב פנים בחינם עם Room Planner: מדדו חדרים, בחרו רצפות, הוסיפו רהיטים, טקסטיל / an excellent AI tool for inspiration for your living room design (YouTube, שחר גולן)

### תוכנה לעיצוב דירה

Captured 2026-11-10T20:51 · modules: paa_by_data_q, img, vid · ads: none

| # | Title (verbatim) | URL |
|---:|---|---|
| 1 | מעצבים את הבית? 16 תוכנות לעיצוב הבית שאתם צריכים להכיר | https://www.bvd.co.il/מעצבים-את-הבית-16-תוכנות-לעיצוב-הבית-שאת/ |
| 2 | Room Planner: עיצוב פנים - אפליקציות ב-Google Play | https://play.google.com/store/apps/details (id stripped) |
| 3 | עיצוב חללים שונים בביתכם | https://www.ikea.com/addon-app/space/platform/latest/il/he/ |
| 4 | מחפשת אפליקציה לעיצוב הבית מדויקת עד כמה שאפשר אם אפשרות ... | https://www.facebook.com/groups/home4y/posts/3997816500487311/ |
| 5 | House Design 3D - Home Planner - אפליקציות ב-Google Play | https://play.google.com/store/apps/details (id stripped) |
| 6 | רידיזיין AI - עיצוב פנים AI בעברית | עוזר אישי ללא עלות | https://www.redesignai.co.il/ |
| 7 | 5 כלי עיצוב חדרים AI חינמיים באמת (2026) | https://genroom.io/he/blog/free-ai-room-design-tools |
| 8 | תוכנה לעיצוב פנים ללא מקצוענים | https://www.shiplus.co.il/פורומים/עיצוב-פנים/19448.html |

**AI block (תקציר מ-AI)**, first lines: הנה התוכנות והאפליקציות הבולטות ביותר לעיצוב הבית ותכנון פנים, המחולקות לפי סוג הצורך: תוכנות לתכנון מדויק ומימדים (דו-ממד ותלת-ממד) Sweet Home 3D: תוכנה חינמית וקוד פתוח המאפשרת שרטוט קירות, דלתות וחלונות לפי מידות אמיתיות עם תצוגת תלת-ממד בזמן אמת. מתאימה במיוחד למי שמתכנן שיפוץ ומעדיף כלי פרקטי למחשב או לדפדפן. SketchUp: תוכנה פופולרית וגמישה ליצירת חללים פנימיים, עם ספריית רהיטים וחומרים עצומה (מתאימה לחובבים מתק...

AI block links: bvd.co.il, homeplannerapp.com, roomsgpt.io, ikea.com, facebook.com, softwarecompare.co.il, facebook.com, instagram.com

Video results: an excellent AI tool for inspiration for your living room design (YouTube, שחר גולן)

### עיצוב דירה ai

Captured 2026-11-10T20:54 · modules: img, vid · ads: none

| # | Title (verbatim) | URL |
|---:|---|---|
| 1 | רידיזיין AI - עיצוב פנים AI בעברית | עוזר אישי ללא עלות | https://www.redesignai.co.il/ |
| 2 | עיצוב פנים AI אונליין — מייקאובר חינם ב-30 שנ' | https://genroom.io/he/interior-design |
| 3 | עיצוב חדרים באמצעות בינה מלאכותית בחינם: שנו את החלל שלכם ... | https://www.adobe.com/il_he/products/firefly/features/ai-room-design.html |
| 4 | עיצוב פנים בחינם בעזרת AI מתוך תמונה. - RoomsGPT | https://www.roomsgpt.io/he |
| 5 | כל אלו תוכנות AI לעיצוב הבית אתם ממליצים? תוכנה שתהיה ... | https://www.facebook.com/groups/home4y/posts/4033165280285766/ |
| 6 | Home AI - בינה לעיצוב פנים - אפליקציות ב ... | https://play.google.com/store/apps/details (id stripped) |
| 7 | 5 כלי עיצוב חדרים AI חינמיים באמת (2026) | https://genroom.io/he/blog/free-ai-room-design-tools |
| 8 | איך לעצב את הבית עם כלי AI חינמיים? | https://pandazzz.co.il/blogs/news/איך-לעצב-את-הבית-עם-כלי-ai-חינמיים |

**AI block (תקציר מ-AI)**, first lines: שימוש בכלי בינה מלאכותית (AI) מאפשר לעצב מחדש חללים בבית, לקבל השראה ולייצר הדמיות ריאליסטיות בקלות וללא צורך בידע מוקדם. Google Play +1 כלי AI מובילים לעיצוב הבית RoomsGPT: מאפשר להעלות תמונה של חדר, לבחור מבין עשרות סגנונות עיצוב (מודרני, כפרי, מינימליסטי וכו') ולקבל הדמיה מחדש בתוך שניות ללא צורך בהרשמה. Luw.ai: כלי מתקדם לעיצוב פנים וחוץ הבית הכולל יצירת תלת־ממד, שרטוט AI, הסרת ריהוט ויצירת לוחות השראה (Mood Boar...

AI block links: redesignai.co.il, roomsgpt.io, luw.ai, adobe.com, pandazzz.co.il, genroom.io, givat-alonim.co.il, genroom.io

### עיצוב דירה קטנה

Captured 2026-11-10T20:50 · modules: img, vid · ads: none

| # | Title (verbatim) | URL |
|---:|---|---|
| 1 | 47 רעיונות של דירות קטנות | עיצוב, דירה קטנטנה, דירה | https://www.pinterest.com/rikikrakauer/דירות-קטנות/ |
| 2 | המדריך הגדול לעיצוב דירה קטנה | https://www.ynet.co.il/architecture/article/bkpfozetn |
| 3 | שיפוץ דירה קטנה שאתם חייבים לראות - 76 מ"ר במרכז תל אביב | https://www.bringithome.co.il/blogs/news/שיפוץ-דירה-קטנה-בעיצוב-נורדי-76-מר-במרכז-תל-אביב |
| 4 | כל מה שצריך לדעת על עיצוב דירה קטנה | https://www.bvd.co.il/design-homes/small/ |
| 5 | קטן עליכם: המדריך השלם לעיצוב דירה קטנה | https://pickinteri.co.il/כללי/עיצוב-דירה-קטנה/ |
| 6 | עיצוב דירה קטנה שחושבת עליכם | אסתי ורועי איפרגן | https://estifergan.co.il/עיצוב-דירה-קטנה/ |
| 7 | דירה קטנה וידידותית לכיס שכולה כיף והנאה | https://www.ikea.com/il/he/ideas/home-furnishings/imagination-station-a-small-budget-friendly-apartment-for-two-pub092df6a0/ |

**AI block (תקציר מ-AI)**, first lines: עיצוב דירה קטנה דורש תכנון חכם ומדויק כדי ליצור תחושת מרחב פתוחה ופונקציונלית מבלי ליצור עומס. עקרונות מרכזיים לעיצוב דירה קטנה פלטת צבעים בהירה: שימוש בצבעים בהירים כמו לבן, בז' ואפור בהיר על הקירות והתקרות מגדיל ויזואלית את החלל. אחסון אנכי ומקסימלי: ניצול גובה הקירות עם מדפים, ארונות עד התקרה ונישות גבס שומר על הרצפה פנויה. ריהוט מודולרי ורב-שימושי: בחירה ברהיטים מתקפלים, שולחנות נפתחים ומיטות עם ארגז אחסון או ספה...

AI block links: pinterest.com, ynet.co.il, bringithome.co.il, bvd.co.il, pickinteri.co.il, ikea.com, midrag.co.il, anatarc.com

Video results: עיצוב דירה קטנה - חמישה טיפים לעיצוב דירה קטנה (YouTube, אתר מידרג, 13 בנוב׳ 2023)

### עיצוב דירה חדשה מקבלן

Captured 2026-11-10T20:52 · modules: img, vid · ads: none

| # | Title (verbatim) | URL |
|---:|---|---|
| 1 | עיצוב דירת קבלן - נטע-לי וטל נוי - אדריכלות ועיצוב פנים ברמה מתקדמת | https://netalinoy.com/project_cat/עיצוב-דירת-קבלן/ |
| 2 | עיצוב דירת קבלן | איך לעצב דירה חדשה מקבלן? דוגמאות ותמונות ... | https://www.midrag.co.il/content/tip/3891 |
| 3 | עיצוב דירת קבלן במרכז – תכנון וליווי מקצועי | https://www.shimrit-design.co.il/איך-להפוך-דירת-קבלן-לדירה-יחודית |
| 4 | ליווי לעיצוב דירת קבלן Elephant Design לירון שנהר | https://www.elephantdesign.co.il/עיצוב-ותכנון-דירה-מקבלן |
| 5 | דירה חדשה מקבלן תכנון עיצוב ושינויי דיירים | https://www.facebook.com/groups/466734475710690/ |
| 6 | עיצוב דירת קבלן - שוקי מאיר עיצוב פנים - עיצוב דירה מקצועי ... | https://shuki-meir.co.il/עיצוב-פנים/עיצוב-דירת-קבלן/ |
| 7 | עיצוב פנים – דירות מקבלן | https://hadif.co.il/blog/עיצוב-פנים-דירות-מקבלן/ |
| 8 | 100 רעיונות של Apartment Interior Design | עיצוב דירת קבלן | https://www.pinterest.com/dnshaked/apartment-interior-design-עיצוב-דירת-קבלן/ |

**AI block (תקציר מ-AI)**, first lines: עיצוב דירת קבלן הוא תהליך שבו הופכים חלל סטנדרטי וגולמי שמקבלים מהקבלן לבית מעוצב, פונקציונלי ומותאם אישית. netalinoy.com +2 שלבים מרכזיים בתהליך שלב א' – שינויי דיירים (כ-4 עד 6 חודשים לפני מועד הקבלן): זהו השלב הקריטי ביותר שבו מבצעים שינויים בתכנון הפנימי של הדירה. הזזת או הריסת קירות פנימיים כדי להתאים את החלל למשפחה (למשל פתיחת מטבח, הגדלת סלון או איחוד חדרים). תכנון מחדש של תשתיות: נקודות חשמל ותקשורת, אינסטלצי...

AI block links: netalinoy.com, ynet.co.il, shimrit-design.co.il, levelstudio.co.il, pinterest.com, sharondavid.co.il, alloy.co.il, rossetto.co.il

### שינויי דיירים

Captured 2026-11-10T20:53 · modules: paa_by_data_q, img, vid · ads: none

| # | Title (verbatim) | URL |
|---:|---|---|
| 1 | מדריך מלא ממתאמת שינויי דיירים (2026) | https://arcb.co.il/tenants-changes/ |
| 2 | ההסבר המקיף ביותר | Indesigns - מתאמת שינויי דיירים לקבלנים. | https://www.indesigns.co.il/שינויי-דיירים/ |
| 3 | SHIFT: בית | https://shift-home.co.il/ |
| 4 | תפנים - ניהול מערך תיאום שינויי דיירים ועיצוב פנים | https://tpnim.co.il/ |
| 5 | שינויי דיירים בדירת קבלן - ליווי אדריכלי אישי ומדויק | https://clararegen.com/שינוי-דיירים/ |
| 6 | ליווי מקצועי לשינויי דיירים בדירות קבלן | https://www.inch.co.il/apartment-changes/ |
| 7 | שינויי דיירים: מהבקשה של הקונה ועד הביצוע בדירה | https://keeperforms.co.il/blog/שינויי-דיירים/ |

**AI block (תקציר מ-AI)**, first lines: שינויי דיירים הוא תהליך שבו רוכשי דירה חדשה מקבלן משנים או משדרגים את התכנון המקורי של הדירה כדי להתאים אותה לצרכיהם האישיים לפני שהבנייה מסתיימת. בל אהרוני +1 סוגי שינויים נפוצים שינויים קלים (מינוריים): הוספת נקודות חשמל ותאורה, הזזת שקעים, שדרוג כלים סניטריים או החלפת ריצוף וחיפויים. שינויים משמעותיים: הריסה או הזזה של מחיצות פנימיות, שינוי מבנה חדרים או הגדלת חדרי רחצה. דברים שלא ניתן לשנות: מעטפת חיצונית של הבני...

AI block links: arcb.co.il, ronitmarom.co.il, mozeslice.com, shirleystein.co.il, inch.co.il, keeperforms.co.il, archonline.co.il, fs.knesset.gov.il

Video results: ניהול שינויי דיירים (YouTube, dekel group, 8 בנוב׳ 2026)

### תכנון מטבח

Captured 2026-11-10T20:53 · modules: paa_by_data_q, img, vid · ads: none

| # | Title (verbatim) | URL |
|---:|---|---|
| 1 | המדריך לתכנון המטבח: שישה צעדים בדרך למטבח החלומות | https://www.regba.co.il/magazine/kitchen-design/המדריך-לתכנון-המטבח/ |
| 2 | תכנון מטבחים – הדרך הנכונה למטבח הנכון | https://tcheletkitchen.co.il/מאמרים/תכנון-מטבחים/ |
| 3 | תכנון מטבח לשנת 2026 • דא קוצ'ינה מטבחים - DaCucina Kitchens | https://www.dacucina-kitchens.com/kitchens/תכנון-מטבח/ |
| 4 | תכנון מטבח - מידות מומלצות ועקרונות - המדריך השלם! | https://touchwood.co.il/בלוג/מדריך-מידות-שימושי-לעיצוב-מטבח/ |
| 5 | תכנון מטבח | https://www.zivltd.com/תכנון-מטבח/ |
| 6 | כלי תכנון אונליין | https://www.ikea.com/il/he/planners/ |
| 7 | תכנון מטבח יוקרתי: שילוב של עיצוב והתאמה אישית | https://www.unoxcasa.com/he_il/blog/תכנון-מטבח-יוקרתי-שילוב-של-עיצוב-והתאמה-אישית/ |
| 8 | תכנון מטבח | טיפים לעיצוב ותכנון המטבח - במידרג | https://www.midrag.co.il/Content/Tip/9836 |

**AI block (תקציר מ-AI)**, first lines: תכנון מטבח נכון מתבסס על שילוב בין אסתטיקה לבין פונקציונליות שמקלה על עבודה יומיומית. מטבחי זיו העקרונות המרכזיים לתכנון מטבח משולש העבודה הקדוש: מיקום נכון ונוח בין שלושת המוקדים המרכזיים – מקרר, כיור וכיריים. המרחק בין צלעות המשולש צריך להיות נוח לתנועה (בדרך כלל בין 1.2 ל-2.7 מטר לכל צלע). מטבחי רגבה +2 חלוקה ל-5 אזורי פעילות (לפי עקרונות חברת בלורן): אחסון מזון, אחסון כלים, ניקוי, הכנה ובישול/אפייה. מידות ומרחקים...

AI block links: zivltd.com, regba.co.il, bluran.co.il, touchwood.co.il, midrag.co.il, genroom.io, ikea.com, dacucina-kitchens.com

### עיצוב סלון

Captured 2026-11-10T20:53 · modules: img, vid · ads: none

| # | Title (verbatim) | URL |
|---:|---|---|
| 1 | 31 רעיונות של עיצוב סלון | סלון, עיצוב, חדרי סלון | https://www.pinterest.com/shirabenasher/עיצוב-סלון/ |
| 2 | עיצוב סלון: 60 סלונים מעוצבים לפי סגנון, עם תמונות - WALLS | https://wallsmag.co.il/סלון-מעוצב-לפי-סגנונות-עיצוב/ |
| 3 | רעיונות לסלון שמתאימים לכל סגנון, טעם ובית | https://www.ikea.com/il/he/rooms/living-room/ |
| 4 | עיצוב סלון | רעיונות והום סטיילינג | https://ida-home.co.il/סלון/ |
| 5 | עיצוב סלון AI — מייקאובר חינם ב-30 שניות | https://genroom.io/he/living-room-design |
| 6 | עיצוב סלון: 30 סלונים מעוצבים על ידי מעצבי פנים | https://pickinteri.co.il/כללי/עיצוב-סלון-כל-הסגנונות/ |
| 7 | מדור עיצוב סלון, עיצוב הסלון - כל מה שכדאי לדעת | https://www.bvd.co.il/rooms/living/ |
| 8 | עיצוב סלון | https://www.nicoletti.co.il/טיפים-לעיצוב-פנים-מודרני-של-הסלון/ |

**AI block (תקציר מ-AI)**, first lines: עיצוב סלון מושלם מתחיל בבחירת סגנון מרכזי, תכנון נכון של העמדת הרהיטים והתאמת הטקסטיליה והתאורה לחלל. wallsmag.co.il +1 סגנונות עיצוב פופולריים הסגנון הנורדי (סקנדינבי): מאופיין בפשטות, מינימליזם, צבעים בהירים וחומרים טבעיים כמו עץ. הסגנון המודרני: קווים נקיים וישרים, צורות גיאומטריות, ושימוש בחומרים כמו זכוכית, מתכת ושיש. הסגנון הכפרי: שימוש בעץ בגוון טבעי, אבן טבעית ואווירה חמה ומזמינה. בוהו-שיק: שילוב של חומרים טב...

AI block links: pinterest.com, wallsmag.co.il, shimrit-design.co.il, midrag.co.il, pickinteri.co.il, ikea.com, ida-home.co.il, rossetto.co.il

### הום סטיילינג

Captured 2026-11-10T20:54 · modules: paa_by_data_q, img, vid, local · ads: none

| # | Title (verbatim) | URL |
|---:|---|---|
| 1 | הילה ברונשטיין: מעצבת הום סטיילינג ועיצוב פנים | https://www.hilladesign.com/ |
| 2 | קורס הום סטיילינג ובינה מלאכותית | https://handesaim.shenkar.ac.il/לימודי-תעודה/לימודי-הום-סטיילינג/ |
| 3 | הום סטיילינג: הלבשת הבית בלי לשבור קירות | https://ida-home.co.il/הום-סטיילינג/ |
| 4 | הום סטיילינג לבית ולסלון | הלבשת הבית - Me Design | https://me-design.co.il/הום-סטיילינג/ |
| 5 | הרצאת הום סטיילינג 5000 - 6B STUDIO | https://6bstudio.co.il/homestyling-talk-low/ |
| 6 | קורס הום סטיילינג | https://www.my-college.org.il/html5/ |
| 7 | מריאנה רידל | מעצבת בתים עם אופי‎ (@marianna_home_styling) | https://www.instagram.com/marianna_home_styling/ |
| 8 | הום סטיילינג - מחירים | כל המידע והמחירים של הלבשת בתים - במידרג | https://www.midrag.co.il/Content/Price/10098 |

**AI block (תקציר מ-AI)**, first lines: הום סטיילינג (הלבשת הבית) הוא תהליך עיצובי שנועד לשדרג את הנראות והאווירה בחלל, ללא צורך בשיפוץ מסיבי, הזזת קירות או טיפול בתשתיות (אינסטלציה וחשמל). הבית של עידה +1 מה כולל תהליך הום סטיילינג? ריהוט משלים: בחירה והעמדה של רהיטים שיוצרים זרימה ונוחות בחלל. טקסטיל: שילוב וילונות, שטיחים, כריות נוי ומצעים שנותנים חמימות ורכות. צבע ותאורה: בחירת גוונים לקירות, טפטים וגופי תאורה שמשנים את האור והאנרגיה בחדר. אקססוריז וטא...

AI block links: ida-home.co.il, hootam.co.il, arti-studio.co.il, midrag.co.il, hit.ac.il, hilit.net, hilladesign.com, handesaim.shenkar.ac.il

### אדריכל או מעצב פנים

Captured 2026-11-10T20:55 · modules: img, vid · ads: none

| # | Title (verbatim) | URL |
|---:|---|---|
| 1 | אדריכל פנים או מעצב פנים: מה ההבדל ומתי נזדקק לכל אחד מהם | https://www.shiplus.co.il/מאמרים/אדריכלות/אדריכל-או-מעצב-פנים.html |
| 2 | אדריכל או מעצב פנים - את מי מהם אתם צריכים? ... | https://www.inbaldesign.co.il/מה-ההבדל-בין-אדריכל-ומעצבת-פנים-ומתי-כד/ |
| 3 | מתי באמת צריכים אדריכל לעומת מעצב פנים | https://www.grynhaus.co.il/מתי-באמת-צריכים-אדריכל-לעומת-מעצב-פנים/ |
| 4 | אדריכל או מעצב פנים - עבור דירת קבלן | https://www.hasolidit.com/kehila/threads/אדריכל-או-מעצב-פנים-עבור-דירת-קבלן.30759/ |
| 5 | אדריכל או מעצב פנים? | https://levelstudio.co.il/he/אדריכל-או-מעצב-פנים/ |
| 6 | לימודי אדריכלות או עיצוב פנים - מה ההבדל ומה מתאים לכם ללמוד | https://www.michlalot.co.il/limudim/arch-or-interior-des.php |
| 7 | האם אני צריך אדריכל או מעצב פנים? : r/AskIreland | https://www.reddit.com/r/AskIreland/comments/1j8m5kw/do_i_need_an_architect_or_interior_designer/ |

**AI block (תקציר מ-AI)**, first lines: ההבדל המרכזי בין אדריכל למעצב פנים טמון בסמכות החוקית, בהיקף העבודה ובהכשרה: אדריכל אחראי על תכנון המבנה הפיזי מאפס, השלד, המעטפת והגשת תוכניות להיתרי בנייה מול הרשויות, בעוד מעצב פנים מתמקד בחלוקת החלל הפנימי, באסתטיקה, בחומרים, בתאורה ובריהוט בתוך המעטפת הקיימת. ענבל קרקו +2 אדריכל (או אדריכלית) הסמכות וחוקיות: בעל סמכות חוקית לתכנן מבנים מכל סוג (מבתים פרטיים ועד גורדי שחקים), לחתום על תוכניות ולבקש היתרי בנייה וא...

AI block links: inbaldesign.co.il, shiplus.co.il, midrag.co.il, me-design.co.il, shimritmishan.com, study.co.il, grynhaus.co.il, liadyosef.co.il

Video results: פודקאסט פרק 99 - מה ההבדל בין אדריכל למעצב פנים ומה תפקידו של ... (key moments incl. 'עלויות ותהליך תכנון')
