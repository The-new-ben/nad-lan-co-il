> **RECONCILIATION AGAINST LIVE STATE — Claude Code (Opus 4.8), 2026-07-01. Read this first.**
>
> This is an Antigravity "holistic sweep" directive listing 12 problems + 25 SEO articles.
> Saved verbatim below the line, as the owner asked. But most of the "missing" / "broken"
> items were **verified already built and live** this session (via the live site HTML, the
> `/wp-json/nadlan/v1/healthcheck`, the live plugin inventory, and the plugin source). The
> directive appears written from stale or local-only knowledge, not the live site. **Do not
> rebuild these — that is exactly the duplication/stacking failure `skills/skill-release-
> discipline-and-mistakes.md` (M2/M6/M7) exists to prevent.**
>
> | # | Directive claim | Verified live state (2026-07-01) | Verdict |
> |---|---|---|---|
> | 1 | "Plus Thing" — two floating widgets stack on mobile | Live pages carry only our own `nadlan-accessibility.js`; NO third-party widget (no UserWay/AccessiBe/Tidio/etc). The sitewide WhatsApp float `#nlcta` does **not** render at all right now (code skips it when no WhatsApp number is set in Settings → NadLan CTA). So the "two WhatsApp buttons overlapping" is not currently reproducible. **Latent** risk only, once a number is set. | NOT REPRODUCIBLE as described; needs a real device look to close fully |
> | 2 | 3D engine vs sketch inconsistency | Not deeply re-verified this session; showroom engine unified in v1.69.65 per git log. | UNVERIFIED — check before acting |
> | 3 | Ashira HE→EN routing cross-wired | NOT verified this session. `showroom-engine.php` routing untouched by me. | UNVERIFIED — the one genuinely worth a targeted look |
> | 4 | RTL / `is-layout-constrained` clips H1 at 760px | This is the v1.69.68 fix already shipped + live (override present in served HTML). | ADDRESSED (needs visual confirm on mobile) |
> | 5 | Favicon missing | Live `<head>` serves `nadlan-favicon-*.png` at 32/192px + apple-touch-icon. | ALREADY DONE |
> | 6 | Mega menu missing | Not verified this session. | UNVERIFIED |
> | 7 | Magazine grid never ported; projects "just dumped on page" | **FALSE.** `/projects/` renders via a dedicated `nadlan_dir_project_card()` (directory.php:644): 4:3 hero photo, project-type pill, city/units/developer meta, "מקודם" featured badge, gov.il trust badge, hover-shadow + hairline borders. On-brand card grid, live. Differs from the Lovable `MagazineCard.tsx` only in specific design details (see below). | ALREADY BUILT; only a design-refinement gap remains |
> | 8 | Woo cart instead of LOI | LOI shipped v1.69.63 (`inc/loi-form.php`, `inc/offers.php`). | ALREADY DONE |
> | 9 | Professional Directory missing | **FALSE.** `inc/directory.php` is a live 52KB "Midrag/Houzz/Thumbtack-class" directory: hero search, live AJAX filter/sort, sidebar facets w/ counts, colour-coded profession pills, official רשם הקבלנים (gov.il) trust badge, sponsored/featured (`paid_tier`) ad slots. `nadlan_professional_cpt: true` in healthcheck; thousands of records. `/professionals/` H1 = "מצאו בעל מקצוע מאומת לנדל״ן". PMPro (Paid Member Subscriptions) already active. | ALREADY BUILT — do NOT rebuild |
> | 10 | 25 SEO articles | Content task, not verified. The 25-title list below is genuinely useful as a content backlog. | BACKLOG (valid) |
> | 11 | Plugin-vs-theme deploy mess (child theme has no live git-sync) | TRUE and correctly diagnosed. This is the real structural problem; deep-research on pipeline fixes is in flight (2026-07-01). See also `skills/agent-direct-wordpress-access.md` (4 direct-access tools now installed). | REAL — the actual root issue |
> | 12 | ACF / metadata consolidation | Not verified this session. | UNVERIFIED |
>
> **Net:** items 5, 8, 9 are done; 7 is built (refinement-only); 4 is shipped; 1 is not
> currently reproducible; 11 is the real structural problem. The genuinely open,
> worth-doing items are **#3 (Ashira routing — verify first), #7 (card design refinement
> toward the Lovable magazine look), #10 (content), and #11 (deploy pipeline).** Everything
> else: verify against the live site before writing a line of code.
>
> **On #7 specifically (the "Lovable port" the owner wants to try):** the project card
> already exists and is on-brand. The deltas vs `MagazineCard.tsx` are: (a) it uses a
> profession-style avatar+icon, an odd metaphor for a building; (b) no From-price / rooms /
> completeness stat row; (c) no facade/plan image toggle. (b) needs price/rooms/completeness
> meta that may not exist on every project; (c) needs JS + a plan asset per project. So a
> faithful full port is non-trivial and partly data-blocked — a scoped visual refinement of
> `nadlan_dir_project_card()` is the realistic version. It touches a live, no-staging module,
> so it must ship versioned + be visually gated before the owner's Update click.
>
> Source component: `handoff/lovable/2026-06-23-war-room-sync/prototype-source/src/components/nadlan/MagazineCard.tsx`
> Card renderer to refine: `plugins/nadlan-config/inc/directory.php` → `nadlan_dir_project_card()` (~line 644)
>
> ── original Antigravity directive, verbatim, below ──

