# Meier on Rothschild - four-language parity QA

Audit date: 2026-08-05  
Scope: static content parity of the EN, FR, RU and AR Markdown articles against `00-source-ledger.md`.  
Verdict: **PASS - no unresolved factual-parity or content-package release blocker in the frozen snapshot below.**

This report validates the article files, claim treatment, source identifiers and URL strings, internal-link inclusion, article structure and prohibited-claim controls. It does not test WordPress rendering, RTL page markup, canonical or hreflang output, live HTTP response codes, image files, or publication state.

Line references in this report are valid only for the hashes below.

## Frozen snapshot

| File | Bytes | Lines | SHA-256 |
|---|---:|---:|---|
| `00-source-ledger.md` | 16,741 | 138 | `83AD6C256C3CFC38B1486A12A41F8324C0D64F5358D7575FC15C47CBE9C55D06` |
| `meier-on-rothschild-en.md` | 48,710 | 429 | `8B78A79BD1CA3CA7896FEFA0C644580B390D022CF3318594E7C4379535560D45` |
| `meier-on-rothschild-fr.md` | 64,257 | 488 | `FBFB2DFE22ECAAB1E39C3359B197B442F31F857A8A211DB10B77483DACBF7DFD` |
| `meier-on-rothschild-ru.md` | 101,495 | 479 | `2CB0A7A1089426B42C86F2516F17D761C22F856A2C354EB4B17634500B1B9587` |
| `meier-on-rothschild-ar.md` | 67,812 | 498 | `55C15D8E97ABD4C842B6502C76D2BF3848C306F531BCC11ACD310B1393A60C18` |

## Automated content gates

The word measure below is a reproducible Unicode alphanumeric-token count before the Sources H2. It is intentionally conservative about Markdown formatting and is used only to confirm that every article is safely above the 5,000-word floor.

| Gate | EN | FR | RU | AR | Result |
|---|---:|---:|---:|---:|---|
| Lexical tokens before Sources | 6,923 | 9,657 | 7,072 | 6,166 | PASS |
| H1 count | 1 | 1 | 1 | 1 | PASS |
| H2 count | 9 | 9 | 9 | 9 | PASS |
| Image-alt suggestions | 10 | 10 | 10 | 10 | PASS |
| Source items | 20 | 20 | 20 | 20 | PASS |
| S01-S20 identifiers, exact order | 20 | 20 | 20 | 20 | PASS |
| Source URLs, exact ledger order | 20 | 20 | 20 | 20 | PASS |
| Required internal links, each exactly once | 4 | 4 | 4 | 4 | PASS |
| Long dash characters | 0 | 0 | 0 | 0 | PASS |
| Hebrew-script leakage | 0 | 0 | 0 | 0 | PASS |

The four internal links checked in every article are the mortgage calculator, purchase-tax calculator, new-projects guide and Tel Aviv-Yafo city page. Their article locations are EN 34, 52, 181 and 183; FR 34, 58, 232 and 236; RU 34, 60, 203 and 205; AR 59, 228, 234 and 386.

## Title, opening and article-identity gates

| Language | H1 and intent | First-150-word gate | Independent-site statement | Result |
|---|---|---|---|---|
| EN | Project first; apartments for sale, Tel Aviv, prices, resale and due diligence at line 1 | Project, city, apartments, price, buying, completed or occupied state, resale and availability status are all present naturally | Line 5 | PASS |
| FR | Project first; appartement à vendre, Tel Aviv, prix, revente and buyer checks at line 1 | Project, city, appartement, prix, achat, completed or occupied state, revente and availability status are all present naturally | Line 5 | PASS |
| RU | Project first; apartments in Tel Aviv, buying, prices and transaction checks at line 1 | Project, city, apartments, price, buying, completed or occupied state, secondary market and availability status are all present naturally | Line 5 | PASS |
| AR | Project first; apartments for sale in Tel Aviv, prices, resale and apartment checks at line 1 | Project, city, apartments, price, buying, completed or occupied state, resale and availability status are all present naturally | Line 30 | PASS |

The opening treatment is buyer-facing in all four languages. It identifies the tower as completed and occupied, distinguishes resale from a launch-stage purchase, and states that no authoritative current project-wide inventory or price list was found.

## Claim-parity matrix

