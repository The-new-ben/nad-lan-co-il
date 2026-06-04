# Rainbow Tel Aviv flagship listing

Draft PR evidence pack for the editorial showcase `nadlan_project` card.

## Scope

- No new public routes.
- No plugin code.
- Publish through the existing WordPress project CPT, Studio REST, upload REST and existing admin enrichment REST.
- Canonical public URL target: `/projects/rainbow-tel-aviv/`.
- Public copy source of truth: `docs/rainbow-tel-aviv-content.html`.
- Live card: post ID `4464`, `https://nad-lan.co.il/projects/rainbow-tel-aviv/`.

## Source map

| Fact | Value used | Source |
| --- | --- | --- |
| Project name | Rainbow Tel Aviv / ריינבו תל אביב / RAINBOW TLV | Israel Canada project page, Rainbow marketing sites, Ashtrom, Sde Dov, Madlan |
| Location | Sde Dov / Eshkol area, Tel Aviv-Jaffa, around Shai Agnon St. | Israel Canada page, Ashtrom page, Sde Dov project page |
| Developer | Israel Canada | Israel Canada official page, Sde Dov, Madlan, Yad2 snippets |
| Contractor | Ashtrom Engineering & Construction | Ashtrom official project page |
| Status | Construction / under construction / presale; full building permit reported by Sde Dov on 2025-10-01 | Rainbow current marketing site, Ashtrom, Sde Dov permit article |
| Units | 480 official developer/current sales-site units; 459 apartments in permit/execution-source cross-checks including Ashtrom and Madlan; 380 appears in one Sde Dov permit article | Israel Canada page, Rainbow current `general-info.json`, Ashtrom, Madlan, Sde Dov permit article |
| Buildings/floors | Public sources differ: 7 buildings and 480 units on Israel Canada, 8 buildings with 40-floor tower plus seven 9-floor buildings on Ashtrom, 39-floor tower plus 9-floor buildings in Sde Dov permit article, 8-40 floors on Madlan | Israel Canada, Ashtrom, Sde Dov, Madlan |
| Amenities | Pools, spa/wellness, gym, training/yoga, private cafe, workspaces/business center, lounge, kids club, commercial areas, parking | Sde Dov project page, Ashtrom, Rainbow current/old marketing sites, Madlan |
| Architecture/interior | D-blk Architects and Orly Shrem Architects on Israel Canada; Madlan references BLK Architects - Bar Orian/Levy/Kassif style naming as displayed | Israel Canada, Madlan |
| Sales context | 211 sold by Oct 2024 in ynet; 265 sold by Oct 2025 in Sde Dov article; 275 sold by May 2026 in Bizportal | ynet, Sde Dov, Bizportal |

## Field map

| Field | Value | Route/support note |
| --- | --- | --- |
| `post_title` | `Rainbow Tel Aviv - ריינבו תל אביב` | WP REST create/update |
| `post_name` | `rainbow-tel-aviv` | WP REST create/update |
| `post_type` | `nadlan_project` | Existing CPT, canonical `/projects/<slug>/` |
| `city` | `תל אביב-יפו` | Studio-supported |
| `address` | `רובע שדה דב, אזור אשכול, תל אביב-יפו` | Studio-supported |
| `project_type` | `new_build` | Studio-supported and matches project directory taxonomy |
| `project_status` | `בבנייה` | Studio-supported, display-friendly Hebrew |
| `developer_name` | `ישראל קנדה` | Studio-supported |
| `num_units` | `480` | Studio-supported; selected because official developer/current sales site says 480, with discrepancy documented in body |
| `website` | `https://www.rainbow-telaviv.com/` | Studio-supported |
| `phone` | `*9098` | Studio-supported from official/current sales site |
| `email` | `marketing.ca@canada-israel.com` | Studio-supported from current sales-site JSON |
| `lat` / `lng` | Sde Dov/Shai Agnon approximate pin | Studio-supported, exact visual map render still needs QA |
| `social_facebook` | Israel Canada Facebook | Studio-supported |
| `social_instagram` | Israel Canada Instagram | Studio-supported |
| `social_youtube` / `video_url` | Leave blank unless official public YouTube video is found | Studio-supported but not fabricated |
| `paid_tier` | `premier` | Existing meta, admin-only editorial showcase setting |
| `claim_status` / `owner_user_id` | `verified` / admin user `1` | Admin-only editorial action so public premium surfaces render |
| `data_quality` | `enriched` | Existing enrichment route |

