# Artifact Index

This is the preserved input library for the NADLAN rebuild.

## Downloaded Bundles And Screenshots

Copied into `source-artifacts/downloads/`:

- `NadLan Ashira Factory Run complete bundle.zip` - complete handoff bundle with standalone Ashira
  showroom, engine files, model assets, and Claude design handoff material.
- `NadLan Ashira Factory Run handoff.zip` - handoff copy of the showroom engine package.
- `NadLan Ashira Factory Run assets.zip` - model and project assets, including GLB/poster files and
  Rainbow floor-plan assets.
- `NadLan Ashira Factory Run docs.zip` - QA screenshots and showroom wiring notes.
- `NadLan Ashira Factory Run mockup.zip` - Ashira facade and poster mock assets.
- `NadLan Ashira Factory Run.zip` and `NadLan Ashira Factory Run1.zip` - earlier exported prototype
  bundles.
- `Rainbow Showroom.dc.html`, `Showroom Engine.dc.html`, `Ashira Target Mockup.dc.html` - static
  prototype pages.
- `support.js` - support script supplied with the prototype material.
- `01-_en.png`, `02-_en.png`, `01-_m.png`, `02-_m.png`, `03-_m.png` - target mock screenshots.
- `rainbow_concept.png` - the facade-cell selector concept: apartments embedded in the building,
  not floating markers.
- `rainbow_diagnosis.png` - diagnosis diagram about cadence, dirty server state, and inverted page
  hierarchy.
- `screenshot.png` - additional prototype/reference screenshot.

Zip inventory already checked:

- `complete bundle.zip`: 41 entries, including standalone Ashira showroom, engine JS/CSS, i18n,
  editorial CSS, models, posters, and facades.
- `handoff.zip`: 41 entries, same family as the complete handoff.
- `assets.zip`: 13 entries, including `dimri.glb`, `rainbow.glb`, posters, and Rainbow plan SVGs.
- `docs.zip`: 3 entries, including QA screenshots and showroom wiring notes.
- `mockup.zip`: 2 entries, Ashira facade/poster mock assets.
- `Run.zip`: 18 entries, including Rainbow showroom HTML, plan SVGs, hero image, QA screenshots.
- `Run1.zip`: 19 entries, including showroom engine HTML, GLB assets, and plan SVGs.

## Prompt And Report Attachments

Copied into `source-artifacts/attachments/`.

These include the long mission prompts, Claude handoff notes, release discipline/mistakes material,
SEO/SERP analysis, Rainbow research, design direction, and product/showroom instructions. They are
not live code, but they are treated as historical evidence so the rebuild does not lose the lessons.

## Visual QA Comparison Pack

Copied into `source-artifacts/qa-compare/`.

Important files:

- `compare-home-desktop-live-vs-mock.png`
- `compare-home-mobile-live-vs-mock.png`
- `compare-ashira-desktop-live-vs-mock.png`
- `compare-ashira-mobile-live-vs-mock.png`
- `qa-notes.md`

Use these for before/after verification. The previous live page was not a pass against the design
mock. The new rebuild must produce replacement screenshots and compare them against these files.

## Platform Solution Package

Copied into `platform-solution-review/`.

Important files:

- `nadlan-platform-orchestrator-plugin.zip`
- `nadlan-platform-child-theme.zip`
- `nadlan-complete-platform-solution.zip`
- extracted child theme
- extracted orchestrator plugin
- extracted complete package
- `platform-solution-review.md`

Verdict: this is a promising candidate architecture because it keeps `nadlan-revenue` as parent,
keeps `nadlan-config` as the business source of truth, and avoids registering
`nadlan_showroom_engine` again. It is not ready for blind live activation. Public copy cleanup,
homepage-band gating, and screenshot QA are required first.

## What These Artifacts Mean

The design target is clear:

1. Clean cream editorial NADLAN brand, not a dark technical dashboard.
2. Project showroom has a rotating 3D context model plus a nearby apartment selector/facade.
3. Buyer copy talks about homes, location, price context, view, surroundings and inquiry.
4. Public surfaces must never expose internal terms such as GLB, BIM, mesh, funnel, lead, token,
   Codex, Lovable, or implementation details.
5. Multilingual pages are real crawlable pages, not a fake client-side language swap.
