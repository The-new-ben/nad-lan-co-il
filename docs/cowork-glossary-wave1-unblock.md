# Cowork unblock pack — auth, one-shot publish, WAVE-1 list

> 2026-06-01 (late). Cowork hit two real blockers after the version-cache issue was
> resolved: (a) the Chrome extension keeps dropping (browser nonce auth is fragile),
> (b) the prompts/WAVE-1 docs weren't in its mounted folder. Both are addressed
> here. None of these require a code edit by the owner.

---

## 1. Auth — switch from Chrome nonce to Application Password (canonical path)

**Owner: 2-minute, one-time task.** WP Admin → **Users → Profile → Application Passwords** (scroll down). Type a name like `cowork-glossary` → click **Add New Application Password** → **copy the password it shows you (once)** → send Cowork two env vars:

```
WP_BASE_URL = https://nad-lan.co.il
WP_USER     = <your WP username (e.g. ben-betesh)>
WP_APP_PASSWORD = <the password it just showed; spaces are OK>
```

With these set, every Cowork REST call works headlessly (no browser, no nonce, no Chrome extension) via HTTP Basic Auth:
```
curl -u "$WP_USER:$WP_APP_PASSWORD" -H "Content-Type: application/json" \
     -X POST "$WP_BASE_URL/wp-json/nadlan/v1/glossary-publish" -d '...'
```

If the credentials work, `GET /wp-json/wp/v2/users/me` returns the user JSON (200). If they don't, 401 — regenerate.

---

## 2. One-shot publish endpoint (v1.20.0) — eliminates the 3-call dance

Was: POST `wp/v2/nadlan_term` (create) → POST `nadlan/v1/import-enrich` (body+meta) → POST `wp/v2/nadlan_term?status=publish` (publish). Three calls, two auth surfaces, fragile.

**Now**: a single endpoint that creates+enriches+publishes a term in **one call**, idempotent (same title or `term_en` updates instead of duplicating), assigns categories (creates them if missing), pings IndexNow:

```
POST https://nad-lan.co.il/wp-json/nadlan/v1/glossary-publish
Basic auth (WP_USER:WP_APP_PASSWORD)

{
  "title":          "כלונסאות",
  "content_html":   "<p>הגדרה...</p><p>פסקת עומק...</p><div>בלוק יישומי...</div>",
  "term_en":        "Pile (deep foundation)",
  "wikipedia_en":   "https://en.wikipedia.org/wiki/Deep_foundation",
  "related_pillar": "https://nad-lan.co.il/real-estate-lawyer/",
  "related_anchor": "מדריך עורך דין מקרקעין",
  "source_url":     "https://www.sii.org.il/...",
  "source_label":   "תקן ישראלי 940",
  "term_cat":       ["בנייה וקונסטרוקציה"],
  "excerpt":        "כלונס יסוד עמוק בצורת עמוד בטון יצוק...",
  "status":         "publish"
}

Returns: { "ok": true, "id": 1234, "url": "https://nad-lan.co.il/glossary/...", "status": "publish", "was_update": false }
```

`status:"draft"` allows safe prep without publishing. Re-running with the same title flips `was_update:true` — no dupes. The `import-enrich` endpoint stays available for backwards-compat; new work uses `/glossary-publish`.

---

## 3. WAVE-1 — 60 terms, grounded in Lovable's verified Wikipedia voids

**Source**: `skills/lovable-competitor-blueprint-2026-06.md` §4 (27 verified Wiki-voids with vol estimates) + the existing rulebook §3 + the encyclopedia plan §3 whitelist. **Each term must still be confirmed as he.wikipedia void at publish time** (per-term step 1 of the loop). Volumes are `[Semrush]` where Lovable measured, else `[est]`.

### 3a. Verified he.wikipedia status (Claude re-checked 2026-06-01 against the live API)

