# Lovable Report 1 - Public Trust + Technical SEO Audit Plan

Source: Lovable project https://lovable.dev/projects/a7493b94-2e46-4d38-9c6a-80dcf0905f45
Captured: 2026-06-21
Mode: Plan mode / no build requested

---

Report 1 only, then stop and write READY FOR NEXT PROMPT.

Report 1: Public Trust + Technical SEO Audit Plan for NadLan.

Use these live URLs as audit targets:

https://nad-lan.co.il/
https://nad-lan.co.il/join-pro/
https: ...
Show more
Waiting for user to approve plan

No tasks tracked yet.
Plan

Report 1: Public trust + technical SEO audit plan for 7 NadLan URLs, with BLOCK posture, audit table, checklists, Playwright QA gate, repo artifact layout, and top 10 P0 fixes.

Open plan
Review
Skip
Approve
Plan
Tell Lovable what to do instead...




Plan
Send message
Add files

Drop any files here to add them to your message

Report 1 — Public Trust + Technical SEO Audit Plan (NadLan)

Plan-only. No crawl run yet, no code, no fixes. All findings below are audit hypotheses to verify on live URLs — every row is NEEDS_VERIFICATION until a Playwright + curl pass collects the listed evidence.

1. Executive Summary — BLOCK / PASS Posture

Current posture: BLOCK. No growth, content, hub, schema-expansion, or link-acquisition work proceeds until every P0 row in this report is PASS. Public trust is a gate, not a phase.

Rationale:

The site is YMYL (purchase, mortgage, legal). One Woo/cart/debug leak on a project page destroys credibility for both Israeli buyers and international investors mid-six/seven-figure decisions.

Fake facades / silent showroom fallback / unlabelled concept assets on flagship projects (Sde Dov / Dimri Yama, Rainbow Tel Aviv) are reputational landmines amplified by the international audience that screenshots and shares.

Duplicate H1s, placeholder sitemap entries, and @wordpress/interactivity console errors signal "unfinished template" to Google's quality systems and to any developer-savvy investor opening DevTools.

Gate definition: PASS = every P0 row's acceptance criteria met, verified by a re-run of the Playwright QA gate (Section 5) at all three viewports, with zero console errors and zero leaked Woo/internal strings across the seven audit URLs.

2. Audit Table (per-URL hypotheses to verify)

Severity: P0 blocker / P1 high / P2 medium. SEO/Trust/Conversion impact: L/M/H. All rows NEEDS_VERIFICATION.

URL

	

Issue (hypothesis)

	

Evidence to collect

	

Sev

	

SEO

	

Trust

	

Conv

	

Recommended fix

	

Acceptance criteria

	

Codex task

	

QA task




/

	

Woo/cart/notifications residue in header/footer; debug/QA text

	

DOM dump of header+footer; grep cart, סל, WooCommerce, debug, QA, notice

	

P0

	

M

	

H

	

H

	

Remove Woo widgets + notification blocks from non-commerce templates via theme partial

	

Zero matches for blocklist; no cart icon on non-commerce pages

	

trust:strip-woo-residue-home

	

qa:home-trust-strings




/

	

Duplicate H1 (theme H1 + section H1)

	

document.querySelectorAll('h1').length

	

P0

	

H

	

M

	

L

	

Demote secondary to H2

	

Exactly one H1

	

seo:single-h1-home

	

qa:h1-count




/

	

@wordpress/interactivity console errors

	

DevTools console capture

	

P0

	

M

	

M

	

M

	

Pin/upgrade interactivity bundle or disable unused block

	

Zero console errors at load + 5s idle

	

infra:fix-wp-interactivity

	

qa:console-clean




/

	

Mobile overflow at 390

	

Screenshot + document.documentElement.scrollWidth vs clientWidth

	

P0

	

M

	

H

	

H

	

Constrain offending section to max-width:100vw; overflow-x:hidden on offender, not body

	

scrollWidth <= clientWidth at 390

	

ui:fix-390-overflow

	

qa:no-h-overflow




/

	

Missing/weak meta description, og:image, canonical

	

curl -sL head dump

	

P1

	

H

	

M

	

L

	

Set HE meta + og + canonical via nadlan-config

	

All four present, ≤160 chars desc

	

seo:home-head-tags

	

qa:home-head




/join-pro/

	

Dead "Join" CTA / form posts to nowhere / shows internal QA copy

	

Click trace + network tab; grep lorem, TODO, בדיקה, test

	

P0

	

L

	

H

	

H

	

Wire to real endpoint or hide CTA until ready

	

CTA either works end-to-end or page is noindex + hidden from nav

	

feature:join-pro-cta

	

qa:join-pro-flow




/join-pro/

	

No author/trust signals for professionals onboarding

	

DOM inspection

	

P1

	

M

	

H

	

H

	

