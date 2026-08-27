# Dimri Yama Showroom Prep And Anti-Drift Plan

Date: 2026-06-19
Status: preparation gate, no risky deploy yet
Target project: DIMRI YAMA / YAMA TLV, Sde Dov, Tel Aviv

## Honesty Statement

This goal is achievable if it is handled as a showroom factory, not as another open-ended plugin
rewrite. The achievable first target is not "perfect countrywide system in one jump"; it is:
create one Dimri Yama page plan and data package that can reuse the Rainbow showroom DNA, prove it
with screenshots, and only then implement in small reversible slices.

I will not mark the work done because a file is written, a branch exists, or a field is saved.
Done means the rendered page passes the buyer and contractor gates in Chrome.

## Anti-Drift Rule For This Mission

Each step must answer one question:

> Does this action directly make the Dimri Yama showroom more real, more verifiable, or more
> reusable?

If no, do not do it.

Workflow:

1. Pick one slice.
2. Define the proof for that slice.
3. Make the smallest change that can pass that proof.
4. Verify in Chrome and with scripts.
5. Record screenshots and source notes.
6. Only then continue.

Missing local tools are not a reason to drift. If a tool is missing, install or configure it where
the PC/session allows. If the environment requires an approval prompt, request it through the tool.
Only these are true owner-only blockers:

- official BIM/GLB/Revit/elevations/floor plans from the developer,
- real unit inventory, prices, availability and legal wording,
- paid-source license approval,
- contractor phone/WhatsApp/contact destination,
- translation/legal review for public English/French/Russian/Arabic pages,
- payment/reservation provider decisions.

## Access Proof Already Established

Chrome/WordPress admin access was verified in this session:

- URL opened: `https://nad-lan.co.il/wp-admin/edit.php?post_type=nadlan_project`
- Screen title: `NadLan Projects`
- Admin bar present: yes
- Logged-in user text: `Ben recovery admin`
- Project rows visible: 20

The live NadLan Config healthcheck was also verified:

- Live version: `1.67.2`
- `project_3d.model_viewer_ready`: true
- `project_3d.showroom_dna_v1664`: true
- `project_3d.facade_picker_side_by_side_v1664`: true
- `project_3d.article_alignment_v1671`: true
- `project_3d.compact_actions_v1672`: true

## What We Are Replicating From Rainbow

The Rainbow DNA is:

- a rotating 3D context model for place, massing, sea/sun/orientation, not apartment picking;
- a fixed facade or elevation selector beside the model for apartment picking;
- apartment cells embedded on the facade, not floating dots;
- selected apartment card with rooms, sqm, floor, view, price estimate, status and actions;
- lead/contact flow carries the selected unit context;
- article headings align above paragraphs, not sideways;
- public copy speaks to buyers/investors/families/foreign buyers, never internal funnel language;
- assets and data should be project fields, not hard-coded one-off plugin code.

## Source Ledger

### Project Facts

Official Dimri project page:
`https://www.dimri.co.il/dimriyama-2/`

Facts to use:

- DIMRI YAMA is between the sea coast and Yarkon Park.
- The project has four buildings, 9 to 39 floors.
- The project includes premium facilities: rooftop infinity pool, indoor semi-Olympic pool, spa,
  sauna, private chef kitchen, gym facing the sea and other amenity spaces.
- Kelly Hoppen CBE is presented as the interior designer.
- Rani Ziss Architects is presented as the architect.
- The compound includes a green inner garden, spacious balconies and a western wave-like facade.
- Dimri was founded in 1989 by Yigal Dimri.

Sde Dov project page:
`https://sdedov.co.il/project/dimri-yama/`

Facts to use:

- The page confirms the same project positioning in the Sde Dov district.
- It lists unit-plan categories by building:
  - Building A: 2, 3, 4 rooms.
  - Building B: 2, 3, 5 rooms.
  - Building C: 2, 3, 4 rooms.
  - Building D: studio, 2, 3 rooms.
- It lists public spaces: infinity pool, indoor pool, spa, gym, yoga/pilates studio, library/work
  space, kids room and wine room.

### Interaction References

Zillow 3D Home / interactive floor plan:
`https://www.zillow.com/3d-home/`

Useful product principle:

- Interactive floor plans help buyers understand where photos belong in the home and whether the
  home fits them.
