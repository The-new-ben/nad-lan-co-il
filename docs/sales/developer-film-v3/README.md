# Developer film, version 3 (HAD-678), local build of 7.11.2026

English voice-over, Hebrew subtitles, for the CEO of a large Israeli developer. Nothing here was uploaded, posted or committed;
no Linear or Notion entry was written by this build.

| File | What |
|---|---|
| `en-vo_he-sub_16x9.mp4` | 1920x1080, 30 fps, H.264 CRF 17 + AAC 192k 48 kHz, moov first: 2:25.59, 25.5 MB, -16.0 LUFS integrated, true peak -1.5 dBTP |
| `en-vo_he-sub_9x16.mp4` | the same film laid out for phones, 1080x1920: 2:25.59, 26.2 MB, -16.0 LUFS integrated, true peak -1.5 dBTP |
| `en-vo_he-sub_16x9-sheet.jpg`, `en-vo_he-sub_9x16-sheet.jpg` | contact sheets, one frame every 3 s decoded from the finished files |
| `voice/` | the six test takes (`tests/`), the 36 takes of the chosen voice (`bm_george/`), the placed voice track (`vo_en_bm_george_final.flac`), why this voice (`choice.json`), the Whisper screening of the final mix (`whisper_check.json`) |
| `campaign-check.md`, `campaign-check/` | the check of 12 developers' live project pages and 5 Meta Ad Library searches: method, table, screenshots, raw JSON |
| `captures/` | the live captures of 7.11.2026: stills, one contact sheet per screencast, the screencasts' timing files and capture logs (the raw screencast frames stay in the build scratch folder) |
| `audio/bed.wav` | the music bed: v2's own generator (`../developer-film-v2/build/bed.py`) run at the new length, -20 LUFS |
| `build/` | every script and the film page (below) |
| `SCRIPT.md` | Ben's script of 7.11 (unchanged); the film follows it with the owner's two rounds of corrections (below) |

## What the film says (as voiced; scene start times)

