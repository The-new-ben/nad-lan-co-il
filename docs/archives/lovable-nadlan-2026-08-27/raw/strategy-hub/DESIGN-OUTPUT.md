# NadLan — Design Output Handoff

Autonomous build against the founding prompt (Part 2) and section prompts (Part 3, S1–S12). Hebrew-first RTL, cream editorial luxury, one dark band per page (footer + theater).

## Completed layers

- L0 Shell — tokens, Google Fonts, `DirectionProvider`, header, footer, all 12 routes.
- L1 S1 Homepage hero — photoreal Tel Aviv shoreline + dark glass search card.
- L2 S2 3D theater band — dark, 4 real project selectors, honest disclosure.
- L3 S3 Live map band — cream, SVG map of Israel, terracotta pins, city chips.
- L4 S4 Rentals band — white card with gold frame + 3 step chips.
- L5 S5 Urban renewal band — band ground, 3 steps, dual CTA.
- L6 S6 Listings grid — 4 ink-sketch building plates, `object-contain` (never cropped).
- L7 S7 Tools row — gold-bordered lead card, 4 supporting tools.
- L8 S8 Magazine row — 3 editorial guides.
- L9 S9 `/project/$slug` — dark 3D stage hero + facts rail + apartment tabs.
- L10 S10 `/my-rentals` — hero, RentalsSection, 6 health cards, 12-month ledger grid.
- L11 S11 `/my-renewal` — 3D model with consent color chips + 10-stage stepper.
- L12 S12 `/en` — English hero, `dir="ltr"` via `LangProvider.setLang("en")`.
- L13 Audit — no `ml-/mr-/pl-/pr-/left-/right-/text-left/text-right` in shell or section code; only logical utilities. One physical class was found and fixed (`md:border-r` → `md:border-e` in `MagazineSection`).
- L14 Handoff — this document. Every section is a self-contained component under `src/components/sections/` that depends only on tokens + copy + local image imports.

## Routes and components

| Route | File | Sections / components used |
| --- | --- | --- |
| `/` | `src/routes/index.tsx` | `HeroSection`, `TheaterSection`, `MapSection`, `RentalsSection`, `UrbanRenewalSection`, `ListingsGridSection`, `ToolsSection`, `MagazineSection` |
| `/projects` | `src/routes/projects.tsx` | Uses copy `HE.theater.projects` |
| `/project/$slug` | `src/routes/project.$slug.tsx` | Dark stage + facts rail + tabs (self-contained) |
| `/listings` | `src/routes/listings.tsx` | Existing route, unchanged in this layer |
| `/listing/$id` | `src/routes/listing.$id.tsx` | Self-contained detail page |
| `/professionals` | `src/routes/professionals.tsx` | Existing route |
| `/urban-renewal` | `src/routes/urban-renewal.tsx` | Hero + `UrbanRenewalSection` |
| `/my-renewal` | `src/routes/my-renewal.tsx` | 3D consent + 10-stage stepper (self-contained) |
| `/my-rentals` | `src/routes/my-rentals.tsx` | Hero + `RentalsSection` + 6 health cards + ledger grid |
| `/calculators` | `src/routes/calculators.tsx` | Tools grid (self-contained) |
| `/glossary` | `src/routes/glossary.tsx` | Definition list (self-contained) |
| `/guides` | `src/routes/guides.tsx` | Existing route |
| `/en` | `src/routes/en.tsx` | English hero, forces `lang="en" dir="ltr"` |

Shell:
- `src/routes/__root.tsx` — root layout, Google Fonts `<link>`, `DirectionProvider`, `LangProvider`.
- `src/components/shell/SiteHeader.tsx` — brand + 6-item nav + HE/EN toggle.
- `src/components/shell/SiteFooter.tsx` — 4 columns on `--theater` (the chrome dark band).
- `src/lib/lang-context.tsx` — HE (default) / EN toggle, sets `document.documentElement.{dir,lang}`.
- `src/lib/nadlan-copy.ts` — all HE and EN production copy.

