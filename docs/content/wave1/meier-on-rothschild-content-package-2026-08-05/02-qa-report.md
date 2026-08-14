# Meier on Rothschild - final content QA

QA date: 2026-08-05

Scope: four content artifacts only, in English, French, Russian and Arabic. No WordPress page, code, media, model, URL or existing language post was edited or published.

## Release verdict

The four articles pass the final structural, language, link, factual-caveat and source-parity gates. Each article is longer than 5,000 lexical words before its Sources section, uses one H1 and the same nine H2 chapters in the required order, and contains the four required internal links exactly once. The common Sources section contains the same 20 URLs in the same byte-for-byte order in all four languages.

The final source reconciliation does not force a false single number where public records disagree. It publishes the height as a sourced 154-to-158-metre conflict and distinguishes ArchDaily's 147-apartment project figure from Globes' May 2019 description of 100 apartments in practice. The current registered condominium subunit count remains unverified. Neither count is represented as current availability.

## Final article metrics

Word counts use Unicode letter and number tokens from the H1 through the line immediately before Sources.

| File | Words before Sources | H1 | H2 | H3 | URLs | Long-dash characters |
|---|---:|---:|---:|---:|---:|---:|
| `meier-on-rothschild-en.md` | 6,923 | 1 | 9 | 59 | 24 | 0 |
| `meier-on-rothschild-fr.md` | 9,657 | 1 | 9 | 62 | 24 | 0 |
| `meier-on-rothschild-ru.md` | 7,072 | 1 | 9 | 62 | 24 | 0 |
| `meier-on-rothschild-ar.md` | 6,166 | 1 | 9 | 52 | 24 | 0 |

The 24 URLs in each article are four contextual internal links and 20 common public sources.

## SEO and opening gates

- Each H1 begins with `Meier on Rothschild` and uses the localized primary query plus Tel Aviv.
- Each opening contains the project, Tel Aviv, apartments, price and buying intent within the first 150 words.
- Each opening states that the tower is completed and occupied and that the buying decision is unit-specific resale due diligence, not a launch-stage purchase.
- No article exposes keyword research, AI-writing, prompt, QA or production language to the buyer.
- The Arabic article is native Arabic and contains no Hebrew or Cyrillic leakage. The English and French articles contain no Hebrew, Arabic or Cyrillic leakage. Russian contains no Hebrew or Arabic leakage.
- There are no em dashes, en dashes or mathematical minus characters in any article.

## Required structure and buyer utility

All four articles use the same H2 order:

1. Overview
2. Location and surroundings
3. The tower and apartments
4. Prices and estimates
5. The developer
6. Project stages
7. Who it suits
8. Frequently asked questions
9. Sources

Every language includes a native independent-site statement, at least ten image-alt suggestions, unit-level checks for title, area, floor, parking, storage, condition and management costs, and the required non-binding estimate wording. The articles distinguish asking prices from completed transactions and do not imply current availability from an old listing.

## Shared fact reconciliation

The following high-risk facts were checked across all four final articles:

- Address: 36 Rothschild Boulevard at Allenby Street, Tel Aviv-Yafo. The project is not the separate Shadal project.
- Status: completed, occupied and operating. No universal delivery promise is made.
- Use: residential tower above a retail base, with resident amenities described only at building level.
- Design: Richard Meier & Partners as principal architect; Barely Levitzky Kassif identified in the tall-building record as architect of record.
- Height: ArchDaily publishes 154 metres; the official MeierArchitects record publishes 158 metres; the reviewed sources do not explain the difference.
- Apartment counts: ArchDaily publishes 147 as a project figure; Globes reported 100 apartments in practice in May 2019; the current legal subunit count is not asserted.
- Floors: the public 42, 41 and 37-over-six-basements descriptions remain visible and are not averaged.
- Planning: the municipal decision is dated 19 March 2025; the Menora Allenby plan allows mixed use up to 45 floors subject to its conditions and aviation limits; resident objections are attributed and are not presented as proof of a unit-specific impact.
- Transport: Allenby is described as an underground Red Line station. No invented walking time is used.
- Views: the building is not described as beachfront and no apartment is promised a sea view.
- Amenities: the existence descriptions are attributed, the pool length conflict is not resolved by invention, and current access, hours, costs and unit rights remain document-specific.
- Current inventory, project-wide price list, management fee, reserves, arrears, parking, storage and exact unit rights are stated as unpublished or unit-specific where no current authoritative record was found.

