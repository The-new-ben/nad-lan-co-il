# 2026 Listing + Profile Visual Asset Spec

Date: 2026-06-03
Scope: Nadlan listing cards, project cards, professional profile cards, single profile/project pages, and generated fallback assets for advertisers who do not yet have premium photography.

## Executive Standard

The "million-dollar look" is not decoration. It is a system: strong primary media, restrained typography, clear proof badges, consistent aspect ratios, and no empty gray boxes. Nadlan should make every paid advertiser feel they bought a real publishing asset, not a database row with a payment button.

The strongest benchmark pattern is clear:

- Zillow Showcase pushes immersive, media-led listings: interactive floor plans, high-resolution scrolling media, AI-selected hero images, room-by-room organization, and performance lifts reported by Zillow.
- Houzz wins through portfolio depth: project photos, professional profile completeness, reviews, keywords, and service-area clarity.
- LoopNet/CoStar sells premium visibility as a media package: ranking, logos/headshots in search, aerial/architectural photography, Matterport, video, drone, retargeting, and reporting.
- Madlan's developer area uses project/developer imagery as identity. Local Israeli users expect project cards to feel like brand assets, not admin records.

## Sources

- Zillow: immersive Showcase listings with high-resolution scrolling hero images, room-by-room organization, interactive floor plans, AI hero/photo organization, and reported saves/pending-sale lift: https://www.zillow.com/agents/new-immersive-listing-experience/
- Zillow: 3D tours, AI-generated interactive floor plans, and listing-media syndication with Realtor.com: https://www.zillow.com/news/new-zillow-and-realtor-com-agreement-expands-access-to-interactive-listing-media/
- Zillow: Showcase facts and benchmark engagement metrics for premium listings: https://www.zillow.com/agents/showcase-facts/
- Houzz Pro: uploading project photos, professional photography, lighting, composition, descriptions, keywords, and location context: https://www.houzz.com/pro-learn/blog/houzz-to-upload-project-photos-to-your-houzz-profile
- Houzz: professional-profile photos, 1,000px+ image guidance, copyright warning, and project organization: https://www.houzz.com/magazine/professional-photos-on-houzz-stsetivw-vs~1857398
- Houzz Pro: photo keywords and relevance rules: https://pro.houzz.com/pro-help/r/guidelines-for-good-photo-keywords
- LoopNet solutions: priority ranking, search branding, listing reports, architectural/aerial photography, Matterport, video, drone, email/newsletter, and retargeting packages: https://www.loopnet.com/solutions/
- Matterport real estate: virtual tours, floor plans, room dimensions, AI-powered descriptions and property intelligence: https://matterport.com/industries/real-estate
- Madlan developers index, local benchmark for developer/project card identity: https://www.madlan.co.il/developers

## Visual Product Model

Nadlan has four public entity surfaces that should share one visual grammar:

1. Professional card
   Purpose: trust and fast contact.
   Primary asset: face/logo/category avatar.
   Proof: license/registry, city, rating/reviews, verified claim, tier.
   CTA: view profile, request quote, claim/upgrade.

2. Project card
   Purpose: brand desire and lead capture.
   Primary asset: rendering/photo/hero illustration.
   Proof: project type, city, developer, status, units, verified source.
   CTA: view project, request details, advertise project.

3. Property card
   Purpose: inspection and action.
   Primary asset: real property image.
   Proof: price, rooms, sqm, city, map, days/live status, promoted badge.
   CTA: view property, contact, save/compare.

4. Empty/fallback advertiser card
   Purpose: avoid looking broken while asking for media.
   Primary asset: generated SVG/gradient/category illustration, never a fake building photo.
   Proof: "missing photos" checklist, type badge, verified source if true.
   CTA: upload photos in Studio, claim card, complete setup.

## Card Layout Spec

### Professional Directory Card

- Container: 8px radius, 1px neutral border, white/off-white background, minimal shadow only on hover.
- Grid: desktop min width 260px; mobile full width.
- Top media row: 1:1 avatar/logo block, 72-96px on desktop, 64px mobile.
- Header: title, profession, city. Do not let imported legal/company names overflow; clamp to 2 lines.
- Proof row: verified badge, registry/source badge, rating/reviews if real.
- Contact row: phone/email/website only when tier allows; otherwise gated CTA.
- CTA: one primary action. Secondary actions are text links.

