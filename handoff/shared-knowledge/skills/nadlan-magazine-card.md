---
name: nadlan-magazine-card
description: Nadlan3D magazine-card pattern — dual-image (facade / floor-plan tabs), transparency badges, mini-stats, asset-state indicator. Use this card wherever projects are listed; never hand-roll a different card.
type: feature
---

# Nadlan3D — magazine card

Reference component: `src/components/nadlan/MagazineCard.tsx`.

## Anatomy

```text
┌─────────────────────────────────┐
│ [Featured][Sponsored]   [F][P] │  ← top-row badges (left) + facade/plan tabs (right)
│                                 │
│        facade or plan           │  ← dual-image area, aspect 4:3
│        (with watermark          │
│         when AI plan)           │
│                                 │
├─────────────────────────────────┤
│  Title                  CITY    │
│  Tagline (2 lines max)          │
│  ─────────────────────────────  │  hairline divider
│  From  |  Rooms  |  Complete %  │  mini-stats grid
│  ─────────────────────────────  │
│  [Enter Showroom]      ● GLB    │  primary CTA + asset-state dot
└─────────────────────────────────┘
```

## Required props

```ts
{ project: Project }
```

`Project` is the shape in `src/lib/projects.mock.ts` — also the shape the
WordPress endpoint will return.

## Required behaviours

- **Dual-image tabs**: user can flip between facade and floor plan inline (no navigation)
- **AI plan watermark**: when showing the plan tab, the overlay (`watermark-ai-overlay`) is mandatory
- **Transparency badges** (see skill `nadlan-listings-ranking`): paid tiers always carry a visible chip; `featured` and `promoted` carry an extra `Sponsored` chip
- **Asset-state dot**: `● GLB` / `○ SVG` / `· empty` rendered in the CTA row, with `title=` tooltip giving the full description
- **Language-aware**: name, city, tagline, currency formatter all switch on `useLang()`
- **Mobile-safe**: title `truncate`, tagline `line-clamp-2`, top-row uses `start-*`/`end-*` so it RTL-mirrors

## Hover affordance

- Image scales `1.02` over 500 ms
- Card lifts via `shadow-[0_8px_24px_-12px_rgba(27,26,23,0.18)]`
- No colour shift (cream-luxury is monochrome by default)

## Where it is used

- `/listings` grid
- `/cities/$city` grid
- Homepage featured strip (first three after `rankProjects`)

## Anti-patterns

- Replacing the card per surface — the card is the single point of trust
- Removing the asset-state dot to "make it cleaner" — that dot is the asset-truth promise
- Adding an inline price slider or other interactive widget — the card stays a read-only summary; interaction lives in the showroom
