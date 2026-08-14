# MEIER ON ROTHSCHILD - English and Arabic source QA

Review date: 2026-08-05  
Scope: `meier-on-rothschild-en.md` and `meier-on-rothschild-ar.md` only  
Authorities checked: `00-source-ledger.md` and `research-source-ledger-draft.md`  
Editing rule: neither article was edited. This report is the only file created by this review.

## Executive verdict

**Not release-clean yet.** Both articles pass the mechanical publishing gates and most factual controls, but they should not be approved until the common factual baseline is reconciled and the line-specific defects below are corrected.

The principal blockers are:

1. Both articles repeat the frozen ledger's 154-metre treatment without the later research ledger's verified 154-versus-158 source conflict.
2. Both articles present 147 apartments as the operative architectural count without explaining that 147 was the planned inventory, a later report described 100 apartments "in practice," and the current registered count was not verified.
3. Arabic adds an unverified 2007 proposal date that does not appear in either approved claim ledger and depends on a CTBUH page that the research audit could not directly inspect.
4. English and Arabic do not yet use exactly the same project facts. Several facts appear in only one language.
5. Arabic contains one unsupported non-resident financing statement and one unsupported international-demand statement.

The address, project identity, occupied status, use mix, development partnership, floor-count conflict, dated transaction figures, asking-versus-sale labels, amenities caveats, Allenby station description, Menora planning caveats, unknown-current-inventory treatment, and all source-order/link mechanics otherwise pass.

## Evidence identity and isolation

Final authoritative input hashes at report validation:

- English SHA-256: `C1D62DB74B9CE41522C621B982775B09EE20897EA3060165103AD0475D1A7FD3`
- Arabic SHA-256: `BF9B7EE86CA70B29D34DE9D8E70A9FD948309A6D7B553690986A1261576B47CB`
- Frozen ledger SHA-256: `3D67E1EE1C53F3305DD5C930FA3C255157DD3B49FC4B7B85C5CDDC1818C5AF7E`
- Research ledger SHA-256: `C19D3D9A300F1FE13F4CB26A764278D06A1CE09221D04975DE2F107B635DC130`

The Arabic article changed concurrently during the audit. The review was rerun against the hash shown above; the concurrent revision added the reported 2016 NIS 80 million acquisition to Arabic line 202 and resolved that earlier parity gap. This QA process did not edit either article. No ledger, page, code, URL, media or other package was modified by this review.

## Automated acceptance gates

Word counts use Unicode letter/number tokens from the H1 through the line immediately before Sources. URLs are excluded from the count.

| Gate | English | Arabic | Result |
|---|---:|---:|---|
| Words before Sources | 6,529 | 5,902 | Pass, both above 5,000 |
| H1 count | 1 | 1 | Pass |
| H2 count | 9 | 9 | Pass |
| Required H2 order | Overview, location, tower/apartments, prices, developer, stages, fit, FAQ, Sources | Native Arabic equivalent in the same order | Pass |
| Sources heading line | 408 | 475 | Pass |
| Source URLs | 18 | 18 | Pass |
| Exact S01-S18 URL order | Exact, case-sensitive match | Exact, case-sensitive match | Pass |
| Mortgage calculator URL occurrences | 1 | 1 | Pass |
| Purchase-tax calculator URL occurrences | 1 | 1 | Pass |
| New-project buyer-guide URL occurrences | 1 | 1 | Pass |
| Tel Aviv city-page URL occurrences | 1 | 1 | Pass |
| Long-dash code points U+2014, U+2013 and U+2212 | 0 | 0 | Pass |
| Hebrew characters | 0 | 0 | Pass |
| Arabic or Cyrillic leakage in English | 0 | Not applicable | Pass |
| Cyrillic leakage in Arabic | Not applicable | 0 | Pass |
| English fallback in Arabic | Not applicable | None found | Pass. Latin text is limited to project, company, source and route names |

The English opening paragraph contains the project, Tel Aviv, apartments, price status and purchase context. The Arabic opening paragraph does the same in native language. Each article includes an independent-site statement: English line 5 and Arabic line 30.

## Release-blocking factual corrections

### 1. Height is a direct-source conflict, not a settled 154 metres

