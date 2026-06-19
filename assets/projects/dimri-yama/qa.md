# Dimri Yama QA Checklist

Status: not yet implemented.

## Required Screenshots

- Desktop 1440px.
- Tablet 768px.
- Mobile 390px.
- Edge mobile user agent.

## Required Buyer Checks

- Intro is above the showroom.
- 3D model is visible, stable and horizontally locked.
- Facade picker sits beside or directly near the model.
- Apartment cells are embedded in the facade, not floating.
- Selected apartment card has dismiss button.
- Contact action carries selected unit context.

## Required Contractor Checks

- Project fields are findable in WordPress admin.
- Unit JSON/payload can be updated without PHP.
- Poster, GLB, facade, drawings and tour URLs are replaceable.

## Required External QA

- Chrome DevTools Device Mode.
- Lighthouse.
- PageSpeed Insights where useful.
- WAVE or equivalent accessibility scan.
- Schema validator if schema changes.

