# Asset Truth, Rights and Freshness Standard

## Principle

The portal must be visually rich without becoming visually deceptive. Asset quantity is not a substitute for asset truth.

## Priority order

1. Developer/client-approved real project photograph.
2. Developer-approved architectural rendering/elevation/plan.
3. Licensed, accurately sourced place/context photograph.
4. Original generated project concept, visibly labelled illustrative and used only where allowed.
5. Neutral premium missing state.

Never use an unrelated stock tower/interior as though it depicts the project.

## Public asset states

| State | Meaning | Allowed public treatment |
| --- | --- | --- |
| `official_photo` | Approved photograph of real project/site/unit | Primary hero/card/gallery |
| `official_render` | Approved developer/architect rendering | Primary with visible rendering caption |
| `official_plan` | Approved current plan/specification | Plan/document area with date/version |
| `licensed_context` | Licensed real place/area image | Area/context section, not project representation |
| `illustrative_concept` | Original/generative/prototype concept | Visible `המחשה בלבד`; not eligible for external launch hero unless owner explicitly accepts |
| `prototype_model` | Non-official 3D/massing/showroom scaffold | Internal review or visibly bounded demo only |
| `missing` | No truthful publishable visual | Neutral designed state; quality gate may keep record out of featured surfaces |
| `expired/blocked` | Permission expired, disputed or withdrawn | Immediately removed from public delivery |

## Required evidence per asset

- Source and original filename/URL/reference.
- Rights holder.
- Permission basis: owned, supplied under agreement, licensed, public-data rule, original generated.
- Authorized channels/markets/languages.
- Approval identity/date.
- Expiry/withdrawal condition.
- Asset type and illustrative state.
- Project/location relationship.
- Caption and alt text.
- Version/date for plans/documents/renderings.
- Crop/focal point and responsive derivatives.

“Found on the developer website” is a source, not permission to republish.

## Repository review assets

The preview uses existing generated/prototype images solely to communicate composition and density. The repository source notes establish that:

- Ashira concept images are not official developer renders.
- Rainbow model, drawings, units, plans and showroom media are illustrative/prototype and not live inventory.
- Dimri's scaffold/poster is illustrative; real prices, inventory, plans and media require owner/developer approval.
- Generic premium-site/showroom images are concept assets, not actual projects or units.

Every preview surface therefore carries a visible review/illustrative notice. These images must not be mistaken for presentation approval.

## Minimum external-presentation media pack per flagship project

- 1 approved hero, ideally 2400px+ wide with desktop/mobile crop guidance.
- 3 approved exterior/context images.
- 3 approved residence/interior images where genuinely representative.
- 2 approved amenity images or honest rendering states.
- Approved developer logo and identity usage.
- At least one approved plan for every displayed unit/plan type.
- Approved brochure/specification when offered.
- Poster and source package for any public video/3D experience.
- Captions, alt text, rights and approval for HE/EN.

If a developer cannot provide this pack, the project can remain searchable in a basic state but should not occupy the premium homepage rail or external investor presentation.

## Card/hero crop rules

- Project card: 4:3, center/focal-point controlled, no text baked into the image.
- Homepage hero: 16:9 or wider, meaningful subject preserved at 1440 and 390 crops.
- Gallery: retain original aspect ratio where practical; avoid aggressive portrait-to-landscape crops.
- Plan/document: never crop dimensions, legends or legal disclaimers.
- Logo: contained, no forced stretch or unapproved recoloring.
- Rendering/illustration label remains readable at mobile.

## Freshness is different from edit time

| Timestamp | Meaning |
| --- | --- |
| Published/modified | WordPress content change |
| Source date | Date on the underlying developer/official/public material |
| Verified at | Date NadLan checked the claim/asset/contact |
| Next review at | Required future check |
| Rights expiry | Last permitted public-use date |

The buyer-facing page uses the relevant verification/source date. A copy edit today does not make a six-month-old price current.

## Stale degradation rules

- Exact price/availability/payment language expires first and becomes confirmation wording.
- Badges tied to missing/expired evidence disappear.
- Expired media is removed immediately and its count recalculated.
- The project may retain stable identity/history while volatile facts are under review.
- Featured placement eligibility is removed whenever the basic verified or media gate fails.
- A conflict opens an editorial state; public copy explains material unresolved discrepancies when the page remains useful.

## External-presentation gate

An image-rich preview is not enough. Before a developer/investor sees the live site:

- all above-the-fold images have approved rights;
- no visible demo/prototype labels remain except intentionally disclosed conceptual material;
- every thumbnail accurately belongs to its project/place;
- gallery counts and media buttons are real;
- plans/documents are current and legible;
- HE/EN captions and alt text exist;
- mobile crops are reviewed;
- rights evidence is stored outside public delivery but linked to the attachment record.

## Performance and accessibility

- Generate AVIF/WebP/JPEG fallbacks as the implementation supports.
- Use `srcset`/sizes and declared width/height or aspect ratio.
- Eager/high-priority load only the LCP hero; lazy-load offscreen thumbnails.
- Avoid autoplay video and heavy 3D in the critical path.
- Alt text describes what the image shows, not keyword stuffing.
- Decorative crops use empty alt; informative plans have meaningful accessible context or a text equivalent.
- Maintain text/background contrast over imagery with a tested overlay, not a guess.
