# Proof Integrity Notes

This packet is intentionally strict about proof. A screenshot is accepted only when it shows the state it claims to prove and is tied to the relevant version.

## Verified live proof

1.69.32 has accepted live proof in qa/showroom-live-selection-16932-2026-06-24/:

- Live healthcheck showed version 1.69.32.
- Desktop marker taps selected the intended units.
- Mobile 390 marker taps selected the intended units.
- Desktop raw model-viewer tap near unit-16-w selected unit-16-w.
- Mobile raw model-viewer tap near unit-16-w selected unit-16-w.
- Public leak scan returned no hits.
- Mobile scroll width stayed 390.

## Duplicate PNG collisions found in older proof folders

The older 1.69.2 to 1.69.29 proof window is not accepted as final proof. A local SHA256 scan found duplicated screenshot files, including this high-risk group around the 1.69.2 manual model-selection proof:

~~~text
manual-model-selection-2026-06-23/01-live-stage-before-click.png
manual-model-selection-2026-06-23/04-desktop-before-manual-click.png
manual-model-selection-2026-06-23/05-desktop-after-manual-click.png
manual-model-selection-2026-06-23/06-live-stage-aligned-visible.png
manual-model-selection-2026-06-23-live-1692/01-live-1692-before-click.png
manual-model-selection-2026-06-23-live-1692/02-live-1692-after-click.png
~~~

Those before and after files being byte-identical means they cannot prove the interaction changed the page.

Other duplicate groups appeared in repeated mobile/grid QA folders. Some duplicates may represent stable repeated states, but they are still weak proof unless the report explains why identical screenshots are expected. For Lovable review, treat releases 1.69.2 to 1.69.29 as disputed or superseded proof, not as final buyer-experience validation.

## Honest correction

This packet does not claim every screenshot from 1.69.2 to 1.69.29 was individually proven fake. It says the proof set is contaminated by verified duplicate PNG groups, and the final accepted proof is the live 1.69.32 QA folder.

