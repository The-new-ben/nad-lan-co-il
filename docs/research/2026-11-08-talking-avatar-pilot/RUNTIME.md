# Local browser runtime

This is an approval prototype. Nothing here deploys the character or changes the live page.

The UI inherits the prior Claude Design NadLan Instruments identity: ink `#0F2233` and `#12202A`, sea `#2F6F86`, mist `#D3DCE2`, IBM Plex Sans. A small transparent portrait replaces the old card. Its shape and palette follow the site's own design, with no cream, gold, terracotta or generic gradient treatment.

## Include

Serve this folder over localhost, link `widget.css`, and include `widget.js` as a module. All Three.js code, the model, textures, voice and lip cues are local files. Third-party runtime requests are not required.

Optional configuration must appear before the module:

```js
window.__NL3D = {conversationEndpoint: '/api/converse'};
```

Without a conversation endpoint the microphone and text-question form are absent. The existing recorded English greeting still works. The caption panel is collapsed by default.

## Interaction

The first trusted pointer-up or eligible keyboard event calls `audio.play()` immediately. There is no timed autoplay attempt and no browser-policy override. It also works when the first interaction precedes the visual reveal. Close, captions, microphone and text-question controls do not inadvertently start the greeting.

The portrait button pauses, resumes or replays. The small status pill shows Tap to hear, Speaking and Hear again, or the current conversation state. Portrait and outside taps do not start the greeting during microphone permission, active recording, a pending response or speech analysis. Close hides the entire character, pauses sound, closes microphone tracks, aborts pending client requests, requests backend job cancellation, cancels animation, releases WebGL and persists the existing `nlag-closed` key. A subsequent page load does not load the model for a visitor who already closed it.

The runtime measures the site's `#nlcta` WhatsApp and `#nla11y` accessibility controls and positions itself above any that overlap its horizontal area. It is anchored 12 pixels from the right on phone and 24 on desktop. Resize, scroll, safe-area and visual viewport changes are considered. Mobile portrait dimensions are 118 by 142 CSS pixels with a total 144 by 166 footprint, desktop 150 by 174 with a total 176 by 198 footprint. Separate 44-pixel touch targets remain available around the head, alongside the computer-made disclosure at 10/12 pixels on phone and 11/14 on desktop. Expanded captions stay inside the viewport, moving beside the head when needed on short screens.

Reduced-motion users get a static idle portrait. Mouth movement remains small during speech. Hidden or closed documents have no animation loop. WebGL/model errors show the existing portrait as a fallback.

## Optional local conversation contract

An intentional microphone press requests permission. MediaRecorder sends a WebM/Opus or MP4 clip as multipart field `audio`. Another press stops the recording. Local silence detection also stops after speech, with a 20-second hard maximum. No recording starts on page load or on an ordinary page tap.

The text form uses the same endpoint with JSON `{text: 'question'}`. A response may immediately return:

```json
{"audioUrl":"/responses/example.wav","text":"answer","userText":"question","cues":[{"start":0,"end":0.2,"value":"B"}]}
```

Or it may return `{jobId, phase}`. The browser polls `GET /api/jobs/:id` every 1.2 seconds and displays Listening, Thinking, or Preparing voice. The completed response can be returned at top level or inside `result`. `phase: "error"` with an `error` string ends polling. Polling has a ten-minute ceiling. Cancel and close call `POST /api/jobs/:id/cancel` when a job ID is known. Cancelling during local speech analysis immediately restores waiting state and Tap to hear, enables Send, hides Cancel and keeps the audio paused. The cancelled request cannot overwrite a newer request's controls when its asynchronous work settles.

Leaving the page pauses playback and stops recording, pending requests and analysis. A delayed microphone permission result is discarded if its request was cancelled, the character closed, or the page became hidden. Recording callbacks retain their own media chunks rather than a later recording's data.

Opening the optional conversation panel makes `GET /api/health`. An HTTP failure or `{available:false}` produces a plain unavailable message. This check does not start a model or request microphone access.

## Diagnostics and reuse

`window.NLAvatar.ready` resolves after model/fallback setup. `diagnostics()` reports renderer, geometry count, bounds, state, frame count, audio time and errors. `playSpeech({url,cues,text})` reuses the audio element and model for new local responses. `stopSpeech()` stops current sound and pending question work. `enableConversation(endpoint)` reveals controls when a local server becomes available.

The v2 model has a small `mouthOpen` deformation and a `BlinkOverlay` material using the exact pre-existing closed-eye artwork on the shaped 3D surface. Its old `blink` morph is held at zero because collapsing the eye texture looked like a squint. Idle yaw is limited to about 2.4 degrees; the asset is intended only for viewing within 3 degrees of frontal.

The existing greeting retains its known Rhubarb timing. New `playSpeech` responses are decoded locally and analyzed by `dynamic-lips.js` in a module Worker before playback. It uses the locally bundled MIT InterviewFlowAI 0.3.0 detector and model, with no remote provider or key. The result is read against the same `audio.currentTime` used for playback. All phonemes are projected onto the one small opening shape, so this is not a full multi-viseme facial rig. Failed analysis falls back to supplied mouth cues. Close, stop, microphone start, and response cancellation abort pending analysis. Browser sound policy still applies.

`diagnostics().lipAnalysis` exposes the actual source, worker flag, event count, duration and analysis timing. The integration test verifies real analysis, changing mouth movement, minimal opening, neutral return, cancellation and no runtime exceptions. It does not establish perceptual superiority over other avatars.

Focused narrow-phone checks at 360 by 640 and 320 by 568 passed with the caption panel collapsed and expanded. Bounds fit, existing site controls remain clear, visible target centers are reachable, opening captions stays silent, and one tap on Close works from the expanded state. Evidence is in `evidence/narrow-phones/`; these are Chrome viewport tests, not physical-handset tests.

## Provenance

Three.js 0.180.0 comes from the official npm package, with its MIT license in `vendor/THREE-LICENSE.txt`. Only relative import paths were changed. Existing `kit/demo/greet-en.mp3` and `kit/greet-en.cues.json` were copied unchanged. The model build and asset provenance are documented separately by the Blender asset builder.

Reference API documentation: [Three.js](https://threejs.org/docs/) and [HTMLMediaElement.play](https://developer.mozilla.org/en-US/docs/Web/API/HTMLMediaElement/play).
