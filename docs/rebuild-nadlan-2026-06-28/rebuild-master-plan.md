# NADLAN Rebuild Master Plan

## What I Understand

The target is not "fix one widget". The target is a rebuilt NADLAN real-estate website:

- strong SEO authority,
- premium Hebrew-first real-estate brand,
- serious international investor pages,
- project catalog and project pages,
- 3D showrooms inside project pages,
- contractor-ready CMS fields for media, model, facade, plans, tours and contact,
- no stacked legacy visuals,
- no fake public language,
- screenshot-driven QA.

The current theme stays as a backup. The next design system is built cleanly, then activated only
after proof.

## Product North Star

NADLAN should feel like a buyer can:

1. search or browse projects,
2. enter a project,
3. understand the building, area, price context and surroundings,
4. choose an apartment from a clear facade/unit selector,
5. view plan, tour, view, media and estimate when available,
6. contact the developer with the selected unit attached.

At the same time, a contractor should see:

1. a premium project display they would pay for,
2. a CMS structure to update images, video, model, availability and contact,
3. lead capture tied to the selected unit,
4. analytics/interest data as the next monetization layer.

## Architecture Decision

Use a clean theme layer plus the existing plugin data layer.

Theme owns:

- site header/footer/nav,
- homepage,
- project archive/catalog,
- single project layout,
- article design,
- typography, spacing, responsive layout,
- visual hierarchy.

Plugin owns:

- CPTs and meta fields,
- showroom engine payload,
- model-viewer and map seams,
- lead capture and routing,
- healthcheck,
- ZIP/manifest/update surfaces,
- import/validation scripts.

This is safer than forcing every visual change into the plugin.

## Phase 0 - Evidence Lock

Already started:

- all supplied bundles/screenshots/prompts copied into `docs/rebuild-nadlan-2026-06-28/`,
- previous live-versus-mock QA copied into the same folder,
- repo knowledge sources mapped,
- anti-stack rules written.

Do not begin rebuild work before this folder is committed or otherwise treated as the working source
of truth.

## Phase 1 - Backup And New Theme Shell

Goal: create a clean theme shell without risking the current live theme.

Steps:

1. Snapshot current root theme files: `theme.json`, `style.css`, `functions.php`, `templates/`,
   `parts/`, `patterns/`.
2. Create the new NADLAN theme/design system in a clean branch or side-by-side theme directory.
3. Implement tokens from the accepted visual direction: cream, ink, gold, terracotta, sage, measured
   borders, editorial type.
4. Build header, footer, navigation, language position, search entry and project CTA.
5. QA the shell on desktop/mobile before adding project complexity.

Acceptance:

- homepage shell matches the approved direction,
- old theme can be restored,
- no duplicate header/footer,
- no Woo/cart/admin/internal leakage on public pages.

## Phase 2 - Homepage Rebuild

Goal: a real-estate authority homepage, not a 3D-only landing page.

Sections:

1. hero: buyer/investor/property search entry,
2. project preview band with showroom cards,
3. calculators/tools band,
4. area/neighborhood intelligence,
5. guides and legal/tax/mortgage content,
6. professional directory entry,
7. contractor/project promotion CTA.

The multi-project showroom engine can appear above the fold but not as the only message. It must
use buyer language: browse projects, compare homes, choose an apartment, check area context.

Acceptance:

- visually compared to the mock pack,
- no internal/product-manager language,
- links resolve,
- mobile layout is clean,
- Lighthouse/SEO quick checks are run.

## Phase 3 - Project Catalog

Goal: `/projects/` becomes the gateway to all project showrooms.

Sections:

- project cards,
- city/area filters,
- price/status tags when sourced,
- project media preview,
- direct link to the project page,
- no dead language-home routes.

Acceptance:

- catalog loads,
- each card routes to a real project,
- no 404 from homepage/project links,
- no duplicate archive/grid renderers.

## Phase 4 - Single Project Template

Goal: build the final project page structure once, then use it for Ashira, Rainbow, Dimri and future
projects.

Order:

1. breadcrumbs,
2. short source-backed intro,
3. hero/project facts,
4. showroom section,
5. apartment selector and selected-apartment card,
6. price range/comps,
7. surroundings/map,
8. media/tour/gallery,
9. full article,
10. inquiry/contact,
11. disclaimer.

3D architecture:

- rotating GLB/model is for context,
- facade/unit selector is for apartment picking unless the GLB has per-unit geometry,
- if real BIM/per-unit GLB arrives later, upgrade the selector without changing the page structure.

Acceptance:

- exactly one showroom renderer,
- selected unit updates card and lead payload,
- mobile selector does not overflow,
- article headings align above paragraphs,
- no fake or single invented prices.

## Phase 5 - Ashira Presentation Page

Goal: Ashira is the first clean rebuilt project page, not stacked over Rainbow history.

Work:

1. SERP research in Hebrew and English first.
2. Research project/developer/location/public facts.
3. Build sourced Hebrew content.
4. Build English investor content.
5. Add French/Russian/Arabic only as separate crawlable pages after content and hreflang structure
   are ready.
6. Use concept media only with visible "illustrative" label.
7. Wire official assets later through CMS fields, not by code rewrites.

Acceptance:

- presentation-ready desktop/mobile screenshots,
- content is buyer-facing and source-backed,
- language pages do not cannibalize or fake switch,
- no internal words on public page.

## Phase 6 - Multilingual Strategy

Short-term:

- use separate crawlable posts/pages per language,
- add reciprocal `hreflang`,
- language switch navigates to sibling URL,
- each language has real translated/localized content.

Do not install a heavy multilingual plugin until we decide URL structure, redirects, Yoast behavior,
editor workflow and migration risk.

External anchor:

- Google says `hreflang` tells Google about localized versions, but Google still determines language
  algorithmically, so each page must be genuinely written in that language.

## Phase 7 - Data And Media Pipeline

Each project should be field-driven:

- project name,
- developer,
- area,
- facts,
- model URL,
- poster URL,
- facade URL,
- units JSON,
- availability/status,
- price estimate inputs,
- video URL,
- tour URL,
- gallery,
- map/environment data,
- contact/WhatsApp,
- language sibling URLs.

Large assets should not bloat the plugin ZIP. Use Media Library or R2/CDN for GLB, posters, facade,
video and tour files.

## Phase 8 - QA System

Every release gets:

- desktop screenshot,
- mobile screenshot,
- Hebrew and English where relevant,
- no horizontal overflow,
- one H1,
- no duplicate renderer,
- no old design remnants,
- no internal public words,
- link check,
- healthcheck when plugin is touched,
- `git show --stat HEAD`.

## What Can Be Built Now

Achievable now:

- the rebuild evidence library,
- the new theme shell,
- homepage template,
- project catalog template,
- single project template,
- Ashira clean project page using available/prototype assets,
- field-driven media slots,
- separate language pages and hreflang,
- screenshot QA workflow.

Not honestly guaranteed without owner/developer assets:

- official photoreal Ashira building,
- exact per-apartment real inventory,
- exact official unit prices,
- true click-any-apartment on rotating 3D unless the model has per-unit geometry,
- official interior tours unless supplied or clearly labelled as illustrative concept media.

## First Build Goal After This Planning Step

Build the new theme shell and homepage/project template prototype in a clean branch, with no live
activation and no plugin release, then screenshot it against the mock. Only after that should we
connect live project data.

This is the safest way to honor "from scratch" without damaging the working production site.
