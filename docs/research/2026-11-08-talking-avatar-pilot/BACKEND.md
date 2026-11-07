# Local conversation review

Run `python server.py` in this folder, then open `http://127.0.0.1:8769/`. The root page uses the saved local website fixture and enables the microphone and text controls. It does not change the live site. The server binds only to loopback and does not accept other origins.

The existing voice environment is reused without installation or modification. Whisper small transcribes English audio, the portable Qwen3 1.7B Q8 model creates an answer using passages from `source-page.html`, and local Chatterbox Multilingual speaks with the existing `kit/ref-female.wav` reference. Voice settings remain exaggeration 0.5, CFG 0.5 and temperature 0.65. Inference is offline. The speech worker rejects network connections and uses cached weights.

Only one job runs at a time. Each model process exits before the next stage starts. A Windows job object contains the Python environment launcher and all its child processes, so cancelling stops the actual inference process as well as the launcher. Stopping a job never terminates user applications. A cancelled job cannot publish a later result or serve its audio.

The API accepts multipart `audio` or JSON `{"text":"question"}` at `POST /api/converse`, returns a job identifier, and exposes progress at `GET /api/jobs/:id`. Cancellation uses `POST /api/jobs/:id/cancel`. A local same-site cookie retains up to four conversation turns. The health endpoint only checks prerequisite files and does not load a model or request microphone permission.

Both conversation and optional prewarm submissions accept a client-generated `X-NL-Request-ID`. `POST /api/requests/:requestId/cancel` records cancellation within the same visitor session even before the upload finishes or the job identifier arrives. Registration checks that cancellation atomically before queuing. Clients retain the submission response and cancel a stale returned job identifier as a second check. They also send token cancellation on close, page exit and replacement. `GET /api/session` can establish the cookie without creating work; a token submission without an existing session returns `session_required` and creates no job.

Cancellation tombstones last 120 seconds and are bounded to 128 per session. Overflow temporarily blocks new registrations only in that session. A duplicate token returns its existing job instead of creating another one. Upload registration has an absolute 20-second deadline. `evidence/latency/streaming/request-token-cancellation.json` verifies unfinished uploads, prewarm, delayed job responses, session isolation, duplicate tokens, missing sessions and bounded storage using actual HTTP, without running models.

Recordings are limited to 15 MiB and 20 seconds. Local copies and diagnostic logs remain under `.runtime/jobs/`; generated audio is under `responses/`. The server does not expose the job directory or Python source. This is a local review environment, without a production retention policy.

Exact previously generated answers can reuse their saved Chatterbox audio. The returned `voiceCacheHit` flag makes that reuse explicit. The language model still runs and must provide a valid answer; a failed model call never returns a canned success. Novel answers require fresh speech generation. The cache is local under `.runtime/voice-cache/` and uses the answer plus voice settings as its key.

## Evidence and limits

`evidence/backend-live-typed.json` records a genuine typed HTTP round trip: 16.703 seconds for Qwen and 203.531 seconds for Chatterbox, or 220.281 seconds in total, with 10.544 seconds of audio. That first run experienced severe memory pressure. The Chatterbox receipt separates 36.422 seconds of model loading and 125.657 seconds of generation; Python/import startup accounts for most of the remaining time. These figures are not an acceptable real-time conversation result.

`evidence/backend-transcription.json` contains fresh Whisper QA of that audio. It heard unwanted words around the second sentence boundary. The first voice is an unapproved review take, not a clean speech-quality pass. ASR alone cannot certify naturalness or pronunciation. `evidence/brain-followup.json` records the corrected two-sentence answer format with a generated question, after the initial baseline did not ask a direct follow-up.

`evidence/backend-controls.json` verifies cancellation of a real Python launcher and child, confirms both processes exit, and checks that cross-origin submissions, an untrusted Host, the private job folder and server source are rejected.

The later complete microphone pipeline is recorded in `evidence/backend-live-microphone.json`: 9.578 seconds for transcription, 13.422 seconds for Qwen, 212.922 seconds for Chatterbox, and 236.093 seconds overall. The 13.361-second reply matches its intended words in fresh Whisper QA after case and punctuation normalization, unlike the earlier take. `evidence/backend-speech-qa-comparison.json` retains both results. This is a word-content check, not a human listening approval. Improved available memory did not resolve the latency bottleneck.

`evidence/queue-http-replacement.json` verifies replacement through actual HTTP requests when all four pending slots are occupied. Cancellation recycles a queued slot immediately, so canceled questions do not cause a false busy response. The test loads no models.

The worker also supports a local cache of the exact reference conditionals, using the reference WAV hash and model revision. It preserves the voice settings. New receipts report reference-cache hits and per-sentence generation time. This optimization is implemented but has not yet been benchmarked in a complete new-response pipeline.

