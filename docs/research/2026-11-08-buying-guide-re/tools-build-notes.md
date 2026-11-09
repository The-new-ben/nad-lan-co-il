# Buying guide, Phase 3 tools and reading layer: build notes (HAD-686, 9.11.2026)

Local work only, in `C:\Users\777\nad-lan\nad-lan-co-il`. Nothing released, nothing committed or pushed, no deploy script run,
no call to the live site. `inc/price-nudge.php` and `assets/nudge/` untouched (0 changes).

## Files (size in bytes, md5)

Plugin (ships at release):

| File | Status | Bytes | md5 |
|---|---|---|---|
| plugins/nadlan-config/assets/instruments/tools/buying3.js | new | 57772 | 74ec3d8bafcbf59534b67ae30a42254e |
| plugins/nadlan-config/assets/instruments/tools/buying3.css | new | 20317 | f9c4f975d90bedfdd3d1ff5134e489a5 |
| plugins/nadlan-config/assets/instruments/data/buying.json | changed | 39045 | c0690e96c61d442d0eb210dea1bcb385 |
| plugins/nadlan-config/inc/buying-hub.php | changed | 47683 | aae3128ca9c7cc8e611771e30730a7a7 |
| plugins/nadlan-config/assets/instruments/tools/buying.js | changed (1 line) | 65859 | 24a6df652341ad3fec2a7c0a0af77e5f |
| plugins/nadlan-config/assets/instruments/tools/buying2.js | changed (bdates, 4 lines) | 37993 | 94e21951c25b22e40c82666a0bf5df89 |

Tests and local preview (not shipped):

| File | Status | Bytes | md5 |
|---|---|---|---|
| tools/instruments/test_buying_hub.js | changed | 32211 | 6f6ba7aa0effa7336389765f1a86a778 |
| tools/instruments/build_buying_harness.py | changed (loads buying3.js and buying3.css too) | 5256 | f18c5f642bec80b610a39f991b4cd95f |
| tools/instruments/build_buying3_harness.py | new | 6073 | d97564045f3532e79d0d463678815ed4 |
| tools/instruments/shot_buying3.py | new | 24903 | eeaf03ba5d56345350d97e8739d1b983 |
| tools/instruments/harness_buying3_src.html | new (sample page: map, 5 chapters, glossary, the 5 shortcodes) | 12579 | b9adcb5ec8eb0c19e5bb95746556279d |
| tools/instruments/harness_buying3.html, harness_buying3_plain.html, _buying3_*.html/json | generated | | |
| tools/instruments/harness_v3.html, harness_v3_plain.html, _v3_*.html/json | generated from page-9-v3.html | | |

All touched and generated files: LF only, no U+2013 or U+2014, JSON parses. The saved theme shell had two long dashes inside the
theme's own CSS comments; the local copy replaces them with a hyphen (the live theme is not touched).

## What each change does

- **buying3.js**: the five tools (pure logic in `window.NLBH3`, tested in Node) and the reading layer (`window.NLBG`). The reading
  layer runs on its own, without any tool on the page.
- **buying3.css**: the reading layer classes, plus `h3.nli__title` for a tool placed inside a chapter.
- **buying.json**: new keys `pay`, `sign`, `keys`, `reg`, `reg_note`, `memo`, and `laws.land8` (Land Law section 8, text and
  link read on wikisource 9.11.2026). The `note` field says what each key is. No number written in the content: percentages and
  days are placeholders filled from `orechdin.json` and `ptax.json`.
- **buying-hub.php**: registry entries for bpay, bsign, bkeys, breg, bmemo (file `buying3`, deps prices-common, buying,
  buying2); `nadlan_bhub_tool_ids()` now lists 15; the five server summaries; the `h="3"` option; an enqueue (priority 21) that
  loads `buying3.css` and `buying3.js` on every page with any buying tool.