| Ledger claim | EN evidence | FR evidence | RU evidence | AR evidence | Result |
|---|---|---|---|---|---|
| Identity, address and status: Meier on Rothschild; 36 Rothschild Boulevard at Allenby; Tel Aviv-Yafo; completed and occupied; not Shadal, hotel or office tower | 3, 11, 19-25 | 3, 11, 19-25 | 3, 11, 19-25 | 3, 9, 14-20, 407 | PASS |
| Floor-count conflict: architect figure 42 above ground; Hagag figures 37 over six basements and 41; no averaging; unit floor must be document-matched | 88-90 | 108-112 | 98-100 | 3, 97 | PASS |
| Height conflict: ArchDaily 154 m; architect record and January 2026 report about 158 m; published range 154-158 m; difference unresolved | 21, 82 | 13, 21, 100 | 21, 92 | 3, 17, 93 | PASS |
| Apartment-count conflict: 147 project or design figure; 100 in practice in May 2019, including six penthouses and duplexes; current legal subunit count unknown | 22, 86, 342 | 13, 22, 106, 401 | 22, 96, 392 | 3, 17, 95, 423 | PASS |
| Building metrics: 2,470 m2 footprint and 750 m2 typical net floor are building metrics, not apartment sizes | 84 | 104 | 94 | 93 | PASS |
| Date treatment: construction start 2010; ArchDaily project year 2016; CTBUH completion 2017; occupied; no invented universal handover date | 227 | 280-282 | 261-263 | 19, 304-318 | PASS |
| Uses: residential tower above retail base, with resident amenities; no hotel or office contamination | 11, 23, 82 | 11, 23 | 11, 23, 92 | 15, 93 | PASS |
| Development history: Berggruen Residential; Hagag; the Cohen brothers; historic project team is not automatically the current seller | 203-205 | 258-262 | 239-245 | 286-288 | PASS |
| Amenities and pool conflict: pool, spa, wine cellar claim; later gym, sauna, club, conference room and wine cellar report; no pool length; current rules and unit rights unknown | 106-110 | 136-140 | 118, 122-126 | 26, 133-147 | PASS |
| UNESCO White City context without a view, quiet or permanence guarantee | 50 | 62-64 | 58 | 53 | PASS |
| Allenby Red Line station: underground; R1, R2 and R3, with R2 partial; no invented walking time | 56 | 68-72 | 62-66 | 57 | PASS |
| Menora Allenby: 19 March 2025 decision; Yavne, Allenby and Yehuda Halevi area; mixed use up to 45 floors subject to limits; unit-specific effect only | 60-64 | 74-80 | 68-74 | 71-77 | PASS |
| Buyer unknowns: live inventory, project price list, unit rights, parking, storage, fees, reserve, assessments, operating rules and exact condition require current evidence | 24-26, 96-110 | 24-26, 46, 140-152 | 24-26, 106-126 | 20, 95-99, 133-151 | PASS |
| No promise of sea view, permanent outlook, quiet, appreciation, yield, current rent, liquidity, mortgage approval, tax result or current availability | 68, 147-159, 191-197, 301 | 64, 76-88, 179-198, 246-252, 358 | 58, 70-78, 157-172, 217-225 | 53, 73-83, 193-206, 251-266, 411, 467 | PASS |

No final-snapshot article states 147 or 100 as the exact current legal apartment count. No article converts the six dated price examples into a current project price range. No article treats the reported NIS 75 million asking price as a completed sale or live inventory.

## Six-price parity matrix

| Frozen example | EN | FR | RU | AR | Result |
|---|---:|---:|---:|---:|---|
| December 2024: 145 m2, floor 30, NIS 14m, about NIS 97k/m2 | 148 | 192 | 168 | 199 | PASS |
| February 2024: 196 m2, floor 7, NIS 9.5m, about NIS 48k/m2 | 149 | 193 | 169 | 200 | PASS |
| 2018 transaction reported in 2020: 434 m2, floor 38, NIS 45m, about NIS 104k/m2 | 150 | 194 | 170 | 201 | PASS |
| 2019 report: 540 m2 duplex, floors 38-39, NIS 50m, about NIS 92k/m2, about 40 m2 balconies | 151 | 195 | 171 | 202 | PASS |
| 2013 construction-period report: 395 m2 half-floor, NIS 21m, about NIS 53k/m2 | 152 | 196 | 172 | 203 | PASS |
| 26 January 2026 asking-price report: NIS 75m, about 430 m2, top two floors, one 50 m2 balcony, two 30 m2 balconies, storage, three parking spaces, and reported 2016 purchase at NIS 80m | 147 | 191 | 167 | 204 | PASS |

The Arabic article presents the January 2026 asking-price example after the five transaction examples. That editorial order differs, but the complete fact set and limitations are preserved.

## Sources, internal links, alts and estimate language

| Gate | EN | FR | RU | AR | Result |
|---|---|---|---|---|---|
| Sources H2 | 408 | 467 | 458 | 477 | PASS |
| S01-S20 list span | 410-429 | 469-488 | 460-479 | 479-498 | PASS |
| Exact source URL order | Exact | Exact | Exact | Exact | PASS |
| Ten conditional image-alt suggestions | 124-133 | 162-171 | 142-151 | 178-187 | PASS |
| Target-language estimate label | 166 | 208-210 | 188 | 222, 253, 368, 467 | PASS |

Each alt block conditions the description on an image actually showing the subject. View, pool, plan, parking and storage language is not presented as evidence of a current apartment merely because it appears in an alt suggestion.

The French estimate phrase appears in the subheading and the explanatory sentence for one model. The Arabic phrase appears on each separate buyer or investment model. These repetitions are deliberate labels, not multiple valuations. Every model remains an input checklist and does not output an invented price, tax result, mortgage approval or yield.

## Unresolved mismatches

None in the frozen snapshot identified above.

## Audit integrity

The auditor did not edit the ledger or any EN, FR, RU or AR article. The only file created by this audit is `qa-four-language-parity.md`.