The frozen ledger says 154 metres, but the later research ledger corrects that treatment: the official MeierArchitects page publishes 158 metres, while ArchDaily and Dezeen publish 154 metres. The articles must preserve this conflict and must not call the 154-metre entry "architect-published" without identifying the actual publication.

English phrases requiring correction:

- Line 21: `154 metres in the architect-published technical data`
- Line 82: `The architect-published record describes a 154-metre residential tower`

Arabic phrases requiring correction:

- Line 3: `وارتفاعا قدره 154 مترا`
- Line 17: `وارتفاعا يبلغ 154 مترا`
- Line 93: `تنشر المادة التقنية ارتفاعا يبلغ 154 مترا`
- Line 312: `وارتفاع 154 مترا`

Required factual treatment: ArchDaily and Dezeen publish 154 metres; the architect's own project page publishes 158 metres; the difference remains unresolved. Do not choose one as an exact universal height.

### 2. 147 is planned inventory, not a safe current apartment count

The research ledger establishes that 147 was the planned total in the 2012 marketing material and 2013 audited filing, with 112 reported sold at 2013 year-end. A May 2019 report described 100 apartments "in practice." The current legal condominium/subunit count was not verified. Both drafts currently preserve the older frozen-ledger formulation and omit this material distinction.

English phrases requiring correction:

- Line 22: `147 apartments in the architect-published specification`
- Line 86: `The same architectural specification publishes 147 apartments. That is the supported design count used here`
- Line 342: `The architect-published technical specification gives 147 apartments`

Arabic phrases requiring correction:

- Line 3: `147 شقة`
- Line 17: `147 شقة`
- Line 93: `و147 شقة`
- Line 312: `و147 شقة`
- Line 421: `تنشر ArchDaily ... 147 شقة` followed by `لا نستخدمها لتغيير المواصفة المنشورة`

Required factual treatment: 147 planned apartments; later reporting described 100 apartments in practice; the current registered subunit count is not published in the reviewed evidence. Neither figure should be represented as the exact current count.

### 3. Arabic adds an unsupported 2007 proposal date

Arabic line 302 says: `يسجل The Skyscraper Center اقتراح المشروع في 2007`.

Neither claim ledger approves a 2007 proposal date. The research ledger expressly records that the CTBUH page returned a security challenge and warns that a CTBUH-only claim should be independently confirmed. The English article does not use 2007. Remove the date or add primary evidence to the common ledger before using it in any language.

Arabic line 312 also calls the ArchDaily 2016 entry `نشر معماري نهائي`, meaning a final architectural publication. ArchDaily lists 2016 as the project year; it does not establish that phrase as a factual completion milestone. The safe chronology is: occupied by the time of the current Hagag classification; occupancy had begun by March 2016 in the later research evidence; architecture publications documented completion/opening in September 2017. If the frozen S01-S18 source set remains controlling, describe only the source differences it can support.

### 4. Arabic makes an unsupported non-resident financing claim

Arabic line 230 says: `قد يطلب البنك من مشتري غير مقيم رأسمالا أكبر`.

The Bank of Israel source and frozen ledger establish category-based LTV limits and lender-specific underwriting. They do not establish a project-wide or universal rule that a non-resident will be required to provide more equity. English correctly says approval and terms remain lender-specific. Arabic should use the same neutral treatment unless a common, authoritative non-resident lending source is added to every language's evidence set.

### 5. Arabic asserts international demand without evidence

Arabic line 364 says: `قد ينجذب المستثمر إلى ندرة العنوان والطلب الدولي`.

No source in either ledger establishes current international demand or quantifies scarcity. This sentence can be reframed as a buyer hypothesis to test, not a market fact. English line 289 uses the safer formulation that the project `may interest an investor` and immediately requires unit-level underwriting.

## Cross-language factual parity gaps

These are not all contradictions, but they violate the requirement that the language products carry the same project facts. Resolve each gap by either adding the fact to both languages with the same caveat or removing it from the language-only version.

