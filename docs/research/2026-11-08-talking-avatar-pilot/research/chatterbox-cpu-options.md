# Focused Chatterbox CPU options, 7 November 2026

Preserve the current voice environment, Multilingual V2 checkpoint, reference WAV and final voice selection. The current reply is not interactive: its 10.544-second WAV took 36.422 seconds of model/reference loading and 125.657 seconds of synthesis; the full typed pipeline was approximately 220 seconds including imports and the response model. The first reply also has a reported repetition artifact, so speed alone is not acceptance.

The shared VOICE-REUSE-INDEX.md and checked-path manifest were read. The installed source is chatterbox-tts 0.1.7, Torch 2.6.0, ONNX Runtime 1.21.1, Transformers 5.2.0. The initial research downloaded no weights; a subsequently authorized isolated Turbo ONNX comparison is now completed, below. No installed environment was changed.

## Two official candidates

| Candidate | Download size from official file inventory | Practical consequence |
| --- | --- | --- |
| Chatterbox Nano | Required three weight files: 1,940,470,024 bytes, plus small tokenizer/conditioning files. The repository additionally contains a 1,056,484,620-byte decoder that the Nano loader does not use. | Official CPU-oriented 110M backbone, but total download and resident model are larger than the headline parameter count suggests. Needs separate source because the installed Turbo class lacks `nano=True` and its config table lacks GPT2_small. |
| Chatterbox Turbo ONNX q4 | Four graphs plus their data files: 721,357,236 bytes; tokenizer.json adds 3,562,272 bytes. | Smaller isolated candidate for the current low-RAM machine. Existing ONNX Runtime can be tried without upgrading the voice environment, but actual graph compatibility and speed remain untested. |

Nano is an official English model using the Turbo class, smaller GPT2 backbone and single-step decoder. Its example accepts a reference audio clip and CPU mode. Hugging Face metadata reports an update on 21 July 2026, so this is not a new release from the requested week. The official README's claim of three times real-time speed is a vendor claim, not a result on this Ryzen. [Official Nano model](https://huggingface.co/ResembleAI/chatterbox-nano), [official example](https://github.com/resemble-ai/chatterbox/blob/master/example_tts_nano.py), [loader source](https://github.com/resemble-ai/chatterbox/blob/master/src/chatterbox/tts_turbo.py).

The official Turbo ONNX repository provides reference-conditioned inference and fp32, fp16, q8, q4 and q4f16 variants. Its published example uses greedy token selection and repetition penalty, so it does not reproduce the current Multilingual V2 temperature/CFG behavior. q4 is the more conservative CPU experiment than q4f16 because it avoids depending on half-precision non-quantized operations. This is a proposed test choice, not a measured speed ranking. [Official Turbo ONNX model and inference example](https://huggingface.co/ResembleAI/chatterbox-turbo-ONNX).

Both models are MIT licensed and need no paid inference service for local execution. Downloads, disk, electricity and computation still have costs. Neither using the same reference WAV nor being in the Chatterbox family guarantees the exact same perceived woman, accent or phrasing. Any candidate must remain a separate comparison until the actual audio is accepted.

## Smallest useful next experiment

After the current microphone pipeline finishes, use a separate `experiments/chatterbox-turbo-onnx-q4/` folder, existing interpreter and explicit CPUExecutionProvider. Download only the selected graphs/data and tokenizer. Do not change the shared package versions or cache ownership. Start with one exact short sentence and the unchanged `kit/ref-female.wav`; keep watermark behavior. Cap generation and fail on a missing stop token instead of treating truncation as a successful voice.

Record load, reference encoding, token generation, decode, watermark and full-file times separately, along with peak process memory. Compare the existing approved greeting reference and one baseline sentence, verify every word, and listen for voice identity and artifacts. A whole-file ONNX result is not streaming. Stop after a compatibility failure rather than upgrading the shared environment. ONNX Runtime documents that quantization can affect both accuracy and speed; kernel support still has to be tested for this particular graph. [Quantization documentation](https://onnxruntime.ai/docs/performance/model-optimizations/quantization.html).

For the unchanged V2 path, reducing cold imports/loading with a persistent worker may save part of the observed overhead, but only if measured memory leaves room for transcription and the response model. It cannot remove the 126-second synthesis cost by itself. A controlled 2-versus-4-thread measurement and one shorter sentence are lower-risk optimizations than swapping voice models. Do not claim a percentage improvement without measuring it.

The official repository now identifies Chatterbox as retired research since August 2026. Its older hosted-service promotion remains lower in the same README and in model cards. Treat the archive and licence as available; do not present the stale paid-service copy as a currently supported offering. [Official repository notice](https://github.com/resemble-ai/chatterbox).

Primary receipts, official README/source snapshots and exact file inventories are in `research/primary/cpu-voice/`. The voice-backend owner has the validated candidate API for explicit optional integration; the current Multilingual V2 engine remains the default.

## Authorized isolated benchmark completed

Selected official artifacts were downloaded at Hugging Face revision `d21799bd0354adb85e348b8a0442a8405110a2cf`. All 15 files passed their source hashes, totalling 724,935,602 bytes. Existing ONNX Runtime 1.21.1 rejected the official graph's GatherBlockQuantized `bits` attribute. That failure is retained. The official 1.31.1 Windows wheel, 14,885,761 bytes, was SHA-256 verified and extracted into this task folder only. A process-local import path selected it; no shared package was installed, removed or upgraded.

The candidate ran CPU-only with four threads, inference networking disabled, the unchanged 9.912-second `kit/ref-female.wav` and output watermarking. A reusable `CPUVoiceEngine` holds sessions, reference conditioning and the watermark model across turns. Both engines generate the two sentences separately with a 220 ms gap. The candidate uses greedy sampling, not V2's temperature/CFG settings, and does not apply V2's edge trimming. This is a named candidate, not a claim that the original engine became faster.

| Same-machine measurement | Existing Multilingual V2 | Turbo ONNX q4 candidate |
| --- | --- | --- |
| Exact existing microphone reply, full cold voice step | 212.922 s | 47.730 s |
| Same reply, synthesis after initialization | 144.3 s | 30.720 s, including watermark |
| Result duration | 13.361 s | 13.620 s |
| Warm next turn, nine-word question | Not measured | 7.176 s for 2.580 s audio |
| Candidate peak resident memory | Not compared | 1.629 GB |

These are observed runs, not a guarantee across workloads or a streaming benchmark. The candidate's cold result includes 16.98 seconds of initialization. A previously recorded baseline had different process and memory conditions, so the same-text numbers establish a useful practical improvement rather than a laboratory-controlled multiplier. Seven seconds for a short warm answer still falls short of instant conversation.

Cached Whisper small reproduced every word of both the same-text reply and warm next question after punctuation/case normalization. The existing cached Chatterbox VoiceEncoder gave cosine similarity 0.9371 between the candidate reply and approved greeting, and 0.9677 between the candidate and baseline same-text reply. These are model-dependent similarity measures without a calibrated pass threshold. They do not establish identical perceived voice, naturalness, preference or human acceptance.

Review audio and receipts are copied into `evidence/chatterbox-onnx-q4/`. Runtime/source remains in `.runtime/chatterbox-onnx-test/`: `onnx_engine.py`, `benchmark_turns.py`, `quality_check.py`, pinned model files and the isolated runtime wheel. No paid service, production write or default voice substitution occurred. The next integration is explicitly selectable, with the original default preserved.
