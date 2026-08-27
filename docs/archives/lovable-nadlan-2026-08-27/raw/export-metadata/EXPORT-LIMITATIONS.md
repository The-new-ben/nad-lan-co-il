# Export limitations

## Official ZIP/source download

The Lovable editor was inspected for a native source download. The visible editor exposes Preview, Code, More, and Connectors, but no direct ZIP/download action. The project reports “No connections yet”. A GitHub/Connector connection would change external account state and was explicitly out of scope, so it was not started.

The official Lovable connector does not expose a bulk ZIP export tool. It exposes `list_files` and one-file-at-a-time `read_file`; those were used to export every text file.

## Binary fidelity

The manifests contain 80 binary files: one Design Lab favicon and 79 Strategy Hub images/screenshots/assets. `read_file` returns binary content through a text channel, which is lossy for arbitrary bytes. The binary payloads were therefore not written as corrupted files. Their exact paths remain in each project’s `file-manifest.json` and are collected in `binary-assets-unexported.json`.

## Screenshots

The first full-page capture of `/production/nadlan` timed out in the browser’s full-page capture operation. Following the approved fallback, 1440×900 viewport screenshots were saved instead for all 11 Design Lab Nadlan routes.

Mobile screenshots and the two Strategy Hub screenshots were not continued after the user indicated that the current material was sufficient and asked to stop adding scope. Their URLs, titles, H1 values, and data-state notes remain in `route-index.json`.

## Privacy and changes

- No cookies, session tokens, browser-profile data, user IDs, passwords, environment values, or unrelated project data were saved.
- No publish, deploy, generation, source edit, privacy change, Git connection, connector installation, deletion, or account change was performed.
- A private preview URL used by the signed-in editor contained a short-lived access token. It was not copied into any export file or report.

