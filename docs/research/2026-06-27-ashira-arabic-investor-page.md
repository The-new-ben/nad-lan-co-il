# Ashira Arabic Foreign-Buyer Page - 2026-06-27

## Purpose

Add the missing Arabic Ashira draft page to the controlled showroom factory. This page is for Arabic-speaking buyers and investors who need to understand the apartment, the district, the documents and the non-binding estimate path before contacting a representative.

## Sources Checked

- Official Ashira project source: `https://ashirabyavisror.com/`
- Tel Aviv municipality Sde Dov district source: `https://www.tel-aviv.gov.il/Residents/Development/Pages/SdeDov.aspx`
- Gov.il Sde Dov planning announcement: `https://www.gov.il/he/pages/sdedov-pr-22072020`
- Kol Zchut purchase tax calculator/source: `https://www.kolzchut.org.il/he/חישוב_מס_רכישה`
- Google localized versions / hreflang: `https://developers.google.com/search/docs/specialty/international/localized-versions`

## Page Decision

- Use a full Arabic RTL project page, not a short language card.
- Keep the same v2 showroom contract as Hebrew, English, French and Russian.
- Keep buyer-facing language only: apartment, project, district, availability, estimate, documents and representative.
- Avoid final price claims. Use Arabic equivalent of "non-binding estimate" until verified inventory and price data exist.
- Keep source-backed district numbers: TA/4444, about 1,300 dunams, about 16,000 housing units and about 40,000 planned residents.

## Factory Evidence

- Pattern: `patterns/project-showroom-ashira-v2-ar.php`
- Preview: `docs/previews/ashira-showroom-v2-ar-preview.html`
- Draft payload: `docs/wp-drafts/ashira-sde-dov-ar-v2-draft.json`
- Content QA: `scripts/qa-ashira-ar-content-depth.mjs`
- Screenshot QA: `npm run qa:showroom-v2-ar-preview`

## Not Yet Done

- No live WordPress import.
- No publication.
- No reciprocal hreflang output.
- No official Ashira BIM/IFC or verified unit inventory.
