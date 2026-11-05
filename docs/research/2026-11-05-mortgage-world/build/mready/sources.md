# mready: sources of the documents list (HAD-675)

Built 5.11.2026 for the tool "מוכנים לאישור עקרוני?" (`mready`). Every document item in `mready.json` lists its sources here, with the
URL and the retrieval time (UTC; Israel time = UTC+2). Pages were fetched with Python `urllib` (`python -I`, browser user agent) and their
text extracted (PDFs with PyMuPDF); raw copies stay in the session scratchpad, not in the repo.

**The label rule.** An item is shown as a plain item ("common") only when at least two independent groups state it and at least one of them is
a bank, Kol Zchut or the Bank of Israel. Discount and Mercantile count as one group (Mercantile is in the Discount group and its forms page
repeats the Discount list); every Leumi page, including the Bizportal interview made with Leumi Mortgages, counts as one group. Anything else
carries the tag **"יש בנקים שמבקשים"**. `test_mready.js` re-derives every label from this rule.

**Blocked or partial.** `boi.org.il` answered Python with a Radware bot check (126 characters, 20:16Z and 20:20Z); the two Bank of Israel
documents were read with WebFetch instead (the appendix 4 PDF was saved by WebFetch and extracted locally). Mizrahi-Tefahot keeps its lists in
PDFs linked from the page (read). No bank page refused a script. No bank publishes a gift letter in its own list: that item is press only and
carries the tag.

## The sources

