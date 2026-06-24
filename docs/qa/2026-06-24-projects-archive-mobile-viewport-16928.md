# Projects Archive Mobile Viewport QA - 1.69.28

Date: 2026-06-24

## Goal

Make `/projects/` render as a real mobile page on 390px screens instead of a desktop-scaled archive.

## Change

- Added a viewport meta tag for the plugin-rendered directory archive shell.
- Removed em dash punctuation from the touched directory archive file.
- Bumped `nadlan-config` to `1.69.28`.
- Built the release ZIP only with `scripts/build-plugin-zip.py`.
- Deployed through WordPress admin after GitHub push.

## Release Gates

- `php -l` passed for:
  - `plugins/nadlan-config/nadlan-config.php`
  - `plugins/nadlan-config/inc/directory.php`
  - `plugins/nadlan-config/inc/health.php`
  - `plugins/nadlan-config/inc/project-3d.php`
- `python scripts/build-plugin-zip.py 1.69.28` passed.
- `python scripts/verify-plugin-release.py 1.69.28` passed.
- ZIP gate: 132 entries, 0 backslash paths, rooted under `nadlan-config/`, CRC ok.
- Live healthcheck after deployment reports `version: 1.69.28`.

## Visual Proof

Screenshots and machine report:

- `docs/qa/screenshots/projects-archive-mobile-viewport-16928-2026-06-24/projects-desktop-1440-top.png`
- `docs/qa/screenshots/projects-archive-mobile-viewport-16928-2026-06-24/projects-desktop-1440-full.png`
- `docs/qa/screenshots/projects-archive-mobile-viewport-16928-2026-06-24/projects-mobile-390-top.png`
- `docs/qa/screenshots/projects-archive-mobile-viewport-16928-2026-06-24/projects-mobile-390-full.png`
- `docs/qa/screenshots/projects-archive-mobile-viewport-16928-2026-06-24/report.json`

Measured result:

- Desktop: `innerWidth=1440`, `scrollWidth=1440`, viewport meta present.
- Mobile: `innerWidth=390`, `scrollWidth=390`, viewport meta present.
- Visible text scan on `/projects/`: no Lovable, Codex, Claude, prompt, token, GLB, SVG, Tailwind, shadcn, Featured, Sponsored, Promoted, SEO, KD, hreflang, canonical, CRM, money page, 390px, Frank Ruhl, or Heebo.
- Visible text em dash count on `/projects/`: 0.

## Honest Notes

- This release fixes the broken mobile scaling on the Projects archive.
- It does not finish the full Lovable listings redesign.
- The page still has an older dark hero and some global floating UI that should be handled in the next listings-design slice.
