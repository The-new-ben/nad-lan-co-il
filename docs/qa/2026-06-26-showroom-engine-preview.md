# Showroom Engine Preview QA

Date: 2026-06-26

Preview:

- `docs/previews/nadlan-showroom-engine-preview.html`

Screenshot folder:

- `docs/qa/screenshots/showroom-engine-preview-2026-06-26/`

Command:

```bash
npm run qa:showroom-engine-preview
```

Result:

- `ok: true`
- no console page errors
- no horizontal overflow at desktop, tablet, mobile or Edge-mobile widths
- visible Hebrew rendered correctly
- buyer copy only in the rendered preview
- model-viewer registered
- selected project and selected apartment flows rendered

Screenshots checked:

- `desktop-1440-initial.png`
- `desktop-1440-selected.png`
- `mobile-390-selected.png`

Buyer-language gate:

The QA script fails visible text containing internal words such as SEO, CMS, CRM, lead, engine,
template, prototype, project manager, supplier, contractor, funnel-style Hebrew words, or working
phrases such as `מקום שמור` and `פרויקטים לבדיקה`.

Honest limitation:

This is a preview proof, not a live WordPress deployment. The included GLB files are prototype
massing assets. Apartment-level picking on the spinning model requires a segmented/named GLB or BIM
conversion where apartments or floors are real meshes.
