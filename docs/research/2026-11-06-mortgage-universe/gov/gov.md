# Mortgage universe: official state and Bank of Israel facts (research, 6.11.2026)

Research only. Nothing on the live site or in `plugins/` was changed. Files in this folder:

| File | What it is |
|---|---|
| `facts.json` | 100 facts, each with value, unit, effective date, source URL and title, retrieval time (UTC) and `verified` true/false |
| `hivun-rates.json` | The Bank of Israel average mortgage rates used for the early-repayment (capitalization) fee, full history, parsed from the official files, plus the Banking Order fee rules in a form a JavaScript tool can read |
| `banks.json` | Mortgage phone and site for 11 lenders, copied only from each bank's own page (page URL recorded) |
| `raw/` | Every downloaded source (PDF, xls, html, csv, json) and text extracts; `raw/banks/` holds the bank pages |

Evidence classes: **official file** = the PDF/xls/csv published by the body itself (Reshumot, BoI, Knesset); **consolidated law** = the text of
ספר החוקים הפתוח on Wikisource, which links each amendment to its Reshumot source (used where the Reshumot print was not opened);
**secondary** = news or search snippet, never counted as verified.

Access on 6.11.2026 (14:31 to 14:47 UTC): **gov.il pages are behind a Cloudflare challenge** (HTTP 403 to scripts and to WebFetch) and
**boi.org.il HTML pages are behind a Radware bot check**. Neither was bypassed. What did work: gov.il `BlobFolder` files, every
`boi.org.il/media/...` and `boi_files` file, the BoI SDMX API, Knesset OData and `fs.knesset.gov.il` PDFs, Reshumot PDFs on olaw.org.il,
Wikisource, and the banks' own sites (except Yahav's `/mortgage/` path and One Zero).

---

## 1. Mortgage registration at the Land Registry (טאבו) and the Registrar of Pledges

