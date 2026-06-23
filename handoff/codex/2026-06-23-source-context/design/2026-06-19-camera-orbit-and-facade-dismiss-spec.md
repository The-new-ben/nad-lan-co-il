# Spec — 3D camera lock + facade dismissible + CMS wiring (project showroom)

> **Status:** implementation contract for Codex. Plugin file owned by Codex per the 2026-06-19 role-split.
> **Owner directives, verbatim (2026-06-19):**
> 1. *"3D model, it shouldn't be spinning 360 — it has to be horizontally docked. It's not logical to look underneath the building. It's not a shoe, it's a building."*
> 2. *"Make the facade dismissible — in case it's overflowing on mobiles or something."*
> 3. *"All the levels deep, all wired up to the CMS, to the settings… if someone wants to define it as 360 spin, then the contractor can do it."*

This spec turns those three sentences into a precise, CMS-controlled, defaults-safe implementation.

---

## 1. Defect summary (current live state)

- **Model tumbles on the polar axis.** `inc/project-3d.php:786` sets `max-camera-orbit="Infinity 180deg auto"` and `auto-rotate` is enabled — so the camera can go past vertical and look at the building's underside. On the placeholder GLB (8.5 KB massing box) this looks especially broken.
- **Facade plane has no close affordance.** When it overflows on a narrow viewport, the buyer cannot recover without scrolling around it.
- **No per-project camera control.** Every project gets the same orbit constraints. A high-quality BIM project should be able to opt into 360°; a placeholder massing model should be locked.

## 2. Target behavior

### 2.1 Camera (model-viewer)
**Default (no contractor input):** "horizontally docked" — orbit allowed only horizontally around the building, never vertically off-axis.
- `auto-rotate`: **off** by default. (No tumbling on placeholder GLBs.)
- Polar (vertical) angle: **locked to 78–85°** (a slight tilt above horizontal — a person looking at a building, not above or below it).
- Azimuth (horizontal): **free 360°** so the buyer can turn the building.
- Field-of-view: unchanged from current.

**Contractor opt-in (per project, via CMS):** full 360° orbit + auto-rotate, for projects that have real BIM/architectural GLBs worth showing from above.

### 2.2 Facade
- Render a **close button** (✕) docked top-left of `.nlp3d-facade-plane` on every viewport.
- Click → CSS class `.nlp3d-facade-dismissed` on `.nlp3d.nlp3d-premium` hides the plane and gives all space to the 3D model.
- A **small "show facade" pill** appears in the toolbar after dismissal, so the buyer can bring it back.
- State persists in `sessionStorage` (`nlp3d-facade-dismissed-<post-id>`) so it doesn't bounce back on minor interactions.

## 3. CMS contract (PHP, `inc/project-3d.php`)

### 3.1 New `$meta` fields (project-level)
Added in `nadlan_p3d_meta()` (the function that assembles `$meta`):

| field | type | default | sanitization | semantics |
|---|---|---|---|---|
| `camera_lock` | string | `'horizontal'` | `sanitize_key`, allowed: `horizontal` \| `free` | preset switch |
| `camera_min_polar` | string | `'78deg'` | regex `/^-?\d{1,3}(\.\d+)?deg$/` | min vertical angle |
| `camera_max_polar` | string | `'85deg'` | same | max vertical angle |
| `camera_auto_rotate` | bool | `false` | `(bool)` | enable model-viewer auto-rotate |
| `camera_rotation_per_second` | string | `'8deg'` | regex `/^\d{1,3}deg$/` | only used if auto_rotate=true |

Backing post-meta keys: `project_3d_camera_lock`, `project_3d_camera_min_polar`, `project_3d_camera_max_polar`, `project_3d_camera_auto_rotate`, `project_3d_camera_rotation_per_second`.

### 3.2 Preset behavior
`camera_lock` is the **single field a non-technical owner sets**. It maps:

| `camera_lock` | min_polar | max_polar | auto_rotate |
|---|---|---|---|
| `horizontal` *(default)* | `78deg` | `85deg` | `false` |
| `free` (contractor opt-in) | `0deg` | `180deg` | `true` |

