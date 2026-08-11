# Portable-report build diagnostics

This explanatory record is intentionally included in the developer handoff. The intermediate debug files it names remain local-only and are not copied into the ZIP.

The local deliverables workspace contains intermediate report files named `report-debug*`, `static-chart-debug.json` and `*verification-failure*.png`. They record a shared-builder browser edge encountered during packaging: the generated sticky header used `100vw`, which included a classic vertical scrollbar and created a 15-pixel horizontal document overflow in the headless-shell verifier.

The finalizer applies a narrowly scoped report-only correction (`width: 100%`, zero viewport-centering margins and horizontal clipping) without altering report content. The canonical build-report verifier uses its own desktop height and passed at 1440 × 1000 and 390 × 844, including the source dialog and keyboard interaction; its JSON records the widths 1440 and 390. The separate package-local Playwright inspection uses 1440 × 900 and 390 × 844 and found `scrollWidth === clientWidth`, zero overflowing elements, zero page errors and zero external requests in both viewports. These are two complementary checks, not two claims about one exact desktop viewport.

The intermediate debug HTML, static-chart dump and failure screenshots remain only in the local working folder and are deliberately excluded from the release ZIP. They are superseded by the verified final report, `report/report-verification.json`, `report/report-inspection.json`, and the final desktop/mobile screenshots. Open `report/report.html`.
