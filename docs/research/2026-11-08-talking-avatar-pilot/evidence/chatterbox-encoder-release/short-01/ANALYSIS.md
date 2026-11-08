# Short encoder-release result and unequal PCM

The coordinator's actual run completed and stopped its owned processes. Peak working set was **1040.980 MiB**, peak commit **1169.023 MiB**, minimum available machine physical memory **1.077 GiB** and commit **1.317 GiB**. Whole child time was **42.859 seconds**, including **32.172 seconds** initialization. This establishes one short run fitting its guarded window, not a long-conversation capacity or latency claim.

The unequal-PCM result is preserved. All three saved files below are mono 24 kHz PCM16 with **61,920 samples / 2.58 seconds**. Candidate and historical warm receipts both report 62 generated tokens and a stop token, but historical token identities were not saved.

| Comparison | Zero-lag waveform correlation | RMS error | Peak absolute error | Best shift within ±100 ms | 10 ms RMS-envelope correlation |
|---|---:|---:|---:|---:|---:|
| New candidate vs historical warm | 0.493915 | 0.061229 | 0.463715 / 15,195 PCM16 steps | 0 samples | 0.978968 |
| New candidate vs historical cold | 0.275151 | 0.076699 | 0.465698 / 15,260 steps | 0 samples | 0.974693 |
| Historical cold vs historical warm | 0.332252 | 0.073236 | 0.484894 / 15,889 steps | -5 samples / -0.208 ms | 0.975499 |

Full numbers and file hashes are in `pcm-analysis.json`. This is not a mere file-header or alignment difference: 61,146 of 61,920 candidate samples differ from the warm sample. Matching duration and similar envelopes do not prove words, voice identity, perceived quality or equivalence. No new listening or speech-recognition result is claimed. The two historical outputs also differ substantially, supporting investigation of stochastic decoding rather than assuming this lifecycle change caused the difference.

## Concrete source explanation

Header-only protobuf inspection of the unchanged official `conditional_decoder_q4.onnx` found three `RandomNormalLike` nodes and one `RandomUniformLike`, all lacking a `seed` attribute. The inspected top-level encoder and speech-language-model graphs have none of these operators. ONNX specifies automatically generated seeds when absent: [RandomNormalLike](https://onnx.ai/onnx/operators/onnx__RandomNormalLike.html), [RandomUniformLike](https://onnx.ai/onnx/operators/onnx__RandomUniformLike.html).

The exact runtime version's [CPU random kernels](https://github.com/microsoft/onnxruntime/blob/v1.31.1/onnxruntime/core/providers/cpu/generator/random.h) seed each generator from the global seed plus that graph node's index when no node seed exists, and retain generator state across calls. The [global seed defaults to clock time](https://github.com/microsoft/onnxruntime/blob/v1.31.1/onnxruntime/core/framework/random_seed.cc). The [Python binding](https://github.com/microsoft/onnxruntime/blob/v1.31.1/onnxruntime/python/onnxruntime_pybind_state.cc) exposes `set_seed` through that global setter. This supports a controlled same-seed, fresh-session comparison; it does not establish equivalence of this unseeded historical pair.

Installed Perth source was read without importing it. `apply_watermark` calls magnitude/phase transforms, its loaded convolutional encoder and inverse transform. The separate random `_attack` helpers are in a training path that this method never calls. The used encoder contains no dropout or random operation. Its random constructor initialization is overwritten by the strict checkpoint load. Autograd remains enabled, exactly as before. The candidate watermark changed its own pre-watermark PCM with RMS error 0.009970 and correlation 0.988200, but there is no historical raw PCM to isolate watermark differences across these recordings.

## Next prepared comparison, not yet run

`../../../research/benchmark_encoder_seeded_pair.py` sets ONNX Runtime seed 682 before any sessions in each fresh process. It runs an instrumented original constructor first, verifies process exit, then starts the encoder-release candidate. The same observation wrappers capture conditioning, generated token identities, decoder inputs and raw/final PCM; no second model remains resident. Torch is seeded only after its normal Perth import and before generation, preserving the model-load memory order. No arena, `no_grad`, weights, sampling, threads or watermark operation changes are combined.

Baseline admission is 2.0 GiB physical / 2.5 GiB commit; candidate admission 1.8 / 2.2. Live abort floors remain 0.75 / 1.0, with owned-job cancellation, nominal 0.1-second memory polling, asynchronous idle health, 120 seconds per child and 360 seconds overall. Exact array/token/PCM checks are required; any mismatch is retained. Even a complete exact match establishes only this nine-word, single-seed regression case. Broader conversation quality, facts, longer utterances and concurrent application behavior remain separate checks.
