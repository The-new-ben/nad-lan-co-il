# International campaign network for developers (HAD-new, Ben 7.11.2026)

Ben's order (voice, 7.11): reverse-engineer immobilier.co.il and similar services abroad, build on nad-lan a dominant page that works like an
app: a developer picks markets, buyers and budget, pays an annual subscription before launch, and the campaign runs; leads land inside the
developer's live 3D project page. Hebrew + English. Claude Design first. Prove superiority parameter by parameter. Never hurt the site's
organic focus (Google must keep reading nad-lan as a real-estate portal). Developers pay their own ad spend. Annual subscription bundled with
the 3D. Premium pricing. Fix the payment flow for real.

## 1. What broke in payment (checked live 7.11.2026)
- Site checkout (WooCommerce 10.9.1 + "חיבור ל-WooCommerce עם morning" 2.4.3, gateways credit card / Bit / Google Pay / Apple Pay all
  enabled): test order 8806 (product 489, 3,990 ₪) reached /checkout/order-pay/ and Morning answered "גישה נדחתה, נא להתחבר מחדש".
  Same error as test orders 8431 (15.10) and 8634 (26.10). All three test orders cancelled. No real customer order exists.
- Cause: Morning rejects the store's connection key. Fix: Ben signs in at Morning, issues a new WooCommerce key, pastes it in
  WooCommerce > Settings > Payments > Morning. Agents may not type keys (house rule). After the paste: rerun
  scratchpad checkout_test.py (to be moved into tools/) and see the Morning card form load.
- Billing entity: the Morning business Ben signed into on 2.11 is "ב.ב.טראפיק", an exempt dealer (receipts only, no VAT). Annual packages
  at the planned size pass the exempt-dealer yearly ceiling fast; billing should come from a VAT-registered business. Accountant's call.
- Fallback that does not depend on the plugin: a Morning payment page per plan (the LDD path) linked from the planner, with the brief saved
  on our side first, so a broken plugin never loses an order.

## 1b. Payment status after the fix (7.11.2026, later the same day)
- FIXED: Morning's WooCommerce connection was registered to jus-tice.co.il only. A new connection for nad-lan.co.il (Ben approved
  18.88 ₪ to 30.11, then 20 ₪ + VAT a month), licence pasted by Ben, status active. Test order 8808 showed the Grow/CreditGuard card form.
- CEILING: one charge up to 20,000 ₪ reaches the card form; 25,000 / 30,000 / 36,000 ₪ answer "סכום זה אינו מורשה". Asked Morning
  support (same thread) to raise it to 150,000 ₪. Until then an annual plan is charged in parts of up to 20,000 ₪.
- Plan products (hidden, virtual): 8809 /product/nlcamp-1/ 36,000; 8810 /product/nlcamp-3/ 72,000; 8811 /product/nlcamp-flagship/
  144,000 (plans-products.json). Re-check: tools/checkout/checkout_check.py, then tools/checkout/cancel_test_order.py.

## 2. Where the page lives (no cannibalization)
| Intent | Owner page | Rule |
|---|---|---|
| פרסום פרויקט נדל"ן (we rank #3 after dara and yad2) | /advertiser-center/ | keep; fix its two H1s and its bare title (finding) |
| פרסום נדל"ן, prices | /advertise/ | keep |
| יזמים, שיווק פרויקטים | /developers/ | keep |
| buy property in Israel (foreign buyers, B2C) | /buy-property-israel-foreign-buyers/ and siblings | never targeted by the new page |
| **שיווק פרויקטים לתושבי חוץ / לקונים בחו"ל, קמפיין בינלאומי** | **NEW /international-campaigns/** (+ /en/international-campaigns/) | tokens "international" and "campaigns" own no URL (audit 7.11) |

Site identity: the page is linked from the three B2B pages and the footer only, never from the main buyer menu or article bodies. 4,658
buyer URLs vs 4 B2B pages. Yad2 ranks for "פרסום פרויקט נדלן" with a B2B page and is still the B2C leader. The SERP for the target
intent has no portal, no tool and no data page (serp-manual.md): open field.

## 3. The product (what a subscription buys)
1. The planner (mobile first, 5 steps): markets and communities, buyers, monthly ad budget, project, preview and pay.
2. The developer's project page on nad-lan in the chosen languages, with the virtual tour, map, price list, units (our existing
   project-stage pipeline). This is what immobilier does not have: their lead is name, phone, email and the listing.
