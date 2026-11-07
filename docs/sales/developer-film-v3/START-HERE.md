# הסרט של נדל״ן ליזמים: מתחילים כאן

**מה זה.** התיקייה הזאת היא סרטון קצר שמתאר את היכולות שלנו: קול באנגלית, כתוביות בעברית, מסך רחב וטלפון. כל גרסה של
הסרט היא קובץ אחד בתיקייה `variants`. לא מתחילים סרט מאפס: מעתיקים גרסה קיימת, משנים את המשפטים, ובונים בפקודה אחת.

**הסרט שאושר.** הגרסה `main-he`. הקבצים בתיקייה הזאת: `en-vo_he-sub_16x9.mp4` (מסך רחב), `en-vo_he-sub_9x16.mp4` (טלפון),
`he-web-16x9.mp4` (הקובץ שבאתר) ו־`poster-16x9.jpg`. הוא באוויר בעמוד https://nad-lan.co.il/marketing/#film (קובץ מדיה 8833),
ומהלילה גם בעמוד האנגלי /en/marketing/. משנים אותו רק במילה של בן.

**גרסאות בעבודה (טיוטות, רק תסריט, עוד לא הוקלטו):**
- `smaller-developer`: ליזמים קטנים יותר. אותה חוויה לקונה, בלי מחלקת שיווק גדולה ובלי תקציב גדול.
- `marketing-department`: לצוותי השיווק אצל היזמים. איזו פנייה מגיעה אליהם, מה הקונה כבר בחר, ואיך זה עובד לצד הקמפיינים שלהם.

**איך מבקשים גרסה חדשה.** כותבים לסוכן משפט אחד: למי הגרסה, מה לשנות בטקסט, ובאיזו שפה. הסוכן מעתיק גרסה קיימת, כותב את
המשפטים, בונה, בודק, ושולח קישור לצפייה. שום דבר לא עולה לאתר בלי אישור.

**הכללים בכל גרסה.**
- לא מסבירים איך אנחנו מגיעים לגוגל ולתשובות של מנועי הבינה המלאכותית. רק "אנחנו יודעים לשים אתכם שם".
- המשפט על מנועי הבינה המלאכותית מזכיר את ChatGPT, את Gemini ואת Claude.
- בלי מספרי תנועה, בלי מספר פניות, בלי הבטחות.
- לא מזכירים את שם הכלי שמקליט את הגולשים. ההקלטות מסומנות רק במדינה ובמכשיר.
- אף פעם לא המילה מתווך.
- מוכרים את איכות הפנייה: "זה לא ליד. זה קונה שכבר יודע מה הוא קונה."
- בגרסה לצוותי שיווק: אנחנו עובדים לצד הקמפיינים שלהם ומוסרים להם קונים שכבר בחרו.
- בלי קווים מפרידים ארוכים.
- בכל מה שגלוי לציבור (כיתוב באתר, שם הקובץ שעולה, כותרת המדיה, התמונה הראשית, כרטיס הסיום): "סרטון קצר שמתאר את
  היכולות שלנו". לא כותבים שם למי הגרסה מיועדת, ולא שהיא עוקפת את מחלקת השיווק.

---

## For agents: the exact steps

Read `C:/Users/777/Documents/agent-tools/FILM-STUDIO.md` first (the one place for every agent on this computer).

Two folders:
- **FILM** = `C:/Users/777/nad-lan/nad-lan-co-il/docs/sales/developer-film-v3/` (this folder, in the public repo): `variants/`,
  `build/` (scripts and the film page), `voice/` (the approved film's takes and voice tests), `captures/` (stills, contact sheets of
  every screencast), `campaign-check.md`, finished films. Every variant except `main-he` writes its finished files to `out/<name>/`.
