# Source Manifest - Public Language Cleanup

Date: 2026-06-23

## Source

- Repository: `https://github.com/The-new-ben/nadlan-strategy-hub`
- Branch: `main`
- Base commit before this cleanup: `f063cce`
- Local preview URL used for screenshots: `http://127.0.0.1:5187`

## Files changed in prototype source

- `src/lib/i18n.ts`
- `src/lib/projects.mock.ts`
- `src/components/nadlan/MagazineCard.tsx`
- `src/components/nadlan/ShowroomViewer.tsx`
- `src/components/nadlan/SiteFooter.tsx`
- `src/components/nadlan/UnitSelector.tsx`
- `src/routes/__root.tsx`
- `src/routes/about.tsx`
- `src/routes/cities.$city.tsx`
- `src/routes/contact.tsx`
- `src/routes/guides.tsx`
- `src/routes/index.tsx`
- `src/routes/listings.tsx`
- `src/routes/showroom.$projectId.tsx`

## Evidence

- Report: `reports/visual-qa.md`
- HTML gallery: `exports/public-language-cleanup-visual-qa.html`
- Scan data: `data/rendered-text-and-overflow-scan.json`
- Screenshot folder: `screenshots/`

## Verification

- `npm run build` passed.
- 18 screenshots captured.
- Rendered public text scan returned zero banned term hits.
- Overflow scan returned zero failures in captured states.

## Remaining product risks

- Generic demo project photos are still present.
- Real 3D model file is missing, so the project tour correctly shows a pending model state.
- The fallback facade is not a premium final showroom.
- Brand mark and final naming still need a dedicated identity pass.
