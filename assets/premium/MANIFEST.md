# Premium asset manifest

Branch: `codex/premium-assets`
Scope: assets only. No PHP, no version bump, no routes, no live changes.

These files are implementation assets for Claude to wire into the specs already opened in PR #36, PR #37, and PR #38.

## Files

| File | Purpose |
| --- | --- |
| `assets/premium/icons-micro-ui.svg` | Reusable SVG symbol sprite for tiny controls, CTAs, Studio controls, and contact actions. |
| `assets/premium/profession-marks.svg` | Reusable SVG symbol sprite for directory category/profession marks. |
| `assets/premium/initial-monogram-avatar-template.svg` | Standalone SVG template for no-photo professional/listing avatars. Replace `{{INITIALS}}`. |
| `assets/premium/premium-fallback-illustrations.svg` | Reusable SVG symbol sprite for sponsored slots, empty states, project fallback, and upload empty state. |
| `assets/premium/button-treatment-reference.svg` | Visual reference sheet for primary, secondary, and ghost button states in RTL. |
| `assets/premium/advertiser-flow-icons.svg` | Reusable SVG symbol sprite for monetization, campaign, order, lead, and Studio completion states. |
| `assets/premium/tier-status-reference.svg` | Visual reference sheet for paid-tier badges and campaign/account states. |
| `assets/premium/preview.html` | Local visual preview for Claude/owner review of all SVG assets before PHP/CSS wiring. |
| `assets/premium/contact-sheet.svg` | Static self-contained SVG contact sheet generated from the actual sprite symbols for direct visual review. |
| `assets/premium/hero-project-fallback.svg` | Standalone 16:10 project/property hero fallback for listings without legal photography. |
| `assets/premium/profile-background-fallback.svg` | Standalone 16:9 professional profile background fallback for profiles without headshot/logo media. |
| `assets/premium/sponsored-card-background.svg` | Standalone 4:3 sponsored placement background for `.nldc-sponsored-spot` and upsell cards. |
| `assets/premium/upload-empty-state.svg` | Standalone Studio media upload/gallery empty-state illustration. |

## Micro UI icon mapping

Source file: `assets/premium/icons-micro-ui.svg`

Usage pattern:

```html
<svg class="nl-icon" aria-hidden="true"><use href="/assets/premium/icons-micro-ui.svg#chip-clear"></use></svg>
```

| Symbol id | Primary selectors | Existing PR-spec section served |
| --- | --- | --- |
| `chip-clear` | `.nldir-chip button`, chip clear controls in advertiser center and Studio | PR #38 `Button grammar`, `Micro interaction states`, selector checklist `Directory and project archive selectors` |
| `close` | lead modal `button.x`, `.nlst-thumb-del`, dialog close buttons, Woo notices where dismissible | PR #38 `Button grammar`, `Icons and badges`, selector checklist `Header, footer, forms, FAB` |
| `help` | `.nlst-help`, field help bubbles, pricing hints | PR #38 `Icons and badges`, selector checklist `Studio and advertiser self-serve selectors` |
| `info` | explanatory tooltips, pricing/package notes, form helper affordances | PR #37 advertiser journey QA, PR #38 `Forms` |
| `upload` | `.nlst-pick`, `.nlst-dropzone`, media upload buttons | PR #38 selector checklist `.nlst-dropzone`, `.nlst-pick`; PR #36 media/fallback direction |
| `delete-overlay` | `.nlst-thumb-del`, gallery remove, media card delete | PR #38 selector checklist `.nlst-thumb-del`; `Button grammar` danger/icon button |
| `save` | `.nlst-save`, advertiser-center save/update actions | PR #38 `Button grammar`; PR #37 Studio/self-serve QA |
| `preview-external` | `.nlst-link`, public preview, external profile/site links | PR #38 `Button grammar`; selector checklist `.nlst-link` |
| `fab-contact` | `.nlfab-btn`, floating lead/contact FAB, mobile contact rail | PR #38 selector checklist `.nlfab-btn`, `Mobile breakpoints` |
| `filter` | `.nldir-pill`, mobile filter drawer buttons, archive filter trigger | PR #36 catalog filter-bar treatment; PR #38 selector checklist `.nldir-pill` |
| `sort` | `.nldir-sortw select`, sort trigger/replacement control | PR #36 filter/sort treatment; PR #38 selector checklist `.nldir-sortw select` |
| `call` | `.nlpf-call`, `.nlfab-btn[href^="tel:"]`, card call CTA | PR #36 single-profile hero/CTA; PR #38 selector checklist `.nlpf-call` |
| `quote` | `.nlpf-quote`, quote CTA, lead request CTA | PR #36 single-profile CTA; PR #37 advertiser/lead funnel QA |
| `whatsapp` | `.nlfab-wa`, WhatsApp CTA, profile contact CTA | PR #38 selector checklist `.nlfab-wa`; PR #37 lead/contact funnel |
| `claim` | `.nlcp-btn`, claim prompt, verified ownership CTA | PR #37 claim/attach flow; PR #38 selector checklist `.nlcp-btn` |

