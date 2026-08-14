# Einstein 33A / Einstein Tower — independent visual and model evidence check

Checked 2026-08-14. This folder is an independent, text-only cross-check. It does not alter the repository model or the existing source registers, and it ships no third-party image bytes.

## Bottom line

The current model gets the most important high-level silhouette right: one 28-level tower, two 13-level lower buildings, a shared double commercial base, a light mineral/glass material family, and a real indexed triangle count above the owner's 30,000-triangle target. The inspected HD GLB passed its validator at 39,840 triangles / 79,680 vertices / 2,400,052 bytes (`cb1f4b1d9603196dd46f7807b0475dfce0357827ae02d76d37fb861fba4ff4e5`).

It is still an illustrative showroom massing, not a source-calibrated site model. Its biggest shortcomings are not triangle count; they are footprint calibration, over-symmetrical facades, a weak crown, an oversized generic rectangular podium, and a public realm that is far less specific than the approved municipal design protocol.

The official municipal evidence supports much more decision-useful modeling than is currently shown:

- two street-level public open spaces in planning area G totaling about 1,230 m²;
- an active, accessible and landscaped public roof over the commercial base, with play, planting, shade, seating, pedestrian and cycle passage;
- separate commercial-street and residential-neighborhood entrance levels;
- an Einstein vehicle entrance and four parking levels in the current permit record;
- a separate 1,300 m² early-childhood treatment/daycare public building in planning area G.

These are public-realm/community facts, not a private resident amenity list. The only pool-specific current record found is a 2025 application for private pools on residential roof terraces; it has no permit number in the municipal layer and does not establish a shared pool or a completed facility.

## Exact target lock

Included target: Hagag Einstein Tower / Einstein 33A, municipal address Einstein 14, block 6885 parcel 32, planning area G / lot 33.

Explicit exclusions:

- Einstein 35 / planning area A;
- Einstein 1–5 / 7–9 / 15 and other Hagag Einstein schemes;
- Gindi/Shbiro Einstein 2•4•6•8;
- Ashtrom Einstein / Einstein 63–67;
- combined 515-unit financing or media descriptions unless a statement is separately attributable to 33A.

The approved municipal development-plan image covers three separate Einstein planning areas on one sheet. It is useful for topology, landscape and circulation logic, but it must be cropped and crosswalked to parcel 32 before any linework is traced into the target model.

## What the official imagery actually shows

The live Hagag gallery consistently shows a slender tower at one end, two close lower blocks at the other, and a continuous base. The tower has a strongly asymmetric facade family: solid light punched-window planes contrasted with a broad glazed/terrace stack. Its crown is a conspicuous asymmetric stepped composition with a tall glazed terminal volume, not the current small sequence of generic boxes. The lower pair has stacked balcony/glazing bands and roof setbacks, but the sources do not supply reliable module counts, dimensions or a signed compass orientation.

The municipal permit polygon for permit record `oid_permit=9945` is about 22.7 × 36.6 m / 664.7 m² and lies at the west end of parcel 32. It may be a useful municipal building/application locus and is directionally consistent with the tower-at-one-end composition. Because the excavation, whole three-volume project permit, and private-roof-pool request all reuse that single polygon, it is not safe to call it the surveyed footprint of all three buildings or to scale the tower from it without the archive plan.

## Current poster verdict

The inspected poster (`5588d09e28f95ac5d6655626027c3ad41f17c5c5c78153ecb2ba138821aa8c85`) is clear, light and original, but reads as a generic pastel axonometric. Exact discrepancies:

- the podium dominates as one uniform rectangular slab instead of expressing the parcel, level changes, commercial edge and active public roof;
- the two lower buildings are nearly cloned and the tower facade is too bilaterally regular;
- the tower crown is too small and too simple relative to the official close render;
- landscaping is decorative rather than a legible public open-space, passage and roof system;
- the road/corner context is abstract enough that a buyer cannot understand arrival, pedestrian movement or the two frontage conditions.

## Interior and facility mapping rule

The owner has expressly approved approximate demonstration mapping. The four selectable local scenes may therefore use `owner_approved_illustrative_mapping`, `decision_grade=false`. This is not a blocker.

The model should keep two different semantic layers:

1. **Source-backed site layers** — commercial base, public landscaped roof/open spaces, circulation/easements, vehicle access, parking concept and separate public building.
2. **Owner-approved demonstration scenes** — living, bedroom, shared arrival/gallery and landscaped terrace concepts. These may be clickable and approximately positioned, but they do not prove a unit, floor, view, facility existence, contractor specification or delivered amenity.

The machine-readable proposed positions are in `hotspot-placement-crosswalk.csv`. They are deliberately replaceable when a signed site, architectural or sales-plan crosswalk arrives.

## Coordinate convention for the hotspot file

- Position space: current model metres, `+Y` up and current declared `+Z` north.
- Normalized coordinates use the current building/podium envelope `x=-35..35`, `y=0..94`, `z=-23..23`; the north-arrow object is excluded.
- A coordinate is a clickable presentation anchor, not an asserted apartment or facility location.

## Files

- `primary-source-register.csv` — independent source and exclusion register.
- `model-geometry-crosswalk.csv` — evidence-to-current-model comparison.
- `independent-model-gap-list.csv` — prioritized exact fixes and acceptance tests.
- `hotspot-placement-crosswalk.csv` — four exact local asset IDs with current-model positions, normals and claim limits.

## Principal primary sources

- [Hagag live target page and gallery](https://www.hagag-group.co.il/projects/ResidentProjects/einstein_tower)
- [Tel Aviv approved architectural-design protocol 20-0005, plan 4695(1)](https://www.tel-aviv.gov.il/Residents/Development/DocLib/%D7%A4%D7%A8%D7%95%D7%98%D7%95%D7%A7%D7%95%D7%9C%2020-0005%20%D7%9E%D7%99%D7%95%D7%9D%201-4-20.pdf)
- [Planning Administration plan 507-0594929 provisions](https://apps.land.gov.il/IturTabotData/takanonim/telmer/5050295.pdf)
- [Tel Aviv municipal permit layer](https://gisn.tel-aviv.gov.il/arcgis/rest/services/IView2/MapServer/772)
- [Tel Aviv municipal parcel layer](https://gisn.tel-aviv.gov.il/arcgis/rest/services/IView2/MapServer/524)
- [Project TLV dated Einstein 14 site page](https://project-tlv.info/buildings/einstein/%D7%A4%D7%A8%D7%95%D7%99%D7%A7%D7%98-%D7%9E%D7%92%D7%93%D7%9C-%D7%90%D7%99%D7%A0%D7%A9%D7%98%D7%99%D7%99%D7%9F/)
