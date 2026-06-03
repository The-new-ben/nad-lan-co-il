# Listing Visual Asset Standard

Use this when designing, auditing, or specifying cards and profile visuals for Nadlan listings, projects, professionals, properties, or advertiser assets.

## Safe Lane Rule

Research, specs, audits, QA reports, and documentation are green-light work.

Do not create new public routes/pages or edit existing plugin modules without Claude + owner sign-off on:

- the canonical URL,
- the module owner,
- whether an existing page should be expanded instead,
- and whether the change collides with `skills/url-namespace-contract.md`.

Plugin code goes through Claude review. Visual/design specs can proceed as docs.

## Core Principle

Premium real-estate UI is media-led, trust-led, and measurement-led.

Every card should answer:

1. What is this?
2. Where is it?
3. Why should I trust it?
4. What action can I take?
5. What is missing, if the advertiser has not completed setup?

## Required Surfaces

- Professional card.
- Project card.
- Property card.
- Sponsored/paid variant.
- Empty/no-media variant.
- Single project/profile hero.
- Studio upload prompt state.

## Visual Requirements

- Fixed media aspect ratios. No layout shift.
- 8px card radius unless the design system says otherwise.
- One primary CTA per card.
- Maximum 3 visible badges per card.
- Real media is always preferred over generated visuals.
- Generated visuals must be clearly generic; never fake a real property, project, face, or logo.
- Missing media should trigger a helpful checklist, not a broken-looking placeholder.

## Ratios

- Project/page hero: 2:1 or 16:9.
- Project card: 16:9.
- Property card: 4:3 or 16:10.
- Gallery thumbnails: 16:9.
- Professional avatar/logo: 1:1.

## Badge System

Allowed badges:

- Verified by Nadlan.
- Government source.
- Claimed.
- Pro.
- Premier.
- Sponsored / ממומן.
- New.
- 3D tour.
- Floorplan.
- Video.

Badges must represent a real state. Do not use decorative badges.

## Generated Asset Policy

Allowed:

- Deterministic SVG category illustrations.
- CSS hero gradients with map/topographic motifs.
- Initials-based avatars.
- Generic profession/project icons.

Not allowed:

- Fake building renderings for a real project.
- Fake property interiors/exteriors.
- Fake human portraits.
- Fake logos.
- Any generated asset that looks like advertiser-supplied evidence.

## QA Pass Bar

Before implementation is accepted:

- Check desktop and 390px mobile.
- Verify no text overflow.
- Verify no image stretching.
- Verify all empty states show upload guidance.
- Verify sponsored/paid surfaces disclose paid status.
- Verify cards remain scannable in under 3 seconds.
- Verify the design does not become one-note beige, green, or dark-blue.

## Reference Doc

Full Nadlan spec:

`docs/2026-06-03-listing-profile-visual-asset-spec.md`
