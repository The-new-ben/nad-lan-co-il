# Guide A - Turn On The AI Concierge

Important truth for v1.51.0: the OpenAI adapter exists in code, but the visible Settings page and the live `/nadlan/v1/concierge` route are still Anthropic-first. A non-developer cannot fully turn on the live concierge with only an OpenAI key from the current wp-admin screen. Ask Claude to fix the OpenAI UI/route wiring before relying on OpenAI while travelling.

What works now:

- The current Settings page can store an Anthropic key.
- The healthcheck can report OpenAI provider/key state from `inc/ai-provider.php`.
- The live chat route still posts to the Anthropic messages endpoint from `inc/ai-concierge.php`.

## Safe Steps For The Current v1.51.0 UI

1. Open WordPress admin.
   `[SCREENSHOT: wp-admin dashboard after login]`

2. Go to Settings -> NadLan AI.
   `[SCREENSHOT: left admin menu with Settings expanded and NadLan AI highlighted]`

3. Look at the key field label.
   `[SCREENSHOT: NadLan AI page showing the password field and whether it says Anthropic API Key]`

4. If it says Anthropic API Key, do not paste an OpenAI key there.
   `[SCREENSHOT: key field with a red annotation "Anthropic field, not OpenAI"]`

5. For immediate live chat with the current UI, paste an Anthropic API key in the key field.
   `[SCREENSHOT: paste into the password field, value hidden]`

6. Tick the "active" checkbox.
   `[SCREENSHOT: active/enabled checkbox checked]`

7. Click Save.
   `[SCREENSHOT: Save button and success notice]`

8. Open `https://nad-lan.co.il/wp-json/nadlan/v1/healthcheck?cb=<current-time>`.
   `[SCREENSHOT: browser showing JSON healthcheck ai block]`

9. Confirm the AI block. For Anthropic, expect `anthropic_key_present:true`. For OpenAI after Claude fixes wiring, expect `provider:"openai"` and `openai_key_present:true`.
   `[SCREENSHOT: ai.provider, ai.openai_key_present, ai.anthropic_key_present, tokens_today, daily_token_cap_global]`

10. Open the public site in an incognito/logged-out browser and click the AI chat bubble.
    `[SCREENSHOT: public page with AI chat bubble open]`

11. Send a simple test message: `כמה מס רכישה על דירה ראשונה?`
    `[SCREENSHOT: chat message and answer]`

12. Recheck healthcheck and confirm today's token/spend counters changed if a real model call happened.
    `[SCREENSHOT: healthcheck ai.tokens_today and usage counters after test]`

## What Claude Must Fix For True OpenAI

1. Move/load `ai-provider.php` before `ai-concierge.php`, or make `ai-concierge.php` not define provider functions first.
2. Change `/nadlan/v1/concierge` to call `nadlan_ai_chat()` instead of posting directly to Anthropic.
3. Add visible Settings fields for provider (`openai`/`anthropic`), `nadlan_ai_openai_key`, global daily cap, per-IP daily cap, and today's usage.
4. Keep stored secrets hidden. The field should be blank after save and say "configured".

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| Healthcheck says `openai_key_present:false` | OpenAI key is not saved in `nadlan_ai_openai_key` or constant `OPENAI_API_KEY`. | Ask Claude to add the OpenAI field or set the option server-side. Do not commit the key to Git. |
| Chat says maintenance / not configured | Current chat checks for an Anthropic-style key through `nadlan_ai_enabled()`. | Use an Anthropic key temporarily or wait for the OpenAI route fix. |
| 401 from OpenAI | Wrong key, revoked key, or key has no API access. | Create a new OpenAI API key and save it only in wp-admin/server option after the UI fix. |
| Empty answer | Provider returned no message or upstream error. | Check Settings -> NadLan AI, healthcheck `ai.last_error` if exposed, and server logs. |
| Cost running too high | Daily caps are too high or bot is abused. | Lower global/per-IP caps once the OpenAI settings UI is fixed; verify `daily_token_cap_global` in healthcheck. |
