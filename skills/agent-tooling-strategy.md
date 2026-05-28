# Agent Tooling Strategy — who does what, using subscriptions not APIs

> **Notice to all agents:** the owner pays for: Claude Code (~$20/mo entry plan), ChatGPT Pro (highest tier), Google Gemini Ultra. The owner does NOT have separate API budgets for OpenAI, Anthropic, or Gemini. **Every workflow must run through an OAuth-logged subscription, not a pay-per-token API key.** Anything that requires `ANTHROPIC_API_KEY`, `OPENAI_API_KEY`, `GEMINI_API_KEY` is out of bounds unless explicitly approved.

## Right tool for right job

| Job | Tool | Why |
|---|---|---|
| Strategy, skill authoring, architecture, code review, high-stakes decisions | **Claude Code (this tool, $20 plan)** | Highest reasoning quality. Used sparingly — owner's credit-limited. **Not for bulk content writing.** |
| Bulk Hebrew article writing (spokes, city pages, neighborhood pages, blog posts) | **Codex CLI on the owner's PC, logged into ChatGPT Pro** | Owner already pays for ChatGPT Pro, no API charge. Codex has good Hebrew + can read repo files including `skills/strategy-master.md`. Codex previously produced acceptable content. |
| Visual content (logos, hero images, neighborhood mood photos) | **ChatGPT Pro image generation OR Gemini Ultra image generation** | Both bundled with subscriptions. No DALL-E API calls. Output flows through `image-pipeline.md` gate. |
| Browser-driven actions (clicking around WP admin, configuring Yoast, opening Google Search Console) | **ChatGPT Operator / Agent mode (Pro tier)** OR **Antigravity (Gemini agentic IDE)** | Both run autonomous browser sessions under the owner's subscription. **No API. No headless scripting that risks ToS.** |
| Research, web scanning, SERP checks | **Whichever agent is currently active.** Gemini Ultra has free Google-grounded search. ChatGPT Pro has browsing. Claude Code has WebSearch. | Already bundled; use whoever is "on" at the moment. |
| Local file operations on Windows (move generated images, batch rename) | **PowerShell scripts authored by Claude Code or Codex** | Scripts are free. Owner runs them locally. |

## The cardinal rule

**Claude Code is for the brain. Codex / ChatGPT Pro is for the hands. Antigravity / Gemini is the third pair of hands. Do not invert this.**

If a task is "write 50 spoke articles about מס רכישה variations" — that's Codex, not Claude.
If a task is "design the spoke architecture for מס רכישה and decide which 50 spokes are worth writing" — that's Claude, in one short session, output saved as a skill, then handed off.

## How an agent picks up where the last one stopped

This is the owner's explicit concern: agents redoing or undoing each other's work.

### The state file: `skills/site-state.md`

Last 5 blocks are the situation report. **Every agent reads them before starting.** Format is enforced by `AGENTS.md`.

### The content backlog file: `docs/content-backlog.md` (to be created by Codex on first run)

A flat markdown checklist of every piece of content the strategy calls for, with status flags. Codex maintains it. Example skeleton:

```markdown
# Content Backlog — nad-lan.co.il

## Pillars
- [x] /buying/ — DRAFT — codex 2026-05-25
- [ ] /selling/
- [ ] /investment/
- [ ] /mortgage/
- [x] /tax-legal/ — PUBLISHED — codex 2026-05-26
- [ ] /urban-renewal/

## Tools
- [ ] /tools/mortgage/ — needs JS calculator
- [ ] /tools/purchase-tax/ — needs JS calculator
- [ ] /tools/valuation/

## Cities (priority order)
- [ ] /cities/tel-aviv/
- [ ] /cities/jerusalem/
- [ ] /cities/haifa/
- [ ] /cities/rishon-lezion/
- ...

## Spokes — Tax & Legal pillar
- [ ] מס רכישה דירה ראשונה
- [ ] מס רכישה למשקיע
- [ ] מס שבח דירה יחידה
- [ ] פטור ממס שבח 2026
- ...
```

When Codex starts a session, it:
1. Reads `skills/site-state.md` (last 5 blocks).
2. Reads `docs/content-backlog.md`.
3. Reads `skills/strategy-master.md` to know what the next item should look like.
4. Reads `skills/copywriting-skill.md` for voice and forbidden phrases.
5. Picks the next unchecked item with no blocker.
6. Writes the content into the repo (Markdown for review, or directly as Page/Post via UPress sync).
7. Marks the item `[x] DRAFT` with date + agent name.
8. Appends a block to `skills/site-state.md`.
9. Commits and pushes.

### The handoff card

For Antigravity / ChatGPT-Operator running browser sessions (WP admin, GSC, Yoast), no commit to repo happens — those are live actions. So they get a different state-update protocol: they leave a comment in `skills/site-state.md` describing what they did in the browser, with timestamps and screenshots filenames stored in `docs/research/screenshots/YYYY-MM-DD/`.

## The "zero-friction self-service" vision

