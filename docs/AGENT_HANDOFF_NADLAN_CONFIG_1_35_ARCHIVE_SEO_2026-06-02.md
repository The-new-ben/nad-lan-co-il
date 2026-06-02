# Agent handoff - nadlan-config v1.35.0 archive SEO polish

Date: 2026-06-02
Agent: Codex
Branch: `codex/nadlan-config-1-35-archive-polish`
Base: fresh branch from `origin/main`
Version coordination: `origin/main` was `1.34.0`; this branch reserves `1.35.0`.

## Read first

- `AGENTS.md`
- `skills/codex-plugin-access-and-deploy.md`
- `skills/article-qa-audit.md`
- `skills/google-blueprint-workflow.md`
- `skills/nadlan-config-plugin.md` for history only. The current deploy source of truth is `skills/codex-plugin-access-and-deploy.md`.
- `skills/SKILLS-TREE.md`
- `skills/README.md`
- `skills/site-state.md`
- `skills/copywriting-skill.md`

## Plugin issue - critical context for Claude Code and all agents

The owner explicitly asked why source changes do not always appear live. The answer is now documented and must be repeated in handoffs:

- The plugin source lives in `plugins/nadlan-config/`.
- The live site does not run raw repo source directly.
- Editing `plugins/nadlan-config/*.php` alone does nothing to the live website.
- The only code path to production is:
  1. Bump plugin version in `plugins/nadlan-config/nadlan-config.php` in two places.
  2. Build `plugin-dist/nadlan-config-X.Y.Z.zip`.
  3. Update `plugin-dist/nadlan-config.json`.
  4. Merge the branch to `main`.
  5. Owner clicks Update in WP Admin for NadLan Config.
- The live plugin updater reads:
  `https://raw.githubusercontent.com/The-new-ben/nad-lan-co-il/main/plugin-dist/nadlan-config.json`
- Raw GitHub can cache for several minutes. Verify the manifest with `git show origin/main:plugin-dist/nadlan-config.json`, not only by opening the raw URL.
- Agents do not have WP Admin, FTP, SSH, or UPress File Manager. The final plugin update click is always the owner's human step.

Current version coordination:

- `origin/main` at branch start: `1.34.0`.
- This branch reserves `1.35.0`.
- Do not let another agent use `1.35.0` in a parallel branch.
- If another branch merges first, abandon this version number, branch fresh from `origin/main`, and bump to the next available version.

Packaging lesson from this session:

- A ZIP made by Windows tooling can show paths like `nadlan-config\lib\...`.
- The deploy skill expects a top-level `nadlan-config/` folder.
- Always inspect ZIP entries before pushing. The first entries should begin with `nadlan-config/`.
- If a bad ZIP was created, rebuild it before committing.

## Skills hierarchy and how to maintain the shared brain

This repo is not only a theme/plugin repo. It is also the operating memory for a multi-agent business build. Skills are append-mostly and should accumulate reusable knowledge.

The hierarchy:

- `AGENTS.md`: prime directive for every agent. Read first. It defines coordination, source-of-truth rules, and required state updates.
- `skills/README.md`: flat index and read order.
- `skills/SKILLS-TREE.md`: portable DNA map. It separates reusable methods from nad-lan-specific implementation.
- `skills/site-state.md`: living situation report. Append a dated block after meaningful work.
- `BACKLOG.md`: priority queue and shipped log.
- `docs/`: detailed reports, handoffs, research, audits, and implementation notes.
- Local Codex skill `nadlan-real-estate-growth`: cross-checkout memory for this machine. Update when a lesson should survive outside this repo.

How to update knowledge:

- If you changed code or site state, append to `skills/site-state.md`.
- If you learned a repeatable method, update the relevant skill.
- If the lesson is broad and portable to other domains, add it to `skills/SKILLS-TREE.md` as DNA.
- If the lesson is a one-time detailed implementation story, create a `docs/AGENT_HANDOFF_...md` or `docs/...AUDIT...md`.
- Do not delete old skills. Mark old sections historical or superseded.
- Do not duplicate a whole method in many places. Point to the source skill.
- Public repo rule: never include secrets, partner names, private lead buyer prices, application passwords, API keys, or customer data.

Reusable DNA for future websites:

- Research before writing.
- Build a money-pillar, spoke, glossary, and directory architecture.
- Keep public copy consumer-facing.
- Use directories with claim, reviews, paid tier, and lead routing as reusable revenue infrastructure.
- Keep a premium design system and mobile-safe UI.
- Package plugin changes through a versioned ZIP and manifest.
- Verify live pages after deployment, not only source code.

## Article and content DNA - what Claude/ChatGPT/Codex should do

The owner asked to preserve the writing and anti-AI-tell workflow so it can be reused on other sites.

The correct heavy article workflow:

1. Pick a specific money keyword or support keyword.
2. Manually inspect the SERP:
   - top organic results
   - title patterns
   - repeated headings
   - People Also Ask / common questions
   - suggested searches
   - visible intent: informational, transactional, comparison, local, legal, calculator, directory
3. Reverse-engineer the SERP blueprint:
   - what Google seems to reward
   - what competitors emphasize
   - what is missing
   - what entities and numbers appear repeatedly
   - what questions must be answered directly
4. Write a prompt for ChatGPT with:
   - keyword
   - intent
   - audience
   - H2/H3 skeleton
   - data requirements
   - internal links needed
   - forbidden phrases
   - public-only language rule
   - no copy-paste from competitors
5. Use ChatGPT for long Hebrew article drafting to avoid burning Codex context.
6. Codex/Claude then do QA, metadata, internal links, schema, and publishing.
7. Run the article QA checklist before publishing.

Anti-AI-tell and public copy rules:

- No public internal language: SEO, CRM, leads, suppliers, money page, revenue, keyword intent, UTM, paid lead, funnel, hub, spoke, pillar.
- No preambles like "במאמר זה".
- No generic endings like "לסיכום" or "כפי שראינו".
- No repeated H2 structures across many pages.
- No copied competitor text. Analyze the DNA, then write original Hebrew adapted to the site.
- Public pages should answer the user's actual question, not explain why the page is good for ranking.
- Scan for forbidden terms from `skills/copywriting-skill.md`.
- For live article QA, use `skills/article-qa-audit.md`.

Important nuance:

- Word count alone is not a ranking formula. The target is a complete answer. For competitive money pages the owner wants deep content, usually 2,000 to 3,500 Hebrew words, but content must still be useful and structured.
- A glossary term should answer definitional intent and link up to the money pillar. It should not cannibalize the transactional guide.
- Directory/listing pages should help users choose and compare. They should not become thin, repetitive, or index pollution.
- For listing UX, a "show more" button is fine for humans, but Google needs crawlable `<a href>` links or paginated URLs.

## Why this exists

The owner asked for a critical non-article scan and improvements that do not write full Hebrew articles. The main live pain points were:

- Archive pages can show English/default archive titles such as `NadLan Projects` or `Archive`.
- Plugin-rendered archive pages may inherit a theme header H1, creating two prominent H1s.
- Directory/listing pages need to feel modern to users but remain crawlable to Google.
- `/projects/` and `/properties/` were thin compared with the stronger guide pages.
- Public pages must not expose internal language such as SEO, CRM, leads, suppliers, money pages, revenue, or keyword intent.

## Web research used

Fresh web research was performed before editing. The implementation follows these principles:

- Google Search Central says helpful content should be people-first, complete, trustworthy, and useful to the intended audience.
- Google title-link guidance warns that multiple large prominent headings can cause Google to choose the wrong visible text as the title link.
- Google pagination guidance says crawlers generally discover URLs through `<a href>` links and do not click buttons. Therefore, a pure JavaScript "show more" UX is not enough for deep crawlability.
- Practical conclusion for this site: keep modern "show more" UI where useful, but expose real crawlable paginated links or fallback links.
- Google URL-change guidance says URL moves need exact mapping, permanent redirects, and aligned canonical/sitemap/internal-link signals. This applies to the Hebrew glossary URL remediation.

Sources to cite in future reports:

- https://developers.google.com/search/docs/fundamentals/creating-helpful-content
- https://developers.google.com/search/docs/advanced/appearance/good-titles-snippets
- https://developers.google.com/search/docs/specialty/ecommerce/pagination-and-incremental-page-loading
- https://developers.google.com/search/docs/fundamentals/seo-starter-guide
- https://developers.google.com/search/docs/crawling-indexing/url-structure
- https://developers.google.com/search/docs/crawling-indexing/site-move-with-url-changes
- https://developers.google.com/search/docs/crawling-indexing/301-redirects
- https://developer.wordpress.org/reference/functions/wp_update_post/
- https://developer.wordpress.org/reference/functions/wp_safe_redirect/

## Files changed

### Plugin source

- `plugins/nadlan-config/nadlan-config.php`
  - Bumped plugin header from `1.34.0` to `1.35.0`.
  - Bumped healthcheck version from `1.34.0` to `1.35.0`.
  - Added new loaded modules `archive-seo` and `url-governance` to the module `foreach` array.