- The comparable interaction for NadLan is: click a unit cell, then immediately see plan/view/media
  and contact options.

Matterport / Homes.com style reference:
`https://www.homes.com/solutions/matterport`

Useful product principle:

- Interior tours and floor plans are buyer confidence tools.
- For Dimri Yama prototype, the tour slot should exist as a CMS field even if the first media is
  clearly marked illustrative.

model-viewer annotations:
`https://modelviewer.dev/examples/annotations/`

Useful technical principle:

- Hotspots use `slot="hotspot..."`, `data-position` and `data-normal`.
- For this project, model-viewer hotspots are for context points only unless we have a true
  apartment-level GLB. Apartment selection stays on the facade/elevation selector.

### QA And Architecture References

Chrome DevTools Device Mode:
`https://developer.chrome.com/docs/devtools/device-mode/`

- Use it to approximate mobile/tablet rendering and catch overflow.

Lighthouse:
`https://developer.chrome.com/docs/lighthouse/overview/`

- Use it for performance, accessibility and SEO audits.

WordPress child themes:
`https://developer.wordpress.org/themes/advanced-topics/child-themes/`

- Child themes can override templates, parts and patterns.
- Child `functions.php` can modify parent behavior.

## Child Theme Versus Plugin Decision

The plugin is already doing too much visual work. For Dimri and future projects, split the work:

Plugin should keep:

- `nadlan_project` CPT and meta registration,
- REST/data endpoints,
- project showroom data contract,
- field sanitization,
- lead/WhatsApp/AI/payment/business logic,
- model-viewer registration and shared runtime rules,
- importer/validator scripts.

Child theme should own:

- project page template hierarchy,
- breadcrumbs placement,
- hero/showroom positioning,
- article heading alignment and paragraph width,
- visual wrappers and responsive layout CSS,
- language/template presentation when content exists in multiple languages.

Asset storage should not bloat plugin ZIPs:

- GLB/poster/facade/tour media should be Media Library, CDN, or raw GitHub asset URLs during
  prototype.
- The plugin ZIP should not carry heavy project-specific media.

## Dimri Yama Showroom Data Plan

Recommended public slug: `dimri-yama`.

Data package folder:

`assets/projects/dimri-yama/`

Required files:

- `source-notes.md`: source ledger, what is official, what is illustrative.
- `project-meta.json`: fields for WordPress project meta.
- `unit-map.json`: apartment/cell records.
- `drawings.json`: approved floor plans, generated placeholder plans and source notes.
- `environment.json`: Sde Dov context, sea/Yarkon/nearby projects/public services.
- `view-layer.json`: optional view-from-apartment metadata.
- `poster.png` or `poster.webp`: lightweight search/social/showroom image.
- `model.glb`: prototype massing GLB, clearly illustrative until official BIM arrives.
- `showroom-payload.json`: compiled payload for import.
- `qa.md`: screenshots, healthcheck, Chrome/QA results.

Prototype model:

- four-building compound,
- one 38-39 floor tower,
- one 15 floor building,
- two 8-9 floor buildings,
- green internal courtyard,
- western sea orientation,
- labels for sea/Yarkon/Sde Dov context,
- horizontal spin lock: do not show underside of the building.

Facade picker:

- fixed side-by-side with the 3D model on desktop,
- stacked directly below/above model on mobile if side-by-side cannot fit,
- cells embedded in the facade/elevation, not dots,
- status colors:
  - available: green,
  - reserved/high demand: gold,
  - sold/unavailable: muted grey/red,
- labels on cells where space allows: building, floor band, rooms/view shorthand,
- selected card must have a dismiss button and must not cover the cells on mobile.

Prototype unit taxonomy from public sources:

- A: 2/3/4-room cells.
- B: 2/3/5-room cells.
- C: 2/3/4-room cells.
- D: studio/2/3-room cells.

Prices and availability:

- Do not invent official prices.
- Use `אומדן לא מחייב` only when showing area estimate.
- Use `לפי פנייה` when no defensible estimate exists.
- Real inventory/prices require owner/developer approval before public claims.

## Content And SEO Plan

Hebrew is first and must be complete before translations.

Visible first paragraph should explain:

- DIMRI YAMA / YAMA TLV,
- Sde Dov, Tel Aviv,
- four buildings,
- Dimri,
- sea/Yarkon context,
- apartment selection and non-binding price/availability estimate.

