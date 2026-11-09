# W7 report: chapter 18, FAQ additions, glossary (page 9 /buying-apartment/, HAD-686)

Written 9.11.2026, 03:40 to 04:10 Israel time. Files: `chapters/c18.html`, `chapters/faq-add.html`, `chapters/glossary.html`, this report. Nothing else was edited, nothing committed.

## Words (Hebrew words)

| Part | Words (with source lines) | Without source lines | Target |
|---|---:|---:|---:|
| c18 מקרים מיוחדים | 1,635 | 1,579 | 1,300 |
| FAQ additions (20 questions) | 1,295 | 1,295 | 1,400 |
| Glossary (69 terms) | 1,608 | 1,608 | 1,500 |
| Total | 4,538 | 4,482 | about 4,200 |

c18 is about 25% over target because of the summary table (about 150 words) and the two cases the brief asked for that had no ledger row (Amidar, common-law couples) and needed a fetched source. If the integrator must cut, the safest cut is the closing paragraph before the "מהשטח" note (it only points to c6 and c7).

## What changed because the other writers' fragments landed first

When I started, only c8, c10 to c13 and c17 were on disk; by the end all of c1 to c17 were there. I checked every H3 against them and changed my parts so nothing is said twice:

- **c18:** W2's c6 already has full H3s on the tenant (same ledger row 18a, nearly the same wording), the company seller (A3, Companies Registrar) and the seller's power of attorney (signed abroad). I removed my three H3s on these and kept one table row and one closing line that point to `#nlbg-c6`. The seller abroad keeps only what c6 lacks (no money before the check, the advance still applies); the foreign-resident buyer part stays. The Amidar H3 points to c5 for which rights confirmation to order instead of restating C12. The heirs H3 stays, because c6 ends its short heirs paragraph with "הפירוט במקרים המיוחדים (שלב 18)".
- **FAQ:** dropped nine planned questions that are now chapter H3s: mortgage on a second flat and a mortgage refused after signing (c2), finding flats (c3), flat size (c4), ordering an extract and search by address (c5), seller is the owner (c6), memorandum binding (c9), lawyer fee and contract contents (c10), signing to keys time (c14), guarantees, handover protocol and developer registration (c17), value by address (c3). Replaced them with candidates no chapter answers (new flats up to 1.2M, periphery, receiver cases and discount, inheritance tax, purchase group).

## c18 structure

Kicker "שלב 18 מתוך 18 · מסלולים נוספים". H2: מקרים מיוחדים בקניית דירה: ירושה, כונס, פירוק שיתוף, פינוי בינוי ועוד. Head: `nlbg-ans`, `nlbg-who`, `nlbg-todo` (5 steps), intro, a 9-row table (case, what is different, what to ask to see). H3s, each with an id for deep links:

| id | H3 |
|---|---|
| nlbg-c18-heirs | דירה בירושה: מה בודקים כשהמוכרים הם היורשים? |
| nlbg-c18-kones | רכישת דירה מכונס נכסים: מה משתנה בסדר השלבים? (fig note: 15 days, 10%, 7 days) |
| nlbg-c18-partition | דירה בפירוק שיתוף: ממי קונים ומה בודקים? |
| nlbg-c18-renewal | בניין שחתם על תמ״א 38 או על פינוי בינוי: מה בודקים? ("עצרו" note) |
| nlbg-c18-amidar | רכישת דירת עמידר: אפשר לקנות דירה בדיור הציבורי? |
| nlbg-c18-abroad | רכישת דירה מתושב חוץ, או כתושבי חוץ: מה משתנה? (fig note: 8% / 10%) |
| nlbg-c18-partners | קונים עם שותפים או עם ההורים: מה שונה בעסקה עצמה? |
| nlbg-c18-cohab | ידועים בציבור קונים דירה: מה מסדירים מראש? |

Then a closing line (tenant and company seller: c6; building deviations: c7, not repeated), a "מהשטח" note, and the back link. No tool belongs to this chapter.