## Profession and category mark mapping

Source file: `assets/premium/profession-marks.svg`

Usage pattern:

```html
<svg class="nldc-mark" aria-hidden="true"><use href="/assets/premium/profession-marks.svg#profession-contractor"></use></svg>
```

| Symbol id | Replaces / serves selectors | Existing PR-spec section served |
| --- | --- | --- |
| `profession-architect` | `.nldc-av`, `.nlpf-av`, `.nldir-pill[data-prof="architect"]` | PR #36 card anatomy/badge system; PR #38 `Icons and badges` |
| `profession-lawyer` | `.nldc-av`, `.nlpf-av`, `.nldir-pill[data-prof="lawyer"]` | PR #36 professional card visuals; PR #38 selector checklist `.nldc-av` |
| `profession-appraiser` | `.nldc-av`, `.nlpf-av`, `.nldir-pill[data-prof="shamai"]` | PR #36 card visuals; PR #38 selector checklist `.nldir-pill` |
| `profession-contractor` | `.nldc-av`, `.nlpf-av`, `.nldir-pill[data-prof="kablan"]` | PR #36 premium catalog card spec; PR #38 selector checklist `.nldc-av` |
| `profession-developer` | project/developer cards, `.nldc-av`, `.nlpf-av`, future developer profile | PR #36 listing/profile visuals; PR #38 `Cards` |
| `profession-mortgage` | `.nldc-av`, `.nlpf-av`, `.nldir-pill[data-prof="mashkanta"]` | PR #36 professional profile visuals |
| `profession-inspector` | `.nldc-av`, `.nlpf-av`, `.nldir-pill[data-prof="bedek_bait"]`, `.nldir-pill[data-prof="mefakeach"]` | PR #36 directory marks; PR #38 selector checklist `.nldir-pill` |
| `profession-broker` | `.nldc-av`, `.nlpf-av`, `.nldir-pill[data-prof="metavech"]` | PR #36 professional cards; PR #38 `Icons and badges` |
| `category-project` | project archive cards, `.nldc-av` on `/projects/`, project fallback badge | PR #36 project card layout and image fallback |
| `category-property` | property archive cards, property fallback badge | PR #36 listing card visuals |

## Monogram avatar mapping

Source file: `assets/premium/initial-monogram-avatar-template.svg`

| Use | Selectors | Existing PR-spec section served |
| --- | --- | --- |
| Professional without headshot/logo | `.nldc-av`, `.nlpf-av` | PR #36 profile visuals; PR #38 `Cards`, `Asset plan` |
| Project/property without legal thumbnail but not enough space for full fallback image | `.nldc-av`, compact card media placeholder | PR #36 empty-state treatments; PR #38 `Asset plan` |
| Advertiser center owned-card picker | advertiser center card avatar/icon slot | PR #37 attach-to-card path; PR #38 micro UI consistency |

Implementation note: replace `{{INITIALS}}` with a sanitized 1-2 character monogram. If Hebrew initials are used, keep the text centered and test at 390px.

## Fallback illustration mapping

Source file: `assets/premium/premium-fallback-illustrations.svg`

