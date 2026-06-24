# 08 WordPress Implementation Map

## Source of truth

The WordPress repo is the runtime source of truth. This packet is the design and implementation reference.

## Mapping table

| Pattern file | WordPress target | Purpose |
|---|---|---|
| `reference/showroom-reference.html` | `plugins/nadlan-config/inc/project-3d.php` | Markup structure for project showroom |
| `reference/showroom-reference.css` | Plugin showroom CSS or premium UI CSS | Visual system for showroom |
| `reference/projects-reference.html` | `plugins/nadlan-config/inc/directory.php` | Project archive card structure |
| `reference/projects-reference.css` | `plugins/nadlan-config/inc/directory-assets.php` or CSS asset | Project archive styles |
| `reference/homepage-reference.html` | WordPress front page template | Homepage structure |
| `reference/homepage-reference.css` | Shared premium CSS | Homepage styles |
| `data/design-tokens.json` | Shared CSS variables | Color, type and spacing source |
| `data/component-map.json` | Developer checklist | Class mapping and replace rules |
| `data/asset-contract.json` | Contractor intake | Asset requirements |
| `data/qa-checklist.json` | QA script input | Proof requirements |

## No stacking rule

Do this:

1. Locate old stylesheet or inline style block for the active showroom.
2. Stop loading it on project pages.
3. Emit the new markup classes.
4. Load the premium stylesheet.
5. Keep the 1.69.32 behavior only after visual replacement is stable.

Do not do this:

```css
.old-showroom .new-override .another-fix { ... }
```

That creates the same patch problem again.

## PHP implementation sketch

```php
<section class="nl3d-stage nl3d-real-state" aria-label="<?php echo esc_attr($labels['building_view']); ?>">
  <?php echo $building_renderer; ?>
  <div class="nl3d-stage-top">
    <span class="nl3d-chip"><?php echo esc_html($labels['building_active']); ?></span>
  </div>
  <?php foreach ($units as $unit): ?>
    <button class="nl3d-unit-pin <?php echo esc_attr($unit['selected_class']); ?>"
      data-unit-id="<?php echo esc_attr($unit['id']); ?>"
      aria-label="<?php echo esc_attr($unit['label']); ?>">
      <strong><?php echo esc_html($unit['floor']); ?></strong>
    </button>
  <?php endforeach; ?>
</section>
```

## JavaScript implementation sketch

```js
function selectUnit(unitId, source) {
  const unit = unitsById[unitId];
  if (!unit) return;

  root.dataset.activeUnit = unit.id;
  updatePins(unit.id);
  updateRail(unit.id);
  updateSelectedPanel(unit);
  moveCameraIfAvailable(unit);
}
```

## Data rule

Every unit must have:

```json
{
  "id": "unit-16-w",
  "floor": 16,
  "line": "W",
  "rooms": 4,
  "sqm": 112,
  "direction_he": "מערב",
  "direction_en": "West",
  "status": "available"
}
```

Drop or hide any unit without a stable id.

## Security and escaping

- Escape all text with `esc_html`.
- Escape attributes with `esc_attr`.
- Sanitize unit IDs to letters, numbers, dash and underscore.
- Sanitize polygon points if facade polygons are used.
- Never output raw contractor HTML in the showroom.

## Mobile rule

Before merge, run 390px QA on:

- Homepage.
- Projects archive.
- Showroom before selection.
- Showroom after selection.

Fail the PR if `document.documentElement.scrollWidth > window.innerWidth`.
