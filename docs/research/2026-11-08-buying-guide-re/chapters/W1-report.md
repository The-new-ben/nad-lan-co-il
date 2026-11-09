# W1 report: chapters c1 to c4 of /buying-apartment/ (HAD-686)

Writer W1, 9.11.2026. Files: `chapters/c1.html`, `c2.html`, `c3.html`, `c4.html`. Nothing else was edited, nothing committed.

## Words per chapter (Hebrew words; HTML comments excluded)

| Chapter | Type | All text | Without the `nlbg-src` source lines | Target |
|---|---|---:|---:|---:|
| c1 לפני שמחפשים | 4 `nlbg-add` blocks | 760 | 693 | 600 |
| c2 קודם המימון | 2 `nlbg-add` blocks | 1,264 | 1,153 | 700 |
| c3 בחירת עיר ושכונה | 3 `nlbg-add` blocks | 524 | 466 | 300 |
| c4 ביקור בדירה ובדיקה פיזית | full new section | 1,000 | 973 | 900 |
| **Total** | | **3,548** | **3,285** | 2,500 |

The total is about 30% over the target. I cut one full pass already (from 3,880 prose words). The rest is unit coverage: 19 economic units plus 22 physical units, the financing clusters 2a to 2d, the physical part of 1d, and two tables (forgotten costs, transaction cost worked example). If the integrator has to cut, the safest cuts are: the gift caution in c2 (about 45 words), the "who checks what" table at the end of c4 (it sums up the H3s above it), and the credit-report paragraph in c2.

## Placement (for the integrator)
- c1, c2, c3: every `nlbg-add` block starts with a `<!-- PLACE: ... -->` comment naming the live paragraph it follows. Block 1 of each file is the chapter head (kicker, `nlbg-ans` with its `nlbg-src`, `nlbg-who`, `nlbg-todo`). The last block of each file ends with `nlbg-back`.
- c4 is a full `<section id="nlbg-c4">`. It holds `<!-- LIVE: ... -->` markers for the two live parts it wraps: the visit-sheet paragraph with `<span id="visit">` and `<!-- TOOL bvisit -->`, and the three paragraphs of the live H2 "בדיקת מצב הדירה והבניין" (that H2 is dropped; its H3 on building deviations and the link row after it go to c7 / W2).
- Anchors used to other chapters: `#nlbg-c2`, `#nlbg-c4`, `#nlbg-c5`, `#nlbg-c7`, `#nlbg-c10`, `#nlbg-c14`, `#nlbg-c18`, plus the live anchors `#ladder` and `#before-sale`.
- Internal links (one per chapter, anchors from page-9-internal-links.txt): c1 none new (the live c1 sections already link the cost calculator and the tax calculator); c2 `/mortgage-calculator/mortgage-for-any-purpose/` "משכנתא לכל מטרה", `/real-estate-tax-advisor/` "יועץ מס מקרקעין"; c3 `/real-estate-broker/` "מתווך נדל״ן: מה בודקים"; c4 `/home-inspection/` "בדק בית", `/real-estate-appraiser/` "שמאי מקרקעין", `/pinkas-hakablanim/` "פנקס הקבלנים". If the live link row "בדק בית · היתר בנייה · טופס 4 · הנדסת בניין" stays in c4 instead of moving to c7, drop one of the two `/home-inspection/` links.
- H3 questions that W7 should not repeat in the FAQ: "מה קורה אם לא מקבלים משכנתא אחרי החתימה?" (FAQ candidate 48), "האם ניתן לקחת משכנתא עבור דירה שנייה?" (PAA, candidate 22), "מהי הדרך הטובה ביותר לבדוק דירה לפני קנייה?" (PAA, candidate 2), "איך מאתרים דירות למכירה?" (PAA, candidate 26), "איך בודקים את גודל הדירה?" (candidate 27), "האם יש אחריות על דירה יד שנייה?".
- No H2 or H3 starts with a protected head phrase (checked by script).