| Fact present in only one draft | Exact location | Parity action |
|---|---|---|
| 2,470 sq m ground footprint | English line 84 | Add to Arabic with the same design-metric caveat, or remove from English |
| Residents filed objections to Menora Allenby | Arabic line 73 | Add to English with S15 attribution, or remove from Arabic; do not turn the objection into proof of impact |
| 19 March 2025 date of the municipal planning decision | English line 62; Arabic body omits it | Add the date to the Arabic planning discussion or remove it from the English body; it already appears in Arabic source label S09 |
| Historical unit combinations/change in luxury units | Arabic line 97 | Add to English only if supported from the common source set, or remove; the strongest support currently sits in the supplemental research rather than frozen S01-S18 |
| `Semi-Olympic` wording from the January 2026 report | Arabic lines 26 and 131 | English lines 106-108 deliberately avoid the label. Keep both languages at `resident pool` with the same public-description conflict, or quote the term in both with attribution |
| 2007 proposal date | Arabic line 302 | Remove unless independently verified and added to the common ledger; this is also a factual blocker |

The following central facts are already aligned across English and Arabic: 36 Rothschild Boulevard at Allenby; completed and occupied residential tower over a retail base; not SHADAL; Richard Meier & Partners and BLK roles; Berggruen Residential plus the Hagag-Cohen partnership history; 42/41/37 floor-source conflict; no current official inventory or price list; the same five dated sale examples; the retrospective reported 2016 NIS 80 million acquisition; the January 2026 NIS 75 million figure as an asking price; no guaranteed sea view; unit-specific parking/storage rights; Allenby Red Line station; and the Menora plan's potential, not predetermined, apartment-specific impact.

## Numerical, date and transaction audit

### Clean numerical claims

Subject to the height and unit-count corrections above, the following numerical claims match the frozen ledger and the later research evidence:

- Address 36 Rothschild Boulevard: English lines 3, 11, 19 and 322; Arabic lines 14, 51 and 405.
- 42 above-ground floors versus Hagag's 37 over six basement levels and another 41-floor company description: English lines 88-90; Arabic lines 17-18, 93-95 and 415-417. Both keep the conflict visible and do not average it.
- ArchDaily's 2,470 sq m footprint and 750 sq m typical net floor metric: English line 84. Arabic includes only the 750 sq m metric at line 93. Both correctly state that these are building/floor metrics, not apartment areas.
- NTA's R1, R2 and R3 patterns, with R2 described as partial: English lines 56 and 390; Arabic line 57. No walking time is invented.
- Menora Allenby planning area and up-to-45-floor mixed-use allowance, subject to planning and aviation limits: English line 62; Arabic lines 73, 338 and 453.
- All five sale examples, the retrospective reported 2016 acquisition and the January 2026 asking-price example use the same dates, floors, areas and amounts in the two drafts: English lines 147-152; Arabic lines 197-202.

### Asking price versus completed sale

This gate passes in both articles.

- English line 147 labels NIS 75 million as a 26 January 2026 asking-price report and says it does not prove a sale or continued availability.
- Arabic line 202 says `هذا سعر مطلوب ... وليس صفقة منجزة` and says later availability is unknown.
- English FAQ line 338 and Arabic FAQ line 429 repeat the distinction correctly.
- The 2024, 2020/2018, 2019 and 2013 examples are all described as dated reported transactions, not current project prices.

The January 2026 Globes language editions conflict on terrace totals. The controlling English S14 describes one 50 sq m balcony and two 30 sq m balconies; the Hebrew version can be read as the two additional terraces totalling about 30 sq m. English line 147 and Arabic line 202 list the English-source components and do not calculate a total, which is the safest treatment under the frozen source order.

## Address, identity, developer and status audit

This gate passes.

- Neither article calls MEIER `Shadal Tower` or places it at Shadal Street.
- Both identify 36 Rothschild Boulevard at Allenby in Tel Aviv-Yafo.
- Both describe residential use over a retail/commercial base and explicitly reject the SHADAL hotel/office contamination.
- Both identify Richard Meier & Partners as principal designer and BLK/Barely Levitzky Kassif as architect of record.
- English lines 203-209 and Arabic lines 284-286 preserve Berggruen Residential, Hagag Group and the Cohen partners instead of presenting Hagag as the sole developer, owner or current seller.
- Both describe the tower as completed and occupied and avoid a universal contractual delivery date.

## Amenities and unit-rights audit

This gate passes with one parity adjustment noted above.

