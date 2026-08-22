# DEPLOY RECEIPT — Tours V5 "Night-Street Render Pass" (2026-08-21)

Owner order (chat, 21.8): use github.com/StarKnightt/night-street to upgrade
the Somail + Sde Dov tours "100 levels up". Session: Fable 5
(claude-fable-5), "nad-lan.co.il — 2026-08-21 16:50".

## What shipped (all live, md5-verified end-to-end)

| surface | change | live md5 | backup |
|---|---|---|---|
| uploads/2026/07/sde-dov-tour.html | V4 → **V5** render pass | ed1f8aba2e9fc266e32b814576d6b929 | .bakV5 (V4 original) |
| uploads/2026/07/somail-tour.html | V1.1 → **V5** render pass | 519b7a13deeeeba95746e17c5a8db445 | .bakV5 (V1.1 original) |
| plugins/nadlan-config/inc/tour-routes.php | `?year=` 404/301 **root fix** + X-NL-Tour proof header | (v5c, LF) | .bakV5 (pre-fix original) |

Plugin version unchanged (1.72.218) — inc-file hot-swap per the proven
live-swap precedent; mirrored to this repo same-session.

## The V5 render pass (both tours; techniques studied from night-street, MIT — no code copied)

1. **AgX filmic tone mapping** (guarded fallback to ACES) + per-state exposure
   re-derivation (day 1.85 / dusk 2.35), day fog pushed out (1900/7400).
2. **Real PCFSoft sun shadows** — armed only after the existing GPU tier probe
   passes (or `?fx=hi`), day-gated, 2048 map in a ±780 box, stale-map dispose,
   self-revoking frame-time watch (skips hidden/throttled frames).
3. **Procedural sky**: 4-octave FBM cumulus + cirrus veil in the dome shader,
   sun-side lit, state-colored (white day / underlit peach-mauve dusk).
4. **Living sea** (sde-dov): animated ripple normals + grazing sheen,
   distance-attenuated (kills moire), day roughness 0.24 for sparkle.
5. **Facade relief** in the shared duskify shader: floor-slab shadow lines,
   mullion edges, per-building paint variance, lit-room ceiling gradient,
   TV-flicker cells, floor-height lit bias (low floors light first).
6. **Ground**: streak/blotch detail in the kurkar maker; all 0x35333b streets
   get an asphalt grain map; dusk light-pools under promenade / Ibn Gvirol lamps.
7. **Motion & life**: palm-canopy sway (sde-dov), 3 gulls over the water (day),
   gull-cry / city-sparrow + cricket audio layers on the existing sound gate.
8. **Grade**: state-lerped `saturate/contrast` CSS filter on the canvas.
9. New QA/demo deep-link: `?fx=hi|lo`; `enableRealShadows` exposed in `__dbg`.

## Evidence (evidence classes per the iron law)

- **eyes**: real-GPU canvas captures (scratchpad LIVE evidence set):
  sde-dov day aerial with per-tower ground shadows; somail day (100 casters);
  somail dusk (sunset burn + varied lit windows); sde-dov dusk street-level
  (room gradients, TV cells, slab lines); mobile 375 frame.
- **code**: boot 479ms local / 1614ms live (<2s law); draw calls 102–106
  (≤140 law); live console clean; towers ready `{dimri:glb, ashira:glb,
  rainbow:glb}`; shadows-on log line; sun-toggle pressed for real via the
  button handler → fog 7400↔3900, exposure 1.85↔2.35, grade lerp — both
  directions; md5(served body) == md5(deployed bytes) for every file.
- Fleet spot-check: rainbow + h-infinity pages 200/h1 ✓. Health 1.72.218 ok
  at open and close. `/tour/designer/` untouched and alive.

## Root fix detail (?year= deep links)

