# YOO Tel Aviv - independent four-language parity audit

Audit date: 2026-08-05, Israel time  
Method: read-only comparison of the four frozen public article files against `00-source-ledger.md`  
Final verdict: **PASS**

## Release decision

No factual, source, language, structure, link or public-copy blocker remains. The first audit failed and the four articles were corrected before this final pass. The final audit was then rerun on the post-correction hashes below.

## Final article checks

| Language | H1 | Required H2s | Common sources | Total URLs | Minimum length | Conditional alts | SHA-256 |
|---|---:|---:|---:|---:|---|---:|---|
| English | 1 | 9 | 13 | 17 | Pass | 10 | `3529C4A76BE8B1977500D411E78BFF25158AAD9F04555B54C7F80226B780466A` |
| French | 1 | 9 | 13 | 17 | Pass | 10 | `1338A7C65A1737F06F62644AC252D7CF0E4F02FBD05A1E9DD59B1C44861BB622` |
| Russian | 1 | 9 | 13 | 17 | Pass | 10 | `50563900FF246857A58E7972BB0B05ACBBBEDB0B581903F35B60DFE495D7CC3D` |
| Arabic | 1 | 9 | 13 | 17 | Pass | 14 | `359B1D994C9E3509152F464E91A281E723AC9474487816F69D6EF0C04B03627A` |

The four S01-S13 source URLs are byte-identical and appear in the exact locked order. The mortgage calculator, purchase-tax calculator, new-project buying guide and Tel Aviv-Yafo city page each appear exactly once per article.

## Corrections verified in the final pass

- The English-only planning maximum of 154 units was removed. The municipal evidence remains limited to 126 existing units in the cited building and a narrow upper-floor unit-change context.
- Exact 2004 and 2005 permit dates were removed from the public articles. All four now use the same scoped timeline: original approvals and construction preceded staged occupancy in 2007, with completion described around 2009.
- The planning identifiers are aligned across all four languages: plans 1750 and 1750a, block 6108, parcels 717 and 718, lots 1 and 2, and an approximately nine-dunam historical site.
- French no longer characterizes the 2026 report as a cancelled sale. It describes a reported dispute concerning one apartment, allegations, responses and an expert view, without a project-wide or final judicial conclusion.
- French now uses the S10-S13 buyer-process sources substantively in the body: current title extract and correct sub-parcel, official purchase-tax simulator and actual buyer facts, government transaction database and comparable selection, and the distinction between a regulatory LTV ceiling and lender approval.
- The rejected old-page figure of 300 was removed from Russian and Arabic public copy.
- Arabic no longer publishes unique 75/70/50 LTV percentages. All languages retain the common principle that a regulatory ceiling is not a bank approval and a lender may offer less.
- Arabic no longer publishes the unique February/March 2004 permit detail or floors 36-37.
- Russian and Arabic production language about frozen sources, old pages, research, files and articles was replaced with direct buyer-facing wording.
- The Russian English fallback `storage` was replaced with native wording.
- The Arabic opening now refers naturally to the residential complex, not a group, and the construction-status phrasing was polished.

## Final parity findings

- Titles and H1s use the exact project-first target-language search formulas.
- Every opening satisfies the project, city, apartment, price and purchase gate and establishes completed, occupied resale status.
- Core facts match: two towers in Park Tzameret; original maximum up to 297 apartments; master 41/37 floor count; 35/39 supplier count; one municipal 40-floor/126-unit record; three underground parking levels; dated 2007 occupancy; completion around 2009; Habas and YOO Inspired by Starck context; Nissim Aloni 19 and 21 without a complete tower mapping; one dated 2023 sale; one narrow 2026 dispute; planned M1; dated school update.
- Current project-wide price, inventory, registered apartment total, management fees, facility schedule, exact coordinates, views and unit rights remain unpublished or unit-specific.
- No invented yield, appreciation, school admission, transport opening, walking time or view promise appears.
- Each language retains its intended buyer lens without changing the fact base.
- No long dash, prohibited stock phrase, internal production language, Unicode replacement character or wrong-script leakage remains.

The four article hashes in `02-qa-report.md` now match this final audit.
