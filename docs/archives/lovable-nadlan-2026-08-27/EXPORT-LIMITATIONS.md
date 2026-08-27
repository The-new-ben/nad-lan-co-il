# מגבלות הייצוא

## מה הייצוא כן מוכיח

- מזהי שני פרויקטי Lovable, מצב הפרסום ו־commit refs שסיפק ה־connector.
- snapshot של הקבצים שה־connector החזיר באותו ref.
- מבנה routes, רכיבים, mock data ו־assets שנמצאים בקוד.
- תצפית חזותית בנקודת זמן על הנתיבים שנפתחו בדפדפן.
- קיום הקבצים ההיסטוריים בריפו בבסיס Git שנרשם.

## מה הייצוא אינו מוכיח

- שה־preview הפרטי יישאר זמין בעתיד.
- שהקוד עבר build נקי, בדיקות end-to-end או התאמת WordPress.
- שטופס, חיפוש, meeting, CRM, 3D, מפה או lead routing פועלים רק מפני שהם מופיעים במסך.
- שנתון קשיח או תמונה הם רשמיים, מעודכנים או מורשים לשימוש.
- שה־canonical/schema/hreflang שהוזכרו בהערות אכן נמצאים ב־HTML הציבורי.
- שהאתר החי Nadlan זהה ל־snapshot. בעת הארכוב production דיווח גרסה חדשה יותר מבסיס הריפו.

## Design Lab

הפרויקט private/unpublished. ה־preview הוא סביבת בדיקה, לא אתר ציבורי. קבצי source נשמרו לפי ref שה־connector סיפק; אין Git/domain/WordPress integration מוכחים. ה־manifest מצהיר על 100 קובצי טקסט וקובץ בינארי אחד. כל 100 קובצי הטקסט נשמרו; `public/favicon.ico` לא היה ניתן לייצוא נאמן ולכן אינו בארכיון. screenshot אינו לוכד hover, keyboard, network payload או כל מצב פנימי.

## Strategy Hub

האתר מפורסם לציבור, אך פרויקט העורך עצמו מסומן private. הוא מכיל כמה דורות של handoff, snapshots וקבצים כפולים. חומרי placeholder ונתונים קשיחים נשמרו לשם היסטוריה בלבד. ה־manifest מצהיר על 436 קובצי טקסט ו־79 קבצים בינאריים; כל קובצי הטקסט התקבלו, אך 67 קובצי PNG ו־12 קובצי JPG לא היו ניתנים לייצוא נאמן ולכן אינם בארכיון.

ב־`handoff/lovable/2026-06-23-war-room-sync/source-manifest.md` שדה source commit נותר `_auto_`; לכן הוא אינו commit provenance מאומת. `prototype-source/README.md` מגדיר את הקוד כ־focused snapshot ולא checkout מלא, ומציין ש־`/models/rainbow.glb` לא נכלל.

## ChatGPT handoff

לא קיים export מובנה ומלא של כל שיחת `NADLAN`. נשמרו שני קבצים מפורשים שהיו זמינים כקבצי attachment: complete bundle ו־Plan Mode transcript. קובץ transcript גדול אחר לא הועתק מפני שהוא ערבב פרויקטים ושיחות שאינם Nadlan; הארכיון לא מעתיק מידע חוצה־פרויקטים רק כדי לטעון שהוא “מלא”.

ה־bundle נטען משיחה פרטית ואינו קובץ שהיה קיים ב־Git בבסיס הארכוב. הוא מסומן בהתאם ב־provenance.

## Screenshots

- נשמרו 11 צילומי desktop, אחד לכל 11 מסלולי Nadlan המרכזיים ב־Design Lab.
- לא נשמרו צילומי mobile ולא נשמרו צילומי Strategy Hub. הכיסוי החסר מסומן ב־`ROUTE-INDEX.md`; הוא לא הושלם בתמונה חלופית או מומצאת.
- נתיב ללא צילום מסומן `missing` או `pending`; לא נוצר placeholder.
- צילום full-page אינו הוכחת click journey.
- readability נבדקת בפתיחת הקובץ, במידות ובדגימה חזותית; אינה מחליפה בדיקת דפדפן אינטראקטיבית.

## Links

קישורי מסמכי הניתוח העליונים נבדקים כקישורים יחסיים. קבצי raw והעתקים היסטוריים נשמרים byte-for-byte ולכן קישורים היסטוריים או absolute paths בתוכם אינם נכתבים מחדש; הם עשויים להצביע למבנה המקורי.

## Hashes

`MANIFEST.json` כולל SHA־256 לכל payload file מלבד עצמו. `SHA256SUMS.txt` כולל גם את `MANIFEST.json`. קובץ ה־checksum עצמו מעוגן ב־Git commit, כדי להימנע מלולאת self-hash בלתי אפשרית.

## Secrets

הסריקה מוגבלת לתיקיית הארכיון ומדווחת רק path/category. קובץ עם secret חשוד אינו נערך בתוך raw; הוא מוחרג בשלמותו ונרשם כאן. עצם היעדר התאמה אינו ביקורת אבטחה מלאה.

קובץ אחד הוחרג באופן שמרני בשל התאמה לכלל `credential_assignment`, אף שהבדיקה המבנית סיווגה אותה כ־placeholder ולא כסוד חי:

`raw/strategy-hub/handoff/codex/2026-06-23-source-context/reports/docs__2026-06-19-dimri-yama-go-live-checklist.md`

לא נשמר ולא הודפס הערך שהתאים. יתר הסריקה לא מצאה private key, token מוכר, JWT, cookie/session assignment או קובץ credential מובהק.

## זכויות

הייצוא אינו מעניק זכויות חדשות. כל asset בלי הוכחת בעלות/רישיון נשאר `rights_unknown`; יש להשיג אישור לפני שימוש מסחרי.
