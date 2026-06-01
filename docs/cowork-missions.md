# Cowork mission pack — nad-lan.co.il (2026-06-01)

> Detailed, self-contained, obstacle-proofed missions for Cowork (hands-on WP/browser/ChatGPT work) to run **in parallel** with Claude Code's coding. Paste each `PROMPT` block as one mission. They are grouped into waves by dependency. Every prompt states its own context, steps, obstacle-handling, deliverable, and stop conditions so Cowork needs no back-channel.
>
> Shared facts Cowork should know:
> - Site: https://nad-lan.co.il (WordPress, UPress host). Owner: Ben Bettesh (בן בטש), עו"ד, bar 29020. Sole phone **0525101555** (landline 036916454 is RETIRED — never use). info@nad-lan.co.il.
> - Plugin **nadlan-config** auto-updates via PUC: it reads `plugin-dist/nadlan-config.json` from the **main** branch of github.com/The-new-ben/nad-lan-co-il; WP Admin → Plugins shows "Update" → click it.
> - Current code lives on branch `claude/charming-meitner-mwVEW` → **PR #4**. Versions: GA4 fix (1.4.0), directory+claim+importer+auction (1.5.0), listing UX (1.6.0).
> - Healthcheck: `GET https://nad-lan.co.il/wp-json/nadlan/v1/healthcheck` (no auth) — reports version + module readiness.
> - Architecture reference in repo: `skills/listings-auction-directory-architecture.md`; open questions: `docs/listings-questions.md`.

---

## WAVE 1 — Deploy & verify (do first; everything else depends on it)

### Mission 1 — Merge PR #4, deploy plugin, smoke-test
```
PROMPT:
You are deploying and verifying a WordPress plugin update for nad-lan.co.il.

CONTEXT: Branch claude/charming-meitner-mwVEW (PR #4) contains nadlan-config v1.6.0 + a GA4 fix. The plugin auto-updates via PUC, which reads plugin-dist/nadlan-config.json from the MAIN branch. So nothing deploys until the branch is merged to main.

STEPS:
1. Open PR #4 on github.com/The-new-ben/nad-lan-co-il. Confirm it targets base=main. Review the file list (plugin code under plugins/nadlan-config/, plugin-dist/*.zip + json, docs/, skills/, 8 theme dash-fix patterns). Merge it to main.
2. In WP Admin → Plugins, look for "NadLan Config — update available". Click Update. (If no notice appears within ~1h, go to Dashboard → Updates → Check again, or deactivate/reactivate the plugin to force the PUC check.)
3. Verify: open https://nad-lan.co.il/wp-json/nadlan/v1/healthcheck . Confirm "version":"1.6.0" AND directory.claim_cpt=true, directory.auction_cpt=true, directory.bids_table=true.
4. GA4: open GA4 property G-G3QRV5646E → Reports → Realtime, browse the site in another tab, confirm you appear. Also view-source the homepage and confirm "G-G3QRV5646E" is present.
5. Confirm new CPT archives load: /professionals/ , /projects/ , /auctions/ (may be empty until import — a 200 page is success).

OBSTACLES:
- Update notice missing → the json on main may be cached by GitHub raw (~5 min) or PUC's 12h transient; force via deactivate/reactivate plugin.
- bids_table=false → visit any /wp-admin/ page once (table installs on admin_init) then re-check.
- GA4 still no data → confirm the plugin actually updated to 1.6.0 first; the tag is in 1.4.0+.

DELIVERABLE: a short report: healthcheck JSON, GA4 realtime yes/no, which archives returned 200. STOP and report if the merge or update fails — do not hand-edit plugin files on the server.
```

---

## WAVE 2 — Seed the directory (after Wave 1; the contractor + project missions run in parallel)

