# Environmental hazards near a home: Hebrew keyword demand (Israel)

Research date: 3.11.2026, data pulled 19:52 UTC (21:52 Israel time).
Source: DataForSEO through the MCP tool `mcp__dataforseo__api_request`.

## Method

- **Labs (L).** `POST /v3/dataforseo_labs/google/keyword_suggestions/live`, location 2376, language "he", limit 100, sorted by volume. We ran 4 seeds: "קרינה" (2,114 suggestions exist), "אנטנה" (516), "מתח גבוה" (327) and "זיהום אוויר" (541).
- **Google Ads (GA).** `POST /v3/keywords_data/google_ads/search_volume/live`, location 2376, language "iw". We ran 4 batches of 10 hand-picked terms covering antennas, power and transformers, noise, hazards and "where to live".
- **Budget.** 8 keyword calls in total, the cap that was set. The trimmed responses did not return the cost.
- **Volume.** Volume is the average monthly searches in Israel over the last 12 months.
- **CPC.** CPC is in USD, as DataForSEO returns it.
- **"No data".** Google Ads returned no volume for the term, meaning under 10 searches or not tracked. It is not a zero.
- **Close variants.** Google Ads merges close variants. For example, "אנטנה סלולרית" and "אנטנות סלולריות" both show 2,400. They are one demand pool, so they must not be added together.
- **Not done here.** We did not run a Search Console check of existing nad-lan.co.il pages for these terms, and we did not run the URL word audit (`tools/gsc/url_word_audit.py`). Both are needed before minting a slug.

## Top 20 terms overall (on-topic, one row per demand cluster)

`govmap` (90,500/month, GA) is left out. It is a navigational brand for the government map portal, whose `govmap.gov.il/sviva` environment layer the AI Overview cites. It shows that Israelis already use a map habit, but it is not a term the page can target.

| # | Term | Volume | Src | CPC $ | Intent group |
|---|---|---|---|---|---|
| 1 | זיהום אוויר | 6,600 | L | 2.07 | Air pollution |
| 2 | אנטנה סלולרית / אנטנות סלולריות | 2,400 | L+GA | 8.77 | Antenna |
| 3 | מפת אנטנות סלולריות | 1,300 | GA | – | Antenna map / distance |
| 4 | קרינה (generic, mixed with UV) | 1,300 | L | 4.72 | Radiation |
| 5 | זיהום אוויר בישראל לפי ערים | 1,000 | L | 0.01 | Air by city |
| 6 | מדד זיהום אוויר | 1,000 | L | – | Air by city |
| 7 | איכות אוויר | 880 | GA | – | Air (seasonal: 3,600 in Feb and Apr 2026, 40 in Sep 2026) |
| 8 | זיהום אוויר היום | 880 | L | – | Air now |
| 9 | זיהום אוויר עכשיו | 720 | L | – | Air now |
| 10 | זיהום אוויר תל אביב | 720 | L | – | Air by city |
| 11 | מפת זיהום אוויר | 480 | L | – | Air map |
| 12 | זיהום אוויר בישראל היום | 480 | L | – | Air now |
| 13 | בדיקת אנטנה סלולרית | 390 | L | **19.16** | Antenna check (highest CPC in the set) |
| 14 | קרינה אלקטרומגנטית | 390 | L | 3.41 | Radiation |
| 15 | מכשיר למדידת קרינה / מודד קרינה / מד קרינה | 390 | L | 1.92–2.16 | Measuring |
| 16 | מתח גבוה (mostly film, course and tariff noise) | 390 | L | – | Power lines |
| 17 | תחזית זיהום אוויר | 390 | L | – | Air forecast |
| 18 | זיהום אוויר בישראל מפה | 390 | L | – | Air map |
| 19 | אנטנה סלולרית מפה | 260 | L | – | Antenna map |
| 20 | זיהום אוויר חיפה / שוהם / בישראל | 260 each | L | – | Air by city |

Next in line: שנאי חשמל 210 (GA, mostly product intent), מודד/מד קרינה variants, and the rest of the city air terms.

## Group tables

### 1. Radiation from antennas and transmitters

| Term | Volume | Src | CPC $ |
|---|---|---|---|
| אנטנה סלולרית | 2,400 | L | 8.77 |
| אנטנות סלולריות | 2,400 | GA | 8.77 (competition index 11) |
| קרינה | 1,300 | L | 4.72 |
| קרינה אלקטרומגנטית / אלקטרומגנטי | 390 | L | 3.41 / 3.14 |
| קרינה מייננת | 480 | L | – |
| רמות קרינה | 140 | L | 3.16 |
| רמת קרינה | 110 | L | 4.64 |
| קרינה בלתי מייננת | 70 | L | – |
| משדרי רדיו | 50 | GA | 0.64 |
| אנטנה סלולרית ליד הבית | 40 | L | – |
| קרינה סלולרית | 20 | GA | – |
| אנטנה סלולרית על הגג | 20 | L | – |
| קרינה מאנטנה סלולרית | 10 | GA | 9.06 |
| אנטנה על הגג | 10 | GA | – |
| אנטנה סלולרית על גג בניין | 10 | L | – |
| האם מסוכן לגור ליד אנטנה סלולרית | 10 | L | – |
| קרינה ממשדרים | no data | GA | – |

