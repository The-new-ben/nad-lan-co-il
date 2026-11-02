---
name: advertiser-deal
description: MANDATORY when a company or professional asks to advertise on nad-lan.co.il, or Ben says someone wants to advertise, sponsor, or "פרסום באתר", or asks for a price offer, a payment link or a sample ad for an advertiser. The whole flow Ben approved with LDD on 2.11.2026, end to end: terms (annual only), the prime spot next to the page's main tool, Claude Design, a mockup made on the real page, ONE image for WhatsApp, the ready message, a payment link through Morning or Grow, the legal and SEO-safe rules, and the build and release after payment.
---

# Advertiser deal (Ben, 2.11.2026: the LDD precedent)

**The case.** Rafi Mandelbaum, CEO of LDD (soil and groundwater remediation), saw the Sde Dov soil-contamination page and asked to work together.

**Ben's own words, which still set the rules:**
- "I want to offer him a year, I have no energy for less."
- "If you put it at the end it's worth nothing to him. It needs a prominent place where people look, for example where the map is, done smartly."
- "Small but effective, that can really bring him buyers."
- "A little English, for an international client."
- "Don't ruin the page, keep our focus."
- "No views and no reports, exposure for a year, in the prime location."
- "I want the link, I want a picture to bring him on WhatsApp."

The worked example lives in `docs/sales/ldd-2026-11/`, and in Linear HAD-662.

## 1. Terms: Ben's, not ours
- **One year only.** No monthly or trial offers.
- **The price is Ben's.**
  - LDD paid 24,000 ₪ + VAT a year, in two payments: 12,000 ₪ + VAT now by link, and 12,000 ₪ + VAT when the card is live.
  - Prices are always written "+ מע״מ".
  - If Ben has not named a price for a new advertiser, ask him one short question and give the LDD price as the reference.
- **Never promise views, reports, clicks or any traffic number.** That is Ben's rule, and the house rule too: no public traffic numbers.
- **What the advertiser buys:** a year in the prime spot of the page that drew him. It starts the day the card goes up.

## 2. The spot: where people look, never the end of the article
- **Find the page's main tool:** the map, the calculator, the price list. Attach the card to it.
- **On a phone:** between the tool and its result card. Everyone who uses the tool scrolls past it.
- **On desktop:** in the tool's column, right under it. If the layout is a grid, the result card spans both rows.
- **Keep it small,** about 165 px high. The tool stays the hero, and our own call to action (for example "בקשת פרטים על מגרש") keeps its weight.
- **The first screen** (H1, the opening paragraph, the tool) is never pushed down.

## 3. The card: Claude Design first
**Where it is designed.** The component is `SponsoredBox` in the design system artifact https://claude.ai/artifact/L9Nqz7Viv7K3MYeZrBc9s8 (v106.2 to v106.3). The README holds the benchmark against Google search ads, Google Maps promoted pins, Zillow's lender card and the IAB native rules. Update the design system before any code.

**What it carries:**
- **The advertiser's own logo,** from their site, on an ink badge.
- **A kicker:** "<Brand> · <what they solve for this page's reader>".
- **A headline tied to what the visitor is doing right now.** LDD: "חוות דעת מומחה על ממצאי מגרש 303", which updates with the plot picked on the map.
- **One English line,** for international buyers.
- **Three trust facts, only from the advertiser's own site:** years, staff, accreditations. Never invent a fact, and never repeat "the leading" claims.
- **Two actions:**
  - "לשיחה עם מומחה" (tel:), in ink, with a line-drawn phone icon (never an emoji);
  - "לאתר <Brand>", in outline.
- **A small label "שיתוף פרסומי"** on the frame. Israeli Consumer Protection Law forbids covert ads. Use the softest honest wording, never "תוכן ממומן" in big type.
- **The look:** the site's Skin A. White, ink #14212b, slate #3b4753, sea #2f6f86, Assistant and Noto Serif Hebrew. No cream, no gold, no gradients.