Owner's stated goal: professionals (lawyers, brokers, mortgage advisors, developers) sign up, choose a plan, pay, and start appearing on the site **without owner intervention**. Owner only sees money. This is buildable but it's a real product, not a config tweak.

### Phase 0 (now)
- WordPress + a paid `professional` CPT with manual approval workflow. Stripe Checkout for the subscription. Notification to owner who clicks "approve" once.

### Phase 1 (3-6 months in)
- Self-service onboarding wizard:
  1. Sign up with email + bar / broker license number.
  2. License validation (manual check by owner or — later — an automated lookup against the public bar / brokers registry).
  3. Choose plan, pay via Stripe.
  4. Fill profile form (photo, bio, cities, specialties).
  5. Auto-publish to the directory.
- Implementable in WordPress with **Paid Memberships Pro** + **Gravity Forms** + **Stripe**. No code needed for the basic version. Plugin licenses are real $$ — owner approves before purchase (per `agent-coordination-protocol.md`).

### Phase 2 (when traffic justifies it)
- Auto-lead routing: an inquiry from `/cities/tel-aviv/` for "buying" gets routed (1) to the owner's law practice intake, (2) to a featured tier-A subscriber broker in TA, (3) to a featured mortgage advisor — all in parallel, all paying per-lead.

### Phase 3 (the AI-owner vision)
- A scheduled agent (running on owner's PC via Codex CLI, or as a Vercel cron, or as a GitHub Action) that:
  - Pulls Google Search Console + GA4 daily.
  - Identifies underperforming pages (high impressions, low CTR).
  - Drafts a rewrite or new spoke as a PR.
  - Owner reviews / merges.
- Same agent monitors the inquiry queue and pings the owner when a high-value lead lands.

**This is a real architecture and it's doable on subscriptions, but not in week 1.** Building it = Phase 3 in `skills/strategy-master.md`.

## On PowerShell + OAuth subscriptions

The owner asked about writing PowerShell to use LLM agents with OpenAI subscription via OAuth. Honest take:

- **Sanctioned path:** OpenAI's own **Codex CLI** is the OAuth-logged-into-ChatGPT-account tool. It's official, supported, and works on Windows. The owner is already using it. **Use it.** Don't write a custom PowerShell wrapper.
- **For browser-driven agentic actions:** ChatGPT **Agent / Operator mode** (Pro tier) is the official sanctioned way. Or Antigravity for Gemini side. Both run inside the vendor's official infrastructure and respect the subscription.
- **Unofficial PowerShell scripts that scrape chat.openai.com or call internal endpoints with OAuth tokens** — risky. Likely violates OpenAI ToS, can get the account flagged. **Don't go there.**
- **What PowerShell IS useful for:** local file pipeline scripts — batch rename images, copy from `C:\Users\pro\.codex\generated_images` into the repo's `assets/images/`, run `git add` + `git commit` + `git push` on a schedule. Codex can write these scripts for the owner on request.

## TL;DR sequencing the agents

```
                 ┌──── Claude Code (this tool) ────┐
                 │ - strategy & architecture       │
                 │ - skill authoring & review      │
                 │ - high-stakes code              │
                 │ - sparingly used                │
                 └──────────┬──────────────────────┘
                            │ commits skills/, docs/
                            ▼
                 ┌──── Codex CLI on PC ─────────────┐
                 │ - reads skills/                  │
                 │ - bulk content (Hebrew)          │
                 │ - image generation + sorting     │
                 │ - PowerShell scripts             │
                 │ - daily/weekly                   │
                 └──────────┬──────────────────────┘
                            │ commits drafts, runs sync
                            ▼
                 ┌──── Antigravity / ChatGPT Operator ┐
                 │ - browser-driven WP-admin actions   │
                 │ - Yoast config clicks               │
                 │ - GSC sitemap submission            │
                 │ - on-demand                         │
                 └──────────┬─────────────────────────┘
                            │ logs back to site-state.md
                            ▼
                 ┌──── Owner ──────────────────────┐
                 │ - approves out-of-scope actions │
                 │ - sees money                    │
                 └─────────────────────────────────┘
```

## Open TODOs for next agent

- [ ] Codex (next run): create `docs/content-backlog.md` from `strategy-master.md` §2 (keyword clusters) and §4 (pillar architecture). Mark already-existing Pages as DRAFT or PUBLISHED. This becomes the source of truth for "what's the next article."
- [ ] Codex: write a PowerShell script `scripts/sync-images-to-repo.ps1` that scans `C:\Users\pro\.codex\generated_images`, prompts owner to tag images per the `image-pipeline.md` gate, then moves approved ones to `assets/images/`.
- [ ] Owner: confirm whether ChatGPT Pro Agent / Operator mode is the right tool for the browser-driven WP admin work, OR whether Antigravity is preferred (the choice affects which agent owns `site-state.md` updates).

---
_Created 2026-05-28 by Claude Code (claude-opus-4-7). Will not be touched again unless an agent or the owner has a substantive update — that's the rule from `README.md`._