### Mission 2 — Import the contractors directory (~14k cards)
```
PROMPT:
You are seeding a WordPress directory from a public open-data file.

CONTEXT: nadlan-config v1.6.0 has an importer that pulls רשם הקבלנים (Contractors Registry) from data.gov.il CKAN (resource 4eb61bd6-18cf-4e7c-9f9c-e166dfa0a2d8, ~14k rows) and creates nadlan_professional "cards". Idempotent (re-running updates, never duplicates). Cards import as data_quality=stub and are intentionally noindexed until enriched.

STEPS:
1. WP Admin → Dashboard → "NadLan Directory Import" widget. Under "קבלנים (רשם הקבלנים)" click "Import next 500". It imports a batch and shows the next offset.
2. Repeat clicking until the offset returns to 0 (full pass). Alternatively, if WP-CLI/SSH is available: `wp nadlan import contractors` does the whole run in one command.
3. Verify: WP Admin → NadLan Professionals shows thousands of entries. Open 3 at random on the front end (/professionals/<slug>/): confirm the facts table shows registry number + classification + city, and a "זה הכרטיס שלכם?" claim CTA appears.
4. Confirm stubs are noindexed: view-source a stub card, find <meta name="robots" content="noindex, follow"> (or equivalent). This is expected and correct.

OBSTACLES:
- Button does nothing / error notice → check healthcheck shows 1.6.0; if CKAN is briefly down the importer returns an error — wait and retry.
- Timeouts on a batch → 500/batch is conservative; if the host is slow, that's fine, just keep clicking (cursor is saved).
- Duplicate cards → should not happen (dedupe by source_id); if seen, report — do not delete manually.

DELIVERABLE: total cards created, 3 sample URLs, confirmation stubs are noindexed. Do NOT enrich content here (that's Mission 4).
```

### Mission 3 — Import urban-renewal projects (~938)
```
PROMPT:
Same as Mission 2 but for projects. In the "NadLan Directory Import" widget use the "התחדשות עירונית" button (data.gov.il resource f65a0daf-f737-49c5-9424-d378d52104f5, ~938 compounds → nadlan_project cards). Or `wp nadlan import urban`. Verify under WP Admin → NadLan Projects and open 3 front-end /projects/<slug>/ cards: facts table should show project type (תמ"א38/פינוי-בינוי), city, units, plan number. Confirm noindex on stubs. DELIVERABLE: count + 3 URLs.
```

---

## WAVE 3 — Enrich content (after Wave 2; the big recurring job)

### Mission 4 — Generate original Hebrew prose for every stub card
```
PROMPT:
You are writing original, factual Hebrew encyclopedia-style descriptions for directory cards and pushing them back into WordPress via REST.

CONTEXT: Cards imported by Missions 2-3 are data_quality=stub (noindexed). Each card has structured meta (registry number, classification, city, units, etc.) readable via the WP REST API. Your job: turn the STRUCTURED FIELDS ONLY into 100% original Hebrew prose (never paste/scrape source text — numbers aren't copyrightable, phrasing is), then push it so the card flips to enriched + indexable.

PER-CARD STEPS:
1. Read a card's fields: GET https://nad-lan.co.il/wp-json/wp/v2/nadlan_professional/<id> (and ?per_page=100&page=N to list; filter to meta.data_quality=stub).
2. Generate with this prompt to ChatGPT:
   "אתה כותב ערך אינפורמטיבי, עובדתי וניטרלי בעברית (סגנון ויקיפדיה) עבור [קבלן/פרויקט]. אל תמציא נתונים, השתמש רק בשדות הבאים, דלג על שדות ריקים. נתונים: {json}. מבנה: פסקת פתיחה (מי/מה/מיקום), פסקת נתונים עם סטטיסטיקות (סיווג/ענפים/יחידות/שנה), פסקת הקשר (מה המשמעות של הסיווג/הסטטוס למשתמש — הסבר כללי), סגנון עובדתי ללא שיווק, גוף שלישי, 120-220 מילים, ייחודי לחלוטין. סיים בשורת מקור: 'המקור: פנקס הקבלנים הרשומים, data.gov.il, עודכן [תאריך]'. פלט: H1 + פסקאות + bullets של עובדות + שורת מקור."
3. Push: POST https://nad-lan.co.il/wp-json/nadlan/v1/import-enrich (auth as an editor via application password) body {"post_id":<id>,"content":"<html>","data_quality":"enriched"}. This sets enriched + pings IndexNow.
4. Run a near-duplicate check across your generated texts (shingle/MinHash or simple n-gram overlap); if two cards are >70% similar, regenerate with more entity-specific framing — templated near-duplicates cause SEO cannibalization.

BATCHING: do 100-200/run, oldest stubs first. This is recurring until all stubs are enriched. Keep a progress log (last id done).

OBSTACLES:
- import-enrich 401 → you need an editor application password; create one in WP Admin → Users → Profile → Application Passwords.
- Empty fields → skip them, never invent. If a card has almost no data, write a 2-sentence minimal entry and leave it stub (don't enrich) so it stays noindexed rather than publish a thin page.

DELIVERABLE: number enriched this run, the progress cursor, and 3 sample enriched URLs. Confirm those 3 are now indexable (no noindex meta).
```