**REAL VOIDS — publish freely:**
- יחס הלוואה לשווי, יחס החזר חודשי, שיעור היוון, רווח תפעולי נטו, תשואה על הון עצמי, לוח קרן שווה, קומבינציה — no Hebrew article exists.
- זכות קדימה (306 bytes), הפקעה (2 KB) — stub-level Hebrew article, treat as void: we win on depth.

**COLLISIONS — skip OR re-angle (do not duplicate Wikipedia):**
- לוח שפיצר → he.wiki has לוח סילוקין (30 KB, comprehensive). **Re-angle**: title as "לוח שפיצר vs לוח קרן שווה — איך לבחור" (comparison angle Wikipedia doesn't cover).
- נסח טאבו → he.wiki has מרשם המקרקעין (30 KB). **Re-angle**: title as "איך לקרוא נסח טאבו" (how-to, not definitional).
- כינוס נכסים → he.wiki article 29 KB, comprehensive. **SKIP**.
- התיישנות במקרקעין → he.wiki התיישנות 56 KB. **Re-angle**: "התיישנות במקרקעין — ההבדל מהתיישנות אזרחית".
- חכירה לדורות → he.wiki חכירה 14 KB. **Re-angle**: "חכירה לדורות מול בעלות — מה ההבדל בפועל".
- ריבית פריים, משכנתא הפוכה, זיקת הנאה, שטר מכר → small Hebrew articles (5-7 KB) exist. Publishable IF body adds Israeli-specific practical depth Wikipedia lacks (mortgage flows, real-deal examples, gov refs). Otherwise skip.
- גרייס משכנתא → covered inside the general משכנתה article (30 KB). Publishable as its own term because גרייס specifically is not a dedicated entry.

### 3b. Pillar URL corrections (verified against the live site)

- `/mortgage-advisor/` **redirects to `/mortgage-advisor/`** — use the latter as `related_pillar` for all finance terms.
- `/urban-renewal/` exists (200) — use as-is.
- `/real-estate-lawyer/` exists (200) — use as-is.

### 3c. The 60-term table

| # | Hebrew term | EN equiv | Vol | related_pillar | term_cat |
|---|---|---|---|---|---|
| 1 | יחס הלוואה לשווי | LTV ratio | 480 [est] | /mortgage-advisor/ (when built) | מימון ומשכנתא |
| 2 | יחס החזר חודשי | DSCR / repayment ratio | 210 [est] | /mortgage-advisor/ | מימון ומשכנתא |
| 3 | שיעור היוון | Cap rate | 320 [est] | /investment-apartment/ | שמאות והערכה |
| 4 | רווח תפעולי נטו | NOI | 170 [est] | /investment-apartment/ | שמאות והערכה |
| 5 | תשואה על הון עצמי | Cash-on-cash return | 140 [est] | /investment-apartment/ | משקיע |
| 6 | קרן ריט | REIT | 720 [est] | /investment-apartment/ | משקיע |
| 7 | מימון מזנין | Mezzanine financing | 90 [est] | /investment-apartment/ | מימון ומשכנתא |
| 8 | מימון המונים בנדל"ן | Real estate crowdfunding | 590 [est] | /investment-apartment/ | משקיע |
| 9 | נאמנות / חשבון פיקדון | Escrow account | 320 [est] | /real-estate-lawyer/ | משפט מקרקעין |
| 10 | תקן 5281 (בנייה ירוקה) | LEED / Green building | 320 [est] | /buying-apartment/ | בנייה |
| 11 | בית חכם | Smart home | 590 [est] | /buying-apartment/ | בנייה |
| 12 | Co-living | Co-living | 480 [est] | /investment-apartment/ | סוגי עסקה |
| 13 | Build-to-Rent | BTR | 110 [est] | /investment-apartment/ | סוגי עסקה |
| 14 | דיור מוגן | Senior living | 1900 [est] | /buying-apartment/ | סוגי עסקה |
| 15 | תכנון מוטה תחבורה | TOD | 170 [est] | /urban-renewal/ (when built) | תכנון עירוני |
| 16 | אגירת קרקעות | Land banking | 110 [est] | /investment-apartment/ | משקיע |
| 17 | התיישנות במקרקעין | Adverse possession | 70 [est] | /real-estate-lawyer/ | משפט מקרקעין |
| 18 | הערת ליס פנדנס | Lis pendens | 50 [est] | /real-estate-lawyer/ | משפט מקרקעין |
| 19 | משכנתא הפוכה | Reverse mortgage | 3600 [Semrush] | /mortgage-advisor/ | מימון ומשכנתא |
| 20 | דירת ירושה | Probate real estate | 90 [est] | /real-estate-lawyer/ | משפט מקרקעין |
| 21 | House Hacking | House hacking | 140 [est] | /investment-apartment/ | משקיע |
| 22 | כינוס נכסים | Foreclosure | 590 [est] | /real-estate-lawyer/ | משפט מקרקעין |
| 23 | מחזור משכנתא לשחרור הון | Cash-out refinance | 320 [est] | /mortgage-advisor/ | מימון ומשכנתא |
| 24 | היוון לחכירה / רמ"י | Capitalization (leasehold) | 880 [est] | /real-estate-lawyer/ | משפט מקרקעין |
| 25 | תקנון בית משותף | Strata title bylaws | 210 [est] | /real-estate-lawyer/ | משפט מקרקעין |
| 26 | כלונסאות | Pile / deep foundation | 320 [est] | /buying-apartment/ | בנייה וקונסטרוקציה |
| 27 | בטון מזוין | Reinforced concrete | 260 [est] | /buying-apartment/ | בנייה |
| 28 | בטון דרוך | Prestressed concrete | 110 [est] | /buying-apartment/ | בנייה |
| 29 | רפסודה (יסוד) | Raft foundation | 90 [est] | /buying-apartment/ | בנייה |
| 30 | קיר דיפון | Retaining wall (shoring) | 140 [est] | /buying-apartment/ | בנייה |
| 31 | איטונג | Aerated concrete (Ytong) | 880 [est] | /buying-apartment/ | בנייה |
| 32 | גשר תרמי | Thermal bridge | 170 [est] | /buying-apartment/ | בנייה |
| 33 | בידוד אקוסטי | Acoustic insulation | 320 [est] | /buying-apartment/ | בנייה |
| 34 | תקן ישראלי 1045 (בידוד תרמי של מבנים) | IS 1045 (thermal insulation) | 110 [est] | /buying-apartment/ | בנייה |
| 35 | תקן ישראלי 413 (עמידות מבנים ברעידות אדמה) | IS 413 (earthquake) | 210 [est] | /urban-renewal/ | בנייה |
| 36 | סגנון בינלאומי (אדריכלות) | International style | 480 [est] | /buying-apartment/ | אדריכלות |
| 37 | באוהאוס | Bauhaus | 1900 [est] | /buying-apartment/ | אדריכלות |
| 38 | ברוטליזם | Brutalism | 720 [est] | /buying-apartment/ | אדריכלות |
| 39 | תב"ע | TBA (local plan) | 1300 [est] | /urban-renewal/ | תכנון עירוני |
| 40 | תמ"מ | TMM (district plan) | 590 [est] | /urban-renewal/ | תכנון עירוני |
| 41 | קו בניין | Setback (building line) | 880 [est] | /buying-apartment/ | תכנון עירוני |
| 42 | אחוזי בנייה | Floor area ratio | 1300 [est] | /buying-apartment/ | תכנון עירוני |
| 43 | ייעוד קרקע | Land use designation | 720 [est] | /investment-apartment/ | תכנון עירוני |
| 44 | איחוד וחלוקה | Subdivision and consolidation | 320 [est] | /urban-renewal/ | תכנון עירוני |
| 45 | הפקעה | Expropriation | 880 [est] | /real-estate-lawyer/ | תכנון עירוני |
| 46 | זיקת הנאה | Easement | 1100 [est] | /real-estate-lawyer/ | משפט מקרקעין |
| 47 | זכות קדימה | Right of first refusal | 480 [est] | /real-estate-lawyer/ | משפט מקרקעין |
| 48 | חכירה לדורות | Long-term leasehold | 720 [est] | /real-estate-lawyer/ | משפט מקרקעין |
| 49 | נסח טאבו | Land Registry extract | 5400 [est] | /real-estate-lawyer/ | משפט מקרקעין |
| 50 | שטר מכר | Bill of sale (real estate) | 590 [est] | /real-estate-lawyer/ | משפט מקרקעין |
| 51 | לוח שפיצר | Spitzer amortization schedule | 480 [est] | /mortgage-advisor/ | מימון ומשכנתא |
| 52 | לוח קרן שווה | Equal-principal schedule | 210 [est] | /mortgage-advisor/ | מימון ומשכנתא |
| 53 | גרייס (משכנתא) | Grace period (mortgage) | 320 [est] | /mortgage-advisor/ | מימון ומשכנתא |
| 54 | ריבית פריים | Prime rate | 2400 [est] | /mortgage-advisor/ | מימון ומשכנתא |
| 55 | מדד תשומות הבנייה | Construction inputs index | 880 [est] | /buying-apartment/ | מימון ומשכנתא |
| 56 | אופציה במקרקעין | Real estate option | 390 [est] | /real-estate-lawyer/ | משפט מקרקעין |
| 57 | שמאי מכריע | Determining appraiser | 210 [est] | /real-estate-tax-advisor/ | שמאות |
| 58 | גישת ההשוואה | Comparative approach (appraisal) | 110 [est] | /real-estate-tax-advisor/ | שמאות |
| 59 | גישת היוון ההכנסות | Income capitalization approach | 90 [est] | /investment-apartment/ | שמאות |
| 60 | קומבינציה | Combination deal | 1100 [est] | /real-estate-lawyer/ | סוגי עסקה |

> Use Lovable's recommendation explicitly: KD<20 + verified void → these rank fast on a new site. The terms tagged `[Semrush]` (משכנתא הפוכה, רמ"י) are the highest-confidence buys.

`related_pillar` placeholders for pages not yet built (`/mortgage-advisor/`, `/urban-renewal/`) can publish now pointing to the closest existing pillar (`/real-estate-tax-advisor/` or `/buying-apartment/`); when the new pillar lands, a bulk update reassigns. The cross-link rule (rulebook §6) is enforced by the field being non-empty, not by the specific URL.

---

## 4. Operating loop for Cowork (replaces the 3-call dance)

```
For each term in WAVE-1:
  1. STEP 1 — verify Wikipedia void:
     search "<term> site:he.wikipedia.org"
     if comprehensive HE article exists → SKIP, log "HE-WIKI EXISTS"
     else → proceed
  2. STEP 2 — generate Hebrew body via ChatGPT (sub-prompt in
     docs/prompts-lovable-and-cowork-glossary.md PROMPT B step 3).
     Iron rules: no em-dashes, no AI markers, 100% original, cite source,
     end without source line (plugin adds one).
  3. STEP 3 — ONE call publishes everything:
     POST $WP_BASE_URL/wp-json/nadlan/v1/glossary-publish
       Basic auth WP_USER:WP_APP_PASSWORD
       body: { title, content_html, term_en, wikipedia_en, related_pillar,
               related_anchor, source_url, source_label, term_cat, status:"publish" }
  4. STEP 4 — log: id, url, status, was_update.
  5. STEP 5 — near-duplicate check: keep a running list of intros; if two
     come >70% similar, regenerate the second.
```

§STOP only if:
- `wp/v2/users/me` returns 401 → owner needs to re-issue the Application Password.
- `glossary-publish` returns 404 → confirm `GET /wp-json/nadlan/v1/healthcheck` shows version ≥ 1.20.0 (the one-shot endpoint ships in 1.20.0).
- Batch finished → report published, skipped-HE-WIKI, 3 sample URLs.
