# AreaMap v1.1: language and direction (7.10.2026, HAD-460)

Local only. Nothing was deployed, committed or pushed. File changed: `scripts/project-stage/area_map/render_map.py`.
New data: `scripts/project-stage/area_map/rova-4.en.json`, `.fr.json`, `.ru.json`, `.ar.json`.

## What changed

1. **`ui(d)`, one place for the interface words.** Hebrew (`UI`, `CHIPS`, `PLURAL`, `dir="rtl"`, `lang="he"`) stays the default.
   A data file may carry a `"ui"` object:
   - `lang`, `dir`, `colon` (the separator after a name in the list, default `": "`; French uses `" : "`);
   - any `UI` key (`chips_label`, `wait`, `reset`, `close`, `list`, `fail`, `osm`);
   - `chips` (`{cat: label}` for the six filters, also the list headings);
   - `plural` (`{type: plural}` for the list lines);
   - `js` (every card string; `cats` and `loc` merge key by key; new optional `lrt` = the words that mark a light-rail stop's
     type, the Hebrew fallback `הקלה` lives in the script, so the Hebrew `data-cfg` is unchanged).
2. **`html()`** prints `dir` and `lang` from `ui`, and every interface word from it. The list headings for projects and urban
   renewal now come from the filter labels (in Hebrew they were already the same words).
3. **Empty layers (coordinator's rule, for Sde Dov):** a layer with no places gets **no filter button** (no visible "0") and
   **no list heading**. The four daily-life layers already skipped empty headings.
4. **CSS: a separate `[dir="ltr"]` block, appended after the phone block.** The Hebrew rules are untouched; removing the
   block gives back the v1 CSS exactly (checked in code). The block mirrors the overlay for left-to-right pages:
   - reset button to the top right;
   - the boundary key to the bottom left;
   - the card to the top left on desktop (full-width bottom sheet on phones, as before);
   - the card's close button to the top right;
   - the before → after arrow flipped.
   No braces inside CSS comments (there are no comments in the block).
5. **Script, four small changes, all keyed on the section's own `dir` / `lang`:**
   - **Base-map labels:** `name:he` → `name` for Hebrew (unchanged). For other languages:
     `name:<lang>` → `name:en` → `name`. Hebrew-only names still show through the RTL plugin.
   - **Zoom buttons:** bottom right on LTR pages, bottom left on RTL pages (unchanged).
   - **Card offset:** the map eases the chosen point away from the card. The offset is `+150` on LTR and `-150` on RTL
     (unchanged).
   - **Light-rail fact:** the line under a light-rail stop's card is found with `T.lrt`, falling back to `הקלה`.

## Hebrew unchanged: proof

`render_map.html()` on the current `rova-4.json`, before the change (copy of v1 kept in the session scratchpad) and after:

| render | md5 before | md5 after |
|---|---|---|
| `html(d)` | bebe79a3f7eb69b3387a2a3aca09faec | bebe79a3f7eb69b3387a2a3aca09faec |
| `html(d, '-d')` | ab9ab3a8eeeec3712ae5d2a7547718cf | ab9ab3a8eeeec3712ae5d2a7547718cf |
| `html(d, '-ph')` | 0e361a030aa263a5fe957bc98ac5cbf4 | 0e361a030aa263a5fe957bc98ac5cbf4 |

Byte-identical (32,593 / 32,601 / 32,605 bytes).

The shared assets do change, on purpose:
- **CSS:** 226b276e… → a9a840eb… (15,647 → 16,163 chars). The only change is the `[dir="ltr"]` block, which does not
  match a Hebrew section.
- **JS:** d380d0f9… → 5b24cf7e… The Hebrew paths are unchanged:
  - the same label expression (`name:he` → `name`);
  - zoom buttons bottom left;
  - card offset `-150`;
  - the light-rail match `הקלה`.

The Hebrew browser run below still reaches `ready` with 6 pins, draws 15 renewal pins and opens its cards with zero errors.

**Sde Dov** (`sde-dov.json`, not edited), counts per layer:

| projects | renewal | edu | parks | shop | transit |
|---|---|---|---|---|---|
| 9 | 0 | 9 | 8 | 2 | 6 |

v1 printed a "התחדשות עירונית 0" filter and an empty heading with an empty list (`<h3>התחדשות עירונית</h3><ul></ul>`).
v1.1 prints five filters and no empty heading. Those two pieces are the only differences in its markup.

## Browser check (headless Chrome, WebGL via SwiftShader, 12 s after the map came into view)

Pages: one per language with the PriceGuide and the AreaMap, built from the data files, in the page's `lang` / `dir`. Shots:
`docs/qa/had-460/i18n-components/<lang>-<1440|390>-{map,card-project,card-renewal,price,price-premium}.png` and
`<lang>-1440-list.png`. Report: `report.json` there. Scripts: `build_pages.py`, `shoot.py` in the same folder.

| | state | pins / renewal drawn | layout (code) | page overflow | errors |
|---|---|---|---|---|---|
| EN, FR, RU at 1440 | ready | 6 / 15 | reset right 15 px, key left 13 px, zoom buttons right 11 px, card left | 0 | 0 |
| EN, FR, RU at 390 | ready | 6 / 15 | reset right 11 px, key left 13 px, card full-width bottom sheet | 0 | 0 |
| AR, HE at 1440 | ready | 6 / 15 | reset left 15 px, key right 13 px, zoom buttons left 11 px, card right (as v1) | 0 | 0 |
| AR, HE at 390 | ready | 6 / 15 | as v1 | 0 | 0 |

Looked at:
- **Base-map labels** come out in the page's language where OSM has them:
  - Latin street names in EN and FR;
  - Cyrillic in RU (for example Арлозоров);
  - Arabic in AR, shaped right to left by the plugin.
  The rest fall back to the English name, then the local one.
- **LTR card:** the close button sits at the top right, the kicker and title start at the left edge, and the before → after
  arrow points right.
- **Pins and filters:** filter counts read 6 / 15 / 11 / 19 / 43 / 4 in every language. The filter row scrolls sideways
  on phones without widening the page.

## Seen, not changed (Hebrew stays identical)

- **Card title indent in RTL (Hebrew and Arabic).**
  - **What happens:** `.nlam__ct{margin:0 34px 8px 0}` is a physical right margin. In RTL the close button is on the left,
    so the title starts 34 px in from the right edge while the kicker and the fact line start at the edge. See
    `he-1440-card-project.png` against `en-1440-card-project.png`.
  - **Proposed fix (not applied, it changes the Hebrew look):** `margin:0 0 8px !important;margin-inline-end:34px !important`
    on `.nlam__ct`. With that rule, the LTR override is not needed for the title.
- **Release hookup is still Hebrew only.**
  - `map_437.py`'s shortcode `[nadlan_area_map key="rova-4"]` switches on the key alone.
  - Language pages need a language: either keys such as `rova-4.en` (from `render_map.load('rova-4.en')`) or a `lang`
    attribute.
  - The PriceGuide shortcode in `pg_helper.py` always renders `he`. Not edited here, by instruction.
- **Project links:**
  - The four projects with language twins link to them: `hamedina-<lang>`, `duo-tel-aviv-<lang>`, `yoo-tel-aviv-<lang>`,
    `park-bavli-<lang>` (each checked 200 with hreflang on 7.10.2026).
  - H Infinity and Akirov Towers have no twins, so their cards link to the Hebrew page.
  - The two renewal compound pages (Arlozorov, Dafna) also link to the Hebrew page.
