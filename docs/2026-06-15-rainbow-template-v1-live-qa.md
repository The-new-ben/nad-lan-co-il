# Rainbow Template v1 Live QA

Date: 2026-06-15  
URL: `https://nad-lan.co.il/projects/rainbow-tel-aviv/`  
Plugin state checked: live healthcheck reports `version: 1.66.2`.

## What Passed

- The live page returns HTTP 200.
- One visible H1 was detected by the visual harness.
- `model-viewer` is defined in Chrome.
- One `<model-viewer>` instance exists.
- Six visible apartment cells exist.
- Tap targets are at least 44px in the current harness.
- The hero image still exists on the server:
  `https://nad-lan.co.il/wp-content/uploads/2026/06/rainbow-tel-aviv-hero.jpg` returns HTTP 200.
- `og:image` points to the Rainbow hero image.

## What Failed

Fresh command:

```powershell
node scripts/qa-project-showroom-visual.mjs `
  --site https://nad-lan.co.il `
  --slug rainbow-tel-aviv `
  --out docs/qa/screenshots/rainbow-template-v1-audit `
  --strict
```

Result: `0 passed / 4 failed`.

Failing viewports:

- `desktop-1440`
- `tablet-768`
- `mobile-390`
- `edge-mobile-390`

## Confirmed Real Issues

### 1. Public Internal Language

The page contains public wording equivalent to "lead panel":

> all apartment clicks, view requests, plan requests or purchase checks can enter the lead panel
> instead of disappearing in an undocumented WhatsApp conversation.

This violates the NadLan public-copy rule. Public wording should say "organized inquiry",
"developer follow-up", or "project contact request", not "lead panel".

### 2. Mobile Crop / Shift

On `mobile-390` and `edge-mobile-390`, the showroom root was measured as:

```json
{ "x": 183.5, "width": 362, "right": 545.5 }
```

That means the element is visually shifted outside the 390px viewport, even though the document
does not report horizontal scroll. This is likely a transform/margin/cascade issue, not content
width alone.

### 3. Selected State Collapses The Scene

After selecting the first apartment on mobile, the scene was measured as:

```json
{ "width": 340, "height": 2 }
```

The selected card appears, but the model/facade effectively collapses. This is not acceptable for a
buyer showroom; the selected card must not remove the product view.

### 4. Heading/Paragraph Visual Alignment

The owner repeatedly reports that headings and paragraphs do not sit in the same readable column.
The CSS currently has multiple late inline overrides for project headings and paragraphs. Template
v1 must enforce one shared content column for `h2`, `h3`, paragraphs, lists and tables under the
single project page.

## Likely Source Areas

- Public wording: Rainbow showroom copy in `plugins/nadlan-config/inc/project-3d.php` or the seeded
  project content.
- Mobile crop: late inline mobile CSS in `project-3d.php`, especially rules that set
  `transform:none!important` while the runtime nudge uses `--nlp3d-mobile-nudge`.
- Scene collapse: mobile selected-card rules that change `.nlp3d-stage-wrap.has-stage-selection`
  and `.nlp3d-scene` sizing.
- Heading alignment: project single-page typography overrides in the same module, plus block-theme
  constrained layout interactions.

## Next Surgical Fix Slice

1. Replace the public internal wording with buyer/contractor language.
2. Restore mobile nudge behavior after all late CSS, or remove the need for JS nudge by fixing the
   mobile margins directly.
3. Override selected mobile state so the scene keeps a real height after unit selection.
4. Dock the selected-apartment card so it does not block the active facade cells.
5. Force project article headings and paragraphs into one shared readable column.
6. Re-run the same visual harness and only then decide whether the template can move toward the
   next project.
