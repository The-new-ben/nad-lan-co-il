# Site-wide premium selector checklist

Date: 2026-06-04
Scope: selector-level audit and implementation map. Docs only.

## Purpose

The owner asked for every micro element to be premium site-wide. This checklist maps the specific selectors and files Claude should inspect when implementing the visual upgrade. It deliberately avoids code changes in this PR.

## Directory and project archive selectors

| Selector / element | File | Current problem | Premium requirement | QA gate |
| --- | --- | --- | --- | --- |
| `.nldir-hero` | `plugins/nadlan-config/inc/directory-assets.php` | Cyber-like radial blue/green/purple gradients read as SaaS template, not luxury real estate. | Replace with restrained editorial surface, real/generated media, or quiet ink/paper treatment. | 390/1240 screenshots show premium first viewport and next content visible. |
| `.nldir-search`, `.nldir-search input`, `.nldir-search button` | `directory-assets.php` | Rounded block search is usable but generic; button is a large gold pill-like rectangle. | Standard premium search bar with stable 44px controls, labelled fields, refined focus ring, no resizing on hover. | Keyboard focus visible; no clipping in Hebrew; no overflow at 390px. |
| `.nldir-pill`, `.nldir-pill span`, `.nldir-pill i` | `directory-assets.php`, `directory.php` | Colored profession pills plus emoji produce the "cheap icons" problem. | Replace emoji with line icons, neutral chips, precise selected state, compact count chip. | No emoji remains in profession filters. |
| `.nldir-check`, `.nldir-check input` | `directory-assets.php` | Native checkbox with green accent conflicts with premium palette. | Custom checkbox with 44px label tap area, gold/deep-green checked state. | Tap target >=44px; checked state visible without relying on color only. |
| `.nldir-cityb` | `directory-assets.php` | City filters are default small text buttons; mobile pills can create a noisy wall. | Use compact list on desktop and scrollable chip row on mobile with clear selected state. | 390px does not wrap into excessive vertical clutter above results. |
| `.nldir-chip`, `.nldir-chip button` | `directory-assets.php` | Clear button is a small red `x`; low tap target and non-premium visual. | 28px chip with 32-40px icon button, accessible label, restrained destructive hover. | Clear control is keyboard reachable and finger tappable. |
| `.nldir-sortw select` | `directory-assets.php` | Native select looks like a default form control. | Premium select wrapper with custom caret, 44px height, RTL-safe spacing. | Native browser default arrow is not visually dominant. |
| `.nldir-results.is-loading` | `directory-assets.php` | Loading is opacity fade only, which looks broken on slow requests. | Skeleton cards or subtle shimmer, preserving grid height. | AJAX filter does not create empty white flash. |
| `.nldir-more` | `directory-assets.php` | Simple black rectangle; no refined state. | Shared premium secondary/primary variant with loading/disabled state. | Loading text does not shift width; 44px height. |
| `.nldir-empty` | `directory-assets.php` | Plain text empty result. | Premium empty state with line illustration, active reset/search CTA, no toy icon. | Empty search at 390px has one clear next action. |

## Card selectors

