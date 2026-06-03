# QA Journey Testing — the Cowork end-to-end smoke-test script

> **What this is.** A complete, paste-ready script for **Claude Cowork** to run
> persona-based, end-to-end journey QA on nad-lan.co.il, document every obstacle,
> and feed structured results back so Claude (code) can fix them and we re-run the
> loop until the site converts flawlessly. Reusable on every site in the network
> (🟪 DNA) — swap the personas + journeys per site.
>
> **Who runs it:** Cowork (browser + can write to the repo). **Who fixes:** Claude
> (plugin/theme code). **Who closes the loop:** the owner reviews the run report.
>
> **Method basis (real standards, cited):** Session-Based Test Management (SBTM,
> Jonathan & James Bach) + persona-based exploratory testing + smoke-testing with
> predefined success cutoffs. Charter-guided sessions find **40–60% more
> actionable bugs** than unguided clicking (BBST research). Sources at the bottom.

---

# ═══════════════════════════════════════════════════════════
# PART A — PASTE THIS TO COWORK (the operating brief)
# ═══════════════════════════════════════════════════════════

> Cowork: you are the **QA lead** for nad-lan.co.il. Your job is to *be* five
> different customers, walk their full journey in a real browser, push every
> button, hit the obstacles, and write down exactly what broke. You do NOT fix
> anything — you document. Claude (code) fixes. Then you re-run.
>
> **Rules of engagement (SBTM):**
> 1. Work in **time-boxed sessions of 60–90 minutes**, one persona per session.
> 2. Each session has a **charter** (the mission) — stay focused on it, but
>    follow the software where it leads.
> 3. **Log every action** as you go, so any bug can be reproduced. A bug nobody
>    can reproduce gets ignored.
> 4. Test on **mobile (390px) AND desktop**. Most of our traffic is mobile.
> 5. For each step record: ✅ pass / ⚠️ friction / ❌ blocker, + a screenshot.
> 6. **Predefine the success cutoff** before you start (each journey lists its
>    "DONE = " bar). If you don't hit it, the journey FAILS — say so plainly.
> 7. Use the **honesty statement**: no sugar-coating. A broken thing is broken.
>
> **Where to write results:** create one file per session at
> `docs/qa/QA-RUN-<YYYY-MM-DD>-<persona-slug>.md` using the template in PART D,
> commit it to a branch `cowork/qa-run-<date>`, and open a PR titled
> `QA run <date> — <persona>`. Also drop a 5-line summary in `BACKLOG.md` under a
> new `## QA findings <date>` heading. If the owner prefers Google Drive, also
> export the same markdown to the shared Drive folder — but the **repo file is
> the source of truth** Claude reads from.
>
> **The loop:** you run → you document in the repo → Claude triages + fixes +
> ships a new plugin version → owner updates → you RE-RUN the same charters →
> mark each prior bug FIXED / STILL-BROKEN / REGRESSED. Repeat until a full run
> is all ✅.

---

# ═══════════════════════════════════════════════════════════
# PART B — THE PERSONAS (be these people)
# ═══════════════════════════════════════════════════════════

Each persona has a name, a mindset, a device, and an emotional state. **Act the
mindset** — a tire-kicker rage-taps; a demanding advertiser expects luxury.

### P1 — "דנה", the tire-kicker buyer (mobile, impatient, skeptical)
A 34-year-old looking to buy a first apartment. Distracted, on her phone, 3
other tabs open. She pushes everything, trusts nothing, and will leave in 20
seconds if confused. **Goal: see if the site earns her attention + a lead.**

### P2 — "יעל", marketing manager of **"פרויקט רֵיינבּוֹ"** (the demanding advertiser — THE BIG ONE)
Marketing manager for a יזם launching a תמ"א 38 / new-build project "רֵיינבּוֹ".
She has budget and wants to advertise the project on our site. She is the
**worst/best customer in the world**: she wants premium placement, she wants
photos, she wants to know **how many people will see it (impressions)**, she
wants to be #1, she asks the concierge hard questions, she expects a flawless
paid checkout, then she wants to **upgrade** for even more exposure, and she
wants a **report** of results. If anything feels less than world-class, she
walks to Madlan. **Goal: she advertises רֵיינבּוֹ flawlessly + feels premium.**

