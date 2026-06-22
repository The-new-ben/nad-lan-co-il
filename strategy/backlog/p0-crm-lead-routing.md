# P0 CRM And Lead Routing

Objective: stop losing high-intent leads, especially WhatsApp clicks.

## Tasks

1. Inventory all CTAs: WhatsApp, call, forms, AI concierge, advisor, developer contact.
2. Standardize lead payload context.
3. Ensure project/unit/listing context travels with every CTA.
4. Add lead event before WhatsApp open where technically feasible.
5. Add admin-visible failure/queue state.
6. Define CRM/webhook destination per customer/project.
7. Produce privacy/consent language.

## Acceptance

- Clicking "contact" from selected apartment creates or queues a lead event.
- WhatsApp message includes project/unit text.
- Developer receives actionable context.
- No public "CRM/funnel/lead" words.
- Legal/privacy links appear where required.

## Risks

- WhatsApp APIs may require paid/provider setup.
- Consent/legal wording needs review.
- CRM destination may differ by customer.
