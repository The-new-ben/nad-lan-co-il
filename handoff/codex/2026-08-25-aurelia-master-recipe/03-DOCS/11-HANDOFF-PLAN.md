# תוכנית מסירה לצוות

## סבב 1 — חוזה לפני UI

קוראים `data/wordpress-contract.json`, `data/unit-selection-audit.json` ו־`docs/12-UNIT-SELECTION-SCIENTIFIC-SPEC.md`. מאשרים ש־`unit_id` יחיד הוא המפתח של model, card, plan, map, panorama, studio, lead ו־Co-tour. אין dataset מקביל.

## סבב 2 — Preview מוגבל

מתקינים adapter 0.5.0 ב־staging/preview בלבד. מאמתים שהוא פועל רק על post 7304. טוענים את GLB v2 ואת הנתונים; אין שינוי ל־Rainbow, DO, Dimri Yama או Ashira.

## סבב 3 — חתך אנכי

מריצים: רשימה → hotspot → tap משטח → כרטיס → תוכנית → Mapbox/אלומה → נוף → פנים → חזרה. בכל צעד רושמים את `unit_id`; כל סטייה היא נורה אדומה. אחר כך בודקים studio, lead ו־Co-tour.

## סבב 4 — viewport ושפה

1440, 390, 320; עברית, אנגלית, צרפתית, רוסית וערבית. בודקים בניין גלוי, target 44px, כרטיס שאינו מכסה, swipe ללא root overflow, focus ו־ESC.

## סבב 5 — HTML ציבורי

מפעילים “צילום View Source ציבורי עכשיו”, משווים hash וחלקים ל־baseline, ובודקים title, description, H1, canonical, hreflang, favicon, JSON-LD, menu, duplicate IDs, scripts ו־styles. כל ממצא צף גם אם אינו שייך ישירות לשורום.

## סבב 6 — קוד ושינוי

כל שינוי ב־engine/mapbox/studio/buyflow/adapter משווה SHA-256 ו־critical needle דרך `data/code-evidence.json`. צהוב מחייב diff; כתום פירושו שהחיבור נעלם. אחרי אישור מעדכנים baseline עם בעלים ותאריך.

## סבב 7 — הרחבה לצי

רק לאחר שהאב עובד, בונים מטריצת פערים לכל פרויקט חי ומעבירים יכולת אחת בכל פעם. לא מוחקים יכולת קיימת רק מפני שאינה במתכון; ממפים אותה, בוחרים מימוש קאנוני ומריצים replay.
