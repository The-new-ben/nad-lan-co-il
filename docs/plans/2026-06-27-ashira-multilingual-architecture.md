# Ashira Multilingual Architecture Gate

Date: 2026-06-27
Status: preflight only. Do not publish, import, or add hreflang until the translated pages exist and pass their own QA.

## Decision

For the first Ashira international version, do not install a sitewide multilingual plugin and do not change the whole site URL structure.

Use separate crawlable WordPress pages for each language, then add reciprocal hreflang only after all pages in the language set exist:

| Language | Page status | Draft slug | Target public title | Direction |
| --- | --- | --- | --- | --- |
| Hebrew | draft-ready | `ashira-sde-dov` | דירות למכירה באשירה שדה דב | rtl |
| English | not written yet | `ashira-sde-dov-en` | Ashira Sde Dov apartments for sale in Tel Aviv | ltr |
| French | not written yet | `ashira-sde-dov-fr` | Appartements à vendre à Ashira Sde Dov, Tel Aviv | ltr |
| Russian | not written yet | `ashira-sde-dov-ru` | Квартиры в Ashira Sde Dov, Тель-Авив | ltr |
| Arabic | draft written, preview QA passed | `ashira-sde-dov-ar` | شقق Ashira Sde Dov للبيع في تل أبيب | rtl |

This is not the final ideal URL architecture. It is the safest first production path because it avoids a broad plugin migration, keeps every slug ASCII, and lets each language page be reviewed independently before it becomes indexable.

## Research Basis

- Google Search Central localized versions: https://developers.google.com/search/docs/specialty/international/localized-versions
  - Use hreflang to connect real localized variants.
  - Each version must reference the other variants and itself.
  - Use fully qualified URLs.
- Yoast hreflang guide: https://yoast.com/hreflang-ultimate-guide/
  - Use hreflang only when the language versions actually exist.
  - Self-links and return links are required.
- Liquid Web WordPress hreflang guide: https://www.liquidweb.com/wordpress/seo/add-hreflang-tags/
  - WordPress paths include plugins, dedicated hreflang tools, or manual theme output.
  - For this site, broad plugin installation is deferred until a staging migration exists.
- Google JavaScript SEO basics: https://developers.google.com/search/docs/crawling-indexing/javascript/javascript-seo-basics
  - Core text, links, headings, project facts and contact paths must be crawlable without relying only on client-side rendering.

## Hreflang Set

Only after all five pages exist, the head tags for each page must include this complete set, with final live URLs:

```html
<link rel="alternate" hreflang="he" href="https://nad-lan.co.il/projects/ashira-sde-dov/" />
<link rel="alternate" hreflang="en" href="https://nad-lan.co.il/ashira-sde-dov-en/" />
<link rel="alternate" hreflang="fr" href="https://nad-lan.co.il/ashira-sde-dov-fr/" />
<link rel="alternate" hreflang="ru" href="https://nad-lan.co.il/ashira-sde-dov-ru/" />
<link rel="alternate" hreflang="ar" href="https://nad-lan.co.il/ashira-sde-dov-ar/" />
<link rel="alternate" hreflang="x-default" href="https://nad-lan.co.il/projects/ashira-sde-dov/" />
```

The exact Hebrew URL may change if Ashira is imported as a page instead of a project CPT. The rule does not change: every language version must list the same complete set, including itself and x-default.

## Content Gate Per Language

Each indexable language page must pass its own gate before publication:

- 3,000+ visible words in that language where appropriate for the query.
- One H1, clear H2 hierarchy, and no article headings pushed sideways.
- Buyer/investor-facing first paragraph.
- Source-backed Sde Dov facts: TA/4444, 16,000 apartments, about 1,300 dunams, about 40,000 planned residents, affordable/special housing context.
- Project facts sourced from the official Ashira site, without copying developer wording.
- Foreign-buyer guidance appropriate to that language: process, documents, legal/tax reminders, financing, currency, and contact.
- Visible non-binding estimate language for price and availability.
- Screenshot QA at desktop, tablet, mobile and Edge-mobile.
- No public internal wording.
- No auto-translation without review.

## Import Order

1. Keep Hebrew Ashira as the source-of-truth draft.
2. Write English from the Hebrew source plus English SERP research.
3. Write French from the source plus French SERP research.
4. Write Russian from the source plus Russian SERP research.
5. Write Arabic from the source plus Arabic SERP research. Done as a draft and preview only.
6. Run content-depth QA per language.
7. Run screenshot QA per language.
8. Only then add reciprocal hreflang and make the pages indexable.

## Arabic Draft Status

The Arabic Ashira draft now exists as `patterns/project-showroom-ashira-v2-ar.php`, with a WordPress import payload at `docs/wp-drafts/ashira-sde-dov-ar-v2-draft.json` and a static QA preview at `docs/previews/ashira-showroom-v2-ar-preview.html`.

It is still not published, not imported, and not connected with hreflang. The safe publication rule remains unchanged: publish language pages only after each page has its own content-depth, screenshot, metadata and internal-link QA.

## Why This Is The Controlled Path

The site needs international buyers, but the wrong multilingual move can damage URL structure and SEO. This path is slower than automatic translation, but safer:

- No broad plugin migration during the first Ashira build.
- No fake language promises.
- No duplicate thin translated pages.
- No hreflang until every return page exists.
- Every language can be checked with screenshots and content gates before publication.
