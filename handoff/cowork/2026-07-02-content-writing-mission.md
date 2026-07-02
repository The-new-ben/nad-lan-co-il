# MISSION: Write and ship the content skeleton — systematically, one article per cycle

**To: Claude Cowork (you have real Chrome + PC + WP REST access).**
**Standing mission. Repeat the loop below until every skeleton is published. Do not stop after one article.**

## What you inherit (all live, verified 2026-07-02)
- **16 skeleton DRAFTS in WordPress, IDs 4960–4975.** Each draft already contains its WRITER BRIEF (gray box at the top: primary keywords, intent, parent pillar, sibling links) + an SEO-researched opening paragraph + an H2 outline. Master map + rules: `docs/content/2026-07-02-content-skeleton-architecture.md`.
- The EN foreign-investor cluster: pillar 4960 (`buy-property-israel-foreign-buyers`) + spokes 4961–4967. The HE gap spokes: 4968–4975, each bound to an EXISTING live pillar.
- Live hub-spoke map (do NOT re-target its keywords): `skills/internal-linking-hub-spoke.md`.
- Site: brand is now **נדלן** (never "נדלן חכם"). Owner is a licensed Israeli lawyer — use for E-E-A-T on legal/tax points ("נבדק על ידי עו"ד" pattern / "Reviewed by a licensed Israeli attorney").
- REST: `$WP_BASE_URL` + `$WP_USER` + `$WP_APP_PASSWORD` env vars (see `skills/agent-onboarding.md`). Read a draft: `GET /wp-json/wp/v2/posts/<id>?context=edit`. Update: `POST /wp-json/wp/v2/posts/<id>`.

## Work order (strict)
1. **4960 (EN pillar)** — must publish first; spokes link into it.
2. 4962 (mortgage non-residents) → 4961 (purchase tax) → 4963 (money transfer/AML) — highest commercial intent.
3. 4964 → 4965 → 4966 → 4967 (rest of EN cluster).
4. 4968 (מחירי דירות 2026) → 4969 (איך למכור דירה) — HE volume leaders.
5. 4970 → 4971 → 4972 → 4973 → 4974 → 4975.

## The per-article loop (repeat verbatim for every draft)

### Step 1 — REAL SERP research in Chrome (the Blueprint, strategy-master.md §13)
Open Google in Chrome (google.com in the article's language; for EN use US/UK results without IL personalization where possible):
1. Search the PRIMARY keyword from the draft's brief. Screenshot the SERP.
2. Record: the 10 organic titles + URLs; featured snippet (who + format); People-Also-Ask questions (open each once to expand more); "Related searches"; autosuggest completions for the keyword stem; SERP TYPE (guides? calculators? gov pages? forums?) → this defines the intent you must match.
3. Open the TOP 3 organic competitors. For each note: word count (rough), H2/H3 backbone, what data/tables/tools they include, what they ALL miss (your differentiator), their title formula.
4. Repeat quickly (steps 1–2 only) for the 2nd/3rd keywords in the brief.
5. Write a 10-line SERP BLUEPRINT: intent, required backbone (the shared H2s), differentiators we will add (3D showrooms, our calculators, lawyer review, gov.il datasets), the PAA questions to answer as an FAQ, the title we will use (beat the best competitor's formula, ≤60 chars, primary keyword first).

### Step 2 — Build the ChatGPT prompt and generate
Construct a prompt to ChatGPT containing: the SERP blueprint; the draft's existing brief + outline (adjust outline per blueprint — blueprint wins); language + audience; **hard rules**: minimum 3,000 words; NO em-dash (U+2014) anywhere - use comma / colon / short hyphen; NO AI-tell phrases (the forbidden lists in `skills/copywriting-skill.md` §3–4 - paste them into the prompt); no invented numbers - only figures you supply from official sources (רשות המסים, למ"ס, בנק ישראל, gov.il — collect the real 2026 numbers in Chrome during Step 1 and PASTE them into the prompt); factual, benefit-led, no hype ("once in a lifetime" is banned); short paragraphs, tables where data compares, an FAQ section answering the PAA questions verbatim; output clean HTML (h2/h3/p/table/ul only).
Review the output YOURSELF before using: grep for `—`, scan for forbidden phrases, verify every number against your Step-1 sources. If it fails, regenerate the failing sections.

### Step 3 — Publish into the existing draft (never a new post)
`POST /wp-json/wp/v2/posts/<id>` with the final HTML as `content` (REPLACE the brief box + outline entirely), keep the existing slug/title unless your blueprint produced a stronger title (then update `title` too — never the slug).
Then wire it:
- Internal links inside the body: parent pillar (exact-match anchor, once), 2 siblings from the brief, ≥1 calculator/tool, ≥1 money surface (/projects/, /properties/ or /professionals/). EN articles must link the 3D showroom projects (that is our proof-of-trust differentiator).
- Append the spoke back-link block per `skills/internal-linking-hub-spoke.md` (the `nadlan-spoke-backlink-v1` pattern) and, when a pillar gains a new spoke, append the spoke's link to the pillar's related-articles block.
- Yoast: set focus keyword = first primary keyword, meta description ≤156 chars containing it (write it yourself, compelling).
- Set `status: publish` ONLY after the QA gate below passes.

### Step 4 — QA gate (all must pass before publish)
[ ] ≥3,000 words · [ ] zero U+2014 · [ ] zero forbidden phrases (grep §3–4 lists) · [ ] every number has a named official source in-text · [ ] E-E-A-T line present on legal/tax topics · [ ] all 5+ internal links resolve (curl each) · [ ] title ≤60 chars w/ primary keyword · [ ] FAQ answers real PAA questions · [ ] renders correctly (open the preview URL in Chrome, screenshot desktop+mobile) · [ ] does NOT target any keyword owned by a live page (check the hub-spoke map).

### Step 5 — Log and continue
Append one line to `docs/content/2026-07-02-content-skeleton-architecture.md` under a "## Shipped log" heading: date, ID, slug, final word count, focus keyword, SERP notes location. Commit via the repo flow (branch → PR → merge, see `AGENTS.md`). Then take the NEXT draft in the work order. Do not wait to be asked.

## Hard boundaries
- Never delete/replace a live published page. Never create new slugs for these topics — the drafts reserve them.
- If a SERP reveals the keyword is owned by an existing live page of ours → STOP that article, log the conflict in the doc, move to the next.
- Demo content (listings/professionals marked לדוגמה) is never cited as real.
- Publishing cadence: quality over speed, but the mission is "days, not months" — one full loop per session minimum.