Add verification policy, license requirements, privacy note

	

Policy block visible above fold

	

content:join-pro-trust

	

qa:join-pro-trust-block




/sitemap/

	

Placeholder entries, broken links, "Sample Page" residue

	

Crawl all links; HTTP status each

	

P0

	

H

	

H

	

L

	

Regenerate HTML sitemap from real routes; remove WP defaults

	

Zero 404s; zero placeholder titles

	

seo:rebuild-html-sitemap

	

qa:sitemap-links




/sitemap/

	

Differs from /sitemap.xml (if any)

	

Compare both

	

P1

	

H

	

L

	

L

	

Single source of truth

	

URL sets reconcile

	

seo:sitemap-parity

	

qa:sitemap-parity




/professionals/

	

Placeholder/demo professionals, fake reviews, missing license #

	

DOM scrape of cards; check for stock names/photos

	

P0

	

M

	

H

	

H

	

Hide demo entries; show empty-state with onboarding CTA

	

Only real, verified pros shown; each card has license/verification badge or marked unverified

	

data:purge-demo-pros

	

qa:pros-no-demo




/professionals/

	

No filter integrity (city/category returns wrong set)

	

Click each filter, capture results

	

P1

	

M

	

M

	

M

	

Fix query; add empty-state

	

Filters return correct subset or honest empty-state

	

feature:pros-filters

	

qa:pros-filter




/property-value-estimator/

	

No methodology, no last-updated, no disclaimer (LEGAL_REVIEW)

	

DOM inspection

	

P0

	

M

	

H

	

M

	

Add methodology block, data sources, last-updated, "not a formal appraisal" disclaimer

	

All four present above fold; LEGAL_REVIEW signed off

	

content:estimator-disclosure

	

qa:estimator-disclosure




/property-value-estimator/

	

Returns suspiciously precise number without confidence range

	

Submit 3 test inputs

	

P0

	

L

	

H

	

H

	

Show range + confidence, not single number

	

UI shows range + "אומדן בלבד"

	

feature:estimator-range

	

qa:estimator-range




/property-value-estimator/

	

Calculator JS errors / values silently default

	

Console + network

	

P1

	

L

	

H

	

M

	

Validate inputs, show errors

	

No silent fallback; explicit validation

	

bug:estimator-validation

	

qa:estimator-errors




/projects/dimri-yama-sde-dov/

	

Fake facade / silent fallback to generic render

	

Visual compare to official Dimri marketing; screenshot

	

P0

	

M

	

H

	

H

	

If no official asset: label concept or show missing; never fake

	

Hero state is one of `official

	

concept

	

missing`, labelled




/projects/dimri-yama-sde-dov/

	

Invented prices, apartment counts, availability

	

Compare to developer site

	

P0

	

M

	

H

	

H

	

Strip invented numerics; show "data per developer, last updated X" or hide

	

Zero numerics not sourced from developer/official PDF

	

showroom:strip-invented-data-dimri

	

qa:dimri-data-source REQUIRES_OFFICIAL_ASSET




/projects/dimri-yama-sde-dov/

	

Dead "Contact developer" / "Brochure" / "Floor plans" buttons

	

Click each CTA

	

P0

	

L

	

H

	

H

	

Disable + hide if not wired; never render dead

	

Every visible CTA performs its action

	

showroom:no-dead-ctas-dimri

	

qa:dimri-ctas




/projects/dimri-yama-sde-dov/

	

Stacked/duplicate sections (template residue)

	

DOM inspection

	

P1

	

M

	

M

	

M

	

Deduplicate template blocks

	

No duplicate hero/cta/gallery blocks

	

showroom:dedupe-dimri

	

qa:dimri-dedupe




/projects/dimri-yama-sde-dov/

	

No EN surface / no hreflang stub

	

View source

	

P1

	

H

	

M

	

M

	

Plan EN mirror; add hreflang x-default + he now, en later

	

<link rel=alternate hreflang> present, valid

	

seo:hreflang-stub-dimri

	

qa:hreflang




/projects/dimri-yama-sde-dov/

	

Missing schema: Residence, Place, Organization (developer), BreadcrumbList

	

View source / Rich Results Test

	

P1

	

H

	

M

	

L

	

Add JSON-LD via nadlan-config

	

Rich Results Test passes; no errors

	

seo:schema-project-dimri

	

qa:schema-dimri




/projects/rainbow-tel-aviv/

	

Same set as Dimri row above

	

Repeat evidence

	

P0

	

M-H

	

H

	

H

	

Same fixes scoped to Rainbow

	

Same acceptance

	

showroom:state-machine-rainbow + parity tasks

	

qa:rainbow-* REQUIRES_OFFICIAL_ASSET




All

	

Internal/QA Hebrew strings leaking (בדיקה, דמו, TODO, placeholder)

	

