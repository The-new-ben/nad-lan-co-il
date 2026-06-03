# Advertiser User Manual — Studio Page (`/studio/`)

> **Who this is for.** Any advertiser (contractor, יזם, real-estate professional)
> who claimed a card on nad-lan.co.il and wants to make it world-class — **with
> zero technical knowledge**. Also: support staff helping advertisers; QA running
> the יעל / Rainbow-Project journey.

---

## 1. What is the Studio?

The Studio is a single web page where advertisers manage everything about their
card on nad-lan.co.il: photos, description, contact details, social-media links,
videos, and an exact map pin — all without ever entering wp-admin.

**URL:** `https://nad-lan.co.il/studio/`
**Requires:** a logged-in WordPress account that owns the card (or admin).

---

## 2. How to get there in 30 seconds

1. The advertiser must first **claim their card** (the "זה הכרטיס שלכם?" button
   on the public profile page). Owner approves the claim, advertiser logs in.
2. Once logged in, visit `https://nad-lan.co.il/studio/` →
   the page lists every card the user owns.
3. Click a card → enters the Studio editor.

---

## 3. What every section does

| Section | What it does | Saved on |
|---|---|---|
| **תמונות** | Drag-and-drop photo upload; first photo becomes the cover; click ✕ to delete. JPG/PNG/WEBP up to 10MB. | Each upload — auto-save |
| **סיפור העסק** | Tagline + full description. Five "AI assist" buttons (improve / shorter / longer / professional / friendly) call our Claude concierge to rewrite the text. | Click "שמירה" |
| **מפה** | Leaflet + OpenStreetMap map. **Drag the pin** to your exact location — lat/lng update automatically. | Click "שמירה" |
| **פרטי הפרויקט / פרטי בעל המקצוע / פרטי הנכס** | Type-specific fields (units / status / יזם · התמחות / ותק · מחיר / חדרים / מ״ר). | Click "שמירה" |
| **מיקום ויצירת קשר** | עיר, כתובת, טלפון, אימייל, אתר. | Click "שמירה" |
| **רשתות חברתיות** | Facebook / Instagram / TikTok / YouTube links — appear as coloured pills on the public profile. | Click "שמירה" |
| **וידאו** | Paste a YouTube or Vimeo URL — embedded as a 16:9 player on the public profile. | Click "שמירה" |

---

## 4. The "save" button and what happens when you click it

- The big black-and-gold **"שמירה"** button at the top right sends a single
  REST call (`POST /nadlan/v1/studio/<id>/save`) with every field.
- A green toast **"✓ נשמר. כל השינויים חיים."** confirms success.
- A red toast means the server rejected something — usually:
  - field too long (truncate),
  - email not valid,
  - URL not a URL.
- **Image uploads save themselves immediately** — no need to click שמירה for them.

---

## 5. The AI copy assistant (✨ buttons)

Below the description there are 5 buttons:

| Button | What it does |
|---|---|
| ✨ שפר טקסט | Improve clarity + tone, keep facts. |
| קצר | Compress to 3 sentences max. |
| הרחב | Expand to 5–7 sentences with the same facts (no fabrication). |
| רשמי | More professional/formal tone. |
| חם ואנושי | Warmer, more human tone. |

**Requirements:** the owner must configure an Anthropic API key in
*wp-admin → Settings → NadLan AI*. Without it the buttons return a friendly
error explaining how to enable.

**Cost:** ~$0.001 per call (Claude Haiku).

---

## 6. The map picker (Leaflet + OpenStreetMap)

- **Drag the marker** to your exact location.
- **Click anywhere on the map** to move the marker.
- Lat/Lng update in the hidden fields automatically.
- Click "שמירה" to persist.
- Map tiles come from openstreetmap.org — **free, no Google API bill**.

---

## 7. Public-page rendering — what advertisers actually get

After Save, the public profile page renders:

- **Photos** as a gallery (already supported via `cards-render.php`).
- **Social links** as branded pills (Facebook blue, Instagram pink, TikTok
  black, YouTube red, Website gold).
- **Video** as an embedded 16:9 player (YouTube or Vimeo).
- All other fields appear in the existing facts table + premium profile header.

---

## 8. Troubleshooting (most common things that go wrong)

| Symptom | Cause | Fix |
|---|---|---|
| "אין הרשאה" page when entering /studio/?id=N | Card owner ID does not match the logged-in user | Verify the claim was approved + the WP user matches |
| Photo upload fails with "bad_type" | File is not JPG/PNG/WEBP/GIF | Convert to JPG |
| Photo upload fails with "too_big" | File > 10MB | Resize before upload |
| AI buttons return "AI_DISABLED" | No Anthropic API key set | wp-admin → Settings → NadLan AI → paste key |
| Map shows blank tiles | OpenStreetMap CDN blocked by network | Try another network; OSM has no API key needed |
| Save returns red toast | A field failed sanitization | Open browser DevTools → Network → see which field |
| Public profile doesn't show new photos | Page caching (Yoast/host) | Clear cache; the studio invalidates the social-proof transient automatically but not 3rd-party page caches |

---

## 9. What is NOT yet in this Studio (honest gap list)

These are flagged in `BACKLOG.md` and will land in v1.42+:

- **Drag-to-reorder gallery** — current gallery shows photos in upload order;
  delete and re-upload to reorder for now.
- **AI image generation in-browser** — possible once an image API key is set
  (OpenAI Images / Stability / Replicate). Hook exists; UI is TODO.
- **Onboarding wizard** (4-step "first claim" walkthrough) — currently the
  Studio loads with current data; no guided tour for new advertisers yet.
- **Advertiser analytics dashboard** (impressions/leads/position over time) —
  basic view counts already render on `/studio/`. Full chart dashboard TODO.
- **Floor plans / 360° / Matterport** — for advanced project marketing.
- **Watermarks on uploaded images** — for advertiser branding protection.

These gaps are real and intentional — we ship a solid foundation and let QA
discover which gaps actually hurt advertisers before building more.

---

## 10. For the QA agent (יעל / Rainbow journey checklist)

When running Journey 2 (the Rainbow Project advertiser):

- ✅ Photo upload works (drag-drop + click).
- ✅ Description editor with AI assist exists.
- ✅ Map picker exists (Leaflet / OSM).
- ✅ Social links + video URL fields exist and render on public page.
- ⚠️ AI assist requires API key (note "AI_DISABLED" if not set).
- ❌ Drag-reorder gallery — not yet built (flag as ⚠️ friction).
- ❌ Impressions/exposure dashboard — basic counts only (flag as ⚠️).
- ❌ Project image AI generation — not yet built (flag as ⚠️).
- ❌ Post-payment onboarding flow — not yet wired (the advertiser must
  manually find /studio/ — flag as ❌ for paid journey).

---

## Revision log
- 2026-06-03 — Created (Claude). Pairs with `inc/studio.php`,
  `inc/studio-rest.php`, `inc/profile-extras.php` in plugin v1.41.0.
