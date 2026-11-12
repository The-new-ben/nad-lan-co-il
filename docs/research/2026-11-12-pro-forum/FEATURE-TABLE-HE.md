# טבלת פיצ'רים: פורום ורשת לאנשי מקצוע בנדל"ן

בטבלה 333 שורות, מאוחדות מ-teardown-forums.md (191 שורות), teardown-social.md (180 שורות) וחלק א של israel-law-business.md (אתרים ישראליים ומאגרי רישוי); פיצ'ר שחזר בכמה מוצרים אוחד לשורה אחת.
עמודת "יש לנו היום" נשענת רק על existing-state.md, שהוא סקירת קוד ולא בדיקה באתר החי.
תאריך: 12.11.2026.


## כניסה והרשמה

| פיצ'ר | מיקרו-פיצ'ר (מה בדיוק קורה, משפט אחד) | למי יש | יש לנו היום | החלטה | למה | מקור |
|---|---|---|---|---|---|---|
| קריאה בלי כניסה | כל אחד קורא דיונים, שאלות וכרטיסים בלי להתחבר, וכניסה נדרשת רק כדי לכתוב. | Discourse, הסולידית, Houzz, מדרג | חלקי: כרטיסים פתוחים בלי כניסה | גרסה ראשונה | תנועה מגוגל חייבת לקרוא חופשי | https://github.com/discourse/discourse/blob/main/config/site_settings.yml ; https://www.hasolidit.com/kehila/ ; https://www.houzz.com/discussions ; https://www.midrag.co.il/Expanel |
| שואלים ועונים בלי ניקוד | שאלה, תשובה ועריכה לא דורשות צבירת נקודות, והמוניטין רשות בלבד. | Stack Overflow | לא | גרסה ראשונה | כל אחד פותח דיון מהרגע הראשון | https://stackoverflow.com/help/whats-reputation ; https://stackoverflow.com/help/privileges/new-user |
| קישור כניסה במייל | קישור במייל מכניס בלי סיסמה, והוא תקף 48 שעות. | Discourse | לא | גרסה ראשונה | כניסה בצעד אחד בלי סיסמה | https://github.com/discourse/discourse/blob/main/config/site_settings.yml |
| כניסה עם החשבון של האתר הראשי | הפורום משתמש בכניסה של האתר הראשי, בלי הרשמה נוספת. | Discourse | חלקי: קישור אישי בלי סיסמה למתווכים | גרסה ראשונה | הפורום בתוך האתר, זהות אחת | https://www.discourse.org/features ; https://github.com/discourse/discourse/blob/main/config/site_settings.yml |
| כניסה עם גוגל ורשתות | כפתורי Google, Facebook, X ועוד, ו-Google כבוי כברירת מחדל. | Discourse | חלקי: כניסת גוגל מאחורי מתג | מאוחר יותר | כניסה חברתית נדחית לשלב מאוחר | https://www.discourse.org/features ; https://github.com/discourse/discourse/tree/main/plugins |
| מפתחות גישה | כניסה עם מפתח הגישה של הטלפון במקום סיסמה, פעיל כברירת מחדל. | Discourse | לא | מאוחר יותר | קוד במייל או בטלפון פשוט יותר עכשיו | https://github.com/discourse/discourse/blob/main/config/site_settings.yml |
| קישורי הזמנה | קישור הזמנה תקף 90 יום, עד 10 ביום, מותר מרמת אמון 2. | Discourse | חלקי: הזמנות בקישור לפירגון | שלב שני | חלק מקבלת הפנים | https://github.com/discourse/discourse/blob/main/config/site_settings.yml |
| הזמנה, ייבוא ואימות מייל | קישורי הזמנה, ייבוא חברים בכמות ואימות מייל חובה בהרשמה פתוחה. | Circle | חלקי: הזמנות בקישור לפירגון | שלב שני | חלק מקבלת הפנים | https://help.circle.so/p/audience/onboarding |
| הזמנה לקבוצה במייל | מנהל מזמין אנשים להצטרף לקבוצה דרך המייל. | Facebook Groups | חלקי: הזמנות בקישור לפירגון | שלב שני | בישראל הזמנה בוואטסאפ חשובה יותר | https://about.fb.com/news/2022/03/new-tools-for-facebook-group-admins/ |
| בוט הדרכה | בוט מוביל משתמש חדש במסלול היכרות, והודעת הפתיחה כבויה כברירת מחדל. | Discourse | לא | שלב שני | חלק מקבלת הפנים | https://github.com/discourse/discourse/blob/main/plugins/discourse-narrative-bot/config/settings.yml |
| טיפים בשימוש ראשון | טיפים קטנים בהקשר בפעם הראשונה, כבויים כברירת מחדל. | Discourse | לא | שלב שני | חלק מקבלת הפנים | https://github.com/discourse/discourse/blob/main/config/site_settings.yml |
| שאלות בהצטרפות | חבר חדש עונה "אני מתווך, שמאי, משקיע" וזה קובע מה יראה, ואפשר לשנות אחר כך. | Discord | לא | שלב שני | בחירות הצטרפות | https://support.discord.com/hc/en-us/articles/11074987197975-Community-Onboarding-FAQ ; https://raw.githubusercontent.com/discord/discord-api-docs/main/developers/resources/guild.mdx |
| מסך ברוכים הבאים | תיאור הקהילה ועד 5 מקומות מומלצים להתחיל בהם. | Discord | לא | שלב שני | חלק מקבלת הפנים | https://raw.githubusercontent.com/discord/discord-api-docs/main/developers/resources/guild.mdx |
| הודעת ברוכים הבאים | חבר חדש מקבל אוטומטית ברכה אישית ואת חוקי הקבוצה. | Facebook Groups | לא | שלב שני | הודעת פתיחה בשלב שני | https://about.fb.com/news/2021/11/new-tools-in-facebook-groups/ |
| חוקים גלויים לחדשים | חוקים בצד המסך, שרשור חוקים נעוץ ותזכורות אוטומטיות. | Reddit | לא | גרסה ראשונה | חוקי קהילה בכניסה | https://support.reddithelp.com/hc/en-us/articles/15484358732692-Welcoming-new-members |
| אישור חוקים לפני כתיבה | חבר חדש מוגבל עד שהוא מאשר את חוקי הקהילה. | Discourse, Discord | לא | גרסה ראשונה | חוקי קהילה והודעת פרטיות בכניסה | https://github.com/discourse/discourse/blob/main/plugins/discourse-policy/config/settings.yml ; https://raw.githubusercontent.com/discord/discord-api-docs/main/developers/resources/guild.mdx |
| הזמנה להירשם אחרי קריאה | קורא שלא נכנס רואה הזמנה קצרה להירשם אחרי שקרא. | Discourse | לא | גרסה ראשונה | מוביל לכניסה בצעד אחד | https://github.com/discourse/discourse/blob/main/config/site_settings.yml |
| שאלות בכניסה לאישור | ההרשמה דורשת תשובה לשאלה (בפייסבוק עד 3 שאלות של 200 תווים) ומנהל מאשר. | Lemmy, Facebook Groups | לא | מאוחר יותר | סותר כניסה בצעד אחד, מתאים לחדר סגור | https://join-lemmy.org/docs/users/01-getting-started.html ; https://raw.githubusercontent.com/LemmyNet/lemmy/0.16.7/config/defaults.hjson ; https://www.facebook.com/help/200755420421098/ (לא אומת במלואו) |
| אישור אוטומטי לפי פרופיל | מנהל מאשר לבד מי שיש לו תמונה, 10, 20 או 50 קשרים, ומעט חברויות בקבוצות. | LinkedIn Groups | לא | מאוחר יותר | שייך לקבוצות עם מנהלים | https://www.linkedin.com/help/linkedin/answer/a1396211 |
| אישור אוטומטי לפי תחום ותפקיד | מי שהתחום, התפקיד או הכישורים שלו תואמים מאושר לבד, והשאר ממתינים. | LinkedIn Groups | לא | מאוחר יותר | שייך לקבוצות עם מנהלים | https://www.linkedin.com/help/linkedin/answer/a1396211 |
| אישור ידני עם סינון | בקשות הצטרפות מאושרות בכמות ומסוננות לפי מקום, חברה ותחום, בלי התראה למנהל. | LinkedIn Groups | לא | מאוחר יותר | שייך לקבוצות עם מנהלים | https://www.linkedin.com/help/linkedin/answer/a541728 |
| עוזר מנהל לבקשות הצטרפות | מנהל קובע תנאים לאישור או לדחייה אוטומטיים, למשל חשבון חדש נדחה. | Facebook Groups | לא | מאוחר יותר | שייך לקבוצות עם מנהלים | https://about.fb.com/news/2022/03/new-tools-for-facebook-group-admins/ |
| חברים מאשרים קולגות | חבר רגיל מאשר בקשת הצטרפות של קשר ישיר שלו. | LinkedIn Groups | לא | מאוחר יותר | שייך לקבוצות עם מנהלים | https://www.linkedin.com/help/linkedin/answer/a553202 |
| כתיבה אנונימית | חבר כותב ומגיב בלי שם, והשם גלוי רק לצוות. | Discourse, Facebook Groups | לא | לא נבנה | חשיפה ללשון הרע ולספאם | https://github.com/discourse/discourse/blob/main/config/site_settings.yml ; https://www.discourse.org/features ; https://www.facebook.com/help/372188260706718 (לא אומת במלואו) |
| אישור לפוסטים אנונימיים | מנהל דורש אישור לפוסט אנונימי, לפוסט בכינוי ולעריכה. | Facebook Groups | לא | לא נבנה | תלוי בכתיבה אנונימית שלא נבנית | https://www.facebook.com/help/372188260706718 (לא אומת במלואו) |
| כינוי במקום שם | שם משתמש שלא חושף זהות, או כינוי באישור מנהל. | Reddit, Facebook Groups | לא | לא נבנה | קרוב לאנונימי, אנשי מקצוע כותבים בשם | https://support.reddithelp.com/hc/en-us/articles/7420342178324-How-does-being-anonymous-work-on-Reddit ; https://www.facebook.com/help/1997112804420300 (לא אומת במלואו) |
| שם תצוגה אמיתי | שם אמיתי בעברית מוצג לצד שם המשתמש. | Discourse, Flarum | חלקי: שם ותפקיד בכרטיס | גרסה ראשונה | כניסה בשם, שם אמיתי ליד כל הודעה | https://github.com/discourse/discourse/blob/main/config/site_settings.yml ; https://docs.flarum.org/extensions/ |
| רמות אימות לקהילה | אפשר לדרוש מייל מאומת, חשבון בן 5 דקות, חברות של 10 דקות או טלפון מאומת. | Discord | לא | גרסה ראשונה | מגבלת משתמש חדש וקוד לטלפון | https://raw.githubusercontent.com/discord/discord-api-docs/main/developers/resources/guild.mdx |
| מגבלת הרשמות לכתובת IP | עד 3 חשבונות לכתובת, 6 כניסות לדקה ו-30 לשעה, ודומיין מייל זמני חסום. | Discourse | חלקי: מגבלות קצב בטפסים | גרסה ראשונה | מגבלות קצב | https://github.com/discourse/discourse/blob/main/config/site_settings.yml |
| שדה מלכודת והצלחה מדומה | שדה נסתר ואתגר הפוך, ורובוט שנכשל מקבל "נשלח" בלי שנוצר דבר. | Discourse | חלקי: שדה מלכודת בכל הטפסים | גרסה ראשונה | שדה מלכודת נסתר | https://github.com/discourse/discourse/blob/main/frontend/discourse/app/components/honeypot-input.js ; https://github.com/discourse/discourse/blob/main/app/controllers/users_controller.rb |
| בדיקת אדם | hCaptcha או reCAPTCHA כבויים כברירת מחדל, בגרסה השקטה סף 0.5, ו-Lemmy מוסיף אימות מייל. | Discourse, Lemmy | לא | גרסה ראשונה | רק בדיקה שקטה, בלי חידה גלויה | https://github.com/discourse/discourse/blob/main/plugins/discourse-captcha/config/settings.yml ; https://raw.githubusercontent.com/LemmyNet/lemmy/0.16.7/config/defaults.hjson |
| ציון סיכון להרשמה | כל הרשמה מקבלת ציון: נמוך עובר, בינוני נבחן, גבוה נחסם, ואחר כך בדיקת אדם. | LinkedIn | לא | מאוחר יותר | מודל כבד, קוד לטלפון מספיק בהתחלה | https://www.linkedin.com/blog/engineering/trust-and-safety/automated-fake-account-detection-at-linkedin |
| בדיקת תמונה מיוצרת | מודל בודק אם תמונת פרופיל נוצרה בבינה מלאכותית, בלי זיהוי פנים. | LinkedIn | לא | מאוחר יותר | פיקוח בבינה מלאכותית | https://www.linkedin.com/blog/member/trust-and-safety/new-linkedin-profile-features-help-verify-identity-detect-remove-fake-accounts-boost-authenticity |
| עסק מוסיף את עצמו | בעל עסק פותח רשומה בחינם בעצמו. | B144 | חלקי: הצטרפות עצמית בפירגון | גרסה ראשונה | איש מקצוע נכנס בצעד אחד | https://www.b144.co.il/ |

## כתיבה