### P3 — "משה", a contractor (kablan) who googled himself (desktop, suspicious)
Finds his auto-imported card from רשם הקבלנים. Asks "who made this? is my data
right? can I control it?" **Goal: claim card → 30-day Pro trial → add photos →
consider upgrading.**

### P4 — "אבי", the lead-seeker (mobile, transactional)
Wants a mortgage and a lawyer. Uses a calculator, then wants a human.
**Goal: become a routed, tracked lead that reaches a preferred partner.**

### P5 — "the adversary" (anyone trying to break it)
Submits garbage, double-clicks, empty forms, 1-char inputs, emoji, very long
text, rapid repeat submits, hits the back button mid-checkout, rotates the
phone, switches network. **Goal: find the cracks before a real user does.**

---

# ═══════════════════════════════════════════════════════════
# PART C — THE JOURNEYS (charters, broken into tiny steps)
# ═══════════════════════════════════════════════════════════

For EVERY step: note the **intent** (why a real person does this), do it, record
✅/⚠️/❌ + screenshot. Bold **DONE =** lines are the predefined success cutoff.

## ───────────────────────────────────────────
## JOURNEY 1 — דנה, tire-kicker buyer (mobile)
## Charter: "Land cold on a money page, try to understand the site, push everything, decide whether to leave or convert."
## DONE = she either (a) submits a lead via a CTA, OR (b) we can name the exact step she bailed and why.
## ───────────────────────────────────────────

1. **Intent: arrived from a Google search for "מס רכישה 2026".** Open
   `https://nad-lan.co.il/` on a 390px mobile viewport. Record: load time, does
   anything jump/shift (layout shift), is there a popup (there should NOT be —
   they were removed in v1.40.3; if one appears, ❌).
2. **Intent: "what is this site?"** Read the hero in 5 seconds. Can she tell what
   the site does + what to do next? Screenshot. ⚠️ if unclear.
3. **Intent: "find the tax answer."** Look for a purchase-tax calculator / guide.
   Navigate to it. Does it exist, load, compute? Enter a sample (apartment
   ₪2,000,000, first home). Record the result + whether it's believable.
4. **Intent: "who can help me?"** Tap into `/professionals/`. Filter by עיר
   (type "תל אביב") + profession (עו״ד). Do results update? Count them. ❌ if
   "0 results" when results clearly exist; ⚠️ if filter feels slow/janky.
5. **Intent: "is this contractor legit?"** Open one professional profile. Is
   there a trust badge (רשם הקבלנים)? A rating area? A "request a quote" button?
   Screenshot.
6. **Intent: "I have a question."** Open the AI concierge (floating chat). Ask in
   Hebrew: *"כמה מס רכישה משלמים על דירה שנייה ב-3 מיליון?"* Record the answer
   quality, latency, whether it links to a page, whether it tries to capture her.
   ⚠️ if the concierge is off (no API key) — note "concierge inactive".
7. **Intent: "I'm losing interest."** Scroll fast, tap back, tap around. Does
   anything trap her or break? (No exit-popup should fire.)
8. **Intent: "ok, maybe."** Find the easiest way to leave her details. Tap
   "request a quote" on a profile OR the WhatsApp button. Fill name+phone.
   Submit. Record: success message? Where does it say it went?
