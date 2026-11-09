# W2 report: chapters c5, c6, c7 (page 9 /buying-apartment/, HAD-686)

- Writer: W2. Written 9.11.2026, 03:40 to 04:01 Israel time (machine clock). Nothing committed.
- Files: `chapters/c5.html` (additions, 3 `nlbg-add` blocks with placement comments), `chapters/c6.html` (new chapter), `chapters/c7.html` (new chapter, with a `MOVE HERE` comment where the live H3 "קניית דירה עם חריגות בנייה" goes; W2 wrote only additions for that part).

## Words (Hebrew)

| Chapter | Target | Body words (no source lines, who chips, kicker, back link) | All Hebrew words in the file |
|---|---|---|---|
| c5 additions | 1,100 | 1,488 | 1,620 |
| c6 new | 900 | 1,398 | 1,492 |
| c7 new | 1,200 | 1,668 | 1,761 |
| Total | 3,200 | 4,554 | 4,873 |

I went past the target so that every open map unit in scope has a place. If the page has to be shorter, cut these first, in this order: the mushaa H3 in c5, the bylaws H3 in c7 (תקנון מצוי או מוסכם), the "lost permit" H3 in c7, and the closing disclosure list in c6. Each of them can lose a paragraph and still keep its unit.

## Self-check (script, 9.11.2026 04:00)
- Python html.parser: no errors, no unclosed tags, in all three files.
- Long dashes (U+2013, U+2014): 0. Forbidden words (אטלס, Atlas, פראייר, דוגמה, "הכלי שלנו"): 0. No paragraph or list item starts with "קניית דירה". No H2 or H3 starts with a protected head phrase.
- Every `<td>` has a `data-l`, and each one matches its column's `<th>` (checked by script).
- Answer sentences: 28, 28 and 27 words.
- I compared 6-word runs against all 201 competitor HTML files in `_private-research/.../html/`. The first pass found 7 runs (law names and set legal phrases); I reworded all 7, and the second pass found 0.
- Internal links: c6 → /real-estate-lawyer/power-of-attorney-real-estate/ ("ייפוי כוח בעסקת מקרקעין"). c7 → /real-estate-lawyer/condo-documents/ ("מסמכי הבית המשותף"), /real-estate-tax-advisor/betterment-levy/ ("היטל השבחה"), /real-estate-appraiser/ ("שמאי מקרקעין"). Anchors come from page-9-internal-links.txt. c5 adds no internal link, because the live H2 already links /tabu-extract-check/ and /real-estate-lawyer/condo-documents/. Cross-chapter anchors: #nlbg-c6, c7, c8, c10, c11, c13, c14, c15, c18.

## Units covered

### amit-vered-map.md (Checks part A)
- **Rights and registration (c5):** #24 area mismatch; #31 finding the block and parcel; #33 sub-parcel versus mushaa; #36 how and when the seller got title (with the 7.5% / 15% advance link); #41 rights confirmation per register (extended); #357 three registers (extended); #209 and #260 re-check the extract (todo box).
- **Seller identity and spouse (c6):** #42, #43 (partial: the bank waiver is written as "ask your bank", since the practice is not confirmed), #49 (without the "fraud is rising" trend, which has no source), #50, #51, #52, #53 (consent in writing is offered as an option, not stated as practice).
- **Occupants (c6):** #44, #45, #46, #47, #48.
- **Condominium file (c7):** #54, #55, #56, #57, #58, #59, #60, #61, #62, #63 (partial: "ask the bank whether its appraiser needs the plan"), #64, #65 (also in c5).
- **Planning (c7):**
  - #71 (partial: where the file is kept, as general practice; "free" is not stated), #72, #74, #75, #77, #78, #79, #80, #81, #82.
  - #84 (partial: ask the collections department about debts, fines or open demands; no claim that a municipality withholds the certificate because of violations).
  - #85, #86, #87, #88 (pointer only: ask the lawyer, link to c8), #89, #90, #92, #95.
  - #96 (levy confirmed; extra arnona written as "sometimes"), #97, #98.
