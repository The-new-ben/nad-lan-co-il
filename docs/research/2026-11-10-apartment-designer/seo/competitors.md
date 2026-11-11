# Competitor teardown: top results of the 8 head queries (HAD-701)

Fetched 10.11.2026 with a normal desktop Chrome user agent (no crawler spoofing). Raw HTML and per-page JSON (title, meta, canonical, robots, every H1/H2/H3 verbatim, word count, price snippets, schema types) are in `competitor-pages/` and `price-pages/`.
Word count = words in `<main>`/`<article>` (or body) minus nav, header, footer, scripts. Tool detection reads the HTML for real inputs, sliders, canvas, iframes and tables; site-wide menus are not counted.
Not fetched: Facebook group posts (login wall, HTTP 400), Instagram (no content), app-store pages (query strings stripped in capture). studio-id.co.il returned 502 to the script and was read through a fetch tool instead (headings listed in prices.md).
Heading lists below drop only obvious chrome (phone numbers, contact-form labels, footer, cookie banners). Everything else is verbatim, in page order.

## Summary across the 8 heads

- **No page combines a working planner, prices and a guide.** Tools exist only on SaaS sites (redesignai, genroom, aihouse, roomsgpt); guides and prices sit on designer blogs and midrag.
- **Price pages are 650 to 2,200 words** with 6 to 14 H2s and a FAQ. Recurring H2 skeleton: מה משפיע על המחיר / מודלי תמחור (לשעה, למ"ר, פרויקטלי, אחוז) / כמה עולה לפי סוג פרויקט (3, 4, 5 חדרים, בית פרטי) / מה כולל שירות מלא / איך לבחור מעצב / שאלות נפוצות. Only ziratadrichalut and bethameatzvot state the VAT basis.
- **Designer homepages are thin** (100 to 1,900 words), portfolio + process + testimonials.
- **Magazines** (bvd, baitvenoy, ynet, pickinteri) win the broad and small-apartment heads with long project lists.
- **FAQPage schema** is common on price and contractor-apartment pages (midrag, shimrit, meitalyaakov, ultimaschool, mayakedem, ziratadrichalut, studio-vida, keinan, nhdesign, shuki-meir).
- **Interactive tools on page 1:** none of the Israeli guide/price pages has a calculator. The only interactive results are the SaaS products themselves.

## עיצוב דירה

### #1 https://www.bvd.co.il/design-homes/apartments/

- Title: עיצוב דירות - המדור שיעזור לכם לעשות את זה נכון | בניין ודיור
- Words: 314 · H2: 26 · H3: 0 · price mentions: 0 · schema: BreadcrumbList, EntryPoint, ImageObject, ListItem, Organization, PropertyValueSpecification, ReadAction, SearchAction, WebPage, WebSite
- Tools: gallery/slider
- File: `competitor-pages/https_www_bvd_co_il_design_homes_apartments__c102d4.json`

- H1: עיצוב דירות
  - H2: שלב חדש, בית חדש: דירה שעברה מהפך מדויק
  - H2: המפלט האורבני הכי יפה שיש
  - H2: בית שהוא חופשה מתמשכת
  - H2: חומריות, חמימות ומשפחה: הבית שעוצב סביב החיים עצמם
  - H2: צבעוני, שובבי אבל גם עתידני
  - H2: פנטהאוז משפחתי באור יהודה: כשהאחסון הופך לחלק משפת העיצוב
  - H2: לב העיר, עם תחושה של ריזורט פרטי: הדירה התל־אביבית שעוצבה סביב חומרים, אור ושקט
  - H2: שקט, חומר ואור: הדירה שנבנתה מחדש סביב החיים עצמם
  - H2: היכן שהרי ירושלים פוגשים חיים מודרניים
  - H2: שלוש חזיתות אל הים: הפנטהאוז החיפאי שתוכנן מחדש סביב הנוף
  - H2: POWER OF CREATION: כשהבית מתבגר יחד עם המשפחה תכנון ועיצוב פנים יפעת מנטש
  - H2: "הארונות הם הקירות החדשים של הבית": ראיון עם תמיר רז, מנכ"ל דלקוב
  - H2: מהפנטזיה האיטלקית למורשת ישראלית: סיפורה של משפחת גטניו
  - H2: לפתוח, להאיר ולנשום: הבית הישן במתן שקיבל חיים חדשים
  - H2: הטיל פגע בבית, העיצוב החזיר אותו לחיים
  - H2: הם רצו בית פרטי והיא תכננה אותו בחודש אחד: הפנטהאוז שמרגיש כמו וילה
  - H2: כשהכלב גונב את הפריים
  - H2: מהפך בדירה עם פרקט שברון
  - H2: היוקרה שלא צריכה להוכיח שום דבר: הפנטהאוז התל־אביבי שעבר מהפך
  - H2: החלום שנדחה בעשור: הצצה לסוויטת ההורים החדשה
  - H2: הים, הקימורים והחומרים: בתוך דירה של 230 מ"ר בתל אביב
  - H2: בוער לכם על קמין? זה מה שכדאי לדעת לפני שמדליקים
  - H2: בין טבע ליוקרה: הבית בהרצליה שבו כל פרט תוכנן עד הסנטימטר האחרון
  - H2: היא לא גדלה אפילו במטר: אבל מרגישה כמו דירה אחרת לגמרי

### #2 https://www.baitvenoy.co.il/עיצוב

- Title: עיצוב פנים מקבל כיוון דרך חדרים, חומרים וסיפורי בתים שונים
- Words: 615 · H2: 4 · H3: 13 · price mentions: 1 · schema: BreadcrumbList, CollectionPage, ContactPoint, ImageObject, ItemList, ListItem, Organization, Thing, WebSite
- Tools: none detected
- File: `competitor-pages/https_www_baitvenoy_co_il__d1869f.json`

- H1: עיצוב פנים דרך מדריכים, כתבות ומדורי המגזין
  - H2: מסלול בין החדרים
    - H3: משולש העבודה במטבח
    - H3: הסלון מתחיל בשטיח
    - H3: חושך בבוקר בחדר השינה
    - H3: אוויר שזורם בחדר הרחצה
    - H3: חדר ילדים לשנים ארוכות
  - H2: התכנון הפנימי מקדים את לוח החומרים
  - H2: רושמים על אותה תכנית
  - H2: מבהירים את היקף הליווי
    - H3: מתי די בריענון החפצים הקיימים?
    - H3: איך מחברים בין שימוש למראה?
    - H3: מה להביא לפגישה על דירה שקיבלתם?
    - H3: מידע וקטגוריות
    - H3: עיצוב בתים ודירות
    - H3: אדריכלות ותכנון
    - H3: עיצוב מסחר ועסקים

### #3 https://www.pinterest.com/kerenorharl0082/עיצוב/

- Title: 88 רעיונות של עיצוב | עיצוב, דירה קטנטנה, פנים המשרד
- Words: 47 · H2: 0 · H3: 0 · price mentions: 0 · schema: none
- Tools: iframes: ct.pinterest.com; quiz text
- File: `competitor-pages/https_www_pinterest_com_kerenorharl0082__3fa1ee.json`

- H1: עיצוב

### #4 https://www.dordesign.co.il/

- Title: מעצבת פנים הדר דור (Dordesign) – עיצוב פנים מרהיב, מעל 20 שנות ניסיון
- Words: 922 · H2: 9 · H3: 12 · price mentions: 0 · schema: Article, BreadcrumbList, CreativeWork, EntryPoint, GeoCoordinates, ImageObject, ListItem, Offer, Organization, Person
- Tools: HTML tables x1; gallery/slider
- File: `competitor-pages/https_www_dordesign_co_il__c9c3c7.json`

- H1: מעצבת פנים הדר דור - Dordesign
  - H2: עיצוב פנים לבתים פרטיים, פנטהאוזים ודירות - תכנון מקצועי ועיצוב מרהיב
  - H2: כיצד לבחור מעצבת פנים ואיך עובדים איתה?
  - H2: פרויקטים נבחרים
    - H3: לפני אחרי בעיצוב פנים
  - H2: מדוע לבחור בי בתור מעצבת פנים שלכם?
  - H2: תקשורת ופרסום
    - H3: זכייה בפרס חביבת הקהל
    - H3: הדר דור בתכנית הבוקר
    - H3: הדר דור במגזין בניין ודיור
    - H3: הדר דור בפרסומת של פנדור
    - H3: הדר דור במגזין לאשה
    - H3: הדר דור בערוץ החיים הטובים
  - H2: לקוחות ממליצים
    - H3: המלצות נוספות >>
  - H2: קטגוריות עיצוב פנים
    - H3: עיצוב בתים
    - H3: עיצוב פנטהאוזים
    - H3: עיצוב דירות
    - H3: עיצוב משרדים ומרפאות
  - H2: תהליך העבודה בסטודיו — איך אנחנו מובילים אתכם לעיצוב מושלם
  - H2: תהליך העבודה בסטודיו — איך אנחנו מובילים אתכם לעיצוב מושלם

### #5 https://www.mako.co.il/living-architecture/local/Article-8482bea0a7fb1a1026.htm

- Title: צפון ת"א: האחים קנו דירה יחד וזה מה שהם עשו
- Words: 1,326 · H2: 0 · H3: 1 · price mentions: 3 · schema: BreadcrumbList, ListItem, NewsArticle, NewsMediaOrganization, Person, SpeakableSpecification, ViewAction, WebPage
- Tools: gallery/slider
- File: `competitor-pages/https_www_mako_co_il_living_architecture_local_Article_8482bea0a7fb1a1026_htm_0393a0.json`

- H1: צפון תל אביב: אח ואחות, שני סגנונות שונים ודירה אחת
    - H3: לכל הכתבות בערוץ living

### #6 https://www.rossetto.co.il/איך-לעצב-את-הבית-לבד/

- Title: איך לעצב את הבית לבד? מדריך פרקטי לעיצוב פנים עצמאי בסטייל | Rossett
- Words: 1,019 · H2: 22 · H3: 6 · price mentions: 1 · schema: Article, ImageObject, Organization, Person
- Tools: gallery/slider
- File: `competitor-pages/https_www_rossetto_co_il__3e243e.json`

- H1: איך לעצב את הבית לבד? מדריך פרקטי לעיצוב פנים עצמאי מלא בסטייל
  - H2: למה לעצב את הבית בעצמכם?
  - H2: מאיפה מתחילים? שלבי העבודה הראשונים
  - H2: 6 טיפים מנצחים לעיצוב הבית בעצמכם
    - H3: טיפ 1: הכניסו את האישיות שלכם לעיצוב
    - H3: טיפ 2: לא להשאיר קירות ריקים
    - H3: טיפ 3: משחק עם טקסטורות ובדים
    - H3: טיפ 4: תאורה – המפתח לאווירה מושלמת
    - H3: טיפ 5: ותרו על סטים תואמים
    - H3: טיפ 6: הוספת צמחייה וירוק לבית
  - H2: ניצול חכם של החלל
  - H2: בחירת צבעים ומיקום רהיטים
  - H2: עיצוב בתקציב מוגבל
  - H2: סיכום והמלצות
  - H2: קטגוריות מוצרים
  - H2: יצירת קשר
- H1: תודה על פנייתך! ניצור קשר בהקדם
  - H2: אנחנו כאן בשבילכם
  - H2: נא מלאו פרטים ונציגינו יחזרו אליכם בהקדם האפשרי
  - H2: או חייגו 1-800-352-929
  - H2: אספקות
  - H2: שירות לקוחות
  - H2: צור קשר

### #7 https://netalinoy.com/project_cat/עיצוב-פנים-מודרני-יוקרתי/

- Title: עיצוב פנים מודרני יוקרתי - נטע לי וטל נוי - עיצוב פנים מודרני ברמה אחרת
- Words: 1,136 · H2: 12 · H3: 5 · price mentions: 0 · schema: BreadcrumbList, CollectionPage, EntryPoint, ImageObject, ListItem, Organization, PropertyValueSpecification, SearchAction, WebSite
- Tools: iframes: netalinoy.com; gallery/slider
- File: `competitor-pages/https_netalinoy_com_project_cat__d17657.json`

- H1: עיצוב פנים מודרני יוקרתי
  - H2: עיצוב פנים מודרני יוקרתי ומעוצב
  - H2: מאפיינים מרכזיים של עיצוב פנים מודרני יוקרתי
  - H2: מדוע לבחור בעיצוב פנים מודרני יוקרתי?
  - H2: איך לבחור מעצב המתמחה בעיצוב מודרני יוקרתי?
  - H2: עיצוב פנים מודרני
  - H2: תכונות עיקריות של עיצוב פנים מודרני
  - H2: התאמת ריהוט ל- עיצוב פנים מודרני
  - H2: חשיבות התאורה בתוך עיצוב פנים מודרני
  - H2: פתרונות אחסון ל עיצוב פנים מודרני
  - H2: עיצוב דירה מודרנית
  - H2: המאפיינים הבולטים של עיצוב דירה מודרנית
    - H3: יתרונות בעיצוב דירה מודרנית
    - H3: תאורה כחלק מרכזי בעיצוב דירה מודרנית
    - H3: שילוב קיימות וטבע
    - H3: פתרונות אחסון מתקדמים
  - H2: המובילים בעיצוב דירות מודרניות
    - H3: מדיניות הפרטיות

### #8 https://www.keinan-arch.com/project_type/עיצוב-פנים/עיצוב-דירות/

- Title: עיצוב דירות | עיצוב פנים לדירה עם מעצבי פנים מומחים - קינן אדריכלים
- Words: 633 · H2: 4 · H3: 0 · price mentions: 0 · schema: Answer, BreadcrumbList, CollectionPage, EntryPoint, FAQPage, ImageObject, ListItem, Organization, PropertyValueSpecification, Question
- Tools: FAQPage schema
- File: `competitor-pages/https_www_keinan_arch_com_project_type__6b0ab3.json`

- H1: עיצוב דירות
  - H2: עיצוב דירה בהתאם לצורך הייחודי של הלקוח
  - H2: עיצוב דירות – האם כדאי לנסות לעשות את זה לבד?
  - H2: איך תמצאו משרד שיתן הרבה מרחב לרצון של הלקוח?
  - H2: עיצוב דירות לכל מטרה – מה חשוב לדעת?

## עיצוב פנים

### #1 https://he.wikipedia.org/wiki/עיצוב_פנים

- Title: עיצוב פנים – ויקיפדיה
- Words: 739 · H2: 7 · H3: 0 · price mentions: 0 · schema: Article, ImageObject, Organization
- Tools: HTML tables x3
- File: `competitor-pages/https_he_wikipedia_org_wiki__0a5aac.json`

  - H2: תוכן עניינים
- H1: עיצוב פנים
  - H2: רקע
  - H2: בישראל
  - H2: שילוב הפנג שווי בעיצוב
  - H2: ראו גם
  - H2: קישורים חיצוניים
  - H2: הערות שוליים

### #2 https://nhdesign.co.il/

- Title: מעצב פנים ניצן הורוביץ - עיצוב פנים דירות יוקרה | עיצוב בתי יוקרה
- Words: 1,017 · H2: 12 · H3: 3 · price mentions: 0 · schema: Answer, BreadcrumbList, EntryPoint, FAQPage, ImageObject, ListItem, Organization, PropertyValueSpecification, Question, ReadAction
- Tools: FAQPage schema; gallery/slider
- File: `competitor-pages/https_nhdesign_co_il__ec1cfb.json`

- H1: מעצב הפנים ניצן הורוביץ
  - H2: הקו שמפריד
  - H2: בין בית לאמנות
  - H2: מעצבים חוויות מרחב ייחודיות תוך שילוב יצירתיות, פונקציונליות ודיוק בכל פרט ופרט.
  - H2: צילום: יאיר גלזר לחברת נאנו
  - H2: מה אנחנו עושים
  - H2: מה אנחנו עושים
    - H3: עיצוב פנים
    - H3: עיצוב מסחרי
    - H3: אדריכלות
  - H2: מה אנחנו עושים
  - H2: עיצוב פנים
  - H2: עיצוב פנים מסחרי
  - H2: אדריכלות
  - H2: אנחנו בסושיאל
  - H2: "יחד ולחוד"

### #3 https://www.bvd.co.il/

- Title: בניין ודיור | המגזין המוביל לאדריכלות, עיצוב פנים, עיצוב הבית
- Words: 1,327 · H2: 17 · H3: 38 · price mentions: 0 · schema: Answer, BreadcrumbList, EntryPoint, ImageObject, ListItem, Organization, PropertyValueSpecification, Question, ReadAction, SearchAction
- Tools: gallery/slider
- File: `competitor-pages/https_www_bvd_co_il__980d27.json`

- H1: בניין ודיור | המגזין המוביל לאדריכלות, עיצוב פנים, עיצוב הבית
  - H2: בניין ודיור מגזין עיצוב פנים – הכתבות האחרונות שלנו
  - H2: מימי לוזון חושפת את הקליניקה לטיפוח העור בתל אביב
  - H2: חופשה במרחק נגיעה: הבית באבן יהודה שמרגיש כמו ריזורט פרטי
  - H2: DESIGN WEEK TEL AVIV 2026
  - H2: מבזקי חדשות ועיצוב
  - H2: מדריכים
  - H2: המדריך לבחירת כיריים
  - H2: המדריך לעיצוב בסגנון מודרני
  - H2: המדריך לעיצוב חדר רחצה
  - H2: כל הטרנדים בשטיחים לבית
    - H3: עיצוב מודרני
    - H3: עיצוב כפרי
    - H3: עיצוב נורדי
    - H3: עיצוב בוהו שיק
    - H3: עיצוב תעשייתי
    - H3: עיצוב קלאסי
  - H2: כל אזור בבית והעיצוב שלו
    - H3: עיצוב מטבחים
    - H3: עיצוב סלונים
    - H3: עיצוב חדרי שינה
    - H3: עיצוב חדרי ילדים
    - H3: עיצוב חדרי אמבטיה
    - H3: עיצוב חדרי עבודה
    - H3: עיצוב גינות
    - H3: עיצוב מרפסות
    - H3: עיצוב כניסות
    - H3: עיצוב פינות אוכל
  - H2: עיצוב לעסקים
    - H3: עיצוב משרדים
    - H3: עיצוב מקומות בילוי ופנאי
    - H3: עיצוב מבנים ציבוריים
  - H2: מעצבי פנים ואדריכלים מומלצים
    - H3: שמחה עזרן
    - H3: שרי בר-נע גבעון
    - H3: הדר דור Dordesign
    - H3: ניצן בן משה
    - H3: קורל אברהם אדריכלות ועיצוב פנים
    - H3: אניה בוניאק סטודיו 18
  - H2: ספקים מומלצים לעיצוב הבית
    - H3: ART - גלריה לריהוט
    - H3: בית ישפאר- Elica
    - H3: דה דיטריש | De Dietrich
    - H3: ALUG
    - H3: ליוולו – Livelo
    - H3: חגית סער
  - H2: עיצוב פנים - שאלות ותשובות
    - H3: עיצוב פנים
    - H3: איך בוחרים סגנון לעיצוב הבית?
    - H3: מה התפקיד של מעצב פנים ולמה חשוב להיעזר בו?
    - H3: מהם הלבטים המרכזיים בעיצוב כל חלל בבית?
    - H3: איך בוחרים מעצב פנים?
    - H3: מה ההבדל בין עיצוב פנים להום סטיילינג?
    - H3: איזה טיפים אסור לפספס לפני שיפוץ דירה או עיצוב הבית?

### #4 https://www.pnim.co.il/

- Title: PNIM | מגזין עיצוב פנים ואדריכלות בישראל
- Words: 151 · H2: 3 · H3: 19 · price mentions: 0 · schema: BreadcrumbList, EntryPoint, ImageObject, ListItem, PropertyValueSpecification, ReadAction, SearchAction, WebPage, WebSite
- Tools: gallery/slider
- File: `competitor-pages/https_www_pnim_co_il__60bf61.json`

  - H2: הפוסטים האחרונים
  - H2: מעצבי פנים
    - H3: לאתר המעצבת
    - H3: לאתר המעצבת
    - H3: לאינסטגרם של האדריכליות
    - H3: לאתר המעצבת
    - H3: לאתר המעצבת
    - H3: לאתר המעצבת
    - H3: לאתר המעצבת
    - H3: לאתר המעצבת
    - H3: לאתר המעצבת
    - H3: לאתר המעצבת
    - H3: לאתר המעצבת
    - H3: לאתר המעצבת
    - H3: לאתר הסטודיו
    - H3: לאתר המעצבת
    - H3: לאתר המעצבת
    - H3: לאתר המעצבת
    - H3: לאתר הסטודיו
    - H3: לאתר המעצבת
    - H3: לאפשרויות הפרסום במגזין
  - H2: Pnim INSTAGRAM

### #5 https://www.design-inbal.co.il/

- Title: עיצוב פנים ואדריכלות [פרוייקטים 2026] מעצבת פנים ענבל ברקוביץ
- Words: 407 · H2: 3 · H3: 3 · price mentions: 0 · schema: ContactPoint, HomeAndConstructionBusiness, LocalBusiness, OpeningHoursSpecification, PostalAddress
- Tools: video embed x1
- File: `competitor-pages/https_www_design_inbal_co_il__99000b.json`

- H1: עיצוב פנים ענבל ברקוביץ
  - H2: הבתים היפים בישראל - עם ענבל ברקוביץ
  - H2: עיצוב פנים בהתאמה אישית
  - H2: שלבי ביצוע – עיצוב פנים
    - H3: פרוייקטים נבחרים
    - H3: כל בית מקבל חותם משלו
    - H3: המומחיות של ענבל ברקוביץ

### #6 https://netalinoy.com/

- Title: Neta-li & Tal Noy - עיצוב פנים ואדריכלות ברמה מתקדמת
- Words: 133 · H2: 1 · H3: 1 · price mentions: 0 · schema: BreadcrumbList, EntryPoint, ImageObject, ListItem, Organization, PropertyValueSpecification, ReadAction, SearchAction, WebPage, WebSite
- Tools: video embed x4; iframes: netalinoy.com; gallery/slider
- File: `competitor-pages/https_netalinoy_com__b93556.json`

- H1: אדריכלות | עיצוב פנים | ניהול פרויקטים
  - H2: פרויקטים נבחרים
    - H3: מדיניות הפרטיות

### #7 https://www.dordesign.co.il/

- Title: מעצבת פנים הדר דור (Dordesign) – עיצוב פנים מרהיב, מעל 20 שנות ניסיון
- Words: 922 · H2: 9 · H3: 12 · price mentions: 0 · schema: Article, BreadcrumbList, CreativeWork, EntryPoint, GeoCoordinates, ImageObject, ListItem, Offer, Organization, Person
- Tools: HTML tables x1; gallery/slider
- File: `competitor-pages/https_www_dordesign_co_il__c9c3c7.json`

- H1: מעצבת פנים הדר דור - Dordesign
  - H2: עיצוב פנים לבתים פרטיים, פנטהאוזים ודירות - תכנון מקצועי ועיצוב מרהיב
  - H2: כיצד לבחור מעצבת פנים ואיך עובדים איתה?
  - H2: פרויקטים נבחרים
    - H3: לפני אחרי בעיצוב פנים
  - H2: מדוע לבחור בי בתור מעצבת פנים שלכם?
  - H2: תקשורת ופרסום
    - H3: זכייה בפרס חביבת הקהל
    - H3: הדר דור בתכנית הבוקר
    - H3: הדר דור במגזין בניין ודיור
    - H3: הדר דור בפרסומת של פנדור
    - H3: הדר דור במגזין לאשה
    - H3: הדר דור בערוץ החיים הטובים
  - H2: לקוחות ממליצים
    - H3: המלצות נוספות >>
  - H2: קטגוריות עיצוב פנים
    - H3: עיצוב בתים
    - H3: עיצוב פנטהאוזים
    - H3: עיצוב דירות
    - H3: עיצוב משרדים ומרפאות
  - H2: תהליך העבודה בסטודיו — איך אנחנו מובילים אתכם לעיצוב מושלם
  - H2: תהליך העבודה בסטודיו — איך אנחנו מובילים אתכם לעיצוב מושלם

### #8 https://www.openu.ac.il/diploma/diploma-13_1.html

- Title: המרכז ללימודי עיצוב פנים | דיפלומה
- Words: 1,283 · H2: 10 · H3: 23 · price mentions: 0 · schema: none
- Tools: calculator-like inputs (4 inputs, 0 sliders, 3 selects); gallery/slider
- File: `competitor-pages/https_www_openu_ac_il_diploma_diploma_13_1_html_36017d.json`

- H1: המרכז ללימודי עיצוב פנים בדיפלומה
  - H2: שני מסלולי לימוד בעיצוב פנים, הום סטיילינג ותכנון חללים במקום אחד
  - H2: ללמוד עיצוב במקום שמחבר בין השראה, ידע מקצועי וכלים עדכניים
  - H2: שני מסלולי לימוד בעולם עיצוב הפנים
    - H3: לימודי עיצוב ותכנון פנים
    - H3: קורס הום סטיילינג בשילוב בינה מלאכותית
  - H2: למה ללמוד אצלנו?
  - H2: עבודות הגמר של הסטודנטים שלנו
  - H2: נבחרת המרצים שלנו
    - H3: אדריכלית איריס לניר
    - H3: דניאל גולדברג
    - H3: איילה כהן
    - H3: כנרת צידון
    - H3: יעל סימנר
    - H3: זיו שוורץ
    - H3: מיכל זגגי
    - H3: איריס בנדו
    - H3: יעקב גולדמן
    - H3: מירי שילה
    - H3: רונית גולן
    - H3: עירית אביר
    - H3: דייבה טייץ
  - H2: קורסים והכשרות לחברות ולארגונים
    - H3: מודל העבודה המדויק שלנו
    - H3: תכנון
    - H3: ביצוע
    - H3: תוצאה
    - H3: בקרה ולמידה
  - H2: ארגונים וחברות שכבר בחרו ללמוד איתנו
  - H2: שאלות שיעזרו לכם לבחור מסלול
  - H2: רוצים להעמיק בעולם עיצוב הפנים?
    - H3: דיפלומה
    - H3: יצירת קשר
    - H3: קורסים בדיפלומה

## מעצבת פנים

### #1 https://www.design-inbal.co.il/

- Title: עיצוב פנים ואדריכלות [פרוייקטים 2026] מעצבת פנים ענבל ברקוביץ
- Words: 407 · H2: 3 · H3: 3 · price mentions: 0 · schema: ContactPoint, HomeAndConstructionBusiness, LocalBusiness, OpeningHoursSpecification, PostalAddress
- Tools: video embed x1
- File: `competitor-pages/https_www_design_inbal_co_il__99000b.json`

- H1: עיצוב פנים ענבל ברקוביץ
  - H2: הבתים היפים בישראל - עם ענבל ברקוביץ
  - H2: עיצוב פנים בהתאמה אישית
  - H2: שלבי ביצוע – עיצוב פנים
    - H3: פרוייקטים נבחרים
    - H3: כל בית מקבל חותם משלו
    - H3: המומחיות של ענבל ברקוביץ

### #2 https://www.yifatdesign.co.il/

- Title: יפעת ירושלמי - מעצבת פנים המתמחה בעיצוב פנים יוקרתי
- Words: 1,851 · H2: 11 · H3: 12 · price mentions: 1 · schema: BreadcrumbList, EntryPoint, ImageObject, ListItem, Organization, PropertyValueSpecification, ReadAction, SearchAction, WebPage, WebSite
- Tools: calculator-like inputs (5 inputs, 0 sliders, 0 selects); gallery/slider
- File: `competitor-pages/https_www_yifatdesign_co_il__4f3f25.json`

    - H3: יפעת ירושלמי בעלת סטודיו לתכנון ועיצוב פנים לפרטי ועסקי.
    - H3: א ו ד ו ת י
  - H2: עיצוב דירות קטנות
    - H3: יפעת ירושלמי בעלת סטודיו לתכנון ועיצוב פנים לפרטי ועסקי.
  - H2: עיצוב דירות קטנות
  - H2: פרוייקטים נבחרים
    - H3: עיצוב דירות ועיצוב בתים פרטיים
    - H3: תכנון ועיצוב משרדים
    - H3: תכנון ועיצוב לובאים
    - H3: עיצוב חללים
    - H3: עיצוב דירות ועיצוב בתים פרטיים
  - H2: פרוייקטים נבחרים
    - H3: תכנון ועיצוב משרדים
    - H3: עיצוב חדרים
    - H3: תכנון ועיצוב לובאים
  - H2: שרותי המשרד
  - H2: לקוחות ממליצים
  - H2: מאמרים
- H1: מעצבת פנים לעיצוב יוקרתי
    - H3: תהליך העבודה לבית שלכם
  - H2: שלח מייל
  - H2: פגישת יעוץ

### #3 https://www.midrag.co.il/Content/SectorPortal/67

- Title: מעצבות פנים מומלצות - 4,500 חוות דעת באתר מידרג
- Words: 2,456 · H2: 12 · H3: 77 · price mentions: 2 · schema: none
- Tools: video embed x7; gallery/slider
- File: `competitor-pages/https_www_midrag_co_il_Content_SectorPortal_67_4dc4ac.json`

- H1: מעצבות פנים מומלצות - 4,500 חוות דעת באתר מידרג
  - H2: מעצבי פנים מומלצים
  - H2: חוות דעת אחרונות על מעצבי פנים מומלצים
    - H3: עיצוב פנים למקלחת, שירותים וחלקים נוספים בבית.
    - H3: פגישת ייעוץ לעיצוב פנים של שני חדרי ילדים קטנים.
    - H3: תכנון ועיצוב שיפוץ קומה שנייה, כולל תוכניות בנייה מסודרות לשני חדרים, שני חדרי אמבטיה ומבואה. מעקב לאחר כל התהליכים, ליווי לבחירת אנשי מקצוע, קרמיקות ועזרה בעיצוב.
    - H3: עיצוב פנים של מטבח ותכנון תאורה בדירה חדשה.
    - H3: עיצוב פנים לדירה חדשה מקבלן שכלל תכנון הדירה מהיסודות, הזזת קירות, עיצוב מטבח, בחירת ריצוף ואביזרים לבית.
    - H3: ייעוץ בנושא עיצוב פנים לקומה בבית פרטי הכוללת סלון, מטבח, שלושה חדרי שירותים ושני חדרי אמבטיה.
    - H3: עיצוב בית חדש כולל תכנון עיצוב ראשוני וליווי במפגשים עם ספקים ובעלי מקצוע.
    - H3: ליווי, תכנון ועיצוב של דירה בת שלושה חדרים שכללה תכנון תשתיות מיוחדות של אינסטלציה וחשמל.
    - H3: ייעוץ על מה להוסיף בדירה חדשה וליווי קבלן.
    - H3: תכנון לובי של בניין מגורים ישן, כולל הדמיה עם ויטרינות חדשות, ציפוי חדש, רצפה חדשה ותאורה חדשה.
  - H2: הום סטיילינג
  - H2: חוות דעת אחרונות על הום סטיילינג
    - H3: ייעוץ להלבשת הבית וליווי ברכישת ריהוט לבית באיקאה.
    - H3: שירותי שיפוץ, הום סטיילינג, נגרות ותאורה בדירת קבלן בגודל מאה מטר.
    - H3: ייעוץ על תאורה בבית.
    - H3: הום סטיילינג למטבח ולחדר רחצה.
    - H3: הום סטיילינג לחדרי שינה וסלון בבית פרטי.
    - H3: הום סטיילינג לדירה בגודל כ 120 מ"ר.
    - H3: הום סטיילינג לשני בתים פרטיים בחללים המרכזיים בבית.
    - H3: פגישת ייעוץ לעיצוב דירה בת שלושה חדרים שכוללת חדר עבודה.
    - H3: הום סטיילינג לדירה בגודל כ20 מ"ר.
    - H3: הום סטיילינג למשרד שבעה חדרים בגודל 100 מ"ר בתהליך שיפוץ.
  - H2: עיצוב מטבחים
  - H2: שיטת הדירוג של מידרג
  - H2: תמונות של עיצוב פנים מהשטח
  - H2: מאמרים בתחום
    - H3: מעצבי פנים
    - H3: מעצבי פנים מומלצים
    - H3: עיצוב סלון
    - H3: דוגמא להצעת מחיר לעיצוב פנים
    - H3: עיצוב מטבחים
    - H3: עיצוב דירת קבלן
    - H3: עיצוב דירה קטנה
    - H3: הום סטיילינג - מחירים
    - H3: עיצוב פנים מודרני
    - H3: עיצוב סלון נורדי
  - H2: סרטונים בתחום
  - H2: מעצבות פנים עונות
    - H3: שטיח מומלץ לחדר ילדים
    - H3: עור אמיתי או דמוי עור?
    - H3: אור לבן או צהוב?
  - H2: מידרג עונים
    - H3: מה זה עיצוב נורדי?
    - H3: מה ההבדל בין עיצוב פנים והום סטיילינג?
    - H3: מה זה הום סטיילינג?
    - H3: מה זה בוהו שיק?
    - H3: מה זה סגנון אקלקטי?
    - H3: מה זה לומן?
    - H3: איך מעצבים בית קטן?
    - H3: איך לעצב מרפסת קטנה?
    - H3: איך לעצב סלון קטן?
    - H3: גובה כסא בר
    - H3: רוחב כסא בר
    - H3: גובה כסא סטנדרטי
    - H3: מרחק בין כיור לכיריים
    - H3: מרחק בין שולחן אוכל לקיר
    - H3: גובה דלפק בר
    - H3: גובה ספה סטנדרטי
    - H3: גובה מנורה מעל שולחן אוכל
    - H3: גובה שולחן בר למטבח
    - H3: מרחק בין ספה לטלוויזיה
    - H3: רוחב שולחן אוכל סטנדרטי
    - H3: באיזה גובה תולים תמונה?
    - H3: רוחב שולחן בר
    - H3: קוטר שולחן עגול
    - H3: מה זה שטיח שאגי
    - H3: מה זה ספת שזלונג?
- ... 20 more headings in the JSON file

### #4 https://www.instagram.com/sharondaviddesigner/?hl=he

- Title: Instagram
- Words: 1 · H2: 0 · H3: 0 · price mentions: 0 · schema: none
- Tools: none detected
- File: `competitor-pages/https_www_instagram_com_sharondaviddesigner_hl_he_d6d358.json`

### #5 https://www.chayaorzel.co.il/

- Title: חיה אורצל מעצבת פנים - עיצוב פנים לדירות ולעסקים
- Words: 1,406 · H2: 9 · H3: 4 · price mentions: 0 · schema: BreadcrumbList, EntryPoint, ImageObject, ListItem, Organization, PropertyValueSpecification, ReadAction, SearchAction, WebPage, WebSite
- Tools: gallery/slider
- File: `competitor-pages/https_www_chayaorzel_co_il__2981aa.json`

  - H2: עיצוב פנים
  - H2: נעים מאד! חיה אורצל.
  - H2: פרוייקטים נבחרים
    - H3: דירה בעיצוב מודרני קלאסי
    - H3: דירה בעיצוב מודרני חמים
    - H3: דופלקס בעיצוב יוקרתי
    - H3: דיור מוגן בית דקל תלפיות
  - H2: לקוחות ממליצים
  - H2: עיצוב ובניית אתר:
  - H2: לפני שאתם מתחילים לחשוב על לשבור קירות...
  - H2: השאירו לי שם, מייל וטלפון ואשלח לכם מדריך - מאחורי הקיר, שייתן לכם את כל המידע והטיפים לפני שאתם יוצאים למשימת עיצוב דירת חלומותיכם. ידע שווה כוח והמון כסף!

### #6 https://www.elamorgan.co.il/

- Title: מעצבת פנים עם סגנון יוקרתי והתאמה אישית - אלה מורגן עיצוב פנים
- Words: 84 · H2: 27 · H3: 28 · price mentions: 0 · schema: BreadcrumbList, EntryPoint, ImageObject, ListItem, Organization, PropertyValueSpecification, ReadAction, SearchAction, WebPage, WebSite
- Tools: iframes: www.elamorgan.co.il; gallery/slider
- File: `competitor-pages/https_www_elamorgan_co_il__c3a077.json`

  - H2: קצת עליי
    - H3: עיצוב פנים ועיצוב הבית
  - H2: עיצוב פנים עם אלה מורגן
    - H3: עיצוב פנים לכל כיס וסגנון
  - H2: עיצוב פנים בצפון
    - H3: עיצוב פנים בצפון לכל מטרה
  - H2: עיצוב פנים בחיפה
  - H2: מעצבת פנים בחיפה לכל דירה
  - H2: מעצבות פנים מומלצות
  - H2: מעצבות פנים מומלצות בישראל
  - H2: מעצבת פנים צפון
  - H2: מעצבת פנים מומלצת בצפון
    - H3: מעצבת פנים בצפון עם המלצות של לקוחות רבים
  - H2: מעצבת פנים בחיפה והקריות
    - H3: מעצבת פנים מקצועית באזור חיפה והקריות
  - H2: מעצבת פנים בקריות
    - H3: עיצוב פנים – איך זה מתבצע?
    - H3: מעצבת פנים בקריות עיצוב הבית מחייב מקצועיות
  - H2: עיצוב פנים
    - H3: עיצוב פנים מודרני או קלאסי בהתאמה אישית
    - H3: עיצוב פנים – איך התהליך מתבצע?
  - H2: מעצבת פנים מומלצת
  - H2: מעצבת פנים דירות קטנות או גדולות
    - H3: מעצבות פנים – איך לבחור?
    - H3: שירותי מעצבת פנים לעיצוב מושלם
  - H2: מעצבות פנים
    - H3: מעצבות פנים מובילות – עיצוב מקצועי ויצירתי
    - H3: כך בוחרים מעצבות פנים
  - H2: מעצבת פנים בחיפה
    - H3: מעצבת פנים בחיפה – איך התהליך עובד?
    - H3: אלה מורגן – מעצבת פנים בחיפה המלצות רבות
  - H2: מעצבת פנים בצפון
  - H2: אלה מורגן – מעצבת פנים בצפון הארץ
    - H3: איך בוחרים מעצבת פנים בצפון?
  - H2: מעצבת פנים מקצועית בצפון
  - H2: עיצוב פנים בחיפה והצפון
    - H3: למה חשוב לקבל שירותי עיצוב פנים מקצועיים בחיפה והקריות ?
    - H3: עיצוב פנים בחיפה – פרקטיות לצד מראה נאה
  - H2: עיצוב פנים מקצועי בחיפה
  - H2: עיצוב פנים בצפון הארץ
    - H3: חשיבות לעיצוב פנים לבית בצפון בצורה מקצועית
    - H3: עיצוב פנים בצפון – מתחשב בכל האלמנטים החשובים
    - H3: עיצוב פנים בצפון – לקבל אפקט נכון ומדויק
  - H2: מעצבת פנים בקריות
    - H3: מעצבת פנים באיזור הקריות
    - H3: כללים לעבודה מול מעצבת פנים בקריות
  - H2: מעצבת פנים קריות
  - H2: מעצבות פנים צפון
  - H2: אלה מורגן – מעצבת פנים מומלצת בצפון
    - H3: מהן שיטות העבודה של מעצבות פנים בצפון?
  - H2: עיצוב בתים בחיפה
    - H3: היתרונות בקבלת שירות עיצוב בתים חיצוני ופנימי
    - H3: עיצוב בתים בחיפה – שילוב של פונקציונאליות והרמוניה
    - H3: עיצוב פנים – עיצוב בתים בחיפה
    - H3: מדיניות הפרטיות

### #7 https://moranrozenberg.co.il/

- Title: מעצבת פנים | מורן רוזנברג מעצבת פנים לבתים בשלבי בנייה ושיפוץ
- Words: 1,928 · H2: 11 · H3: 0 · price mentions: 0 · schema: BreadcrumbList, EntryPoint, ImageObject, ListItem, Organization, PropertyValueSpecification, ReadAction, SearchAction, WebPage, WebSite
- Tools: gallery/slider
- File: `competitor-pages/https_moranrozenberg_co_il__f59dc0.json`

  - H2: תכנון ועיצוב פנים
  - H2: הום סטיילינג
  - H2: מסלולי ייעוץ
- H1: מורן רוזנברג, עיצוב פנים
  - H2: תכנון ועיצוב פנים
  - H2: הום סטיילינג
  - H2: מסלולי ייעוץ
  - H2: מוזמנים ליצור קשר 054-6966711

### #8 https://www.shiplus.co.il/בעלי-מקצוע-כלליים/מעצבי-פנים/תל-אביב-יפו/

- Title: מעצבי פנים בתל אביב: מעצבי פנים מומלצים בתל אביב והסביבה
- Words: 1,972 · H2: 22 · H3: 6 · price mentions: 0 · schema: BreadcrumbList, ListItem, WebPage
- Tools: calculator-like inputs (4 inputs, 0 sliders, 1 selects); gallery/slider
- File: `competitor-pages/https_www_shiplus_co_il__9d969b.json`

- H1: מעצבי פנים מומלצים בתל אביב
  - H2: חפשו מעצב/ת פנים בתל אביב בסגנון שלכם. התרשמו מפרוייקטים ומהמלצות של לקוחות קודמים ובחרו נכון.
  - H2: מעצב פנים בתל אביב, לא רק מוציא את החלומות שלכם לפועל, הוא גם נקודת מפתח בתהליך השיפוץ המורכב. מעצב הפנים יעזור לכם בבחירת בעלי המקצוע ובפיקוח על העבודה, במציאת חנויות מתאימות לבחירת החומרים והריהוט ואף ישיג עבורכם הנחות יחודיות.
  - H2: חפשו בעלי מקצוע
  - H2: אלכסיי וסרגיי מולוצ'ניק
  - H2: מירב סואד
  - H2: דניאל בן משה
  - H2: רינת ישראלי
  - H2: הודיה מילר
  - H2: מיכל אהרוני גובס
  - H2: רמי ימין
  - H2: עיצוב פנים בתל אביב
  - H2: מעצב פנים בתל אביב - מה בדיוק הוא עושה?
  - H2: מעצב פנים בת"א - שימוש בפלטת צבעים
  - H2: פגישה מקדימה לקראת עבודה עם מעצב או מעצבת פנים
  - H2: האם זה משתלם לשכור מעצב פנים בתל אביב?
  - H2: מעצב או מעצבת פנים בתל אביב: סיכום
  - H2: מעצבי פנים באזור תל אביב
  - H2: מעצבי פנים בכל הארץ
  - H2: מאמרים בנושא עיצוב פנים
    - H3: סגנונות לעיצוב הבית שכדאי להכיר - 2019
    - H3: סגנונות לעיצוב הבית שכדאי להכיר - 2019
    - H3: 5 טרנדים מובילים בתחום העיצוב לקיץ 2023
    - H3: 5 טרנדים מובילים בתחום העיצוב לקיץ 2023
    - H3: אפליקציות לעיצוב הבית - עזרים מומלצים לשיפוץ
    - H3: אפליקציות לעיצוב הבית - עזרים מומלצים לשיפוץ
  - H2: חפשו בעלי מקצוע
  - H2: מחירון עיצוב פנים
  - H2: בעלי מקצוע ב תל אביב

## מעצב פנים מחיר

### #1 https://www.midrag.co.il/Content/Price/15364

- Title: מעצבת פנים מחיר | כל המחירים של מעצבות פנים - במידרג
- Words: 1,952 · H2: 9 · H3: 7 · price mentions: 21 · schema: Answer, Article, FAQPage, ImageObject, Organization, Question
- Tools: FAQPage schema; gallery/slider
- File: `competitor-pages/https_www_midrag_co_il_Content_Price_15364_28e22c.json`

- H1: מעצבת פנים מחיר
  - H2: מעצבות פנים מומלצות
  - H2: מחיר פגישת ייעוץ עם מעצבת פנים
  - H2: מחיר מעצבת פנים
    - H3: פגישות וסקיצות
    - H3: תוכניות עבודה מפורטות
    - H3: הדמית תלת מימד
    - H3: כתב כמויות
    - H3: לווי לקניות
    - H3: ליווי בשטח
    - H3: הלבשת הבית
  - H2: מה משפיע על מחיר
  - H2: מתי משלמים למעצבת פנים?
  - H2: מעצבות פנים מומלצות
  - H2: שאלות נפוצות לדף זה
  - H2: אנשים שהתעניינו במעצבת פנים מחיר התעניינו גם בזה...
  - H2: טיפים ומחירים ב שיפוץ ועיצוב הבית

### #2 https://www.shimrit-design.co.il/interior-design-pricing-guide

- Title: כמה עולה מעצבת פנים? | שמרית אוחיון
- Words: 1,870 · H2: 10 · H3: 25 · price mentions: 7 · schema: Answer, BlogPosting, FAQPage, Person, Question, VideoObject
- Tools: FAQPage schema; gallery/slider
- File: `competitor-pages/https_www_shimrit_design_co_il_interior_design_pricing_guide_7d8935.json`

- H1: כמה עולה מעצבת פנים? המדריך המלא לאזור המרכז
  - H2: למה קשה לקבל מחיר מדויק מראש?
  - H2: כמה עולה כל שירות?
  - H2: 6 גורמים שקובעים את העלות הסופית
    - H3: גודל הדירה
    - H3: היקף השיפוץ
    - H3: רמת הגימור
    - H3: היקף הליווי
    - H3: מורכבות הפרויקט
    - H3: לוח הזמנים
  - H2: הם כבר עשו את זה
  - H2: מה כוללת עיצוב דירת קבלן?
  - H2: עם מעצבת פנים לעומת בלי מעצבת פנים
  - H2: מחיר עיצוב דירת קבלן – מה חשוב לקחת בחשבון?
  - H2: עוד שאלות על מחיר עיצוב פנים
    - H3: כמה עולה מעצבת פנים לשעה?
    - H3: כמה עולה מעצבת פנים לפרויקט שלם?
    - H3: האם שיחת הייעוץ הראשונה עולה כסף?
    - H3: האם כדאי לשכור מעצבת פנים לדירת קבלן?
    - H3: מה ההבדל בין הום סטיילינג לעיצוב פנים מלא?
    - H3: האם המחיר כולל את הריהוט והחומרים?
    - H3: כמה זמן לוקח פרויקט עיצוב?
    - H3: האם יש הבדל במחיר בין אזורי השירות (תל אביב, ראשון לציון, מודיעין, רחובות)?
    - H3: איך לדעת אם מחיר שקיבלתי מעצבת פנים סביר?
  - H2: קראו גם מאמרים קשורים
  - H2: רוצים לדעת כמה זה יעלה לכם?
- H1: מגזין עיצוב: השראה, טרנדים ורעיונות לבית שלכם
    - H3: תכנון תאורה למשרדים ולחללים מסחריים | שמרית אוחיון
    - H3: עיצוב פנים במודיעין – המדריך המלא | שמרית אוחיון
    - H3: פנג שוואי בבית: המדריך המלא לעיצוב פנים מלא באנרגיה | שמרית אוחיון
    - H3: שינויי דיירים בדירת קבלן – 5 טעויות שכדאי למנוע
    - H3: מודרני, כפרי או נורדי? כך תבחרו את סגנון העיצוב לבית שלכם
    - H3: הטרנדים החמים בעיצוב פנים לשנת 2026
    - H3: כמה עולה שיפוץ דירה? המדריך לתכנון תקציב והימנעות מחריגות
    - H3: תכנון תאורה לבית – המדריך המלא 2026 | שמרית אוחיון
    - H3: עיצוב דירת קבלן – תכנון וליווי מקצועי | שמרית אוחיון
    - H3: עיצוב סינרגי: איך להפוך את התמונות שלכם לחלק בלתי נפרד מהבית (ולא רק לקישוט)

### #3 https://studio-id.co.il/כמה-עולה-מעצבת-פנים/

Not fetched (login wall or blocked). Title from SERP: כמה עולה מעצבת פנים? 150-450 ₪ למ"ר (מחירון 2026)

### #4 https://meitalyaakov.co.il/interior-designer-cost-2026/

- Title: כמה עולה מעצבת פנים – מחירים ל-2026 | מיטל יעקב – מעצבת פנים
- Words: 1,128 · H2: 8 · H3: 6 · price mentions: 11 · schema: AdministrativeArea, Answer, Article, BreadcrumbList, CommentAction, EntryPoint, FAQPage, ImageObject, ListItem, OpeningHoursSpecification
- Tools: HTML tables x1; FAQPage schema; gallery/slider
- File: `competitor-pages/https_meitalyaakov_co_il_interior_designer_cost_2026__00bc32.json`

- H1: כמה עולה מעצבת פנים? מחירים שקופים ואמיתיים לשנת 2026
  - H2: שלושה מודלים של תמחור — וכיצד לדעת מה מתאים לכם
  - H2: מה מצפה לכם לפי סוג הפרויקט
  - H2: מה באמת מזיז את המחיר
  - H2: העלות האמיתית של "לעשות לבד"
  - H2: שאלות שכדאי לשאול לפני שחותמים
  - H2: שאלות נפוצות על מחיר מעצבת פנים
    - H3: כמה עולה לעצב ולרהט דירה, כולל הריהוט?
    - H3: כמה עולה ייעוץ לחלל אחד, למשל סלון?
    - H3: האם הדמיה של הבית כלולה במחיר?
    - H3: האם פיקוח באתר בזמן השיפוץ כלול?
    - H3: מה ההבדל במחיר בין שינויי דיירים לליווי מלא?
    - H3: מתי כדאי להתחיל לעבוד עם מעצבת כדי לא לשלם פעמיים?
  - H2: אז כמה עולה מעצבת פנים — בשורה תחתונה
  - H2: רוצים להתייעץ?

### #5 https://inandout.co.il/interior-design-cost/

- Title: כמה עולה עיצוב פנים? מחירון ותקציב 2026 | in and out
- Words: 1,589 · H2: 14 · H3: 23 · price mentions: 32 · schema: Article, BreadcrumbList, CommentAction, EntryPoint, ImageObject, ListItem, Person, PropertyValueSpecification, ReadAction, SearchAction
- Tools: calculator-like inputs (4 inputs, 0 sliders, 0 selects); gallery/slider
- File: `competitor-pages/https_inandout_co_il_interior_design_cost__b20862.json`

- H1: כמה עולה עיצוב פנים? מחירון מלא וסקירת תקציב 2026
  - H2: מה משפיע על מחיר עיצוב פנים?
    - H3: גודל וסוג הפרויקט
    - H3: היקף השירות והליווי
    - H3: ניסיון ומוניטין המעצב או המעצבת
    - H3: מיקום גיאוגרפי ואזור השירות
  - H2: מודלי תמחור נפוצים בעיצוב פנים
    - H3: תמחור לפי שעה
    - H3: תמחור לפי מ"ר
    - H3: תמחור פרויקטלי (מחיר קבוע)
    - H3: תמחור לפי אחוזים מעלות הביצוע
  - H2: כמה עולה עיצוב פנים לפי סוג פרויקט?
    - H3: עיצוב חדר בודד או הום סטיילינג
    - H3: עיצוב דירת 3-4 חדרים
    - H3: עיצוב בית פרטי או וילה
    - H3: עיצוב דירת קבלן ושינויי דיירים
  - H2: מה כולל שירות עיצוב פנים מלא?
    - H3: ביקור ראשוני, מדידות ותכנון מרחב
    - H3: לוח השראה, הדמיות תלת ממד וליווי רכש
    - H3: פיקוח באתר לאורך הביצוע
  - H2: איך לבחור מעצב פנים ולתכנן תקציב נכון?
    - H3: שאלות שכדאי לשאול לפני חתימה על חוזה
    - H3: טיפים לחיסכון בעלויות בלי לוותר על איכות
  - H2: לסיכום
  - H2: שאלות נפוצות על עיצוב פנים
  - H2: עוד מהמגזין
    - H3: עיצוב כניסה לבית: איך יוצרים רושם ראשוני מושלם?
    - H3: עיצוב בית מודרני – כל מה שצריך לדעת על סגנון ועקרונות
    - H3: עיצוב בוהו שיק: המדריך המלא לסגנון הבוהמי בבית
  - H2: משאלות
    - H3: הרשימה עדיין ריקה
  - H2: Live the In&Out Look
  - H2: מעוניינים לקבל הצעת מחיר?
  - H2: מה תרצו למצוא?

### #6 https://ultimaschool.co.il/magazine/כמה-עולה-לעצב-דירה-בשנת-2026-פירוט-מחירים-ב/

- Title: כמה עולה לעצב דירה בשנת 2026? פירוט מחירים בישראל - מכללת אולטימה
- Words: 1,395 · H2: 11 · H3: 8 · price mentions: 7 · schema: Answer, Article, BreadcrumbList, EntryPoint, FAQPage, ImageObject, ListItem, Organization, Person, PropertyValueSpecification
- Tools: calculator-like inputs (4 inputs, 0 sliders, 4 selects); HTML tables x1; FAQPage schema; gallery/slider
- File: `competitor-pages/https_ultimaschool_co_il_magazine_2026__913e35.json`

- H1: כמה עולה לעצב דירה בשנת 2026? פירוט מחירים בישראל
  - H2: חשוב להבין את העלויות לפני שמתחילים
  - H2: מהם הגורמים המשפיעים על מחיר עיצוב דירה?
  - H2: כמה עולה פגישת ייעוץ עם מעצב פנים?
  - H2: עלות עיצוב פנים לפי חדר או חלל
  - H2: כמה עולה ליווי מלא של מעצב פנים לעיצוב דירה?
  - H2: עלויות נוספות שכדאי לקחת בחשבון
  - H2: האם אפשר לעצב דירה בתקציב נמוך?
  - H2: איך לבחור מעצב פנים שמתאים לתקציב שלכם?
  - H2: לימודי עיצוב פנים – מכללת אולטימה
  - H2: שאלות ותשובות על עלויות עיצוב דירה
    - H3: כמה עולה מעצב פנים לדירת 4 חדרים?
    - H3: האם מחיר פגישת הייעוץ מקוזז אחר כך?
    - H3: מה ההבדל בין ליווי חלקי לליווי מלא של מעצב פנים?
    - H3: האם כדאי להשקיע במעצב פנים לשיפוץ קטן?
    - H3: כתבות נוספות
  - H2: רוצים להירשם ללימודים באולטימה?

### #7 https://www.facebook.com/groups/home4y/posts/3985757208359907/

Not fetched (login wall or blocked). Title from SERP: מנסה להבין עלויות... כמה עולה מעצב.ת פנים לשיפוץ בית 3 קומות, ...

### #8 https://mayakedem.com/מאמרים/כמה-עולה-עיצוב-פנים/

- Title: כמה עולה עיצוב פנים? פירוק מרכיבי העלות וניתוח כדאיות ההשקעה - מאיה קדם מעצבת פנים
- Words: 2,191 · H2: 10 · H3: 16 · price mentions: 4 · schema: Answer, Article, BreadcrumbList, Country, EntryPoint, FAQPage, ImageObject, ListItem, OpeningHoursSpecification, Person
- Tools: HTML tables x2; FAQPage schema; gallery/slider
- File: `competitor-pages/https_mayakedem_com__03d17e.json`

- H1: כמה עולה עיצוב פנים? המדריך המלא לתכנון התקציב (2026)
  - H2: מחירון עיצוב פנים: 5 הגורמים המרכזיים שקובעים את המחיר
    - H3: היקף ומורכבות הפרויקט (Scope of Work)
    - H3: רמת החומרים והגמרים (Finishes)
    - H3: ניסיון ומוניטין המעצב/ת
    - H3: מעטפת השירותים הנלווים
    - H3: מיקום גיאוגרפי ומגמות שוק
  - H2: איך משלמים? 4 מודלי התמחור הנפוצים בשוק
    - H3: תמחור לפי שעה (Hourly Rate)
    - H3: שכר טרחה גלובלי (Fixed Fee / Flat Rate)
    - H3: מקדמה ודמי רצינות (Retainer)
    - H3: החזרי הוצאות נלוות (Reimbursable Expenses)
  - H2: השוואה: עיצוב יוקרה (High-End) מול עיצוב בתקציב מוגבל
    - H3: מומחיות ורמת הליווי (Expertise & Service Level)
    - H3: מפרט החומרים (Materials Specification)
    - H3: התאמה אישית מול מוצרי מדף (Bespoke vs. Off-the-Shelf)
    - H3: טבלת השוואה מסכמת: יוקרה מול סטנדרט
  - H2: האם עיצוב פנים הוא השקעה משתלמת? ניתוח ROI
    - H3: 1. הערך הנדל"ני: השבחת הנכס (Resale Value)
    - H3: 2. הערך הפונקציונלי: מיצוי פוטנציאל החלל (Space Optimization)
    - H3: 3. הערך הפסיכולוגי: שיפור איכות החיים (Well-being)
  - H2: מחירון עיצוב פנים
  - H2: מה מחיר מעצבת פנים?
  - H2: מחירון עיצוב פנים 2024
  - H2: מחירון עיצוב פנים 2025
  - H2: מחירון עיצוב פנים 2026 - תחזית
  - H2: שאלות נפוצות

## ייעוץ עיצוב פנים מחיר

### #1 https://www.midrag.co.il/Content/Price/15364

- Title: מעצבת פנים מחיר | כל המחירים של מעצבות פנים - במידרג
- Words: 1,952 · H2: 9 · H3: 7 · price mentions: 21 · schema: Answer, Article, FAQPage, ImageObject, Organization, Question
- Tools: FAQPage schema; gallery/slider
- File: `competitor-pages/https_www_midrag_co_il_Content_Price_15364_28e22c.json`

- H1: מעצבת פנים מחיר
  - H2: מעצבות פנים מומלצות
  - H2: מחיר פגישת ייעוץ עם מעצבת פנים
  - H2: מחיר מעצבת פנים
    - H3: פגישות וסקיצות
    - H3: תוכניות עבודה מפורטות
    - H3: הדמית תלת מימד
    - H3: כתב כמויות
    - H3: לווי לקניות
    - H3: ליווי בשטח
    - H3: הלבשת הבית
  - H2: מה משפיע על מחיר
  - H2: מתי משלמים למעצבת פנים?
  - H2: מעצבות פנים מומלצות
  - H2: שאלות נפוצות לדף זה
  - H2: אנשים שהתעניינו במעצבת פנים מחיר התעניינו גם בזה...
  - H2: טיפים ומחירים ב שיפוץ ועיצוב הבית

### #2 https://www.goldistudio.com/עיצוב-פנים-מחיר/

- Title: מחירון עיצוב פנים | עיצוב פנים מחיר - אלון גולדמן
- Words: 728 · H2: 9 · H3: 0 · price mentions: 4 · schema: ImageObject, Organization, ReadAction, SearchAction, WebPage, WebSite
- Tools: gallery/slider
- File: `competitor-pages/https_www_goldistudio_com__bacd6e.json`

- H1: מחירון עיצוב פנים | עיצוב פנים מחיר
  - H2: עיצוב פנים – היום לעומת פעם
  - H2: מה זה בעצם עיצוב פנים?
  - H2: מחירון עיצוב פנים
  - H2: מחיר עיצוב פנים עם אלון גולדמן
  - H2: לסיכום
  - H2: “אני שונא חופשות. אם אתה יכול לבנות בניינים, למה לשבת על שפת-הים?”
  - H2: האדריכל האמריקאי פיליפ ג’ונסון
  - H2: מעדיפים שאני אחזור אליכם?

### #3 https://www.shimrit-design.co.il/interior-design-pricing-guide

- Title: כמה עולה מעצבת פנים? | שמרית אוחיון
- Words: 1,870 · H2: 10 · H3: 25 · price mentions: 7 · schema: Answer, BlogPosting, FAQPage, Person, Question, VideoObject
- Tools: FAQPage schema; gallery/slider
- File: `competitor-pages/https_www_shimrit_design_co_il_interior_design_pricing_guide_7d8935.json`

- H1: כמה עולה מעצבת פנים? המדריך המלא לאזור המרכז
  - H2: למה קשה לקבל מחיר מדויק מראש?
  - H2: כמה עולה כל שירות?
  - H2: 6 גורמים שקובעים את העלות הסופית
    - H3: גודל הדירה
    - H3: היקף השיפוץ
    - H3: רמת הגימור
    - H3: היקף הליווי
    - H3: מורכבות הפרויקט
    - H3: לוח הזמנים
  - H2: הם כבר עשו את זה
  - H2: מה כוללת עיצוב דירת קבלן?
  - H2: עם מעצבת פנים לעומת בלי מעצבת פנים
  - H2: מחיר עיצוב דירת קבלן – מה חשוב לקחת בחשבון?
  - H2: עוד שאלות על מחיר עיצוב פנים
    - H3: כמה עולה מעצבת פנים לשעה?
    - H3: כמה עולה מעצבת פנים לפרויקט שלם?
    - H3: האם שיחת הייעוץ הראשונה עולה כסף?
    - H3: האם כדאי לשכור מעצבת פנים לדירת קבלן?
    - H3: מה ההבדל בין הום סטיילינג לעיצוב פנים מלא?
    - H3: האם המחיר כולל את הריהוט והחומרים?
    - H3: כמה זמן לוקח פרויקט עיצוב?
    - H3: האם יש הבדל במחיר בין אזורי השירות (תל אביב, ראשון לציון, מודיעין, רחובות)?
    - H3: איך לדעת אם מחיר שקיבלתי מעצבת פנים סביר?
  - H2: קראו גם מאמרים קשורים
  - H2: רוצים לדעת כמה זה יעלה לכם?
- H1: מגזין עיצוב: השראה, טרנדים ורעיונות לבית שלכם
    - H3: תכנון תאורה למשרדים ולחללים מסחריים | שמרית אוחיון
    - H3: עיצוב פנים במודיעין – המדריך המלא | שמרית אוחיון
    - H3: פנג שוואי בבית: המדריך המלא לעיצוב פנים מלא באנרגיה | שמרית אוחיון
    - H3: שינויי דיירים בדירת קבלן – 5 טעויות שכדאי למנוע
    - H3: מודרני, כפרי או נורדי? כך תבחרו את סגנון העיצוב לבית שלכם
    - H3: הטרנדים החמים בעיצוב פנים לשנת 2026
    - H3: כמה עולה שיפוץ דירה? המדריך לתכנון תקציב והימנעות מחריגות
    - H3: תכנון תאורה לבית – המדריך המלא 2026 | שמרית אוחיון
    - H3: עיצוב דירת קבלן – תכנון וליווי מקצועי | שמרית אוחיון
    - H3: עיצוב סינרגי: איך להפוך את התמונות שלכם לחלק בלתי נפרד מהבית (ולא רק לקישוט)

### #4 https://www.facebook.com/groups/2321376998117581/posts/3646063335648934/

Not fetched (login wall or blocked). Title from SERP: שלום לכולם, מה המחיר שנהוג לשלם על פגישת ייעוץ עם מעצבת ...

### #5 https://inandout.co.il/interior-design-cost/

- Title: כמה עולה עיצוב פנים? מחירון ותקציב 2026 | in and out
- Words: 1,589 · H2: 14 · H3: 23 · price mentions: 32 · schema: Article, BreadcrumbList, CommentAction, EntryPoint, ImageObject, ListItem, Person, PropertyValueSpecification, ReadAction, SearchAction
- Tools: calculator-like inputs (4 inputs, 0 sliders, 0 selects); gallery/slider
- File: `competitor-pages/https_inandout_co_il_interior_design_cost__b20862.json`

- H1: כמה עולה עיצוב פנים? מחירון מלא וסקירת תקציב 2026
  - H2: מה משפיע על מחיר עיצוב פנים?
    - H3: גודל וסוג הפרויקט
    - H3: היקף השירות והליווי
    - H3: ניסיון ומוניטין המעצב או המעצבת
    - H3: מיקום גיאוגרפי ואזור השירות
  - H2: מודלי תמחור נפוצים בעיצוב פנים
    - H3: תמחור לפי שעה
    - H3: תמחור לפי מ"ר
    - H3: תמחור פרויקטלי (מחיר קבוע)
    - H3: תמחור לפי אחוזים מעלות הביצוע
  - H2: כמה עולה עיצוב פנים לפי סוג פרויקט?
    - H3: עיצוב חדר בודד או הום סטיילינג
    - H3: עיצוב דירת 3-4 חדרים
    - H3: עיצוב בית פרטי או וילה
    - H3: עיצוב דירת קבלן ושינויי דיירים
  - H2: מה כולל שירות עיצוב פנים מלא?
    - H3: ביקור ראשוני, מדידות ותכנון מרחב
    - H3: לוח השראה, הדמיות תלת ממד וליווי רכש
    - H3: פיקוח באתר לאורך הביצוע
  - H2: איך לבחור מעצב פנים ולתכנן תקציב נכון?
    - H3: שאלות שכדאי לשאול לפני חתימה על חוזה
    - H3: טיפים לחיסכון בעלויות בלי לוותר על איכות
  - H2: לסיכום
  - H2: שאלות נפוצות על עיצוב פנים
  - H2: עוד מהמגזין
    - H3: עיצוב כניסה לבית: איך יוצרים רושם ראשוני מושלם?
    - H3: עיצוב בית מודרני – כל מה שצריך לדעת על סגנון ועקרונות
    - H3: עיצוב בוהו שיק: המדריך המלא לסגנון הבוהמי בבית
  - H2: משאלות
    - H3: הרשימה עדיין ריקה
  - H2: Live the In&Out Look
  - H2: מעוניינים לקבל הצעת מחיר?
  - H2: מה תרצו למצוא?

### #6 https://bethameatzvot.co.il/מחירון-אקסטרא/

- Title: מחירון - בית המעצבות
- Words: 229 · H2: 10 · H3: 3 · price mentions: 6 · schema: BreadcrumbList, EntryPoint, ListItem, PropertyValueSpecification, ReadAction, SearchAction, WebPage, WebSite
- Tools: gallery/slider
- File: `competitor-pages/https_bethameatzvot_co_il__a81285.json`

- H1: מחירון אקסטרא
  - H2: השירותים הנפוצים ביותר.
- H1: בבית המעצבות ניתן להזמין בתוספת תשלום מבחר שירותים בתחום:
  - H2: תכנון אדריכלי
  - H2: תוכניות עבודה
  - H2: עיצוב דירות קבלן בהתאמה אישית
  - H2: עיצוב פנים, תוכניות וליווי חלקי/מלא
  - H2: שינוי דיירים
  - H2: * המחירים לפני מע"מ
  - H2: * לעוד שירותים תנתן הצעת מחיר בהתאמה לדרישות
  - H2: מחירון אקסטרא
    - H3: דברו איתנו בוואצאפ
    - H3: שלחו לנו דוא"ל

### #7 https://ultimaschool.co.il/magazine/כמה-עולה-לעצב-דירה-בשנת-2026-פירוט-מחירים-ב/

- Title: כמה עולה לעצב דירה בשנת 2026? פירוט מחירים בישראל - מכללת אולטימה
- Words: 1,395 · H2: 11 · H3: 8 · price mentions: 7 · schema: Answer, Article, BreadcrumbList, EntryPoint, FAQPage, ImageObject, ListItem, Organization, Person, PropertyValueSpecification
- Tools: calculator-like inputs (4 inputs, 0 sliders, 4 selects); HTML tables x1; FAQPage schema; gallery/slider
- File: `competitor-pages/https_ultimaschool_co_il_magazine_2026__913e35.json`

- H1: כמה עולה לעצב דירה בשנת 2026? פירוט מחירים בישראל
  - H2: חשוב להבין את העלויות לפני שמתחילים
  - H2: מהם הגורמים המשפיעים על מחיר עיצוב דירה?
  - H2: כמה עולה פגישת ייעוץ עם מעצב פנים?
  - H2: עלות עיצוב פנים לפי חדר או חלל
  - H2: כמה עולה ליווי מלא של מעצב פנים לעיצוב דירה?
  - H2: עלויות נוספות שכדאי לקחת בחשבון
  - H2: האם אפשר לעצב דירה בתקציב נמוך?
  - H2: איך לבחור מעצב פנים שמתאים לתקציב שלכם?
  - H2: לימודי עיצוב פנים – מכללת אולטימה
  - H2: שאלות ותשובות על עלויות עיצוב דירה
    - H3: כמה עולה מעצב פנים לדירת 4 חדרים?
    - H3: האם מחיר פגישת הייעוץ מקוזז אחר כך?
    - H3: מה ההבדל בין ליווי חלקי לליווי מלא של מעצב פנים?
    - H3: האם כדאי להשקיע במעצב פנים לשיפוץ קטן?
    - H3: כתבות נוספות
  - H2: רוצים להירשם ללימודים באולטימה?

### #8 https://mayakedem.com/מאמרים/כמה-עולה-עיצוב-פנים/

- Title: כמה עולה עיצוב פנים? פירוק מרכיבי העלות וניתוח כדאיות ההשקעה - מאיה קדם מעצבת פנים
- Words: 2,191 · H2: 10 · H3: 16 · price mentions: 4 · schema: Answer, Article, BreadcrumbList, Country, EntryPoint, FAQPage, ImageObject, ListItem, OpeningHoursSpecification, Person
- Tools: HTML tables x2; FAQPage schema; gallery/slider
- File: `competitor-pages/https_mayakedem_com__03d17e.json`

- H1: כמה עולה עיצוב פנים? המדריך המלא לתכנון התקציב (2026)
  - H2: מחירון עיצוב פנים: 5 הגורמים המרכזיים שקובעים את המחיר
    - H3: היקף ומורכבות הפרויקט (Scope of Work)
    - H3: רמת החומרים והגמרים (Finishes)
    - H3: ניסיון ומוניטין המעצב/ת
    - H3: מעטפת השירותים הנלווים
    - H3: מיקום גיאוגרפי ומגמות שוק
  - H2: איך משלמים? 4 מודלי התמחור הנפוצים בשוק
    - H3: תמחור לפי שעה (Hourly Rate)
    - H3: שכר טרחה גלובלי (Fixed Fee / Flat Rate)
    - H3: מקדמה ודמי רצינות (Retainer)
    - H3: החזרי הוצאות נלוות (Reimbursable Expenses)
  - H2: השוואה: עיצוב יוקרה (High-End) מול עיצוב בתקציב מוגבל
    - H3: מומחיות ורמת הליווי (Expertise & Service Level)
    - H3: מפרט החומרים (Materials Specification)
    - H3: התאמה אישית מול מוצרי מדף (Bespoke vs. Off-the-Shelf)
    - H3: טבלת השוואה מסכמת: יוקרה מול סטנדרט
  - H2: האם עיצוב פנים הוא השקעה משתלמת? ניתוח ROI
    - H3: 1. הערך הנדל"ני: השבחת הנכס (Resale Value)
    - H3: 2. הערך הפונקציונלי: מיצוי פוטנציאל החלל (Space Optimization)
    - H3: 3. הערך הפסיכולוגי: שיפור איכות החיים (Well-being)
  - H2: מחירון עיצוב פנים
  - H2: מה מחיר מעצבת פנים?
  - H2: מחירון עיצוב פנים 2024
  - H2: מחירון עיצוב פנים 2025
  - H2: מחירון עיצוב פנים 2026 - תחזית
  - H2: שאלות נפוצות

### #9 https://www.ziratadrichalut.co.il/blog/one-time-design-consultation

- Title: ייעוץ עיצוב פנים חד-פעמי: מה מקבלים, כמה זה עולה ומתי זה מספיק | זירת האדריכלות
- Words: 647 · H2: 10 · H3: 0 · price mentions: 4 · schema: Answer, Article, BreadcrumbList, Country, FAQPage, ImageObject, ListItem, Offer, Organization, Question
- Tools: HTML tables x1; FAQPage schema
- File: `competitor-pages/https_www_ziratadrichalut_co_il_blog_one_time_design_consultation_8f0baa.json`

- H1: ייעוץ עיצוב פנים חד-פעמי: מה מקבלים, כמה זה עולה ומתי זה מספיק
  - H2: מה קורה בפגישת ייעוץ
  - H2: למי זה מתאים
  - H2: למי זה לא מספיק
  - H2: איך מפיקים את המרב מהפגישה
  - H2: כמה זה עולה לעומת האלטרנטיבות
  - H2: טעות נפוצה: ייעוץ כדי לחסוך מעצבת בשיפוץ
  - H2: איך מוצאים מעצבת לייעוץ
  - H2: שאלות נפוצות
  - H2: רוצים שנמצא לכם מעצבת פנים שמתאימה?
  - H2: עוד בנושא

## עיצוב דירה בתלת מימד

### #1 https://www.aihouse.com/he

- Title: AiHouse: תוכנת עיצוב וייצור פנים תלת-ממדית המונעת על ידי בינה מלאכותית
- Words: 915 · H2: 7 · H3: 5 · price mentions: 0 · schema: none
- Tools: gallery/slider
- File: `competitor-pages/https_www_aihouse_com_he_89ac72.json`

    - H3: תוכנת עיצוב בית מעשית המונעת על ידי בינה מלאכותית למקצוענים
    - H3: לוקח שנייה אחת: צור פריסות בסגנון שלך עם AI
  - H2: אמון על ידי 20,000 עסקים ברחבי העולם
  - H2: פתרון מקיף שמפשט את זרימת העבודה שלך
    - H3: פלטפורמת עיצוב מונעת בינה מלאכותית
    - H3: צור מרחבים תלת-ממדיים מרהיבים תוך דקות כדי להגביר מכירות
    - H3: JEGA Cloud Factory: אינטגרציה עיצוב-ייצור
  - H2: תוכנה מובילה בתעשייה להנעת העסק שלך
  - H2: חדשות
  - H2: הצטרף לרשת הגלובלית שלנו כדי למכור את פתרונות ה-SaaS המובילים
  - H2: ראה מדוע המשתמשים שלנו אוהבים את AiHouse
  - H2: נסו את AiHouse 5 Plus בחינם

### #2 https://studio-vida.co.il/הדמיות-תלת-מימד-לבתים/

- Title: סטודיו וידה | הדמיות תלת מימד לבתים ברמה הגבוהה ביותר
- Words: 1,818 · H2: 12 · H3: 40 · price mentions: 0 · schema: Answer, BreadcrumbList, ContactPoint, FAQPage, GeoCoordinates, ImageObject, ListItem, Organization, Place, PostalAddress
- Tools: FAQPage schema; gallery/slider
- File: `competitor-pages/https_studio_vida_co_il__864e7f.json`

- H1: הדמיות תלת מימד לבתים
  - H2: מהן הדמיות תלת מימד לבתים?
  - H2: סוגי ההדמיות שאנו מציעים
    - H3: הדמיות תלת מימד אדריכלות
    - H3: הדמיות עיצוב פנים
    - H3: הדמיות חוץ
  - H2: יתר ונות הדמיות תלת מימד לבתים
    - H3: שאלות ותשובות:
  - H2: מהן הדמיות תלת מימד לבתים?
  - H2: למה חשוב להשתמש בהדמיות תלת מימד בתהליך התכנון?
  - H2: האם הדמיות תלת מימד יכולות לעזור בשיווק ומכירת נכסים?
  - H2: שאלה: מה ההבדל בין הדמיות תלת מימד לתוכניות?
    - H3: שירותים נוספים
  - H2: עכשיו כשאתם כבר מכירים אותנו השאירו את פרטיכם ונחזור בהקדם
  - H2: שירותים
    - H3: סיור וירטואלי (VR)
    - H3: סרטון מוצר
    - H3: תכניות מכירה בדו-מימד ובתלת-מימד
    - H3: הדמיות עיצוב פנים
    - H3: בניית אתרים
    - H3: סיור וירטואלי של 360° בחלל
    - H3: סרטי אנימציה אדריכליים
    - H3: הדמיות חנות
    - H3: הדמיות רהיטים
    - H3: הדמיית חדר שינה
    - H3: הפקת הדמיות פנים וחוץ פוטו-ריאליסטיות
    - H3: הדמיות חוץ
    - H3: הדמיות תלת מימד לבתים
    - H3: הדמיות בית כנסת
    - H3: מיתוג נדלן
    - H3: הדמיות מוצר
    - H3: הדמיית חדרי אמבטיה
    - H3: הדמיות אדריכליות
    - H3: תוכניות מכר
    - H3: הדמיות פנים
  - H2: מאמרים
    - H3: תהליך מיתוג נדל”ן: מה חשוב לדעת לפני שמתחילים
    - H3: כיצד מסייעות הדמיות אדריכליות לפרויקטים מסחריים לשיפור תהליכי קבלת החלטות
    - H3: הדמיות חדר שינה: ליצור חלל מושלם
    - H3: מיתוג פרויקט מתחיל בלוגו נדלן מושלם
    - H3: למה בינה מלאכותית לא יכולה להחליף סטודיו להדמיות?
    - H3: בניית אתרים לעסקים קטנים
    - H3: איך הדמיות אדריכליות יכולות לשפר את תהליכי התכנון והבניה?
    - H3: הדמיות תלת מימד בתחום האדריכלות
    - H3: איך להשתמש בהדמיות כדי לשפר את השיווק של פרויקטים נדלן
    - H3: מיתוג בעסקים: איך מתחילים?
    - H3: כיצד אדריכלים משתמשים בהדמיות חוץ להבנת רעיונות מורכבים
    - H3: סטודיו וידה – הבחירה הנכונה
    - H3: הדמיה פוטוריאליסטית
    - H3: הדמיות נדלן
    - H3: מה זה הדמיות אדריכליות בתלת מימד?
  - H2: בואו נהיה בקשר

### #3 https://rollinom.com/he/what-is-a-virtual-tour-he/

- Title: עיצוב הבית בעזרת תוכנת הדמיה תלת מימד | רולינום
- Words: 389 · H2: 1 · H3: 0 · price mentions: 0 · schema: Article, BreadcrumbList, CommentAction, EntryPoint, ImageObject, ListItem, Organization, Person, ReadAction, SearchAction
- Tools: gallery/slider
- File: `competitor-pages/https_rollinom_com_he_what_is_a_virtual_tour_he__94547e.json`

- H1: עיצוב הבית בעזרת תוכנת הדמיה תלת מימד
  - H2: דף תשלום

### #4 https://www.homega3d.com/הדמיות-פנים/הדמיה-בית-פרטי/

- Title: הדמיה בית פרטי | Homega 3D - טכנולוגיות תלת מימד
- Words: 732 · H2: 7 · H3: 2 · price mentions: 1 · schema: BreadcrumbList, ImageObject, ListItem, ReadAction, SearchAction, WebPage, WebSite
- Tools: iframes: my.matterport.com; gallery/slider; 3D/planner embed
- File: `competitor-pages/https_www_homega3d_com__c7d5ab.json`

- H1: הדמיה בית פרטי
  - H2: הדמיה בית פרטי
  - H2: הדמיה בית פרטי
  - H2: הדמיות בית פרטי- בזכות עיצוב פנים
    - H3: רוצים לשווק נדל"ן- רק עם הדמיות אדריכליות
    - H3: מוכרים חיים לא דירה
  - H2: הדמיות 3D וVR
  - H2: תמונות HDR
  - H2: תכניות קומה ובניין
  - H2: למה לבחור ב HOMEGA 3D

### #5 https://realitech.co.il/3d-interior-design-visualization-guide/

- Title: הדמיית פנים מעוצבת: המדריך המלא לעיצוב הבית בתלת מימד (2026)
- Words: 3,088 · H2: 11 · H3: 18 · price mentions: 12 · schema: Answer, Article, BreadcrumbList, CommentAction, EntryPoint, FAQPage, ImageObject, ListItem, OpeningHoursSpecification, Person
- Tools: calculator-like inputs (4 inputs, 0 sliders, 0 selects); iframes: realitech.viewin360.co; FAQPage schema; gallery/slider
- File: `competitor-pages/https_realitech_co_il_3d_interior_design_visualization_guide__981560.json`

- H1: הדמיית פנים מעוצבת: המדריך המלא לעיצוב הבית בתלת מימד (2026)
  - H2: נקודות מפתח
  - H2: תוכן העניינים
  - H2: מהי הדמיית פנים מעוצבת ומדוע היא קריטית להצלחת הפרויקט?
    - H3: המחשת חלל ופרופורציות ללא ניחושים
    - H3: הפחתת מתחים וקבלת החלטות משותפת
  - H2: איך הדמיית פנים עוזרת בבחירת חומרים, תאורה וטקסטורות?
    - H3: דיוק בחומרי גמר וחיפויים
    - H3: תכנון תאורה חכם ופונקציונלי
  - H2: הדמיה פוטוריאליסטית מול סקיצה בדו-ממד: ההבדלים שחוסכים לכם כסף
    - H3: זיהוי כשלים תכנוניים מראש
    - H3: החזר השקעה (ROI) בבנייה פרטית
  - H2: שלב אחר שלב: איך להתכונן להפקת הדמיית פנים מושלמת?
    - H3: הכנת חומרי הגלם לסטודיו
    - H3: תהליך הפידבק והתיקונים
  - H2: הדמיות הפנים של Realitech: להפוך חזון למציאות מוחשית
    - H3: סיורי 360 וסרטונים: לקחת את ההדמיה צעד קדימה
    - H3: מקצועיות ללא פשרות במחיר נגיש
  - H2: הופכים תוכניות למציאות: הצעד הבא בבית החדש שלכם
  - H2: שאלות נפוצות
    - H3: כמה עולה הדמיית פנים מעוצבת ב-Realitech?
    - H3: כמה זמן לוקח להפיק הדמיית פנים פוטוריאליסטית?
    - H3: האם ניתן לבצע שינויים בעיצוב לאחר שההדמיה כבר מוכנה?
    - H3: אילו קבצים אני צריך לספק כדי להתחיל את העבודה מול הסטודיו?
    - H3: מה ההבדל בין הדמיית פנים לסרטון שיווק נדל"ן?
    - H3: האם ההדמיה כוללת גם שירותי עיצוב פנים או רק המחשה של תוכנית קיימת?
    - H3: האם הדמיית פנים מתאימה גם לשיפוץ של דירה קטנה?
    - H3: איך אני יכול לדעת שהחומרים בהדמיה ייראו בדיוק כמו במציאות?
  - H2: כתיבת תגובה לבטל
  - H2: קבלו הצעה לפרויקט שלכם

### #6 https://www.redesignai.co.il/blog/סטודיו-שרטוט-מתוכנית-דירה-לתלת-ממד

- Title: סטודיו שרטוט: מתוכנית דירה לתלת־ממד ולעיצוב הבית
- Words: 1,006 · H2: 10 · H3: 16 · price mentions: 0 · schema: none
- Tools: video embed x1
- File: `competitor-pages/https_www_redesignai_co_il_blog__4fdeb0.json`

    - H3: עוקבים ונהנים
- H1: סטודיו שרטוט: מתוכנית דירה לתלת־ממד ולעיצוב הבית
  - H2: מדריך לשימוש בסטודיו השרטוט של רידיזיין
  - H2: מתחילים מתוכנית הדירה
  - H2: רואים את החלוקה בתלת־ממד
  - H2: מלבישים את הבית בריהוט
  - H2: משנים, מנסים ומשווים
  - H2: מתלת־ממד להדמיה של החדר
  - H2: מדריך וידאו: לראות את העבודה בסטודיו
  - H2: מה כדאי להכין לפני שמתחילים?
  - H2: שאלות שעולות לפני ההתנסות
    - H3: אפשר להעלות צילום של התוכנית?
    - H3: חייבים לדעת לעבוד בתלת־ממד?
    - H3: האם כל ההדמיות זהות לתוכנית?
    - H3: איך מתחילים?
    - H3: רוצים לראות את הבית שלכם מעוצב מחדש?
  - H2: מאמרים נוספים שיעניינו אתכם
    - H3: עיצוב חדר שינה: רעיונות לחדר קטן והדמיות לפני ואחרי
    - H3: עיצוב חללים קטנים עם AI: רעיונות והדמיות לפני ואחרי
    - H3: AI בעיצוב פנים: מה זה באמת עושה ואיך מפיקים מזה תוצאה
    - H3: עיצוב משרד ביתי קטן: שולחן, תאורה ולפני ואחרי
    - H3: טרנדים בעיצוב פנים 2026: צבעים וחומרים שכדאי להכיר
    - H3: עיצוב הבית עם AI למתחילים: מתמונה לרשימת קניות
    - H3: צור קשר
    - H3: כלי AI
    - H3: בלוג
    - H3: אודות

### #7 https://www.saf.co.il/noa/prd_1510

- Title: הדמיות תלת מימד
- Words: 135 · H2: 0 · H3: 10 · price mentions: 0 · schema: none
- Tools: calculator-like inputs (6 inputs, 0 sliders, 0 selects); gallery/slider
- File: `competitor-pages/https_www_saf_co_il_noa_prd_1510_a15cb5.json`

- H1: הדמיות תלת מימד
    - H3: צור קשר
    - H3: מוצרים דומים
    - H3: קטגוריות
    - H3: נושאים קשורים
    - H3: השארו מעודכנים
    - H3: ClassRoom
    - H3: הורדות קבצים
    - H3: פורומים
    - H3: אינדקסים ורשימות
    - H3: אתר Saf

## תוכנה לעיצוב דירה

### #1 https://www.bvd.co.il/מעצבים-את-הבית-16-תוכנות-לעיצוב-הבית-שאת/

- Title: מעצבים את הבית? 16 תוכנות לעיצוב הבית שאתם צריכים להכיר ב 2024
- Words: 1,304 · H2: 39 · H3: 1 · price mentions: 0 · schema: Article, BreadcrumbList, CommentAction, EntryPoint, ImageObject, ListItem, Organization, Person, PropertyValueSpecification, ReadAction
- Tools: calculator-like inputs (8 inputs, 0 sliders, 1 selects); gallery/slider; 3D/planner embed
- File: `competitor-pages/https_www_bvd_co_il_16__a1c4dc.json`

- H1: מעצבים את הבית? 16 תוכנות לעיצוב הבית שאתם צריכים להכיר
  - H2: הדמיית תלת ממד של פינת אוכל וספרייה עמוסה בפריטים
  - H2: AutoCAD
  - H2: שרטוט תלת ממדי של מטבח
  - H2: SketchUp
  - H2: תלת ממד של שתי תוכניות האחת לפני והשנייה אחרי עיצוב מחדש
  - H2: Revit
  - H2: הדמייה שלחדר שינה עם קירות שקופים פתוחים לעיצוב החוץ שסביב הבית
  - H2: Photoshop
  - H2: הדמיה בשכבות וצבעים עזים של ירוק, זהב וצהוב
  - H2: ds Max
  - H2: הדמיה של חלל גדול ומורכב עם השפעת אור טבעי ומלאכותי
  - H2: Rhino
  - H2: הדמיה של חומר עשוי גלים בו מודגש הצבע והמרקם
  - H2: Architect
  - H2: הדמיה של מטבח כולל מכשירים
  - H2: InDesign
  - H2: הדמיה של סלון ומטבח ומדרגות לקומה עליונה
  - H2: Lumion
  - H2: הדמיה של חדר שינה ומסדרון שיוצא ממנו וממשיך לחלקים אחרים בבית
  - H2: Procreate
  - H2: הדמיה עם מרקמי חומרים, רהיטים ואקססוריז
  - H2: Planner5D
  - H2: הדמיה של חלל גדול והשפעת תאורת היום שחודרת פנימה דרך החלונות
  - H2: Home Designer Suite:
  - H2: הדמיה שמחזקת את תחושת המרחב כולל אפשרות לניצול הגובה
  - H2: Sweet Home 3D
  - H2: הדמיה של חומרים ומרקמים ליצירת לוח השראה
  - H2: RoomSketcher
  - H2: הדמית תלת ממד של לוח השראה עם מגוון של חומרים
  - H2: Live Interior 3D
  - H2: הדמיה תלת ממד של שילוב בין אלמנטים, חומרים וצבעים
  - H2: DreamPlan
  - H2: הדמית תלת ממד של חדר ילדים עם רהיטים וצעצועים
  - H2: לסיכום :
  - H2: הדמיית תלת ממד של קיר ירוק בשילוב סרגלי עץ אנכיים המשמשים כמעקה למדרגות
    - H3: כתיבת תגובה לבטל
  - H2: המדריך לעיצוב מטבח
  - H2: בין חומר, אור וטבע: ביתה הפרטי של תהילה גור ברמת פולג

### #3 https://www.ikea.com/addon-app/space/platform/latest/il/he/

- Title: IKEA
- Words: 1 · H2: 0 · H3: 0 · price mentions: 0 · schema: none
- Tools: none detected
- File: `competitor-pages/https_www_ikea_com_addon_app_space_platform_latest_il_he__fe503c.json`

### #4 https://www.facebook.com/groups/home4y/posts/3997816500487311/

Not fetched (login wall or blocked). Title from SERP: מחפשת אפליקציה לעיצוב הבית מדויקת עד כמה שאפשר אם אפשרות ...

### #6 https://www.redesignai.co.il/

- Title: רידיזיין AI - עיצוב פנים AI בעברית | עוזר אישי ללא עלות
- Words: 1,092 · H2: 11 · H3: 22 · price mentions: 3 · schema: Answer, FAQPage, Question
- Tools: calculator-like inputs (1 inputs, 1 sliders, 0 selects); FAQPage schema; gallery/slider
- File: `competitor-pages/https_www_redesignai_co_il__fcc36a.json`

    - H3: עוקבים ונהנים
- H1: הבית שלכם, מתחיל כאן.
  - H2: איזה סגנון מרגיש לכם אתם?
  - H2: מתוכנית על הנייר, למרחב שאפשר לגלות.
  - H2: עיצוב פנים AI, מהסלון ועד הגינה.
  - H2: אותו סלון. כיוון חדש.
  - H2: לא צריך לדעת לעצב. רק לדעת מה בא לכם לשנות.
    - H3: מעלים תמונה
    - H3: נותנים כיוון
    - H3: רואים אפשרות חדשה
  - H2: מה תרצו לעשות היום?
    - H3: לשנות. לשלב. לדייק.
    - H3: לראות את התוכנית מתעוררת
    - H3: אהבתם רהיט בתמונה?
  - H2: מגזין עיצוב נדל״ן של גלובס
    - H3: מציג את רידיזיין כזווית הישראלית של מהפכת העיצוב עם AI
  - H2: קרדיט ראשון להיכרות. מנוי לרעיונות הבאים.
    - H3: מתחילים להכיר
    - H3: מנוי חודשי
    - H3: פרו
  - H2: כמה דברים שכדאי לדעת.
  - H2: מדריכים לבית שלכם.
    - H3: סטודיו שרטוט: מתוכנית לתלת־ממד
    - H3: עיצוב חדר שינה
    - H3: עיצוב מטבח קטן
    - H3: עיצוב חדר אמבטיה
    - H3: עיצוב מרפסת פנטהאוז
    - H3: עיצוב משרד ביתי קטן
    - H3: עיצוב הבית עם AI למתחילים
  - H2: בואו לגלות מה הוא יכול להיות.
    - H3: צור קשר
    - H3: כלי AI
    - H3: בלוג
    - H3: אודות

### #7 https://genroom.io/he/blog/free-ai-room-design-tools

- Title: 5 כלי עיצוב חדרים AI חינמיים באמת (2026)
- Words: 2,002 · H2: 10 · H3: 44 · price mentions: 2 · schema: Answer, Article, BreadcrumbList, EntryPoint, FAQPage, ImageObject, ListItem, Offer, Organization, Question
- Tools: HTML tables x1; FAQPage schema; gallery/slider
- File: `competitor-pages/https_genroom_io_he_blog_free_ai_room_design_tools_d8d19a.json`

- H1: 5 כלי עיצוב חדרים בינה מלאכותית חינמיים מובילים ב-2026
  - H2: איך בדקנו
  - H2: 1. GenRoom — כלי עיצוב החדרים החינמי הטוב ביותר בכלל
    - H3: למה הוא מדורג ראשון
    - H3: מסלול חינמי
    - H3: חוזקות מרכזיות
    - H3: מגבלות
    - H3: מתאים ביותר עבור
  - H2: 2. RoomsGPT — הטוב ביותר לחקירה מהירה ללא הרשמה
    - H3: סקירה כללית
    - H3: מסלול חינמי
    - H3: חוזקות מרכזיות
    - H3: מגבלות
    - H3: מתאים ביותר עבור
  - H2: 3. Spacely AI — הטוב ביותר להיברידיות תוכנית קומה + AI
    - H3: סקירה כללית
    - H3: מסלול חינמי
    - H3: חוזקות מרכזיות
    - H3: מגבלות
    - H3: מתאים ביותר עבור
  - H2: 4. VisualGPT — הטוב ביותר לרינדורים בסגנון תלת-ממד
    - H3: סקירה כללית
    - H3: מסלול חינמי
    - H3: חוזקות מרכזיות
    - H3: מגבלות
    - H3: מתאים ביותר עבור
    - H3: צרו עיצוב פנים עם AI
  - H2: 5. InstantInterior AI — פערי האיכות הקטנים ביותר בין חינם לתשלום
    - H3: סקירה כללית
    - H3: מסלול חינמי
    - H3: חוזקות מרכזיות
    - H3: מגבלות
    - H3: מתאים ביותר עבור
  - H2: טבלת השוואה
  - H2: איך להפיק את המרב מכלי עיצוב חדרים חינמיים מבוססי AI
    - H3: 1. התחילו עם תמונות טובות
    - H3: 2. נסו סגנונות מרובים
    - H3: 3. השתמשו באותה תמונה בכלים שונים
    - H3: 4. שימו לב לפרופורציות
    - H3: 5. עברו לתשלום כשאתם מוכנים
  - H2: שאלות נפוצות (FAQ)
    - H3: האם הכלים האלה באמת חינמיים?
    - H3: האם עיצוב חדרים ב-AI יכול להחליף מעצב פנים אנושי?
    - H3: איזה כלי הכי טוב לעיצוב וירטואלי?
    - H3: האם הכלים האלה עובדים בנייד?
    - H3: מה לגבי פרטיות — האם התמונות שלי נשמרות?
  - H2: השורה התחתונה
    - H3: מאמרים קשורים
    - H3: צרו עיצוב פנים עם AI
    - H3: מוצר
    - H3: סוגי עיצוב
    - H3: רעיונות לעיצוב
    - H3: מקרי שימוש
    - H3: חברה
    - H3: תמיכה

### #8 https://www.shiplus.co.il/פורומים/עיצוב-פנים/19448.html

- Title: תוכנה לעיצוב פנים ללא מקצוענים - שיפוצים פלוס
- Words: 453 · H2: 3 · H3: 10 · price mentions: 0 · schema: BreadcrumbList, ListItem, WebPage
- Tools: gallery/slider
- File: `competitor-pages/https_www_shiplus_co_il_19448_html_4b5fd0.json`

- H1: תוכנה לעיצוב פנים ללא מקצוענים
  - H2: 2 תגובות
  - H2: מעצבי פנים בכל הארץ
  - H2: מאמרים בנושא עיצוב פנים
    - H3: סגנונות לעיצוב הבית שכדאי להכיר - 2019
    - H3: סגנונות לעיצוב הבית שכדאי להכיר - 2019
    - H3: 5 טרנדים מובילים בתחום העיצוב לקיץ 2023
    - H3: 5 טרנדים מובילים בתחום העיצוב לקיץ 2023
    - H3: אפליקציות לעיצוב הבית - עזרים מומלצים לשיפוץ
    - H3: אפליקציות לעיצוב הבית - עזרים מומלצים לשיפוץ
    - H3: טיפים בנושא עיצוב פנים
    - H3: הום סטיילינג - טיפ לחיסכון בעלויות
    - H3: פתרון עיצובי להסתרת ארון חשמל
    - H3: מה כדאי לדעת כשמדביקים פסיפס?

## עיצוב דירה חדשה מקבלן

### #1 https://netalinoy.com/project_cat/עיצוב-דירת-קבלן/

- Title: עיצוב דירת קבלן - נטע-לי וטל נוי - אדריכלות ועיצוב פנים ברמה מתקדמת
- Words: 778 · H2: 9 · H3: 3 · price mentions: 0 · schema: BreadcrumbList, CollectionPage, EntryPoint, ImageObject, ListItem, Organization, PropertyValueSpecification, SearchAction, WebSite
- Tools: iframes: netalinoy.com; gallery/slider
- File: `competitor-pages/https_netalinoy_com_project_cat__6e8210.json`

- H1: עיצוב דירת קבלן
  - H2: עיצוב דירת קבלן
  - H2: תהליך עיצוב דירת קבלן
  - H2: יתרונות בעיצוב דירת קבלן
  - H2: טיפים חשובים לעיצוב דירת קבלן
  - H2: בחירת המעצב המתאים בעיצוב דירת קבלן
  - H2: בחירת עיצוב אישי לדירה חדשה
  - H2: היתרונות בעיצוב דירה חדשה
  - H2: דגשים חשובים בעיצוב דירה חדשה מקבלן
    - H3: שימוש בטכנולוגיה מתקדמת
    - H3: כיצד להפוך דירה חדשה מקבלן לבית?
  - H2: עיצוב דירות יוקרה עם נטע-לי וטל נוי
    - H3: מדיניות הפרטיות

### #2 https://www.midrag.co.il/content/tip/3891

- Title: עיצוב דירת קבלן | איך לעצב דירה חדשה מקבלן? דוגמאות ותמונות ממעצבי פנים - במידרג
- Words: 2,574 · H2: 9 · H3: 28 · price mentions: 0 · schema: Article, ImageObject, Organization
- Tools: video embed x1; gallery/slider
- File: `competitor-pages/https_www_midrag_co_il_content_tip_3891_362f1f.json`

- H1: עיצוב דירת קבלן
  - H2: מעצבי ומעצבות פנים מומלצים ומומלצות באתר מידרג
  - H2: עיצוב דירת קבלן ביבנה הירוקה – העיצוב של נורית
    - H3: עיצוב הסלון בדירה
    - H3: עיצוב פינת האוכל
    - H3: עיצוב המטבח
    - H3: עיצוב חדר שינה
    - H3: עיצוב חדר ילדים
    - H3: מעצבות פנים מסבירות על עיצוב דירת קבלן
  - H2: עיצוב דירת קבלן לסבא וסבתא – העיצוב של דורית
    - H3: עיצוב המטבח
    - H3: עיצוב הסלון
    - H3: עיצוב חדר אורחים
    - H3: עיצוב המקלחת
    - H3: עיצוב חדר השירות
  - H2: עיצוב דירת קבלן ירושלמית - העיצוב של ישראל
    - H3: עיצוב חדר השינה
    - H3: החדר של אריאלה
    - H3: החדר של רונן
    - H3: החדר של לירן
    - H3: עיצוב פינת האוכל
    - H3: עיצוב המטבח
    - H3: עיצוב הסלון
    - H3: עיצוב חדר האמבטיה
  - H2: עיצוב מודרני וכפרי לדירת קבלן - העיצוב של מיטל
    - H3: עיצוב חלל הכניסה
    - H3: עיצוב הסלון
    - H3: עיצוב המטבח
    - H3: עיצוב פינת האוכל
    - H3: עיצוב חדר השינה
    - H3: עיצוב חדר משפחה
    - H3: עיצוב חדרי הילדים
    - H3: עיצוב חדר אמבטיה
    - H3: עיצוב הגינה
  - H2: עיצוב דירה- תמונות מלקוחות מידרג
  - H2: מעצבי פנים מומלצים בעיצוב דירת קבלן
  - H2: אנשים שהתעניינו בעיצוב דירת קבלן התעניינו גם בזה...
  - H2: טיפים נוספים ב שיפוץ ועיצוב הבית

### #3 https://www.shimrit-design.co.il/איך-להפוך-דירת-קבלן-לדירה-יחודית

- Title: עיצוב דירת קבלן במרכז | שמרית אוחיון
- Words: 1,385 · H2: 6 · H3: 14 · price mentions: 5 · schema: Answer, BlogPosting, FAQPage, Person, Question, VideoObject
- Tools: FAQPage schema; gallery/slider
- File: `competitor-pages/https_www_shimrit_design_co_il__facf22.json`

- H1: עיצוב דירת קבלן במרכז: סודות המקצוע שיהפכו דירת סטנדרט לבית יוקרה (מדריך ומחירון)
  - H2: 4 סודות עיצוב שהקבלן לא יספר לכם (ופתרונות מעשיים)
    - H3: סוד 1: המלכודת של הנמכות המיזוג (ואיך אני פותרת אותה)
    - H3: סוד 2: "המפלצת" שבכניסה לבית
    - H3: סוד 3: אשליית המרחב של דלתות קו אפס
    - H3: סוד 4: המטבח – מתי להשתדרג ומתי לחכות?
  - H2: עיצוב סינרגי מחבר בין תכנון פונקציונלי, אור, תנועה, חומרים ואווירה.
  - H2: תכנון מוקדם הוא אחד השלבים המשמעותיים ביותר בדירת קבלן.
  - H2: אז איפה שמים את הכסף? (תעדוף תקציב חכם)
  - H2: מתכננים לעבור לדירה חדשה באזור המרכז?
  - H2: רכשתם דירת קבלן? זה הזמן לתכנן לפני שההחלטות מתקבעות.
- H1: מגזין עיצוב: השראה, טרנדים ורעיונות לבית שלכם
    - H3: תכנון תאורה למשרדים ולחללים מסחריים | שמרית אוחיון
    - H3: עיצוב פנים במודיעין – המדריך המלא | שמרית אוחיון
    - H3: פנג שוואי בבית: המדריך המלא לעיצוב פנים מלא באנרגיה | שמרית אוחיון
    - H3: שינויי דיירים בדירת קבלן – 5 טעויות שכדאי למנוע
    - H3: כמה עולה מעצבת פנים? מדריך מחירים ושירותים
    - H3: מודרני, כפרי או נורדי? כך תבחרו את סגנון העיצוב לבית שלכם
    - H3: הטרנדים החמים בעיצוב פנים לשנת 2026
    - H3: כמה עולה שיפוץ דירה? המדריך לתכנון תקציב והימנעות מחריגות
    - H3: תכנון תאורה לבית – המדריך המלא 2026 | שמרית אוחיון
    - H3: עיצוב דירת קבלן – תכנון וליווי מקצועי | שמרית אוחיון

### #4 https://www.elephantdesign.co.il/עיצוב-ותכנון-דירה-מקבלן

- Title: ליווי לעיצוב דירת קבלן Elephant Design לירון שנהר - סטודיו לעיצוב פנים
- Words: 644 · H2: 6 · H3: 5 · price mentions: 0 · schema: none
- Tools: iframes: static.parastorage.com; gallery/slider
- File: `competitor-pages/https_www_elephantdesign_co_il__ea10fc.json`

- H1: עיצוב פנים לדירה מקבלן
    - H3: תכנון מדויק מהשלב הכי חשוב
- H1: רכשתם דירה חדשה על הנייר? מזל טוב!
  - H2: זוכת פרס מעצבת השנה
  - H2: לשנת 2019-2020. לירון שנהר, מעצבת ומתכננת פנים, בעלת סטודיו ELEPHANT DESIGN. כבר כמעט שני עשורים אני מלווה לקוחות עם מאות פרויקטים בכל הארץ, עם התמחות ממוקדת בליווי לדירות קבלן. מה שמנחה אותי הוא: הוא דיוק, הקשבה וניסיון לייצר חלל שהוא גם פרקטי, גם הרמוני – ובעיקר, שלכם.
- H1: מה אני עושה בשבילכם? ​
  - H2: שני עשורים של פעילות ומאות פרויקטים מוצלחים בפריסה ארצית
  - H2: הנה מה שיש ללקוחות לספר
  - H2: שאלות נפוצות
    - H3: רכשנו "דירה על הנייר" באיזה שלב רצוי לשלב מעצב פנים?
    - H3: למה לא להסתפק במחלקת שינויי דיירים?
    - H3: יש לנו תקציב מוגבל – כדאי לעבוד עם מעצבת?
    - H3: איך בוחרים מעצבת פנים?

### #5 https://www.facebook.com/groups/466734475710690/

Not fetched (login wall or blocked). Title from SERP: דירה חדשה מקבלן תכנון עיצוב ושינויי דיירים

### #6 https://shuki-meir.co.il/עיצוב-פנים/עיצוב-דירת-קבלן/

- Title: עיצוב דירת קבלן - שוקי מאיר עיצוב פנים - עיצוב דירה מקצועי בהתאמה אישית
- Words: 1,100 · H2: 10 · H3: 3 · price mentions: 0 · schema: Answer, Article, BreadcrumbList, CommentAction, EntryPoint, FAQPage, ImageObject, ListItem, Organization, Person
- Tools: FAQPage schema; gallery/slider
- File: `competitor-pages/https_shuki_meir_co_il__c07c0f.json`

  - H2: למידע נוסף
    - H3: למידע נוסף
  - H2: בלוג
  - H2: עיצוב דירת קבלן
  - H2: עיצוב דירה מקבלן
  - H2: עיצוב פנים דירת קבלן
  - H2: שאלות נפוצות
  - H2: פוסטים נוספים
  - H2: עיצוב פנים דירת קבלן – בחירה אולטמטיבית
  - H2: מה חשוב לדעת על עיצוב פנים דירת קבלן?
    - H3: למה כדאי להשקיע בבחירת סטודיו העיצוב שלכם?

### #7 https://hadif.co.il/blog/עיצוב-פנים-דירות-מקבלן/

- Title: עיצוב פנים – דירות מקבלן – חדיף
- Words: 720 · H2: 14 · H3: 0 · price mentions: 0 · schema: none
- Tools: gallery/slider
- File: `competitor-pages/https_hadif_co_il_blog__fef6c0.json`

- H1: עיצוב פנים – דירות מקבלן
  - H2: לאחר הגשמת החלום והחתימה על חוזה רכישת הדירה, מתחילים בעלי הנכס לחשוב על השלב הבא והוא עיצוב פנים – דירות קבלן. הם מודעים לשפע האפשרויות הקיימות ומעוניינים לגור בדירה שהיא מעוצבת על פי טעמם האישי.
  - H2: בחירה של מעצבת פנים
  - H2: בחירה של מעצבת פנים
  - H2: שינויים והתאמות במהלך בניית הנכס
  - H2: בחירה של חומרי גלם
  - H2: הלבשה של הבית
  - H2: מאמרים קשורים
- H1: כך תזהו קבלן בנייה שכדאי לרכוש ממנו דירה חדשה
- H1: 3 ההשקעות המשתלמות ביותר
- H1: 6 טיפים לעיצוב פנים לבית
- H1: בניית בית מותאם לגיל השלישי
  - H2: החברה
  - H2: חדיף פלטינום
  - H2: פרויקטים
  - H2: צור קשר
  - H2: משרדים ראשיים
  - H2: צור קשר
  - H2: משרד ברמת גן

### #8 https://www.pinterest.com/dnshaked/apartment-interior-design-עיצוב-דירת-קבלן/

- Title: 100 רעיונות של Apartment Interior Design | עיצוב דירת קבלן | עיצוב, סטודיו לעיצוב, עיצוב מסעדות
- Words: 92 · H2: 1 · H3: 0 · price mentions: 0 · schema: none
- Tools: iframes: ct.pinterest.com; quiz text
- File: `competitor-pages/https_www_pinterest_com_dnshaked_apartment_interior_design__76533f.json`

- H1: Apartment Interior Design | עיצוב דירת קבלן
  - H2: דירות בתל אביב | TLV Apartments