### 2. Distance from an antenna and maps by address

| Term | Volume | Src | CPC $ |
|---|---|---|---|
| מפת אנטנות סלולריות | 1,300 (stable 1,000–1,300 every month) | GA | – |
| בדיקת אנטנה סלולרית | 390 | L | 19.16 |
| אנטנה סלולרית מפה | 260 | L | – |
| מרחק בטוח מאנטנה סלולרית | 20 (70 in Oct 2025) | GA | – |
| מפת קרינה | 10 | GA | – |

Google's related searches show more phrasings, but with no volume measured: "אנטנות סלולריות לפי כתובת", "מפת אנטנות סלולריות 5g", "מפת אנטנות סלולריות בישראל", and "מפת אנטנות סלולריות המשרד להגנת הסביבה".

### 3. Power lines, transformer rooms and substations

| Term | Volume | Src | CPC $ |
|---|---|---|---|
| מתח גבוה (noisy) | 390 | L | – |
| שנאי חשמל | 210 | GA | 0.74 (competition index 79, product intent) |
| קווי מתח גבוה | 70 | L | – |
| חדר שנאים | 70 | GA | 2.08 |
| שנאים מתח גבוה / שנאי מתח גבוה | 50 / 50 | L | 0.35 / 0.24 |
| עמודי חשמל מתח גבוה / עמוד חשמל מתח גבוה | 50 / 50 | L | – |
| תחנת השנאה | 40 | GA | – |
| עמוד מתח גבוה | 40 | L | 0.09 |
| חדר חשמל מתח גבוה | 20 | L | – |
| איך מזהים קו מתח גבוה | 20 | L | – |
| מפת קווי מתח גבוה | 20 | L | – |
| קרינה מקווי מתח גבוה | 10 | GA | – |
| קרינה מעמוד חשמל | 10 | GA | – |
| קרינה מלוח חשמל | 10 | GA | 4.06 |
| קרינה מחדר שנאים | 10 | GA | – |
| קרינה משנאי | 10 | GA | – |
| מרחק בטוח מקו מתח גבוה | 10 | L | – |
| קו מתח גבוה ליד הבית | 10 | L | – |
| מגורים ליד קו מתח גבוה | 10 | L | – |
| עמוד חשמל מתח גבוה ליד הבית | 10 | L | – |
| קווי מתח גבוה בישראל / קווי מתח גבוה מפה | 10 / 10 | L | – |
| פורום קרינה מעמודי חשמל מתח גבוה | 10 | L | – |
| בדיקת קרינה מתח גבוה | 10 | L | – |
| קווי מתח גבוה ליד הבית | no data | GA | – |

### 4. Measuring radiation, its price and the professionals

| Term | Volume | Src | CPC $ |
|---|---|---|---|
| מכשיר לבדיקת קרינה / מכשיר מודד קרינה / מכשיר למדידת קרינה / מודד קרינה / מד קרינה | 390 each (one cluster) | L | 1.92–2.16 |
| מדד קרינה (ambiguous with UV) | 320 | L | – |
| בדיקת קרינה / בדיקות קרינה | 110 / 110 | L | 6.00 |
| מיגון קרינה | 90 | L | 4.32 |
| מגן קרינה | 90 | L | – |
| מד/מודד קרינה אלקטרומגנטית (4 variants) | 90 each | L | 1.90–2.42 |
| בודק קרינה מוסמך | 70 | L | 3.00 |
| בודק קרינה | 50 | L | 3.26 |
| יועץ קרינה | 50 | L | 8.18 |
| מד קרינה ksp | 50 | L | 1.95 |
| בדיקת קרינה בבית | 40 | GA | 3.58 (competition MEDIUM) |
| מדידת קרינה | 10 | GA | 3.82 (competition HIGH, index 80) |
| בדיקת קרינה מחיר | 10 | GA | 9.56 |
| קרינה בבית / קרינה אלקטרומגנטית בבית | 10 / 10 | GA | – |
| מדידת קרינה מחיר | no data | GA | – |
| קרינה בדירה | no data | GA | – |
| בדיקת קרינה לפני קניית דירה | no data | GA | – |

### 5. Air pollution by city

