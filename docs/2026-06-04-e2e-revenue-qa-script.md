# nad-lan.co.il — End-to-End Revenue & Site QA Script

> **Purpose.** A pass/fail script another agent (or a tester) can run top to bottom to certify the site is ready for customer acquisition. Every step has an expected outcome, a measurable check, and a screenshot to capture.
>
> **Test environment.** The live site `https://nad-lan.co.il`. Plugin v1.42.7+. Logged-in tester needs a fresh WordPress account they own. **Do NOT use the owner's admin account for the buyer path** — use a real subscriber-tier test account so payment activation can be verified end to end without admin shortcuts.
>
> **Tools needed.** Real Chrome at 1440px desktop AND 390px mobile, a test credit card from Morning / Green Invoice's sandbox if available (otherwise a low-value real card you can refund), and access to the admin Order list to verify activation.

## Pass criteria
A page **passes** when every "✅ Expected" item is true AND no item under "🛑 Hard fail if you see" is present. If any hard-fail item appears, stop, screenshot, and report — do not continue down the path.

---

## Part 1 — Public site (anonymous visitor)

For every page below: open in a fresh incognito window. Verify desktop (1440) AND mobile (390). Screenshot full-page.

### 1.1 Homepage `/`
- ✅ Hero shows a Tel Aviv coastal photo (not flat dark color, not line art)
- ✅ Counts read 942 projects / 2,702 pros / 22 terms (live from REST)
- ✅ Single H1: "נדל״ן חכם: קנייה, מכירה והשקעה..."
- ✅ 4 real project cards under "פרויקטים חדשים והתחדשות עירונית"
- ✅ Footer has 4 dark columns + accessibility link + copyright
- ✅ Floating נגישות button visible bottom-left
- 🛑 Hard fail: "מתוך המאגר", "כמו תבנית", "מתוך המערכת", "טיפוגרפיה" anywhere on page (internal language)
- 🛑 Hard fail: 2 H1s (use DevTools `$$('h1').length === 1`)
- 🛑 Hard fail: `document.documentElement.scrollWidth > clientWidth` (horizontal overflow)
- 🛑 Hard fail: any PHP error string ("Fatal error", "Warning:", "Notice:") in the body
- **Screenshot:** `01-home-desk.png`, `01-home-mob.png`

### 1.2 `/projects/` catalog
- ✅ Hero is dark teal with skyline overlay
- ✅ Grid shows 24 cards
- ✅ Every card has a real architectural image (no dark blocks, no concept-line-art)
- ✅ City rail on the right shows cities with counts
- ✅ Click any card → navigates to the project profile (`/projects/<slug>/`)
- ✅ Footer present (4 columns, dark)
- 🛑 Hard fail: more than 4 cards with no photo (lazy-load straggler OK; missing image is not)
- 🛑 Hard fail: 2 H1s
- **Screenshot:** `02-projects-desk.png`, `02-projects-mob.png`

