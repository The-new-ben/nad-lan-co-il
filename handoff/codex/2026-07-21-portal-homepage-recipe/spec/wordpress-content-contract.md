# WordPress Content and Governance Contract

## Status and boundary

This is an implementation specification only. It does not change WordPress, the REST API, application passwords, users, roles, plugins, the block theme or live content. Every proposed field or workflow change requires a separate owner-approved implementation task.

## Architectural decision

WordPress remains the authoritative editorial and operational system. Public pages, cards, maps, feeds and future external consumers read the same project records. There is no detached JSON catalog, no parallel static homepage inventory and no manual duplication of language variants into featured slots.

Content portability stays with the existing `nadlan-config` plugin layer; presentation stays with the block theme, template parts and patterns.

## Existing content graph to reuse

| Entity | Existing WordPress owner | Portal role |
| --- | --- | --- |
| Project/development | `nadlan_project` | Stable development identity and project mini-site |
| Property/listing | `nadlan_property` | Individual resale/rental/property record |
| Professional | `nadlan_professional` | Verified/sponsored human service layer |
| City | `nadlan_city` | Geographic hub and facet |
| Compound | `nadlan_compound` | Multi-project district/compound hub |
| Profession | `nadlan_profession` | Professional category/facet |
| Editorial content | WordPress posts/guides | News, analysis and evergreen guidance |
| Project ownership | existing claim flow | Developer/editor relationship and update responsibility |
| Project 3D | existing `project_3d_*` meta | Optional source-aware digital-showroom capability |

## Existing project fields to preserve

The current plugin already exposes a useful baseline through REST-aware project meta:

- `developer_name`, `contractor_name`, `architect_name`;
- `address`, `city`, `neighborhood`, `gush`, `helka`;
- `project_type`, `project_status`;
- `num_units`, `num_buildings`, `num_floors`, `completion_year`;
- `price_min`, `price_max`;
- `website`, `phone`, `lat`, `lng`;
- `photos_csv`, `video_url`, `tour3d_url`;
- `source`, `source_url`, `source_id`;
- `claim_status`, `owner_user_id`, `verified_at`;
- `is_demo`, `data_quality`;
- `paid_tier` and existing placement/auction relationships;
- the full existing `project_3d_*` showroom family.

These fields should not be duplicated under new names without a migration/compatibility reason.

## Gaps that require an approved field design

The following names are proposed contract labels, not yet authorized code changes.

### Public identity and narrative

| Proposed field | Type | Public behavior |
| --- | --- | --- |
| `project_summary` | localized rich text | two-to-three-sentence decision summary |
| `project_name_en` or translation relationship | relation/string | stable HE/EN identity without homepage duplicates |
| `developer_profile_id` | post relation | link to canonical developer/professional/company entity |
| `sales_contact_id` | user/post relation | named route and languages |
| `project_reference` | string | developer/internal project identifier when publishable |

### Commercial and lifecycle state

| Proposed field | Type | Public behavior |
| --- | --- | --- |
| `price_display_policy` | enum | exact/range/estimate/request-current-price/hidden |
| `price_currency` | enum | source currency; display conversion is separate |
| `price_verified_at` | datetime | freshness of commercial wording |
| `availability_policy` | enum | live units/plan types/on-request/not public |
| `availability_verified_at` | datetime | freshness of unit state |
| `handover_date` / `handover_text` | date + localized text | structured date plus approved wording |
| `construction_stage` | enum | planning/pre-sale/marketing/construction/occupied/completed |
| `stage_verified_at` | datetime | source date for lifecycle claim |
| `payment_plan_summary` | localized text | shown only when approved/current |
| `payment_plan_verified_at` | datetime | expiry behavior for volatile terms |

### Comparable unit/product data

| Proposed field | Type | Public behavior |
| --- | --- | --- |
| `room_count_min/max` | decimal | project card range |
| `size_sqm_min/max` | decimal | project card/detail range |
| `unit_type_records` | child entity or validated JSON | plan types without implying live units |
| `unit_inventory_records` | child entity or validated JSON | exact units, status and selected-unit inquiry |
| `unit_data_source` | source relation | source/provenance for unit matrix |
| `unit_data_verified_at` | datetime | controls availability badge and stale behavior |

