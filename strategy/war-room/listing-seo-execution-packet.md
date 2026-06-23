# Listings and SEO Execution Packet

Date: 2026-06-23

Purpose: turn the recovered keyword universe, page architecture, listings prototype screenshots, and anti-cannibalization rule into a build-ready execution packet.

## Current Evidence Read

- The keyword map has 225 rows with canonical owners.
- 117 rows are money pages and 108 are support pages.
- 31 rows are P0 and 105 rows are P1.
- 39 page templates exist in the page architecture map.
- The current listings prototype renders desktop and 390px mobile without obvious horizontal overflow, but it is not production-ready because the images and supply are not verified and the SEO indexing model is not yet enforced.

## Product Decision

Listings are not a small catalog feature. They are a marketplace and SEO engine. The build must start with canonical ownership and data trust:

1. One keyword row owns each indexable money page.
2. Filters are user tools first, not unlimited indexable pages.
3. Listing cards must show source, freshness, image truth, and paid-state disclosure where applicable.
4. Empty or thin supply pages must not become indexed doorway pages.
5. Support content links into money pages and does not compete with them.

## Google Search References Checked

- Canonicalization: https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls
- Ecommerce URL structure: https://developers.google.com/search/docs/specialty/ecommerce/designing-a-url-structure-for-ecommerce-sites
- Outbound link qualification: https://developers.google.com/search/docs/crawling-indexing/qualify-outbound-links
- Structured data guidelines: https://developers.google.com/search/docs/appearance/structured-data/sd-policies
- Structured data intro: https://developers.google.com/search/docs/appearance/structured-data/intro-structured-data
- Localized versions and hreflang: https://developers.google.com/search/docs/specialty/international/localized-versions

## Build Backlog

Use `listing-seo-execution-packet.csv` as the implementation queue. The first slices are:

- LS-001 keyword registry enforcement
- LS-002 canonical marketplace routes
- LS-003 facets and filters
- LS-004 listing card trust
- LS-005 asset truth
- LS-011 freshness and supply
- LS-015 QA release gate

## Screenshot Gates

Every implementation PR must save:

- desktop 1440 marketplace screenshot
- mobile 390 marketplace screenshot
- filter drawer open
- applied filter state
- empty result state
- paid and non-paid cards side by side
- listing detail first viewport
- footer with CTA visible

## Non-Production Warning

The current prototype screenshots are evidence of direction and problems, not production proof. Do not present generic project images, incomplete freshness labels, or demo supply as final public inventory.
