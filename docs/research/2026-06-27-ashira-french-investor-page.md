# Ashira Sde Dov French Buyer Page Research - 2026-06-27

## Scope

This note supports the French Ashira Sde Dov draft page. The goal is a real buyer/investor page, not a short translation. The page is meant for French-speaking buyers comparing new Tel Aviv apartments from abroad and needs to explain project context, apartment selection, estimates, documents and verification steps.

## Sources Checked

- Official Ashira project site: https://ashirabyavisror.com/
- Tel Aviv Municipality Sde Dov district page: https://www.tel-aviv.gov.il/Residents/Development/Pages/SdeDov.aspx
- Gov.il Sde Dov planning announcement: https://www.gov.il/he/pages/sdedov-pr-22072020
- Google Search Central localized versions guidance: https://developers.google.com/search/docs/specialty/international/localized-versions
- French/English SERP checks around:
  - `appartements a vendre Ashira Sde Dov Tel Aviv`
  - `acheter appartement Sde Dov Tel Aviv francais`
  - `Ashira Sde Dov appartement Tel Aviv`
  - `Sde Dov Tel Aviv projet immobilier francais`

## Buyer Intent Observed

- French-specific public results are thin, which means the page should not be a short duplicate. It should answer the foreign-buyer questions directly.
- Core query language should combine project name, location and transaction language:
  - `Ashira Sde Dov`
  - `appartements a vendre`
  - `Tel Aviv`
  - `quartier Sde Dov`
  - `acheteurs etrangers`
- The page needs more than project marketing. It needs practical buyer proof: what to verify, what documents to request, how estimates are handled and how district-scale facts differ from apartment-specific facts.

## Facts Used In Copy

- Sde Dov is treated as a district-scale redevelopment, not only a single-building claim.
- District facts used in the French copy:
  - `TA/4444`
  - about `1,300` dunams
  - about `16,000` housing units
  - about `40,000` future residents
  - reference to `logement abordable`
- Project facts used from Ashira's official site:
  - Avisror as the project brand/developer signal
  - apartment range described as 2 to 5 rooms
  - Avner Yashar and Dana Oberson named as design signals
  - amenities and nearby anchors described as project-site claims, not as verified apartment-specific facts

## Page Decisions

- Use a full French page, not a language stub.
- Keep the same showroom structure as Hebrew and English:
  - hero image
  - 3D context model
  - fixed facade picker
  - selected-apartment card
  - French long-form guide
  - source and reliability note
- Keep asset folder shared as `assets/projects/ashira-sde-dov/`; translated pages get their own ASCII slug but reuse the same approved media.
- Keep public wording buyer-facing. Avoid internal terms such as SEO, CMS, CRM, funnel, project manager, supplier, prototype, factory, placeholder or monetization.
- Treat all prices and availability as non-binding until verified.

## QA Evidence

- `npm run qa:ashira-fr-content-depth`
  - 3,769 visible words
  - 18 H2 headings
  - 9 source links found by the gate
  - no Hebrew visible text
  - no internal wording leak
- `npm run qa:showroom-v2-fr-preview`
  - desktop, tablet, mobile and Edge-mobile screenshots captured
  - no horizontal overflow
  - one H1
  - model-viewer registered
  - clickable apartment cells present
  - selected card does not overlap the facade