## Optional faster comparison

The default remains the existing Multilingual V2 voice on port 8769. `python server.py --port 8770 --voice-engine onnx-q4` explicitly selects the separately tested Chatterbox Turbo ONNX q4 candidate on a separate local port. It uses the official model and an isolated ONNX Runtime wheel under this task's `.runtime/chatterbox-onnx-test/`; no shared package installation or provider call is involved. This is a different Chatterbox model and still needs Ben's listening approval.

The candidate keeps a single voice worker warm after the first real request. Its sessions, exact reference conditioning and watermarker are reused. Whisper and Qwen still run in separate sequential child processes. Before transcription or the response model, the server releases the idle voice worker if free physical memory is below 3 GiB. It also releases it after synthesis if less than 2 GiB remains. Cancellation terminates the active candidate's entire owned process tree; a subsequent request loads a new worker. Health checks never start it.

Candidate responses explicitly report `voiceEngine: "onnx-q4"`, `voiceCandidate: true`, `voiceWorkerWarm` and `voiceCacheHit`. Candidate and original audio cache entries are separate. Without the explicit `--streaming` flag this comparison returns the completed recording; the sentence-streaming configuration is documented below.

An actual browser question using the original voice's verified exact-answer cache completed in 20.375 seconds, including 20.344 seconds of fresh Qwen inference and no new synthesis. `evidence/backend-browser-cached-roundtrip.json` records `voiceCacheHit: true`. This measures a cached repeat, not a novel-response voice speed.

The research benchmark generated the same 40-word reply in 47.73 seconds from cold initialization, including 30.72 seconds of generation. A subsequent nine-word sentence took 7.176 seconds in the same process. Both clips matched the intended words in Whisper QA. These are voice-only measurements, not full conversation latency or human approval of voice identity. The detailed comparison is in `.runtime/chatterbox-onnx-test/turns-receipt.json` and `quality-receipt.json`.

The server's actual persistent-worker integration is separately verified in `evidence/optional-voice-integration.json`. It generated the same full reply in 59.672 seconds including 24.906 seconds of worker initialization, then generated the short next question in 7.234 seconds without reloading. Mid-generation cancellation terminated the worker, returned a cancellation result and produced no late audio. The original MTL server remained selected throughout this isolated integration test. These timings reflect the machine's workload during that test and still do not establish instant conversation.

`evidence/backend-persona-checks.json` records genuine Qwen answers to the human-identity and broker-action questions. The identity answer explicitly says “I'm a fictional, computer-made guide.” The second answer declines arranging viewings or negotiating offers.

## Current combined candidate and resource limit

The current candidate configuration is:

```
python server.py --port 8770 --voice-engine onnx-q4 --streaming --prewarm --persistent-brain --stt-engine faster-small-en
```

It serves the separate streaming client, publishes each actually generated sentence before starting the next, and optionally warms the voice only after an explicit page gesture. Qwen may remain warm in its owned worker. The isolated faster-whisper small.en int8 transcriber uses a fresh child process per recording, with four CPU threads. No exact-answer audio cache is used in streaming mode. The experimental extra-short prompt remains off because its tested answer quality regressed. The original port 8769 review and client remain unchanged.

The combined fresh-inference test is currently blocked by actual available RAM. One real candidate request was rejected with 1.491 GiB available against the unchanged 3 GiB startup guard. It returned `errorCode: "resource_busy"` and “This computer is busy. Please try again shortly.” Numerical resource details stay in the diagnostic receipt. No model ran, no guard was bypassed and no owner application was closed. See `evidence/latency/streaming/resource-rejection.json`.

`evidence/latency/streaming/server-protocol-fixture.json` separately verifies the real HTTP and worker acknowledgment path using a tiny, silent synthetic model fixture. It confirms first-chunk publication before next-sentence generation, session ownership, unchanged full-answer text, and cleanup after later-sentence failure or cancellation. The fixture is explicitly not speech inference, not naturalness evidence and not a model or first-audible latency result. Genuine combined first-audible timing remains unmeasured. `STREAMING.md` documents the complete candidate contract.

`evidence/microphone-question-48k.wav` is a controlled microphone test fixture generated locally using Windows speech synthesis. Its text is “What should I check before buying a family home in Israel?” It is not a recording of Ben or an assistant voice result.

Lip cues from this backend use 80 ms PCM amplitude windows. They support small mouth opening, but they are not learned visemes or phoneme recognition. The browser may supply a separate learned lip model.

The prototype labels the character as computer-made. It does not arrange viewings, submit offers, negotiate or claim professional credentials. Answers avoid exact current financial figures and use the saved guide rather than claiming live property data. This backend remains loopback-only. Ben's later authorization to deploy on the single English buying-guide page is handled separately and does not make these local endpoints public.