| id | publisher | page | retrieved (UTC) |
|---|---|---|---|
| `kz_aip` | כל זכות | [אישור עקרוני למשכנתא בנקאית](https://www.kolzchut.org.il/he/אישור_עקרוני_למשכנתא_בנקאית) | 2026-11-05 20:16:27 |
| `kz_cert` | כל זכות | [הוצאת תעודת זכאות למשכנתא](https://www.kolzchut.org.il/he/הוצאת_תעודת_זכאות_למשכנתא) | 2026-11-05 20:19:18 |
| `kz_oleh` | כל זכות | [סיוע ברכישת דירה (משכנתא) לעולים](https://www.kolzchut.org.il/he/סיוע_ברכישת_דירה_%28משכנתא%29_לעולים) | 2026-11-05 20:19:17 |
| `hap_steps` | בנק הפועלים | [ארבעת השלבים בדרך למשכנתא](https://www.bankhapoalim.co.il/he/mortgage/steps) | 2026-11-05 20:16:27 |
| `hap_guide` | בנק הפועלים | [המדריך למשכנתא (PDF)](https://www.bankhapoalim.co.il/sites/default/files/media/PDFS/mortgage/mortgage_updated_guide.pdf) | 2026-11-05 20:16:28 |
| `leumi_info` | בנק לאומי | [המידע הנדרש לצורך הגשת בקשה למשכנתא](https://www.leumi.co.il/he/Articles/50138) | 2026-11-05 20:16:28 |
| `leumi_tadrich` | לאומי למשכנתאות | [תדריך ללווים בנושא קבלת הלוואה (PDF)](https://mortgage.leumi.co.il/mortgage/s3fs-public/doc/tadrich_lovim_acc.pdf) | 2026-11-05 20:16:30 |
| `leumi_coll` | בנק לאומי | [רשימת בטחונות מלאה](https://www.leumi.co.il/he/Mortgage1/Complete-Collateral-List) | 2026-11-05 20:16:30 |
| `leumi_foreign` | ביזפורטל, בשיתוף לאומי למשכנתאות | [משכנתא לתושבי חוץ: כך תרכשו נכס בישראל (ראיון עם מנהלת סניף המשכנתאות לתושבי חוץ בלאומי)](https://www.bizportal.co.il/mortgage_arena/news/article/20030478) | 2026-11-05 20:20:11 |
| `miz_docs` | מזרחי טפחות | [מסמכים להגשת בקשה למשכנתא](https://www.mizrahi-tefahot.co.il/mortgages/takemortgagelib/mortgage-documents/) | 2026-11-05 20:16:31 |
| `miz_borrowers` | מזרחי טפחות | [מסמכים דרושים הנוגעים למבקשי ההלוואה (PDF)](https://www.mizrahi-tefahot.co.il/media/fhjkotsk/מסמכים-דרושים-הנוגעים-למבקשי-ההלוואה.pdf) | 2026-11-05 20:16:58 |
| `miz_guar` | מזרחי טפחות | [מסמכים דרושים הנוגעים לערבים (PDF)](https://www.mizrahi-tefahot.co.il/media/rvujhxmo/מסמכים-דרושים-הנוגעים-לערבים.pdf) | 2026-11-05 20:16:59 |
| `miz_lien` | מזרחי טפחות | [מסמכים ופעולות הדרושים לשעבוד הנכס (PDF)](https://www.mizrahi-tefahot.co.il/media/ayhhsacz/מסמכים-ופעולות-הדרושים-לשעבוד-הנכס.pdf) | 2026-11-05 20:16:59 |
| `miz_en` | Mizrahi-Tefahot | [All you need to know about the Mortgage (Q&A, English)](https://www.mizrahi-tefahot.co.il/en/about-mizrahi-tefahot/qa-mortgages-in-israel/) | 2026-11-05 20:19:16 |
| `disc_list` | בנק דיסקונט | [רשימת המסמכים לבחינת אישור הלוואת משכנתא (PDF)](https://mortgage.discountbank.co.il/media/ewvppwmr/loan_doc_list.pdf) | 2026-11-05 20:17:32 |
| `disc_aip` | בנק דיסקונט | [איך מקבלים אישור עקרוני למשכנתא](https://mortgage.discountbank.co.il/what-is-mortgage/principle-approval) | 2026-11-05 20:16:59 |
| `merc_forms` | בנק מרכנתיל (קבוצת דיסקונט) | [טפסים ואישורים להגשת בקשה למשכנתא](https://mortgage.mercantile.co.il/general/forms) | 2026-11-05 20:17:33 |
| `merc_aip` | בנק מרכנתיל (קבוצת דיסקונט) | [איך מוציאים אישור עקרוני למשכנתא?](https://mortgage.mercantile.co.il/guide/principal-approval) | 2026-11-05 20:17:33 |
| `jer_guide` | בנק ירושלים | [מדריך לקבלת משכנתא, מרץ 2026 (PDF)](https://www.bankjerusalem.co.il/media/6832/madrich-mashcanta-march2026-57368-2.pdf) | 2026-11-05 20:17:35 |
| `jer_process` | בנק ירושלים | [אישור עקרוני למשכנתא: תהליך](https://www.bankjerusalem.co.il/mortgage/mortgage-guide/process) | 2026-11-05 20:17:33 |
| `fibi_tadrich` | הבנק הבינלאומי | [תדריך ללווה, הלוואות לדיור (PDF)](https://www.fibi.co.il/media/o4clxkis/תדריך-ללוה-הלוואות-לדיור.pdf) | 2026-11-05 20:16:32 |
| `boi_format` | בנק ישראל | [תוספת 4: דף הסבר למבקש הלוואה ופורמט אישור עקרוני (PDF)](https://www.boi.org.il/media/tjujh4ms/פורמט-אישור-עקרוני.pdf) | 2026-11-05 20:21:55 |
| `boi_pr` | בנק ישראל | [רפורמה צרכנית בשוק המשכנתאות (הודעה לעיתונות, 14.11.2021)](https://www.boi.org.il/publications/pressreleases/בנק-ישראל-מודיע-על-קידום-רפורמה-צרכנית-להגברת-שקיפות-המידע-ללקוחות-הבנקים-ולשיפור-סביבת-התחרות-בשוק-המשכנתאות/) | 2026-11-05 20:21:30 |
| `press_biz` | ביזפורטל | [הורים שעוזרים במשכנתא: הבנקים יכירו בחצי בלבד מההכנסה שלהם](https://www.bizportal.co.il/realestates/news/article/20047080) | 2026-11-05 20:20:11 |
| `press_hon` | הון | [עזרה מההורים בקניית דירה: מתנה, הלוואה או ערבות](https://www.hon.co.il/parents-help-buying-apartment/) | 2026-11-05 20:25:02 |

## What each source says (paraphrase, short quotes)

- `kz_aip`: page: valid at least 24 days, free, no obligation; documents are not required but help (payslips, bank statements, sale contract); with the approval the bank hands a list of documents and a date, and a list of approved appraisers
- `kz_cert`: page: eligibility certificate documents: ID with appendix, army or national service months, siblings IDs or details; marriage certificate for married couples
- `kz_oleh`: page: oleh with a valid oleh certificate; for the eligibility certificate: oleh certificate, IDs, army service where relevant, marriage certificate
- `hap_steps`: stage 3 list: "תעודת זהות + ספחים", "לשכיר 3 תלושי שכר אחרונים", "לעצמאי שומת מס אחרונה / אישור רו"ח", "תדפיסי עו"ש של 3 החודשים האחרונים", "תדפיס יתרת הלוואות קיימות", "חוזה רכישה", "נסח טאבו ... או אישור זכויות", "תעודת זכאות", "הוכחת הון עצמי", bank appraiser; stage 4: life and structure insurance with the bank as beneficiary
- `hap_guide`: PDF list: ID + personal details appendix; salaried 3 payslips; salaried company owner 4 payslips, form 106, CPA approval, tax assessment; self employed CPA approval + tax assessment; original current account statements of 3 months from all accounts; existing loans balance printout; purchase contract; tabu extract or rights confirmation; life and structure insurance; irrevocable debit order from the account bank
- `leumi_info`: page: the data needed for a request: ID and personal details, account, occupation and income, savings and liabilities, the property; tabu extract or rights confirmation by the registering body; further documents may be asked
- `leumi_tadrich`: PDF: the document list is not closed; guarantors: income approvals, bank statements and loan details; appraisal from the bank list; registration of a mortgage or a warning note for the bank and an approved extract after it; debit authorization; documents for the eligibility certificate (ID with appendix, marriage, army service)
- `leumi_coll`: page: full collateral list by registration: pledge of the borrowers rights at the pledges registrar, notarized irrevocable power of attorney, seller commitment and warning notes, pledges register extracts on the seller, contractor commitment, the voucher booklet of the accompanying bank, Sale Law guarantee or policy and its assignment, appraisal, letter of intent from the creditor if the home is under a lien; "not a closed list"
- `leumi_foreign`: Bizportal interview made with Leumi Mortgages: foreign residents bring wider documents: proofs of income from abroad, bank reports, tax approvals, sometimes a notarized translation; a local representative with a power of attorney can act
- `miz_docs`: page: the tabu extract can be produced on the Ministry of Justice site and emailed, free
- `miz_borrowers`: PDF: valid Israeli ID; foreign citizen: passport and a further valid photo ID; salaried: payslips of 3 months + form 106 for the previous year; self employed: tax assessment for the previous year + CPA approval for the current year; controlling shareholder: approved assessment, CPA form 3806, audited report, trial balance; current account statements of 3 months for every account; loan balances report; signed application form; Housing Ministry eligibility certificate
- `miz_guar`: PDF for guarantors: ID (or passport + photo ID), payslips of 3 months, or tax assessment and CPA approval
- `miz_lien`: PDF: per registration type: mortgage pledge deed, pledge notice registered at the pledges registrar, notarized irrevocable power of attorney, commitment to register a mortgage signed by the seller or by the contractor and the registered owners, warning notes for the buyer and for the bank, Sale Law guarantee assigned to the bank, the payment voucher booklet of the accompanying bank
- `miz_en`: English Q&A: foreign citizen LTV 50%; proof of a monthly income (in Israel or abroad); the bank is legally obligated to check the origins of the funds and the income, so all relevant documentation is needed
- `disc_list`: PDF: IDs with the personal details appendix of all borrowers and guarantors; statements of all accounts for the 3 months before the request; eligibility certificate; purchase contract with appendices; rights confirmation or tabu extract; salaried: 3 last payslips, under 12 months seniority also the last payslip of the previous employer, company insider adds audited balance sheet and tax assessment; self employed: last tax assessment + CPA or tax adviser approval for the current year; existing mortgage at another bank: balances and 24 months of payments; mortgage transfer: the sale contract of the property the mortgage moves from; eligibility: oleh certificate, marriage certificate, army or national service, siblings details; bringing all documents is not a condition for an approval in principle
- `disc_aip`: page: later in the deal further documents: appraisal, life and property insurance policy, mortgage deed registration, notary approval
- `merc_forms`: Mercantile (Discount group) forms page: the same salaried / self employed / mortgage transfer list as the Discount PDF
- `merc_aip`: page: generally no documents are needed for the approval in principle, it relies on the client declarations; valid 24 days from the bank signature (guide/before-the-mortgage); free and not binding
- `jer_guide`: PDF March 2026: ID matching the population register; foreign resident: valid passport + a further valid ID, an irrevocable power of attorney if a representative acts, otherwise a stay visa; consent to the credit data register; salaried 3 months payslips; self employed: last tax assessment, VAT reports, CPA approval; current account statements of 3 months; eligibility certificate; guarantors: ID + income approvals; tabu extract or housing company approval; pledges register extract for a second hand home not yet registered to the sellers; contract; appraisal; release of the seller lien; Sale Law guarantee assignment; debit authorization; life insurance; oleh certificate (for the eligibility certificate)
- `jer_process`: 
- `fibi_tadrich`: PDF: purchase contract; tabu extract or housing company / ILA approval; salaried: 3 last payslips and bank statements of 3 months, in some cases form 106; self employed: last income tax assessment and CPA or tax adviser approval for the current year; eligibility certificate for directed loans
- `boi_format`: Directive appendix 4 (approval format): the approval is based on the data you provided
- `boi_pr`: press release 14.11.2021: uniform approval format with three uniform baskets, online requests
- `press_biz`: article: the bank wants to see where the money came from: usually a signed gift letter (no repayment duty) and statements showing the source, also for anti money laundering rules
- `press_hon`: guide: what the bank wants to see: the source of the money and a transfer printout from the parents; a gift letter stating there is no repayment duty

## The approval in principle (facts shown in the tool)

- Valid at least 24 days: `kz_aip`, `hap_steps`, `merc_aip`.
- Free and not binding: `kz_aip`, `merc_aip`.
- Documents are not a condition for the approval; they speed the check: `kz_aip`, `disc_list`, `merc_aip`.
- Based on the data the applicant gave: `boi_format`, `hap_steps`.
- The limits: `boi-mortgage-v2.json` key `rules` (directive 329, version 13 of 30.6.2026): payment up to 50% of the disposable income, the
  40% capital threshold, LTV 75% single home, 70% replacement home, 50% additional home. Oleh 75% and foreign resident 50%: `cost.json`
  (the site data used by afford.js); foreign 50% also stated by `miz_en`. Purchase tax: `ptax.json` (Tax Authority brackets, checked
  25.10.2026). Lawyer 0.5% + VAT 18%: `cost.json`. Rate: Bank of Israel all-banks average mix (`by_bank`, 9.2026).

## Every document item

### לאישור העקרוני

**`id_il`** תעודת זהות עם הספח
- shown when: `{"buyer": ["single", "replace", "extra", "oleh"]}`
- sources: `hap_steps` (בנק הפועלים, 20:16Z) · `hap_guide` (בנק הפועלים, 20:16Z) · `miz_borrowers` (מזרחי טפחות, 20:16Z) · `disc_list` (בנק דיסקונט, 20:17Z) · `jer_guide` (בנק ירושלים, 20:17Z)

**`id_foreign`** דרכון בתוקף ועוד מסמך מזהה בתוקף עם תמונה
- shown when: `{"buyer": ["foreign"]}`
- sources: `miz_borrowers` (מזרחי טפחות, 20:16Z) · `jer_guide` (בנק ירושלים, 20:17Z)

**`app_form`** טופס הבקשה למשכנתא של הבנק, מלא וחתום
- sources: `miz_borrowers` (מזרחי טפחות, 20:16Z) · `disc_list` (בנק דיסקונט, 20:17Z)

**`bank3`** דפי חשבון העו״ש של 3 החודשים האחרונים, מכל החשבונות
- sources: `hap_steps` (בנק הפועלים, 20:16Z) · `hap_guide` (בנק הפועלים, 20:16Z) · `miz_borrowers` (מזרחי טפחות, 20:16Z) · `disc_list` (בנק דיסקונט, 20:17Z) · `jer_guide` (בנק ירושלים, 20:17Z) · `fibi_tadrich` (הבנק הבינלאומי, 20:16Z) · `kz_aip` (כל זכות, 20:16Z)

**`pay3`** 3 תלושי השכר האחרונים
- shown when: `{"type": ["salaried", "both"]}`
- sources: `hap_steps` (בנק הפועלים, 20:16Z) · `miz_borrowers` (מזרחי טפחות, 20:16Z) · `disc_list` (בנק דיסקונט, 20:17Z) · `jer_guide` (בנק ירושלים, 20:17Z) · `fibi_tadrich` (הבנק הבינלאומי, 20:16Z) · `merc_forms` (בנק מרכנתיל (קבוצת דיסקונט), 20:17Z)

**`f106`** טופס 106 של השנה הקודמת
- shown when: `{"type": ["salaried", "both"]}`
- sources: `miz_borrowers` (מזרחי טפחות, 20:16Z) · `fibi_tadrich` (הבנק הבינלאומי, 20:16Z)

**`prev_job`** אם הוותק בעבודה הנוכחית פחות מ־12 חודשים: תלוש שכר אחרון ממקום העבודה הקודם **(יש בנקים שמבקשים)**
- shown when: `{"type": ["salaried", "both"]}`
- sources: `disc_list` (בנק דיסקונט, 20:17Z) · `merc_forms` (בנק מרכנתיל (קבוצת דיסקונט), 20:17Z)

**`ctrl`** אם אתם בעלי שליטה בחברה שמעסיקה אתכם: דוחות כספיים מבוקרים של החברה ושומת המס האחרונה
- shown when: `{"type": ["salaried", "both"]}`
- sources: `miz_borrowers` (מזרחי טפחות, 20:16Z) · `disc_list` (בנק דיסקונט, 20:17Z) · `hap_guide` (בנק הפועלים, 20:16Z) · `merc_forms` (בנק מרכנתיל (קבוצת דיסקונט), 20:17Z)

**`tax_assess`** שומת המס האחרונה
- shown when: `{"type": ["self", "both"]}`
- sources: `hap_steps` (בנק הפועלים, 20:16Z) · `miz_borrowers` (מזרחי טפחות, 20:16Z) · `disc_list` (בנק דיסקונט, 20:17Z) · `jer_guide` (בנק ירושלים, 20:17Z) · `fibi_tadrich` (הבנק הבינלאומי, 20:16Z)

**`cpa`** אישור רואה חשבון על ההכנסה בשנת המס הנוכחית, בנוסח של הבנק
- shown when: `{"type": ["self", "both"]}`
- sources: `miz_borrowers` (מזרחי טפחות, 20:16Z) · `disc_list` (בנק דיסקונט, 20:17Z) · `jer_guide` (בנק ירושלים, 20:17Z) · `fibi_tadrich` (הבנק הבינלאומי, 20:16Z) · `hap_guide` (בנק הפועלים, 20:16Z)

**`vat`** דוחות מע״מ **(יש בנקים שמבקשים)**
- shown when: `{"type": ["self", "both"]}`
- sources: `jer_guide` (בנק ירושלים, 20:17Z)

**`loans_report`** דוח יתרות של ההלוואות הקיימות
- shown when: `{"loans": true}`
- sources: `hap_steps` (בנק הפועלים, 20:16Z) · `hap_guide` (בנק הפועלים, 20:16Z) · `miz_borrowers` (מזרחי טפחות, 20:16Z) · `disc_list` (בנק דיסקונט, 20:17Z)

**`savings_proof`** אישור על ההון העצמי: יתרות בחשבונות, בפיקדונות ובחסכונות
- shown when: `{"equity": ["savings"]}`
- sources: `hap_steps` (בנק הפועלים, 20:16Z) · `miz_en` (Mizrahi-Tefahot, 20:19Z) · `leumi_info` (בנק לאומי, 20:16Z)

**`gift_trail`** תדפיס חשבון שמראה את העברת הכסף מהמשפחה ומאיפה הגיע
- shown when: `{"equity": ["gift"]}`
- sources: `miz_en` (Mizrahi-Tefahot, 20:19Z) · `press_biz` (ביזפורטל, 20:20Z) · `press_hon` (הון, 20:25Z)

**`gift_letter`** מכתב מתנה חתום: הסכום ניתן בלי חובת החזר **(יש בנקים שמבקשים)**
- shown when: `{"equity": ["gift"]}`
- sources: `press_biz` (ביזפורטל, 20:20Z) · `press_hon` (הון, 20:25Z)

**`sale_contract`** חוזה המכירה של הדירה הנוכחית **(יש בנקים שמבקשים)**
- shown when: `{"any": [{"equity": ["sale"]}, {"buyer": ["replace"]}]}`
- sources: `disc_list` (בנק דיסקונט, 20:17Z) · `merc_forms` (בנק מרכנתיל (קבוצת דיסקונט), 20:17Z)

**`old_mortgage`** אם יש משכנתא על הדירה הנוכחית: דוח יתרות ופירוט התשלומים של 24 החודשים האחרונים במשכנתא הקיימת **(יש בנקים שמבקשים)**
- shown when: `{"any": [{"equity": ["sale"]}, {"buyer": ["replace"]}]}`
- sources: `disc_list` (בנק דיסקונט, 20:17Z)

**`elig`** תעודת זכאות ממשרד הבינוי והשיכון
- shown when: `{"any": [{"buyer": ["oleh"]}, {"equity": ["grant"]}]}`
- sources: `hap_steps` (בנק הפועלים, 20:16Z) · `miz_borrowers` (מזרחי טפחות, 20:16Z) · `disc_list` (בנק דיסקונט, 20:17Z) · `jer_guide` (בנק ירושלים, 20:17Z) · `fibi_tadrich` (הבנק הבינלאומי, 20:16Z) · `kz_cert` (כל זכות, 20:19Z)

**`elig_opt`** אם אתם זכאים לסיוע מהמדינה: תעודת זכאות ממשרד הבינוי והשיכון
- shown when: `{"buyer": ["single"], "noequity": ["grant"]}`
- sources: `hap_steps` (בנק הפועלים, 20:16Z) · `miz_borrowers` (מזרחי טפחות, 20:16Z) · `disc_list` (בנק דיסקונט, 20:17Z) · `jer_guide` (בנק ירושלים, 20:17Z) · `fibi_tadrich` (הבנק הבינלאומי, 20:16Z) · `kz_cert` (כל זכות, 20:19Z)

**`elig_docs`** לתעודת הזכאות: אישור על שירות צבאי או לאומי, תעודת נישואין לזוג נשוי, ופרטי האחים והאחיות
- shown when: `{"any": [{"buyer": ["oleh"]}, {"equity": ["grant"]}]}`
- sources: `kz_cert` (כל זכות, 20:19Z) · `kz_oleh` (כל זכות, 20:19Z) · `disc_list` (בנק דיסקונט, 20:17Z) · `jer_guide` (בנק ירושלים, 20:17Z)

**`oleh_cert`** תעודת עולה
- shown when: `{"buyer": ["oleh"]}`
- sources: `kz_oleh` (כל זכות, 20:19Z) · `disc_list` (בנק דיסקונט, 20:17Z) · `jer_guide` (בנק ירושלים, 20:17Z)

**`foreign_income`** אישורי הכנסה מארץ המגורים
- shown when: `{"buyer": ["foreign"]}`
- sources: `leumi_foreign` (ביזפורטל, בשיתוף לאומי למשכנתאות, 20:20Z) · `miz_en` (Mizrahi-Tefahot, 20:19Z)

**`foreign_tax`** אישורי מס מארץ המגורים **(יש בנקים שמבקשים)**
- shown when: `{"buyer": ["foreign"]}`
- sources: `leumi_foreign` (ביזפורטל, בשיתוף לאומי למשכנתאות, 20:20Z)

**`foreign_transl`** תרגום נוטריוני של מסמכים מחו״ל **(יש בנקים שמבקשים)**
- shown when: `{"buyer": ["foreign"]}`
- sources: `leumi_foreign` (ביזפורטל, בשיתוף לאומי למשכנתאות, 20:20Z)

**`foreign_poa`** אם מיופה כוח פועל בשמכם בישראל: ייפוי כוח למיופה הכוח
- shown when: `{"buyer": ["foreign"]}`
- sources: `jer_guide` (בנק ירושלים, 20:17Z) · `leumi_foreign` (ביזפורטל, בשיתוף לאומי למשכנתאות, 20:20Z)

**`foreign_visa`** אם אין מיופה כוח: אשרת שהייה בישראל **(יש בנקים שמבקשים)**
- shown when: `{"buyer": ["foreign"]}`
- sources: `jer_guide` (בנק ירושלים, 20:17Z)

**`credit_consent`** חתימה על הסכמה לבדיקה במאגר נתוני האשראי **(יש בנקים שמבקשים)**
- sources: `jer_guide` (בנק ירושלים, 20:17Z)

### למשכנתא עצמה, אחרי האישור

**`contract`** חוזה הרכישה החתום, עם כל הנספחים
- sources: `hap_steps` (בנק הפועלים, 20:16Z) · `hap_guide` (בנק הפועלים, 20:16Z) · `disc_list` (בנק דיסקונט, 20:17Z) · `jer_guide` (בנק ירושלים, 20:17Z) · `fibi_tadrich` (הבנק הבינלאומי, 20:16Z) · `kz_aip` (כל זכות, 20:16Z)

**`tabu`** נסח טאבו עדכני, או אישור זכויות מרשות מקרקעי ישראל או מהחברה המשכנת, לפי מקום הרישום
- sources: `hap_steps` (בנק הפועלים, 20:16Z) · `disc_list` (בנק דיסקונט, 20:17Z) · `jer_guide` (בנק ירושלים, 20:17Z) · `fibi_tadrich` (הבנק הבינלאומי, 20:16Z) · `leumi_info` (בנק לאומי, 20:16Z) · `miz_docs` (מזרחי טפחות, 20:16Z)

**`appraisal`** הערכת שמאי מרשימת השמאים של הבנק
- sources: `hap_steps` (בנק הפועלים, 20:16Z) · `disc_list` (בנק דיסקונט, 20:17Z) · `jer_guide` (בנק ירושלים, 20:17Z) · `leumi_coll` (בנק לאומי, 20:16Z) · `leumi_tadrich` (לאומי למשכנתאות, 20:16Z) · `kz_aip` (כל זכות, 20:16Z)

**`insurance`** ביטוח חיים וביטוח מבנה, עם הבנק כמוטב
- sources: `hap_steps` (בנק הפועלים, 20:16Z) · `hap_guide` (בנק הפועלים, 20:16Z) · `disc_aip` (בנק דיסקונט, 20:16Z) · `jer_guide` (בנק ירושלים, 20:17Z)

**`debit`** הרשאה לחיוב חשבון העו״ש בתשלום החודשי
- sources: `hap_guide` (בנק הפועלים, 20:16Z) · `leumi_tadrich` (לאומי למשכנתאות, 20:16Z) · `jer_guide` (בנק ירושלים, 20:17Z)

**`lien`** רישום משכנתא או הערת אזהרה לטובת הבנק, ונסח מעודכן אחרי הרישום
- sources: `miz_lien` (מזרחי טפחות, 20:16Z) · `leumi_coll` (בנק לאומי, 20:16Z) · `leumi_tadrich` (לאומי למשכנתאות, 20:16Z) · `jer_guide` (בנק ירושלים, 20:17Z)

**`pledge`** משכון הזכויות לטובת הבנק ברשם המשכונות
- sources: `miz_lien` (מזרחי טפחות, 20:16Z) · `leumi_coll` (בנק לאומי, 20:16Z)

**`poa_bank`** ייפוי כוח נוטריוני בלתי חוזר לטובת הבנק
- sources: `miz_lien` (מזרחי טפחות, 20:16Z) · `leumi_coll` (בנק לאומי, 20:16Z)

**`dev_commit`** כתב התחייבות של הקבלן לרישום משכנתא לטובת הבנק
- shown when: `{"market": ["new"]}`
- sources: `miz_lien` (מזרחי טפחות, 20:16Z) · `leumi_coll` (בנק לאומי, 20:16Z)

**`salelaw`** ערבות חוק המכר, או פוליסת ביטוח לפי החוק, מוסבת לבנק
- shown when: `{"market": ["new"]}`
- sources: `miz_lien` (מזרחי טפחות, 20:16Z) · `leumi_coll` (בנק לאומי, 20:16Z) · `jer_guide` (בנק ירושלים, 20:17Z)

**`vouchers`** פנקס שוברי התשלום מהבנק המלווה של הפרויקט
- shown when: `{"market": ["new"]}`
- sources: `miz_lien` (מזרחי טפחות, 20:16Z) · `leumi_coll` (בנק לאומי, 20:16Z)

**`seller_commit`** כתב התחייבות של המוכר לרישום משכנתא לטובת הבנק
- shown when: `{"market": ["used"]}`
- sources: `miz_lien` (מזרחי טפחות, 20:16Z) · `leumi_coll` (בנק לאומי, 20:16Z)

**`warn_notes`** הערות אזהרה בטאבו: לטובתכם על הרכישה, ולטובת הבנק
- shown when: `{"market": ["used"]}`
- sources: `miz_lien` (מזרחי טפחות, 20:16Z) · `leumi_coll` (בנק לאומי, 20:16Z)

**`pledges_seller`** דפי עיון מרשם המשכונות על שם המוכר
- shown when: `{"market": ["used"]}`
- sources: `leumi_coll` (בנק לאומי, 20:16Z) · `jer_guide` (בנק ירושלים, 20:17Z)

**`seller_lien`** אם הדירה משועבדת לבנק של המוכר: מכתב כוונות מהבנק של המוכר, או אישור על סילוק השעבוד
- shown when: `{"market": ["used"]}`
- sources: `leumi_coll` (בנק לאומי, 20:16Z) · `jer_guide` (בנק ירושלים, 20:17Z)

**`guarantors`** אם הבנק מבקש ערבים: תעודת זהות, אישורי הכנסה ודפי חשבון של הערבים
- sources: `miz_guar` (מזרחי טפחות, 20:16Z) · `jer_guide` (בנק ירושלים, 20:17Z) · `leumi_tadrich` (לאומי למשכנתאות, 20:16Z) · `disc_list` (בנק דיסקונט, 20:17Z)

## Read but left out (one source only, or outside the five questions)

- A sample cheque of the paying account (`miz_borrowers` only). Statements printed from the internet are refused (`disc_list` only).
- Income from alimony, rent or allowances (`miz_borrowers`; rent also `disc_list`): the five questions do not ask about other income.
- Pregnancy, disability and single parent papers for the eligibility certificate (`kz_cert`, `jer_guide`): case details the tool does not ask.
- Self build, development contract, receiver or estate sales, trustee and power of attorney sales (`disc_list`, `fibi_tadrich`).
- A credit report from the country of residence and an Israeli bank account for foreign residents: found only on broker and press pages.
- Discount asks for a tabu extract issued within one month of the request (`disc_list` only).
