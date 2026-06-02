# URL Slug Governance

## Hard Rule

Public Hebrew content is allowed and desired. Public Hebrew or other non-ASCII URL slugs are forbidden.

Do not create URLs like:

- `/glossary/עסקת-קומבינציה/`
- `/השקעת-נדלן-ביוון/`
- any path that renders as `%d7%...`

Use ASCII slugs only:

- `/glossary/combination-deal/`
- `/real-estate-investment-greece/`
- `/purchase-tax-2026/`

## Why

The owner explicitly rejected Hebrew URLs after live glossary terms appeared as percent-encoded paths. These URLs complicate redirects, future redirection-plugin work, crawling, reporting, support, and cross-agent publishing.

## Code Guard

`plugins/nadlan-config/inc/url-governance.php` is the global prevention mechanism.

It filters public WordPress saves and replaces empty or non-ASCII public slugs with ASCII slugs for public post types. It does not silently migrate all existing pages because broad URL migrations require mapping and redirects.

`plugins/nadlan-config/inc/glossary.php` has an extra glossary-specific remediation:

- future `nadlan_term` posts get ASCII `post_name`;
- future `nadlan_term_cat` categories get ASCII slugs;
- existing Hebrew glossary term/category slugs migrate once after plugin update;
- old Hebrew glossary paths are stored in `nadlan_glossary_redirect_map`;
- old Hebrew glossary URLs redirect with 301 to the new ASCII URLs.

## Publishing Checklist

Before publishing any Page, Post, CPT item, glossary term, city, project, professional, or taxonomy:

- Confirm the public slug is ASCII only.
- Confirm the URL path has no Hebrew and no `%d7`.
- If changing an existing URL, create an exact old URL -> new URL 301 mapping first.
- Update internal links to point to the new canonical URL.
- Confirm canonical and sitemap output show the new ASCII URL.
- Record the change in `skills/site-state.md`.

## Glossary Special Rule

A glossary term is content, not a label.

Do not publish a glossary term as an indexable page unless it is a world-class definitional article:

- at least 800 Hebrew words;
- clear definitional intent only;
- no cannibalization of a money pillar or spoke;
- source-backed;
- links up to the correct pillar/spoke;
- links sideways only to approved related glossary terms;
- marked `data_quality=worldclass` or `data_quality=approved` only after review.

Short glossary entries should stay draft or noindex. They should not appear in the glossary index and should not receive automatic internal links.

## Repair Method For Existing Bad URLs

Never delete bad URLs blindly.

1. Inventory every old URL.
2. Create exact one-to-one ASCII replacement URLs.
3. Add 301 redirects from old to new.
4. Update internal links.
5. Verify old URL returns 301.
6. Verify new URL returns 200.
7. Verify canonical and sitemap point to new URL.
8. Monitor Google Search Console for old URLs moving into "Page with redirect".

## ChatGPT Term Expansion Workflow

Use ChatGPT for heavy Hebrew expansion, but Codex/Claude must supply the blueprint:

- target term;
- English equivalent;
- source URLs;
- related pillar;
- what this term must not cannibalize;
- required sections;
- examples from Israeli real-estate practice;
- definitions, practical meaning, risks, documents, numbers where relevant;
- internal links to pillar/spokes;
- strict instruction: no internal SEO language and no AI-tell punctuation.

The result is reviewed before being marked `worldclass` or `approved`.

## Codex Stamp

2026-06-02: Added after owner flagged live Hebrew glossary URLs and thin 100-word glossary pages as severe risks. This skill is portable DNA for every Hebrew site in the portfolio.
