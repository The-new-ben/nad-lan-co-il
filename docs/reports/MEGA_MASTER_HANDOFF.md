# NADLAN: THE MEGA MASTER HANDOFF & PLATFORM DIRECTIVE

**To any AI Agent (Antigravity, Codex, CloudCode, Claude) reading this document:**
**STOP.** Do not write a single line of code until you have read this entire document. This is the Master Holistic Handoff. We are no longer doing pinpoint fixes or hacking things together. You must understand the full business model, the design vibe, the user journey, and the structural mess of the current codebase before you touch anything.

If you are asked to fix a bug, you must fix it *in the context of this master architecture*. 

---

## 1. BRAND IDENTITY & DESIGN VIBE
**What is NadLan?** 
NadLan is a high-end, premium real estate portal designed to disrupt the Israeli market (competing with Yad2/Madlan) and attract foreign investors (competing with Zillow/Compass). 

**The Vibe:** "Quiet Luxury." 
- **Colors:** Deep Charcoal (`#1c1a15`), Warm Cream (`#faf7f1`), and Terracotta (`#c2563a`). No generic WordPress blue/red. 
- **Typography:** High-contrast. Clean Sans-serif for data (`Inter` or `Heebo`), elegant Serif for headers (`Frank Ruhl Libre` or `Fraunces`).
- **Aesthetic:** We use a **"Creamy, Sketchy, Architectural"** design language. We do not use cheap, fake-looking AI generations. Everything should feel bespoke, professional, and trustworthy to High-Net-Worth Individuals (HNWIs).

---

## 2. THE BUYER JOURNEY & USER EXPERIENCE

The website is an ecosystem, not just a list of properties.

### A. The Traffic Funnel (SEO & Articles)
Buyers arrive via Google searching for "Sde Dov real estate" or "Israel mortgages for foreigners". They land on the **Magazine / Guides**. These pages must have flawless Technical SEO (no duplicate H1s, correct schema) and establish immediate trust.

### B. The Homepage & Map
The user lands on the homepage. They do not see a messy WooCommerce store. They see a sleek, app-like hero section with a search bar. They see a Mapbox integration with **3D building extrusions** (Zillow-style), allowing them to understand the geography of luxury developments instantly.

### C. The Project Showroom (The Decision Point)
When a user clicks on a project (e.g., *Ashira* or *Rainbow*), they enter the **Showroom**. 
- They see the project's surroundings.
- They interact with the building facade to select an apartment.
- They view floorplans and specs.

### D. The Action (No Shopping Carts)
Real estate is not an e-commerce checkout. We do not use "Add to Cart" or "Buy Now".
On mobile and desktop, the user is presented with a clean, unified **Action Rail** anchored at the bottom:
1.  **Call** (Direct to contractor)
2.  **WhatsApp** (Instant chat)
3.  **Offer Letter (LOI)** (A sleek, non-binding digital form to reserve a unit)

---

## 3. THE 3D SHOWROOM STRATEGY (SKETCH-FIRST)

**CRITICAL SHIFT:** We are moving away from heavy, glitchy, spinning 3D `.glb` models that flip upside down and break the browser.

**The "Sketch-First" Facade Approach:**
1.  We use a high-quality, static 2D image (an architectural sketch or render) of the building.
2.  We use CSS/HTML to draw invisible, clickable hot-zones over the windows/apartments.
3.  When a user hovers, it highlights. When clicked, a sleek white data panel slides out from the side showing the unit details (rooms, price, direction).
*This provides the illusion of 3D interaction with zero performance cost and 100% reliability.*

---

## 4. MONETIZATION & BUSINESS MODEL ("MILITARI-UTILIZATION")

We are building a machine that makes contractors fight for space and leads.
*   **Lead Arbitrage:** We capture international buyer intent via the LOI/WhatsApp rail and route it to contractors for a fee/commission.
*   **Premium Project Tiers:** Standard listings are boring text. Developers must pay a monthly subscription to activate the "Showroom Engine" (the interactive Sketch-First facade).
*   **Professional Directory:** Real estate agents, mortgage brokers, and designers pay a Freemium/Pro subscription (via PMPro + Stripe) to be listed and cross-linked to the projects they represent.

---

## 5. TECHNICAL ARCHITECTURE & THE DEPLOYMENT MESS

This is where the site is currently failing. You must understand this structure to avoid breaking things further.

**The Stack:**
*   **Parent Theme:** `nadlan-revenue` (Do not edit directly).
*   **Child Theme:** `nadlan-platform-child` (The intended home for our custom code).
*   **The Engine Plugin:** `nadlan-config` (Where the Showroom Engine lives: `plugins/nadlan-config/inc/showroom-engine.php`).

**The UPress Roadblock:**
The host (UPress) is blocking Git deployments from syncing with the Child Theme. Because of this, previous agents panicked and started injecting *everything*—including emergency layout CSS—into the `nadlan-config` plugin. 

**The Result:** The codebase is a fragmented, fragile mess. Elements are stacked on top of each other. The backend is fighting the frontend.

---

## 6. CURRENT CRITICAL BUGS & ROADBLOCKS (DO NOT REPEAT THESE)

If you are developing, you must solve these issues holistically, not with cheap CSS hacks.

