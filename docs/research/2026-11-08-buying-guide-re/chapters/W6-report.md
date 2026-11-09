# W6 report: chapter c17 (buying from a developer), HAD-686

Date: 9.11.2026, Israel time. File written: `chapters/c17.html` (one `<section id="nlbg-c17">`). Nothing else edited, nothing committed.

## Words

| Part | Hebrew words |
|---|---:|
| Head (kicker, H2, answer, who, to-do box, intro paragraph, overview table) | 334 |
| מה לבדוק לפני קניית דירה מקבלן? | 273 |
| האם טופס הזמנה מקבלן מחייב? | 141 |
| מה כולל חוזה רכישת דירה מקבלן? | 190 |
| מה זה מפרט, ומה זו גרמושקה? | 180 |
| איזו ערבות מקבלים לפי חוק המכר? | 354 |
| איך עובד פנקס השוברים? | 173 |
| מה מביאים ליום החתימה אצל הקבלן? | 92 |
| כמה מוסיפה ההצמדה למדד תשומות הבנייה? | 215 |
| כמה עולה עורך הדין של הקבלן, ואילו הוצאות עוד מגיעות? | 202 |
| שינויי דיירים: עד מתי אפשר ובכמה? | 150 |
| מה מגיע על איחור במסירת דירה מקבלן? | 207 |
| מה ההבדל בין טופס 4 לתעודת גמר? | 97 |
| מה נכנס בגמר החשבון מול הקבלן? | 85 |
| מה בודקים ביום המסירה, ומה זה פרוטוקול מסירה? | 210 |
| כמה זמן הקבלן אחראי לליקויים? | 161 |
| מתי הקבלן חייב לרשום את הדירה על שמכם בטאבו? | 167 |
| אפשר למכור דירה מקבלן לפני המסירה? | 146 |
| מה המשכנתא מממנת בדירה מקבלן, ומה לא? | 196 |
| **Total body (source lines excluded)** | **3,573** |
| Total including the `nlbg-src` lines | 3,809 |

This is about 37% over the 2,600 target. A first draft ran to 4,600 words; I cut it down while keeping the units. If the integrator must cut further, these go first with the least loss: the signing-day H3 (92 words, which c12 may already cover), then the overview table (about 120 words).

## Structure and placement notes for the integrator

- H2: `רכישת דירה מקבלן: מבדיקת היזם ועד הרישום בטאבו`. "רכישת דירה מקבלן" is search 17 in serp-family-top5. The H2 avoids the protected heads and does not open with "קניית דירה".
- H3s are real search phrasings or questions. "מה לבדוק לפני קניית דירה מקבלן" is an exact related search. Others follow the related searches and people-also-ask ("קניית דירה מקבלן תשלומים", "שכר טרחת עורך דין קבלן", "הוצאות בקניית דירה מקבלן", "מתכוונים למכור דירה מקבלן לפני המסירה", "פיצוי על איחור במסירה").
- The existing live section stays inside this chapter, marked by an HTML comment after the intro paragraph: the H2 "יד שנייה, מקבלן או להשקעה: מה בודקים בכל סוג", its table and paragraph, its H3 "קניית דירה מקבלן: ערבות, מדד ולוח תשלומים", and its nlbp-go links row. Nothing in c17 repeats the facts in that section: vouchers to the project account, half-linkage, the 3.6% index change, 10/90 and 20/80, and the 5,915 ₪ / 0.5% cap. The lawyer-fee H3 adds only what is new: the price ceiling, what the cap covers, direct payment with an invoice, and the extra charges.
- Child-page links, once each: `/real-estate-lawyer/sale-of-apartments-law/` (חוק המכר, as the brief asked), `/projects/` (anchor "לכל 976 הפרויקטים בקטלוג", as the brief asked), `/pinkas-hakablanim/` (פנקס הקבלנים), `/real-estate-lawyer/form-4-occupancy-permit/` (טופס 4), `/home-inspection/` (בדק בית, body text only), `/real-estate-tax-advisor/capital-gains-tax-guide/` (מס שבח). All anchors are taken from page-9-internal-links.txt.
- One overlap to know about: the wrapped section's nlbp-go row already links `/real-estate-lawyer/sale-of-apartments-law/`. Once assembled, that URL appears twice in chapter 17. I kept it because the brief asked for it. I removed my link to `/new-projects/contractor-delay-compensation/` because that row already carries it.
- In-guide anchors: #nlbg-c8 (taxes, twice), #nlbg-c10, #nlbg-c12, #nlbg-c15, #nlbg-c16, #nlbg-map.
- No tool is assigned to c17, so there is no TOOL comment.

