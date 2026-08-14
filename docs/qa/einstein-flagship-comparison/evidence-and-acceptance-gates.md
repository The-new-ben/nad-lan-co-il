# Evidence ledger and acceptance gates

## 1. Exact repository evidence

Use `file :: symbol` as the stable citation. Line numbers may move while the branch is active.

| Evidence | Exact file / symbol | What it proves |
| --- | --- | --- |
| Canonical entity and unconfirmed aliases | `data/projects/einstein-tower.json :: identity`, `location`, `building_form`, `units`, `db_meta` | Post `4867`, slug `einstein-tower`, parcel `6885/32`, 215 total units, three buildings, zero supplied inventory, Hebrew-only and `ready_for_page=false` |
| Identity regression | `scripts/qa-einstein-project-identity.mjs` | In-place slug/post, parcel/building/unit totals, zero inventory, distinct related Einstein projects and catalog row reconcile |
| Contract allow-list | `plugins/nadlan-config/assets/flagship-v3/contracts/registry.json :: contracts[project_contract_id=einstein-tower-6885-32]` | Public release off, Hebrew only, exact model/poster hashes, three mapping groups, owner decisions and future source-cited lane |
| Contract validation | `plugins/nadlan-config/inc/flagship-surface.php :: nadlan_flagship_v3_validate_post()` | One fail-closed composition point for identity, inventory, representations, visual tools, experiences and buyer-decision data |
| Zero inventory | `plugins/nadlan-config/inc/flagship-surface.php :: nadlan_flagship_v3_validate_inventory()` | Nonempty `project_3d_units` is rejected for the current Einstein contract |
| Asset identity | `plugins/nadlan-config/inc/flagship-surface.php :: nadlan_flagship_v3_validate_representations()` | Required HD/LOD/poster roles, exact allow-listed hashes, distinct HD/LOD and matching post meta URLs |
| Concept mapping | `plugins/nadlan-config/inc/flagship-surface.php :: nadlan_flagship_v3_validate_experiences()` | Owner-approved illustration remains non-decision-grade; uncited exact spatial mapping is rejected |
| Four visual doors | `plugins/nadlan-config/inc/flagship-surface.php :: nadlan_flagship_v3_validate_visual_playground()` | Exactly View, Interior, Design and Comments; delivery state is `prepared_no_write` |
| Runtime capabilities | `plugins/nadlan-config/inc/flagship-surface.php :: nadlan_flagship_v3_runtime_config()` | `inventory_selection=false`, `lead_submission=false`, `comment_submission=false`, `writes_enabled=false` |
| Visible H1 and protected stage | `plugins/nadlan-config/inc/flagship-surface.php :: nadlan_flagship_v3_render_for()` | v3 owns a visible H1, canvas, model anchors, controls, playground, experiences and buyer-decision sections |
| Dossier boundary | `plugins/nadlan-config/inc/flagship-surface.php :: nadlan_flagship_v3_safe_article_html()` | Rejects H1/main/script/style/iframe/form/event handlers/external media and duplicate dossier markers |
| No legacy fallback | `plugins/nadlan-config/inc/flagship-surface.php :: nadlan_flagship_v3_dispatch()` | A selected invalid v3 contract returns empty rather than silently rendering the legacy surface |
| First-party model reader | `plugins/nadlan-config/assets/flagship-v3/flagship-viewer.js :: create()`, `load()`, `loadUrl()` | WebGL2; read-only same-origin GET; redirect rejection; 12 MB safety cap; keyboard/pointer camera; cleanup |
| Flat material limitation | `plugins/nadlan-config/assets/flagship-v3/flagship-viewer.js :: fragment shader`, `load()` | Renderer consumes `baseColorFactor` into a color uniform; it does not sample material textures |
| Model/fullscreen state | `plugins/nadlan-config/assets/flagship-v3/flagship.js :: captureModelState()`, `openExperience()`, `restorePage()` | Body-level dialog and restoration of model state, scroll and focus |
| Playable visual tools | `assets/showroom/flagship-showroom-runtime.js :: previewMarkup()`, `toolBodyMarkup()`, `installDrag()`, `openTool()` | Schematic map, step/door/light interior simulation, one draggable sofa and local prepared-no-write annotation |
| Model space | `plugins/nadlan-config/assets/flagship-v3/flagship.css :: .nlfs__protected-stage`, `.nlfs__model-hotspot` | Protected stage, clipped overlays, `touch-action:none`, 44 px model-anchor hit areas and mobile height floor |
| Remaining target-size gap | `plugins/nadlan-config/assets/flagship-v3/flagship.css :: .nlfs__source-refs a` | Source-reference targets are 32 x 32, below the site's 44 px product standard |
| Shared loader | `plugins/nadlan-config/nadlan-config.php :: module list` | Working tree loads `flagship-surface` before `showroom-engine` |
| Shared dispatch seam | `plugins/nadlan-config/inc/showroom-engine.php :: priority-8 content composer`, `PHP_INT_MAX content callback` | Selected v3 pages route through the new surface while unselected projects retain legacy rendering |
| Legacy data engine | `plugins/nadlan-config/inc/showroom-engine.php :: nadlan_showroom_engine_build_project()` | Shared project meta feeds model, units, floor height, environment, tours and landmarks |
| Legacy live context map | `plugins/nadlan-config/inc/project-experience.php :: unified map renderer`, `plugins/nadlan-config/assets/showroom-engine/mapbox-init.js :: mount()` | Live Mapbox map, project/nearby pins, POI layers and one-map doctrine |
| Legacy direction/view | `plugins/nadlan-config/assets/showroom-engine/engine.js :: showViewCone()`, `winCam()`, `winView()` | Direction cone/beam, model-to-map bearing and live view-from-unit camera paths |
| Existing lead rail | `plugins/nadlan-config/assets/showroom-engine/buyflow.js :: submit path` | Selected unit context is posted through the existing shared lead route |
| Recipe reconciliation | `skills/recipe-flagship-project-page.md`; `docs/plans/einstein-flagship-recipe-draft/`; maintained `nadlan-flagship-project-showroom` agent skill | Obsolete `<1 MB`/no-normal rule and missing links are removed; shared-engine, governed-package, measured-model and private-readback gates are active |
| New owner fidelity rule | `docs/plans/einstein-tower-owner-decision-log.md :: OWNER-2026-08-14-EINSTEIN-ILLUSTRATIVE-MASSING` | Einstein HD must contain at least 30,000 real rendered triangles and retain a separate LOD |
| Publication boundary | `docs/plans/einstein-tower-publication-manifest.json :: private_stage`, `blocked_until`, `publish_rule` | Distinct password sandbox, before snapshot, private readback and explicit release are mandatory |
| Prior cross-market UI research | `docs/2026-06-04-sitewide-premium-micro-ui-standard.md :: Reference signals checked` | Records which Israeli and international product surfaces informed the repository's micro-UI standard; it is a capability reference, not proof of commercial impact |
| Prior catalog research | `docs/2026-06-04-catalog-premium-spec.md :: What I Actually Looked At` | Records the repository's observed catalog patterns and the separation between evidence, interpretation and implementation decisions |
| Prior apartment-cell research | `docs/2026-06-14-rainbow-apartment-cell-product-spec.md :: Research lessons` | Records comparison lessons for visual unit choice, view context, trust and inquiry progression without claiming causation |
| Prior showroom-journey research | `docs/design/2026-06-19-project-showroom-engine-interior-journey.md :: External Product References`, `Buyer Journey Gate` | Records external product references and the repository's buyer-journey gate for interactive showroom experiences |