## Units covered

### amit-vered-map.md, "Checks part A", the physical flat, building, engineer and appraiser (22 PARTIAL/NO units in scope)
- Covered: #8, #9, #10, #19, #21 (c3 noise and neighbours); #13, #14, #15, #17 (without the 5 to 10% premium), #18, #20, #23, #24, #67, #69, #95, #97, #98, #100 (c4); #26 (without the ten-year number), #27 (c1).
- Partly: #96. The appraiser H3 in c4 says the appraiser checks how an unpermitted addition affects value. The legal consequences (extra arnona, levy, fines, demolition) belong to W2's c7, and I link there.
- Also touched: #81 (surveyor or engineer matches the flat to the plan, in c4), #89 (town plans on Mavat, in c3).

### amit-vered-map.md, "Checks part B (economic)" (19 PARTIAL/NO units, all covered)
- c1: #114 (margin as a fixed line, no percentage), #120, #122 (file opening, the bank's registry fees, verifying the POA; the pledge-registrar fee is left out), #124, #126, #128, #130 (replaced by a sourced worked example: 0.8% to 1.5% single home, 8.7% to 9.4% additional home, with no generic 15%).
- c2: #105, #111, #112, #132, #134, #135, #136, #138, #143 (written as a caution, no "20% more financing"), #145, #146, #147.
- Also touched in c2: #284 (insurance), #285 (bank appraiser), #298 and #299 (the clearing mechanism and the schedule rule, one sentence each, pointing to c14).

### amit-vered-map.md, the S1 frame: #1, #2, #3 (c1, "ממה מתחילים").

