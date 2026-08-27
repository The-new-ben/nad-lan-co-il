# 3D Apartment Configurator + Mapbox Cost/RTL — Cited Research
**Date:** 2026-06-12 · **Researcher:** Claude (deep-research agent, 29 tool uses)
**Target:** v1.61.0 product slice — turn the Rainbow page from "site widget" into "shopping app".

## TL;DR — give to Codex as the build contract
1. **Default surface = building spinner**, not the map. Map drops below the fold and is lazy-instantiated.
2. **Kill nested scrollbars**: one page scroll; if a panel must scroll, only it does, with `overflow:auto; overscroll-behavior: contain;`.
3. **Mapbox RTL fix (before any Map ctor)**: `mapboxgl.setRTLTextPlugin('https://api.mapbox.com/mapbox-gl-js/plugins/mapbox-gl-rtl-text/v0.3.0/mapbox-gl-rtl-text.js', null, true)`. v0.3.0 is current (Mapbox docs); the plugin is NOT auto-injected on third-party sites.
4. **Mapbox cost playbook** (citing docs.mapbox.com/help/troubleshooting/manage-web-map-costs):
   - IntersectionObserver-gate every `new mapboxgl.Map()`.
   - Listing/index pages: render Mapbox **Static Images API** thumbnail + "Show map" button; only the click constructs the GL map.
   - `maxBounds`, `minZoom`, `maxZoom` to cap tile fetches.
   - Reuse a single Map instance across SPA routes inside the **12-hour session window** (one paid map load covers 12h of interaction).
   - Cost: $5 per 1,000 loads after free tier.
5. **Animated sun** = SunCalc (BSD, tiny) + 2 sliders (hour, day-of-year) + a `<div class="sun">` with `box-shadow` glow positioned via `getPosition(date, lat, lng)`. Pure CSS keyframes for sky gradient. No three.js.
6. **Apartment detail = in-place card** anchored beside the clicked unit (drawer on desktop, bottom-sheet on mobile). NEVER a centered modal.
7. **`project_architectural_drawing` field** on `nadlan_project` — one URL → lightbox with `overscroll-behavior: contain`, dismiss on Esc / backdrop / swipe.
8. **Pinch + double-tap zoom** via Pointer Events directly (canonical MDN pinch recipe: cache pointerdown, `Math.hypot` on pointermove with cache.length===2). `touch-action: none` on the spinner. No Hammer.js.
9. **Storage rule** (owner's WP-disk constraint): default = CSS-3D mass + polygon meta (zero new assets); developer-supplied facade = one URL field; sprite sequences ONLY if commissioned → Cloudflare R2 (10GB free, $0.015/GB after, zero egress). Never on the WP host. Never on GitHub raw.

## Spinner pattern decision
Two viable patterns from production:
- **Image sequence** (Nike/Apple/WebRotate/Cloudimage): 24–100 pre-rendered JPGs swapped on drag. Cloudimage360 (MIT, ~25KB, 2.1k stars) ships sequential loading + pinch-zoom + `initOnClick` first-frame preview. Warning from their docs: each frame ≈4MB GPU RAM — cap mobile frame count.
- **three.js OrbitControls**: real model, free, but heavy to ship+author. Single-touch = orbit, pinch = zoom, three-finger = pan.

**Pick for nad-lan:** keep our CSS-3D extruded mass + polygon overlay as default (we already control it, costs nothing). Upgrade individual projects to a 36-frame R2 sprite IF the developer commissions it. **Never ship three.js on public listing pages.**

## Production case-study patterns (apartment-on-tower selectors)
- **Render Vision Apartment Viewer**, **Flatter.hu** (Hungarian — "3D model not image sequence", in-place "compact apartment card" not modal), **Lennar interactive site plan**, **Toll Brothers LiveSite** (touchscreen 3D sales center), **Shapespark**. Convergence: full-bleed dark stage with the building centered, gestures everywhere, no nested scrollbars, unit details as in-place cards.
- Click targets = SVG polygons over a flat render with popovers (MarkerKit, IRE WP plugin patterns — same as our `points` data layer).

## Gesture details
- `touch-action: none` on the spinner so the browser doesn't steal pan/zoom.
- Pinch via Pointer Events: cache `pointerdown` events, on `pointermove` with `cache.length===2` compute `Math.hypot(dx,dy)` vs `prevDiff`.
- Double-tap zoom: track `lastTapTime` on `pointerup`, fire zoom if next `pointerup` within 300ms and within ~30px.
- Tesla configurator design language: full-viewport photography, near-zero UI, dark mode default. Steal: dark stage, no chrome, hover-in controls.

## Sources (full list)
- 360 spinners: jqueryscript.net best-360-product-view · webrotate360.com multi-row · github.com/scaleflex/cloudimage-360-view · spritespin.ginie.eu
- three.js orbit: discourse.threejs.org/t/orbitcontrols-handle-double-touch-gesture-on-mobile-device · forum.zimjs.com OrbitControls pinch zoom
- Apartment selectors: render-vision.com/apartment-selector · flatter.hu/en · shapespark.com/industries-real-estate · discover.lennar.com Lake Ridge · tollbrothers.com/sitemap · r2u.io/en/blog/toll-brothers-livesite · markerkit.com interactive-multi-floor-house-plan · ireplugin.com
- Sun: github.com/mourner/suncalc · andrewmarsh.com sunpath3d · github.com/antarktikali/threejs-sunlight · codeconvey.com css-sunset-animation · dev.to dianale animated-sky
- Mapbox: docs.mapbox.com/mapbox-gl-js/example/mapbox-gl-rtl-text · maplibre.org setRTLTextPlugin · github.com/mapbox/mapbox-gl-rtl-text · npmjs.com/@mapbox/mapbox-gl-rtl-text · docs.maptiler.com RTL guide · docs.mapbox.com/mapbox-gl-js/guides/pricing · docs.mapbox.com/help/troubleshooting/manage-web-map-costs · docs.mapbox.com/api/maps/static-images · mapbox.com/static-maps · g2.com Mapbox pricing 2026 · docs.hypaapps.com Mapbox costs
- Storage: developers.cloudflare.com/r2/pricing · leanopstech.com R2 pricing 2026 · emgoto.com hosting-images-cloudflare-r2
- UX/gestures: MDN overscroll-behavior · developer.chrome.com/blog/overscroll-behavior · bennadel.com overscroll-behavior-only-affects-scroll-containers · MDN Pinch zoom gestures · MDN touch-action · css-tricks.com touch-action · hammerjs.github.io · getdesign.md tesla

