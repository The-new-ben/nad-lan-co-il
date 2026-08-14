# ASHIRA multilingual content QA

Completed: 2026-08-04

Scope: content files only. No WordPress, live page, repository code, URL, media or shared system was changed.

## Deliverable matrix

| Language | File | Body words before Sources | H1 | Required H2s | Common sources | Required internal links | Alt suggestions |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| English | `ashira-sde-dov-en.md` | 9,093 | 1 | 9 | 14 | 4 present | 10 |
| French | `ashira-sde-dov-fr.md` | 9,082 | 1 | 9 | 14 | 4 present | 10 |
| Russian | `ashira-sde-dov-ru.md` | 6,777 | 1 | 9 | 14 | 4 present | 10 |
| Arabic | `ashira-sde-dov-ar.md` | 5,510 | 1 | 9 | 14 | 4 present | 10 |

Word counts exclude metadata and the Sources section and use whitespace-delimited visible words. Headings are included.

## Research gates

- Real Google Chrome used with Israel as the Google location.
- Separate English, French, Russian and Arabic search rounds completed.
- Evidence captured from live autocomplete, People Also Ask, related searches and competitor result titles.
- Exact target-language primary phrase used in each SEO title and H1, case-insensitive.
- Project facts frozen before drafting in `00-source-ledger.md`.
- Conflicts resolved uniformly across the four drafts.
- Current prices and live inventory stated as unpublished.
- Historical prices retained only as dated 2024 and 2025 reporting.

## Content gates

- Exactly one public H1 in each file.
- Exactly nine required H2 sections in the requested order, with Sources last.
- First 150 words contain the project, Tel Aviv, apartments, price and buying in the target language.
- Same 14 public source URLs in the same order across all four drafts.
- Mortgage calculator, purchase-tax calculator, new-project buyer guide and Tel Aviv city page present naturally in every article.
- Independent-site statement present in every language.
- Ten language-native image-alt suggestions supplied per language.
- No long dash character of any kind.
- No prohibited stock phrases found.
- No Hebrew-script leakage in EN, FR, RU or AR.
- Arabic marked RTL.
- No illustrative demo apartment IDs, sizes, availability labels or unsupported price-per-sqm figures.
- No current availability, guaranteed sea view, guaranteed 2030 delivery, guaranteed yield or appreciation claim.

## Link checks

The four internal links returned HTTP 200 during QA:

- https://nad-lan.co.il/mortgage-calculator/
- https://nad-lan.co.il/purchase-tax-calculator/
- https://nad-lan.co.il/new-projects/
- https://nad-lan.co.il/cities/%d7%aa%d7%9c-%d7%90%d7%91%d7%99%d7%91-%d7%99%d7%a4%d7%95/

## Isolation evidence

The separate repository at `C:\Users\pro\nad-lan-co-il` remained unchanged by this work. Its status before and after showed only the same pre-existing untracked file: `scripts/qa-showroom-core-runtime.mjs`.