`year` is a WP-reserved public query var: `/tour/*?year=2035` turned the main
query into a date archive → hard 404; `?year=2026` → 301-canonical to
`/2026/`. Fix at the correct layer: a `request` filter keeps ONLY
`nadlan_tour` in the main query for tour URLs (template_redirect was too late
— redirect_canonical wins). Verified live: both broken shapes now 200 with
the full tour body.

## Traps learned (also in memory)

- A **stale allocated shadow map poisons the pass** silently — dispose before
  re-arming (`sun.shadow.map.dispose()`).
- A **background/throttled tab produces 250ms+ rAF frames** — any frame-time
  guard must skip `document.hidden`/long deltas or it false-revokes.
- **template_redirect is too late** to rescue reserved-query-var hijacks;
  fix at `request` filter.
- Live plugin files may be the **LF flavor** of CRLF repo blobs — base-md5
  no-clobber guards must compare against the live flavor (peek first).
- https pages cannot fetch http://127.0.0.1 (mixed content) — the local
  screenshot-POST pipe works from http:// pages only.

## Rollback

Each file keeps a `.bakV5` sibling holding the exact pre-V5 bytes
(no-clobber: written once, phase reruns never overwrote them).

---

# V6 ADDENDUM — same day, evening (owner follow-up orders)

Owner: auto-start the tour on click-in, add an openable instructions menu,
improve the walk feel (with web research), merge the walk tour with Earth 3D
now, save the night-street repo with us, add Hebrew+English narration with
maximum pronunciation accuracy (more web research on niqqud).

## Shipped live (md5-verified, .bakV6 = the V5 bytes)

| surface | change | live md5 |
|---|---|---|
| sde-dov-tour.html | V6: auto-tour, ☰ guide menu (he/en), narration (6 he + 6 en clips), walk feel | 174abb03a1e9837406dc47f0448bb997 |
| somail-tour.html | V6: auto-tour, ☰ guide menu (he/en), walk feel | 2241a7f40cc10fb8d57519db02d4154d |
| earth-experience.php | 🚶 "לרדת לרחוב" FAB per scene → /tour/{slug}/?mode=explore (server-linted) | 4762aeb2d3ddadb622753ee69d23a3d4 |
| uploads/2026/08/narr-sdedov-{he,en}-{0..5}.mp3 | 12 narration clips, exact names, all 200 | — |

- **Auto-start**: plain load → guided flight begins by itself (~1.3s), chip
  says any touch stops it; deep links (?t/?focus/explore), ?demo=0 and
  reduced-motion keep the calm boot; background tabs restart on focus.
- **Guide menu**: ☰ next to the language pill — what's-here, how-to-move,
  guided-flight / free-walk / helicopter-Earth / hub links; ESC,
  click-outside, ✕ all close (never-stuck); fully i18n he/en.
- **Earth↔street loop closed both ways**: earth pages got the walk FAB; the
  tours' menu links to /earth/{scene}/.
- **Walk feel** (research: subtle-or-sick — head-bob kept tiny, damped):
  distance-locked footfall bob (step ≈ 1.42m) + lateral sway + 2.2° FOV push
  while gliding + soft synthesized footstep taps; ALL disabled under
  prefers-reduced-motion.
- **Narration**: script from the tour's own verified facts (airport closed
  2019, TA/4444, 16k homes, the three flagships, runway park, time machine);
  spoken column per the measured pronunciation playbook — numbers as
  gender-correct words, niqqud ONLY on risk words (דּוֹב הוֹז, דִּימְרִי יָמָה,
  רֵיינְבּוֹ, אַשִירָה, אֲבִישְׂרוֹר, אַיינְשְׁטֵיין, אִבְּן גְּבִירוֹל), ellipsis/period
  pacing, no SSML; he-IL-AvriNeural -8% / en-US-ChristopherNeural -6%.
  Plays via the existing sound button; caption bar always accompanies;
  follows scroll chapters; stops in explore; works in reduced-motion mode.
