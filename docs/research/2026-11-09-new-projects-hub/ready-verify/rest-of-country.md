# Ready-to-move check, rest of the country (outside Tel Aviv-Yafo)

Checked 9.11.2026. Input: `plugins/nadlan-config/data/projects-market.json` (read 25.10.2026), the 58 rows with status `immediate` or `near_occupancy` outside תל אביב-יפו, in 29 cities. Row-by-row evidence: `rest-of-country.json` in this folder.

## Headline

- **Confirmed immediate: 37** (all 37 were `immediate` in the input).
- **Confirmed near occupancy: 9** (all were `near_occupancy` in the input).
- **Changed status: 12.** 11 rows marked `immediate` are only near occupancy today, and 1 `near_occupancy` row cannot be confirmed (now `marketing`).
- **Not found: 0.** Two projects no longer have a Yad2 marketing page (רובע איילון, בריגה ארט). Both were confirmed from other sources: a news report and the developer's own page.
- **Blocked: 0 left.** Yad2 blocks automated fetches (Radware "verifying your browser" page). I read every Yad2 page in the owner's own Chrome as a normal visitor. No CAPTCHA appeared and nothing was bypassed. No Madlan page was needed.
- **Sources used:** 15 developer pages, 38 Yad2 project pages (each one placed by the developer), 4 nadlan.com pages, 1 news report. Some developers have no project page or publish no status on it (Shviro, Amram, Bonei HaTichon, Matzlawi, CREATE). For many smaller developers I did not search for a site at all. In those cases the Yad2 listing is the source, and the notes say so.

## Main finding: the Yad2 flag means "near", not "immediate"

Yad2 has an occupancy flag (`immediateOccupancy`), but on its project cards that flag is displayed as **"אכלוס קרוב"** (near occupancy). The 25.10 build seems to have treated the flag as "immediate" whenever the listing had no date. That explains most of the changed rows. In this check, a row counts as immediate only when the page says so in words (אכלוס מיידי, כניסה מיידית, מפתח עכשיו, מאוכלס, באכלוס), or when the developer's own date has passed and the page says it is ready. In two cases (שבירו בגני תקווה and שבירו בראש העין) the only evidence is Yad2's own project status "פרוייקט מאוכלס".

## Status changes (12)

| Project | City | Input | Today | Why |
|---|---|---|---|---|
| AQUA RESORT | אילת | immediate | near_occupancy | Only the "אכלוס קרוב" flag; no date; still under construction |
| אייל פרץ בפארק | באר שבע | immediate | near_occupancy | Phase A occupied since 2024; construction continues; no date for units now on sale |
| טורקיז | ג'סר א זרקא | immediate | near_occupancy | Date 07/2026 has passed, but the page's own stage still shows construction under way |
| NEXT טירת הכרמל | טירת כרמל | immediate | near_occupancy | Text says only "אכלוס קרוב" |
| רמותיים | ירושלים | immediate | near_occupancy | "לאכלוס של כשנה" |
| שדרות היובל | ירושלים | immediate | near_occupancy | "מגוון מועדי אכלוס", no date |
| PATIO בן שמן | לוד | immediate | near_occupancy | Page still says "אכלוס קרוב" and "06/26" |
| פסגות אור נתניה | נתניה | immediate | near_occupancy | Now "אכלוס פברואר 2027" (input said 12/2026) |
| ביאליק 8 פתח תקווה | פתח תקווה | immediate | near_occupancy | "אכלוס בקרוב", page last updated 29.7.2026 |
| רוטשילד פתח תקווה | פתח תקווה | immediate | near_occupancy | Developer text says "אכלוס קרוב" |
| CREATE - קריאייט | קריית אתא | immediate | near_occupancy | Flag only; no date; no price |
| גרופית בשמורה | פרדס חנה-כרכור | near_occupancy | marketing | The "תוך כ-10 חודשים" line is gone; only "וילות אחרונות!" |

## Every label mismatch (10)

1. **אייל פרץ בפארק, באר שבע:** input says immediate. The page says phase A has been occupied since 2024 and construction continues, and the units on sale carry only "אכלוס קרוב".
2. **טורקיז, ג'סר א זרקא:** the published date 07/2026 has passed, but the page's stage is "ניתן היתר בניה", the registry says "בתהליך בניה", and there is no "אכלוס מיידי" text.
3. **NEXT טירת הכרמל:** input says immediate; the page says "אכלוס קרוב", no date.
4. **רמותיים, ירושלים:** input says immediate; the page says "לאכלוס של כשנה".
5. **שדרות היובל, ירושלים:** input says immediate; the page says "מגוון מועדי אכלוס" and the project is under construction.
6. **PATIO בן שמן, לוד:** input says immediate with 06/2026. On 5.11 the page still said "אכלוס קרוב" and "האכלוס לא רחוק … 06/26".
7. **גלי נתניה:** the developer's tag says "אכלוס מיידי", but the same page says building 2 is planned for 2027. Only units in building 1 can be immediate.
8. **פסגות אור נתניה:** input says immediate with 12/2026; the page now says February 2027 and "הבנייה בעיצומה".
9. **ביאליק 8, פתח תקווה:** input says immediate. The page says "אכלוס בקרוב" with 08/2026 and has not been updated since 29.7.2026.
10. **רוטשילד פתח תקווה:** input says immediate. The developer's text says "אכלוס קרוב", while the Yad2 registry says "פרוייקט מאוכלס".

