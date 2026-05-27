# NadLan WordPress Draft Creation Log

Date: 2026-05-27
Executor: Codex acting as operator

## Scope

Updated or created the first NadLan real-estate money-page drafts through the WordPress REST API using the encrypted local app-password helper.

No app password or plaintext credential was written to the repository.

## Research Inputs

- WordPress REST API pages endpoint: https://developer.wordpress.org/rest-api/reference/pages/
- WordPress REST API authentication / application passwords: https://developer.wordpress.org/rest-api/using-the-rest-api/authentication/
- Google people-first content guidance: https://developers.google.com/search/docs/fundamentals/creating-helpful-content
- Google recrawl and sitemap guidance for after publishing: https://developers.google.com/search/docs/crawling-indexing/ask-google-to-recrawl
- Israel Tax Authority purchase tax simulator: https://www.gov.il/en/service/real_eatate_taxsimulator
- Tabu extract official service: https://www.gov.il/he/service/land_registration_extract

## Drafts Updated

| ID | Slug | Status | Title |
| --- | --- | --- | --- |
| 6 | `purchase-tax-calculator` | draft | מחשבון מס רכישה: הערכת עלות לפני קניית דירה |
| 7 | `mortgage-advisor` | draft | יועץ משכנתאות: בדיקת מימון לפני חתימה על דירה |
| 8 | `apartment-buying-checklist` | draft | רשימת בדיקות לפני קניית דירה |
| 10 | `investment-apartment` | draft | דירה להשקעה: בדיקת עסקה לפני התחייבות |
| 11 | `real-estate-lawyer` | draft | עורך דין מקרקעין: בדיקה משפטית לפני חתימה |

## Drafts Created

| ID | Slug | Status | Title |
| --- | --- | --- | --- |
| 17 | `new-projects` | draft | פרויקטים חדשים ודירות מקבלן: התאמת פרויקט לפני פנייה לספק |
| 18 | `tabu-extract-check` | draft | בדיקת נסח טאבו לפני רכישת דירה |

## Still Existing

| ID | Slug | Status | Note |
| --- | --- | --- | --- |
| 9 | `buying-apartment` | draft | Existing buyer pillar; not updated in this pass because the production-priority checklist page is now `apartment-buying-checklist`. |

## Publication Gates

Before publishing:

- Confirm every CTA routes to `nadlan_lead` or a page-specific form that preserves source and UTM fields.
- Add official-source links and visible update dates to tax, Tabu, mortgage, legal, and project sections.
- Add referral/commercial disclosure before broker, lawyer, mortgage, appraiser, inspector, or project handoffs.
- Do not publish tax formulas, mortgage rates, project prices, availability, returns, or legal conclusions without current source and review.
- Confirm final slug redirects if old draft slugs are indexed or internally linked.
- After publishing, submit the sitemap and request recrawl in Search Console for the live URLs.