## Units covered (other-competitors-gaps, cluster "קנייה מקבלן", 11a to 11h: 154 units)

Full = the fact is on the page. Partial = the core is there, but a detail is left out because it is not confirmed.

| Cluster | Units | Full | Partial | Not | Notes |
|---|---:|---:|---:|---:|---|
| 11a preparation, developer check | 16 | 14 | 2 | 0 | Full: ELK 1, 3, 5, 6, 8, 9, 12, 14, 15; YLD 3, 5, 6; GOV 8; MAD 3. Partial: ELK 18 (warning note as security is covered; the Supervisor's warning about urban renewal is not confirmed), YLP 30 (stated as the 2026 change on who may issue a guarantee). |
| 11b request form, contract, changes annex | 28 | 27 | 0 | 1 | Full: ELK 25 to 30, 113, 114, 116 to 125, 158, 159; YLD 2, 8; AVD 1 to 5. Not: ELK 160 (a law firm's case story; no invented anecdotes). |
| 11c payment schedule, index, advance payments | 16 | 13 | 2 | 1 | Full: ELK 21, 23, 31, 33, 36 to 40, 42 to 45. Partial: ELK 34, 35 (the rule "last index published before the linkage date", s.5ג(ד), is stated; the CBS publication day is not confirmed). Not: ELK 32 (history of dollar linkage, unconfirmed). |
| 11d spec, plans (garmushka), power of attorney | 15 | 12 | 2 | 1 | Full: ELK 47 to 57; YLD 4. Partial: ELK 59, 60 (notarial power of attorney costs money; its fee and scope are not stated). Not: ELK 61 (refund rule in discount-price projects, unconfirmed). |
| 11e Sale Law securities | 14 | 12 | 2 | 0 | Full: ELK 62 to 65, 67, 69, 70; YLQ 21 to 23; YLF 11; GOV 4. Partial: ELK 66 (the VAT fund is stated from s.3ג2; amendment numbers and history are not), ELK 68 (reason given: money comes back; the bank's staged escort is not described). |
| 11f costs: developer's lawyer, registration, meters, management, lift, parking | 9 | 8 | 1 | 0 | Partial: ELK 74 (the Supervisor's decision of 2.12.2019 is not cited, being unconfirmed; written as practice with a request for a cap). |
| 11g delay, force majeure, tenant changes, deviations | 23 | 21 | 2 | 0 | Partial: ELK 161, 162 (sent to the lawyer against the spec; legal tolerance of execution deviations is not stated). The Shams ruling (ELK 91) is not cited; the form contents are given as practice. |
| 11h after signing, final settlement, Form 4, protocol, defects | 33 | 32 | 1 | 0 | Partial: ELK 147 (the online bank check tool is not confirmed; written as "verify with the lending bank", from D14b). |
| **Total 11a to 11h** | **154** | **139** | **12** | **3** | 151 of 154 touched |

Also covered from neighbouring clusters, because the brief puts them in c17:
- 10a (registration duties, s.6B, resale): 15 of 16 full (ELK 104, 107 to 112, 183 to 190). Not: ELK 105 (double sales).
- 7a (signing day with a developer): 14 full (ELK 129 to 132, 135 to 144), 2 partial (133, 134), 3 left to c12 (ELK 126 to 128).
- 8a: ELK 149 and 156 (equity first, the bank pays through vouchers). ELK 152, 154, 155 are left to c14.
- Amit Vered map: #17 (research the builder), #193 and #195 (payment schedule as protection), #91 (Form 4), partly #359 (registration time). ELK 193 to 195 (future sale and the single-home exemption) are covered too.

## Facts used, with ledger ids

- sources-ledger-gov: D17a (contractor register, statuses, QR), D17b (refusers list, criteria, 17 entries, live address), D13 (buyer guide, checklist, Russian version), B10 (registration status lookup), E19a (mavat), A5a (tax clearances needed for registration), D14a, D14b, D14c (stage percentages 31/25/5/6/10/13/5/5), D14e, D15a, D15b, D16 (defect periods), A6 (single-home exemption, 18 months since it became a dwelling), A2a (declaration in 30 days), A2c (payment deferral).
- sources-ledger-law: 1a, 1b, 3a, 3b, 3c, 3d (older rule mentioned, not detailed), 3e, 3f (20 years), 3g, 3h, 4a, 4b (14 business days), 4c (through decision 6), 8a, 8b, 14b (cap applies up to 4,642,750 ₪).
- LEDGER-DECISIONS: 4 (delay compensation), 5 (linkage), 6 ("since 2026 more licensed bodies", no date), 7 (mortgage limits), 11 (developer lawyer cap), 13 (live refusers list), 16 (project account: only "the voucher goes to the supervised project account").
- From the live page's own sourced rows: the construction input index rose 3.6%, September 2025 to September 2026 (CBS). It is used only as the assumption in the worked example, which is labelled "חישוב להמחשה".

## Facts I fetched myself (official texts, read-only)

All are Israel time on 9.11.2026. The Git Bash clock printed "JST", but PowerShell shows Israel Standard Time with the same digits.

| Time | URL | What was used |
|---|---|---|
| ~03:41 to 03:42:40 | https://he.wikisource.org/wiki/חוק_המכר_(דירות) (rendered page, then raw wikitext) | s.2 (spec and maintenance instructions attached and signed; any change needs both signatures); s.3(א),(א1),(ג),(ה)-(ז) (spec form set by order; priced items; deadline for tenant changes not before 6 months after the foundations stage; credit and charge at the listed price; updated spec); s.4(א),(ג) (defect and warranty periods start at handover; 3-year warranty; 20 years for fundamental defects); s.4ב (chance to repair; repeat within 2 years or urgent repair not done lets the buyer repair at the seller's cost); s.5 (no spec means a high-quality presumption, with the burden on the seller); s.5א (text confirms 3a to 3c); s.5ב(ב) (late-payment interest only after 7 days); s.5ג(ג),(ד) (no linkage after the contractual date except 5א(ג) delays; last index published before the linkage date); s.6 (bylaw changes to common property and expense shares must be disclosed, otherwise the standard bylaw applies); s.6א (management company identity and terms in the contract; a limiting clause lasts at most 3 years unless extended by the owners); s.6ב (registration timetable and the force-majeure exclusion); s.6ג(א),(ג) (what the cap covers; paid directly to the lawyer against a tax invoice); s.7א(א),(ב) (no contracting out against the buyer; a waiver as a condition for handover, repairs or a sub-buyer transfer is void, contracts from 7.7.2022) |
| 03:43:17 | https://he.wikisource.org/wiki/חוק_התכנון_והבניה (raw) | s.157א(ב),(ה1) (local committee chair and engineer approve the utilities connection; electricity for building works is allowed with a permit; approval when built per the permit and fit for use); s.158מז (definition of a completion certificate) |
| 03:43:41 | https://he.wikisource.org/wiki/חוק_המכר_(דירות)_(הבטחת_השקעות_של_רוכשי_דירות) (raw) | s.1 ("seller" includes one who bought from the builder to resell); s.2(1)-(5) (the five securities, the VAT exclusion, the events); s.2א (swapping the security after completion and possession, unless the contract forbids it); s.2א1(ב) (written notice when there is no financial escort); s.2ג (release letter: seller asks within 30 days of the first voucher payment, issuer answers within 30 days); s.3 (stage limits unless guaranteed); s.3א (costs on the seller); s.3א1 (linkage of the secured sum); s.3ב(ג)-(ה) (vouchers only; irrevocable instruction; 14 business days); s.3ג (the mortgage lender pays only after verifying the security); s.3ג2 (Finance Ministry fund returns the VAT component); s.3ד, 3ה (the Supervisor's register and handling of public complaints) |
| 03:45:13 | https://he.wikisource.org/wiki/צו_מכר_דירות_(טופס_של_מפרט) (raw) | items 1 to 6 (identifiers: block and parcel or plan and plot, flat and floor, landowner, ownership or lease; area by the outer faces of external walls, centre of a shared wall; attached areas with marked parking and storage plans); item 10.1 (plans: flat at 1:50 or larger with room sizes, floor at 1:100 with common property, entrance and basement, roof, plot) |
| ~03:46 | https://he.wikisource.org/wiki/חוק_המקרקעין (raw) | s.57, s.58 (expense share by floor-area ratio unless the bylaw says otherwise) |
| ~03:43 | https://www.kolzchut.org.il/he/טופס_4 and .../תעודת_גמר | both returned HTTP 404; nothing used |

## Missing facts (left out, or written without the number)

- The CBS publication day of the construction input index (competitors say the 15th): not confirmed. Written as "the last index published before the payment".
- Linkage history (dollar), amendment numbers and years of the Safeguard Law, and the background collapse: not confirmed.
- The Supervisor's decision of 2.12.2019 on charging for registration drawings and fees, and typical sums (per room): not confirmed. Written as practice: ask for a cap in shekels and a date.
- The notarial power-of-attorney fee and what it allows beyond an ordinary power; the refund rule in discount-price projects: not confirmed.
- An online tool at each bank to check that a project account is active: not confirmed (decision 16). Written as "verify with the lending bank".
- That the Supervisor discourages a warning note as the sole security in urban renewal: not confirmed.
- Whether a contractor's licence must be "of the current year": not confirmed. The register status check is stated instead.
- Typical numbers: tenant-change discount (about 10%), the size of the final payment (about 10%), the minimum for advance payments (75,000 ₪), the approval-fee case (10,000 ₪ plus VAT). None confirmed; written without numbers or left out.
- The Shams ruling (tenant-change form contents): not verified; no ruling cited.
- "Form 5" as a name, and whether occupancy needs the completion certificate: not confirmed (kolzchut pages 404). Only the law's definitions are used.
- Legal tolerance of area deviations (execution deviation): not confirmed; sent to the lawyer.
- The advance on the seller's capital-gains tax in a developer deal (decision 1: after 80%): deliberately not stated in c17. Ledger A3 also lists an exception for a contractor bound under the Sale Law. Left to c8, where W3 handles the advance.
- The ministry hotline 1299 (GOV 12): not confirmed.

## Self-check (run 9.11.2026)

- Long dashes (U+2013, U+2014): 0. Minus sign (U+2212): 0.
- Forbidden words: אטלס / Atlas 0; דוגמה / דוגמא 0 (worked figures are labelled "חישוב להמחשה"); פראייר 0; no talk about the site's own tools; no superlatives about ourselves.
- No H2 or H3 starts with a protected head, and no paragraph, list item or heading opens with "קניית דירה".
- 63 `<td>` cells, all with `data-l`. No inline styles, no scripts.
- python html.parser: no unclosed tags, no mismatches.
- 6-word overlap against all competitor JSON blocks in `_private-research/2026-11-08-buying-guide-re/html`: 0 hits, after two rewordings. One was an order title in a source line; the other was "על חוק המכר במשרד הבינוי והשיכון".
- Every official number has a `nlbg-src` line or a `nlbg-note--fig` after it, dated 9.11.2026. The 3.6% figure is from the live page's CBS row and appears only in the example.
