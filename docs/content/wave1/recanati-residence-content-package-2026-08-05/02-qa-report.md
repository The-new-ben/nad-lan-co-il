# RECANATI RESIDENCE - final QA report

QA date: 5 August 2026  
Result: PASS  
Scope: four public article files plus private editorial support files

## Article acceptance summary

| Language | Conservative count before Sources | H1 | H2 | Required internal links | Locked sources | Long dashes | Result |
|---|---:|---:|---:|---:|---:|---:|---|
| English | 6,812 | 1 | 9 | 4 of 4, once each | 5 of 5, ordered | 0 | PASS |
| French | 8,365 | 1 | 9 | 4 of 4, once each | 5 of 5, ordered | 0 | PASS |
| Russian | 8,396 | 1 | 9 | 4 of 4, once each | 5 of 5, ordered | 0 | PASS |
| Arabic | more than 7,800 | 1 | 9 | 4 of 4, once each | 5 of 5, ordered | 0 | PASS |

Every count excludes the final Sources section and exceeds the 5,000-word requirement.

## Title and opening gates

- Every public article begins directly with the exact H1 locked in `publishing-fields.md`. No YAML, title-field marker or internal publishing instruction precedes it.
- Project name appears first in every H1.
- English contains the live primary phrase `apartments for sale north Tel Aviv`.
- French contains the live primary phrase `appartement neuf Tel Aviv`.
- Russian contains the live primary phrase `новостройки Тель-Авив`.
- Arabic contains the live primary phrase `شقق للبيع في تل أبيب`.
- Within the opening 150 words, every version names RECANATI RESIDENCE and Tel Aviv and naturally uses its language's terms for apartments, price and buying.
- Every opening gives the same core data: 198 apartments, three completed 16-floor buildings, current immediate-occupancy/occupied context, and the need to reconfirm current price and inventory.

## Structure gates

Every article has exactly these nine H2 content roles, localized natively and in the same order:

1. Overview
2. Location and surroundings
3. Buildings and apartments
4. Prices and estimates
5. Developer
6. Project stages
7. Who it suits
8. Frequently asked questions
9. Sources

Each article contains one concise native independence statement. Calls to action ask for a current dated unit sheet, price and documents without promising availability, a discount, an appointment, a response time or representation by the developer.

## Link gates

Each article contains exactly one occurrence of each approved internal URL:

- `https://nad-lan.co.il/mortgage-calculator/`
- `https://nad-lan.co.il/purchase-tax-calculator/`
- `https://nad-lan.co.il/new-projects/`
- `https://nad-lan.co.il/cities/%D7%AA%D7%9C-%D7%90%D7%91%D7%99%D7%91-%D7%99%D7%A4%D7%95/`

Each article then contains the same five external sources in the exact locked order. No additional public URL appears. All five source URLs returned HTTP 200 in the final direct check.

The broken `/buying-apartment-from-contractor/` route, generic showroom `home.html` and `project.html` routes, Sde Dov design route and expired old Recanati mini-site were excluded.

## Factual gates

The four articles preserve the same factual contract:

- Ramat Aviv Gimel, not Neve Avivim.
- Completed demolition-and-reconstruction urban renewal.
- 198 apartments, 3 buildings, current official 16-floor description.
- Historic replacement of 96 old apartments and original allocation of 102 units for developer marketing.
- 3-5-room mix, mini-penthouses and penthouses.
- More than 15 metres between buildings and 3 underground parking levels at project level.
- Ashtrom Residences, formerly Ashdar, together with Enav.
- Canaan Shenhav Architects and Dana Oberson.
- Buildings 1 and 2 completed in March 2023; building 3 completed in June 2023.
- Current official immediate-occupancy presentation and partner description of an occupied project.

Current price, inventory, exact current entrance, apartment-specific area/floor/orientation, parking, storage, view, fees, tax, payment terms and possession date remain unverified until a current unit file is supplied.

The historic 2023 regulatory example of a 237 sqm Building C unit at NIS 14.083 million excluding VAT and NIS 59,422 per sqm excluding VAT is always dated and described as a large high-end unit. It is never presented as a current price, project average or valuation estimate.

## Language and public-copy gates

- English and French contain no Hebrew, Arabic or Cyrillic-script leakage.
- Russian contains no Hebrew or Arabic-script leakage.
- Arabic contains no Hebrew or Cyrillic-script leakage and no English fallback sentence. Latin text is limited to official brand names, project/team names, planning identifiers and URLs.
- Arabic publishing direction is locked as RTL.
- No article contains an em dash or en dash.
- No article contains internal production language about SEO, keywords, Google suggestions, PAA, QA, language intent, public-writing rules or the existing-page audit.
- Prohibited stock endings and certainty phrases were absent.
- Search phrases are integrated as buyer language rather than exposed as keyword strings.

## Independent semantic review

An independent review initially found targeted public-copy and language issues. Corrections were applied and rechecked:

- Removed self-audit and foreign-language-production wording from English.
- Recast raw search-language insertions as natural buyer questions in English and French.
- Corrected three French native constructions and removed an absolute construction-risk claim.
- Corrected the Russian history from the reversed `96 instead of 198` to replacement of 96 old apartments by 198 new apartments.
- Removed an unsupported Russian inference that mini-penthouses and penthouses are necessarily larger.
- Refined Arabic buyer phrasing, uncertainty language and service/inspection wording.
- Preserved Ashtrom Residences, Ashdar, Enav, Canaan Shenhav Architects and Dana Oberson in Latin in Arabic.

Final independent outcomes: EN/FR/RU PASS; Arabic PASS.

## Final article hashes

- EN: `87DD43CBB0597067F9DCC6445F1E917B491B96787CF4200FD47F357CE40495D1`
- FR: `22919A04992B4B0970E1A25BF005FA3FCDBEBF86BB9E9323B1D967FA489968AF`
- RU: `5456CD9569F0C0343BD9D685D4222874792B153F63B7A454266F01437A7F695C`
- AR: `EEFD334F37DE34E1F381222D8F982BB6213E89DF03CA3E77EFBBC144235A3B78`

No live page, WordPress post, code file, media asset, canonical or hreflang output was changed.

