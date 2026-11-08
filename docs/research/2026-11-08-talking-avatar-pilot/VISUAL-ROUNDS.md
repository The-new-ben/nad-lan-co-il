# Local visual refinement, 7 November 2026

The original fictional blonde from `../kit/face-a.png` remains the sole identity source. No new character was generated. This is a local prototype, with no WordPress changes or paid service use.

The four visual iterations below correspond to three full browser review batches. The closed-eye asset iteration was incorporated into the head-only version before the second full browser batch. Focused panel, cancellation and narrow-phone checks are additional targeted checks, not extra full review batches.

The UI follows the existing Claude Design NadLan Instruments identity: ink `#0F2233` and `#12202A`, sea `#2F6F86`, mist `#D3DCE2`, IBM Plex Sans. The small transparent head and instrument-like controls follow this subject's palette, avoiding cream, gold and generic card styling. The article is an unmodified read-only fixture of the source page.

## Round 1: landmark baseline

Preserved at `iterations/01-landmark-baseline/`. The image-derived mesh had real landmark depth, but its projected eye closure looked like a squint. The hair retained some window blue at the perimeter. The visible bust and large status pill competed with the requested small face. Behavior passed 35 checks at four sizes; visual limitations remained.

Evidence: `evidence/round-01/phone-waiting.png`, plus desktop, phone-small and landscape screenshots.

## Round 2: closed eyes and original likeness

Preserved at `iterations/02-closed-eyes/`. The original `frame-BLINK.png` was projected onto the same shaped mesh and crossfaded locally. The prior blink morph stays at zero. This removes texture collapsing through the iris. Semi-transparent hair edges were decontaminated from neighboring opaque hair. Broad shoulder cropping was still visually distracting.

## Round 3: head only and smaller controls

This iteration introduced `assets/nadlan-advisor-v2.glb` and editable `nadlan-advisor-v2.blend`. Clothing was removed from the texture using the local segmentation result, the short neck fades below the chin, and the camera fit the head more closely. The status pill, disclosure and visible close control became smaller; all control hit areas remained 44 pixels. The footprint at this historical stage was 144 by 160 pixels on mobile and 170 by 184 on desktop. Round 4 below records the final dimensions after improving disclosure readability. Idle yaw is bounded to about 2.4 degrees.

Transparent RGB pixels were cleared without changing visible pixels, reducing the v2 GLB from 3,493,748 to 953,224 bytes. Remaining blue-gray hair edge contamination is still visible in enlarged inspection and should not be described as a perfect strand matte.

Evidence: `evidence/round-02-head-only/` contains a second 35/35 behavior run and screenshots at 390, 360, 1366 and 844 landscape widths. `assets/blender-v2-front.png`, `blender-v2-speaking.png`, `blender-v2-blink.png`, `blender-v2-angle--3.png`, `blender-v2-angle-3.png` and `blender-v2-wireframe.png` are actual Blender 5.2.1 renders. The 25-degree render is inspection evidence of inferred depth, outside the intended production turn range.

## Round 4: Claude Design review applied

The parent agent obtained an actual Claude Design review at [the design artifact](https://claude.ai/design/p/80d1d297-8f1d-4874-8d77-2c7b07d5480f?file=HAD-682+Talking+Head+Polish.dc.html). Its remaining useful changes were applied: right anchoring at 12 pixels on phone and 24 on desktop preserves the starts of article lines; disclosure is now 10/12 pixels on phone and 11/14 on desktop; the visible close control is 20 pixels, microphone 28 and CC 24 by 18, with all hit areas 44 pixels. Portrait dimensions are 118 by 142 on phone and 150 by 174 on desktop, total footprints 144 by 166 and 176 by 198. Side controls sit above the disclosure to avoid obscuring its last letters.

`evidence/round-03-claude-review/` records another 35 passed behavior checks at four sizes. `evidence/panels/` records 17 checks for expanded caption bounds, clear site controls, reachable close, silent caption opening and a same-character fallback when the GLB fails. Existing WhatsApp/accessibility rectangles are measured at runtime, not assumed. The earlier round screenshots remain available for comparison.

## Dynamic speech integration

`evidence/dynamic-integration/results.json` records six passed checks in real local Chrome. A supplied audio response was analyzed into 139 events over 11.805 seconds, then played through the widget using that learned timeline. Recorded mouth influence stayed between 0 and approximately 0.467. Stopping returns to neutral, and closing during analysis prevents later playback. The existing English Chatterbox greeting is unchanged. This test demonstrates arbitrary audio timing integration, not a live language-model conversation; the backend test is separate.

## Limits

This asset is an inferred front surface derived from one approved photograph, with a curved hair perimeter and dedicated mouth opening. The unseen sides, ears and back were not reconstructed. It must not be called a complete 360-degree volumetric head. The unlit photographic material preserves likeness but does not respond to scene lighting like a fully shaded skin model. There is one mouth-opening shape, so round and spread visemes are reduced to small opening and closure. No claim of frontier-level realism or superiority is supported by these checks.
