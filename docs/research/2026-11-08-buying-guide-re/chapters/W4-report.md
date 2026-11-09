# W4 report: chapters c10, c11, c12 (phase החתימה), HAD-686

Written 9.11.2026, 03:38 to 03:57 Israel time. Files: `c10.html`, `c11.html`, `c12.html` in this folder. Nothing else was edited, nothing committed.

## Words (Hebrew words, counted by script)

| Chapter | H2 | All text | Without source, kicker and back lines | Brief target |
|---|---|---:|---:|---:|
| c10 | חוזה קניית דירה יד שנייה: הסעיפים, מנגנוני ההגנה ועורך הדין | 1,882 | 1,790 | 1,600 |
| c11 | לוח התשלומים בעסקת יד שנייה: מה משלמים, מתי ומול מה | 990 | 929 | 600 |
| c12 | מעמד החתימה על החוזה: מה מביאים, על מה חותמים ומה לוקחים הביתה | 1,027 | 952 | 600 |
| Total | | 3,899 | 3,671 | 2,800 |

About 30% over the target. The overshoot is the 19 developer signing-day units (ELK 126 to 144, about 230 words in the last H3 of c12) and the seller-mortgage clearing units in c11. If the integrator must cut, the c12 H3 "חותמים מול קבלן" can move to chapter 17 as is.

## Structure notes for the integrator

- c10 is a new chapter head. The live section "תפקיד עורך הדין בקניית דירה" (H2, three paragraphs, nlbp-go link row) is marked with an HTML comment right after the todo box and stays unchanged; whether its heading stays H2 or becomes H3 is your outline call.
- The live nlbp-go row already links `/real-estate-lawyer/`, `apartment-sale-contract/`, `power-of-attorney-real-estate/`, `breach-apartment-sale-contract/`. c10 adds in-text links to the same four (anchors from page-9-internal-links.txt: עורך דין מקרקעין, חוזה מכר דירה, ייפוי כוח בעסקת מקרקעין, הפרת חוזה מכר) plus `/real-estate-lawyer/apartment-memorandum/` (זיכרון דברים). Drop one of each pair if you want one link per child per chapter.
- Other internal links: c11 `/real-estate-tax-advisor/capital-gains-tax-guide/` (מס שבח); c12 `/real-estate-lawyer/condo-documents/` (מסמכי הבית המשותף). Cross-links to `#nlbg-c1, c6, c7, c8, c9, c11 to c17`.
- Tool marks: `<!-- TOOL bpay -->` at the end of c11, `<!-- TOOL bsign -->` at the end of c12, each after one plain sentence on what the tool does (no internals assumed; tools-build-notes.md did not exist when I wrote).
- One fig note in c11 carries the label "כלל רשמי" instead of "מספר רשמי" because it states rules, not numbers (certificates needed for registration). Same class.
- Two source links are `http://masmak2026.mag.calltext.co.il/...` (the Tax Authority 2026 digital guide, as recorded in sources-ledger-gov A2c, A3, A5a).
- Live text conflict, not touched: the live lawyer section (and the live FAQ on who pays capital gains tax) says the advance is "7.5% מהמחיר ... אלא אם המוכר הציג אישור אחר". LEDGER-DECISIONS 1 adds the 15% rate for a seller who bought up to 6.11.2001. c11 states the full rule; the live sentence needs Ben's or the integrator's decision.

## Map units covered

Amit Vered map (amit-vered-map.md), stages Payment schedule, Lawyer, Signing meeting, Contract, Security mechanisms, Annexes, Accompanying documents, First payment, Cash deal (rows 193 to 245; YES rows 196, 197, 198, 200, 205, 222, 241 were already on the page):