| פיצ'ר | מיקרו-פיצ'ר (מה בדיוק קורה, משפט אחד) | למי יש | יש לנו היום | החלטה | למה | מקור |
|---|---|---|---|---|---|---|
| שמירת טיוטה | הטיוטה נשמרת לבד, ובטלפון מופיע פס "טיוטה בתהליך, הקישו להמשך". | Discourse | לא | גרסה ראשונה | בטלפון מפריעים באמצע | https://www.discourse.org/features ; https://github.com/discourse/discourse/blob/main/config/locales/client.en.yml |
| ציטוט מסימון טקסט | סימון טקסט בתגובה מציג כפתור ציטוט, וכל משתמש יכול לכבות אותו. | Discourse | לא | גרסה ראשונה | ציטוט תגובה | https://github.com/discourse/discourse/blob/main/config/locales/client.en.yml ; https://github.com/discourse/discourse/blob/main/config/site_settings.yml |
| שיתוף ציטוט | ליד כפתור הציטוט יש גם כפתור "שיתוף" לקטע המסומן. | Discourse | לא | שלב שני | נוח, לא חיוני בהתחלה | https://github.com/discourse/discourse/blob/main/config/locales/client.en.yml |
| אזכור עם @ | @שם שולח התראה, עד 10 אזכורים בהודעה ו-2 למשתמש חדש. | Discourse, Flarum, Lemmy, Discord | לא | שלב שני | אזכורים בשלב שני | https://github.com/discourse/discourse/blob/main/config/site_settings.yml ; https://join-lemmy.org/ |
| אזכור בלי @ | מקלידים שם ולוחצים Tab כדי להכניס אזכור (ניסוי). | Discord | לא | שלב שני | אזכורים בשלב שני | https://support.discord.com/hc/en-us/articles/35692242798743-Mention-Suggestions-FAQ |
| אזכור קבוצה | @קבוצה מגיע לכל היותר ל-100 אנשים. | Discourse | לא | שלב שני | אזכורים בשלב שני | https://github.com/discourse/discourse/blob/main/config/site_settings.yml |
| תצוגה מקדימה לקישור | קישור מודבק הופך לכרטיס תצוגה, עד 50 בהודעה, עם רשימת אתרים חסומים. | Discourse | לא | שלב שני | תצוגת קישורים בשלב שני | https://www.discourse.org/features ; https://github.com/discourse/discourse/blob/main/config/site_settings.yml |
| העלאת תמונה בגרירה והדבקה | גוררים או מדביקים תמונה לעורך, עד 10,240 קילובייט. | Discourse, Lemmy | לא | שלב שני | הדבקה והעלאת תמונות | https://www.discourse.org/features ; https://github.com/discourse/discourse/blob/main/config/site_settings.yml ; https://join-lemmy.org/ |
| העתקת תמונות חיצוניות | תמונה מאתר אחר נשמרת אצלנו כדי שההודעה לא תישבר. | Discourse | לא | שלב שני | חלק מהעלאת תמונות | https://github.com/discourse/discourse/blob/main/config/site_settings.yml |
| עורך עם עיצוב פשוט | עורך שמעצב כמו במעבד תמלילים, לצד שפות עיצוב טקסט. | Discourse, Flarum | לא | גרסה ראשונה | פתיחת דיון צריכה עורך פשוט | https://www.discourse.org/features ; https://flarum.org/ |
| בוחר אימוג'י | בוחר עם חיפוש, חמש ערכות ואימוג'י מותאמים. | Discourse, Flarum, Lemmy | לא | מאוחר יותר | המקלדת בטלפון כבר נותנת | https://www.discourse.org/features ; https://join-lemmy.org/ |
| סקר | סקר עם 2 עד 4 אפשרויות ומועד סיום (לינקדאין), או עד 20 אפשרויות (Discourse). | Discourse, LinkedIn | לא | שלב שני | סקרים בשלב שני | https://github.com/discourse/discourse/blob/main/plugins/poll/config/settings.yml ; https://www.linkedin.com/help/linkedin/answer/a522948 |
| "יש דיון דומה" | בזמן הקלדת כותרת מופיעים דיונים דומים, מכותרת של 10 תווים. | Discourse | לא | גרסה ראשונה | מונע שאלות כפולות | https://github.com/discourse/discourse/blob/main/config/locales/client.en.yml ; https://github.com/discourse/discourse/blob/main/config/site_settings.yml |
| חסימת כותרת כפולה | כותרת זהה לדיון קיים נדחית כברירת מחדל. | Discourse | לא | גרסה ראשונה | טקסט כפול נדחה | https://github.com/discourse/discourse/blob/main/config/site_settings.yml |
| תשובות מוכנות לצוות | הצוות שולף תשובות מוכנות ונימוקי הסרה שמורים. | Discourse, Reddit | לא | גרסה ראשונה | כלי לתור הבדיקה של הצוות | https://github.com/discourse/discourse/blob/main/plugins/discourse-templates/config/settings.yml ; https://support.reddithelp.com/hc/en-us/search?query=removal+reasons |
| תשובה כדיון חדש | מהעורך אפשר לפתוח דיון חדש שמקשר חזרה לדיון המקורי. | Discourse | לא | שלב שני | נוח, לא חיוני בהתחלה | https://github.com/discourse/discourse/blob/main/config/locales/client.en.yml |
| חלון עריכה שקט | תיקון בתוך 5 דקות ופחות מ-100 תווים לא נרשם כגרסה חדשה. | Discourse | לא | שלב שני | חלון עריכה | https://github.com/discourse/discourse/blob/main/config/site_settings.yml |
| מגבלת זמן לעריכה | משתמש חדש עורך עד 24 שעות, ותיק עד 30 יום. | Discourse | לא | שלב שני | חלון עריכה | https://github.com/discourse/discourse/blob/main/config/site_settings.yml ; https://blog.discourse.org/2018/06/understanding-discourse-trust-levels/ |
| היסטוריית עריכות ציבורית | כל אחד רואה את גרסאות ההודעה, עם שם העורך ואפשרות החזרה. | Discourse, Stack Overflow | לא | שלב שני | היסטוריית עריכה | https://github.com/discourse/discourse/blob/main/config/site_settings.yml ; https://stackoverflow.com/help/editing |
| סיבת עריכה | שדה רשות "למה אתם עורכים?". | Discourse | לא | שלב שני | חלק מהיסטוריית העריכה | https://github.com/discourse/discourse/blob/main/config/locales/client.en.yml |
| עריכה קהילתית בבדיקה | עריכה של משתמש חדש נכנסת לתור ודורשת 2 אישורים. | Stack Overflow | לא | מאוחר יותר | קרוב לדפי ויקי | https://stackoverflow.com/help/editing |
| הודעת ויקי | הודעה שאחרים יכולים לערוך יחד. | Discourse, Stack Overflow | לא | מאוחר יותר | דפי ויקי | https://www.discourse.org/features ; https://stackoverflow.com/help/privileges |
| אזהרת חוקים בזמן כתיבה | הצוות מגדיר תבניות טקסט, והכותב רואה אזהרה עוד לפני השליחה. | Reddit | חלקי: מסנן מילים אסורות במתווכים | שלב שני | אחרי שכללי החסימה עובדים | https://support.reddithelp.com/hc/en-us/articles/17625458521748-Automations-Post-Comment-Guidance-Set-Up |
| בדיקת חוקים בבינה מלאכותית | בשליחה מודל בודק את הטיוטה מול החוקים ומסמן חשד להפרה. | Reddit | לא | מאוחר יותר | פיקוח בבינה מלאכותית | https://support.reddithelp.com/hc/en-us/articles/35317229808660-Post-Check-Poster-Eligibility-Guide |
| כיבוי התראה בתשובה | תשובה מתריעה לכותב המקורי, והמשיב יכול לכבות. | Discord | לא | שלב שני | קרוב לאזכורים | https://support.discord.com/hc/en-us/articles/360057382374-Replies-FAQ |
| הסתרה והרחבה בטקסט | ספוילר, בלוק נפתח, הערות שוליים ותאריכים לפי שעון מקומי. | Discourse | לא | מאוחר יותר | לא נחוץ לפורום מקצועי בהתחלה | https://www.discourse.org/features ; https://github.com/discourse/discourse/tree/main/plugins |
| אורך מינימלי | הודעה לפחות 20 תווים וכותרת 15, וטקסט כמו "אאאא" נחסם. | Discourse | לא | גרסה ראשונה | מגבלות משתמש חדש | https://github.com/discourse/discourse/blob/main/config/site_settings.yml |
| תגית חובה בדיון חדש | הפורום יכול לדרוש לפחות תגית אחת, עד 5 תגיות. | Discord | לא | שלב שני | תגיות בשלב שני | https://raw.githubusercontent.com/discord/discord-api-docs/main/developers/resources/channel.mdx ; https://support.discord.com/hc/en-us/articles/6208479917079-Forum-Channels-FAQ |
| דיונים קבועים מתוזמנים | הצוות קובע דיון שחוזר כל שעה, יום, שבוע או חודש. | Reddit | לא | שלב שני | דיון מומחה שבועי | https://support.reddithelp.com/hc/en-us/articles/15484443169556-Scheduled-and-Recurring-Posts |
| תזמון פוסט | פוסט מתוזמן מ-10 דקות עד 3 חודשים קדימה, ואפשר לערוך, להזיז או לפרסם מיד. | LinkedIn | לא | שלב שני | קרוב לדיונים מתוזמנים | https://www.linkedin.com/help/linkedin/answer/a1347212 |
| טיוטות ותזמון בידי בינה מלאכותית | עוזר מנהל מנסח פוסטים ומתזמן עד חמישה בבת אחת. | Facebook Groups | לא | מאוחר יותר | בינה מלאכותית | https://about.fb.com/news/2026/10/new-tools-for-the-admins-who-build-communities-on-forum/ |
| יומן מנהלים משותף | מנהלים רואים יומן אחד של פוסטים מתוזמנים. | Facebook Groups | לא | מאוחר יותר | צוות קטן בהתחלה | https://about.fb.com/news/2026/10/new-tools-for-the-admins-who-build-communities-on-forum/ |
| שאלה הופכת לכרטיס בקשה | פוסט שנקרא כשאלה מעוצב מחדש כדי להזמין עצות. | Facebook Groups | לא | שלב שני | שיפור אחרי שהליבה עובדת | https://about.fb.com/news/2021/07/new-ways-to-elevate-experts-in-facebook-groups/ |

## קריאה ודיון

