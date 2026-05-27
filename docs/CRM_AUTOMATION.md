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
