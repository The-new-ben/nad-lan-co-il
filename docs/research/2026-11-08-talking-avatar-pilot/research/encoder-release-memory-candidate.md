# Same-voice memory lifecycle experiment

Prepared 8 November 2026. Ben has approved the lighter Chatterbox voice; this experiment preserves that model, exact reference, token selection, decoder and Perth watermark. It is a separate implementation, not a public or default change. Claude Desktop and GrokBot remain open. The initial unseeded short run and one authorized seeded pair have now completed; see the measured update below.

## What is measured

The historical nine-word benchmark reached **1.226 GiB OS peak working set**. Its final private bytes were **1.257 GiB**, an end-of-run observation, not lifetime peak commit. The 40-word reply reached **1.517 GiB peak working set** and **1.603 GiB observed final private bytes**. Source: `../evidence/chatterbox-onnx-q4/benchmark-receipt.json` and `turns-receipt.json`. New monitoring records the operating system's peak working and peak pagefile/commit counters through process exit.

The four ONNX graph plus external-data file sizes are: reference encoder **220.07 MiB**, token embedding **35.56 MiB**, speech language model **195.25 MiB**, conditional decoder **237.06 MiB**. These are disk sizes, not measured component working sets. The reference encoder took 2.042 seconds to load plus 1.138 seconds to encode in the historical full-reply run. Decoder load took 8.292 seconds; repeatedly unloading it would add that cost per sentence and is not part of this first experiment.

## Smallest separate change

`onnx_encoder_release_candidate.py` loads only the encoder, encodes the unchanged reference, copies its four output arrays, deletes the encoder and all original output aliases, and collects garbage before loading the other three sessions. The encoder is never used again in the original implementation. Keeping independent NumPy arrays avoids accidentally keeping an encoder allocator alive through an output buffer. Actual memory reclamation must still be measured.

The existing `_sentence` body and `generate` method are reused. Observing wrappers record encoder array shape/dtype/hash, every generated speech token, decoder input tokens, pre-watermark float PCM and final watermarked float PCM. There is no CPU arena change, `no_grad` addition, new quantization, prompt change or altered watermark. The saved same-text comparison is `../evidence/chatterbox-onnx-q4/warm-next-question.wav`; exact PCM16 equality is tested, with the historical warm-state difference explicitly recorded. No earlier conditioning/token/raw-float artifacts are available, so new instrumentation does not itself prove intermediate equality with a baseline.

## Bounded coordinator run

Both new files passed syntax parsing. The default command reports `preparedOnly: true`, `inferenceStarted: false`. Only the coordinator may start the prepared run:

```powershell
python "C:/Users/777/Documents/agent-tools/talking-agent/prototype-3d/research/benchmark_encoder_release_candidate.py" --go --label short-01
```

It tests only “What city and budget do you have in mind?” with the exact reference. Provisional short-test admission is **1.8 GiB physical / 2.2 GiB available commit**, with unchanged **0.75 / 1.0 GiB live abort floors**, nominal 0.1-second sampling, a suspended child assigned to an owned Windows Job before resuming, asynchronous idle checks on 8769, 120 seconds for the child and 180 seconds overall. Unknown health or unavailable process memory aborts. Parent/child output, source hashes, phase samples, native peaks, audio and equality evidence are retained under `evidence/chatterbox-encoder-release/<label>`.

This is a bounded research admission threshold, not a production capacity claim. Subtracting the encoder's 0.215 GiB disk size from the old short peak suggests about **1.011 GiB** plus the 0.75 GiB reserve, or **1.761 GiB**. That unmeasured estimate is the basis for the narrow 1.8 GiB test gate. The same arithmetic for the long reply gives about **2.052 GiB** including reserve, above the recently reported 1.84 GiB free. A short success therefore cannot establish that full conversation fits. Failure or insufficient savings should lead to a separately reviewed phase-by-phase variant, not weaker abort floors.

## Other options, not combined here

Strictly stop STT before Qwen, then Qwen before voice. Existing conditional release can retain two models when memory initially looks sufficient; explicit sequential ownership gives predictable peak behavior at a cold-start latency cost. The candidate STT is already a one-recording subprocess. Its eight-thread test measured 0.731 GiB peak; the faster four-thread receipt lacks a peak measurement, so those figures cannot be silently combined.

The installed llama CLI has memory mapping enabled by default, context 2048 and batch/physical batch 128 in `brain.command`. Smaller physical batch can reduce temporary compute memory while keeping the same text/context; it needs a separate output/latency check. Do not add `mlock`, shorten the grounding prompt, or remove property caveats to fit. The pinned Q4 header has 28 layers, eight KV heads and 128-dimensional keys/values: full F16 KV at context 2048 is approximately 224 MiB before overhead. Context 1536 would save 56 MiB, but requires checking every prompt plus response and conversation history; it is not a free factuality-preserving change. The unchanged Q4 benchmark should remain distinct from such tuning.

ONNX defaults enable CPU arenas, memory patterns and reuse. Disabling an arena or using a shared allocator may change retained memory and latency, so test those separately only if encoder release is insufficient. Official documentation: [Python session options](https://onnxruntime.ai/docs/api/python/api_summary.html#sessionoptions) and [memory consumption](https://onnxruntime.ai/docs/performance/tune-performance/memory.html). Perth's installed `apply_watermark` currently builds an autograd graph; `torch.no_grad()` around only that call is another separate value-regression candidate, not part of this run and not removal of the watermark.

## Measured update

The [seeded pair-03 regression](../evidence/chatterbox-encoder-seeded/pair-03/README.md) passed all eight exact checks, including conditioning, generated token IDs, pre/post-watermark float PCM and final WAV. For this nine-word sample, peak working memory fell from 1256.094 to 1042.227 MiB, and peak commit from 1315.070 to 1170.121 MiB. Both owned process trees stopped. Live floors were preserved with both owner apps open. The earlier unseeded PCM inequality is retained with [numeric and source analysis](../evidence/chatterbox-encoder-release/short-01/ANALYSIS.md): the unchanged decoder contains four unseeded random operators, so historical warm/fresh PCM equality was not a controlled expectation. This short same-seed result supports the lifecycle change, without establishing longer-answer capacity, global voice quality or real-time latency.