| פיצ'ר | מיקרו-פיצ'ר (מה בדיוק קורה, משפט אחד) | למי יש | יש לנו היום | החלטה | למה | מקור |
|---|---|---|---|---|---|---|
| בית פורום אחד וכתובת קבועה לכל דיון | כל שאלה או שרשור יושבים בכתובת קבועה עם מספר, ולפעמים גם שם. | מדרג, הסולידית, Houzz, תפוז | לא | גרסה ראשונה | כתובת יציבה לכל דיון | https://www.midrag.co.il/Expanel ; https://www.hasolidit.com/kehila/forums/%D7%A0%D7%93%D7%9C-%D7%9F.28/ ; https://www.houzz.com/discussions ; https://www.tapuz.co.il/forums/ (לא אומת במלואו) |
| "המומחים עונים" | אנשי מקצוע עונים על שאלות גולשים לפי תחום, ובתפוז יש מדור מומחים. | מדרג, תפוז | לא | גרסה ראשונה | פתיחת דיון ותשובות | https://www.midrag.co.il/Expanel ; https://www.tapuz.co.il/forums/ (לא אומת במלואו) |
| איש מקצוע עונה עם קישור לכרטיס | אנשי מקצוע כותבים בדיונים והשם שלהם מקשר לפרופיל. | Houzz | לא | גרסה ראשונה | תווית תפקיד ליד השם | https://www.houzz.com/discussions |
| טעינה בגלילה | הודעות נטענות תוך כדי גלילה, בלי עמודים. | Discourse | לא | שלב שני | בהתחלה הדיונים קצרים | https://www.discourse.org/features |
| מעקב מיקום קריאה | המערכת סופרת זמן קריאה לכל הודעה, עוצרת אחרי 3 דקות בלי גלילה. | Discourse | לא | שלב שני | בסיס למונה "לא נקרא" | https://github.com/discourse/discourse/blob/main/frontend/discourse/app/services/screen-track.js |
| מונה חדש ולא נקרא | דיון נחשב חדש יומיים, ונכנס למעקב אחרי 5 דקות קריאה. | Discourse | לא | שלב שני | דורש כניסה ומעקב | https://github.com/discourse/discourse/blob/main/config/site_settings.yml |
| קפיצה להודעה | כפתורי "קפוץ להודעה", "נקרא לאחרונה" ו"להודעה האחרונה". | Discourse | לא | שלב שני | שימושי כשהדיונים יתארכו | https://github.com/discourse/discourse/blob/main/config/locales/client.en.yml |
| סרגל ציר זמן | ציר אנכי עם גלילה וכפתור חזרה בדיונים ארוכים. | Discourse | לא | מאוחר יותר | רק לדיונים ארוכים מאוד | https://github.com/discourse/discourse/tree/main/frontend/discourse/app/components/topic-timeline ; https://github.com/discourse/discourse/blob/main/config/locales/client.en.yml |
| הרחבת הקשר | תשובה נפתחת במקום כדי להראות מה לפניה ואחריה, וציטוט נפתח למקור. | Discourse | לא | מאוחר יותר | לא חיוני בהתחלה | https://www.discourse.org/features |
| סיכום לפי הודעות מובילות | "סכם" מצמצם דיון של 50 הודעות ומעלה להודעות הפופולריות. | Discourse | לא | מאוחר יותר | רלוונטי רק לדיונים גדולים | https://www.discourse.org/features ; https://github.com/discourse/discourse/blob/main/config/site_settings.yml |
| סיכום בבינה מלאכותית | סיכום ושורת תמצית לכל דיון, כבוי כברירת מחדל. | Discourse | לא | מאוחר יותר | בינה מלאכותית | https://github.com/discourse/discourse/blob/main/plugins/discourse-ai/config/settings.yml |
| סימון התשובה שעזרה | השואל מסמן תשובה, היא מוצגת מתחת לשאלה עם סימן וי, ובסטאק אוברפלו גם נקודות. | Discourse, Stack Overflow | לא | גרסה ראשונה | השואל מסמן את מה שעזר | https://github.com/discourse/discourse/blob/main/plugins/discourse-solved/config/settings.yml ; https://stackoverflow.com/help/accepted-answer |
| תגובה נעוצה של מנהל | מנהל נועץ תגובה, למשל תשובה או תיקון, כדי שכולם יראו. | Facebook Groups | לא | שלב שני | הודעות נעוצות | https://about.fb.com/news/2026/10/new-tools-for-the-admins-who-build-communities-on-forum/ |
| תגובות מקוננות | תגובות בעץ, עם מיון חם, מובילות, חדשות, ישנות ושטוח. | Lemmy, Reddit | לא | מאוחר יותר | רשימה שטוחה פשוטה יותר בטלפון | https://join-lemmy.org/docs/users/03-votes-and-ranking.html |
| מיון דיונים | פעילים, חמים, שנויים במחלוקת, חדשים, הכי הרבה תגובות ומובילים לפי תקופה. | Lemmy | לא | שלב שני | חלק מדירוג הפיד | https://join-lemmy.org/docs/users/03-votes-and-ranking.html |
| מיון תוצאות חיפוש | רלוונטיות, חם, מוביל, חדש ומספר תגובות, עם סינון זמן. | Reddit | לא | שלב שני | שיפור אחרי שהליבה עובדת | https://support.reddithelp.com/hc/en-us/articles/19695706914196-What-filters-and-sorts-are-available |
| רשימה או גלריה | מיון לפי פעילות אחרונה או יצירה, ותצוגת רשימה או גלריה. | Discord | לא | שלב שני | שיפור תצוגה | https://raw.githubusercontent.com/discord/discord-api-docs/main/developers/resources/channel.mdx |
| הסתרת דיונים רדומים | דיון בלי פעילות עובר ל"ישנים" אחרי שעה עד שבוע, ותגובה מחזירה אותו. | Discord | לא | מאוחר יותר | בפורום צעיר כל דיון צריך להיראות | https://support.discord.com/hc/en-us/articles/6208479917079-Forum-Channels-FAQ |
| קרוסלת דיונים מודגשים | עד 6 פוסטים מודגשים בקרוסלה, כל אחד עם תווית כמו אירוע או הודעה. | Reddit | לא | שלב שני | הודעות נעוצות | https://support.reddithelp.com/hc/en-us/articles/15484641176724-Community-highlights-sticky-posts |
| נעיצת דיון | דיונים נעוצים בראש הרשימה, הודעות מנהלים מסודרות למעלה. | Flarum, Discourse, Discord, Lemmy, Facebook Groups, הסולידית | לא | שלב שני | הודעות נעוצות | https://docs.flarum.org/extensions/ ; https://www.discourse.org/features ; https://join-lemmy.org/docs/users/04-moderation.html ; https://about.fb.com/news/2021/11/new-tools-in-facebook-groups/ ; https://www.hasolidit.com/kehila/forums/%D7%A0%D7%93%D7%9C-%D7%9F.28/ |
| דיונים קשורים בסוף הדיון | בסוף כל דיון בלוק "דיונים מוצעים", ואפשרות לקשורים בבינה מלאכותית. | Discourse | לא | גרסה ראשונה | קרוב לדיונים דומים, משאיר את מי שהגיע מגוגל | https://github.com/discourse/discourse/blob/main/config/locales/client.en.yml ; https://github.com/discourse/discourse/blob/main/plugins/discourse-ai/config/settings.yml |
| מוני צפיות ותגובות | מספר הצפיות והתגובות מוצג ברשימה, וצבע לפי כמה הדיון חם. | Discourse | לא | גרסה ראשונה | מוני צפיות ותגובות | https://github.com/discourse/discourse/blob/main/config/site_settings.yml |
| זמן הפעילות האחרונה | ליד כל פורום ודיון כתוב מתי נכתבה ההודעה האחרונה. | הסולידית, Houzz | לא | גרסה ראשונה | חלק מהמונים, מראה שיש חיים | https://www.hasolidit.com/kehila/ ; https://www.houzz.com/discussions |
| זמן קריאה כולל | סך זמן הקריאה של משתמש מוצג בסטטיסטיקה שלו. | Discourse | לא | מאוחר יותר | ערך נמוך | https://github.com/discourse/discourse/blob/main/config/locales/client.en.yml |
| סגירה ככפילות | שאלה כפולה מקבלת תווית ופס שמקשר למקור, אחרי 3 הצבעות. | Stack Overflow | לא | מאוחר יותר | בהתחלה מספיק "יש דיון דומה" | https://stackoverflow.com/help/duplicates |
| שאלה מוגנת | אחרי תשובות חלשות מחדשים, מענה דורש 10 נקודות. | Stack Overflow | לא | לא נבנה | שער ניקוד שחוסם אנשים רגילים | https://stackoverflow.com/help/privileges/new-user |
| עמודות חיות זו לצד זו | דף עם עמודות חיות של דיונים והתראות. | Flarum | לא | מאוחר יותר | לא מתאים לטלפון | https://flarum.org/ |
| סינון לפי תגית | סינון דיונים לפי תגית אחת או כמה, ולחיצה על תווית פותחת את כל הדומים. | Discord, Reddit | לא | שלב שני | תגיות בשלב שני | https://support.discord.com/hc/en-us/articles/6208479917079-Forum-Channels-FAQ ; https://support.reddithelp.com/hc/en-us/articles/15484545678996-Post-Flair |
| דירוג תגובות | התגובות שלי, של חברים והנעוצות קודם, ואחריהן לפי רלוונטיות ופופולריות. | Instagram | לא | שלב שני | חלק מהדירוג | https://transparency.meta.com/features/explaining-ranking/ig-comments/ |
| מיון "מאומתים קודם" | הצופה ממיין תגובות לפי חדשות או לפי מאומתים קודם. | Instagram | לא | שלב שני | חלק מהדירוג | https://transparency.meta.com/features/explaining-ranking/ig-comments/ |
| נקודת מבט מודגשת | סימון ויזואלי מקדים דעות בולטות בגילוי ובנושאים חמים. | Threads | לא | שלב שני | קרוב להודעות נעוצות | https://about.fb.com/news/2025/07/introducing-messaging-highlighted-perspectives-threads/ |
| תגובות רק לעוקבים | הכותב מגביל תגובות וציטוטים לעוקבים שלו. | Threads | לא | מאוחר יותר | הפורום פתוח לכל מי שנכנס | https://about.fb.com/news/2025/03/new-threads-features-more-personalized-experience-you-control/ |
| אישור תגובות בידי הכותב | הכותב בוחר אילו תגובות יופיעו בפומבי, לכל פוסט. | Threads | לא | מאוחר יותר | הצוות מפקח, לא הכותב | https://about.fb.com/news/2025/03/new-threads-features-more-personalized-experience-you-control/ |
| סינון תגובות | סינון תגובות לאנשים שאני עוקב אחריהם או לתגובות עם אזכור. | Threads | לא | מאוחר יותר | ערך נמוך | https://about.fb.com/news/2025/03/new-threads-features-more-personalized-experience-you-control/ |
| מדריך מחירים ומחשבונים | מדריך מה צרכנים שילמו ומחשבונים, "המלצה בלבד". | מדרג, B144 | לא | מאוחר יותר | לא חלק מליבת הפורום | https://www.midrag.co.il/Content/MainPriceList ; https://www.b144.co.il/PriceList/ |

## תגובות ומוניטין

| פיצ'ר | מיקרו-פיצ'ר (מה בדיוק קורה, משפט אחד) | למי יש | יש לנו היום | החלטה | למה | מקור |
|---|---|---|---|---|---|---|
| "תודה" אחת חיובית | לחיצה אחת מסמנת שההודעה עזרה, עד 50 ביום כברירת מחדל. | Discourse, Flarum | לא | גרסה ראשונה | תגובה חיובית אחת, בלי הורדות | https://github.com/discourse/discourse/blob/main/config/site_settings.yml ; https://blog.discourse.org/2018/06/understanding-discourse-trust-levels/ ; https://github.com/flarum/framework/tree/2.x/extensions |
| סט תגובות רגשיות | כמה תגובות כמו מועיל, מזל טוב, תודה, נבחרות בלחיצה ארוכה. | Discourse, LinkedIn | לא | שלב שני | קודם "תודה" אחת | https://github.com/discourse/discourse/blob/main/plugins/discourse-reactions/config/settings.yml ; https://www.linkedin.com/help/linkedin/answer/a528190 |
| תגובה מותאמת לקהילה | מנהל משנה את סמלי התגובה, צבעים ורקעים, ולכל קהילה לייק משלה. | Facebook Groups, Threads | לא | מאוחר יותר | עיצוב, לא חיוני | https://about.fb.com/news/2021/11/new-tools-in-facebook-groups/ ; https://about.fb.com/news/2025/10/introducing-threads-communities-find-your-people/ |
| הצבעה למעלה ולמטה | ניקוד פלוס ומינוס גלוי לכל הודעה. | Lemmy, Reddit | לא | לא נבנה | הורדות פוגעות ומסוכנות בקהילה מקצועית | https://join-lemmy.org/ ; https://join-lemmy.org/docs/users/01-getting-started.html |
| הצבעה על תשובות במצב שאלות | תוסף הצבעה בסגנון שאלות ותשובות, ההתנהגות לא נבדקה. | Discourse | לא | לא נבנה | כולל הצבעה שלילית | https://github.com/discourse/discourse/tree/main/plugins (לא אומת במלואו) |
| הצבעה על נושאים | הצבעה על בקשות בסגנון "רעיון לשיפור", עם מכסת קולות לכל רמה. | Discourse | לא | מאוחר יותר | ערך נמוך לקהילה קטנה | https://github.com/discourse/discourse/blob/main/plugins/discourse-topic-voting/config/settings.yml |
| נקודות מוניטין | 10 נקודות על הצבעה, 15 על תשובה שנבחרה, תקרה של 200 ביום, ויש גם הורדות. | Stack Overflow | לא | שלב שני | נקודות בשלב שני, בלי הורדות | https://stackoverflow.com/help/whats-reputation |
| סולם הרשאות לפי ניקוד | כל פעולה נפתחת רק מניקוד מסוים, מ-1 ועד 25,000. | Stack Overflow | לא | לא נבנה | שער ניקוד שחוסם אנשים רגילים | https://stackoverflow.com/help/privileges |
| קארמה | ציון מהצבעות, וקהילות דורשות קארמה לפני כתיבה. | Reddit | לא | לא נבנה | שער ניקוד שחוסם אנשים רגילים | https://support.reddithelp.com/hc/en-us/articles/204511829-What-is-karma |
| רמות אמון אוטומטיות | אחרי קריאה וזמן באתר משתמש עולה רמה והמגבלות שלו מוסרות. | Discourse | לא | גרסה ראשונה | גרסה פשוטה של מגבלות משתמש חדש | https://github.com/discourse/discourse/blob/main/config/site_settings.yml ; https://blog.discourse.org/2018/06/understanding-discourse-trust-levels/ |
| איבוד רמת אמון | רמה 3 יורדת אם הדרישות לא נשמרות, עם שבועיים חסד. | Discourse | לא | מאוחר יותר | מורכב לקהילה קטנה | https://blog.discourse.org/2018/06/understanding-discourse-trust-levels/ |
| תגים בשלוש דרגות | ארד, כסף וזהב, למשל "שאלה טובה" מ-25 הצבעות. | Stack Overflow, Discourse | לא | שלב שני | רמות ותגים | https://stackoverflow.com/help/badges ; https://github.com/discourse/discourse/blob/main/config/site_settings.yml |
| הישגים קהילתיים | תגים כמו ותיק 3 שנים ותורם קבוע 20 יום, ולוח מובילים. | Reddit | לא | שלב שני | רמות ותגים | https://support.reddithelp.com/hc/en-us/articles/25564722077588-Community-Achievements |
| נקודות, רמות וטבלת מובילים | נקודה לכל לייק, 9 רמות, טבלת 10 מובילים לשבוע, לחודש ולתמיד. | Circle, Discourse | לא | שלב שני | נקודות ורמות | https://help.circle.so/p/audience/gamification/get-to-know-gamification ; https://github.com/discourse/discourse/blob/main/plugins/discourse-gamification/config/settings.yml |
| מעמד אלוף קהילה | מעמד "אלוף קהילה" ניתן ליותר אנשים. | Threads | לא | שלב שני | קרוב לרמות ותגים | https://about.fb.com/news/2026/06/meta-launching-new-features-500-million-monthly-threads-users/ |
| פרס על שאלה | 50 עד 500 נקודות לתשובה, לשבעה ימים, בלי החזר. | Stack Overflow | לא | מאוחר יותר | קרוב לפרסים ולכסף | https://stackoverflow.com/help/bounty |
| פרסים בין חברים | חברים נותנים פרס כמו "מעמיק" שמקדם את הפוסט. | Facebook Groups | לא | מאוחר יותר | פרסים | https://about.fb.com/news/2021/11/new-tools-in-facebook-groups/ |
| פרס שנתי | פעם בשנה שכנים בוחרים עסקים אהובים ומקבלים רשימה לכל שכונה. | Nextdoor | לא | מאוחר יותר | פרסים | https://business.nextdoor.com/en-us/small-business/faves |
| תווית תפקיד ליד השם | תווית כמו "מתווך מורשה" או "מומחה" ליד השם בכל הודעה. | Reddit, Facebook Groups | חלקי: תפקיד ועיר בכרטיס | גרסה ראשונה | תוויות תפקיד ליד השמות | https://support.reddithelp.com/hc/en-us/articles/15484503095060-User-Flair ; https://about.fb.com/news/2021/07/new-ways-to-elevate-experts-in-facebook-groups/ |
| סימן מאומת | סימן שמאשר זהות בחינם, בלי השפעה על הדירוג. | Reddit, LinkedIn | חלקי: תג רישיון למתווכים ולקבלנים | גרסה ראשונה | סימן איש מקצוע מאומת | https://support.reddithelp.com/hc/en-us/articles/42763717293716-Verified-profiles-on-Reddit ; https://www.linkedin.com/help/linkedin/answer/a1359065 |
| בדיקה מול פנקס רשמי | מספר רישיון נבדק מול מאגר פתוח: 25,375 מתווכים, 3,198 שמאים, 24,742 שורות קבלנים, ולינקדאין לא בודקת רישיון. | data.gov.il, חסר ב-LinkedIn | חלקי: מתווכים נבדקים מול הפנקס בהצטרפות | גרסה ראשונה | סימן מאומת מפנקסי הרישוי | https://data.gov.il/api/3/action/datastore_search?resource_id=a0f56034-88db-4132-8803-854bcdb01ca1 ; https://data.gov.il/api/3/action/package_search?q=שמאי ; https://data.gov.il/api/3/action/package_search?q=קבלנים ; https://www.linkedin.com/help/linkedin/answer/a1359065 |
| תג בלי פרטי המסמך | התג יכול להראות מדינה מנפיקה אבל אף פעם לא את פרטי המסמך. | LinkedIn | לא | גרסה ראשונה | חלק מסימן המאומת | https://www.linkedin.com/help/linkedin/answer/a1631613 |
| "על הפרופיל הזה" | חלון שמראה מתי נוצר הפרופיל, מתי עודכן והאם טלפון ומייל אומתו. | LinkedIn | לא | גרסה ראשונה | מחזק את סימן המאומת, נגד הונאות | https://www.linkedin.com/blog/member/trust-and-safety/new-linkedin-profile-features-help-verify-identity-detect-remove-fake-accounts-boost-authenticity |
| אימות מקום עבודה במייל | קוד נשלח למייל בדומיין של החברה. | LinkedIn | לא | מאוחר יותר | הפנקס הרשמי חזק יותר | https://www.linkedin.com/help/linkedin/answer/a1359065 |
| אימות זהות בצילום תעודה | צילום תעודה, סריקת שבב וסלפי דרך ספק חיצוני. | LinkedIn | לא | מאוחר יותר | יקר, הפנקס זול יותר | https://www.linkedin.com/help/linkedin/answer/a1631613 |
| אימות עורכי דין ויועצי משכנתאות | לא נמצא מאגר פתוח לעורכי דין ויועצי משכנתאות, ומאגר האסבסט לא נבדק. | לשכת עורכי הדין (חסום), data.gov.il | לא | מאוחר יותר | אין היום מקור לבדיקה | https://www.israelbar.org.il/ (לא אומת במלואו) |
| תג מאומת בחבילה בתשלום | חבילה עסקית כוללת תג מאומת והגנה מהתחזות. | Facebook, Instagram, WhatsApp | לא | מאוחר יותר | פיצ'ר כסף | https://about.fb.com/news/2026/09/introducing-meta-one-subscription-service-more-features-ai/ |
| הערות קהילה | הערה מוצגת רק כשמדרגים שבדרך כלל חלוקים מסכימים, והנתונים פתוחים. | X | לא | מאוחר יותר | דורש הרבה מדרגים | https://github.com/twitter/communitynotes/blob/main/documentation/under-the-hood/ranking-notes.md ; https://github.com/twitter/communitynotes |
| בקשת המלצה | בוחרים קשר, מציינים את הקשר ביניכם ואת התפקיד אז, והקשר נעול אחרי השליחה ורק בשפה הראשית של הפרופיל. | LinkedIn | חלקי: המלצות עמיתים מאחורי מתג | שלב שני | המלצות בין אנשי מקצוע | https://www.linkedin.com/help/linkedin/answer/a546682 |
| כתיבת המלצה | ממליצים רק על קשר ישיר, וההמלצה מופיעה אצל המקבל ואצל הכותב. | LinkedIn | חלקי: המלצות עמיתים מאחורי מתג | שלב שני | המלצות בין אנשי מקצוע | https://www.linkedin.com/help/linkedin/answer/a543723 |
| המקבל שולט בתצוגה | המקבל מחליט אם להציג המלצה, וכל צד יכול להסתיר אותה. | LinkedIn | כן: המקבל מסתיר המלצה | שלב שני | המלצות בין אנשי מקצוע | https://www.linkedin.com/help/linkedin/answer/a543723 |
| מדור המלצות רק כשיש | מדור ההמלצות מופיע רק אחרי ההמלצה הראשונה. | LinkedIn | לא | שלב שני | חלק מההמלצות | https://www.linkedin.com/help/linkedin/answer/a546682 |
| המלצות שלא נקנות | כל המלצה מגיעה מלקוח מאומת, הדף חינם ואי אפשר לקנות המלצות. | Nextdoor | לא | שלב שני | המלצות חיוביות בלבד, בלי קנייה | https://business.nextdoor.com/en-us/small-business/faves |
| קישור "המליצו עליי" | בעל עסק שולח קישור ללקוחות כדי לאסוף המלצות. | Nextdoor | לא | שלב שני | חלק מההמלצות | https://business.nextdoor.com/en-us/small-business/faves |
| מעקב לעומת המלצה | סימון עסק כמועדף הוא בעיקר מעקב, והמלצה כתובה היא פעולה נפרדת. | Nextdoor | לא | שלב שני | מעקב והמלצה בשלב שני | https://help.nextdoor.com/s/article/About-Recommendations?language=en_US (לא אומת במלואו) |
| המלצה בתוך פוסט | שכן ממליץ על עסק בתיוג שלו בפוסט. | Nextdoor | לא | שלב שני | אזכורים בשלב שני | https://help.nextdoor.com/s/article/About-Recommendations?language=en_US (לא אומת במלואו) |
| עריכה ומחיקה של המלצה | הכותב עורך או מוחק המלצה מתפריט שלוש נקודות. | Nextdoor | לא | שלב שני | חלק מההמלצות | https://help.nextdoor.com/s/article/About-Recommendations?language=en_US (לא אומת במלואו) |
| הזמנה לכתוב ביקורת | אחרי העבודה איש המקצוע מזמין את הלקוח לכתוב ביקורת. | LinkedIn | לא | לא נבנה | ביקורות קהל בשלב הזה לא | https://www.linkedin.com/help/linkedin/answer/a550345 |
| סינון אנשי מקצוע לפי ביקורות | 15 חשבוניות, שיחות ללקוחות, ציון מעל 9, הסרה אוטומטית וחסימה על דירוג שלילי. | מדרג | לא | לא נבנה | דירוג קהל וסיכון לשון הרע | https://biz.midrag.co.il/Content/Article/14450 ; https://www.midrag.co.il/Content/Article/17281 ; https://www.midrag.co.il/Content/Article/10461 |
| ביקורות גולשים מזוהות | ביקורת אחת לחשבון, זיהוי בגוגל או קוד לנייד, בדיקה אוטומטית, ושם מלא, ראשי תיבות או אנונימי. | B144, מדרג | חלקי: כוכבים רק כשמאומת | לא נבנה | כוכבים וביקורות קהל לא בשלב הזה | https://www.b144.co.il/MarketingReviews/ ; https://www.midrag.co.il/Content/Article/10461 |
| תגובת בעל העסק לביקורת | בעל העסק לא מסיר ביקורת אלא רק מגיב עליה בפומבי, ושתי הגרסאות נשמרות. | B144, מדרג | לא | לא נבנה | תלוי בביקורות שלא נבנות | https://www.b144.co.il/MarketingReviews/ ; https://www.midrag.co.il/Content/Article/17281 |
| דירוג לפי ביקורות בלי תשלום | הדירוג לפי ציונים בלבד, ואין קידום בתשלום. | מדרג | לא | לא נבנה | דירוג לפי כוכבים לא עכשיו, ודירוג בתשלום אף פעם | https://www.midrag.co.il/Content/Article/17281 |

