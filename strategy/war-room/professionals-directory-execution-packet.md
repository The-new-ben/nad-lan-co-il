# Professionals Directory Execution Packet

Date: 2026-06-23

Status: build-ready specification, not a live implementation.

## Purpose

NadLan needs a professional layer that supports real-estate decisions without becoming a fake review site, a thin directory, or a cannibalization risk. The professional system should help users find the right support by category, city, language, transaction stage, and verification state. It must also create a measurable referral surface for NadLan while preserving trust.

This packet closes the previous P0 gap:

> Need verification methodology, profile schema, sponsored/review policy, category/city templates, contact routing.

## Core Page Model

| Page family | Role | Indexing rule |
| --- | --- | --- |
| `professionals_hub` | Main professional entry point | Index only with useful category navigation and verification policy |
| `professional_category` | Category directory | Index when category has real profile supply or substantial category value |
| `professional_city_category` | Local service directory | Index only when not thin and when it owns local service intent |
| `professional_profile` | Provider/entity conversion page | Index only after owner approval and safe verification state |

## Professional Categories

The first working category set:

1. Real-estate lawyer
2. Appraiser
3. Mortgage advisor
4. Tax advisor
5. Interior designer
6. Architect
7. Inspector or engineer
8. Broker or agent
9. Property manager
10. Foreign-buyer concierge
11. Contractor or developer contact
12. Insurance advisor

## Verification Statuses

The status system is defined in `professionals-verification-policy.csv`:

- `pending`
- `claimed`
- `document_verified`
- `license_verified`
- `owner_approved`
- `rejected`
- `suspended`
- `stale`

Sensitive categories such as lawyers, tax advisors, finance professionals, appraisers, brokers, and contractors require official-source or document review before any strong public claim.

## Official and Public Source Anchors

Use these as verification anchors where relevant:

- Israel Bar Association lawyer directory: https://www.israelbar.biz/hatzibor_harahv/sefer_orchey_hadin/
- Israeli government appraiser registry: https://www.gov.il/he/Departments/DynamicCollectors/search-appraisers
- Israeli government real-estate broker registry: https://www.gov.il/he/Departments/DynamicCollectors/search-real-estate-broker
- Israeli government contractor registry: https://www.gov.il/apps/moch/rasham/home
- Israeli government contractor registry dataset: https://data.gov.il/he/datasets/ministry_of_housing/pinkashakablanim

No professional page should claim legal, tax, finance, appraisal, engineering, or construction authority unless the claim is backed by the relevant source, document, or owner-approved review note.

## Public Trust Rules

1. No fake ratings.
2. No fabricated reviews.
3. No “recommended” copy unless there is a documented methodology and owner approval.
4. Paid placement must be disclosed in public language.
5. Verification and paid placement are separate. A paid profile is not automatically verified.
6. The directory does not provide legal, tax, mortgage, appraisal, or engineering advice.
7. Stale or disputed profiles are hidden or downgraded until reviewed.
8. Profile pages must show source/review date for sensitive claims.

## Anti-Cannibalization Rules

Professional pages must support money pages, not compete with them:

- City buyer pages own apartment and project demand.
- Project pages own project demand.
- Guides own informational education.
- Professional category pages own service-provider discovery.
- Professional profiles own provider/entity intent.

Examples:

- A page for “real-estate lawyer Tel Aviv” may own service intent.
- It must link to Tel Aviv buying/project pages, but it must not pretend to be the main Tel Aviv apartment page.
- A purchase-tax guide may mention tax review and link to the tax-advisor category, but it remains informational and should not become a provider directory.

## Routing

The routing matrix is defined in `professionals-routing-matrix.csv`. Key entry points:

- Project detail pages
- Unit and showroom states
- Listing detail pages
- City buying hubs
- Urban renewal guides
- Mortgage calculator
- Purchase-tax and legal guides
- English foreign-buyer pages
- Professionals hub and category pages
- Contractor/provider intake
- Admin war room

## Required Runtime Behavior

- Filter by category, city, language, transaction stage, and verification status.
- Show profile cards with clear evidence state, contact options, and disclosure.
- Provide an empty state when a category/city has no verified supply.
- Support category intake when the user needs help but no profile is approved.
- Log source surface, page family, category, city, language, profile id when present, and disclosure state.
- Keep contact details in the form or CRM system, not in analytics.

## Implementation Outputs

- `professionals-directory-product-spec.csv`
- `professionals-verification-policy.csv`
- `professionals-routing-matrix.csv`
- `professional-profile-schema.json`
- `professionals-directory-execution-packet-rtl.html`
- `professionals-directory-execution-packet-visual-qa.md`

## Not Implemented Yet

This packet does not prove:

- live WordPress directory templates
- live provider database
- verified professional records
- live lead routing
- legal or financial review approval
- public profile screenshots
- monetization packages

The next build slice should implement the private registry and one category prototype first, then capture desktop and 390px screenshots for hub, category, city-category, profile, empty state, and lead state.