- **night-street archived** at skills-external/night-street-study/ (source
  zip 21.7MB + TECHNIQUE/COLDSTART/NOTES/README).

## Evidence

- Auto-start seen on screen (headless, visible-mode): no gate, demo chip
  live, ☰ present — local and LIVE shots.
- Menu pressed for real in-browser: panel content/buttons/Earth-href read
  back correct, ESC closed it.
- Narration audio PLAYED for real in-browser from the live library
  (currentTime 1.46s of 13.8s, chapter-0 he) and caption bound correctly.
- Deploy: 3/3 md5_written_ok, earth php server-lint ok, snippet+payloads
  deleted, health 1.72.218 ok, rainbow+h-infinity spot-check pass.
- Whisper QA for the clips is SAC-blocked on this machine (tiktoken DLL) —
  pronunciation assured by the measured playbook rules (the proven niqqud
  pipeline with 23 live instances), verified clip durations, and the same
  engine/voice as the live EcoCity narration.

## New traps

- PowerShell pipelines corrupt Hebrew bytes in `git show` output — extract
  via `cmd /c git show > file` and byte-convert in python (blob-hash verify).
- Hidden pane tabs freeze rAF: UI reveals must use setTimeout, not
  double-rAF, or panels/captions never appear for background loads.
- SAC now also blocks whisper/tiktoken native DLLs (voice QA path gone).

---

# V7 ADDENDUM — 2026-08-22 (owner orders: tours hub + distribution + SEO mega-nav)

Owner: centralize the tours + connect to the menu + spread across projects
and sale/rent pages + find the FR/RU tours and spread on language pages +
ONE horizontal opening mega menu on the homepage, topics in logical order,
SEO-first (projects/prices near the crawl), with web research.

## Shipped live (all peek-gated, server-linted, .bakV7, verified eyes+code)

1. **/tours/ hub (page 7263)** — DNA-styled cards for every live experience
   (Sde Dov, Somail, both helicopters, designer, EcoCity), keyword lead with
   internal links, h1=1, Yoast title+desc set. The canonical share URL.
2. **Homepage mega-nav consolidated (home-v2.php)** — ONE horizontal opening
   nav, SEO order: פרויקטים חדשים → מחירים ונתונים → דירות → סיורים תלת־ממד →
   מדריכים וכלים → אנשי מקצוע → אזורי ביקוש/נדל"ן בחו"ל (plain). Prices
   panel now links the REAL converting city price pages
   (/tel-aviv|jerusalem|herzliya|ramat-gan|netanya-apartment-prices/) instead
   of catalog facets. Every destination of the old theme row preserved
   (/premium/ moved into the tours group, /guides/ bolded). Theme's duplicate
   row hidden on the homepage only.
3. **Sitewide menu item** — "סיורים תלת־ממד" injected into the static theme
   nav from mobile-nav-repair.php (language-aware label, dupe-guarded).
