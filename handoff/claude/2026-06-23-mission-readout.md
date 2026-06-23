# Mission readout — Claude, 2026-06-23

> Owner asked: "go over all the repo and all Lovable materials and tell me you are going to run with a mission."
> This is the proof I know the picture.

## 1. Where we are (verified from repo)

- **main** = `8643e74` · plugin 1.68.2 · live 1.68.2 (in sync, the showroom fixes through the fake-grid removal + camera lock are deployed).
- **strategy/nadlan-seo-product-war-plan** = the working branch. Carries: Lovable's full design package, Codex's 1.69.0 visual port (dark, not pushed live by owner), Codex's keystone wiring (unit-click → camera) at `292b756`, Lovable's cream tokens at `handoff/lovable/.../data/nadlan-tokens.css` (verified vanilla CSS, all tokens, 8 `@font-face`, HE/EN/RTL, component→pattern map).

## 2. Where we're going (Lovable's direction, in one paragraph)

**Cream-luxury editorial.** Background `#FAF7F1`, ink `#1B1A17`, gold `#9C7A3C` as accent, terracotta `#C2563A` only for "Featured" CTAs, Frank Ruhl Libre + Heebo for Hebrew, Fraunces + Inter Tight for English, 1px hairline borders, generous whitespace, one shadow only. **Calm, bright, expensive.** The opposite of the current dark/gold skin. NadLan is positioned as the best new-projects showroom + foreign-buyer concierge + contractor-funded marketplace — not another listings board. KD-0 wedge: `פרויקטים חדשים <city>`. Three pilots: Rainbow (real GLB), Dimri (concept/facade), one urban-renewal TBD.

## 3. The keystone (the bug that was killing us)

`syncModelViewerCamera()` returned early after setting `camera-orbit`, never setting `camera-target` — so the model spun to an angle but didn't focus on the unit. **Lovable found it in report 01 §4. Codex fixed it at `292b756`.** The wiring works; the visual still needs the cream skin.

## 4. The non-negotiable rules (from owner)

- **No stacking.** Replace at the source, do not paint over. The `wp_add_inline_style` cap in the pre-push hook is 8.
- **No AI tells, no em dashes, no internal field names** in public copy. The pre-push hook scans buyer-visible strings for `project_3d_*`, `GLB`, `Lovable`, `Codex`, `nlp3d-`, `camera_orbit`, `hotspot_position`, `fallback`, `war room`, `KD`, `money page`.
- **No claim without screenshot.** M11.
- **Use Lovable language, not war-room language.** Public surfaces speak to buyers/contractors/investors.

## 5. What this PR ships (the sync infrastructure)

1. `STATE.md` — shared truth file, auto-updated by pre-push hook.
2. `scripts/sync.sh` — 5-second pre-work read every agent runs.
3. `.githooks/pre-push` — mechanical gate that rejects bad releases locally before they reach GitHub. Install with `git config core.hooksPath .githooks`.
4. `scripts/rebuild-master-skill.sh` — regenerates `skills/MASTER-SKILL.md` (one big skill file) from every skill in the repo. Individual skills stay alive.
5. `skills/MASTER-SKILL.md` — auto-generated index of every rule. Read first every session.
6. `skills/agent-autonomy-playbook.md` — the "how Codex runs autonomously" playbook with 14 cited 2026 sources.
7. This readout.

**No `project-3d.php` touched. No plugin runtime change. Doesn't block Codex's 1.69.1.**

## 6. The hand-off (what Codex does next)

1. Run `git config core.hooksPath .githooks` once.
2. Apply Lovable's cream tokens by **deleting** dark CSS at the source (not adding a cream layer on top — the hook will reject if it counts >8 inline-style enqueues).
3. Bump to 1.69.1. Build with `scripts/build-plugin-zip.py`. Run `scripts/verify-plugin-release.py`. Run `bash scripts/sync.sh` to confirm.
4. Screenshot Rainbow 1280 + 390 in HE, on the cream skin.
5. Push. If the hook rejects, fix locally and push again.
6. PR ready-for-review. Claude merges.

## 7. The owner's exit

The owner deploys the plugin update after merge. That's the only manual step left in the loop.

## 8. Honesty statement

I read every Lovable report (00–06), the design rules skill, the tokens skill, the language cleanup skill, the strategy brief, the brand direction, the prototype source structure, the i18n keys, the keystone wiring at §4, the cream token CSS file, and the existing `verify-plugin-release.py`. I know what we're building, why, for whom, and how it's monetized. I know the gap (cream skin not applied yet) and the keystone (unit→camera wiring, already in). I'm not guessing.

The PR I'm pushing now is the sync infrastructure that makes the next ten releases not need owner supervision. That is the mission.