### other-competitors-map.md refs
- 1d physical / purpose / search: YLQ 2, YLF 2, YLF 3 (c1); GIN 9, NM 15, NM 16 (c3); PR 16 (c4). GOV 9 and YG 59 (Environment Ministry data) are only covered in practical terms (noise sources). The live c3 already links /environmental-hazards/. No official URL for the ministry's noise or antenna data is in the ledgers.
- 1c, the physical and appraisal parts only: PR 11 (no warranty from a private seller), PR 14 (contract tied to the bank's final approval), YLQ 25 (in part, through the area check).
- 2a: LZ 2 (a loan used as equity counts as a fixed expense under directive 329), LZ 5 and LZ 7 (our own worked numbers: what is repaid in 24 months, and the effect of the CBS 1.8% fall), YLP 22, NM 3 (in part: the official 50% cap instead of the one-third rule of thumb), NM 1. Not covered: LZ 3, LZ 4, LZ 6, LZ 8 to LZ 12 (opinions, unsourced figures, joining loans not confirmed).
- 2b: YG 36, YLP 31, KZM 5, KZM 18. Not covered: YLP 18 (green tracks, not confirmed), KZM 6 and KZM 7 (niche).
- 2c: YG 39, PR 36, MZ 14, plus MZ 16 (contents insurance) and MZ 11. MZ 10 is covered without the 0.25% / 360 ₪ figure.
- 2d: KZM 10, 14, 15, 16, 22, 24, 25, 26. KZM 13 (Ethiopian immigrants' grant) is left out: the fetch did not give me a clear page title for it.
- 12f: YLF 13 (buying on the free market ends "דירה בהנחה" eligibility; written from ledger row D18a).
- Seller's mortgage: YG 13, YG 14, PR 6. Insurance and appraisal: PR 30, PR 31, GIN 24. Inspection findings: PR 17, YLQ 19, YG 55, YG 57. Appraiser: YLP 40, YG 28. Brokers: ledger 10a to 10c.

## Facts used, with ledger ids
- Directive 329 v13 (law ledger 8a to 8e, decision 7): LTV 75 / 70 / 50; repayment up to 50%; 30 years; variable share up to 66.66%. I re-read the PDF myself, see below.
- Additional-home purchase tax 8% up to 6,055,070 ₪ for purchases up to 10.2.2027 (gov A1b, decision 2). The single-home tax of 1,752 ₪ on 2,028,800 ₪ is the live page's own sourced figure; 162,304 ₪ is 8% of the same price.
- Land Registry fees 2026: warning note 188, mortgage 188, sale registration 44, extract 18 ₪ (gov B7a, B7c, B7d, B7e, decision 9).
- ILA consent fees on a non-capitalised lease, and no ILA approval for a capitalised urban flat registered with a no-restriction note (gov C11a).
- "דירה בהנחה" eligibility is for people without a flat; upgraders only in follow-up lotteries (gov D18a).
- Tax Authority deals database: free, search by place or block and parcel and property type (gov B9).
- Mavat is the official plans site from 1.5.2022 (gov E19a).
- Defect periods: 4 years for piping, leaks and waterproofing; 5 years for cracks over 1.5 mm; 7 years for exterior cladding; 2 years for tiling and carpentry; 3 years of warranty after each (gov D16, law 3e).
- Broker law: written order and its details, three conditions, no legal tariff (law 10a, 10b, 10c).
- Agreed damages, s.15(a) Contracts (Remedies) Law (law 11).
- CBS dwelling price index down 1.8% year on year (law 20, decision 14).
- From the live page with its own source: national median 4-room price of 2,028,800 ₪ (Tax Authority deals, April to June 2026); BoI average mortgage rate of 4.62% (August 2026) and the 8,479 ₪ repayment; lawyer 0.5% to 1% plus VAT, appraiser 350 to 950 ₪, inspection 1,500 to 2,500 ₪ (Bizportal, 6.8.2026).
- My own arithmetic, labelled "חישוב להמחשה", on those inputs, using the live page's convention (effective annual rate, Spitzer, 25 years): +1 point gives 9,326 ₪ (+847); the two-thirds-variable mix gives about +565 ₪; after 24 months 203,499 ₪ has been paid, of which 68,729 ₪ is principal, leaving a balance of 1,452,871 ₪; 1.8% of the price is 36,518 ₪; the transaction-cost table totals.

## Facts I read myself (WebFetch, 9.11.2026; the machine clock shows the label "JST", and the times below are that clock)
1. **Directive 329, version 13 (30.6.2026)**, https://www.boi.org.il/media/ez4npagt/329.pdf, saved 03:46:08 and read through a local text extraction. Used:
   - LTV is measured on the value of the purchased property only (s.1).
   - The single or replacement home affidavit (s.3; not used in the text, left for W5).
   - Total LTV includes earlier loans on the same flat (s.4).
   - Reduced-price flats (s.4א): valuation and the 2.1M cap; own funds of 60,000 ₪ with a "מחיר למשתכן החדשה" grant or 100,000 ₪ otherwise. I wrote this, then cut it from c2 for length. It is free for W6 or the /dira-behanacha/ owner.
   - Above 40% the bank holds a 100% risk weight (s.6).
   - Bridge loans with an original term of up to 3 years are exempt from the repayment caps (s.11, 12.1).
   - Non-purchase loan up to 70% when the part above 50% is up to 200,000 ₪ (s.10א).
   - Annex A: disposable income, fixed expenses over 18 months, rent when the borrower will not live in the flat, half of a first-degree relative's income under four conditions, a co-living spouse's full income, the grace and bullet treatment.
2. **Sale (Apartments) Law, s.1 and s.4**, https://he.wikisource.org/wiki/חוק_המכר_(דירות), about 03:48. A "מוכר" is one who built, or bought in order to sell. "קונה משנה" is a defined term and the defect duties run to it. The inspection period starts when the flat is made available to the buyer (s.4(ג)).
3. **Kol Zchut "משכנתא"** (updated 7.1.2026), https://www.kolzchut.org.il/he/משכנתא, about 03:50: the list of state aid tracks and the three mortgage-fee exemptions (titles only, no amounts).
4. **Kol Zchut "ביטוח משכנתא"** (updated 7.7.2026), https://www.kolzchut.org.il/he/ביטוח_משכנתא, about 03:51: free choice of insurer, switching without a fee, the bank's 14-day answer; it cites BoI housing-loan procedures ss.11 and 11א.
5. **Kol Zchut credit data page** (updated 27.8.2025), https://www.kolzchut.org.il/he/קבלת_מידע_על_נתוני_אשראי_ודירוג_האשראי_האישי, about 03:52: one free report a year from the BoI credit data system, national digital ID or *6194; lenders may use the rating with consent.
6. **Kol Zchut early repayment fees** (updated 2.3.2025), https://www.kolzchut.org.il/he/עמלות_פירעון_מוקדם_למשכנתא, about 03:53: the discounting fee follows the gap to the BoI average rate; 10 to 45 days' written notice avoids the no-notice fee.
7. Tried and failed: https://www.kolzchut.org.il/he/אישור_עקרוני_למשכנתא returned 404 (about 03:49).

## Missing facts (written as ideas without numbers, or left out)
- A safety-margin percentage (their 5%, another competitor's 25%): no official source.
- A total ancillary cost ratio (their 15%): replaced by the sourced worked example.
- Surveyor fee, mortgage file-opening fee (a competitor's 0.25% up to 360 ₪), notary or lawyer fee for verifying the bank POA, utility connection costs, ILA consent-fee amounts, pledge-registrar fee (gov E20 not confirmed).
- How long an in-principle approval stays valid, and whether the rate is locked (Kol Zchut page 404; directive 451 not read).
- The bank's document list with counts (3 payslips, 3 months of statements): competitors only.
- Bank fees when a deal is cancelled after a file is opened: competitors only; written as a question to ask.
- Green mortgage tracks, and interest-free joining loans from banks: not confirmed; left out.
- Whether a bank computes LTV on the lower of price and appraisal: directive 329 says only "the value of the purchased property" (its definition refers to reporting directive 876, not read). The appraisal-gap text says "can shrink", not a rule.
- Premium for a reputed builder (5 to 10%), the ten-year planning horizon, the one-third rule of thumb: opinions; left out as numbers.
- An Environment Ministry URL for noise or antenna data: the gov.il buyer guide links to a noise page (gov D13), but the URL is not in the ledger.
- Ethiopian immigrants' purchase grant, and amounts for every aid track: not confirmed in this pass.

## Chosen to leave out, and why
- Purchase-tax reliefs for disability groups and bereaved families (AV #161, #163): these are tax units (part C) for W3's c8, not part B.
- Repayment difficulty, the six-month extension and the exceptions committee (cluster 2e): after the purchase; no internal page to link; no ledger source.
- Mortgage execution after signing: the borrower papers, affidavit, notary POA, bank warning note and deeds (AV #281 to #297, #328 to #332). These are W5's c14. c2 points to `#nlbg-c14` and covers only what is decided before signing.
- The joint-house file, the plan and the building file (AV #54 to #65, #70 to #93): W2's c5 and c7. c4 points there and covers only what can be seen on site.
- Copyright: I did not open the competitors' raw JSON. All wording is my own, and the fragments were written from the paraphrased unit maps and the ledgers only.

## Self-check (script, 9.11.2026)
- Python html.parser with a tag-balance stack: no mismatched or unclosed tags in any of the four files.
- Long dashes U+2013 and U+2014: 0. Forbidden words (אטלס, Atlas, פראייר, דוגמה): 0. No paragraph opens with "קניית דירה".
- Every `<td>` has `data-l` (c1: 54, c4: 24).
- Every number in the text has a `nlbg-src` line or a `nlbg-note--fig` after it, or is labelled as our own calculation.
- Each `nlbg-ans` is 29 to 32 words.
