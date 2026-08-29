# EcoCity pilot for nad-lan.co.il

Repository-ready research, content and product specification for two flagship project pages:

- Stricker 13–Brandeis 14, Tel Aviv
- Bnei Dan 54–56, Tel Aviv

Research cut-off: 2026-08-28 (UTC)

## Non-negotiable scope

This package is a draft and implementation specification only. It does not authorize a live-site change, publication, deletion, redirect, lead delivery, or use of third-party media. Claude must work locally on a new branch and stop before any push, deploy or WordPress mutation.

The pages are independent editorial/product pages by nad-lan.co.il. Unless a written commercial relationship is approved, the project pages must not imply that nad-lan.co.il is EcoCity’s official site, exclusive sales agent, partner or authorized representative.

## Package map

| Path | Purpose |
|---|---|
| `governance/fact-register.csv` | Claim-level truth register, state, source and publication rule |
| `governance/blockers-and-required-inputs.md` | Contradictions, unsafe live claims and developer inputs needed |
| `governance/media-rights-ledger.csv` | Empty approval ledger; no asset may render until a complete row is approved |
| `content/*/source-of-truth.he.md` | Canonical Hebrew editorial source for each project |
| `content/*/content.he.json` | Machine-readable Hebrew content draft; no inventory or prices |
| `localization/adaptation-matrices.md` | English, French, Russian and Arabic adaptation by audience and section |
| `product/page-and-3d-spec.md` | Page architecture, location modules, media, 3D, buyer journey, forms and conversion |
| `product/schema-and-measurement.md` | Conditional structured data, analytics contract and privacy rules |
| `product/benchmark-patterns.md` | Focused patterns from leading international project sites |
| `qa/green-gates.md` | Aurelia-aligned pre-merge and pre-publication green gates |
| `qa/validation-report.md` | Executed package checks and deliberately non-green dependencies |
| `claude-local-handoff.md` | Exact local implementation brief for Claude |
| `sources/source-ledger.md` | Source ledger with URLs and access notes |
| `schemas/project-content.schema.json` | Validation schema for the two JSON content records |
| `qa/validate-package.mjs` | Dependency-free package, schema, fact-ID and rights-ledger validator |

## Truth states

- `VERIFIED_PRIMARY`: supported by the project owner/developer or an official authority and fit for carefully attributed use.
- `TIME_SENSITIVE`: supported now but must be refreshed before preview and again before publication.
- `DEVELOPER_CLAIM`: first-party marketing statement that must be presented as the developer’s claim, not as an independent guarantee.
- `SECONDARY_CONFIRM`: discovered in a non-primary source; do not publish until the developer, architect or authority confirms it.
- `CONFLICT`: sources disagree; suppress the field.
- `MISSING`: no reliable evidence obtained; leave absent or show “contact for current information,” never a fabricated value.
- `BLOCKED_RIGHTS`: the content may exist, but the right to reuse or transform it was not established.

## Implementation principle

The public page must be useful with JavaScript disabled and without the 3D viewer. The viewer, apartment selector, view simulator and live inventory are progressive enhancements. No number is rendered from a design mockup, old page, search snippet or model label. Every rendered project fact must resolve to a current fact-register entry or an approved developer feed.

Run `node qa/validate-package.mjs` from the package root before handoff. This validates the content records against the bundled schema, checks CSV structure and fact references, and confirms that blocked inventory, price, coordinates and media remain empty.