**Anchors the integrator must add to the live FAQ H3s** (c18 and the FAQ link to them by heading; the live H3s have no id):
- `id="faq-kones"` on "קניית דירה מכונס נכסים: על מה שמים לב?"
- `id="faq-partners"` on "קניית דירה עם שותפים או על שם הילד: מה צריך לדעת?"
- `id="faq-parents"` on "ההורים עוזרים: מתנה או הלוואה, ומה עם האחים?"
- `id="faq-wedding"` on "קונים לפני החתונה: על שם מי רושמים?"

Internal links in c18 (once each): /urban-renewal/check/ (בדיקת התחדשות עירונית), /purchase-tax-calculator/ (מחשבון מס רכישה). External: official sources only, plus mavat.iplan.gov.il (מידע תכנוני).

## FAQ additions (20)

Each answer is 43 to 70 words, direct answer first, inline source in brackets in the live FAQ's style. Candidate numbers refer to the "FAQ candidates" table in `other-competitors-gaps.md`.

| # | Question | Candidate |
|---|---|---|
| 1 | מהם השלבים בתהליך קניית דירה? | 10 (PAA) |
| 2 | דירה יד שנייה: מה בודקים לפני שקונים? | 2 (PAA "הדרך הטובה ביותר" is c4's H3; developer half is c17) |
| 3 | הערת אזהרה או רישום בעלות בטאבו: מה ההבדל? | 39 |
| 4 | האם אישור העירייה לטאבו אומר שאין חריגות בנייה? | 24 |
| 5 | קונים דירה ראשונה בגיל צעיר: מה עושים קודם? | 13, 42 |
| 6 | כדאי לקנות דירה בבניין שעומד לעבור פינוי בינוי או חיזוק בתמ״א 38? | 14 |
| 7 | האם אפשר לקנות דירת עמידר? | 4 |
| 8 | ידועים בציבור שקונים דירה: מה צריך לדעת? | 7 |
| 9 | מה משלם תושב חוץ שקונה דירה בישראל? | 9 (buyer side only) |
| 10 | מה זה דירה על הנייר, ומה הסיכון? | 16 |
| 11 | מבצע 20/80 מקבלן: על מה מסתכלים? | 18 |
| 12 | איפה אפשר למצוא דירות חדשות עד 1.2 מיליון שקל? | 26 (PAA) |
| 13 | האם כדאי לקנות דירה בפריפריה? | 35 |
| 14 | באילו מקרים דירה נמכרת דרך כונס נכסים, והאם היא זולה יותר? | 3 (the "which cases / discount" half; the live FAQ keeps "what to watch") |
| 15 | יש מס ירושה על דירה שהתקבלה בירושה? | 21 |
| 16 | קבוצת רכישה: האם זה כדאי? | 33 |
| 17 | לשכור או לקנות דירה: איך מחליטים? | 23 |
| 18 | האם רווקים יכולים לקבל משכנתא, ובאילו תנאים? | 41 |
| 19 | האם כדאי לקנות דירה להשקעה? | 1 (short, links /investment/, does not target it) |
| 20 | כדאי לקנות דירה בחו״ל? | 36 (short, links /investment/) |

The /investment/ anchor is "השקעות נדל״ן", the anchor used for that URL elsewhere on the site (found in `docs/qa/had-575/page-backup/page-4489-20261021-224330.html`); page 9 itself has no link to /investment/ today.

Candidates answered elsewhere on the page and therefore not added: 5, 6 (c10), 11 (c5), 12 (c16, c17), 15 (c3), 17, 19, 20, 30, 31, 32, 40, 44, 45, 46, 47 (c17), 22, 48 (c2), 27 (c4, c5), 28 (c14), 29 (c9), 34 (c8, live FAQ), 37 (c4 and the visit sheet), 38 (c6), 43 (c10, c13), 49 (c5), 25 and 8 (c1, c8; owned by /dira-behanacha/), 50 (intent unclear).

## Glossary (69 terms)

`<dl class="nlbg-gloss" id="nlbg-gloss">`, sorted alphabetically, each `<dd>` ending with a link to its chapter (`#nlbg-c1` to `#nlbg-c18`). All 60 terms of the brief's list are in (גב אל גב as "עסקת גב אל גב", מקדמה as "מקדמה על חשבון מס שבח", שובר תשלום with פנקס שוברים), plus 9 more: גוש חלקה ותת חלקה, נכס מהוון, דמי הסכמה, גרמושקה, פרצלציה, מסירת חזקה, הצמדה למדד (separate from the attachment sense of הצמדה), טופס בקשת רכישה, גמר חשבון. The last two and גרמושקה also define FAQ candidates 32, 45 and 46. The glossary deliberately has no figures: every number lives in its chapter with its source line.

## Units covered

- **other-competitors-map:** PR 43 (inherited flat: orders), PR 44 (receiver terms, firm dates), PR 45 (dissolution: other parties, parallel proceedings), PR 46 (urban renewal: progress, agreements, interim use); KON 1, 2, 3, 5, 6 (deposit as the official 10%), 7 (approval), 10 (two FAQ questions: which cases, discount); NM 11, 17, 22 and YLP 28 (urban renewal: agreement, securities, value); NM 18, 19 (purchase group, as a risk checklist without the 15% to 20% figure); NM 14 and PR 2 (abroad and investment, link only); YLF 13 not covered (see below); KZG 1 to 12 not used, see "left out".
- **amit-vered-map:** 36 (acquisition by inheritance), 42 (partner claim, buyer side; seller side is c6), 234 (probate order as an annex, via the heirs H3). Units 44 to 48, 338, 339 (tenants) and 50 (fraud) are W2's c6.
- **FAQ candidates:** see the table above (20 candidates answered).

## Facts used (ledger ids)

- **sources-ledger-gov:** A1a (0% bracket up to 1,978,745 ₪, first-flat FAQ), A1b (8% / 10% for a non-resident, to 10.2.2027; nothing published from 11.2.2027), A3 with LEDGER-DECISIONS 1 (the advance is only referred to c8; no rate restated in my parts), A5a (tax clearances for registration, glossary), B7a (188 ₪), B7d (44 ₪), B8d (digital extract is the original, glossary), B9 (deals database, free), C11a (capitalised lease, consent fees, glossary), D14a (7% and the securities), D14b (vouchers, glossary), D15a / D15b (linkage limits, compensation after one month), D16 (defects period starts at handover, glossary, no lengths), D18b (lottery types), E19a (מידע תכנוני link), E20 (pledges registry open to the public, glossary).
- **sources-ledger-law:** 1b (memorandum test, glossary), 2a, 2b, 2c (warning note), 3a, 3h (Sale Law, contracts from 7.7.2022), 4a (7%), 6a, 6c (betterment levy, glossary), 7a, 7b (municipal certificate), 8a, 8b (75 / 70 / 50%, 50% PTI, version of 30.6.2026), 10a, 10b, 10c (broker fee conditions, no legal tariff, glossary), 11 (agreed compensation, glossary), 15a (heirs: inheritance order, probate order, heirs' agreement after one of them), 16a (execution sale: 15 days, 10%, bidding, balance in 7 days, purchase confirmation for registration, alternative housing), 16b (partition: sections 37, 40, 40א), 17b (presumption of sharing applies to common-law couples).
- **Live page (with its own source):** eligibility certificate valid one year; Negev assistance 48,000 to 84,000 ₪ (Housing Ministry pages read 6.11.2026); the eligibility loan has no early-repayment fee (glossary).
- **LEDGER-DECISIONS applied:** 1 (advance: section 15(ב), not restated in c18 after c6/c8 cover it), 6 (since 2026 more licensed bodies may issue a guarantee: not needed after the guarantee FAQ was dropped), 7, 16 (heirs: "check with the lawyer"; urban renewal: "ask for the signed agreement and read it with the lawyer"; no building-file location claim).

## New facts fetched (WebFetch, read-only)

| URL | Read at | Used for |
|---|---|---|
| https://www.kolzchut.org.il/he/רכישת_דירה_בדיור_הציבורי (page updated 12.4.2026, 10:07) | 9.11.2026 03:44 | Today public-housing tenants cannot buy their public flat; the page's content was removed for that reason. c18 Amidar H3 and FAQ 7 |
| https://www.kolzchut.org.il/he/ידועים_בציבור (updated 21.10.2025) | 9.11.2026 03:46 | Common-law couples can apply for Housing Ministry assistance with a declaration form signed before a lawyer. c18 and FAQ 8 |
| https://www.kolzchut.org.il/he/מכירת_דירת_מגורים_במסגרת_מימוש_משכנתא_בהוצאה_לפועל (updated 10.5.2026, 08:32) | 9.11.2026 03:47 | Exact start points of the 15 days (from publication) and the 7 days (from being declared the winner), refining ledger row 16a |
| https://he.wikisource.org/wiki/חוק_מיסוי_מקרקעין_(שבח_ורכישה) | 9.11.2026 03:55 | Section 4: inheritance is not a sale. FAQ 15 (no capital-gains or purchase tax on receiving the inheritance itself) |
| https://www.kolzchut.org.il/he/ירושה and /מס_עיזבון | 9.11.2026 03:57 | Looked for a statement that Israel has no inheritance tax: the first page is an empty redirect, the second is 404. So the FAQ does not say "no inheritance tax in Israel"; it says only what section 4 says |

## Missing facts (left out, not stated as fact)

- What a buyer inherits from a signed urban-renewal agreement (ledger 19, LEDGER-DECISIONS 16): written as "ask for the signed agreement and read it with the lawyer".
- Whether heirs may sell before they are registered (15b): left to the lawyer.
- What co-ownership dissolution means in practice for a buyer beyond the law text (16c): only the law text is used.
- The registration fee for heirs' rights in 2026 (kolzchut shows 183 ₪ for 2025; the 2026 fee notice row was not in the gov ledger): no number.
- The 1/3 and 1/2 share rule for an additional flat (Amit Vered 164): not in my ledgers; W3's c8 covers it with its own source, so the inheritance FAQ only says "check with the lawyer".
- A statement that Israel has no inheritance tax: no official page found.
- The bank's financing limit for a foreign resident: the live FAQ says 50% (directive 329) but ledger row 8a lists 50% only for an investment flat, so c18 says "check with the bank" without a number.
- VAT when a company sells (only "ask the lawyer"; c6 covers it).
- Receiver price discount ranges (KON 6, 7: 5% to 10% deposit, 10% to 15% below market) and purchase-group savings (NM 18: 15% to 20%): competitor claims, not used.
- Discount-housing equity rule under directive 329 (8e): the mechanics were unclear in the ledger paraphrase, so no FAQ on it.
- Losing lottery eligibility after a free-market purchase (YLF 13): not confirmed, not written.

## Left out on purpose

- KZG (receiving a public-housing flat as a tenant: 4 working days, 60-day repairs): renting from the state is not a purchase, and kolzchut now says tenants cannot buy, so the guide states that and moves on.
- Tenant, company seller and seller's power of attorney as full c18 H3s: c6 covers them (see above).
- A separate H3 on building deviations: c7 owns the topic, so c18 has a table row and one line.

## Self-check (script run on the final files)

- Long dashes (U+2013, U+2014): 0 in all three files.
- Forbidden words (אטלס, Atlas, פראייר, דוגמה/דוגמא, UI talk, superlatives about us): 0.
- No paragraph opens with "קניית דירה"; no H2/H3 starts with a protected head phrase.
- Every `<td>` has `data-l` (c18 table: 27 cells).
- Tags balance in all three files (python html.parser, custom open/close stack): 0 errors, 0 unclosed.
- Every number in c18 has a `nlbg-note--fig` or a `nlbg-src` line; every number in the FAQ carries an inline source like the live FAQ; the glossary has no figures.
- 6-word runs: compared with the 204 extracted pages in `_private-research/2026-11-08-buying-guide-re/html/*.json`. Zero matches with any competitor. The only matches are with our own live page, where c18 names the live FAQ headings it links to and repeats the official figures (8% / 10%, the Negev amounts) in the same wording.
- Headings compared with the 19 live FAQ questions and all H3s in c1 to c17: no duplicate question.
