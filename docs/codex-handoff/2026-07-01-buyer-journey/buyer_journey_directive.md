# NadLan: Comprehensive Website Review & Marketing Directive

**Date:** July 1, 2026
**Objective:** Honest, no-compromise audit and specification for `nad-lan.co.il` prior to marketing launch.
**Focus Areas:** Buyer Journey, 3D Models, SEO, Monetization, International Traffic, Mobile Responsiveness, and Code Fixes.

---

## 1. Executive Summary: The Honest Truth

NadLan has the technical foundation to disrupt the Israeli real estate market, but the current front-end execution falls short of a premium, trustworthy user journey. Right now, it looks too much like a standard WooCommerce template and less like a dedicated, high-end real estate portal. 

To compete with Yad2/Madlan locally and Zillow/Redfin internationally, we must pivot from a "generic WordPress site" to an **App-Like Portal Experience**. 

**The biggest blockers to launch are:**
1. **The 3D Model UX:** Infinite scrolling/flipping breaks the illusion of reality.
2. **Mobile Clutter:** Too many floating widgets overlap, making the site hard to navigate on phones.
3. **The Purchase Journey:** Trying to emulate an "e-commerce cart" for real estate is legally and experientially flawed. We must shift to an "Offer Letter / Lead Gen" model.
4. **SEO Cannibalization:** Structural issues (like duplicate H1s) will prevent the site from ranking for competitive terms.

---

## 2. Competitor Analysis: Israel & Abroad

| Feature | Yad2 (Israel) | Madlan (Israel) | Zillow (US / Global) | **NadLan (The Goal)** |
| :--- | :--- | :--- | :--- | :--- |
| **Aesthetics** | Cluttered, ad-heavy, outdated UI. | Clean map-first, but dry and corporate. | Minimalist, immersive media, high trust. | **Luxurious (Dark/Gold), immersive 3D, high-contrast typography.** |
| **3D / Showroom** | None (Static photos). | None. | Limited (Matterport tours only). | **Interactive GLB models + Live Unit Selection.** |
| **Buyer Journey** | Lead gen (Phone calls). | Lead gen (Forms). | Agent routing. | **Non-Binding Offer Letter (LOI) + Direct to Contractor.** |
| **International** | Hebrew only. | Hebrew only. | English only. | **Multi-lingual routing (HE, EN, FR, RU, AR) for foreign investors.** |
| **Monetization** | Pay-per-listing / Banners. | Subscription / Promoted. | Agent Subscriptions. | **Freemium + Professional PMPro Subscriptions.** |

---

## 3. The 3D Model Spec (Crucial Fix)

### The Problem: The "Weird Spin"
Currently, the `<model-viewer>` component allows the user to rotate the model infinitely on the vertical axis (polar). This causes the building to flip upside down, breaking the user's spatial awareness and feeling cheap.

### The Fix: Restrict Camera Orbit (Code Recommendation)
We must restrict the 3D model so the user can only spin it horizontally (azimuth) like walking around a building, and limit the vertical tilt.

**Code to implement in the Showroom Engine (`showroom-engine.php` or template):**
```html
<model-viewer
  src="[YOUR_GLB_URL]"
  camera-controls
  interaction-prompt="none"
  min-camera-orbit="auto 70deg auto"
  max-camera-orbit="auto 90deg auto"
  min-field-of-view="30deg"
  max-field-of-view="60deg">
</model-viewer>
```
*This locks the vertical axis between 70 and 90 degrees, preventing the model from flipping over.*

---

## 4. The Buyer Journey (Redesign)

Real estate in Israel cannot be purchased via an online shopping cart (Electronic Signature Law). The current setup risks confusing buyers.

### Step-by-Step Spec:
1. **Discovery:** User views the 3D model and selects a unit (e.g., "Apt 12, Floor 4, Sea View").
2. **The Hook (Instead of "Add to Cart"):** Replace the cart button with **"Submit Offer Letter (LOI)"** or **"Reserve Unit"**.
3. **The Form:** A sleek, multi-step form (built via code, not a clunky plugin) that asks for:
   - Full Name & ID/Passport
   - Offer Price (Optional)
   - Mortgage Pre-Approval Status (Yes/No)
   - Contact Info
4. **The Handoff:** This routes directly into the Contractor Dashboard via our backend tracking.

> [!TIP]
> **Mobile Responsiveness Fix:** On mobile, collapse all interactive prompts (WhatsApp, Lead Form, Accessibility) into a single, unified **Floating Action Rail** anchored at the bottom of the screen. Never let buttons overlap.

---

## 5. SEO & International Traffic (Code Fixes)

To attract foreign buyers (US, France, Russia), the site's technical SEO must be flawless.

### 5.1 Duplicate H1 Fix (Critical Blocker)
Currently, the site logo in the header is an `<h1>`, and the project title is also an `<h1>`. This destroys our keyword ranking capability.

**Code to modify in `functions.php` or `header.php`:**
```php
<?php if ( is_front_page() || is_home() ) : ?>
    <h1 class="site-title"><a href="<?php echo esc_url( home_url( '/' ) ); ?>">נדלן חכם</a></h1>
<?php else : ?>
    <div class="site-title"><a href="<?php echo esc_url( home_url( '/' ) ); ?>">נדלן חכם</a></div>
<?php endif; ?>
```

### 5.2 LTR/RTL CSS Alignment
When a French or English investor visits, the text must align Left-to-Right. The current CSS doesn't handle this robustly.

**Code to add to `style.css`:**
```css
html[lang="en"] body,
html[lang="fr"] body,
html[lang="ru"] body {
    direction: ltr;
    text-align: left;
}

html[lang="he"] body,
html[lang="ar"] body {
    direction: rtl;
    text-align: right;
}
```

---

## 6. Visual Design Recommendations

The design must scream "Luxury" and "Trust". 

- **Colors:** Use a strict palette. **Dark Ink** (`#0e1111`) for backgrounds, **Cream** (`#f9f6f0`) for text, and **Gold** (`#c5a059`) for primary actions.
- **Typography:** Use **Heebo** for data/numbers and **Frank Ruhl Libre** for headings. Stop using default browser fonts.
- **UI Elements:** Use glassmorphism (frosted glass effects) over the map and 3D models to make the UI feel native.

*See the attached artifacts for visual mockups of the Homepage, Split-Search, and 3D Showroom.*

---

## 7. Monetization Spec

1. **Freemium Tier:** Basic directory listing for professionals.
2. **Pro Tier (₪199/mo):** Verified badge, priority ranking in search, direct lead routing.
3. **Execution:** Use PMPro + Stripe integration. When a payment succeeds, trigger a webhook to **Morning (Green Invoice)** API to automatically generate and send the tax receipt (חשבונית מס קבלה).

---

## Action Plan

If you approve this directive, I will immediately begin executing the code changes in the repository:
1. Fix the H1 SEO bug in `functions.php`.
2. Add the RTL/LTR CSS rules.
3. Implement the `min-camera-orbit` fix for the 3D models.
4. Draft the custom LOI (Offer Letter) form code to replace the shopping cart flow.
