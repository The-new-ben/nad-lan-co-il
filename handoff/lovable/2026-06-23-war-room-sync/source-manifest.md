# Source manifest ג€” Lovable ג†’ WordPress handoff

Sync date: 2026-06-23

## Source (Lovable)

- **Lovable project id:** `a7493b94-2e46-4d38-9c6a-80dcf0905f45`
- **Lovable project URL:** https://lovable.dev/projects/a7493b94-2e46-4d38-9c6a-80dcf0905f45
- **Source GitHub repo URL:** https://github.com/The-new-ben/nadlan-strategy-hub
- **Source branch:** `main` (Lovable's default mirror branch)
- **Source commit hash:** _auto ג€” written by Lovable when this commit lands; read latest from `https://github.com/The-new-ben/nadlan-strategy-hub/commits/main`._

## Destination (WordPress repo, owned by Codex)

- **Destination repo:** https://github.com/The-new-ben/nad-lan-co-il
- **Destination branch:** `strategy/nadlan-seo-product-war-plan`
- **Destination folder:** `handoff/lovable/2026-06-23-war-room-sync/`
- **Reference commit already created by Codex:** `0d1381c`

## How Codex fetches this

```bash
git clone --branch main --depth 1 \
  https://github.com/The-new-ben/nadlan-strategy-hub /tmp/lovable-src

# verbatim copy ג€” same path on both sides, no rewriting
rsync -a --delete \
  /tmp/lovable-src/handoff/lovable/2026-06-23-war-room-sync/ \
  <wp-repo>/handoff/lovable/2026-06-23-war-room-sync/

cd <wp-repo>
git checkout strategy/nadlan-seo-product-war-plan
git add handoff/lovable/2026-06-23-war-room-sync
git commit -m "sync: lovable war-room 2026-06-23"
git push origin strategy/nadlan-seo-product-war-plan
```

Re-run the same block on every subsequent Lovable update ג€” the folder is the canonical surface.

## Files synced in this batch

`reports/` (7 markdown files, all the strategy/advisor output to date):

- `reports/plan.md` ג€” the master 8-report plan + scope, anomalies, contractor kit schema.
- `reports/00-strategy-brief.md` ג€” one-page thesis, target users, what we are / aren't, sequencing.
- `reports/01-showroom-redesign.md` ג€” core UX deliverable: 4-layer mobile-first 3D showroom spec for Dimri Yama, Rainbow Tel Aviv, + urban-renewal pilot.
- `reports/advisor-notes.md` ג€” running decision log, newest at top, includes WP-team anomalies.
- `reports/rest-api-map.md` ג€” every `nadlan/v1` + `auctions/v1` route ג†’ handler file:line + live probe result.
- `reports/repo-inventory.md` ג€” area-by-area code map of the WordPress repo.
- `reports/report-3a-real-semrush.md` ג€” real Semrush KD/volume/CPC data driving the money-page sequence.

`exports/`, `screenshots/`, `data/` ג€” `.gitkeep` only. See "Missing assets" below.

## Missing assets / not yet produced

- **No screenshots.** Earlier read-only Lovable sessions captured home, `/project/dimri-yama/`, `/project/rainbow-tel-aviv/` but those captures were not persisted to the repo. Regeneratable on request via Playwright.
- **No keyword CSV/XLSX.** All Semrush data lives inline as markdown tables inside `reports/report-3a-real-semrush.md`. No raw export.
- **No PDFs, ZIPs, HTML exports.**
- **Reports not yet drafted** (queued ג€” outlined in `reports/plan.md`):
  - `02-design-system.md`
  - `03-content-architecture.md`
  - `04-monetization-playbook.md`
  - `05-foreign-buyer-engine.md`
  - `06-lead-ops.md`
  - `07-seo-money-pages.md`
- **Contractor onboarding kit** (the ZIP schema described in `plan.md` ֲ§"What the contractor feeds") ג€” schema is specified; no example bundle built yet.
- **3rd pilot slug** for the urban-renewal / ׳×׳׳ 38 showroom ג€” still TBD; needs pick from the live WP project catalog.

## What Codex should read first (in order)

1. `reports/plan.md` ג€” full plan, scope, deliverables map. Read this before anything else.
2. `reports/00-strategy-brief.md` ג€” thesis, target users, sequencing of the build.
3. `reports/01-showroom-redesign.md` ג€” core UX spec; this is what gets implemented first in WordPress.
4. `reports/report-3a-real-semrush.md` ג€” keyword/volume/KD data justifying money-page priority order.
5. `reports/repo-inventory.md` + `reports/rest-api-map.md` ג€” code/REST map of the WordPress side; needed to wire showroom JS to existing endpoints.
6. `reports/advisor-notes.md` ג€” open anomalies for the WP eng team to clear in parallel (showroom 401, offers 404, hotspot wiring missing in JS, plugin-dist drift, Dimri Yama GLB is an 8KB stub).

## Sync going forward

On every meaningful Lovable session, the agent will:
- Append a dated entry to `reports/advisor-notes.md` (newest at top) ג€” what was decided, what changed, what's queued.
- Add new reports to `reports/` as they're drafted (02 through 07).
- Drop any new screenshots, exports, or data files into the matching folder and list them here.

Full chat transcripts are not exportable from Lovable; the decision log in `advisor-notes.md` is the substitute Codex should rely on.

---

## Addendum ג€” 2026-06-23 build run (Nadlan3D prototype)

This run shipped the **showroom prototype + listings + sitewide IA** on top of TanStack Start. Scope was locked at ~45-65 credits, owner-approved guardrails enforced (Hebrew-capable fonts, transparency labels, AI-plan watermark, asset truth, mobile 390 px).

### New reports (appended, prior reports untouched)

- `reports/02-showroom-prototype.md` ג€” `/showroom/$projectId` spec + asset-truth gradient (real GLB ג†’ facade SVG ג†’ empty state)
- `reports/03-listings-ia.md` ג€” magazine grid, filter/sort, ranking hierarchy, sitewide IA, war-room + country-landing future outline
- `reports/04-brand-nadlan3d.md` ג€” wordmark, taglines, domain risk notes, 3 alternative names
- `reports/05-fallback-floorplan-spec.md` ג€” AI-plan watermark rules + contractor-upload CTA

### New shared skills (cross-agent knowledge)

- `handoff/shared-knowledge/skills/nadlan-editorial-bright-tokens.md` ג€” cream-luxury tokens, Hebrew-first typography, hairlines, watermark utility
- `handoff/shared-knowledge/skills/nadlan-listings-ranking.md` ג€” ranking cascade (paid ג†’ completeness ג†’ engagement ג†’ freshness ג†’ locality) + transparency labels
- `handoff/shared-knowledge/skills/nadlan-magazine-card.md` ג€” single-source card pattern with dual-image tabs and asset-state dot

### Codebase changes (Lovable repo)

- `src/styles.css` ג€” rewritten as cream-luxury design tokens (cream / ink / gold / terracotta), HE+EN font stacks, `hairline` + `watermark-ai-overlay` utilities
- `src/lib/i18n.ts`, `src/lib/lang-context.tsx` ג€” HE-default i18n provider, EN toggle, dir switching
- `src/lib/projects.mock.ts` ג€” 6 mock projects, shape mirrors `nadlan/v1/projects`, `rankProjects()` reference implementation
- `src/components/nadlan/` ג€” `Nadlan3DMark`, `SiteHeader`, `SiteFooter`, `MagazineCard`, `ShowroomViewer`, `UnitSelector`
- `src/routes/` ג€” `__root.tsx` rewritten with `LangProvider` + `SiteHeader/Footer`; new routes: `index.tsx`, `listings.tsx`, `showroom.$projectId.tsx`, `cities.$city.tsx`, `guides.tsx`, `professionals.tsx`, `about.tsx`, `contact.tsx`
- `public/models/`, `public/plans/` ג€” README slots for real GLB / contractor plans
- `package.json` ג€” added `@fontsource/frank-ruhl-libre`, `@fontsource/heebo`, `@fontsource/fraunces`, `@fontsource/inter-tight`

### Out of scope this run (deferred, not removed from strategy)

- War Room dashboard coded screen (future run, ~25-40 credits, behind auth)
- Dubai / Cyprus / Greece / Thailand landing+listings (~20 credits per pair)
- Real backend (Lovable Cloud), real GLB upload pipeline, WhatsApp ingestion, payments
- Real AI floor-plan generation (only the **presentation** of AI plans is built; generation is mocked)
- Playwright screenshots ג€” folder is wired (`screenshots/`) but the capture step was skipped to stay inside the credit envelope; can be re-run on request

### Acceptance gates status

- [x] Hebrew fonts: Frank Ruhl Libre + Heebo for HE; Fraunces + Inter Tight scoped to LTR only
- [x] Featured / Sponsored / Promoted labels visible on every paid card
- [x] AI plan watermark + contractor-upload CTA present on every plan render
- [x] Asset-truth gradient renders all three states without fakes
- [x] Mobile-first: viewer/grid/drawer designed at 390 px, bottom-sheet for units
- [x] Per-route `head()` with canonical + hreflang on every shareable leaf
- [x] All 4 reports + 3 skills committed; source-manifest.md appended (not overwritten)

---

## Addendum ג€” 2026-06-23 Codex verification import

Codex pulled Lovable source commit `b275f7a`, installed dependencies locally with `npm install --no-package-lock`, and verified:

- `npm run build` passes locally.
- Local preview responded at `http://127.0.0.1:5187/`.
- Screenshots were generated after the Lovable commit and added to this handoff folder.
- A source snapshot was copied to `prototype-source/` so the WordPress port can inspect the relevant TanStack files without cloning the whole Lovable app.

### Screenshots added

- `screenshots/home-mobile-390.png`
- `screenshots/home-desktop-1440.png`
- `screenshots/listings-mobile-390.png`
- `screenshots/listings-desktop-1440.png`
- `screenshots/showroom-rainbow-mobile-390.png`
- `screenshots/showroom-rainbow-desktop-1440.png`
- `screenshots/showroom-dimri-mobile-390.png`
- `screenshots/showroom-dimri-desktop-1440.png`
- `screenshots/showroom-empty-mobile-390.png`
- `screenshots/showroom-empty-desktop-1440.png`
- `screenshots/home--en--default--mobile-390.png`
- `screenshots/home--en--default--desktop-1440.png`
- `screenshots/home--he--mobile-menu-open--mobile-390.png`
- `screenshots/home--en--mobile-menu-open--mobile-390.png`
- `screenshots/listings--en--default--mobile-390.png`
- `screenshots/listings--en--default--desktop-1440.png`
- `screenshots/showroom-rainbow--en--glb-state--mobile-390.png`
- `screenshots/showroom-rainbow--en--glb-state--desktop-1440.png`
- `screenshots/city-tel-aviv--he--default--mobile-390.png`
- `screenshots/city-tel-aviv--he--default--desktop-1440.png`
- `screenshots/city-tel-aviv--en--default--mobile-390.png`
- `screenshots/city-tel-aviv--en--default--desktop-1440.png`
- `screenshots/owner-lovable-preview-homepage-2026-06-23.png`
- `screenshots/owner-lovable-sync-dialog-2026-06-23.png`

### Prototype source snapshot added

- `prototype-source/package.json`
- `prototype-source/vite.config.ts`
- `prototype-source/src/styles.css`
- `prototype-source/src/components/nadlan/`
- `prototype-source/src/lib/i18n.ts`
- `prototype-source/src/lib/lang-context.tsx`
- `prototype-source/src/lib/projects.mock.ts`
- `prototype-source/src/routes/`
- `prototype-source/public/models/README.md`
- `prototype-source/public/plans/README.md`

### Remaining truth gaps

- `public/models/rainbow.glb` is still a slot, not a committed GLB payload in this Lovable repo.
- The Rainbow screenshot therefore proves the asset-state UI path, not a real rendered GLB.
- The screenshot gate is now satisfied by Codex-generated evidence, not by the original Lovable build commit.

### Codex visual QA added

- `reports/06-codex-visual-qa.md`
- `exports/2026-06-23-nadlan3d-visual-qa.html`
- `handoff/shared-knowledge/skills/nadlan-public-language-cleanup.md`
- `handoff/codex/lovable-prompts/2026-06-23-public-language-visual-cleanup-prompt.md`
- Owner Lovable sync dialog decision: wait for GitHub sync. Do not rebuild and do not spend another 45-65 credits for the same prototype.
- [x] Screenshots — added by Codex verification in this handoff folder
- [ ] Real `rainbow.glb` payload ג€” slot prepared at `public/models/`, file mirrors from WP repo in next sync

