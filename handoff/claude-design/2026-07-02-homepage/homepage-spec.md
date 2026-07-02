# NADLAN HOMEPAGE — FULL SPEC (design + SEO + monetization + CMS wiring)
Date 2026-07-02 · Companion visual: `handoff/claude-design/2026-07-02-homepage/` (PNG band-by-band
example + printable page). Reference stack: `2026-07-02-critical-report-and-full-spec.md` (site
audit), `2026-06-28-nadlan-master-spec.md` (fix spec), tokens in
`plugins/nadlan-config/assets/showroom-engine/tokens.css`.

## 0. Verdict on home-v2 (fetched 2026-07-02) — why it feels thin
- 6 short bands, ~40 links. An authority homepage carries 12+ bands and 150+ crawlable links.
- The "featured projects" row is THREE LANGUAGE COPIES of the same Ashira page (EN/FR/RU) presented
  as three projects — looks broken and wastes the flagship slot. Featured = Ashira, Rainbow, Dimri.
- "סיור 3D" labels lead with mechanism; buyers search apartments, not tours.
- No market data, no news/editorial, no areas grid, no professionals band, no mega footer — the four
  things that make Zillow/Madlan homepages feel like institutions.
- Raw wa.me URL printed as text; stat chips unlinked; hero headline is clever but not keyword-bearing.

## 1. The strategy in one paragraph
The homepage does NOT rank for "דירות למכירה" — category pages do. The homepage's jobs: (1) convert
navigational/brand traffic, (2) DISTRIBUTE link equity into the pages that rank (areas, tools,
guides, projects, professionals), (3) look like a 50-year institution so every visitor — buyer,
contractor, lawyer — trusts it in 5 seconds. Rich = many real doors, each labeled with the buyer's
own search words. Every band below exists to catch one intent and tunnel it.

