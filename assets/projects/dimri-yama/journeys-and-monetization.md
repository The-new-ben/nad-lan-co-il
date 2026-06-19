# Dimri Yama Journeys And Monetization

Status: internal planning, not public copy.

## Audience

Public page users:

- Israeli buyers comparing new projects.
- Families considering Sde Dov.
- Investors looking for district context, risk and price logic.
- Foreign buyers who need English/French/Russian/Arabic entry points later.

Not public users:

- internal agents,
- plugin developers,
- SEO operators,
- CRM operators,
- deployment operators.

Do not leak internal words to the public page.

## Buyer Journey

1. Arrives from search, project directory or a shared link.
2. Sees a short project-specific intro, not generic marketing.
3. Sees the 3D context model: compound, sea, Yarkon direction, sun/orientation.
4. Uses the facade picker beside the model to choose an apartment cell.
5. Reads apartment facts: building, floor, rooms, sqm, balcony, view, status and price wording.
6. Opens the floor plan, interior tour, view-from-apartment or gallery when available.
7. Contacts the project with the selected unit attached.
8. Can dismiss the card and choose another unit.

## Contractor / Developer Journey

1. Pays for a project showroom setup.
2. Provides official BIM/render/floor plans/inventory when available.
3. Gets a premium page with model, facade picker, content, media and contact flow.
4. Can update availability, status, price wording and media without PHP.
5. Receives lead context: selected unit, floor, rooms, view and user message.
6. Reviews interest signals by unit later.

## Site Owner / Operator Journey

1. Create project asset folder.
2. Fill source-notes, project meta, unit-map, drawings, environment and view-layer files.
3. Validate payload.
4. Upload or paste fields through WordPress admin.
5. Run screenshot QA.
6. Publish only after proof.
7. Reuse the runbook for the next project.

## Monetization

Initial product:

- setup fee for research, page, model/facade, media preparation and QA;
- monthly project showroom subscription;
- premium listing exposure in project directory;
- lead routing and selected-unit context.

Upsells:

- official BIM conversion;
- apartment-level model;
- Matterport/interior tour integration;
- multilingual investor package;
- lead analytics by unit;
- professional partner layer: mortgage, lawyer, interior design, finance;
- later reservation/payment workflow after legal/payment provider approval.

## CMS Requirements

Project-level fields:

- GLB URL;
- poster URL;
- facade/elevation URL or SVG;
- drawings JSON;
- environment JSON;
- video URL;
- tour URL;
- contractor contact/WhatsApp;
- price source note;
- language status.

Unit-level fields:

- building;
- floor;
- rooms;
- sqm;
- balcony;
- direction;
- view;
- status;
- price estimate or inquiry-only;
- plan URL;
- tour URL;
- cell polygon/points;
- model hotspot only if official apartment-level GLB exists.

