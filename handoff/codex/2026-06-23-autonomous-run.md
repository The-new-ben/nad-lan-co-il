# Codex autonomous run (hand this to Codex to start a solo session)

> The owner is away. No human is watching mid-run. The system watches you instead.
> Your job is to move the showroom forward in small, verified, shippable slices.

## The one rule that makes solo work safe

You propose, the system verifies, the human supervises. The pre-push hook is your
supervisor while the owner sleeps. If your push is rejected, the system caught a
real problem. Fix the cause. Do not bypass it.

## Before any work (run this every session and every loop iteration)

1. `bash scripts/sync.sh`
2. `cat STATE.md`
3. `head -250 skills/MASTER-SKILL.md`
4. `git config core.hooksPath .githooks`  (installs the gate once)

If you cannot recite main HEAD, plugin version, and live version from the sync
output, you have not synced. Run it again.

## The loop (repeat until the backlog is empty or you hit a real blocker)

1. Take the top item from the backlog.
2. Write the goal in ONE sentence: "When this is done, X will exist on a PR." If
   you cannot write that sentence, re-read the item before touching code.
3. Branch off the LATEST main:
   `git fetch origin main && git checkout -b claude/<short-name> origin/main`.
   One item, one branch, one small PR. Never pile work onto one giant branch again.
4. Make the change. Smallest diff that achieves the goal.
5. If it touches the plugin: bump ALL SIX version surfaces together (patch bump),
   then `python3 scripts/build-plugin-zip.py <ver>` and
   `python3 scripts/verify-plugin-release.py <ver>`.
6. Prove it with screenshots: 1280 desktop and 390 mobile, Hebrew and English.
   Commit them under `docs/qa/screenshots/`. No screenshot, no claim.
7. `git push`. The hook runs. If it rejects you, read the failure, fix the real
   cause, push again. Use `GIT_HOOK_BYPASS=1` only when the push is docs-only and
   the failure is the known CMS-label false positive.
8. Open a PR ready-for-review with an honesty statement. Do NOT merge it. Two-key
   rule: you build, Claude or the owner merges.
9. Update `STATE.md`: the "What's happening" and "Next gate" sections. This is
   your trail for when the humans return.
10. Next item.

## Backlog (priority order)

1. **Self-hosted fonts.** Download the 8 woff2 files (Frank Ruhl Libre
   400/500/700/900, Heebo 300/400/500/700), commit them to
   `wp-content/themes/nadlan-revenue/assets/fonts/` at the exact paths the cream
   CSS expects, then remove the Google `@import` fallback. Confirm no font 404 in
   the network tab. The type is half of the premium look.
2. **Model-viewer lighting.** The 3D viewport still reads dark. Without new assets
   you can still raise `exposure`, set `shadow-intensity`, and add a neutral
   `environment-image` or tone-mapping on `<model-viewer>` so the model sits in
   the cream world, not a dark box. Screenshot before and after.
3. **Camera keystone re-check on the cream skin.** Click a unit, confirm both
   `camera-orbit` and `camera-target` are set and `jumpCameraToGoal()` fires.
   Screenshot the focused unit.
4. **Verifier hardening.** Extend `scripts/verify-plugin-release.py` to also check
   the two cache-busters (`wp_register_style` and `wp_register_script`) so it
   checks all six surfaces, not four.
5. **Hook scope.** Refine `.githooks/pre-push` to scan the diff against
   `origin/main`, not the whole tree, so pre-existing CMS labels stop causing
   false positives.
6. **Dimri Yama concept facade.** Apply the cream skin and the concept facade
   treatment. The Mapbox runtime failure is a separate known defect: if you touch
   it, set the RTL text plugin before map init and make failures visible, never
   silent.

Do not write new skill files or research reports during this run unless a backlog
item asks for it. Your output is shippable plugin slices, not documentation.

## Hard rules (the hook enforces most of these; honor them anyway)

- **No stacking.** Replace at the source. Delete the old, then put the new. Never
  add a cream override layer on top of a dark one.
- **No public-language leaks.** Buyer-visible text never contains internal names,
  field keys, GLB, SVG, Lovable, Codex, war-room, fallback, or any code token.
  CMS admin labels are the only place those words may appear.
- **No AI tells. No em dashes** in any copy or any file you write.
- **No fake anything.** No fake facade, no fake price, no doctored screenshot. If
  a thing is broken, show it broken and fix the code, not the picture.
- **Use Lovable's language and tokens**, not invented copy.

## Stop and wait (the only genuine owner-only blockers)

Write the blocker into `STATE.md` and the PR, then move to the next backlog item.
Do not fake a result around a missing input.

- Real BIM or official GLB from a developer.
- Real inventory, prices, or legal/tax approval.
- Paid-source access or API credentials.
- Contractor contact details.
- Anything irreversible (force-push main, delete data, post PII).

## When you finish or get stuck

Leave `STATE.md` current. Leave every PR ready-for-review with an honesty
statement. Stop. Do not merge. Do not deploy. The humans take it from there.

## Honesty statement (paste into each PR, filled in)

> I synced before I started. The hook is installed and ran on my push. I bumped
> all six version surfaces. The ZIP is guarded-built and verified clean. The
> screenshots are real captures at 1280 and 390 in HE and EN. I did not stack, I
> did not leak internal language, I did not fake any asset. I did not merge this
> PR. Open question or blocker: <one line, or "none">.