## 2. Live rendered evidence

Observed on 2026-08-14 at 390 x 844 after scrolling each model into view.

| Page | HTTP | H1 | Body width | Model stage | Unified map | Hotspots | Hreflang | Model semantics |
| --- | ---: | --- | --- | --- | --- | --- | ---: | --- |
| H Infinity | 200 | One 1 x 1 absolute H1 | 390 / 390 | 368 x 490.7 | 348 x 440 | 52; all below 44 px | 2 | `<model-viewer>` had no `alt` or `aria-label` |
| Rainbow | 200 | One 1 x 1 absolute H1 | 390 / 390 | 368 x 490.7 | 348 x 440 | 6; all below 44 px | 6 | `<model-viewer>` had no `alt` or `aria-label` |
| Dimri Yama | 200 | One 1 x 1 absolute H1 | 390 / 390 | 368 x 490.7 | 348 x 440 | 4; all below 44 px | 6 | `<model-viewer>` had no `alt` or `aria-label` |
| Ashira | 200 | One 1 x 1 absolute H1 | 390 / 390 | 368 x 490.7 | 348 x 440 | 5; all below 44 px | 6 | `<model-viewer>` had no `alt` or `aria-label` |
| ToHa2 | 200 | One 1 x 1 absolute H1 | 390 / 390 | 368 x 490.7 | 348 x 440 | 75; all below 44 px | 6 | `<model-viewer>` had no `alt` or `aria-label` |
| The Park | 200 | One 1 x 1 absolute H1 | 390 / 390 | 368 x 490.7 | 348 x 440 | 44; all below 44 px | 6 | `<model-viewer>` had no `alt` or `aria-label` |

