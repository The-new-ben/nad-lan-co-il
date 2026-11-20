# Gate frames for board 1b (round 4)

Files here: `frame1-overview.png` (390 x 444 CSS px at DPR 2), `frame2-part.png` (same), `clusters.json` (one entry per chip: room, chip centre x/y in stage px, size, count, state, parts, leader line yes/no, room centre), `plan-4r.png` (342 x 342 at DPR 2) and `plan-4r.json` (walls as segments, openings, runs, parts, clusters in the 342 px frame), `measure-ao.json` (the raw measurements), `3D-BUDGET.md` (budget and loading rule).

## Re-run

From the repo root `C:\Users\777\nad-lan\nad-lan-co-il` (Git Bash; needs Python with Playwright, desktop Chrome with a GPU, internet for three.js and the fonts):

```
python -m http.server 8765 --bind 127.0.0.1 &
MSYS_NO_PATHCONV=1 PYTHONIOENCODING=utf-8 python docs/design-lab/rentals-xray/gate.py      # the five gate files
MSYS_NO_PATHCONV=1 PYTHONIOENCODING=utf-8 python docs/design-lab/rentals-xray/measure.py   # measure-ao.json (ambient pass on and off)
```

Live pages: `http://127.0.0.1:8765/docs/design-lab/rentals-xray/xray.html?mode=xray&markers=1` (frame 1), `xray.html?mode=xray&layer=w` then `xray.closeup('boiler',{d:4,az:-138,el:38,fov:42,ndcY:0.12,aim:[22,-55,-30]})` in the console (frame 2), `plan4r.html` (flat drawing). URL switches: `ao=0` (no ambient pass), `az`, `el`, `margin`, `labels=1` (floor names, off by default), `wallc` (wall tint).

## Final measurements with the ambient pass ON

Desktop Chrome emulating a phone, NOT a real phone (integrated AMD Radeon, 390 x 844, DPR 2). Median of three cold loads: 31 requests, 585 KB (three.js and addons 234 KB compressed, our own files 289 KB uncompressed, fonts 62 KB), first 3D frame 1.69 s, lighting environment 2.98 s. Render work per frame over 150 orbit frames: CPU submit median 6.5 ms and p95 11.3 ms; with the GPU finished median 19.3 ms and p95 34.1 ms. Without the ambient pass the same frames are 16.2 ms p95 (GPU finished). The pass costs about +13 ms median and +18 ms p95 per frame. Details and the budget the build must meet: `3D-BUDGET.md`.

## What frame 1 is (round 5)

Home turned toward the boiler's room (azimuth -62, elevation 67, field of view 20): the home covers 93% of the stage width and 81% of its height; the fault room is in the lower half. Markers: a room with one part is a 44 px icon-only circle (room and part names are in its `aria-label` and in `clusters.json`); the kitchen (three parts) is a narrow 44 px pill "name · count"; the living room is a 44 px clock circle with a 2.5 px ink ring and a 19 px tag "מזגן סלון"; the fault is a 44 px #a11616 circle with a white "!" on the boiler's room and a 24 px tag "דוד שמש · תקלה" on the page background. No floor names. Markers are 8 px apart and inside the stage. Three markers (kitchen, safe room, bath) had to leave the home for the page background, each with a 1 px leader line and a dot at its room centre, to bring the share down.

**Marker share of the home (measured, written in `clusters.json` as `markerShareOfHome`): 0.14** (8,873 px² of marker, tag and dot rectangles over the home's projected floor outline of 63,280 px², sampled every 2 px, rectangles counted as full rectangles). First layout with every marker on its own room: 0.258, over the limit of one sixth; after moving the kitchen pill, the safe-room circle and the bath circle off the home it is 0.14.

What the markers cover and what stays visible: the walls, the boiler room with its tank and the red/blue runs, and all four run colours (purple along the walls, blue and red at the laundry and the south wall, yellow gas at the cooktop at the bottom edge) are visible and none is under a marker. Covered: part of the living room and hall floors (clock circle, its tag, the hall circle) and the master-bedroom floor (one circle). Not fully clear: the fault tag's leader line crosses the south-east corner of the home, and the gas run is only a few short dashes because the plan's gas run is 1.4 m long.
