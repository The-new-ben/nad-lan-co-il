# SKILL: building the selected-unit scene (the mobile UX rebuild)

Purpose: any session, any model, can continue this build from paper. Owner-approved
direction after the 2026-08-08 external audit. Status updates belong at the bottom.

## The decision

Selecting an apartment is a full STATE of the theater, not a panel:
building -> unit scene (model stays mounted in a compact strip + selected badge;
map+beam always visible; facts; four curiosity-labeled doors) -> body-level
<dialog> tools (plan/view/tour/studio) -> one-tap back at every level.
Zero nested scrolling anywhere. Desktop keeps its side panel until mobile is
approved, then gets the compact summary with the same dialogs.

## Where everything is

- The audit package (verdict, architecture, risks, test plan, competitor research):
  docs/audits/mobile-ux-audit-2026-08-08/
- READY CODE SKELETONS: docs/audits/mobile-ux-audit-2026-08-08/proposed-code/
  - engine-selected-unit.js  (renderUnitScreen, beam, clearUnitScreen)
  - fullscreen-tools.js      (openUnitTool/closeUnitTool, dialog shell, cleanup)
  - unit-surface.css         (namespace .nl-unit-*, no inset shorthand, 100dvh)
  - i18n-additions.js        (all five languages, no EN fallback)
  - integration-diff-guide.md (THE MAP: exact anchors + replacement selectUnit/closePanel)
  - wordpress-inline-style.php (how to attach the CSS to the engine handle)
- Engine: plugins/nadlan-config/assets/showroom-engine/engine.js (single IIFE;
  helpers project(), unit(), t(), DIR_BEARING, flyCamera, UNIT_MQ are PRIVATE -
  code must be pasted INSIDE the IIFE, not loaded as a separate file).
- The reverted older attempts (bottom sheet, flow v2 incl. the beam SVG):
  git commit f810815, and the board's "קוד שמור" block.

## The flag (sandbox gating)

PHP: SR.config.selected_unit_surface = ( get_post_meta( id, 'nl_unit_scene', true ) === 'on' )
JS:  if (SR.config.selected_unit_surface) renderUnitScreen(...) else legacy path.
Only the sandbox post carries the meta. Production behavior is byte-identical
until the owner flips the meta (or a site option) after phone approval.
Rollback = remove the meta. Never patch DOM from PHP, never MutationObserver.

## The sandbox

Post type nadlan_project, slug sandbox-unit-scene, clone of rainbow-tel-aviv
(content + all metas + GLB + units), noindex, meta nl_unit_scene=on.
Owner tests on HIS phone; emulator results are "plausible", never "approved".

## Release gates (from the audit, owner law)

- zero inner scrollers in any state (console snippet in proposed-code/acceptance-console-snippets.js)
- selection from hotspot AND from inventory cards lands the scene in-viewport
- model+beam+facts+doors visible in one screen; doors 2x2 on short phones
- tools close by tap, Escape, Android Back; camera and unit survive the round trip
- HE/AR RTL, EN/FR/RU LTR; no silent EN fallback for the new keys
- 20 open/close cycles: no listener/resource growth
- owner's physical phone approval BEFORE any wider rollout

## Also on the table (owner directives 2026-08-08)

- Badge on hotspot select (small details chip) before the scene "bounce".
- Environment layer in the scene: doors to area tour + Google Earth when the
  project has them (rainbow does).
- Lead-form bug (onSubmit .catch(done) fakes success): FIX APPROVED? ask owner -
  one line, separate tiny deploy.
- Drop-materials factory: docs/intake/<project>/ convention + PROJECT-STANDARD.md
  + board prompts 1-10; next project should build from a folder of materials.

## Status log (append here)

- 2026-08-08: skill created; sandbox build started this session.
- 2026-08-08 evening: INTEGRATED AND LIVE ON SANDBOX. engine.js spliced (fragments + flag-routed selectUnit/closePanel, legacy kept), i18n 5-lang keys in, unit-surface.css attached per-flag, config selected_unit_surface from nl_unit_scene post meta OR nadlan_selected_unit_surface option. Deployed v1.72.182. Sandbox post id 6201 /projects/sandbox-unit-scene/ (rainbow clone, 79 metas, noindex, flag on). ACCEPTANCE PASSED in emulation: zero nested scrollers, beam+4 doors+facts one screen, dialog body-child 375x812, close keeps unit, back-to-building clean; rainbow verified pure legacy. AWAITING OWNER PHONE VERDICT.
