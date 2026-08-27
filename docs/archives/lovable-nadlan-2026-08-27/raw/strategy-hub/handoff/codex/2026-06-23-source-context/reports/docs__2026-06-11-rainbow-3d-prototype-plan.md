# Rainbow Tel Aviv / Sde Dov 3D Prototype Plan

Status: prototype artifact plus v1.59.0 plugin implementation branch.

Preview: `docs/previews/rainbow-3d-prototype.html`

Plugin branch: `codex/rainbow-3d-prototype`

Target module: `plugins/nadlan-config/inc/project-3d.php`

## Why This Exists

The live Rainbow page has a working but flat `.nlp3d` demo picker. It does not yet satisfy the owner request for a premium, high-tech, Sde-Dov-scale 3D sales experience.

Live proof checked on 2026-06-11:

- `https://nad-lan.co.il/projects/rainbow-tel-aviv/` returns 200.
- The page contains `.nlp3d` and `.nlp3d-data`.
- The page contains the public copy `תצוגת הדגמה. תוכניות הדירות המלאות יעלו בקרוב.`
- The page does not contain `.nlcmp` and does not load Mapbox on Rainbow.
- `https://nad-lan.co.il/compound/sde-dov/` returns 404 until the compound seed is reviewed/deployed and the map flag/token are enabled.

This prototype is meant to show the product direction and the v1.59.0 plugin branch wires the same interaction pattern into the existing project 3D module: a premium model-like interface, selectable floors, selectable units, and a payload shape that maps into the existing lead endpoint.

## Source Research

### Sde Dov District

Official Sde Dov FAQ states that the district is on the former Sde Dov Airport site, evacuated in 2020, with the Mediterranean Sea to the west, Profess Street to the north, Levi Eshkol Street to the east, and Shai Agnon Street to the south.

