# GSC findings package × city-purge cross-analysis — 2026-08-25 (evening)

Input: the owner's independent findings package (another agent, OAuth API pull,
data range 2026-05-27..2026-08-23, PRE-purge) at
`C:\Users\777\Documents\GSC-Data\deliverables\nad-lan-gsc-findings-2026-08-25.zip`
(SHA-256 verified a8ff46c3…, 238 files, 7,622 QA checks passed, zero
direct-vs-daily mismatches). This doc records the cross-analysis against the
same-day city-layer purge (see RECEIPT-CITY-PURGE-2026-08-25.md) and the agreed
treatment queue. Analysis script: session scratchpad analyze003.py.

## Headline cross-result [code]

Of 457 likely+possible cannibalization groups (951 multi-URL queries total):

| bucket | groups | impressions | status |
|---|---:|---:|---|
| involve /city/, /cities/ or ?city= | **192** | **7,421** | **RESOLVED by tonight's purge** (410 + trash + GSC removals) |
| http-vs-https same path | 35 | 2,286 | 308 already live; time heals; re-check 1.10 |
| numeric-suffix (-2/-3) dupes | 4 (+4 more in other classes) | ~50 | REAL — forensic + merge queue below |
| other (intent overlaps) | 226 | 3,129 | treatment queue below |

P0_CANNIBALIZATION_REVIEW pages: 257 → 83 were city-layer (gone), 174 remain.
Not-in-sitemap URLs: 250 → 199 were city-layer (gone), 51 remain
(38 real pages + 11 parameterized + 2 http).

## Treatment queue (owner GO required per lane)

### A. Small technical deploy (one snippet-swap round)
1. **robots.txt: block the PMS action params** — `/?pms_user=…&pms_action=pms_delete_user…`
   is INDEXED and收 impressions on שדה דב money queries ("דירות בשדה דב" 85,
   "דירות למכירה בשדה דב" 84). Add `Disallow: /*?pms_action=` +
   `Disallow: /*?pms_user=` via robots_txt filter. (Was already proposed and
   owner-ok-pending on 18.8; now has hard evidence.)

### B. Import-duplicate forensic → merge (7 pairs, each needs eyes before trash)
| query (impr) | keep-candidate | dupe-candidate |
|---|---|---|
| אגבאריה מוחמד (6) | professionals/אגבאריה-מוחמד-2 | professionals/אגבאריה-מוחמד-3 (or vice versa) |
| מגדל רוטשילד בת ים (7) | projects/מגדל-הים-רוטשילד-2 (stronger) | projects/רוטשילד |
| גני שפירא (4) | projects/שפירא | projects/שפירא-3 |
| פרויקטים חדשים באבן יהודה (20+26) | projects/העצמאות-3 ↔ real base? | forensic |
| פרויקטים חדשים באילת (7) | projects/אילת-2 | (no base seen — rename review) |
| מגדל גפן (5) | projects/הגפן | projects/מתחם-הגפן-1-4 |
| תוכנית ל (23, benign) | projects/צהל-2 | verify only |
Plus 65 P2_REVIEW_DUPLICATE_PATTERN URLs with no GSC signal — sweep later.

### C. Intent differentiation (content edits, no deletions)
1. **מחשבון משכנתא הפוכה (308 impr)**: parent `/mortgage-calculator/` competes
   with child `/mortgage-calculator/reverse-mortgage/`. Parent gets exact-anchor
   link "מחשבון משכנתא הפוכה" → child; keep "הפוכה" wording OUT of parent title.
2. **דירות להשקעה (172) + נכסים להשקעה (89)**: `/investment/` vs
   `/investment/apartments-for-investment/` — same parent-child pattern.
3. **זכויות בנייה (103)**: glossary term vs `/property-value/building-rights-check/`
   tool — tool title says בדיקה, glossary links the tool.
4. **בדיקת נסח טאבו (83)**: `/tabu-extract-check/` tool vs 2 glossary terms — same fix.
5. **מכירת דירה family (157+151+129+76)**: selling vs buying vs investment —
   mostly http/https + adjacent intents; after A+http-healing re-review.

### D. Frozen / watch only
- **DUO (240+235+99 impr)**: he-base vs -fr/-ru siblings surface on "duo tel aviv";
  hreflang review candidate — DUO IS FROZEN (HAD-200) until the owner's word.
- שדה דב hub vs merkaz (100) — wave-1 titles/links already shipped; watch.
- http/https 35 groups — no action possible beyond existing 308 (no new redirects law).

### E. Inventory hygiene (later lane)
- 38 real pages absent from sitemap incl. `/purchase-tax/`,
  `/residential-lease-agreement/`, `/global/italy|miami|new-york/`, 2 glossary
  terms — find why (indexability/exclusion) and fix.
