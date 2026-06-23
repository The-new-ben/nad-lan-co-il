# NadLan War Room Execution Spec

Date: 2026-06-23  
Branch: `strategy/nadlan-seo-product-war-plan`  
Scope: strategy, SEO governance, product UX, visual evidence, and build backlog. No runtime code is changed by this packet.

## Objective

NadLan is being organized as a premium real-estate platform for Israel and international buyers. The operating model is not to avoid competitive money keywords. The operating model is to own the full real-estate market over time, with priorities, proof gates, and one canonical owner for every keyword.

This spec ties the existing strategy package into build-ready artifacts:

- `keyword-to-page-owner.csv` assigns every keyword row to one canonical owner.
- `current-evidence-register.csv` lists the evidence that can be trusted now and what still needs rechecking.
- `sprint-ready-backlog.csv` turns the strategy into work items with acceptance gates.
- `owner-output-index-rtl.html` gives the owner a readable Hebrew dashboard for this packet.

## Current Verified State

The WordPress repo is a block theme repo named `NadLan Revenue`. The current working branch for this war-room work is `strategy/nadlan-seo-product-war-plan`.

Current durable strategy assets already in the repo:

- 225 keyword rows in `strategy/04-keyword-master-universe.csv`.
- 39 page architecture templates in `strategy/war-room/page-architecture-map.csv`.
- 15 UX build surfaces in `strategy/war-room/ux-build-spec.csv`.
- 14 implementation-plan items in `strategy/implementation-plan.csv`.
- Current gap map in `strategy/war-room/full-war-room-gap-map.csv`.
- Lovable strategy-hub import in `handoff/lovable/2026-06-23-war-room-sync/`.
- Prototype public-language QA in `handoff/codex/2026-06-23-public-language-cleanup/`.

Known blockers that must not be hidden:

- Final Stage 1 public trust screenshots are still pending after UPress theme pull and cache clear.
- Official GSC, Semrush, legal, tax, and finance exports are not attached yet.
- Real production assets for contractor-grade project pages are missing for many surfaces, including 3D model assets, facade assets, floor plans, views, and verified project photography.
- The Lovable prototype is useful as design evidence, but it is not a production build and it used generic project images.

## Source Of Truth

The repo is the source of truth. Chat memory, Lovable memory, and agent claims are not source of truth unless the output is committed into the repo.

Cross-agent material must be placed under:

- `handoff/lovable/` for Lovable output.
- `handoff/codex/` for Codex output.
- `handoff/claude/` for Claude output when present.
- `handoff/shared-knowledge/` for reusable skills and shared rules.

The strategy folder is the execution source:

- `strategy/README.md` explains the packet.
- `strategy/war-room/` contains the current build map.
- `strategy/lovable/` contains prior Lovable research, screenshots, workbook, and reports.

## Keyword Ownership

File: `strategy/war-room/keyword-to-page-owner.csv`

This file is the anti-cannibalization backbone. Every keyword from Report 2 has:

- `keyword_id`
- exact keyword
- language
- cluster and subcluster
- suggested URL
- canonical page template
- exact canonical owner URL
- parent hub
- money or support role
- readiness state
- trust gate
- internal-link rule

Rules:

1. A writer or builder may not create a new page without checking this file first.
2. A support page links upward to its parent hub and the canonical money owner.
3. A money page receives links from support pages in the same cluster.
4. If a keyword needs a new route, update the page architecture map before drafting content.
5. No page should compete with the canonical owner in title, H1, slug, or primary internal anchor.

## Page Architecture

File: `strategy/war-room/page-architecture-map.csv`

The architecture has these active families:

- Home and primary navigation.
- Buying and rental hubs.
- City and neighborhood hubs.
- New projects and project detail pages.
- 3D showroom pages.
- Developer pages.
- Tools and calculators.
- Professionals.
- Urban renewal.
- International buyer pages.
- Trust and comparison pages.
- Glossary and answer-engine support.

This is not a small site. It is a long-range system for money pages, support pages, trust pages, tools, professionals, and international investor funnels.

## Listings UX

Source files:

- `strategy/war-room/ux-build-spec.csv`
- `strategy/10-listings-ux-spec.md`
- `strategy/war-room/sprint-ready-backlog.csv`

