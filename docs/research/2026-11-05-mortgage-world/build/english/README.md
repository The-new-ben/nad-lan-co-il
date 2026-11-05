# English twin of /mortgage-calculator/ (HAD-675), build folder

Built locally on 5.11.2026. **Nothing was deployed, nothing was written to the site, nothing was committed.** The site was only read
(GET), while release 1.72.588 was live (health 1.72.588). Decisions come from `../../keywords.md` section 9.

| File | What it is |
|---|---|
| `mquick.js` | the quick calculator, Hebrew byte-identical, English when its section says `lang="en"` |
| `mortgage-market.php` | the market block, Hebrew byte-identical, `nadlan_mm_render( 'en' )`, English Dataset, `nadlan_mm_quick_summary( 'en' )` |
| `page-en.html` | the WordPress page body (built by `write_en_page.py --build` from `boi-mortgage.json`) |
| `seo.json` | title (H1), slug, parent, Yoast title and description, the mquick `en` registry block, owned intents |
| `write_en_page.py` | `--build` (local), `--dry` (GET only, tested), no flag = create the DRAFT, `--publish` (after review and release) |
| `harness.php` | WordPress-free renderer of `mortgage-market.php` (both languages) and of the page |
| `render-en.html` | the harness output: the page body with the English market block, the English summary and the Dataset JSON-LD |
| `shot-en-phone.png`, `shot-en-desktop.png` | headless Chrome screenshots of `render-en.html` with the real `core.js` + this `mquick.js` running (phone column 358 px; desktop 1280 px) |

## 1. The recipe of the English twins (found in the repo and confirmed on the live site)

- **Scripts:** `docs/tools/asbestos/create_pages.py` (created /en/asbestos/, post 8761, `published-en.json`), `docs/tools/hazards/create_page.py`
  (/en/environmental-hazards/, 8769), `docs/tools/asbestos/update_pages.py` (content updates with a backup and a restore on failure).
  REST helpers: the top of `scripts/skin-a/deployskin.py` up to the health GET (app password, decrypted inside the runner, never printed).
- **REST call:** `POST /wp-json/wp/v2/pages` with `title` (it becomes the H1: the theme prints `<h1 class="nlds-pagehead__title">`; the
  content has no `<h1>`), `slug`, `status`, `content`, `parent`, and `meta: {_yoast_wpseo_title, _yoast_wpseo_metadesc}`.
- **Parent:** the published root page with slug `en` and parent 0, resolved at run time (`GET /wp/v2/pages?slug=en&parent=0`); id **5011**
  on 5.11.2026. 8761 and 8769 both have parent 5011.
- **Language:** no meta needed. `inc/page-lang.php` `nadlan_pglang_lang()` takes the language from the top ancestor's slug (`en`) and
  prints `<html lang="en" dir="ltr">`; `_nadlan_page_lang` exists only for English text on a root path (post 4962) and stays empty on
  8761. The tools follow it: `inc/instruments.php` `nadlan_nli_tool_lang()` gives `en` only on an /en/ page AND only for a tool whose
  registry entry has an `en` block; the shortcode then prints `<section class="nli" dir="ltr" lang="en">` and `core.js` `langOf()` reads it.
- **hreflang:** `inc/page-lang.php` `nadlan_pglang_family()`: the family key is the page path minus the language prefix, so
  `mortgage-calculator` (page 121, root) and `en/mortgage-calculator` pair automatically; `wp_head` prints `hreflang="he"`, `"en"` and
  `x-default` (the Hebrew URL) on both, but only when both are **published** (a draft is not in the family). Live proof:
  /asbestos/ and /en/asbestos/ print exactly that trio. The family is cached 12 h in the transient `nlpglang_fam_<md5(path)>`; saving
  either page clears it (`save_post_page`). The Hebrew page's HTML cache may lag until it is purged.
- **FAQPage:** `inc/instruments.php` `nadlan_nli_faq()` reads `<h2>Frequently asked questions</h2>` and the `<h3>` + `<p>` pairs up to
  the next `<h2>`; one FAQPage per page (live /en/asbestos/: 1 FAQPage, 13 questions).
- **Language pass:** `inc/lang-pages.php` never touches `.entry-content` on English guide pages, so the Hebrew terms in the body stay.
- **Breadcrumb:** `[nadlan_crumbs]` (inc/breadcrumbs.php) is Hebrew only (`בית`, `dir="rtl"`), so the English page does not use it
  (the asbestos twin does not either).

## 2. What changed in the two components

Both copies start from the repo files, which match live 1.72.588 for `mquick.js` (MD5 3092772d16a8c0aa5bc602724ab336c8 = the live
file). The live `mortgage-market.php` cannot be read over HTTP: diff it against the live file before the release (memory: the repo is
not always the live file).

