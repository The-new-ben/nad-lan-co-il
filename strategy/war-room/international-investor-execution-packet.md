# International Investor Execution Packet

Date: 2026-06-23

Status: build-ready specification, not live implementation.

## Purpose

This packet defines the international investor layer for NadLan:

- foreign buyers buying property in Israel
- English investor pages
- project/showroom paths for premium contractor sales
- tax, mortgage, trust, and professional routing
- concierge lead handling
- future Israeli-investor-abroad pages for Cyprus, Greece, Dubai, Thailand, and similar markets

The key rule: international pages are not translated Hebrew pages. They are written for the foreign buyer's actual concerns.

## Core Decision

Build English for Israel first. Keep future countries separate and controlled.

1. `/en` and child pages serve people buying in Israel.
2. `/abroad/{country}` serves Israelis considering investment abroad.
3. Future country pages remain noindex until official country source packs and local legal review exist.

This preserves NadLan's Israeli real-estate authority while still allowing long-range expansion.

## First English Pages

The first indexable English slice should be:

- `/en`
- `/en/buy-property-israel`
- `/en/buy/tel-aviv`
- `/en/projects/tel-aviv`
- `/en/tax/foreign-buyer-purchase-tax`
- `/en/mortgage/foreign-buyers`

These pages connect SEO demand, project monetization, legal/tax trust, mortgage intent, and concierge leads.

## Page Map

The structured page plan is in:

- `international-investor-page-map.csv`

It covers:

- English hub pages
- English city pages
- English project/showroom routes
- tax and mortgage guides
- professional categories
- trust pages
- future abroad country pages

## Source Gates

Do not publish high-risk pages without source review.

Official sources used for this specification:

- Israel Tax Authority real estate taxation: https://www.gov.il/en/departments/topics/realty_taxation
- Israel Tax Authority purchase tax simulator: https://www.gov.il/en/service/real_eatate_taxsimulator
- Israel Tax Authority property declaration service: https://www.gov.il/en/service/real-estate-tax-7000
- Bank of Israel: https://www.boi.org.il/en/
- Google international SEO guidance: https://developers.google.com/search/docs/specialty/international/managing-multi-regional-sites

## Legal And Tax Boundary

Public pages must not:

- promise tax treatment
- publish tax brackets without date and source
- promise mortgage approval, rates, or LTV
- claim local country rules for Cyprus, Greece, Dubai, or Thailand without local counsel review
- imply that an asset, unit, view, or tour is real if it is missing or illustrative

Public pages must:

- show source dates where facts are used
- route tax and legal questions to qualified professionals
- use clear caveats
- keep contact details out of analytics
- carry internal reviewer status before publication

## Concierge Funnel

The foreign-buyer concierge should collect:

- country
- language
- budget band
- preferred city or project
- intent: own, invest, aliyah, family, relocation
- timeline
- preferred contact channel
- consent

Analytics receives only context and bands. CRM/form storage holds the contact details.

## Showroom Requirements

English project pages and showroom pages must support:

- asset status
- official source notes
- unit interest
- floor plan or honest missing state
- view/surroundings layer when available
- interior tour only if real or clearly illustrative
- concierge CTA
- save/share path for remote buyers

No fake 3D proof.

## Future Abroad Track

The abroad expansion is allowed but not mixed into the Israel buyer funnel.

Initial country order:

1. Cyprus
2. Greece
3. Dubai/UAE
4. Thailand

Each country needs:

- official government or regulator sources
- local legal review
- tax caveat
- asset permission rules
- project partner verification
- noindex until reviewed

## Acceptance Gate

The international investor packet is ready to implement when:

- the owner approves the first English page set
- source gates are assigned to each legal/tax/finance page
- concierge lead fields are approved
- project assets are verified
- screenshot requirements are accepted
- no country-abroad page is indexable before review

## Files In This Packet

- `international-investor-page-map.csv`
- `international-investor-execution-packet.csv`
- `international-investor-execution-packet.md`
- `international-investor-execution-packet-rtl.html`
- `international-investor-execution-packet-preview.png`
- `international-investor-execution-packet-preview-mobile.png`
- `international-investor-execution-packet-visual-qa.md`
