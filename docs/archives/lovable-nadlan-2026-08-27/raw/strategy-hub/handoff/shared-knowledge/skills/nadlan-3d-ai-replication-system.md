# NadLan 3D AI Replication System

Status: active

Date: 2026-06-23

Use this whenever NadLan, Codex, Lovable, Claude, or another agent needs to repeat the current 3D/AI real-estate website process on NadLan or another WordPress site.

## Goal

Create a repeatable A-to-Z system for turning a WordPress real-estate site into a premium 3D/AI product platform:

- investor-ready showroom
- project and apartment listing experience
- multilingual SEO architecture
- design system
- contractor intake and monetization model
- AI concierge and guided buying flow
- owner-readable reports and screenshots
- repo-synced handoff folders

Lovable may be used for prototype acceleration, but the process must work without Lovable.

## Required Repository Structure

Every target WordPress repo should use:

- `handoff/codex/<date>-<project>-source-context/`
- `handoff/lovable/<date-or-run>/` when Lovable is used
- `handoff/claude/<date-or-run>/` when Claude is used
- `handoff/shared-knowledge/skills/`
- `handoff/shared-knowledge/decisions/`
- `handoff/shared-knowledge/indexes/`

Do not leave important decisions only in chat.

## Workflow

1. Bootstrap the workspace.
   - Create the `handoff/` structure and a `source-manifest.md`.
   - Record repo URL, branch, public site URL, languages, source commits, and read order.

2. Inventory before designing.
   - Scan reports, prompts, branches, screenshots, themes, plugins, routes, REST endpoints, assets, and menus.
   - Capture public site screenshots on mobile and desktop.
   - Record prior agent outputs from Codex, Lovable, Claude, `.lovable/`, and any report folders.

3. Build an asset-truth matrix.
   - GLB models, facade SVGs, floor plans, render images, maps, interior tours, icons, logo, favicon, Open Graph images.
   - Mark each as real, reused, placeholder, missing, or contractor-required.
   - Do not fake maps, facades, Matterport/Cupix tours, tax/legal advice, or official plans.

4. Define product architecture.
   - Showroom: project identity, 3D/facade stage, apartment click, view, surroundings, floor plan, interior tour, AI design, consultant, lead.
   - Listings: premium cards, filters, map/list behavior, paid labels, ranking hierarchy, empty/loading/error states.
   - Sitewide IA: home, projects, cities, guides, professionals, foreign-buyer pages, about, contact, contractor intake.
   - War room: admin or owner-facing dashboard for reports, keyword ownership, implementation status, screenshots, and decisions.

5. Define SEO and language architecture.
   - One canonical owner per money keyword.
   - Supporting pages link to money pages without cannibalizing them.
   - Include canonical, hreflang, schema, breadcrumbs, sitemap, noindex, and internal-linking rules.
   - Hebrew first where relevant, complete English for international investors, future language backlog documented.

6. Define design system.
   - Brand direction, typography, color tokens, icons, favicon, motion, components, responsive behavior.
   - Explain why each design choice fits contractors, Israeli buyers, foreign investors, and premium project marketing.
   - Include RTL/LTR rules and mobile 390px acceptance.

7. Prototype or implement.
   - If using Lovable, require committed files, reports, screenshots, and manifest updates.
   - If using Codex directly, implement in the WordPress theme/plugin structure and verify with browser screenshots.
   - Do not accept a one-viewport demo or a decorative mock that hides broken assets.

8. Package for the owner.
   - Commit durable outputs.
   - Create owner-readable HTML for important reports.
   - State what exists, what is missing, what is real, and what must be built next.

## Minimum Output Contract

Each full project run should produce:

- source manifest
- repo/public-site inventory
- asset-truth matrix
- keyword ownership map
- page IA and route map
- showroom state machine
- listings ranking and transparency rules
- design tokens and component inventory
- multilingual SEO plan
- WordPress implementation backlog
- owner-readable HTML export
- mobile and desktop screenshots
- shared skills or playbooks for future agents

## Current NadLan References

- `handoff/shared-knowledge/skills/nadlan-cross-agent-sync.md`
- `handoff/shared-knowledge/skills/nadlan-showroom-design-rules.md`
- `handoff/codex/2026-06-23-source-context/README.md`
- `handoff/codex/2026-06-23-lovable-locked-build-scope.md`
- `handoff/codex/lovable-prompts/2026-06-23-showroom-visual-redesign-prompt.md`

## Local Codex Skill

Codex now also has a local reusable skill:

`nadlan-3d-ai-replication`

It includes a bootstrap script that can initialize the same `handoff/` structure for future WordPress real-estate projects.