- English lines 106-110 and Arabic lines 26, 131-145 attribute the pool, spa, gym, sauna, residents' club, meeting room and wine-cellar descriptions to developer or dated news sources.
- Neither article promises present opening hours, staffing, service level or inclusion in a unit's rights.
- Neither article calls the pool definitively Olympic-size.
- Both require current management rules, invoices, budget, arrears, reserves and special-assessment information.
- Both treat parking, storage and wine-cellar rights as apartment-specific and require registration/plan/contract verification.

## Transport and planning audit

This gate passes apart from the parity gaps already listed.

- Allenby is accurately described as an underground Red Line station. Neither draft invents a walking time.
- The municipal Menora Allenby area is correctly placed between Yavne, Allenby and Yehuda Halevi streets.
- Both state that the plan can allow mixed-use construction up to 45 floors subject to its conditions and limits.
- Both reject any automatic conclusion about one apartment's light, view, noise or access and require floor-, direction- and unit-specific analysis.
- Neither article promises permanent open views or a fixed completion timetable for nearby works.

## Unknowns and prohibited-promise audit

This gate passes.

Both articles preserve the required unknowns:

- No authoritative current project-wide inventory.
- No current official project-wide price list.
- No confirmed current status of the January 2026 private listing.
- No current public unit-level management charge, reserve or arrears record.
- No unit-specific legal proof of area, floor, parking, storage, wine cellar or view.
- No current official amenity hours, access rules or service level.
- No guaranteed rent, yield, appreciation, liquidity, mortgage approval, tax outcome, quiet or sea view.

Both use explicit non-binding estimate language: English line 166; Arabic lines 220, 251, 366 and 465. Search hits for `guarantee`, `yield`, `مضمون`, `ضمان` and `عائدية` were all cautions or negations, not promises. No scarcity statement, `prices start at` statement, delivery promise, Shadal contamination, 565 sq m penthouse claim, 40-floor claim or demo-model fact appears.

## Additional editorial/source cautions

These are lower priority than the release blockers, but should be repaired during the same editorial pass:

1. Arabic line 360 says `لكن العقد العبري والمستندات الرسمية هي التي يجب شرحها بدقة`. The controlling instrument is the signed agreement and applicable official documents, not automatically a Hebrew-language contract. Use transaction-specific wording and let counsel identify which text controls.
2. Arabic line 473 says `المقال الجديد يصحح العنوان والاستعمال`. This exposes internal editorial process to the buyer. A public-facing answer can simply say that the nad-lan page is a starting point and that external sources plus unit documents control.
3. English line 82 and Arabic line 93 describe the ArchDaily-style data as if it came directly from the architect's own technical page. Identify the publication precisely because the official architect page is the source of the conflicting 158-metre value.
4. CTBUH S06 was inaccessible behind a security challenge in the later research audit. Claims that also have ArchDaily, Hagag, TASE or completion-publication support can remain attributed to those accessible sources. A CTBUH-only fact should not be added.

## Final acceptance checklist

| Requirement | Status |
|---|---|
| 5,000 words before Sources | Pass EN and AR |
| One H1 | Pass EN and AR |
| Nine H2 sections in required order | Pass EN and AR |
| Exact S01-S18 URLs in exact order | Pass EN and AR |
| Four required internal links exactly once | Pass EN and AR |
| Long-dash ban | Pass EN and AR |
| Script leakage | Pass EN and AR |
| Address and MEIER/SHADAL separation | Pass EN and AR |
| Developer/ownership nuance | Pass EN and AR |
| Asking-versus-sale labeling | Pass EN and AR |
| Unknown current inventory and price | Pass EN and AR |
| Amenities and unit-specific rights caveats | Pass EN and AR |
| Transport and planning caveats | Pass EN and AR |
| Height reconciliation | **Fail EN and AR** |
| Planned versus current apartment-count treatment | **Fail EN and AR** |
| No unsupported timeline facts | Pass EN; **fail AR at line 302** |
| High-stakes financing wording | Pass EN; **fail AR at line 230** |
| Cross-language factual parity | **Fail until the listed gaps are resolved** |

Approval can be reconsidered after the common ledger is reconciled and the listed article lines are revised. No other factual defect was found in the reviewed numerical, date, address, developer, amenity, transport, planning, price-labeling, source-order, promise or language-leakage gates.
