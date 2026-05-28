# WordPress 7.0 Abilities API — `nadlan/*` registrations

> **Notice to all agents:** WordPress 7.0 (released 2026-05-20) ships the Abilities API as a first-class core feature. The live site at nad-lan.co.il is running WP 7.0 with this API exposed at `/wp-json/wp-abilities/v1/abilities`. The functions.php in this theme **registers four `nadlan/*` abilities** so any AI agent (Codex, ChatGPT Operator, Antigravity, Claude) can introspect what the site can do, without that agent needing to read the codebase.

## What is the Abilities API

Standardized registry by which plugins, themes, and core declare machine-readable capabilities. AI agents query a single endpoint and get a structured list of what's possible: name, label, description, input schema, output schema, who can execute it.

This replaces the "agent reads PHP source and guesses what hooks exist" problem with "agent reads a JSON catalog."

## Public endpoint

```
GET https://nad-lan.co.il/wp-json/wp-abilities/v1/abilities
```

Returns at minimum:
- `core/get-site-info` (WP core)
- `core/get-environment-info` (WP core)
- `yoast-seo/get-seo-scores` (Yoast SEO plugin)
- `yoast-seo/get-readability-scores` (Yoast SEO plugin)
- `nadlan/get-pillars` (this theme — added 2026-05-28)
- `nadlan/get-calculators` (this theme)
- `nadlan/get-cities` (this theme)
- `nadlan/get-lead-stats` (this theme; requires `manage_options`)

## Abilities we registered

### `nadlan/get-pillars`
Returns the slugs, Hebrew titles, and URLs of the pillar pages defined in the nad-lan content strategy (buying, selling, investment, mortgage, tax-legal, urban-renewal, professionals, new-projects, commercial). Uses `get_page_by_path()`, so it auto-omits pillars that aren't published yet. Public.

### `nadlan/get-calculators`
Returns the slugs and URLs of the five calculator pages: mortgage, purchase-tax, valuation, investment cashflow, total purchase cost. Public.

### `nadlan/get-cities`
Returns all published Pages whose slug ends in `-apartment-prices` or `-house-prices`. Currently surfaces the 11 Tel Aviv-area pages Codex created. Public.

### `nadlan/get-lead-stats`
Returns count of `nadlan_lead` CPT entries in the last 7 / 30 / 90 days. **Permission-gated** (`manage_options`) so unauthenticated/non-admin callers get nothing. Never exposes PII.

## How a future AI agent should use this

Typical agent loop (Codex, Antigravity, or a future Claude session):

1. `GET /wp-json/wp-abilities/v1/abilities` to discover what's possible.
2. For each `nadlan/*` ability, read the `description` to understand the business meaning.
3. Call the ability via its registered endpoint to fetch live data.
4. Reason over the live data against `skills/strategy-master.md` to decide next actions.
5. Take action (write to the repo, commit, ask the owner to deploy).
6. Update `site-state.md`.

This is how the "AI-managed website" loop closes without API keys: the agent calls public WordPress endpoints, the agent's reasoning is paid for by the agent's subscription (ChatGPT Pro, Gemini Ultra, Claude plan), and the site exposes only what we authorize via abilities.

## Adding a new ability — checklist

In `functions.php`, inside `nadlan_revenue_register_abilities()`:

```php
wp_register_ability(
    'nadlan/<name>',
    array(
        'label'              => __( 'Short label', 'nadlan-revenue' ),
        'description'        => __( 'Plain-English: what does this do, when would an agent call it, what does it return.', 'nadlan-revenue' ),
        'input_schema'       => array( 'type' => 'object', /* JSON schema */ ),
        'output_schema'      => array( 'type' => 'object', /* JSON schema */ ),
        'execute_callback'   => 'nadlan_revenue_ability_<name>',
        'permission_callback' => '__return_true', // or current_user_can(...)
    )
);
```

Then implement `nadlan_revenue_ability_<name>()` and document it here.

## What we will NOT register as abilities

- Anything that exposes PII of leads, members, or visitors.
- Anything that takes destructive action without a separate confirmation step (do not register `nadlan/delete-page`).
- Anything that costs the owner money on invocation (no `nadlan/buy-stock-photo`).
- Anything that bypasses the owner's review of public-facing copy (do not register `nadlan/publish-article`).

The Abilities API is for READS by AI agents. Write actions go through the regular owner-reviewed pipeline (commits to the repo, owner activates, owner clicks publish).

## Open TODOs for next agent

- [ ] Add `nadlan/get-content-backlog` once `docs/content-backlog.md` exists. Returns the list of unwritten pillar/spoke targets so an agent can pick the next priority.
- [ ] Add `nadlan/get-yoast-status` returning per-page cornerstone/score data — possibly chains to `yoast-seo/get-seo-scores`.
- [ ] Add `nadlan/get-recent-google-search-console` once Site Kit confirms GSC connection and we wire it (Site Kit exposes its own REST data; an ability could wrap it).
- [ ] When the `professional` CPT exists (Phase 1 of the self-service vision in `agent-tooling-strategy.md`), add `nadlan/get-professionals`.

---
_Created 2026-05-28 by Claude Code (claude-opus-4-7)._
