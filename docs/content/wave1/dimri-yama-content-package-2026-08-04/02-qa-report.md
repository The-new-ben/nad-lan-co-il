# DIMRI YAMA multilingual content QA

Completed: 2026-08-04

Scope: content files and research evidence only. No WordPress record, live page, repository code, shared feature, URL or media item was changed.

## Deliverable matrix

| Language | File | Words from H1 to before Sources | H1 | Required H2s | Common sources | Internal links | Alt suggestions |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| English | `dimri-yama-sde-dov-en.md` | 9,665 | 1 | 9 | 16 | 4 | 10 |
| French | `dimri-yama-sde-dov-fr.md` | 10,112 | 1 | 9 | 16 | 4 | 10 |
| Russian | `dimri-yama-sde-dov-ru.md` | 8,630 | 1 | 9 | 16 | 4 | 10 |
| Arabic | `dimri-yama-sde-dov-ar.md` | 6,682 | 1 | 9 | 16 | 4 | 10 |

Word counts exclude publishing metadata and the Sources section. They use whitespace-delimited visible words and include headings.

## Search and intent gates

- The user's connected Google Chrome browser was used for separate English, French, Russian and Arabic research rounds.
- Google used Israel targeting, no personalization and the requested interface or language restriction. The footer identified Tel Aviv or Tel Aviv-Yafo from the user's IP.
- Exact queries, observed autocomplete, result titles, related searches, PAA when present and collection limitations are recorded in `01-live-google-intent-ledger.md`.
- Each language uses its selected live-Google phrase in both the SEO title and H1.
- Cultural differences affect vocabulary, sequence, examples and practical questions. They do not change the shared project facts.

## Structure and public-copy gates

- Exactly one H1 in every article.
- Exactly nine H2 sections in the required order, with Sources last.
- Every H1 starts with DIMRI YAMA and Tel Aviv in the target language.
- The first 150 words of every article contain DIMRI YAMA, Tel Aviv, apartments, price and buying in natural target-language wording.
- Every article includes one natural independent-site statement.
- Every article supplies ten native image-alt suggestions in publishing metadata.
- Arabic metadata specifies RTL; English, French and Russian specify LTR.
- No long dash characters, Hebrew-script leakage, mojibake or exact duplicate long paragraphs were found.
- No banned stock conclusion or certainty phrases were found.
- The article bodies contain no internal SEO, QA, prompt or workflow language.

## Factual consistency gates

- All four articles use one frozen fact ledger.
- All four state 458 planned apartments, four buildings, the hotel and commercial components, while keeping them distinct from residential amenities.
- The 38/39/40 and 15/16 floor-count conflict is disclosed as a counting-convention issue that must be checked in the offered building documents.
- Plot 107 and Eshkol are used as the verified planning location. The commercial address is explicitly qualified as unverified.
- The NIS 3.75 million figure appears only as a dated December 2025 launch example for a two-room apartment of about 56.5 square metres.
- The 41 cumulative contracts and 1% completion are dated to 31 March 2026 and are not presented as live inventory or current progress.
- Four related-party purchases are always described as four of nine Q1 2026 contracts, never as almost half of all project sales.
- The corporate 2031 planning year is separated from a binding apartment handover date.
- The district-wide and lot-specific PFAS disclosures are included neutrally, with no claim that the entire plot is affected or the matter is fully resolved.
- Planned district services and transport are kept in future tense and separated from services operating today.
- No demo apartment record, demo availability label or unsupported showroom price range appears as project fact.
- No current availability, guaranteed sea view, permanent view, yield, appreciation, resale period, finance approval or delivery promise is made.

## Common sources and links

- The same 16 public source URLs appear once and in the exact same order in all four Sources sections.
- Thirteen source URLs returned HTTP 200 in direct validation.
- Calcalist and two `gov.il` pages rejected the automated request with an access-control response. Each was opened successfully in the user's Chrome browser and returned the expected article or government service title and content.
- The four required internal links returned HTTP 200 during final QA:
  - https://nad-lan.co.il/mortgage-calculator/
  - https://nad-lan.co.il/purchase-tax-calculator/
  - https://nad-lan.co.il/new-projects/
  - https://nad-lan.co.il/cities/%d7%aa%d7%9c-%d7%90%d7%91%d7%99%d7%91-%d7%99%d7%a4%d7%95/

## File hashes

- `dimri-yama-sde-dov-en.md`: `9733D254BBCE2E868ACC54ECB85EA2E3D74DB95BC69E58F53D3A6C865F9CD84C`
- `dimri-yama-sde-dov-fr.md`: `4DE71723D2B328DECF8C731227FC4DC313A5001C2C6541C6523A7C94C9940710`
- `dimri-yama-sde-dov-ru.md`: `A437889AA098BCABD37EC68C2A978B3A1F54464B80A7970D4AC9CADDC9E7C912`
- `dimri-yama-sde-dov-ar.md`: `F3971F03F00EEA9EC0CE34225BC414F3923AB1F7884EE2DCCA75A2555DA8621B`

## Isolation evidence

The separate repository at `C:\Users\pro\nad-lan-co-il` remained unchanged by this work. Its status before packaging showed only the same pre-existing untracked file recorded during the ASHIRA package: `scripts/qa-showroom-core-runtime.mjs`.
