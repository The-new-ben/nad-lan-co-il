# ביקורת עצמית

## איפה העבודה הקודמת הייתה לא מספיק טובה

1. היא נתנה למעבדת CSS מעמד של חוויה מעשית, אף שהאתר כבר החזיק Mapbox/beam, Studio, RFP, Co-tour ו־Cesium. זה יצר “שיפור” שחתך יכולות במקום לשמרן.
2. היא סימנה facilities לפי רשומות ותמונות, לא לפי renderer, click ו־anchor. עשרה מתקנים אפילו מחזרו אותה תמונה.
3. היא הציגה צ׳ק־ליסט עשיר במספרים, אך חלק מהירוקים היו hardcoded או הסתפקו בשדה קיים. 138 בדיקות אינן שוות הרבה אם קליק אינו ראיה.
4. היא יצרה hotspot positions באחוזי CSS על SVG במקום להוכיח mesh/node/anchor.
5. היא לא זיהתה שה־prototype hard-coded לפוסט/slug אחרים ולכן המתכון וה־BOM לא הופיעו בפוסט החי.
6. היא לא זיהתה את ה־inline adapter החי שאינו בריפו ומסתיר 320 hotspots.
7. היא לא זיהתה את cache split-brain; לכן היה קל לפרש runtime לא עקבי כעוד בעיית layout.
8. היא לא ראתה ש־engine דורס title SEO תקין.
9. היא קראה ל־flat background pan “סיור” ולא דרשה room graph.
10. היא קראה ל־WhatsApp “שיחת וידאו” ולא הוכיחה media API.
11. היא לא בדקה שה־Studio משתמש בתוכנית אמיתית; הוא משתמש במלבנים סינתטיים.
12. היא לא עקבה עד RFP schema כדי לראות ש־studio snapshot נשמט.

## איפה גם החבילה הנוכחית עדיין אינה סוף הדרך

1. 12 הפנורמות מלאות כ־media, אך GLB הקיים עדיין אינו מכיל facility nodes. לכן model hotspots אינם ירוקים.
2. scene hotspot labels הוגדרו, אך yaw/pitch טרם authored לכל תמונה. לא סימנו אותם ירוק.
3. לא נוצרו 320 window-view assets או view cameras; זה דורש מקור תכנון/geo או pipeline render.
4. לא נבנה room graph לכל טיפוס דירה; הסיור החי עדיין לא הוחלף.
5. לא הוטמע Studio geometry/BOM בפועל.
6. לא הותקן conference provider.
7. לא נכתבו 5,000 מילים של מאמר שיווקי סופי בחמש שפות.
8. לא נבדק lead submit אמיתי, בצדק, משום שלא היה אישור בזמן פעולה לשליחת data.
9. לא ניתן להוכיח favicon ב־SERP באמצעות Source בלבד.
10. הקוד reference אינו production patch; הוא דורש review ושילוב בתוך core.

## למה זו בכל זאת קפיצה משמעותית

- הופרדו עובדה חיה, חוזה יעד ונכס generated.
- נמצאו שורשי runtime/cache/title ולא רק סימפטומים חזותיים.
- הקוד האמיתי של map/beam נשמר ונקשר למתכון.
- כל מתקן קיבל asset נפרד, ID, data/BOM ומסלול הפעלה.
- המתכון הפך ל־737 בדיקות עם evidence policy.
- ה־Source fingerprint יציב ואינו שומר raw sensitive snapshot.
- WordPress קיבל תכנית migration/rollback במקום ZIP שנראה installable אך חסר assets/importer.

## מבחן היושר

אם שואלים “האם יש לנו כבר דף מושלם?” — לא.

אם שואלים “האם עכשיו יודעים בדיוק למה הדף החי קשה, איזה קוד לשמר, מה חסר, איך ייראה המסלול, אילו נכסים נדרשים ואיזו ראיה תאפשר נורה ירוקה?” — כן, ברמה גבוהה בהרבה מהגרסה הקודמת.
