# Yoast SEO Configuration — target state and current status

> **Notice to all agents:** Yoast is installed on the live site but not configured (owner-confirmed 2026-05-28). This file is the target configuration. When you actually configure Yoast, update this file's "current status" section.

## Current status (2026-05-28)

- Plugin installed: **yes** (Yoast SEO, free version unless otherwise noted).
- Configured: **no**.
- General settings: defaults.
- Titles & meta templates: defaults (`%%title%% %%page%% %%sep%% %%sitename%%`).
- Schema: default (Organization + WebSite).
- XML sitemap: default (enabled).
- Social: not configured.
- Webmaster verification: **not connected** to Google Search Console or Bing Webmaster Tools.
- Redirections: **not present** (requires Yoast Premium or alternative like Redirection plugin).
- Logo for schema: **owner uploaded a generated logo recently**; verify dimensions ≥ 112×112.

## Target configuration

### General → Site representation

- Organization or person: **Organization** (`nad-lan` brand). Not "person" — even though the owner is a lawyer, the site is the brand. The lawyer credential surfaces via author by-line, not site identity.
- Organization name: `nad-lan` (Hebrew display: `נד-לן` if owner approves; otherwise English).
- Organization logo: 512×512 transparent PNG minimum, also a 112×112 favicon.
- Default OG image: 1200×630 with the nad-lan logo + tagline in Hebrew.

### Search appearance → Content types

- **Pages**: show in search results ✓ ; date in snippet preview ✗ ; SEO title template `%%title%% %%sep%% %%sitename%%` (drop `%%page%%` for single Pages).
- **Posts**: show ✓ ; date in snippet ✓ (freshness signal for spokes); template `%%title%% %%sep%% %%sitename%%`.
- **Properties / Projects / Professionals (CPTs, when registered)**: show ✓ ; tailored templates per type (e.g. `%%title%% — %%price%% ₪ %%sep%% nad-lan`).
- **Categories / Tags / Author archives**: noindex unless content strategy uses them. Default: noindex.
- **Date archives**: noindex.
- **Format archives**: disable.
- **Media (attachment) URLs**: redirect to parent post. Critical — these waste crawl budget if not redirected.

### Search appearance → Breadcrumbs

- Enable.
- Separator: `›` (single).
- Anchor text for homepage: `דף הבית`.
- Prefix for the breadcrumb path: empty.
- Prefix for archive breadcrumbs: empty.
- Bold the last page: yes.
- Show Blog page in breadcrumbs: no (we use Pages, not the WP blog as homepage).

### Schema — IMPORTANT, conflicts with theme

The custom theme already outputs a `WebSite` JSON-LD in `functions.php:94-112`. Yoast will also output one by default. Two conflicting `WebSite` schemas on the same page is a problem.

**Decision (recommend):** Disable the theme's hand-rolled `nadlan_revenue_schema()` and rely on Yoast's schema. Yoast's is correct, well-maintained, and integrated with breadcrumbs and Organization.

Implementation when the time comes: remove the `add_action('wp_head', 'nadlan_revenue_schema')` line in `functions.php` and document the removal in `site-state.md`. Do NOT do this until Yoast is fully configured.

### Schema — Person (E-E-A-T moat for the lawyer)

Configure Yoast's "Author" schema for the owner's profile:
- Type: Person.
- Name: owner's full Hebrew name.
- Description: `עורך דין החבר בלשכת עורכי הדין בישראל. מתמחה בנדל"ן ומיסוי מקרקעין.` (or whatever the owner's exact bar status is).
- `sameAs`: lawyer's official lawyer-bar profile URL (lawyer.org.il directory), LinkedIn, any law firm site.
- `jobTitle`: `עורך דין`.
- `worksFor`: linked Organization (the law firm name, if separate; otherwise `nad-lan`).

By-line every legal/tax article with this author. This is the E-E-A-T moat against content-mill competitors.

### Social

- Facebook page URL (if exists).
- X/Twitter handle (if exists).
- Default OG image (the 1200×630 above).
- Twitter card type: `summary_large_image`.

### XML sitemap

- Enabled.
- Index sitemap: `/sitemap_index.xml`.
- Submit to Google Search Console (see below).
- Pages: include. Posts: include. CPTs (when registered): include each. Taxonomies: include only those used for navigation. Author archives: exclude. Date archives: exclude.

### Tools → Webmaster verification

- Google Search Console: add the verification meta tag.
- Bing Webmaster Tools: add the verification meta tag.
- (Yandex / others: skip unless owner wants RU/CIS traffic.)

### Tools → Redirections

Yoast Premium or the free **Redirection** plugin. Set up before any URL change. Maintain a redirect log in `docs/research/redirects-log.md`.

## E-E-A-T checklist for legal/tax pages

Each tax / legal pillar and spoke MUST have:

1. Author by-line: `מאת [owner full name], עורך דין`.
2. "Last reviewed" date visible.
3. Citation footer: government source URLs (rashut hamasim, ministry of justice), at least one.
4. A disclaimer: `אין לראות במאמר ייעוץ משפטי. לפני קבלת החלטות יש להיוועץ בעורך דין.` Yes, the owner is a lawyer; this disclaimer is still required by Israeli bar rules for general content.
5. Schema: `Article` with `author` linked to the Person schema; if it's a FAQ, also `FAQPage` for the visible Q&A only.

## Open TODOs for next agent

- [ ] Open Google Search Console for nad-lan.co.il. Verify via Yoast meta tag (preferred) or DNS TXT. Submit sitemap.
- [ ] Open Bing Webmaster Tools. Verify. Submit sitemap.
- [ ] Decide: remove theme `nadlan_revenue_schema()` once Yoast is fully configured, OR keep it because Yoast is misconfigured. Currently NEITHER is fully right.
- [ ] Verify the uploaded logo dimensions; replace if under 112×112.
- [ ] Configure Person schema for the owner.

---
_Created 2026-05-28 by Claude Code (claude-opus-4-7)._
