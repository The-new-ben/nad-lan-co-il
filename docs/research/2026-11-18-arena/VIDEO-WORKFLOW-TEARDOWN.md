# פירוק מסלול שיחות הווידאו: Zoom ושאר המוצרים, מול השיחה שלנו בפורום

תאריך: 18.11.2026. מחקר מדפי עזרה, הודעות שחרור ובלוגים רשמיים בלבד. לא נכנסנו לשום חשבון, לא פתרנו שום בדיקת רובוט ולא בדקנו מוצר ביד.

**מה כבר קיים ולא חוזר כאן.** הקובץ `docs/research/2026-11-12-pro-forum/MEETING-WHITEBOARD-TEARDOWN.md` (12.11.2026) פירק 203 פרטים של לוח, סימון, מדידה וסמנים. כאן ההרחבה: המסלול של השיחה עצמה, מי נכנס ואיך, שליטת מארח, משחקיות, ומה עושים אחרי. כשפרט כבר מופיע שם, כתוב "ראו שורה N בפירוק של 12.11".

**קיצורים לקבצים שלנו (עמודת "אצלנו").** כל הנתיבים יחסית ל־`plugins/nadlan-config/`.
- **call.js** = `assets/proforum/call.js` (כפתור "שיחת וידאו", דף הכניסה, מסך השיחה, הזמנות, הודעה בפורום, מתגים אישיים).
- **board.js** = `assets/proforum/board.js` (הלוח המשותף בתוך השיחה).
- **php** = `inc/pro-forum-call.php` (מי רשאי להתקשר למי, חדרים, מכסות, מייל הזמנה, מפתח LiveKit).
- הקוד נקרא ב־18.11.2026. "יש" אומר שהקוד קיים, לא שנבדק בטלפון אמיתי.

**עמודת המקור.** כתובת = הדף שממנו נלקח הפרט, נאסף ב־18.11.2026. רוב הדפים נקראו דרך סיכום של מנוע החיפוש על הדף הרשמי. דפים שנפתחו במלואם מסומנים "(נקרא במלואו)". "צד שלישי" = דף של אוניברסיטה או אתר אחר, לא של היצרן. "לא אומת" = לא נמצא מקור.

---

## 1. המסלול אצל כל אחד

### Zoom, שיחה מיידית (מארח עם חשבון)
1. לוחצים New Meeting. ברירת המחדל: מספר חדר אקראי. אפשר לבחור במקום זה את החדר הקבוע (PMI) מהחץ שליד הכפתור.
2. החלון נפתח. לפי הגדרה, הקישור מועתק לבד ללוח ההעתקה ("Automatically copy invite link").
3. מזמינים מתוך Participants > Invite: אנשי קשר של Zoom (מקבלים חלון על המסך), מייל (פותח את תוכנת המייל עם הפרטים), Call Out או SMS (Zoom מחייג למספר ומצרף אותו בשמע בלבד), או Copy invite link.
4. בטלפון: אותו דבר מכפתור ההוספה ברשימת המשתתפים: מייל, הודעה, אנשי קשר, העתקת קישור.
5. בזמן השיחה: השתקה, וידאו, צ'אט, שיתוף מסך, תגובות, יד מורמת, לוח, הערות אישיות, כתוביות, סיכום AI.
6. סיום: Leave למשתתף. רק המארח מסיים לכולם. אחר כך, אם הוגדר, סקר אגודל למעלה או למטה.

### Zoom, אורח בלי חשבון
1. מקבל קישור (במייל, בהודעה, ביומן). אם הסיסמה מוטמעת בקישור, לחיצה אחת מספיקה.
2. אם אין אפליקציה: Join from your browser, או ב־Zoom Web App לוחצים Join a meeting ומקלידים מספר וסיסמה.
3. כותב שם.
4. אם יש חדר המתנה: מחכה עד שהמארח או המארח המשותף לוחץ Admit. אפשר להגדיר שרק אורחים לא מחוברים ימתינו.
5. אם המארח נעל את הפגישה, אף אחד לא נכנס, גם עם קישור וסיסמה.
6. המארח יכול לחסום כניסה מהדפדפן, ויכול לדרוש שכולם יהיו מחוברים לחשבון.

### Zoom, פגישה מתוזמנת
1. Schedule: נושא, שעה, סיסמה, חדר המתנה, הצפנה מקצה לקצה.
2. היומן (גוגל או אאוטלוק) שולח הזמנה. אם הצ'אט לפני ואחרי הפגישה פעיל, נפתחת קבוצת צ'אט לכל המוזמנים, וכל מה שנכתב בשיחה נשאר בה אחר כך.
3. אפשר גם לתזמן מתוך ערוץ צ'אט, ואז כל חברי הערוץ מוזמנים.
4. Zoom Scheduler: דף הזמנת תורים ציבורי שאפשר לשלב באתר.

### Google Meet
1. מתחילים פגישה חדשה מהאפליקציה, מהיומן או מ־Gmail. מקבלים קישור.
2. ההגדרה של המארח: Open (כל מי שיש לו קישור נכנס), Trusted (אנשי הארגון והמוזמנים נכנסים, אחרים מבקשים), Restricted (רק מוזמנים, השאר מבקשים).
3. מי שלא רשאי לוחץ "Ask to join" (דפיקה). רק המארח רואה את הבקשות. אפשר לאשר או לדחות אחד אחד, או את כולם. אפשר לבטל את האפשרות לבקש, ואז בקשות נדחות לבד.
4. בזמן השיחה: יד מורמת, תגובות, כתוביות, רקעים, סקרים, שאלות ותשובות, חדרי עבודה (במנויים מסוימים).
5. מעבר מכשיר: פותחים את Meet במחשב, בוחרים בפגישה ולוחצים "Switch here". המכשיר הקודם מתנתק, או "Join here too" לשניהם.
6. בהליכה: Meet מזהה תנועה ומציע On-the-Go: מצלמה כבויה, בלי וידאו, כפתורים גדולים, פחות נתונים.

### Microsoft Teams
1. Meet now מהיומן, מצ'אט קבוצתי, או הקלדת /meetnow.
2. Copy meeting link או Share invite במייל.
3. מי שלא עוקף את הלובי מחכה בלובי. ברירת המחדל: אנשי הארגון ואורחים נכנסים, אנונימיים מחכים.
4. רק מארגנים ומציגים מכניסים מהלובי (ברירת מחדל).
5. בשיחה: יד מורמת עם סדר, תגובות לכמה שניות, Whiteboard.
6. סיום לכולם: החץ שליד Leave > End meeting. סיכום AI רק אם הוא הופעל לפני הסוף.

### WhatsApp
1. בשיחה רגילה: לוחצים על אייקון השיחה בצ'אט. עד 32 משתתפים פעילים.
2. קישור שיחה: לשונית Calls > "+" > יצירת קישור. אפשר להפעיל "Require approval to join" (חדר המתנה).
3. שולחים את הקישור לכל אחד, גם בלי וואטסאפ.
4. אורח בלי חשבון (חדש, 14.10.2026): פותח את הקישור בדפדפן במחשב, כותב שם, מחכה שהמארח יכניס. אורח תמיד צריך אישור.
5. אורח יכול: שמע, וידאו, שיתוף מסך, תגובות (אגודל, לב), יד מורמת. לא יכול: לראות מספרי טלפון, לכתוב הודעות, להוסיף אנשים.
6. המארח יכול להוציא אורח בכל רגע. אין הגבלת זמן.
7. קישור שלא היה בשימוש 30 יום מפסיק לעבוד.
8. בקבוצה: "צ'אט קולי" שנכנסים אליו בלי צלצול לכולם. נגמר לבד אחרי 60 דקות בלי אף אחד.

### Facebook Messenger ו־Groups
1. Messenger Rooms (חדרים בקישור) הופסקו בסוף 2023, לפי עזרת Meta.
2. היום: שיחה קולית או וידאו מתוך צ'אט, כפתור בפינה העליונה.
3. Community Chats בקבוצות פייסבוק (כולל ערוצי שמע) הופסקו ב־5.10.2025 לפי סיכום החיפוש. ההפניה היא ל־Messenger Communities ול־WhatsApp Communities. מקור ישיר לסגירה לא אומת.

### Discord
1. אין צלצול. נכנסים לערוץ קולי בלחיצה, וכל חברי השרת רואים מי בפנים ויכולים "לקפוץ".
2. בערוץ: מצלמה, Go Live (שידור מסך עד 50 צופים), פעילויות (משחקים, צפייה משותפת), Soundboard.
3. ערוץ במה (Stage): נכנסים בשקט כקהל עם מיקרופון כבוי. דוברים מורשים מדברים.
4. אפשר לכתוב סטטוס לערוץ ("מה עושים כאן עכשיו").
5. שיחה פרטית קבוצתית כן מצלצלת.

