# Nadlan Non-Article Archive and Navigation Fixes - 2026-06-02

Codex stamp: 2026-06-02. Scope requested by the owner: do what is possible now without writing full Hebrew articles. Small Hebrew labels and page architecture changes are allowed. Full pillar/spoke/article production should move to ChatGPT using the SERP Blueprint workflow.

## What I Could Do Without Massive Hebrew Writing

I could safely do these now:

- Live URL verification and rendered/mobile checks.
- Route conflict correction.
- Navigation/internal-link fixes.
- WordPress REST template attempts.
- Glossary archive structure improvement.
- Crawlability and archive diagnostics.
- Plugin patch specification for the next deploy.
- SERP Blueprint to ChatGPT workflow documentation.
- Skill and knowledge updates.

I did not write full Hebrew articles. I did not generate a 1,000-4,000 word page in Codex.

## Fresh Research Used

- Google link best practices: Google needs crawlable `<a href>` links with descriptive anchor text. Source: https://developers.google.com/search/docs/crawling-indexing/links-crawlable
- Google pagination and incremental loading: pagination, load-more, and infinite scroll can all work, but the crawler must be able to discover all content. Source: https://developers.google.com/search/docs/specialty/ecommerce/pagination-and-incremental-page-loading
- Google faceted navigation crawling: uncontrolled filter URLs can create infinite URL spaces and slow discovery of useful pages. Source: https://developers.google.com/crawling/docs/faceted-navigation
- Google helpful content: content should be substantial, original, trustworthy, and useful to people, not just written to manipulate rankings. Source: https://developers.google.com/search/docs/fundamentals/creating-helpful-content
- Google structured data: Article and ProfilePage structured data should be validated and deployed on accessible, indexable pages. Sources: https://developers.google.com/search/docs/appearance/structured-data/article and https://developers.google.com/search/docs/appearance/structured-data/profile-page

## Live Changes Applied

### 1. Professionals Guide Route Conflict

Problem: the strong long-form professionals guide existed as a WordPress page with slug `/professionals/`, but the custom post type archive also owns `/professionals/`. The archive won the route, so the guide was effectively hidden.

Action: moved the guide page to:

- `https://nad-lan.co.il/real-estate-professionals-guide/`

Verification:

- HTTP 200.
- One H1.
- Canonical present.
- Viewport present.
- 2,383+ rendered words.
- No internal/private terms found.

### 2. Navigation Link Added

Problem: after the guide was moved, it needed a crawlable public path.

Action: added one submenu link under `אנשי מקצוע`:

- Label: `מדריך בחירת אנשי מקצוע`
- URL: `https://nad-lan.co.il/real-estate-professionals-guide/`

Verification:

- Homepage public HTML contains the link once.
- Script output: `hasGuideLink: true`, `linkOccurrences: 1`.

### 3. Custom Archive Templates Created

Created or updated custom block templates through WordPress REST:

- `archive-nadlan_professional`
- `archive-nadlan_project`
- `archive-nadlan_property`
- `archive-nadlan_term`

Result:

- `/glossary/` uses the custom template body. It now has a user-facing H1: `מילון נדל״ן ומושגים חשובים`, custom intro, related links, and one H1.
- `/professionals/`, `/projects/`, and `/properties/` do not use the custom block templates. They are being rendered by the plugin/archive path, not by the block archive templates.

Honesty: the template work partially succeeded. It fixed the visible glossary body, but did not fix project/property/professional archives.

### 4. Verification Scripts Added

Added:

- `scripts/nadlan-nonarticle-archive-fixes-20260602.mjs`
- `scripts/nadlan-archive-source-inspect-20260602.mjs`
- `scripts/nadlan-navigation-professionals-guide-link-20260602.mjs`

The scripts are idempotent and document the exact live evidence.

## Current Live Findings After Fixes

| URL | Status | H1 | Viewport | Canonical | Main Issue |
| --- | ---: | ---: | --- | --- | --- |
| `/real-estate-professionals-guide/` | 200 | 1 | yes | yes | Looks structurally clean. |
| `/glossary/` | 200 | 1 | yes | yes | Body improved, but title still says archive. |
| `/professionals/` | 200 | 2 | no | yes | Plugin/archive route still outputs site brand as H1. |
| `/projects/` | 200 | 2 | no | yes | Title says `ארכיון NadLan Projects`; thin at about 220 words. |
| `/properties/` | 200 | 2 | no | yes | Title says `ארכיון NadLan Properties`; very thin at about 77 words. |

