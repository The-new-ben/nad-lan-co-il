# Home live QA: project-first positioning

Date: 2026-06-24

Live URL tested: `https://nad-lan.co.il/?codex_qa=home_project_first_after_rail`

Related commits:

- `4516d0a` theme: make home project-first
- `35d3577` theme: keep home contact rail off search

## What changed

The active WordPress theme front page now positions NadLan around project discovery, apartment choice, and investor-ready project presentation.

Primary live headline:

`נדל״ן חכם: בוחרים פרויקט ודירה לפני שפונים ליזם`

The primary CTA now points to the Rainbow project showroom:

`https://nad-lan.co.il/projects/rainbow-tel-aviv/`

The previous generic directory/tools positioning was removed from the active front-page copy.

## Screenshots saved

- `desktop-1440.png`
- `mobile-390.png`

Machine-readable reports:

- `desktop-1440.json`
- `mobile-390.json`
- `home-live-report.json`

## Checks performed

- Desktop 1440 screenshot captured after UPress theme pull.
- Mobile 390 screenshot captured after UPress theme pull.
- Automated horizontal overflow check passed at both sizes.
- Automated public-language scan found no forbidden visible terms.
- Desktop floating contact rail no longer covers the hero search row after the second fix.
- Mobile hero, CTAs, project cards, tools, professional cards, footer, and bottom contact rail were visually inspected.

## Results

Desktop 1440:

- `horizontalOverflow: 0`
- `forbiddenPublicText: []`

Mobile 390:

- `horizontalOverflow: 0`
- `forbiddenPublicText: []`

## Honest limitations

- This slice changed the active Home positioning, title, meta description, CTA path, and the floating rail behavior. It was not a full Home visual rebuild.
- The Home hero still uses the existing dark coastal visual treatment. A future design slice should decide whether to replace the first viewport with the full Lovable cream editorial direction.
- Some project images are existing site assets. This QA does not claim that every project image is an official contractor asset.
- Legacy directory and listing modules still contain older class names and language outside this Home slice. Cleaning those safely requires a separate plugin release and screenshot pass.
