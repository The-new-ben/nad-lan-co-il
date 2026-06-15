# Rainbow Template v1 Control Gate

Date: 2026-06-15  
Scope: Rainbow Tel Aviv first, then Sde Dov projects.  
Status: Control gate, docs-only. No plugin code, no ZIP, no deploy.

## Honest Current State

Rainbow is not ready to clone into the next project yet.

The page is much closer than the first versions: the live plugin is back to a clean `1.66.2`, the
model rail exists, the buyer can select units, and the page has a project-specific SEO title,
description, schema flags and media. But the current implementation still fails the template gate.
If we start making more projects now, we will multiply the same problems.

## Evidence Checked

Live URL checked:

`https://nad-lan.co.il/projects/rainbow-tel-aviv/`

Live healthcheck evidence:

- `version`: `1.66.2`
- `project_3d.model_viewer_ready`: true
- `project_3d.projects_with_glb`: 1
- `project_3d.dual_showroom`: true
- `project_3d.cell_selector`: true
- `lead_e2e`: true
- `whatsapp_loaded`: true
- `price_meta`: true
- `faq_meta`: true

Media evidence:

- `og:image` points to `rainbow-tel-aviv-hero.jpg`.
- `https://nad-lan.co.il/wp-content/uploads/2026/06/rainbow-tel-aviv-hero.jpg` returns HTTP 200.
- `https://nad-lan.co.il/wp-content/uploads/2026/06/rainbow-tel-aviv-hero-1024x576.jpg` returns HTTP 200.

Current QA evidence:

The visual harness `scripts/qa-project-showroom-visual.mjs` failed all four viewports in strict
mode in the last recorded run:

- desktop 1440
- tablet 768
- mobile 390
- Edge mobile 390

The most important failures were:

- mobile showroom shifted/cropped,
- public wording check failed,
- buyer CTA signal was not detected by the harness,
- the selected card can dominate or block the selection experience,
- only a small sample of units exists,
- the selector is still not visually strong enough to read as a full building inventory.

## Product Truth

The owner is asking for a buyer showroom, not a 3D decoration.

The buyer should understand, without explanation:

1. this is Rainbow Tel Aviv,
2. apartments are selectable,
3. available/reserved/sold state is visible,
4. the selected apartment has floor, rooms, sqm, view and non-binding price context,
5. the next action is to ask about that exact apartment.

The contractor should understand:

1. this can be their project page,
2. inventory and media can be edited from CMS fields,
3. inquiries arrive with unit context,
4. this is a premium sales room, not a standard WordPress listing.

## Architecture Decision

Until the developer supplies official BIM or a GLB where every apartment is a separate clickable
surface, do not promise true apartment-level 360-degree picking inside the rotating 3D model.

The honest v1 architecture is:

1. Keep the GLB/model-viewer building as the premium rotating product object.
2. Add a static facade or elevation selector beside it for apartment picking.
3. Make the facade cells look like apartments embedded in the building, not floating dots.
4. Wire both views to the same `project_3d_units` data.
5. When official BIM arrives, replace the facade approximation with real mesh-level hotspots.

This is not a downgrade. It is the correct product shape until official geometry exists.

## Template v1 Must Pass

Rainbow Template v1 is not ready until all of these pass on the live page:

1. One visible H1.
2. No visible raw code, class names, JavaScript, PHP warnings or internal operations words.
3. Hero/project image renders and `og:image` uses HTTPS.
4. Short buyer intro appears before the showroom and names the project, Sde Dov, developer,
   availability and non-binding price context.
5. The showroom is not cropped at 1440, 768, 390, or Edge mobile 390.
6. On mobile, the showroom starts within the viewport and does not shift right.
7. The GLB/model-viewer is visible, not blank, and the fallback tower is hidden once the GLB loads.
8. The model opens close enough for buyers to see the building.
9. Spin/drag is stable and not too fast.
10. Apartment selection is by cell/rectangle, not abstract dot.
11. Cells are available/reserved/sold color-coded.
12. Recommended available units may pulse, but sold units do not pulse.
13. Every tap target is at least 44px on mobile.
14. Selecting a cell opens a selected-apartment card without hiding the building.
15. The card shows unit label, floor, rooms, sqm, view, status and non-binding estimate.
16. The card has a clear buyer CTA for that selected unit.
17. WhatsApp/contact/lead payload includes the selected unit.
18. The contractor CTA exists but does not use internal words.
19. The page has index/follow, canonical, title, description, and project schema.
20. `price_range`, `price_min`, `price_max`, `amenities`, `official_site_url`, and
    `project_faq_json` are filled or intentionally marked missing.
21. English/international readiness is documented: canonical Hebrew page now, future translated
    pages with hreflang later.
22. Chrome screenshots are captured at 1440, 768, 390 and Edge mobile 390.
23. The owner manual explains how to update all fields without writing code.
24. The next project can be created from one payload file plus media/model assets.

## Next Surgical Slice

Do not start another broad plugin build. The next code slice should be narrow:

1. Fix mobile cropping/shift first.
2. Make the selected apartment card non-blocking.
3. Make the cell selector visually stronger: apartment rectangles in the facade, with enough
   label/status information to be useful.
4. Normalize the heading/body alignment so section titles sit visually with their paragraphs.
5. Replace or repair the first public image/OG if the rendered page still does not show the intended
   image after cache is cleared.
6. Re-run the live visual harness.

Only after this slice passes should Rainbow be used as a template for another project.

## Owner-Only Inputs Needed Later

These are not blockers for the next surgical slice, but they are needed for the full product:

1. official developer BIM/GLB,
2. official elevation/facade drawing,
3. real available/reserved/sold inventory,
4. approved unit prices or approved estimate method,
5. contractor WhatsApp and phone,
6. approved English copy policy for foreign buyers,
7. CDN or storage decision for large GLB/video assets.

## Replication Rule

The next Sde Dov project should not get custom code.

It should get:

1. a project research file,
2. a payload JSON file,
3. model/poster/media URLs,
4. unit map JSON,
5. drawings/environment JSON,
6. Chrome QA screenshots,
7. published page verification.

If a next project requires editing `project-3d.php`, the template is not finished yet.