---

## WAVE 4 — Test the interactive systems (parallel; after Wave 1)

### Mission 5 — End-to-end test the claim funnel
```
PROMPT:
Test the card-claim funnel on nad-lan.co.il and report bugs (do not fix code — report).

STEPS:
1. On any /professionals/<slug>/ card, fill the "בקשו בעלות על הכרטיס" form (use a test name + your email). Submit. Expect: success message; the card's claim_status flips to "pending"; admin gets an email; a "NadLan Claim" entry appears in WP Admin.
2. As admin, open the NadLan Claim → click "Approve & assign owner". Expect: a subscriber account created/linked for that email (password-set email sent); the card claim_status → verified; owner_user_id set.
3. Log in as that subscriber. Confirm: you CAN edit your own card (title/content/photos). Confirm you CANNOT edit a different card or access other admin areas. THIS IS THE KEY SECURITY CHECK.
4. Try to claim a second, different card as the same user and confirm the scope stays limited to cards you own.

OBSTACLES: rate-limit (5/10min per IP) is expected; wait if you hit it. Honeypot field "company" must stay empty (it's hidden).

DELIVERABLE: pass/fail per step, especially step 3 (privilege escalation). Flag anything where a non-owner could edit a card or reach admin. Report to owner; Claude Code will harden based on your findings (see docs/listings-questions.md §B).
```

### Mission 6 — End-to-end test the auction engine
```
PROMPT:
Test the timed-auction engine on nad-lan.co.il and report.

SETUP: WP Admin → NadLan Auctions → Add New. Set custom fields: listing_id (any nadlan_property id), start_time (now, ISO like 2026-06-01T10:00:00Z), end_time (now + ~10 min), starting_price 1000000, reserve_price 1200000, bid_increment 10000, buyers_premium_pct 5, soft_close_window_sec 120, soft_close_extend_sec 120, status "live". Publish; note the auction id.

TESTS (use 2 logged-in test users; the bid API is POST https://nad-lan.co.il/wp-json/auctions/v1/<id>/bids with header X-WP-Nonce, body {"max_amount":N}):
1. Place a proxy max of 1,300,000 as user A. GET /auctions/v1/<id>/state → current_high should be the starting price (1,000,000), reserve_met false (reserve 1.2M not yet exceeded by display).
2. As user B bid max 1,150,000. Expect: A auto-bids; A still leads at 1,160,000 (B's max + increment), B is outbid.
3. As user B bid max 1,350,000. Expect: B leads at 1,310,000 (A's max + increment); reserve now met.
4. Within 2 min of end_time, place a bid → confirm end_time extends by ~2 min (soft-close) and status becomes "extended".
5. Let it end; within the hour (cron) confirm status becomes "sold" (reserve met) — or trigger by waiting.

OBSTACLES: 401 on bid → must be logged in + send X-WP-Nonce (wpApiSettings.nonce). 409 "not_live" → check start/end times and status. Times are UTC.

DELIVERABLE: the state JSON after each step, whether proxy/soft-close/reserve behaved as described. Report mismatches (don't fix code).
```

---

## WAVE 5 — Build the lawyer-marketplace product (parallel; uses approved docs)