If the contractor sets `camera_min_polar` / `camera_max_polar` / `camera_auto_rotate` explicitly, those override the preset. So:
- 99% of owners: leave the dropdown on "Horizontal" — get the locked behavior.
- 1% of contractors with real BIM: set "Free orbit" or override the individual angles.

### 3.3 Renderer changes (`inc/project-3d.php:771–830`)
Replace the hardcoded `min-camera-orbit="-Infinity 0deg auto"` / `max-camera-orbit="Infinity 180deg auto"` / `auto-rotate` block with `$meta`-driven attributes:

```php
<?php
$min_pol = esc_attr( $meta['camera_min_polar'] );
$max_pol = esc_attr( $meta['camera_max_polar'] );
$rot     = esc_attr( $meta['camera_rotation_per_second'] );
?>
<model-viewer
    ...
    min-camera-orbit="-Infinity <?php echo $min_pol; ?> auto"
    max-camera-orbit="Infinity <?php echo $max_pol; ?> auto"
    <?php if ( $meta['camera_auto_rotate'] ) : ?>
    auto-rotate
    auto-rotate-delay="3500"
    rotation-per-second="<?php echo $rot; ?>"
    <?php endif; ?>
    ...
>
```

### 3.4 Metabox (admin UI)
Add to the existing project-3D metabox:
- Dropdown **"3D camera"** → `Horizontal (recommended)` / `Free 360° (BIM required)`.
- Toggle **"Auto-rotate"** (visible only when "Free 360°" selected).
- Two number inputs **"Min vertical angle (deg)"** / **"Max vertical angle (deg)"** in an "Advanced" `<details>` block, defaulting to the preset values.

### 3.5 REST exposure
Extend `register_post_meta` for `nadlan_project`:
```php
foreach ( [ 'project_3d_camera_lock', 'project_3d_camera_min_polar', 'project_3d_camera_max_polar', 'project_3d_camera_rotation_per_second' ] as $k ) {
    register_post_meta( 'nadlan_project', $k, [ 'type'=>'string', 'single'=>true, 'show_in_rest'=>true, 'auth_callback'=> /*editor*/ ] );
}
register_post_meta( 'nadlan_project', 'project_3d_camera_auto_rotate', [ 'type'=>'boolean', 'single'=>true, 'show_in_rest'=>true, 'auth_callback'=> /*editor*/ ] );
```

Also expose in the showroom-payload REST route already used for Rainbow/Dimri.

## 4. Facade dismissible (JS + CSS)

### 4.1 Markup
Inside `.nlp3d-facade-plane`, before the cell layer:
```html
<button type="button" class="nlp3d-fp-close" aria-label="הסתר חזית" title="הסתר חזית">✕</button>
```

After dismissal, the toolbar gets:
```html
<button type="button" class="nlp3d-fp-restore" aria-label="הצג חזית" hidden>הצג חזית</button>
```

### 4.2 Behavior (vanilla JS, inside existing `nadlan_p3d_inline_js`)
```js
var KEY = 'nlp3d-facade-dismissed-' + projectId;
var fp  = root.querySelector('.nlp3d-facade-plane');
var btn = root.querySelector('.nlp3d-fp-close');
var res = root.querySelector('.nlp3d-fp-restore');

function setDismissed(on){
  root.classList.toggle('nlp3d-facade-dismissed', on);
  if (res) res.hidden = !on;
  try { sessionStorage.setItem(KEY, on ? '1' : '0'); } catch (e) {}
}
if (sessionStorage.getItem(KEY) === '1') setDismissed(true);
if (btn) btn.addEventListener('click', function(){ setDismissed(true); });
if (res) res.addEventListener('click', function(){ setDismissed(false); });
```