### X Spaces
1. המארח פותח Space (שמע). אפשר להפעיל הקלטה כבר בפתיחה.
2. מאזינים לוחצים Request כדי לדבר. המארח או שני מארחים משותפים מאשרים.
3. עד 13 דוברים כולל המארחים (בדף אחר כתוב 11 ועוד 2).
4. בסוף: מספר המשתתפים וקישור לשיתוף ההקלטה בפוסט.

### Telegram
1. בקבוצה או ערוץ: מתחילים "Video Chat". מאזינים נכנסים מושתקים.
2. מאזין מרים יד כדי לבקש לדבר.
3. שיתוף מסך (במחשב גם חלון של תוכנה אחת), סינון רעשים שאפשר לכבות.
4. שידור חי: צופים מרימים יד ומצטרפים לשידור אם המארח מרשה.

### FaceTime בקישור
1. המארח יוצר קישור ב־FaceTime ושולח.
2. מי שבאנדרואיד או בווינדוס פותח בדפדפן (Chrome או Edge מומלצים), כותב שם, לוחץ Join.
3. מחכה. המארח לוחץ "Approve Join Request".
4. מהדפדפן אין SharePlay ואין שיתוף מסך.

### Whereby
1. לכל חדר כתובת קבועה שלא משתנה.
2. למארח קישור נפרד (host link) עם הרשאות: נעילה, הכנסה, הוצאה, השתקה, הבלטה, מחיקת הודעות וקבצים.
3. חדר נעול: האורח רואה מסך "דפיקה". המארח מכניס, משאיר להמתין עם הודעה, או דוחה.
4. הרשאות המארח פגות שעה אחרי זמן הסיום של החדר.

### Gather, Butter, Around (מפגש עם חום)
1. Gather: מסתובבים במשרד מצויר. "Wave" כדי למשוך תשומת לב, הוא ניגש. מקשים 1 עד 7 לתגובות, f לקונפטי, z לריקוד, ותשואות כשקבוצה עושה את זה יחד.
2. Butter: בונים סדר יום בבלוקים עם זמן. הבלוק מתמלא ירוק והופך אדום כשנגמר הזמן. סקרים, טיימר, מוזיקה, GIF בצ'אט, תגובות עם צליל.
3. Around: ראשים צפים קטנים על המסך. נקנה על ידי Miro ב־2022, והתכונות עברו לשיחות בתוך Miro (צד שלישי).

### Miro, FigJam, Excalidraw (לוח)
1. Miro: טיימר לכולם עם נגן מוזיקה, הצבעה, תגובות, "Bring to me" שמושך את כולם למסך שלך, Talktrack (סרטון מוקלט על הלוח).
2. FigJam: טיימר עד 99:59 עם מוזיקה אחת לכולם וכל אחד מנמיך לעצמו, חותמות, Emotes, High five, צ'אט ליד הסמן. גם מי שרק צופה יכול להשתמש בהם.
3. Excalidraw: קישור שיתוף בלי חשבון, מוצפן מקצה לקצה, והשרת רק מעביר הודעות.

### אצלנו היום (מהקוד)
1. חבר פורום פותח דיון. מי שענה ומי שפתח רואים כפתור "שיחת וידאו" בשורת הכותב, אם הצד השני הפעיל את המתג "אפשר לפנות אליי בשיחת וידאו" (ברירת מחדל כבוי). php, call.js.
2. מאז 18.11 אפשר להתקשר גם מכרטיס בעל מקצוע. php.
3. אורח שלוחץ: "כדי להצטרף לשיחה צריך להיכנס לפורום". שם, מייל וקוד. אחרי הכניסה השיחה נפתחת לבד. call.js.
4. דף כניסה: מצלמה ומיקרופון כבויים, תצוגה מקדימה וקו עוצמה רק כשמפעילים, "השיחה לא מוקלטת". call.js.
5. הצד השני מקבל הודעה בתוך הפורום (בדיקה כל 25 שניות, רק כשהוא על דף בפורום) עם "כניסה לשיחה" או "לא עכשיו", ומייל רק אם הפעיל את המתג. call.js, php.
6. בשיחה: המסך מלא, הבקשה מוצמדת למעלה עם משך השיחה, מיקרופון, מצלמה, החלפת מצלמה, "עוד" (קול בלבד, הזמנת עוד מישהו), סיום. עד 4 אנשים. call.js, php.
7. לוח משותף: תמונה או תוכנית מהמצלמה או מהמכשיר, עט, מרקר, חץ, צורה, הערה ממוספרת, מידה עם כיול, לייזר, מחק לסימונים שלי, "עקבו אחריי", שמירה כתמונה. board.js.
8. סיום: חוזרים לדיון. כלום לא נשמר באתר. אין סיכום, אין סיום לכולם. call.js.

---

## 2. הטבלה הגדולה: פרט אחר פרט

