# Skill: Goal Discipline And Anti-Drift

Use this skill before any long NadLan mission, especially project showroom, SEO, deployment,
WordPress admin, plugin, or child-theme work.

## Prime Rule

Do not confuse motion with progress. A task is progressing only when the next action makes the
requested end state more true and can be verified with evidence.

## Operating Method

1. Write the target in one sentence.
2. List the proof that would show the target is achieved.
3. Choose the smallest next step that produces or changes that proof.
4. Do that step.
5. Verify the result immediately.
6. Record the result and the next step.
7. Do not start a second branch, second feature, second article, or second deployment path until
   the current step is verified or explicitly abandoned.

## Anti-Drift Rules

- If live deployment is the blocker, do not write more speculative docs or features. Deploy or
  prove exactly why deployment cannot happen.
- If a browser/admin screen is needed, open Chrome and inspect the real screen. Do not infer from
  code alone.
- If a tool is missing, install, configure, or find the approved equivalent when possible. Do not
  use a missing local tool as a reason to invent a weaker path.
- If the environment requires an approval prompt, request the approval through the available tool
  and keep the task moving after it is granted. If the owner must act, state the exact action.
- If a source, login, payment account, official BIM/GLB, legal approval, OTP, or paid data license
  is owner-only, log it as owner-only and continue the next unblocked part.
- Never call a change done because it is committed, pushed, merged, saved in WordPress, or imported
  into meta. Done requires the buyer-facing rendered page or runtime behavior to pass the gate.
- Do not create another QA script when an existing script or Chrome screenshot can answer the
  question.
- Do not patch around the target. If the owner asks for apartment cells on the facade, do not ship
  floating dots and call it equivalent.

## Blocker Format

Use this exact format when blocked:

```text
BLOCKER:
Exact blocker:
Evidence:
Why it blocks the target:
What I tried:
Owner action needed:
Next unblocked step I will do meanwhile:
```

If there is no owner action needed, it is not a blocker. Continue working.

## Evidence Gate

For NadLan project pages, evidence means:

- Chrome screenshot at desktop, tablet, and mobile.
- Live URL or local preview URL.
- Healthcheck/version when plugin behavior is involved.
- One H1, no horizontal overflow, no console errors, no raw code leak.
- Buyer journey click proof: choose apartment, see selected card, open contact/view/details.
- Contractor journey proof: owner can find and edit the fields or payload used for the page.
- Source ledger for public facts, prices, claims, images, and generated illustrative material.

## Child Theme Versus Plugin Discipline

- Put reusable data contracts, REST endpoints, CPT/meta registration, sanitization, and shared
  business logic in the plugin.
- Put project-page layout, page chrome, heading alignment, visual wrappers, and template styling in
  the child theme when possible.
- Do not add a new plugin feature for a one-page visual concern if a theme template or CSS layer is
  the safer durable place.
- If plugin changes are unavoidable, keep the slice small and verify the ZIP with the release
  discipline skill before deployment.

## Questions Policy

Ask questions only when the answer cannot be discovered and a wrong assumption can harm the site,
legal position, payments, or public claims. Otherwise, make the conservative assumption and proceed.


