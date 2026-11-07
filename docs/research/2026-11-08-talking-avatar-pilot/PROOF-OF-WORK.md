# HAD-682: actual work and review evidence

Local approval prototype, 7 November 2026. No production deployment. No newly purchased service or paid GPU. The existing website and measurement settings were not changed.

The visual uses the exact approved fictional woman from `../kit/face-a.png`. It follows the actual Claude Design review and the NadLan Instruments palette: ink #0F2233 / #12202A, sea #2F6F86, mist #D3DCE2, white; IBM Plex Sans. Small precise controls and a transparent head avoid the generic cream/gold card treatment. The existing host page styling is retained.

| Tool or method | What actually happened | Evidence |
|---|---|---|
| Blender 5.2 | Built and rendered editable photo-textured 3D facial geometry, subtle mouth deformation, blink overlay, transparent head and neck fade. | `nadlan-advisor-v2.blend`, `assets/nadlan-advisor-v2.glb`, Blender front/angle/wireframe renders in `assets/` |
| Claude Design | Created a real before/after polish specification. Applied right anchoring, head-only crop, disclosure readability and compact controls. | `evidence/claude-design-review.txt`, `.png`; [project](https://claude.ai/design/p/80d1d297-8f1d-4874-8d77-2c7b07d5480f) |
| Gemini | Returned five voice/rendering edge cases. Reviewed critically, not blindly accepted. Its synthetic-tap and 0 dB suggestions are incorrect; its numerical limits are proposals, not standards. | `evidence/gemini-review.txt`, `.png`; [review](https://gemini.google.com/app/c8611a7d2496a4ec) |
| Antigravity CLI | Ran a real read-only code review. Timeout produced a partial review identifying microphone/greeting races, stale cancellation state and queue capacity issues. Those findings were independently reproduced and fixed. | `evidence/antigravity-review-final.json`, cancellation and queue evidence |
| DaVinci Resolve | Launched the installed application and tried its official local scripting interface. The app remained at its Software Update window and the interface did not connect. Closed only this task's startup process. No Resolve edit or render is claimed. | Tool execution history; no fabricated Resolve project |
| Chrome via supported Computer Use | Inspected the real local page and captured actual mobile-size and desktop frames, first trusted interaction, greeting, and close. | `evidence/videos/*-final-capture.json`, final MP4 files |
| FFmpeg | Encoded the observed browser frames and attached the exact original Chatterbox greeting at the measured playback start. No voice replacement or shortened waiting time. | `mux_browser_capture.py`, `evidence/videos/video-provenance.json` |
| Local Whisper, Qwen and Chatterbox | Actual spoken input was transcribed, answered and voiced offline. The microphone input was an explicitly controlled Windows TTS test question, not a recording of Ben. | `evidence/backend-live-microphone.json`, `evidence/backend-microphone-reply-transcription.json` |
| New learned lip analysis | Pinned MIT Talking Avatar 0.3.0, published 2 November, runs locally in a worker and times small mouth openings against the actual audio clock. | `research/current-avatar-review.md`, `research/local-viseme-benchmark.md`, `evidence/visemes/` |
| Independent subagents | Separate geometry/UI, voice backend, and research/QA work; defects were reproduced independently. | `VISUAL-ROUNDS.md`, `BACKEND.md`, `research/interaction-audit.md` |

## Review clips

- `evidence/videos/nadlan-small-avatar-phone-final.mp4`: Chrome at 390×844 CSS pixels, not a physical phone.
- `evidence/videos/nadlan-small-avatar-desktop-final.mp4`: Chrome at 1366×768.
- `evidence/videos/nadlan-small-avatar-conversation-final.mp4`: an actual typed question, fresh local Qwen answer, and spoken reply with learned mouth timing. The verified Chatterbox audio is reused from the earlier successful microphone test (`voiceCacheHit: true`). The complete 21.2-second answer-generation wait is retained. This is not a new-voice generation speed demonstration or a recording of a spoken user question.
- Both use the unchanged existing English greeting, start after a real browser interaction and include a verified closed page at the end.
- Actual capture is approximately 14 unique frames per second; the 30 fps output duplicates frames while preserving timestamps. Do not describe it as 30 unique captured frames per second.
- The final closed state is also captured directly because destroying the idle WebGL canvas can stop the screencast's frame stream. The last actual page capture is held briefly for inspection.

## Full microphone path

`evidence/mediarecorder-chain/receipt.json` records 12 successful checks through a real Chrome MediaRecorder, actual WebM upload, Whisper, Qwen, verified cached Chatterbox audio and 187 learned lip events. It uses a clearly labelled WAV-backed fake microphone device, not Ben's microphone or a mock backend response. Recording start to audible reply was 35.125 seconds. The server processed the cached-voice turn in 28.781 seconds. Closing a second recording stopped its tracks and sent no new question. This is a repeat-answer result, not the speed of producing a new voice recording.

`evidence/backend-persona-checks.json` records real model checks: it identifies itself as a fictional computer-made guide and refuses arranging viewings or negotiating offers. These checks do not constitute exhaustive proof of every possible model output.

## Proven limits

This is inferred, photo-textured frontal 3D geometry, with a permitted viewing range of about ±3 degrees. It is not a complete volumetric reconstruction, a 360-degree head or a full multi-viseme facial rig. Some hair-edge contamination remains visible when enlarged. No claim of superiority over every current avatar is supported.

The research covers relevant primary-source releases in the week ending 7 November, plus clearly dated comparisons outside that week. It is not an exhaustive survey of every avatar made worldwide. Paid providers were researched, not secretly run or purchased.

The original Chatterbox Multilingual microphone test took 236.1 seconds, including 212.9 seconds for voice. The final reply's words matched a separate Whisper check. That is functional local speech, but not a responsive production conversation.

The separately isolated official Chatterbox Turbo ONNX q4 candidate produced the same text with the same reference WAV in 47.73 seconds cold. A nine-word next turn in the already loaded process took 7.176 seconds. Both recordings passed exact-word Whisper checks. The optional persistent-worker integration then measured 59.672 seconds cold and 7.234 seconds for the short warm reply, and verified that cancellation kills its entire owned process with no late audio. These are voice-generation timings, not total conversation latency. An approximate voice-encoder similarity of 0.937 to the approved greeting is not a human listening approval. The existing environment and default Multilingual voice remain unchanged. Candidate audio and receipts are in `evidence/chatterbox-onnx-q4/` and `evidence/optional-voice-integration.json`; see `research/chatterbox-cpu-options.md` for the primary sources and measured comparisons.

The local server listens on this computer only. A public website cannot use a visitor's localhost to reach Ben's computer. On8 November the public route was implemented as a same-origin WordPress queue with this computer polling outbound. No public listener or tunnel was opened here. A genuine public generated reply remains unproved because the low-memory guard currently prevents inference.

On8 November Ben explicitly authorized the single-page replacement and emailed links. The large widget was replaced on page5154 with release `v-1701190a83c6`; the content outside its existing marker block was preserved byte-for-byte. See `PUBLIC-PILOT.md` for current operation and recovery. This is not approval to deploy on another project.

## Further local latency and reliability work

The optional sentence-streaming client passed 17 native browser checks and 33 targeted failure/recovery checks with explicitly controlled backend publication. Two additional native microphone races were reproduced in both archived widgets and fixed in both current widgets, with four passing fixed cases. These checks are not model inference or voice-quality evidence.

Separate real inference benchmarks measured same-model warm answers in 4.33 to 5.91 seconds and English transcription at a 2.50-second warm median. A more aggressive short-answer instruction was rejected for a content-quality regression. The combined inference experiment encountered insufficient free RAM for its existing 3 GiB startup reserve, so no combined first-sentence latency is claimed. See `research/latency-integration-round.md` for sources, exact test scope and remaining work.

## Public pilot evidence, 8 November

The actual anonymous live page passed29 scoped checks on1440px desktop and390px phone viewports: trusted-tap original greeting, real-site obstacle clearance, captions/text, denied microphone recovery, persistent close, homepage exclusion, HTTPS cookie flags and no-store responses. The real `Who are you?` submission returned503 with no job, correctly recorded as unavailable rather than a successful conversation. Receipt: `evidence/public-relay/live-browser/receipt.json`.

Before publication,20 native Chrome→actual local WordPress→actual Python worker controls passed with an explicitly controlled model/audio fixture. These prove transport, playback and cancellation mechanics, not STT/LLM/TTS model performance. Real public speech remains outstanding.

Fourteen public assets were downloaded and matched their SHA256 hashes. WordPress page readback matched exactly. Source audit returned GREEN200 with one H1 and one canonical. Native owner-profile Chrome was also pressed and photographed on both widths. The two local review clips were uploaded as static links, and Ben was emailed the pilot and clips, including the actual voice-availability limitation. No scientific superiority or world-best claim is supported.