## מבנה וקטגוריות

| פיצ'ר | מיקרו-פיצ'ר (מה בדיוק קורה, משפט אחד) | למי יש | יש לנו היום | החלטה | למה | מקור |
|---|---|---|---|---|---|---|
| קטגוריה חובה | אי אפשר לפתוח דיון בלי קטגוריה. | Discourse | חלקי: 34 מקצועות בחמש קבוצות | גרסה ראשונה | קטגוריות לפי מקצוע ונושא | https://github.com/discourse/discourse/blob/main/config/site_settings.yml |
| מדריך לפי מקצוע ועיר | גלישה באנשי מקצוע לפי תחום (במדרג 150) ולפי עיר. | מדרג, B144, Houzz, יד2 | כן: מדריך עם סינון מקצוע ועיר | גרסה ראשונה | הפורום נשען על הקטגוריות האלה | https://www.midrag.co.il/ ; https://www.b144.co.il/ ; https://www.houzz.com/ ; https://www.yad2.co.il/ (לא אומת במלואו) |
| תגיות ותוויות לדיון | תגיות ותוויות לדיון, עד 20 תגיות בפורום ו-5 בדיון, וחלקן רק לצוות. | Flarum, Discord, Discourse, Reddit | לא | שלב שני | תגיות בשלב שני | https://github.com/flarum/framework/tree/2.x/extensions ; https://raw.githubusercontent.com/discord/discord-api-docs/main/developers/resources/channel.mdx ; https://support.reddithelp.com/hc/en-us/articles/15484545678996-Post-Flair |
| הנחיות כתיבה בכל פורום | כל פורום מציג הנחיות בזמן פתיחת דיון. | Discord | לא | גרסה ראשונה | חוקי קהילה | https://support.discord.com/hc/en-us/articles/6208479917079-Forum-Channels-FAQ |
| סינון "נפתר" | אפשר להפעיל "נפתר" לפי קטגוריה ולסנן דיונים שנפתרו. | Discourse | לא | גרסה ראשונה | חלק מסימון התשובה שעזרה | https://github.com/discourse/discourse/blob/main/plugins/discourse-solved/config/settings.yml |
| הקצאת דיון לאדם | דיון מוקצה לאדם עם מצב חדש, בטיפול, הושלם. | Discourse | לא | מאוחר יותר | כלי עבודה פנימי, ערך נמוך | https://github.com/discourse/discourse/blob/main/plugins/discourse-assign/config/settings.yml |
| קבוצות והרשאות | קבוצות עם גישה לפי קטגוריה וקבוצות שמנהלות את עצמן. | Discourse, Flarum | לא | מאוחר יותר | קבוצות עם מנהלים משלהן | https://www.discourse.org/features ; https://flarum.org/ |
| כרטיס משתמש בלחיצה | לחיצה על שם מציגה כרטיס קטן עם רמה ופרטים. | Discourse, Circle | לא | שלב שני | כרטיס פרופיל בלחיצה | https://github.com/discourse/discourse/tree/main/plugins/discourse-gamification ; https://help.circle.so/p/audience/gamification/get-to-know-gamification |
| סטטוס משתמש | משתמש קובע סטטוס, כבוי כברירת מחדל. | Discourse | לא | מאוחר יותר | ערך נמוך | https://github.com/discourse/discourse/blob/main/config/site_settings.yml |
| קישור מוצג לדיון | לדיון אפשר לצרף קישור חיצוני בולט. | Discourse | לא | שלב שני | קרוב לתצוגת קישורים | https://github.com/discourse/discourse/blob/main/config/site_settings.yml |
| אירועים ויומן | תוסף אירועים ומרחבי אירועים, ומפגשים חוזרים בקבוצות. | Discourse, Circle, Facebook Groups | לא | שלב שני | אירועים | https://github.com/discourse/discourse/tree/main/plugins ; https://help.circle.so/ ; https://about.fb.com/news/2021/11/new-tools-in-facebook-groups/ |
| מפגש שאלות ותשובות | מארח עונה בזמן אמת, והשאלות שנענו מוצגות בערימה להחלקה. | Facebook Groups | לא | שלב שני | שאלות ותשובות שבועיות עם מומחה | https://about.fb.com/news/2021/07/new-ways-to-elevate-experts-in-facebook-groups/ |
| איתור מומחים לפי נושא | מנהלים חיפשו אנשים לפי נושא והזמינו אותם כמומחים (ניסוי). | Facebook Groups | לא | מאוחר יותר | ערך בינוני, עבודת צוות | https://about.fb.com/news/2021/07/new-ways-to-elevate-experts-in-facebook-groups/ |
| קהילות ומרחבים | קהילות שנרשמים אליהן, או מרחבי פוסטים, תמונות וצ'אט. | Lemmy, Circle | לא | מאוחר יותר | מרחבים | https://join-lemmy.org/docs/users/01-getting-started.html ; https://help.circle.so/ |
| תתי קבוצות | מנהלים פותחים תתי קבוצות לפי נושא או אזור (ניסוי). | Facebook Groups | לא | מאוחר יותר | קבוצות עם מנהלים משלהן | https://about.fb.com/news/2021/11/new-tools-in-facebook-groups/ |
| נושא שגדל לקהילה | קהילה נבנית על תגית, ומד מראה כמה קרוב הנושא להפוך לקהילה. | Threads | לא | מאוחר יותר | מרחבים | https://about.fb.com/news/2026/06/meta-launching-new-features-500-million-monthly-threads-users/ |
| מרכז קהילות | מרכז קהילות בתפריט וסמל לכל קהילה. | Threads | לא | מאוחר יותר | מרחבים | https://about.fb.com/news/2026/06/meta-launching-new-features-500-million-monthly-threads-users/ |
| הצטרפות מתגית | כפתור "הצטרף" על תגית, והקהילות מופיעות בפרופיל. | Threads | לא | מאוחר יותר | מרחבים | https://about.fb.com/news/2025/10/introducing-threads-communities-find-your-people/ |
| ערכות פיצ'רים בלחיצה | חבילות של סוגי פוסטים, תגים וכלי ניהול מופעלות בלחיצה. | Facebook Groups | לא | מאוחר יותר | שייך לקבוצות עם מנהלים | https://about.fb.com/news/2021/11/new-tools-in-facebook-groups/ |
| תובנות לפי שלב הקהילה | תובנות למנהל לפי קבוצה חדשה, צומחת או ותיקה. | Facebook Groups | לא | מאוחר יותר | שייך לקבוצות עם מנהלים | https://about.fb.com/news/2026/10/new-tools-for-the-admins-who-build-communities-on-forum/ |
| קוד QR | קוד QR שסורקים ומגיעים לדף ההצטרפות. | Facebook Groups | לא | שלב שני | QR לכרטיס | https://about.fb.com/news/2022/03/new-tools-for-facebook-group-admins/ |

## פרופיל איש מקצוע

