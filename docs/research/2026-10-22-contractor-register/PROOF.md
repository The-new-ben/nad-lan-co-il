# Proof: /pinkas-hakablanim/ against the pages that rank for the contractor register (22.10.2026)

The method is the same as for /prices-greece/: two scripts read every page as Google gets it.

- `tools/fact_coverage.py` checks 32 facts a buyer needs before signing with a contractor (`coverage-facts.json`).
  - The facts were written from the official pages and from Google's "People also ask", not from our page.
  - They include facts our page did not have.
- `tools/depth_proof.py` counts words, figures, tables, tools, FAQ and schema.

The 10 competitors are the content pages in the top 10 of the five SERPs in `serps.json`. The gov.il search service itself is not counted. Read at 22:43 on 22.10.2026.

## Facts covered (of 32)

| Page | Facts |
|---|---|
| **nad-lan.co.il/pinkas-hakablanim/** | **31** |
| nadlancenter.co.il/article/6331 | 13 |
| thebuilder.co.il (סיווג קבלנים) | 10 |
| midrag (article 14754) | 6 |
| hatikva.org.il (פנקס הקבלנים) | 6 |
| yuvalsegal.co.il | 5 |
| michlal.com (רשם הקבלנים) | 4 |
| medicalmalpractice, greeninvoice, rkablanim | 1 each |
| renovations.org.il | 0 |

**Only we state:**
- the classification amounts in force from 1.10.2026. Every competitor quotes an older table, or none.
- the area limits for residential building;
- the statuses מוקפא, מוחרג and מותלה, and the registrar's decisions list;
- that individuals' ID numbers are not published (so you search them by name or contractor number);
- the true number of contractors (17,874). Others say "12,000" or "14,000".
- the date of the data.

The full matrix is in `proof-facts.md`.

## Depth

| | Words | Figures | Tables | Cells | Tools | FAQ |
|---|---|---|---|---|---|---|
| **ours** | 2,144 | 252 | 4 | 237 | 2 | 10 |
| hatikva | **2,886** | 35 | 0 | 0 | 0 | 5 |
| midrag | 1,733 | 49 | 2 | 27 | 1 (a lead form) | 0 |
| rkablanim | 1,031 | 11 | 0 | 0 | 0 | 0 |
| michlal | 825 | 11 | 0 | 0 | 0 | 2 |

## Honesty statement

1. **Words.** hatikva has more words (2,886 against our 2,144). Most of its text is sales copy, and it has unfilled "איקס" placeholders. We did not pad.
2. **Pictures.** Most competitors have stock photos; we have none. Our visuals are the two tools and three bar charts, which are HTML rows that the counting script does not count as images.
3. **A fact we still do not have: the registration fee.** midrag quotes amounts. We did not find them on an official page, so they are not on ours.
4. **Facts the first run found missing, added the same evening:**
   - that working unregistered above the threshold is an offence;
   - that the registrar handles complaints and can take disciplinary steps.
5. **Our data is the open register as of 17.8.2026.** The ministry's open file has not been updated for nine weeks. Every result links to the live official record, and the page says so.

## What only this page has

- One search over all 17,874 contractors, with no captcha: name, contractor number, company number, city, branch, level, recognised.
- Every result shows what the level allows **today** on one site, plus restrictions in a red stamp, the official record, and our profile when we have one.
- **"My job":** a job type and an amount give the answer the law gives (must the contractor be registered?), the minimum level, and the contractors who can do it.
- The classification ladder: tap an amount, and the level each group needs lights up.
