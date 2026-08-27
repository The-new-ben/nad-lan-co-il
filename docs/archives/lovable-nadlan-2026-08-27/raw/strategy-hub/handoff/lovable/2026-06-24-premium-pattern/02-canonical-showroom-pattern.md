# 02 Canonical Showroom Pattern

## Product sentence

Pick a project, select an apartment, understand the apartment, ask for details.

Everything in the showroom must support that sentence.

## Chosen apartment selection path

Decision: C, Hybrid.

### Why not A only

Authored apartment cells are practical now, but they are not the full premium promise forever. If the product stops there, contractors will keep asking why every window cannot be selected.

### Why not B now

Requiring exact geometry now blocks implementation until each contractor supplies perfect assets. That would stop sales and stop demos.

### Why C wins

Hybrid lets NadLan3D ship now with honest authored apartment selection, while the contractor asset contract defines the upgrade path to exact apartment geometry later.

## Buyer-facing behavior

The buyer sees:

1. Project title and location.
2. Building view.
3. Available apartments on the building and in the unit rail.
4. Selected apartment panel.
5. Facts: floor, rooms, area, balcony, direction, status.
6. Plan or dignified missing-plan state.
7. Inquiry actions.

The buyer does not see technical explanations.

## Showroom layout, desktop

Canvas target: 1440px wide.

- Page max width: 1240px.
- Outer gutter: 40px.
- Header height: 76px.
- Hero heading block: 36px top, 24px bottom.
- Main grid: left stage 1fr, right panel 360px.
- Grid gap: 18px.
- Stage minimum height: 642px.
- Selected panel appears in the right column, below the unit rail.
- Inquiry strip appears below the grid.

## Showroom layout, mobile 390

Canvas target: 390px wide.

- Outer gutter: 20px.
- Header height: 64px.
- Only brand and language chip remain visible in header.
- H1 size: 36px.
- Stage minimum height: 466px.
- Main grid becomes one column.
- Unit cards become horizontal scroll rail.
- Each unit card min width: 236px.
- Selected panel sits below the rail.
- Buttons become full width.
- No fixed bottom dock until footer overlap is solved.

## State 1: real building model available

Use this when the project has a real loaded building asset and selected unit coordinates are authored.

Public label:

- HE: מבט בניין פעיל
- EN: Building view active

Do not say the file format.

## State 2: facade fallback available

Use this when the project has a high-quality facade render or traced elevation, but no real model.

Public label:

- HE: חזית הפרויקט
- EN: Project facade

The apartment selection still works through authored cells or polygons.

## State 3: missing asset

Use this when the contractor has not delivered a building image, facade, or model.

Public label:

- HE: ממתינים לחומר חזותי מהיזם
- EN: Awaiting project visuals

The page still shows project facts and inquiry path. It must not show a fake building.

## Selected apartment panel

Required content:

- Label: selected apartment.
- Apartment title.
- Short description.
- Facts grid.
- Plan area or missing-plan state.
- Primary action.
- WhatsApp action.

Hebrew example:

```html
<section class="nl3d-selected-panel nl3d-card">
  <span class="nl3d-chip">הדירה שנבחרה</span>
  <h2 class="nl3d-h2">דירה 16, קו מערבי</h2>
  <p>דירת 4 חדרים עם מרפסת מערבית. המחיר והזמינות יאומתו מול נציג הפרויקט לפני התקדמות.</p>
</section>
```

## Contractor asset requirements

Now:

- Project name.
- City.
- Developer.
- Hero render or facade photo.
- Units data.
- Inquiry destination.

Premium later:

- Segmented apartment geometry with stable apartment IDs.
- Official floor plans.
- View images or panoramas.
- Updated status feed.

## What Codex builds now

Codex keeps the 1.69.32 input behavior and replaces the presentation:

- New wrapper classes.
- New stage styling.
- New unit rail.
- New selected panel.
- New mobile 390 layout.
- New public copy.

## What is not claimed publicly

- Exact independent picking for every window.
- Technical model source.
- Internal proof mechanics.
- Internal ranking or sales operations.

## Upgrade later

When exact apartment geometry arrives, Codex changes only the selection resolver. The UI remains unchanged. Buyer copy remains unchanged.

