# Local conversation latency round

7 November 2026. The reviewed appearance and original Chatterbox Multilingual default remain unchanged. Optional experiments are isolated on port 8770. The live site has not been changed, and no paid service was started.

## Actual inference measured separately

- Same official Qwen3-1.7B Q8 model and original prompt, retained in memory: substantive new questions took 5.907 and 4.332 seconds. First process startup plus first answer took 13.075 seconds. This is answer generation only, with real matching-prefix reuse and no answer cache. See `warm-brain-candidate.md`.
- English small.en int8 recognition: 2.500-second median over twelve warm calls, versus 3.947 seconds for the original Whisper small. Four controlled synthesized questions were run four times in each of three configurations, yielding 48 transcriptions. Declared cities, addresses and numbers were preserved. These are not recordings of Ben or diverse human accents. See `stt-cpu-benchmark.md`.
- A shorter-answer prompt was rejected because it omitted an important independent-checks caveat and missed word limits. The combined candidate keeps the original prompt. See `concise-brain-comparison.md`.

These isolated timings cannot be added together as a measured conversation result. In particular, the Qwen model consumed about 1.85 GiB while resident. The voice memory reserve can intentionally evict it, losing the next turn's warm advantage.

## Browser scheduling and failure checks

`widget-stream.js` and `stream-player.js` are optional candidate modules. A generated sentence can be analysed and played while the next sentence is being generated. Playback follows actual audio time and uses the existing minimal mouth deformation. Complete-answer replay uses the combined response, not merely the final sentence.

- Six queue unit scenarios passed: ordered/deduplicated publication, out-of-order receipt, cancellation, preparation failure, missing sentence and changed publication.
- Seventeen native Chrome checks passed with controlled API publication and actual audio/learned lip analysis. They cover first playback before the final publication, ordered playback, prefetch, full-answer replay, close, cancel and pause/resume. Evidence: `evidence/latency/stream-client/results.json`.
- Thirty-three targeted native Chrome checks passed across a later-sentence server failure, an unavailable audio file, a missing sentence and a busy-computer rejection. Audio stops, incomplete answers cannot be replayed, owned server work is cancelled, microphone and text actions recover, and a new successful question restores playback. Evidence: `evidence/latency/stream-failures/results.json`.

These are explicitly controlled backend responses. They prove browser sequencing and failure handling, not inference speed, naturalness or first-sentence latency from actual models. The busy message uses a stable error code, with internal resource details kept out of the small user interface.

## Native microphone regressions

Two real MediaRecorder lifecycle bugs were independently reproduced in both archived widgets and then fixed in both current widgets:

1. Submitting a typed question during recording left the recorder running and sent a second audio question later.
2. Cancelling after native `stop()` but before its delayed stop event still sent the recording.

Four expected old-behaviour failures and four fixed-case passes are preserved in `evidence/recorder-races/`. The native events and track endings were observed using a WAV-backed fake microphone; backend replies were controlled. There was no model inference in these lifecycle tests. A generation token now invalidates delayed sends, and typed submit ends all recording tracks first.

## Combined inference is not yet verified

The intended combined configuration is local port 8770 with the ONNX q4 voice, actual sentence publication, explicit prewarm, persistent original-prompt Qwen and the faster English transcription adapter. The optional short-answer prompt remains off.

At the combined test window the machine had less than the candidate's 3 GiB free-memory startup requirement. No owner applications were closed and the guard was not lowered. The original local preview on port 8769 remains available. A new end-to-end first-audible-sentence measurement is therefore still required before claiming that this candidate improves complete conversation latency.

The actual configured server rejected a new question at 1.491 GiB free before submission (1.477 GiB when the worker checked), returning `resource_busy` and the plain busy-computer message. It performed no model inference. Receipt: `evidence/latency/streaming/resource-rejection.json`.

A separate controlled silent-model fixture exercised the real server and voice-worker acknowledgment path. The first sentence was published before the second generation began and before a combined file existed. Cross-session access was denied; complete answer text was retained. Later-sentence failure and cancellation cleared published chunks, denied old chunk URLs, stopped both launcher and worker, and produced no late second chunk or combined file. Receipt: `evidence/latency/streaming/server-protocol-fixture.json`. Its `modelInference` flag is explicitly false. It verifies the protocol, not real sentence synthesis or a timing improvement.

Visual/voice approval is pending. Public conversation hosting also remains unresolved: the public page cannot reach Ben's loopback server. Existing local videos remain the review deliverables; no fabricated faster-conversation video was made.
