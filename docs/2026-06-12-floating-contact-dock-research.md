# Premium Floating Contact Dock (AI + WhatsApp + Call) — Cited Research
**Date:** 2026-06-12 · **Researcher:** Claude (deep-research agent, 12+ searches / 8+ fetches)
**Target:** v1.61.0 `nadlan-config` module replacing the three plain floating buttons. No subscriptions.

## TL;DR spec (build contract)
1. One 56–64px gold launcher, **bottom-LEFT** (RTL mirror; Israeli sites keep the נגישות widget right — avoids collision), `bottom: calc(env(safe-area-inset-bottom) + 16px)`, `z-index: 2147483000`, hides on scroll-down / restores on scroll-up.
2. Tap → fan-out of 3 **labeled** chips (Hebrew labels, never icon-only): נציג AI / וואטסאפ / חיוג — **WAI-ARIA Disclosure pattern** (`aria-expanded` + `aria-controls`, Esc closes, focus returns to launcher). NOT role=menu.
3. WhatsApp chip: `https://wa.me/972525101555?text=` + `encodeURIComponent` of Hebrew greeting **including current property title/URL**. (No `+`, no leading 0, no dashes in wa.me. Verified format on remax.co.il.)
4. Call chip: `tel:+972525101555` (E.164, drop domestic 0).
5. AI chip opens `role="dialog" aria-modal="true"` RTL panel, focus-trapped, messages in `aria-live="polite"`, streaming via existing WP REST proxy (OpenAI key stays server-side).
6. **Speaking avatar** — verified tech facts:
   - `speechSynthesis` does NOT route through Web Audio → AnalyserNode amplitude lip-sync is impossible on browser TTS. `boundary` events don't fire on Android Chrome.
   - WORKS: OpenAI `tts-1` audio → `<audio>` → `MediaElementAudioSourceNode` → `AnalyserNode` → true amplitude lip-sync on a 2D SVG face. Our key, pennies per utterance.
   - Fallback: browser `speechSynthesis` he-IL (iOS = single voice "Carmit"; Android = Google TTS, lang code `he_IL` with underscore — normalize) + time-based mouth-flap between onstart/onend.
   - Voice ALWAYS opt-in (user gesture required by browsers anyway; iOS respects mute switch).
   - TalkingHead 3D (MIT) exists but needs three.js + has no Hebrew viseme module — SKIP.
7. Proactive nudge: gentle pulse after ~30s on LISTING pages only (never homepage, never instant); dismissal persisted in localStorage, quiet 7 days. No auto-pop on mobile.
8. All animation behind `prefers-reduced-motion: no-preference`; contrast 4.5:1 text / 3:1 icons (WCAG 2.2 AA).
9. Vanilla JS + CSS, one enqueued script, no iframes, no widget SaaS.
10. Theme viewport meta needs `viewport-fit=cover` for iOS safe-area to report.

## Conversion evidence
- Live chat ≈ +20% conversion avg; chat engagers 2.8× more likely to convert, ~60% higher spend (Social Intents, ReveChat).
- 38% more likely to buy with live chat; +10% AOV (Forrester via Tidio); 305% ROI proactive chat (Etech); ~15% of visitors engage.
- WhatsApp widgets: vendor-claimed up to +45% conversion (upper bound, vendor data).
- WhatsApp Israel penetration: **98% women / 97% men** (Statista Jan 2024) → WhatsApp is the hero action.

## Accessibility audit traps (documented Intercom failures — do not repeat)
- Focus NOT moving into panel on open (stays on launcher) — Intercom community-reported.
- Hover-state contrast below 3:1.
- Testing only default desktop view — keyboard/zoom/mobile/close behavior is where widgets fail audits.

## Z-index reality
Commercial widgets mount at max-int 2147483647. Sit just below (2147483000) so cookie/a11y overlays can win. Audit collision with existing sticky CTA + accessibility widget.

## Sources
m1.material.io FAB + m2 bidirectionality · mobbin.com FAB glossary · uxplanet.org Babich FAB · polypane.app safe-area · MDN env()/prefers-reduced-motion/Web Speech API/boundary_event · w3.org WAI APG (disclosure, menu-button, modal-dialog) + C39 · intercom.com messenger-accessibility + community a11y thread · oscarchat.ai a11y checklist + click-to-chat · makethingsaccessible.com WCAG 2.2 contrast · faq.whatsapp.com/5913398998672934 · qualimero.com whatsapp-link · remax.co.il (live verified) · en.wikipedia.org Telephone numbers in Israel · ynet.co.il (live: bottom-right Butterfly widget) · statista.com WhatsApp Israel · socialintents.com + revechat.com + tidio.com chat stats · zendesk standard triggers · proprofschat proactive best practices · buttonizer + mystickyelements (WP dock plugins) · gist.github.com Koze iOS voices (Carmit) · talkrapp.com speechSynthesis lessons · dev.to cross-browser speech synthesis · digitalocean.com TTS-no-audio-stream Q · github.com/met4citizen/TalkingHead
