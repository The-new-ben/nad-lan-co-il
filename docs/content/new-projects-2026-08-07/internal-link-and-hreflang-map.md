# Internal link, canonical and hreflang map

Updated: 2026-08-07

## Publishing principle

Every public file in this package represents a self-contained language page. It receives a self-referencing canonical. Language versions of the same topic form one reciprocal hreflang set only after every declared version is live, indexable, complete and returns HTTP 200. An unfinished or missing language URL is omitted from the set rather than published as a thin page or redirected into another language.

The Hebrew version is the default route. English, French, Russian and Arabic use the language prefix before the same topical route. The `x-default` may point to the Hebrew version unless the live site implements a genuine language selector that is a better neutral destination.

## Anchor URLs

| Language | Canonical anchor | hreflang |
|---|---|---|
| Hebrew | `/new-projects/` | `he` |
| English | `/en/new-projects/` | `en` |
| French | `/fr/new-projects/` | `fr` |
| Russian | `/ru/new-projects/` | `ru` |
| Arabic | `/ar/new-projects/` | `ar` |

Every supporting article links to the anchor in its own language within the opening section. The anchor links to a supporting guide only when that exact language version has been published and passed QA.

## Canonical topic routes

| ID | Hebrew route | Available language versions |
|---|---|---|
| 01 | `/guides/new-apartment-sale-specification/` | he, en, fr, ru, ar |
| 02 | `/guides/new-project-management-fees/` | he, en, fr, ru, ar |
| 03 | `/guides/new-project-ev-charging/` | he, en, fr, ru |
| 04 | `/guides/neighboring-development-check/` | he, en, fr, ru, ar |
| 05 | `/guides/new-apartment-acoustics/` | he, en, fr, ru |
| 06 | `/guides/residential-tower-elevators/` | he, en, fr, ru |
| 07 | `/guides/common-property-handover/` | he, en, fr, ru, ar |
| 08 | `/guides/new-project-parking/` | he, en, fr, ru |
| 09 | `/guides/residential-project-pool/` | he, en, fr, ru |
| 10 | `/guides/new-apartment-balcony/` | he, en, fr, ru, ar |
| 11 | `/guides/residential-project-wellness/` | he, en, fr, ru |
| 12 | `/guides/tower-resilience-systems/` | he, en, fr, ru, ar |
| 13 | `/guides/new-apartment-mamad/` | he, en, fr, ru, ar |
| 14 | `/guides/mixed-use-residential-project/` | he, en, fr, ru, ar |
| 15 | `/guides/new-apartment-buyer-changes/` | he, en, fr, ru, ar |
| 16 | `/guides/remote-new-apartment-handover-israel/` | he, en, fr, ru, ar |

For a foreign version, insert the language prefix before `/guides/`. For example, the English route for topic 06 is `/en/guides/residential-tower-elevators/`, and the Arabic route for topic 16 is `/ar/guides/remote-new-apartment-handover-israel/`.

## Reciprocal hreflang sets

Topics 01, 02, 04, 07, 10, 12, 13, 14, 15 and 16 use five alternates: `he`, `en`, `fr`, `ru` and `ar`, plus `x-default` if site policy uses it.

Topics 03, 05, 06, 08, 09 and 11 use four alternates: `he`, `en`, `fr` and `ru`, plus `x-default` if site policy uses it. They do not declare an Arabic alternate until a full Arabic article exists. The Arabic anchor may still link to a Hebrew or another language guide only when the link label clearly states the destination language and the content is genuinely useful. It must not present that destination as an Arabic equivalent.

## Exclusive ownership and lateral links

| ID | Exclusive decision owned here | Contextual lateral links |
|---|---|---|
| 01 | Audit of the binding sale specification, plans, versions and written promises | 04 neighboring plot, 05 acoustics, 08 parking, 10 balcony, 15 buyer changes |
| 02 | Shared operating budget, reserves and lifecycle replacement cost | 03 EV charging, 06 elevators, 09 pool, 11 wellness, 12 resilience, 14 mixed use |
| 03 | EV electrical capacity, pathways, load management, metering and operation | 02 management cost, 07 common handover, 08 parking, 12 resilience |
| 04 | Planning and permit evidence for what may be built around the selected unit | 05 acoustics, 10 balcony, existing building-rights guide |
| 05 | Apartment-specific sound paths, design evidence and verification | 01 specification, 04 neighboring plot, 06 elevators, 10 balcony, 11 wellness, 14 mixed use |
| 06 | Lift traffic, destination time, outages, emergency operation and maintenance | 02 management cost, 05 acoustics, 07 common handover, 12 resilience |
| 07 | Commissioned transfer of common systems, documents, controls and open defects | 02 management cost, 03 EV charging, 06 elevators, 08 parking, 09 pool, 11 wellness, 12 resilience, 16 remote handover |
| 08 | Parking geometry, access, mechanical systems, drainage and daily usability | 03 EV charging, 07 common handover, 12 resilience, 14 mixed use |
| 09 | Pool geometry, water treatment, indoor climate, safety, operation and evidence | 02 management cost, 07 common handover, 11 wellness, 12 resilience |
| 10 | Balcony usable geometry, sun, wind, drainage, privacy and envelope interfaces | 01 specification, 04 neighboring plot, 05 acoustics, 12 resilience |
| 11 | Gym, studio, sauna, steam room and recovery-space performance | 02 management cost, 05 acoustics, 07 common handover, 09 pool |
| 12 | Building operation during utility failures, with proof testing and resident priorities | 02 management cost, 03 EV charging, 06 elevators, 07 common handover, 08 parking, 09 pool, 13 mamad |
| 13 | Mamad usability, approved components, readiness, maintenance and prohibited interventions | 01 specification, 12 resilience, 15 buyer changes, 16 remote handover |
| 14 | Residential impact of adjacent commercial uses, including odor, loading, waste, security and allocations | 02 management cost, 05 acoustics, 08 parking, 12 resilience |
| 15 | Buyer-change freeze dates, coordination, approvals, pricing, versions and proof | 01 specification, 05 acoustics, 10 balcony, 13 mamad, protected index and delay guides |
| 16 | Remote new-apartment delivery, authority, evidence, access, account transfer and follow-up | 01 specification, 07 common handover, 13 mamad, 15 buyer changes, protected inspection and occupancy pages |

