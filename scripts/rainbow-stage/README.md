# Rainbow Tel Aviv: the 3D stage (24.9.2026)

A three.js stage for the Rainbow project page, built for the owner's order "Rainbow, כן, תחזירו אותו, ברמה מאוד גבוהה".
Not on the site yet: a private preview for the owner is at https://claude.ai/artifact/9tmAyq6iDBWkmy95Yxr6wd .

- `stage.js` (ES module, three 0.170 from jsDelivr through an import map), `stage.css`, `poster.jpg` (next to stage.js).
  `mountRainbowStage(el, options)` returns `{ ready, preset, setPreset, selectFloor, clearFloor, setAutoOrbit, stats, phase, dispose }`;
  a floor button fires `nl:floor` with `{ floor }`. `demo.html` is the full-screen demo; `checks/` re-runs the 32 checks
  (they expect `python -m http.server 47913` in this folder).
- The scene: a 40-floor elliptical tower with a slow balcony wave, six curved boutique blocks around the courtyard, two
  pools, the sea to the west and pale volumes for the quarter; sunset and noon presets; about 121k triangles.
- Honesty: the layout is illustrative and labelled "הדמיה להמחשה בלבד, על בסיס מקורות פומביים. אינה תוכנית מכר." The floor
  line is the project-wide fact from the marketing ("בפרויקט דירות 2 עד 5 חדרים"), never a per-floor split; the top three
  floors say "קומות הפנטהאוז, לפי פרסומי השיווק". The open button reads "סיור וירטואלי בפרויקט" (language DNA).
- Built by Opus 5.5: under the project rules Fable audits it before anything is built on it.
