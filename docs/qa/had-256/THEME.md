# HAD-256 · theme integration (open item 4)

Snapshot 3 (`2ce0a741`) inside the site's real theme and real plugin, on a new bench **127.0.0.1:9405** (loopback only;
9401-9404 untouched). A fix candidate (`e28df264`, owner-wizard 2.0.1, not in snapshot 3) ran on **127.0.0.1:9406**.
Raw rows: `results.json` (id `T4`, variants `theme` and `theme-candidate-2.0.1`), probes `theme/theme-probe.json` and
`theme/candidate-2.0.1/theme-probe.json`. Evidence class: code (DOM + computed styles in a real headless Chrome) and eyes
(the screenshots below were looked at). Not a live check: the live site was only read anonymously.

| | |
|---|---|
| Start | `node scripts/had-256/local/start.mjs theme 2ce0a741 9405` (`theme e28df264 9406` for the candidate) |
| Run | `cd scripts/had-256/tests && python test_theme.py` (`NLJ_THEME_PORT=9406 NLJ_THEME_TAG=candidate-2.0.1` for the candidate) |
| Lives in | `scripts/had-256/local/.runtime/theme-<commit>/` (`snapshot/` = git-archive copy, `site/` = its own WordPress + SQLite) |

## What the bench is, and how close to live

| Part | Source on the bench | Same as live? |
|---|---|---|
| Parent theme NadLan Revenue 1.1.0 | repo root at the commit (style.css, style.min.css, functions.php, theme.json, templates, parts, patterns, styles, assets) | `style.css`, `nadlan-premium-sitewide.css`, `nadlan-premium-revenue.css`, `nlpc-header-parent-override.css`: **byte-identical** to the live public files (5.10). PHP and templates: repo (live PHP is not readable without credentials). |
| Child theme NadLan Platform Child 0.1.6 | `themes/nadlan-platform-child` | `platform.css` **differs** in the repo (13,826 B vs live 12,148 B: radius 2px vs 6px, weights, ellipsis rules): the bench uses the **live bytes** (`theme/live-ref/platform.css`). |
| nadlan-config (all modules) | repo at the commit (= 6e9cf930 for everything but the two snippets) | `nlds.css` byte-identical. Version string 1.72.372 vs live 1.72.429: runner hunks applied on the live text only (e.g. 1.72.427 prints the theme base stylesheet once; the bench prints style.min.css and style.css, cascade-neutral per perf_427.py). |
| Code Snippets | x-skin-a 638 = the live read of 2.10 (`docs/qa/v8-traffic/`); x-broker-drop, x-broker-join 699, x-owner-wizard 707 from the commit (LF; the QA-SNAPSHOT-3 hashes), run at `plugins_loaded` priority 1 as Code Snippets runs them | skin-a.css byte-identical; option `nadlan_skin_a = all` (the live page has `nl-skin-a`). |
| Page /post-listing/ | `scripts/broker-drop/pages/post-listing-he.html` (the text deploydrop.py wrote to page 4958: H1 + paragraph + shortcode block) | Rendered structure matches the live HTML of 5.10: `header#nlhp-top` (sticky, 57 px), `main.nlpc-main.nlpc-page-main`, one H1, `footer.nlpc-site-footer`, `#nlcta`, `#nla11y`, the plugin's "איך זה עובד" box for visitors. |
| Language | `he_IL` locale filter + RTL direction (no language pack downloaded) | `<html dir="rtl" lang="he-IL">` as live; core strings (skip link) stay English. |
| Not on the bench | WooCommerce, Paid Member Subscriptions, Yoast, Site Kit, LiteSpeed, the Hotjar loader (third-party, not in the repo) | their CSS (wc-blocks-rtl.css, pms css) and body classes are absent; Yoast's robots/title are absent. |

## Results, snapshot 3 (2ce0a741), 13 screens x 4 widths (320, 390, 412, 1440) x he/en

