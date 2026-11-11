# Kikar showroom: language inventory (he → en, later ar)

11.11.2026. Read-only inventory; nothing in the plugin was changed. The full list is `showroom-i18n-inventory.json` beside this file
(357 entries, one per Hebrew string occurrence, 285 distinct keys). Paths below are under `plugins/nadlan-config/` unless they start
with `assets/`. Line numbers are the files as of this date.

Check made on the list: every `he` value was matched against its source line (0 misses), and every Hebrew letter on every non-comment
line of the four JS files falls inside an entry (0 uncovered lines). Two entries carry a placeholder for a nested conditional whose
Hebrew is listed separately (`${near}` at cockpit.js:131, `${feeClause}` at cockpit.js:166).

## Counts

| File | Entries | data-label | button | heading | aria-label | alt | toast | number-format | whatsapp-text | other |
|---|---|---|---|---|---|---|---|---|---|---|
| assets/project-stage/world/showroom.js | 65 | 24 | 11 | 4 | 6 | 4 | 0 | 0 | 1 | 15 |
| assets/project-stage/world/cockpit.js | 161 | 40 | 32 | 24 | 7 | 3 | 2 | 8 | 0 | 45 |
| assets/project-stage/world/journey.js | 45 | 15 | 3 | 4 | 5 | 4 | 0 | 2 | 0 | 12 |
| assets/basket/basket.js | 86 | 5 | 19 | 5 | 7 | 0 | 0 | 2 | 11 | 37 |
| **Total** | **357** | 84 | 65 | 37 | 25 | 11 | 2 | 12 | 12 | 109 |

"other" = captions, hints, notes, form labels, map lines, share text (the note on each entry says which). No `title` attributes exist
in these files.

The counts are higher than the first estimate (60/134/37/86) because shared tables are counted per copy: the 8 direction words and
the 7 sector names are repeated in showroom.js:21-24, cockpit.js:27-29 and journey.js:22-25 (45 entries, 15 keys), and nested
conditionals are split out.

WhatsApp text (role `whatsapp-text`, all marked AWAITING BEN): showroom.js:116 (one template) and basket.js:236 (3 parts) and
basket.js:321-331 (8 parts). The cockpit sends no WhatsApp text of its own: its icon uses the page link `C.wa` (cockpit.js:249), which
PHP already builds per language from `nadlan_ps_world_words()['wa_tx']` (project-stage.php:1155). Note that showroom.js:115-116
overwrites that link's `text=` with its own Hebrew.

## How the showroom is gated to Hebrew

journey.js does not check the language. It only chooses showroom vs the earlier path by a URL switch:

- journey.js:15 `const SHOWROOM = new URLSearchParams(location.search).get('kikar') !== 'journey';`
- journey.js:172-177 `export function mountJourney(stage) { if (SHOWROOM) { ... import(new URL('showroom.js' ...)).then((m) => m.mountShowroom(stage)) ... return { open }; }`

The Hebrew-only gate is in PHP, so on the English page none of these scripts is loaded at all:

- inc/project-stage.php:1121-1122 `function nadlan_ps_kikar_next( $ps ) { return 'hamedina' === (string) ( $ps['dir'] ?? '' ) && 'he' === (string) ( $ps['lang'] ?? 'he' ); }`
- inc/project-stage.php:1177-1198 only when that is true does the page config get `next.cockpit` and `next.journey` (js, css, data, base, ver, avail, wa). Neither carries a `lang`, although the same config has `'lang' => $tl` for the 3D world (1165) and `$la` already builds `dir`/`lang` per language (1152: he and ar → rtl).
- inc/project-stage.php:1284-1287 (inline JS) imports cockpit.js and journey.js only `if (c.next && c.next.journey)`.
- inc/basket.php:23 `return $ps && 'he' === ( $ps['lang'] ?? 'he' ); // Hebrew-only for now (HAD-361)`: on the English page the basket config is not printed, so `window.__nlBasket` does not exist and the showroom's basket step (showroom.js:135, 189) silently does nothing.

## Every place that assumes RTL or Hebrew

