# NadLan Autonomous Execution Master Skill

> This is the consolidated operating skill for Codex, Claude, Lovable imports, and any future agent working on NadLan or cloning the NadLan method to another WordPress site. Open this before any showroom, listing, homepage, city page, SEO, plugin, theme, or visual-design execution. It does not replace the smaller skills. It is the master checklist that points to them and keeps the rules in one place.

## When to use this

- At the start of every NadLan implementation session.
- Before changing the showroom, listings, homepage, city pages, public copy, plugin releases, theme CSS, or admin strategy room.
- Before replicating the NadLan 3D and AI process onto another WordPress site.

## Honesty statements

1. I do not call work done without proof.
2. I do not claim that a visual change is correct without screenshots saved in the repo.
3. I do not claim a release ZIP is safe without checking the real artifact.
4. I do not fake missing assets, facades, floor plans, maps, market data, or project photos.
5. I do not expose internal agent, prompt, SEO, or technical language on public pages.
6. I do not stack CSS or duplicate elements as a final solution. If a design is replaced, the old active source is removed or disabled first, then the new source becomes primary.

## First reading order

Read these before acting:

1. `AGENTS.md`
2. `COORDINATION.md`
3. `BACKLOG.md`
4. `skills/MAP.md`
5. This file
6. `skills/codex-plugin-access-and-deploy.md`
7. `skills/honesty-statement.md`
8. `skills/copywriting-skill.md`
9. `handoff/shared-knowledge/skills/nadlan-screenshot-first-visual-qa.md`
10. `handoff/lovable/2026-06-23-war-room-sync/source-manifest.md`
11. `handoff/lovable/2026-06-23-war-room-sync/reports/`
12. `handoff/lovable/2026-06-23-war-room-sync/data/nadlan-tokens.css`
13. `docs/research/2026-06-23-codex-skills-research.md` when improving Codex, skills, autonomy, or release discipline.

For a design task, also read:

- `skills/luxury-design-system.md`
- `skills/design-rtl-hebrew.md`
- `skills/project-3d-sales-experience.md`
- `handoff/shared-knowledge/skills/nadlan-showroom-design-rules.md`
- `handoff/shared-knowledge/skills/nadlan-editorial-bright-tokens.md`

For SEO or public copy, also read:

- `skills/url-namespace-contract.md`
- `skills/internal-linking-hub-spoke.md`
- `skills/authority-eeat-program.md`
- `skills/yoast-config.md`

For autonomous Codex, WordPress plugin, or release work, also open the relevant adopted skill:

- `skills/adopted-codex-goal-bundle.md`
- `skills/adopted-codex-instruction-chain.md`
- `skills/adopted-codex-progressive-disclosure.md`
- `skills/adopted-codex-visual-proof-loop.md`
- `skills/adopted-wp-playground-verification.md`
- `skills/adopted-wp-plugin-quality-gate.md`
- `skills/adopted-wp-security-threat-gate.md`
- `skills/adopted-wp-performance-gate.md`
- `skills/adopted-wp-accessibility-rtl-gate.md`
- `skills/adopted-wp-release-agent-gate.md`
- `skills/adopted-wp-rest-api-contract-gate.md`
- `skills/adopted-wp-mcp-abilities-map.md`

## Adopted Codex and WordPress skill pack

The adopted skill pack was created after external research into Codex skills, AGENTS.md, WordPress agent skills, visual QA, release gates, and autonomous work loops. The research report is `docs/research/2026-06-23-codex-skills-research.md`.

Use these as operating modules:

| Skill | Use it when |
|---|---|
| `skills/adopted-codex-goal-bundle.md` | The request is broad and must become one bounded execution slice with proof. |
| `skills/adopted-codex-instruction-chain.md` | Repo guidance, AGENTS.md, commands, done definition, or escalation rules may be stale or unclear. |
| `skills/adopted-codex-progressive-disclosure.md` | There are too many reports or references and Codex must load only the relevant ones. |
| `skills/adopted-codex-visual-proof-loop.md` | Any visible UI, screenshot, responsive, or public-language task is in scope. |
| `skills/adopted-wp-playground-verification.md` | A WordPress change needs local runtime proof before it is considered ready. |
| `skills/adopted-wp-plugin-quality-gate.md` | Plugin code, ZIP packaging, release artifact, i18n, or Plugin Check quality is in scope. |
| `skills/adopted-wp-security-threat-gate.md` | REST, AJAX, SQL, uploads, auth, nonce, escaping, or user input is touched. |
| `skills/adopted-wp-performance-gate.md` | Public pages, asset loading, queries, REST calls, or duplicate CSS/JS may affect speed. |
| `skills/adopted-wp-accessibility-rtl-gate.md` | Hebrew, RTL, keyboard, focus, contrast, mobile, or public UI is touched. |
| `skills/adopted-wp-release-agent-gate.md` | A release needs separation between implementer, verifier, package, and deploy steps. |
| `skills/adopted-wp-rest-api-contract-gate.md` | REST endpoints, schemas, permissions, or API consumers are touched. |
| `skills/adopted-wp-mcp-abilities-map.md` | Existing plugin capabilities, MCP, abilities, or WordPress admin surfaces should be mapped before inventing new code. |

Rules for adopted skills:

- Keep each skill small and single-purpose.
- Do not copy outside skills wholesale.
- Adapt external advice to NadLan: public-language hygiene, no CSS or element stacking, two-key plugin release gate, screenshot proof, RTL Hebrew, Lovable sync, and UPress deployment reality.
- When a new external pattern becomes useful, add a small NadLan skill and update this master file, `skills/MAP.md`, `skills/SKILLS-TREE.md`, and `BACKLOG.md`.

## The no-stacking rule

This is one large rule that overrides quick fixes:

If the goal is to replace a visual system, do not add a late override layer on top of the old system. Remove or stop loading the old active CSS, old template section, old duplicated element, or old render path first. Then add the new system as the primary source.

Allowed:

- Keep old functions or files for history if they are not active.
- Add a scoped compatibility rule only when it preserves behavior, not when it paints over the old design.
- Use CSS variables and tokens as the primary source.

Not allowed:

- Old dark showroom CSS loaded first, cream CSS loaded last.
- Old floating cards kept in the DOM and hidden with more CSS while a new card is added.
- Duplicate mobile drawers, duplicate CTAs, duplicate hero blocks, duplicate H1s.
- `!important` as a substitute for removing the wrong active source.
- A screenshot that looks correct only because an injected preview CSS overrode the real deployed CSS.

Why this rule exists:

- WordPress inline styles are printed in order after the registered stylesheet, so later blocks can silently override earlier blocks. See `wp_add_inline_style`: https://developer.wordpress.org/reference/functions/wp_add_inline_style/
- CSS cascade order makes late rules win when specificity and origin allow it. See MDN cascade: https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Cascade/Introduction
- `!important` changes cascade order and should be rare, not the architecture. See MDN cascade: https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Cascade/Introduction

## Autonomous execution loop

Use this loop without waiting for the owner unless credentials, payment, destructive deploy, or private data decisions are required.

1. Sync context.
   - Fetch current branch and inspect `git status`.
   - Read `COORDINATION.md`, `BACKLOG.md`, and the latest handoff files.
   - If Lovable is involved, fetch `https://github.com/The-new-ben/nadlan-strategy-hub.git` and mirror only the relevant `handoff/lovable/...` files.

2. Define the slice.
   - One public outcome at a time: showroom, then homepage, then listings, then city pages.
   - For plugin releases, one version per release and one PR per coherent release.
   - Write the acceptance criteria before editing.

3. Inspect before editing.
   - Search for existing source owners.
   - Identify active enqueue paths, templates, render functions, and duplicate UI elements.
   - Screenshot the current state if the task is visual.

4. Implement by replacement, not stacking.
   - Remove or disable the old active visual source.
   - Add the new source using the Lovable tokens and WordPress stack.
   - Keep behavior and data truth intact.

5. Run technical gates.
   - PHP lint for changed PHP files.
   - Inline JS syntax check when PHP contains JavaScript.
   - Build plugin ZIP with `scripts/build-plugin-zip.py`.
   - Verify plugin release with `scripts/verify-plugin-release.py`.
   - Inspect ZIP for backslash paths, rooted entries, traversal, CRC, and version drift.

6. Run public-language gates.
   - Search public output and source for internal words: prompt, war room, money page, KD, GLB status labels for buyers, Sponsored/Featured labels unless legally and UX approved, CRM, lead, pipeline, schema, token, Tailwind, Lovable, Codex, Claude.
   - No em dash in new public or owner-readable copy.
   - No generic AI filler from `skills/copywriting-skill.md`.

