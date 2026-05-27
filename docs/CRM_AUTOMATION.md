# NadLan CRM Automation Notes

## Current theme CRM

- Lead source: front-page form in `front-page.php`.
- Storage: private WordPress custom post type `nadlan_lead`.
- Required fields: name, phone, consent checkbox.
- Captured fields: email, goal, city, budget, timeline, message, landing URL, referrer URL, UTM source/medium/campaign/term/content.
- Default status: `new`.
- Admin statuses: `new`, `qualified`, `contacted`, `partner_sent`, `closed_won`, `closed_lost`.
- Notification: `wp_mail()` to the site admin email.

## Lead routing model

1. Real estate purchase or sale leads go first to qualification.
2. Mortgage leads route to a mortgage adviser after phone validation.
3. Purchase tax and legal check leads route to lawyer/tax partner offers.
4. Investment-apartment leads need budget, target city, and timeline before partner handoff.
5. Every partner handoff must set status to `partner_sent` and record the partner outside the public page.

## App-password policy

Use WordPress Application Passwords only for API publishing/automation. Create a named password per automation user, never commit it to GitHub, and revoke it immediately if the machine or workflow changes.

Reference: https://developer.wordpress.org/rest-api/reference/application-passwords/

## SEO and measurement policy

The homepage and money pages should keep:

- Hebrew `dir="rtl"` and `lang="he-IL"`.
- Fast code-first markup with no page-builder dependency for critical pages.
- Structured data only when it accurately matches visible content.
- Clear consent and source attribution for leads.
- Core Web Vitals-friendly CSS and minimal frontend JavaScript.

References:

- https://developers.google.com/search/docs/fundamentals/seo-starter-guide
- https://developers.google.com/search/docs/appearance/page-experience
- https://developer.wordpress.org/themes/

## 2026-05-27 Initial Status Routing

New leads no longer all start as `new`.

- Leads with at least two useful qualification signals among goal, city, budget, and timeline start as `qualified`.
- Thin or incomplete leads remain `new` for manual review.

## 2026-05-27 Conversion Measurement

When the stored-lead redirect reaches `?lead=received`, the theme pushes a privacy-safe `generate_lead` event into `window.dataLayer`.

Payload fields: `event`, `lead_form`, `portfolio_site`, `lead_result`, and `conversion_source`.

No personally identifiable information, buyer details, message text, budget, or deal data is sent in this browser event. Configure GTM/GA4 to treat `generate_lead` as the lead key event after production deployment.

## 2026-05-27 Admin Source Columns

The NadLan Leads admin list shows `UTM source` and `Landing URL` beside the core triage fields so operators can quickly spot which campaigns and pages are producing leads.

Open the private lead detail screen for the full attribution record, including referrer URL and the complete UTM set.

## 2026-05-27 Revenue Board

The NadLan Leads menu includes a `Revenue Board` submenu. It summarizes the latest 50 private leads by status, UTM source, and landing URL, then lists the latest leads with edit links.

Use it for weekly revenue triage: identify which pages and campaigns are producing qualified real-estate opportunities before prioritizing new SEO work, partner outreach, or paid tests.

The `Export board CSV` button downloads only board-level fields: lead ID, date, status, priority, score, UTM source/medium/campaign, landing URL, and the private admin edit URL. It intentionally excludes name, phone, email, message, budget, city, and deal details.

## 2026-05-27 Lead Priority Scoring

New leads get an operator-only score and priority band: `Hot`, `Warm`, or `Watch`. NadLan scoring favors goal, city, budget, timeline, and numeric budget signals.

The score is for queue priority only. It does not guarantee mortgage approval, legal/tax outcome, partner acceptance, conversion, price, or revenue.