**Direction and language set in code**
- showroom.js:232 `el.dir = 'rtl'; el.lang = 'he';`
- cockpit.js:255 `el.dir = 'rtl'; el.lang = 'he';`
- journey.js:161 `el.dir = 'rtl'; el.lang = 'he';`
- basket.js:91 `dir: 'rtl', lang: 'he'` on the drawer
- CSS forces it again: showroom.css:6 `direction:rtl;text-align:right`; cockpit.css:13 `direction: rtl`; journey.js:29 `.nljy{...direction:rtl}` and journey.js:181 `.nljy-entry{...direction:rtl}` (CSS inside the JS).

**Physical left/right that should follow the reading side**
- showroom.css:26 `.nlsr-cap{...left:12px}` (inline-end), :27 `.nlsr-hint{...right:10px}` and :31 `.nlsr-back{...right:10px}` (inline-start). Use `inset-inline-*`.
- cockpit.css:42 `.nlck-tile{...text-align:right}`, :63 `.nlck-strip button{...text-align:right}`; journey.js:57 `.vc{text-align:right}`, :60 `.vc small{text-align:left}`. Use `start`/`end`.
- cockpit.js:241 the panorama is centred with a negative `scrollLeft` (`pan.scrollLeft = -(pan.scrollWidth - pan.clientWidth) / 2`). Negative scrollLeft is the RTL convention; under LTR it clamps to 0 and the view opens at its left edge. Needs a sign by direction.

**Physical left/right that must NOT flip (geography or mechanics)**
- showroom.css:59 `.nlsr-ml--sea{left:6px}` and :60 `.nlsr-ml--n{right:6px}`: the sea is west on the map picture; showroom.js:243 alt says so. Keep physical.
- journey.js:50 `.ladder input{writing-mode:vertical-lr;direction:rtl}`: this is what puts floor 1 at the bottom of the vertical slider. Functional, keep in every language.
- journey.js:69-70 `.tapl{left:0}.tapr{right:0}` story tap zones; showroom.js:205 drag turns the tower by physical `dx`; showroom.js:220 ArrowLeft/ArrowRight step frames; cockpit.js:222 360 drag by physical `dx`. Spatial, not reading order: no change needed.
- Positions from picture coordinates (showroom.js:76 handle `left:%`, :87 tag `left`, journey.js:108 tower button `left:px`) are image space and stay.
- Already logical and fine both ways: showroom.css:74; cockpit.css:31-34, 44, 46, 53, 69, 74, 128; cockpit.css:145 (desktop panel: `inset:16px auto 16px 16px` then `inset-inline-start/end`, the logical pair wins). cockpit.css:127 `padding-inline-start:76px` leaves room for the site's accessibility button: check which corner that button sits in on an LTR page.
- showroom.css:93 the wide-screen grid ('head stage') follows `direction`, so in English the model moves to the right column; the comment at showroom.css:91 ("the reading side first") says that is the intent.

**Arrow glyphs inside strings**
- "back" glyph `›` leading: showroom.js:238, cockpit.js:91, cockpit.js:107, journey.js:98 (button text). In LTR it must be `‹`.
- "forward" glyph `‹` trailing: showroom.js:126, cockpit.js:217 (door hotspot label + ' ‹'). In LTR it must be `›`.
- Neutral: showroom.js:240 `↔`, showroom.js:244 `↑` (north, geographic), journey.js:98 `✕`, basket.js:99 `×`.

**Number formatting**
- cockpit.js:20 `toLocaleString('he-IL', ...)` (used by `num`, `ils`, every price, distance and the share text at cockpit.js:305).
- basket.js:14 `new Intl.NumberFormat('he-IL', ...)` (price input re-format at :267, every ₪ line, the WhatsApp message at :329).
- showroom.js and journey.js format no numbers (floor numbers and `toFixed(1)` only).
- Units in the strings: `מ׳` means metres at cockpit.js:93, 174, 192, 304 and journey.js:120, 156, but MILLION at cockpit.js:147 (`${...} מ׳ ₪`). `דק׳` minutes at cockpit.js:174. `מ״ר` at cockpit.js:160 and in cockpit.json `deals[].apt`.
- ₪ is written after the number everywhere (cockpit.js:22, 101, 147, 305; basket.js:15); English expects `₪` before.

