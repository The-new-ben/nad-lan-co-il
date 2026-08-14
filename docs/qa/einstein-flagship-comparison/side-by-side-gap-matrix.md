# Side-by-side flagship gap matrix

## 1. Live model and interaction inventory

The model statistics below come from the exact GLB URL referenced by each rendered page on 2026-08-14. Triangle totals are the sum of rendered primitive index counts divided by three. They are geometry facts, not a quality score by themselves.

| Project | Model bytes | Triangles | Meshes / nodes / materials | Visible model controls at 390 px | Main observed strength | Main observed gap |
| --- | ---: | ---: | --- | --- | --- | --- |
| H Infinity | 696,908 | 23,104 | 1 / 1 / 3 | 52 visible floor markers; every one measured 22.8 or 38 px | Full-height tower interaction, live unified map and broad project narrative | All 52 markers say direction is being checked and status needs verification; every target is below the site's 44 px standard; dense projected markers can collide |
| Rainbow | 851,668 | 15,588 | 1 / 1 / 12 | 6 visible markers, all 38 px | Small, comprehensible illustrative set with room/floor/direction labels | Still illustrative, below 44 px and not a complete verified inventory |
| Dimri Yama | 429,444 | 9,548 | 777 / 778 / 15 | 4 visible markers, 22.8 or 38 px | Rich component/node structure and compact byte size | Low interaction coverage; markers remain illustrative and below 44 px |
| Ashira | 488,188 | 10,988 | 897 / 898 / 14 | 5 visible markers, all 22.8 px | Rich component/node structure and compact byte size | Low interaction coverage; markers remain illustrative and below 44 px |
| ToHa2 | 940,000 | 31,232 | 1 / 1 / 3 | 75 visible floor markers, all 38 px | Highest live triangle count and complete commercial floor sweep | Dense floor layer, generic illustrative direction and sub-44 px targets |
| The Park | 1,173,216 | 19,488 | 1 / 1 / 3 | 44 visible floor markers, all 38 px | Complete commercial floor sweep with live context map | Dense layer, generic illustrative direction, sub-44 px targets and model above the old `<1 MB` recipe rule |
| Einstein HD | 2,420,492 | 39,912 | 13 / 13 / 10 | 3 governed concept anchors serving 4 scenes | Highest geometric detail in this set, separate named components, reviewed asset hash and low-density interaction layer | Local/private only; heavier than the fleet; flat-color viewer; anchor points are model-local illustrations, not real-world positions |
| Einstein LOD | 32,244 | 156 | 9 / 9 / 10 | Same 3 concept contracts serving 4 scenes | Distinct, extremely small constrained-data fallback | Visual sufficiency at real WordPress scale is not yet proven; 156 triangles can preserve only a coarse silhouette |

Exact Einstein HD SHA-256: `71fcca8a0f58743b5f2257684c79957fbbff8e0169f5438bdc78231f27968a53`; 79,824 vertices.
Exact Einstein LOD SHA-256: `485161974b6d343956d249d821c893b72a59678e8e8ee2810c90cee5f23079ce`; 312 vertices.

### Hotspot copy observed

| Project | Example rendered label | Decision quality |
| --- | --- | --- |
| H Infinity | `קומה 1 · כיוון בבדיקה, סטטוס לבירור` | A floor can be explored, but it does not answer availability, apartment type, area, price or verified view |
| Rainbow | `3 חדרים, קומה 8, דרום-מערב, להמחשה` | More useful for exploration, still explicitly illustrative |
| Dimri Yama | `4 חדרים, קומה 24, דרום-מערב, בעדיפות` | Adds a preference signal, but the review did not establish verified live inventory |
| Ashira | `4 חדרים, קומה 10, דרום-מערב, בעדיפות` | Adds a preference signal, but the review did not establish verified live inventory |
| ToHa2 | `קומה 1 · מערב, להמחשה` | Floor-level commercial exploration, not a specific available office |
| The Park | `קומה 1 · מערב, להמחשה` | Floor-level commercial exploration, not a specific available office |
| Einstein | Three anchors for representative interior, arrival concept and landscaped open-space concept | Every anchor is explicitly `owner_approved_illustrative_mapping`, `source_cited=false`, `decision_grade=false`, and `real_world_orientation_calibrated=false` |

