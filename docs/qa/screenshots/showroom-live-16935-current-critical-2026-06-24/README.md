# Rainbow Showroom Live QA Before 1.69.36

Date: 2026-06-24

Live version captured: 1.69.35

Purpose: document the real failure that triggered the 1.69.36 package.

## What The Screenshots Prove

- Unit selection worked on live 1.69.35 for `unit-16-w`.
- The camera orbit and camera target changed after selection.
- The selected unit card opened.
- The page still showed two competing buyer interfaces: the new stage card and the old apartment console/list/detail column.
- Mobile 390 had no full-page horizontal scroll, but several elements bled 2 to 3 pixels past the viewport and some toolbar controls were still too narrow.

## What 1.69.36 Changes

- Removes the old console/list/detail/compare markup from the active showroom render path.
- Keeps the working stage card as the single buyer-facing selected-unit surface.
- Adds JavaScript null guards so unit selection still works after the old nodes are removed.
- Makes the active premium showroom a single vertical cream flow instead of a two-column stage plus console.
- Keeps toolbar controls at a 44px minimum tap target.

## Honesty Status

These screenshots are before/failure proof from the live site. They are not screenshots of 1.69.36, because 1.69.36 has been packaged but not installed on the live WordPress site at the time this note was written.

After the owner installs 1.69.36, run the same QA harness again and save fresh live screenshots in a new folder.
