# A0 - Source Registry And Gap Audit

## Source Registry

| Source | What it contains | How it affects strategy | Status | Risk if ignored | Next action |
|---|---|---:|---|---|---|
| Live site `nad-lan.co.il` | Public WordPress pages, projects, professionals, guides, UI leaks, actual page state | Ground truth for what buyers and Google see | PARTIAL | Strategy targets non-existent or stale pages | Run crawler + screenshot QA after every deploy |
| Live healthcheck | Plugin version, features, lead state, Mapbox/token presence, project_3d flags | Confirms plugin runtime and deployed version | VERIFIED | Confusing merged code with live code | Check before and after every plugin deploy |
| GitHub repo | Theme, plugin, scripts, skills, docs, QA artifacts | Source of truth for code and agent memory | VERIFIED | Repeating stale branch/temp-folder mistakes | Always branch from `origin/main` |
| Lovable project | Visual/product planning workspace at provided URL | Input/output staging for strategy and gallery work | PARTIAL | Lovable memory becomes hidden source | Copy every useful output into repo |
| `docs/codex-handoff/` | Transfer packet for new Codex instance | Engineering continuity | VERIFIED | New PC repeats old state confusion | Read before any new PC work |
| `COORDINATION.md` | Agent billboard, current/past plans, mistakes, specs | Coordination memory | PARTIAL | "NOW" may be stale | Verify with Git/live before trusting |
| `skills/skill-release-discipline-and-mistakes.md` | Release mistakes, plugin rules, no silent fallback | Prevents repeat breakage | VERIFIED | Server/plugin damage | Read before plugin or showroom work |
| `skills/project-page-premium-showroom-runbook.md` | Project showroom DNA, model/facade rules, fields, QA | Governs Rainbow/Dimri/project clone work | VERIFIED | Fake showroom, bad mobile, bad copy | Apply before every project page |
| `scripts/qa-stage1-public-trust.mjs` | Screenshot/DOM public trust QA for key pages | Stage 1 gate | VERIFIED | Trust leaks stay invisible | Run after theme pull |
| Stage 1 screenshots | Before/after evidence for trust cleanup | Baseline and regression proof | PARTIAL | Claims without visual proof | Generate final screenshots after UPress pull |
| Existing project CPT records | Rainbow, Dimri, other project data | Project spoke base | PARTIAL | Project pages lack canonical data | Export current project meta |
| Existing content clusters | Sde Dov, Ramat Aviv, Bat Yam, guides, glossary | SEO base and internal links | PARTIAL | Cannibalization or thin pages | Build canonical page registry |
| Keyword foundation reports | Previous keyword ideas, Report 2 foundation | Starter universe only | PARTIAL | Mistaking seed list for full universe | Expand to 1500-3000 rows |
| SERP blueprint skills | Manual Google SERP reverse-engineering workflow | Method for content creation | VERIFIED | Generic AI content | Use before every money page |
| Semrush/GSC | Volume, KD, queries, CTR, impressions, cannibalization | Prioritization and proof | MISSING | Fake data and wrong priorities | Export or connect before final numbers |
| Live Google SERP | Titles, snippets, competitors, PAA, intent, ads | Real ranking blueprint | NEEDS_VERIFICATION | Wrong page type | Manual SERP scans per term |
| Official sources | Gov, municipalities, developers, tax, planning | Trust and legal safety | PARTIAL | Unsupported public claims | Source every number |
| Design system | Tokens and UX principles | Visual consistency | PARTIAL | Cheap/WordPress look | Build component gallery |
| Project assets | GLB, facade, poster, tours, floor plans | Showroom credibility | PARTIAL | Fake facade/false promises | Asset provenance registry |
| CRM/lead routing | Lead CPT, WhatsApp, lead e2e, AI qualify | Monetization | PARTIAL | Leads go nowhere | Define lead payload and SLA |
| Legal/compliance | Outreach, broker, tax/legal advice, privacy | Risk control | PARTIAL | Spam/privacy/false claim exposure | Legal review checklist |

## What We Have

- WordPress content layer and custom block theme.
- `nadlan-config` plugin with live healthcheck and project_3d runtime.
- Public trust QA harness.
- A strong mistake catalog: no fake facade, no silent fallback, no poisoned ZIP.
- Project showroom concepts for Rainbow and Dimri.
- Some project pages and Sde Dov content foundation.
- Lead capture and routing infrastructure.
- A real repo history with screenshots, specs, and QA files.
- A Lovable project URL for visual/planning work.

## What We Do Not Have

- Full 1500-3000 keyword universe with volume/KD/CPC.
- GSC query export and cannibalization proof.
- Live SERP reverse-engineering for the top 100 money terms.
- A final canonical page registry accepted as the publishing law.
- A production-quality visual component gallery.
- Real map/list listing product.
- Real official Dimri/Rainbow BIM and per-unit geometry.
- Official facade/elevation assets for most projects.
- Home.com/Matterport-style interior journey with real media.
- Developer dashboard and self-service asset upload.
- Full CRM/lead assignment SLA.
- International URL/hreflang architecture.

## Strategic Correction

NadLan is not avoiding hard categories because competitors are strong. The correct logic is:

- Compete long-term for the most commercial terms.
- Stage only when product, data, legal, source, or supply readiness is missing.
- Never ship a doorway/thin/fake page just to have a URL.

## Priority Ladder

### P0

- Public trust gate.
- Homepage strategy.
- New-projects money cluster.
- Project showroom credibility.
- Keyword/page registry.
- 3D tiered MVP.
- CRM lead routing.
- Source-of-truth and cannibalization control.

### P1

- Listings shell.
- Top city pages.
- Top professional pages.
- Content plan.
- Design gallery.

### P2

- Programmatic city/neighborhood scale.
- Suppliers/contractors.
- AEO/AI answer layer.
- English foreign-investor bridge.

### P3

- Full app layer.
- Full international.
- Advanced Cesium/Google 3D view.
- Investor dashboard.

## Required Next Reports

1. A1 Keyword/SERP Master Expansion.
2. A2 SERP Reverse Engineering Top 100.
3. A3 Canonical Page Registry.
4. A4 Homepage + Visual Product Board.
5. A5 Listings UX/Product Spec.
6. A6 Project Showroom + 3D Technical Build Spec.
7. A7 CRM/Lead Engine + Monetization.
8. A8 International/i18n.
9. A9 Agent Execution OS + QA.