### Mission 7 — Build the /contract-audit/ product + lawyer profile in WP
```
PROMPT:
You are building a WooCommerce product page and a lawyer profile page on nad-lan.co.il from approved specs in the repo.

SOURCES (read first): docs/contract-audit-product-page.md, docs/lawyer-profile-template.md, docs/contract-audit-tos-refund-disclaimer.md.

BUILD:
1. Create the page /contract-audit/ with the approved Hebrew copy: H1 "בדיקת חוזה דירה — לא חותמים עד שבודקים", how-it-works, the 3-tier block (בסיסי ₪390 / מלא ₪690 ⭐ / קבלן ₪1,200, all + מע"מ), "מה לא כלול", FAQ (as FAQPage), final CTA. Use the GREEN canonical design.
2. Create 3 WooCommerce products (or 1 variable, 3 variations) at those prices; add the rush "+₪200 24h" as a product add-on/fee. Checkout via the existing Grow/Meshulam gateway; confirm Greeninvoice issues a חשבונית מס on payment.
3. Add the intake fields (file upload + transaction type + role + signing date + pages + concerns + contact + consent line) as order fields, captured to order meta. On payment, email the order + file to the lawyer (Ben) at info@nad-lan.co.il (auto-email handoff).
4. Create the lawyer profile page /lawyers/ben-betesh/ per the template (use the nadlan_professional CPT): name, bar 29020, specialty, the 3 services with prices, bio placeholder (owner to supply real bio/headshot), disclaimer footer.
5. Add a CTA block on the existing /real-estate-lawyer/ pillar linking DOWN to /contract-audit/.

CANNIBALIZATION RULE: the product page uses "ביקורת חוזה דירה"; do NOT reuse the pillar's exact "בדיקה משפטית" phrase as the product H1/title.

OBSTACLES: missing bio/headshot/sample-opinion → use the placeholders in the template and flag to owner. Don't invent credentials.

DELIVERABLE: the live URLs, a test order screenshot showing a חשבונית מס issued, confirmation the lawyer-handoff email fired. STOP before going live if the חשבונית doesn't issue — report.
```

---

## WAVE 6 — Expand inventory & data (parallel; lower priority, think-ahead)

### Mission 8 — Service-provider registries (שמאים / אדריכלים / עו"ד / בדק בית)
```
PROMPT:
Research and prepare import data for Israeli real-estate service-provider registries, to extend the directory beyond contractors.

FOR EACH profession, find the authoritative public registry + whether it's bulk-downloadable, and map its fields to our card schema (profession, registry/license number, name, city, address, phone, email, classification/specialty):
- שמאי מקרקעין → מועצת שמאי המקרקעין (Real Estate Appraisers Council).
- אדריכלים/מהנדסים → פנקס המהנדסים והאדריכלים.
- עורכי דין → לשכת עורכי הדין (israelbar).
- בדק בית / מפקחי בנייה → check if any registry exists (likely none → mark self-reported).
- יועצי משכנתא → NO statutory registry (self-reported only — flag).

For any source that is a data.gov.il CKAN dataset, capture the dataset slug + resource_id + verified column names (test the API: data.gov.il/api/3/action/datastore_search?resource_id=...&limit=5). For non-CKAN registries, document the access method (CSV/scrape/none) and ToS.

DELIVERABLE: a markdown table per profession (source URL, downloadable Y/N, resource_id if CKAN, field mapping, verification level). This feeds a future importer extension. Do NOT scrape anything behind a ToS prohibition — flag instead. Do not invent resource_ids.
```

### Mission 9 — New-build projects (beyond urban-renewal)
```
PROMPT:
Identify and structure new-construction project data (the projects NOT covered by the urban-renewal dataset) to seed project cards.

There is no single open national dataset for marketed new-build projects. Investigate, ToS-aware:
1. Municipal open-data (e.g. Tel Aviv opendata.tel-aviv.gov.il) for building permits/projects — capture any usable datasets + fields.
2. CBS building-starts/permits aggregates (statistical only — note as context, not per-project).
3. Whether developer/marketing project pages can be catalogued (project name, developer, city, units, price-from, status) WITHOUT violating Yad2/Madlan ToS — prefer first-party developer sites and municipal sources over scraping portals.

DELIVERABLE: a sourcing plan + a sample of 20 real projects in structured JSON (name, developer, city, units, status, source_url) drawn only from permitted sources, ready for the import-enrich pipeline. Flag every ToS concern; do not scrape prohibited sources.
```

