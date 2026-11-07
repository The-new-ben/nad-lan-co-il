# New instrument: "מתכנן הקמפיין" / Campaign planner (nlcamp)

Ben, 7.11.2026: an app-like page where a property developer builds a campaign to sell a project to buyers abroad and in the
diaspora, sees the plan and the price, and pays an annual subscription before launch. Built 7.11.2026, **local only**: nothing
deployed, nothing committed, no live write, no existing repo file edited (`inc/instruments.php`, `nadlan-config.php`, `core.js`,
`core.css`, `advertiser-*.php`, `conversion-cta.php` untouched). Two new plugin files plus this folder.

## Files

| File | What |
|---|---|
| `plugins/nadlan-config/assets/instruments/tools/nlcamp.js` | **New.** The tool (id `nlcamp`), Hebrew and English in one file. Pure logic in `window.NLCAMP` (runs in node); the page part registers a `custom` NadLan Instruments tool. CSS scoped to `.nlcp` (style id `nlcp-css`). |
| `plugins/nadlan-config/inc/campaign-brief.php` | **New server file.** `POST /wp-json/nadlan/v1/campaign-brief`, the private post type `nadlan_camp_brief`, the admin mail, `window.NLCAMP_CONFIG`, the server summary, a `/health` line. See below. |
| `build-nlcamp/test_nlcamp.js` | Node test, **90 assertions**. Last run: `test_nlcamp.out.txt`. |
| `build-nlcamp/test_campaign_brief.php` | PHP test of the server file with small WordPress stubs, **66 assertions**; also `--json` (read by the node test) and `--summary he|en`. Last run: `test_campaign_brief.out.txt`. |
| `build-nlcamp/preview.html` | Local mount exactly as the shortcode prints it (`section.nli` + `div.nli-host[data-nli=nlcamp]`, kicker, title, the server summary, related links), Hebrew by default, `?lang=en` for the English page, `?stub=1` answers the brief locally for hand checks, `?theme=1` adds the live theme stylesheets (read only). |
| `build-nlcamp/summary.he.html`, `summary.en.html` | The server summary rendered by `test_campaign_brief.php --summary` (pasted into preview.html). |
| `build-nlcamp/verify.py` | Playwright, Chrome (`channel="chrome"`, headless) at 390x844 (mobile, touch) and 1280x900, Hebrew and English, plus a Hebrew phone pass under the live theme. Starts its own `http.server` on a free 127.0.0.1 port, stops it in `finally`. **529 checks.** Last run: `verify.out.txt`, `verify.json`, `shots/` (48 images). |
| `build-nlcamp/registry.php.txt` | The `nadlan_nli_tools()` entry, the two summary branches, the module-list line. `php -l` clean (PHP 8.3). |

Run from the repo root:
`node docs/research/2026-11-07-campaign-network/build/build-nlcamp/test_nlcamp.js`,
`php docs/research/2026-11-07-campaign-network/build/build-nlcamp/test_campaign_brief.php`,
`python docs/research/2026-11-07-campaign-network/build/build-nlcamp/verify.py`.

## What it does

Mobile first, 5 steps, a 5-segment progress bar with "n / 5", Back / Next, every control at least 44 px. Language: a `data-lang`
attribute on the host or a wrapper, else the nearest `lang` (the shortcode prints it on the section). "he" is Hebrew and RTL; any other
language gets English and LTR.

1. **Markets and communities**: 10 chips (France, USA, UK, Canada, Belgium, Switzerland, South Africa, Australia, Russian speakers,
   Olim in Israel), each showing its languages (EN, FR, RU); live readout of the campaign languages and the plan that fits. The line
   "הפרסום מכוון לפי מדינה, עיר ושפה, ובעיתונות ובניוזלטרים של הקהילות" (coordinator 7.11: Meta and Google forbid religion or
   ethnicity targeting, housing ads are a special category). No word of religion anywhere (tested).
2. **Buyers**: one of four cards (aliyah or holidays, investors, parents of children in Israel, luxury).
3. **Monthly ad budget**: 3,000 to 60,000 in steps of 1,000, typed, -/+ (disabled at the ends) or a slider; the monthly and the
   **yearly total** (the only survey-red figure on the tool, tested on every view); "paid by you straight to the channels, not part of the
   plan price"; the suggested split Meta 55 / Google 25 / community press and newsletters 15 / international portals 5 as a bar and a
   list with amounts, labelled a starting point, changeable in 5-point steps (must sum to 100) with a reset. **No reach, lead or
   cost-per-lead number.** The hook is `NLCAMP.benchmarks = null`.
4. **The project**: new (we build the page and the virtual tour from plans and specs; name optional) or an existing nad-lan page
   (address or name required).