- **buying.js** (panel): the tool keeps the heading level the server printed (h3 stays h3 after the script draws the tool).
- **buying2.js** (bdates): bdates now saves its signing date in the shared plan store (`localStorage nlbh-plan-v1`, field
  `sign`) and sends `nlbh:sign`; it also reads a date set in bpay or breg. Before this, bdates saved nothing, so "prefill from
  bdates" had nothing to read.

## Shortcodes and attributes

```
[nadlan_tool id="bpay"]     לוח התשלומים שלכם בעסקת יד שנייה
[nadlan_tool id="bsign"]    יום החתימה: מה מביאים, על מה חותמים, עם מה יוצאים
[nadlan_tool id="bkeys"]    פרוטוקול מסירה וקריאת מונים
[nadlan_tool id="breg"]     מעקב רישום: מהחתימה ועד נסח על שמכם
[nadlan_tool id="bmemo"]    חתמתם על זיכרון דברים? בודקים בדקה
```

- `h="3"`: works for all 15 buying tools (the ten old ones too). Inside a chapter whose head is an h2, write
  `[nadlan_tool id="bpay" h="3"]`. The tool title is then an h3 in the server HTML and after the script runs; sub-heads inside
  that tool become h4. Any other value, or no `h`, changes nothing. **`id` must come first**: the engine finds the tools of a page
  with `\[nadlan_tool\s+id="..."`, so `[nadlan_tool h="3" id="bpay"]` would not load the scripts.
- The engine's own presets (`city`, `price` and so on) are not used by these five tools.

## Class names the content must use

Guide map (one block, before the first chapter):
```
<nav id="nlbg-map" class="nlbg-map" aria-label="מפת המדריך">
  <h2>...</h2> <p class="nlbg-map__lede">...</p>
  <div class="nlbg-map__phases">
    <div class="nlbg-map__phase"><h3>לפני שקונים</h3>
      <ol class="nlbg-map__chips"> (or ul)
        <li><a href="#nlbg-c1" data-ch="c1"><b>1</b>תקציב ומחיר נוח</a></li>
```
The script adds the dot (`<i>`), a hidden "(נקרא)" for screen readers, `is-read` (chip and chapter) and `is-now` +
`aria-current="location"` (the chip of the chapter in view), and a line "קראתם N מתוך M שלבים" with a button "ניקוי הסימון"
(shown only once something was read). Any number of phases: one column on phones, two from 640 px, all in one row from 1000 px.
A chapter counts as read when 60% of it has passed the middle of the screen and the reader stops there (400 ms with no scroll),
so a jump through the page marks nothing. Kept in `localStorage nlbg-read-v1`. Nothing is ever hidden.

Chapter:
```
<section class="nlbg-ch" id="nlbg-c13">
  <p class="nlbg-kick">שלב 13 מתוך 18 · אחרי החתימה</p>
  <h2>...</h2>
  <p class="nlbg-ans">the answer sentence</p>
  <div class="nlbg-who"><span>רשם המקרקעין (טאבו)</span><span>עורך הדין</span></div>
  <div class="nlbg-todo"><p class="nlbg-todo__t">מה עושים בשלב הזה</p><ol><li>...</li></ol>
     <p class="nlbg-todo__tool"><a href="#...">הכלי לשלב הזה: ...</a></p></div>     (title may also be h3, h4 or .nlbg-todo__h)
  <div class="nlbg-note nlbg-note--stop|--field|--fig"><p class="nlbg-note__lab">עצרו|מהשטח|מספר רשמי</p><p>... <b>188 ₪</b></p>
     <p class="nlbg-src">מקור: <a href="...">...</a> · נבדק D.M.YYYY</p></div>
  <div class="nlbg-tw"><table class="nlbg-tbl"> ... <td data-l="column label">...</td></table></div>
  [nadlan_tool id="bpay" h="3"]
  <p class="nlbg-back"><a href="#nlbg-map">חזרה למפת המדריך</a></p>
</section>
```
In `--fig` notes, every `<b>` or `<strong>` is the figure (mono, on the yellow marker). Tables: wide screens keep a real table;
phones show each row as a card, every cell headed by its `data-l`. The chapter carries the 3 px ink rule at its top.

