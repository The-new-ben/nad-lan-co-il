# Project Showroom State Machine And Unit Contract

Date: 2026-06-23

Status: build-ready specification, not runtime implementation.

## Purpose

This packet closes the missing project showroom planning layer:

- explicit state machine
- project and unit JSON contract
- asset verification rules
- map/tour/model/facade fallbacks
- admin field requirements
- screenshot gates

It builds on:

- `strategy/11-project-showroom-3d-spec.md`
- `strategy/war-room/showroom-rebuild-execution-packet.csv`
- `docs/templates/project-showroom-payload.schema.json`
- `assets/projects/rainbow-tel-aviv/showroom-payload.json`
- `assets/projects/dimri-yama/showroom-payload.json`

## Validation Evidence

Current sample payload validation:

- Rainbow Tel Aviv payload passes the existing schema with 17 meta fields, 6 units, 6 drawings, and zero errors.
- Dimri Yama payload passes the existing schema with 18 meta fields, 4 units, 3 drawings, and zero errors.

Passing schema does not mean contractor-ready. It only proves the data shape is currently parseable.

## Core Rule

The visual stage never chooses a fake fallback.

The system must choose exactly one public primary state:

1. official 3D model
2. official facade/elevation
3. concept visual clearly marked as illustrative
4. missing-material request
5. clean unavailable state after asset failure

## Files

- `project-showroom-state-machine.csv`
- `project-showroom-admin-field-matrix.csv`
- `project-showroom-unit-schema.json`
- `project-showroom-state-machine-rtl.html`
- `project-showroom-state-machine-preview.png`
- `project-showroom-state-machine-preview-mobile.png`
- `project-showroom-state-machine-visual-qa.md`

## Implementation Rule

No project showroom implementation can be accepted unless it has:

- one primary asset state
- validated unit payload
- visible selected-unit state
- missing-asset state
- asset-error state
- map unavailable state
- lead payload with project and unit context
- desktop and 390px mobile screenshots

## Remaining Runtime Work

- Wire the visual stage to the state machine.
- Wire unit selection to model camera, facade polygons, or safe list-only mode.
- Add admin fields or import workflow for every required field.
- Capture every state in desktop and mobile screenshots.
- Replace prototype/concept assets with developer-approved assets before contractor sales use.