| # | Start | Voice-over (English, as said) | Hebrew subtitle (burned in) |
|---|---|---|---|
| 01 | 0:00.0 | Right now, a buyer in Paris is looking for a home in Tel Aviv. Another in London. Another in Ra'anana. | ברגע זה, קונה בפריז מחפש בית בתל אביב. עוד אחד בלונדון. ועוד אחד ברעננה. |
| 02 | 0:08.6 | You can build a beautiful render. You can buy ads. Every developer does. | אפשר לבנות הדמיה יפה. אפשר לקנות מודעות. כל יזם עושה את זה. |
| 03 | 0:14.8 | We checked the live project pages of twelve leading Israeli developers. Ten stop at the render and a form. None lets the buyer step inside and pick his floor. | בדקנו את עמודי הפרויקטים החיים של 12 יזמים מובילים בישראל. עשרה נעצרים בהדמיה ובטופס. באף אחד מהם הקונה לא נכנס לבניין ובוחר קומה. |
| 04 | 0:27.1 | What no one sells you is all of it, working together, on one buyer. Your marketing department runs the campaign. We are the special unit you send in for one mission: bringing you buyers who are ready to sign. | מה שאף אחד לא מוכר לכם: את הכל, עובד ביחד, על קונה אחד. מחלקת השיווק שלכם מובילה את הקמפיין. אנחנו היחידה המיוחדת שאתם שולחים למשימה אחת: להביא לכם קונים שמוכנים לחתום. |
| 05 | 0:42.7 | When he searches in his own language, he finds your project. On Google, and in the AI answers buyers now ask. We know how to put you there. | כשהוא מחפש בשפה שלו, הוא מוצא את הפרויקט שלכם. בגוגל, ובתשובות ה־AI. אנחנו יודעים לשים אתכם שם. |
| 06 | 0:53.2 | He doesn't just look at a render. He lands inside it. | הוא לא רק מסתכל על הדמיה. הוא נוחת בתוכה. |
| 07 | 0:57.3 | He picks the floor. He sees his view. He furnishes the apartment and leaves his notes. | בוחר קומה. רואה את הנוף שלו. מעצב את הדירה ומשאיר הערות. |
| 08 | 1:04.5 | He can walk the neighbourhood as it will be, after your building is built. And we're now taking it into VR, inside the apartment. | הוא מסתובב בשכונה כמו שהיא תיראה אחרי שהבניין ייבנה. ועכשיו אנחנו מכניסים את זה למשקפי VR, בתוך הדירה. |
| 09 | 1:14.0 | Prices, the neighbourhood, the numbers. A complete decision room for your project. | מחירים, השכונה, המספרים. חדר החלטות שלם לפרויקט שלכם. |
| 10 | 1:20.3 | These are real buyers. Israel. The UK. France. Australia. Checking the area, the maps, the renders. Choosing, and reaching out. | אלה קונים אמיתיים. ישראל, בריטניה, צרפת, אוסטרליה. בודקים את האזור, את המפות, את ההדמיות. בוחרים, ופונים. |
| 11 | 1:32.0 | One tap opens a live video meeting inside the project page. Your team, the buyer, his family, anyone he wants to bring, looking at the same floor plan together. | לחיצה אחת פותחת פגישת וידאו בתוך עמוד הפרויקט: הצוות שלכם, הקונה, המשפחה שלו וכל מי שהוא רוצה לצרף, מסתכלים יחד על תוכנית הדירה. |
| 12 | 1:43.9 | You don't get a name and a phone number. Floor twenty-three. Sea view. In French. This isn't a lead. It's a buyer who already knows what he's buying. | לא מקבלים שם וטלפון. קומה 23, לים, בצרפתית. זה לא ליד. זה קונה שכבר יודע מה הוא קונה. |
| 13 | 1:55.4 | From there, our team stays with him all the way to the signed contract. We don't let him slip away. | משם הצוות שלנו נשאר איתו עד החוזה החתום. לא נותנים לו לברוח. |
| 14 | 2:02.5 | The big money is abroad right now. We're there. And we're here, in Israel. | הכסף הגדול נמצא עכשיו בחו״ל. אנחנו שם. וגם כאן, בארץ. |
| 15 | 2:08.7 | Pick your markets, your buyers, your budget. Your campaign can be live in seven days. | בוחרים שווקים, קונים ותקציב. הקמפיין יכול להיות באוויר תוך שבעה ימים. |
| 16 | 2:15.7 | More buyers. Bigger budgets. Your next project. nad-lan.co.il, slash marketing. | יותר קונים. יותר תקציב. הפרויקט הבא שלכם. nad-lan.co.il/marketing (on the end card, not as a subtitle) |

Changes against `SCRIPT.md`, all from the owner's corrections of 7.11 evening or for length (no claim added):
- Scene 2 drops "You can get traffic" and "Renders are easy today" (traffic is not the point any more; length).
- Scene 3 states the check exactly: 12 live project pages, 10 stop at renders and a form, 2 add a 360 view, 0 let the buyer step
  into the building and pick a floor (`campaign-check.md`). The developers are not named on screen.
