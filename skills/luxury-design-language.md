# Luxury Design Language — nad-lan.co.il

> **Notice to all agents:** this is the canonical visual system, derived 2026-05-28 from studying the most premium real-estate websites in the world (Sotheby's International Realty, Christie's International Real Estate, The Agency, Compass, and the Mediaboom "50 luxury examples" + Luxury Presence typography guidance). It **supersedes** the earlier `visual-design-skill.md` corporate-blue palette. When the two conflict, this file wins. The owner rejected the corporate-blue/trust-blue look and the cartoon-house logo on 2026-05-28 and asked explicitly to copy the luxury leaders' design language.

## Sources studied (proof of research, 2026-05-28)

- Sotheby's International Realty — `sothebysrealty.com` — centuries-of-tradition luxury, serif-led, restrained.
- Christie's International Real Estate — `christiesrealestate.com` — "Parisian interiors, streamlined minimalist layout, exclusivity."
- The Agency — `theagencyre.com` — "minimalist design + impactful full-bleed visuals, immersive."
- Compass — clean modern, high-quality imagery, straightforward search.
- Mediaboom "50 Luxury Real Estate Website Design" — concrete patterns (below).
- Luxury Presence brand-fonts guide — typography consensus (Playfair Display serif headings).

## The distilled luxury design language

### Principle: restraint + warmth + space
Luxury is **forced minimalism**. Generous whitespace signals confidence. Content (and eventually photography) does the talking. Never loud, never busy, never bright-corporate.

### Typography — THE single biggest lever
Research consensus: **serif headings + light sans body** = expensive. Sans-only = affordable/cheap.

- **Headings: Frank Ruhl Libre** — the Hebrew transitional serif, the Hebrew counterpart to Playfair Display. Elegant, traditional, authoritative. Weights 500/700/900. Bundled at `assets/fonts/frank-ruhl-libre/`.
- **Body: Heebo** — clean humanist sans, weight 300–400 for that light luxury feel. Bundled at `assets/fonts/heebo/`.
- **Eyebrows / labels / categories:** Heebo, small (12–13px), **wide letter-spacing** (0.15–0.2em), often with manual character spacing in Hebrew (no uppercase exists in Hebrew, so tracking carries the "label" signal).
- Big serif headings get **tight** tracking (-0.01 to -0.02em) and generous line-height (1.15–1.25).
- Body: 17–18px, line-height 1.7 (more air than the earlier 1.65).
- **No font bundled from a CDN at runtime** — all woff2 local in the theme (page-speed + privacy + no external dependency).

### Color — warm minimal, NOT corporate blue
Pivot away from `#0E3A8A` trust-blue. Luxury real estate = warm neutrals + one restrained metallic accent.

| Token | Hex | Role |
|---|---|---|
| `ink` (contrast) | `#1A1A1C` | near-black text + dark sections (not pure #000) |
| `base` | `#FFFFFF` | page background |
| `cream` | `#F7F4ED` | warm section background, cards, panels |
| `gold` (accent) | `#B08D57` | the single metallic accent — rules, small highlights, hovers. Muted antique gold, NOT bright #D89B3C |
| `stone` | `#7A746C` | muted secondary text, eyebrows, captions |
| `line` | `#E5E1D8` | hairline borders, dividers (warm, not cool gray) |
| `positive` | `#3E6F57` | price-up (muted forest, not bright green) |
| `negative` | `#9B4A3F` | price-down (muted terracotta, not bright red) |

Rule: **two neutrals (cream + ink) + one accent (gold)**. Changing colors per section = cheap. Stick to these everywhere.

### Whitespace & rhythm
- Section vertical padding: 96–140px desktop, 64–80px mobile (more than the earlier 80/64).
- Max content width ~720px for text, ~1280px for wide sections.
- Card padding 28–32px.
- Let single elements stand alone with air around them.

### Shadows — subtle, warm, layered (NOT heavy)
- Default card: none or `0 1px 2px rgba(26,26,28,.04)`.
- Hover lift: `0 12px 32px rgba(26,26,28,.10)` + translateY(-3px), 200ms ease.
- 2026 luxury leans toward **hairline borders over shadows** (Tactile-Brutalism-lite). Prefer a 1px `line` border + tiny shadow over big soft shadows.

### Buttons — quiet, not loud
- Primary: ink background, cream text, **no border-radius or tiny (2–4px)**, generous padding (16px × 36px), small letter-spaced label. Hover: gold background OR subtle lift.
- Secondary: transparent with 1px ink/gold border, ink text. Hover: fill.
- **No bright fills, no big rounded pills, no gradients.** Luxury buttons are restrained rectangles.

### Header — thin, sticky, minimal
- Slim (64–72px), cream or white, 1px bottom hairline.
- Serif or refined wordmark logo (right, RTL).
- Minimal nav, wide-tracked.
- Sticky / "traveling" on scroll with a subtle backdrop blur + hairline.
- A single quiet CTA, not a loud button.

### Logo
- **Elegant serif wordmark** in Frank Ruhl Libre — "נדל״ן חכם" — with a thin gold rule and a wide-tracked tagline eyebrow.
- **No cartoon house icon** (rejected by owner). If a mark is used, a refined monogram (נ) in a thin gold frame, like a crest.
- Favicon: monogram "נ" Frank Ruhl on ink with thin gold inner frame.

### Imagery (when available, Codex)
- Full-bleed, high-resolution architectural photography.
- Matte, not over-saturated. Warm tone to match cream palette.
- Generous whitespace around images, never cramped.

### Micro-interactions (systematic, not ad-hoc)
- Global tokens: transition 200ms, ease `cubic-bezier(.4,0,.2,1)`.
- Link hover: animated underline (gold), grows from right (RTL).
- Card hover: lift 3px + hairline → soft shadow.
- Button hover: bg shift to gold or ink↔cream invert.
- Smooth scroll, antialiased font smoothing, branded text selection (cream-on-gold).

## Implementation map

- **theme.json** — palette (above), fontFamilies with local fontFace for Frank Ruhl Libre + Heebo, heading styles (serif, tracking), button styles (quiet), spacing scale, body 1.7 line-height. Needs theme re-sync.
- **style.css + style.min.css** — micro-interactions, sticky header polish, link underline animation, card hover, selection color, eyebrow letter-spacing utility. Needs theme re-sync.
- **Logo / favicon / OG** — generated PNGs in `assets/branding/`, uploaded to media, set as site_logo + site_icon + Yoast default OG. Live via REST, no sync.
- **Header/footer template parts** — refine to thin sticky header + restrained footer. Live via REST.

## What this replaces / deprecates
- `visual-design-skill.md` §6.1 palette (gold #D89B3C bright, trust blue dominant) → DEPRECATED in favor of the warm-minimal palette here.
- The "green-dominant" accidental look from Codex's accent-3 usage → overridden by the new palette.
- The cartoon-house logo (v1) → replaced by serif wordmark.

## Open TODOs
- [ ] Owner approves the luxury logo/OG direction (sent 2026-05-28).
- [ ] After approval: owner does ONE theme re-sync (UPress Git pull from main) to apply theme.json + bundled fonts + premium CSS in one shot.
- [ ] Re-upload approved logo/favicon/OG (already wired; swap media if direction changes).
- [ ] Refine header template part to thin sticky + serif wordmark.
- [ ] Codex: source warm architectural photography per image-pipeline.md.
- [ ] Consider a serif-headings + photography hero on the homepage (Codex content).

---
_Created 2026-05-28 by Claude Code (claude-opus-4-8). Research sources cited above; fonts bundled OFL-licensed (Frank Ruhl Libre, Heebo) from Google Fonts._