7. Run screenshot gates.
   - Save desktop 1440 or 1280 and mobile 390 screenshots in the repo.
   - Include Hebrew and English when changed.
   - Include important states: real model, facade fallback, missing asset, selected unit, contact flow, empty state, error state.
   - Write a visual QA note with what passed, what failed, and what is not live yet.

8. Commit and push.
   - Commit only the scoped files.
   - Push branch.
   - Open or update PR.
   - Do not merge your own PR if the two-key gate is active.

9. After deploy.
   - Verify live healthcheck version.
   - Capture live screenshots again.
   - Record the result in `skills/site-state.md` or `COORDINATION.md`.

## Screenshot proof requirements

Minimum for every public UI change:

- `desktop-1440.png` or `desktop-1280.png`
- `mobile-390.png`
- HTML or Markdown visual QA report
- `report.json` when a Playwright harness exists

For showroom:

- Rainbow or the active project with real GLB state.
- Unit selected state.
- Mobile 390 with no horizontal overflow.
- Contractor-sellable assessment.

For listings, homepage, and city pages:

- Hebrew and English when available.
- Header, main viewport, below-fold cards, footer.
- Mobile menu open if header changes.
- No public leakage of internal labels.

Screenshots are not proof if:

- They are only from Lovable when the live target is WordPress.
- They are only an injected preview and not labeled as such.
- They crop away the broken area.
- They hide the mobile bottom or right edge where overflow appears.

Playwright screenshot reference: https://playwright.dev/docs/screenshots

## Asset truth rules

Use this order:

1. Real owner, contractor, project, or public-source image with source recorded.
2. Real facade, render, floor plan, or GLB from the project.
3. Researched public image with source and date recorded.
4. Generated prototype image, clearly marked as illustrative.
5. Premium missing state when no truthful asset exists.

Never present an unrelated mock villa or apartment as a real project asset.

For the showroom:

- Real GLB means render the model and use unit-map camera data.
- Facade fallback means use a real facade/elevation image or show a truthful missing state.
- No generated rectangle grid pretending to be a facade.
- If a buyer clicks a unit, the model or facade must move or focus to the unit where data exists.

## Public-language rules

Public visitors include:

- Israeli buyers.
- Israeli investors.
- Foreign investors.
- Contractors and developers evaluating whether to pay.
- Professionals who may claim or sponsor listings.

Public pages must not talk to agents, developers, or internal SEO operators. Keep technical terms out unless the user needs them. A contractor upload screen can say GLB. A buyer-facing button should not.

Forbidden in buyer-facing UI:

- Lovable, Codex, Claude, prompt, token, Tailwind, shadcn.
- money page, KD, pillar, spoke, cluster, cannibalization.
- lead, CRM, pipeline, attribution, UTM.
- fake, mock, placeholder, unless it is an honest missing-state note.
- Sponsored, Featured, Promoted unless the disclosure and ranking policy are final and legally approved.

Use buyer language:

- "בחרו דירה"
- "בדקו נוף וכיוון"
- "השאירו פרטים לשיחה עם היזם"
- "המחיר והזמינות יאומתו לפני התקדמות"

Use contractor language:

- "העלאת מודל תלת ממד"
- "העלאת חזית"
- "שיוך דירות לנקודות במודל"
- "תצוגת משקיעים"

Use investor language:

- "תשואה משוערת"
- "סביבת הפרויקט"
- "עלויות רכישה"
- "בדיקות לפני החלטה"

## Plugin release rules

Before any plugin release:

1. Bump all version surfaces.
2. Update cache-busters for style and script.
3. Build ZIP only with `scripts/build-plugin-zip.py`.
4. Verify with `scripts/verify-plugin-release.py`.
5. Confirm no backslash paths in ZIP.
6. Confirm version surfaces match.
7. Confirm manifest download URL matches the version.
8. Do not hand-zip on Windows.
9. Do not deploy until screenshots and verifier are saved.

Why:

- A pre-push hook can reject bad pushes by exiting non-zero. Git hook reference: https://git-scm.com/book/en/v2/Customizing-Git-Git-Hooks
- WordPress plugins need explicit sanitization and validation for untrusted data. WordPress security reference: https://developer.wordpress.org/apis/security/sanitizing/
- WordPress plugin development must follow hooks, security, i18n, and lifecycle rules. Plugin handbook: https://developer.wordpress.org/plugins/

