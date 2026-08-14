# Einstein flagship comparison

Snapshot date: 2026-08-14
Status: read-only comparison of the live fleet against the local/private Einstein flagship implementation. This folder does not authorize deployment or public release.

## Outcome

Einstein is the strongest governed project package in the repository, but it is not yet the strongest complete buyer product.

It improves the parts that make a flagship safe to scale:

- one canonical identity (`einstein-tower-6885-32`, parcel `6885/32`, WordPress post `4867`);
- source-linked facts, explicit effective dates and separate current/future states;
- an original 39,912-triangle / 79,824-vertex HD model, a distinct 156-triangle / 312-vertex LOD, independently re-read hashes and three governed concept anchors serving four scenes;
- a protected mobile model stage with no overlay over the building;
- four visual invitations below the model: View, Interior, Design and Comments;
- zero-inventory fail-closed behavior instead of invented apartments;
- a first-party same-origin viewer, one visible H1 in the v3 renderer, private-stage headers and no browser write path.

The remaining product gaps are substantial:

- the v3 WordPress path has fixture and offline proof, but no authenticated private WordPress readback or live screenshot proof;
- the View tool is a schematic visual, not the fleet's live Mapbox context map or direction beam;
- Interior is a controlled concept simulation with four selectable images, not a spatial tour tied to an official plan;
- Design drags one illustrative sofa, not a plan-aware apartment configurator;
- Comments prepares a local annotation but does not deliver to OLP;
- inventory, unit plans, unit-specific views, prices and selected-unit inquiry are intentionally absent;
- lead and comment submission are disabled;
- Hebrew is the only staged language;
- real-world model orientation and all three concept-hotspot positions remain uncalibrated;
- the first-party WebGL viewer renders flat base-color materials and does not consume image textures;
- the former recipe drift is closed: the repository entry now points to the maintained playbook,
  and the reusable `nadlan-flagship-project-showroom` skill is merged in the agent-skills repository.

The release decision is therefore: keep Einstein private until the acceptance gates in [evidence-and-acceptance-gates.md](evidence-and-acceptance-gates.md) pass. The exact fleet and competitor comparison is in [side-by-side-gap-matrix.md](side-by-side-gap-matrix.md).

## Pages inspected

Every live fleet row below was opened and rendered at a 390 x 844 mobile viewport on 2026-08-14. The model was scrolled into view before hotspot measurements.

| Comparator | Live URL | Role in the comparison |
| --- | --- | --- |
| H Infinity | <https://nad-lan.co.il/projects/h-infinity-somail-tel-aviv/> | Current owner-designated flagship baseline |
| Rainbow | <https://nad-lan.co.il/projects/rainbow-tel-aviv/> | Residential page with a small authored illustrative unit set |
| Dimri Yama | <https://nad-lan.co.il/projects/dimri-yama-sde-dov/> | Residential page with a high-node-count model and a small unit set |
| Ashira | <https://nad-lan.co.il/projects/ashira-sde-dov/> | Residential page with a high-node-count model and a small unit set |
| ToHa2 | <https://nad-lan.co.il/projects/toha2-tel-aviv/> | Commercial high-rise floor-selection baseline |
| The Park | <https://nad-lan.co.il/projects/the-park-bnei-brak/> | Commercial floor-selection and context baseline |
| Einstein | Not public in v3 | Local/private proposed successor; canonical public URL remains reserved at `/projects/einstein-tower/` |

“Dimri” and “Yama” refer to one inspected implementation, the Dimri Yama page above.

## Evidence method

The comparison combines four evidence types and keeps their states separate:

1. Rendered-browser observations of the six live pages at 390 x 844.
2. Read-only inspection of the exact GLB bytes served by those pages.
3. Repository inspection of Einstein contracts and named renderer/runtime symbols.
4. Local automated checks run on 2026-08-14:
   - direct GLB v2 JSON/BIN inspection and accessor recount - PASS for exact bytes, SHA-256, triangles, vertices, mesh/node/material counts, metadata and HD/LOD hotspot parity;
   - `node assets/projects/einstein-tower/validate-model.mjs` - PASS;
   - `php scripts/qa-flagship-v3-php.php` - PASS;
   - `node scripts/qa-einstein-project-identity.mjs` - PASS;
   - `node scripts/qa-project-showroom-inventory-contract.mjs` - PASS;
   - `node scripts/qa-einstein-flagship-offline.mjs` - PASS at 320 x 568, 390 x 844, 568 x 320 and 1280 x 800.

Existing competitor findings were used only where they name an observed capability and a source. No ranking, conversion or causation claim is inferred from the comparison.

## State labels used in this report

| Label | Meaning |
| --- | --- |
| Live-observed | Rendered on a current public page during this review |
| Local-proven | Executed by a repository fixture or offline browser test |
| Contracted | Required by data/code, but not yet proven in private WordPress |
| Planned | Architecture recommendation only |
| Not checked | No adequate evidence was produced in this review |

## Files in this package

- [side-by-side-gap-matrix.md](side-by-side-gap-matrix.md) - project-by-project, cross-cutting and competitor capability gaps.
- [evidence-and-acceptance-gates.md](evidence-and-acceptance-gates.md) - exact source/symbol ledger, current status and binary release gates.
- [../../plans/einstein-flagship-recipe-draft/README.md](../../plans/einstein-flagship-recipe-draft/README.md) - reusable architecture, applied skill delta and traceability.