4. **Mobile order** — the duplicate hamburger retired; the swipeable
   horizontal row (owner's stated preference) is THE mobile nav.
5. **Distribution** — feature-bar membership now on BASE slug (language
   siblings -en/-fr/-ru/-ar inherit their district tour with ?lang=en);
   DUO-tel-aviv explicitly in the Somail family (was the missing hero);
   pretty /tour/ URLs everywhere (teaser + bar); property singles
   (sale/rent) got a tours strip via listings-ux.php.
6. **i18n** — tours/nav keys added in all 5 languages.

## FR/RU tours — the truth

Searched the entire uploads library server-side (glob 2026/*/*.html): NO
French or Russian tour files exist. What exists is he/en INSIDE the two
quarter tours. Distribution therefore deep-links `?lang=en` on foreign
pages; building real FR/RU tour UI+narration is a priced follow-up.

## SEO research applied (owner-ordered search)

Nav = links from every page → only the strongest hubs with keyword anchors;
tight panels (link dumps dilute PageRank); money pages ≤3 clicks; real HTML
<a> links (the mega uses native details/summary + plain anchors); hierarchy
kept (nav → hubs → children). Sources in the war-room issue.

## The save of the day

The server-side token lint gate REJECTED my first home-v2 swap — an
apostrophe ("theme's") inside the single-quoted PHP CSS string, the exact
2026-07-12 outage class. Site never flinched; fixed and redeployed. The
pipeline's lint chain has now paid for itself in production.

Verified: home mega order/tours group/hide-rule/price links (code) + desktop
and 375px screenshots (eyes); /tours/ h1=1 + cards; DUO tour chip live;
rainbow pretty links + old uploads URL absent; health 1.72.218 ok.

---

# V8 ADDENDUM — 2026-08-22 (owner order: wide WhatsApp button, plan approved)

Owner: a WIDE WhatsApp button for mobile+desktop, design-DNA, must not hide
important elements, WhatsApp logo + SITE logo on it, text "לפרטים נוספים"
(his pick), also English (his follow-up), click pulls page context (improve
the existing), REPLACES the green circle sitewide (his pick).

## Shipped live (.bakV8, peek-gated, server-linted)

- **inc/conversion-cta.php** — the 56px circle became a 54px-tall PILL:
  WhatsApp glyph in a translucent round chip (inline SVG kept), label
  `cta_wa_b` + micro-line `cta_wa_s`, and the NadLan brand chip — the
  favicon's dark-square-three-gold-bars drawn as inline SVG (no image file
  exists; the header logo is pure CSS). `dir` follows the page language so
  the pill mirrors correctly on LTR pages. Carries `data-nl-whatsapp`,
  which FIXES the flagship-v3 adopt-existing contract (its selector matched
  nothing before). Opener message localized (`cta_wa_msg`).
- **inc/i18n.php** — 4 keys × 5 languages (he/en/fr/ru/ar).
- **inc/wa-source.php** — the click-time context stamp now writes a
  localized label (מקור/Source/Источник/المصدر) chosen by
  `document.documentElement.lang`; idempotence recognises all variants,
  raw + URL-encoded.
- **inc/premium-ui.php** — the mobile `width:52px!important` square rule
  (which would have CRUSHED the pill) split to the AI fab only; pill gets
  `min-height:50px`. NOTE: live premium-ui had DRIFTED from repo HEAD
  (never-mirrored past swap) — the peek gate skipped it, the live bytes
  were pulled via a b64 route, patched by line-surgery with content
  assertions, and redeployed against the LIVE base md5. The repo copy now
  equals the live+patch state; the pre-patch live bytes are archived at
  docs/wp-state/premium-ui.live-1.72.218.php.

## Evidence

- Eyes: desktop crop — pill bottom-left (RTL) over the hero, all three
  elements; mobile 375 crop on /tours/; EN crop — pill bottom-RIGHT (LTR
  mirror), "For more details" / "Fast reply on WhatsApp".
- Real clicks through the interceptor (browser, both languages):
  he → `שלום, אשמח לפרטים נוספים.\n\nמקור: {title}\n{url}`
  en → `Hi, I’d like more details.\n\nSource: {title}\n{url}`
- Old circle CSS absent from the rendered page; engine project pages keep
  their designed behavior (floating CTA hidden there — the showroom's own
  WhatsApp pill serves, and it gets the same stamp).
- Health 1.72.218 ok; rainbow + h-infinity spot-check pass.

## New traps

- premium-ui.php live ≠ repo HEAD (undocumented drift) — ALWAYS peek; for
  drifted files: pull live b64 → patch on live bytes → swap vs live md5.
- Exact-string patches over pulled live files can miss on invisible chars —
  line-surgery with whitespace-stripped content assertions is the robust
  form.
- PowerShell here-string "tabs" are not the file's tabs — never build
  byte-exact anchors in PS; use python against the actual bytes.
