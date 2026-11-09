# W5 report: chapters 13 to 16 (אחרי החתימה עד המפתח), HAD-686

Written 9.11.2026, about 03:40 to 04:10 Israel time. Files: `c13.html`, `c14.html`, `c15.html`, `c16.html` in this folder. No other file was edited, nothing was committed.

## Words (Hebrew words, body text; source lines, kicker and back link not counted)

| Chapter | H2 | Body words | With source lines | Target |
|---|---|---:|---:|---:|
| c13 | הערת אזהרה: ההגנה שנרשמת מיד אחרי החתימה | 1,175 | 1,271 | 900 |
| c14 | דיווח, אישורים ומשכנתאות: מה קורה בין החתימה למסירה | 1,749 | 1,890 | 1,600 |
| c15 | המסירה: הפגישה בדירה, הפרוטוקול והמפתחות | 816 | 836 | 600 |
| c16 | הרישום על שמכם: משטר המכר ועד נסח חדש | 738 | 797 | 600 |
| Total | | 4,478 | 4,794 | 3,700 |

c14 counts only new text; the live section "קניית דירה: המועדים אחרי החתימה" (table, paragraph, `#calendar` anchor and `[nadlan_tool id="bdates"]`) is not rewritten. A comment in c14 marks where it goes (as an H3, as in v3). I went over the target because the after-signing stage alone has 75 open units, and I already cut the parts that siblings cover (see "Overlaps").

Tool markers: `<!-- TOOL breg -->` at the end of c14 and `<!-- TOOL bkeys -->` in c15, under the protocol H3. The text around them matches what the tools do (see `inc/buying-hub.php` and `buying3.js`).

## Units covered

### amit-vered-map: the stages "After signing" (246 to 332), "Handover" (333 to 351), "Registration" (352 to 363)
These stages have 105 PARTIAL or NO units. My chapters cover 102 of them. Two more are covered in c11 (W4), which my chapters link to. One is left out on purpose.

- **c13 (warning note):** 247, 248, 249, 251, 252, 253, 254, 255, 256, 257, 258, 259, 260, 261. Units 246 and 250 were YES already and are expanded here.
- **c14 (report, tax, mortgages, certificates, deposit):**
  - Tax report and payment: 263, 264, 265, 266, 267, 268, 270, 271, 272, 273
  - Advance on the seller's tax, execution side: 277 (in the worked example; c8 states the rule), 278, 280
  - Your mortgage: 281 to 298
  - The seller's mortgage: 301, 302, 303
  - Municipal and tax certificates: 307, 309, 310, 311, 312, 313 (no fee figure), 314 (no time figure), 315, 316, 317, 318, 320, 321, 322
  - Tax deposit: 323, 324, 325, 326
  - Mortgage deeds: 328, 329 (no lead-time figure), 330, 331, 332
- **c15 (handover):** 333 to 351, all 19. Unit 349 (gas) is covered as an idea only.
- **c16 (registration):** 327, 352, 353, 354, 355, 356, 358, 359, 360, 361, 362, 363. Unit 357 was YES already and is expanded here.
- **Covered in c11 (W4) and linked from c14:** 299 (a bigger seller mortgage clears earlier in the schedule) and 300 (the three ways to clear it: pay off, drag, freeze).
- **Left out:** 319, the property-tax clearance rule for flats with no deal since 31.12.1999. LEDGER-DECISIONS item 16 and ledger row A5b say it is not confirmed.

### other-competitors-gaps
- **8a (bank after signing):**
  - In c14: ELK 149 (your own money is paid before the loan), ELK 154 and 155 (the developer signs the bank papers only after the contract's conditions are met, and nobody edits the bank's annex without its approval), ELK 156 (payment through the voucher booklet, with a pointer to c17).
  - ELK 152 is covered as an idea (start right after signing) without the competitor's "about a week".
- **8b (the warning note in plain words):** KZW 5 (the two exceptions: you agree, or a court orders), KZW 7 (a warning note is also a Sale Law security, pointer to c17), KZW 8 (the online route), and PR 51 (note versus registration). All in c13.
- **8c:** PR 50 is in c14 as a table of the official time for each step. There is no total figure, because no official one exists.
- **9a:** GIN 43, GIN 45 and MZ 16 (renovate while the flat is empty, move-day manners, contents insurance). All in c15.
- **10a (developer registration):** ELK 104, 183, 184 and 190 are covered briefly in c16, with a pointer to c17.
  - Section 6ב and the resale rules (ELK 105 to 112, 185 to 189) are fully in c17 (W6). I first wrote an H3 on section 6ב myself (checked on Wikisource), then removed it to avoid a second copy on the page.