- c11: 193, 194, 195 (schedule as protection, bad spread, buyer rationale and cash flow), 214 (with c10), 240 (partial: no percentage), 245 (cash deal). Also seller-mortgage units from other sections: 145 (official payoff balance), 146, 147, 297, 298, 299, 300 (drag, freeze, repay), 301, 302, 303 (clean extract and pledge registrar after payoff). These overlap W5's chapter 14 at concept level only.
- c10: 199, 201, 202 (selection, broker-referred lawyer, dispute), 211, 212, 213, 214, 215, 216, 217, 218, 219 (partial: no 10%), 220, 223, 224, 225, 226 (no day count), 227, 228, 229 (without the spouse practice), 230, 231, 232, 233, 234. From the lawyer gap list: 3, 64, 80, 100, 156.
- c12: 203, 204, 206, 207, 208, 209, 210 (venue yes, duration no), 221, 235, 236, 237, 238, 239 (partial: no cheque fee), 242, 243, 244.
- Count: rows 193 to 245 hold 53 units, 7 already YES, 46 PARTIAL/NO. All 46 are now written: 40 in full, 6 partly (5 because their number has no official source: 210 duration, 219 the 10%, 226 the 7 to 14 days, 239 the cheque fee, 240 the first-payment share; and 229 without the spouse-consent practice, per decision 16). Plus 15 units from other AV sections (145, 146, 147, 297 to 303, 3, 64, 80, 100, 156).

Other competitors (other-competitors-map.md):

- "החוזה ומנגנוני ההגנה" 5a: PR 17 (findings into binding clauses: repair, price cut, holdback, condition on the bank) in c10. PR 3 (one-view stage list) is the guide map, not mine.
- "לוח התשלומים" 6a: PR 48 in c11 (no statutory split stated, schedule fitted to bank release, number of payments follows time to handover, usual flow first / interim against documents / last against possession and transfer deeds).
- "יום החתימה" 7a: ELK 126 to 144 in c12 (venue, timing, ID with appendix and licence, cheque book, phone and email, printed annexes to compare, arrive early, the signing set in several copies, marking flat, balconies, laundry screen, parking and storage and signing in the centre, why the marking matters, voucher book check of flat number, floor and parcel, photos of cheques and annexes, contacts, no countersigned copy and asking for it with a full scan, the file). ELK 128 written without the clock hours; ELK 133 without "30 minutes" and dress.
- "עורך הדין והליווי": no new units listed there.
- Also touched in passing (owned by other writers): PR 13, 14 (contract shields for violations, bank condition) in c10; PR 18 (contents list; net versus gross area not written), PR 19, 20, 21, 22, 23 (usage fee), 25, 26; YLP 12, 13, 15, 16.

## Facts used and their ledger ids

| Fact | Where | Ledger |
|---|---|---|
| Land transaction commitment must be in writing (s.8); deal completes by registration, until then a commitment (s.7) | c10, c12 | law 1a; gov C11d (s.7); my fetch of s.7 |
| Warning note on a written commitment in a contract or irrevocable POA (s.126) | c12 | law 2a |
| Registrar deletes a note by court order, or when satisfied the parties agreed or its basis is void (s.132(א)) | c10 | law 2e |
| Agreed damages without proof of damage; court may reduce if no reasonable relation to foreseeable damage (s.15(א)) | c10 | law 11 |
| Warning note 188 ₪, deletion 127 ₪, mortgage 188 ₪, sale registration 44 ₪, signed online extract 18 ₪, condo file copy 39 ₪ (2026, from 1.1.2026) | c10, c12 | gov B7a, B7b, B7c, B7d, B7e, B7f, B7g; decision 9 |
| Online warning note: lawyers with a smart card, up to 3 business days; documents needed | c10, c12 | gov B8a, B8b; decision 9 |
| Online sale registration up to 16 business days | c10 | gov B8c; decision 9 |
| Extract and ILA rights confirmation are originals only in digital form; ILA confirmation 81 ₪; housing-company flat: ILA notice is free and not binding | c12 | gov B8d, C11c, C12; decision 10 |
| Buyer's declaration within 30 days; online through the lawyer's representative system; service free; contract and extract attached | c10, c12 | law 5a; gov A2a, A2b |
| Purchase tax within 60 days, deferred until possession, more than half paid, or POA for registration (s.51, 90א) | c11 | gov A2c; law 5b |
| Advance on capital gains tax: 7.5% / 15%, after more than 40% paid, none with the single-home exemption or a Tax Authority certificate (s.15(ב)) | c11 | decision 1; gov A3; law 5c |
| Registration needs no-debt certificates for capital gains, purchase and property tax | c11 | gov A5a |
| Registration needs a certificate that the betterment levy was paid or secured | c11 | law 6c |
| Registration needs a municipal certificate that the owner's debts on that property were paid (s.324) | c11 | law 7a |
| Bar's recommended minimum tariff: not binding (rule 2); 2026: 1% up to 633,967 ₪, 0.75% above | c10 | law 14a; decision 11 |
| Developer's lawyer fee charged to the buyer: lower of 0.5% or 5,915 ₪ plus VAT, price up to 4,642,750 ₪ | c10 | law 14b; decision 11 |
| VAT 18% from 1.1.2025 | c10 | gov A4; decision 12 |
| Stage payment table exists only for new construction when the security is not a guarantee or policy | c11 | gov D14c |
| Developer must notify the buyer in writing at signing of the right to security (s.2א1) | c12 | gov D14e |
| Voucher-only payment in a financed project; the lender issues the security within 14 business days (s.3ב) | c12 | law 4b; gov D14b |
| Median 4-room price 2,028,800 ₪ used for the tariff calculation | c10 | live page, its own sourced figure (Tax Authority deals, April to June 2026) |

