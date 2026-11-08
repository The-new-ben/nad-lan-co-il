# Seeded encoder-release regression passed for one short sentence

One authorized paired run completed on 8 November 2026. It used the original approved Turbo ONNX q4 voice and exact reference, with the original constructor first and encoder-release candidate second in separate fresh processes. Both used ORT seed 682 before session construction, four threads, and the same original generation and watermark operations. Claude Desktop and GrokBot remained open. No public/default engine change was made.

Question: **What city and budget do you have in mind?** Both outputs are 2.58 seconds, 61,920 samples at 24 kHz, with 62 emitted tokens and a stop token.

All eight exact comparisons passed: conditioning arrays, emitted speech tokens, decoder token inputs, pre-watermark float PCM, watermarked float PCM, final PCM16, reference hash and completed stop tokens. The final WAV SHA256 is identical: `7efd7c5ed320f95ab0c8ad4064dd48e5c9f910411e3283939ccb95adab212438`. Torch RNG state was unchanged during generation in both variants, consistent with the reviewed direct Perth watermark path having no random operation.

| Measurement | Original constructor | Encoder released |
|---|---:|---:|
| OS peak working set, MiB | 1256.094 | 1042.227 |
| OS peak commit, MiB | 1315.070 | 1170.121 |
| Minimum machine available physical, GiB | 1.1849 | 1.4333 |
| Minimum machine available commit, GiB | 2.0111 | 2.0591 |
| Child initialization, seconds | 25.813 | 22.219 |
| Synthesis including watermark, seconds | 9.090 | 8.887 |
| Whole child, seconds | 34.953 | 31.109 |
| Parent-monitored variant wall time, seconds | 36.719 | 32.547 |
| Owned processes stopped | Yes | Yes |

Peak working memory decreased by **213.867 MiB / 17.03%** and peak commit by **144.949 MiB / 11.02%** in this pair. These are maximum individual observed process counters; native available-memory monitoring covered the whole machine. Both observed process lists were empty after cleanup. The complete paired parent run took 70.797 seconds.

The invocation waited for two readiness samples three seconds apart, each above 2.2 GiB physical and 2.7 GiB commit. Admission and abort limits were unchanged. No abort was needed. Readiness evidence is in `../pair-03-readiness.json`; raw source hashes, outputs, phase/memory samples and comparisons are retained beside this note and in `baseline/` and `candidate/`.

This supports the specific encoder-lifetime change preserving this seeded nine-word output while using less memory. It is not an exhaustive voice-quality test, a long-utterance capacity result or proof of real-time conversation. The candidate ran second, so file-cache and changing machine-load effects prevent attributing the modest timing difference solely to the change. No new listening or speech-recognition test was performed. The prior unseeded PCM mismatch remains recorded in `../../chatterbox-encoder-release/short-01/`; it was not overwritten or relabeled as equal.

Recommended next step: retain the same model/reference/operators and review integration of encoder release with strict sequential STT, brain and voice lifetimes. Separately test a representative longer answer under the unchanged live memory floors before claiming full conversation capacity. Do not relax factuality checks or owner application requirements based on this short success.
