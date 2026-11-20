# 3D view: measured today and the budget the build must meet

Measured on 20.11.2026 with `docs/design-lab/rentals-xray/measure.py` (the lab harness, not product code). **Desktop Chrome emulating a phone viewport (390 x 844, DPR 2, touch), on an integrated AMD Radeon GPU: NOT a real phone.** A phone's CPU, GPU, radio and heat limits are not measured. Numbers are the median of three cold loads (empty cache) unless marked.

## Measured today (harness page `xray.html?mode=xray&markers=1`)

| | ambient pass ON | ambient pass OFF |
|---|---|---|
| requests | 31 | 19 |
| transferred | 585 KB | 566 KB |
| of which three.js + its addons (CDN, compressed) | 234 KB | 215 KB |
| of which our own files (local server, **uncompressed**) | 289 KB | 289 KB |
| of which web fonts (Google Fonts, page chrome) | 62 KB | 62 KB |
| first 3D frame | 1.69 s (1.69 to 1.81) | 1.43 s (1.41 to 1.45) |
| lighting environment loaded | 2.98 s | 2.44 s |
| render work per frame, 150 orbit frames, CPU only (issuing the draw calls) | median 6.5 ms, p95 11.3 ms | median 3.1 ms, p95 5.3 ms |
| render work per frame, same frames, GPU finished (1-pixel read-back) | median 19.3 ms, p95 34.1 ms | median 6.3 ms, p95 16.2 ms |
| draw calls / triangles | about 310 / about 100k | the same |

**What the ambient-occlusion pass (three's GTAOPass through the EffectComposer, full resolution 780 x 888) costs:** +13 ms per frame at the median and +18 ms at the 95th percentile on this GPU, +0.26 s to the first frame, +19 KB, +12 requests. It is the most expensive single thing in the picture.

## Budget the build must meet on a mid-range phone

1. At most **500 KB transferred** for the 3D view beyond the page itself (three.js, our code, the lighting environment; fonts belong to the page).
2. The first 3D frame within **2.0 s** of the request.
3. Render work at most **8 ms per frame at the 95th percentile**, measured with the GPU finished, not only the CPU submit time.

Today's harness does not meet 1 (our own code is 289 KB uncompressed; compressed and minified it should be a fraction of that, **not yet measured**) and does not meet 3 on this laptop GPU in either setting (16 ms p95 without the ambient pass, 34 ms with it). Item 3 therefore needs a decision before the build: AO at half resolution, a baked contact-shadow texture for the floor, or no AO on phones. It must be measured on a real mid-range phone before anyone claims it passes.

## Loading rule (what the build does)

- **The flat drawing loads first on every phone.** It is the page's first and default view.
- The 3D view replaces it **only if** its first frame arrived within **2.5 s of the request** AND the first second of frames stayed under **12 ms of work at the 95th percentile**.
- Otherwise the drawing stays, and 3D is **offered by a press** ("הצג בתלת-ממד").
- The choice is **remembered per device** (a stored flag: 3D on, or drawing); a person who pressed for 3D keeps 3D, a device that failed the test keeps the drawing without testing again until the flag is cleared.

## Ambient shading rule (why, and what the build does)

The ambient pass costs about **+13 ms a frame at the median and +18 ms at the 95th percentile** on the test GPU (an integrated AMD Radeon; the same frames measure **19 ms median and 34 ms at the 95th percentile with the pass on, 6 ms and 16 ms with it off**, GPU finished). While the camera moves that breaks the 8 ms budget. The build rule is therefore: **ambient shading is computed only when the camera is at rest (or baked once per plan), never while the camera moves**; during a drag or a fly-in the view renders without it, and the shaded frame is drawn when the camera stops. Measure both paths (moving without the pass, at rest with it) on a real mid-range phone before the 3D slice; the numbers above are a desktop GPU emulating a phone viewport, NOT a real phone.
