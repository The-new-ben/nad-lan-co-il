# Proof after round M, 6.11.2026 (live 1.72.596 + page 121 content)

Every row of `delta.md` (government sites, ranking competitors, pre-signing tools abroad) against https://nad-lan.co.il/mortgage-calculator/
as it is live now. Evidence: release `docs/qa/project-stage-2026-09-24/deploy-result-596.json` (1032 page checks), live press
`content/press-live-m.json` + `content/shots/live-m-*` (phone 390 and desktop 1280: chips open, tools mount, converter 4.95 -> 5.06,
FAQPage 41, byline last, one h1, no horizontal scroll, no console errors), source audit 13:0x UTC (scripts + mcheck, mnomeff, mzakaut;
JSON-LD 5 -> 6), benchmark `../2026-11-05-mortgage-world/proof/` (Israel 32 lead / 34 tie / 11 lose; world 24 / 38 / 15).

Legend: **yes** = we have it now, at least as good; **by design** = left out on purpose (owner rule or not Israeli); **Ben** = his decision.

| # | Component | Before | Now | Where on the page / evidence |
|---|---|---|---|---|
| A1 | Eligibility points calculator | no | **yes** | chip "מחשבון זכאות" (`mzakaut`): 8 official profiles, siblings per applicant (zakaut.com sums them wrongly), 72/72 tests |
| A2 | Official points tables | no | **yes** | chapter "מחשבון זכאות משכנתא", 2 tables with gov.il link and 30.3.2026 |
| A3 | Basic loan by band (11 bands) | no | **yes** | same chapter, table 54,240 to 161,665 ₪; singles and olim labelled |
| A4 | Supplements (service, reserve, zones, 10 פלוס, olim, Negev) | no | **yes** | inside `mzakaut` with source and date per line; chapter list |
| A5 | Eligible-loan terms | partly | **yes** | rule in words (rate number unverified: BoI page behind a CAPTCHA), 30 years, CPI, no prepayment fee |
| A6 | Eligibility process | partly | **yes** | chapter: registration, certificate valid one year, before the purchase contract, documents, appeal |
| A7 | קו המשווה named and linked | partly | **yes** | "הממוצע החודשי של בנק ישראל" + sources + FAQ "מה זה קו המשווה" |
| A8 | Nominal to effective converter | partly | **yes** | `mnomeff` in the averages chapter (pressed live: 4.95% -> 5.06%) |
| A9 | Indexation calculator | yes | yes | /cpi-calculator/ |
| A10 | Directive 451 format and current version | partly | **yes** | link now version 22 (utld2tgp/451.pdf); `mcheck` reads the whole uniform approval |
| A11 | Directive 329 current version | partly | **yes** | version 13 (30.6.2026) cited; the s.4א rule keeps its version 12 date |
| A12 | CMA insurance calculators | partly | **yes** | links in "בדיקת משכנתא לפני חתימה", sources, mquick |
| A13 | Kol Zchut rights pages | no | **yes** | sources list |
| A14 | The 451 bank forecasts | no | partly | `mcheck` shows its own recompute and the bank's, and says which; the bond-based series itself is not public in a readable file (unverified) |
| A15 | Change vs last month | partly | **yes** | sentence under "המספרים של היום" (July to August per track) |
| A16 | gov.il life-events steps | n/a | yes | covered by `mcheck` insurance check; the page itself is 403 to every reader |
| B1 | Eligibility keywords | no | **yes** | H2 "מחשבון זכאות משכנתא: הניקוד וגובה ההלוואה ממשרד הבינוי והשיכון" + chip + FAQ |
| B2 | "בדיקת משכנתא לפני חתימה" | partly | **yes** | H2 + chip + `mcheck` |
| B3 | IRR definition | partly | **yes** | "שלושת הסלים האחידים" |
| B4 | "סל מוצע" | no | **yes** | same chapter + `mcheck` |
| B5 | Payback per shekel | partly | **yes** | 1.69 ₪ (קל״צ 4.62%) and 1.63 ₪ (system mix, 9.2026) |
| B6 | Glossary | yes | yes | /glossary/ |
| B7 | Mortgage without life insurance (PAA) | partly | **yes** | FAQ, 451 s.11, link to /mortgage-home-insurance/ |
| B8 | Mortgage registration, lien removal | partly | **Ben** | "רישום משכנתא" 1,000/mo has no owner page; a page or not is his call |
| B9 | Olim eligibility | partly | **yes** | `mzakaut` olim profiles + chapter line |
| B10 | War relief on payments | no | **Ben** | outside the calculator; no owner page |
| B11 | Purpose first | yes | yes | buyer type in every tool |
| B12 | Russian / Arabic versions | no | **Ben** | language plan |
| C1 | Bank rate band under each rate field | partly | **yes** | Mortgage 2.0 v2: lowest and highest of 7 banks, 9.2026, קו המשווה |
| C2 | Change frequency on variable tracks | partly | **yes** | 1, 2, 2.5, 5, 10 years |
| C3 | Term in months | partly | **yes** | years or months, 48 to 360 |
| C4 | Schedule menu (grace + Spitzer) | partly | yes | Spitzer, equal, balloon, bullet, grace partial or full |
| C5 | Export | partly | **yes** | CSV schedule download (UTF-8 BOM) + print + copy |
| C6 | Live rule check | yes | yes | |
| C7 | Prime shock and CPI | yes | yes | |
| C8 | Price from equity and payment | yes | yes | |
| C9 | Three scenarios side by side | partly | **yes** | היום / תחזית בנק ישראל / תרחיש מחמיר |
| C10 | Balance after 5 years, PTI per mix | yes | yes | |
| C11 | Highest payment with its time | partly | **yes** | already in v1 ("שנה 25, חודש 12"), confirmed |
| C12 | Construction index schedule | yes | yes | `mkeys` |
| C13 | Refinance break-even | yes | yes | `mexit` |
| C14 | Uniform baskets for my amount | partly | **yes** | Mortgage 2.0 v2 toggle, math equal to `mexit` |
| C15 | Eligible track filled from points | partly | partly | `mzakaut` gives the amount; the rate stays typed (rate unverified) |
| C16 | Deep links | partly | yes | hash state in every tool (no new indexable URLs, by rule) |
| C17 | Lead form with the mix | no | **by design** | no lead forms in tools (privacy rule) |
| C18 | Reader comments | no | **Ben** | never faked |
| D1 | Eligibility documents | partly | **yes** | chapter list "מסמכים לבקשה" (gov.il S2) |
| D2 | Approval checklist | partly | **yes** | `mcheck`, 28 checks |
| D3 | Final documents vs approval | no | **yes** | `mcheck` second mode |
| D4 | Bank documents by profile | yes | yes | `mready` |
| D5 | External insurance steps | no | **yes** | chapter + `mcheck` |
| D6 | Eligibility appeal | no | **yes** | chapter line + `mzakaut` process |
| D7 | Mortgage registration request | no | **Ben** | with B8 |
| D8 | Two-offer worksheet | yes | yes | `moffers` (three offers) |
| E1 | Author and reviewer | no | **yes** | "נכתב על ידי צוות נדל״ן · נבדק על ידי צוות נדל״ן" at the very end + WebPage author / reviewedBy / lastReviewed (benchmark row 56: Israel LEAD, none of 19 has one) |
| E2 | One date line | partly | **yes** | the byline line: updated 6.11.2026, BoI data to 9.2026 |
| E3 | Method and assumptions | partly | **yes** | H2 "איך המחשבון מחשב: הנחות, מה לא כלול ומקורות" |
| E4 | What is excluded | partly | **yes** | same chapter |
| E5 | Official sources with dates | yes | yes, more | +6 sources |
| E6 | Licence numbers | n/a | by design | the site never presents itself as a broker or adviser |
| E7 | Ratings | no | **Ben** | never invented |
| E8 | Contact | yes | yes | |
| E9 | Schema stack | yes | yes, more | + WebPage author / reviewedBy (Organization) |
| E10 | BoI disclaimer on bank-reported data | partly | **yes** | "שהבנקים מדווחים עליהם" under the averages |
| F1 | Field-by-field explainer of the offer | no | **yes** | `mcheck` full mode, every 451 row |
| F2 | Final document diff | no | **yes** | `mcheck` mode 2 |
| F3 | Total cost not rate | yes | yes | |
| F4 | Rate vs dated average + change | yes | yes, more | + month change |
| F5 | Three offers | partly | yes | `moffers` + `mcheck` check 11 |
| F6 | Validity date | no | **yes** | `mcheck` check 1 (24 / 12 days, countdown) |
| F7 | Risk labels (prepayment, balloon) | partly | **yes** | `mcheck` checks 16, 17 |
| F8 | Linked insurance choice | partly | **yes** | `mcheck` + chapter |
| F9 | Worst-case payment | yes | yes | |
| F10 | Consequences of non-payment | no | **yes** | `mcheck` fixed note |
| F11 | Wire-fraud warning | no | **yes** | chapter line + `mcheck` |
| F12 | Walk away, no pressure | no | **yes** | `mcheck` summary |
| F13 | Reflection period | n/a | n/a | none in Israeli law found; not claimed |
| F14 | Complaint path | no | partly | BoI public enquiries URL not verified this session |

**Count (78 rows):** 66 yes (49 of them closed today), 3 partly (A14 the bond-based forecast series is not public in a readable
file; C15 the eligibility rate is unverified; F14 the complaints URL is unverified), 6 for Ben (B8, B10, B12, C18, D7, E7), 2 by
design (C17, E6), 1 not applicable in Israel (F13).

The structural benchmark rows still lost are unchanged and known:
- speed and weight (Ben keeps Stripe, chat and Hotjar);
- phone page height;
- first input y (the content-first law puts H1, answer and CTAs first);
- payment frequency (Israeli mortgages are monthly);
- visible words on phone (chapters fold).