**mquick.js** (MD5 dca80be72d20e4aca84c8eb8a4168cce): `EN = NI.langOf(root) === 'en'`. In English: every label, the result lines, the
LTV note, the source line (linking the Bank of Israel English page `by_bank.src.page_en`), the copy text and its button; the shekel sign
before the number and numbers `en-US` (`₪5,428`); months in English; bank chips from `by_bank.banks[].en` ("All banks" for the system
row); `<div class="nlmq" dir="ltr" lang="en">`; the two buttons point at the English page's anchors (`#amortization-schedule`,
`#mortgage-market`), because the full tool and the bank-offer check are not on it. One extra style block `#nlmq-css-en` (Plex Sans
first, the input aligned left) is added only in English. The Hebrew branch builds the same strings as before.

**mortgage-market.php** (MD5 9a84ee1976e8b71ab1971e64f1573921): only 3 original lines changed: `nadlan_mm_quick_summary( $lang = 'he' )`,
the style literal moved unchanged into `nadlan_mm_css()`, and the shortcode now takes `lang` (`[nadlan_mortgage_market lang="en"]`, or
any /en/ page). New: `nadlan_mm_render_en()` (same data, math and order; LTR; `₪` before numbers; English bank and city names;
quarters as `Q1 2026`; English sources line), `nadlan_mm_city_en()` (24 cities + "All of Israel"; an unknown city stays in Hebrew
inside `lang="he"`), `nadlan_mm_quarter_en()`, and an English Dataset JSON-LD (`inLanguage: en`) when the page holds
`[nadlan_mortgage_market lang="en"]` or is an /en/ page. The Hebrew path is otherwise untouched.

**Also needed in the release: two hunks on the LIVE `inc/instruments.php`** (I did not touch plugins/). Without them the English page
shows the quick calculator in Hebrew; `write_en_page.py --publish` checks for that and refuses.

```php
// 1. the mquick registry entry (repo line 317): add after 'data' => array( 'boi-mortgage.json' ),
				'en' => array(
					'name' => 'Quick mortgage calculator', 'kicker' => 'Calculator · Mortgage',
					'desc' => 'A quick Israeli mortgage calculator: the first monthly payment, the total repaid and the interest by mortgage amount, by home price and equity, or by the monthly payment that suits you, over 15 to 30 years, at the average track mix and rates of all banks or of one bank, from the latest Bank of Israel data.',
				),
// 2. first line inside nadlan_nli_summary_en( $id ) (repo line 1124):
		if ( 'mquick' === $id ) { return function_exists( 'nadlan_mm_quick_summary' ) ? nadlan_mm_quick_summary( 'en' ) : ''; }
```

**The full calculator `[nadlan_tool id="mortgage"]` is NOT mounted on the English page:** `tools/mortgage.js` says "Hebrew only (RTL)"
in its header, never calls `langOf`, holds 178 Hebrew lines, and its registry entry has no `en` block. The page links to the Hebrew
page for it instead.

## 3. The page

- **H1 (page title):** Israeli Mortgage Calculator: Monthly Payment, Track Mix and Amortization ("Israeli" in the H1 and "Israel" in the
  title cover both spellings Google groups; keywords.md section 9 proposed "Israeli" for the H1).
- **Yoast title (58):** Israel Mortgage Calculator 2026: Payments, Rates, Schedule ("Rates" instead of keywords.md's "Tracks", for
  "israel mortgage rates", 90 a month in Israel).
- **Description (154):** Israeli mortgage calculator in English: monthly payment in NIS at the latest Bank of Israel rates by bank and
  track, amortization schedule and 2026 rules.