9. **VERIFY (Cowork → owner): the lead arrived.** Confirm the owner's `💰 Lead
   Inbox` (wp-admin) shows the new lead within 2 min. (Ask the owner or check if
   you have admin access.) ❌ if it never arrives.
10. **DONE check.** Did she convert (lead submitted + received) OR can you name
    the exact bail step + reason? Write the verdict.

## ───────────────────────────────────────────
## JOURNEY 2 — יעל / פרויקט רֵיינבּוֹ, the demanding advertiser (THE BIG ONE) — mobile + desktop
## Charter: "A funded marketing manager wants to advertise her project on our site, with photos and exposure data, pay, then upgrade for more. Make her feel this beats Madlan/Yad2 — or document every place it doesn't."
## DONE = she reaches a COMPLETED paid project-campaign checkout (₪3,990 product 489) with a clear promise of placement + exposure reporting, AND every question she asked got a real answer. Any dead-end = ❌ and the journey FAILS.
## ───────────────────────────────────────────

1. **Intent: "where do I advertise my project?"** From the homepage, try to find
   "advertise your project / הצטרפו כיזם". Time how long it takes. ❌ if there's
   no obvious path (this is a money path — it must be findable in ≤2 taps).
2. **Intent: "what do I get and what does it cost?"** Reach `/join-pro/`. Is the
   project-campaign offer (₪3,990) clear? Does it state **what she gets**
   (placement, duration, exposure)? Screenshot the offer. ⚠️ if value is vague.
3. **Intent: "how many people will actually see it?"** Look for any exposure/
   traffic promise or stats ("X views/month", "Y בעלי מקצוע"). Marketing managers
   demand this. Record what exposure proof exists. ⚠️/❌ if there's none — note
   "no exposure data shown; advertiser cannot judge ROI" (this is a known gap —
   document it, don't skip it).
4. **Intent: "I have questions before I pay."** Open the concierge and ask, one
   at a time: (a) *"כמה זמן הקמפיין רץ?"* (b) *"אפשר להעלות תמונות של הפרויקט?"*
   (c) *"איך אדע כמה אנשים ראו את המודעה?"* (d) *"מה ההבדל בין Pro ל-Premier?"*
   Record each answer + whether it was correct/helpful. ❌ for any question the
   concierge can't answer at all.
5. **Intent: "let me see where my project would appear."** Browse `/projects/`.
   Does it look premium? Are there colour pills, filters, real project cards?
   Would a sponsored card stand out? Screenshot. Compare honestly to a Madlan
   project page (open madlan.co.il in another tab) — write 3 bullets: where we
   win, where we lose.
6. **Intent: "I'll buy the campaign."** Add the ₪3,990 project-campaign (product
   489) to cart → checkout. Record EVERY field. Is it one-page or multi-step?
   (Single-page converts better — note which it is.) Try the `FIRSTMONTHFREE`
   coupon — does it apply/err correctly?
7. **Intent: "pay."** Reach the Green Invoice (Morning) payment step. **Use a
   test/real card per the owner's instruction** — do NOT complete a real charge
   unless the owner explicitly says to. Record: does the gateway load? Is it
   Hebrew? Does it offer Bit / Google Pay / Apple Pay? Screenshot the pay page.
   ❌ if the gateway errors or never loads.
8. **Intent: "did it work?"** After payment (or test), is there a clear
   confirmation + an invoice (חשבונית) from Morning? Does she now know what
   happens next (when/where her project appears)? ⚠️ if the post-payment "what
   now?" is unclear — advertisers panic without it.
9. **Intent: "now I want MORE exposure — upgrade."** Look for an upsell to a
   bigger package / featured placement / Premier. Can she upgrade? Record the
   path. ⚠️/❌ if there's no upgrade path after paying.
10. **Intent: "show me my results."** Look for ANY advertiser dashboard / report
    ("your project got X views / Y leads"). Record what exists. (Known gap —
    document precisely what a world-class advertiser report would need: impressions,
    clicks, leads, position, period.)
11. **Intent: "upload my project photos."** Try to attach images to her project.
    Can she? How? ❌/⚠️ — document the exact mechanism or its absence. (We
    discussed image generation as a future item — note current reality.)
12. **DONE check.** Did she complete a paid campaign with a clear placement +
    exposure promise, and get every question answered? List every ❌ and ⚠️ in
    priority order — these are the highest-value fixes in the whole site.

## ───────────────────────────────────────────
## JOURNEY 3 — משה, contractor claiming his card (desktop)
## Charter: "A contractor finds his auto-imported card, verifies his data, claims it, starts the trial, adds value, considers paying."
## DONE = he submits a claim request AND it lands in the owner's inbox; bonus if he reaches a paid upgrade.
## ───────────────────────────────────────────

1. **Intent: "is my business on here?"** Search the directory for a real
   contractor name (pick any from `/professionals/`). Open the profile.
2. **Intent: "is my data right?"** Check the registry number, classification,
   city. Is the source cited (gov.il)? ⚠️ if data looks wrong/garbled.
3. **Intent: "this is mine — give me control."** Find the "זה הכרטיס שלכם?"
   claim prompt. Tap it. Fill name+email+phone. Submit.
4. **Intent: "what do I get?"** Does it clearly promise the 30-day Pro trial?
   Record the message.
5. **VERIFY: claim request reached the owner** (`💰 Lead Inbox` / pending claims).
6. **Intent: "make my card better."** Look for how he'd add photos / edit. Record
   the path (or its absence — claimed-card editing may need owner approval first).
7. **Intent: "get me to the top."** Find the upgrade CTA on his profile (the
   "you're at position #X" upsell). Does it show a position? Tap upgrade → cart.
8. **DONE check.** Claim submitted + received? Upgrade path clear? Verdict.

## ───────────────────────────────────────────
## JOURNEY 4 — אבי, lead-seeker → preferred partner (mobile)
## Charter: "A buyer uses a tool, then wants a human pro; the lead must route to a preferred partner and be tracked."
## DONE = a lead is created AND (if a preferred partner exists for that profession) a partner-routed email is sent + the referral is logged.
## ───────────────────────────────────────────

1. **Intent: "what's my mortgage?"** Use the mortgage calculator. Get a result.
2. **Intent: "I want a real advisor / lawyer."** Trigger a quote/lead with a goal
   that mentions a profession, e.g. *"אני צריך עורך דין מקרקעין"*.
3. **Intent: submit** name+phone. Record success.
4. **VERIFY (owner side):** the lead appears in `💰 Lead Inbox`; if the owner has
   added a preferred partner for עו״ד, confirm the partner-routed email fired and
   a `nadlan_referral` was logged. ❌ if routing silently drops.
5. **DONE check.** Verdict + the meta on the lead (`matched_profession`,
   `preferred_routed`).

## ───────────────────────────────────────────
## JOURNEY 5 — the adversary (break it)
## Charter: "Try to break every form and flow a real frustrated/malicious user might."
## DONE = a list of everything that broke or behaved badly under abuse.
## ───────────────────────────────────────────

1. Submit every form **empty** → expect a clean validation message, not a crash.
2. Submit name="א" (1 char), phone="123" → expect rejection or graceful handling.
3. Paste 5,000 characters into a text field → expect truncation, not a 500.
4. Put `<script>alert(1)</script>` and `'; DROP TABLE` into fields → expect it
   sanitized, never reflected/executed.
