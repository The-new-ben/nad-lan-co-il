# NadLan small talking pilot

Current at8 November2026. Owner approval: Ben expressly requested publication on the English buying guide and an email with working links. Only WordPress page5154 was replaced, inside its existing `nlagent` markers. Existing content outside the block was preserved exactly. No analytics settings, other page, shared plugin version, domain or DNS change.

- Live: https://nad-lan.co.il/en/buy-property-in-israel/
- Current release: `v-6dff055c6784`, 14 allowlisted files, 4,914,004 bytes. The two review videos load only when opened, not with the widget. Their original versioned URLs below remain valid and intentionally unchanged.
- Intentional recovery link: https://nad-lan.co.il/en/buy-property-in-israel/#talk
- Phone review: https://nad-lan.co.il/wp-content/uploads/nadlan-avatar/v-1701190a83c6/review/nadlan-small-avatar-phone-final.mp4
- Desktop review: https://nad-lan.co.il/wp-content/uploads/nadlan-avatar/v-1701190a83c6/review/nadlan-small-avatar-desktop-final.mp4
- Clips are local Chrome captures made before deployment. Phone is viewport emulation, not a physical handset. Subsequent actual-public-page evidence is under `evidence/public-relay/live-browser/` and `evidence/public-deployment/`.

## What works and what remains

The portrait reveals on entry with explicit `revealDelay:0`; sound still waits for a trusted interaction. The original English Chatterbox greeting, small portrait, subtle lips, captions, microphone permission handling, text field, one-click persistent close and clearance from the actual WhatsApp/accessibility controls passed live checks. Both `/` and `/en/` had no widget in the scoped recovery checks. The character is labelled computer-made. The same approved face, original voice, ink/sea palette and IBM Plex Sans remain in use.

A saved close from either the old large card or this portrait uses `nlag-closed`. Previously that hid the character permanently without a recovery control. The current release leaves a 72 by 44 pixel **Talk** button when closed. A trusted click reopens one guide and starts the original greeting. The `#talk` link deliberately clears only that dismissal and reveals the guide silently; it consumes the fragment so a later close remains closed on ordinary reload. Sound still requires a trusted interaction.

Public talk-back transport is installed, but no completed public spoken reply is established. The initial public identity question returned 503 before admission. A later controlled public WAV request was accepted and completed transcription in 10.672 s and Qwen in 12.938 s, then was cancelled for critical memory during original Chatterbox loading/generation. Local total was 55.219 s; HTTP test elapsed time was 58.172 s. Input was a Windows-synthesized question, not Ben or a physical microphone; browser playback was not tested. The original voice process reached 6.060 GiB peak resident memory and 8.090 GiB peak commit before cancellation, while sampled free physical RAM reached 0.0445 GiB. These are dated test observations, not current availability or a complete synthesis peak.

The public worker now admits original port 8769 work only when at least 7.1 GiB physical RAM and 9.1 GiB commit capacity are available. Both independent conditions must pass. The optional port 8770 candidate retains its existing 3 GiB physical check and is not selected publicly. The stronger original-voice gate follows the interrupted measurement plus reserve; it does not guarantee completion or latency. Loader optimization is still pending. Check current readiness rather than copying an old free-RAM value. Owner applications were not closed. Original historical local new-voice end-to-end measurement was 236.1 s; separate optional-engine timings do not describe this public configuration.

The [original MTL loader candidate](research/original-mtl-loader-proposal.md) is prepared, compiled and independently reviewed at source level. Its guarded launcher was invoked once, but [preflight stopped it before any child or model started](evidence/original-mtl-loader-candidate/parent-receipt.json): 1.4583 GiB physical and 1.6194 GiB commit capacity were available against this isolated experiment's 6/8 GiB minimum. That experimental minimum does not replace public admission's 7.1/9.1 GiB. No candidate inference, memory-saving measurement, audio comparison or production change occurred. At this handoff, worker 23712 remains running behind the unavailable resource gate and the recorded greeting remains live. Ben explicitly instructed that both Claude Desktop and GrokBot remain open. Preserve both applications; no owner application was terminated, and there is no pending app-closure decision. Work on other existing candidate options continues.

The first actual user microphone upload must not be described simply as a too-short recording: its WebM has a 234.095 s timestamp gap. The existing 20.1 s timeline cutoff left only 0.119 s decoded audio, below the 0.25 s transcription minimum. A later upload decoded 4.02 s, completed Whisper and Qwen and reached original TTS before cancellation. The old worker log does not establish that cancellation's cause; do not attribute it to HTTP 429 without the visitor's request evidence. Sanitized findings are in `evidence/public-relay/recent-job-diagnostics.json`.

The computer must remain on, online and have sufficient resources. The worker is a manually launched hidden process, not an installed boot service. There is no paid server, external paid inference fallback or public listener on this computer.

## Operation