| # | פרט | מה קורה בדיוק | אצל מי | אצלנו היום | מקור |
|---|---|---|---|---|---|
| | **כניסה, קישור והזמנה** | | | | |
| 1 | פגישה מיידית | לחיצה אחת פותחת חדר עם מספר אקראי. | Zoom, Meet, Teams (Meet now) | חלקי: לחיצה על "שיחת וידאו" פותחת חדר, רק מול אדם מסוים מתוך דיון או כרטיס. call.js, php | https://support.microsoft.com/en-us/teams/meetings/start-an-instant-meeting-in-microsoft-teams |
| 2 | חדר אישי קבוע (PMI) | מספר של 10 עד 11 ספרות שהוא החדר הקבוע של המשתמש. | Zoom | אין | https://it.umn.edu/services-technologies/how-tos/zoom-set-custom-link-your-personal (צד שלישי) |
| 3 | קישור אישי בשם | כינוי של 5 עד 40 תווים, ייחודי בכל Zoom, שמוביל לחדר הקבוע. | Zoom | אין | https://itsupport.ou.edu/TDClient/30/Unified/KB/PrintArticle?ID=3273 (צד שלישי) |
| 4 | חדר בכתובת קבועה | כתובת החדר לא משתנה בין פגישות. | Whereby | אין: חדר חדש לכל שיחה, נגמר עם השיחה. php | https://whereby.com/blog/how-to-start-your-first-whereby-meeting/ |
| 5 | קישור מארח נפרד | למארח קישור אחר שנותן לו הרשאות ניהול. | Whereby | אין | https://docs.whereby.com/whereby-product-features/user-roles-and-privileges |
| 6 | תזמון פגישה | נושא, שעה, סיסמה, חדר המתנה, נשלח ביומן. | Zoom, Meet, Teams | אין | https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0060700 |
| 7 | תזמון מתוך ערוץ צ'אט | כל חברי הערוץ מוזמנים אוטומטית. | Zoom | אין | https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0058336 |
| 8 | דף הזמנת תורים | דף ציבורי שבו בוחרים שעה ומקבלים קישור. | Zoom Scheduler | אין | https://www.zoom.com/en/products/appointment-scheduler/ |
| 9 | דף תורים משולב באתר | מטמיעים את דף ההזמנה בתוך אתר. | Zoom Scheduler | אין | https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0083594 |
| 10 | אירוע עם אישור הגעה | אירוע בקבוצה או בצ'אט אחד על אחד, "אולי", פלוס אחד, תזכורת לפני. | WhatsApp | אין | https://blog.whatsapp.com/new-feature-roundup-updates-to-group-chats-events-calls-channels-and-more (נקרא במלואו) |
| 11 | שיחה מתוך היומן | תוסף ליומן גוגל ואאוטלוק מוסיף קישור שיחה להזמנה. מוזמנים נכנסים עם או בלי חשבון. הוכרז כ"בהמשך השנה". | WhatsApp | אין | https://blog.whatsapp.com/now-you-can-invite-anyone-to-a-whatsapp-call-no-account-needed-no-cost-no-time-limit (נקרא במלואו) |
| 12 | העתקת קישור הזמנה | Copy invite link או Copy invitation מעתיקים קישור או טקסט מלא. | Zoom, Teams | אין: הקישור עם `#call=` נשלח רק במייל. php | https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0063688 |
| 13 | העתקה אוטומטית בפתיחה | הקישור נכנס ללוח ההעתקה ברגע שהפגישה נפתחת. | Zoom | אין | https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0060612 (נקרא במלואו) |
| 14 | הזמנה במייל מתוך השיחה | פותח את תוכנת המייל עם פרטי הפגישה. | Zoom | חלקי: "הזמינו עוד מישהו" שולח מייל רק אם המוזמן הפעיל מייל. php | https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0063688 |
| 15 | הזמנת איש קשר שמופיעה על המסך שלו | המוזמן מקבל חלון מיד באפליקציה. | Zoom | חלקי: הודעה בפורום, נבדקת כל 25 שניות ורק כשהוא על דף בפורום. call.js | https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0063688 |
| 16 | חיוג החוצה או SMS | Zoom מחייג למספר ומצרף אותו בשמע בלבד, או שולח הודעה. | Zoom | אין | https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0063688 |
| 17 | הוספה לשיחה פעילה של שניים | מוסיפים מישהו לשיחה אחד על אחד מתוך הצ'אט. | WhatsApp | יש: "הזמינו עוד מישהו", עד 4 בחדר, 20 הזמנות ליום. call.js, php | https://blog.whatsapp.com/new-feature-roundup-updates-to-group-chats-events-calls-channels-and-more (נקרא במלואו) |
| 18 | הזמנה בקישור לכל אחד, גם בלי האפליקציה | הקישור עובד לכל מי שמקבל אותו. | WhatsApp, Zoom, Meet, FaceTime | אין: רק חבר פורום שעומד בכללים. php | https://blog.whatsapp.com/now-you-can-invite-anyone-to-a-whatsapp-call-no-account-needed-no-cost-no-time-limit (נקרא במלואו) |
| 19 | כניסה מהדפדפן בלי התקנה | Zoom Web App: Join a meeting, מספר וסיסמה. | Zoom, Meet, FaceTime (דפדפן), WhatsApp (מחשב) | יש: הכול בדפדפן, אין אפליקציה. call.js | https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0059744 |
| 20 | אורח רק כותב שם | אורח בלי חשבון כותב שם ומחכה לאישור. | WhatsApp, FaceTime | אין: אורח חייב להיכנס לפורום (שם, מייל, קוד). call.js | https://support.apple.com/en-us/109364 |
| 21 | השיחה נפתחת לבד אחרי ההרשמה | אורח שלחץ, נרשם, והשיחה ממשיכה בלי לחיצה נוספת. | רק אצלנו | יש: savePending ו־takePending. call.js | אין מקור חיצוני |
| 22 | סיסמה לפגישה | קוד שצריך להקליד או שמוטמע בקישור. | Zoom | אין: במקום סיסמה, בדיקת חברות ומזהה חדר אקראי. php | https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0063160 |
| 23 | סיסמה מוצפנת בתוך הקישור | לחיצה אחת בלי להקליד קוד. מנהל יכול לבטל. | Zoom | אין | https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0065979 |
| 24 | חדר המתנה | המשתתף מחכה עד שהמארח מכניס. | Zoom, WhatsApp, FaceTime | אין | https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0059359 |
| 25 | המתנה רק לאורחים | רק מי שלא מחובר או לא מהחשבון ממתין. | Zoom | אין | https://it.stonybrook.edu/help/kb/enabling-waiting-room-in-zoom-so-meeting-participants-can-only-join-once-admitted-by-a-host (צד שלישי) |
| 26 | הכנסת כולם בלחיצה | Admit All. | Zoom, Meet | אין | https://teamdynamix.umich.edu/TDClient/30/Portal/KB/Article/3004/Zoom-Enable-and-Configure-Waiting-Rooms (צד שלישי) |
| 27 | חדר המתנה מעוצב | כותרת, לוגו, תמונה או סרטון בחדר ההמתנה. | Zoom | אין | https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0059359 |
| 28 | צ'אט עם הממתין | המארח כותב לאדם שבחדר ההמתנה. | Zoom Contact Center | אין | https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0063781 |
| 29 | דפיקה (Ask to join) | מי שלא הוזמן מבקש להיכנס, רק המארח רואה. | Meet, Whereby | אין | https://support.google.com/meet/answer/16229038?hl=en&co=GENIE.Platform%3DDesktop |
| 30 | ביטול האפשרות לדפוק | בקשות ממי שלא הוזמן נדחות לבד. | Meet | יש בפועל: מי שלא עומד בכללים מקבל הודעה ולא נכנס. php | https://support.google.com/a/users/answer/11989526?hl=en |
| 31 | רמות גישה פתוח, מהימן, מוגבל | הגדרה אחת קובעת מי נכנס ישר ומי מבקש. | Meet | חלקי: כלל אחד קבוע, רק מי שכתב בדיון או בעל הכרטיס. php | https://support.google.com/meet/answer/16229038?hl=en&co=GENIE.Platform%3DDesktop |
| 32 | השארה בהמתנה עם הודעה | המארח עונה לדופק "רק רגע" בלי להכניס. | Whereby | אין | https://docs.whereby.com/whereby-product-features/waiting-rooms |
| 33 | לובי עם כללי עקיפה | מי עוקף את הלובי: כולם, הארגון, המוזמנים, רק מארגנים. | Teams | אין | https://learn.microsoft.com/en-us/microsoftteams/who-can-bypass-meeting-lobby |
| 34 | מי רשאי להכניס מהלובי | ברירת מחדל: מארגנים ומציגים. | Teams | אין | https://learn.microsoft.com/en-us/microsoftteams/who-can-bypass-meeting-lobby |
| 35 | נעילת פגישה | אחרי נעילה אף אחד לא נכנס, גם עם קישור. | Zoom, Whereby | חלקי: חדר מוגבל ל־4, ורק מי שהוזמן נכנס. php | https://www.bu.edu/tech/services/cccs/collaboration/online/zoom/getting-started/meeting-security/in-meeting-security (צד שלישי) |
| 36 | קישור פג אחרי 30 יום בלי שימוש | קישור שלא היה בשימוש חודש לא עובד. | WhatsApp | חלקי: "השיחה הזו כבר הסתיימה", וההודעה בפורום חיה 15 דקות. call.js, php | https://faq.whatsapp.com/335663222921532 |
| 37 | נכנסים עם מצלמה כבויה | הגדרה אישית "Keep my camera off". | Zoom | יש: תמיד כבויה בכניסה. call.js | https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0060612 (נקרא במלואו) |
| 38 | נכנסים מושתקים | "Keep my microphone muted". | Zoom | יש: תמיד כבוי בכניסה. call.js | https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0060612 (נקרא במלואו) |
| 39 | תצוגה מקדימה לפני כניסה | רואים את עצמכם לפני שנכנסים. | Zoom | יש: רק אחרי שמפעילים מצלמה. call.js | https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0060612 (נקרא במלואו) |
| 40 | קו עוצמת מיקרופון לפני כניסה | "דברו, והקו זז". | אצלנו. אצל אחרים לא אומת | יש. call.js | לא אומת אצל אחרים |
| 41 | שאלה לפני יציאה | "בטוחים שרוצים לצאת?". | Zoom | אין | https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0060612 (נקרא במלואו) |
| 42 | חיבור שמע אוטומטי | מצטרפים עם שמע בלי לחיצה נוספת. | Zoom (טלפון) | יש בפועל: השמע מתחבר, ויש "הקישו כדי לשמוע" כשהדפדפן חוסם. call.js | https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0060612 (נקרא במלואו) |
| 43 | מעבר מכשיר בלי לנתק | "Switch here" במחשב לוקח את השיחה מהטלפון. | Meet | אין | https://support.google.com/meet/answer/14762432?hl=en |
| 44 | גם כאן וגם שם | "Join here too" משאיר את השיחה בשני המכשירים. | Meet | אין | https://support.google.com/meet/answer/14762432?hl=en |
| 45 | מכשיר שני ללוח בלבד | מצטרפים ממכשיר נוסף עם מיקרופון ווידאו כבויים, לשיתוף ולצ'אט. | Meet (Companion) | אין | https://support.google.com/meet/answer/11295507?hl=en |
| 46 | צ'אט לפני ואחרי הפגישה | קבוצת צ'אט לכל המוזמנים, ההודעות מהשיחה נשארות בה. | Zoom | חלקי: הדיון בפורום הוא המקום לפני ואחרי, אבל אין צ'אט בתוך השיחה. call.js | https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0058605 |
| 47 | לשונית שיחות עם היסטוריה | מקום אחד לשיחות, קישורים והיסטוריה. | WhatsApp | אין | https://blog.whatsapp.com/new-feature-roundup-updates-to-group-chats-events-calls-channels-and-more (נקרא במלואו) |
| 48 | הודעה על שיחה שלא נענתה | מי שלא ענה מקבל הודעה בצ'אט. | WhatsApp | אין | https://blog.whatsapp.com/new-feature-roundup-missed-call-messages-new-status-stickers-and-more |
| 49 | כפתור שיחה מכרטיס האדם | מתקשרים לבעל מקצוע מהכרטיס שלו, בלי דיון. | אצלנו (18.11) | יש. php (nlfc_card_member) | אין מקור חיצוני |
| 50 | מתג "אפשר לפנות אליי" | כל חבר מחליט אם אפשר להתקשר אליו, כבוי כברירת מחדל. | אצלנו | יש. call.js, php | אין מקור חיצוני |
| 51 | הפסקת מיילים בלחיצה אחת | קישור במייל מכבה את מיילי ההזמנה. | אצלנו | יש. php | אין מקור חיצוני |
| 52 | תקרה ליום לאותו אדם | לא יותר מ־3 שיחות ביום מאותו אדם לאותו אדם. | אצלנו | יש. php (nlfc_pair_cap) | אין מקור חיצוני |
| | **שליטת מארח** | | | | |
| 53 | מארח משותף | מארח מוסיף אנשים עם רוב הרשאות הניהול. | Zoom, Meet | אין | https://support.google.com/meet/answer/10885841 |
| 54 | מארח חלופי | מי שיכול להתחיל את הפגישה אם המארח לא הגיע. | Zoom | אין | https://support.zoom.us/hc/en-us/articles/360040324512-Roles-in-a-meeting (לא נפתח, הפניה בלבד) |
| 55 | השתקת כולם | Mute All משתיק את כל מי שבפנים. | Zoom | אין | https://www.etsu.edu/helpdesk/documents/zoom-manage-participants.pdf (צד שלישי) |
| 56 | בקשה מכולם לבטל השתקה | חלון אצל כל מושתק, והוא בוחר. | Zoom | אין | https://www.etsu.edu/helpdesk/documents/zoom-manage-participants.pdf (צד שלישי) |
| 57 | השתקת אדם אחד | המארח משתיק משתתף מיד. | Zoom, Whereby, X Spaces | אין | https://docs.whereby.com/whereby-product-features/user-roles-and-privileges |
| 58 | בקשה מאדם לבטל השתקה | חלון בקשה, לא כפייה. | Zoom | אין | https://www.etsu.edu/helpdesk/documents/zoom-manage-participants.pdf (צד שלישי) |
| 59 | כיבוי וידאו של משתתף | המארח עוצר מצלמה של מישהו. | Zoom | אין | https://itshelp.aurora.edu/hc/en-us/articles/34556939362327-Managing-Zoom-Participants (צד שלישי) |
| 60 | שינוי שם משתתף | שם חדש לפגישה הזו בלבד. | Zoom | אין: השם בא מפרופיל הפורום. call.js | https://itshelp.aurora.edu/hc/en-us/articles/34556939362327-Managing-Zoom-Participants (צד שלישי) |
| 61 | שינוי שם עצמי רק באישור | המארח קובע אם משתתפים משנים את שמם. | Zoom | לא רלוונטי: שם מהפורום, עם המקצוע לידו. call.js | https://itshelp.aurora.edu/hc/en-us/articles/34556939362327-Managing-Zoom-Participants (צד שלישי) |
| 62 | הוצאת משתתף | Remove ברשימת המשתתפים. | Zoom, Whereby, WhatsApp | אין | https://blog.whatsapp.com/now-you-can-invite-anyone-to-a-whatsapp-call-no-account-needed-no-cost-no-time-limit (נקרא במלואו) |
| 63 | מי שהוצא לא חוזר | אלא אם הופעלה הגדרה שמאפשרת. | Zoom | אין | https://ccri.teamdynamix.com/TDClient/2073/Portal/KB/Article/136342/Zoom-Host-Controls (צד שלישי) |
| 64 | החזרה לחדר ההמתנה | הוצאה רכה למי שאינו מסוכן. | Zoom | אין | https://www.dpo.uab.edu/elearning/academic-technologies/zoom/manage-participants (צד שלישי) |
| 65 | הקפאת כל הפעילות | כיבוי וידאו, שמע, שיתוף ואפליקציות לכולם, ונעילה. | Zoom | אין | https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0061231 |
| 66 | דיווח על משתתף | דיווח לצוות הבטיחות, המדווח מוצא מהשיחה, אישור תוך 7 ימים. | Zoom | אין בתוך השיחה | https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0067474 |
| 67 | מנהל מכבה את הדיווח | הגדרה ברמת החשבון. | Zoom | אין | https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0064664 |
| 68 | סיום לכולם | רק המארח (או מציג ב־Teams) מסיים לכל המשתתפים. | Zoom, Teams | אין: יציאה של אחד משאירה את האחרים. call.js | https://support.microsoft.com/en-us/teams/meetings/end-a-meeting-for-everyone-in-attendance-in-microsoft-teams |
| 69 | הבלטה לכולם (Spotlight) | אדם אחד הופך לדובר הראשי אצל כולם. צריך 3 עם וידאו. | Zoom, Whereby | אין | https://community.zoom.com/t5/Meetings/Spotlight-and-pin-Participants-don-t-see-what-host-does-when/m-p/156694 (פורום של Zoom) |
| 70 | הצמדת וידאו אצלי | משנה רק את התצוגה שלי, עד 9 וידאו. | Zoom | אין | https://www.ucl.ac.uk/news/2021/feb/todays-zoom-tip-25-february-2021 (צד שלישי) |
| 71 | תצוגת גלריה | רשת של עד 25 או 49 במסך. | Zoom | חלקי: עד 4 אנשים, פריסה ל־3 ו־4 לא נבדקה בטלפון. call.js | https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0060612 (נקרא במלואו) |
| 72 | תצוגת דובר | מי שמדבר גדול. | Zoom | חלקי: סימון "מדבר/ת". call.js, board.js | https://gbc.libanswers.com/oirt-edtech/faq/297142 (צד שלישי) |
| 73 | הסתרת משתתפים בלי וידאו | "Show non-video participants" כבוי. | Zoom | אין | https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0060612 (נקרא במלואו) |
| 74 | שעון משך השיחה | "Show meeting timer". | Zoom | יש: משך השיחה בפס העליון. call.js | https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0060612 (נקרא במלואו) |
| 75 | שעון זמן שנותר | השעון סופר אחורה לסוף הפגישה המתוזמנת. | Zoom | אין | https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0060612 (נקרא במלואו) |
| 76 | מצב מיקוד | משתתפים רואים רק את המארח ואת עצמם, המארח רואה את כולם. | Zoom | אין | https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0058349 |
| 77 | תצוגה בחדר משותף מצויר | עד 25 משתתפים על רקע אחד. | Zoom (Immersive), Teams (Together mode, לא אומת) | אין | https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0058351 |
| 78 | ספירת סמלי משוב אצל המארח | המארח רואה כמה לחצו "כן" או "לאט" ומנקה. | Zoom | אין | https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0063323 |
| 79 | הורדת יד בידי המארח | המארח מוריד יד של משתתף. | Zoom, Meet ("Lower all") | אין | https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0068290 |
| 80 | הפיכת מאזין לדובר | מארח מאשר בקשה לדבר או מזמין לדבר. | X Spaces, Telegram | אין | https://help.x.com/en/using-x/spaces-hosting |
| 81 | מחיקת הודעות וקבצים של אחרים | המארח מוחק מה שמישהו שיתף. | Whereby | אין | https://docs.whereby.com/whereby-product-features/user-roles-and-privileges |
| 82 | הרשאות מארח פגות | שעה אחרי סיום הזמן של החדר. | Whereby | לא רלוונטי | https://docs.whereby.com/whereby-product-features/user-roles-and-privileges |
| 83 | מתגים של בעל האתר | מנהל מדליק ומכבה כל יכולת. | Zoom, Teams | חלקי: מתג אחד לכל השיחות ומכסה יומית. php | https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0058301 |
| 84 | מכסות נגד ניצול | הגבלה של חדרים ליום לאדם, לכתובת ולכל האתר. | אצלנו | יש: 8, 8, 40. php | אין מקור חיצוני |
| | **שמע, וידאו וטלפון** | | | | |
| 85 | השתקה עם קיצור מקלדת | Alt+A או Command+Shift+A. | Zoom | חלקי: כפתור בלבד. call.js | https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0062674 (נקרא במלואו) |
| 86 | החלפת מצלמה קדמית ואחורית | בטלפון. | WhatsApp, Zoom (לא אומת בעמוד) | יש: "החלפה", רק כשהמצלמה דולקת. call.js | לא אומת בעמוד רשמי |
| 87 | תמונה עצמית במראה רק בקדמית | הצילום האחורי לא הפוך. | אצלנו | יש. call.js | אין מקור חיצוני |
| 88 | קול בלבד לחיסכון בנתונים | הווידאו של האחרים נעצר, השמע ממשיך. | Meet (On-the-Go), Telegram | יש: "קול בלבד, חוסך נתונים". call.js | https://support.google.com/meet/answer/14000592?hl=en%3D |
| 89 | הצעה אוטומטית כשזזים | Meet מזהה הליכה ומציע מצב בדרכים. | Meet | אין | https://workspaceupdates.googleblog.com/2023/11/take-google-meet-on-go-with-ease.html |
| 90 | מצב נהיגה | החלקה ימינה: משתיק, מכבה וידאו, "הקישו כדי לדבר". | Zoom | אין | https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0060612 (נקרא במלואו) |
| 91 | תמונה בתוך תמונה | חלון צף קטן כשעוברים לאפליקציה או לשונית אחרת. | Meet (Chrome במחשב) | אין | https://support.google.com/meet/answer/13665919?hl=en-BS |
| 92 | חלון צף אוטומטי במעבר לשונית | נפתח לבד, עם הגדרה מתי. | Meet | אין | https://workspaceupdates.googleblog.com/2024/08/picture-in-picture-in-google-meet-will-open-when-switching-tabs.html |
| 93 | שיחה חיה במסך הנעילה | Live Activity באייפון בזמן שיחה קולית. | Discord (4.8.2026) | אין | https://discord.com/blog/discord-patch-notes-august-4-2026 |
| 94 | הגדלת וידאו בצביטה | צובטים על הווידאו כדי להגדיל. | WhatsApp (אייפון) | אין בווידאו. בלוח יש צביטה. board.js | https://blog.whatsapp.com/new-feature-roundup-updates-to-group-chats-events-calls-channels-and-more (נקרא במלואו) |
| 95 | שדרוג אוטומטי ל־HD | כשיש רוחב פס. | WhatsApp | לא נבדק | https://blog.whatsapp.com/new-feature-roundup-updates-to-group-chats-events-calls-channels-and-more (נקרא במלואו) |
| 96 | סינון רעשי רקע | מסיר הקלדה, דלת, רעש בנייה. | Meet, Zoom, Discord (Krisp), Telegram | לא נבדק בקוד שלנו | https://support.google.com/meet/answer/9919960?hl=en&co=GENIE.Platform%3DDesktop |
| 97 | צליל מקורי | מכבה את סינון הרעשים כדי לשמוע הכול. | Zoom | אין | https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0064198 |
| 98 | שיפור שמע וידאו בבינה מלאכותית | Studio sound ו־Studio lighting. | Meet | אין | https://support.google.com/meet/answer/14441737?hl=en |
| 99 | תיקון תאורה חלשה | אוטומטי או ידני. | Zoom | אין | https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0060352 |
| 100 | ריכוך פנים | Touch up my appearance עם מחוון. | Zoom | אין | https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0060352 |
| 101 | טשטוש רקע | Blur, נשמר כברירת מחדל. | Zoom, Meet | אין | https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0061066 |
| 102 | רקע וירטואלי | תמונה או סרטון במקום החדר. | Zoom, Meet | אין | https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0060387 |
| 103 | דמות תלת ממד במקום פנים | עוקבת אחרי תנועות הראש והבעות. | Zoom | אין | https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0058351 (הופיע בסיכום חיפוש משותף, דף נפרד על Avatars לא נפתח) |
| 104 | הודעה על מי נכנס ויצא | "Show name when participants join". | Zoom | יש: "הצטרף/ה" ו"יצא/ה". call.js | https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0060612 (נקרא במלואו) |
| 105 | הודעת "מתחברים שוב" | אחרי נפילה, חוזרים לאותו חדר עם אותה זהות. | אצלנו. Claude Meetings (ראו שורה 114 בפירוק של 12.11) | יש. call.js, php | https://support.claude.com/en/articles/18325154-use-claude-meetings |
| 106 | "הקישו כדי לשמוע" | כשהדפדפן חוסם שמע אוטומטי. | אצלנו | יש. call.js | אין מקור חיצוני |
| 107 | השארת האפליקציה ברקע | ממשיכים לקבל הזמנות כשהאפליקציה ממוזערת. | Zoom | אין: ההודעה מגיעה רק כשהדף פתוח. call.js | https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0065212 |
| 108 | כתוביות חיות | מילים על המסך, נדלק רק אצלי. | Meet, Zoom | אין | https://support.google.com/meet/answer/15077804?hl=en&co=GENIE.Platform%3DDesktop |
| 109 | כתוביות מתורגמות | כל אחד בוחר שפה. במנויים מסוימים. | Meet, Zoom | אין | https://support.google.com/meet/answer/10964115?hl=en&co=GENIE.Platform%3DAndroid |
| 110 | כתוביות תמיד דולקות | הגדרה אישית בטלפון. | Zoom | אין | https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0060612 (נקרא במלואו) |
| 111 | הצפנה מקצה לקצה | כשמופעלת: אין הקלטה בענן, אין צ'אט, אין סקרים, אין דפדפן. | Zoom | לא נבדק: התעבורה עוברת ב־LiveKit, לא נטען שיש הצפנה כזו | https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0075502 |
| 112 | הצפנה בצד הלקוח בלי דפיקה | בפגישה מוצפנת אי אפשר לבקש להיכנס. | Meet | לא רלוונטי | https://support.google.com/meet/answer/11605714?hl=en&co=GENIE.Platform%3DAndroid |
| | **תגובות ומשחקיות** | | | | |
| 113 | תגובת אימוג'י | עפה על המסך ונעלמת אחרי כ־10 שניות. | Zoom, Meet, Teams, WhatsApp | אין | https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0063323 |
| 114 | תגובות מונפשות צפות | אימוג'י שעולים ומרחפים. | Zoom (אייפון) | אין | https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0060612 (נקרא במלואו) |
| 115 | גוון עור לתגובות | בחירה אישית. | Zoom | אין | https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0060612 (נקרא במלואו) |
| 116 | סמלי משוב שנשארים | כן, לא, לאט יותר, מהר יותר, תיכף חוזר, לא כאן. | Zoom | אין | https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0063323 |
| 117 | הרמת יד | המארח מקבל התראה ויכול לבקש לבטל השתקה. | Zoom, Meet, Teams, WhatsApp, Telegram | אין | https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0068290 |
| 118 | סדר הידיים | רואים מי הרים ראשון. | Teams, Meet | אין | https://support.microsoft.com/en-us/teams/meetings/use-meeting-controls-in-microsoft-teams |
| 119 | הרמת יד בטלפון רגיל | *9 בחיוג. | Zoom | אין | https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0068290 |
| 120 | תגובה בתנועת יד מול המצלמה | מחזיקים תנועה 2 שניות. לב ממלא את המסך בלבבות, חגיגה בזיקוקים. | Zoom | אין | https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0067842 |
| 121 | מארח מכבה תגובות | לשיחה שלמה. | Meet, Teams | אין | https://support.google.com/meet/answer/13151720?hl=en&co=GENIE.Platform%3DDesktop |
| 122 | סקר משוב בסוף השיחה | אגודל למעלה מסיים. אגודל למטה שואל מה השתבש. | Zoom | אין | https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0066367 |
| 123 | סקר מותאם אחרי הפגישה | המארח בונה שאלון שנפתח כשהפגישה נגמרת. | Zoom | אין | https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0066844 |
| 124 | לוח צלילים | קטע שמע קצר שכל הערוץ שומע. מנהל קובע מי רשאי. | Discord | אין | https://support.discord.com/hc/en-us/articles/12612888127767-Discord-Soundboard-Guide-Using-Adding-and-Managing-Sounds |
| 125 | פעילויות בערוץ קולי | משחקים וצפייה משותפת מתוך השיחה. | Discord | אין | https://support.discord.com/hc/en-us/articles/7931156448919-Activity-Sharing-on-Discord-FAQ |
| 126 | סרגל תגובות במקשים | 1 עד 7: נפנוף, לב, קונפטי, אגודל, צחוק, מחיאות, 100. | Gather | אין | https://support.gather.town/hc/en-us/articles/15910325457172-Use-Emotes-and-Customize-the-Emote-Bar |
| 127 | קונפטי וריקוד | f זורק קונפטי, z רוקד. | Gather | אין | https://support.gather.town/articles/4269803312-applause-extension |
| 128 | תשואות קבוצתיות | כשכמה זורקים קונפטי יחד נשמעות מחיאות. | Gather | אין | https://support.gather.town/articles/4269803312-applause-extension |
| 129 | נפנוף למשיכת תשומת לב | מנפנפים, והאדם ניגש אם פנוי. | Gather | אין | https://support.gather.town/articles/3367182370-gather-for-engineering-teams |
| 130 | תגובות עם צליל | כל תגובה משמיעה אפקט קצר. | Butter | אין | https://www.butter.us/features/engagement |
| 131 | GIF בצ'אט עם שרשורים | שאלות ורעיונות בשרשורים, עם GIF. | Butter | אין | https://www.butter.us/features/engagement |
| 132 | סדר יום בבלוקים עם זמן | הבלוק מתמלא ירוק ונהיה אדום כשנגמר. | Butter | אין | https://help.butter.us/agenda |
| 133 | פלייליסט מוזיקה בשיחה | מוזיקה לכולם בזמן עבודה. | Butter, FigJam, Miro | אין | https://support.butter.us/en/articles/6990669-what-is-butter |
| 134 | טיימר לכולם עם מוזיקה | ספירה לאחור שמתחילה ונגמרת לכל הלוח. | Miro, FigJam | אין | https://help.miro.com/hc/en-us/articles/360017730933-Timer |
| 135 | טיימר אחד לקובץ, עד 99:59 | כל אחד מנמיך את המוזיקה לעצמו. | FigJam | אין | https://help.figma.com/hc/en-us/articles/4402269549591-Stay-on-track-with-the-timer-in-FigJam |
| 136 | גם צופה יכול לחגוג | מי שרק צופה שולח Emotes ו־High five. | FigJam | חלקי: אצלנו כולם מציירים ומשתמשים בלייזר, אין תפקיד צופה. board.js | https://help.figma.com/hc/en-us/articles/15300412458647-Explore-FigJam-files |
| 137 | High five | שני סמנים נפגשים. | FigJam | אין (ראו שורה 102 בפירוק של 12.11) | https://help.figma.com/hc/en-us/articles/4502073572247-FigJam-for-iPad |
| 138 | הצבעה על פתקים | מספר קולות לאדם, אפשר בעילום שם. | Zoom Whiteboard, Miro, FigJam | אין | https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0085121 |
| 139 | מצב פרטי בלוח | פתקים מוסתרים עד שהמנחה חושף. | Zoom Whiteboard, Miro | אין | https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0077861 |
| 140 | סרטון הדרכה מוקלט על הלוח | Talktrack, צופים מגיבים באימוג'י ברגע מסוים. | Miro | אין | https://help.miro.com/hc/en-us/articles/35405180333202-Talktrack |
| 141 | ראשים צפים | בועות וידאו קטנות מעל כל תוכנה. | Around (נסגר, עבר ל־Miro) | אין | https://alternativeto.net/news/2025/1/the-video-call-app-around-is-shutting-down-just-over-a-year-after-its-acquisition-by-miro (צד שלישי) |
| | **צ'אט, סקרים, שאלות וחדרים** | | | | |
| 142 | צ'אט בתוך השיחה | הודעות לכולם או לאחד. | Zoom, Meet, Teams | אין | https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0062674 (נקרא במלואו) |
| 143 | קבצים בצ'אט | כבוי כברירת מחדל, מנהל קובע סוגים וגודל. | Zoom | אין. תמונה עולה ללוח במקום. board.js | https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0058822 |
| 144 | צילום מסך או "חגיגה" בצ'אט | שולחים צילום מסך או תגובת חגיגה. | Zoom | אין | https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0064413 |
| 145 | אורח בלי הודעות | אורח לא כותב בצ'אט. | WhatsApp | לא רלוונטי | https://blog.whatsapp.com/now-you-can-invite-anyone-to-a-whatsapp-call-no-account-needed-no-cost-no-time-limit (נקרא במלואו) |
| 146 | סקר בשיחה | המארח שואל, דוח במייל עם שמות ותשובות. | Zoom, Meet | אין | https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0066150 |
| 147 | סקר מתקדם וחידון | התאמה, דירוג, תשובה פתוחה. | Zoom | אין | https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0066150 |
| 148 | שאלות ותשובות עם הצבעה | בעילום שם, אישור לפני פרסום, עד 500 שאלות. | Meet, Zoom | אין | https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0058425 |
| 149 | חדרי עבודה קטנים | מפצלים את השיחה לחדרים. | Zoom, Meet | אין | https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0061583 |
| 150 | חדרים לפי תשובת סקר | כל מי שענה אותו דבר באותו חדר. | Zoom | אין | https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0058236 |
| 151 | הערות אישיות עם תמלול | פתקים פרטיים שמתחברים לתמלול. | Zoom (My Notes) | אין | https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0083849 |
| 152 | מסמך משותף בתוך הפגישה | עורכים מסמך יחד בזמן השיחה. | Zoom Docs | אין | https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0075023 |
| 153 | רכיב חי בצ'אט | רשימה או טבלה שמתעדכנת אצל כולם. | Teams (Loop) | אין | https://support.microsoft.com/en-us/office/use-a-loop-component-in-a-chat-b1ed0278-4a5c-4756-aeb6-9f0fe387d722 |
| 154 | אורח אנונימי בלי רכיבים חיים | אנונימי לא רואה ולא עורך רכיבי Loop בלוח. | Teams | לא רלוונטי: אין אנונימיים אצלנו | https://support.microsoft.com/en-us/office/loop-components-in-whiteboard-c5f08f54-995e-473e-be6e-7f92555da347 |
| | **ערוצים קהילתיים** | | | | |
| 155 | ערוץ קולי שקופצים אליו | בלי צלצול, רואים מי בפנים. | Discord | אין | https://support.discord.com/hc/en-us/articles/360045138571-Beginner-s-Guide-to-Discord |
| 156 | סטטוס לערוץ | שורה "מה עושים כאן עכשיו" מתחת לשם הערוץ. | Discord | אין | https://support.discord.com/hc/en-us/articles/19583625604887-Voice-Channels-FAQs |
| 157 | כניסה שקטה בלי צליל | נכנסים בלי צליל כניסה. | Discord | אין | https://support.discord.com/hc/en-us/community/posts/22233303534871-Add-role-permission-that-restricts-the-newly-added-ability-to-join-voice-channels-without-entrance-sound (פורום) |
| 158 | במה עם קהל מושתק | עד 5 מצלמות על הבמה, קהל מקשיב. | Discord | אין | https://support.discord.com/hc/en-us/articles/1500005513722-Stage-Channels-FAQ |
| 159 | שידור מסך לחברי הערוץ | Go Live עד 50 צופים. | Discord | אין | https://support.discord.com/hc/en-us/articles/360040816151-Go-Live-and-Screen-Share |
| 160 | צ'אט קולי בקבוצה | לחיצה ארוכה מתחילה, בלי לצלצל לכולם, נגמר אחרי 60 דקות ריקות. | WhatsApp | אין | https://faq.whatsapp.com/3966323053691518/?cms_platform=android |
| 161 | הצטרפות שקטה עם נפנוף | הקבוצה רואה שאתם מחוברים, בלי התראה. | WhatsApp | אין | https://faq.whatsapp.com/3966323053691518/?cms_platform=android |
| 162 | קהילה של קבוצות | קבוצות רבות תחת קהילה אחת עם הודעות מנהלים. | WhatsApp, Messenger | חלקי: הפורום הוא הקהילה, השיחה יוצאת מדיון. php | https://blog.whatsapp.com/communities-now-available |
| 163 | סקר וקריאה בהודעות קהילה | רק מנהלים, חברים מגיבים, עד 1,024 חברים. | WhatsApp | אין | https://faq.whatsapp.com/582420703681043 |
| 164 | בקשה לדבר ב־Space | Request מתחת למיקרופון. | X Spaces | אין | https://help.x.com/en/using-x/spaces |
| 165 | הקלטת Space וסיכום נוכחות | בסוף: כמה היו וקישור לשיתוף. | X Spaces | אין | https://help.x.com/en/using-x/spaces-hosting |
| 166 | מאזין מרים יד בצ'אט וידאו | המנהלים רואים מי רוצה לדבר. | Telegram | אין | https://telegram.org/blog/voice-chats-on-steroids |
| 167 | צופה בשידור מצטרף לשידור | מרים יד ונכנס לבמה. | Telegram | אין | https://telegram.org/blog/live-streams-forwarding-next-channel |
| 168 | עד 200 נוספים לשיחה פעילה | הוספה המונית לשיחה קיימת. | Telegram | אין: עד 4. php | https://telegram.org/blog/group-calls-made-easy |
| 169 | חדר וירטואלי מתמשך | מקום קבוע שנכנסים אליו כל היום. | Zoom Huddles | אין | https://www.zoom.com/en/products/hub/ |
| | **שיתוף ולוח** | | | | |
| 170 | שיתוף מסך | מציגים מסך או חלון. | Zoom, Meet, Teams, WhatsApp, Telegram | אין: במקום זה תמונה או תוכנית ללוח. board.js | https://telegram.org/blog/group-video-calls |
| 171 | שיתוף שמע עם המסך | הצליל של מה שמשתף נשמע. | WhatsApp | אין | https://blog.whatsapp.com/better-calling-across-desktop-and-mobile |
| 172 | שיתוף חלון של תוכנה אחת | לא כל המסך. | Telegram (מחשב) | אין | https://telegram.org/blog/group-video-calls |
| 173 | שליטה מרחוק | לוקחים שליטה במחשב של מי שמשתף. לא בטלפון. | Zoom | אין | https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0067931 |
| 174 | לעקוב אחרי הסמן של המציג | התצוגה הולכת אחרי מה שהמציג מצביע. | Zoom | חלקי: "עקבו אחריי" בלוח. board.js | https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0068708 |
| 175 | שרטוט של צופים על השיתוף | כל אחד מסמן, המארח יכול לחסום. | Zoom | יש: כולם מציירים, אין חסימה. board.js | https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0060943 |
| 176 | עט נעלם | הקו דוהה תוך שניות, רק למציג. | Zoom | יש: לייזר לכולם. board.js | https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0067931 |
| 177 | תבניות לוח בתוך הפגישה | בוחרים תבנית ופותחים לעריכה או להצגה. | Zoom | אין | https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0058133 |
| 178 | פתקים עם תגיות, הצבעה ונעילה | צבע, אימוג'י, תווית כותב, הצבעה, נעילה. | Zoom Whiteboard | חלקי: הערה ממוספרת עם "סוכם". board.js | https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0061925 |
| 179 | פתקים מבינה מלאכותית | יוצר פתקים מבקשה. | Zoom Whiteboard | אין | https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0057610 |
| 180 | תמונה מהמצלמה ישר ללוח | צילום בטלפון ונשלח לכולם. | אצלנו. Procore דומה (ראו שורה 36 בפירוק של 12.11) | יש. board.js | https://v2.support.procore.com/en-au/product-manuals/drawings-ios/tutorials/add-photos-to-a-drawing-ios |
| 181 | מידה על תוכנית עם כיול | מודדים קו ידוע, ואז כל קו מקבל אורך "בערך". | אצלנו. Bluebeam, Procore (שורות 59 עד 74 בפירוק של 12.11) | יש. board.js | https://support.procore.com/products/online/user-guide/project-level/drawings/tutorials/add-measurements-to-a-drawing |
| 182 | הערה שמסומנת "סוכם" | כל אחד מסמן הערה כסגורה, עם ספירה. | אצלנו. Meet מסמן החלטות בסיכום (שורה 125 בפירוק של 12.11) | יש. board.js | https://support.google.com/meet/answer/14754931?hl=en |
| 183 | ניקוי רק הסימונים שלי | שני לחיצות, רק שלי. | Teams | יש. board.js | https://support.microsoft.com/office/use-annotation-while-sharing-your-screen-in-microsoft-teams-876ba527-7112-437e-b410-5aec7363c473 |
| 184 | שמירת הלוח כתמונה | PNG למכשיר. | Zoom, Claude, Excalidraw | יש: נשמר רק במכשיר. board.js | https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0061925 |
| 185 | לוח בקישור בלי חשבון | קישור מוצפן, השרת רק מעביר. | Excalidraw | אין: הלוח חי רק בתוך השיחה. board.js | https://plus.excalidraw.com/blog/end-to-end-encryption |
| 186 | לוח של צד שלישי בתוך השיחה | Jamboard נסגר, ממליצים על FigJam ו־Miro כתוספים. | Meet | לא רלוונטי: הלוח שלנו מובנה. board.js | https://workspaceupdates.googleblog.com/2023/09/the-next-phase-of-digital-whiteboarding-for-google-workspace.html |
| | **הקלטה, בינה מלאכותית ואחרי** | | | | |
| 187 | הקלטה בענן | המארח מקליט, נשמר בחשבון. | Zoom | אין, בכוונה: "השיחה לא מוקלטת". call.js | https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0061101 |
| 188 | בקשה להקליט | משתתף מבקש מהמארח רשות להקליט. | Zoom | אין | https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0062674 (נקרא במלואו) |
| 189 | סימן הקלטה לכולם | כל המשתתפים רואים שמקליטים. | X Spaces, Meet | הפוך: אצלנו כתוב בכל מסך "השיחה לא מוקלטת". call.js | https://help.x.com/en/using-x/spaces-hosting |
| 190 | תמלול להקלטה | קובץ VTT, רק אנגלית, רק בענן. | Zoom | אין | https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0065911 |
| 191 | הקלטה חכמה | פרקים, נקודות חשובות וצעדים הבאים. | Zoom | אין | https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0061101 |
| 192 | סיכום ושאלות AI בזמן השיחה | אייקון AI, ואם המארח לא הפעיל, מבקשים ממנו. | Zoom | אין | https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0062674 (נקרא במלואו) |
| 193 | תמלולי סיכום נשמרים | המארח והמנהל מורידים או מוחקים. | Zoom | אין | https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0076632 |
| 194 | סיכום AI בלי תמלול | נוצר רק אם המתג דלק כשהפגישה נגמרה. | Teams | אין | https://support.microsoft.com/en-us/teams/meetings/use-intelligent-recap-microsoft-teams-meetings-without-transcription |
| 195 | מקליט קולי עם AI | הקלטת שיחה פנים אל פנים, יותר שפות. | Zoom | אין | https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0080794 |
| 196 | סרטון קצר במקום פגישה | מקליטים מסך ופנים ושולחים. | Zoom Clips, Miro Talktrack | אין | https://www.zoom.com/en/products/hub/ (סיכום חיפוש, דף ייעודי ל־Clips לא נפתח) |
| 197 | מקום אחד לכל מה שנוצר | הקלטות, סיכומים, לוחות, מסמכים. | Zoom Hub | חלקי: הדיון הוא הבית, אבל הלוח לא נשמר בו. board.js | https://www.zoom.com/en/products/hub/ |
| 198 | שיתוף הקלטה בפוסט | קישור מוכן לפרסום. | X Spaces | אין | https://help.x.com/en/using-x/spaces-hosting |
| 199 | הבטחה על שימוש בנתונים | "לא מאמנים מודלים על השמע והווידאו שלכם". | Zoom | יש בדרך אחרת: "שום דבר לא נשמר באתר". board.js | https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0076632 |
| 200 | הזמנת עמדות ומשרדים | הזמנת שולחן או חדר, עם צ'ק אין. | Zoom Workspace Reservation | לא רלוונטי | https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0059638 |