Einstein intentionally improves interaction density: three separated concept anchors are easier to operate than 44-75 projected floor dots. It does not yet improve the buyer's unit decision because it has no unit truth.

## 2. Cross-cutting gap matrix

| Dimension | H Infinity / live fleet | Einstein v3 evidence | Einstein win | Residual gap and required architecture |
| --- | --- | --- | --- | --- |
| Canonical identity | Live pages are resolved by post/slug and shared engine data | `data/projects/einstein-tower.json` binds contract `einstein-tower-6885-32` to post `4867`, slug `einstein-tower`, parcel `6885/32`; Einstein 18 and Levichko aliases are unconfirmed | Strong collision protection; prevents merging Einstein 33A with Einstein 35, Einstein 19 or the separate Ashdar/Ashtrom project | Private readback must prove the exact crosswalk before any mutation; never create a second canonical |
| Source governance | Legacy engine accepts the project meta payload; claim-level source state is not consistently visible | `nadlan_flagship_v3_validate_post()` composes identity, representation, experience and buyer-decision contracts; source references render per fact | Claim/source/effective-date architecture is stronger | Source refresh and contradiction handling need a reusable maintenance job; public source chips need 44 px treatment |
| Page heading / SEO clarity | All six live pages have one H1, but it is a 1 x 1 absolutely positioned screen-reader text element | `nadlan_flagship_v3_render_for()` emits a visible page H1 and the dossier sanitizer rejects another H1 | Better visible page identity and single-owner heading | Must be proven in authenticated WordPress and checked with the theme/header; canonical, title, description, breadcrumbs and schema still need release proof |
| Mobile model space | All six live stages measured about 368 x 490.7 px at 390 px; body width did not overflow | `.nlfs__protected-stage` reserves `max(430px, 68svh)` on mobile and clips overlays; the current unchanged-input offline matrix passes all four required viewports | Directly implements the owner's “building is the jewel” rule | Prove the same geometry in real WordPress with header, cookie/WhatsApp chrome and browser safe areas |
| Model semantics | Live models range from one merged mesh to 897 meshes; quality and interaction semantics vary | Einstein has 13 named meshes/nodes and 10 materials, plus three concept contracts in scene extras | More maintainable component identity and a higher detail floor | Current viewer reads `baseColorFactor` only; no texture, animation, occlusion-aware hotspot normal or material-map rendering is proven |
| Spatial truth | Legacy floor/unit positions can be explicit or derived by fallback formula | Einstein records exact model coordinates and separate confidence fields; exact-point confidence is 0.18-0.24 in the allow-list | It distinguishes “precise coordinate in this model” from “precise location in reality” | North is an illustrative `0`; no survey/BIM crosswalk, cardinal facade, unit, room, entrance or amenity location is calibrated |
| Unit decision | Rainbow/Dimri/Ashira expose small illustrative unit sets; commercial pages expose floors; H Infinity exposes 52 generic floor rows | `nadlan_flagship_v3_validate_inventory()` requires zero units and runtime capability `inventory_selection=false` | No fake inventory, prices or availability | Cannot answer the six unit questions in the existing interior-journey contract; add a separate source-verified inventory lane later |
| Map and direction beam | Shared legacy code provides a live Mapbox map, context markers, view cone/beam and view-from-unit paths | Buyer-decision “context map” is currently rendered as current/future text cards; the View tool is schematic CSS | Current/future states and source-linked context are better organized | Add one on-demand shared map adapter with current/future layers, calibrated North, nearby facilities and the frozen legacy beam contract; do not copy map code |
| Interior and facilities | Legacy engine can lazy-load a tour, panoramas and generated first-person room geometry when its fields exist | The current offline matrix proves four selectable concept scenes, step/turn/door/light simulation and model-anchor entry | Visually teases the user and gives facilities an explicit selectable lane | It is not a 360 tour, spatial walk, official plan or facility specification; upgrade through a scene-provider interface when contractor assets arrive |
| Design tool | Not a consistent fleet-wide project-page capability | `assets/showroom/flagship-showroom-runtime.js::installDrag()` moves one illustrative sofa inside bounded percentages | A genuine playable response, not text-only | No walls, dimensions, collision rules, room library, saved option or official plan binding; label capability as a concept layout until those exist |
| Comments / OLP | Legacy lead system exists, but this comparison did not establish a visual-annotation path | Comments can add a local pin and mark a question; state becomes `prepared_no_write` | Safe demonstration without accidental external write | OLP delivery is absent. Production requires recipient, authentication, consent, privacy, retention, idempotency, durable acknowledgement and recoverable failure |
| Buyer dossier | Live pages vary; H Infinity has 12 H2 sections, while the other inspected pages have 24-37 | `nadlan_flagship_v3_render_buyer_decision()` renders facts, current/future context, sea method, education, transit, construction/views, overseas-buyer process and sources | More decision-oriented and source-granular | Live map, alternatives, verified costs, unit economics and selected-unit next action remain missing |
| Conversion path | Legacy `buyflow.js` sends selected-unit context to the existing lead endpoint; live pages have inquiry surfaces | Runtime declares `lead_submission=false`, `comment_submission=false`, `writes_enabled=false`; primary action is an in-page anchor | Correct privacy boundary for private demo | Not commercially complete. Add the existing shared lead adapter only after consent and routing gates; never create a second lead endpoint |
| Language system | Rainbow, Dimri Yama, Ashira, ToHa2 and The Park rendered six hreflang links; H Infinity rendered two | Registry allows Hebrew only; manifest says hreflang is not applicable until real siblings exist | Avoids empty/partial translated routes | Build EN/FR/RU/AR as full content and function siblings later, then emit reciprocal HE/EN/FR/RU/AR plus x-default |
| Dependency/performance posture | Legacy stage loads Google-hosted `model-viewer` and Mapbox when configured | Einstein uses a local WebGL2 viewer, same-origin GLB/image validation, HD/LOD selection for Save-Data and a 12 MB safety cap | Smaller trust boundary and deterministic asset allow-list | HD is 2.42 MB and mounts immediately; no real WordPress transfer/timing/Core Web Vitals result; the 12 MB safety cap is not a performance budget |
| Accessibility | Live model-viewer elements had no `alt` or `aria-label`; all observed live hotspot targets were below 44 px | Canvas has an aria label and keyboard controls; model anchors and major controls are 44 px; dialogs restore focus; reduced motion is present | Clear improvement in model operability and target sizing | Source-reference chips are 32 x 32; screen-reader flow, contrast and real WordPress focus order are not checked |
| Integration and rollback | Legacy renderer is already public and fleet-wide | Main `492d988` contains the shared loader/dispatcher, private-asset source contract and guarded recovery rail; public release remains false | Versioned selection protects unselected projects and the recovery design fails closed | No authenticated private WordPress clone/readback or live `1.72.206` proof exists; canonical post `4867` remains untouched until the exact release gates pass |
| Reuse | One large legacy engine handles many pages, with project-specific data and historical additions | v3 separates shared-path files from the governed Einstein package; the repository v2 recipe and merged agent skill define the target shared-engine/per-project-package/archetype architecture | The target is documented without a copied project runtime | Archetype is not executable and current JS/CSS/PHP still encode Einstein decisions, cardinalities, hooks, copy and policy; externalize the profile, forward-test a different project, and keep repository separation as a separately approved roadmap decision |

