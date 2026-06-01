# Listings · Directory · Auction — Architecture & Knowledge (BUILT v1.5.0)

> Consolidates three deep-research passes (best-in-class portals, cutting-edge proptech, IL directory data sources) + the infrastructure shipped in nadlan-config **v1.5.0**. Written provider-agnostic where possible for **reuse on Justice.co.il**. Owner brief 2026-06-01: free SEO cards for all IL projects+contractors+service-givers (claim-to-upgrade), Zillow-grade listings, online auctions, "levels above competitors", deeply wired, latest tech.

---

## 0. What is already BUILT and shipped (v1.5.0, on feature branch / PR #4)

Modular includes under `plugins/nadlan-config/inc/`, wired via `require_once` loop in the main plugin, healthcheck reports readiness. **Nothing live until merge→main + WP "Update".**

| Module | What it does |
|---|---|
| `catalog-meta.php` | REST meta for `nadlan_project` + `nadlan_professional`; shared claim/ownership/provenance meta on all 3 card CPTs. New cards default `claim_status=unclaimed`. |
| `claim.php` | `nadlan_claim` request CPT; public `POST /nadlan/v1/claim` (honeypot+rate-limit); admin "Approve & assign owner" meta box → creates/links a subscriber + sets `owner_user_id`, `claim_status=verified`; `map_meta_cap` lets a verified owner edit ONLY their own card + upload files. |
| `import.php` | data.gov.il CKAN importer. Contractors (res `4eb61bd6-18cf-4e7c-9f9c-e166dfa0a2d8`, ~14k) → `nadlan_professional`; urban-renewal (res `f65a0daf-f737-49c5-9424-d378d52104f5`, ~938) → `nadlan_project`. Idempotent upsert by `source_id`. Dashboard "Import next 500" buttons + `wp nadlan import contractors|urban` WP-CLI + `POST /nadlan/v1/import-enrich` for the Cowork/ChatGPT enrichment push. |
| `auction.php` | `nadlan_auction` CPT + custom `wp_nadlan_bids` table (dbDelta). Proxy/auto-bid, hidden reserve, soft-close anti-sniping, buyer's premium. `auctions/v1` REST: `/{id}/state`, `/{id}/bids` (GET history, POST place-bid). Per-auction `GET_LOCK` serializes bids. Hourly cron closes ended auctions. |
| `schema.php` | JSON-LD per card (GeneralContractor / ApartmentComplex / RealEstateListing / Event). **Thin-content noindex guard**: stub cards (data_quality≠enriched, <80 words, unclaimed) get `noindex,follow` via `wp_robots` + `wpseo_robots`. |
| `cards-render.php` | Appends facts table + media gallery + claim CTA (JS→claim REST) + provenance line to card single views. `[nadlan_card]` shortcode. Scoped CSS/JS. |

**Operate it:** WP Admin → Dashboard → "NadLan Directory Import" widget → click "Import next 500" repeatedly (or run WP-CLI) → cards appear under /professionals/ and /projects/ as `stub` (noindexed) → Cowork enriches each via `import-enrich` (original Hebrew prose) → card flips to `enriched` + indexable + IndexNow-pinged.

---

## 1. The strategic thesis (why this wins)

- **IL has no productized listing+auction+directory leader that's open and data-rich AND conversion-optimized.** Yad2 = inventory volume; Madlan = data depth; neither nails proactive alerts, seller funnels, or auctions. (See competitor read in §2.)
- **Free auto-cards = SEO land-grab.** ~14k contractors + ~938 renewal compounds + projects + service providers = thousands of branded/navigational pages we own before the entity does. Entity finds its #1-ranking card → claims → upgrades → marketing-platform revenue. The SEO does the selling (same insight as the contract-audit research).
- **Stats-rich original cards read as a knowledge source** → Google + AI answer-engines prefer them. Numbers aren't copyrightable; only phrasing is → generate original prose from structured fields (never paste source text).

---

## 2. Competitor read (verified research)

