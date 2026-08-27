# Owner Approval Prompt For Lovable Build

Paste this into Lovable after its scope proposal.

```text
PROCEED FULL RUN.

Approved to start building under your locked single-run scope, with the guardrails below. This approval is for the TanStack Start Lovable prototype run, estimated 45-65 credits.

Build:

1. Interactive showroom prototype.
2. Listings page with magazine cards and ranking hierarchy.
3. Sitewide IA: nav, homepage, breadcrumbs, hub pages.
4. Editorial-bright design system.
5. Nadlan3D brand direction with .ai positioning.
6. Sync all outputs to GitHub so Codex can mirror into WordPress.

Important output folder:

Use:

handoff/lovable/2026-06-23-war-room-sync/

Append to the existing package. Do not delete or overwrite existing reports unless you are updating source-manifest.md intentionally. Add new reports, screenshots, data, prototype notes, and manifest entries. If you need a separate prototype subfolder, create it inside that folder.

Required reports:

- reports/02-showroom-prototype.md
- reports/03-listings-ia.md
- reports/04-brand-nadlan3d.md
- reports/05-fallback-floorplan-spec.md

Required shared skills:

- handoff/shared-knowledge/skills/nadlan-editorial-bright-tokens.md
- handoff/shared-knowledge/skills/nadlan-listings-ranking.md
- handoff/shared-knowledge/skills/nadlan-magazine-card.md

Also create or update source-manifest.md with every file you add.

Critical corrections and guardrails:

1. Hebrew fonts: Fraunces and Inter Tight are not enough for Hebrew UI. Use Hebrew-capable fonts for RTL Hebrew:
   - Hebrew display: Frank Ruhl Libre, Noto Serif Hebrew, or another Hebrew-capable editorial serif.
   - Hebrew body/UI: Heebo, Assistant, Noto Sans Hebrew, or another Hebrew-capable clean sans.
   - Fraunces and Inter Tight may be used for English/LTR brand accents only if they render correctly.
   - Do not ship Hebrew screens where the main type falls back unpredictably.

2. Nadlan3D is approved as a working prototype brand direction, not a final legal/domain claim. Include availability-risk notes and alternatives. Do not claim legal clearance for nadlan3d.com, nadlan.ai, trademarks, or social handles.

3. Dubai/Cyprus/Greece/Thailand landings are deferred only as coded pages in this run. They are not excluded from the strategy. Keep IA/backlog hooks for outbound investment markets and note them in the report.

4. War Room dashboard is deferred only as a coded screen in this run. Include a concise future-run outline in the report.

5. Paid ranking: if paid tier affects listing order, the UI/spec must include public transparency labels such as Featured/Sponsored/Promoted where appropriate. Do not create hidden paid placement that looks organic.

6. AI floor-plan fallback is allowed only as an explicitly illustrative placeholder:
   - permanent watermark: "Illustrative - AI generated"
   - clear CTA: "Contractor: upload real plan"
   - never present generated plans as official floor plans.

7. Asset truth remains mandatory:
   - real GLB -> model-first
   - facade only -> facade-first, labeled
   - nothing -> premium missing-state
   - no fake map, no fake facade, no fake Matterport, no fake legal/tax/mortgage/investment advice.

8. Mobile acceptance is mandatory:
   - verify 390px
   - no horizontal overflow
   - bottom sheet for unit details
   - footer dock actions must fit and not feel cheap.

9. Preserve full-market ambition. This run focuses on showroom/listings/IA/design because of credits, but the reports must not say NadLan avoids hard markets or hard keywords. Hard means phased, not excluded.

10. If credits cross roughly 55 mid-build, pause and report what is done, what remains, and the estimated incremental credits before continuing.

After the build, commit and push to:

https://github.com/The-new-ben/nadlan-strategy-hub
branch: main

Return:

1. exact commit hash
2. changed file list
3. preview URL if available
4. screenshot list
5. any missing acceptance gates
```

