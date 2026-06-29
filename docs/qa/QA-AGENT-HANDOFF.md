# QA Agent Handoff — NadLan showroom (read this first)

> For the QA + admin agent (Claude-in-Chrome on the owner's PC). You have real Chrome
> and WordPress admin. The porting agent (me) has repo write access; you do not.
> **You do not need to push anything.** See the delivery protocol below.

## Repo + folder map (so you know where everything is)

- Repo: `https://github.com/The-new-ben/nad-lan-co-il` (branch `main`)
- Plugin: `plugins/nadlan-config/`
  - Bridge that mounts the new engine: `plugins/nadlan-config/inc/showroom-engine.php`
  - Engine assets: `plugins/nadlan-config/assets/showroom-engine/`
    `engine.js` · `showroom.css` · `tokens.css` · `i18n.js` · `mapbox-init.js` · `data.js` · `models/`
- QA evidence goes under: `docs/qa/screenshots/`
- Current on main: **1.69.56** (verify, don't trust this line:
  https://nad-lan.co.il/wp-json/nadlan/v1/healthcheck ). Engine ported, CMS-wired,
  project-agnostic, de-stacked, hreflang, real Mapbox when a token is set. Full map:
  `docs/COWORK-ACCESS-MAP.md`.

## Delivery protocol — DO NOT fight git (this removes your push blocker)

You cannot push (no GitHub MCP, git shell down, can't type credentials). **Do not try.**
Instead:
1. Capture screenshots and findings.
2. Paste a plain-text `report.md` (the full findings) back in chat to the owner.
3. The porting agent commits it to `docs/qa/screenshots/...` from its own environment.
This is how the last report landed in the repo. Reporting IS delivering. No web-UI upload needed.

## Known blockers and the REAL fixes

- **Runtime version lags the file (opcache).** If `/wp-json/nadlan/v1/healthcheck` shows an
  older `version` than the Plugins screen, the new code is not executing yet. **Fix: WP-Admin →
  Plugins → Deactivate "NadLan Config" → Activate it again.** That flushes PHP opcache for the
  plugin. Re-check the healthcheck reads the new version BEFORE testing — otherwise you test old code.
- **390 mobile not capturable** from your tools (no DevTools device mode, `resize_window` no-ops).
  Acceptable: do the desktop pass and state mobile was not capturable. Do not fake it. If the owner
  flips DevTools device mode (F12 → Ctrl+Shift+M → 390) you capture then.
- **WebGL blank capture** = background tab. Bring Chrome foreground before capturing the 3D.

## This round's mission (verify the engine swap on Ashira)

1. **Confirm runtime:** healthcheck `version` must read **1.69.56**. If it lags, deactivate/reactivate
   the plugin (above), then re-check. Screenshot it.
2. **Turn the engine on for Ashira:** edit project `ashira-sde-dov` (post 4744) → enable Custom Fields
   (Options → Preferences/Screen Options) → add field `nlp3d_use_engine` = `1` → Update. Screenshot the saved field.
3. **Verify the real Ashira page** `https://nad-lan.co.il/projects/ashira-sde-dov/` (no `?lang`),
   desktop, HE then EN. Screenshot each check:
   - default language Hebrew/RTL; building model loads; facade toggle; apartment select → panel with
     real data; inquiry form carries the selected unit.
   - **the fix to confirm:** the **map now renders (real Mapbox)** if a token is set in option
     `nadlan_mapbox_token`; and **English renders LTR** (not RTL).
   - console errors (record all), visible-text leaks (GLB/BIM/hotspot/mesh/Lovable/Codex/Featured/Sponsored),
     em-dashes.
4. **Regression:** open a project WITHOUT the flag (e.g. Rainbow) — confirm it still shows the old
   showroom unchanged (proves the swap is isolated, no breakage).
5. **Deliver:** paste the full `report.md` text in chat. The porting agent commits it. Do not soften failures.

## Interior look — open-source tech for the future build (no paid platform)

For when we build the immersive interior (the porting agent builds this, sources for reference):
- **Pannellum** (MIT, 21KB) single-room 360 — https://github.com/mpetroff/pannellum
- **Marzipano** (Apache-2.0, Google) multi-room 360 walk-through — https://www.marzipano.net/
- **Photo Sphere Viewer** (MIT) rich hotspots — https://github.com/mistic100/Photo-Sphere-Viewer
- **A-Frame** (MIT, WebXR) goggles + gyroscope "enter the world" — https://aframe.io
All embeddable, free; contractor supplies the 360 photos. No Matterport fee required.