| Symbol id | Selectors / surfaces | Existing PR-spec section served |
| --- | --- | --- |
| `sponsored-spot` | `.nldc-sponsored-spot`, `.nldc-sponsor`, paid placement empty ad slot | PR #36 sponsored state design; PR #38 selector checklist `.nldc-sponsored-spot` |
| `empty-search` | `.nldir-empty`, empty filters/search, no owned cards in advertiser center | PR #36 empty-state treatments; PR #38 `Micro interaction states` |
| `project-fallback` | project/property cards with no legal image, single project fallback hero | PR #36 generated-asset plan; PR #38 `Asset plan` |
| `upload-empty` | `.nlst-dropzone`, Studio media uploader empty state | PR #37 Studio QA; PR #38 selector checklist `.nlst-dropzone` |

Standalone SVG fallbacks:

| File | Selectors / surfaces | Existing PR-spec section served |
| --- | --- | --- |
| `hero-project-fallback.svg` | `.nldc` project/property cards, single project/property hero, `.nlpf-banner`, media gallery fallback | PR #36 image-first cards and empty-state treatments; PR #38 `Asset plan` |
| `profile-background-fallback.svg` | professional single hero, `.nlpf-banner`, professional cards without logo/headshot | PR #36 single-profile hero; PR #38 card/profile fallback rules |
| `sponsored-card-background.svg` | `.nldc-sponsored-spot`, `.nldc-sponsor`, advertiser upsell cards, available paid placement | PR #36 sponsored state design; PR #38 selector checklist `.nldc-sponsored-spot` |
| `upload-empty-state.svg` | `.nlst-dropzone`, `.nlst-gallery:empty`, Studio image onboarding | PR #37 Studio upload QA; PR #38 selector checklist `.nlst-dropzone` |

## Button treatment reference

Source file: `assets/premium/button-treatment-reference.svg`

| Serves | Selectors | Existing PR-spec section served |
| --- | --- | --- |
| Primary/default/hover/focus/disabled reference | `.woocommerce a.button`, `.woocommerce button.button`, `.woocommerce input.button`, `.woocommerce .button.alt`, `.wc-block-components-button`, `.nlst-save`, `.nlst-pick`, `.nldir-more`, `.nlpf-call`, `.nlpf-quote`, `.nlcp-btn`, `.wp-block-button__link`, `.wp-element-button`, `.nadlan-guide .btn`, `.nlfab-btn` | PR #38 `Button grammar`, `Micro interaction states`; PR #36 premium catalog target |

## Advertiser monetization and campaign state mapping

Source file: `assets/premium/advertiser-flow-icons.svg`

Usage pattern:

```html
<svg class="nl-af-icon" aria-hidden="true"><use href="/assets/premium/advertiser-flow-icons.svg#tier-premier"></use></svg>
```

