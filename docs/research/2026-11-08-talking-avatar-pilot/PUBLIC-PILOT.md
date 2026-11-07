# NadLan small talking pilot

Current at8 November2026. Owner approval: Ben expressly requested publication on the English buying guide and an email with working links. Only WordPress page5154 was replaced, inside its existing `nlagent` markers. Existing content outside the block was preserved exactly. No analytics settings, other page, shared plugin version, domain or DNS change.

- Live: https://nad-lan.co.il/en/buy-property-in-israel/
- Release: `v-1701190a83c6`,14 allowlisted files,4,911,453 bytes. The two review videos load only when opened, not with the widget.
- Phone review: https://nad-lan.co.il/wp-content/uploads/nadlan-avatar/v-1701190a83c6/review/nadlan-small-avatar-phone-final.mp4
- Desktop review: https://nad-lan.co.il/wp-content/uploads/nadlan-avatar/v-1701190a83c6/review/nadlan-small-avatar-desktop-final.mp4
- Clips are local Chrome captures made before deployment. Phone is viewport emulation, not a physical handset. Subsequent actual-public-page evidence is under `evidence/public-relay/live-browser/` and `evidence/public-deployment/`.

## What works and what remains

The original English Chatterbox greeting starts after a trusted first interaction. The small portrait, subtle lips, captions, microphone permission handling, text field, one-click persistent close and clearance from the actual WhatsApp/accessibility controls passed live checks. The homepage has no widget. The character is labelled computer-made.

Public talk-back transport is installed, but the actual public identity question returned503 unavailable, with no job created. Available physical RAM was about1.5GiB against the measured workflow's existing3GiB startup reserve. No successful public generated reply or fast conversation is claimed. Owner applications were not closed. Original local new-voice end-to-end measurement was236.1s; optional faster-engine measurements are separate and that engine is not selected publicly.

The computer must remain on, online and have sufficient resources. The worker is a manually launched hidden process, not an installed boot service. There is no paid server, external paid inference fallback or public listener on this computer.

## Operation

`server.py --voice-engine mtl` serves the unchanged original voice on `127.0.0.1:8769`. `public-relay/worker.py --local-base http://127.0.0.1:8769 --run` polls WordPress outbound. Check for an existing matching process before launching another. The initial public worker PID was13368; inspect current process identity rather than assuming that PID is reusable.

Code Snippet1638, named `HAD682 NadLan one-page talk-back relay`, is active. Its only activation option is `nadlan_talk_enabled`. API namespace is `/wp-json/nadlan-talk/v1`; visitor requests are restricted to the English guide and their session. Read `public-relay/CONTRACT.md` and `WORKER.md` for cancellation, cookie ownership, retention and operational limits. Private authentication is reused only inside scripts from the established owner registry. No credential enters the browser or public bundle.

For a local-only readiness check, run `python public-relay/worker.py --local-base http://127.0.0.1:8769 --check-local`. It loads no credentials or models and makes no public request. A successful check does not prove a public answer.

## Scoped update and recovery

`build_public_package.py` builds only the explicit asset allowlist. `deploy_public_pilot.py --conversation` is a read-only plan. Add `--go` only for an authorized replacement of the same page. It saves a backup, hashes every public asset and rereads the exact page. It refuses to overwrite an intervening edit; that read/check is best-effort, not an atomic CMS transaction.

`restore_public_pilot.py` performs a read-only rollback plan. With `--go`, it restores this deployment's exact prior page only if the current page still matches this deployment's hash. If another editor changed the page, it stops for a scoped review. After restoring, rerun the site's source audit and public browser checks.

To stop public generation, create the single file `.runtime/public-relay.stop`; the owned worker cancels its job and exits. Remove that file deliberately before a new authorized start. `python public-relay/deploy_relay.py --disable --go` disables only the relay option and named snippet, not page content. Existing uploaded versioned assets are retained for recovery.

The initial helper-cleanup pass had a hosting/API discrepancy: temporary snippets1637 and1639 reported inactive and their endpoints disappeared, but subsequent reads still listed the records; repeating DELETE1637 returned500. No active temporary endpoint remains. The permanent relay is unaffected. The first page runner also incorrectly rejected a successful204 DELETE response; that status handling was corrected. Failed receipts and the cleanup correction are retained rather than overwritten. Do not claim those temporary database records were physically deleted.

## Evidence and handoff

`evidence/public-deployment/latest.json` proves exact page/asset readback. `evidence/public-relay/live-browser/receipt.json` records29/29 scoped live checks and explicitly preserves the503 result. `evidence/public-relay/browser-wordpress/receipt.json` records20 transport tests with a controlled model fixture, not real speech inference. Source audit returnedGREEN200, oneH1 and onecanonical. Native owner-profile Chrome was also pressed and photographed.

Ben was emailed the live page and both review clips, with the current voice limitation stated. Shared learning is maintained in `../skill/SKILL.md`. Finish the first character's actual public conversation before starting additional characters. Deployment approval for NadLan does not authorize publishing on Hadmaya or Justice.
