# Premium Catalog Design Standard

Use this skill when auditing or specifying a marketplace/catalog/listing/profile experience that must feel first-class, expensive, and trustworthy.

## Standard

A premium catalog does not start with icons. It starts with evidence:

- real photography, licensed imagery, generated illustrative media, logos, or strong monograms
- clear identity and location
- high-value facts above low-value labels
- trust proof that is designed, not dumped
- quiet controls that help the user decide
- mobile layouts that never ask the user to pinch, guess, or fight the page

## Before-State Audit Checklist

Check every catalog and single profile surface for:

- Image-first quality: Are cards led by real or tasteful generated media, or by emoji/icons?
- Hierarchy: Can a user read name, location, primary fact, status, and action in one scan?
- Premium state: Does paid/editorial premium materially change the card, or only add a badge?
- Empty states: Are missing reviews/photos/claims hidden gracefully, or advertised as absence?
- Trust proof: Are license, registry, verification, reviews, and source dates legible and credible?
- Controls: Are filters practical search tools, or decorative pills?
- Mobile: Are there 44px tap targets, no horizontal overflow, and no text under 14px?
- RTL: Are gutters, arrows, badges, and sticky elements correctly aligned for Hebrew?

## Premium Patterns

Cards:

- Use a 4:3 or 16:10 media block.
- Keep radius at 6-8px unless the local design system says otherwise.
- Use a neutral surface, thin border, and disciplined shadow.
- Keep facts to two or three lines.
- Make sponsored cards better, not louder.

Profiles:

- Project profiles need media, project name, city/neighborhood, developer, status, fact strip, source/verification, and CTA before long copy.
- Professional profiles need identity, specialty, service area, proof, portfolio/reviews where available, and CTA before claim/admin prompts.

Generated fallbacks:

- Prefer generated architectural context, monograms, or category illustrations.
- Do not use emoji as identity.
- Do not fake real project photography.
- Caption or mark generated/illustrative assets when users could mistake them for real renders.

Controls:

- Use search, filters, sort, and active chips.
- Avoid glassy pill clouds.
- Mobile filters should be a bottom sheet or compact drawer.

## Anti-Patterns

- Emoji avatars for serious real estate, legal, mortgage, contractor, or developer entities.
- Bright pink/blue category pills as the dominant visual language.
- Empty gradient hero bands.
- Sponsored cards that look like placeholder printouts.
- Review-empty copy repeated across many cards.
- Registry proof hidden as tiny footer text.
- Tables or cards that widen the page on a 390px phone.

## Source Lessons To Reuse

- Zillow Showcase: premium listing means richer media and interaction, not a small label.
- Compass: cards should lead with image, price/facts, address, and status.
- The Modern House: editorial restraint can make listings feel curated and valuable.
- Sothebyâ€™s International Realty: luxury listings sell lifestyle, setting, scale, and amenities.
- LoopNet: professional catalogs need serious filters, market trust, and business-grade density.
- Houzz: professional profiles must foreground proof: reviews, license, awards, portfolio.
- Madlan: Israeli project pages need concrete facts: units, floors, developer, stage, architect.
- realestate.com.au and Idealista: search, filters, valuation, saved searches, and owner/pro tools should feel like one product system.

## Delivery Rule

If implementation requires a new public URL, a new route, or a plugin module change, stop and get Claude/owner sign-off first. Research, audit, specs, and docs are safe. Public routes and plugin code are not safe without review.

