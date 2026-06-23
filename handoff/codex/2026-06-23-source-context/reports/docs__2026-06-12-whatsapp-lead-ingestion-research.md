# WhatsApp → Funnel Lead Ingestion — Cited Research + Ranked Plan
**Date:** 2026-06-12 · **Researcher:** Claude (deep-research agent, 14+ searches / 10+ fetches)
**Problem:** owner's personal 052-510-1555 receives leads from many sites; they get lost. Feed them into the existing funnel (lead CPT + OpenAI qualify + routing + nurture) without risking the number.

## THE headline finding — Coexistence (changes everything)
Meta launched **"Coexistence" GA on May 6, 2025**: ONE number can run the WhatsApp **Business app** AND the **Cloud API simultaneously** — messages mirror both ways ("Messaging Echoes" webhooks), and up to **6 months of chat history syncs** to the API side. This is the only Meta-sanctioned way to automate an existing personal business number.
- Eligibility: number must be on the WhatsApp **Business app** (not the green consumer app); account age + quality checks; onboarding via a Tech Provider Embedded Signup.
- Gotcha: the app must be opened at least once every ~13-14 days or the link drops.
- Israel was never on the excluded-country list; exclusions (EU/UK etc.) lifted Nov 2025.
Sources: developers.facebook.com embedded-signup onboarding-business-app-users · docs.360dialog.com coexistence · ycloud.com coexistence update · sanuker.com · chakrahq.com

## Ban-risk verdict on unofficial bridges (HARD NO on the personal number)
- **Oct 2025 mass-ban wave** hit Baileys bots that ran 3+ years clean (GitHub WhiskeySockets/Baileys #1869). whatsapp-web.js bans after as few as 10-200 messages (#3594, #3474). WAHA's own docs: "shouldn't be considered totally safe". Green API admits WhatsApp bans up to 2M accounts/month.
- None run on shared WP hosting anyway (need VPS/Docker, e.g., Hetzner CAX11 ~€4/mo).
- **Verdict: NEVER on 052-510-1555.** The number is unrecoverable collateral.

## Costs (2026, Israel)
- Cloud API **inbound + all replies within the 24h service window = FREE** (since Nov 2024 service conversations free; July 2025 per-message model charges only templates).
- Israel template rates ≈ utility ₪0.06 · marketing ₪0.13 · auth ₪0.035 per message (FullnessCRM calculator).
- Direct-with-Meta as Tech Provider = NO platform fee. Israeli BSP/SaaS wrappers charge ₪179-645/mo (Gambot, Glassix, CommBox, Funner/Fireberry) for what we already own (funnel + AI).
- Dedicated number acquisition: prepaid Israeli SIM ~₪30 one-time, or Sonetel ~$2/mo (documented WA-verification success). Data-only eSIMs can't verify.

## Zero-risk manual paths (verified mechanics)
1. **Share-to-funnel** — Android: installed PWA with `share_target` manifest appears in the system share sheet (absolute action URL required). iOS: Shortcuts accepts share-sheet text; "Get Contents of URL" does POST JSON with custom headers. Long-press message → Share → ~3 seconds, no login.
2. **Chat export backfill** — WhatsApp "Export chat" emits `_chat.txt` (`[date, time] - Sender: Message`, UTF-8, ~40k msgs) → email to a dedicated inbox → **Postie** (free WP plugin, IMAP polling) or custom cron parses → leads. Perfect for rescuing HISTORIC lost leads.
3. **Forward-to-bot-number** — forwarding hides the original sender (confirmed); the lead's phone must be in the TEXT or shared as a contact card; the OpenAI parser extracts it. Zero ban risk (normal user behavior).
4. Business-app LABELS have no API/export — dead end, confirmed.

## RANKED PLAN
1. **THIS WEEK (₪0, zero risk):** REST endpoint `/nadlan/v1/wa-lead` (secret-token header) → gpt-4o-mini parses blob (name, phone, intent, budget, source) → lead CPT → existing ack/qualify/routing/nurture fire. iPhone Shortcut + Android share-target. ~3 sec/lead.
2. **THIS WEEK:** chat-export → email → backfill parser for historic lost leads.
3. **NEXT MONTH:** dedicated Israeli number on direct Cloud API (no BSP) ← all site wa.me CTAs; webhook → funnel; AI auto-qualifies in the free service window. ≈₪0-50/mo.
4. **LATER:** Coexistence-onboard 052 itself (requires moving it to the WhatsApp Business app first if it's on the consumer app) — full automation of the personal number, Meta-sanctioned.
5. **NEVER:** Baileys/whatsapp-web.js/WAHA/Green API/Whapi on the personal number.
Total: week-1 ₪0; full architecture ₪30 one-time + <₪50/mo vs ₪179-645/mo Israeli SaaS.

## Monetization tie-in
Captured WA leads enter the existing routing engine (paid tiers route first); AI-scored 80+ = "verified hot buyer" inventory for flat-fee deal-team intros (lawyer/mortgage/inspector) — the legally-clean revenue lanes from the 2026-06-11 research.