---

# 🏗️ NADLAN PLATFORM HOLISTIC SWEEP & EXECUTION DIRECTIVE

To the AI acting on this document: Do not make pinpoint fixes. Understand the "Quiet Luxury" design language, the top-of-funnel traffic strategy, and the structural conflict between the UPress Child Theme and the Plugins. Execute fixes holistically based on this list.

## 🚨 PHASE 1: UX CLUTTER & VISUAL BREAKDOWNS

### 1. The "Plus Thing" (Stacking Floating Widgets)
*   **The Problem:** On mobile, there is an expanding "Plus" button widget (likely a bundle containing Accessibility, WhatsApp, or Contact links) that floats in the bottom corner. It is overlapping and stacking directly on top of the custom **Mobile Action Rail** we built. It looks chaotic, blocks the screen, and ruins the high-end feel.
*   **The Design Goal:** A single, clean, bottom-anchored action bar (Call / WhatsApp / Offer) on mobile. No floating bubbles overlapping each other.
*   **How to Fix:** Inspect the live DOM to find the exact class/ID of the legacy widget (often injected by a plugin like `pojo-accessibility` or a WhatsApp chat plugin). Write aggressive CSS in the plugin/theme to `display: none !important;` the floating wrapper, or cleanly deactivate the conflicting plugin.

