# Nadlan Platform Master Handoff
*The comprehensive technical, architectural, and design specification for the platform.*

## 1. Platform Vision
Nadlan is a premium real estate platform that seamlessly blends dynamic design with a high-conversion user journey. The platform combines:
- **Project Showrooms:** Immersive, 3D-driven landing pages (Ashira, Duo, Bialik) for high-ticket developments.
- **Professional Directory:** A trusted, sleek network for real estate agents, lawyers, and architects.
- **Content Hub & Magazine:** A high-SEO glossary and guide section for foreign and local investors.
- **Tools:** Integrated financial calculators (Purchase Tax, Mortgage) to capture bottom-of-funnel leads.

## 2. Core Audit Findings
Prior to this handoff, a rigorous E2E audit was conducted.
The key findings that must be addressed by any new contractor:
- **Technical SEO:** LTR/RTL misalignments in English articles, missing font assets (`Fraunces`, `Inter Tight`), and Mapbox instantiation warnings.
- **Design System:** Inconsistent use of the design tokens (e.g., `--cream`, `--ink`, `--gold`). Missing typographic hierarchy causing fallback fonts to render.
- **Architecture:** The current plugin-based "emergency hacking" (e.g., `nadlan-config`) creates JS race conditions (specifically in `calculators.php`).
- **User Experience:** The buyer journey is fragmented. Popups (like the contact plus icon) are intrusive.

**Read the full reports here:**
- [E2E Platform Design & UX Audit](docs/reports/e2e_platform_design_and_ux_audit.md)
- [Live Site Analysis](docs/reports/live_site_analysis.md)
- [Architecture & Design Flow](docs/reports/architecture_and_design_flow.md)

## 3. The New Draft Mockups
To provide a concrete, pixel-perfect blueprint, we have deployed realistic HTML/CSS mockups directly into WordPress as **Draft Pages**. These mockups do not interfere with the live site but demonstrate exactly how the final pages should look and feel within the WordPress container.

**Draft Mockups Created (Check WP Admin -> Pages (Drafts)):**
1. **Mockup: Homepage:** A combination of premium aesthetics, minus any "Compass" influence.
2. **Mockup: Listing Standard:** Clean, high-conversion property layout.
3. **Mockup: Listing Premium (3D):** The Sketch-first facade layout for projects like Ashira.
4. **Mockup: Projects Catalog Map:** Split-screen map and list layout.
5. **Mockup: Professional Directory:** A clean grid of verified professionals.
6. **Mockup: Professional Profile:** Role-specific profile designs (e.g., architect blueprint motifs).
7. **Mockup: Glossary Hub:** SEO-optimized dictionary landing page.
8. **Mockup: Magazine Article:** Properly formatted LTR English guide.
9. **Mockup: Purchase Tax Calculator:** Fixed JS race conditions with a clean UI.
10. **Mockup: Contact / Lead Funnel:** Removing intrusive popups for a sleek slide-out.

*(And 10 additional mobile-responsive views)*

## 4. Development Workflow & Scripts
All mockups are generated from raw HTML/CSS stored in `draft-mockups/`.
To deploy or update mockups to WordPress Drafts:
```bash
wp eval-file scripts/deploy_drafts.php
```

## 5. Contractor Directives
- **Zero "Compass" clones.** The design must be unique, utilizing our defined tokens.
- **Fix the JS Race Conditions.** `nadlan-config/inc/calculators.php` must be refactored to wait for `window.NADLAN_PTAX`.
- **Implement the Typography.** Add the `@font-face` rules for `Fraunces` and `Inter Tight` to `style.css`.
- **Content:** Refer to the Claude SEO Hitlist in the skills folder. All English content must be wrapped in `.article-en-ltr`.
