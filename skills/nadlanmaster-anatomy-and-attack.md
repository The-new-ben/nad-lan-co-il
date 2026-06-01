# nadlanmaster.co.il — anatomy, business model, and our attack plan

> Owner brief 2026-06-01: nadlanmaster is the closest WordPress competitor and the one to beat. This skill captures what was verified by **direct probe** (May 2026) + the cannibalization-safe content gaps we attack + the Lovable deep-research mission. Honest, sourced; "מה הוסק" flagged where it is.

## 1. Verified anatomy (direct fetch, 2026-06-01)

| signal | value |
|---|---|
| Stack | **WordPress 5.4.19** (4+ years old — security & schema gap) + Yoast SEO sitemaps + **Contact Form 7** (CF7) for lead capture + GTM + **GA4 `G-PQG7YNQFV0`** |
| Schema present | basic only: `Organization`, `WebSite`+`SearchAction`, `WebPage`, `ImageObject`. **No `RealEstateListing`, no `Article`, no `BreadcrumbList`, no `FAQPage`, no `LocalBusiness`** |
| Indexable URLs | **~650 total** = 280 posts (post-sitemap.xml) + 71 categories (category-sitemap.xml, mostly Israeli cities) + 299 pages (page-sitemap.xml) |
| robots.txt | minimal (disallow `/wp-admin/`, allow ajax, sitemap reference) |
| Project page lead capture | **3 CF7 forms per page** (top, mid, footer) — aggressive |
| Page weight | ~200 KB HTML per project landing page |

## 2. Verified silo / silos (what they own)

**Commercial pillars in main nav (top-of-funnel money keywords):**
- איך קונים דירה (process)
- מדריך הערכת שווי דירה ("שווי דירה" — top P1 per our rulebook §3.2)
- מדריך רכישת דירה מקבלן
- מדריך קניית דירה על הנייר
- המדריך למציאת השקעה מניבה
- המדריך לאיתור דירות חדשות למכירה
- מדריך רכישת קרקע חקלאית
- **מחשבון תשואה** + **מחשבון מס רכישה** (both at money intent)
- השקעה בטוחה עם תשואה גבוהה / משקיע כשיר / השקעות אלטרנטיביות / השקעה לטווח ארוך / ליווי משקיעים
- קבוצת רכישה (group purchase)

**City categories (71 categories — most cities of Israel covered):**
ofaqim, eilat, alfe-menashe, ariel, ashdod, ashkelon, beer-yaakov, beer-sheva, bet-shemesh, bnei-brak, binyamina, bat-yam, givat-shmuel, givatayim, dimona, hod-hasharon, herzliya, hadera, holon, haifa, harish, jerusalem, kohavyair, modiin, nahariya, ness-ziona, netivot, netanya, afula, petah-tikva, kiryat-ono/bialik/gat/motzkin, rosh-haayin, rishonlezion, rehovot, ramat-gan, ramat-hasharon, raanana, telaviv, tel-mond + regions (north/hasharon/merkaz/darom-projects).

**Foreign-market pillars (the unique grab vs Israeli portals):**
פורטוגל, קפריסין, יוון (אתונה, בטומי), אמירויות (דובאי), גאורגיה, ארה"ב, פולין — each its own pillar.

