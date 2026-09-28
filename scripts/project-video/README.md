# A project's video

The owner's order, 28.9.2026: "a video for every project presenting it, the advantages". Built for Rainbow Tel Aviv first.
Same approach as `scripts/broker-video/`: a canvas composer recorded by the installed Chrome's MediaRecorder through
Playwright. No ffmpeg, no downloads. About 45 to 50 seconds, 30 fps, silent (the page plays it muted).

```
capture.py      stills of the project's live 3D stage (read-only, headless Chrome with WebGL)
composer.html   the timeline, drawn on a canvas from data/<slug>.json
render.py       record, frames, posters, inspect (drives composer.html)
verify.html     decodes a finished file and grabs frames (used by render.py frames)
tools/          mp4tools.py (remux to progressive MP4, inspect), sheet.py (contact sheet of frames)
data/<slug>.json  every visible line with its source
img/<slug>/     the stills (captured) and the view cards (copied from the plugin)
out/            <slug>_1920x1080.mp4, _1080x1920.mp4 (10 Mbps), the _web versions (2.5 Mbps), posters (JPG q82)
frames/         check frames decoded from the finished files
```

## The next project, step by step

1. **Facts.** Read the live project page (lead, facts tiles, price section, facilities) and its research file if there is one.
   Only what the page or the research prints goes in. A fact without a source stays out. Prices only as the page prints
   them, with "דווח" and the date, and the page's own caveat. The developer is never presented as us: the outro always
   carries the site's name and "פלטפורמה עצמאית, לא מטעם היזם".
2. **Stills.** `python capture.py --slug <slug> --url https://nad-lan.co.il/projects/<slug>/`
   It makes the stage fill a 1920x1080 and a 1080x1920 viewport (in the headless browser only), waits for the model,
   and saves `img/<slug>/stage-<state>_<w>x<h>.jpg`: `hero`, `hero-noon`, `facilities`, `lot` (same camera, no pins),
   `facility-N` (one card open each), `quarter`, `quarter-own` (other developers' pins, the planned rail stop, school and
   park pins hidden). `capture_<w>x<h>.json` lists what was clicked, the visible pins and card text, and a blank-canvas
   check. **Look at every still** and drop any with glitches, cut text or an empty canvas. Stages without a facilities
   chip or a noon preset simply skip those states.
3. **View cards** (when the project has a tour): copy 2 or 3 of
   `plugins/nadlan-config/assets/project-stage/<project>/tour/*-card.jpg` to `img/<slug>/views/`. The floor and the
   direction come from the file name only (`living-36w` = floor 36, living room, west). The full-size files in that folder
   are 360° panoramas, not usable as flat pictures.
4. **Data.** Copy `data/rainbow-tel-aviv.json` and edit. Every visible string is `{ "text": ..., "source": ... }`.
   Scenes, in order, each with `dur` in seconds (0.5 s crossfades are added between scenes):
   - `title`: `title`, `line`, `small`, over `image` (`landscape`/`portrait` `src` + `focus` [x, y] 0..1), `zoom` in|out.
     Fully drawn from the first frame (messaging apps use it as the thumbnail).
   - `card`: `kicker`, `title`, `lines[]`, `source` over an image; or `"panel": "paper"` with `stats[]`
     (`value`, `caption`) for numbers (two columns in landscape, stacked in portrait). `render: true` puts the
     "הדמיה להמחשה" label on the frame; a paper panel has no picture and no label.
   - `list`: `kicker`, `items[]` (appear one by one), `source` over an image (the facilities).
   - `views`: `kicker`, `items[]` (`src`, `title`, `line`), `source`. Each view is framed on a blurred copy of itself and
     carries "הדמיה להמחשה, נוף משוער" on the picture.
   - `outro`: `kicker`, `actions[]` (`primary` = terracotta; `sub` = a phone number, only the one in the page's own
     WhatsApp link). The site's name, domain and the independence line come from `brand`.
   House style is enforced in the composer: no em or en dashes, no emoji, a number never starts a wrapped line.
5. **Look before recording.** `python render.py stills --project <slug> --size 1080x1920` (and `1920x1080`) draws the
   composer's check list as PNGs into `frames/`. `python tools/sheet.py sheet.jpg frames/still_*.png` makes one sheet.
   Or preview live: `python -m http.server` in this folder, open `composer.html?project=<slug>&w=1080&h=1920`.
6. **Render.** `python render.py all --project <slug>`: both sizes at 10 Mbps and at 2.5 Mbps (`_web`), the check frames
   decoded from the finished files, and both posters (content time 2.0 s). Recording is real time: about 5 minutes for
   four takes. Keep the machine otherwise quiet while it records.
7. **Check.** Look at every frame in `frames/` at full size: Hebrew not clipped and not reversed, readable at phone
   size, the label on every rendering, every line equal to its source in the JSON.
   `python render.py inspect --video out/<slug>_1080x1920.mp4` must show `progressive`, index (`moov`) before `mdat`,
   30 fps, `frames_longer_than_1.5x_33ms: 0`.

## The narrated cut (a voice telling about the project and the area)

8. **Script.** `data/<slug>.narration.json`: one short line per scene (one per view card), only from the data JSON,
   each with `text` (as written), `spoken` (the exact TTS input) and `source`. The site's voice playbook: numbers as
   gender-correct words ("ארבע מאות חמישים ותשע דירות"), dates as words ("עד מרץ אלפיים עשרים ושש"), vowel marks only
   on the risk words (רֵיינְבּוֹ, שְׂדֵה דּוֹב, בּוּטִיק, נַדְלָן), commas and periods for pacing, no SSML. "הדמיה להמחשה" is said once
   (title), the last line ends with "נדל״ן, פלטפורמה עצמאית". Never the chatterbox clone, never an EcoCity clip.
9. **Voice.** `C:\Users\777\nad-lan\voice-rig\venv\Scripts\python.exe narrate.py --project <slug> [--force]`:
   he-IL-AvriNeural at -8% (the site's tours) into `audio/<slug>/<id>.mp3`, measures where the speech starts and ends,
   and writes the timing back into the narration JSON: a scene too short for its line is stretched (the voice is never
   rushed), each view card gets its own length, the facility names are revealed with the voice.
10. **Render.** `python render.py all --project <slug> --narr`: `out/<slug>_<size>_narrated.mp4` (10 Mbps video, AAC
    128 kbps) and `_narrated_web.mp4` (2.5 Mbps, AAC 96 kbps), both sizes. The composer (`&narr=1`) decodes the clips
    with WebAudio, schedules them on the film's clock from the first recorded frame, and records a
    MediaStreamAudioDestinationNode track together with the canvas (H.264 + AAC in MP4, this Chrome supports both).
    `tools/mp4multi.py` remuxes the two-track file (moov first, audio ended with the picture). The run also decodes
    each file's sound in Chrome, measures every line's onset against the plan (`delta_ms`) and saves a 16 kHz WAV.
11. **Listen.** `...\voice-rig\venv\Scripts\python.exe tools\transcribe.py --project <slug> --wav frames\<name>_16k.wav
    --clips <clips.json>`: whisper small per line and for the whole track, next to the script.

Nothing here writes to the site. Uploading the web files and posters to the media library and placing the video on the
project page is a separate, owner-approved release (see `scripts/broker-video/upload_media.py` for the pattern).