Glossary:
```
<section class="nlbg-glossary" id="nlbg-glossary"><h2>מילון המונחים לקונה</h2>
<dl id="nlbg-gloss" class="nlbg-gloss"><dt>...</dt><dd>... <a href="#nlbg-c5">שלב 5</a></dd> ... </dl></section>
```
(`dt`/`dd` pairs, or `div > dt + dd`.) The script puts a labelled search field right above the `dl` ("חיפוש במילון המונחים") and a
live count ("69 מונחים", "5 מונחים מתוך 69", "מונח אחד", or "לא נמצא מונח כזה"). Niqqud, maqaf and quotes do not matter
(רמ"י finds רמ״י). Without JS the full list shows.

## The tools, briefly

- **bpay**: inputs price (starts at the national 4-room median of prices-hub, with its quarter), the buyer's mortgage (starts at
  75%, the single-home LTV of nrm.json), the seller's balance (0), the first payment in % (starts at 10; the help says it is set in
  the contract and is the reader's to change; no "customary" claim), the advance (7.5%, 15% for a flat bought before 7.11.2001,
  or none when the seller shows a certificate), optional signing date (prefilled from the shared plan) and handover date. Output:
  the five payments in order with when, amount, to whom, own money or mortgage, and what protects the buyer; the advance row
  quotes the bwho row text with the same source (חוק מיסוי מקרקעין סעיף 15, נבדק 26.10.2026) and names the payment that crosses
  40%. The buyer's own money pays first; when the seller's balance is larger than the money left, the mortgage pays the rest of
  it straight to the seller's bank (a warning says so) and the handover payment can reach 0 (a warning says so). Errors in plain
  Hebrew: no price, mortgage above the price, first payment out of 0 to 100 or above the buyer's own money, first payment plus
  advance above the price, seller's balance larger than what is left after the first payment and the advance, handover before
  signing. Warnings: LTV above 75%, the split, the advance paid from the mortgage, the 40% crossed at signing, nothing left for the
  handover. Totals, a five-part bar with a legend, the 30 and 60 day dates (the bdates rule), share bar, print or PDF, a reset.
  Saved in `nlbh-pay-v1`.
- **bsign**: the three lists from `buying.json sign` (5, 4, 3 items), ticks saved in `nlbh-sign-v1`, the dates filled when a
  signing date is known, print or PDF with tick boxes, a reset.
