# מפת יישום ל־WordPress

## עיקרון

מיישמים את המוצר באמצעות תבניות ובלוקים reusable. לא מעתיקים צילום מסך ולא בונים HTML קשיח לכל עמוד.

## גבול Theme / Plugin

### Theme

- tokens, typography, spacing ו־layout.
- header, footer ו־mobile drawer.
- archive/detail templates.
- cards, filters, breadcrumbs ו־CTA presentation.

### `nadlan-config` Plugin

- fields ו־meta contracts.
- REST/AJAX, permissions ו־validation.
- seeded/verified state.
- analytics events.
- schema values המבוססים על נתונים אמיתיים.
- advisory checklist לעורך.

## תבניות

| URL family | תבנית | בלוקים מרכזיים |
| --- | --- | --- |
| `/projects/` | Project archive | hero, filters, hub links, project cards, load more |
| `/projects/{slug}/` | Project detail | facts, media, 3D, units, map, facilities, sources, contact |
| `/properties/` | Property archive | intent header, filters, state label, listing cards, load more |
| `/properties/{slug}/` | Property detail | gallery, facts, verified availability, source, contact |
| `/post-listing/` | Supply funnel | explanation, form steps, preview, submission status |

## חוזה נתונים לפרויקט

שדות ליבה מומלצים:

- `source_name`, `source_url`, `source_accessed_at`
- `content_state`: `seeded`, `verified`, `archived`
- `total_units`
- `demo_units`
- `verified_available_units`
- `price_source`, `price_as_of`
- `planning_status`, `planning_source_url`
- `developer_name`, `developer_source_url`
- `asset_owner`, `asset_license`, `asset_version`
- `three_d_fallback_image`

## צ'ק־ליסט פנימי

הצ'ק־ליסט מציג `עבר`, `מומלץ לשפר` או `חסר`. הוא רשאי לחשב ציון ולהפנות לשדה, אך:

- אינו חוסם Save.
- אינו חוסם Preview.
- אינו חוסם Publish.
- אינו מחייב עורך להכניס ערך פיקטיבי.

דוגמה טובה: `אפשר לפרסם. מומלץ להשלים מקור לתחזית האכלוס.`

דוגמה רעה: `הפרסום חסום עד שכל 24 השדות מלאים.`

## ביצועים

- route-scoped assets בלבד.
- lazy loading ל־3D ולגלריות.
- fallback לכל מודל.
- pagination או virtualization לרשימות יחידות גדולות.
- תמונות AVIF/WebP עם מידות ידועות.
- אין מאות כרטיסים חוזרים ב־DOM הראשון.

## Accessibility ו־RTL

- logical CSS properties בלבד.
- focus גלוי ומלא.
- labels אמיתיים לפילטרים.
- `prefers-reduced-motion` ל־3D ואנימציות.
- contrast ברמת AA לפחות.
- QA ב־390, 768 ו־1440.

## Release

1. branch חדש מ־`origin/main`.
2. implementation קטן לפי template family.
3. PHP lint ו־JS syntax.
4. צילום לפני/אחרי.
5. build של plugin ZIP רק אם plugin השתנה.
6. PR ל־review; לא merge עצמי.
7. deploy רק לאחר merge והוכחת signature חי.

החבילה הנוכחית אינה משנה את האתר החי ואינה דורשת deploy.
