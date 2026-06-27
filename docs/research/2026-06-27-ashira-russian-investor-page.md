# Ashira Sde Dov Russian Buyer Page Research - 2026-06-27

## Scope

This note supports the Russian Ashira Sde Dov draft page. The page is written for Russian-speaking buyers and investors comparing a new apartment in Tel Aviv from Israel or abroad. It is a complete page, not a short translation.

## Sources Checked

- Official Ashira project site: https://ashirabyavisror.com/
- Tel Aviv Municipality Sde Dov district page: https://www.tel-aviv.gov.il/Residents/Development/Pages/SdeDov.aspx
- Gov.il Sde Dov planning announcement: https://www.gov.il/he/pages/sdedov-pr-22072020
- Google Search Central localized versions guidance: https://developers.google.com/search/docs/specialty/international/localized-versions
- Kol Zchut Russian page about purchase tax calculation: https://www.kolzchut.org.il/ru/%D0%A0%D0%B0%D1%81%D1%87%D0%B5%D1%82_%D0%BD%D0%B0%D0%BB%D0%BE%D0%B3%D0%B0_%D0%BD%D0%B0_%D0%BF%D0%BE%D0%BA%D1%83%D0%BF%D0%BA%D1%83_%D0%BD%D0%B5%D0%B4%D0%B2%D0%B8%D0%B6%D0%B8%D0%BC%D0%BE%D1%81%D1%82%D0%B8
- Russian SERP checks around:
  - `купить квартиру в Тель Авиве Sde Dov Ashira`
  - `Ashira Sde Dov квартиры Тель Авив Avisror`
  - `квартиры в новостройке Тель Авив Сде Дов`
  - `покупка квартиры в Израиле иностранцем Тель Авив налог`

## Buyer Intent Observed

- Russian search language tends to combine broad transaction language with Israel/Tel Aviv terms, not only the project name.
- The page should answer the full foreign-buyer path:
  - where the project is
  - what Sde Dov means as a district
  - how to compare apartments
  - how price estimates are treated
  - what documents to request
  - what tax/financing subjects should be checked with professionals
- The page should not present public planning numbers as apartment-specific claims.

## Facts Used In Copy

- District context:
  - `TA/4444`
  - about `1,300` dunams
  - about `16,000` housing units
  - about `40,000` future residents
  - `доступное жилье`
- Project context:
  - Ashira as an Avisror project signal
  - apartment range described as 2 to 5 rooms
  - Avner Yashar and Dana Oberson as design signals from the official site
  - amenities and nearby anchors treated as project-site claims
- Russian buyer context:
  - purchase tax is mentioned as a topic to verify, not as personal advice
  - budget language stays cautious and non-binding

## Page Decisions

- Use ASCII slug `ashira-sde-dov-ru`.
- Keep `lang="ru"` and `dir="ltr"`.
- Reuse the shared Ashira asset folder `assets/projects/ashira-sde-dov/`.
- Keep the same showroom structure as Hebrew, English and French:
  - hero image
  - 3D context model
  - fixed facade selector
  - selected-apartment card
  - long-form Russian guide
  - source and reliability note
- Keep public wording buyer-facing. Avoid internal operational terms.
- Treat all prices, availability and visuals as non-binding until verified.

## QA Evidence

- `npm run qa:ashira-ru-content-depth`
  - 3,119 visible words
  - 18 H2 headings
  - 10 source links found by the gate
  - Cyrillic text present
  - no Hebrew visible text
  - no internal wording leak
- `npm run qa:showroom-v2-ru-preview`
  - desktop, tablet, mobile and Edge-mobile screenshots captured
  - no horizontal overflow
  - one H1
  - model-viewer registered
  - clickable apartment cells present
  - selected card does not overlap the facade

