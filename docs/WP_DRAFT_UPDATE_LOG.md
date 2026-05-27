# NadLan WordPress Draft Update Log

Date: 2026-05-27
Owner: Codex acting as operator
Site: `nad-lan.co.il`
Method: WordPress REST API via encrypted local application password helper
Status: all pages remain `draft`

## 2026-05-27 Money Page Upgrade

Updated eight draft pages from `docs/MONEY_PAGE_BRIEFS.md` and the buyer-pillar draft.

| ID | Slug | Status | Updated title |
| --- | --- | --- | --- |
| 6 | `purchase-tax-calculator` | draft | `מחשבון מס רכישה: הערכת עלות לפני קניית דירה` |
| 7 | `mortgage-advisor` | draft | `יועץ משכנתאות: בדיקת משכנתא לפני חתימה או הצעה` |
| 8 | `apartment-buying-checklist` | draft | `בדיקות לפני קניית דירה: רשימת בדיקות משפטיות, כספיות ופיזיות` |
| 9 | `buying-apartment` | draft | `קניית דירה בישראל: מפת החלטות לפני חתימה` |
| 10 | `investment-apartment` | draft | `דירה להשקעה: בדיקת עסקה, מימון וסיכונים לפני רכישה` |
| 11 | `real-estate-lawyer` | draft | `עורך דין מקרקעין: בדיקה משפטית לפני חתימת חוזה דירה` |
| 17 | `new-projects` | draft | `פרויקטים חדשים ודירה מקבלן: בדיקת התאמה לפני פנייה` |
| 18 | `tabu-extract-check` | draft | `בדיקת נסח טאבו: מה לבדוק לפני קניית דירה` |

## What Changed

- Reframed pages as decision tools and lead-routing pages, not generic real-estate articles.
- Added commercial-intent sections for:
  - purchase tax estimate
  - mortgage adviser handoff
  - buying checklist
  - buyer pillar/internal hub
  - investment apartment evaluation
  - real-estate lawyer routing
  - new-project / contractor-apartment intake
  - Tabu extract check
- Added CRM-ready CTA language using the existing `/#lead` route.
- Added qualification fields into the copy: city, budget, property type, buyer status, mortgage need, legal need, signing timeline, project/resale preference, and source intent.
- Added guardrails:
  - no binding tax advice
  - no mortgage approval or rate promises
  - no legal conclusions
  - no guaranteed return, price, availability, delivery, or passive income
  - no interpretation of a specific Tabu extract without a lawyer
  - no project/referral handoff without disclosure and consent

## Page-Specific Notes

### `purchase-tax-calculator`

Commercial role: purchase-tax estimate and professional routing.

Added:

- Clear statement that the page is an estimate/routing page, not binding tax advice.
- Inputs to collect before routing: price, city, asset type, buyer status, timeline, mortgage need, legal/tax need.
- Official-source note for Israel Tax Authority simulator and real-estate taxation services.

### `mortgage-advisor`

Commercial role: mortgage adviser qualification.

Added:

- Focus on approval route, bank comparison, repayment structure, and total cost.
- Warning that approval, interest, and terms depend on lender underwriting.
- Bank of Israel source note for mortgage comparison context.

### `apartment-buying-checklist`

Commercial role: buyer lead magnet and professional routing page.

Added:

- Three-layer checklist: legal, financial, physical/planning.
- Routing logic to lawyer, mortgage adviser, appraiser, inspector, and tax professional.
- Clear no legal/engineering conclusion language.

### `buying-apartment`

Commercial role: buyer pillar and internal link hub.

Added:

- Decision map linking to purchase tax, mortgage adviser, checklist, lawyer, and Tabu check pages.
- Lead-quality CTA for buyer stage, city, budget, financing, legal need, and timeline.

### `investment-apartment`

Commercial role: investor lead and partner routing.

Added:

- Cost-stack framing: purchase tax, mortgage, vacancy, management, maintenance, renovation, sale-risk context.
- Professional routing table.
- Strong no-return/no-passive-income guarantee language.

### `real-estate-lawyer`

Commercial role: legal-check lead.

Added:

- What a lawyer reviews: ownership, Tabu, liens, warnings, contract, tax reporting, project documents.
- Urgency table for before-signing and document-risk cases.
- First-contact privacy note: do not send sensitive documents in the initial form.

### `new-projects`

Commercial role: new-build / contractor-apartment lead.

Added:

- Project-fit intake: city, budget, rooms, delivery, equity, mortgage readiness.
- New-build vs resale comparison.
- Disclosure requirement before connecting users to project, broker, developer, or commercial partner.

### `tabu-extract-check`

Commercial role: ownership-check and lawyer-routing lead.

Added:

- What a Tabu extract can show.
- When Tabu is not enough.
- Official gov.il Tabu service note.
- No interpretation of specific extracts without legal review.

## Research Anchors Used

- Google helpful content: https://developers.google.com/search/docs/fundamentals/creating-helpful-content
- Google LocalBusiness structured data: https://developers.google.com/search/docs/appearance/structured-data/local-business
- Israel Tax Authority purchase-tax simulator: https://www.gov.il/en/service/real_eatate_taxsimulator
- Israel Tax Authority real-estate transaction declaration service: https://www.gov.il/en/service/real-estate-tax-7000
- Land Registration extract / Tabu service: https://www.gov.il/he/service/land_registration_extract
- Bank of Israel mortgage comparison / Equalizer: https://www.boi.org.il/information/bank-paymnts/financial-education/campaigns/boi-equator/mortgage/
- Bank of Israel mortgage transparency reform: https://www.boi.org.il/information/bank-paymnts/financial-education/הרפורמה-להגברת-שקיפות-המידע-והתחרות-במשכנתאות/

## Verification

REST verification returned these pages as `draft` after update:

- `purchase-tax-calculator`, modified `2026-05-27T04:53:13`
- `mortgage-advisor`, modified `2026-05-27T04:53:13`
- `apartment-buying-checklist`, modified `2026-05-27T04:53:13`
- `buying-apartment`, modified `2026-05-27T04:53:13`
- `investment-apartment`, modified `2026-05-27T04:53:35`
- `real-estate-lawyer`, modified `2026-05-27T04:53:35`
- `new-projects`, modified `2026-05-27T04:53:35`
- `tabu-extract-check`, modified `2026-05-27T04:53:35`

## Next Steps

1. Verify the lead form captures source page and UTM for each draft URL.
2. Add a real purchase-tax calculator component only after formula/source/update owner are approved.
3. Confirm partner/referral disclosure language for lawyers, mortgage advisers, brokers, projects, appraisers, and inspectors.
4. Add final Hebrew/legal/tax review before publishing.
5. Publish only after production deployment path and CRM test are confirmed.
