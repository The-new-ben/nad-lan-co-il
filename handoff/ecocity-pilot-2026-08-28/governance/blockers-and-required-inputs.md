# Publication blockers and required inputs

## Executive decision

The two page concepts can be built locally now, but neither page is green for publication. The project narrative and page architecture are ready; the project data, media rights and 3D geometry are not yet complete enough for a public, apartment-level sales experience.

## High-risk contradictions discovered

1. **Project status conflict:** EcoCity currently presents both projects as “in marketing” and “pre-construction / approaching execution,” with planned occupancy in 2028. The current nad-lan Bnei Dan page and project catalog use “under construction.” Until an official permit/construction update is obtained, the nad-lan status must be suppressed or changed only in a local draft to an attributed, dated formulation.
2. **Inventory without a verified feed:** the current nad-lan interface displays “8 apartments to choose” for Stricker–Brandeis and other availability-like counters. No approved inventory file or API was provided. These counters must not appear in the pilot unless EcoCity supplies a current feed with stable unit IDs, status, timestamp and owner.
3. **Unsourced prices and distances:** current nad-lan project pages contain estimated prices and exact distances to other projects. The user explicitly prohibited invented or interpolated prices and distances. The pilot must hide those modules unless each row has a source, observed date and reproducible routing/measurement method.
4. **Template contamination on EcoCity copy pages:** EcoCity’s indexed copy pages contain unrelated names and fields such as “Fable,” “Bnei Dan 20,” duplicate apartment records, `null`, sea-view claims and generic benefits. These pages are not safe for automated ingestion. Only the clean main project pages and explicitly approved project files may feed the pilot.
5. **Formal neighborhood conflict for Bnei Dan:** EcoCity marketing copy refers to the “old north,” while independent project directories classify the address in the northern part of the “new north.” Do not publish a formal neighborhood label until the municipality/GIS or EcoCity confirms the intended classification. The safe public wording is “north Tel Aviv, on Bnei Dan Street along Yarkon Park.”
6. **View permanence:** “open forever,” “unobstructed” and similar statements require a planning/legal basis. A current park-facing orientation is not a guarantee against every future obstruction. Suppress permanent-view language unless counsel and the approved sales materials clear it.
7. **Light rail tense:** the Green Line and Yehuda HaMaccabi station are future infrastructure. Never write as if the service is operating. Keep current transport and planned transport in separate UI groups with a “planned / under construction” label and a source date.
8. **3D and window-view accuracy:** an illustrative massing model cannot be called “the real project model” or “the real view from the window.” Until approved architectural geometry, surveyed coordinates, floor elevations and obstruction data are loaded, label it “interactive simulation for orientation only.”

## Developer data package required from EcoCity

### Legal and project facts

- Current official project name in Hebrew and English, and approved transliterations in French, Russian and Arabic.
- Written confirmation of the relationship, if any, between EcoCity and nad-lan.co.il and the approved independence/marketing disclosure.
- Official status, permit stage, permit/application identifiers, demolition/start status and planned delivery language that may legally be published.
- Approved building count, floor count, total unit count and project type.
- Architect, interior designer, landscape architect, contractor, lender/financial accompaniment and sales contact, only where approved for publication.
- Approved wording for parking, storage, accessibility, balconies, directions, exposures, views, specifications and shared spaces.
- Legal review of all future-infrastructure, view and delivery wording.

### Inventory contract

Provide CSV, JSON or API data with:

`project_id`, `building_id`, `unit_id`, `marketing_name`, `floor`, `rooms`, `bedrooms`, `internal_area_sqm`, `balcony_area_sqm`, `garden_area_sqm`, `exposure`, `parking`, `storage`, `accessibility`, `availability_status`, `price_ils`, `price_visibility`, `floor_plan_asset_id`, `model_mesh_id`, `last_updated_at`, `source_owner`.

Required rules:

- Stable IDs cannot be presentation labels.
- Unknown is `null`, never zero or an empty marketing phrase.
- Availability and price require `last_updated_at` and expire automatically.
- Sold/reserved/available definitions must be documented.
- No public price when `price_visibility` is not expressly public.
- A nightly stale-data alert and a manual “hide inventory” kill switch are required.

### Location and amenity data

- Approved WGS84 coordinates and survey origin for each building.
- Written approval of any claimed walking, cycling or driving times and the routing provider/mode/date.
- Approved list of neighborhood anchors; named businesses must be rechecked at preview and publication.
- School-zone claims must link to the current municipal lookup and state that registration/allocation may change.

### Media and rights

For every asset: `asset_id`, original filename, creator, owner/licensor, project, asset type, depicted space/unit, creation date, permitted channels, permitted languages, derivative/AI-edit permission, crop permission, credit line, exclusivity, expiry, source file URL and written approval reference.

Required assets:

- Exterior hero render for desktop and mobile crops.
- Street-level render from each relevant frontage.
- Approved building elevations and sections.
- Floor plans for every public unit type.
- Interior renders tied to a named unit/type, or explicitly labeled as general inspiration.
- Approved logo/brand kit.
- Site photographs with capture date.
- Video masters, transcripts, captions and poster frames.
- Approved brochure and technical specification.

No image from EcoCity, Wix CDN, Project TLV, Instagram, press or a search result may be copied into the repository without this rights record.

## Safe local work allowed now

- Build templates and component states with neutral placeholders.
- Load the canonical Hebrew copy and localized metadata/adaptation matrices.
- Implement schema rules with fields omitted by default.
- Create a disabled inventory adapter and mocked fixtures clearly stored under `fixtures/` and excluded from production builds.
- Build 3D progressive-enhancement shells and accessible text/table alternatives.
- Run local accessibility, performance, schema and content tests.

## Actions expressly forbidden

- No live WordPress edit, API write, publication, deployment, push to production, deletion or redirect.
- No scraping EcoCity inventory into production.
- No publishing prices, apartment counts, permit status, distances, dates or view guarantees not green in the fact register.
- No lead routing to EcoCity until destination, processor roles, consent text and security are approved.
- No use of third-party media without documented rights.
- No reuse of the contaminated EcoCity copy-page apartment records.

