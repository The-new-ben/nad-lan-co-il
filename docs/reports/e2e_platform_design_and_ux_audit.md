# NadLan: Platform Design, Front-End & UX Audit
**Commissioned by:** NadLan Executive Review Panel  
**Date of Audit:** July 8, 2026  
**Auditor Perspectives applied:** Real-Estate Product Designer (Compass/Zillow), Conversion/UX Researcher, Senior Frontend Engineer (WP/ThreeJS/Mapbox), Visual Brand Director, RTL/Localization Specialist, and Technical-SEO Strategist.

---

## 1. Executive Summary: Top 10 Major Deficiencies to Fix Before Investors

These 10 critical issues represent severe visual, financial, or functional breakages that must be resolved prior to showing the site to contractors and investors:

1. **[P0] Page-Load Race Condition in Purchase Tax Calculator:** The calculator's calculation script runs on load and crashes because the `window.NADLAN_PTAX` JSON variable is enqueued in the footer, throwing a fatal JS error that breaks all calculation and input-tab switching. (Severity: **P0**)
2. **[P0] Missing English Font Faces:** The serif `Fraunces` and sans-serif `Inter Tight` fonts are declared in variables and rules throughout the custom theme, but their `@font-face` definitions are missing from the CSS. They default to standard browser serif/sans, degrading LTR visual luxury. (Severity: **P0**)
3. **[P0] 404 Routing on English Projects Catalog:** Clicking the English language switcher on the projects archive routes the user to `/en/projects/`, which results in a fatal WordPress **404 Page Not Found** error. (Severity: **P0**)
4. **[P0] Rainbow Tel Aviv Flagship 3D Asset 404:** The raw 3D `.glb` file for the Rainbow Tel Aviv flagship project is fetched from a broken GitHub URL, throwing a 404 network error and rendering a generic error box. (Severity: **P0**)
5. **[P1] Generic "Twisting Tower" 3D Model on Listings:** Regular properties display a generic, spinnable 3D tower that has no resemblance to the actual listing. It confuses users, is styled with a raw grey loading container, and distracts from the bespoke facade sketch. (Severity: **P1**)
6. **[P1] Sun Modes Active State Button Bug:** On the flagship showroom, clicking "Dusk" or "Night" updates the lighting filter but fails to change the active state button UI. The "Day" button remains styled as "pressed" in the HTML. (Severity: **P1**)
7. **[P1] Low-Trust Gravatar Avatars for Professionals:** For listed professionals without a custom photo, the directory defaults to standard Gravatar grey shadows. This looks cheap, unvetted, and completely off-brand. (Severity: **P1**)
8. **[P1] Accessibility Violation in Mortgage Calculator:** The calculator includes 9 form fields without associated `<label>` tags or `id`/`name` attributes, triggering severe accessibility warnings and breaking browser autofill. (Severity: **P1**)
9. **[P1] Incorrect Tax Calculations on Purchase Tax Calculator:** For primary homes over 1.97M NIS, the calculator fails to compute tax on the remaining balance (e.g. 2.5M NIS displays 0 NIS tax). The investor tab fails to trigger recalculations. (Severity: **P1**)
10. **[P2] Mapbox Map Container is Polluted:** The 3D projects catalog throws console warnings because the Mapbox GL instance container div contains prior HTML elements, risking interactive event degradation. (Severity: **P2**)

---

## 2. Prioritized Master Table of Findings

