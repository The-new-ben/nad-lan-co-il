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