## 2. Keyword → surface map (build category pages to rank; homepage links to them)
| Intent (HE examples; high→mid volume) | Ranking surface | Homepage door (band #) |
|---|---|---|
| דירות למכירה, דירות למכירה בתל אביב/חיפה/... | /properties/ + city archives | Hero search tabs + band 6 |
| דירות להשכרה + city | /properties/?type=rent + city | Hero tab + band 6 |
| פרויקטים חדשים, דירות חדשות מקבלן | /projects/ + area hubs | Band 5 |
| מחירי דירות, מחיר למ"ר בתל אביב | area hubs + price pages (comps data) | Band 4 (market data) |
| מחשבון משכנתא, מס רכישה, החזר חודשי | calculator pages (already strong) | Band 9 |
| קניית דירה מקבלן, נסח טאבו, חוזה מכר | guide pages | Band 8 (magazine) |
| נדל"ן להשקעה, איפה כדאי לקנות דירה | /investment/ + area hubs | Bands 4+8 |
| עורך דין מקרקעין, שמאי מקרקעין + city | /professionals/ archives | Band 10 |
| buying property in israel, tel aviv real estate (EN/FR/RU) | language landing pages | Band 11 |
Rule: homepage `<title>`: "נדלן — דירות למכירה, פרויקטים חדשים ומחירי דירות בישראל". H1 carries
buyer words (see band 3). Never "3D" in title/H1/H2 — it appears as a badge on project cards only.

## 3. THE 12 BANDS (order, content, source, monetization) — see PNG for the look
All bands render from the CMS (options + CPT queries). Band manager: one option
`nadlan_home_bands` (ordered array of band ids with on/off) so the owner can reorder without code.
Tokens throughout: cream #FAF7F1 page, ink #1B1A17, gold #9C7A3C structure, terracotta #C2563A money
CTAs, dark theater #14130F only for bands 5 and 11. Fonts Frank Ruhl Libre/Heebo (HE).

**B1 · Market ticker (utility bar, 36px, ink bg).** מדד תשומות הבנייה, ריבית בנק ישראל, עסקאות
החודש, מחיר ממוצע למ"ר ת"א — 4 live figures + date. Source: options refreshed by the comps/gov cron
(`nadlan_market_snapshot` option, daily WP-Cron). Intent: instant "institution" signal; links to the
price pages. This single strip does more "50-year-old authority" than any hero image.

**B2 · Header + MEGA MENU.** Logo (3-bar mark + NADLAN). Five roots, each a mega panel (grid of
links + one featured card): דירות (למכירה/להשכרה/לפי עיר ×8/פרסום דירה) · פרויקטים חדשים (לפי
אזור, המובילים, התחדשות עירונית) · מחירים ונתונים (מחיר למ"ר לפי עיר, עסקאות אחרונות, מדדים) ·
מדריכים וכלים (5 מחשבונים, 6 מדריכים, מילון) · אנשי מקצוע (עו"ד/שמאי/יועץ משכנתאות/בדק בית + לפי
עיר). Implementation: WP nav menus with a `mega` class per root; panel = `<div class="nl-mega">`
populated from child items; pure CSS open on hover/focus-within (a11y: button + aria-expanded on
mobile). ~60 crawlable links live here.

**B3 · Hero — search-first.** H1: "מוצאים דירה, בודקים מחיר, מכירים את הסביבה — לפני שחותמים".
Sub: one honest line. SEARCH BOX (the Zillow pattern): tabs לקנייה/להשכרה/פרויקטים חדשים/אנשי
מקצוע + city/area autosuggest + budget select → submits to the matching archive with query args
(no JS SPA needed: GET to /properties/?city=…). Right column: the Ashira poster with availability
dots + "בחרו דירה מתוך הבניין" badge → project page. 4 stat chips below, EACH LINKED (projects
965 → /projects/, professionals 2,723 → /professionals/, calculators → hub, guides → hub).

**B4 · Market data cards.** 4 cards: מחיר ממוצע למ"ר (ת"א/ארצי), שינוי שנתי, ריבית ממוצעת
למשכנתא, עסקאות ברבעון — each with source + date + link to its data page. Source: same
`nadlan_market_snapshot`. Monetization: none (trust band). SEO: earns "מחירי דירות" internal-link
relevance and freshness.

**B5 · Featured projects — the DARK band (the product).** Theater-dark strip (#14130F), 3 large
cards: Ashira / Rainbow / Dimri — poster, name, area, price-from (אומדן, מסומן), availability dots,
badge "בחירת דירה מתוך הבניין". First card carries `ממומן` tag when sold as placement. One shared
lazy model-viewer preview on hover (critical-report PART 5 code). Source: `nadlan_project` where
engine-active, ordered by placement auction (existing module). Monetization: THE flagship slot —
sell as "פרויקט מוביל בעמוד הבית" (weekly/monthly via existing placement-auction).

**B6 · Listings — דירות למכירה ולהשכרה.** Two tabs, 8 cards (photo, price, rooms/sqm, city,
verified badge), + "פרסמו דירה חינם" card (AI assistant — existing flow). Source: `nadlan_property`
newest/featured. Monetization: featured-listing upsell (existing featured-upsell module); label
`מקודם` on paid cards. SEO: links into city archives ("דירות למכירה בחיפה ←" row footer links, 8
cities — these anchor-text links are what ranks the archives).

**B7 · Areas grid — אזורי ביקוש.** 6-8 area cards (photo/map thumb, avg ₪/מ"ר, # projects, # deals):
שדה דב, רמת אביב, צהלה, בת ים, חיפה, ירושלים, נתניה, באר שבע. Source: area taxonomy + snapshot
figures. SEO: the strongest internal links on the page — area hubs are where "דירות ב{city}" ranks.

**B8 · Magazine — חדשות ומדריכים (the "rich content" band).** Newspaper layout: 1 lead editorial
card (image, kicker, H3, 2-line dek, date) + 4 headline rows (kicker + headline + date) + right
rail "המדריכים החשובים" list (5 evergreen guides). Source: `post` CPT (news/analysis) + curated
guide list. Cadence: 2-3 posts/week minimum — freshness is a ranking system; an empty news band is
worse than none, so the band collapses below 3 recent posts. Monetization: sponsored article slot
(`תוכן ממומן` label, one max).

**B9 · Tools — כלים שחוסכים טעויות יקרות.** 5 calculator cards + מילון + "כמה שווה הדירה שלי".
Existing pages; keep the band, add the estimator as lead card (it's a lead magnet: estimate →
"רוצים הערכה מדויקת? עו"ד/שמאי מומלץ ←" → professionals funnel).

**B10 · Professionals — sponsored mechanism.** 4 cards: עו"ד מקרקעין, שמאי, יועץ משכנתאות, בדק
בית — each shows ONE professional (photo, name, city, rating, gov-verified badge) + "עוד 2,723
אנשי מקצוע ←". Slot logic: paid `sponsored` professionals rotate first (label `ממומן`, required by
law), else top-rated. Source: `nadlan_professional` meta `sponsored_until`. Monetization: monthly
sponsorship per category×city — this is the scalable revenue line (2,723 supply, clear value).
Wire: `nadlan_pro_sponsor_slot( $category, $city )` helper; greeninvoice billing exists.

**B11 · International — dark band #2.** "Buying property in Israel?" EN headline + FR/RU/AR
sub-links, 3 trust points (process, legal, financing), CTA → EN landing page (a real page, not the
Ashira EN post: `/en/` hub with projects + guides for foreign buyers). Monetization: foreign-buyer
leads are the highest-value leads; route with `lang` field (already in lead payload).

**B12 · MEGA FOOTER (the SEO floor).** 6 columns, ~80 links: דירות לפי עיר (10) · פרויקטים לפי
אזור (8) · מחשבונים ומדריכים (10) · אנשי מקצוע לפי תחום (6) ולפי עיר (6) · מחירים ונתונים (5) ·
NadLan (אודות, צור קשר, שפות, תקנון). Plus trust line (disclaimer), WhatsApp labeled button, the
existing counts row. Implementation: `parts/footer.html` block part rebuilt; links from menus so
they're CMS-managed. Every column heading is an H2-styled label (not a real H2).

## 4. CMS wiring summary (what the agent builds)
- `nadlan_home_bands` option (ordered ids, on/off) + one renderer per band in
  `inc/homepage.php` (exists — extend): `nadlan_home_band_ticker()`, `_hero()`, `_market()`,
  `_projects()`, `_listings()`, `_areas()`, `_magazine()`, `_tools()`, `_pros()`, `_intl()`.
- `nadlan_market_snapshot` option: `{ppsqm_tlv, ppsqm_il, yoy, mortgage_rate, deals_q, updated}` —
  daily cron from the existing gov/comps import; every figure prints value+date+source.
- Sponsorship meta: project placement (existing auction) · `nadlan_property.featured_until` ·
  `nadlan_professional.sponsored_until` + category/city. All sponsored units carry the visible
  `ממומן`/`מקודם` label — legal + trust.
- Search: plain GET form → archive URLs with query args; autosuggest from a cached city/area list
  REST endpoint (`/nadlan/v1/suggest?q=`).
- Version surfaces + screenshot gates per master-spec PART J. No-stacking law applies: home-v2
  REPLACES the current homepage in one release; the old one is archived, not left as a second home.

## 5. Acceptance gates (homepage release)
□ 12 bands render from CMS data; any band with missing data collapses cleanly.
□ ≥150 crawlable internal links; mega menu keyboard-accessible; footer columns from menus.
□ Featured projects = 3 DISTINCT projects; language variants appear only as a language switcher.
□ Title/H1 carry buyer keywords; no "3D/תלת-ממד" in title/H1/H2; badges only.
□ All sponsored slots labeled; every stat has source+date; no invented numbers.
□ LCP ≤ 2.5s (hero is server-rendered text+img; one lazy model-viewer max); CLS ≈ 0.
□ Screenshots desktop 1440 + mobile 390, HE, attached; compared against the PNG example.