| פיצ'ר | מיקרו-פיצ'ר (מה בדיוק קורה, משפט אחד) | למי יש | יש לנו היום | החלטה | למה | מקור |
|---|---|---|---|---|---|---|
| פרופיל ציבורי לגוגל | הפרופיל גלוי למי שלא נכנס ומופיע במנועי חיפוש, ושינויים מגיעים לגוגל לאט. | LinkedIn | כן: כרטיס ציבורי בכתובת קבועה | גרסה ראשונה | נתונים מובנים לפרופילים | https://www.linkedin.com/help/linkedin/answer/a518980 |
| כל אזכור מגיע לכרטיס | המלצות ופוסטים שמתייגים את העסק מוצגים בלשונית בדף העסק. | Nextdoor | לא | גרסה ראשונה | חלון הפורום בתוך הכרטיס | https://help.nextdoor.com/s/article/About-Recommendations?language=en_US (לא אומת במלואו) |
| הסתרה או הסרה של הכרטיס | איש מקצוע מבקש להסיר את כל הפרופיל, ובמדרג זה בכתב תוך 10 ימי עסקים. | מדרג | לא | גרסה ראשונה | הסתרה או הסרה בלחיצה אחת | https://www.midrag.co.il/Content/Article/10461 |
| שדות פרופיל מותאמים | שדות כמו מספר רישיון, אזור והתמחות. | Circle | כן: רישיון, אזורים והתמחות בכרטיס | גרסה ראשונה | קיים, חלון הפורום נשען עליו | https://help.circle.so/ |
| כפתור פעולה אישי | כפתור אחד כמו "קביעת פגישה" או "אתר" שמקשר לכתובת של איש המקצוע. | LinkedIn | חלקי: ישיר רק למתווכים | גרסה ראשונה | כפתורי פנייה שמגיעים לאיש המקצוע | https://www.linkedin.com/help/linkedin/answer/a1484520 |
| הכפתור עוקב אחרי השם | הכפתור האישי מופיע גם בפוסטים, בהודעות ובחיפוש, פעיל כברירת מחדל. | LinkedIn | לא | שלב שני | אחרי שהכפתור בכרטיס עובד | https://www.linkedin.com/help/linkedin/answer/a1484520 |
| כישורים | עד 100 כישורים, והמדור מוסתר כשהוא ריק. | LinkedIn | כן: שבבי התמחות, שפות ואזורים | שלב שני | תגיות בשלב שני | https://www.linkedin.com/help/linkedin/answer/a549047 |
| הצעות כישורים | חלון ההוספה מציע כישורים ומאפשר לעקוב אחריהם. | LinkedIn | לא | שלב שני | רשימה קבועה כמו תגיות | https://www.linkedin.com/help/linkedin/answer/a549047 |
| נושאים בביוגרפיה | עד עשרה נושאים בביוגרפיה, ולחיצה פותחת את השיחות עליהם. | Threads | לא | שלב שני | תגיות בשלב שני | https://about.fb.com/news/2025/03/new-threads-features-more-personalized-experience-you-control/ |
| תיק עבודות מוצמד | איש המקצוע נועץ פוסטים, תמונות וקישורים בראש הפרופיל, ובלינקדאין הם לא בחיפוש ודורשים כניסה. | LinkedIn | לא | שלב שני | קרוב להודעות נעוצות | https://www.linkedin.com/help/linkedin/answer/a552452/featured-section-on-your-profile-faqs |
| דף שירותים | רשימת שירותים, אזור עבודה, עבודה מרחוק ומחיר התחלתי או "צרו קשר". | LinkedIn | חלקי: אזורי פעילות והתמחויות | שלב שני | קיים בחלקו, משלימים אחרי הפורום | https://www.linkedin.com/help/linkedin/answer/a564491 |
| מחיר כהערכה | המחיר ההתחלתי מוצג כהערכה ולא כמחיר סופי. | LinkedIn | לא | שלב שני | חלק מדף השירותים | https://www.linkedin.com/help/linkedin/answer/a564491 |
| מדיה ובקשה בשירותים בתשלום | תמונות, ביקורת וכפתור "בקשת שירות" רק במנוי בתשלום. | LinkedIn | לא | מאוחר יותר | פיצ'ר כסף | https://www.linkedin.com/help/linkedin/answer/a564491 |
| תג "עונה תוך יום" | זמן תגובה ממוצע ל-180 יום כשעונים תוך 24 שעות, ואחוז מענה מ-80%. | LinkedIn | חלקי: שדה זמן תגובה | שלב שני | תג "עונה תוך יום" | https://www.linkedin.com/help/linkedin/answer/a550345 |
| מי צפה בכרטיס | בחינם רואים את 3 הצופים האחרונים מ-90 יום. | LinkedIn | חלקי: צפיות נספרות ולא מוצגות | שלב שני | סטטיסטיקה שבועית לאיש המקצוע | https://www.linkedin.com/help/linkedin/answer/a548046 |
| רשימת צופים בתשלום | במנוי רואים את כל הצופים עד 365 יום. | LinkedIn | לא | מאוחר יותר | פיצ'ר כסף | https://www.linkedin.com/help/linkedin/answer/a548046 |
| תוספות פרופיל בתשלום | עד 5 תמונות שער, הצעות פרופיל בבינה מלאכותית ומיקום בולט. | LinkedIn | לא | מאוחר יותר | פיצ'ר כסף | https://premium.linkedin.com/small-business/business |
| מסגרת "פנוי לעבודה" | מסגרת על התמונה, לכולם או רק למגייסים. | LinkedIn | לא | מאוחר יותר | ערך בינוני | https://www.linkedin.com/help/linkedin/answer/a566495 (לא אומת במלואו) |
| חמישה קישורים עם מונה | עד חמישה קישורים בביוגרפיה, ובעל הפרופיל רואה כמה לחצו על כל אחד. | Threads | חלקי: קישורי רשתות ואתר | שלב שני | חלק מהסטטיסטיקה לאיש המקצוע | https://about.fb.com/news/2025/03/new-threads-features-more-personalized-experience-you-control/ |

## פנייה ישירה והודעות

| פיצ'ר | מיקרו-פיצ'ר (מה בדיוק קורה, משפט אחד) | למי יש | יש לנו היום | החלטה | למה | מקור |
|---|---|---|---|---|---|---|
| פנייה חופשית בלי חיבור | לקוח פונה לאיש המקצוע בחינם בלי להיות מחובר אליו, והתשלום מחוץ לאתר. | LinkedIn | חלקי: ישיר רק למתווכים | גרסה ראשונה | כפתורי פנייה שמגיעים לאיש המקצוע עצמו | https://www.linkedin.com/help/linkedin/answer/a564491 ; https://www.linkedin.com/help/linkedin/answer/a550345 |
| בקשת הצעת מחיר | לקוח שולח בקשה מדף השירות, ואיש המקצוע עונה "שלח הצעה" או "לא תודה". | LinkedIn | חלקי: בקשת הצעה מגיעה לבעל האתר | גרסה ראשונה | הבקשה צריכה להגיע לאיש המקצוע עצמו | https://www.linkedin.com/help/linkedin/answer/a570605 |
| "דברו איתי" דרך האתר | האתר מבקש קודם את טלפון הפונה, ואיש המקצוע רואה רק חלק מהמספר. | מדרג | לא | לא נבנה | חלק ממודל עמלה, אצלנו הפנייה ישירה | https://www.midrag.co.il/Content/Article/17281 ; https://biz.midrag.co.il/Content/Article/14483 |
| הזמנת חיבור עם הערה | הזמנה אישית עם הערה של 200 תווים, 5 בחינם. | LinkedIn | לא | שלב שני | קרוב למעקב אחרי אדם | https://www.linkedin.com/help/linkedin/answer/a6239760 |
| הודעות פרטיות | הודעות פרטיות מרמת אמון 1, עד 20 ביום. | Discourse, Flarum, Lemmy, Reddit | לא | מאוחר יותר | הודעות פרטיות | https://github.com/discourse/discourse/blob/main/config/site_settings.yml ; https://flarum.org/ |
| צ'אט באתר | ערוצי צ'אט ליד הדיונים, ואפשר לצטט מהצ'אט לדיון. | Discourse, Discord | לא | מאוחר יותר | צ'אט בתוך האתר | https://www.discourse.org/features |
| הודעות רק לקשרים | חשבון חינם שולח הודעות רק לקשרים קיימים. | LinkedIn | לא | מאוחר יותר | הודעות פרטיות | https://www.linkedin.com/help/linkedin/answer/a6239760 |
| בקשות הודעה ממי שלא עוקב | הודעה ממי שלא עוקב נכנסת לבקשות בלי קישורים ומדיה, עם מכסה לשולח. | Threads | לא | מאוחר יותר | הודעות פרטיות | https://about.fb.com/news/2025/07/introducing-messaging-highlighted-perspectives-threads/ |
| תיקיית ספאם נסתרת | תיקייה נסתרת תופסת הודעות מזיקות. | Threads | לא | מאוחר יותר | הודעות פרטיות | https://about.fb.com/news/2025/07/introducing-messaging-highlighted-perspectives-threads/ |
| רק ממי שאני עוקב | המשתמש חוסם בקשות ממי שהוא לא עוקב אחריו. | Threads | לא | מאוחר יותר | הודעות פרטיות | https://about.fb.com/news/2025/07/introducing-messaging-highlighted-perspectives-threads/ |
| צ'אט קבוצתי | צ'אט של עד 50 עוקבים עם שם. | Threads | לא | מאוחר יותר | צ'אט בתוך האתר | https://about.fb.com/news/2025/07/introducing-messaging-highlighted-perspectives-threads/ |
| אזהרת הונאה בהודעה | הודעה שמבקשת לעבור לפלטפורמה אחרת מקבלת אזהרה ואפשר לדווח בשקט. | LinkedIn | לא | מאוחר יותר | שייך להודעות פרטיות | https://www.linkedin.com/blog/member/trust-and-safety/new-linkedin-profile-features-help-verify-identity-detect-remove-fake-accounts-boost-authenticity |
| הודעות בתשלום | קרדיטים חודשיים לפנייה קרה, 5 עד 50, פגים אחרי 90 יום. | LinkedIn | לא | מאוחר יותר | פיצ'ר כסף | https://www.linkedin.com/help/linkedin/answer/a554514 |
| החזר קרדיט | הקרדיט חוזר כשהנמען מקבל את ההודעה. | LinkedIn | לא | מאוחר יותר | פיצ'ר כסף | https://www.linkedin.com/help/linkedin/answer/a554514 |
| כיבוי הודעות בתשלום | הנמען יכול לכבות קבלת הודעות בתשלום. | LinkedIn | לא | מאוחר יותר | שייך להודעות פרטיות | https://www.linkedin.com/help/linkedin/answer/a6239760 |
| שליחה לעוד ספקים | במנוי אפשר להעביר את הבקשה לעוד אנשי מקצוע רלוונטיים. | LinkedIn | לא | מאוחר יותר | פיצ'ר כסף | https://www.linkedin.com/help/linkedin/answer/a550345 |
| טופס לידים במודעה | מודעה עם טופס מיידי, והלידים יוצאים כקובץ. | Facebook, Instagram | לא | מאוחר יותר | פיצ'ר כסף | https://www.facebook.com/business/help/397336587121938 (לא אומת במלואו) |
| אנשי מקצוע של שותף | בחלק מהתחומים מוצגים אנשי מקצוע מאתר שותף. | Nextdoor | לא | מאוחר יותר | שותפויות בהמשך | https://help.nextdoor.com/s/article/About-Recommendations?language=en_US (לא אומת במלואו) |

## פיד

