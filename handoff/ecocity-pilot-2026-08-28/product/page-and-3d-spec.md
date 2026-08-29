# Page, media and 3D product specification

## Product outcome

Each page must answer four questions in order:

1. What is verified about this project now?
2. What would living at this address mean in practical terms?
3. Which residence or building should the buyer investigate?
4. What must be checked before providing details or making a decision?

The 3D viewer serves question 3. It is not the page, and it must never be the only route to project facts or unit selection.

## Shared page architecture

| Order | Component | Purpose | Data rule | Conversion action |
|---:|---|---|---|---|
| 1 | Independence strip | State that nad-lan is independent and show last verified date | Static approved disclosure | Open methodology |
| 2 | Hero | Identify address, developer and one defensible positioning line | Verified facts only; licensed hero or neutral placeholder | Request current information |
| 3 | Fact bar | Give 3-5 scannable facts with source/date | Every item maps to a green `fact_id` | Open “what is verified” |
| 4 | Trust drawer | Separate verified, developer claim, missing and time-sensitive fields | Render directly from fact register | View source links |
| 5 | Building selector | Choose a building or understand project massing | Stricker: two confirmed buildings; Bnei Dan: no split until plan confirmation | Select building |
| 6 | 3D/2D switcher | Explore massing, floors and orientation | 3D only after geometry gate; accessible table and elevations always available | Start exploration |
| 7 | Residence selector | Filter approved inventory | Entire module disabled without feed; no fixture data in production | Select residence |
| 8 | Unit detail | Plan, dimensions, exposure, attachments and status | All fields feed-backed with timestamp | Request this residence |
| 9 | Project story | Explain architecture and daily life | Canonical Hebrew copy plus localized adaptation | Continue to location |
| 10 | Location explorer | Streets, park, transport, education, culture, leisure and services | No hard distance without verified coordinates/method | Open route/source |
| 11 | Current vs planned transport | Prevent future infrastructure from appearing operational | Official transit source and date | Open official update |
| 12 | Buyer journey | Turn inspiration into due diligence | General information, no legal advice | Save checklist |
| 13 | FAQ | Resolve project and process objections | Answers exactly reflect visible facts | Expand question |
| 14 | Related pages | Continue within EcoCity/project/buyer cluster | Only healthy, relevant internal URLs | Open related guide |
| 15 | Lead form | Capture a qualified, transparent inquiry | Destination and consent must be approved | Submit inquiry |
| 16 | Sources and update log | Show provenance and revisions | Generated from source ledger/fact register | Open source |

## Project-specific page behavior

### Stricker 13-Brandeis 14

- The building selector is the first interactive decision. It must show “Stricker 13” and “Brandeis 14” as addresses, not “Building 1/2.”
- The comparison view may place the two approved building elevations side by side and compare only populated, source-backed fields.
- The fact bar can show “two buildings,” “26 residences in each,” “marketing / pre-construction as checked,” and “planned occupancy 2028,” after freshness validation.
- A full-floor penthouse tag appears only on unit records explicitly confirmed by the feed. The project-level story may retain the attributed general claim.
- Location storytelling centers on the transition between residential streets, Yehuda HaMaccabi, Milano Square, Yarkon Park and the planned Green Line.

### Bnei Dan 54-56

- The park relationship is the hero and orientation device. A map/diagram may place “building frontage” and “Yarkon Park,” but it cannot imply a legal view corridor.
- Do not create two building buttons merely because the address contains 54-56. Wait for approved massing/plans.
- The fact bar can show “along Yarkon Park,” “eight storeys according to EcoCity,” “marketing / pre-construction as checked,” and “planned occupancy 2028.”
- “Open frontage,” “deeper balconies” and “conventional parking” carry a visible “according to EcoCity” source treatment until unit-level confirmation.
- The view simulator defaults to an explanation state. A user chooses floor and direction only when exact floor elevations and camera locations exist.

## Location content model

Every point of interest is a data record, not prose pasted into five languages:

```json
{
  "poi_id": "stable-provider-id",
  "category": "park|transport|education|culture|leisure|health|daily-service|business|beach",
  "name": {"he-IL": "", "en": "", "fr": "", "ru": "", "ar": ""},
  "coordinates": null,
  "relationship": "adjacent|in-area|destination|planned",
  "distance_m": null,
  "walking_minutes": null,
  "source_url": "",
  "source_owner": "",
  "observed_at": "",
  "expires_at": "",
  "sponsored": false
}
```

Rules:

- `adjacent` requires verified parcel/street geometry, not marketing language alone.
- Distance requires verified project coordinates and a named measurement method. Walking time requires a route provider, mode, retrieval date and accessible route caveat where relevant.
- A planned station is always `relationship: planned` and is visually distinct.
- School proximity is not school assignment. If no official assignment record is attached, the card says “check current municipal registration.”
- A business record expires quickly and disappears safely when stale. Editorial copy must remain useful without it.
- Beach is a separate destination layer. Neither project is described as beachfront.

## Media specification

### Required asset states

1. `missing`: neutral branded placeholder; no generated imitation of the real building.
2. `supplied_unlicensed`: visible only to the internal review environment.
3. `licensed_unapproved`: held from page builds.
4. `approved`: may render in approved locales/channels according to rights metadata.
5. `expired_or_revoked`: removed from builds without deleting the audit record.

### Asset requirements

| Asset | Minimum content requirement | Accessibility | Rights requirement |
|---|---|---|---|
| Hero exterior | Correct project and frontage; desktop and mobile focal point | Descriptive alt when informative; empty alt when purely decorative | Written web, locale, crop and derivative permission |
| Street view | Capture date and direction | Caption states date and viewpoint | Photographer/owner and reuse scope |
| Floor plan | Unit/type ID, scale or dimensions, orientation, revision | HTML data table and long description | Distribution rights; no removal of required legal notes |
| Interior render | Project and unit/type association | Alt says “rendering” and names depicted room | Rendering owner and language/channel permission |
| Video | Approved project, date/version | Captions, transcript, keyboard controls, no autoplay audio | Music, voice, footage and territory rights |
| Map | Verified coordinates and provider attribution | Text address, keyboard route link | Provider terms and attribution |
| 3D model | Approved geometry and version | Equivalent selector/table; reduced-motion mode | Model ownership and derivative/web-delivery rights |

### Image delivery

- Store original master outside the web bundle; generate AVIF/WebP plus JPEG/PNG fallback as needed.
- Use responsive `srcset` and explicit dimensions to prevent layout shift.
- Do not lazy-load the LCP hero; lazy-load below-the-fold galleries in a search-friendly way.
- Keep captions and disclosure outside image pixels so they remain translatable and accessible.
- No text baked into renderings except legally required marks supplied by the rights owner.

## 3D model handoff

### Source package

Required before a project model can be called verified:

- Approved site plan, floor plans, roof plan, all elevations and key sections.
- Drawing revision/date and written statement identifying the controlling set.
- Building/parcel coordinates in WGS84 and preferably Israel TM Grid (`EPSG:2039`).
- True north, ground datum, finished-floor elevations and floor-to-floor heights.
- Balcony, setback, roof, entrance, parking-ramp and surrounding-context geometry needed for orientation.
- Stable building, floor and unit identifiers matching the inventory feed.
- Approved materials/colors only where supplied; otherwise a neutral analytic material.

### Delivery format and hierarchy

- Source model: IFC, RVT, DWG or equivalent approved design source.
- Web model: glTF 2.0 / GLB with documented compression and texture pipeline.
- Scene hierarchy: `project > building > level > unit > balcony/terrace > semantic surfaces`.
- Each selectable unit mesh maps to one `unit_id`. A merged decorative mesh cannot carry inventory status.
- Store `model_version`, `source_drawing_revision`, `generated_at`, `verified_by` and coordinate metadata in a sidecar manifest.

### Levels of detail

- `LOD0`: simple project massing and footprint for city/flight view.
- `LOD1`: verified façade rhythm, setbacks, balconies and roof silhouette for building view.
- `LOD2`: selectable floors and unit volumes for apartment selection.
- `LOD3`: optional interior shell only for units with approved plans and rights.