Calculation shown in c10 (labelled as a calculation): 1% × 633,967 = 6,340 ₪; 0.75% × (2,028,800 − 633,967) = 10,461 ₪; total about 16,801 ₪ before VAT.

### Facts I fetched myself (not in the ledgers)

| Fact | URL | Read on |
|---|---|---|
| Material breach defined (s.6), including that a blanket "every breach is material" clause holds only if reasonable at signing; cancellation for material breach (s.7(א)); non-material breach only after an extension (s.7(ב)); cancellation by notice within a reasonable time (s.8); agreed damages do not bar other remedies (s.15(ב)); no enforcement or damages for unforeseeable circumstances that made performance impossible or fundamentally different (s.18) | https://he.wikisource.org/wiki/חוק_החוזים_(תרופות_בשל_הפרת_חוזה) | 9.11.2026 ~03:40, s.15(ב) re-read ~03:45 |
| A land deal requires registration and is completed by it; an unregistered deal is a commitment (s.7) | https://he.wikisource.org/wiki/חוק_המקרקעין | 9.11.2026 ~03:40 |
| Agency termination rules do not apply when the authority was given to secure another person's right that depends on performance (s.14(ב)), the basis of the irrevocable POA | https://he.wikisource.org/wiki/חוק_השליחות | 9.11.2026 ~03:41 |

Also read on Land Law: s.9 (priority of the first deal) was read but not used; s.91 is about mortgages, not POAs, so nothing on who must certify an irrevocable POA was stated.

## Missing facts (left out, no official source)

- Usual first-payment share (their 10% to 20%, sometimes 30% to 40%): written as "no rate in law, set in negotiation".
- Bank-cheque fee (their 13 to 14 ₪).
- Typical agreed damages of 10% of the price.
- Payment grace of 7 to 14 days: written as "ימים ספורים".
- Length of the signing meeting (their 1 to 1.5 hours); ELK clock hours for arrival; "30 minutes early".
- Who must certify an irrevocable POA for land (notary or lawyer): not found in the law sections read; written only as "אימות מסמכים אם יידרש" in the fee scope.
- The practice of a spouse's signature on the sale (decision 16): not stated; c10 only says the sellers bring every consent the bank requires, and points to chapter 6.
- When buyers usually pay their lawyer: no source; written as advice (tie part of the fee to registration).
- Typical time from signing to handover (PR 50, 45 to 90 days): not used.

## Self-check

- python html.parser: all three files parse, no mismatched tags, no inline styles, no scripts.
- Every `<td>` has a `data-l` equal to its column `<th>` (89 cells).
- Zero U+2013 / U+2014. No אטלס, Atlas, פראייר, דוגמה, "אפס".
- No H2 or H3 starts with a protected head phrase; no paragraph starts with "קניית דירה".
- Every number has a source line or a fig note with the ledger date 9.11.2026.
- 6-word overlap check against all private competitor block files (228,853 six-word runs): no hits in running text. Remaining hits are official law or rule titles inside source lines only ("חוק המכר (דירות) (הבטחת השקעות של רוכשי דירות)", "כללי לשכת עורכי הדין (התעריף המינימלי המומלץ)"). Earlier overlaps with our own live deadlines table were rewritten.
