# Design round 2 (HAD-707), 11.11.2026

Canvas (private, Claude Design): https://claude.ai/artifact/V8wiqeJ4qtS4qnzgxmXyCA
Round 1 (boards 1 to 7) is untouched. Round 2 adds boards 8 to 17 in five new rows below it.

## Boards added

| # | File | What it is |
|---|---|---|
| 8 | HubPhone.dc.html | Hub `/design-studio/` v2 at 390: H1, answer, two buttons, the engine block (real plan capture with dimension lines, north arrow, scale bar, numbered callouts, title block, 3D and walk captures), the legend of the 7 working features, the two-way choice, the 20-tool index, the online designer and consultation section (real call capture), questions, the two sibling pages |
| 9 | HubDesktop.dc.html | Same source at 1440 (two-column hero, 4-column legend and tool index, 4-step timeline) |
| 10 | CostPhone.dc.html | `/design-studio/designer-cost/` at 390: the fee calculator as a schedule (five pricing models side by side on one 0 to 80,000 ₪ ruler), the 16-row price schedule, costs by 3/4/5 rooms drawn to scale, the quote checker plus "what is included" matrix, the payment chain dimension, saving options, contractor-flat note, questions |
| 11 | CostDesktop.dc.html | Same source at 1440 |
| 12 | DesignersPhone.dc.html | `/profession/מעצב-פנים/` at 390: the four-question "which professional do I need" chooser, the neutral list (filters, record cards, claim/remove link, the self-updated record state, empty state), "bring your own designer" into the plan and the call, the choosing guide as numbered drawing notes, the role section with the architect link, questions, join the list |
| 13 | DesignersDesktop.dc.html | Same source at 1440 (filter column + two-column records) |
| 14 | EnginePoints.dc.html | Engine, phone: electrical points sheet, redrawn from module-evidence m4/m6 |
| 15 | EnginePartition.dc.html | Engine, phone: new-partition drawing mode, redrawn from module-evidence m5 |
| 16 | ToolAnatomyPhone.dc.html | The shared pattern of every tool, drawn once on a real example (parquet for the 30.4 m² living room), with its four states and six build rules |
| 17 | ToolAnatomyDesktop.dc.html | Same source at 1440 |

Assets uploaded to the canvas: `plans-evidence/example-4r.png` (the plan) and `call-evidence/c7-buyer-sees-rep-pointer.png` (the call with the pen). The two round-1 captures (3D from above, walk view) are reused.

## Palette and faces

Drafting white `#F2F5F7` (ground), white `#FFFFFF` (sheets), plan ink `#0F2233` (text, rules, dark bands), blueprint blue `#1F5FA8` (only what you can touch, move or press; blue tint `#D6E5F6` for the active mode), dimension red `#B5302A` (only measurements and stop messages), green `#1C7A4E` (only "included" / "free"), greys with a blue bias: `#33475A` body-2, `#46596A` labels, `#B9C6CF` hairlines, `#DCE4E9` grid, `#E6ECF0` panel.
Faces: IBM Plex Sans Hebrew (everything), IBM Plex Mono (every number, size and price, tabular).
Why this is not the default look: it is taken from the architect's working drawing (dimension lines with slash ticks, section bubbles, title block, north arrow, scale bar, chain dimension, numbered general notes) and from a drawing-office schedule, not from a web template: no cream, no gradient, no rounded soft-shadow cards, no serif, no Inter, everything aligned to a hard grid with 2 px ink rules.

## Rules a builder must follow

**One source per page.** Each phone and desktop pair is the same file; the layout changes by a container query at 960 px (`.pg{container-type:inline-size}`). Build the page once, responsive; do not fork a desktop page.

**Spacing scale (px):** 4, 8, 12, 16, 24, 32, 48, 88. Side gutter 16 on phones, 48 on desktop; max content width 1312. Section padding 48 (phone) / 88 (desktop). Every section opens with a 2 px ink rule.