The H1 exists semantically but is not a visible page title: its measured box is 1 x 1 and its position is absolute. "No horizontal overflow" here means document client width equaled document scroll width at the tested mobile viewport; it is not a complete responsive certification.

## 3. Local test evidence

| Check run on 2026-08-14 | Result | Scope |
| --- | --- | --- |
| `php scripts/qa-flagship-v3-php.php` | PASS | Private fixture, exact contracts/assets, one visible H1, no form/write path, source/mapping rejection, same-origin viewer, unselected legacy preservation |
| `node scripts/qa-einstein-project-identity.mjs` | PASS | Post/slug/parcel/building/unit identity, aliases, related-project separation and catalog row |
| `node scripts/qa-project-showroom-inventory-contract.mjs` | PASS | Zero units fail closed; explicit non-decision inventory remains a future compatible lane; legacy payload remains compatible |
| `node scripts/qa-einstein-flagship-offline.mjs` | PASS | Real local GLB, protected model, four permanent teasers, four selectable interior/facility scenes, three anchors, exact Back, no tool I/O, 44 px/12 px/no-inner-scroll at four viewports |

These are local/fixture results. They do not substitute for authenticated WordPress readback, actual network performance or public-page proof.

## 4. Binary acceptance gates

Legend: PASS = evidenced now; FAIL = current implementation contradicts the gate; OPEN = not yet proved; DEFERRED = waits for contractor/official data and must not block an honest zero-inventory private demo.

### A. Identity and release boundary

| ID | Gate | Current |
| --- | --- | --- |
| A1 | One canonical: post `4867`, slug `einstein-tower`, contract `einstein-tower-6885-32`, parcel `6885/32` | PASS locally |
| A2 | Einstein 18/Levichko remain aliases only; separate Einstein projects remain distinct | PASS locally |
| A3 | Private stage is a different password-protected post linked back to `4867` | OPEN |
| A4 | Canonical post `4867` is unchanged until a before snapshot, rollback artifact and explicit release action exist | OPEN operationally |
| A5 | `public_release_enabled` remains false during private acceptance | PASS |

### B. Evidence and public truth

| ID | Gate | Current |
| --- | --- | --- |
| B1 | Every public factual value has a source ID, effective date and truth/current/future state where applicable | PASS in buyer contract fixture; OPEN in WordPress |
| B2 | No model-local coordinate is described as a surveyed/cardinal/official real-world location | PASS in contracts |
| B3 | One global demonstration label is visible; repetitive caveats do not bury the interaction | PASS in fixture/offline; OPEN in WordPress |
| B4 | Unit, availability, price, plan and unit-view claims remain absent while inventory is empty | PASS |
| B5 | Source refresh identifies changed/expired claims before publication | OPEN |

### C. Model and hotspots

| ID | Gate | Current |
| --- | --- | --- |
| C1 | HD contains at least 30,000 real rendered triangles, no hidden/filler geometry used to reach the count | PASS on count; filler/visual review PASS only in offline preview |
| C2 | HD/LOD/poster bytes and SHA-256 values exactly match the contract registry | PASS locally |
| C3 | HD and LOD are distinct; LOD preserves a readable project silhouette at constrained-data/mobile scale | Distinct PASS; visual sufficiency OPEN in WordPress |
| C4 | Model center remains directly hit-testable; no CTA, teaser, label or hotspot layer covers the building | PASS offline; OPEN in WordPress |
| C5 | Every hotspot has asset/scene binding, model component, model coordinate, confidence, evidence basis, ambiguity and prohibited inferences | PASS |
| C6 | Projected hotspots remain at least 47.5 px apart at required camera/viewports or collapse into an accessible list/cluster | PASS offline for three anchors; OPEN in WordPress |
| C7 | Every model/scene asset is same-origin, immutable/reviewed and route-scoped | PASS locally; OPEN in deployed headers/network |
| C8 | Material rendering meets the intended visual standard, including textures when required | FAIL for texture support in current first-party viewer |

### D. Playable buyer tools

