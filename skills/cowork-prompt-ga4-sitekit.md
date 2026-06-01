# Cowork Prompt — wire GA4 via Google Site Kit (hands-on, obstacle-proofed)

> Single copy-paste for a fresh Claude Cowork session. Goal: get GA4 (G-G3QRV5646E) firing on every page of nad-lan.co.il through the already-active Google Site Kit plugin, finish the Search Console link, and verify. Cowork is hands-on (browser + WP admin). The ONE thing Cowork cannot do alone is the Google OAuth sign-in (owner's Google credentials) — the prompt handles that by pausing for the owner.

---

## COPY EVERYTHING BELOW THIS LINE → PASTE TO CLAUDE COWORK → SEND

```
COWORK TASK — WIRE GA4 ANALYTICS VIA GOOGLE SITE KIT
=====================================================

Goal: GA4 (Measurement ID G-G3QRV5646E, GA4 property 539731843, account "NadLan")
must fire on every public page of https://nad-lan.co.il, via the Google Site Kit
plugin that is ALREADY INSTALLED AND ACTIVE on the site. Then link Search Console
and verify. Do NOT hardcode a gtag snippet anywhere (Site Kit injects it; a second
copy would double-count). Do NOT bump the nadlan-config plugin for this.

CONTEXT YOU NEED (verify, don't assume):
- WP admin: use the URL + login the owner has configured. If you have a logged-in
  browser session to wp-admin, use it. If not, authenticate via the application
  password where REST suffices, but Site Kit setup needs the wp-admin UI + a Google
  OAuth flow (browser).
- Site Kit plugin slug: google-site-kit (confirmed active via
  GET /wp-json/wp/v2/plugins — status "active").
- GA4 already created (by the owner): account NadLan (396337110), property
  nad-lan.co.il (539731843), web data stream "nad-lan-main" (14981066845),
  Measurement ID G-G3QRV5646E. Time zone Israel/Jerusalem, currency ILS.
- Google Search Console: the nad-lan.co.il DOMAIN property is already verified
  (via DNS TXT). Site Kit should detect it.

STEP 0 — BASELINE CHECK (REST, cheap, do first)
  curl -s "https://nad-lan.co.il/" | grep -oE "G-[A-Z0-9]{6,}|GTM-[A-Z0-9]+"
  - If G-G3QRV5646E already appears → GA4 is ALREADY live. Jump to STEP 4 (verify
    + Search Console link). Do not re-add.
  - If nothing appears → continue to STEP 1.

STEP 1 — OPEN SITE KIT IN WP ADMIN (browser)
  Navigate to: <wp-admin-url>/admin.php?page=googlesitekit-dashboard
  - If Site Kit shows "Set up Site Kit" / not connected to any Google account:
      this requires the OWNER's Google sign-in (OAuth). YOU CANNOT enter the
      owner's Google password. → Go to OBSTACLE-A.
  - If Site Kit is already connected to a Google account (dashboard shows data
    or "Connect more services"): continue to STEP 2.

STEP 2 — CONNECT THE ANALYTICS MODULE
  Site Kit → Settings → "Connect more services" → Analytics → "Set up Analytics".
  - Site Kit will ask which GA4 account/property/stream to use. Choose:
      Account: NadLan (396337110)
      Property: nad-lan.co.il (539731843)
      Web data stream: nad-lan-main (14981066845)  [Measurement ID G-G3QRV5646E]
  - If it offers "let Site Kit create a new property" — DO NOT. Pick the EXISTING
    property above (creating a new one makes a second, empty GA4 = data split).
  - Enable the GA4 snippet placement ("Place Analytics code on your site" = ON).
  - Save / Configure. Site Kit now injects gtag on every page.
  - If a Google OAuth/permission screen appears mid-flow → OBSTACLE-A.

STEP 3 — CONFIRM SNIPPET PLACEMENT SETTING
  Site Kit → Settings → Analytics → ensure "Let Site Kit place code on your site"
  is enabled (not "I'll place it myself"). If the latter, switch to Site-Kit-placed
  so we don't need any theme/plugin edit.

STEP 4 — LINK SEARCH CONSOLE (the piece the GA4 dialog couldn't finish)
  Two places it can be done — do whichever is available:
  (a) Site Kit → Settings → Search Console: confirm property is
      nad-lan.co.il (Domain). Site Kit usually auto-connects this on setup.
  (b) In GA4 itself (analytics.google.com) → Admin → Property → Product Links →
      Search Console links → Link → pick nad-lan.co.il → pick web stream
      nad-lan-main → Confirm.
  - If the GA4 "select web stream" list is EMPTY (known propagation lag — the
    stream was created recently): wait 10 min and retry once. If still empty,
    leave it; it is non-blocking (GA4↔GSC reports have a 24-48h delay anyway).
    Log it and move on.

STEP 5 — VERIFY (must pass before declaring done)
  a) curl -s "https://nad-lan.co.il/" | grep -oE "G-G3QRV5646E"
       → must return G-G3QRV5646E (tag is live). Check 2-3 pages (home, an
         article, /join-pro/), not just home.
  b) Confirm only ONE GA4 tag (no duplicate). grep count of "G-G3QRV5646E"
       in page source should be the Site-Kit-injected pair (gtag.js src + config),
       not 2 separate independent installs. If you see a DIFFERENT G-id too,
       something else is tagging — report it.
  c) In GA4 → Reports → Realtime: open the site in another tab, confirm your
       visit appears (may take 30-60s). If you can't reach GA4 UI, skip; the
       on-page tag presence (5a) is the binding proof.

STEP 6 — (OPTIONAL, only if time) MARK KEY EVENTS
  In GA4 → Admin → Events → Mark as key event: 'generate_lead' (we'll emit this
  from the lead endpoint later), 'purchase' (Woo). Do NOT build custom event code
  now — just note in the report that lead-event wiring is a later task.

STEP 7 — REPORT + LOG
  Append a block to skills/site-state.md: GA4 wired via Site Kit (yes/no),
  Search Console linked (yes/no/pending-propagation), verification result
  (tag present on which pages), any obstacle hit. Commit + push to
  origin claude/charming-meitner-mwVEW.

============================ OBSTACLES (pre-solved) ============================

OBSTACLE-A — Site Kit needs Google OAuth sign-in (owner credentials)
  This is the ONE step you cannot do (you must not enter the owner's Google
  password). Options, in order:
  1. If the browser already has the owner's Google account signed in, the OAuth
     "Allow" screen may appear — you may click "Allow"/"Continue" to grant Site
     Kit access IF the correct account (the one owning GA4 property 539731843 /
     mistabrajustice@gmail.com) is already selected. Do NOT pick a different
     account. Do NOT type a password.
  2. If sign-in/password is required (no active session): STOP this step,
     post a clear message to the owner:
       "Site Kit needs you to connect your Google account once (the one that
        owns the GA4 property, mistabrajustice@gmail.com). Please: WP Admin →
        Site Kit → Sign in with Google → allow all requested scopes (Analytics
        + Search Console + PageSpeed). Takes ~90 seconds. Tell me when done and
        I'll finish wiring + verify."
     Then continue with any non-blocked work and resume STEP 2 after the owner
     confirms.

OBSTACLE-B — Site Kit offers to CREATE a new GA4 property
  Never accept. Always select the EXISTING property nad-lan.co.il (539731843).
  Creating new = a second empty property and split data. If the existing
  property doesn't appear in the picker, it's a permissions/propagation issue:
  confirm the signed-in Google account has Editor/Admin on property 539731843;
  wait 10 min; retry. If still absent, report to owner.

OBSTACLE-C — gtag already present (some other G-id, or Tag Manager)
  Earlier scans found NO G- tag on the site, but verify in STEP 0. If you find a
  DIFFERENT measurement ID or a GTM container injecting GA: do not remove it
  blindly; report what you found + where (which plugin/theme) and ask the owner
  before changing, to avoid breaking existing tracking.

OBSTACLE-D — Site Kit "code placed by another plugin" warning
  If Site Kit warns the GA tag is already placed elsewhere, find the source
  (Insert Headers/Footers plugin, theme option). Prefer letting SITE KIT own the
  tag; disable the other source. Verify single tag (STEP 5b).

OBSTACLE-E — WP admin login not available to you
  If you cannot reach wp-admin (no session, app-password insufficient for UI):
  you cannot complete Site Kit setup (it is a UI+OAuth flow). Post the STEP 1-5
  instructions to the owner as a numbered checklist they can do in ~5 minutes,
  and offer to verify (STEP 5a via curl) once they confirm. Do NOT attempt to
  brute-force or guess credentials.

OBSTACLE-F — Caching shows old (un-tagged) HTML
  If STEP 5a doesn't show the tag right after setup, purge cache (the site is
  behind nginx/UPress caching). Look for a cache-purge in WP admin (UPress / WP
  Super Cache / LiteSpeed). Re-check after purge. Allow 2-3 min.

============================ HARD RULES ============================
- Never enter the owner's Google password. OAuth is the owner's action if no
  session exists.
- Never create a new GA4 property; always use 539731843 / G-G3QRV5646E.
- Never hardcode gtag in the theme or nadlan-config plugin (double-count risk).
- Single tag only. Verify it.
- If blocked on OAuth, hand the owner the exact checklist and stop politely;
  don't burn cycles.

START: STEP 0 (curl baseline) → then proceed. End with STEP 7 report.
```

---

## Notes for the owner (you)

- The realistic outcome: if your Google account isn't already signed into Site Kit in the site's browser session, **Cowork will hit OBSTACLE-A and hand you a 90-second checklist** — connecting Site Kit to Google is an OAuth step only you can authorize. That's expected and safe; Cowork then verifies the tag is live.
- Fastest path of all: you do **WP Admin → Site Kit → Sign in with Google → connect Analytics → pick nad-lan.co.il (G-G3QRV5646E)** yourself (~2 min), then paste the prompt and Cowork just verifies + finishes the Search Console link.

_Created 2026-06-01 by Claude Code (claude-opus-4-8). GA4 via Site Kit = zero code, no plugin deploy, no double-tagging._