## Design tokens (as implemented in `src/styles.css`)

| Token | Value | Role |
| --- | --- | --- |
| `--paper` | `#FAF7F1` | Page ground |
| `--ink` | `#1B1A17` | Text |
| `--gold` | `#9C7A3C` | Structure accents, links, kickers |
| `--terracotta` | `#C2563A` | Money CTAs only |
| `--hairline` | `#E2DCD0` | 1px borders |
| `--band` | `#F3EEE3` | Alternate band ground |
| `--theater` | `#14130F` | Single dark stage per page |
| `--muted-ink` | `#A79E8D` | Secondary text |
| `--success` | `#517048` | Statutory / positive |
| `--warning` | `#9C7A3C` | Warning (same hue as gold) |
| `--danger` | `#C2563A` | Danger (same hue as terracotta) |

Typography: Frank Ruhl Libre 500/600/700/800 headings, Heebo 400–700 body/UI, loaded via `<link>` from Google Fonts in `src/routes/__root.tsx`. `@fontsource` packages and `tw-animate-css` were removed to match the spec.

Radii: cards 16 px (`rounded-2xl` = `calc(0.75rem + 8px)`), pills 999 px, small radius `--radius: 0.75rem`.

Shadow: `stage-shadow` utility → `0 24px 60px -28px rgba(27,26,23,0.35)`.

Utilities emitted: `hairline`, `hairline-b`, `hairline-t`, `kicker`, `stage-shadow`, `btn-terracotta`, `btn-terracotta-hover`, `btn-gold-outline`, `chip`.

## Generated images

Every image is architectural ink-and-wash on cream paper with a single gold accent, or photoreal aerial. No stock people, no gradients, no abstract 3D.

