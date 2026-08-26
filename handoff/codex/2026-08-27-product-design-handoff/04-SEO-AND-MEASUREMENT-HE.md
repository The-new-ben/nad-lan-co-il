# SEO, מקורות ומדידה

## URL ownership

- `/projects/` מחזיק intent של גילוי והשוואת פרויקטים.
- `/projects/{slug}/` מחזיק entity יחיד של פרויקט.
- `/properties/` מחזיק intent של listings.
- `/properties/{slug}/` מחזיק נכס יחיד.
- כלי מס רכישה, סימולטור מס רכישה, מס שבח ונסח טאבו נשארים יעדים נפרדים.

## דרישות index

לכל URL מאונדקס:

- H1 יחיד.
- Title ו־Meta ייחודיים.
- Canonical self-referencing יחיד.
- Breadcrumb visible + BreadcrumbList.
- Schema שתואם לתוכן הגלוי.
- קישור פנימי מ־hub או pillar מתאים.

מסלול פגישה פנימי, preview ועמודי facet לא נבחרים צריכים להישאר `noindex` לפי מדיניות אחת, לא החלטות נקודתיות.

## Seeded / Demo

Seeded הוא מצב תוכן לגיטימי במעבדת מוצר, אך אינו מקור נתונים. עד אימות:

- מציגים `נכס הדגמה` או `פרופיל דמו`.
- אין `verified`, ביקורות, דירוגים או זמינות מומצאת.
- אין `Offer` או availability ב־Schema אם אינם אמיתיים.
- אין להסתיר את מצב ההדגמה, אך גם אין להציג warning אגרסיבי בכל כרטיס.

## מקורות

לכל עובדה מסחרית או תכנונית:

- source name.
- resolvable URL.
- accessed date.
- method כאשר מדובר בחישוב.
- freshness date.

`nadlan-flagship` לבדו אינו מקור בר־אימות.

## מדידה עסקית

אירועים מומלצים:

| Event | משמעות |
| --- | --- |
| `project_view` | צפייה בפרויקט |
| `unit_select` | בחירת יחידה במודל/רשימה |
| `facility_open` | פתיחת facility או 360 |
| `listing_view` | צפייה בנכס |
| `filter_use` | שימוש בפילטר |
| `contact_start` | התחלת פנייה |
| `listing_submit` | שליחת נכס |
| `meeting_path_complete` | השלמת מסלול ההדגמה |

המדד העסקי אינו pageview בלבד. סדר העדיפויות נקבע לפי פנייה מתאימה, בחירת יחידה, lead איכותי והכנסה, לצד crawl ו־ranking.

## 410 וקניבליזציה

אין לבצע 410 על בסיס הדגמה או תחושת כפילות. מועמד ל־410 דורש יחד:

1. אפס ערך GSC משמעותי לאורך תקופה מספקת.
2. אין conversion.
3. אין backlinks איכותיים.
4. אין תפקיד במבנה.
5. עמוד אחר מחזיק בבירור את אותו intent.
6. אין צורך להעביר signals.

עד לקבלת מטריצה כזאת, שומרים את החלטת המחיקה פתוחה.
