# New tool for /mortgage-calculator/: "כשקשה לשלם" (mkashe), the mortgage hardship tool

HAD-675, mortgage universe. Built 6.11.2026, **local only**: nothing deployed, nothing committed, no live write, no existing file edited
(`inc/instruments.php` untouched). Demand it answers (manual SERP 6.11.2026): אי החזר משכנתא, אי תשלום משכנתא ("מהן ההשלכות של אי
תשלום משכנתא?"), הקפאת משכנתא (לחצי שנה, ל־3 חודשים, ללא ריבית, השלכות, מילואים, מלחמה, שאגת הארי, עם כלביא, by bank), מחשבון הקפאת
משכנתא, דחיית תשלומי משכנתא, כינוס נכסים משכנתא, משכנתא עם תיק הוצאה לפועל, התנגדות לביצוע משכנתא.

## Files

| File | What |
|---|---|
| `plugins/nadlan-config/assets/instruments/tools/mkashe.js` | The tool (id `mkashe`), Hebrew only, RTL. Pure logic in `window.NLKS`. Labels only: every rule, number, program and source comes from the data file. |
| `plugins/nadlan-config/assets/instruments/data/kashe.json` | `"key": "kashe"`, `"checked": "2026-11-06"`, `"src"`; 27 sources (URL, short label, date and its kind, read date); `rules` (every number, each with its section); the timeline, bank lines, free help, rights, the ended outlines, the copy sentence, `unverified`. |
| `build-mkashe/registry.php.txt` | The exact PHP: the `nadlan_nli_tools()` entry and the `nadlan_nli_summary()` branch, plus the switcher chip and pane. `php -l` clean (PHP 8.3). |
| `build-mkashe/render_summary.php` | Renders the branch against the real data files with WordPress stubs; output `summary.out.html`. |
| `build-mkashe/test_mkashe.js` | Node test, **71 assertions**. Last run: `test_mkashe.out.txt`. |
| `build-mkashe/hand_spitzer.py` | The 50-digit decimal calculation the test literals come from. |
| `build-mkashe/preview.html` | Local mount exactly as the shortcode prints it, inside pane `#tool-kashe`, with the rendered server summary. `?theme=1` adds the live theme stylesheets (read only). |
| `build-mkashe/verify.py` | Playwright (Chrome, headless) at 390x844 `is_mobile` and 1280x900, plus a phone pass under the live theme; its own `http.server` on a free 127.0.0.1 port, stopped in `finally`. **134 checks.** Last run: `verify.out.txt`, `verify.json`, `shots/`. |
| `build-mkashe/sources/kz-*.txt` | The text of the 15 Kol Zchut pages as fetched (with their "עודכן לאחרונה" line). |

Run from the repo root: `node docs/research/2026-11-06-mortgage-universe/build/build-mkashe/test_mkashe.js`,
`php docs/research/2026-11-06-mortgage-universe/build/build-mkashe/render_summary.php`,
`python docs/research/2026-11-06-mortgage-universe/build/build-mkashe/verify.py`.

## Results (6.11.2026)

* Node: **71 of 71**. PHP: summary rendered, all 10 key numbers present, no long dash.
* Browser: **134 of 134** at 390 and 1280 and under the live theme: every month button (1 to 6) and every card pressed and checked
  against `NLKS`; payment mode and back; bad values; the four jump buttons; the date of the first missed payment; all six situations;
  both outlines "הסתיים"; copy (clipboard read back) and the case link (opened in a new page, the same case returns); the sources list.
  No console error or warning, no horizontal scroll, every visible control (buttons, inputs, tel links, the sources summary) at least
  44 px, every input labelled, every group named, no long dash and no banned word in the rendered text.
* Screenshots looked at (eyes): `calc-390`, `late-390` (cut in slices), `rights-all-390`, `war-390`, `page-default-1280`,
  `late-1280`, `rights-all-1280`, `page-theme-390`. Fixed after looking: Hebrew in the mono face (source chips, the step labels, the
  outline dates, "לא זז") fell back to a Courier-like font, now the text face; the "cheapest" tag pushed one card's rows down, now every
  card reserves the row; all Kol Zchut chips read "כל זכות · עודכן ..." alike, now they carry the page title; the bank list took about
  250 px a bank on a phone, now the numbers share a row; desktop timeline lines ran 1,050 px wide, now the bank and help lines sit beside
  it (340 px column) and the rights list is two columns; the date field no longer spans the whole width; a second `.nlks__cheap`
  (the outlines note) was renamed.

## Worked examples (hand-worked with 50-digit decimals; all in the test)

Monthly rate = annual / 1200; full deferral: B(1+i)^d over n - d months; interest only: B x i during, then B over n - d; extension:
B(1+i)^d over n months; "extra" = all payments to the end minus P0 x n. CPI unchanged.

| Case | Before | דחייה מלאה | ריבית בלבד | הארכת תקופה | Cheapest |
|---|---|---|---|---|---|
| 1,000,000 / 300 months / 4.62% / 3 months | 5,626.66 | after 5,722.51 (+95.86), extra 11,589.50; interest joined 11,594.52 | 3,850 during, after 5,656.92, extra 3,659.47 | after 5,691.89, extra 19,571.52, 3 months longer | ריבית בלבד |
| same, 6 months | 5,626.66 | 5,820.54, +23,240.79 | 5,687.88, +7,338.44 | 5,757.89, +39,369.96 | ריבית בלבד |
| same, 1 month | 5,626.66 | 5,658.37, +3,856.31 | 5,636.67, +1,217.66 | 5,648.32, +6,498.79 | ריבית בלבד |
| 600,000 / 180 / 5% / 2 months | 4,744.76 | 4,820.53, +3,997.00 | 4,780.61, +1,890.99 | 4,784.38, +7,131.97 | ריבית בלבד |
| 400,000 / 120 / 0% / 3 months | 3,333.33 | 3,418.80, +0 | 3,418.80, +0 | 3,333.33, +0 | none ("בריבית 0% אין עלות נוספת") |

Also: the rate solved back from 1,000,000 / 300 / 5,626.66 is 4.62%; first missed payment 10.5.2026 puts the 6-month line on
10.11.2026 (31.8 -> 28.2, 29.2 in 2028). The server summary prints the first row at the BoI rate of the data file (4.62%, 8.2026).

## What the tool does

1. **מחשבון הקפאת משכנתא**: balance, months left, the rate (opens on `boi-mortgage.json` `rates.fixed_nl`, the BoI average of new
   fixed not linked loans, 8.2026: 4.62%, labelled) or the payment (the rate is solved from it), 1 to 6 months. Three cards side by
   side (payment after, + a month, extra to the end), the cheapest named in one sentence, the full breakdown of the pressed card, and
   the s.9ח1 note (the bank sets the terms and must explain the costs in writing before signing).
2. **אם כבר לא שילמתם**: six ordered steps (day 0, the 21-business-day notice, the 6-month line, the execution-office warning, the
   receiver, the sale) each with "מה מגן עליכם" (open green), "מה אפשר לעשות" (sea) and a red note only where there is a caution (the
   notice exemption, the immediate-enforcement exceptions, the alternative-housing cost); an optional date of the first missed payment
   (kept in the page, not in the link); the bank lines (Mizrahi-Tefahot *8860, extension 4 then 3, and the existing-mortgage lines
   banks.json has for Leumi, Hapoalim, Discount, Jerusalem, Yahav); free help: שי״ל 118, *2310, the Legal Aid office, *35592.
3. **The rights checklist**: מילואים, פיטורים או מחלה, לידה, פטירה של לווה, הלוואת זכאות, גיל מבוגר, and the six rights of every
   borrower, each with its section or Kol Zchut page and date.
4. **מתווי מלחמה שהסתיימו**: שאגת הארי (outline 2.3.2026, extended 15.4.2026, applications until 15.5.2026) and עם כלביא (17.6.2025,
   1.7 to 31.7.2025); the status is computed from the last application day, so both read "הסתיים"; the one line "בכל מבצע חדש בנק
   ישראל מפרסם מתווה; בודקים מול הבנק."
5. **Copy and link**: the summary has the calculator numbers and the general rules only (no ticked situation, no date); the link is
   `#mkashe=` (base64url of balance, months, mode, rate or payment, months deferred, card), written only when asked; the page address
   is never changed. The not-legal-advice line, all 27 sources with dates, the check date.

## Sources used

* `gov/gov.md` sections 2 (s.9A1), 3(d), 4 and the unverified list; `gov/facts.json` topic 4-relief-and-arrears; the law texts
  re-read in `gov/raw/wikisource-*.html` (Banking (Service to Customer) Law 5א1, 9א1, 9ח1, 9ח2; Execution Law 38, 81ב1; Housing
  Loans Law 5א, 5ב); `gov/banks.json`.
* Kol Zchut (the `kolzchut/` folder had no pages.json or kolzchut.md): 15 pages fetched 6.11.2026 14:58 UTC with curl and a normal
  user agent (HTTP 200, no block): הארכה של שישה חודשים (עודכן 7.1.2026), מימוש על החוב שבפיגור בלבד (14.5.2026), המדריך לנוטלי
  משכנתא שנפתח נגדם תיק (10.5.2026), מכירה עצמית (10.5.2026), פירעון כשמונה כונס (14.5.2026), עיכוב ביצוע (14.5.2026), השהיית
  החלטה (13.5.2026), סידור מגורים חלופי (13.5.2026), ועדת חריגים and its appeal (10.4.2025), קשישים נזקקים (10.4.2025), מוקד *2310
  (2.3.2025), שי״ל (24.5.2026), ביטוח משכנתא (7.7.2026), the reservists guide (26.7.2026). Texts in `sources/`.

## Still unverified (kept off the page)

1. A cap on mortgage arrears interest: not in the law text read. 2. A BoI directive on borrowers in arrears: boi.org.il pages blocked.
3. The Swords of Iron outline terms, including what Kol Zchut writes about reservists then: secondary only per gov.md; the reservist
   right shows only Kol Zchut's line that no special arrangement was set in שאגת הארי. 4. A reservist advice-cost refund: no source.
5. Law sections were read in the Wikisource consolidated text, not Reshumot. 6. Bank lines: only Mizrahi-Tefahot publishes an
   arrears line; Mercantile, FIBI, Otsar Ha-Hayal, Massad (general numbers only) and One Zero (blocked) are not shown.
7. Kol Zchut says the bank brings a committee request within 30 days (procedure 08/29, not read); the page shows the law's 60 / 15 / 30.
8. Our reading of "הארכת תקופה": the loan grows by exactly the deferral months (the payment then rises by (1+i)^d); banks may instead
   keep the payment and extend further. The calculator states its three definitions on the page.

## Server summary (summary.out.html, rendered 6.11.2026)

"מחשבון הקפאת משכנתא, דוגמה: יתרה של 1,000,000 ₪ ל־300 חודשים בריבית 4.62% ... ההחזר היום 5,627 ₪. דחייה מלאה של 3 חודשים ...
אחר כך 5,723 ₪ ..." then seven rules as a list (6 months and arrears only, 21 business days, 20 / 90 days and 90 days after the receiver,
alternative housing and 18 months, the 2.5 million fee rule, 3 months up to 3 times and 12 months after death, the committee 60 / 15 /
30), the two outlines with "הסתיים" computed from today's date, and the not-legal-advice line with the check date.

## Release steps (not done)

1. Paste `registry.php.txt` parts (1) and (2) into `inc/instruments.php`; ship `tools/mkashe.js` and `data/kashe.json`.
2. Add the chip and pane `tool-kashe` to the page switcher (markup in the snippet header). Where the chip goes and its wording on the
   live page are the owner's call.
3. After release: source audit of the raw HTML, content_first_check, and the press-through in the owner's Chrome.

## Design

The instruments palette: ink #12202A, ink-2 #3E4C58, mute #5E6A75, line #D3DCE2, sea #2F6F86, sea-deep #1F4B5C, ground #F6F8F9;
open green #4F9A5C only for protections, survey red #C42550 only for cautions and errors. IBM Plex Sans Hebrew for text, IBM Plex
Mono for numbers and inputs only. Why not the default look: the surface is a court-and-bank record read step by step, a ruled
timeline with numbered square markers, each line stamped with its law section or page and date, hard 2 px rules between parts; no
cream, gold, amber, gradient, emoji or soft card. CSS id-scoped (`#nlks`) with `!important` where the theme restyles plain elements.
