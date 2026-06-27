# Ashira Multilingual Architecture Gate

Date: 2026-06-27
Status: preflight only. Do not publish, import, or add hreflang until the language pages exist on their final URLs and pass their own QA.

## Decision

For the first Ashira international release, do not install a sitewide multilingual plugin and do not change the whole site URL structure.

Use separate crawlable `nadlan_project` drafts for each language. Because they are project CPT drafts, every target URL must sit under `/projects/`, not at the site root.

The machine-readable source of truth is:

- `docs/plans/2026-06-27-ashira-publication-manifest.json`
- Gate: `npm run qa:ashira-publication-readiness`
- Full aggregate gate: `npm run qa:ashira-full-preflight`
- Hreflang preflight files:
  - `docs/seo/ashira-hreflang-map.json`
  - `docs/seo/ashira-hreflang-head.html`
  - `docs/qa/project-hreflang-artifact-report.json`
- Import dry-run proof:
  - `docs/qa/project-draft-import-dry-run-report.json`

## Current Language Set

| Language | Status | Draft slug | Target public URL | Direction |
| --- | --- | --- | --- | --- |
| Hebrew | draft-ready, preview QA passed | `ashira-sde-dov` | `https://nad-lan.co.il/projects/ashira-sde-dov/` | rtl |
| English | draft-ready, preview QA passed | `ashira-sde-dov-en` | `https://nad-lan.co.il/projects/ashira-sde-dov-en/` | ltr |
| French | draft-ready, preview QA passed | `ashira-sde-dov-fr` | `https://nad-lan.co.il/projects/ashira-sde-dov-fr/` | ltr |
| Russian | draft-ready, preview QA passed | `ashira-sde-dov-ru` | `https://nad-lan.co.il/projects/ashira-sde-dov-ru/` | ltr |
| Arabic | draft-ready, preview QA passed | `ashira-sde-dov-ar` | `https://nad-lan.co.il/projects/ashira-sde-dov-ar/` | rtl |

This is not a final multilingual-platform migration. It is the safe first production path because it avoids a broad plugin migration, keeps every slug ASCII, keeps every language page reviewable independently, and avoids fake language links.

## Research Basis

- Google Search Central localized versions: https://developers.google.com/search/docs/specialty/international/localized-versions
  - Use hreflang to connect real localized variants.
  - Each version must reference the other variants and itself.
  - Use fully qualified URLs.
- Yoast hreflang guide: https://yoast.com/hreflang-ultimate-guide/
  - Use hreflang only when language versions actually exist.
  - Self-links and return links are required.
- Liquid Web WordPress hreflang guide: https://www.liquidweb.com/wordpress/seo/add-hreflang-tags/
  - WordPress can use plugins, dedicated hreflang tools, or manual theme output.
  - For this site, broad plugin installation is deferred until a staging migration exists.
- Google JavaScript SEO basics: https://developers.google.com/search/docs/crawling-indexing/javascript/javascript-seo-basics
  - Core text, links, headings, project facts and contact paths must be crawlable without relying only on client-side rendering.

## Hreflang Set

Only after all five pages exist at their final URLs, every page in the set must include the same complete reciprocal set:

```html
<link rel="alternate" hreflang="he" href="https://nad-lan.co.il/projects/ashira-sde-dov/" />
<link rel="alternate" hreflang="en" href="https://nad-lan.co.il/projects/ashira-sde-dov-en/" />
<link rel="alternate" hreflang="fr" href="https://nad-lan.co.il/projects/ashira-sde-dov-fr/" />
<link rel="alternate" hreflang="ru" href="https://nad-lan.co.il/projects/ashira-sde-dov-ru/" />
<link rel="alternate" hreflang="ar" href="https://nad-lan.co.il/projects/ashira-sde-dov-ar/" />
<link rel="alternate" hreflang="x-default" href="https://nad-lan.co.il/projects/ashira-sde-dov/" />
```

The snippet above is now generated from the publication manifest, not typed by hand:

```bash
npm run build:project-hreflang-artifact
npm run qa:project-hreflang-artifact
```

This remains a preflight artifact only. Do not place it in the live `<head>` until every URL in the
set is published, indexable and screenshot-verified.

## Content Gate Per Language

Each indexable language page must pass its own gate before publication:

- 3,000+ visible words where appropriate for the query.
- One H1, clear H2 hierarchy, and no article headings pushed sideways.
- Buyer/investor-facing first paragraph.
- Source-backed Sde Dov facts: TA/4444, 16,000 apartments, about 1,300 dunams, about 40,000 planned residents, and affordable/special housing context.
- Project facts sourced from the official Ashira site, without copying developer wording.
- Foreign-buyer guidance appropriate to that language: process, documents, legal/tax reminders, financing, currency, and contact.
- Visible non-binding estimate language for price and availability.
- Screenshot QA at desktop, tablet, mobile and Edge-mobile.
- No public internal wording.
- No auto-translation without review.

## Publication Order

1. Keep all five pages as drafts until the owner approves publication.
2. Run content-depth QA for every language.
3. Run screenshot QA for every language.
4. Build and verify the preflight hreflang artifact.
5. Run the manifest-level WordPress draft import dry-run.
6. Run `npm run qa:ashira-publication-readiness`.
7. Import only as draft first.
8. Verify the rendered WordPress draft URLs with screenshots.
9. Add reciprocal hreflang only after every language page has a real final URL.
10. Make pages indexable only after the final live verification.

Before any owner review or import attempt, run the aggregate gate:

```bash
npm run qa:ashira-full-preflight
```

It executes the research, architecture, content-depth, screenshot, factory, draft, hreflang,
import dry-run, project-publication and homepage-dependency gates together and writes
`docs/qa/ashira-full-preflight-report.json`. A green individual report is not enough if the
aggregate report is stale or red.

## Why This Is The Controlled Path

The site needs international buyers, but the wrong multilingual move can damage URL structure and SEO. This path is slower than automatic translation, but safer:

- No broad plugin migration during the first Ashira build.
- No fake language promises.
- No duplicate thin translated pages.
- No root-path collision for project pages.
- No hreflang until every return page exists.
- Every language can be checked with screenshots and content gates before publication.
