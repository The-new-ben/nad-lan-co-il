# Hotspot placement methodology — frozen 2026-08-14

This note freezes three logical anchors serving four local selectable scene assets. No source image bytes are included.

## Method

1. Lock the target to Einstein 33A / Einstein 14 / block 6885 parcel 32.
2. Use the live Hagag target gallery for visible building-zone cues.
3. Use Tel Aviv protocol 20-0005 / design plan 4695(1) for permitted use, access and public-realm categories.
4. Use municipal permit `oid_permit=9945` for the current project composition, four parking levels and ground-floor lobby category.
5. Place the click point on an existing current-model component that best represents the supported zone.
6. Mark every exact point `owner_approved_illustrative_mapping`, `decision_grade=false`, `source_cited_mapping=false`. Sources constrain a zone or use; the owner authorizes the final interpolated click coordinate.

## Frozen anchors

- `representative-interior-concept` — `(16.0, 34.7, 5.8)`, normal `(0,0,1)`, on `Tower_28_Level_Massing;Glass_Terrace_Strips`. Both living and bedroom scenes open from this aggregate anchor. This deliberately avoids inventing a bedroom floor, facade or unit.
- `arrival-shared-podium-concept` — `(12.0, 9.5, -13.25)`, normal `(0,0,-1)`, at `Tower_28_Level_Massing;Podium_Double_Level`. The lobby/arrival category is supported; the exact door is not.
- `landscaped-public-roof-concept` — `(27.0, 10.0, 14.0)`, normal `(0,1,0)`, on `Landscape_Terraces;Podium_Double_Level`. The active landscaped public roof/open-space category is strongly supported; the chosen slab and point are illustrative.

Exact asset-to-anchor rows, confidence, ambiguity and prohibited inference are in `hotspot-placement-crosswalk.csv`. Direct source URLs are in `hotspot-anchor-summary.csv` and `primary-source-register.csv`.

## Permit geometry nuance

The `oid_permit=9945` GIS polygon is about 22.7 × 36.6 m / 664.7 m² at the west end of parcel 32. It may be a municipal building/application locus and may help later orientation work. The excavation record, the whole three-volume project permit and the private-roof-pool request all reuse that same single polygon. Therefore it is **not** accepted as the surveyed footprint of all three buildings, and it is not used to scale any current mesh.

## Replacement rule

Replace an approximate anchor only when a signed ground-floor, elevation, apartment or landscape/roof plan is linked to `project_contract_id=einstein-tower-6885-32` and crosswalked to the current GLB. Preserve the old coordinate and source trail in history; do not silently upgrade `source_cited_mapping`.