| Selector / element | File | Current problem | Premium requirement | QA gate |
| --- | --- | --- | --- | --- |
| `.nldc` | `plugins/nadlan-config/inc/directory-assets.php` | Text-first card with thin colored top stripe feels like a template. | Image/proof-first card anatomy, neutral border, editorial spacing, stable card height. | Cards align in rows at 1240px and remain readable at 390px. |
| `.nldc::before` | `directory-assets.php` | Category color stripe drives toy-like palette. | Remove or convert to subtle tier/proof accent. | No bright category stripe dominates the card. |
| `.nldc-sponsor` | `directory-assets.php`, `sponsored-spot.php` | Rounded gold pill and inline badge placement look ad-hoc. | Small explicit sponsored/featured badge with consistent paid-placement design. | Paid/editorial tier remains transparent and not garish. |
| `.nldc-av` | `directory-assets.php`, `directory.php` | Primary visual is an emoji in a rounded square. This is the biggest cheap-looking signal. | Use real image/logo/monogram/icon mark. No emoji. | `rg` for emoji in directory card renderer returns no live card icon use. |
| `.nldc-name` | `directory-assets.php` | Title typography is decent but cramped beside emoji avatar; no media hierarchy. | Keep serif option, increase hierarchy, clamp consistently, avoid layout shift. | Long Hebrew names do not collide with badge/CTA. |
| `.nldc-pill` | `directory-assets.php` | Bright category label pill reinforces mass-market color system. | Neutral metadata chip with optional icon, 24-28px height. | At most two visible chips before overflow/details. |
| `.nldc-vf` | `directory-assets.php` | Text checkmark lacks badge grammar. | Verified shield/check badge, deep green, accessible label. | Verification is readable in grayscale. |
| `.nldc-stars`, `.nldc-norate` | `directory-assets.php` | Star text and "first to rate" placeholder feel unfinished. | Use rating component or proof row; empty review state should invite credible action. | No raw star glyph row if there are zero reviews. |
| `.nldc-city`, `.nldc-reg` | `directory-assets.php`, `directory.php` | Uses pin/shield emoji in metadata. | Replace with line icons or text labels. | No emoji remains in metadata rows. |
| `.nldc-go` | `directory-assets.php` | Link-style CTA is small and generic. | Use clear action row: profile, call, quote, claim depending context. | CTA order is predictable and tappable. |
| `.nldc-sponsored-spot` | `plugins/nadlan-config/inc/sponsored-spot.php` | Dashed border, megaphone emoji, inline styles, coupon-like composition. | Premium ad slot with editorial layout, generated/fallback visual, one paid CTA, one pricing link. | Sponsored card does not look like a printout among premium cards. |

## Single profile and single listing selectors

| Selector / element | File | Current problem | Premium requirement | QA gate |
| --- | --- | --- | --- | --- |
| `.nlpf-banner` | `plugins/nadlan-config/inc/directory-assets.php` | Current shell can show generic gradient/template styling. | Hero should be media-first or editorial ink/paper, with trust facts and clear CTA. | Above fold communicates project/pro identity without cheap gradient. |
| `.nlpf-av` | `directory-assets.php` | Avatar fallback can inherit cheap icon logic. | Real logo/headshot/project image, then generated monogram fallback. | Missing media still looks intentional. |
| `.nlpf-pill`, `.nlpf-reg` | `directory-assets.php` | Pills and registry proof are not a full trust system. | Convert into proof rail: verified, license/registry, tier, city, updated date. | Trust facts scan before sales copy. |
| `.nlpf-call`, `.nlpf-quote` | `directory-assets.php` | CTAs need shared button grammar and mobile sticky treatment. | Primary/secondary button pair, 44px min, icon plus text, loading/contact states. | Sticky CTA never covers footer/forms. |
| `.nlpf-norate` | `directory-assets.php` | Empty rating state reads incomplete. | Invite first review or hide rating module until credible data exists. | No visible low-trust placeholder on flagship pages. |
| `.nlcard-claim-form input` | `plugins/nadlan-config/inc/cards-render.php` | Boxed fields with basic 8px radius. | Shared premium form field style, labelled fields, error/helper text. | Claim form passes mobile field/tap QA. |
| `.nlcp-btn` | `plugins/nadlan-config/inc/claim-prompt.php` | Claim CTA is isolated from global button system. | Premium primary with clear benefit and trial disclosure. | Claim CTA is consistent with paid funnel buttons. |

## Studio and advertiser self-serve selectors