Source: [Sde Dov FAQ](https://sdedov.co.il/faq-en/)

The same FAQ states approximately 16,000 residential units are planned, with commercial areas, employment zones, public institutions, parks, a coastal promenade, and transportation infrastructure.

Source: [Sde Dov FAQ](https://sdedov.co.il/faq-en/)

The district is divided into Eshkol, Central, and Northern areas. Eshkol is the first area marketed to developers and construction has begun there.

Source: [Sde Dov FAQ](https://sdedov.co.il/faq-en/)

The FAQ describes planned public transportation around the Green Line, with stations including Profess, Nofei Yam, Einstein, and Zehava Levitov.

Source: [Sde Dov FAQ](https://sdedov.co.il/faq-en/)

The FAQ describes an architectural vision with luxury residential towers, mid-rise buildings, low-rise urban fabric, open spaces, modern facades, balconies, sea views, and tower heights ranging from 20 to 45 floors.

Source: [Sde Dov FAQ](https://sdedov.co.il/faq-en/)

### Rainbow Tel Aviv

The Sde Dov Rainbow page describes Rainbow Tel Aviv as a residential resort project facing sea and Tel Aviv skyline views. It names Israel Canada as the developer and says a building permit has been received.

Source: [Rainbow Tel Aviv on sdedov.co.il](https://sdedov.co.il/project/rainbow/)

The page lists amenities including swimming pools, spa, training/gym areas, private cafe, business area, and workspaces.

Source: [Rainbow Tel Aviv on sdedov.co.il](https://sdedov.co.il/project/rainbow/)

The page’s public-area section lists gym, spa, kids club, lounge, business meeting areas, private cafe, and swimming pools.

Source: [Rainbow Tel Aviv on sdedov.co.il](https://sdedov.co.il/project/rainbow/)

### 3D Stack Direction

Mapbox’s official 3D buildings example uses a `fill-extrusion` layer to display building heights in 3D and recommends Mapbox Standard because it includes 3D buildings by default.

Source: [Mapbox GL JS 3D buildings](https://docs.mapbox.com/mapbox-gl-js/example/3d-buildings/)

Mapbox’s official indoor extrusion example demonstrates using GeoJSON properties for `fill-extrusion-height`, `fill-extrusion-base`, and color. This is the right mental model for floor and unit extrusion once we have polygons.

Source: [Mapbox GL JS 3D extrusion floorplan](https://docs.mapbox.com/mapbox-gl-js/example/3d-extrusion-floorplan/)

Cesium’s real-estate material frames the long-term path: combine high-resolution drone data and BIM models with global 3D content, then display availability, price, and decision-support factors in a realistic 3D geospatial context.

Source: [Cesium Real Estate](https://cesium.com/industries/real-estate/)

## Prototype Behavior

The preview intentionally shows:

- premium dark blueprint + champagne visual language
- Tel Aviv coastal/district visual hints
- rotating building mass controlled by view buttons
- stack of selectable floors
- unit list per floor
- selected unit panel with rooms, sqm, direction, state
- lead payload shape for `POST /wp-json/nadlan/v1/lead`
- clear disclaimer that availability/prices are illustrative and must not be published as live inventory

The prototype intentionally does not:

- claim real unit availability
- claim real prices
- copy official Rainbow imagery
- use a stock skyline photo
- pretend the current live plugin already does this

## CMS Contract

The existing project picker already uses these fields:

- `project_3d_image`
- `project_3d_viewbox`
- `project_3d_units`
- `project_3d_demo`

The existing lead flow accepts:

- `card_id`
- `name`
- `phone`
- `email`
- `message`
- `source`
- `unit`

For Rainbow, the prototype payload keeps `card_id: 4464` and uses `source: rainbow_3d_prototype`.

Production should store unit records in `project_3d_units` with this shape:

```json
{
  "id": "R-28-A",
  "building": "tower",
  "floor": 28,
  "rooms": 4,
  "sqm": 112,
  "balcony": 14,
  "dir": "ים / צפון-מערב",
  "status": "available",
  "price": "",
  "plan": "",
  "points": "..."
}
```

`price` should remain empty unless provided by a verified owner/source. Public UI should render “לפי פנייה” rather than invented prices.

## Implementation Path

### Phase 1: Make The Current Flat Picker Premium

No Mapbox required.

- Replace the plain flat `.nlp3d` skin with the prototype visual language.
- Add a floor selector and unit state panel.
- Use current `project_3d_units` if present.
- If only `project_3d_demo=1`, render a highly polished illustrative mode with a visible demo label.
- Keep lead submission through `/nadlan/v1/lead`.
- Keep `card_id=4464` for Rainbow.

### Phase 2: Make Rainbow Data Real

- Source or owner-provide facade/elevation or clean architectural illustration.
- Trace real unit polygons into `project_3d_units`.
- Keep every unit state as unknown or inquiry-only until the owner/developer gives availability.
- Add `building`, `floor`, `line`, `view`, and `plan_url` fields.
- Add admin validation so malformed JSON cannot break the page.

### Phase 3: Compound Context

Depends on PR #145 and Mapbox token.

- Deploy v1.58.1 compound seed.
- Enable `nadlan_feature_compound_map`.
- Add `nadlan_mapbox_token`.
- Trigger admin page load so the seed runs.
- Confirm `compounds.count=1` and `compound_map.pins_count=1`.
- Confirm `/compound/sde-dov/` renders the map and a Rainbow pin.

### Phase 4: District Scale

For all Sde Dov projects:

- one `nadlan_compound` term per district area if needed: `sde-dov`, `sde-dov-eshkol`, `sde-dov-central`, `sde-dov-north`
- one `nadlan_project` per marketed project
- lat/lng on every project
- optional `project_3d_image` and `project_3d_units` per project
- later: GeoJSON/3D Tiles asset path for real BIM/drone-derived models

## Monetization And Lead Flow

The 3D experience should create paid value in four places:

- Premier showcase: a project with real 3D gets stronger visual placement.
- Lead capture: every selected unit submits `card_id`, unit ID, floor, direction, rooms, sqm.
- Advertiser proof: owner can show “unit-level leads” in Advertiser Center instead of generic inquiries.
- Upsell product: “3D interactive project model” can become a paid add-on for developers.

No success-fee or price claim should be automated from this prototype. It only captures intent.

## QA Gate Before Plugin Wiring

| Gate | Evidence Needed |
| --- | --- |
| Desktop visual | 1440px screenshot shows premium model, floor selector, unit panel, no WordPress feel |
| Mobile visual | 390px screenshot is usable, no horizontal overflow, tap targets 44px |
| Interaction | selecting a floor updates highlighted floor and unit list |
| Unit selection | selecting a unit updates lead payload |
| Demo honesty | UI visibly labels illustrative/demo data |
| Lead contract | payload includes `card_id`, `unit`, `floor`, `rooms`, `sqm`, `source` |
| Accessibility | buttons have labels/focus states; panel works by keyboard |
| Performance | preview has no heavy runtime dependency; production Mapbox loads only on compound map |
| Source safety | no copied developer photos, no stock skyline, no fake faces |
| CMS safety | malformed `project_3d_units` degrades to demo/empty state, not fatal |

## Open Gaps

- Need Claude/owner decision: should the premium project picker be upgraded inside existing `inc/project-3d.php` next, or should it wait until Cowork provides real elevation art and traced polygons?
- Need Mapbox token to show district map.
- Need PR #145 reviewed/deployed to create the Sde Dov compound relationship.
- Need real Rainbow unit/elevation data, or an owner-approved illustrative architectural drawing that is clearly labeled.
- Need screenshots from a real browser after the prototype is opened.

