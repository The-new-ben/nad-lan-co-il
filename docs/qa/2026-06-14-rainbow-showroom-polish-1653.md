# Rainbow Showroom Polish v1.65.3 QA

## Scope

This slice responds to the owner screenshot where the real GLB and the older procedural tower were
visible together, the model opened too far away and spun too fast, apartment picking felt unclear,
and light headings below the showroom lacked contrast.

## SERP / Copy Inputs

Fresh search checks before rewriting the intro showed the strongest public language around:

- Official Rainbow / Israel Canada pages: `Rainbow Tel Aviv`, `שדה דב`, `ישראל קנדה`,
  resort-style residence, sea proximity and amenities.
- Madlan result: developer Israel Canada, new construction, 7 buildings, 8-40 floors, 459 units,
  `בריכת אינפיניטי`, `2 דקות מהים`, `סמוך לרכבת הקלה`.
- SdeDov.co.il result: `ריזורט המגורים`, view to sea and Tel Aviv skyline, pools, spa, fitness,
  permit received.
- Calcalist / Ynet price coverage: public interest is price-led, with reported averages and
  high-profile transactions. Public copy must keep every price as an estimate or sourced fact.

The new intro therefore uses natural buyer phrases: `דירות למכירה ב-Rainbow Tel Aviv`, `שדה דב`,
`ישראל קנדה`, `מחירים`, `זמינות`, `מגדל`, `בנייני בוטיק`, `קרבה לים`, and `אומדן לא מחייב`.

## Code Changes

- GLB camera starts closer and calmer: `field-of-view="24deg"`, `camera-target="0m 56m 0m"`,
  `rotation-per-second="8deg"`, `auto-rotate-delay="3500"`.
- After `model-viewer` loads, the old `.nlp3d-tower`, `.nlp3d-facade`, sea, runway, horizon and
  shadow fallback layers are `display:none`; they return only on model error.
- Apartment stage markers keep 54-56px hit targets, status colors, recommended pulse only when the
  unit is available, sold-unit blocking, hover/focus/tap tooltip styling, and one-click selection.
- Selected apartment card gets mobile sheet handling and stage tabs that reuse the existing tool
  panels instead of creating another UI.
- Project body headings and the old `.nlpf-name` get dark text contrast on light backgrounds.
- Health flags added: `serp_intro_copy_v1653`, `model_fallback_hides_after_glb_v1653`,
  `hotspot_tap_preview_v1653`, `heading_contrast_v1653`.

## Local Gate

```text
node --check scripts/qa-project-showroom-live.mjs
node --check scripts/qa-project-showroom-visual.mjs
node -e "... extract nadlan_p3d_inline_js ... new Function(js)"
inline JS ok 60291

node scripts/validate-project-showroom-payload.mjs --payload assets/projects/rainbow-tel-aviv/showroom-payload.json
errors: []
units: 6
drawings: 6

git diff --check
clean except Windows CRLF warnings

plugin-dist/nadlan-config-1.65.3.zip
root: nadlan-config/
backslash_paths=0
markers present: field-of-view="24deg", selectUnit(u.id,source||'stage-pick'),
model_fallback_hides_after_glb_v1653
```

PHP lint is not available in this Windows shell (`php` is not on PATH).

## Live Baseline Before Deploy

Live healthcheck still reported `version: 1.64.6` during this QA, so the live page does **not** yet
contain the v1.65.3 fixes.

Live DOM before deploy confirmed the owner's screenshot:

- `<model-viewer>` exists, but still has old attrs: `field-of-view="30deg"`,
  `rotation-per-second="18deg"`, `camera-target="0m 68m 0m"`.
- `.nlp3d-tower` after GLB load is still `display:block`, `opacity:0.9`, `visibility:visible`.
- `.nlp3d-intro` is not present.
- One H1 and no horizontal page overflow were okay.

Visual harness baseline against live 1.64.6 wrote screenshots to:

`docs/qa/screenshots/rainbow-1653-before-live/`

It failed as expected on:

- selected apartment card did not reveal on one click,
- mobile/Edge root was slightly cropped,
- public-text scan still detected internal wording in the current live build.

These failures are the reason this v1.65.3 package exists. They must be re-run after deploying
v1.65.3.

## Post-Deploy Gate

After WordPress updates to v1.65.3:

1. Healthcheck version is `1.65.3`.
2. `project_3d.serp_intro_copy_v1653` and
   `project_3d.model_fallback_hides_after_glb_v1653` are true.
3. Chrome at 1440 / 768 / 390 / Edge-mobile:
   - intro appears above the showroom,
   - model opens closer and rotates gently,
   - old fallback tower is not visible after GLB load,
   - one click on an apartment marker opens the selected-apartment card,
   - sold markers do not select,
   - no horizontal overflow,
   - headings below the showroom are readable on the light page.