Lateral links are placed only at the exact point where the current guide reaches the boundary of another decision. A footer list of every article is not a substitute for contextual links. Each page should usually link to two to five genuinely relevant siblings, not all fifteen.

## Protected existing owners

The package does not create a new owner for these intents:

| Existing route | Intent it continues to own | What supporting articles may say |
|---|---|---|
| `/new-projects/construction-input-index/` | Construction input index, calculation and index exposure | Mention that a price or variation may be indexed, then link for the calculation |
| `/new-projects/contractor-delay-compensation/` | Delayed delivery and statutory or contractual compensation | Record the relevant delay interface, then link for the legal analysis |
| `/new-projects/presale-apartment/` | Presale and deferred-payment structures | Mention purchase stage only where it changes available evidence |
| `/investment/bank-guarantee-purchase/` | Bank accompaniment and Sale Law payment security | Ask for proof and payment instructions, then link for the protection mechanism |
| `/home-inspection/` | Full apartment inspection and defect methodology | Describe a topic-specific check, then link for the complete inspection |
| `/real-estate-lawyer/form-4-occupancy-permit/` | Occupancy approval | Treat it as a handover checkpoint and link for the legal or municipal detail |
| `/real-estate-lawyer/sale-of-apartments-law/` | Sale Apartments Law rights and remedies | Cite a relevant official source and link for broad statutory rights |
| `/property-value/building-rights-check/` | General building-rights investigation | Topic 04 owns only the selected new apartment's neighboring-development decision |
| `/property-management/` | General ongoing property management | Topic 16 owns only the transition and remote handover workflow |
| `/commercial-real-estate/commercial-property-management-fees/` | Commercial management fees | Topic 14 owns only residential allocation and interface risk in a mixed building |

Foreign-language supporting articles may link to a protected Hebrew page when no complete localized owner exists. The link label should identify that the official or detailed resource is in Hebrew. Do not create a translated URL unless a substantive localized page is being launched.

Live-route verification on 2026-08-07 found that `/en/home-inspection/` resolves to the Hebrew `/home-inspection/` page. Until a substantive English owner is launched, foreign articles should link directly to `/home-inspection/` and identify the destination as Hebrew. They must not use the redirecting English-looking path because it creates a language expectation that the live destination does not meet.

## Publishing sequence

1. Freeze all final Markdown files and run minimum-word, metadata, H1, dash, source and link checks.
2. Create the destination pages privately or in a staging environment with `noindex` and without sitemap inclusion.
3. Verify rendered language, direction, headings, tables, links, source URLs and mobile behavior.
4. Publish every version in a topic's declared hreflang set in one coordinated release.
5. Apply self-canonicals and reciprocal hreflang annotations only after all destinations return 200.
6. Add the topic pages to the correct language XML sitemap.
7. Add links from the matching language anchor and the approved sibling pages.
8. Request indexing only after the internal links, canonical and hreflang are live.
9. Inspect the rendered HTML rather than relying only on CMS fields.
10. Monitor indexing and query ownership. If the anchor begins ranking for a narrow technical query, strengthen the contextual handoff. If a supporting page begins ranking for the broad national query, narrow its title, opening and internal anchor text rather than deleting valuable depth.

## Pre-publication link QA

- No public link points to a draft, 404, redirect chain or language-mismatched anchor.
- Every supporting page has one contextual link upward to the matching language anchor.
- Every declared hreflang URL returns 200, has a self-canonical and points back to all members of the set.
- No topic 03, 05, 06, 08, 09 or 11 page declares a nonexistent Arabic alternate.
- Exact slugs match this map. Do not use alternatives such as `/guides/ev-charging-new-building/`.
- Relative internal URLs preserve the current host and avoid accidental staging domains.
- External claims link directly to the supporting government, standards-body or technical source, not to a search-result page.
- Project inventory placeholders remain `[PROJECT_LINK]` until a live catalog URL is supplied.
- A country-abroad article is never placed in these hreflang sets because it answers a different market and legal intent.