**Project landing pages (280 — confirmed by sample):** הרובע הצפוני הרצליה, מתחם האלף ראשון לציון, חוף התכלת הרצליה, רובע הים חדרה, מתחם המייסדים נס ציונה, מגדלי הטמפלרים שרונה (קבוצת חגג), דה-וינצי תל אביב, הבית כוכב יאיר (אמפא מליבו), חזנוביץ 10-12 יובלים תל אביב, The New TLV (דקר גלעד), פסגת דן רמת גן, Via4 רמת גן, יבנה סנטרל, נבו נוף השרון נתניה, NH Park מודיעין, Time Tower רמת גן, פרי בכפר אלדד/פרי תל מונד, Ocean Breeze נתניה, סבינים בלאגן/סביוני נוף, פרויקט ONE רעננה (קבוצת בר-עוז), טריפל רעננה (קבוצת מזרחי), 456 פתח תקווה (MSN נדל"ן), 'אנגליה החדשה' קייב, etc.

**Developer (יזם) categories** (these are PAID relationships):
- `/canada-israel/` (קנדה-ישראל)
- `/hanan-mor/` (חנן מור)
- `/kadima-zoran/` (קדימה צורן)

## 3. Verified business model (what they actually monetize)

1. **Paid project landing pages for developers** — confirmed by 3 CF7 forms per project page + 280 project posts + a `/pirsum/` page (= "advertise with us") + a `/pirsumi/` category (= "sponsored"). This is the main revenue.
2. **"ליווי משקיעים" service** (investor consulting) — high-margin lead funnel from the investment pillars.
3. **"השקעות אלטרנטיביות" + "משקיע כשיר"** — likely commissions/affiliate on alternative-investment products marketed to "qualified investors" (משקיע כשיר is a regulated category in Israel).
4. **Foreign-market deal flow** — Portugal/Cyprus/Greece/UAE pillars feed leads to companies that sell foreign properties to Israeli investors (lucrative commission category).

## 4. Honest assessment — where we already beat them, where we don't

> **Honest** per owner's request — not flattery, not panic.

### ✅ We are ahead of them (already-shipped):
| area | nadlanmaster | nad-lan v1.16.0 |
|---|---|---|
| WordPress version | 5.4.19 (4+ years old — security/schema risk) | latest (v6.7+) |
| Schema | Organization/WebSite/WebPage only | RealEstateListing, GeneralContractor, ApartmentComplex, Event (auction), BreadcrumbList, FAQPage, VideoObject, AggregateRating (when real) |
| Card data layer | none (just article posts) | 14k auto-imported contractors (רשם הקבלנים) + 938 urban-renewal compounds — REAL public-data cards, idempotent re-import |
| AVM / valuation | none — they only have a "guide" page | full comparable-sales AVM with FSD confidence + `wp_nadlan_deals` cache (slots in govmap ETL via filter) |
| Neighborhood/POI | none | Overpass POI panel, 24h cache, fail-silent |
| Live map | none | Leaflet + markercluster on /properties/ archive + city hubs |
| Search | basic WP `?s=` | NL Hebrew search (LLM→strict JSON filter→WP_Query) with regex fallback + 1h cache |
| AI desc | none | guarded by HUD/IL anti-discrimination, post-gen steering scan, never auto-publishes |
| Auction | none | timed auctions w/ proxy bid, soft-close, hidden reserve, custom bid table |
| Lead drip | none visible | 6-step Hebrew sequence, state machine, opt-out |
| Saved search | none | double-opt-in email alerts, daily cron |
| Compare listings | none | localStorage tray + /compare/ |
| Mortgage calc | static guide | live JS calc + 6 more calculator slots planned (rulebook §9.3) |

### ⚠️ Where they still beat us today (close these):
| area | what they have | what we need |
|---|---|---|
| **Established trust/age** | ~650 indexable URLs, 4+ years of accumulated backlinks/authority | takes time; we mitigate with depth (rulebook §4) + the encyclopedia (cannibalization-safe long-tail) |
| **Developer relationships** | 280 paid project landing pages | our 938 urban-renewal cards are STUBS — none monetized yet. Need: (a) flip the high-traffic ones to Pro tier with paid developer relationships; (b) outreach to יזמים; (c) the rulebook §10 sponsor model |
| **Foreign-market pillars** | Portugal/Cyprus/Greece/UAE/USA pillars + posts | ZERO. **Decision needed (banked):** does "nad-lan" expand to chu"l, or stay Israeli-pure? Rulebook §1 says "quiet authority IL" — argues against foreign sprawl |
| **Calculator pillars as PAGES** | Yields + Purchase-tax pages ranking for high-intent | we have JS calcs but no dedicated pillar pages. Rulebook §5.1 lists 7 calculator pillars to build |
| **"קבוצת רכישה"** | category + content | none on our side. Money keyword, definitional play available |
| **"משקיע כשיר" / "השקעות אלטרנטיביות"** | pillars + funnels | none. High-LTV lead segment |

### ❌ Where they will keep beating us if we ignore it:
- Their **silo internal-linking** is dense — every post under every category. We have categories (CPT taxonomies) but few internal links UP from cards to pillars yet (we DO have UP-links from city-hubs to /real-estate-lawyer/ and /contract-audit/). Need explicit silo wiring per rulebook §6.

## 5. Cannibalization-safe content gaps (what to add WITHOUT breaking the rulebook §3.6)

Cross-referenced against:
- Existing 100-page inventory (site-state.md cannibalization map)
- Our own pillars: /real-estate-lawyer/, /contract-audit/
- Our existing CPTs: nadlan_property/project/professional/auction/lead/saved-search/claim/esign
- Encyclopedia plan (skills/content-encyclopedia-glossary-plan.md)

**Safe to add as ORIGINAL Hebrew pillars/spokes (not on our inventory; not on a Israeli competitor's lock; rulebook target_intent unique):**

### A. Calculator pillars (5 to build — rulebook §9.3):
1. **שווי דירה** (`/home-value/`) — pillar + form posting to existing `[nadlan_home_value]` shortcode + AVM. ⚠ Avoid "כמה שווה הדירה שלי" (intent close to existing; differentiate by H1 wording).
2. **מחשבון תשואה / איך מחשבים תשואה** (`/yield-calculator/`) — pillar with calc + investor lead form. Direct competitor: nadlanmaster owns this. Beat by data depth (gov-data avg ₪/sqm + actual rent comparables from data.gov.il if available).
3. **מחשבון מס רכישה** (`/purchase-tax-calculator/`) — pillar + calc. Authoritative source: רשות המסים tax brackets (data is public + non-copyrightable).
4. **מחשבון מס שבח** (`/capital-gains-calculator/`) — same model.
5. **מחשבון משכנתא + יחס החזר** (`/mortgage-calculator/`) — calc + lender lead.

### B. Wikipedia-orphan glossary (already mapped — skills/content-encyclopedia-glossary-plan.md §3):
Owner-flagged as highest-EV "no Hebrew article exists" play. These do NOT exist on nadlanmaster either:
- **Construction/architecture**: בטון מזוין, כלונסאות, איטונג, בלוק תרמי, בידוד תרמי/אקוסטי, באוהאוס, ברוטליזם, סגנון בינלאומי, תקן 1045, תקן 413.
- **Planning law**: תב"ע, תמ"מ, קו בניין, אחוזי בנייה, ייעוד קרקע, הפקעה, איחוד וחלוקה.
- **Real-estate law definitions** (not transactional): זיקת הנאה, זכות קדימה, ליס פנדנס, רכוש משותף, צו בית משותף, חכירה לדורות, נסח טאבו, שטר מכר (definitional, not "מה לבדוק בחוזה").
- **Mortgage definitions**: לוח שפיצר, לוח קרן שווה, גרייס, פריים, ריבית קבועה/משתנה (definitional, not "מחזור משכנתא").
- **Appraisal**: שמאי מקרקעין, שמאי מכריע, גישת ההשוואה/העלות/היוון, שווי שוק, שווי מימוש מהיר.
- **Professions** (definitional, link to /professionals/ directory): קבלן רשום, מפקח בנייה, מהנדס קונסטרוקטור, אדריכל רשוי.
- **Deal types**: קומבינציה, פרי-סייל, קבוצת רכישה, REIT, סאבלט (definitional).

**These work because:**
1. Most have **no Hebrew Wikipedia article** (low SERP competition; we can rank #1 fast).
2. Pure definitional intent ≠ the transactional intent of our pillars (rulebook §3.6 rule 5 — "אחד-לכוונה").
3. Each becomes an internal link upward to a money pillar (rulebook §6: "spoke מקשר פעם אחת לעוגן").
4. Stats-rich + Hebrew + cited gov sources = GEO/AI-engine bait (skills/content-encyclopedia-glossary-plan.md §1).

### C. Israeli-specific MISSING pillars we can own:
- **התחדשות עירונית** (umbrella pillar) — we have 938 stub cards but no UMBRELLA pillar at the keyword. nadlanmaster doesn't dominate this.
- **מחיר למשתכן** — government program, periodic lotteries, high search volume. ⚠ Verify if dataset exists; if so, programmatic SEO play.
- **חוק מכר דירות** + **טופס 4** — definitional + legal pillars. nadlanmaster has a "termite extermination before tofes 4" page (URL `/termite-extermination-before-tofes4/`) — they barely touch the topic; we can own it.

### D. **DO NOT BUILD** (cannibalization risk vs our existing build):
- ❌ "בדיקת חוזה דירה" / "ביקורת חוזה דירה" → owned by `/contract-audit/`.
- ❌ "עורך דין מקרקעין" → owned by `/real-estate-lawyer/`.
- ❌ Per-city "דירות למכירה ב<עיר>" → /city/<city>/properties/ hub already covers it (v1.10.0).
- ❌ Per-city "קבלנים ב<עיר>" → /city/<city>/contractors/ hub already covers it.

### E. Foreign-market expansion — owner DECISION needed (banked):
nadlanmaster's strongest non-IL keyword grab. Per the rulebook §1 we're "quiet authority IL" → DON'T sprawl. But: Portugal/Cyprus/Greece are where many Israeli investors actually buy. Recommendation if owner wants in: build 1-2 (Portugal + Cyprus) as "השקעת ישראלים בחו"ל" angle (tax, regulation, repatriation), not as a brokerage. Reuse the directory/listing infra (CPTs are generic).

## 6. Mission for Lovable — verified Semrush-powered analysis

> **Why Lovable**: it has live **Semrush integration** (no separate Semrush account, free until 2026-08-15) — confirmed by Lovable docs. It can actually pull KD/volume/backlinks per keyword, which we can't from raw fetching. Use Lovable to convert our hypothesis (this skill) into **measured** keyword priorities.

**Paste this prompt to Lovable as a single message:**

```
ROLE
You are an SEO competitive analyst with access to live Semrush data (Lovable's
built-in integration — no separate Semrush account). Output structured findings
with verifiable Semrush metrics; flag everything you cannot verify.

GOAL
We are nad-lan.co.il (Israeli real-estate WordPress site). Our closest WordPress
competitor is nadlanmaster.co.il. We have already deeply analyzed nadlanmaster
by direct fetch (anatomy is in skills/nadlanmaster-anatomy-and-attack.md). I now
need you to MEASURE what we hypothesized.

TASKS (use Semrush for every number; mark anything unverified as [UNVERIFIED]):

1. Pull nadlanmaster.co.il in Semrush. Capture:
   - Authority Score, monthly organic traffic estimate, top 20 organic keywords
     with positions, search volume, KD, CPC, traffic share, intent label,
     and the landing URL for each.
   - Backlink profile summary (referring domains, top 10 anchors).
   - Top 10 traffic-driving PAGES (URL + estimated monthly visits).

2. Pull nad-lan.co.il (us) in Semrush. Same fields. Note: we are early-stage,
   numbers may be tiny. Don't pad — report zero where it is zero.

3. Keyword gap (Semrush "Keyword Gap" or equivalent):
   - Keywords nadlanmaster ranks for in top 20 that we don't rank for at all.
   - For each gap keyword: KD, volume, CPC, intent.
   - REMOVE gaps that match these EXISTING owned URLs of ours (cannibalization
     guardrail — these are OUR pages already, do not recommend rebuilding):
       /real-estate-lawyer/, /contract-audit/, /city/<city>/contractors/,
       /city/<city>/projects/, /city/<city>/properties/, /properties/,
       /projects/, /professionals/, /auctions/, /compare/.
   - Categorize remaining gaps by my pillar map:
       calculators (שווי, תשואה, מס רכישה, מס שבח, משכנתא),
       definitional/encyclopedia (Wikipedia-orphan Hebrew real-estate terms),
       התחדשות עירונית umbrella, מחיר למשתכן, קבוצת רכישה, חוק מכר/טופס 4,
       foreign markets (פורטוגל/קפריסין/יוון/אמירויות).

4. For each TOP-20 gap keyword, verify there is NO Hebrew Wikipedia article
   currently ranking on page 1 of Google (manual check). Mark which gap
   keywords have a Wikipedia void (these are highest priority — the owner
   specifically flagged this play).

5. Backlink analysis: nadlanmaster's top 25 referring domains. For each note
   whether it is Israeli, real-estate-relevant, and whether it is achievable
   for us (guest post, partner, directory). Be honest — most won't be.

6. Technical SEO comparison snapshot (Semrush Site Audit if available, or your
   own quick measurement): nadlanmaster vs us on Core Web Vitals, mobile,
   schema coverage, sitemap completeness.

DELIVERABLE
A single Markdown report with these sections:
  - Executive summary (3-5 bullets, honest)
  - nadlanmaster snapshot (table)
  - us snapshot (table)
  - Top-20 cannibalization-safe gap keywords with Semrush metrics + Wikipedia-void
    flag + suggested URL slug for us + my pillar/calculator/glossary bucket
  - Top-10 backlink targets we can realistically pursue
  - Technical gaps we should close
  - "Build now" prioritized list (rank by KD-vs-traffic ROI)

CONSTRAINTS
- Don't invent numbers. If Semrush says 0 or unknown, write that.
- Don't recommend keywords I already own (see TASK 3 exclusion list).
- Don't include foreign-market keywords by default — flag them as a separate
  block I will decide on.
- Hebrew SERP context matters; don't conflate global keywords with IL volume.
- Stay under 80 unverified claims; quality over volume.
```

## 7. Companion Cowork mission — when Lovable returns the report

```
PROMPT (for Cowork once Lovable returns the gap report)

CONTEXT
Lovable just produced a Semrush-grounded keyword/backlink gap report comparing
nadlan-lan.co.il vs nadlanmaster.co.il (see attached report). Combined with the
internal nad-lan rulebook (skills/nadlan-seo-content-design-monetization-rulebook.md)
and the existing 100-page inventory (skills/site-state.md cannibalization map),
your job is to convert the report into a build-ready content plan.

DELIVERABLE
A markdown plan with:
1. The top 10 cannibalization-safe pillars/spokes to build first (ranked by
   verified KD/volume ROI), each with: H1 (no SEO jargon, no AI-tells, no
   em-dash per rulebook §8.3), target_intent (rulebook §3.6), URL slug, the
   single pillar it feeds (silo per §6), and a 4-sentence original Hebrew
   intro that obeys §8 (no marketing, no superlatives, source-cited).
2. The top 20 Wikipedia-orphan glossary terms (from the report's Wikipedia-void
   flag) ready for the ChatGPT→Drive→Cowork→publish runbook (v3.2). Each with
   primary keyword, expected anchor-up pillar, source citation (gov.il / לשכת
   עוה"ד / רשות המסים).
3. A "do not build" list — gap keywords Lovable surfaced that DO cannibalize
   an existing page; explain why for each.

RULES
- Every recommendation must pass rulebook §12 quality gates.
- Quote Hebrew verbatim from Semrush; don't translate.
- Don't write the actual content here — only the brief. Content is built via
  the existing ChatGPT→Drive→Cowork batch runbook.
```

## 8. What we ship right now (no waiting on Lovable)

### v1.16.0 — tier paywall on directory cards (closes the leak)
Shipped this commit. Per the rulebook §10 Free/Pro/Premier model. Default = `free` with 30-day trial. Trial cards = full surfaces (taste); post-trial free cards = facts only (phone/email/photos hidden + "שדרגו לפרו" CTA). Pro = full surfaces. Premier = Pro + verified badge + priority sort. Admin meta box per card. Healthcheck reports per-tier counts. **This stops the "free links + free contacts" bleeding immediately**; the moment we import 14k contractors, none of them will get free advertising — they get a stub with their registry-confirmed name, and the value (contact + photos + leads) is gated.

### Pending owner decisions (banked):
- Pro/Premier monthly price (rulebook §10 leaves it open — typical IL benchmarks: ₪149-499/mo "Pro", ₪999-1999/mo "Premier").
- Free-trial length (default 30 days; can change via `NADLAN_FREE_TRIAL_DAYS`).
- Foreign-market expansion (Portugal/Cyprus only, or skip).
- Lovable account access — owner must paste the prompt in §6 into Lovable.

## 9. Honesty statement

This skill was built from **direct HTTP fetches of nadlanmaster.co.il, sub-sitemaps, and a sample project page** performed 2026-06-01, plus three live web searches (sources below). **No Semrush data was used here** — KD/volume/backlinks are claimed only where directly observable (URL counts from sitemaps). Anything beyond is hypothesis flagged as such; the Lovable mission in §6 is designed to convert hypotheses into measured numbers. nadlanmaster's revenue model is *inferred* from `/pirsum/`, `/pirsumi/`, the developer-specific category URLs, and the 3-form-per-project pattern — these are strong signals but not verified financials.

**Sources used:**
- Direct fetch: `https://www.nadlanmaster.co.il/`, `/sitemap_index.xml`, `/post-sitemap.xml`, `/category-sitemap.xml`, `/page-sitemap.xml`, `/robots.txt`, and the sample project page `/הרובע-הצפוני-הרצליה/`.
- Web searches: "nadlanmaster.co.il SEO strategy", "how to prompt Lovable AI for SEO competitive analysis 2026" (confirmed Lovable's Semrush integration is free until 2026-08-15), "real estate directory free vs paid listings monetization 2026" (confirmed 83% of top apps use freemium; basic browsing free, advanced features paid).