The application loads the smallest useful LOD first. Large textures and interior detail are never part of the initial page request.

### Geometry green gate

- Building count matches the controlling plan.
- Floor count and floor elevations match sections.
- Footprint, setbacks, balconies, roof and entrances match approved drawings within a documented tolerance chosen by the architecture team.
- North and project coordinates match the approved survey.
- Unit IDs, floors and positions reconcile 100% with the approved inventory file.
- No neighboring building, tree, skyline, sea band or landmark is invented to improve the view.
- A checker signs a visual comparison sheet for each façade and representative floor.

### View simulation

The simulator is permitted only when the following are known:

- Exact project origin and true north.
- Camera point inside the named unit, including floor elevation and eye height.
- Approved façade/window opening.
- Context geometry with source and capture date.
- Field of view and projection settings.

Every result displays:

“Interactive simulation based on model version [version], source drawings [revision] and context data checked [date]. It is not a contractual promise of view or future surroundings.”

If context is partial, show an analytic horizon/grid, not fabricated city scenery. A verified photo from a drone or mast must retain capture point, altitude, direction, lens and date.

### Performance targets for the viewer

- Viewer code is split from the main content and loads on intent or near viewport.
- Hero and core page content do not wait for WebGL.
- Initial mobile model payload target: no more than 5 MB compressed. Initial desktop target: no more than 10 MB compressed. Treat these as engineering budgets, not project facts.
- Maintain a static image/elevation fallback and a complete HTML unit table.
- Pause rendering when offscreen or the tab is hidden.
- Respect `prefers-reduced-motion`; flight and auto-rotation are off in reduced-motion mode.
- On WebGL failure, preserve all content and conversion actions.

### 3D accessibility

- All unit selection functions work by keyboard in the parallel HTML interface.
- The canvas has a concise accessible name and instructions, but complex data is not trapped in canvas-only semantics.
- A selected object updates an ARIA live status without stealing focus.
- Floor/building/unit state is reflected in the URL so it can be shared and restored.
- Color is never the only signal for availability; use text labels and patterns/icons.
- Provide reset view, zoom controls, high-contrast selection and a no-motion mode.

## Lead form and conversion

### Form sequence

1. Context: selected project, building and unit, if verified.
2. Intent: current availability, plan/spec, sales meeting, accessibility, foreign-buyer information or general question.
3. Contact: name plus one required channel; email/phone validation is locale aware.
4. Preferred language and contact time, optional.
5. Message, optional.
6. Required privacy acknowledgment and a separate optional marketing consent. Neither is preselected.
7. Plain-language destination: “Your inquiry will be sent to [approved recipient].” If no recipient is approved, store nothing and present a non-submittable prototype state.

### Form rules

- Do not make marketing consent a condition of a service inquiry unless counsel approves the exact legal basis.
- Do not put phone, email, name or free-text message in analytics events, URLs or browser storage.
- Use server-side validation, CSRF protection, rate limiting, bot protection that preserves accessibility, audit logs and an explicit retention policy.
- Localized error text must identify the field and remedy; do not rely on color.
- Success returns an inquiry reference and a copy of non-sensitive selections.
- Do not promise response time without an operational service-level agreement.

## Accessibility target

Target WCAG 2.2 AA for the complete page, including the 3D alternative, forms, maps, dialogs, cookie controls and language switcher. W3C recommends WCAG 2.2 for new and updated work: [WCAG 2.2](https://www.w3.org/TR/WCAG22/).

Minimum checks:

- One logical H1; descriptive headings and labels.
- Skip link, landmarks and consistent keyboard focus.
- Visible focus not obscured by sticky UI.
- Minimum target size and non-drag alternatives.
- Correct labels, autocomplete tokens, instructions and status messages.
- Captions/transcripts for synchronized media.
- Contrast and 200%/400% zoom without loss of content.
- Correct `lang` and `dir`; language-of-parts markup.
- Dialog focus trap and return; Escape behavior.
- No autoplay audio; reduced motion honored.
- Screen-reader and keyboard test in both LTR and RTL layouts.