## 3. Competitor capability benchmark

This section compares observable product capabilities only. It does not claim that a feature caused traffic, ranking or conversion.

| Benchmark | Source-backed capability used in the repository research | Current fleet / Einstein gap | Architecture response |
| --- | --- | --- | --- |
| Zillow Showcase / 3D Home | Official materials connect premium media, 3D tours, interactive floor plans and exterior/context presentation | Einstein has a model and concept scenes but no plan-linked spatial tour; fleet capabilities are fragmented between model, unit and map code | One selected-entity state must connect building anchor -> unit/floor -> plan/tour -> view -> inquiry. Provider adapters can be concept, 360, Matterport or BIM without changing the page shell |
| Compass | Existing benchmark records a quiet, image-first listing hierarchy with price/status/address and core facts immediately scannable | Einstein's factual dossier is strong, but the primary model is followed by several systems before a verified product/price state exists | Keep the calm model-first layout, then surface only verified commercial facts in a compact decision rail; never fill missing fields with decorative claims |
| Yad2 new-project pages | Existing benchmark records gallery, project counts/stage, map/nearby context, unit offers and inquiry in one buyer path | Einstein has sourced project facts and concept exploration, but no unit offers or direct inquiry | Treat verified unit inventory and the existing lead adapter as a later capability module; keep the page useful in zero-inventory mode |
| Madlan project/neighborhood surfaces | Existing benchmark records concrete project facts plus neighborhood tradeoffs and alternatives | Einstein improves claim-level sourcing/current-future separation, but alternatives and live geographic exploration are not yet productized | Add a source-backed comparison/context module using the same project catalog and map data; distinguish editorial/dynamic market context from primary project evidence |
| Hagag official Einstein material | Official project page and company snapshot support name, developer, architect, building composition and construction context, but available sources use floor-counting/address language that requires reconciliation | Einstein correctly preserves the contradiction and canonical parcel; visual geometry remains illustrative | Keep identity and contradiction gates before model generation; later contractor files replace representation assets through the same hash/version registry |