- **Count:** 54 Amit Vered units: 46 covered in full, 8 partial (#43, #49, #53, #63, #71, #84, #88, #96). Of the 54, #41, #357, #209 and #260 were already YES or PARTIAL on the page and are extended here.

### other-competitors-map.md (בדיקות לפני קנייה: rights, seller, condominium, planning)
- **Cluster 1a:** YG 4, PR 47, YLP 23, MAD 5.
- **Cluster 1b:** YG 11, YG 12, PR 9, YLP 39 (partial: consent fees and lease debts; initial and annual fees not detailed), GOV 6. Also GOV 8 (the list of developers that refuse to register).
- **Cluster 1c:** YG 21 (partial: expropriation note only), YG 27, PR 11, PR 13, PR 14, YLP 33, YLQ 25.
- **Related rows deepened:** YG 7, 8, 9, 15, 16, 17, 18, 22, 23, 25, 26, 28; PR 7, 8, 24, 43 (pointer to c18); YLP 10, 40; YLQ 4, 24, 27; MAD 4.
- **FAQ candidates answered in the body:** #11 (how to check an extract, by address, for free), #38 (how to make sure the seller is the owner), #24 (partial), #27 (partial), #49 (partial).

## Facts used

### From sources-ledger-gov.md
- **B7e:** extract 18 ₪ online, 88 ₪ certified copy, 154 ₪ concentrated condominium extract.
- **B7f:** condominium file 39 ₪ online with an email within 24 hours; physical inspection with a copy 257 ₪.
- **B7g:** the fees are valid from 1.1.2026 and are updated by the index.
- **B8d:** anyone can order an extract; the digital file is the original.
- **A3 with LEDGER-DECISIONS 1:** the advance is 7.5% or 15% by the seller's acquisition date and always 7.5% for a company. It is paid after more than 40% of the price. It does not apply when the seller asks for the exemption or shows a Tax Authority certificate.
- **A4:** VAT 18% from 1.1.2025.
- **A5a:** registration needs a certificate of no capital-gains, purchase or property tax debts.
- **B10:** the Housing Ministry registration-status lookup: its stages; it is anonymous, free and not an official extract.
- **C11a:** ILA transfer: all rights holders apply, by registered post; a capitalised flat needs no approval; consent fees and lease-fee debts.
- **C11c:** the ILA rights confirmation: 81 ₪, credit card only, through "רמ״י שלי"; the digital copy is the original.
- **C11d:** the lease must be in force and there must be no debts; ILA registers no warning note on rights not yet registered.
- **C12:** for a flat with a housing company, ILA gives only a free notice that is not binding.
- **D17b:** the list of developers that refuse to register, 17 entries.
- **E19a:** the planning-information system, official since 1.5.2022.
- **E20:** the pledges registry exists and is open to the public.

### From sources-ledger-law.md
- **2a to 2d:** sections 126, 127(א), 127(ב), 128.
- **6a, 6b:** the betterment levy is half of the gain, paid at the latest when the right is realised.
- **15a:** heirs need an inheritance order or a probated will.
- **17a, 17b:** the spouses' property law (sections 4 and 11) and the presumption of sharing (married before 1.1.1974, common-law partners).
- **18a:** the buyer steps into the landlord's place, and the residential landlord must give written notice.

### Read by me (WebFetch, read-only, 9.11.2026)
| Source | URL | Read at (about) | Used for |
|---|---|---|---|
| Land Law (Wikisource) | https://he.wikisource.org/wiki/חוק_המקרקעין | 03:44 and 03:55 | ss. 7(ב), 29, 52 ("דירה" covers a business or any purpose; definition of "רכוש משותף"), 55(א), 55(ג) (attachment is set in the bylaws, never for stairwells, a lift, shelters or shared facilities), 57(א), 62(א) (changing agreed bylaws needs owners holding two thirds of the common property; a new attachment needs all owners), 64 (the standard bylaws apply by default), 71א, 71ב (special majority; relative building rights protected), 145 (amending the registration order), 146 (cancelling it) |
| Planning and Building Law (Wikisource rendered page, plus raw text from offset 560000) | https://he.wikisource.org/wiki/חוק_התכנון_והבניה and https://he.wikisource.org/w/index.php?title=חוק_התכנון_והבניה&action=raw | 03:46 to 03:50 | s. 145(א) (what needs a permit; interior changes to a flat are excluded), s. 203 (definition of "עבודה אסורה"), s. 221 (administrative demolition order: who issues it, the six-month limit and 30 days from occupancy), s. 243 (up to two years in prison or a fine) |
| Agency Law (Wikisource) | https://he.wikisource.org/wiki/חוק_השליחות | 03:51 | s. 14(א) (agency ends on cancellation, death, loss of capacity or bankruptcy), s. 14(ב) (an authorisation that secures another person's right) |
| Sale (Apartments) Law (Wikisource) | https://he.wikisource.org/wiki/חוק_המכר_(דירות) | 03:52 | s. 1, the definition of "מוכר", which supports "a second-hand deal has no defects period" |
| Kol Zchut, protected tenant (updated 20.11.2025) | https://www.kolzchut.org.il/he/דייר_מוגן | 03:52 | eviction only on the grounds in section 131 of the Tenant Protection Law |
| Pledges Law (Wikisource) | https://he.wikisource.org/wiki/חוק_המשכון | 03:54 | read for background; nothing from it is stated in the text |
| Tried, no result | kolzchut ייפוי_כוח_מתמשך (404, two spellings); kolzchut רשם_המשכונות (404); Companies Law on Wikisource (s. 178 there is about share certificates; the rule on registering a company's charges was not found) | 03:51 to 03:54 | nothing used |

## Missing facts (written as an idea without a number or rule, or left out)
1. **ILA:** the time and fee for a transfer of rights (C11b, not stated on the page).
2. **Housing company:** the fee for its rights confirmation and the name of its document. The table says "לפי תעריף החברה".
3. **Pledges registry:** the search and registration fees (E20). Also not confirmed: that rights in a housing-company flat are pledged there. The text says only that the lawyer searches there for such flats.
4. **Companies registrar:**
   - not confirmed: the fee for a company extract, and the rule that registers a company's charges (Companies Ordinance; not fetched);
   - written as a check item only.
5. **Building file (E19b):**
   - not confirmed: that the local committee keeps it, and that viewing it is free;
   - used: the general-practice wording from LEDGER-DECISIONS 16, with no source line.
6. **Name and ID mismatch:** the Land Registry identification procedure was not read on gov.il. The text says only "עורך הדין מסדיר את הזיהוי מול לשכת רישום המקרקעין".
7. **Continuing power of attorney:** whether selling the home needs court approval (the Kol Zchut page returned 404). No rule is stated.
8. **Protected tenant:** whether the protection continues after a sale is not stated by Kol Zchut. Only the eviction-grounds rule is used.
9. **Spouse:** the practice of a spouse's signature (law 17c, LEDGER-DECISIONS 16). It is offered as an option to decide with the lawyer.
10. **Municipal certificate:** that a municipality withholds it because of building violations (#84). It is written as a question to the collections department.
11. **Extra arnona on a built-over area:** a general practitioner point, written with "לפעמים", and no source.
12. **The fraud trend (#49):** no official statistic, so it is left out.
13. **An administrative fine for building offences:** not found in the part of the law I read, so it is not stated.
14. **GovMap:** named as the government map for finding the block and parcel by address. It is not linked, and it was not re-checked today.

## Left out on purpose
- **The warning-note mechanics** (fees, online filing, the housing-company note fee, the pledge fee): they belong to c13 (W5), which already covers them. c5 keeps only one line on section 127(ב) and links to c13.
- **The 140 sqm levy exemption and the VAT detail:** c8 (W3) covers them. c7 and c6 link to c8.
- **The seller-mortgage payoff mechanics:** c11 (W4) covers them. c5 links to c11.
- **The units on the physical inspection** (#13 to #23, #66 to #69): they belong to W1's c4.
- **No 301 or redirect, no noindex, and no sitewide change** anywhere in these fragments.
