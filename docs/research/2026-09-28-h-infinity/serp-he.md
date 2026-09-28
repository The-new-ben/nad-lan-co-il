# Hebrew SERP - H Infinity / מגדל אינפיניטי / מתחם סומייל (28.9.2026)

## How this was collected (read before trusting the order)
- **Autocomplete = real Google.** Google Suggest API with `hl=iw&gl=il` (the same data as the search box).
- **Result lists = the WebSearch tool** (a search index queried from the US). Google.co.il itself cannot be read
  without JavaScript and without logging in, which the rules forbid. The domains and titles below are what ranks for
  these queries in that index; the exact Google.co.il order may differ by a few places.
- **"People also ask" could not be observed directly** (it needs a rendered Google page). In its place: question-form
  autocomplete, the conversational queries in our own Search Console for this page, and the questions competitors
  answer. These are marked "PAA-proxy".
- **Our own Search Console** for /projects/h-infinity-somail-tel-aviv/ (file gsc_hinf.csv exported earlier today by
  the parent session): impressions only, no clicks yet.

## 1. What people type (autocomplete, Google, hl=iw, gl=il)
| Seed | Google suggests |
|---|---|
| אינפיניטי חג | **אינפיניטי חגג · מגדל אינפיניטי חגג · אינפיניטי קבוצת חג'ג · אינפיניטי טאוור חגג · פרויקט אינפיניטי חגג** |
| אינפיניטי תל אביב | אינפיניטי תל אביב · **מגדל אינפיניטי תל אביב** · **פרויקט אינפיניטי תל אביב** · מגדלי אינפיניטי תל אביב · **מגדל אינפיניטי תל אביב כתובת** · (noise: מוסך, בריכת אינפיניטי) · אינפיניטי טאואר תל אביב |
| מגדל אינפיניטי | מגדל אינפיניטי · מגדל אינפיניטי תל אביב · מגדל אינפיניטי חגג · מגדל אינפיניטי תל אביב כתובת · מגדל אינפיניטי רעננה (**collision**) · **מגדל אינפיניטי למכירה** |
| H Infinity | h infinity tower · **h infinity מחירים** · h infinity tower tel aviv · h infinity tel aviv · (noise: h infinity control, kalman filter) |
| h infinity מ | **h infinity מחירים** · h infinity tower מתחם סומייל · מגדל h infinity |
| infinity חגג | infinity חגג · infinity tower חגג |
| אייץ אינפיניטי | **no suggestions** (nobody types it this way) |
| סומייל | סומייל · סומייל תל אביב (the rest is "סומלייה", wine) |
| סומייל תל אביב | מתחם סומייל תל אביב · פרויקט סומייל תל אביב · שכונת סומייל תל אביב · כפר סומייל תל אביב · סומייל צפון תל אביב · בניין סומייל תל אביב · מתחם סומייל עיריית תל אביב |
| מתחם סומייל | מתחם סומייל תל אביב · **מתחם סומייל עיריית תל אביב** · **מתחם סומייל מחירים** · **מתחם סומייל חגג** |
| סומייל פרויקט | פרויקט סומייל · פרויקט סומייל תל אביב · **פרויקט סומייל חגג** · פרויקט סומייל אפריקה ישראל |
| סומייל מגדל | מגדל סומייל · מגדלי סומייל |
| כפר סומייל | כפר סומייל תל אביב · כפר ערבי סומייל |
| חגג אבן גבירול | פרויקט חגג אבן גבירול · מגדלי חג'ג אבן גבירול · חגג גרופ אבן גבירול |
| מגדל חגג | מגדלי חג'ג הארבעה (**collision: office towers**) · מגדלי חג'ג תל אביב · מגדלי חג'ג אבן גבירול · **חגג מגדל אינפיניטי** · מגדל בבלי חגג |
| קבוצת חגג | קבוצת חגג מניה · מאיה · **קבוצת חגג אינפיניטי** · קבוצת חג'ג תל אביב · טלפון |
| אבן גבירול 128 | אבן גבירול 128 תל אביב |
| דירות למכירה אבן גבירול | דירות למכירה אבן גבירול תל אביב · יד 2 דירות למכירה אבן גבירול תל אביב |
| פרויקטים חדשים בצפון הישן | פרויקטים חדשים בצפון הישן תל אביב |
| מגדלי יוקרה בתל אביב | מגדלי יוקרה בתל אביב להשכרה |
| No suggestions for | דירות למכירה סומייל · אינפיניטי מחירים (as typed) · חג'ג' אינפיניטי אכלוס · קבוצת רכישה סומייל · מגדל מגורים אבן גבירול |