5. Double-tap submit 5× fast → expect ONE lead, not five (rate-limit works?).
6. Start checkout, hit browser Back, retry → expect no broken cart/double charge.
7. Rotate phone portrait↔landscape on the directory + a profile → expect no
   overflow/clipping.
8. Open the concierge, send 12 messages fast → expect the rate-limit message, not
   a crash or runaway cost.
9. Hit a renamed-old glossary URL (Hebrew slug) → expect a 301 to the new Latin
   URL, not a 404.
10. **DONE check.** Every abuse either handled gracefully or logged as a ❌.

---

# ═══════════════════════════════════════════════════════════
# PART D — SESSION REPORT TEMPLATE (Cowork fills one per journey)
# ═══════════════════════════════════════════════════════════

Save as `docs/qa/QA-RUN-<YYYY-MM-DD>-<persona-slug>.md`:

```markdown
# QA Session Report — <Persona> — <YYYY-MM-DD>

- **Charter:** <the mission, copied from PART C>
- **Tester:** Cowork
- **Duration:** <start–end, minutes>
- **Devices:** mobile 390px / desktop <browser>
- **Live plugin version at test time:** <from /wp-json/nadlan/v1/healthcheck>
- **DONE cutoff:** <the predefined bar for this journey>
- **VERDICT:** ✅ PASS / ❌ FAIL  — <one sentence>

## Step log
| # | Intent | Action | Result ✅/⚠️/❌ | Screenshot | Note |
|---|---|---|---|---|---|
| 1 | ... | ... | ⚠️ | shot-01 | ... |

## Bugs found (one block each — must be reproducible)
### BUG-<persona>-01 · severity: blocker/major/minor/cosmetic
- **Where:** <URL + device>
- **Steps to reproduce:** 1… 2… 3…
- **Expected:** …
- **Actual:** …
- **Screenshot:** <link>

## Friction (not bugs, but hurts conversion)
- …

## Where we WIN vs Madlan/Yad2/Nadlanmaster (be honest)
- …
## Where we LOSE (be honest)
- …

## Top 3 highest-value fixes from this session
1. …
```

