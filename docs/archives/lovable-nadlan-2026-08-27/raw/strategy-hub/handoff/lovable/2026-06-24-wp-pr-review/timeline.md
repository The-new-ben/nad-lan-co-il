# Timeline - 1.69.1 to 1.69.32

The arc starts after b25ff8a, the merged 1.69.1 cream showroom release. It ends at d5306af, the 1.69.32 row-aligned model tap fallback. The live proof for 1.69.32 was committed afterward at 3c08364.

| Version | Commit | Goal | Proof status |
|---|---|---|---|
| 1.69.2 | 9fc4768 | Make Rainbow apartment units selectable from the showroom instead of leaving the model as a passive object. | INVALID / DUPLICATE PNG RISK - the disputed 1.69.2 proof window contains byte-identical before and after screenshots in the manual model-selection folders. Treat this release as unproven visually. |
| 1.69.3 | 7e75ebd | Polish the selected apartment flow so buyers can see a clearer unit selection after tapping. | WEAK / SUPERSEDED - QA proof exists nearby in history, but later fixes prove this was not complete. Falls inside the disputed 1.69.2 to 1.69.29 proof-thrash window. |
| 1.69.4 | 459d88b | Clean model pin selection so buyer taps resolve more predictably to the intended unit. | WEAK / SUPERSEDED - screenshots were added after this release, but later releases continued fixing the same selection problem. |
| 1.69.5 | c160861 | Improve how taps on the 3D model choose a showroom apartment. | WEAK / SUPERSEDED - QA exists in history but is not accepted as final proof because later releases fixed the same behavior again. |
| 1.69.6 | a15d1a7 | Improve mobile picking so a 390px buyer can tap the model and get the right apartment. | WEAK / SUPERSEDED - mobile QA exists, but not final proof. |
| 1.69.7 | 0d9eb81 | Let upper-floor model taps select units instead of being blocked by overlay or stage behavior. | WEAK / SUPERSEDED - not reliable enough to stop the patch cycle. |
| 1.69.8 | d933b7d | Make the selected unit state clearer for buyers after interaction. | WEAK / SUPERSEDED - proof exists for some state, but later releases show core interaction remained unstable. |
| 1.69.9 | 26fb2d9 | Improve mobile marker clarity so apartment markers are easier to understand. | WEAK / INSPECT - falls inside the repeated screenshot proof window. Review raw QA before accepting. |
| 1.69.10 | 2717ff6 | Spread mobile markers to reduce overlap and make apartment selection easier. | WEAK / INSPECT - later releases still adjusted selection and fallback behavior. |
| 1.69.11 | 286a85c | Make the selected-unit dock visually separated from the showroom stage. | WEAK / DESIGN ONLY - no final interaction proof. |
| 1.69.12 | c191ea8 | Fix the rendering of the selection dock separator. | WEAK / DESIGN ONLY - not a selection proof release. |
| 1.69.13 | 625830a | Clean selected-card text so the buyer sees more professional public language. | WEAK / SUPERSEDED - QA exists nearby, but not final proof of the model interaction. |
| 1.69.14 | d03c733 | Polish the selected apartment card for a more credible contractor-facing showroom. | WEAK / SUPERSEDED - useful visual proof may exist, but later fixes show product behavior remained incomplete. |
| 1.69.15 | 8fb48e2 | Keep the action rail contained so it does not break the showroom layout. | WEAK / LAYOUT ONLY - not final interaction proof. |
| 1.69.16 | d0444ee | Try mesh surface picking so direct taps on the model can choose a unit. | WEAK / SUPERSEDED - later fallback and row-alignment fixes show mesh picking alone was insufficient. |
| 1.69.17 | 88978a1 | Return the showroom to a useful overview after selection or load. | WEAK / SUPERSEDED - camera behavior kept changing afterward. |
| 1.69.18 | 9ce9a83 | Frame the selected apartment better when a unit is selected. | WEAK / SUPERSEDED - camera work continued through 1.69.20 and beyond. |
| 1.69.19 | e0c0fb1 | Tune target units used by the showroom selection QA and behavior. | WEAK / TARGETED - does not prove every apartment or exact mesh picking. |
| 1.69.20 | 6a6fd99 | Make the camera settle more reliably after unit selection. | WEAK / SUPERSEDED - later visibility and repaint fixes were still needed. |
| 1.69.21 | adef3e4 | Keep the selected showroom model visible after apartment interaction. | WEAK / SUPERSEDED - later repaint fixes followed immediately. |
| 1.69.22 | 2d616ec | Force selected model repaint so the buyer sees the updated selection state. | WEAK / SUPERSEDED - faster repaint and reliable tap fixes followed. |
| 1.69.23 | 662a214 | Speed up the selected model repaint after a buyer taps a unit. | WEAK / SUPERSEDED - reliable tap work followed. |
| 1.69.24 | f396a55 | Make apartment taps reliable enough for live showroom QA. | PARTIAL / DISPUTED - live QA folders exist, but duplicate PNG collisions appear in the broader 1.69.2 to 1.69.29 proof set. Treat as not final. |
| 1.69.25 | 72197cf | Allow direct apartment selection from Rainbow model-surface taps. | PARTIAL / SUPERSEDED - later mesh preference and bias fixes changed the same logic. |
| 1.69.26 | e51405a | Prefer mesh pick results when resolving model-surface taps. | PARTIAL / SUPERSEDED - horizontal bias followed. |
| 1.69.27 | 611b949 | Bias model-surface selection by horizontal distance to reduce wrong apartment matches. | PARTIAL / SUPERSEDED - later live checks still required 1.69.30 to 1.69.32 fallback changes. |
| 1.69.28 | c0f0c89 | Fix the projects archive mobile viewport so listings do not overflow on 390px screens. | PARTIAL / VIEWPORT - QA commit exists, but not related to model selection proof. |
| 1.69.29 | e42c3a9 | Apply cream visual skin to the projects archive so it matches the Lovable direction. | PARTIAL / DESIGN - QA proof exists, but duplicated screenshot risk is flagged for the older proof window. |
| 1.69.30 | 9096825 | Improve showroom model tap fallback for mobile where direct surface selection misses. | PARTIAL / SUPERSEDED - QA existed, but later 1.69.31 and 1.69.32 fixed the same fallback area. |
| 1.69.31 | c15bdde | Improve model tap fallback when the intended apartment is row-aligned with the tap. | FAILED / SUPERSEDED - the owner-critical test found unit-16-w raw tap could select unit-24-nw. Fixed by 1.69.32. |
| 1.69.32 | d5306af | Prefer row-aligned model taps so the intended Rainbow apartment is selected on desktop and mobile. | VERIFIED LIVE - desktop and 390 mobile marker taps plus raw model-viewer tap selected unit-16-w. See qa/showroom-live-selection-16932-2026-06-24/. |

## Product reading

The release history shows heavy patching around a single product question: can a buyer tap the visible building model and reliably select the intended apartment? The answer is now better for authored hotspots and row-aligned raw taps, but it is still not true BIM-backed per-window picking.

Lovable should decide whether the next spec should stay with authored hotspot fallback, require contractor-provided apartment geometry, or define a hybrid contract where the public UI clearly reflects the asset truth.

