# Compact local candidate integration

Prepared 8 November 2026. No server was restarted and no model, browser or public request was run during this integration.

Explicit launch configuration for root review:

```text
python server.py --port 8770 --voice-engine onnx-q4 --streaming --stt-engine faster-small-en --brain-model q4 --no-repack --sequential-models --memory-profile compact
```

The compact profile requires this candidate port, Q4, no repacking and sequential residency. Persistent answer workers and prewarming cannot be used with it. Default port 8769 retains MTL, Q8, Whisper small and the original content-validation behavior. The legacy ONNX profile retains its 3 GiB physical admission check.

Compact admission requires 2.3 GiB available physical memory and 2.5 GiB remaining Windows commit capacity before the request and each child-model stage. While a job owns a running process, the existing checkpoint mechanism observes both resources in the 0.1-second polling loops and stops that owned process tree at or below 0.75/1.0 GiB. These are provisional long-voice experiment thresholds, not proof that a full conversation fits or a hard OS memory cap. Health reports the profile, exact admission values, runtime floors and requested no-repack flag without loading a model. Per-job private receipts retain entry samples, minimum observed values and any abort sample.

The ONNX worker imports the frozen `research/onnx_encoder_release_candidate.py`. ORT seed 682 is set before constructing sessions; Torch seed 682 follows normal engine initialization, as in the checked seeded pair. Token generation, decoder and watermark behavior remain inherited from the approved engine. A distinct encoder-release/seed cache identity prevents older unseeded voice metadata from appearing as a new implementation result. The original MTL cache identity is unchanged.

On candidate port 8770 only, recognized property questions use the reviewed editorial lookup before prompt construction or model execution. Their result and receipt identify the property source, editorial mode and `languageModelInference:false`. All other questions keep the existing general prompt and validator. Only the existing validator's exact unverified-figure, role-action and false-human-identity rejections produce a prepared source-gap or role-boundary response. The rejected text and reason remain private; public text/audio receive only the explicit boundary. These responses identify editorial mode and a model attempt without claiming that the replacement was model inference. Empty, incomplete, overlong, process, timeout and transport failures remain errors. The persistent Q8 adapter retains its own previous failure behavior; compact mode excludes it.

Before-state copies are retained at `evidence/compact-integration-before/`. Validation:

- `evidence/compact-integration-controls/receipt.json`: 34 controlled checks, including actual owned sleeping-process termination for each independent memory floor, admission mismatch, metadata, property/model routing, private rejection handling, no operational-failure fallback, seed/import order and invalid CLI combinations. Speech output is explicitly silent fixture audio, not synthesis.
- `evidence/compact-integration-decode-regressions/receipt.json`: 20 existing checks repeated against the new server, including actual FFmpeg timestamp-gap decoding, duration/upload bounds, cancellation and owned descendant shutdown. The original earlier receipt was not overwritten.
- `evidence/property-context-regressions.json`: 54 property scope/intent checks, with no model.

The next genuine multipart speech turn, actual memory peak, first-chunk timing, complete reply and listening assessment remain separate root-owned validation. Public worker policy and deployment are outside this patch.
