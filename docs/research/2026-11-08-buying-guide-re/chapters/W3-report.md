# W3 report: chapters 8 and 9 (page 9 /buying-apartment/, HAD-686)

Written 9.11.2026, 03:40 to 04:00 Israel time. Files: `chapters/c8.html`, `chapters/c9.html`. Nothing else was edited, nothing committed.

## Words (Hebrew words)

| Chapter | Body (without source lines) | With source lines | Target |
|---|---:|---:|---:|
| c8 המסים בעסקה מהצד של הקונה | 1,790 | 1,983 | 1,300 |
| c9 משא ומתן וזיכרון דברים | 1,313 | 1,385 | 1,000 |
| Total | 3,103 | 3,368 | about 2,400 |

Over target by about 30%. The reason is the order to cover every PARTIAL/NO unit (62 units across the two chapters). If the integrator needs to cut, the safest cuts are the VAT H3 in c8 (short, partly on the live cost table) and the closing paragraph of each H3 that only links onward.

## Structure

- **c8** (שלב 8 מתוך 18 · לפני החתימה). H2: המסים בעסקה מהצד של הקונה: מה אתם משלמים ומה בודקים אצל המוכר. H3s: כמה מס רכישה משלמים על דירה ראשונה? · האם בן הזוג נחשב לעניין דירה יחידה? · מי זכאי להנחה במס רכישה? · איך מקטינים את המס בדרך חוקית? · מי משלם מס שבח, ולמה זה מעניין את הקונה? · מה זו מקדמה על חשבון מס השבח? · מתי משלמים היטל השבחה, ומה הקונה בודק? · מה זה פטור 140 מטר מהיטל השבחה? · מתי מס השבח של המוכר נדחה ועובר אליכם? · יש מע״מ בקניית דירה? · מה קורה אם מאחרים בדיווח או בתשלום?
  `<!-- TOOL bwho -->` sits right after the seller-tax H3. The existing tool moves there together with its anchor `<span id="who-pays">` (the live FAQ links to `#who-pays`).
- **c9** (שלב 9 מתוך 18 · החתימה). H2: משא ומתן וזיכרון דברים: מה כבר מחייב לפני החוזה. H3s: מה זה זיכרון דברים, ומה כותבים בו? · האם זיכרון דברים מחייב? · למה לא לחתום על זיכרון דברים לפני הבדיקות? · מתי מתחילים 30 הימים לדיווח לרשות המסים? · כבר חתמתם על זיכרון דברים: מה עושים עכשיו? · המוכר מתעקש על זיכרון דברים: איך מצמצמים את הסיכון? · דמי רצינות: כמה משלמים ולמי? · איך מנהלים משא ומתן על מחיר דירה? · על מה מתמקחים חוץ מהמחיר? · מתי מגיעים למתווך דמי תיווך? · מתי עוזבים את המשא ומתן?
  `<!-- TOOL bmemo -->` sits after "כבר חתמתם". The six questions in the text before it match the tool's six questions in `buying.json` (memo.q). The boffer tool is linked through the existing live anchor `#offer`, with the live CTA anchor text "הצעת מחיר לדירה". There is no `#boffer` element on the live page; `boffer` only appears in the shortcode.

## Units covered

**amit-vered-map, Checks part C (tax), units 148 to 177: all 17 PARTIAL/NO units covered**
150, 151, 152, 156, 157, 161, 163, 164, 166, 167, 168 (linear route named, not detailed), 169, 172 (as an "imagine" case, no numbers), 174, 175, 176, 177.
Also covered on the way, though they belong to the post-signing stage: 277 (s.15(ד): counted both ways), 278 (full advance gives the betterment-tax clearance), 280 (no advance on a qualifying-home exemption sale).

**amit-vered-map, Memorandum, units 178 to 192: all 13 PARTIAL/NO units covered**
178, 179, 180, 181, 183, 184, 185, 186 (written as the intent test: a signature is strong evidence but not the whole test; not stated as a rule that an unsigned memo binds), 187, 188, 189, 191, 192.

