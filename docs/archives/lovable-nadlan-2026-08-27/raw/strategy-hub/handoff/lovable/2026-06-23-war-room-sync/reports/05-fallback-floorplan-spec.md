# Report 05 — Fallback floor-plan spec

Sync date: 2026-06-23

## Why this exists

Most contractors in Israel don't ship a clean per-unit floor plan with their
marketing material. The product can't wait for them: without a plan, the unit
drawer is blank and the user bounces. The compromise — and the **only**
compromise — is an illustrative AI-generated placeholder, with rules so it
can't be mistaken for the official plan.

## Three non-negotiable rules

1. **Permanent watermark** rendered as a CSS overlay on every AI plan, in both languages:
   ```
   להמחשה בלבד · נוצר ב-AI   /   Illustrative · AI generated
   ```
   The overlay is implemented as the `watermark-ai-overlay` utility in `src/styles.css`. It's a 45° repeating gradient + centred uppercase label, `pointer-events: none`, never removable from the DOM.

2. **CTA directly beneath the plan** in every surface that renders it:
   - HE: `קבלן: העלה תוכנית רשמית`
   - EN: `Contractor: upload real plan`
   Wired in `MagazineCard.tsx` and `UnitSelector.tsx`.

3. **Never labelled** with phrases like "official plan", "approved plan", "תוכנית מאושרת". The micro-copy is:
   - HE: `התוכנית להמחשה בלבד. הקבלן עדיין לא העלה תוכנית רשמית.`
   - EN: `Plan is illustrative only. Developer has not uploaded an official plan.`

## Generation mode (this run: on-demand only)

- The prototype **does not call an LLM/image model**. The placeholder is a hand-drawn schematic SVG rendered inline — that's enough to demonstrate the UX without consuming credits per project.
- The pattern is documented so the next run can wire `lovable-ai`/`gemini-2.5-flash-image` to generate per-unit plans on demand and cache them.

## Future on-demand pipeline (deferred)

```text
contractor uploads "rough sketch" or text brief
         ↓
server fn (TanStack createServerFn, .ai-gateway)
         ↓
returns 1024×768 PNG, server-side composites the watermark
         ↓
stored in Lovable Cloud → public CDN URL
         ↓
component renders <img> + the same overlay as safety
```

The overlay is rendered **on top in the client** even when the image already
has the watermark baked in — defence in depth.

## Asset-state matrix (cross-ref report 02)

| `asset_state`  | Plan shown                  | Watermark | Upload CTA |
|----------------|-----------------------------|-----------|------------|
| `real-glb`     | real plan if uploaded, else AI placeholder | yes (on AI) | yes (on AI) |
| `facade-svg`   | AI placeholder              | yes       | yes        |
| `empty`        | none — empty state instead  | n/a       | yes        |

## Acceptance gate

- Watermark visible at 390 px on every plan render (mobile drawer, card "Plan" tab)
- Contractor CTA visible in the same viewport — no scrolling required
- Document language switching toggles watermark text without rerendering the SVG

