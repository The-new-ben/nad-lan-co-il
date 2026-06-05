# GAP 4 QA: OpenAI Provider Adapter

Scope: nadlan-config v1.43.2, `plugins/nadlan-config/inc/ai-provider.php`, `ai-concierge.php`, `ai-features.php`, `studio-rest.php`, `studio.php`.

## Instructions Read

- `AGENTS.md`: repo is source of truth; plugin code only reaches live through bumped ZIP + manifest on `main`.
- `BACKLOG.md`: AI concierge is a P4 zero-friction goal; revenue gaps are built one branch at a time.
- `skills/MAP.md`: mandatory deploy, honesty, security, copywriting, and plugin skills.
- `skills/site-state.md`: read the recent state trail; plugin is the runtime backbone.
- `skills/codex-plugin-access-and-deploy.md`: one branch, version bump, lint, ZIP, manifest, draft PR.
- `docs/2026-06-04-master-architecture-build-bible.md`: GAP 4 target is default OpenAI, Anthropic fallback, cost guard, graceful failure.
- `docs/2026-06-04-codex-implementation-spec.md`: `nadlan_ai_chat($system,$messages,$max_tokens)` adapter and settings page.
- Official OpenAI docs checked: [Chat Completions API](https://platform.openai.com/docs/api-reference/chat/create), [Text generation](https://platform.openai.com/docs/guides/text), [Migrate to Responses](https://platform.openai.com/docs/guides/migrate-to-responses), [Pricing](https://platform.openai.com/docs/pricing/).

OpenAI docs currently recommend Responses for brand-new apps, while Chat Completions remains supported. This PR keeps Chat Completions because the repo spec explicitly requires it and the existing WordPress code already passes chat-style message arrays.

## What Changed

- New `inc/ai-provider.php`:
  - `nadlan_ai_provider()` defaults to `openai`.
  - `nadlan_ai_chat()` is the shared text adapter.
  - OpenAI path posts server-side to `https://api.openai.com/v1/chat/completions` with `store=false`.
  - Anthropic path remains as a fallback only.
  - Global daily estimated token cap checked before the per-IP cap via `nadlan_ai_guard()`.
  - Per-IP daily estimated token cap as the second guard.
  - Monthly usage/cost counter in `nadlan_ai_usage_YYYYMM`.
  - Successful calls increment `nadlan_ai_tokens_today_YYYYMMDD` with autoload disabled.
  - Healthcheck exposes provider/key-present/usage metadata, never key values.
- Loader adds `ai-provider` before `ai-features`, `ai-concierge`, and `studio-rest`.
- `ai-concierge.php` now calls `nadlan_ai_chat()` instead of hard-coded Anthropic.
- `ai-features.php` keeps the old `nadlan_llm_request()` compatibility wrapper but delegates to `nadlan_ai_chat()`.
- `studio-rest.php` AI copy endpoint now uses the shared adapter.
- `studio.php` no longer tells advertisers to configure Anthropic specifically.
- Settings page now supports provider radio, OpenAI key, Anthropic fallback key, per-IP cap, global cap, today usage/cap, and usage display without printing stored secrets into password fields.
- OpenAI and Anthropic HTTP calls pin `sslverify => true`.

## 10-Cycle Proof

| Cycle | Result |
|---|---|
| C1 foundation | One shared adapter, loaded before all callers. |
| C2 idempotence | Settings saves overwrite options deterministically; usage counters only increment after calls/errors. |
| C3 security | Keys are server-side only; healthcheck returns booleans, not secrets; public errors do not expose upstream details. |
| C4 edge cases | Missing key, disabled AI, over daily cap, empty upstream response, and HTTP failures return `WP_Error` or clean 503 JSON. |
| C5 observability | Healthcheck `ai` object + `nadlan_ai_usage_YYYYMM` + `nadlan_ai_tokens_today_YYYYMMDD` + `nadlan_ai_last_error`. |
| C6 automation | Concierge, Studio AI copy, listing-description generator, and NL search all use the same provider switch. |
| C7 premium UX/copy | User-facing fallback text is Hebrew, no provider-specific dead-end copy, no internal "lead" wording in the prompt path. |
| C8 full journey | Visitor chat, advertiser Studio copy assist, admin property description, and NL search all share OpenAI default. |
| C9 deterministic proof | ZIP gates below verify the module, loader, OpenAI endpoint, fallback endpoint, and no direct provider calls outside the adapter. |
| C10 hardening | Global daily cap checked before per-IP cap, `sslverify => true`, `store=false`, request IDs on OpenAI calls, graceful no-key state. |

## Local Gates

PHP CLI is not available on this Windows machine (`php` not on PATH and no common local PHP install found), so PHP lint was not run locally. Claude must run `php -l` before merge.

Run after ZIP build:

```bash
unzip -l plugin-dist/nadlan-config-1.43.2.zip | head

unzip -p plugin-dist/nadlan-config-1.43.2.zip nadlan-config/nadlan-config.php \
  | grep -c "ai-provider"

unzip -p plugin-dist/nadlan-config-1.43.2.zip nadlan-config/inc/ai-provider.php \
  | grep -c -E "nadlan_ai_chat|api.openai.com/v1/chat/completions|store'\\s*=>\\s*false|sslverify|nadlan_ai_daily_token_cap_global|nadlan_ai_tokens_today_|nadlan_ai_guard|nadlan_ai_usage_"

unzip -p plugin-dist/nadlan-config-1.43.2.zip nadlan-config/inc/ai-concierge.php \
  | grep -c "nadlan_ai_chat"

unzip -p plugin-dist/nadlan-config-1.43.2.zip nadlan-config/inc/studio-rest.php \
  | grep -c "nadlan_ai_chat"
```

Expected:

- top-level ZIP entries start with `nadlan-config/`.
- loader count is at least `1`.
- `ai-provider.php` signature count is at least `5`.
- `ai-concierge.php` and `studio-rest.php` each include `nadlan_ai_chat`.

Provider isolation:

```bash
grep -R "api.anthropic.com" plugins/nadlan-config/inc
grep -R "api.openai.com/v1/chat/completions" plugins/nadlan-config/inc
```

Expected:

- `api.anthropic.com` appears only in `inc/ai-provider.php` as fallback.
- `api.openai.com/v1/chat/completions` appears only in `inc/ai-provider.php`.

## Live QA After Owner Update

1. Confirm version:

```bash
curl -s "https://nad-lan.co.il/wp-json/nadlan/v1/healthcheck?cb=$(date +%s)"
```

Expected: `"version":"1.43.2"` and an `ai` object with `provider:"openai"`, `daily_token_cap_global`, and `tokens_today`.

2. Missing-key graceful failure:

```bash
curl -s -X POST "https://nad-lan.co.il/wp-json/nadlan/v1/concierge" \
  -H "Content-Type: application/json" \
  -d '{"messages":[{"role":"user","content":"מתי כדאי לקחת עורך דין מקרקעין?"}]}'
```

Expected without key: HTTP 503 JSON with a clean Hebrew message, no fatal, no provider error text.

3. OpenAI configured path:

Owner action: WP Admin -> Settings -> NadLan AI -> Provider OpenAI -> paste API key -> Save.

Then rerun the same curl. Expected: `ok:true`, Hebrew answer, `usage.provider:"openai"`, usage counters increase.

4. Anthropic fallback:

Owner action: Provider Anthropic + fallback key. Expected: same endpoint still answers and `usage.provider:"anthropic"`.

## Known Honest Gaps

- I did not create or inspect an OpenAI key. The repo is public, and no local key exists.
- I did not run a live model request.
- PHP lint is pending because no PHP executable is available locally.