## 2. Our Search Console for this page (impressions, avg position)
מתחם סומייל 30 (14.6) · h infinity 9 (9.2) · חגג אבן גבירול 9 (12.2) · מתחם סומייל מחירים 6 (7.2) · מגדל אינפיניטי
תל אביב 5 (13.6) · מתחם סומייל תל אביב 5 (9.2) · פרויקט אינפיניטי תל אביב 4 (13) · h infinity מחירים 3 (10) ·
אינפיניטי חגג 2 (21) · אינפיניטי תל אביב 2 (10.5) · מגדל אינפיניטי 2 (24.5) · פרויקט סומייל תל אביב 2 (11) ·
אינפיניטי טאוור 1 (6) · מגדל אינפיניטי חגג 1 (20) · מגדלי אינפיניטי תל אביב 1 (11) · אבן גבירול ז'בוטינסקי 1 (25).
**Conversational follow-ups** (AI-mode style, position 3-9): "מה הכתובת שלו", "איפה הוא יושב", "טווח מחירים",
"מחיר", "למגורים", "פרטים נוספים", "כן אשמח מאוד". Reading: people ask an assistant about the project and then ask
for **the address, the location and the price range**. The answer paragraph must hold all three.

## 3. Result lists per query (WebSearch index, 28.9.2026)

### "אייץ' אינפיניטי חג'ג' סומייל" / "פרויקט אייץ' אינפיניטי"
1. israelhayom.co.il/article/828809 - "קבוצת חג'ג' רכשה מגרש נוסף במתחם סומייל" (the 121 lot)
2. calcalist.co.il L-3777183 - "חג'ג' שכחה לעדכן את קבוצת הרכישה בסומייל על הוספת שטחי ציבור במתחם"
3. globes.co.il did=1001392692 - "ללא קבוצת הרכישה: "סומייל" הופך לפרויקט יזמי בהובלת קבוצת חג'ג'" (30.11.2021)
4. calcalist.co.il/article/b1p8qwzcee - "בלב הפועם של ת"א: קבוצת חג'ג' מכרה מאות דירות במגדל INFINITY" (1.9.2025, sponsored)
5. magdilim.co.il - "פרוייקט סומייל עובר לשליטת האחים חג'ג'"
6. infinity-hagag.co.il - "קבוצת חג'ג'" (marketing landing)
7. project-tlv.info/urban-plans/sumail/hagag/ - "פרויקט מגדל חג'ג' מתחם סומייל / אינפיניטי - H Infinity"
8. a broker site "H - INFINITY TOWER - מתחם סומייל - קבוצת חג'ג'"
9. hagag-group.ussl.co.il/h-infinity/ (an old Hagag mirror)
- "פרויקט אייץ' אינפיניטי" also pulls Infinity Park Raanana (ice.co.il, m-y-s.com, infinity-park.co.il) and El-Har's
  "מגדל אינפיניטי רעננה": the spelled-out Hebrew name is **ambiguous and not typed**.

### "H Infinity תל אביב" / "H Infinity תל אביב חג'ג'"
1. calcalist b1p8qwzcee (sold hundreds, 1.9.2025)
2. **madlan.co.il/projects/H-Infinit** - "H Infinity Tower תל אביב יפו - פרויקט בניה חדשה | מדלן"
3. **hagag-group.co.il/projects/ResidentProjects/h_infinity** - "מגדל היוקרה H INFINITY - מתחם סומייל • קבוצת חג'ג'"
4. infinity-hagag.co.il
5. project-tlv.info (Hagag tower page)
6. nadlan.com/project/אינפיניטי - "אינפיניטי, תל אביב יפו - NADLAN.COM | ..."
7. homeinisrael.com - "קבוצת חג - פרויקט "HH-Infinity Tower" תל אביב"
8. infinity8.co.il/office-towers/h-tower/ - "H Tower - INFINITY" (**collision: an office-tower brand**)
9. nadlanmaster.co.il - "פרויקט H-Infinity - מגדל H אינפיניטי של קבוצת חג'ג' בתל אביב" (stale: "48 קומות", "צפי לאכלוס תוך 5 שנים")
Snippet language: "INFINITY TOWER... במתחם סומייל, בלב ליבה של תל אביב... בין הרחובות ז'בוטינסקי ואבן גבירול"; "מגדל יוקרה בן 52
קומות ובניין בוטיק בן 7 קומות"; "פרופסור משה צור"; "לובי כניסה... כ-10 מטרים".

