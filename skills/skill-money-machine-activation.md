# Skill: Money-Machine Activation Runbook (any WordPress site)
Reusable pattern proven on nad-lan.co.il (2026-06-11).
1. SHIP DARK: every revenue feature behind an option flag (default off) + ONE master switchboard
   settings page listing all flags (critical: flag-gated screens can't host their own toggle).
2. HEALTHCHECK: a public JSON endpoint exposing version + per-feature enabled + live metrics.
   Every activation step is verified against it (append ?cb=timestamp to bypass cache).
3. ACTIVATION ORDER: update plugin -> generate API keys in the provider browser UI -> store keys in
   a PINNED Google Keep note ("<SITE> PROD KEYS - DO NOT DELETE") -> paste into settings -> flip
   flags ONE AT A TIME, lowest-risk first (UI helpers -> admin tools -> public flows -> AI -> automation),
   smoke test after each.
4. SMOKE per flag: a real end-user action (submit a lead) + healthcheck metric movement + inbox proof.
5. KNOWN TRAPS (hit them all on nad-lan): (a) <button type="submit" name="x_save"> WITHOUT
   value="1" never satisfies !empty($_POST['x_save']) -> page silently never saves; (b) wp_mail
   returns true but mail never arrives -> ALWAYS configure SMTP (WP Mail SMTP + Brevo/UPress relay
   + SPF/DKIM) and test to a real Gmail inbox; (c) provider plan gates (Morning API needs a paid
   tier); (d) manifest CDN caching delays update visibility ~3 min.
6. EVIDENCE: per-step PASS/FAIL/BLOCKED table + final healthcheck JSON + key-storage note name.
