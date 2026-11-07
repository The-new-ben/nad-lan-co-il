# Developer film, version 2 (HAD-678), local build of 7.11.2026

Nothing here was uploaded, posted or committed. Built from Ben's film of 1.11.2026 and the approved 12-scene storyboard
(`design-campaign/project/Film.dc.html`), in the new look.

| File | What |
|---|---|
| `he-16x9.mp4` | Hebrew, 1920x1080, 30 fps, 90.00 s, H.264 (CRF 17) + AAC 192k 48 kHz, moov first, 13.3 MB, -19.9 LUFS |
| `he-9x16.mp4` | the same film laid out for phones, 1080x1920, 90.00 s, 14.3 MB |
| `he-16x9-sheet.jpg`, `he-9x16-sheet.jpg` | contact sheets, one frame every 3 s decoded from the finished files |
| `captures/live/` | the live captures of 7.11.2026 (stage stills, event logs, French and English page elements, screencast sheets) |
| `captures/planner/` | the campaign planner's five steps on a phone (local build) |
| `captures/ben/` | Ben's film one frame per second, and the first frame of every cut-out of his footage |
| `audio/bed.wav` | the music bed (synthesised here, -20 LUFS) |
| `build/` | every script and the film page (below) |

## Look

Survey ground `#F6F8F9` with a 96 px ruled grid, ink `#12202A`, sea `#2F6F86`, sea-deep `#1F4B5C`, one survey magenta `#C42550`
per scene at most (TLV point, the nad-lan source chip, the "דוגמה" label, the end-card rule; in scene 10 the planner's own yearly
total). Karantina for titles, IBM Plex Sans Hebrew for text, IBM Plex Mono for figures and addresses, all drawn by Chrome (no ffmpeg
text). Frames are white with a hairline and two sea corner ticks (survey marks), no rounded soft-shadow cards, no cream, no
terracotta, no gold, no gradients, no emoji. Why not the default look: palette and marks come from marine charts and survey
instruments, cool and high contrast, matching the stage's own noon light.

## Sound

Ben's track is his English voice-over (Whisper: "Right now, a buyer is searching for a new apartment in Tel Aviv..."), not music,
so it is not used. The Hebrew cut carries its words on screen and runs on a quiet synthesised bed (`build/bed.py`, after the house
`music_temp.py`; no third-party audio, no paid voice: ElevenLabs had 4 characters left on 28.10).

## Scenes and the source of every shot

