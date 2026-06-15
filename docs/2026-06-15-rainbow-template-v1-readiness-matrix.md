# Rainbow Tel Aviv Template v1 Readiness Matrix

Date: 2026-06-15  
Live target checked: `https://nad-lan.co.il/wp-json/nadlan/v1/healthcheck?cb=codex-readiness`  
Live plugin version at check time: `1.66.2`  
Purpose: keep the Rainbow flagship project honest before cloning it into the next Sde Dov project.

## Executive Status

Rainbow is no longer a plain article. It has the core rails for a repeatable project showroom:

- project-specific SEO title and meta;
- project schema fields for price/FAQ/official-site data;
- a GLB/model-viewer rail;
- dual showroom architecture: rotating 3D model plus static facade/elevation selector;
- apartment cells driven by `project_3d_units`;
- owner metabox and REST/payload routes;
- lead/WhatsApp rails that preserve selected-unit context;
- visual QA scripts and owner manual.

It is still **not** the final reusable template until the live page passes mobile visual QA after
the v1.66.3 containment patch and until the product selector uses approved facade/BIM material for
each new project.

## Current Evidence From Live 1.66.2

| Area | Evidence | Status |
| --- | --- | --- |
| Plugin deploy | Healthcheck reports `version: 1.66.2`. | Live |
| Model-viewer rail | `project_3d.model_viewer_ready: true`, `model_viewer_module_tag: true`, `model_viewer_reveal: "auto"`, `projects_with_glb: 1`. | Live |
| Dual selector | `dual_showroom_v1661: true`, `embedded_selector_with_glb_v1661: true`, `stage_xywh_fields_v1661: true`. | Live |
| CMS editability | `admin_unit_builder_v1650: true`, `rest_showroom_fields_v1651: true`, `showroom_payload_api_v1652: true`, `showroom_payload_fields: 17`. | Live |
| SEO/schema | `project_page_assembly.rainbow_seo_v1634: true`, `faq_meta: true`, `price_meta: true`, title and description overrides present. | Live |
| Lead journey | `lead_unit_payload: true`, `lead_e2e.enabled: true`, `whatsapp_funnel.loaded: true`. | Live |
| QA blocker pending | PR #187 adds v1.66.3 mobile containment, public-copy cleanup and same-site OG-image HTTPS normalization. | Pending deploy |

## Pending Patch Before Rainbow Can Be Cloned

Draft PR #187: `v1.66.3 Rainbow mobile containment + public copy cleanup`.

Why it matters:

- the 390px and Edge-mobile visual harness measured the showroom root shifted off-screen;
- after selecting an apartment, the mobile scene collapsed to a 2px strip;
- old public wording still contained internal words around leads / lead panel;
- the rendered same-site `og:image` URL was HTTP, which blocks the template gate.

Do not use Rainbow as the clone source for the next project until the post-deploy gate proves:

1. healthcheck reports `version: 1.66.3`;
2. `project_page_assembly.rainbow_public_copy_v1663` is true;
3. the visual harness passes or shows only accepted non-blocking findings at 1440, 768, 390 and
   Edge-mobile;
4. public copy contains no internal operations terms;
5. rendered `og:image` uses `https://`.

## Executable Template Gate

Use this command before Rainbow, or any future project, is declared ready to clone:

```powershell
node scripts/qa-project-template-gate.mjs `
  --site https://nad-lan.co.il `
  --slug rainbow-tel-aviv `
  --post-id 4464 `
  --min-version 1.66.3 `
  --visual `
  --strict `
  --out docs/qa/rainbow-template-gate-live.json
```

For translation projects, add `--require-translations` only after real translated URLs exist.

Current live production proof, before PR #187 is deployed: `docs/qa/rainbow-template-gate-live-1662.json`.
It reports `20 passed / 5 failed`, so the page is **not template-ready yet**. The current blocking
failures are exactly the expected ones:

1. live plugin is still `1.66.2`, below the `1.66.3` template gate;
2. `project_page_assembly.rainbow_public_copy_v1663` has not run on production;
3. the OG image URL is HTTP instead of HTTPS, and PR #187 now contains the intended normalizer;
4. public text still contains internal lead wording from the old copy;
5. the visual Chrome gate was not run in that command.

This gate is intentionally stricter than the structural showroom gate. A project can be structurally
healthy and still fail the template gate if the buyer-facing visual page, public copy or SEO asset
quality is not ready.

## What Is Done Enough To Reuse

| Capability | Clone rule |
| --- | --- |
| Project data contract | Use `showroom-payload.json` as the handoff artifact. Do not manually paste every field when a payload import is available. |
| 3D model field | `project_model_glb` is the swappable model URL. Use external/raw/CDN URLs, not huge files in the plugin ZIP. |
| Poster field | `project_model_poster` is required so the stage never starts blank. |
| Unit data | `project_3d_units` is the current source for status, floor, rooms, sqm, view, estimates, facade cell placement and model hotspots. |
| Owner editing | The `בחירת דירות אינטראקטיבית` metabox is the owner-facing path. Raw JSON is import/debug, not the preferred owner workflow. |
| Schema | Fill `amenities`, `official_site_url`, `price_range`, `price_min`, `price_max`, `project_faq_json`. Schema code already emits these fields. |
| Lead capture | All CTAs must keep `card_id` and selected-unit data. WhatsApp should enter the same lead rails, not disappear into private chat. |
| Health proof | Every new feature needs a healthcheck marker that proves it ran on live after plugin update. |

## What Is Not Done Yet