- `plugins/nadlan-config/inc/archive-seo.php`
  - New guarded module.
  - Adds public Hebrew archive-title map for:
    - `nadlan_professional`
    - `nadlan_project`
    - `nadlan_property`
    - `nadlan_term`
  - Filters:
    - `get_the_archive_title`
    - `pre_get_document_title`
    - `document_title_parts`
    - Yoast title and social title filters
    - Yoast meta description and social description filters
  - Adds `CollectionPage` JSON-LD for catalog archives.
  - Adds `nadlan_archive_render_header()` and `nadlan_archive_render_footer()` helpers for plugin-rendered archives.
  - Root cause found during live visual check: plugin archive pages call `get_header()` / `get_footer()` inside a block theme, so WordPress renders theme-compat classic header/footer with the visible default credit `פועל על WordPress`. The new helpers preserve the document shell but replace the visible compatibility header/footer with the block theme `header` and `footer` template parts.
  - Demotes the first site-brand H1 to a `div` if the fallback header still appears. This reduces the duplicate-H1 risk without changing the full theme.
  - Adds viewport fallback on public catalog archives because live `1.34.0` rendered those archive pages without a viewport meta tag.

- `plugins/nadlan-config/inc/glossary.php`
  - Hard rule added: no `nadlan_term` or `nadlan_term_cat` public URL may use Hebrew/non-ASCII slug text.
  - Future glossary-publish calls now set ASCII `post_name` values.
  - New glossary categories now receive ASCII slugs.
  - Existing Hebrew term/category slugs are migrated once on `admin_init` for an admin user after the plugin update.
  - Exact old Hebrew slugs are stored in `nadlan_glossary_redirect_map` and 301 redirected to the new ASCII URLs.
  - Migration flushes rewrite rules once and clears the glossary autolink cache.
  - Glossary quality gate raised: a term needs 800+ words and `data_quality=worldclass` or `approved` before it is indexable.
  - Future thin glossary submissions are forced to draft and tagged `thin_draft`.
  - Thin/unapproved glossary terms are excluded from the glossary index, CPT archive, automatic internal links, and Yoast sitemap entries.

- `plugins/nadlan-config/inc/url-governance.php`
  - New global public slug guard.
  - Prevents future public Page/Post/CPT saves from creating Hebrew/non-ASCII public slugs.
  - Does not silently migrate existing broad-site URLs; existing URL repair still needs exact 301 mapping.

- `plugins/nadlan-config/inc/directory.php`
  - Updated `/professionals/` title separator to avoid long dash punctuation.
  - Uses `nadlan_archive_render_header()` when available.
  - Uses `nadlan_archive_render_footer()` when available, preventing the WordPress compatibility footer credit.
  - Adds a crawlable fallback next-page link under the visual "הצגת עוד" button when more professional pages exist.

- `plugins/nadlan-config/inc/directory-assets.php`
  - Adds small CSS for the crawlable fallback pager.

- `plugins/nadlan-config/inc/archive-grid.php`
  - Uses the new archive title labels for project/property H1s.
  - Uses `nadlan_archive_render_header()` when available.
  - Uses `nadlan_archive_render_footer()` when available, preventing the WordPress compatibility footer credit.
  - Adds short consumer-facing intro notes for project/property archive pages.
  - Removes a long dash from public archive copy.
  - Replaces visible numbered pagination on project/property archive grids with a premium "הצגת עוד" next-page link. This is still a normal crawlable `<a href>` URL, not JS-only loading.

### Knowledge and coordination docs

- `docs/AGENT_HANDOFF_NADLAN_CONFIG_1_35_ARCHIVE_SEO_2026-06-02.md`
  - This file.

Package artifacts in this branch:

- `plugin-dist/nadlan-config.json`
  - Version set to `1.35.0`.
  - Download URL set to the matching `main` raw ZIP path.
  - `1.35.0` changelog prepended.
- `plugin-dist/nadlan-config-1.35.0.zip`
  - Built from the `plugins` parent.
  - Verified with top-level `nadlan-config/` folder.
  - Verified to contain `nadlan-config/inc/archive-seo.php`.
- `BACKLOG.md`, `skills/site-state.md`, `skills/SKILLS-TREE.md`, `skills/nadlan-config-plugin.md`
  - Updated for cross-agent coordination.
- Local Codex skill `C:\Users\pro\.codex\skills\nadlan-real-estate-growth\SKILL.md`
  - Updated with the v1.35.0 archive SEO package stamp.

## What this deliberately did not do

- Did not write or publish full Hebrew articles.
- Did not touch homepage design.
- Did not use WordPress REST to bypass the repo.
- Did not change WP admin, FTP, SSH, UPress file manager, or live server files.
- Did not expose internal SEO/revenue language in public copy.
- Did not remove pagination in a way that harms crawlability.

## Verification already done

- Branch was created fresh from `origin/main`.
- Current `origin/main` manifest version was checked: `1.34.0`.
- PHP lint passed using local PHP:
  - `plugins/nadlan-config/nadlan-config.php`
  - `plugins/nadlan-config/inc/archive-seo.php`
  - `plugins/nadlan-config/inc/archive-grid.php`
  - `plugins/nadlan-config/inc/directory.php`
  - `plugins/nadlan-config/inc/directory-assets.php`