- **Zillow**: Zestimate AVM, "what's my home worth" seller funnel, mortgage calcs, 3D Home/SkyTour, saved search.
- **Redfin**: Redfin Estimate, **Hot Homes** (predicted-to-sell), days-on-market + favorite/tour counts as social proof, "Go Tour" CTA.
- **Realtor.com**: noise indicator, Flood Factor; surfaces price/schools/commute/crime/noise.
- **Rightmove**: sold-price history (Land Registry), full-screen floorplans, School Checker per listing.
- **Yad2 (IL)**: largest inventory, amenity checklist, neighborhood 0–5 user rating, map. *(JS-rendered; verify live.)*
- **Madlan (IL)**: data depth — median price, ₪/sqm, demographics, resident reviews, transaction history, planning/תב"ע, claims even sunlight; pulls Tax Authority + CBS. *(Verify sunlight/planning claims.)*

**To beat both:** Madlan-grade data + Redfin/Zillow conversion mechanics + Yad2-grade inventory, in proper Hebrew RTL.

---

## 3. Listings feature roadmap (the "Zillow" build — NOT yet built, prioritized)

Top must-builds (from research, ranked by SEO+conversion value):
1. **Nearby deal-history + AVM estimate** on every listing (govmap/nadlan deals → cached table → comps median). Madlan's moat.
2. **Neighborhood data panel** (median ₪/sqm, trend chart, demographics, resident reviews) — CBS + cached deals.
3. **Rich media**: photo + floorplan + video + 3D/360 (Kuula/Zillow 3D free-tier embeds), full-screen RTL gallery.
4. **Saved searches + email/WhatsApp/push alerts** (accounts + WP-Cron matcher).
5. **"How much is my apartment worth" seller lead funnel** (AVM → email + capture lead).
6. **One-tap WhatsApp + תיאום ביקור (schedule viewing)** flow.
7. **School + planning (תב"ע) overlays** (data.gov.il schools, govmap planning layers).
8. **Compare + favorites synced across devices**.
9. **Localized משכנתא/affordability calculator in ₪**.
10. **Programmatic SEO**: per-neighborhood landing pages from deal/CBS data + JSON-LD RealEstateListing.

IL-specific: full RTL, **גוש/חלקה/תת-חלקה** as first-class meta (join key to gov data), ועדה מקומית + תב"ע, מחיר למשתכן flag, IL listing types (דירת גן/פנטהאוז/דו-משפחתי/קוטג'/מגרש/מסחרי) + amenities (ממ"ד/מעלית/חניה/מרפסת/ארנונה/ועד בית).

**Cutting-edge "build now, high impact / low cost"** (from proptech scout): AI listing descriptions (LLM, pennies), JSON-LD (done), 3D tours (free embeds), AI virtual staging (disclose!), comps-based AVM lead magnet, similar-listings (SQL), e-sign on auction win (BoldSign/Dropbox Sign), NL search (LLM→filters), WhatsApp click-to-chat + chatbot, instant tour booking, image auto-tagging. **SKIP (hype):** blockchain tokenization / on-chain deeds (<0.1% market, no legal recognition, no liquidity).

---

## 4. Verified IL data sources (for importer + enrichment)