## Codex autonomy rules

Codex should work autonomously when:

- The repo contains enough context.
- The task is a bounded implementation or QA slice.
- The needed source files are local.
- The next action does not spend user money or deploy to production.
- The action can be verified with commands and screenshots.

Codex must stop or ask only when:

- Credentials or user account approval is needed.
- A payment or credits decision is needed.
- A destructive deploy or live server action is needed.
- Public legal or regulated wording needs owner approval.
- Two agents changed the same file in conflicting ways.

Good owner prompt for autonomous Codex work:

```text
Use the NadLan autonomous execution master skill. Continue the active goal. Read the latest handoff, Lovable materials, COORDINATION, BACKLOG, and screenshot skill. Work as a self-contained execution loop: inspect, edit, verify, screenshot, write QA, commit, push, and prepare PR. Do not stack CSS or duplicate elements. Replace old active sources. Use Lovable language and tokens. Remove internal public-language leaks. Use guarded plugin packaging. Do not ask questions unless credentials, spending, live deploy, or legal approval are required.
```

## Lovable sync rules

Lovable is an accelerator, not the live WordPress source.

Canonical Lovable hub:

- `https://github.com/The-new-ben/nadlan-strategy-hub.git`
- Import target in this repo: `handoff/lovable/2026-06-23-war-room-sync/`

Use Lovable for:

- Design direction.
- Tokens.
- Prototype behavior.
- Screenshots and visual reference.
- Reports and page IA.

Do not assume:

- Lovable React routes are live WordPress code.
- Lovable screenshots prove the WordPress implementation.
- Lovable labels are safe public copy.

When importing:

- Copy the exact handoff path.
- Commit source manifests and screenshots.
- Record the source repo, branch, and commit when known.
- Do not rewrite reports to look stronger than they are.

## WordPress implementation rules

- Prefer existing plugin modules and theme patterns.
- Keep one capability per plugin module.
- Use WordPress enqueue APIs.
- Escape output and sanitize input.
- Do not leak admin controls or internal labels to public screens.
- For RTL, use logical properties where practical.
- For Hebrew, use the approved fonts and copy rules.
- For English, verify LTR direction and line lengths.

WordPress enqueue reference: https://developer.wordpress.org/reference/functions/wp_enqueue_style/

## SEO and anti-cannibalization rules

NadLan competes across the full Israeli real-estate market and foreign-investor routes, but pages must be organized.

Rules:

- One search intent, one canonical URL.
- Money pages get protected by a canonical page registry.
- Supporting content links to the money page instead of competing with it.
- City pages, project pages, professionals, guides, and glossary pages need distinct intent.
- No article is published without internal-link targets and a cannibalization check.
- Foreign-investor pages need language, tax, FX, legal, project, and concierge structure.

Use:

- `skills/url-namespace-contract.md`
- `skills/internal-linking-hub-spoke.md`
- `skills/authority-eeat-program.md`
- `handoff/lovable/2026-06-23-war-room-sync/reports/03-listings-ia.md`
- `handoff/lovable/2026-06-23-war-room-sync/reports/00-strategy-brief.md`

## Admin strategy room

The owner needs visible, right-to-left, non-technical access to strategy outputs.

Future admin dashboard requirements:

- Show synced Lovable, Codex, and Claude reports.
- Show source repo, branch, commit, and date.
- Show keyword universe, page registry, cannibalization status, screenshot QA, release status, and next actions.
- Keep internal strategy private behind WordPress admin capability.
- Do not expose strategy-room language on public pages.

Build this after the showroom slice is complete.

## Research basis

Use these sources as the operating proof set:

1. OpenAI Codex best practices: reusable workflows should become skills and be scoped to one job. https://developers.openai.com/codex/learn/best-practices
2. OpenAI AGENTS.md guide: Codex reads project guidance files before work. https://developers.openai.com/codex/guides/agents-md
3. OpenAI Agent Skills: skills package instructions, resources, and scripts for reliable workflows. https://developers.openai.com/codex/skills
4. OpenAI non-interactive mode: Codex can run scripted tasks in automation and CI. https://developers.openai.com/codex/noninteractive
5. OpenAI CLI reference: `codex exec` supports scripted runs and working-directory control. https://developers.openai.com/codex/cli/reference
6. OpenAI hooks: deterministic scripts can be attached to lifecycle events, with trust review. https://developers.openai.com/codex/hooks
7. OpenAI difficult-problem iteration: inspect visual artifacts directly and loop with scoring. https://developers.openai.com/codex/use-cases/iterate-on-difficult-problems
8. WordPress `wp_add_inline_style`: inline CSS is printed after the stylesheet and in order. https://developer.wordpress.org/reference/functions/wp_add_inline_style/
9. WordPress `wp_enqueue_style`: enqueue and version styles explicitly. https://developer.wordpress.org/reference/functions/wp_enqueue_style/
10. MDN CSS cascade: source order, specificity, origins, and `!important` determine which rules win. https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Cascade/Introduction
11. Playwright screenshots: use browser screenshots as durable visual evidence. https://playwright.dev/docs/screenshots
12. Git hooks: pre-push hooks can block unsafe pushes with non-zero exit. https://git-scm.com/book/en/v2/Customizing-Git-Git-Hooks
13. WordPress sanitizing: validate and sanitize untrusted data. https://developer.wordpress.org/apis/security/sanitizing/
14. WordPress plugin handbook: use proper plugin architecture, hooks, security, and lifecycle rules. https://developer.wordpress.org/plugins/
15. WordPress agent skills by WordPress contributors: avoid outdated patterns, security misses, block deprecations, and ignored tooling. https://github.com/WordPress/agent-skills
16. AGENTS.md standard: use a predictable file for build commands, tests, style, and security notes. https://agents.md/
17. Blake Crosley: put build/test commands first, define done, escalation, and task sections clearly. https://blakecrosley.com/blog/agents-md-patterns
18. Brandon Payton for WordPress: agents work better with a clear feedback loop and WordPress runtime testing. https://wordpress.org/news/2026/01/new-ai-agent-skill/
19. Fellyph Cintra for WordPress Playground: structured Blueprint references reduce common agent schema mistakes. https://make.wordpress.org/playground/2026/04/02/teach-your-coding-agent-to-write-wordpress-playground-blueprints/
20. Jorge Rosal WordPress skills: plugin architecture, security, accessibility, testing, release engineering, WP-CLI, and Playground gates. https://github.com/jorgerosal/wordpress-skills
21. Nathan Onn agent skills: rough WordPress specs can become GOAL, VERIFY, and PROGRESS bundles for autonomous Codex. https://github.com/nathanonn/agent-skills
22. Tom Willmot WordPress.com Codex skill: verify access and use REST fallbacks when MCP writes are unavailable. https://github.com/willmot/wordpress-com-codex-skill
23. Joost de Valk: plugins should expose instructions and ability maps so agents do not treat them as black boxes. https://joost.blog/agent-ready-plugins/
24. Box developer blog: routing tables and progressive disclosure keep skills focused and reliable. https://blog.box.com/teaching-ai-agents-work-your-content-building-box-skill-openai-codex
25. Varun Dubey: scoped agents need purpose, constrained tools, exit conditions, and hard constraints. https://vapvarun.com/custom-ai-agents-wordpress-plugin-development-repo-tour/
26. Plugin Check article: use Plugin Check through Admin or WP-CLI for i18n, security, performance, and accessibility signals. https://dev.to/shahibur_rahman_6670cd024/deep-dive-ensuring-wordpress-plugin-quality-with-plugin-check-pcp-59e9
27. Composio Codex skills roundup: UI work needs real browser-flow verification. https://composio.dev/content/top-codex-skills

## Current active showroom rule

For the 1.69.x Lovable showroom port:

- Active CSS path must load the Lovable cream system as the primary showroom stylesheet.
- Old dark inline CSS stacks must not be enqueued before it.
- Footer CSS injections must not repaint the showroom after the primary stylesheet.
- Version must be 1.69.1 or later for the cream release.
- Screenshots must show cream, not dark teal or black.

## Revision log

- 2026-06-23 - Created by Codex after owner required autonomous execution, screenshot proof, no CSS or element stacking, and one consolidated skill file. Existing smaller skills remain active.
- 2026-06-23 - Added adopted Codex and WordPress skill pack from external research, including goal bundling, instruction chain, progressive disclosure, visual proof, Playground verification, plugin quality, security, performance, accessibility, release, REST, and abilities-map gates.
