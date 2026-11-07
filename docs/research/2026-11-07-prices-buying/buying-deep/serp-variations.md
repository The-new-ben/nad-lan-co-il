# SERP variations: 24 buying searches (7.11.2026, second pass)

- **Device and method:** desktop, the owner's Chrome ("gmktec"), `google.co.il/search?q=…&hl=iw&gl=il`, signed-in Google account. Each page was loaded like a person would, then the rendered page was read: organic titles and URLs, the AI answer, people-also-ask, the related-searches block and whether a video pack appeared. Insight boxes from Search Console were not recorded (public repo).
- **Google's label changed:** the AI answer is now headed **"תקציר מ-AI"** (the earlier label was "סקירה כללית מבוססת AI"). There is also an "מצב AI" tab in the top bar.
- **CAPTCHA:** none during the 24 variations. A CAPTCHA (google.com/sorry) appeared later, on the 46th search of the session, during the related-search drill (see `related-searches.md`). It was not solved or bypassed; that pass stopped.
- **The first pass** (`../serp-buying.md`) already covers: קניית דירה · איך לקנות דירה · מחשבון קניית דירה · עלויות קניית דירה · קניית דירה ראשונה · מה לבדוק לפני קניית דירה יד שניה · קניית דירה ללא הון עצמי. This file adds 24 more and re-loads "קניית דירה ראשונה" (its result is stable).
- `[videos]` = a video pack was shown.

## Summary across the 24
| Signal | Result |
|---|---|
| AI answer | present on **23 of 24**. Absent only on "קניית דירה מכונס נכסים". On 3 searches it was still generating ("בתהליך חשיבה") when the page was read: טיפים לקניית דירה, קניית דירה לזוג צעיר, קניית דירה ידועים בציבור. "איך קונים דירה" had no AI answer on the first load and one on a reload minutes later. |
| People-also-ask | shown on only **4 of the 24** (the AI answer usually replaces it): איך קונים דירה (first load only), קניית דירה מקבלן, קניית דירה שלא רשומה בטאבו, קניית דירה עם חריגות בנייה; plus 1 related search (סיוע ברכישת דירה נכות כללית) |
| Video pack | 9 of 24: יד שנייה, איך קונים, תהליך, מקבלן, בלי הון עצמי, טיפים, להשקעה, עם שותפים, עכשיו או לחכות |
| nad-lan.co.il in the visible results | **0 of 24** (and 0 of the 21 related searches opened) |
| The owner's other site | jus-tice.co.il/apartment-purchase-guide-comprehensive/ is **#8 for "צ'ק ליסט לקניית דירה"** (a related search) |
| Who owns the SERP | law firms. The most frequent domains across the 24: yonilevy.co.il (11 SERPs), gov.il (10), amitvered.co.il (8), kolzchut.org.il (6), prlaw.co.il (6), elkayamlaw.co.il, nadlanmaster.co.il, tidhar.co.il, lazyinvestor.co.il, gelberglaw.co.il, midrag.co.il (5 each), dabullaw.co.il, wecheck.co.il (4 each), gindi.com (3) |

---

## A. Process family