- `/duo-preview/` publicly reachable — flag to owner (exposure).
- `/site-map/` + `/sitemap/` HTML junk pages rank for a Spanish query; review.
- `/projects/page/2/` pagination remnant (owner law: no pagination).
- 1,691 P2_GSC_OPPORTUNITY pages = the long-game refresh queue.

## GSC API access — ESTABLISHED (owner order, same evening)

- Tools in repo: `tools/gsc/gsc_api.py` (zero-dependency python: sites /
  sitemaps / query with pagination+CSV / totals) + the package's node tooling
  (needs `npm i googleapis`).
- Secrets stay at `%USERPROFILE%\Documents\jus-tice-secrets\gsc\` — now
  deny-listed in .claude/settings.json like the WP secrets. Never print/commit.
- Verified live [code]: token refresh ok, scope `webmasters.readonly`,
  sc-domain:nad-lan.co.il = siteOwner; sample final-7d (16-22.8):
  123 clicks / 16,110 impressions / pos 25.8 (3-month baseline was pos 31.4).
- **Scope limit**: token is READ-ONLY. API sitemap-submit would need a one-time
  interactive full-scope consent by the owner; the UI path (done today) covers it.
- CLAUDE.md now carries the access block; memory: nadlan-gsc-api-access.
- **Same evening, owner order "full access": FULL webmasters scope obtained**
  via loopback OAuth consent driven through the owner's Chrome
  (gsc-token-full.json; the readonly token untouched). Proven by an API
  sitemap submit: lastSubmitted 2026-08-25T18:03Z, errors=0. gsc_api.py now
  prefers the full token and gained `submit-sitemap`.

## F. URL word-duplication audit (owner law 25.8; tool: tools/gsc/url_word_audit.py)

Live-sitemap scan, 4,372 URLs [code]:

- **93 URLs repeat a word inside their own path.** Clusters: 22× `/investment/{city}-investment-apartment/`,
  20× `/commercial-real-estate/commercial-*`, 7× `/mortgage-calculator/mortgage-*`,
  7× `/short-term-rentals-abroad/short-term-rentals-*`, guide children repeating
  parent names (buying-apartment, real-estate-lawyer), ~15 benign Hebrew
  person/project names (בן-משה-משה style).
- **Discovery:** `/new-projects/new-projects-tel-aviv/` and
  `/new-projects/north-tel-aviv-new-projects/` are surviving city-project-intent
  pages OUTSIDE the purged /city/ layer — they compete with /projects/ on the
  exact head queries (the 163-impr "צפון הישן" group's extra URLs). Added to the
  phase-2 intent-map review: guide keeps guide-intent wording, /projects/ owns
  the category phrase.
- Cross-URL token pressure (awareness, not deletion): real/estate 105 URLs,
  apartment 100, tel/aviv ~75, commercial 74, prices 67, new 57 — mostly the
  guide clusters + the professionals name directory (natural). `demo` appears in
  22 sitemap URLs — hygiene review item.
- Standing law recorded as CLAUDE.md iron law 9: one word = one owner URL; no
  double words in a URL; audit before minting any slug; no retroactive renames.

## G. Per-page verdicts — **REVISED after owner review + eyes (late 25.8): NO deletions for now**

The owner caught two real errors in the first draft below, verified with eyes:
1. **Demo pages are the SEED of the listings sections** — 7 of the 8 catalog
   properties are demo; deleting them empties /properties/. They stay until real
   listings replace them (0 impressions = zero SEO harm meanwhile).
2. **/sitemap/ + /site-map/ are NOT junk** — eyes show a DESIGNED human hub
   ("כל מה שיש בנדלן במקום אחד", stat tiles + section cards; the footer links it).
   The inventory's word_count=33 misread a dynamic page. Real issue is only that
   the SAME hub answers on TWO URLs → dedup to one canonical URL, no deletion.
Also eyes-verified: the /investment/ city pages are QUALITY long-form articles
(market data, advice boxes, internal links) with no parameters — their zero
impressions is a discovery problem, not a content problem. Deleting quality
pages was premature; the work is internal links + the root↔apartments-for-investment
merge (content op, owner GO). Guides stay unless they actively harm. The
original draft verdicts below are kept for the record only.

**DELETE-LIST (45 pages, awaiting the owner's GO):**
- 22 `demo` pages (15 fabricated professionals + 7 fabricated property listings,
  ~20 words each, 0 impressions — honesty-law violations sitting in the sitemap).
- 16 `/investment/{city}-investment-apartment/` pages with **0 impressions AND
  0 clicks** (ashdod, bat-yam, beer-sheva, haifa, hod-hasharon, holon, jerusalem,
  kfar-saba, kiryat-ono, modiin, petah-tikva, raanana, rehovot, rishon-lezion,
  where-to-buy, investment-via-company) — 3-5K words each, Google ignored them.
- 5 zero/zero guides: mortgage-calculator/bridge-loan-apartment,
  real-estate-lawyer/when-real-estate-lawyer-required,
  real-estate-tax-advisor/capital-gains-tax-guide + purchase-tax-investor.
- `/sitemap/` (33 words, 93 impr) + `/site-map/` (120 impr, pos 78) — junk HTML
  sitemaps outranking real pages on stray queries.
- PLUS one merge-delete: `/investment/apartments-for-investment/` (522 impr,
  pos 43) folds INTO `/investment/` root (2,644 impr) → one owner for
  "דירות להשקעה", then the child is trashed.

**KEEP (owner invited push-back; the evidence):**
- `/commercial-real-estate/` shelf: **37 clicks** (management-fees 11,
  brokerage-fee 6, port/office/shop price pages 1-4 each at pos 5-8) — the only
  guide shelf that already EARNS; deleting it burns real traffic.
- 6 investment-city pages WITH impressions at pos 4.7-8 (ashkelon 88, netanya 18,
  ramat-gan 15, givatayim 13, ramat-hasharon 9, herzliya 7) — ranking well on
  tiny-volume niches; re-judge at the 1.10 checkpoint, cut then if still 0 clicks.
- `/new-projects/new-projects-tel-aviv/` (178 impr, **pos 10.8**, P1_PROTECT) —
  the best-positioned TLV city asset left; hold for the phase-2 intent map
  (candidate to become the future TLV page). north-tel-aviv-new-projects
  (262 impr, pos 53) decided in the same review.
- `/short-term-rentals-abroad/` (8 pages, pos 4-7) — the international shelf
  backing the developer-recruitment pitch; unique tokens, no collision.
- `/investment-apartment/tel-aviv-investment-neighborhoods/` (159 impr, pos 10,
  protected) — kept; its near-empty section root is a phase-2 fold (child URL
  depends on the parent path — cannot trash the parent alone).

## I. Round 2 EXECUTED (owner GO, 25.8 night) — evidence classes inline

1. **robots.txt pms-block LIVE** [code+eyes]: the site serves a PHYSICAL
   robots.txt (nginx static, Last-Modified 2.6.2026) — the WP `robots_txt`
   filter never fires (the one added to smart-404.php in 1.72.220 stays as
   dormant fallback). The physical file was patched via snippet (ABSPATH jail,
   `.bakC2` sibling, md5 in/out): `Disallow: /*?pms_action=` +
   `Disallow: /*?pms_user=` inside the UA group; HTTP-verified.
2. **Duplicate forensic — the evidence gate did its job** [code]:
   trashed (backup dupes-export-2026-08-25.json, both verified 404):
   `professionals/אגבאריה-מוחמד-2` (id 2769; identical name to the stronger -3)
   and `projects/רוטשילד` (id 1070; same city בת ים as the stronger
   מגדל-הים-רוטשילד-2). **NOT touched — different real projects sharing street
   names**: שפירא (קרית ים) vs שפירא-3 (גדרה); הגפן (ירושלים) vs מתחם-הגפן-1-4
   (כפר סבא); העצמאות (אור יהודה), אילת (רמת השרון), צה"ל (קרית ים) all have
   distinct bases. Lesson: the -N suffixes are mostly WP slug collisions of
   street-named projects across cities, NOT import corruption.
3. **GSC deep sweep** [code+eyes]: coverage (UI, data to 21.8): 3.11K indexed /
   2.92K not — 914 404s, 557 noindex, 218 canonical-alternate, 55 redirect,
   **1,115 Discovered-not-indexed**, 53 Crawled-not-indexed. URL Inspection API
   over 26 money pages: **25 PASS** (all fleet+tools+investment pages indexed;
   several investment pages re-crawled 25.8 after the sitemap resubmit). The ONE
   failure: `/construction-engineering-guide/` (the owner's 10.9K-word article,
   live 22.8) — never crawled. It IS in page-sitemap.xml (verified) →
   **Request Indexing pressed via the owner's Chrome; "Indexing requested —
   priority crawl queue" confirmed on screen.**
4. **Standing WATCH list** (owner: "check all the time"): investment cluster +
   TLV pages consolidation decision (owner undecided — re-judge 1.10);
   the 1,115 discovered-not-indexed pool; removals still "Processing";
   engineering-article indexing; sitemap/site-map dedup pending owner ok.

## H. GSC access made GLOBAL (owner order: every session, every project)
- Global user-level `C:\Users\777\.claude\CLAUDE.md` created — loads in EVERY
  project on this machine: full-access declaration law, secrets paths, tool
  usage, the full property list the token covers (10 properties, siteOwner).
- Tools copied to the repo-independent home:
  `C:\Users\777\Documents\GSC-Data\tools\{gsc_api.py, url_word_audit.py}`.