- **10b:** GIN 40 is in c14 (the longer the gap between signing and handover, the more likely the approvals arrive in time).
- **Also covered:** GIN 38, 39 and 41 (mapped to Amit Vered units) in c14 and c16.

## Facts used (ledger ids)

- **c13:**
  - sources-ledger-law 2a, 2b, 2c, 2d, 2e (Land Law sections 126, 127(א), 127(ב), 128, 132(א), plus Kol Zchut's two exceptions)
  - Gov ledger B7a (188 ₪; no separate online fee; charged only when registered), B7b (127 ₪), B7g (valid from 1.1.2026, indexed each year), B7e (18 ₪)
  - B8a (online filing for lawyers only, Comsign or Personal ID; the document list; manual filing Sunday and Wednesday 08:30 to 12:30, by post or deposit box)
  - B8b (up to 3 business days, with the exclusions), B8d (anyone can order an extract; only the digital one is official)
  - C11c (81 ₪, credit card only, digital original), C11d (ILA: a deal not registered is only a commitment; no warning note on rights not yet in the land registry), C12 (housing company: free, non-binding notice from the ILA; the binding document comes from the managing body)
  - E20 (pledge registrar: open to the public, fee depends on the chosen period, 3 / 5 / 10 days)
  - Law 4a and gov D14a (a warning note with no earlier charge is a Sale Law security)
  - New: Land Law section 9, read on Wikisource (see below).
- **c14:**
  - A2a and law 5a (30 days); A2b (forms 7000, 7000ב and 7002; the representatives' system; online when not represented; manual only in exceptions; free of charge; contract, extract and abbreviated signatures form)
  - New: section 73(ג), the contents of the buyer's declaration (Wikisource, see below)
  - A2c and law 5b (60 days; deferral as in the live table); law 5g plus decision 3 (assessment difference within 15 days; after an objection, the undisputed part within 30 days); law 5h (purchase-tax approval only after full payment)
  - A5d (form 704: free, by appointment, passed to the handler within 5 business days); new: Kol Zchut, how to pay (regional office or online with the voucher's internet and assessment numbers; instalments carry interest and linkage)
  - A2d plus decision 3 (310 ₪ per two weeks, section 94א; a weekly arrears fine with NO rate; 5% administrative fine; 2 per mille for an exempt buyer who did not declare; the two fines do not apply to the same period); law 5d (section 94)
  - A3 plus decision 1, execution side only (after more than 40% of the price, not before day 30; voucher form 7152; reduction form 7155; does not apply when part of the price is not paid in money; the 7.5% rate in the worked example; a land-registry approval once the advance is fully paid)
  - Law 2a (the bank's warning note on the seller's undertaking to register a mortgage); B7c (188 ₪ for a mortgage); new: regulation 14 of the Land Regulations 2011 (Wikisource)
  - Law 7a (section 324; the certificate is not needed to register a mortgage), 7b (section 21 of the Local Councils Ordinance), 6c (betterment-levy certificate, Third Schedule section 10(א)), 7c (time-barred arnona: from 15.4.2015, 7 years)
  - A5a (no debts in capital-gains, purchase and property tax)
  - Timeline table: B8b, A5d, E20, B8c, A2a.
- **c15:** law 18a (the buyer steps into the landlord's shoes; the detail is left to c6), 12a (electricity: the IEC site, the change-of-customer form, phone 103, the form fields, the final bill stays with the outgoing customer), 13a (arnona, sections 325 and 326), 13b (water: report the number of residents; charged as two persons without a report; a refund for a late report covers at most 6 billing periods, 12 months).
- **c16:** C11d plus the Land Law section 7 text (Wikisource); B7d (44 ₪); B7c (188 ₪); B8c (16 business days, with the exclusions); C11a (ILA transfer of rights); C11b (stated as not published); C11c (digital original); B10 (Housing Ministry registration status); B7e (18 ₪); new: section 73(א) (Wikisource).

### Read today with WebFetch (official texts only), 9.11.2026, 03:42 to 03:46 Israel time
- https://he.wikisource.org/wiki/חוק_המקרקעין : section 7(א), (ב) and section 9, read in full.
- https://he.wikisource.org/wiki/חוק_מיסוי_מקרקעין_(שבח_ורכישה) : section 15(ד)(1), (2) (the advance counts as the seller's tax payment and as part of the price, whatever the contract says); section 73(א) and (ג) (contents of the seller's and the buyer's declarations; the buyer's includes the Cash Use Reduction Law details).
- https://he.wikisource.org/wiki/חוק_המכר_(דירות) : sections 6ב and 6ג. Checked, then the H3 that used them was removed because c17 covers them (the wording matches c17's).
- https://he.wikisource.org/wiki/תקנות_המקרקעין_(ניהול_ורישום) : regulation 14(א), (ב) (the lawyer has the parties sign and verifies the signatures; with several lawyers, each verifies his own client).
- https://www.kolzchut.org.il/he/תשלום_מס_רכישה : how to pay (regional collection department, or the online system with the voucher's internet number and assessment number); instalments carry interest and linkage. Page updated 2.3.2025.

## Missing facts (the idea is written without a number)
- **Housing company:** fee and processing time for registering the buyer's undertaking (Amit Vered: 7 to 14 days, 150 to 500 ₪, plus 350 ₪). Not found on an official page.
- **Israel Land Authority:** processing time for registering an undertaking, and the time and fee of a rights transfer (C11b, decision 10).
- **Pledge registration fee** (E20, decision 16): it depends on the chosen period, and no amount is printed.
- **Municipal certificate fee and processing time** (Amit Vered: 100 to 200 ₪, 30 days, 3 to 4 months). Not read on any authority's page.
- **Time to get each approval:** betterment-tax approval, the bank's mortgage file, and the lead time for mortgage deeds (Amit Vered: 7 to 10 business days). None has an official figure.
- **Fees and rules that are not confirmed:** the electricity name-change fee (12b); water meter-reading rules (13c); gas account transfer and the deposit (no source); the fee for deleting the seller's mortgage (not in the ledger).
- **Form 7000א** for several buyers who are not one family: not confirmed. The ledger names 7000ב and 7002, and those are the forms used.
- **Total time from signing to handover** (PR: 45 to 90 days): no official source, so the chapter gives the official step times instead.
- **The Bar's recommended fee for a warning note** (748 or 1,068 ₪ in row 14a): it is unclear which amount applies, so it is not used.

## Left out on purpose
- **Not confirmed or contradicted:**
  - The 31.12.1999 property-tax rule (decision 16).
  - Amit Vered's "150 ₪ online" warning-note fee: the 2026 fee notice has one amount, 188 ₪.
  - "30 days" to pay an assessment difference: section 91(א) says 15 days (decision 3).
  - "0.2% a week": decision 3 says to state the rule without a rate.
- **Already written by other writers, so kept out to avoid a second copy on the page:**
  - The advance rates and its exemptions (c8, W3; also in c11). c14 links to c8 and keeps only the execution.
  - The three ways to clear the seller's mortgage (c11, W4). c14 links to c11.
  - The tenant-law rule (c6, W2, and c18). c15 links to c6.
  - Section 6ב and developer resale (c17, W6). c16 points to c17.

## Notes for the integrator
1. The live deadlines table, row "מקדמה על מס שבח", shows 7.5% only. Decision 1 adds 15% for a seller who bought up to 6.11.2001. I did not touch the live text; the row needs the second rate, or a link to c8.
2. c8 (W3) also prints the lateness fines (310 ₪, weekly fine, 5%, 15 days), and c14 prints them too because my brief asks for them. Keep one copy. The best home is c14, since c8 already says the full deadlines are there. c14's fine box adds two items c8 lacks: 2 per mille for an exempt buyer who did not declare, and that the two fines do not overlap.
3. c14 holds the existing deadlines section as an H3 in the same place v3 put it. My H3s follow it.
4. Links:
   - Child pages: c13 /tabu-extract-check/; c14 /purchase-tax-calculator/, /mortgage-home-insurance/, /real-estate-tax-advisor/betterment-levy/; c16 /tabu-extract-check/. Each anchor is the one used in page-9-internal-links.txt.
   - Chapter anchors: #nlbg-c2, c6, c8, c10, c11, c13, c14, c16, c17.

## Self-check
- **Rules:** zero long dashes (U+2012 to U+2015 checked); zero of the forbidden words (אטלס, Atlas, פראייר, דוגמה, "הכלי שלנו"). No H2 or H3 starts with a protected head phrase, and no paragraph opens with "קניית דירה". Every answer sentence is under 40 words (36, 29, 26, 30).
- **HTML:** every `<td>` has `data-l` (42 cells). All four files parse with python html.parser, with no unclosed or mismatched tags.
- **Sources:** every official number has a `nlbg-note--fig` box or a `nlbg-src` line, dated 9.11.2026.
- **Copying:** against all 405 private competitor extractions, zero runs of 6 words match (I rephrased the few law-title and wording collisions). Against the live page, zero. Against the sibling chapters, the only shared runs are the box title "מה עושים בשלב הזה" and one fee list (44 ₪ / 188 ₪).
