# Einstein Tower illustrative model assets

This isolated asset set represents **EINSTEIN TOWER / Einstein 33A**, parcel
6885/32, with canonical contract ID `einstein-tower-6885-32`.

It is an original, project-specific **owner-approved illustration** governed by
`OWNER-2026-08-14-EINSTEIN-ILLUSTRATIVE-MASSING`. It is decision-grade false
and is not BIM, a survey, as-built geometry, a sales plan, or inventory. The
owner permits the labelled illustration itself to be published, while the
asset remains in the separate `private_stage` release gate until the page-level
release process is satisfied.
Geometric facade panels and level bands are visual detail only and must never
be adapted into floors or units.

The GLB also carries three deliberately approximate experience anchors—one
representative-interior walkthrough opening two scenes, one arrival concept
and one landscaped open-space concept—under
`OWNER-2026-08-14-EINSTEIN-INTERIOR-FACILITIES-DEMO`. Their mapping state is
`owner_approved_illustrative_mapping`: they are clickable, owner-approved
demonstration anchors in model space, not proof that a facility exists or that
either scene belongs to an official floor, unit or room. The separate future
`source_cited_mapping` lane must never be inferred from these coordinates.
Every anchor declares the authored component/zone, model-space position and
normal, visible-marker offset, scene IDs, evidence category, confidence,
ambiguity and prohibited inferences. Model axes are not a real-world
orientation until a signed municipal/survey transform is supplied.
The categorical confidence statement is retained alongside the trusted
two-part `placement_confidence` (`zone` and `exact_point`). The frozen pairs
are 0.68/0.18 for the representative interior, 0.63/0.20 for arrival and
0.86/0.24 for landscaped open space; these values do not upgrade an
illustrative point to source-cited placement.
The internal `tool_id` continues to distinguish interior from facility
content, while every anchor has the explicit
`open_surface_tool_id=interior`. The public showroom therefore exposes exactly
four permanent tiles (View, Interior, Design and Comments); both facility
concepts are selectable inside Interior and may be opened there directly from
their independent model anchors.
The four matching local WebP assets—two selectable representative-interior
scenes and two selectable shared-space concepts—and their immutable hashes, dimensions, scope
and prohibited claims are declared in `experience/manifest.json`. Consumers
must validate that manifest, require the exact owner decision, keep one visible
showroom-level demonstration disclosure, and fail closed if an asset is
missing, altered or expired. No external source image is shipped or hotlinked.

Run from the repository root:

```text
node assets/projects/einstein-tower/generate-model.mjs
node assets/projects/einstein-tower/validate-model.mjs
```

`generate-model.mjs` is deterministic and dependency-free except for the
already-installed ImageMagick executable used only to encode the compact WebP
poster. The GLB validator independently counts indexed triangles, checks
meaningful component names, exact identity/governance metadata, North=0/+Z,
and byte budgets.
