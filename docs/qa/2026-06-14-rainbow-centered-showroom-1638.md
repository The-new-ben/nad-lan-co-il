# QA: Rainbow Centered Showroom 1.63.8

## Reason

Live 1.63.7 prevented a totally blank stage, but Chrome showed the visible tower too low in the viewport and the generic model-viewer hand prompt over the stage. That still did not read like a premium showroom.

## Fix

- Raise the visible fallback tower inside `.nlp3d-scene.has-model-viewer`.
- Hide model-viewer’s generic interaction prompt with `--interaction-prompt-display:none`.
- Keep the 1.63.7 no-blank fallback and hotspot protection.

## Gate

After install, the Rainbow stage should show a visible tower in the main viewport with no generic hand prompt covering it.
