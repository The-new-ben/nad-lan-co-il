# Technical SEO And Schema Execution Packet

Date: 2026-06-23

Status: build-ready specification, not live implementation proof.

## Purpose

This packet turns the short schema and technical SEO notes into a route-by-route matrix that Codex can implement against. It covers:

- index/noindex rules
- canonical rules
- robots rules
- sitemap inclusion
- hreflang rules
- structured data
- breadcrumbs
- noindex conditions
- source and validation gates

## Core Decision

No page family gets built or indexed without a row in `technical-seo-page-matrix.csv`.

This is the protection against:

- duplicate city pages
- filter URL index bloat
- fake listing schema
- unsupported project offers
- unreviewed English pages
- country-abroad pages diluting Israel authority
- duplicate schema from plugins and custom code

## Official Sources

Official Google sources used:

- Structured data overview: https://developers.google.com/search/docs/appearance/structured-data/intro-structured-data
- Supported structured data gallery: https://developers.google.com/search/docs/appearance/structured-data/search-gallery
- Canonical URLs: https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls
- Robots meta and noindex: https://developers.google.com/search/docs/crawling-indexing/block-indexing
- Robots meta specifications: https://developers.google.com/search/docs/crawling-indexing/robots-meta-tag
- Sitemaps: https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap
- Breadcrumb structured data: https://developers.google.com/search/docs/appearance/structured-data/breadcrumb
- Product structured data: https://developers.google.com/search/docs/appearance/structured-data/product
- Organization structured data: https://developers.google.com/search/docs/appearance/structured-data/organization
- International and multilingual sites: https://developers.google.com/search/docs/specialty/international/managing-multi-regional-sites
- Search Console: https://search.google.com/search-console/about

## Structured Data Rules

Allowed only when the visible page proves the facts:

- `Organization` and `WebSite` on the home page.
- `BreadcrumbList` on pages with stable hierarchy.
- `ItemList` on hubs and result pages with visible listed items.
- `Product` and `Offer` only when price, availability, currency, and source are visible and real.
- `LocalBusiness` or `ProfessionalService` only for verified professional profiles.
- `Article` for reviewed guides and reports.

Not allowed:

- fake prices
- fake availability
- fake reviews
- official project claims without source
- unsupported tax or mortgage claims
- duplicate schema from multiple systems
- schema that describes content users cannot see

## Indexation Rules

Index by default only when the page has:

- canonical owner
- unique intent
- visible useful content
- source gate passed
- no fake assets
- no legal/finance review gaps
- mobile screenshot proof

Use noindex for:

- unverified listings
- arbitrary filters and sort states
- city pages without real supply
- project pages with missing official source
- showroom pages that are canvas-only or fake-asset-only
- tax/mortgage pages before review
- English pages before source and language review
- abroad country pages before country source packs

## Release Gate

Before any page family ships:

- matrix row exists
- canonical rule exists
- robots rule exists
- sitemap decision exists
- breadcrumb path exists
- schema owner exists
- duplicate schema scan is clean
- desktop screenshot exists
- 390px screenshot exists
- rendered text scan is clean
- Search Console evidence is attached after deployment

## Files In This Packet

- `technical-seo-page-matrix.csv`
- `technical-seo-execution-packet.csv`
- `technical-seo-execution-packet.md`
- `technical-seo-execution-packet-rtl.html`
- `technical-seo-execution-packet-preview.png`
- `technical-seo-execution-packet-preview-mobile.png`
- `technical-seo-execution-packet-visual-qa.md`
