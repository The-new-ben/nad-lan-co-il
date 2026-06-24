# 07 Codex Build Plan

Small PRs only. Do not stack more CSS over the old design. Replace the active design source.

## PR 1: showroom premium visual replacement

### Goal

Replace the old active showroom shell with the premium NadLan3D shell.

### Files likely touched in WordPress

- `plugins/nadlan-config/inc/project-3d.php`
- Showroom stylesheet currently emitted or enqueued by the plugin.
- Plugin asset enqueue file if one exists.
- `plugins/nadlan-config/nadlan-config.php` for version bump only.
- `plugins/nadlan-config/inc/health.php` for version flag only.

### Remove or stop loading first

- Old dark teal showroom stylesheet.
- Inline duplicate stage card styling in the PHP renderer.
- Any obsolete CSS that defines the previous selected card shell.

### Add

- `nl3d-showroom-grid`
- `nl3d-stage`
- `nl3d-unit-pin`
- `nl3d-unit-rail`
- `nl3d-selected-panel`
- `nl3d-contact-strip`

### Screenshot proof required

- Desktop 1440 before replacement.
- Desktop 1440 after replacement.
- Mobile 390 after replacement.
- Mobile 390 scroll width proof.

### Acceptance criteria

- Cream editorial design visible.
- Building is the visual center.
- Selected panel visible and styled.
- Mobile 390 has no horizontal overflow.
- No banned public terms.

### What not to touch

- Do not rewrite the selection resolver.
- Do not change REST routes.
- Do not change project data schema.

### Rollback risk

Medium. Visual replacement touches the main sales page. Keep the previous stylesheet load behind one version flag for quick rollback.

### Public-language checks

Scan rendered text for the banned list and em dash.

## PR 2: apartment selection UX and selected state

### Goal

Make selected apartment behavior feel intentional, not patched.

### Files likely touched

- `plugins/nadlan-config/inc/project-3d.php`
- Inline showroom script or extracted showroom JS.
- Showroom stylesheet.

### Keep

- 1.69.32 authored-unit selection and row-aligned surface tap behavior.

### Add

- Selected unit updates pin, unit rail card and selected panel together.
- Empty selected state.
- Disabled or sold visual state.
- Keyboard activation for unit buttons.

### Screenshot proof required

- Desktop selected unit 16 from marker.
- Desktop selected unit 16 from raw surface tap.
- Mobile 390 selected unit 16 from marker.
- Mobile 390 selected unit 16 from raw surface tap.
- Screenshot must show selected card and highlighted pin.

### Acceptance criteria

- The selected apartment name matches the highlighted unit.
- Camera movement does not hide the building.
- Selected panel opens or updates without layout jump.
- The UI never claims exact every-window picking.

### What not to touch

- Do not add a new selection algorithm unless the current handler fails proof.
- Do not expose technical labels to buyers.

### Rollback risk

Medium. Interaction changes can regress the owner-critical unit 16 test.

### Public-language checks

No technical source words in labels, buttons or status copy.

## PR 3: projects archive premium cards

### Goal

Make `/projects/` feel like a premium project shelf, not a listing board.

### Files likely touched

- `plugins/nadlan-config/inc/directory.php`
- `plugins/nadlan-config/inc/directory-assets.php`
- Archive CSS.

### Remove or stop loading first

- Old listing-board card skin.
- Any card labels that expose internal ranking tiers.

### Add

- Fixed media aspect ratio.
- Project facts grid.
- Clear showroom CTA.
- Public disclosure only when an item is paid.

### Screenshot proof required

- Desktop archive.
- Mobile 390 archive.
- One card with missing asset state.
- Text scan proof.

### Acceptance criteria

- Cards are not cluttered.
- Project name, city, developer and availability are visible.
- CTA is clear.
- Mobile cards are single column.

### What not to touch

- Do not change ranking logic.
- Do not change search endpoints.

### Rollback risk

Low to medium.

### Public-language checks

Do not show internal tier names to buyers.

## PR 4: homepage and brand shell

### Goal

Make NadLan3D clear in the first viewport as a showroom product.

### Files likely touched

- WordPress home template.
- Header template or plugin header injection.
- Shared premium stylesheet.

### Remove or stop loading first

- Generic hero section.
- Any copy that describes internal mechanics.

### Add

- Strong wordmark.
- Hero showing the showroom product.
- Buyer path and developer path.
- Three project preview cards.

### Screenshot proof required

- Desktop homepage.
- Mobile 390 homepage.
- Header closeup.

### Acceptance criteria

- Brand visible in first viewport.
- Showroom is the product, not a side feature.
- No card-inside-card hero.
- Mobile shows next section hint.

### What not to touch

- Do not change payment, account or directory logic.

### Rollback risk

Medium.

### Public-language checks

No generic filler. No internal team language.

## PR 5: favicon, app icons, OG card

### Goal

Replace generic site identity with NadLan3D identity.

### Files likely touched

- WordPress media uploads or theme assets.
- Header metadata hook.
- SEO plugin settings if active.

### Add

- `favicon-32.png`
- `favicon-192.png`
- `apple-touch-icon-180.png`
- `og-card.png`

### Screenshot proof required

- Browser tab favicon if visible.
- HTML head source showing icon links.
- Social debugger screenshot if available.

### Acceptance criteria

- Icons are not blurry.
- OG card uses cream, ink and gold.
- Project pages can override OG later.

### What not to touch

- Do not edit unrelated SEO titles.

### Rollback risk

Low.

### Public-language checks

OG text must be clean and short.

## PR 6: mobile 390 QA and public-language cleanup

### Goal

Prove the shipped result is safe to show.

### Files likely touched

- Only files required to fix issues found in QA.

### Screenshot proof required

- Homepage 390.
- Projects 390.
- Showroom 390 before selection.
- Showroom 390 after unit 16 marker selection.
- Showroom 390 after unit 16 raw surface selection.
- Desktop showroom after unit 16 raw surface selection.
- Public text scan report.
- Horizontal overflow report.

### Acceptance criteria

- scrollWidth equals innerWidth at 390.
- No banned terms.
- No em dash.
- Selected unit text, highlighted pin and selected rail item match.
- Inquiry action visible.

### What not to touch

- No new feature work.
- No new design changes unless they fix QA failure.

### Rollback risk

Low.

### Public-language checks

Must pass before owner demo.
