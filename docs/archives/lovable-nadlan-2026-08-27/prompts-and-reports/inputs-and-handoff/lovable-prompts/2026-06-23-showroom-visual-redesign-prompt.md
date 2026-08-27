# Prompt For Lovable: NadLan Showroom Visual Redesign And Prototype

You are working in the Lovable GitHub hub repository:

https://github.com/The-new-ben/nadlan-strategy-hub

You must push your output to GitHub.

Do not leave final work only inside `.lovable/`.
Do not output a thin Markdown-only report.
Do not claim completion without screenshots, prototype, design tokens, and a source manifest.

## Operating Mode And Credit Gate

This is a two-step Lovable run.

Step 1, before spending heavily:

- read the repo files listed below
- inspect the current public website
- capture/record what you inspected
- explain the exact intended scope
- explain which parts are high-credit/high-processing
- list the outputs you will create
- list any blocking questions
- then wait for the owner to write exactly: `PROCEED FULL RUN`

Step 2, only after the owner writes `PROCEED FULL RUN`:

- produce the full prototype, screenshots, reports, structured data, exports, and source manifest
- commit and push everything to GitHub

Do not begin the heavy prototype/screenshot generation until the owner confirms the full run.

## Required Output Folder

Create this exact folder at the root of the Lovable hub repo:

`handoff/lovable/2026-06-23-showroom-visual-redesign/`

Inside it, create:

```text
handoff/lovable/2026-06-23-showroom-visual-redesign/
  source-manifest.md
  reports/
  prototype/
  screenshots/
  exports/
  data/
  assets/
```

Commit and push to:

Repository:
`https://github.com/The-new-ben/nadlan-strategy-hub`

Branch:
`main`

After pushing, report the exact GitHub commit hash.

## Read First

Before designing, read the already synced handoff package:

```text
handoff/lovable/2026-06-23-war-room-sync/reports/plan.md
handoff/lovable/2026-06-23-war-room-sync/reports/00-strategy-brief.md
handoff/lovable/2026-06-23-war-room-sync/reports/01-showroom-redesign.md
handoff/lovable/2026-06-23-war-room-sync/reports/report-3a-real-semrush.md
handoff/lovable/2026-06-23-war-room-sync/reports/repo-inventory.md
handoff/lovable/2026-06-23-war-room-sync/reports/rest-api-map.md
handoff/lovable/2026-06-23-war-room-sync/reports/advisor-notes.md
```

Also read Codex's latest request package if present:

```text
handoff/codex/2026-06-23-showroom-redesign-readout.md
handoff/codex/2026-06-23-stakeholder-input-packet.md
handoff/codex/2026-06-23-source-context/README.md
handoff/codex/2026-06-23-source-context/source-manifest.md
handoff/codex/2026-06-23-source-context/data/repo-research-design-inventory.csv
handoff/codex/2026-06-23-source-context/data/qa-screenshot-inventory.csv
handoff/codex/2026-06-23-source-context/data/relevant-remote-branches.csv
handoff/codex/2026-06-23-source-context/data/skills-inventory.csv
handoff/codex/2026-06-23-source-context/skills/
handoff/shared-knowledge/README.md
handoff/shared-knowledge/skills/nadlan-cross-agent-sync.md
handoff/shared-knowledge/skills/nadlan-showroom-design-rules.md
handoff/codex/lovable-prompts/2026-06-23-showroom-visual-redesign-prompt.md
handoff/codex/exports/2026-06-23-showroom-redesign-next-lovable-prompt.html
handoff/codex/exports/2026-06-23-stakeholder-input-packet.html
```

The source-context folder contains prior Codex, Claude, and Lovable reports. Use it. Do not redesign from a thin prompt when this repo already contains historical research, design specs, QA screenshots, and branch signals.

Use the skill and shared-knowledge files as project memory. If you create reusable guidance, add it to:

```text
handoff/lovable/2026-06-23-showroom-visual-redesign/knowledge/
handoff/shared-knowledge/skills/
```

Commit those files to GitHub. Do not leave reusable skills only in Lovable chat or Lovable Knowledge UI.

Inspect the current public site:

```text
https://nad-lan.co.il
```

Capture current-state evidence before proposing the redesign:

- homepage desktop screenshot
- homepage mobile screenshot
- showroom/project page desktop screenshot if publicly reachable
- showroom/project page mobile screenshot if publicly reachable
- navigation/menu screenshot
- current contact/WhatsApp/dial CTA screenshot
- any map/facade/showroom failure state you can see

If a page is not reachable, record the exact URL tried and why it failed. Do not invent a screenshot.

Then use these WordPress repo facts as hard constraints:

- Source-of-truth repo: `https://github.com/The-new-ben/nad-lan-co-il`
- Active Codex branch: `strategy/nadlan-seo-product-war-plan`
- Current showroom renderer: `plugins/nadlan-config/inc/project-3d.php`
- Older theme-pattern showroom: `patterns/project-showroom-dimri-yama.php`
- Small brochure-level JS: `assets/js/nadlan-project-showroom.js`
- Showroom CSS: `assets/css/nadlan-project-showroom.css`
- Rainbow data: `assets/projects/rainbow-tel-aviv/`
- Dimri data: `assets/projects/dimri-yama/`

Important current reality:

- Rainbow is the technical reference: it has `model.glb`, poster, plans, environment, unit map, `hotspot_position`, and `camera_orbit`.
- Dimri has stronger sales/story material, but no real GLB. Treat it as a concept/official-facade fallback until contractor assets arrive.
- The current facade and Mapbox experience are not contractor-ready.
- The UI must be rebuilt mobile-first. No horizontal overflow. No fake stacked facades. No fake map. No generic brochure card.
- If an asset is missing, design a premium explicit missing-asset state and a contractor intake CTA.

## Mission

Produce an implementation-grade visual and UX package for the NadLan showroom redesign.

The first priority is the project showroom, because this is what sells contractors.

The wider website redesign matters, but do not spread yourself thin. Deliver a deep showroom package first, with enough sitewide design system and IA to prevent rework.

The listing arm exists but should not dominate the first public hierarchy until it is strong enough. The initial navigation and homepage should lead with premium projects, 3D/project showroom, investor confidence, foreign-buyer/investor support, and professional trust. Listings can be present as a system component, but not as the main promise if the inventory is not yet strong.

NadLan's ambition:

NadLan is not another Israeli listings board. It is the best new-project showroom and investor funnel in Israel, with SEO as the engine. It must serve:

- Israeli buyers
- international investors
- foreign buyers / Aliyah buyers
- contractors and developers who pay for premium exposure
- professionals who support the transaction

We compete across the whole Israeli real-estate market. Do not say a money keyword, listing type, or competitor area is irrelevant just because it is hard. Difficulty affects sequencing, not ambition.

This is not a leftover-keyword strategy.

The project showroom is the first premium wedge because it can sell contractors now, but the war-room architecture must cover the whole money market:

- new contractor projects
- second-hand apartments
- rentals where they support buyer/investor intent
- urban renewal, Tama 38, and Pinui Binui
- luxury real estate
- commercial real estate
- land, planning, and zoning intent
- mortgages and financing
- appraisal, inspection, law, tax, architecture, interior design, property management, and other professional services
- Israeli buyers investing abroad
- international buyers investing in Israel

Do not reject high-value keywords or categories because they are competitive. Classify them by role:

- direct money page
- project/listing page
- city or neighborhood hub
- professional/service page
- guide/support article
- comparison page
- lead qualification flow
- internal-linking support page

Competition difficulty only changes priority and sequencing. It does not remove the topic from the master universe.

Also include outbound investment markets for Israeli investors:

- Cyprus
- Dubai / UAE
- Greece
- Thailand
- additional destinations that clearly fit Israeli real-estate investment demand

For each outbound market, define the SEO architecture and the technical product model: country pages, city/project pages, 3D/project showroom eligibility, local professional network, FX display, tax/legal disclaimer, partner-intake workflow, and concierge lead routing.

Brand/name exploration is required.

The owner says "Nadlan Chakam" appears occupied, so do not assume it is available. Explore premium, credible naming directions such as NadLan AI, NadLan 3D, NadLan Pro, NadLan Global, or stronger alternatives. Check naming fit for Hebrew, English, foreign investors, contractors, SEO, favicon/logo, and legal/domain/social availability risk. Do not make a legal claim; give a shortlist and what must be checked.

## External Benchmarks To Research

Research current product patterns. Do not copy visuals directly. Extract mechanisms.

Use at minimum:

- Zillow 3D Home and interactive floor plans
- Homes.com + Matterport listing/tour experience
- Matterport real-estate digital twins, floor plans, and property marketing
- Mapbox real-estate maps and 3D basemap patterns
- JamesEdition luxury real-estate trust/presentation
- OnTheMarket listing detail structure
- Madlan/Yad2/Homeless Israeli search expectations
- model-viewer official hotspot and camera controls
- Israeli investor-abroad real-estate pages for Cyprus, Dubai/UAE, Greece, and Thailand
- professional-service funnels around real-estate transactions: lawyers, mortgage advisors, appraisers, inspectors, architects, interior designers, tax advisors, and property managers

Design implications to carry forward:

- Zillow: 3D tours and floor plans should be part of the listing decision flow, not a decorative media tab.
- Homes.com/Matterport: tours, floor plans, revisiting rooms, and sharing are core buyer behaviors.
- Mapbox: the map should carry context, 3D buildings, landmarks, lighting, and project surroundings when token/data are available.
- model-viewer: unit selection must drive `camera-orbit`, `camera-target`, and hotspot focus.
- Israeli SEO: money pages and project pages must have clear Hebrew commercial intent, not internal product language.

## Required Prototype

Build a working Lovable/TanStack/React prototype inside the Lovable repo under:

`handoff/lovable/2026-06-23-showroom-visual-redesign/prototype/`

It must be usable in Lovable preview and must include realistic mock data for:

1. Rainbow Tel Aviv
2. Dimri Yama
3. Urban-renewal / Tama 38 pilot

The prototype must implement these screens/states:

1. Mobile initial showroom, 390px wide.
2. Mobile floor picker bottom sheet.
3. Mobile unit selected state.
4. Mobile unit detail drawer with tabs: plan, interior tour, view, surroundings, AI advisor.
5. Mobile view-from-apartment / map context state.
6. Mobile lead/WhatsApp/concierge state.
7. Desktop showroom, 1440px wide.
8. Contractor pitch view: what a developer sees and why they pay.
9. International investor mode: English copy, FX, tax/legal disclaimer, concierge.
10. Asset-missing state: no GLB, no facade, no Mapbox token, no Matterport URL.

This prototype must not be a static card gallery. It must have functional controls:

- project switcher
- floor selector
- unit selector
- bottom sheet open/collapse
- tabs
- compare units
- save/share state
- WhatsApp/lead modal state
- language toggle HE/EN
- FX toggle NIS/USD/EUR/GBP
- AI advisor panel with realistic suggested prompts and non-binding disclaimers
- map/token missing state
- contractor asset-intake state

Use real available assets by URL when possible:

- Rainbow model: `https://raw.githubusercontent.com/The-new-ben/nad-lan-co-il/main/assets/projects/rainbow-tel-aviv/model.glb`
- Rainbow poster: `https://raw.githubusercontent.com/The-new-ben/nad-lan-co-il/main/assets/projects/rainbow-tel-aviv/rainbow-showroom-hero-v1664.jpg`
- Rainbow plans under `assets/projects/rainbow-tel-aviv/plans/`
- Dimri available assets under `assets/projects/dimri-yama/`

If an asset cannot be loaded, do not fake it. Render the premium missing-state component.

## Visual Direction

The current dark/gold look is not enough. Create a real premium Israeli/international real-estate product system.

Avoid:

- generic black/gold luxury template
- one-note navy/gold palette
- huge brochure cards
- fake decorative facades
- text-heavy first screen
- internal admin language on public pages
- placeholder rectangles as final assets
- weak CTA hierarchy
- mobile overflow

Aim for:

- precise, quiet premium product UI
- large visual stage
- clear one-thumb mobile path
- investor confidence
- official/prototype/missing asset transparency
- multilingual readiness
- contractor-grade trust
- dense but scannable decision data

Use iconography, not text pills where icons are better. Prefer lucide icons for:

- Building2
- Layers3
- Map
- Sun
- Compass
- Eye
- Ruler
- Home
- DoorOpen
- MessageCircle
- Bot
- Share2
- Heart
- Globe2
- Banknote
- FileText
- ShieldCheck
- CalendarClock
- Users

## Required Design Outputs

Create these files:

```text
reports/02-design-system.md
reports/08-showroom-visual-redesign-spec.md
reports/09-sitewide-brand-seo-ux-system.md
reports/10-wordpress-war-room-dashboard-spec.md
reports/11-codex-implementation-backlog.md
reports/12-full-market-money-keyword-expansion.md
reports/13-international-investment-expansion.md
reports/14-stakeholder-input-packet.md
```

Each report must be practical and implementation-grade.

`02-design-system.md` must include:

- brand thesis
- brand/name options and recommendation
- typography system for Hebrew and English
- color tokens
- spacing tokens
- radius/elevation tokens
- status colors
- icon system
- favicon/OG direction
- logo mark direction
- RTL/LTR rules
- accessibility rules
- component inventory
- exact CSS variable names

`08-showroom-visual-redesign-spec.md` must include:

- exact layout at 390, 768, 1440
- state machine
- screen-by-screen behavior
- bottom sheet behavior
- right rail behavior
- map behavior
- view-from-apartment behavior
- interior/tour behavior
- lead modal behavior
- AI advisor behavior
- asset fallback behavior
- copy for all major UI states in Hebrew and English
- implementation notes for `project-3d.php`

`09-sitewide-brand-seo-ux-system.md` must include:

- homepage direction
- project page direction
- intelligent listing page direction
- current listing-arm hierarchy recommendation: visible but not primary until inventory is stronger
- professionals page direction
- foreign buyer pages
- city money pages
- neighborhood pages
- article/guide pages
- menus and navigation
- page headline formulas
- schema/SEO notes
- internal linking rules
- external link acquisition strategy: who to get links from, why they would link, and which pages should receive authority
- no-cannibalization rules
- anti-cannibalization source-of-truth workflow so agents and writers do not damage money pages

`10-wordpress-war-room-dashboard-spec.md` must specify the WordPress admin dashboard for the owner:

- agent sync status: Lovable/Codex/Claude
- latest commits and imported reports
- report viewer
- prompt queue
- keyword source of truth
- cannibalization guard
- showroom readiness checklist per project
- asset completeness matrix
- SEO page backlog
- content approval workflow
- contractor package pipeline
- contractor-facing premium dashboard / demo experience
- contractor onboarding and asset-intake workflow
- international destination pipeline
- professional vertical pipeline
- lead/concierge ops status
- export buttons
- AI drafting tools with approval gates
- WhatsApp/call/email CTA health and routing overview

`11-codex-implementation-backlog.md` must be a precise build plan for Codex:

- files likely touched
- order of implementation
- risks
- acceptance tests
- mobile QA checklist
- public trust checklist
- what not to touch yet
- technical split between theme, child theme, plugin, data files, REST, admin dashboard, and public assets
- specific notes for `plugins/nadlan-config/inc/project-3d.php`, `assets/css/nadlan-project-showroom.css`, `assets/js/nadlan-project-showroom.js`, and project asset folders

`12-full-market-money-keyword-expansion.md` must prove that the strategy is not avoiding the market:

- complete Israeli real-estate keyword universe by commercial intent
- money-page/support-page split
- listing/project/professional/guide/page-type mapping
- cannibalization rules for overlapping topics
- examples of Hebrew public H1s and SEO titles
- what should be built now, next, later, and why
- explicit note: "hard keyword" means phased, not excluded

`13-international-investment-expansion.md` must cover Israeli outbound investment and international inbound buyers:

- Israel inbound: English and other foreign-buyer flows
- outbound: Cyprus, Dubai/UAE, Greece, Thailand, and additional justified markets
- country/city/project page structure
- project showroom applicability by destination
- currency and language behavior
- professional network requirements per destination
- legal/tax/mortgage disclaimer approach
- partner-intake and verification workflow
- technical implementation options in WordPress
- whether each market needs projects, guides, partner pages, local professional pages, or 3D showroom support first

`14-stakeholder-input-packet.md` must prepare the owner to call the relevant business/technical stakeholder:

- exact questions to ask the stakeholder
- asset questions: GLB, facade, plans, Matterport/Cupix, photos, drone, map coordinates
- business questions: contractor packages, lead routing, commission model, exclusivity, service providers
- technical questions: WordPress plugin path, data model, API needs, Mapbox token, hosting/performance, multilingual setup
- decision table: what the stakeholder's answers change in the build plan
- call summary template to paste back into the war room

## Required Data Files

Create:

```text
data/design-tokens.json
data/showroom-state-machine.json
data/showroom-component-contracts.json
data/page-architecture-screen-matrix.csv
data/keyword-page-support-map.csv
data/asset-readiness-matrix.csv
data/full-market-keyword-universe.csv
data/international-destination-page-map.csv
data/professional-verticals-map.csv
data/stakeholder-input-checklist.csv
data/brand-name-options.csv
data/current-site-screenshot-inventory.csv
data/link-acquisition-targets.csv
```

These must be usable by Codex. Do not bury structured data only in prose.

## Required Visual Outputs

Create screenshots from the prototype:

```text
screenshots/showroom-mobile-390-initial.png
screenshots/showroom-mobile-390-unit-selected.png
screenshots/showroom-mobile-390-view-map.png
screenshots/showroom-mobile-390-ai-advisor.png
screenshots/showroom-tablet-768.png
screenshots/showroom-desktop-1440.png
screenshots/showroom-asset-missing-state.png
screenshots/war-room-dashboard-admin.png
```

Also create owner-readable exports:

```text
exports/showroom-redesign-owner-readable-he-rtl.html
exports/showroom-redesign-codex-handoff.html
```

The owner-readable HTML must be readable in a browser, right-to-left where Hebrew appears, and must include images/screenshots inline.

## AI And Intelligence Requirements

Design NadLan as an intelligent listing/showroom platform.

Include:

- AI buyer/investor assistant
- unit comparison assistant
- interior design advisor
- financing/mortgage next-step advisor
- legal/tax explainer gateway with disclaimers
- foreign-buyer concierge intake
- AI content drafting inside WordPress admin, but with human approval before publishing
- lead qualification summary
- suggested follow-up messages for WhatsApp/email
- polished WhatsApp, call, save, share, and concierge CTAs as one coherent contact system

Do not present AI as legal, tax, mortgage, or investment advice. It is a guided assistant and lead qualification layer.

## SEO And Copy Requirements

Write public copy, not internal strategy copy.

Required public language examples:

- Hebrew default for Israeli buyers.
- English mode for international investors.
- No internal phrases like "money page", "KD", "war room", "contractor monetization" on public pages.
- Use commercial-intent headlines that match search behavior.

For the showroom page, include:

- SEO title formula
- meta description
- H1
- opening paragraph
- project trust block
- unit selector microcopy
- floor selector microcopy
- view/map microcopy
- interior/tour microcopy
- AI assistant microcopy
- lead CTA copy
- FAQ schema questions
- internal links to city, neighborhood, new projects, guides, professionals

## Asset Rules

Do not fake facades.

Use this asset policy:

1. If real GLB exists: model-first with hotspot/unit controls.
2. If official or concept facade exists: facade-first, visibly labeled as official/concept/prototype.
3. If neither exists: no fake visual. Show premium missing-asset state and contractor intake checklist.
4. If Mapbox token/data is missing: show a designed not-ready map state; do not pretend the map is live.
5. If Matterport/Cupix URL is missing: show tour-missing state and contractor asset request.

## Acceptance Gates

This run is not complete unless all of these are true:

- The prototype runs in Lovable preview.
- Screenshots exist for mobile/tablet/desktop.
- No mobile horizontal overflow at 390px.
- Text fits buttons/cards.
- Controls visibly work.
- Design tokens exist as JSON.
- Component contracts exist as JSON.
- Owner-readable HTML exists.
- Codex implementation backlog exists.
- `source-manifest.md` records source repo, branch, commit, and file list.
- The work is committed and pushed to `https://github.com/The-new-ben/nadlan-strategy-hub`.
- The package does not exclude money categories because they are hard or competitive.
- Cyprus, Dubai/UAE, Greece, Thailand, inbound foreign buyers, and Israeli professional-service verticals are mapped into the page architecture and data files.

## Credit Discipline

Do one focused high-quality run.

Do not spend credits expanding endlessly into every possible website page. For this run:

1. Fully design and prototype the showroom.
2. Produce the sitewide system/SEO/war-room dashboard specs at implementation level.
3. Leave deeper coded prototypes for listings/professionals/homepage to the next run unless you finish the showroom package first.

Quality standard:

If the output is mostly prose, it failed.
If there are no screenshots, it failed.
If Codex cannot start implementation from the files, it failed.