| ID | Page/Surface | Section / Element | Severity | Heuristic / Principle | Why it Matters | Fix Direction (No Code) | File / Module | Competitor Ref | Effort |
|---|---|---|---|---|---|---|---|---|---|
| **01** | Calculators | Purchase Tax (`#nlptax`) | **P0** | Script Ordering (Race Condition) | Breaks calculator calculation and tab toggling on load. | Enqueue `window.NADLAN_PTAX` in `wp_head` instead of `wp_footer` (or load it synchronously before shortcode output). | `inc/calculators.php` | Zillow / NerdWallet | Ship-this-week |
| **02** | Global Styles | Typography (`style.css`) | **P0** | Brand Consistency & Hierarchy | Fallbacks look amateurish and break LTR visual identity. | Add missing `@font-face` rules for `Fraunces` and `Inter Tight` linking to theme woff2 assets. | `style.css` | Compass | Ship-this-week |
| **03** | Projects | English Catalog (`/en/projects/`) | **P0** | Routing / Information Architecture | Users switching to English hit an empty 404, causing high bounce rates. | Map `/en/projects/` rewrite rule to the `nadlan_project` archive loop in multi-language configurations. | `inc/project-page-assembly.php` | Airbnb | Ship-this-week |
| **04** | Flagship Page | Rainbow 3D Model | **P0** | Content Availability & Trust | Broken asset throws a 404 network error and breaks the 3D showcase promise. | Correct the raw GitHub asset URL or upload the `model.glb` to the UPress uploads directory. | `inc/showroom-engine.php` | Matterport / VTS | Ship-this-week |
| **05** | Regular Listing | 3D Theater (`.nlps-3d`) | **P1** | Truth in Advertising / Clarity | A generic twisting tower that is not the actual building degrades listing trust. | Demote/remove the twisting 3D viewer. Lead with the hand-drawn ink sketch and parametric SVG facade side-by-side. | `inc/property-showroom.php` | Compass | Ship-this-week |
| **06** | Project Showroom | Sun Mode Selector (`.nlps-3d__light`) | **P1** | Feedback of System State | User cannot tell which light mode is active; day button stays visually pressed. | Update JS handler to toggle the `aria-pressed` and active class across sibling buttons. | `inc/property-showroom.php` | 3D condo configurators | Ship-this-week |
| **07** | Professional Directory | Profile Avatars | **P1** | Trust and Brand Authority | Gravatar silhouettes look unvetted and cheap. | Replace default Gravatars with customized, elegant line-art sketch portrait avatars matched to roles. | `inc/pro-cards.php` | Zillow Premier Agent | Ship-this-week |
| **08** | Calculators | Mortgage Form Fields | **P1** | Accessibility (WCAG 2.1) & Scannability | Fails screen readers, keyboard navigation, and browser autofill. | Wrap inputs in `<label>` elements; map explicit `id`, `name`, and `autocomplete` attributes. | `inc/calculators.php` | Zillow | Ship-this-week |
| **09** | Calculators | Tax Calculation Logic | **P1** | Accuracy / Financial Integrity | Displaying incorrect tax values ruins financial credibility. | Align JavaScript calculation brackets with official 2026 Israel Tax Authority progressive rates. | `inc/calculators.php` | Israel Tax Authority | Ship-this-week |
| **10** | Projects Catalog | Mapbox 3D Map | **P2** | Performance & Interaction | Container clutter causes visual lag and click-event degradation. | Ensure the map container element is initialized completely empty. | `inc/drone-map.php` | Mapbox GL standard | Ship-this-month |

---

## 3. Per-Page Visual & UX Audits

### Homepage
*   **Desktop & Mobile Audit:** The current homepage uses a night drone-map hero that renders plain dots. It misses the approved mockup's promise: showcasing impressive, spinnable 3D building models up front. The copy has been cleaned of "language bragging" but needs visual weight.
*   **Competitor Benchmark (Compass):** Compass utilizes strict layout restraint and leads with premium exclusive-listings-first grids. Our homepage feels busy with too many text-heavy CTA bands.
*   **RTL/LTR Translation:** Toggling to English works structurally, but font fallbacks break the editorial look due to missing font declarations.

### Projects Catalog & 3D Map
*   **3D Map Audit:** The Mapbox container throws console warnings because it isn't initialized clean. The Three.js lighting uses viewport anchors which can cause unexpected shadows on rotation.
*   **Competitor Benchmark (Matterport/Zillow 3D):** Matterport coordinates look seamless. Our map dots feel flat and uninformative at a glance.

### Flagship Project Page (3D Showroom)
*   **3D Showroom Audit:** Rainbow Tel Aviv is broken (404 GLB). On Duo Tel Aviv, the Dusk/Night filters apply a nice CSS sepia/dark filter overlay, but the button active states do not swap.
*   **Sun Hours:** The "direct sun hours" line is static. If a user is on "Night Mode", displaying "7.5 sun hours" without dynamic explanation is confusing. It should state: "Equinox Day calculation: 7.5 hours".