| Symbol id | Selectors / surfaces | Existing PR-spec section served |
| --- | --- | --- |
| `tier-free` | free card state, unpaid listing badge, advertiser center card status | PR #37 advertiser tier QA; PR #38 badge/state grammar |
| `tier-pro` | `paid_tier=pro`, `.nldc-sponsor`, upgrade package cards, advertiser center tier chip | PR #37 paid tier/order bridge; PR #38 `Icons and badges` |
| `tier-premier` | `paid_tier=premier`, featured/premier card state, flagship/editorial premium marker | PR #36 premium catalog spec; PR #37 editorial premium note |
| `tier-project-premier` | product `489`, project campaign package, `/join-pro/` project package card | PR #37 product-to-tier QA; PR #38 monetization buttons/states |
| `tier-property-pro` | product `490`, property promotion package, property card paid state | PR #37 product-to-tier QA |
| `paid-order` | order row/card in advertiser center, paid order details, attach order to card path | PR #37 no-card-id fallback and attach-to-card path |
| `billing-card` | checkout/account billing state, Woo order/payment surfaces | PR #37 billing/order management; PR #38 Woo buttons/states |
| `campaign-calendar` | `campaign_end` display, active campaign countdown, renewal prompts | PR #37 campaign_end QA and downgrade cron visibility |
| `campaign-expired` | expired campaign state after daily downgrade, renewal CTA | PR #37 daily downgrade cron and non-permanent paid tier gate |
| `attach-card` | unassigned paid order, card picker, "attach to card" UI | PR #37 card_id fallback requirement |
| `exposure-chart` | advertiser center exposure panel, paid value proof, directory float-up explanation | PR #37 advertiser journey QA; PR #36 premium sponsored value |
| `lead-inbox` | lead count panel, exact `lead_card_id` attribution, advertiser center leads | PR #37 lead attribution QA |
| `verified-shield` | `.nldc-vf`, `.nlpf-reg`, claim verified state, editorial showcase verified state | PR #36 trust badges; PR #38 selector checklist `.nldc-vf` |
| `completion-meter` | Studio completion score, listing quality checklist, onboarding progress | PR #37 Studio QA; PR #38 micro interaction states |
| `ai-copy` | `.nlst-ai`, AI copy/improve/shorten/expand actions | PR #37 self-serve Studio QA; PR #38 selector checklist `.nlst-ai` |
| `gallery-media` | `.nlst-gallery`, media completeness, listing image state | PR #36 image-first cards; PR #38 selector checklist `.nlst-gallery` |
| `map-pin-premium` | `.nlst-map`, project/property map field, card location row | PR #36 single profile/project field map; PR #38 `Forms` |

## Tier and status reference

Source file: `assets/premium/tier-status-reference.svg`

| Serves | Selectors / surfaces | Existing PR-spec section served |
| --- | --- | --- |
| Paid-tier badge visual reference | `.nldc-sponsor`, `.nldc-pill`, `.nlpf-pill`, advertiser center tier chips, `/join-pro/` package cards | PR #36 badge system; PR #37 paid tier/product mapping; PR #38 `Icons and badges` |
| Campaign/account status reference | advertiser center card state, order rows, renewal/expired prompts, active campaign countdown | PR #37 billing/order/campaign QA; PR #38 `Micro interaction states` |

## Needs Claude/owner generation

No raster assets were generated in this branch. The user explicitly asked not to burn retries on unreliable raster/browser/upload work. These should be generated or selected later, then uploaded through the owner-approved media path.

### Architectural project fallback hero

Use for: project/property cards and single heroes where there are no legal photos.

Prompt:

```text
Create an original premium architectural fallback image for an Israeli real-estate project listing. Abstract Tel Aviv coastal high-rise forms, refined facade rhythm, warm paper background, ink linework, muted gold highlights, no people, no logos, no text, no photorealistic claim, luxury editorial real-estate style, 16:10 wide composition, suitable as an illustrative placeholder.
```

Selectors/surfaces: `.nldc` project cards, single project hero, `.nlpf-banner`, future media gallery fallback.

### Professional profile no-photo background

Use for: single professional profile hero when there is no headshot/logo/project image.

Prompt:

```text
Create a restrained premium professional profile background for an Israeli real-estate expert directory. Minimal office/architectural line texture, paper and ink palette, subtle muted gold rule, no face, no logo, no text, no cartoon, editorial luxury directory style, 16:9 composition.
```

Selectors/surfaces: `.nlpf-banner`, `.nlpf-av`, professional profile hero media area.

### Sponsored placement premium card background

Use for: paid available slot in the catalog.

Prompt:

```text
Create a premium sponsored-placement background for a real-estate directory card. Warm paper, subtle architectural grid, small gold spotlight motif, no megaphone emoji, no ad clutter, no text, no logo, compact 4:3 composition.
```

Selectors/surfaces: `.nldc-sponsored-spot`, `.nldc-sponsor`.

## Rules for implementation

- These assets are safe source assets only. They do not change live rendering until Claude wires them.
- Keep icons `currentColor` so PHP/CSS controls color through tokens.
- Do not inline emoji next to these icons. Replace emoji UI, do not decorate it.
- Use accessible labels on buttons. Symbols can be `aria-hidden="true"` when text labels are present.
- Keep paid/sponsored placements explicitly labelled.
- Test all wired uses at 390, 600, 900, and 1240px before merging implementation.
