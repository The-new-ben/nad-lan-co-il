# מה נעשה ולמה — יומן החלטות

## נקודת המוצא

המטרה לא הייתה “לעצב דף יפה”, אלא להוציא מן הפרויקטים החיים מתכון שאפשר להוכיח. Rainbow, DO, Dimri Yama ו־Ashira שימשו מקור אמת ליכולות: 3D, יחידות, Mapbox/אלומה, תוכניות, פנים, facilities, studio, buyflow ו־Co-tour. הוחלט שלא למחוק קוד חי או להחליף יכולת ב־CSS demo.

## מה נשמר מן המערכת

- `engine-current.js`: יחידות, hotspots, selectUnit, adoption של המפה והאלומה.
- `mapbox-init-current.js`: Mapbox, token וקואורדינטות.
- `studio-current.js`: בחירות, notes, export ו־video.
- `buyflow-current.js`: lead/RFP והקשר דירה.
- `mv-ux-current.js`: מצלמה, detents ומצפן.
- `i18n-current.js`: חמש שפות פונקציונליות.

לכל קובץ נשמר hash מלא וקטעי קוד קריטיים.

## מה נמצא בבדיקה הפורנזית

1. מפת הפרויקט והאלומה הן יכולת אמיתית בקוד, לא רעיון עיצובי. `engine.js` מעביר את המפה מיד אחרי הבניין ומסובב marker לפי הדירה.
2. hotspot קיים ב־engine כ־`model-viewer` annotation עם position/normal ו־unit ID.
3. בחירה קיימת מזינה Mapbox, plan, studio וטופס; צריך להיכנס דרך הנתיב הזה ולא לעקוף אותו.
4. ב־GLB של המעבדה גובה הקומה במודל הוא 3.05m, לא 3.35m. השימוש בגובה האדריכלי יצר drift מצטבר.
5. source ציבורי של Rainbow כולל ארבע הצהרות favicon, שני owners ל־schema ועומס assets—ממצאים שאינם נראים בצילום מסך.

## מה נבנה

- GLB v2 עם 320 `UNIT_ANCHOR` nodes ו־extras מלאים.
- compiler שמוסיף selection contract לכל 320 היחידות.
- validator שמאמת anchors, bounds, normals, floor bands ו־legacy prohibition.
- surface resolver שנשען על פגיעה אמיתית בגאומטריה.
- projected overlay נגיש עם occlusion probe.
- adapter נוסף ל־Three.js semantic meshes לפרויקטים עתידיים.
- store ואירוע יחיד ששומרים `unit_id` ב־URL ובכל הצרכנים.
- מסך Selection עם 67 בדיקות; מסך Source עם fingerprints; code evidence עם hashes ו־needles.
- תוסף WordPress 0.5.0 שמגשר אל המנוע הקיים ושומר View Source ציבורי.
- viewport harness נפרד שאינו משנה את הדמו.

## מה תוקן תוך כדי הוכחה

- העוגנים הוזזו ל־model pitch הנכון.
- click handler הועבר ל־pointer capture כדי להבדיל tap מ־drag בתוך Shadow DOM של model-viewer.
- auto rotate הוסר; סיבוב לחזית הוא פעולה מפורשת.
- unit שאינו ברשימת 70 הראשונות נשמר במלאי לאחר בחירה.
- ב־390/320 הכרטיס הועבר לזרימה מתחת לבניין.
- scrollbars אופקיים שהתגלו ב־screenshots הוסתרו, swipe נשמר ו־root overflow בוטל.
- code evidence הורחב מ־15 ל־20 bindings: selection, map, studio, buyflow, i18n, model UX, WordPress ו־Source.

## תוצאת replay

- desktop surface: `aur-t-24-a`.
- projected hotspot: `aur-g1-02`.
- mobile 320 surface: `aur-t-29-b`.
- mobile map: B, floor 29, 4 rooms נשמרו.
- DOM: 24/24; code fingerprints: 20/20; data: 22/22.

## החלטות שלא הוסתרו

- `UNIT_PICK` meshes אינם קיימים עדיין, לכן Tier A צהוב.
- WordPress preview לא הותקן, לכן התשתית החיה כתומה.
- אין טקסטי המתנה בדמו; חסרים פנימיים אינם מוצגים לרוכש.
- מחירים בדמו הם חלק מחוזה היחידה; אופי הצגתם לציבור נשאר החלטת בעל האתר.
- המתכון אינו publish blocker. הוא מערכת נורות, ראיות ו־diff.