## 4. Google must not punish the page
1. **Every link to the advertiser** is `rel="sponsored noopener"`. That is Google's attribute for paid links: no ranking credit passes, and the page is not seen as selling links.
2. **The card is wrapped in `data-nosnippet`.** Its words never enter the page's snippet or an AI answer.
3. **No headings inside the card,** only strong and span. The page's outline is unchanged.
4. **Nothing else on the page changes:** title, meta, H1, text, FAQ and URL stay. No new page, no noindex, and never a 301.
5. **No extra JSON-LD.** The logo is hosted on our site and lazy-loaded.
6. **The negative-topics rule:** the card names only the advertiser. No developer, no project name, and no dispute or contamination-chemistry wording (for example no PFAS).

## 5. The mockup and the WhatsApp image
- **Build it on the real live page, in a local browser only.** Nothing is released.
  - The pattern is `docs/sales/ldd-2026-11/ldd-card-shot.py`.
  - Playwright with Chrome, 390x844 at 3x, a mobile user agent, he-IL.
  - Inject `ldd-card.css` plus the card HTML after the tool.
  - Hide `#nlcta` and `#nla11y` for the shot, then crop the tool and the card.
- **Deliver ONE image** for WhatsApp, for example `ldd-whatsapp.jpg`, with SendUserFile. A desktop shot is optional.
- **Quick checks are fine** in the browser pane or in Ben's Chrome (inject with JS, screenshot, reload). Never edit the live site for a mockup.

## 6. The message to the advertiser
Use `docs/sales/ldd-2026-11/REPLY-HE.md` (v3) as the template. Write it in Ben's voice: short and professional.
1. Thank him, and say you are happy to work together.
2. **The offer:** a card of <Brand> in the most prominent place on the page he read, attached to <the tool>, so the reader sees it exactly when the question comes up.
3. **What is on the card,** as a short list.
4. **Term:** a year from the day it goes up.
5. **Price:** X ₪ + מע״מ a year, in two payments: half now by the attached link, and half on the day the card goes up.
6. **Timing:** after the first payment the card goes up and he gets a link. Wording changes can be made before it goes up.
7. "מצרף תמונה של איך זה ייראה בטלפון", then sign as Ben, נדל״ן · nad-lan.co.il.

## 7. The payment link
- **Not through the site's store.**
  - The site's WooCommerce + Morning checkout fails ("גישה נדחתה, נא להתחבר מחדש", tested 26.10.2026).
  - Ben stopped sending people there on 2.11.2026.
- **A link from Morning or Grow:**
  - Morning (Green Invoice): https://app.greeninvoice.co.il
  - Grow: https://grow.website
- **Ben signs in himself** in his Chrome "gmktec" (deviceId 3faca133-7015-4514-8329-3c39506b4ecd). The agent never types passwords, codes or card details, and never accepts terms for him.
- **Once he is in,** create a payment request or link for the first payment: "מקדמה, פרסום שנתי באתר נדל"ן, <Brand>", amount + VAT. Give the link to Ben. Never send it to the client, and change no other account setting.
- **Ben sends** the image, the message and the link himself on WhatsApp.

## 8. After the first payment (only on Ben's word that it was paid)
1. **Build the card in the plugin:**
   - a small new file in `plugins/nadlan-config/inc/` with its CSS;
   - the logo copied to the plugin's assets;
   - shown only on the agreed page.
2. **Release through the chain** in `scripts/project-stage`:
   - make_deployNNN.py from the latest deployNNN.py;
   - read the lock line in `docs/coordination/claude-codex.md` and the live health https://nad-lan.co.il/wp-json/nadlan/v1/health in separate commands;
   - one runner at a time, in the background.
   - Add checks that the card is there, that the links carry `rel="sponsored`, that `data-nosnippet` is present, and that the page's H1 and title are unchanged.
3. **Verify** at 390 px and on desktop in a real browser, then send Ben the link.
4. **The second payment link** goes out on the day it is live, with the same flow as section 7.
5. **The year:** note the start date in Linear. Remind Ben one month before the year ends.

## 9. Tracking and talk
- **A Linear issue** (team Hadmaia, related to HAD-608/HAD-662), a row in the Notion database "מרכז הבקרה של הפרויקטים", and a folder `docs/sales/<brand>-<yyyy-mm>/`.
- **Talking to Ben:**
  - Ben is often on his phone. Use short, plain Hebrew and one question at a time.
  - If he asks for a separate session, it can be started only when he types in the desktop app, not over Remote Control. Say so in one line, and otherwise do it in the current session.
- **Never touch the wording** of the site's WhatsApp buttons or messages along the way (Ben's rule, 1.11.2026).