The listing experience must be materially better than common Israeli listing pages. Minimum requirements:

- Strong media area with real image or honest missing-media state.
- Search, filter, map/list, and city context without mobile overflow.
- Price, rooms, area, floor, freshness, verification, and asset completeness.
- Clear public labels for paid placement without leaking internal ranking language.
- Save, compare, WhatsApp/contact, and lead source tracking.
- Schema, canonical/noindex filter rules, breadcrumbs, and clean Hebrew copy.

The listing arm may not dominate navigation before supply is credible, but it must be architected as a full money-page system.

## Project And Showroom UX

Source files:

- `strategy/11-project-showroom-3d-spec.md`
- `strategy/war-room/ux-build-spec.csv`
- `handoff/lovable/2026-06-23-war-room-sync/exports/2026-06-23-nadlan3d-visual-qa.html`
- `handoff/codex/2026-06-23-public-language-cleanup/exports/public-language-cleanup-visual-qa.html`

The showroom goal is contractor-facing and investor-facing credibility:

- Project overview.
- Building or facade view.
- Apartment click.
- Apartment detail.
- View from the apartment when assets exist.
- Surroundings and map context.
- Floor plan.
- Interior tour or honest pending-state.
- Design/consulting lead path.
- WhatsApp, call, and inquiry routing.

No fake facade, fake apartment state, or silent fallback is allowed. If a real asset is missing, the UI must say that asset is pending and route the contractor or internal team to upload it.

## Visual Direction

The current visual direction is still not final. The useful direction from the Lovable prototype is:

- premium editorial spacing,
- Hebrew-first typography,
- calm cream and dark text contrast,
- product-first pages,
- mobile-first layout,
- strong project cards,
- explicit proof gates.

However, the prototype also showed issues that must not be copied into production:

- public copy leaked internal terms,
- some labels used English inside Hebrew UI,
- project photos were generic,
- the 3D asset state was not production truth,
- visual polish was not enough for a contractor sales meeting.

Every visual build slice must include saved screenshots and a short visual QA note.

## Evidence Register

File: `strategy/war-room/current-evidence-register.csv`

This file separates proof from assumption:

- Verified repo artifacts.
- Owner-readable HTML exports.
- Prototype evidence.
- Current-site evidence that still needs live recheck.
- Limitations and next verification actions.

Any future report must reference evidence by file path, not by vague memory.

## Backlog Execution Rule

File: `strategy/war-room/sprint-ready-backlog.csv`

Each sprint item includes:

- priority,
- workstream,
- source gap,
- dependencies,
- acceptance test,
- visual evidence required,
- SEO evidence required,
- analytics event,
- risk,
- rollback,
- owner gate.

No visual product work is considered done until screenshots exist for mobile and desktop and the screenshot has been reviewed for text leakage, overflow, asset truth, and professional polish.

## Admin War Room Target

The repo-based war room is the current source. The WordPress admin target is a future implementation:

- keyword registry,
- report library,
- screenshot gallery,
- implementation status,
- content gates,
- asset truth,
- owner decisions,
- writer workflow controls.

The admin war room should use custom post types or custom database tables only after the registry fields are stable. The current CSV and HTML outputs are the correct first layer.

## Next 10 Build Steps

1. Run final Stage 1 public trust screenshots after UPress pulls latest main and clears cache.
2. Review `keyword-to-page-owner.csv` and approve the canonical owner system.
3. Freeze all writing against the keyword owner map to prevent cannibalization.
4. Approve the first project/showroom build slice and required real assets.
5. Implement the showroom state model with honest asset truth.
6. Capture mobile and desktop screenshots for every showroom state.
7. Implement premium listing card and search foundation.
8. Capture listing screenshots and scan for public language leakage.
9. Implement the homepage authority and conversion redesign.
10. Build the WordPress admin war-room dashboard after the repo war-room files stabilize.

## Files Added In This Execution Layer

- `strategy/war-room/master-war-room-execution-spec.md`
- `strategy/war-room/keyword-to-page-owner.csv`
- `strategy/war-room/current-evidence-register.csv`
- `strategy/war-room/sprint-ready-backlog.csv`
- `strategy/war-room/owner-output-index-rtl.html`
- `strategy/war-room/owner-output-index-preview.png`

