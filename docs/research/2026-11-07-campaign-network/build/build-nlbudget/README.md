# New instrument: "כמה עולה לשווק את הפרויקט" / What it costs to market your project (nlbudget)

HAD-678, 7.11.2026: the second instrument of the developer marketing page (after the campaign planner `nlcamp`). Built **locally only**:
nothing deployed, nothing committed, no live write, no existing repo file edited (`inc/instruments.php`, `nadlan-config.php`, `core.js`,
`core.css` untouched). Two new plugin files plus this folder. Design: `Budget.dc.html` of the campaign design canvas (inputs panel on the
right, three readouts, the line-item table with a source per row, the spend-by-stage bars).

## Files

| File | What |
|---|---|
| `plugins/nadlan-config/assets/instruments/tools/nlbudget.js` | **New.** The tool (id `nlbudget`), Hebrew and English in one file. Pure logic in `window.NLBUDGET` (runs in node, takes the data as an argument); the page part registers a `custom` NadLan Instruments tool and reads `data.nlbudget`. CSS scoped to `.nlbg` (style id `nlbg-css`). Sends nothing anywhere. |
| `plugins/nadlan-config/assets/instruments/data/nlbudget.json` | **New.** Every number the tool shows (33 figures, 17 budget lines). **Built, never hand-edited.** |
| `build-nlbudget/build_nlbudget_data.py` | Builds the data file from `teardown/pages.json`, `competitors/services.json`, `teardown/union.md` and `PLAN.md`. Refuses to write when a number is not found in its verbatim evidence string. |
| `build-nlbudget/test_nlbudget.js` | Node test, **84 assertions**. Last run: `test_nlbudget.out.txt`. |
| `build-nlbudget/test_nlbudget_summary.php` | PHP test of the snippet, **23 assertions**; writes `summary.he.html` / `summary.en.html` and pastes them into `preview.html`; `--summary he|en` prints one (read by the node test). Last run: `test_nlbudget_summary.out.txt`. |
| `build-nlbudget/preview.html` | Local mount exactly as the shortcode prints it (`section.nli` + `div.nli-host[data-nli=nlbudget][data-nli-data=...]`, kicker, title, server summary, related links). `?lang=en`, `?both=1` (the planner below, as on the hub), `?theme=1` (live theme stylesheets, read only). |
| `build-nlbudget/verify.py` | Playwright, Chrome (`channel="chrome"`, headless), 390x844 (mobile, touch) and 1280x900, he and en, plus a both-tools pass and a Hebrew phone pass under the live theme. Own `http.server` on a free 127.0.0.1 port, stopped in `finally`. **317 checks.** Last run: `verify.out.txt`, `verify.json`, `shots/` (33 images). |
| `build-nlbudget/registry.php.txt` | The `nadlan_nli_tools()` entry, the two summary branches, the summary function `nadlan_nlb_summary()`. `php -l` clean (PHP 8.3). |

Run from the repo root: `python .../build-nlbudget/build_nlbudget_data.py`, `node .../build-nlbudget/test_nlbudget.js`,
`php .../build-nlbudget/test_nlbudget_summary.php`, `python .../build-nlbudget/verify.py`.

## The data (nlbudget.json)