| Term | Volume | Src | CPC $ |
|---|---|---|---|
| זיהום אוויר | 6,600 | L | 2.07 |
| זיהום אוויר בישראל לפי ערים | 1,000 | L | 0.01 |
| מדד זיהום אוויר | 1,000 | L | – |
| איכות אוויר | 880 | GA | – |
| זיהום אוויר היום | 880 | L | – |
| זיהום אוויר עכשיו | 720 | L | – |
| זיהום אוויר תל אביב | 720 | L | – |
| זיהום אוויר בישראל היום | 480 | L | – |
| מפת זיהום אוויר | 480 | L | – |
| תחזית זיהום אוויר | 390 | L | – |
| זיהום אוויר בישראל מפה | 390 | L | – |
| זיהום אוויר תל אביב עכשיו / בישראל / שוהם / חיפה | 260 each | L | – |
| דוח זיהום אוויר / זיהום אוויר בתל אביב / ניטור זיהום אוויר | 170 each | L | ניטור: 2.54 |
| מדד זיהום אוויר תל אביב / זיהום אוויר בירושלים / זיהום אוויר מפה | 140 each | L | – |
| זיהום אוויר באר שבע / דרגת, דרגות זיהום אוויר / רמת זיהום אוויר היום | 110 each | L | – |
| זיהום אוויר במפרץ חיפה / בחיפה / מודיעין / משרד הבריאות זיהום אוויר | 90 each | L | – |
| מדידת זיהום אוויר / מכשיר למדידת זיהום אוויר / מודד זיהום אוויר | 90 each | L | 1.33 |
| זיהום אוויר אשקלון / ראש העין / רמת גן / פתח תקווה / מחר | 70 each | L | – |
| זיהום אוויר בחיפה לפי שכונות | 70 | L | 3.43 |
| מפת זיהום אוויר ישראל / בישראל / חיפה | 70 each | L | – |
| זיהום אוויר חולון / הרצליה / אשדוד | 50 each | L | – |
| זיהום אוויר חדרה / רחובות / ראשון לציון | 40 each | L | – |
| בדיקת זיהום אוויר | 40 | L | 9.18 |

### 6. Noise

| Term | Volume | Src | CPC $ |
|---|---|---|---|
| רעש מטוסים | 70 (peak 110 in Jan 2026) | GA | – |
| תלונה על רעש | 70 | GA | – |
| מפגעי רעש | 50 | GA | – |
| מפת רעש מטוסים | 10 (40 in Nov 2025) | GA | – |
| מפת רעש | no data | GA | – |

### 7. "Where to live", "safe area" and hazard maps

| Term | Volume | Src | Note |
|---|---|---|---|
| govmap | 90,500 | GA | Navigational: the government map portal, which has the environment layer govmap.gov.il/sviva |
| מפגעים סביבתיים | 30 | GA | Same monthly curve as the next row, so one cluster |
| מפגע סביבתי | 30 | GA | |
| איפה כדאי לגור | 10 | GA | |
| איפה הכי טוב לגור בישראל | no data | GA | |
| הערים הכי טובות לגור בישראל | no data | GA | |
| מפת מפגעים | no data | GA | |
| תחנת דלק ליד הבית | no data | GA | |

### 8. Others (adjacent or off-topic; do not target)

| Term | Volume | Src | Why it is excluded |
|---|---|---|---|
| אינדקס קרינה | 8,100 | L | Sun UV index (seasonal: 22,200 in May 2026, 1,000 in Dec 2025) |
| אינדקס קרינה עכשיו / שבועי | 2,400 / 1,300 | L | UV |
| דה קרינה | 1,900 | L | Chocolate shop |
| נורת זיהום אוויר | 1,000 | L | Car warning light |
| אנטנה עידן פלוס | 480 | L | TV antenna product |
| קרינה ברכבים חשמליים / ברכב חשמלי | 140 / 140 | L | EV cabin radiation. Adjacent: the Ministry of Environmental Protection keeps a car-radiation database |
| מתח גבוה סרט | 140 | L | Film |

## What the numbers say

1. **Demand sits in two pools.**
   - Air pollution: now, by city, and maps. More than 15,000 searches a month across the cluster in the Labs data. These terms are near duplicates, so the real reach is lower than the sum.
   - Antenna location by address: 1,300 for the map plus 2,400 for the head term, plus a long tail.
2. **The fears have no head terms.** Power lines, transformer rooms, broadcast transmitters, noise and "where to live" are each 10 to 70 searches a month. They are a long tail around one page, not separate pages.
3. **Money sits in checking and measuring.** "בדיקת אנטנה סלולרית" has a CPC of $19.16, "בדיקת קרינה מחיר" $9.56, "בדיקת זיהום אוויר" $9.18 and "יועץ קרינה" $8.18. That is a lead-generation signal for certified radiation testers.
4. **Nobody searches the real-estate framing yet.** "בדיקת קרינה לפני קניית דירה" and "קרינה בדירה" returned no data. The page would create this intent rather than capture it, so its title has to lead with the searched words: antennas near the home, the antenna map, air pollution by city.
