# App-Grade 3D Configurator Research (Nike-spin, sun, gestures, Mapbox costs/RTL)
**Date:** 2026-06-12 · saved for the v1.61.x interaction rewrite. Key verdicts:
1. DEFAULT SURFACE = building spinner, map lazy + below fold. (Flatter, Render Vision, Toll Brothers LiveSite pattern: full-bleed dark stage, in-place unit cards, never centered modals.)
2. Spinner tech: keep our CSS-3D mass + polygons as default ($0 storage); optional 36-frame sprite (Cloudimage-360 pattern, initOnClick, ~25KB lib) ONLY for commissioned projects, hosted on Cloudflare R2 (10GB free, ZERO egress — never GitHub raw, never WP host).
3. Mapbox Hebrew fix: mapboxgl.setRTLTextPlugin('https://api.mapbox.com/mapbox-gl-js/plugins/mapbox-gl-rtl-text/v0.3.0/mapbox-gl-rtl-text.js', null, true) ONCE before any Map — NOT auto-injected by Standard style (docs.mapbox.com/mapbox-gl-js/example/mapbox-gl-rtl-text).
4. Mapbox cost: a "load" = Map constructor; interactions free for 12h session ($5/1k after 50k free). Playbook per Mapbox docs: IntersectionObserver lazy-init, "Show map" button on index pages, Static Images API for thumbnails, maxBounds+min/maxZoom, reuse one Map instance.
5. Sun: SunCalc.getPosition + 2 sliders (hour, day-of-year) + CSS-positioned glowing div over the spinner. ~3KB, no three.js. Reference UX: Andrew Marsh sunpath3d.
6. Gestures: native PointerEvents (NOT Hammer.js — tap-delay reason is dead): touch-action:none on stage, pointer cache + Math.hypot pinch (MDN pattern), 300ms/30px double-tap.
7. Scrollbars: page scrolls; AT MOST one panel scrolls per screen with overscroll-behavior:contain (only works on real scroll containers — Ben Nadel gotcha). Everything else fits via grid/flex.
8. Premium language: Tesla configurator pattern — full-viewport imagery, near-zero UI chrome, dark default.
Full citations in the agent report (sources include Mapbox docs, MDN, Cloudimage-360, WebRotate, Flatter, R2U/Toll Brothers, Cloudflare R2 pricing, getdesign.md/Tesla).