### Regular Listing Page (Bialik RG 4R Demo)
*   **3D Tower Audit:** Rendering a generic, twisting 3D tower that is explicitly NOT the building is highly misleading. While a notice label is shown, the visual dominance of a fake building hurts the platform's core promise of "real 3D accuracy."
*   **Poster Loading:** During load, the container displays a generic gray field before the GLB renders.
*   **Visual Verdict:** Remove the generic 3D model. The parametric 2D SVG facade (which highlights the exact floor) is extremely impressive, lightweight, and accurate. It should be the main visual hero on listings, paired with a bespoke sketch.

### Professionals Directory & Profiles
*   **Audit:** The sponsored card listings on terms are woven nicely, but standard Gravatars look amateurish. There are no default avatars designed for the brand's creamy/sketch aesthetic.
*   **Competitor Benchmark (Zillow Agent Directory):** Zillow uses professional, vetted face portraits with gold Premier Agent borders. Our profiles look cold without fallback graphics.

---

## 4. Proposed Design Wireframes & Mockups

### Homepage Hero (Spinnable 3D Flagship)
Instead of a simple flat map with plain dots, the homepage hero should split into a spinnable architectural 3D sketch and a clean, search-first bar.

![Homepage Hero Wireframe](file:///C:/Users/pro/.gemini/antigravity/brain/106dbcc6-9bca-4a6f-8ee1-166cc3ba54b5/homepage_hero_wireframe_1783541822626.jpg)

*   **Proposed Layout:** Dark theater mode background (`#14130F`), clean search interface on the right with serif headings, and a spinnable detailed 3D building sketch model on the left to instantly convey the product's core feature.

---

### Property Listing Page (Sketch-First Facade)
Rather than loading a misleading, generic 3D tower that fails to represent the asset, we replace it with a high-end ink sketch of the actual building and the parametric SVG facade side-by-side.

![Property Listing Wireframe](file:///C:/Users/pro/.gemini/antigravity/brain/106dbcc6-9bca-4a6f-8ee1-166cc3ba54b5/property_listing_wireframe_1783541835580.jpg)

*   **Proposed Layout:** Editorial layout with clean property facts (price, room count, floor, sqm) above. Left side displays the bespoke hand-drawn ink sketch of the building. Right side hosts the lightweight, interactive SVG facade selector showing the highlighted unit.

---

### Professional Card & Custom Role Avatars
We replace Gravatar placeholders with elegant default silhouettes designed to fit the visual DNA.

![Professional Card Avatar Wireframe](file:///C:/Users/pro/.gemini/antigravity/brain/106dbcc6-9bca-4a6f-8ee1-166cc3ba54b5/professional_card_avatar_wireframe_1783541847302.jpg)

*   **Proposed Layout:** Minimalist profile card with cream background (#FAF7F1). Default avatar is an elegant line-art sketch portrait in gold and ink lines matching the professional's specific role (e.g. Attorney, Architect, Advisor).

---

## 5. "Top 20 Before Investors" Punch List

This punch list outlines the exact, buildable changes required. Every change is scoped to WordPress PHP, CSS, or vanilla JS:

1.  **Fix Tax Calculator Race Condition:** Shift the `window.NADLAN_PTAX` script output from `wp_footer` (priority 5) to `wp_head` or output it inline before the shortcode in `inc/calculators.php`. (*Effort: Ship-this-week*)
2.  **Add LTR Fonts to Theme CSS:** Insert the `@font-face` rules for `Fraunces` and `Inter Tight` in `style.css` pointing to local woff2 files. (*Effort: Ship-this-week*)
3.  **Fix English Projects Catalog Route:** Add rewrite rules for the `/en/projects/` path to point to the `nadlan_project` custom post type archive list. (*Effort: Ship-this-week*)
4.  **Resolve Rainbow Tel Aviv 3D Asset 404:** Update the path of the Rainbow GLB model in `inc/showroom-engine.php` to point to a valid media library URL. (*Effort: Ship-this-week*)
5.  **Remove Generic 3D Tower from Listings:** Delete the `model-viewer` block from the `nadlan_property` template and set the interactive 2D SVG facade and actual sketch as the main visual anchors in `inc/property-showroom.php`. (*Effort: Ship-this-week*)
6.  **Fix active button state in Sun Selector:** Modify the click event listener in `inc/showroom-engine.php` (and `property-showroom.php`) to correctly toggle active styles/attributes on the dusk/night buttons. (*Effort: Ship-this-week*)
7.  **Implement Role-Based Default Avatars:** Code a fallback in `inc/pro-cards.php` that serves role-specific default sketch vector files (e.g., `avatar-lawyer.svg`, `avatar-architect.svg`) instead of gravatar URLs when metadata is empty. (*Effort: Ship-this-week*)
8.  **Add Labels/IDs to Mortgage Calculator Form:** Add semantic `<label>` tags and matching `id`/`name` attributes to all form inputs in `inc/calculators.php`. (*Effort: Ship-this-week*)
9.  **Recalibrate Purchase Tax Brackets:** Correct the progressive calculation brackets for `single` residences and fix the event listener to trigger recalculation when changing dropdown selectors. (*Effort: Ship-this-week*)
10. **Clean Mapbox Map Container:** Add `container.innerHTML = ""` prior to Mapbox initialization in `assets/showroom-engine/engine.js`. (*Effort: Ship-this-week*)
11. **Consolidate Color Tokens:** Search PHP files for hardcoded hex codes (`#FAF7F1`, `#1B1A17`, etc.) and replace them with standard CSS variables (`var(--cream)`, `var(--ink)`). (*Effort: Ship-this-month*)
12. **Sun Hours Label Clarification:** Add a tooltip or small subtitle below the direct sun hours label clarifying that calculations are based on standard equinox solar angles. (*Effort: Ship-this-week*)
13. **Clean Up Table Borders on Mobile:** Add LTR/RTL media queries in `editorial.css` to ensure tables scroll horizontally on mobile screens without squishing text columns. (*Effort: Ship-this-week*)
14. **Add "Claim Profile" CTA to profiles:** Ensure all unclaimed professional cards render a clear "בעל המקצוע? לתביעת הכרטיס ←" link to feed the monetized claim funnel. (*Effort: Ship-this-week*)
15. **Pre-render 3D Stage Loading Background:** Replace the solid grey 3D loading box with a blurred, CSS-based mockup image of the building model during the download phase. (*Effort: Ship-this-week*)
16. **A-Z Encyclopedia Navigation Polish:** Group glossary terms alphabetically on `/glossary/` to mimic Wikipedia's directory search pattern. (*Effort: Ship-this-month*)
17. **Standardize Breadcrumbs:** Ensure all child post types (e.g., specific terms or listings) output standardized breadcrumbs pointing back to the main category hubs. (*Effort: Ship-this-week*)
18. **Add Milestone Notification Toggle in admin:** Build a checkbox in `admin-control.php` to allow the owner to activate/deactivate the automated milestone notifications. (*Effort: Ship-this-week*)
19. **Add canonical tags to professionals/projects:** Ensure Yoast SEO handles canonical links cleanly for all registered CPTs. (*Effort: Ship-this-week*)
20. **Disable autoplay auto-rotation on user scroll:** Prevent Mapbox or ThreeJS elements from rotating/spinning if the user scrolls past the element, saving client rendering overhead. (*Effort: Ship-this-week*)

---

## 6. Organic SEO Growth & Traffic Strategy

*   **Programmatic Directory Mapping:** The 1,700+ imported contractors are currently hidden from indexing via `noindex,follow`. To transform this into a traffic engine, the owner should set up an **automated Claim Funnel SEO landing page** once 100+ profiles are completed, allowing local searches ("קבלן רשום בתל אביב") to index.
*   **Dual-Language Schema:** Integrate standard `JSON-LD` schemas (`RealEstateAgent`, `SingleFamilyResidence`, `FAQPage`) that output correct localized schemas based on whether the visitor uses English or Hebrew.
*   **The Encyclopedia Internal Linker:** Automate internal linking by utilizing the `glossary-autolink` module to parse property listing descriptions and link key real estate terms directly to the corresponding encyclopedia pages. This will build a massive internal link network.
