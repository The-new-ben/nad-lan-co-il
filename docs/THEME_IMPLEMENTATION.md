# NadLan Theme Implementation

Updated: 2026-05-27

## Files

- `style.css` - theme metadata and RTL real-estate funnel styling.
- `functions.php` - theme setup, `nadlan_lead` CRM CPT, lead handler, admin status workflow, schema, and attribution capture.
- `front-page.php` - Hebrew homepage for buyer, mortgage, purchase-tax, investment, and real-estate-lawyer leads.
- `header.php`, `footer.php`, `index.php` - base WordPress templates.
- `theme.json` - editor palette, layout widths, and Hebrew font stack.

## Commercial Positioning

Primary revenue cluster:

- `purchase-tax-calculator`
- `mortgage-check`
- `buying-checklist`
- `buying-apartment`
- `investment-apartment`
- `real-estate-lawyer`

The site should compete on hard commercial real-estate intent rather than generic property news.

## SEO And Trust

- Front-page schema uses `RealEstateAgent` to describe the real-estate service-routing surface.
- Content must avoid promising mortgage approval, tax outcome, yield, legal result, or property availability.
- Money pages should include practical calculators/checklists, update dates, and professional-review notes where needed.
- Financial, tax, and legal decisions must be routed to qualified professionals.

## CRM Behavior

- Form submission creates a private `nadlan_lead`.
- Required fields: name, phone, consent.
- Anti-spam: hidden honeypot field.
- Stored attribution: landing page, referrer, and UTM fields.
- Admin status can be updated from the lead edit screen.

## UPress Sync Checklist

1. Create a dedicated empty theme folder in UPress file manager.
2. Connect this GitHub branch to that folder only.
3. Do not sync into `/wp-content/themes` root.
4. Run PHP lint in staging or via UPress tooling.
5. Preview the theme without activating on production.
6. Submit a test lead and verify CRM/email/UTM capture.
7. Only then activate.

## Remaining Work

- Add reviewed copy for each draft money page.
- Add mortgage/tax/legal partner routing rules once providers are selected.
- Add calculators only after formulas and disclaimers are verified.
- Add Search Console and conversion events after activation.