- Scene 4 adds the positioning line (second correction, verbatim); "That's what we built" dropped for length.
- New scene 8: the quarter walk as planned for 2035, then VR (Ben's words; on screen "VR · בפיתוח · המחשה", no date).
- Scene 10 (recordings) gets more time and the line "Checking the area, the maps, the renders"; no tool name anywhere.
- Scene 11: the video meeting line of the second correction, verbatim, over the live page's shared viewing room.
- Scene 12: "You get a buyer who already chose" replaced by the owner's line "This isn't a lead. It's a buyer who already knows
  what he's buying."
- Scene 15: "goes live in seven days" became "can be live in seven days" (the page states seven days as the target).
- Scene 16: the end card of the second correction, verbatim, then nad-lan.co.il/marketing.
- "We're the special unit" is said "We are the special unit" (all six test voices were heard as "where the").
- Never said or shown: how we get into Google or AI answers, the word broker, lead or traffic counts, guarantees.
  v2's scene "למה מצטטים אותנו" and its source close-ups are gone.

Length: 145.59 s (2:25.59), 16 scenes, 36 voice takes, 39 subtitle lines. Longer than the 2:15 the owner allowed for, because every line of both corrections is kept verbatim at a calm pace.

## Voice and sound

- Engines tried, free and local only (per `C:/Users/777/Documents/agent-tools/VOICE-REUSE-INDEX.md`): Kokoro-82M v1.0 fp32
  (am_michael, bm_george, af_heart) and VibeVoice-Realtime-0.5B on the CPU (en-Carter_man, en-Frank_man, en-Grace_woman), the
  same 12 to 15 s line. No Chatterbox gateway, no paid GPU, no ElevenLabs.
- Chosen: **Kokoro bm_george** (British, male), speed 1.0. Why, in short: low and steady (median 140 Hz, 3.9 semitone spread),
  the cleanest sound of the six (noise floor -93 dB), the clearest to Whisper, and full bandwidth; the two VibeVoice male voices
  are cut hard at 8 kHz (their prompts are 16 kHz audio) and the VibeVoice female voice has a -56 dB noise floor. All measurements
  and the takes are in `voice/`. Nobody listened in this build: the choice rests on these measurements, so Ben should play the six
  test takes; any other voice drops in with one command (below) and the picture follows its timing.
- Each subtitle group is one generation; `vo_build.py` trims each take, lays it on the timeline with set pauses (0.32 s inside a
  scene, longer before a punch line), splits two-line groups at the pause in the take itself, and times every Hebrew line to it.
- Mix: the voice at -16 LUFS, v2's bed under it, ducked 12 dB while the voice speaks (0.2 s look-ahead, 0.25 s down, 0.8 s up,
  pauses under 1.6 s stay ducked), the whole mix normalised to -16.0 LUFS integrated, true peak -1.5 dBTP.
- Whisper small (cached, CPU) on the final mix: 19 raw word differences in 336 script words (`voice/whisper_check.json`). Read one by one, none is a mispronunciation: British versus American spelling (neighbourhood), "V R" written "VR", "we're" written "we are", "None" written "Non", the words "Floor" and "More" counted in the next window (the full transcript has "Floor 23" and "More buyers"), "nad-lan.co.il" written ".co .il", and "Ra'anana" written "Rannanet" (Whisper does not know the name; the voice says ra-a-NA-na). Before the fixes the check also caught "lead" heard as "laid" (fixed by lengthening the vowel) and "We're the" heard as "where the" (now "We are the"). Screening only, not a listening test.

## Look

The v2 look, unchanged: survey ground `#F6F8F9` with a 96 px ruled grid, ink `#12202A`, sea `#2F6F86`, sea-deep `#1F4B5C`, one
survey magenta `#C42550` per scene at most (the TLV point, our page among the AI sources, the "0" of the check, the arrow to
"buyers ready to sign", the highlight ring in the room, the "דוגמה" labels, the end-card rule). Karantina, IBM Plex Sans Hebrew,
IBM Plex Mono, all drawn by Chrome, including the subtitles (RTL, one or two lines; checked on every still). White frames with a
hairline and two sea corner ticks; no cream, no terracotta, no gold, no gradients, no emoji. Why not the default look: palette and
marks from marine charts and survey instruments, cool and high contrast.

## Every shot, its source, and what is real