**ספירה:** 200 שורות.

---

## 3. משחקיות וכיף

- **תגובות אימוג'י שנעלמות אחרי כ־10 שניות.** Zoom. https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0063323
- **תגובות מונפשות שמרחפות על המסך.** Zoom באייפון. https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0060612
- **לב בידיים מול המצלמה ממלא את המסך בלבבות, חגיגה בזיקוקים.** Zoom. https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0067842
- **הרמת יד אמיתית מול המצלמה מרימה יד בשיחה.** Meet (ראו שורה 105 בפירוק של 12.11), Zoom. https://support.google.com/meet/answer/10159750
- **סמלי משוב שנשארים: "לאט יותר", "תיכף חוזר".** Zoom. https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0063323
- **אגודל למעלה או למטה בסוף השיחה.** Zoom. https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0066367
- **תגובות בזמן צ'אט קולי, בלי להפריע.** WhatsApp. https://blog.whatsapp.com/new-feature-roundup-updates-to-group-chats-events-calls-channels-and-more
- **אגודל ולב גם לאורח מהדפדפן.** WhatsApp. https://blog.whatsapp.com/now-you-can-invite-anyone-to-a-whatsapp-call-no-account-needed-no-cost-no-time-limit
- **נפנוף כשמצטרפים בשקט לצ'אט קולי.** WhatsApp. https://faq.whatsapp.com/3966323053691518/?cms_platform=android
- **לוח צלילים: קטע שמע קצר שכולם שומעים.** Discord. https://support.discord.com/hc/en-us/articles/12612888127767-Discord-Soundboard-Guide-Using-Adding-and-Managing-Sounds
- **משחקים וצפייה משותפת בתוך הערוץ (Watch Together, Sketch Heads, Letter League).** Discord. https://support.discord.com/hc/en-us/articles/7931156448919-Activity-Sharing-on-Discord-FAQ
- **סטטוס לערוץ: "בונים מטבח, בואו".** Discord. https://support.discord.com/hc/en-us/articles/19583625604887-Voice-Channels-FAQs
- **סרגל תגובות במקשים 1 עד 7, קונפטי ב־f, ריקוד ב־z.** Gather. https://support.gather.town/hc/en-us/articles/15910325457172-Use-Emotes-and-Customize-the-Emote-Bar
- **מחיאות כפיים אוטומטיות כשקבוצה חוגגת יחד.** Gather. https://support.gather.town/articles/4269803312-applause-extension
- **נפנוף שמביא את האדם אליכם.** Gather. https://support.gather.town/articles/3367182370-gather-for-engineering-teams
- **תגובות עם אפקט צליל, GIF בצ'אט.** Butter. https://www.butter.us/features/engagement
- **סדר יום שמתמלא ירוק והופך אדום כשהזמן נגמר.** Butter. https://help.butter.us/agenda
- **טיימר לכולם עם נגן מוזיקה.** Miro. https://help.miro.com/hc/en-us/articles/360017730933-Timer
- **טיימר עם מוזיקה אחת לכולם, כל אחד מנמיך לעצמו.** FigJam. https://help.figma.com/hc/en-us/articles/4402269549591-Stay-on-track-with-the-timer-in-FigJam
- **High five בין שני סמנים, Emotes, צ'אט ליד הסמן, גם לצופים.** FigJam. https://help.figma.com/hc/en-us/articles/15300412458647-Explore-FigJam-files
- **חותמות שנדבקות לפתק ומראות מי חתם.** FigJam (שורה 12 בפירוק של 12.11). https://help.figma.com/hc/en-us/articles/1500004290981
- **הצבעה עם תוצאות מוסתרות עד הסוף.** Miro, FigJam, Zoom Whiteboard. https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0085121
- **צופים מגיבים באימוג'י לרגע מסוים בסרטון הדרכה.** Miro Talktrack. https://help.miro.com/hc/en-us/articles/35405180333202-Talktrack
- **חדר מצויר משותף שבו כולם יושבים יחד.** Zoom Immersive View. https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0058351
- **דמות תלת ממד שמחקה את הפנים.** Zoom Avatars. https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0058351
- **ראשים צפים קטנים.** Around. https://alternativeto.net/news/2025/1/the-video-call-app-around-is-shutting-down-just-over-a-year-after-its-acquisition-by-miro (צד שלישי)
- **מילה חמה בסוף שיחה (kudos) לאדם שעזר.** לא נמצא אצל אף אחד במוצרי הווידאו. קרוב: סקר האגודל של Zoom, שהולך למנהל ולא לאדם.

