# Revenue + Autonomous Architecture (cited) — the platform, not a point solution

**Purpose:** the owner's directive — "money, money, money, don't narrow us" and "a full autonomous
system that handles WhatsApp, gives service, and builds what's needed," generalizable to ANY
WordPress business. This doc is the researched, cited architecture behind the revenue surface in
`docs/agent-comms/claude-codex-channel.md`. Every number traces to a source in the appendix. Figures
marked (est.) are practitioner consensus, not audited disclosures — flagged honestly.

This is design + sequencing. Codex keeps building the foundation gaps; modules here land as their
own gaps afterward. Cheap hooks (`nadlan_deal_closed`, `nadlan_revenue_event`) go in now.

---

## Part 1 — Full revenue surface, with what competitors actually charge

The high-value money is NOT the listing fee. It is the **transaction** (success fee + financial
attach) and **ARPA upsell**. Evidence:

| Stream | Who pays | Real benchmark (cited) | Our status |
|---|---|---|---|
| Tiered paid listings ("depth") | advertiser | Rightmove ARPA **£1,524/mo**, growth almost all ARPA not seats; REA "Buy" yield +19% on price + depth | ✅ tiers / 🟡 recurring |
| Per-listing media/prominence add-ons | advertiser | 3D tours **+50–75% views**; floor plans **+60% views / +79% saves** (Zillow); REA Premiere+ **+18% views, +20% enquiries, sells 12 days faster**, Luxe **2× Premiere+ views** | 🔭 |
| Featured/paid placement + auction | advertiser | classifieds "bump/refresh" = recurring micro-purchase | ✅ GAP1 / 🔭 auction |
| **Success/referral fee on closed deal** | pro/agent | broker referral **~25% (20–35%)**; **Zillow Flex 15–40%, ~35% typical** — "pay for closings, not leads" | 🔭 **MAJOR** |
| **Financial-services attach** (mortgage/title/insurance/warranty) | buyer/partner | highest value per transaction; Zillow Q4 mortgage rev **doubled to $41M**; realtor.com adjacencies **~20% of revenue** | 🔭 **MAJOR** |
| Pro lead-gen (pay-per-lead) | pro | Thumbtack **$35–60/lead** (range $10–200+), credit wallet, **multiple pros charged per lead**; Houzz Pro sub **$49–99/mo** + ads from **$499/mo** | 🟡 routing built / 🔭 charging |
| Platform take-rate on any commerce | seller | durable equilibrium **~10–15% of GMV**: Airbnb **~14.3%**, Booking **~14.3%**, Etsy **~11% all-in**, Amazon **8–15%/category** | 🔭 (generalization) |
| Self-serve advertising | brands | Etsy Offsite Ads **12–15% of attributed order**; Amazon ads **$17.24B/quarter** | 🔭 |
| Platform-as-SaaS (white-label) | other businesses | tiered recurring + setup **$5k–50k**; revenue-share **30–40%**; usage-based grows ~28% faster (est.) | 🔭 (replication goal) |

**Design takeaways the build must honor:**
1. Sell the LISTING as a tiered product (Standard→Feature→Premium→Elite), and pair every paid
   upgrade with a measured uplift stat in the upgrade UI — that is exactly how REA/Rightmove drive
   ARPA. (Sources: Rightmove AR, REA FY24, Zillow 3D.)
2. Treat the **transaction, not the listing, as the monetization unit** — one closed deal stacks
   success fee + mortgage + title + insurance + warranty. Build the deal module to fire all of these
   at "offer accepted / closing." (Sources: Zillow Flex, realtor.com adjacencies, NAR RESPA.)
3. Offer pros **all three** models (lead-credit wallet, subscription, success fee) and let them
   choose — different verticals prefer different ones; the credit wallet is the cash-flow engine.
   (Source: Thumbtack/Houzz/Bark.)