`server.py --voice-engine mtl` serves the unchanged original voice on `127.0.0.1:8769`. `public-relay/worker.py --local-base http://127.0.0.1:8769 --run` polls WordPress outbound. At this 8 November handoff the guarded worker is PID 23712 and the unchanged original server is PID 25516. The earlier worker PID 13368 is historical. Check current process identity before starting or stopping anything; PIDs are not durable ownership proof.

The browser retries only an accepted job's GET poll when HTTP 429 has the recognized `busy` code, with at most three extra attempts and 1/2/4 s delays. A larger numeric or HTTP-date `Retry-After` is respected within the response deadline. A successful poll resets the counter. Other rate/authentication failures are not retried, and this change never resubmits the question POST. Close aborts pending waits and cancels the owned job. The worker separately retries recognized private-call contention within its bounded contract.

Code Snippet1638, named `HAD682 NadLan one-page talk-back relay`, is active. Its only activation option is `nadlan_talk_enabled`. API namespace is `/wp-json/nadlan-talk/v1`; visitor requests are restricted to the English guide and their session. Read `public-relay/CONTRACT.md` and `WORKER.md` for cancellation, cookie ownership, retention and operational limits. Private authentication is reused only inside scripts from the established owner registry. No credential enters the browser or public bundle.

For a local-only readiness check, run `python public-relay/worker.py --local-base http://127.0.0.1:8769 --check-local`. It loads no credentials or models and makes no public request. A successful check does not prove a public answer.

## Scoped update and recovery

`build_public_package.py` builds only the explicit asset allowlist. `deploy_public_pilot.py --conversation` is a read-only plan. Add `--go` only for an authorized replacement of the same page. It saves a backup, hashes every public asset and rereads the exact page. It refuses to overwrite an intervening edit; that read/check is best-effort, not an atomic CMS transaction.

`restore_public_pilot.py` performs a read-only rollback plan. With `--go`, it restores this deployment's exact prior page only if the current page still matches this deployment's hash. If another editor changed the page, it stops for a scoped review. After restoring, rerun the site's source audit and public browser checks.

To stop public generation, create the single file `.runtime/public-relay.stop`; the owned worker cancels its job and exits. Remove that file deliberately before a new authorized start. `python public-relay/deploy_relay.py --disable --go` disables only the relay option and named snippet, not page content. Existing uploaded versioned assets are retained for recovery.

The initial helper-cleanup pass had a hosting/API discrepancy: temporary snippets1637 and1639 reported inactive and their endpoints disappeared, but subsequent reads still listed the records; repeating DELETE1637 returned500. No active temporary endpoint remains. The permanent relay is unaffected. The first page runner also incorrectly rejected a successful204 DELETE response; that status handling was corrected. Failed receipts and the cleanup correction are retained rather than overwritten. Do not claim those temporary database records were physically deleted.

## Evidence and handoff

`evidence/public-deployment/latest.json` proves exact current page/asset readback and unchanged content outside the existing block. Current evidence:

- `evidence/visibility-recovery/v-6dff055c6784-live/receipt.json`: 16 fresh live checks at 390 and 1366 pixels, including actual zero-delay config, original greeting, close/Talk, persistence, obstacle clearance and exact JS/CSS hashes. No avatar API POST or conversation inference.
- `evidence/latency/poll-busy-retry/v-6dff055c6784/receipt.json`: 47 controlled local polling checks, actual packaged browser and prerecorded audio. Earlier mixed-build evidence is retained as superseded.
- `evidence/visibility-recovery/v-6dff055c6784/immediate-config/receipt.json`: seven local zero-delay, silence and persistent-choice checks.
- `evidence/public-relay/worker-controls-resource-admission.json`: 28 controlled worker checks, including independent physical/commit admission conditions and bounded contention retries; no model inference.
- `evidence/public-relay/real-reply-recovery/receipt.json` and `evidence/memory-recovery/public-original-audio-summary.json`: the genuine public controlled-WAV attempt and memory cancellation described above, not completed audio.

Previous recovery evidence remains: 40 local checks in `evidence/visibility-recovery/v-2d37e9a1a8ad/receipt.json`, 28 live checks in its `-live/receipt.json`, and owner-profile phone-size screenshot `evidence/visibility-recovery/live-native-phone.png`. These retain keyboard, silent fragment and delayed-GLB coverage; do not relabel them as fresh checks of the later release.

The initial `evidence/public-relay/live-browser/receipt.json` retains 29/29 scoped live checks and the 503 result. `evidence/public-relay/browser-wordpress/receipt.json` retains 20 transport tests with a controlled model fixture, not real speech inference. Source audit returned GREEN 200, one H1 and one canonical. Historical releases, videos, failure receipts and the initial visibility reproduction remain available.

Ben was emailed the live page and both review clips, with the current voice limitation stated. Shared learning is maintained in `../skill/SKILL.md`. Finish the first character's actual public conversation before starting additional characters. Deployment approval for NadLan does not authorize publishing on Hadmaya or Justice.