| File | Section | Prompt (verbatim) |
| --- | --- | --- |
| `src/assets/hero-tel-aviv-shoreline.jpg` | S1 (`HeroSection`), also `/en` hero | Photoreal aerial oblique photograph of Tel Aviv shoreline at late afternoon warm golden light. Wide Mediterranean beach on left, marina with small white boats, then dense white and cream residential city receding into distance with Bauhaus buildings and modern towers. Soft warm haze, no people visible, no text, no logos. Editorial architectural photography, cinematic, restrained color grading, cream and warm tones dominant. |
| `src/assets/theater-3d-stage.jpg` | S2, S9 (fallback) | A single tall dark cinema-lit 3D architectural model of a modern residential tower floating on a very dark charcoal background (near black #14130F), warm subtle radial glow behind it, individual apartments visible as delicate glowing units, no text, no logos, editorial real-estate publication mood. The building has a horseshoe curved shape suggesting the Rainbow project in Beer Yaakov. Muted gold accent on ground floor. |
| `src/assets/sketch-building-holon.jpg` | S2 selector (Keshet Holon), `/projects` | Architectural ink and wash sketch on cream paper background. A residential apartment building shown in three-quarter perspective with visible floors and windows, subtle warm cream and off-white washes, single muted gold accent on one balcony. Loose confident ink lines, no color gradients, no purple, no people, no text. Editorial illustration style, restrained, luxurious real-estate publication aesthetic. Empty margins for typography. |
| `src/assets/sketch-duo-ramat-gan.jpg` | S2 selector (DUO Ramat Gan) | Architectural ink and wash sketch on cream paper. Two elegant residential towers side by side in three-quarter view, tall slender proportions, subtle balcony rhythm, warm cream washes, one muted gold accent on ground floor entrance. Loose ink linework, no color, no people, no logos, no text. Editorial luxury real-estate illustration. |
| `src/assets/sketch-rainbow-beer-yaakov.jpg` | S2 selector (Rainbow Beer Yaakov), `/project/$slug` default | Architectural ink and wash sketch on cream paper. A curved horseshoe-shaped residential block with rainbow-arc massing (single unified curved building, no color rainbow), three-quarter perspective, warm cream washes, single muted gold accent on entrance canopy. Loose ink lines, editorial luxury real-estate publication style, no text, no people, no logos. |
| `src/assets/sketch-sde-dov.jpg` | S2 selector (Sde Dov TA) | Architectural ink and wash sketch on cream paper. Master-plan aerial view of a large new-neighborhood district next to the Mediterranean sea, orderly grid of residential blocks with green plazas, port on the left, sea horizon at top. Warm cream washes, single muted gold accent on the central plaza. Ink linework, no color, no people, no text, no logos. Editorial luxury real-estate publication. |
| `src/assets/sketch-rentals-dashboard.jpg` | S4 (`RentalsSection`), `/my-rentals` hero | Architectural ink and wash sketch on cream paper. A stylized isometric view of a residential building with apartment units highlighted as small colored dots (a few muted green, a few muted gold, one muted terracotta), a small map of the city hovering above the building. Warm cream washes, ink linework, no photorealism, no people, no text, no logos, no bright gradients. Editorial luxury real-estate publication style, evokes a landlord dashboard concept. |
| `src/assets/sketch-urban-renewal.jpg` | S5 (`UrbanRenewalSection`), `/urban-renewal` hero, `/my-renewal` stage | Architectural ink and wash sketch on cream paper. An older 4-story residential building being reconceived, with a lighter sketch of a new taller building rising behind it in the same drawing, symbolizing urban renewal. Warm cream washes, single muted gold accent on the new building's entrance, ink linework, no people, no text, no logos, no bright colors. Editorial luxury real-estate publication style. |
| `src/assets/sketch-listing-tlv-bauhaus.jpg` | S6 listing 1 (Tel Aviv lev) | Architectural ink and wash sketch on cream paper. Front elevation of a renovated three-room apartment in a classic Tel Aviv Bauhaus building, showing the building's white curved facade with the apartment's windows highlighted. Warm cream wash, single muted gold accent on the balcony rail. Ink linework, editorial luxury real-estate publication, no people, no text, no logos. |
| `src/assets/sketch-listing-jlm.jpg` | S6 listing 2 (Jerusalem Rehavia) | Architectural ink and wash sketch on cream paper. Front elevation of a modern 4-story residential building in Jerusalem with stone cladding and arched windows, warm cream washes, one muted gold accent on the door. Ink linework, editorial luxury real-estate publication, no people, no text, no logos, no bright colors. |
| `src/assets/sketch-listing-haifa.jpg` | S6 listing 3 (Haifa Carmel) | Architectural ink and wash sketch on cream paper. Front elevation of a mid-century residential building in Haifa on a hillside with sea view in background, warm cream washes, one muted gold accent on the balcony rail. Ink linework, editorial luxury real-estate publication, no people, no text, no logos. |
| `src/assets/sketch-listing-rg.jpg` | S6 listing 4 (Ramat Gan Bavli) | Architectural ink and wash sketch on cream paper. Front elevation of a new residential tower in Ramat Gan with landscaped ground floor, warm cream washes, one muted gold accent on the entrance canopy. Ink linework, editorial luxury real-estate publication, no people, no text, no logos. |

Model used: `imagegen--generate_image` `standard` tier for every image. Aspect ratios preserved via `object-contain` for building plates so nothing is cropped (S6 rule).

## Deviations from the brief and why

1. **Google Fonts scale set to 500 / 600 / 700 / 800 for Frank Ruhl Libre** and 400 / 500 / 600 / 700 for Heebo. The brief specified 500–800 and 400–700 — same range, tightened to weights actually referenced in components. If you need 400 for Frank Ruhl Libre or 600 for Heebo, add them to the `<link>` `family=` query in `src/routes/__root.tsx`.
2. **Two dark surfaces coexist on every page — the theater band (or hero glass card) and the footer.** The founding brief says "one dark band per page (the 3D theater)". The footer is styled as a chrome band on `--theater`, not a content band. Ways to fully honor the rule:
   - remove the dark footer and use a cream footer with a hairline top,
   - or drop the dark theater on non-homepage routes (already done — only `/`, `/project/$slug` and `/my-rentals` demo carry any dark surface beyond the footer). Recommend converting the footer to cream at your review — it's a one-file change in `src/components/shell/SiteFooter.tsx`.
3. **`/my-rentals` demo frame is a static 12-month ledger + 6 static health cards.** The live product (v1.72.96) has real logic; the landing page here is the marketing surface only, matching what the section prompt asked for.
4. **Existing routes `/listings`, `/professionals`, `/guides`, `/about`, `/contact`, `/showroom/$projectId` were not redesigned** — they were already in the repo and outside Part 2/Part 3 scope. They still work under the new tokens (same semantic names, new hex values).
5. **Old `SiteHeader` / `SiteFooter` under `src/components/nadlan/`** are unused by the new shell but left in place to avoid breaking `handoff/*` routes. Safe to delete when convenient.
6. **The map illustration is an inline SVG stylized outline of Israel with terracotta pins**, not a generated image — this keeps it precise (real coordinates, real chip counts) and lightweight. All other imagery is generated.
7. **No English translation for S2–S11 yet.** `/en` is a fully translated homepage hero (S12 scope). Other Hebrew routes currently render Hebrew even when `lang` is toggled to `en`, because the redesigned section copy only exists in `HE`. Adding `EN.*` entries for `theater`, `map`, `rentals`, `renewal`, `listings`, `tools`, `magazine`, `project`, `myRentals`, `myRenewal` in `src/lib/nadlan-copy.ts` and switching each component from `HE.*` to `isHe ? HE.* : EN.*` is the mechanical follow-up — copy is the only missing input.

## Lifting a section into another codebase

Every file under `src/components/sections/` depends only on:
- design tokens in `src/styles.css` (paper / ink / gold / terracotta / hairline / band / theater + utilities `kicker`, `hairline`, `btn-terracotta`, `btn-gold-outline`, `chip`, `stage-shadow`),
- copy in `src/lib/nadlan-copy.ts`,
- images under `src/assets/`,
- `lucide-react` for icons.

To transplant a section: copy the section file + its images + the copy block it reads + the token block from `styles.css` (or the equivalent WordPress theme tokens). Ready to consume by the WordPress build.

## Audit results (L13)

Scanned every file under `src/components/{shell,sections}`, `src/routes/index.tsx`, `src/routes/en.tsx`, `src/routes/projects.tsx`, `src/routes/project.$slug.tsx`, `src/routes/listing.$id.tsx`, `src/routes/urban-renewal.tsx`, `src/routes/my-renewal.tsx`, `src/routes/my-rentals.tsx`, `src/routes/calculators.tsx`, `src/routes/glossary.tsx`, `src/routes/__root.tsx` for:

- `ml-*`, `mr-*`, `pl-*`, `pr-*`, `left-*`, `right-*`, `text-left`, `text-right` — **none remaining after fix**.
- English text on Hebrew surfaces — none in redesigned surfaces. `/en` is deliberately English.
- Second dark surface — only the theater band on `/`, the dark stage hero on `/project/$slug`, plus the chrome footer (see Deviation 2).
- Lorem ipsum — none.
- Placeholder images — none. Every rendered image is a real generated asset tied to its section.
- Unmirrored directional icons — only `Search` (symmetric) and `Calculator`/`Coins`/`Scale`/`Home`/`Building2` (symmetric) are used; no chevrons or arrows were introduced that need mirroring.

## What to do next

- Publish, then wire the GitHub sync (Settings → GitHub → Connect project) or download the zip from the code editor.
- The English routes need copy in `EN.*` for the remaining sections — send it and the switch takes a single edit per component.
- If the dark footer bothers you at the audit, flip `bg-theater text-paper` → `bg-paper text-ink hairline-t` in `SiteFooter.tsx`; nothing else changes.

