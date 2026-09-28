ion cannot request approval. Separately, one GitHub directory response unexpectedly included temporary authenticated download URLs in tool output; they are not reproduced here.
tokens used
252,061
## 1. LiveKit (the video call)

**I located the Hadmaya integration, but could not verify a populated LiveKit Cloud project or recover its public URL.** No files were changed.

The relevant repository is `The-new-ben/courtai`, locally at `C:\Users\777\Documents\ChatGPT-Work\courtai`.

- `supabase/functions/video-sessions-api/index.ts` reads `LIVEKIT_SERVER_URL`, `LIVEKIT_API_KEY`, and `LIVEKIT_API_SECRET`.
- `supabase/functions/hearings/index.ts` also references LiveKit credentials.
- The corresponding Supabase project is **worklaw-leads**, ref `mlnwpocuvjnelttvscja`. I verified that `video-sessions-api` is deployed. Credential presence and validity remain unverified.
- Look in that project’s **Edge Functions → Secrets**, then the owner’s LiveKit Cloud dashboard. I found no independently verified DUO configuration.

**Yes, nad-lan can share the project.** Its tokens already restrict access to room names prefixed `nadlan-`. Unique room names plus room-scoped tokens separate calls; they do **not** separate billing, quotas, or administrative authority. Prefer a dedicated nad-lan API-key pair within the same project. [LiveKit token documentation](https://docs.livekit.io/home/server/generating-tokens)

Paste these three corresponding items into:

`https://nad-lan.co.il/wp-admin/options-general.php?page=nadlan-together`

| Dashboard item | WordPress option |
|---|---|
| Project WebSocket URL, `wss://…livekit.cloud` | `nadlan_tr_lk_url` |
| API key belonging to that project | `nadlan_tr_lk_key` |
| Matching API secret | `nadlan_tr_lk_secret` |

The form exists in `plugins/nadlan-config/inc/together.php:747`; the secret field is write-only. A participant JWT is **not** the API secret.

## 2. Hebrew voice for our films

**The strongest recorded Hebrew result is Chatterbox Multilingual + Dicta.** The deployed Hadmaya speech function records Ben’s 27 September blind ratings over 20 Hebrew sentences: **4.7/5 versus 2.9/5 for OpenAI**. This is an owner preference result, not population-level proof; I did not independently listen or reproduce it.

Define **H** as:

`C:\Users\777\Documents\ChatGPT-Work\courtai-voice-science-2026-09-27`

The reproducible implementation is:

- `H\services\chatterbox\`: `app.py`, `runtime.py`, `hebrew.py`, `settings.py`, `assets.lock.json`.
- Engine: `chatterbox-tts==0.1.7`; pinned `ResembleAI/chatterbox` checkpoint `t3_mtl23ls_v2.safetensors`.
- Hebrew preparation: pinned Dicta ONNX; preserve source letters and supplied niqqud.
- Study voice: `shimmer` maps to seat `judge-female`, reference `services/chatterbox/assets/judge-female.wav`.
- Baseline: exaggeration **0.5**, CFG **0.5**, temperature **0.8**; seed was not exposed.
- Current `speechDelivery.ts` offers bounded acting controls: warm/calm **0.4/0.5**; confident **0.55/0.45**. These are candidates for film auditions, not the proven winning settings.
- Experiment: `H\research\voice-science-20260927\run-experiment.mjs`.
- Hosted service: Hugging Face Space `Benben777/hadmaya-hebrew-chatterbox`.

The older `C:\Users\777\nad-lan\voice-rig\clone-test*.py` uses an Avri-derived reference. Retain it as historical evidence; do not revive EcoCity content.

**Credential locations:** Chatterbox connection configuration lives in `C:\Users\777\Documents\jus-tice-secrets\chatterbox\gateway.env`; service authentication in `service-token.txt`. The existing authorized Hadmaya gateway grant is in `...\jus-tice-secrets\hadmaya\access-codes-20260922.json`. Reuse through the gateway, preserving its quotas.

**ElevenLabs:** deployed server code reads Supabase secret **`ELEVEN_LABS_API_KEY`**; another function accepts `ELEVENLABS_API_KEY` too. I found no local ElevenLabs key in the inspected locations; current credits were not tested. For Hebrew, audition **`eleven_v3` + Sarah (`EXAVITQu4vr4xnSDxMaL`)**, stability **0.5**. For English, audition **Brian (`nPczCjzI2devNBz1zQrb`)** with `eleven_multilingual_v2`; French/Russian can use that model too. Hebrew requires the Hebrew-capable model, not Multilingual v2. [Language support](https://elevenlabs.io/docs/help-center/other/what-languages-do-you-support)

**Exact Windows generation recipe:** commands below are provided for later execution, not run here. Prepare `he.txt` and `en.txt`, one short sentence per nonempty line, approximately 90–110 words each. This generates one WAV per sentence and an exactly 50-second combined WAV; it refuses to truncate oversized narration. Requires an active Chatterbox grant and available service. The Python launcher could not start inside this restricted session.

```powershell
$env:NARRATION_REPO = 'C:\Users\777\Documents\ChatGPT-Work\courtai-voice-science-2026-09-27'
@'
import os,re,json,base64,urllib.request,io,wave,uuid
from pathlib import Path
root=Path(os.environ["NARRATION_REPO"])
cfg=(root/"src/integrations/supabase/config.ts").read_text(encoding="utf-8")
key=re.search(r"const FALLBACK_ANON_KEY = '([^']+)'",cfg).group(1)
grant=json.loads(Path(r"C:\Users\777\Documents\jus-tice-secrets\hadmaya\access-codes-20260922.json").read_text(encoding="utf-8"))["pro"]
url="https://mlnwpocuvjnelttvscja.supabase.co/functions/v1/text-to-speech-openai"
for lang in ("he","en"):
    lines=[s.strip() for s in Path(lang+".txt").read_text(encoding="utf-8-sig").splitlines() if s.strip()]
    assert lines and all(len(s)<=500 for s in lines)
    pcm=b""; session="film-"+str(uuid.uuid4())
    for i,text in enumerate(lines):
        body=dict(text=text,language=lang,provider="openai",voicePolicy="participant",
                  voice="shimmer",role="judge",sessionId=session)
        req=urllib.request.Request(url,data=json.dumps(body).encode(),
            headers={"Content-Type":"application/json","apikey":key,"x-hadmaya-access":grant})
        with urllib.request.urlopen(req,timeout=120) as response:
            result=json.load(response)
        assert result.get("provider")=="chatterbox","Unexpected provider"
        audio=base64.b64decode(result["audioContent"])
        with wave.open(io.BytesIO(audio),"rb") as w:
            assert (w.getnchannels(),w.getsampwidth(),w.getframerate())==(1,2,24000)
            pcm+=w.readframes(w.getnframes())+bytes(8640)
        Path(f"{lang}-{i:02}.wav").write_bytes(audio)
    assert len(pcm)<=50*24000*2,"Shorten script; narration exceeds 50 seconds"
    with wave.open(f"{lang}-50.wav","wb") as w:
        w.setparams((1,2,24000,0,"NONE","not compressed"))
        w.writeframes(pcm+bytes(50*24000*2-len(pcm)))
'@ | & 'C:\Users\777\nad-lan\voice-rig\venv\Scripts\python.exe' -B -
```

**Film integration:** `narrate.py` currently accepts project JSON, not arbitrary text, and assumes MP3. Claude should replace `synth()` with a provider adapter, support WAV filenames/duration measurement, and retain speech-onset analysis. Use sentence clips matching scene IDs; enforce the 50-second editorial budget rather than silently extending scenes.

No ffmpeg is needed: `composer.html` already combines WebAudio with canvas capture; `render.py --narr` records H.264/AAC and `tools/mp4multi.py` remuxes both tracks. After adaptation:

```powershell
# From scripts/project-video, using the existing render environment:
python render.py all --project rainbow-tel-aviv --narr
```

This re-records the composition; `mp4multi.py` alone does not add audio to a silent MP4.

## 3. UX: the floor card covers the 3D model

**Use a docked inspector, with selection independent of panel visibility.**

The obstruction is explained by `rainbow/stage.js:1395`: `placeLabel()` positions `.rbs-label` every frame and clamps it inside the stage. `labelClose` currently calls `clearFloor()`, destroying selection.

- **Desktop:** reserve a 320–360px logical-end column; render the model in the remaining viewport. Minimize to a compact selected-floor tab.
- **Phone:** stage-local bottom sheet with **56px collapsed**, **35%**, and **65%** snap points. Start compact. Drag the handle downward to collapse; preserve floor/direction.
- Keep rotation available outside the sheet. Use 44px controls, keyboard collapse, focus restoration, safe-area padding, and reduced motion.

Concrete changes:

1. Add `setInspectorState()`; separate collapse from `clearFloor()`.
2. Stop `placeLabel()` applying transforms to pinned inspectors; retain lightweight hover labels.
3. Update `resize()`, `floorFrame()` and `frameFloor()` to frame selection inside the unobscured rectangle; recalculate after snapping and orientation changes.
4. Edit `rainbow/stage.css`; use `assets/nlds/nlds.css` tokens. `bridge.js` keeps existing `nl:floor`, `nl:facing`, and action contracts.
5. Test 320/390/1440px, rapid selection, RTL, keyboard, and ray-picking after viewport changes.

References: [VisEngine Sobha One](https://visengine.com/portfolio/interactive-3d-masterplan-sobha-one/) for building-to-unit continuity; [Realspace](https://www.the-boundary.io/work/jervois-and-lawrence-apartments) for immersive apartment exploration. The docking prescription is my recommendation, not a claim those products implement these exact snaps.

Claude Design must precede visible implementation.

## 4. Breakthroughs for the presentation (graphics and technology)

`studio_kit.py` explicitly builds furniture from primitives. `rainbow_interior.py` already uses Cycles, denoising and AgX. **Increasing samples alone will not fix asset quality.**

Estimates below are prototype engineering effort and incremental USD cash, excluding labor; they are planning allowances, not quotations.

| # | Concrete option and handoff | Effort / cash / principal risk |
|---|---|---|
| 1 | Replace primitive furniture with scanned assets; real-scale PBR fabric, wood and stone. Lab `labs/interior-quality`; Claude integrates into `studio_kit.py`. [Poly Haven: CC0](https://polyhaven.com/license); paid Fab assets require asset-specific licence review. | 3–5 days / $0–300 / downloadable-asset redistribution rights |
| 2 | Match exposure, daylight and practical lights against one photographic reference; calibrated materials before 8K panoramas. Lab comparison; Claude updates `rainbow_interior.py`. | 2–4 days / $0–100 / CPU render time |
| 3 | Bake indirect lighting and AO into optimized GLBs; retain dynamic direct sun. Lab `labs/baked-interior`; Claude integrates scene loading. [Three.js materials](https://threejs.org/docs/pages/MeshStandardMaterial.html) | 4–7 days / $0–100 / UV seams, double lighting |
| 4 | Capture a real showroom as Gaussian splats, with collision mesh and annotations. Lab `labs/splat-room`; Claude integrates viewer. [SuperSplat](https://developer.playcanvas.com/user-manual/gaussian-splatting/editing/supersplat/) | 5–10 days / $100–1,000 / capture access, mirrors, mobile memory |
| 5 | WebGPU progressive path tracing for a stationary “inspect finishes” mode; raster fallback during movement. Lab `labs/pathtrace-room` first. | 7–15 days / $0–200 / device support, heat, convergence |
| 6 | Continuous lobby → lift → corridor → apartment/gym/pool walk using connected geometry, collision and streamed zones. Lab one route; Claude integrates navigation. | 15–30 days / $0–500 / missing architectural geometry |
| 7 | Make shops separately pickable meshes with verified unit IDs, frontage, area and availability. Lab `labs/commercial-picking`; Claude integrates stage events. | 3–6 days / $0–100 / invented tenancy or stock |
| 8 | Obtain developer sales-plan PDFs plus IFC/DWG, revision and publication permission. Cross-check municipal permit plans by address/parcel. Lab plan registration; Claude publishes sourced inventory. [Tel Aviv archive](https://pre.tel-aviv.gov.il/Residents/Construction/Pages/Archive.aspx) | 2–5 days after receipt / $0–300 / permit plan differs from sale plan |
| 9 | Per-apartment sun exposure: georeferenced facade, surrounding buildings, dated sun position, ray-tested obstruction. Lab `labs/unit-sun`; Claude integrates an explicitly estimated result. | 5–10 days / $0–200 / inaccurate neighboring geometry |
| 10 | Compare two units using synchronized view, plan, sunlight and verified facts; retain identity into tour/design/contact. Extend `labs/unit-journey`; Claude integrates contracts. | 5–8 days / $0–100 / mismatched IDs and revisions |

Prioritize **1, 2, 8, 10**. They improve buyer confidence before expensive rendering research. Proposed labs were not created.

## 5. Marketing breakthroughs

Pitch Africa Israel with **DUO**, which its [official project page](https://afi.duo-tlv.com/) identifies as its development. Use Rainbow as a separate capability demonstration.

| # | Experiment | Measure |
|---|---|---|
| 1 | DUO pilot covering a small verified inventory in EN/FR/RU | Attended qualified appointments per eligible visitor |
| 2 | Shareable selected-unit link preserving floor, direction and language | Recipient return-to-unit and appointment rates |
| 3 | Scheduled multilingual shared-viewing rooms with partners abroad | Booking-to-attendance; attendance-to-next-step |
| 4 | Three localized 50-second films, each answering one buyer concern | Completion → project visit → qualified appointment |
| 5 | Dated unit evidence pack: plan, view, specification, availability | Pack recipients progressing to a sales meeting |
| 6 | “Choose between these two apartments” comparison session | Shortlist completion and decision time |
| 7 | Native-language neighborhood briefs connected to relevant units | Organic visits producing qualified shortlists |
| 8 | Consent-based referral pilots with relocation professionals | Accepted referrals and attended meetings by source |
| 9 | Resume a saved shortlist across devices and family members | Seven-day return rate and assisted appointments |
| 10 | Developer pilot report joining engagement to sales-team outcomes | Incremental appointments, opportunities and verified sales |

Use language cohorts, consistent qualification criteria, and a comparison group where traffic permits. Views and clicks are intermediate signals, not revenue.

A read-only Supabase URL query was blocked by the approval gate because this session cannot request approval. Separately, one GitHub directory response unexpectedly included temporary authenticated download URLs in tool output; they are not reproduced here.