| Check | Result |
|---|---|
| Exactly one visible H1 on every screen | **pass** 104/104 (the page's `פרסום נכס למכירה או להשכרה, בחינם`; the app uses H2) |
| Site header, footer, floating bar `#nlcta`, accessibility button `#nla11y-btn` on every screen | **pass** 104/104 (bar and button never overlap each other) |
| No horizontal overflow, 44 px targets, visible focus ring, no JS error | **pass** 8/8 runs |
| App text contrast 4.5:1 (3:1 large) on computed colours | **pass** (361-469 text nodes per run, none under) |
| Page text around the app (H1, paragraph, "how it works" box) 4.5:1 | **pass** 8/8; site header and footer text: none under either |
| Forward focus (Tab, 13 screens, settled smooth scroll): no control's own box under `#nlcta`, `#nla11y-btn` or the header, centre visible, inside the viewport | **pass** on every run (info: the long consent labels of `#j-phone-ok` / `#j-owner-ok` reach under the bar at 320-412 while the checkbox itself is clear, 2-4 per run, mostly English) |
| **Backward focus (Shift+Tab): no control under the sticky header** | **FAIL on all 8 runs** (2 × 8 runs, the second after the probe was refined: the same result): 7-16 controls per run end with their centre under `.nlhp-top`, e.g. `#j-price`, `#j-rooms`, `מכירה` / `השכרה`, `פרסום המודעה` (320 he), `מודעה חדשה`, `הסרה מהאתר` |

Why: the app sets `html:has(#nlj-app){scroll-padding-top:24px}`, written on the bench theme whose header does not stick.
The live header (`.nlhp-top`, sticky, 57 px) covers the top 57 px, so a control the page scrolls UP to lands under it
(WCAG 2.4.11). The site's own pages with a sticky header use 77 px (`conversion-cta.php`, world pages).

## The fix candidate (e28df264, owner-wizard 2.0.1; snapshot 3 untouched)

`--nlj-head-room` = the measured bottom of a sticky/fixed site header + 16 px (24 px without one) as `scroll-padding-top`,
and `clearBar()` also scrolls a control that is left partly under the header. 19 lines in owner-wizard.php, nothing else.
Same suite on 127.0.0.1:9406 (13 screens x 4 widths x he/en, 2,448 focus events forward and backward): **32/32 pass**:
one H1, header, footer, bar and accessibility button on every screen; no control's box under the bar, the accessibility
button or the sticky header in either direction, no centre covered, none outside the viewport; no overflow, 44 px,
focus ring, no JS error, contrast as before. Info only: the consent labels as above (0-4 per run). Snapshot 3 on 9405 in
the same hour: the header check fails on all 8 runs, everything else passes. Candidate screenshots: first screens only
(`theme/candidate-2.0.1/<lang>-<width>/NN-<screen>-view.jpg`; the full pages were dropped to keep the repo light, the
change does not alter any layout). Bind proof for both benches: `bind-check-theme-9405-9406.txt` (127.0.0.1 only, the
LAN address refused; 9401-9404 still on their own PIDs).

## Seen on the screenshots (eyes), for Maya and Ben (not code defects of the app)

1. **?lang=en sits inside a Hebrew page**: the page H1, the paragraph and the plugin's "איך זה עובד" box stay Hebrew,
   `<html lang="he-IL" dir="rtl">`; only the app is English (`en-390/01-auth-signup-view.jpg`). Choices: an English
   wrapper filtered by the snippet for `lang=en`, a separate English page, or no public link to `?lang=en` yet.
2. **Copy that promises more than 2.0 does**: the page paragraph (page 4958) and the plugin's "how it works" step 3 say
   the listing goes up "עם כפתורי וואטסאפ וחיוג אליכם"; in 2.0 the number is published only when the owner ticks the
   consent box (unchecked by default). Iron law 3 (honesty): reword, e.g. "ואם תרצו, עם כפתורי וואטסאפ וחיוג אליכם".
3. **Two "how it works" boxes for a visitor**: the app's own "מה קורה אחר כך" (beside the form at 1440) and the
   plugin's "איך זה עובד" under it (`inc/property-wizard.php`, logged-out only). One should go.
4. **Phones, first screen**: the page H1 + a 5-line paragraph + the app's kicker, H2 and lead push the form down; at
   390x844 the first field sits right under the floating bar and the accessibility button at rest
   (`he-390/01-auth-signup-view.jpg`; a focus scrolls it clear). Two intros say the same thing; one should go
   (Maya's design call).
5. The page H1 and intro stay above every later step (details, photos, published, My listings), e.g.
   `he-1440/10-published.jpg`.
6. The error summary "יש 9 פרטים לתיקון" stays until the next "continue" even when every field is filled
   (`he-390/07-details-filled-view.jpg`); the same on the earlier bench (product behaviour, not the theme).
7. Site-wide, outside HAD-256: the `nl-legal` note under the footer is light grey on cream (not measured here).

## Screenshots

`theme/he-390/`, `theme/he-1440/`, `theme/en-390/`, `theme/en-1440/`: for each of the 13 screens a full page
(`NN-<screen>.jpg`; the fixed bar is drawn where it sits on the first screen) and the first screen as seen
(`NN-<screen>-view.jpg`). Candidate: `theme/candidate-2.0.1/<lang>-<width>/` (first screens). A view taken right after
a full-page shot can show the sticky header a few pixels down: Playwright resizes the window for the full page, the app's
resize handler scrolls the focused control clear, and the shot catches the smooth scroll (seen on both commits).