## Exact Plugin Fix Needed Next

This cannot be safely deployed from the current local repo because the active live plugin is newer than the exported plugin source I can see. Active plugin healthcheck reports `nadlan-config` version `1.33.0`; the local export under temp contains older plugin code. Do not blindly ship the stale plugin.

When the current plugin source is pulled/exported, patch it with one small versioned release:

1. Register Hebrew public labels for CPTs while keeping admin labels readable:
   - `nadlan_property`: `נכסים`
   - `nadlan_project`: `פרויקטים`
   - `nadlan_professional`: `אנשי מקצוע`
   - `nadlan_term`: `מילון נדל״ן`

2. Add title/meta filters for post type archives:
   - `/projects/`: `פרויקטים חדשים והתחדשות עירונית | נדל״ן חכם`
   - `/properties/`: `נכסים למכירה והשקעה | נדל״ן חכם`
   - `/glossary/`: `מילון נדל״ן ומושגים חשובים | נדל״ן חכם`
   - `/professionals/`: keep current good title or refine.

3. Add `wp_head` safety for plugin-rendered archives:
   - viewport meta if missing.
   - no duplicate brand H1 in archive output.
   - one page H1 only.

4. Keep facet URL rules:
   - Index only valuable combinations.
   - `noindex,follow` for deep or empty filter combinations.
   - Keep every important listing reachable by normal links, not only JavaScript.

5. Re-run:
   - `node scripts\nadlan-archive-source-inspect-20260602.mjs`
   - mobile screenshots for `/professionals/`, `/projects/`, `/properties/`.

## SEO Opinion: Archive Pages, Pagination, Show More

The owner preference for “show more” is good for UX if it is implemented correctly. For SEO, it must not be JavaScript-only.

Recommended model:

- Human UI can use “show more”.
- HTML must expose crawlable links to page 2, page 3, or category/city pages using real `<a href>`.
- Important directory segments should become real indexable hubs, for example `/projects/tel-aviv/` only when there is enough unique data.
- Deep facets and empty combinations should be `noindex,follow` or blocked from crawl, because they can create crawl waste.

I do not recommend deleting pagination entirely unless the “show more” button is backed by crawlable URL states.

## SEO Opinion: Listings and Catalogs

The index/catalog layer is not automatically contaminating the money pages. It becomes dangerous only when thousands of thin pages are indexable and target generic commercial keywords.

Current correct direction:

- Entity/profile pages should target branded/navigational intent.
- Money pages should target generic high-value intent.
- Stub professionals/projects should stay `noindex,follow` until enriched.
- Enriched profiles should include unique facts: city, specialty, license/source, services, verification/update date, questions to ask, and links to relevant guides.

## SEO Opinion: Glossary

Keep the glossary. It is valuable for authority and AI/GEO if handled carefully.

Rules:

- Standalone term pages only when the query is truly definitional.
- If the term overlaps a money guide, add it as an H2 anchor inside the money guide instead of creating a second URL.
- Terms must link up to one parent pillar/spoke and sideways to sibling terms.
- Do not let the glossary outrank the money guide for commercial intent.
- Do not use auto-linking that links every occurrence across the site.

The current glossary body is now better, but it still needs plugin-level document title cleanup and a richer A-Z/category UI later.

## Revenue and Product Direction

Highest ROI non-article work remains:

1. Mortgage and purchase-tax tool funnels.
2. Property valuation/seller funnel.
3. Professionals directory with claim, verification, paid profile upgrade, and inquiry flow.
4. Project/developer pages with verified data, city status pages, and project inquiry paths.
5. Auction/seller experiments only after legal/payment flow is reviewed.

The big opportunity is not just content. It is a real estate decision product: tools, verified professionals, project data, seller valuation, alerts, and inquiries.

## Honesty Statement

I fixed what could be fixed safely without long Hebrew writing or an unsafe plugin deploy: the hidden professionals guide is now accessible and linked from the main menu, the glossary archive body is user-facing and structurally cleaner, and the diagnostics are preserved. I did not fix the project/property/professional archive title/H1/viewport issues because the live routes are controlled by the active plugin/archive path and the current plugin source is not present in the repo at the active live version. The next real fix is a small plugin release from the current plugin source, not more article writing.