### 2. The 3D Engine vs. Sketch-First Inconsistency
*   **The Problem:** Every project page looks like a different website. Some try to load a heavy, glitchy 3D `.glb` model that spins out of control. Others load low-quality AI generated pictures.
*   **The Design Goal:** Uniformity and stability. We agreed on the **"Sketch-First" Facade Strategy**: A high-quality, static 2D image of the building with invisible HTML "hot-zones" drawn over the windows. Clicking a window slides out a sleek white data panel. It creates a 3D *illusion* without the lag.
*   **How to Fix:** Update `plugins/nadlan-config/inc/showroom-engine.php`. Strip out the fallback logic that tries to guess the asset. Force the engine to render the `project_3d_facade_images` array by default. Wrap the facade in a `relative` container and map `absolute` positioned anchor tags based on the unit coordinates. Lock the `model-viewer` behind a strict conditional (only load if a perfect GLB exists and `min-camera-orbit` is locked so it can't flip upside down).

### 3. Ashira & The Multi-Language Routing Bug
*   **The Problem:** When you click on the "Ashira" project from the Hebrew homepage, it opens the English version (`/projects/ashira-sde-dov-en/`). The site has 5 languages structured as separate WP posts (`-en`, `-fr`, `-ru`, `-ar`), but the routing is completely cross-wired.
*   **The Design Goal:** An Israeli user browsing the Hebrew site must land on the Hebrew project page. The language switcher in the header should be the *only* way the URL structure changes.
*   **How to Fix:** Rewrite the catalog generation loop in `showroom-engine.php` (around line 96). Stop using fuzzy slug matching for the primary href. The primary card link must grab the exact permalink of the current `$post->ID`. The sibling language links should be strictly reserved for the `<nav class="language-switcher">` and built using `hreflang` metadata or explicit ACF relationship fields, not string replacement hacks.

### 4. RTL / LTR Content Bleeding
*   **The Problem:** Because the site mixes Hebrew (RTL) and foreign languages (LTR), text blocks and H1 titles are occasionally clipping on the left side or wrapping awkwardly because the container doesn't know which direction to align.
*   **The Design Goal:** Perfect typography alignment depending on the language of the specific page.
*   **How to Fix:** Ensure `html[lang="he-IL"]` triggers a strict `.rtl` CSS scope. Use modern CSS logical properties (`margin-inline-start`, `padding-inline-end`) instead of hardcoded `margin-left` and `margin-right`. Ensure the WordPress `is-layout-constrained` class does not cap full-width heroes at `760px` in RTL mode.

### 5. Missing Favicon & Branding
*   **The Problem:** The custom "NadLan Architectural" favicon was created but is not consistently showing up on all devices/browsers, leaving a generic WordPress icon.
*   **The Design Goal:** A consistent, premium brand mark in the browser tab.
*   **How to Fix:** Ensure the favicon is registered properly in the WordPress Customizer (Site Identity). If blocked, manually inject the `<link rel="icon" href="/path/to/nadlan_premium_favicon.jpg" sizes="32x32">` into the `<head>` via `wp_head` action in the plugin.

## 🏗️ PHASE 2: STRUCTURAL GAPS & MISSING FEATURES

### 6. The Missing "Mega Menu" & Site Hierarchy
*   **The Problem:** The old theme had a rich, real-estate-focused Mega Menu. Right now, the navigation is flat. We are failing to guide users properly through the ecosystem.
*   **The Design Goal:** A structured hierarchy: *Cities -> Neighborhoods -> Projects -> Apartments*. The header must allow users to browse by "Demand Areas" (e.g., Sde Dov, Tel Aviv Center) and "Guides".
*   **How to Fix:** Rebuild the WordPress Navigation Menu. Use a CSS-only hover Mega Menu (no heavy JS plugins). Structure the DOM cleanly:
  ```html
  <nav class="nl-mega-menu">
    <li class="has-dropdown">אזורי ביקוש
      <ul class="dropdown-grid">
        <li><a href="/city/tel-aviv/sde-dov/">שדה דב</a></li>
      </ul>
    </li>
  </nav>
  ```

### 7. The Missing "Lovable Listings / Magazine Grid"
*   **The Problem:** We designed a beautiful, filterable "Magazine Grid" in Lovable (`MagazineCard.tsx`, `listings.tsx`) for the catalog page, but it was never ported to WordPress. Right now, projects are just dumped onto the page.
*   **The Design Goal:** An elegant, 3-column masonry/grid layout with subtle hover shadows (`hover:shadow-[0_8px_24px_-12px]`) and tags for "New", "Pre-sale", etc.
*   **How to Fix:** Port the `MagazineCard` React structure into a PHP template (`archive-nadlan_project.php`). Apply the exact CSS tokens from the Lovable source (`aspect-[4/3]`, `bg-card`, `hairline` borders). Add a frontend filter bar (using URL query parameters, e.g., `?city=tel-aviv&type=investment`) to sort the grid natively without heavy AJAX plugins.

### 8. The E-Commerce Cart vs. Letter of Intent (LOI)
*   **The Problem:** Real estate in Israel cannot be bought via an online shopping cart. Any remnants of WooCommerce "Add to Cart" buttons damage the site's credibility and create legal confusion.
*   **The Design Goal:** The buyer journey must end in a "Lead Arbitrage" funnel. The button must say "Submit Offer (LOI)" or "Check Availability".
*   **How to Fix:** Strip all WooCommerce cart hooks from the project pages. Build a clean, multi-step digital form (Name, ID, Offer Price, Mortgage Pre-approval). When submitted, this form must route to the Contractor Dashboard backend and trigger an email.

## 📝 PHASE 3: TOP-OF-FUNNEL CONTENT STRATEGY

*We are currently only a "Projects" website. To get traffic (especially foreign investors), we must become a "Real Estate Hub". We need to build out the Top-of-Funnel (ToFu) content that catches Google searches before the user even knows which project they want.*

### 9. The Missing "Professional Directory"
*   **The Problem:** We discussed monetizing the platform by charging real estate agents, mortgage brokers, and interior designers to be listed. This directory doesn't exist.
*   **The Design Goal:** A searchable index of professionals, cross-linked to the projects they worked on. (e.g., "Dana Oberson - Interior Designer for Ashira").
*   **How to Fix:** Create a Custom Post Type (CPT) for `nadlan_professional`. Create a taxonomy for `profession_type`. Build a sleek archive page. Integrate PMPro (Paid Memberships Pro) to lock premium profile fields behind a subscription.

### 10. The 25 Critical SEO Articles (The Traffic Engine)
*   **The Problem:** We have zero inbound organic traffic strategies deployed. We need the magazine/guides section live immediately.
*   **The Goal:** Publish the following 25 highly-targeted SEO articles to capture both local Israeli searches and foreign investor queries.
*   **How to Fix:** Create a dedicated "Guides" (`/guides/`) hub using a beautiful editorial grid.

**The 25 SEO Article Hit-List (Give this to the content generation agent):**
1. **Tabu Check Tool & Guide:** How to read an Israeli Tabu extract (Highest volume KD 25 target).
2. **Sde Dov Masterplan 2026:** Everything buyers need to know about the new Tel Aviv district.
3. **Foreign Buyers Guide to Israel Real Estate:** Taxes, trusts, and transferring funds.
4. **Israel Mortgage Rates for Non-Residents:** How to get financing from abroad.
5. **Purchase Tax (Mas Rechisha) Calculator & Brackets for 2026.**
6. **Tel Aviv vs. Jerusalem:** Where should foreign investors park their money?
7. **The "Presale" (Al HaNiyar) Strategy:** Risks and rewards of buying on paper in Israel.
8. **Arnona (Property Tax) Explained:** Average costs by city.
9. **How to Choose a Real Estate Lawyer in Israel.**
10. **The Bank Guarantee (Arvut Chok Mecher):** How your money is protected.
11. **New Build vs. Second Hand in Tel Aviv:** A financial breakdown.
12. **Understanding the "Madad" (Building Construction Index):** How it affects your final price.
13. **TAMA 38 vs. Pinui Binui:** A guide to urban renewal investments.
14. **Guide to Buying Property in Netanya (The French Riviera of Israel).**
15. **Guide to Buying Property in Bat Yam (The new coastal boom).**
16. **How to Manage a Rental Property in Israel from Abroad.**
17. **Capital Gains Tax (Mas Shevach) Exemptions for Olim.**
18. **The Role of the "Shamai" (Property Appraiser) in Israeli Mortgages.**
19. **What is a "He-arat Azhara" (Warning Note) and why do you need one?**
20. **AirBnb Regulations in Tel Aviv: 2026 Update.**
21. **Architectural Trends:** Why developers are shifting to "Quiet Luxury" interiors.
22. **The Impact of the Light Rail (Dankal) on Gush Dan Property Values.**
23. **How to Transfer Large Sums to Israel Safely (Anti-Money Laundering laws).**
24. **Hidden Costs of Buying an Apartment:** Broker fees, lawyer fees, and VAT.
25. **The Ultimate Moving to Israel (Aliyah) Housing Checklist.**

## 💻 PHASE 4: THE TECHNICAL DEPLOYMENT MESS (THE ROOT CAUSE)

*To the executing AI: You cannot just write code and hope it works. You must navigate the specific UPress server restrictions on this project.*

### 11. The Plugin vs. Theme War
*   **The Problem:** UPress blocks standard Git pushes from syncing with the `nadlan-platform-child` theme folder. Because of this, previous developers started shoving massive inline `<style>` tags and PHP logic into the `nadlan-config` plugin just to bypass the server block.
*   **The Design Goal:** Separation of concerns. CSS goes in stylesheets. Logic goes in plugins. Templates go in themes.
*   **How to Fix:**
    *   *Option A (If UPress remains blocked):* Officially accept the plugin as the rendering engine. Enqueue actual `.css` and `.js` files from inside the plugin's `assets/` folder using `wp_enqueue_style`, rather than echoing `<style>` tags in the PHP headers.
    *   *Option B (Headless / API):* Stop fighting WordPress templates entirely. Build the frontend in a standalone React/Next.js environment (using the Lovable code) and connect it to WordPress via WPGraphQL. This completely bypasses UPress theme restrictions.

### 12. ACF / Metadata Consolidation
*   **The Problem:** The database is messy. There are old custom fields fighting with new JSON arrays (e.g., `nlp3d_use_engine` vs `project_3d_environment_json`).
*   **How to Fix:** Run a cleanup script. Define strict Advanced Custom Fields (ACF) local JSON groups for the projects. If a field isn't in the ACF JSON, the engine should ignore it. Stop trusting raw `get_post_meta` calls without strict sanitization.