### 1.3 `/professionals/` catalog
- ✅ Grid of pros, each card has a dark teal top region + gold SVG profession mark
- ✅ Profession filter pills at top (no raw "category-project"/"profession-developer" text — that's the OLD bug; should be SVG icons)
- ✅ "✓ מאומת" badge appears on verified pros
- 🛑 Hard fail: raw sprite-ID text in any pill or card
- **Screenshot:** `03-professionals-desk.png`, `03-professionals-mob.png`

### 1.4 Single project — Rainbow Tel Aviv `/projects/rainbow-tel-aviv/`
- ✅ Page title + premium banner
- ✅ Featured image displays the real Rainbow hero photo
- ✅ Gallery shows multiple images
- ✅ Body content uses serif H2/H3 (not default block-theme sans)
- ✅ `paid_tier=premier` badge or visual distinction
- ✅ No "Written by" / "in" theme post-meta strings
- ✅ Footer present
- 🛑 Hard fail: "Written by" or bare "in" text near the title
- 🛑 Hard fail: missing gallery (zero images)
- **Screenshot:** `04-rainbow-desk.png`, `04-rainbow-mob.png`

### 1.5 Single pro profile — pick the first one in `/professionals/`
- ✅ Premium header with city + profession + verified status
- ✅ "התקשרו" + "בקשת הצעת מחיר" CTAs work (click → either tel: or prompt + REST call returns OK)
- ✅ Footer present
- **Screenshot:** `05-pro-profile-desk.png`, `05-pro-profile-mob.png`

### 1.6 Glossary `/glossary/`
- ✅ Tile grid of terms
- ✅ Each tile is bordered card, serif title
- ✅ Click a term → loads `/glossary/<slug>/`, has H1, content, related terms block
- **Screenshot:** `06-glossary-desk.png`, `06-glossary-mob.png`

### 1.7 Article page — `/mortgage-calculator/mortgage-porting/`
- ✅ Hero image at top
- ✅ Body uses serif H2/H3, ~72ch reading width
- ✅ Tables are readable on mobile (stack to rows on 390px)
- ✅ FAQ schema present (`script[type="application/ld+json"]` containing `"@type":"FAQPage"`)
- **Screenshot:** `07-article-desk.png`, `07-article-mob.png`

---

## Part 2 — Revenue path (anonymous visitor → first-time buyer)

This is the money path. Run it in **one continuous session** so cookies/cart persist.

### 2.1 `/join-pro/` — see the packages
- ✅ 3 pricing cards visible: בסיסי / Pro / Premier
- ✅ Pro card is the dark teal "hero" with gold price + "מומלץ" badge
- ✅ Each card has a CTA button
- ✅ Prices match WP (Pro ₪349, Premier ₪749, etc.)
- 🛑 Hard fail: any Hebrew banner saying "החנות שלנו תושק בקרוב" or "דברים נפלאים מחכים באופק"
- **Screenshot:** `08-joinpro-desk.png`, `08-joinpro-mob.png`

### 2.2 Click "הצטרפו ל-Pro" (or `/?add-to-cart=476` directly)
- ✅ Lands on `/cart/` (or shows a mini-cart confirmation)
- ✅ Cart contains 1 line item: "Pro – אנשי מקצוע נדלן (חודש ראשון חינם)"
- ✅ Quantity input, subtotal, total all show ₪349 (or ₪0 if first-month coupon applied)
- ✅ "התקדמו לתשלום" (proceed-to-checkout) button visible
- 🛑 Hard fail: coming-soon page replaces the cart
- 🛑 Hard fail: error message "Cannot be purchased"
- **Screenshot:** `09-cart-with-pro-desk.png`

### 2.3 `/checkout/`
- ✅ Order summary on the right shows the Pro line item + total
- ✅ Billing fields visible (name / email / phone / Israeli address)
- ✅ Payment methods listed: Morning credit card, Bit, Google Pay, Apple Pay (at minimum credit card)
- ✅ "Place order" button present
- ✅ Terms checkbox if required by Woo settings
- ✅ **No shipping section** (products are virtual)
- 🛑 Hard fail: shipping methods/cost showing
- 🛑 Hard fail: no payment methods listed
- 🛑 Hard fail: place-order button missing or disabled
- **Screenshot:** `10-checkout-desk.png`, `10-checkout-mob.png`

### 2.4 Complete the order with a test/real credit card
- Fill realistic billing details (your test details — not a customer's)
- Select credit card
- Click "Place order"
- ✅ Redirect to Morning's payment page (separate domain) → enter card → submit
- ✅ Redirect back to `/order-received/` (thank-you page)
- ✅ Thank-you page shows: order number, total, email confirmation note, link back to advertiser center
- 🛑 Hard fail: 500 error on return
- 🛑 Hard fail: order says "failed" or "cancelled" without a clear reason
- **Screenshot:** `11-thankyou-desk.png` + the email if received

### 2.5 Order activation verification — owner side
Within 60 seconds of paying:
- ✅ `wp-admin → WooCommerce → Orders` shows the new order with status "Processing" or "Completed"
- ✅ The order's billing email matches the test buyer
- ✅ Order metadata includes `paid_order_id`, `paid_product_id=476` linked to a `card_id` if a card was selected
- ✅ The buyer's `paid_tier` meta on their card flipped from `free` to `pro` (check via REST: `GET /wp-json/wp/v2/nadlan_professional/<card_id>?_fields=meta`)
- ✅ `campaign_end` meta is set to ~30 days out (for product 476)
- 🛑 Hard fail: tier did NOT activate even though order is paid
- **Screenshot:** admin order detail + REST response JSON

### 2.6 Refund the test order (cleanup)
- `wp-admin → Orders → Refund` for the full amount
- ✅ Refund succeeds in Morning
- ✅ Daily downgrade cron returns the card to `free` tier (or fire it manually via WP-CLI `wp cron event run nadlan_ao_daily_downgrade`)

---

## Part 3 — Listing creation system (logged-in advertiser)

### 3.1 Register a new test user
- Sign up at `/my-account/` (or `wp-admin/wp-login.php?action=register`)
- Verify the welcome email arrives
- ✅ User account created with `subscriber` role
- **Screenshot:** `12-register-desk.png`

### 3.2 Open `/studio/` as the new user
- ✅ Studio picker page loads (NOT a wp-login redirect)
- ✅ Header has the navy "create new listing" panel: 3 type buttons (נכס למכירה/השכרה · פרויקט/יזם · כרטיס בעל מקצוע) + title input + "צרו פרסום ←" button
- ✅ Below the create panel: "עדיין אין לכם פרסומים" empty state with a search link
- **Screenshot:** `13-studio-empty.png`

### 3.3 Create a new listing — type=property
- Pick "נכס למכירה / השכרה"
- Type a title: "דירה לבדיקה QA — אל תפרסמו"
- Click "צרו פרסום ←"
- ✅ Brief "יוצר פרסום…" message
- ✅ Redirect to `/studio/?id=<new_id>` (the editor)
- ✅ The new listing exists with `owner_user_id` = the test user, `claim_status=verified`, `data_quality=stub`, `paid_tier=free` (verify via admin)
- 🛑 Hard fail: 403, 500, or any "שגיאה ביצירת הפרסום" message
- **Screenshot:** `14-studio-created.png`

### 3.4 Edit the listing in Studio
- Upload at least 1 image (drag-drop or click)
- Fill description, city, price, rooms (for property)
- Pin a location on the map
- Save
- ✅ Photo appears in the gallery
- ✅ All saved fields persist on page reload
- 🛑 Hard fail: upload fails or photo doesn't render
- **Screenshot:** `15-studio-edit.png`

### 3.5 View the new listing publicly
- Open `/properties/<new-slug>/` in a fresh incognito window
- ✅ Public profile loads, image visible, content visible
- ✅ HTML head contains `<meta name="robots" content="noindex,follow">` (stub guard)
- 🛑 Hard fail: index/follow on a stub listing (would invite Google spam)
- **Screenshot:** `16-listing-public.png`

### 3.6 Delete the test listing (cleanup)
- Admin → Posts → Properties → trash the test listing
- Verify it 404s publicly

---

## Part 4 — Internal / advertiser surfaces

### 4.1 `/advertiser-center/` as a non-admin user
- ✅ Shows the user's owned listings (or empty state if none)
- ✅ For each owned listing: photo count, views, inquiries, current tier
- ✅ "ערוך כרטיס" link goes to `/studio/?id=<id>`
- ✅ "שדרוג" CTAs link to `/cart/?add-to-cart=<pid>&card_id=<id>`
- **Screenshot:** `17-advertiser-center.png`

### 4.2 Login screen `/wp-login.php` (we want it branded)
- ✅ Branded with the SVG seal mark or the nad-lan wordmark (not raw WP logo)
- ✅ Background uses the brand palette
- **Screenshot:** `18-login.png`

---

## Part 5 — Accessibility, performance, SEO smoke checks

### 5.1 Accessibility widget
- On any page, click the navy נגישות button (bottom-left)
- ✅ Panel opens with 10 controls
- ✅ "ניגודיות גבוהה" actually changes contrast (black bg, yellow text)
- ✅ "הגדלת טקסט" actually enlarges
- ✅ "איפוס" restores everything
- ✅ Settings persist across page navigation
- **Screenshot:** `19-a11y-open.png`

### 5.2 SEO smoke
For homepage, /projects/, Rainbow, /join-pro/, one article:
- ✅ Exactly 1 `<title>` and 1 `<meta name="description">`
- ✅ Exactly 1 canonical, self-referencing
- ✅ Robots: `index, follow` on real pages; `noindex` on stub listings and thin city hubs
- ✅ `og:image` present
- ✅ One H1 per page

### 5.3 Mobile overflow
For every page in this script: run `document.documentElement.scrollWidth - document.documentElement.clientWidth` in DevTools at 390px viewport.
- ✅ Result must be `<= 2` (no horizontal overflow)

### 5.4 PHP errors
On every page above: open DevTools network tab.
- ✅ Status 200 (no 500s)
- ✅ Page body contains zero of: "Fatal error", "Parse error", "Warning:", "Notice:"

---

## Sign-off

Tester fills the table below. Site is **ready for customer acquisition** only when every Part 1–5 row says PASS.

| Part | Section | PASS / FAIL | Screenshot(s) | Notes |
|---|---|---|---|---|
| 1 | Homepage |  |  |  |
| 1 | /projects/ |  |  |  |
| 1 | /professionals/ |  |  |  |
| 1 | Rainbow project |  |  |  |
| 1 | Pro profile |  |  |  |
| 1 | Glossary |  |  |  |
| 1 | Article |  |  |  |
| 2 | /join-pro/ |  |  |  |
| 2 | Add-to-cart |  |  |  |
| 2 | Checkout |  |  |  |
| 2 | Place order |  |  |  |
| 2 | Order activates tier |  |  |  |
| 2 | Refund cleanup |  |  |  |
| 3 | Register user |  |  |  |
| 3 | /studio/ |  |  |  |
| 3 | Create listing |  |  |  |
| 3 | Edit listing |  |  |  |
| 3 | Listing public noindex |  |  |  |
| 4 | /advertiser-center/ |  |  |  |
| 4 | Branded login |  |  |  |
| 5 | Accessibility widget |  |  |  |
| 5 | SEO smoke |  |  |  |
| 5 | Mobile overflow |  |  |  |
| 5 | No PHP errors |  |  |  |

**Reporter:** _______
**Date:** _______
**Plugin version on healthcheck (`/wp-json/nadlan/v1/healthcheck`):** _______

---

## Appendix A — Common selector gotchas (audit notes)

Tested 2026-06-04 against live nad-lan.co.il (plugin v1.42.7+, Codex revenue layer applied):

- **Cart page** uses **WooCommerce Blocks**, not the classic shortcode. Correct selectors:
  - Line items: `.wc-block-cart-items__row` (NOT `tr.cart_item`)
  - Proceed-to-checkout: `.wc-block-cart__submit-button` (NOT `.checkout-button`)
- **Checkout page** is the classic checkout, not Blocks. Correct selectors:
  - Place-order button: `button[name="woocommerce_checkout_place_order"]` or text "בצעו הזמנה"
  - Payment method list: there's no `.wc_payment_method` — the Morning gateway renders its own div, look for elements with "מורנינג" in text
- **/join-pro/ page** is page-id-491. Pricing cards are inside a `<section id="plans">` with the markup `[card] [card] [card] [card]` (4 cards including a free property option Codex added). Buy links use the format `/cart/?add-to-cart=<pid>` (with the cart path), not the bare `?add-to-cart=<pid>` shortcut.

If a selector fails, **read the actual rendered HTML before declaring a bug** — the surface evolved with the revenue layer.

## Appendix B — One-line healthcheck

Quick smoke before running the full script:

```
curl -s -k https://nad-lan.co.il/wp-json/nadlan/v1/healthcheck | python3 -m json.tool
curl -s -k -u "$WP_USER:$WP_APP_PASSWORD" "https://nad-lan.co.il/wp-json/wc-admin/options?options=woocommerce_coming_soon"
```

Expected:
- `"version":"1.42.7"` (or newer)
- `"woocommerce_coming_soon":"no"` (NOT "yes")
