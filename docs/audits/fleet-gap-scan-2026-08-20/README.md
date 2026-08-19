# Fleet gap scan — images + missing info (2026-08-20, Fable 5)

**Method:** 36 surfaces fetched server-side (custom UA) + JS-rendered eyes pass via headless
Chrome (playwright-python is now ALSO blocked by Smart App Control — greenlet DLL; Chrome
headless direct is the working eyes rig on this machine). Raw data: `fleet-scan-results.json`
in this directory. Owner order 20.8 (voice): scan only, no content writing — ChatGPT writes,
agent delivers, this doc is the map + the agent contract.

## 1. Headline findings (evidence class per line)

| # | Finding | Evidence | Scope |
|---|---|---|---|
| 1 | **Fleet has almost no content images.** 0 `<img>` in rendered body: duo, h-infinity, the-park, akirov, yoo, meier, toha2, stricker, bnei-dan. Rainbow has 4 (hero/amenities/location + tour poster), ashira 1, dimri 1, einstein 1, gindi 1, utopia 5. | code | fleet |
| 2 | **Hero visuals are generic cream sketches** that do not match the real buildings: einstein (3 generic white towers), duo (watercolor twins), yoo (sketch), meier (flat slab — nothing like the iconic white Meier tower), stricker (sketch). Utopia/gindi/h-infinity/akirov/toha2: NO visual in first folds at all. | eyes (headless shots in scratchpad session) | fleet |
| 3 | **THE PARK renders a black band with a broken-image icon** — `model_poster` is an empty string (CEO report 8.11 confirmed). Visible defect on a flagship. | eyes+code | the-park |
| 4 | **Language siblings lost their showroom payload**: yoo/meier/gindi/toha2/the-park -en/-fr/-ru/-ar have units=0 (mains that have units!) and/or `model_poster` empty, and up to 9 empty headings each. This is the sanitizer-drop class the CEO report warned about (9.7) — happening wholesale, not just hotspot_position. **Code-fix lane, not an image lane.** | code | ~20 sibling pages |
| 5 | **"מימון, ייעוץ ועיצוב - הכל במקום אחד" is an EMPTY heading on 10+ pages** (einstein, duo, the-park, akirov, yoo, meier, toha2, h-infinity, stricker, bnei-dan). Site-wide empty promise box. | code | fleet |
| 6 | Einstein empty headings: **כיום / בעת האכלוס / חבילת המסמכים שכדאי לבקש / למי הפרויקט עשוי להתאים** — 4 headings with zero content. Utopia: **הבניינים והדירות** empty. Dimri: 2 empty legal headings. | code | 3 pages |
| 7 | **Feature-bar "בקרוב" disease**: yoo 6/7 features disabled-בקרוב (even המודל התלת ממדי!), meier 5, the-park 3, duo 3, einstein 2, utopia 2, gindi 2. "מה אפשר לעשות כאן" that mostly says "not yet" = anti-"30-years-running". | eyes | fleet |
| 8 | The owner-named promise sections (**כל מה שמסביב / פרויקטים סמוכים / פונים מחו"ל**) do NOT exist on any fleet page — not even as empty headings. The disease today = sections missing entirely + the empty headings above. | code | fleet |
| 9 | **Alt-text gaps**: `sdedov-tour-poster.jpg` has NO alt everywhere it appears (homepage, rainbow, sde-dov); homepage has **2 `<img>` with empty src** (broken); rainbow's 3 images share one identical alt. | code | site chrome |
| 10 | FAQ answers exist but are thin (120–190 chars each); "שאלות נפוצות" heading-empty hits are structural false-positives (h3 questions follow). | code | fleet |

## 2. Einstein numeric claims — for owner verification (NOTHING changed)

**There is NO "33,000" anywhere on /projects/einstein-tower/** — checked server HTML AND
JS-rendered text. The figures that ARE on the page:

- Project: **215 יחידות דיור** (explicitly framed as program size, not stock) · מגדל **28 קומות** + שני מבנים **13 קומות** (דף קשור של חג'ג' מציג 12) · **3 מבנים** מעל בסיס מסחרי כפול · גוש **6885** חלקה **32** · איינשטיין 33א' (שם בדוח החברה) · איינשטיין 18 = שם עבודה, חלקה 40 סמוכה · כתובת היתר: איינשטיין 14 · **4 קומות חניה**.
- Permits/timeline: היתר **20241734** מ-9.7.2026 · בקשה **20231320** · מצב מדווח: חפירה ודיפון (31.12.2025) · הערכת חברה להשלמה: **רבעון 3 2030** · כתבה 1/2026 הזכירה סוף 2029 · נת"ע: עבודות תשתית בצומת 16.7.2026 · קו ירוק מקטע דרומי: **2028**.
- District: **כ-16,000 יחידות דיור** ברובע (עירייה) · school סמל מוסד **30064** (נופי ים).
- Map estimate chips (אומדן ₪/מ"ר, לא מחייב): FIRST **75,000** · GINDI VOGUE **54,000** · ASHIRA **75,000** · DIMRI YAMA **75,000** · RAINBOW **76,000** · ZOHI **90,000**.

If the owner saw 33,000 somewhere, it is not on this page today — possibly another page or an
older version. The only district-scale numbers now: 16,000 units / 40,000 residents (on /sde-dov/).

## 3. Image-factory pipeline — the agent↔ChatGPT contract (v1)

Owner will NOT write prompts. An agent (his Chrome extension / cowork) runs this loop per project:

**Stage A — facts first (research, no invention):** developer's official site + press for:
verified facilities list, building form (towers/floors/cladding), status, surroundings, view
directions (from our geo data). Output `facts-{slug}.json`. NO facility enters a prompt that
is not verified — honesty law.

**Stage B — prompt chain (ChatGPT images, one after another).** Fixed series per project,
every prompt carries: style block (premium Israeli real-estate photography; warm cream/ink/gold
grade to match site DNA; no text/logos/watermarks ON the image; no recognizable faces),
aspect + minimum size, and the project facts. Series:
1. `hero` — exterior dusk, real building form, 16:9 ≥2400×1350
2. `exterior-day` — street level, 4:3 ≥1600×1200
3. `lobby` — interior, 4:3
4. `facility-icons` — the owner's beloved colorful icon-board style, 1:1 ≥1600×1600, **icon-safe framing: all icons inside the central 60%; nothing within 20% of any edge** (survives 16:9 and 4:3 crops)
5. `interior-living` + 6. `interior-bedroom` — per real spec (rooms/sqm), 4:3
7. `balcony-view` — direction-true (sea/park per geo dir), 16:9
8. `floor-plan` — clean schematic PNG, labeled-in-caption not on image
9. `amenity-{name}` — one per VERIFIED facility (pool/gym/spa/lounge)
Listings keep REAL photos (never sketches). Generated goes only where no developer material exists.

**Stage C — delivery contract (what ChatGPT-agent hands back):** per image a manifest row:
`{slug, type, seq, filename, alt_he, caption, placement}` where
filename = `{slug}-{type}-{NN}-{hebrew-keyword-translit}.jpg` (e.g.
`duo-tel-aviv-hero-01-migdaley-duo-tel-aviv.jpg`), alt_he = full Hebrew sentence with project
name + type, caption = `הדמיה להמחשה` for every generated asset (caption text, NEVER printed on
the image), placement ∈ {hero, gallery, facility-board, plan-tab, og}. Sizes as in Stage B;
JPEG quality 82+; plans as PNG.

**Stage D — placement (deploy agent, this pipeline):** manifest → REST media upload with
SEO filename + alt → wire hero/meta/og/galleries per placement → eyes verify per page → fleet
spot-check. Nothing placed without the caption law.

**Priority order (from this scan):** 1) THE PARK poster (visible defect) · 2) einstein hero ·
3) duo/yoo/meier heroes (mismatch class) · 4) fleet interiors+plans (flagships first) ·
5) facility boards fleet-wide · 6) alt sweep (chrome images + empty-src fixes) ·
(parallel code lane, not images: language-sibling payload loss #4, empty "מימון" box #5).

## 4. Kept as improvement maps (owner order)

- `nadlan-shark-business-plan.md` (Downloads) — money/GTM critique; owner corrections 20.8:
  lawyer lane NOT a direction now; 5-language foreign exposure IS the strategy; materials have
  developer releases where noted (EcoCity CEO explicit; Rainbow editorial-premier).
- `nadlan-3d-ceo-report-2026-08-19.md` (einstein repo docs/reports/) — 3D truth map, patches 8.1-8.13.
- This scan — the images/info work-list.
