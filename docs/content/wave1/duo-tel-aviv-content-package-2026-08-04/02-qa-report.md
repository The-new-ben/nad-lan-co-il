# DUO Tel Aviv multilingual content QA

Final QA date: 5 August 2026

Research cut-off used in public copy: 4 August 2026

Scope: content-only package. No WordPress import, page edit, code change, media change, URL change or publication was performed.

## Deliverable matrix

The word count below uses a reproducible Unicode lexical-token scan from the H1 through the line before Sources. Markdown metadata and the source list are excluded.

| Language | File | Words | H1 | Required H2s | Common sources | Internal links | Alt suggestions |
|---|---|---:|---:|---:|---:|---:|---:|
| English | `duo-tel-aviv-en.md` | 7,778 | 1 | 9 | 18 | 4 | 10 |
| French | `duo-tel-aviv-fr.md` | 9,065 | 1 | 9 | 18 | 4 | 10 |
| Russian | `duo-tel-aviv-ru.md` | 7,375 | 1 | 9 | 18 | 4 | 10 |
| Arabic | `duo-tel-aviv-ar.md` | 6,534 | 1 | 9 | 18 | 4 | 10 |

All four articles exceed the 5,000-word requirement before Sources.

## Live Google intent gates

The search-intent ledger records real Google Chrome searches with `gl=il`, personalization disabled and Tel Aviv-Yafo shown by Google as the Israel location. English, French, Russian and Arabic were researched separately before drafting.

Selected title and H1 phrases:

- English: `DUO Tel Aviv apartments`.
- French: `DUO Tel Aviv appartements`.
- Russian: `купить квартиру в DUO Tel Aviv`, placed after the project-first opening.
- Arabic: `شقق جديدة للبيع في مركز تل أبيب`, placed after the project-first opening.

The first 150 words of every article contain the project, city, apartment term, price term and buying term in the target language. Each opening also states the two-tower and 668-apartment overview, the status of current public price information and the practical buying question.

## Structure and public-copy gates

All four files pass:

- One project-first H1.
- Exactly nine required H2 sections, in localized parallel order.
- No em dash or en dash character.
- No internal keyword, search-engine, QA or production commentary in the public article.
- No formulaic copied opening across languages.
- Ten image-alt suggestions nested under an H3 rather than an extra H2.
- A visible independent-site statement in the target language.
- Visible FAQ questions with answers that remain within the frozen evidence.
- No exact duplicate paragraph of 180 characters or more within an article.

## Factual consistency gates

Every language preserves the same current fact base:

- Two residential towers.
- 54 total floors and 50 residential floors in each tower.
- 668 apartments in the whole project.
- 510 apartments in the marketable pool covered by the company sales tables.
- 366 cumulative contracts and 144 not sold within that pool at 31 March 2026, clearly identified as a dated snapshot rather than current inventory.
- Nine contracts in Q1 2026.
- Q1 2026 average of NIS 64,800 per sqm excluding VAT and average apartment consideration of NIS 10.508 million including VAT, both identified as nine-contract averages rather than current offers.
- 82% financial or engineering completion reported by the developer at 31 March 2026, identified as a dated company measure rather than apartment readiness.
- Completion and the start of occupancy during 2027 only as a forward-looking corporate forecast, never a contractual handover date.
- No verified public live price list and no current apartment-by-apartment availability schedule at the research cut-off.
- No model-derived inventory, prototype unit, demo direction, borrowed interior, guaranteed view, yield, appreciation, tenant or delivery claim.

The earlier Danya capital-markets presentation URL was found to be a real 404 in Chrome. It was removed. The articles no longer use its project-specific 66% or Q3 2027 claims. S14 now points to Danya's live official Q1 2026 TASE/MAYA report, which is used only as current contractor context.

The NTA notice published on 23 July 2026 covered a defined work window on the nights of 26 to 30 July. The final articles state that this window had passed by the 4 August research cut-off. They use it as evidence of recent works and potentially changing access arrangements, not proof of an ongoing closure.

## Language and leakage gates

Character-level script scan after the final factual corrections:

| Language | Target-script letters | Other-script leakage | Mojibake | Long dashes |
|---|---:|---:|---:|---:|
| English | Latin 100% | 0 Hebrew, Arabic or Cyrillic | 0 | 0 |
| French | Latin 100% | 0 Hebrew, Arabic or Cyrillic | 0 | 0 |
| Russian | 43,800+ Cyrillic letters; remaining Latin is mainly names, URLs and standard abbreviations | 0 Hebrew or Arabic | 0 | 0 |
| Arabic | 30,100+ Arabic letters; remaining Latin is mainly brand names, addresses, URLs and abbreviations | 0 Hebrew or Cyrillic | 0 | 0 |

Arabic is written as full Arabic public copy and is ready for an RTL publishing container. Brand and project names remain in Latin where required.

## Common sources and links

All four Sources sections contain the same 18 URLs, in the exact frozen-ledger order.

Automated response check:

- S01-S14: HTTP 200.
- S17-S18: HTTP 200.
- S15-S16: raw automated request returns 403 because of Cloudflare bot protection.

Real Chrome verification for S15-S16:

- S15 opened successfully as `תחנת ארלוזורוב מערב | נת"ע - NTA` and visibly supports the underground Green Line station beneath Somail and the eastern entrance around Ibn Gabirol and Arlozorov.
- S16 opened successfully as `עבודות תשתית ברחוב ארלוזורוב, בקטע שבין רחוב רמז לרחוב אבן גבירול | נת"ע - NTA`, with visible date 23 July 2026 and the 26 to 30 July work window.

The four required internal links appear exactly once in every article and returned HTTP 200:

- Mortgage calculator.
- Purchase-tax calculator.
- New-project buying guide.
- Tel Aviv-Yafo city page.

## Independent review evidence

- `qa-en-fr-review.md`: English and French factual, structural and language audit. Final verdict PASS after the French wording and S14 correction.
- `qa-ru-review.md`: Russian factual, structural, language and near-duplicate audit. Final verdict PASS.
- `qa-ar-review.md`: Arabic factual, structural, language and cultural audit.
- `qa-four-language-parity.md`: four-language source, fact, link and formatting parity audit.

## Final article hashes

| File | SHA-256 |
|---|---|
| `duo-tel-aviv-en.md` | `39BCEB5DBB948F28F2171BE96AB5F58F8C96327828E641BE9B723ACD3508B3EC` |
| `duo-tel-aviv-fr.md` | `C5A5CFB597E6EA6080AB35A331FB3D9A0ACADFD3DF2A244C4F12E18DE45F383F` |
| `duo-tel-aviv-ru.md` | `6F49B0CDA1906D215782E716D7AB6DFEAAC2D94DD7938CC6E61A971EFEA6D7CF` |
| `duo-tel-aviv-ar.md` | `C1F3E0C6191E9C218E1E65CA8292B3F43F51C1FBCFAC6470447B0BDC4C82AFD3` |

## Isolation evidence

The live-site repository at `C:\Users\pro\nad-lan-co-il` was not edited. Its status after this content package remains the same pre-existing untracked file:

`?? scripts/qa-showroom-core-runtime.mjs`

No project page, translation page, canonical, hreflang, post field, model, media asset or shared engine file was touched.