Site-wide grep via crawl

	

P0

	

L

	

H

	

M

	

Remove from public templates

	

Zero matches across audit URLs

	

trust:strip-internal-strings

	

qa:no-internal-strings




All

	

International investor friction: no EN toggle, no currency note, no foreign-buyer disclaimer where relevant

	

DOM inspection

	

P1

	

M

	

H

	

H

	

Add EN stub + "for foreign buyers see X" link (LEGAL_REVIEW)

	

EN toggle visible (even if stub); disclaimer present where tax/legal claims appear

	

i18n:en-stub

	

qa:en-stub LEGAL_REVIEW

3. Technical SEO Checklist (per audited URL)

For each of the seven URLs, verify:

Canonical: exactly one <link rel="canonical">, self-referential, absolute HTTPS, no trailing-slash mismatch.

Title: unique, ≤60 chars, brand suffix consistent, no Lovable App / Just another WordPress site / template defaults.

Meta description: unique, ≤160 chars, no truncation mid-word, no placeholder.

H1: exactly one, meaningful, matches page intent; not the site name on every page.

Heading order: H1 → H2 → H3 with no skips; no H1 inside <header> site logo.

Schema (JSON-LD):

All pages: Organization, WebSite, BreadcrumbList.

Project pages: Residence or ApartmentComplex, Place, Organization (developer).

Estimator: WebApplication + FAQPage (if FAQs present).

Professionals listing: ItemList of Person/LocalBusiness.

Run Rich Results Test — zero errors.

Sitemaps: /sitemap.xml returns 200, valid XML, no placeholder URLs, lastmod present. HTML /sitemap/ page parity.

robots.txt: present, allows crawl, references sitemap; no accidental Disallow: /.

noindex audit: confirm only intended pages (e.g. cart, account, internal) are noindex; confirm no audit URL is noindex by mistake.

hreflang (future EN): at minimum x-default + he-IL stubs now; en slot reserved; no self-referencing errors.

Core Web Vitals: LCP < 2.5s, INP < 200ms, CLS < 0.1 on mobile (PageSpeed Insights field+lab).

Mobile usability: tap targets ≥ 48px, no horizontal scroll at 390, font ≥ 16px for body.

Console: zero errors, zero @wordpress/interactivity warnings, zero CSP violations, zero 404s for assets.

Network: zero 4xx/5xx for first-party assets; no mixed content; HTTP/2 or HTTP/3.

Image hygiene: every <img> has alt; project hero uses loading="eager" fetchpriority="high"; below-fold loading="lazy".

Indexability sanity: curl -A "Googlebot" -sL returns the same primary content as a normal request (no cloaking, no JS-only critical content).

4. Public-Trust Checklist

For each audit URL:

No WooCommerce widgets, cart icon, checkout links, "My Account", or order notices on non-commerce pages.
No notification banners referencing internal events (deploys, cron, plugin updates, license).
No debug output: `var_dump`, `print_r`, PHP notices, React error boundaries, Vite HMR text, stack traces.
No internal terminology: `QA`, `staging`, `בדיקה`, `דמו`, `placeholder`, `TODO`, `lorem`, ticket IDs, JIRA keys.
No dead buttons: every visible CTA either performs its action, opens a real destination, or is removed.
No placeholder content: no "Sample Page", no "Hello world", no stock professional names ("ישראל ישראלי"), no obvious stock photography for project facades.
No fake showroom: project facade is the actual building (`official`) or explicitly labelled `concept` (renders/architect mockups) or `missing`.
No silent fallback: if data is missing, show an honest empty-state — never substitute generic imagery, never invent numbers.
No invented commercial data: prices, square meters, apartment counts, delivery dates, availability must cite source + date or be omitted.
No unlabelled concept assets: renders carry a visible `הדמיה` / `concept` badge.
Author / reviewer / last-updated visible on YMYL content (estimator, professional profiles, legal pages).
International trust: language toggle visible (even if EN is a stub), currency context where prices appear, foreign-buyer disclaimer where tax/legal claims surface (LEGAL_REVIEW).
5. Playwright + Chrome QA Gate

Viewports (mandatory): 1440×900, 768×1024, 390×844. Screenshots at each viewport for each URL → 7 URLs × 3 viewports = 21 baseline screenshots per run.

Per-URL assertions (must all pass):

// trust strings
expect(html).not.toMatchAny([/WooCommerce/i, /cart/i, /סל קניות/, /checkout/i,
                             /var_dump/, /TODO/, /lorem/i, /בדיקה/, /placeholder/i,
                             /staging/i, /QA[-_ ]/])

// h1
expect(page.locator('h1')).toHaveCount(1)

// console
expect(consoleErrors).toHaveLength(0)
expect(consoleWarnings.filter(w => /@wordpress\/interactivity/.test(w))).toHaveLength(0)

