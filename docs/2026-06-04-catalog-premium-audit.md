# Premium Catalog Before-State Audit

Date: 2026-06-04
Scope: `/projects/`, `/professionals/`, one live project profile, and one live professional profile on `nad-lan.co.il`.
Constraint: docs-only audit. No plugin code, no routes, no version bump.

## What I Audited

Live surfaces:

- `https://nad-lan.co.il/projects/`
- `https://nad-lan.co.il/professionals/`
- `https://nad-lan.co.il/projects/rainbow-tel-aviv/`
- `https://nad-lan.co.il/professionals/×’×‘××™-×ž×™×›××œ-2/`

Relevant implementation ownership found by class search:

- `plugins/nadlan-config/inc/directory.php`
- `plugins/nadlan-config/inc/directory-assets.php`
- `plugins/nadlan-config/inc/sponsored-spot.php`
- `plugins/nadlan-config/inc/ga4-events.php`

Important standing rule: this audit does not propose any new public URL. It follows `skills/url-namespace-contract.md`: no new public route or plugin module edit without Claude and owner sign-off.

## Surface 1: `/projects/`

The project catalog is functionally useful, but visually it reads like a lightweight WordPress directory rather than a premium real-estate marketplace.

| Element / class | Severity | Failure | Why it matters |
| --- | --- | --- | --- |
| `.nldc-av` | Blocker | The card avatar is an emoji, for example `ðŸ¢`, inside a small rounded square. | A serious project catalog needs photography, architectural renders, developer logos, or disciplined generated fallbacks. Emoji turns a high-value development into a toy-like object. |
| `.nldc-pill` | Major | Project type appears as a bright pill such as `×‘× ×™×™×” ×—×“×©×”`, using current blue/pink/cyber-accent logic. | The category label is louder than the project story. It feels like a tag cloud, not luxury editorial UI. |
| `.nldc-sponsor` | Major | Featured placement is only a small gold `×ž×§×•×“×` pill. | A paid or editorial premium card should feel materially better through media, hierarchy, and confidence signals. The current badge is an afterthought. |
| `.nldc` | Major | Cards are image-free white boxes with a colored top rule and icon/avatar. | The catalog does not let a buyer scan quality, style, neighborhood, or price posture visually. It looks like a data export. |
| `.nldc-reg` | Minor | The repeated `data.gov.il` trust footer is tiny and mechanical. | Trust is important, but repeated registry text at the bottom of every card does not create emotional confidence or premium value. |
| `.nldir-pill` | Major | The filter pills sit on a dark gradient hero and use glassy rounded styling. | This creates a â€œdashboard demoâ€ feeling. Premium real-estate catalogs usually use quieter segmented controls, refined filter drawers, or map/list controls. |

Specific live example: the Rainbow Tel Aviv card floats first and is marked `is-featured`, but it still uses `.nldc-av` with `ðŸ¢`, `.nldc-pill`, `.nldc-sponsor`, and a registry footer. The content is premium; the catalog shell is not.

## Surface 2: `/professionals/`

The professional directory has the same shell, but the visual mismatch is even sharper because professional trust depends on identity, proof, reviews, and work examples.

| Element / class | Severity | Failure | Why it matters |
| --- | --- | --- | --- |
| `.nldc-av` | Blocker | Professional avatars are emojis such as `ðŸ—ï¸`, not real logos, headshots, project images, or generated professional marks. | A contractor, lawyer, appraiser, or architect profile must look accountable. Emoji makes the directory feel unverified even when registry data exists. |
| `.nldc-pill` | Major | Profession labels use the same colored-pill system as projects. | The taxonomy is visible, but not authoritative. Premium professional directories make specialties feel precise and credentialed. |
| `.nldc-rate.nldc-norate` | Major | Many cards repeat `×”×™×• ×”×¨××©×•× ×™× ×œ×“×¨×’`. | Repeated empty review states create the feeling of an unused marketplace. The UI should hide absence gracefully and foreground registry proof, service area, or response quality instead. |
| `.nldc-cls` | Minor | Classification/service details are compact gray text. | Important contractor classification data is present but low-hierarchy and hard to scan. |
| `.nldc-reg` | Minor | Registry authority appears in a tiny repeated footer line. | It should become a designed trust chip or verified credential, not a footnote. |
| `.nldc` | Major | The card lacks a portfolio thumbnail, service proof, or premium identity surface. | A pro directory must answer â€œwhy trust this person?â€ in one scan. The current card mostly answers â€œwhat type is this row?â€ |

## Surface 3: Single Project Page

Audited live example: `https://nad-lan.co.il/projects/rainbow-tel-aviv/`