### "מגדל אינפיניטי חג'ג' תל אביב מחירים" (≈ "h infinity מחירים")
1. themarker.com 1.12.2014 - "קבוצת חג'ג': 90 דירות החל מ-2.2 מ' ש' נמכרו במגדל שיוקם במרכז ת"א"
2. calcalist b1p8qwzcee
3. **yad2.co.il/yad1/project/5793** - "פרויקט INFINITY TOWER - הצפון החדש - כיכר המדינה, תל אביב יפו | קבוצת חג'ג' | אלקטרה בע"מ"
4. hagag-group.co.il (home)
5. infinity-hagag.co.il
6. hagag-group.co.il H INFINITY page
7. project-tlv.info
8. homeinisrael.com
9. nadlanmaster.co.il
Snippet prices shown: "החל מ-65,000 ₪ למ"ר", "2.2 מיליון" (2014), "2.5 חדרים מ-4.5 מיליון", "4 חדרים... מ-8.1 מיליון".
**Nobody in the list shows recorded deal prices in the snippet** (Madlan has them on the page, not in the snippet).

### "מתחם סומייל תל אביב" / "מתחם סומייל"
1. magdilim.co.il/15062114/ - "מתחם סומייל: כיצד הפך המתחם המוזנח לזירה הנדל"נית החמה ביותר בתל אביב?"
2. **he.wikipedia.org/wiki/סומייל**
3. timeout.co.il - "מגדל ציבורי חדש: כך ייראה בניין העירייה שנבנה על קרקעות סומייל"
4. calcalist.co.il/tags/מתחם_סומייל
5. project-tlv.info/urban-plans/sumail/ - "פרויקט מתחם סומייל / סומיל"
6. gbwawa.com - "מתחם סומייל (סמל) דרום תל אביב - WAWA" and "... צפון"
7. yaar.yaar.net - "סומייל - תל אביב" (history)
8. electra-construction.co.il - "מתחם סומייל"
Snippet themes: "המתחם החם ביותר בתל אביב", "בין הצירים הראשיים אבן גבירול, ז'בוטינסקי, בן סרוק וארלוזורוב",
"על חורבות הכפר הערבי סומייל... 45 דונם", "כ-1,200 דירות במגדלים בני 50 קומות", "מבנה חדש בן 24 קומות בפינת אבן
גבירול-ארלוזורוב ישמש את משרדי העירייה".

### "מתחם סומייל מחירים דירות 2026" / "דירות למכירה מתחם סומייל תל אביב"
1. israelhayom.co.il/business/real-estate/article/7079038 - ""זיהינו את מתחם סומייל כדבר הבא""
2. magdilim.co.il/15062114/
3. calcalist.co.il/real-estate/article/BJ5EPA3t00 - "אושרה תוספת של 52 דירות למגדל הצפוני שתבנה אפריקה ישראל מגורים במתחם סומייל"
4. calcalist L-3849900 - "המגרש הצפוני והאחרון במתחם סומייל בת"א מוצע למכירה"
5. themarker.com premium - "הכניסה למיליונרים בלבד: השכונה החדשה שנבנית בלב תל אביב כבר מושכת אש"
6. globes did=1001278988 - "אפריקה ישראל תקים מגדל מגורים בן 300 דירות במתחם סומייל"
7. ynet L-4656081 - "ת"א: עוד בניין במתחם סומייל; מה המחירים?"
8. walla - "לב לבייב... רכש את מתחם סומייל"
9. btrvalue.co.il - "נמכר מגרש למגורים - מתחם סומייל צפון"
Snippet claims: "מכ-55,000 שקל למ"ר לכ-70,000 שקל למ"ר" (older), "4 מגדלים בני 50 קומות", Africa Israel "5.1 מיליון שקל לדירה" (older).
**Gap: no page answers "מתחם סומייל מחירים" with 2025-2026 deal data for both towers side by side.**

