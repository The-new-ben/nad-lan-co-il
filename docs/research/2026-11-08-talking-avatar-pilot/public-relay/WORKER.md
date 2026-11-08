# Outbound local worker

`worker.py` polls the reviewed WordPress relay and calls an existing loopback voice server. It opens no listener, tunnel or public route to this computer. It imports no model and has no paid-provider fallback. Do not upload this Python file or the local verification scripts with the public assets.

The production authentication loader executes only the definitions before the existing `deployskin.py` health call. No deployment body runs. It reuses the helper's private request API and DPAPI-backed application password in memory, rejects a different website origin and disables redirects for authenticated requests. It does not create, copy or print a credential. Ordinary logs contain turn outcome, chunk count and, on failure, a numeric status and allowlisted code. Response bodies, tokens, paths and transcripts are never logged.

Local readiness can be checked without loading credentials, contacting the website or loading models:

```
python public-relay/worker.py --local-base http://127.0.0.1:8769 --check-local
```

After the page and relay have been reviewed and enabled, the authorized launch is explicit:

```
python public-relay/worker.py --local-base http://127.0.0.1:8769 --run
```

Port 8769 preserves the original voice. Selecting the different optional engine requires explicitly changing the port to 8770; the worker never substitutes it automatically. `--once` limits a run to one claim attempt. The worker is not a Windows service and is not installed to start on boot. Use a hidden process when running it from a launcher. Stop it gracefully so it can cancel its current turn and mark itself unavailable. The relay's 45-second lease also expires if the process unexpectedly disappears.

For a hidden process, create `.runtime/public-relay.stop` to request a graceful stop. The active-turn monitor checks this every second, and the idle loop every three seconds. A new launch refuses to run while this file exists; remove it deliberately before restarting. This stops only the relay's current owned local job, never owner applications.

Before claiming, the worker requires a healthy, idle local server supporting request-token cancellation. Original port8769 additionally requires at least7.1GiB available physical RAM AND9.1GiB remaining commit capacity. Both must pass independently. Optional port8770 keeps its existing3GiB physical guard. It reports `ready:false` and `resource_busy` when either required reserve is insufficient. The server retains its own guards. Local decoding validates the actual audio duration before transcription or other model inference; the browser's duration hint is not trusted. No inference is attempted by the readiness check.

The original thresholds follow the controlled8November2026 public audio attempt in `evidence/memory-recovery/public-original-audio-summary.json`: original MTL reached6205.371MiB peak resident memory (6.060GiB) and8284.379MiB peak process commit (8.090GiB) before cancellation. A1GiB reserve rounded upward gives7.1/9.1GiB. Starting with5.595GiB physical RAM was insufficient; sampled availability fell to0.0445GiB. This is an admission safeguard based on an interrupted load, not a guarantee of the complete generation peak or acceptable latency. It does not approve an automatic engine substitution.

Both reserve readings use Windows `GlobalMemoryStatusEx`. `ullAvailPhys` supplies physical availability; `ullAvailPageFile` supplies remaining commit capacity available to the process. The latter is not free disk space or current pagefile usage. A failed native query returns zero reserves. No pagefile or system settings are changed.

Each public `ownerKey` has a separate in-memory local session cookie. The same visitor reuses that session and its four-turn history. Different visitors never share a cookie or history. The map is limited to 128 visitors and evicts idle entries after 30 minutes. Restarting this worker resets those mappings. The existing local backend retains its private diagnostic files under `.runtime/jobs` and response files under `responses`; WordPress's separate 15-minute transient retention does not delete those local diagnostics.

The worker checks public cancellation and deadlines every second and renews its 45-second lease every ten seconds. Cancellation, deadline expiry, lost lease or transport uncertainty cancels the visitor's local request token, even while the initial upload is waiting. If a job ID arrives late, that owned job is also canceled. No other visitor's cookie or job is used. Cancelled or failed turns never send a successful completion.

Only exact HTTP429 with WordPress code `busy` is retried, because the relay lock rejects it before running the route callback. There are at most three total attempts, with0.3s and0.9s delays. Each turn retry rechecks cancellation and deadline. Rate limits, authentication failures,404/409, other statuses and uncertain transport are never replayed.

Available chunks are fetched with the same visitor's local cookie and forwarded once per index. The final combined recording is separately uploaded for complete replay. The PHP relay checks lease ownership again before accepting every update, closing the race between local checks and public cancellation. It removes published chunks on later failure. Only loopback response paths and bounded mono PCM WAVs are accepted; no arbitrary URL is fetched. Progress and public errors exclude diagnostic paths and stack traces.

`verify_worker.py` uses real loopback HTTP servers with controlled silent audio and a model fixture. It verifies visitor isolation, reuse, cumulative chunk deduplication, full replay, multipart audio, cancellation before an ID arrives, later-sentence failure, lease loss, bounded lock retries and resource admission. Independent physical/commit mismatches are checked for8769;8770 retains its existing behavior. It loads no production credentials and sends no public request. Latest receipt: `evidence/public-relay/worker-controls-resource-admission.json`; previous controls are retained. This is transport/control evidence, not model quality, public hosting or first-audible latency evidence.

`verify_wordpress_worker.py` also passed against the isolated real WordPress 7.1.3/PHP relay on port 8797, using only its temporary local credentials and a silent loopback model fixture. The test covers two sentence publications and full replay, visitor ownership, reuse, outsider denial and cancellation before the local job ID arrives. The first attempt exposed a diagnostic race when PHP rejected a progress update before the cancellation monitor noticed the close. The worker now confirms the remote terminal state after a 409; the failure log and corrected pass are both retained. See `evidence/public-relay/wordpress-worker-integration.json` and `wordpress-worker-initial-failure.log`. No production request or actual speech inference occurred in this integration test.

`verify_browser_wordpress.py` then passed 20 native Chrome checks against the real local WordPress relay and this worker. It verified cookie/CSRF setup, typed two-chunk playback and full replay, visitor isolation, native MediaRecorder WebM bytes and duration, expiry recovery with exactly one retry, close during session refresh, close during playback and actual page-navigation cancellation. The model backend used prerecorded greeting excerpts; no STT, Qwen or TTS inference ran. Browser lip analysis and playback were real. The preliminary harness timing failure is retained separately. Evidence is under `evidence/public-relay/browser-wordpress/`. Its `package-compatibility.json` verifies that the final public package only adds the two review videos to the browser-tested core files.
