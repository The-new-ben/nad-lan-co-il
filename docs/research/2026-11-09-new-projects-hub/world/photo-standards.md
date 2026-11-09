# Photo standards: how the leaders keep listing photos consistent

Measured on 9.11.2026.

**How the measurements were taken:**
- **Photo shapes:** read live in the owner's Chrome with a DOM script. It measured the width-to-height ratio of every image box wider than 150 px, counted native `loading="lazy"`, and recorded photo counters and labels.
- **Rules:** the policy rules marked [prior] are known industry practice, not re-checked today.

## 1. Measured shapes (rendered boxes)
| Site | Surface | Dominant ratio | Count | Lazy | Notes |
|---|---|---|---|---|---|
| Redfin | New-homes search cards | **1.50 (3:2)** | 50 of 54 large images | 48/72 | Very uniform |
| Redfin | Community page | **1.50 (3:2)** | 24 | 27/50 | Same ratio as search |
| Realtor.com | Search cards | **1.50 (3:2)** | 19 of 19 | 20/30 | "Photo 1 of 3" counter |
| Zillow | Search cards | **~1.72** | 27 | 2/49 | JavaScript-virtualised list; in-card carousel |
| Zillow | Plan page hero / gallery tiles | ~1.84 / ~1.56 | 27 / 16 | 6/81 | "See all 40 photos" |
| NewHomeSource | Community cards | **1.78 (16:9)** | 40 | 42/66 | — |
| Booking.com | Search cards | **1.00 (square)** | 20 | 29/30 | Square crop hides inconsistent sources |
| Compass | Development hub | **0.75 (3:4 portrait)** | 21 of 21 | 0/23 | Editorial architecture look |
| Rightmove | Cards | (not measured, fetch only) | — | — | "1/16" counter, floor-plan and virtual-tour icons [fetch] |

**The pattern:** every leader uses **one ratio per surface**. The same ratio appears on the search card and on the community page, so a project never "jumps" between list and detail. The mass-market portals have converged on **3:2** (Redfin, Realtor) or close to it (Zillow 1.72, NHS 16:9). Luxury (Compass) breaks the convention on purpose, with a portrait editorial crop.

## 2. First-photo rules
- **[prior] US MLS practice:** the primary photo is the **front exterior** of the property. Many MLS rules forbid logos, agent photos or text overlays on the first photo, and many require a minimum resolution.
- **[prior] Builder sites (NewHomeSource, Zillow new construction):**
  - community cards lead with the **community's best exterior or amenity shot**
  - plan cards lead with the **elevation rendering**
  - quick move-in homes lead with a **real exterior photo** once the home is built
- **[code] Zillow** shows an "Exterior design options" carousel (Design 1–5) separate from the photo gallery, so renders of the elevation options are not mixed into the real photos.

## 3. Renders versus real photos: labelling
- **[prior] UK (Rightmove):** new-home renders carry a "CGI" or "computer generated image" caption, under advertising-standards practice.
- **[prior] Australia (Domain):** "Artist impression" on renders.
- **[prior] US:** "Virtually staged" disclosure is required by many MLSs when furniture is added digitally. Builders add "Photos may show upgraded features / model home" disclaimers.
- **[code] Zillow:** "Report a problem" exists on data rows; photo-level reporting is [prior].

## 4. Placeholders and missing media
- **[code] NewHomeSource:** shows "Pricing coming soon" instead of a fake price. Media follows the same principle: no stock photo of another building.
- **[prior] Leaders** show a neutral branded block (name and map tile) when no photo exists, never a misleading image.
- **[code] Skeleton loaders:** none were detected by class name on these pages (they use JavaScript placeholders and native lazy loading instead). This is not a strong signal either way.

## 5. Standard for nad-lan /projects/ (combining the leaders with the owner's laws)
| Rule | Standard |
|---|---|
| Ratio | **3:2 everywhere in the mass hub** (cards, project page gallery tiles, city hubs). Luxury collections may use **3:4 portrait** as a separate, deliberate line. One ratio per surface, never mixed inside a row. |
| First photo | The **building exterior**. A real photo if it is built or occupied; otherwise the developer's render. Never an interior first, never a logo, never text baked into the image. |
| Labels on every image (a small corner chip) | **"צילום אמיתי"** (real photo) only on real photos (owner law). **"הדמיה"** (render) on every render. **"דירה לדוגמה"** (model apartment) on model-apartment images (owner law 25.9). **"צילום אוויר"** (aerial photo) for drone shots. **"התקדמות בנייה · אוקטובר 2026"** (construction progress, with the month) for dated site photos. |
| Never | A white-box 3D model as "the picture" (owner law). A stock photo of another place. An AI image presented as real. Amateur photos on a sales surface. |
| Missing photo | A neutral block with the project name, city and a map tile. No fake image and no "image coming soon" text. Unknown is omitted, not announced. |
| Counter and media icons | "1/16", plus icons for תוכנית (plan) / 360 / סרטון (video) / מודל תלת־ממד (3D model), only when that media exists. |
| Alt text | "[project], [street], [city] – חזית / הדמיה / דירה לדוגמה – סלון" (façade / render / model apartment – living room). It says what the photo is and whether it is real. |
| Technical | `width` and `height` attributes, or CSS `aspect-ratio: 3/2`, to stop layout shift. Responsive `srcset`. WebP or AVIF. First row `loading="eager"` + `fetchpriority="high"`; everything else `loading="lazy"`. At most 5 photos in a card carousel. |
| Order inside the gallery | Exterior → aerial/location → lobby and amenities → model-apartment interiors (labelled) → plans → construction progress (dated). |
| Source line | "תמונות: [developer], באדיבות" (photos: courtesy of [developer]) under the gallery, matching the rule that developer marketing data is published as is, with credit. |
