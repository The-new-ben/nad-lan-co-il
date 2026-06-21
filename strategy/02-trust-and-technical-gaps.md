# Trust And Technical Gaps

P0 rule:
Public trust comes before growth, SEO scale, homepage redesign, and Dimri showroom expansion.

Immediate live gap:
- PR #212 is in `origin/main`, but live probes still show public WooCommerce asset handles.
- Required unblock: UPress theme Git pull and cache clear.

Acceptance criteria:
- No WooCommerce mini-cart/cart/checkout/notification surfaces on non-commerce public pages.
- Commerce pages remain functional: cart, checkout, account, shop, product, product taxonomies, and add-to-cart flows.
- No `@wordpress/interactivity` console error on public non-commerce pages.
- No horizontal overflow at 1440, 768, and 390.
- One visible H1 on target pages.
- No `More posts`, `Leave a reply`, English template residue, or placeholder sitemap text.

Target pages:
- `/`
- `/join-pro/`
- `/sitemap/`
- `/professionals/`
- `/projects/dimri-yama-sde-dov/`

Do not solve with:
- CSS hiding of broken commerce UI.
- Z-index stacking over broken components.
- Extra docs/scripts while deployment is the blocker.

QA proof:
- Run `scripts/qa-stage1-public-trust.mjs --phase final --out docs/qa/screenshots/stage1-public-trust-final` only after UPress deploy/cache clear.

