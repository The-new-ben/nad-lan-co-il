# Premium Micro UI Standard

Use this skill when auditing or implementing a premium UI pass for Nadlan or another real-estate/marketplace WordPress site.

## Goal

Every visible control must feel intentional: buttons, icon buttons, chips, badges, inputs, selects, textareas, tabs, pagination, notices, tooltips, upload controls, floating CTAs, checkout actions, empty states, and sponsored placements.

## Rules

1. Start with selectors, not vibes. Find every `button`, `.btn`, `.pill`, `.badge`, `.chip`, `input`, `select`, `textarea`, `wp-element-button`, `wp-block-button__link`, `woocommerce` button, and block checkout selector.
2. Replace emoji-as-UI with real icons or generated fallback assets. Emoji may appear in body copy only when the brand intentionally wants it, never as primary catalog/profile UI.
3. Use one token system: ink, paper, muted gold, deep green, hairline borders, radius 0-8px, subtle shadows.
4. Use a button grammar: primary, premium primary, secondary, ghost/text, icon, danger, disabled, loading. Each has hover, active, focus-visible, disabled, and loading states.
5. Tap targets must be at least 44px on mobile for public conversion controls.
6. Do not let hover/focus/loading states change layout dimensions.
7. Labels are required for forms. Placeholders are hints, not labels.
8. Paid/sponsored states must be clear and premium, not coupon-like or hidden.
9. Empty states need a useful next action and a restrained visual. Never leave a blank card or default text block.
10. Verify at 390, 600, 900, and 1240px before calling the pass complete.

## Nadlan selectors to check first

- Directory/cards: `.nldir-*`, `.nldc-*`, `.nldc-sponsored-spot`
- Single profiles/listings: `.nlpf-*`, `.nlcard-*`, `.nlcp-*`
- Studio: `.nlst-*`
- WooCommerce: `.woocommerce a.button`, `.woocommerce button.button`, `.woocommerce input.button`, `.woocommerce .button.alt`, `.wc-block-components-button`, `.select2-container .select2-selection`
- Header/footer and lead capture: `.nlfab-*`, `.nlf *`, `.wp-block-button__link`, `.wp-element-button`
- Calculators/tools: `.nlc-*`, `.nlcalc-*`, `.nlhv *`, `.nlnls *`

## QA checklist

- No horizontal overflow at 390px.
- No conversion tap target below 44px.
- Keyboard focus is visible on all controls.
- Loading/disabled states are visible and stable.
- No default WordPress/Woo/browser button remains in the funnel.
- No emoji remains as primary UI in cards, filters, sponsored slots, Studio uploader, or social labels.
- Sponsored/paid/editorial states are labelled accurately.
- Fallback/generated assets are legal and labelled illustrative where needed.

