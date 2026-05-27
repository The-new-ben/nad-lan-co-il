# NadLan Money Page Briefs

Date: 2026-05-27
Owner: Codex acting as operator
Scope: first production content wave for `nad-lan.co.il`

## Research Inputs

- Google people-first content guidance: https://developers.google.com/search/docs/fundamentals/creating-helpful-content
- Google LocalBusiness structured data guidance: https://developers.google.com/search/docs/appearance/structured-data/local-business
- Google recrawl and sitemap guidance for after publishing: https://developers.google.com/search/docs/crawling-indexing/ask-google-to-recrawl
- Israel Tax Authority purchase tax simulator: https://www.gov.il/en/service/real_eatate_taxsimulator
- Israel Tax Authority real-estate transaction declaration service: https://www.gov.il/en/service/real-estate-tax-7000
- Land registration extract / Tabu service: https://www.gov.il/he/service/land_registration_extract
- Real-estate registration status service: https://www.gov.il/he/service/real-estate-registration-status
- Licensed real-estate appraiser database: https://www.gov.il/he/Departments/DynamicCollectors/search-appraisers
- Professional disciplinary unit for licensed professionals, including real-estate brokers and appraisers: https://www.gov.il/he/Departments/Units/disciplinary-prosecution

## Content Strategy

NadLan should win through decision tools and high-trust lead routing, not generic real-estate articles.

The first content wave should help a user answer one of five expensive questions:

1. What will this transaction cost me?
2. What must I check before signing?
3. Who should review the mortgage, legal, tax, appraisal, or project risk?
4. Is this property or project suitable for my budget and timeline?
5. Which professional should get this lead next?

Each page should preserve city, budget, asset type, timeline, mortgage need, legal need, source page, and UTM fields into `nadlan_lead`.

## Current WordPress Draft Map

Existing drafts:

| ID | Current slug | Production role |
| --- | --- | --- |
| 6 | `purchase-tax-calculator` | Keep as priority 1 |
| 7 | `mortgage-check` | Should become or redirect to `/mortgage-advisor/` |
| 8 | `buying-checklist` | Should become or redirect to `/apartment-buying-checklist/` |
| 9 | `buying-apartment` | Buyer pillar / internal link hub |
| 10 | `investment-apartment` | Keep as priority investor page |
| 11 | `real-estate-lawyer` | Keep as legal-check page |

Missing production-priority drafts to create next:

- `/new-projects/`
- `/tabu-extract-check/`

Slug decision before production:

- Prefer clear production slugs from `docs/PRODUCTION_LAUNCH_PLAN.md`.
- If existing draft URLs already have internal history, use 301 redirects from old slugs to final slugs after publishing.

## Page 1: Purchase Tax Calculator

Slug: `/purchase-tax-calculator/`

Primary intent:

- `מחשבון מס רכישה`
- `מס רכישה דירה ראשונה`
- `מס רכישה דירה שנייה`
- `חישוב מס רכישה`

Buyer:

- Apartment buyer before signing
- Investor comparing deal cost
- Buyer with lawyer/mortgage need

CTA:

- `בדיקת עסקה עם מומחה`

Required sections:

- Clear warning: this is an estimate / routing page, not binding tax advice.
- Link to the official Israel Tax Authority simulator.
- Explain the inputs: purchase price, first/only apartment, replacement apartment, additional apartment, resident/nonresident considerations where reviewed.
- Checklist before relying on a number: contract price, linked expenses, buyer status, family status, deadlines, exemptions/reliefs.
- Lead capture: price, city, asset type, buyer status, timeline, lawyer need, mortgage need.
- Partner routes: real-estate lawyer, tax professional, mortgage adviser.

Do not publish:

- Hard-coded tax brackets unless formula, source, update date, and review owner are documented.
- Any sentence implying final tax liability without professional review.

## Page 2: Apartment Buying Checklist

Preferred slug: `/apartment-buying-checklist/`
Current draft slug: `buying-checklist`

Primary intent:

- `קניית דירה`
- `בדיקות לפני קניית דירה`
- `רשימת בדיקות לקניית דירה`
- `בדיקת דירה לפני קניה`

Buyer:

- First-time buyer
- Family upgrading apartment
- Buyer before signing
- Buyer who needs lawyer, mortgage adviser, appraiser, or inspector

CTA:

- `קבלת רשימת בדיקות`

Required sections:

- Legal checks: Tabu extract, ownership, liens, easements, warnings, shared house details.
- Financial checks: purchase tax, mortgage approval, equity, payment schedule, extra costs.
- Physical checks: inspection, building age, defects, systems, renovations.
- Planning checks: permits, extensions, city planning, neighborhood risk.
- Professional routing: lawyer, appraiser, inspector, mortgage adviser.
- Lead form route: city, budget, property type, signing timeline, mortgage need, legal need.

Do not publish:

- Legal advice or final safety/defect conclusions.
- A checklist that implies all properties are the same.

## Page 3: Mortgage Advisor

Preferred slug: `/mortgage-advisor/`
Current draft slug: `mortgage-check`

Primary intent:

- `יועץ משכנתאות`
- `בדיקת משכנתא`
- `אישור עקרוני משכנתא`
- `משכנתא לדירה להשקעה`

Buyer:

- Buyer before offer or contract
- Investor comparing leverage
- Buyer who needs approval and monthly payment estimate

CTA:

- `בדיקת משכנתא`

Required sections:

- What a mortgage adviser can help with: approval route, bank comparison, repayment structure, insurance, timeline.
- Inputs: purchase price, equity, income, obligations, city, property type, contract timeline.
- Warning: approval, interest, and terms depend on lender underwriting.
- Lead quality questions: already signed or not, first apartment or investor, mortgage amount, urgency.
- Cross-links: purchase tax, buying checklist, investment apartment.