Article structure:

1. Buyer summary.
2. Available apartment selector explanation.
3. Project facts table.
4. Location: sea, Yarkon, Sde Dov.
5. Architecture and interior design: Rani Ziss, Kelly Hoppen.
6. Amenities.
7. Investor view and risk notes.
8. Foreign buyer guide.
9. FAQ.
10. Contact / request details.

Languages:

- Hebrew page first.
- English, French, Russian and Arabic should be separate reviewed pages or translation layer with
  correct hreflang.
- Do not claim the multilingual version is ready until each page is reviewed and screenshots pass.

## Buyer Journey Gate

At minimum, a buyer must be able to:

1. Land on the page and immediately understand this is DIMRI YAMA in Sde Dov.
2. See a premium model and context without scrolling too far.
3. Understand sea/Yarkon/sun orientation.
4. Click an apartment cell on the facade.
5. See floor, rooms, sqm, view, status and price wording.
6. Open floor plan/tour/view tabs if present.
7. Contact with the selected unit attached.
8. Dismiss the selected card and choose another unit.

## Contractor Journey Gate

At minimum, a contractor/operator must be able to:

1. Find the project in WordPress admin.
2. Know where the showroom fields live.
3. Replace poster/GLB/facade/drawings/tour URLs.
4. Edit units, status, estimated price and availability.
5. See contact leads with unit context.
6. Update the project without writing PHP.

If the current JSON field is too technical, the next durable task is a simple repeater UI, but the
first implementation can still use validated JSON as long as the owner manual is clear.

## QA Plan

Chrome screenshots:

- Desktop 1440px.
- Tablet 768px.
- Mobile 390px.
- Edge mobile UA.

Required checks:

- one visible H1,
- no raw code/class leak,
- no horizontal overflow,
- no console errors,
- headings aligned above paragraphs,
- model does not show underside on drag,
- facade does not overflow into model on mobile,
- selected card has dismiss button and does not block picking,
- apartment cells are obvious and at least 44px tap target,
- lead/contact button carries unit context,
- Lighthouse performance/accessibility/SEO run recorded,
- WAVE or equivalent accessibility scan recorded,
- Schema validator run recorded when schema changes.

## Immediate Next Slices

Slice 0: verify current Rainbow live and archive lessons.

Proof: screenshots at 1440/768/390 and a short note of remaining flaws.

Slice 1: create Dimri data scaffold only.

Proof: `assets/projects/dimri-yama/` exists, validates, and has source-notes with no copied
unlicensed assets.

Slice 2: generate prototype poster/facade/model assets.

Proof: files exist under budget and are clearly labelled illustrative.

Slice 3: create or find the Dimri WordPress project and fill fields.

Proof: Chrome screenshot of admin fields and public draft/preview.

Slice 4: layout in child theme where possible.

Proof: no plugin ZIP unless data/runtime contract requires it.

Slice 5: publish only after QA screenshots are green.

Proof: live URL and screenshots pass the gate.

## Full Spectrum Required For A Complete Dimri Yama Project

This is the complete target, split into achievable deliverables.

### 1. Research And Source Truth

- Official project facts from Dimri.
- Sde Dov district and competing project context.
- Public plan categories by building.
- Amenities, architect, designer, developer and location facts.
- Competitor SERP and project-page comparison.
- Source ledger for every public claim.

### 2. Page And Design System

- Child-theme-first project template or scoped theme CSS.
- Showroom hero near the top, not buried under article text.
- Short project-relevant intro above the showroom.
- Headings aligned above paragraphs.
- Mobile flow: intro, compact showroom, selected apartment card, contact.
- No raw code leaks, no sideways headings, no overlapping controls.

### 3. 3D Context Model

- Prototype GLB generated from public facts: four buildings, courtyard, sea/Yarkon orientation.
- Horizontal camera lock so the buyer does not see the underside.
- Slow, stable rotation.
- Sea, sun, nearby context and labels.
- Clear label: illustrative model until official BIM is supplied.

### 4. Fixed Facade Apartment Picker

- Static facade/elevation beside the 3D model on desktop.
- Directly stacked near the model on mobile.
- Apartment cells embedded in the facade.
- Status color, label, tap target, hover/tap information.
- Selected apartment card with dismiss button.
- Cell data editable from CMS payload.

