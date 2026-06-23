# Codex Visual QA - Nadlan3D Lovable Prototype

Date: 2026-06-23

Source commit checked: `b275f7a`

Verification commit in Lovable hub with screenshots: `eaaba35`

Status: prototype exists, build passes, visual result is not contractor-ready yet.

## Screenshot Set

Captured and saved under `handoff/lovable/2026-06-23-war-room-sync/screenshots/`.

Hebrew and core state coverage:

- `home-mobile-390.png`
- `home-desktop-1440.png`
- `home--he--mobile-menu-open--mobile-390.png`
- `listings-mobile-390.png`
- `listings-desktop-1440.png`
- `showroom-rainbow-mobile-390.png`
- `showroom-rainbow-desktop-1440.png`
- `showroom-dimri-mobile-390.png`
- `showroom-dimri-desktop-1440.png`
- `showroom-empty-mobile-390.png`
- `showroom-empty-desktop-1440.png`
- `city-tel-aviv--he--default--mobile-390.png`
- `city-tel-aviv--he--default--desktop-1440.png`

English coverage:

- `home--en--default--mobile-390.png`
- `home--en--default--desktop-1440.png`
- `home--en--mobile-menu-open--mobile-390.png`
- `listings--en--default--mobile-390.png`
- `listings--en--default--desktop-1440.png`
- `showroom-rainbow--en--glb-state--mobile-390.png`
- `showroom-rainbow--en--glb-state--desktop-1440.png`
- `city-tel-aviv--en--default--mobile-390.png`
- `city-tel-aviv--en--default--desktop-1440.png`

## What Passed

1. The app is real in GitHub. The routes, components, reports, and shared skills exist in `nadlan-strategy-hub/main`.
2. `npm run build` passes locally.
3. Hebrew and English modes render.
4. The responsive shell works at 390px and 1440px without obvious horizontal scroll in the captured routes.
5. Paid labels are visible: Featured, Sponsored, Promoted, Standard.
6. The missing-asset state exists and asks for contractor upload.
7. City pages exist in Hebrew and English.
8. The mobile menu opens and is readable.

## Visual Failures

0. Internal implementation language is visible in public UI.
   - The owner-provided Lovable preview screenshot shows public text such as `Showroom`, `GLB`, `RTL`, `390px`, font names, and `Featured / Sponsored / Promoted`.
   - These belong in internal reports, not buyer-facing pages.
   - Fix: apply `handoff/shared-knowledge/skills/nadlan-public-language-cleanup.md`.

1. Rainbow is marked as GLB/live but no real `rainbow.glb` payload exists in this Lovable repo.
   - In screenshots, Rainbow still shows a schematic loading facade.
   - This must not be presented as a working 3D model.
   - Fix: only show GLB/live when the model element actually loads.

2. Top listing images are not trustworthy enough.
   - Several cards use generic stock-style photos that do not prove the actual project.
   - Some Hebrew mobile and desktop captures show blank beige image blocks.
   - Important project results need real project pictures, researched source images, or a premium missing-state.
   - Do not use unrelated villas, interiors, or skyline images as if they are project images.

3. Dimri facade is too generic.
   - The fallback communicates the asset state, but visually it is a simple schematic building.
   - It is not good enough for a contractor-facing pitch.
   - Fix: use a real facade render, traced SVG, or a high-quality clearly labeled concept image.

4. Sticky CTA overlaps the footer on showroom pages.
   - The WhatsApp and contact dock sits over footer content in mobile and desktop screenshots.
   - Fix: add bottom spacing on pages with the fixed dock, or make the dock context-aware near the footer.

5. Brand signal is still weak.
   - The header reads mostly as `Nadlan` with a small `3D` mark.
   - For the pitch, Nadlan3D must be visible as a strong first-viewport product signal.

6. Public copy still has polishing issues.
   - Some copy mixes Hebrew with English product and implementation terms.
   - Some English copy uses em dash style punctuation.
   - New owner-facing and public copy should avoid em dashes and generic AI-sounding filler.
   - Paid placement should be disclosed with public labels such as `ממומן`, `מודעה`, `Ad`, or `Sponsored`, not with an internal ranking taxonomy.

7. Plan and facade tabs were not fully interaction-tested.
   - The screenshots show the tab labels, but not a verified selected plan state.
   - The next run should capture tab switching and selected unit state.

## Current Decision

This Lovable prototype is useful as a direction and implementation reference, not as a final design.

Codex should port only the useful structure:

- route map
- language shell
- ranking transparency
- asset-truth state machine
- missing-asset CTA
- cream-luxury token direction

Codex should not port these visual weaknesses:

- generic project images
- blank image blocks
- schematic facade as final artwork
- GLB/live label without a real loaded model
- footer overlap
- weak Nadlan3D brand presence

## Next Visual Work

1. Replace top project images with real or source-researched imagery.
2. Add real `rainbow.glb` or downgrade Rainbow to an honest fallback state.
3. Rebuild Dimri facade from a real render or traced concept.
4. Fix sticky CTA spacing.
5. Strengthen Nadlan3D logo and first-viewport brand signal.
6. Capture plan-tab and unit-selected states.
7. Re-run the full screenshot set after fixes.

## Owner Lovable Preview Evidence

The owner-provided Lovable preview screenshot is saved as:

`screenshots/owner-lovable-preview-homepage-2026-06-23.png`

It confirms the prototype has reached Lovable preview, but it also confirms the public-language problem.
