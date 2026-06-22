# NadLan War Room OS

Date: 2026-06-22
Branch: `strategy/nadlan-context-reset-war-room-os`
Mode: strategy/reset only. No product code, no deploy.

## Purpose

This folder is the operating system for turning NadLan from a set of WordPress/plugin experiments into a governed real-estate portal build plan.

It exists because previous runs produced partial reports, browser outputs, and implementation attempts without a single source of truth. From now on, agents start here before writing product code.

## Current Project Links

- Live site: https://nad-lan.co.il
- Lovable project: https://lovable.dev/projects/a7493b94-2e46-4d38-9c6a-80dcf0905f45
- Repo: https://github.com/The-new-ben/nad-lan-co-il
- Live healthcheck: https://nad-lan.co.il/wp-json/nadlan/v1/healthcheck

## Read Order

1. `00-source-registry.md`
2. `01-gap-audit.md`
3. `02-keyword-serp-master.md`
4. `03-serp-reverse-engineering.md`
5. `04-canonical-page-registry.md`
6. `05-homepage-visual-product-board.md`
7. `06-listings-ux-product-spec.md`
8. `07-project-showroom-3d-build-spec.md`
9. `08-crm-lead-engine-monetization.md`
10. `09-international-i18n.md`
11. `10-agent-execution-os.md`
12. `11-implementation-backlog.md`
13. `12-qa-gates.md`
14. `13-risk-register.md`
15. `14-lovable-visual-gallery-plan.md`
16. `lovable/README.md`

Then read the backlog slices under `strategy/backlog/`.

## Status Labels

Use these labels exactly:

- `VERIFIED` - checked in repo, live site, official source, or committed QA artifact.
- `PARTIAL` - some evidence exists but not enough for build/publish.
- `NEEDS_VERIFICATION` - requires Semrush, GSC, live SERP, crawler, or manual source check.
- `ASSUMPTION` - logical inference not yet verified.
- `LEGAL_REVIEW` - legal/privacy/consumer/broker/financial risk.
- `REQUIRES_OFFICIAL_ASSET` - needs official developer/municipal/project asset.
- `OFFICIAL_SOURCE_REQUIRED` - number or claim requires official/public source.

## Immediate Priority

P0 is not "write more pages." P0 is:

1. Public trust gate.
2. Keyword/page source-of-truth registry.
3. Homepage strategy and project entry.
4. New-projects/project-showroom credibility.
5. CRM/lead payload and routing.
6. QA gates with screenshots.

## Hard Rules

- No product code from this branch.
- No deploy from this branch.
- No fake facade.
- No silent fallback.
- No dead buttons.
- No internal public copy.
- No Semrush/GSC numbers invented.
- No "competitor is too strong so surrender" reasoning.
- Every page has one source-of-truth keyword.
- Every build task has acceptance criteria and screenshot QA.

## What This Is Not

This is not the final Semrush/GSC export, not a full crawl, and not a live SERP scrape. It is the control system that tells the next agents exactly what must be researched, built, verified, and blocked.