// network
expect(failedRequests.filter(r => r.url.startsWith(origin))).toHaveLength(0)
expect(mixedContent).toHaveLength(0)

// horizontal overflow at 390
expect(scrollWidth).toBeLessThanOrEqual(clientWidth)

// head tags
expect(canonical).toBeOneSelfReferential()
expect(title.length).toBeLessThanOrEqual(60)
expect(metaDesc.length).toBeLessThanOrEqual(160)

// dead CTAs
for (const cta of visibleCtas) {
  expect(cta).toHaveResolvableTarget()  // href, onClick handler, or form action
}

Per-URL extra assertions:

/join-pro/: submit form with throwaway data → expect 2xx + visible confirmation (or page is noindex + hidden from nav).

/sitemap/: every link returns 200; zero "Sample Page" titles.

/professionals/: zero cards lack license # or verification badge; filters return correct subsets.

/property-value-estimator/: methodology + last-updated + disclaimer visible; result shows range, not single number; invalid input produces explicit error.

/projects/dimri-yama-sde-dov/ and /projects/rainbow-tel-aviv/: hero data-asset-state ∈ {official, concept, missing}; concept assets carry visible הדמיה badge; every numeric claim has data-source attribute or sibling source line; no duplicate hero/gallery/CTA blocks.

Screenshot naming: screenshots/<run-id>/<viewport>/<url-slug>.png plus screenshots/<run-id>/<viewport>/<url-slug>-fold.png (above-fold only).

Run output: machine-readable report.json + human report.html + raw console.log + network.har per URL.

6. Repo Artifact Layout (suggested for Codex)
audits/
  YYYY-MM-DD-report-1/
    report.html                 # human summary
    report.json                 # machine results (pass/fail per assertion)
    findings.csv                # one row per Section 2 audit row, with current state
    workbook/
      keyword-workbook.xlsx     # touched only by Report 4+; placeholder for now
    screenshots/
      1440/<url-slug>.png
      768/<url-slug>.png
      390/<url-slug>.png
      390/<url-slug>-overflow.png
    network/
      <url-slug>.har
    console/
      <url-slug>.log
    head/
      <url-slug>.head.html
    schema/
      <url-slug>.jsonld.json
      <url-slug>.rich-results.json
qa/
  playwright/
    trust.spec.ts
    seo-head.spec.ts
    showroom-state.spec.ts
    estimator.spec.ts
    join-pro.spec.ts
docs/
  trust-gate.md                 # current BLOCK/PASS state, updated each run
  showroom-state-machine.md     # official|concept|missing contract
  legal/
    estimator-disclaimer.md     # LEGAL_REVIEW
    foreign-buyer-notes.md      # LEGAL_REVIEW

Each Codex task in Section 2 commits under audits/.../findings.csv row update + corresponding code change + updated screenshot(s).

7. Top 10 P0 Fixes (ranked)

Strip WooCommerce / cart / notification residue from all non-commerce templates (home, join-pro, professionals, estimator, project pages). Single biggest trust loss.

Project showroom state machine (official | concept | missing) on Dimri Yama Sde Dov and Rainbow Tel Aviv — no silent fallback, no fake facade, no invented data. REQUIRES_OFFICIAL_ASSET.

Remove dead CTAs site-wide (join-pro, project brochures/floor-plans/contact, estimator).

Purge demo/placeholder professionals and any stock names/photos from /professionals/; show honest empty-state with onboarding CTA.

Estimator disclosure + range output: methodology, sources, last-updated, "not a formal appraisal" disclaimer, confidence range instead of single number. LEGAL_REVIEW.

Rebuild HTML /sitemap/ from real routes; reconcile with /sitemap.xml; remove WP defaults and "Sample Page".

Eliminate @wordpress/interactivity console errors and any other console noise across the seven URLs.

Single H1 per page + correct heading order on home and project pages.

Fix 390px mobile horizontal overflow on home and project pages (constrain offenders, not body).

Internal/QA string purge across templates (בדיקה, דמו, TODO, placeholder, ticket IDs).

International-investor add-ons (P1, scheduled immediately after P0 PASS): EN language toggle stub + hreflang stubs, currency context where prices appear, foreign-buyer disclaimer slot on project + estimator pages (LEGAL_REVIEW).

Labels Recap

ASSUMPTION — every issue in Section 2 is hypothesized from the brief; confirm via the QA gate before fixing.

NEEDS_VERIFICATION — all severity/impact ratings re-scored after the first Playwright run.

LEGAL_REVIEW — estimator disclaimer, foreign-buyer content, any tax/legal claim on project pages.

REQUIRES_OFFICIAL_ASSET — Dimri Yama Sde Dov and Rainbow Tel Aviv hero/gallery/spec data; professional license verification.

READY FOR NEXT PROMPT.

B
I
Title