### 5. Home.com / Zillow Style Interior Layer

- Floor plan slot.
- Interior tour slot.
- Gallery/media slot.
- View-from-apartment slot.
- If no official media exists, use clearly marked illustrative prototype media.
- Contractor can replace the media later without code.

### 6. Buyer Journey

- See project immediately.
- Understand location and building context.
- Choose an available apartment cell.
- See apartment details and price wording.
- Open tour/view/floor plan.
- Contact with apartment context attached.
- Compare or choose another apartment.

### 7. Contractor Journey

- Contractor/operator can update project poster, GLB, facade, drawings and tour URLs.
- Contractor/operator can update units, status, price wording and availability.
- Contractor/operator can see which apartment generated interest.
- Contractor/operator sees the page as a premium sales center, not a blog article.

### 8. Client / Operator Journey

- Admin can create the next project from a data folder.
- No PHP editing for a normal new project.
- One project asset folder plus CMS fields should be enough.
- QA screenshots and source ledger are required before publishing.

### 9. Monetization

- Per-project setup fee for model, facade, article, media and QA.
- Monthly project showroom subscription.
- Paid upgrade for real BIM, interior tour, lead analytics and premium placement.
- Later: reservation/payment flow only after legal/payment provider decisions.

### 10. Multilingual / Foreign Investor Layer

- Hebrew page first.
- English, French, Russian and Arabic only after reviewed translations.
- Each language needs its own title/meta/body checks and hreflang.
- The same facts must match across languages.
- Public copy must never expose internal words like SEO, funnel, CRM or monetization.

### 11. External QA

- Chrome desktop/tablet/mobile screenshots.
- Edge mobile UA screenshot.
- Lighthouse for performance/accessibility/SEO.
- Chrome DevTools Device Mode for responsive review.
- WAVE or equivalent accessibility pass.
- Schema validator when schema changes.
- Live healthcheck when plugin behavior changes.

## Achievable Goal For The Next Work Cycle

## Current State After Theme Pattern Slice

Done in PR #190:

- Dimri Yama source ledger and reusable project payload scaffold.
- Prototype poster, facade SVG, and massing GLB assets for local demonstration.
- Local showroom preview with desktop/tablet/mobile screenshots.
- Theme-owned block pattern for Dimri Yama, keeping presentation out of the plugin.
- Theme CSS and JS loaded only when the content contains `data-nlps-showroom`.
- 3D context model next to a fixed facade apartment selector.
- Selected-apartment card with plan/tour/view/contact tabs and a close button.
- Buyer form that sends the selected unit context to `/nadlan/v1/lead` when rendered in WordPress.
- Skill updates documenting the theme-first showroom contract.

Not done yet:

- No live WordPress Dimri Yama project page has been published by this PR.
- No official Dimri BIM/GLB, inventory, availability, prices, or approved floor plans are available.
- No approved contractor WhatsApp/phone/email has been provided for public routing.
- No Hebrew/French/English/Russian/Arabic final public copy has been published yet.
- No true mobile-device Chrome QA has been completed for the live page; the local CLI screenshot pass exposed a viewport mismatch and is not enough for final approval.
- No payment/reservation flow is included. This slice supports non-binding inquiry only.

True owner-only blockers:

- Official BIM/GLB or approved model export.
- Official facade/elevation and apartment geometry.
- Real inventory, status, price estimates, and legal approval for public display.
- Contractor contact details and preferred routing.
- Approved media for interior tour, floor plans, finishes, sales video, and foreign-language copy.

Next safe slice:

1. Create the actual Dimri Yama WordPress draft using the theme pattern, not a plugin ZIP.
2. Fill it with prototype assets and clear "illustration only" copy.
3. Run logged-in Chrome QA on the draft at desktop/tablet/mobile.
4. Only after the draft is visually green, decide whether to publish or keep it internal until official materials arrive.

Do not try to finish every future countrywide feature at once.

The next achievable cycle is:

1. Create a clean Dimri Yama asset/data scaffold.
2. Generate prototype poster/facade/model placeholders with no unlicensed copied media.
3. Produce a Hebrew-first project content outline with foreign-language expansion map.
4. Decide the theme/plugin boundary for the first implementation slice.
5. Verify the scaffold and plan with scripts and Chrome before any production deploy.

If that passes, the next cycle is implementation of the public Dimri draft page.

