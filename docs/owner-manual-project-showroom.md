# Owner Manual: Project 3D Showroom Fields

This manual explains how to update a NadLan project page such as Rainbow Tel Aviv so the public
buyer page shows a real interactive showroom, not only a written article.

## Short Answer

The showroom is controlled from the project edit screen in WordPress, inside the metabox named:

`בחירת דירות אינטראקטיבית`

If the metabox is not visible, open the editor options and enable it:

1. Open the project in WordPress admin.
2. Click the three-dot menu in the top corner of the block editor.
3. Open `Preferences` / `העדפות`.
4. Open `Panels` / `פאנלים`.
5. Turn on `בחירת דירות אינטראקטיבית` and `Custom Fields` / `שדות מיוחדים` if they appear.
6. Scroll under the main editor. The metabox usually appears below the content area.

## Fields

### Real 3D Model

`project_3d_model_type`

Use one of these values:

- `gltf` for a real GLB model.
- `bim` for an official BIM-derived model.
- `procedural` for the schematic fallback.
- `facade` or `sprite360` only when that specific pipeline is used.

For Rainbow prototype use: `gltf`.

`project_model_glb`

The URL of the `.glb` model file.

Rainbow prototype:

`https://raw.githubusercontent.com/The-new-ben/nad-lan-co-il/main/assets/projects/rainbow-tel-aviv/model.glb`

Later, replace this with the official developer BIM/GLB URL when the developer supplies it.

`project_model_poster`

A lightweight image shown while the model loads.

Rainbow prototype:

`https://raw.githubusercontent.com/The-new-ben/nad-lan-co-il/main/assets/projects/rainbow-tel-aviv/poster.png`

`project_model_usdz`

Optional iPhone AR model. Leave blank until there is a real USDZ file.

## Units And Apartment Hotspots

`project_3d_units`

JSON array of apartment/unit rows. Each row can include:

- `id`
- `title`
- `label`
- `floor`
- `rooms`
- `sqm`
- `balcony`
- `dir`
- `view`
- `status`
- `recommended`
- `availability`
- `price_estimate`
- `price_note`
- `plan`
- `interior_url`
- `tour_url`
- `view_note`
- `hotspot_position`
- `hotspot_normal`
- `camera_orbit`

The important model fields are:

- `label`: short buyer label shown on the clickable marker or tooltip.
- `status`: `available`, `reserved`, or `sold`; this controls marker color.
- `recommended`: `true` marks a strong unit with a subtle pulse. Use it only for units the owner
  wants to feature, such as sea view, high floor or limited availability.
- `hotspot_position`: where the clickable apartment marker appears on the 3D model.
- `hotspot_normal`: the direction the marker faces.
- `camera_orbit`: optional camera angle when the apartment is selected.

Rainbow prototype unit file:

`https://raw.githubusercontent.com/The-new-ben/nad-lan-co-il/main/assets/projects/rainbow-tel-aviv/unit-map.json`

The plugin can seed this file automatically for Rainbow. For the next project, prepare the same
`unit-map.json` file and paste or import it into the field.

## Buyer Flow Standard

The public showroom should read in this order:

1. Short SEO intro above the model: project, location, developer, price/availability disclaimer.
2. Compact model stage with obvious color-coded apartment markers.
3. Selected-apartment card with title, status, view, price estimate and actions.
4. Lead form and advisor choices carrying the selected unit into the lead funnel.

If the page does not follow that order on mobile, the project is not ready for publication.

The selected-apartment card is controlled by the unit JSON:

- `status` controls the marker color and the card status.
- `recommended: true` adds a recommendation tag and pulse.
- `view`, `dir`, `rooms`, `sqm` and `floor` become the buyer summary.
- `price` is treated as official only when approved. `price_estimate` is shown as an estimate and
  must stay non-binding.
- `price_source` / `price_note` should explain where the estimate came from.

If those fields are empty, the public page falls back to `לפי פנייה`. Do not publish fake inventory
or fake official prices.

## Drawings, Plans And Materials

`project_3d_drawings_json`

Use this for approved floor plans, site plans, elevation drawings and legal/source notes.

Accepted formats:

```json
[
  {
    "label": "תוכנית 4 חדרים",
    "type": "floor_plan",
    "url": "https://example.com/plan.svg",
    "source": "המחשה מקורית, לא תוכנית מכר"
  }
]
```

or:

```json
{
  "items": [
    {
      "label": "תוכנית 4 חדרים",
      "type": "floor_plan",
      "url": "https://example.com/plan.svg",
      "source": "המחשה מקורית, לא תוכנית מכר"
    }
  ]
}
```

Rainbow prototype drawings:

`https://raw.githubusercontent.com/The-new-ben/nad-lan-co-il/main/assets/projects/rainbow-tel-aviv/drawings.json`

## Surroundings And Nearby Projects

`project_3d_environment_json`

Use this for nearby projects, parks, transport, schools, public services and source notes.

Accepted formats:

- Simple flat item array.
- Structured object with `layers[].items[]`.

The plugin flattens the structured format into buyer-facing cards.

Important rule: illustrative relative positions are not exact survey pins. Do not present them as
exact map coordinates until verified by the developer, municipality or survey data.

Rainbow prototype environment:

`https://raw.githubusercontent.com/The-new-ben/nad-lan-co-il/main/assets/projects/rainbow-tel-aviv/environment.json`

## Price Fields

`project_3d_avg_price_per_sqm`

Optional approximate price per sqm. Leave blank unless the owner approved the source.

`project_3d_price_source_note`

Required when any estimate is shown. The note must say the number is an estimate and not binding.

Recommended wording:

`אומדן לא מחייב לפי מקור מאושר. יש לאמת מחיר, זמינות ותנאים מול היזם לפני כל התקדמות.`

## Media Fields

`project_3d_video_url`

Developer-approved sales video or YouTube link.

`project_3d_tour_url`

Interior tour, Matterport-style tour, or approved apartment walkthrough.

`project_3d_cesium_tiles_url`

Future seam for Cesium / Google Photorealistic 3D Tiles. Leave blank until the paid/keyed setup is
approved.

## Classic Editor Question

Classic Editor can make old metaboxes easier to see, but it should not be the long-term answer.

Recommended decision:

- Do not install Classic Editor as the permanent workflow.
- Keep Gutenberg because Yoast, blocks and future page assembly are already there.
- Improve the plugin metabox/sidebar so the showroom fields are easy to find without changing the
  whole editor.
- Use Classic Editor only as a temporary emergency aid if the owner cannot access the fields.

## Deployment Checklist

After code is merged:

1. Pull or sync the UPress server Git copy.
2. Update the NadLan Config plugin in WordPress.
3. Clear UPress cache.
4. Hard refresh the public project page.
5. Open `/wp-json/nadlan/v1/healthcheck`.
6. Confirm the version number matches the deployed plugin.
7. Confirm `project_3d.model_viewer_ready` is true.
8. Confirm `project_3d.model_viewer_module_tag` is true.
9. Confirm `project_3d.projects_with_glb` is at least 1 for Rainbow.
10. In Chrome, confirm `customElements.get('model-viewer')` returns a function.
11. Capture desktop and mobile screenshots of the rendered model.

## Definition Of Done

The work is not done when a field is saved.

The work is done only when the public buyer page shows:

- real model or honest fallback,
- no blank model stage,
- working rotation/drag,
- clickable unit hotspots,
- buyer-facing unit details,
- no raw code leaks,
- no horizontal overflow,
- one H1,
- project-relevant first paragraph,
- non-binding price wording,
- Chrome screenshots proving the rendered result.
