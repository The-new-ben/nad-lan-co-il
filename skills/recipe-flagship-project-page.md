# Recipe: build a flagship project page (the H Infinity standard)

> THE canonical, executable recipe lives at
> **`docs/playbooks/flagship-showroom-recipe.md`** — full phases, exact meta
> keys, code, design tokens, deploy pipeline, QA gates. This skill is the
> entry point; any model executing a new project page (first designee:
> Einstein 18) follows the playbook end to end.

## The shape (memorize)

1. **Dossier first** (`docs/content/<slug>/dossier-start.md`): anchored
   facts + explicit unknowns. Unknown stays unknown forever after.
2. **Card**: `nadlan_project` post + the exact meta contract
   (`project_3d_units`, `project_env_landmarks`, `project_model_glb`,
   `project_hero_eyebrow`, `geo_confidence`, `nl_unit_scene_v2:on`, ...).
3. **GLB**: pure-python glTF massing model (<1MB, no normals, uint16),
   poster SVG so the stage never boots empty.
4. **Engine does the rest** — bands, honest stats, beam ring, window
   view/panorama key off the DATA. If a feature is missing, fix metas,
   never fork the engine.
5. **Deploy** via the payload→media→snippet→swap→probe→purge pipeline.
6. **QA gates** — real screenshots looked at (desktop+mobile, he+en),
   one h1, escaped-needle for Hebrew payloads, console clean, fleet
   regression (ToHa2 + one sde-dov page).

## The two red lines

- **HONESTY LAW:** no invented rooms/sqm/status/direction/price/tour/
  imagery. Zeros never render. Generic = labeled generic.
- **BEAM FREEZE (owner 2026-08-13):** the golden direction beam on the map
  is untouchable — no layout/logic/styling changes ever, and every engine
  change is checked for beam side effects fleet-wide before deploy.

## Related

- docs/playbooks/flagship-showroom-recipe.md (THE recipe)
- docs/playbooks/glb-gen-h-infinity.py (GLB generator to parameterize)
- skills/adopted-codex-visual-proof-loop.md (screenshot law)
- skills/adopted-claude-hebrew-payload-verification.md (escaped needle)
- skills/adopted-claude-chrome-verification-clicks.md (click/verify traps)