**Type scale (phone / desktop):** H1 35-38 / 60-72, weight 700, line-height 1.04-1.1, letter-spacing -0.015em, balanced wrap. H2 27 / 40. H3 19 / 22. Lead 18 / 20 at 1.62. Body 17. Secondary 15.5 in `#33475A`. Labels 12.5 bold, +0.04em, `#46596A`. Numbers always mono.

**Components:**
- Buttons: primary blue fill 54 px high; secondary white with 2 px ink border; on hover both go ink. Square corners everywhere. Chips 44 px, selected = ink fill.
- Section bubble (H2 marker): 48 px circle split by a line, section number above, total below, mono.
- Engine figure: drawing area with a dimension-line overlay (red, slash ticks), north arrow, scale bar 0-3 m, numbered blue callouts matching a legend; title block strip under it (apartment, rooms, area, ceiling height).
- Range bar: thin ink line with end ticks = everything published; blue band = the typical range. LTR ruler, mono labels.
- Schedule table: ink header row, grey group rows, hairline rows, scrolls inside its own frame on phones.
- Record card (directory): index number, name, city · region, speciality tags, one neutral line, published pricing only, "to the business's site", footer "made from public information, not a partner" + "this is my business: update or remove". Self-updated records get a blue border and a "העסק עדכן בעצמו" tag. Order is alphabetical, never ranked.
- Numbered notes (guides): mono blue number + bold title + one line, like general notes on a drawing sheet.

**States:** every tool opens filled from the plan (never empty); missing input = blue prompt in place of the number; fewer than three sources = full range only, labelled "מעט מקורות", no typical range invented; stop = red sentence that says what to do. Engine modes show a blue tint banner with the one-line instruction.

**The tool pattern (board 16):** A name (a Google phrase, real heading) · B one-line question · C inputs with ready values from the plan · D the result as a full Hebrew sentence on an ink band, live, no "calculate" button · E the range bar with its basis (number of sources, VAT, "נבדק בנובמבר 2026", no site names) · F "how this is calculated", closed by default.

**Engine fixes shown on boards 14-15 (vs. the m4/m5/m6 captures):** the plan keeps the screen while editing (the 3D view shrinks to a 92 px thumbnail instead of taking the top half and the sheet covering the plan); symbols drawn at one size (about 16 px) with 7-unit strokes, oriented to their wall; room names and areas sit in the lower part of each room, lights in the upper part, so labels never collide with symbols; windows drawn as double lines (not blue, since blue means "movable"); the safe room hatched; counts per symbol type on the buttons; the price of the change shown at once as a range; the new partition gets its length and its distance from the wall as red dimensions, both rooms' new areas live, a door option, and 44 px end handles.

**Content laws kept:** headings only from `heading-evidence-designer.md` and `heading-evidence-v2.md` (non-evidence titles are drawn as styled paragraphs, not headings); no H2 on שינויי דיירים or אדריכל (link only); prices only from `prices-items/designer-fees.json` and `price-ranges.json`, as ranges with the unit and "נבדק בנובמבר 2026"; no site names on any board.

## Left as placeholders (no facts yet)

- Designer listings: no `market/listing/designers-listing.json` exists, so every record is `[שם הסטודיו] · [עיר]`, `[משפט ניטרלי]`, `[תמחור]`; the result count is `[מספר]`.
- Online consultation price: no checked range; shown as `[טווח מחיר, אין עדיין נתון שנבדק]`. The in-home meeting range (800-1,800 ₪) is shown instead, labelled as such.
- The list of designers who offer online consultation and the "תיאום שיחה" booking: shown as a bracketed slot; per the honesty law it ships only when a real designer has joined.
- Payment split per stage: `[%]` on all four stages.
- "Design in one day" price and the architect's fee: bracketed.
- "What is included by service level" matrix: drawn from the service definitions; marked `[לאמת מול הצעות אמיתיות לפני פרסום]`.
- Most FAQ answers: `[תשובה]`.
- Site logo: `[לוגו האתר]`. The link to the tenant-changes guide and the architect page are anchors on the boards.
- Board heights on the canvas are estimates (the pages are fluid); a frame may show blank space at its bottom.