| Gap | Why It Matters | Safe Next Step |
| --- | --- | --- |
| Official per-apartment 3D geometry | A true 360-degree rotating building where every apartment surface is clickable requires a BIM/GLB where units are separate meshes. The current prototype model is not that. | Keep the GLB as emotional 3D and use facade/elevation cells for precise apartment picking until developer BIM exists. |
| Official facade/elevation | The current facade selector can place cells, but a real contractor page should use the developer's approved elevation or a licensed/original illustration. | Ask the developer for elevation/front render/floor stack, then map `stage_x/y/w/h` cells to that image. |
| Real inventory and prices | Estimates are useful but cannot be sold as official availability or official price. | Store status and prices only with source note and owner approval. Default to `אומדן לא מחייב` or `לפי פנייה`. |
| Mobile/social final polish | PR #187 targets the mobile containment failure, public-copy cleanup and same-site OG HTTPS normalization, but live green proof must come after deploy. | Merge/update/cache-clear, then rerun visual and template QA. |
| International pages | Live Rainbow is Hebrew. No proven EN/FR/RU page, hreflang set, translated schema, or foreign-buyer CTA exists yet. | Decide translation architecture before creating routes. Start with English as a pilot after Hebrew template is green. |
| Yoast 100% proof | Title/meta/schema exist, but a Yoast green-light screenshot or API proof is not stored in the repo. | Add Yoast/readability proof to the project QA packet before declaring SEO complete. |
| SERP/rank proof | IndexNow pings exist, but ranking for project terms is not proven. | Track queries: `ריינבו תל אביב`, `Rainbow Tel Aviv`, `ריינבו שדה דב`, `דירות למכירה Rainbow תל אביב`, `מחיר ריינבו תל אביב`. |

## Multilingual Readiness Plan

Do **not** create multilingual public routes casually. The current URL contract is one concept, one
canonical URL unless an owner-approved language architecture exists.

Recommended architecture before implementation:

1. Hebrew canonical remains `/projects/rainbow-tel-aviv/`.
2. If multilingual is approved, use language-prefixed equivalents such as:
   - `/en/projects/rainbow-tel-aviv/`
   - `/fr/projects/rainbow-tel-aviv/`
   - `/ru/projects/rainbow-tel-aviv/`
3. Add `hreflang` only when each translated page is real, published and equivalent.
4. Keep all facts, prices and disclaimers source-linked in the source payload, then translate the
   presentation layer. Do not let translations invent availability, taxes, financing rules or
   legal promises.
5. The first language pilot should be English for foreign buyers. French and Russian follow only
   after the English workflow is proven.

Fields that must be language-ready:

- project title and subtitle;
- first intro paragraph;
- selected-apartment card labels;
- price disclaimer;
- FAQ;
- foreign-buyer block;
- lead/WhatsApp default messages;
- schema description and FAQ answers.

## Safe Architecture Split

This is the boundary to reduce future breakage:

| Layer | Owns | Must Not Own |
| --- | --- | --- |
| Plugin | CPT/meta/REST, showroom renderer, schema, lead payload, healthcheck, package update. | Global site typography, header/footer layout, generic page chrome. |
| Theme | Header, footer, breadcrumbs placement, global page width, typography rhythm, body article skin. | Project inventory, model data, lead routing, business logic. |
| CMS/project payload | Per-project content, Yoast fields, model URLs, unit inventory, drawings, surroundings, official links. | PHP behavior or global CSS hacks. |
| External storage/CDN | GLB, poster, large renders, developer material. | Plugin ZIP contents, unless the asset is tiny and intentionally bundled. |

Rule: a future project should be mostly **fields and assets**, not a new plugin release. Plugin
changes are justified only when the template itself lacks a reusable capability.

## One-Shot Project Factory Checklist

For the next Sde Dov project, do this in order:

1. Research SERP and official/developer/municipal facts.
2. Create `assets/projects/<slug>/source-notes.md`.
3. Build or collect approved model/facade/poster assets.
4. Create `unit-map.json`, `drawings.json`, `environment.json`.
5. Generate `showroom-payload.json`.
6. Validate the payload against `docs/templates/project-showroom-payload.schema.json`.
7. Create or update the `nadlan_project` post with ASCII slug.
8. Import the payload through `/wp-json/nadlan/v1/project-showroom/<id>`.
9. Fill Yoast title/meta and schema meta.
10. Run visual QA at 1440, 768, 390 and Edge-mobile.
11. Check one H1, no internal public wording, no overflow, clickable apartment cells, lead payload,
    schema, title/meta and image/poster visibility.
12. Publish only after the screenshots prove the buyer page, not just the saved fields.

## Owner / Developer Inputs Still Needed

The site can prototype without these, but the final paid contractor version needs them:

1. Official BIM/GLB or source model, preferably with per-apartment surfaces.
2. Official elevation/facade render or blueprint for embedded apartment cells.
3. Official inventory status: available/reserved/sold.
4. Approved price list, price ranges or payment-plan wording.
5. Official floor plans and apartment plans.
6. Developer-approved sales video / interior tour / meeting link.
7. Contractor WhatsApp and sales email.
8. Permission to publish any paid-source sales or transaction data.
9. Storage/CDN decision for large GLB and media assets.
10. Translation/legal review for English and other foreign-buyer pages.

## Decision

Rainbow can be used as a **technical base** for the next project after v1.66.3 passes live QA.

Rainbow should not yet be used as a **sales-quality visual clone** until the facade/elevation source
is replaced with approved project art and the mobile selected-card gate is green on production.
