# הפערים עד למוצר אמיתי

## תמונת מצב

Design Lab מדגים היטב איך אפשר לסדר מידע, אך הוא אינו מחובר למערכת העסקית או המרחבית של Nadlan. הפער המרכזי אינו עוד CSS; הוא חיבור עקבי בין נתונים, אינטראקציה, SEO, לידים וראיות.

| תחום | מה קיים בארכיון | מה חסר ל־production | ראיית השלמה נדרשת |
|---|---|---|---|
| זהות ו־brand | shell, RTL, cream/ink, היררכיה | token system אחד, assets מאושרים, ללא shell כפול | השוואת desktop/mobile לבית ולפרויקט חי |
| תמונות ונכסים | מעט favicon/asset מקומי; ב־Strategy Hub גם placeholders | hero, gallery, facilities, floorplans ו־rights לכל פרויקט | asset manifest עם source, rights, hash ו־slot |
| 3D | layout ורעיונות showroom | GLB אמיתי, LOD, poster, camera, mesh/anchor סמנטי | click evidence על מודל אמיתי בשלושה viewports |
| יחידות | כרטיסים ומספרים קשיחים | inventory export ו־`unit_id` יציב | crosswalk מלא ו־refresh owner |
| תוכניות | ייצוגים/תמונות היסטוריים | site/floor/unit plans, צפון, קנה מידה, זום ונגישות | plan_id שמחובר ל־unit_id |
| בחירת דירה | UI רעיוני | mesh/hotspot → unit → card → plan → map → view | אותו unit_id בכל event וב־lead payload |
| facilities/amenities | cards או לוח תמונה | registry, מיקום, מפלס, מפרט, שעות, נגישות, hotspot ומדיה | facility_id + source + click עובד |
| סביבה ומפה | רעיון map-first | Mapbox חי, נקודת פרויקט, POI, זמני הליכה, azimuth ונוף | state משותף עם בחירת היחידה |
| סיור וקול | references היסטוריים | 360/POV, narration manifest, subtitles ושמירת state | מסלול בדפדפן ללא reset של היחידה |
| סטודיו/BOM | אינו ממומש ב־Design Lab | מפרט דירה, options, pricing policy, export/send | BOM version + payload + receipt |
| CRM ולידים | CTAs וטפסים חזותיים | endpoints, routing, consent, SLA, spam control, CRM join | lead success בשרת עם project_id/unit_id |
| פגישה/וידאו | עמוד נרטיב ו־meeting mock | calendar/video integration, timezone, confirmation/cancel | booking receipt ו־analytics event |
| WordPress | הערות handoff בלבד | CPT/meta/REST adapter, templates/blocks, enqueue/cache/nonces | staging plugin + Source + regression checks |
| SEO | titles, descriptions והצעות canonical בקוד | SSR head, canonical, hreflang, schema, sitemap, snippet strategy | View Source ו־rich-results/schema validation |
| i18n | RTL ועברית חזקים; Strategy Hub כולל חלק מאנגלית | חמש שפות מלאות, URL siblings, labels, assets ו־fallback | route/source matrix לכל שפה |
| analytics | כמעט אין אירועי product | event dictionary ממומש, IDs, lead success ו־CRM attribution | GA4 DebugView/Data API + lead-ledger join |
| data pipeline | arrays ו־mock data | source adapters, freshness, errors, cache ו־owner | scheduled refresh + provenance receipt |
| פרטיות/אבטחה | אין מערכת מלאה | consent, retention, roles, PII boundaries, upload controls | security/privacy review לפני חיבור טפסים |
| בדיקות | תצלומים והערות | 1440/390/320, clicks, keyboard, performance, Source fingerprint | evidence per requirement, לא “אמור לעבוד” |

## פערים מיוחדים למיני־סייט EcoCity

כדי להפוך את התבנית למיני־סייט אמיתי נדרשים בנוסף:

1. זהות מאושרת של הפרויקט, היזם, האדריכל, הקבלן, הכתובת והסטטוס.
2. export יחידות וזמינות עם מזהה יציב.
3. BIM/IFC/CAD או GLB עם מזהי בניין, קומה ויחידה.
4. תוכניות אתר, קומות ודירות.
5. רשימת מתקנים מלאה עם BOM, מיקום ומדיה.
6. assets רשמיים והיתר שימוש.
7. יעד ליד, WhatsApp/email/CRM/calendar/video conference ו־SLA.
8. החלטת שפות ואישור תרגומים.
9. analytics שמחבר landing → unit → lead → meeting/עסקה.

## מה אפשר לבנות בלי להמציא עובדות

אפשר לבנות shell, ניווט, מצבי empty/error, contracts, source cards, תבניות תוכן, adapter ל־WordPress ומנגנון בדיקה. אפשר גם ליצור הדמיות שמסומנות כ־concept. אי אפשר להצהיר על יחידה, כיוון, זמינות, מחיר רשמי, facility או תוכנית ללא חומר מתאים.

## סדר סגירת הפערים

1. data/asset manifest ומקור אמת.
2. WordPress adapter ו־URL/SEO contract.
3. מסלול אנכי אחד אמיתי של יחידה.
4. facilities וסביבה.
5. lead/meeting ו־analytics.
6. שפות, ביצועים ונגישות.
7. הרחבה לפרויקטים נוספים רק לאחר ראיות דפדפן.