5. **Summary and plan**: a definition list with a "שינוי" button on every row (back to that step, state kept); the recommended plan
   preselected by the number of markets (1 One market 36,000; 2-3 Three markets 72,000; 4+ Flagship 144,000, "₪ לשנה" / "₪ a year",
   no VAT wording); the developer can switch, but a plan smaller than the markets chosen is refused with a plain message; the lead
   line "כל פנייה מגיעה אליכם בוואטסאפ, עם מה שהקונה פתח בפרויקט" (the wrong-number replacement was removed on the coordinator's
   correction: no guarantee); contact fields (name, company, phone, email), a privacy notice (purpose, no legal duty, not passed on,
   link to the privacy page) and a consent box; copy the summary and WhatsApp (wa.me with text only; the shared text never carries the
   contact details). **Send saves the brief first**; only a saved brief shows the reference (NLC-yymmdd-XXXX) and the payment step:
   a button to the WooCommerce product of the plan (`NLCAMP.plans[k].productUrl`, `&nlc_ref=<reference>` appended) or, while null,
   "קישור לתשלום יישלח אליכם עוד היום" / "A payment link will be sent to you today". No card data is ever asked. A server error keeps the
   form and says so. The state lives in memory only (no address hash, no browser storage).
   **First-payment mode** (coordinator 7.11: Morning's terminal takes one charge of up to about 20,000; 20,000 passes, 25,000 is refused):
   when `NLCAMP.plans[k].firstPay` is set (the server sends 18,000), the button reads "לתשלום ראשון: ₪18,000 (שלושה שווקים, ₪72,000
   לשנה)" / "Pay the first part: ₪18,000 (Three markets, ₪72,000 a year)" and the line under it "את היתרה, ₪54,000, משלמים בתשלומים של
   עד ₪18,000, בקישורים שנשלחים אליכם." / "The rest, ₪54,000, is paid in parts of up to ₪18,000 through links we send you." Figures
   in `<bdi>`; the part amount is filled from firstPay (so it follows the option), written "₪18,000" like every figure of the tool.
   Without firstPay the full-price button stays ("לתשלום: שלושה שווקים, ₪72,000 לשנה").

## Server file (new): `inc/campaign-brief.php`

No existing route fits: `advertiser-orders.php` and `advertiser-center.php` have no public route for a brief (WooCommerce hooks and
the admin `/lead/status` only), and the public `/lead` route files a **buyer** lead that starts the lead routing and the buyer nurture
mails (lead-e2e, lead-nurture), wrong for a developer's order. Payment stays the shop's own WooCommerce + Morning checkout; this file
only stores the brief and prints the product links ("not a fifth payment system").
- `POST /wp-json/nadlan/v1/campaign-brief`: every field checked again (allow lists, budget range and step, split of 4 shares in 5s
  summing to 100, plan against the market count, contact, consent === true); languages, yearly budget and price computed on the server
  (browser values ignored); saved as a **private** `nadlan_camp_brief` post (not public, not queryable, not in REST, no URL, not in
  search; listed under Projects in wp-admin with a read-only box), meta `_nlc_ref`, `_nlc_status` = new, `_nlc_brief` (JSON),
  `_nlc_consent_at`; mailed to the site admin with the payment state (first payment of 18,000 on product 882x and the rest to send in
  links of up to 18,000; or the full payment; or "send a payment link today" when there is no product); answered 201
  `{ok, ref, plan, price}`.