| פיצ'ר | מיקרו-פיצ'ר (מה בדיוק קורה, משפט אחד) | למי יש | יש לנו היום | החלטה | למה | מקור |
|---|---|---|---|---|---|---|
| משקל לשיחה שהכותב עונה בה | תשובה שהכותב מגיב עליה שווה 75 לעומת 0.5 ללייק, ודיווח שווה מינוס 369. | X | לא | שלב שני | דירוג פיד, כולל משקל למענה חוזר | https://github.com/twitter/the-algorithm-ml/blob/main/projects/home/recap/README.md |
| זמן שהייה | הזמן נספר כשלפחות חצי עדכון נראה בגלילה, וגם אחרי לחיצה. | LinkedIn | לא | שלב שני | דירוג פיד | https://www.linkedin.com/blog/engineering/feed/understanding-feed-dwell-time |
| ענישת דילוג | מודל מנבא אם יגללו מהר הלאה ומוריד את הציון. | LinkedIn | לא | מאוחר יותר | מודל כבד לאתר קטן | https://www.linkedin.com/blog/engineering/feed/understanding-feed-dwell-time |
| נוסחת משקלים | ציון שמשלב לחיצות, תגובות, שיתופים וערך לכותב. | LinkedIn | לא | שלב שני | דירוג פיד | https://www.linkedin.com/blog/engineering/feed/understanding-feed-dwell-time |
| שלבי מנגנון הדירוג | איסוף מועמדים, נתונים, ציון, סינון, ערבוב והגשה. | X | לא | שלב שני | דירוג פיד | https://github.com/twitter/the-algorithm/blob/main/home-mixer/README.md |
| גיוון כותבים | לא שני פוסטים ברצף מאותו כותב או צליל, ובלי מה שכבר נראה. | X, TikTok | לא | שלב שני | דירוג פיד | https://github.com/twitter/the-algorithm/blob/main/home-mixer/README.md ; https://newsroom.tiktok.com/en-us/how-tiktok-recommends-videos-for-you |
| חצי ממי שעוקבים | כחצי מהפיד מגיע מחשבונות שהמשתמש עוקב אחריהם. | X | לא | שלב שני | מעקב ודירוג פיד | https://github.com/twitter/the-algorithm |
| גיוון סוגי פוסטים | כ-500 פוסטים בכל סבב, ולא כמה סרטונים ברצף. | Facebook | לא | שלב שני | דירוג פיד | https://transparency.meta.com/features/explaining-ranking/fb-feed/ |
| ניבוי בפיד קבוצות | ניבוי הצבעה, תגובה, זמן צפייה והצטרפות אחרי צפייה, לכ-200 פוסטים. | Facebook Groups | לא | שלב שני | דירוג פיד | https://transparency.meta.com/features/explaining-ranking/fb-groups-feed/ |
| אותות פיד באינסטגרם | פעילות הצופה, פופולריות, זמן והיסטוריה עם הכותב. | Instagram | לא | שלב שני | דירוג פיד | https://about.instagram.com/blog/announcements/instagram-ranking-explained |
| ניקוי לפני דירוג | פוסט שמפר כללים יוצא עוד לפני הדירוג. | Facebook | לא | שלב שני | חלק מדירוג הפיד | https://transparency.meta.com/features/explaining-ranking/fb-feed/ |
| סינון חסומים ומושתקים | סינון והורדה בדירוג של מה שנחסם, הושתק או לא מתאים. | X | לא | שלב שני | חלק מדירוג הפיד | https://github.com/twitter/the-algorithm |
| לשונית "עוקב" לפי זמן | לשונית שמראה רק את מי שעוקבים אחריו, מהחדש לישן. | Facebook | לא | שלב שני | מעקב אחרי אדם | https://transparency.meta.com/features/explaining-ranking/fb-feed/ |
| מועדפים | חשבונות נבחרים מופיעים ראשונים. | Facebook | לא | שלב שני | מעקב אחרי אדם | https://transparency.meta.com/features/explaining-ranking/fb-feed/ |
| השהיה | השהיית אדם או קבוצה ל-30 יום. | Facebook | לא | שלב שני | שליטה בפיד | https://transparency.meta.com/features/explaining-ranking/fb-groups-feed/ |
| הסתרה ו"לא מעניין" | הסתרת פוסט ומשוב "מעניין" או "לא מעניין" משנים את הדירוג. | Facebook | לא | שלב שני | שליטה בפיד | https://transparency.meta.com/features/explaining-ranking/fb-feed/ |
| כיוון האלגוריתם לימים | בקשה ליותר או פחות מנושא ליום, שלושה או שבעה. | Threads | לא | מאוחר יותר | ערך נמוך בהתחלה | https://about.fb.com/news/2026/06/meta-launching-new-features-500-million-monthly-threads-users/ |
| פיד מותאם כברירת מחדל | פיד אישי כמו "האזור שלי והמקצוע שלי" נפתח ראשון. | Threads | לא | שלב שני | מעקב אחרי נושא | https://about.fb.com/news/2025/03/new-threads-features-more-personalized-experience-you-control/ |
| גילוי ממי שלא עוקבים | רוב הפיד מגיע ממי שלא עוקבים אחריו, כך שגם חדש מגיע לאנשים. | Instagram | לא | שלב שני | דירוג פיד | https://about.instagram.com/blog/announcements/instagram-ranking-explained |
| המלצה בין מקומות | פוסט מומלץ גם במקומות אחרים, ונתונים מראים מאיפה הגיעו. | Threads | לא | שלב שני | דיונים יופיעו בדפי פרויקטים ומאמרים | https://about.fb.com/news/2025/03/new-threads-features-more-personalized-experience-you-control/ |
| הצטרפות אחרי צפייה | הפיד מנבא מי יצטרף אחרי שראה פוסט מוצע. | Facebook Groups | לא | שלב שני | דירוג פיד | https://transparency.meta.com/features/explaining-ranking/fb-groups-feed/ |
| מומחים מזמינים עוקבים | מומחה מזמין עוקבים פעילים לקבוצה שפתח. | Facebook Groups | לא | מאוחר יותר | קבוצות עם מנהלים משלהן | https://about.fb.com/news/2021/07/new-ways-to-elevate-experts-in-facebook-groups/ |
| מרכז המומלצים באזור | מרכז שמראה עסקים רק לפי המלצות שכנים מאומתים. | Nextdoor | לא | שלב שני | המלצות בין אנשי מקצוע | https://blog.nextdoor.com/small-business-improvements |
| סיכום ידע בבינה מלאכותית | חיפוש שמסכם מידע על עסק מהמלצות שכנים. | Nextdoor | לא | מאוחר יותר | בינה מלאכותית | https://blog.nextdoor.com/small-business-improvements |
| ניוזלטר של חבר | כל חבר פותח ניוזלטר, והמנויים מקבלים כל גיליון פעם אחת. | LinkedIn | לא | מאוחר יותר | ניוזלטרים של חברים | https://www.linkedin.com/help/linkedin/answer/a517914 |
| הזמנה אוטומטית לניוזלטר | מי שעוקב אחרי כותב מוזמן לבד להירשם לניוזלטר שלו. | LinkedIn | לא | מאוחר יותר | ניוזלטרים של חברים | https://www.linkedin.com/help/linkedin/answer/a517914 |
| כפתור הרשמה בחמישה מקומות | כפתור הרשמה בהתראות, בפיד, במאמר, בדף הניוזלטר ובהצעות. | LinkedIn | לא | מאוחר יותר | ניוזלטרים של חברים | https://www.linkedin.com/help/linkedin/answer/a517914 |

## סרטונים קצרים

| פיצ'ר | מיקרו-פיצ'ר (מה בדיוק קורה, משפט אחד) | למי יש | יש לנו היום | החלטה | למה | מקור |
|---|---|---|---|---|---|---|
| אורך וצורה | סרטון קצר עומד או ריבועי עד 3 דקות. | YouTube | חלקי: סרטון בכרטיס | שלב שני | העלאת סרטון קצר | https://support.google.com/youtube/answer/15424877?hl=en |
| מענה בסרטון לתגובה | לוחצים "השב", מצלמים, התגובה מוצמדת כמדבקה והסרטון מופיע גם כתוכן חדש. | YouTube, TikTok | לא | שלב שני | תשובות בסרטון | https://support.google.com/youtube/answer/12816427?hl=en-GB ; https://newsroom.tiktok.com/en-us/product-tutorial-reply-to-comments-with-video |
| כתוביות אוטומטיות | כתוביות נוצרות לבד, היוצר מתקן, והצופה יכול לכבות. | TikTok | לא | שלב שני | סרטונים עם כתוביות | https://newsroom.tiktok.com/en-us/introducing-auto-captions |
| קישור מסרטון לכרטיס | סרטון מקשר לסרטון אחר של הערוץ, מוצג מתחת לשם. | YouTube | לא | שלב שני | כל סרטון מוביל לכרטיס | https://support.google.com/youtube/answer/14075157?hl=en |
| תמונת שער | פריים מהסרטון או תמונה מותאמת משמשים כשער. | YouTube | לא | שלב שני | חלק מהעלאת סרטון | https://support.google.com/youtube/answer/72431?hl=en (לא אומת במלואו) |
| העלאה בכמות | עד 15 סרטונים בבת אחת מהמחשב. | YouTube | לא | מאוחר יותר | ערך נמוך | https://support.google.com/youtube/answer/12779649?hl=en&co=GENIE.Platform%3DDesktop |
| פרטיות לפי גיל | העלאה פרטית לבני 13 עד 17 וציבורית לבוגרים. | YouTube | לא | מאוחר יותר | המשתמשים בוגרים | https://support.google.com/youtube/answer/12779649?hl=en&co=GENIE.Platform%3DDesktop |
| חסימת זכויות יוצרים | סרטון מעל דקה עם תביעת זכויות נחסם עד שזה נפתר. | YouTube | לא | שלב שני | אזהרה בהעלאת סרטון | https://support.google.com/youtube/answer/15424877?hl=en |
| מגבלת מוזיקה | שירים מהספרייה עד 90 שניות בסרטון. | YouTube | לא | מאוחר יותר | ערך נמוך | https://support.google.com/youtube/answer/15424877?hl=en |
| אותות דירוג סרטונים | כמה בחרו לצפות, משך צפייה ממוצע ואחוז שנצפה. | YouTube | לא | שלב שני | דירוג פיד | https://support.google.com/youtube/answer/11914225?hl=en&co=YOUTUBE._YTVideoType%3Dshorts |
| קצר לא פוגע בארוך | ביצועי סרטון קצר לא מזיקים להמלצות על סרטונים ארוכים. | YouTube | לא | שלב שני | חלק מדירוג הסרטונים | https://support.google.com/youtube/answer/11914225?hl=en&co=YOUTUBE._YTVideoType%3Dshorts |
| אותות ריילס | ניבוי צפייה מתחת ל-3 שניות, צפייה מלאה, שיתוף ומעקב, וגם אם הקול פתוח. | Instagram | לא | שלב שני | דירוג פיד | https://transparency.meta.com/features/explaining-ranking/ig-reels-chaining/ |
| שליטת צופה | לשונית עוקבים, דיווח, שמירה, "לא מעניין" ושיתוף להודעות. | Instagram | לא | שלב שני | שמירה ושיתוף | https://transparency.meta.com/features/explaining-ranking/ig-reels-chaining/ |
| הורדת סרטון חלש | סרטון באיכות נמוכה, עם סימן מים או מחזור מוצג פחות. | Instagram | לא | שלב שני | דירוג פיד | https://about.instagram.com/blog/announcements/instagram-ranking-explained |
| אותות "בשבילך" | פעולות המשתמש, כיתוב וצליל, וסיום סרטון ארוך כאות חזק. | TikTok | לא | שלב שני | דירוג פיד | https://newsroom.tiktok.com/en-us/how-tiktok-recommends-videos-for-you |
| מספר עוקבים לא קובע | מספר עוקבים ולהיטים קודמים אינם גורם ישיר. | TikTok | לא | שלב שני | חדש יכול להגיע לאנשים | https://newsroom.tiktok.com/en-us/how-tiktok-recommends-videos-for-you |
| סימון וידאו לגוגל | שם, תמונה ותאריך חובה, והסימון רק בדף שבו הסרטון מתנגן. | Google | לא | שלב שני | מגיע עם הסרטונים | https://developers.google.com/search/docs/appearance/structured-data/video |
| רגעי מפתח | פרקים עם זמנים לסרטון של 30 שניות ומעלה. | Google | לא | שלב שני | מגיע עם הסרטונים | https://developers.google.com/search/docs/appearance/structured-data/video |
| פקדי נגן | עצירה, ניגון, דילוג ופס התקדמות קבוע. | Threads | לא | שלב שני | מגיע עם הסרטונים | https://about.fb.com/news/2025/03/new-threads-features-more-personalized-experience-you-control/ |
| רמיקס | חיתוך 1 עד 5 שניות, מסך ירוק, צליל ושיתוף זה לצד זה. | YouTube | לא | לא נבנה | שימוש בסרטונים של אחרים | https://support.google.com/youtube/answer/10623810?hl=en |
| ביטול רמיקס ומחיקה בשרשרת | רמיקס פעיל כברירת מחדל, ומחיקת המקור מוחקת את הרמיקסים. | YouTube | לא | לא נבנה | תלוי ברמיקס שלא נבנה | https://support.google.com/youtube/answer/10623810?hl=en |
| חיבור קטע מסרטון אחר | משתמש מכניס עד 5 שניות מסרטון של אחר לסרטון שלו. | TikTok | לא | לא נבנה | שימוש בסרטונים של אחרים | https://newsroom.tiktok.com/en-us/new-on-tiktok-introducing-stitch |

## התראות וחזרה לאתר

| פיצ'ר | מיקרו-פיצ'ר (מה בדיוק קורה, משפט אחד) | למי יש | יש לנו היום | החלטה | למה | מקור |
|---|---|---|---|---|---|---|
| מעקב אחרי דיון ומייל על תשובה | לחיצה אחת למעקב, השתקה או צפייה בדיון, ופעמון ומייל כשמישהו עונה. | Discourse, Flarum, Lemmy | לא | גרסה ראשונה | מעקב אחרי דיון ומייל על תשובה | https://github.com/discourse/discourse/blob/main/config/locales/client.en.yml ; https://github.com/flarum/framework/tree/2.x/extensions ; https://join-lemmy.org/docs/users/01-getting-started.html |
| התראה לצוות על ממתינים | הצוות מקבל תזכורת על פריט שלא טופל אחרי 48 שעות, ובלינקדאין אין התראה בכלל. | Discourse, חסר ב-LinkedIn Groups | חלקי: תיבת לידים עם מונה ממתינים | גרסה ראשונה | תור בדיקה לצוות | https://github.com/discourse/discourse/blob/main/config/site_settings.yml ; https://www.linkedin.com/help/linkedin/answer/a541728 |
| סיכום שבועי במייל | עד 5 דיונים פופולריים בשבוע, נעצר אם אין לפחות 2 חדשים, עם הסרה בכל מייל. | Discourse, Circle, Flarum | חלקי: דיוור עם הסכמה והסרה | שלב שני | סיכום שבועי שמדלג כשאין חדש | https://github.com/discourse/discourse/blob/main/config/site_settings.yml ; https://help.circle.so/p/audience/notifications/setting-up-the-weekly-digest ; https://flarum.org/ |
| סיכום שבועי ליוצר | השוואה שבועית של צפיות, עוקבים ותגובות עם טיפים. | Threads | חלקי: מייל חודשי לאיש מקצוע כבוי | שלב שני | סטטיסטיקה שבועית לאיש המקצוע | https://about.fb.com/news/2025/03/new-threads-features-more-personalized-experience-you-control/ |
| פירוט תובנות | לייקים, תגובות, ערים מובילות וגרף של 7 עד 90 יום. | Threads | לא | שלב שני | סטטיסטיקה לאיש המקצוע | https://about.fb.com/news/2025/03/new-threads-features-more-personalized-experience-you-control/ |
| התראות לטלפון | בקשה להתראות דחיפה פעילה כברירת מחדל, ואפליקציות לטלפון. | Discourse | לא | שלב שני | התראות דחיפה לטלפון | https://github.com/discourse/discourse/blob/main/config/site_settings.yml ; https://www.discourse.org/features |
| ברירות מחדל לחבר חדש | המנהל קובע העדפות התראה לחברים חדשים ולכל מרחב. | Circle | לא | שלב שני | חלק מקבלת הפנים | https://help.circle.so/p/audience/notifications |
| התראה על מענה בסרטון | המגיב מקבל התראה כשהיוצר עונה לו בסרטון. | YouTube | לא | שלב שני | תשובות בסרטון | https://support.google.com/youtube/answer/12816427?hl=en-GB |
| מענה מהמייל | ההתראה מגיעה במייל ואפשר לענות ישר מהמייל, כבוי כברירת מחדל. | Discourse | לא | מאוחר יותר | מענה במייל | https://www.discourse.org/features ; https://github.com/discourse/discourse/blob/main/config/site_settings.yml |
| מצב רשימת תפוצה | כל הודעה בפורום נשלחת במייל, כבוי כברירת מחדל. | Discourse | לא | לא נבנה | מצב רשימת תפוצה | https://github.com/discourse/discourse/blob/main/config/locales/client.en.yml ; https://github.com/discourse/discourse/blob/main/config/site_settings.yml |
| הזנת RSS | הזנות לכמה תצוגות. | Lemmy | לא | מאוחר יותר | ערך נמוך | https://join-lemmy.org/ |
| עדכוני פיצ'רים למנהלים | דף הבית של המנהל מראה פיד של כלים חדשים. | Facebook Groups | לא | מאוחר יותר | ערך נמוך | https://about.fb.com/news/2026/10/new-tools-for-the-admins-who-build-communities-on-forum/ |
| התראה על גיליון ניוזלטר | כל גיליון נשלח בדחיפה, באתר ובמייל, עם הסרה בתחתית. | LinkedIn | לא | מאוחר יותר | ניוזלטרים של חברים | https://www.linkedin.com/help/linkedin/answer/a517914 |

