# CRM, Lead Engine, And Monetization

Purpose: convert premium project/showroom pages into qualified business while keeping public pages clean and buyer-first.

## Business Model

| Product | Customer | Value | Revenue model |
|---|---|---|---|
| Project Premier | developer/contractor | premium project page + showroom + lead context | setup fee + monthly |
| Property Pro | agent/broker | listing exposure + rich media + lead routing | monthly/listing package |
| Professional Pro | lawyer/mortgage/appraiser | verified profile + leads | monthly |
| Legal services | buyer/seller/investor | lawyer-owned transaction support | case/consultation |
| Advertising/placement | developer/pro | visibility | sponsored, clearly labeled |

Any exact pricing is `NEEDS_VERIFICATION` unless from approved public package copy or owner approval.

## Lead Context

Every lead should carry context:

```json
{
  "source_page": "",
  "source_component": "showroom|listing|tool|article|professional",
  "project": "",
  "unit": "",
  "listing": "",
  "language": "he|en|fr|ru|ar",
  "intent": "buy|invest|legal|mortgage|developer_contact|professional_join",
  "cta": "",
  "utm": {},
  "asset_state": "official|concept|missing"
}
```

## WhatsApp Problem

The owner identified a major leak: WhatsApp conversations can bypass the funnel. Fix:

1. All WhatsApp links include encoded context in the message.
2. The same click also posts a lead event before opening WhatsApp when technically possible.
3. If event post fails, show visible failure or queue locally; do not silently drop if reliable capture is required.
4. CRM status distinguishes "WhatsApp clicked" from "form submitted" from "developer called."

## Public Copy Rules

Never show:
- lead funnel.
- CRM.
- automation.
- internal routing.
- debug.
- coming soon ecommerce text.

Public copy should say:
- "דברו עם נציג הפרויקט"
- "קבלו פרטים על הדירה"
- "בדיקת התאמה למשקיעים"
- "שיחה עם עורך דין נדלן"

## CRM Options

Short-term:
- WordPress CPT `nadlan_lead`.
- email notification.
- CSV export.
- webhook.

Mid-term:
- Make/Zapier/n8n webhook.
- WhatsApp Business API only after cost/legal decision.
- CRM destination per project/customer.

Long-term:
- dashboard for developers/professionals.
- lead quality scoring.
- unit interest analytics.
- package billing.

## Legal And Privacy

- Add consent checkbox where required.
- Privacy policy link on every form.
- Do not expose internal lead status publicly.
- If legal advice is requested, route as potential legal intake with conflict/engagement checks.
- Pricing claims and tax estimates require `LEGAL_REVIEW`.

## Acceptance Criteria

- Lead created with full source context.
- WhatsApp/call/form CTAs attach project/unit/listing context.
- Contractor can receive lead without developer editing code.
- No public leakage of internal funnel language.
- CRM failure state is visible to admin/QA, not silently hidden.
