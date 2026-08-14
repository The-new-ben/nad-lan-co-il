# Existing Hebrew RECANATI RESIDENCE page - content audit

Audit date: 5 August 2026

Scope: read-only audit of https://nad-lan.co.il/projects/recanati-residence/. The user instructed that the Hebrew page remain untouched.

## Editorial verdict

The page is centered on the wrong neighborhood and wrong lifecycle. Its current official identity is a completed urban-renewal project in Ramat Aviv Gimel with immediate occupancy, not a future Neve Avivim project and not a Sde Dov project.

## Identity and fact errors

- Current title and H1 use `נווה אביבים`. Current first-party evidence uses Ramat Aviv Gimel.
- Current copy uses Ashdar as if it were the current brand. Ashdar changed its name to Ashtrom Residences in February 2025. Historical references may still say Ashdar, but public current copy should reconcile the names.
- The page does not clearly lead with the completed/occupied reality and immediate-occupancy status.
- Current price and current unit inventory are not established by a dated official unit sheet.
- A single exact current street entrance is not established by the current official page.
- The project-level existence of underground parking does not prove a parking allocation for a particular apartment.

## Generic and Sde Dov leakage

The embedded showroom record exposes zero floors, an empty unit array, zero average price, a generic model flag and a concept-facade flag. Despite that absence of real project-unit data, the public UI exposes apartment selection, design studio, facade controls and a standard tour.

Visible content includes Sde Dov and sea labels, a Sde Dov footer link, a Sde Dov design route, a generic standard residential model and generic apartment scenes. None of these proves a Recanati apartment, building, view or floor.

The page also shows Sde Dov project comparisons and unsupported internal price estimates for other projects. These are not valid Recanati comparables without a dated transaction method.

## Crawl and public-copy problems

- Generic engine copy appears before the real article and before the useful project facts.
- The first crawlable content includes false Sde Dov and sea wording.
- The real H1 arrives late, while an identical title appears earlier as an H2.
- One H2 is empty.
- Jump-navigation placeholders such as `פרק 2`, `פרק 3` and `פרק 15` are visible.
- A visible line describes an international keyword string. This is production-language leakage and not buyer copy.
- The page lacks a real linked sources section.
- FAQ structured data does not match the visible FAQ and includes an apartment-selection claim despite an empty project unit array.
- Multiple project and breadcrumb schemas duplicate one another.
- Neighborhood-confidence coordinates are rendered as though they were precise project coordinates.
- The current language cluster exposes only Hebrew and x-default rather than four native sibling pages.
- The public article is below the 5,000-word content standard once generic navigation and engine copy are excluded.

## Broken and excluded links

- `https://nad-lan.co.il/projects/recanati-residence/home.html` returned 404.
- `https://nad-lan.co.il/projects/recanati-residence/project.html?project=recanati-residence` returned 404.
- The live `/tour/designer/` route opens generic Sde Dov content and is excluded from Recanati article links.

## Safe correction baseline for the new foreign-language content

- RECANATI RESIDENCE, Ramat Aviv Gimel, Tel Aviv-Yafo.
- Completed demolition-and-reconstruction urban-renewal complex.
- 198 apartments in three completed 16-floor buildings.
- Published mix of 3-5 rooms, mini-penthouses and penthouses.
- Three underground parking levels and more than 15 metres between buildings at project level.
- Ashtrom Residences, formerly Ashdar, with Enav.
- Current official presentation: immediate occupancy; current price and inventory require fresh confirmation.
- No generic model, standard tour, selected-apartment card, sea view, Sde Dov comparison or demo price may become a project fact.

## Technical locations observed during read-only trace

These locations explain the leakage but were not edited:

- `plugins/nadlan-config/inc/showroom-engine.php` contains generic-model fallback and Sde Dov area payload logic.
- `plugins/nadlan-config/assets/showroom-engine/engine.js` generates the broken local `home.html` and `project.html` routes.
- `plugins/nadlan-config/inc/project-experience.php` supplies the comparison block.
- `plugins/nadlan-config/assets/showroom-engine/i18n.js` contains Sde Dov labels.

This package supplies content only. It does not repair those shared modules.

