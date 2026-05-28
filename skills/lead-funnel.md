# Lead Funnel & Monetization Pipeline

> **Notice to all agents:** this is how nad-lan.co.il captures and converts. The owner's goal: zero-friction — people call him, advertise, and self-register/pay, with minimal manual work. This skill tracks what's built and the roadmap to full automation.

## Live now (2026-05-28)

- **Floating contact button (FAB)** site-wide (in the footer template part, `source: custom`): a gold-dot "ייעוץ ראשוני בחינם" button bottom-inline-start. Opens a **lead modal** (name/phone/email/topic/message + honeypot).
- **Public lead REST endpoint** (plugin v1.1.1): `POST /wp-json/nadlan/v1/lead` — honeypot-protected, IP rate-limited (5/10min), no WP nonce (works on cached pages). Creates a private `nadlan_lead` post + emails `admin_email`. **Requires plugin v1.1.1 active.**
- The homepage CTA band + any `onclick="window.nadlanOpenLead()"` opens the same modal.
- Existing `admin_post_nadlan_lead` handler (v1.0.3) remains for classic form posts.

## Still needed for "people register & pay themselves" (roadmap)

### WhatsApp + phone (owner input needed)
Add a WhatsApp leg + `tel:` to the FAB. **Blocked on owner providing the WhatsApp number + phone.** Once given, add a second FAB button `wa.me/<number>?text=...` and a `tel:` link.

### Self-service professional registration + payment (the big one)
Goal: a professional signs up, picks a tier (free/pro/premier per `design-monetization-surfaces.md`), pays, and appears in the directory — no owner action.
- **Recommended stack** (owner approval on cost): **Paid Memberships Pro (free core) + Stripe (pay-per-use, no monthly)** OR **WooCommerce + Stripe**. Both integrate with the `nadlan_professional` CPT.
- Flow: register → license-number field → choose tier → Stripe Checkout → on payment webhook, set `nadlan_professional.tier` + publish. 
- Owner sees money in Stripe; approves nothing manually (or one-click approve for trust).
- **Decision needed:** PMPro vs WooCommerce; whether to manual-approve first listing (recommended for trust/legal).

### Developer project advertising (highest ticket)
`nadlan_project` CPT + a "advertise your project" intake → invoice via Stripe/Green Invoice. 20-80K ₪/mo per `monetization-lawyer-angle.md`. Manual sales-assisted at first.

### Lead routing / CRM
Currently leads → `nadlan_lead` + admin email. Next: route by topic (legal→owner, mortgage→partner broker, etc.) via webhook fan-out. Add a stats endpoint (manage_options) for a dashboard.

## Funnel map (current)

```
Visitor → tool/guide/short-rent page (value) → FAB "ייעוץ" → modal → POST /nadlan/v1/lead
   → nadlan_lead (private CPT) + admin email → owner calls back → law-practice engagement
```

## Open TODOs

- [ ] Owner: provide WhatsApp number + phone → wire the WhatsApp/tel FAB legs.
- [ ] Owner: decide self-registration stack (PMPro+Stripe vs Woo+Stripe) + manual-approve-first y/n.
- [ ] Build the professional self-registration + Stripe flow.
- [ ] Lead routing by topic + a manage_options stats endpoint.
- [ ] Add the FAB lead modal to a dedicated /contact/ page too.

---
_Created 2026-05-28 by Claude Code (claude-opus-4-8)._