- Guards without a nonce (cached pages make a nonce go stale): honeypot, at least 2 s to fill, Origin must be the site (www allowed),
  body up to 8 KB, 5 briefs an hour per visitor (the site's `nadlan_hardening_client_key`), 60 a day for the site.
- `window.NLCAMP_CONFIG` printed before `nlcamp.js` only on pages with the tool: the REST address, the privacy page, and per plan
  `productUrl` (checkout `?add-to-cart=<id>`) and `firstPay`. Products (hidden in the shop, 7.11): full plans 8809 / 8810 / 8811 (36,000 /
  72,000 / 144,000), first payments of 18,000: 8822 / 8823 / 8824. The options `nadlan_cb_product_one/_three/_flag` are read first; when
  unset the code uses 8822 / 8823 / 8824, so **the release needs no option write**; an option set to 0 means no product. The option
  `nadlan_cb_first_amount` (int, default 18,000 when unset or empty; 0 = the full plan in one charge) becomes `firstPay` of every plan
  it is below (null otherwise). When Morning raises the cap: set the first amount to 0 and the three product options to 8809 / 8810 / 8811.
- `nadlan_cb_summary( 'he' | 'en' )`: the plain summary the shortcode prints before the script (all markets, languages, the targeting
  line, the three prices a year, the budget range paid directly, payment before launch).
- `/health`: `campaign_brief` version (1.1.0), the three product ids and the first amount.

## Results (7.11.2026)

- **Node 90 of 90**: plan recommendation 0..10, covers, languages implied, budget range/step/clamp/-+, yearly totals, the split (290
  cases add up to the budget in whole shekels), validation per step and in screen order, the payload keys (exactly what PHP reads, no
  card field, a copy), the shared text (no contact details, the reference only after saving, RLM marks keep "Meta 55%" together in
  Hebrew WhatsApp text), the payment link (javascript:, http: and quotes refused), `NLCAMP_CONFIG`, **i18n: every he key has an en key
  and back (139 keys, same placeholders)**, no long dash, no tech word, no VAT, no religion word, only token colours, no gradient or
  shadow, survey red once; the first-payment mode (rest 18,000 / 54,000 / 126,000; firstPay refused when 0, negative, not below the
  price, not whole, a string; the wording exactly as given); and the same offer as the PHP (prices, limits, names, markets, languages,
  budget, recommendation table, first amount 18,000 and products 8822 / 8823 / 8824 by default).
- **PHP 66 of 66**: the private type and the route; a good brief stored, mailed, answered; 24 refusals each naming its field; honeypot,
  too fast, foreign Origin, "null" Origin, 8 KB, bad JSON; nothing refused is stored; 5 an hour then 429, 60 a day then 429; a reference
  collision drawn again; the config: defaults (8822 / 8823 / 8824, firstPay 18,000), the full plans (first amount 0, 8809 / 8810 /
  8811), a product option 0 (no link), a first amount not below the price, an empty option; the mail in each payment state; the health
  line; both summaries; no long dash or VAT wording in any mail.
- **Browser 529 of 529** (he and en, 390 and 1280, plus the theme pass): every control pressed as listed in verify.py; on every view no
  horizontal scroll, every button, link button, summary, text input and card at least 44 px, every input labelled, every group named,
  no long dash, no tech word, no VAT wording, survey red only on the yearly total; focus on the step heading after each move; the server
  error then the save; the request is a JSON POST without cookies; nothing leaves 127.0.0.1 except Google fonts (wa.me stubbed);
  one console error per run, the deliberate 500 of the failure test (counted, required to be exactly one), nothing else. The pay step
  in all three server settings: first payment (the default: "לתשלום ראשון: ₪18,000 ..." to 8823, the rest line, the figures in `<bdi>`),
  full plan (to 8810, no rest line), no product (the same-day link line).
- **Looked at (eyes)**: `he-390-step1`, `he-390-step3-split`, `he-390-step5-errors`, `he-390-pay`, `en-1280-step3`, `he-1280-step5`,
  `theme-he-390-step5`. Fixed after looking: the pay button lost the spaces around the price (flex items; now one span); loose paragraph
  margins and an empty footer line on the saved view; "Meta 55%, Google 25%" reordered in Hebrew so 25% sat beside Meta (each item now
  isolated); the split panel had no open/close marker (a chevron now). After the first-payment change: `he-390-done` (the button wraps
  to two lines on the phone, reads right).

## Not done / open

1. **Payment**: payment works on the site again (Morning reconnected 7.11); the products exist (hidden) and the code defaults to the
   first-payment products, so the release sends developers to pay 18,000 at once. **The rest (18,000 / 54,000 / 126,000) is paid
   through links someone sends by hand**, as the button text and the admin mail say. `nlc_ref` rides on the checkout link but no hook
   writes it into the order yet (not written on purpose: no untested code on the checkout). Not pressed on the live checkout from here.
2. **Benchmarks**: `NLCAMP.benchmarks` stays null until there is a sourced reach / lead / cost per lead figure per market.
3. **Release steps** in `registry.php.txt`: the registry entry, the two summary branches, `'campaign-brief'` in the module list of the
   LIVE `nadlan-config.php` (the repo copy of that list is not the live one: it does not even name `instruments`), ship the two new files,
   the page `/international-campaigns/` + `/en/international-campaigns/` with `[nadlan_tool id="nlcamp"]` (url_word_audit first).
4. **To confirm with Ben**: the buyer descriptions and the plan descriptions (scope by market count only; no feature promises added);
   that a plan smaller than the markets chosen is refused (not just warned); the privacy page link `/privacy/` on English pages; the
   brief status flow (new, link sent, paid, live) is by hand for now; English related links are empty until an English B2B page exists.
5. Not tracked by me: no Linear issue or Notion row was opened from this build (left to the coordinating session).

## Design

NadLan Instruments as is: ground #F6F8F9, surface #FFFFFF, ink #12202A / #3E4C58, mute #5E6A75, line #D3DCE2, sea #2F6F86 (pressed chips,
the primary button, the pay button), sea-deep #1F4B5C (the current step), survey #C42550 on the yearly total only, data fills only for the
split (Meta sea, Google sea-deep, press plan-open #4F9A5C, portals plan-civic #8E7CC3). Faces: IBM Plex Sans Hebrew for the UI, IBM Plex
Mono for every figure (in `<bdi>`), Karantina only for the tool title (core.css: 44 px, 38 px on phones); on English pages the core's
Latin Plex (Plex Sans, Plex Sans Condensed title). Radius 2 px fields and buttons, 6 px cards, 999 px chips; borders, no shadows, no
gradient of ours, no emoji. Why it is not the default AI look: it reads as a media-buying order sheet (a survey-instrument palette of
steel blue on form-paper white, a ruled summary ledger, mono figures, one red total), not cream, gold or a purple gradient hero.
