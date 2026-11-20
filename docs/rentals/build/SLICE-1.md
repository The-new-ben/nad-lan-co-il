# Rentals world, build slice 1 (HAD-795, stage 5)

Agreed with the coordinator on 20.11.2026. Starts when gate frame 1 (the 3D overview) has passed the coordinator and this session; the slice itself contains NO 3D. Design source: boards 1a, 2, 3, 4 (docs/rentals/design/README.md).

## What the slice is
1. The landing screen "היום" (board 4): the home drawing in a title block (date, one sentence), the lease ruler, the bottom-anchored main card in three states (urgent, due soon, quiet day), the fixed camera row, five tabs with icons (היום, הדירה, השכירות, כספים, מסמכים).
2. Camera-first repair (board 3): one button, the phone camera, saved with no form; details after. Target 3 presses, two of them the phone's own camera.
3. The index update that saves (board 3): the sheet shows today's rent, the base index, the latest index and the new rent, and one button saves it for the month it applies to. Target 2 presses.
4. The tenancy axis in its simplest form (board 2): the folding ruler with twelve month buttons, the next-due sheet, and "התקבל" in one press.
5. Hebrew and English together. Drawing mode only.

Not in slice 1: the 3D view (second slice, behind its budget measurement and the picture gate), send-a-professional, close-with-invoice, add-a-document, the full axis rows after the next-due one, French, Russian and Arabic, opening version 2 to the public (the coordinator's decision).

## Where it lives
- Version 2 of the rentals app (live for administrators and pilot landlords only: option `nadlan_rentals_v2` = 'admin'), so real visitors do not see the slice until the coordinator opens v2. Source of truth for v2 files: the live server (fetch through the bridge and compare md5 before every edit); a copy is in worktree `.claude/worktrees/bold-cray-ad2cea`; the main checkout now holds `assets/rentals/i18n/`, `help/`, `guide/` as released in 1.72.720.
- New files (additive, nothing removed): `assets/rentals/rm-today.js` + `rm-today.css` (the drawing sheet, the ruler, the main card, the camera row), `assets/rentals/rm-plan2d.js` (the flat services drawing from a plan), strings added to `assets/rentals/i18n/he.json` and `en.json`. The existing today view stays reachable (a setting) until the new one has passed a week of use by the administrator.
- Server: reuse `inc/rentals/rest.php` and `money.php`. New endpoints only where a one-press job needs one: (a) create a repair together with its first photo in one call; (b) confirm an index update (a ledger record with the base index, the applied index, the new amount and the month it starts; append-only like every money record, with a `client_ref` so a retry never doubles); (c) mark this month's rent received with the expected amount and today's date in one call, if the present call needs more than one.

## Open design decisions taken now
- An apartment with no plan: the title block shows the systems as a row of the same line icons with their states instead of a floor drawing, and offers "להוסיף תוכנית" (the apartment designer's own plan maker already exists). Never a made-up floor plan.
- The parts of the home come from the appliances table that v2 already has, extended with the tree's parts (docs/rentals/bom/tree/06-maintenance.json, 06.01): each part has a kind (system or appliance the landlord left), a room, a layer (water, electricity, gas, air conditioning) and a state derived from its open repairs and reminders.
- "Who repairs by law" text appears only for systems, in the statute's own words (s.25ח); for appliances the landlord left the screen points to the contract and states no rule (lawyer list).
- Reminders shown are the landlord's own; nothing is sent to a tenant automatically.

## Budgets and checks (written before the code)
- Phone first at 390 px: every button 44 px or more; the main card's actions and the camera row between 35% and 98% of the height; "what is waiting" with 0 presses; repair with a photo 3 presses; index update 2; rent received 1.
- Weight: the slice adds no 3D library; target under 60 KB of new script and style, measured.
- Reduced motion: every transition off under `prefers-reduced-motion`.
- Tests before release: a lab script that presses the four jobs at 390 and 1440 in he and en and counts presses (the pattern of `docs/rentals/bom/compare/taps-v2/count_v2.py`); the existing labs (lab_money, lab_drill, lab_shots) must still pass; `php -l`, `node --check`.
- Release: through the queue (`docs/coordination/claude-codex.md` claim and lock lines, `scripts/project-stage/make_deployNNN.py` on `kl_release.build_release`, `tools/source_audit.py` before and after, `tools/content_first_check.py`, Rainbow and H Infinity spot checks), then pressed live as the administrator in the owner's Chrome and reported with the sentence "not measured on a real phone" until someone holds one.

## Still drafts for a lawyer (labelled as drafts in the product)
The landlord's own signature; guarantors as people; reminders to tenants; the screening tip; who repairs an appliance the landlord left; Credit Data Law s.110 from 26.1.2027; whether a security cheque counts toward the cap (v2 code still adds it: `rm-drawers.js:85`, `:375`).
