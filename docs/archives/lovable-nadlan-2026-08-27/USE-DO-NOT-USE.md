# מה למחזר, מה להתאים ומה אסור להעתיק

## למחזר רעיונית

| רכיב | למה הוא טוב | איך משתמשים בו |
|---|---|---|
| היררכיית `/production/nadlan` | מתחילה במשימת המשתמש ולא ברשימת קטגוריות | מתרגמים לרכיבי WordPress הקיימים ולנתונים חיים |
| מסלולי קונה/מוכר/בודק עסקה | הופכים פורטל רחב לסדרת החלטות ברורה | כל צעד מקושר לכלי או עמוד קאנוני אמיתי |
| ארכיוני projects/properties | פילטרים, מצבי ריק והבחנה בין אמיתי לדמו ברורים | מחברים ל־CPT, taxonomy ו־REST של Nadlan |
| `Demo / Missing / Verified` | מונע מדמו להיראות כעובדה | מחליפים את `Verified` בסטטוס שמגובה במקור ובתאריך |
| כרטיס מקור ותאריך | נותן למשתמש דרך להבין מה ידוע | שדה קאנוני אחד, מוצג גם באדמין וגם בפומבי לפי הצורך |
| RTL, מובייל ונגישות | סדר קריאה ומגע טובים ברוב המסכים | מעתיקים tokens ודפוסים, לא את מעטפת React |
| internal linking לפי intent | מפחית קניבליזציה ומוביל לצעד הבא | מאמתים URL owner מול מפת האתר האמיתית |
| מצבי empty/loading/error | מונעים מסך שבור או מידע מומצא | נדרשים לכל widget שמחובר לנתונים |
| נרטיב הפגישה | מסכם מוצר, נתונים וחוסרים באופן קריא | משמש מסמך פנימי בלבד; נשאר `noindex` |

## למחזר רק לאחר התאמה

| רכיב | ההתאמה הנדרשת |
|---|---|
| `ProductionShell` | להפוך ל־shell אחד בתוך Nadlan; לא להוסיף header/footer מקוננים |
| חיפוש מהיר | כרגע הטופס עוצר submit. יש לחבר לחיפוש/REST אמיתי, URL state ואנליטיקה |
| ארכיון פרויקטים | להחליף arrays קשיחים ב־CPT/REST, מקור, תאריך ורמת שלמות |
| עמוד Rainbow | לשמר מבנה מקור/עובדות, אך לייבא מהעמוד וה־meta החיים ולא מערכי הדמו |
| עמוד נכס Baka demo | להשתמש כתבנית בלבד; כל המפרט והמדיה הם דמו |
| meeting / post-listing | לבנות endpoint, consent, upload validation, CRM וסטטוס הצלחה/כשל |
| map-first | לחבר Mapbox/Cesium הקיימים, נקודות אמיתיות ו־state משותף; אין מפה דקורטיבית |
| עיצוב cream/ink | לאחד עם tokens ונכסי Nadlan המאושרים; להוציא Unsplash ו־placeholder imagery |
| React/TanStack routes | לתרגם ל־PHP/templates/blocks או לאפליקציה מחוברת עם חוזה URL/SEO ברור |
| schema/canonical suggestions | לממש בשרת ולבדוק ב־View Source; טקסט בתוך אב־טיפוס אינו schema |

## אסור להעתיק כמקור אמת

- מחירי Rainbow, מספרי יחידות, זמינות, קומות או נתוני שוק הקשיחים בקוד Lovable.
- תמונות Unsplash או תמונות גנריות כאילו הן חומר רשמי של פרויקט.
- hotspot, floor picker, plan או map mockup כאילו הם כלי אינטראקטיבי עובד.
- CTA או טופס ש־`preventDefault()` עוצר אותו ללא endpoint, הודעת הצלחה ורישום ליד.
- badges מסוג `מאומת` ללא מסמך, תאריך, source owner ותהליך רענון.
- קישורים לנתיבי demo כ־canonical ציבורי.
- טקסטי SEO, FAQ או schema בלי בדיקת intent, ownership ו־HTML Source חי.
- React code ישירות לתוך WordPress בלי adapter, namespace, enqueue, cache, nonce, i18n ואימות compatibility.
- נתוני Strategy Hub הישן כעובדות; הוא מאגר היסטורי ורעיוני בלבד.
- כל secret, token, cookie, environment file או browser profile, גם אם הופיע בייצוא.

## כלל WordPress

היישום העתידי צריך לשמור על WordPress כמקור התוכן וה־SEO, ועל מנועי Nadlan הקיימים כמקור לאינטראקציה. Lovable מספק wireframe, היררכיה ורעיונות קומפוננטה; הוא אינו מחליף את `nadlan_project`, שדות ה־meta, REST, engine.js, Mapbox, lead routing או analytics.

## כלל 3D ויחידות

יכולת מסומנת כעובדת רק אם אותו `unit_id` נשמר לאורך השרשרת: בניין/mesh או anchor → בחירה → כרטיס → תוכנית → מפה/כיוון → מראה מהחלון → ליד. שום מיקום CSS, מספר קומה קשיח או תמונת תוכנית לא מהווים הוכחה לכך.
