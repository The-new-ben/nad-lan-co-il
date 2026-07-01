# NadLan — Comprehensive Website Audit & Spec Report

**Date:** July 1, 2026  
**Target Domain:** `https://nad-lan.co.il/`  
**Plugin Version:** `1.69.62`  
**Visual Target Mockup:** [ashira_pr4_pr5_visual_mockup](file:///C:/Users/pro/.gemini/antigravity/brain/106dbcc6-9bca-4a6f-8ee1-166cc3ba54b5/ashira_pr4_pr5_visual_mockup_1782896433054.jpg)

---

## 1. Technical & SEO Audit (Live Findings)

### 1.1 Duplicated H1 Tags (SEO Blocker)
Our live HTML parsing of `https://nad-lan.co.il/projects/ashira-sde-dov/` revealed two `<h1>` tags on the page:
1. `<h1>נדלן חכם</h1>` (Wrapped around the site logo/link in the header)
2. `<h1>דירות למכירה באשירה שדה דב</h1>` (The project page title)

> [!WARNING]  
> **SEO Impact:** Multiple H1 tags dilute keyword relevance and confuse search crawlers regarding the primary topic of the page. The site logo should only be an `<h1>` on the front page. On all singular posts, category archives, and tools pages, it should be demoted to a `<div>`.

### 1.2 Multi-Language SEO (Hreflang Verification)
The language routing and alternates are correctly configured on the live database. Sibling links for Ashira Sde Dov are output as:
- `he` -> `https://nad-lan.co.il/projects/ashira-sde-dov/`
- `en` -> `https://nad-lan.co.il/projects/ashira-sde-dov-en/`
- `fr` -> `https://nad-lan.co.il/projects/ashira-sde-dov-fr/`
- `ru` -> `https://nad-lan.co.il/projects/ashira-sde-dov-ru/`
- `ar` -> `https://nad-lan.co.il/projects/ashira-sde-dov-ar/`
- `x-default` -> `https://nad-lan.co.il/projects/ashira-sde-dov/`

This is a premium technical SEO implementation that prevents search engine cannibalization and helps capture international buyer queries.

### 1.3 WooCommerce Cleanliness & Public Trust
- WooCommerce general stylesheet (`wc-blocks-rtl.css`) is loaded, but active cart fragments and `wc-add-to-cart` scripts have been successfully dequeued from all public pages.
- **Result:** Improves public trust, prevents commercial cart leakage on editorial pages, and increases page load speed.

---

## 2. Competitor Comparison

We compare NadLan to leading Israeli listings portals and international benchmarks:

| Feature | Yad2 (Israel) | Madlan (Israel) | Zillow / Redfin (US) | NadLan (Proposed Spec) |
| :--- | :--- | :--- | :--- | :--- |
| **Visual Aesthetics** | Poor (Cluttered banners, standard tables, aggressive ads) | Average (Map-first, clean lists, limited visual brand) | Premium (Minimalist, dark-theater media modes, clear fonts) | **Excellent (Calm cream/warm ink palette, premium typography)** |
| **Interactive Showroom** | None (Static photos and basic PDFs) | None (Map coordinates only) | Limited (Matterport tours, no structural floor-plan picker) | **Active (Interactive 3D GLB model and traced facade selectors)** |
| **AVM Valuation** | Basic price range estimates | Strong neighborhood stats & tax data | Advanced (Zestimate comps+hedonic blending) | **Active (Local comps table + FSD confidence interval)** |
| **International Funnel** | Hebrew only | Hebrew only | English only | **Multi-lingual routing (HE, EN, FR, RU, AR) with alternate sitemaps** |

---

## 3. User Journey Gaps & Recommendations

### 3.1 3D Model Interface & "Weird Spin"
- **Issue:** The standard `<model-viewer>` configuration allows infinite polar vertical orbit. When spinning the model, it flips upside down or twists unnaturally.
- **Fix:** Restrict the `camera-orbit` and polar vertical lock to horizontal (azimuth) rotation only.
```html
<model-viewer
  src="ashira.glb"
  camera-controls
  interaction-prompt="none"
  min-camera-orbit="auto 70deg auto"
  max-camera-orbit="auto 90deg auto">
</model-viewer>
```

### 3.2 Mobile Responsiveness (The Floating Action Rail)
- **Issue:** Mobile screens frequently suffer from stacked action overlays (WhatsApp CTA, Lead wizard, and Accessibility helper buttons overlapping at the bottom-left).
- **Fix:** Collapse all interactive prompts into a unified, slide-out **Floating Action Rail** anchored at the bottom-center.

### 3.3 The Buyer Journey (Try to Purchase)
- **Problem:** Real estate regulations in Israel (Electronic Signature Law 5761-2001) prevent full online property purchases. 
- **Solution:** Focus on the **Non-Binding Offer Letter (LOI)** as the high-intent conversion step. Let users build their purchase profile (rooms, price range, mortgage limit), sign an offer letter using our secure e-sign module, and route the lead instantly to the contractor dashboard.

---

## 4. Code Actions & Recommendations

### 4.1 Fix: Site Logo H1 Demotion (Theme Level)
Modify the main theme header output (typically in `header.php` or `parts/header.html`) to dynamically output `<div>` for the site title unless on the homepage:
```php
<?php if ( is_front_page() || is_home() ) : ?>
    <h1 class="site-title"><a href="<?php echo esc_url( home_url( '/' ) ); ?>">נדלן חכם</a></h1>
<?php else : ?>
    <div class="site-title"><a href="<?php echo esc_url( home_url( '/' ) ); ?>">נדלן חכם</a></div>
<?php endif; ?>
```

### 4.2 Fix: Add Style Refinements for LTR / RTL Alignments
Add explicit rules to `style.css` to handle text directions correctly on multi-language project singles:
```css
/* LTR Language System overrides (EN, FR, RU) */
html[lang="en"] .nadlan-project-article,
html[lang="fr"] .nadlan-project-article,
html[lang="ru"] .nadlan-project-article {
    direction: ltr;
    text-align: left;
}

html[lang="he"] .nadlan-project-article,
html[lang="ar"] .nadlan-project-article {
    direction: rtl;
    text-align: right;
}
```