### "אבן גבירול 128 תל אביב"
1. d.co.il - a business listing at Ibn Gabirol 128 (old address noise)
2. he.wikipedia - רחוב אבן גבירול
3. bus line 128 pages (noise)
4. **yad2 project 5793** - snippet: "INFINITY TOWER... באבן גבירול 128 ... בפינת אבן גבירול וז'בוטינסקי"
5. **newkey.co.il/projects/hagag-group/h-infinity-tower/** - "פרויקט חדש שלמה אבן גבירול 128 בתל אביב"
6. tabanow.co.il - plan 507-0643890
7. project-tlv.info/buildings/ibn-gabirol/
**Opportunity:** the address query is weak and noisy; a page that says "אבן גבירול 128" in the title/lead wins it.

### "מגדל חג'ג' סומייל אבן גבירול"
magdilim (control), nadlancenter 4672 ("עכשיו זה רשמי: קבוצת חג'ג' היא בעלת השליטה בפרויקט סומייל"), calcalist
L-3792931 ("מאחורי הקלעים של מגדל היוקרה של חג'ג' בסומייל"), ynet L-4412640 ("בהלת המגדלים: 50 קומות ייבנו באבן גבירול"),
ynet L-4656081, infinity-hagag.co.il, hagag-group.co.il.

### "מגדל אינפיניטי למכירה תל אביב דירה"
a Facebook group post "דירת יוקרה למכירה במגדל אינפיניטי של קבוצת חג'ג'!", yad2 5793, madlan, nadlan.com, hagag-group,
project-tlv, luxury-realestate-israel.com, telaviv360.co.il, nadlanmaster. Snippet mentions a ₪1M-at-signing model
"from ₪4,100,000... remainder two years after occupancy" (unverified, undated).

### "מגדל אינפיניטי תל אביב כתובת"
yad2 5793 ("אבן גבירול 128, בצפון החדש - כיכר המדינה"), newkey (EINSTEIN TOWER, wrong project), hagag-group,
infinity8.co.il office towers ×3 (**collision**), homeinisrael, nadlanmaster, an Airbnb listing.

## 4. Name variants Google connects to this project (Hebrew)
Strong (typed): **מגדל אינפיניטי**, **אינפיניטי חג'ג'**, **H Infinity / h infinity tower**, **מתחם סומייל**,
**פרויקט סומייל**, אינפיניטי טאוור, INFINITY TOWER, מגדל אינפיניטי תל אביב, פרויקט אינפיניטי תל אביב.
Official/filing: H - INFINITY TOWER - מתחם סומייל; סומייל 124; אינפיניטי - סומייל; קבוצת הרכישה "אינפיניטי".
Weak (not typed): אייץ' אינפיניטי; מגדל H אינפיניטי.
Collisions: אינפיניטי (investment house), אינפיניטי פארק רעננה, מגדל אינפיניטי רעננה, INFINITY office towers,
מגדלי חג'ג' (HaArba'a offices), סומייל 121 (Hagag's other lot).

## 5. PAA-proxy questions (Hebrew)
- מה הכתובת של מגדל אינפיניטי? / איפה נמצא מגדל אינפיניטי של חג'ג'?
- כמה קומות יש במגדל אינפיניטי? (51? 52? 53?)
- כמה דירות יש בפרויקט?
- מה טווח המחירים במגדל אינפיניטי? כמה עולה דירה? כמה עולה מ"ר?
- מתי אכלוס מגדל אינפיניטי?
- מי הקבלן? מי האדריכל?
- מה זה מתחם סומייל? למה קוראים לו סומייל? מה היה שם?
- אילו פרויקטים יש במתחם סומייל? (DUO, אינפיניטי, מגדל העירייה)
- האם יש בריכה? איזו?
- האם הרכבת הקלה מגיעה לשם ומתי?
- מה המבצע של חג'ג' (מיליון שקל בחתימה)? מה התשואה המובטחת?
- האם כדאי לקנות? מה הסיכונים? מה קרה עם קבוצת הרכישה?
- האם אפשר לקנות מחו"ל? כמה מס רכישה?
