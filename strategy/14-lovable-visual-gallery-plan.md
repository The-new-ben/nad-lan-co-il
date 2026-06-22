# Lovable Visual Gallery Plan

Purpose: use Lovable as a visual component sandbox without making it the source of truth.

Lovable project URL:

`https://lovable.dev/projects/a7493b94-2e46-4d38-9c6a-80dcf0905f45`

Important limitation: this URL is dynamic/authenticated from the agent environment. Any Lovable output that matters must be exported or copied into this repository. Do not rely on hidden Lovable memory.

## Goal

Create a static visual gallery that demonstrates the future NadLan product system before implementation:

- homepage.
- listings.
- project showroom.
- facade selector.
- selected apartment card.
- interior tour.
- map/lookaround.
- missing asset states.
- professional directory.
- Join Pro.
- guides/legal pages.
- international page variants.

## Design Foundation

Use:
- Heebo for UI/content.
- IBM Plex Mono for metrics/technical labels.
- brand blue `#1561D8`.
- ink `#0B0F14`.
- background `#F5F7FA`.
- success `#0E7C66`.
- warning `#B57700`.
- danger `#B5311B`.

Do not use Assistant as the primary font unless the whole design system is changed.

## Gallery Screens

| # | Screen | Purpose | Must show |
|---:|---|---|---|
| 1 | Homepage hero | national product entry | search, projects, tools, trust |
| 2 | Search results | listing UX | map/list, filters, real/missing inventory states |
| 3 | Listing card | card system | price, rooms, sqm, location, source, CTA |
| 4 | Project showroom hero | premium project page | 3D context + facade picker nearby |
| 5 | Facade selector | apartment selection | real/concept/missing asset states, polygons |
| 6 | Selected apartment | buyer decision card | facts, view, tour, contact |
| 7 | Interior tour | Homes/Matterport-style journey | iframe/tour/floor-plan/missing states |
| 8 | Map/lookaround | location intelligence | sea/park/context labels, failure state |
| 9 | Missing asset | honesty state | clear instruction, no fake facade |
| 10 | Price estimate | investor signal | non-binding disclaimer |
| 11 | Professional directory | marketplace | taxonomy, verification, trust |
| 12 | Join Pro | monetization | packages, benefits, no internal copy |
| 13 | Legal guide | E-E-A-T | byline, source dates, disclaimer |
| 14 | Foreign buyer | i18n | EN/FR/RU/AR direction variants |
| 15 | QA state board | internal review | viewport proof, status labels |

## Public Copy Rules

The gallery must be buyer/contractor-facing where public. Do not show:

- lead funnel.
- CRM.
- debug.
- internal QA text.
- fake official asset labels.
- fake availability.

## Asset State Labels

| State | Label |
|---|---|
| official | חומר רשמי מהיזם |
| concept | הדמיה מקורית להמחשה - לא חומר רשמי |
| missing | ממתין לחומר רשמי |
| error | התצוגה לא נטענה |

## Export Rules

If a Lovable output is good:

1. Export/copy it into repo under `docs/design/lovable/` or a future implementation branch.
2. Commit screenshots at 1440/768/390.
3. Record source prompt and date.
4. Do not deploy directly from Lovable.

## Acceptance Criteria

- Gallery is static and safe.
- No API keys/secrets.
- No product deployment.
- Screens match strategy tokens.
- Missing/concept/official states are visible.
- The gallery can guide implementation without becoming hidden source state.