Before implementation, choose whether unit data remains validated project meta JSON, becomes a dedicated child CPT, or uses a hybrid. The choice should be based on expected unit volume, revision needs, query/filter requirements and developer editing UX—not convenience in a mockup.

### Facilities and context

| Proposed field | Type | Public behavior |
| --- | --- | --- |
| `project_amenity` | controlled taxonomy or term relation | canonical amenity/facility system |
| `amenity_evidence` | relation/structured meta | source, approval and planned/delivered state |
| `project_poi` | structured relation | schools, health, shopping, recreation, transport |
| `specification_document_ids` | attachment relations | approved/versioned specification documents |

### Freshness, source and review

| Proposed field | Type | Public behavior |
| --- | --- | --- |
| `source_type` | enum | developer/official registry/public source/editorial/owner |
| `verified_by_user_id` | user relation | internal accountability; public name optional |
| `next_review_at` | datetime | scheduled re-verification |
| `verification_status` | enum | unchecked/in-review/verified/conflict/stale |
| `verification_note` | private text | source conflicts and editorial resolution |
| `public_source_note` | localized text | concise buyer-facing provenance/caveat |
| `content_completeness` | computed object | quality gates, never edited as a marketing number |

## Media model

### Decision

Long term, project galleries should be WordPress attachment relationships, not an opaque comma-separated URL list. `photos_csv` can remain a migration bridge but should not be the final rights/provenance system.

### Attachment-level contract

Every publishable attachment needs:

- attachment ID and file variants;
- project relationship;
- media category: exterior, context, interior, amenity, plan, map, video poster, 3D poster, document;
- source and source URL/reference;
- rights holder and permission basis;
- approval status and approving owner;
- permission/expiry date when applicable;
- photo/rendering/illustration/model/generated state;
- visible caption and localized alt text;
- language and market scope;
- version/upload date;
- crop/focal point;
- public/private flag.

An asset can be technically uploaded but ineligible for public use. Public queries return only approved, unexpired media.

## Translation model

- Hebrew is the initial canonical editorial record; English is a linked equivalent, not a suffix accidentally treated as another project.
- Project, developer, media and unit identifiers remain stable across languages.
- Localized fields include title/summary/captions/alt/facility labels/process content.
- Numeric/source/status fields are shared or synchronized, not manually retyped per language.
- Currency and unit controls are display preferences; the source value/unit remains recorded.
- Language switchers preserve the equivalent entity and selected unit/plan where safe.
- A project cannot receive `foreign-buyer ready` until the English record passes its own content and contact gate.

## Homepage ownership

The July 2 CMS/reorderable-band architecture remains the correct direction:

- zone order/visibility controlled by an approved WordPress setting or editor-owned composition;
- content rails populated by quality-gated queries and editorial selections;
- menus and footer managed as WordPress navigation;
- reusable visual sections implemented as block patterns/template parts where appropriate;
- no statistics or project arrays hardcoded into templates;
- a band collapses when its query has insufficient eligible records.

The implementation mechanism—existing `home-v2` extension, block template composition or a carefully split hybrid—must be chosen only after owner approval and code review.

## Editorial workflow

```text
Draft / imported
→ ownership/source identified
→ required facts completed
→ media rights reviewed
→ commercial facts verified
→ HE editorial review
→ EN review (if claimed)
→ contact route tested
→ approved for public state
→ published
→ scheduled re-verification
→ verified again / degraded / unpublished
```

### Roles and responsibilities

| Role | Responsibility | Must not do |
| --- | --- | --- |
| Developer contributor | claim and propose facts/media | self-award verification or publish unreviewed claims |
| NadLan editor | normalize copy, taxonomy and relationships | invent commercial facts |
| Media/rights reviewer | approve source, permission and visible state | treat upload as permission |
| Verification reviewer | confirm sources/dates and conflicts | sell verification |
| Translation reviewer | approve language parity and legal/commercial nuance | machine-publish high-stakes copy without review |
| Site owner/admin | approve policy, exceptions and publication | expose credentials or bypass audit trail casually |

Capabilities should express these boundaries. A REST write must pass the same capability and validation rules as a wp-admin edit.