Primary capability references already recorded in the repository:

- Zillow Showcase: <https://www.zillowgroup.com/news/zillow-showcase-brings-listings-to-life/>
- Zillow 3D Home: <https://www.zillow.com/marketing/3d-home/>
- Compass: <https://www.compass.com/>
- Yad2: <https://www.yad2.co.il/realestate/newprojects>
- Madlan: <https://www.madlan.co.il/projects>
- Hagag Einstein Tower: <https://www.hagag-group.co.il/projects/ResidentProjects/einstein_tower>

## 4. Priority conclusion

### P0 - required before private WordPress acceptance

1. Freeze the `1.72.206` source/package contract and rerun the full local PHP, private-asset and integration suite; local PASS still does not prove WordPress installation.
2. Create a distinct password-protected Einstein sandbox; do not modify post `4867`.
3. Round-trip every v3 meta contract and exact asset hash through authenticated WordPress readback.
4. Prove one visible H1, one demo label, one v3 root, no legacy root, no overlay on the building and exact Back restoration in WordPress.
5. Prove the four visual tools accurately describe their current capability level; do not call the schematic View a live map or the concept Interior a spatial tour.

### P1 - required before a complete public flagship

1. Add a shared, on-demand live context map adapter and integrate the frozen direction-beam behavior without changing legacy beam semantics.
2. Add a real inquiry path through the existing lead rail; retain zero-unit context when inventory is absent.
3. Bring every interactive target, including source chips, to the 44 px product standard.
4. Measure real WordPress transfer, LCP, INP, CLS and memory on representative mobile hardware; decide the HD/LOD threshold from evidence.
5. Complete private keyboard, screen-reader, contrast, RTL, safe-area and sticky-control tests.
6. Prove catalog/archive/internal-link/breadcrumb/canonical/schema behavior without creating a duplicate URL.

### P2 - upgrade when contractor material arrives

1. Replace illustrative massing and model-local mapping with source-cited survey/BIM calibration.
2. Import verified inventory, floor plans, prices, status and unit-specific views into the shared selected-entity contract.
3. Upgrade Interior to an official spatial provider and Design to a plan-aware configurator.
4. Activate comment/OLP delivery only after the full delivery/privacy contract passes.
5. Produce full HE/EN/FR/RU/AR siblings, then enable reciprocal hreflang.
