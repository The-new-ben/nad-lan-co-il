# Self-Registration & Payments Plan — Paid Memberships Pro + Stripe

> **Notice to all agents:** decision locked 2026-05-28 — PMPro + Stripe is the chosen stack for the professional self-registration funnel (the "people pay me, I see money flow" path). This skill is the concrete install + config plan. Owner approves cost at install time (PMPro core is free, Stripe is per-transaction).

## What we're building

A professional (broker, mortgage advisor, lawyer, appraiser, inspector, architect, etc.) lands on `/professionals/` → clicks "Join the directory" → picks a tier (Free / Pro / Premier) → enters license number + profile → Stripe Checkout → on successful payment, the system:
1. Creates a `nadlan_professional` CPT post tied to their user account.
2. Sets `tier` meta to free/pro/premier.
3. Sets `verified` meta to false initially (manual one-click verification by owner OR auto if they pass a license-number regex check).
4. Publishes their profile to the directory.
5. Emails owner: "New professional signed up — tier X, payment Y ₪".
6. Emails the professional: welcome + profile-edit link.

From then on, monthly auto-renewal via Stripe (or one-time payment, depending on tier).

**Owner sees money in Stripe dashboard. Zero ongoing involvement** (unless they want manual approval for trust).

## Stack — three plugins, all free core

1. **Paid Memberships Pro** (paidmembershipspro.com) — free core. The membership engine. Tiers, recurring, checkout flow, registration form.
2. **Paid Memberships Pro - Stripe Gateway** — bundled with PMPro core. No extra cost.
3. **(Optional) PMPro Register Helper** — free addon for extra fields (license number, specialty, cities served).

## Cost truth

- PMPro core: **free**.
- Stripe: **per-transaction** (2.9% + 1.20 ₪ on Israeli cards as of 2026). Zero monthly.
- No commitments. Cancel any time.

## Stripe keys needed

Owner creates a Stripe account at stripe.com (free, ~5 min). Two key pairs:
- **Test publishable + secret** keys (for staging).
- **Live publishable + secret** keys (when going live).

Once owner has the keys, PMPro → Settings → Payment Gateway → Stripe → paste keys → save.

## Three tiers

Per `design-monetization-surfaces.md` §F:

| Tier | Price | What they get | Card visual |
|---|---|---|---|
| **Free** | 0 ₪ | Basic profile, listing in `/professionals/`, name + city + specialty + contact form | Standard card |
| **Pro** | **99 ₪/month** | Free + multiple cities, social links, gold "pro" tag, priority in filter results | 1px gold-600 hairline frame + gold "pro" eyebrow |
| **Premier** | **299 ₪/month** | Pro + cream-100 card surface + gold inset frame on portrait + sticky top of any filter result + verified badge + 5 sponsored placements/month | Cream-100 surface + gold portrait inset + sticky top + "פרימייר" gold eyebrow |

Numbers are starting points; owner can A/B test.

## Build steps — order matters

### Step 1: Owner installs the 2 plugins (1-time, ~5 min)
1. WP Admin → Plugins → Add New → search "Paid Memberships Pro" → install + activate.
2. (Optional) Install "PMPro Register Helper" for the license-number custom field.
3. Stripe gateway is bundled — no separate install.

### Step 2: Owner enters Stripe keys (~3 min)
1. Sign up at stripe.com (free) if not already.
2. Stripe Dashboard → Developers → API keys → copy test publishable + secret.
3. WP Admin → Memberships → Payment Settings → Gateway: Stripe → paste keys.

### Step 3: Agent creates the 3 tiers via PMPro REST or wp-admin
PMPro has REST endpoints for membership level creation. Agent (Claude) can script this once the keys are in. Otherwise wp-admin → Memberships → Membership Levels → Add: Free / Pro / Premier with the prices above.

### Step 4: Agent builds the registration page
Custom page at `/become-a-professional/` with the PMPro registration block + custom fields:
- license_no (regex-validated: lawyer = `\d{5,7}`, broker = `\d{4,6}/\w` etc.)
- specialty (taxonomy `profession`)
- cities served (multi-select linked to `nadlan_city` taxonomy)
- bio (textarea, max 600 chars)
- photo (image upload, processed to 4:5)
- WhatsApp, Facebook, LinkedIn (optional URLs)

### Step 5: Agent writes the success hook
On `pmpro_after_checkout` action: create the `nadlan_professional` CPT post tied to user_id, copy fields from PMPro user meta to nadlan_professional meta (tier, license_no, etc.), publish.

This hook lives in `nadlan-config` plugin (v1.3.0 — single capability per release per plugin lessons).

### Step 6: Agent wires the directory display
Update `/professionals/` archive widget to read `nadlan_professional` CPT (already exists), tier visual differentials per `design-monetization-surfaces.md` §F.

### Step 7: Owner verifies test flow
- Owner uses Stripe test card `4242 4242 4242 4242` to register as a fake professional.
- Verify profile appears, tier correct, email arrived.
- Switch Stripe to live keys, smoke-test with own card and refund.

## Manual-approve-first vs auto-publish

**Recommendation:** manual approve the **first 30 days** for trust/legal safety (owner is a lawyer; license-number validation is the legal disclosure shield). After 30 days + 20 sign-ups, switch to auto-publish.

In code: `auto_publish` boolean flag in `nadlan-config` options. Default false. Owner flips it via wp-admin or REST when ready.

## Revenue model (back-of-envelope)

- 20 Pro × 99 = **1,980 ₪/month**
- 8 Premier × 299 = **2,392 ₪/month**
- Total recurring at 28 paid pros: **~4,400 ₪/month**, ~52,800 ₪/year (~$14k).
- Plus per-deal closing-attorney fees from leads the directory converts to the law practice (the big number).

## Open TODOs

- [ ] Owner installs PMPro + creates Stripe account + pastes keys.
- [ ] Agent creates 3 tiers (script or wp-admin).
- [ ] Agent builds `/become-a-professional/` page with the PMPro block.
- [ ] Agent ships plugin v1.3.0 with the `pmpro_after_checkout` hook + CPT mapper.
- [ ] Agent updates `/professionals/` archive with tier visual differentials.
- [ ] Owner test-flow + go-live decision.

---
_Created 2026-05-28 by Claude Code (claude-opus-4-8). Decision locked: Paid Memberships Pro + Stripe._
