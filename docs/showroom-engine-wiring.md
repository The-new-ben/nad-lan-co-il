# NadLan Showroom Engine — Wiring Contract

The engine (`Showroom Engine.dc.html`) is **data-driven and CMS-pluggable**. The same component
renders any project. It resolves its data in this order:

1. **`window.NADLAN_SHOWROOM`** — injected by WordPress (real CMS data). Used if present.
2. **`assets/engine/projects.js`** — bundled prototype manifest (fallback / demo).

No code changes per project. Drop it in the theme, print the payload, done.

---

## 1. How WordPress feeds it (the only wiring step)

In the block/template that renders the showroom, print the project payload before the component:

```php
<script>
  window.NADLAN_SHOWROOM = <?php echo wp_json_encode( nadlan_showroom_payload( get_the_ID() ) ); ?>;
  window.NADLAN_LEAD_ENDPOINT = '<?php echo esc_url_raw( rest_url('nadlan/v1/lead') ); ?>';
</script>
```

`nadlan_showroom_payload()` is the existing builder behind `assets/projects/<slug>/showroom-payload.json`.
The engine accepts **any** of these shapes:

- a single project payload: `{ slug, name, sub, floors, model_glb, poster, units:[...] }`
- a map: `{ "rainbow": {…}, "dimri-yama": {…} }`
- the raw repo payload: `{ slug, meta:{ project_3d_units:[…], project_model_glb, project_model_poster } }`

Select a project with `?project=<slug>` in the URL, or the `project` prop, or the on-page switcher.

## 2. Field correspondence (CMS → engine)

The engine normalizes these field names automatically (`normalizeProjects`), so existing
`nadlan_project` meta maps straight through — no renaming:

| Engine input | CMS / payload field(s) accepted |
|---|---|
| project name / subtitle | `name` / `sub` (fallback: slug) |
| model file | `model_glb` · `project_model_glb` (fallback: generated `assets/engine/<slug>.glb`) |
| poster image | `poster` · `project_model_poster` |
| floor count | `floors` · `project_floors` |
| unit list | `units` · `project_3d_units` |
| unit hotspot position | `position` · `hotspot_position` |
| unit hotspot normal | `normal` · `hotspot_normal` |
| unit camera framing | `orbit` · `camera_orbit` |
| floor / rooms / sqm / balcony | `floor` · `rooms` · `sqm` · `balcony` |
| direction | `dir` · `direction` |
| view text | `view` |
| status | `status` (`available` / `reserved` / `sold`) |
| plan drawing | `plan` (key `plan-4br` or a full URL) |

Any missing 3D coordinate is derived from `floor` + `direction` by the generator (below), so a
project can go live with only the unit table and get a usable model immediately.

## 3. Leads (already wired)

On submit the engine POSTs JSON to `window.NADLAN_LEAD_ENDPOINT` (default `/wp-json/nadlan/v1/lead`,
the existing route) with the full unit-level payload:

```
source, project_slug, project_title, name, phone, email,
unit, floor, rooms, sqm, balcony, direction, view,
building, availability, reservation_state, message, market_note
```

If no backend is reachable (prototype/offline) it shows the thank-you locally. On WordPress it
records a real lead. Override the endpoint with the `leadEndpoint` prop or `window.NADLAN_LEAD_ENDPOINT`.

## 4. Adding the NEXT project (the factory)

The model + poster are produced by the **parametric generator** (see the build script that wrote
`assets/engine/*.glb` and `projects.js`). To add a project:

1. Add a project spec: `{ slug, floors, floorH, podiumFloors, fpX, fpZ, twist, taperTop, boutiques, units }`.
2. Run the generator → it writes `<slug>.glb`, a poster, and the normalized unit coords.
3. Or skip the generator entirely and set `project_model_glb` to the developer's official BIM/glTF
   when it arrives — the engine swaps to it with no other change.

The engine, facade selector, unit drawer, lead funnel and analytics hooks are identical for every
project. One engine, every project in the catalog.

## 5. Honesty rule (carried from the product direction doc)

Generated models are labelled illustrative until official developer BIM/plans replace them. No
invented prices, no official-inventory claims, no fake tours. The disclaimer band ships in the page.