Unknown (no date and no clear wording): AQUA RESORT, CREATE, גרופית בשמורה.
Dates that passed without a page update (kept as near occupancy): שינקין 46 גבעתיים (10/2026), סמטת המעלות 3 רמת השרון (Q3/2026).

## Every price that changed vs the input

| Project | City | Input | Today | Rooms |
|---|---|---|---|---|
| סטורי גלי ים | נתניה | 2,760,000 | 2,860,000 | 5 |
| פטיו ירושלים 28-30 | נתניה | 4,650,000 | 4,180,000 | 4, last penthouse |
| פסגות אור נתניה | נתניה | 4,190,000 | 3,350,000 | 3 (a 5-room is 4,190,000) |
| הרימון | קריית אונו | 3,350,000 | 3,900,000 | 4, penthouse (nadlan.com still shows 3,350,000, stale) |
| Tel Mond Collection | תל מונד | 5,290,000 | 4,290,000 | 6, garden (headline still says 5,290,000; text and unit table say 4,290,000) |
| אפגד באגמים | אשקלון | 1,585,000 | not published | only penthouses left |
| CREATE - קריאייט | קריית אתא | 1,920,000 | not published | |

The other 35 input prices are still published unchanged. Three of them are now tied to a specific room count: אייל פרץ (4 rooms), צרפתי בפארק (5 rooms) and רובע הנשיאים (3-room garden). אומאמי still shows 2,990,000 for 3 rooms, but its text says only 4 and 5 rooms remain (from 3,690,000).

## Other things to fix before publishing

- **שבירו ודוראל ביבנה:** the text says the 5 and 6 room units are "יד שנייה ישירות מהקבלן" (second-hand homes sold by the contractor). These are not new apartments.
- **רובע איילון, בת ים:** a news report (Funder, 28.10.2026) says phase A received its completion certificate and 47 units remain. The developer's page still says "בבנייה" and there is no live listing, so there is no price or room mix.
- **Addresses that differ from the input:** אפגד באגמים (now שדרות עמק יזרעאל 68), עין צורים (number 4, not 6), שבירו בראש העין (now שבזי 201), הרימון (now הרימון 1, neighbourhood קיראון), טורקיז and רמותיים (no house number today).
- **Rooms that shrank:** העצמאות הרצליה has no penthouses left. רובע הברון and הרימון have only penthouses left. פטיו ירושלים has one penthouse left. פרשקובסקי נופי בן שמן has two units left. מיתר בקריה האקדמית has two mini penthouses left.
- **Weak "immediate" evidence:** רוטשטיין הקוטג'ים (label "מאוכלס" only, no stock count), מגדל הצוק II (date 07/2025, but the page does not say any units are left), בריגה ארט (no date; developer says the units are ready to move into), רובינא הירוקה (Form 4 per a 2024 article; developer page has no status).

## Counts per city (verified status)

| City | Rows | Immediate | Near | Marketing |
|---|---|---|---|---|
| נתניה | 8 | 6 | 2 | 0 |
| הרצליה | 5 | 5 | 0 | 0 |
| פתח תקווה | 5 | 3 | 2 | 0 |
| ירושלים | 4 | 0 | 4 | 0 |
| באר יעקב | 2 | 1 | 1 | 0 |
| באר שבע | 2 | 1 | 1 | 0 |
| בת ים | 2 | 1 | 1 | 0 |
| גבעתיים | 2 | 1 | 1 | 0 |
| לוד | 2 | 1 | 1 | 0 |
| פרדס חנה-כרכור | 2 | 1 | 0 | 1 |
| קריית אונו | 2 | 2 | 0 | 0 |
| קריית אתא | 2 | 1 | 1 | 0 |
| רמת גן | 2 | 2 | 0 | 0 |
| רמת השרון | 2 | 1 | 1 | 0 |
| רעננה | 2 | 1 | 1 | 0 |
| אור יהודה | 1 | 1 | 0 | 0 |
| אילת | 1 | 0 | 1 | 0 |
| אשקלון | 1 | 1 | 0 | 0 |
| ג'סר א זרקא | 1 | 0 | 1 | 0 |
| גני תקווה | 1 | 1 | 0 | 0 |
| חיפה | 1 | 1 | 0 | 0 |
| טירת כרמל | 1 | 0 | 1 | 0 |
| יבנה | 1 | 1 | 0 | 0 |
| כפר סבא | 1 | 1 | 0 | 0 |
| נהריה | 1 | 0 | 1 | 0 |
| נס ציונה | 1 | 1 | 0 | 0 |
| ראש העין | 1 | 1 | 0 | 0 |
| ראשון לציון | 1 | 1 | 0 | 0 |
| תל מונד | 1 | 1 | 0 | 0 |
| **Total (29 cities)** | **58** | **37** | **20** | **1** |

## Method and limits

- Each row was read on 9.11.2026. Prices, dates and deals are recorded only where a page showed them that day. Where a page showed no number, the field is empty and nothing was carried over from the input.
- Yad2 values were read from the page's own data (project name, address, "החל מ" price, unit table, the developer's text, the entrance date, Yad2's registry status and the last-update time).
- No deal text on any page carried an expiry date, so `deal_expiry` is empty everywhere.
- No forms, sign-ups or messages were sent. Nothing on any site was changed.