## מניעת ספאם ופיקוח

| פיצ'ר | מיקרו-פיצ'ר (מה בדיוק קורה, משפט אחד) | למי יש | יש לנו היום | החלטה | למה | מקור |
|---|---|---|---|---|---|---|
| מגבלות משתמש חדש | משתמש חדש: 2 קישורים, 2 אזכורים, בלי קבצים, 3 דיונים ו-10 תגובות ביום הראשון, ובלי קישורים בתגובות. | Discourse, Stack Overflow, Discord | לא | גרסה ראשונה | מגבלות משתמש חדש | https://github.com/discourse/discourse/blob/main/config/site_settings.yml ; https://stackoverflow.com/help/privileges/new-user ; https://raw.githubusercontent.com/discord/discord-api-docs/main/developers/resources/auto-moderation.mdx |
| המתנה בין הודעות | 5 שניות בין הודעות, 30 למשתמש חדש, ו-10 שניות בפלרום, וטקסט זהה נדחה בתוך 5 דקות. | Discourse, Flarum, Lemmy | חלקי: מגבלות קצב בטפסים | גרסה ראשונה | המתנה בין הודעות וטקסט כפול נדחה | https://github.com/discourse/discourse/blob/main/config/site_settings.yml ; https://raw.githubusercontent.com/flarum/framework/2.x/framework/core/src/Post/PostCreationThrottler.php ; https://raw.githubusercontent.com/flarum/framework/2.x/framework/core/src/User/Throttler/EmailActivationThrottler.php ; https://raw.githubusercontent.com/LemmyNet/lemmy/0.16.7/config/defaults.hjson (לא אומת במלואו) ; https://raw.githubusercontent.com/LemmyNet/lemmy/main/crates/db_schema/src/source/local_site_rate_limit.rs (לא אומת במלואו) |
| תקרות יומיות | 50 לייקים, 20 דיווחים, 30 עריכות ו-20 הודעות פרטיות ביום. | Discourse | חלקי: מגבלות קצב בטפסים | גרסה ראשונה | מגבלות קצב | https://github.com/discourse/discourse/blob/main/config/site_settings.yml |
| זיהוי אתר שחוזר | משתמש חדש שמקשר 3 פעמים לאותו אתר נתפס, עם רשימות אתרים מותרים וחסומים. | Discourse | חלקי: ניקוי קישורים וטלפונים בהמלצות | גרסה ראשונה | הגבלת קישורים למשתמש חדש | https://github.com/discourse/discourse/blob/main/config/site_settings.yml |
| כלל קבוע לקישורים | מנהל משלב תנאים כמו קישור או אורך לכלל אוטומטי ששולח לבדיקה. | Facebook Groups | לא | גרסה ראשונה | קישור ממשתמש חדש הולך לבדיקה | https://about.fb.com/news/2026/10/new-tools-for-the-admins-who-build-communities-on-forum/ |
| מילים אסורות וכללי מילים | רשימת מילים ותבניות שעוצרות הודעה, שולחות התראה לצוות או משתיקות. | Circle, Discord | חלקי: מסנן מילים אסורות במתווכים | גרסה ראשונה | עוצר ספאם של טלפונים ווואטסאפ | https://help.circle.so/p/administration/moderation/manage-moderation-settings ; https://raw.githubusercontent.com/discord/discord-api-docs/main/developers/resources/auto-moderation.mdx ; https://support.discord.com/hc/en-us/articles/4421269296535-AutoMod-FAQ |
| הודעה ראשונה ממתינה לאישור | התוכן של חבר חדש מוחזק עד שההודעה הראשונה מאושרת, ומי שנדחה נשאר בבדיקה. | Circle, Discourse, Flarum | חלקי: ביקורות וכרטיסים ממתינים לאישור | גרסה ראשונה | הודעה ראשונה ממתינה לאישור | https://help.circle.so/p/administration/moderation/manage-moderation-settings ; https://github.com/discourse/discourse/blob/main/config/site_settings.yml ; https://raw.githubusercontent.com/flarum/framework/2.x/extensions/approval/src/Listener/ApproveContent.php |
| דיווח והסתרה אוטומטית | אחרי כמה דיווחים ההודעה מוסתרת לבד, ודיווח שוקל הרבה יותר מלייק. | Discourse, Circle, X | לא | גרסה ראשונה | כפתור דיווח והסתרה אחרי כמה דיווחים | https://github.com/discourse/discourse/blob/main/config/site_settings.yml ; https://help.circle.so/p/administration/moderation/manage-moderation-settings ; https://github.com/twitter/the-algorithm-ml/blob/main/projects/home/recap/README.md |
| השתקת משתמש חדש אחרי דיווחים | משתמש חדש שדווח בידי 3 אנשים שונים מושתק. | Discourse | לא | גרסה ראשונה | המשך של הסתרה אחרי דיווחים | https://github.com/discourse/discourse/blob/main/config/site_settings.yml |
| סגירת דיון אחרי דיווחים | 5 מדווחים סוגרים דיון, והוא נפתח שוב אחרי 4 שעות. | Discourse | לא | גרסה ראשונה | המשך של הסתרה אחרי דיווחים | https://github.com/discourse/discourse/blob/main/config/site_settings.yml |
| תיקון טעות שדווחה | טעות שדווחה מתוקנת תוך 7 ימי עסקים. | מדרג | לא | גרסה ראשונה | חלק מכפתור הדיווח | https://www.midrag.co.il/Content/Article/10461 |
| מצב איטי לשרשור | המתנה של עד 6 שעות בין הודעות של אותו אדם בשרשור סוער. | Discord | לא | גרסה ראשונה | מגבלות קצב | https://support.discord.com/hc/en-us/articles/360016150952-Slowmode-FAQ ; https://raw.githubusercontent.com/discord/discord-api-docs/main/developers/resources/channel.mdx |
| השעיה, השתקה וחסימה | עצירה זמנית של כתיבה ותגובות עם סיבה ביומן, הגבלת פעילות, או חסימה שמונעת חזרה. | Discord, Facebook Groups, Flarum, Discourse, LinkedIn Groups | לא | גרסה ראשונה | כלי בסיסי לצוות לצד תור הבדיקה | https://support.discord.com/hc/en-us/articles/4413305239191-Time-Out-FAQ ; https://about.fb.com/news/2022/03/new-tools-for-facebook-group-admins/ ; https://www.facebook.com/help/719854838671405 (לא אומת במלואו) ; https://github.com/flarum/framework/tree/2.x/extensions ; https://blog.discourse.org/2018/06/understanding-discourse-trust-levels/ ; https://www.linkedin.com/help/linkedin/answer/a553202 |
| נעילת שרשור | נעילה עוצרת תגובות חדשות. | Flarum, Lemmy, Reddit | לא | גרסה ראשונה | כלי בסיסי לצוות | https://github.com/flarum/framework/tree/2.x/extensions ; https://join-lemmy.org/docs/users/04-moderation.html |
| תור בדיקה לצוות | לשוניות לבדיקה, מדווחים, הוסרו ונערכו, עם מיון לפי מספר דיווחים. | Reddit | חלקי: תיבת לידים עם מונה ממתינים | גרסה ראשונה | תור בדיקה לצוות | https://support.reddithelp.com/hc/en-us/articles/15484440494356-Moderation-Queue |
| צוות בשם | אי אפשר לנהל או לפקח בעילום שם. | LinkedIn Groups | לא | גרסה ראשונה | אמון, חלק מצוות הבדיקה | https://www.linkedin.com/help/linkedin/answer/a553202 |
| חוקים נגד קידום עצמי | לכל היותר 10% קידום עצמי, בלי פרסום בלי רשות, ופרסומות צד שלישי רק באישור. | Reddit, הסולידית, מדרג | לא | גרסה ראשונה | חוקי קהילה | https://support.reddithelp.com/hc/en-us/articles/28012014962580-How-do-I-keep-spam-out-of-my-community ; https://www.hasolidit.com/kehila/ ; https://www.midrag.co.il/Content/Article/10461 |
| כללים לבקשת שירות | בקשה לא תכיל טלפון או מייל, ובקשות כפולות או מעבר למכסה נחסמות. | LinkedIn | לא | גרסה ראשונה | מגבלות קצב וטקסט כפול | https://www.linkedin.com/help/recruiter/answer/a799706 (לא אומת במלואו) |
| יומן פעולות וכלי פרטיות | יומן פעולות, ייצוא ומחיקת מידע לפי בקשה. | Flarum | חלקי: הבטחת תיקון ומחיקה במייל | גרסה ראשונה | הודעת פרטיות וזכויות בכניסה | https://flarum.org/ |
| Akismet | בדיקת הודעות של משתמשים חדשים בשירות חיצוני שלומד מהסתרה ומאישור. | Discourse, Flarum | לא | שלב שני | בתשלום חודשי, קודם כללים חינמיים | https://github.com/discourse/discourse-akismet/blob/main/config/settings.yml ; https://raw.githubusercontent.com/flarum/framework/2.x/extensions/akismet/extend.php |
| סריקת ספאם בבינה מלאכותית | מודל סורק את 3 ההודעות הראשונות של משתמש חדש. | Discourse | לא | מאוחר יותר | פיקוח בבינה מלאכותית | https://github.com/discourse/discourse/blob/main/plugins/discourse-ai/config/settings.yml |
| תיוג בבינה מלאכותית בתור | כל פוסט ממתין מתויג "כנראה עומד" או "אולי מפר". | Facebook Groups | לא | מאוחר יותר | פיקוח בבינה מלאכותית | https://about.fb.com/news/2026/10/new-tools-for-the-admins-who-build-communities-on-forum/ |
| דחיית מידע כוזב | פוסט שבודקי עובדות סימנו כשקרי נדחה לבד. | Facebook Groups | לא | מאוחר יותר | אין בודקי עובדות בעברית לחבר | https://about.fb.com/news/2022/03/new-tools-for-facebook-group-admins/ |
| מסנן הטרדה | מודל מעביר תגובות שנראות מטרידות לתור, עם רשימת חריגים. | Reddit | לא | מאוחר יותר | פיקוח בבינה מלאכותית | https://support.reddithelp.com/hc/en-us/articles/23856209638932-Harassment-filter |
| בקרת קהל | תגובות של מי שעוד לא נחשב אמין מקופלות או מסוננות. | Reddit | לא | מאוחר יותר | נשען על ניקוד שלילי, הודעה ראשונה ממתינה מספיקה | https://support.reddithelp.com/hc/en-us/articles/15484545006996-Crowd-Control |
| מסנן מוניטין | סינון לפי ציון איכות כללי של החשבון. | Reddit | לא | מאוחר יותר | דורש הרבה נתונים | https://support.reddithelp.com/hc/en-us/articles/27441485903124-Reputation-filter |
| מסנן עקיפת חסימה | סינון תוכן מחשבונות משנה של מי שנחסם. | Reddit | לא | מאוחר יותר | כבד לבנייה | https://support.reddithelp.com/hc/en-us/articles/15484544471444-Ban-evasion-filter |
| התראות על פעילות חריגה | פעילות חריגה מתריעה לצוות, שעוצר הזמנות והודעות בלחיצה. | Discord | לא | מאוחר יותר | ערך בינוני בהתחלה | https://support.discord.com/hc/en-us/articles/17439993574167-Activity-Alerts-Security-Actions |
| חסימת שאלות שקטה | מי ששאל שאלות חלשות נחסם משאלות בלי סימן גלוי. | Stack Overflow | לא | לא נבנה | שער שחוסם אנשים רגילים מלשאול | https://stackoverflow.com/help/question-bans |
| תורי בדיקה קהילתיים | חברים בודקים שאלות ראשונות, תשובות מאוחרות ועריכות. | Stack Overflow | לא | מאוחר יותר | לא מתאים לקהילה קטנה | https://stackoverflow.com/help/review-queues |
| יומן פיקוח ציבורי | הסרות ופעולות צוות מוצגות ביומן שמקושר מכל דף. | Lemmy | לא | מאוחר יותר | שקיפות, לא חיוני בהתחלה | https://join-lemmy.org/docs/users/04-moderation.html ; https://join-lemmy.org/ |
| מחיקה אוטומטית של מה שהוסר | הודעה שהוסרה נמחקת אחרי 24 שעות. | Discourse | לא | מאוחר יותר | מדיניות שמירה, אחרי ייעוץ | https://github.com/discourse/discourse/blob/main/config/site_settings.yml |

## גוגל ונראות בחיפוש

