# Memory recovery and ownership audit, 8 November 2026

The original loopback voice service (PID25516, port8769) and public outbound worker (PID13368) were preserved. No owner documents or applications were closed, no agent backend was trimmed or killed, and no disk files or pagefile settings were changed.

## Actual recovery

| Authorized action | Measured available RAM | Result |
| --- | --- | --- |
| Stop idle task candidate24532, then one reclaim of idle Claude desktop14988/17504 | 2.1345 to2.6024GiB after10s | Actual gain0.4679GiB. Apps alive; private allocations unchanged immediately. |
| Root resets its finished computer-use runtime through the supported tool | Audit2.383 to2.6837GiB | About0.301GiB more available; commit fell about1.262GiB. Background changes were not controlled. |
| First strict-zero-CPU renderer14752 check | 2.7038 to2.6959GiB after30s | Skipped, zero reclaim calls, because fresh CPU sample exceeded zero. |
| One newly authorized low-CPU renderer14752 reclaim | 2.7893 immediately before,2.8748 at10s,2.8196 at30s | Only0.0303GiB sustained gain at30s. Most GUI pages returned to working set. Process remained alive and responding. |
| Additional17264/17356 proposed pass | Not performed | Helper initialization defect occurred before process action; root subsequently stopped further reclaim when ready. Zero calls. |

Evidence: `bounded-pass.json`, `after-root-cua-reset.json`, `renderer14752-pass.json`, `renderer14752-lowcpu-pass.json`, and `renderers17264-17356-pass.json`. Working-set reduction is not reported as equivalent free physical RAM.

Windows EmptyWorkingSet removes pageable resident pages without releasing committed allocations or terminating a process. Pages can immediately return when used; the observed renderer refault demonstrates that limitation. Official references: [EmptyWorkingSet](https://learn.microsoft.com/en-us/windows/win32/api/psapi/nf-psapi-emptyworkingset), [Working set](https://learn.microsoft.com/en-us/windows/win32/memory/working-set).

## Process ownership and capacity

The read-only inventory found67 node/node_repl processes with about2404.87MiB aggregate working set.55 trace to live Codex app/agent ancestry and12 to Claude. No missing or reused ancestor PID chain established an abandoned tool. A quiet process or absent TCP listener does not prove a stdio worker is unused. None was stopped.

Examples retained in `node-ownership-audit.json`: CUA4344 to node_repl26020 to node25228 to codex3064; CUA19104 to node_repl17244 to node14172 to codex14876. The latter exited after root's supported runtime reset. Command lines were classified privately; raw command lines and secret values were not printed or saved.

At the inventory snapshot: physical available2.383GiB; committed21.237/25.099GiB. Existing pagefile allocation12489MiB, usage1181MiB, peak2229MiB. C: free11.58GiB of475.59GiB. Disk deletion would not directly reclaim active model RAM, and none was attempted.

## Original voice memory evidence

The prior successful original Chatterbox Multilingual typed and microphone receipts record full generation and timings, but no original TTS peak working set or private commit. The smaller optional ONNX model's peak does not establish the original model's requirements. The3GiB admission guard remains unchanged.

The later `public-original-memory.jsonl` read-only monitor began after the first public request's substantial model stages and cannot establish their peaks. It observed a later brief local child with198.52MiB peak working set and276.387MiB peak pagefile before exit. Those values describe an incomplete startup, not loaded MTL inference. Available RAM during this narrow window was3.3088 to3.5077GiB; remaining commit capacity5.1405 to5.4646GiB. The real public request's cancellation and transport failure are separate evidence, not successful speech delivery.

A revised resource admission rule needs a complete monitored original-model turn with simultaneous physical availability, commit reserve, page-in pressure and task child-process peaks. General OS paging behavior alone does not justify lowering the guard or promising responsive operation.

## Subsequent original-model measurement

The authorized controlled public audio request was monitored from before submission through cancellation and process exit. This is a real Whisper/Qwen/Chatterbox attempt using a Windows TTS question fixture, not Ben's physical microphone and not successful final speech delivery.

The original MTL child reached6205.371MiB peak working set and8284.379MiB peak process commit. Sampled private commit reached8236.285MiB. Windows calls the latter peak counter `PeakPagefileUsage`, but it is peak process commit, not an amount of disk paging. See Microsoft's [PROCESS_MEMORY_COUNTERS_EX definition](https://learn.microsoft.com/en-us/windows/win32/api/psapi/ns-psapi-process_memory_counters_ex).

The request began with5.595GiB physical RAM available. During original voice startup, sampled available physical RAM fell to0.0445GiB and remaining commit capacity to0.723GiB. Peak measured page input was122744.882pages/second. STT completed in10.672s and Qwen in12.938s; voice was canceled after31.422s, with55.219s total local time. The2-second monitor can miss briefer troughs, while retained process handles preserve the OS-recorded lifetime peaks.

After task children exited, available physical RAM recovered to6.525GiB and commit capacity to8.6675GiB. No reclaim, model request or process termination was performed by the monitoring agent. Evidence: `public-original-audio-20261108.jsonl` and `public-original-audio-summary.json`.

This measurement supersedes the earlier lack of original-model evidence. The3GiB entry check alone is insufficient for fresh original MTL inference on this computer. Lowering it is not supported. This canceled load does not establish the complete generation peak or a guaranteed safe threshold.
