# Report 04 — Brand direction: Nadlan3D

Sync date: 2026-06-23
Status: **working prototype direction — not legal or domain clearance**

## Wordmark

`Nadlan` set in Frank Ruhl Libre 500 (Hebrew-native editorial serif), with a
gold (`#9C7A3C` / `oklch(0.595 0.085 75)`) **`3D`** superscript set in Inter
Tight 600. Hairline rule underneath, 0.5 px stroke at 40 % opacity. Exported as
the SVG component `src/components/nadlan/Nadlan3DMark.tsx` (variants: `full`
and `mark`).

The Hebrew display face is Frank Ruhl Libre and the body face is Heebo. The
mark is designed so the same composition reads in HE (`נדל"ן 3D` lockup) and
in EN (`Nadlan 3D` lockup) without changing proportions.

## Taglines

- **HE**: נדל״ן שרואים לפני שקונים
- **EN**: Real Estate, Rendered Real

## Domain posture

| Use            | Domain                  | Status          |
|----------------|-------------------------|-----------------|
| Primary        | `nadlan3d.com`          | not verified    |
| AI concierge   | `nadlan.ai`             | not verified    |
| Fallback HE    | `nadlan3d.co.il`        | not verified    |

**No domain has been checked at a registrar.** Treat this as a brand direction the prototype is built around; legal/availability clearance is a separate step before any external launch.

## Alternative names (if `Nadlan3D` is blocked)

1. **Plana** — neutral, exportable, evokes "plan" + "plane"
2. **Tavnit** (תבנית) — Hebrew for "blueprint/template", short, ownable
3. **Nadlan Live** — keeps the category in the name, signals real-time / real models

Each would require the same availability check.

## Risk notes

- `nadlan*` is a crowded Hebrew namespace — short suffixes are likely taken
- `.ai` registry pricing is significantly higher than `.com` / `.co.il`
- Trademark in Israel (kind 36/41) should be filed before marketing spend
- The wordmark uses Frank Ruhl Libre under SIL OFL — safe for commercial use; Fraunces and Heebo are also OFL

## Visual system reference

- Tokens skill: `handoff/shared-knowledge/skills/nadlan-editorial-bright-tokens.md`
- Card pattern: `handoff/shared-knowledge/skills/nadlan-magazine-card.md`
- Ranking rule: `handoff/shared-knowledge/skills/nadlan-listings-ranking.md`

These three skills are the shared knowledge so other agents (Codex on WordPress, future Lovable runs) inherit the same tokens, ranking, and card pattern.