| פיצ'ר | מיקרו-פיצ'ר (מה בדיוק קורה, משפט אחד) | למי יש | יש לנו היום | החלטה | למה | מקור |
|---|---|---|---|---|---|---|
| דף מוכן מהשרת לגוגל | גוגל מקבל דף מלא מהשרת עם כותרת, תיאור וקישורי הקודם והבא. | Discourse | לא | גרסה ראשונה | דף שגוגל קורא | https://github.com/discourse/discourse/blob/main/app/views/layouts/crawler.html.erb ; https://github.com/discourse/discourse/blob/main/app/views/topics/show.html.erb |
| סימון מבנה בדף הדיון | פירורי לחם, כותב, תאריכים, מונה לייקים וטקסט לכל הודעה, בלי הודעות מוסתרות. | Discourse | לא | גרסה ראשונה | נתונים מובנים לדיונים | https://github.com/discourse/discourse/blob/main/app/views/topics/show.html.erb |
| סכמת דיון בפורום | חובה כותב, תאריך וטקסט, ומומלץ כתובת, כותרת, תגובות ומצב "נמחק". | Google | לא | גרסה ראשונה | נתונים מובנים לדיונים | https://developers.google.com/search/docs/appearance/structured-data/discussion-forum |
| סכמת שאלה ותשובה | שאלה אחת לדף, מספר תשובות ותשובה שנבחרה או מוצעת. | Google | לא | גרסה ראשונה | נתונים מובנים לדיונים | https://developers.google.com/search/docs/appearance/structured-data/qapage |
| סכמה לתשובה שנבחרה | תוסף "נפתר" מוסיף סימון מבנה תמיד. | Discourse | לא | גרסה ראשונה | נתונים מובנים לדיונים | https://github.com/discourse/discourse/blob/main/plugins/discourse-solved/config/settings.yml |
| סכמת דף פרופיל | אדם או ארגון עם שם, ומומלץ תאריכים, נתוני פעילות ותמונה. | Google | חלקי: סכמת עסק מקומי בכרטיס | גרסה ראשונה | נתונים מובנים לפרופילים | https://developers.google.com/search/docs/appearance/structured-data/profile-page |
| סימון קישורי משתמשים | קישורים של משתמשים מסומנים כתוכן גולשים, ואפשר להסיר את הסימון לחברים אמינים. | Discourse, Google | חלקי: ניקוי קישורים וטלפונים בהמלצות | גרסה ראשונה | הגבלת קישורים וגוגל | https://github.com/discourse/discourse/blob/main/config/site_settings.yml ; https://developers.google.com/search/docs/crawling-indexing/qualify-outbound-links |
| מפת אתר לדיונים | מפת אתר פעילה כברירת מחדל, עד 10,000 כתובות בעמוד. | Discourse | לא | גרסה ראשונה | מפת אתר לדיונים | https://github.com/discourse/discourse/blob/main/config/site_settings.yml |
| עברית בכתובת | בחירה אם מילים בעברית נשארות בכתובת, ובהסולידית הן נשמרות מקודדות. | Discourse, הסולידית | לא | גרסה ראשונה | כתובת קבועה לכל דיון, נבחרת לפני ההשקה | https://github.com/discourse/discourse/blob/main/config/site_settings.yml ; https://github.com/discourse/discourse/blob/main/app/models/slug_setting.rb ; https://www.hasolidit.com/kehila/forums/%D7%A0%D7%93%D7%9C-%D7%9F.28/ |
| טיפול בתוכן ריק | הודעות ריקות או מוסתרות לא נשלחות לגוגל, ודיון של 10,000 הודעות נסגר וממשיך בחדש. | Discourse | לא | גרסה ראשונה | חלק מהדף שגוגל קורא | https://github.com/discourse/discourse/blob/main/app/views/topics/show.html.erb ; https://github.com/discourse/discourse/blob/main/config/site_settings.yml |

## חיים בזמן אמת

| פיצ'ר | מיקרו-פיצ'ר (מה בדיוק קורה, משפט אחד) | למי יש | יש לנו היום | החלטה | למה | מקור |
|---|---|---|---|---|---|---|
| "כותב עכשיו" | מתחת לדיון מופיעים עד 5 שמות של מי שכותב תשובה כרגע. | Discourse, Flarum | לא | שלב שני | "כותב עכשיו" | https://github.com/discourse/discourse/blob/main/plugins/discourse-presence/config/settings.yml ; https://flarum.org/ |
| תשובות חדשות נכנסות חי | דיונים, תשובות והתראות מופיעים בלי רענון, בקבוצות כל 10 שניות, עם הודעה קופצת. | Flarum | לא | שלב שני | הכנסה חיה של תשובות | https://raw.githubusercontent.com/flarum/framework/2.x/extensions/realtime/extend.php ; https://flarum.org/ |
| הסתרת נוכחות | משתמש יכול להסתיר שהוא נמצא באתר. | Discourse | לא | שלב שני | בא יחד עם "כותב עכשיו" | https://github.com/discourse/discourse/blob/main/config/site_settings.yml |
| צ'אט חי עם מארחים | צ'אטים חיים עם מארחים ומארחים משותפים, וציטוט רגעים לפיד. | Threads | לא | מאוחר יותר | חדרי שיחה | https://about.fb.com/news/2026/06/meta-launching-new-features-500-million-monthly-threads-users/ |

## נגישות וטלפון

| פיצ'ר | מיקרו-פיצ'ר (מה בדיוק קורה, משפט אחד) | למי יש | יש לנו היום | החלטה | למה | מקור |
|---|---|---|---|---|---|---|
| ימין לשמאל אמיתי | ממשק מימין לשמאל לעברית ולשפות דומות, עם תרגום מלא. | Discourse | לא | גרסה ראשונה | ימין לשמאל ופריסה לטלפון | https://github.com/discourse/discourse/blob/main/lib/rtl.rb |
| ניגודיות ומצב כהה | ערכת צבעים לפי תקן נגישות ומצב כהה. | Discourse, Flarum, Lemmy | לא | גרסה ראשונה | בסיס נגישות | https://www.discourse.org/features ; https://flarum.org/ ; https://join-lemmy.org/ |
| ניווט מלא במקלדת | מעבר בין רכיבים במקלדת עם מסגרת מיקוד. | Discord | לא | גרסה ראשונה | בסיס מקלדת וקורא מסך | https://support.discord.com/hc/en-us/articles/1500000056121-Keyboard-Navigation-FAQ |
| התאמות לטלפון | חיפוש בתפריט הנייד, תפריטים נפתחים בנגיעה ראשונה ורטט אופציונלי. | Flarum | לא | גרסה ראשונה | פריסה לטלפון | https://flarum.org/ |
| כפתור כתיבה צף | כפתור "שאל שאלה" נשאר גלוי בהישג האגודל בזמן גלילה. | Facebook Groups | לא | גרסה ראשונה | פריסה לטלפון ומטרות מגע 44 פיקסלים | https://about.fb.com/news/2021/11/new-tools-in-facebook-groups/ |
| דפדפנים נתמכים | דפדפנים עדכניים ו-Safari מגרסה 16.4. | Discourse | לא | גרסה ראשונה | פריסה לטלפון | https://github.com/discourse/discourse |
| קיצורי מקלדת | ערכת קיצורים כמו ? לעזרה ו-/ לחיפוש. | Discourse | לא | מאוחר יותר | ערכות קיצורי מקלדת | https://github.com/discourse/discourse/blob/main/frontend/discourse/app/services/keyboard-shortcuts.js (לא אומת במלואו) |

## כסף

| פיצ'ר | מיקרו-פיצ'ר (מה בדיוק קורה, משפט אחד) | למי יש | יש לנו היום | החלטה | למה | מקור |
|---|---|---|---|---|---|---|
| מנויים בתשלום | מנויים, טבלת מחירים וקמפיין גיוס, כבוי כברירת מחדל. | Discourse | חלקי: מסלולי חינם, פרו ופרימיר | מאוחר יותר | מחכה להחלטה עסקית של הבעלים | https://github.com/discourse/discourse/blob/main/plugins/discourse-subscriptions/config/settings.yml |
| חומות תשלום | תשלום חד פעמי, מנוי או תשלומים, קופונים וסגירת מרחב. | Circle | לא | מאוחר יותר | מחכה להחלטה עסקית של הבעלים | https://help.circle.so/p/payments/paywall-setup |
| מנויי תפקיד | רכישת מנוי לתפקיד בשרת. | Discord | לא | מאוחר יותר | מחכה להחלטה עסקית של הבעלים | https://raw.githubusercontent.com/discord/discord-api-docs/main/developers/resources/guild.mdx |
| פרסומות ושותפים | תוסף פרסומות ותוסף שותפים, ובהסולידית באנר של בית השקעות. | Discourse, הסולידית | לא | מאוחר יותר | מחכה להחלטה עסקית של הבעלים | https://github.com/discourse/discourse/tree/main/plugins ; https://www.discourse.org/features ; https://www.hasolidit.com/kehila/ |
| פרסים בתשלום | פרסים בחינם ובתשלום על פוסטים, שמכניסים כסף למקבלים. | Reddit | לא | מאוחר יותר | פרסים | https://support.reddithelp.com/hc/en-us/articles/26465598697876-What-are-awards-and-how-do-I-use-them |
| לוח משרות ופחות פרסומות | לוח משרות, פרסום, ומ-200 נקודות חלק מהפרסומות נעלמות. | Stack Overflow | לא | מאוחר יותר | לוח משרות | https://stackoverflow.com/help/privileges ; https://stackoverflow.com/help/editing (לא אומת במלואו) |
| מנוי עסקי | חשיפה מעבר לרשת, 15 הודעות בתשלום, רשימת צופים לשנה וכפתור אישי. | LinkedIn | לא | מאוחר יותר | מחכה להחלטה עסקית של הבעלים | https://premium.linkedin.com/small-business/business |
| כלי מכירות | חיפוש לידים ו-50 הודעות בתשלום בחודש. | LinkedIn | לא | מאוחר יותר | מחכה להחלטה עסקית של הבעלים | https://business.linkedin.com/sell/sales-navigator/compare-plans |
| יותר לידים למנויים | מנויים מקבלים יותר בקשות שירות וכפתור "בקשת שירות". | LinkedIn | לא | מאוחר יותר | מחכה להחלטה עסקית של הבעלים | https://www.linkedin.com/help/linkedin/answer/a564491 |
| חבילות עסקיות | חבילות של 14.99 עד 499 דולר בחודש עם תג מאומת. | Meta | לא | מאוחר יותר | מחכה להחלטה עסקית של הבעלים | https://about.fb.com/news/2026/09/introducing-meta-one-subscription-service-more-features-ai/ |
| קידום ממומן | קידום מ-5 דולר ליותר מ-6 ימים, ועד 75% חריגה מהתקציב היומי. | Meta | חלקי: תווית מקודם וחסות כרטיס | מאוחר יותר | פוסטים מקודמים | https://www.facebook.com/business/ads/pricing |
| תתי קבוצות בתשלום וחנות | תתי קבוצות בתשלום, חנות של הקבוצה וגיוס תרומות (ניסוי). | Facebook Groups | לא | מאוחר יותר | מחכה להחלטה עסקית של הבעלים | https://about.fb.com/news/2021/11/new-tools-in-facebook-groups/ |
| עמלה על עבודה שנסגרה | 5% עד 10% מכל עבודה אחרי שאיש המקצוע קיבל תשלום, ודמי בדיקה של כ-390 ש"ח. | מדרג | לא | מאוחר יותר | החלטת בעלים, ואסור לקשור לעסקת נכס | https://biz.midrag.co.il/Content/Article/14483 |
| קרן פיצוי | פיצוי ללקוח עד 1,000 ש"ח. | מדרג | לא | מאוחר יותר | מחכה להחלטה עסקית של הבעלים | https://www.midrag.co.il/Content/Article/10461 |
| מנוי תוכנה לאנשי מקצוע | מ-199 דולר בחודש לאדם אחד ו-399 לצוות. | Houzz | לא | מאוחר יותר | מחכה להחלטה עסקית של הבעלים | https://www.houzz.com/houzz-pro/pricing |
| חבילת פרסום | פרסום ממומן מ-499 דולר בחודש, וב-B144 פרסום בתשלום עם דף ביטול. | Houzz, B144 | לא | מאוחר יותר | מחכה להחלטה עסקית של הבעלים | https://www.houzz.com/houzz-pro/pricing ; https://www.b144.co.il/ |


## סיכום ההחלטות

| החלטה | מספר שורות |
|---|---|
| גרסה ראשונה | 82 |
| שלב שני | 119 |
| מאוחר יותר | 113 |
| לא נבנה | 19 |
| סך הכול | 333 |

### מה נכנס לגרסה הראשונה

קריאה בלי כניסה; שואלים ועונים בלי ניקוד; קישור כניסה במייל; כניסה עם החשבון של האתר הראשי; חוקים גלויים לחדשים; אישור חוקים לפני כתיבה; הזמנה להירשם אחרי קריאה; שם תצוגה אמיתי; רמות אימות לקהילה; מגבלת הרשמות לכתובת IP; שדה מלכודת והצלחה מדומה; בדיקת אדם; עסק מוסיף את עצמו; שמירת טיוטה; ציטוט מסימון טקסט; עורך עם עיצוב פשוט; "יש דיון דומה"; חסימת כותרת כפולה; תשובות מוכנות לצוות; אורך מינימלי; בית פורום אחד וכתובת קבועה לכל דיון; "המומחים עונים"; איש מקצוע עונה עם קישור לכרטיס; סימון התשובה שעזרה; דיונים קשורים בסוף הדיון; מוני צפיות ותגובות; זמן הפעילות האחרונה; "תודה" אחת חיובית; רמות אמון אוטומטיות; תווית תפקיד ליד השם; סימן מאומת; בדיקה מול פנקס רשמי; תג בלי פרטי המסמך; "על הפרופיל הזה"; קטגוריה חובה; מדריך לפי מקצוע ועיר; הנחיות כתיבה בכל פורום; סינון "נפתר"; פרופיל ציבורי לגוגל; כל אזכור מגיע לכרטיס; הסתרה או הסרה של הכרטיס; שדות פרופיל מותאמים; כפתור פעולה אישי; פנייה חופשית בלי חיבור; בקשת הצעת מחיר; מעקב אחרי דיון ומייל על תשובה; התראה לצוות על ממתינים; מגבלות משתמש חדש; המתנה בין הודעות; תקרות יומיות; זיהוי אתר שחוזר; כלל קבוע לקישורים; מילים אסורות וכללי מילים; הודעה ראשונה ממתינה לאישור; דיווח והסתרה אוטומטית; השתקת משתמש חדש אחרי דיווחים; סגירת דיון אחרי דיווחים; תיקון טעות שדווחה; מצב איטי לשרשור; השעיה, השתקה וחסימה; נעילת שרשור; תור בדיקה לצוות; צוות בשם; חוקים נגד קידום עצמי; כללים לבקשת שירות; יומן פעולות וכלי פרטיות; דף מוכן מהשרת לגוגל; סימון מבנה בדף הדיון; סכמת דיון בפורום; סכמת שאלה ותשובה; סכמה לתשובה שנבחרה; סכמת דף פרופיל; סימון קישורי משתמשים; מפת אתר לדיונים; עברית בכתובת; טיפול בתוכן ריק; ימין לשמאל אמיתי; ניגודיות ומצב כהה; ניווט מלא במקלדת; התאמות לטלפון; כפתור כתיבה צף; דפדפנים נתמכים.

### הערה

שיתוף דיון לוואטסאפ, מטרות מגע של 44 פיקסלים והודעת פרטיות בכניסה הם חלק מכללי הגרסה הראשונה, אבל אין להם שורה נפרדת בקבצי המחקר, ולכן הם לא מופיעים כשורה בטבלה.
