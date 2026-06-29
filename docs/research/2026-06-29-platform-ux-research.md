# NadLan Platform UX Research

Date: 2026-06-29

This note records the research inputs for the premium platform rebuild pass before code changes. It is intentionally decision-oriented: every source maps to one NadLan implementation rule.

## Property And Portal Patterns

| Source | URL | Insight | NadLan decision |
| --- | --- | --- | --- |
| Zillow 3D Home | https://www.zillow.com/3d-home/ | 3D/tour content works when it is part of the property decision path, not a separate demo. | Keep 3D as the building/media section of the project page, and connect selection to apartment facts and inquiry. |
| Zillow Zestimate | https://www.zillow.com/z/zestimate/ | Users understand value as an estimate plus uncertainty, not a final sale price. | Show only price ranges with date and "אומדן לא מחייב"; never show a fake single exact price. |
| Compass listings and collections | https://www.compass.com/ | Premium listing pages make saving, sharing, comparing and similar homes part of the buyer workflow. | Keep selected-apartment state, related projects, and future save/share as buyer actions, not internal lead language. |
| Homes.com Matterport | https://www.homes.com/solutions/matterport | Interior tours are a buyer confidence layer that should load only when the user asks for them. | Add a lazy "סיור פנים" slot fed by project tour URLs or panoramas; collapse honestly if missing. |
| Rightmove | https://www.rightmove.co.uk/ | UK detail pages foreground photos, floorplans, map, key facts and contact in a predictable order. | Project pages should keep hero, building, apartments, price, surroundings, media, article and inquiry in one stable order. |
| OnTheMarket | https://www.onthemarket.com/ | Property users expect floorplan, map and agent contact to stay close to the decision moment. | Keep selected-unit facts, plan/view/media and contact in the same selected-apartment panel. |
| Yad2 real estate | https://www.yad2.co.il/realestate/forsale | Israeli buyers scan location, rooms, size and price quickly before deeper reading. | Project/archive cards must show location, rooms/units, sqm/floors when known, and a short buyer promise. |
| Madlan | https://www.madlan.co.il/ | Israeli market pages win trust with area context and transaction/neighborhood signals. | Use area/project pages with real surroundings, nearby projects, public transaction comps where available, and source dates. |
| Booking | https://www.booking.com/ | High-conversion travel pages use sticky search, availability, map, reviews and clear next action. | Homepage/project pages should expose search/filter and availability/status before long explanation text. |
| Expedia | https://www.expedia.com/ | Map/list and trust signals help users compare options without losing the current item. | The project archive can use a premium card grid first, with map/list as a later stable enhancement. |
| Nike product pages | https://www.nike.com/ | 3D product orbit should be controlled and framed, not show awkward underside views. | Lock model camera limits to buyer-facing horizontal orbit; 3D is visual context while facade/list is the precise picker. |

## Technical And SEO Sources

| Source | URL | Insight | NadLan decision |
| --- | --- | --- | --- |
| Google localized versions | https://developers.google.com/search/docs/specialty/international/localized-versions | Separate language URLs must reciprocally identify each other with hreflang, including self links. | No hash language buttons. Use real HE/EN/FR/RU/AR URLs only when pages exist, with reciprocal hreflang and x-default. |
| WordPress child themes | https://developer.wordpress.org/themes/advanced-topics/child-themes/ | Child themes add to parent themes and must not duplicate parent functions. | Keep child theme presentation-only; do not copy parent functions.php. |
| WordPress theme.json | https://developer.wordpress.org/block-editor/how-to-guides/themes/theme-json/ | Theme tokens should live in a predictable configuration where native blocks can inherit them. | Mirror locked NadLan tokens into theme.json where possible; keep wide public CSS scoped. |
| WordPress Shortcode API | https://developer.wordpress.org/apis/shortcode/ | Shortcode callbacks must return output and should be explicit insertion points. | Use shortcodes only as explicit bridge points, not as hidden duplicate renderers. |
| WordPress REST API custom endpoints | https://developer.wordpress.org/rest-api/extending-the-rest-api/adding-custom-endpoints/ | REST endpoints need namespace, callback and permission callback. | Lead/content-gap/comps routes must be explicit, permissioned where needed, and return data rather than echoing JSON. |
| model-viewer | https://modelviewer.dev/ | Browser-native model display is suitable for GLB with camera controls, poster and lazy loading. | Use model-viewer for the 3D context surface, with poster and horizontal camera constraints. |
| Pannellum | https://pannellum.org/ | Lightweight panorama viewer can power simple 360 interiors without a paid dependency. | Add optional panorama slots for interior experience; lazy-load only on click. |
| Marzipano | https://www.marzipano.net/ | Multi-room virtual tours can be built from panoramas when a contractor supplies assets. | Keep Marzipano as a future multi-room implementation path behind project data. |
| Mapbox GL JS | https://docs.mapbox.com/mapbox-gl-js/guides/ | Mapbox is strong for interactive maps and markers when token and coordinates are valid. | Use Mapbox for surroundings when configured; otherwise show a stylized fallback with real relative positions. |
| WCAG overview | https://www.w3.org/WAI/standards-guidelines/wcag/ | Controls need keyboard access, visible focus, readable contrast and usable target sizes. | Header, language selector, apartment selector, accessibility widget and contact CTAs must pass desktop/mobile visual QA. |

## Implementation Guardrails

- Buyer-facing copy speaks to buyers, investors, families and foreign buyers. It must not expose internal workflow terms.
- The homepage is a business hub and must not be replaced by a narrow 3D demo.
- Project pages should use one showroom renderer, one article body, one inquiry path and one language-switching method.
- Missing data collapses or becomes an honest note. It does not become fake prices, fake photos or fake official claims.