4. **RESPA / regulatory gate:** in the US, paying for referrals of settlement services is restricted;
   affiliated-business arrangements must be structured carefully. For Israel, different rules apply.
   The attach/referral engine MUST be jurisdiction-gated behind config — never hardcode a fee that
   could be illegal in a target market. (Source: NAR RESPA FAQ.)

---

## Part 2 — The deal/transaction module (owner's headline: "be part of the deal")

New gap `codex/gap-deal-engine` (after the foundation gaps). Design:

- **Deal object** (CPT or table): buyer, listing, assigned pro, stage (`new → engaged → offer →
  closing → closed/lost`), agreed referral %, and the stacked attach line items.
- **Trigger:** `do_action('nadlan_deal_closed', $deal)` (seam added now). On closed:
  - compute the success fee = `referral_pct × pro_commission` (default 25%, configurable per
    category/grade; Flex-style 15–40% band) and raise a **deferred WooCommerce order** to the pro.
  - fire the **attach layer**: mortgage / title / insurance / warranty partner referrals, each a
    WooCommerce line item with its own commission/affiliate rate.
  - write a `nadlan_revenue_event('success_fee'|'attach', $amount, $meta)` for the metrics dashboard.
- **Lead → deal continuity:** GAP 2 already captures and routes the lead; the deal engine advances
  that same lead through stages, so speed-to-lead (Part 4) feeds the deal directly.
- **Compliance artifact:** persist a written referral-agreement record per deal (referral fees are
  legally sensitive). Jurisdiction config decides which attach types are allowed.

This is the single highest-leverage revenue line. It does not exist yet; it is now a tracked MAJOR gap.

---

## Part 3 — Generalize to ANY WordPress commerce (replication goal)

One engine, per-vertical config — never `if (vertical==='realestate')` in core.

- **WooCommerce is the universal transaction substrate.** A "listing" is a generic **OFFER** —
  product, service, or booking — via WooCommerce **custom product types**; services/appointments map
  to the Bookings model (`create_wc_booking`, Bookings REST API). Real estate is just one offer schema.
- **Config-driven verticalization** via the WordPress Settings API: field schemas, qualification
  questions, AI prompts, fee tables, and allowed attach types all load from options, per site.
  (Source: WP plugin best practices — "make features configurable, don't hardcode.")
- **Take-rate engine** (~10–15% default) deducted at checkout via a marketplace/split-payment layer,
  configurable per category — so the same plugin monetizes a furniture store, a clinic's bookings, or
  apartments.
- **Codex action now (cheap):** keep new code business-agnostic, generic option/CPT names, vertical
  specifics behind filters. Near-zero cost; preserves replication.

---

## Part 4 — Autonomous layer (WhatsApp + speed-to-lead + safe agent)

New gaps after foundation. Researched hard constraints (22 sources) — these are non-negotiable:

**4a. WhatsApp inbound (owner's #1 problem).**
- Integration: Meta WhatsApp Business **Cloud API** (direct, no per-message markup) or Twilio (unified
  with SMS/voice, adds fees) or a BSP (360dialog). Bridge via a `register_rest_route()` webhook;
  verify the Meta `hub.challenge` on GET and `X-Hub-Signature-256` HMAC on POST; enqueue inbound to an
  async worker (Action Scheduler).
- **HARD: the 24-hour customer-service window.** Inside 24h of a user's message you may reply free-form
  at no per-message cost; outside it, every business-initiated message must use a **pre-approved
  template (HSM)** in a Meta category (Marketing/Utility/Authentication/Service). Pre-approval exists to
  police spam.
- **HARD: explicit opt-in** before any business-initiated message, or risk WABA suspension.
- **HARD: quality tiers / messaging limits** start at **250 conversations/24h**, scale to unlimited on
  good quality; a "Flagged" rating for 7 days drops a tier. → throttle template sends, prefer staying
  inside the free window.
- Inbound calls: WhatsApp Business Calling API (via Twilio Voice) or missed-call → WhatsApp callback.

**4b. Speed-to-lead — the reason this must be autonomous.**
- HBR/Lead-Response-Management study (2,241 firms, ~100k leads): responding within **5 minutes** =
  **~100× more likely to connect, ~21× more likely to qualify** vs 30 minutes. A human owner cannot
  hit a 5-minute SLA 24/7; an agent answers in seconds. Pipeline: inbound webhook → async queue →
  agent qualifies (budget/intent/timeline) → routes (book a slot / escalate / nurture) — all inside
  the free 24h window, all feeding the deal engine.

**4c. The agent that "builds what a customer asks" — honest about the risk.**
- Pattern: tool/function-calling loop (OpenAI tools; Anthropic "agents are LLMs using tools in a loop"
  — design the tools, not just the prompt).
- **The danger (do not gloss over):** an autonomous agent that ingests untrusted inbound messages AND
  holds secrets AND can act/communicate externally is in Simon Willison's **"lethal trifecta"** —
  prompt-injection can exfiltrate secrets or break the live site, and "no guardrails currently offer
  foolproof protection." An agent with plugin/file-write on production can do irreversible damage.
- **SAFE design (mandatory):**
  1. **Propose-not-apply** — the agent emits a diff/plan into a pending-changes queue; it NEVER writes
     live code or changes config directly.
  2. **Owner approval gate** — one-tap approve/reject (WhatsApp template or admin screen). "Zero-touch"
     means zero-touch for **lead handling**, NOT for code/site mutation.
  3. **Capability-scoped tool whitelist** (create draft post, draft reply, book slot) — never arbitrary
     `eval`/filesystem write. Prefer data-driven config edits over generated PHP.
  4. **Sandbox/staging** apply first; **audit log** every tool call + args + approver.
  5. **Credential isolation** — the message-ingesting agent must not hold the secrets that complete the
     trifecta.
- **Honest ceiling:** no AI agent resolves 100% — Intercom Fin case studies report **42–67% resolution**.
  A human-handoff path is mandatory, not optional.

---

## Part 5 — Multi-site SaaS replication

- **Updates:** YahnisElsts **plugin-update-checker** from your own license-gated release server (NOT a
  GitHub PAT — a PAT grants access to ALL your private repos and must never ship to client sites).
- **Isolation:** each client site holds only its own keys/config; never centralize one client's
  WhatsApp tokens or customer data where another client or a shared agent context can read them (the
  Part 4c trifecta rule, restated for productization).
- **Pricing:** tiered recurring + setup fee, optional 30–40% revenue-share for success-based clients.

---

## Part 6 — Sequencing (does not disrupt current gaps)

Foundation (Codex, in flight): GAP5 ✅ → GAP6 ✅ → GAP3 (recurring) → placement-auction →
AI-support → business-metrics → reliability → seams/hardening.

Then revenue/autonomy gaps (Claude sequences with owner):
1. **Listing tiers + media add-ons** (fastest ARPA, proven lever).
2. **Deal engine** (success fee + attach) — highest leverage.
3. **Pro lead-credit wallet** (cash-flow engine).
4. **Take-rate engine** (generalization to any commerce).
5. **WhatsApp autonomous responder** (speed-to-lead) — the owner's #1.
6. **Self-serve advertising**.
7. **Safe agentic builder** (propose-not-apply) — last, because it's the riskiest.
8. **White-label SaaS** packaging.

Owner decisions needed before building each money module: referral % default + per-jurisdiction
legality of attach/referral fees; take-rate %; pro pricing per vertical; WhatsApp provider (Meta vs
Twilio vs BSP).

---

## Sources (deduped)

**Monetization** — Zillow FY24 (https://www.onlinemarketplaces.com/articles/zillow-q4-2024-and-fy-2024-results-double-digit-revenue-growth-as-net-losses-narrow/) · Zillow 10-K (https://www.sec.gov/Archives/edgar/data/1617640/000161764025000016/z-20241231.htm) · Zillow Flex (https://theclose.com/zillow-flex/ , https://www.zillow.com/premier-agent/flex-pricing/) · Zillow 3D (https://www.zillow.com/3d-home/) · Rightmove AR (https://plc.rightmove.co.uk/content/uploads/2024/03/Rightmove-plc-Annual-Report-2023.pdf) · Rightmove ARPA (https://propertyindustryeye.com/eye-news-update-rightmove-average-revenue-per-advertiser-soars-by-11/) · REA FY24 (https://www.onlinemarketplaces.com/articles/rea-group-grows-revenue-23-in-fy24-with-domestic-and-indian-portal-businesses-growing-market-leadership/ , https://aimgroup.com/2024/08/10/rea-group-fy2024-an-exceptional-result/) · CoStar (https://www.businesswire.com/news/home/20240423523220/en/) · referral fees (https://theclose.com/real-estate-referral-fees/ , https://www.givereferrals.com/post/real-estate-referral-fees) · realtor.com adjacencies (https://www.onlinemarketplaces.com/articles/move-inc-fy-2025-steady-revenues-at-realtor-com-as-lead-volume-declines-9/) · NAR RESPA (https://www.nar.realtor/real-estate-settlement-procedures-act-respa/respa-faq) · Airbnb 8-K (https://www.sec.gov/Archives/edgar/data/0001559720/000119312524134183/d813800dex991.htm) · Booking 8-K (https://www.sec.gov/Archives/edgar/data/0001075531/000107553124000026/ex99133124.htm) · take-rate (https://www.sharetribe.com/marketplace-glossary/commission-take-rate/) · marketplace fees (https://sellercloud.com/blog/what-are-marketplace-fees-amazon-ebay-walmart-etsy/) · Thumbtack (https://help.thumbtack.com/article/pay-for-leads) · Houzz/Thumbtack pricing (https://pro.houzz.com/for-pros/compare-thumbtack-alternative) · Amazon ads (https://www.marketplacepulse.com/stats/amazon-advertising-services-sales) · Etsy ads (https://www.pixelcut.ai/learn/etsy-advertising) · white-label SaaS (https://www.getmonetizely.com/articles/white-label-pricing-models-maximizing-value-when-licensing-your-technology)

**Autonomous / WhatsApp / agent** — Twilio WhatsApp (https://www.twilio.com/docs/whatsapp/api) · Meta webhooks (https://developers.facebook.com/docs/whatsapp/cloud-api/webhooks/payload-examples) · 360dialog limits (https://docs.360dialog.com/docs/waba-management/capacity-quality-rating-and-messaging-limits) · WhatsApp Calling (https://www.twilio.com/docs/voice/whatsapp-business-calling) · OpenAI function calling (https://developers.openai.com/api/docs/guides/function-calling) · Anthropic agents (https://www.anthropic.com/engineering/building-effective-agents) · lethal trifecta (https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/) · speed-to-lead (https://brightcall.ai/blog/harvard-business-review-best-practices-for-lead-response-management , https://www.leadangel.com/blog/operations/how-speed-to-lead-helps-you-close-more-deals/) · Woo custom product types (https://developer.woocommerce.com/docs/) · Woo Bookings (https://woocommerce.com/documentation/products/extensions/woocommerce-bookings/developer-docs-bookings/) · WP best practices (https://developer.wordpress.org/plugins/plugin-basics/best-practices/) · WP Settings API (https://developer.wordpress.org/plugins/settings/settings-api/) · plugin-update-checker (https://github.com/YahnisElsts/plugin-update-checker) · Intercom Fin (https://www.intercom.com/help/en/articles/13533623-fin-ai-agent-automation-rate)

*Researched 2026-06-05 via fan-out web search + adversarial verification. Estimates flagged (est.).*
