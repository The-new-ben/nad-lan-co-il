# YOO Tel Aviv - final content QA report

QA date: 2026-08-05, Israel time  
Scope: four public-language article files and their shared research package  
Release type: content package only

## Outcome

The English, French, Russian and Arabic articles pass the mechanical content gates listed below. A separate independent read-only review in `qa-four-language-parity.md` records the final human comparison of factual parity, buyer-facing tone and unsupported-claim risk.

No WordPress post, live page, Hebrew field, template, source file, code file, media item, URL, canonical value or hreflang value was changed during this work.

## Article measurements

Lexical words are counted before the final Sources H2. The count includes natural-language words and excludes punctuation. Every result clears the required 5,000-word floor.

| Language | File | Lexical words | H1 | H2 | Locked sources | Total URLs | Required internal links | Long dashes | Broken replacement characters |
|---|---|---:|---:|---:|---:|---:|---|---:|---:|
| English | `yoo-tel-aviv-en.md` | 8,100 | 1 | 9 | 13 | 17 | 1 + 1 + 1 + 1 | 0 | 0 |
| French | `yoo-tel-aviv-fr.md` | 8,499 | 1 | 9 | 13 | 17 | 1 + 1 + 1 + 1 | 0 | 0 |
| Russian | `yoo-tel-aviv-ru.md` | 5,566 | 1 | 9 | 13 | 17 | 1 + 1 + 1 + 1 | 0 | 0 |
| Arabic | `yoo-tel-aviv-ar.md` | 6,563 | 1 | 9 | 13 | 17 | 1 + 1 + 1 + 1 | 0 | 0 |

The four required internal links are the mortgage calculator, purchase-tax calculator, new-project buying guide and the working Tel Aviv-Yafo city page. Each appears exactly once in every article.

## Heading and opening gates

- The H1 is the first heading in every article.
- Each H1 begins with the project name and city in the exact target-language search formula recorded in the Chrome research.
- Every article has exactly one H1.
- Every article has the nine required H2 sections in the native-language order: overview, location and surroundings, towers and apartments, prices and estimates, developer, stages, buyer fit, FAQs and Sources.
- The opening 150 words in each language name YOO and Tel Aviv and naturally cover apartments, price and purchase intent.
- The opening establishes the completed, occupied, resale-market status before detailed analysis.
- The public opening does not describe Google research, keyword selection, SEO work, editorial workflow or QA.

## Language gates

- English contains no Hebrew, Arabic or Cyrillic characters.
- French contains no Hebrew, Arabic or Cyrillic characters.
- Russian contains no Hebrew or Arabic characters.
- Arabic contains no Hebrew or Cyrillic characters.
- Arabic publication direction is explicitly `rtl` in `publishing-fields.md`.
- No article contains an em dash or en dash.
- No article contains a Unicode replacement character.
- The prohibited stock phrases and their direct target-language equivalents were not found.
- Each article states once, in native buyer-facing language, that nad-lan.co.il is an independent information site and is not affiliated with the relevant developer or seller.
- Every article contains its required native label for an estimate that is not binding.

## Source parity

All four Sources sections contain S01 through S13 as clickable Markdown links. The URL sequence is byte-for-byte identical across the four articles and matches the locked order in `00-source-ledger.md`:

1. Habas 2007 annual report hosted by the Tel Aviv Stock Exchange
2. Tel Aviv-Yafo municipal planning record from 2023
3. Official YOO Residences portfolio page
4. Alum Eshet project record
5. Ministry of Justice 2023 insolvency report
6. NTA M1 Tel Aviv page
7. Tel Aviv-Yafo municipal school update
8. Globes report of a completed 2023 transaction
9. Globes report of a 2026 dispute concerning one apartment
10. Official Land Registry extract service
11. Official purchase-tax simulator
12. Government real-estate information database
13. Bank of Israel mortgage-transparency and loan-to-value guidance

The research-only Daniela Zerrad page is not included in any public Sources section, so no language has an extra visible source.

## Locked fact gates

The four articles preserve the following distinctions:

- YOO Tel Aviv is a completed and occupied two-tower residential complex in Park Tzameret, not Sde Dov and not a beachfront project.
- Current purchase opportunities are treated as unit-specific resale offers, not an active developer inventory.
- The historical Habas filing described an original plan of up to 297 apartments, 41 and 37 above-ground floors and three underground parking levels.
- Public sources count floors differently. Alum Eshet lists 35 and 39 floors, while a 2023 municipal record describes YOO 2 at Nissim Aloni 19 as 40 floors and 126 existing units. The articles do not erase this conflict.
- Nissim Aloni 19 and 21 are publicly evidenced addresses. The complete address-to-tower mapping remains unresolved, except that the municipal record calls Nissim Aloni 19 YOO 2.
- Staged occupancy began in 2007, approximate completion is described around 2009, and the official YOO portfolio marks the original project Sold.
- Historical amenities are not converted into a promise about current operation, access rules, condition or fees.
- The June 2023 Globes transaction remains a dated example for the reported apartment: Nissim Aloni 21, 3.5 rooms, 123 square metres, floor 12 of 37, NIS 6.65 million, with three underground parking spaces and a storage room reported for that unit.
- The February 2026 Globes dispute remains a reported dispute about one apartment. Allegations, responses and an expert position are not presented as an adjudicated project-wide defect.
- The Ministry of Justice liquidation statement about Habas group structures is not treated as proof of a defect or impairment in a privately owned apartment's title.
- M1 stations are described as planned, not operating. No opening date or fixed walking time is promised.
- The school publication is described as a 2024-2025 municipal expansion update. It does not become a current catchment, capacity or admission guarantee.

## Unpublished-field discipline

The articles do not invent or infer a current project-wide apartment count, developer inventory, price list, price per square metre, management fee, registered rights, seller authority, exact coordinates, current facility schedule, school admission, fixed view, rental yield, appreciation, delivery date or financing approval.

Any current asking price, area, floor, room count, orientation, parking, storage, alteration, occupancy, view, charge or possession term is tied to the exact apartment and must be documented before an offer.

## Image-alt gate

Each language contains at least ten native-language image-alt suggestions. Every suggestion is conditional on the supplied image actually showing the described building, apartment, plan, view, parking space, storage room or facility. A generic render is not described as an actual apartment or current view.

## File hashes at article freeze

- English: `3529C4A76BE8B1977500D411E78BFF25158AAD9F04555B54C7F80226B780466A`
- French: `1338A7C65A1737F06F62644AC252D7CF0E4F02FBD05A1E9DD59B1C44861BB622`
- Russian: `50563900FF246857A58E7972BB0B05ACBBBEDB0B581903F35B60DFE495D7CC3D`
- Arabic: `359B1D994C9E3509152F464E91A281E723AC9474487816F69D6EF0C04B03627A`
- Locked source ledger: `EDA4965D816EA80E4FE6272946B01D692998E99D5211310098625D44C7270268`

If an article is edited after this report, its full structural, link, source-order, language and factual-parity checks must be rerun and the corresponding hash updated.