The Rainbow article body is strong and long-form, but the profile shell around it is still the old template. This is expected because the design upgrade has not been implemented.

| Element / class | Severity | Failure | Why it matters |
| --- | --- | --- | --- |
| `.nlpf-banner` | Blocker | The hero banner is an empty gradient strip. | A flagship project page should open with project media: render, skyline context, location, or gallery. Empty gradient is generic and cheap. |
| `.nlpf-av` | Blocker | The project identity uses the `ðŸ¢` emoji at 42px. | This breaks the â€œworld-class listingâ€ promise immediately above a multi-million-shekel project. |
| `.nlpf-pill` | Major | Category/status is a pill next to the title. | The pill competes with the name instead of supporting a refined fact strip. |
| `.nlpf-reg` | Major | The registry chip says `×ž××’×¨ ×”×ª×—×“×©×•×ª ×¢×™×¨×•× ×™×ª Â· data.gov.il`. | For an editorial showcase, trust should be clearer: official source, developer, permit/status caveat, and last verified date. |
| `.nlpremier` | Minor | The Premier indicator is a small text badge above the profile. | Premium status is not integrated into the visual system. It says â€œPremierâ€ without looking premier. |
| `.nlcard-facts` | Major | Facts are rendered as a basic table/module below the article flow. | High-value project facts should be a designed, scannable fact deck near the hero and repeated before CTAs. |

Notes:

- The project currently has no uploaded gallery images in the shell because the generated Rainbow media was handed off for Claude to upload separately.
- The long article is premium content, but the visible listing chrome remains current-system.

## Surface 4: Single Professional Page

Audited live example: `https://nad-lan.co.il/professionals/×’×‘××™-×ž×™×›××œ-2/`

The professional profile has trust data and CTAs, but its presentation feels like a generated stub.

| Element / class | Severity | Failure | Why it matters |
| --- | --- | --- | --- |
| `.nlpf-banner` | Blocker | The profile opens with the same empty gradient banner. | A professional page needs identity: logo, headshot, work photo, service-area visual, or strong verified credential panel. |
| `.nlpf-av` | Blocker | The profile identity is an emoji, for example `ðŸ—ï¸`. | This is the clearest â€œcheap templateâ€ signal on the page. |
| `.nlpf-norate` | Major | Empty review copy says `×˜×¨× ×”×ª×§×‘×œ×• ×—×•×•×ª ×“×¢×ª â€” ×”×™×• ×”×¨××©×•× ×™×`. | A public professional page should not lead with marketplace emptiness. Hide or soften until there is a review base. |
| `.nlpf-call`, `.nlpf-quote` | Major | CTAs are generic buttons with a phone emoji and gradient fill. | Premium profiles need proof-first CTA architecture: verified, response expectation, service match, and contact confidence. |
| `.nlcard-claim` | Major | The claim form appears in the public profile flow. | Ownership/claim UX can be valuable, but on a premium profile it should not feel like an admin stub embedded in the buyer experience. |
| `.nlrev` | Minor | The review module is visible before there is enough profile proof. | Empty review UI should not be a dominant public feature until the profile has portfolio, proof, and service detail. |

## Sponsored Spot Audit

Implementation found in `plugins/nadlan-config/inc/sponsored-spot.php`.

| Element / class | Severity | Failure | Why it matters |
| --- | --- | --- | --- |
| `.nldc-sponsored-spot` | Blocker | The available sponsored slot renders as a dashed box with light gradient background. | It looks like a printout or placeholder, not a valuable advertising product. |
| `.nldc-sponsor` inside sponsored spot | Major | The label `×ž×§×•×“× Â· ×¤× ×•×™` is centered, but the slot has no premium preview of the value being sold. | The monetization surface should sell exposure with confidence: placement, estimated reach, package name, and a refined CTA. |
| Inline sponsored styles | Minor | The sponsored card has inline presentation styling. | It makes the state harder to evolve consistently with the card system and premium design tokens. |

## Cross-Surface Root Causes

- Media is missing from the primary card and hero systems.
- Emoji icons act as identity. This is the strongest non-premium signal.
- The palette leans on bright blue/pink/gold pills instead of a restrained real-estate palette.
- Premium state is a badge, not a full hierarchy change.
- Empty states are too visible and too literal.
- Registry trust is technically present but visually low-value.
- The card system is data-first, not image-first.
- The single profile shell does not match the long-form editorial ambition of the Rainbow content.

## What I Could Not Do And Why

- I did not generate replacement screenshots because the requested deliverable is audit/spec only, not visual mockups.
- I did not edit `inc/*.php`, CSS, route registration, plugin version, or live content. This PR must stay docs-only.
