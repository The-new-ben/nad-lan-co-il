# Lead Funnel + Autonomous Lead System — Cited Best Practices (Chunk B steering checklist)

31 sources across two streams (funnel design + autonomous-system architecture). This is the bar
Claude holds Codex's CHUNK B to — not "it works," but "it matches the proven pattern." Estimates
flagged. Honest limits stated.

## 1. Funnel stages + advancement (codify our own thresholds)
Visitor → Lead → MQL → SQL → Opportunity → Close. A raw form-fill is a LEAD, not an SQL — never
auto-promote to SQL without a human confirming budget+timeline+reachability. Real-estate close
anchors: paid online leads **0.4–1.2%**, referral/past-client **30%+** — segment KPIs by source.
(Prospeo https://prospeo.io/s/lead-conversion-rate-benchmarks ; Follow Up Boss https://www.followupboss.com/blog/real-estate-lead-conversion-rate)
→ CHUNK B: lead_status {new,contacted,won,lost} is the minimal spine; design the meta so a future
  scoring/MQL layer slots in. Status changes are human-driven + audited.

## 2. Capture optimization (the form is the top of the funnel)
**~3 fields converts highest (~25%); 4→3 fields ≈ +50% conversion.** Avoid dropdowns/textareas in
first capture. Single column, labels above fields, sticky mobile CTA near price/availability.
Progressive profiling: name/phone/intent first, enrich budget/timeline later.
(HubSpot https://blog.hubspot.com/blog/tabid/6307/bid/6746/which-types-of-form-fields-lower-landing-page-conversions.aspx ; NN/g https://www.nngroup.com/articles/web-form-design/)
→ CHUNK B: keep the capture form SHORT (don't add fields). If Codex adds qualification fields, they
  must be progressive/optional, not block the first submit.

## 3. Speed-to-lead — the highest-leverage rule
Respond within **5 minutes → 100x connect, 21x qualify** (Oldroyd/InsideSales; vendor data, flag).
**~78% buy from the first business to respond.** The instant auto-response must do THREE jobs:
(1) ACKNOWLEDGE the specific inquiry ("קיבלנו את פנייתך לגבי <address>"), (2) QUALIFY with ONE
question (timeline or budget), (3) NEXT STEP ("נציג יחזור אליך תוך X דקות" / book a slot).
(Casey Response https://caseyresponse.com/blog/lead-response-time-statistics ; Follow Up Boss Action Plans https://www.followupboss.com/features/action-plans)
→ CHUNK B GATE UPGRADE: the auto-ack must be acknowledge+qualify+next-step, NOT a generic "thanks."
  I will check the ack copy against this. A bare "תודה" FAILS the bar.

## 4. Qualification + scoring (design the seam now, build later)
BANT (budget/authority/need/timeline) for high-ticket; score on behavioral (viewings, tool use,
saves) + demographic (location, pre-approval, budget band). Route by score: hot→instant human+best
agent; warm→SLA+nurture; cold→drip only.
(6sense https://6sense.com/blog/what-is-the-bant-lead-qualification-framework/ ; Oracle https://www.oracle.com/cx/marketing/what-is-lead-scoring/)
→ CHUNK B: leave do_action('nadlan_lead_qualified',$lead,$score) seam + a lead_score meta field
  (unused this chunk) so the scoring engine lands without refactor.

## 5. Routing + SLA + escalation + fallback (don't dead-end a lead)
Round-robin (equitable) vs ownership vs first-come. **Tiered SLA timers**: hot ~15min, warm ~60min.
Staged escalation: nudge at 80% of SLA → manager at breach → auto-reassign to a FALLBACK QUEUE past
SLA. Native round-robin can't see availability — maintain an "available owners" check or hot leads
dump on absent reps.
(Salesforce Ben https://www.salesforceben.com/why-your-salesforce-lead-routing-isnt-delivering-speed-to-lead-and-how-to-fix-it/ ; Follow Up Boss https://www.followupboss.com/features/lead-routing ; HubSpot OOO limit https://knowledge.hubspot.com/workflows/assign-tickets-using-workflows)
→ CHUNK B GATE UPGRADE: routing must have a FALLBACK (unclaimed/free→admin, already in G5) AND a
  documented escalation seam (do_action('nadlan_lead_sla_breach',$lead)) + a response-time metric
  (G6). If the owner doesn't respond, the lead must not silently dead-end.

## 6. Nurture / follow-up (persistence is the money)
Leads need **5–12 touches** (≈80% of sales between touch 5 and 12); most quit after 1–2. Multi-touch
cadence: front-load days 1–3 (call+SMS+email), taper weekly→monthly; multi-channel; win-back cold
leads before archiving (real-estate timelines are long).
(SPOTIO https://spotio.com/blog/sales-follow-ups/ ; Ylopo https://www.ylopo.com/blog/real-estate-email-drip)
→ CHUNK B: out of scope to BUILD the drip, but leave the seam (do_action('nadlan_lead_ack') already
  specced) so the nurture engine (next chunk) hooks in. Don't auto-archive leads.

## 7. Autonomous-system mechanics (for Chunks B→G)
- Capture→CRM: webhook → normalize → match-or-create (DEDUPE) → enrich → THEN automate. Never
  contact a duplicate. (Follow Up Boss https://help.followupboss.com/hc/en-us/articles/360014570494-Lead-Flow-Overview ; HubSpot dedupe https://integrateiq.com/blogs/hubspot-data-deduplication-best-practices/)
- Idempotency: webhooks fire >once; Twilio ships an idempotency token but does NOT guarantee
  exactly-once — store an idempotency key, make every "send" check a first-touch flag, queue with
  bounded retries + dead-letter, audit every touch. (Twilio https://www.twilio.com/docs/usage/webhooks/webhooks-connection-overrides)
- Score-gated handoff: at threshold, STOP the drip and create a human task — never keep
  auto-nurturing a sales-ready lead. (n8n https://n8n.io/workflows/7343-automated-lead-capture-scoring-and-crm-integration-with-hubspot-clearbit-and-slack/ ; BoldTrail https://boldtrail.com/boldtrail-smart-crm/)
→ CHUNK B GATE: G3 idempotency must hold (atomic guard, ack once); audit log of every transition (G4).

## 8. Metrics the owner watches
Lead volume, **median response time (sub-5-min target)**, contact rate, qualification rate,
conversion rate, CPL per channel (RE avg ~$416–480; FB $5–25; Google ~$66), cost-per-QUALIFIED-lead.
(AmpiFire https://ampifire.com/blog/average-real-estate-cost-per-lead-prices-rates-2026-ads-vs-content/)
→ CHUNK B G6: healthcheck lead_e2e must expose leads_7d, delivered_7d, ack_rate,
  avg_response_minutes, by_status. Response time is the #1 operational metric.

## HONEST LIMITS (state these, don't hide them)
- Best-in-class AI resolution ≈ **51%** (Intercom Fin) — ~half still need a human; handoff is
  MANDATORY, not optional. (https://www.intercom.com/help/en/articles/8205718-fin-ai-agent-outcomes)
- AI hallucinates on price/terms unless RAG-grounded; negotiation/close/compliance = human gates.
- SMS/WhatsApp need consent + opt-out + (US) A2P 10DLC or carriers filter — that's WHY WhatsApp is a
  later chunk gated on the owner's account setup, not this one. (Twilio https://www.twilio.com/docs/messaging/compliance/a2p-10dlc)
- This chunk delivers the WEB/EMAIL lead journey end-to-end and working; it is NOT the full
  autonomous closed loop. That is honest scoping, sequenced — not a dodge.

## Sources (31, deduped) — see the two research streams; all URLs inline above.
