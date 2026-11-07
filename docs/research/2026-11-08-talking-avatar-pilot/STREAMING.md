# Optional sentence-streaming comparison

The original review remains at `http://127.0.0.1:8769/`, using `widget.js` and the original voice. The separate candidate uses port 8770, `widget-stream.js` and `stream-player.js` without changing the visible design.

Launch the complete candidate with:

```
python server.py --port 8770 --voice-engine onnx-q4 --streaming --prewarm --persistent-brain --stt-engine faster-small-en
```

The extra-short response experiment is disabled. Its wording degraded a guide answer and missed its intended limits. The candidate keeps the original grounding, disclosure and professional-role instructions. No exact-answer audio cache is used in streaming mode.

## Actual generation contract

`POST /api/converse` still accepts JSON text or multipart audio and returns a job identifier. Polling the job returns a cumulative `chunks` array, with stable zero-based indices. Each chunk has `audioUrl`, `text`, `cues`, `duration`, `generatedAtEpoch`, `audioWrittenAtEpoch` and `publishedAtEpoch`. The browser must play each index once.

The phase becomes `streaming` when the first actual sentence is ready. The ONNX worker generates and watermarks that sentence, writes its WAV, and emits it. It then waits for an acknowledgment. The server exposes the chunk in the job state before acknowledging, so the worker cannot begin the next sentence earlier. Nonfinal chunks include a short trailing silence. This is new sentence generation, not subdivision of an already completed recording.

The final phase is `done`. It retains all chunks and a legacy `result.audioUrl` containing the actual concatenation. Per-sentence metadata records when generation started; comparing it with the previous publication timestamp verifies the ordering. API publication time is not browser first-audible time; browser playback must be measured separately.

Cancelling clears exposed chunks and the final result, terminates the active owned worker process tree, and denies subsequent audio requests for that job. The browser also aborts fetches and clears its playback queue. Every chunk request checks the same session ownership as the job.

## Explicit warmup and memory

`--prewarm` adds an explicit first-gesture endpoint to the candidate page. Without the flag, the page does not call that endpoint. Health checks never load models. `POST /api/prewarm` creates a separate session-owned job; the existing cancel route handles it. A normal question preserves a queued prewarm so its useful loading work can finish. Closing a prewarm releases an idle worker only if that session still owns it, never if another job is using it.

The page establishes its session cookie before JavaScript can submit first-gesture requests, preventing concurrent warmup and question requests from creating different owners. Duplicate active prewarm requests reuse their job. Cancelled queued work immediately releases its queue slot.

Both `/api/converse` and `/api/prewarm` accept `X-NL-Request-ID`. The client cancels that identifier through `POST /api/requests/:requestId/cancel` when closing, leaving or replacing a request, including before the initial response has returned. The server retains session-scoped cancellation tombstones for 120 seconds and checks them before registration. The submission response stays readable so a stale returned job can also be canceled. Token-bearing submissions require an established session cookie. The real HTTP controls in `evidence/latency/streaming/request-token-cancellation.json` cover early upload cancellation, early prewarm cancellation, delayed responses, ownership and bounded storage; no model inference is part of that test.

Only Qwen and the optional voice may remain warm. The faster English transcriber runs in an isolated child process and exits after each recording. Candidate startup requires three GiB of available physical RAM. Idle models are released when necessary, and both warm workers expire after two minutes of inactivity. Memory-driven eviction is retained in the evidence and must not be described as a warm result.

At the initial combined-test handoff, available RAM fell below the startup threshold despite no task-owned model process remaining. No owner applications were closed and no guard was bypassed. Full fresh-response and first-audible claims require actual successful receipts, not the earlier isolated voice or language-model benchmarks.

`evidence/latency/streaming/prewarm-controls.json` verifies the HTTP ownership, deduplication, queue recycling and private-source restrictions without starting models. Genuine paired inference, when resources permit, is recorded separately by `verify_streaming_api.py`.

The actual blocked request is retained in `evidence/latency/streaming/resource-rejection.json`: 1.491 GiB available, `resource_busy`, and the plain message “This computer is busy. Please try again shortly.” No inference occurred. The HTTP/worker control fixture in `server-protocol-fixture.json` separately passed publication ordering, full-text retention, ownership, later-sentence failure and cancellation. Its silent synthetic samples are not real speech or latency evidence.