| # | Time | On screen | Source | Real or labelled |
|---|---|---|---|---|
| 01 | 0:00 | Map, lines Paris, London, New York to Tel Aviv; "ברגע זה, קונה בפריז מחפש דירה בתל אביב." | drawn here; coastlines from world-atlas 2.0.2 land-50m (Natural Earth, public) | graphic |
| 02 | 0:07 | Google search typed in French, then the French project page | Ben's film 9.05 to 10.40 s (slowed); live screencast of `nad-lan.co.il/projects/rainbow-tel-aviv-fr/` (HTTP 200, 7.11.2026); 9:16 uses a phone capture of the same page | real, tab says which |
| 03 | 0:15 | The answer of Google's AI Mode | text from `docs/research/2026-11-07-campaign-network/geo-test-2026-11-07.md` and the brief: exact opening sentence, sources en.globes.co.il, shavnu.com, nad-lan.co.il/projects/rainbow-tel-aviv-en/, "AI Mode · Google · 7.11.2026" | a faithful re-set of the answer, in our type, with the line "משפט הפתיחה ורשימת המקורות, כפי שהופיעו בבדיקה ב־7.11.2026" (no screenshot of the answer exists) |
| 04 | 0:22 | Three reasons | element captures of the live English page: the "Average price · About 81,800 ₪ per m² · The developer's reports, up to 3.2026" tile, the FAQ block; the French page's language bar | real |
| 05 | 0:28 | The 3D stage: hover, tap on the tower, floor 23, the sea-side example apartment | live CDP screencast of `/projects/rainbow-tel-aviv/`, driven through the stage's own controls (noon light button, a tap, ArrowUp/Down, ArrowRight); events logged: nl:floor 24 then 23, nl:facing 23-w bearing 270 (`captures/live/stage_*.json`). 0:31 to 0:35 plays at double speed | real |
| 06 | 0:35 | The view from the window, then furnished | Ben's film 30.70 to 32.40 s (UI says "Floor 25 · towards the sea · Example apartment") and 40.50 to 42.60 s | real footage, labelled "הדמיה · דירה לדוגמה" |
| 07 | 0:42 | Recording with the mouse path, then the click heatmap with the empty 3D area beside our stage | Ben's film 61.30 to 63.60 s and 66.60 to 71.20 s; our live stage screencast next to it with "את הבניין משלבים מהבמה שלנו" and "מפת הלחיצות לא מקליטה את התלת ממד, לכן המשטח שם ריק." | real |
| 08 | 0:52 | Israel phone, UK desktop, France phone, Australia phone | Ben's film 58.50 to 60.90 s and 64.00 to 66.10 s (slowed to about a third) | real; the UK panel shows a building as in Ben's film, labelled "הבניין: מהבמה שלנו" |
| 09 | 1:00 | The click on contact, then the WhatsApp message to the developer | Ben's film 72.10 to 73.90 s; the message card is made here | the card is labelled "דוגמה" and "הודעה לדוגמה, לא פנייה אמיתית" |
| 10 | 1:08 | The campaign planner on a phone, five steps | `build/capture_planner.py`: the local planner build (`build-nlcamp/preview.html`), its own controls (France and Canada, investors, ₪25,000 a month, existing page); the project field holds "הפרויקט שלכם" instead of the verify run's test address | real screens of the local build (not live on the site yet) |
| 11 | 1:16 | Three rows of the comparison | the table in `design-campaign/project/Main.dc.html` (checked 7.11.2026); immobilier's lead cell is shortened to "מייל או SMS" (the table's "או מערכת לקוחות" dropped under the no-tech-words rule) | our table, "נבדק באתרים של כל שירות, 7.11.2026." |
| 12 | 1:24 | "שיווק פרויקט נדל״ן לקונים בחו״ל", "בנו את הקמפיין שלכם", nad-lan.co.il, five languages | | end card |

Ben's footage is cut out of his cream frames (crop rectangles in `build/prep_assets.py`), upscaled x2, and re-framed in the new
look. His captions, cream background and pills are not in the new film.

## What could not be captured

- No screenshot of the AI Mode answer exists; scene 3 re-sets the recorded text (see the label on screen).
- `/international-campaigns/` (the planned page) answers 404 today, so the end card shows only `nad-lan.co.il`.
- The planner is a local build; the film shows it as built, not as a live page.
- The view-from-the-floor map window under the stage was not captured (scroll target off screen in the headless run); scene 6 uses
  Ben's view footage instead.
- The UK panel's building: Hotjar does not record the 3D canvas, so that picture was placed in Ben's film; it is labelled as ours.

## Rebuild (local)

```
python build/capture_live.py stage <scratch>/film2/live 1920x1080      # and 1080x1920
python build/capture_live.py pages <scratch>/film2/live
python build/capture_langbar.py <scratch>/film2/live
python build/capture_fr_phone.py <scratch>/film2/live
python build/capture_planner.py <scratch>/film2/planner
python build/prep_assets.py <scratch>/film2                            # Ben's cut-outs, 30 fps casts, stills, land.json
python build/bed.py 90 audio/bed.wav
python build/render.py frames <scratch>/film2 h --workers 5            # and v
python build/render.py encode <scratch>/film2 h he-16x9.mp4 audio/bed.wav
python build/sheet.py he-16x9.mp4 he-16x9-sheet.jpg
```

`build/film.html` is the whole film (both layouts, `?f=h` / `?f=v`, `window.render(t)`); `build/ben_probe.py` and `ben_listen.py`
are the checks of Ben's film; `probe_stage.py`, `probe_tower.py` and `live_common.py` the stage probes (analytics requests are
blocked in the capture browser, so the captures add no visits to Hotjar or Analytics).