Do not publish:

- Rate promises.
- Bank approval promises.
- Example payments without source/date/assumptions.

## Page 4: Real Estate Lawyer

Slug: `/real-estate-lawyer/`

Primary intent:

- `עורך דין מקרקעין`
- `עורך דין קניית דירה`
- `בדיקה משפטית לפני חתימה`
- `חוזה מכר דירה`

Buyer:

- Buyer or seller before signing
- Buyer with Tabu/project concern
- Investor needing contract/tax/legal review

CTA:

- `בדיקה משפטית לפני חתימה`

Required sections:

- What a lawyer reviews: ownership, liens, warnings, contract, payment schedule, tax reporting, registration route, project/developer documents.
- What the site does: routes a lead and organizes context; it does not give legal advice.
- Urgency rules: before signing, during negotiation, after discovering registration issue.
- Lead fields: city, property type, stage, counterparty, signing deadline, documents available.
- Cross-links: Tabu extract check, purchase tax, buying checklist.

Do not publish:

- Legal conclusions about a user's deal.
- Fee promises, result promises, or unreviewed lawyer advertising claims.

## Page 5: Investment Apartment

Slug: `/investment-apartment/`

Primary intent:

- `דירה להשקעה`
- `דירות להשקעה בישראל`
- `השקעות נדלן בישראל`
- `איפה כדאי לקנות דירה להשקעה`

Buyer:

- Investor with budget
- Buyer comparing cities/projects
- User who may need broker/project referral, mortgage, lawyer, appraiser

CTA:

- `איתור עסקה להשקעה`

Required sections:

- Investor profile: budget, equity, city preference, risk tolerance, rent expectations, holding period.
- Cost stack: purchase tax, lawyer, broker, mortgage, renovation, vacancy, maintenance, management, sale tax considerations.
- Risk questions: tenant risk, liquidity, project delay, neighborhood change, financing stress.
- Professional routing: mortgage, lawyer, appraiser, broker/project partner.
- Lead form route: budget, city, timeline, mortgage need, project/resale preference.

Do not publish:

- Guaranteed return or passive-income promises.
- Unverified project claims or "best city" claims without source and update date.

## Page 6: New Projects

Slug: `/new-projects/`

Primary intent:

- `דירות חדשות`
- `פרויקטים חדשים`
- `דירה מקבלן`
- `דירות חדשות למכירה`

Buyer:

- Buyer considering contractor/developer projects
- Investor evaluating project launch
- Family comparing new-build vs resale

CTA:

- `התאמת פרויקט`

Required sections:

- Project-fit intake: city, budget, rooms, delivery timeline, equity, mortgage readiness.
- Checks before referral: developer/contractor identity, registration route, permits, expected delivery, indexation, payment schedule, guarantees.
- Route to lawyer/mortgage adviser before contract.
- Referral disclosure: if the site sends the lead to a broker/project/supplier, commercial terms must be disclosed.
- Cross-links: buying checklist, mortgage adviser, real-estate lawyer.

Do not publish:

- Specific project availability, price, delivery, or yield unless partner-confirmed with date.
- Project rankings without evidence and commercial disclosure.

## Page 7: Tabu Extract Check

Slug: `/tabu-extract-check/`

Primary intent:

- `נסח טאבו`
- `בדיקת נסח טאבו`
- `הפקת נסח טאבו`
- `בדיקת בעלות דירה`

Buyer:

- Buyer before signing
- Seller preparing documents
- Investor checking ownership/risk

CTA:

- `בדיקת נסח לפני רכישה`

Required sections:

- Explain what a Tabu extract can show: registered owners, mortgages, liens, court orders, restrictions, and other registrations.
- Link to official land registration extract service.
- Explain when Tabu is not enough: company housing, Israel Land Authority, project registration, shared house docs, legal interpretation.
- Lead route: property city, block/parcel if known, purchase stage, lawyer need.
- Cross-links: real-estate lawyer, buying checklist, purchase tax.

Do not publish:

- Interpretations of a specific extract without a lawyer.
- Instructions that bypass official government services.

## Internal Link Plan

- Homepage links to all seven pages/tools.
- `purchase-tax-calculator` links to `real-estate-lawyer`, `mortgage-advisor`, and `investment-apartment`.
- `apartment-buying-checklist` links to `tabu-extract-check`, `real-estate-lawyer`, `mortgage-advisor`, and `purchase-tax-calculator`.
- `mortgage-advisor` links to `purchase-tax-calculator`, `buying-apartment`, and `investment-apartment`.
- `real-estate-lawyer` links to `tabu-extract-check`, `purchase-tax-calculator`, and `apartment-buying-checklist`.
- `investment-apartment` links to `purchase-tax-calculator`, `mortgage-advisor`, and `new-projects`.
- `new-projects` links to `real-estate-lawyer`, `mortgage-advisor`, and `apartment-buying-checklist`.
- `tabu-extract-check` links to `real-estate-lawyer` and `apartment-buying-checklist`.

## Production Readiness Tasks

1. Update existing WordPress drafts with the content structure above.
2. Create missing drafts for `/new-projects/` and `/tabu-extract-check/`.
3. Decide whether to rename existing draft slugs or publish with redirects.
4. Add official-source sections and update dates.
5. Confirm all CTAs route into `nadlan_lead` or a page-specific lead form that preserves UTM/source.
6. Add affiliate/referral disclosure before any broker/project/professional handoff.
7. After production activation, submit sitemap and request recrawl for the live URLs through Search Console.
