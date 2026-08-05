# DUO Tel Aviv four-language source and parity audit

Audit date: 4 August 2026

Audit mode: read-only review of the four articles against the corrected `00-source-ledger.md`. No article was edited during this audit.

Overall result: **PASS**

Blockers: none. Two residual present-tense labels found during the first S16 rerun were corrected before this final result.

## Corrected source contract

- Frozen-ledger SHA-256: `FD5662035B48CF0348C6A7572E2BC5930D5C25278E50B28DBEE1CAFC8E2A34DD`
- Every language ends with exactly 18 source URLs in the same order as the current ledger.
- S14 is the live official Danya Q1 2026 TASE/MAYA quarterly report: `https://mayafiles.tase.co.il/rpdf/1742001-1743000/P1742403-00.pdf`.
- The former `denya-group.com/wp-content/uploads/2026/05/...` presentation URL occurs zero times across EN, FR, RU and AR.
- Project-specific Danya `66%` claims occur zero times.
- Danya Q3 2027 handover or completion claims occur zero times.
- S16 is a notice published on 23 July for works scheduled on the nights of 26-30 July. Because that window had ended before the 4 August research cut-off, it supports only recent work and potentially changing access arrangements, not an ongoing closure.

## Language-file results

| Language | Words before Sources | H1 | H2 | Sources/order | Four required internal links | Image alts | Long dashes | Wrong-script leakage | Result |
|---|---:|---:|---:|---|---|---:|---:|---:|---|
| EN | 7,778 | 1 | 9 | 18, exact | Each exactly once | 10 | 0 | 0 | PASS |
| FR | 9,065 | 1 | 9 | 18, exact | Each exactly once | 10 | 0 | 0 | PASS |
| RU | 7,375 | 1 | 9 | 18, exact | Each exactly once | 10 | 0 | 0 | PASS |
| AR | 6,534 | 1 | 9 | 18, exact | Each exactly once | 10 | 0 | 0 | PASS |

Word counts use a Unicode letter-and-number token scan from the H1 through the content immediately before the Sources H2.

## S16 timing verification

- EN line 99 correctly says the 26-30 July notice had passed by 4 August and does not prove that the same closure remained active.
- FR line 76 correctly says the period had ended and does not prove that the same closure remained in place.
- RU lines 89 and 491 correctly say the period had ended and require a fresh access check.
- AR line 103 correctly says the period had ended and does not prove that the same closure continued.
- The French general sentence now says that phases of work can affect access and requires checking notices valid on the visit date. Its H3 now refers to recent work notices rather than current works.
- The Russian H3 now asks what the recent work notice tells a buyer rather than calling the works current.

All four languages now distinguish the expired 26-30 July window from the need to recheck current access notices.

## Required fact parity

All four files preserve the same factual contract without contradiction:

- Two residential towers.
- 54 total floors in each tower, including 50 residential floors.
- 668 apartments across the whole project.
- 510 apartments in the partners' sales-reporting or marketable-rights pool, not the whole project and not current live inventory.
- 366 cumulative contracts and 144 not sold within that 510-apartment pool at 31 March 2026.
- The 144 figure is explicitly dated and not presented as current availability.
- Nine contracts in Q1 2026.
- Q1 2026 consideration of NIS 80.147 million excluding VAT.
- Q1 2026 average of NIS 64,800 per sqm excluding VAT.
- Q1 2026 average apartment consideration of NIS 10.508 million including VAT.
- Africa Israel Residences' 82% financial or engineering progress measure is tied to 31 March 2026 and its own reporting basis.
- The 82% figure is not presented as apartment readiness or an occupancy approval.
- Completion and start of occupancy during 2027 are described only as Africa Israel Residences' forward-looking corporate forecast.
- Every language separates the 2027 forecast from the contractual handover date for a selected apartment.
- Every language states that no verified current public price list or apartment-by-apartment live availability was found.
- No language treats interactive-model data as inventory, availability, a price, an approved facade or a guaranteed view.

The 2025 and Q1 2026 price figures, VAT bases and arithmetic reconciliation are consistent across EN, FR, RU and AR. Decimal punctuation changes only according to normal target-language usage.

## Internal links

Each file contains each of these URLs exactly once before Sources:

1. `https://nad-lan.co.il/mortgage-calculator/`
2. `https://nad-lan.co.il/purchase-tax-calculator/`
3. `https://nad-lan.co.il/new-projects/`
4. `https://nad-lan.co.il/cities/%d7%aa%d7%9c-%d7%90%d7%91%d7%99%d7%91-%d7%99%d7%a4%d7%95/`

## Language and formatting checks

- EN body: zero Hebrew, Arabic or Cyrillic characters detected.
- FR body: zero Hebrew, Arabic or Cyrillic characters detected.
- RU body: zero Hebrew or Arabic characters detected; Cyrillic accounts for 96.2% of body letters, with Latin retained for brands and necessary identifiers.
- AR body: zero Hebrew or Cyrillic characters detected; Arabic accounts for 97.5% of body letters, with Latin retained for brands and necessary identifiers.
- Mojibake markers detected: zero in every file.
- En dash and em dash characters detected: zero in every file.
- Every file includes exactly ten numbered image-alt suggestions.

## File hashes audited

- EN: `39BCEB5DBB948F28F2171BE96AB5F58F8C96327828E641BE9B723ACD3508B3EC`
- FR: `C5A5CFB597E6EA6080AB35A331FB3D9A0ACADFD3DF2A244C4F12E18DE45F383F`
- RU: `6F49B0CDA1906D215782E716D7AB6DFEAAC2D94DD7938CC6E61A971EFEA6D7CF`
- AR: `C1F3E0C6191E9C218E1E65CA8292B3F43F51C1FBCFAC6470447B0BDC4C82AFD3`

Final decision: **PASS - no publication blocker found in the source, fact-parity, link, script, alt-text, timing or dash gates.**