- **רשם הקבלנים** (the ~14k seed): dataset `data.gov.il/dataset/pinkashakablanim`, resource `4eb61bd6-18cf-4e7c-9f9c-e166dfa0a2d8`. CKAN: `data.gov.il/api/3/action/datastore_search?resource_id=...&limit=&offset=`. Key cols: `MISPAR_KABLAN` (canonical id), `SHEM_YESHUT` (name), `MISPAR_YESHUT` (company id), `SHEM_YISHUV` (city), `SHEM_REHOV`/`MISPAR_BAIT`, `MISPAR_TEL`, `EMAIL`, `KOD_ANAF`/`TEUR_ANAF` (branch), `SIVUG` (1–5 classification), `KABLAN_MUKAR`. One contractor = multiple rows (dedupe on MISPAR_KABLAN, aggregate branches). Branch codes: gov.il/he/departments/general/anfey_rishum_pinkas_hakablanim.
- **התחדשות עירונית** (תמ"א38/פינוי-בינוי, ~938): dataset `data.gov.il/dataset/urban_renewal`, resource `f65a0daf-f737-49c5-9424-d378d52104f5`. Cols: `MisparMitham`, `Yeshuv`+`SemelYeshuv`, `ShemMitcham`, `YachadKayam`/`YachadTosafti`/`YachadMutza`, `TaarichHachraza`, `MisparTochnit`, `KishurLatar`, `Maslul`, `ShnatMatanTokef`, `Bebitzua`, `Status`.
- **Deals/price** (nadlan.gov.il, Tax Authority): NO official API — UI only; ToS caution; State Comptroller 2025 flags data quality. Use for ₪/sqm enrichment, not primary seed. govmap layer `?lay=NADLAN`.
- **govmap** GIS/parcels/planning: `govmap.gov.il/sites/api_examples.html`. Community clients (nadlan-mcp etc.) report deal/parcel endpoints — paths reverse-engineered, **re-verify**. Build a caching ETL layer (cron → custom tables), never live per-pageview.
- **CBS/הלמ"ס**: building permits (statistical, not project-level), locality demographics.
- **Schools**: data.gov.il Ministry of Education dataset (search `package_search`, verify resource_id).
- **OSM Overpass** (`overpass-api.de/api/interpreter`): POI/transit for "what's nearby".

Build sequencing: Phase 1 contractors (clean CSV) → Phase 2 urban-renewal → Phase 3 new-build projects (scrape, messy) → Phase 4 service providers (per-profession registries: שמאים מועצת שמאי המקרקעין, אדריכלים פנקס המהנדסים, עו"ד לשכת עוה"ד, יועצי משכנתא = no registry → mark self-reported).

---

## 5. Original-content generation (anti-plagiarism)

Feed ONLY structured fields (numbers/dates/codes) to ChatGPT, instruct 100% original Hebrew Wikipedia-style prose, 120–220 words, no marketing, end with provenance line. Per-type prompt variants (project=timeline/price; contractor=branch table; service=credential+verification level). Run a near-duplicate (MinHash/shingling) check across generated cards to avoid templated cannibalization. Push result via `POST /nadlan/v1/import-enrich`. (Delegate the batch to Cowork — same pipeline as article batches.)

---

## 6. Claim / verification model (anti-hijack) — built skeleton + TODO

Built: claim request → admin approve → owner assigned → owner edits own card. **Verification METHOD is the hardening TODO** (see questions doc). Best-practice layered model to implement:
1. Match canonical id (MISPAR_KABLAN + company id / license no.) against registry row.
2. **OTP to the registry-listed phone/email** (`MISPAR_TEL`/`EMAIL`), NOT a typed contact — the key anti-hijack step (Google-postcard principle).
3. Domain/email match → instant verify.
4. Document upload fallback → human review.
5. Manual/video review for contested/high-value claims.
6. Hardening: never reveal OTP via support; re-verify on owner transfer; queue competing claims; rate-limit; immutable edit log; pre-claim card is read-only public data so a hijack can't alter facts.

---

## 7. Auction engine spec (BUILT — reference)

Timed English auctions (Auction.com/Hubzu model). Data: `nadlan_auction` CPT + `wp_nadlan_bids` table. Proxy/auto-bid: bidder submits `max_amount`; system shows min needed to lead = one increment above next-highest max. Hidden reserve → `reserve_met` flag. Soft-close: bid within `soft_close_window_sec` (default 120) extends end by `soft_close_extend_sec` (default 120). Buyer's premium % on win. Server-side validation + per-auction `GET_LOCK` (no double-winner). Hourly cron closes; on-page countdown should also re-check at zero. **TODO**: deposit holds + capture via Grow/Meshulam; e-sign on win (BoldSign/Dropbox Sign, ~48h window); true realtime (Pusher/Ably) vs current /state polling; system cron for second-level precision (WP-Cron is minute-ish).

---

## 8. Cannibalization discipline (HARD RULE)

- Entity cards = **navigational/branded** intent (the proper noun only). canonical = the card. Org/LocalBusiness/RealEstateListing schema.
- Generic keyword pages (e.g. "קבלן רשום בתל אביב", "תמ"א 38 מדריך") = hub/category pages that rank for the keyword and **link DOWN** to cards — never duplicated by cards.
- One URL = one intent. Cross-check every slug+focus-keyword against the **100-page inventory** (site-state.md cannibalization map).
- Thin/stub cards = `noindex,follow` until enriched (BUILT in schema.php). Facet/empty city combos should noindex too.
- Near-duplicate check across generated card bodies (MinHash).

---

## 8b. AVM / valuation methodology (BUILT v1.7.0 — `inc/avm-deals.php`)

Research-grounded (2025–26 best practice):
- **AVMs blend methods:** comparable-sales (comps), **hedonic regression** (value from features: sqm, rooms, age, location, sale timing), repeat-sales, and tax-assessment models. Modern AVMs are ML (gradient boosting: XGBoost/LightGBM/CatBoost; RF; sometimes LSTM/Transformer for time trends) and report a **confidence score / Forecast Standard Deviation (FSD)**. Leaders claim ~2% median error on-market, ~90–94% accuracy; 2026 trend = **explainable AI (SHAP)** for interpretable reports (needed in regulated/lending use).
- **What we built (v1.7.0):** a comparable-sales AVM as the pragmatic phase-1 — median ₪/sqm of nearby comps (same city, sqm ±25%, rooms ±1, last 36 months, 10% trimmed for robustness) × subject sqm; confidence = (1−coefficient-of-variation) scaled by sample size; ± band 5–25% from dispersion. Returns `insufficient_data` under 5 comps so it never shows a junk number. Reads ONLY from the cached `wp_nadlan_deals` table (never calls upstream per pageview).
- **Data ingest, two paths (decoupled from endpoint reverse-engineering):** (a) `nadlan_deals_remote` filter where Cowork's verified govmap/nadlan endpoint (mission M10) slots in for a cron ETL; (b) `POST /nadlan/v1/deals-ingest` so Cowork can push verified deal rows directly. Either fills the cache; the AVM works off it regardless.
- **Surfaces:** on-listing valuation block (estimate + range + comp count + confidence% + "not an appraisal" disclaimer), neighborhood 12-mo stats, and a `[nadlan_home_value]` **seller lead funnel** (estimate + captures phone → lead).
- **Roadmap upgrade:** replace median-comps with a trained gradient-boosting model + SHAP explanation once enough deal rows are cached; add repeat-sales index per neighborhood; price-trend charts.
- **BLANK (legal):** storing nadlan.gov.il price data needs ToS/legal sign-off (no official API). Govmap deal endpoints are reverse-engineered — verify (M10) before wiring the live ETL.

## 8c. AI features (BUILT v1.9.0 — `inc/ai-features.php`) + compliance discipline

**Hard rule, baked into the prompt AND a post-generation scanner:** no steering language by protected class. HUD (USA, 2024) and Israel's **חוק איסור הפליה במוצרים, בשירותים ובכניסה למקומות ציבוריים** both apply to AI-generated marketing copy — the platform is legally responsible for what it publishes. Penalties are real (US: per-violation can exceed $100k).

Banned phrases (non-exhaustive; reviewed list lives in code):
- Family/age: "מתאים למשפחות עם ילדים", "ל-zugot צעירים", "great for young professionals", "perfect for families".
- Religion/ethnicity: "קרוב לבית כנסת/מסגד/כנסייה", "שכונה דתית/חרדית/חילונית/ערבית/יהודית", "close to church/synagogue/mosque".
- Disability: "walking distance" (ableist) → "near".
- Exclusionary: "exclusive neighborhood".

What v1.9.0 ships:
- `nadlan_llm_request($system,$user,$opts)` — pluggable LLM adapter (default Anthropic, gated on `NADLAN_LLM_API_KEY`; swap via filter for OpenAI/DeepSeek). Never fails open: returns `WP_Error` on missing key.
- **AI description generator** (admin meta box on `nadlan_property`): reads facts → prompts the LLM with the guardrails → runs `nadlan_compliance_scan()` → if hits, stores as DRAFT + flags for editor; if clean, editor still must click "Approve & write to content". Never auto-publishes.
- **Natural-language search** (`GET /nadlan/v1/nl-search?q=...` + `[nadlan_nl_search]`): LLM parses Hebrew → strict-JSON filter → reuses `nadlan_ss_meta_query()` → returns items + the parsed filter for transparency. **Deterministic regex fallback** for Hebrew patterns (`N חדרים`, `עד N מיליון`, `ב<עיר>`, `שכירות`/`מכירה`) keeps it working even if LLM is down. 1-hour transient cache per query.

Research grounding: Realmo Rey, planetRE+DeepSeek, Zillow's NL search (May 2026 launches); 2026 best-practice = LLM→structured filter→deterministic query, with cache + fallback.

**BLANK (owner):** pick LLM provider + add `NADLAN_LLM_API_KEY` to wp-config.php. Compliance list is conservative; review with counsel before relaxing. NL-search UX (autocomplete, history, voice) is roadmap.

## 8d. Programmatic SEO city hubs (BUILT v1.10.0 — `inc/city-hubs.php`) — 2026 discipline

**2026 reality (research):** Google now treats thin programmatic pages as **doorway/scaled-content abuse** with manual-action risk. The bar is much higher than 2022. Best practice:
- **≥25-30% UNIQUE data per URL** (not boilerplate). Real numbers, real entities, not "nice place to live".
- **Quality > volume.** 10 strong neighborhood hubs > 100 thin ones. Start with priority cities; expand from data.
- Zillow's model = hyper-local pages with home values + price trends + schools + walkability — context-rich, not template-stuffed.

What v1.10.0 ships:
- Rewrite endpoints `/city/<city>/{contractors|projects|properties}/` (no DB pages — clean, cache-friendly).
- **Card-count floor = 5** (configurable): under the floor → 404 (no thin page enters the index). Between 5 and the doubled floor → `noindex,follow`. Above → indexable.
- Per-hub unique data: count, AVG ₪/sqm + 12-mo deal count from the `wp_nadlan_deals` cache, plus top cards rendered inline.
- `CollectionPage` + `ItemList` JSON-LD, `meta description` derived from real counts, dedicated `/sitemap-nadlan-hubs.xml` (linked into Yoast sitemap index) that only includes hubs above the floor.
- Per-kind UP-link: contractor hubs → `/real-estate-lawyer/` pillar; project hubs → `/contract-audit/` product; property hubs → `[nadlan_save_search]` alert form. Cannibalization-safe (hub keyword = generic; cards = branded).

## 8e. Rich media (BUILT v1.10.0 — `inc/media.php`)

- **Kuula** is the recommended 3D-tour platform (Matterport dropped by Zillow Oct 2025 after CoStar acquired it; Kuula is the approved Zillow provider). We support: Kuula iframe (JS-style for iOS/perf, post-id auto-extracted), generic iframe (CloudPano/Panoee), video via WP oEmbed (YouTube/Vimeo), floorplan image or PDF (iframe).
- Tabbed UI on property singles. `VideoObject` JSON-LD when a video is set (rich-result eligible).
- Meta: `tour_url`, `video_url`, `floorplan_url` (REST exposed).

## 9. REUSE → Justice.co.il

The whole pattern is portable: free-card land-grab → claim → upgrade → marketing platform; CKAN/registry importer; original-content pipeline; thin-content noindex guard; auction engine; cannibalization discipline. For Justice.co.il swap entity types (lawyers/courts/legal-topics/rulings) and registries (לשכת עוה"ד, court databases). Keep modules provider-agnostic. **Standing instruction: keep recording all research + patterns into skills/ as the reusable asset.**
