# URL Namespace Contract — collision & cannibalization prevention

> **Why this exists.** The owner asked us to be "100 steps ahead" so that as this site (and
> the sibling sites) grow content, agents do NOT create URL collisions, slug messes, or
> keyword cannibalization that tangle SEO later. This is the law every agent (Claude, Codex,
> Cowork, Gemini, ChatGPT-via-browser) follows **before publishing or renaming anything**.
>
> This is **portable DNA** — reuse on every site in the network; only the niche-specific
> pillar list changes.

---

## 1. The slug law (non-negotiable)

1. **Latin only.** Slugs are lowercase ASCII `a-z 0-9 -`. **No Hebrew in slugs, ever.**
   Hebrew slugs break reports, analytics, CLIs, and exports. (The page TITLE stays Hebrew —
   only the URL is Latin. Title and slug are independent.)
2. **Concept, not sentence.** The slug is the *thing*, not a headline or question.
   - ✅ `/glossary/land-registry-extract/`   ❌ `/glossary/how-to-read-the-tabu-extract/`
   - ✅ `/glossary/cap-rate/`                 ❌ `/glossary/cap-rate-vs-yield-how-to-choose/`
3. **One concept = one URL.** Never create a second page for the same concept/keyword.
   Before publishing, **search the existing slug space** (see §4). If it exists, expand the
   existing page; do not make a rival.
4. **Renaming a slug = automatic 301.** WordPress stores the old slug in `_wp_old_slug` and
   301-redirects it. So slug cleanups are safe and reversible. Always VERIFY the old URL
   returns 301 → new URL after a rename (we did this for all 22 glossary terms 2026-06-02).
5. **Never reuse a retired slug** for a different concept (it would hijack the old 301).

---

## 2. The namespace map — what path belongs to what

Each content type owns a path prefix. **Do not cross the streams.**

| Path prefix | Content type | Indexing | Who publishes |
|---|---|---|---|
| `/glossary/<concept>/` | `nadlan_term` — short, single-concept definitions, each uplinking to ONE money pillar | indexable IF ≥350w + enriched, else `noindex` | content agent (clean concept slug) |
| `/<money-pillar>/` | cornerstone money pages (e.g. `/mortgage-advisor/`, `/investment-apartment/`, `/real-estate-tax-advisor/`) | indexable, canonical, the keyword owners | human-reviewed |
| `/guides/<topic>/` *(reserved)* | long how-to / comparison articles (the "vs", "how to", "step by step") — these must NOT live in `/glossary/` | indexable | content agent |
| `/city/<city>/<facet>/` | geo hubs (contractors/projects per city) | indexable only ≥ card floor, else noindex/404 | `city-hubs.php` (auto) |
| `/professionals/`, `/projects/`, `/properties/` | directory archives (premium AJAX) | indexable landing; entity stubs `noindex,follow` | `directory.php` (auto) |
| `/professionals/<name>/`, `/projects/<name>/` | entity profiles | `noindex` until claimed/enriched | importer (auto) |
| price/city guides (`/<city>-apartment-prices/`) | informational price pages | indexable | content agent |

**Rule:** a "vs / how-to / comparison" piece is a **guide**, not a glossary term. A glossary
term is a definition. If a draft is >600 words of process, it belongs in `/guides/` or under
a pillar — never `/glossary/`. This is what keeps the glossary a glossary.

---

## 3. Cannibalization prevention (the keyword-ownership rule)

1. **Every commercial keyword is owned by exactly ONE pillar.** Maintain the owner map in
   `internal-linking-hub-spoke.md`. Before writing for a keyword, check who owns it.
2. **Glossary terms target definitional long-tail only** ("מה זה X", "X הסבר"), never the
   commercial head term. Each term links UP to its owning pillar (anchor = the pillar's
   keyword), passing equity to the pillar, not competing with it.
3. **Spokes link up to their pillar; pillars link down to spokes.** No spoke targets the
   pillar's head keyword.
4. **If two pages start ranking for the same query**, merge them (301 the weaker into the
   stronger) — do not let them split equity. Audit quarterly with `site:` + Search Console.
5. **Noindex is a feature.** Thin/auto-generated entity pages stay `noindex,follow`
   (`schema.php` guard). They pass link equity without competing for keywords. Do not "fix"
   them into the index unless they become genuinely unique + valuable.

---

## 4. Pre-publish checklist (run EVERY time, any agent)

```
1. Decide the concept + its ONE canonical keyword.
2. Check ownership: does a pillar already own this keyword? (internal-linking-hub-spoke.md)
   - yes → expand that pillar / write a spoke that links up. Do NOT make a rival page.
3. Check slug collision (REST, 5 seconds):
   GET /wp-json/wp/v2/<type>?slug=<proposed-latin-slug>
   GET /wp-json/wp/v2/search?search=<concept>
   - any hit → expand the existing URL, do not duplicate.
4. Pick a Latin concept slug per §1. Confirm it's in the right namespace per §2.
5. Set the canonical to self. Set noindex if it doesn't meet the quality floor.
6. Add the up-link to the owning pillar (for spokes/terms).
7. Publish. VERIFY live: 200 on new URL, one H1, Hebrew body, no internal/CRM language.
8. If you renamed an existing slug: VERIFY the old URL 301s to the new one.
```

---

## 5. Canonical & indexing policy

- **Every indexable page declares a self-referential canonical.** (Open item: some
  `nadlan_project` / `nadlan_professional` pages currently lack one — fix via Yoast config
  or a single-source canonical, NOT a second canonical on top of Yoast. Never emit two
  canonicals.)
- **One H1 per page.** Archive/profile templates that produce a second H1 (site logo as H1)
  must demote the logo to non-H1 at the theme/template level — not via fragile regex on
  rendered HTML.
- **Schema: one source.** Yoast owns page-level schema (WebPage/Article/Breadcrumb). Our
  plugin adds only entity-specific graphs (ItemList, AggregateRating, DefinedTerm) that
  Yoast doesn't. Never duplicate a graph Yoast already emits.

---

## 6. Agent division (who touches URLs)

- **Content agents** (Cowork/ChatGPT/Gemini/Codex-content): create pages following §1–§4.
  Latin slugs only. Never invent a rival to an existing keyword owner.
- **Structural agent** (Claude / reviewed code): owns the rendering modules
  (`directory.php`, `archive-grid.php`, `reviews.php`, `city-hubs.php`, `schema.php`) and
  any slug/redirect/canonical *mechanics*. Plugin code merges to `main` only after review.
- **Nobody** edits another agent's module in a parallel branch.

---

## 7. Public route / module sign-off rule

Do **not** create new public routes/pages or edit existing plugin modules without Claude +
owner sign-off on the URL and the module owner.

Research, specs, audits, and docs are the safe green-light lane. Plugin code goes through
Claude review. If a public page may overlap an existing intent, stop and decide the canonical
URL first.

---

## Revision log
- 2026-06-03 — Added the public route/module sign-off rule after the parked `/advertise/`
  build revealed a potential collision with the live `/join-pro/` package page.
- 2026-06-02 — Created (Claude). Triggered by: 22 glossary terms migrated from Hebrew
  sentence-slugs to clean Latin concept slugs (all old URLs 301 → new). Establishes the
  namespace map + cannibalization rules so future content (guides, more terms, city pages)
  never collides. See `docs/glossary-slug-migration-2026-06-02.md` for the migration record.