---

## 4. מה חסר לנו, לפי סדר חשיבות

לבעלי מקצוע ולקונים בטלפון:

1. אורח שנכנס רק עם שם וקישור (בלי מייל וקוד), ובעל המקצוע מאשר אותו. WhatsApp ו־FaceTime כבר עושים את זה.
2. כפתור "שליחת הקישור בוואטסאפ" ו"העתקת קישור" מתוך השיחה ומהכרטיס.
3. צלצול אמיתי לטלפון של מי שלא על דף בפורום (התראת דחיפה), במקום בדיקה כל 25 שניות.
4. תזמון שיחה לשעה מסוימת עם תזכורת וקובץ יומן.
5. חדר המתנה עם "רק רגע" למי שמחכה.
6. הוצאת משתתף ודיווח עליו מתוך השיחה.
7. סיום לכולם בידי מי שפתח.
8. צ'אט קצר בתוך השיחה, לכתובת, מספר טלפון או מחיר שקשה להגיד בקול.
9. שמירת הלוח והסימונים בדיון אחרי השיחה, לא רק כתמונה בטלפון.
10. סיכום בסוף: מה סוכם, ההערות שסומנו "סוכם", המידות, מי היה ומתי.
11. תמונה בתוך תמונה, כדי להסתכל על וואטסאפ או גלריה בלי לאבד את השיחה.
12. שיתוף מסך מהמחשב (תוכנית ב־PDF, הצעת מחיר).
13. הודעה על שיחה שלא נענתה, עם "התקשרו חזרה".
14. מעבר מהטלפון למחשב באמצע השיחה בלי לנתק.
15. תגובות מהירות: אגודל, לב, "מסכים", בלי לפתוח מיקרופון ברעש של אתר בנייה.
16. סינון רעשי רקע, מוצהר ונבדק, לאתרי בנייה ומשאיות.
17. טשטוש רקע, לקונה שמדבר מהבית.
18. מצב נהיגה: קול בלבד, כפתורים ענקיים, הצעה אוטומטית כשזזים.
19. כתוביות חיות בעברית, לרעש ולכבדי שמיעה.
20. הרמת יד ותור כשיש 3 או 4 בשיחה.
21. השתקת משתתף בידי מי שפתח.
22. חדר קבוע לבעל מקצוע בכתובת שלא משתנה ("הלינק שלי").
23. דף תורים בכרטיס בעל המקצוע: לקוח בוחר שעה פנויה.
24. סקר אגודל בסוף השיחה, ומילה טובה לבעל המקצוע שנכנסת לכרטיס שלו.
25. טיימר משותף, למשל "10 דקות ייעוץ חינם".
26. בקשה להקלטה עם הסכמה של כולם, כשבאמת צריך (ליקוי בנייה שמתועד).
27. מכשיר שני ללוח בלבד (טאבלט ללוח, טלפון לווידאו).
28. היסטוריית שיחות לכל חבר.
29. חדר שקופצים אליו בלי צלצול, למשל "שעת שאלות פתוחה" של מהנדס.
30. בדיקה אמיתית על שני טלפונים, ופריסה נבדקת ל־3 ו־4 אנשים.