**2026 fees (official file: הודעת המקרקעין (אגרות), התשפ"ו-2026, קובץ התקנות 12193, 5.1.2026, עמ' 732; in force from 1.1.2026)**

| Action | 2026 fee |
|---|---|
| רישום משכנתה, משכנתה נוספת או הגדלת סכום ההלוואה | **188 ₪** |
| העברת משכנתה; העברת מקרקעין בכפוף למשכנתה; שינוי או תיקון בתנאי משכנתה (תיקון משכנתה) | **188 ₪** each |
| רישום פדיון (ביטול/מחיקת משכנתה) כשהכסף משולם ישירות לבעל המשכנתה | **פטור** |
| רישום פדיון כשהכסף מופקד בלשכה | 188 ₪ |
| הערת אזהרה, לכל רישום | **188 ₪** |
| מחיקת הערת אזהרה בבקשת הצדדים | 127 ₪ |
| נסח טאבו מאושר (דלפק) | **88 ₪** |
| נסח מאושר אלקטרוני חתום (מקוון) | **18 ₪** |
| נסח מרוכז לבית משותף | 154 ₪ |
| עיון, לכל נכס | 85 ₪ |
| מחיקת זכות שפקעה | 127 ₪ |
| רישום ירושה | 188 ₪ |

- The 2026 table has **no separate line** for "הערת אזהרה בגין התחייבות לרישום משכנתה": any warning note is item 13 (188 ₪). Charging that
  note at 188 ₪ is an inference from the table.
- Fees change every **1 January** by the CPI (November against November), rounded to a whole shekel (reg. 2(ב), 2(ב1)). The borrower
  (הממשכן) pays the mortgage registration fee (reg. 21). Exemptions: disabled, injured and bereaved families (reg. 12), olim under reg. 13; a fee
  deposited when a commitment to register a mortgage is made counts as paid (reg. 11א). (consolidated law)
- Reg. 2א gives 80% of the fee for warning-note actions filed online on the Justice Ministry site and no fee when a bank deletes an expired
  right online; it is a two-year temporary provision and **whether it is in force in 2026 is unverified**.

**Cancellation after payoff**
- Banking (Service to Customer) Law **s.9A**: after full payoff the bank cancels the liens and, for a mortgage or registered pledge, files the
  deletion notice **within 30 days** of payoff; **the bank pays** the deletion cost. One deadline for every banking corporation. The "60 days for
  a mortgage bank" claim was **not found** in the text. (consolidated law, amended 2026)
- Land Regulations 2011 **reg. 71(ב)(2)**: the registrar may cancel a mortgage at the request of the mortgagee bank alone. The gov.il service
  "בקשה לביטול רישום משכנתה בהתאם לסעיף 71ב(2)" refers to this regulation (the page itself was blocked).
- **Reg. 72**: when the lender refuses to accept payment, the borrower may deposit the debt with the registrar (with the deed, proof of the
  refusal and of the amount); the lender gets at least 15 days' notice, then the registrar can order the mortgage struck off.

**Second-degree mortgage**: a bank may not unreasonably refuse consent to a subordinate lien for another creditor; that creditor enforces only
with the first bank's consent, which may not be unreasonably withheld (Banking (Service to Customer) Law **s.7ח**). Registering an additional
mortgage costs 188 ₪. Equal-degree (pari passu) mortgages: no official text read.

**Registrar of Pledges (משכון, when the home is not registered)** (official file: הודעת המשכון (סדרי רישום ועיון), קובץ התקנות 12123,
14.12.2025, in force 1.1.2026): **45 ₪ a year** for up to 5 years at the counter, **38 ₪ a year** online, free from the 6th year; cancellation
free; changes and extensions 45 ₪ (38 ₪ online); search 38 ₪ (12 ₪ on the internet).

**Not read (gov.il blocked)**: the `mortgage_registration` service page (who files, "מקרקעין ברשת", documents, deposit boxes, reception days,
*8653), the `fees-2026` page, and the Israel Land Authority service "התחייבות לרישום משכנתא" (a search snippet says it is issued online in
the personal area "רמ"י שלי"; fee unknown). The housing-company (חברה משכנת) commitment process was not found.

## 2. Early repayment and the capitalization fee (עמלת היוון)

**The official rate series** (official files, downloaded into `raw/`):
- `https://www.boi.org.il/boi_files/Pikuah/mashfix.xls`: unindexed shekel loans (loans from 1.3.2013 by term bucket; a single series for
  loans made until 28.2.2013).
- `https://www.boi.org.il/boi_files/Pikuah/pribmash.xls`: CPI-linked loans (current buckets from 2011; an older bucket set back to 1996).
- Monthly. Last-Modified **18.10.2026**; latest row **in force from 19.10.2026**, data month **September 2026**. Byte-identical to the 5.11
  download. Rates are **effective annual** on a monthly-payment basis (the file carries an effective-to-nominal sheet).

| Unindexed (in force 19.10.2026) | avg | ≤1y | 1-5 | 5-10 | 10-15 | 15-20 | 20-25 | >25 |
|---|---|---|---|---|---|---|---|---|
| % effective | 4.5459 | 4.3505 | 4.5069 | 4.5927 | 4.6074 | 4.7390 | 4.7878 | 4.8886 |

| CPI-linked (in force 19.10.2026) | avg | ≤5y | 5-10 | 10-15 | 15-20 | 20-25 | >25 |
|---|---|---|---|---|---|---|---|
| % effective | 3.4910 | 3.5010 | 3.4871 | 3.2417 | 3.4552 | 3.3652 | 3.5272 |

`hivun-rates.json` holds all rows (163 unindexed, 53 pre-2013, 183 CPI-linked, 248 old-structure CPI rows), bucket limits in months, and the
lookup steps.

**The rules** (צו הבנקאות (פירעון מוקדם של הלוואה לדיור), התשס"ב-2002, amended 27.8.2014; consolidated law, matched with the BoI-hosted copy
`boi.org.il/media/qy5cow0l/116.pdf`):
- Operational fee **up to 60 ₪** (s.3(1)); the Supervisor may index it by notice (no update found).
- Notice under **10 days**: **0.1%** of the repaid amount; not on a same-bank refinance amount, not when the borrower died (s.3(2)). Notice
  no earlier than **45 days** ahead (s.10(ב)).
- Capitalization fee only if the average rate is below the loan's rate: s.3(3) = PV(A) minus PV; s.3(4) = PV(A) minus PV(C) using the average
  at origination; **the lower of the two** (s.3(5)). Second schedule gives the exact formula (in `hivun-rates.json`).
- **No capitalization fee** when the rate changes at unknown dates or at least yearly (prime, yearly variable), and only the operational fee
  on a rate-change day (s.4); **no fee at all on state eligibility loans** (s.2).
- Cuts: **20% after 3 years, 30% after 5** (complementary loans to eligibility: 10/20/30/40% after 1/2/3/4 years) (s.8).
- CPI-linked loan repaid on the 1st to 15th: repaid amount x half the average monthly CPI change of the last 12 indices (s.5).
- Partial prepayment: pro rata, or by the payments brought forward when the term is shortened (schedule part C).
- **Right to an estimate**: an explanation sheet with the fees and amounts as far as known in advance when asking to prepay, and an itemized
  statement **within 60 days** after (s.12).
- On enforcement of a single home: no prepayment fee unless the proceeds exceed **2.5 million ₪** (CPI-linked) or the full debt (Banking
  (Service to Customer) Law s.9A1).
- The BoI page `information/interestrates/` and "cir2103" could not be read (Radware). The formula above is from the Order itself.

## 3. Regulation and law in 2026

**(a) Relief for borrowers hurt by the rate rise**
- **Knesset private bill פ/6640/25** "הצעת חוק סיוע לנוטלי הלוואות לדיור עקב עליית הריבית (הוראת שעה), התשפ"ו-2026" (official PDF): laid
  for **preliminary debate on 23.3.2026**, first initiator MK Yosef Taieb with 22 others; status on 6.11.2026: still "הונחה על שולחן הכנסת
  לדיון מוקדם". It proposes a monthly grant of **75% of the rise** in the monthly payment against the March 2022 payment (CPI-adjusted), for
  single-home loans signed **up to 1.3.2022**, tapering to zero between the average home price and twice it, capped at the first grant, paid
  through the lender, **5 years**, extendable a year at a time.
- The government memorandum on tazkirim.gov.il was **not read** (JavaScript-only site). News reports (secondary): distributed about 13.1.2026,
  initiated by NEC chair Prof. Avi Simhon, about 2 bn ₪ a year.
- **BoI response, 13.11.2025** (official PDF): opposes subsidizing existing mortgages (burden not significantly up, low credit losses,
  discrimination, retroactive interference; reported cost 3 bn ₪ funded by a bank levy).

**(b) Bank of Israel housing-loan limits (Directive 329, version 13, circular 2852 of 30.6.2026; official PDFs)**
- PTI cap **50%** (s.5); above 40% a 100% risk weight (s.6).
- **From 1.10.2026** the monthly payment in the PTI includes **earlier loans secured by the same property**, at any bank or lender (Annex A
  1.1; circular 2840 of 8.2.2026, s.9, start moved from 1.7.2026 to 1.10.2026 by circular 2852). This is the official basis for the
  "October 2026" claim; precisely it covers loans on the same property, not every loan of the household. The December 2025 draft excluded
  loans already on the books before the start date.
- **Relative's income**: at most **half** of the disposable income of a first-degree relative who has no right in the property, is a
  guarantor, was checked and pays at least 20% (Annex A 1.3); a spouse living in the home counts in full. **Q&A 4.11 (11.3.2026, published
  10.5.2026)**: the half cap applies even when the relative signs as a borrower and pays everything. The "November 2026" date in Google's
  overview was **not found**.
- Variable share ≤ **66.66%**; from 1.10.2026 on total credit secured by the same property at the same bank (Q&A 5.1).
- LTV 75% / 70% / 50%; term 30 years; reduced-price homes valued at most 2.1 million ₪, own money at least 100,000 ₪ (60,000 ₪ with the
  grant); any-purpose loans up to 70% when the part above 50% is at most 200,000 ₪ (now permanent); until **31.12.2026** contractor-subsidized
  bullet/balloon loans at most **10%** of a bank's quarterly housing-loan executions (s.8א).

**(c) Mortgage advisors bill** "הצעת חוק הסדרת העיסוק בייעוץ משכנתאות, התשפ"ו-2026" (פ/5070/25; Knesset OData and the first-reading PDF):
passed the preliminary stage and went to the Economy Committee on **10.12.2025**; first-reading text published **8.6.2026** (הצעות חוק הכנסת
1196, p.244); status on 6.11.2026: **laid on the table for first reading** (last update 13.10.2026). It proposes a register at the Justice
Ministry with exams, advisors who are not employees of a financial body and are paid only by the client, start 3 months after publication,
and transition rules for those with 7 years (or 2 years under conditions) of practice.
Other bills: a reservist mortgage-freeze bill has been "in preparation for first reading" since 19.12.2024; a reservist deferral bill was stopped.

**(d) Eligibility loans (הלוואת זכאות)**: the Housing Loans Law **s.4**, as amended by the **2026 Economic Plan Law** (ספר החוקים 3510,
31.3.2026), now reads: CPI-linked interest at the **BoI-published average rate of banks on housing credit, minus 0.5%, but not above 3%** or
the lending bank's own rate, whichever is lower, by term, for holders of at least 599 points. Before 2026 the benchmark was "the average rate of
the mortgage banks". The **current published eligibility rate is unverified** (gov.il blocked); an illustration from pribmash minus 0.5 (capped
at 3) is in `facts.json` and must not be shown as official. The MoCH page "הפחתת הריבית על המשכנתאות" was not read. Hardship: a special
committee (Finance, Housing, the bank) decides within 60 days, appeal within 15 days, appeal decided within 30 (s.5א).

**(e) חוק ערבות למשכנתאות, תשי"ב-1952**: lets the Finance Minister guarantee, for the State, loans that finance home building, within a
total set by the Knesset Finance Committee.

## 4. Wartime relief and borrowers in arrears

- **"שאגת הארי"** (operation from 28.2.2026; BoI outline published **2.3.2026**; official presentation and clarification files):
  evacuated households whose home was damaged, or who were physically hurt: **mortgage deferral of 3 months, any amount, no interest or fees**
  (first home and upgraders); consumer loans up to 100,000 ₪ for 3 months; small businesses (turnover up to 25 million ₪) 2 months on up
  to 2 million ₪; reservist business owners: 2 months without overdraft interest up to 30,000 ₪. Window 16.3 to 16.4.2026, **extended on
  15.4.2026** to those hurt from 16.4.2026 with applications **until 15.5.2026**; at most 3 months in total for households. Deferred sums
  go to the end of the loan, are spread over the rest of the term, or become a 4-year interest-free loan starting after a year (bank's
  choice). Accrued interest is collected; CPI linkage on the deferred sum is at the bank's discretion. Borrowers in legal proceedings
  are excluded; those already in arrears get at most 180 days from the start of arrears.
- **"עם כלביא"** (operation from 13.6.2025; outline 17.6.2025): same household terms; window 1.7 to 31.7.2025.
- **"חרבות ברזל"**: BoI Temporary Directive 251 of 28.12.2023 is confirmed; the terms of the October 2023 outline were seen only in
  secondary sources (unverified).
- **Standing rights** (consolidated law): optional hardship deferral agreed in the loan (unemployment, illness over 3 months, birth):
  up to 3 months, once per 12 months, at most 3 times (Banking (Service to Customer) Law s.9ח1); after a borrower's death up to 12 months
  with no arrears interest (s.9ח2); **21 business days'** written notice before acceleration or legal action (s.5א1).
- **Execution Law**: no enforcement filing against an individual's home before **6 months** from the first missed payment; 20 days to ask
  to sell yourself (90-day stay); paying the arrears (or half with security) within 90 days of the receiver's appointment stops the process;
  immediate enforcement when arrears exceed 10% of the balance and in other listed cases (s.81ב1). Sale and eviction only with reasonable
  alternative housing; if waived in the deed, rent money for up to **18 months** (s.38).

## 5. Bank of Israel statistics

Nothing newer than the 5.11.2026 build (`plugins/.../boi-mortgage.json`, `2026-11-05-mortgage-world/data/data.md`): SDMX `BIR_MRTG_99`
still ends at **August 2026** (10,272 new loans, 10.90 bn ₪, PTI 29.23%) with only the **September volume** (8,668,214.64 thousand ₪, first
release); `BMB_99` ends at **August 2026** (673.3 bn ₪ in 1,156,467 loans, 0.61% 90+ days past due). The average-rate files are unchanged.
No new figure is added here.

## 6. Bank mortgage lines (from each bank's own site; details in `banks.json`)

| Bank | Mortgage line(s) | Page | Digital application |
|---|---|---|---|
| Leumi | *3200 / 076-8038181 (new); *6062 / 076-8038111 (existing) | mortgage.leumi.co.il contact-us | yes |
| Hapoalim | *2408 / 1-800-800-700 / 03-6532408 (new, refinance); *2401 / 03-6532401 (existing) | bankhapoalim.co.il/contact-us | yes |
| Mizrahi-Tefahot | *8860 ext. 4 (4-5 existing, 4-2 refinance, 4-3 arrears); WhatsApp 076-8818860 | mizrahi-tefahot.co.il/contact-us | yes |
| Discount | 03-9439008 / *2009 | mortgage.discountbank.co.il | yes |
| Mercantile | general *3477 only (mortgage line not found) | mercantile.co.il/private/contact-us | yes |
| FIBI | general *3009 only (mortgage insurance *5176) | fibi.co.il mortgages page | yes (digmo) |
| Otsar Ha-Hayal | general *3390 | bankotsar.co.il mortgages page | yes (digmo) |
| Massad | Massad call *2448 | bankmassad.co.il mortgages page | yes (digmo) |
| Jerusalem | *5727 / 076-8095111 (new); *5726 / 076-8095143 (existing) | bankjerusalem.co.il/mortgage | yes |
| Yahav | refers to Tefahot *8860 ext. 4 (general *2616) | bank-yahav.co.il/loans/mortgage-in-tefahot | via Tefahot |
| One Zero | blocked | | unknown |

---

## Everything unverified, and why

1. **gov.il service and fee pages** (mortgage registration process, "מקרקעין ברשת" filing, who files, documents, deposit boxes, reception
   days, *8653, online-versus-counter split, the fees-2026 page): Cloudflare challenge, not bypassed. The fee amounts themselves are verified
   from the Reshumot notice.
2. **Online fee discount (reg. 2א)**: text read, but whether the two-year temporary provision is in force in 2026 is unknown.
3. **Israel Land Authority and housing-company "התחייבות לרישום משכנתה"**: process seen only in a search snippet; fee not found.
4. **Equal-degree mortgage**: no official text read.
5. **"60 days for a mortgage bank" to deliver cancellation documents**: not in the Banking (Service to Customer) Law text read (30 days, all
   banks). Treat as unsupported.
6. **BoI page "ריביות ועמלת פירעון מוקדם" and "cir2103"**: Radware bot check; cir2103 not found by search. Whether the 60 ₪ operational fee
   was ever indexed: not found.
7. **The government memorandum on tazkirim.gov.il**: JavaScript-only site, not read; date, comment deadline and cost come from news only.
8. **"November 2026" start of the 50% relative-income rule**: the rule exists (Annex A 1.3, Q&A 4.11 of 11.3.2026); no November date found.
9. **Current eligibility-loan rate and the MoCH page "הפחתת הריבית על המשכנתאות"**: gov.il blocked; which BoI series the 2026 wording
   points to is not confirmed; the commencement date of the 2026 amendment was not checked.
10. **Swords of Iron outline terms (October 2023)** beyond Temporary Directive 251: secondary sources only.
11. **A refund of mortgage-advice costs for reservists**: no official source found.
12. **BoI directive on handling borrowers in arrears and any cap on arrears interest**: not found or not readable (boi.org.il HTML blocked).
13. **Mercantile mortgage-specific phone; One Zero**: Mercantile's number loads by JavaScript (only the general *3477 is shown); One Zero
    is behind Cloudflare. Bank Esh and non-bank lenders were not checked.
14. **Consolidated-law class**: s.9A, 9A1, 7ח, 5א1, 9ח1, 9ח2 of the Banking (Service to Customer) Law, the Execution Law, the Housing Loans
    Law, the land and pledge regulations' rules and the Banking Order were read in the Wikisource consolidated text (not the Nevo or
    Reshumot print). They are marked verified with that note; the Order's figures were also matched against the BoI-hosted copy.
