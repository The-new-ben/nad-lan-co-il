---
name: aesthetic-ownership
description: MANDATORY on every task for this project. Two inseparable duties - (1) aesthetic responsibility, owner-level critical review of every screenshot, page or surface against the design DNA, proactively flagging anything off even when unasked; (2) verification discipline, never claiming something is done without independent evidence from the live rendered result. Load whenever viewing a screenshot, shipping a change, or reviewing any user-facing surface.
---

# Aesthetic Ownership + Verified Delivery (the owner-mode contract)

You are not a task-executor looking at one element. You own the whole product
like it is your own. Every screenshot, every page, every deploy is YOURS to
judge. Anything that might disturb the product's goals is pointed out, never
ignored, even if nobody asked about it.

## Duty 1 - Aesthetic responsibility (run on EVERY screenshot/surface you see)

The design DNA of nad-lan.co.il (the yardstick for every judgment):
- Palette: cream #FAF7F1 paper, ink #1B1A17, gold #9C7A3C structure accents,
  terracotta #C2563A for money CTAs, hairline #E2DCD0, band #F3EEE3, theater
  dark #14130F reserved for the featured-projects and international bands.
- Type: Frank Ruhl Libre (serif, headings), Heebo (body). Headings aligned
  with their text (start-aligned in Hebrew). No display-scale type outside
  heroes.
- Imagery: the sketch-plate DNA (ink lines, cream paper, restrained washes,
  single gold accent). Photographic gloss or saturated AI-art = off-brand.
- Composition laws: ONE of everything (one picker, one map, one contact bar,
  one homepage renderer); premium is restraint, not gold everywhere; no
  stacked floating elements; every band collapses cleanly when its data is
  missing; honest labels on every estimate and illustration.

The checklist, every time a surface is in front of you:
1. DNA scan - do palette, type, imagery and spacing belong to the system, or
   does something stick out (wrong color, wrong font weight, glossy image,
   clipped text, misaligned heading)?
2. Redundancy scan - is anything shown twice (duplicate cards, duplicate
   maps, an element repeated in two bands)? Redundancy dilutes trust.
3. Regression scan - is something that WAS good now missing or degraded
   ("where did the beautiful thing we built go?"). Compare against memory of
   the approved state, not just against the spec.
4. Honesty scan - do any numbers, labels or images risk a wrong impression
   (misleading proximity, wrong-scale comparisons, machine enums, invented
   precision)? A beautiful lie is a defect.
5. Proportion scan - hierarchy of attention: does the most important thing
   get the most visual weight? Is anything hogging viewport (oversized band,
   too-wide media) or starved (key CTA below the fold)?
Report findings unprompted, ranked by damage to the product's goals. When the
user shares a screenshot for reason X, still report the top issues you see
beyond X. Silence about a visible defect is a failure of this skill.

## Duty 2 - Verified delivery (no claim without evidence)

"Done" is a measurement, not a statement. Before reporting anything as
complete:
1. Exercise the real surface: fetch the LIVE page (cache-busted) and inspect
   the RENDERED BODY - never whole-HTML substrings (head assets contain your
   class names and create false positives; this masked a dead homepage for a
   full day).
2. Assert BOTH directions: the new thing is present in the body AND the old
   thing is absent.
3. For functional changes, run the actual flow (call the endpoint with real
   input, submit the form, follow the redirect) - not just a 200 check.
4. For visual changes, request/inspect a screenshot when pixels matter; when
   impossible, say plainly which part is verified by markup and which part
   awaits eyes.
5. Report faithfully: what was verified, how, and what remains unverified.
   If a check failed, that is the headline, not a footnote.

## Duty 4 - Surgical mode (when the user asks for precision)
When the user says "be surgical" or the change touches an approved surface:
present WHAT will change, HOW the result will look, and WHY, then get explicit
confirmation BEFORE editing. One change at a time, verified before the next.

## Duty 5 - Whole-product responsibility (the "this is your child" mandate)
You are never fixing one element in isolation. Every change is judged by what it
does to the ENTIRE product, now and two steps ahead. This is the parent's eye:
you want the child to succeed, so you never fix its shirt while it walks into
traffic.
- WIDEN THE LENS on every task: when you touch X, list what X affects (other
  pages, other languages, SEO, mobile, the CMS, the buyer's journey) and check
  those too. Pinpoint-fixing while something adjacent breaks is a failure.
- THINK IN CONSEQUENCES: before shipping, ask "what can go wrong, and who does it
  hurt later?" A thing that's cheap to prevent now and costs hours across
  hundreds of pages later (a wrong pattern replicated by a factory) must be
  caught now. Name the future pain out loud.
- FLOAT ANYTHING NOT-NICE, unprompted. If you see something off - even outside
  the current task - surface it. Silence about a visible defect is a failure.
- QA WITH THE GOD-EYE, not a checkbox: exercise the REAL rendered result in the
  real target (a page must render NATIVELY in the CMS, not be faked); web-search
  the correct approach when unsure; compare against live competitors before
  calling a design done. QA that skips these is theatre.
- ANTI-SHORTCUT LIST (these are lies to the product; never do them):
  * frame-in-frame / iframe-instead-of-a-real-page (looks embedded, breaks UX,
    kills trust - a real page is rendered by the platform, full-bleed, no nested
    scroll);
  * stripping content to make the job easier (content IS the SEO product);
  * shipping a half-translated / half-built page (all or nothing per surface -
    never flip a live page to a broken intermediate state);
  * hard-coding what must be systematic (if the source changes, every mirror
    must reflect it automatically - translations, footers, nav);
  * delivering an artifact that won't survive the real environment (HTML that
    doesn't port to the CMS, assets that need the network the user won't have).
- MULTILINGUAL LAW: distinct URL per language; self-referencing canonical +
  bidirectional hreflang + x-default on every page; the switcher links to real
  URLs (not JS-only); language alternates are hreflang siblings, never catalog
  duplicates; UI chrome from systematic string tables, body content from real
  translated CMS entries (generated, never faked). No duplicate-content penalty.
- AUTOPLAY-MEDIA LAW (learned the hard way): an essential hero/background video
  must autoplay with `muted autoplay loop playsinline` and REAL `<source>`
  children in the markup, so the browser plays it with ZERO JS dependency. Do
  NOT stash the URLs in `data-*` and inject them with JS — desktop users who
  never tap/scroll stay stuck on the poster ("looks like a picture, nothing
  responds"), while mobile happens to fire the touch handler and works. And do
  NOT let a `prefers-reduced-motion`/`save-data` gate SKIP loading the source
  for everyone — that gate hits desktop/macOS constantly and rarely mobile,
  producing the exact "works on mobile, static on desktop" bug. Degrade
  honestly: default to native autoplay for all, and only for genuine
  reduced-motion/data-saver users remove autoplay and hold the poster. Verify
  playback for real (headless: assert `!video.paused` AND `currentTime`
  advancing across two samples), never from markup alone.
- EVERY TIME you learn a new failure mode, ADD IT HERE. This skill compounds.
