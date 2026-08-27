# Spec — 1.68.1 facade-plane overflow fix (single mobile rule)

> **Status:** implementation contract for Codex. Target **1.68.1**.
> **Owner directive (2026-06-19, verbatim):** *"It's still overflowing. The facade is not."*

## 1. What the live page actually does

I gated the deployed 1.68.0 against `https://nad-lan.co.il/projects/dimri-yama-sde-dov/`:

- ✅ `<figure class="nlp3d-facade">` count: **0** — the original "old facade over new" bug is fixed by `$render_legacy_facade`.
- ✅ `<svg class="nlp3d-facade-hotspots">` count: **0** — legacy SVG also non-emitted.
- ✅ `<model-viewer>` count: **1**, `.nlp3d-model-error` present.
- ❌ **`.nlp3d-facade-plane` overflows the mobile viewport** in `is-dual-showroom` mode.

## 2. The actual cause (file `plugins/nadlan-config/inc/project-3d.php`)

There are at least 6 rules redefining `.nlp3d.nlp3d-premium.is-dual-showroom .nlp3d-facade-plane`, each marked `!important`, fighting source-order:

| line region | width | position | breakpoint |
|---|---|---|---|
| ~1235 | `min(56%,460px)` | `left:48%; translateX(-50%)` | base |
| ~1236 | `min(30%,340px)` | `right:3%; left:auto; transform:none` | base dual |
| ~1253 (mobile MQ) | `min(86%,320px)` | `left:50%; transform:translateX(-50%)` | ≤760px ✓ correct |
| ~1267 (`!important`) | `min(38%,420px)!important` | `right:3%!important; left:auto!important; transform:none!important` | **base — wins on mobile too** |
| ~1280 region | `right:5%`-ish, various | overrides | various |
| ~1294 region | `right:14px`-ish | overrides | various |

**Why it overflows:** because line ~1267 (and friends) carry `!important` and appear *after* the mobile media query in source order, CSS source-order resolves to them on mobile. So at 390px viewport the facade plane gets `width:min(38%,420px)` ≈ 148px-ish (or 420px if vw is large enough) at `right:3%` — and the entire pinned-right positioning is wrong for the mobile single-column stack the mobile MQ wanted.

Also: `.nlp3d.nlp3d-premium.is-mobile-edge-fixed` applies `transform:translateX(var(--nlp3d-mobile-nudge,0px))` on top, which can push it further sideways. That class is set by `fitMobileShowroom()` JS as a leftover from the 1.65-era constrained-width bug, which `alignfull` already solved.

## 3. The fix (surgical)

### 3.1 Consolidate the dual-showroom facade-plane CSS
Goal: **one rule per breakpoint** for `.nlp3d.nlp3d-premium.is-dual-showroom .nlp3d-facade-plane`. Delete the duplicate redefinitions (lines ~1267, ~1280, ~1294 — keep one canonical per media query).

### 3.2 Make the mobile rule actually win
Either:
- Mark the mobile rule with `!important`, OR
- Move it to AFTER the desktop overrides in source order so it wins naturally without `!important`.

Recommended canonical mobile rule (`@media(max-width:760px)`):
```css
.nlp3d.nlp3d-premium.is-dual-showroom .nlp3d-facade-plane{
  position:absolute!important;
  left:50%!important;
  right:auto!important;
  top:49%!important;
  width:min(calc(100vw - 28px), 360px)!important;
  height:45%!important;
  transform:translateX(-50%)!important;
  z-index:16!important;
}
```

### 3.3 Stop fighting the wrapper transform
Remove `is-mobile-edge-fixed` from `fitMobileShowroom()` when the wrapper has `alignfull` (which it always does now). The `--nlp3d-mobile-nudge` transform is a 1.65-era hack for the constrained-width bug that `nadlan_p3d_layout_constrained_fix_css()` already solved.

Or simpler: just set `--nlp3d-mobile-nudge: 0px` unconditionally on `.nlp3d.nlp3d-premium`. The variable still exists; the value is just neutralized.

### 3.4 Version surfaces
Bump 6 surfaces to **1.68.1**. Build ZIP with `scripts/build-plugin-zip.py`. Healthcheck flag: `facade_plane_mobile_overflow_v1681: true`.

## 4. Acceptance gate (Claude re-runs)

1. Live DOM on Dimri at `width=390` user-agent: **no horizontal scrollbar**, `.nlp3d-facade-plane` rect right-edge ≤ `390px`.
2. `count('nlp3d-facade')` still 0 (don't regress 1.68.0).
3. `<model-viewer>` count 1, `.nlp3d-model-error` present.
4. Screenshots @ 1440 / 768 / 390 in `docs/qa/screenshots/v1681-facade-overflow/` showing facade plane within viewport.
5. Healthcheck `facade_plane_mobile_overflow_v1681: true`.
6. `php -l` clean, JS clean, ZIP rootless 0-backslash CRC-ok.
7. 21 selector markers survive.

## 5. Honesty boundary

- This does NOT fix Mapbox (separate runtime defect).
- This does NOT fix penthouse/floor ordering (data fix).
- This does NOT replace the placeholder GLB (owner-input).
- This is **specifically** the "still overflowing" complaint from 2026-06-19.

## 6. Sequence

1.68.0 (deployed ✓) → **1.68.1 (this — mobile overflow)** → 1.68.2 functional facade polygons spec (already merged as design doc).

