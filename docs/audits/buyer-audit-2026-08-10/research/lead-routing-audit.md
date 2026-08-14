# Lead capture, ownership and response audit

**Status:** source-observed and live-configuration-observed; no lead was submitted.

## Executive finding

The selected-floor contact surface can create a lead, but neither ToHa2 nor THE PARK has an accountable project owner configured in the platform. Both project cards are `unclaimed`, have no owner user, no verified commercial route, and no meaningful source/data-quality metadata. Under the current routing rules, the likely delivery path is the site administrator fallback—not the landlord, developer, broker or a named NadLan commercial desk.

The UI then hides that routing result behind a generic success message. A foreign company cannot know who received the request, what reference number to quote, or when to expect an answer.

## Current path

```text
Selected floor contact dialog
        |
        v
POST /wp-json/nadlan/v1/lead
        |
        +-- validate name + phone/email + consent
        +-- rate limit by IP
        +-- persist project/floor/unit context
        +-- optional E2E lead capture/routing
        |
        +-- owner delivery only when owner exists AND tier is pro/premier
        |
        `-- otherwise fallback_admin
```

### Positive controls found

- At least one contact method is required by the endpoint.
- The v2 route requires consent.
- The endpoint rate-limits repeated requests.
- Project, unit, floor, area, direction, status and consent context are present in the current allowlist and persistence path.
- The routing email body can include selected-floor context.

### Commercial blockers

| Gap | Buyer/business impact | Required change |
|---|---|---|
| Project route depends on claim/paid tier | A genuine commercial enquiry can fall to a generic administrator even when a landlord/broker contact exists outside the claim system. | Add an explicit, verified `commercial_lead_route` per project, independent of advertising tier. |
| No owner on either audited project | No accountable recipient or operational SLA. | Configure a NadLan commercial desk as the safe default; optionally add verified landlord/broker delivery after agreement. |
| Generic success only | Buyer cannot prove receipt or follow up. | Return and show an opaque case ID, recipient category and response target. |
| Apartment-centric form | Missing company, role, headcount, move date, area, budget, fit-out and infrastructure needs. | Use a bounded five-step commercial brief and preserve the immutable project/building/tower/floor/suite and question context automatically. |
| Three enquiry surfaces coexist | Sticky form, selected-unit contact and scheduler have different fields and promises. | Route all commercial enquiries through one service contract and one case record. |
| No question-level workflow | “Please send power schedule” disappears inside free text. | Store normalized `question_ids[]`, `document_ids[]`, status and response attachment links. |
| No observable SLA/escalation | Leads can age silently. | Track assigned, acknowledged, answered and closed timestamps; escalate before SLA breach. |
| No delivery acceptance test | Source correctness does not prove mailbox/CRM receipt. | Use a non-production test route and seeded test project for end-to-end acceptance before release. |

## Proposed commercial enquiry contract

### Project routing record

```json
{
  "project_id": 6213,
  "route_type": "nadlan_commercial_desk",
  "recipient_category": "NadLan commercial leasing desk",
  "primary_queue": "commercial-tel-aviv",
  "fallback_queue": "commercial-general",
  "ack_sla_minutes": 15,
  "human_response_sla_business_hours": 4,
  "owner_verified_at": "2026-08-10T00:00:00+03:00",
  "owner_verified_by": "admin-user-id",
  "active": true
}
```

The public client must never receive an email address, internal user ID or queue credential. It receives only `case_id`, `recipient_label`, `acknowledged_at` and `response_target`.

### Buyer brief

```json
{
  "project_id": 6213,
  "project_contract_id": "the-park-bnei-brak",
  "asset_type": "commercial_office",
  "asset": {
    "building_id": "building-main",
    "tower_id": "tower-a",
    "floor_id": "floor-20",
    "suite_id": null
  },
  "company": {
    "name": "Example US Startup",
    "website": "https://example.com",
    "contact_name": "Jane Buyer",
    "role": "COO",
    "email": "jane@example.com",
    "phone_e164": "+12125550123"
  },
  "requirement": {
    "headcount_now": 180,
    "headcount_36m": 300,
    "target_move_date": "2027-03-01",
    "rentable_sqm_min": 2200,
    "rentable_sqm_max": 3200,
    "budget_currency": "ILS",
    "budget_basis": "monthly_all_in",
    "special_uses": ["secure_lab", "24x7_noc", "catering"]
  },
  "question_ids": [
    "availability.live_schedule",
    "area.certified_measurement",
    "mep.power_capacity",
    "telecom.carrier_list",
    "commercial.full_cost_schedule"
  ],
  "document_ids": [
    "floor_pack.current",
    "mep.landlord_schedule",
    "commercial.heads_of_terms_template"
  ],
  "consent": true,
  "locale": "en-US",
  "source_surface": "selected_floor"
}
```

## Required buyer experience

1. The buyer taps **Ask about this floor** or any missing fact’s **Request this item**.
2. The selected project, floor, open questions and required documents are already in the brief.
3. Five bounded steps separate questions, requested documents, contact details, office requirements and consent. On very short screens every step fits without an internal scroller, and Back preserves the exact selected-asset tuple and answers.
4. Submission returns: “Request NL-COM-8F4K2 received by the NadLan commercial desk. Human response target: within 4 business hours.”
5. A confirmation email contains the same case ID and a secure response/status link.
6. The assigned desk sees data freshness and missing-document tasks, not only a free-text message.
7. If no human acknowledges within 15 minutes during working hours, the case escalates.

## Ownership model

| Role | Accountable for |
|---|---|
| Project data steward | Source documents, field freshness, contradictions and expiry. |
| NadLan commercial desk | Buyer acknowledgement, qualification, follow-up and RFP coordination. |
| Verified landlord/broker contact | Authoritative availability, commercial terms and data-room delivery. |
| Product operations | Route health, SLA alerts, consent retention and bounce/failure handling. |
| Engineering | Idempotency, spam protection, privacy, structured context and observability. |

## Operational dashboard KPIs

- enquiry acceptance rate and validation failures;
- percent with an accountable route;
- acknowledgement time p50/p95;
- human response time p50/p95;
- unanswered question count by project and category;
- document request fulfilment rate;
- lead-to-tour, tour-to-proposal and proposal-to-lease conversion;
- duplicate enquiry rate;
- route failure/bounce rate;
- consent evidence completeness;
- floor-data freshness at enquiry time.

## Acceptance tests

1. Seed a non-public test project with a test commercial route.
2. Submit from every locale and viewport using test recipients only.
3. Verify one and only one case is created; double click/retry remains idempotent.
4. Verify selected project/floor/suite, question IDs, documents and consent are preserved.
5. Verify buyer sees a case ID and response target.
6. Verify the test inbox/CRM receives the same context and no PII is logged to analytics.
7. Remove the primary route and prove fallback plus alerting.
8. Simulate a bounce and prove escalation.
9. Verify deletion/export/retention controls for the buyer’s data.
10. Confirm no real contact or production CRM is involved in pre-release QA.
