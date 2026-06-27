# QA — Live Showroom — nadlan-config 1.69.43

**Date:** 2026-06-27
**Tester:** QA agent (real Chrome, Claude-in-Chrome)
**Target:** `https://nad-lan.co.il/projects/ashira-sde-dov/`
**Renderer reported by healthcheck:** `premium_showroom_v10_buyer_product`

> IMPORTANT SCOPE NOTE (added by porting agent): this QA tested the **existing live
> project page**, which renders the OLD `premium_showroom_v10_buyer_product` showroom,
> NOT the new `[nadlan_showroom_engine]` shortcode engine. The two defects below are
> in the OLD showroom. The new engine (slices 1/1b) replaces it in slice 3.

## Version
- Live healthcheck `version`: **1.69.43** ✅
- PHP 8.5.5, WP 7.0, `project_3d.enabled: true`, `projects_with_3d: 9`, `projects_with_glb: 2`,
  `model_full_360: false`, `camera_lock_default: horizontal`.

## Default language
- `/projects/ashira-sde-dov/` with no `?lang` → `document.documentElement.lang="he-IL"`, `dir="rtl"`.
- **Default = Hebrew (RTL).** ✅

## Functional checks (desktop, real Chrome)
| # | Check | Result |
|---|---|---|
| a | 3D model loads, not blank | ✅ PASS — GLB `model-context.glb` loads, `loaded:true`, drag-rotatable; horizontal-locked; does NOT auto-spin despite the attribute |
| b | Facade toggle switches | ✅ PASS — "מבט ראשי" ↔ "חזית" tower picker (−/+/360/עיר/ים) |
| c | Apartment select → panel with data | ✅ PASS — unit 18W → "הדירה שנבחרה" panel: 5 rooms, 132 m², floor 18, sea+Reading view |
| d | Map block renders | ❌ FAIL — `nlp3d-view-map` collapsed (height 0); `window.mapboxgl` NOT loaded; zero map canvases; "view" tab shows a placeholder |
| e | Inquiry form carries selected unit | ✅ PASS — hidden `selected_unit=ashira-18-west`; button "שלחו פנייה עם הדירה שנבחרה" |
| f | Language switch text + direction | ⚠️ PARTIAL FAIL — EN slug translates text but stays `lang="he-IL" dir="rtl"` → English renders RTL, punctuation at wrong end; no in-page language pills; no hreflang alternates |

## Console / scroll / leaks
- Console errors: **none** (only model-viewer debug logs).
- Desktop horizontal scroll: none (scrollWidth 1625 ≤ innerWidth).
- Leaked internal terms (GLB/BIM/hotspot/mesh/Lovable/Codex/Featured/Sponsored): **none** in visible text.
- Em-dashes: **0**.

## Not completed this round (environment, not the engine)
- Mobile 390 pass: the QA environment could not set the viewport to 390 (resize/zoom no-op).
- Git push from the QA machine: the local git sandbox failed to boot (`HYPERVISOR_VIRT_DISABLED`).
  Report carried into the repo by the porting agent instead.

## Verdict
The OLD live showroom works for 3D + facade + selection + inquiry, Hebrew default is correct,
console is clean, no leaks. Two real defects in the OLD showroom: (d) the map does not render,
and (f) English is served RTL with no hreflang. Both are addressed by replacing the old showroom
with the new engine (slice 3) and wiring real Mapbox (slice 2).