---

## 5. מה אף אחד מהם לא עושה

1. **שיחה שקשורה לבקשה, לדירה או לפרויקט.** השיחה נפתחת מתוך הבקשה או עמוד הדירה, והכול נשמר שם. קשה להעתיק: Zoom ו־WhatsApp לא יודעים מה זו דירה, בקשה או פרויקט, ואין להם את המאגר.
2. **סיום שיחה בסיכום חתום.** בסוף כל צד מאשר בלחיצה את רשימת "מה סוכם", עם תאריך ושמות, ונשמר בדיון. קשה להעתיק: דורש זהות אמיתית של בעל מקצוע ושל לקוח באותו אתר, והקשר לבקשה.
3. **הצעת מחיר שנכתבת יחד על הלוח.** שורות עבודה, כמות, מחיר, מתוך המידות שנמדדו על התוכנית. קשה להעתיק: דורש מדידה עם כיול, ומחירונים מקומיים לעבודות בארץ.
4. **מדידה על תוכנית עם קנה מידה בתוך שיחת וידאו.** קיים אצלנו בלוח. אצל Bluebeam ו־Procore זה בכלי משרד, לא בשיחה בטלפון. קשה להעתיק: מוצרי וידאו לא בנויים לשרטוט מהנדסי, ומוצרי שרטוט לא בנויים לשיחה.
5. **כרטיס בעל מקצוע חי בתוך השיחה.** רישיון, ביקורות, עבודות קודמות, ואם רשום בפנקס. קשה להעתיק: דורש מאגר מאומת של בעלי מקצוע בארץ ובדיקה מול מאגרי רישוי ממשלתיים.
6. **הזמנת בעל מקצוע נוסף לשיחה לפי מקצוע.** "צריך חשמלאי עכשיו" מביא חשמלאי פנוי מהפורום לשיחה. קשה להעתיק: דורש קהילה של בעלי מקצוע פעילים וזמינים, לא רק כלי.
7. **צילום של המקום נצמד לנקודה בתוכנית.** צולם בשיחה ונועץ במקום בתוכנית, ונשאר בבקשה. קשה להעתיק: דורש לוח, תוכנית ושיחה כמוצר אחד.
8. **מילה טובה בסוף שיחה שנכנסת לכרטיס.** לקוח מודה לבעל המקצוע בלחיצה, והתודה מופיעה בכרטיס עם תאריך. קשה להעתיק: הכלים הקיימים מודדים איכות שיחה, לא אמון בין אנשים.
9. **שיחה בעברית מוכנה לאתר בנייה.** קול בלבד, כפתורים גדולים, השתקה אוטומטית ברעש חזק, עבודה עם כפפות. קשה להעתיק: דורש התאמה מקומית ובדיקות בשטח שהחברות הגדולות לא יעשו לשוק קטן.
10. **רצף אחרי השיחה: משימות עם תאריך וביקור באתר.** מתוך הערות "סוכם" נוצרות משימות ותזכורת לביקור, בתוך הבקשה. קשה להעתיק: דורש את הבקשה, הצדדים, והלוח באותו מקום.