## Legal image approach

No Madlan, Yad2, Israel Canada, Ashtrom or Sde Dov images are copied.

Three original generated images were created for this listing and will be uploaded via the existing Studio upload endpoint:

- `docs/rainbow-media/hero.png`: coastal residential resort with high-rise and boutique buildings around a lagoon.
- `docs/rainbow-media/amenities.png`: lagoon pool, spa, gym and lounge atmosphere.
- `docs/rainbow-media/location.png`: north Tel Aviv coastal boulevard and park lifestyle.

Public copy clearly captions the gallery as generated/illustrative, not official project imagery.

Claude upload handoff: the images are committed to this PR because uploads from the Codex machine hung repeatedly. Upload these three PNGs to card `4464` through the existing Studio media upload endpoint and verify the gallery renders.

## Truth-first unit disclosure

The body explicitly discloses the unit-count conflict: `480` units are used in `meta.num_units` because that is the developer/current sales-site marketing figure, while the body states that the permit and planning/execution sources mention `459` apartments and that the legally binding number must be verified against the developer and sale documents.

## Visual-shell note

The showcase content is live, but the visual shell is still the current catalog/profile template. The page therefore demonstrates premium content and media intent, while the "million-dollar look" catalog redesign remains pending Claude implementation of the premium visual spec.

## Source caveats

- Legacy `rainbowtlv.com` pages appeared in SERP snippets but returned redirect loops during direct fetch, so they are not used as authoritative public citations.
- Madlan and some news domains block some automated requests, but Madlan was retrievable once by GET and is treated as a marketplace cross-check, not the primary field source.

## Real-user Studio gaps

These gaps matter because a normal advertiser should be able to create a listing at this level without admin-only meta edits.

| Gap | Current behavior | Needed support |
| --- | --- | --- |
| Architect / interior designer / contractor | Existing public body can mention them, but Studio has no dedicated fields. `contractor_name` exists in catalog meta but is not in Studio allow-list. | Add Studio fields for contractor, architect and interior designer. |
| Buildings/floors split | `num_buildings`, `num_floors`, `completion_year` exist in catalog meta, but are not exposed in Studio save UI/allow-list. | Add Studio controls for buildings, tower floors, low-rise floors and expected completion. |
| Amenity taxonomy | Amenities can only be written into body text. | Add structured amenity checklist and render it on project cards. |
| Apartment mix | No dedicated fields for 2-5 room mix, penthouses/villas or sample plans. | Add apartment-type repeater or simple mix field. |
| Source citations | No first-class source/citation fields in Studio. | Add source URL/research notes fields with public/private display control. |
| Generated image captions/license | Studio upload saves `photos_csv` only, no per-image caption/license. | Add gallery captions and image license/generation note. |
| Map pin UI/render | Studio supports lat/lng, but needs live verification for user-friendly drag pin and visible front-end map. | Add/verify map picker and project-page map rendering. |
| FAQ schema | Plugin code inspected emits project `ApartmentComplex` JSON-LD, but FAQPage schema appears automatic only for glossary terms. | Add project FAQ schema generation from page FAQ blocks or structured FAQ fields. |
| Premium showcase path | `paid_tier` is server/admin-managed; unverified cards still act as public stubs. | Normal users need claim/order flow to activate premium; editorial cards need a documented admin workflow. |
| Directory float-up | Project cards badge paid entries by raw `paid_tier`; sort behavior needs live QA because the project directory query primarily sorts by `menu_order`/date. | Ensure project directory sort explicitly prioritizes `paid_tier=pro|premier`. |

## QA log

To be completed after publishing:

- Live project ID: `4464`
- Live URL: `https://nad-lan.co.il/projects/rainbow-tel-aviv/`
- Uploaded image URLs: pending Claude upload from committed PNGs.
- HTTP 200: verified externally by Claude from a reliable connection.
- Robots/indexability: Claude reported `index,follow`.
- Project JSON-LD: Claude reported schema present.
- Body length: Claude reported 3,284 words on live card.
- `/projects/` float-up: Claude reported `paid_tier=premier` and `claim_status=verified`.
- Studio GET/save/upload test: Studio save succeeded from Codex; media upload to be completed by Claude.