| Selector / element | File | Current problem | Premium requirement | QA gate |
| --- | --- | --- | --- | --- |
| `.nlst-bar` | `plugins/nadlan-config/inc/studio.php` | Dark gradient rounded panel feels dashboard-like, not elite real-estate publishing. | Editorial command bar: title, status, preview, save, completion score. | 390px keeps actions visible without wrap chaos. |
| `.nlst-save` | `studio.php` | Gold gradient button is acceptable but local-only; no shared loading grammar. | Shared premium primary with locked width, spinner, saved/saving/error states. | Save action cannot double-submit and does not jump width. |
| `.nlst-link` | `studio.php` | Link is text-only and low affordance. | Ghost/text action with external-link icon and focus state. | Keyboard focus visible. |
| `.nlst-help` | `studio.php` | `?` circle feels basic and not accessible enough. | Info icon button with tooltip, accessible label, 40/44px tap target where practical. | All help controls are keyboard accessible. |
| `.nlst-section input/select/textarea` | `studio.php` | Local boxed controls with 9px radius; inconsistent with footer/calculators/Woo. | Unified form grammar: label, helper, underline or refined box, focus ring, errors. | No field below 44px on touch. |
| `.nlst-ai` | `studio.php` | Small AI pills, sparkle emoji, random mode chips. | AI command group with icon, segmented controls, clear selected/loading state. | AI actions do not wrap into unreadable chip soup at 390px. |
| `.nlst-dropzone`, `.nlst-drop-icon`, `.nlst-pick` | `studio.php` | Camera emoji and dashed zone are functional but not premium. | Media uploader with real upload icon, preview-first layout, quality/completeness guidance. | Drag, click, upload progress, error, and empty states all polished. |
| `.nlst-thumb-del` | `studio.php` | Small circular `x` overlay may be under 44px and harsh. | Icon button with confirmation or undo; 40/44px mobile hit target. | Delete is tappable and not accidentally triggered. |
| `.nlst-thumb-cover` | `studio.php` | Cover badge is local gold pill. | Small consistent media badge, positioned without covering key photo content. | Cover state visible on dark/light images. |
| `.nlst-status.is-ok`, `.nlst-status.is-err` | `studio.php` | Status colors are generic green/red blocks. | Toast/inline notice component with icon, refined palette, close/action affordance. | Screen reader announcement and visual state both clear. |

## WooCommerce and monetization selectors

| Selector / element | File | Current problem | Premium requirement | QA gate |
| --- | --- | --- | --- | --- |
| `.woocommerce a.button`, `.woocommerce button.button`, `.woocommerce input.button`, `.woocommerce .button.alt` | `plugins/nadlan-config/inc/catalog-shine.php` | Local ink/gold buttons exist, but not aligned with site-wide grammar and may miss block cart buttons. | Global Woo button pass: product, cart, checkout, account, notices, disabled/loading. | Add-to-cart, checkout, coupon, update-cart all look premium. |
| `.wc-block-components-button` | Woo Cart/Checkout Blocks | May bypass classic Woo selectors. | Add explicit block selector coverage if Woo blocks are used. | Cart/checkout mobile screenshots show real premium buttons. |
| `.woocommerce-message .button`, `.woocommerce-info .button` | `catalog-shine.php` | Notice buttons are gold but not full component state. | Notice action button uses compact secondary/premium variant. | Messages do not look like default Woo strips. |
| `.woocommerce .woocommerce-ordering select` | `catalog-shine.php` | Native select with 8px box. | Premium select wrapper/caret, 44px touch target. | No native gray select visual on mobile. |
| `.woocommerce div.product form.cart .button` | `catalog-shine.php` | Product primary CTA is local only. | Same premium primary as `/join-pro/` checkout CTAs. | Product page CTA hierarchy is obvious. |
| `.woocommerce .quantity .qty` | `catalog-shine.php` | Default quantity box with local border. | Refined stepper/number input treatment. | Touch target and numeric alignment pass. |
| `.select2-container .select2-selection` | `catalog-shine.php` | Select2 can look mismatched. | Tokenized Select2 field, RTL-safe, focus visible. | Checkout fields look like one system. |

## Header, footer, forms, FAB, and content utility selectors