| # | On screen | Source | Real or labelled |
|---|---|---|---|
| 01 | Route chart: Paris, New York, London, then a zoom to Israel and Ra'anana | drawn here; coastlines world-atlas 2.0.2 land-50m (Natural Earth, public), from v2 | graphic |
| 02 | A wall of 12 renders, "ממומן" chips on four, then a lead form | OUR OWN renders from the plugin's project tours (`plugins/nadlan-config/assets/project-stage/`: Kikar Hamedina cards, Rainbow and DUO facility panoramas, centre crops); the form is drawn here | tab "הדמיות כמו בכל קמפיין · מתוך ההדמיות שלנו · ללא שם פרויקט"; form labelled "טופס טיפוסי"; no other company's image or logo |
| 03 | The check: 12 page outlines, 10 / 2 / 0 | `campaign-check.md` (7.11.2026) | real count, no developer named |
| 04 | Black, the mark, then "מחלקת השיווק שלכם" under "נדל״ן · היחידה המיוחדת" and "קונים שמוכנים לחתום" | drawn here | graphic |
| 05 | Google typed in French, the French project page, the AI Mode answer | Ben's film 9.05 to 10.40 s; v2's live screencast of `/projects/rainbow-tel-aviv-fr/` (phone page in 9:16); the answer re-set as in v2 from `docs/research/2026-11-07-campaign-network/geo-test-2026-11-07.md` | real; the answer is labelled "התשובה, כפי שהופיעה בבדיקה ב־7.11.2026" (no screenshot of it exists) |
| 06 | Into the Rainbow stage | v2's live screencast of `/projects/rainbow-tel-aviv/` driven by its own controls | real |
| 07 | Floor 23 on the stage, then the 360 example apartment (floor 25, toward the sea): bare, "בהיר", "עם ריהוט · עץ חם", and the room's notes list | v2 stage cast; NEW screencast `captures/tour360/` (the page's own 360 viewer and its "עיצוב הדירה" choices, 7.11.2026, HTTP 200); the notes card is a crop of the room capture of scene 11 | real UI; renders labelled "הדמיה" and "דירה לדוגמה" (the viewer's own labels plus the tab). The 360 exists for floors 10, 25 and 36, so the view is floor 25 |
| 08 | The Sde Dov quarter, "הרובע 2035", free walk; then the roof pool of the 360 in two lens shapes | NEW screencast `captures/walk/` of `/tour/sde-dov/` (HTTP 200; its own 2035 switch and walk control); the pool from the 360 screencast | walk labelled "הדמיה לפי התוכנית"; the VR picture is labelled "VR · בפיתוח · המחשה" (VR does not exist yet) |
| 09 | The one-map section, the price box, the price tile, sold apartments | NEW element captures of the Hebrew Rainbow page (`captures/rainbow/`, HTTP 200): `#nlpjx-map`, the top of `#nlpjx-price` (its table of neighbouring projects cut off, no other project named), the facts tile, the top of `#nlps-deals` | real |
| 10 | Israel phone, UK desktop, France phone, Australia phone; the Israel desktop mouse path; the click map with our stage beside it; the click on contact | Ben's film (as v2): 58.5 to 60.9, 64.0 to 66.1, 61.3 to 63.6, 66.6 to 71.2, 72.1 to 73.9 s | real recordings, labelled by country and device only, no tool name; the UK building and the inset are labelled "הבניין: מהבמה שלנו" |
| 11 | The hero button "שיחת וידאו עם נציג", then the shared viewing room ("בשידור חי · 5 משתתפים") on the plan of floor 23, tiles for the rep, the buyer, his partner, a friend, an interior designer, three pinned notes | NEW: element capture of the live page; `build/capture_room.py` ran the live page's own room (`?room=` of an id that does not exist) with every room API call answered inside the capture browser and a stand-in for the LiveKit library (`build/fake_livekit.mjs`, connects to nothing, no cameras, so tiles show initials) | real interface; participants, names and notes are demo, labelled "משתתפים והערות לדוגמה". Nothing was created on the site |
| 12 | "שם / טלפון" crossed out, then the WhatsApp message with floor 23, sea, French, what he saw, 3 notes | drawn here (as v2) | labelled "דוגמה" and "הודעה לדוגמה, לא פנייה אמיתית" |
| 13 | Mortgage calculator, purchase-tax calculator, the "שיחת וידאו עם נציג נדל״ן" booking band | NEW screencasts of `/mortgage-calculator/` and `/purchase-tax-calculator/` (HTTP 200), phone stills in 9:16; the booking band of the Rainbow page | real |
| 14 | The route chart again, then Ra'anana, Haifa, Jerusalem, Ashdod to Tel Aviv | drawn here | graphic |
| 15 | The campaign planner on a phone, five steps, and "7 ימים" | NEW: the LIVE planner of `/marketing/` on a phone (`captures/planner/`, HTTP 200): France and Canada, investors, 25,000 a month, existing page "הפרויקט שלכם"; step 5 shown, never sent (its endpoint also blocked in the capture browser) | real |
| 16 | יותר קונים. יותר תקציב. הפרויקט הבא שלכם. nad-lan.co.il/marketing | drawn here | end card (no subtitle: the card is the line) |

## What was not used, or could not be captured

- `/brokers/` (H1 "מתווכי נדל״ן") and `/professionals/` (real brokers' names and licence numbers) were captured or checked but are
  NOT in the film: they would show the word broker and private people. Scene 13 shows the mortgage and purchase-tax calculators and
  the booking band instead.
- The apartment designer `/tour/designer/` was captured (`captures/designer/`) but left out: its low-poly interior is below the
  premium level the owner asked for; the 360 tour's furnished renders carry "he furnishes the apartment" instead.
- `/compound/sde-dov/` and `/projects/hamedina/` answer 200 (captures in `captures/hamedina/`); the walk beat uses the Sde Dov
  tour only (its 2035 switch is the "as it will be" picture).
- The stage's "view from the floor" window needs a pick on the tower; the headless tap did not register (as in v2), so the view is
  the 360 tour's floor 25.
- The AI Mode answer has no screenshot (as in v2): re-set with its date.
- `/international-campaigns/` still answers 404; the end card points to `/marketing/`.

## Rebuild (local)

```
# voice (voice-rig venv python), then the timeline, subtitles and mix
python build/voice_kokoro.py test voice/tests
python build/voice_vibevoice.py test voice/tests                         (vibevoice-env python)
python build/voice_compare.py voice/tests
python build/voice_kokoro.py lines build/script_v3.json voice/bm_george bm_george 1.0
python ../developer-film-v2/build/bed.py <seconds> audio/bed.wav
python build/vo_build.py voice/bm_george <scratch>/film3/audio --bed audio/bed.wav
# captures (installed Chrome, headless; analytics blocked in the capture browser)
python build/capture_rainbow.py captures/rainbow
python build/capture_room.py captures/room 1920x1080 --lk                 (and 1080x1920)
python build/capture_v3.py tour360|walk captures/<x> 1920x1080            (and 1080x1920)
python build/capture_v3.py planner captures/planner ; python build/capture_v3.py pages captures/pages
# assets, frames, files
python build/prep_v3.py <scratch>/film3 captures                          (needs v2's <scratch>/film2/web)
python build/render.py frames <scratch>/film3 h --workers 5               (and v)
python build/render.py encode <scratch>/film3 h en-vo_he-sub_16x9.mp4 <scratch>/film3/audio/mix.wav
python build/sheet.py en-vo_he-sub_16x9.mp4 en-vo_he-sub_16x9-sheet.jpg
python build/whisper_check.py <scratch>/film3/audio/mix.wav <scratch>/film3/audio/timeline.json voice/whisper_check.json
```

`build/film.html` is the whole film (both layouts, `?f=h` / `?f=v`, `window.render(t)`); the scenes and subtitles follow
`timeline.json`. `build/script_v3.json` holds every voiced line, its Hebrew subtitle and the pronunciation fixes.
`build/campaign_check.py` and its helpers are the campaign check's scripts.
