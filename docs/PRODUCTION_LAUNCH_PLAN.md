# NadLan production launch plan

Date: 2026-05-27

## Goal

Turn `nad-lan.co.il` into the second production launch candidate after Robbottx. The money lane is high-intent Israeli real-estate qualification: buyers, sellers, investors, mortgage leads, real-estate lawyers, appraisers, inspection providers, and project/broker referrals.

## Research inputs

- Google LocalBusiness structured data: https://developers.google.com/search/docs/appearance/structured-data/local-business
- Google robots meta/noindex reference: https://developers.google.com/search/docs/crawling-indexing/robots-meta-tag
- Google Search Console recrawl and sitemap guidance: https://developers.google.com/search/docs/crawling-indexing/ask-google-to-recrawl
- Israel Tax Authority purchase tax simulator: https://www.gov.il/en/service/real_eatate_taxsimulator
- Israel Tax Authority real-estate transaction declaration service: https://www.gov.il/en/service/real-estate-tax-7000
- Tabu extract service from the Israeli Land Registration and Settlement of Rights Authority: https://www.gov.il/he/service/land_registration_extract

## Launch position

NadLan should launch second:

1. Real-estate leads can monetize through mortgage advisers, brokers, lawyers, inspectors, appraisers, investment projects, and paid reports.
2. The site can be calculator-led, which creates durable SEO value and lead capture.
3. The risk is manageable if all tax/legal/mortgage content is treated as guidance and routed to professionals rather than presented as advice.

## Production go/no-go checklist

- Confirm staging theme is still active and verified: `NadLan Revenue`.
- Export only the theme/code changes unless a deliberate content/database migration is approved.
- Do not overwrite new production posts, users, comments, leads, forms, or SEO settings from staging.
- Confirm production `home` and `siteurl` remain `https://nad-lan.co.il`.
- Confirm no staging URL remains in menus, schema, canonical tags, CRM form actions, draft links, or assets.
- Confirm staging is blocked from indexing and production is indexable.
- Confirm sitemap output includes only live production URLs after launch.
- Confirm Google Search Console access before requesting recrawl.
- Confirm `nadlan_lead` CRM appears in production after activation.
- Submit one internal production test lead, then delete or clearly mark it as internal.
- Confirm admin email notification works.
- Review `All 404 Redirect to Homepage` or similar redirect plugins before SEO rollout; mass-redirecting 404s to home can hide broken money pages.

## Pages/tools to publish first

| Priority | Page/tool | Intent | CTA |
| --- | --- | --- | --- |
| 1 | `/purchase-tax-calculator/` | `מחשבון מס רכישה`, purchase-tax estimate intent | `בדיקת עסקה עם מומחה` |
| 2 | `/apartment-buying-checklist/` | `קניית דירה`, buyer due-diligence checklist | `קבלת רשימת בדיקות` |
| 3 | `/mortgage-advisor/` | `יועץ משכנתאות`, mortgage lead routing | `בדיקת משכנתא` |
| 4 | `/real-estate-lawyer/` | `עורך דין מקרקעין`, legal-check routing | `בדיקה משפטית לפני חתימה` |
| 5 | `/investment-apartment/` | `דירה להשקעה`, investor qualification | `איתור עסקה להשקעה` |
| 6 | `/new-projects/` | `דירות חדשות`, project and broker referrals | `התאמת פרויקט` |
| 7 | `/tabu-extract-check/` | `נסח טאבו`, ownership/lien check education | `בדיקת נסח לפני רכישה` |

Do not publish calculators with hard-coded tax brackets unless the update date, source, and formula are documented. Prefer a lead/tool page that links to official Tax Authority services until a maintained calculator module is reviewed.

## Content rules

- Every tax page must cite the Israel Tax Authority or an official government service where possible.
- Every legal-check page must say it is not legal advice and route users to a licensed lawyer.
- Every mortgage page must say rates/approval depend on lender underwriting and route users to a qualified adviser.
- Every investment page must avoid guaranteed returns, passive-income promises, or unverified project claims.
- Every project/broker page must disclose referral/commercial relationships before collecting a lead.
- Every page should capture city, budget, asset type, timeline, mortgage need, legal need, and source page.

## CRM routing

Primary staged fields:

- Contact: name, phone, email.
- Intent: buy, sell, invest, mortgage, legal check, appraisal, project match.
- Property context: city, property type, budget, timeline.
- Commercial filters: mortgage need, legal need, urgency, investor/buyer/seller route.
- Attribution: landing URL, referrer, UTM fields.

Qualification priority:

1. Buyer/seller/investor with concrete city, budget, and timeline.
2. Mortgage lead with purchase price/equity estimate.
3. Legal-check lead before signing or during contract review.
4. Appraisal/inspection lead tied to a specific property.
5. Generic "just checking" leads stay in nurture/content.

## Monetization path

1. Mortgage adviser referral/lead fee.
2. Real-estate lawyer referral or paid consultation route.
3. Broker/project referral fee where compliant and disclosed.
4. Paid buyer due-diligence report or checklist review.
5. Later: Grow + Green Invoice for paid reports or consultation invoices after pricing is approved.

## Measurement

- Track lead value by route: mortgage, lawyer, broker/project, inspection/appraisal, investor.
- Track city and budget bands because partner economics vary by transaction value.
- Weekly KPI: qualified leads, professional referrals sent, consultations booked, projected partner revenue.
- First target: 10 qualified leads or 3 active partner conversations before broad content expansion.

## Risks

- Real estate, mortgage, legal, and tax content can affect users financially. Treat it as high-trust/YMYL content.
- Calculator errors can create legal and trust risk. Maintain source dates and formula reviews.
- Private GitHub to uPress Git sync remains blocked until a deploy credential/token method is explicitly approved.
- Do not embed a GitHub token in uPress Git manager until that exact credential method is approved.
