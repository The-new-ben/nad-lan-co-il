# Spec: "בדיקת משכנתא לפני חתימה" (pre-signing check), to beat every tool found

Research only, 6.11.2026. Rules quoted from primary texts read today: directive 451 version 22 (7/23, the current file
https://boi.org.il/media/utld2tgp/451.pdf; our page still links version 20, 1/22), directive 329 version 13 (circular 2852,
30.6.2026), צו הבנקאות (פירעון מוקדם של הלוואה לדיור), התשס"ב-2002 (Nevo text, sub-agent), BoI קו המשווה (Power BI, data month
2026-09). Anything else is marked **unverified**.

## 1. Why this tool, and who has what today

| Who | What it does | Gap we close |
|---|---|---|
| arielmash.com | Paid service "בדיקת משכנתא לפני חתימה" from 3,000 ₪ incl. VAT, 5 checks by a human; a free two-offer worksheet | Free, instant, every check sourced |
| YC משכנתאות | Article with 7 checks, a table "נתון בהצעה / השאלה / למה זה חשוב", official sources | A tool that runs the checks on the user's numbers |
| Supermarker | Step 4 "קיבלתם הצעה מהבנק?": rate per track against the BoI average, gap in shekels | Reads the whole approval, not only rates |
| Banks (Hapoalim, Leumi, Mizrahi) | Show the 4 numbers per uniform basket for their own price | Cross-bank, and the user's real approval |
| BoI קו המשווה | IRR and mix per bank per month | Personal comparison against it |
| CFPB Loan Estimate / Closing Disclosure explainers | Field-by-field "Actions to take", final document diffed against the offer, wire-fraud warning, "walk away" | The Israeli equivalent built on the 451 format |
| EU ESIS | Fixed sections incl. validity date, worst-case payment, linked insurance, exit cost, default consequences | Same items mapped to Israeli law |
| Ours today | `moffers` (4 numbers x 3 baskets x 2 to 3 banks, each against its own bank's BoI average, negotiation text); `mortgage` "ההצעה שלכם מול בנק ישראל" (rate per track and term); `mexit` (exit fee by horizon); `mready` (documents) | They are separate; nothing reads the proposed basket, fees, guarantors, validity, insurance, appraisal or the final contract |

Placement: the main page owns "בדיקת משכנתא" (Search Console shows impressions for it; figures kept out of the public repo; keywords.md intent 6) and "השוואת משכנתאות".
Build it as a mode of the existing offers tool (chip "בדיקה לפני חתימה" in the switcher, next to "שלוש הצעות, טבלה אחת"), not a new URL.
/mortgage-calculator/mortgage-pre-approval/ owns "אישור עקרוני למשכנתא" (link to it for the explanation), /mortgage-advisor/ links
in with its existing title, /mortgage-home-insurance/ owns insurance (link), /mortgage-refinance/ owns refinance and the fee
deep dive (link).

## 2. What the user types (mapped to the uniform approval of directive 451, תוספת 6)

The official format (451, תוספת 6, read today) has a header, four baskets (סל אחיד 1, 2, 3 and סל מוצע) and "מידע נוסף". The tool
mirrors it so the user copies line by line. **No name and no ID number are asked** even though the approval prints them.

**Header (once per approval):** bank (list of the 9 mortgage banks + "אחר") · date of the approval (תאריך) · "האם נדרשים ערבים
להלוואה" (yes / no) · property: price, buyer type (דירה יחידה / חליפית / להשקעה / מחיר מופחת), new from a developer or second hand,
delivery date if new · "סך ההלוואה המבוקשת".

**Per basket, per track (the rows of תוספת 6, numbered as on the form):**
1. שם ההלוואה (track list: קבועה לא צמודה, קבועה צמודה, פריים, משתנה צמודה / לא צמודה with change frequency 1, 2, 2.5, 5 years, מט"ח, הלוואת זכאות)
2. סכום ההלוואה (₪)
3. תקופת ההלוואה (חודשים)
4. אופן התשלום (only in סל מוצע: שפיצר, קרן שווה, בלון, בוליט, גרייס חלקי / מלא and its months)
5. שיעור הריבית השנתית
6. בריבית משתנה: מנגנון קביעת הריבית (anchor + margin, change frequency)
7. הריבית הכוללת החזויה (כולל עמלות ותחזיות)
8. סכום ההחזר החודשי (לחודש ראשון עבור חודש תשלום מלא)
9. סכום ההחזר החודשי הגבוה ביותר הצפוי על פי התחזית (וחודש התשלום)
10. סך כל הסכום הצפוי החזוי שישולם עד לסוף תקופת ההלוואה
11. סכומי החיובים והעמלות, לרבות הוצאות לצד ג'
12. האם קיימת עמלת פירעון מוקדם בגין הפרשי ריבית (yes / no)
Plus the basket totals row ("סה"כ"). A quick mode asks only rows 7 to 11 per basket (what `moffers` asks today).

**מידע נוסף (451 s.4ג(ג)):** linkage rate, base and date · rate-change principles · the note that the anchor may change on the loan day ·
early repayment terms · the risks the bank requires insured · the appraisers list · the documents list.

**The user's own context (optional, kept in the page only):** net household income, existing loan payments, equity and its source,
years until a likely sale, upgrade or refinance, eligibility certificate (yes / no / not checked), quotes for life and structure
insurance (from life.cma.gov.il and dira.cma.gov.il).

**Mode 2, before the signing day:** the same fields from the final loan documents, diffed against the approval.

## 3. The checks (each prints the rule, its source and the user's number)

| # | Check | Rule | Source | Flag |
|---|---|---|---|---|
| 1 | Validity countdown | Terms held at least 24 days from the approval date, shown prominently; at least 12 days when no new lien is needed | 451 s.4ג(א)(4), (ז) | days left; red if expired, amber under 5 days |
| 2 | Completeness | Approval includes the tailored mix and the three uniform baskets (exempt: any-purpose under 10 years, housing loans without a lien under 10 years, government-agreement loans) | 451 s.4ג(א)(2)-(3), תוספת 5 | red if a basket is missing |
| 3 | Uniform basket form | Terms offered 10/15/20/25/30 years; Spitzer; basket 1 = 100% קל"צ; basket 2 = thirds קל"צ / פריים / משתנה צמודה כל 5 שנים על בסיס אג"ח ממשלתי; basket 3 = halves קל"צ / פריים | 451 s.4ג(ב)(2)-(3), תוספת 5 | amber if mix or term differs |
| 4 | Totals add up | Track amounts sum to the requested loan; loan + equity = price | arithmetic | red on mismatch |
| 5 | Financing share | LTV at most 75% (single), 70% (replacement), 50% (investment); reduced-price rules (value cap 2.1M, own money 100,000 or 60,000 ₪) | 329 (version 13), `boi-mortgage.json` rules | red above cap |
| 6 | Payment to income | First payment (and the highest expected) / disposable income: up to 40% ok, 40% to 50% passes with the capital note, above 50% fails; existing loans count | 329 s.5 and Annex A | red / amber |
| 7 | Variable share | Variable-rate part at most two thirds; at least one third fixed | 329 s.7 | red above 66.66% |
| 8 | Term | Every track at most 30 years | 329 s.8 | red above 30 |
| 9 | Price of this bank vs itself | Each basket's IRR against that bank's IRR in קו המשווה (2026-09: מזרחי-טפחות 5.16, לאומי 5.03, הפועלים 5.11, דיסקונט 4.95, הבינלאומי 4.75, מרכנתיל 5.23, ירושלים 6.96, ממוצע המערכת 5.09) | BoI קו המשווה (bank-reported, s.16יא חוק הבנקאות (שירות ללקוח)) | where the offer sits, never "good" or "bad" |
| 10 | Rate per track vs market | Each track's rate against the BoI average for the same track and term (term files) and the bank's own track average; prime as P plus or minus margin (system average 4.15 = P-0.60 in 2026-09) | BoI SDMX, mashfix/pribmash, קו המשווה | gap in shekels a month and over the loan |
| 11 | Across banks | Same basket, same amount and term, cheapest marked; different amounts scaled; different terms compared by IRR | 451 explanation sheet ("לשפר את יכולתכם לערוך השוואת עלויות") | gap in shekels |
| 12 | Recompute | Our engine recomputes rows 8 to 10 from rows 2, 3, 5, 6; a gap beyond a tolerance means a typing error or a cost inside the bank's figure. Banks use the 451 forecasts ("נגזרות ממחירי אגרות החוב הממשלתיות", "מתעדכנות אחת לשבועיים"); we use the BoI Research forecast, so show both and say which | 451 תוספת 6 explanation sheet | info |
| 13 | Highest payment and when | Row 9 and its month; payment-to-income at that month; plus our stress (+1% on variable, the 2022 replay) | 451 s.4ג(ב)(10); `mreplay` | amber if the peak breaks 50% |
| 14 | Fees and third-party costs | Row 11 per basket compared across banks; a reservation or option fee is not allowed | 451 s.8 ("דמי שריון", "תשלום בגין אופציה לקבלת הלוואה") | red if a reservation fee appears |
| 15 | File opening fee | Kol Zchut: up to 360 ₪ (no source cited there) | **unverified**; the bank's mortgage tariff (451 s.4(א)(4) points to it) | info |
| 16 | Early repayment cost | Row 12 per track; for fixed tracks the capitalisation fee by the Banking Order (20% off after 3 years, 30% after 5; operational fee up to 60 ₪; 0.1% without 10 to 45 days notice; CPI half-average rule on the 1st to 15th; none on prime / tracks changing at least yearly; none on a directed loan); cost at the user's horizon | צו הבנקאות ss.2-8, 10; `mexit` | amber when a large fixed share meets a short horizon |
| 17 | Balloon, bullet, grace | Any track not Spitzer or equal principal: show the lump sum and its month; grace: interest added (full) or paid (partial) | 451 definitions (7/23); CFPB labels balloon risky; ESIS interest-only notice | amber |
| 18 | Linkage exposure | CPI-linked share; balance and payment under the BoI inflation forecast (2.0% next 4 quarters, published 21.10.2026) | `boi-mortgage.json` forecast | info |
| 19 | Variable mechanism | Anchor, margin, change frequency; the rate shown is correct for the approval day and "העוגן (באחוזים) יכול להשתנות ביום מתן ההלוואה" | 451 s.4ג(ב)(5), (ג)(1) | info |
| 20 | Guarantors | "האם נדרשים ערבים להלוואה" = yes | 451 תוספת 6 header | amber, with questions |
| 21 | Insurance rights | The borrower may insure outside the bank's agency; the bank answers on a policy within 14 days; no life or property insurance may be required on loans or balances up to 30,000 ₪; property insurance not above the revalued unpaid balance (excluding land, plus up to 20%); a new flat from a developer is not insured before the contractual delivery date; annual statement | 451 s.11(א)-(ה) | info with links to life.cma.gov.il and dira.cma.gov.il |
| 22 | Full monthly cost | Payment + typed life and structure quotes + arnona and building committee (no official price table exists, fields stay empty) | `mquick` v5 | info |
| 23 | Appraisal | Charge is the lower of the actual cost or the bank tariff; a paying borrower gets a copy; another bank's appraisal may be reused within 90 days if the appraiser is on the list | 451 s.9(ג)-(ה) | info |
| 24 | Eligibility | If the household may be eligible: certificate valid one year from the request; apply before signing the purchase contract; the eligible loan carries no early repayment fee | gov.il mortgage_guide (25.09.2024); צו הבנקאות s.2 | amber "לא נבדק" |
| 25 | New flat timeline | Developer payment dates vs loan draws, grace until delivery, construction-index linkage | `mkeys`, Sale Law s.5ג | info |
| 26 | Mode 2 diff | Every field of the final documents against the approval; any change listed with "ask why" (amount higher, rate different, a new fee, a new insurance requirement, a track changed) | CFPB Closing Disclosure pattern; 451 s.4ג(ו) (late documents: the bank must say the hold period passed and give an updated approval) | red on any unexplained change |
| 27 | Payment instructions | Before any transfer to a seller or developer, confirm account details by phone with a number saved in advance; the eligible-loan money goes straight to the seller's account against a written confirmation | CFPB closing checklist (wire fraud); gov.il mortgage_guide | info |
| 28 | Credit report | One free BoI credit data report a year ("דוח ריכוז נתונים") before applying | Kol Zchut (updated 27.8.2025 per sub-agent) | info, **date unverified** |

Not claimed (no Israeli source found): a statutory reflection period before signing (the EU has 7 days; Israel's window is the
24-day hold), a tolerance rule for fee increases between approval and signing (US only), a minimum number of offers.

## 4. What it outputs

1. **Flags**, grouped red / amber / info, each one line: the user's number, the rule, the source with its date, and a link to the
   page that owns the topic.
2. **A written summary** in plain Hebrew, 5 to 8 sentences built only from typed numbers and dated official figures, for example:
   "בסל 2 ההחזר הגבוה הצפוי הוא X בחודש Y, שהם Z% מההכנסה הפנויה; הריבית הכוללת החזויה גבוהה ב-W מהממוצע של אותו בנק בקו
   המשווה (ספטמבר 2026); נשארו N ימים לתוקף האישור." Never a recommendation.
3. **Questions to ask the bank**, generated from the flags: "למה סכומי החיובים והעמלות בסל המוצע גבוהים ב-X מבנק ב'?", "מה
   מנגנון העוגן במסלול המשתנה ומתי נקודת השינוי הראשונה?", "האם אפשר לקבל את ביטוח החיים והמבנה מחברה אחרת, ומה הבנק צריך
   לאשר תוך 14 יום?", "האם נדרשים ערבים ולמה?", "האם אפשר להשתמש בשומה מבנק אחר (פחות מ-90 יום)?", "מה העמלה לפירעון מוקדם
   בשנה ה-N לפי המסלולים?".
4. **The negotiation text** (exists in `moffers`) extended with the fee and validity lines.
5. **Print or save as PDF, copy, WhatsApp share**; a case link in the URL hash only (as `mdecision`, `mexit` do). Nothing is sent to a
   server; no lead form; one plain link to /mortgage-advisor/.

## 5. Data it needs

| Data | Have it? | Where |
|---|---|---|
| BoI averages by track and term, by bank, IRR per bank | yes | `boi-mortgage.json` (by_bank, prepay, tracks), refresh monthly around the 20th |
| Uniform basket definitions, terms, Spitzer | yes | `boi-mortgage.json` baskets (source label cites 451 circular 2694; update to version 22, 7/23) |
| 329 limits | yes | `boi-mortgage.json` rules (versions 12 and 13 noted) |
| Banking Order fee formula | yes | `boi-mortgage.json` fees, prepay |
| BoI Research forecast | yes | forecast (21.10.2026) |
| The 451 forecasts banks must use (biweekly, from bond prices) | **no** | location on boi.org.il not found in this pass (unverified) |
| Mortgage tariffs (file opening fee) per bank | **no** | bank tariffs under כללי הבנקאות (שירות ללקוח)(עמלות), תשס"ח-2008; not read |
| Insurance prices | none official | only the CMA comparison calculators (inputs in inventory.json) |

## 6. Rules for the build

- Wording: "בדיקה", "השוואה", "מה לשאול", never "המלצה" or "כדאי לבחור"; whether a ranked check counts as regulated advice is
  **unverified** (world.md section 8).
- Privacy: no name, ID, phone or email fields; optional browser storage in try/catch; follow the lead-privacy memory if a lead
  path is ever added.
- Phone first: one basket per screen with a basket switcher; the quick mode (rows 7 to 11) first, full rows behind one tap.
- No long dashes in any string; Hebrew RTL; every number with its month.
