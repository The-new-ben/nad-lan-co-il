# Site-wide premium micro UI standard

Date: 2026-06-04
Scope: docs-only implementation standard for nad-lan.co.il. No public routes, no plugin module edits, no version bump.

## Owner intent

The site must stop reading as a generic WordPress template. The standard is not only "better cards" on `/projects/`. Every surface, down to the smallest close button, icon chip, form control, WooCommerce notice button, Studio upload affordance, and sticky mobile CTA, must feel deliberate, expensive, and trustworthy.

Premium here means restraint, precision, durable typography, high-quality media, real hierarchy, and polished interaction states. It does not mean neon gradients, childish emoji icons, noisy badges, oversized pills, or default browser/WooCommerce buttons.

## Reference signals checked

These are the live/current reference targets used for the standard. The lesson is the point, not a request to copy their UI. Access note: several real-estate portals block scripted fetches with 403/429 responses, so Claude should also do a normal browser visual pass before implementation. The selector map and required Nadlan fixes below do not depend on copying inaccessible source code from any competitor.

| Source | URL | Design lesson for Nadlan |
| --- | --- | --- |
| Zillow Showcase | https://www.zillow.com/news/zillow-showcase-brings-listings-to-life// | Premium listings are sold through immersive media, interactive floor plans, flyover-style context, and upgraded presentation. Nadlan paid tiers need a clear visual upgrade, not only a text badge. |
| Zillow 3D Home floor plans | https://www.zillow.com/3d-home/floor-plans/ | Even utility media can be framed as a polished product feature. Empty project pages should guide owners toward floor plans, gallery, video, and map completeness. |
| Compass | https://www.compass.com/ | The public surface is quiet and search-first. Buttons and filters are not playful; they are crisp, neutral, and high-confidence. |
| Sotheby's International Realty | https://www.sothebysrealty.com/ | Luxury pages use editorial restraint, strong imagery, and minimal chrome. The brand does not need bright UI colors to feel premium. |
| The Modern House | https://themodernhouse.com/ | The premium signal comes from curation, editorial type, white space, and architectural photography. Nadlan project pages should feel curated, not scraped. |
| LoopNet | https://www.loopnet.com/ | Commercial users need dense facts, stats, and search clarity. Premium does not mean hiding utility; it means making professional data easy to scan. |
| Houzz professionals | https://www.houzz.com/professionals | Professional profiles rely on proof: ratings, verified/license cues, project photos, badges, and clear contact actions. Nadlan's pro cards need trust hierarchy instead of decorative emoji. |
| Houzz pro directory policy | https://pro.houzz.com/pro-help/r/pros-shown-on-houzz | Sponsored placements must be clearly labelled. Nadlan can look premium while staying explicit about paid placement. |
| idealista | https://www.idealista.com/ | High-volume search portals can stay practical, compact, and fast. Nadlan filters must remain efficient on mobile rather than becoming decorative panels. |
| realestate.com.au | https://www.realestate.com.au/ | Consumer real-estate UX blends search, saved state, alerts, and property education. Nadlan CTAs should feel like useful next actions, not generic "learn more" buttons. |

Automated fetch status from this workspace:

| URL | Status |
| --- | --- |
| `https://www.zillow.com/news/zillow-showcase-brings-listings-to-life//` | 403 to scripted fetch |
| `https://www.zillow.com/3d-home/floor-plans/` | 403 to scripted fetch |
| `https://www.compass.com/` | 200 |
| `https://www.sothebysrealty.com/` | 202 |
| `https://themodernhouse.com/` | 403 to scripted fetch |
| `https://www.loopnet.com/` | 403 to scripted fetch |
| `https://www.houzz.com/professionals` | 200 |
| `https://pro.houzz.com/pro-help/r/pros-shown-on-houzz` | 200 |
| `https://www.idealista.com/` | 403 to scripted fetch |
| `https://www.realestate.com.au/` | 429 to scripted fetch |

## Design tokens

Claude should implement a shared token layer before styling individual selectors. The site already has several local token attempts, but they are fragmented across inline CSS blocks.

Required token direction:

| Token | Value direction | Usage |
| --- | --- | --- |
| Ink | `#1B1A17`, `#2D2A24`, `#5E5A50` | Primary text, button fill, high-confidence UI. |
| Paper | `#FFFFFF`, `#FBF9F5`, `#F4EFE6` | Page background, elevated panels, empty states. |
| Gold | `#9C7A3C`, `#B89254`, `#D7C08A` | Premium accents, selected state, focus, sponsored label. |
| Deep green | `#0E3B33`, `#165A4A` | Trust/verified secondary accent. |
| Error | `#9F2D20` | Form errors only. Never use loud red for decorative chips. |
| Line | `rgba(27,26,23,.12)` and `rgba(27,26,23,.22)` | Hairlines, separators, input borders. |
| Radius | 0, 2, 4, 6, 8 | Cards and controls should be 8px or less unless avatar/circular icon. |
| Shadow | subtle layered shadows only | `0 10px 30px rgba(27,26,23,.08)` maximum for normal cards. Avoid floaty toy shadows. |

No dominant pink/blue/purple card system. No cyber gradient hero. No emoji color palette. No bright rounded colored badges as the main visual language.

## Typography

Use a serif/sans split. Current code already references `Frank Ruhl Libre` and `Heebo`; keep that direction but standardize scale.

| Role | Desktop | Mobile | Weight | Notes |
| --- | ---: | ---: | --- | --- |
| Page H1 | 44-56px | 32-38px | 500-600 | Serif, restrained, no negative letter spacing. |
| Section H2 | 28-34px | 24-28px | 500-600 | Serif or high-confidence sans depending on page. |
| Card title | 18-22px | 17-20px | 600 | Clamp to 2 lines; do not resize card height unpredictably. |
| Body | 16-18px | 16px | 400 | Hebrew line-height 1.65-1.8. |
| Meta | 13-14px | 13-14px | 500 | No text below 12px except legal/utility. |
| Label | 12.5-13.5px | 13px | 600 | Fixed labels above fields, not placeholder-only forms. |
| Button | 14.5-16px | 15-16px | 650-750 | Line-height 1; min height 44px on touch. |

Letter spacing must be 0 for normal Hebrew text. Uppercase English eyebrow text may use slight positive spacing only where the text is Latin.

## Button grammar

No default button is allowed anywhere public or self-serve. This includes `wp-element-button`, WooCommerce buttons, Studio buttons, floating contact buttons, calculator CTAs, close buttons, load-more buttons, and chip clear buttons.

Required variants:

| Variant | Visual | Behavior |
| --- | --- | --- |
| Primary | Ink fill, paper text, 1px ink border | Hover gold or deep green only when action is commercial/positive; active presses down 1px; min height 44px. |
| Premium primary | Gold fill, ink or white text depending contrast | Use for paid upgrade, checkout, publish, save, request quote. Must not be overused on every card. |
| Secondary | Transparent paper, ink text, hairline border | Hover light paper fill, border strengthens. |
| Ghost/text | No box, ink/gold text, underline or arrow cue | Use for low-risk navigation, never primary conversion. |
| Icon button | Square 40px desktop, 44px touch, 1px hairline | Use for close/delete/reorder/zoom/share. Use a real icon, not `x`, `?`, emoji, or text in a pill. |
| Danger | Transparent or soft error outline | Delete/remove only; never bright red filled unless destructive confirmation. |
| Loading | Locked width, spinner/progress, disabled style | Text must not jump when state changes from "save" to "saving". |
| Disabled | Muted, visible, cursor default | Must explain reason nearby where action is monetized. |

Buttons must use stable dimensions. Hover/focus cannot change width/height. Buttons with Hebrew text must not clip at 390px viewport.

## Micro interaction states

Every interactive element needs these states:

| State | Standard |
| --- | --- |
| Default | Calm, high contrast, aligned to token system. |
| Hover | Subtle background or border shift; no large lifts on dense grids. |
| Active | 1px press or reduced shadow. |
| Focus-visible | 2px gold ring or underline plus 2px offset. Must be keyboard-visible. |
| Loading | Skeleton, shimmer, spinner, or disabled state with stable size. |
| Error | Human-readable error, no alert-only failures. |
| Empty | Editorial prompt plus next action. Never a blank white card or toy icon. |

## Icons and badges

Replace emoji icons with a coherent icon system. Use Lucide-style 1.5px stroke icons or equivalent inline SVG. Examples:

| Current pattern | Replacement |
| --- | --- |
| Construction/building/house emoji in `.nldc-av` | Monoline category icon, neutral/gold line, optional generated category mark. |
| Megaphone emoji in `.nldc-sponsored-spot` | Sponsored placement icon: small gold line megaphone or spotlight, no emoji. |
| Checkmark text in `.nldc-vf` | Verified badge with shield/check icon and explicit text. |
| Social label emoji in Studio | Real network icons or text labels with neutral icon buttons. |
| `?` help bubbles | Info icon button with tooltip and accessible label. |
| `x` close/delete | X icon button with hover/focus/destructive state. |

