# Premium Revenue Implementation, Theme-Owned

Branch: `codex/full-premium-revenue-implementation`  
Scope: theme files, screenshots, preview, documentation. No `inc/*.php`, no plugin ZIP, no plugin version bump.

## Honest Status

This is not live yet. It is ready for review and deployment through the theme/plugin release lane.

Live today, before this branch:

- Homepage still reads like a restrained WordPress block page, not a premium real-estate product.
- `/projects/`, `/professionals/`, Rainbow, and the concept-art cards are better than before, but not enough to carry the full site.
- `/join-pro/` has package buttons, but the public payment path is blocked by WooCommerce coming-soon.
- `/my-account/` and logged-out `/advertiser-center/` still expose a generic Woo/WordPress feeling.

The money blocker is real. The live `/cart/?add-to-cart=476` response contains:

```html
<meta name='woo-coming-soon-page' content='yes'>
<div data-block-name="woocommerce/coming-soon" data-store-only="true" class="wp-block-woocommerce-coming-soon woocommerce-coming-soon-store-only">
```

So a customer cannot reliably click from pricing to cart/checkout and pay until WooCommerce store visibility is corrected or the exclusion hook is active.

## What This Branch Adds

### 1. Theme wiring

File: `functions.php`

- Enqueues `assets/css/nadlan-premium-revenue.css`.
- Enqueues `assets/js/nadlan-premium-revenue.js`.
- Adds a WooCommerce coming-soon exclusion for the revenue path:
  - `/cart/`
  - `/checkout/`
  - `/my-account/`
  - `/join-pro/`
  - `?add-to-cart=475|476|477|489|490`
- Replaces `/join-pro/` content with a premium productized pricing page.
- Adds a premium logged-out gateway for `/advertiser-center/`, `/advertiser-dashboard/`, and `/studio/`.
- Adds branded login styling so customers do not fall into a raw WordPress login screen.

The WooCommerce hook used is `woocommerce_coming_soon_exclude`, introduced in WooCommerce 9.1. WooCommerce documents that coming-soon mode is controlled from WooCommerce settings and can apply to store pages; hook references show the exclusion filter in `ComingSoonRequestHandler::should_show_coming_soon()`.

Sources:

- https://woocommerce.com/document/configuring-woocommerce-settings/coming-soon-mode/
- https://wp-kama.com/plugin/woocommerce/hook/woocommerce_coming_soon_exclude

### 2. Premium site-wide customer CSS

File: `assets/css/nadlan-premium-revenue.css`

Covers:

- Homepage hero, search, stat panel, project cards, tools, CTA band.
- Catalog/profile reinforcement selectors: `.nldir-hero`, `.nldir-pill`, `.nldc`, `.nldc-media`, `.nldc-av`, `.nldc-sponsored-spot`, `.nlpf-banner`, `.nlpf-name`.
- `/join-pro/` pricing cards and revenue flow.
- WooCommerce cart, checkout, account, buttons, fields, notices, and coming-soon fallback.
- Logged-out advertiser/studio gateway.
- Studio and advertiser-center chrome: `.nlst-*`, `.nlac-*`.
- Mobile constraints and overflow prevention.

### 3. Lightweight interaction layer

File: `assets/js/nadlan-premium-revenue.js`

- Tags money-path links with an accessible label when missing.
- Adds polished busy state to payment/save buttons.
- Adds form-ready classes for Woo and Studio fields.
- Maintains viewport height variable for mobile polish.

### 4. Preview and screenshots

Preview:

- `docs/previews/nadlan-premium-revenue-implementation.html`

Screenshots:

- `docs/qa/screenshots/premium-revenue/before-live-current.png`
- `docs/qa/screenshots/premium-revenue/before-commerce-blocker.png`
- `docs/qa/screenshots/premium-revenue/preview-1440.png`
- `docs/qa/screenshots/premium-revenue/preview-full-1440.png`
- `docs/qa/screenshots/premium-revenue/preview-mobile-500.png`

The mobile proof is captured at a real mobile breakpoint that Chrome headless records reliably. A separate Chrome DevTools measurement showed a mobile viewport with `scrollWidth` below viewport width and no overflowing offenders.

## The Five Polish Cycles In This Deliverable

