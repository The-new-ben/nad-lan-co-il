# Relay implementation and verification

Prepared locally on 8 November 2026 for HAD-682. Only this directory and local evidence were changed. The shared NadLan plugin, release version, live WordPress, DNS and public listeners were untouched. The module defaults to disabled through `get_option('nadlan_talk_enabled', false)`.

`nadlan-talk-relay.php` supplies the one-page REST contract in CONTRACT.md. It is standalone and can be loaded as a guarded module or as an authenticated Code Snippets body after stripping the opening PHP tag. Installing/loading the code does not set the enable option. The root coordinator owns deployment and the separate enable decision.

The implementation uses a signed visitor cookie, visitor-bound CSRF, exact Origin and guide Referer checks, real application-password authentication for worker-only routes, owner checks for jobs and audio, pre-registration cancellation tombstones, a finite queue, expiring worker leases, bounded private transient payloads and no-store API responses. Browser microphone input is <=20seconds by hint and <=15MiB by entire body; actual decoded duration is checked by the existing local backend before model inference. The worker reaches the website outbound and keeps a separate local session per visitor. No public port or tunnel is required.

Actual isolated verification used the existing WordPress7.1.3 core and official SQLite Database Integration plugin, with a fresh database and fixture-only credentials. Existing Atlas/TALVE sites were not modified. Outbound WordPress HTTP and mail were blocked in the fixture. The local PHP8.3.33 server binds127.0.0.1:8797.

| Evidence | Result | What it establishes |
| --- | --- | --- |
| `../evidence/public-relay/php-controls.json` | 29/29 | Actual REST authentication, session separation, CSRF/origin/page checks, idempotency, authorized exact WAV bytes, cancellation, expired lease and queue capacity. |
| `../evidence/public-relay/php-upload-controls.json` | 8/8 | Actual multipart parsing and exact upload recovery, public/private field separation, duration hints, error no-store headers, per-session starts and global payload capacity. The capacity case sets accounted bytes to the cap instead of allocating128MiB. |
| `../evidence/public-relay/wordpress-worker-integration.json` | 4/4 | Real Python worker to real PHP/WordPress, with a silent local backend fixture: repeated/split visitors, two chunks and full replay, unauthorized audio denial and cancellation before the local ID arrives. |
| `../evidence/public-relay/worker-controls.json` | Separate worker controls | See worker documentation and its latest count; these are controlled HTTP fixtures, not inference. |

Failures were retained. Initial binary audio did not survive text transient storage; the implementation now base64-encodes private input/output payloads and checks write success. A missing CSRF header initially raised a PHP8 type error; it now correctly returns403. The cross-language test also exposed a worker-only diagnostic race after PHP correctly rejected a cancelled write; the worker now confirms terminal cancellation after409. Original receipts/logs remain alongside the successful ones.

The module currently accounts at most128MiB of raw payloads; database base64 overhead is additional. Jobs expire after900seconds. Read access ends immediately at expiry; physical deletion is request/WordPress-cron driven, not a wall-clock deletion guarantee when no requests arrive. The one-page guide cache and analytics settings are not changed.

Limits: this test ran WordPress on SQLite/PHP's single-threaded development server, not UPress MySQL or its edge cache/proxy. HTTPS Secure-cookie behavior requires actual live readback; the isolated HTTP fixture verifies HttpOnly/Strict and the source selects Secure when WordPress reports HTTPS. No public microphone, real remote Chatterbox answer, physical handset, provider capacity or first-audible latency was established. The actual computer's3GiB startup guard remains in force. Reuse the existing Chatterbox voice by default; transport verification does not approve the alternate candidate voice.

For any later public enablement, verify live namespace routing, cookie flags and no-store headers first, then use two separate visitor sessions and an actual remote-network browser. Verify cancellation before ID, cancellation during inference, no late audio, offline/busy behavior and the selected voice before describing an emailed test link as working talk-back.
