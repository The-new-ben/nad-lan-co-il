# WordPress Content Types — Page vs Post vs CPT

> **Notice to all agents (Codex especially):** in earlier sessions Codex generated all content as WordPress **Pages**. That is partially wrong. Read this decision rule before creating any new content.

## Decision rule

| Content | Type | Reason |
|---|---|---|
| Homepage | Page (front page) | Single, hierarchical, no archive needed |
| Pillar pages (`/buying/`, `/selling/`, `/investment/`, `/mortgage/`, `/tax-legal/`, `/urban-renewal/`) | **Page** | Top of hierarchy, one per topic, evergreen, parent for child pages |
| City pages (`/cities/{city}/`) | **Page** under a `Cities` parent page | Hierarchy maps to URL, evergreen, ~50 pages total |
| Neighborhood pages (`/cities/{city}/{neighborhood}/`) | **Page** under city | Hierarchy, ~200-500 pages eventually |
| Tools / calculators (`/tools/mortgage/`, `/tools/purchase-tax/`, `/tools/valuation/`) | **Page** (with shortcode for the JS app) | Single, evergreen, top-level |
| Legal/about/contact/privacy | **Page** | Standard |
| Spoke guides ("מס רכישה דירה ראשונה", "כמה עולה דירה ברמת אביב", etc.) | **Post** in custom taxonomy `guide_topic` | High volume (100+), need archive, need taxonomy queries, dated for freshness signal |
| Blog / news / market updates | **Post** in built-in category | Standard blog |
| Property listings | **CPT: `property`** | Specialized fields (price, rooms, sqm, etc.), specialized archive, specialized schema |
| Developer projects | **CPT: `project`** | Distinct fields and lifecycle |
| Professional directory entries (lawyers, brokers, mortgage advisors, appraisers) | **CPT: `professional`** with taxonomy `profession` | Distinct schema (Person + Organization), distinct fields, distinct archive |
| Public transaction data mirrored from nadlan.gov.il | **CPT: `transaction`** (or store in custom table for performance) | Volume too large for `wp_posts` |

## Why Pages are wrong for spokes

- No native taxonomy → no "all guides about מס רכישה" archive.
- No category/tag-driven internal linking.
- No date-stamped archive (Google reads freshness on Posts more readily).
- Hard to query "give me all guides where `pillar = mortgage` ordered by date".
- The standard sitemap separates Pages and Posts; mixing them confuses Yoast's pillar/cornerstone setup.

## Migration plan (when ready)

Codex previously created content as Pages. We do not migrate yet. We document the rule, and when the owner approves Phase 2:

1. Identify which of the existing Pages are actually pillars (keep as Page) vs spokes (convert to Post).
2. For each spoke being converted: create a new Post, copy content, set canonical to the new Post URL, 301 the old Page URL.
3. Update internal links.
4. Keep pillars as Pages forever.

**Do not do this migration silently.** It changes URLs. It needs Yoast Redirections set up first. It needs sitemap re-submission. Document the steps in `yoast-config.md` before executing.

## Custom Post Type registration

When CPTs are registered in `functions.php` (or a small companion plugin), use these slugs and labels. **Do not change slugs after launch** — URLs depend on them.

## Hard URL Slug Rule

Read `url-slug-governance.md` before creating or migrating any public URL.

Public titles and body copy may be Hebrew. Public URL slugs must be ASCII only. Never create a Page, Post, CPT item, taxonomy term, project, professional, city, or glossary term with Hebrew/non-ASCII path text or a `%d7` percent-encoded path.

If an existing Hebrew URL must be repaired, do not delete it blindly. Create the ASCII replacement, add exact 301 redirect mapping, update internal links, verify canonical/sitemap output, and document the migration.

```php
// property → /properties/{slug}/
// project → /projects/{slug}/
// professional → /professionals/{slug}/, taxonomy 'profession' → /profession/{slug}/
// transaction → not publicly addressable; queried as data
// guide_topic taxonomy on standard Post → /guide-topic/{slug}/
```

`functions.php` currently registers only `nadlan_lead` (a private CPT for the inquiry form). All other CPTs are **not yet registered** in code — when registering, prefix functions with `nadlan_revenue_` to stay consistent with the existing pattern.

## Yoast cornerstone configuration

- Mark every pillar Page as **cornerstone**.
- Mark every city Page as **cornerstone**.
- Do NOT mark spoke Posts as cornerstone (defeats the purpose).
- Set the "primary category" on every spoke Post to one and only one pillar topic. This enforces the hub-and-spoke "one parent" rule from the strategy.

## Open TODOs for next agent

- [ ] Audit current live site: list every Page Codex created, classify each as pillar / city / neighborhood / spoke / tool / legal. Output to `docs/research/content-audit-YYYY-MM-DD.md`.
- [ ] Decide CPT registration timing — before or after migrating spokes off Pages.

---
_Created 2026-05-28 by Claude Code (claude-opus-4-7)._