Each figure: value or range (`v` / `lo`, `hi`), `unit`, `currency` (ILS, USD, AUD or none), `scope` (il / abroad) and `country`, source name
(`src_he`, `src_en`), `url`, `date` (the page's own published / modified date from pages.json), `retrieved`, `flag` as union.md marks it
(cited, price list, agency claim, agency claim + unnamed source, example; plus own price and not published for NadLan's plans and our own
checks), `vat` where the source states it, and `ev`: the verbatim value string of the source record. Tested: every evidence string is found
verbatim in its file, every number of a figure appears in its evidence, and the Hebrew / English words of a figure hold no number its fields
do not. No currency conversion anywhere (the brief allows no FX source): US benchmarks stay in dollars, the Feasly example in A$.

## What it does

Inputs (right on desktop, first on phones): units for sale, average price, stage (4 pills), who sells (2 pills; the commission field appears
for a marketing company, **empty, no default**), share for buyers abroad (field + slider), sales period, leads per deal (**empty, no
default**; the hint shows the sources' own examples: 200 or 40, Semerenko; 48, Mirai). It opens on **Semerenko's own example** (60 apartments
x 2.4 million, tagged "דוגמה") and a 24-month window (the top of Semerenko's 12 to 24).

1. **Marketing-and-sales budget, whole project** (the one survey-red figure, underlined as in the design): developer's team = Start Point's
   2% to 4% (sales team and advertising included), both bounds named; marketing company = WE DO MEDIA's 1% (Israel) to Feasly's 2% (Australia,
   marketing only) plus the developer's own rate, marked partial until he enters it. Each bound shows its source, date and flag; the year
   line; "marketing alone about 1%, 0.75% online". On the example: 2,880,000 to 5,760,000 ₪; marketing alone 1,440,000 (the source said
   about 1.4 million). A panel lists all 7 published anchors on the project (Israel first, then Australia, the render studio, US builders).
2. **Advertising per apartment sold**: Start Point's 3,000 to 23,000 ₪ (claim, unnamed reports), times the units, as a share of the price.
3. **Leads**, only with the developer's leads per deal: deals x leads, split Israel / abroad by the share; their cost at three labelled bases:
   Start Point's exclusive lead price list (128 to 173 ₪, before VAT), Semerenko's campaign claim (300 to 800 ₪), LocaliQ's US search medians
   for buyers abroad ($102.51 to $142.59, in dollars).
- **The budget sheet**, 17 lines, each with range, stage and source + flag: renders (3-angle set 4,000 to 6,000; 3D sales plan 1,000 to 1,500
  per unit x units; film 12,000 to 30,000; Mabatim price list), the project page with a virtual tour ("כלול במנוי נדל״ן" + the link
  "המנויים: שוק אחד 36,000 ₪ לשנה, שלושה שווקים 72,000 ₪ לשנה, פרויקט דגל 144,000 ₪ לשנה"), paid online ads (about 0.75% of sales, WE DO
  MEDIA), and **11 lines with "לא פורסם מחיר ישראלי"** (research, branding, photography, site, CRM, outdoor and fence, print, radio/TV, PR and
  SEO, events abroad, sales office and model apartment) plus the sales team, each with a "המחיר שלכם" field that joins the total. Context under
  a line where a source exists: the Feasly example abroad, Globes' reported campaigns (2 to 5 million ₪), the 4 exhibitions that publish no
  exhibitor price, the broker fee (1% to 2% plus VAT). The selected stage marks its lines "בשלב שלכם". Total of the priced lines.
- **Spend by stage**: Feasly's worked example (A$530,000 of A$720,000 before launch = 74%, 26% after, +22% if the sale runs 12 more months),
  labelled "דוגמה מחו״ל"; the stage bar follows the stage; Pixel Nadlan's Israeli stage durations (weeks, claim) under it.
- **Context line**: the 2025 ad spend of Aura, Tidhar, Israel Canada, Hagag and Dimri (Globes from Ifat, list price), in the source's order.
- **Share**: copy as text and WhatsApp (wa.me, text only): inputs, the readouts with sources and flags, every line, the page address.
  State in memory only.

## Results (7.11.2026)

- **Data build**: 33 figures, every number found in its evidence (the check caught "one week" written in words: kept as text only).
- **Node 84 of 84**: provenance (verbatim evidence, numbers in evidence, no stray number in the words, dates = the pages' own dates), the
  figures against union.md, the example worked through (2,880,000 to 5,760,000; 1,440,000; company 1,440,000 to 2,880,000 partial, with 1.5%
  3,600,000 to 5,040,000; fee 2,160,000), leads and their cost, the sheet total 1,156,000 to 1,206,000 with 12 open lines, the stage
  marks, the spread 74 / 26 / +22, 800 random projects (no inverted range, the rounded total holds the exact one), validation, formatting,
  the shared text, **i18n parity (both languages, same placeholders, no unused string)**, no long dash, no tech word, no religion word, VAT
  wording only where a source states it, no ranking claim, token colours only, no gradient or shadow, survey once, and the server summary
  giving the same numbers.
- **PHP 23 of 23**: lint, the entry, both branches, both summaries (example total, anchors with source and flag, lead prices, render rows,
  the plans, the unpriced lines), no long dash, no outbound link, no data file = empty summary.
- **Browser 317 of 317** (he and en, 390 and 1280, both-tools, theme): every control pressed as listed in verify.py; on every view no
  horizontal scroll, every control at least 44 px, every input labelled, every group named, no long dash or tech word, survey red on the
  total only, every source line flagged; no console error or warning; nothing leaves 127.0.0.1 except Google fonts (wa.me and /marketing/
  stubbed, the live site aborted).
- **Looked at (eyes)**: he 390 and 1280, en 1280, theme he 390, he 1280 both-tools, he 390 company. Fixed after looking: in Hebrew the ₪ sat
  on the wrong side of the figures (it was inside the LTR isolate; now outside, after the number as Hebrew reads); the plans link broke into
  columns on phones (inline-flex; now a block); the source name repeated in the bounds; Hebrew sub-lines set in the mono face; the sheet was
  cramped beside the inputs on desktop (now full width below the inputs and readouts); "התקדמות" tripped the blacklist substring "דמו" (line
  renamed "צילום האתר לאורך הבנייה").

## Not done / open

1. **Release** (registry.php.txt): the entry, the two branches, the summary function inside the `nadlan_nli_tools` block; ship `nlbudget.js`
   and `nlbudget.json`. No module-list change. Then the shortcode `[nadlan_tool id="nlbudget"]` (with quotes) on the hub page.
2. **The hub page does not exist yet.** The plans link goes to `/marketing/` (he) and `/en/marketing/` (en), the slug decided in PLAN.md
   section 8 (`plans_href` in the data file); with the planner on the same page it scrolls to it instead. url_word_audit before minting.
3. **To confirm with Ben**: (a) sources are **named, not linked** (the research-stays-internal law; URLs stay in the data file); (b) VAT
   words appear only where a source states its terms (Start Point "before VAT", the broker fee "plus VAT"), never on NadLan's prices;
   (c) "תוכנית מכר בתלת ממד" is the price list's product name and the design's wording (language-dna restricts "תלת ממד" on buyer pages);
   (d) competitor and developer names on the page (Start Point, Semerenko, Mirai, WE DO MEDIA, Mabatim; Aura, Tidhar, Israel Canada, Hagag,
   Dimri in the ad-spend line); (e) the example defaults (Semerenko's 60 x 2.4 million, 24 months).
4. **Modelling choices, labelled on the page**: the paid-media line is a single "about" figure (0.75% of sales, WE DO MEDIA, the only
   Israeli anchor for it); the marketing-company upper bound is Feasly's 2% (Australia) because no Israeli marketing-only upper bound is
   published; the stage of each line is our placement from Pixel Nadlan's timeline and Semerenko's line list, not a sourced number; Feasly's
   "$" is shown as A$ (an Australian guide: feasly.com.au, GST, NSW law); the US lead benchmark is not converted to shekels.
5. **Gaps the tool states rather than fills**: no Israeli price for 11 lines, no Israeli commission rate, no Israeli spread by stage, no
   Israeli cost per lead for buyers abroad. Filling them needs new sourced data (data file first, then the tool).
6. Not pressed on the live site; no Linear issue or Notion row opened from this build (left to the coordinating session).

## Design

NadLan Instruments as is: ground #F6F8F9 (the inputs panel), surface #FFFFFF (cards, tables), ink #12202A / #3E4C58, mute #5E6A75, line
#D3DCE2, sea #2F6F86 (pressed pills, the stage marks, cited and price-list flags), sea-deep #1F4B5C (the current stage bar), survey #C42550
only as the underline of the total, open #4F9A5C for NadLan's own price flag; agency claims in a dashed outline. Faces: IBM Plex Sans Hebrew,
IBM Plex Mono for every figure (in `<bdi>`), Karantina only for the title (core.css); Latin Plex on English pages. Borders, no shadows, no
gradient, no emoji. Why it is not the default AI look: it reads as a cost estimator's sheet (steel-blue survey palette on form white, ruled
tables, mono figures, dashed outlines that mark an unproven claim, one red underline), not cream, gold or a purple gradient hero.