## Dated price parity

The same six dated examples appear in all languages with the same status and caveats:

1. 26 January 2026 asking-price report: NIS 75 million for an atypical upper duplex of about 430 square metres, with the reported balconies, storage and three parking spaces; the report also states a 2016 purchase at NIS 80 million. It is not presented as a completed NIS 75 million sale.
2. December 2024 reported transaction: 145 square metres, floor 30, NIS 14 million, about NIS 97,000 per square metre.
3. February 2024 reported transaction: 196 square metres, floor 7, NIS 9.5 million, about NIS 48,000 per square metre.
4. Reported 2018 transaction published in 2020: 434 square metres, floor 38, NIS 45 million, about NIS 104,000 per square metre.
5. 2019 report: 540-square-metre duplex on floors 38 and 39, about 40 square metres of balconies, NIS 50 million, about NIS 92,000 per square metre.
6. 2013 construction-period report: 395-square-metre half-floor apartment, NIS 21 million, about NIS 53,000 per square metre.

No article converts these heterogeneous examples into a current price range, an appraisal, a guaranteed yield or a project minimum.

## Link and source gates

Each article contains exactly one contextual link to each required destination:

- `https://nad-lan.co.il/mortgage-calculator/`
- `https://nad-lan.co.il/purchase-tax-calculator/`
- `https://nad-lan.co.il/new-projects/`
- `https://nad-lan.co.il/cities/%d7%aa%d7%9c-%d7%90%d7%91%d7%99%d7%91-%d7%99%d7%a4%d7%95/`

The current percent-encoded city URL returns HTTP 200. Tested guessed ASCII alternatives returned 404, so this content-only package keeps the working destination rather than inventing a broken URL. A coordinated ASCII canonical and redirect, if desired, is a separate platform task.

All four Sources chapters match `00-source-ledger.md` exactly from S01 through S20. No extra external URL appears before Sources.

## Real Chrome evidence

Localized Google research in the connected Chrome browser is recorded in `01-live-google-intent-ledger.md`. Protected and high-risk source checks are recorded in `03-browser-source-verification.md`.

The final reconciliation was triggered by two pages rendered directly in Chrome:

- The official MeierArchitects page displayed `42-story 158-meter-high` in its visible Facts and Figures block.
- The Globes report dated 15 May 2019 displayed the statement that the tower had 42 floors and 100 apartments in practice, including six penthouses and duplexes.

Those checks supersede the earlier draft treatment that used 154 metres and 147 apartments without showing the later source conflict.

## Independent review history

- `qa-en-ar-source-review.md` is the pre-correction review that identified the height, apartment-count and Arabic evidence defects. Every release-blocking item in that report was corrected in the final articles and ledger.
- `qa-en-fr-review.md` is the pre-reconciliation EN-FR language review. Its only platform-level concern was the working percent-encoded city URL; no guessed 404 replacement was inserted.
- `qa-four-language-parity.md` records the independent final-snapshot parity review after the S01-S20 migration.

## Frozen final hashes

| File | SHA-256 |
|---|---|
| `00-source-ledger.md` | `83AD6C256C3CFC38B1486A12A41F8324C0D64F5358D7575FC15C47CBE9C55D06` |
| `meier-on-rothschild-en.md` | `8B78A79BD1CA3CA7896FEFA0C644580B390D022CF3318594E7C4379535560D45` |
| `meier-on-rothschild-fr.md` | `FBFB2DFE22ECAAB1E39C3359B197B442F31F857A8A211DB10B77483DACBF7DFD` |
| `meier-on-rothschild-ru.md` | `2CB0A7A1089426B42C86F2516F17D761C22F856A2C354EB4B17634500B1B9587` |
| `meier-on-rothschild-ar.md` | `55C15D8E97ABD4C842B6502C76D2BF3848C306F531BCC11ACD310B1393A60C18` |
| `qa-four-language-parity.md` | `13BE4D7D792484E4BCFC3BC04885D81E8BDF070C99A9FB84563F211BBC451294` |

## Isolation evidence

The live site repository was checked read-only after the article work. Its status still showed only the pre-existing untracked file `scripts/qa-showroom-core-runtime.mjs`. This package did not edit that file or any site file. All changes are confined to this content-package directory.
