# NadLan — Complete Sales Experience (surgical feature set)

> Owner directive 2026-06-27: stop refining in circles; define the *complete* product now
> so we don't discover features late. Sourced from e-commerce + real-estate leaders
> (Zillow, Compass, Homes.com, Shopify/e-commerce CRO). Each item is a small, additive,
> data-driven feature on the existing engine — not a redesign. Honest only: no fake
> scarcity, no fake social proof, no fabricated numbers.

## A. Convert the buyer (e-commerce CRO, applied to apartments)

1. **Honest scarcity badges** from real unit status: "3 דירות זמינות", "אחרונה בקומה", "אוזל".
   Drawn from `status` (available/reserved/sold) — never a fake countdown.
   (Product badges lift conversion up to ~55%; fake timers destroy trust —
   https://yithemes.com/blog/best-practices/urgency-and-scarcity-how-to-use-dynamic-badges-to-reduce-cart-abandonment-on-woocommerce/ , https://scandiweb.com/blog/scarcity-marketing-examples-tactics/)
2. **Trust signals**: "פרויקט מאומת", "אומדן לא מחייב", source + last-updated stamp on data.
   (+17% completion with trust badges; #1 abandonment cause is distrust —
   https://flaircommerce.com/guides/trust-badges/ , https://www.shopify.com/blog/trust-badges)
3. **Guest favorites + "הדירות שלי"** (no login, localStorage) + "email me this apartment".
   (Wishlist sites convert ~30% higher; guest wishlist is critical —
   https://savetowishlist.com/wishlists-increase-ecommerce-conversion-optimization/ , https://thegood.com/insights/10-ways-to-drive-more-ecommerce-wish-list-conversions/)
4. **Micro-interactions**: cinematic unit-select, "נשמר!" toast, smooth panel/transition feedback.
   (Micro-interactions build subconscious trust for high-ticket —
   https://contentsquare.com/guides/ecommerce-ux/)
5. **Low-friction lead** = the checkout: shortest possible inquiry, unit context attached,
   sticky inquire + WhatsApp. (Fundamentals over flash; minimise fields —
   https://www.digitalapplied.com/blog/ecommerce-checkout-optimization-2026-ux-guide)

## B. Real-estate decision tools (Zillow / Compass / Homes.com)

6. **Saved search + alerts**: "הודיעו לי על דירה מתאימה" and "alert on price/availability change."
   Captures a lead and powers remarketing. (Zillow instant alerts —
   https://www.zillow.com/learn/zillow-advanced-search/)
7. **Mortgage / affordability calculator** (Israel): price, equity (~25-50%), rate, term -> monthly.
   (Zillow built-in calculator + BuyAbility — https://www.zillow.com/mortgage/calculator/payment/advanced-report/)
8. **Walk / Transit / Bike score + commute time** (enter your work address -> minutes by car/transit)
   in the complete-world block. (Zillow/Redfin Walk Score under Neighborhood —
   https://www.redfin.com/how-walk-score-works)
9. **Compare** 2-3 units / projects side by side (have it; polish to a tray).
10. **Pre-launch / register-interest** mode for new projects ("בקרוב · הירשמו מראש").
    This is the new-projects + foreign-investor funnel + honest FOMO.
    (Zillow Preview pre-market listings — https://www.housingwire.com/articles/zillow-preview-public-premarketing/)
11. **3D tour / interior** path (showroom now; interior walk-through later).

## C. Foreign-investor concierge (the high-value crowd)

12. Currency display toggle, process/financing/tax guidance per language, a concierge contact path,
    hreflang-correct language pages. (Already in the engine's investor block + i18n.)

## D. Monetization / contractor FOMO (the payer)

13. **Featured / priority tier** lifts a project in gallery, map, and nearby-projects
    (seeded: `project_featured` / `project_tier`). Mirrors Zillow Showcase / StreetEasy priority
    (https://www.ylopo.com/blog/ads-on-zillow , https://www.realestatenews.com/2026/04/14/streeteasy-product-aims-to-give-agents-an-edge-in-tough-market).
14. **Contractor dashboard** to upload assets, set units/prices, mark featured, preview
    (separate WP build; never buyer-visible).
15. **Nearby-projects map** where a contractor sees the others and wants in (pay to appear / rank).

## Build order (additive slices, each screenshot-gated)
- Slice 2 (next): real Mapbox + spokes + scores/commute (items 8, 15) + map placement (13).
- Slice 4: honest scarcity + trust signals + guest favorites view + "saved!" toast (1,2,3,4).
- Slice 5: saved-search/alerts + mortgage calculator (6,7).
- Slice 6: pre-launch/register-interest mode + foreign-investor polish (10,12).
- Slice 7: contractor dashboard (14).
Each ships as its own small PR, default-safe, verified by the real-Chrome QA agent.