- **Slug / parent / status:** `mortgage-calculator` under /en/ (5011), created as a draft.
- **Order (content first):** answer paragraph (56 words, ₪5,428 for September 2026) · a line on NIS and sources · CTAs (#quick,
  #mortgage-market, #amortization-schedule) · one line to the foreigners page with the exact anchor "Israel mortgage for foreigners" ·
  `[nadlan_tool id="mquick"]` · `[nadlan_mortgage_market lang="en"]` · how Israeli mortgages work (track table with rates and shares,
  CPI, prime and the Bank of Israel rate) · the three uniform baskets (computed first payments: ₪5,625 / ₪5,269 / ₪5,471) · Directive
  329 limits (table) with August 2026 borrower data · early repayment fees · olim and returning residents (citizenship and the
  single-home cap, disposable income, the eligibility loan and years since immigration, comparing offers, a Hebrew glossary) · yearly
  amortization schedule (25 rows; year 1: ₪65,140 paid, ₪42,215 interest; total interest ₪628,489) · four rules AI answers get wrong ·
  15 FAQ · sources and method · a link to the Hebrew page with the anchor "מחשבון משכנתא".
- **Facts:** only from `boi-mortgage.json` and `dna.md` section 6; the olim section uses no other source. Left out as unverified: 2026
  eligibility-loan amounts, prime-track margins by bank, anything about income earned abroad. One sentence states a convention
  not in those sources: "Israeli listings count the living room as a room, so 4 rooms usually means three bedrooms" (market block);
  remove it if Ben wants sources only.
- **Never targets foreigners:** no heading says foreigner or non-resident; two links to /israel-mortgage-non-residents/ with the exact anchor.
- **Look:** the NadLan Instruments system the Hebrew page already uses: ink #12202A, teal #2F6F86, rules #D3DCE2, red underline
  #C42550 only on the key number; IBM Plex Sans for text and IBM Plex Mono for figures (the Latin faces the English pages already load).
  Not the default look: no cream, no gold, no gradient, no Inter; it reads like a bank rate sheet.

## 4. Checks run

- `php -l` both PHP files: no errors. `node --check mquick.js`: OK. `python -m py_compile write_en_page.py`: OK.
- **Hebrew identity (code):** `harness.php render` on the original and the patched PHP, Hebrew page: section, Dataset and summary are
  byte-identical (MD5 d5e87d60…, 45c83d60…, 037176d6…). English with `lang="en"` and English by page language give the same bytes.
  The English section and Dataset hold no Hebrew letter.
- **mquick in a browser (code):** headless Chrome, the real `core.js`, served locally: the Hebrew DOM after mounting is identical for the
  original and the patched file, and so is a scripted run (30 years, one bank, price mode 2M with 400K equity, payment mode 7,500,
  back). English run: ₪5,428 / ₪4,931 / ₪4,778 (First International) / ₪7,645 with "Loan to value 80.0%: above 75% ..." / ₪1,569,754
  for a ₪7,500 payment; no Hebrew letter in the tool; `#nlmq-css-en` only in English.
- **Eyes:** `shot-en-phone.png`, `shot-en-desktop.png` (LTR, principal bar left, chips and tables readable). Not seen on the live site
  (nothing is live).
- **Page gates** (`write_en_page.py`): 17 OK (no h1, one mquick, no Hebrew full tool, one market shortcode, order, 40 to 60 word answer
  with the number, 15 FAQ pairs, exact anchor, no foreigner heading, no long dash, no spaced hyphen, no forbidden word, every #anchor has
  a target, title 58 with the head term first, description 154, H1 differs from the title, no straight double quote). About 3,500
  visible words.
- **`--dry` (GET only) on 5.11.2026 ~23:15:** /en/ root 5011; Hebrew twin 121 published at the root; slug free under 5011; no page or post
  with the same title; /israel-mortgage-non-residents/ 200; live 1.72.588; live mquick.js has no English yet (expected).

## 5. Release order (for the release engineer, each step on Ben's word)

1. Release `mquick.js` (to `assets/instruments/tools/`) and `mortgage-market.php` (to `inc/`), plus the two instruments.php hunks on
   the live file; lock line, `source_audit.py` before and after; check /mortgage-calculator/ is unchanged (Hebrew identity).
2. `python write_en_page.py --dry`, then `python write_en_page.py` (creates the draft, reads it back).
3. Ben reviews the draft in wp-admin. Then `python write_en_page.py --publish`: publishes, reads the live page (lang, one H1, the
   hreflang trio, mquick and the market block in English, English Dataset, one FAQPage with 15 questions, Yoast title) and moves it
   back to draft if any check fails. Then purge the cache of /mortgage-calculator/ so its new hreflang shows; resubmit the sitemap only
   (no indexing request).

## 6. Findings (not fixed here)

1. The Hebrew Dataset description and the file header say "25 ערים"; the data holds 24 cities plus the national row. The English text says
   "24 cities and nationwide". The Hebrew text stays as it is (byte-identical rule).
2. Keywords.md section 9: the foreigners page title still ends with "Calculator" and two English URLs would then aim at "israel mortgage
   calculator"; dropping that word, and pointing its "Mortgage calculator in Hebrew" links at the twin, needs Ben's word (no URL change).
3. On a phone the eight English bank names take five rows of chips, and "15 years" wraps in the term buttons; readable, but taller than
   the Hebrew tool. Shorter chip names would mean leaving the data file's `en` names.
4. The numbers in the page body are fixed at September 2026 (each dated); the market block and the tool update by themselves with each
   new data file. A later rebuild (`--build`) refreshes the body.
5. The English page has no visible breadcrumb or BreadcrumbList: `[nadlan_crumbs]` is Hebrew only.