| ID | Gate | Current |
| --- | --- | --- |
| D1 | Exactly four permanent top-level invitations: View, Interior, Design, Comments | PASS offline/fixture |
| D2 | Touch/focus visually activates the invitation; activation opens a body-level full-screen experience | PASS offline |
| D3 | Back restores exact model camera, scroll, active teaser and focus | PASS offline |
| D4 | View capability label matches reality: schematic until a live map and beam are connected | OPEN copy review |
| D5 | Interior capability label matches reality: concept simulation until a spatial tour/plan exists | OPEN copy review |
| D6 | Facilities are selectable inside the Interior experience and bound to governed anchors | PASS offline |
| D7 | Design is labeled as an illustrative layout interaction until official plan geometry exists | OPEN copy review |
| D8 | Comments visibly says local/prepared-only and creates no external write | PASS offline |
| D9 | OLP delivery remains disabled until recipient/auth/privacy/retention/idempotency/acknowledgement/retry/failure gates pass | PASS by absence; production DEFERRED |

### E. Buyer decision and money path

| ID | Gate | Current |
| --- | --- | --- |
| E1 | Page answers identity, building composition, current construction, future context, education snapshot, sea method and overseas-buyer process with sources | PASS fixture/content contract; OPEN in WordPress |
| E2 | One on-demand live map renders current/future layers and nearby decision points | FAIL; current View is schematic and context section is text |
| E3 | Direction beam uses the existing frozen shared semantics and a calibrated project orientation | FAIL; orientation is illustrative and v3 has no live beam |
| E4 | If inventory exists, a selected unit answers availability, floor, rooms, sqm, direction/view, price basis, plan/tour and inquiry context | DEFERRED; current inventory is empty |
| E5 | In zero-inventory mode, inquiry still captures project/language/source without inventing a unit | FAIL; lead submission is disabled |
| E6 | Real inquiry uses the existing shared lead rail, with consent and recoverable errors; no second endpoint | OPEN |

### F. Mobile, accessibility and performance

| ID | Gate | Current |
| --- | --- | --- |
| F1 | 320 x 568, 390 x 844, 568 x 320 and 1280 x 800: no horizontal overflow, clipped controls or inner scroll trap | PASS offline; OPEN in WordPress |
| F2 | All interactive targets are at least 44 x 44 px, including citation/source controls | FAIL; source-reference chips are 32 x 32 |
| F3 | Keyboard operates model, dialogs, tools and Back; visible focus returns correctly | PASS offline; OPEN in WordPress |
| F4 | Canvas/model has an accessible name and poster alternative | PASS in renderer fixture; OPEN in WordPress |
| F5 | RTL/LTR, screen-reader reading order, dialog announcements and contrast pass manual/automated review | OPEN |
| F6 | Reduced-motion and Save-Data paths work without losing content or control | Code present; OPEN in WordPress |
| F7 | Real WordPress request/transfer inventory, LCP, INP, CLS and memory meet agreed budgets on representative mobile hardware | OPEN / not measured |
| F8 | Showroom-only assets load only on the selected project route and no duplicate renderer initializes | Contracted; OPEN in WordPress network trace |

### G. SEO, language and fleet integration

| ID | Gate | Current |
| --- | --- | --- |
| G1 | Exactly one visible H1; self-canonical only when public; no canonical while private | PASS fixture; OPEN in WordPress |
| G2 | Title, description, breadcrumb and project/entity schema have one owner and contain no duplicate graphs | OPEN |
| G3 | No second Einstein URL or cannibalizing article; catalog card resolves to post `4867` after release | PASS locally; OPEN live |
| G4 | Hebrew is complete before first release; no hreflang to absent pages | PASS manifest state |
| G5 | Future HE/EN/FR/RU/AR siblings are complete, reciprocal, functionally equivalent and include x-default before hreflang activation | DEFERRED |
| G6 | Rainbow, Dimri Yama, Ashira, ToHa2, The Park and H Infinity retain renderer, map, beam, unit/lead and responsive behavior | OPEN fleet regression |
| G7 | Public archive, REST search, sitemap, feeds and catalog exclude private stage and include only the released canonical | Fixture PASS for protections; OPEN in WordPress |

## 5. Explicitly not checked

- Authenticated/private WordPress staging and exact REST readback.
- Real public v3 render; public release is disabled.
- Core Web Vitals, transfer size, CPU/GPU time and memory on production.
- Screen-reader output, contrast audit and assistive-technology behavior in WordPress.
- Search Console performance or indexing effects.
- Contractor BIM, official plans, price list, live inventory, target amenities or unit-specific views.
- Legal/contractual accuracy beyond the cited source register.
