# Directory Listings Project — PLAN / KNOWLEDGE ONLY (build deferred)

> **Status: MAP ONLY. Do NOT build yet.** Owner brief 2026-06-01. This is recorded knowledge for later execution (likely via Cowork + ChatGPT, like the article batches). It is also intended to be a **reusable skill for the next project, Justice.co.il** — capture patterns generically, not nad-lan-only.

---

## 1. The idea (owner's words, distilled)

Build a **free directory of listing "cards"** covering, exhaustively:
1. **Every real-estate PROJECT in Israel** (new developments / פרויקטים), small to big.
2. **Every CONTRACTOR / builder in Israel** (קבלנים), small to big.

Each entity gets a **free card opened automatically** by us (they don't ask for it). The card is a **mini-Wikipedia page**: highly informative, original (NOT copied), rich with **statistics and numbers** (AI engines and Google reward this as a knowledge source → E-E-A-T / authority signal).

The free card is a **teaser**: enough to rank and be found, but to get pictures / richer content / editing, the entity must **CLAIM** the card → register as owner → upgrade → then they can upload photos, edit, post updates, and use it as a **marketing platform**.

This is a **lead-gen + SEO land-grab**: own the search real estate for "[project name]" and "[contractor name]" before anyone else, then convert owners into paying/registered users when they discover their own card.

---

## 2. Why it works (the SEO / AI thesis)

- **Long-tail domination:** thousands of entity pages (project names, contractor names) = thousands of low-competition queries we can own. Nobody else has a complete, structured, original index.
- **Knowledge-source authority:** original, stats-rich pages read as a *reference* (Wikipedia-like) → Google + AI answer-engines cite/prefer them. Numbers + structured data = AI-friendly.
- **Claim funnel:** the entity finds its own card ranking #1 → wants control/pictures → claims → registers → upsell. Zero cold outreach; the SEO does the selling (same insight as the contract-audit research: *show up where they search*).
- **Compounding:** every claimed card adds owner-supplied fresh content (photos, updates) → more ranking signal.

---

## 3. HARD CONSTRAINT — no keyword cannibalization

**Iron rule (same as the encyclopedia/glossary plan):** never target an existing focus keyword owned by a pillar/spoke/city/tool page.
- Cross-check every card slug + focus keyword against the **100-page slug+focus-keyword inventory** (the cannibalization map captured 2026-06-01, see site-state.md).
- Entity cards target **entity-name intent** (`"[שם פרויקט]"`, `"[שם קבלן] ביקורות"`), which is *navigational/branded* — distinct from the informational pillars and the transactional product pages. That separation is what keeps it safe, but VERIFY per batch.
- Distinct CPT + URL namespace so it can't collide: reuse the existing **`project`** and **`professional`** catalog CPTs (already registered in `plugins/nadlan-config/nadlan-config.php`). Likely URLs: `/projects/{slug}/`, `/contractors/{slug}/` — confirm against inventory before minting.

---

## 4. Content generation pattern (reuse the article-batch machinery)

Mirror the proven Cowork + ChatGPT pipeline (see runbook-cowork-article-batch-v3.md):
1. **Scrape** source material per entity (project/contractor): public data, registry info, addresses, project sizes, unit counts, completion years, etc. **Only public data; mark unknowns, never invent** (same honesty discipline as the competitor research).
2. **Feed to ChatGPT** to produce an **original, non-copied, informative** page (Wikipedia-style): overview, key facts table, **statistics/numbers**, location, status. Not a paraphrase of one source — synthesise.
3. **Publish** as a `project` / `professional` CPT entry with schema (see §6).
4. **Claim CTA** on every card.

> Same anti-AI-tell + word-floor + duplicate-H2 discipline as the article runbooks applies.

---

## 5. The claim-to-upgrade mechanic

- **Free (default, system-created):** name, location, key public facts, stats, one map, claim CTA. Read-only.
- **Claimed / registered owner:** verify ownership (email/phone/registry match) → unlock editing: upload photos, edit description, post updates/news, add contact, mark "verified owner". This is the marketing-platform upgrade.
- **Verification** is the trust gate — define how an owner proves they own the project/contractor entity (avoid hijacking). TBD at build.
- Ties into the existing lead/registration infra (nadlan_lead CPT, lead REST endpoint) — extend, don't reinvent.

---

## 6. Schema / structured data (the AI-assertiveness lever)

- Projects: `RealEstateListing` / `Residence` / `Place` + `Organization` (developer) — with numeric properties (units, floors, year, price range where public).
- Contractors: `Organization` / `LocalBusiness` (+ `Contractor` where applicable) — founding date, area served, project count, `aggregateRating` once reviews exist.
- Stats rendered as on-page facts tables AND mirrored in JSON-LD → maximises machine-readability.

---

## 7. Optional expansion (owner floated, lower priority)

- **Biggest global contractors** as knowledge/reference articles — pure authority/E-E-A-T plays that lend the domain topical assertiveness. Same "knowledge source + stats" formula. Only if it doesn't dilute the Israeli core or cannibalize.

---

## 8. Execution notes / sequencing

- **Build deferred.** Per owner: also still pending = hands-on testing with Cowork; and the contract-audit product build; and (lowest priority) the contact-button fix.
- When built, **scraping + content-gen likely delegated to Cowork** (per-entity, ChatGPT-authored), same as article batches.
- Scale concern: thousands of pages — plan for batched generation, indexing budget (IndexNow auto-ping already in plugin), and avoiding thin-content penalties (each card must clear a real informativeness/stats bar, not a stub).

---

## 9. REUSE → Justice.co.il (owner directive)

Owner: *"the next project will be Justice.co.il, and we need to use these skills — not start from scratch."*
- This directory pattern (free-card land-grab → claim → upgrade → marketing platform), the Cowork+ChatGPT original-content pipeline, the cannibalization guardrail, and the schema/stats authority approach are **generic and portable**. Keep this skill provider-agnostic so Justice.co.il can adopt it directly (swap entity types: e.g. legal entities/lawyers/courts/topics instead of projects/contractors).
- **Standing instruction:** keep recording all research, patterns, and knowledge into `skills/` as we go — these are the reusable asset for the next project.
