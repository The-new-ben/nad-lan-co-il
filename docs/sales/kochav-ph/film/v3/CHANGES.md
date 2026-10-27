# Kochav HaTzafon film, v3 (27.10.2026): what changed from v2, and why

Local build only. Nothing here was uploaded to the site, the plugin or git.

| File | What it is |
|---|---|
| `kochav-film-en-v3.mp4` | English narration, English captions. 2:07.3, 1920x1080, 30 fps, H.264 + AAC 48 kHz, -16.0 LUFS |
| `kochav-film-en-v3-he.mp4` | The same cut and sound, with Hebrew captions, titles, cards and end card |
| `kochav-film-v3.jpg` | Poster: Meital's own photograph of the living room, graded as in the film, with the watermark |
| `frames.jpg` | One frame every 5 s of the English cut, with the time on each frame |
| `compose_v3.py`, `narration_v3.json`, `tts_v3.py` | The build, the text and the voice script (v2's `compose.py`, `narration.json` and `audio/` are untouched) |
| `film_en.ass`, `film_he.ass`, `timeline_v3.json` | The titles and captions as built, and where every shot sits |

v2 = the published `web/kochav-film-en-v2.mp4` (2:10.2; the web-size encode of the local build `kochav-film-en.mp4`, same length). The v2 times below are from v2's `film.ass` and a frame check of the local v2 build.

## 1. Price per square metre: removed everywhere

| v2 time | Removed | Replaced by (v3 time) |
|---|---|---|
| 1:27.5 to 1:31.9 | Card "NIS 49–51K · per m², the average home in Kochav HaTzafon · Bizportal, July 2026" | Card "NIS 6.1M · median home deal in Kochav HaTzafon, 2023 to Oct 2025 · 4th highest in Israel · Mako" (1:25.6 to 1:34.9) |
| 1:32.0 to 1:36.4 | Card "NIS 90K+ · per m², new homes in the neighbourhood · Bizportal, July 2026" | Card "2028 · planned opening of the Green Line light rail · Maariv, Aug 2025" (1:39.1 to 1:42.2) |
| 1:41.4 to 1:47.9 | Card "+$136 · per m² for homes within 100 m of Yarkon Park · Technion, Shefer & Zakai, 2003" | Card "100 m · homes this close to Yarkon Park were worth more · Technion study, Shefer & Zakai, 2003" (the finding, without its money figure) (1:42.7 to 1:46.9) |
| 1:27.5 to 1:36.4 | Narration: "Homes in Kochav HaTzafon average around fifty thousand shekels per square metre, and new homes here reach ninety thousand and more." | "Between 2023 and October 2025, the median home deal in Kochav HaTzafon was NIS 6.1 million, the fourth highest in Israel." (neighbourhood figure from Mako, never this home's price) |

Kept cards: "16,000 · new homes planned in the Sde Dov quarter" and "+5% to 20%+ · home values next to new city park links abroad (HR&A, 2014)". The tag "Area data, not a valuation of this home" stays on the whole numbers scene.

## 2. Tall buildings that do not exist: every such shot removed

Every shot rendered from our 3D city, and every photoreal still made from it that shows the surroundings, is out. Lifestyle stills with an invented tower skyline are out; two of them survive only as crops below the horizon (no buildings at all). Every tower now in the film is a real one, in Meital's own photographs and video.

| v2 time | Removed shot | Why | Now in its place (v3 time) |
|---|---|---|---|
| 0:00.0 to 0:04.4 | `real_aerial` (photoreal still made from the 3D city) | dense invented tower blocks around the home | Meital's drone video over the neighbourhood (0:00.0 to 0:02.9) and her drone photo of the neighbourhood, the football pitches, Yarkon and the sea (0:02.9 to 0:07.2) |
| 0:18.5 to 0:22.4 | `real_centre` (photoreal from 3D) | high-rise blocks behind the shops | nothing: the centre keeps its three lifestyle illustrations (café, deli, nut shop), none with towers |
| 0:34.4 to 0:38.8 | 3D walk on the bridge (`shots3d/walk`) | grey 3D towers on the horizon | Meital's drone photo: the neighbourhood, the pitches and Yarkon today (0:29.8 to 0:36.2) |
| 0:38.7 to 0:47.5 | `real_bridge_day` (photoreal from 3D) | invented glass towers behind the bridge | the planned-bridge simulation, cropped tight (see below) |
| 0:47.3 to 0:50.8 | `park_run` illustration | invented tower skyline | Meital's drone video of the real skyline over the park (0:45.5 to 0:48.0) |
| 0:50.8 to 0:54.1 | `sport` illustration (full frame) | towers on the horizon | same illustration cropped below the horizon, no buildings (0:52.0 to 0:54.3), labelled "Illustration" |
| 0:54.0 to 0:58.0 | `park_family` illustration (full frame) | towers behind the river | same illustration cropped below the horizon (0:48.0 to 0:52.0), labelled "Illustration" |
| 1:17.6 to 1:25.6 | `bbq` illustration | a party in front of an invented wall of towers, read as the home's view | Meital's video of the covered terrace (1:18.9 to 1:23.7) |
| 1:25.4 to 1:37.6 | `real_aerial` again (numbers backdrop) | invented towers | the real view from the terrace, from Meital's reel (1:23.5 to 1:34.0) |
| 1:37.5 to 1:56.2 | `night` illustration | terrace party over an invented night skyline | Meital's drone photo of the Sde Dov quarter under construction (1:34.0 to 1:42.6) and her photo of the covered terrace and its view (1:42.6 to 1:53.3) |
| 1:56.0 to 2:01.8 | 3D night bridge (`shots3d/night`) | 3D tower blocks | Meital's dusk video of the terrace (1:53.2 to 1:56.7) |

Kept simulation: v2 0:29.5 to 0:34.4, `real_bridge_top` (the planned bridge). In v3 (0:36.2 to 0:45.6) it is cropped to the boulevard, the bridge and the lawns only (no building in frame) and its label changed from "Planned bridge · illustration" to "Planned bridge · simulation".

Real footage kept from v2: the drone opening (re-trimmed, and the crop moved down: in v2 a ghost of Meital's burned-in Hebrew caption showed at the top of the frame around 0:04), the home, the terraces, the dusk terrace. New labels on every aerial: "Aerial video of the area", "Aerial photo of the neighbourhood", "Aerial photo · the neighbourhood and the park today", "Aerial photo · the Sde Dov quarter under construction", so no aerial reads as the view from the home.

## 3. Tennis courts and football pitches

v2 0:47.8 to 0:57.1 narration "...running paths along the river, cycling, tennis, the sports centre, and long Saturdays on the lawn." becomes "...running paths along the river, cycling, and long Saturdays on the lawn. And right by the home, tennis courts and football pitches." (caption 0:53.4 to 0:57.5). The line plays over Meital's drone video that shows the courts and pitches beside the neighbourhood (0:54.3 to 0:57.6). Her drone photo also shows the pitches at 0:02.9 and 0:29.8.

## 4. A NEW home in a NEW building

- Opening line under the title (v2 "A mini penthouse in north Tel Aviv, between the city and Yarkon Park") is now "A new mini penthouse in a new boutique building · north Tel Aviv" (0:01.0 to 0:05.8).
- Chapter "THE HOME" is now "A BRAND-NEW HOME" (0:57.8).
- Narration (v2 0:58.3) "Back home, almost two hundred square metres on the eleventh floor." is now "Back home, a brand-new mini penthouse of about 197 sqm, on the eleventh floor."
- End card line: "A new home in a new boutique building, north Tel Aviv".

## 5. End card (2:01.5 to 2:07.3)

v2 (2:04.0 to 2:10.2): "5 rooms · 197 m² · 74 m² sun terrace · 3 exposures · floor 11 of 12", then the phone in small type: "Private viewing   Meital Katzir · Nadlan Al HaYam · +972 52-363-1582".

v3, English:

    Mini penthouse · Kochav HaTzafon
    A new home in a new boutique building, north Tel Aviv
    5 rooms · about 197 sqm · about 80 sqm of terraces · floor 11
    PRIVATE VIEWING
    Meital Katzir · Nadlan Al HaYam          (70 px)
    052-3631582                              (118 px, bold)
    From abroad +972 52-363-1582 · nad-lan.co.il

v3, Hebrew cut: מיני פנטהאוז · כוכב הצפון / נכס חדש בבניין בוטיק חדש, צפון תל אביב / 5 חדרים · כ-197 מ״ר · כ-80 מ״ר מרפסות · קומה 11 / לתיאום צפייה פרטית / מיטל קציר · נדל״ן על הים / 052-3631582 / nad-lan.co.il

"3 exposures" was dropped: Meital's own posts say 3 in some and 4 in others.

## 6. Areas only as "about"

- Narration and caption: "about 197 sqm" (home) and "about 80 sqm of terraces" (v2 1:16.3 "a seventy-four square metre sun terrace, open on three sides" is now "And then, the real living room: about 80 sqm of terraces."; "open on three sides" dropped as not verified).
- End card: "about 197 sqm · about 80 sqm of terraces" (v2 had the exact "197 m²" and "74 m²").

## 7. Sound and length

- Regenerated with the same temporary voice (gpt-4o-mini-tts, "marin", same instructions): park, home, terrace, numbers. Open, morning, centre, bridge and close reuse v2's recordings. Each new take was screened by speech recognition; two terrace takes that began "Then the..." were heard as German ("Dann der...") and rejected (kept in `audio/rejected/`), so the line now begins "And then, ...".
- The numbers line was shortened to fit the 2:10 limit (the first wording ran 34.8 s; the used take is 28.9 s).
- Captions are timed to the pauses in the voice and checked word by word against speech-recognition timestamps.
- Music: the same self-made temporary bed (`music_temp.py`), regenerated at the new length. Meital's licensed reel music is not used.
- Length 2:07.3 (v2 2:10.2). Loudness -16.0 LUFS integrated, true peak -1.4 dBFS (both cuts).

## 8. Checks run on the final files

- Frames every 2 s of both cuts looked at one by one: no per-m² figure, and no tower that is not in Meital's real photographs or video.
- Grep of `film_en.ass` and `film_he.ass` for "m²", "sqm", "per m", "למ״ר": no "m²", no "per m", no "למ״ר". "sqm" / "מ״ר" appear only in "about 197 sqm" and "about 80 sqm of terraces" (home caption, terrace caption, end card).
- Full decode (`ffmpeg -v error -i file -f null -`) of both cuts: no errors.
- Still open: the temporary voice says "Sde Dov" slightly unclearly in the new numbers take; the final film is to be voiced by Meital anyway.