| Cycle | Surface | What changed | Proof |
|---|---|---|---|
| 1 | Homepage above fold | Image-led architectural blueprint hero, premium search, stat panel, deep teal/champagne art direction | `preview-1440.png`, `preview-mobile-500.png` |
| 2 | Catalog/listing cards | No abandoned blank cards: every default card gets original architectural concept art | `preview-1440.png` |
| 3 | Pricing | `/join-pro/` becomes a product page with four clear paid packages | `preview-full-1440.png` |
| 4 | Payment/account | Woo cart/checkout/account controls get the same button, field, card, and focus grammar | `preview-full-1440.png` |
| 5 | Internal journey | Logged-out Studio/advertiser-center becomes a branded customer gateway instead of raw WP login/redirect | `preview-full-1440.png` |

## Previous Assets That Were Produced And Where They Are

These assets are not stolen or lost. They are in the repository or proof folder:

- `assets/premium/` - micro UI icons, profession marks, fallback illustrations, button reference sheet, monogram avatar.
- `assets/premium/concept/` - original SVG concept art: Tel Aviv-style skyline, blueprint texture, project concept, property concept, hero coast concept.
- `assets/premium-site/` - large visual direction images used by the theme layer.
- `docs/rainbow-media/` - Rainbow Tel Aviv generated PNGs: hero, amenities, location.
- `docs/previews/nadlan-premium-revenue-implementation.html` - the current complete visual target.
- `C:\Users\pro\Documents\websites\.codex-tmp\nadlan-proof-20260604-193816\` - older live-before and target screenshots, including the earlier Rainbow/homepage direction previews.

Why they were not fully visible on the live website:

- The concept SVGs were wired into the plugin cards by Claude, but that only improved card/profile surfaces.
- The homepage is theme/page-content owned, so plugin concept-art wiring did not automatically redesign it.
- `/my-account/`, Woo checkout, login, and logged-out internal gates are Woo/theme surfaces, not directory card surfaces.
- `/join-pro/` links were blocked by WooCommerce coming-soon, so the monetization path could not be proven live.
- This branch now targets those missing theme/Woo/customer surfaces.

## Deployment Map

1. Merge or pull this branch into the active WordPress theme repo.
2. Deploy the theme files:
   - `functions.php`
   - `assets/css/nadlan-premium-revenue.css`
   - `assets/js/nadlan-premium-revenue.js`
3. In WordPress admin, verify WooCommerce store visibility is live:
   - WooCommerce → Settings → Site visibility.
   - The code-level exclusion is a safety net, not a replacement for store visibility sanity.
4. Clear caches.
5. QA these live URLs:
   - `/`
   - `/projects/`
   - `/professionals/`
   - `/projects/rainbow-tel-aviv/`
   - `/join-pro/`
   - `/cart/?add-to-cart=476`
   - `/cart/?add-to-cart=477`
   - `/cart/?add-to-cart=489`
   - `/cart/?add-to-cart=490`
   - `/checkout/`
   - `/my-account/`
   - `/advertiser-center/`
   - `/studio/`

## Verification Run

- `git diff --check`: passed, only Windows LF-to-CRLF warning on `functions.php`.
- PHP lint: passed with `C:\Users\pro\Documents\websites\.codex-tools\php-8.3.31-nts-Win32-vs16-x64\php.exe -l functions.php`.
- Chrome screenshots: generated desktop and mobile preview proofs.
- Mobile overflow: Chrome DevTools measurement returned no overflowing offenders at the tested mobile viewport.

## Benchmarks Used For Direction

- Apple: full-bleed product imagery, minimal text, disciplined CTA hierarchy. https://www.apple.com/
- Xero: productized pricing/accounting signup path with clear trial/buy entry points. https://www.xero.com/
- Compass: premium real-estate search expectations and quiet navigation. https://www.compass.com/
- Sotheby’s International Realty: luxury restraint, dark/light contrast, editorial real-estate framing. https://www.sothebysrealty.com/
- The Modern House: editorial property presentation and calm high-end typography. https://themodernhouse.com/

## Still Not Claimed

- I did not take a real payment.
- I did not create a fake customer order.
- I did not email or acquire customers.
- I did not package or bump the plugin.
- I did not edit `plugins/nadlan-config/inc/*.php`.

Those are the next QA and sales steps after this design/revenue layer is reviewed and deployed.
