# Foreign Investor and 3D System

## Strategic role

Foreign-buyer readiness and 3D should make NadLan more useful after the visitor recognizes a familiar property portal. Neither should replace the primary inventory/search identity.

## Foreign-buyer readiness contract

A project earns `Foreign-buyer ready` only when all required elements pass:

### Content parity

- Complete English project title, summary, facts, media captions and facility labels.
- English project status, handover and price policy match the Hebrew source record.
- Plans/documents have an English version or an honest language label.
- Corresponding canonical/hreflang relationship works.

### Display preferences

- ILS source values retained.
- Optional USD/EUR display uses a dated rate and says it is an indicative conversion.
- Square meters remain source-of-truth; sqft can be displayed as a conversion.
- Dates, numbers and phone formats match locale without changing underlying facts.

### Transaction understanding

- Plain-language buying process.
- Total-cost categories: tax, legal, finance, registration, maintenance/fees where applicable.
- Clear educational/not-legal-or-tax-advice boundary.
- Links to verified relevant professionals.
- Source/date on calculators and assumptions.

### Remote operation

- Named English-speaking contact owner.
- Working international phone/WhatsApp/email/form path.
- Remote appointment/tour workflow and response expectation.
- Timezone-aware scheduling or clear availability.
- Consent and lead-routing fields preserve language and selected project/unit.

### Decision evidence

- Approved media and plans.
- Project/location map.
- Construction/handover state and last checked date.
- Remote 3D/video only where it is true and working.
- A way to request current availability without implying an online purchase/reservation if none exists.

Translation alone is insufficient.

## Recommended foreign-buyer page structure

1. Image-led project discovery and search in English.
2. Curated foreign-ready projects, not every partially translated record.
3. How buying in Israel works.
4. Total-cost estimator and currency/unit preferences.
5. Remote-viewing process.
6. City/area guides with project inventory.
7. Named legal, tax, mortgage and inspection categories with caveats.
8. One contextual inquiry/scheduling path.

The strongest benchmark combination is RealEstate-Israel's multilingual inventory, BuyWise's process/cost clarity, Idealista's remote/media system and Zoopla Overseas' transaction education.

## 3D maturity levels

| Level | Data | Allowed public promise |
| --- | --- | --- |
| 0 — none | no approved model/tour | no 3D badge or empty viewer |
| 1 — media tour | approved Matterport/Kuula/video/virtual tour | `סיור וירטואלי` with provider/source |
| 2 — project model | approved GLB/USdz/massing, no unit mapping | `מודל 3D של הפרויקט`; no exact unit selection |
| 3 — authored demo targets | model plus curated target coordinates/demo units | `המחשת בחירת דירה`; clearly not live/complete inventory |
| 4 — unit-aware model | official segmented geometry/IDs mapped to approved unit data | `בחירת דירה מתוך הבניין` within published inventory policy |
| 5 — transactional digital showroom | level 4 + current availability, plans, views, contextual lead/reservation policy | full synchronized showroom; still label non-binding states |

## Exact-selection truth boundary

Exact click-any-window selection requires at least one trustworthy mapping source:

- official GLB with named per-unit meshes/object IDs;
- BIM/IFC/Revit mapping exported with stable unit identifiers;
- approved facade/elevation polygons mapped to unit IDs;
- another contractor-provided apartment-level geometry contract.

The current Rainbow prototype demonstrates authored targets and approximate nearest-unit interaction. It does not prove exact per-window picking or live availability. This limitation must remain visible until the official data exists.

## 3D data contract

Reuse the existing `project_3d_*` model/poster/camera/drawings/environment/facade/site-plan/unit fields. Before public level 4/5 readiness, every unit mapping additionally needs:

- stable project/unit ID;
- building/entrance/floor/unit designation;
- mesh/object or polygon ID;
- plan attachment ID/version;
- orientation/exposure and view source;
- availability/price policy source and verified date;
- model source, rights and version;
- transformation/calibration record;
- QA result for desktop and touch selection;
- fallback behavior when the model fails.

## Homepage and card behavior

- `3D` is one evidence-backed badge among others.
- Cards use an image/poster and load no heavy viewer.
- Homepage may use at most one lazy, user-opened 3D preview after launch performance is proven.
- The project detail owns the full model, unit selection and view experience.
- Mobile defaults to the unit list/table if the model interaction is less clear or less accessible.

## Performance/accessibility

- Poster-first; load model only on explicit action or when safely below the fold.
- Respect reduced motion.
- Provide keyboard/list/table alternative to spatial selection.
- Announce selected unit and changes to assistive technology.
- Keep unit facts and inquiry available without WebGL.
- Do not block page content when third-party tours fail.

## Foreign-buyer + 3D combined opportunity

The differentiated remote journey is:

```text
English project discovery
→ approved project media and source/date
→ inspect plans / optional 3D
→ select a plan or exact unit when data permits
→ see price policy, costs and area evidence
→ schedule a remote conversation carrying the selected context
```

This is credible only when the content, rights, data and human workflow are complete. A model alone is not a foreign-investor product.