- **bkeys**: handover date (prefilled from bpay's handover date), electricity, water and gas readings, keys and remotes, defects
  and what stays (one per line), the five transfers. Every transfer's `how` and `src` are empty in buying.json: the content team
  copies the official wording and its page (`src` = `{label, url, date}` or a `laws` key). Empty values are hidden everywhere.
  No phone number or procedure was invented. Print or PDF with two signature lines. Saved in `nlbh-keys-v1`.
- **breg**: ten steps from `buying.json reg`, each with who and the proof, status טרם / נשלח / התקבל (saved in `nlbh-reg-v1`),
  due dates for the declaration (30 days) and the tax (60 days) from the shared signing date, "המועד עבר" in red when late and not
  received, a note on ILA and housing-company flats, print or PDF, a reset.
- **bmemo**: six yes or no questions. high = price and flat identified, and (both signed and not "subject to contract") or money
  paid; mid = any of essentials, both signed or money paid; low = none of these. Each level has its plain next step, the reasons
  from the answers, section 8 quoted with its link and date, and "זה לא ייעוץ משפטי; זו רשימה של מה לשאול את עורך הדין."
  Answers live only in memory and are gone after a reload.

## Tests and checks run (all on 9.11.2026)

- `node tools/instruments/test_buying_hub.js`: **130 passed** (90 before, 40 new: content shape, the five payments always add up
  to the price across 1,000+ valid cases with own money and mortgage split exactly, the design case 245,000 / 420,000 /
  1,500,000 / 183,750 / 101,250, the advance at 7.5%, 15% and 0, the 40% crossing, the split case, every validation case, the
  dates equal to bdates, the LTV warning, the bmemo scoring cases, the breg and bsign helpers, the glossary key, the read rule,
  and the PHP summaries: 15 markers, 5 payments, 12 list items, 10 table rows, 6 questions, no empty how printed).
- `node tools/instruments/test_prices_hub.js`: **91 passed**.
- `node --check` buying.js, buying2.js, buying3.js: OK. `php -l inc/buying-hub.php`: no syntax errors.
- `python tools/instruments/shot_buying3.py` (headless Chrome, 390 x 844 and 1366 x 900, the saved live theme shell): **ALL PASS,
  98 checks**: no page errors, no sideways scroll, h3 inside chapters and h2 outside, one h1, the map (a jump marks nothing,
  reading marks, reload keeps), phone table cards, bpay (prefill, the design case, 15%, three errors with the field marked, the
  handover days), bsign, bkeys, breg, bmemo (high, then medium, nothing after reload), the glossary (count, quotes, clear), touch
  targets 48 px on the phone and 44 px on desktop, keyboard focus outline, every reload, the four print views, reduced motion,
  and a no-JS render (the five summaries, h3 in the HTML, the full glossary, 16 chip links).
- Regression: the Phase 1 and 2 browser checks (`shot_buying.py`, run from a copy with its output sent to a scratch folder so the
  old evidence was not overwritten): **ALL PASS** with the edited buying.js and buying2.js.
- `python tools/instruments/shot_buying3.py v3` on the content team's `page-9-v3.html` (draft of 04:04, 9.11.2026): 15 tools
  mount, 18 chapters wired, 69-term glossary filters, no sideways scroll, touch targets pass, no page errors. **One content
  finding**: `bhelp` (chapter 1), `bsell` (chapter 2) and `bdates` (chapter 14) sit inside chapters without `h="3"`, so they print
  an h2 under the chapter's h2. Adding `h="3"` to those three shortcodes fixes it (bwho already got it in a newer draft).

## Screenshots

`docs/research/2026-11-08-buying-guide-re/shots-tools/`:
390 and 1366 each: `-00-top`, `-01-map`, `-02-chapter13`, `-03-bpay`, `-04-bpay-error`, `-05-bsign`, `-06-bkeys`, `-07-breg`,
`-08-bmemo`, `-09-glossary-filtered`, `-10-print-bpay`, `-11-chapter11`; `390-nojs-bpay-summary.png`; and from the v3 draft
`v3-390-map`, `v3-1366-map`, `v3-390-chapter-first`, `v3-1366-chapter-first`, `v3-390-glossary`, `v3-1366-glossary`
(31 files in all).

## How to rerun

```
python tools/instruments/build_buying3_harness.py
python tools/instruments/shot_buying3.py
python tools/instruments/build_buying3_harness.py docs/research/2026-11-08-buying-guide-re/page-9-v3.html v3
python tools/instruments/shot_buying3.py v3
```

## Not done, or still unknown

- Not released and not checked on the live site: the harness uses the live page shell saved on 8.11.2026, so a theme change after
  that date is not covered. At release, check the rendered page 9 at 390 and 1366 again.
- Tested in Chromium only (headless Chrome); not in Safari or Firefox. `:has()` is used only for the green tint of a ticked row.
- Print was checked through the print view the page builds (and a print-media screenshot), not by saving a real PDF file.
- bkeys: the official wording and the page for each transfer (electricity, arnona, water, gas, house committee) are still
  empty; nothing in buying.json was verified for them, so nothing is shown until the content team fills `keys.transfers[].how`
  and `src`.
- The design README lists a seventh item, "bgloss". It was built as the glossary enhancer on the server-rendered `dl` (as this
  task asked), not as a separate shortcode.
- Linear HAD-686 and the Notion row were not updated from here (local build only); the calling session owns them.
