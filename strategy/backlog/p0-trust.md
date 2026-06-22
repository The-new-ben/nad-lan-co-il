# P0 Trust Cleanup

Objective: remove public trust damage before building more product.

## Why This Is P0

A buyer, investor, or contractor will not trust a premium real-estate site if public pages show WooCommerce cart chrome, debug text, placeholders, code leakage, or unfinished sitemap patterns.

## Tasks

1. Confirm non-commerce public pages do not show Woo/cart/checkout/notification blocks.
2. Confirm `/join-pro/` has no internal ecommerce or "coming soon" copy.
3. Confirm `/sitemap/` has no placeholders such as `...`, empty dates, or fake structure.
4. Confirm project pages do not show "More posts" or duplicate H1s.
5. Confirm article headings align above paragraphs at mobile/tablet/desktop.
6. Confirm floating action buttons are one clean rail, not stacked buttons.

## Acceptance

- Screenshots at 1440, 768, 390 for homepage, Join Pro, Sitemap, Professionals, Rainbow, Dimri.
- Text grep for forbidden words returns no public hits or documented false positives.
- No horizontal overflow.
- One H1 per page.
- Public pages have no internal operational language.

## Do Not Do

- Do not hide serious content problems with CSS only.
- Do not call it fixed before live screenshots.
- Do not mix trust cleanup with showroom feature work in the same PR.