| Selector / element | File | Current problem | Premium requirement | QA gate |
| --- | --- | --- | --- | --- |
| `.nlfab-btn`, `.nlfab-wa` | `docs/wp-state/template-part-footer.html` | Floating buttons can cover content and look like generic sticky widgets. | Premium sticky contact rail with icons, safe-area padding, collapse/minimize behavior. | 390px screenshot shows no overlap with form/cart/footer content. |
| `.nlf input`, `.nlf textarea`, `.nlf select` | `template-part-footer.html` | Underline fields are closer to premium but need shared state and errors. | Move into global form grammar; use consistent labels/helper/errors. | Footer lead modal matches Studio/Woo field style. |
| `button.x` in lead modal | `template-part-footer.html` | Raw `x` close button. | Icon button, 44px touch, focus ring, accessible label. | Close is visible and tappable on mobile. |
| `.wp-block-button__link`, `.wp-element-button` | WordPress content/theme output | Default block buttons can leak into articles and pages. | Global block button reset to premium variants. | `rg`/visual scan finds no default WP blue/rounded CTA. |
| `.nadlan-guide .btn` | `docs/wp-state/page-purchase-tax-calculator.html` | Article guide CTAs are legacy local buttons. | Convert guide CTAs to shared primary/secondary/link variants. | Article CTAs remain premium on recent posts. |
| `.nlc-ptx input[type=number]`, `.nlc-calc input[type=number]` | `docs/wp-state/page-purchase-tax-calculator.html`, `page-mortgage-calculator.html` | Calculator fields are boxed defaults with local shadows/radius. | Unified numeric field with suffix/prefix, helper, focus, 44px min. | Calculators pass 390px overflow and tap QA. |
| `.nlc-radio label` | `page-purchase-tax-calculator.html` | Custom radios hide input and may lack accessible visual/focus. | Proper radio/segmented control with focus-visible and ARIA where needed. | Keyboard can change options. |
| `.nlcalc input`, `.nlcalc select`, `.nlcalc-cta input` | `plugins/nadlan-config/inc/calculators.php` | Mixed underline and boxed controls. | Consolidate into shared calculator/form component. | All calculators share one input language. |
| `.nlhv input` | `plugins/nadlan-config/inc/avm-deals.php` | Basic bordered fields. | Premium lead/valuation form field pattern. | AVM form looks like same site. |
| `.nlnls input` | `plugins/nadlan-config/inc/ai-features.php` | 70% width input with gray border/radius. | Full-width responsive search/AI input with premium command button. | No arbitrary 70% width on mobile. |
| `.nlag-badge` | `plugins/nadlan-config/inc/archive-grid.php` | Badge ownership unclear; can drift from premium standard. | Use shared badge grammar. | Archive badges match card/profile badges. |
| `.nlfp-btn`, `.nlfp-badge` | `plugins/nadlan-config/inc/catalog-shine.php` | Featured-pro block has its own CTA/badge style. | Bring into shared button/badge/token system. | Catalog page does not have one-off CTA styling. |
| `#nladd-cmp button`, `.nlcmp-mount` | `plugins/nadlan-config/inc/compare.php` | Compare tray controls can be tiny/default. | Premium bottom tray, icon buttons, mobile safe-area, clear remove action. | Compare tray does not cover primary CTAs. |

## Search commands for implementation

Claude can start with these non-destructive searches:

```powershell
rg -n "emoji|🏗|🏘|🏢|📣|📍|🛡|📸|✨|📘|🎵|▶|button|btn|pill|badge|chip|input|select|textarea|wp-element-button|wp-block-button|wc-block-components-button" plugins docs
rg -n "nldc-|nldir-|nlpf-|nlst-|nlfab|nlcalc|nlc-|woocommerce|select2|nlcard|nlcp|nlag|nlfp|nlcmp" plugins docs
```

## QA gates

- Screenshot `/projects/`, `/professionals/`, one project, one professional, `/join-pro/`, cart, checkout, Studio, footer lead modal, and two calculator/article pages at 390, 600, 900, and 1240px.
- Confirm no horizontal overflow at 390px.
- Confirm no tap target below 44px for public conversion controls.
- Confirm keyboard focus is visible for every button/link/input/select.
- Confirm no emoji is used as a primary icon in cards, filters, sponsored placements, uploader, or social labels.
- Confirm no default Woo, WP block, Select2, or browser-native-looking button remains in the monetization path.
- Confirm paid/sponsored placements are labelled clearly and look premium.
- Confirm generated fallback assets are original/licensed and labelled illustrative where needed.
