# Showroom overview and apartment selection QA

- Created: 2026-06-24T03:07:27.681Z
- URL: https://nad-lan.co.il/projects/rainbow-tel-aviv/?codex_qa=overview_selection_16923
- Selected unit tested: unit-16-w
- Overall pass: yes

## What this proves

- The first showroom frame opens on a building overview, with no apartment preselected.
- A real buyer click on the visible model apartment target selects the unit.
- The selected unit sets camera orbit and camera target, and opens the selected-apartment card.
- Desktop and 390px mobile screenshots are saved in this folder.

## Desktop

- Pass: yes
- Before active unit: none
- After active unit: unit-16-w
- After camera orbit: 35deg 63deg 38m
- After camera target: -5m 55m 7m

## Mobile 390

- Pass: yes
- Before active unit: none
- After active unit: unit-16-w
- After camera orbit: 35deg 63deg auto
- After camera target: -5m 55m 7m

## Honesty

This proves selection on the authored visible apartment targets and camera movement for the tested unit. It does not prove true click-any-window BIM picking because the project still has only authored unit points, not apartment-level mesh metadata.
