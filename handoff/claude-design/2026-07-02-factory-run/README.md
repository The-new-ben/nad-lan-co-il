# Claude Design factory run - 2026-07-02 (owner upload)

Provenance: five packages uploaded by the owner on 2026-07-02
(NadLan_A, NadLan_Ashira_Factory_Run, NadLanFactory_Run, NadLan_homepage,
Homepage_Rich_Mockup.pdf). This folder is the deduplicated union of what was
NEW versus the repo at v1.69.85.

## Contents
- `*.dc.html` - DevCanvas exports: Showroom Engine, Rainbow Showroom,
  Ashira Target Mockup, Homepage Rich Mockup (+ print variants). These are
  self-contained interactive mockups; open in a browser.
- `Homepage Rich Mockup.pdf` - print of the homepage mockup (the visual
  reference for `../2026-07-02-homepage/homepage-spec.md`).
- `assets/engine/` - factory-run engine assets: `projects.js` (prototype
  manifest consumed by the engine when `window.NADLAN_SHOWROOM` is absent -
  see `docs/showroom-engine-wiring.md`) and OPTIMIZED re-exports of
  `rainbow.glb` (79KB vs 199KB canonical) and `dimri.glb` (53KB vs 180KB).
  NOT promoted to `assets/engine/` at repo root pending visual QA - if they
  look identical in the viewer, swap them in for the LCP win.
- `screenshots/` - factory-run renders: `0N-_m.png` (Hebrew mockup states),
  `0N-_en.png` (English states).

## Related material landed elsewhere in this drop
- `handoff/claude-design/2026-07-02-homepage/homepage-spec.md` + band PNGs
  (NOTE: the 7 band PNGs exported blank/white - the PDF and the .dc.html in
  this folder are the working visual reference).
- `handoff/claude-design/2026-07-02-critical-report-and-full-spec.md` -
  the site audit + implementation spec (R1 of its roadmap shipped v1.69.85).
- `handoff/claude-design/2026-06-28-wordpress-integration-spec.md`
- `docs/showroom-engine-wiring.md` - the CMS-to-engine data contract
  (window.NADLAN_SHOWROOM, field normalization table, lead payload).
- `handoff/claude-design/2026-06-27-showroom-engine/` gained the standalone
  engine HTML exports + `editorial.css`.