3. Leads with context: language, city, source campaign, the units the buyer opened in the tour, time in the tour; delivered to the
   developer on WhatsApp and email, stored on our side.
4. Creatives: ads, cards and a short film per language (existing film pipeline).
5. Distribution: Meta (Facebook, Instagram), Google, community press and newsletters (list from the Kochav research), international
   boards (107 mapped by Codex), our own language pages.
6. Ad spend: paid by the developer straight to Meta and Google, in an ad account on the developer's name that we manage (partner access).

## 4. Honest statement: what I can and cannot run
Can, now: the page and planner; the order flow and brief capture; project pages in 5 languages with the tour; creatives; lead routing with
context; organic distribution with Ben's approval per post; a daily automatic checkout test that alerts when payment breaks.
Cannot without Ben: paste the Morning key; sign in to Facebook / Meta Business (the gmktec Chrome is signed out of Facebook, so the
"בן בטש נדל\"ן" campaign could not be read); create ad accounts, add payment methods, accept platform terms; spend any money (each launch
needs his OK); promise lead counts (never).

## 5. Pricing proposal (Ben decides)
Anchors we have: LDD sponsor card 24,000 ₪ a year; product 489 "קמפיין פרויקט" 3,990 ₪ a month; immobilier from 69 ₪ a lead.
APPROVED by Ben 7.11.2026, annual, ad spend separate: one market 36,000 ₪; three markets 72,000 ₪; flagship 144,000 ₪. Written "₪ לשנה" (VAT wording waits for the accountant).

## 6. Gaps vs immobilier to close
They publish in 7 to 8 languages (fr, en, he, ru, es, pt, it, de); we have 5 (he, en, fr, ru, ar). Spanish and Portuguese reach Latin
American communities. Proposal only.

## 7. Build order (loop)
1. Competitor matrix (agent) -> fill the proof table.
2. Planner tool `nlcamp` in NadLanInstruments (he + en), brief saved via REST, order via WooCommerce + Morning page fallback.
3. Page /international-campaigns/ he + en (url_word_audit passed), linked from the three B2B pages.
4. Lead-with-context: tour events attached to the lead form on project pages.
5. Release through the runner, press live on phone and desktop, source audit, benchmark vs immobilier.

Evidence: serp-manual.md; design canvas https://claude.ai/artifact/CCEWLTVzmsbQ3wDnekCnsF (v3: desktop page + interactive phone planner).

## 8. Page decision after Ben's 7.11 midday order ("the whole field in one page, rank first for what developers search")
- Manual SERP (kw/serp-manual-2.md): "שיווק פרויקטים" is a brand SERP of sales-marketing firms (brokers; we never present as a broker).
  The winnable developer intent is the budget question: "כמה עולה לשווק פרויקט נדל״ן" / "תקציב שיווק פרויקט נדל״ן": only agency
  guides rank, no tool, no portal, no AI answer shown. Plus the open field "שיווק פרויקטים לתושבי חוץ".
- So ONE hub page: H1 around "שיווק פרויקט נדל״ן" + the budget question; sections = the full breakdown of a project's marketing (every
  line item with sourced prices), the market and data, foreign buyers, AI-answer exposure (geo-test-2026-11-07.md), the planner, our
  proptech (3D project pages, rentals, renewal room, brokers), proof vs competitors, FAQ with schema.
- Slug: /marketing/ and /en/marketing/ ("marketing" and "budget" own no URL; "project" is owned by /global/project/..., "cost" by
  /apartment-purchase-cost-calculator/). Replaces the earlier /international-campaigns/ idea (nothing was live).
- Tools on the page: (1) the campaign planner nlcamp (built, release 1.72.599 in preparation); (2) a budget breakdown calculator
  (every line item, by project size and stage, sourced ranges); (3) an AI-citation check for a project (Google AI Mode test, dated);
  (4) the 3D visit replay (listens to nl:floor / nl:facing / nl:view outside the frozen engine; Hotjar cannot record WebGL).
- Film v2 from Ben's 1.11 video: storyboard Film.dc.html in the canvas, build in docs/sales/developer-film-v2/.
