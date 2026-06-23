# Report 02 — Showroom prototype (Nadlan3D)

Sync date: 2026-06-23
Lovable run: showroom + listings + sitewide IA (single-run, cream luxury, HE+EN)

## Goal

A 3D showroom for every project — verifiable asset truth, mobile-first, RTL real.

## Route

`/showroom/$projectId` (TanStack file route: `src/routes/showroom.$projectId.tsx`).
Loader: `projectBySlug` from `src/lib/projects.mock.ts`. Throws `notFound()` for unknown slugs.

## Layout

```text
breadcrumbs
title · city · developer · tagline
┌──────────────────────────┬────────────┐
│  ShowroomViewer          │  UnitList  │
│  (16:9 / 16:10 mobile)   │  (cards)   │
└──────────────────────────┴────────────┘
buyer-journey strip (4 steps, numbered)
sticky bottom CTA dock (WhatsApp + contact)
```

## Asset truth gradient (the demo the run was built around)

| Project          | `asset_state` | Renderer                                          |
|------------------|---------------|---------------------------------------------------|
| Rainbow Tower    | `real-glb`    | `<model-viewer>` (dynamic CDN import) + GLB       |
| Dimri Yama       | `facade-svg`  | Inline CSS-extrude SVG, "schematic" label         |
| Carmel Heights   | `facade-svg`  | Same SVG generator with project-specific seed     |
| Kiryat Yam       | `empty`       | "Awaiting developer asset upload" empty-state CTA |

The viewer never silently swaps a fake for a real model. The state label is rendered explicitly in the viewer footer.

## Unit selector

- List, not a 3D click-target (mobile reliability over wow factor)
- Click opens **bottom-sheet** on mobile, centred dialog on `sm+`
- Drawer shows: floor plan with permanent **AI watermark**, price, room/sqm, two CTAs + contractor-upload link

## Floor-plan fallback (cross-reference: report 05)

Every drawer and listing card renders an **inline SVG placeholder** with the watermark overlay:

```
להמחשה בלבד · נוצר ב-AI   /   Illustrative · AI generated
```

CTA right under the plan: **"קבלן: העלה תוכנית רשמית" / "Contractor: upload real plan"**. Never labelled as the official plan. Generation itself is mocked in the prototype.

## Mobile acceptance

- Verified at 390 px (no horizontal scroll)
- Bottom-sheet behaviour on `< sm` breakpoint
- Sticky CTA dock collapses to icon-only on narrow widths

## Tech notes

- `<model-viewer>` loaded via `import(/* @vite-ignore */ webpackIgnore url)` inside `useEffect` — never SSRed
- Facade SVG is procedural (no external assets) so the prototype works offline
- All copy goes through `useLang()` / `t()` (HE default, EN toggle)
- Head meta per route includes per-leaf `canonical` + HE/EN `hreflang` alternates, plus `og:image` from `project.hero_image` (leaf-only, never on root)

## Out-of-scope this run

Real upload pipeline, Matterport, contractor backoffice, payments. AI plan generation is mocked — only the **presentation** of an AI plan with watermark is built.