---

## 6. מה לא אומת ולמה

- **רוב הדפים נקראו דרך סיכום של מנוע החיפוש**, לא נפתחו במלואם. נפתחו במלואם: Zoom KB0060612 (הגדרות), Zoom KB0062674 (כפתורי משתתף), שני פוסטים בבלוג של WhatsApp (אורחים 14.10.2026, ריכוז תכונות 9.4.2025). יתכן שפרטים קטנים בסיכומים לא מדויקים.
- **Zoom:** חלק מהשליטה במארח (השתקה, שינוי שם, הוצאה, הבלטה, הצמדה, חדר המתנה למשתתפים לא מחוברים) נלקח מדפי אוניברסיטאות. דף התפקידים הרשמי מפנה ל־support.zoom.us ולא נפתח. תמונה בתוך תמונה בטלפון, חיסכון בנתונים, ושיתוף לוואטסאפ לא נמצאו בדף רשמי. Huddles ו־Docs רק בסיכום כללי. שעוני ספירה בחדרי עבודה לא נבדקו.
- **Meet:** "סיום לכולם" לא נמצא בחיפוש. הרמת יד לפי תנועה מגיעה מהפירוק של 12.11.
- **Teams:** Together mode לא נמצא בדף רשמי. אין פרט עליו מעבר לשם.
- **Messenger ו־Facebook:** סגירת Messenger Rooms וסגירת Community Chats הגיעו מסיכומי חיפוש. דף ישיר לא נפתח. שמע חי בקבוצות פייסבוק (live audio) לא אומת.
- **X:** קהילות X נבדקו רק ברמת "יש מנהלים וכללים". מספר הדוברים סותר בין שני דפים (13 מול 11 ועוד 2).
- **Telegram:** תגובות בתוך צ'אט וידאו לא אומתו.
- **FaceTime:** תגובות ותנועות למשתתף מהדפדפן לא אומתו.
- **Around:** האם עדיין פעיל, סותר בין מקורות. כל מה שעליו מצד שלישי.
- **Gather:** "ring" או צלצול לא נמצא.
- **Butter:** מדבקות לא נמצאו. המקורות הם דפי שיווק של Butter.
- **Discord:** סטטוס אישי (לא פנוי, לא להפריע) לא נמצא.
- **אצלנו:** הכול מקריאת קוד ב־18.11.2026. לא נבדק בטלפון אמיתי, לא נבדקה פריסה ל־3 ו־4 אנשים, לא נבדק אם הדפדפן מסנן רעשים כברירת מחדל דרך LiveKit, ולא נבדק אם יש הצפנה מקצה לקצה.
- **לא נכנסנו לשום מוצר**, לא פתחנו חשבון, לא פתרנו בדיקת רובוט. אף דף לא נחסם בדרך שדרשה זאת.