**Dates**
- No `Date` formatting in the four files. Dates come as text from data: cockpit.json `deals[].date` "M.YYYY" (printed at cockpit.js:147); basket `C.tax.effective` "16.1.2025" (inc/calculators.php:36, printed at basket.js:296); basket `C.tax.frozen` is Hebrew words, "ינואר 2028" (inc/calculators.php:37).

**Hebrew grammar baked into code**
- showroom.js:105 the prefix letter מ ("from") is glued to a variable: `מ${esc(DIRN[...])}`.
- basket.js:236 and :321 the prefix ב ("at") is glued to the project name: `'...סל דירה ב' + C.name`.
- Word-order concatenation that English reverses: basket.js:235 (`'עוד אין במאגר ' + t.ask + ' באזור.'`), basket.js:248 (`'להוסיף את ' + p.name + ' לצוות'`), cockpit.js:131 (`'גימור ' + P[1]`), basket.js:297 (`lawPct + '% מהמחיר...'`). All need templates with variables.

**Hebrew used as data, not just display**
- showroom.js:256 finds the call button by its Hebrew text: `callRow().replace('שיחת וידאו עם נציג', 'שיחת וידאו עכשיו, עם נציג')`. Breaks in any other language.
- showroom.js:151 the `nl:facing` event carries `facing: DIRS[...]` and `label: 'מגדל ' + tower` in Hebrew; basket.js:51 stores `label` in localStorage (key `nl-basket:<slug>`) and prints it later (basket.js:38, 322). A choice saved on the Hebrew page stays Hebrew on the English page.
- Analytics values are Hebrew words: showroom.js:165 `facing: DIRN[...]`, cockpit.js:272 `facing: dirWord(...)`. Translating them would split the reports; send a fixed code (bearing or n/ne/e...).

**Hebrew-only regexes**
- None in the four files (the regexes are `#dira=` hashes, `/kikar|hamedina/i`, `/[^\d]/`). One side effect for Arabic: basket.js:75, 268 and 306 strip everything but ASCII digits, so Arabic-Indic digits typed into the price are dropped.

**Fonts**
- showroom.css:9, 39 and journey.js:40, 55, 184 use 'Noto Serif Hebrew' with Georgia as fallback: English falls to Georgia, Arabic gets no chosen face. A per-language face is a design decision (design law: name the faces).

## Data files with Hebrew the UI prints

- `assets/project-stage/hamedina/cockpit.json` (printed by cockpit.js): `deals[].apt` "4 חדרים · 140 מ״ר" (cockpit.js:147), `deals[].src` "גלובס" (:153 via `D.deals[0].src`), `tax.asof`, `arnona.asof`, `mortgage.src` "בנק ישראל", `mortgage.label` "קבועה לא צמודה (קל״צ)", `fee.src` "מעריב", `fee.note` (all :166). Hebrew but not printed: `deals[].psqm`, `sums.*`, `arnona.type`. No language key exists in the file; the simplest fix is `apt_en`-style siblings or an `i18n: { en: {...}, ar: {...} }` block.
- `assets/project-stage/hamedina/places.json` (cockpit.js:174 prints `p.name`): 1,245 places, 1,141 with Hebrew names, only 370 carry `names.en`/`names.ar`. world.js:2393-2395 already has the rule to reuse: the page language's name, else English, else leave the place out (a Hebrew-only name is not shown).
- `turn/turn.json` and `aerial.json`: no Hebrew.
- `assets/project-stage/hamedina/world-i18n.json` (v1): fr, ru and ar, 107 entries each, keyed by the English text of world.json (civic places, park features, landmarks, stations). It is read only by world.js (world.js:959-976, `overlayWords`) for the 3D world. It has no `en` block (English is the key) and none of the showroom, cockpit or basket words; the place-kind and group words the cockpit needs already exist per language in world.js `I18N.<lang>.kinds` / `.cats` (world.js:141, 243, 347, 448, 549 and 114, 213, 318, 419, 520).
- PHP-side words the basket prints: team slot labels and the profession asked for (inc/basket.php:31-36), the project name `$ps['name']` (:121), `$ps['sectors']` direction words (:118), `$ps['basket_hint']` (:125), `tax.frozen` (inc/calculators.php:37). The Hebrew poster alt for the showcase is inc/project-stage.php:1178.

## Recommended minimal approach