- **WORK** = `C:/Users/777/Documents/film-studio-work/nadlan-developer-film/` (outside the repo; big, partly Ben's own footage, never
  commit or upload it): `web/` (every picture the film page draws, shared by all variants), `casts_raw/`, `var/<name>/` (one
  variant's sound, frames, stills, the subtitle check strips).

### 1. Copy a variant

```
copy variants\main-he.json variants\<new-name>.json
```
In the copy set: `"name": "<new-name>"`, `"status"` (DRAFT...), `"audience"` in neutral words, `"outputs": {"dir": "out/<new-name>", ...}`,
`"voice": {"takes": "out/<new-name>/voice", ...}`, and `"poster"` (the scene id and line the poster frame is taken from).
The two drafts (`smaller-developer.json`, `marketing-department.json`) are good starting points too.

### 2. Edit the lines

Every scene is one **picture module** of `build/film.html` (`"module": "s05"`); each module at most once per variant, in any order.
Inside a scene, every `group` is one voice take and one or two subtitle lines:
```
{"en": "the English voice-over line",
 "he": ["the Hebrew subtitle"]                      or two lines: ["first", "second"] with "split": [0.5] (where in the take),
 "say": "how the engine should say it",            (optional: spelling for the voice, e.g. "Nad lan dot co dot eel")
 "ph": [["lˈiːd", "lˈiːːd"]],                       (optional: a phoneme fix the spelling cannot carry)
 "gap": 0.6}                                       (optional: the pause before this line, default 0.32 s)
```
Scene `"lead"` / `"tail"` are the breaths before and after its words. `"screen": {"key": "text"}` replaces the words marked
`data-t` in that module. A Hebrew subtitle line longer than about 55 characters becomes two lines on the phone cut; more than two
lines stops the build.

| Module | What it shows | Lines it times to | `screen` keys |
|---|---|---|---|
| s01 | route chart, Paris and New York, London, then a zoom to Israel and Ra'anana | 1: Paris; 2: London, then Ra'anana | |
| s02 | wall of OUR OWN renders, "ממומן" chips, then a typical lead form | 1: the wall and the chips; 2: the form | formTitle, formText |
| s03 | the check: 12 live project pages, 10 / 2 / 0 | 1: the pages; 2: 10 and 2; 3: the 0 | title |
| s04 | black, the nad-lan mark, then the positioning diagram | 1: black, the mark at its end; 2: the band; 3: the unit and the goal | band, bandNote, unit, unitNote, goal |
| s05 | Google typed in French, our French project page, the AI Mode answer | 1: search, then page; 2: the answer card; 3: our page marked | |
| s06 | into the live 3D stage of Rainbow | 1 | |
| s07 | floor 23, the 360 example apartment bare, furnished, the notes list | 1: floor, then view; 2: furnished, notes near its end | |
| s08 | the Sde Dov quarter walk as planned for 2035, then VR (labelled "בפיתוח · המחשה") | 1: walk; 2: VR | |
| s09 | the one-map section, price box, price tile, sold apartments | 1 | |
| s10 | Ben's real visitor recordings (country and device only), the click map, the contact click | 1: four countries; 2: mouse path then click map; 3: contact | |
| s11 | the "שיחת וידאו עם נציג" button, then the shared viewing room on the plan (demo participants) | 1: the tap; 2: the participants, then the plan | |
| s12 | a bare "name, phone" lead, then the WhatsApp message (labelled "דוגמה") | 1: bare lead; 2: floor, view, language; 3: the big words | bigA, bigB |
| s13 | mortgage calculator, purchase-tax calculator, the booking band | any | |
| s14 | route chart again, then Israeli cities to Tel Aviv | 2: the zoom to Israel | |
| s15 | the live campaign planner on a phone, five steps, "7" | 2: the "7" | sevenN, sevenText |
| s16 | end card, no subtitle (its words are the card) | 1: three lines; 2: the address | line1, line2, line3, url |

The picture labels are Hebrew and the page is right to left: a variant with other subtitles needs those labels translated first.

### 3. Build: one command

```
cd C:/Users/777/nad-lan/nad-lan-co-il/docs/sales/developer-film-v3
python build/film.py --variant <name>
```
About 15 minutes on this PC: the voice (Kokoro bm_george, local, free; only new or changed lines are voiced), the mix and the
subtitle timing, every frame in both layouts, the two films, the web cut, the poster, the contact sheets, the subtitle check and
Whisper. Parts: `--only voice,mix` or `--from frames`. A new script can be seen on screen before anything is voiced:
`python build/film.py --variant <name> --only dry` (guessed timing, one still per scene, sheets in `WORK/var/<name>/dry/`).

`python build/film.py` with no flag rebuilds the approved film (main-he). An approved film is never written over its published
files: the rebuild goes to `out/_rebuild-main-he/` (compare with `python build/compare_films.py . out/_rebuild-main-he`;
replace the published files only on Ben's word, with `--replace-approved`). The check of 7.11.2026 (`build/rebuild-check-main-he.txt`):
the same voice, timeline, subtitles, sound bytes, poster, durations and 4,419 frames per film; the picture equal to the eye but
not to the byte in a few image-heavy stretches (lowest PSNR 48 dB). Any other check run: `--out out/_check-<name>`.

The single steps, if needed (each takes `--variant <name>`; no flag = main-he):
```
C:/Users/777/nad-lan/voice-rig/venv/Scripts/python.exe build/voice_kokoro.py variant     the takes
C:/Users/777/nad-lan/voice-rig/venv/Scripts/python.exe build/vo_build.py                 mix, bed, subtitle timing, timeline
python build/prep_v3.py [--assets]                                                       timeline to the film page (--assets: rebuild the shared pictures)
python build/render.py frames h|v [--workers 5] ; python build/render.py encode h|v      frames and films
python build/render.py web                                                               the 1280x720 site copy (CRF 26, AAC 128k, faststart)
python build/poster.py [--at <seconds>]                                                  the poster
python build/render.py stills h 12.5,40 ; python build/sheet.py <film.mp4> <sheet.jpg>   stills, contact sheet
C:/Users/777/nad-lan/voice-rig/venv/Scripts/python.exe build/whisper_check.py            Whisper on the mix
```

### 4. The checks (look, do not assume)

- **Whisper:** the build prints every line whose words differ from the script; the file is `out/<name>/whisper_check.json`.
  Read each one: digits for words, British or American spelling and a word counted in the next window are fine; a real
  mishearing is fixed with `"say"` (spelling) or `"ph"` (phonemes), then `--only voice,mix` and the rest again.
  ChatGPT, Gemini and Claude are said right with plain spelling (checked).
- **Hebrew subtitles, right to left:** open `WORK/var/<name>/subtitles_check_h.jpg` and `_v.jpg` (every line, drawn in each
  layout). Hebrew reads right to left, English names stay whole and in place ("ChatGPT, Gemini ו־Claude"), two lines at most.
- **Contact sheets:** `out/<name>/en-vo_he-sub_16x9-sheet.jpg` and `_9x16-sheet.jpg`, one frame every 3 s. Look at every tile:
  nothing cut off, labels "דוגמה" / "הדמיה" / "המחשה" where they belong, no other company's name or logo.
- **Sound:** both films at -16 LUFS (printed by the mix step).

### 5. The web cut and the poster

Made by the build: `out/<name>/he-web-16x9.mp4` (1280x720, H.264 high, CRF 26, AAC 128k, faststart, aim under 15 MB) and
`out/<name>/poster-16x9.jpg` (1280x720, under 200 KB, no subtitle box). Publishing is Ben's call; upload names and media titles
stay neutral (for example `nadlan-capabilities-he.mp4`, "סרטון קצר שמתאר את היכולות שלנו").

### 6. The film index

```
python C:/Users/777/Documents/agent-tools/build_video_index.py
python C:/Users/777/Documents/agent-tools/video_index_head.py
```