## Proposed freshness policy

Owner approval is required for the exact intervals. A safe starting policy is:

| Data family | Recheck target | Stale behavior |
| --- | --- | --- |
| Unit availability, price, payment plan | 7 days | remove exact value/status badge; switch to confirmation wording |
| Construction stage and handover | 30 days | mark check overdue; suppress prominent state if unresolved |
| Contact route | 30 days + automated health test | remove lead-ready state if test fails |
| Gallery/plan rights | on change and before expiry | remove expired asset immediately |
| Project/team/facilities | 90 days | remove verified badge after grace period |
| Stable identity/source | annual or conflict-triggered | open editorial conflict; unpublish only if identity cannot be trusted |
| Market/transaction data | source-specific | show explicit as-of date; never imply live |

The page may remain published with stable facts while volatile fields degrade. “Stale” does not mean silently showing the old price.

## REST API contract

### Public reads

Public project/card responses should whitelist a stable view model rather than expose every raw/private meta field:

- identity and URLs;
- approved card media variants and asset state;
- developer/location/taxonomy relations;
- price display object, not raw private negotiation data;
- comparable fact object;
- eligible badge list generated from evidence;
- public source/freshness object;
- actions/capabilities available to the viewer;
- language equivalents.

Private notes, rights documents, personal data, service credentials and internal lead routing never appear in public responses.

### Writes

- authenticated WordPress user/service identity only;
- minimum required capability per project and field family;
- nonce/cookie for browser sessions or narrowly scoped application password for approved service automation;
- no credential stored in Git, HTML previews, logs or public documentation;
- schema validation and sanitization before write;
- explicit field allowlist;
- audit identity/time/source;
- revision or durable change history for critical facts;
- media upload separated from media approval;
- rate limits and error responses that do not reveal secrets.

This research phase intentionally performs no REST write and creates/revokes no application password.

## Revisions and auditability

- Enable/confirm revision support for critical project meta selected for implementation.
- Record who changed price policy, availability, stage, handover, contact and source evidence.
- Preserve prior values and resolution notes for conflicts.
- Bulk import is idempotent through stable `source_id`; it does not overwrite a verified human edit without a conflict rule.
- Automated updates may propose a change; publication rules decide whether they can publish it.

## Quality gate computation

`content_completeness` is derived, not manually entered. Example dimensions:

- identity 15%;
- approved hero/gallery 20%;
- location/developer relationship 15%;
- lifecycle/commercial freshness 15%;
- plan/unit structure 10%;
- source/verification 15%;
- contact test 10%.

Exact weights require owner approval. Public state should rely on hard required fields as well as the score; a high score cannot compensate for missing media rights or broken contact.

## Existing endpoint alignment

The design can reuse existing `/projects`, `/map`, `/near`, `/suggest`, `/compare`, `/favorite`, `/saved-search`, `/lead`, `/concierge`, Studio and project-showroom surfaces. Before implementation:

1. document their current schemas and permission callbacks;
2. confirm production/plugin version alignment;
3. avoid exposing internal HTML-only responses as the long-term card contract if structured consumers need data;
4. add no endpoint solely for a static preview;
5. verify live behavior with clicks/browser navigation where hosting security blocks direct admin URLs.

## Performance/data-delivery rules

- Server-render the first useful homepage/project content.
- Cache public read models and invalidate on relevant publish/verification changes.
- Return responsive media URLs and dimensions.
- Do not serialize heavy unit/3D/environment payloads into every card or homepage request.
- Load map, full gallery, video and 3D only after user intent or below the fold.
- Preserve source `modified`/verification dates separately; content-edit time is not the same as data freshness.

## Implementation acceptance

- One canonical project record powers card, catalog, map, homepage, detail and language equivalents.
- Demo records cannot enter public/featured queries.
- No public badge can be produced by decorative free text.
- Media permission and illustrative state travel with the asset.
- Stale volatile fields automatically degrade or enter review.
- Sponsored and verified states remain independent.
- HE/EN parity can be audited.
- Writes are capability-scoped and auditable.
- No secret or application password is committed.
- Owner explicitly approves code work before any of the above is implemented.