1.  **The "Plus Thing" (Stacking Clutter):** There is a legacy floating Accessibility/WhatsApp widget bundle that expands via a "plus" icon. It overlaps with our custom Mobile Action Rail. It looks terrible. **Solution:** Kill the legacy plugins/theme widgets causing it. Split the functionality cleanly. No overlapping elements allowed.
2.  **The Ashira Translation Routing:** The site has 5 languages (HE, EN, FR, RU, AR), built as separate WordPress posts (e.g., `ashira-sde-dov` vs `ashira-sde-dov-en`). Currently, clicking Ashira on the Hebrew homepage routes the user to the English version. **Solution:** The `showroom-engine.php` (lines 96-101) dynamic routing logic is broken. Links must strictly point to the current active language's base URL.
3.  **Inconsistent Assets (AI vs Sketches):** The showroom engine tries to load whatever is in the database—sometimes a GLB model, sometimes a random AI picture. **Solution:** Lock the engine logic down. Enforce the Sketch-First static image as the primary default. Only load 3D if explicitly flagged and verified.

---

## 7. CODE EXAMPLES: THE WAY FORWARD

### Bad Practice (What we stop doing today):
*   Using `!important` to force CSS over conflicting plugins.
*   Injecting heavy `<style>` blocks in PHP headers because we can't sync the child theme.
*   Letting WordPress Block Engine inject `is-layout-constrained` which clips full-width designs.

### Good Practice (How you code from now on):
*   **Clean CSS Grid/Flexbox:** Build cohesive layouts where text and displays sit side-by-side cleanly, not stacked like a broken mobile view on desktop.
*   **Headless / API Thinking:** If the WordPress theme is too restrictive, we explore bypassing it. Build standalone React/Next.js components that talk to the WP REST API, rendering clean HTML on the frontend without theme interference.

*Example of the Sketch-First Clickable Overlay (Concept):*
```html
<div class="facade-container" style="position: relative; aspect-ratio: 4/3;">
  <img src="architectural-sketch.jpg" style="width: 100%; object-fit: cover;" />
  <!-- Clickable Unit Overlays -->
  <a href="#unit-12" class="unit-hotspot" style="position: absolute; top: 40%; left: 30%; width: 10%; height: 5%;"></a>
</div>
```

---

## 8. DIRECTORY OF CRITICAL RESOURCES

**AGENT PROMPT: You are required to use your `view_file` or `read_file` tools to read these documents if you need specific technical details on any sub-system.**

**Strategic Artifacts (Located in `C:\Users\pro\.gemini\antigravity\brain\106dbcc6-9bca-4a6f-8ee1-166cc3ba54b5\`):**
*   [project_state_summary.md](file:///C:/Users/pro/.gemini/antigravity/brain/106dbcc6-9bca-4a6f-8ee1-166cc3ba54b5/project_state_summary.md) - The brutal audit of current failures.
*   [architecture_and_design_flow.md](file:///C:/Users/pro/.gemini/antigravity/brain/106dbcc6-9bca-4a6f-8ee1-166cc3ba54b5/architecture_and_design_flow.md) - Mermaid diagrams of the site ecosystem and data flow.
*   [buyer_journey_directive.md](file:///C:/Users/pro/.gemini/antigravity/brain/106dbcc6-9bca-4a6f-8ee1-166cc3ba54b5/buyer_journey_directive.md) - Exact specs for SEO, LOI forms, and competitors.
*   [sketch_strategy_realistic.md](file:///C:/Users/pro/.gemini/antigravity/brain/106dbcc6-9bca-4a6f-8ee1-166cc3ba54b5/sketch_strategy_realistic.md) - Why we use 2D facades instead of 3D models.
*   [operations_manual.md](file:///C:/Users/pro/.gemini/antigravity/brain/106dbcc6-9bca-4a6f-8ee1-166cc3ba54b5/operations_manual.md) - Monetization tiers and 3D processing pipeline.
*   [visual_guide.md](file:///C:/Users/pro/.gemini/antigravity/brain/106dbcc6-9bca-4a6f-8ee1-166cc3ba54b5/visual_guide.md) - Before/After visual targets.
*   [codex_master_protocol.md](file:///C:/Users/pro/.gemini/antigravity/brain/106dbcc6-9bca-4a6f-8ee1-166cc3ba54b5/codex_master_protocol.md) - Collaboration rules for multi-agent workflows.

**Code Repositories:**
*   **The Live Codebase:** `C:\Users\pro\.gemini\antigravity\scratch\nad-lan-co-il\`
    *   *Critical file:* `plugins\nadlan-config\inc\showroom-engine.php`
*   **The React Design Prototypes (Lovable):** `C:\Users\pro\.gemini\antigravity\scratch\nadlan-strategy-hub\handoff\lovable\2026-06-23-war-room-sync\prototype-source\src\components\nadlan\`
    *   *Reference these files for perfect CSS/React architecture before porting to WP.*

---
**END OF DIRECTIVE.** 
**To the acting AI:** Acknowledge receipt of this document. Confirm you understand the "Sketch-First" strategy, the UPress deployment problem, and the mandate to stop stacking elements. Formulate your execution plan based *only* on this holistic understanding.
