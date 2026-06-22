# Canonical Page Registry

Purpose: prevent keyword cannibalization, thin pages, and "many pages doing the same job." Every important URL must own one primary intent.

## URL Grammar

| Page type | Canonical pattern | Notes |
|---|---|---|
| Homepage | `/` | brand, national portal, trust, search entry |
| Buy listings | `/buy/` | future listing inventory, not fake inventory |
| Rent listings | `/rent/` | future rental inventory |
| Projects hub | `/projects/` | all new projects |
| Project page | `/projects/{project-slug}/` | project name owns query |
| District hub | `/{district-slug}/` or `/districts/{slug}/` | Sde Dov currently top-level `/sde-dov/` |
| City | `/cities/{city}/` | city intent |
| Neighborhood | `/cities/{city}/{neighborhood}/` | local intent |
| Tools | `/tools/{tool}/` | calculator/tool query |
| Guides | `/guides/{slug}/` | informational |
| Professionals | `/professionals/` and `/professionals/{slug}/` | marketplace |
| Join Pro | `/join-pro/` | B2B monetization |
| International | `/en/...`, `/fr/...`, `/ru/...`, `/ar/...` | hreflang required |

## Canonical Rules

1. One page, one primary query.
2. Project pages lead with project name, not the district query.
3. District hubs own the district and compare projects.
4. City pages own the city; neighborhood pages own the local sub-intent.
5. Tools own functional queries and link to legal/investor articles.
6. Foreign-language pages are not direct machine copies. They must match the foreign investor intent.
7. If a page has no real content or no real data, keep it draft/noindex until ready.

## Registry

The CSV version is `strategy/04-canonical-page-registry.csv`. Treat that CSV as the working table for agents and exports.

## Known Immediate Cannibalization Risks

| Risk | Cause | Fix |
|---|---|---|
| Rainbow vs Sde Dov hub | both may overuse "שדה דב" | Rainbow title/body must lead with "Rainbow Tel Aviv"; Sde Dov hub owns district |
| Dimri vs Sde Dov hub | project page may become district article | Dimri owns project-specific facts, developer, units, showroom |
| City/listing pages | future listings may duplicate project pages | listing pages are inventory; project pages are developer/new-project content |
| Legal guides | many articles can target purchase tax | one canonical purchase-tax pillar; spokes link back |
| International pages | EN/FR/RU/AR duplicate Hebrew | each language must have unique buyer context, currency/legal notes, hreflang |

## Page States

| State | Meaning | Public behavior |
|---|---|---|
| `LIVE_CANONICAL` | page is public and owns query | index |
| `LIVE_SUPPORTING` | useful but not primary | index if unique |
| `DRAFT` | not public | noindex or unpublished |
| `NEEDS_REWRITE` | public but thin/leaky | fix before expansion |
| `NOINDEX_UTILITY` | useful to users, not search | noindex |
| `REQUIRES_OFFICIAL_ASSET` | showroom media missing | show missing/concept state |
| `LEGAL_REVIEW` | legal/price/tax claims need approval | do not publish definitive claims |

## Minimum Fields Per Registry Row

- URL
- Page type
- Primary keyword
- Secondary keywords
- Audience
- Funnel stage
- Canonical role
- Internal links in/out
- Schema type
- Required source data
- Current status
- Next action
- Owner