---

# ═══════════════════════════════════════════════════════════
# PART E — SEVERITY + ACCEPTANCE BAR (so we agree what "done" means)
# ═══════════════════════════════════════════════════════════

**Severity:**
- **Blocker** — a money path is dead (can't pay, can't submit, page 502/404 on a
  journey step). Fix before anything else.
- **Major** — journey completes but with real friction or wrong data.
- **Minor** — annoyance, cosmetic-but-noticeable.
- **Cosmetic** — polish.

**Acceptance bar for "the site converts flawlessly" (our predefined cutoff,
per smoke-test best practice — define it BEFORE testing):**
- Journeys 1–4 each reach their **DONE =** line with **zero Blockers**.
- The advertiser journey (J2) reaches a completed paid checkout with a clear
  placement + exposure promise.
- Every lead/claim submitted **arrives** in the owner's `💰 Lead Inbox`.
- The adversary journey (J5) produces **no 500s / no double-charges / no XSS**.
- Mobile: no horizontal overflow, no layout jump, no surprise popup.

A run that meets all of the above = ✅ ship-grade. Anything less = we fix the
Blockers/Majors and re-run (the circle).

---

# ═══════════════════════════════════════════════════════════
# PART F — THE LOOP (how the circle closes)
# ═══════════════════════════════════════════════════════════

1. **Cowork** runs a session → writes the report to `docs/qa/` → opens a PR →
   appends a 5-line summary to `BACKLOG.md` under `## QA findings <date>`.
2. **Claude (code)** reads the report, triages each bug by severity, fixes the
   Blockers/Majors, ships a new plugin version (verified in the ZIP), tells the
   owner to Update.
3. **Owner** updates the plugin + reviews the report.
4. **Cowork** re-runs the SAME charters → marks each prior bug
   FIXED / STILL-BROKEN / REGRESSED.
5. Repeat until a full run is all ✅ across J1–J5. Then we raise the bar (harder
   personas, more cities, edge devices).

---

## Sources (the standards this script is built on)
- Session-Based Test Management (charters, time-boxed sessions, session reports;
  40–60% more bugs when charter-guided):
  [PractiTest — exploratory & session-based tests](https://www.practitest.com/help/test-planning-and-execution/tests/exploratory-and-session-based-tests/),
  [Tricentis — creating an exploratory testing charter](https://www.tricentis.com/blog/creating-an-exploratory-testing-charter),
  [Yuri Kan — test charter writing](https://yrkan.com/blog/test-charter-writing/),
  [TestRail — exploratory testing techniques](https://www.testrail.com/blog/perform-exploratory-testing/).
- Persona-based / customer-journey testing:
  [QASource — CX testing 2026 guide](https://www.qasource.com/blog/a-complete-guide-to-customer-experience-testing),
  [TestRiq — persona-based testing](https://www.testriq.com/blog/post/persona-based-testing-enhancing-qa-with-real-user-simulation),
  [Applause — customer journey testing FAQs](https://www.applause.com/blog/customer-journey-testing-faqs-answered/),
  [Testlio — customer journey testing](https://testlio.com/blog/customer-journey-testing/).
- Smoke testing with predefined success cutoffs + landing/checkout expectations:
  [CXL — guide to smoke testing](https://cxl.com/blog/smoke-test/),
  [Bundl — validate purchase intent](https://www.bundl.com/articles/techniques-validating-purchase-intention-in-4-easy-steps-the-smoke-test),
  [VWO — ecommerce A/B testing elements](https://vwo.com/blog/ecommerce-ab-testing/),
  [Unbounce — ecommerce testing guide](https://unbounce.com/a-b-testing/ecommerce-testing/).

## Revision log
- 2026-06-03 — Created (Claude). Built from web research of SBTM, persona-based
  exploratory testing, and smoke-test acceptance practice (sources above). Five
  personas incl. the "Rainbow Project" demanding advertiser; five journey charters
  with micro-steps + intent; session-report template; severity + acceptance bar;
  the fix→re-run loop. Portable DNA — reuse on jus-tice / hea-lth / travel sites
  by swapping personas + journeys.
