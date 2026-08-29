# Conditional structured data, measurement and privacy

## Structured-data policy

Structured data mirrors visible, current page content. It never repairs missing content, promotes a developer claim to a guarantee or exposes inventory hidden from users. Google’s guidelines require structured data to be representative, current and non-misleading: [Google structured data guidelines](https://developers.google.com/search/docs/appearance/structured-data/sd-policies).

Schema.org includes `ApartmentComplex`, `FloorPlan` and `RealEstateListing`, but that does not mean Google promises a real-estate rich result. Use these types for machine understanding and validate both syntax and visible equivalence.

## Base graph allowed before inventory

The base graph may contain:

- `WebPage` for the localized editorial page.
- `ApartmentComplex` as the subject, with address, name and description only when green.
- `Organization` for nad-lan.co.il as publisher.
- `Organization` for EcoCity as the project entity described by the page, without implying that nad-lan is EcoCity or its authorized agent.
- `BreadcrumbList` matching visible breadcrumbs.
- `FAQPage` only when the exact questions and answers are visible on the page. It may help semantic understanding even when no Google rich result is available.

### Base JSON-LD pattern

```json
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "WebPage",
      "@id": "{{canonical_url}}#webpage",
      "url": "{{canonical_url}}",
      "name": "{{localized_title}}",
      "description": "{{localized_meta_description}}",
      "inLanguage": "{{locale}}",
      "dateModified": "{{actual_page_modified_date}}",
      "isPartOf": {"@id": "https://nad-lan.co.il/#website"},
      "about": {"@id": "{{canonical_url}}#project"},
      "breadcrumb": {"@id": "{{canonical_url}}#breadcrumb"}
    },
    {
      "@type": "ApartmentComplex",
      "@id": "{{canonical_url}}#project",
      "name": "{{localized_project_name}}",
      "description": "{{localized_visible_summary}}",
      "address": {
        "@type": "PostalAddress",
        "streetAddress": "{{verified_street_address}}",
        "addressLocality": "Tel Aviv-Yafo",
        "addressCountry": "IL"
      },
      "tourBookingPage": "{{canonical_url}}#inquiry"
    },
    {
      "@type": "BreadcrumbList",
      "@id": "{{canonical_url}}#breadcrumb",
      "itemListElement": "{{visible_breadcrumb_items}}"
    }
  ]
}
```

All placeholders must be resolved or the property must be omitted. Never render template braces in public HTML.

## Conditional properties

| Property/type | Condition required | Otherwise |
|---|---|---|
| `geo` | Approved coordinates tied to project/building and survey source | Omit |
| `numberOfAccommodationUnits` | Approved total unit count in fact register | Omit |
| `numberOfAvailableAccommodationUnits` | Live approved feed, visible count and freshness within policy | Omit |
| `accommodationFloorPlan` / `FloorPlan` | Visible approved plan/type with stable ID and rights | Omit |
| `RealEstateListing` | The page visibly lists one or more current offers and records actual posting/update dates | Omit |
| `Offer.price` / `priceCurrency` | Exact public price from approved feed, visible on page, with availability and validity | Omit |
| `availability` | Approved, defined inventory status visible to the user | Omit |
| `image` | Licensed, crawlable, project-relevant image visible on page | Omit |
| `FAQPage` | Exact FAQ is visible and localized | Omit |
| `VideoObject` | Video is visible, licensed, crawlable and has required metadata/transcript | Omit |
| `AggregateRating` / `Review` | Genuine review system, evidence and policy approval | Never use in this pilot |

## Project-specific schema limits

### Stricker 13-Brandeis 14

- `numberOfAccommodationUnits` may be `52` only while fact `S-002` is fresh and the visible page says the same.
- Model the subject as one project entity. If the implementation creates child building entities, their relationship and addresses must come from approved data.
- Do not set a floor count, geo, offer, price or availability now.

### Bnei Dan 54-56

- Do not set `numberOfAccommodationUnits`; the total is missing.
- `numberOfFloors: 8` may be used only if the property is supported by the chosen schema type, visible on the page and fact `B-003` is refreshed. Otherwise leave the fact in visible content only.
- Do not create two buildings from the two street numbers without approved plans.
- Do not mark “unobstructed view” or a view guarantee in `amenityFeature`.

## Multilingual schema

- Each localized URL emits localized `name`, `description`, FAQ and page URL.
- Entity `@id` strategy must be consistent. Use a language-neutral project entity ID only if the architecture supports one canonical entity; otherwise keep page-scoped IDs and connect variants through page `hreflang`, not improvised `sameAs` links.
- `inLanguage` matches the page language.
- Address proper nouns may retain official spelling; readable transliteration can be visible but must not change the underlying address.
- Each locale page includes the same factual numbers. A CI number-diff must catch additions.

## Analytics event contract

No event contains name, email, phone, free-text message, exact personal address, contract documents or another direct identifier.

| Event | Trigger | Required properties | Success question |
|---|---|---|---|
| `project_view` | Meaningful page view after consent policy | `project_id`, `locale`, `page_version` | Which project/locale is seen? |
| `fact_source_open` | User opens a source or verification drawer | `project_id`, `fact_id`, `locale` | Do readers use trust evidence? |
| `building_select` | Building changes | `project_id`, `building_id`, `locale`, `input_mode` | Which building attracts interest? |
| `model_start` | Viewer loads by user intent | `project_id`, `model_version`, `device_class` | Does 3D earn use? |
| `model_interaction` | First orbit/zoom/semantic select | `project_id`, `model_version`, `interaction_type` | Is the viewer understandable? |
| `model_fallback` | WebGL/error fallback activates | `project_id`, `reason`, `device_class` | Where does 3D fail? |
| `floor_select` | Floor selected | `project_id`, `building_id`, `floor_id`, `input_mode` | Which floors are explored? |
| `unit_select` | Verified unit selected | `project_id`, `building_id`, `unit_id`, `inventory_updated_at` | Which units create intent? |
| `floor_plan_open` | Approved plan opens | `project_id`, `unit_id_or_type_id`, `asset_version` | Are plans used? |
| `view_simulation_open` | Simulation opens | `project_id`, `unit_id_or_viewpoint_id`, `model_version` | Does view exploration influence intent? |
| `poi_filter` | Location category selected | `project_id`, `category`, `locale` | Which daily-life need matters? |
| `route_open` | User opens external directions | `project_id`, `poi_id`, `mode` | Which destinations lead to action? |
| `buyer_checklist_open` | Checklist opens/downloads | `project_id`, `locale` | Are users preparing for due diligence? |
| `compare_start` | Comparison begins | `project_id`, `comparison_type` | Does choice support matter? |
| `share_project_state` | User shares project/unit state | `project_id`, `building_id`, `unit_id_or_null`, `locale` | What is shared? |
| `lead_start` | First form interaction | `project_id`, `context_type`, `locale` | How many qualified journeys start? |
| `lead_validation_error` | Client/server validation fails | `project_id`, `field_code`, `error_code`, `locale` | Which fields block users? |
| `lead_submit` | Server accepts inquiry | `project_id`, `context_type`, `destination_code`, `locale`, `marketing_consent` | How many valid inquiries are created? |
| `language_switch` | Locale changes | `project_id`, `from_locale`, `to_locale` | Which language demand exists? |

`unit_id` is allowed only as a public inventory identifier that contains no personal data. It is absent until an approved feed exists.

## Funnel definitions

### Discovery funnel

`project_view -> trust/location engagement -> model or plan engagement -> lead_start -> lead_submit`

### Unit funnel

`project_view -> building_select -> floor_select -> unit_select -> floor_plan_open/view_simulation_open -> lead_submit`

### Quality metrics

- Lead conversion rate by project and locale.
- Qualified-unit lead rate, where a verified unit was selected.
- Model-to-lead and plan-to-lead rates.
- Form completion and validation failure by field/locale.
- 3D fallback/error rate by device.
- Source-drawer usage.
- Location category usage.
- Language switch and localized lead rate.
- Stale inventory suppressions and feed age.
- Core Web Vitals by template, locale and 3D exposure.

Do not optimize toward raw time-on-page or animation use. The pilot goal is a trustworthy, qualified journey, not keeping users inside a viewer.

## Performance measurement

Green field targets, measured at the 75th percentile where field data exists:

- LCP at or below 2.5 seconds.
- INP at or below 200 milliseconds.
- CLS at or below 0.1.

These are the “good” Core Web Vitals thresholds documented by [web.dev](https://web.dev/articles/vitals). In local CI, use Lighthouse and a representative mid-tier mobile profile, but do not claim field compliance from lab results alone.

Capture:

- LCP element and whether it is licensed hero or placeholder.
- Long tasks and viewer initialization cost.
- Layout shifts from language, consent, gallery and model.
- 3D bundle size, texture bytes and time to interactive viewer.
- Form response time and error rate.

## Consent, privacy and lead routing

- The local prototype must use a sink/mock adapter. It must not send email, WhatsApp, CRM requests or WordPress writes.
- Before any real integration, name the controller/recipient, purpose, fields, processors, retention, deletion route and security owner.
- Required service/privacy acknowledgment and optional marketing consent are distinct and unselected.
- Consent text is localized and versioned; `consent_text_version` belongs in the server audit record, not in a marketing analytics payload.
- Analytics follows the site’s approved consent policy. Do not load non-essential trackers before the required consent state.
- Strip query-string contact data. Redact server logs and error traces.
- Provide a route for access, correction and deletion requests after legal review.

## Experiment rules

Allowed local experiments:

- Fact-first hero versus story-first hero, with identical claims.
- Static elevation versus click-to-load 3D as the primary exploration surface.
- “Request current information” versus “Prepare for a sales meeting,” while destination remains identical and clear.
- Short versus staged form, with the same required data and consent.

Forbidden experiments:

- Fake scarcity, countdowns or “only X left” without feed evidence.
- Hiding independent-site disclosure.
- Preselecting marketing consent.
- Showing a lower stale price to increase form starts.
- Labeling planned transport as open.
- Using different factual claims by language or traffic source.

