# NadLan Platform Child 0.1.6 Self Review

Date: 2026-06-29

## What Improved

- The active child theme was replaced live through WordPress admin.
- Homepage now uses the new child header and footer.
- The existing homepage project showcase is visible and marked as `[data-nlpo-home-projects]`.
- Homepage has exactly one H1, no horizontal overflow, no visible internal-language leaks, and zero console errors in the QA pass.
- Ashira HE and EN still render the canonical showroom engine with `#nl-root = 1`, `.nlv2-showroom = 0`, and `.nlp3d = 0`.
- Calculator, professionals, guide, projects, homepage, and Ashira all returned HTTP 200 in desktop and mobile checks.

## Anti-Stack Statement

- No new homepage project band was appended.
- No new showroom shortcode was registered.
- The existing `.nlux-showcase` block is reused and marked at render time.
- The child theme does not rewrite `wp_posts.post_content`.
- The legacy Rainbow/Dimri `.nlp3d` renderer was not touched in this slice.

## What Still Needs Work

- `/projects/` and `/professionals/` still report two H1 elements.
- `/mortgage-calculator/` and `/buying-apartment/` report zero H1 elements.
- Ashira desktop has offscreen internal controls in the engine area, although the page itself does not horizontally overflow.
- Homepage language pages are not yet real HE/EN/FR/RU/AR equivalents in this slice.
- Ashira long-form multilingual content and full project-factory rebuild are not completed in this slice.
- Some homepage project cards still use dark/missing-looking thumbnails on mobile; this needs the asset-provenance/content pass.

## Ship Decision

Safe as a narrow child-theme chrome and homepage-marker slice. Not complete as the full premium multilingual project factory.