**other-competitors-gaps, המסים מצד הקונה and זיכרון דברים ומשא ומתן: 32 units listed, 29 covered, 1 partial, 2 left out**
- 3a: KZP 7, 8, 9, 12, 17, 23: covered (group list and the medical committee; no rates).
- 3b: KZP 3, 4, 25 and KZS 13: covered. KZS 12: left out (ruling not read).
- 3c: KZP 18, 22, 24: covered (ss.102, 103, 103א; hotline *4954). YG 33: covered as practice (keep a document for every equity source). YG 32: left out (not confirmed, as the gaps file says).
- 3d: KZH 3, 4, 7, 8, 9: covered.
- 3e: ELK 195, 197, KZS 2, 3, 4, 5, 10: covered. ELK 198: partial (the 18 months run "from the day it became a dwelling", per A6; the Form 4 link is not verified).
- 3f: YG 38 (general line), YLF 5 (marginal-bracket point with a worked computation): covered.
- 4a: YLP 36: covered, plus YLP 35 and 37 (payment dates, furniture, parking, storage).

## Facts used

**From the ledgers**
- Decisions: 1 (the advance, stated exactly), 2 (8% and 10% "לרכישות עד 10.2.2027" from the notice of 12.10.2026; single-home brackets frozen to 15.1.2028; no bracket table), 3 (310 ₪ per two weeks; late payment without a rate; 5% administrative fine; 15 days for an assessment difference), 11 (the developer's lawyer cap is only mentioned, without its numbers), 12 (VAT 18%), 15 (24 months, as on the live page), 16 (no 31.12.1999 property-tax rule).
- Gov ledger: A1a (first-bracket threshold, used in the computation), A1b, A2a, A2c, A2d, A3, A4, A5a, A6 (exemption conditions; cap 5,008,000 ₪ to 31.12.2027), B9 (Tax Authority deal database, free).
- Law ledger: 1a (s.8), 1b (Kol Zchut's two tests), 2a (s.126), 5a, 5b, 5e, 5g (15 days per decision 3), 5h, 6a, 6b, 6c, 6d, 7a, 10a (including "whether VAT is included"), 10b, 10c, 11.
- Live page rows: national median for a 4-room flat, 2,028,800 ₪ (Tax Authority deals, April to June 2026), and its purchase tax of 1,752 ₪. Developer VAT included in the price (live cost table).
- My computation: an additional home at the same price is 8% × 2,028,800 = 162,304 ₪, and 2,028,800 minus 1,978,745 = 50,055 ₪ taxed at 3.5% = 1,752 ₪, the same as the live hero.

**New reads (not in the ledgers), read-only**
1. Land Taxation Law, raw wikitext, downloaded 09.11.2026 03:43: `https://he.wikisource.org/w/index.php?title=חוק_מיסוי_מקרקעין_(שבח_ורכישה)&action=raw`. Used:
   - s.1: the definition of "מכירה", which includes granting a right to receive a right in land;
   - s.4 (inheritance is not a sale) and s.4א (on a divorce-judgment transfer, the acquisition value and date carry over);
   - s.9(א) (the buyer owes purchase tax), s.9(ג1ג)(4)(א) and (ג) (the family unit; shares per s.49ג(3); protected tenancy before 1.1.1997);
   - s.15(א) to (ה) and (ח) (matches decision 1);
   - s.29 with s.62 (a gift to a relative is exempt; the giver's acquisition value carries over);
   - s.39 (deductions: improvements, lawyer, appraiser and surveyor, broker up to 2%);
   - s.49 (qualifying dwelling: used mainly as a home for 4/5 of the period or the 4 years before the sale) and s.49ג(3) (one third, one half if inherited);
   - s.73(א), s.84 (artificial transactions), ss.102, 103, 103א, and the chapter on options (פרק חמישי 2).
2. Planning and Building Law, raw wikitext, downloaded 09.11.2026 03:43: `https://he.wikisource.org/w/index.php?title=חוק_התכנון_והבניה&action=raw`. Used from the Third Schedule:
   - s.1 (the definitions of השבחה and מימוש זכויות);
   - s.4(1) and 4(4)(א) (an assessment the owner demands within 90 days), s.4(7) (assessed as of the plan's start day);
   - s.6(ד) (warning notes for the levy);
   - s.14(א) (appeal within 45 days) and 14(ב)(1) (decisive appraiser);
   - s.19(ב)(7) (accessibility, including a lift), 19(ב)(9) (safe room), 19(ג)(1) and (2), 19(ג1).
3. Kol Zchut, מס רכישה, page updated 8.7.2025, read 09.11.2026 about 03:45 and 03:47. Used: the relief groups, the medical committee procedure, the refund and cancellation procedures, hotline *4954, and the title of the same-sex ruling.
4. Kol Zchut, היטל השבחה, page updated 29.11.2023, read about 03:45. Used: the levy is paid to the local authority; it is computed at plan approval and usually paid at sale; objection to the amount or to the debt; no levy on plans approved before 1.7.1975; the triggers.
5. Kol Zchut, הנחה במס רכישה בהעברת זכויות במקרקעין לקרוב משפחה ללא תמורה, page updated 8.7.2025, read about 03:46. Used: a 2/3 discount, and the list of relatives (spouse, sibling, child or grandchild, a child's spouse).
6. Kol Zchut, פטור ממס רכישה בהעברת זכויות מקרקעין בדירה לבן זוג ללא תמורה, page updated 21.7.2026, read about 03:46. Used: an exemption for spouses who live together, including same-sex couples; 2/3 for spouses who do not live together.
7. Kol Zchut, זכותון ללקוחות של מתווכי דירות ומקרקעין, page updated 26.8.2026, read about 03:46. Confirms 1b, and adds that the broker's right to a fee arises once there is a binding agreement.

## Missing facts (written as ideas, or left out)

- The seller's linear calculation: the dates and the method. It is named only.
- Whether "dwelling" for the 18-month test needs a completed building or Form 4 (ELK 198).
- Reporting the source of financing to the Tax Authority within six months (YG 32): not confirmed, not written.
- The ruling on shared living and separate property (KZS 12): not read.
- The rate and conditions of each relief group: not stated; the reader is sent to the official page and *4954.
- The weekly late-payment rate (0.2% against 0.5%): left without a rate, per decision 3.
- The property-tax clearance for flats with no deal since 31.12.1999: not stated, per decision 16. Only A5a is used.
- Who pays the levy for a plan approved between signing and sale: not stated (unverified).
- The 1.7.1975 levy cut-off is stated from Kol Zchut only; it is not in the law text read.
- The gift carry-over is stated for value only (s.29); the acquisition date was not verified for gifts. It is stated for divorce (s.4א).

## Left out on purpose

- A second bracket table (decision 2). Only the first-bracket threshold appears, inside the worked computation.
- The numbers of the developer's lawyer cap: they are already on the live page and belong to c10 and c17.
- The purchase-tax payment channels, the voucher and the bank's documents: c14 (W5).
- The mechanics of the tax deposit: c10 (W4) and c14 (W5). c8 only says why it is needed and links to them.

## Notes for the integrator

1. **Live text to correct (report only, not edited).** The live FAQ "מי משלם את מס השבח...", the lawyer section and the deadlines-table row "מקדמה על מס שבח" all give 7.5% only and "אחרי שעברו 40%". Decision 1 requires both rates (15% for a seller who bought up to 6.11.2001) and "more than 40%" (80% from a contractor). The bwho data already holds 15% (orechdin.cgt_advance.rate_old).
2. **Overlap with W5 c14.** c14 also has H3s on the advance and on late payment. c8 explains them before signing, to plan the contract; c14 covers doing them after signing. To avoid repetition, keep the advance fig note in one chapter and cross-link it from the other.
3. **Anchors used.** Existing on the live page: `#benefits`, `#before-sale`, `#offer`. New chapters: `#nlbg-c1`, `#nlbg-c7`, `#nlbg-c8`, `#nlbg-c10`, `#nlbg-c11`, `#nlbg-c14`, `#nlbg-map`.
4. **Child links, one per child per chapter, with anchors from page-9-internal-links.txt.**
   - c8: /purchase-tax-calculator/ "מחשבון מס רכישה", /real-estate-tax-advisor/ "יועץ מס מקרקעין", /real-estate-tax-advisor/betterment-levy/ "היטל השבחה", /real-estate-tax-advisor/capital-gains-tax-guide/ "מס שבח".
   - c9: /real-estate-lawyer/apartment-memorandum/ "זיכרון דברים", /selling-apartment/who-pays-broker-fees/ "מי משלם דמי תיווך", /real-estate-broker/ "מתווך נדל״ן: מה בודקים".

## Self-check

- python html.parser: 0 errors, no unclosed tags, in both files.
- Long dashes (U+2013, U+2014): 0. Forbidden words (אטלס, Atlas, פראייר, דוגמה, slogans, site or UI talk): 0.
- No tables, so there is no `<td>` to carry `data-l`.
- No H2 or H3 starts with a protected head phrase. No paragraph opens with "קניית דירה". Answer sentences are 36 and 31 words.
- Every number has a fig note or a source line, with the reading date 9.11.2026.
- 6-word overlap: checked against all 204 private block files (our own live page among them) (348,114 six-word runs). 0 hits against competitors. Four phrases that first matched Amit Vered, Kol Zchut (two pages) and shoora.co.il were rewritten. 2 hits remain, both against our own live page: the 24-months phrase and the live anchor text of the bsell calculator.