### 1. איך קונים דירה [videos]
- **Organic (reload):** 1 amitvered.co.il/קניית-דירה/ "קניית דירה - המדריך המלא לרכישת דירה (2026)" (sitelinks "קניית דירה יד שניה – איך מתחילים?", "בדיקות מקדמיות – חלק ב'") · 2 yeda-kesef.co.il "איך צעירים יכולים לקנות דירה בישראל? המדריך המלא" (stars 5.0 (765)) · 3 nadlanmaster.co.il "תהליך קניית דירה - איך קונים דירה בישראל? (מעודכן ל-2025)" · 4 nahala.co.il "איך קונים דירה – המדריך השלם לקניית דירה" · 5 wecheck.co.il "קניית דירה - מדריך מקיף איך קונים דירה" · 6 tidhar.co.il "מתכננים לקנות דירה להשקעה?" · 7 lazyinvestor.co.il "רכישת דירה ב-0₪ הון עצמי" (stars 4.9 (563)).
- **Videos:** "תהליך קניית דירה: מדריך פשוט" (YouTube, 21:14, 10 key moments) · "איך לקנות דירה ראשונה: מדריך מקיף להתנהלות כלכלית נכונה" (Ono Academic College, 9:38) · "קונים דירה על הנייר? זה מה שחייבים לדעת לפני שחותמים" (ynet, 22:31, a month old). **Images:** Kan 11 "מתחת לבלטות", Mashcantaman "איך קונים דירה ללא הון עצמי?".
- **AI (reload): present.** Sources: amitvered, yeda-kesef, mizrahi-tefahot, nadlanmaster, gindi, gov.il. "תהליך מובנה שדורש היערכות כלכלית, בדיקות מקדמיות וליווי מקצועי". Steps: equity "בדרך כלל נדרש מינימום של 25% עד 30%"; a pre-approval before searching; the monthly repayment "לא אמור לעלות על שליש מההכנסה הפנויה"; second-hand vs new (safe room, delivery-delay risk); an independent lawyer; land registry and Israel Land Authority records, permits and deviations, engineering; "אין לחתום על 'זיכרון דברים' מחייב ללא ייעוץ משפטי מוקדם"; warning note right after signing; purchase tax "חובה לשלם תוך 60 יום"; handover protocol; registration; a pointer to the Ministry of Construction and Housing guide.
- **People-also-ask (first load):** איפה כדאי לקנות דירה להשקעה? · מהן הבדיקות שיש לבצע לפני קניית דירה? · האם ניתן לקנות דירה בלי משכנתא? · איפה הכי זול לקנות דירה בישראל?
- **Related:** קניית דירה יד שנייה · מה לבדוק לפני קניית דירה יד שניה · מה לבדוק לפני קניית דירה מקבלן · קניית דירה ראשונה · איך קונים דירה להשקעה · חוזה קניית דירה יד שניה · עורך דין קניית דירה מחיר · איך לקנות דירה ללא הון עצמי (the first load had "איך לקנות דירה בארץ עם 100 אלף ש"ח" instead of the lawyer-price one).

### 2. תהליך קניית דירה [videos]
- **Organic:** 1 amitvered · 2 yonilevy.co.il "תהליך רכישת דירה: המדריך השלם לשנת 2026" · 3 gindi.com "6 השלבים הנדרשים לרכישת דירה בישראל" · 4 gov.il/he/pages/new_apartment_buyer "המדריך לרוכש דירה מקבלן" · 5 nadlanmaster · 6 jc-law.co.il "מדריך לרכישת דירה יד שניה" (2022 URL) · 7 elkayamlaw.co.il "קניית דירה מקבלן (2026) – המדריך המקיף בישראל!" · 8 tidhar.co.il "תהליך קניית דירה יד ראשונה".
- **AI: present.** Sources: gindi, yonilevy, gov.il, amitvered, sarusi-law, gertelaw. Five numbered stages: (1) finance and pre-approval, "לדירה ראשונה נדרש בדרך כלל הון עצמי של לפחות 25%", ancillary costs (appraiser, lawyer, broker, purchase tax, fees, moving); (2) search and due diligence: land-registry extract or a rights certificate (ILA / housing company), municipal planning check (permits, deviations, future plans), **prior debts (arnona, water, betterment levy, house committee)**; (3) negotiation and contract with an independent lawyer, "לוח תשלומים, מנגנוני ביטחונות ומועד מסירה", avoid a binding memorandum; (4) after signing: warning note, "הגשת הצהרה ותשלום מס רכישה… תוך 60 יום… (או 30 יום לפי הנחיות מיסוי מקרקעין)", payments by schedule, mortgage file; (5) possession: protocol, meter readings (electricity, water, gas), registration.
- **People-also-ask:** none.
- **Related:** קניית דירה יד שנייה · מה לבדוק לפני קניית דירה מקבלן · קניית דירה ראשונה · חוזה קניית דירה יד שניה · עורך דין קניית דירה מחיר · **שאלות לפני קניית דירה** · **איך לקנות דירה בגיל צעיר** · איך לקנות דירה ללא הון עצמי.

### 3. שלבי קניית דירה
- **Organic:** 1 amitvered · 2 gindi "6 השלבים" · 3 jc-law · 4 elkayamlaw · 5 gov.il new_apartment_buyer · 6 martindale.co.il "קניית דירה: חמישה שלבים קריטיים בהם עורך הדין מעניק ביטחון" · 7 sarusi-law.co.il "קניית דירה ראשונה – המדריך המלא לרכישת דירה (2026)" · 8 klikatnadlan.co.il "לוח תשלומים ברכישת דירה: המדריך לפריסה נכונה" · 9 alev-law.co.il "תהליך קניית דירה - שלב אחר שלב".
- **AI: present**, word for word the same answer and sources as "תהליך קניית דירה". Google treats the two as one intent.
- **Related:** adds **קניית דירה מקבלן על הנייר** to the "תהליך" list.
- **Reading:** "6 השלבים", "חמישה שלבים", "שלב אחר שלב": a counted step skeleton in the title is the DNA.

### 4. טיפים לקניית דירה [videos]
- **Organic:** 1 amitvered · 2 gov.il new_apartment_buyer · 3 yonilevy "קניית דירה ראשונה: 5 טיפים מניסיון לקנייה מוצלחת" · 4 gindi · 5 shahar-bedek.co.il "טעויות נפוצות לפני רכישת דירה חדשה" (a home-inspection firm, 9.11.2025) · 6 tidhar "המדריך המלא לקניית דירה מקבלן" · 7 nnlaw.co.il "10 טיפים לרכישת דירה" · 8 colman.ac.il "חושבים על קניית דירה? כמה דברים שחשוב לקחת בחשבון" (a college blog).
- **AI:** present, still generating at capture.
- **Related:** קניית דירה יד שנייה · מה לבדוק לפני קניית דירה מקבלן · מה לבדוק לפני קניית דירה יד שניה · קניית דירה ראשונה · **דירה מקבלן 20 80** · קניית דירה מקבלן על הנייר · חוזה קניית דירה יד שניה · **קניית דירה מקבלן תשלומים**.

### 5. טעויות בקניית דירה
- **Organic:** 1 yonilevy "הטעויות הנפוצות שכדאי להימנע מהן בקניית דירה ראשונה" · 2 partouche-law.com "6 טעויות נפוצות בקניית דירה שעולות מאות אלפי שקלים" · 3 igud-nadlan.org "טעויות קריטיות ברכישת דירה ראשונה – ומה עושים במקום" · 4 shahar-bedek.co.il · 5 aharon-law.com · 6 hb-adv.co.il "5 טעויות נפוצות בקניית דירה מקבלן!" · 7 itaishahar.co.il (a criminal-law firm) · 8 sgdlawyer.co.il "טעויות נפוצות בקניית ומכירת דירה: זכרון דברים, מיסוי ורישום" · 9 doron-aharoni.com "הסכם רכישת דירה יד 2: 7 סעיפים לבדוק לפני החתימה".
- **AI: present.** Sources: shahar-bedek, itaishahar, yonilevy. Mistake 1, budget: looking only at the price, ignoring purchase tax, lawyer, broker, renovation, moving and "מדדי תשומות הבנייה (בקניית דירה מקבלן)". Mistake 2: signing with no pre-approval. Mistake 3: mixing a home with an investment ("ערבוב מטרות הרכישה").
- **Related:** none shown.

### 6. מה לבדוק לפני קניית דירה
- **Organic:** 1 ygoldlaw.co.il "10 בדיקות חשובות לפני קניית דירה או בית" · 2 mishpati.co.il "14 שאלות שאתם חייבים לשאול לפני קניית דירה" · 3 weller-law-office.com "40 בדיקות לפני רכישת דירה | המדריך המשפטי המלא לרוכשים" · 4 amitvered · 5 alev-law.co.il "כל מה שחשוב לבדוק לפני קניית דירה יד שנייה" · 6 madlan.co.il/mortgage/smartBuying "מה חייבים לבדוק לפני קנית דירה?" · 7 **gov.il checklist PDF "רשמת תיוג ('צ'ק ליסט') מה צריך לבדוק לפני שרוכשים דירה?"** · 8 midrag.co.il · 9 doron-aharoni.com "בדיקות לפני קניית דירה: זכויות, היתרים וחובות".
- **AI: present.** Sources: ygoldlaw, mishpati, weller-law-office, amitvered, gov.il, partouche-law, weislaw, nadlancenter, 9000000.co.il (an insurer). Three blocks: (1) legal: land-registry extract or rights certificate, seller identity and marital status, condominium file and plan (parking, storage, roof), permits and deviations, an independent lawyer, no memorandum; (2) financial: pre-approval, the full cost list, and for a developer: Sale Law securities, developer strength, trust accounts; (3) physical and surroundings: a daytime visit, water pressure, electricity, air conditioning, damp or mould.
- **Related:** מה לבדוק לפני קניית דירה יד שניה · מה לבדוק לפני קניית דירה מקבלן · תהליך קניית דירה · קניית דירה יד שנייה · קניית דירה ראשונה · חוזה קניית דירה יד שניה · עורך דין קניית דירה מחיר · **צ'ק ליסט לקניית דירה**.
- **Reading:** counted lists win ("10 בדיקות", "14 שאלות", "40 בדיקות"). Our /apartment-buying-checklist/ is not in the top 9.

## B. Deal-type family

### 7. קניית דירה יד שנייה [videos]
- **Organic:** 1 yad2 /realestate/forsale · 2 yad2 Tel Aviv area · 3 prlaw.co.il "קניית דירה יד שנייה - מדריך מלא וייצוג משפטי" · 4 yad2 Center and Sharon · 5 dsegev-law.co.il "קניית דירה יד שנייה 2026: המדריך המקיף בישראל!" · 6 arbell-law.co.il "תהליך קניית דירה יד שנייה: מדריך משפטי מקיף לרוכשים 2026".
- **AI: present.** Sources: yad2, yadata.yad2, madlan, yonilevy. It opens transactionally ("מתחילה בחיפוש נכסים בלוח יד2 … ובאמצעות הערכת שווי … yadata"), then: market research and price comparison; pre-approval; legal check (land registry, ILA, housing company; debts, liens, deviations); **engineering check ("בדק בית": infrastructure, electricity, plumbing, damp)**; **surroundings (visit at different hours, noise, parking, house committee)**; negotiation; contract and warning note.
- **Related (all listing intent):** יד 2 דירות למכירה בתל אביב ללא תיווך · דירות למכירה עד 800 אלף יד 2 · יד 2 דירות למכירה ללא תיווך · דירות למכירה תל אביב יד 2 · דירות למכירה עד 600 אלף יד 2 · דירות עד 500 אלף שקל יד 2 · דירות עד 300 אלף שקל יד 2 · יד 2 דירות להשכרה ללא תיווך.
- **Reading:** half listings, half law firms. Price bands under ₪800K appear again (as on the head query).

### 8. קניית דירה מקבלן [videos]
- **Organic:** 1 elkayamlaw.co.il · 2 gov.il new_apartment_buyer · 3 nadlanmaster.co.il "רכישת דירה מקבלן - המדריך המלא לרוכש ב-2026 (כל המידע)" · 4 prlaw.co.il "רכישת דירה מקבלן" · 5 tidhar.co.il "המדריך המלא לקניית דירה מקבלן" · 6 dsegev-law.co.il "קניית דירה מקבלן: המדריך לרוכש בשנת 2026" · 7 gelberglaw.co.il "רכישת דירה מקבלן: החוזה, הערבויות ולוח התשלומים" · 8 dabullaw.co.il "קניה מקבלן: המדריך המשפטי המלא לרכישת דירה על הנייר".
- **People-also-ask:** מהי האחריות של קבלן על דירה לפי חוק המכר? · איפה אפשר למצוא דירות במחיר עד מיליון שקל? · מהן הבדיקות שיש לבצע לפני קניית דירה? · מהם השלבים בתהליך קניית דירה?
- **AI: present.** Sources: gov.il, nadlanmaster, elkayamlaw, dabullaw, gelberglaw. Due diligence: land-registry and land ownership, a valid permit, **"בדיקת רישיון הקבלן, הסיווג והאיתנות הפיננסית"**; the **purchase-request form** ("דמי רצינות"): "לא לחתום עליו בלי ייעוץ משפטי (הוא מחייב דיווח לרשויות המס תוך כ-40 יום)"; an independent lawyer; a **changes annex**; CPI linkage "לרוב מוגבל לרכיב הבנייה"; agreed compensation for a delay "מעבר ל-60 יום (על פי חוק המכר)"; **"אסור לשלם לקבלן מעל 7% ממחיר הדירה ללא קבלת בטוחה"**; pay only with the bank's voucher booklet; Form 4; inspection; protocol.
- **Related:** קניית דירה מקבלן על הנייר · מה לבדוק לפני קניית דירה מקבלן · קניית דירה מקבלן תשלומים · דירה מקבלן 20 80 · חוזה קניית דירה מקבלן · ערבות בנקאית בקניית דירה מקבלן · צ'ק ליסט לקניית דירה · טופס הרשמה לרכישת דירה מקבלן.

### 9. קניית דירה על הנייר
- **Organic:** 1 socity.co.il "קניית דירה על הנייר ב-2026: כך תחסכו מאות אלפי שקלים" · 2 nadlanmaster "מידע, יתרונות וחסרונות" · 3 hadif.co.il "האם כדאי לקנות דירות על הנייר וממה צריך להיזהר?" · 4 prlaw "מדריך מלא לרוכשים" · 5 midrag.co.il tip · 6 elkayamlaw "(פריסייל) – מדריך משפטי לרוכשים" · 7 shorfinancy.co.il "על הנייר מול פינוי בינוי - יתרונות וסיכונים" · 8 gelberglaw "הסיכונים ומה בודקים".
- **AI: present.** Ten sources incl. ynet. Advantages: "הנחה ממחיר השוק שיכולה לנוע בין 10% ל-30% (או 5%–20% בפרויקטים מסוימים)", payment spread (20/80), choosing floor and orientation, buyer changes. Risks: the construction input index ("מייקרים את עלות הדירה בעשרות אלפי שקלים"), delays, render vs reality, developer solvency. Protections: the 7% rule, a dedicated trust account, closed bank accompaniment, a valid permit, an independent lawyer, the contractor licence and the zoning plan.
- **Related:** קניית דירה על הנייר מקבלן · לקנות דירה על הנייר ולמכור · מס רכישה דירה על הנייר · מס שבח דירה על הנייר · **מתי משלמים מס רכישה על דירה על הנייר** · מחיר למשתכן · **איך להתמקח על מחיר דירה מקבלן**.
- **Note:** the AI's discount range is unsourced and changes between loads (10–30%, 5–20%, 15–20% on the related search). An honest, dated number would beat it.

### 10. קניית דירה מכונס נכסים
- **Organic:** 1 kones2.co.il (listings) · 2 konesonline.co.il (board) · 3 prlaw "מדריך וסיכונים" · 4 nadlancenter.co.il "כונס נכסים – המדריך השלם לשנת 2026" · 5 yasmint-law.com · 6 gelberglaw "ב-2026: מה חשוב לבדוק לפני שקונים" · 7 amitvered "קניית דירה מכונס נכסים - מה חשוב לדעת?" · 8 konesisrael.co.il · 9 houses.bidspirit.com (auctions) · 10 kones2 assets.
- **AI: absent** (the only one of the 24).
- **Related:** כונס נכסים ממשלתי · אתר כונס נכסים רשמי · כונס נכסים דירות · כונס נכסים דירות gov · דירות מכונס נכסים חינם · מחירי דירות מכונס נכסים · כונס נכסים איך זה עובד · כונס נכסים רכב.

### 11. קניית דירה מעמידר
- **Organic:** 1 gov.il service "בקשה של דייר בדיור הציבורי לקניית הדירה שבה הוא מתגורר" · 2 amidar.co.il "רכש דירות" · 3 ashlaw.co.il "האם ניתן לקנות דירה מעמידר?" · 4 main.knesset.gov.il press release "דייר בדיור ציבורי יוכל לרכוש במחיר מסובסד" (18.11.2025) · 5 beiton-minhali.co.il · 6 amidar "רכש דירות 2025 למלאי הדיור הציבורי" · 7 dabullaw · 8 kolzchut "זכאות לדיור ציבורי" · 9 amidar "מי זכאי לרכישת דירה".
- **AI: present.** "חוק הדיור הציבורי… פג בפברואר 2023 ומאז לא ניתן להגיש בקשות חדשות"; a new bill passed a first reading only; historical terms (5 years of residence; no property worth over ₪350,000; debts settled); the reverse programme (private owners sell flats to Amidar's stock).
- **Related:** רכישת דירת עמידר 2026 · קניית דירה מעמידר כל זכות · חוק קניית דירת עמידר · דירות עמידר פנויות · האם אפשר לקנות דירת עמידר · איתור דירות עמידר · הנחה ברכישת דירת עמידר · עמידר דירות ריקות.

### 12. קניית דירה בירושה
- **Organic (all seller or tax side):** kolzchut "פטור ממס שבח במכירת דירה שהתקבלה בירושה" · yonilevy "מכירת דירה שהתקבלה בירושה" · gov.il Tax Authority position paper 02-2026 · gaplaw · ygoldlaw · prlaw · limorarbel · alev-law "מכירת דירת ירושה בין אחים" · gelberglaw.
- **AI: present.** Sources: prlaw, gelberglaw. Receiving an inherited flat is not a sale (no capital-gains or purchase tax at the transfer, no estate tax in Israel); a succession or probate order first; registration only after the order.
- **Related:** מכירת דירה שהתקבלה בירושה מס שבח · מס ירושה על דירה שניה · פטור ממס שבח דירה בירושה · סעיף 49ב(5) · מס ירושה על דירה בישראל · חישוב מס שבח ירושה · מכירת חלק מדירה שהתקבלה בירושה · פטור דירת ירושה תושב חוץ.
- **Reading:** the buyer-side intent ("buying from heirs") has no SERP of its own; a hub FAQ is enough.

### 13. קניית דירה שלא רשומה בטאבו (from autocomplete)
- **Organic:** 1 yonilevy "קניית דירה ללא טאבו - המדריך המלא לעסקה בטוחה" · 2 luach-nadlan.co.il "כמה מסוכן לרכוש דירה ללא טאבו?" · 3 midrag · 4 doron-aharoni "שלושה מצבים, מה לבדוק ומתי להיזהר" · 5 lawdin.co.il "5 סכנות" · 6 gelberglaw "רמ״י וחברה משכנת" · 7 nitzanlaw · 8 shovalilaw "המדריך המלא לרכישה מחברה משכנת" · 9 dabullaw.
- **People-also-ask:** האם ניתן למכור דירה ללא טאבו? · איפה אפשר למצוא דירות למכירה עד מיליון שקל? · מהי אגרת רישום מכר בטאבו? · מי עושה רישום בטאבו?
- **AI: present.** A contractual right instead of a proprietary one; rights held by a housing company, the ILA or the Civil Administration; **a pledge at the Registrar of Pledges instead of a warning note**; the bank needs an undertaking to register the mortgage; price and liquidity discount; a rights certificate "עדכני ל-30 הימים האחרונים"; the seller's original contract; the sale plan.
- **Related:** דירה שלא רשומה בטאבו רק הערת אזהרה · איך רושמים דירה בטאבו · למה דירה לא רשומה בטאבו · בדיקת רישום בטאבו חינם · משכנתא על דירה שלא רשומה בטאבו · דירה רשומה במנהל · מכירת דירה עם הערת אזהרה · חברה משכנת.

### 14. קניית דירה עם חריגות בנייה (from autocomplete)
- **Organic:** eliavlaw.co.il · yasmint-law "המדריך השלם לקניית בית עם חריגות בניה" · lb-arc.co.il (an architect) · partouche-law · midrag · yael-boaz.co.il · prlaw · dabullaw · yonilevy.
- **People-also-ask:** האם ניתן להעביר זכויות בנכס עם חריגות בנייה? · מה עלי לעשות אם קניתי בית עם חריגות בנייה? · האם חלה התיישנות על חריגות בנייה? · **מהו מחשבון רכישת דירה?**
- **AI: present.** Liability passes to the buyer (section 243 of the Planning and Building Law); demolition orders and criminal exposure; the bank's appraiser lowers the value; legalising may trigger a betterment levy "כ-50% משווי ההשבחה"; registration can be blocked; a 5-year limitation on the construction offence, none on the use; compare the building file and the permit drawing ("גרמושקה") with reality; legalising takes "בממוצע מעל שנה"; contract protections.
- **Related:** אישור עירייה לטאבו חריגות בנייה · איך בודקים חריגות בניה.

## C. Money family

### 15. קניית דירה בלי הון עצמי [videos]
- **Organic:** 1 lazyinvestor "רכישת דירה ב-0₪ הון עצמי" · 2 nahala "4 שיטות" · 3 powercouple.co.il · 4 mizrahi-tefahot "מן הון להון" · 5 nitzanm.co.il "מדריך לרכישת דירה בלי הון עצמי 2025" · 6 credit360.co.il · 7 **project.avivmelisron.co.il "אביב מליסרון משנים את השיטה: כך אפשר לרכוש דירה בלי הון עצמי"** (a developer's own zero-equity sales page ranks) · 8 wecheck.
- **AI: present.** "כמעט בלתי אפשרית בצורה ישירה" (25% equity, 75% financing). Methods: a lien on the parents' home "עד לכ-50% משווי הנכס שלהם"; general-purpose loans (more expensive, raise the monthly payment); loans against study and pension funds; government programmes; periphery grants (Dimona, Eilat). Risks: a double burden; the bank's repayment-to-income ratio.
- **Related:** קניית דירה שניה ללא הון עצמי · משכנתא ללא הון עצמי · איך להשיג הון עצמי למשכנתא · דירה בהנחה · הון עצמי לדירה · הון עצמי 100 אלף · **מחשבון הון עצמי** · קניית דירה ללא משכנתא.

### 16. קניית דירה עם משכנתא
- **Organic:** menoramivt.co.il (investment mortgage) · harel-group "1+1" · nadlanavon.co.il "האם כדאי לקנות דירה עם משכנתא?" · wecheck · bankjerusalem · vider.co.il "משכנתא על נכס קיים" · dabullaw "מכירת דירה עם משכנתא" · kolzchut "משכנתא" · Discount investment mortgage.
- **AI: present**, with Google's disclaimer "התשובות מה-AI עלולות לכלול טעויות. לקבלת ייעוץ פיננסי, כדאי שתפנה לאנשי מקצוע". Financing up to 75% for a single home and "עד 50%" for an additional one; "לפחות שליש מההלוואה חייב להיות במסלול של ריבית קבועה"; up to 30 years; pre-approval; life and structure insurance.
- **Related:** mortgage-on-existing-home phrasings (owned by the mortgage cluster).

### 17. קניית דירה לזוג צעיר
- **Organic:** 1 kolzchut "סיוע ברכישת דירה (משכנתא) לזוגות ומשפחות ותיקים" · 2 555.co.il "מדריך משכנתא לזוגות צעירים" · 3 wecheck · 4 evensapir.co.il · 5 ofekm.com "דירה ראשונה לזוג צעיר: כל השלבים" · 6 ram-haim.co.il · 7 gov.il "סיוע במשכנתא למשפחות ותיקות ולזוגות צעירים" · 8 shelifinance.co.il · 9 hasolidit.com (forum).
- **AI:** present, still generating at capture.
- **Related:** סיוע ברכישת דירה נכות כללית · מענק לרכישת דירה ראשונה למחוסרי דיור · סיוע ברכישת דירה ראשונה · **זכאות משכנתא לזוגות צעירים** · **זכאות חוק הנגב** · **משכנתא מועדפת** · כל זכות קניית דירה · הלוואה לרכישת דירה ילד נכה.
- **Reading:** the intent is eligibility ("זכאות"). nad-lan already holds the data (zakaut.json).

### 18. קניית דירה להשקעה [videos]
- **Organic:** globes.co.il "רוצים לרכוש דירה להשקעה? 5 דברים" · lazyinvestor · fingrow · nadlancenter · nadlanmaster "איפה כדאי לקנות דירה להשקעה ב-2026?" · mor.law · socity "רכישת דירה בישראל [הדרך היחידה לקנות דירה ב-2026]" · gurgroup "דירה להשקעה מול תיק השקעות".
- **AI: present.** It states "מימון… של עד 75% משווי הנכס" for an investment flat, which contradicts the 50% it states on other searches; purchase tax 8% up to ₪6,055,070 and 10% above; capital-gains tax 25% of the real gain; a rent-income exemption "כ-5,654 ₪ בחודש"; rental yield "בין 2.4% ל-4.1%".
- **Related:** city variants, "איפה כדאי לקנות דירה להשקעה בארץ / בחו"ל", "דירה להשקעה עד מיליון". Owned by /investment/.

### 19. קניית דירה לפני מכירה (from autocomplete)
- **Organic:** mashcantaman.co.il "מה עושים כאשר רוכשים דירה חדשה לפני מכירת הדירה הקיימת?" · ygoldlaw "מכירת ורכישת דירה במקביל – מה קודם?" · midrag "למכור או לקנות דירה - מה קודם? שאלנו 77 מתווכים" · directnadlan · brikman-law · ofekm "משפרי דיור: לקנות לפני שמוכרים" · yonilevy · davar1.co.il · a Facebook group post.
- **AI: present** (short; source Mashcantaman): the "משפר דיור" route needs planning.
- **Related:** האם כדאי למכור עכשיו דירה · האם זה זמן טוב למכור דירה · **האם כדאי למכור דירה בזמן מלחמה** · איך מוכרים וקונים דירה · לא מצליח למכור דירה · הלוואת גישור · מס רכישה · יד 2 דירות למכירה.

### 20. האם לקנות דירה עכשיו או לחכות [videos] (from autocomplete)
- **Organic:** 1 a Facebook group post · 2 themarker.com (21.8.2026) "'הבנתי ששווה לחכות. מה שקורה עכשיו זו רק תחילת המפולת'" · 3 kopel.co.il · 4 madlan.co.il/blog "האם מחירי הדירות ירדו? כך תחשבו כמה באמת עולה ההמתנה" · 5 mdfinance.co.il "לקנות דירה עכשיו או לחכות ל-2027?" · 6 lazyinvestor "לקנות או לשכור?" · 7 nadlanit.co.il · 8 realestatepeople.online.
- **AI: present.** "ירידות מחירים מתונות של כ-1.5% עד 1.8%" over the year; "מלאי גבוה של דירות חדשות שלא נמכרו (כ-84 אלף דירות)"; "ריבית בנק ישראל עומדת על 3.25%"; when to buy now (stable job, enough equity, a good deal, a 10-year horizon) and when to wait.
- **Related:** תחזית מחירי הדירות 2026 · מגדל עם 109 דירות ריקות · מדלן · מגדלי הים התיכון.
- **Reading:** Madlan's "what waiting really costs" is the only tool-shaped answer. This intent belongs on the prices hub; the buying hub links it.

## D. Buyer-status and structure family

### 21. קניית דירה ראשונה (re-load)
- **Organic:** yonilevy "5 טיפים" · amitvered · lazyinvestor "הדרך לדירה ראשונה" · shikum.mod.gov.il · fingrow · tidhar · kolzchut "חישוב מס רכישה" · Discount · Leumi. Same as the first pass.
- **AI: present.** 75% financing; brackets "נכון לינואר 2024 – ינואר 2028" per Kol Zchut: up to ₪1,978,745 0% · to ₪2,347,040 3.5% · to ₪6,055,070 5% · to ₪20,183,565 8% · above 10%; broker 1–2% plus VAT. (Our ptax.json records the brackets as effective 16.1.2025 and frozen until 15.1.2028: the AI's date range needs checking.)
- **Related:** unchanged (סיוע ברכישת דירה נכות כללית · מענק לרכישת דירה ראשונה למחוסרי דיור · הדרך לדירה ראשונה · סיוע ברכישת דירה ראשונה …).

### 22. קניית דירה עם שותפים [videos] (from autocomplete)
- **Organic:** yonilevy (an investment property with a partner) · brikman-law "משתלם לרכוש דירה בשותפות" · ashlaw "מה הסיכונים?" · calcalist "לקנות דירה להשקעה עם שותפים" · themarker (15.4.2025) · rivkit.co.il "האם אפשר לקחת משכנתא בנפרד?" · din.co.il forum on purchase tax · mli-law.co.il.
- **AI: present.** Pros: lower equity per partner. Cons: banks give one joint mortgage, "כל שותף אחראי על מלוא החזר ההלוואה"; financing is capped (often 50%) if a partner already owns a flat; inheritance and partition disputes. Purchase tax: the rate follows each partner's own status.
- **Related:** קניית דירה בשותפות מס רכישה · רבע דירה מס רכישה · רכישת דירה שלישית · שליש דירה באותו בניין · שליש דירה במתנה · שליש דירה יתרונות וחסרונות · הוראת ביצוע שליש דירה · מס רכישה 1/3 דירה.

### 23. קניית דירה ידועים בציבור
- **Organic:** gov.il "הגדרת המונח 'ידועים בציבור'" (housing-eligibility definition) · kolzchut (property division) · ashlaw · rotenberglaw.co.il "ידועים בציבור דירה" · todivorce.co.il · lawreviews.co.il "הסכם ממון ידועים בציבור" · isaving.co.il (Ministry programmes) · yonilevy · gerushin.co.il.
- **AI:** present, still generating at capture.
- **Related:** חזקת השיתוף ידועים בציבור · **תצהיר ידועים בציבור מחיר למשתכן** · ידועים בציבור ביטוח לאומי · הסכם ידועים בציבור · טופס ידועים בציבור להורדה · העברה ללא תמורה בין בני זוג · ידוע בציבור · ביטול ידועים בציבור.
- **Reading:** family-law intent (property split) plus housing-programme eligibility. The hub only needs a short "buying as a couple" item (whose name, a cohabitation agreement, programme declarations).

### 24. קניית דירה מתושב חוץ
- **Organic (Google reads it as buying *by* a foreign resident):** amitvered "קניית דירה תושב חוץ - מדריך 2026" · y-tax.co.il "מס רכישה לתושבי חוץ" · yonilevy (land) · yeshnadlan.co.il · barlaw.co.il · yasmint-law PDF guide · elkayamlaw (selling by a foreign resident) · gov.il Tax Authority FAQ for new immigrants · klikatnadlan.
- **AI: present.** A foreign resident gets no single-home brackets: 8% up to ₪6,055,070 and 10% above; pay within 60 days.
- **Related:** מחשבון מס רכישה תושב חוץ · פטור מס רכישה תושב חוץ · מס שבח תושב חוץ · רכישת דירה לתושב חוץ · מס רכישה עולה חדש · הגדרת תושב חוץ · מס מכירת דירה תושב חוץ.
- **Gap:** the Israeli buyer who buys *from* a foreign-resident seller (withholding, a capital-gains approval before paying) has no page anywhere in the SERP.

---

## Numbers the AI answers quote (verify every one before publishing)
| Claim | Where | Status |
|---|---|---|
| Financing caps: 75% single / first home, 70% improver, 50% additional; "או 10% במחיר למשתכן" for equity | 6 searches | matches nrm.json (BoI Directive 329); the 10% claim needs a source |
| Investment flat "עד 75%" | קניית דירה להשקעה | **contradicts** the 50% elsewhere: an AI error |
| Monthly repayment ≤ one third of disposable income | איך קונים דירה, הדרך לדירה ראשונה | a rule of thumb; the BoI PTI rule is different (mneches.json) |
| At least one third fixed rate; up to 30 years | קניית דירה עם משכנתא | check against BoI |
| Purchase-tax declaration and payment: "תוך 60 יום" / "או 30 יום" / registration form "תוך כ-40 יום" | תהליך, מקבלן | **inconsistent**; verify against the Tax Authority |
| Brackets 0 / 3.5 / 5 / 8 / 10% at 1,978,745 / 2,347,040 / 6,055,070 / 20,183,565 | ראשונה, להשקעה, תושב חוץ | matches ptax.json; effective-date wording differs |
| No payment over 7% to a developer without a Sale Law guarantee | מקבלן, על הנייר, ערבות בנקאית | matches the Sale Law (bank-guarantee page) |
| Delay compensation beyond 60 days | מקבלן | check the Sale Law amendment wording |
| Payment caps by construction stage (7–15 / 20 / 40 / 60 / 75 / 85 / 100%) | קניית דירה מקבלן תשלומים (Kol Zchut) | needs the regulation text |
| Developer's lawyer fee cap ~₪5,915 plus VAT or 0.5% | עורך דין קניית דירה מחיר | **matches orechdin.json** (5,915; 0.5%; 2026) |
| Lawyer 0.5–1.5% plus VAT | same | consistent with cost.json (0.5–1%) |
| Second-hand grant up to ₪50,000 for flats of ₪300,000–600,000 | מענק… למחוסרי דיור | Ministry programme; verify current terms |
| Prices down ~1.5–1.8% y/y; ~84,000 unsold new flats; BoI rate 3.25% | עכשיו או לחכות | BoI rate matches boi-rate.json; the rest need CBS / Finance Ministry dates |
| Rent-income exemption ~₪5,654 a month; yield 2.4–4.1% | להשקעה | verify (Tax Authority; our invest.json) |
| Building-offence limitation 5 years; betterment levy ~50% | חריגות בנייה | legal; cite the law |
| Amidar purchase law expired February 2023; a bill passed first reading | מעמידר | Knesset press release 18.11.2025 |
