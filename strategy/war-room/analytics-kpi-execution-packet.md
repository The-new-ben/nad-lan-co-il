# Analytics And KPI Execution Packet

Date: 2026-06-23

Status: build-ready specification, not live instrumentation.

## Purpose

NadLan needs proof that the showroom, project pages, property results, professionals, tools, international investor pages, and contractor intake create business value. This packet defines the event dictionary and owner dashboard before implementation so the team does not invent numbers later.

## Core Decision

Use one controlled event dictionary. Every important action must have:

- one event name
- one trigger
- required parameters
- privacy rule
- owner KPI mapping
- debug evidence requirement

No event is trusted until it is visible in a debug tool with the expected payload.

## Sources Used

Official Google documentation used for the tracking model:

- GA4 recommended events: https://developers.google.com/analytics/devguides/collection/ga4/reference/events
- GA4 ecommerce measurement events: https://developers.google.com/analytics/devguides/collection/ga4/ecommerce
- Google Tag Manager data layer: https://developers.google.com/tag-platform/tag-manager/datalayer
- GA4 event parameters and custom dimensions: https://developers.google.com/analytics/devguides/collection/ga4/event-parameters
- GA4 DebugView: https://support.google.com/analytics/answer/7201382
- Google Consent Mode setup: https://developers.google.com/tag-platform/security/guides/consent

## Event Strategy

Use recommended events where the meaning is accurate:

- `search`
- `view_search_results`
- `view_item_list`
- `select_item`
- `view_item`
- `generate_lead`

Use custom events for NadLan-specific behavior:

- `filter_apply`
- `showroom_open`
- `unit_select`
- `view_context_open`
- `tour_open`
- `interior_request_start`
- `map_open`
- `map_poi_select`
- `professional_profile_open`
- `tool_result_generated`
- `contractor_intake_submit`
- `registry_view`
- `publish_gate_block`

The complete dictionary is in `analytics-event-dictionary.csv`.

## Required Parameters

Core parameters:

- `page_type`
- `language`
- `source_surface`
- `canonical_owner`
- `city`
- `project_id`
- `unit_id`
- `asset_status`
- `lead_type`
- `form_id`
- `tool_id`
- `professional_id`
- `intake_step`

Do not register every parameter as a report dimension. Register only the parameters that power dashboard cards and owner decisions.

## Privacy Rules

Analytics must not receive:

- names
- phone numbers
- emails
- message body
- exact private address
- raw sensitive financial values
- private notes from contractors or buyers

Use:

- internal ids
- category labels
- value bands
- price bands
- CRM record id
- lead type
- source surface

The CRM or form system stores the contact record. Analytics stores behavior context.

## Funnel Model

### Property Results

Measure:

- search
- result list view
- filter
- sort
- card open
- save
- compare
- contact click
- lead submit

Primary KPIs:

- result-to-detail rate
- detail-to-lead rate
- filter usage
- zero-result searches
- leads by city and page type

### Showroom

Measure:

- showroom entry
- unit selection
- view layer
- map or surroundings layer
- interior tour
- consultation request
- lead start
- lead submit

Primary KPIs:

- showroom entry rate
- unit interest by project
- tour usage
- lead rate after unit selection
- asset status impact

### International Buyer

Measure:

- language switch
- English route open
- guide engagement
- concierge start
- concierge submit

Primary KPIs:

- international traffic by language
- foreign-buyer lead rate
- project interest by language
- guide-to-lead bridge

### Professionals

Measure:

- professional category open
- profile open
- contact click
- inquiry submit

Primary KPIs:

- demand by professional category
- verified profile engagement
- referral lead volume
- lead quality by source

### Contractor Pipeline

Measure:

- intake start
- package interest
- asset bundle state
- intake submit
- CRM status
- proposal status
- closed revenue outside analytics

Primary KPIs:

- contractor inquiry volume
- qualified contractor leads
- proposal conversion
- won/lost status
- revenue by project package

## Owner Dashboard Cards

Build cards only when real sources exist:

1. Traffic by page group and language.
2. Leads by source surface and lead type.
3. Showroom funnel by project and asset status.
4. Property intent: search, filter, detail open, save, compare, lead.
5. International investor funnel.
6. Professional referral funnel.
7. Contractor pipeline.
8. Content governance: blocked items, stale pages, missing screenshots.
9. Revenue status: won, proposal, qualified, inquiry.
10. Data quality: missing events, broken payloads, stale sources.

Each card must show source and last updated date.

## QA Gate

Before calling analytics complete:

- event appears in debug tool
- required parameters are present
- no personal data is sent
- desktop route is tested
- mobile route is tested
- screenshot or debug capture is saved
- event is linked from evidence register
- owner dashboard uses the event correctly

## Files In This Packet

- `analytics-event-dictionary.csv`
- `analytics-kpi-execution-packet.csv`
- `analytics-kpi-execution-packet.md`
- `analytics-kpi-execution-packet-rtl.html`
- `analytics-kpi-execution-packet-preview.png`
- `analytics-kpi-execution-packet-preview-mobile.png`
- `analytics-kpi-execution-packet-visual-qa.md`
