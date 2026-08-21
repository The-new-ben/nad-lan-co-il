# DEPLOY RECEIPT — Tours V5 "Night-Street Render Pass" (2026-08-21)

Owner order (chat, 21.8): use github.com/StarKnightt/night-street to upgrade
the Somail + Sde Dov tours "100 levels up". Session: Fable 5
(claude-fable-5), "nad-lan.co.il — 2026-08-21 16:50".

## What shipped (all live, md5-verified end-to-end)

| surface | change | live md5 | backup |
|---|---|---|---|
| uploads/2026/07/sde-dov-tour.html | V4 → **V5** render pass | ed1f8aba2e9fc266e32b814576d6b929 | .bakV5 (V4 original) |
| uploads/2026/07/somail-tour.html | V1.1 → **V5** render pass | 519b7a13deeeeba95746e17c5a8db445 | .bakV5 (V1.1 original) |
| plugins/nadlan-config/inc/tour-routes.php | `?year=` 404/301 **root fix** + X-NL-Tour proof header | (v5c, LF) | .bakV5 (pre-fix original) |

Plugin version unchanged (1.72.218) — inc-file hot-swap per the proven
live-swap precedent; mirrored to this repo same-session.

## The V5 render pass (both tours; techniques studied from night-street, MIT — no code copied)

1. **AgX filmic tone mapping** (guarded fallback to ACES) + per-state exposure
   re-derivation (day 1.85 / dusk 2.35), day fog pushed out (1900/7400).
2. **Real PCFSoft sun shadows** — armed only after the existing GPU tier probe
   passes (or `?fx=hi`), day-gated, 2048 map in a ±780 box, stale-map dispose,
   self-revoking frame-time watch (skips hidden/throttled frames).
3. **Procedural sky**: 4-octave FBM cumulus + cirrus veil in the dome shader,
   sun-side lit, state-colored (white day / underlit peach-mauve dusk).
4. **Living sea** (sde-dov): animated ripple normals + grazing sheen,
   distance-attenuated (kills moire), day roughness 0.24 for sparkle.
5. **Facade relief** in the shared duskify shader: floor-slab shadow lines,
   mullion edges, per-building paint variance, lit-room ceiling gradient,
   TV-flicker cells, floor-height lit bias (low floors light first).
6. **Ground**: streak/blotch detail in the kurkar maker; all 0x35333b streets
   get an asphalt grain map; dusk light-pools under promenade / Ibn Gvirol lamps.
7. **Motion & life**: palm-canopy sway (sde-dov), 3 gulls over the water (day),
   gull-cry / city-sparrow + cricket audio layers on the existing sound gate.
8. **Grade**: state-lerped `saturate/contrast` CSS filter on the canvas.
9. New QA/demo deep-link: `?fx=hi|lo`; `enableRealShadows` exposed in `__dbg`.

## Evidence (evidence classes per the iron law)

- **eyes**: real-GPU canvas captures (scratchpad LIVE evidence set):
  sde-dov day aerial with per-tower ground shadows; somail day (100 casters);
  somail dusk (sunset burn + varied lit windows); sde-dov dusk street-level
  (room gradients, TV cells, slab lines); mobile 375 frame.
- **code**: boot 479ms local / 1614ms live (<2s law); draw calls 102–106
  (≤140 law); live console clean; towers ready `{dimri:glb, ashira:glb,
  rainbow:glb}`; shadows-on log line; sun-toggle pressed for real via the
  button handler → fog 7400↔3900, exposure 1.85↔2.35, grade lerp — both
  directions; md5(served body) == md5(deployed bytes) for every file.
- Fleet spot-check: rainbow + h-infinity pages 200/h1 ✓. Health 1.72.218 ok
  at open and close. `/tour/designer/` untouched and alive.

## Root fix detail (?year= deep links)

`year` is a WP-reserved public query var: `/tour/*?year=2035` turned the main
query into a date archive → hard 404; `?year=2026` → 301-canonical to
`/2026/`. Fix at the correct layer: a `request` filter keeps ONLY
`nadlan_tour` in the main query for tour URLs (template_redirect was too late
— redirect_canonical wins). Verified live: both broken shapes now 200 with
the full tour body.

## Traps learned (also in memory)

- A **stale allocated shadow map poisons the pass** silently — dispose before
  re-arming (`sun.shadow.map.dispose()`).
- A **background/throttled tab produces 250ms+ rAF frames** — any frame-time
  guard must skip `document.hidden`/long deltas or it false-revokes.
- **template_redirect is too late** to rescue reserved-query-var hijacks;
  fix at `request` filter.
- Live plugin files may be the **LF flavor** of CRLF repo blobs — base-md5
  no-clobber guards must compare against the live flavor (peek first).
- https pages cannot fetch http://127.0.0.1 (mixed content) — the local
  screenshot-POST pipe works from http:// pages only.

## Rollback

Each file keeps a `.bakV5` sibling holding the exact pre-V5 bytes
(no-clobber: written once, phase reruns never overwrote them).
