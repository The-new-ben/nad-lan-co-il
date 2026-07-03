# Project-page FACTORY (2026-07-03) — modular, data-driven, real

One template (`_template.html`) + one generator (`generate.py`) → a real
standalone project page per project. Proves the pattern is modular (per-module
checkboxes: 3D / choose / price / map / buy / media / area / FAQ) and not a
hand-made one-off. Four real instances in `pages/`.

## What is REAL vs generated (honesty)
- **3D**: `gen-buildings.mjs` (the repo factory, floor counts corrected to
  35/38/39/54 and the anchored site shrunk ~3x so the tower is the hero) emits
  `models/*.glb`, embedded in each page as a self-contained data URI. Labeled
  "מודל אדריכלי גנרי · להמחשה" (generic architectural model). DUO also carries
  "מודל ברירת מחדל · טרם התקבלו חומרים מהיזם" (the default-building fallback).
- **3D hotspots + camera**: real per-unit coordinates from `projects.generated.json`.
- **Map**: real Mapbox GL at real coordinates + real comps.
- **Units**: real per-project unit data. DUO's are illustrative (labeled).
- **Prices**: sourced estimates ("אומדן", source shown) — NOT invented deals.
  Live gov.il transaction feed is a separate build task.
- **Languages**: full he/en/fr/ru/ar switcher, RTL-correct.

## _retired-bad-ashira-glb/
The old Ashira GLBs had a ~1km ground plane (building rendered as a dot). Moved
here out of the asset paths per owner instruction so nothing references them.
The corrected Ashira tower is `models/ashira.glb`.
