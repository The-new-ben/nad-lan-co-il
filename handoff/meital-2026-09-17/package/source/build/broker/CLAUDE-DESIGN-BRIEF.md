# Claude Design brief: Meital Katzir broker profile on nad-lan.co.il

Use this after running `/design` in the chat. It follows the practices found in research (design system first, one dense brief, explicit aesthetic constraints, real photography, several directions, rewrite nothing into generic copy).

## 1. Design system (set up first)

- Brand: nad-lan.co.il, Skin A. Colors: paper #F7F6F2, surface #FFFFFF, ink #14212B, ink-2 #3B4753, mute #6B7680, line #E3E1DA, sea #2F6F86 (the only action color), sea-hover #255C70, deep #1F4B5C, abyss #10262F, sand #EEE9DD, mist #CFE3EA, foam #E8F1F3.
- Type: Noto Serif Hebrew 600 for display and names; Assistant 400/600/700/800 for UI and body; tabular lining figures for every number. Latin fallback Noto Serif / Assistant.
- Shape: pill buttons (999px), cards 10px, feature bands 22px. One hairline horizon motif (1px line, sea to mist gradient) is the only ornament.
- Do not use: Inter, Roboto, purple or blue-violet gradients, glassmorphism stacks, emoji, stock "luxury" gold, fake testimonials, invented statistics, long dashes.

## 2. The brief (one paragraph)

Design a Hebrew (RTL) broker profile page, with an English (LTR) twin, for Meital Katzir, licensed Israeli real estate broker (license 3131540), brand "נדל״ן על הים" (Real Estate by the Sea), published on nad-lan.co.il under a cooperation agreement. Audience: high-net-worth buyers and tenants, many relocating or investing from abroad, who judge in seconds from a phone. The page must feel like Sotheby's editorial calm with Compass restraint: photography leads, the palette stays paper, ink and sea, and every number is precise. Sections in order: full-bleed hero on a real sea-view photo with her name at display scale, brand line, one factual sentence, WhatsApp, call and Instagram; a four-figure fact band (11 exclusive listings, 6 neighborhoods, sale prices NIS 4.65 to 18 million with the estate on request, rents NIS 9,500 to 27,000); a signature block for the private estate in Herzliya Pituach (700 sqm built, 1,100 sqm plot, 7 suites, 3 levels, price on request); a filterable grid of 11 full-detail listing cards (photo, deal badge, neighborhood, title, price and price per sqm, rooms, area, balcony, floor, 3 highlights, amenity chips, entry, last update, WhatsApp with the listing code, link to the full listing page); a schematic coastal map from Herzliya Pituach to Sarona with listing counts; an Instagram photo strip; a digital business card (front in deep sea, back with phone, WhatsApp, Instagram handle and a WhatsApp QR); a three-column "how the pages are built" band (every figure sourced, the real cost, market and setting); and a dark contact footer with the legal note. Mobile first with a sticky WhatsApp and call bar.

## 3. Ask for three directions

1. Editorial: large serif, generous white space, photography in tall frames.
2. Waterline: deep sea bands alternating with paper, the horizon line crossing sections.
3. Gallery: dense catalog grid with a quiet header, for brokers with many listings.

Then combine the best parts.

## 4. Artboards to produce

- Main: Hebrew broker page, desktop 1440 wide, flowing.
- Mobile: Hebrew broker page, 390 wide.
- English: English broker page, desktop 1440 wide.
- ListingCard: the full-detail card in sale and rent states, and the "details being confirmed" state.
- BrokerCard: business card front and back at 1050 x 600, plus a 1080 x 1350 share image.

## 5. Content rules

- Facts only from `build/broker/cards.json` and the listing editorials. No testimonials, deal counts, years of experience or awards unless Meital supplies them.
- Street names only where already public in the listing pages; no house numbers.
- L09 and L11 carry "זמינות בבדיקה" until Meital confirms them.
- Photos: Meital's own listing photos only. No AI images presented as a property.
- Hebrew: the Hebrew word in the sentence, the English professional term in parentheses on first use only.

## 6. Source files in this package

- `build/broker/cards.json`: card data for all 11 listings.
- `build/broker/nlb-broker.css` and `build/broker/broker.html.j2`: the coded version of this page (HTML export baseline).
- `research_design_2026-09-16.md`: the research log behind these choices.