- `git diff --check` reported only Windows line-ending normalization warnings, not whitespace errors.
- A first Windows ZIP build was rejected because archive entries used backslash path separators. Rebuild with forward-slash ZIP entries before committing.
- Full plugin PHP lint passed across every `plugins/nadlan-config/**/*.php` file.
- Manifest consistency passed:
  - `version=1.35.0`
  - `download_url=https://raw.githubusercontent.com/The-new-ben/nad-lan-co-il/main/plugin-dist/nadlan-config-1.35.0.zip`
- ZIP consistency passed:
  - includes `nadlan-config/nadlan-config.php`
  - includes `nadlan-config/inc/archive-seo.php`
  - includes `nadlan-config/lib/plugin-update-checker/plugin-update-checker.php`
- all entries start with `nadlan-config/`

## Live visual check before merge

The owner updated the plugin and still saw no archive changes. Codex verified why:

- Live healthcheck: `nadlan-config` version is `1.34.0`.
- Main manifest still advertises `1.34.0`.
- This branch is still unmerged and contains `1.35.0`.
- Therefore the owner's WP update could not have installed these archive fixes yet.

Rendered live checks on `1.34.0`:

- `/projects/`
  - title: `ארכיון NadLan Projects - נדלן חכם`
  - H1s: `נדלן חכם` and `פרויקטים והתחדשות עירונית`
  - numbered `.page-numbers` pagination visible
  - no viewport meta
  - visible theme-compat shell includes old header and WordPress footer credit
- `/properties/`
  - title: `ארכיון NadLan Properties - נדלן חכם`
  - same numbered pagination issue
- `/professionals/`
  - has "הצגת עוד", but still two H1s before `1.35.0`

Action taken after visual check:

- `1.35.0` now also remediates live Hebrew/percent-encoded glossary URLs by migrating existing glossary term/category slugs to ASCII and preserving old paths with exact 301 redirects.
- `1.35.0` now also replaces `archive-grid.php` numbered pagination with a premium crawlable "הצגת עוד" link for project/property archives.

## Still required before merge

1. Commit and push branch.
2. Open PR to `main`.
3. After merge, owner must click:
   - WP Admin -> Plugins -> NadLan Config -> Update to `1.35.0`
   - If update does not appear: Dashboard -> Updates -> Check again.
4. After owner updates, verify:
   - `https://nad-lan.co.il/wp-json/nadlan/v1/healthcheck`
   - Expected live version: `1.35.0`.

## Known caveat

Earlier live checks showed the site might still be on plugin `1.33.0` while `main` already had `1.34.0`. That means some improvements already merged to `main` may not be visible until the owner performs the WP plugin update. Do not judge the branch by live pages until the owner updates the plugin after merge.

## Recommended live QA after owner update

Check these public URLs:

- `https://nad-lan.co.il/professionals/`
- `https://nad-lan.co.il/projects/`
- `https://nad-lan.co.il/properties/`
- `https://nad-lan.co.il/glossary/`

For each:

- HTTP 200.
- One visible page H1 after theme header demotion.
- Consumer-facing title and meta.
- No internal wording from `skills/copywriting-skill.md` forbidden list.
- No long dash punctuation in public copy.
- Canonical and indexability via Yoast.
- Crawlable links to deeper listing pages, not only JS buttons.
- `/glossary/` term links contain no raw Hebrew and no `%d7` percent-encoded Hebrew in the path.
- One old percent-encoded glossary URL returns `301` to its new ASCII `/glossary/<slug>/` URL.
- New glossary canonical/sitemap URLs use the ASCII slug only.
- Mobile viewport present.
- Page still loads with cache-busting query string.

## Next content work, not done here

When the owner authorizes content writing again:

- Use `skills/google-blueprint-workflow.md` and `skills/article-qa-audit.md`.
- Use ChatGPT for heavy Hebrew drafting to avoid burning Codex context.
- Codex should do SERP research, prompt design, QA, internal links, metadata, schema, and deployment.
- Proposed content expansions:
  - Project archive explanatory layer: how to compare a project, what status means, what to check before approaching a developer.
  - Property archive explanatory layer: buying intent, investment intent, deal checks, taxes, mortgage path.
  - Glossary restructure: one concept per strong term page, Wikipedia-style but original Hebrew, terms linked up to money pillars.
  - Professional directory guide: choosing contractors, appraisers, mortgage advisors, lawyers, inspectors.

## Honesty statement

This package fixes source-level plugin problems and packages them for the auto-update flow. It does not by itself change the live site until it is merged to `main` and the owner clicks the WP plugin update. The code-level changes are small and lint-clean; the visual/live effect still needs post-update browser verification.
