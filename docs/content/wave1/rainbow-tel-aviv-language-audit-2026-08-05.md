# Rainbow Tel Aviv foreign-language existence audit

Audit date: 5 August 2026  
Method: read-only inspection in the user's real Google Chrome browser  
Decision: create no new Rainbow language articles

## Existence result

All four foreign-language pages already exist as distinct `nadlan_project` posts. Each requested URL returned HTTP 200 without a redirect, and the final URL matched the requested URL.

| Language | URL suffix | Post ID | HTML language and direction | Localized article depth |
|---|---|---:|---|---:|
| English | `rainbow-tel-aviv-en` | 5060 | `en`, LTR | 3,088 words |
| French | `rainbow-tel-aviv-fr` | 5071 | `fr`, LTR | 4,478 words |
| Russian | `rainbow-tel-aviv-ru` | 5072 | incorrectly `iw`, computed LTR | 3,037 words |
| Arabic | `rainbow-tel-aviv-ar` | 5074 | incorrectly `iw`, RTL | 3,032 words |

Direct pages:

- https://nad-lan.co.il/projects/rainbow-tel-aviv-en/
- https://nad-lan.co.il/projects/rainbow-tel-aviv-fr/
- https://nad-lan.co.il/projects/rainbow-tel-aviv-ru/
- https://nad-lan.co.il/projects/rainbow-tel-aviv-ar/

## Translation-cluster result

Each page has one localized H1, a self-referencing canonical, index/follow robots and the same six-link hreflang cluster: Hebrew, English, French, Russian, Arabic and x-default pointing to Hebrew. These are existing language siblings, not missing URLs.

Creating new French or Arabic articles would violate the instruction to create only missing versions and could create duplicate-content risk. Rainbow is therefore excluded from new-content generation and from the combined content deliverable.

## Quality backlog for a future refresh

- All four foreign-language articles are below the 5,000-word standard.
- French, Russian and Arabic use the same 14-H2, 70-paragraph translated structure rather than culturally distinct content products.
- The English composition is separate but still only about 3,088 words in the rendered article.
- Every foreign-language page outputs a Hebrew meta description.
- Hebrew interface and breadcrumb text appears before the localized article.
- Structured data declares `inLanguage: he-IL` on every foreign-language page.
- Russian and Arabic incorrectly output `lang="iw"`.
- The French H1 is unaccented: `Rainbow Tel Aviv | Residence balneaire a Sde Dov`.
- Every page carries an `rtl` body class, although computed direction is LTR for English, French and Russian and RTL for Arabic.

These issues require a separate refresh authorization because the user's current rule is to leave existing Rainbow languages untouched. No page, post, code, canonical, hreflang or file on the live site was modified during this audit.

