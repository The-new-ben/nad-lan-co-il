# Nadlan3D prototype source snapshot

This folder is a focused source snapshot from the Lovable TanStack Start prototype at source commit `b275f7a`, plus Codex verification artifacts generated after that commit.

It is not a full app checkout and intentionally excludes `node_modules`, build output, caches, and Lovable internal state.

## Porting read order

1. `src/lib/projects.mock.ts`
2. `src/styles.css`
3. `src/components/nadlan/ShowroomViewer.tsx`
4. `src/components/nadlan/UnitSelector.tsx`
5. `src/components/nadlan/MagazineCard.tsx`
6. `src/routes/showroom.$projectId.tsx`
7. `src/routes/listings.tsx`
8. `src/lib/i18n.ts`
9. `src/lib/lang-context.tsx`

## Important truth note

The prototype includes a slot for `/models/rainbow.glb`, but the GLB payload is not committed here. The WordPress port must use the real WP asset when available or keep the labeled fallback state.
