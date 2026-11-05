# mready: "מוכנים לאישור עקרוני?" (HAD-675)

Panel 6 of the approved design board (`Tools.dc.html`) for https://nad-lan.co.il/mortgage-calculator/. Built locally on 5.11.2026.
**Not deployed, not committed, nothing written under `plugins/`.**

## What it does

Five questions: how the household earns (שכירים / עצמאים / שכיר ועצמאי), one or two borrowers, net income and existing loan payments,
where the equity comes from (חיסכון, עזרה מהמשפחה, ממכירת דירה, מענק, each an amount), and the home (דירה יחידה / חליפית / נוספת /
עולה חדש / תושב חוץ, מקבלן or יד שנייה, price, term). It opens filled with an example marked "דוגמה", and four ready cases fill
everything in one tap.

1. **The readiness card, "X מתוך 4"** (the one decisive number, red underline; failed limits in red, passed checks as a green
   fill marker only):
   - payment to disposable income (income less existing loan payments, the definition `mortgage.js` uses on the same page): up to
     40% passes, 40% to 50% passes with the capital note, above 50% fails (directive 329, `rules.pti_risk`, `rules.pti_max`);
   - LTV: the equity covers the down payment at the cap of the buyer type (75 / 70 / 50; oleh 75 and foreign resident 50 from
     `cost.json`);
   - equity against the down payment plus purchase tax (`ptax.json`, the oleh cap as in `afford.js`; a replacement buyer on
     single-home brackets) and the lawyer, 0.5% + VAT (`cost.json`);
   - the documents for the approval in principle: all core items ticked.
   The first payment uses the Bank of Israel all-banks average mix of the latest month (`boim.by_bank`, 1,000,000 over 25 years =
   5,428 a month in 9.2026, the same calibration as `mbudget`). The highest passing price at 40% and at 50% is
   `window.NLAF.compute` from `tools/afford.js`, fed with the disposable income and the equivalent rate.
2. **The personal documents list**, from `mready.json`: 43 sourced items, filtered by the answers, split into "לאישור העקרוני" and
   "למשכנתא עצמה, אחרי האישור", per-borrower words resolved (לכל אחד מהלווים / ללווה השכיר / ללווה העצמאי). Items stated by only
   one group (or by press only) carry the tag "יש בנקים שמבקשים". A checklist: ticks only, kept in the page and in `localStorage`
   (`nlmr:ticks:v1`, every access in try/catch); no income or amount is stored or sent. Copy as text, WhatsApp, print.
3. One plain link "לשלוח את התיק ליועץ" to https://nad-lan.co.il/mortgage-advisor/. No form.

## Files

| file | what |
|---|---|
| `mready.js` | the tool: pure logic on `window.NLMR` + the custom surface (`NadLanInstruments.register('mready', {custom})`) |
| `mready.json` | the documents (43), sources (25) with URL and UTC retrieval time, the approval facts, the rules snapshot, presets |
| `sources.md` | every document item with its sources and retrieval times, what each source says, what was read and left out |
| `test_mready.js` | node test: `node docs/research/2026-11-05-mortgage-world/build/mready/test_mready.js` (5,600+ checks, OK) |
| `preview.html` | mounts the tool like the shortcode; serve the repo root: `python -m http.server 47731 --bind 127.0.0.1` |
| `registry.php.txt` | the `nadlan_nli_tools()` entry |
| `summary.php.txt` | the `nadlan_nli_summary()` branch: crawlable Hebrew sentences built from `data/mready.json` (lint + run: OK) |
| `shots/` | 375 px: top, card (couple, foreign), documents; 1280 px: top, documents |

## Checked in the browser pane (eyes)

375 px and 1280 px, no horizontal scroll, no console errors. Pressed: the foreign residents ready case (2 מתוך 4, equity short by
₪74,880, the foreign list), a document tick (kept after reload, focus stays on the box), typing a new income (18,000: the payment
check fails at 54.3%, the "דוגמה" tag drops), the copy button (text verified). Print layout was not looked at.

## To ship (release session, Ben's word)

1. Copy `mready.js` to `plugins/nadlan-config/assets/instruments/tools/mready.js` and `mready.json` to `.../instruments/data/mready.json`.
2. Paste `registry.php.txt` into `nadlan_nli_tools()` and `summary.php.txt` into `nadlan_nli_summary()` (`inc/instruments.php`).
3. `data/boi-mortgage.json` must be the v2 file (by_bank, rules); with v1 the rate falls back to the fixed not linked average.
4. Place `[nadlan_tool id="mready"]` on /mortgage-calculator/ below the answer paragraph and the main calculator (content-first law).

## Research notes and limits

- Sources: Hapoalim (page + guide PDF), Leumi (page, collateral list, borrower guide PDF, the Bizportal interview made with Leumi
  Mortgages), Mizrahi-Tefahot (page + three PDFs + English Q&A), Discount (list PDF) and Mercantile (same group), FIBI (guide PDF),
  Bank of Jerusalem (guide PDF, March 2026), Kol Zchut (three pages), Bank of Israel (appendix 4 format, press release).
- `boi.org.il` blocks scripts (Radware bot check); its two documents were read with WebFetch.
- No bank publishes a gift letter in its list; two press sources do, so it carries the tag. Foreign-resident income papers rest on
  Mizrahi-Tefahot and the Leumi interview; tax papers and translation on Leumi only (tagged).
- The tool does not ask about other income (rent, alimony, allowances), broker fees, the appraiser or the bank file fee; the
  replacement buyer is shown on single-home brackets, which holds only when the previous home is sold in time.