### Mission 10 — Verify govmap / nadlan deal-data endpoints (for AVM + neighborhood panel)
```
PROMPT:
Verify the live API endpoints for Israeli real-estate deal data so Claude Code can build a caching ETL + AVM/neighborhood features.

The community references (re-verify, paths may have changed): govmap.gov.il deal endpoints (deals-within-radius, street-deals, neighborhood-deals), nadlan.gov.il transaction search. For a known address (e.g. a Tel Aviv street), capture: (a) the exact request (method, URL, headers, body) that returns recent deals, (b) a sample JSON response with field names, (c) gush/חלקה lookup by coordinate, (d) any rate limits or auth. 

DELIVERABLE: a verified request/response spec (curl examples + sample payloads + field dictionary) for: address→coords, coords→parcel(gush/helka), and deals-by-radius. Flag ToS/legal constraints on storing nadlan price data (get owner/legal sign-off noted). Claude Code will build the ETL from your spec.
```

---

## WAVE 7 — Polish & optimize (lowest priority; after the above)

### Mission 11 — Contact-button redesign (the deferred fix)
```
PROMPT:
Fix and redesign the floating contact buttons on nad-lan.co.il. CONTEXT: they currently render EMPTY on mobile — the component (a wp:html block in the WP Site Editor Footer template part; source snapshot at docs/wp-state/template-part-footer.html, classes .nlfab*) hides text labels under 600px with no icon fallback. Redesign per 2025 best practice: a circular green WhatsApp FAB (#25D366, 56px, border-radius 50%, subtle pulse) bottom-right; on mobile a full-width sticky bottom bar with ICON+label segments (WhatsApp / חיוג / ייעוץ) so buttons are never empty; keep the nadlanOpenLead modal + the tel:/wa.me links to 0525101555 (+972525101555). Add SVG icons inline. RTL-correct. Edit the Footer template part in WP Site Editor (Appearance → Editor → Patterns/Template Parts → Footer). DELIVERABLE: before/after mobile + desktop screenshots; confirm buttons show icons on a real phone width.
```

### Mission 12 — GA4 consolidation (once data confirmed flowing)
```
PROMPT:
CONTEXT: the site now loads BOTH Google Tag GT-W6VHT5TK (via Site Kit) and a direct GA4 tag G-G3QRV5646E (hardcoded in nadlan-config, guarded by the NADLAN_GA4_HARDCODE constant). Once you confirm G-G3QRV5646E is receiving data (Realtime), eliminate double-counting: EITHER (a) add G-G3QRV5646E as a destination inside the GT-W6VHT5TK Google Tag and disable the hardcode by adding `define('NADLAN_GA4_HARDCODE', false);` to wp-config.php; OR (b) keep the hardcode and ensure Site Kit is NOT also pointed at G-G3QRV5646E. Pick one source of truth. DELIVERABLE: which option you chose and confirmation each pageview is counted once (check Realtime event counts aren't doubled).
```

### Mission 13 — Programmatic SEO: city/neighborhood hub pages
```
PROMPT:
Build cannibalization-safe hub pages that aggregate the directory cards and capture generic keyword traffic, linking DOWN to branded cards.
CONTEXT: branded cards target the proper-noun (navigational) intent. Hub pages target generic intent ("קבלנים רשומים ב<עיר>", "התחדשות עירונית ב<עיר>") and must NOT duplicate card content — they list/link to cards. Cross-check every hub slug + focus keyword against the 100-page inventory in site-state.md before publishing (one URL = one intent). For the top 20 cities by card count, create a hub page with: a short original intro, a filterable list/links to that city's contractor + project cards, and internal links up to the relevant pillar. Set noindex on hubs with <5 cards (thin). DELIVERABLE: list of hub URLs created + the keyword each targets + confirmation none collides with an existing inventory keyword.
```

---

## Sequencing summary
- **Wave 1 (Mission 1)** must finish first.
- Then run **Wave 2 (2,3)**, **Wave 4 (5,6)**, **Wave 5 (7)** in parallel.
- **Wave 3 (4)** after Wave 2. **Wave 6 (8,9,10)** anytime in parallel (research-heavy). **Wave 7 (11,12,13)** last.
- Anything Cowork finds broken in Missions 5/6 → report; Claude Code hardens from the findings (docs/listings-questions.md §B).