Badge rules:

- Sponsored/paid badges must be transparent about paid placement.
- Badge height should be 24-28px, not large toy pills.
- Avoid hot pink, bright blue, lime, and random category colors.
- Use no more than two badges per card before overflow collapses into details.

## Cards

Cards should be image-first for real estate and proof-first for professionals.

Project/property card:

- 4:3 or 16:10 image area first.
- Title, city, project status, developer, units, and tier badge in a fixed hierarchy.
- No emoji avatar as primary visual.
- Missing image uses a premium generated fallback asset, not a blank or emoji.
- Sponsored/editorial tier gets better media treatment and placement, not a gaudy border.

Professional card:

- Portrait/logo or generated monogram mark first, then name and specialty.
- Verified/license proof, city, registry number, rating/review status.
- CTA row must distinguish `profile`, `call`, `quote`, and `claim`.

Sponsored slot:

- Must look like a premium media placement, not a dashed coupon.
- Label: "Sponsored" or Hebrew equivalent, high contrast and small.
- Visual: editorial background, premium icon, concise value proposition.
- CTA: one primary action and one subdued compare-pricing link.

## Forms

All inputs, selects, textareas, search fields, WooCommerce checkout fields, Studio fields, and modal lead forms must share one form grammar:

- Label above every field. Placeholder is hint only.
- Minimum 44px field height.
- Border or underline style must be consistent per surface.
- Focus visible in gold.
- Error and helper text below field, 13-14px.
- RTL-safe padding and icons.
- Selects must use custom caret or native select with premium wrapper, not default gray boxes.
- Numeric inputs need suffix/prefix treatment for NIS, percent, sqm, years.
- Checkbox/radio controls need custom 18-20px marks with 44px label tap area.

## Mobile breakpoints

The minimum QA grid:

| Width | Gate |
| ---: | --- |
| 390px | No horizontal overflow; all tap targets >=44px; sticky/FAB does not cover content or checkout. |
| 600px | Cards transition cleanly from single to two columns only where density supports it. |
| 900px | Tablet filters and sidebars must not force desktop widths. |
| 1240px | Desktop max-widths and gutters must feel intentional; no narrow WordPress column floating on a huge beige canvas. |

The `/projects/` audit previously showed a mobile viewport rendering as 980px-wide content. That is a blocker class of issue: premium UI cannot exist if the page ignores the device width.

## Site-wide surfaces that must be included

Claude implementation should treat these as one batch, not separate polish jobs:

- Directory/catalog archives: `/projects/`, `/professionals/`, property archive, Woo product/catalog surfaces.
- Single pages: project, professional, property, article pages with CTAs, calculators, and forms.
- Advertiser funnel: `/join-pro/`, cart, checkout, advertiser center, Studio.
- Header/footer: nav, mobile menu, floating contact buttons, lead modal, newsletter/contact form.
- Utility content: mortgage calculator, purchase tax calculator, sitemap, guide CTAs, compare tray.
- WordPress/Woo defaults: block buttons, checkout buttons, notices, tabs, pagination, Select2.

## Asset plan

No new bitmap assets are needed for tiny buttons themselves. The premium replacement is a shared icon system and a fallback visual library.

Generate or create these assets only when implementing:

| Asset | Format | Use |
| --- | --- | --- |
| Project fallback hero | SVG or generated PNG/WebP | Cards/projects with no legal photos. Abstract architectural facade, neutral palette, marked illustrative. |
| Professional monogram frame | SVG | Professionals with no headshot/logo. Initials, thin border, no emoji. |
| Category icon set | Inline SVG/Lucide | Project, professional, property, verified, sponsored, claim, upload, delete, save, share, phone, WhatsApp. |
| Empty-state illustration | SVG | Empty search results, no cards, no images, no reviews. Restrained line drawing, not cartoon. |
| Sponsored placeholder | SVG or CSS art | Sponsored slot background, gold hairline, small icon, premium CTA. |

Legal note: do not copy Madlan/Yad2/developer photos. For missing photos use original generated assets or licensed/CC imagery, with captions where needed.

## Implementation rule

This document is a spec. It intentionally does not touch plugin code. Public routes and plugin module edits still require Claude sign-off. The implementation should be one coherent UI pass with screenshot QA, not scattered local fixes.
