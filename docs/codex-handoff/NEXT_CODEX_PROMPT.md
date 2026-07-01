# Codex Knowledge Transfer (KT) / End of Shift
**Date:** July 1, 2026
**Topic:** Buyer Journey, SEO H1 Fix, Mobile Rail, and 3D Model Corrections

## Context for the Next Agent
The previous agent (me) performed a full SEO/UX audit on the live site and created a directive (uyer_journey_directive.md). The user authorized execution, but then clarified they wanted all changes pushed to a separate branch for review by another agent before implementing on the live site or main.

## What is in this Branch (codex/buyer-journey-fixes-2026-07-01)?
1. **Code Changes (Staged/Committed):**
   - unctions.php: Added SEO H1 demotion filter + Mobile Floating Action Rail.
   - style.css: Added LTR/RTL multi-language alignments.
   - project-3d.php & all project-showroom-*.php patterns: Added min-camera-orbit and max-camera-orbit to prevent the 3D <model-viewer> from flipping upside down.
   - plugins/nadlan-config/inc/loi-form.php: Created the new Non-Binding Offer Letter shortcode logic.
   - plugins/nadlan-config/nadlan-config.php: Included loi-form.php.

2. **Documentation (In docs/codex-handoff/2026-07-01-buyer-journey/):**
   - udit_results.md: The raw technical findings.
   - uyer_journey_directive.md: The full spec/directive.
   - implementation_plan.md: The master war room architecture.
   - walkthrough.md: A summary of exactly what code changed.

## Your Mission
The user wants you to **review these changes** and ensure they are safe, correct, and align with the design system before merging them into main. Do not push directly to main until the user or you have thoroughly vetted this branch.