1. **One strings module** `assets/project-stage/world/showroom-i18n.js` (ES module) exporting `STR = { he: {...}, en: {...}, ar: {...} }` keyed as in the JSON, plus:
   - `lang()` → `(cfg.lang || document.documentElement.lang || 'he').slice(0, 2)`, unknown → `'en'` (same rule as world.js:759-760);
   - `dir(l)` → `'rtl'` for he and ar, else `'ltr'`;
   - `t(key, vars)` → template with `${name}` replacement, falling back to `en`, then `he`;
   - `nf(l)` → `Intl.NumberFormat` per language (`he-IL`, `en-US`; for `ar` keep Latin digits as world.js does at :2915) and `money(n, l)` placing ₪ per language;
   - `glyph.back(l)` / `glyph.fwd(l)` for `›`/`‹`;
   - the shared tables once: `DIRS`, `DIRN`, `SECTORS`, `GROUPS`, `KINDS` (or import the kinds/cats from world.js's I18N).
2. **PHP passes the language**: add `'lang' => $tl` to `$cfg['next']['cockpit']` and `['journey']` (project-stage.php:1181-1197) and to the basket config (basket.php:120-132); widen `nadlan_ps_kikar_next()` (project-stage.php:1122) and `nadlan_bk_on()` (basket.php:23) to en/ar when the strings are ready. The modules read `C.lang` first and `<html lang>` second.
3. **Set direction from the language**: replace the four hard-coded `dir='rtl'; lang='he'` (showroom.js:232, cockpit.js:255, journey.js:161, basket.js:91) with `dir(L)` / `L`; drop `direction:rtl` from showroom.css:6, cockpit.css:13, journey.js:29, :181 (the element's `dir` attribute is enough); make showroom.css:26/27/31, cockpit.css:42/63, journey.js:57/60 logical; keep showroom.css:59-60 and journey.js:50 physical.
4. **Basket**: it is a classic deferred script, not a module, and also serves other project pages. Minimal path: PHP prints the basket's words for the page language into `nadlan-basket-cfg` (it already prints `team`, `name`, `sectors` there), generated from the same table; or the basket reads `window.__nlI18n` (set by the strings module) with its Hebrew as fallback.
5. **Stop passing words between modules**: `nl:facing` should carry tower/floor/bearing only; the basket and the cockpit build the label in their own language (removes the stale-Hebrew-in-localStorage problem). Analytics get codes, not words.

Functions that print words and must read the language (a module-level `L` set at mount, or a `lang` parameter for the pure helpers marked *):

- showroom.js: `sectorOf`*, `paintPic`, `paintHandles`, `paintBand`, `paintMap`, `facingText`, `waHref`, `paintCard`, `paintSteps`, `paintHint`, `announce`, `callRow` (+ the `.replace` at :256), `mountShowroom`; tables `DIRS`, `DIRN`, `SECTORS`, `STEPS`.
- cockpit.js: `num`*, `ils`*, `dirWord`*, `sectorOf`*, `label`*, `home`, `subTop`, `scrView`, `roomsRow`, `scrInside`, `scrFac`, `scrPlan`, `scrPrice`, `scrArea`, `scrSave`, `pano` (door labels), `render` (pan centring sign), `paintBar`, `mount`, `onClick` (toasts, share text); tables `DIRS`, `SECTORS`, `GROUPS`, `KINDS`, `PANOS`, `FACS`, `ROOMS`, `DOORS`.
- journey.js: `dirWord`*, `sectorOf`*, `top`, `render`, `onInput`, `open`, `mountJourney` (entry markup), the `css` string; tables `DIRS`, `SECTORS`. (Only the `?kikar=journey` path still uses it; the showroom is the default.)
- basket.js: `nf`/`ils`*, `unitLine`*, `build`, `steps`, `renderUnit`, `renderStyle`, `renderTeam`, `prosBox`, `renderPrice`, `message`, `renderActions`, `entry`, `mount`; tables `BUYERS`, `STYLES`.

Owner items before anything ships: the WhatsApp texts (12 entries marked AWAITING BEN), the share text (cockpit.js:303-305), the legal notice (basket.js:348), and the English name of the basket ("My selection" proposed; literal "Apartment basket").
