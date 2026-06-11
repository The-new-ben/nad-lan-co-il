# Skill: Non-Binding Offers Engine (legal-safe bidding for any marketplace)
Proven pattern (nad-lan v1.57.0, inc/offers.php) + legal spec (docs/2026-06-11-offers-feature-spec-cited.md).
1. LEGAL FRAME (Israel): flat listing fee ONLY, never success fee (חוק המתווכים "הפגשה בתמורה");
   explicit non-binding checkbox; platform passes contacts, never negotiates; offline close
   framed as "התמחרות אצל עורך הדין".
2. MODEL: offer CPT (private) with amount/financing/flexibility/consent; statuses pending->live->
   connected/declined/withdrawn/expired; anonymous handles ("מציע #N").
3. TRANSPARENCY per listing: sealed | leading_amount | full_open. Default leading_amount (open
   formats fetch 1.2-9.6% higher prices than sealed - cite Chow et al.). Sealed must NEVER leak
   amounts via any endpoint.
4. ANTI-SNIPING: window_end extends +24h on each new leading offer.
5. ANTI-ABUSE: honeypot field (pretend success), 5/hour/IP rate limit, phone+card dedupe
   (same buyer revises instead of duplicating), seller minimum.
6. NOTIFY: owner gets amount+handle only; contact details revealed only on explicit connect
   (consent-gated, phase 2).
