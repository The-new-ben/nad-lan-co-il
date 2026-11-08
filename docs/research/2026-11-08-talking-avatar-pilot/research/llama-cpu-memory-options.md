# CPU Q4 memory options, source review only

The installed official b12189 CPU CLI supports `--no-repack` (`-nr`) and `--load-mode none`. Only `--help` was executed for this review. No model was loaded, no application was closed and no public configuration changed.

The earlier `q4-low-headroom-eight-01` run aborted at its resource floor during the first case. Its reported peak was 1,985.773 MiB working set and 1,062.637 MiB private commit. That discrepancy is consistent with mapped file pages plus separately allocated weights, but the old error-only log does not prove the selected buffer types. Do not label the cause established by that receipt alone.

## Minimal isolated comparisons

1. Add **only `--no-repack`** to the existing CPU Q4 command. Keep the same model, context, batch, threads, seed and sampling. The option disables extra CPU buffer types, including the optimized repacking path. Default CPU buffers can wrap mapped model data instead of allocating a second repacked representation. It preserves stored quantized weights, but changes the kernel path, so exact output and speed must still be tested. [Argument implementation](https://github.com/ggml-org/llama.cpp/blob/b12189/common/arg.cpp), [buffer selection and mapped allocation](https://github.com/ggml-org/llama.cpp/blob/b12189/src/llama-model.cpp).

2. As a separate comparison, **`--load-mode none` with repacking enabled** avoids the mapped source while retaining the optimized repacking kernels. The non-mapped loader reads repacked tensors through a temporary buffer, visits larger tensors first and shrinks an oversized buffer. This may reduce working-set duplication but still needs private allocation for the weights and temporary tensor. It is not an established fit under current commit headroom. [Loader implementation](https://github.com/ggml-org/llama.cpp/blob/b12189/src/llama-model-loader.cpp).

The concrete mechanism: `CPU_REPACK` allocates a separate CPU buffer and repacks supplied source data into it. The Windows mapping implementation prefetches eligible mapped ranges, while `unmap_fragment` does nothing on Windows. Mapped source and repacked storage can therefore coexist. This supports the hypothesis, not a measured saving. [CPU repacking](https://github.com/ggml-org/llama.cpp/blob/b12189/ggml/src/ggml-cpu/repack.cpp), [Windows mapping](https://github.com/ggml-org/llama.cpp/blob/b12189/src/llama-mmap.cpp).

## Other controls

- Existing `-b 128 -ub 128` already use much smaller batches than the CLI defaults of 2,048 and 512. Reducing the physical microbatch can reduce compute workspace later, but does not remove the loader's mapped/repacked duplication. It should be a separate test if loading succeeds and the compute stage becomes the limit.
- Keep the current context and F16 KV-cache types for the first comparison. Smaller context changes available prompt/history capacity; quantized KV changes precision. Neither directly addresses a load-stage failure.
- `--no-host` is not a replacement for `--no-repack`. Its stated purpose is to bypass a host buffer so extra buffers can be used. A generic CPU tensor override is also insufficient: the loader explicitly considers extra CPU buffer types when selecting a CPU override.
- `--lazy-mode on` is limited to tensors marked for lazy reading, not general layer-weight streaming. It is not a demonstrated solution for this dense Qwen model. MoE cache controls concern a different model structure.

For any authorized experiment, retain owned-process containment, the existing physical/commit abort floors and deadlines. Use verbosity 3 to capture model, mapped/repacked and compute/KV buffer evidence. Report total time, memory peaks, actual exit, validation and content separately. No new public admission threshold follows from this source review.

Source snapshots and the installed CLI help are retained under `research/primary/llama-cpu-repack/`; `receipt.json` records hashes and the help-only scope.