### Project Directory Card

- Container: 8px radius, 1px border, image-first.
- Image aspect ratio: 16:9 for cards; allow 2:1 for wide premium/sponsored placement.
- Image behavior: `object-fit: cover`, center focal point unless admin sets focal metadata.
- Top overlay: project type pill, paid tier badge, sponsored disclosure if paid placement.
- Content: project name, city/neighborhood, developer, status, units range.
- CTA: view project / request details.
- Missing media: use project-type illustration, not a blank placeholder.

### Property Card

- Image aspect ratio: 4:3 or 16:10. Property buyers inspect, so avoid overly cinematic crops.
- Price line: largest text after title; use consistent ILS formatting.
- Facts: rooms, sqm, floor, city. Use compact chips or a single facts row.
- Trust: promoted badge, verified-owner badge, map pin, date/status.
- Actions: view, compare/save, contact.

### Single Profile / Project Page

- Hero area: media-led, above the fold, with clear title and CTA visible without scrolling.
- Desktop hero media: 16:9 or full-width 2:1.
- Mobile hero media: 4:5 or 1:1 crop fallback to preserve the subject.
- Primary CTA remains sticky only if it does not cover content; no intrusive bottom bars.
- Side facts panel: status, city, type, proof badges, paid tier, campaign badge where relevant.
- Gallery: consistent 16:9 thumbnails; floorplan and 3D tour have explicit badges.

## Type Scale

Use stable sizes; do not scale font size with viewport width.

- Page H1: 44-56px desktop, 32-36px mobile, 1.08-1.15 line-height.
- Section H2: 30-36px desktop, 24-28px mobile.
- Card title: 18-21px desktop, 17-19px mobile.
- Card facts/body: 13.5-15px.
- Badge text: 11-12px, uppercase only for Latin technical labels. Hebrew badges stay natural.
- CTA text: 14-15px, 700-800 weight.

Typeface guidance:

- Hebrew UI/body: Heebo or the existing site sans.
- Premium display: Frank Ruhl Libre only for true page headings or project/profile hero titles.
- Do not use display-size type inside cards.

## Image Ratios + Asset Sizes

Store and request media in predictable ratios so cards stop jumping.

| Surface | Ratio | Minimum source | Preferred exported size |
|---|---:|---:|---:|
| Project/page hero | 2:1 or 16:9 | 1600px wide | 1536x768 or 1600x900 WebP |
| Project card | 16:9 | 1200px wide | 1200x675 WebP |
| Property card | 4:3 or 16:10 | 1000px wide | 1000x750 or 1200x750 WebP |
| Gallery thumb | 16:9 | 900px wide | 900x506 WebP |
| Professional avatar/logo | 1:1 | 512px | 512x512 WebP/PNG |
| Default SVG placeholder | any vector | n/a | inline SVG or cached SVG file |

Never stretch media. Crop deliberately, preserve faces/logos/buildings, and add focal-position metadata later if needed.

## Badge System

Badges must answer "why should I trust this?" or "what did the advertiser buy?"

Core badges:

- Verified by Nadlan: identity/license/business checked.
- Government source: imported from official registry/source.
- Claimed: owner controls this card.
- Pro / Premier: paid tier.
- Sponsored / ממומן: paid editorial or sponsored placement. Required disclosure.
- New: recently added, limited to 30 days.
- Has photos: only when a real gallery exists.
- 3D tour / Floorplan / Video: specific media capabilities.
- Lead response: only after real response-time tracking exists.

Badge design:

- 6px radius or pill when short.
- 11-12px text, 5-8px vertical padding.
- Maximum 3 visible badges on a card. Move extras into detail pages.
- Do not stack badges over faces/logos. On project media, top-right overlay is acceptable with a subtle scrim.

## Empty-State Treatments

Empty states are conversion moments. They should not look like missing data.

Professional without image:

- Generated avatar with initials + profession icon.
- Soft category gradient using profession color.
- Text: "העלו לוגו או תמונה כדי לשפר אמון".
- CTA in Studio: upload logo/photo.

Project without image:

- SVG illustration by project type: urban renewal, new build, Tama 38, commercial.
- City/neighborhood line remains visible.
- Label: "הדמיית ברירת מחדל - לא תמונת הפרויקט".
- CTA: upload renderings/photos.

Property without image:

- Neutral property placeholder with map/city motif.
- Do not generate fake interiors/exteriors for a real property.
- CTA: upload at least 5 real photos.

Gallery empty:

- Checklist state: hero image, 5 gallery photos, floorplan, map pin, video/3D tour.
- Show progress, not shame.

## Generated-Asset Plan

This plan is for advertisers who have no photos yet. It keeps the product premium without inventing fake evidence.

### 1. Deterministic SVG Placeholders

Use generated SVGs for category/project-type placeholders:

- Profession icons: lawyer, appraiser, contractor, mortgage advisor, broker, architect, inspector.
- Project icons: urban renewal towers, crane/new build, Tama 38 facade, neighborhood map, residential blocks.
- Property icons: apartment building, house, map pin, floorplan grid.

Implementation note for Claude later:

- SVG should be deterministic from post type + category/profession + city hash, so repeated cards feel consistent.
- Inline SVG or cached generated file is cheaper than AI images and safe for licensing.
- Never use a generated "real-looking" building as if it were the actual advertised project.

### 2. CSS Hero Gradients

Use CSS gradients for hero backgrounds when no media exists:

- Base: deep green/ink + muted gold accent.
- Add subtle map-grid/topographic pattern as SVG mask.
- Project type changes accent color, not the whole palette.
- Keep contrast high enough for white Hebrew headline text.

### 3. Default Avatars

For professionals:

- Initials from title/company name.
- Profession icon in the corner.
- Verified/registry badges remain separate from the avatar.
- If a company logo exists later, logo replaces avatar automatically.

Do not generate fake human portraits. Fake faces reduce trust and can create legal/identity problems.

### 4. AI-Generated Illustrations

Allowed:

- Abstract category illustrations.
- Generic city/map motifs.
- Non-photoreal editorial headers for guides.

Not allowed:

- Fake renderings of a specific real project.
- Fake property interiors/exteriors.
- Fake portraits or logos.
- Any generated image that could be mistaken for a real asset supplied by the advertiser.

### 5. Upload Prompt for Advertisers

Studio should eventually ask for:

- 1 hero image/rendering.
- 5-12 gallery images.
- Logo/avatar.
- Floorplan PDF/image when relevant.
- Video or 3D tour URL if relevant.
- Alt text/caption for each uploaded image.

## Premium-Feel Checklist

A card or profile is not premium until all of this is true:

- Image ratio is stable and no layout shift occurs on load.
- No text overlaps media or escapes cards on mobile.
- The first visual is either real media or a clearly labeled illustration.
- The title, city, type, proof, and CTA are scannable in under 3 seconds.
- Badges are limited and meaningful.
- Paid tier is visible but not louder than the entity name.
- Missing media prompts are helpful and specific.
- CTAs are consistent: primary action uses one style, secondary links are quieter.
- Sponsored/paid placements are disclosed.
- The card can be understood without relying on color alone.
- The visual system is not one-note beige/green; use restrained accent variety by entity type.

## QA Charters for Implementation

When Claude implements this spec, QA should inspect:

1. Professional card with real logo/photo.
2. Professional card with no image.
3. Project card with rendering.
4. Project card with no media.
5. Property card with photo gallery.
6. Property card with no media.
7. Paid Pro and Premier card states.
8. Sponsored card disclosure.
9. Mobile 390px card grid.
10. Single project profile above the fold.

Pass bar:

- No empty gray boxes.
- No stretched or distorted media.
- No badge clutter.
- No text overflow on 390px mobile.
- Every missing-asset state tells the advertiser what to upload next.

## Implementation Boundaries

This document is a design/asset spec only. It does not authorize new public URLs, public pages, plugin modules, or route changes. Per the standing rule, public URL/page/module changes need Claude + owner sign-off before code work.