### 4.3 CSS
Append a new inline style block at the end of `nadlan_p3d_facade_cell_selector_css()`:
```css
.nlp3d-fp-close{position:absolute;top:8px;inset-inline-start:8px;z-index:20;width:36px;height:36px;border:1px solid rgba(255,247,198,.42);background:rgba(7,15,16,.78);color:#fff7df;font-size:18px;line-height:1;cursor:pointer;border-radius:999px;display:grid;place-items:center}
.nlp3d-fp-close:hover,.nlp3d-fp-close:focus-visible{background:rgba(7,15,16,.96);outline:none;box-shadow:0 0 0 2px rgba(255,247,198,.62)}
.nlp3d.nlp3d-premium.nlp3d-facade-dismissed .nlp3d-facade-plane{display:none!important}
.nlp3d.nlp3d-premium.nlp3d-facade-dismissed .nlp3d-model-viewer{right:0!important;left:0!important;bottom:0!important;top:0!important;width:100%!important;height:100%!important}
.nlp3d-fp-restore{min-height:36px;padding:6px 12px;border:1px solid rgba(234,216,163,.36);background:rgba(7,15,16,.78);color:#fff7df;font-size:13px;font-weight:800;cursor:pointer;border-radius:999px}
.nlp3d-fp-restore:hover,.nlp3d-fp-restore:focus-visible{background:rgba(234,216,163,.18);outline:none;box-shadow:0 0 0 2px rgba(255,247,198,.62)}
```

## 5. Healthcheck flags (per M5/M11 — provable from `/wp-json/nadlan/v1/healthcheck`)

Add to `project_3d` block:
- `camera_lock_default_horizontal_v1676`: `true`
- `camera_cms_controlled_v1676`: `true`
- `facade_dismissible_v1676`: `true`

## 6. Version bump
- Plugin **1.67.6** (above current `1.67.5` on main).
- All 6 surfaces (header, version array, health.php, both register_style/script, manifest + ZIP filename) — per pre-flight in `skill-release-discipline-and-mistakes.md` §2.

## 7. Acceptance gate (Codex provides; Claude re-runs before merge)

| # | Check | Pass criteria |
|---|---|---|
| 1 | Default behavior unchanged on existing projects without meta | All projects render with `camera_lock=horizontal`, polar locked 78–85°, no auto-rotate |
| 2 | Free orbit opt-in works | Setting `camera_lock=free` on a test project allows full vertical orbit + auto-rotate |
| 3 | Facade close button visible | Screenshot at 1440 / 768 / 390 shows the `.nlp3d-fp-close` button top-left |
| 4 | Facade dismissed → model gets full space | Screenshot after clicking ✕ shows the model expanded full bleed |
| 5 | State persists | Reload the page within the session — facade stays dismissed |
| 6 | Healthcheck flags | `curl /wp-json/nadlan/v1/healthcheck` returns the three v1676 flags |
| 7 | No regression on selector | `renderApartmentCells`, `is-facade-select`, `nlp3d-facade-plane` markers still present (the embedded selector survives) |
| 8 | PHP lint / JS check / ZIP guard | All pass per pre-flight §2 |

Screenshots committed at `docs/qa/screenshots/v1676-camera-facade/<viewport>.png` for 1440 / 768 / 390 (M11).

## 8. Honest scope boundaries

- **This does NOT fix Mapbox.** That's a separate runtime defect — Codex needs the Chrome console error first. Tracked in COORDINATION.md §5.
- **This does NOT replace the placeholder GLB.** A massing-box model is still a massing box; locking the camera just stops it from looking *worse*. A real BIM is owner-input.
- **This does NOT change the embedded apartment-cell selector.** The selector is the picker; this change is camera + dismissibility.
- **Penthouse/floor ordering issue** (owner: *"the penthouse looks downstairs, it should be up"*): separate bug — likely an inverted `floor` sort or data error in the unit map. Codex to file a sibling spec; not blocking this PR.

## 9. Out-of-scope but flagged (for the next slice)

- **Facade logic / realism.** Owner: *"the facade has no logic"* + *"has to reflect all the available assets"*. This needs traced polygons keyed to the actual building face + real elevation imagery (Dimri/Rainbow). Tracked in COORDINATION.md §13 as a separate facade-quality slice after the BIM/elevation assets are committed under `assets/projects/<slug>/`.
