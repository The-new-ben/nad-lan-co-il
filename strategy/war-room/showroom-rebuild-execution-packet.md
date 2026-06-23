# Showroom Rebuild Execution Packet

Date: 2026-06-23

Purpose: turn the existing showroom research, Lovable prototype, and live screenshots into a build-ready packet for the next NadLan project showroom slice.

## Current Evidence Read

- Live Dimri public page has real page depth and commercial structure, but the showroom is too heavy and not yet a focused premium sales experience.
- Lovable prototype after public-language cleanup proves the state-machine idea and mobile drawer discipline, but it is not contractor-ready because the visual assets are still schematic and the brand signal is weak.
- Existing strategy files already define the core rule: no silent fallback, no fake facade, no dead buttons, no stacking.

## Product Decision

The next showroom build should not polish the current stacked experience. It should rebuild the project showroom as a strict asset-truth product:

1. Official model or official facade exists: show it as the primary buyer surface.
2. Approved concept exists: show it as concept only, not as finished project proof.
3. No approved visual asset exists: show a premium missing-asset state and a contractor upload checklist.
4. Broken model, broken map, or broken tour: show a clean unavailable state and log it. Do not resurrect old schematic facades.

## Public Language Rules

Public Hebrew should use:

- סיור בפרויקט
- בחירת דירה
- תכנון הדירה
- נוף וסביבה
- סיור פנים
- בדיקת רכישה
- המודל ממתין להעלאה
- הדמיה רשמית
- הדמיית קונספט

Public UI should not expose:

- file formats
- internal ranking labels
- font names
- implementation terms
- prompt wording
- unsupported claims that a model, price, availability, or view is official

## Target Screen Order

Desktop:

1. Project identity strip.
2. Large visual stage.
3. Side unit list or compact unit selector.
4. Selected unit card docked beside or below the stage.
5. Unit tabs: plan, view, interior, costs, contact.
6. Long SEO body, tables, FAQ, and related pages below.

Mobile 390:

1. Project identity.
2. Visual stage with stable height.
3. Unit selector.
4. Selected unit bottom sheet.
5. Tabs become stacked or scroll-safe.
6. Sticky CTA must not cover footer, stage, or selected unit.

## Build Backlog

Use `showroom-rebuild-execution-packet.csv` as the implementation queue. The highest-risk first slices are:

- SR-001 asset truth
- SR-003 visual stage
- SR-004 unit selector
- SR-008 lead capture
- SR-010 public language

## Screenshot Gates

Every implementation PR must save screenshots for:

- desktop 1440 first viewport
- mobile 390 first viewport
- selected unit open on mobile
- missing asset state
- broken model state
- map unavailable state
- footer with sticky CTA visible

## External Product References

- Zillow 3D Home: virtual tours and interactive floor plans as listing assets.
- Zillow Showcase: premium listing treatment and elevated presentation for sellers.
- Zillow SkyTour: exterior angle, elevation, and surrounding context.
- Matterport: 3D tours, floor plans, photos, and property marketing assets.
- Homes.com Matterport: digital twin plus floor-plan touring.
- JamesEdition: curated international luxury real estate pattern.

